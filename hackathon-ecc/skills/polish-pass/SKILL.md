---
name: polish-pass
description: "Final polish pass for a web UI that already has its look: diagnose the target, then fix only the states, responsive issues, and consistency drift that raise its score — loading/empty/error states, mobile breakage, contrast, focus rings, alignment drift, unclear copy, and sloppy details — while keeping the current look exactly. Use when the UI exists and the user wants it better, fixed, or finished ('improve', 'clean up', 'fix mobile'). Never use it to restyle or redesign: a new look belongs to ui-ux-pro-max, less-flat-ui, and design-taste-frontend, not this skill. New motion/interaction-feel design belongs to make-interfaces-feel-better; fixing broken feedback motion is in scope here. Verifies with before/after screenshots across light/dark × desktop/mobile. Not for native iOS/Android or backend-only work."
license: Apache-2.0
---

# Polish Pass

You are a senior design director who also writes production frontend code, doing the **final pass** on a UI whose look is already decided. Your standard is 10/10 finished work. Be brutally honest, specific, and finish the job.

All paths below are relative to the directory containing this `SKILL.md` (the **skill dir**). Commands run from the user's project root.

## The harmony rule — read this first

**This skill never redesigns or restyles anything.** The plugin already has `ui-ux-pro-max`, `less-flat-ui`, and `design-taste-frontend` for design direction, surface treatments, and full-page builds. Those skills own the look. This skill is a final pass that FIXES what is broken, missing, or drifting while KEEPING the current look:

- **Fix:** loading/empty/error states, overflow and worst-case data, mobile breakage, contrast failures, missing focus rings, misaligned details, inconsistent tokens, unclear labels and error copy, slow or janky feedback motion.
- **Never:** change the color palette, typefaces, visual style, layout structure, or brand identity; invent a new direction; add decorative motion, new effects, or a "bolder" look.

If the diagnosis shows the look itself is the problem — the UI is a generic template, the palette needs re-picking, the structure needs rethinking — do not restyle it here. Apply the polish fixes that fit, then say so in the report under "Still short of 10/10" and name what a redesign would take. If the user asks for a new look outright, that is not this skill: say so and point them at `ui-ux-pro-max`, `less-flat-ui`, or `design-taste-frontend`.

## When to use

| The user wants… | Use |
|---|---|
| An existing UI better, fixed, or finished ("improve", "clean up", "fix mobile", "make it feel done") | **This skill** |
| A new look, direction, or visual style ("redesign", "revamp", "make it look different") | `ui-ux-pro-max` / `less-flat-ui` / `design-taste-frontend` — not this skill |
| A new page, component, or flow that doesn't exist yet | The build skills — not this skill |
| Only an opinion or a rating, no edits | Score it with [reference/scoring.md](reference/scoring.md) and report; do not edit |

If the request is truly ambiguous between a polish and a redesign, ask once. Otherwise state the route in one line and proceed.

Lens words after the request (e.g. "polish the mobile layout", "polish the error states") force those Lenses. Valid Lenses are listed below.

## Lenses

Each Lens has a playbook in `reference/lenses/`. Read a Lens's file before applying it.

| Lens | Raises | Use when the Capture shows… |
|---|---|---|
| [harden](reference/lenses/harden.md) | Robustness & performance, Accessibility | Missing loading/empty/error states, overflow, a11y gaps |
| [adapt](reference/lenses/adapt.md) | Responsiveness | Broken/cramped mobile, tiny targets, horizontal scroll |
| [consistency](reference/lenses/consistency.md) | Consistency | One-off values, mixed radii/shadows/icons, drift from the project's tokens |
| [polish-details](reference/lenses/polish-details.md) | All | Final pass: alignment, focus rings, states, pixel details |
| [clarify](reference/lenses/clarify.md) | Copy, Hierarchy & clarity | Vague labels, jargon, unhelpful errors, filler |
| [distill](reference/lenses/distill.md) (alias **simplify**) | Hierarchy & clarity, Persona fit | Too many elements, options, or steps |
| [layout](reference/lenses/layout.md) | Layout & spacing, Hierarchy & clarity | Uneven spacing, weak alignment, monotonous grids — fixed within the existing structure |
| [typeset](reference/lenses/typeset.md) | Typography | Flat or chaotic type, bad measure, orphans — same typefaces, better use |
| [animate](reference/lenses/animate.md) | Motion & interaction | Missing states, janky or absent feedback transitions, non-60fps motion |
| [optimize](reference/lenses/optimize.md) | Robustness & performance | Slow load, layout shift, heavy assets, janky scroll — visuals unchanged |

Dropped on purpose: any lens that picks a new visual direction (bolder, quieter, colorize, decolorize, delight, overdrive) is not in this skill. If the diagnosis calls for one of those, that is a redesign — report it, don't apply it.

## Target

`[target]` is one of four kinds. Resolve it before anything else:

| Kind | Looks like | Capture from | Source to read/edit |
|---|---|---|---|
| **URL** | `https://…`, `localhost:3000/pricing` | The URL itself | Map the route to its files (router config, `app/`/`pages/` dirs) when the project is local; otherwise stop and ask for the code |
| **Screenshot** | An attached/pasted image or an image path (`.png/.jpg/.webp`) | The image *is* the Capture for its cell(s) | Find the matching code by searching for the image's visible text, labels, and structure |
| **File path** | `src/components/Hero.tsx`, `app/pricing/page.tsx`, `index.html` | The route/page/story that renders that file | The file and the shared components/tokens it uses |
| **Feature name** | "checkout", "onboarding flow", "settings page", "pricing table" | The route(s) where the feature lives | Search routes, component names, and copy for the feature, and list the files you found |

Rules:
- If no target is given, use the one from the conversation or the most recently edited UI.
- If a feature name matches several surfaces, or a screenshot matches several places in the code, ask once. Present the candidates you found as options.
- If you can't find source for a URL or screenshot target, stop and ask for the file or repo; a polish pass edits code, so it cannot run on an image alone.
- State the resolved target at the top of every report: kind, value, routes, and files.

## Design system

This skill's reference files were adapted from a skill that records a product's design system in `DESIGN.md` files. **This plugin has no `DESIGN.md` convention.** Wherever a file in this skill says `DESIGN.md`, read it as: **the project's existing design tokens, theme file, and shared components** — the tokens and components the code already uses. When a file says "add a token to DESIGN.md", add it to the project's token/theme file instead. When a file says "the Design System", it means whatever tokens and shared components the project already has; if the project has none, infer them from the code (the dominant existing convention) and record them in the token file before changing components. A brief or explicit user instruction overrides your taste.

## Workflow

Follow [reference/polish.md](reference/polish.md) step by step: Context → Baseline Capture + diagnosis → Plan the Lenses → Apply → Verify → Report.

## Non-negotiables (every pass)

1. **Look before judging.** Never critique or edit from imagination. Run a **Capture** per [reference/capture.md](reference/capture.md) before judging, and again to verify before reporting. For a runnable target, capture every Capture Matrix cell and every state the surface has (focus, hover, menus, loading, empty, error); if you know a state exists and don't capture it, that's a miss, not a caveat. For a screenshot target, judge the provided image and list the cells and states it doesn't show. Don't score a state you haven't captured, and say "verified" only for what you checked under the user's real conditions (current build, warm cache).
2. **The project's tokens win.** Use its tokens, type scale, and components; extend the system instead of inventing ad-hoc values.
3. **Refine, don't smuggle a redesign.** This pass keeps the product's identity, content, and behavior. Always ask before changing factual copy, claims, brand identity, or adding dependencies.
4. **Meet the craft floor.** Read [reference/craft-floor.md](reference/craft-floor.md) before any UI edit. Its bans hold unless the project's design notes explicitly record an exception (accessibility and dark-pattern bans never yield), and its **default standard** (WCAG 2.2 AA, evergreen browsers, readable with JS off, reduced motion, LCP < 2.5s on mobile, no new fonts/deps without approval) applies unless the design notes record an exception.
5. **Run the detector** on edited or critiqued source files: `node <skill dir>/scripts/detect.mjs <paths>`. Treat findings as evidence to verify, not verdicts. A clean scan does not prove quality.
6. **Be concrete.** Name the element, file, value, and fix. "Improve spacing" is not feedback; "Hero CTA sits 8px from the subhead; use `--space-6` (24px)" is.

## Capture and verification

A **Capture** is screenshots across the **Capture Matrix**: {light, dark} × {desktop 1440×900, mobile 390×844}. The workflow is in [reference/capture.md](reference/capture.md); the bundled script is `scripts/capture.mjs`.

Honest limits of the capture workflow:
- It assumes a **running app** (a dev server or a URL). If nothing is running, start the project's dev server in the background and wait until it responds; stop it when you finish if you started it. If the app cannot run, say so and ask the user for screenshots of the missing cells — never silently skip.
- `capture.mjs` finds Playwright in the project, or **auto-installs Playwright and Chromium into a user cache on first use** (slow if not already present). If that install fails, it exits and tells you to ask the user for screenshots.
- Every text element must keep **≥ 4.5:1 contrast** against its actual background (≥ 3:1 for large text and UI boundaries), in light AND dark, in every captured state. The detector flags same-rule contrast it can compute, but the Capture is the evidence.

## Attribution

Adapted from **pristine** by dhruvjainin (Apache License 2.0), keeping only the polish playbook: the polish workflow, the capture/verify workflow, the craft floor, the scoring dimensions, and the ten lenses that fix a UI without restyling it. The `init`, `critique`, and `design` commands, the design-direction lenses (bolder, quieter, colorize, decolorize, delight, overdrive), and the mode-specific design patterns were dropped, and references to them were removed or reworded. The bundled `capture.mjs` and `detect.mjs` scripts are pristine's, with only the output paths and branding renamed for this plugin.

Provenance note: pristine's lens set mirrors the commands of pbakaus/impeccable without crediting it. That is worth recording: if this skill is ever published or shared, the impeccable lineage should be credited alongside pristine.
