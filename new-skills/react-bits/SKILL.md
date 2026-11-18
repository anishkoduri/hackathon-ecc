---
name: react-bits
description: Use when a React/Next.js build needs an animated component — a text effect, an animated background, an interactive UI piece, or a ready-made block — from the React Bits library, or when the user names React Bits or a bit by name. Installs the component fresh per project via the CLI; never embeds component source in the plugin.
---

> **Hackathon-ecc note (fix #31, REACTBITS_F31).** React Bits (reactbits.dev, DavidHDev/react-bits) is a free library of animated React components — text effects, backgrounds, interactive UI, ready-made blocks — that install as source you own, copy-and-own like shadcn/ui. **Catalog + install guide only:** this skill is a lookup, not embedded source. NO React Bits `.tsx`, `.jsx`, or `.css` source is stored in this skill or in this plugin — components are installed fresh per project at time of use, via the CLI below. **License (hard constraint): MIT + Commons Clause.** Free for personal and commercial use inside an app or product; the components themselves may NOT be sold, sublicensed, or redistributed — alone, bundled, or ported. **React/Next only:** React Bits components are React. Non-React builds do not use them (same routing rule as ShaderGradient: Vanta or CSS gradients on non-React builds). **Counts drift weekly** (new components land regularly): never freeze a component count in a build or a decision record — read the live catalog at `https://reactbits.dev/` when you need it. **Reviewed baseline:** the plugin reviewed the library at commit `9d9c687dc4f55b23539aa5417b703078047efa74` (fix #22 §11, REACTBITS_F22) — install fresh via the CLI and record the commit you installed in the decision record. **Plugin rules override this skill where they differ:** every component is a §10 directive (component name + exact variant + the job it serves, with a D19 reason); motion values come from the motion tokens, never hardcoded numbers; `prefers-reduced-motion: reduce` gets a complete static fallback.

# React Bits — animated React components, installed as source you own

## What it is

React Bits is a library of animated React components in five groups: Text Animations, Animations, Components, Backgrounds, and Micro Interactions. Each component ships in four variants — pick one per install:

| Variant suffix | Language | Styling |
|---|---|---|
| `-JS-CSS` | JavaScript | Plain CSS |
| `-JS-TW` | JavaScript | Tailwind |
| `-TS-CSS` | TypeScript | Plain CSS |
| `-TS-TW` | TypeScript | Tailwind |

The variant matches the project's language and styling: a TypeScript + Tailwind build installs `-TS-TW`; a JavaScript + CSS build installs `-JS-CSS`. Never install a variant the project does not use.

## Install (per project, at time of use)

One CLI command per component, from the project's root:

```bash
npx shadcn@latest add @react-bits/SplitText-TS-TW
```

Swap `SplitText` for the chosen component and the suffix for the project's variant. Import the installed component and render it in the React app. Or install by hand: open the component's Code tab on `reactbits.dev`, choose the language and styling, copy the files into the project, and install the dependencies listed there.

The installed copy in the project IS the pin: record the component name, the variant, and the source commit in the decision record (`docs/design-tokens.md`). A component installed without that record is an incomplete build.

## Workflow

### 1. Browse the live catalog — never from memory

Read the live catalog at `https://reactbits.dev/` and pick the component by the surface's job (the text effect the headline needs, the background the hero needs, the interaction the control needs). Judge fit against the dealt theme and the brief — never by name alone, and never from a frozen list in this skill (the catalog grows weekly).

### 2. Install exactly one variant

Install the single variant the project uses (see the table above). Do not install all four variants, do not install a component "to try it" without a surface that needs it, and do not install a component whose job is already covered by a stronger element (record the rejection with its D19 reason).

### 3. Theme-match it, then direct it

A React Bits component arrives with its own defaults. Before it is accepted:

- Re-tint it to the dealt theme's tokens (never its stock palette on a themed build).
- Set its motion values from the motion tokens (duration, easing, stagger) — never the stock values where the theme's motion system says otherwise.
- Record it as a §10 directive: component name + exact variant + the surface + the job it serves + the D19 reason.

### 4. Respect the reduced-motion fallback

Every installed component keeps its reduced-motion behaviour: under `prefers-reduced-motion: reduce` the animation is off and the content is fully visible at rest. A component that hides content when motion is reduced is not shipped — fix the fallback first, or do not install the component.

## What NOT to do

- **No embedded source.** Never paste a React Bits component's `.tsx`, `.jsx`, or `.css` source into this skill, into the plugin, or into a decision record — install it via the CLI or copy it into the project by hand, once, for this build.
- **No redistribution.** Never sell, sublicense, or redistribute the components — alone, bundled, or ported (MIT + Commons Clause). Shipping them inside the built app is use, not redistribution; publishing them as a library or a template is not.
- **No frozen counts.** Never write the library's component count as a fixed number — read the live catalog.
- **No non-React use.** Never install a React Bits component on a non-React build — the routing rule sends non-React builds to Vanta or CSS gradients.
- **No stock defaults on a themed build.** A component shipped with its stock palette and stock motion on a dealt-theme build is a template read, not a design decision.

## Files

- The live catalog: `https://reactbits.dev/` (Text Animations, Animations, Components, Backgrounds, Micro Interactions)
- Installation guide: `https://reactbits.dev/get-started/installation`
- Source repo: `https://github.com/DavidHDev/react-bits`
- The fix #22 pin and stack scope: owned by this skill (commit `9d9c687…`); the upstream vendored record stays in `skills/ui-ux-pro-max/SKILL.md` (§11, REACTBITS_F22)
- Motion examples in this plugin: `skills/motion-patterns/SKILL.md` (Code Examples)
