#!/usr/bin/env python3
"""Fix program #22: weave 7 @charles.unemployed reels (142 items) + H1/H2
accents + Mobbin + direct-don't-describe + 4 free libraries + Bang Motion
port into the plugin's design process (fix22/SPEC.md).

Applies every patch block from the five wave-1 spec files to build.sh as a
single runtime patch block (fix17/fix20/fix21 pattern: the block patches the
BUILT tree at build time, after STEP 2 assembles it and after the fix17/19/
20/21 blocks run), plus the Bang pin record and the three.js GSAP pin fix.

Patch specs applied (in dependency-safe order ab -> cd -> g -> process ->
libraries; patches within a file run in list order so chained anchors work):
  AB-01..AB-14  fix22/ab-patches.md (Groups A+B + H1/H2 ui-ux-pro-max +
                orchestrate portions; orchestrate staged edit already applied)
  CD-P1..P7     fix22/cd-pointers.md (Groups C+D pointers)
  G-P-G1..P-G3  fix22/g-pointers.md (glossary owning-skill pointers)
  PROC-P1..P5   fix22/process-patches.md (Mobbin + directives)
  LIB-01..04,   fix22/libraries-patches.md (Lenis / GSAP / Vanta / React Bits)
  LIB-06..08    (LIB-05 already applied to the staged Taste source; NOT
                re-applied here)
  CSV-GSAP      three.js data file GSAP CDN pin 3.12.2 -> 3.15.1 (upstream
                ui-ux-pro-max clone data; no build.sh-embedded copy exists,
                so the runtime block patches the built file)
  BANG-PIN      BANG_PIN record next to the 6 clone SHAs in build.sh
                (record-only pin: the repo is NOT cloned at build time; the
                rules are ported into pitch-deck-video, see fix22/bang-report.md)

Every substitution asserts count==1 at preflight (against the CURRENT built
tree, in-memory simulation in list order) and again at build time (the
runtime block asserts per file). A bad anchor aborts before anything is
written. A silently dropped patch is the worst outcome, so failures are
loud: the patch id + anchor + count are printed and the script exits 1.

APPLICATION DECISIONS (recorded, not silent):
  - AB-03b chains on AB-03a: its anchor is the line AB-03a inserts. The
    preflight simulates the patches in order, so AB-03b is checked against
    the post-AB-03a text; the runtime block applies the subs in list order.
  - AB-03f anchor/replacement indentation: the spec prints the token block
    with +2 spaces (markdown rendering); the real file uses 4-space keys
    and a 0-indent close. The applied anchor/replacement use the file's
    real indentation; content is otherwise verbatim.
  - LIB-02 anchor: the spec's 4-line tail would land the insert INSIDE the
    tsx code fence (before its closing fence). The applied anchor is the
    4-line tail PLUS the closing fence (count==1), so the insert lands
    after the Scroll progress bar example, as the spec's placement says.
  - PROC-P3 anchor: the spec prints only the opening of the Direction
    source bullet; inserting after that fragment would split the bullet
    mid-line. The applied anchor is the complete bullet line (count==1);
    the insert lands after the complete bullet, as the spec's placement says.
  - D19 / theme-match bullets printed after an insert fence are part of the
    inserted text (every new rule carries its D19 reason): they are appended
    to their insert. AB-03's D19 + theme-match (token group as a whole)
    have no named placement; they are appended immediately after the
    motionTokens block (in the AB-03f replacement), the only sensible home.
  - Three token conflicts from ab-patches.md (B3 30ms vs Rule 5 floor; B15
    0.8x vs exit-faster 60-70%; B4 0.97 vs scale.press 0.95) are applied
    EXACTLY as specified, conflict flags carried in the comments. Nothing
    here resolves them; the parent adjudicates.
  - GSAP converges on 3.15.1 everywhere (LIB-02/LIB-03/LIB-04 texts already
    say 3.15.1; the Bang staged note was updated to 3.15.1 by direct edit;
    the threejs.csv CDN pin is fixed here). Three.js is SCOPED, not
    single-version: Vanta scenes 0.134.0, general scenes 0.185.1, Bang's
    0.161.0 recorded as Bang's version only. This supersedes the Bang staged
    note's earlier "ONE pinned version each" alignment flag; flagged in the
    integrator report as a SPEC tension (SPEC §12 alignment vs §11 D3-D4).
  - Sweep #30 Finding 1 (Nov 12): the three group anchor tokens
    ANIM_TOKENS_F22 / ANIM_RULES_F22 / ANIM_ADV_F22 were named in
    ab-patches.md and disposition-B.md but never inserted. AB-03g/AB-05g/
    AB-09g insert ONLY each token string as a group label (a comment line
    above the motionTokens block; a bold label line above the AB-05 rules;
    a bold label line above the AB-09 rules). No new rules, no restated
    content, nothing moved. Their anchors are lines AB-03/AB-05/AB-09
    insert (AB-03g's anchor is pre-existing), so they MUST stay after
    AB-05/AB-09 in PATCHES list order. Re-runs with new patches print
    SKIPPED-ALREADY for patches already in the build.sh block and APPLIED
    for the new ones (see preflight `already` + main()).

Staged-source edits already applied by wave-1 agents (NOT touched here):
  orchestrate SKILL.md (step 3: principles/laws/H2/Mobbin research/
  directives), design-taste-frontend SKILL.md + 15 Hallmark theme files +
  glossary file, polish-pass slop-checklist.md + unslop-fixes.md + wiring,
  pitch-deck-video SKILL.md (Bang port). Direct staged fixes applied by
  hand alongside this script (not through it): glossary G8 40x40px wording,
  disposition-E.md:122 banned-pattern scrub, pitch-deck-video GSAP 3.15.1
  convergence note.
"""
import os
import re
import shutil
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")
BANG_SHA = "c1aa65e921c970d858705fcb4a53a8294d1a4131"

MF = "skills/motion-foundations/SKILL.md"
MP = "skills/motion-patterns/SKILL.md"
MA = "skills/motion-advanced/SKILL.md"
MIFB = "skills/make-interfaces-feel-better/SKILL.md"
UIPRO = "skills/ui-ux-pro-max/SKILL.md"
UIPRO_QR = "skills/ui-ux-pro-max/references/quick-reference.md"
THREEJS_CSV = "skills/ui-ux-pro-max/data/stacks/threejs.csv"
GAN_PLANNER = "agents/ecc-gan-planner.md"
GAN_GENERATOR = "agents/ecc-gan-generator.md"
GAN_EVALUATOR = "agents/ecc-gan-evaluator.md"
LFUI = "skills/less-flat-ui/SKILL.md"
DS = "skills/design-system/SKILL.md"
PP = "skills/polish-pass/SKILL.md"

# --- long anchors (verbatim from the built tree) ---

AB01_ANCHOR = """Responsiveness always outranks smoothness. A 60 fps animation that causes
input delay is worse than no animation."""

AB03F_OLD = """    pop:    1.04,
  },
}"""

AB03F_NEW = """    pop:    1.04,
  },
  exitFactor: 0.8, // B15 (fix #22): exits run 20% shorter than their enter — exit duration = 0.8 x the matching enter duration. CONFLICT FLAG (SPEC §4c): quick-reference `exit-faster-than-enter` says ~60–70%; quick-reference is NOT changed here; the parent adjudicates.
}"""

AB03_TAIL = """

- **D19 (for the token group as a whole)** — Motion: the tokens are the values every animation in the build runs on, so motion timing is decided once and reused, never improvised per component; Theme: tokens are values, not looks — the theme still decides what the moving element is and what it means; Texture: none — tokens carry no surface treatment; Visuals: the values keep entrances, moves, and exits legible (nothing too fast to see, nothing slow enough to wait on); Techniques: values live in `motionTokens` and are imported, never hardcoded in components (Rule 5); Colors: none — tokens do not choose colours.

- **Theme-match precondition:** tokens are numbers, not designs — every element animated with them must still match the dealt theme (its material, tokens, palette balance, and do-nots); a token applied in a way that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element."""

LIB02_ANCHOR = """      style={{ scaleX: scrollYProgress }}
    />
  )
}
```"""

LIB04_ANCHOR = """- `--motion` attaches a ready-to-use GSAP snippet (with framework notes, Do/Don't, and performance notes) pulled from `--domain gsap`, matched to the resolved tier (Subtle/Standard/Complex). The `--motion` dial is only an intensity parameter — it picks how much motion, not how the interface should feel or when it should move. Motion feel and timing decisions belong to `make-interfaces-feel-better` (see `rules/hackathon-mode.mdc` §5): decide feel/timing there first and record the decision as one line in the design-system brief (MASTER.md) before setting `--motion`, then use `--motion` only to set the intensity tier of the implementation. Do not use `--motion` to make a feel/timing decision on its own."""

LIB06_ANCHOR = """**Anti-generic bar (design guidance, not a screen verdict):** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above. Design guidance the brief and Verify record as candidate evidence for `browser-qa` (checked against the recorded named direction): (1) Direction trace — every primary screen should visibly trace to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product is candidate evidence for `browser-qa`. (2) Memorable anchor — the primary view should carry the one unmistakable anchor from the captivating bar above; if no anchor can be named, record that as candidate evidence for `browser-qa`. (3) Not a default template — a surface that looks like a default template is candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail."""

P3_ANCHOR = """- **Direction source**: [the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` BEFORE this loop — copied here, not generated: the planner records the supplied direction and never re-derives one from a searched reference or a fresh invention; if no direction is recorded, do NOT invent one and do NOT record a brief default: the design-lead step in `/gan-build` Phase 1 records the direction before this agent launches — if this agent is ever launched with no direction recorded, invoke the design-lead (model `grok-4.7-high`) to generate it through the package skills and record it in `docs/design-tokens.md` first, then copy it here — never a searched external reference, per the anti-derivative rule]"""

P7A_ANCHOR = """### Button feedback

```tsx
"use client"
import { motion } from "motion/react"
import { springs, motionTokens } from "@/lib/motion-tokens"

<motion.button
  whileHover={{ scale: motionTokens.scale.pop }}
  whileTap={{ scale: motionTokens.scale.press }}
  transition={springs.snappy}
/>
```"""

PG2_ANCHOR = """- **`motion-patterns`** — consumes tokens and springs defined here to build button, modal, stagger, page transition, and scroll patterns. Does not redefine any values."""

PG3_ANCHOR = """- **`motion-foundations`** — defines all tokens, springs, the `useSafeMotion` hook, and SSR guards that every pattern here imports. Must be set up first."""

# --- AB insert texts (fix22/ab-patches.md, verbatim) ---

AB01 = """

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

- **D19 (for the principles set as a whole)** — Motion: the principles decide what moves,
how it moves, and how fast, so motion serves attention and state; Theme: each
principle is applied in the dealt theme's motion voice, never as a generic stock move;
Texture: none — the principles govern motion, not surface treatment; Visuals: staging,
arcs, and appeal keep the moving picture legible and on-character; Techniques: the
principles route to the motion-* token and pattern implementations, never to ad-hoc
values; Colors: none — the principles do not choose colours."""

AB02 = """
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
"""

AB03A = """
    dropdown: 0.2,   // B2 (fix #22): dropdowns animate at 150–250ms; 0.2s is the default inside the range."""

AB03B = """
    staggerRow: 0.03, // B3 (fix #22): list rows stagger by 30ms per row. CONFLICT FLAG (SPEC §4c): 0.03s sits below motion-patterns Rule 5's 0.05s floor — Rule 5 is NOT changed here; the parent adjudicates."""

AB03C_NEW = """    smooth: [0.22, 1, 0.36, 1], // B1 (fix #22): the ease-out curve — entrances use this easing."""

AB03D = """
    inOut:  [0.65, 0, 0.35, 1], // B9 (fix #22): ease-in-out for moves — an element travelling from one place to another."""

AB03E = """
    popover: 0.95, // B10 (fix #22): popovers start at scale 0.95 and grow to 1. Separate token from press — the value coincides with press by chance, never merge them.
    stretch: 1.12, // B5 (fix #22): a moving knob stretches 12% along its direction of travel while it moves, then springs back."""

AB04 = """
11. **Entrances ease out (fix #22 B1).** Every entrance uses the ease-out curve
    (`easing.smooth`): fast start, slow landing. An entrance that eases in (slow start)
    feels like the page is holding the element back.
12. **Moves ease in-out (fix #22 B9).** An element travelling from one place to another
    uses the ease-in-out curve (`easing.inOut`): slow start, fast middle, slow landing.
    Ease-out is for arriving; ease-in-out is for travelling.

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
`docs/design-tokens.md`."""

AB05 = """
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
`docs/design-tokens.md`."""

AB06 = """
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
"""

AB07 = """
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

- **D19 (for the popover example)** — Motion: the 0.95 start scale and the trigger
origin are what make the popover read as growing out of its trigger; Theme: the
popover is the theme's own surface, animated, never restyled by the animation;
Texture: none — the example adds no surface treatment; Visuals: the popover's growth
is visible and anchored, so the eye follows it from the trigger; Techniques: the
start scale comes from `motionTokens.scale.popover` (Rule 8), the origin is set
explicitly; Colors: none — the example does not choose colours.

- **Theme-match precondition:** as AB-03.
"""

AB08 = """
**Reuse the same layoutId (fix #22 B20).** The example above is the primary home of
this rule: the source and the destination carry the same `layoutId` (`"hero-image"`),
so the same object expands instead of being replaced. A disconnected replacement —
unmounting one element and mounting a different one with no shared `layoutId` — is
the failure this rule prevents: the eye loses the object and has to find it again.
This is the shared element transition (glossary G20); B20 points at it and adds
nothing beyond the rule and this example.

- **D19 (for the B20 note)** — Motion: the shared `layoutId` is what turns a cut into
a continuous move; Theme: the expanding object is the theme's own element, carried
across contexts, never restyled by the move; Texture: none — the note adds no
surface treatment; Visuals: the object stays visible through the transition, so
spatial continuity holds; Techniques: one `layoutId` string shared by both contexts
(Rule 8 — no inline values); Colors: none — the note does not choose colours.

- **Theme-match precondition:** as AB-03.
"""

AB09 = """
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
`docs/design-tokens.md`."""

AB10 = """
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

- **D19 (for the three examples as a set)** — Motion: the mask edge, the 12% stretch,
and the overlapped handoff are the moving parts the eye follows; Theme: each example
animates the theme's own element, never restyles it; Texture: none — the examples add
no surface treatment; Visuals: the reveal, the stretch, and the handoff are all
visible and anchored, so nothing flashes or vanishes; Techniques: `clipPath`,
`motionTokens.scale.stretch`, and `useAnimate` with an explicit overlap delay (all
token-governed, Rule 6); Colors: the mask example's revealed colour is the theme's
own token, never a new colour invented by the reveal.

- **Theme-match precondition:** as AB-03.
"""

AB11 = """
**Motion feel decisions route through the principles (fix #22, PRINCIPLES_F22 /
LAWS_F22).** Timing, easing, and feel calls in this skill are decided against
`motion-foundations` Principles A1–A12 and the UX laws A13–A20 — name the principle or
law behind each feel decision in the decision record; this skill never invents a feel
rule the principles do not support. Theme-match precondition: every feel decision must
still match the dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

- **D19 (for the pointer)** — Motion: the pointer is what keeps feel decisions grounded
in the principles instead of taste; Theme: the principles are applied in the dealt
theme's motion voice; Texture: none — the pointer adds no surface treatment;
Visuals: none — the pointer changes no look, only where the decision is grounded;
Techniques: the pointer names the owning skill (`motion-foundations`), never restates
it; Colors: none — the pointer does not choose colours."""

AB12 = """
**UX laws for motion decisions (fix #22, LAWS_F22).** Motion and interaction-feel
decisions on app surfaces route through `motion-foundations` Decision Guidance (Fitts's,
Hick's, Miller's, Doherty, Postel's, Jakob's, frequency of use) — the laws live there,
not here; this skill points at them and never restates them. Feel and timing itself is
decided in `make-interfaces-feel-better` against `motion-foundations` Principles
(PRINCIPLES_F22). Theme-match precondition: the laws are decision rules, not a look —
every element decided under them must still match the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.

- **D19 (for the pointer)** — Motion: the pointer routes motion decisions to the laws
that govern them; Theme: the laws apply inside the dealt theme, they do not restyle
it; Texture: none — the pointer adds no surface treatment; Visuals: none — the
pointer changes no look, only where the decision is grounded; Techniques: the pointer
names the owning skill (`motion-foundations`), never restates it; Colors: none — the
pointer does not choose colours."""

AB13 = """
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
re-dealt, never applied, and the reason is recorded in `docs/design-tokens.md`."""

AB14 = """
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
`docs/design-tokens.md`."""

# --- Sweep #30 Finding 1: group anchor labels (insertion only) ---
# Each inserts ONLY its anchor token string as a group label on content
# that already exists. No new rules, no restated content, nothing moved.

AB03G = """
// Animation token values (fix #22) — group anchor: ANIM_TOKENS_F22
"""

AB05G = """
**Animation rules (fix #22) — group anchor: ANIM_RULES_F22.**
"""

AB09G = """
**Advanced animation rules (fix #22) — group anchor: ANIM_ADV_F22.**
"""

# --- CD pointer texts (fix22/cd-pointers.md, verbatim) ---

CD_P1 = """
- `headline-specific` - Headlines name the specific outcome or value (what it does, for whom, to what end), not a generic claim; a vague headline is fixed in polish-pass (UNSLOP_F22 D9 — Make headlines specific), never by restyling here (fix #22)"""

CD_P2 = """
- `cta-emphasis` - The one primary CTA is emphasized by size, weight, fill, and the accent (H1, ACCENT_F22); secondary actions stay subordinate. Emphasis detail lives in polish-pass (UNSLOP_F22 D10 — Emphasize the CTA) (fix #22)"""

CD_P3 = """
- `color-contrast-polish` - Text-contrast failures found in a polish pass are fixed against the polish-pass craft floor (Contrast ≥4.5:1, ≥3:1 large text, in light AND dark, in every state) — see UNSLOP_F22 D15 (fix #22); this rule states the ratio, the craft floor is the check"""

CD_P4 = """
- `headline-wrap-polish` - Headline wrapping is fixed in a polish pass against the craft floor (headings use `text-wrap: balance`, no orphans, no mid-phrase breaks) — see UNSLOP_F22 D16 (fix #22)"""

CD_P5 = """
- `tabular-polish` - Tabular figures are applied in a polish pass wherever digits change or align (counters, prices, tables) — see UNSLOP_F22 D18 (fix #22); the same value also lives in make-interfaces-feel-better (tabular-nums rule)"""

CD_P6 = """
- `spacing-group-polish` - Grouping with spacing is applied in a polish pass (related items tight, distinct groups at least 2 spacing steps apart; spacing, not dividers or borders, does the grouping) — see UNSLOP_F22 D8 (fix #22); this skill owns the spacing scale (`spacing-scale`)"""

CD_P7A = """
Animate useful feedback only (UNSLOP_F22 D20, fix #22): press feedback, a success pulse, a state change — motion that tells the user something happened. No decorative motion. This is one family with motion-foundations Principle A10 (Exaggerated feedback) and motion-patterns B8 (Pulse to confirm success); the A10/B8 items live in the motion skills (Groups A+B), this fix points at them."""

CD_P7B = """
Feedback animation (UNSLOP_F22 D20) uses the `fast` token for button feedback; see motion-patterns "Button feedback" and Principle A10 / B8 (fix #22)."""

# --- G pointer texts (fix22/g-pointers.md, verbatim) ---

G_PG1 = """
Design vocabulary — the definitions of kerning, optical centre, tabular numbers, tracking, x-height, leading, widow, line length, optimistic update, touch target, affordance, combobox, progressive disclosure, layout shift, safe area, and OKLCH live in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies those concepts, the glossary defines them."""

G_PG2 = """
Design vocabulary — the definition of interruptible animation (G18) lives in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies the concept, the glossary defines it."""

G_PG3 = """
Design vocabulary — the definitions of origin-aware animation (G10), stagger (G14), and shared element transition (G20) live in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies those concepts, the glossary defines them."""

# --- Process patch texts (fix22/process-patches.md, verbatim) ---

PROC_P1 = """

**Pattern reference while building (fix #22 §9, MOBBIN_PATTERN_F22):** when a build needs a component or flow this skill describes abstractly, the implementing agent MAY consult the matching Mobbin pattern (mobbin.com) for how real apps handle it — structure, states, conventions — then implements it through this skill, theme-matched, with a D19 reason. The no-copy boundary: Mobbin informs pattern knowledge only — never the design direction, never a screen to copy; the generating skill is always the recorded source in `docs/design-tokens.md`, never a Mobbin URL, and a specific Mobbin screen is never cited as the source of a decision. Access is web browsing only on the free tier ($0; limited apps/sites, no search, no Flows/Animations, 3 collections) — no paid subscription, no paid account, no account creation that costs money, no API/MCP on the free tier. If the needed pattern is paywalled or Mobbin is unreachable, build from the skills alone and record the gap — the build is NEVER blocked on Mobbin. Platform match: web patterns for web builds; iOS/Android patterns only where the build is a mobile-web surface and the pattern transfers. Theme-match precondition: a pattern is applied only when it matches the dealt theme (or, on app surfaces with no landing, the named direction in `design-system/<project-slug>/MASTER.md`). (D19 — Motion: patterns inform how a flow moves; Theme: the dealt theme filters which patterns apply; Texture: none — pattern reference sets no surface treatment; Visuals: patterns inform the structure users expect; Techniques: consultation is category-level browsing, never copying a screen; Colors: none — pattern reference sets no colour.)"""

PROC_P2 = """

**Component specs are directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** every component spec on app surfaces is a DIRECTIVE — exact values (exact tokens, exact measurements, exact type decisions: face, size, weight, line-height, tracking; exact copy; exact motion values: duration, easing, distance; exact layout instructions: structure, spacing, order), naming the skill it routes through AND giving the values. Every component entry in `design-system/<project-slug>/MASTER.md` records its directive alongside the experience it creates and its six fix #19 D19 dimension lines. A component described in prose without exact values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete; a reason without its directive is not a design decision. Implementers execute component directives verbatim and do not re-interpret them — an ambiguous, unbuildable, or conflicting directive is surfaced as a recorded gap instead of improvised around; improvising around a directive is off-skill improvisation and fails the audit. Theme-match precondition: every component directive must match the recorded direction. (D19 — Motion: directives carry exact motion values where motion is decided; Theme: directives are generated through the recorded direction; Texture: directives name the exact treatments where texture is decided; Visuals: directives fix the exact visual outcome per component; Techniques: directives name the skill they route through; Colors: directives carry exact colour tokens.)"""

PROC_P3 = """

- **Directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** the Design Direction section above is recorded as DIRECTIVES, not prose — every design decision in `gan-harness/spec.md` carries exact values (exact tokens, exact measurements, exact type decisions: face, size, weight, line-height, tracking; exact copy; exact motion values: duration, easing, distance; exact layout instructions: structure, spacing, order), each naming the skill it routes through, plus its fix #19 D19 reason. A design decision written as prose without exact values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete. The Generator executes these directives verbatim and does not re-interpret them. Theme-match precondition: every directive must match the recorded direction copied above. (D19 — Motion: directives carry exact motion values; Theme: directives are the recorded direction expressed as values; Texture: directives name the exact treatments; Visuals: directives fix the exact visual outcome; Techniques: directives name the skill they route through; Colors: directives carry exact colour tokens.)"""

PROC_P4 = """

**Directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** the spec's design decisions are DIRECTIVES with exact values — execute them verbatim. Do not re-interpret a directive: if a directive is ambiguous, unbuildable, or conflicts with another directive, surface it as a recorded gap (note it in the iteration commit message and in your return text) instead of improvising around it. Improvising around a directive is off-skill improvisation and fails the audit. Creativity lives in the spec's directives, fidelity in the execution. A directive without its D19 reason is incomplete — if the spec hands you a design decision as prose without exact values, or a directive without its D19 reason, flag it as a recorded gap and do not build on the prose. (D19 — Motion: execute the spec's exact motion values; Theme: execute the recorded direction as written; Texture: execute the spec's exact treatments; Visuals: execute the spec's exact visual outcome; Techniques: the spec names the skill each directive routes through; Colors: execute the spec's exact colour tokens.)"""

PROC_P5 = """

**Feedback items are directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** every feedback item in the file is a DIRECTIVE — an exact replacement (exact file, exact element, exact old value → exact new value, exact tokens/measurements/copy), naming the skill it routes through, plus its fix #19 D19 reason. A feedback item described in prose without exact replacement values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete. The Generator executes feedback directives verbatim; a feedback item that asks the Generator to re-interpret a design decision instead of giving it exact values is not a directive and must be rewritten. Theme-match precondition: every feedback directive must match the recorded direction. (D19 — Motion: feedback directives carry exact motion values where motion is fixed; Theme: fixes conform to the recorded direction; Texture: feedback names exact treatments where texture is fixed; Visuals: feedback states the exact visual outcome; Techniques: feedback names the skill it routes through; Colors: feedback carries exact colour tokens.) Scoring itself stays as the rubric requires — this rule governs the feedback items, never the scores, and never a screen-distinctiveness verdict (that is `browser-qa`'s alone)."""

# --- Libraries patch texts (fix22/libraries-patches.md, verbatim) ---

LIB01 = """

### Smooth scroll — Lenis (fix #22 §11, LENIS_F22)

Smooth scrolling is a scroll behaviour, not an animation: where a build wants
buttery, momentum-based scrolling, the approved mechanism is Lenis
(`lenis@1.3.27`, MIT, vanilla JS, all stacks). Lenis owns the scroll; it never
owns the animation — scroll-driven animation is driven by GSAP ScrollTrigger
(see `motion-patterns` scroll routing, SCROLLTRIGGER_F22) or by `motion/react`
`useScroll`, never by Lenis itself. Directed init (§10): `new Lenis({
autoRaf: true, lerp: 0.1, anchors: true })` — `lerp: 0.1` is the directed
smoothing value; do not tune it per component. Lenis is NOT initialised when
`prefers-reduced-motion: reduce` matches or on low-end devices
(`motionConfig.shouldAnimate()` false): native scroll is the fallback, and
anchor navigation still works. SCOPE: motion-governed app surfaces only
(React/Next.js and other app stacks). The design-taste-frontend page system
keeps its standing rule (`references/motion.md`: no smooth-scroll library on
any Taste landing page) — Lenis never applies there, and a Taste landing page
that initialises Lenis is an incomplete build. Lenis is a menu item, never a
default: a build that adds smooth scrolling with no theme reason — no dealt
moment or scroll story that needs it — does not add it. Theme-match
precondition: smooth scrolling is a feel decision, not a look — it must still
match the dealt theme's motion voice; a clash is not applied, with the reason
recorded in `docs/design-tokens.md`.

(D19 — Motion: Lenis decides how the scroll itself feels — the smoothing value
is the motion decision; Theme: the scroll feel is the dealt theme's motion
voice, never a stock glide; Texture: none — Lenis adds no surface treatment;
Visuals: the scroll stays native (real scroll positions, working anchors, no
transform illusion), so layout and sticky behaviour never break; Techniques:
the single approved mechanism is Lenis at the pinned version, initialised once
per page with the directed options above; Colors: none — Lenis chooses no
colours.)"""

LIB02 = """

**Scroll-driven animation routes through Lenis + ScrollTrigger (fix #22 §11,
LENIS_F22 / SCROLLTRIGGER_F22).** The two patterns above — Scroll reveal and
Scroll progress bar — are the motion-* defaults on React/Next.js surfaces
(`useScroll` + `useTransform`, `whileInView`). Where the stack supports it and
the build uses GSAP, the same two patterns route through Lenis + ScrollTrigger
instead: Lenis owns the scroll (`lenis@1.3.27`, see `motion-foundations`
smooth-scroll rule, LENIS_F22), ScrollTrigger drives the animation
(`gsap@3.15.1`, `gsap.registerPlugin(ScrollTrigger)` once at the top of the
entry file before any `scrollTrigger` config — an unregistered ScrollTrigger
throws). Directed per §10 (effect name + exact parameters, never prose): a
scroll reveal is `gsap.from(el, { opacity: 0, y: 12, duration:
motionTokens.duration.slow, ease: motionTokens.easing.smooth, scrollTrigger: {
trigger: el, start: 'top 90%', toggleActions: 'play none none reverse' } })`;
a scroll progress bar is a scrubbed tween on `scrollYProgress` (see the `gsap`
domain rows in `ui-ux-pro-max` `data/motion.csv` — the 17 GSAP presets — for
the ready-to-use snippets, matched to the motion tier). The Group B token
values travel with the tween: dropdown duration
`motionTokens.duration.dropdown` (0.2s, 150–250ms band), row stagger
`motionTokens.duration.staggerRow` (0.03s — under the AB-03 conflict flag vs
Rule 5's 0.05s floor; the parent adjudicates), popover start scale
`motionTokens.scale.popover` (0.95), knob stretch
`motionTokens.scale.stretch` (1.12), exits at `motionTokens.exitFactor`
(0.8× the enter — under the AB-03 conflict flag vs quick-reference ~60–70%;
the parent adjudicates), entrances on `motionTokens.easing.smooth`, moves on
`motionTokens.easing.inOut`. The 1500ms fail-safe (fix #17 M2) still binds:
content revealed by a ScrollTrigger tween becomes visible within 1500ms of
entering the viewport even if the trigger never fires. Under
`prefers-reduced-motion: reduce` neither Lenis nor the ScrollTrigger tween
runs — the content renders at its final state immediately. SCOPE:
motion-governed app surfaces only; Taste landing pages keep their standing
rule (`references/motion.md`: scrolling moves nothing but the dealt moment).
Theme-match precondition: every element animated under this routing must still
match the dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: Lenis + ScrollTrigger decide how scroll position drives
animation, with the Group B token values as the tween parameters; Theme: the
scroll story is the dealt theme's motion voice, never a stock parallax;
Texture: none — the routing adds no surface treatment; Visuals: reveals and
progress stay anchored to real scroll position, so nothing appears or vanishes
off-scroll; Techniques: Lenis owns scroll, ScrollTrigger owns the animation,
values come from `motionTokens` (Rule 8); Colors: none — the routing chooses
no colours.)"""

LIB03 = """

**Design asset libraries — stack scope (fix #22 §11, LENIS_F22 / GSAP_F22 /
VANTA_F22 / REACTBITS_F22).** Four free libraries are approved menu items,
never defaults — each is chosen through the skills, theme-matched, with a D19
reason, and directed per §10 (library + effect name + exact parameters).
Stack scope: **Lenis** (`lenis@1.3.27`, MIT) and **GSAP** (`gsap@3.15.1`,
GreenSock Standard "no charge" licence — free, all plugins included) are
vanilla JS and available on every stack in the list above; **Vanta**
(`vanta@0.5.24`, MIT) is vanilla JS plus three.js (`three@0.134.0` for Vanta
scenes — the README-documented pair; the general three.js pin in
`data/stacks/threejs.csv` does not apply to Vanta scenes) and is used only for
dealt hero backgrounds / shader scenes on tech, gaming, software, and
hardware surfaces (see `design-taste-frontend` step 2, VANTA_F22); **React
Bits** (repo commit `9d9c687dc4f55b23539aa5417b703078047efa74`, MIT + Commons
Clause) is React/Next.js ONLY — on any other stack the pattern is
re-implemented with the stack's own tools (see `motion-patterns`,
REACTBITS_F22). Every library effect respects `prefers-reduced-motion: reduce`
(static fallback or off) — no library exempts the rule. Unpinned versions
("latest") FAIL the pin check. The pinned versions live here and in the owning
skills; a build that needs a newer version re-pins deliberately and records
the new pin + its verification, never floats. Theme-match precondition: a
library effect is applied only when it matches the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the libraries are the motion / scroll / background mechanisms,
chosen per build; Theme: every effect is theme-matched or not applied;
Texture: Vanta scenes and the Lenis scroll feel are texture / motion
treatments chosen through the theme; Visuals: scope keeps effects on the
surfaces where they read (3D backgrounds on tech heroes, bits on React);
Techniques: exact pins + stack scope, install-on-demand per project (see
`fix22/libraries-report.md` §4); Colors: none — the libraries choose no
colours (Vanta effect colours are the theme's own tokens).)"""

LIB04 = """

- **GSAP is the animation engine; ScrollTrigger is its scroll plugin (fix #22
  §11, GSAP_F22 / SCROLLTRIGGER_F22).** The `--domain gsap` integration is
  verified intact: 17 GSAP presets in `data/motion.csv` (rows 1–17: hover,
  scroll reveal, stagger list, page transition, parallax, loading, and more),
  each with a ready-to-use snippet, framework notes, Do/Don't, and performance
  notes, matched to the motion tier (Subtle/Standard/Complex) by `--motion`.
  What is new here: **ScrollTrigger** (`gsap@3.15.1`, free with all plugins
  since GSAP 3.13 under the GreenSock Standard "no charge" licence) is the
  approved scroll-animation plugin — register it once
  (`gsap.registerPlugin(ScrollTrigger)`) before any `scrollTrigger` config,
  then drive scroll reveals, scrollytelling pins, parallax layers, and scroll
  progress bars through it (see `motion-patterns` scroll routing,
  SCROLLTRIGGER_F22). Note the preset snippets already use `scrollTrigger`
  configs (motion.csv rows 4–6, 13–14) — this rule names the plugin in the
  skill prose, where it was previously data-only. **Group B numbers travel
  through GSAP tweens:** where the build uses GSAP, the fix #22 Group B values
  are tween parameters, never prose — dropdown duration
  `motionTokens.duration.dropdown` (0.2s, 150–250ms band), row stagger
  `motionTokens.duration.staggerRow` (0.03s), popover start scale
  `motionTokens.scale.popover` (0.95), knob stretch
  `motionTokens.scale.stretch` (1.12), exits at `motionTokens.exitFactor`
  (0.8× the enter), entrances on `motionTokens.easing.smooth` (ease-out),
  moves on `motionTokens.easing.inOut` (ease-in-out). (Press scale is under
  the AB-03 conflict flag — `motionTokens.scale.press` 0.95 vs the polish
  default 0.97; the parent adjudicates; this spec does not set it.) A GSAP
  effect is directed per §10 (effect name + exact parameters: tween target,
  properties, duration, ease, stagger, ScrollTrigger config) — a GSAP effect
  described in prose without exact parameters is incomplete and FAILS the
  handoff check. Every GSAP tween respects `prefers-reduced-motion: reduce`
  (render the final state immediately — every preset's framework notes already
  say so). Pin: `gsap@3.15.1`, exact, in the project's package.json +
  lockfile; "latest" FAILS the pin check. Theme-match precondition: a GSAP
  effect is applied only when it matches the dealt theme; a clash is not
  applied, with the reason recorded in `docs/design-tokens.md`.

  (D19 — Motion: GSAP + ScrollTrigger are the animation engine — the Group B
  values are its tween parameters; Theme: effects are the dealt theme's motion
  voice, never stock tweens; Texture: none — GSAP adds no surface treatment;
  Visuals: ScrollTrigger keeps animation tied to real scroll position, so
  reveals never fire off-screen; Techniques: the 17 presets + `--domain gsap`
  search are the source, values come from `motionTokens`; Colors: none — GSAP
  chooses no colours.)"""

LIB06 = """

**Animated 3D backgrounds — Vanta, on app surfaces (fix #22 §11, VANTA_F22).**
Where an app surface needs an animated 3D background — a hero or a dealt
moment, never a default wash — the approved source is Vanta (`vanta@0.5.24`,
MIT, plus `three@0.134.0` — the README-documented pair; the general three.js
pin in `data/stacks/threejs.csv` does not apply to Vanta scenes). The effect
(WAVES, BIRDS, NET, FOG, CLOUDS, GLOBE, and the other three.js-backed
effects) is chosen through the design package, theme-matched, as a §10
directive (effect name + exact parameters: colour, scale, speed, mouse/touch
controls) recorded in MASTER.md / `docs/design-tokens.md` with its fix #19 D19
reason. Constraints, all binding: theme-matched (effect colours are the
theme's own tokens); a static fallback (the theme's gradient or image ground)
on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable
under `prefers-reduced-motion: reduce` (the finished still shows instead);
never behind text without a scrim and a 4.5:1 contrast check; one Vanta scene
per page by default; destroy the effect on unmount (`effect.destroy()`).
p5.js-backed Vanta effects (e.g. TRUNK) are not covered — no p5 pin,
recorded-gap if a build wants one. The full Vanta rule (shader scenes / hero
backgrounds) lives in `design-taste-frontend` step 2 (VANTA_F22); this skill
states the app-surface use. A Vanta background with no reduced-motion fallback
or no scrim/contrast check is an incomplete build — a static check item in
step 6, never a screen verdict. Theme-match precondition: a Vanta scene is
applied only when it matches the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the scene's motion is the dealt moment's motion; Theme:
theme-matched, colours are the theme's own tokens; Texture: the animated
ground is the surface's texture layer; Visuals: the scene is the hero anchor,
never behind unreadable text; Techniques: Vanta + three.js at the pinned pair,
destroy on unmount; Colors: effect colours are the theme's own tokens.)"""

LIB07 = """
### React Bits — animated components, React/Next only (fix #22 §11, REACTBITS_F22)

React Bits is a copy-paste library of animated React components and
backgrounds (text effects, backgrounds, components) — the bits are source
files copied into the project, not a runtime package: add one bit with the
shadcn CLI (`npx shadcn@latest add @react-bits/<BitName>-TS-TW` for the
TypeScript + Tailwind flavour, `-JS-TW` / `-TS-CSS` / `-JS-CSS` as the build
needs) or the jsrepo CLI (`npx jsrepo add
github/DavidHDev/react-bits/<ComponentName>`), at the pinned repo commit
`9d9c687dc4f55b23539aa5417b703078047efa74` (2026-11-10; MIT + Commons Clause
— free for personal and commercial use inside an app or product; the
components themselves may not be sold, sublicensed, or redistributed as a
library). Each bit is used as a §10 directive (component/effect name + exact
props, as listed for that bit on reactbits.dev — the directive records the
prop values, it never says "a split-text effect") with its fix #19 D19 reason,
recorded in `docs/design-tokens.md`. SCOPE — React/Next.js builds ONLY: this
skill is React-scoped and React Bits is React-only. On a non-React stack the
PATTERN is implemented with the stack's own tools (recorded-gap style: name
the closest equivalent — a CSS / GSAP / vanilla implementation of the same
effect — never force React Bits outside React). Some bits need optional peer
dependencies (GSAP, three.js) — those resolve through the already-pinned
`gsap@3.15.1` / `three@0.134.0` (Vanta pair) pins where the bit needs them,
never a new floating install. Bits that animate text or backgrounds respect
`prefers-reduced-motion: reduce` (static final state) — a bit with no
reduced-motion handling is not used. React Bits is a menu, never a default: a
bit is used only when the dealt theme calls for that exact effect.
Theme-match precondition: every bit must still match the dealt theme; a clash
is not applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the bit's animation is the motion decision, with exact props as
the values; Theme: the bit is theme-matched or not used; Texture: none — a bit
adds motion, not a surface treatment (background bits excepted: those ARE the
surface's texture, theme-matched); Visuals: the bit's effect is visible and
anchored, never decoration that obscures content; Techniques: copy-paste
source at the pinned commit, CLI install, peer deps through existing pins;
Colors: none — the bit's colours are the theme's own tokens.)

"""

LIB08 = """

**React Bits — React/Next only (fix #22 §11, REACTBITS_F22).** Animated React
components and backgrounds (text effects, backgrounds, components) from React
Bits are an approved menu item on React/Next.js builds only: copy-paste
source at the pinned repo commit
`9d9c687dc4f55b23539aa5417b703078047efa74` (MIT + Commons Clause — free inside
an app or product; the components themselves may not be sold, sublicensed, or
redistributed). Each bit is used as a §10 directive (component name + exact
props) with its fix #19 D19 reason. On any non-React stack the pattern is
re-implemented with the stack's own tools — never force React Bits outside
React. The primary home is `motion-patterns` (REACTBITS_F22); this skill
states the scope, it does not restate the install. Theme-match precondition: a
bit is applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`. (D19 — Motion: the bit's
animation is the motion decision; Theme: theme-matched or not used; Texture:
none — a bit adds motion, not a surface treatment (background bits excepted);
Visuals: the effect never obscures content; Techniques: copy-paste source at
the pinned commit; Colors: none — the bit's colours are the theme's own
tokens.)"""

CSV_GSAP_OLD = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"
CSV_GSAP_NEW = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.1/gsap.min.js"

# --- patch table: (id, rel, old, new, mode, token) ---
# mode: 'after' (old -> old+new), 'before' (old -> new+old), 'replace' (old -> new).
# token: a distinctive string of the new text that must be ABSENT from the
# original built file (idempotency / already-applied guard).

PG1_ANCHOR = """For the full rule list per category (all 120 UX guidelines with rationale), read `references/quick-reference.md`. For app-specific polish rules (icons, touch feedback, dark mode contrast, safe areas) and the canonical pre-delivery checklist, read `references/pro-rules.md`."""

LIB03_ANCHOR = """**Available stacks:** `react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `angular`, `laravel`, `swiftui`, `react-native`, `flutter`, `jetpack-compose`, `html-tailwind`, `shadcn`, `threejs`, `javafx`, `wpf`, `winui`, `avalonia`, `uno`, `uwp`. Use the stack detected in Step 1."""

REDUCED_MOTION_TAIL = "reduced-motion renders are exempt from the entrance itself but never from visibility."


# --- fix #22 §13-§17 additions (apply22.py) ---
DEPTH09 = """### Depth tokens — 3D motion values (fix #22 §13, DEPTH_F22)

```ts
// lib/motion-tokens.ts — depth values live beside motionTokens and are imported, never hardcoded (Rule 5).
export const depthTokens = {
  perspective: 1000, // px — the perspective distance for 3D-transform heroes; smaller reads deeper.
  parallax: { near: 0.5, mid: 0.25, far: 0.1 }, // scroll-linked translate multipliers: foreground moves most, background least.
  tilt: { max: 6 }, // degrees — maximum card tilt on pointer move; small, never a spin.
  elevation: { raised: 8, floating: 16, modal: 24 }, // px blur of the shadow that sells the height at each level (see ui-ux-pro-max depth rules, DEPTH_F22).
}
```

**3D motion rules.** Parallax distances, 3D transform values, and camera moves come from `depthTokens` (Rule 5: no inline numbers — depth values are token values too). A parallax layer moves at its `depthTokens.parallax` multiplier (`useScroll` + `useTransform`); a 3D-transform hero sets `perspective: depthTokens.perspective` on its parent and rotates on `rotateX` / `rotateY` within `depthTokens.tilt.max`; a camera move (Bang Motion §12, camera-through-world) travels through the layers at the parallax multipliers, never as a jump cut. Occlusion is real: a foreground layer may cover a background layer, and the covered content must never be the only copy of anything the user needs. Depth of field: background layers may blur while the foreground stays sharp — never the reverse. Under `prefers-reduced-motion: reduce` all depth motion is off — every layer renders at its final state immediately (same rule as Rule 3: all transforms disabled, opacity-only fades at ≤ 0.2s the only permitted fallback). A11 solid drawing in 3D (Principles above) binds here: an object keeps believable volume, weight, and depth while it moves.

- **D19 (for the depth tokens)** — Motion: the tokens are the values every depth move runs on, so parallax, tilt, and camera moves are decided once and reused; Theme: tokens are values, not looks — the theme still decides what the layered element is; Texture: none — depth tokens carry no surface treatment (Soft Shadow #23 is the texture-side depth cue, see `less-flat-ui` DEPTH_F22); Visuals: the multipliers keep near/mid/far layers legible (nothing moves so far it leaves the frame); Techniques: values live in `depthTokens` and are imported, never hardcoded (Rule 5); Colors: none — depth tokens do not choose colours; Depth: the tokens ARE the depth values — perspective, parallax distances, tilt, elevation blur.

- **Theme-match precondition:** tokens are numbers, not designs — every element moved under them must still match the dealt theme; a token applied in a way that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element."""
DEPTH10 = """### Parallax layers and 3D-transform hero (fix #22 §13, DEPTH_F22)

```tsx
"use client"
import { motion, useScroll, useTransform } from "motion/react"
import { depthTokens } from "@/lib/motion-tokens"

// Parallax: each layer translates at its depthTokens.parallax multiplier —
// foreground (near) moves most, background (far) moves least. The multipliers
// are the depth: 0.5 / 0.25 / 0.1, never per-layer improvisation (Rule 8).
const { scrollYProgress } = useScroll()
const yNear = useTransform(scrollYProgress, [0, 1], [0, -120 * depthTokens.parallax.near])
const yFar = useTransform(scrollYProgress, [0, 1], [0, 60 * depthTokens.parallax.far])
<motion.div style={{ y: yNear }} />  // foreground layer
<motion.div style={{ y: yFar }} />   // background layer
```

**3D-transform hero.** The hero sets `perspective: depthTokens.perspective`
(1000px) on its parent; the hero object rotates within
`depthTokens.tilt.max` (6°) on pointer move (`rotateX` / `rotateY`) and
settles on release. A flip or turn keeps the object's shadow, edge, and
layering consistent through the move (A11 solid drawing in 3D) — it never
flattens into a texture or shears. **Camera move (Bang Motion §12).** A
camera-through-world move travels through the layers at the parallax
multipliers — push-through, glide, settle — with a subject that persists
across the move; the camera is depth in motion, not a slide transition.
**Depth of field.** Background layers may blur while the foreground stays
sharp; never blur the layer the user must read. Under
`prefers-reduced-motion: reduce` none of this runs — every layer renders at
its final state immediately (see `motion-foundations` Rule 3). SCOPE:
motion-governed app surfaces only; Taste landing pages keep their standing
rule (`references/motion.md`: scrolling moves nothing but the dealt moment) —
a Taste depth moment is a dealt moment (DEPTH_F22 in
`design-taste-frontend`), not a scroll parallax.

- **D19 (for the parallax / 3D-hero patterns)** — Motion: the multipliers, the
perspective, and the tilt cap are the moving values; Theme: the layered hero
is the dealt theme's depth, never a stock parallax; Texture: none — the
patterns add no surface treatment; Visuals: near/mid/far layers stay legible
and the foreground never leaves the frame; Techniques: values come from
`depthTokens` (Rule 8), the camera move follows Bang Motion §12;
Colors: none — the patterns do not choose colours; Depth: the layer order,
parallax distances, and perspective value are the depth decision itself.

- **Theme-match precondition:** as AB-03 — every element moved under these
patterns must still match the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`."""
DEPTH11 = """

**Depth rules — the z-axis on app surfaces (fix #22 §13, DEPTH_F22).** Every app surface has a named depth strategy (orchestrate step 3, DEPTH_F22): flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world — recorded in `docs/design-tokens.md` alongside the other directives, with exact values per §10. The rules:

- **Elevation system.** Shadow levels ARE depth: raised (`depthTokens.elevation.raised`, 8px blur), floating (16px), modal (24px) — a shadow's blur sells the height. One shadow alone reads flat; layered shadows at different blurs read as real height (see Soft Shadow #23 in `less-flat-ui`, DEPTH_F22 — the texture-side depth cue). Elevation is directed: the level per element is named in the design package, never improvised.
- **Perspective.** 3D-transform surfaces set `perspective: depthTokens.perspective` (1000px) on the parent; smaller reads deeper. A surface with no perspective value has no 3D transforms.
- **Parallax.** Layers move at `depthTokens.parallax` multipliers (near 0.5 / mid 0.25 / far 0.1): foreground moves most, background least. Parallax is a depth decision with exact distances, never a decorative drift.
- **3D transforms.** Tilt and rotation stay within `depthTokens.tilt.max` (6°); a flip or turn keeps the object's shadow, edge, and layering consistent (A11 solid drawing in 3D). GSAP 3D transforms (§11) are the implementation on GSAP builds; `react-three-fiber` (§15) is the 3D layer on React builds; Vanta (§11, VANTA_F22 above) is the vanilla-JS 3D path.
- **Layering.** Every surface declares its layer order — foreground / midground / background — in the design package. The order is the depth strategy made explicit.
- **Occlusion.** A foreground layer may cover a background layer; the covered content must never be the only copy of anything the user needs, and an occluded control must never be the only path to an action.
- **Depth of field.** Background layers may blur while the foreground stays sharp; never blur the layer the user must read.
- **Theme-matched depth.** A brutalist theme's depth is hard offset shadows and stacked cards; a luxury theme's is soft elevation and slow parallax; a sticker theme's is die-cut layers and hard offset shadows. Depth treatment must match the theme deal, with a D19 reason.
- **Never hurts readability or performance.** Text over 3D/deep backgrounds needs a scrim and a 4.5:1 contrast check (same rule as §11 Vanta). 3D motion respects `prefers-reduced-motion: reduce` (static fallback or off) with a mobile/low-power fallback. A deep design that is unreadable or that stutters on a phone FAILS the check — the finding is candidate evidence for `browser-qa`, never a verdict of this skill. One WebGL-heavy effect per surface (§15): a surface never stacks two WebGL depth effects.

- **D19 (for the depth rules)** — Motion: the rules name how depth moves (parallax distances, camera moves, 3D transforms) or record `none — <reason>` for a still flat surface; Theme: the rules are applied in the dealt theme's depth (brutalist / luxury / sticker, above), never as a generic 3D effect; Texture: depth and texture are different axes — texture is the `less-flat-ui` layer, depth is the z-axis (Soft Shadow #23 is both); Visuals: layer order, occlusion, and depth of field keep the layered picture legible; Techniques: the rules route to depth tokens, Vanta, GSAP 3D, and the Bang Motion camera, never to ad-hoc values; Colors: depth treatments use the theme's own tokens; Depth: the rules ARE the depth axis — elevation, perspective, parallax, layering, occlusion, depth of field.

- **Theme-match precondition:** a depth treatment that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the surface."""
DEPTH12 = """

**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** App surfaces record the same seventh dimension as the full rule in `design-taste-frontend` step 4a (DEPTH_F22 there): every app-surface UI decision's recorded reason in MASTER.md addresses SEVEN dimensions, the six above plus **Depth** (the z-axis: layers, elevation, perspective, parallax, occlusion, depth of field — or `flat by choice — <reason>` where flat is the deliberate call). A MASTER.md entry is complete only when it carries all seven dimension lines. The six-dimension text above is unchanged; this line extends it."""
DEPTH13 = """

**Depth and texture are different axes (fix #22 §13, DEPTH_F22).** This skill owns texture — the 23 treatments. The z-axis is owned by the depth rules (`ui-ux-pro-max` depth rules, DEPTH_F22) and the depth tokens (`motion-foundations` depth tokens, DEPTH_F22): layers, elevation, perspective, parallax, occlusion. Overlap, recorded once here and not duplicated: Soft Shadow #23 is BOTH — a texture treatment in this catalogue AND a depth cue (its three layered shadows sell elevation). A shadow used as a depth cue still needs its depth strategy named in the design package (orchestrate step 3, DEPTH_F22); a treatment with no depth intent is texture only, and its Depth dimension line records `flat by choice — <reason>` or `none — <reason>` for the z-axis. (D19 — Motion: none — a shadow does not move; Theme: the shadow tint follows the dealt theme's surface; Texture: the shadow IS the texture treatment; Visuals: layered blurs read as real height where one shadow reads flat; Techniques: the three-layer `box-shadow` above, never two separate drop shadows; Colors: the shadow tint is the surface's own hue at low opacity; Depth: the shadow is the elevation cue — its blur is the height.)"""
ORBMP = """### Thinking Orb — the loading indicator for AI/agent waiting states (fix #22 §14, ORBS_F22)

The approved loading indicator for AI/agent waiting states is the Thinking
Orb (Jakub Antalik, `thinking-orbs@0.3.2`, MIT — see the pin record in
`ui-ux-pro-max`, ORBS_F22): a dotted orb on a plain 2D canvas, one distinct
hand-tuned animation per agent state — never a generic spinner. This is the
approved IMPLEMENTATION of Group D fix D19 "Add loading states" (polish-pass
unslop-fixes.md): the loading state for an AI/agent wait is an orb, not a
spinner, and the state must match what the agent is actually doing.

**The nine verified states (repo-verified — see the report §2; there is NO
"tenth" state and NO state named "thinking").** Each state is a distinct
animation, not a recolour:

| State | What the agent is doing | The animation does | Use it when |
|---|---|---|---|
| `working` | general activity | particles on tilted orbits | the agent is working and no narrower state fits |
| `searching` | retrieving | a scan meridian sweeps a dotted globe | retrieving / looking something up |
| `solving` | computing | bands scramble, then click back solved | computing / solving a problem |
| `listening` | capturing input | a waveform rolls through the rings | capturing input (voice, audio, live input) |
| `connecting` | establishing | a constellation wires itself | establishing a connection / handshake |
| `weaving` | combining | three strands plait around the sphere | combining / merging sources or results |
| `composing` | generating | an undulating multi-band sash | generating text, code, or media |
| `breathing` | idle / waiting | a ring slowly morphing | waiting with nothing active to report (idle hold) |
| `shaping` | transforming | dotted outline: circle → triangle → square | transforming / reshaping output |

**Correction to the SPEC §14 mapping draft:** the draft mapped "thinking =
reasoning". There is no `thinking` state in the library. Reasoning maps to
`working` (general activity) or `solving` (computing), whichever the moment
actually is. The `breathing` state's on-screen label reads "Thinking…" but
`breathing` is the IDLE/WAITING state — never use it for reasoning. A build
that shows a "thinking" orb while the agent reasons is a mismatched state.

**Sizes — two tuned presets, not a scale factor.** `size={64}` is the
chat-avatar scale (in agent messages, beside the agent's avatar or name);
`size={20}` is the inline-text scale (next to status text, e.g. "Searching…
<orb>"). Each size carries its own dot count, dot size, and speed tuning
(tokens in `motion-foundations`, ORBS_F22). Never scale an orb with CSS to
some other size — pick 64 or 20.

**Usage (React/Next):**

```tsx
import { ThinkingOrb } from 'thinking-orbs';

// Chat-avatar scale, in an agent message while the agent retrieves:
<ThinkingOrb state="searching" size={64} />

// Inline-text scale, next to status text:
<span>Searching… <ThinkingOrb state="searching" size={20} /></span>
```

`speed` is a multiplier on the preset's baked speed (`speed={1.5}` runs 1.5x
the baked speed). `paused` freezes on the current frame. Every orb carries
`role="img"` with a per-state `aria-label` out of the box ("Working…",
"Searching…", … — the `breathing` label reads "Thinking…"); pass an explicit
`aria-label` only to override it with the product's own status wording.

**Rules — state-matched, never decorative.**

- The orb state MUST match the actual agent activity. A `solving` orb while
  the app is just loading a page is a mismatched state. A generic spinner
  anywhere an AI/agent wait is shown is out — the orb replaces it.
- Menu, not defaults: use ONLY the states the product actually uses. A
  product that only ever retrieves and generates uses `searching` and
  `composing` — it does not ship all nine. The design package names the
  states the product uses (orchestrate step 3, ORBS_F22).
- Not decoration, not a brand mark: an orb never appears where nothing is
  waiting, never as a logo, never as a decorative background element.
- Not a general spinner: non-AI loading (page loads, file uploads, form
  submits with no agent behind them) does NOT use an orb — it uses the
  product's ordinary loading treatment. The orb is for AI/agent waits only.
- Monochrome + theme-matched: the orb takes the theme's ink colour (light
  ink on dark substrates, dark ink on light ones — `theme="auto"` detects
  from the host project; pin with `theme="dark"` / `theme="light"` where the
  substrate is fixed). Never a rainbow orb, never a brand-colour orb, never
  the accent colour — the ink is a neutral, never the accent.
- Cursor gravity is an OPTIONAL interactive extra, off by default: the
  `gravity={{ sprite }}` prop bends the pointer toward the orb, and it needs
  a pointer-raster `sprite` the package does NOT ship. It is documented in
  the author's Libraries.dev skill reference, NOT in the standalone repo's
  component at main — a build that wants it verifies the prop exists in the
  installed version first, and records a gap if it does not. Gravity turns
  itself off under reduced motion. Never a default, never required.
- Performance is the point (requirements, not options — tokens in
  `motion-foundations`, ORBS_F22): plain 2D canvas arcs only (no WebGL, no
  SVG filters, no `ctx.filter`); every instance pauses itself when scrolled
  offscreen (`IntersectionObserver`) or when the tab is hidden, then resumes
  in phase, and still paints one frame while paused; device-pixel-ratio
  capped at 2; `prefers-reduced-motion: reduce` renders a frozen one-frame
  orb (no animation) that still follows the live theme.

**Dry-run fixture check phrases (fixtures (a)–(e) judge against these):**
(a) "a generic spinner" FAILS — a build with a generic spinner for an
AI/agent wait FAILS the check. (b) "a state-matched orb" PASSES — a build
whose orb state matches the actual agent activity PASSES. (c) "a mismatched
orb state" FAILS — an orb whose state does not match the actual agent
activity FAILS. (d) "an orb used as decoration" FAILS — an orb shown where
nothing is waiting, or used as a logo or decorative element, FAILS.
(e) "an orb that does not respect reduced motion" FAILS — an orb that
animates under `prefers-reduced-motion: reduce` instead of rendering a
frozen one-frame orb FAILS.

- **D19 (for the orb pattern)** — Motion: the orb IS the waiting-state
motion — its state, size, and speed are the motion decision, and it pauses
offscreen/hidden and freezes under reduced motion; Theme: the orb takes the
theme's ink and is used only for the states the dealt theme's product
actually has, never as decoration; Texture: none — the orb is a canvas
animation, not a surface treatment; Visuals: the state-matched orb tells the
user what the agent is actually doing, where a generic spinner tells them
nothing; Techniques: the single approved implementation is
`thinking-orbs@0.3.2` on React/Next (ORBS_F22 pin in `ui-ux-pro-max`),
non-React stacks implement the pattern with their own tools; Colors: the
orb is strictly monochrome in the theme's ink — never a rainbow, brand, or
accent colour.

- **Theme-match precondition:** as AB-03 — every orb must still match the
dealt theme (its ink is the theme's ink); an orb in a colour that clashes
with the theme is not applied, and the reason is recorded in
`docs/design-tokens.md`."""
ORBMF = """### Thinking Orb tokens (fix #22 §14, ORBS_F22)

The tokens for the Thinking Orb pattern (`motion-patterns`, ORBS_F22). The
library ships nine states × two sizes as baked tunings (`src/presets.ts` in
the repo): each (state, size) pair resolves to an engine mode plus
speed/count/size multipliers over the mode's base profile, resolved once and
cached. The numbers below ARE the tokens — a build uses the library's baked
tunings, never re-tunes them per component.

**Sizes.** `64` = chat-avatar scale; `20` = inline-text scale. Two tuned
presets, not a scale factor: each size has its own dot count, dot size, and
speed tuning. The engine produces 24–600 dots per frame depending on state
and size. Never scale an orb with CSS to another size — pick 64 or 20.

**Per-state tunings (speed / count / size multipliers over the base profile;
`extra` where the mode carries one).** Verified live from
`src/presets.ts` (repo main, Nov 12, 2026):

| State (engine mode) | size 64 — speed / count / size | size 20 — speed / count / size |
|---|---|---|
| `working` (orbits) | 1.885 / 1 / 1 | 3.9 / 0.238 / 2.4 |
| `searching` (globe) | 2.015 / 0.42 / 1.15, extra scanMul 4.08, dimBase 0.45 | 2.665 / 0.105 / 1.75, extra scanMul 4.335, dimBase 0.45 |
| `solving` (rubik) | 1.82 / 0.35 / 1.05 | 1.95 / 0.088 / 1.9 |
| `listening` (wave) | 4.388 / 0.341 / 1 | 3.998 / 0.105 / 1.6 |
| `connecting` (web) | 3.315 / 1.35 / 0.95 | 6.63 / 0.25 / 1.52 |
| `weaving` (braid) | 1.625 / 0.5 / 1 | 2.75 / 0.1125 / 1.36 |
| `composing` (ribbon) | 2.34 / 0.25 / 0.85, extra spin 0, bandMul 3.9, wobMul 1 | 3.12 / 0.051 / 1.073, extra spin 0, bandMul 4.94, wobMul 1 |
| `breathing` (ring) | 3.24 / 0.25 / 0.956, extra spin 0, bandMul 3.627, wobMul 0.368 | 3.78 / 0.028 / 1.622, extra spin 0, bandMul 3.968, wobMul 0.565 |
| `shaping` (morph) | 2.405 / 0.702 / 0.395, extra spread 1.45 | 2.08 / 0.53 / 1.011, extra spread 1.45 |

**Speed multiplier.** The `speed` prop is a multiplier on the preset's baked
speed (`speed={1.5}` = 1.5x the baked speed). The baked speed is the default;
a build changes it only with a recorded reason (e.g. a deliberately slower
idle orb), never per component by taste.

**Monochrome rule.** Strictly monochrome: light ink on dark substrates, dark
ink on light ones. `theme="auto"` (default) resolves in three layers and
updates live: an ancestor `data-theme="dark|light"` attribute or `dark` /
`light` class (watched via `MutationObserver`); otherwise
`prefers-color-scheme`; SSR-safe (the canvas paints only on the client,
after the theme has resolved). Pin with `theme="dark"` / `theme="light"`
where the substrate is fixed. The ink is the theme's ink — never a rainbow,
brand, or accent colour.

**Reduced-motion behaviour — frozen one-frame orb.** Under
`prefers-reduced-motion: reduce` the orb renders ONE static representative
frame (frame at t=0.6 in the library) and does not animate — and still
follows the live theme. This is a requirement, not an option: an orb that
animates under reduced motion FAILS the check (fixture (e)).

**Offscreen / hidden pause.** Every instance pauses itself when scrolled
offscreen (`IntersectionObserver`) or when the tab is hidden
(`visibilitychange`), then resumes in phase — all instances share one clock.
A paused orb still paints one frame. This is a requirement, not an option.

**Device-pixel-ratio cap.** DPR is capped at 2 (`Math.min(2,
devicePixelRatio)` in the library). This is a requirement, not an option.

**Render budget.** Plain 2D canvas arcs only — no `ctx.filter`, no SVG
filters, no WebGL — the same pixels everywhere, cheap on low-end devices,
60 fps, minimal main-thread use. The heaviest state is under 1% of a 60 fps
frame budget in the library's own measurement; the plugin records the 2D
canvas + pause + DPR-cap requirements and does not re-measure them.

- **D19 (for the orb tokens)** — Motion: the tunings ARE the motion values —
baked per (state, size), speed a multiplier on them, pause offscreen/hidden,
frozen one frame under reduced motion; Theme: the monochrome rule is the
theme's ink, resolved live from the host project; Texture: none — tokens
carry no surface treatment; Visuals: two tuned sizes keep the orb legible at
avatar scale and inline scale, never a CSS-scaled blur; Techniques: the
tunings are the library's baked presets, imported, never re-tuned per
component; Colors: strictly monochrome ink — the tokens choose no colour
beyond the theme's ink.

- **Theme-match precondition:** as AB-03 — tokens are values, not designs;
every orb rendered with them must still match the dealt theme; a clash is
not applied, with the reason recorded in `docs/design-tokens.md`."""
ORBUIPRO = """
**Thinking Orb — the loading indicator component for AI/agent waiting states (fix #22 §14, ORBS_F22).** The component rules live here; the pattern lives in `motion-patterns` (ORBS_F22) and the tokens in `motion-foundations` (ORBS_F22). **Where it goes:** size 64 (chat-avatar scale) inside agent messages, beside the agent's avatar or name; size 20 (inline-text scale) next to status text ("Searching… <orb>"). **When to use it:** AI/agent waiting states only — while the agent is working, searching, solving, listening, connecting, weaving, composing, breathing (idle hold), or shaping, with the state matched to the actual activity. **When NOT to use it:** never as a general spinner for non-AI loading (page loads, uploads, form submits with no agent behind them — those use the product's ordinary loading treatment); never as decoration; never as a brand mark or logo. **Menu, not defaults:** only the states the product actually uses are shipped — the design package names them (orchestrate step 3, ORBS_F22). **Supply chain (pinned, verified live Nov 12, 2026):** `thinking-orbs@0.3.2` — exact pin in the project's `package.json` + lockfile; "latest" FAILS the pin check. The repo's `package.json` at main reads 0.3.1; 0.3.2 is the version published on npm (registry `latest`, verified Nov 12, 2026) — pin 0.3.2, the published version, not the repo's 0.3.1. License MIT, verified live (repo LICENSE + `package.json` `"license": "MIT"` + npm registry `"license": "MIT"`); free for commercial use. Peer dependency: React >= 18. **Stack scope:** React/Next via npm `thinking-orbs`. React Native: a package (`thinking-orbs-native`) exists IN the repo under `ports/react-native/`, is NOT published on npm, and has NOT run on a device or simulator yet — install-from-repo only, gated on that verification, never assumed shippable. SwiftUI: PLANNED only (`ports/ios/ThinkingOrbsKit` in the repo's port plan) — no Swift package exists in the repo; do not claim SwiftUI support until it ships. Non-React stacks implement the pattern with their own tools (same routing rule as React Bits, §11): the orb PATTERN (state-matched, monochrome, two sizes, pause + reduced-motion behaviour) is implemented natively, never by forcing the React package outside React. **Monochrome + theme-matched:** the orb takes the theme's ink colour, never a rainbow, brand, or accent colour. Theme-match precondition: an orb is applied only when it matches the dealt theme; a clash is not applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the orb is the waiting-state motion, state-matched and pausing offscreen/hidden; Theme: theme-matched ink, used only for the product's real agent states; Texture: none — the orb adds motion, not a surface treatment; Visuals: the orb sits at avatar or inline scale where the wait is, never as a decorative element; Techniques: the pinned npm package on React/Next, install-from-repo-gated on React Native, planned-only on SwiftUI, native re-implementation elsewhere; Colors: strictly monochrome theme ink, never the accent.)"""
L1501 = """
### React Three Fiber — the 3D implementation layer for React (fix #22 §15, R3F_F22)

React Three Fiber (R3F) is THE 3D implementation layer for React builds:
the §13 depth rules (3D transforms, parallax, camera moves) are implemented
through R3F on React builds. Vanta (§11) stays the vanilla-JS 3D path; R3F
is the React path. R3F is a React renderer for Three.js: JSX elements map
to Three.js objects declaratively (`<mesh />` becomes `new THREE.Mesh()`),
with no overhead (components render outside React). Ecosystem (menu, never
defaults): `@react-three/drei` helpers, Rapier physics, postprocessing, XR.
Install (exact pins, per project, install-on-demand): `npm install
three@0.185.1 @types/three@0.185.1 @react-three/fiber@9.8.2` on React 19,
`@react-three/fiber@8.18.0` on React 18. `three@0.185.1` is the plugin's
general three.js pin (`data/stacks/threejs.csv` row 1) — it satisfies the
R3F peer ranges (v9: `three >=0.156`; v8: `three >=0.133`) and the
ShaderGradient matrix (`three >=0.158.0`); it is NOT the Vanta-scoped
`three@0.134.0`, which governs Vanta scenes only. **Version pairing is
STRICT — check it before installing:** read the project's `package.json`
`react` version first, then install the matching R3F major. React 18 +
R3F v9 FAILS the pairing check. React 19 + R3F v8 FAILS the pairing check.
Next.js 15 App Router MUST use R3F v9 + React 19 (R3F v8 is structurally
incompatible with the App Router's vendored React 19). Directed per §10
(library + effect + exact parameters): a 3D scene is a `<Canvas>` with an
exact camera (`camera={{ position: [0, 0, 5], fov: 45 }}`), exact lights,
and exact motion values (see `motion-patterns`, R3F_F22) — never "a 3D
hero". Under `prefers-reduced-motion: reduce` the scene does not run — a
static image/poster of the finished scene shows instead. One WebGL-heavy
effect per surface (WEBGL_ONE_F22, see the `polish-pass` slop checklist):
an R3F scene counts as the surface's one effect. Theme-match
precondition: a 3D scene is applied only when it matches the dealt theme;
a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: R3F is how 3D motion (rotation, parallax, camera moves) is
implemented on React builds, with exact camera and motion values; Theme:
the scene is the dealt theme's depth, never a stock 3D demo; Texture:
none — R3F adds geometry and light, not a surface treatment (a glass or
gradient ground inside the scene is that library's own treatment);
Visuals: the scene is the hero's depth anchor, never behind unreadable
text (4.5:1 scrim/contrast check where text overlaps it); Techniques: R3F
at the paired pin, peer deps pinned with it, install-on-demand per
project; Colors: none — the scene's colours are the theme's own tokens.)"""
L1502 = """### 3D scene — React Three Fiber (fix #22 §15, R3F_F22)

A 3D scene on a React/Next.js build is built with React Three Fiber
(`@react-three/fiber` — see `motion-foundations`, R3F_F22, for the strict
version pairing: React 18 + R3F v9 FAILS the pairing check, React 19 +
R3F v8 FAILS the pairing check). The scene below is the pattern: a
`<Canvas>` with an exact camera and lights, a mesh whose rotation is
driven per frame. 3D motion values (rotation speed, camera position,
parallax distance) are §10 directives — exact numbers in the directive,
never prose. SCOPE — React/Next.js builds ONLY: on a non-React stack the
same depth is built with the stack's own tools or with Vanta (§11, the
vanilla-JS 3D path) — never force R3F outside React.

```tsx
"use client"
import { Canvas, useFrame } from "@react-three/fiber"
import { useRef } from "react"

// R3F_F22: the 3D scene pattern. Camera, lights, and motion values are
// exact (directed per §10); the mesh rotates 0.01 radians per frame.
function SpinningBox() {
  const ref = useRef()
  useFrame((state, delta) => (ref.current.rotation.y += delta * 0.6))
  return (
    <mesh ref={ref}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#ff5005" />
    </mesh>
  )
}

<Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
  <ambientLight intensity={Math.PI / 2} />
  <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
  <SpinningBox />
</Canvas>
```

**Parallax through the camera (fix #22 §13 depth).** Depth motion is a
camera move, not a layout shift: the camera's position (or a group's
position) moves with scroll or pointer, with exact distances in the
directive (e.g. `camera.position.z` from 5 to 3.5 across the scroll).
Under `prefers-reduced-motion: reduce` the Canvas does not mount — a
static image/poster of the finished scene renders in its place. An R3F
scene is the surface's one WebGL-heavy effect (WEBGL_ONE_F22) — it never
shares a surface with a Vanta scene, a ShaderGradient, liquid glass, or
liquid metal. Theme-match precondition: the scene must still match the
dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the per-frame rotation and the camera move are the 3D
motion values, exact in the directive; Theme: the scene is the dealt
theme's depth moment, never a stock spinning cube; Texture: none — the
scene adds geometry and light, not a surface treatment; Visuals: the
object stays visible and legible through the move (A11 solid drawing in
3D); Techniques: R3F at the paired pin, Canvas + useFrame, install-on-demand
per project; Colors: none — the scene's colours are the theme's own
tokens.)
"""
L1503 = """
**§15 design asset libraries — stack scope (fix #22 §15, R3F_F22 /
LIQGLASS_F22 / SHADERGRAD_F22 / LIQLOGO_F22).** Four more free libraries
are approved menu items, never defaults — each is chosen through the
skills, theme-matched, with a D19 reason, and directed per §10 (library +
effect name + exact parameters). Stack scope: **react-three-fiber**
(`@react-three/fiber@9.8.2` on React 19, `@react-three/fiber@8.18.0` on
React 18, MIT; peer deps `three@0.185.1` + `@types/three@0.185.1`) and
**ShaderGradient** (`@shadergradient/react@2.4.20`, ESM-only; MIT declared
in package.json + README but NO root LICENSE file — see the caveat below)
are React/Next.js ONLY — on any other stack the pattern is re-implemented
with the stack's own tools (see `motion-patterns`, R3F_F22 /
SHADERGRAD_F22). **liquid-glass-js** (repo commit
`78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package — copy
`container.js`, `button.js`, `glass.css` into the project) is vanilla JS
and available on every stack. **liquid-logo** (repo commit
`689bb38a1e0d5a6a8baf2d34847635eefde19994`; PolyForm Shield 1.0.0, not MIT)
is a STANDALONE TOOL, not a runtime dependency — it produces the animated
brand mark once (see `design-taste-frontend` step 4a, LIQLOGO_F22); it is
never installed as a project dependency. **One WebGL-heavy effect per
surface (WEBGL_ONE_F22):** a surface/page uses AT MOST ONE WebGL-heavy
library effect (an R3F scene, a Vanta scene, a ShaderGradient, liquid
glass, liquid metal). Stacking two or more WebGL-heavy effects on one
surface FAILS the `polish-pass` flag (see the slop checklist,
WEBGL_ONE_F22) — performance + "more, not bolder" restraint. Every library
effect respects `prefers-reduced-motion: reduce` (static fallback or off)
— no library exempts the rule. Unpinned versions ("latest") FAIL the pin
check. The pinned versions live here and in the owning skills; a build
that needs a newer version re-pins deliberately and records the new pin +
its verification, never floats. Theme-match precondition: a library effect
is applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the libraries are the 3D / gradient / glass / brand-motion
mechanisms, chosen per build; Theme: every effect is theme-matched or not
applied; Texture: ShaderGradient grounds and liquid glass ARE texture /
surface treatments chosen through the theme; Visuals: scope keeps effects
on the surfaces where they read (3D scenes on React heroes, glass on rich
backgrounds, gradients on landing heroes); Techniques: exact pins + stack
scope, install-on-demand per project (liquid-glass-js vendored file
copies, liquid-logo a standalone tool — see `fix22/libraries15-report.md`
§5 in the manifest record); Colors: none — the libraries choose no
colours (ShaderGradient colours come from the customize URL, which is the
theme's own palette).)

**ShaderGradient licence caveat (fix #22 §15, SHADERGRAD_F22).** The
ShaderGradient repo has NO root LICENSE file (verified live: no `LICENSE`
in the repo root, no licence field on the repo page). The MIT grant rests
on two declarations only: the README ("MIT © ruucm, stone-skipper") and
the `@shadergradient/react` package.json (`"license": "MIT"`). That is a
recorded caveat, not an assumed-away fact: if a build's legal review
needs actual licence text, the grant must be confirmed with the
maintainer before shipping — the plugin records the caveat and proceeds
on the declared MIT. Install `@shadergradient/react` (v2), NOT legacy
`shadergradient` (v1.3.5, dead end): a build installing legacy
`shadergradient` v1 FAILS the version check. The Figma plugin's paid Pro
tier is out of scope — the npm library is the integration, and it is free."""
L1504 = """
**Animated brand mark — liquid-logo, standalone tool (fix #22 §15,
LIQLOGO_F22).** Where a build wants its wordmark animated as liquid
metal, the approved production method is liquid-logo
(paper-design/liquid-logo, repo commit
`689bb38a1e0d5a6a8baf2d34847635eefde19994`; PolyForm Shield 1.0.0 — the
animated mark is a brand asset produced ONCE with the tool or its hosted
version at liquid.paper.design, exported as MP4/PNG, and shipped as an
asset; it is never a runtime dependency and never the only logo — the
original static logo is kept as the fallback for old phones and
non-WebGL contexts. The full rule (input requirements, the honest input
check, attribution) lives in `design-taste-frontend` step 4a (fix #20 B1,
LIQLOGO_F22); this skill states the app-surface use. Theme-match
precondition: the animated mark is the build's own brand, produced once
from its own wordmark — a liquid-metal treatment that clashes with the
dealt theme is not used, with the reason recorded in
`docs/design-tokens.md`. (D19 — Motion: the animation is the brand
motion, produced once, never runtime-heavy; Theme: the mark is the
build's own brand, theme-matched; Texture: none — the mark is an asset,
not a surface treatment; Visuals: the animated mark is the brand anchor,
the static logo is the fallback where it cannot play; Techniques:
standalone tool at the pinned commit, asset output only; Colors: none —
the metal is the shader's own chrome, the brand's colours are unchanged.)"""
L1506 = """**Liquid glass — real refraction (fix #22 §15, LIQGLASS_F22).** Fluted
glass (#2 above) is a frosted-blur approximation. Where a build needs
REAL refraction — Apple-style liquid glass with edge highlights, blur,
and masking through WebGL 2.0 shaders, not just `backdrop-filter` blur —
the approved implementation is liquid-glass-js (dashersw/liquid-glass-js,
repo commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package
— copy `container.js`, `button.js`, `glass.css` into the project; vanilla
JS, all stacks, no build step). Use for nav bars, floating cards, modals,
and CTA buttons over rich backgrounds. Directed per §10 (class + exact
parameters, from the library's own API): `new Container({ type: 'pill',
borderRadius: 24, tintOpacity: 0.3 })` for a nav pill, `new Button({
text: '<label>', size: 28, type: 'pill', tintOpacity: 0.4, warp: true,
onClick: <handler> })` for a glass CTA; global glass parameters via
`window.glassControls` (`edgeIntensity: 0.02, rimIntensity: 0.08,
blurRadius: 7.0, tintOpacity: 0.3` — the directed defaults, do not tune
per component). Shape types: `'rounded'` / `'circle'` / `'pill'`
(defaults: `borderRadius: 48`, `tintOpacity: 0.2`, `size: 48` for Button).
Performance note (from the README): the library samples the page with
html2canvas (`html2canvas@1.4.1`) — that sampling is the cost; keep glass
to one surface per screen by default and never stack it with another
WebGL-heavy effect (one WebGL-heavy effect per surface, WEBGL_ONE_F22 —
see the `polish-pass` slop checklist). Fallback: under
`prefers-reduced-motion: reduce`, on mobile/low-power, or whenever WebGL
is unavailable, the glass renders as frosted blur — treatment #2 fluted
glass above — never as a missing element. Text over glass keeps 4.5:1
contrast. Cross-reference, do not duplicate: Group E trend "Liquid Glass"
(E15, in `design-taste-frontend`) is the MENU item; this library is the
IMPLEMENTATION. Record the treatment per surface in
`docs/design-tokens.md` like every other treatment, with its six fix #19
D19 dimension lines.

(D19 — Motion: none — the glass does not move (its refraction is light,
not motion); Theme: the glass is the theme's own material, never a generic
blur wash; Texture: the glass IS the surface's texture layer (real
refraction, not a flat treatment); Visuals: the glass panel stays legible
— 4.5:1 over it, content above it; Techniques: vendored file copies at
the pinned commit, html2canvas@1.4.1 for page sampling, no npm package;
Colors: the glass tint is the theme's own tint, never a new colour.)"""
L1701 = """
### Particle backgrounds — Casberry, a standalone tool (fix #22 §17, CASBERRY_F22)

Where a build needs a bespoke particle scene — a hero or dealt moment the
libraries do not have (Vanta's named effects, a hand-built React Three
Fiber scene) — the approved production method is Casberry
(particles.casberry.in, "AI Particle Architect", free, no sign-up, no
install): a hosted tool that generates a live 20,000+ particle Three.js /
WebGL simulation from a prompt and exports React / Three.js code or a
standalone WebGL / HTML file, which is then dropped into the project.
Casberry is a STANDALONE TOOL, not a library to import and not a runtime
dependency — the plugin never imports it; it records the tool + the
export step (same form as liquid-logo, §15). Directed per §10: the agent
writes the prompt / spec with exact values (particle count, form, motion,
colours from the theme's own tokens, controls) and the tool generates;
the generated effect is reviewed against the theme and D19 before use.
The export is the surface's one WebGL-heavy effect (see the
`polish-pass` slop checklist, one-WebGL rule): a Casberry export never
shares a surface with a Vanta scene, a React Three Fiber scene, a
ShaderGradient, liquid glass, or liquid metal. Constraints, all binding:
theme-matched (particle colours are the theme's own tokens); a static
fallback (the theme's gradient or image ground) on mobile/low-power and
whenever WebGL is unavailable; the scene MUST disable under
`prefers-reduced-motion: reduce` (the finished still shows instead);
never behind text without a scrim and a 4.5:1 contrast check. TRUST FLAG
+ EXPORT REVIEW (binding): the domain carries a very low automated trust
score (ScamAdviser 1/100, WHOIS hidden, iframed — a weak automated
signal, NOT a verdict; a second checker rates it 60/100 with no malware
detected) and its terms / licence are UNRESOLVED (no terms or licence
statement found on the site as of Nov 13, 2026 — exported effects are
NOT assumed free for commercial use). Every exported snippet is
therefore treated as UNTRUSTED code: review every line before it enters
a build (same bar as the plugin's security re-scan — no document /
window / fetch / eval / network access, no obfuscated payloads), never
paste it blind; a Casberry export pasted without review FAILS the
security check (see the `polish-pass` slop checklist, export-review
check). Which 3D path to reach for: Vanta (§11) is the imported
3D-background LIBRARY for a known effect; Casberry is the TOOL that
exports Three.js code for a bespoke particle scene; React Three Fiber
(§15) is the React 3D layer the exported React code can feed and the
layer for hand-built React scenes. Theme-match precondition: a particle
scene is applied only when it matches the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the particle motion is the dealt moment's motion, with
exact values in the directing prompt; Theme: the scene is the dealt
theme's depth, never a stock particle demo; Texture: the particle field
is the surface's texture / depth layer; Visuals: the scene is the hero's
visual anchor, never behind unreadable text (4.5:1 scrim / contrast
check where text overlaps it); Techniques: standalone tool at
particles.casberry.in, exported code reviewed line by line before it
enters the build, no runtime dependency; Colors: none — the particle
colours are the theme's own tokens.)"""
L1702 = """### OriginKit — animated components, React/Next only (fix #22 §17, ORIGINKIT_F22)

OriginKit (originkit.dev) is a browsable catalog of animated React
components — backgrounds, cursor treatments, text effects, buttons,
loaders, image galleries — fetched by copy-paste from the site or
through its MCP server. The catalog is organised in 6 categories
(interactive elements, image galleries, text effects, animations,
background animations, buttons). COUNT NOTE (binding): the site's own
numbers disagree — the homepage says "Discover 805 Components" (Nov 13,
2026), the skill README says 50 across the 6 categories, the pricing
page says 60 components — the categories matter more than the exact
number; never cite a component count as exact. Stack: React, Tailwind
CSS, Framer Motion; usable in Framer, React, Next.js, Vite. SCOPE —
React/Next.js builds ONLY: on a non-React stack the PATTERN is
implemented with the stack's own tools (recorded-gap style: name the
closest equivalent — a CSS / GSAP / vanilla implementation of the same
effect — never force OriginKit outside React). Each component is used as
a §10 directive (component name + exact props, as listed for that
component on originkit.dev — the directive records the prop values, it
never says "a fluid-trail effect") with its fix #19 D19 reason, recorded
in `docs/design-tokens.md`. ACCESS + CAP (binding): browsing is free, no
API key. FETCHING component source requires a FREE API key
(originkit.dev > Settings > API Integration). DAILY LIMIT: 10 component
fetches per key per day, resets midnight UTC, shared between MCP and
website copies. A build needing more than 10 OriginKit fetches in a day
hits the cap: proceed from the skills alone, record the gap, never pay
for Pro ($79/yr) or Ultimate ($99/yr) — same form as Mobbin §9.
Pro-marked components are excluded on the free tier. API KEY HANDLING
(binding): the free key is an env var only, never written to any file
(same rule as the ElevenLabs narration key). NO MCP WIRING in the plugin:
the default is copy-paste from the site; the MCP server
(https://mcp.originkit.dev/mcp) is NOT wired in unless reachability +
env-only key flow are verified — that verification has NOT been done, so
copy-paste is the only wired path. LICENSE (binding): CONDITIONAL /
source-available — NOT a clean open-source licence. The terms restrict
redistribution of components and templates: components are for use in
your own project, not for redistribution, and the plugin must not
re-publish OriginKit components as its own. DISTINCTION CHECK (binding):
OriginKit (originkit.dev — animated flourishes) is NOT Origin UI
(originui.com, now coss ui / Base UI — solid form / layout primitives:
button, input, nav, card shells). A build citing Origin UI when it
means OriginKit (or vice versa) FAILS the distinction check. DEDUPE vs
React Bits (§11): React Bits is the importable MIT library (copy-paste
source at a pinned commit); OriginKit is the browsable catalog for
animated flourishes fetched by copy-paste or MCP. Reach for React Bits
when the build wants a pinned, importable bit; reach for OriginKit when
the build wants to browse a catalog for a flourish (background, cursor
treatment, text effect, button, loader) and fetch it. OriginKit
components are IMPLEMENTATIONS of motion patterns — the pattern stays
the authority, the component is the menu item. Components that animate
respect `prefers-reduced-motion: reduce` (static final state) — a
component with no reduced-motion handling is not used. OriginKit is a
menu, never a default: a component is used only when the dealt theme
calls for that exact effect. Theme-match precondition: every component
must still match the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the component's animation is the motion decision, with
exact props as the values; Theme: the component is theme-matched or not
used; Texture: none — a component adds motion, not a surface treatment
(background components excepted: those ARE the surface's texture,
theme-matched); Visuals: the component's effect is visible and anchored,
never decoration that obscures content; Techniques: copy-paste fetch at
the 10/day cap, env-only key, no MCP wiring; Colors: none — the
component's colours are the theme's own tokens.)

### Particle background — Casberry export (fix #22 §17, CASBERRY_F22)

A bespoke particle background on any stack is produced with Casberry
(particles.casberry.in) — see `motion-foundations` for the full rule:
the agent directs the prompt with exact values, exports React /
Three.js code or a standalone WebGL / HTML file, and drops it into the
project. The export is the surface's one WebGL-heavy effect and is
reviewed as untrusted code before it enters the build (same bar as the
plugin's security re-scan) — never pasted blind. Under
`prefers-reduced-motion: reduce` the scene does not run — a static
image / poster of the finished scene renders in its place. Theme-match
precondition: the particle scene must still match the dealt theme; a
clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the particle motion is the dealt moment's motion, exact
in the directing prompt; Theme: the scene is the dealt theme's depth
moment, never a stock particle demo; Texture: the particle field is the
surface's texture / depth layer; Visuals: the scene is the hero's visual
anchor, never behind unreadable text; Techniques: standalone tool,
exported code reviewed line by line, no runtime dependency; Colors:
none — the particle colours are the theme's own tokens.)
"""
L1703 = """
**§17 design asset libraries — stack scope (fix #22 §17, CASBERRY_F22 /
ORIGINKIT_F22 / DAISYUI_F22).** Three more free libraries / tools are
approved menu items, never defaults — each is chosen through the
skills, theme-matched, with a D19 reason, and directed per §10 (library
+ effect name + exact parameters). The three arrive in three different
integration forms: **daisyUI** (`daisyui@5.7.50`, MIT) is an npm plugin
dependency; **OriginKit** (originkit.dev; conditional / source-available
licence — see `motion-patterns`) is a browsable library fetched by
copy-paste (MCP not wired — see below); **Casberry**
(particles.casberry.in; terms unresolved — see
`motion-foundations`) is a standalone tool that exports code. Stack
scope: **daisyUI** is Tailwind builds ONLY (any framework, since it is
CSS) — daisyUI 5.x pairs with Tailwind CSS v4 ONLY (`@plugin "daisyui"`
in CSS; v4 class names changed from earlier versions — never mix
v4-era snippets with v5); **OriginKit** is React/Next.js ONLY
(Framer / React / Vite); **Casberry** exports are stack-independent
(the exported React code feeds the React 3D layer on React builds; the
standalone HTML file drops into any stack). Install (exact pins, per
project, install-on-demand): `npm i -D daisyui@5.7.50`, then `@import
"tailwindcss";` + `@plugin "daisyui";` in CSS. Caps + paid exclusions
(binding): OriginKit free tier — 10 component fetches per key per day
(resets midnight UTC, shared MCP + website copies), Pro-marked
components excluded, Pro ($79/yr) / Ultimate ($99/yr) never paid;
daisyUI free (MIT) — the Blueprint MCP server ($22/mo, paid licence
key) is NOT wired, and the paid Dashboard / Charts skills, Figma
library, and templates are out of scope; Casberry free, no sign-up —
terms unresolved, exports reviewed as untrusted code. Running total of
asset libraries / tools in fix #22: §11's 4 + §15's 4 + §17's 3 = 11.
Every library effect respects `prefers-reduced-motion: reduce` (static
fallback or off) — no library exempts the rule. Unpinned versions
("latest") FAIL the pin check. The pinned versions live here and in the
owning skills; a build that needs a newer version re-pins deliberately
and records the new pin + its verification, never floats. Theme-match
precondition: a library effect is applied only when it matches the
dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the libraries are the component / flourish / particle
mechanisms, chosen per build; Theme: every effect is theme-matched or
not applied; Texture: Casberry particle fields ARE texture / surface
treatments chosen through the theme; Visuals: scope keeps effects on
the surfaces where they read (daisyUI components on Tailwind builds,
OriginKit flourishes on React, particle scenes on heroes); Techniques:
exact pins + stack scope + caps, install-on-demand per project
(OriginKit copy-paste fetch, Casberry standalone tool — see
`fix22/libraries17-patches.md` §6 in the manifest record); Colors: none
— the libraries choose no colours (daisyUI themes are re-themed to the
brand deal; OriginKit and Casberry colours are the theme's own tokens).)"""
L1704 = """
### Component library menu — daisyUI (fix #22 §17, DAISYUI_F22)

On Tailwind builds, daisyUI (`daisyui@5.7.50`, MIT) is an approved menu
item for prebuilt components: semantic class names (`btn`, `card`,
`modal`, `toggle`, ...) on top of Tailwind utilities, plus built-in
themes; 68 components; 0 JavaScript shipped, 0 dependencies;
framework-agnostic (any framework, since it is CSS). Install (exact pin,
per project, install-on-demand): `npm i -D daisyui@5.7.50`, then
`@import "tailwindcss";` + `@plugin "daisyui";` in CSS. Version pairing
is PINNED: daisyUI 5.x + Tailwind CSS v4 ONLY — v4 class names changed
from earlier versions; never mix v4-era snippets with v5, and never
install daisyUI 4 against Tailwind v4. FIT-CHECK (binding): daisyUI has
a strong default look. Its components are a MENU of implementations,
re-themed through the brand / theme deal — the design package chooses
the direction; daisyUI supplies prebuilt components that get re-themed.
A build shipping daisyUI's default theme unexamined FAILS (generic look
— the Home Run lesson). DEDUPE vs shadcn: the plugin already pins
shadcn (`shadcn@4.23.0`, build.sh pin) as its React copy-paste
component set. Reach for daisyUI when the build is Tailwind-native and
wants semantic-class components with zero JS on any framework; reach
for shadcn when the build is React and wants the copy-paste component
set. The component primitives in this skill stay the authority — daisyUI
is the menu item, never the source of the primitives. Paid extras OUT
of scope: the Blueprint MCP server ($22/mo, paid licence key) is NOT
wired; Dashboard / Charts skills, the Figma library, and templates are
paid — out of scope. Theme-match precondition: a daisyUI component is
applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: none — daisyUI adds components, not motion (an animated
component on top of daisyUI is a motion-patterns decision); Theme: the
components are re-themed to the brand deal, never shipped in the
default theme; Texture: none — daisyUI adds component structure, not a
surface treatment; Visuals: semantic classes keep the markup readable
and the components consistent across the build; Techniques: exact pin +
Tailwind v4 pairing, install-on-demand per project; Colors: the theme
colours ARE the re-theme — the default theme's colours are never
shipped unexamined.)"""

DEMOGATE_B2S1 = """8. **Deploy via `deploy-fast`.** **Demo — never automatic (fix #22 /demo gate, DEMOGATE_B2S1_F22).** `/demo` is not filmed here."""
DEMOGATE_B2S2 = """Do NOT film via `/demo` here — `/demo` (`pitch-deck-video`) runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video). If the user asked for one, film the LOCAL app from the project dir after deploy (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it; the video file is `<app-name>-video/out/demo.mp4`. If no video was requested, the final report notes that no demo video was filmed. (fix #22 /demo gate, DEMOGATE_B2S2_F22)"""
DEMOGATE_B2S3 = """A filmed video shows the verified tree as it stands after any revert (see 6b) — a held redesign is never in the filmed tree. After deploy (and any requested filming), invoke `readme-writer` to write/update the README from the built app, before the final report in step 9 (fix #22 /demo gate, DEMOGATE_B2S3_F22)"""
DEMOGATE_B2S4 = """and, if a video was filmed, the demo-video handoff: the video file path (`<app-name>-video/out/demo.mp4`) plus the narration record (ElevenLabs usage remaining, narration status per line-set, the provider decision-log entries, and the music credit). If no video was filmed, the report notes that instead. (fix #22 /demo gate, DEMOGATE_B2S4_F22)"""
DEMOGATE_B2S5 = """If a video was filmed, the report also states the demo video handoff: the video file path (the local filmed video file) AND the instruction "upload this file to YouTube/Vimeo and paste the link into Devpost" — the first build never uploads the video anywhere (it has no YouTube/Devpost account access), so the file path + upload instruction is how the video reaches the submission. If no video was filmed, the report notes that no demo video was filmed. (fix #22 /demo gate, DEMOGATE_B2S5_F22)"""
DEMOGATE_B2C1 = """8. Deploy via `deploy-fast`. Do NOT film via `/demo` here — `/demo` runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video); if the user asked for one, film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report). (fix #22 /demo gate, DEMOGATE_B2C1_F22)"""
DEMOGATE_B3S1 = """After the redeploy, verify the deploy serves the new version (no removed feature, no dangling references) — UNLESS the deploy was already known-blocked (blocked-deploy handling above: no git-linked deploy, no deploy-fast path, or an unauthenticated deploy CLI): in that case skip the check entirely and note it in the final report. Otherwise take the deployed URL and deploy path from `.hackathon/run-ledger.md` (or `docs/final-report.md` if the ledger is absent), then poll the deployed app until it serves the new version, with a BOUNDED wait — check every ~30s, stop after ~5 minutes. If it never becomes ready in that bound, record the deploy as not-verified in the final report and move on — never wait unboundedly. (The poll verifies the redeploy; it is not a prelude to filming — no re-film happens here.) Then, before any future re-film, update `shots.json` FIRST — remove the feature's shots, selectors, and narration lines — then re-check every remaining shot against the updated demo storyboard in `docs/scope.md` (move the feature to the cut list first, so the storyboard is current): a shot whose feature was removed, or whose narration still promises the removed feature, is removed or rewritten before the re-film. If the user asks for a re-film, re-film via `/demo --rebuild`, which films the LOCAL app from the project dir (`APP_DIR`/project root), never a deployed URL; if the deploy was blocked, film local anyway and note in the final report that the video shows the local app, not the deployed one. (fix #22 /demo gate, DEMOGATE_B3S1_F22)"""
DEMOGATE_B3S2 = """**Narration continuity on a requested re-film (fix #22 /demo gate, DEMOGATE_B3S2_F22):** if the user asks for a re-film, narration lines that did not change are served from the per-line cache"""
DEMOGATE_B3S3 = """After a requested re-film, IF a hosted video link exists (in the Devpost submission, the README, or the final report) AND the agent has YouTube/Vimeo account access for that host, re-upload the new video (fix #22 /demo gate, DEMOGATE_B3S3_F22)"""
DEMOGATE_B3S4 = """the removal is done-with-blocked-re-upload, satisfied by the stale-video record (or the re-filmed LOCAL video, if the user asked for a re-film) plus this blocked record, not by a phantom upload (fix #22 /demo gate, DEMOGATE_B3S4_F22)"""
DEMOGATE_B3S5 = """The removal's done-condition for the video ("the demo video reflects the removal, or is flagged as stale") is satisfied by the re-filmed LOCAL video (if the user asked for a re-film) + the honest hosting note, or by the stale-video record when no re-film was requested — never by a phantom upload, never by an automatic re-film. (fix #22 /demo gate, DEMOGATE_B3S5_F22)"""
DEMOGATE_B3S6 = """a removal is not done until the deployed app, the ledger, and the inventory all reflect it, and the demo video is either re-filmed (on request) or flagged as stale; none of them may go stale silently. (fix #22 /demo gate, DEMOGATE_B3S6_F22)"""
DEMOGATE_B3S7 = """the re-uploaded video link if a hosted video existed and a re-film was requested (or the blocked re-upload record from step 5 if the re-upload was blocked for no account access), else the honest hosting note from step 5 — "video re-filmed locally at <path>, not yet hosted" if a re-film was requested, or "demo video STALE — shows the removed feature; re-film with `/demo --rebuild` on request" if not (fix #22 /demo gate, DEMOGATE_B3S7_F22)"""
DEMOGATE_B3C1 = """update `shots.json` (remove the feature's shots, selectors, and narration lines) so it is ready for a re-film, note in the final report that the demo video is now stale (re-film with `/demo --rebuild` only when the user asks), re-upload the video and update its link only if a re-film was requested and a hosted link exists, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal). (fix #22 /demo gate, DEMOGATE_B3C1_F22)"""

DEMOGATE_B2S6 = """it runs once, after deploy/commit/README, and never gates a feature. (fix #22 /demo gate, DEMOGATE_B2S6_F22)"""

DEMOGATE_B2S7 = """**Narration-key prompt — once, at the start of the standalone run, never blocking.** At the start of the run (step 1), if the user asked for a demo video and narration will need a key and none is set (no `ELEVENLABS_API_KEY` in the environment, no MiniMax credentials), issue the single `pitch-deck-video` narration-key prompt once. If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed (ElevenLabs free tier — 10,000 characters a month, no credit card — with the free-tier facts), then continue the build immediately without waiting: the prompt never blocks, the key is an env var only and is never written to any file, and if it never arrives the video renders music-only/silent with a note in the final report. This is the ONE sanctioned user prompt during the standalone run besides grill-me itself (hackathon-mode §7 carve-out) — never a wait point, never an approval gate. Do NOT re-prompt at `/demo` time: the single early prompt covers the run, and a user-invoked `/demo` uses the key if present, else falls back to music-only/silent. **Key handoff to a user-invoked `/demo`:** if the user replies with a key mid-run, hold it in working context ONLY and pass it to `/demo` via the dispatch if the user asks for a video: the `/demo` dispatch carries an explicit env instruction naming `ELEVENLABS_API_KEY` with the value held in working context, and the `/demo` executor runs the `tts` step with that variable set in its process environment — the key travels in the dispatch (working context), never in a file; `tts.mjs` reads it only from the environment. If the key arrives after the user-invoked `/demo` already rendered but before the step-9 final report, re-run the video script step (`npm run script` in the video project — tts + render) with the key set, so the delivered video is the narrated cut; if it arrives after the report, note the re-run command in the report with the key redacted (`ELEVENLABS_API_KEY=$KEY npm run script` in the video project dir — the user supplies their own key). (fix #22 /demo gate, DEMOGATE_B2S7_F22)"""

PATCHES = [
    # --- AB (Groups A+B + H1/H2) ---
    ("AB-01", MF, AB01_ANCHOR, AB01, "after", "PRINCIPLES_F22"),
    ("AB-02", MF, "## Core Concepts", AB02, "before", "LAWS_F22"),
    ("AB-03a", MF, "    fast:    0.18,", AB03A, "after", "dropdown: 0.2,"),
    ("AB-03b", MF, AB03A.strip(), AB03B, "after", "staggerRow: 0.03,"),
    ("AB-03c", MF, "    smooth: [0.22, 1, 0.36, 1],", AB03C_NEW, "replace",
     "the ease-out curve — entrances use this easing"),
    ("AB-03d", MF, "    linear: [0, 0, 1, 1],", AB03D, "after",
     "inOut:  [0.65, 0, 0.35, 1],"),
    ("AB-03e", MF, "    press:  0.95,", AB03E, "after", "popover: 0.95,"),
    ("AB-03f", MF, AB03F_OLD, AB03F_NEW + AB03_TAIL, "replace",
     "exitFactor: 0.8,"),
    ("AB-04", MF, REDUCED_MOTION_TAIL, AB04, "after",
     "Entrances ease out (fix #22 B1)"),
    ("AB-05", MP, REDUCED_MOTION_TAIL, AB05, "after",
     "Enter from the trigger (fix #22 B11"),
    ("AB-06", MP, "### Modal", AB06, "before", "### Dropdown (fix #22 B2)"),
    ("AB-07", MP, "### Toast stack", AB07, "before",
     "### Popover (fix #22 B10/B11/B12)"),
    ("AB-08", MP, "### Accordion", AB08, "before",
     "Reuse the same layoutId (fix #22 B20)"),
    ("AB-09", MA, "8. **SVG morphing requires equal path command counts.** Paths with different command structures snap instead of interpolating.",
     AB09, "after", "Overlap old & new states in multi-step sequences"),
    ("AB-10", MA, "### Cursor follower", AB10, "before",
     "### Mask reveal (fix #22 B17)"),
    ("AB-11", MIFB, "For React/Next.js motion implementation, see the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`) — this skill decides the feel/timing; they provide the tokens and patterns.",
     AB11, "after", "Motion feel decisions route through the principles (fix #22"),
    ("AB-12", UIPRO, "**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.",
     AB12, "after", "UX laws for motion decisions (fix #22"),
    ("AB-13", UIPRO, "One accent, one button pair, one card style: gates.md F4/F15 governs on landing pages, the Impeccable craft floor on app surfaces.",
     AB13, "after", "One accent colour (fix #22 H1"),
    ("AB-14", UIPRO, "Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable — this skill never states a screen pass/fail.",
     AB14, "after", "Accent hierarchy — every screen declares"),
    # --- CD pointers (Groups C+D) ---
    ("CD-P1", UIPRO_QR, "- `visual-hierarchy` - Establish hierarchy via size, spacing, contrast — not color alone",
     CD_P1, "after", "headline-specific"),
    ("CD-P2", UIPRO_QR, "- `primary-action` - Each screen should have only one primary CTA; secondary actions visually subordinate (Apple HIG)",
     CD_P2, "after", "cta-emphasis"),
    ("CD-P3", UIPRO_QR, "- `color-contrast` - Minimum 4.5:1 ratio for normal text (large text 3:1); Material Design",
     CD_P3, "after", "color-contrast-polish"),
    ("CD-P4", UIPRO_QR, "- `heading-line-balance` - Use balanced wrapping on short headings as a progressive, user-agent-controlled heuristic; keep natural wrapping readable and never force final words together with blanket nonbreaking spaces",
     CD_P4, "after", "headline-wrap-polish"),
    ("CD-P5", UIPRO_QR, "- `number-tabular` - Use tabular/monospaced figures for data columns, prices, and timers to prevent layout shift",
     CD_P5, "after", "tabular-polish"),
    ("CD-P6", UIPRO_QR, "- `whitespace-balance` - Use whitespace intentionally to group related items and separate sections; avoid visual clutter (Apple HIG)",
     CD_P6, "after", "spacing-group-polish"),
    ("CD-P7a", MP, P7A_ANCHOR, CD_P7A, "after",
     "Animate useful feedback only (UNSLOP_F22 D20"),
    ("CD-P7b", MF, "| `crawl` | Deliberate storytelling; use sparingly |",
     CD_P7B, "after", "Feedback animation (UNSLOP_F22 D20)"),
    # --- G pointers (glossary) ---
    ("G-P-G1", UIPRO, PG1_ANCHOR, G_PG1, "after",
     "Design vocabulary — the definitions of kerning"),
    ("G-P-G2", MF, PG2_ANCHOR, G_PG2, "after",
     "the definition of interruptible animation (G18)"),
    ("G-P-G3", MP, PG3_ANCHOR, G_PG3, "after",
     "the definitions of origin-aware animation (G10)"),
    # --- Process patches (Mobbin §9 + directives §10) ---
    ("PROC-P1", UIPRO, "**Generated direction — never based on a searched reference.** Web search may inform facts (real product details, competitor awareness) but never the design direction: no design may be based off a searched external reference — not a marketing website, not a Dribbble shot, not a template, not any found page.",
     PROC_P1, "after", "MOBBIN_PATTERN_F22"),
    ("PROC-P2", UIPRO, "**Every component is an experience (fix #20 X1, app surfaces).** On app surfaces, each component is designed as a moment/interaction, not a static functional block; every component entry in MASTER.md states the experience it creates (what it feels like, what moment it is) alongside its six fix #19 D19 dimension lines. A component recorded only as a functional block is an incomplete build. The full X1 rule lives in `design-taste-frontend` step 4a.",
     PROC_P2, "after", "Component specs are directives, not descriptions (fix #22 §10"),
    ("PROC-P3", GAN_PLANNER, P3_ANCHOR, PROC_P3, "after",
     "the Design Direction section above is recorded as DIRECTIVES"),
    ("PROC-P4", GAN_GENERATOR, "6. **Keep the dev server running** — The Evaluator needs a live app to test.",
     PROC_P4, "after", "the spec's design decisions are DIRECTIVES with exact values"),
    ("PROC-P5", GAN_EVALUATOR, "Write feedback to `gan-harness/feedback/feedback-NNN.md`:",
     PROC_P5, "after", "Feedback items are directives, not descriptions (fix #22 §10"),
    # --- Libraries (§11) ---
    ("LIB-01", MF, "- The animation is purely decorative with no UX purpose",
     LIB01, "after", "### Smooth scroll — Lenis (fix #22 §11"),
    ("LIB-02", MP, LIB02_ANCHOR, LIB02, "after",
     "Scroll-driven animation routes through Lenis + ScrollTrigger"),
    ("LIB-03", UIPRO, LIB03_ANCHOR, LIB03, "after",
     "Design asset libraries — stack scope (fix #22 §11"),
    ("LIB-04", UIPRO, LIB04_ANCHOR, LIB04, "after",
     "GSAP is the animation engine; ScrollTrigger is its scroll plugin"),
    ("LIB-06", UIPRO, LIB06_ANCHOR, LIB06, "after",
     "Animated 3D backgrounds — Vanta, on app surfaces"),
    ("LIB-07", MP, "## End-to-End Example", LIB07, "before",
     "### React Bits — animated components, React/Next only"),
    ("LIB-08", UIPRO, "Domain is auto-detected from the query if `--domain` is omitted — but auto-detection can misroute overlapping terms (e.g. \"font\" matches both `typography` and `google-fonts`). If results look off-topic, pass `--domain` explicitly.",
     LIB08, "after", "React Bits — React/Next only (fix #22 §11"),
    # --- three.js data file: stale GSAP CDN pin 3.12.2 -> 3.15.1 ---
    ("CSV-GSAP", THREEJS_CSV, CSV_GSAP_OLD, CSV_GSAP_NEW, "replace",
     "gsap/3.15.1/gsap.min.js"),
    # --- Sweep #30 Finding 1: group anchor labels (insertion only) ---
    # MUST stay after AB-05 / AB-09 in list order: the AB-05g / AB-09g
    # anchors are lines those patches insert (AB-03g's anchor is
    # pre-existing). Each inserts ONLY its anchor token as a group label.
    ("AB-03g", MF, "export const motionTokens = {", AB03G, "before",
     "ANIM_TOKENS_F22"),
    ("AB-05g", MP, "11. **Enter from the trigger (fix #22 B11 — origin-aware animation, glossary G10).**",
     AB05G, "before", "ANIM_RULES_F22"),
    ("AB-09g", MA, "9. **Overlap old & new states in multi-step sequences (fix #22 B16).** In an imperative",
     AB09G, "before", "ANIM_ADV_F22"),
    ('DEPTH-09', MF, 'export const springs = {', DEPTH09, 'before', 'DEPTH_F22'),
    ('DEPTH-10', MP, '### Expanding card', DEPTH10, 'before', 'DEPTH_F22'),
    ('DEPTH-11', UIPRO, "(D19 — Motion: the scene's motion is the dealt moment's motion; Theme:\ntheme-matched, colours are the theme's own tokens; Texture: the animated\nground is the surface's texture layer; Visuals: the scene is the hero anchor,\nnever behind unreadable text; Techniques: Vanta + three.js at the pinned pair,\ndestroy on unmount; Colors: effect colours are the theme's own tokens.)", DEPTH11, 'after', 'DEPTH_F22'),
    ('DEPTH-12', UIPRO, 'The full D19 rule lives in `design-taste-frontend` step 4a.', DEPTH12, 'after', 'DEPTH_F22'),
    ('DEPTH-13', LFUI, 'Layers with everything: a shadow is a depth cue, not a pattern, so it stacks on top of any other treatment without competing.', DEPTH13, 'after', 'DEPTH_F22'),
    ('ORB-MP', MP, '### Toast stack', ORBMP, 'before', 'ORBS_F22'),
    ('ORB-MF', MF, '### Accessibility', ORBMF, 'before', 'ORBS_F22'),
    ('ORB-UIPRO', UIPRO, 'One accent, one button pair, one card style: gates.md F4/F15 governs on landing pages, the Impeccable craft floor on app surfaces.', ORBUIPRO, 'after', 'ORBS_F22'),
    ('L15-01', MF, '- **A11 Solid drawing in 3D** — an object keeps believable volume, weight, and depth\n  while it moves. In UI: a card that flips or expands keeps its shadow, edge, and\n  layering consistent through the move; it never flattens into a texture or shears.', L1501, 'after', 'R3F_F22'),
    ('L15-02', MP, '## End-to-End Example', L1502, 'before', 'R3F_F22'),
    ('L15-03', UIPRO, 'library effect is applied only when it matches the dealt theme; a clash is not\napplied, with the reason recorded in `docs/design-tokens.md`.', L1503, 'after', 'R3F_F22'),
    ('L15-04', UIPRO, 'A build with no recorded brand identity is an incomplete build. The full B1 rule lives in `design-taste-frontend` step 4a.', L1504, 'after', 'LIQLOGO_F22'),
    ('L15-06', LFUI, '### 3. Thermal gradients', L1506, 'before', 'LIQGLASS_F22'),
    ('VERCEL-02', PP, 'Also read the slop checklist ([reference/slop-checklist.md](reference/slop-checklist.md), `SLOP_F22`) and apply its fixes from [reference/unslop-fixes.md](reference/unslop-fixes.md) (`UNSLOP_F22`) on every pass', " Also read the Vercel checklist ([reference/vercel-checklist.md](reference/vercel-checklist.md), `VERCEL_F22`) and apply its fix guidance on every pass — the checklist's findings are static checks producing candidate evidence for `browser-qa`, never verdicts, and a finding is cleared only by a recorded D19 reason + theme-fit.", 'after', 'VERCEL_F22'),
    ('VERCEL-03', PP, 'After the detector runs, run the slop checklist ([reference/slop-checklist.md](reference/slop-checklist.md), `SLOP_F22`) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and fix flagged instances with [reference/unslop-fixes.md](reference/unslop-fixes.md) (`UNSLOP_F22`).', ' Then run the Vercel checklist ([reference/vercel-checklist.md](reference/vercel-checklist.md), `VERCEL_F22`) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and fix flagged instances with its paired fix guidance, or clear them with a recorded D19 reason + theme-fit.', 'after', 'VERCEL_F22'),
    ('VERCEL-04', UIPRO_QR, '- `aria-labels` - aria-label for icon-only buttons; accessibilityLabel in native (Apple HIG)', '\n- `vercel-a11y-check` - Accessibility, focus, and form rules are checked in a polish pass against the pinned Vercel checklist (VERCEL_F22): labels, keyboard handlers, semantic elements, alt text, live regions, focus visibility, autocomplete, paste, spellcheck, error placement (V-A1–V-A12, V-F1–V-F5, V-FO1–V-FO11) — this skill states the patterns, the checklist is the check (fix #22)', 'after', 'vercel-a11y-check'),
    ('VERCEL-05', UIPRO_QR, '- `touch-target-size` - Min 44×44pt (Apple) / 48×48dp (Material); extend hit area beyond visual bounds if needed', '\n- `vercel-touch-check` - Touch, safe-area, and drag rules are checked in a polish pass against the pinned Vercel checklist (VERCEL_F22): touch-action, tap highlight, overscroll, drag alternatives, autoFocus, safe-area insets (V-TO1–V-TO7, V-S1–V-S3) — this skill states the sizes, the checklist is the check (fix #22)', 'after', 'vercel-touch-check'),
    ('VERCEL-06', UIPRO_QR, '- `number-tabular` - Use tabular/monospaced figures for data columns, prices, and timers to prevent layout shift', '\n- `vercel-type-check` - Typography and copy rules are checked in a polish pass against the pinned Vercel checklist (VERCEL_F22): ellipsis, curly quotes, non-breaking spaces, loading ellipsis, tabular figures, balanced headings, active voice, Title Case, numerals, specific labels, error next-steps (V-T1–V-T6, V-CC1–V-CC7) — this skill states the type scale, the checklist is the check (fix #22)', 'after', 'vercel-type-check'),
    ('VERCEL-07', MF, '4. **Never animate layout properties.** `width`, `height`, `top`, `left`, `margin`, `padding` are banned from `animate`. Use `transform` and `opacity` only.', '\n\nAnimation rules are also checked in a polish pass against the pinned Vercel checklist (VERCEL_F22): reduced-motion, transform/opacity-only, no `transition: all`, transform-origin, SVG `<g>` transforms, interruptible animations, autoplay controls (V-AN1–V-AN8) — this skill states the tokens and rules, the checklist is the file:line check (fix #22).', 'after', 'VERCEL_F22'),
    ('L17-01', MF, '- **A11 Solid drawing in 3D** — an object keeps believable volume, weight, and depth\n  while it moves. In UI: a card that flips or expands keeps its shadow, edge, and\n  layering consistent through the move; it never flattens into a texture or shears.', L1701, 'after', 'CASBERRY_F22'),
    ('L17-02', MP, '## End-to-End Example', L1702, 'before', 'ORIGINKIT_F22'),
    ('L17-03', UIPRO, "The Figma plugin's paid Pro\ntier is out of scope — the npm library is the integration, and it is free.", L1703, 'after', 'DAISYUI_F22'),
    ('L17-04', DS, 'Output: `DESIGN.md` + `design-tokens.json` + `design-preview.html`', L1704, 'after', 'DAISYUI_F22'),
    ("DEMOGATE_B2S1", "skills/orch-build-mvp/SKILL.md", '8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.**', DEMOGATE_B2S1, "replace", "DEMOGATE_B2S1_F22"),
    ("DEMOGATE_B2S2", "skills/orch-build-mvp/SKILL.md", 'then film the LOCAL app from the project dir (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it. The demo video is a required deliverable; its file is `<app-name>-video/out/demo.mp4`.', DEMOGATE_B2S2, "replace", "DEMOGATE_B2S2_F22"),
    ("DEMOGATE_B2S3", "skills/orch-build-mvp/SKILL.md", '`/demo` films the verified tree as it stands after any revert (see 6b) — a held redesign is never in the filmed tree. After filming, invoke `readme-writer` to write/update the README from the built app, before the final report in step 9', DEMOGATE_B2S3, "replace", "DEMOGATE_B2S3_F22"),
    ("DEMOGATE_B2S4", "skills/orch-build-mvp/SKILL.md", 'and the demo-video handoff: the video file path (`<app-name>-video/out/demo.mp4`) plus the narration record (ElevenLabs usage remaining, narration status per line-set, the provider decision-log entries, and the music credit).', DEMOGATE_B2S4, "replace", "DEMOGATE_B2S4_F22"),
    ("DEMOGATE_B2S5", "skills/orch-build-mvp/SKILL.md", 'The report also states the demo video handoff: the video file path (the local filmed video file) AND the instruction "upload this file to YouTube/Vimeo and paste the link into Devpost" — the first build never uploads the video anywhere (it has no YouTube/Devpost account access), so the file path + upload instruction is how the video reaches the submission.', DEMOGATE_B2S5, "replace", "DEMOGATE_B2S5_F22"),
    ("DEMOGATE_B2C1", "commands/orch-build-mvp.md", '8. Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — the demo video is a required deliverable; film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report).', DEMOGATE_B2C1, "replace", "DEMOGATE_B2C1_F22"),
    ("DEMOGATE_B3S1", "skills/orch-change-feature/SKILL.md", "After the redeploy, wait for the deploy to be ready before re-filming — UNLESS the deploy was already known-blocked (blocked-deploy handling above: no git-linked deploy, no deploy-fast path, or an unauthenticated deploy CLI): in that case skip the poll entirely, film local immediately, and note it in the final report — polling a URL that can never become ready burns up to ~5 minutes for nothing. Otherwise take the deployed URL and deploy path from `.hackathon/run-ledger.md` (or `docs/final-report.md` if the ledger is absent), then poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes. If it never becomes ready in that bound, film local and note it in the final report — never film a stale deployed URL, and never wait unboundedly. Then, before re-filming, update `shots.json` FIRST relative to the re-film — remove the feature's shots, selectors, and narration lines (FIRST means first before the re-film, not first in this step overall: the push/re-deploy above precedes it) — then re-check every remaining shot against the updated demo storyboard in `docs/scope.md` (move the feature to the cut list first, so the storyboard is current): a shot whose feature was removed, or whose narration still promises the removed feature, is removed or rewritten before the re-film — then re-film via `/demo --rebuild`, which films the LOCAL app from the project dir (`APP_DIR`/project root), never a deployed URL; if the deploy was blocked, film local anyway and note in the final report that the video shows the local app, not the deployed one.", DEMOGATE_B3S1, "replace", "DEMOGATE_B3S1_F22"),
    ("DEMOGATE_B3S2", "skills/orch-change-feature/SKILL.md", '**Narration continuity on the re-film:** narration lines that did not change are served from the per-line cache', DEMOGATE_B3S2, "replace", "DEMOGATE_B3S2_F22"),
    ("DEMOGATE_B3S3", "skills/orch-change-feature/SKILL.md", 'After re-filming, IF a hosted video link exists (in the Devpost submission, the README, or the final report) AND the agent has YouTube/Vimeo account access for that host, re-upload the new video', DEMOGATE_B3S3, "replace", "DEMOGATE_B3S3_F22"),
    ("DEMOGATE_B3S4", "skills/orch-change-feature/SKILL.md", 'the removal is done-with-blocked-re-upload, satisfied by the re-filmed LOCAL video plus this blocked record, not by a phantom upload', DEMOGATE_B3S4, "replace", "DEMOGATE_B3S4_F22"),
    ("DEMOGATE_B3S5", "skills/orch-change-feature/SKILL.md", 'The removal\'s done-condition ("the demo video reflects the removal") is satisfied by the re-filmed LOCAL video + the honest hosting note, not by a phantom upload.', DEMOGATE_B3S5, "replace", "DEMOGATE_B3S5_F22"),
    ("DEMOGATE_B3S6", "skills/orch-change-feature/SKILL.md", 'a removal is not done until the deployed app, the demo video, the ledger, and the inventory all reflect it; none of them may go stale.', DEMOGATE_B3S6, "replace", "DEMOGATE_B3S6_F22"),
    ("DEMOGATE_B3S7", "skills/orch-change-feature/SKILL.md", 'the re-uploaded video link if a hosted video existed (or the blocked re-upload record from step 5 if the re-upload was blocked for no account access), else the honest hosting note from step 5 — "video re-filmed locally at <path>, not yet hosted"', DEMOGATE_B3S7, "replace", "DEMOGATE_B3S7_F22"),
    ("DEMOGATE_B3C1", "commands/orch-change-feature.md", 'update `shots.json` before re-filming, re-film locally via `/demo --rebuild`, re-upload the video and update its link, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal).', DEMOGATE_B3C1, "replace", "DEMOGATE_B3C1_F22"),
    ("DEMOGATE_B2S6", "skills/orch-build-mvp/SKILL.md", 'it runs once, after deploy/demo/commit/README, and never gates a feature.', DEMOGATE_B2S6, "replace", "DEMOGATE_B2S6_F22"),
    ("DEMOGATE_B2S7", "skills/orch-build-mvp/SKILL.md", '**Narration-key prompt — once, at the start of the standalone run, never blocking.** At the start of the run (step 1), if narration will need a key and none is set (no `ELEVENLABS_API_KEY` in the environment, no MiniMax credentials), issue the single `pitch-deck-video` narration-key prompt once (ElevenLabs free tier — 10,000 characters a month, no credit card — with the free-tier facts), then continue the build immediately without waiting: the prompt never blocks, the key is an env var only and is never written to any file, and if it never arrives the video renders music-only/silent with a note in the final report. This is the ONE sanctioned user prompt during the standalone run besides grill-me itself (hackathon-mode §7 carve-out) — never a wait point, never an approval gate. Do NOT re-prompt at step 8 `/demo` time: the single early prompt covers the run, and `/demo` uses the key if present, else falls back to music-only/silent. **Key handoff to step 8:** if the user replies with a key mid-run, hold it in working context ONLY and pass it to the step-8 `/demo` via the dispatch: the step-8 dispatch carries an explicit env instruction naming `ELEVENLABS_API_KEY` with the value held in working context, and the `/demo` executor runs the `tts` step with that variable set in its process environment — the key travels in the dispatch (working context), never in a file; `tts.mjs` reads it only from the environment. If the key arrives after step 8 already rendered but before the step-9 final report, re-run the video script step (`npm run script` in the video project — tts + render) with the key set, so the delivered video is the narrated cut; if it arrives after the report, note the re-run command in the report with the key redacted (`ELEVENLABS_API_KEY=$KEY npm run script` in the video project dir — the user supplies their own key).', DEMOGATE_B2S7, "replace", "DEMOGATE_B2S7_F22"),
]

BANG_PIN_LINES = (
    'BANG_PIN="%s"\n'
    "# bangtutorial/bang-motion — MIT, no tags; SHA is the only pin available.\n"
    "# Record-only pin: the repo is NOT cloned at build time (no fetch_repo\n"
    "# call); Bang Motion's rules are ported into pitch-deck-video (fix #22\n"
    "# §12). The pin freezes the port's source so it stays auditable.\n"
    % BANG_SHA
)
BANG_PIN_ANCHOR = 'AGENTSKILLS_PIN="c13e8b35d44085accc7ec3b1b4410247d4969514"'


def build_sh_block():
    """The fix22 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix22: weave 7 @charles.unemployed reels (142 items) + H1/H2 accents + Mobbin + directives + 4 libraries + Bang Motion port ---")
    lines.append("# (motion-*, make-interfaces-feel-better, ui-ux-pro-max, GAN agents and")
    lines.append("#  ui-ux-pro-max data files are upstream/ECC; they have no staged source")
    lines.append("#  and are patched here. The staged-source halves -- orchestrate,")
    lines.append("#  design-taste-frontend (+ 15 Hallmark themes + glossary), polish-pass")
    lines.append("#  (slop checklist + unslop fixes + wiring), pitch-deck-video (Bang port)")
    lines.append("#  -- were applied directly to their sources by the wave-1 agents.")
    lines.append("#  All anchors were verified count==1 against the post-fix21 built tree")
    lines.append("#  by fix22/fix22.py's preflight (in-memory simulation, in list order);")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly")
    lines.append("#  on mismatch. Three token conflicts from ab-patches.md are carried")
    lines.append("#  unresolved in the comments (B3 30ms vs Rule 5 floor; B15 0.8x vs")
    lines.append("#  exit-faster ~60-70%; B4 0.97 vs scale.press 0.95) — the parent")
    lines.append("#  adjudicates. GSAP converges on 3.15.1; three.js is scoped (Vanta")
    lines.append("#  0.134.0, general 0.185.1, Bang's 0.161.0 recorded as Bang's only).")
    lines.append("# Placement: before STEP 5 (after the fix21 block).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for pid, rel, old, new, mode, _token in PATCHES:
        lines.append("  (%s, %s, %s, %s, %s),  # %s" % (
            repr(pid), repr(rel), repr(old), repr(new), repr(mode), repr(pid)))
    lines.append("]")
    lines.append("for pid, rel, old, add, mode in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix22 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    if mode == 'after':")
    lines.append("        new = old + add")
    lines.append("    elif mode == 'before':")
    lines.append("        new = add.rstrip('\\n') + '\\n\\n' + old")
    lines.append("    else:  # replace")
    lines.append("        new = add")
    lines.append("    open(p, \"w\").write(t.replace(old, new))")
    lines.append("print(\"fix22 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def _apply_patch(text, old, new, mode):
    if mode == "after":
        return text.replace(old, old + new)
    if mode == "before":
        return text.replace(old, new.rstrip("\n") + "\n\n" + old)
    return text.replace(old, new)  # replace


def preflight(allow_bang_pin=False, already=()):
    """Check every anchor count==1 (in-memory simulation, in list order)
    before writing anything. FAIL LOUDLY on any mismatch.

    `already`: patch ids present in a previous build.sh fix22 block (a
    re-run with new patches appended, Sweep #30). Those patches are
    skipped in the simulation — the current built tree already carries
    them — but their token MUST still be in the built file, or the tree
    is inconsistent with build.sh and the run fails loudly."""
    originals = {}
    sim = {}
    for _pid, rel, _old, _new, _mode, _token in PATCHES:
        if rel not in originals:
            path = os.path.join(BUILT, rel)
            originals[rel] = open(path, encoding="utf-8").read()
            sim[rel] = originals[rel]
    failures = []
    for pid, rel, old, new, mode, token in PATCHES:
        if pid in already:
            # Already applied in a previous run: token must still be in
            # the built file; the patch itself is not re-simulated.
            if token not in originals[rel]:
                failures.append((pid, rel, "ALREADY-BUT-TOKEN-MISSING", token))
            continue
        # Idempotency guard: the new text must not already be in the file.
        if token in originals[rel]:
            failures.append((pid, rel, "TOKEN-ALREADY-PRESENT", token))
            continue
        n = sim[rel].count(old)
        if n != 1:
            failures.append((pid, rel, "ANCHOR-COUNT=%d" % n, old[:100]))
            continue
        sim[rel] = _apply_patch(sim[rel], old, new, mode)
    # build.sh anchors.
    btext = open(BUILD_SH, encoding="utf-8").read()
    if btext.count("# STEP 5 — Counts") != 1:
        failures.append(("BUILD-SH", "build.sh", "STEP-5-ANCHOR",
                         "# STEP 5 — Counts"))
    if "fix22 upstream block applied" in btext:
        failures.append(("BUILD-SH", "build.sh", "BLOCK-ALREADY-PRESENT",
                         "fix22 upstream block applied"))
    if "BANG_PIN=" in btext and not allow_bang_pin:
        failures.append(("BUILD-SH", "build.sh", "BANG-PIN-ALREADY-PRESENT",
                         "BANG_PIN="))
    if btext.count(BANG_PIN_ANCHOR) != 1:
        failures.append(("BUILD-SH", "build.sh", "BANG-PIN-ANCHOR-COUNT=%d"
                         % btext.count(BANG_PIN_ANCHOR), BANG_PIN_ANCHOR))
    if btext.count("fix21 upstream block applied") != 1:
        failures.append(("BUILD-SH", "build.sh", "FIX21-BLOCK-MISSING",
                         "fix21 upstream block applied"))
    # Banned-term scan over every addition and the generated block.
    block = build_sh_block()
    # Block-structure validation: the generated subs tuples must each have
    # exactly 5 elements (pid, rel, old, new, mode) with a valid mode, or
    # the build-time unpack fails. (A format-string slip here once emitted
    # 4-tuples with the mode as a comment; never again.)
    import ast as _ast
    _m = re.search(r"subs = \[(.*?)\n\]", block, re.S)
    assert _m, "PREFLIGHT: subs list not found in generated block"
    _subs = _ast.literal_eval("[" + _m.group(1) + "\n]")
    assert len(_subs) == len(PATCHES), \
        "PREFLIGHT: generated subs count %d != PATCHES %d" % (len(_subs), len(PATCHES))
    for _t in _subs:
        assert len(_t) == 5 and _t[4] in ("after", "before", "replace"), \
            "PREFLIGHT: malformed subs tuple: %r" % (_t[:1],)
    compile(block, "fix22-block", "exec")
    for pid, _rel, _old, new, _mode, _token in PATCHES:
        low = new.lower()
        for term in BANNED:
            if term in low:
                failures.append((pid, "addition", "BANNED-TERM=%s" % term,
                                 new[:80]))
    for term in BANNED:
        if term in block.lower():
            failures.append(("BLOCK", "build.sh block", "BANNED-TERM=%s" % term,
                             term))
    if failures:
        print("PREFLIGHT FAILED — %d problem(s), nothing written:" % len(failures))
        for pid, rel, kind, detail in failures:
            print("  FAILED %s in %s: %s: %r" % (pid, rel, kind, detail))
        sys.exit(1)
    print("preflight OK: %d patches, all anchors count==1, all tokens absent, "
          "banned-term scan clean" % len(PATCHES))


def self_checks():
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "fix22 upstream block applied" in btext, \
        "SELF-CHECK build.sh: fix22 block missing"
    assert 'BANG_PIN="%s"' % BANG_SHA in btext, \
        "SELF-CHECK build.sh: BANG_PIN missing"
    assert btext.count("# STEP 5 — Counts") == 1, \
        "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find("fix22 upstream block applied") > btext.find(
        "fix21 upstream block applied"), \
        "SELF-CHECK build.sh: fix22 block must sit after the fix21 block"
    assert btext.find('BANG_PIN="%s"' % BANG_SHA) > btext.find(
        'AGENTSKILLS_PIN="'), "SELF-CHECK build.sh: BANG_PIN not after AGENTSKILLS_PIN"
    for pid, _rel, _old, _new, _mode, token in PATCHES:
        assert token in btext, \
            "SELF-CHECK build.sh: patch %s token missing from block: %r" % (pid, token)
    print("self-checks OK: fix22 block + BANG_PIN present in build.sh; "
          "all %d patch tokens present in the block" % len(PATCHES))


def _extract_block(btext):
    """The fix22 block text in build.sh, or None if absent."""
    start = btext.find("# --- fix22:")
    if start == -1:
        return None
    end = btext.find("# STEP 5 — Counts", start)
    assert end != -1, "fix22 block present but STEP 5 anchor missing"
    return btext[start:end]


def _block_subs(block):
    """The fix22 block's subs tuples, or None if unparseable."""
    import ast as _ast
    m = re.search(r"subs = \[(.*?)\n\]", block, re.S)
    if not m:
        return None
    try:
        return _ast.literal_eval("[" + m.group(1) + "\n]")
    except Exception:
        return None


def _block_is_valid(block):
    """True iff the block's subs tuples match PATCHES exactly (all
    5-element, valid mode, count == len(PATCHES))."""
    subs = _block_subs(block)
    return (subs is not None and len(subs) == len(PATCHES)
            and all(len(t) == 5 and t[4] in ("after", "before", "replace")
                    for t in subs))


def main():
    btext = open(BUILD_SH, encoding="utf-8").read()
    existing = _extract_block(btext)
    # Patches already in a previous fix22 block: re-running with new
    # patches appended must not duplicate them (Sweep #30).
    _old_subs = _block_subs(existing) if existing is not None else None
    already = {_t[0] for _t in _old_subs} if _old_subs else set()
    bang_already = 'BANG_PIN="%s"' % BANG_SHA in btext
    if existing is not None:
        if _block_is_valid(existing):
            # Re-run: nothing to duplicate. Verify the block is complete, then
            # report every patch as already applied.
            missing = [pid for pid, _r, _o, _n, _m, tok in PATCHES
                       if tok not in btext]
            if missing or 'BANG_PIN="%s"' % BANG_SHA not in btext:
                print("ERROR: fix22 block present but incomplete; missing tokens "
                      "for %s; BANG_PIN present=%s — coordinator must resolve"
                      % (missing, 'BANG_PIN="%s"' % BANG_SHA in btext))
                sys.exit(1)
            for pid, _r, _o, _n, _m, _t in PATCHES:
                print("SKIPPED-ALREADY %s" % pid)
            print("SKIPPED-ALREADY BANG-PIN")
            print("fix22.py: already applied, nothing written")
            return
        # Block present but not current: either malformed, or a previous
        # valid block superseded by new patches appended to PATCHES.
        _all_pids = {pid for pid, _r, _o, _n, _m, _t in PATCHES}
        if (_old_subs and len(_old_subs) == len(already)
                and already < _all_pids
                and all(len(_t) == 5
                        and _t[4] in ("after", "before", "replace")
                        for _t in _old_subs)):
            print("UPDATE: existing fix22 block covers %d of %d patches; "
                  "removing and re-applying with the new patches (BANG_PIN kept)"
                  % (len(_old_subs), len(PATCHES)))
        else:
            print("REPAIR: removed malformed fix22 block from build.sh; "
                  "re-applying (BANG_PIN kept)")
        btext = btext.replace(existing, "", 1)
        open(BUILD_SH, "w", encoding="utf-8").write(btext)

    preflight(allow_bang_pin='BANG_PIN="%s"' % BANG_SHA in
              open(BUILD_SH, encoding="utf-8").read(), already=already)

    # 1. Backup build.sh (keep the first pre-fix22 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix22")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix22")
    else:
        print("build.sh.before-fix22 already exists, kept")

    # 2. BANG_PIN record next to the 6 clone SHAs (skip if already present).
    btext = open(BUILD_SH, encoding="utf-8").read()
    if 'BANG_PIN="%s"' % BANG_SHA in btext:
        print("build.sh: BANG_PIN record already present, kept")
    else:
        assert btext.count(BANG_PIN_ANCHOR) == 1
        btext = btext.replace(BANG_PIN_ANCHOR,
                              BANG_PIN_ANCHOR + "\n" + BANG_PIN_LINES.rstrip("\n"),
                              1)
        open(BUILD_SH, "w", encoding="utf-8").write(btext)
        print("build.sh: BANG_PIN record added after AGENTSKILLS_PIN")

    # 3. Append the fix22 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print("build.sh: fix22 block appended (%d upstream subs, %d lines)"
          % (len(PATCHES), len(block.splitlines())))

    self_checks()

    for pid, _r, _o, _n, _m, _t in PATCHES:
        print(("SKIPPED-ALREADY %s" % pid) if pid in already
              else ("APPLIED %s" % pid))
    print("SKIPPED-ALREADY BANG-PIN" if bang_already else "APPLIED BANG-PIN")


if __name__ == "__main__":
    main()
