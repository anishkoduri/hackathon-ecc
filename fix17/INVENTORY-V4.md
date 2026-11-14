# INVENTORY — Campus Eats cold-start render at v4 (fix program #17, worker 1)

- **Date:** 2026-11-11 (analysis only — no plugin file edited, `build.sh` not run,
  the Campus Eats artifact not touched or inventoried; its v5 edit is running
  separately and is NOT included here).
- **Counting rule:** `~/workspace/hackathon-plugin/fix15/BASELINE.md` — one discrete,
  deliberate design application = one count; instances count individually
  (3 spot rows = 3; 4 Bento tiles = 4); each element classified into exactly ONE
  kind by precedence **Moment > Effect > Visual > Diagram > Treatment >
  Component > Motion > Type**. What does NOT count: copy words, sections as such,
  the theme itself, a dealt item with no recorded application.
- **Sources read (read-only):** `fix15/BASELINE.md`, `fix15/dryrun25-report.md`,
  `fix15/SPEC.md` (rules R1–R5 / C1–C3 / D1), the built tree's
  `skills/less-flat-ui/SKILL.md` (the 23-treatment catalogue),
  `skills/design-taste-frontend/references/hallmark/references/themes/sticker.md`
  (the dealt Sticker theme), `skills/motion-patterns/SKILL.md`,
  `skills/motion-advanced/SKILL.md`, `skills/motion-foundations/SKILL.md`.
  The v2/v3/v4 deltas are taken from the render history in the task brief, not
  from the live artifact.
- **Treatment boundary applied:** the counting rule defines Treatment as "a
  less-flat-ui treatment application on ONE surface". The 23 catalogue
  treatments are: Felt, Fluted glass, Thermal gradients, Water ripples,
  Speckled graphite, Single-hue landscapes, Blueprint grids, Halftone, Grainy
  gradients, Grass texture, Dithered images, Paper texture, Contour lines,
  Cloud sky, Pixel mosaics, Lens distortion, Stippled gradients, Square-dot
  grids, Blurred photos, Iridescent shapes, Impressionist paintings, ASCII and
  pixels, Soft shadow. Handmade surface marks (tape, perforation, scribble,
  doodle trail) are NOT among the 23; they are classified Treatment in spirit
  (a mark applied to one surface) and flagged as gaps in §6 because no catalogue
  entry or rule produces them.

## 1. v1 list — baseline, 25 elements (copied from fix15/BASELINE.md)

Hero:
1. news pill — Component
2. button pair (primary + ghost) — Component
3. app-frame window — Visual
4. search bar (inside app-frame) — Component
5. spot row 1 (tacos) — Component
6. spot row 2 (burger) — Component
7. spot row 3 (coffee) — Component
8. floating card 1 — Treatment (Soft Shadow)
9. floating card 2 — Treatment (Soft Shadow)
10. hero entrance — Motion
11. hover layer (page-wide) — Motion

Bento (4 tiles):
12–15. tile x4 — Component

Steps (3 cards):
16–18. step card x3 — Component

Lime field:
19. budget stepper — Component
20. running total (Bowlby figure) — Type
21. threshold bar — Component
22. price ladder card — Component

Ink band:
23. ink-band statement — Moment (letters-assemble)
24. pink corner tag — Component

Footer:
25. footer (footer-dark) — Component

v1 by kind: Component 18, Treatment 2, Visual 1, Motion 2, Moment 1, Type 1,
Effect 0, Diagram 0. **Total 25.**

## 2. v2 delta — +7, total 32

| # | Element | Kind | Coverage (§6) |
|---|---|---|---|
| 31 | marquee ticker | Component | GAP |
| 32 | "Open late" starburst (spinning is its behaviour; one application) | Component | GAP |
| 33 | dorm-to-tacos walk-route diagram | Diagram | COVERED (R2) |
| 34 | "Tonight's picks" card row (counted as one row-unit; see note) | Component | GAP |
| 35 | tape tab on app frame | Treatment | GAP |
| 36 | "Till 2 AM" tile badge | Component | GAP (minor) |
| 37 | perforated coupon edge on the price ladder | Treatment | GAP |

v2 by kind: Component 22 (+4), Treatment 4 (+2), Visual 1, Motion 2, Moment 1,
Type 1, Effect 0, Diagram 1 (+1). **Total 32.**

Reconciliation note — the brief lists 8 prose items for v2 but states +7.
The 8th item resolves as follows: **"Bento sublines" are copy words and do not
count** (BASELINE.md exclusion); the "Till 2 AM" tile badge in the same item
counts once (#36). **"Budget-bar scale ticks" are NOT counted**: they are
detailing of the existing threshold bar (#21), not a discrete new application —
the same class as sublines on an existing tile. Alternative reading: count the
ticks as a Treatment on the bar surface → v2 would be 33 (Treatment 5).
The two readings differ by exactly this one judgment call.

Also recorded for v2: fonts self-hosted as bundled woff2 — a build step, not an
element; COVERED by fix #15 C2.

Open compliance question (not a gap, a missing record): the fix #15 re-trace
compelled three further elements — **iris-opens (R1), the centred-hero loop
(R4), the Bento lead-tile lone figure (R5)** — and NONE of the three appears in
the v2 delta list. Either they were not applied in the artifact v2 edit, or
the history omits them. R1/R4/R5 compliance in the artifact is therefore
unverified from the given history. (The lone figure reappears as a v3 element,
#45 below, counted there instead.)

## 3. v3 delta — +8, total 40

| # | Element | Kind | Coverage (§6) |
|---|---|---|---|
| 38 | rotating Taco Compass seal (rotation is behaviour; one application) | Component | GAP (+ theme-fit question) |
| 39 | hand-drawn pink scribble underline | Treatment | GAP + THEME CLASH |
| 40 | dotted "hungry shortcut" doodle trail with heart pin — the trail | Treatment | GAP + THEME CLASH |
| 41 | heart pin (at the trail's end) | Component | GAP |
| 42 | fork-flag "You are hungry here" pin | Component | GAP |
| 43 | torn napkin receipt ("Tonight on $8") | Component | GAP |
| 44 | interactive "Tried it" stamp on pick cards (counted once as one feature; see note) | Component | GAP |
| 45 | Bento lead-tile lone figure, set at 4.9rem | Type | COVERED (R5, arriving late) |

v3 by kind: Component 27 (+5), Treatment 6 (+2), Visual 1, Motion 2, Moment 1,
Type 2 (+1), Effect 0, Diagram 1. **Total 40.**

Notes:
- The "Tried it" stamp is counted once (one interactive feature on the picks
  row). Per-card instance counting would add +2 more if the picks row holds
  3 cards (card count not stated in the history); see Sensitivity (§5).
- The v3 type scale-up ("type scaled up to fill bubble/card space: hero
  3–5.4rem, Bento figures 4.9rem, budget total 4.2rem") adds **0 new elements**
  beyond #45: the hero headline is a heading (excluded from Type), the budget
  total is already counted (#20), and the non-lead Bento figures are large
  numerals inside their tiles, not separate type moments (the Sticker theme
  allows one lone figure a screen, `sticker.md:46`). The "size type to fill
  its container" posture itself has no compelling rule — minor gap in §6.
- Theme clashes (#39, #40): `sticker.md:85` — "Never a drawn sticker, mascot
  or doodle". A hand-drawn scribble underline and a doodle trail are drawn
  doodles by name. Under fix #15 rule A (theme-match is a precondition, a
  clashing element is not applied), these two should not have been applied to
  this build. The compass seal (#38) carries the same question in milder form
  (a drawn emblem vs `:85`); pins (#41, #42) are functional markers, not
  doodles, so no clash is claimed for them.

## 4. v4 delta — +14, total 54

| # | Element | Kind | Coverage (§6) |
|---|---|---|---|
| 46 | scroll-triggered sticker entrances, staggered rise-and-settle, 1500ms fail-safe (one entrance system; the fail-safe is a detail of it) | Motion | GAP (reconciliation — form exists, theme forbids) |
| 47 | photo tilt (hover) | Motion | COVERED (sticker.md:74) |
| 48 | name warms pink (hover) | Motion | GAP |
| 49 | lift + tap-to-pop (hover) | Motion | GAP |
| 50 | lift + sticker wiggle (hover) | Motion | GAP |
| 51 | float-card bob (one loop pattern across the two float cards) | Motion | GAP |
| 52 | news-dot pulse | Motion | COVERED (motion-advanced PulseDot) |
| 53 | starburst breathes while spinning | Motion | GAP |
| 54 | compass grows on hover | Motion | COVERED (motion-advanced useHoverScale) |
| 55 | fork-flag sways | Motion | GAP |
| 56 | heart beats | Motion | GAP |
| 57 | tacos pin pulses | Motion | COVERED (motion-advanced pulse indicator) |
| 58 | marquee pauses on hover | Motion | GAP |
| 59 | "Roll a craving" interactive bit, with aria-live announcement | Component | GAP (bit unruled; aria-live practice covered) |

v4 by kind: Component 28 (+1), Treatment 6, Visual 1, Motion 15 (+13),
Moment 1, Type 2, Effect 0, Diagram 1. **Total 54.**

Reduced-motion respected in CSS and JS adds **0 elements** (it is a constraint
honoured, not an application); the practice is COVERED by
`motion-foundations` (`prefers-reduced-motion`, `:150/:172/:180/:196`).

Flag — brief label vs measured count: the brief labels v4 "motion +10-15%".
Measured rule-literally, v4 is **+14 on 40 = +35%** (13 of it Motion).
The +10-15% band (+4 to +6) is reachable only by NOT counting motion layered
onto existing pieces as new elements; see the alternative readings in §5.
The primary count follows BASELINE.md literally: "one discrete, deliberate
design application", Motion expressly includes "other authored motion element",
and the baseline itself counts motion applied to existing pieces (hero entrance
#10 is motion on the hero; the fix #15 R4 hero loop is motion inside the
existing app-frame window). Each v4 motion behaviour is a distinct authored
application on a distinct piece, so each counts once.

## 5. v4 TOTAL and count by kind

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

Growth: v1 → v4 is +29 (+116%); v3 → v4 is +14 (+35%); v2 → v3 is +8 (+25%);
v1 → v2 is +7 (+28%). No Effect has been applied at any version.

Sensitivity — stated assumptions that move the total, each with its size:
- Scale ticks counted as a Treatment (v2): +1 → 55 (Treatment 7).
- "Tonight's picks" row counted per card (3 cards assumed): +2 → 56/57.
- "Tried it" stamp counted per pick card (3 assumed): +2 → 56/58.
- Float-card bob counted per card (2 cards): +1 → 55.
- Hero headline at 5.4rem counted as a Type moment ("statement set large"):
  +1 → 55 (Type 3) — rejected in the primary count because it is the page
  heading, and Type is defined as BEYOND a section heading.
- Alternative reading A (life-in-pieces motion §4 #51–#58 not counted as new
  elements, only hover micros + scroll entrances + Roll a craving): v4 = 46
  (+6, +15% — the top of the brief's band).
- Alternative reading B (only genuinely new motion systems count: scroll
  entrances + Roll a craving): v4 = 42 (+2, +5%).

## 6. Coverage — covered by an existing rule, or BACK-PORT GAP

Standard applied: COVERED means an existing package rule compels the element,
names it, or provides the pattern that produces it in the same form — "there
is a motion skill" does not cover a specific motion. GAP means a new rule (or
a widened rule / a catalogue entry / a theme decision) is needed before a fresh
build under the package would produce this element.

### Covered (7 element-applications + 2 practices)

- #33 walk-route diagram — **R2** (fix #15: one diagram by default on software
  pages; form is the implementer's choice among the table's presets). Note:
  a walk-route / route-map form is not a named preset (hub, lanes, pulses) —
  worth naming as a preset when R2 is next touched, but not a gap on its own.
- #45 Bento lead-tile lone figure — **R5** (Range lead element is its own type
  moment; source `sticker.md:61` "the lead tile carries the lone figure").
  Arrived in v3, not v2 — see the §2 open question.
- #47 photo tilt — **Sticker theme physics**, `sticker.md:74`: "a hover lifts
  a clickable raised surface 2px and turns it a degree".
- #52 news-dot pulse — **motion-advanced PulseDot / pulse-indicator pattern**
  (`SKILL.md:24,469`).
- #54 compass grows on hover — **motion-advanced `useHoverScale`**
  (`SKILL.md:34`).
- #57 tacos pin pulses — **motion-advanced pulse-indicator pattern**
  (same as #52, applied to a map pin rather than a dot).
- Fonts self-hosted as bundled woff2 (v2 build step, not an element) — **C2**.
- Reduced-motion respected (v4 practice, not an element) — **motion-foundations**
  `prefers-reduced-motion` (`:150/:172/:180/:196`).
- aria-live announcement on "Roll a craving" (v4 practice) — the live-region
  practice exists in the package (`accessibility/SKILL.md`,
  `frontend-a11y/SKILL.md` carry `aria-live`); the bit itself is a gap below.

### BACK-PORT GAPS — the core deliverable (23 + 1 minor)

**v2 (6):**
1. Marquee ticker → needs a marquee/ticker-strip pattern rule (Taste page
   system or motion-patterns), theme-matched, including its scroll behaviour.
2. "Open late" starburst (spinning badge) → needs a starburst/badge-seal
   pattern (Sticker theme or ui-ux-pro-max) plus a continuous-spin rule; no
   rule produces a starburst or licenses continuous spinning.
3. "Tonight's picks" card row → needs a picks/recommendation-row section
   pattern (a card row beyond Bento / steps / spot rows).
4. Tape tab on app frame → needs tape as a treatment (new catalogue entry in
   less-flat-ui) OR R3 widened so a theme-matched handmade surface treatment
   counts as a treatment kind. As written, R3 counts catalogue kinds only,
   so a tape tab does not satisfy R3's second-kind requirement.
5. "Till 2 AM" tile badge → needs a badge/chip slot on Bento tiles. Minor:
   the chip form itself is theme-defined (`sticker.md:68` "Chips are pills
   with a 2px inset rule"); only the placement on a tile is unruled.
6. Perforated coupon edge → needs perforation as a treatment (new catalogue
   entry) or the same R3 widening as #4.

**v3 (7 + 1 minor):**
7. Taco Compass seal (rotating) → needs a rotating seal/compass-badge
   pattern; plus a theme-fit call — a drawn emblem against `sticker.md:85`
   ("Never a drawn sticker, mascot or doodle").
8. Hand-drawn pink scribble underline → needs a hand-drawn-mark rule — AND
   **clashes with `sticker.md:85`** (a drawn doodle, by name). Rule A
   (theme-match is a precondition) would have blocked it. Coordinator call:
   amend the theme's do-not, or drop the element; a back-port rule cannot be
   written until that call is made.
9. Dotted "hungry shortcut" doodle trail → same as #8 (named "doodle",
   same `:85` clash, same call needed).
10. Heart pin → needs a pin/marker component rule (map-style pins as page
    elements).
11. Fork-flag pin → needs a flag-pin marker rule (same family as #10; may
    fold into one pin/marker rule).
12. Torn napkin receipt → needs a receipt-card pattern (paper-artifact card;
    theme-fit is fine — a real paper object, not a drawn doodle).
13. Interactive "Tried it" stamp → needs an interactive stamp pattern for
    cards (stamp as a state toggle; theme-fit is fine — a print-shop artifact).
- Minor: "size type to fill its container" posture (v3 scale-up) → needs a
  fill-sizing rule, e.g. "size display figures to fill their tile/bubble up
  to the theme's cap". C3 verifies scale/weight steps only; the Sticker theme
  permits a lone figure up to 12rem (`sticker.md:46`) but never requires
  filling. No element count rides on this — it governs sizing of #20/#45.

**v4 (10):**
14. Scroll-triggered sticker entrances + 1500ms fail-safe → needs a
    scroll-reveal fail-safe rule (no rule names a fail-safe timeout) AND
    reconciliation with `sticker.md:74` ("nothing on scroll"): the form is
    covered by motion-patterns scroll-reveal + stagger (`whileInView`,
    stagger list; motion-advanced `useScrollReveal`), but the dealt theme
    forbids scroll motion. Coordinator call: amend the theme or drop scroll
    entrances on Sticker builds.
15. Name warms pink (hover) → needs a hover colour-warm rule for names/text.
    Link hover is underline-only (`sticker.md:69`); pink text on the paper
    ground is a do-not (`sticker.md:84`) — scope the rule to names on fills
    if it is written.
16. Lift + tap-to-pop → needs a card/photo tap-pop pattern. The lift half is
    covered (theme physics `:74` + motion-patterns button hover-pop
    `scale.pop`); the tap-to-pop half is unruled and inverts the theme's
    press physics (a press "pushes it onto its shadow", `:74`; the button
    pattern's `whileTap` is `scale.press`).
17. Lift + sticker wiggle → needs a wiggle pattern (lift half covered, `:74`;
    the wiggle itself is unruled).
18. Float-card bob → needs an ambient bob / card-loop pattern. R4's hero loop
    is hero-scoped; no rule gives cards a continuous loop.
19. Starburst breathes while spinning → needs a breathe pattern (and the spin
    itself, from #2, is still unruled).
20. Fork-flag sways → needs a sway pattern.
21. Heart beats → needs a beat pattern (a beat is a double-thump, distinct
    from the covered pulse in #52/#57).
22. Marquee pauses on hover → needs a pause-on-hover rule for marquees
    (follows from gap #1; listed separately because it is a behaviour rule,
    not the strip itself).
23. "Roll a craving" interactive bit → needs a randomizer/roller-bit pattern
    (a control that surfaces a random suggestion). The aria-live announcement
    is covered practice (see above); only the bit is a gap.

### Open compliance questions (not gaps — missing records)

- **R1 iris-opens** and **R4 hero loop**: no record of application in the
  v2/v3/v4 delta lists. If they are absent from the artifact, that is an
  R1/R4 compliance failure in the artifact, not a rule gap — the rules exist
  and compel them. Verify against the artifact (outside this worker's scope)
  before fix17 writes any new rule for them.
- **R5** is satisfied late (v3, #45) rather than in v2; no action needed if
  the artifact now carries it.

### Gap count summary

- Covered elements: 6 of 34 new applications (#33, #45, #47, #52, #54, #57)
  + 3 covered practices (C2 self-host, reduced-motion, aria-live).
- Back-port gaps: **23** (v2: 6, v3: 7, v4: 10) + 1 minor (fill-sizing).
- Theme clashes needing a coordinator call before any rule is written:
  scribble underline (#8 / #39), doodle trail (#9 / #40), scroll entrances
  (#14 / #46); theme-fit questions: compass seal (#7), name warms pink (#15),
  tap-to-pop (#16).

## 7. v5 — NOT included

**v5 (+15-20% more elements) is running separately and is NOT inventoried
here.** This file covers v1–v4 only (total 54 at v4). v5 must be inventoried
later, as a delta on top of this v4 baseline, once its edit lands — do not
fold v5 elements into the counts above.
