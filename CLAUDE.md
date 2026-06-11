# Cobblemon Delta Ranked Team Building Workspace

This is a paid team-building service for Cobblemon Delta ranked. The user is
consistently Top 100 (Top 20 in the new season) and the creator of Delta-Calc
on Modrinth. Clients pay in-game currency in Mesa.

**Tiers (updated 2026-05-16):** 60k Basic Team Guide · 300k Full Team Guide. The middle "build without doc" tier was retired.

## Where to look

### Read first — `notes/`
The rulebook. Skim before any build.

- `team_building_principles.md` — hard principles (win conditions, glue, speed control, doc structure)
- `team_archetypes.md` — archetype cores and example pieces
- `meta_overview.md` — current meta, custom-threat takeaways, viability summary
- `tierlist.md` — practical ladder tier list
- `player_notes.md` — tone, pricing, past client orders, lessons
- `balance_history.md` — patch history
- `mod_days.md` — per-mon notes with confirmed sets. **Authoritative when it contradicts the generated data.**
- `discord-sentiment.md` — synthesized scouting from the `#🥇｜competitive` Discord channel. **Signal, not fact.** Refresh with `/sync-sentiment`. Use for "where the meta is leaning" awareness; never override `mod_days.md` or usage data with a Discord opinion.
- `opponent-meta.md` — synthesized from **real opponent teams the user faced on ranked**, captured by the personal DeltaCalc fork into the DeltaCalc data folder. Refresh with `/sync-opponents`. Highest-recency signal we have — fresher than the May 6 usage scrape, more concrete than Discord sentiment. Check the sample-size note at the top before quoting numbers. **Opponent handles are anonymized (Opponent_A, etc.) in this file.**

### Data — `data/` (May 6, 2026 snapshot)
- `data/mons/<species>.json` — per-mon canonical lookup. Has `species` (types, base stats, abilities), `legalMoves`, and `_curated` (usage-weighted abilities/items/moves/spreads — **often empty**; fall back to `data/usage/`). Filenames are lowercase-hyphenated: `ogerpon-wellspring.json`, `tinkaton-gamma.json`, `terapagos-atom.json`.
- `data/delta-movesets.generated.json` — curated movesets across mons.
- `data/delta-auto-sets.generated.json` — auto-generated sets (lower trust than curated).
- `data/learnsets.generated.json` — full learnsets (43 MB; grep, don't load whole).
- **`data/team-builder.json`** — **the Discord forum scrape**, source-of-truth for custom mon mechanics. One entry per mon (316 total) pulled from the Cobblemon Delta Discord forum channel. Each entry has parsed `signatureAbilities`, `signatureMoves`, `forms` (with stats/abilities per form, including Megas and ATOM Cosmic/Galactic forms), plus a **`rawContent`** field with the full raw thread text — the parsed fields are often incomplete, so always check `rawContent` too. This is where to find: custom ability descriptions (Parasol Prayer text, Cosmo Shift, Desert Spirit), custom move descriptions with BP/PP/accuracy, custom Z-moves (Astral Burst, Universe Expansion), mega-evolution stat boosts and abilities, obtain methods, form mechanics.
- `data/usage/` — **ranked ladder usage scrape** (from `ranked.cobblemondelta.com`). Per-mon real-world usage % for moves/items/abilities/spreads. Source-of-truth for custom-only abilities like `parasolprayer` and items like `tangledtimium-z` when the per-mon `_curated` block is empty. Files:
  - `season-6-mid-1500.generated.json` — high-ELO (most relevant for ranked builds)
  - `season-6-mid-1300.generated.json` — mid-ELO
  - `season-6-mid-1000.generated.json` — low-ELO (use to detect "low-ladder cheese" sets that won't translate up)
  - `battle-database.generated.json` — aggregate of all three plus Smogon fallback

### Reference — `reference/`
- `Viability Rankings March3 (including Banned list).pdf` — official viability + bans.
- `season meta changes.txt` — patch tier movements + new bans.

### Past work — `teams/`
Delivered builds. Use for **doc structure and tone**, not as a set source — meta and prices shift.

### Don't edit — `archive/`
Original handoff zip + JSON backup.

## Hard rules

1. **Tera Type is banned in ranked.** Never recommend a Tera type, never include a Tera line in a Pokepaste or battle doc, ignore `tera_type` fields in data.
2. **Banned mons.** Recent bans include Mega Raichu-Y, Mega Delphox, and **Mega Gengar** (banned ~2026-05-05, multi-author Discord confirmation). Check `reference/season meta changes.txt` and the viability PDF before recommending any flagged S/A+ mon. Note: Iron Sentinel is **legal in ranked** despite a budget-tournament ban (don't conflate the two).
3. **Custom mechanics ≠ vanilla.** Confirm against `notes/mod_days.md` before quoting numbers. Common gotchas:
   - **Upgrade** = Booster Energy replacement. Boosts Tangled Time's ability, not the signature move. May display "heightened" without a +1 stage.
   - **Parasol Prayer** (Tinkaton-Gamma) sets Delta Stream and overwrites weather.
   - **Terapagos-ATOM** Z-moves (Astral Burst vs Universe Expansion) change form and ability — always specify which Z-crystal the client has.
   - **Draculedge** Conviction = +25% on super-effective; Twin Cross hits twice.
   - **Ivy Cudgel** should be Water-type on Ogerpon-Wellspring.
4. **Legal moves only.** Before writing a set, verify each move appears in `legalMoves` inside `data/mons/<species>.json`. If `_curated` lists a move missing from `legalMoves`, flag it — don't quietly drop or include it.
5. **No phantom mons in docs.** When a slot is replaced, scrub every reference to the old mon (e.g. no Kingambit/Sucker Punch/Supreme Overlord language in an Archapult + Tinkaton-Gamma doc).
6. **Verify type effectiveness before locking any offensive move.** Use [`data/type-chart.json`](data/type-chart.json). For each attacking slot on the team, compute the multiplier against every defender in `commonSwitchIns` (Tinkaton-Gamma, Corviknight, Gliscor, Alomomola, Ferrothorn, Heatran/-Delta, Garganacl, Tapukehe, Secret Armor, Mega Scizor, Delta Steelix — Skarmory and Clefgar are not run at high ladder, exclude them even if the JSON still lists them). Show your work in a coverage table — see `/build` step 4.5. **A move at 0.25× or worse into a common switch-in is a bug, not a feature.** Either swap it, justify it (setup/status/hazards aren't coverage), or note the gap in the matchup guide. Apply ability/weather modifiers from `type-chart.json` `modifiers` (Strong Winds, Levitate, Water Absorb, Flash Fire, Scrappy) before reading the multiplier as final.

## Data freshness

`data/` is a **May 6, 2026** snapshot. The meta moves fast. When `notes/` or `reference/` contradicts the JSON, **the notes win.** Use JSON for stats and learnsets; use notes for sets and viability calls. Refreshing means re-running `Z:\Cb delta\DeltaCalc\tools\database\` scripts — ask before doing it.

## Lookup chains

Two different questions need different sources. Walk the chain top-down and stop at the first hit.

### "What does X do?" (custom mechanics — abilities, moves, Z-moves, megas, forms)

1. **`notes/mod_days.md`** — hand-curated set notes and mechanic clarifications. Wins on contradictions.
2. **`data/team-builder.json`** — the Discord forum scrape. Find the entry by `name`, then read in order:
   - `signatureAbilities[]` and `signatureMoves[]` (parsed)
   - `forms[].abilities` and `forms[].stats` (per-form data)
   - **`rawContent`** — full raw Discord post. The parser misses things (e.g. Terapagos-ATOM's Z-moves and Cosmic/Galactic form abilities live only in `rawContent`). When the parsed fields are empty or thin, grep `rawContent` for keywords like `"Signature Z-Move"`, `"Z-Move"`, `"Mega"`, the form name, or the ability name.
3. **`data/mons/<species>.json`** — fallback for vanilla pokedex info (types, base stats, ability list).
4. **Ask the user.** Don't invent custom-mechanic behavior.

### "What's actually run on X at high ladder?" (usage)

1. **`notes/mod_days.md`** if the mon is documented there with a confirmed set.
2. **`data/mons/<species>.json`** `_curated` block (often empty — if so, skip).
3. **`data/usage/season-6-mid-1500.generated.json`** — high-ELO usage %. Drop to `-1300` or `-1000` if missing.
4. **`data/usage/battle-database.generated.json`** — aggregate + Smogon fallback for vanilla mons.
5. **Ask the user.**

### Legal-move validation (separate concern, non-negotiable)

`data/mons/<species>.json` → `legalMoves[]`. Every move on a Pokepaste must appear here. The team-builder scrape and usage data may *suggest* a move; only `legalMoves` *confirms* it.

### Naming gotchas

- Team-builder names use display form: `"Tinkaton-Gamma"`, `"Mega Flygon"`, `"Terapagos-ATOM"`.
- Usage scrape names normalize weird: `"Parasolprayer"` (no space), `"tangledtimium-z"` (hyphenated lowercase). Match on `id`/`slug`, not display name.
- Per-mon JSON filenames are lowercase-hyphenated: `tinkaton-gamma.json`, `mega-flygon.json`.

## Damage calc

The workspace has a damage calculator at [`tools/calc.py`](tools/calc.py). It's a faithful port of the in-game DeltaCalc mod's Kotlin damage engine (`Z:\Cb delta\DeltaCalc\src\main\kotlin\com\cobblemonextendedbattleui\calc\DamageEngine.kt`) — same floor/int truncation, same modifier ordering, same custom-ability handling (Parasol Prayer, Conviction, Reap, Draconic, etc.).

### Invocation

```
python tools/calc.py \
  --attacker "Archapult" --attacker-ability "Infiltrator" --attacker-item "Life Orb" \
  --attacker-nature "Jolly" --attacker-evs "0/252/0/0/4/252" \
  --level 100 \
  --move "Dragon Darts" \
  --defender "Tinkaton-Gamma" --defender-ability "Parasol Prayer" --defender-item "Heavy-Duty Boots" \
  --defender-nature "Calm" --defender-evs "252/0/4/0/252/0" \
  --conditions "rain,attacker-screens-off"
```

EV/IV format is `hp/atk/def/spa/spd/spe`. IVs default to 31 across the board.

### Supported conditions (comma-separated)

`rain`, `sun`, `sand`, `snow`, `electric-terrain`, `psychic-terrain`, `grassy-terrain`, `misty-terrain`, `light-screen`, `reflect`, `aurora-veil`, `strong-winds` (auto-applied when defender's ability is Parasol Prayer or Delta Stream), `attacker-+N` / `defender-+N` for stat stages on the active attacking/defending stat, `attacker-burn`, `attacker-low-hp`, `defender-low-hp`.

### Output

One block to stdout, e.g.

```
Archapult (Jolly, Life Orb) Dragon Darts vs Tinkaton-Gamma (Calm, Heavy-Duty Boots) in strong winds
Hits:        2 (multi-hit, fixed)
Damage:      164-194 (49.7% - 58.8%)
Effectiveness: 1x
Result:      2HKO
Confidence:  HIGH
Warnings:    Multi-hit (2 hits)
```

`Confidence` is HIGH when vanilla mechanics are confidently modeled; LOW when an unknown ability/item slipped through. Self-test cases live under `python tools/calc.py --self-test`.

### Known limitations — what the calc does NOT model

The calc is faithful to `DamageEngine.kt`, which means it inherits the engine's known gaps. Compensate manually with explicit `--attacker-+N` / `--defender-+N` boosts and read the result with these caveats in mind.

**Abilities that pass through as 1× (need manual simulation):**
- **Protosynthesis** (sun or Booster Energy) and **Quark Drive** (electric terrain or Upgrade/Booster) — they boost the holder's highest non-HP stat by 1.3× (1.5× if it's Speed). Simulate with `--attacker-+1` or `--defender-+1` on the relevant stat. Affects Tangled Time (SpA), Iron Sentinel (SpA), Iron Coil (SpA), Secret Armor (Atk), Iron Valiant, Iron Treads.
- **Cosmo Shift / Accretion Shell / Zodiac Orbit** (Terapagos-ATOM) — the form change isn't auto-applied. Look up the target form's stats from `data/team-builder.json` `rawContent` (Cosmic = 100/105/100/115/100/80, Galactic = 150/100/115/140/115/80) and pass them as if they were base stats by using the appropriate form's species file if it exists, or note the limitation in the deliverable.
- **Sound-boost / state-conditional abilities** specific to one mon (e.g. Desert Spirit on Mega Flygon: +1.3× to sound moves and in sand) — verify the Kotlin source before relying on the calc; rare ones aren't ported.

**Recovery / status abilities with no calc impact** (correctly ignored, but mention in the doc if they swing the matchup):
- Regenerator, Poison Heal, Magic Guard, Natural Cure — no damage modification but they affect KO math by restoring HP between turns. The calc reports raw damage; the doc should note "after Poison Heal recovery" or "after Regen pivot" if relevant.

**Items not in the table** — only common competitive items, plates, gems, and Ogerpon masks are modeled. Niche type-up consumables (e.g. resist berries, Soul Dew, Adamant/Lustrous Orb) may not apply. If the calc says `Confidence: LOW` with an item warning, treat the number as a ballpark.

**MoveFlagDatabase is hand-curated (~40 entries).** Move-tag-based ability boosts (Tough Claws, Strong Jaw, Sheer Force, Iron Fist, Pixilate, Aerilate, etc.) may miss on rare/custom moves not in the flag table. This is **under-boost**, not over-boost — the calc will read low, not high. Cross-check signature-move flags from `data/team-builder.json` if a custom-move calc looks suspicious.

**Knock Off mega-stone heuristic** identifies mega stones by `"ite"`-suffix on the item name, which can false-positive on non-mega items with that suffix (mostly hypothetical, but flag if you see weirdness on Knock Off damage).

**Flash Fire** correctly grants Fire immunity but does NOT boost the holder's subsequent Fire moves (Kotlin doesn't either). If a Heatran absorbed a Fire move and is now clicking Magma Storm, the calc reports the unboosted number.

**Divergences from the in-game DeltaCalc mod (Python is "more correct" than what players see):**
- **Strong Winds** (Parasol Prayer / Delta Stream → Ice/Rock/Electric vs Flying = 1×): implemented in Python, **not in the mod's Kotlin engine yet**. If a player references the in-game number for these matchups, expect a 2× disagreement.
- **Infiltrator screen bypass**: implemented in Python, not in the mod. Same disagreement risk on screened matchups.

When the calc result will mismatch what players see in-game for one of these reasons, **say so in the doc** — don't quietly hand them a number that contradicts their calculator panel.

## Tone

Short, confident, not overly formal. Example:

> Main issue is the team is way too physical-heavy. Barraskewda, Urshifu, Ogerpon, and Mega Swampert all pressure the same way, so good players can pivot around it with Skarm/Corv/Alomomola, Helmet, burns, etc. I'd either add a real special rain breaker or a stronger glue slot.

## Client workflow

1. Ask: required mon, playstyle, budget. If budget matters, ask their box.
2. Build around role compression first, favorite mon second.
3. Confirm any unclear custom-mechanic assumption before locking sets.
4. Deliver:
   - Pokepaste (no Tera line).
   - For the 200k tier, a battle doc with these sections:
     - Team identity
     - Each role (one paragraph per mon)
     - Standard leads + when NOT to lead the default
     - Early / mid / endgame plan
     - Win conditions
     - What to preserve
     - Common matchup guide
     - Replacement options
     - Known weaknesses

## Deliverable quality gate (factual lint)

Deliverable docx/pdf are produced **only** via `python tools/md_to_docx_pdf.py <draft.md> <out.docx> <out.pdf>`. That converter runs [`tools/lint_team.py`](tools/lint_team.py) fail-closed before converting, and a `PreToolUse` hook (`.claude/settings.json` → `tools/export_gate_hook.py`) blocks any other docx/pdf-producing command (legacy `teams/build_*` scripts, `python -c`, etc.). The linter hard-blocks on: illegal move (vs `legalMoves`), illegal ability, banned mon (`notes/banlist.md`), species-locked item mismatch (`data/item_locks.json`), Tera line, hygiene violations (dashes / customer language / internal refs), unresolvable species, and a missing/empty/stale verifier sidecar. Confirmed data gaps go in `data/lint_allowlists.json` with a reason, not silently ignored.

Every Full-tier build writes a hash-bound sidecar `teams/<name>.verify.md` (independent verifier sub-agent findings + resolutions, internal only) — see `build.md` §7.6. Editing the draft after verifying invalidates the hash and re-blocks export until you re-verify. Tests: `python -m pytest tools/tests/`.

## Pokepaste format

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
