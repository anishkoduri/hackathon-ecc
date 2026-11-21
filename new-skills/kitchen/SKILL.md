---
name: kitchen
description: Use when a build needs a tactile, physical-metaphor interaction — a receipt-printing checkout, a tactile button, a cassette audio player, a hold-to-confirm delete, a magnetic drop zone, playing cards, a stamp or ticket treatment, a scramble-text reveal, or a self-drawing loader — from dqnamo's Kitchen, or when the user names the Kitchen or a component by name. Copies the component from its page per project; never embeds component source in the plugin.
---

> **Hackathon-ecc note (fix #35, KITCHEN_F35).** dqnamo's Kitchen (dqnamo.com/kitchen, by dqnamo — a London-based design engineer) is 15 free component experiments: each component ships with its own code right on its page, copy and paste directly into a project. **Catalog + copy guide only:** this skill is a lookup, not embedded source. NO Kitchen `.tsx` or `.css` source is stored in this skill or in this plugin — components are copied from their page (or the repo file below) once, per project, at time of use. **License (verified Nov 17, 2026, from the source): ISC.** The repo `github.com/dqnamo/website` declares `"license": "ISC"` in its `package.json` (commit `0a517fea`, main; read via the GitHub connector), publishes no separate copyright line (`"author": ""`, no LICENSE file in the repo root), and is `"private": true` — the Kitchen is copy-paste, not an npm package. An independent third-party notice (norixahome.com/third-party-notices.txt) states the same: "The project declares the ISC license in its package.json and publishes no separate copyright line." ISC permits use, copy, modify, and distribution for any purpose with or without fee, provided the copyright notice and this permission notice appear in all copies — so every copied component keeps attribution to dqnamo (`dqnamo.com`) and the ISC permission notice. **Free-tier only:** all 15 components are free; no paid plan exists for the Kitchen. **React/Next.js:** the components are React (Next.js 16, React 19, Tailwind v4 in the source repo). Non-React builds do not use them directly — the pattern is re-implemented with the stack's own tools (same routing rule as React Bits). **Counts:** the 15 below were verified Nov 17, 2026 from the live Kitchen page and the repo's `components/experiment-catalog.ts` (`experimentCount = experiments.length + 1`); if the live Kitchen shows more, the live list wins. **Plugin rules override this skill where they differ:** every component is a §10 directive (component name + the surface + the job it serves, with a D19 reason); motion values come from the motion tokens, never hardcoded numbers; `prefers-reduced-motion: reduce` gets a complete static fallback. **Layer role: tactile** (inventory `skills/orchestrate/references/design-inventory.md` §12) — the tactile layer of the one design system: one memorable physical-metaphor interaction per surface, at most; the direction cites each component considered as USED or CONSIDERED-AND-REJECTED with a D19 reason, routed through the inventory, never around it.

# dqnamo's Kitchen — tactile copy-paste components

## What it is

The Kitchen is a set of 15 component experiments and interface studies by dqnamo — physical objects rendered as UI: things that print, spin, fill while held, pull toward a drag, fan out, and draw themselves. The standout quality is tactility: each component behaves like the object it pictures, which is what makes a surface feel alive instead of decorated. Use a Kitchen component when the brief calls for one memorable interaction, not as a general component library — the Kitchen has no form controls, no layout primitives, no data display. One Kitchen piece per surface, at most, and only where its job is real.

## The 15 components (verified Nov 17, 2026)

Get each one from its experiment page (`dqnamo.com/experiments/<slug>` — the page shows the live demo and its own code) or from the repo file (`github.com/dqnamo/website`, `components/`). Three components have no confirmed top-level repo file at the reviewed commit — those are page-only; do not guess a file path for them.

| Component | What it does | Page | Repo file |
|---|---|---|---|
| Tactile Button | A physical button study built from a shaped face, firm edge, and compressible depth | `/experiments/tactile-button` | `components/TactileButton.tsx` |
| Scramble Text | A compact text component that reveals changed text through an encrypted scramble | Kitchen index (custom card) | `components/ScrambleText.tsx` |
| Receipt Printer | A SaaS checkout state that prints a physical receipt when payment clears (demo: £230.40 Pro plan, annual) | `/experiments/receipt-printer` | `components/ReceiptPrinter.tsx` |
| Cassette Audio Player | A tactile audio player with turning reels and a compact-cassette control surface ("One Small Step") | `/experiments/cassette-player` | page-only (no `Cassette*.tsx` in `components/` at `0a517fea`) |
| Hold to Confirm | A deliberate action that fills while held, then offers a timed undo — prevents accidental deletes | `/experiments/hold-to-confirm` | `components/HoldToConfirmButton.tsx` (+ `UndoNotice.tsx`) |
| Magnetic Drop Zone | A file target that pulls toward an incoming drag before the file lands | `/experiments/magnetic-drop-zone` | `components/MagneticDropZone.tsx` |
| Dynamic Button | A button that smoothly resizes as its label animates | `/experiments/dynamic-button` | `components/DynamicButton.tsx` (+ `DynamicButtonV2.tsx`) |
| Playing Cards | A composable playing card, plus a fanned hand you can thumb through and play | `/experiments/playing-cards` | `components/PlayingCard.tsx` + `components/PlayingCardFan.tsx` |
| Ticket | A perforated ticket silhouette with composable sections and subtle parallax depth | `/experiments/ticket` | `components/Ticket.tsx` (+ `TicketPattern.tsx`) |
| Stamp | A reusable postage stamp frame for images, text, and custom React content | `/experiments/stamp` | `components/Stamp.tsx` |
| Scroll Fade List | A compact list surface with a soft overflow fade | `/experiments/scroll-fade-list` | page-only (no confirmed file at `0a517fea`) |
| Advanced Model Selector | A benchmark-informed picker with model configuration | `/experiments/model-selector` | page-only (no confirmed file at `0a517fea`) |
| Animated Signature | A reusable SVG signature component that draws itself on mount | `/experiments/signature` | `components/Signature.tsx` |
| Logo Trace Loader | A traced logo loader that resolves into a filled mark | `/experiments/logo-trace-loader` | `components/LogoTraceLoader.tsx` |
| Iridescent Foil | A layered CSS foil treatment that reacts to scroll and pointer | `/experiments/iridescent-foil` | `components/IridescentFoil.tsx` + `components/IridescentFoil.module.css` |

Second channel: dqnamo also publishes open-source React components on 21st.dev (self-drawing sparklines — `components/AnimatedSparkline.tsx` / `components/Sparkline.tsx` in the repo — logo-trace loaders, scramble text), previewed there and installed via shadcn. Where a Kitchen component is also on 21st.dev, either route installs the same component; the Kitchen page is the primary source.

## Copy (per project, at time of use)

1. Open the component's experiment page and read the code shown there (or the repo file above). Copy the component file — and only the files it imports — into the project.
2. Install only the dependencies the copied code imports. The source repo's dependency set is: `motion` (`^12.40.0`), `three` (`^0.185.1`), `@phosphor-icons/react`, `lucide-react`, `react-parallax-tilt`, `@number-flow/react`, `zustand`, `@base-ui/react`, Tailwind v4. Where a dependency already has a plugin pin (`three@0.185.1` is the R3F pin; GSAP is `gsap@3.15.1`), use the pin, never a floating install.
3. Keep the attribution with the copy: a comment naming dqnamo (`dqnamo.com`) and the ISC permission notice, next to the copied component. The repo publishes no copyright line, so the attribution is the record.
4. Record the component name, the page/repo source, and the source commit (`0a517fea` or newer, read at copy time) in the decision record (`docs/design-tokens.md`). A component copied without that record is an incomplete build.

## Workflow

### 1. Browse the live Kitchen — never from memory

Read the live Kitchen at `https://www.dqnamo.com/kitchen` and pick the component by the surface's job (the checkout that should print a receipt, the delete that must not fire by accident, the loader that should draw itself). Judge fit against the dealt theme and the brief — never by name alone.

### 2. Copy exactly one component for one job

Copy the single component the surface needs. Do not copy a component "to try it" without a surface that needs it, and do not copy a component whose job is already covered by a stronger element (record the rejection with its D19 reason). One Kitchen piece per surface, at most.

### 3. Theme-match it, then direct it

A Kitchen component arrives with its own defaults. Before it is accepted:

- Re-tint it to the dealt theme's tokens (never its stock palette on a themed build).
- Set its motion values from the motion tokens (duration, easing, stagger) — never the stock values where the theme's motion system says otherwise.
- Record it as a §10 directive: component name + the surface + the job it serves + the D19 reason.

### 4. Respect the reduced-motion fallback

Every copied component keeps its reduced-motion behaviour: under `prefers-reduced-motion: reduce` the animation is off and the content is fully visible at rest. A component that hides content when motion is reduced is not shipped — fix the fallback first, or do not copy the component.

## What NOT to do

- **No embedded source.** Never paste a Kitchen component's `.tsx` or `.css` source into this skill, into the plugin, or into a decision record — copy it into the project once, for this build.
- **No redistribution as a library.** ISC permits copying into the built app (use); publishing the copied components as a library or a template is not use — do not do it.
- **No dropped attribution.** Never copy a component without the dqnamo attribution + ISC notice — the license requires the notice in all copies.
- **No guessed file paths.** Three components are page-only at the reviewed commit — copy those from the page, never from a guessed repo path.
- **No non-React use.** Never install a Kitchen component on a non-React build — the routing rule sends non-React builds to the pattern re-implemented with the stack's own tools.
- **No stock defaults on a themed build.** A component shipped with its stock palette and stock motion on a dealt-theme build is a template read, not a design decision.
- **No paid plan.** There is none for the Kitchen — never pay for, subscribe to, or route around a paywall for a Kitchen component.

## Files

- The live Kitchen: `https://www.dqnamo.com/kitchen` (15 experiments)
- Source repo: `https://github.com/dqnamo/website` (components under `components/`; catalog `components/experiment-catalog.ts`; reviewed commit `0a517fea`, main)
- Second channel: 21st.dev (dqnamo's open-source React components — sparklines, logo-trace loaders, scramble text; shadcn install)
- License: ISC, declared in the repo's `package.json` (no LICENSE file, no copyright line published); corroborated by `https://www.norixahome.com/third-party-notices.txt`
- Design inventory entry: `skills/orchestrate/references/design-inventory.md` (§12)
