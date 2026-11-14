# Fix #22 §15 patch specs — 4 more libraries from the cindie.zhu reel

**Status:** patch specs for the coordinator + report. Do NOT edit `build.sh`
from this file alone — apply each build.sh-embedded spec as a patch in the
existing build.sh fix22 patch block (same convention as `fix22/fix22.py`,
which the coordinator extends), apply the staged-source specs directly to
their staged files (same convention as `fix22/libraries-patches.md` LIB-05),
and apply the less-flat-ui spec to its source file (see L15-06 edit point).
Do NOT edit `hackathon-ecc/` directly. Do NOT run `bash build.sh` as part
of applying (the coordinator rebuilds once). Do NOT run `fix11/fix11-stage.py`.
Do NOT edit `fix22.py` or `verify22.py` from this file.

**Patch format:** 5-tuples `(id, file, anchor, new_text, mode)` with mode
`before` / `after` / `replace`, exactly as tasked. NOTE — format
discrepancy, flagged for the coordinator: `fix22/fix22.py`'s `PATCHES` list
is actually 6-tuples `(id, rel, old, new, mode, token)`, the 6th element
being an idempotency token. The token for every patch below is the `_F22`
anchor string named in its `new_text` (listed in the summary table); the
coordinator maps it to the 6th tuple element when extending `fix22.py`.
`new_text` below is the full "Insert (full text)" block of each patch spec.

**Anchor convention (same as ab-patches.md / libraries-patches.md):** every
anchor below was verified to occur EXACTLY ONCE in its target file in the
current built tree / staged source (counts recorded per patch, checked
2026-11-12/13). Apply in fix17 style: assert the anchor count is 1, fail
loudly on mismatch, never guess. Insert AFTER the anchor unless the entry
says BEFORE. Anchors are copied VERBATIM from the target file (including
line wrapping — the built tree wraps long paragraphs; a one-line anchor
that spans a wrap in the file does NOT match).

**Anchor-collision check (2026-11-13):** no anchor below collides with any
anchor in `fix22/ab-patches.md` (AB-01–AB-14), `fix22/process-patches.md`
(P1–P5), or `fix22/libraries-patches.md` (LIB-01–LIB-08). L15-03
deliberately chains on LIB-03: its anchor is the tail of the text LIB-03
inserted, so it MUST run after LIB-03 in `PATCHES` list order (same
chaining pattern as AB-03b on AB-03a in `fix22.py`). L15-02 shares the
`## End-to-End Example` anchor with LIB-07 (`before`); LIB-07 runs first,
so L15-02 lands after the React Bits section, before the heading — the
intended order. L15-05 shares no anchor with LIB-05 (Vanta bullet, staged
line 126); it anchors on the following line instead.

**Anchor tokens for cross-reference / verify22.py:** `R3F_F22` (L15-01,
L15-02, L15-03, L15-05), `LIQGLASS_F22` (L15-03, L15-05, L15-06),
`SHADERGRAD_F22` (L15-03, L15-05), `LIQLOGO_F22` (L15-03, L15-04, L15-07),
`WEBGL_ONE_F22` (L15-03, L15-08). All five tokens were 0 in build.sh and 0
in the built tree before this fix (checked 2026-11-13). Each token occurs
exactly once per file it is placed in (never repeated within a file).

**Pinned versions (all verified live 2026-11-13 — see §2 of the report):**
- R3F: `@react-three/fiber@9.8.2` (React 19) / `@react-three/fiber@8.18.0`
  (React 18), MIT; peer deps `three@0.185.1` (the plugin's general pin) +
  `@types/three@0.185.1`.
- liquid-glass-js: NO npm package — pinned repo commit
  `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; copy `container.js`,
  `button.js`, `glass.css`; page sampling via `html2canvas@1.4.1`.
- ShaderGradient: `@shadergradient/react@2.4.20` (npm latest, ESM-only),
  MIT declared in package.json + README but NO root LICENSE file (caveat);
  install also `three-stdlib@2.36.1` + `camera-controls@3.1.2`.
- liquid-logo: STANDALONE TOOL, not a dependency — pinned repo commit
  `689bb38a1e0d5a6a8baf2d34847635eefde19994`; repo PolyForm Shield 1.0.0,
  underlying `@paper-design/shaders-react` Apache-2.0 (latest 0.0.82; the
  tool itself pins 0.0.21).

**Bundled vs install-on-demand (per library, following the plugin's existing
convention — see report §5):** R3F + ShaderGradient install-on-demand per
project (exact pins in the project's package.json + lockfile); liquid-glass-js
is vendored file copies at the pinned commit (no npm package exists);
liquid-logo is a standalone tool (no install; run the hosted version or the
repo at the pinned commit, output is an asset only).

Banned terms check: none of the new texts below contains any of the seven
banned terms (case-insensitive). The word "AI" does not appear in them.

---

## Summary table

| Patch | File (edit point) | Mode | Anchor (short form) | Token |
|-------|-------------------|------|---------------------|-------|
| L15-01 | `skills/motion-foundations/SKILL.md` (build.sh fix22 block) | after | A11 Solid drawing in 3D block | `R3F_F22` |
| L15-02 | `skills/motion-patterns/SKILL.md` (build.sh fix22 block) | before | `## End-to-End Example` | `R3F_F22` |
| L15-03 | `skills/ui-ux-pro-max/SKILL.md` (build.sh fix22 block) | after | LIB-03 paragraph tail (chained on LIB-03) | `R3F_F22` / `LIQGLASS_F22` / `SHADERGRAD_F22` / `LIQLOGO_F22` / `WEBGL_ONE_F22` |
| L15-04 | `skills/ui-ux-pro-max/SKILL.md` (build.sh fix22 block) | after | B1 app-surfaces paragraph tail sentence | `LIQLOGO_F22` |
| L15-05 | `new-skills/design-taste-frontend/SKILL.md` (STAGED source, direct edit) | before | `- **One object never carries the page.**` line | `R3F_F22` / `LIQGLASS_F22` / `SHADERGRAD_F22` |
| L15-06 | `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (source file, NOT build.sh — see edit point) | before | `### 3. Thermal gradients` | `LIQGLASS_F22` |
| L15-07 | `new-skills/design-taste-frontend/SKILL.md` (STAGED source, direct edit) | after | B1 paragraph tail sentence (staged line 416) | `LIQLOGO_F22` |
| L15-08 | `round2-skills/polish-pass/reference/slop-checklist.md` (STAGED source, direct edit) | after | file tail (accent-hierarchy D19 close) | `WEBGL_ONE_F22` |

---

## L15-01 — motion-foundations, React Three Fiber as the 3D implementation layer (R3F_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, Principles section
  (A11 Solid drawing in 3D — R3F is how that principle is built on React).
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-01/LIB-02).
- **Built-tree location:** the A11 principle block (3 lines).
- **Anchor (count==1, insert AFTER):**

  ```
  - **A11 Solid drawing in 3D** — an object keeps believable volume, weight, and depth
    while it moves. In UI: a card that flips or expands keeps its shadow, edge, and
    layering consistent through the move; it never flattens into a texture or shears.
  ```

- **Insert (full text):**

```md

### React Three Fiber — the 3D implementation layer for React (fix #22 §15, R3F_F22)

React Three Fiber (R3F) is THE 3D implementation layer for React builds:
the §13 depth rules (3D transforms, parallax, camera moves) are implemented
through R3F on React builds. Vanta (§11) stays the vanilla-JS 3D path; R3F
is the React path. R3F is a React renderer for Three.js: JSX elements map
to Three.js objects declaratively (`<mesh />` becomes `new THREE.Mesh()`),
with no overhead (components render outside React). Ecosystem (menu, never
defaults): `@react-three/drei` helpers, Rapier physics, postprocessing, XR.
Install (exact pins, per project, install-on-demand): `npm install
three@0.185.1 @types/three@0.185.1 @react-three/fiber@9.8.2` on React 19,
`@react-three/fiber@8.18.0` on React 18. `three@0.185.1` is the plugin's
general three.js pin (`data/stacks/threejs.csv` row 1) — it satisfies the
R3F peer ranges (v9: `three >=0.156`; v8: `three >=0.133`) and the
ShaderGradient matrix (`three >=0.158.0`); it is NOT the Vanta-scoped
`three@0.134.0`, which governs Vanta scenes only. **Version pairing is
STRICT — check it before installing:** read the project's `package.json`
`react` version first, then install the matching R3F major. React 18 +
R3F v9 FAILS the pairing check. React 19 + R3F v8 FAILS the pairing check.
Next.js 15 App Router MUST use R3F v9 + React 19 (R3F v8 is structurally
incompatible with the App Router's vendored React 19). Directed per §10
(library + effect + exact parameters): a 3D scene is a `<Canvas>` with an
exact camera (`camera={{ position: [0, 0, 5], fov: 45 }}`), exact lights,
and exact motion values (see `motion-patterns`, R3F_F22) — never "a 3D
hero". Under `prefers-reduced-motion: reduce` the scene does not run — a
static image/poster of the finished scene shows instead. One WebGL-heavy
effect per surface (WEBGL_ONE_F22, see the `polish-pass` slop checklist):
an R3F scene counts as the surface's one effect. Theme-match
precondition: a 3D scene is applied only when it matches the dealt theme;
a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: R3F is how 3D motion (rotation, parallax, camera moves) is
implemented on React builds, with exact camera and motion values; Theme:
the scene is the dealt theme's depth, never a stock 3D demo; Texture:
none — R3F adds geometry and light, not a surface treatment (a glass or
gradient ground inside the scene is that library's own treatment);
Visuals: the scene is the hero's depth anchor, never behind unreadable
text (4.5:1 scrim/contrast check where text overlaps it); Techniques: R3F
at the paired pin, peer deps pinned with it, install-on-demand per
project; Colors: none — the scene's colours are the theme's own tokens.)
```

## L15-02 — motion-patterns, 3D scene example (React Three Fiber) (R3F_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples`
  section, after the last example (React Bits, LIB-07), before the
  End-to-End Example.
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-02/LIB-07).
- **Built-tree location:** `## End-to-End Example` heading.
- **Anchor (count==1, insert BEFORE):**

  ```
  ## End-to-End Example
  ```

- **Insert (full text):**

```md
### 3D scene — React Three Fiber (fix #22 §15, R3F_F22)

A 3D scene on a React/Next.js build is built with React Three Fiber
(`@react-three/fiber` — see `motion-foundations`, R3F_F22, for the strict
version pairing: React 18 + R3F v9 FAILS the pairing check, React 19 +
R3F v8 FAILS the pairing check). The scene below is the pattern: a
`<Canvas>` with an exact camera and lights, a mesh whose rotation is
driven per frame. 3D motion values (rotation speed, camera position,
parallax distance) are §10 directives — exact numbers in the directive,
never prose. SCOPE — React/Next.js builds ONLY: on a non-React stack the
same depth is built with the stack's own tools or with Vanta (§11, the
vanilla-JS 3D path) — never force R3F outside React.

```tsx
"use client"
import { Canvas, useFrame } from "@react-three/fiber"
import { useRef } from "react"

// R3F_F22: the 3D scene pattern. Camera, lights, and motion values are
// exact (directed per §10); the mesh rotates 0.01 radians per frame.
function SpinningBox() {
  const ref = useRef()
  useFrame((state, delta) => (ref.current.rotation.y += delta * 0.6))
  return (
    <mesh ref={ref}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#ff5005" />
    </mesh>
  )
}

<Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
  <ambientLight intensity={Math.PI / 2} />
  <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
  <SpinningBox />
</Canvas>
```

**Parallax through the camera (fix #22 §13 depth).** Depth motion is a
camera move, not a layout shift: the camera's position (or a group's
position) moves with scroll or pointer, with exact distances in the
directive (e.g. `camera.position.z` from 5 to 3.5 across the scroll).
Under `prefers-reduced-motion: reduce` the Canvas does not mount — a
static image/poster of the finished scene renders in its place. An R3F
scene is the surface's one WebGL-heavy effect (WEBGL_ONE_F22) — it never
shares a surface with a Vanta scene, a ShaderGradient, liquid glass, or
liquid metal. Theme-match precondition: the scene must still match the
dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the per-frame rotation and the camera move are the 3D
motion values, exact in the directive; Theme: the scene is the dealt
theme's depth moment, never a stock spinning cube; Texture: none — the
scene adds geometry and light, not a surface treatment; Visuals: the
object stays visible and legible through the move (A11 solid drawing in
3D); Techniques: R3F at the paired pin, Canvas + useFrame, install-on-demand
per project; Colors: none — the scene's colours are the theme's own
tokens.)

```

## L15-03 — ui-ux-pro-max, §15 libraries stack scope + one-WebGL rule (R3F_F22 / LIQGLASS_F22 / SHADERGRAD_F22 / LIQLOGO_F22 / WEBGL_ONE_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 4: Stack
  Guidelines`, immediately after the §11 libraries scope paragraph
  (LIB-03).
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-03/LIB-04/LIB-06/LIB-08).
- **Built-tree location:** lines 375–396 (the LIB-03 paragraph; anchor is
  its 3-line tail). CHAINED anchor: this patch MUST run after LIB-03 in
  `PATCHES` list order (same chaining pattern as AB-03b on AB-03a).
- **Anchor (count==1, insert AFTER):**

  ```
  library effect is applied only when it matches the dealt theme; a clash is not
  applied, with the reason recorded in `docs/design-tokens.md`.
  ```

- **Insert (full text):**

```md

**§15 design asset libraries — stack scope (fix #22 §15, R3F_F22 /
LIQGLASS_F22 / SHADERGRAD_F22 / LIQLOGO_F22).** Four more free libraries
are approved menu items, never defaults — each is chosen through the
skills, theme-matched, with a D19 reason, and directed per §10 (library +
effect name + exact parameters). Stack scope: **react-three-fiber**
(`@react-three/fiber@9.8.2` on React 19, `@react-three/fiber@8.18.0` on
React 18, MIT; peer deps `three@0.185.1` + `@types/three@0.185.1`) and
**ShaderGradient** (`@shadergradient/react@2.4.20`, ESM-only; MIT declared
in package.json + README but NO root LICENSE file — see the caveat below)
are React/Next.js ONLY — on any other stack the pattern is re-implemented
with the stack's own tools (see `motion-patterns`, R3F_F22 /
SHADERGRAD_F22). **liquid-glass-js** (repo commit
`78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package — copy
`container.js`, `button.js`, `glass.css` into the project) is vanilla JS
and available on every stack. **liquid-logo** (repo commit
`689bb38a1e0d5a6a8baf2d34847635eefde19994`; PolyForm Shield 1.0.0, not MIT)
is a STANDALONE TOOL, not a runtime dependency — it produces the animated
brand mark once (see `design-taste-frontend` step 4a, LIQLOGO_F22); it is
never installed as a project dependency. **One WebGL-heavy effect per
surface (WEBGL_ONE_F22):** a surface/page uses AT MOST ONE WebGL-heavy
library effect (an R3F scene, a Vanta scene, a ShaderGradient, liquid
glass, liquid metal). Stacking two or more WebGL-heavy effects on one
surface FAILS the `polish-pass` flag (see the slop checklist,
WEBGL_ONE_F22) — performance + "more, not bolder" restraint. Every library
effect respects `prefers-reduced-motion: reduce` (static fallback or off)
— no library exempts the rule. Unpinned versions ("latest") FAIL the pin
check. The pinned versions live here and in the owning skills; a build
that needs a newer version re-pins deliberately and records the new pin +
its verification, never floats. Theme-match precondition: a library effect
is applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the libraries are the 3D / gradient / glass / brand-motion
mechanisms, chosen per build; Theme: every effect is theme-matched or not
applied; Texture: ShaderGradient grounds and liquid glass ARE texture /
surface treatments chosen through the theme; Visuals: scope keeps effects
on the surfaces where they read (3D scenes on React heroes, glass on rich
backgrounds, gradients on landing heroes); Techniques: exact pins + stack
scope, install-on-demand per project (liquid-glass-js vendored file
copies, liquid-logo a standalone tool — see `fix22/libraries15-report.md`
§5 in the manifest record); Colors: none — the libraries choose no
colours (ShaderGradient colours come from the customize URL, which is the
theme's own palette).)

**ShaderGradient licence caveat (fix #22 §15, SHADERGRAD_F22).** The
ShaderGradient repo has NO root LICENSE file (verified live: no `LICENSE`
in the repo root, no licence field on the repo page). The MIT grant rests
on two declarations only: the README ("MIT © ruucm, stone-skipper") and
the `@shadergradient/react` package.json (`"license": "MIT"`). That is a
recorded caveat, not an assumed-away fact: if a build's legal review
needs actual licence text, the grant must be confirmed with the
maintainer before shipping — the plugin records the caveat and proceeds
on the declared MIT. Install `@shadergradient/react` (v2), NOT legacy
`shadergradient` (v1.3.5, dead end): a build installing legacy
`shadergradient` v1 FAILS the version check. The Figma plugin's paid Pro
tier is out of scope — the npm library is the integration, and it is free.
```

## L15-04 — ui-ux-pro-max, liquid-logo brand-asset pointer (LIQLOGO_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, app-surfaces brand identity
  paragraph (fix #20 B1, app surfaces).
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill).
- **Built-tree location:** line 215 (the B1 app-surfaces paragraph; anchor
  is its closing sentence).
- **Anchor (count==1, insert AFTER):**

  ```
  A build with no recorded brand identity is an incomplete build. The full B1 rule lives in `design-taste-frontend` step 4a.
  ```

- **Insert (full text):**

```md

**Animated brand mark — liquid-logo, standalone tool (fix #22 §15,
LIQLOGO_F22).** Where a build wants its wordmark animated as liquid
metal, the approved production method is liquid-logo
(paper-design/liquid-logo, repo commit
`689bb38a1e0d5a6a8baf2d34847635eefde19994`; PolyForm Shield 1.0.0 — the
animated mark is a brand asset produced ONCE with the tool or its hosted
version at liquid.paper.design, exported as MP4/PNG, and shipped as an
asset; it is never a runtime dependency and never the only logo — the
original static logo is kept as the fallback for old phones and
non-WebGL contexts. The full rule (input requirements, the honest input
check, attribution) lives in `design-taste-frontend` step 4a (fix #20 B1,
LIQLOGO_F22); this skill states the app-surface use. Theme-match
precondition: the animated mark is the build's own brand, produced once
from its own wordmark — a liquid-metal treatment that clashes with the
dealt theme is not used, with the reason recorded in
`docs/design-tokens.md`. (D19 — Motion: the animation is the brand
motion, produced once, never runtime-heavy; Theme: the mark is the
build's own brand, theme-matched; Texture: none — the mark is an asset,
not a surface treatment; Visuals: the animated mark is the brand anchor,
the static logo is the fallback where it cannot play; Techniques:
standalone tool at the pinned commit, asset output only; Colors: none —
the metal is the shader's own chrome, the brand's colours are unchanged.)
```

## L15-05 — design-taste-frontend, §15 libraries on landing pages (SHADERGRAD_F22 / R3F_F22 / LIQGLASS_F22) — STAGED EDIT

- **Target (staged source):** `new-skills/design-taste-frontend/SKILL.md`,
  section 2 (Tech bullet area, after the Vanta bullet at staged line 126).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  LIB-05). The staged file is the source of truth for this skill; build.sh
  installs it — do NOT also patch it through the build.sh fix22 block.
- **Staged location:** insert BEFORE the `- **One object never carries the
  page.**` line (staged line 127).
- **Anchor (count==1, insert BEFORE):**

  ```
  - **One object never carries the page.** The product or hero object whole leads the hero and **two more sections at
  ```

  (Anchor is the first line of that bullet as wrapped in the staged file;
  the insert goes before the whole bullet.)

- **Insert (full text):**

```md
- **Animated 3D gradients come from ShaderGradient (fix #22 §15, SHADERGRAD_F22).** Where the deal calls for the one effect as an animated gradient ground — full-bleed hero, login, or waitlist backgrounds where CSS gradients feel flat — the approved source is ShaderGradient (`@shadergradient/react@2.4.20`, ESM-only; MIT declared in package.json + README but NO root LICENSE file — see the caveat in `ui-ux-pro-max`, SHADERGRAD_F22; React/Next.js ONLY — non-React builds use Vanta or CSS gradients, the same routing rule as React Bits §11). Install: `npm i @shadergradient/react@2.4.20 @react-three/fiber@9.8.2` (React 19) or `@react-three/fiber@8.18.0` (React 18) `three@0.185.1 three-stdlib@2.36.1 camera-controls@3.1.2` (and `@types/three@0.185.1` for TypeScript). Configure by URL, not by hand: design at shadergradient.co/customize, copy the URL — the URL IS the config — and carry it in the §10 directive as `control='query'` + the full `urlString` + the preset name. The 10 presets are the menu (halo, pensive, mint, interstella, nightyNight, violaOrientalis, universe, sunset, mandarin, cottonCandy), never defaults — the preset is theme-matched. Mesh types: `plane` / `sphere` / `waterPlane` (waterPlane at low `uSpeed` for ambient motion behind glassmorphism cards). Constraints, all binding: theme-matched (the URL's colours are the theme's own palette); a static gradient fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; the gradient is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). Install `@shadergradient/react` (v2), NOT legacy `shadergradient` (v1.3.5): a build installing legacy `shadergradient` v1 FAILS the version check. (D19 — Motion: the gradient's ambient motion is the dealt moment's motion; Theme: theme-matched, colours are the theme's own palette from the URL; Texture: the animated ground is the page's texture layer; Visuals: the gradient is the hero's visual anchor, never behind unreadable text; Techniques: `@shadergradient/react` at the pinned version, URL-as-config, install-on-demand per project; Colors: the gradient colours ARE the theme's palette, carried in the URL, never invented.)
- **3D hero and dealt moments on React come from React Three Fiber (fix #22 §15, R3F_F22).** Where the deal calls for the one effect or a dealt moment as a real 3D scene on a React build — a hero object, a camera-through-world moment — the approved implementation is R3F (`@react-three/fiber@9.8.2` on React 19, `@react-three/fiber@8.18.0` on React 18, MIT; peer deps `three@0.185.1` + `@types/three@0.185.1`; see `motion-foundations`, R3F_F22, for the strict pairing rule — React 18 + R3F v9 FAILS the pairing check). The §13 depth rules (3D transforms, parallax, camera moves) run through R3F on React builds; Vanta stays the vanilla-JS 3D path. The scene is directed per §10 (effect + exact camera, lights, and motion values) and recorded in `docs/design-tokens.md` with its fix #19 D19 reason. Constraints, all binding: theme-matched; a static image/poster fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check; the scene is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). (D19 — Motion: the scene's motion is the dealt moment's motion; Theme: theme-matched, the scene is the theme's own depth; Texture: none — the scene adds geometry and light, not a surface treatment; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: R3F at the paired pin, install-on-demand per project; Colors: the scene's colours are the theme's own tokens.)
- **Liquid glass hero and nav moments come from liquid-glass-js (fix #22 §15, LIQGLASS_F22).** Where the deal calls for a glass hero panel, a glass nav bar, or a floating glass card — glass as a dealt moment, never a default wash — the approved implementation is liquid-glass-js (dashersw/liquid-glass-js, repo commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package — copy `container.js`, `button.js`, `glass.css` into the project; vanilla JS, no build step). The glass is directed per §10 (class + exact parameters: `type` `'rounded'` / `'circle'` / `'pill'`, `borderRadius`, `tintOpacity`, `blurRadius` — see `less-flat-ui`, LIQGLASS_F22, for the directed values). Cross-reference, do not duplicate: Group E trend "Liquid Glass" (E15) is the MENU item; this library is the IMPLEMENTATION — the trend entry is never restated here and this rule never restates the trend. Constraints, all binding: theme-matched (the glass must be the theme's own material, never a generic backdrop-blur wash — Refract explicitly bans frosted glass and is NOT a fit); a frosted-blur fallback (less-flat-ui #2 fluted glass) on mobile/low-power and whenever WebGL is unavailable; the glass MUST disable under `prefers-reduced-motion: reduce` (the frosted fallback shows instead); text over glass keeps 4.5:1 contrast; the glass is the surface's one WebGL-heavy effect (WEBGL_ONE_F22). (D19 — Motion: none — the glass does not move (its refraction is light, not motion); Theme: the glass is the theme's own material; Texture: the glass IS the surface's texture layer; Visuals: the glass panel is the hero/nav anchor, never behind unreadable text; Techniques: vendored file copies at the pinned commit, no npm package; Colors: the glass tint is the theme's own tint, never a new colour.)
```

## L15-06 — less-flat-ui, liquid glass as a surface treatment (LIQGLASS_F22)

- **Target:** `~/workspace/cursor-skills/less-flat-ui/SKILL.md`, after
  the Fluted glass treatment (#2), as a NOTE — not a numbered treatment.
  The 23-treatment catalogue stays 23; this is implementation guidance
  for a texture the catalogue already names, not a 24th treatment.
- **Edit point:** the less-flat-ui SOURCE file itself. build.sh:263
  copies this file into the plugin (`cp -r
  "$HOME/workspace/cursor-skills/less-flat-ui"
  "$PLUGIN_DIR/skills/less-flat-ui"`), so there is no build.sh-embedded
  copy to patch — the fix22 block cannot reach it. HAZARD, flagged for
  the coordinator: this source file is the SHARED global Cursor skill
  (also used outside the plugin); editing it changes the global skill
  too. The alternative — patching the built copy in the fix22 block like
  the Batch E fix #4 patches (build.sh:20972+) — would make the built
  text diverge from the shared source on every rebuild; the coordinator
  decides which edit point wins and records it. The patch below is
  written for the source file.
- **Built-tree note:** the built copy is byte-identical to this source
  (build.sh:20979), so the anchor below occurs exactly once in both.
- **Anchor (count==1, insert BEFORE):**

  ```
  ### 3. Thermal gradients
  ```

- **Insert (full text):**

```md
**Liquid glass — real refraction (fix #22 §15, LIQGLASS_F22).** Fluted
glass (#2 above) is a frosted-blur approximation. Where a build needs
REAL refraction — Apple-style liquid glass with edge highlights, blur,
and masking through WebGL 2.0 shaders, not just `backdrop-filter` blur —
the approved implementation is liquid-glass-js (dashersw/liquid-glass-js,
repo commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`, MIT; NO npm package
— copy `container.js`, `button.js`, `glass.css` into the project; vanilla
JS, all stacks, no build step). Use for nav bars, floating cards, modals,
and CTA buttons over rich backgrounds. Directed per §10 (class + exact
parameters, from the library's own API): `new Container({ type: 'pill',
borderRadius: 24, tintOpacity: 0.3 })` for a nav pill, `new Button({
text: '<label>', size: 28, type: 'pill', tintOpacity: 0.4, warp: true,
onClick: <handler> })` for a glass CTA; global glass parameters via
`window.glassControls` (`edgeIntensity: 0.02, rimIntensity: 0.08,
blurRadius: 7.0, tintOpacity: 0.3` — the directed defaults, do not tune
per component). Shape types: `'rounded'` / `'circle'` / `'pill'`
(defaults: `borderRadius: 48`, `tintOpacity: 0.2`, `size: 48` for Button).
Performance note (from the README): the library samples the page with
html2canvas (`html2canvas@1.4.1`) — that sampling is the cost; keep glass
to one surface per screen by default and never stack it with another
WebGL-heavy effect (one WebGL-heavy effect per surface, WEBGL_ONE_F22 —
see the `polish-pass` slop checklist). Fallback: under
`prefers-reduced-motion: reduce`, on mobile/low-power, or whenever WebGL
is unavailable, the glass renders as frosted blur — treatment #2 fluted
glass above — never as a missing element. Text over glass keeps 4.5:1
contrast. Cross-reference, do not duplicate: Group E trend "Liquid Glass"
(E15, in `design-taste-frontend`) is the MENU item; this library is the
IMPLEMENTATION. Record the treatment per surface in
`docs/design-tokens.md` like every other treatment, with its six fix #19
D19 dimension lines.

(D19 — Motion: none — the glass does not move (its refraction is light,
not motion); Theme: the glass is the theme's own material, never a generic
blur wash; Texture: the glass IS the surface's texture layer (real
refraction, not a flat treatment); Visuals: the glass panel stays legible
— 4.5:1 over it, content above it; Techniques: vendored file copies at
the pinned commit, html2canvas@1.4.1 for page sampling, no npm package;
Colors: the glass tint is the theme's own tint, never a new colour.)
```

## L15-07 — design-taste-frontend, liquid-logo as the B1 brand asset (LIQLOGO_F22) — STAGED EDIT

- **Target (staged source):** `new-skills/design-taste-frontend/SKILL.md`,
  step 4a brand identity (fix #20 B1 paragraph, staged line 416).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  LIB-05). Do NOT also patch it through the build.sh fix22 block.
- **Staged location:** staged line 416 (the B1 paragraph; anchor is its
  closing sentence).
- **Anchor (count==1, insert AFTER):**

  ```
  when it does not, the build deals one and records it.
  ```

  (Full sentence: "When a project already has a brand (a real product, a
  real wordmark), the record names it and the build conforms to it; when
  it does not, the build deals one and records it." — the anchor above is
  the sentence's tail, verified count==1 in the staged file.)

- **Insert (full text):**

```md
- **Animated brand mark — liquid-logo, a standalone tool (fix #22 §15, LIQLOGO_F22).** liquid-logo is a STANDALONE TOOL, not a library to import and not a runtime dependency: run it (or its hosted version at liquid.paper.design) to produce the animated brand mark ONCE — export MP4/PNG, or port the shader idea into a small R3F shader — and ship the output as an asset. Pin: repo commit `689bb38a1e0d5a6a8baf2d34847635eefde19994` (paper-design/liquid-logo, `package.json` version 0.1.0, `private: true` — there is no published package to install). Licences, both recorded: the liquid-logo repo itself is under the PolyForm Shield Licence 1.0.0 (NOT MIT — it carries a noncompete clause: do not use the tool to provide a competing product); the effect is built on `@paper-design/shaders-react` (Apache 2.0, latest 0.0.82 — the tool itself pins 0.0.21 in its own `package.json`). The animated logo is a brand asset, generated once — never runtime-heavy, never the only logo: the original static logo is kept as the fallback for old phones and non-WebGL contexts, and a build using the animated logo with no static fallback FAILS the check. Retain paper-design attribution in a code comment where the asset is used. Input requirements (honest check first): the input must be a transparent PNG/SVG with high contrast, solid shapes, no gradients or drop shadows, and no thin details. Before producing it, ask and answer honestly: "tell me honestly whether the logo will work with this shader" — if the logo has thin details, gradients, or low contrast, the answer is no and the static logo ships alone; do not force the effect onto an unsuitable mark. (D19 — Motion: the animation is the brand motion, produced once, never runtime-heavy; Theme: the mark is the build's own brand, theme-matched; Texture: none — the mark is an asset, not a surface treatment; Visuals: the animated mark is the brand anchor, the static logo is the fallback where it cannot play; Techniques: standalone tool at the pinned commit, MP4/PNG asset output, attribution comment retained; Colors: none — the metal is the shader's own chrome, the brand's colours are unchanged.)
```

## L15-08 — polish-pass slop checklist, one-WebGL-heavy-effect-per-surface flag (WEBGL_ONE_F22) — STAGED EDIT

- **Target (staged source):**
  `round2-skills/polish-pass/reference/slop-checklist.md`, appended after
  the Accent hierarchy section (the file's current end).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  the slop-checklist / unslop-fixes staged files). Do NOT patch through
  the build.sh fix22 block.
- **Staged location:** end of file (484 lines).
- **Anchor (count==1, insert AFTER):**

  ```
  decision record; Colors: color (H1) is one accentuation means, used for
    action/emphasis only.
  ```

  (The closing lines of the Accent hierarchy D19 block, verified
  count==1 in the staged file.)

- **Insert (full text):**

```md

## One WebGL-heavy effect per surface — WEBGL_ONE_F22 (fix #22 §15)

- **What counts as a flag:** a surface (or page) carrying TWO OR MORE
  WebGL-heavy library effects at once — any two of: an R3F scene
  (R3F_F22), a Vanta scene (VANTA_F22), a ShaderGradient
  (SHADERGRAD_F22), liquid glass (LIQGLASS_F22), liquid metal
  (LIQLOGO_F22). Stacking them is a performance failure and a
  "more, not bolder" failure: a surface stacking two WebGL-heavy effects
  FAILS this check. One effect plus a non-WebGL treatment (a CSS
  gradient, a less-flat-ui texture, a static image) is not stacking.
- **Justified use:** exactly ONE WebGL-heavy effect on the surface,
  theme-matched, with its static fallback and its reduced-motion handling
  recorded — a surface with one theme-matched WebGL effect + static
  fallback PASSES. There is no clearance for two effects on one surface:
  the fix is to remove all but one, never to record a reason for the
  stack.
- **Clearance:** not applicable — fix, do not clear. (A single effect
  needs no clearance under this check; its own theme-fit + fallback are
  checked under its own rule.)
- **Standing:** a static check producing candidate evidence for
  `browser-qa`, never a verdict — same standing as every check in this
  file (fix #13e screen-verdicts rule).
- **Cross-references, do not duplicate:** the per-library rules own their
  own effect (R3F_F22 in `motion-foundations` / `motion-patterns`,
  VANTA_F22 in `design-taste-frontend` step 2, SHADERGRAD_F22 in
  `design-taste-frontend` step 2, LIQGLASS_F22 in `less-flat-ui`, the
  one-effect deal in `design-taste-frontend` step 2). This check only
  counts effects per surface; it never restates any library's install or
  parameters.
- **D19 —** Motion: the count is what keeps the surface's motion budget
  to one WebGL effect; Theme: the one effect must fit the dealt theme;
  Texture: the one effect is the surface's texture/depth layer — a second
  effect adds no theme value; Visuals: one effect reads as a deliberate
  anchor, two read as clutter; Techniques: count the WebGL contexts and
  effects per surface in the static check; Colors: none — the check counts
  effects, it chooses no colours.
```

---

## Integrator checklist (after applying)

1. Apply L15-01–L15-04 in the build.sh fix22 patch block (extend
   `fix22.py`'s `PATCHES` with the 6th token element — see the format note
   at the top), L15-05 + L15-07 directly to
   `new-skills/design-taste-frontend/SKILL.md`, L15-06 to
   `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (or the built copy
   per the coordinator's edit-point decision — record it), L15-08
   directly to `round2-skills/polish-pass/reference/slop-checklist.md`.
   Rebuild (`bash build.sh`, exit 0) and confirm the built tree contains
   every anchor token exactly once per file: `R3F_F22` in
   `skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`,
   `skills/ui-ux-pro-max/SKILL.md`, `skills/design-taste-frontend/SKILL.md`;
   `LIQGLASS_F22` in `skills/ui-ux-pro-max/SKILL.md`,
   `skills/design-taste-frontend/SKILL.md`, `skills/less-flat-ui/SKILL.md`;
   `SHADERGRAD_F22` in `skills/ui-ux-pro-max/SKILL.md` and
   `skills/design-taste-frontend/SKILL.md`; `LIQLOGO_F22` in
   `skills/ui-ux-pro-max/SKILL.md` and
   `skills/design-taste-frontend/SKILL.md`; `WEBGL_ONE_F22` in
   `skills/ui-ux-pro-max/SKILL.md` and
   `skills/polish-pass/reference/slop-checklist.md`.
2. Confirm counts: no new skill, no new command, no new trigger key from
   this patch spec (rules and pointers only). less-flat-ui stays at 23
   treatments (L15-06 is a note, not a 24th treatment).
3. Confirm the staged Taste edits (L15-05, L15-07) survive the rebuild
   unchanged, and that the wave-1 / §11 texts in that file (TRENDS_F22,
   DIRECTIVES_F22, MOBBIN_PATTERN_F22, VANTA_F22 at staged line 126) are
   untouched. Confirm the staged polish-pass edit (L15-08) survives.
4. Confirm banned terms are 0 in the built tree (case-insensitive) after
   the rebuild.
5. Confirm the fix #19/#20/#21 font rules, the screen-verdicts rule, and
   the model pins are untouched by this spec (no entry touches them).
6. Confirm the `liquid-glass-design` dangling reference is recorded as
   resolved per option (b) in the report §4 — no patch in this spec
   touches build.sh:18731 or the audit20a block.
7. verify22.py additions (for the coordinator): each library named in its
   target skills with pinned version + verified licence + stack scope; the
   R3F React-version pairing rule stated; the ShaderGradient v2 (not v1)
   install stated; the liquid-glass-js no-npm-package file-copy handling
   stated; the liquid-logo standalone-tool handling + static-logo fallback
   + attribution stated; the one-WebGL-effect-per-surface rule stated;
   the `liquid-glass-design` dangling reference resolved (option (b),
   recorded).

---

# Report — fix #22 §15 (4 more libraries)

## 1. Deliverable

`fix22/libraries15-patches.md` (this file): patch specs L15-01–L15-08 +
this report. No plugin file was edited, `build.sh` was not run, `fix22.py`
and `verify22.py` were not edited.

## 2. Live-verified versions + licences (all checked 2026-11-13, do not take the SPEC's expectations as verified)

| Library | Repo | Pinned version | Licence (verified live) | Source of verification |
|---------|------|---------------|------------------------|------------------------|
| react-three-fiber | https://github.com/pmndrs/react-three-fiber | `@react-three/fiber@9.8.2` (React 19) / `@react-three/fiber@8.18.0` (React 18); peer `three@0.185.1` + `@types/three@0.185.1` | **MIT** | GitHub repo page (33,688 stars; "License: MIT License (MIT)"; `LICENSE` in root files; current commit `d74622ea8ed717f7212d7e19d65ff3e325508389`); npm registry `@react-three/fiber/latest` → 9.8.2, `"license":"MIT"`, gitHead `e6ec3506ebf7879c26bd5ac27986b5d4421f3254`, peer `react >=19 <19.4`, `three >=0.156`; `npm view @react-three/fiber@8` → 8.18.0, MIT, peer `react >=18 <19`, `three >=0.133`; README pairing verbatim: "@react-three/fiber@8 pairs with react@18, @react-three/fiber@9 pairs with react@19"; install line `npm install three @types/three @react-three/fiber` verbatim from README. |
| liquid-glass-js | https://github.com/dashersw/liquid-glass-js | **No npm package** — pinned repo commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a` (main HEAD, single commit in repo) | **MIT** | GitHub repo page (1,771 stars; "License: MIT License (MIT)"; `LICENSE` in root files; README "Licensed under the MIT License"); root files confirm `container.js`, `button.js`, `glass.css` exist; README: "Zero Dependencies: Pure JavaScript (except html2canvas for page sampling)", WebGL 2.0, Container/Button option tables verbatim (defaults `borderRadius: 48`, `tintOpacity: 0.2`, Button `size: 48`; `window.glassControls` example `edgeIntensity: 0.02, rimIntensity: 0.08, blurRadius: 7.0, tintOpacity: 0.3`); html2canvas pinned `1.4.1` in the README quick-start script tag; roadmap lists "Bundle for NPM" as future work — confirms no npm package today; no tags, no releases. |
| shadergradient | https://github.com/ruucm/shadergradient | `@shadergradient/react@2.4.20` (npm latest, ESM-only); install also `three-stdlib@2.36.1` + `camera-controls@3.1.2` | **MIT declared, NO root LICENSE file — recorded caveat** (see §6 D1) | GitHub repo page (3,151 stars; root files list has NO `LICENSE`; repo page shows no licence field); README "License: MIT © ruucm, stone-skipper" + npm registry `@shadergradient/react/latest` → 2.4.20, `"license":"MIT"`, `main: ./dist/index.mjs` (ESM-only), peer `react ^18.2.0 \|\| ^19.0.0`; README install + compatibility matrix verbatim (Next 15 App Router MUST use R3F v9 + React 19; `three >=0.158.0`); `control='query'` + `urlString` example verbatim; 10 presets verified from upstream `packages/shadergradient/src/presets.ts` (keys: halo, pensive, mint, interstella, nightyNight, violaOrientalis, universe, sunset, mandarin, cottonCandy); current commit `68bdd740037a11c639f8b91fd775949c71d718d0`. |
| liquid-logo | https://github.com/paper-design/liquid-logo | **Standalone tool, not a dependency** — pinned repo commit `689bb38a1e0d5a6a8baf2d34847635eefde19994` (main HEAD); `package.json` version 0.1.0, `private: true` | **PolyForm Shield 1.0.0** (repo) + **Apache-2.0** (`@paper-design/shaders-react`) — recorded flag (see §6 D2) | GitHub repo page (1,454 stars; "License: Other (NOASSERTION)"; `LICENSE` in root files); `LICENSE` read verbatim — "PolyForm Shield License 1.0.0" incl. the noncompete clause; README links the hosted version liquid.paper.design; `package.json` read verbatim — `"private": true`, `"@paper-design/shaders-react": "0.0.21"`, React 19 / Next 15.2.8 app; npm registry `@paper-design/shaders-react/latest` → 0.0.82, `"license":"Apache-2.0"`. |
| three.js (peer dep) | https://github.com/mrdoob/three.js | `three@0.185.1` (plugin general pin, kept); latest upstream 0.187.0 NOT adopted | **MIT** | `data/stacks/threejs.csv` row 1 (existing pin); `npm view three version` → 0.187.0; `npm view @types/three version` → 0.187.0; `@types/three@0.185.1` verified to exist (`npm view` → 0.185.1). |
| three-stdlib / camera-controls (ShaderGradient peers) | npm | `three-stdlib@2.36.1`, `camera-controls@3.1.2` | **MIT / MIT** | `npm view` version + licence for each. |

## 3. R3F version-pairing rule (verified, not assumed)

- **v8 ↔ React 18, v9 ↔ React 19 — strict.** Sources: R3F README
  warning verbatim; v9.8.2 peer `react >=19 <19.4`; v8.18.0 peer `react
  >=18 <19`; ShaderGradient README compatibility matrix (Next 15 App
  Router MUST use R3F v9 + React 19).
- **Version check (stated in L15-01/L15-02/L15-05):** read the project's
  `package.json` `react` version FIRST, then install the matching R3F
  major. React 18 + R3F v9 FAILS the pairing check. React 19 + R3F v8
  FAILS the pairing check.
- **three pin for R3F scenes:** `three@0.185.1` (the plugin's general
  pin) satisfies v9 peer `>=0.156`, v8 peer `>=0.133`, and the
  ShaderGradient matrix `>=0.158.0`. It is deliberately NOT the
  Vanta-scoped `three@0.134.0` (different scope, unchanged) and NOT
  upstream latest 0.187.0 (the general pin stays 0.185.1; a re-pin is a
  separate deliberate decision, never a float).

## 4. Namesake resolutions (verified live)

### liquid-glass-js: dashersw (the reel's repo) vs ozcanyldzhn (namesake)

- **Reel = dashersw/liquid-glass-js.** Evidence: the SPEC records the
  creator's own guide names dashersw (see the caveat below); the
  distinguishing facts are independently verified — dashersw ships
  `Container` + `Button` classes, three shape types (rounded/circle/pill),
  WebGL 2.0 shaders, zero deps except html2canvas, and NO npm package
  (roadmap: "Bundle for NPM"); ozcanyldzhn/liquid-glass.js is a DIFFERENT
  library — an npm package (`@ozcanyldzhn/liquid-glass-js`) of
  framework-agnostic web components using SVG displacement mapping, 6
  stars, created 2026-08-19, MIT. The two must never be confused: a build
  installing `@ozcanyldzhn/liquid-glass-js` is NOT using liquid-glass-js
  as woven here, and the patch texts name the dashersw repo + the file
  copies explicitly so the wrong install cannot be mistaken for the right
  one.
- **Caveat (not independently re-verified):** the creator's guide URL
  (`cindiezhu.com.au/guides/4-github-design-repos`) failed to resolve in
  this session (`browser.open` source-fetch failure; not retried per the
  runtime instruction). The "guide names dashersw" claim therefore rests
  on the SPEC (parent-verified), not on a fresh fetch. The resolution
  does not depend on it: the API/file-copy facts above distinguish the
  two repos on their own. Coordinator may re-check the guide URL if it
  matters for the manifest.

### liquid-logo: paper-design (the reel's repo) vs collidingScopes (same name)

- **Reel = paper-design/liquid-logo.** Evidence: the SPEC records the
  creator's own guide names paper-design; independently verified
  distinguishing facts — paper-design is the hosted tool at
  liquid.paper.design (linked from its own README), built on
  `@paper-design/shaders-react`, PolyForm Shield licensed; collidingScopes/
  liquid-logo is a separate standalone browser tool (MIT, 307 stars,
  PNG/MP4 export, own GLSL shaders), NOT built on Paper Shaders.
- **SPEC wording flag (for the parent):** the SPEC calls collidingScopes
  the "earlier same-named repo". Creation dates verified live say the
  opposite: paper-design was created 2025-02-18, collidingScopes
  2025-03-03 — paper-design predates collidingScopes by 13 days. The
  resolution (reel = paper-design) is unchanged — only the word
  "earlier" is wrong, or meant something other than creation date. The
  coordinator should correct the wording in the manifest, not the
  resolution.

## 5. The `liquid-glass-design` dangling reference — resolved as option (b): corrected, not a gap-fill

Re-verified from scratch (2026-11-13):

- **Coverage re-check (word-boundary greps over build.sh):**
  `react-three-fiber` / `three-fiber` 0; `shadergradient` /
  `shader gradient` / `shader-gradient` 0; `liquid-logo` / `liquid logo`
  0; `liquid-glass` 4 hits — all the string `liquid-glass-design`, at
  build.sh:18731, 19412, 19449, 19458 (same lines as the parent baseline).
- **Built-tree check:** `grep -rn 'liquid-glass-design'
  hackathon-ecc/skills/` = **0 hits**. No skill text anywhere in the
  built tree references `liquid-glass-design`. (The string "liquid glass"
  does appear in built skill text — Taste E15 trend entry, ui-ux-pro-max
  data files — but never as the skill name `liquid-glass-design`.)
- **What the 4 build.sh hits are:**
  - build.sh:18731 — the `pi-core.json` upstream include list: a
    governance list of expected-unshipped skills (asserted:
    `set(_removed) == _expected_unshipped`). `liquid-glass-design` sits
    there alongside `swiftui-patterns` and other never-shipped ECC
    skills. This is NOT plugin rule text and must NOT be edited —
    changing it would break the assert.
  - build.sh:19412, 19449, 19458 — the audit20a fix block: the comment
    (19412) records that `accessibility` + `frontend-slides` "Related
    Skills" lists named `liquid-glass-design` (and `swiftui-patterns`),
    "neither of which exists", and the Fix 2a/2b patches (19449, 19458)
    DELETED those dangling entries/lines. The correction already
    happened; the remaining hits are the fix's own record.
- **Decision — option (b), corrected:** the dangling skill-text
  references were already corrected by the earlier audit fix (Fix 2a/2b
  deletions); the only surviving build.sh hit is the governance list,
  which is expected-unshipped by design. The liquid-glass-js integration
  in this spec is NEW implementation (a real refraction library with
  Container/Button classes), NOT filling the gap the dangling reference
  pointed at — the reference pointed at a nonexistent skill, not at an
  implementation gap, and no skill named `liquid-glass-design` is created
  or restored by this fix. No patch in this spec touches build.sh:18731
  or the audit20a block.

## 6. Bundled vs install-on-demand (per library)

Existing convention followed (same as `fix22/libraries-report.md` §4:
plugin-script deps are exact-pinned in the repo-root `package.json` +
`package-lock.json` and installed with `npm ci`; clone sources are pinned
to SHAs; CBM binary is NOT bundled; `puppeteer-core` is install-only at a
pinned version):

| Library | Decision | Reason |
|---------|----------|--------|
| react-three-fiber (+ `three`, `@types/three`) | **Install-on-demand, per project** (`npm install three@0.185.1 @types/three@0.185.1 @react-three/fiber@9.8.2` / `@8.18.0`, exact pins in the project's package.json + lockfile) | A build's runtime dependency, not a plugin-script dependency. The plugin never loads R3F itself. |
| liquid-glass-js | **Vendored file copies at the pinned commit** (copy `container.js`, `button.js`, `glass.css` from dashersw/liquid-glass-js @ `78cb6ccb…` into the project; `html2canvas@1.4.1` loaded per the README quick-start) | No npm package exists — there is nothing to `npm install`. The pin is the repo commit SHA by necessity. No tags/releases exist, so no semver pin is possible. |
| ShaderGradient (+ R3F, `three`, `three-stdlib`, `camera-controls`) | **Install-on-demand, per project** (`npm i @shadergradient/react@2.4.20 @react-three/fiber@<paired> three@0.185.1 three-stdlib@2.36.1 camera-controls@3.1.2`, exact pins in the project's package.json + lockfile) | Same as R3F. The customize URL is config, not a dependency. |
| liquid-logo | **Standalone tool, no install** (run the hosted version at liquid.paper.design, or the repo at the pinned commit `689bb38a…`; output is an MP4/PNG asset only) | `package.json` is `private: true`, version 0.1.0 — there is no published package. The plugin never installs it; the build ships the produced asset + the static-logo fallback. |

**Security note (how checked):** each repo/licence/version was verified
live from the authoritative source (GitHub repo page + raw files + npm
registry, §2). All four are public libraries/tools with real usage
(R3F 33.6k stars, ShaderGradient 3.1k, liquid-glass-js 1.7k,
liquid-logo 1.4k). No install scripts were run by this agent, and the
plugin itself never installs these libraries — they are installed by the
build's own package-manager step, copied as source, or run as a
standalone tool. The standing re-scan bar (0 malicious) applies at audit
time over the new pins; nothing here exempts it.

## 7. SPEC deviations proposed / flags for the coordinator

**D1 — ShaderGradient licence is MIT-declared but has NO root LICENSE file
(SPEC §15 expected MIT).** Verified live: no `LICENSE` in the repo root,
no licence field on the repo page. The MIT grant rests on the README
("MIT © ruucm, stone-skipper") and the package.json `"license": "MIT"`.
The free-only rule still holds; only the licence *evidence* differs.
Recorded as a caveat in L15-03/L15-05 (verify22.py must assert the
caveat text, not a root LICENSE file). If a build's legal review needs
actual licence text, the grant must be confirmed with the maintainer
before shipping.

**D2 — liquid-logo licence is PolyForm Shield 1.0.0, NOT MIT (SPEC §15
flagged this; verified).** The repo's `LICENSE` read verbatim is
PolyForm Shield 1.0.0, which carries a noncompete clause (do not use the
tool to provide a competing product). The underlying
`@paper-design/shaders-react` is Apache-2.0 (latest 0.0.82; the tool
itself pins 0.0.21). Recorded in L15-03/L15-04/L15-07 with which licence
applies to what. The plugin's use (producing one brand asset for a
build's own product) does not compete with the tool, but the manifest
must record the noncompete — and verify22.py must assert "PolyForm
Shield" for the repo, not "MIT".

**D3 — liquid-glass-js has no tags, no releases, one commit.** The pin
is the commit SHA `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a` by necessity.
The repo is a single-commit snapshot (created 2025-06-11); treat it as a
pinned asset, not a live dependency needing upstream updates (same
treatment as Bang Motion §12). If upstream later publishes an npm
package, re-pinning is a deliberate decision, never a float.

**D4 — liquid-logo's tool pins an old shaders-react (0.0.21 vs latest
0.0.82).** The tool is a standalone Next app, not a dependency, so its
internal pin does not propagate into builds. Recorded in L15-07; no
action — the build never installs `@paper-design/shaders-react` unless
it ports the shader idea into its own R3F shader, in which case it pins
the current verified version deliberately.

**D5 — three.js pins now coexist three-ways (by scope, intentional).**
General `three@0.185.1` (R3F + ShaderGradient scenes, this fix);
Vanta-scoped `three@0.134.0` (unchanged, §11); upstream latest 0.187.0
(verified, NOT adopted). The three pins are scoped, not single-version —
same treatment as the fix22.py GSAP/three.js convergence note (GSAP
converges on one version; three.js is scoped).

**D6 — R3F v8 latest is 8.18.0, not 8.17.10.** The ShaderGradient
package.json devDeps cite `^8.17.10`; the v8 line has since moved to
8.18.0 (verified via `npm view`). The pin in this spec is 8.18.0. No
conflict — the devDep range is the upstream repo's, not the plugin's.

**D7 — The §13 seventh D19 dimension (Depth) is NOT added to these
patches' D19 blocks.** These texts use the standing six-dimension D19
form (Motion / Theme / Texture / Visuals / Techniques / Colors), matching
the §11 patches. §13 (3D/depth) may extend D19 with a seventh Depth
dimension; if the coordinator adopts that form, these blocks should be
aligned then — flagged, not silently pre-empted.

**D8 — L15-06 edit point is the shared global less-flat-ui source.**
build.sh:263 copies `~/workspace/cursor-skills/less-flat-ui/` into the
plugin, so the source file is the only edit point that survives a
rebuild — but that file is also the global Cursor skill used outside the
plugin, so editing it changes the global skill too. The alternative
(patching the built copy in the fix22 block, like the Batch E fix #4
patches at build.sh:20972+) would diverge from the source on every
rebuild. The coordinator decides and records the choice; this spec is
written for the source file.

**D9 — SPEC wording flag (see §4):** the SPEC calls collidingScopes the
"earlier" liquid-logo repo; creation dates show paper-design
(2025-02-18) predates collidingScopes (2025-03-03). Resolution unchanged
(reel = paper-design); correct the wording in the manifest.

**D10 — The cindie.zhu guide URL did not resolve in this session** (see
§4). The namesake resolutions rest on the SPEC + independently verified
repo facts, not on a fresh guide fetch. Coordinator may re-check the
guide for the manifest.

## 8. Dry-run fixtures — exact check phrases (SPEC §15 verification)

The patch texts are written so each SPEC §15 dry-run fixture is decidable
against an exact phrase in the built tree:

| Fixture | Verdict | Exact check phrase(s) in the patch text |
|---------|---------|------------------------------------------|
| (a) A surface stacking two WebGL-heavy effects FAILS | FAIL | L15-08: "a surface (or page) carrying TWO OR MORE WebGL-heavy library effects at once"; "a surface stacking two WebGL-heavy effects FAILS this check"; L15-03: "Stacking two or more WebGL-heavy effects on one surface FAILS the `polish-pass` flag" |
| (b) A surface with one theme-matched WebGL effect + static fallback PASSES | PASS | L15-08: "exactly ONE WebGL-heavy effect on the surface, theme-matched, with its static fallback and its reduced-motion handling recorded — a surface with one theme-matched WebGL effect + static fallback PASSES" |
| (c) A React 18 build installing R3F v9 FAILS the pairing check | FAIL | L15-01/L15-02/L15-05: "React 18 + R3F v9 FAILS the pairing check" (and "React 19 + R3F v8 FAILS the pairing check") |
| (d) A build installing legacy `shadergradient` v1 FAILS | FAIL | L15-03/L15-05: "Install `@shadergradient/react` (v2), NOT legacy `shadergradient` (v1.3.5"; "a build installing legacy `shadergradient` v1 FAILS the version check" |
| (e) A build using the animated logo with no static fallback FAILS | FAIL | L15-07: "the original static logo is kept as the fallback for old phones and non-WebGL contexts, and a build using the animated logo with no static fallback FAILS the check" |
| (f) A build applying a library effect with no theme reason FAILS | FAIL | Every patch: "Theme-match precondition: a library effect is applied only when it matches the dealt theme; a clash is not applied, with the reason recorded in `docs/design-tokens.md`" (L15-03) and per-library equivalents |
| (g) A build using an unpinned ("latest") library version FAILS the pin check | FAIL | L15-03: "Unpinned versions (\"latest\") FAIL the pin check" |

Additional decidable phrases: R3F pairing version check ("read the
project's `package.json` `react` version first, then install the matching
R3F major"); ShaderGradient URL-as-config ("design at
shadergradient.co/customize, copy the URL — the URL IS the config");
liquid-glass-js no-npm handling ("NO npm package — copy `container.js`,
`button.js`, `glass.css` into the project"); liquid-logo standalone
handling ("STANDALONE TOOL, not a library to import and not a runtime
dependency"); the honest input check ("tell me honestly whether the logo
will work with this shader"); the one-WebGL rule ("One WebGL-heavy
effect per surface (WEBGL_ONE_F22)").

## 9. Self-verification performed

- Re-ran all coverage greps over build.sh (R3F 0, shadergradient 0,
  liquid-logo 0, liquid-glass 4 hits at 18731/19412/19449/19458) and
  confirmed the built tree has 0 hits for `liquid-glass-design` under
  `hackathon-ecc/skills/`.
- Verified every L15-01–L15-08 anchor occurs exactly once in its target
  file in the current built tree / staged source (counts recorded per
  patch): L15-01 A11 block 1; L15-02 `## End-to-End Example` 1 (in
  motion-patterns); L15-03 LIB-03 tail 1 (chained, runs after LIB-03);
  L15-04 B1 tail sentence 1 (in ui-ux-pro-max); L15-05 `- **One object
  never carries the page.**` 1 (in the staged Taste file); L15-06
  `### 3. Thermal gradients` 1 (in the less-flat-ui source); L15-07 B1
  tail sentence 1 (in the staged Taste file, line 416); L15-08 slop
  tail 1 (in the staged slop-checklist, 484 lines).
- Checked no anchor collides with ab-patches.md, process-patches.md, or
  libraries-patches.md anchors; L15-02 shares LIB-07's anchor with the
  documented order (LIB-07 first).
- Verified the five anchor tokens (`R3F_F22`, `LIQGLASS_F22`,
  `SHADERGRAD_F22`, `LIQLOGO_F22`, `WEBGL_ONE_F22`) were 0 in build.sh
  and 0 in the built tree before this fix.
- Verified all versions/licences live from GitHub repo pages, raw files,
  and the npm registry (§2 table); verified the 10 ShaderGradient preset
  keys from upstream `presets.ts`; verified both namesake repos live
  (§4).
- Banned-term scan (case-insensitive) over this file: **0 hits** for any
  of the seven banned terms (verified by grep after writing — see the
  coordinator's re-check).
- No new skill created; no font rules, screen-verdicts rule, model pins,
  marketplace manifest, or Audit #4 backup touched; `hackathon-ecc/`
  never edited; `bash build.sh` never run; `fix11/fix11-stage.py` never
  run; `fix22.py` / `verify22.py` never edited.
- No file outside `~/workspace/hackathon-plugin/fix22/` was written.

## 10. Open items for the coordinator / parent

1. Apply L15-01–L15-08 per the integrator checklist; rebuild; run the
   verify22.py additions in §7 of the patch specs.
2. Adjudicate / record deviations D1–D10 in the manifest (esp. D1
   ShaderGradient missing LICENSE caveat, D2 PolyForm Shield noncompete,
   D8 less-flat-ui edit point, D9 "earlier" wording correction).
3. Dry-run fixtures per SPEC §15, using the exact check phrases in §8.
4. The §13 coordinator owns the Depth D19 dimension (D7) — align these
   D19 blocks if the seventh dimension is adopted.
5. The `liquid-glass-design` resolution (option (b), §5) needs only the
   manifest record — no code change.
