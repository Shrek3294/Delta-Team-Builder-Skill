# Cobblemon Delta Ranked Team Building

AI-assisted team building workspace for [Cobblemon Delta](https://modrinth.com/mod/cobblemon-delta) ranked ladder. Built and maintained by a Top 100 ranked player and the creator of [Delta-Calc](https://modrinth.com/mod/delta-calc).

> **New here? Never used a coding tool before?**
> Read the [**Walkthrough — No Coding Experience Needed**](WALKTHROUGH.md) first.
> It covers Claude Code, Cursor, Codex, Qodo, and Gemini/Antigravity step by step.

## What this is

A complete knowledge base + Claude Code skill for building competitive Cobblemon Delta teams. It combines:

- **Meta notes** — tier list, archetypes, balance history, confirmed sets from ladder captures
- **Scraped data** — per-mon stats/learnsets/abilities, ranked usage data (May 2026 snapshot), Discord forum custom-mechanic descriptions
- **Damage calculator** — faithful Python port of the in-game DeltaCalc engine (`tools/calc.py`)
- **Build pipeline** — linting, docx/PDF export, and a Claude Code slash command (`/build`) that takes a client order end-to-end

The workspace is designed to run inside [Claude Code](https://modrinth.com/mod/delta-calc) using the instructions in `CLAUDE.md`.

## Structure

```
notes/          Meta notes, tier list, confirmed sets, opponent data
data/
  mons/         Per-mon JSON (stats, abilities, legalMoves, curated sets)
  usage/        Ranked ladder usage scrapes (1000/1300/1500 ELO tiers)
  team-builder.json   Discord forum scrape — custom ability/move descriptions
  learnsets.generated.json  Full learnsets (43 MB, tracked via Git LFS)
tools/
  calc.py            Damage calculator
  lint_team.py       Deliverable quality gate
  md_to_docx_pdf.py  Export pipeline
  export_gate_hook.py  Pre-tool hook (blocks legacy export paths)
reference/      Official viability PDF, patch notes
.claude/
  commands/     Slash commands: /build, /sync-sentiment, /sync-opponents
  settings.json Claude Code hooks config
CLAUDE.md       Full AI instructions — read this first
```

## Setup

1. Install [Claude Code](https://claude.ai/code) and open this folder as a project.
2. Install Python dependencies: `pip install python-docx pypdf2` (for the export tools).
3. For the damage calc: `python tools/calc.py --self-test` to verify it's working.
4. Git LFS is required for `data/learnsets.generated.json`: `git lfs install && git lfs pull`.

## Damage calculator

```bash
python tools/calc.py \
  --attacker "Archapult" --attacker-ability "Infiltrator" --attacker-item "Life Orb" \
  --attacker-nature "Jolly" --attacker-evs "0/252/0/0/4/252" \
  --level 100 \
  --move "Dragon Darts" \
  --defender "Tinkaton-Gamma" --defender-ability "Parasol Prayer" --defender-item "Heavy-Duty Boots" \
  --defender-nature "Calm" --defender-evs "252/0/4/0/252/0"
```

See `CLAUDE.md` for full invocation docs and known limitations.

## Data freshness

`data/` is a **May 6, 2026** snapshot. Usage stats at [ranked.cobblemondelta.com](https://ranked.cobblemondelta.com) are the live source. Re-running the database scripts in `tools/` regenerates the snapshots.

## Pricing tiers

This workspace was built to support a paid service:

- **60k** — Basic Team Guide (Pokepaste + brief notes)
- **300k** — Full Team Guide (Pokepaste + full battle doc)

Prices are in Mesa in-game currency on the Cobblemon Delta server.

---

[Delta-Calc on Modrinth](https://modrinth.com/mod/delta-calc)
