# Fix #31 (DRAFT SPEC) — Design-library additions: GetLayers, GSAP, React Bits, Hairline illustrations

**Status:** DRAFT spec, written Nov 16, 2026. Starts after fix #30 lands (sequence: #29 adaptability → #30 model routing → #31 this fix). Do not start while #29 or #30 runs (two agents must never edit the plugin tree at once).

## Decision (Anish, Nov 16, 2026)

Add four design resources to the plugin's palette-first inventory, all free-tier only, no paid plans purchased:

1. **GetLayers** (getlayers.ai, Textura) — FREE SET ONLY.
2. **GSAP** (gsap.com, GreenSock/Webflow).
3. **React Bits** (reactbits.dev, DavidHDev/react-bits).
4. **Hairline illustrations** (Lucas Marques, @lucasmarkes/hairline).

## What each is (verified Nov 16, 2026)

### GetLayers — free set only
- Library of hand-designed visual "layers" for cinematic marketing sites. At review: 50 page templates, 114 real-time 3D WebGL scenes, 10 animated sections, 276 backgrounds, 1,088 pointer-reactive gradients. Counts drift (new layers weekly) — do NOT freeze counts in the plugin. **Correction Nov 17, 2026 (fix #31): the live counts already drifted one day after review — `llms.txt` reads 62 templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088 gradients. The skill carries NO counts; read `llms.txt` live.**
- Each layer copies as one long prompt an agent rebuilds in the stack. Five categories: Templates, 3D Scenes, Sections, Backgrounds, Gradients.
- Agent channels: published skill at `storage.getlayers.ai/skill/getlayers/SKILL.md`, `llms.txt`, prompts. MCP at `https://mcp.getlayers.ai/mcp` requires Full Stack Lifetime — NOT available on the free set, so the plugin must NOT wire the MCP. Use the skill/prompts path only. **Correction Nov 17, 2026 (audit #97-A1): the SPEC's ($199) was wrong — the live pricing page lists Full Stack Lifetime at $249 ($499 struck through; $199 is Unlimited Plus). The skill carries no price (prices drift like counts).**
- **License (hard constraint):** may not scrape, redistribute, or resell the library; bulk/automated copying gets accounts restricted. The plugin must NOT vendor any GetLayers content. Reference only.
- **Guardrail:** a layer is a foundation, not a finished brand. Restyle copy, palette, and subject matter. Do NOT ship free trial layers unchanged.
- **Weight (direction update, Anish Nov 16, 2026 ~10:02 PM CT):** GetLayers prompts carry MORE WEIGHT in the design skill — a first-class, high-priority source in the palette-first flow, not a minor or optional entry. The design-lead consults the GetLayers prompts early (FIRST, alongside or ahead of the other palette sources), and the direction leans on GetLayers layers heavily as the foundation. The weight is visible in ordering (GetLayers first in every palette list), explicit priority language in the skill, and a check that the design direction cites the GetLayers layers USED or CONSIDERED-AND-REJECTED with a D19 reason (same as every inventory entry). Constraints unchanged: free set only, no vendored content, foundation not finished brand.

### GSAP — GreenSock Animation Platform
- Framework-agnostic JavaScript animation engine. Version ~~3.15.0 (Apr 2026)~~ **3.15.1 (npm latest, verified Nov 17, 2026 — the SPEC's 3.15.0 was already superseded; the skill pins `gsap@3.15.1`, matching the inventory's existing pin)**. Free, including every former Club plugin (SplitText, ScrollTrigger, MorphSVG, DrawSVG, ScrollSmoother, Inertia, MotionPathHelper, CustomEase), commercial use included, from the public `gsap` npm package. No Club paywall, no private registry.
- **License (hard constraint):** NOT OSI open source. Custom Webflow "Standard no charge" license; IP stays with Webflow; bans use in no-code visual animation builders competing with Webflow; Webflow can terminate at discretion. The plugin must install GSAP from npm at build time and must NOT vendor or redistribute its source.
- Official MIT agent skills: `github.com/greensock/gsap-skills` (8 skills: core, timeline, scrolltrigger, plugins, utils, react, performance, frameworks). Use as reference.
- Note: GSAP has no opinion about React/Next.js — it needs a client boundary in Next.js builds. It is the timeline/scroll/canvas specialist; it is not a component library.

### React Bits
- Free library of 200+ animated React components (text effects, backgrounds, interactive UI, ready-made blocks), copy-and-own like shadcn/ui. Four variants per component: JS-CSS, JS-TW, TS-CSS, TS-TW. Count drifts weekly — do NOT freeze counts in the plugin.
- Install fresh per-project via shadcn/jsrepo CLI. Official Vue/Svelte ports exist (vue-bits.dev, sveltebits.xyz). Main library is React-only.
- **License (hard constraint):** MIT + Commons Clause. Free for personal and commercial use. May NOT sell, sublicense, or redistribute the components themselves — alone, bundled, or ported. The plugin's skill must be a catalog + install guide (lookup, not embedded source). Install components at time of use via CLI. Do NOT store component source in the skill or the plugin.
- Community skills exist as reference (verify against the live repo before borrowing structure; do not copy wholesale).

### Hairline illustrations — Lucas Marques
- MIT-licensed open-source library of 33 interactive isometric SVG line figures that respond to the visitor's pointer (Terrain, Turntable, Keyboard, Terminal, Branches, Vault, Router, Loupe, Sieve, etc.). Covers interfaces, data, machines, devices, coding, security, connectivity, empty states.
- Zero runtime dependencies, ESM-only, 63.5 kB gzipped for the full set. React 18+ or plain JS/anything with a DOM. Importing one figure carries only that figure into the bundle. Figures fill the parent's width at a 5:4 aspect ratio.
- Install: `npm i @lucasmarkes/hairline`; shadcn integration: `npx shadcn@latest add https://hairline.lucasmarkes.com/r/hairline.json`.
- Two coding-agent skills: `hairline-create` (generate a new figure from an idea) and `hairline-adopt` (convert an existing SVG into the same line style). Include both as reference.
- Best for: dev-tool sites, technical docs, landing pages, portfolios, thoughtfully designed empty states. NOT Hairline UI (hairlineui.com) — that is a different product and was explicitly not picked.

## Scope

- Add one skill (or inventory entry) per resource, following the MotionSites/Animaster pattern from fix #27: what it is, when to use it, how to reach for it, license constraints, what NOT to do.
- Weave all four into the palette-first design flow (fix #27): the designer inventories available components/designs first (MotionSites, Animaster, GetLayers, GSAP, React Bits, Hairline illustrations, the existing design package), bases the design on that palette, tailors, then builds. Add all four to the single inventory catalog (fix #23).
- Update the verifier with checks for the new skills/references + license checks (no vendored GetLayers content, no embedded React Bits component source, no vendored GSAP source in the built tree); add `verify31.py` following the fix #27 pattern.
- Do NOT change: model pins (fix #30), the adaptability routing (fix #29), the debloat from #28, the design package, grill-me. Do NOT purchase any paid plan (GetLayers Unlimited/Full Stack, Hairline UI templates, React Bits Pro) — free tiers only.
- Constraints: author Anish Koduri <akoduri05@gmail.com> only, NO `Co-authored-by: Cursor` trailer, no AI tool as contributor/author; build.sh is the source of truth; staged sources only; never re-run fix11/fix11-stage.py; fix dirs stay; do NOT push (create a verified git bundle for the Windows pull).

## Verification

- Audit loop (at least 2 rounds) + sweep + dry-run, with HONEST verdicts: record NOT MET as written if the final audit or sweep carries a minor fixed post-hoc without a re-audit/re-sweep, per the fix #27 convention.
- The dry-run must include a design leg: a build whose design pass inventories the new sources and uses at least one item from each where the brief calls for it (or records why a source was correctly skipped), verifying the palette-first routing picks them when relevant.
- License checks in verify31: no GetLayers library content vendored, no React Bits `.tsx`/`.jsx`/`.css` source embedded, no GSAP source vendored; counts for GetLayers/React Bits are NOT hardcoded (they drift).

## Open items

- GetLayers free-set contents change over time; the skill should point at the live library and `llms.txt`, not a frozen list.
- React Bits component count grows weekly; same rule — point at the live catalog.
- Hairline UI (hairlineui.com) is a different product and is NOT in scope. If Anish later wants its free components, that is a separate decision.
