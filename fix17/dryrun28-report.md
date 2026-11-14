# Dry-run #28 — Fix #17 re-trace of the Campus Eats final artifact (v5)

- **Date:** 2026-11-11, evening CST. Worker: dry-run worker (fix #17), check-only.
- **Scope kept:** no plugin file edited, `build.sh` not run, Campus Eats artifact not touched (read-only).
- **Pass/fail target (PARENT-GUIDANCE.md decision 2):** FINAL artifact literal count ±2 = **59–63**, literal rule from fix15/BASELINE.md. The SPEC draft's 30–34 band is superseded and is NOT used.
- **Verdict: PASS.** Recount = **61 literal** (primary reading), inside 59–63. Stricter reading = **60**.

## 0. Source limitation — read this first

The task brief said to read the artifact source at `~/workspace/cold-start-render/campus-eats/` (`index.html` + assets). **That source does not exist in this workspace.** The directory contains only:

- `docs/design-tokens.md` (7,038 bytes, v1-era: frozen system, "nothing on scroll otherwise", one authored moment; records NONE of the v2–v5 elements),
- `.hallmark/log.json` (theme deal record only),
- `.taste-skill/history.json` (moments dealt: `letters-assemble`, `iris-opens`),
- `.taste-skill/layout-history.json`.

There is no `index.html`, no assets directory, no JS/CSS to grep. Consequences, stated plainly rather than papered over:

1. The v5 recount below is **not an independent re-derivation from live HTML**. It is the v4 inventory (54, from fix17/INVENTORY-V4.md) + the v5 delta (7 elements, as named in PARENT-GUIDANCE.md). The v4 inventory itself was built from render history, not live source — same limitation, inherited.
2. The R1/R4 finding (§C) is therefore a finding about **what is recorded**, not a proven fact about the live v5 render: the tokens file that omits iris-opens/hero loop also omits all 36 v2–v5 elements known to be in the render, so absence from that file proves nothing about the live page. What CAN be said: no record of R1/R4 application exists anywhere in the available source, and the v2/v3/v4 delta histories likewise record neither. Verification against the live artifact requires the live artifact, which was not available to this worker.
3. Kind classifications for the v5 delta are judgments from the one-line descriptions in PARENT-GUIDANCE.md, following the v1–v4 precedents in INVENTORY-V4.md. Each judgment call is flagged in §A.

## (A) Recount — final artifact (v5), BASELINE.md literal rule

Counting rule (fix15/BASELINE.md): one discrete, deliberate design application = one count; instances count individually; exactly one kind per element by precedence Moment > Effect > Visual > Diagram > Treatment > Component > Motion > Type. Does NOT count: copy words, sections, the theme itself, a dealt item with no recorded application.

### v4 baseline (from INVENTORY-V4.md, unchanged)

| Kind | v1 | v2 | v3 | v4 |
|---|---|---|---|---|
| Component | 18 | 22 | 27 | **28** |
| Treatment | 2 | 4 | 6 | **6** |
| Visual | 1 | 1 | 1 | **1** |
| Motion | 2 | 2 | 2 | **15** |
| Moment | 1 | 1 | 1 | **1** |
| Type | 1 | 1 | 2 | **2** |
| Effect | 0 | 0 | 0 | **0** |
| Diagram | 0 | 1 | 1 | **1** |
| **Total** | **25** | **32** | **40** | **54** |

### v5 delta — +7 (numbered #60–#66, continuing INVENTORY-V4.md)

| # | Element (per PARENT-GUIDANCE.md) | Kind | Basis / precedent |
|---|---|---|---|
| 60 | Hover sticker-peel corner on the price ladder | Motion | A hover behaviour on the existing price-ladder card; same class as v4 hover micros #47–#50 (photo tilt, name warms, tap-to-pop, wiggle). The peel is a behaviour, not a new surface. |
| 61 | Washi tape strips pinning the ramen photo | Treatment | Handmade mark on one surface; same class as v2 tape tab #35 (Treatment). Now covered by the fix #17 R3 widening, which names washi explicitly. |
| 62 | Pink marker checks that draw in on step cards ×3 — **counted as ONE feature** | Treatment | One draw-in check feature applied across the 3 step cards. Precedent: v3 #44 "Tried it" stamp counted once as one feature on the picks row (INVENTORY-V4.md §3). The mark is the element (Treatment, cf. v3 scribble #39); the draw-in is its behaviour (cf. starburst #32, whose spin is its behaviour, one count). **Sensitivity below: per-instance counting = 3, total 63.** |
| 63 | Five-coin stack filling with the budget stepper | Component | A new discrete UI piece (the stack), whose filling is its behaviour — same class as threshold bar #21 (Component). Not motion-on-an-existing-piece: the stack did not exist before v5. |
| 64 | Perforated Northgate Loop bus-pass ticket under the napkin receipt | Component | A new paper-artifact card — same class as torn napkin receipt #43 (Component). The perforation is detailing of the new card, not a treatment on an existing surface (contrast #37, perforated edge on the existing price ladder = Treatment). R3 widening covers the perforation detail; the card itself is the element. |
| 65 | Tappable five-sticker sheet in the ink band (taco, coffee, star, heart, burger) | Component | One interactive sheet — same class as v4 #59 "Roll a craving" interactive bit (Component). The five stickers are items within the one sheet, not five elements (cf. button pair #2 = one element; spot rows are separate rows, not items in one row). |
| 66 | Drifting confetti stars (ink band) | Motion | An ambient loop; same class as v4 #51 float-card bob (Motion). The stars are new marks, but the element's content is the drift — a loop, not a new functional piece. |

v5 delta by kind: **Component +3, Treatment +2, Motion +2, Moment 0, Type 0, Visual 0, Effect 0, Diagram 0. Total +7.**

### v5 TOTAL — literal (primary) reading

| Kind | v4 | v5 delta | **v5 total** |
|---|---|---|---|
| Component | 28 | +3 | **31** |
| Treatment | 6 | +2 | **8** |
| Visual | 1 | 0 | **1** |
| Motion | 15 | +2 | **17** |
| Moment | 1 | 0 | **1** |
| Type | 2 | 0 | **2** |
| Effect | 0 | 0 | **0** |
| Diagram | 1 | 0 | **1** |
| **Total** | **54** | **+7** | **61** |

**61 is inside the 59–63 target. PASS.**

### Stricter reading (motion layered onto existing pieces is not a new element)

Same rule as INVENTORY-V4.md §5 reading A, which gave v4 = 46 (excluded #51–#58, the eight life-in-pieces ambient loops; kept hover micros #47–#50, scroll entrances #46, Roll a craving #59). Applied identically to v5:

- #60 peel corner: **kept** — a hover micro, same class as #47–#50, which reading A keeps.
- #61 washi, #62 checks, #63 coin stack, #64 ticket, #65 sticker sheet: **kept** — new content/marks/pieces, not motion layered onto an existing piece.
- #66 confetti stars: **excluded** — an ambient loop, same class as #51 float-card bob, which reading A excludes. (Sensitivity: the stars are new marks, so a reader who counts new-mark loops would keep it → stricter 61.)

| Kind | v5 literal | stricter adjustment | **v5 stricter** |
|---|---|---|---|
| Component | 31 | 0 | **31** |
| Treatment | 8 | 0 | **8** |
| Visual | 1 | 0 | **1** |
| Motion | 17 | −1 (#66) | **16** |
| Moment | 1 | 0 | **1** |
| Type | 2 | 0 | **2** |
| Effect | 0 | 0 | **0** |
| Diagram | 1 | 0 | **1** |
| **Total** | **61** | **−1** | **60** |

Stricter v5 = **60** (v4 stricter 46 → +14, i.e. the v5 delta is +7 literal / +6 stricter; the only stricter-vs-literal difference in v5 is the confetti loop).

### Sensitivities (each moves the total; none moves it out of 59–63)

- Marker checks counted per instance (×3, BASELINE.md's "instances count individually" read literally): Treatment 8 → 10, **total 63** — still inside the band (top edge). The primary 61 follows the v3 #44 "one feature" precedent and the parent's own 54 + 7 = 61 arithmetic; the per-instance reading is recorded here, not hidden.
- Confetti kept under the stricter reading (new marks, not layered motion): stricter 60 → 61.
- Per-instance checks + confetti-kept stricter: stricter 62.
- Ticket counted as Treatment (perforation as the application, card as detailing): Component 31 → 30, Treatment 8 → 9, total unchanged at 61.
- Coin stack counted as Motion (a filling animation): Component 31 → 30, Motion 17 → 18, total unchanged at 61.
- Budget-bar scale ticks as a Treatment (rejected in INVENTORY-V4.md §2, same reasoning): +1 → 62 (literal). Not adopted.
- No Effect has been applied at any version (v1–v5).

## (B) Coverage mapping — every element to a rule

Rules checked in the BUILT tree (`~/workspace/hackathon-plugin/hackathon-ecc/skills/`, read-only greps this run): `fix #17` occurs in design-taste-frontend (4), orchestrate (1), ui-ux-pro-max (3), less-flat-ui (2), motion-patterns (3), motion-foundations (3), motion-advanced (1), make-interfaces-feel-better (7), orch-build-mvp (1), polish-pass (1), sticker.md (2). Verified present: M4's named loops in make-interfaces-feel-better ("a card's bob", "a seal's breathe", "a flag's sway", "a heart's beat", "a marquee's pause-on-hover"); M3's named hovers ("warm a name's colour", "lift-and-pop", "wiggle a sticker"); "washi" in less-flat-ui; "Scoped exceptions" in sticker.md. Rule texts confirmed against fix17/fix17.py (U1/T1/F1/E1/M1–M6, STATIC_CHECKS, STICKER_EXCEPTIONS, R3_WIDEN).

Coverage tiers used (standard from INVENTORY-V4.md §6, extended):

- **SPECIFIC** — a rule compels, names, or provides the pattern for the element in the same form.
- **GENERIC (U1/E1)** — the element is an invented page-only element of the class U1 compels (≥3 per build) and E1 pushes; no rule names this specific element. U1 compels three inventions per build, not every invention — so generic coverage is real but weaker than specific. Elements with ONLY generic coverage are flagged `(generic only)`; they are NOT listed as remaining gaps (a rule does cover them), but a future rule could name the pattern specifically.
- **PRE-EXISTING** — covered by a rule that predates fix #15/#17 (theme physics, motion-advanced patterns, a11y practice). Not a fix #17 gap.
- **BASELINE** — v1 elements producible by the original package (page system / theme / ui-ux-pro-max); the back-port gap analysis scoped to the v2–v5 deltas, so these were never gaps.

**Result: 0 elements map to NO rule. 0 remaining back-port gaps by the mapping standard.** 7 elements have generic-only coverage (flagged below); everything else is specific, pre-existing, or baseline.

### v1 — baseline (25), all BASELINE unless noted

| # | Element | Kind | Rule(s) |
|---|---|---|---|
| 1 | news pill | Component | BASELINE (page system); M3 governs its hover state |
| 2 | button pair | Component | BASELINE; M3 (hover/press) |
| 3 | app-frame window | Visual | BASELINE (centred-hero spec); M4 (R4 hero loop lives here — see §C) |
| 4 | search bar (app-frame) | Component | BASELINE (ui-ux-pro-max) |
| 5–7 | spot row ×3 | Component | BASELINE (ui-ux-pro-max) |
| 8–9 | floating card ×2 | Treatment | BASELINE; fix #15 R3 (treatment-kind applications R3 counts) |
| 10 | hero entrance | Motion | M4 SPECIFIC (named: "hero entrance … must actually move") |
| 11 | hover layer (page-wide) | Motion | M3 SPECIFIC (hover layer per interactive element) |
| 12–15 | Bento tile ×4 | Component | BASELINE (Range pattern); T1 governs figure/label fill inside each tile |
| 16–18 | step card ×3 | Component | BASELINE; M3 (hover) |
| 19 | budget stepper | Component | BASELINE; M5 SPECIFIC (the interactive bit's control) |
| 20 | running total (Bowlby figure) | Type | T1 SPECIFIC (figure in a bounded container; 60% fill); F1 (Source cell) |
| 21 | threshold bar | Component | BASELINE |
| 22 | price ladder card | Component | BASELINE; T1 SPECIFIC (price-ladder cell is a named T1 container) |
| 23 | ink-band statement | Moment | BASELINE (dealt moment letters-assemble); M4 (dealt moment must move); F1/T1 govern its type |
| 24 | pink corner tag | Component | BASELINE; T1 (tag label fill) |
| 25 | footer | Component | BASELINE (footer-dark) |

### v2 delta (7)

| # | Element | Kind | Rule(s) |
|---|---|---|---|
| 31 | marquee ticker | Component | **U1/E1 (generic only)** — no marquee-strip pattern rule names the strip. M4 names only its pause-on-hover (#58), not the strip itself. |
| 32 | "Open late" starburst (spinning) | Component | M4 SPECIFIC (spin is authored motion that must move; "a seal's breathe" is the named sibling loop) + U1/E1 (badge invention) |
| 33 | dorm-to-tacos walk-route diagram | Diagram | **R2 (fix #15) SPECIFIC** |
| 34 | "Tonight's picks" card row | Component | **U1/E1 (generic only)** — no picks/recommendation-row pattern rule. |
| 35 | tape tab on app frame | Treatment | **R3 widening (fix #17) SPECIFIC** — "tape … counts as a treatment kind" |
| 36 | "Till 2 AM" tile badge | Component | T1 SPECIFIC (badge label is named T1 container type; fill rule governs it) + U1/E1. Note: badge *placement* on a tile is still only generically covered (the minor gap stands as a placement note, not an element gap). |
| 37 | perforated coupon edge, price ladder | Treatment | **R3 widening SPECIFIC** — "perforation … counts as a treatment kind" |

### v3 delta (8)

| # | Element | Kind | Rule(s) |
|---|---|---|---|
| 38 | Taco Compass seal (rotating) | Component | **Sticker exception A SPECIFIC** ("a drawn seal/emblem (e.g. a Taco Compass) is permitted") + M4 (rotation loop) + U1/E1 |
| 39 | hand-drawn pink scribble underline | Treatment | **Exception A SPECIFIC** ("hand-drawn ink scribble underline … permitted") + **R3 widening SPECIFIC** ("a hand-drawn ink mark counts as a treatment kind") |
| 40 | dotted "hungry shortcut" doodle trail + heart pin trail | Treatment | **Exception A SPECIFIC** ("doodle trail … permitted") + **R3 widening SPECIFIC** |
| 41 | heart pin (trail's end) | Component | **U1/E1 (generic only)** — no pin/marker pattern rule. |
| 42 | fork-flag "You are hungry here" pin | Component | **U1/E1 (generic only)** — no flag-pin pattern rule. |
| 43 | torn napkin receipt | Component | **U1/E1 (generic only)** — no receipt-card pattern rule. |
| 44 | interactive "Tried it" stamp | Component | M5 SPECIFIC (a working interactive bit — stamp as state toggle) + U1/E1 |
| 45 | Bento lead-tile lone figure, 4.9rem | Type | **R5 (fix #15) SPECIFIC** + T1 SPECIFIC (the lone figure is T1's headline case; 60% fill governs it) |

### v4 delta (14)

| # | Element | Kind | Rule(s) |
|---|---|---|---|
| 46 | scroll-triggered sticker entrances, staggered rise-and-settle, 1500ms fail-safe | Motion | **Exception B SPECIFIC** ("scroll rise-and-settle entrances … as sticker motion") + **M2 SPECIFIC** (1500ms fail-safe) + M1 (scope note: M1 itself does NOT apply to Taste landing pages — exception B is the license; M1's text says so explicitly) |
| 47 | photo tilt (hover) | Motion | PRE-EXISTING (sticker.md:74 physics) + M3 SPECIFIC |
| 48 | name warms pink (hover) | Motion | **M3 SPECIFIC** — names "warm a name's colour on a fill" verbatim |
| 49 | lift + tap-to-pop (hover) | Motion | **M3 SPECIFIC** — names "lift-and-pop a card or photograph on tap" verbatim |
| 50 | lift + sticker wiggle (hover) | Motion | **M3 SPECIFIC** — names "wiggle a sticker" verbatim |
| 51 | float-card bob | Motion | **M4 SPECIFIC** — names "a card's bob" verbatim |
| 52 | news-dot pulse | Motion | PRE-EXISTING (motion-advanced PulseDot) + M4 |
| 53 | starburst breathes while spinning | Motion | **M4 SPECIFIC** — names "a seal's breathe" verbatim |
| 54 | compass grows on hover | Motion | PRE-EXISTING (motion-advanced useHoverScale) + M3 |
| 55 | fork-flag sways | Motion | **M4 SPECIFIC** — names "a flag's sway" verbatim |
| 56 | heart beats | Motion | **M4 SPECIFIC** — names "a heart's beat" verbatim |
| 57 | tacos pin pulses | Motion | PRE-EXISTING (motion-advanced pulse indicator) + M4 |
| 58 | marquee pauses on hover | Motion | **M4 SPECIFIC** — names "a marquee's pause-on-hover" verbatim |
| 59 | "Roll a craving" interactive bit + aria-live | Component | **M5 SPECIFIC** (the interactive bit) + U1/E1; aria-live = PRE-EXISTING a11y practice |

### v5 delta (7)

| # | Element | Kind | Rule(s) |
|---|---|---|---|
| 60 | hover sticker-peel corner, price ladder | Motion | M3 SPECIFIC ("each distinct hover behaviour is its own authored motion, recorded in the Motion list") + U1/E1 |
| 61 | washi tape strips pinning ramen photo | Treatment | **R3 widening SPECIFIC** — names "washi" verbatim |
| 62 | pink marker checks draw in on step cards ×3 (one feature) | Treatment | **Exception A SPECIFIC** (hand-drawn ink marks) + **R3 widening SPECIFIC** + M4 (the draw-in must actually move) |
| 63 | five-coin stack filling with budget stepper | Component | M4 SPECIFIC ("count" is a named M4 authored-motion class; the filling stack is a live count/state) + **U1/E1 (generic only for the stack piece itself)** — no coin-stack pattern rule. |
| 64 | perforated Northgate Loop bus-pass ticket | Component | **U1/E1 (generic only for the ticket piece)** + R3 widening SPECIFIC for the perforation detail. No bus-pass/receipt-card pattern rule. |
| 65 | tappable five-sticker sheet, ink band | Component | M5 SPECIFIC (a tappable bit — one control + its feedback) + U1/E1 |
| 66 | drifting confetti stars, ink band | Motion | M4 SPECIFIC (ambient loop on an existing piece/section; the same class as #51 bob, which M4 names) + U1/E1 |

### Coverage summary

- Total elements: **61**. Mapped to ≥1 rule: **61**. Unmapped: **0**. Remaining back-port gaps: **0** by the mapping standard.
- Generic-only (U1/E1, no specific pattern rule): **7** — #31 marquee ticker, #34 picks row, #41 heart pin, #42 fork-flag pin, #43 napkin receipt, #63 coin stack (piece), #64 bus-pass ticket (piece). These are covered as inventions, not as named patterns; if a future fix wants them as named patterns (marquee strip, pin/marker, receipt card, coin stack), that is new pattern work, not a back-port gap — U1/E1 already compel the class.
- Specific fix #17 coverage: R3 widening (#35, #37, #39, #40, #61, #62, #64-detail), exception A (#38, #39, #40, #62), exception B + M2 (#46), M3 (#47–#50, #60), M4 (#51, #53, #55, #56, #58, #62-draw, #63-count, #66), M5 (#44, #59, #65), T1 (#20, #22, #36, #45), U1/E1 (all invented elements). M1 contributes nothing on this landing page by design (Option B; exception B is the license — see §D note). M6 and F1 govern behaviour/recording, not elements: M6 = reduced-motion gating (practice, 0 elements, correctly); F1 = Source cells on every Type row (recording, 0 elements, correctly).
- Fix #15 coverage carried forward: R2 (#33), R5 + T1 (#45), C2 (fonts self-hosted, build step, 0 elements), reduced-motion practice (M6's predecessor), aria-live practice (#59).
- E1 push firing (PARENT-GUIDANCE.md, Anish: "more creative… trailblazing"): at least one genuinely original element per build that a template would not produce — satisfied several times over: #64 bus-pass ticket, #65 five-sticker sheet, #63 coin stack, #38 Taco Compass, #43 napkin receipt. All are template-foreign, theme-matched inventions.

## (C) R1/R4 finding — with evidence

**Finding: R1 (iris-opens) and R4 (hero loop) have NO recorded application in any source available to this worker — and the available source cannot settle whether they are in the live v5 render.**

Evidence (all greps run read-only this session on `~/workspace/cold-start-render/campus-eats/`):

- `docs/design-tokens.md:16` — "Moments dealt: letters-assemble (statement) + **iris-opens (section transition)**." — iris-opens is listed as DEALT, not applied. No application is recorded anywhere in the file.
- `docs/design-tokens.md:63` — Motion: "hero enters once on load; hover lifts …; **one authored moment (letters-assemble on the ink-band statement); nothing on scroll otherwise**". The only applied moment named is letters-assemble.
- `.taste-skill/history.json` — moments recorded: `letters-assemble`, `iris-opens` (both with the same timestamp/seed) — a DEAL record, not an application record.
- Grep for `loop` across the whole artifact directory: **zero hits**. No "hero loop", no loop of any kind is mentioned anywhere.
- Grep for `fail-safe` / `1500`: **zero hits** (consistent with the tokens file being v1-era; the fail-safe is a v4 feature, also unrecorded there).
- fix15/BASELINE.md "Baseline gaps" already recorded both as unapplied at v1: "iris-opens: second dealt moment, no recorded application anywhere. Hero window loop: the centred-hero spec's loop inside the window, no recorded application anywhere." INVENTORY-V4.md §2/§6 recorded the same absence through v4 ("no record of application in the v2/v3/v4 delta lists").

What this does and does not establish:

- It DOES establish: the fix #15 rules R1 and R4 are **not evidenced in the artifact's own record** at any version v1–v5, and no v2–v5 delta history mentions either. The rules exist and compel both elements; the record shows neither firing. This is a rule-effectiveness finding, as PARENT-GUIDANCE.md decision 3 requires it to be surfaced — it is surfaced here, not hidden, and the count in §A was NOT adjusted for it (61 stands as counted).
- It does NOT establish that the live v5 render lacks them: the only tokens file available is frozen at v1 and omits all 36 v2–v5 elements that are known to be in the render (marquee, compass, scroll entrances, sticker sheet, …), so its silence on R1/R4 is equally consistent with "never applied" and with "applied but never recorded". **Definitive verification needs the live artifact source (index.html/assets), which was not present in this workspace.** The parent should treat R1/R4 compliance as UNVERIFIED (not failed), pending a grep of the live v5 source — or, if the live render is checked and both are absent, as a genuine compliance failure of the render against fix #15 rules R1/R4 (a render-process finding, not a rule gap: the rules compel them already).
- Note for the record: R5 IS satisfied (late, v3 #45, the lone figure) — the only one of the three fix #15 re-trace elements whose application is recorded.

## (D) Rebuild simulation — INFORMATIONAL ONLY, not pass/fail

Starting state: fix #15 after-state (dry-run #25) = **30 elements** (Component 18, Treatment 3, Visual 1, Motion 3, Moment 2, Type 2, Effect 0, Diagram 1). Question: what would the fix #17 rules compel in a FRESH Campus Eats rebuild from that state?

| Rule | Δ elements | Kind(s) | Reasoning |
|---|---|---|---|
| U1 — ≥3 unique page-only elements | **+3** | Inventor's choice (illustrative split below: Component +2, Type +1) | The only fix #17 rule that compels NEW elements by count. Kinds are not predetermined — the dry-run invents its own. Illustrative kinds per SPEC-DRAFT §C (die-cut price-tag tab, sticker-peel corner, lime stamp-chip) would land Component/Type; any split summing to 3 is consistent with the rule. |
| T1 — type fills its bubble | 0 | — | Sizing rule over existing type (#20, #45, labels). No new element. |
| F1 — font decisions cite type system | 0 | — | Recording rule (Source cells). No new element. |
| M1 — scroll entrances | 0 (compelled) | — | Option B (SPEC-DRAFT §A, kept by fix17.py): Taste landing pages keep the scroll ban; M1 applies to motion-governed app surfaces only. The Campus Eats landing page has no such scrolled surface; the app-frame has no scroll. |
| M2 — 1500ms fail-safe | 0 | — | Mechanism inside entrances, not an element. |
| M3 — hover micros | 0 | — | Behaviour/verification over already-counted elements (hover layer #11 is in the 30). Distinct hover behaviours beyond the layer are inventions (counted under U1), not M3-compelled. |
| M4 — life in existing pieces | 0 | — | Verification rule: each already-counted piece (hero entrance, R4 loop, dealt moment, count, diagram pulse) must move. The R4 hero loop and iris-opens moment are already in the 30 (Motion 3, Moment 2). |
| M5 — interactive bit | 0 | — | The bit is the budget stepper + live total, already counted (#19 Component, #20 Type). Dry-run #25 confirmed; nothing new. |
| M6 — reduced motion | 0 | — | Gating/practice, not an element. |
| E1 — creative push | 0 | — | Permission + bounds + active push; the elements it pushes are counted under U1. |
| Sticker exceptions A/B | 0 (compelled) | — | Permissions, not compulsion. Exception A permits hand-drawn ink marks; exception B permits scroll entrances as sticker motion. |
| **Simulation total (compelled)** | **+3 → 33** | **C20, T3, V1, Mtn3, Mom2, Ty3, E0, D1** (with the U1 kind split illustrative) | Matches the SPEC-DRAFT §C prediction of 33 exactly. |

Two honest notes on the simulation (informational, not pass/fail):

1. **The +1 that is permitted but not compelled:** exception B + E1's push make a scroll-entrance system (the v4 #46, +1 Motion) the expected design-lead choice on a Sticker rebuild — the actual v4 render did exactly this. If the lead takes it, the fresh rebuild lands at **34** (Motion 3 → 4). The compelled floor is 33; 34 is the realistic rebuild. Neither number is the pass/fail target — §A's 61 is.
2. **The simulation exposes the structural point of fix #17:** the rules compel only +3 (U1) over the fix #15 after-state, while the final artifact is 61. The other +28 elements (v2–v4 inventions, v4 motion density, v5's 7) are not compelled element-by-element by any rule — they are produced by the COMBINATION of U1's minimum (≥3), E1's active trailblazing push, M3/M4's density requirements (every interactive element hovers; every authored piece moves), and the R3 widening + exceptions that license the handmade material. A rebuild under these rules should land well above 33 in practice (the v4 render's +14 was 13 Motion, i.e. M3/M4 density firing through invention), but the rules as written guarantee only the 33 floor. If the parent wants a higher guaranteed floor, that is a U1-minimum or M-density decision for a future fix — not a finding against this one, whose target (§A) was the re-trace, which PASSED.

## Files / evidence used (read-only)

- `~/workspace/hackathon-plugin/fix17/PARENT-GUIDANCE.md` (target 59–63; v5 delta list; exception decisions)
- `~/workspace/hackathon-plugin/fix17/INVENTORY-V4.md` (v4 inventory 54; stricter reading 46; §6 coverage)
- `~/workspace/hackathon-plugin/fix15/BASELINE.md` (counting rule)
- `~/workspace/hackathon-plugin/fix17/SPEC-DRAFT.md` (§C prediction 33 — superseded band, used only for §D)
- `~/workspace/hackathon-plugin/fix17/SKILL-MAP.md` (placement anchors, pre-fix16 — used as background only)
- `~/workspace/hackathon-plugin/fix17/fix17.py` (implemented rule texts: U1/T1/F1/E1/M1–M6, exceptions A/B, R3 widening; M1 Option B)
- Built tree greps: `fix #17` counts per skill file; M3/M4 verbatim phrases in make-interfaces-feel-better; "washi" in less-flat-ui; "Scoped exceptions" in sticker.md
- Artifact (read-only): `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md`, `.hallmark/log.json`, `.taste-skill/history.json` — **no index.html or assets exist in this workspace** (see §0)
