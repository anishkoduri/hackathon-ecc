---
name: threeui
description: Use when a build needs a ready-made 3D or WebGL component — a 3D hero section, a shader scene, an interactive 3D element or motion component — from ThreeUI (MengTo / DesignCode), or when the user names ThreeUI or a component by name. Catalog + install guide only: components install fresh per project from the npm package; never embeds component source in the plugin.
---

> **Hackathon-ecc note (fix #34, THREEUI_F34).** ThreeUI (threeui.com, by MengTo / DesignCode) is an open-source library of ready-to-use Three.js components — 3D hero sections, shader scenes, icons, and motion components — for React builds. **Catalog + install guide only:** this skill is a lookup, not embedded source. NO ThreeUI component source is stored in this skill or in this plugin — components are installed fresh per project from the npm package below. **License (hard constraint): MIT** — verified Nov 19, 2026 from the source repo (`github.com/MengTo/threeui`, commit `68802d54`): application code, Community component code, and ThreeUI-authored Community imagery are MIT; bundled open fonts stay under SIL OFL 1.1 and bundled Three.js runtime files stay MIT (see the repo's `ASSET-LICENSES.md` / `FONT-LICENSES.md` / `THIRD_PARTY_NOTICES.md`). Keep the MIT notice with any copy, and credit MengTo / DesignCode. **Free Community edition ONLY (free-set rule, same as `getlayers`):** the open-source Community catalog — 50 parent components, 111 routes, 141 free variants plus 23 singletons (164 browse results) at the reviewed baseline. Pro and Beta components are paid (Pro source is delivered to members through an authenticated CLI, never via npm) and are OUT — a build never installs, fetches, or recreates a Pro/Beta component. **Counts drift** (the Community catalog syncs from the main project): never freeze a count in a build or a decision record — read the live catalog at `https://threeui.com/` when you need current numbers. **React/Three.js only:** ThreeUI components are React + Three.js (WebGL). Non-React builds do not use them — Vanta or CSS/canvas treatments carry the depth there (same routing rule as React Bits). **Plugin rules override this skill where they differ:** every component is a §10 directive (component name + the surface + the job it serves, with a D19 reason); the component is the surface's ONE WebGL-heavy effect (WEBGL_ONE_F22); motion values come from the motion tokens, never hardcoded numbers; `prefers-reduced-motion: reduce` gets a complete static fallback. **Layer role: 3D components** (inventory `skills/orchestrate/references/design-inventory.md` §13) — the immersion toolkit of the one design system: the ready-made 3D layer the `motion-principles` immersion direction calls for; the direction cites each component considered as USED or CONSIDERED-AND-REJECTED with a D19 reason, routed through the inventory, never around it.

# ThreeUI — ready-made 3D components for React builds

## What it is

ThreeUI is a catalog of finished Three.js components — full 3D hero sections, shader-driven scenes, 3D icons, and motion components — each with live controls and variants, published as the open-source Community edition of DesignCode's ThreeUI. Where `react-bits` supplies animated 2D components and `gsap` animates what a build already renders, ThreeUI supplies the 3D scene itself: the turning hero object, the shader ground, the camera-travel moment. It is the fastest honest route to the immersion direction (`motion-principles` §5) on a React build — a real scene, theme-matched and directed, instead of a stock WebGL demo pasted behind a headline.

## Install (per project, at time of use)

Install the public Community package from npm, in the project:

```bash
npm install @designcodeio/threeui
```

Import the component and the shared styles:

```tsx
import { AtTheHorizon } from "@designcodeio/threeui";
import "@designcodeio/threeui/style.css";
```

For the smallest import graph, import a component by its subpath (`@designcodeio/threeui/components/<ComponentName>`). The installed copy in the project IS the pin: record the component name, the package version, and the surface it serves in the decision record (`docs/design-tokens.md`).

**Asset quirk (binding):** components that render full HTML documents expect their runtime files at the same root-relative URLs the ThreeUI preview uses. Copy the needed files from `node_modules/@designcodeio/threeui/lib-dist/assets/` into the app's public directory, or override the component's `sourceUrl` / `assetBaseUrl` prop where it offers one. A component that renders blank in the built app but worked in the preview has almost always missed this step — check it before debugging the scene.

## Workflow

### 1. Browse the live catalog — never from memory

Read the live catalog at `https://threeui.com/` (or the Community repo's browse grid) and pick the component by the surface's job — the hero scene, the shader ground, the 3D accent the brief calls for. Confirm the component is in the free Community set before considering it: if it is marked Pro or Beta, it is out, and the rejection is recorded with its D19 reason. Judge fit against the dealt theme and the brief, never by name alone and never from a frozen list in this skill.

### 2. Install, then theme-match it

Install the package, import the one component the surface needs, and re-dress it before it is accepted: its colors and materials take the dealt theme's tokens (never the demo scene's palette on a themed build), its motion values come from the motion tokens, and its camera/framing is directed per §10 (component name + exact parameters + the job it serves + the D19 reason). A ThreeUI scene shipped with its stock look is a template read, not a design decision.

### 3. Respect the immersion guardrails

A 3D scene is the heaviest thing on its surface, and it ships only with its fallbacks:

- **One WebGL-heavy effect per surface** (WEBGL_ONE_F22) — the ThreeUI scene is that effect; no second scene, shader ground, or Vanta layer shares the surface.
- **Performance budget:** the scene must hold its frame on a mid device — pause or stop rendering offscreen, and prefer the component's own controls for quality over bespoke optimization. A scene that janks the scroll is not shipped at that quality; step it down or fall back.
- **Static/2D fallback:** on mobile, low-power devices, and wherever WebGL is unavailable, the surface ships a static image/poster or 2D treatment of the same moment — designed, not a blank hole.
- **Reduced motion:** under `prefers-reduced-motion: reduce` the scene renders its finished still (or the static fallback) and any camera travel or ambient loop is off; the content is fully visible at rest.
- **Text over scene:** never behind text without a scrim and a 4.5:1 contrast check.
- **Cleanup:** the scene is destroyed/unmounted with its component — no orphaned WebGL contexts across routes.

## What NOT to do

- **No Pro or Beta components.** Never install the members' CLI, authenticate to the Pro source, or recreate a Pro/Beta component from its preview — the free Community set is the whole menu.
- **No embedded source.** Never paste a ThreeUI component's source into this skill, into the plugin, or into a decision record — install the npm package in the project, once, for this build.
- **No frozen counts.** Never write the catalog's component count as a fixed number in a build — read the live catalog; the baseline in the note above is a review record, not a promise.
- **No non-React use.** Never install ThreeUI on a non-React build — the routing rule sends non-React builds to Vanta or CSS/canvas depth.
- **No scene without a fallback.** A ThreeUI component with no static fallback, no reduced-motion still, or no scrim/contrast check over text is an incomplete build — a static check item, and `browser-qa` judges the rendered result.

## Files

- Live catalog: `https://threeui.com/`
- Source repo (Community edition, MIT): `https://github.com/MengTo/threeui`
- npm package: `@designcodeio/threeui`
- The immersion direction this toolkit serves: `skills/motion-principles/SKILL.md` (§5)
- Depth rules and the WebGL cap: `skills/design-taste-frontend/SKILL.md` (DEPTH_F22, WEBGL_ONE_F22)
