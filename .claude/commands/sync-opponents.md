---
description: Synthesize opponent-team captures from the in-game DeltaCalc fork into notes/opponent-meta.md
---

# Sync opponent-team captures

$ARGUMENTS

---

## Workflow

### 1. Read the source folder
Captures are written by the user's personal DeltaCalc fork during ranked battles. Path (Windows default):

```
%APPDATA%\ModrinthApp\profiles\Cobblemon Delta\config\deltacalc\opponent-teams\
```

Each file is one battle: `YYYY-MM-DD_HH-MM-SS__<opponent>.md`. Format:

- Front-matter: `date`, `opponent`, `player`, `battle_id`, `turns`, `opponent_mons_seen`
- Body: six per-mon blocks with species, item (if revealed), ability (if revealed), types, moves (with `?` for unrevealed slots), optional status

Read all `.md` files in the folder. Don't filter by date — fold everything into the synthesis. The folder is read-only from this command's perspective; the in-game calc owns writes.

### 2. Sample-size gate
Count total captures. Add a NOTE at the top of `notes/opponent-meta.md`:

- **< 30 captures:** "Sample size: N captures. Too small for statistical claims. Treat percentages as illustrative, not authoritative. Re-run after more battles."
- **30–100 captures:** "Sample size: N captures. Useful for archetype-prevalence reads; treat single-mon usage % with caution below the top 10."
- **100+:** "Sample size: N captures. Statistically meaningful for mon prevalence, archetype distribution, and confirmed sets in the top 30."

Still synthesize whatever you have; the warning calibrates trust.

### 3. Synthesize → `notes/opponent-meta.md`

Overwrite the file with this structure. Drop empty sections.

```
# Opponent meta — captured ladder data

> **Source:** in-game DeltaCalc captures, `<captures path>`
> **Captures:** N battles, date range <first> → <last>
> **Sample-size note:** <calibration sentence from §2>
> **Distinct opponents:** M
> **Reliability:** Real ladder matchups, partial info per mon (only what the mod saw revealed). Higher signal than the May 6 usage scrape because it's current; lower coverage because of sample size and partial reveals.

## Mon prevalence
[Table ranked by appearances. Cap at top 30; long tail in a footnote.]

| Mon | Teams | % | Common partners |
|---|---|---|---|

## Archetype distribution
[Cluster captured teams by archetype: Rain, Web HO, Balance, TR, Stall, Bulky Offense, etc. For each archetype: count, common members, lead patterns, notable variations.]

## Confirmed sets seen on ladder
[For each frequently-appearing mon, list the actual revealed moves/items/abilities aggregated across captures. Cross-check `notes/mod_days.md`:
- If the captured set matches `mod_days.md`: ✓ confirmed in the wild
- If it diverges (different item, different move slot, different ability): flag with "**Diverges from `mod_days.md`** — captured: X; documented: Y"]

## Recurring cores / pair frequencies
[Which mon pairs appear together repeatedly? E.g. "Drizzle Typhlosion-Delta + Mega Swampert in N rain teams." Helps identify which mons function as team templates.]

## New or unusual picks
[Anything off-meta worth flagging: new variants (Tinkaton-Omega, Heatran-Delta Pressurize), cheese sets, unexpected items, unusual ability calls. Especially flag mons NOT in `notes/mod_days.md` — these need an entry written.]

## Comparison to other signals
[Where opponent-meta disagrees with `notes/discord-sentiment.md` or `data/usage/season-6-mid-1500.generated.json`:
- "Channel says X is hot — appears in N/M captures (low/high vs hype)"
- "Usage scrape lists Y at rank R — captured at <prevalence>"
Real ladder games at our rating > channel chatter > 2-week-old aggregate stats.]

## Per-opponent scouting (optional, if useful)
[If the same opponent appears 3+ times with consistent picks, summarize their tendencies. Stable handles are useful for ladder rematches. Drop this section if all opponents are one-offs.]
```

### 4. Handle / privacy

Opponent handles must be anonymized in `notes/opponent-meta.md` using labels like `Opponent_A`, `Opponent_B`, etc. Stable patterns are still scouting-useful in this form. **Do not use real IGNs in `notes/opponent-meta.md` or any `teams/<client>.md` deliverable.** Describe team archetypes by label or archetype name only.

### 5. Length cap

~200 lines. The point is digestibility during `/build` step 3, not exhaustive logging. The raw captures are the audit trail.

### 6. Don't re-read after writing

The output file is fully overwritten each run. No append, no merge with prior synthesis — the raw captures are the durable record.
