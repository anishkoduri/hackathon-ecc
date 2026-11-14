---
name: motion-patterns
description: Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, page transitions, exit animations, scroll, and layout — built on motion-foundations tokens and springs. Use when animating a specific UI element in React or Next.js — button, modal, toast, stagger, page transition, or scroll. For motion feel/timing decisions, use make-interfaces-feel-better first — this skill implements the animation.
tags: [motion, animation, ui-patterns]
category: frontend
author: jeff
metadata:
  version: 1.0.0
---

# Motion Patterns

Copy-paste patterns for the most common UI animation needs.
Every pattern here is built on `motion-foundations` tokens and springs.
Do not define new duration or easing values here — import them.

## When to Activate

- Animating a button, card, modal, or toast notification
- Building list entrances with stagger
- Setting up page transitions in Next.js App Router
- Adding entrance or exit animations to conditional content
- Implementing scroll-reveal, scroll-linked progress, or sticky story sections
- Building expanding cards, accordions, or shared-element transitions

## Outputs

This skill produces:

- Accessible, SSR-safe animation for all standard UI components
- `AnimatePresence`-wrapped conditional renders with correct exit behavior
- Page transition wrapper component for Next.js App Router
- Scroll-reveal and scroll-linked patterns using `useScroll` + `useTransform`
- Layout animation patterns (`layout`, `layoutId`) for expanding and crossfading elements

## Principles

- Every pattern imports from `motion-foundations`. No raw numbers.
- Every conditional render is wrapped in `AnimatePresence` with a `key`.
- Exit animations are always defined alongside enter animations — never as an afterthought.
- `layout` is used only for small, isolated shifts. Large subtrees get explicit transforms.

**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).

## Rules

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Every pattern on a build ships with its motion live: entrances, staggers, dealt moments, micro-interactions, state transitions -- routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A build that feels static fails, even if every static rule passes. Each pattern is recorded in `docs/design-tokens.md`'s Motion list with its trigger and its token values, and its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A pattern that should move and does not move in the rendered page is a finding (M4). `prefers-reduced-motion` is respected in every pattern with a complete static fallback -- a frozen one-frame state or the static final state, content visible at rest -- never a broken one. (D19 -- Motion: each pattern IS a motion decision -- trigger + tokens recorded; Theme: patterns move in the dealt theme's motion voice; Texture: none -- patterns carry no surface treatment; Visuals: live patterns are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 8); Colors: none -- patterns choose no colours.)

1. **Always wrap conditional renders in `AnimatePresence` with a `key`** on the direct child. Without a key, exit animations never fire.
2. **Always define `exit` when defining `initial` + `animate`.** An animation without an exit is incomplete.
3. **Use `mode="wait"` on page transitions.** Enter must not start until exit completes.
4. **Never use `layout` on subtrees with more than ~5 children or deeply nested DOM.** Use explicit `x`/`y` transforms instead.
5. **Stagger interval must stay between `0.05s` and `0.10s`.** Below feels mechanical; above feels sluggish. Scope: this floor governs container-level `staggerChildren` intervals; per-row settle steps (`motionTokens.duration.staggerRow`, B3, 0.03s) are a different scope and are not bound by this floor (fix #24 adjudication of the AB-03 conflict flag).
6. **Modals must always include:** focus trap, Escape-key close, scroll lock, `role="dialog"`, `aria-modal="true"`.
7. **Scroll reveals use `viewport={{ once: true }}`.** Repeating on scroll-out is distracting, not informative.
8. **All token values are imported from `motion-foundations`.** No inline numbers.
9. **M1 — Scroll entrances on motion-governed surfaces (fix #17).** On surfaces governed by the motion-* skills (React/Next.js app surfaces), each content section enters on scroll: `whileInView` with `viewport={{ once: true }}` (motion-patterns rule 7), using motion-foundations tokens. Each entrance is recorded per surface in `docs/design-tokens.md`'s Motion list (surface → entrance → tokens used). A section with no entrance and no recorded reason is an incomplete build — a static check item in step 6, never a screen verdict. SCOPE: the design-taste-frontend page system keeps its standing rule (`references/motion.md`: 'Scrolling moves nothing but the dealt moment') — scroll entrances do NOT apply to Taste landing pages under this rule. A theme file may record a scoped, named exception permitting scroll entrances as that theme's own motion (see sticker.md, fix #17 exception B) — the exception is the theme's decision, not this rule's.
10. **M2 — 1500ms fail-safe: content can never stay hidden (fix #17).** Every scroll-entrance element becomes fully visible within 1500ms of entering the viewport even if its observer never fires: a timed fail-safe (a timer or CSS fallback that forces the visible state — opacity 1, transform none — 1500ms after mount/entry) is a required part of every entrance implementation, and its presence is recorded in the Motion list (surface → entrance → fail-safe mechanism). The step-6 check scrolls to each section, waits 1500ms, and confirms in the screenshot that no content is still hidden (no element left at opacity 0 or off-screen). A section still hidden after the wait is a finding, fed to the fix batch. Under `prefers-reduced-motion: reduce` the content is visible at rest, with no entrance to fail — reduced-motion renders are exempt from the entrance itself but never from visibility.

**Animation rules (fix #22) — group anchor: ANIM_RULES_F22.**

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
`docs/design-tokens.md`.

## Decision Guidance

**Interactive depth — the interface invites interaction (fix #23 §9, DYNAMIC_F23).** Patterns are chosen so the user can DO things, not just look: sortable, filterable, expandable, draggable where it serves the job (Accordion, Expanding card, Dropdown, Modal, Popover, Toast stack, Page transition — each with its live behaviour, not a static mock). Every interactive pattern responds immediately: press states (press scale 0.97), hover, transitions — and every state change it drives is choreographed (AnimatePresence enter/exit, `layout` for size/position changes, stagger for lists), with its trigger and token values recorded in `docs/design-tokens.md`'s Motion list. A control that looks interactive but does nothing on press is a gap; a surface showing frozen mock content — counts and totals that never move — is a gap: surfaces show live state (data updating, statuses changing, counts and totals moving). A state change with no motion is a gap. `prefers-reduced-motion` is respected in every pattern with a complete static fallback — the state still changes, content visible at rest — never a broken one. (D19 — Motion: each interactive pattern IS a motion decision — trigger + tokens recorded; Theme: patterns move in the dealt theme's motion voice; Texture: none — patterns carry no surface treatment; Visuals: live patterns are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 8); Colors: none — patterns choose no colours; Depth: a pattern that reorders layers names the layer order, or `flat by choice — <reason>`.)

### Choosing the right pattern

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate.

| Situation | Pattern |
| ---------------------------------------- | ---------------------- |
| Element appears / disappears             | `AnimatePresence`      |
| List of items loading in sequence        | Stagger variants       |
| Navigating between routes                | Page transition wrapper|
| Element changes size in place            | `layout` prop          |
| Same element moves across page contexts  | `layoutId`             |
| Element enters when scrolled into view   | `whileInView`          |
| Value tied to scroll position            | `useScroll` + `useTransform` |

### When to use `mode="wait"` vs `mode="sync"`

| Mode | Use when |
| ------- | --------------------------------------- |
| `wait` | Page transitions, content swaps (one at a time) |
| `sync` | Stacked notifications, list items (overlap is fine) |
| `popLayout` | Items removed from a reflow list |

## Core Concepts

### AnimatePresence contract

Three things must always be true:

1. `AnimatePresence` wraps the conditional
2. The direct child has a `key`
3. The child has an `exit` prop

Miss any one of these and the exit animation silently fails.

### layout vs layoutId

- `layout` — animates the element's own size/position change in place
- `layoutId` — links two separate elements, crossfading between them across renders

Use `layout="position"` on text inside an expanding container to prevent text reflow from animating.

## Code Examples

### Button feedback

```tsx
"use client"
import { motion } from "motion/react"
import { springs, motionTokens } from "@/lib/motion-tokens"

<motion.button
  whileHover={{ scale: motionTokens.scale.pop }}
  whileTap={{ scale: motionTokens.scale.press }}
  transition={springs.snappy}
/>
```
Animate useful feedback only (UNSLOP_F22 D20, fix #22): press feedback, a success pulse, a state change — motion that tells the user something happened. No decorative motion. This is one family with motion-foundations Principle A10 (Exaggerated feedback) and motion-patterns B8 (Pulse to confirm success); the A10/B8 items live in the motion skills (Groups A+B), this fix points at them.

### Stagger list

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

const container = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.08,   // within the 0.05–0.10 rule
      delayChildren: 0.1,
    },
  },
}

const item = {
  hidden:  { opacity: 0, y: motionTokens.distance.md },
  visible: { opacity: 1, y: 0, transition: springs.gentle },
}

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((i) => (
    <motion.li key={i.id} variants={item} />
  ))}
</motion.ul>
```


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

### Modal

```tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

// Wrap at the call site:
// <AnimatePresence>{isOpen && <Modal key="modal" />}</AnimatePresence>

export function Modal({ onClose }: { onClose: () => void }) {
  return (
    <>
      {/* Overlay */}
      <motion.div
        className="fixed inset-0 bg-black/50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      />

      {/* Panel — accessibility requirements: focus trap, Escape close,
          scroll lock, role="dialog", aria-modal="true" */}
      <motion.div
        role="dialog"
        aria-modal="true"
        className="fixed inset-x-4 top-1/2 -translate-y-1/2 rounded-xl bg-white p-6"
        initial={{
          opacity: 0,
          scale: motionTokens.scale.press,
          y: motionTokens.distance.sm,
        }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{
          opacity: 0,
          scale: motionTokens.scale.press,
          y: motionTokens.distance.sm,
        }}
        transition={springs.gentle}
      />
    </>
  )
}
```


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

### Thinking Orb — the loading indicator for AI/agent waiting states (fix #22 §14, ORBS_F22)

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
`docs/design-tokens.md`.

### Toast stack

```tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

<AnimatePresence mode="sync">
  {toasts.map((t) => (
    <motion.div
      key={t.id}
      layout
      initial={{
        opacity: 0,
        x: motionTokens.distance.xl,
        scale: motionTokens.scale.subtle,
      }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{
        opacity: 0,
        x: motionTokens.distance.xl,
        scale: motionTokens.scale.subtle,
      }}
      transition={springs.snappy}
    />
  ))}
</AnimatePresence>
```

### Page transition (Next.js App Router)

```tsx
// components/page-transition.tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { usePathname } from "next/navigation"
import { motionTokens } from "@/lib/motion-tokens"

const variants = {
  initial: { opacity: 0, y: motionTokens.distance.sm },
  enter:   { opacity: 1, y: 0 },
  exit:    { opacity: 0, y: -motionTokens.distance.sm },
}

export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        variants={variants}
        initial="initial"
        animate="enter"
        exit="exit"
        transition={{
          duration: motionTokens.duration.normal,
          ease: motionTokens.easing.smooth,
        }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Scroll reveal

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

<motion.div
  initial={{ opacity: 0, y: motionTokens.distance.lg }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-80px" }}   // once: true — rule 7
  transition={{ duration: motionTokens.duration.slow, ease: motionTokens.easing.smooth }}
/>
```

**1500ms fail-safe (fix #17 M2).** If the reveal has not fired within 1500ms of the element entering the viewport, the content is shown anyway — nothing ever stays hidden because an observer never fired. Implement with a timer or CSS fallback that forces the visible state (opacity 1, transform none) 1500ms after mount/entry; record the mechanism in the Motion list. See `motion-advanced` `useScrollRevealSafe` for the shared implementation.

### Scroll progress bar

```tsx
"use client"
import { motion, useScroll } from "motion/react"

export function ScrollProgress() {
  const { scrollYProgress } = useScroll()
  return (
    <motion.div
      className="fixed top-0 left-0 h-1 bg-indigo-500 origin-left w-full"
      style={{ scaleX: scrollYProgress }}
    />
  )
}
```

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
`motionTokens.duration.staggerRow` (0.03s — per-row settle steps under B3; Rule 5's 0.05s floor governs container-level `staggerChildren` only, fix #24 adjudication), popover start scale
`motionTokens.scale.popover` (0.95), knob stretch
`motionTokens.scale.stretch` (1.12), exits at `motionTokens.exitFactor`
(0.8× the enter — `motionTokens.exitFactor` (B15) is the single source of truth per Rule 8; the quick-reference ~60–70% defers to it, fix #24 adjudication), entrances on `motionTokens.easing.smooth`, moves on
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
no colours.)

### Parallax layers and 3D-transform hero (fix #22 §13, DEPTH_F22)

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
reason recorded in `docs/design-tokens.md`.

### Expanding card

```tsx
"use client"
import { useState } from "react"
import { motion, AnimatePresence } from "motion/react"
import { springs, motionTokens } from "@/lib/motion-tokens"

export function ExpandingCard({ title, body }: { title: string; body: string }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <motion.div layout onClick={() => setExpanded(!expanded)} className="cursor-pointer">
      {/* layout="position" prevents text reflow from animating */}
      <motion.h2 layout="position" className="font-semibold">
        {title}
      </motion.h2>

      <AnimatePresence>
        {expanded && (
          <motion.p
            key="body"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: motionTokens.duration.fast }}
          >
            {body}
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
```

### Shared-element crossfade

```tsx
// Source context
<motion.img layoutId="hero-image" src={src} className="w-16 h-16 rounded" />

// Destination context (same layoutId — motion handles the transition)
<motion.img layoutId="hero-image" src={src} className="w-full rounded-xl" />
```


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

### Accordion

```tsx
<motion.div
  initial={false}
  animate={{ opacity: open ? 1 : 0, scaleY: open ? 1 : 0 }}
  style={{ transformOrigin: "top", overflow: "hidden" }}
  transition={{
    duration: motionTokens.duration.normal,
    ease: motionTokens.easing.smooth,
  }}
> {children}
</motion.div>
```


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

### 3D scene — React Three Fiber (fix #22 §15, R3F_F22)

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

### OriginKit — animated components, React/Next only (fix #22 §17, ORIGINKIT_F22)

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

## End-to-End Example

A staggered list that enters on mount, handles conditional presence, and
respects reduced motion — combining tokens, springs, AnimatePresence, and
the accessibility hook from `motion-foundations`:

```tsx
"use client"
import { useState } from "react"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"
import { useSafeMotion } from "@/hooks/use-reduced-motion"

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08, delayChildren: 0.1 },
  },
}

function ListItem({ label, onRemove }: { label: string; onRemove: () => void }) {
  const safe = useSafeMotion(motionTokens.distance.sm)
  return (
    <motion.li
      variants={{
        hidden:  safe.initial,
        visible: safe.animate,
      }}
      exit={safe.exit}
      transition={springs.gentle}
      className="flex items-center justify-between p-3 rounded-lg bg-white shadow-sm"
    >
      <span>{label}</span>
      <button onClick={onRemove}>Remove</button>
    </motion.li>
  )
}

export function AnimatedList({ items, onRemove }: {
  items: { id: string; label: string }[]
  onRemove: (id: string) => void
}) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-2"
    >
      <AnimatePresence mode="popLayout">
        {items.map((item) => (
          <ListItem
            key={item.id}
            label={item.label}
            onRemove={() => onRemove(item.id)}
          />
        ))}
      </AnimatePresence>
    </motion.ul>
  )
}
```

## Constraints / Non-Goals

This skill does **not** cover:

- Token and spring definitions → see `motion-foundations`
- Drag interactions, swipe gestures, reorderable lists → see `motion-advanced`
- Text animations (word/character reveal, counters) → see `motion-advanced`
- SVG path drawing or morphing → see `motion-advanced`
- Custom animation hooks → see `motion-advanced`
- CSS-only transitions not using `motion/react`

## Anti-Patterns

| Anti-pattern | Rule violated | Fix |
| -------------------------------------------- | ------- | ------------------------------------------ |
| `AnimatePresence` child missing `key` | Rule 1 | Add stable `key` to the direct child |
| `initial` + `animate` without `exit` | Rule 2 | Always define all three together |
| Page transition without `mode="wait"` | Rule 3 | Add `mode="wait"` to `AnimatePresence` |
| `layout` on a 50-item list | Rule 4 | Use `mode="popLayout"` or explicit transforms |
| `staggerChildren: 0.2` on a 10-item list | Rule 5 | Cap at `0.08–0.10` |
| Modal without focus trap | Rule 6 | Add `focus-trap-react` or Radix Dialog |
| `whileInView` without `viewport={{ once: true }}` | Rule 7 | Repeating entrances distract, not inform |
| `transition={{ duration: 0.3 }}` inline | Rule 8 | Use `motionTokens.duration.normal` |

## Related Skills

- **`motion-foundations`** — defines all tokens, springs, the `useSafeMotion` hook, and SSR guards that every pattern here imports. Must be set up first.
Design vocabulary — the definitions of origin-aware animation (G10), stagger (G14), and shared element transition (G20) live in `skills/design-taste-frontend/references/design-glossary.md` (`GLOSSARY_F22`); this skill applies those concepts, the glossary defines them.
- **`motion-advanced`** — extends these patterns with drag, gestures, SVG, text, custom hooks, and imperative sequencing. Does not redefine any patterns from this skill.
