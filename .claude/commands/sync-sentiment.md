---
description: Re-scrape the Cobblemon Delta ranked Discord channel and refresh notes/discord-sentiment.md
---

# Sync Discord ranked sentiment

$ARGUMENTS

---

## Workflow

### 1. Scrape
Run the scraper to pull the last 24h of messages from `#🥇｜competitive`:

```
cd "Z:\Cb delta scraper"
HOURS_BACK=24 node scrape-ranked-channel.js
```

(Override the window with `HOURS_BACK=72` etc. for a longer pass — 24h is the default and matches the synthesis cadence.)

The scraper writes `Z:\Cb delta\Delta team building\data\discord-ranked\raw\<YYYY-MM-DD>.jsonl`. Bot messages and obvious noise (single emoji, "lol/lmao/gg" reactions) are dropped at write time.

### 2. Read the raw dump
Read the latest `data/discord-ranked/raw/<date>.jsonl`. It's chronological, one message per line. Skim the whole thing — most "signal" comes from threads of 3-15 messages on a single topic, not from individual statements.

### 3. Synthesize into `notes/discord-sentiment.md`

Overwrite the file (do not append — sentiment is point-in-time). Use this exact section structure:

- **Front-matter block** — source channel, time window, message count, latest raw dump path, and the **reliability note** ("signal not fact, weight against mod_days.md / usage data / viability PDF").
- **Hot right now** — mons or mechanics with sustained discussion (5+ messages from 2+ authors). One sub-section per topic. Include: typing/role context, sets discussed, walls/checks named, any direct damage cites the channel produced.
- **Active complaints / sentiment shifts** — recurring whines that signal something might get nerfed, or mons the channel reads as having fallen off. Cross-reference any contradictions with `notes/tierlist.md`.
- **Counter-meta tech** — specific anti-meta sets, item picks, ability picks people mention as solving a problem. These are the "I run X to deal with Y" gold.
- **Patch / dev notes overheard** — anything stated as a balance/dev fact (bans, mechanic clarifications, upcoming changes). Mark with low confidence unless the source is a known authority.
- **Substantive messages (quote bank)** — 5-10 actually-useful quotes with handle and message ID for traceability.
- **How to use this in `/build`** — three to five bullets reminding the model that this is signal not fact, and giving any topic-specific weighting calls (e.g. "if a future mon is on the horizon, mention as flex; don't build around it").

### 4. Filtering rules — what to drop

Don't include:
- VGC-only / off-format chatter (the channel sometimes drifts into showdown OU, ZA, doubles)
- Single-message hot takes with no follow-up
- Pure complaints with no actionable signal ("X is broken" alone is noise; "X is broken because Y always 2HKOs" is signal)
- Memes, gifs, off-topic reactions
- Single-author monologues unless the author is a known top-ladder voice or a dev

Do include:
- Anything echoed by 2+ authors
- Damage calcs the channel produces (cite verbatim with message ID)
- Specific set / item / ability recommendations attributed to a handle
- Mentioned-by-name future content (upcoming mons, balance hints)
- Tech the channel says works against the current top mons (Tinkaton-Gamma, Tangled Time, Draculedge, Secret Armor, Ogerpon-W, Mega Scizor, Archapult, Terapagos-ATOM, etc.)

### 4a. Ban / nerf claim — strict sourcing rule

**Ban / nerf / "removed" claims are the highest-risk failure mode** (the Iron Sentinel false-positive came from a 2-word "Its banned" reply that was actually about a budget tournament, not ranked).

For any claim of the form "X is banned," "X is nerfed," "X got removed," "X is no longer in ranked":

**Required for inclusion:**
- (a) **Authority confirmation** — the message is from Invin (the dev), a known mod, or quoted directly from a pinned message / official source. Quote the source verbatim with message ID.

**OR**

- (b) **Multi-message thread context** that explicitly names the format / scope. The thread must make clear *which* format the ban applies to (ranked singles vs ranked doubles vs budget tournament vs upcoming format vs Showdown drift). At least 3 messages from 2+ authors on the same scope.

**If neither (a) nor (b) holds:** drop the claim, OR include it only with explicit hedging — "channel chatter suggests X may be banned in [scope guessed], but unconfirmed; do not act on this until verified." Two-word confirmations like "Its banned" from non-authorities → drop unless thread context anchors the scope.

**Always disambiguate scope** when including ban claims:
- Ranked singles (the actual format the build service targets)
- Ranked doubles / VGC-style (irrelevant for builds)
- Tournament-specific (budget tourneys, themed tourneys — irrelevant for builds)
- Upcoming format (signal only, not fact)
- Showdown OU / non-Delta (drop)

If the scope is "tournament-only" or "upcoming format only," explicitly state "**X remains legal in ranked play**" so the synthesis can't be misread later.

### 5. Length target

Aim for ~150-300 lines of synthesis. Long enough to be useful, short enough to be re-read at the start of every `/build` without burning context. If a section is empty for the day, drop it rather than padding.

### 6. Don't touch the raw

The raw JSONL files in `data/discord-ranked/raw/` are the audit trail. Never edit them. Old files accumulate so we can compare windows over time; if the folder gets too big, manually prune the oldest (no auto-rotation yet).
