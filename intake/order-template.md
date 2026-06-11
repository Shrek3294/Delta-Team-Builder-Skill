# Ranked team-building order intake template

Paste the block below to any client who orders. They fill it in the DM and reply. Designed to fit on one phone screen.

---

## Copy-paste block (send to client)

```
RANKED TEAM ORDER — fill in as much as you can, I'll DM you for anything missing.

1. Tier: [60k Basic Team Guide / 300k Full Team Guide]
2. Required mons (must include): [e.g. "Archapult, Tinkaton-Gamma" or "none"]
3. Playstyle: [Balance / Rain / Hyper Offense / Trick Room / Screens / Web / Stall / Surprise me]
4. Budget: [e.g. "10m per mon" / "50m total" / "no budget"]
5. Mons / types I want to AVOID: [e.g. "no Steel spam, no Kingambit" or "none"]
6. Owned high-value assets: [Z-crystals, ranked rewards like Draculedge/Sevigarde, hidden abilities, IV'd mons — list anything I should plan around]
7. Current ladder rating (approx): [for context — top 20 / top 100 / climbing / casual]
8. Anything else? [favorite mon, specific theme, "I always lose to X," etc.]

(If budget is tight, paste a screenshot of your PC after this so I can see what you have.)
```

---

## Why these fields

| # | Field | Maps to `/build` step | Why required |
|---|---|---|---|
| 1 | Tier | Step 1 (tier extraction) | Drives deliverable depth |
| 2 | Required mons | Step 1 (required mons) | Anchors the build |
| 3 | Playstyle | Step 1 (playstyle/archetype) | Drives core selection |
| 4 | Budget | Step 1 (budget) + Step 2 (must-have) | Determines what's reachable |
| 5 | Avoid | Step 1 (avoid/banned by customer) | Prevents wasted iteration |
| 6 | Owned assets | Step 1 (custom assets) | Z-crystal call for Terapagos-ATOM, prevents recommending a 9m Draculedge if they already own one |
| 7 | Ladder context | NEW — not in `/build` yet | Top 20 build is different from top 100 build; lets you tune for the actual field |
| 8 | Open text | Step 2 (anything custom-mechanic-dependent) | Catches what the schema misses |

## What you do with a filled-in reply

1. Paste the whole reply (verbatim) as the argument to `/build` — the prompt's Step 1 (Parse the order) already knows how to extract these fields.
2. If fields 4 or 6 are vague and budget matters, ask for the PC screenshot in DM before proceeding.
3. Otherwise: `/build` continues through research → build → deliver as normal.

## Lazy-client fallback

If a client replies "just build me HO" or "use my favorite mon," counter-DM:
> "Need a few quick answers first — won't take a minute, helps me build you the right team rather than a generic one. [paste template]"

If they still won't fill it, push them to the 40k Review tier rather than 100k/200k. Lower expectations on both sides.

## When to upgrade to a Google Form

This text template works for ~80% of orders. Escalate to a form if:
- You're getting too many partial replies and the back-and-forth is wasting more time than the form would
- You want a permanent paper trail of orders (Sheets backing)
- You want to automate intake → workspace (form submission auto-creates a `teams/<customer>-intake.md`)

If you hit that threshold, ask me to build the Google Form version — same fields, conditional logic (only ask about Z-crystals if Terapagos-ATOM is in field 2, etc.), results-to-Sheets.
