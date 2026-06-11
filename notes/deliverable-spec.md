# Deliverable spec

Single source of truth for what a client-facing build deliverable must look like. Referenced from `.claude/commands/build.md`. If you change any rule here, also update the corresponding memory entry so future sessions stay aligned.

## Pokepaste (every build)

- No Tera line. Tera is banned in ranked.
- Standard format:
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
- For Mega mons, list the pre-Mega ability (the one held before evolution) on the Pokepaste line. Explain the Mega ability swap in the doc, not the paste.

## Chat reply (every build)

- Always paste the full Pokepaste block in the chat reply, even when it's also in the .md file. Clients copy from chat.

## Battle doc (300k Full tier)

- Opens with a 6-row team summary table. Columns: **Pokemon, Item, Ability, Moves, Role.** The Moves column is required (not optional).
- No Pokepaste block inside the .docx. The client gets the paste separately via chat / .md file.
- No coverage check table. The §4.5 type grid is internal-only; never include it in the client doc.
- Footer links the Delta-Calc mod so players can run their own numbers: https://modrinth.com/mod/delta-calc
- Sections, in order:
  1. Team identity
  2. Each role (one paragraph per mon)
  3. Standard leads + when NOT to lead the default
  4. Early / mid / endgame plan
  5. Win conditions
  6. What to preserve
  7. Common matchup guide
  8. Replacement options
  9. Known weaknesses

## File outputs

- Every .docx ships with a matching .pdf in the same folder. Some buyers don't have Word.
- Drafts live in `teams/<short-customer-or-theme>.md`. Use a theme name when the customer is sensitive (`kyurem-ho-2026-05.md`).

## Tone and language

- Short, confident, not formal. See `notes/player_notes.md` for tone exemplars.
- **Banned punctuation in client-facing prose: em-dashes (—) and en-dashes (–).** Convert to commas, periods, or sentence breaks.
- **Banned phrasings** (customer-facing language that reveals this is a paid service):
  - "customer asked for", "as requested", "client's draft"
  - "your team", "you asked for", "you wanted"
  - Anything that addresses the reader in second person about the order itself
  - Read the doc as a standalone team report, not a fulfillment artifact.
- **Banned internal data refs** (reveal scrape internals):
  - "1500+ usage", "X% usage", "dominant spread"
  - "JSON gap", "_curated", "auto-gen"
  - "the scrape says", "in the data"
  - Talk about what the team does, not where the numbers came from.

## Audit before delivery

Run `grep` (or visual scan) of the final doc for the banned strings above. A single em-dash or "customer asked" slipping through is a shipped error.
