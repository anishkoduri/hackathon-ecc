---
name: getlayers
description: Use when the build needs a cinematic visual layer — a page template, a real-time 3D WebGL scene, an animated background, a page section, or a pointer-reactive gradient — from the GetLayers library, or when the user names GetLayers or a GetLayers layer. Rebuilds the layer from its prompt in the project's own stack; never ships a layer unchanged.
---

> **Hackathon-ecc note (fix #31, GETLAYERS_F31).** GetLayers (getlayers.ai, Textura) is a prompt-first library: every layer copies as one self-contained prompt an agent rebuilds in any stack. **FREE SET ONLY** — never the paid Unlimited / Unlimited Plus / Full Stack plans, never a paid service. **No MCP:** the GetLayers MCP (`https://mcp.getlayers.ai/mcp`) requires the Full Stack Lifetime plan and is NOT wired in this plugin; this skill uses the prompt path only (browse the live library, copy the layer's prompt, rebuild it). **Reference only:** the plugin vendors NO GetLayers content — no layer prompts, no templates, no scenes, no backgrounds, no gradients, no media. The library's licence bars scraping, redistribution, and resale; bulk or automated copying gets accounts restricted. **A layer is a foundation, not a finished brand:** restyle its copy, palette, and subject matter to the dealt theme and the brief — never ship a free trial layer unchanged. **Weight in the palette-first flow:** GetLayers prompts are a first-class, high-priority source — the design-lead consults them FIRST, before the other palette sources, and the direction leans on GetLayers layers heavily as its foundation. The design direction names the GetLayers layers USED or CONSIDERED-AND-REJECTED, each with a D19 reason (same as every inventory entry). **Counts drift weekly** (new layers land every week): never freeze a count in a build or a decision record — read the live counts at `https://getlayers.ai/llms.txt` when you need them. Every layer, free ones included, carries a commercial licence (no attribution). **Layer role: foundation** (inventory `skills/orchestrate/references/design-inventory.md` §12) — the first layer of the one design system, consulted first; the direction cites every layer considered as USED or CONSIDERED-AND-REJECTED with a D19 reason. **Plugin rules override this skill where they differ:** fonts are static and self-hosted (never a Google Fonts CDN link from a layer); one WebGL-heavy effect per surface (WEBGL_ONE_F22) — a GetLayers 3D scene or animated background IS that surface's one WebGL-heavy effect; `prefers-reduced-motion: reduce` gets a complete static fallback.

# GetLayers — prompt-first cinematic layers

## What it is

GetLayers is a curated library of visual layers for cinematic marketing sites, in five categories:

- **Templates** — production-ready page and hero templates for animation-heavy marketing sites.
- **3D Scenes** — interactive real-time WebGL scenes (particles, fluid, terrain, galaxy, shader fields).
- **Sections** — drop-in animated page sections (features, cards, carousels, showcases, roadmaps, loaders), each with its motion already wired.
- **Backgrounds** — animated and static backdrops (landscape, abstract glass, particles, cosmic, molecular).
- **Gradients** — animated, pointer-interactive gradients drawn in pure WebGL, about a kilobyte each, no libraries, no video.

Every layer is copyable as one self-contained prompt. A free layer's prompt is free for everyone, and free backgrounds' video files download for free. The live catalog is at `https://getlayers.ai/` and the machine-readable index at `https://getlayers.ai/llms.txt` (categories, core pages, key facts) — read `llms.txt` first when you need the current counts or the category links; the counts there are the live ones.

## When to reach for it

- The brief calls for a cinematic hero, an animated ground, a real-time 3D scene, or a pointer-reactive gradient and the dealt theme's material fits a library layer.
- A landing page needs a section whose motion is already designed (a loader, a showcase, a carousel) rather than invented from scratch.
- The build needs a video background (a free background's 4K master) or a gradient ground behind a hero.

Do NOT reach for it when the surface's job is app UI (dashboards, forms, data) — layers are marketing-site material. A GetLayers layer never replaces the dealt Hallmark theme or the design direction; it is palette material the design-lead inventories first (PALETTE-FIRST_F27) and tailors.

## Priority in the palette-first flow

GetLayers prompts are consulted FIRST in the palette inventory — ahead of MotionSites, the design package, and the dealt Hallmark theme — because the direction leans on GetLayers layers heavily as its foundation. The flow:

1. The design-lead reads the live GetLayers library (`llms.txt` + the category pages) before the other palette sources and picks the layers that fit the surface's job and the dealt theme.
2. The direction is built on those layers — their compositions, their motion, their grounds — then tailored to the brief (step 4 of the workflow below).
3. The design direction names every GetLayers layer it USED and every layer it CONSIDERED-AND-REJECTED, each with a D19 reason — the same treatment as every inventory entry. A direction that names no GetLayers layer at all (neither used nor considered-and-rejected, nor `not considered — <reason>`) is a finding at the audit.

Priority is about consultation order and foundation weight, not about forcing a layer: if no free layer fits the surface's job, the direction records `not considered — <reason>` and builds from the design package instead — never a mismatched layer, never a generic fallback.

## Workflow

### 1. Browse the live library — never from memory

Read `https://getlayers.ai/llms.txt` for the current categories and counts, then browse the category pages (`/templates`, `/3d-scenes`, `/sections`, `/backgrounds`, `/gradients`). Judge fit by reading descriptions and the live preview, in the brief's own language — never by tag-matching, and never from a frozen list in this skill (the library changes weekly). Pick the ONE layer that fits the surface's job and the dealt theme; record the pick (layer name, category, URL) in the design direction with its D19 reason.

### 2. Copy the layer's prompt

On the layer's page, copy its prompt — the single self-contained prompt that rebuilds the layer. That prompt is the build spec for the layer: it carries the composition, the motion, and the configuration. Do NOT copy the layer's source (source downloads are a Full Stack benefit, not available here) and do NOT vendor the prompt into the plugin — the prompt is used once, for this build, in the project.

### 3. Rebuild it in the project's stack

Rebuild the layer from the prompt in the build's actual stack (React/Next.js, Vite, or plain HTML). A template's portable single-HTML master is translated into the stack; a Next.js template is rebuilt as the Next tree, never handed over as HTML to translate back. Follow the prompt's composition and motion; adapt only the integration (imports, file layout, the project's token system).

### 4. Restyle it into the brand — the foundation rule

A layer is a foundation, not a finished brand. Before the layer is accepted:

- Re-tint it through its configuration to the dealt theme's palette (never by editing shader colour — that produces garbage).
- Replace its copy with the brief's own copy, its subject matter with the brief's subject, its type with the dealt pairing.
- Keep its motion and its composition — that is what the layer is for.
- Record what was tailored and why (a fix #19 D19 reason) in `docs/design-tokens.md`.

A build that ships a free trial layer unchanged — same copy, same palette, same subject — is a template build, not a design, and fails the ambition bar (AMBITION_F23).

### 5. Media: download, never hotlink

- Backgrounds ship as video: download the background's video (4K master) and poster into the project (e.g. `public/`) and wire a full-bleed muted looping autoplay `<video>` with the poster. Never hotlink `storage.getlayers.ai` (watermarked, and the links expire).
- 3D scenes and templates reference heavy media (`.glb`, `.mp4`, textures) by URL: download every file into the project and repoint the markup at the local copies. Verify each file's size after download — an expired link writes a short error page under a media filename, and the only symptom is a blank canvas.
- The reveal choreography is the default: an immersive loader, content gated until it completes, text/images/scroll revealing in sequence, a 3D scene entering with a real entrance — unless the brief asks to simplify.

## What NOT to do

- **No MCP.** Do not wire `https://mcp.getlayers.ai/mcp`, do not call `getlayers_*` tools, do not configure an MCP server for GetLayers — the MCP is a paid Full Stack benefit and is not available on the free set.
- **No paid plans.** Never buy or upgrade to Unlimited, Unlimited Plus, or Full Stack; never spend Studio credits (image/video/3D generation, upscaling, background removal) — those are paid, and this plugin spends nothing.
- **No vendored content.** No layer prompt, template, scene, background, gradient, or media file is stored in this plugin or in the project beyond the one build's own rebuilt code and its downloaded media.
- **No frozen counts.** Never write the library's counts as fixed numbers in a build, a decision record, or a skill — read `llms.txt` live.
- **No unchanged layers.** Never ship a free trial layer as-is (see step 4).
- **No hotlinked media.** Never ship a production page that hotlinks GetLayers' storage bucket.
- **No generic fallback.** If no free layer fits the surface's job, say so in the decision record and build the surface from the design package instead — never force a mismatched layer, and never fall back to a generic centered stack.

## Files

- The live library: `https://getlayers.ai/` (categories: `/templates`, `/3d-scenes`, `/sections`, `/backgrounds`, `/gradients`).
- The live index: `https://getlayers.ai/llms.txt` (current counts, category links, key facts).
- Docs: `https://getlayers.ai/docs` (how a prompt differs from source, per-stack guidance).
- The AI design tools (`https://getlayers.ai/tools`) are free browser tools for making an effect (animated text, custom cursors, ASCII art, SVG to 3D, gradients, and more) — free to run, tune, copy, and download; use them to make an effect, not a page.
