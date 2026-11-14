---
name: design-system
description: "Generate a design system from an existing codebase or audit one for visual consistency: extract tokens (colors, typography, spacing, shadows) into design-tokens.json and CSS custom properties with DESIGN.md rationale and an interactive HTML preview, score the UI across 10 dimensions, and flag AI-slop patterns. Use when starting a design system, auditing visual consistency before a redesign, or reviewing a PR that touches styling."
metadata:
  origin: ECC
---

# Design System — Generate & Audit Visual Systems

## When to Use

- Starting a new project that needs a design system
- Auditing an existing codebase for visual consistency
- Before a redesign — understand what you have
- When the UI looks "off" but you can't pinpoint why
- Reviewing PRs that touch styling

## How It Works

### Mode 1: Generate Design System

Analyzes your codebase and generates a cohesive design system:

```
1. Scan CSS/Tailwind/styled-components for existing patterns
2. Extract: colors, typography, spacing, border-radius, shadows, breakpoints
3. Generate the direction through the design package skills (`ui-ux-pro-max` direction / `design-taste-frontend` / dealt Hallmark theme) and record it in `design-tokens.md` — never competitor sites and never a searched external reference (orchestrate row-10 anti-derivative rule)
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.
4. Propose a design token set (JSON + CSS custom properties)
5. Generate DESIGN.md with rationale for each decision
6. Create an interactive HTML preview page (self-contained, no deps)
```

Output: `DESIGN.md` + `design-tokens.json` + `design-preview.html`
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
shipped unexamined.)

### Mode 2: Visual Audit

Scores your UI across 10 dimensions (0-10 each):
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

```
1. Color consistency — are you using your palette or random hex values?
2. Typography hierarchy — clear h1 > h2 > h3 > body > caption?
3. Spacing rhythm — consistent scale (4px/8px/16px) or arbitrary?
4. Component consistency — do similar elements look similar?
5. Responsive behavior — fluid or broken at breakpoints?
6. Dark mode — complete or half-done?
7. Animation — purposeful or gratuitous?
8. Accessibility — contrast ratios, focus states, touch targets
9. Information density — cluttered or clean?
10. Polish — hover states, transitions, loading states, empty states
```

Each dimension gets a score, specific examples, and a fix with exact file:line.

### Mode 3: AI Slop Detection

Identifies generic AI-generated design patterns. **Scope — pattern evidence, not a distinctiveness verdict:** the patterns below are code-level evidence (they exist in the code); a slop finding — including "Generic hero with centered text over stock gradient" — is candidate evidence for `browser-qa`, never a verdict that a screen reads as a default template. Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by `browser-qa` in the visual loop. Append slop findings to `.hallmark/candidate-evidence.md` with the screen and pattern for `browser-qa` to judge.

```
- Gratuitous gradients on everything
- Purple-to-blue defaults
- "Glass morphism" cards with no purpose
- Rounded corners on things that shouldn't be rounded
- Excessive animations on scroll
- Generic hero with centered text over stock gradient
- Sans-serif font stack with no personality
```

## Examples

**Generate for a SaaS app:**

Invoke the `design-system` skill: generate a system with style minimal and palette earth-tones.

**Audit existing UI:**

Invoke the `design-system` skill: audit the UI at http://localhost:3000, pages / /pricing /docs.

**Check for AI slop:**

Invoke the `design-system` skill: run a slop-check.
