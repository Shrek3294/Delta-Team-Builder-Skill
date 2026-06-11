# Plan Review Log: Hard-gated factual verification for team-build deliverables
Act 1 (grill) complete — plan locked with the user. MAX_ROUNDS=5.

## Round 1 — Codex
THREAD_ID=019ea4b2-c045-75f0-b666-546d49354485 · VERDICT: REVISE

Material issues found:
1. Bypassable choke point: hook only matches `md_to_docx_pdf.py`; other exporters/direct Python/Node/PS calls evade it. Fix: run linter *inside* the converter; deprecate alternate exporters.
2. PreToolUse TOCTOU: a compound command can lint, then modify, then export the modified file in one call. Fix: lint inside the converter immediately before conversion.
3. Species normalization under-specified: files mix `mega-flygon.json` and `gengar-mega.json`; banlist uses `Mega Gengar`/`Raichu-Mega-Y`. Fix: build an alias map, not lowercase-hyphen rules.
4. Ban-by-grep false-fails legal notes ("X is legal") and false-misses form aliases. Fix: parse active banned bullets into canonical ids, exact-match.
5. Ability legality omitted though the table has an Ability column and wrong custom abilities are in the failure class. Fix: validate abilities vs species/form abilities + exceptions.
6. "Any Tera line anywhere" can catch `Terapagos-ATOM`/prose. Fix: anchor to set syntax `^\s*Tera\s*(Type)?:`.
7. Item legality lacks a clean schema in team-builder.json (Z items embedded in raw text, Megas not enumerated). Fix: generated/checked `item_locks.json` + unknown-item warnings.
8. Move parsing only covers the top table; misses Basic-tier fenced sets, replacement sets, quoted calc moves. Fix: scope explicitly or also parse those blocks.
9. Phantom-mon grep over all species is noisy (Kingambit appears legitimately in matchup prose). Fix: limit to tracked prior-slot names or classify by section.
10. settings.json merge behavior unspecified. Fix: define exact hook JSON, preserve existing keys.
11. Observability thin: no tests/fixtures/denial logging. Fix: pytest fixtures + denial log.

### Claude's response
Accepting all 11, with two deliberate downgrades (arbiter calls):
- **#1 + #2 (ACCEPT, architectural change):** Move the linter INTO `md_to_docx_pdf.py` as a fail-closed gate at the top of the script (lint the SRC it is about to convert, abort on failure). This is strictly better than hook-only and closes the TOCTOU window. Keep the PreToolUse hook as a *secondary* defense layer, not the primary gate.
- **#3 (ACCEPT):** Alias map built from filename stems + species displayName + banlist canonical forms; elevated from "risk" to core approach. Must be tested against the real `data/mons/` filename list.
- **#4 (ACCEPT):** Ban check parses the active banned-bullet lines of `notes/banlist.md` into canonical ids and exact-matches resolved species/form ids; never substring-greps the whole file.
- **#5 (ACCEPT):** Add ability-column legality check vs `species.abilities` + form abilities + a documented-exception allowlist (e.g. Mega pre/post ability like Slaughtermaus Vorpal→Reap).
- **#6 (ACCEPT):** Tera check anchored to `^\s*Tera\s?(Type)?\s*:` only; explicitly must not match `Terapagos`.
- **#7 (ACCEPT, with downgrade):** Build a checked `data/item_locks.json` (Z-crystal + Mega-stone → species). Known-mismatch = HARD FAIL; unknown/unmapped item = WARN (avoid false-blocking on incomplete mapping).
- **#8 (ACCEPT, scoped):** HARD legal-move/ability/item checks apply to the 6-row team table only (the shipped sets). Replacement-option sets get best-effort WARN-level legal checks if parseable. Basic tier produces no docx, so the hook never fires there — out of scope by construction.
- **#9 (ACCEPT, downgrade to WARN):** Phantom-mon residue is WARN-only, never a hard block, and section-aware (only considered in identity/role/wincon sections). Prefer tracked prior-slot names when available.
- **#10 (ACCEPT):** Specify exact hook JSON; writer merges into existing settings.json rather than overwriting.
- **#11 (ACCEPT):** Add `tools/tests/` pytest fixtures (one passing team, several poisoned teams covering each check, alias edge cases, ban aliases, data-gap allowlist) and append hook/converter denials to `teams/.lint-denials.log`.

## Round 2 — Codex
VERDICT: REVISE

Findings:
1. Plan still overclaims converter-internal lint "cannot be bypassed"; existing one-off exporters remain bypasses. Fix: single canonical export wrapper, forbid alternates, hook denies docx/pdf commands outside the wrapper.
2. "Deprecate/avoid alternate exporter" is advisory, not enforcement. Fix: archive old exporters or make them call the linted wrapper.
3. Data-gap allowlist parsed from mod_days.md prose is fragile. Fix: structured `data/lint_allowlists.json` with `{species, move, reason}`.
4. Mega ability legality underspecified: Pokepaste/table convention is pre-Mega ability, so validating against resolved Mega form false-fails. Fix: define table convention, validate Mega holders against base-form pre-Mega abilities + documented post-Mega checks.
5. Ban parsing from `reference/season meta changes.txt` is vague (not structured). Fix: treat `notes/banlist.md` as the canonical machine-readable ban source.
6. Verifier sub-agent has no auditable completion marker. Fix: require a Verifier findings/resolutions block before export; linter warns/fails if missing for Full tier.

### Claude's response
VERIFIED Codex's bypass claim: `ls teams/*.py teams/*.js` returns ~30 one-off exporters (build_*.js, build_*.py). Real bypasses. Also confirmed `season meta changes.txt` is unstructured prose. Accepting all 6:
- **#1 + #2 (ACCEPT, non-destructive enforcement):** `/build` must call ONLY `tools/md_to_docx_pdf.py` (stated in build.md). The PreToolUse hook denies any Bash command that runs node/python against a `teams/build_*`/`teams/_build*` script or otherwise produces a docx/pdf outside the canonical wrapper, directing to the wrapper. The legacy one-off scripts are the user's historical build records — NOT deleted or moved (hard rule: don't destroy files I didn't create); they are simply frozen and blocked from producing NEW exports by the hook. Enforcement without destruction. Drop the "cannot be bypassed" overclaim wording.
- **#3 (ACCEPT):** Allowlist moves to structured `data/lint_allowlists.json` (`{species, move, reason}` + ability/item gap entries); linter reads JSON, not mod_days prose.
- **#4 (ACCEPT):** Convention defined: team table + Pokepaste name the holder but list the PRE-Mega ability (per deliverable-spec / Slaughtermaus Vorpal precedent). Linter validates the ability against the BASE-form abilities; post-Mega abilities live on the documented-exception allowlist. Mega-named holders resolve to base-form ability set for the check.
- **#5 (ACCEPT):** `notes/banlist.md` is the SOLE machine-parsed ban source. `season meta changes.txt` is human reference only, never parsed by the linter.
- **#6 (ACCEPT, refined):** The mandatory verifier writes findings+resolutions to a sidecar `teams/<name>.verify.md` (kept OUT of the client docx — internal only). The converter/linter HARD FAILs a Full-tier export if the sidecar is missing or empty. This is the auditable completion marker for the mandatory sub-agent step.

## Round 3 — Codex
VERDICT: REVISE (prior findings confirmed addressed; 4 narrower issues)

Findings:
1. Sidecar check (exists + non-empty) allows a STALE sidecar from an older draft to satisfy the gate. Fix: sidecar embeds SRC hash/mtime; lint_team.py verifies it matches the exact SRC being exported.
2. Tests don't cover verifier sidecar despite it being a hard gate. Fix: fixtures for missing / empty / stale-hash / matching-hash sidecar.
3. Key Decisions still says converter-internal lint "makes the gate unbypassable by alternate exporters" — only true because of the hook. Fix: converter lint closes TOCTOU for the canonical path; the hook blocks alternates.
4. "Otherwise produces a docx/pdf outside the canonical wrapper" is too vague (evadable via `python -c`, `node -e`, copied paths, renamed scripts). Fix: hook blocks any command containing a `.docx`/`.pdf` output path unless it invokes `tools/md_to_docx_pdf.py`.

### Claude's response
All 4 ACCEPTED (clean, narrow tightening):
- **#1:** Sidecar must contain a `source-sha256:` header = SHA-256 of the SRC `.md`. The linter recomputes the hash of the file being exported and HARD FAILs if absent or mismatched. Stale sidecars no longer pass.
- **#2:** Add fixtures: missing sidecar, empty sidecar, stale-hash sidecar (hash of a different file), matching-hash sidecar (passes).
- **#3:** Reworded the Key Decisions bullet: converter-internal lint closes the TOCTOU window on the canonical path; the PreToolUse hook is what blocks alternate exporters. No more "unbypassable by alternate exporters" overclaim on the converter.
- **#4:** Hook deny rule made concrete: deny any Bash command whose text contains a `.docx` or `.pdf` output target UNLESS the command invokes `tools/md_to_docx_pdf.py`. This catches `python -c`, `node -e`, renamed scripts, and copied output paths.

## Round 4 — Codex
VERDICT: APPROVED

All Round 3 blockers confirmed addressed (hash-bound sidecar, sidecar test fixtures, converter-vs-hook guarantees separated, concrete non-canonical export deny rule). No new material flaws. Residual items are implementation details, not plan defects:
- The hook's command-text matching must be tested to avoid both bypasses and false blocks.
- The alias / base-form mapping needs real fixture coverage.

Converged after 4 rounds. Plan locked pending human sign-off.
