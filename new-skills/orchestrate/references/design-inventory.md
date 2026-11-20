# Design Inventory — every element the design package can use (fix #23 §1, INVENTORY_F23)

The orchestrator and the design-lead READ this file at the design-package
step (orchestrate step 3) BEFORE deciding anything, and the decision record
cites inventory entries USED vs CONSIDERED-AND-REJECTED, per entry, with a
fix #19 D19 reason. A design that could have been made without this package
— one that uses none of the inventoried elements beyond the bare minimum —
FAILS the ambition bar (AMBITION_F23). "Considered and rejected" must be
specific (why this element does not serve this build), never a blanket line.

Paths below are built-tree paths (`skills/...` as the plugin ships them).
Where a skill's staged home differs, the staged home is noted. Counts were
verified by reading the actual files (Nov 12, 2026); where a skill's own
header claim and its data file disagree, both numbers are given and the data
file is the inventory source.

Currency rule (INVENTORY_F23): this file is kept current — any future fix
that adds design elements updates it in the same change, with the new
entries, counts, and paths. A fix that adds an element and does not update
this file is incomplete.

## 1. ui-ux-pro-max — lookup-only inventory for dashboards, apps, components (fix #32: no longer the design lead)

Home: `skills/ui-ux-pro-max/SKILL.md` + `skills/ui-ux-pro-max/data/` +
`skills/ui-ux-pro-max/references/` (`pro-rules.md`, `quick-reference.md`).

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Styles — 89 rows in `data/styles.csv` (skill header describes 89 searchable styles, 51 active; the csv is the inventory source) | Named visual styles with palettes, effects, best-for / do-not-use-for, era, complexity | `skills/ui-ux-pro-max/data/styles.csv` | App/dashboard lookups after Taste sets the direction; never "modern clean" |
| Palettes — 192 product palettes | Product-type palettes with primary/secondary/accent/background/foreground/card/muted/border/destructive/ring + reasoning profiles | `skills/ui-ux-pro-max/data/colors.csv` | Colour decisions for an app surface; the palette balance comes from here (lookup — after Taste sets the direction) |
| Font pairings — 74 | Heading + body font pairings with mood keywords, best-for, import + Tailwind config | `skills/ui-ux-pro-max/data/typography.csv` | Type lookups on app surfaces after Taste sets the direction (Taste step 4a decides the pairing; `data/typography.csv` is the lookup source); re-dealt per build, never inherited |
| UX guidelines — 120 | Categorised do / don't rules with good/bad code examples and severity | `skills/ui-ux-pro-max/data/ux-guidelines.csv` | Any interaction, form, navigation, or feedback decision, as lookups after Taste sets the direction |
| Icons — 105 curated icons | Named icons with library, import code, usage, style, semantic role, allowed contexts | `skills/ui-ux-pro-max/data/icons.csv` | Iconography on any surface; the import code is the directive |
| GSAP presets — 17 | Ready GSAP snippets with trigger, duration, easing, framework notes, do/don't, performance notes | `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17) + `--domain gsap` | Motion on GSAP builds; ScrollTrigger is the scroll plugin (GSAP_F22). Usage skill: `skills/gsap/SKILL.md` (fix #31). Owned by the gsap skill (fix #32, D32-5); the CSV stays the lookup source |
| Chart types — 25 | Best chart per data type, secondary options, when to use / not use, volume threshold, colour + accessibility guidance | `skills/ui-ux-pro-max/data/charts.csv` | Any data surface, as a lookup after Taste sets the direction; the chart choice is a design decision, not a default |
| Stacks — 22 | Per-stack implementation guidance (react, nextjs, vue, svelte, astro, nuxtjs, nuxt-ui, angular, laravel, swiftui, react-native, flutter, jetpack-compose, html-tailwind, shadcn, threejs, javafx, wpf, winui, avalonia, uno, uwp) | `skills/ui-ux-pro-max/data/stacks/` (22 csv files) | Implementing the design on the build's actual stack |
| App-interface rows — 32; landing rows — 34; products rows — 192 | Searchable interface patterns and product references | `skills/ui-ux-pro-max/data/app-interface.csv`, `landing.csv`, `products.csv` | App-surface structure lookups; landing structure on app-led builds |
| Depth rules (DEPTH_F22) | Depth strategy rules: layered / deep-3D / parallax / Vanta / 3D-transform hero / camera-through-world, theme-matched, scrim + 4.5:1 over 3D | `skills/ui-ux-pro-max/SKILL.md` (depth rules) | Every surface's depth strategy as a lookup (orchestrate step 3) — the design-lead (Taste) applies the strategy; the rules are referenced, not led, here (fix #32, D32-3) |
| Design asset library pins (§11/§15/§17) | Pinned versions + stack scope for all 11 libraries/tools (see §9 below); owned by their per-skill homes, with the upstream vendored record in `skills/ui-ux-pro-max/SKILL.md` (§11/§15/§17) | `skills/ui-ux-pro-max/SKILL.md` (LENIS_F22 / GSAP_F22 / VANTA_F22 / REACTBITS_F22 / R3F_F22 / LIQGLASS_F22 / SHADERGRAD_F22 / LIQLOGO_F22 / CASBERRY_F22 / ORIGINKIT_F22 / DAISYUI_F22) | Any library effect; unpinned "latest" fails the pin check |

## 2. design-taste-frontend (Taste) — full landing / company pages

Home: `skills/design-taste-frontend/SKILL.md` + `skills/design-taste-frontend/references/` +
`skills/design-taste-frontend/library/` + `skills/design-taste-frontend/assets/`.
Staged home: `new-skills/design-taste-frontend/`.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Hero + dealt moments — 18 moments in the index, 13 dealt | Dealt moments (transition 4, text 4, hover 1, scroll 7, liquid 2); 5 retired, never dealt | `skills/design-taste-frontend/assets/moments/index.json` + `references/moments.md` | The hero moment and 1–2 dealt moments on every landing page, never skipped |
| Hero entrance | The hero enters on load through the motion layer (`data-enter`), text visible without script, 700ms safety mark | `skills/design-taste-frontend/references/motion.md` | Every landing hero; the entrance is part of the hero, not an add-on |
| Finish gate (`references/gate.md`) | The finish review: captivating-hero bar, specificity, and the checks a page must pass before it is done | `skills/design-taste-frontend/references/gate.md` | Before any landing page is reported finished |
| Sections library — 45 recipes | One system, one section per screen: nav, logo-row, quote-stat, bento, split-text, tabs-tour, app-frame, steps, photo-band, timeline-rail, booking-form, and 34 more | `skills/design-taste-frontend/references/sections-library.md` | Section structure; a recipe reused as-is is a catalogue item, not an invention (fails U1) |
| Palettes — 64 | Palette catalogue (json) | `skills/design-taste-frontend/library/palettes.json` | Landing palette candidates; the dealt theme picks, never a default |
| Type — 39 pairings | Type catalogue (json), incl. the `fraunces` pairing (display Fraunces, Figtree body) | `skills/design-taste-frontend/library/type.json` | Landing type; the pairing is re-dealt per build |
| Backgrounds / cards / copy / diagrams / effects / icons / layout / photos / scenes / sections / system | Per-kind reference inventories: backgrounds (111 lines), cards, copy moves/registers/tells/voice, diagrams, creative/object/usage effects, icons, layout-v4, photos, scenes, sections, system | `skills/design-taste-frontend/references/` (one file per kind) | The element kind the surface needs; each file is the catalogue for its kind |
| Motion reference | The page motion system: hero entrance, dealt-moment motion, hover layer, reduced-motion stills | `skills/design-taste-frontend/references/motion.md` | Any motion on a landing page; the Taste scroll ban stands (scrolling moves nothing but the dealt moment) |

## 3. Hallmark — the 50-theme catalog, sloplint, hero/finish reviews

Home: `skills/design-taste-frontend/references/hallmark/` (staged:
`new-skills/design-taste-frontend/references/hallmark/`).

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Theme catalog — 50 themes | Fifty dealt themes (almanac, arcade, atelier, bloom, blueprint, broadside, brutal, carnival, cobalt, console, coral, darkroom, dose, dusk, editorial, formwork, furrow, garden, grid, halftone, hedgerow, hum, ink, kiln, loom, lumen, manifesto, midnight, newsprint, overprint, pasteup, piste, refract, ribbon, rim, riso, solstice, specimen, spore, sport, squeeze, sticker, studio, terminal, terrazzo, ultraviolet, vantage, vellum, wayfind, werkstatt) | `skills/design-taste-frontend/references/hallmark/references/themes/` (50 theme files + README.md (51 .md files) + `index.json`) | The direction itself: the theme is DEALT, never chosen by taste |
| sloplint | The lint that flags template/slop reads in a build | `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` (+ `sloplint-render.mjs`) | Static check before the finish review; flags are candidate evidence, never a verdict |
| Hero review | The hero-review template: what makes a hero read as dealt vs template | `skills/design-taste-frontend/references/hallmark/references/review-hero.md` | Judging the hero (candidate evidence for browser-qa) |
| Finish review | The finish-review template: the final read before a page ships | `skills/design-taste-frontend/references/hallmark/references/review-finish.md` | The last check on a landing page |
| Gates + redesign | The gate definitions and the redesign procedure | `skills/design-taste-frontend/references/hallmark/references/gates.md`, `redesign.md` | Gating a build; any redesign follows this procedure with snapshot-before-redesign |

## 4. Impeccable — detector rules, craft floor

Home: `skills/polish-pass/reference/` (Impeccable lives inside polish-pass).
Staged home: `round2-skills/polish-pass/reference/`.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Detector rules — 62 | The slop detector: 62 rules (id, name, category, severity, description) flagging AI-generated-UI tells | `skills/polish-pass/reference/impeccable-detector-rules.json` | Static slop detection on any UI; a flag is candidate evidence, never a verdict |
| Craft floor | The floor every build must pass: contrast, colour system, typography, spacing/layout, theming variables, depth, states, mobile platform, browser surfaces, motion, copy — plus the bans (colour/surface, layout/structure, type/iconography, effects/motion, copy) | `skills/polish-pass/reference/craft-floor.md` (+ `impeccable-craft-floor.md`) | Every build, every surface; a floor/ban break blocks |
| Critique + extract + onboard | The critique template, the extraction notes, the onboarding guide | `skills/polish-pass/reference/impeccable-critique.md`, `impeccable-extract.md`, `impeccable-onboard.md` | Running an Impeccable critique; onboarding a new reviewer |

## 5. less-flat-ui — all 23 treatments

Home: the shared global Cursor skill `~/.cursor/skills/less-flat-ui/` —
READ-ONLY for this plugin (D-A2); the plugin ships the built copy at
`skills/less-flat-ui/SKILL.md`. Never edit the global source from this fix.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Treatments #1–#23 | Felt texture, Fluted glass, Thermal gradients, Water ripples, Speckled graphite, Single-hue landscapes, Blueprint grids, Halftone, Grainy gradients, Grass texture, Dithered images, Paper texture, Contour lines, Cloud sky, Pixel mosaics, Lens distortion, Stippled gradients, Square-dot grids, Blurred photos, Iridescent shapes, Impressionist paintings, ASCII and pixels, Soft shadow (#23 — also a depth cue, see §8) | `skills/less-flat-ui/SKILL.md` ("The 23 treatments") | Any surface that reads dull/flat; layer every compatible treatment that fits, theme-matched |
| Picker: match the mood | The treatment picker — which treatments fit which mood/theme | `skills/less-flat-ui/SKILL.md` ("Picker: match the mood") | Choosing treatments through the theme, not by taste |
| Record what you applied | The per-surface application record | `skills/less-flat-ui/SKILL.md` ("Record what you applied") | Recording treatments in `docs/design-tokens.md` |

## 6. Motion — motion-foundations / motion-patterns / motion-advanced

Home: `skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`,
`skills/motion-advanced/SKILL.md`. Upstream/ECC skills; patched by the
build.sh runtime-patch blocks, never by editing the built tree.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Group A principles A1–A12 | Disney's 12 principles reframed for UI: squash & stretch, anticipation wind-up, staging the focus, pose to pose, follow through, slow in & slow out, arcs, secondary action, snappy timing (timing), exaggerated feedback, solid drawing in 3D, overall appeal | `skills/motion-foundations/SKILL.md` (PRINCIPLES_F22) | Every motion decision names its principles in the decision record |
| Group A laws A13–A20 | UX laws that decide motion: Fitts's, bigger hit areas, Hick's, Miller's, Doherty threshold, Postel's, Jakob's, frequency of use | `skills/motion-foundations/SKILL.md` (LAWS_F22) | Any motion decision with a usability consequence |
| Group B tokens/rules B1–B20 | The 20 animation values/rules: B1 ease-out entrances; B2 dropdowns 150–250ms; B3 stagger rows 30ms; B4 press scale 0.97; B5 knob stretch 12%; B6 stagger as details settle; B7 arcs; B8 pulse to confirm; B9 ease-in-out moves; B10 popovers start 0.95; B11 enter from the trigger; B12 exit to the trigger; B13 no bounce on everyday UI; B14 don't tween while held; B15 exits 20% shorter; B16 overlap old & new states; B17 masks for reveals & colour; B18 crossfade icons + blur; B19 rubber band past bounds; B20 reuse the same layoutId | Tokens in `skills/motion-foundations/SKILL.md` (motionTokens/depthTokens); rules B11–B20 in `skills/motion-patterns/SKILL.md` (ANIM_RULES_F22); advanced rules in `skills/motion-advanced/SKILL.md` (ANIM_ADV_F22) | Every motion value on a build is a token value, never a hardcoded number (Rule 5); known open conflicts (B3 30ms vs Rule 5 floor 0.05s; B15 0.8x vs quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95) are carried as flags, never silently resolved |
| Motion tokens + springs | `motionTokens` (durations, easings, stagger, scale) and the `springs` map (snappy, gentle, bouncy, instant, release) | `skills/motion-foundations/SKILL.md` (Token system, ANIM_TOKENS_F22) | Any duration/easing/spring value |
| Code examples — motion-patterns | Button feedback, stagger list, dropdown (B2), modal, popover (B10/B11/B12), Thinking Orb (ORBS_F22), toast stack, page transition, scroll reveal, scroll progress bar, parallax layers + 3D-transform hero (DEPTH_F22), expanding card, shared-element crossfade, accordion, React Bits, R3F 3D scene, OriginKit, Casberry particle background | `skills/motion-patterns/SKILL.md` (Code Examples) | Implementing a motion pattern; the example is the implementation, not a sketch |
| Code examples — motion-advanced (17) | Draggable card, drag-to-dismiss sheet, reorderable list, swipe detection, long press hook, word-by-word reveal, number counter, SVG path draw-on, stroke progress ring, useScrollReveal hook, mask reveal (B17), stretching knob (B5), overlapping state change (B16), cursor follower, shimmer skeleton, button loading state, infinite animation with visibility pause | `skills/motion-advanced/SKILL.md` (Code Examples) | Advanced choreography a basic pattern cannot express |
| M1/M2 fail-safes (fix #17) | Scroll entrances on motion-governed surfaces (M1); the 1500ms fail-safe — content can never stay hidden (M2) | `skills/motion-foundations/SKILL.md` + `skills/motion-patterns/SKILL.md` (Rules 9–10) | Motion-governed (React/Next) app surfaces; Taste landing pages keep the scroll ban except a theme-recorded scoped exception |
| Reduced-motion rules | `prefers-reduced-motion: reduce` overrides everything: transforms off, opacity-only fades ≤ 0.2s, content visible at rest, complete static fallback (M6) | `skills/motion-foundations/SKILL.md` (Rule 3, Accessibility) + `skills/motion-patterns/SKILL.md` | Every motion decision, everywhere; the fallback is a complete design, not a broken one |

## 7. polish-pass — slop checklist, unslop fixes, Vercel checklist, accent checks

Home: `skills/polish-pass/SKILL.md` + `skills/polish-pass/reference/`.
Staged home: `round2-skills/polish-pass/`.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Slop checklist — 20 checks C1–C20 | Tags & pills, excessive italics, Instrument Serif, negative kerning, over-detailed UI, dividers, colour shades & opacities, bordered containers, over-detailed diagrams, verbose text, code breadcrumbs, section numbering, eyebrows, dithering, ASCII images, squircles, excessive mono, ALL CAPS subtitles, gradient backgrounds, periods in titles — FLAGS, not bans | `skills/polish-pass/reference/slop-checklist.md` (SLOP_F22) | Final polish on any UI; a recorded D19 reason + theme-fit clears a flag |
| Unslop fixes — 20 fixes D1–D20 | The fix per slop indicator: delete filler badges, drop redundant labels, unitalicise, mono only where needed, use a design system, show the actual product, …, animate useful feedback (D20) | `skills/polish-pass/reference/unslop-fixes.md` (UNSLOP_F22) | Fixing a flagged item; the fix is directed, not described |
| Vercel pinned-snapshot checklist — 16 groups, 104 rules | Pinned snapshot of the Vercel web-design guidelines: Accessibility, Focus States, Forms, Animation, Typography, Content Handling, Images, Performance, Navigation & State, Touch & Interaction, Safe Areas & Layout, Dark Mode & Theming, Locale & i18n, Hydration Safety, Hover & Interactive States, Content & Copy — candidate evidence, deduped against Impeccable + existing rules | `skills/polish-pass/reference/vercel-checklist.md` (VERCEL_F22) | Static audit evidence; PINNED SNAPSHOT only, never the live fetch |
| Accent checks — H1/H2 | Accent sprawl (one accent colour, sparingly + consistently for CTAs/active states/highlights) and accent hierarchy (deliberate emphasis order per screen) | `skills/polish-pass/reference/slop-checklist.md` (ACCENT_F22, ACCENTUATION_F22) | Any screen with an accent; sprawl is a flag |
| One WebGL-heavy effect per surface | A surface uses at most one WebGL-heavy library effect | `skills/polish-pass/reference/slop-checklist.md` (WEBGL_ONE_F22) | Any surface with a WebGL effect |
| Thinking Orb check | State-matched orb, never a generic spinner, never a mismatched state | `skills/polish-pass/reference/slop-checklist.md` (ORBS_F22) | Any AI/agent wait |
| Depth check | The z-axis check: layer order, elevation, parallax, occlusion | `skills/polish-pass/reference/slop-checklist.md` (DEPTH_F22) | Any surface with a depth strategy; the rules are a lookup (DEPTH_F22), applied by the design-lead (Taste) at orchestrate step 3 |

## 8. design-system + make-interfaces-feel-better

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| design-system — Mode 1 Generate | Generate a visual system (MASTER.md) for a project | `skills/design-system/SKILL.md` (Mode 1) | New design-system work; the first UI slice writes `design-system/<project-slug>/MASTER.md` |
| design-system — Mode 2 Visual Audit | Audit an existing system against the floor | `skills/design-system/SKILL.md` (Mode 2) | Checking a system that already exists |
| design-system — Mode 3 AI Slop Detection | Slop detection on a system | `skills/design-system/SKILL.md` (Mode 3) | A system that reads as generated |
| design-system — daisyUI component menu | The daisyUI 5 component menu (68 components) | `skills/design-system/SKILL.md` (DAISYUI_F22) | Tailwind builds needing a component library, re-themed to the brand deal |
| make-interfaces-feel-better — 9 principles | Concentric Radius, Optical Alignment, Shadows And Borders, Text Wrapping, Font Smoothing, Image Outlines, Motion, Transition Scope, Hit Areas | `skills/make-interfaces-feel-better/SKILL.md` (Core Principles) | Feel/timing decisions: how an interface should feel and when it should move — decided here before `--motion` sets intensity |
| make-interfaces-feel-better — default motion set (fix #17) | Scroll entrances + 1500ms fail-safe (M1/M2), hover micro-interactions (M3), life in existing pieces (M4), one interactive bit per page (M5), reduced motion respected (M6) | `skills/make-interfaces-feel-better/SKILL.md` (Motion) | Every page's baseline motion; recorded in the Motion list |

## 9. Fix #22 additions — glossary, accents, Mobbin, directives, libraries, Bang, Depth, Orbs

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Glossary — 20 terms G1–G20 | Kerning, optical centre, tabular numbers, layout shift, tracking, optimistic update, x-height, touch target, leading, origin-aware animation, OKLCH, widow, safe area, stagger, line length, affordance, combobox, interruptible animation, progressive disclosure, shared element transition — vocabulary, not rules | `skills/design-taste-frontend/references/design-glossary.md` (GLOSSARY_F22) | Using a term correctly in a decision record or directive |
| H1 colour accent (ACCENT_F22) | One accent colour, used sparingly + consistently for CTAs, active states, highlights | Orchestrate step 3 + `skills/polish-pass/reference/slop-checklist.md` | Any screen with an accent; sprawl is a polish-pass flag |
| H2 accentuation accents (ACCENTUATION_F22) | Deliberate emphasis hierarchy per screen (first/second/third, by size, weight, colour, spacing, motion, texture), recorded in the decision record | Orchestrate step 3 + `skills/polish-pass/reference/slop-checklist.md` | Every screen; a screen with no deliberate accentuation fails the check |
| Mobbin pattern research (MOBBIN_RESEARCH_F22) | Category + pattern level consultation of the Mobbin library (onboarding, paywall, feed, …) — inspiration, never copying, never the design source; free tier only, never blocked on Mobbin | Orchestrate step 3; `mobbin.com` (web browsing, free tier) | Before direction is generated, to know what patterns exist in the build's categories |
| Direct-don't-describe (DIRECTIVES_F22) | Design bots DIRECT with concrete executable directives (exact tokens, measurements, type, copy, motion values, layout) — never prose descriptions | Orchestrate steps 3–4 | Every implementer brief for a UI slice |
| 11 asset libraries/tools — menu, never defaults; one WebGL-heavy effect per surface | (1) Lenis `lenis@1.3.27` (smooth scroll, vanilla); (2) GSAP `gsap@3.15.1` (+ ScrollTrigger, all plugins; usage skill `skills/gsap/SKILL.md`); (3) Vanta `vanta@0.5.24` + `three@0.134.0` (hero shader scenes); (4) React Bits (commit `9d9c687…`, React/Next only; usage skill `skills/react-bits/SKILL.md`); (5) react-three-fiber `@react-three/fiber@9.8.2` (React 19) / `@8.18.0` (React 18) + `three@0.185.1` (the 3D layer for React); (6) liquid-glass-js (commit `78cb6cc…`, vanilla, no npm package — copy the files); (7) ShaderGradient `@shadergradient/react@2.4.20` (React/Next only; MIT declared but no root LICENSE file — recorded caveat); (8) liquid-logo (commit `689bb38…`, STANDALONE TOOL for the animated brand mark, never a runtime dep); (9) Casberry `particles.casberry.in` (STANDALONE TOOL exporting Three.js code — terms unresolved, exports BARRED from shipped builds until terms are confirmed, reviewed as untrusted code); (10) OriginKit (React/Next only, free tier 10 fetches/day, conditional/source-available licence); (11) daisyUI `daisyui@5.7.50` (Tailwind v4 plugin, 68 components) | Owned by their per-skill homes — `skills/motion-foundations/SKILL.md` (Lenis, R3F, Casberry), `skills/motion-patterns/SKILL.md` (React Bits, R3F, OriginKit, Casberry), `skills/design-system/SKILL.md` (daisyUI), `skills/design-taste-frontend/SKILL.md` (Vanta, liquid-glass, ShaderGradient, liquid-logo), `skills/gsap/SKILL.md` (GSAP), `skills/react-bits/SKILL.md` (React Bits); the upstream vendored record stays in `skills/ui-ux-pro-max/SKILL.md` (§11/§15/§17) | Where the library fits the build and the theme; each use is theme-matched with a D19 reason and directed per §10 |
| Bang Motion layer (pitch-deck-video, /demo only) | One continuous world, not slides: 10 style directions (cinematic dark, poster color-block, editorial light, paper & print, retro/analog, brutalist mono, pastel playful, luxury dark, flat pop with photos, grainy gradient) + 19 opener concepts + kinetic typography; camera-through-world architecture; GSAP 3.15.1 / Three.js 0.161.0 are Bang's versions as found, not plugin pins | `skills/pitch-deck-video/SKILL.md` (BANG_STYLES_F22, BANG_OPENERS_F22) | /demo videos only, on explicit invocation; never automatic |
| Depth tokens (DEPTH_F22) | `depthTokens`: perspective 1000px; parallax near 0.5 / mid 0.25 / far 0.1; tilt max 6°; elevation raised 8 / floating 16 / modal 24 (px blur) | `skills/motion-foundations/SKILL.md` (Depth tokens) | Every depth move; values are imported, never hardcoded (Rule 5) |
| Thinking Orb states — 9 (ORBS_F22) | `working`, `searching`, `solving`, `listening`, `connecting`, `weaving`, `composing`, `breathing` (idle/waiting — its label reads "Thinking…"), `shaping`; sizes 64 (chat-avatar) and 20 (inline-text); `thinking-orbs@0.3.2`; no "tenth" state, no state named "thinking" | `skills/motion-patterns/SKILL.md` (Thinking Orb) + tokens in `skills/motion-foundations/SKILL.md` | AI/agent waiting states only; state must match the actual activity; menu, not defaults |

## 10. Skill-bundled reference inventories (catalogs that ship with a skill)
Cross-note: this section duplicates §1/§2/§3/§4 entries — those sections govern; §10 is a quick index only.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Taste palettes + type | 64 palettes, 39 type pairings (json catalogs) | `skills/design-taste-frontend/library/palettes.json`, `type.json` | Landing palette/type candidates (see §2) |
| Taste asset catalogs | Moments (18/13 dealt), backgrounds, components, diagrams, effects, icons, layout, motion, objects, photos, scenes, system, ui | `skills/design-taste-frontend/assets/` | The element kind the landing surface needs |
| ui-ux-pro-max data catalogs | styles (89 rows), colors (192), typography (74), icons (105), charts (25), ux-guidelines (120), motion/GSAP presets (17), stacks (22) | `skills/ui-ux-pro-max/data/` | App/dashboard lookups after Taste sets the direction (see §1) |
| Hallmark theme catalog | 50 themes | `skills/design-taste-frontend/references/hallmark/references/themes/` | The direction deal (see §3) |
| Impeccable detector catalog | 62 detector rules | `skills/polish-pass/reference/impeccable-detector-rules.json` | Slop detection (see §4) |

## 11. Scoped exceptions (recorded decisions that narrow a rule)

| Exception | Rule it narrows | Scope | Reason |
|---|---|---|---|
| Variable fonts in the pitch-deck-video template (VARFONT_F26) | The static-only font rule (fix #19/#21; pitch-deck-video SKILL.md: "keep fonts self-hosted and static") | Template only: `skills/pitch-deck-video/template/public/fonts/HankenGrotesk.woff2` (34,704 B, variable wght 100–900) + `JetBrainsMono.woff2` (30,376 B, variable wght 400–500). Instrument Serif (`InstrumentSerif.woff2`, 21,032 B) stays static, weight 400 only. | The video renders in a single controlled Chromium and the output is a fixed video file, so the cross-platform variance the static-only rule guards against does not apply. App UI fonts stay static-only. Recorded fix #26 §4 (parent decision at the fix #25 close). |

## 12. Fix #31 additions — GetLayers, GSAP, React Bits, Hairline illustrations

Home: `skills/getlayers/SKILL.md`, `skills/gsap/SKILL.md`,
`skills/react-bits/SKILL.md`, `skills/hairline-create/SKILL.md`,
`skills/hairline-adopt/SKILL.md`. Staged home: `new-skills/` (same names).
All four resources are free-tier only; no paid plan is purchased for any of
them. Counts for GetLayers and React Bits drift weekly — this file freezes
no count for either; read the live library when you need the current numbers.
GetLayers prompts carry the most weight in the palette-first flow — they are
consulted FIRST, before the other palette sources, and the direction leans on
them heavily as its foundation (see the skill).

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| GetLayers — prompt-first cinematic layers (GETLAYERS_F31) | A curated library of visual layers for cinematic marketing sites: page templates, real-time 3D WebGL scenes, animated sections, animated/static backgrounds, pointer-reactive gradients. Every layer copies as one self-contained prompt an agent rebuilds in the stack. FREE SET ONLY; the MCP requires the Full Stack Lifetime plan and is NOT wired; the plugin vendors NO GetLayers content (reference only); a layer is a foundation, never shipped unchanged | `skills/getlayers/SKILL.md`; live library `https://getlayers.ai/`; live index `https://getlayers.ai/llms.txt` (current counts + category links) | Consulted FIRST in the palette inventory — the first-class foundation the direction leans on. A cinematic hero, animated ground, real-time 3D scene, or gradient ground on a marketing surface; a section whose motion is already designed. Never app UI; never a mismatched layer forced onto a surface. The direction cites the layers USED or CONSIDERED-AND-REJECTED, each with a D19 reason |
| GSAP — timeline / scroll / canvas animation (GSAP_F31) | Framework-agnostic JavaScript animation engine: tweens, timelines, ScrollTrigger, MotionPath, MorphSVG, DrawSVG, and every former Club plugin, 100% free for commercial use from the public npm package. NOT OSI open source (Webflow "Standard no charge" licence; bans competing no-code animation builders). Pin `gsap@3.15.1`; install from npm at build time, never vendor source. Official MIT agent skills (`github.com/greensock/gsap-skills`, 8 skills) are the deep API reference | `skills/gsap/SKILL.md`; presets (lookup source) in `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17); pin + stack scope in `skills/ui-ux-pro-max/SKILL.md` (§11, GSAP_F22) | Hero entrance choreography, scroll-linked sections, staggered reveals, canvas/SVG animation. Owned by `skills/gsap/SKILL.md` (fix #32, D32-5). Not a component library; not smooth scrolling alone (Lenis); not a CSS-only micro-interaction |
| React Bits — animated React components (REACTBITS_F31) | Animated React components (text effects, backgrounds, interactive UI, ready-made blocks) that install as source you own, copy-and-own like shadcn/ui. Four variants per component: JS-CSS, JS-TW, TS-CSS, TS-TW. MIT + Commons Clause (may NOT sell, sublicense, or redistribute the components). This skill is a catalog + install guide — NO component source is embedded anywhere in the plugin | `skills/react-bits/SKILL.md`; live catalog `https://reactbits.dev/`; install guide `https://reactbits.dev/get-started/installation`; reviewed baseline commit `9d9c687…` (fix #22 §11) | An animated component on a React/Next.js build, installed fresh per project via `npx shadcn@latest add @react-bits/<Component>-<JS\|TS>-<CSS\|TW>`. Never on a non-React build; never with stock defaults on a themed build |
| Hairline illustrations — interactive isometric SVG line figures (HAIRLINE_F31) | 33 interactive isometric SVG line figures that answer the pointer (Terrain, Turntable, Keyboard, Terminal, Branches, Vault, Router, Loupe, Sieve, and more). Zero runtime dependencies, ESM-only; React 18+ an optional peer. MIT (Lucas Marques). Install per project: `npm i @lucasmarkes/hairline@0.5.1` or `npx shadcn@latest add https://hairline.lucasmarkes.com/r/hairline.json`. Two skills: `hairline-create` draws a new figure from an idea; `hairline-adopt` rebuilds an existing SVG as a figure. NOT Hairline UI (hairlineui.com) — a different product, not in scope | `skills/hairline-create/SKILL.md` + `skills/hairline-adopt/SKILL.md` (vendored MIT copies); live figures `https://hairline.lucasmarkes.com` | Hero art, section illustration, or a thoughtfully designed empty state on dev-tool sites, technical docs, landing pages, portfolios. Best at 160–240px for empty states; figures fill the parent's width at a 5:4 aspect ratio |

## 13. Fix #34 additions — Motion Principles, ThreeUI

Home: `skills/motion-principles/SKILL.md`, `skills/threeui/SKILL.md`.
Staged home: `new-skills/` (same names). Fix #34 (ported from the
factory variant's round 10). The motion-principles skill is authored
natively from textbook public knowledge — no vendored source; the
originating reel's own skill file is not used. ThreeUI is a catalog +
install guide for the free Community edition only; Pro/Beta
components are paid and out (free-set rule). Neither skill carries
trigger keys — design skills route through this inventory and the
palette-first citation, the standing precedent (same as MotionSites,
GSAP, React Bits).

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Motion Principles — the why of UI motion (MOTIONPRINCIPLES_F34) | **Layer role: motion principles** — the why layer of the one design system: 19 principles (Disney's twelve adapted to UI + the HCI laws), each with its UI meaning, when to apply it, when to restrain it, and its numeric guardrail where one exists (Doherty: feedback within 400ms; timing: UI animation under 300ms; origin awareness; interruptible motion; frequency-of-use restraint), plus the immersion direction (depth and spatial continuity, full-viewport moments, scroll-driven progression, with binding restraint guardrails). Taste consults it whenever motion is decided and names the principle(s) in the D19 record; `gsap` implements against it; `browser-qa` renders the motion verdict from its checkable subset (MOTION-QA_F34) | `skills/motion-principles/SKILL.md` | Any motion decision — an entrance, a transition, a gesture, a scroll sequence, the dealt moment's movement — and any immersive surface. A motion with no named principle is not shipped; a principle claimed but not visible in the result is a finding |
| ThreeUI — ready-made 3D components (THREEUI_F34) | **Layer role: 3D components** — the immersion toolkit of the one design system: ready-made Three.js components (3D hero sections, shader scenes, icons, motion components) for React builds, by MengTo / DesignCode. MIT (verified Nov 19, 2026 from the repo, commit `68802d54`). FREE COMMUNITY EDITION ONLY — 50 parent components, 111 routes, 141 free variants + 23 singletons (164 browse results) at the reviewed baseline; Pro/Beta are paid and out. This skill is a catalog + install guide — NO component source is embedded anywhere in the plugin; components install per project from the npm package `@designcodeio/threeui`, with the runtime-asset copy step for full-document components | `skills/threeui/SKILL.md`; live catalog `https://threeui.com/`; source repo `https://github.com/MengTo/threeui` | A ready-made 3D hero, shader scene, or 3D accent on a React build — the immersion direction's fastest honest implementation. Never Pro/Beta; never on a non-React build; never without its static/2D fallback and reduced-motion still |

## 14. Fix #34 additions — Pre-build Research, the Design Contract

Home: `skills/prebuild-research/SKILL.md`. Staged home: `new-skills/` (same name). Fix #34 (ported from the factory variant's round 11). The research skill runs before the design package exists — it is the pipeline's pre-design step, not a design layer: it feeds feature expansion and the direction with researched fuel, under hard caps, and carries no trigger key (the orchestrate flow invokes it by name — the fix #31 design-skill precedent).

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| Pre-build research (RESEARCHBRIEF_F34) | **Pipeline role: research** — a bounded web sweep (≤4 searches + ≤4 fetches, primary sources only) run after scoping and before expansion + design, producing ONE compact brief (`docs/research-brief.md`, ≤ ~600 tokens): feature ideas for the expansion step + framework/architecture patterns for the project type, every source logged. Expansion records which ideas it took and which it dropped, each with a reason. Fuel, never authority — the decision record outranks the brief, and the anti-derivative rule stands | `skills/prebuild-research/SKILL.md` | Every first build, at orchestrate step 1.5; any later run that re-opens scope. Never mid-build (a mid-build question is a brief gap, not a research phase); never blocked on — an unreachable source set records the gap and the build proceeds |
| The design contract (DESIGNCONTRACT_F34) | **Design-package artifact** — Taste step 4a's frozen system issued as a binding contract in `docs/design-contract.md`: hosting line (HOSTING_F34), palette tokens, type scale, spacing scale, motion specs (principles + guardrails cited), named components with inventory citations, states, and a Deviations field. Implementers implement it literally; the pre-build restatement gate checks the implementer's read-back against it before the build; `browser-qa` verifies the built screens against it (CONTRACT-QA_F34) | `docs/design-contract.md` (per project, written by the design-lead); the form lives in `skills/design-taste-frontend/SKILL.md` step 4a | Every build with a UI surface — the contract is what implementers build from and what QA verifies against; a design decision not in the contract is not yet a build input |

## 15. code-mode — the execution discipline (fix #34, CODEMODE_F34)

**Layer role: none — this is an execution entry, not a design element.** It
is catalogued here for the same reason §14 catalogues the pipeline steps:
the inventory is the one place a reader can find every named capability the
plugin carries.

- **code-mode** (`skills/code-mode/SKILL.md`, + the helper library in
  `skills/code-mode/scripts/`) — the script-first discipline for the
  orchestrator's data-heavy mechanical work: ONE gated program, a distilled
  digest of at most 500 E3 back, raw output in files (SCRIPT-FIRST_F34,
  SCRIPT-GATE_F34). Reach for it when a step's work is scanning, filtering,
  counting, or transforming across many files — never for a design decision,
  a verdict, or a subagent's work (subagents do not run these scripts). It
  carries no trigger key by design: `orchestrate` and `browser-qa` invoke
  it by name (the routing decision is recorded in fix34/SPEC.md).

## How the record uses this file (the ambition bar, AMBITION_F23)

1. At the design-package step, the orchestrator and the design-lead read this
   file BEFORE deciding. The decision record then lists, per build: which
   inventory entries were USED (entry + surface + D19 reason) and which were
   CONSIDERED-AND-REJECTED (entry + the specific reason it does not serve
   this build — never a blanket line).
2. A build that uses only a small slice of the inventory without recorded
   specific reasons for the rest FAILS the ambition bar.
3. A design that could have been made without this package — none of the
   inventoried elements beyond the bare minimum — fails the ambition bar.
4. Ambition is MORE elements, MORE motion, MORE decisions — not louder.
   "More, not bolder" stands; a loud but thin build still fails.
5. F6 (impressive is the governing bar) is the PRIMARY gate: browser-qa
   judges impressive AND ambitious, not just rule-correct. A rule-correct
   but unambitious design fails.
