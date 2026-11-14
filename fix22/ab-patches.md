# Fix #22 — Groups A + B patch spec (implementation agent: Groups A+B)

Scope: Group A (20 UX & animation principles, A1–A20) + Group B (20 beautiful-AI-animation
techniques, B1–B20) + fix #22 H1 (colour accents, ACCENT_F22) + fix #22 H2 (accentuation
accents, ACCENTUATION_F22) — ui-ux-pro-max and orchestrate portions of H1/H2 only. The
polish-pass portions of H1/H2 belong to the Groups C+D agent and are NOT in this file.

## How the integrator applies this file

- Target paths are paths inside the BUILT tree (`hackathon-ecc/skills/...`), i.e. the
  post-build file content. Every anchor below was verified to occur EXACTLY ONCE in its
  target file in the post-fix16 built tree (count==1, checked 2026-11-12). Apply in the
  fix17 style: assert the anchor count is 1, fail the build loudly on mismatch, never
  guess. Insert AFTER the anchor unless the entry says BEFORE.
- Do NOT edit `hackathon-ecc/` directly. Do NOT edit `build.sh` by hand for these —
  add a fix22 patch block to `build.sh` that performs these substitutions at build time
  (same mechanism as the fix17 block). Do NOT run `bash build.sh` as part of applying
  (the integrator rebuilds once). Do NOT run `fix11/fix11-stage.py`.
- The orchestrate edit (step 3, design-package brief) is ALREADY APPLIED directly to the
  staged source `new-skills/orchestrate/SKILL.md` line 62 — it is NOT a patch entry here.
  It flows through the STEP 2 copy at build time; verify it survives the rebuild.
- Anchor tokens for cross-reference by other groups: PRINCIPLES_F22 (AB-01),
  LAWS_F22 (AB-02), ANIM_TOKENS_F22 (AB-03), ANIM_RULES_F22 (AB-04, AB-05, AB-06, AB-07,
  AB-08), ANIM_ADV_F22 (AB-09, AB-10), ACCENT_F22 (AB-13), ACCENTUATION_F22 (AB-14).
- Every new rule below carries its fix #19 D19 six-dimension reason (Motion / Theme /
  Texture / Visuals / Techniques / Colors — each a reason or explicit `none — <reason>`)
  and the theme-match precondition explicitly. Layout-only reasoning fails.
- Banned terms: none of the inserted text contains the banned terms (checked).

## Token conflicts / observations (SPEC §4c — recorded, NOT silently resolved)

1. **B3 (30ms row stagger) vs motion-patterns Rule 5 (stagger interval 0.05–0.10s).**
   The 30ms value (AB-03, `duration.staggerRow: 0.03`) sits BELOW Rule 5's 0.05s floor
   ("Below feels mechanical"). Rule 5 is NOT changed by this patch. Note the plugin
   already holds this tension: ui-ux-pro-max `references/quick-reference.md`
   `stagger-sequence` says 30–50ms per item, which also sits below Rule 5's floor.
   Parent adjudicates: narrow Rule 5's floor for list-row entrances, or scope the 30ms
   value to rows only. Until adjudicated, the token is placed as specified and Rule 5
   still governs general stagger intervals.
2. **B15 (exits 20% shorter, exit = 0.8 x enter) vs quick-reference `exit-faster-than-enter`
   (~60–70% of enter).** The B15 value (AB-03, `exitFactor: 0.8`) conflicts numerically
   with the quick-reference rule. Quick-reference is NOT changed by this patch. Parent
   adjudicates which ratio governs. Until adjudicated, the B15 value is placed as
   specified in the motion token/rule layer.
3. **B4 (press scale 0.97) vs motion-foundations `scale.press: 0.95` — OBSERVATION.**
   B4 is already covered by the polish default (0.97, range 0.95–0.98) and no new text
   is added for it. But the motion token `scale.press` is 0.95 — the BOTTOM of that
   range, not the 0.97 default — so the motion-* press scale and the polish press
   default differ for the same concept in different layers. Neither value is changed
   by this patch. Parent adjudicates whether to align `scale.press` to 0.97 or keep
   layer-specific values.
4. **B16 (overlap old & new states) vs motion-patterns Rule 3 (`mode="wait"` on page
   transitions).** No conflict once scoped: B16 (AB-05 rule 16, AB-09 rule 9, AB-10
   example) applies to in-container content swaps, where the incoming state starts
   before the outgoing finishes so the screen never blanks. Rule 3 still governs page
   transitions (enter must not start until exit completes). The scope boundary is
   stated in the rule text itself.

## AB-01 — motion-foundations, Principles A1–A12 (PRINCIPLES_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, `## Principles` section.
- **Anchor (count==1, insert AFTER):**
  ```
  Responsiveness always outranks smoothness. A 60 fps animation that causes
  input delay is worse than no animation.
  ```
- **Insert (full text):**

```md

**Animation principles (fix #22, PRINCIPLES_F22).** The twelve principles below govern
every motion decision in this skill. Each line states what the principle is and how it
shows up in UI. A build names which principles it leans on in the decision record
(orchestrate step 3, design-package brief) — a motion decision with no named principle
is an ungrounded decision.

- **A1 Squash & stretch** — a moving object deforms slightly along its direction of
  travel (squashes on impact, stretches while moving) so it reads as physical, not
  rigid. In UI: a pressed button or a landing card squashes a few percent on press and
  eases back, instead of scaling uniformly.
- **A2 Anticipation wind-up** — a small move in the opposite direction before the main
  move, so the main move reads as intentional. In UI: a knob stretches before it
  slides (B5), a sheet pulls back slightly before it dismisses, a control winds up
  before it springs (see also B19 rubber band).
- **A3 Staging the focus** — only one thing moves, changes, or demands attention at a
  time, so the eye knows where to look. In UI: when a modal opens, the page behind it
  stills; when a toast arrives, nothing else animates with it.
- **A4 Pose to pose** — motion travels between clear, readable states (poses), never
  through an unreadable in-between. In UI: a card has a defined collapsed pose and a
  defined expanded pose; the transition interpolates between them, and both poses are
  legible at rest.
- **A5 Follow through** — parts of an object keep moving briefly after the main body
  stops, then settle. In UI: a list's trailing rows settle a beat after the leading
  row; a sheet's content settles after the sheet lands.
- **A6 Slow in & slow out** — motion eases at both ends (slow start, slow stop) instead
  of starting and stopping abruptly. In UI: entrances ease out (B1) and moves ease
  in-out (B9); nothing starts at full speed or halts dead.
- **A7 Moving in arcs** — objects travel along curved paths, not straight lines, so
  motion reads as natural. In UI: a dragged card, a flying element, or a moving knob
  follows an arc (B7 is this principle applied — the primary home is motion-patterns).
- **A8 Secondary action** — a smaller motion supports the main motion without
  competing with it. In UI: as a row enters, its details settle in after it (B6 is
  this principle applied); as a button is pressed, its icon shifts a touch.
- **A9 Snappy timing** — timing is the principle: motion is quick enough to feel
  responsive, never so slow it feels like waiting. In UI: feedback lands in the
  150–250ms band (B2); a transition that drags past its token duration is a defect,
  not a style.
- **A10 Exaggerated feedback** — feedback is big enough to be unmistakable, then
  settles. In UI: a success pulse (B8) overshoots slightly so the confirmation cannot
  be missed; a destructive action's feedback is visibly stronger than a neutral one.
  (One family with B8 and D20 animate-useful-feedback; D20 points here.)
- **A11 Solid drawing in 3D** — an object keeps believable volume, weight, and depth
  while it moves. In UI: a card that flips or expands keeps its shadow, edge, and
  layering consistent through the move; it never flattens into a texture or shears.
- **A12 Overall appeal** — the motion as a whole is pleasing and on-character for the
  build, not merely correct per rule. In UI: the sum of the build's motion reads as
  one personality (the dealt theme's motion voice), judged at the finish review.

Theme-match precondition: these principles are a decision vocabulary, not a look —
every element animated under them must still match the dealt theme (its material,
tokens, palette balance, and do-nots); a principle applied in a way that clashes with
the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with
the element.

D19 (for the principles set as a whole) — Motion: the principles decide what moves,
how it moves, and how fast, so motion serves attention and state; Theme: each
principle is applied in the dealt theme's motion voice, never as a generic stock move;
Texture: none — the principles govern motion, not surface treatment; Visuals: staging,
arcs, and appeal keep the moving picture legible and on-character; Techniques: the
principles route to the motion-* token and pattern implementations, never to ad-hoc
values; Colors: none — the principles do not choose colours.
```

## AB-02 — motion-foundations, UX laws A13–A20 (LAWS_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, `## Decision Guidance` section.
- **Anchor (count==1, insert BEFORE):**
  ```
  ## Core Concepts
  ```
- **Insert (full text):**

```md
### UX laws that decide motion (fix #22, LAWS_F22)

Each law below is a decision rule with its one-line consequence for design decisions.
The laws live here and nowhere else — `ui-ux-pro-max` points at them (AB-12) and never
restates them; `make-interfaces-feel-better` routes feel decisions through them (AB-11).

- **A13 Fitts's law** — the time to reach a target depends on its size and distance:
  big, near targets are fast; small, far targets are slow. Consequence: put the most
  frequent actions on the biggest, nearest targets, and never make a primary action
  small or far away. D19 — Motion: target size and distance set how fast a reach
  feels; Theme: the law applies inside the dealt theme, it does not restyle it;
  Texture: none — the law is about reach, not surface; Visuals: bigger, nearer
  targets read as more important; Techniques: implement via the hit-area rule and
  placement, never via decoration; Colors: none — the law does not choose colours.
- **A14 Bigger hit areas** — NAMED here as Fitts's law (A13) with its rationale; the
  size rule itself already exists and is NOT duplicated: interactive controls keep at
  least a 44x44px hit area (the plugin floor — `make-interfaces-feel-better` Hit Areas
  section), expanding with a pseudo-element when the visible icon is smaller, without
  letting expanded areas overlap. Consequence: a control that cannot be hit reliably
  cannot be used quickly, whatever its motion does. D19 — Motion: the hit area is what
  the pointer actually reaches, so it bounds every motion decision on the control;
  Theme: none — size is a usability floor, not a theme choice; Texture: none — the
  area is invisible, not a treatment; Visuals: the visible control stays the theme's
  size while the hit area grows beneath it; Techniques: pseudo-element expansion, never
  a visible size change; Colors: none — the law does not choose colours.
- **A15 Hick's law** — decision time grows with the number and complexity of choices.
  Consequence: fewer, clearer options per screen and per menu; every added choice
  costs the user time, so a screen that offers everything offers nothing quickly.
  D19 — Motion: fewer choices means fewer competing motions and a faster read;
  Theme: none — the law is about choice count, not theme; Texture: none — the law is
  about structure, not surface; Visuals: the remaining choices get the space and
  emphasis the removed ones freed; Techniques: progressive disclosure and grouping,
  never decoration; Colors: none — the law does not choose colours.
- **A16 Miller's law** — working memory holds about seven items (give or take two), so
  information must be chunked. Consequence: group lists, steps, and options into
  chunks of five to nine; a 20-item flat list is a memory failure, not a layout.
  D19 — Motion: chunks enter and settle as groups (stagger per chunk, not per item
  past the chunk); Theme: none — the law is about chunking, not theme; Texture:
  none — the law is about structure, not surface; Visuals: chunk boundaries are
  visible (spacing, grouping) so the eye can count the chunks; Techniques: grouping
  and spacing, never decoration; Colors: none — the law does not choose colours.
- **A17 Doherty threshold** — the system must respond within about 400ms or the user's
  attention breaks and productivity falls. Consequence: every interaction gets visible
  feedback inside 400ms (an optimistic update, a loading state, a press response) —
  a silent 500ms wait is a defect even if the result is correct. D19 — Motion:
  feedback inside 400ms is the motion deadline every animation budget answers to;
  Theme: none — the threshold is a human limit, not a theme choice; Texture: none —
  the law is about timing, not surface; Visuals: the feedback must be visible (a
  state change the eye can see), not a silent background update; Techniques:
  optimistic updates and loading states, never a longer animation; Colors: none —
  the law does not choose colours.
- **A18 Postel's law** — be liberal in what you accept, conservative in what you send.
  Consequence: accept sloppy input gracefully (forgiving parsing, tolerant gestures,
  generous tap targets) and emit strict, predictable output (exact states, clean
  values). D19 — Motion: tolerant input means a gesture that slightly misses still
  lands, and the motion confirms it instead of snapping back; Theme: none — the law
  is about input/output, not theme; Texture: none — the law is about behaviour, not
  surface; Visuals: the accepted state is shown plainly so the user knows what was
  taken; Techniques: forgiving handlers and strict emitters, never silent coercion;
  Colors: none — the law does not choose colours.
- **A19 Jakob's law** — users spend most of their time on other products, so they
  expect your product to work like the ones they already know. Consequence: follow
  established patterns for standard interactions (menus, dialogs, navigation) and
  spend originality on the product's own job, not on reinventing a dropdown. D19 —
  Motion: standard interactions use standard motion (the motion-patterns defaults),
  so the user never has to learn a new feel for a known job; Theme: the dealt theme
  dresses the pattern, it does not replace the pattern's behaviour; Texture: none —
  the law is about behaviour, not surface; Visuals: the familiar pattern reads as
  familiar at a glance; Techniques: the motion-patterns library, never a bespoke
  reinvention of a standard control; Colors: none — the law does not choose colours.
- **A20 Frequency of use** — the more often a thing is used, the more it should be
  optimised (bigger, nearer, faster, fewer steps). Consequence: rank every action by
  how often it is used and spend the best targets, the shortest paths, and the
  snappiest feedback on the top of the ranking; a rare action never outranks a daily
  one. D19 — Motion: the most-used actions get the fastest, most direct motion;
  Theme: none — the law is about ranking, not theme; Texture: none — the law is
  about priority, not surface; Visuals: the most-used action is the most prominent
  one on its screen; Techniques: ranking by measured or stated frequency, never by
  guesswork; Colors: none — the law does not choose colours.

Theme-match precondition: the laws are decision rules, not a look — every element
decided under them must still match the dealt theme (its material, tokens, palette
balance, and do-nots); a law applied in a way that clashes with the theme is not
applied, and the reason is recorded in `docs/design-tokens.md` with the element.
```

## AB-03 — motion-foundations, token values (ANIM_TOKENS_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, `### Token system` code block.
- **Note:** each sub-entry below is a separate anchor/insert pair inside the same code
  block. All anchors verified count==1 in the built file. The numbers are VALUES with
  their context (which element, which state), per SPEC §4c — not prose suggestions.

### AB-03a — dropdown duration (B2)

- **Anchor (count==1, insert AFTER):**
  ```
      fast:    0.18,
  ```
- **Insert:**
  ```
      dropdown: 0.2,   // B2 (fix #22): dropdowns animate at 150–250ms; 0.2s is the default inside the range.
  ```

### AB-03b — list-row stagger (B3) — CONFLICT FLAG, see header item 1

- **Anchor (count==1, insert AFTER):** the line inserted by AB-03a:
  ```
      dropdown: 0.2,   // B2 (fix #22): dropdowns animate at 150–250ms; 0.2s is the default inside the range.
  ```
- **Insert:**
  ```
      staggerRow: 0.03, // B3 (fix #22): list rows stagger by 30ms per row. CONFLICT FLAG (SPEC §4c): 0.03s sits below motion-patterns Rule 5's 0.05s floor — Rule 5 is NOT changed here; the parent adjudicates.
  ```

### AB-03c — ease-out curve named for entrances (B1)

- **Anchor (count==1, REPLACE with anchor + comment):**
  ```
      smooth: [0.22, 1, 0.36, 1],
  ```
- **Replacement:**
  ```
      smooth: [0.22, 1, 0.36, 1], // B1 (fix #22): the ease-out curve — entrances use this easing.
  ```

### AB-03d — ease-in-out curve for moves (B9)

- **Anchor (count==1, insert AFTER):**
  ```
      linear: [0, 0, 1, 1],
  ```
- **Insert:**
  ```
      inOut:  [0.65, 0, 0.35, 1], // B9 (fix #22): ease-in-out for moves — an element travelling from one place to another.
  ```

### AB-03e — popover start scale (B10) + knob stretch (B5)

- **Anchor (count==1, insert AFTER):**
  ```
      press:  0.95,
  ```
- **Insert:**
  ```
      popover: 0.95, // B10 (fix #22): popovers start at scale 0.95 and grow to 1. Separate token from press — the value coincides with press by chance, never merge them.
      stretch: 1.12, // B5 (fix #22): a moving knob stretches 12% along its direction of travel while it moves, then springs back.
  ```

### AB-03f — exit factor (B15) — CONFLICT FLAG, see header item 2

- **Anchor (count==1, REPLACE with anchor + inserted line):**
  ```
      pop:    1.04,
    },
  }
  ```
  (the end of the `scale` map and the close of the `motionTokens` object)
- **Replacement:**
  ```
      pop:    1.04,
    },
    exitFactor: 0.8, // B15 (fix #22): exits run 20% shorter than their enter — exit duration = 0.8 x the matching enter duration. CONFLICT FLAG (SPEC §4c): quick-reference `exit-faster-than-enter` says ~60–70%; quick-reference is NOT changed here; the parent adjudicates.
  }
  ```

- **D19 (for the token group as a whole)** — Motion: the tokens are the values every
  animation in the build runs on, so motion timing is decided once and reused, never
  improvised per component; Theme: tokens are values, not looks — the theme still
  decides what the moving element is and what it means; Texture: none — tokens carry
  no surface treatment; Visuals: the values keep entrances, moves, and exits legible
  (nothing too fast to see, nothing slow enough to wait on); Techniques: values live
  in `motionTokens` and are imported, never hardcoded in components (Rule 5);
  Colors: none — tokens do not choose colours.
- **Theme-match precondition:** tokens are numbers, not designs — every element
  animated with them must still match the dealt theme (its material, tokens, palette
  balance, and do-nots); a token applied in a way that clashes with the theme is not
  applied, and the reason is recorded in `docs/design-tokens.md` with the element.

## AB-04 — motion-foundations, easing rules (B1/B9) (ANIM_RULES_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, `## Rules` section.
- **Anchor (count==1, insert AFTER):** the end of Rule 10 (M2):
  ```
  reduced-motion renders are exempt from the entrance itself but never from visibility.
  ```
- **Insert (full text):**

```md
11. **Entrances ease out (fix #22 B1).** Every entrance uses the ease-out curve
    (`easing.smooth`): fast start, slow landing. An entrance that eases in (slow start)
    feels like the page is holding the element back.
12. **Moves ease in-out (fix #22 B9).** An element travelling from one place to another
    uses the ease-in-out curve (`easing.inOut`): slow start, fast middle, slow landing.
    Ease-out is for arriving; ease-in-out is for travelling.
```

- **D19 (for rules 11–12)** — Motion: the easing curve is what makes an entrance feel
  like an arrival and a move feel like travel; Theme: the curves are the theme's
  motion voice applied consistently, never per-component improvisation; Texture:
  none — easing carries no surface treatment; Visuals: eased motion reads as
  deliberate where linear motion reads as mechanical; Techniques: the curves come from
  `motionTokens.easing`, never hardcoded (Rule 5); Colors: none — easing does not
  choose colours.
- **Theme-match precondition:** as AB-03 — the easing rules govern how elements move,
  never what they look like; every element moved under them must still match the dealt
  theme, and a clash is not applied, with the reason recorded in
  `docs/design-tokens.md`.

## AB-05 — motion-patterns, Rules 11–19 (B11–B16, B8, B20, B7) (ANIM_RULES_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Rules` section.
- **Anchor (count==1, insert AFTER):** the end of Rule 10 (M2):
  ```
  reduced-motion renders are exempt from the entrance itself but never from visibility.
  ```
- **Insert (full text):**

```md
11. **Enter from the trigger (fix #22 B11 — origin-aware animation, glossary G10).**
    A popover, dropdown, or menu enters from the element that opened it: its
    `transformOrigin` sits at the trigger, and its initial position grows out of the
    trigger's edge. An element that appears from nowhere has no spatial story.
12. **Exit to the trigger (fix #22 B12 — origin-aware animation, glossary G10).** The
    same element exits back to its trigger: same origin, reversed path. Enter and exit
    are one round trip, not two unrelated animations.
13. **No bounce on everyday UI (fix #22 B13).** The bounce easing (`easing.bounce`) and
    the `bouncy` spring are for playful moments only (empty states, onboarding) — never
    for everyday controls, menus, dialogs, or lists. A bouncing dropdown is a toy, not
    a tool.
14. **Don't tween while held (fix #22 B14 — related: glossary G18 interruptible
    animation).** While the user holds or drags an element, drive its values directly
    from the gesture (motion values, `useTransform`) — never run a timed tween against
    a held element. A tween fights the hand; a driven value follows it. On release, a
    spring takes over.
15. **Exits run 20% shorter than their enter (fix #22 B15).** Exit duration = 0.8 x the
    matching enter duration (`motionTokens.exitFactor`). An exit that lasts as long as
    its enter feels like the interface is lingering; a shorter, quieter exit feels
    responsive. (Conflict flag: see the header of this patch spec, item 2.)
16. **Overlap old & new states (fix #22 B16).** During an in-container content swap, the
    incoming state starts before the outgoing state finishes, so the screen never
    blanks between them — crossfade, don't cut to empty. SCOPE: in-container swaps
    only. Page transitions still use `mode="wait"` (Rule 3): enter must not start
    until exit completes there.
17. **Pulse to confirm success (fix #22 B8 — one family with A10 exaggerated feedback;
    D20 animate-useful-feedback points here).** A successful action gets one short
    pulse (scale up slightly and back, once) so the confirmation cannot be missed. One
    pulse, then still — a looping pulse is a live indicator (see `motion-advanced`
    `PulseDot`), not a confirmation.
18. **Reuse the same layoutId (fix #22 B20 — shared element transition, glossary G20).**
    When the same object appears in two contexts, both contexts use the same
    `layoutId` so the object expands in place (see the Shared-element crossfade
    example below — its primary home). A disconnected replacement (unmount one element,
    mount a different one with no shared `layoutId`) loses the object; the eye has to
    find it again.
19. **Move along arcs (fix #22 B7 — the moving-in-arcs principle, A7, applied).** An
    element travelling between two points follows a curved path (an arc via `x`/`y`
    keyframes or a curved `useTransform` mapping), not a straight line — straight-line
    travel between distant points reads as mechanical. Short hops may stay straight; any
    travel the eye follows takes the arc.

Icon swaps (fix #22 B18) are already covered — `make-interfaces-feel-better` ("Icon
swaps: cross-fade with opacity, scale, and blur instead of instant visibility
toggles") — so no new rule is added here; the motion-patterns button and modal
examples follow it.
```

- **D19 (for rules 11–19 as a set)** — Motion: the rules decide where motion starts and
  ends, how long exits run, and what overlaps, so every transition tells a spatial
  story instead of flashing; Theme: origin, bounce, and overlap are applied in the
  dealt theme's motion voice, never as stock effects; Texture: none — the rules govern
  motion, not surface treatment; Visuals: trigger-anchored, overlapped, confirmed
  motion keeps the eye on the object instead of losing it between states; Techniques:
  all values come from `motion-foundations` tokens (Rule 8), and the trigger origin is
  set explicitly per element; Colors: none — the rules do not choose colours.
- **Theme-match precondition:** as AB-03 — every element moved under these rules must
  still match the dealt theme; a clash is not applied, with the reason recorded in
  `docs/design-tokens.md`.

## AB-06 — motion-patterns, Dropdown example (B2) + stagger-as-details-settle note (B6) (ANIM_RULES_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples` section.
- **Anchor (count==1, insert BEFORE):**
  ```
  ### Modal
  ```
- **Insert (full text):**

```tsx
### Dropdown (fix #22 B2)

```tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

// B2: dropdowns animate at 150–250ms (motionTokens.duration.dropdown, 0.2s default).
// The panel enters from its trigger (B11) and exits back to it (B12).
<AnimatePresence>
  {open && (
    <motion.div
      key="menu"
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -4 }}
      transition={{ duration: motionTokens.duration.dropdown, ease: motionTokens.easing.smooth }}
      style={{ transformOrigin: "top left" }} // origin at the trigger (B11/B12)
    />
  )}
</AnimatePresence>
```

**Stagger as details settle (fix #22 B6).** When a row's details load after the row
itself (image, then title, then meta), stagger the details in 30ms steps
(`motionTokens.duration.staggerRow`) so the row settles instead of popping whole — the
same stagger primitive as the Stagger list example above, applied inside the row
(glossary G14 Stagger). This is the secondary-action principle (A8) applied to a row.
```

- **D19 (for the dropdown example + B6 note)** — Motion: the dropdown duration band
  and the 30ms settle steps are the timing values the pattern runs on; Theme: the
  dropdown and the settling row are the theme's own surfaces, animated, never restyled
  by the animation; Texture: none — the example adds no surface treatment; Visuals:
  the panel grows from its trigger and the row settles visibly instead of flashing;
  Techniques: durations and stagger come from `motionTokens` (Rule 8), the trigger
  origin is set explicitly; Colors: none — the example does not choose colours.
- **Theme-match precondition:** as AB-03 — the dropdown and the settling row must
  match the dealt theme; a clash is not applied, with the reason recorded in
  `docs/design-tokens.md`.

## AB-07 — motion-patterns, Popover example (B10/B11/B12) (ANIM_RULES_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples` section.
- **Anchor (count==1, insert BEFORE):**
  ```
  ### Toast stack
  ```
- **Insert (full text):**

```tsx
### Popover (fix #22 B10/B11/B12)

```tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

// B10: popovers start at scale 0.95 (motionTokens.scale.popover) and grow to 1.
// B11/B12: the popover enters from its trigger and exits back to it.
<AnimatePresence>
  {open && (
    <motion.div
      key="popover"
      initial={{ opacity: 0, scale: motionTokens.scale.popover }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: motionTokens.scale.popover }}
      transition={springs.gentle}
      style={{ transformOrigin: "top left" }} // origin at the trigger (B11/B12)
    />
  )}
</AnimatePresence>
```
```

- **D19 (for the popover example)** — Motion: the 0.95 start scale and the trigger
  origin are what make the popover read as growing out of its trigger; Theme: the
  popover is the theme's own surface, animated, never restyled by the animation;
  Texture: none — the example adds no surface treatment; Visuals: the popover's growth
  is visible and anchored, so the eye follows it from the trigger; Techniques: the
  start scale comes from `motionTokens.scale.popover` (Rule 8), the origin is set
  explicitly; Colors: none — the example does not choose colours.
- **Theme-match precondition:** as AB-03.

## AB-08 — motion-patterns, B20 note on the shared-element example (ANIM_RULES_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples` section.
- **Anchor (count==1, insert BEFORE):**
  ```
  ### Accordion
  ```
- **Insert (full text):**

```md
**Reuse the same layoutId (fix #22 B20).** The example above is the primary home of
this rule: the source and the destination carry the same `layoutId` (`"hero-image"`),
so the same object expands instead of being replaced. A disconnected replacement —
unmounting one element and mounting a different one with no shared `layoutId` — is
the failure this rule prevents: the eye loses the object and has to find it again.
This is the shared element transition (glossary G20); B20 points at it and adds
nothing beyond the rule and this example.
```

- **D19 (for the B20 note)** — Motion: the shared `layoutId` is what turns a cut into
  a continuous move; Theme: the expanding object is the theme's own element, carried
  across contexts, never restyled by the move; Texture: none — the note adds no
  surface treatment; Visuals: the object stays visible through the transition, so
  spatial continuity holds; Techniques: one `layoutId` string shared by both contexts
  (Rule 8 — no inline values); Colors: none — the note does not choose colours.
- **Theme-match precondition:** as AB-03.

## AB-09 — motion-advanced, Rules 9–11 (B16/B17/B19) (ANIM_ADV_F22)

- **Target:** `skills/motion-advanced/SKILL.md`, `## Rules` section.
- **Anchor (count==1, insert AFTER):**
  ```
  8. **SVG morphing requires equal path command counts.** Paths with different command structures snap instead of interpolating.
  ```
- **Insert (full text):**

```md
9. **Overlap old & new states in multi-step sequences (fix #22 B16).** In an imperative
    sequence (`useAnimate`), the incoming step starts before the outgoing step finishes,
    so the screen never blanks between them. SCOPE: in-container swaps and sequences
    only — page transitions still use `mode="wait"` (motion-patterns Rule 3).
10. **Masks for reveals & colour (fix #22 B17).** Reveal an element (or a colour change)
    behind a mask — `clipPath` inset, or a mask image — instead of fading the whole
    element in: the mask edge is the moving part, the content behind it is already
    there. A colour change revealed by a sweeping mask reads as a transformation; the
    same change as a flat crossfade reads as a swap.
11. **Rubber band past bounds (fix #22 B19).** A dragged or scrolled element may travel
    past its bound and spring back — resistance grows with distance past the bound
    (`dragElastic` on drag; a spring on release). The overshoot is small and the
    spring-back is immediate; a bound that stops dead feels broken, and an overshoot
    that never returns is a bug. This is the anticipation principle (A2) applied to a
    bound.
```

- **D19 (for rules 9–11 as a set)** — Motion: overlap, masks, and rubber-banding decide
  how a sequence hands off, how a reveal travels, and how a bound behaves, so advanced
  motion stays continuous instead of cutting; Theme: the choreography is the dealt
  theme's motion voice, never a stock effect; Texture: none — the rules govern motion,
  not surface treatment; Visuals: the eye follows the mask edge and the overshoot
  instead of losing the element between states; Techniques: `useAnimate` sequences,
  `clipPath`/mask, and `dragElastic` + spring release (all token-governed, Rule 6);
  Colors: the mask rule covers colour reveals — the revealed colour is the theme's own
  token, never a new colour invented by the reveal.
- **Theme-match precondition:** as AB-03 — every element moved under these rules must
  still match the dealt theme; a clash is not applied, with the reason recorded in
  `docs/design-tokens.md`.

## AB-10 — motion-advanced, examples: mask reveal (B17), stretching knob (B5), overlapping state change (B16) (ANIM_ADV_F22)

- **Target:** `skills/motion-advanced/SKILL.md`, `## Code Examples` section.
- **Anchor (count==1, insert BEFORE):**
  ```
  ### Cursor follower
  ```
- **Insert (full text):**

```tsx
### Mask reveal (fix #22 B17)

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

// B17: the reveal travels behind a mask — the clip edge moves, the content is
// already there. Same technique reveals a colour change: the new colour sits
// behind the mask and the mask sweeps across.
<motion.div
  initial={{ clipPath: "inset(0 100% 0 0)" }}
  animate={{ clipPath: "inset(0 0% 0 0)" }}
  transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
/>
```

### Stretching knob (fix #22 B5)

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

// B5: a moving knob stretches 12% along its direction of travel
// (motionTokens.scale.stretch, 1.12) while it moves, then springs back.
// This is the anticipation principle (A2) applied to a control.
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 200 }}
  whileDrag={{ scaleX: motionTokens.scale.stretch }}
  dragTransition={springs.release}
/>
```

### Overlapping state change (fix #22 B16)

```tsx
"use client"
import { useAnimate } from "motion/react"

// B16: the incoming state starts before the outgoing state finishes — the
// screen never blanks between them. Scope: in-container swaps only;
// page transitions still use mode="wait" (motion-patterns Rule 3).
const [scope, animate] = useAnimate()

async function swap() {
  await Promise.all([
    animate(".old", { opacity: 0 }, { duration: 0.2 }),
    animate(".new", { opacity: 1 }, { duration: 0.2, delay: 0.1 }),
  ])
}
```
```

- **D19 (for the three examples as a set)** — Motion: the mask edge, the 12% stretch,
  and the overlapped handoff are the moving parts the eye follows; Theme: each example
  animates the theme's own element, never restyles it; Texture: none — the examples add
  no surface treatment; Visuals: the reveal, the stretch, and the handoff are all
  visible and anchored, so nothing flashes or vanishes; Techniques: `clipPath`,
  `motionTokens.scale.stretch`, and `useAnimate` with an explicit overlap delay (all
  token-governed, Rule 6); Colors: the mask example's revealed colour is the theme's
  own token, never a new colour invented by the reveal.
- **Theme-match precondition:** as AB-03.

## AB-11 — make-interfaces-feel-better, pointer to the principles and laws

- **Target:** `skills/make-interfaces-feel-better/SKILL.md`, `## When to Use` section.
- **Anchor (count==1, insert AFTER):**
  ```
  For React/Next.js motion implementation, see the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`) — this skill decides the feel/timing; they provide the tokens and patterns.
  ```
- **Insert (full text):**

```md
**Motion feel decisions route through the principles (fix #22, PRINCIPLES_F22 /
LAWS_F22).** Timing, easing, and feel calls in this skill are decided against
`motion-foundations` Principles A1–A12 and the UX laws A13–A20 — name the principle or
law behind each feel decision in the decision record; this skill never invents a feel
rule the principles do not support. Theme-match precondition: every feel decision must
still match the dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.
```

- **D19 (for the pointer)** — Motion: the pointer is what keeps feel decisions grounded
  in the principles instead of taste; Theme: the principles are applied in the dealt
  theme's motion voice; Texture: none — the pointer adds no surface treatment;
  Visuals: none — the pointer changes no look, only where the decision is grounded;
  Techniques: the pointer names the owning skill (`motion-foundations`), never restates
  it; Colors: none — the pointer does not choose colours.

## AB-12 — ui-ux-pro-max, pointer to the laws (LAWS_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 2: Generate Design System` section.
- **Anchor (count==1, insert AFTER):**
  ```
  **Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.
  ```
- **Insert (full text):**

```md
**UX laws for motion decisions (fix #22, LAWS_F22).** Motion and interaction-feel
decisions on app surfaces route through `motion-foundations` Decision Guidance (Fitts's,
Hick's, Miller's, Doherty, Postel's, Jakob's, frequency of use) — the laws live there,
not here; this skill points at them and never restates them. Feel and timing itself is
decided in `make-interfaces-feel-better` against `motion-foundations` Principles
(PRINCIPLES_F22). Theme-match precondition: the laws are decision rules, not a look —
every element decided under them must still match the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.
```

- **D19 (for the pointer)** — Motion: the pointer routes motion decisions to the laws
  that govern them; Theme: the laws apply inside the dealt theme, they do not restyle
  it; Texture: none — the pointer adds no surface treatment; Visuals: none — the
  pointer changes no look, only where the decision is grounded; Techniques: the pointer
  names the owning skill (`motion-foundations`), never restates it; Colors: none — the
  pointer does not choose colours.

## AB-13 — ui-ux-pro-max, one accent colour (fix #22 H1, ACCENT_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 2: Generate Design System` section.
- **Anchor (count==1, insert AFTER):**
  ```
  One accent, one button pair, one card style: gates.md F4/F15 governs on landing pages, the Impeccable craft floor on app surfaces.
  ```
- **Insert (full text):**

```md
**One accent colour (fix #22 H1, ACCENT_F22).** The build has ONE accent colour (or
one defined accent palette with a single dominant accent): it is part of the brand
identity tokens (fix #20 B1) and is theme-matched; it is used sparingly and
consistently for the things that must be noticed — CTAs, active states, highlights,
the single most important element per screen — and for action/emphasis only, never as
a general fill or background wash. The accent colour is recorded in the decision
record (`design-system/<project-slug>/MASTER.md` / `docs/design-tokens.md`) with its
fix #19 D19 reason, like every other UI decision. Accent sprawl — multiple competing
accent colours, or the accent used on non-action elements — is a `polish-pass` flag
(see the accent-sprawl check there); this skill states the concept, `polish-pass`
enforces the flag. This is the concept; the fix is D11 "Add an accent colour"
(polish-pass fix guidance), which this rule points at and does not duplicate.
```

- **D19 (for the accent-colour rule)** — Motion: none — the accent colour does not move;
  the accent hierarchy it serves is motion-adjacent only where motion is the accent
  means (see AB-14); Theme: the accent is theme-matched and part of the brand identity
  tokens (fix #20 B1); Texture: none — the accent is a colour, not a surface
  treatment; Visuals: one consistent accent makes the things that must be noticed
  unmistakable, and its sparing use is what keeps it noticeable; Techniques: the
  accent is a token in MASTER.md / `docs/design-tokens.md`, referenced, never a raw
  value in components; Colors: the accent IS the colour decision — one colour, used
  for action/emphasis only, never as a general fill.
- **Theme-match precondition:** the accent colour is theme-matched by definition (it is
  part of the brand identity tokens); an accent that clashes with the dealt theme is
  re-dealt, never applied, and the reason is recorded in `docs/design-tokens.md`.

## AB-14 — ui-ux-pro-max, accent hierarchy (fix #22 H2, ACCENTUATION_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `## When to Apply` section (after the
  captivating-bar paragraph).
- **Anchor (count==1, insert AFTER):**
  ```
  Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable — this skill never states a screen pass/fail.
  ```
- **Insert (full text):**

```md
**Accent hierarchy — every screen declares what draws the eye first (fix #22 H2,
ACCENTUATION_F22).** Accentuation is the deliberate emphasis that creates hierarchy
and focal points — the means by which a screen says "look here first." Means include
size, weight, colour (the fix #22 H1 accent colour), spacing, motion, and texture
(less-flat-ui treatments as accent means). Every screen declares its accent hierarchy
in the decision record — what is accentuated first, second, and third, and by what
means — with a fix #19 D19 reason for each accent. A screen with no deliberate
accentuation (everything the same weight, nothing draws the eye) fails the check —
the check itself is a static record check here; whether the eye lands where the design
intends on the rendered screen is `polish-pass` / `browser-qa` candidate evidence, not
a verdict of this skill. H2 is the umbrella principle; its specific means live where
they already do and are NOT duplicated here: fix #20 F5 (important text gets the
unique important font — that IS an accentuation means), fix #20 F6 (impressive as the
bar), the dealt moments (fix #15 R1/R4/R5 moments ARE accentuation), and the fix #22
H1 accent colour. The design package must name the accent hierarchy (orchestrate
step 3, design-package brief).
```

- **D19 (for the accent-hierarchy rule)** — Motion: motion is one accentuation means —
  the first accent may move while the rest stay still, and the hierarchy names which;
  Theme: the hierarchy is the dealt theme's emphasis order, never a generic
  big-to-small ladder; Texture: texture (less-flat-ui treatments) is one accentuation
  means, named per accent; Visuals: the hierarchy is what makes the screen readable
  at a glance — first, second, third, in that order; Techniques: the hierarchy is
  recorded in the decision record (first/second/third + means + D19 reason per
  accent), never left implicit; Colors: colour (the fix #22 H1 accent colour) is one
  accentuation means, and the accent colour's own rule (AB-13) governs its use.
- **Theme-match precondition:** the hierarchy is theme-matched by definition (its means
  are the theme's own size, weight, colour, spacing, motion, and texture); an accent
  that clashes with the dealt theme is not applied, and the reason is recorded in
  `docs/design-tokens.md`.

## Integrator checklist (after applying)

1. Rebuild (`bash build.sh`, exit 0) and confirm the built tree contains every anchor
   token: PRINCIPLES_F22, LAWS_F22, ANIM_TOKENS_F22, ANIM_RULES_F22, ANIM_ADV_F22,
   ACCENT_F22, ACCENTUATION_F22 — plus the orchestrate staged edit (step 3) surviving
   the rebuild.
2. Confirm counts: no new skill, no new command, no new trigger key from this patch
   spec (pointers and rules only). The token additions (AB-03) add values to
   `motionTokens`, not skills.
3. Confirm the three conflict flags (header items 1–3) are carried into the manifest
   unresolved — do NOT resolve them by editing Rule 5, quick-reference, or
   `scale.press` while applying this spec.
4. Confirm banned terms are 0 in the built tree (case-insensitive).
5. Confirm the fix #19/#20/#21 font rules, the screen-verdicts rule, and the model
   pins are untouched by this spec (no entry touches them).
