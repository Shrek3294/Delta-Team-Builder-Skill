# Discord ranked-channel sentiment

> **Source:** `#🥇｜competitive` (channel `1091426589964771368`).
> **Window:** 21 days, 2026-04-29 23:21 UTC → 2026-05-19 ~09:08 UTC.
> **Messages analyzed:** ~21,882 (across 5 raw dumps).
> **Latest raw dumps:** `data/discord-ranked/raw/2026-04-29_to_2026-05-06.jsonl`, `2026-05-06_to_2026-05-13.jsonl`, `2026-05-14.jsonl`, `2026-05-16.jsonl`, `2026-05-19.jsonl` (covers 5/16 06:12 UTC → 5/19 09:08 UTC, 2,006 messages).
>
> **Reliability note:** Discord opinions are *signal, not fact*. Weight against `notes/mod_days.md`, `data/usage/season-6-mid-1500.generated.json`, and the viability PDF before letting any item here change a build call. Use the way you'd use a scouting report — directional, not authoritative.
>
> **Cadence:** ~1,040 msgs/day average across ~180 distinct authors. Week 1: 4/30 (1,488) · 5/01 (1,770) · 5/02 (564) · 5/03 (1,775 — Iron Sentinel release) · 5/04 (578) · 5/05 (596) · 5/06 (774 — status mechanics patch). Week 2: 5/07 (872) · 5/08 (1,462) · 5/09 (1,232) · 5/10 (1,792 — Hydrapple-Ultra release). Week 3: 5/11 (828) · 5/12 (1,244) · 5/13 (2,207 — VGC ban list) · 5/14 (411) · 5/15 (Sevigarde release, see 5/16 dump) · 5/16 (793 — Sevigarde post-release autopsy) · 5/17 (618 — Trapinch-ATOM teaser) · 5/18 (387) · 5/19 (208, partial).
>
> **Major dev events in window:** (1) 5/06 ranked-season patch swapped Sleep / Para / Freeze to Pokemon Champions mechanics. (2) Iron Sentinel released 5/03. (3) Hydrapple-Ultra released 5/10. (4) Sevigarde released 5/15. (5) Trapinch-ATOM teased/added to Showdown teambuilder around 5/17 — Bug/Water pre-evo paradox, see Hot section.

## Hot right now (last 7 days, 2026-05-13 → 2026-05-19)

### Sevigarde — 4 days post-release verdict
The pre-release hype collapsed; the post-release autopsy crystallized. Channel consensus: **RUBL / UU tier, Choice Band breaker is the only viable set**, not a wincon. Dev (Invin) self-rated it as "mid" and said he's using Clodsire instead (msg `1505144533266993182`) — that's effectively the official confidence level.

- **Confirmed kit (still):** Thousand Arrows, Extreme Speed, Poison Fang, Poison Jab, Scale Shot (TM), Encore, Toxic, Haze, Dragon Tail, Rest. **No setup** (no Coil/DDance/SD/Glare). Shed Skin + Rest is the floor on bulk sets. Resists Stealth Rocks.
- **The only set people actually run: Choice Band Thousand Arrows breaker.** "If banded is the only good set there is no surprise factor" (Antheon msg `1505140401533747250`), counter-take from Floaty: "you cant swap into thousand arrows unless you're called ferrothorn" (msg `1505140473881301042`). Lab/lupss/Luna all converged here over the week.
  - **Damage cites that landed this week (CB):**
    > 252+ Atk Choice Band Sevygarde Thousand Arrows vs. 248 HP / 252+ Def Corviknight: 306-360 (76.6 - 90.2%) — guaranteed 2HKO after Leftovers (floaty msg `1505140273246769203`)
    >
    > 252+ Atk Choice Band Sevygarde Thousand Arrows vs. 252 HP / 252+ Def Uxie-Delta: 288-338 (88.8 - 104.3%) — 31.3% chance to OHKO (Lupsss msg `1506149767573536880`)
    >
    > 252+ Atk Choice Band Sevygarde Thousand Arrows vs. 0 HP / 4 Def Yanmellia: 288-339 (85.4 - 100.5%) — 6.3% chance to OHKO (Luna msg `1506150774860943400`)
    
    The Uxie-Delta hit is the big one — D-Uxie is the canonical defensive Psychic glue on bulky teams, and CB Sevigarde rolling OHKO with no setup is a real wallbreaker thesis.
- **Thousand Arrows mechanic clarification (Luna + Lupsss):** TArrows hits Flying types neutrally (not super effective) because it grounds them first; Levitate users take *normal* (always-neutral) damage. So D-Uxie eating 100% rolls is from sheer BP, not type advantage (msgs `1506150491791425637` → `1506150807568121877`).
- **The defensive Shed-Skin/Rest set is a "winning harder" set, not a real role** — even within the Rest defenders camp (beeg_lad, Fred) the position is "it can work" not "it's the play." Antheon's pushback held up: "If you're doing that you can live anything on your opponents team already which is winning by default" (msg `1505144951258742844`).
- **The competing-with-Nidoking thesis:**
  > "Sheer Force LO outputs more work than garde" (DreadfulGhost msg `1505139256635691100`)
  > "Mogged by Nidoking" / "Nidoking gets ice moves for the flying types so it must be better" (Invin sarcasm-cosign, msg `1505145310584897657`)
- **Real verdict for builds (4 days in):** Choice Band Thousand Arrows / Espeed / Poison STAB / coverage is the de facto set. Pair with a hazard setter — without rocks the CB damage drops out of OHKO range on Corviknight. **Not a wincon, not centerpiece.** If a client has one and wants to use it, slot as a wallbreaker; if they don't, do not push them to grind for one — the channel reads it as a UU staple, not an A-tier piece. The Iron Pilot Mind Drive anti-meta prediction from release week did NOT materialize — channel has not converged on a counter because it's not threatening enough to require one.

### Trapinch-ATOM (NEW — appeared in delta Showdown teambuilder ~5/17)
A new ATOM-variant Trapinch. **Bug/Water typing, 153 base Atk, 66 base Spe**, abilities **Hyper Cutter / Strong Jaw**. Released to the Showdown teambuilder around 5/17 (per Fred's stat screenshot msg `1505527446081110056` and Luna's "super strong delta trapinch" cosign msg `1505625601183322192`). Multi-author thread (Fred, beeg_lad, Bio, mvincent05, Smudget, Luna, Lupsss, Dan, chillin, haqes, Kifi) over 5/17 — scope is delta ranked. *Not yet documented in `notes/mod_days.md` or `season meta changes.txt` — flag for the user to record.*

- **Movepool:** First Impression, Crabhammer, Aqua Step, Dual Divide, Ice Fang, Psychic Fangs, Crunch, Bite, Bug Bite, Leech Life. Gets Sticky Webs (per floaty msg `1505530812395946125`). **Strong Jaw is the HA** — Ice Fang, Psy Fangs, Crunch, Bite are all boosted; **Bug Bite is NOT a biting move** in implementation (multi-author confirmation: beeg_lad / Bio / Luna / Fred — channel-known consistent translation quirk).
- **Set direction discussed (mvincent05 + Smudget):**
  > 252+ Atk Choice Band Trapinch First Impression vs. 252 HP / 4 Def Landorus-Therian: 165-195 (43.1 - 51%) — 97.7% chance to 2HKO after Stealth Rock (msg `1505588896107462767`)
  >
  > -1 252+ Atk Choice Band Strong Jaw Trapinch Ice Fang vs. 252 HP / 4 Def Landorus-Therian: 568-672 (148.6 - 175.9%) — guaranteed OHKO (msg `1505591455518032035`)
  
  CB First Impression breaker is the obvious set (Fred / mvincent05 / Smudget); Trick Room slot also floated for the 66 Spe (Smudget msg `1505548793154769059`, kapi msg `1505644876757471354`).
- **STABmons / draft note:** Smudget's STABmons set was Aqua Step / Dual Divide / Leech Life / coverage — explicitly NOT First Impression because "u turn + set up is not the play" and "dual divide is its only way to touch steels" (msgs `1505551813288525926` → `1505554036223643749`). For ranked singles, CB First Impression is the lean.
- **Pre-evo caveat:** "it's a pre-evo atom so it's not gonna be great" (haqes msg `1505542754367836191`); "I don't think it will be meta by any means but it has threat potential" (beeg_lad msg `1505531198577836224`). Smudget speculation that more evos drop later: "fuck bug type 🔥 delta will only have 3 bug types 🔥" — joking about typing direction.
- **Verdict for builds:** Treat as a potential CB First Impression revenge breaker — strong on a TR team or as a Lando-T / non-Sash physical answer. Confirm with the user before recommending: this is brand new and not in `mod_days.md` yet. Not a centerpiece. If the client owns one and wants to use it, slot 6 only.

### Hydrapple-Ultra — item meta has split
9 days post-release. Channel verdict has flipped from "AV Regen default" to **AV vs Heavy-Duty Boots is now a live debate**, with Boots gaining ground.

- **Item split (goon_6's prompt + responses, msgs `1505652678968082453` → `1505655091804246057`):** Lupsss/Plains lean **Boots** ("the same sets you run on regular hydrapple but you swap giga drain with sludge bomb" — Luna msg `1505658221854199899`). Paradise + beeg_lad + DeS keep **AV** ("being able to just eat fairy hits as a dragon is a luxury they don't usually have" — beeg_lad msg `1505655239133495567`).
- **Rocky Helmet variant suggested** by LeedleBob (msg `1505668038064603328`) — "Wogerpon will be in shambles trying to u-turn unpunished." Real take given Ultra's U-turn resist; not yet adopted by main voices.
- **Standard moveslot tweak from base Hydrapple:** swap Giga Drain for Sludge Bomb (Luna). Earth Power stays for Steels. "walls woger lowk. Boosted poison type giga drain is also super powerful on a fat mon like that" (Dan msg `1505764137693876294`).
- **Tier sentiment hardening:** "Need uapple in s tier asap" (Paradise msg `1505596499197825115`), Trigby cosign "facts." Channel reads it as overperforming.
- **Verdict update for builds:** **Default to AV Regen for clients who want defensive utility / pivot value, Boots for clients on offensive/balanced teams who want to abuse the U-turn resist for switch-in safety.** Sludge Bomb is now in the canonical 4-move set over Giga Drain. Continue to flag nerf-volatility risk to clients — channel still expects mid-season nerf ("It is going to be so funny when hydrapple ends up nerfed" from week 3 still in the air).

### Gholdaton SD + Recover under Electric Terrain — the new "should this be nerfed" mon
Replaces Drifblimp as the channel's polarizing wincon. Multi-author over 5/19 (dreadfulghost, durian cultist, Lupsss, Milk, Luna, lab9850).

- **Complaint:** "We need to nerf gholdaton again" / "I hate SD + recover" (DreadfulGhost msgs `1506149874012258355`/`1506149936977416192`). durian cultist agrees it's "really hard to beat on eterrain" (msg `1506150016467730482`) but stops short of nerf-worthy.
- **Defense:** "Gholdaton is fine imo... can't break grounds as it wants to unless you're Clodsire or a frail Nidoking. Swampert/Landorus/Gliscor/Sevygarde and god knows how many more mons eats Gholdaton for breakfast because they got the bulk" (Lupsss msgs `1506150127012679711` → `1506150708481888277`). Milk: "very very good but not broken it's balanced by 4mss" (msg `1506151046299390012`).
- **Verdict:** Bulky physical Ground answers are the consensus check (Swampert / Lando-T / Gliscor / Sevygarde). Off-Electric Terrain it's just a wall. Stick to the canonical Surge Surfer + Tapu Koko pair from `mod_days.md`; do not switch to Good as Gold without a strong reason.

### Tinkaton-Gamma — checks evolving
A new line on the established Gammaton check list: **Choice Band Barraskewda Poison Jab OHKOs** (HeartUnderBlade msg `1505980366521892946`):
> 252+ Atk Choice Band Barraskewda Poison Jab vs. 252 HP / 4 Def Tinkaton-Gamma: 382-450 (102.1 - 120.3%) — guaranteed OHKO

"It doesn't need to be stab" (msg `1505980354027192320`) — the lesson is "any strong physical attacker with poison or steel coverage works." Adds to the existing Heavy Slam Great Tusk / Iron Moth Sludge Wave / Iron Pilot answer set. **Update for rain builds:** CB Barraskewda already on rain teams is now a Gammaton answer too — no need to over-build for Gammaton on rain.

## Established / settled (from earlier in the 21-day window)

### Iron Sentinel — channel verdict downgraded (Established + sentiment shift)
beeg_lad opened a 5/16-late retrospective (msg `1505354006887792811`); creationq's response landed it as **decent but outclassed by Galarian Zapdos on rain**.

- "id rather have zapdos on my rain team" (creationq msg `1505357467289129072`). "It's frail and stealth rock weak" / "aint noone clicking defog with a mon that frail" (msgs `1505357764820602954`/`1505358017485602816`). Dan cosign: "It truly does not get better than Zapdos. Ou staple since gen 1" (msg `1505359775490113738`).
- The Flying Future Sight is the only differentiator, and "doesn't even work in rain" (beeg_lad msg `1505358354250334259`).
- **Iron Sentinel is legal in ranked play** — the budget tournament ban from week 1 is *tournament-specific only*.
- **Verdict for builds:** Keep as situational mention; don't push it onto rain teams over Galarian Zapdos. Best on Electric or Rain teams that already have a Defogger and need a future-sight pivot.

### Hydrapple-Ultra (Poison/Dragon, released 2026-05-10)
See Hot section for the new Boots/AV split. Canonical AV Regen set still in `notes/mod_days.md`. Sludge Bomb has displaced Giga Drain in the consensus 4-move set. Kingambit "giga walls it", Mega Mawile +2 Play Rough OHKOs uninvested, Specs Tapu Lele Psyshock OHKOs through AV in Psychic Terrain, Great Tusk Headlong Rush is the physical answer.

### DDance Kyurem — established HO threat
Sub / Roost / DDance set noted as still being run despite Alomomola — "that is like, an extremely common kyurem set" (HeartUnderBlade msg `1506146814162767894`). Lab dissents: "scummy set" (msg `1506147064961175703`). durian cultist: "I'd rather play against that than some of the more annoying mons on the server" (msg `1506147245555323042`). Standard sets unchanged from week 2: Icicle Spear / DDance / Earth Power / Marshadow-Delta coverage; or Sub / Roost / DDance / Icicle Spear only if you can break Alomomola.

### Corrosive Terrain teambuilding (now settled, mechanic-clarified)
Atè still running corrosive teams 5/18 onwards. **Mechanics clarification by Luna/Milk for new builders (msgs `1506175168949784606` → `1506187159403761735`):**
- C-Terrain cuts Steel-type move damage by 50% on grounded targets.
- Hitting Steel types with Poison moves was a Corrosion ability mechanic — **removed at some prior point.** "i thiiink that it used to be where if you had corrosion you could hit steel types with poison moves however i think that has since been removed" (Luna msg `1506187159403761735`).
- Toxic Chain, Poison Heal, Toxic Boost are confirmed removed from the C-Terrain interaction (Luna msg `1506185999506473021`).
- Merciless is "crit if poisoned" (NOT a steel-hit ability — clears up earlier confusion, Milk msg `1506176047694221362`).
- Pieces named (consistent with week 2): D-Mesprit, Veneon, Hydrapple-Ultra, Sneasler + Corrosive Seed + Unburden, Ferrothorn, Tinkaton-Gamma (NOT protected — airborne).

### Mega Delta Lopunny set wars (settled in week 2 — Fake Out / ESpeed / CC / Cold Departure with QM)
No new discussion in 5/16-5/19 window. Default set carries.

### Tinkaton-Gamma standard set (settled — Boots / Moonblast / Updraft / Moonlight / Defog)
Reaffirmed by Dan (msg `1505748592403546203`): "boots moonblast updraft moonlight defog, max hp and spdef." Matches `mod_days.md` exactly.

### Girashadow (settled — fast Will-O-Wisp / Hex with Defog)
Multi-author reaffirmation 5/18 (beeg_lad asks msg `1506005085174501500`, Luna: "Fast bulky will-o hex" msg `1506005397331513384`). Flex 4th slot: Defog (most common), Knock Off, Draco Meteor, Dragon Pulse, Rest. Dan suggests "willo aura sphere" for Kingambit cover (msg `1506012730736382092`).

### Mono-Fairy / D-Meowscarada (settled — Purranormal Specs Moonblast)
No new discussion. Carry forward.

### Drifblimp CM / Strength Sap (settled — polarizing stall, doubles-only ban)
No new takes in window. Polarizing but unaffected by the 5/13 doubles ban.

### Galarian Zapdos (settled — CB pivot, top-ladder staple)
Newly reinforced as the canonical rain Flying slot (see Iron Sentinel demotion above).

### Liesler / Mega Slaughtermaus / Spectreon / Energeist
No new discussion this window. Established positions hold.

## Active complaints / sentiment shifts

- **Gholdaton SD-Recover frustration** (new, see Hot). Specifically the Electric Terrain Surge Surfer + SD + Recover line.
- **"Eventually every delta mon is gonna 'need' nerfs until it's just nat dex ou again"** — Dan (msg `1505855529698721854`) summarizing the meta-fatigue with Invin's nerf cadence. dreadfulghost cosign: "Champions will fix this." Just venting, not actionable.
- **Shrookle epidemic on ranked** (floaty msg `1505862391462891601`): "whats with the shrookle epidemic." Counters re-listed: sun teams (Harvest exploits!), Brickchef msg `1505870994688970853` recommends Adamant Band Hoopa-U Zen Headbutt OHKOs. Taunt users (Bio). Real signal for client builds — if a client expects ladder grind, expect Shrookle webs leads.
- **Iron Pilot price gate** — Pilot is "more like 1.5 mil" (Dan msg `1505500331448991814`). Affects which clients can afford to slot it. Iron Valiant 400k cheapest (skinned). 
- **Items are "banned in ranked" confusion** — chillin questioned this (msg `1505608485088526416`) — there ARE banned items in `#info` (per Smudget msg `1505719175115575516`). Not specifically problematic for builds, just noise.
- **Mainline-feeling-creep** — dreadfulghost: "Moonblast and iron head got nerfed to be more honest" (msg `1505855998215065724`); Smudget: "YEAH NO FUCKING WONDER IRON HEAD GOT NERFED" looking at a screenshot (msg `1505706063150977147`). **Channel is talking about base-game / Champions nerfs, not delta-specific changes.** See conflicts section below. Do not act on this as a delta fact.

## Counter-meta tech

- **CB Barraskewda Poison Jab vs Gammaton** — guaranteed OHKO regardless of non-STAB (HeartUnderBlade msg `1505980366521892946`). Already on rain teams; pivotal anti-Gammaton bonus.
- **Bulletproof immune to Sludge Bomb** — relevant against Hydrapple-Ultra into Bulletproof users; Bullet Punch / Bullet Seed are punches, not "bullet"-tagged (lab9850 msgs `1506162857509650492` → `1506163203359379547`). Goolossal-with-Bulletproof remains a hard wall to Sludge Bomb-locked Hydrapple-Ultra.
- **CB First Impression Trapinch-ATOM** as a Lando-T revenge breaker (see Hot section).
- **Hyper Voice Eeveon** > Tri Attack — Guiltybench cite (msg `1506097522416943224`), Milk cosign. "all eevees" get it.
- **Sun teams answer Shrookle** — Harvest procs 100% under sun and SHrookle's berry-eat sustain becomes a vulnerability when you can OHKO through it before berry resets matter. Brickchef's CB Hoopa-U Zen Headbutt also OHKOs.
- **Rawst Berry Shrookle** (dreadfulghost msg `1505869783353131008`) — burn answer to Will-O-Wisp leads.
- **Spectreon / Mega Klocktowl as Pursuit trappers for Terapagos-ATOM** (durian cultist msg `1506144197126783186`) — fresh recommendation for clients running Terapagos teams.
- **Mega Naught is now Hydrapple-vulnerable** (durian cultist msg `1506155684687773707`): "With ultra hydrapple being so common it might struggle." Iron Defense / bulky Naught no longer a safe call.

## Patch / dev notes overheard

- **★ STATUS MECHANICS PATCHED 2026-05-06 (ranked singles) — reconfirmed in window.** Fred quoted the patch note verbatim (msg `1505949794349355090`) settling a debate about freeze duration:
  > Sleep, Paralysis and Freeze status conditions have been updated to Pokemon Champions mechanics
  > • Sleep now lasts 1-2 turns. You have a 33% chance to wake up on the second turn
  > • Paralysis will now only have a 12.5% chance to fully paralyze you rather than 25%
  > • Freeze now only lasts up to 3 turns with a 25% chance to thaw each turn.
- **Sevigarde released 2026-05-15** (last week). Channel verdict in Hot section. Invin's "this pokemon is mid. I'm using clodsire" (msg `1505144533266993182`) is the dev's authoritative tier read.
- **Trapinch-ATOM** added to delta Showdown teambuilder around 5/17. Bug/Water, 153 Atk / 66 Spe, Strong Jaw + Hyper Cutter. Multi-author confirmation (Fred, Bio, mvincent05, beeg_lad, Smudget, Luna — 6+ authors over the day on 5/17). Scope: **ranked singles** (Dan's "is sevygarde not supposed to have thousand arrows? it says its an illegal move on delta showdown" msg `1506018534558404769` confirms they're talking about delta showdown teambuilder which mirrors ranked). **Conflict with static notes: not present in `notes/mod_days.md` or `reference/season meta changes.txt`.** User should add to `notes/mod_days.md` and update `season meta changes.txt` under Additions/Releases. Date the release for 2026-05-17.
- **Hydrapple-Ultra dropped 2026-05-10** (established). Item meta has split AV vs Boots (see Hot).
- **Iron Sentinel released to ranked on or around 2026-05-03** (established). **Legal in ranked play.** Channel demoted to UU-level in 5/16 retrospective (see Established section).
- **Mega Gengar is banned in ranked** (established, multi-author thread 5/05).
- **Mega Greninja is banned in ranked** — reconfirmed in window: "It is but it's banned in ranked" (Fred msg `1505163857403056179`) responding to fresh asker. Multi-author chain (Plains + Fred). Passes 4a.
- **Good as Gold is banned in ranked.** Pengo1 asked Invin (msg `1505728766398304346`); Invin responded with a discord-channel-link citation to the original ranking-change post (msg `1505826967352639540`). Drasher's reasoning: "good as gold would be extra evil on delta because steel spikes also exist" (msg `1505743020165693470`). Authority confirmation (Invin) + multi-author thread — passes 4a strict sourcing.
- **Iron Head and Moonblast "got nerfed" — UNCONFIRMED for delta. Treat as channel speculation only.** Smudget (msg `1505706063150977147`, reacting to a screenshot) and dreadfulghost (msg `1505855998215065724`) — both reactions, no scope clarification, no Invin confirmation. **Conflict with static notes:** `reference/season meta changes.txt` line 81 explicitly states "Salt Cure / Moonblast / Leech Seed Champs nerfs are NOT in delta. Treat at original values." Earlier discord-sentiment also says Moonblast 10% SpA-drop nerf is not in delta per Lab. **Do not regress on this — treat Moonblast 95 BP unchanged and Iron Head unchanged in delta until Invin or a pinned source confirms otherwise.** Fails rule 4a (no authority, no scope multi-message thread).
- **Apex Tyrant nerf** — beeg_lad reference msg `1505854653173076031` ("we know what you did to that guy too… needed nerfs, but removing levitate might've been overkill"). Reaffirms Apex Tyrant got a real nerf (Levitate removal). Smudget's 1-of-1 status remains; sheet placement misleading.
- **Mega Galarian Slowbro still doesn't exist in delta ranked** (established). Showdown bug only.
- **Salt Cure / Moonblast Champs nerfs are NOT in delta** (established, see Iron Head/Moonblast confusion above).
- **Tera Type, Generic-typing Z-moves, Ubers-tier mons** all banned in ranked (DeS msg `1505222230009708554`: "Anything above S is banned in ranked"). Ranked viability sheet S-and-below is the legal pool.
- **Confusion mechanic NOT buffed** — durian cultist confirmed "nope same as its always been" to user wondering after rough confusion luck (msg `1506135524757471304`).
- **Mega Charizard-Delta** (DRG/Rock with Sheer Force) — channel pushback against it being good. "Slow mono dragon chud with sheer force" (Dan msg `1505286047917936821`). Luna: "if its dragon/ground id honestly rather just use garchomp or savage scar" (msg `1505287076759736360`). Process-of-elimination "best dragon rock type" but ranked-irrelevant.
- **Mega Lopunny screen/Pursuit-trapper meta** — Lab/beeg_lad floating Mega Absol Z as pursuit trapper for Dragapult cleanup (msg `1505515156417941634`). Speculative, not yet adopted.

## Substantive messages (quote bank)

- **Invin self-rating Sevigarde:**
  > "This pokemon is mid. I'm using clodsire" (msg `1505144533266993182`)
  >
  > "More like thousand losses !" (msg `1505145703612026892`)

- **Floaty defending CB Sevigarde despite the predictability complaint:**
  > "which doesnt matter because you cant swap into thousand arrows unless you're called ferrothorn" (msg `1505140473881301042`)

- **Lupsss reframing Sevigarde-CB into D-Uxie:**
  > "252+ Atk Choice Band Sevygarde Thousand Arrows vs. 252 HP / 252+ Def Uxie-Delta: 288-338 (88.8 - 104.3%) — 31.3% chance to OHKO" (msg `1506149767573536880`)

- **HeartUnderBlade on CB Barraskewda vs Gammaton:**
  > "it doesn't need to be stab · 252+ Atk Choice Band Barraskewda Poison Jab vs. 252 HP / 4 Def Tinkaton-Gamma: 382-450 (102.1 - 120.3%) -- guaranteed OHKO" (msgs `1505980354027192320` + `1505980366521892946`)

- **Fred quoting the status mechanics patch note (settles a freeze-mechanic dispute):**
  > "Sleep, Paralysis and Freeze status conditions have been updated to Pokemon Champions mechanics · Sleep now lasts 1-2 turns. You have a 33% chance to wake up on the second turn · Paralysis will now only have a 12.5% chance to fully paralyze you rather than 25% · Freeze now only lasts up to 3 turns with a 25% chance to thaw each turn." (msg `1505949794349355090`)

- **mvincent05 on Trapinch-ATOM Choice Band breaker (post-Champions FP buff):**
  > "atom trapinch seems like a funny band mon · especially with the first impression buff in champions · -1 252+ Atk Choice Band Strong Jaw Trapinch Ice Fang vs. 252 HP / 4 Def Landorus-Therian: 568-672 (148.6 - 175.9%) -- guaranteed OHKO" (msgs `1505588156878032937` + `1505588207889154129` + `1505591455518032035`)

- **Lupsss defending Gholdaton against the "nerf again" call:**
  > "Gholdaton is fine imo... can't break grounds as it wants to unless you're Clodsire or a frail Nidoking. Swampert/Landorus/Gliscor/Sevygarde and god knows how many more mons eats Gholdaton for breakfast because they got the bulk" (msgs `1506150127012679711` → `1506150708481888277`)

- **beeg_lad on Iron Sentinel's diminished role:**
  > "Just use zapdos · There is [a reason to not have both]: stacking very similar mons that cover the same threats offensively" (msgs `1505359588969676961` + `1505360576082219190`)

- **Luna explaining Thousand Arrows mechanic against Levitate vs Flying:**
  > "it is specifically neutral to flying mons · levitate takes normal damage always · its neutral ALWAYS thats fun actually" (msgs `1506150491791425637` + `1506150515690573894` + `1506150807568121877`)

- **Dan on Invin nerf-cadence fatigue:**
  > "Eventually every delta mon is gonna 'need' nerfs until it's just nat dex ou again" (msg `1505855529698721854`)

- **Brickchef's anti-Shrookle counter:**
  > "Just run hoopa-u the goat and click zen headbutt · adamant band ohkos it" (msgs `1505870994688970853` + `1505871046106943488`)

## How to use this in `/build`

1. **Don't quote channel takes as facts.** Treat as scouting — useful for "the meta is leaning this way," not for "this set is correct." Cross-check `notes/mod_days.md`, `data/usage/season-6-mid-1500.generated.json`, and the viability PDF before changing a build call.
2. **Sevigarde post-release reality check.** The pre-release "S-tier" hype is dead, and even the release-week "RUBL/UU defensive utility" verdict has been refined. **Channel consensus is now: CB Thousand Arrows breaker, no other set is competitive.** Invin self-rates as "mid." Do not push a client to grind for Sevigarde; if they own one, slot CB on a team that needs a Lando-T / D-Uxie / Corviknight breaker and has rocks support. The Iron Pilot Mind Drive anti-meta tech from week 3 is NOT needed — Sevigarde never reached the saturation that would have justified it.
3. **Trapinch-ATOM is a flag, not a build piece yet.** Confirm with the user before using. Not in `mod_days.md`. If client owns one and wants to use it: CB First Impression breaker is the lean, 66 Spe also supports TR. Add to `mod_days.md` and `season meta changes.txt` once user reconciles.
4. **Hydrapple-Ultra: AV vs Boots is now a choice, not a default.** AV Regen for defensive pivots; Heavy-Duty Boots for offensive teams that want the U-turn-resist swap-in safety. Sludge Bomb has replaced Giga Drain in the canonical 4-move set. Earth Power for Steels. Rocky Helmet variant is fringe — don't recommend yet.
5. **Status mechanics changed 5/06.** Sleep 1-2 turns, Para 12.5%, Freeze 3-turn cap 25% thaw. Salt Cure / Moonblast / Iron Head / Leech Seed are **NOT** nerfed in delta despite channel speculation in window. Treat as original values.
6. **Iron Sentinel is legal in ranked but no longer the rain pick.** Galarian Zapdos is the channel's canonical rain Flying. Use Iron Sentinel only if the client specifically wants the Flying Future Sight tech (and only outside rain).
7. **New Tinkaton-Gamma answer:** CB Barraskewda Poison Jab OHKOs. Useful for rain teams that needed a Gammaton answer slot they already had on the team. Heavy Slam Great Tusk remains the cleanest non-rain answer.
8. **Gholdaton is fine, not broken.** Bulky Ground answers (Swampert / Lando-T / Gliscor / Sevygarde) check it. Surge Surfer + Tapu Koko Electric Terrain is the meta pair.
9. **Shrookle is in a popularity wave** — clients on offensive teams should bring a Taunt user or sun support; a Hoopa-U Zen Headbutt is an explicit answer. Rawst Berry counters Will-O leads.
10. **Topic-specific weighting:**
    - Sevigarde: ONLY CB Thousand Arrows. Don't recommend Rest-Shed-Skin defensive sets — channel has moved off them.
    - Hydrapple-Ultra: AV Regen default; Boots if offensive. Sludge Bomb > Giga Drain now.
    - Trapinch-ATOM: confirm ownership and user-reconciliation first.
    - Iron Sentinel: outside-rain only; don't push as a rain piece.
    - Gholdaton: keep the canonical Surge Surfer set; bulky Grounds check it.
    - Tinkaton-Gamma: still Defog/Updraft utility from `mod_days.md`; clients on rain get Barraskewda Poison Jab "for free" as a Gammaton answer.
    - Girashadow: fast Will-O / Hex / Defog / flex (Dragon Tail, Knock Off, Aura Sphere for Kingambit) — Aura Sphere is new this week.
11. **Tonal cues:** the channel's voice remains short, opinionated, profanity OK. "bum"/"goated"/"chud"/"sahur" are current. Useful as stylistic reference for the deliverable.
12. **Step 3.5 conflicts to flag in client work:**
    - **Trapinch-ATOM** release not in static notes — reconcile.
    - **Iron Head / Moonblast** channel-claimed nerfs contradict `season meta changes.txt`. **Static notes win** — these are not nerfed in delta. If a client cites the channel claim, push back with the static note.
