---
description: Take a customer order and build a ranked team end-to-end
---

# New team build

Customer order (verbatim from Discord or in-game):

$ARGUMENTS

---

## Workflow

Run the standard build process per [CLAUDE.md](../../CLAUDE.md).

### 1. Parse the order
List what you extracted:
- **Required mons** (the customer asked for these by name)
- **Playstyle / archetype** (rain, HO, balance, TR, screens, web, semi-stall) — or "unspecified"
- **Budget** — total or per-mon, or "no budget" / "unspecified"
- **Avoid / banned by customer** (mons they hate, types they want fewer of, "no Steel")
- **Custom assets they own** (Z-crystals, ranked rewards like Draculedge / Sevigarde, specific IV/BP'd mons)
- **Ladder context** (top 20 / top 100 / climbing / casual) — tune the build for the actual field they're playing
- **Tier**: 60k Basic Team Guide · 300k Full Team Guide. (The 100k middle tier was retired 2026-05-16; if a returning client references it, honor the old price they were quoted but flag the change.) If the customer didn't say, ask.

**If the order arrived in the structured intake-template format** (see `intake/order-template.md` — numbered fields 1–8), extract field-by-field rather than free-text parsing. Field numbers are stable: 1=tier, 2=required mons, 3=playstyle, 4=budget, 5=avoid, 6=owned assets, 7=ladder context, 8=open. If any required numbered field is left blank or "N/A," treat as a real gap in Step 2.

### 1.5 Ban-list gate
Before researching anything, grep [`notes/banlist.md`](notes/banlist.md) **and** [`reference/season meta changes.txt`](reference/season meta changes.txt) for every required mon, every customer-favorite mega, and every legendary referenced in the order. Anything banned → stop and tell the client before continuing. Do not silently substitute. Common recent hits: Mega Gengar, Mega Raichu-Y, Mega Delphox, all box legends, Kyurem fusions.

### 2. Ask for missing must-haves only
Don't ask filler. Real gaps:
- Budget if it matters and isn't stated
- Box contents if budget is tight
- Z-crystal owned for Terapagos-ATOM (Astral Burst vs Universe Expansion changes the build)
- Archetype preference if not implied by the requested mons
- Anything custom-mechanic-dependent the order leaves ambiguous

If nothing material is missing, say "no gaps, proceeding" and continue.

### 3. Research
For **each** named mon, walk both lookup chains from CLAUDE.md:

**Custom mechanics** (what the mon's abilities/moves/Z-moves/forms actually do):
1. Grep `notes/mod_days.md` for the mon — confirmed mechanic notes win.
2. Find the mon's entry by `name` in `data/team-builder.json`. Read parsed `signatureAbilities`, `signatureMoves`, and `forms[]`. If they're thin or empty, **grep `rawContent`** for keywords (`"Signature Z-Move"`, `"Mega"`, form names like `"Galactic"` / `"Cosmic"`, ability name). The raw Discord post text has the full descriptions even when the parser missed them.
3. `data/mons/<species>.json` for vanilla pokedex info.

**Real high-ladder usage** (what's actually being run):
1. `notes/mod_days.md` if it documents a confirmed set.
2. `_curated` in `data/mons/<species>.json` (often empty — skip).
3. `data/usage/season-6-mid-1500.generated.json` for usage % on moves/items/abilities/spreads. Drop to `-1300` or `-1000` if missing. Match on `id`/`slug` (names normalize weird: `"Parasolprayer"`, `"tangledtimium-z"`).

**Legality** (non-negotiable): Every move you write must appear in `data/mons/<species>.json` → `legalMoves[]`.

Also:
- Skim `reference/season meta changes.txt` for any recent tier shift or ban on the requested archetype.
- Check `notes/balance_history.md` if the customer references a recent patch.
- Skim `notes/discord-sentiment.md` for current meta scouting (where the chatter is leaning, what's hot/falling). **Treat as signal, not fact** — never override `notes/mod_days.md` or usage data with a Discord opinion. Useful for: future-mon awareness, counter-meta tech ideas, tonal cues, recent dev/balance hints.
- Skim `notes/opponent-meta.md` for **what's actually being run on ladder this week** (captured from the user's own ranked battles via the personal DeltaCalc fork). This is the most current signal available — fresher than the usage scrape (May 6 snapshot) and grounded in real games, not chat. Check the sample-size note at the top: small samples (<30 captures) are illustrative only; larger samples are statistically meaningful for the top 30 mons. When opponent-meta and Discord sentiment disagree, opponent-meta wins for "what's actually being played." Also grep the raw captures folder (path in opponent-meta.md header) directly for any specific mon the client named — concrete recent sets land here even when they don't make the synthesis cut. **Never include opponent handles in client-facing deliverables** — anonymize as `Opponent-A`, `Opponent-B`, etc. if quoting.

### 3.5 Reconcile sentiment with the static notes
After step 3, if `notes/discord-sentiment.md` claims a release, ban, nerf, or tier shift that **`notes/mod_days.md`, `notes/tierlist.md`, or `reference/season meta changes.txt` does not reflect**, surface the conflict to the user before continuing. Format: "Sentiment claims X (msg ID Y); static notes don't have it. Confirm before I treat as fact?"

This catches the Iron-Sentinel-style misread: when the synthesis pass infers a fact from short Discord chatter without strong sourcing, the user gets a chance to correct before the build is wrong. If the user confirms, ask whether they want it pushed into the static notes for next time.

### 4. Build the team
Apply principles from [`notes/team_building_principles.md`](notes/team_building_principles.md). Show your work explicitly:

**Open-ended orders: diversify past top-20 usage.** If the customer named 0 or 1 required mons and just asked for an archetype ("best HO team," "build me a balance team"), do NOT anchor every slot on the top-20 usage list — different customers playing each other on ladder will end up against near-identical builds. Scan `data/usage/season-6-mid-1500.generated.json` past rank 20 for viable A/A+ tier picks (cross-check `notes/tierlist.md`) and substitute at least one or two slots — rocks setter, hazard remover, secondary breaker, glue pivot are the natural variety slots. Don't trade away the wincon for novelty; the goal is variety across builds, not lower-tier cheese.


- **Win conditions** (name 1–3 realistic ones)
- **Speed control** (priority / TR / Scarf / Booster/Upgrade / Web / weather speed / TWave)
- **Defensive glue** — each defensive slot must do 2+ of: hazards, removal, Knock Off, pivoting, weather control, status, recovery, immunities, priority denial, setup denial, scouting
- **Lead plan + anti-lead backup**
- **Preserved immunities** (Dragon / Ground / Water — flag if you remove the only one)
- **Physical/special balance** (flag if rain stacks Barraskewda + Urshifu + Ogerpon + Swampert without a special breaker)

### 4.4 Lock in actual typing
Before running any coverage math, read `data/mons/<species>.json` `types` for **each of the 6 mons on the build** and **each defender** you're about to put in the coverage table. Write the types out literally in a short list. Do not work from memory — memory has been wrong here before:

- Tinkaton-Gamma is **Flying/Fairy**, not Steel/Fairy. Fighting is 0.25× resisted; Electric/Ice/Rock/Poison are 2×.
- Iron Sentinel is **Water/Flying**, not Steel. It is not a fairy break and is not a steel switch-in.
- Verify any mon whose form/Mega changes type (Mega Altaria, Mega Scizor, Terapagos forms, Heatran-Delta, etc.) using the actual JSON or `data/team-builder.json` form data.

This step is the input to §4.5. If you skip it, the coverage table operates on assumed typing and the conclusions are wrong.

### 4.5 Coverage check (CLAUDE.md rule 6)
Build a coverage table for every offensive move on the team using the types you just wrote down in 4.4. Load `data/type-chart.json`. Defenders = the `commonSwitchIns` list there, plus any switch-in the customer's expected matchups should worry about. **Skarmory and Clefgar are NOT run at high ladder — drop them from any coverage table even if `commonSwitchIns` still lists them.** Substitute from `data/usage/season-6-mid-1500.generated.json` defender ranks instead.

Format (one row per attacking move, columns = defenders — abbreviate names):

```
| Mon / Move (type)            | Tink-G  | Corv    | Glisc   | Alo     | Ferro   | Heat    | H-D     | Garg    | Tapu    |
|------------------------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| Archapult / Dragon Darts (D) | 0.5×    | 0.5×    | 1×      | 1×      | 0.5×    | 0.5×    | 0.5×    | 1×      | 0×      |
| Archapult / Iron Head (Stl)  | 2×      | 0.5×    | 1×      | 1×      | 0.5×    | 0.5×    | 0.5×    | 2×      | 2×      |
```

Apply `type-chart.json` `modifiers` before reading any cell as final:
- **Strong Winds** (Tinkaton-Gamma + Parasol Prayer up): Ice/Rock/Electric vs Flying-types → 1× instead of 2×.
- **Levitate / Air Balloon**: Ground → 0×.
- **Water Absorb / Flash Fire**: Water → 0× / Fire → 0× on that mon specifically.
- **Scrappy** (Mega Lopunny): Normal & Fighting hit Ghost-types at 1× before second-type math.

Any move at 0.25× or worse into a common switch-in is a flag — fix it, justify it (setup/status/hazards aren't coverage), or document the gap in the matchup section.

### 4.6 Damage check
Identify the 2-3 most important damage interactions that define the team's win conditions — the matchups that decide whether the team wins or loses against the meta. Examples: "does +2 Ogerpon-Wellspring Ivy Cudgel OHKO Skarmory after rocks", "does Tinkaton-Gamma Updraft 2HKO Mega Flygon", "does specs Archapult Draco Meteor 2HKO max-HP Corviknight".

For each, run `python tools/calc.py ...` (see [`CLAUDE.md`](../../CLAUDE.md) §Damage calc for invocation) and quote the output verbatim in the deliverable. The calc is a faithful port of the in-game DeltaCalc engine — its numbers are what the actual game produces.

Cap at 5 calcs per build. Focus on wincon-defining matchups. Don't run the calc against every defender from §4.5; the coverage table already covers raw type math. The damage check answers a different question: "given the numbers, does the wincon actually pull through?"

Before invoking, skim **[CLAUDE.md §Damage calc → Known limitations](../../CLAUDE.md)** so you compensate correctly:
- For Protosynthesis / Quark Drive / Booster / Upgrade mons (Tangled Time, Iron Sentinel, Iron Coil, Secret Armor, Iron Valiant), pass `--attacker-+1` or `--defender-+1` on the boosted stat — the calc doesn't auto-apply the booster boost.
- For Terapagos-ATOM, the calc doesn't auto-transform to Cosmic/Galactic — note the form math explicitly.
- For Strong Winds and Infiltrator + screens, the Python calc disagrees with the in-game mod calc (Python is correct, mod has a known gap). If the player will check the in-game number, flag the disagreement in the doc.
- Confidence: LOW with an item/ability warning means treat the number as a ballpark; don't quote it as gospel.

### 5. Pre-draft gate (fast)
A short hard-stop check before writing the doc. Each item is binary: pass or fix.
- Every move appears in `legalMoves` of that mon's JSON. If a curated move is missing from `legalMoves`, flag it — don't quietly include or drop.
- Ability matches a real option in `species.abilities` or `_curated.abilities`.
- Item is legal on the holder: Z-crystals (e.g. `deltatyphlosium-z`, `tangledtimium-z`) and Mega stones are species-locked. Check `data/team-builder.json` for the species the item belongs to.
- No Tera line on any set.

Everything else (coverage, hygiene, speed math, calc sanity, phantom mons) is audited in §7.5 after the draft is written. Don't double-check it here.

### 6. Deliver per tier

**60k Basic Team Guide** — terse list of the 2–4 biggest issues with the customer's existing team in the user's tone (short, confident, not formal), plus 1–3 concrete fixes (swap X for Y, change item, retune EVs). No full rebuild. If the client has no existing team and ordered this tier, push them to 300k or ask if they meant the Full tier — Basic is review-only.

**300k Full Team Guide** — Pokepaste + full battle doc. Follow [`notes/deliverable-spec.md`](notes/deliverable-spec.md) for the complete spec (sections, team table at top, no Pokepaste in docx, no coverage table, footer link, file outputs, banned phrasings and punctuation). That file is the single source of truth — if it conflicts with anything else, it wins.

### 7. Save the draft
Write the deliverable to `teams/<short-customer-or-theme>.md` so it's ready to paste into Word for the .docx export. If the customer name is sensitive, use the theme (e.g. `kyurem-ho-2026-05.md`).

### 7.5 Final error audit (run on every order)
Read the whole draft top-to-bottom one more time. Every category below is a class of error that has shipped on a real build before — these are the high-leverage things to catch. Apply fixes inline, then regenerate the .docx and .pdf if they were already built.

**Speed math.** Final Speed at lvl 100 with 31 IV and 252 EV is `(2*base + 99) * nature_mult` (1.1 positive, 1.0 neutral, 0.9 negative). At 0 EV: `(2*base + 36) * nature_mult`. Multiplicative Speed abilities (Surge Surfer, Chlorophyll, Swift Swim, Sand Rush, Slush Rush, Unburden) apply 2× to the FINAL stat, not the base. Choice Scarf is 1.5×. Booster Energy / Upgrade on Speed is 1.5×, on other stats is 1.3×.
- Recompute every Speed number quoted in the doc. Common miss is multiplying base × 2 instead of computing final stat × 2.
- For "X outspeeds Y" claims, compute both. Watch for speed ties at common 130-base lines (Tapu Koko, Mega Slaughtermaus, Dragapult-Ultra cluster).
- For "outspeeds Booster Iron Valiant" or "outspeeds Scarf X" claims, compute 1.5× of the opponent's max Spe.

**Mechanic attribution.** Common confusions to catch:
- Strong Winds is the weather; Delta Stream is the Rayquaza ability that sets it. Tinkaton-Gamma's Parasol Prayer sets Strong Winds, not Delta Stream.
- Updraft (Tinkaton-Gamma) swaps the target's ability to Levitate. The value is removing Intimidate / Flash Fire / Protosynthesis / Purifying Salt / Magic Bounce, not "Ground types stop fearing EQ" (most are already Ground-immune or don't care).
- Mega Slaughtermaus's ability is Reap (auto-crit on slicing moves), not Vorpal. Pokepaste lists pre-Mega ability (Vorpal); doc explains the Mega swap.
- Surge Surfer doubles Speed only under Electric Terrain.
- Weather and terrain coexist — neither overrides the other's mechanics. Rain + Electric Terrain is a valid simultaneous state.
- For any custom ability or signature move referenced in the doc, the description should match `data/team-builder.json` `rawContent` or `notes/mod_days.md`.

**Coverage and matchup correctness.** For every "X fears Y's Z move" or "Y handles X" claim:
- Multiply effectiveness against both defender types from `data/type-chart.json`. Common miss: Superpower vs Corviknight (Steel/Flying) = 2× × 0.5× = 1× neutral. Corv does NOT fear Superpower.
- Verify the proposed defender isn't 4× SE'd by the threat (common miss: "Gholdaton handles Mega Swampert" when EQ is 4× into Steel/Fairy).
- Re-check the §4.5 coverage table against the final Pokepaste. If moves changed during drafting, the table is stale.

**Doc hygiene (now machine-enforced).** The mechanical checks below are run automatically by [`tools/lint_team.py`](../../tools/lint_team.py) and **hard-block the export** at `tools/md_to_docx_pdf.py` (see §8). You no longer grep for them by hand, but you still have to *fix* whatever a blocked export reports:
- em-dash / en-dash, customer-facing language, internal data refs (the full `notes/deliverable-spec.md` banned lists)
- every team-table move present in `legalMoves` (or allowlisted in `data/lint_allowlists.json`)
- ability legality, banned mons, item locks, no Tera line, species resolve to a real `data/mons` file

What the linter does NOT fully catch, so still scan by hand:
- **Phantom-mon residue.** The linter only WARNs on non-team names in the identity section. When you swap a slot, scrub ability/move references too ("Sucker Punch," "Supreme Overlord," "Regenerator pivot") that imply a mon no longer on the team. The Kingambit lesson is real.
- **Coverage / speed / damage reasoning** (the judgment items above) — the linter checks legality, not whether a claim is true.

**Damage calc sanity.** For any calc output quoted:
- Re-verify the conditions string applied (the calc silently passes unknown conditions through). For +2 SD claims, sanity-check that the quoted damage is ~2× the unboosted damage.
- For Mega evolutions, the calc uses base-form stats and the pre-Mega ability unless you pass the Mega ability explicitly. Slaughtermaus-Mega, Mega Scizor, Mega Altaria, and Mega Diancie all have different Mega abilities — note the discrepancy in the doc when relevant.
- For Strong Winds / Infiltrator-through-screens claims, flag the disagreement between python calc and in-game mod calc.

Re-read the draft once more after applying fixes. A surrounding paragraph often needs a small rewrite when a single fact changes.

### 7.6 Independent verifier pass (mandatory, Full tier)
The §7.5 audit is you reviewing your own draft in the same context — it shares your prior and misses what you were confidently wrong about. So hand the draft to a **fresh sub-agent with a clean context** that cannot inherit that prior.

Spawn an `Explore` (or general) agent with this instruction, giving it only the draft path and the data dirs:

> You have no reliable vanilla Pokémon knowledge for this mod. Every Delta-specific factual claim in this deliverable (typing, ability behavior, move effect, speed tier, coverage multiplier, KO claim) must be verifiable against a cited file in `data/` or `notes/`, or it is a finding. Read only the deliverable plus the data files. Refute, don't rubber-stamp. List each unverifiable or contradicted claim with the file you checked.

Then write the agent's findings **and your resolution of each** to a sidecar `teams/<name>.verify.md`. This file is internal — it never goes in the client docx. It MUST start with a hash header binding it to the exact draft:

```
source-sha256: <sha256 of teams/<name>.md>

## Verifier findings & resolutions
- <finding> -> <fixed / dismissed because ...>
```

Generate the hash with `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "teams/<name>.md"`. If you edit the draft afterward, the hash no longer matches and the export will block until you re-run this step — that is intentional.

### 8. Export (single canonical path, hard-gated)
Produce the `.docx` and `.pdf` **only** via the one canonical exporter:

```
python tools/md_to_docx_pdf.py "teams/<name>.md" "teams/<name>.docx" "teams/<name>.pdf"
```

Do **not** use any `teams/build_*.py` / `build_*.js` script or hand-roll a docx/pdf another way — those are frozen historical builds and the PreToolUse hook will block them. The exporter runs [`tools/lint_team.py`](../../tools/lint_team.py) fail-closed before converting: if it reports a HARD FAIL (illegal move/ability/item, banned mon, Tera line, hygiene violation, unresolvable species, or a missing/stale verifier sidecar from §7.6), the export aborts and prints exactly what to fix. Fix it, or — only for a confirmed data gap — add the entry to `data/lint_allowlists.json` with a reason, then re-export.

## Format

Pokepaste — no Tera line:

```
Mon Name @ Item
Ability: Ability Name
Nature
EVs: HP / Atk / Def / SpA / SpD / Spe
- Move 1
- Move 2
- Move 3
- Move 4
```

## Past orders as reference
Read `notes/player_notes.md` "First/Second/Third Paid Order Notes" for tone and depth of the deliverable. `teams/` has the actual delivered docs.
