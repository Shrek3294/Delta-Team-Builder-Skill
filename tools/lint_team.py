#!/usr/bin/env python3
"""Deterministic factual linter for Cobblemon Delta team deliverables.

Parses the 6-row team table at the top of a teams/<name>.md deliverable and
checks every shipped set against ground-truth data (no model prior involved):

  HARD FAIL (blocks export, exit 1):
    - species can't be resolved to a data/mons file
    - banned mon (notes/banlist.md, parsed -> canonical token-sets)
    - illegal move (not in legalMoves[], not on the data-gap allowlist)
    - illegal ability (not in base/mega abilities, not on the exception allowlist)
    - known item/holder mismatch (data/item_locks.json)
    - Tera line in set syntax
    - doc-hygiene violations (em/en dash, customer language, internal data refs)
    - missing / empty / stale verifier sidecar (teams/<name>.verify.md, hash-bound)

  WARN (reported, never blocks):
    - phantom mon residue in identity/role/wincon prose
    - an "-ite"/"-z" looking locked item not present in item_locks.json

Importable: lint_file(path, require_verify=True) -> LintResult.
CLI: python tools/lint_team.py <file.md> [--no-require-verify]   (exit 1 on HARD FAIL)

This module is the single source of truth for mechanical checks. It is invoked
both by tools/md_to_docx_pdf.py (fail-closed, before conversion) and by the
PreToolUse hook in .claude/settings.json.
"""
import sys
import os
import re
import json
import glob
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONS_DIR = os.path.join(ROOT, "data", "mons")
BANLIST = os.path.join(ROOT, "notes", "banlist.md")
ITEM_LOCKS = os.path.join(ROOT, "data", "item_locks.json")
ALLOWLISTS = os.path.join(ROOT, "data", "lint_allowlists.json")
DENIAL_LOG = os.path.join(ROOT, "teams", ".lint-denials.log")


# ---------- normalization ----------

def collapse(name):
    """Lowercase, strip every non-alphanumeric char. 'Mega Raichu-Y' -> 'megaraichuy'."""
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def tokens(name):
    """Order-independent token set. 'Raichu-Mega-Y' and 'Mega Raichu-Y' both -> {raichu,mega,y}."""
    return frozenset(t for t in re.split(r"[^a-z0-9]+", (name or "").lower()) if t)


# ---------- data loading ----------

class Data:
    """Lazily-built indexes over data/mons, banlist, item locks, allowlists."""

    def __init__(self, mons_dir=MONS_DIR, banlist=BANLIST,
                 item_locks=ITEM_LOCKS, allowlists=ALLOWLISTS):
        self.mons_dir = mons_dir
        self.collapsed_to_stem = {}      # 'tinkatongamma' -> 'tinkaton-gamma'
        self.tokens_to_stem = {}         # frozenset -> 'tinkaton-gamma'
        self.alias_collisions = []       # (key, stem_a, stem_b) for tests
        self._mon_cache = {}
        self._build_alias_map()
        self.ban_token_sets, self.ban_collapsed = self._parse_banlist(banlist)
        self.item_locks = self._load_item_locks(item_locks)
        self.move_gaps, self.ability_exceptions = self._load_allowlists(allowlists)

    def _register(self, key_collapsed, key_tokens, stem):
        if key_collapsed:
            prev = self.collapsed_to_stem.get(key_collapsed)
            if prev and prev != stem:
                self.alias_collisions.append((key_collapsed, prev, stem))
            else:
                self.collapsed_to_stem[key_collapsed] = stem
        if key_tokens:
            prev = self.tokens_to_stem.get(key_tokens)
            if prev and prev != stem:
                self.alias_collisions.append((tuple(sorted(key_tokens)), prev, stem))
            else:
                self.tokens_to_stem[key_tokens] = stem

    def _build_alias_map(self):
        for path in glob.glob(os.path.join(self.mons_dir, "*.json")):
            stem = os.path.splitext(os.path.basename(path))[0]
            names = {stem}
            try:
                d = json.load(open(path, encoding="utf-8"))
            except Exception:
                d = {}
            sp = d.get("species") or {}
            cur = d.get("_curated") or {}
            for k in ("displayName", "speciesId", "speciesKey"):
                if sp.get(k):
                    names.add(sp[k])
                if cur.get(k):
                    names.add(cur[k])
            for a in (cur.get("aliases") or []):
                names.add(a)
            for n in names:
                self._register(collapse(n), tokens(n), stem)

    def resolve(self, name):
        """Display name -> data/mons stem, or None. Tries collapsed then token-set."""
        c = collapse(name)
        if c in self.collapsed_to_stem:
            return self.collapsed_to_stem[c]
        t = tokens(name)
        return self.tokens_to_stem.get(t)

    def load_mon(self, stem):
        if stem not in self._mon_cache:
            path = os.path.join(self.mons_dir, stem + ".json")
            try:
                self._mon_cache[stem] = json.load(open(path, encoding="utf-8"))
            except Exception:
                self._mon_cache[stem] = {}
        return self._mon_cache[stem]

    # ----- banlist -----

    BAN_SECTIONS_SKIP = ("quick sanity", "when to apply")

    def _parse_banlist(self, path):
        token_sets, collapsed = set(), set()
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            # Fail loud: a banlist we can't read means the ban check is blind.
            raise RuntimeError("lint_team: cannot read banlist at %s" % path)
        in_ban_block = False
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("## "):
                heading = s[3:].lower()
                # Ban-bearing top-level sections only.
                in_ban_block = ("currently banned" in heading
                                or "historical bans" in heading)
                continue
            if s.startswith("### "):
                continue  # subsection header inside a ban block; keep state
            if not in_ban_block:
                continue
            if not s.startswith("- "):
                continue
            name = s[2:].strip().lstrip("*").strip()
            # Cut description after the first separator.
            for sep in (" — ", " – ", " (", ":", " --"):
                idx = name.find(sep)
                if idx != -1:
                    name = name[:idx]
            name = name.strip().strip("*").strip()
            if name:
                token_sets.add(tokens(name))
                collapsed.add(collapse(name))
        if not collapsed:
            raise RuntimeError("lint_team: banlist parser found no banned entries "
                               "(format changed?) at %s" % path)
        return token_sets, collapsed

    def is_banned(self, name, stem=None):
        if tokens(name) in self.ban_token_sets or collapse(name) in self.ban_collapsed:
            return True
        if stem:
            d = self.load_mon(stem)
            sp = d.get("species") or {}
            cur = d.get("_curated") or {}
            cands = [stem, sp.get("displayName"), cur.get("displayName")]
            cands += (cur.get("aliases") or [])
            for c in cands:
                if c and (tokens(c) in self.ban_token_sets
                          or collapse(c) in self.ban_collapsed):
                    return True
        return False

    # ----- item locks / allowlists -----

    def _load_item_locks(self, path):
        merged = {}
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            return merged
        for section, mapping in d.items():
            if section.startswith("_") or not isinstance(mapping, dict):
                continue
            for item, stems in mapping.items():
                merged[collapse(item)] = list(stems)
        return merged

    def _load_allowlists(self, path):
        move_gaps, abil = set(), set()
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            return move_gaps, abil
        for e in d.get("move_gaps", []):
            move_gaps.add((collapse(e["species"]), collapse(e["move"])))
        for e in d.get("ability_exceptions", []):
            abil.add((collapse(e["species"]), collapse(e["ability"])))
        return move_gaps, abil

    # ----- per-mon helpers -----

    def base_stem(self, stem):
        """Strip a -mega/mega- (and -mega-x/y) marker to the base form stem if it exists."""
        for variant in (
            re.sub(r"(^mega-|-mega(-[xyz])?$)", "", stem),
            stem.replace("-mega-x", "").replace("-mega-y", "").replace("-mega", ""),
        ):
            if variant and variant != stem and os.path.exists(
                    os.path.join(self.mons_dir, variant + ".json")):
                return variant
        return None

    def legal_move_set(self, stem):
        d = self.load_mon(stem)
        out = set()
        for m in (d.get("legalMoves") or []):
            if m.get("id"):
                out.add(collapse(m["id"]))
            if m.get("displayName"):
                out.add(collapse(m["displayName"]))
        return out

    def ability_set(self, stem):
        d = self.load_mon(stem)
        sp = d.get("species") or {}
        out = {collapse(a) for a in (sp.get("abilities") or [])}
        b = self.base_stem(stem)
        if b:
            bd = self.load_mon(b)
            bsp = bd.get("species") or {}
            out |= {collapse(a) for a in (bsp.get("abilities") or [])}
        return out


# ---------- result type ----------

class LintResult:
    def __init__(self):
        self.hard = []   # list[str]
        self.warn = []   # list[str]

    @property
    def ok(self):
        return not self.hard

    def report(self):
        lines = []
        if self.hard:
            lines.append("HARD FAIL (%d):" % len(self.hard))
            lines += ["  x " + h for h in self.hard]
        if self.warn:
            lines.append("WARN (%d):" % len(self.warn))
            lines += ["  ! " + w for w in self.warn]
        if not lines:
            lines.append("OK - no issues.")
        return "\n".join(lines)


# ---------- table parsing ----------

def parse_team_table(text):
    """Return up to 6 rows: dicts {pokemon,item,ability,moves:[...],role}.

    Finds the first markdown table whose header row contains Pokemon and Moves.
    Returns (rows, error_or_None). error set if a table is expected but unparseable.
    """
    lines = text.splitlines()
    header_idx = None
    for i, ln in enumerate(lines):
        low = ln.lower()
        if ln.lstrip().startswith("|") and "pokemon" in low and "move" in low:
            header_idx = i
            break
    if header_idx is None:
        return [], "no team table found (header row with Pokemon + Moves)"

    def cells(ln):
        parts = [c.strip() for c in ln.strip().strip("|").split("|")]
        return parts

    header = [c.lower() for c in cells(lines[header_idx])]

    def col(name):
        for j, h in enumerate(header):
            if name in h:
                return j
        return None

    ci = {k: col(k) for k in ("pokemon", "item", "ability", "move", "role")}
    if ci["pokemon"] is None or ci["move"] is None:
        return [], "team table missing Pokemon or Moves column"

    rows = []
    i = header_idx + 1
    if i < len(lines) and set(cells(lines[i])[0] if cells(lines[i]) else "") <= set("-: "):
        i += 1  # skip the |---|---| separator
    while i < len(lines):
        ln = lines[i]
        if not ln.lstrip().startswith("|"):
            break
        c = cells(ln)
        if all(not x or set(x) <= set("-: ") for x in c):
            i += 1
            continue

        def get(key):
            j = ci[key]
            return c[j] if j is not None and j < len(c) else ""
        moves = [m.strip() for m in re.split(r"[,/]", get("move")) if m.strip()]
        rows.append({
            "pokemon": get("pokemon").strip().strip("*"),
            "item": get("item").strip(),
            "ability": get("ability").strip(),
            "moves": moves,
            "role": get("role").strip(),
        })
        i += 1
        if len(rows) >= 6:
            break
    if not rows:
        return [], "team table header found but no data rows parsed"
    return rows, None


# ---------- hygiene / tera / phantom ----------

HYGIENE_PATTERNS = [
    (re.compile(r"[—–]"), "em/en dash (use a comma or rewrite)"),
    (re.compile(r"(?i)\b(customer|as requested|client'?s draft|you asked|your team)\b"),
     "customer-facing language"),
    (re.compile(r"(?i)(1500\+|%\s*usage|usage\s*%|dominant spread|json gap|_curated|auto-gen|the scrape)"),
     "internal data reference"),
]
TERA_RE = re.compile(r"(?im)^\s*tera\s?(type)?\s*:")
# Phantom check is restricted to the "team identity" section only. Per-mon role
# paragraphs and matchup/win-condition prose legitimately name other mons, so
# scanning them produces noise (Codex round 1). WARN-only regardless.
WINCON_HEADINGS = ("identity",)
CAND_RE = re.compile(r"\b([A-Z][a-zA-Z]+(?:[- ][A-Z][a-zA-Z0-9]+)*)\b")


def _hygiene(text, res):
    for rx, label in HYGIENE_PATTERNS:
        for m in rx.finditer(text):
            res.hard.append("hygiene: %s -> '%s'" % (label, m.group(0)))
    if TERA_RE.search(text):
        res.hard.append("Tera line present (Tera is banned in ranked)")


def _phantom(text, team_stems, data, res):
    """WARN-only, section-aware: non-team mon names in identity/role/wincon prose."""
    lines = text.splitlines()
    in_section = False
    seen = set()
    for ln in lines:
        s = ln.strip()
        if s.startswith("#"):
            h = s.lstrip("#").strip().lower()
            in_section = any(k in h for k in WINCON_HEADINGS)
            continue
        if not in_section:
            continue
        for m in CAND_RE.finditer(ln):
            cand = m.group(1)
            stem = data.resolve(cand)
            if stem and stem not in team_stems and stem not in seen:
                seen.add(stem)
                res.warn.append("possible phantom mon in identity/role prose: '%s' (%s) not on the team"
                                % (cand, stem))


# ---------- verifier sidecar ----------

SHA_RE = re.compile(r"(?im)^\s*source-sha256\s*:\s*([0-9a-f]{64})\b")


def _sidecar_path(src_path):
    base = os.path.splitext(src_path)[0]
    return base + ".verify.md"


def check_sidecar(src_path, res):
    side = _sidecar_path(src_path)
    if not os.path.exists(side):
        res.hard.append("verifier sidecar missing: %s (run the verifier step)" % os.path.basename(side))
        return
    content = open(side, encoding="utf-8").read().strip()
    if not content:
        res.hard.append("verifier sidecar is empty: %s" % os.path.basename(side))
        return
    m = SHA_RE.search(content)
    if not m:
        res.hard.append("verifier sidecar missing 'source-sha256:' header: %s" % os.path.basename(side))
        return
    actual = hashlib.sha256(open(src_path, "rb").read()).hexdigest()
    if m.group(1).lower() != actual:
        res.hard.append("verifier sidecar is stale: source-sha256 does not match %s "
                        "(re-run the verifier after editing the draft)" % os.path.basename(src_path))


# ---------- main lint ----------

def lint_text(text, data=None, require_table=True):
    """Lint deliverable text (no sidecar/file checks). Returns LintResult.

    require_table=True: a missing team table is a HARD FAIL (Full-tier build).
    require_table=False: no table -> run hygiene/Tera only (e.g. Basic review docs).
    """
    data = data or Data()
    res = LintResult()
    rows, err = parse_team_table(text)
    if err:
        if require_table:
            res.hard.append("table parse: %s" % err)
        # hygiene/Tera apply to every client doc regardless of a team table
        _hygiene(text, res)
        return res

    team_stems = set()
    for r in rows:
        name = r["pokemon"]
        stem = data.resolve(name)
        if not stem:
            res.hard.append("unresolvable species: '%s' (no data/mons file)" % name)
            continue
        team_stems.add(stem)
        sc = collapse(name)

        if data.is_banned(name, stem):
            res.hard.append("banned mon: '%s'" % name)

        legal = data.legal_move_set(stem)
        for mv in r["moves"]:
            cm = collapse(mv)
            if cm in legal:
                continue
            if (sc, cm) in data.move_gaps or (collapse(stem), cm) in data.move_gaps:
                continue
            res.hard.append("illegal move: '%s' not in legalMoves of %s" % (mv, name))

        if r["ability"]:
            abils = data.ability_set(stem)
            ca = collapse(r["ability"])
            if ca and ca not in abils \
                    and (sc, ca) not in data.ability_exceptions \
                    and (collapse(stem), ca) not in data.ability_exceptions:
                res.hard.append("illegal ability: '%s' not valid for %s" % (r["ability"], name))

        item = r["item"]
        if item:
            ci = collapse(item)
            if ci in data.item_locks:
                allowed = {collapse(s) for s in data.item_locks[ci]}
                if collapse(stem) not in allowed:
                    res.hard.append("item lock: '%s' is species-locked, illegal on %s" % (item, name))
            elif ci.endswith("ite") and ci not in NON_MEGA_ITES:
                # mega-stone-shaped item we don't have a lock entry for -> surface, don't block
                res.warn.append("item '%s' on %s looks like a mega stone but is not in item_locks.json (verify)"
                                % (item, name))

    _hygiene(text, res)
    _phantom(text, team_stems, data, res)
    return res


# "-ite" items that are NOT mega stones (don't WARN on these).
NON_MEGA_ITES = {collapse(x) for x in ["Eviolite", "Gabite", "Dragonite", "Bug Bite"]}


def lint_file(path, require_verify=True, data=None):
    """Lint a teams/<name>.md file (team table required). Returns LintResult."""
    data = data or Data()
    text = open(path, encoding="utf-8").read()
    res = lint_text(text, data=data, require_table=True)
    if require_verify:
        check_sidecar(path, res)
    return res


def lint_for_export(path, data=None):
    """Gate used by the converter/hook. If the doc has a team table, run the full
    lint + hash-bound sidecar (Full-tier build). If it has no table (e.g. a Basic
    review doc), run hygiene/Tera only and do not require a sidecar."""
    data = data or Data()
    text = open(path, encoding="utf-8").read()
    _, err = parse_team_table(text)
    has_table = err is None
    res = lint_text(text, data=data, require_table=has_table)
    if has_table:
        check_sidecar(path, res)
    return res


def _log_denial(path, res):
    try:
        with open(DENIAL_LOG, "a", encoding="utf-8") as f:
            f.write("DENIED export of %s\n%s\n\n" % (path, res.report()))
    except Exception:
        pass


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    require_verify = "--no-require-verify" not in argv
    if not args:
        print("usage: lint_team.py <teams/file.md> [--no-require-verify]")
        return 2
    path = args[0]
    if not os.path.exists(path):
        print("lint_team: file not found: %s" % path)
        return 2
    res = lint_file(path, require_verify=require_verify)
    print(res.report())
    if not res.ok:
        _log_denial(path, res)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
