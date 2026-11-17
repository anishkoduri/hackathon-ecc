#!/usr/bin/env python3
"""Fix #31 staged weave (coordinator tool, run once, NOT part of build.sh).

Edits STAGED sources only; they flow into the built tree through the STEP 2
copy (new-skills loop + orchestrate/rules copies). Every substitution asserts
its anchor occurs EXACTLY once and the script writes nothing on any failure.
The build-time assertions live in fix31.py (built-tree census + license
checks); the verifier is verify31.py.

Edits:
  W1. new-skills/orchestrate/SKILL.md — DESIGNPKG-AUTO paragraph: add the
      five new skills to the package list + the palette list + a gloss line.
  W2. new-rules/hackathon-mode.mdc — the IDENTICAL three insertions, so the
      DESIGNPKG-AUTO block stays byte-identical to orchestrate (fix #27).
  W3. new-skills/design-taste-frontend/SKILL.md — palette-first paragraph:
      add the five new skills to the design-package list.
  W4. new-skills/orchestrate/SKILL.md — inventory paragraph: add the fix #31
      additions to the enumeration.
  W5. new-skills/orchestrate/references/design-inventory.md — new §12 for
      the four resources + cross-pointers in §1 (GSAP presets) and §9
      (GSAP / React Bits library rows).
  W6. build.sh — add the five new skills to the new-skills loop.
"""
import os
import sys

ROOT = os.path.expanduser("~/workspace/hackathon-plugin")
ERRORS = []
CHANGES = []


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sub_once(text, old, new, where):
    n = text.count(old)
    if n != 1:
        ERRORS.append(f"{where}: anchor occurs {n} times, expected 1 :: {old[:70]!r}")
        return text
    CHANGES.append(f"{where}: substituted :: {old[:50]!r} ...")
    return text.replace(old, new)


NEW_SKILL_LIST = " / getlayers / gsap / react-bits / hairline-create / hairline-adopt"
NEW_GLOSS = (" `getlayers` — prompt-first cinematic layers (free set only; reference only, "
             "never vendored; restyled, never shipped unchanged) (fix #31, GETLAYERS_F31). "
             "`gsap` — timeline/scroll animation from the public npm package at build time, "
             "never vendored (fix #31, GSAP_F31). `react-bits` — animated React components "
             "installed fresh per project via CLI, never embedded (fix #31, REACTBITS_F31). "
             "`hairline-create` / `hairline-adopt` — interactive isometric SVG line figures, "
             "MIT (fix #31, HAIRLINE_F31).")
NEW_PALETTE = ("`motionsites-web-builder`, `getlayers`, `gsap`, `react-bits`, "
               "`hairline-create`, `hairline-adopt`, `ui-ux-pro-max`")

# ---------------------------------------------------------------- W1 + W2
# The DESIGNPKG-AUTO block is byte-identical in orchestrate + hackathon-mode;
# apply the identical three insertions to both files.
for rel in ("new-skills/orchestrate/SKILL.md", "new-rules/hackathon-mode.mdc"):
    t = read(rel)
    t = sub_once(
        t,
        "design-system / motionsites-web-builder, with the design-lead deciding which leads)",
        "design-system / motionsites-web-builder" + NEW_SKILL_LIST +
        ", with the design-lead deciding which leads)",
        rel + " W1/W2 package list")
    t = sub_once(
        t,
        "consulted, never a template) (fix #27, MOTIONSITES_F27).",
        "consulted, never a template) (fix #27, MOTIONSITES_F27)." + NEW_GLOSS,
        rel + " W1/W2 gloss")
    t = sub_once(
        t,
        "(`motionsites-web-builder`, `ui-ux-pro-max`, `less-flat-ui`, "
        "`motion-foundations`, `motion-patterns`, `motion-advanced`, "
        "`make-interfaces-feel-better`, `design-system`, the dealt Hallmark theme)",
        "(" + NEW_PALETTE + ", `less-flat-ui`, `motion-foundations`, "
        "`motion-patterns`, `motion-advanced`, `make-interfaces-feel-better`, "
        "`design-system`, the dealt Hallmark theme)",
        rel + " W1/W2 palette list")
    if not ERRORS:
        write(rel, t)

# ---------------------------------------------------------------- W3
rel = "new-skills/design-taste-frontend/SKILL.md"
t = read(rel)
t = sub_once(
    t,
    "the design package (`ui-ux-pro-max`, `less-flat-ui`, `motion-foundations`, "
    "`motion-patterns`, `motion-advanced`, `make-interfaces-feel-better`, "
    "`design-system`), and the dealt Hallmark theme",
    "the design package (`ui-ux-pro-max`, `less-flat-ui`, `motion-foundations`, "
    "`motion-patterns`, `motion-advanced`, `make-interfaces-feel-better`, "
    "`design-system`, `getlayers`, `gsap`, `react-bits`, `hairline-create`, "
    "`hairline-adopt`), and the dealt Hallmark theme",
    rel + " W3 palette list")
if not ERRORS:
    write(rel, t)

# ---------------------------------------------------------------- W4
rel = "new-skills/orchestrate/SKILL.md"
t = read(rel)
t = sub_once(
    t,
    "design-system, make-interfaces-feel-better, and the fix #22 additions",
    "design-system, make-interfaces-feel-better, the fix #31 additions "
    "(GetLayers prompt-first layers, GSAP animation, React Bits components, "
    "Hairline illustrations — see §12 of the inventory), and the fix #22 additions",
    rel + " W4 inventory enumeration")
if not ERRORS:
    write(rel, t)

# ---------------------------------------------------------------- W5
rel = "new-skills/orchestrate/references/design-inventory.md"
t = read(rel)
t = sub_once(
    t,
    "| GSAP presets — 17 | Ready GSAP snippets with trigger, duration, easing, framework notes, do/don't, performance notes | `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17) + `--domain gsap` | Motion on GSAP builds; ScrollTrigger is the scroll plugin (GSAP_F22) |",
    "| GSAP presets — 17 | Ready GSAP snippets with trigger, duration, easing, framework notes, do/don't, performance notes | `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17) + `--domain gsap` | Motion on GSAP builds; ScrollTrigger is the scroll plugin (GSAP_F22). Usage skill: `skills/gsap/SKILL.md` (fix #31) |",
    rel + " W5 §1 GSAP presets pointer")
t = sub_once(
    t,
    "(2) GSAP `gsap@3.15.1` (+ ScrollTrigger, all plugins);",
    "(2) GSAP `gsap@3.15.1` (+ ScrollTrigger, all plugins; usage skill `skills/gsap/SKILL.md`);",
    rel + " W5 §9 GSAP row")
t = sub_once(
    t,
    "(4) React Bits (commit `9d9c687…`, React/Next only);",
    "(4) React Bits (commit `9d9c687…`, React/Next only; usage skill `skills/react-bits/SKILL.md`);",
    rel + " W5 §9 React Bits row")
section12 = """
## 12. Fix #31 additions — GetLayers, GSAP, React Bits, Hairline illustrations

Home: `skills/getlayers/SKILL.md`, `skills/gsap/SKILL.md`,
`skills/react-bits/SKILL.md`, `skills/hairline-create/SKILL.md`,
`skills/hairline-adopt/SKILL.md`. Staged home: `new-skills/` (same names).
All four resources are free-tier only; no paid plan is purchased for any of
them. Counts for GetLayers and React Bits drift weekly — this file freezes
no count for either; read the live library when you need the current numbers.

| Entry | What it is | Where it lives | Reach for it when |
|---|---|---|---|
| GetLayers — prompt-first cinematic layers (GETLAYERS_F31) | A curated library of visual layers for cinematic marketing sites: page templates, real-time 3D WebGL scenes, animated sections, animated/static backgrounds, pointer-reactive gradients. Every layer copies as one self-contained prompt an agent rebuilds in the stack. FREE SET ONLY; the MCP requires the Full Stack Lifetime plan and is NOT wired; the plugin vendors NO GetLayers content (reference only); a layer is a foundation, never shipped unchanged | `skills/getlayers/SKILL.md`; live library `https://getlayers.ai/`; live index `https://getlayers.ai/llms.txt` (current counts + category links) | A cinematic hero, animated ground, real-time 3D scene, or gradient ground on a marketing surface; a section whose motion is already designed. Never app UI; never a mismatched layer forced onto a surface |
| GSAP — timeline / scroll / canvas animation (GSAP_F31) | Framework-agnostic JavaScript animation engine: tweens, timelines, ScrollTrigger, MotionPath, MorphSVG, DrawSVG, and every former Club plugin, 100% free for commercial use from the public npm package. NOT OSI open source (Webflow "Standard no charge" licence; bans competing no-code animation builders). Pin `gsap@3.15.1`; install from npm at build time, never vendor source. Official MIT agent skills (`github.com/greensock/gsap-skills`, 8 skills) are the deep API reference | `skills/gsap/SKILL.md`; presets in `skills/ui-ux-pro-max/data/motion.csv` (rows 1–17); pin + stack scope in `skills/ui-ux-pro-max/SKILL.md` (§11, GSAP_F22) | Hero entrance choreography, scroll-linked sections, staggered reveals, canvas/SVG animation. Not a component library; not smooth scrolling alone (Lenis); not a CSS-only micro-interaction |
| React Bits — animated React components (REACTBITS_F31) | Animated React components (text effects, backgrounds, interactive UI, ready-made blocks) that install as source you own, copy-and-own like shadcn/ui. Four variants per component: JS-CSS, JS-TW, TS-CSS, TS-TW. MIT + Commons Clause (may NOT sell, sublicense, or redistribute the components). This skill is a catalog + install guide — NO component source is embedded anywhere in the plugin | `skills/react-bits/SKILL.md`; live catalog `https://reactbits.dev/`; install guide `https://reactbits.dev/get-started/installation`; reviewed baseline commit `9d9c687…` (fix #22 §11) | An animated component on a React/Next.js build, installed fresh per project via `npx shadcn@latest add @react-bits/<Component>-<JS\\|TS>-<CSS\\|TW>`. Never on a non-React build; never with stock defaults on a themed build |
| Hairline illustrations — interactive isometric SVG line figures (HAIRLINE_F31) | 33 interactive isometric SVG line figures that answer the pointer (Terrain, Turntable, Keyboard, Terminal, Branches, Vault, Router, Loupe, Sieve, and more). Zero runtime dependencies, ESM-only; React 18+ an optional peer. MIT (Lucas Marques). Install per project: `npm i @lucasmarkes/hairline@0.5.1` or `npx shadcn@latest add https://hairline.lucasmarkes.com/r/hairline.json`. Two skills: `hairline-create` draws a new figure from an idea; `hairline-adopt` rebuilds an existing SVG as a figure. NOT Hairline UI (hairlineui.com) — a different product, not in scope | `skills/hairline-create/SKILL.md` + `skills/hairline-adopt/SKILL.md` (vendored MIT copies); live figures `https://hairline.lucasmarkes.com` | Hero art, section illustration, or a thoughtfully designed empty state on dev-tool sites, technical docs, landing pages, portfolios. Best at 160–240px for empty states; figures fill the parent's width at a 5:4 aspect ratio |

"""
t = sub_once(
    t,
    "## How the record uses this file (the ambition bar, AMBITION_F23)",
    section12.strip("\n") + "\n\n## How the record uses this file (the ambition bar, AMBITION_F23)",
    rel + " W5 §12 insert")
if not ERRORS:
    write(rel, t)

# ---------------------------------------------------------------- W6
rel = "build.sh"
t = read(rel)
t = sub_once(
    t,
    "for s in grill-me feature-expansion integration design-taste-frontend codebase-memory motionsites-web-builder; do",
    "for s in grill-me feature-expansion integration design-taste-frontend codebase-memory motionsites-web-builder getlayers gsap react-bits hairline-create hairline-adopt; do",
    rel + " W6 new-skills loop")
if not ERRORS:
    write(rel, t)

if ERRORS:
    print("WEAVE FAILED — nothing was written for the failed files:")
    for e in ERRORS:
        print("  ERROR: " + e)
    sys.exit(1)
print("WEAVE OK:")
for c in CHANGES:
    print("  " + c)
