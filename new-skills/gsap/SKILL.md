---
name: gsap
description: Use when the build needs JavaScript animation — timelines, scroll-driven animation, or canvas/DOM motion — and GSAP is the chosen engine, or when the user names GSAP, ScrollTrigger, or a timeline animation. Installs GSAP from the public npm package at build time; never vendors its source.
---

> **Hackathon-ecc note (fix #31, GSAP_F31).** GSAP (GreenSock Animation Platform, gsap.com) is a framework-agnostic JavaScript animation engine — the timeline / scroll / canvas specialist. **100% free, including every former Club plugin** (SplitText, ScrollTrigger, MorphSVG, DrawSVG, ScrollSmoother, Inertia, MotionPathHelper, CustomEase) for commercial use, from the public `gsap` npm package — no Club membership, no private registry, no auth token. **License (hard constraint): GSAP is NOT OSI open source.** It ships under Webflow's "Standard no charge" license (`https://gsap.com/standard-license`); the IP stays with Webflow, and the licence bans use in no-code visual animation builders competing with Webflow; Webflow can terminate it at its discretion. This plugin installs GSAP from npm at build time and **never vendors or redistributes its source**. **Pin:** `gsap@3.15.1` (npm latest, verified Nov 17, 2026) — install the pinned version, never bare `latest`. **Reference:** the official MIT agent skills at `github.com/greensock/gsap-skills` (8 skills: core, timeline, scrolltrigger, plugins, utils, react, performance, frameworks; install with `npx skills add https://github.com/greensock/gsap-skills`) are the deep API reference — read the one the work needs when this skill's patterns are not enough. **Plugin rules override this skill where they differ:** motion values come from the motion tokens (`motion-foundations`), never hardcoded numbers; `prefers-reduced-motion: reduce` gets a complete static fallback; one WebGL-heavy effect per surface (WEBGL_ONE_F22). GSAP is not a component library — it animates what the components render.

# GSAP — timeline, scroll, and canvas animation

## What it is

GSAP animates DOM elements, SVG, canvas, and WebGL scenes through tweens and timelines. It is the right engine when the brief calls for:

- **Timelines** — sequenced, choreographed motion (hero entrances, staggered reveals, multi-step transitions).
- **Scroll-driven animation** — ScrollTrigger: scroll-linked tweens, pinning, scrub, triggers that fire on scroll position.
- **Canvas / SVG motion** — MotionPath, MorphSVG, DrawSVG, physics and inertia plugins.
- **Framework-agnostic use** — vanilla JS, React, Vue, Svelte; the same core API everywhere.

It is NOT a component library and NOT a design system: it moves what exists, it does not supply the components. For components, use `react-bits` (React/Next) or the design package. For scroll smoothing, Lenis (`lenis`) is the smooth-scroll companion; GSAP drives the animation, Lenis drives the scroll.

## Install (build time, pinned)

```bash
npm i gsap@3.15.1
```

React builds also install the official React binding for the `useGSAP` hook:

```bash
npm i @gsap/react
```

Install from the public npm registry at build time, in the project — never copy GSAP source files into the project or the plugin, never check a GSAP bundle into the repo, never pin `latest`.

## Canonical patterns

Register plugins once per app, before any tween uses them:

```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
```

Prefer a single tween with transform aliases and `autoAlpha` over chained delays; prefer a timeline over a chain of tweens:

```js
gsap.to(".box", { x: 100, autoAlpha: 1, duration: 0.6, ease: "power2.inOut" });

const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2" } });
tl.to(".a", { x: 100 })
  .to(".b", { y: 50 }, "+=0.2")
  .to(".c", { opacity: 0 }, "-=0.1");
```

ScrollTrigger attaches to a timeline or a top-level tween; call `ScrollTrigger.refresh()` after layout changes:

```js
const tl2 = gsap.timeline({
  scrollTrigger: {
    trigger: ".section",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});
tl2.to(".panel", { x: 100 }).to(".panel", { rotation: 5, duration: 0.7 });
```

React: use the `useGSAP` hook with a scope, never a bare selector without one; clean up on unmount (the hook and `gsap.context()` both revert on cleanup):

```js
import { useGSAP } from "@gsap/react";
gsap.registerPlugin(useGSAP);
useGSAP(() => { gsap.to(ref.current, { x: 100 }); }, { scope: containerRef });
```

Next.js: GSAP needs a client boundary — animation code runs in a client component (`"use client"`), never in a server component. ScrollTrigger pinning and scrub are client-side only.

## Performance rules (binding)

- Animate transforms (`x`, `y`, `scale`, `rotation`) and `opacity`/`autoAlpha` — never layout properties (`width`, `height`, `top`, `left`) on a hot path.
- Batch ScrollTriggers; keep the trigger count small; `ScrollTrigger.refresh()` after fonts load or layout shifts, not on every frame.
- Durations and easings come from the motion tokens (`motion-foundations`), never invented numbers — the token is the directive.
- Every animated surface carries its reduced-motion fallback: under `prefers-reduced-motion: reduce`, transforms are off, content is visible at rest, and the fallback is a complete design, not a broken one (M6).

## When to reach for it — and when not to

- Reach for it for the hero entrance choreography, a scroll-linked section, a staggered reveal, a canvas/SVG animation, or any motion the motion-* skills describe but do not implement.
- Do NOT reach for it for a component (use `react-bits` or the design package), for smooth scrolling alone (Lenis), or for a CSS-only hover/press micro-interaction (the motion tokens + CSS cover those).
- A GSAP animation that is not theme-matched — wrong easing, wrong duration, motion that fights the dealt theme — is not applied, and the reason is recorded (D19).

## Deep reference

When the work needs API detail this skill does not carry (a plugin's options, a ScrollTrigger edge case, a framework lifecycle question), read the matching official skill from `github.com/greensock/gsap-skills`:

| Need | Official skill |
|---|---|
| Core API (`to` / `from` / `fromTo`, easing, stagger, defaults) | `gsap-core` |
| Timelines (sequencing, position parameter, labels, nesting) | `gsap-timeline` |
| ScrollTrigger (scroll-linked animation, pinning, scrub, refresh) | `gsap-scrolltrigger` |
| Plugins (ScrollTo, ScrollSmoother, Flip, Draggable, Inertia, Observer, SplitText, MorphSVG, CustomEase, and more) | `gsap-plugins` |
| `gsap.utils` (clamp, mapRange, interpolate, snap, toArray, and more) | `gsap-utils` |
| React (`useGSAP`, refs, context, cleanup, SSR) | `gsap-react` |
| Performance (transforms over layout, batching, ScrollTrigger tips) | `gsap-performance` |
| Vue, Svelte, and other frameworks (lifecycle, scoping, cleanup) | `gsap-frameworks` |

The official skills are MIT-licensed reference, fetched at use time from the repo — they are not vendored into this plugin.

## Files

- GSAP docs: `https://gsap.com/docs/v3/`
- Licence: `https://gsap.com/standard-license`
- Official agent skills: `https://github.com/greensock/gsap-skills` (`skills/llms.txt` is the skill index)
- The design package's GSAP presets (17 ready snippets), owned by this skill: `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17) stays the lookup source + `--domain gsap`
- Motion tokens and rules: `skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`
