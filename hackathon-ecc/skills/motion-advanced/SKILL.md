---
name: motion-advanced
description: Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG path drawing, custom hooks, imperative sequences (useAnimate), loaders, and the full API decision tree. Requires motion-foundations. Use when building drag and drop, gestures, text or SVG animation, or imperative animation sequences in React or Next.js. For motion feel/timing decisions, use make-interfaces-feel-better first — this skill implements the advanced pattern.
tags: [motion, animation, advanced, gestures, svg]
category: frontend
author: jeff
metadata:
  version: 1.0.0
---

# Motion Advanced

Complex, interactive, and physics-based animation patterns.
Requires `motion-foundations` to be set up first.
Use these when `motion-patterns` is not enough.

## When to Activate

- Building drag-to-dismiss sheets, swipe gestures, or reorderable lists
- Animating text word-by-word, character-by-character, or as a live counter
- Drawing SVG paths, morphing icons, or animating circular progress
- Writing a custom animation hook (`useScrollReveal`, magnetic button, cursor follower)
- Sequencing multi-step animations imperatively with `useAnimate`
- Building spinners, shimmer skeletons, pulse indicators, or loading button states

## Outputs

This skill produces:

- Drag interactions: draggable cards, drag-to-dismiss sheets, `Reorder.Group` lists
- Gesture hooks: swipe detection, long press, pinch outline
- Text animation components: word reveal, character typewriter, number counter
- SVG animation: path draw-on, icon morph, stroke progress ring
- Custom hooks: `useScrollReveal`, `useHoverScale`, `useNavigationDirection`, `useInViewOnce`
- Imperative sequences via `useAnimate` with interrupt-safe `async/await`
- Loader components: spinner, shimmer, pulse dot, progress bar, button loading state

## Principles

- Physics-based motion (`useSpring`, `springs.*`) always feels more natural than duration-based for direct manipulation.
- `useMotionValue` + `useTransform` computes derived values without triggering re-renders.
- `useAnimate` sequences are imperative and interrupt-safe — calling `animate()` mid-flight cancels the previous animation automatically.
- Motion values (`useMotionValue`, `useSpring`) are SSR-safe and do not cause hydration errors.

**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).

## Rules

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** Advanced choreography is deliberate motion too: every drag, reveal, counter, mask, knob, overlap, cursor-follow, shimmer, or loading piece on a build must actually move in the rendered page, routed through the fix #22 motion tokens (Group A principles + Group B values, e.g. B5 knob stretch 12%, B16 overlap old & new states, B17 masks, B19 rubber band) and recorded in `docs/design-tokens.md`'s Motion list with its trigger and its token values, plus its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A build that feels static fails, even if every static rule passes -- an advanced piece that sits still is a finding (M4). `prefers-reduced-motion` is respected everywhere with a complete static fallback -- the piece renders at its final state, content visible at rest -- never a broken one. (D19 -- Motion: each advanced piece IS a motion decision -- trigger + tokens recorded; Theme: choreography moves in the dealt theme's motion voice; Texture: none -- choreography carries no surface treatment; Visuals: moving pieces are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 6); Colors: none -- choreography chooses no colours.)

1. **Drag interactions must be tested on touch devices**, not just mouse. `drag` prop works on both but feel and threshold differ.
2. **Infinite animations must pause when `document.visibilityState === "hidden"`.** Background tabs must not consume GPU/CPU.
3. **Swipe threshold must be explicit.** Never infer intent from velocity alone; combine `offset` + `velocity` checks.
4. **`useAnimate` scope ref must be attached to a mounted DOM element.** Calling `animate()` before mount throws silently.
5. **Motion values must not be recreated on render.** `useMotionValue(0)` inside a component body is correct; `new MotionValue(0)` in a render is not.
6. **All token values are imported from `motion-foundations`.** No inline numbers.
7. **Custom hooks must handle cleanup.** Every `window.addEventListener` needs a matching `removeEventListener` in the `useEffect` return.
8. **SVG morphing requires equal path command counts.** Paths with different command structures snap instead of interpolating.

**Advanced animation rules (fix #22) — group anchor: ANIM_ADV_F22.**

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
`docs/design-tokens.md`.

## Decision Guidance

**Advanced pieces are live and interactive (fix #23 §9, DYNAMIC_F23).** Every advanced piece on a build must actually respond and move in the rendered page: drags with physics on release, reorderable lists, drag-to-dismiss, swipe detection, long-press, counters tweening to live values, SVG draws, mask reveals, shimmer skeletons and button loading states — routed through the fix #22 motion tokens (Group A principles + Group B values) and recorded in `docs/design-tokens.md`'s Motion list with trigger and token values, plus its D19 reason (Motion dimension), directed per §10 (direct, don't describe). A draggable that snaps without physics, a counter that jumps to its value without tweening, or a loading state that flips to loaded with no transition is a gap — a state change with no motion is a gap, and a control that does not respond is a gap. `prefers-reduced-motion` is respected everywhere with a complete static fallback — the piece renders at its final state, content visible at rest — never a broken one. (D19 — Motion: each advanced piece IS a motion decision — trigger + tokens recorded; Theme: choreography moves in the dealt theme's motion voice; Texture: none — choreography carries no surface treatment; Visuals: moving pieces are what make the build read as alive; Techniques: values come from `motion-foundations` tokens, never inline numbers (Rule 6); Colors: none — choreography chooses no colours; Depth: a piece that reorders layers names the layer order, or `flat by choice — <reason>`.)

### Choosing the right advanced API

**Design-decision pointer:** D19/F6/X1 as relevant (motion is a D19 dimension; the experience is the moment) — design-package rule — Taste step 4a / orchestrate.

| Scenario | API |
| ------------------------------ | -------------------------------- |
| Drag with physics on release | `drag` + `dragTransition: springs.release` |
| Ordered drag-to-reorder list | `Reorder.Group` + `Reorder.Item` |
| Dismiss on drag offset | `drag="y"` + `onDragEnd` offset check |
| Swipe left/right | `drag="x"` + `onDragEnd` offset check |
| Long press | `useLongPress` hook |
| Value smoothed over time | `useSpring` |
| Value derived from another | `useTransform` |
| Multi-step sequence | `useAnimate` with `async/await` |
| One-shot imperative animation | `animate()` from `motion` |
| Text entering word by word | Stagger on `inline-block` spans |
| SVG drawing on | `pathLength` 0 → 1 |
| SVG morph | `d` attribute tween (equal commands) |
| Circular progress | `strokeDashoffset` tween |

### When to use `useSpring` vs a spring transition

| | `useSpring` | `transition: springs.*` |
| -------------- | ---------------------------------------- | ----------------------- |
| Use for | Cursor follower, pointer-tracked values | Discrete state changes |
| Updates | Continuous, on every frame | Triggered by state change |
| Interrupt | Smooth — physics picks up from velocity | Restarts from current value |

## Core Concepts

### useMotionValue + useTransform

Reactive computation without re-renders:

```tsx
const x = useMotionValue(0)
const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])
// opacity updates every frame as x changes — no setState, no re-render
```

### useAnimate

Returns `[scope, animate]`. The scope ref must be attached to a DOM element.
`animate()` calls are interrupt-safe — calling mid-flight cancels the previous run.

```tsx
const [scope, animate] = useAnimate()

async function play() {
  await animate(".step-1", { opacity: 1 }, { duration: 0.3 })
  await animate(".step-2", { x: 0 },       { duration: 0.4 })
        animate(".step-3", { scale: 1 },    { duration: 0.25 })  // fire and forget
}

return <div ref={scope}>...</div>
```

## Code Examples

### Draggable card

```tsx
"use client"
import { motion } from "motion/react"
import { springs, motionTokens } from "@/lib/motion-tokens"

<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  dragElastic={0.1}
  whileDrag={{
    scale: motionTokens.scale.pop,
    boxShadow: "0 16px 40px rgba(0,0,0,0.2)",
  }}
  dragTransition={springs.release}
/>
```

### Drag-to-dismiss sheet

```tsx
"use client"
import { motion, useMotionValue, useTransform } from "motion/react"

export function BottomSheet({ onClose }: { onClose: () => void }) {
  const y = useMotionValue(0)
  const opacity = useTransform(y, [0, 200], [1, 0])

  return (
    <motion.div
      drag="y"
      dragConstraints={{ top: 0 }}
      style={{ y, opacity }}
      onDragEnd={(_, info) => {
        // Rule 3: combine offset + velocity
        if (info.offset.y > 120 || info.velocity.y > 500) onClose()
      }}
    />
  )
}
```

### Reorderable list

```tsx
"use client"
import { Reorder } from "motion/react"

export function SortableList() {
  const [items, setItems] = useState(initialItems)
  return (
    <Reorder.Group axis="y" values={items} onReorder={setItems}>
      {items.map((item) => (
        <Reorder.Item key={item.id} value={item}>
          {item.label}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  )
}
```

### Swipe detection

```tsx
"use client"
import { motion } from "motion/react"

const OFFSET_THRESHOLD  = 50
const VELOCITY_THRESHOLD = 300

<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(_, info) => {
    const swipedRight = info.offset.x > OFFSET_THRESHOLD  || info.velocity.x > VELOCITY_THRESHOLD
    const swipedLeft  = info.offset.x < -OFFSET_THRESHOLD || info.velocity.x < -VELOCITY_THRESHOLD
    if (swipedRight) onSwipeRight()
    if (swipedLeft)  onSwipeLeft()
  }}
/>
```

### Long press hook

```tsx
import { useRef } from "react"

export function useLongPress(callback: () => void, ms = 600) {
  const timerRef = useRef<ReturnType<typeof setTimeout>>()
  return {
    onPointerDown:  () => { timerRef.current = setTimeout(callback, ms) },
    onPointerUp:    () => clearTimeout(timerRef.current),
    onPointerLeave: () => clearTimeout(timerRef.current),
  }
}
```

### Word-by-word reveal

```tsx
"use client"
import { motion } from "motion/react"
import { springs } from "@/lib/motion-tokens"

export function AnimatedText({ text }: { text: string }) {
  return (
    <motion.p
      variants={{ visible: { transition: { staggerChildren: 0.05 } } }}
      initial="hidden"
      animate="visible"
    >
      {text.split(" ").map((word, i) => (
        <motion.span
          key={i}
          className="inline-block mr-1"
          variants={{
            hidden:  { opacity: 0, y: 12 },
            visible: { opacity: 1, y: 0, transition: springs.gentle },
          }}
        >
          {word}
        </motion.span>
      ))}
    </motion.p>
  )
}
```

### Number counter

```tsx
"use client"
import { useRef, useEffect } from "react"
import { animate } from "motion"
import { motionTokens } from "@/lib/motion-tokens"

export function Counter({ to }: { to: number }) {
  const nodeRef = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    const controls = animate(0, to, {
      duration: motionTokens.duration.crawl,
      ease: motionTokens.easing.smooth,
      onUpdate: (v) => {
        if (nodeRef.current) nodeRef.current.textContent = Math.round(v).toString()
      },
    })
    return controls.stop   // Rule 7: cleanup
  }, [to])

  return <span ref={nodeRef} />
}
```

### SVG path draw-on

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

<motion.path
  d="M 0 100 Q 50 0 100 100"
  initial={{ pathLength: 0, opacity: 0 }}
  animate={{ pathLength: 1, opacity: 1 }}
  transition={{ duration: motionTokens.duration.slow, ease: motionTokens.easing.smooth }}
/>
```

### Stroke progress ring

```tsx
"use client"
import { motion } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

const CIRCUMFERENCE = 2 * Math.PI * 40   // r=40

export function ProgressRing({ progress }: { progress: number }) {
  return (
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="40" fill="none" stroke="#e5e7eb" strokeWidth="8" />
      <motion.circle
        cx="50" cy="50" r="40"
        fill="none" stroke="#6366f1" strokeWidth="8"
        strokeLinecap="round"
        strokeDasharray={CIRCUMFERENCE}
        animate={{ strokeDashoffset: CIRCUMFERENCE - (progress / 100) * CIRCUMFERENCE }}
        transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
        style={{ rotate: -90, transformOrigin: "center" }}
      />
    </svg>
  )
}
```

### useScrollReveal hook

```tsx
"use client"
import { useRef } from "react"
import { useScroll, useTransform } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

export function useScrollReveal() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const opacity = useTransform(scrollYProgress, [0, 0.3], [0, 1])
  const y       = useTransform(scrollYProgress, [0, 0.3], [motionTokens.distance.lg, 0])
  return { ref, style: { opacity, y } }
}

// Usage
const { ref, style } = useScrollReveal()
<motion.section ref={ref} style={style} />
```

// 1500ms fail-safe (fix #17 M2): if the reveal has not completed within
// 1500ms of mount, force the visible state — content can never stay hidden
// because an observer never fired. Record the mechanism in the Motion list.
export function useScrollRevealSafe() {
  const { ref, style } = useScrollReveal()
  const [revealed, setRevealed] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setRevealed(true), 1500)
    return () => clearTimeout(t)
  }, [])
  return { ref, style: revealed ? { opacity: 1, y: 0 } : style }
}



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

### Cursor follower

```tsx
"use client"
import { useEffect } from "react"
import { motion, useMotionValue, useSpring } from "motion/react"
import { springs } from "@/lib/motion-tokens"

export function CursorFollower() {
  const x = useMotionValue(-100)
  const y = useMotionValue(-100)
  const sx = useSpring(x, springs.gentle)
  const sy = useSpring(y, springs.gentle)

  useEffect(() => {
    const move = (e: MouseEvent) => { x.set(e.clientX); y.set(e.clientY) }
    window.addEventListener("mousemove", move)
    return () => window.removeEventListener("mousemove", move)   // Rule 7
  }, [])

  return (
    <motion.div
      className="fixed top-0 left-0 w-6 h-6 rounded-full bg-indigo-500
                 pointer-events-none -translate-x-1/2 -translate-y-1/2 z-50"
      style={{ x: sx, y: sy }}
    />
  )
}
```

### Shimmer skeleton

```tsx
"use client"
import { useEffect } from "react"
import { motion, useAnimation } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

export function ShimmerSkeleton({ className = "" }: { className?: string }) {
  const controls = useAnimation()

  useEffect(() => {
    const play = () =>
      controls.start({
        x: ["-100%", "100%"],
        transition: {
          repeat: Infinity,
          duration: motionTokens.duration.crawl,
          ease: motionTokens.easing.linear,
        },
      })

    const handleVisibility = () => {
      if (document.visibilityState === "hidden") controls.stop()
      else void play()
    }

    void play()
    document.addEventListener("visibilitychange", handleVisibility)
    return () => {
      controls.stop()
      document.removeEventListener("visibilitychange", handleVisibility)
    }
  }, [controls])

  return (
    <div className={`relative overflow-hidden bg-gray-200 rounded ${className}`}>
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/60 to-transparent"
        initial={{ x: "-100%" }}
        animate={controls}
      />
    </div>
  )
}
```

### Button loading state

```tsx
"use client"
import { motion, AnimatePresence } from "motion/react"
import { motionTokens, springs } from "@/lib/motion-tokens"

export function LoadingButton({
  loading,
  label,
  onClick,
}: {
  loading: boolean
  label: string
  onClick: () => void
}) {
  return (
    <motion.button
      onClick={onClick}
      animate={{ opacity: loading ? 0.7 : 1 }}
      whileTap={loading ? {} : { scale: motionTokens.scale.press }}
      transition={springs.snappy}
      disabled={loading}
    >
      <AnimatePresence mode="wait">
        {loading ? (
          <motion.span
            key="loading"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: motionTokens.duration.fast }}
          >
            …
          </motion.span>
        ) : (
          <motion.span
            key="label"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: motionTokens.duration.fast }}
          >
            {label}
          </motion.span>
        )}
      </AnimatePresence>
    </motion.button>
  )
}
```

### Infinite animation with visibility pause

```tsx
"use client"
import { useEffect } from "react"
import { motion, useAnimation } from "motion/react"
import { motionTokens } from "@/lib/motion-tokens"

export function PulseDot() {
  const controls = useAnimation()

  useEffect(() => {
    const pulse = () =>
      controls.start({
        scale: [1, 1.4, 1],
        opacity: [1, 0.6, 1],
        transition: { repeat: Infinity, duration: motionTokens.duration.crawl },
      })

    // Rule 2: pause when tab is hidden
    const handleVisibility = () => {
      if (document.visibilityState === "hidden") controls.stop()
      else void pulse()
    }

    void pulse()
    document.addEventListener("visibilitychange", handleVisibility)
    // Rule 7: stop controls and remove listeners on unmount.
    return () => {
      controls.stop()
      document.removeEventListener("visibilitychange", handleVisibility)
    }
  }, [controls])

  return <motion.span className="w-2 h-2 rounded-full bg-green-400" animate={controls} />
}
```

## End-to-End Example

Drag-to-dismiss sheet with shimmer content, loading state, and reduced motion
support — combining `useMotionValue`, `useTransform`, `useSafeMotion`,
`AnimatePresence`, and tokens from `motion-foundations`:

```tsx
"use client"
import { useState } from "react"
import { motion, AnimatePresence, useMotionValue, useTransform } from "motion/react"
import { springs, motionTokens } from "@/lib/motion-tokens"
import { useSafeMotion } from "@/hooks/use-reduced-motion"
import { ShimmerSkeleton } from "./shimmer-skeleton"

export function DismissibleSheet({
  isOpen,
  onClose,
  loading,
  children,
}: {
  isOpen: boolean
  onClose: () => void
  loading: boolean
  children: React.ReactNode
}) {
  const safe = useSafeMotion(motionTokens.distance.xl)
  const y = useMotionValue(0)
  const opacity = useTransform(y, [0, 200], [1, 0])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            key="backdrop"
            className="fixed inset-0 bg-black/40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Sheet — drag-to-dismiss */}
          <motion.div
            key="sheet"
            className="fixed bottom-0 inset-x-0 rounded-t-2xl bg-white p-6"
            drag="y"
            dragConstraints={{ top: 0 }}
            style={{ y, opacity }}
            onDragEnd={(_, info) => {
              if (info.offset.y > 120 || info.velocity.y > 500) onClose()
            }}
            initial={safe.initial}
            animate={safe.animate}
            exit={safe.exit}
            transition={springs.gentle}
          >
            {loading ? (
              <div className="space-y-3">
                <ShimmerSkeleton className="h-4 w-3/4" />
                <ShimmerSkeleton className="h-4 w-1/2" />
                <ShimmerSkeleton className="h-20 w-full" />
              </div>
            ) : children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Constraints / Non-Goals

This skill does **not** cover:

- Token and spring definitions → see `motion-foundations`
- Standard UI patterns (button, modal, stagger, page transitions) → see `motion-patterns`
- CSS-only animations or Tailwind `animate-*` without `motion/react`
- Canvas or WebGL-based animation (Three.js, Pixi, etc.)
- Full drag-and-drop systems with external state managers (dnd-kit, react-beautiful-dnd)
- Game-loop or frame-by-frame animation

## Anti-Patterns

| Anti-pattern | Rule violated | Fix |
| ---------------------------------------------- | ------- | ------------------------------------------------ |
| `drag` tested only on desktop | Rule 1 | Test on touch emulator and real device |
| `animate={{ repeat: Infinity }}` with no pause | Rule 2 | Add `visibilitychange` listener |
| `onDragEnd` checking only offset, not velocity | Rule 3 | Check both `info.offset` and `info.velocity` |
| `animate(scope, ...)` before `useEffect` | Rule 4 | Call `animate()` only after mount |
| `const x = new MotionValue(0)` in render | Rule 5 | Use `const x = useMotionValue(0)` |
| `transition={{ duration: 1.2 }}` inline | Rule 6 | Use `motionTokens.duration.crawl` |
| `useEffect` without cleanup | Rule 7 | Return `removeEventListener` / `controls.stop` |
| SVG morph between paths with different commands | Rule 8 | Normalize path commands before animating |

## Related Skills

- **`motion-foundations`** — defines all tokens, springs, `useSafeMotion`, and SSR guards imported here. Must be set up before using this skill.
- **`motion-patterns`** — handles standard UI patterns (button, modal, stagger, page transitions, scroll reveals). Use it before reaching for the advanced patterns here.
