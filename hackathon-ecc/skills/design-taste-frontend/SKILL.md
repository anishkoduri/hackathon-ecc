---
name: design-taste-frontend
description: >-
  Taste skill v2.5.1 (design-taste-frontend), the anti-slop frontend skill. Builds professional company websites at the level
  of figma.com and x.ai: plain copy in a voice of its own, one system, one section per screen,
  equal edges, real photographs and real product UI (licensed stand-in photographs when the client
  has none; a product render only when the brief asks for 3D), a hero entrance and one or two dealt
  moments on every page, shader effects and scenes only on tech, gaming and software pages, quiet
  micro-interactions, and a checker and finish gate that enforce it in a real browser. Use ONLY for a full company or landing-page build from scratch, or a full-page redesign where
  this skill leads the page system — a landing page, company, product, shop, cafe, hotel, studio,
  SaaS, AI, developer-tool or game site, as static HTML/CSS or inside an existing React, Next.js,
  Vue, Svelte, Astro or Tailwind project, or when the user says a page looks generic, templated or
  "AI-made". Do NOT use for dashboards, apps, components, or fixes to existing UI — those belong to
  ui-ux-pro-max (dashboards/apps/components) and polish-pass (fixes to existing UI).
---

# Taste skill v2.5.1

Build the website a good company would ship: it says plainly what is sold, shows the real thing on
every screen, and looks made for this client, not from a template and not like an art piece.
figma.com and x.ai are the bar (in words: `layout-v4.md` section 1).

`<skill>` is this folder. It needs Node 22+ and Chrome, Edge or Chromium (ffmpeg optional).

## House rules

These nine win over everything else in this skill.

1. **No caption or description under any image, render or visual.** Licence credits go in one
   footer line.
2. **Every visual renders, never an empty ground,** at 1440, 1024, 768 and 390.
3. **One section per screen:** the hero alone on the first screen, every section exactly one or
   two screens tall at 1440x900, no second section heading peeking in. The one exception is a
   live `photo-chapters` section, three or four screens, set by the moment.
4. **Equal left and right content edges.**
5. **Hover micro-animations:** a linked card lifts 2px, a photo zooms 1.02-1.03 inside its frame,
   buttons step on hover and press on click, underlines draw, card loops cycle in 2.5-4 s, repeat
   and restart on hover. The motion layer does it; never strip or override it. No tilt, carousels
   or timed tabs. Every hero enters once on load (`data-enter`), and every page carries one dealt
   moment, two on a long page (the gate holds both).
6. **More and better real photographs where they fit;** nicer backgrounds; better heroes, layouts
   and fonts.
7. **Real full-colour icons** (a known product's real icon, never a drawn one); small diagram
   visuals in cards (a hub with branches; one input, a main processor, three parallel lanes;
   pulses running along the lines).
8. **The big award-site scenes and creative moments are part of the skill:** every page deals its
   moments (photo- and type-led off tech), but shader effects and scenes only where the trade has a
   technical subject (tech, AI, developer tools, gaming, fintech, hardware), never on a local cafe,
   bakery, guesthouse or shop: those get photographs.
9. **Addresses:** street and district only (no street given: the district), no house number, postcode or coordinates; no register
   or VAT numbers; no phone in a real format; contacts on `.example`.

**Captivating hero — the bar:** the hero's first view must make the product's most surprising moment visible immediately. Test: a first-time visitor can name, in 5 seconds and without scrolling, the one surprising thing this product does; if they cannot, the hero falls short of this bar — record that as candidate evidence for `browser-qa`, whose visual-loop verdict alone decides whether the hero passes the distinctiveness bar, even if every other check passes.

**Hero — amazing, dealt, recorded (fix #23 §4, HERO_F23).** The hero surface — a landing hero, or the home/feed surface of an app — gets a dealt amazing moment: a dealt moment + a distinctive composition + motion, recorded in the decision record (`docs/design-tokens.md`) as the hero-moment line (the dealt moment, the composition, the motion values, with its fix #19 D19 reason). The hero is the highest-weight `browser-qa` surface: a merely adequate hero fails F6, however correct the rest of the page is. Calibration: on a phone-first utility app the home/feed surface IS the hero surface and still gets the moment treatment, but the amazing bar is calibrated to the product — the moment must serve the product's job (the thing the user opens the app to do), not decorate it. "Amazing" never means a generic hero section pasted onto an app that does not need one, and never a louder hero — "more, not bolder" stands. The hero-moment line is also written to the Picks block (`.hallmark/picks.md`, Hero-moment row) at the deal, so the hero review judges the hero against the moment it was dealt.

- **D19 (for the hero moment)** — Motion: the moment's entrance, stagger, and loop are the hero's motion, named with token values; Theme: the moment is the dealt theme's material made visible (its hero posture, its signature); Texture: the moment carries the theme's surface treatment where the theme gives it one, or `none — <reason>`; Visuals: the composition is distinctive — the product's own thing at true size, never a centred stack; Techniques: the moment routes through the dealt moment, the hero deal, and the motion tokens; Colors: the moment uses the theme's own tokens; Depth: the moment names its layer order (what sits in front, what sits behind).

**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).

## 1. The kind of business decides everything

Write the kind on the plan's first line and declare it on the page: the page type on
`<html data-type>` and `<meta name="page-type">` (the same value), and `<meta name="site-kind">`;
a place adds `<meta name="page-kind" content="place">`. The dealers take the last column
(`start.mjs --page`, `moments.mjs --page`), the hero dealer the page type; `consistency.mjs` reads
the metas.

| Brief | page type | site-kind | kind |
|---|---|---|---|
| App, SaaS, AI, developer tool, fintech or banking app, a studio selling its own software | software | software | software |
| A game, a studio launching its game | software | gaming | gaming |
| Hardware or a tech device (a drone, a robot arm, a keyboard) | product | tech | tech |
| Any other physical product or brand (a chair, a bike, coffee beans sold online) | product | other | product |
| People are hired: clinic, law firm, agency, creative studio, trade | service | other | service |
| People come to it: cafe, bar, bakery, restaurant, guesthouse, small hotel, shop, florist, bike shop, gym, local studio | place | other | place |

A maker that also opens its door or teaches (a ceramics studio, a bakery with a web shop) is a
**place**; its web shop becomes the goods section. It is a product only when nothing happens at the door.

"Tech" below means site-kind software, gaming or tech; "other" is everything else. Effects,
scenes, loops, counts, CSS grounds, dark pages and dark heroes are tech only. An other page is
photographs, flat colour, type, real icons, the hero's entrance, its dealt moment (photo- or
type-led, `moments.md`) and the hover layer.

**Texture boundary with `less-flat-ui`.** This skill owns the whole page system: every
section it lays out — including a flat-colour section — is styled by the page system, so do
NOT texture it. `less-flat-ui` texture applies only to a surface the page system leaves
unstyled (for example a bare app-chrome panel or an unstyled utility surface inside the
`app-frame`), never to a section of the page itself. If a section looks flat, that is the
page system's choice, not a gap to fill.

## 2. The page plan by kind

The full plans, deal lists and section order: `references/sections.md`.

- **Place** (a cafe, bakery, guesthouse, shop). Photographs lead: 12 to 20 on the full page, 8 to
  12 compact, under 8 frames the 3-screen short page, whatever the trade; no client photographs:
  the draft path and a live search (`photos.md`), then count; the palette dealt by trade. The hero
  a photograph whenever a frame fits (a remote place: its region's landscape), the visit block on
  screen two, the offer, the place, orders or booking.
  **Variety without effects** (`sections.md` section 4): the offer and the place deal different
  compositions, never two sections round one picture; one type moment (the address or name set large); one main action a screen; list text 16px. Flat grounds, square
  photographs, one button style, the phone bar, the dealt moments; no effect, ground, loop,
  fragment, diagram or tab.
- **Product and service** (site-kind other). Photographs lead: the product, the people, the rooms,
  the work, two or more a screen on a product page. Real icons for the tools a studio uses; one
  still diagram at most; flat grounds and one brand band. No shader effect, print, grain, gradient,
  scene or loop (the dealt moments only); WebGL only for a product render the brief asks for. **A
  physical product with no photographs is shown in photographs:** stand-ins of the same kind of
  thing from `photos.mjs search`, each listed in the report, on the full product page; a render
  (`assets/objects/product-render`, stills) only when the brief asks for 3D or a render; never a
  drawing, mood stock or a set of props (`sections.md`, Product).
- **Every product page** (photographed, in stand-ins or rendered on a 3D ask, hardware too; the bar is Figure and 1X;
  `sections.md`, Product): the product **big** where it stands
  whole (most of its frame, or on the ground at anchor scale), never mid-size in a grey rounded
  panel on a grey ground; **a different picture each section**, never one view twice; **every headline promise pictured** (a family bike shows the child bench); dealt
  compositions, no structure twice, one contrasting ground; the **swatch changes the picture**,
  every colour shown once; **no fact twice**; buttons step and press (rule 5).
- **Tech** (software, gaming, hardware). The client's own subject leads at true size. Software: its
  own UI as live HTML showing what it works on (a code-review tool: a red and green diff with its
  Accept action) in one `app-frame`, never a generic dashboard or only fragments on panels; cards:
  fragments on lit panels, pulsing diagrams, real icons. Hardware: its photographs, else stand-in
  photographs of its kind (a render only when the brief asks for 3D), never a split hero of only
  an order form or a drawn SVG. A game: its name in the h1, a launch line, its world as full-bleed
  key art (else its name set large over stand-in photographs of its setting), an effect never in
  its place (`sections.md`, Gaming). **60 to 80 words a screen** outside UI mocks (`copy.md`). By
  deal: **one effect** (a shader ground in the hero or the one `[data-visual]` frame, a WebGL
  part, an object or one big scene) and **one or two moments** in their own sections; four live
  WebGL contexts at most; no card moves with the scroll (`effects-usage.md`).
- **Animated 3D backgrounds come from Vanta (fix #22 §11, VANTA_F22).** Where the deal calls for the one effect as a shader ground or a big scene — tech, gaming, software, hardware only — the approved source is Vanta (`vanta@0.5.24`, MIT, plus `three@0.134.0`, the README-documented pair; vanilla JS; three.js-backed effects: WAVES, BIRDS, NET, FOG, CLOUDS, GLOBE, and the rest). The effect is directed per §10 (effect name + exact parameters: colour, scale, speed, mouse/touch controls on or off), recorded in `docs/design-tokens.md` with its fix #19 D19 reason — a Vanta scene is the dealt moment or the hero background, never a default wash. Constraints, all binding: theme-matched (the effect's colours are the theme's own tokens); a static fallback (the theme's gradient or image ground) on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; one Vanta scene per page by default (the four-WebGL-context cap above still binds); destroy the effect on unmount (`effect.destroy()`). p5.js-backed Vanta effects (e.g. TRUNK) are not covered — no p5 pin, recorded-gap if a build wants one. A Vanta background with no reduced-motion fallback or no scrim/contrast check is an incomplete build — a static check item in step 6, never a screen verdict. (D19 — Motion: the scene's motion is the dealt moment's motion; Theme: theme-matched, colours are the theme's own tokens; Texture: the animated ground is the page's texture layer; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: Vanta + three.js at the pinned pair, destroy on unmount; Colors: effect colours are the theme's own tokens, never invented.)

- **Depth as a dealt moment / theme element (fix #22 §13, DEPTH_F22).** 3D is a dealt moment and a theme element, not a coat of effects: a shader scene, a Vanta background, or a 3D hero element is the page's depth moment where the deal calls for one, and the depth strategy for every surface is named in the design package (orchestrate step 3, DEPTH_F22) — flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world. A dealt moment CAN be a depth moment (fix #15 R1/R4/R5): where the deal returns a moment that reads in depth (a hero object that turns, a scene the camera travels through), the moment is recorded with its depth values, not just its look. Cross-references, do not duplicate: Group A A11 solid drawing in 3D (`motion-foundations` Principles, PRINCIPLES_F22) — an object keeps believable volume while it moves; Bang Motion's camera-through-world (§12) — the camera IS depth in motion, and the one-world / moving-camera / persistent-subject architecture is the deep-3D strategy for the video's motion layer; Vanta 3D backgrounds (§11, VANTA_F22 above) — the depth source for hero scenes; GSAP 3D transforms (§11) — the implementation for 3D motion on web builds; fix #20 F6 — depth is one of the ways a design earns "impressive". Depth is directed per §10 (effect name + exact parameters: layer order, elevation levels, parallax distances, perspective values, transform parameters), recorded in `docs/design-tokens.md` with its D19 reason (seven dimensions, Depth included). A 3D hero element with no named depth strategy, no theme reason, no scrim/contrast check (4.5:1), or no reduced-motion fallback is an incomplete build — a static check item in step 6, never a screen verdict.

- **D19 (for the depth-as-dealt-moment rule)** — Motion: the depth moment's motion is the camera move, the parallax, or the 3D transform — named with its values; Theme: the depth moment is the dealt theme's depth (brutalist hard offset shadows, luxury soft elevation, sticker die-cut layers); Texture: the depth moment may carry a `less-flat-ui` treatment, but depth and texture are different axes (Soft Shadow #23 is both); Visuals: the depth moment is the hero's visual anchor and must read at first glance; Techniques: Vanta / GSAP 3D / Bang Motion camera, at their pinned versions, never an unpinned effect; Colors: the scene's colours are the theme's own tokens; Depth: the moment's layer order, elevation, and parallax distances are the depth decision itself.

- **Theme-match precondition:** a depth moment that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the moment.
- **Animated 3D gradients come from ShaderGradient (fix #22 §15, SHADERGRAD_F22).** Where the deal calls for the one effect as an animated gradient ground — full-bleed hero, login, or waitlist backgrounds where CSS gradients feel flat — the approved source is ShaderGradient (`@shadergradient/react@2.4.20`, ESM-only; MIT declared in package.json + README but NO root LICENSE file — see the caveat in `ui-ux-pro-max`, SHADERGRAD_F22; React/Next.js ONLY — non-React builds use Vanta or CSS gradients, the same routing rule as React Bits §11). Install: `npm i @shadergradient/react@2.4.20 @react-three/fiber@9.8.2` (React 19) or `@react-three/fiber@8.18.0` (React 18) `three@0.185.1 three-stdlib@2.36.1 camera-controls@3.1.2` (and `@types/three@0.185.1` for TypeScript). Configure by URL, not by hand: design at shadergradient.co/customize, copy the URL — the URL IS the config — and carry it in the §10 directive as `control='query'` + the full `urlString` + the preset name. The 10 presets are the menu (halo, pensive, mint, interstella, nightyNight, violaOrientalis, universe, sunset, mandarin, cottonCandy), never defaults — the preset is theme-matched. Mesh types: `plane` / `sphere` / `waterPlane` (waterPlane at low `uSpeed` for ambient motion behind glassmorphism cards). Constraints, all binding: theme-matched (the URL's colours are the theme's own palette); a static gradient fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; the gradient is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). Install `@shadergradient/react` (v2), NOT legacy `shadergradient` (v1.3.5): a build installing legacy `shadergradient` v1 FAILS the version check. (D19 — Motion: the gradient's ambient motion is the dealt moment's motion; Theme: theme-matched, colours are the theme's own palette from the URL; Texture: the animated ground is the page's texture layer; Visuals: the gradient is the hero's visual anchor, never behind unreadable text; Techniques: `@shadergradient/react` at the pinned version, URL-as-config, install-on-demand per project; Colors: the gradient colours ARE the theme's palette, carried in the URL, never invented.)
- **3D hero and dealt moments on React come from React Three Fiber (fix #22 §15, R3F_F22).** Where the deal calls for the one effect or a dealt moment as a real 3D scene on a React build — a hero object, a camera-through-world moment — the approved implementation is R3F (`@react-three/fiber@9.8.2` on React 19, `@react-three/fiber@8.18.0` on React 18, MIT; peer deps `three@0.185.1` + `@types/three@0.185.1`; see `motion-foundations`, R3F_F22, for the strict pairing rule — React 18 + R3F v9 FAILS the pairing check). The §13 depth rules (3D transforms, parallax, camera moves) run through R3F on React builds; Vanta stays the vanilla-JS 3D path. The scene is directed per §10 (effect + exact camera, lights, and motion values) and recorded in `docs/design-tokens.md` with its fix #19 D19 reason. Constraints, all binding: theme-matched; a static image/poster fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; the scene is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). (D19 — Motion: the scene's motion is the dealt moment's motion; Theme: theme-matched, the scene is the theme's own depth; Texture: none — the scene adds geometry and light, not a surface treatment; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: R3F at the paired pin, install-on-demand per project; Colors: the scene's colours are the theme's own tokens.)
- **Liquid glass hero and nav moments come from liquid-glass-js (fix #22 §15, LIQGLASS_F22).** Where the deal calls for a glass hero panel, a glass nav bar, or a floating glass card — glass as a dealt moment, never a default wash — the approved implementation is liquid-glass-js (dashersw/liquid-glass-js, repo commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package — copy `container.js`, `button.js`, `glass.css` into the project; vanilla JS, no build step). The glass is directed per §10 (class + exact parameters: `type` `'rounded'` / `'circle'` / `'pill'`, `borderRadius`, `tintOpacity`, `blurRadius` — see `less-flat-ui`, LIQGLASS_F22, for the directed values). Cross-reference, do not duplicate: Group E trend "Liquid Glass" (E15) is the MENU item; this library is the IMPLEMENTATION — the trend entry is never restated here and this rule never restates the trend. Constraints, all binding: theme-matched (the glass must be the theme's own material, never a generic backdrop-blur wash — Refract explicitly bans frosted glass and is NOT a fit); a frosted-blur fallback (less-flat-ui #2 fluted glass) on mobile/low-power and whenever WebGL is unavailable; the glass MUST disable under `prefers-reduced-motion: reduce` (the frosted fallback shows instead); text over glass keeps 4.5:1 contrast; the glass is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). (D19 — Motion: none — the glass does not move (its refraction is light, not motion); Theme: the glass is the theme's own material; Texture: the glass IS the surface's texture layer; Visuals: the glass panel is the hero/nav anchor, never behind unreadable text; Techniques: vendored file copies at the pinned commit, no npm package; Colors: the glass tint is the theme's own tint, never a new colour.)

- **Bespoke particle hero backgrounds come from Casberry (fix #22 §17, CASBERRY_F22).** Where the deal calls for the one effect as a bespoke particle scene — a hero the libraries do not have — the approved production method is Casberry (particles.casberry.in, free, no sign-up): direct the prompt with exact values, export React / Three.js code or a standalone WebGL / HTML file, drop it into the build. STANDALONE TOOL, not a dependency (same form as liquid-logo, §15). The export is the surface's one WebGL-heavy effect; it is reviewed as untrusted code before it enters the build (very low automated trust score on the domain; terms unresolved — see `motion-foundations`). Constraints, all binding: theme-matched (particle colours are the theme's own tokens); a static fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check. (D19 — Motion: the particle motion is the dealt moment's motion; Theme: theme-matched, the scene is the theme's own depth; Texture: the particle field is the page's texture layer; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: standalone tool, exported code reviewed line by line, no runtime dependency; Colors: the particle colours are the theme's own tokens.)
- **Animated flourishes on React come from OriginKit (fix #22 §17, ORIGINKIT_F22).** Where the deal calls for an animated flourish — a background, a cursor treatment, a text effect, a button, a loader — on a React build, the approved browsable catalog is OriginKit (originkit.dev; React, Tailwind CSS, Framer Motion). Fetch by copy-paste from the site (default — the MCP server is NOT wired in the plugin). Cap (binding): 10 component fetches per key per day (resets midnight UTC); a build needing more proceeds from the skills alone and records the gap, never pays for Pro ($79/yr) or Ultimate ($99/yr). Pro-marked components are excluded on the free tier. Licence is conditional / source-available — components are for use in your own project, not for redistribution; the plugin never re-publishes OriginKit components as its own. NOT Origin UI (originui.com, now coss ui / Base UI — solid form / layout primitives): a build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check. Each component is used as a §10 directive (component name + exact props) with its fix #19 D19 reason. (D19 — Motion: the component's animation is the dealt moment's motion; Theme: theme-matched, the flourish is the theme's own motion; Texture: none — a flourish adds motion, not a surface treatment (background flourishes excepted: those ARE the page's texture layer); Visuals: the flourish is the hero's visual anchor, never decoration that obscures content; Techniques: copy-paste fetch at the 10/day cap, env-only key, no MCP wiring; Colors: the component's colours are the theme's own tokens.)
- **Prebuilt components on Tailwind landing builds come from daisyUI (fix #22 §17, DAISYUI_F22).** Where the build is Tailwind and needs prebuilt components — buttons, cards, modals, toggles — the approved library is daisyUI (`daisyui@5.7.50`, MIT; `@plugin "daisyui"` in CSS; daisyUI 5.x + Tailwind CSS v4 ONLY). Components are a MENU of implementations, re-themed through the brand / theme deal: a build shipping daisyUI's default theme unexamined FAILS (generic look — the Home Run lesson). The design package chooses the direction; daisyUI supplies prebuilt components that get re-themed. (D19 — Motion: none — daisyUI adds components, not motion; Theme: the components are re-themed to the brand deal, never shipped in the default theme; Texture: none — daisyUI adds component structure, not a surface treatment; Visuals: the components are consistent across the page, never the default look; Techniques: exact pin + Tailwind v4 pairing, install-on-demand per project; Colors: the theme colours ARE the re-theme.)

- **One object never carries the page.** The product or hero object whole leads the hero and **two more sections at
  most**; another kind of visual the brief supports carries the rest (`sections.md` section 1,
  its table): a game's world and crew; hardware's use at the bench, its parts close up; a still
  diagram card, a type moment, a context photograph where the trade allows.
- **The client's own assets get slots.** A trailer, key art, screenshots, CAD renders or a motion
  video the brief names each get a frame that reads finished now (a real `<video>` with a stand-in
  poster, a play control only when there is a page or file to play, three to five stand-in
  photographs of the world, a CAD frame), named in a comment for the client's file, never empty
  (`sections-library.md`, client-slots).

## 3. What serves which page

Open the reference of every asset family the page uses first. A dash means never.

| Need | Asset | Software, gaming | Hardware | Product, service | Place | Reference |
|---|---|---|---|---|---|---|
| Heights, edges, heroes, type | `system.css`, `assets/layout` | dealt hero | dealt hero | dealt hero | place hero | `layout-v4.md` |
| Sections and recipes | `starter.html` | its plan | product plan | its plan | place plan | `sections.md`, `sections-library.md` |
| Tokens, grid, buttons, nav, footer, colour | `system.css`, `system.js` | yes | yes | yes | place tokens | `system.md` |
| Forms, keyboard, head and share tags | `starter.html`, `system.css`, `system.js` | yes | yes | yes | yes | `system.md` |
| Copy, contacts, credits | `scripts/copy-lint.mjs` | yes | yes | yes | yes | `copy.md`, `copy-voice.md` |
| Hero entrance, hover, press, focus, nav, tabs | `assets/motion` | yes | yes | yes | yes | `motion.md` |
| Card loops, a count | `assets/motion`, `assets/ui` | yes | yes | - | - | `motion.md`, `cards.md` |
| Photographs | `scripts/photos.mjs` | people, customers; a game's art, else stand-ins of its setting | lead | lead | lead, 12-20 | `photos.md` |
| Real tool, app and file icons | `scripts/icons.mjs` | yes | yes | tools really used | - | `icons.md` |
| Feature cards, UI fragments | `assets/ui` | lead (gaming: none) | its app | an app the client runs | - | `cards.md` |
| Diagram cards (hub, lanes, pulses) | `assets/diagrams` | 1-2 by default, pulsing; 0 only with a recorded reason in the section plan | 0-2, pulsing | 0-1, still | - | `diagrams.md` |
| CSS grounds | `assets/backgrounds` | 0-2 dealt | 0-2 dealt | flat tokens | flat tokens | `backgrounds.md` |
| Shader grounds | `assets/effects` | the one effect | the one effect | - | - | `effects-usage.md` |
| Creative parts (`fx-*`) | `assets/components` | yes | yes | `fx-photo` plain, `fx-map` still | `fx-map` still | `effects-creative.md` |
| Objects and prints | `assets/objects` | one, as the effect; a render when the brief asks for 3D | its render when the brief asks for 3D | its render when the brief asks for 3D | - | `effects-objects.md` |
| Award-site moments | `assets/moments` | 1-2 | 1-2 | 1-2 (photo, type) | 1-2 (photo, type) | `moments.md` |
| Big scenes | `assets/scenes` | 0-1 | 0-1 | - | - | `scenes.md` |
| Speed and weight | `scripts/perf.mjs` | yes | yes | yes | yes | `perf.md` |

Read `copy.md`, `copy-voice.md`, `system.md`, `layout-v4.md` and `sections.md` in full before the first page.

## 4. The run

0. **The stack.** An empty folder builds a static page: copy `<skill>/assets` into `assets` and
   start from `assets/starter.html`. An existing project builds in its own stack, its components
   taking the starter's markup and classes, with the kit copied into its public folder
   (`public/assets`) and loaded from there as plain files. A brief that asks for Next.js builds a
   static export (`output: 'export'`), checked on its built page (`--root out`).

1. **Read the brief.** Write down the kind (section 1), what is sold, who buys it, the one main
   action (the transaction: Book a room, Order a cake, Start a free trial; a place with neither:
   Get directions) and the real material: logo, screens, photographs, prices, address, hours.
   Then arm the finish gate, before any page exists:

   ```bash
   node <skill>/scripts/gate.mjs --start index.html --kind <kind> --category "<what is sold>" --primary "<main action>"
   ```

   A framework build names its dev server's URL (`--start http://localhost:5173/`) or its built page
   (`--start dist/index.html --root dist`; a Next.js export: `out`) in place of `index.html`, and
   rebuilds before every gate run.

2. **Write all the copy first,** with the copy layer (`copy-voice.md`: the fact sheet, the voice
   card on the plan, the page's shape, the device budget; a register from `copy-registers.md`, the
   moves of `copy-moves.md`) within the rules of `copy.md`: the h1 names the category and the buyer or the place (a game: its name and genre),
   one hard fact on the first screen, a noun in every heading, buttons as a verb and an object.
   Nothing is invented but a coined brand name (searched first, the result kept in `names.json`
   beside the page) and, on a place, plausible hours and prices, each marked `data-assumed`
   (`copy.md`, What may be assumed). A draft kept in a `.md` file lints the same way as the page
   (the voice card and part labels are skipped).

3. **Plan the page as screens.** Line 1: the kind. Line 2: the deal (step 4), with one sentence on
   why the palette fits the trade. Then one line per
   section: its id, its one idea, its picture and its kind (object, use, parts, world, slot, diagram, type; three object lines at most), its
   screens (1 or 2, from its content height, `layout-v4.md` section 2), which section holds a
   moment and why it moves (on tech also the effect or the scene). Pick the photographs now (`photos.md`); their count,
   stand-ins included, sets a place's length (section 2). Then read `cards.md` and the recipe of
   every id you use in `sections-library.md`.

4. **Deal, never choose by taste.** Read `new-skills/orchestrate/references/design-inventory.md` FIRST — before any deal — so the theme, palette, and pairing are chosen from the inventoried elements (fix #23 §1, THE INVENTORY). Each command keeps a history, so pages differ:
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

   **Palette first — inventory the available components BEFORE the direction is finalized (fix #27, PALETTE-FIRST_F27).** Before any deal in this step — before the Hallmark theme deal and before the palette deal below — the design-lead inventories the available component palette FIRST and bases the design direction on it: read the available component/design sources — `getlayers` FIRST (prompt-first cinematic layers; the first-class foundation the direction leans on — consult its prompts before the other palette sources), then `motionsites-web-builder` (cinematic components, motion patterns, hero treatments, media; free sample only, fetched from upstream at use time; consulted, never a template), the design package (`ui-ux-pro-max`, `less-flat-ui`, `motion-foundations`, `motion-patterns`, `motion-advanced`, `make-interfaces-feel-better`, `design-system`, `gsap`, `react-bits`, `hairline-create`, `hairline-adopt`), and the dealt Hallmark theme (the starting point, not a cage) — and select the components, motion patterns, hero treatments, and media the design will be built from, tailored to this project's needs. Record the palette in the design direction (plan line 2 and `docs/design-tokens.md`, step 4a): which sources, which components, what was tailored and why — a fix #19 D19 reason for each. A design direction that names no palette components is incomplete. Tailoring is expected: the palette is starting material, not a template to copy wholesale. Planning a full design first and then rejecting the available components is the old order and is not done. The audit checks the design-direction record names the palette components used (sources + components + tailoring); a direction with no palette attribution is a finding. GetLayers layers are cited the same way as every inventory entry — USED or CONSIDERED-AND-REJECTED, each with a D19 reason; a direction that names no GetLayers layer at all (neither used nor considered-and-rejected, nor `not considered — <reason>`) is a finding.

   ```bash
   node <skill>/assets/layout/deal.mjs --type <page type> --has <photo,ui,film,object,setting> --history .taste-skill/layout-history.json   # the hero; a game adds --kind gaming, hardware --kind tech
   node <skill>/scripts/start.mjs deal --page <kind> --trade <trade> --history .taste-skill/history.json    # three palettes made for the trade, three pairings: take the first; add --axis after a word or editorial hero
   node <skill>/scripts/start.mjs css --page <kind> --palette <id> --type <id> --radius soft --history .taste-skill/history.json
   node <skill>/scripts/start.mjs brand --page place --bg "#.." --ink "#.." --accent "#.." [--surface "#.."] [--muted "#.."] --type <id> --radius soft   # the client's own colours (a logo, a painted shopfront), in place of css
   node <skill>/scripts/moments.mjs pick --page <kind> --count 1|2 --fits section,statement --photo --history .taste-skill/history.json   # every kind
   node -e "for(const l of process.argv.slice(1)){const o=l.split('|');console.log(o[Math.floor(Math.random()*o.length)])}" <the kind's lists, below>
   ```

   Run every command from the project folder (the deal arms the gate in the folder it runs in, or
   joins the build already open one or two folders up). The
   lists, in order nav, footer, close, rhythm, buttons, mark (`sections.md` sections 2 and 3):
   - software: `"nav-mega|nav-cards|nav-centre" "footer-dark|footer-statement|footer-columns" "close-type|close-word" "dark-band|surface-pairs|space" "solid|pill|tonal|arrow" "wordmark|initial|arc|ring|stack|dots"`
   - gaming: `"nav-mega|nav-centre|nav-cards" "footer-dark|footer-statement" "close-word|close-type" "dark-band|media-band|space" "solid|pill|block" "wordmark|initial|arc|ring|stack|dots"`
   - product and hardware: `"nav-cards|nav-split|nav-mega" "footer-columns|footer-dark" "close-photo|close-type|close-word" "dark-band|brand-band" "arrow|solid|block|pill" "wordmark|initial|arc|ring|stack|dots"`
   - service: `"nav-mega|nav-split|nav-centre" "footer-visit|footer-dark|footer-columns" "close-type|close-photo" "surface-pairs|dark-band|space" "solid|tonal|block|arrow" "wordmark|initial|arc|ring|stack|dots"`
   - place: the whole line in `sections.md` section 4, Place (The deal), read in its order.

   A product or hardware with no photographs deals with `--has photo` for its stand-ins;
   `--has object` only for a cut-out or a render the brief asks for (always the `product` hero, its
   widest view across the wrap, no box); a game without art files passes `--has setting` (the
   `photo` hero, its name over a stand-in of its setting; a game always passes `--has`). A product
   page is dealt only the product, photo and film heroes. A place's hero is printed, never dealt (`--type
   place`). A dealt part that needs a photograph the page lacks is dealt again (`sections.md` section 2). Take the
   first palette and the first pairing printed (the next only when the first clashes with the
   client's own logo or photographs, or the pairing fails `hero-lines`, said on plan line 2); the client's own colours go through
   `start.mjs brand` instead (`sections.md` section 4, Look); never violet: deal again. Keep the `:root` block as printed, except the font delivery: the Google Fonts link the block prints requests static instances only (fix #19 F2) and is the generation source — instance the dealt faces to static files per the step 4a instancing step and ship those files with `@font-face` + preloads, never a CDN link as the delivery. Radius: `sharp` for fintech and developer tools, `soft` by default,
   `round` for consumer apps, square on a place. On tech only: the lit ground (`<html data-ground>`:
   `sand|sky|sage` through the one-liner), the CSS grounds (`backgrounds.md`) and the one effect
   (`effects-usage.md`). Write every result on plan line 2 and in
   the comment at the top of `<body>`, and build exactly that (a short page drops what it has no section for: `sections.md` section 4). Also write the deal's Picks block (Material, Signature, and Hero-moment rows — the Hero-moment row records the dealt hero moment from HERO_F23: the moment, the composition, the motion values) to `.hallmark/picks.md` in the project root — the hero review and finish review take those rows as file paths.

   **Deal a Hallmark theme for the direction first.** Read `new-skills/orchestrate/references/design-inventory.md` FIRST — before deciding — and choose the theme from the inventoried elements (fix #23 §1, THE INVENTORY; record USED vs CONSIDERED-AND-REJECTED per entry). Count convention (fix #24 F-06): wherever a frozen rule text says 'six dimensions', read seven — the six fix #19 dimensions plus Depth (fix #22 §13, DEPTH_F22). Before the palette deal above, run the Hallmark theme deal — it picks the material world the page lives in, so the direction is dealt, not invented. The dealt theme is the starting point, not the cage (fix #27, THEME-START_F27). The design-lead may depart from the theme's material where the brief's job demands it, recording the departure as a D19-reasoned decision (what was departed from, why the job needs it).

   ```bash
   node <skill>/references/hallmark/scripts/theme.mjs deal --genre <genre> --prompt "<the brief>" --log .hallmark/log.json
   ```

   Map the page kind to a Hallmark genre for the deal: tech/dark/atmospheric → `atmospheric`; SaaS/devtool/B2B → `modern-minimal`; playful/fun/kids/games → `playful`; ops/technical-tooling (dashboards, ops consoles, monitoring, admin) → `atmospheric` or `modern-minimal` by the brief's mood; data/video-pipeline (pipelines, processing, video, telemetry) → `atmospheric`; scientific domains (lab, research, clinical, instrumentation) → `modern-minimal` or `atmospheric` by the brief's mood. Nothing defaults to `editorial` (fix #27, THEME-START_F27): where no genre above fits, pass the brief's domain words in the deal prompt and let the deal pick — never fall back to `editorial`. The deal returns 3 themes from the 50-theme catalog (`references/hallmark/references/themes/`, `index.json`); pick the one whose material can carry the brief — read the theme file's header (paper/display/accent/posture), its `material` line, and its feel paragraph. After picking, log the pick so the next deal avoids it: `node <skill>/references/hallmark/scripts/theme.mjs log --entry '{"theme":"<picked theme name>","axes":"<paper>/<display>/<accent> triple from the deal line>","prompt":"<the brief>","shape":"<dealt hero/layout shape>","hero":"<hero posture>","nav":"<nav form>","footer":"<footer form>","imagery":"<imagery plan>","sections":"<section list>","fingerprint":"<shape + axes fingerprint>","signature":"<theme signature>"}' --log .hallmark/log.json` — the deal reads the recent 3 log entries to avoid re-dealing recent themes and axes, and without the log entry that avoidance never works. Log every field `theme.mjs` reads (it warns `missing … which Rotation reads` for a short entry): take shape/hero/nav/footer/imagery/sections/fingerprint/signature from the deal, the theme file, and the plan — and if the build changes the shape, re-log with the settled values, so the repetition check (gates.md:189) reads the real page. The theme pictures (`.jpg`) are NOT staged in this plugin, so pick by the material description, not the picture. Take the theme's palette balance, type voice, surfaces, and Range (the sections it makes without a photograph); the theme never sets what the page contains or in what order. The theme's Tokens block is the page's `:root` tokens — use it in place of `start.mjs css` for the palette (the hero deal, moments, and nav/footer/close lists above still run). If the dealt theme clashes with the client's own logo or photographs, re-deal once (`--reroll 1`); the client's own colours go through `start.mjs brand` instead. If you re-deal, log the re-dealt pick too — the log must record the theme actually built, not the first pick. Do NOT use `theme.mjs draw` or `theme.mjs scaffold` — Taste owns shape and scaffold. The Hallmark Floor binds the page: read `references/hallmark/references/hallmark-floor.md` (16 non-waivable rules + the 6-axis pre-emit critique) and follow it; where it and this skill disagree, the stricter ban wins. The dealt theme is recorded as directives, not prose — see the DIRECTIVES_F22 rule in step 4a: theme slug, Tokens block, and moments are exact values the build executes verbatim.

   **Trend menu (TRENDS_F22, fix #22 Group E) — opt-in options, never defaults.** The design package MAY draw on these twenty trends when the dealt theme matches them. Never apply a trend because it is trending. The anti-derivative rule stands (a trend is not a reference design to copy), "more, not bolder" stands, and the theme-match precondition stands: a trend that clashes with the dealt theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the trend. Every trend a build uses is recorded there with its fix #19 D19 reason (seven dimensions each, below). A trend used with no theme-match reason is an incomplete build — a static check item in step 6, never a screen verdict; browser-qa alone judges whether it reads on the rendered screen. Where a trend overlaps a slop indicator, the trend entry carries the §4a deliberate-use condition (deliberate + theme-matched + recorded): the trend and the slop check are two sides of the same rule. Overlapping pairs: E1 dithering with C14; E2 ASCII over video with C15; E9 Instrument Serif with C3; E12 all-caps eyebrows with C13/C18; E19 squircles with C16; E7 dark gradient heroes with C19. Hallmark cross-references below name the fitting theme file(s); where a theme file carries a `TRENDS_F22` Range line, that line is the cross-reference and points back here for the full D19 reason.

   - **E1 Dithering (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C14 condition (deliberate + theme-matched + recorded). The technique already exists as less-flat-ui #11 Dithered images and in the Taste `ascii-shade` effect family. Flagged as slop when dithering IS the whole visual identity or a default wash with no theme reason. Hallmark fit: Halftone (the dot screen is its print voice), Riso (grain where the ink skips).
     - Motion: none — dithering is a static print treatment; it carries no entrance, hover, or loop.
     - Theme: fits only where the dealt theme's material is print (Halftone dot screen, Riso ink grain); elsewhere it reads as a default wash.
     - Texture: this IS the texture layer; use the less-flat-ui #11 path (build-time Bayer step, ship the file), never a live wash over a whole page.
     - Visuals: a dithered image or field reads printed and grainy; keep text readable over it and never dither the type itself.
     - Techniques: pairs with halftone and dot-screen print treatments; do not stack with a second busy pattern (less-flat-ui layering rule).
     - Colors: one ink plus the paper ground; the dither stays inside the theme's palette balance, never a new hue.
   - **E2 ASCII over video (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C15 condition (deliberate + theme-matched + recorded). The technique already exists as the Taste `ascii-shade` effect and less-flat-ui #22 ASCII and pixels. The video underneath stays the subject (the client's own footage or product motion); never ASCII as a default background, and never ASCII behind code or running text. Hallmark fit: Cobalt (a generated ASCII field is its ground), Terminal (pictures printed in the page's own glyphs).
     - Motion: the video moves; the ASCII layer follows it (the `ascii-shade` slow form); no extra loop added on top.
     - Theme: fits only where the dealt theme's material is character-based (Cobalt ASCII field, Terminal glyph pictures); on any other theme it is a costume.
     - Texture: the ASCII rendering is the texture; it replaces, never stacks with, another busy pattern.
     - Visuals: the picture must still read at a glance; glyph density stays low enough that the subject survives.
     - Techniques: the `ascii-shade` effect as specified in `effects-usage.md`; never ASCII behind code or running text (less-flat-ui do-not).
     - Colors: glyphs in the theme's ink and one signal only; never a rainbow glyph field.
   - **E3 Infinite canvases (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A boundless pannable and zoomable canvas surface for tools, boards, and maps. Hallmark fit: Blueprint (a drafting sheet that extends past the frame).
     - Motion: pan and zoom are the motion, eased and interruptible; the canvas never auto-scrolls or animates on its own.
     - Theme: fits only a sheet-based theme (Blueprint); on a page theme it is a foreign object.
     - Texture: none — the canvas ground is the theme's own sheet (blueprint lines, dimension strings); no extra texture layer on top.
     - Visuals: the content on the canvas carries the page; the canvas itself stays quiet so the work reads.
     - Techniques: pairs with a diagram or map treatment from the theme's Range; minimap or zoom controls only where the theme's controls allow.
     - Colors: the theme's paper and ink only; canvas chrome takes no new accent.
   - **E4 Disco logos (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A wordmark or logo treatment with mirror-ball light play: RGB-split lettering, hard light, loud colour fields. Hallmark fit: Arcade (Bungee capitals split in RGB, CRT light), Carnival (two accents competing as whole fields).
     - Motion: none — the logo is static; any shimmer is a hover-only micro-interaction, never an ambient loop.
     - Theme: fits only loud playful themes whose material is light and colour (Arcade, Carnival); on a restrained theme it shouts.
     - Texture: none — the colour fields are flat fills; no grain or gloss layered on.
     - Visuals: the wordmark stays legible at every size; the split or field never breaks the letterforms.
     - Techniques: pairs with the theme's display face at poster size; the logo treatment never becomes a second brand.
     - Colors: the theme's own loud inks only (Arcade ember and acid, Carnival two fields); no new hue introduced for the effect.
   - **E5 Renaissance branding (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. Classical old-master art direction: parchment, gilt, deep pigment, old-master portraiture as material. Hallmark fit: Vellum (parchment, heritage, manuscript), Atelier (gallery, maker's catalogue).
     - Motion: none — stillness is the register; entrances stay the page system's own.
     - Theme: fits only heritage and editorial themes whose material is old paper and pigment (Vellum, Atelier); on a tech theme it is a costume.
     - Texture: the theme's own paper (parchment, limewash) carries the texture; no added distress or ageing filter.
     - Visuals: real photographs or the product, printed in the theme's ink; never a generated old-master pastiche.
     - Techniques: pairs with the theme's display face (Vellum blackletter, Atelier roman serif) and hairline rules.
     - Colors: the theme's parchment, umber ink, and one pigment only; gilt reads as the accent, never as a second gold.
   - **E6 Monet backgrounds (TRENDS_F22).** Pointer only, do not duplicate: the treatment is less-flat-ui #21 Impressionist paintings. Opt-in only, theme-matched. The background must read as impressionist light (broken colour, daylight), never as a blurred photograph or a gradient wash. No Hallmark cross-reference: no theme's material is impressionist painting, and forcing one would invent a fit.
     - Motion: none — the painting is still; light moves only where the theme's own motion allows.
     - Theme: fits where the dealt theme's material is daylight and pigment; the choice is recorded with the theme-fit reason.
     - Texture: this IS the texture layer, via less-flat-ui #21; no second texture stacked on it.
     - Visuals: the painting sits behind content that stays readable; contrast 4.5:1 holds over it.
     - Techniques: pairs with the theme's display face and palette; the painting never carries the page's information.
     - Colors: the painting's own broken colour inside the theme's palette balance; no new accent pulled from it.
   - **E7 Dark gradient heroes (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C19 condition (deliberate + theme-matched + recorded). Hallmark fit: Dusk (a real landscape at the turn of the light behind the hero). The gradient must be the theme's own light falloff (Dusk photographed dusk light), never a synthetic wash; gates.md 2a bans purple-to-blue, purple-to-pink, and cyan-on-dark gradients anywhere, so a default purple gradient wash FAILS the polish check. Midnight's ground is solid blue and is not a fit.
     - Motion: none — the hero's light is still; the hero entrance is the page system's own.
     - Theme: fits only where the dealt theme's material is dusk light (Dusk); on any other theme a dark gradient hero is a default wash.
     - Texture: none — the gradient is the ground; no grain or texture layered over it except the theme's own.
     - Visuals: the head sits on the gradient's palest part and stays readable; the product beside it, never glowing.
     - Techniques: pairs with the theme's hero posture (Dusk Stage hero); the gradient never becomes a second effect.
     - Colors: one hue's falloff from the theme's own palette; no violet, no second hue introduced.
   - **E8 Pixel loaders (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A loading state rendered in pixel blocks. Hallmark fit: Arcade (Silkscreen pixel figures, CRT). Every interactive surface already needs a loading state (step 4a); the pixel treatment is only the style of that state, and the loader never gates reading: it shows only while a real async action runs.
     - Motion: the pixel animation is the loading feedback; it stops the moment the content arrives and never loops past the wait.
     - Theme: fits only where the dealt theme's display class is pixel (Arcade); on any other theme a pixel loader is a costume.
     - Texture: none — the pixel blocks are the treatment; no extra texture on the loading surface.
     - Visuals: the loader is small and clearly a state, never a full-screen gate; the loaded content is the picture.
     - Techniques: pairs with the theme's pixel face (Silkscreen figures); the loader never becomes the page's moment.
     - Colors: the theme's ink and one signal only; no new colour for the loader.
   - **E9 Instrument Serif (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C3 condition (deliberate + theme-matched + recorded). The face already exists in the plugin as a dealt display face (Lumen) and a layout-v4 static-face example. Defaulting to Instrument Serif because it is the familiar choice IS the tell; it is allowed only as the dealt display face on a theme whose material names it. The font rules still bind (fix #19 F3 unique pairing, fix #20 F5 important text, fix #21 F7 artistic decision, static instances only). Hallmark fit: Lumen (display IS Instrument Serif, lowercase, a step large).
     - Motion: none — the face carries no motion; its underline draw (the Lumen verb) is the theme's own.
     - Theme: fits only Lumen, whose material is lowercase Instrument Serif heads; on any other theme it must be dealt, not assumed.
     - Texture: none — the face is type, not texture; no texture applied to make it read.
     - Visuals: set lowercase and a step large per Lumen; narrow and light, so it never sets at plain section size.
     - Techniques: pairs with the theme's Type rules (Lumen lowercase register, Geist body, mono readouts).
     - Colors: the theme's ink; the one accented word rule (the Lumen verb) still binds, never a second accented word.
   - **E10 One italic word (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C2/D3 one rule: a single deliberate italic accent is fine; random or excessive italics are slop. Exactly one italic word per page, the outlier. Hallmark Reflex 38 (italic display as a flourish) is waived only where the theme declares it as material. Hallmark fit: Spore (a second name after a product's, a grape, a vintage, a Latin name, is Instrument Sans italic, the outlier and the only italic). Never an italic head, never italic as a default emphasis.
     - Motion: none — the italic word carries no motion; it is a type accent only.
     - Theme: fits only where the dealt theme's material names one italic outlier (Spore); elsewhere italic stays in-paragraph emphasis only.
     - Texture: none — the accent is typographic, not textural.
     - Visuals: one word, set apart by slant alone; the rest of the line stays roman so the outlier reads.
     - Techniques: pairs with the theme's Type rules (Spore Young Serif heads, Instrument Sans italic second name).
     - Colors: the theme's ink; the italic word takes no colour accent of its own.
   - **E11 Cream backgrounds (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart as a trend, but the Hallmark gate 65 guard applies: cream paper with a high-contrast serif and a terracotta accent is the most recognised generated look and is refused on custom or unthemed builds. A cream ground is allowed only as a catalog theme's own paper, dealt on its keywords. Hallmark fit: Hum (grained cream paper pulled toward pear-yellow), Halftone (butter-cream stock).
     - Motion: none — the paper is still; the page's motion is the system's own.
     - Theme: fits only where the dealt theme's paper is cream (Hum, Halftone); on any other theme a cream ground is an unthemed default.
     - Texture: the paper's own grain (Hum fibre, Halftone print) is the texture; no extra texture layer.
     - Visuals: never pure-white panels on a cream page (`backgrounds.md`); photographs print in the theme's treatment.
     - Techniques: pairs with the theme's display face and rules; the cream never carries a second paper colour.
     - Colors: the theme's paper and ink; the accent stays the theme's own single signal, never terracotta added to cream by hand.
   - **E12 All-caps eyebrows (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C13/C18 condition (deliberate + theme-matched + recorded). Allowed only as a deliberate key label in a theme whose display voice is built on capitals (Manifesto Anton capitals, Broadside Six Caps wood capitals; gates.md 67: capitals survive as the display voice of a theme built on them); never the default label style. The skill's own rule is sentence case everywhere, labels 13px at 500, never tracked capitals (`system.md`). No theme file carries an eyebrow line: the theme contract forbids eyebrows in any form and the theme validator rejects the word, so the fit is recorded here in the menu only. Never tracked: letter-spacing stays the theme's own, never spread apart.
     - Motion: none — the label is static type; it carries no entrance or loop.
     - Theme: fits only caps-led themes (Manifesto, Broadside); on any other theme an all-caps eyebrow is the default tell.
     - Texture: none — the label is type, not texture.
     - Visuals: one key label, small and plain; the heading beneath it names the thing.
     - Techniques: pairs with the theme's caps display voice; the label never takes a second style (no rule, no pill, no tracking).
     - Colors: the theme's ink or muted; the label takes no accent fill.
   - **E13 Pulsing live dots (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A small dot that pulses to say something is live. Hallmark fit: Wayfind (one cobalt live dot on the row that just changed; a live dot blinks once when a row updates, never loops). The dot marks a real live state; it pulses on change and then rests, never loops forever. The existing timing is `motion.md`'s live dot at 2.4s inside the looping visual.
     - Motion: the pulse is the motion: one blink on change, then still; a looping pulse is a finding, not a feature.
     - Theme: fits only where the dealt theme's material names a live dot (Wayfind cobalt live); on any other theme the dot must be earned by a live state, not decoration.
     - Texture: none — the dot is a signal, not a texture.
     - Visuals: one dot, small, on the thing that changed; never a dot on every row or card.
     - Techniques: pairs with the theme's status treatment (Wayfind rows, cobalt for what is live).
     - Colors: the theme's live signal only (Wayfind cobalt); the dot never takes the accent.
   - **E14 Sparkle icons (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A small sparkle or star mark on an icon to say something is new, magic, or enhanced. The sparkle marks one real thing; never a sparkle on every icon, never a sparkle as decoration on a plain icon. No Hallmark cross-reference: no theme's material names a sparkle motif, and forcing one would invent a fit.
     - Motion: none — the sparkle is static; if it twinkles, it does so once on appearance, never as an ambient loop.
     - Theme: fits only where the dealt theme's voice allows a small bright signal; the choice is recorded with the theme-fit reason.
     - Texture: none — the sparkle is an icon mark, not a texture.
     - Visuals: one small mark beside the icon it qualifies; the icon itself stays the theme's real icon.
     - Techniques: pairs with the theme's icon treatment (real icons, `icons.md`); the sparkle never replaces the icon.
     - Colors: the theme's one signal colour; the sparkle never introduces a new hue.
   - **E15 Liquid Glass (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A translucent glass surface with refraction-like light. Hallmark fit: Dusk (the product in smoked glass with a lit top edge; frosted fog over a photograph), Dose (translucent tinted plastic). The glass must be the theme's own material (Dusk smoked glass, Dose tinted plastic), never a generic backdrop-blur wash; Refract explicitly bans frosted glass and is NOT a fit. Text over glass keeps 4.5:1 contrast.
     - Motion: none — the glass is still; light moves only where the theme's own motion allows.
     - Theme: fits only glass-material themes (Dusk, Dose); on any other theme Liquid Glass is a borrowed effect.
     - Texture: the glass itself is the surface; no extra texture or blur layered on it.
     - Visuals: the glass holds the product or a photograph; content beneath it stays legible, never smeared.
     - Techniques: pairs with the theme's surface rules (Dusk glass pane beside a list, Dose tinted bands); the glass never becomes a second effect.
     - Colors: the theme's glass tint only (Dusk smoked, Dose tinted plastic); no rainbow refraction, no new hue.
   - **E16 Three icon cards (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A section of three cards, each led by an icon. The plugin's variety rules (fix #15 canonical variety) push against default three-card layouts: allowed when theme-matched, never the default section shape. The three cards must differ in composition (never the skeleton: eyebrow, claim heading, two-line lede, three cards, figures, in every section); a card layout repeats at most twice a page (`sections.md`). No Hallmark cross-reference: no theme prescribes three icon cards.
     - Motion: the cards take the hover layer only; no scroll entrance, no stagger as a default.
     - Theme: fits only where the dealt theme's Range makes card-led sections; the choice is recorded with the theme-fit reason.
     - Texture: none by default; a card takes a texture only where the page system leaves it unstyled.
     - Visuals: three real icons (the tools really used), each card with its own picture or fact; never three look-alike cards.
     - Techniques: pairs with the theme's card treatment and the `sections-library.md` recipe for the card used; the section never repeats the skeleton.
     - Colors: the theme's tokens; the three cards share one card style, one radius scale, one accent.
   - **E17 Decorative flowcharts (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C5/C9 condition: a diagram must earn its detail (fix #15 R2: one diagram by default on software pages); decorative flowcharts are fine when theme-matched and simple, and an overly detailed diagram that adds nothing is slop. Hallmark fit: Blueprint (dimension strings, keylines, the white line as the only signal). The flowchart is simple, drawn in the theme's own lines; a flowchart that carries real steps is a diagram, not a decoration, and follows `diagrams.md`.
     - Motion: none — the flowchart is still; pulses run only on a real diagram (`diagrams.md` pulsing lanes).
     - Theme: fits only where the dealt theme's material is lines and dimensions (Blueprint); on any other theme a flowchart is a foreign object.
     - Texture: none — the lines are the treatment; no texture under them.
     - Visuals: few nodes, few connectors, all legible; the chart never crowds the section.
     - Techniques: pairs with the theme's Range (Blueprint keylines, dimension strings); the chart never becomes a second diagram.
     - Colors: the theme's ink and one signal; the connectors take no new hue.
   - **E18 Endless marquees (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. A row of words that scrolls without end. Hallmark fit: Arcade, Editorial (both picture a Marquee Hero). Words only, never logos (`moments.md`: a logo never moves; `motion.md` bans a logo marquee); a pause button always (`moments.md` marquee-row); the marquee merges into the section above as its last row; endless means the row loops seamlessly, never a second marquee on the page.
     - Motion: the scroll is the motion, slow and steady with a pause button; under reduced motion it rests as a wrapped row.
     - Theme: fits only where the dealt theme pictures a marquee (Arcade, Editorial); on any other theme it is a borrowed loop.
     - Texture: none — the words are the treatment; no texture behind the row.
     - Visuals: real words (trades, cities, formats), set in the theme's display face; the row never carries a fact the page needs elsewhere.
     - Techniques: pairs with the `moments.md` marquee-row treatment; the marquee never becomes the page's moment.
     - Colors: the theme's ink on its paper; the row takes no accent fill.
   - **E19 Squircles (TRENDS_F22).** Opt-in only, theme-matched, with the §4a C16 condition: a shape, fine when theme-matched; slop when it is the default container shape with no reason. Hallmark fit: Squeeze (soft rounded tiles a step lighter or deeper), Bloom (part tones on rounded clips). One radius per component type (`polish-pass` polish-details: inner radius equals outer minus padding).
     - Motion: none — the shape is static; it carries no entrance or hover of its own.
     - Theme: fits only where the dealt theme's material is soft rounded tiles or clips (Squeeze, Bloom); on a square-cut theme it clashes.
     - Texture: none — the shape is geometry, not texture; the surface inside takes the theme's own treatment only.
     - Visuals: the squircle reads as the theme's tile or clip, with content that fills it (fix #17 T1).
     - Techniques: pairs with the theme's radius scale (one radius per component type); corner smoothing only where the design system uses it.
     - Colors: the theme's paper steps; the squircle takes no new fill.
   - **E20 Pretext text wrapping (TRENDS_F22).** Opt-in only, theme-matched. No slop counterpart. Body text wrapped around a figure, pull-quote, or shaped element (text that runs around a pre-set shape). Hallmark fit: Newsprint (justified columns under hairline rules, broadsheet text craft). The wrap serves reading (editorial), never a decorative wrap that breaks measure; the fix #15 C3 body-measure rule (65–75ch) still governs the wrapped lines; the figure the text wraps is real (a photograph or the product), never a drawn shape.
     - Motion: none — the wrap is static type; it carries no entrance or loop.
     - Theme: fits only where the dealt theme's material is editorial text craft (Newsprint); on any other theme the wrap is a borrowed layout.
     - Texture: none — the wrap is type, not texture.
     - Visuals: the wrapped lines stay even and readable; no ragged gap opens beside the figure.
     - Techniques: pairs with the theme's Type rules (Newsprint Spectral body, column rules); the wrap never becomes a second column system.
     - Colors: the theme's ink; the wrapped figure takes no new treatment.

   **Every dealt moment is applied or re-dealt (fix #15 R1 — baseline: iris-opens was dealt and never applied).** The build record in `docs/design-tokens.md` must list one application per dealt moment, or a re-deal log entry with reason. A dealt moment with neither is an incomplete build — a static check item in step 6 below, never a screen verdict.

**Design bar — beat Campus Eats v5 (fix #25 §4(d), BENCHMARK_V5_F25).** The design-lead reads `skills/orchestrate/references/design-benchmark-v5.md` alongside the inventory BEFORE dealing/deciding: the re-traced design must beat v5 on all seven dimensions (count ≥ 62 literal / ≥ 61 stricter; variety ≥ 7 kinds with ≥ 2 kinds above v5; hero inventory + loop or second moment; Motion ≥ 18 / ≥ 17 stricter; ≥ 9 interactive items with ≥ 2 cross-surface drives; ≥ 3 live-data surfaces; 0 alignment problems) — a tie on any dimension is below the bar on that dimension. The static table is checked at orchestrate step 5a; the live dimensions (hero strength, live dynamic behaviour, live functionality, alignment) are `browser-qa`'s verdict alone.

4a. **Define the design system before building any UI.** Before step 5, freeze the system on the plan (one line each) — this is a pre-UI step, not a gate: **visual identity** (the one idea the page looks like, in words); **typography + type scale** (the dealt pairing and tokens, `system.md` Type); The dealt pairing is the ONLY permitted faces on the build — no other face is introduced — and the pairing + its source are recorded in `docs/design-tokens.md` (fix #15 C1). Display faces are self-hosted as STATIC instances (one bundled woff2 file per weight + `@font-face` in the built page) whenever the face's character matters — a variable font file is never the shipped format, and the closest installed font is a failure, not a fallback; body faces are likewise static instances, and name their source (self-hosted static files + preloads) in `docs/design-tokens.md` (fix #19 F2, extending fix #15 C2). No `system-ui` or bare generic fallback anywhere as a live path; `font-synthesis: none` and `text-size-adjust: 100%`. This is a required build step, not a recommendation; checkable: the built page contains `@font-face` for the display face, and the tokens file names the source. **colour palette + semantic tokens** (ink, `--action`, `--g-main`/`--g-alt`/`--g-dark`, `--muted` — what each token MEANS, e.g. action, success, error, disabled — `system.md` Colour; no raw hex in components — gates.md 48/24a governs on landing); **spacing/layout system** (rhythm tokens + the 12-column grid, `system.md` Rhythm tokens); **component hierarchy** (which components exist, which are primary vs. secondary, one button pair / one card style / one radius scale — `system.md` Radius and buttons, Cards; gates.md F4/F15 governs on landing); **navigation / IA** (nav structure and section order — `system.md` Nav, `sections.md`); **responsive behaviour** (how each section stacks at 1024 / 768 / 390 / 320); **motion / micro-interactions** (hero entrance, hover/press, the dealt moments — house rule 5, `motion.md`; for motion beyond the page system's own entrance and moments — for example interactive app-frame widgets in React/Next.js — decide feel and timing with `make-interfaces-feel-better` first, then implement with the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`)); **accessibility** (contrast 4.5:1, focus rings, keyboard order, reduced motion — `system.md` Access, checklist); **loading / empty / success / error states** for every interactive surface (what each state shows, in the page's own voice — a loading state never an empty ground, an empty state that says what to do next, an error under its own field, a success confirmed only after a real send). Then write the frozen system to `docs/design-tokens.md` in the project root (one line each, same items) — first two lines are the dealt Hallmark theme: its slug, its Tokens block values, and its palette balance, so a later slice briefing from this file alone can recover which theme (and its Range/material) the landing used — and this file is the durable single source of truth: later UI slices' briefs restate tokens from it, and the dashboard MASTER.md (`ui-ux-pro-max`) must conform to it; on divergence this file wins. **Directives, not descriptions (fix #22 §10, DIRECTIVES_F22):** the frozen system above is recorded as DIRECTIVES, not prose — `docs/design-tokens.md` lists the directives per surface (surface → directive + D19 reason): exact tokens, exact measurements, exact type decisions (face, size, weight, line-height, tracking), exact copy, exact motion values (duration, easing, distance), exact layout instructions (structure, spacing, order), each naming the skill it routes through. A description without exact values is incomplete and FAILS the handoff check; a directive without its D19 reason is incomplete; a reason without its directive is not a design decision. The dealt Hallmark theme is recorded the same way — as tokens + moments (exact values), not prose: the theme deal's output (theme slug, Tokens block, palette balance, dealt hero/layout shape, moments) is a set of directives the build executes verbatim. Implementers do not re-interpret directives — an ambiguous, unbuildable, or conflicting directive is surfaced as a recorded gap instead of improvised around. Theme-match precondition: every directive must match the dealt theme. (D19 — Motion: directives carry exact motion values; Theme: directives are the dealt theme expressed as values; Texture: directives name the exact treatments; Visuals: directives fix the exact visual outcome; Techniques: directives name the skill they route through; Colors: directives carry exact colour tokens.) If the project has no landing page, this step does not run and the first UI slice (`ui-ux-pro-max`) writes the file instead — see orchestrate's no-landing fallback. **Anti-generic principles:** never a generic AI-dashboard look — no excessive gradients, no grid of repetitive look-alike cards, no decorative clutter that carries no information; every choice is deliberate typography, spacing, alignment, and contrast, and a surface that adds nothing is cut. Anything already fixed by the deal above is named, not re-decided; only the missing pieces (notably the states and the semantic token meanings) are defined here.

**Functionality story — show how it works (fix #23 §5, FUNC_F23).** The design must surface the technical depth: show HOW the thing works. A mechanism diagram, live figures, the pipeline, data flowing, the stack, the live system state — as a first-class surface, theme-matched, not an afterthought. R2 (one diagram by default on software pages) is strengthened into a functionality requirement: every build shows its mechanism (diagram / live data / system state) somewhere the user sees it early — on the hero surface or the first screen after it, never buried below the fold. The stack is named where the mechanism is shown. The decision record states the functionality story: what is technically new here, and how the design shows it. A build that looks good but hides what the thing does fails. This is never a generic "add a diagram" rule: the mechanism shown must be THIS build's mechanism — its pipeline, its data, its stack — with the product's own names and real figures (`diagrams.md`, FUNC-DIAG_F23); a preset layout relabelled with generic words does not satisfy it.

- **D19 (for the functionality story)** — Motion: the mechanism moves where it is live (pulsing lanes, live figures updating) or records `none — <reason>` where it is a still diagram; Theme: the mechanism is drawn in the theme's own lines, tokens, and material; Texture: the mechanism surface carries the theme's treatment where the theme gives it one, or `none — <reason>`; Visuals: the mechanism is the section's picture — the real pipeline, not a decorative flowchart; Techniques: the mechanism routes through `diagrams.md` (or the live-data surface that shows it) with the product's own labels; Colors: the mechanism uses the theme's ink and one signal; Depth: the mechanism names its layer order (pipeline stages front to back) or `flat by choice — <reason>`. Also read the Impeccable craft floor (`skills/polish-pass/reference/impeccable-craft-floor.md` in the plugin) before building any UI: its bans are absolute as static/code-level checks — a pinned brief never overrides a ban — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone) — and where it and this skill disagree, the stricter ban wins — except that on a landing page Hallmark gate 2b's guarded single-hue gradient-text ramp is permitted (gates.md §4 governs there; the polish detector's gradient-text tell does not apply to it), and except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite on this check alone. **Single source of truth on divergence:** this frozen landing system (recorded in `docs/design-tokens.md`) is the single source of truth for the whole product's design tokens. When the dashboard/app slice later records its system in `design-system/<project-slug>/MASTER.md` (ui-ux-pro-max), that MASTER.md must conform to this frozen system — same tokens, same type scale, same component decisions. If the two diverge, this frozen landing system wins; do not re-derive a competing system. **Each Range pattern's named lead element is its own element (fix #15 R5 — baseline: the Bento lead tile's lone figure was folded into the tile, not counted).** When a theme Range pattern names a lead/hero element (e.g. Sticker's Bento "the lead tile carries the lone figure"), that element is recorded as its own type moment in `docs/design-tokens.md`, distinct from the surface carrying it.

**Unique page-only elements — at least three per build (fix #17 U1).** Every build invents at least THREE unique, one-of-a-kind elements and records them in the 'Unique elements' list in `docs/design-tokens.md`. 'Unique' means ALL FOUR: (1) page-only — the element occurs on exactly one page of this build and is not repeated on any other page or surface of the same build (a repeated instance is one element used twice, not two unique elements — and a repeated element is a pattern, not unique); (2) not a reusable pattern — it is not built from a sections-library recipe, a ui-ux-pro-max pattern, a dealt moment, a Range pattern element, a less-flat-ui treatment, a hero spec, or any other catalogue item in any skill; (3) not in any skill's catalogue — no skill file names it, depicts it, or prescribes it as an option; (4) invented for that page through the skills — generated from the dealt theme's material world (its material, tokens, palette balance, and do-nots) to serve one section's job. Each list entry names the element, its surface, its kind (BASELINE.md counting rule), the section job it serves, the theme material it draws on, and why it is not a catalogue item. At least one of the three must sit on the primary page. A build whose Unique list has fewer than three complete entries is incomplete — a static check item in step 6, never a screen verdict. Each unique element counts once under the BASELINE.md counting rule, as its kind.

**Type fills its bubble (fix #17 T1).** For every display, figure, or label type set inside a bounded container — a tile, card, bubble, chip, tag, badge, stat fill, or price-ladder cell — the size is chosen so the type fills its container: the rendered glyph bounding box must span at least 60% of the container's inner width where the layout fills horizontally, or at least 60% of its inner height where it fills vertically, measured in-page (glyph box vs container box) and recorded per surface in `docs/design-tokens.md`'s Type list as surface → face/size → container inner size → fill ratio. Bounded by no-overflow (no text clipped or spilling its container at 1440 or 390) and no-crowding (type never touches the container edge — the inset is at least the theme's own padding/rhythm token — and adjacent type runs never collide; the existing check.mjs collision/overflow findings govern). The step-6 screenshot check includes a dead-space item: a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding, fed to the fix batch like other checks. Flowing body copy is not a bubble — the C3 body-measure rule (65–75ch) governs there, not this rule.

**Every font decision cites the type system (fix #17 F1 — extends fix #15 C1–C3, does not replace them).** Every face, weight, size, and tracking value on the page is an explicit value from the skills' type system — the dealt pairing (Taste step 4a / ui-ux-pro-max type scale), the theme file's type voice, or the `system.md` Type scale step. No face, weight, size, or tracking on the page is a browser or framework default, and no value is chosen flat (unstated, inherited, 'whatever it came with'). The Type list in `docs/design-tokens.md` gains two columns — weight and tracking — and every row gains a Source cell naming the exact skill text the choice comes from (pairing line, theme-file line, or scale step). A row with an empty Source cell, a Source of 'default', or a value that traces to no recorded pairing/scale/theme line is an incomplete build — a static check item in step 6, never a screen verdict. The polish-pass harmony check verifies the Type list including the Source cells (consistency only — a surface whose type does not trace to the recorded pairing/scale is a harmony divergence, recorded as candidate evidence, never a verdict). App surfaces record theirs the same way in `design-system/<project-slug>/MASTER.md`, conforming to the tokens file.

**Push boundaries — be trailblazing, not dumb (fix #17 E1).** The design-lead MUST push boundaries and aim to be trailblazing: invent original, first-of-its-kind elements for the page — the unique elements of U1 are the normal case, and a build with no element a template would not produce has not pushed far enough. 'Trailblazing' means original, first-of-its-kind decisions, not safe or derivative ones. 'Not in a dumb way' means EVERY boundary push must still: (1) serve the section's job, named in the Unique-list entry; (2) fit the theme's material world — material, tokens, palette balance, do-nots — **or a recorded departure from it** (D19 reason required) (fix #27, THEME-START_F27); (3) obey the type/space rules — the C3 Type list, the T1 fill rule, measure and contrast checks; (4) be theme-matched (fix #15 rule A); (5) pass the craft floor; (6) pass the Hallmark floor; (7) use no violet; (8) be anti-derivative — never based on a searched reference, and the entry names the theme material it draws on, never a URL; (9) stand or fall on browser-qa's verdict on the rendered screen, which is the final word on whether the invented element reads as distinct rather than generic or template. NOT within reason: a new palette (the Tokens block is the page's `:root` — re-deal once if it clashes); a template pattern (a sections-library recipe reused as-is is a catalogue item, not an invention — it fails U1's not-a-catalogue test); breaking a floor or a ban (craft-floor bans are absolute; the Hallmark floor binds). Inventing a theme direction is a recorded D19 decision, not a forbidden move (fix #27, THEME-START_F27): a departure from the dealt theme is recorded with what was departed from and why the job needs it — a re-deal is the easy path, a recorded departure is the permitted one. Each invented element's Unique-list entry carries the nine-point bound checklist, one line per bound; a missing or failed bound is a static-check finding, and a floor/ban break blocks. Distinctiveness itself is browser-qa's verdict alone.

**Fonts render identically on iPhone and web — static bundled files only (fix #19 F2 — extends fix #15 C2).** The shipped font files are STATIC instances — one file per weight (e.g. 400/500/600/700/800), generated from a variable font with fontTools instancer/subsetter where the source is variable, with the optical size baked in (opsz) and no fvar table. A variable font file is NEVER the shipped delivery format: its interpolated weights render differently under iOS vs Windows, which is exactly the bug this rule fixes — a variable font may be the generation source, never a shipped file. NO system-ui / system fallback anywhere as a live path: no `system-ui` in any font stack, no bare generic `sans-serif`/`serif` as a live path — the stack names bundled faces only, and a bundled face that fails to load is a visible failure (a finding), never silently papered over by a system font. `font-synthesis: none` (no browser-synthesised bold/italic — the synthesised weights are the ones that diverge) and `text-size-adjust: 100%` (no platform text scaling). Preload the first-paint faces. The D1 screenshot QA (desktop + mobile) confirms the SAME faces render on both widths — compare the rendered faces, not just layout; a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding, the way the v1 audit caught Bowlby falling back to a plain sans. Where the stack's default font loading serves a variable font (e.g. next/font), the build instances it to static files before shipping. Recorded in `docs/design-tokens.md`'s Type list: each face → its static files (weight → file), source, and preloads. A Type-list row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build — a static check item in step 6, never a screen verdict.

**Instance the dealt faces to static files before shipping (fix #19 F2 — the instancing step).** The Google Fonts link `start.mjs` prints requests static instances only (explicit weights, no variable `..` ranges) and is the generation source, never the shipped delivery. Before shipping, instance each dealt face: (1) download the face's OFL variable font (or its static release where one ships); (2) instance it per weight with the fontTools instancer (`fonttools varLib.instancer`, one instance per weight the build uses, e.g. 400/500/600/700/800), with the optical size baked in (opsz) and the other axes (wdth/SOFT/WONK) fixed at their dealt values; (3) subset each instance with the fontTools subsetter (latin + latin-ext); (4) verify each file is static — no fvar table — and its usWeightClass matches the intended weight; (5) bundle the static woff2 files, add one `@font-face` per weight, and preload the first-paint faces. A Type-list row naming a variable file, a system fallback, a bare generic fallback, or no preload is an incomplete build — a static check item in step 6, never a screen verdict.

**Font choice is unique and interesting — forced, never a default (fix #19 F3 — extends fix #15 C1, fix #17 F1).** No generic/system font as a display or body face. The pairing must be distinctive: a one-off display face with character plus a characterful body face — the pairing itself is a design decision, made THROUGH the design skills (the dealt pairing in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with a Source cell naming the exact skill text (fix #17 F1), never inherited from a framework default, a browser default, or a template. A pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build — a static check item in step 6, never a screen verdict. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2); the body face likewise.

**Plain/body text uses Tiempos (fix #19 F4).** Body and plain text use Tiempos (Klim, paid, NOT bundleable). The canonical free stand-in is Fraunces, set at a 1.55 reading line-height. Wherever the stand-in is used, record it explicitly as the stand-in in the Type list (face → 'Fraunces (stand-in for Tiempos)') — never present Fraunces as Tiempos. Tiempos itself is never shipped from this plugin (no paid licence); if the project holds a Tiempos licence, the licensed files replace the stand-in and the record says so. A dealt theme that names a different body face keeps it ONLY as a scoped, recorded exception in `docs/design-tokens.md` with a fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback). A theme body face delivered as a variable file or with a system fallback is a bug to fix, not an exception to record.

**Every UI decision carries a thought-out reason across the FULL experience (fix #19 D19).** No silent defaults, no arbitrary picks. Each UI decision run through the skills — font, color, layout, element, treatment, motion, component, spacing — carries an explicit recorded reason in the decision record (`docs/design-tokens.md` / the decision record / `design-system/<project-slug>/MASTER.md` on app surfaces; the run ledger for the smallest flows): (1) what job it serves, (2) what was considered and rejected, (3) how it matches the theme. The reasoning must consider the FULL experience, not just the UI: every decision's recorded reason addresses SIX dimensions, one line each — **Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`); **Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots); **Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`); **Visuals** (imagery, iconography, visual treatment, what it looks like); **Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind, e.g. a dealt moment, a diagram, an effect, a type moment, a craft-floor rule); **Colors** (palette tokens used, balance, contrast). A dimension that genuinely does not apply records `none — <reason>` — an explicit none, never a missing line. A decision whose recorded reasoning covers only layout/structure — the UI alone — does NOT satisfy this rule. A UI decision with no recorded reason, a missing dimension, or a layout-only reason is an incomplete build — a static check item in step 6, never a screen verdict. The audit/dry-run loop CHECKS the reasoning is present: the static checks verify every decision-record entry carries all six dimension lines, and the blind reviewer on UI diffs flags a missing dimension as a finding (minor at least). The check verifies the reasoning is PRESENT and addresses the dimensions — the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check.

**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).** The six dimensions above are unchanged — the fix #19 D19 rule text is verbatim and stays byte-identical (verify19 asserts it as a substring). This line EXTENDS it: every UI decision's recorded reason now addresses SEVEN dimensions, the six above plus **Depth** (the z-axis: layers — foreground / midground / background — elevation, perspective, parallax, occlusion, and depth of field; what sits in front, what sits behind, and how far apart the layers read, or `flat by choice — <reason>` where flat is the deliberate call). A decision-record entry is complete only when it carries all seven dimension lines; a missing Depth line is the same incompleteness as a missing sixth line — a static check item in step 6, never a screen verdict. Depth is a reason, not a mandate for 3D: a flat surface with a recorded `flat by choice — <reason>` satisfies the dimension.

**Body-only scope for the Tiempos rule (fix #20 — fix #19 F4 is body-only).** Tiempos and the Fraunces stand-in are for BASIC text only — body copy and plain reading text. They are NEVER used for important text. This binds each face in its role as the body/reading face: when Tiempos/Fraunces is the body face, it is never used for important text. A pairing that deals Fraunces (or Tiempos) as the *display* face, with a different face as the body face — for example the `fraunces` pairing in Taste's type catalogue (display Fraunces, Figtree body) — is governed by fix #19 F3 / fix #20 F5, not by this scope rule: on that build the face is the display face, not the body stand-in. Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses the display face (fix #20 F5), never the body face. A build that sets a heading, hero line, call to action, or key label in the body face is an incomplete build — a static check item in step 6, never a screen verdict. Boundary: fix #19 F3 governs the display/important face; fix #19 F4 governs basic text only. A face is either the display face (important text) or the body face (basic text), never both on the same build — except a scoped, recorded exception under this scope rule. Where a dealt theme names the same face for display and body, the design-lead deals a distinct display face and records it in `docs/design-tokens.md`; keeping the collision is a scoped, recorded exception with a fix #19 D19 reason AND the impressive-bar justification (fix #20 F6) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback).

**Important text uses a unique, important font (fix #20 F5).** Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses a UNIQUE, IMPORTANT font: a distinctive display face, chosen through the design skills (the dealt display face in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with its fix #19 D19 reason and its impressive-bar justification (fix #20 F6). Not the body face, not a generic/system font. A 'key label' is a label meant to stand out — a featured section label, an emphasis badge or price label. Ordinary small labels — nav links, table heads, captions, chips, form labels, meta rows — follow the Hallmark gates: the body face, a step smaller, sentence case, untracked. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2). A build that sets important text in the body face, or in a generic/system font, is an incomplete build — a static check item in step 6, never a screen verdict.

**The design just has to be impressive (fix #20 F6 — the governing bar).** The font rules serve this standard; a font choice that is correct per the rules but leaves the design unimpressive still fails. The finish review judges impressiveness as a verdict — browser-qa's visual verdict on the rendered screens, never a static check — and the decision record must state, for the important font on each surface, why it is the impressive choice for that surface (what makes it stand out, what it beats, why this surface earns it). A decision record that cannot say why the important font is impressive is an incomplete build. This bar connects to, and does not replace, the existing posture: more-not-bolder (fix #13), the E1 creativity push (trailblazing, not dumb), and fix #19 D19 (the six-dimension reason). A design that is rule-correct but unimpressive fails at the finish review; a design that is impressive but breaks a ban still fails — the bar governs, the bans bind.

**Every build carries a distinct brand identity (fix #20 B1).** The build carries the product's own brand — its wordmark, its identity tokens (the name, the mark, the voice, the palette and type that are its own), and its voice — recorded in the decision record (`docs/design-tokens.md` / MASTER.md on app surfaces). The brand is the through-line: every surface, component, and decision expresses it. A build with no recorded brand identity — no wordmark, no identity tokens, no voice on the record — is an incomplete build — a static check item in step 6, never a screen verdict. The brand is generated through the skills (the dealt direction in Taste step 4a / the ui-ux-pro-max identity), never inherited from a template; a build that reads as a generic template has, by definition, no brand. When a project already has a brand (a real product, a real wordmark), the record names it and the build conforms to it; when it does not, the build deals one and records it.

- **Animated brand mark — liquid-logo, a standalone tool (fix #22 §15, LIQLOGO_F22).** liquid-logo is a STANDALONE TOOL, not a library to import and not a runtime dependency: run it (or its hosted version at liquid.paper.design) to produce the animated brand mark ONCE — export MP4/PNG, or port the shader idea into a small R3F shader — and ship the output as an asset. Pin: repo commit `689bb38a1e0d5a6a8baf2d34847635eefde19994` (paper-design/liquid-logo, `package.json` version 0.1.0, `private: true` — there is no published package to install). Licences, both recorded: the liquid-logo repo itself is under the PolyForm Shield Licence 1.0.0 (NOT MIT — it carries a noncompete clause: do not use the tool to provide a competing product); the effect is built on `@paper-design/shaders-react` (Apache 2.0, latest 0.0.82 — the tool itself pins 0.0.21 in its own `package.json`). The animated logo is a brand asset, generated once — never runtime-heavy, never the only logo: the original static logo is kept as the fallback for old phones and non-WebGL contexts, and a build using the animated logo with no static fallback FAILS the check. Retain paper-design attribution in a code comment where the asset is used. Input requirements (honest check first): the input must be a transparent PNG/SVG with high contrast, solid shapes, no gradients or drop shadows, and no thin details. Before producing it, ask and answer honestly: "tell me honestly whether the logo will work with this shader" — if the logo has thin details, gradients, or low contrast, the answer is no and the static logo ships alone; do not force the effect onto an unsuitable mark. (D19 — Motion: the animation is the brand motion, produced once, never runtime-heavy; Theme: the mark is the build's own brand, theme-matched; Texture: none — the mark is an asset, not a surface treatment; Visuals: the animated mark is the brand anchor, the static logo is the fallback where it cannot play; Techniques: standalone tool at the pinned commit, MP4/PNG asset output, attribution comment retained; Colors: none — the metal is the shader's own chrome, the brand's colours are unchanged.)

**Every component is an experience (fix #20 X1).** Each component is designed as a moment/interaction, not a static functional block. Every component entry in the decision record states the experience it creates — what it feels like, what moment it is — alongside its six fix #19 D19 dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors). A component recorded only as a functional block ("a card that shows X", "a list of items") with no experience statement is an incomplete build — a static check item in step 6, never a screen verdict. The experience statement is the component's own: what the user feels using it, what moment it stages, what it does that a static block would not. A component with no interactive or felt quality records that explicitly (`no felt moment — <reason>`, e.g. a legally-required static notice) — an explicit none, never a missing line.

**Long body and small text only — the Tiempos rule tightened (fix #21 — fix #19 F4 tightened).** Tiempos and the Fraunces stand-in are for LONG-LENGTH body text and SMALL incidental text only — running paragraphs of reading prose, and small text here and there (ordinary small labels: captions, meta rows, table heads, form labels, chips, small nav links). They are NOT a default for text generally, and they are NEVER used for main text we see visually. 'Body and plain text use Tiempos' (fix #19 F4) reads, after this fix, as long-length body text and small incidental text only. A build that sets its labels, captions, buttons, prices, names, or any other text element in the body face by default — with no artistic font decision behind it — is an incomplete build, even if no single element is 'important' text. The body face is the face serving as body/reading text on that build; the role-scoping from fix #20 stands (a pairing that deals Fraunces as the display face, with a different face as body, is governed by fix #19 F3 / fix #20 F5, not by this scope rule).

**Every text element gets an artistic font design decision (fix #21 F7).** Every text element — heading, label, caption, button, price, name, body, meta row, table head, chip, nav link, call to action — has a deliberate, recorded artistic font design decision behind it: which face, why this face, what job it serves, how it matches the theme and the brand. The decision is recorded in the decision record's Type list, per text element — or per text class where the class is genuinely uniform (one decision line per class, naming the class and the face and the reason; a blanket 'all text' line is not a class decision). No text element defaults to the body face without a decision. Main text we see visually — headings, display type, hero text, prominent labels, prices, names — uses the unique important font (fix #20 F5) or another artistic face chosen through the skills, never the body face as a default. A text element with no recorded artistic font decision, or a main visible text element set in the body face, is an incomplete build — a static check item in step 6, never a screen verdict. The decision is covered by its fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions); the font decision is the D19 reason for that text element's font choice.

**Redesign of an existing page (keeping content + wiring).** When the job is a full-page redesign that keeps every fact, link, form, field, handler, route, id, and test hook, follow the Hallmark redesign flow (`references/hallmark/references/redesign.md`) — factory routing for the redesign flow lives there: page subagents are single-task factory drones with director briefs (GLOBAL-ROUTING_F29). record the before-state (`sloplint --before`, links/fields/handlers/headings + screenshots to `.hallmark/before*`), build, then `sloplint --kept` — anything lost is `FAIL kept` / `WARN kept`. Depths: **full** (system + composition change; default), **restyle** (system only, keep the layout), **polish** (only what a gate names).

5. **Build.** In `starter.html`: set `<html lang data-type data-radius data-buttons data-motion>`
   (lang: the brief's language), the three metas, the head block (title, description, og, icon,
   theme-color: `system.md`, Head) and the nav class; keep the skip link and the `m-enter` head
   line; copy only the `<section class="hero …" data-enter>` of
   `assets/layout/hero-<id>.html` (never its nav, other sections, footer or credit line; every word
   and picture becomes the client's); move the dealt close and footer out of their `<template>`s
   and delete the rest. Every section is `main > section` with
   one `.wrap`, its h2 first, `--h: 1` or `2`. Build each to its recipe with the system's classes
   and tokens; write page CSS only where a reference says page CSS (inside a visual, `--p-h`,
   `.wall`, `.rail`, `.device`). Paste UI from `assets/ui/<name>/fragment.html` and rewrite every
   name, number and logo to the client's (kit icons become `data-icon`, `cards.md`); a diagram card is `data-diagram="<preset>"`
   with the client's labels; run `icons.mjs scan index.html --out assets/icons --colour` last, so every icon
   the page names is a local file. Mount an effect, object, moment or scene exactly as its
   reference says, never from your own script. A moment's section is copied from
   `assets/moments/_demo/in-page.html` (place: photo-chapters, word-highlight) or
   `in-page-service.html` (pinned-chapters, picture-develops film); a moment's own `demo.html` shows
   it alone and is not a page model. A form is the starter's `booking-form` (`system.md`,
   Forms). Credits: the one footer line from `photos.mjs credits`, once the markup uses the
   photographs (it reads the page). Copy the hero's tile from `shoot.mjs` beside the page as `share.jpg`. **The dealt hero's loop is implemented or waived (fix #15 R4 — baseline: the centred-hero spec's loop inside the window was never applied).** The dealt hero's loop (or moment-inside-window) is implemented and recorded in `docs/design-tokens.md`, or waived with reason there. **Pattern reference while building (fix #22 §9, MOBBIN_PATTERN_F22):** when a build needs a component or flow this skill describes abstractly, the implementing agent MAY consult the matching Mobbin pattern (mobbin.com) for how real apps handle it — structure, states, conventions — then implements it through this skill, theme-matched, with a D19 reason. Dealt moments may be informed by real patterns but are generated through Taste. The no-copy boundary: Mobbin informs pattern knowledge only — never the design direction, never a screen to copy; the generating skill is always the recorded source in `docs/design-tokens.md`, never a Mobbin URL, and a specific Mobbin screen is never cited as the source of a decision. Access is web browsing only on the free tier ($0; limited apps/sites, no search, no Flows/Animations, 3 collections) — no paid subscription, no paid account, no account creation that costs money, no API/MCP on the free tier. If the needed pattern is paywalled or Mobbin is unreachable, build from the skills alone and record the gap — the build is NEVER blocked on Mobbin. Platform match: web patterns for web builds; iOS/Android patterns only where the build is a mobile-web surface and the pattern transfers. Theme-match precondition: a pattern is applied only when it matches the dealt theme. (D19 — Motion: patterns inform how a flow moves; Theme: the dealt theme filters which patterns apply; Texture: none — pattern reference sets no surface treatment; Visuals: patterns inform the structure users expect; Techniques: consultation is category-level browsing, never copying a screen; Colors: none — pattern reference sets no colour.)

6. **Check and look.** Only the skill's scripts, each running one headless Chrome with WebGL on the
   CPU, closed by its own PID, one at a time in the foreground with a 10-minute timeout; never in
   the background, a windowed browser or a browser tool.
   Each serves the page file itself over http on 127.0.0.1 (never `file://`), so no server is needed;
   for a built page whose links start at the site root (`/_astro/page.css`), pass `--root` with the build folder (`dist`).
   `--profile <dir>` is the Chrome profile: a folder of its own in the OS temp folder or in the
   project's `.taste-skill` folder (`.taste-skill/chrome-check`), never outside the project (no
   `../`); a relative one that leads out of it is replaced by `.taste-skill/chrome-<script>`. Then:

   ```bash
   node <skill>/scripts/copy-lint.mjs index.html --kind <kind>
   node <skill>/scripts/consistency.mjs index.html --widths 1440,1024,820,768,390 --rhythm-widths 1440,820,768,390 --profile <dir> --page <kind> --category "<what is sold>" --primary "<main action>"
   node <skill>/assets/layout/check.mjs --url index.html --profile <dir> --sizes 1440x900,1024x768,820x1180,768x1024,390x844 --shots shots/layout
   node <skill>/scripts/shoot.mjs --url index.html --w 1440 --out shots/1440.png --profile <dir>
   node <skill>/scripts/perf.mjs index.html --profile <dir>
   ```

   Shoot 1024, 820x1180, 768x1024 and 390 as well. Every `check.mjs` finding fails the page on layout-correctness grounds (no `--no-stress`); a layout finding is not a distinctiveness verdict — that is `browser-qa`'s alone.
   copy-lint opens no browser and takes under a second. Fix every FAIL (a copy-lint WARN too, or say
   why it stays) and read the copy aloud (`copy-voice.md` section 6); shoot again and read every
   screenshot against the checklist. Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1). **Copy + type checks enforced and recorded (fix #15 C3).** Taste copy-voice rules apply to ALL copy; craft-floor type checks (body measure 65–75ch, obvious scale/weight steps, balanced headings, contrast 4.5:1 / 3:1 large) are verified per surface and recorded in `docs/design-tokens.md`'s Type list (surface → face/size/measure/contrast). In the fix rounds run `consistency.mjs --quick --widths
   1440,390`. Then the gate, which runs the checker at 1440 and 390 every time, walks the page at 320
   for overflow, collide and tap-size, and runs copy-lint, whose FAILs block like the checker's:

   **Fix #17 static checks (all static checks, never screen verdicts).** (U1) The 'Unique elements' list in `docs/design-tokens.md` has at least three complete entries — element, surface, kind, section job, theme material, why-not-a-catalogue-item — with at least one on the primary page; fewer is an incomplete build. (F1) The Type list gains weight and tracking columns and a Source cell per row naming the exact skill text; a row with an empty or 'default' Source is an incomplete build. (T1) Each Type-list row records the fill ratio (glyph box / container box, minimum 0.60), and the screenshot check includes the dead-space item (a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding). (M1–M6) The Motion list records, per surface: each scroll entrance with its tokens and fail-safe mechanism (M1/M2, motion-governed surfaces only — landing pages keep the Taste scroll ban except where a theme file records a scoped exception); hovered shots per interactive surface and each distinct hover behaviour (M3); each authored motion piece with its trigger, confirmed moving in the D1 pass (M4); one working interactive bit per page with an interactive surface, or the recorded exemption 'no interactive surface — none' (M5); the reduced-motion render noted, or recorded as not run (M6). (E1) Each Unique-list entry carries the nine-point bound checklist, all passing, or the failure recorded as a finding; a floor/ban break blocks.

   **Fix #19 static checks (all static checks, never screen verdicts).** (F2) The Type list names, per face, its static files (weight → file) with source and preloads; a row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build. (F3) The pairing is recorded with a Source cell naming the exact skill text; a pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build. (F4) Body/plain text is Tiempos or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. (D1 face check) The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths — a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding. (D19) Every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; an entry missing a dimension, or a reason covering only layout/structure, is an incomplete build.

   **Fix #20 static checks (all static checks, never screen verdicts).** (F4 scope) The Type list marks the body face as body-only — the body face is the face serving as body/reading text on that build, so a pairing that deals Fraunces as the display face (with a different body face) is checked under F5, not here; no heading, display, hero, call-to-action, or key-label token points at the body face; a dealt theme naming the same face for display and body is either re-dealt with a distinct display face or recorded as a scoped exception with a fix #19 D19 reason and a fix #20 F6 justification. (F5) Every important-text token points at the display face; the display face is recorded with its fix #19 D19 reason and its fix #20 F6 justification; a build setting important text in the body face or a generic/system font is an incomplete build. (F6 record) The decision record states, for the important font on each surface, why it is the impressive choice for that surface; a record that cannot say so is an incomplete build. (F6 verdict) The impressiveness verdict itself is browser-qa's at the finish review, never a static check. (B1) The decision record names the build's brand identity (wordmark, identity tokens, voice); a build with no recorded brand identity is an incomplete build. (X1) Every component entry in the decision record states the experience it creates (what it feels like, what moment it is) alongside the six D19 dimension lines; a component recorded only as a functional block is an incomplete build.

   **Fix #21 static checks (all static checks, never screen verdicts).** (F4 tight) The Type list marks the body face as long-body-and-small-text-only — no token for main visible text points at the body face; the body face serves long-length body text and small incidental text only. (F7) Every text element in the Type list — or every genuinely uniform text class — carries its recorded artistic font decision (face + why + job + theme/brand fit); a text element with no recorded decision is an incomplete build; a main visible text element (heading, display, hero, prominent label, price, name, call to action) set in the body face is an incomplete build; a blanket 'all text' class line is not a class decision. (F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice.

   **Fix #22 static check (all static checks, never screen verdicts).** (TRENDS_F22) A trend used without a theme-match reason in `docs/design-tokens.md` is an incomplete build. Run the SLOP_F22 slop checklist in polish-pass as a static check; its flags are candidate evidence for browser-qa, never verdicts.

   **Fix #23 static checks (all static checks, never screen verdicts).** (HERO_F23) The decision record carries a hero-moment line (dealt moment + distinctive composition + motion values, with its D19 reason) and the Picks block (`.hallmark/picks.md`) carries the matching Hero-moment row; a hero with no recorded moment, or a Picks block with no Hero-moment row, is an incomplete build. (FUNC_F23) The decision record states the functionality story (what is technically new, and how the design shows it) and the build shows its mechanism (diagram / live data / system state) on the hero surface or the first screen after it; a build with no recorded functionality story, or no mechanism visible early, is an incomplete build. The verdicts themselves — whether the hero is amazing, whether the mechanism reads as groundbreaking — are `browser-qa`'s alone (HERO-BQA_F23, FUNC-BQA_F23), never a static check.

   ```bash
   node <skill>/scripts/gate.mjs index.html
   ```

   Fix what it lists and run it again until its last line is `GATE: PASS` or `GATE: OPEN`, three
   rounds at most (to ask the user something after a block, just stop again). During a hackathon first build after grill-me, there is no user to ask — and a one-prompt removal of a first-build feature is auto-approved whenever it happens, so there is no user to ask then either: after 3 rounds without `GATE: PASS` or `GATE: OPEN`, stop, record the last `GATE:` line and every open FAIL in the final report, and finish — do not loop further and do not wait. When the user tells you
   to stop, or to ship the page as it is, run `gate.mjs --done "<what they said>"` (`GATE: DONE`)
   and report the open FAILs.
   `GATE: SETUP` (no page yet, a framework's source shell, a page that is not local): arm what a
   browser can open (step 1) and run it again. `GATE: ERROR` (the checks could not run) or
   `GATE: OFF`: put the line in the report and finish; do not rerun. Never edit
   the kit's files or hide anything from the checker. A FAIL you judge false is waived in
   `.taste-skill/waivers.json` with its reason, never fixed by gaming the check (`references/gate.md`);
   a word from the client's own copy that copy-lint FAILs is waived hit by hit, the brief as the reason
   (a word inside the client's name, as the logo or the title writes it, is not counted: one WARN).

   **Screenshot QA at least once before finish (fix #15 D1).** Before the final report is written, the build runs a screenshot QA pass at least once: the rendered page/app is inspected in screenshots (desktop + mobile) for whitespace, sizing, spacing, alignment, overflow, and collisions. The pass counts toward the requirement from whichever existing tooling ran it (Taste shoot.mjs / check.mjs / consistency.mjs, polish-pass before/after verification, or browser-qa's visual loop) — do not run a duplicate pass to satisfy it; record the run (tool, screens, findings count) in the run ledger and the final report. A build that never ran a screenshot QA pass is incomplete and cannot be reported as finished. Findings feed the fix batch like other checks; browser-qa alone issues pass/fail verdicts on rendered screens.

   **Hallmark sloplint.** Before the report, run the Hallmark gate checker on the built page:

   ```bash
   node <skill>/references/hallmark/scripts/sloplint.mjs index.html --render
   ```

   The static tier always runs. The render tier needs `puppeteer-core` + Chrome: if `puppeteer-core` is missing, install the pinned version (`npm i -g puppeteer-core@25.17.0` — it cannot reuse the plugin's Playwright as a drop-in; the render script is written against the Puppeteer API); if Chrome is not found, set `CHROME_PATH` to the Chrome install (on Windows usually `C:\Program Files\Google\Chrome\Application\chrome.exe`). If the render tier cannot run, run the static tier only and record that the render tier did not run — never claim a render pass. Fix every `FAIL`; fix or waive every `REFLEX` (waivers recorded in the CSS stamp, per `references/hallmark/references/gates.md`).

   **Hallmark hero review.** Once the hero is built and shot, run the hero review in a fresh context — **when both this hero review and the finish review (orchestrate Verify stage 6) apply, they run as ONE fresh-context review (fix #27, W3_F27): the same fresh-context sub-agent reads both prompts (`review-hero.md` + `review-finish.md`) and returns one verdict set; do not spend two fresh contexts on the same screens.** A sub-agent if the harness has one (it reads `references/hallmark/references/review-hero.md` and follows it — you do not read the prompt yourself; pass the hero screenshots, the stamp's first two lines, and the Picks block (`.hallmark/picks.md`, written at the deal — its Material + Signature rows) as file paths); otherwise re-read the prompt yourself and judge from the screenshots alone. Act on its first word (`no-findings` / `findings`) for the craft findings; findings join the fix batch — EXCEPT template observations (anything that reads as a template, or that a model would be expected to make for this prompt), which are candidate evidence for `browser-qa`, never fix-batch verdicts: append them to `.hallmark/candidate-evidence.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge. Write the hero review's findings to `.hallmark/hero-review.md` in the project root as soon as the review returns, and update the file with how each finding was settled (fixed, or waived with its reason) when you act on it — the finish review in Verify reads this file, so it must list every finding and its settlement, not just the open ones.

7. **Report:** the `GATE:` line first, then every waiver with its reason and every open FAIL; the
   kind, the deal (palette and why it fits, pairing, hero, grounds, effect, moments, scene); the
   voice card in one line and every copy-lint WARN kept, with why; the checker, layout and perf
   results; what you could not check; every assumed fact (the checker's `assumed` list) and the
   coined name's search; the form's `.example` stand-in and the canonical domain still to come; the photographs and art the client must supply, every
   stand-in frame among them (library and live search); every client slot, its file and its stand-in.

## 5. Checklist
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

Each line names its checks: `consistency.mjs` ids in brackets, `check.mjs` findings in braces,
`perf.mjs` rows. The last line is for your eyes.

- **First screen:** says what is sold, for whom or where, with one hard fact [copy-headline,
  copy-fact]; the hero fills it alone at every width, its main button inside it [hero-screen,
  hero-fill, fold-action, fold-cut] {hero-fold}; the hero carries its dealt amazing moment (HERO_F23), and the mechanism is visible early — on this screen or the first screen after it (FUNC_F23).
- **One section per screen:** every section 1 or 2 screens, its h2 first and top-aligned, no
  neighbour's heading or picture in its tile, nothing sparse, no section half empty [section-height, one-section,
  one-heading, section-air, one-screen, section-gaps, empty-area] {screen-short, screen-height, sparse,
  neighbour, neighbour-ground}.
- **Equal edges:** every block on the `.wrap` lines or the grid's columns, nothing out to one side,
  no sideways scroll [container-edges, row-lines, split-pair, off-grid, right-edge, col-edge,
  spill, off-viewport, stagger, top-stagger] {edge-left, edge-right, spill, bleed-one-side,
  one-sided, lines}.
- **Every visual draws** at 1440, 1024, 768 and 390; a refused effect shows its still fallback
  [visual-empty, empty-visual, gl-fallback, shader-lint, no-visual, photo-weight].
- **No caption** explains, apologises for or labels a picture; credits in one footer line
  [visual-caption, caption, credit-wall, photo-credit]; no placeholder, sample note or printed
  `.example` address [placeholder, sample-label].
- **The right things for the kind:** outside tech no effect ground, print or scene, only the
  dealt photo- or type-led moments (WebGL only for a product render the brief asked for)
  [effect-kind, effects-fit, photo-print]; the subject itself
  shows: the product big, whole in three sections at most, a new picture each [product-shown,
  same-object, photo-repeat]; each asset the brief names in its slot; a game's name and its world as key art,
  the diff of a code-review tool, software's `app-frame`;
  real photographs where they fit, none twice [photo-set, photo-repeat, photo-upscale]; real icons in their own
  colours; flat grounds on other [grounds]; a place deals two different compositions and one type
  moment.
- **Motion:** every button, link, linked card and linked photograph visibly answers the pointer,
  nothing tilts [motion-layer, hover, hover-move, tilt]; the hero enters once on load
  [hero-enter]; one or two dealt moments [moment-none]; card loops cycle in 2.5-4 s [loop-cycle]; nothing moves because the page scrolled
  except a dealt moment inside its own section (every kind) or the big scene (tech)
  [scroll-linked, scroll-reveal, pinned: expected only there]; anything
  moving past 5 s has a pause button [loop-pause]; under reduced motion everything rests and nothing
  stays hidden [reduced-motion, hidden-content]; at most four live contexts [webgl].
- **Contacts** as rule 9 [street-number, postcode, coordinates, company-number, phone-number];
  Get directions only with a street, "See the area" with a district, no map link with a town only [map-link].
- **Keyboard and head:** every control named, alt on pictures, labels you can see, headings one
  level at a time, no tabindex above 0; Tab reaches the skip link first, its ring shows at once and
  never under the header; the menu button says its state; lang, title, description and share tags
  [a11y-name, img-alt, field-label, heading-order, tabindex, skip-link, focus-ring, focus-visible,
  focus-hidden, menu-toggle, lang, page-meta, share-meta].
- **One system:** one button pair, one card style, one radius scale, one link look [button-styles,
  button-shape, card-family, card-layout, link-styles]; two boxes deep at most [nesting]; one
  heading scale, its faces loaded [heading-scale, font-load]; text contrast [text-contrast,
  contrast].
- **Copy and links:** headings name things, buttons a verb and an object, at most two hero actions
  [copy-headings, copy-buttons, copy-actions, action-count]; one action twice a screen at most
  [action-repeat]; a heading's grey half is its own sentence [run-on]; one fact, one wording
  [fact-agree]; assumed facts marked, never an open-now line from them [assumed, open-now]; every
  link lands, forms send, a confirmation only after a real send, each error under its own field
  [links, forms, form-send, form-fields]; no slop word, stock line, leftover or device used as a
  tic, a voice of its own (copy-lint's ids: copy-residue, copy-slop-word, copy-stock-phrase,
  copy-two-fragment, copy-virtue, ...; `copy-voice.md`).
- **Fast:** no FAIL row in `perf.mjs` (image weight, contexts, layout shift).
- **820, 768, 390 and 320:** sections on their screens [section-height]; on a phone a section is at
  least its screens and grows with what it holds, so nothing lies on anything else or under a fixed
  bar [collide]; every link and control outside running text 44px tall [tap-size] (a FAIL when
  another target is under 8px away); nothing past the screen at 320 [off-viewport], and nothing
  lies on anything else there either [collide]; the first screen ending whole or on a clear bleed [fold-card]
  (`layout-v4.md`); splits stack text first, no row half empty; one column at 390, buttons full
  width, a full-screen menu; the place action bar.
- **Your eyes:** beside the figma.com and x.ai frames it reads as a professional company site;
  nothing tilted, staggered, cut or overlapping; the hero is the work, not a mood.

## 6. Never

- A card, row or tile that fades in on scroll; a fade-in on every section; parallax on text;
  scroll-jacking; random blinking.
- Stock photographs passed off as the client's product, people or place (a stand-in is listed in
  the report as one, never shown with another maker's name or logo); a product page that never
  shows the product.
- A drawn look-alike of a real logo; invented reviews, quotes, customers or figures.
- Violet or lavender in the page's own design: accent, ground, gradient, effect colour or tint (a
  real third-party logo keeps its own colours, `icons.md`).
- Copying a reference site's code, copy, pictures or signature effect.
- Deleting or editing the kit's own files (`assets/`, `scripts/`) to clear a check: a check that
  flags a kit file is reported, and the page is checked again after any change.

## References

All in `references/`; section 3 names the one each asset needs.

## Cursor note

This skill was written for Cursor. In this Cursor plugin the finish gate does not auto-run on stop (the Cursor `Stop` hook was removed from the frontmatter); run it explicitly as step 6 says (`node <skill>/scripts/gate.mjs index.html`) and repeat until `GATE: PASS` or `GATE: OPEN`. The skill needs Node 22+ and Chrome, Edge or Chromium.

## Attribution

Taste skill (design-taste-frontend, v2.5.1) by Leonxlnx, MIT licensed. Source: https://github.com/Leonxlnx/taste-skill. Included in hackathon-ecc with only the Cursor hook removed for Cursor; all other content is the original.
