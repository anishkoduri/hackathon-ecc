---
name: less-flat-ui
description: Make the UI more striking with 22 textured treatments (felt, fluted glass, thermal gradients, halftone, grainy gradients, blueprint grids, contour lines, pixel mosaics, iridescent shapes, ASCII/pixel art, and more). Apply every treatment that fits the project, layering compatible ones on backgrounds, cards, buttons, dividers, and headings. Use when flat surfaces look dull; keep text readable. Invoke by asking to make the UI less flat. Inside a design-taste-frontend build, apply the texture layer only where its page system leaves a surface unstyled — never over its hero, dealt moments, or shader scenes.
---

# Less Flat UI

Source of the 22 treatments: Instagram reel by @charles.unemployed, "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)". The reel frames them as backgrounds, but each one is a texture/pattern treatment that can go on any surface: page backgrounds, cards, buttons, dividers, headings, modals, nav.

## When to use

Apply treatments when the UI looks flat or dull: heroes, landing pages, empty states, cards, buttons, dividers, headings, modals. Apply EVERY treatment that fits the project's mood, not just one. The picker table below is a menu, not a single choice. On a landing page built with design-taste-frontend, apply treatments only where the Taste page system leaves a surface unstyled — never over the hero, dealt moments, or shader scenes. A flat-colour section IS part of the page system — do not texture it.

A treatment fits when:

- It matches the project's mood (see the picker table). Never pick at random.
- It can sit on the surface you are treating without hurting readability or usability.
- Body text still passes contrast (4.5:1 minimum). If in doubt, add a scrim (see Shared utilities).

Do NOT use when:

- The page is a dense dashboard, form, or data table. Flat and calm wins there. A data-dense page is one whose primary content is tables/grids of numbers.
- A flat-colour section of a design-taste-frontend page: it IS part of the page system, not an unstyled surface — do not texture it.
- The project already has a strong brand background or a photo-led design.
- The treatment would fight the content (e.g. contour lines behind a map, ASCII art behind code).

Rules:

- **Apply all that fit, then edit down.** Layer every fitting treatment, then look at the result: if it reads busy or muddy, remove the weakest treatment and check again. Stop as soon as it reads clean. Restraint is applied at the end, not the start.
- **Texture in service of the wow moment, not decoration:** apply treatments where they amplify the page's captivating moment; never texture for its own sake — if a treatment does not make the memorable moment stronger, leave that surface flat.
- **Layer compatible treatments, not competing ones.** Grain, gradients, and soft textures layer with almost anything. Two busy patterns (pixel mosaics + halftone, two grids, ASCII + stippling) fight each other; pick the stronger one.
- **Treatments stay behind content.** Content sits above them (`position: relative; z-index: 2` on content, background layers at `z-index: 0/1`). A treatment on a card or button must never reduce that element's legibility or affordance.
- **Prefer CSS gradients and SVG over images.** They are sharp at every size and cost almost nothing.
- **Respect `prefers-reduced-motion`.** Any animated variant (ripples, lens, clouds) must be static under reduced motion.
- **Keep noise cheap.** Noise tiles are 160px, `opacity` 0.05–0.12, never animated.

## Picker: match the mood

| Project mood | Best treatments |
|---|---|
| Technical, engineering, dev tools | Blueprint grids, contour lines, ASCII and pixels, halftone, square-dot grids |
| Premium, soft, wellness, beauty | Paper texture, cloud sky, felt texture, grainy gradients |
| Bold, playful, consumer | Pixel mosaics, thermal gradients, iridescent shapes, dithered images |
| Photo-led, editorial | Blurred photos, impressionist paintings, single-hue landscapes |
| Dark, moody, gaming | Speckled graphite, lens distortion, stippled gradients, fluted glass |
| Data, science, research | Contour lines, blueprint grids, stippled gradients, thermal gradients |
| Retro, zine, brutalist | Halftone, dithered images, ASCII and pixels, pixel mosaics |

The "Data, science, research" row applies to non-dense data/science pages (marketing, explainer, editorial) — on a data-dense page (primary content is tables/grids of numbers) no treatment applies; the page stays flat.

If none of the rows fits, do not force a treatment. Flat is fine.

## Where else to apply them

Backgrounds are the default surface, but the same treatments work on components:

| Surface | Treatments that work well |
|---|---|
| Cards and panels | Felt, paper, fluted glass, grainy gradients, speckled graphite |
| Buttons and CTAs | Thermal gradients, iridescent shapes, grainy gradients |
| Section dividers | Contour lines, halftone strip, square-dot grid strip, ASCII divider |
| Headings and display type | Grainy gradients (text fill via background-clip), halftone behind type, dithered images |
| Modals and overlays | Fluted glass, blurred photos |
| Nav and sidebars | Blueprint grids (subtle), square-dot grids, felt |
| Badges, tags, chips | Pixel mosaics, halftone, stippled gradients |
| Empty states and illustrations | Single-hue landscapes, cloud sky, impressionist dabs, pixel mosaics |

A treatment on a small surface can be bolder than on a full page: a button can carry a full thermal gradient, a page background usually should not.

## Shared utilities

Put these in a `backgrounds.css` file (or a `<style>` block) and reference them by class. Do not cram data-URI SVGs into Tailwind arbitrary values. Record every treatment applied, on which surface, in `docs/design-tokens.md` (or MASTER.md on a dashboard-only build) — later slices and polish-pass read the record from there, not from the CSS.

Grain overlay (reused by felt, grainy gradients, paper, speckled graphite):

```css
.grain { position: relative; isolation: isolate; }
.grain::after {
  content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
  background-size: 160px 160px;
  opacity: 0.08; mix-blend-mode: overlay;
}
.grain > * { position: relative; z-index: 2; }
```

Scrim for text over busy backgrounds:

```css
.scrim { position: relative; }
.scrim::before {
  content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background: linear-gradient(180deg, rgba(8, 8, 16, 0.55), rgba(8, 8, 16, 0.25));
}
.scrim > * { position: relative; z-index: 2; }
```

## The 22 treatments

Re-tint every example below to the project's dealt palette and tokens before using it — the hex values are placeholders, not the palette. Never copy a purple/violet gradient onto a landing page (Hallmark gate 2a and Taste §6 Never ban it); the craft floor's purple-blue-gradient ban applies the same way on app surfaces.

### 1. Felt texture

Best for: soft, tactile, premium surfaces. Warm matte fabric feel.

```css
.felt {
  background-color: #7d6f66;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E"),
    linear-gradient(160deg, #8a7d74, #6b5d54);
  background-size: 160px 160px, cover;
}
```

Keep the base color muted. Felt reads as soft only when contrast is low.

### 2. Fluted glass

Best for: frosted panels, cards over imagery, premium overlays.

```css
.fluted-glass {
  background-color: rgba(255, 255, 255, 0.14);
  background-image: repeating-linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.30) 0 2px,
    rgba(255, 255, 255, 0.06) 2px 6px,
    rgba(0, 0, 0, 0.10) 6px 8px,
    rgba(255, 255, 255, 0.05) 8px 14px
  );
  backdrop-filter: blur(14px) saturate(1.3);
  -webkit-backdrop-filter: blur(14px) saturate(1.3);
  border: 1px solid rgba(255, 255, 255, 0.25);
}
```

Needs something behind it to frost (a photo or gradient). On a flat color it does nothing.

### 3. Thermal gradients

Best for: heatmaps, energy, AI/data products, bold heroes — on non-dense surfaces (never a data-dense dashboard — see Do NOT use).

```css
.thermal {
  background:
    radial-gradient(60% 50% at 20% 20%, #ff5e3a 0%, transparent 60%),
    radial-gradient(50% 60% at 80% 30%, #ffb400 0%, transparent 55%),
    radial-gradient(70% 70% at 50% 90%, #7b2ff7 0%, transparent 60%),
    linear-gradient(180deg, #1a0b2e, #2b1055);
}
```

Order matters: hottest color first, dark base last. White text only, with a scrim if the yellow zone sits behind copy.

### 4. Water ripples

Best for: calm, aquatic, meditative products. Static by default.

```css
.ripples {
  background:
    repeating-radial-gradient(circle at 30% 40%, rgba(255, 255, 255, 0.35) 0 1px, transparent 1px 14px),
    repeating-radial-gradient(circle at 70% 65%, rgba(255, 255, 255, 0.22) 0 1px, transparent 1px 18px),
    linear-gradient(180deg, #0e4d64, #0a2e3f);
}
```

Animated variant: animate the `background-position` of the ripple layers very slowly (60s+ linear infinite) and disable it under `prefers-reduced-motion`. Never animate fast; it reads as a glitch.

### 5. Speckled graphite

Best for: dark developer tools, gaming, moody non-dense dashboards (never a data-dense dashboard — see Do NOT use).

```css
.speckled-graphite {
  background-color: #232326;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.9 0'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E");
  background-size: 140px 140px;
}
```

Keep speckle subtle (the `feColorMatrix` alpha row controls density). Light text, no extra decoration.

### 6. Single-hue landscapes

Best for: editorial, travel, wellness, calm landing pages.

```css
.single-hue {
  background: linear-gradient(180deg, #d8ecdf 0%, #a9d3b8 45%, #5da884 100%);
}
```

Layer SVG hill shapes in progressively darker tints of the same hue on top (three `<path>` layers, each ~15% darker). The whole scene stays inside one hue family; that restraint is the look.

### 7. Blueprint grids

Best for: engineering, architecture, dev tools, technical products.

```css
.blueprint {
  background-color: #1e4f9c;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.28) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.28) 1px, transparent 1px),
    linear-gradient(rgba(255, 255, 255, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.12) 1px, transparent 1px);
  background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
}
```

Two grid scales (100px major, 20px minor) sell the drafting-table feel. White or pale-blue text only.

### 8. Halftone

Best for: retro, print/zine, bold posters, comic styles.

```css
.halftone {
  background-color: #f4efe6;
  background-image: radial-gradient(circle, #1a1a1a 1.2px, transparent 1.4px);
  background-size: 12px 12px;
}
```

True variable-size halftone (dots growing toward an image) needs SVG or canvas. The CSS version is a uniform dot screen: use it as a texture, not as a picture.

### 9. Grainy gradients

Best for: almost any non-dense surface. The safest treatment on this list.

```css
.grainy-gradient {
  background: linear-gradient(135deg, #ff8a5c, #ff5e8a 45%, #7b2ff7);
}
```

Then add the shared `.grain` overlay class on the same element. Grain kills the cheap digital banding that flat CSS gradients get, and it works under any palette. When unsure, pick this one.

### 10. Grass texture

Best for: outdoors, sports, eco, playful products.

```css
.grass {
  background:
    repeating-linear-gradient(100deg, transparent 0 3px, rgba(0, 0, 0, 0.14) 3px 4px),
    repeating-linear-gradient(80deg, transparent 0 5px, rgba(255, 255, 255, 0.08) 5px 6px),
    linear-gradient(180deg, #7fb069, #3e7a3a);
}
```

The crossed repeating gradients at slight angles fake grass blades. For a hero, layer a real grass SVG silhouette at the bottom edge instead of relying on the gradient alone.

### 11. Dithered images

Best for: retro, lo-fi, zine, pixel-art-adjacent products.

Do this at build time, not in CSS: run the image through a Bayer dithering step (canvas script, ImageMagick, or an editor) and ship the dithered file. CSS fallback if you must do it live:

```css
.dithered { position: relative; }
.dithered::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background-image: conic-gradient(#000 25%, transparent 0);
  background-size: 4px 4px;
  opacity: 0.18; mix-blend-mode: multiply;
}
```

The fallback only suggests dithering. Real Bayer dithering on a 1-bit or limited palette is what makes it read.

### 12. Paper texture

Best for: editorial, notes, journals, premium minimal products.

```css
.paper {
  background-color: #f5f0e6;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.4'/%3E%3C/svg%3E"),
    repeating-linear-gradient(0deg, transparent 0 3px, rgba(0, 0, 0, 0.015) 3px 4px);
  background-size: 160px 160px, auto;
}
```

Off-white, never pure white. Dark warm-gray text (`#2b2620`), never pure black, or the paper looks dirty.

### 13. Contour lines

Best for: maps, outdoors, data/science, technical products — on non-dense surfaces (never a data-dense dashboard — see Do NOT use).

```css
.contours {
  background-color: #0f2a1d;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600' viewBox='0 0 600 600'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.32)' stroke-width='1'%3E%3Cpath d='M300 70 C 380 90 430 160 420 250 C 410 340 350 400 300 420 C 240 440 170 380 160 300 C 150 220 220 120 300 70 Z'/%3E%3Cpath d='M300 120 C 360 135 395 190 388 255 C 380 320 335 365 300 380 C 255 395 200 350 192 295 C 185 235 240 150 300 120 Z'/%3E%3Cpath d='M300 175 C 340 185 365 225 360 265 C 354 305 325 335 300 342 C 268 350 230 320 226 285 C 222 245 260 195 300 175 Z'/%3E%3Cpath d='M300 230 C 322 238 335 258 332 282 C 329 305 315 320 300 323 C 280 326 262 308 261 288 C 260 262 280 240 300 230 Z'/%3E%3C/g%3E%3C/svg%3E");
  background-size: 600px 600px;
  background-position: center;
}
```

Nested wobbly closed paths read as topography. Keep the stroke faint; contour lines are a texture, not a map, unless the project actually is one.

### 14. Cloud sky

Best for: calm, dreamy, wellness, kids, weather products.

```css
.cloud-sky {
  background:
    radial-gradient(40% 30% at 20% 30%, rgba(255, 255, 255, 0.9), transparent 70%),
    radial-gradient(35% 25% at 70% 20%, rgba(255, 255, 255, 0.7), transparent 70%),
    radial-gradient(50% 35% at 50% 75%, rgba(255, 255, 255, 0.5), transparent 70%),
    linear-gradient(180deg, #aee2ff 0%, #e8f6ff 55%, #ffffff 100%);
}
```

Soft white blobs over a sky gradient. Dark slate text (`#1e3a4c`), never black, and keep clouds out of the top-left where headlines usually sit.

### 15. Pixel mosaics

Best for: playful, gaming, retro, creative tools.

```css
.pixel-mosaic {
  background-color: #111114;
  background-image: conic-gradient(#ff6b6b 25%, #ffd93d 0 50%, #6bcb77 0 75%, #4d96ff 0);
  background-size: 48px 48px;
}
```

The conic trick tiles 2x2 color blocks. Vary the tile size (32–64px) and palette per project. For a photographic mosaic, build it from a real image with a canvas pixelation step instead.

### 16. Lens distortion

Best for: experimental, optical, camera, or AR products. Use sparingly.

```css
/* Cheap static fake: a circular bulge */
.lens-fake {
  border-radius: 50%;
  transform: scale(1.04);
  box-shadow: inset 0 0 60px rgba(255, 255, 255, 0.25), inset 0 0 120px rgba(0, 0, 0, 0.35);
}
```

Real distortion needs an SVG filter on the element:

```xml
<filter id="lens">
  <feImage href="data:image/svg+xml,...radial-gradient displacement map..." preserveAspectRatio="none" result="map"/>
  <feDisplacementMap in="SourceGraphic" in2="map" scale="36" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

Keep `scale` between 20 and 40. More than that looks broken, not artsy. Never apply to text.

### 17. Stippled gradients

Best for: editorial, scientific illustration, elegant dark sections.

```css
.stippled {
  background-color: #efe9dc;
  background-image: radial-gradient(circle, rgba(30, 25, 20, 0.55) 1px, transparent 1.5px);
  background-size: 10px 10px;
  -webkit-mask-image: linear-gradient(180deg, #000 0%, transparent 85%);
  mask-image: linear-gradient(180deg, #000 0%, transparent 85%);
}
```

The mask fades the dot field along the gradient, so density follows tone like real stippling. Flip the mask direction to fade the other way.

### 18. Square-dot grids

Best for: technical, minimal, dev tools, non-dense dashboards that want texture without noise (never a data-dense dashboard).

```css
.square-dots {
  background-color: #fafafa;
  background-image:
    linear-gradient(90deg, rgba(0, 0, 0, 0.28) 0 3px, transparent 3px),
    linear-gradient(rgba(0, 0, 0, 0.28) 0 3px, transparent 3px);
  background-size: 16px 16px;
  background-position: -1px -1px;
}
```

Small filled squares at grid intersections. Darker variant: `#101014` base with `rgba(255,255,255,0.25)` dots. Keep dots small (2–3px); bigger reads as a checkerboard.

### 19. Blurred photos

Best for: photo-led heroes, music, food, travel, any product with good imagery.

```css
.blurred-photo { position: relative; overflow: hidden; isolation: isolate; }
.blurred-photo::before {
  content: ""; position: absolute; inset: -24px; z-index: 0;
  background-image: url("photo.jpg");
  background-size: cover; background-position: center;
  filter: blur(24px) saturate(1.25);
}
.blurred-photo::after {
  content: ""; position: absolute; inset: 0; z-index: 1;
  background: rgba(10, 10, 20, 0.45);
}
.blurred-photo > * { position: relative; z-index: 2; }
```

The `inset: -24px` hides the blur's transparent edges. Always add the dark scrim (`::after`) or text will fail contrast. Use the project's own photo, never a stock filler.

### 20. Iridescent shapes

Best for: playful, beauty, creative tools, bold consumer heroes.

```css
.iridescent {
  background:
    radial-gradient(45% 45% at 25% 25%, rgba(255, 0, 128, 0.55), transparent 70%),
    radial-gradient(40% 40% at 75% 30%, rgba(0, 229, 255, 0.50), transparent 70%),
    radial-gradient(55% 55% at 55% 85%, rgba(255, 214, 0, 0.45), transparent 70%),
    linear-gradient(135deg, #1b1035, #0b1026);
}
```

For a soap-bubble variant, put the same blobs on a separate layer with `filter: blur(30px)` and `mix-blend-mode: screen`. Keep the palette to three hues max or it turns to mud.

### 21. Impressionist paintings

Best for: art, editorial, food, travel, romantic or nostalgic products.

```css
.impressionist {
  background:
    radial-gradient(18% 12% at 22% 30%, #e8b04b 0%, transparent 70%),
    radial-gradient(14% 10% at 68% 24%, #7fa8c9 0%, transparent 70%),
    radial-gradient(20% 14% at 40% 62%, #c96f4a 0%, transparent 70%),
    radial-gradient(16% 12% at 78% 66%, #8a9a5b 0%, transparent 70%),
    radial-gradient(22% 14% at 55% 40%, #d9c27a 0%, transparent 70%),
    linear-gradient(180deg, #f2e3c6, #e3cfa5);
}
```

Many small soft dabs of varied color, like brush strokes. Add the shared `.grain` overlay to break the digital smoothness. Pick dabs from the project's palette, not random colors.

### 22. ASCII and pixels

Best for: dev tools, terminals, retro, hacker aesthetics, easter eggs.

```css
.ascii-bg {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 10px; line-height: 1; letter-spacing: 0;
  color: rgba(255, 255, 255, 0.14);
  user-select: none; pointer-events: none;
  overflow: hidden; white-space: pre;
}
```

Fill it with a small script (mark the element `aria-hidden="true"`):

```js
const chars = " .:-=+*#%@";
const el = document.querySelector(".ascii-bg");
const cols = Math.ceil(el.clientWidth / 6);
const rows = Math.ceil(el.clientHeight / 10);
let out = "";
for (let y = 0; y < rows; y++) {
  for (let x = 0; x < cols; x++) {
    const dx = x / cols - 0.5, dy = y / rows - 0.5;
    const d = Math.sqrt(dx * dx + dy * dy);
    const v = Math.max(0, 1 - d * 1.6) * Math.random();
    out += chars[Math.floor(v * (chars.length - 1))];
  }
  out += "\n";
}
el.textContent = out;
```

Characters cluster into a soft radial blob. Keep opacity low; ASCII is texture, not content, so it must never be readable as text or selectable.

## Tailwind notes

- These live in plain CSS classes in `backgrounds.css`. Import the file once (globals.css / main.css) and use the class names.
- Do not paste data-URI SVGs into Tailwind arbitrary values; the escaping breaks.
- In Tailwind v4 you can register a treatment as `@utility bg-blueprint { ... }` if you want it to compose with variants, but a plain class is fine.
- Pair with the ui-ux-pro-max skill: that skill owns layout, type, and components; this skill owns the texture and depth layer (backgrounds, cards, buttons, dividers). If the two disagree on mood, the texture yields to the design system.
