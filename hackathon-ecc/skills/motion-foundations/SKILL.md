---
name: motion-foundations
description: Motion tokens, spring presets, performance rules, device adaptation, accessibility enforcement, and SSR safety for React / Next.js using motion/react. Foundation layer — all other motion skills depend on this. Use when setting up motion tokens, spring presets, reduced-motion handling, or SSR-safe animation in React or Next.js. For motion feel/timing decisions, use make-interfaces-feel-better first — this skill provides the tokens and implementation foundation.
tags: [motion, animation, performance, accessibility]
category: frontend
author: jeff
metadata:
  version: 1.0.0
---

# Motion Foundations

The base layer of the motion system. Defines every value, constraint, and
rule that downstream skills (`motion-patterns`, `motion-advanced`) inherit.
Load this skill before any animation work begins.

## When to Activate

- Starting any animated component from scratch
- Setting up tokens, spring presets, or easing values
- Implementing `prefers-reduced-motion` support
- Debugging hydration mismatches from animation initial states
- Evaluating whether an animation should exist at all

## Outputs

This skill produces:

- A shared `motionTokens` object (duration, easing, distance, scale)
- A shared `springs` preset map (5 named configs)
- A `shouldAnimate()` gate used by all components
- Accessibility-compliant animation defaults via `useReducedMotion`
- SSR-safe initial states with zero hydration warnings

## Principles

Motion must do at least one of the following or it must be removed:

- Guide attention
- Communicate state
- Preserve spatial continuity

Responsiveness always outranks smoothness. A 60 fps animation that causes
input delay is worse than no animation.

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
colours are the theme's own tokens.)
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
project; Colors: none — the scene's colours are the theme's own tokens.)
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
values; Colors: none — the principles do not choose colours.

**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).

## Rules

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Every build ships deliberate, eye-catching motion: entrances, staggers, dealt moments, micro-interactions, state transitions -- routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A build that feels static fails, even if every static rule passes. Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values, directed per §10 (direct, don't describe). Scope: on motion-governed surfaces (React/Next app surfaces) this means scroll entrances (M1) + staggers + micro-interactions; on Taste landing pages the scroll ban stands (scrolling moves nothing but the dealt moment) and the motion is the hero entrance + dealt moments + micro-interactions. `prefers-reduced-motion` is respected everywhere with a complete static fallback -- content visible at rest, no entrance to fail, every loop/scene rendered at its final state -- never a broken one. (D19 -- Motion: this rule IS the motion decision -- deliberate motion on every build, token-routed; Theme: motion is the dealt theme's motion voice, never a generic effect; Texture: none -- motion carries no surface treatment; Visuals: motion is what makes the build read as alive rather than static; Techniques: values come from `motionTokens` and the Group B rules, never hardcoded; Colors: none -- motion chooses no colours.)

These are non-negotiable. They apply to every component in the system.

1. **Use `motion/react` only.** Never import from `framer-motion`. Never mix the two in the same tree.
2. **`initial` must match server output.** If the server renders `opacity: 1`, the `initial` prop must also be `opacity: 1`. No exceptions.
3. **Reduced motion overrides everything.** When `useReducedMotion()` returns `true` or `prefersReduced` is `true`, all transforms are disabled. Opacity-only fades at ≤ 0.2s are the only permitted fallback.
4. **Never animate layout properties.** `width`, `height`, `top`, `left`, `margin`, `padding` are banned from `animate`. Use `transform` and `opacity` only.

Animation rules are also checked in a polish pass against the pinned Vercel checklist (VERCEL_F22): reduced-motion, transform/opacity-only, no `transition: all`, transform-origin, SVG `<g>` transforms, interruptible animations, autoplay controls (V-AN1–V-AN8) — this skill states the tokens and rules, the checklist is the file:line check (fix #22).
5. **All token values come from `motionTokens`.** Hardcoded durations and easings in component files are forbidden.
6. **All spring configs come from the `springs` map.** Inline `stiffness`/`damping` values are forbidden.
7. **`"use client"` is required** on every file that imports from `motion/react`.
8. **Never read `window` or `navigator` at module level.** Always guard with `typeof window !== "undefined"`.
9. **M1 — Scroll entrances on motion-governed surfaces (fix #17).** On surfaces governed by the motion-* skills (React/Next.js app surfaces), each content section enters on scroll: `whileInView` with `viewport={{ once: true }}` (motion-patterns rule 7), using motion-foundations tokens. Each entrance is recorded per surface in `docs/design-tokens.md`'s Motion list (surface → entrance → tokens used). A section with no entrance and no recorded reason is an incomplete build — a static check item in step 6, never a screen verdict. SCOPE: the design-taste-frontend page system keeps its standing rule (`references/motion.md`: 'Scrolling moves nothing but the dealt moment') — scroll entrances do NOT apply to Taste landing pages under this rule. A theme file may record a scoped, named exception permitting scroll entrances as that theme's own motion (see sticker.md, fix #17 exception B) — the exception is the theme's decision, not this rule's.
10. **M2 — 1500ms fail-safe: content can never stay hidden (fix #17).** Every scroll-entrance element becomes fully visible within 1500ms of entering the viewport even if its observer never fires: a timed fail-safe (a timer or CSS fallback that forces the visible state — opacity 1, transform none — 1500ms after mount/entry) is a required part of every entrance implementation, and its presence is recorded in the Motion list (surface → entrance → fail-safe mechanism). The step-6 check scrolls to each section, waits 1500ms, and confirms in the screenshot that no content is still hidden (no element left at opacity 0 or off-screen). A section still hidden after the wait is a finding, fed to the fix batch. Under `prefers-reduced-motion: reduce` the content is visible at rest, with no entrance to fail — reduced-motion renders are exempt from the entrance itself but never from visibility.
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
`docs/design-tokens.md`.

## Decision Guidance

**State changes are choreographed, not instant swaps (fix #23 §9, DYNAMIC_F23).** Every state change on a build is a choreographed transition, routed through the fix #22 motion tokens (Group A principles + Group B values) and, where the change is a moment, a dealt moment: entering/leaving, loading to loaded, empty to filled, selected, confirmed. A state change with no motion is a gap — the interface must never snap between states with nothing in between. Each state change is recorded in `docs/design-tokens.md`'s Motion list with its trigger, its token values, and its D19 reason (Motion dimension), directed per §10 (direct, don't describe). This is the state-change rule; §2 (MOTION_F23) is the motion-presence rule — deliberate motion on every build — and this section says how each change moves, it does not restate it. `prefers-reduced-motion` is respected everywhere: the state still changes and the content is correct at rest — opacity-only fades at ≤ 0.2s or no motion — with a complete static fallback, never a broken state. (D19 — Motion: each state change IS a motion decision — trigger + tokens recorded; Theme: changes move in the dealt theme's motion voice; Texture: none — state changes carry no surface treatment; Visuals: choreographed changes are what make the interface read as alive rather than frozen; Techniques: values come from `motionTokens` and the Group B rules, never hardcoded; Colors: none — state changes choose no colours; Depth: a change that reorders layers names the layer order, or `flat by choice — <reason>`.)

### Choosing a duration

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate.

| Token | Use when |
| --------- | -------------------------------------------- |
| `instant` | Tooltip show/hide, focus ring, badge update |
| `fast` | Button feedback, icon swap, chip toggle |
| `normal` | Modal open, card expand, page element enter |
| `slow` | Hero entrance, full-page transition |
| `crawl` | Deliberate storytelling; use sparingly |
Feedback animation (UNSLOP_F22 D20) uses the `fast` token for button feedback; see motion-patterns "Button feedback" and Principle A10 / B8 (fix #22).

### Choosing a spring

| Preset | Use when |
| --------- | ------------------------------------------ |
| `snappy` | Default UI — buttons, chips, nav items |
| `gentle` | Cards, modals, panels landing softly |
| `bouncy` | Playful moments — empty states, onboarding |
| `instant` | Tooltips, popovers, dropdowns |
| `release` | Drag release — natural physics feel |

### When to disable animation entirely

Disable (make `shouldAnimate()` return `false`) when:

- `prefersReduced` is `true`
- `isLowEnd` is `true` and the animation is non-essential
- The element is off-screen and will never enter the viewport
- The animation is purely decorative with no UX purpose

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
colours.)


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

## Core Concepts

### Token system

```ts
// lib/motion-tokens.ts

// Animation token values (fix #22) — group anchor: ANIM_TOKENS_F22

export const motionTokens = {
  duration: {
    instant: 0.08,
    fast:    0.18,
    dropdown: 0.2,   // B2 (fix #22): dropdowns animate at 150–250ms; 0.2s is the default inside the range.
    staggerRow: 0.03, // B3 (fix #22): list rows stagger by 30ms per row. Adjudicated fix #24: Rule 5's 0.05s floor governs container-level `staggerChildren`; B3 governs per-row settle steps — different scopes, no conflict.
    normal:  0.35,
    slow:    0.6,
    crawl:   1.0,
  },
  easing: {
    smooth: [0.22, 1, 0.36, 1], // B1 (fix #22): the ease-out curve — entrances use this easing.
    sharp:  [0.4, 0, 0.2, 1],
    bounce: [0.34, 1.56, 0.64, 1],
    linear: [0, 0, 1, 1],
    inOut:  [0.65, 0, 0.35, 1], // B9 (fix #22): ease-in-out for moves — an element travelling from one place to another.
  },
  distance: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 48,
  },
  scale: {
    subtle: 0.98,
    press:  0.95,
    popover: 0.95, // B10 (fix #22): popovers start at scale 0.95 and grow to 1. Separate token from press — the value coincides with press by chance, never merge them.
    stretch: 1.12, // B5 (fix #22): a moving knob stretches 12% along its direction of travel while it moves, then springs back.
    pop:    1.04,
  },
  exitFactor: 0.8, // B15 (fix #22): exits run 20% shorter than their enter — exit duration = 0.8 x the matching enter duration. Adjudicated fix #24: `motionTokens.exitFactor` (B15) is the single source of truth per Rule 8; the quick-reference ~60–70% defers to it.
}

- **D19 (for the token group as a whole)** — Motion: the tokens are the values every animation in the build runs on, so motion timing is decided once and reused, never improvised per component; Theme: tokens are values, not looks — the theme still decides what the moving element is and what it means; Texture: none — tokens carry no surface treatment; Visuals: the values keep entrances, moves, and exits legible (nothing too fast to see, nothing slow enough to wait on); Techniques: values live in `motionTokens` and are imported, never hardcoded in components (Rule 5); Colors: none — tokens do not choose colours.

- **Theme-match precondition:** tokens are numbers, not designs — every element animated with them must still match the dealt theme (its material, tokens, palette balance, and do-nots); a token applied in a way that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element.

### Depth tokens — 3D motion values (fix #22 §13, DEPTH_F22)

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

- **Theme-match precondition:** tokens are numbers, not designs — every element moved under them must still match the dealt theme; a token applied in a way that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element.

export const springs = {
  snappy:  { type: "spring", stiffness: 300, damping: 30 },
  gentle:  { type: "spring", stiffness: 120, damping: 14 },
  bouncy:  { type: "spring", stiffness: 400, damping: 10 },
  instant: { type: "spring", stiffness: 600, damping: 35 },
  release: { type: "spring", stiffness: 200, damping: 20, restDelta: 0.001 },
}
```

### Runtime flags

```ts
// lib/motion-config.ts
export const motionConfig = {
  isLowEnd() {
    return (
      typeof navigator !== "undefined" &&
      navigator.hardwareConcurrency <= 4
    )
  },

  prefersReduced() {
    return (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    )
  },

  shouldAnimate({ essential = false } = {}) {
    if (this.prefersReduced()) return false
    if (!essential && this.isLowEnd()) return false
    return true
  },

  duration() {
    return this.isLowEnd() || this.prefersReduced()
      ? motionTokens.duration.instant
      : motionTokens.duration.normal
  },
}
```

### Thinking Orb tokens (fix #22 §14, ORBS_F22)

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
not applied, with the reason recorded in `docs/design-tokens.md`.

### Accessibility

**Priority order (highest to lowest):**

1. `prefers-reduced-motion: reduce` — disables all transforms, limits opacity transitions to ≤ 0.2s
2. Low-end device detection — reduces duration, removes non-essential animations
3. Design preference — everything else

Motion must degrade gracefully. It must never disappear abruptly in a way
that causes layout shift or confuses orientation. Under reduced motion the fail-safe still reveals (opacity-only ≤ 0.2s) — content is visible at rest with no entrance to fail (fix #17 M2/M6). Every motion rule in this section is gated on `prefers-reduced-motion: reduce`, in both layers: the CSS block above and the JS guard (`useSafeMotion` / `motionConfig.shouldAnimate`); the built page must contain both, and the step-6 record notes the reduced-motion render (or records that it did not run — never claim a render pass that did not run) (fix #17 M6).

```tsx
// hooks/use-reduced-motion.tsx
"use client"
import { useReducedMotion } from "motion/react"

export function useSafeMotion(fullY: number = 16) {
  const reduce = useReducedMotion()
  return {
    initial: { opacity: 0, y: reduce ? 0 : fullY },
    animate: { opacity: 1, y: 0 },
    exit:    { opacity: 0, y: reduce ? 0 : -fullY },
  }
}
```

```css
/* globals.css */
@media (prefers-reduced-motion: reduce) {
  .motion-safe-transition  { transition: opacity 0.15s; }
  .motion-reduce-transform { transform: none !important; }
}
```

```html
<!-- Tailwind -->
<div class="motion-safe:animate-fade motion-reduce:opacity-100"></div>
```

### SSR / hydration safety

**Rule: `initial` must always match what the server renders.**

```tsx
// WRONG — server renders opacity:1 but initial says 0 → hydration mismatch
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} />

// CORRECT — use AnimatePresence or defer to client mount
"use client"
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])

<motion.div
  initial={{ opacity: mounted ? 0 : 1 }}
  animate={{ opacity: 1 }}
/>
```

## Code Examples

### End-to-end: tokens + springs + accessibility + SSR guard

```tsx
// components/fade-in-card.tsx
"use client"

import { useState, useEffect } from "react"
import { motion } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"
import { useSafeMotion } from "@/hooks/use-reduced-motion"
import { motionConfig } from "@/lib/motion-config"

interface FadeInCardProps {
  children: React.ReactNode
  delay?: number
}

export function FadeInCard({ children, delay = 0 }: FadeInCardProps) {
  // SSR guard — initial must match server output (opacity: 1)
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  // Accessibility — disables transform when reduced motion is preferred
  const safeMotion = useSafeMotion(motionTokens.distance.md)

  // Device gate — skip animation on low-end hardware
  if (!motionConfig.shouldAnimate() || !mounted) {
    return <div>{children}</div>
  }

  return (
    <motion.div
      initial={safeMotion.initial}
      animate={safeMotion.animate}
      exit={safeMotion.exit}
      transition={{
        ...springs.gentle,
        delay,
      }}
      whileHover={{ scale: motionTokens.scale.pop }}
      whileTap={{ scale: motionTokens.scale.press }}
    >
      {children}
    </motion.div>
  )
}
```

## Constraints / Non-Goals

This skill does **not** cover:

- UI component patterns (button, modal, stagger) → see `motion-patterns`
- Drag, gestures, SVG, text animations, custom hooks → see `motion-advanced`
- CSS-only animations or Tailwind `animate-*` classes without `motion/react`
- Third-party animation libraries (GSAP, anime.js, etc.)
- Motion design decisions (when to animate, what to emphasize) — that is a design concern, not a code constraint

## Anti-Patterns

| Anti-pattern | Rule violated | Fix |
| --------------------------------------- | ------- | ------------------------------- |
| `import { motion } from "framer-motion"` | Rule 1 | Use `motion/react` |
| `initial={{ opacity: 0 }}` on SSR component | Rule 2 | Add mount guard |
| Skipping `useReducedMotion` check | Rule 3 | Use `useSafeMotion` hook |
| `animate={{ width: "100%" }}` | Rule 4 | Use `scaleX` transform instead |
| `transition={{ duration: 0.4 }}` inline | Rule 5 | Use `motionTokens.duration.normal` |
| `{ stiffness: 300, damping: 30 }` inline | Rule 6 | Use `springs.snappy` |
| Missing `"use client"` directive | Rule 7 | Add to top of file |
| `navigator.hardwareConcurrency` at module level | Rule 8 | Wrap in `typeof navigator !== "undefined"` |

## Related Skills

- **`motion-patterns`** — consumes tokens and springs defined here to build button, modal, stagger, page transition, and scroll patterns. Does not redefine any values.
Design vocabulary — the definition of interruptible animation (G18) lives in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies the concept, the glossary defines it.
- **`motion-advanced`** — consumes tokens and springs defined here for drag, SVG, text, and gesture patterns. Adds `useAnimate` sequences and custom hooks on top of this foundation.
