# Fix #22 §11 patch specs — 4 free GitHub design asset libraries

**Status:** patch specs for the integrator + one applied staged edit (LIB-05).
Do NOT edit `build.sh` from this file alone — apply each build.sh-embedded spec as
a patch in the existing build.sh patch blocks for the target file (same convention
as the existing `audit_patch` / `audit2_patch` entries and as `fix22/ab-patches.md`
/ `fix22/process-patches.md`), then rebuild. Do NOT edit `hackathon-ecc/` directly.
Do NOT run `bash build.sh` as part of applying (the integrator rebuilds once).
Do NOT run `fix11/fix11-stage.py`.

**Anchor convention (same as ab-patches.md):** every anchor below was verified to
occur EXACTLY ONCE in its target file in the Audit #66 built tree (count==1,
checked 2026-11-12). Apply in the fix17 style: assert the anchor count is 1,
fail the build loudly on mismatch, never guess. Insert AFTER the anchor unless
the entry says BEFORE.

**Anchor-collision check (2026-11-12):** none of the anchors below collides with
any anchor in `fix22/ab-patches.md` (AB-01–AB-14), `fix22/process-patches.md`
(P1–P5), or with each other. Specifically avoided: AB-04/AB-05's shared Rule-10
anchor ("reduced-motion renders are exempt from the entrance itself but never
from visibility"), AB-03's `motionTokens` block (LIB-01 deliberately adds NO
token entry — see its note), AB-06 (before `### Modal`), AB-07 (before
`### Toast stack`), AB-08 (before `### Accordion`), AB-12/AB-13/AB-14 and P1/P2
anchors in ui-ux-pro-max. AB-03's conflict flags (30ms stagger vs Rule 5's
0.05s floor; exit 0.8× vs quick-reference ~60–70%; press 0.95 vs polish 0.97)
are NOT re-litigated here — LIB-02/LIB-04 route the token values as they stand
and cite the flags where a value is under one.

**Anchor tokens for cross-reference / verify22.py:** LENIS_F22 (LIB-01, LIB-02,
LIB-03), GSAP_F22 (LIB-03, LIB-04), SCROLLTRIGGER_F22 (LIB-02, LIB-04),
VANTA_F22 (LIB-05 applied, LIB-06), REACTBITS_F22 (LIB-07, LIB-08). All five
tokens were 0 in build.sh and 0 in the built tree before this fix (checked
2026-11-12).

**Pinned versions (all verified live 2026-11-12 — see `fix22/libraries-report.md`
for sources):**
- Lenis `lenis@1.3.27`, MIT — npm registry latest, gitHead
  `1f60fb9199a823f10fb23f7df55011defbb2747a`.
- GSAP `gsap@3.15.1`, GreenSock Standard "no charge" licence (free, all plugins
  incl. commercial, since 3.13) — NOT MIT; see report §5 deviation D1.
- Vanta `vanta@0.5.24`, MIT, plus `three@0.134.0` (r134, the README-documented
  pair) — NOT the latest three.js (0.187.0) and NOT the plugin's general three
  pin (0.185.1); see report §5 deviations D3–D4.
- React Bits: no npm package — pinned repo commit
  `9d9c687dc4f55b23539aa5417b703078047efa74` (2026-11-10), MIT + Commons Clause
  — NOT pure MIT; see report §5 deviation D2.

**Bundled vs install-on-demand (per library, following the plugin's existing
convention — node_modules ships only plugin-script deps, exact-pinned in
package.json + package-lock.json + `npm ci` per build.sh:13735–13737;
puppeteer-core is install-only at a pinned version; CBM binary is NOT bundled):**
all four libraries are INSTALL-ON-DEMAND per project build, never bundled in
the plugin. Lenis / GSAP / Vanta (+ three.js) install as exact-pinned npm deps
in the generated project's package.json + lockfile. React Bits is copy-paste
source vendored into the project at the pinned commit (no runtime dependency).
Full reasoning per library is in `fix22/libraries-report.md` §4.

Banned terms check: none of the new texts below contains any of the seven banned
terms (case-insensitive). The word "AI" does not appear in them.

---

## LIB-01 — motion-foundations, smooth-scroll rule (Lenis) (LENIS_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, `### When to disable animation
  entirely` section.
- **Built-tree location:** lines 87–94 (the disable list; anchor is its last line).
- **Anchor (count==1, insert AFTER):**

  ```
  - The animation is purely decorative with no UX purpose
  ```

- **Insert (full text):**

```md

### Smooth scroll — Lenis (fix #22 §11, LENIS_F22)

Smooth scrolling is a scroll behaviour, not an animation: where a build wants
buttery, momentum-based scrolling, the approved mechanism is Lenis
(`lenis@1.3.27`, MIT, vanilla JS, all stacks). Lenis owns the scroll; it never
owns the animation — scroll-driven animation is driven by GSAP ScrollTrigger
(see `motion-patterns` scroll routing, SCROLLTRIGGER_F22) or by `motion/react`
`useScroll`, never by Lenis itself. Directed init (§10): `new Lenis({
autoRaf: true, lerp: 0.1, anchors: true })` — `lerp: 0.1` is the directed
smoothing value; do not tune it per component. Lenis is NOT initialised when
`prefers-reduced-motion: reduce` matches or on low-end devices
(`motionConfig.shouldAnimate()` false): native scroll is the fallback, and
anchor navigation still works. SCOPE: motion-governed app surfaces only
(React/Next.js and other app stacks). The design-taste-frontend page system
keeps its standing rule (`references/motion.md`: no smooth-scroll library on
any Taste landing page) — Lenis never applies there, and a Taste landing page
that initialises Lenis is an incomplete build. Lenis is a menu item, never a
default: a build that adds smooth scrolling with no theme reason — no dealt
moment or scroll story that needs it — does not add it. Theme-match
precondition: smooth scrolling is a feel decision, not a look — it must still
match the dealt theme's motion voice; a clash is not applied, with the reason
recorded in `docs/design-tokens.md`.

(D19 — Motion: Lenis decides how the scroll itself feels — the smoothing value
is the motion decision; Theme: the scroll feel is the dealt theme's motion
voice, never a stock glide; Texture: none — Lenis adds no surface treatment;
Visuals: the scroll stays native (real scroll positions, working anchors, no
transform illusion), so layout and sticky behaviour never break; Techniques:
the single approved mechanism is Lenis at the pinned version, initialised once
per page with the directed options above; Colors: none — Lenis chooses no
colours.)
```

- **Note — no `motionTokens` entry:** the Lenis values (`lerp: 0.1`) live in the
  directed init above, not in `motionTokens`. AB-03 owns the token block and a
  token edit here would collide with its anchors; a future token pass may move
  the Lenis values into `motionTokens`. Flagged for the coordinator, not a
  silent change.
- **Note — Constraints line untouched:** the skill's Constraints line
  ("Third-party animation libraries (GSAP, anime.js, etc.)" — not covered)
  stays as-is. It refers to animation engines; Lenis is a scroll mechanism
  named here only as the approved smooth-scroll rule, not as an animation
  library the skill teaches. Flagged for the coordinator in the report.

## LIB-02 — motion-patterns, scroll routing through Lenis + ScrollTrigger (LENIS_F22 / SCROLLTRIGGER_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples` section,
  after the Scroll progress bar example.
- **Built-tree location:** lines 275–291 (anchor is the tail of the
  `ScrollProgress` function).
- **Anchor (count==1, insert AFTER):**

  ```tsx
        style={{ scaleX: scrollYProgress }}
      />
    )
  }
  ```

  (The line `style={{ scaleX: scrollYProgress }}` alone was verified count==1;
  the 4-line tail above is the anchor as applied.)

- **Insert (full text):**

```md

**Scroll-driven animation routes through Lenis + ScrollTrigger (fix #22 §11,
LENIS_F22 / SCROLLTRIGGER_F22).** The two patterns above — Scroll reveal and
Scroll progress bar — are the motion-* defaults on React/Next.js surfaces
(`useScroll` + `useTransform`, `whileInView`). Where the stack supports it and
the build uses GSAP, the same two patterns route through Lenis + ScrollTrigger
instead: Lenis owns the scroll (`lenis@1.3.27`, see `motion-foundations`
smooth-scroll rule, LENIS_F22), ScrollTrigger drives the animation
(`gsap@3.15.1`, `gsap.registerPlugin(ScrollTrigger)` once at the top of the
entry file before any `scrollTrigger` config — an unregistered ScrollTrigger
throws). Directed per §10 (effect name + exact parameters, never prose): a
scroll reveal is `gsap.from(el, { opacity: 0, y: 12, duration:
motionTokens.duration.slow, ease: motionTokens.easing.smooth, scrollTrigger: {
trigger: el, start: 'top 90%', toggleActions: 'play none none reverse' } })`;
a scroll progress bar is a scrubbed tween on `scrollYProgress` (see the `gsap`
domain rows in `ui-ux-pro-max` `data/motion.csv` — the 17 GSAP presets — for
the ready-to-use snippets, matched to the motion tier). The Group B token
values travel with the tween: dropdown duration
`motionTokens.duration.dropdown` (0.2s, 150–250ms band), row stagger
`motionTokens.duration.staggerRow` (0.03s — under the AB-03 conflict flag vs
Rule 5's 0.05s floor; the parent adjudicates), popover start scale
`motionTokens.scale.popover` (0.95), knob stretch
`motionTokens.scale.stretch` (1.12), exits at `motionTokens.exitFactor`
(0.8× the enter — under the AB-03 conflict flag vs quick-reference ~60–70%;
the parent adjudicates), entrances on `motionTokens.easing.smooth`, moves on
`motionTokens.easing.inOut`. The 1500ms fail-safe (fix #17 M2) still binds:
content revealed by a ScrollTrigger tween becomes visible within 1500ms of
entering the viewport even if the trigger never fires. Under
`prefers-reduced-motion: reduce` neither Lenis nor the ScrollTrigger tween
runs — the content renders at its final state immediately. SCOPE:
motion-governed app surfaces only; Taste landing pages keep their standing
rule (`references/motion.md`: scrolling moves nothing but the dealt moment).
Theme-match precondition: every element animated under this routing must still
match the dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: Lenis + ScrollTrigger decide how scroll position drives
animation, with the Group B token values as the tween parameters; Theme: the
scroll story is the dealt theme's motion voice, never a stock parallax;
Texture: none — the routing adds no surface treatment; Visuals: reveals and
progress stay anchored to real scroll position, so nothing appears or vanishes
off-scroll; Techniques: Lenis owns scroll, ScrollTrigger owns the animation,
values come from `motionTokens` (Rule 8); Colors: none — the routing chooses
no colours.)
```

## LIB-03 — ui-ux-pro-max, design asset libraries stack scope (LENIS_F22 / GSAP_F22 / VANTA_F22 / REACTBITS_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 4: Stack Guidelines`.
- **Built-tree location:** line 204 (the Available stacks line).
- **Anchor (count==1, insert AFTER):**

  ```
  **Available stacks:** `react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `angular`, `laravel`, `swiftui`, `react-native`, `flutter`, `jetpack-compose`, `html-tailwind`, `shadcn`, `threejs`, `javafx`, `wpf`, `winui`, `avalonia`, `uno`, `uwp`. Use the stack detected in Step 1.
  ```

- **Insert (full text):**

```md

**Design asset libraries — stack scope (fix #22 §11, LENIS_F22 / GSAP_F22 /
VANTA_F22 / REACTBITS_F22).** Four free libraries are approved menu items,
never defaults — each is chosen through the skills, theme-matched, with a D19
reason, and directed per §10 (library + effect name + exact parameters).
Stack scope: **Lenis** (`lenis@1.3.27`, MIT) and **GSAP** (`gsap@3.15.1`,
GreenSock Standard "no charge" licence — free, all plugins included) are
vanilla JS and available on every stack in the list above; **Vanta**
(`vanta@0.5.24`, MIT) is vanilla JS plus three.js (`three@0.134.0` for Vanta
scenes — the README-documented pair; the general three.js pin in
`data/stacks/threejs.csv` does not apply to Vanta scenes) and is used only for
dealt hero backgrounds / shader scenes on tech, gaming, software, and
hardware surfaces (see `design-taste-frontend` step 2, VANTA_F22); **React
Bits** (repo commit `9d9c687dc4f55b23539aa5417b703078047efa74`, MIT + Commons
Clause) is React/Next.js ONLY — on any other stack the pattern is
re-implemented with the stack's own tools (see `motion-patterns`,
REACTBITS_F22). Every library effect respects `prefers-reduced-motion: reduce`
(static fallback or off) — no library exempts the rule. Unpinned versions
("latest") FAIL the pin check. The pinned versions live here and in the owning
skills; a build that needs a newer version re-pins deliberately and records
the new pin + its verification, never floats. Theme-match precondition: a
library effect is applied only when it matches the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the libraries are the motion / scroll / background mechanisms,
chosen per build; Theme: every effect is theme-matched or not applied;
Texture: Vanta scenes and the Lenis scroll feel are texture / motion
treatments chosen through the theme; Visuals: scope keeps effects on the
surfaces where they read (3D backgrounds on tech heroes, bits on React);
Techniques: exact pins + stack scope, install-on-demand per project (see
`fix22/libraries-report.md` §4); Colors: none — the libraries choose no
colours (Vanta effect colours are the theme's own tokens).)
```

## LIB-04 — ui-ux-pro-max, GSAP extension: ScrollTrigger + Group B numbers through tweens (GSAP_F22 / SCROLLTRIGGER_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 2c: Design Dials`
  (the `--motion` bullet).
- **Built-tree location:** line 164 (the `--motion` bullet).
- **Anchor (count==1, insert AFTER):** the complete `--motion` bullet:

  ```
  - `--motion` attaches a ready-to-use GSAP snippet (with framework notes, Do/Don't, and performance notes) pulled from `--domain gsap`, matched to the resolved tier (Subtle/Standard/Complex). The `--motion` dial is only an intensity parameter — it picks how much motion, not how the interface should feel or when it should move. Motion feel and timing decisions belong to `make-interfaces-feel-better` (see `rules/hackathon-mode.mdc` §5): decide feel/timing there first and record the decision as one line in the design-system brief (MASTER.md) before setting `--motion`, then use `--motion` only to set the intensity tier of the implementation. Do not use `--motion` to make a feel/timing decision on its own.
  ```

- **Integrator note:** this bullet text also appears in build.sh at lines 7382,
  7401, 13253, 13272, and in a patch pair at 15825–15826 (embedded skill copies
  + patch-block copies). Apply this spec in the ui-ux-pro-max build.sh patch
  block (cf. build.sh:7263, same block as process-patches.md P1/P2), against
  the built-tree occurrence (SKILL.md:164) — do not patch the other build.sh
  copies.
- **Insert (full text):**

```md

- **GSAP is the animation engine; ScrollTrigger is its scroll plugin (fix #22
  §11, GSAP_F22 / SCROLLTRIGGER_F22).** The `--domain gsap` integration is
  verified intact: 17 GSAP presets in `data/motion.csv` (rows 1–17: hover,
  scroll reveal, stagger list, page transition, parallax, loading, and more),
  each with a ready-to-use snippet, framework notes, Do/Don't, and performance
  notes, matched to the motion tier (Subtle/Standard/Complex) by `--motion`.
  What is new here: **ScrollTrigger** (`gsap@3.15.1`, free with all plugins
  since GSAP 3.13 under the GreenSock Standard "no charge" licence) is the
  approved scroll-animation plugin — register it once
  (`gsap.registerPlugin(ScrollTrigger)`) before any `scrollTrigger` config,
  then drive scroll reveals, scrollytelling pins, parallax layers, and scroll
  progress bars through it (see `motion-patterns` scroll routing,
  SCROLLTRIGGER_F22). Note the preset snippets already use `scrollTrigger`
  configs (motion.csv rows 4–6, 13–14) — this rule names the plugin in the
  skill prose, where it was previously data-only. **Group B numbers travel
  through GSAP tweens:** where the build uses GSAP, the fix #22 Group B values
  are tween parameters, never prose — dropdown duration
  `motionTokens.duration.dropdown` (0.2s, 150–250ms band), row stagger
  `motionTokens.duration.staggerRow` (0.03s), popover start scale
  `motionTokens.scale.popover` (0.95), knob stretch
  `motionTokens.scale.stretch` (1.12), exits at `motionTokens.exitFactor`
  (0.8× the enter), entrances on `motionTokens.easing.smooth` (ease-out),
  moves on `motionTokens.easing.inOut` (ease-in-out). (Press scale is under
  the AB-03 conflict flag — `motionTokens.scale.press` 0.95 vs the polish
  default 0.97; the parent adjudicates; this spec does not set it.) A GSAP
  effect is directed per §10 (effect name + exact parameters: tween target,
  properties, duration, ease, stagger, ScrollTrigger config) — a GSAP effect
  described in prose without exact parameters is incomplete and FAILS the
  handoff check. Every GSAP tween respects `prefers-reduced-motion: reduce`
  (render the final state immediately — every preset's framework notes already
  say so). Pin: `gsap@3.15.1`, exact, in the project's package.json +
  lockfile; "latest" FAILS the pin check. Theme-match precondition: a GSAP
  effect is applied only when it matches the dealt theme; a clash is not
  applied, with the reason recorded in `docs/design-tokens.md`.

  (D19 — Motion: GSAP + ScrollTrigger are the animation engine — the Group B
  values are its tween parameters; Theme: effects are the dealt theme's motion
  voice, never stock tweens; Texture: none — GSAP adds no surface treatment;
  Visuals: ScrollTrigger keeps animation tied to real scroll position, so
  reveals never fire off-screen; Techniques: the 17 presets + `--domain gsap`
  search are the source, values come from `motionTokens`; Colors: none — GSAP
  chooses no colours.)
```

## LIB-05 — design-taste-frontend, Vanta as the approved animated-3D-background source (VANTA_F22) — APPLIED DIRECTLY

- **Target (staged source):**
  `new-skills/design-taste-frontend/SKILL.md`, section 2 (Tech bullet, the
  "one effect" deal line).
- **Status: APPLIED 2026-11-12.** Inserted after the "By deal: **one effect**"
  sentence (staged lines 123–124), before the "- **One object never carries
  the page.**" bullet. `VANTA_F22` now occurs exactly once in the file, at
  **line 126** (file now 607 lines, was 606). Verified by re-grep after the
  edit. No wave-1 text was touched (TRENDS_F22, DIRECTIVES_F22,
  MOBBIN_PATTERN_F22, and the step-6 static-check line are intact elsewhere in
  the file).
- **Text inserted (verbatim):**

```md
- **Animated 3D backgrounds come from Vanta (fix #22 §11, VANTA_F22).** Where the deal calls for the one effect as a shader ground or a big scene — tech, gaming, software, hardware only — the approved source is Vanta (`vanta@0.5.24`, MIT, plus `three@0.134.0`, the README-documented pair; vanilla JS; three.js-backed effects: WAVES, BIRDS, NET, FOG, CLOUDS, GLOBE, and the rest). The effect is directed per §10 (effect name + exact parameters: colour, scale, speed, mouse/touch controls on or off), recorded in `docs/design-tokens.md` with its fix #19 D19 reason — a Vanta scene is the dealt moment or the hero background, never a default wash. Constraints, all binding: theme-matched (the effect's colours are the theme's own tokens); a static fallback (the theme's gradient or image ground) on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; one Vanta scene per page by default (the four-WebGL-context cap above still binds); destroy the effect on unmount (`effect.destroy()`). p5.js-backed Vanta effects (e.g. TRUNK) are not covered — no p5 pin, recorded-gap if a build wants one. A Vanta background with no reduced-motion fallback or no scrim/contrast check is an incomplete build — a static check item in step 6, never a screen verdict. (D19 — Motion: the scene's motion is the dealt moment's motion; Theme: theme-matched, colours are the theme's own tokens; Texture: the animated ground is the page's texture layer; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: Vanta + three.js at the pinned pair, destroy on unmount; Colors: effect colours are the theme's own tokens, never invented.)
```

## LIB-06 — ui-ux-pro-max, Vanta background options on app surfaces (VANTA_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `## When to Apply` section
  (after the Anti-generic bar paragraph).
- **Built-tree location:** lines ~96–98 (the Anti-generic bar paragraph; anchor
  is its last sentence).
- **Anchor (count==1, insert AFTER):**

  ```
  **Anti-generic bar (design guidance, not a screen verdict):** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above. Design guidance the brief and Verify record as candidate evidence for `browser-qa` (checked against the recorded named direction): (1) Direction trace — every primary screen should visibly trace to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product is candidate evidence for `browser-qa`. (2) Memorable anchor — the primary view should carry the one unmistakable anchor from the captivating bar above; if no anchor can be named, record that as candidate evidence for `browser-qa`. (3) Not a default template — a surface that looks like a default template is candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail.
  ```

- **Collision note:** AB-14 anchors on the *captivating-bar* paragraph's
  "Only `browser-qa`..." sentence ("fails for having nothing memorable");
  this spec anchors on the *Anti-generic bar* paragraph's different sentence
  ("fails any of these"). No collision.
- **Insert (full text):**

```md

**Animated 3D backgrounds — Vanta, on app surfaces (fix #22 §11, VANTA_F22).**
Where an app surface needs an animated 3D background — a hero or a dealt
moment, never a default wash — the approved source is Vanta (`vanta@0.5.24`,
MIT, plus `three@0.134.0` — the README-documented pair; the general three.js
pin in `data/stacks/threejs.csv` does not apply to Vanta scenes). The effect
(WAVES, BIRDS, NET, FOG, CLOUDS, GLOBE, and the other three.js-backed
effects) is chosen through the design package, theme-matched, as a §10
directive (effect name + exact parameters: colour, scale, speed, mouse/touch
controls) recorded in MASTER.md / `docs/design-tokens.md` with its fix #19 D19
reason. Constraints, all binding: theme-matched (effect colours are the
theme's own tokens); a static fallback (the theme's gradient or image ground)
on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable
under `prefers-reduced-motion: reduce` (the finished still shows instead);
never behind text without a scrim and a 4.5:1 contrast check; one Vanta scene
per page by default; destroy the effect on unmount (`effect.destroy()`).
p5.js-backed Vanta effects (e.g. TRUNK) are not covered — no p5 pin,
recorded-gap if a build wants one. The full Vanta rule (shader scenes / hero
backgrounds) lives in `design-taste-frontend` step 2 (VANTA_F22); this skill
states the app-surface use. A Vanta background with no reduced-motion fallback
or no scrim/contrast check is an incomplete build — a static check item in
step 6, never a screen verdict. Theme-match precondition: a Vanta scene is
applied only when it matches the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the scene's motion is the dealt moment's motion; Theme:
theme-matched, colours are the theme's own tokens; Texture: the animated
ground is the surface's texture layer; Visuals: the scene is the hero anchor,
never behind unreadable text; Techniques: Vanta + three.js at the pinned pair,
destroy on unmount; Colors: effect colours are the theme's own tokens.)
```

## LIB-07 — motion-patterns, React Bits (React/Next only) (REACTBITS_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples` section,
  after the last example (Accordion), before the End-to-End Example.
- **Built-tree location:** line 353 (`## End-to-End Example` heading).
- **Anchor (count==1, insert BEFORE):**

  ```
  ## End-to-End Example
  ```

- **Insert (full text):**

```md
### React Bits — animated components, React/Next only (fix #22 §11, REACTBITS_F22)

React Bits is a copy-paste library of animated React components and
backgrounds (text effects, backgrounds, components) — the bits are source
files copied into the project, not a runtime package: add one bit with the
shadcn CLI (`npx shadcn@latest add @react-bits/<BitName>-TS-TW` for the
TypeScript + Tailwind flavour, `-JS-TW` / `-TS-CSS` / `-JS-CSS` as the build
needs) or the jsrepo CLI (`npx jsrepo add
github/DavidHDev/react-bits/<ComponentName>`), at the pinned repo commit
`9d9c687dc4f55b23539aa5417b703078047efa74` (2026-11-10; MIT + Commons Clause
— free for personal and commercial use inside an app or product; the
components themselves may not be sold, sublicensed, or redistributed as a
library). Each bit is used as a §10 directive (component/effect name + exact
props, as listed for that bit on reactbits.dev — the directive records the
prop values, it never says "a split-text effect") with its fix #19 D19 reason,
recorded in `docs/design-tokens.md`. SCOPE — React/Next.js builds ONLY: this
skill is React-scoped and React Bits is React-only. On a non-React stack the
PATTERN is implemented with the stack's own tools (recorded-gap style: name
the closest equivalent — a CSS / GSAP / vanilla implementation of the same
effect — never force React Bits outside React). Some bits need optional peer
dependencies (GSAP, three.js) — those resolve through the already-pinned
`gsap@3.15.1` / `three@0.134.0` (Vanta pair) pins where the bit needs them,
never a new floating install. Bits that animate text or backgrounds respect
`prefers-reduced-motion: reduce` (static final state) — a bit with no
reduced-motion handling is not used. React Bits is a menu, never a default: a
bit is used only when the dealt theme calls for that exact effect.
Theme-match precondition: every bit must still match the dealt theme; a clash
is not applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the bit's animation is the motion decision, with exact props as
the values; Theme: the bit is theme-matched or not used; Texture: none — a bit
adds motion, not a surface treatment (background bits excepted: those ARE the
surface's texture, theme-matched); Visuals: the bit's effect is visible and
anchored, never decoration that obscures content; Techniques: copy-paste
source at the pinned commit, CLI install, peer deps through existing pins;
Colors: none — the bit's colours are the theme's own tokens.)
```

## LIB-08 — ui-ux-pro-max, React Bits scope pointer (REACTBITS_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 3: Supplement with
  Detailed Searches` (after the domain table, at the auto-detection note).
- **Built-tree location:** line ~196 (the "Domain is auto-detected" paragraph).
- **Anchor (count==1, insert AFTER):**

  ```
  Domain is auto-detected from the query if `--domain` is omitted — but auto-detection can misroute overlapping terms (e.g. "font" matches both `typography` and `google-fonts`). If results look off-topic, pass `--domain` explicitly.
  ```

- **Insert (full text):**

```md

**React Bits — React/Next only (fix #22 §11, REACTBITS_F22).** Animated React
components and backgrounds (text effects, backgrounds, components) from React
Bits are an approved menu item on React/Next.js builds only: copy-paste
source at the pinned repo commit
`9d9c687dc4f55b23539aa5417b703078047efa74` (MIT + Commons Clause — free inside
an app or product; the components themselves may not be sold, sublicensed, or
redistributed). Each bit is used as a §10 directive (component name + exact
props) with its fix #19 D19 reason. On any non-React stack the pattern is
re-implemented with the stack's own tools — never force React Bits outside
React. The primary home is `motion-patterns` (REACTBITS_F22); this skill
states the scope, it does not restate the install. Theme-match precondition: a
bit is applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`. (D19 — Motion: the bit's
animation is the motion decision; Theme: theme-matched or not used; Texture:
none — a bit adds motion, not a surface treatment (background bits excepted);
Visuals: the effect never obscures content; Techniques: copy-paste source at
the pinned commit; Colors: none — the bit's colours are the theme's own
tokens.)
```

---

## Integrator checklist (after applying)

1. Rebuild (`bash build.sh`, exit 0) and confirm the built tree contains every
   anchor token: LENIS_F22 in `skills/motion-foundations/SKILL.md`,
   `skills/motion-patterns/SKILL.md`, `skills/ui-ux-pro-max/SKILL.md`;
   GSAP_F22 + SCROLLTRIGGER_F22 in `skills/ui-ux-pro-max/SKILL.md` and
   SCROLLTRIGGER_F22 in `skills/motion-patterns/SKILL.md`; VANTA_F22 in
   `skills/design-taste-frontend/SKILL.md` (staged edit — verify it survives
   the rebuild) and in `skills/ui-ux-pro-max/SKILL.md`; REACTBITS_F22 in
   `skills/motion-patterns/SKILL.md` and `skills/ui-ux-pro-max/SKILL.md`.
   Each token occurs exactly as specified (LIB-03 carries all four tokens in
   one paragraph; LIB-04 carries GSAP_F22 + SCROLLTRIGGER_F22).
2. Confirm counts: no new skill, no new command, no new trigger key from this
   patch spec (rules and pointers only).
3. Confirm the staged Taste edit (LIB-05, line 126) survives the rebuild
   unchanged, and that the wave-1 texts in that file (TRENDS_F22,
   DIRECTIVES_F22, MOBBIN_PATTERN_F22) are untouched.
4. Confirm banned terms are 0 in the built tree (case-insensitive) after the
   rebuild.
5. Confirm the fix #19/#20/#21 font rules, the screen-verdicts rule, and the
   model pins are untouched by this spec (no entry touches them).
6. Confirm the AB-03 conflict flags are still carried unresolved (LIB-02 /
   LIB-04 cite them, they do not resolve them).
7. Verify22.py additions (for the coordinator): each library named in its
   target skills with pinned version + verified licence + stack scope; the
   GSAP `--domain gsap` integration intact (SKILL.md:164, :191; motion.csv
   rows 1–17); ScrollTrigger referenced in skill prose; the Lenis smooth-scroll
   rule exists; Vanta's reduced-motion + mobile-fallback + scrim constraints
   stated; React Bits' React-only scope stated.
