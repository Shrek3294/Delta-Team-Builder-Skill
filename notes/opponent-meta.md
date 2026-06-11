# Opponent meta — captured ladder data

> **Source:** in-game DeltaCalc captures from the DeltaCalc data folder
> **Captures:** 36 battles, 2026-05-21 → 2026-05-24 (4-day window, 3 distinct laddering sessions).
> **Sample-size note:** **36 captures. Useful for archetype-prevalence reads; treat single-mon usage % with caution below the top 10.** Ranks 1-10 are real signal, ranks 10-20 are directional, anything 1-2 appearances is anecdote.
> **Distinct opponents:** 30. Repeats: Opponent_A (3, identical team), Opponent_B (4, two team-builds), Opponent_C (2, very different teams), Opponent_D (2, identical team), Opponent_E (3 — one sand team, two identical Koko-offense), others all one-off.
> **Reliability:** Real ladder matchups, partial info per mon (only what the mod saw revealed during the match). Higher signal than the 2-week-old usage scrape because it's current week; lower coverage because of partial reveals. ~216 total mon-slots seen.

## Mon prevalence

Top 30 of 90+ distinct species seen. % is "team appearance" out of 36. Common partners are the 1-2 species most often sharing the team.

| Mon | Teams | % | Common partners |
|---|---|---|---|
| Heatran (any) | 13 | 36% | Tinkaton-Gamma (8), Ironvaliant (7), Ogerpon-Wellspring (6) |
| Ironvaliant (Normal) | 11 | 31% | Tinkaton-Gamma (9), Heatran (7), Ogerpon-Wellspring (7) |
| Tinkaton-Gamma | 10 | 28% | Ironvaliant (9), Heatran (8), Ogerpon-Wellspring (7) |
| Ogerpon (any form) | 10 | 28% | Wellspring is 7/10; Tinkaton-Gamma (7), Ironvaliant (7) |
| Marshadow-Delta | 7 | 19% | Tinkaton-Gamma (5), Heatran-Delta (4), Ironvaliant (4) |
| Garchomp | 6 | 17% | Tapu Koko (2), Heatran (2) — usually Rough Skin |
| Corviknight | 6 | 17% | Heatran (3), Ferrothorn (2) — hazard-stack glue |
| Dragonite (any) | 6 | 17% | Ironvaliant (5), Heatran (5), Tinkaton-Gamma (4) — all on Opponent_B variants |
| Heatran-Delta (subset of above) | 5 | 14% | Tinkaton-Gamma (4), Ironvaliant (4), Marshadow-Delta (4) |
| Mawile | 5 | 14% | Ironvaliant (5), Tinkaton-Gamma (4) — Opponent_A template core |
| Gliscor | 5 | 14% | Heatran (3), Mawile (2) — Poison Heal where revealed |
| Tapu Koko | 5 | 14% | Gholdaton (3), Raging Bolt (1) |
| Ferrothorn | 3 | 8% | Heatran (2), Corviknight (2) — Iron Barbs Spikes |
| Ectarachnid | 3 | 8% | Sevygarde (2), Volcanion-Delta (2) |
| Gholdaton | 3 | 8% | Tapu Koko (3), Raging Bolt (1) — always Life Orb / Leftovers |
| Kartana | 3 | 8% | Ninetales (2 — Opponent_D's Aurora Veil HO) |
| Kingambit | 3 | 8% | Ironvaliant (1), Iron Moth (1) — Supreme Overlord where revealed |
| Scizor | 3 | 8% | Mixed; Bullet Punch + SD set when revealed |
| Swampert | 3 | 8% | Rain teams (2/3); Mega in at least one slot |
| Tornadus | 2 | 6% | One Defog (Opponent_G), one Nasty Plot (Opponent_H) |
| Tyranitar | 2 | 6% | Sand Stream once (Opponent_H); deltastream once (Opponent_E, see flags) |
| Hydrapple-Ultra | 2 | 6% | Corviknight (2) — bulky pivot role |
| Iron Moth | 2 | 6% | Kingambit (1), Tapu Lele (1) |
| Raging Bolt | 2 | 6% | Tapu Koko (1), Tinkaton-Gamma (1) |
| Volcanion-Delta | 2 | 6% | Ectarachnid (2), Sevygarde (2) — Miasma Leak ability |
| Sevygarde | 2 | 6% | Volcanion-Delta (2), Ectarachnid (2) |
| Typhlosion-Delta | 2 | 6% | Swampert (2) — always Drizzle |
| Ninetales / Regice / Mamoswine / Tentacruel / Glalie | 2 each | 6% | Opponent_D's ice spam team, twice |
| Greattusk | 2 | 6% | Mixed |
| Alomomola | 2 | 6% | Mixed water support |
| Meowscarada | 2 | 6% | Mixed |
| Weavile | 2 | 6% | Mixed |
| Tapu Lele | 2 | 6% | Mixed |
| Ceruledge | 2 | 6% | Mixed |
| Zapdos | 2 | 6% | Ironvaliant (2), Heatran (2) — Opponent_B's later-window pivot |
| Charizard | 2 | 6% | One Drought variant (Opponent_I), one generic |
| Grimmeon | 2 | 6% | Mixed Dark/Fairy utility |

**Long tail (1× each, ~50 mons):** Jirachi, Cosmachi, Hippowdon, Gogoat-Delta, Flygon-Normal, Flygon-Ultra, Whimsicott, Kommoo, Mega Gardevoir, Radiantmoon, Slowking, Victini-Delta, Rillaboom, Keldeo, Hoopa-Unbound, Blaziken, Enamorus, Arcanine-Delta, Banette, Grimmsnarl, Ironblaster, Aggron, Dragapult, Clefable, Beedrill, Kleavor, Slaughtermaus, Steelix-Delta, Shrookle, Terapagos-Terastal, Terapagos-Normal, Mew-Atom, Clodsire, Dondozo, Blissey, Slowhost, Araquanid, Articeon, Golisopod, Tapufini, Starmie, Landorus, Valianttime, Archapult, Spectreon, Tapukehe, Samurott, Gyarados, Metagross, Ironhands, Machamp, Staraptor, Drifblimp, Barraskewda, Greninja, Urshifu, Latios, Sceptile, Excadrill, Gimmighoul, Joltik, Floatzel, Karrablast, Gastly, Tinkaton-Omega, Dragonite-mega.

## Archetype distribution

| Archetype | Captures | Example opponent(s) | Lead pattern |
|---|---|---|---|
| **Bulky offense (Heatran / Ironvaliant / Tinkaton-G / Ogerpon-W core)** | 10 | Opponent_A (×3 same team), Opponent_B (×4, two builds), Opponent_AA, Opponent_F-adjacent | Heatran-Delta or Heatran-Normal lead for Stealth Rock |
| **Tapu Koko electric-terrain offense** | 4 | Opponent_M, Opponent_N, Opponent_O, Opponent_E (×2 same team) | Tapu Koko Volt Switch lead |
| **Sand** | 2 | Opponent_E #1 (Tyranitar deltastream — see flag), Opponent_H (Tyranitar Sand Stream + Ferro/Hydrapple-U/Corv) | Hippowdon or Tyranitar lead |
| **Rain** | 2 | Opponent_K (Typhlosion-D + Swampert + Eruptois utility), Opponent_L (Typhlosion-D + Barraskewda + Greninja + Swampert) | Typhlosion-Delta Drizzle lead |
| **Aurora Veil ice HO** | 2 | Opponent_D (×2 same team) | Ninetales Snow Warning + Aurora Veil → Mamoswine LO breaker |
| **Bulky balance / mixed pivot** | 4 | Opponent_F (Slowking/Victini-D/Tusk/Rilla/Keldeo/Alomo), Opponent_P, Opponent_G (utility variant), Opponent_Q (hazard-stack) | No fixed lead |
| **Sevygarde / Volcanion-Delta poison core** | 2 | Opponent_R, Opponent_S | Mixed |
| **Web HO** | 1 | Opponent_T (Tinkaton-Omega web → Iron Moth / Kingambit / Cornerstone Ogerpon / Raging Bolt / Enamorus) | Tinkaton-Omega Sticky Web lead |
| **Stall** | 1 | Opponent_J (Mew-Atom/Gliscor/Corv/Clodsire/Dondozo/Blissey) | Variable |
| **Bug spam offense** | 1 | Opponent_U (Meowscarada/Beedrill/Ectarachnid/Kleavor/Slaughtermaus/Kingambit) | Lead Meowscarada |
| **Water spam** | 1 | Opponent_V (Araquanid/Articeon/Golisopod/Tapufini/Starmie/Alomo) | Variable |
| **Hydrapple-U + Wellspring pivot stack** | 1 | Opponent_W | Mixed |
| **Cheese / troll** | 1 | Opponent_C #2 — all-NFE/low-level team (Excadrill/Gimmighoul/Joltik/Floatzel/Karrablast/Gastly). Forfeit-bait. | n/a |
| **Disorganized / hard to classify** | 5 | Opponent_X, Opponent_Y, Opponent_C #1, Opponent_Z, Opponent_L-adjacent | Likely sub-1500 |

**Key lead-pattern reads:**
- The **Heatran-lead rocks → Tinkaton-G defog → Ironvaliant/Marsh-D pressure** sequence is the modal flow this week. If you don't know what's coming, plan for that.
- **Tapu Koko Volt Switch** is the second-most-common lead (4 captures, distinct opponents).
- Typhlosion-Delta Drizzle is the rain tell on T1.

## Confirmed sets seen on ladder

Cross-checked against `notes/mod_days.md` where applicable.

- **Tinkaton-Gamma (Parasol Prayer):** Updraft / Moonblast / Defog / Moonlight observed across 10 captures. ✓ Matches `mod_days.md` canonical set exactly. **Confirmed in the wild (10/10 teams).**
- **Heatran-Normal (Air Balloon):** Stealth Rock / Earth Power / Magma Storm or Flamethrower or Scald / Protect or Flash Cannon. Seen 6× with Air Balloon, 2× with Leftovers, 1× explicit Flash Fire (Opponent_N). One Opponent_B capture revealed **"Pressurize" as a 4th move slot** which is actually the ability name — likely a mod display artifact (Pressurize is an *ability*, not a move). Otherwise standard Showdown rocks Heatran. ✓ Matches doc framing.
- **Heatran-Delta (Pressurize):** Scald / Stealth Rock / Earth Power, sometimes 4th. 5 captures. Pressurize confirmed as the live ability in capture #26 (Opponent_A #2 — explicit move-slot reveal again, same artifact). ✓ **Pressurize is the locked ability** — escalate from "possible" to "documented" in `mod_days.md`.
- **Ironvaliant-Normal (Quark Drive, often @ Upgrade):** Moonblast / Thunderbolt / Knock Off or Destiny Bond. 11 captures, item revealed as Upgrade in 4. ✓ Matches `mod_days.md` Upgrade Quark Drive canonical set.
- **Ogerpon-Wellspring (Water Absorb):** Horn Leech / Ivy Cudgel / Swords Dance / (U-turn or Spiky Shield). 7 captures, Water Absorb confirmed in 3. ✓ Standard.
- **Marshadow-Delta:** Spectral Thief / Shadow Sneak / Flare Blitz. 7 captures, fully consistent. One Life Orb confirmed (Opponent_AA). ✓ Matches `mod_days.md`.
- **Mawile:** Swords Dance / Sucker Punch / Play Rough or Iron Head. 5 captures, ability never revealed but offensive set is consistent. Pairs with the Opponent_A template every time.
- **Dragonite-Normal:** Dragon Dance / Extreme Speed / Dual Wingbeat (or Draco Meteor + Ice Beam on the special variant). Two sets visible — DD physical and CM-less special pivot. Both on Opponent_B.
- **Iron Moth (Quark Drive @ Upgrade):** Sludge Wave / Fiery Dance. ✓ Matches `mod_days.md`.
- **Gholdaton (Life Orb or Leftovers):** Swords Dance / Supercell Slam / Skitter Smack. Ability never revealed — `mod_days.md` says default Surge Surfer with Tapu Koko; pair appears 3/3 times. ✓
- **Eruptois (Leftovers):** Lava Plume / Scald / Heat Siphon / Rapid Spin. Same defensive utility set as 8-capture pass. ✗ **Diverges from `mod_days.md`** — doc frames Eruptois as a "struggling breaker"; captures show defensive hazard-removal role. Still flagged for documentation update.
- **Cosmachi (set):** Encore / Wish / Ether Burst / Thunder Wave. 1 capture only this window. **Not in `mod_days.md`** — **new entry candidate** (carries over from prior pass).
- **Tyranitar (Sand Stream, Opponent_H):** Stealth Rock / Knock Off. Standard sand setter. ✓
- **Tyranitar (deltastream, Opponent_E capture #2 only):** Rock Slide. **Did NOT reappear in new captures.** Stays a one-off. See "New / unusual" below.
- **Volcanion-Delta (Miasma Leak, Black Sludge):** Earth Power confirmed once, full set unseen. **Not in `mod_days.md`** — new entry candidate.
- **Sevygarde:** Thousand Arrows / Substitute / Poison Jab @ Leftovers (Opponent_R). Note this is **Subs Lefties, NOT the CB Thousand Arrows set** `discord-sentiment.md` says is the only good build. Either a mid-ladder misbuild or evidence the channel's "CB only" verdict is overstated. ✗ Diverges from sentiment doc.
- **Tapukehe (Corrosive Surge):** Flip Turn confirmed. ✓ Matches `mod_days.md` framing.
- **Spectreon (Life Orb):** Destiny Bond / Protect / Whisk Away. Standard.
- **Mew-Atom (Acclimate):** Psychic Noise / Gene Splice. New variant, **not in `mod_days.md`** — new entry candidate.
- **Ferrothorn (Iron Barbs @ Leftovers):** Spikes / Leech Seed / Body Press or Power Whip / Gyro Ball or Curse. 3 captures, all running Spikes. ✓
- **Hydrapple-Ultra:** Sludge Bomb / Fickle Beam or Energy Ball. Item unrevealed in both captures. Sludge Bomb confirms the `discord-sentiment.md` "Sludge Bomb has replaced Giga Drain" claim. ✓
- **Ninetales (Snow Warning):** Aurora Veil / Dazzling Gleam / Extrasensory / Blizzard. Veil setter for Opponent_D's HO. ✓ Standard.
- **Tinkaton-Omega (Fairy/Bug):** Sticky Web lead — only Opponent_T still. **Not in `mod_days.md`.** Did not reappear in new captures but stays a documented variant.

## Recurring cores / pair frequencies

Now meaningful at 36 captures:

- **Heatran + Tinkaton-Gamma + Ironvaliant 3-core:** appears in **7 teams** (Opponent_A ×3, Opponent_B ×3 of 4, Opponent_AA-adjacent). This is the dominant bulky offense template right now.
- **+ Ogerpon-Wellspring 4-core:** the above 3 + Wellspring appears in **6 teams** — basically the same group. If you see Tinkaton-Gamma early, plan for Wellspring SD as a wincon.
- **Opponent_A's locked 6:** Heatran-Delta / Ironvaliant / Tinkaton-Gamma / Ogerpon-W / Mawile / Marshadow-Delta — same team 3 times. **Highest-confidence rematch prep on the ladder.**
- **Opponent_B evolution:** weeks 1-2 ran Gliscor + Mawile + Dragonite + Ironvaliant + Heatran + Tinkaton-G; week 3 swapped Gliscor/Mawile out for Zapdos + Ogerpon-Wellspring. Two stable builds — track which one leads.
- **Tapu Koko + Gholdaton:** 3/3 Gholdaton appearances pair with Tapu Koko. Matches the channel's canonical Surge Surfer Gholdaton pair.
- **Typhlosion-Delta + Mega Swampert:** 2/2 rain teams run this pair. The rain tell.
- **Ninetales + Regice + Mamoswine + Tentacruel + Glalie + Kartana:** Opponent_D's full Aurora Veil ice HO, twice. Memorize it.
- **Ferrothorn + Corviknight:** hazard stack pair in 2/3 Ferro teams.
- **Sevygarde + Volcanion-Delta + Ectarachnid:** appears in 2 teams (Opponent_R, Opponent_S). Potential emerging core to watch.

## New or unusual picks worth flagging

1. **Mew-Atom (Acclimate, Psychic/Poison) — Opponent_J.** Stall lead, Psychic Noise + Gene Splice. **Not in `mod_days.md`.** Worth an entry — this looks like a new mod-released variant.
2. **Volcanion-Delta (Miasma Leak, Dark/Poison).** 2 captures with same ability. **Not in `mod_days.md`.** Add entry.
3. **Cosmachi (full utility set).** Still not in `mod_days.md`; carrying over from the 8-capture flag.
4. **Tinkaton-Omega (Fairy/Bug, Sticky Web lead).** Still only 1 capture (Opponent_T), still not in `mod_days.md`. Variant exists but is rare.
5. **Tyranitar Delta Stream — UNCONFIRMED.** Did **not** reappear in 28 new captures. Opponent_H's Tyranitar uses canonical Sand Stream. The Opponent_E #1 sighting stays a likely capture-snapshot glitch or a one-off custom Smogon-style import. Lowering confidence; do not document as a real variant.
6. **Heatran-Delta "Pressurize" appearing as a 4th move slot** (captures #26 Opponent_A #2, #36 Opponent_B #4 for Heatran-Normal too). This is a mod display artifact — the ability is leaking into the moves list. Note in `mod_days.md` so we don't misread future captures.
7. **Charizard Drought variant** (Opponent_I) — sun setter (Charizard + Tapu Lele + Heatran-Delta + Terapagos + Flygon-Ultra Spikes + Shrookle). Unusual sun build, single capture.
8. **Flygon-Ultra (Steel/Dragon, Spikes / Steel Skewer)** — same Opponent_I team. Spike-setter Flygon variant; likely worth a `mod_days.md` entry if it reappears.
9. **Terapagos appearing twice** (Terapagos-Terastal Opponent_I, Terapagos-Normal Opponent_Y) — both with Tera Shell ability. Becoming a real ladder pick despite no `mod_days.md` entry.
10. **Sevygarde Subs-Lefties set** (Opponent_R) — diverges from channel "CB only" sentiment. Possibly a mid-ladder misbuild OR an underdocumented set.
11. **Dragonite-mega** (Opponent_O) — Mega stone confirmed, Dragon Pulse / Hurricane special set.
12. **Valianttime (Transience, Steel/Fairy)** — Opponent_C. Single capture, unusual mon, set unrevealed.
13. **Opponent_C #2 cheese team** — six unevolved/low-level mons (Excadrill, Gimmighoul-Roaming, Joltik, Karrablast, Gastly, Floatzel). Almost certainly a forfeit-bait or smurf account. Ignore for archetype counting.

## Comparison to other signals

| Claim / source | Captures (36) show | Verdict |
|---|---|---|
| `discord-sentiment.md`: Sevigarde "only CB Thousand Arrows is good" | 2 captures, **1 is Subs-Lefties not CB** | Mild contradiction; channel verdict may be overstated |
| `discord-sentiment.md`: Hydrapple-Ultra meta-relevant, AV/Boots split, Sludge Bomb replaces Giga Drain | 2 captures, both running Sludge Bomb | ✓ confirms |
| `discord-sentiment.md`: G-Zapdos is canonical rain Flying (Iron Sentinel demoted) | 0 G-Zapdos in rain teams; 0 Iron Sentinel anywhere. 2 Zapdos captures are on bulky balance (Opponent_B), not rain. | Neither claim contradicted but neither confirmed either |
| `discord-sentiment.md`: Tinkaton-Gamma settled set (Boots/Moonblast/Updraft/Moonlight/Defog) | 10/10 captures match | ✓ strongly confirms |
| `discord-sentiment.md`: Gholdaton "fine, not broken", Tapu Koko Surge Surfer pair canonical | 3/3 Gholdaton appearances paired with Tapu Koko | ✓ confirms the pair, prevalence is moderate |
| `mod_days.md`: Tinkaton-Gamma S-tier glue | 28% of teams — actually top-3 most common mon | ✓ S-tier validated |
| `mod_days.md`: Eruptois "struggles" framing | 1 capture, defensive utility set (Lava Plume / Scald / Heat Siphon / Rapid Spin) | ✗ Diverges, see action items |
| `mod_days.md`: Heatran-Delta BP investment concerns, ability unclear | 5 captures, Pressurize consistent | Update `mod_days.md` to lock Pressurize |
| `mod_days.md`: Kingambit standard cleaner | 3/36 captures, Supreme Overlord confirmed once | Present but not dominant |
| `mod_days.md`: Iron Moth Upgrade Quark Drive | 2 captures, both with Upgrade | ✓ confirms |
| `data/usage/season-6-mid-1500.generated.json`: aggregate rankings | Ironvaliant / Heatran / Tinkaton-G / Ogerpon-W cluster mirrors top of usage | ✓ ladder aligns with mid-1500 scrape |

**Surprises:**
- **Sevigarde appeared 2× despite the channel hype** — way less common than chatter implies. Either the post-release surge cooled, or it's gatekept by Iron Pilot price tier (only certain clients can afford it).
- **Hydrapple-Ultra at only 2/36** — channel hot but ladder presence modest. Could be sample-window bias (only 4-day window).
- **Mawile at 14%** — way more prevalent than `mod_days.md` or sentiment doc would suggest. Driven entirely by the Opponent_A/Opponent_B bulky-offense template using it as a Sucker Punch / SD wincon.
- **Marshadow-Delta at 19%** — top-5 mon, on every variant of the Heatran/Ironvaliant/Tinkaton core.
- **Iron Sentinel still at 0** — same as prior pass. Channel "demoted to UU" verdict holds.

## Per-opponent scouting (rematch prep)

**Opponent_A (3 captures, locked team):**
> Heatran-Delta / Ironvaliant-Normal Upgrade / Tinkaton-Gamma / Ogerpon-Wellspring / Mawile / Marshadow-Delta
- Most-laddered opponent this window. Same six every time. Heatran-Delta or Tinkaton-Gamma lead. SD Wellspring is the late-game wincon. Bring a Steel-resistant Fire answer (Heatran-Delta hits Mawile + Tinkaton + Ironvaliant in different ways) and a way to revenge Wellspring after a SD. **Highest rematch-prep value of any opponent.**

**Opponent_B (4 captures, 2 builds):**
- **Build A** (captures 19, 23): Gliscor / Mawile / Ironvaliant / Dragonite / Heatran-Air Balloon / Tinkaton-Gamma. Bulky offense with Gliscor as the SR + status anchor and Mawile/Dragonite as physical wincons.
- **Build B** (captures 34, 36): Zapdos-Leftovers / Ironvaliant / Dragonite / Heatran-Air Balloon / Ogerpon-Wellspring / Tinkaton-Gamma. Drops Gliscor + Mawile, adds Zapdos pivot + Wellspring. More offensive.
- Tells: if you see Zapdos T1 or T2, it's Build B. Either way Ironvaliant + Tinkaton-G + Heatran + Dragonite is the locked 4-core.

**Opponent_E (3 captures, 2 builds):**
- Sand-deltastream team (capture 2, possibly snapshot glitch — probably won't see it again).
- Mixed offense: Tapu Koko / Ironvaliant / Hoopa-Unbound / Garchomp / Marshadow-Delta / Tinkaton-Gamma. Captures 6 and 9 identical.

**Opponent_C (2 captures):** Wildly different teams between matches — once a real Greattusk/Valianttime/Iron Moth team, once a 6-unevolved cheese team. Either a smurf alt or two players sharing a handle. Don't rematch-prep.

**Opponent_D (2 captures, locked team):** Ninetales Aurora Veil + Mamoswine LO + Glalie + Regice + Tentacruel + Kartana. Snow HO; lead Ninetales every time. Bring a fast Fire or steel-priority answer.

**Other opponents are one-offs; no scouting carry-over.**

## Action items for `mod_days.md`

1. **Add Mew-Atom entry** (Acclimate, Psychic/Poison, Psychic Noise + Gene Splice). New variant on stall.
2. **Add Volcanion-Delta entry** (Miasma Leak, Dark/Poison). 2 captures, real pick.
3. **Add Cosmachi entry** (Encore/Wish/Ether Burst/T-Wave utility). Carrying over from prior pass.
4. **Lock Heatran-Delta Pressurize** as the documented ability — 5 confirmations.
5. **Update Eruptois entry** — defensive Lava Plume / Scald / Heat Siphon / Rapid Spin role, not "struggling breaker." Carrying over.
6. **Note Pressurize as ability vs. move display artifact** — captures may show Pressurize in the moves list when it's actually the ability. Don't misread.
7. **Add Tinkaton-Omega entry** (Fairy/Bug, Sticky Web lead). 1 capture but documented variant exists. Carrying over.
8. **Investigate Tyranitar deltastream:** still only 1 capture across 36, no rematch. **Lower confidence — likely glitch/import artifact, not a real custom variant.** Do not document.
9. **Add Flygon-Ultra entry** (Steel/Dragon, Spikes + Steel Skewer). 1 capture but distinctive variant.
10. **Add Valianttime entry** (Transience, Steel/Fairy) if it reappears.
11. **Cross-check Sevygarde "CB only" sentiment** — captured Subs-Lefties set suggests the channel verdict may be overstated, or this is a mid-ladder misbuild. Worth a sentiment-doc note.
12. **Re-run after another 30-50 captures** to validate prevalence rankings 10-20 (currently directional, not statistical).
