---
name: make-interfaces-feel-better
description: Apply concrete design-engineering details that make interfaces feel polished. Use when improving motion and interaction-feel details only — animation timing/easing, hover/press feedback, and micro-interactions. Do NOT use for states, responsive breakage, spacing/alignment, shadows, hit areas, or consistency drift, which belong to polish-pass.
metadata:
  origin: community
---

# Make Interfaces Feel Better

Use this skill for the small design-engineering details that compound into a
more polished interface.

Source: salvaged from stale community PR #1659 by `linus707`.

**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).

## When to Use

- The user says the UI feels off, flat, generic, cramped, jumpy, or unfinished.
- You are building controls, cards, lists, dashboards, navigation, forms, or
  toolbars.
- A component needs hover, active, focus, enter, exit, loading, or empty states.
- A frontend review needs specific before/after recommendations.
- For React/Next.js motion implementation, see the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`) — this skill decides the feel/timing; they provide the tokens and patterns.
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
it; Colors: none — the pointer does not choose colours.

## Core Principles

### Concentric Radius

For nearby nested rounded surfaces:

```text
outer radius = inner radius + padding
```

If padding is large, treat layers as separate surfaces instead of forcing the
math. The point is optical coherence, not formula worship.

### Optical Alignment

Geometric centering is not always visual centering. Icon buttons, play
triangles, arrows, stars, and asymmetric icons often need a small offset. Fix the
SVG when possible; otherwise adjust with a pixel-level margin or padding change.

### Shadows And Borders

Use borders for separation and focus rings. Use layered shadows when a card,
button, dropdown, or popover needs depth. Shadows should be transparent and
subtle enough to work across backgrounds.

### Text Wrapping

- Use `text-wrap: balance` on headings and short titles.
- Use `text-wrap: pretty` on short-to-medium body text, captions, descriptions,
  and list items.
- Avoid both on long prose, code, and preformatted content.
- Use `font-variant-numeric: tabular-nums` for counters, timers, prices, tables,
  and other updating numbers.

### Font Smoothing

On macOS, apply antialiased font smoothing at the root layout when the project
does not already do so:

```css
html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Image Outlines

Images often need a subtle inset outline so their edges do not blur into the
surface.

```css
img {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px;
}

@media (prefers-color-scheme: dark) {
  img {
    outline-color: rgba(255, 255, 255, 0.1);
  }
}
```

Use neutral black or white alpha outlines. Do not tint image outlines with the
brand palette.

### Motion

**Motion is the default, not an afterthought (fix #23 §2, MOTION_F23).** The feel/timing decisions made here include a deliberate-motion inventory per surface: what moves (entrances, staggers, dealt moments, micro-interactions, state transitions), what triggers it, and which fix #22 motion tokens it runs on (Group A principles + Group B values, e.g. stagger 30ms, press scale 0.97, dropdowns 150-250ms). A surface with no deliberate motion and no recorded reason fails -- a build that feels static fails, even if every static rule passes. Motion is recorded in the decision record with its D19 reason (Motion dimension) and its token values, directed per §10 (direct, don't describe). `prefers-reduced-motion` is respected everywhere with a complete static fallback -- content visible at rest, no entrance to fail -- never a broken one. (D19 -- Motion: the inventory IS the motion decision for the surface; Theme: motion is the dealt theme's motion voice; Texture: none -- motion carries no surface treatment; Visuals: deliberate motion is what makes the surface read as alive; Techniques: feel/timing decided here, implemented with the motion-* skills; Colors: none -- motion chooses no colours.)

Use CSS transitions for interactive state changes because they can retarget
when the user changes intent mid-motion. Reserve keyframes for staged
one-shot entrances or loading sequences.
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

Good motion defaults:

- Enter: combine opacity, small `translateY`, and optionally blur.
- Exit: shorter and quieter than enter, usually 150ms.
- Press: `scale(0.97)` for tactile buttons (the polish default — animate.md's 0.95–0.98 range, default 0.97), with a way to disable it when the
  movement distracts.
- Icon swaps: cross-fade with opacity, scale, and blur instead of instant
  visibility toggles.

**Default motion set (fix #17, v4-level).** Every page carries the default motion set — scroll entrances with a 1500ms fail-safe (M1/M2, on motion-governed surfaces; landing pages keep the Taste scroll ban except where a theme file records a scoped exception), hover micro-interactions on every interactive element (M3), life in existing pieces (M4), and at least one small interactive bit per page where the page has one (M5) — decided here for feel/timing, implemented with the motion-* skills. Reduced motion is respected in CSS and JS (M6). Each item is recorded in `docs/design-tokens.md`'s Motion list (surface → item → trigger/tokens/fail-safe).

**M3 — Hover micro-interactions on every interactive element (fix #17).** Every link, button, linked card, and linked photograph has a visible hover state per the hover layer (`references/motion.md`, hover-layer table) and the motion defaults (enter: opacity + small translateY; press: scale 0.97; transitions scoped to the changed properties, never `transition: all`). A hover may also warm a name's colour on a fill (never pink text on the paper ground), lift-and-pop a card or photograph on tap, or wiggle a sticker — each distinct hover behaviour is its own authored motion, recorded in `docs/design-tokens.md`'s Motion list. The step-6 check shoots a hovered card and a hovered photograph at 1440 (the existing Taste rule) and records hovered shots per interactive surface; an interactive element with no visible hover change is a finding, fed to the fix batch like other checks.

**M4 — Life in existing pieces (fix #17).** Every authored motion element already on the page — hero entrance, dealt hero loop (fix #15 R4), dealt moment, count, diagram pulse, effect/scene loop — must actually move in the rendered page. Ambient loops on existing pieces (a card's bob, a seal's breathe, a flag's sway, a heart's beat, a marquee's pause-on-hover) are authored motion too, each recorded in the Motion list with its trigger (on load / on scroll / on hover / timed loop / count). The D1 screenshot pass (and browser-qa's visual loop) confirms each one moves; a piece that should move and does not is a finding.

**M5 — At least one small interactive bit per page, where the page has one (fix #17).** Each page that carries an interactive surface — a stepper, toggle, tab, filter, counter, peek-list, or live total — must have at least one working interactive bit recorded in `docs/design-tokens.md` (name, surface, what it does, what state it shows). A page with an interactive surface and no recorded bit is incomplete — a static check item in step 6, never a screen verdict. A page with no interactive surface is exempt, and the exemption is recorded ('no interactive surface — none'). The bit is small: one control and its feedback, not a feature.

### Transition Scope

Never use `transition: all`. Specify the changed properties:

```css
.button {
  transition-property: transform, background-color, box-shadow;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}
```

Use `will-change` only for first-frame stutter on compositor-friendly
properties such as `transform`, `opacity`, and `filter`. Never use
`will-change: all`.

### Hit Areas

Interactive controls must have at least a 44x44px hit area (the plugin floor — quick-reference §2). Expand with a pseudo-element when the visible icon is smaller, but do not let expanded hit areas overlap.

## Review Output

When reviewing a UI polish pass, report concrete changes in before/after rows:

| Principle | Before | After |
| --- | --- | --- |
| Concentric radius | Same radius on parent and child | Parent radius accounts for padding |
| Tabular numbers | Counter shifts as digits change | Counter uses `tabular-nums` |
| Transition scope | `transition: all` | Explicit transition properties |

Include file paths and properties when they are not obvious from the snippets.
Omit principles that you checked but did not change.

## Checklist

- Nested rounded elements are optically coherent.
- Icons are visually centered.
- Buttons, cards, and popovers use borders or shadows for the right reason.
- Headings and short text avoid awkward wrapping.
- Dynamic numbers use tabular numerals.
- Images have neutral outlines where needed.
- Enter and exit animations are split, subtle, and interruptible where
  appropriate.
- Buttons have tactile active states without exaggerated motion.
- `transition: all` and `will-change: all` are absent.
- Small controls still have usable hit areas.
- Every interactive element has a visible hover state, with hovered shots recorded per interactive surface (fix #17 M3).
- Every authored motion element actually moves in the rendered page; each recorded in the Motion list with its trigger (fix #17 M4).
- Each page with an interactive surface has at least one working interactive bit recorded, or the exemption noted (fix #17 M5).
