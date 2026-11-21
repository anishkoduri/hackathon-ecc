#!/usr/bin/env python3
"""Fix #35 — design-layer parity with the factory variant (round 14 +
amendment, DECISION-F-191..F-196), regular side.

Run by build.sh as a patch step (after fix34.py, before STEP 5):
    python3 "$PLUGIN_ROOT/fix35/fix35.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. The kitchen skill and every staged
weave edit are staged sources (stage35.py + weave35.py run by the
coordinator before the build; kitchen flows through the STEP 2 loop).
This script:
  1. Asserts the pre-state census (counts 76 + kitchen staged = 77,
     MODELSEL pin census from the fix #33 post-state, README at 76,
     trigger coverage 76/48) and that the staged weave landed in the
     built copies (canonical DESIGNPKG-AUTO, Taste parity edits,
     getlayers layer role, citation renumber).
  2. Rewrites skills/orchestrate/references/design-inventory.md to the
     factory's normalized content (D35-5: ALL inventory edits run here,
     because fix34.py asserts the old §13/§14/§15 headers earlier in
     the same build): preamble, §0 layer map, Type-row Fraunces rule,
     §10 cross-note, §12 layer roles + Kitchen row, §13 MotionSites,
     §14/§15 headers in the factory's literal "Factory round N" forms,
     §16 code-mode with the F-193 verbatim-adoption lines.
  3. Replaces browser-qa's MOTION-QA + CONTRACT-QA paragraphs with the
     factory wording (provenance re-cited "(fix #35, ...)") and adds
     the scripted-evidence paragraph + Evidence report line.
  4. Rewrites the README count lines 76 -> 77, adds the fix #35
     provenance note, and sets trigger coverage.skills to 77 (no new
     trigger key — the fix #31 design-skill precedent).
  5. Generates manifests/design-parity.json (the parity normalizer is
     embedded below; it reproduces the factory's published manifest)
     and asserts every normalized hash equals the factory's value.
  6. Post-asserts the port: excluded factory machinery absent (with
     the D35-8 needle-pinned allowlist for the two inventory lines
     that name orchestrator-briefing), the deploy-fast Netlify pricing
     row byte-untouched, DESIGNPKG-AUTO byte-identical in orchestrate
     + hackathon-mode, pin census unchanged.

Exits non-zero on any error so the build fails rather than shipping a
half-synced tree. Patch log: fix35/fix35-patch-log.md (it records the
decisions D35-1..D35-8 and Anish's Nov 20, 2026 approval to run the
build machinery).

SPEC: fix35/SPEC.md + fix35/BLOCKER-canonical-vs-fix32-scan.md.
Counts: skills 76 -> 77, agents 45, rules 48, commands 55, hooks 15,
trigger keys 48 (unchanged).
"""
import hashlib
import json
import os
import re
import sys

PLUGIN_DIR = os.path.abspath(sys.argv[1])
PLUGIN_ROOT = os.path.dirname(PLUGIN_DIR)
ERRORS = []
CHANGES = []
OWED = []

def p(*parts):
    return os.path.join(PLUGIN_DIR, *parts)

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def sub(path, old, new, label):
    text = read(path)
    n = text.count(old)
    if n != 1:
        ERRORS.append(f"{label}: needle found {n}x (expected 1) in {os.path.relpath(path, PLUGIN_DIR)}")
        return
    write(path, text.replace(old, new))
    CHANGES.append(f"{label}: {os.path.relpath(path, PLUGIN_DIR)}")

def insert_after(path, anchor, block, label):
    text = read(path)
    n = text.count(anchor)
    if n != 1:
        ERRORS.append(f"{label}: anchor found {n}x (expected 1) in {os.path.relpath(path, PLUGIN_DIR)}")
        return
    write(path, text.replace(anchor, anchor + block))
    CHANGES.append(f"{label}: {os.path.relpath(path, PLUGIN_DIR)}")

def insert_before(path, anchor, block, label):
    text = read(path)
    n = text.count(anchor)
    if n != 1:
        ERRORS.append(f"{label}: anchor found {n}x (expected 1) in {os.path.relpath(path, PLUGIN_DIR)}")
        return
    write(path, text.replace(anchor, block + anchor))
    CHANGES.append(f"{label}: {os.path.relpath(path, PLUGIN_DIR)}")

def walk_text_files():
    for root, dirs, files in os.walk(PLUGIN_DIR):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                with open(fp, encoding="utf-8") as f:
                    yield fp, f.read()
            except (UnicodeDecodeError, OSError):
                continue

def census(token):
    return sum(text.count(token) for _, text in walk_text_files())

# ---------------------------------------------------------------- 1. Pre-state census
skills = sorted(d for d in os.listdir(p("skills")) if os.path.isdir(p("skills", d)))
agents = [f for f in os.listdir(p("agents")) if f.endswith(".md")]
rules = [f for f in os.listdir(p("rules")) if f.endswith(".mdc")]
commands = [f for f in os.listdir(p("commands")) if f.endswith(".md")]
if len(skills) != 77:
    ERRORS.append(f"census: built skills = {len(skills)} (expected 77)")
if "kitchen" not in skills:
    ERRORS.append("census: kitchen missing from built tree (STEP 2 loop / stage35)")
if len(agents) != 45:
    ERRORS.append(f"census: built agents = {len(agents)} (expected 45)")
if len(rules) != 48:
    ERRORS.append(f"census: built rules = {len(rules)} (expected 48)")
if len(commands) != 55:
    ERRORS.append(f"census: built commands = {len(commands)} (expected 55)")
CHANGES.append(f"census: counts skills 77 (76 + kitchen), agents {len(agents)}, rules {len(rules)}, commands {len(commands)}")

PIN_CENSUS = {"grok-4.7-high": 0, "Grok 4.7 High": 2, "grok-4.7-extra-high": 0,
              "Grok 4.7 Extra High": 0, "cursor-grok-4.6-high-fast": 72}
for token, expected in PIN_CENSUS.items():
    got = census(token)
    if got != expected:
        ERRORS.append(f"census: pin census drift: {token!r} x{got} (expected x{expected}, fix #33 post-state)")
CHANGES.append("census: MODELSEL pin census holds at the fix #33 post-state")

_readme = read(p("README.md"))
for line in ["76 skills, 45 agents, 48 rules, and 55 commands in",
             "76 skills widen the routing surface",
             "56 MB and 76 skills against a minimal set",
             "structured process — 76 skills, 45 agents, 55 comm"]:
    if line not in _readme:
        ERRORS.append(f"census: README pre-state line missing: {line!r}")
_man = read(p("manifests/context-packs/skill-triggers@1.json"))
if '"skills": 76,' not in _man or json.loads(_man).get("coverage") != {"skills": 76, "withTriggers": 48}:
    ERRORS.append("census: trigger coverage pre-state is not {skills: 76, withTriggers: 48}")
CHANGES.append("census: README at 76 in all 4 count lines; trigger coverage 76/48")

CANONICAL_PAREN = "(design-taste-frontend / ui-ux-pro-max / less-flat-ui / polish-pass / motion-foundations / motion-patterns / motion-advanced / make-interfaces-feel-better / design-system / motionsites-web-builder / kitchen / motion-principles / threeui / getlayers / gsap / react-bits / hairline-create / hairline-adopt, with the design-lead deciding which leads)"
WEAVE_NEEDLES = [
    ("skills/kitchen/SKILL.md", "**Hackathon-ecc note (fix #35, KITCHEN_F35).**"),
    ("skills/orchestrate/SKILL.md", CANONICAL_PAREN),
    ("rules/hackathon-mode.mdc", CANONICAL_PAREN),
    ("skills/orchestrate/SKILL.md", "`kitchen` — dqnamo's Kitchen, 15 copy-paste tactile components, ISC, copied from the page per project, never embedded (fix #35, KITCHEN_F35)."),
    ("skills/orchestrate/SKILL.md", "dqnamo's Kitchen tactile components (fix #35 — §12), and MotionSites cinematic components (fix #27 — §13)"),
    ("skills/orchestrate/SKILL.md", "the fix #34 motion/3D layer (§14: `motion-principles` principles + guardrails, `threeui` free-Community 3D components)"),
    ("skills/orchestrate/SKILL.md", "motion work — + `make-interfaces-feel-better` + `motion-principles`; 3D work — + `threeui`;"),
    ("skills/orchestrate/SKILL.md", "scope → `prebuild-research` (step 1.5) → `feature-expansion` Phases 0–3 (automatic, right after the research step —"),
    ("skills/design-taste-frontend/SKILL.md", "`hairline-create`, `hairline-adopt`, `kitchen`), and the dealt Hallmark theme"),
    ("skills/design-taste-frontend/SKILL.md", "A Kitchen piece whose motion breaks a Taste house rule (no tilt, no carousel, no timed tabs — house rule 5)"),
    ("skills/design-taste-frontend/SKILL.md", "Fraunces role rule: Fraunces is body-only as the Tiempos stand-in (fix #19 F4)"),
    ("skills/design-taste-frontend/SKILL.md", "GSAP 3D transforms (§11; usage skill `skills/gsap/SKILL.md`, inventory §12)"),
    ("skills/design-taste-frontend/SKILL.md", "`system.md` Type — Fraunces body-only as the Tiempos stand-in, fix #19 F4; see the F4/F5 scope rules below)"),
    ("skills/design-taste-frontend/SKILL.md", "React Bits / Kitchen supply the animated component or tactile piece where the widget needs one"),
    ("skills/design-taste-frontend/SKILL.md", "tokens.) **The design contract — the frozen system issued as a contract (fix #34, DESIGNCONTRACT_F34).**"),
    ("skills/design-taste-frontend/SKILL.md", "`flat by choice — <reason>`.)\n\nIf the project has no landing page"),
    ("skills/design-taste-frontend/SKILL.md", "Colors: none — the principles do not choose colours.)\n\n- **Theme-match precondition:**"),
    ("skills/getlayers/SKILL.md", "**Layer role: foundation** (inventory `skills/orchestrate/references/design-inventory.md` §12)"),
    ("skills/motion-principles/SKILL.md", "design-inventory.md` §14)"),
    ("skills/threeui/SKILL.md", "design-inventory.md` §14)"),
    ("skills/prebuild-research/SKILL.md", "design-inventory.md` §15)"),
]
for rel, needle in WEAVE_NEEDLES:
    if needle not in read(p(rel)):
        ERRORS.append(f"census: staged weave needle missing in built {rel}: {needle[:60]!r}")
CHANGES.append(f"census: staged weave landed ({len(WEAVE_NEEDLES)} needles across 8 built files)")

_inv_pre = read(p("skills/orchestrate/references/design-inventory.md"))
for header in ["## 13. Fix #34 additions — Motion Principles, ThreeUI",
               "## 14. Fix #34 additions — Pre-build Research, the Design Contract",
               "## 15. code-mode — the execution discipline (fix #34, CODEMODE_F34)"]:
    if header not in _inv_pre:
        ERRORS.append(f"census: inventory pre-state header missing (fix35 edits start from it): {header!r}")
if "## 0. One system" in _inv_pre or "KITCHEN_F35" in _inv_pre:
    ERRORS.append("census: inventory already carries fix #35 edits (double-run?)")
CHANGES.append("census: inventory at the fix #34 state (§13/§14/§15 headers) — fix35 edits start here")

_bqa_pre = read(p("skills/browser-qa/SKILL.md"))
for header in ["**Motion verdict (fix #34, MOTION-QA_F34).**", "**Contract verdict (fix #34, CONTRACT-QA_F34).**"]:
    if _bqa_pre.count(header) != 1:
        ERRORS.append(f"census: browser-qa pre-state header count != 1: {header!r}")
if "Scripted evidence collection" in _bqa_pre:
    ERRORS.append("census: browser-qa already carries the scripted-evidence paragraph (double-run?)")
CHANGES.append("census: browser-qa at the fix #34 state (both verdicts present once, no scripted-evidence paragraph)")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 2. Inventory parity rewrite
INV = p("skills/orchestrate/references/design-inventory.md")

sub(INV, "verified by reading the actual files (Nov 12, 2026); where a skill's own\nheader claim and its data file disagree, both numbers are given and the data\nfile is the inventory source.",
         "verified by reading the actual files (Nov 12, 2026); where a skill's header\nclaim and its data file disagree, both numbers are given and the data file\ngoverns.",
         "inventory preamble (factory wording)")

S0_BLOCK = '## 0. One system — the layer map\n\nThe sections below are ONE design system, not a menu of alternatives: every\nbuild reads this file as layers, in consultation order, and the direction\ncites each layer USED or CONSIDERED-AND-REJECTED with a D19 reason (see "How\nthe record uses this file" below). No layer replaces another.\n\n| Layer | Role | Source | Inventory |\n|---|---|---|---|\n| Foundation | The cinematic ground the direction leans on — consulted FIRST | GetLayers prompt-first layers (free set only) | §12 |\n| Direction | The dealt theme and the page system that leads the build | Hallmark theme deal (§3); Taste leads full site builds (§2) | §2, §3 |\n| Intelligence | General design intelligence — styles, palettes, pairings, guidelines, icons, charts, stacks | ui-ux-pro-max | §1 |\n| Components | Animated components and cinematic component sources | React Bits (§12); MotionSites (§13); daisyUI (§8, §9); ThreeUI (§14) — ready-made 3D components | §12, §13, §8, §14 |\n| Motion | The motion engine behind the motion system | GSAP (§12) driving the motion tokens and principles (§6); motion-principles (§14) — the why layer the principles are dealt from | §12, §6, §14 |\n| Texture | The not-flat surface treatment | less-flat-ui, all 23 treatments | §5 |\n| Illustrations | Interactive line figures for hero art, sections, empty states | Hairline (§12) | §12 |\n| Tactile | One memorable physical-metaphor interaction per surface, at most | dqnamo\'s Kitchen (§12) | §12 |\n| Floor | The craft floor, slop checks, and finish reviews that bind every layer | Impeccable (§4); polish-pass (§7); design-system + make-interfaces-feel-better (§8) | §4, §7, §8 |\n\nGetLayers never replaces the dealt theme; GSAP never supplies components;\nReact Bits never supplies motion direction; a Kitchen piece never stands in\nfor the component system; less-flat-ui never textures a surface the page\nsystem already styles (Taste texture boundary). A design decision that names\nno layer is a decision with no inventory citation — route it back here or\nrecord it as a gap.'
insert_before(INV, "## 1. ui-ux-pro-max — lookup-only inventory for dashboards, apps, components (fix #32: no longer the design lead)",
              S0_BLOCK + "\n\n", "inventory §0 layer map inserted")

sub(INV, "| Type — 39 pairings | Type catalogue (json), incl. the `fraunces` pairing (display Fraunces, Figtree body) |",
         "| Type — 39 pairings | Type catalogue (json), incl. the `fraunces` pairing (display Fraunces, Figtree body). Fraunces role rule: Fraunces is body-only as the Tiempos stand-in (fix #19 F4, fix #20 scope) — never a display face where it is the body face; the pairing's display-Fraunces use is governed by fix #19 F3 / fix #20 F5 — never both roles on one build |",
         "inventory Type row Fraunces role rule")

sub(INV, "Cross-note: this section duplicates §1/§2/§3/§4 entries — those sections govern; §10 is a quick index only.",
         "Cross-note: this section is NOT a second catalog — the one catalog is §§1–9 plus §12–§13, and this section only re-indexes §1/§2/§3/§4 entries for quick lookup; those sections govern, and where this index and a governing section disagree, the governing section wins.",
         "inventory §10 cross-note (factory wording)")

sub(INV, "`skills/hairline-adopt/SKILL.md`. Staged home: `new-skills/` (same names).\nAll four resources are free-tier only;",
         "`skills/hairline-adopt/SKILL.md`, `skills/kitchen/SKILL.md` (fix #35, KITCHEN_F35). Staged home: `new-skills/` (same names).\nAll five resources are free-tier only;",
         "inventory §12 home para gains kitchen")

sub(INV, "no count for either; read the live library when you need the current numbers.\nGetLayers prompts carry the most weight in the palette-first flow — they are\nconsulted FIRST, before the other palette sources, and the direction leans on\nthem heavily as its foundation (see the skill).",
         "no count for either; read the live library for current numbers.\nGetLayers prompts carry the most weight in the palette-first flow — consulted\nFIRST, before the other palette sources; the direction leans on them heavily\nas its foundation (see the skill).",
         "inventory §12 GetLayers weight sentence (factory wording)")

sub(INV, "| GetLayers — prompt-first cinematic layers (GETLAYERS_F31) | A curated library of visual layers",
         "| GetLayers — prompt-first cinematic layers (GETLAYERS_F31) | **Layer role: foundation** — the first layer of the one design system, consulted FIRST. Curated visual layers",
         "inventory §12 GetLayers row layer role")
sub(INV, "| GSAP — timeline / scroll / canvas animation (GSAP_F31) | Framework-agnostic JavaScript animation engine",
         "| GSAP — timeline / scroll / canvas animation (GSAP_F31) | **Layer role: motion** — the motion engine of the one design system. Framework-agnostic JavaScript animation engine",
         "inventory §12 GSAP row layer role")
sub(INV, "| React Bits — animated React components (REACTBITS_F31) | Animated React components",
         "| React Bits — animated React components (REACTBITS_F31) | **Layer role: animated components** — the component layer of the one design system. Animated React components",
         "inventory §12 React Bits row layer role")
sub(INV, "| Hairline illustrations — interactive isometric SVG line figures (HAIRLINE_F31) | 33 interactive isometric SVG line figures",
         "| Hairline illustrations — interactive isometric SVG line figures (HAIRLINE_F31) | **Layer role: illustrations** — the illustration layer of the one design system. 33 interactive isometric SVG line figures",
         "inventory §12 Hairline row layer role")
sub(INV, "figures fill the parent's width at a 5:4 aspect ratio |",
         "figures fill the parent's width at a 5:4 aspect ratio. Never a photorealistic or filled illustration; never a traced copy of a source SVG — adopt rebuilds the object as solids |",
         "inventory §12 Hairline row tail (factory wording)")

KITCHEN_ROW = '| dqnamo\'s Kitchen — tactile copy-paste components (KITCHEN_F35, fix #35) | **Layer role: tactile** — the tactile layer of the one design system: one memorable physical-metaphor interaction per surface, at most. 15 free component experiments by dqnamo (London design engineer): Tactile Button, Scramble Text, Receipt Printer, Cassette Audio Player, Hold to Confirm, Magnetic Drop Zone, Dynamic Button, Playing Cards, Ticket, Stamp, Scroll Fade List, Advanced Model Selector, Animated Signature, Logo Trace Loader, Iridescent Foil. Each ships with its own code on its page — copy and paste directly into the project. ISC (verified Nov 17, 2026 from the repo\'s `package.json`, commit `0a517fea`; no LICENSE file, no copyright line published; `"private": true` — copy-paste, not an npm package). This skill is a catalog + copy guide — NO component source is embedded anywhere in the plugin; every copy keeps the dqnamo attribution + ISC notice | `skills/kitchen/SKILL.md`; live Kitchen `https://www.dqnamo.com/kitchen`; source repo `https://github.com/dqnamo/website` (`components/`, catalog `components/experiment-catalog.ts`); second channel 21st.dev (sparklines, logo-trace loaders, scramble text; shadcn install) | One memorable tactile interaction per surface — the checkout that prints a receipt, the delete that must not fire by accident, the loader that draws itself, the button that feels physical. Never a general component library (no forms, layout, or data display); never more than one Kitchen piece per surface; never on a non-React build except as a re-implemented pattern |'
_inv_now = read(INV)
_hairline_row = [l for l in _inv_now.split("\n") if l.startswith("| Hairline illustrations")]
if len(_hairline_row) != 1:
    ERRORS.append("inventory: Hairline row not found exactly once for the Kitchen row insert")
else:
    insert_after(INV, _hairline_row[0], "\n" + KITCHEN_ROW, "inventory §12 Kitchen row inserted")

S13_BLOCK = "## 13. MotionSites — cinematic component source (fix #27, MOTIONSITES_F27)\n\nHome: `skills/motionsites-web-builder/SKILL.md` + `skills/motionsites-web-builder/references/` (techniques, spec template, craft, assets, builders, review). Staged home: `new-skills/motionsites-web-builder/`. MIT (skill, references, scripts); the upstream `examples/` and `media/` folders are © MotionSites and are NOT shipped — fetched at use time, free sample only.\n\n| Entry | What it is | Where it lives | Reach for it when |\n|---|---|---|---|\n| MotionSites — cinematic components, motion patterns, hero treatments, media (MOTIONSITES_F27) | **Layer role: component source** — the cinematic components, motion patterns, hero treatments, and media the direction draws on, consulted, never a template. The 40 most-liked free MotionSites prompts (examples) + the media shelf (cinematic videos, transparent cut-outs) + the techniques index (signature effects with working code) + the spec template and review rubric. Taste still leads; browser-qa still owns every pass/fail screen verdict. FREE SAMPLE ONLY — never the paid MotionSites Unlimited library, never a paid service; the upstream sponsor/upsell block is stripped and never appended to a delivery | `skills/motionsites-web-builder/SKILL.md`; examples index + media shelf fetched at use time from upstream (raw GitHub URLs in the skill's steps 2–3); techniques in `skills/motionsites-web-builder/references/techniques/` | A cinematic component, motion pattern, hero treatment, or piece of media the build needs and no inventoried skill supplies — cited in the direction as USED or CONSIDERED-AND-REJECTED with a D19 reason, like every inventory entry. Never a template to copy wholesale (never its brand names, copy, or exact layouts); never premium/paid content; never the design source — the direction is generated through the package, MotionSites informs it |"
sub(INV, "## 13. Fix #34 additions — Motion Principles, ThreeUI",
         S13_BLOCK + "\n\n## 14. Factory round 10 additions — Motion Principles, ThreeUI",
         "inventory §13 MotionSites inserted; §14 header takes the factory's literal form")

sub(INV, "Staged home: `new-skills/` (same names). Fix #34 (ported from the\nfactory variant's round 10).",
         "Staged home: `new-skills/` (same names). Factory round 10\n(DECISION-F-35/F-35).",
         "inventory §14 intro provenance")
sub(INV, "(same as MotionSites,\nGSAP, React Bits).",
         "(same as MotionSites,\nGSAP, React Bits, Kitchen).",
         "inventory §14 trigger-key sentence gains Kitchen")

sub(INV, "## 14. Fix #34 additions — Pre-build Research, the Design Contract",
         "## 15. Factory round 11 additions — Pre-build Research, the Design Contract",
         "inventory §15 header takes the factory's literal form")
sub(INV, "— the fix #31 design-skill precedent).",
         "— the fix #31 design-skill precedent). The factory variant routes the same invocation through `orchestrator-briefing` (not ported; fix #34).",
         "inventory §15 Home line: factory-routing clause appended (D35-8 allowlist line 1)")
sub(INV, "the pre-build restatement gate checks the implementer's read-back against it before the build;",
         "the pre-build restatement gate checks the implementer's read-back against it before dispatch;",
         "inventory §15 contract row: factory's 'before dispatch'")

sub(INV, "## 15. code-mode — the execution discipline (fix #34, CODEMODE_F34)",
         "## 16. code-mode — the execution discipline (fix #34, CODEMODE_F34; inventory entry added fix #35, DECISION-F-35)",
         "inventory §16 header")
sub(INV, "is catalogued here for the same reason §14 catalogues the pipeline steps:\nthe inventory is the one place a reader can find every named capability the\nplugin carries.",
         "is catalogued here for the same reason §15 catalogues the pipeline steps:\nthe inventory is the one place a reader can find every named capability the\nfactory carries, and leaving the round-12 discipline out made its absence\nread as an oversight (round 12 recorded it as deliberately not adopted,\nDECISION-F-35; round 13 reverses that call — the inclusion logic of §15\nalready covers non-design pipeline artifacts).",
         "inventory §16 intro (factory history adopted verbatim, F-193; DECISION-F-35)")
sub(INV, "  a verdict, or a subagent's work (subagents do not run these scripts). It\n  carries no trigger key by design: `orchestrate` and `browser-qa` invoke\n  it by name (the routing decision is recorded in fix34/SPEC.md).",
         "  a verdict, or a subagent's work (subagents do not run these scripts; the factory's drone exclusion is this clause's origin). It carries no\n  trigger key by design: `orchestrate`, and — in the factory variant — `orchestrator-briefing` §6, and\n  `browser-qa` invoke it by name (the routing decision is recorded in SPEC\n  DECISION-F-35).",
         "inventory §16 bullet tail (D35-8 allowlist line 2)")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 3. browser-qa factory wording
BQA = p("skills/browser-qa/SKILL.md")
MOTION_NEW = "**Motion verdict (fix #35, MOTION-QA_F34).** In the visual loop, judge the build's motion against the checkable subset of `motion-principles` (MOTIONPRINCIPLES_F34), from the rendered interface, never from source: (a) **Doherty response** — every driven input shows visible feedback within 400ms (a press state, an optimistic update, or a skeleton; measure the interaction, do not eyeball it); (b) **timing ceiling** — UI animations (entrances, exits, hovers, state changes) run under 300ms, except motion recorded in the decision record as the content itself (a dealt hero moment, a scroll-scrubbed sequence); (c) **origin awareness** — menus, popovers, and expansions grow from their trigger, not from an arbitrary center; (d) **interruptibility** — a second input mid-animation cancels or retargets from the current position; it never locks the user out and never snaps back to the start; (e) **frequency-of-use restraint** — the surface's most-used actions carry the least motion; a daily action wrapped in a long animation FAILS this criterion however good it looks once; (f) **reduced-motion fallback** — under `prefers-reduced-motion: reduce`, animation is off or replaced by its still and the content is fully visible at rest. A failure on any criterion is a motion finding (minor at least) routed to the design skill that dealt the motion; an interaction the harness cannot drive is recorded as unverified, never as passed. This verdict is `browser-qa`'s alone, like the hero and memorability verdicts: `motion-principles` names what good motion is; this skill alone judges whether the built screen has it."
CONTRACT_NEW = "**Contract verdict (fix #35, CONTRACT-QA_F34).** Where a design contract exists (`docs/design-contract.md`, DESIGNCONTRACT_F34), judge the built screens AGAINST it, field by field, from the rendered interface: (a) **palette tokens** — the colours on screen are the contract's token values (sample the rendered output; a near-miss hex is a mismatch, not a pass); (b) **type scale** — headings and body render at the contract's faces, sizes, weights, and line-heights; (c) **spacing scale** — the layout rhythm follows the contract's spacing tokens and grid; (d) **motion specs** — the motion on screen matches the contract's values (the motion verdict above judges those values against the principles; this verdict judges the screen against the contract); (e) **components** — the contract's named components are the ones on screen, doing the jobs the contract assigns them; (f) **states** — the loading / empty / success / error states exist and match the contract where the harness can drive them. A value on screen that is not the contract's value, with no deviation recorded in the contract's Deviations field, is a contract finding (minor at least) routed to the implementer of that slice; a value covered by a recorded deviation is verified against the deviation, not the original value. A restatement mismatch that reaches this verdict means the pre-build gate was skipped — record that as a finding against the run, not just the slice. This verdict is `browser-qa`'s alone: the contract names the standard; this skill alone judges whether the built screen meets it."
SCRIPTED_NEW = "**Scripted evidence collection (fix #35, SCRIPT-FIRST_F34).** The mechanical gathering under these verdicts — DOM and screenshot inventories, coverage-matrix measurements, console and network log digests — may be collected by ONE gated orchestrator script written against the `code-mode` helpers (CODEMODE_F34): the script returns counts and exceptions under the 500 E3 distilled cap, its raw output stays in `.hackathon/script-output/`, and the gate record (SCRIPT-GATE_F34) sits in the run ledger. The script's output is EVIDENCE, never a verdict: every row of the QA report below is judged by this skill from that evidence, exactly as when the gathering was done by hand. A verdict the script appears to have decided is a finding against the run, not a result."

def replace_span(path, start_marker, end_marker, new_text, label):
    text = read(path)
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        ERRORS.append(f"{label}: span markers not unique in {os.path.relpath(path, PLUGIN_DIR)}")
        return
    i = text.find(start_marker)
    j = text.find(end_marker) + len(end_marker)
    if j <= i:
        ERRORS.append(f"{label}: span end precedes start")
        return
    write(path, text[:i] + new_text + text[j:])
    CHANGES.append(f"{label}: {os.path.relpath(path, PLUGIN_DIR)}")

replace_span(BQA, "**Motion verdict (fix #34, MOTION-QA_F34).**",
             "this skill alone judges whether the built screen has it.",
             MOTION_NEW, "browser-qa MOTION-QA paragraph (factory wording)")
replace_span(BQA, "**Contract verdict (fix #34, CONTRACT-QA_F34).**",
             "this skill alone judges whether the built screen honours it.",
             CONTRACT_NEW, "browser-qa CONTRACT-QA paragraph (factory wording)")
insert_after(BQA, CONTRACT_NEW, "\n\n" + SCRIPTED_NEW, "browser-qa scripted-evidence paragraph")
insert_after(BQA, "- [✓/✗] Contract (CONTRACT-QA_F34): palette tokens exact; type scale exact; spacing scale followed; motion matches the contract's specs; named components present; states match; every mismatch covered by a recorded deviation",
             "\n- Evidence: mechanical collection scripted where used (SCRIPT-FIRST_F34) — the script name, its gate record, and its raw-output file are named in the run ledger; verdicts above are this skill's alone",
             "browser-qa Evidence report line")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 4. README + trigger coverage
sub(p("README.md"), "76 skills, 45 agents, 48 rules, and 55 commands in",
    "77 skills, 45 agents, 48 rules, and 55 commands in", "README count line 1")
sub(p("README.md"), "76 skills widen the routing surface",
    "77 skills widen the routing surface", "README count line 2")
sub(p("README.md"), "56 MB and 76 skills against a minimal set",
    "56 MB and 77 skills against a minimal set", "README count line 3")
sub(p("README.md"), "structured process — 76 skills, 45 agents, 55 comm",
    "structured process — 77 skills, 45 agents, 55 comm", "README count line 4")
NOTE35 = "- **Fix #35 design parity (Nov 20, 2026)** — the design layer is synced with the factory variant (its round 14 + amendment): `kitchen` (dqnamo's Kitchen — 15 tactile copy-paste components, ISC, copied from the page per project, never embedded) joins the design package as the tactile layer; the design inventory gains the §0 layer map, §12 layer roles, and the §13 MotionSites section, with the fix #34 sections renumbered to §14–§16; `browser-qa`'s motion + contract verdicts take the factory wording and gain scripted evidence collection; both verifiers now assert the design-parity manifest (`manifests/design-parity.json`). Skills are now 77. (`KITCHEN_F35`)\n"
_readme = read(p("README.md"))
_anchor = "- **Fix #34 factory port (Nov 19, 2026)**"
if _readme.count(_anchor) != 1:
    ERRORS.append("README: fix #34 note anchor not found exactly once")
else:
    write(p("README.md"), _readme.replace(_anchor, NOTE35 + _anchor))
    CHANGES.append("README: fix #35 provenance note added before the fix #34 note")
sub(p("manifests/context-packs/skill-triggers@1.json"), '"skills": 76,', '"skills": 77,',
    "trigger coverage.skills 76 -> 77")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 5. Parity manifest
_DROP_TOKENS = ("drone", "openrouter", "cm_dispatch", "cursor-agent",
                "orchestrator-briefing")

def normalize(text):
    """The factory's DECISION-F-192 normalization, byte-for-byte (factory
    fix-round14.py _norm == its verifier §30 _norm14): drop `model:`
    lines and lines mentioning the drone machinery (case-sensitive
    substring), then reduce provenance markers, rule IDs, decision
    numbers and DECISION ids to placeholders — substitutions applied to
    the joined text, F-\\d+ BEFORE the DECISION rule (that order is what
    renders DECISION-F-170 as DECISION-X#)."""
    lines = []
    for line in text.split("\n"):
        if line.startswith("model:"):
            continue
        if any(tok in line for tok in _DROP_TOKENS):
            continue
        lines.append(line)
    t = "\n".join(lines)
    t = re.sub(r"factory round \d+", "SRC", t)
    t = re.sub(r"fix #\d+[a-z]?", "SRC", t)
    t = re.sub(r"Fix #\d+", "SRC", t)
    t = re.sub(r"_F\d+", "_F#", t)
    t = re.sub(r"F-\d+", "F-#", t)
    t = re.sub(r"DECISION-[A-Z]+-?\d*", "DECISION-X", t)
    return t

PARITY_FILES = [
    "skills/browser-qa/SKILL.md",
    "skills/design-taste-frontend/SKILL.md",
    "skills/getlayers/SKILL.md",
    "skills/kitchen/SKILL.md",
    "skills/motion-principles/SKILL.md",
    "skills/orchestrate/references/design-inventory.md",
    "skills/threeui/SKILL.md",
    "skills/ui-ux-pro-max/SKILL.md",
]
PARITY_TARGETS = {
    "skills/browser-qa/SKILL.md": "e4a7bc7bfa0ad52d54c439ad6876427b19143f2096e0560f287746bfed8f06cb",
    "skills/design-taste-frontend/SKILL.md": "1bd2356e5d05462dc44959f8f886644632fa4ae323a1a29052dd81b7fe142973",
    "skills/getlayers/SKILL.md": "dda55d470eb0161a6fd3d5986b0117620395c11f505f84116d68717e5fc19161",
    "skills/kitchen/SKILL.md": "503ff11a80293be1cd8a0fec65ebbfc1552f3efd3f57119402ca6845151cf302",
    "skills/motion-principles/SKILL.md": "265dfd75ef22b653ff156ce9aa229153779e670813d4749e174a152be9030b43",
    "skills/orchestrate/references/design-inventory.md": "8360e40d5910789da5c4822c6ec8a5878bfe6ed3dc24642b3e5562230d3cddb0",
    "skills/threeui/SKILL.md": "af031ecd8f4ed378efcf909dc8d7c9a7e8f7dbceafc756a706a0bd49794b6af5",
    "skills/ui-ux-pro-max/SKILL.md": "37b2f213fcd5fd5e9a1373bc499156b6dd18b5fce03b59730107110cc0ad3d4e",
}
computed = {}
for rel in PARITY_FILES:
    computed[rel] = hashlib.sha256(normalize(read(p(rel))).encode("utf-8")).hexdigest()
    if computed[rel] != PARITY_TARGETS[rel]:
        ERRORS.append(f"parity: {rel} normalized hash {computed[rel]} != factory target {PARITY_TARGETS[rel]}")
if not ERRORS:
    manifest = json.dumps({"files": computed}, indent=2, sort_keys=True) + "\n"
    write(p("manifests/design-parity.json"), manifest)
    CHANGES.append("parity: manifests/design-parity.json written; all 8 normalized hashes equal the factory's published values")
    CHANGES.append(f"parity: design-parity.json sha256 = {hashlib.sha256(manifest.encode('utf-8')).hexdigest()}")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 6. Post-assertions
_readme = read(p("README.md"))
if "77 skills" not in _readme or "76 skills" in _readme:
    ERRORS.append("post: README count lines not fully at 77")
_man = json.loads(read(p("manifests/context-packs/skill-triggers@1.json")))
if _man.get("coverage") != {"skills": 77, "withTriggers": 48}:
    ERRORS.append(f"post: trigger coverage = {_man.get('coverage')} (expected 77/48)")
_bqa = read(p("skills/browser-qa/SKILL.md"))
for needle in ["**Motion verdict (fix #35, MOTION-QA_F34).**", "**Contract verdict (fix #35, CONTRACT-QA_F34).**",
               "**Scripted evidence collection (fix #35, SCRIPT-FIRST_F34).**",
               "- [✓/✗] Motion (MOTION-QA_F34):", "- [✓/✗] Contract (CONTRACT-QA_F34):",
               "- Evidence: mechanical collection scripted where used (SCRIPT-FIRST_F34)"]:
    if _bqa.count(needle) != 1:
        ERRORS.append(f"post: browser-qa needle count != 1: {needle[:50]!r}")
CHANGES.append("post: README 77 in all 4 lines; coverage 77/48; browser-qa carries both factory verdicts + scripted evidence + Evidence line")

_inv = read(INV)
for needle in ["## 0. One system — the layer map",
               "## 13. MotionSites — cinematic component source (fix #27, MOTIONSITES_F27)",
               "## 14. Factory round 10 additions — Motion Principles, ThreeUI",
               "## 15. Factory round 11 additions — Pre-build Research, the Design Contract",
               "## 16. code-mode — the execution discipline (fix #34, CODEMODE_F34; inventory entry added fix #35, DECISION-F-35)",
               "(KITCHEN_F35, fix #35)"]:
    if needle not in _inv:
        ERRORS.append(f"post: inventory needle missing: {needle[:60]!r}")
for gone in ["## 13. Fix #34 additions", "## 14. Fix #34 additions", "## 15. code-mode"]:
    if gone in _inv:
        ERRORS.append(f"post: inventory still carries the pre-parity header: {gone!r}")
CHANGES.append("post: inventory carries §0 + §13 + the factory-literal §14/§15 headers + §16; old headers gone")

for bad_dir in ["skills/orchestrator-briefing", "skills/openrouter-drones"]:
    if os.path.exists(p(bad_dir)):
        ERRORS.append(f"post: excluded factory artifact present: {bad_dir}")
drone_agents = [f for f in agents if f.startswith("drone-")]
if drone_agents:
    ERRORS.append(f"post: drone agents present: {drone_agents}")
FACTORY_ID_RE = re.compile(r"\b(?:MOTIONPRINCIPLES|THREEUI|MOTION-QA|CONTRACT-QA|DESIGNCONTRACT|RESEARCHBRIEF|HOSTING|CODEMODE|SCRIPT-FIRST|SCRIPT-GATE|KITCHEN)_F1\d\d\b|\bKITCHEN_F32\b")
EXCLUDED_STRINGS = ["CLI-DISPATCH_F32", "CAPTIVATION_F32", "PARALLEL-CALLS_F154", "openrouter-drones", "cm_dispatch"]
INV_REL = "skills/orchestrate/references/design-inventory.md"
ALLOW_FRAGMENTS = ["routes the same invocation through `orchestrator-briefing`",
                   "`orchestrator-briefing` §6"]
for fp, text in walk_text_files():
    rel = os.path.relpath(fp, PLUGIN_DIR)
    if FACTORY_ID_RE.search(text):
        ERRORS.append(f"post: factory-numbered rule ID survives in {rel}")
    for s in EXCLUDED_STRINGS:
        if s in text:
            ERRORS.append(f"post: excluded string {s!r} present in {rel}")
    if "orchestrator-briefing" in text:
        if rel != INV_REL:
            ERRORS.append(f"post: 'orchestrator-briefing' present outside the D35-8 allowlist: {rel}")
        else:
            lines = [l for l in text.split("\n") if "orchestrator-briefing" in l]
            if len(lines) != 2 or not all(any(f in l for f in ALLOW_FRAGMENTS) for l in lines):
                ERRORS.append("post: inventory 'orchestrator-briefing' occurrences are not exactly the two D35-8 allowlisted lines")
CHANGES.append("post: no excluded machinery (briefing/drones/cm_dispatch/factory IDs) anywhere in the built tree, except the two D35-8 allowlisted inventory lines")

PRICING_ROW = "| **Netlify** | Static front ends | 300 credits/mo | — | **15 credits per production deploy**, so about 20 deploys uses up the month (the 300-credit model applies to accounts created since Sep 4, 2025; older accounts keep prior limits) |"
if PRICING_ROW not in read(p("skills/deploy-fast/SKILL.md")):
    ERRORS.append("post: deploy-fast Netlify pricing row altered (its touch-up is dated Dec 4, 2026 — not this fix)")
CHANGES.append("post: deploy-fast Netlify pricing row byte-untouched")

def designpkg_block(text):
    m = re.search(r"\*\*DESIGNPKG-AUTO.*?(?=This is the design half of BIND)", text, re.S)
    return m.group(0) if m else None
if designpkg_block(read(p("skills/orchestrate/SKILL.md"))) != designpkg_block(read(p("rules/hackathon-mode.mdc"))):
    ERRORS.append("post: DESIGNPKG-AUTO blocks differ between orchestrate and hackathon-mode")
CHANGES.append("post: DESIGNPKG-AUTO byte-identical in orchestrate + hackathon-mode, canonical decision-B parenthetical in both")

for token, expected in PIN_CENSUS.items():
    got = census(token)
    if got != expected:
        ERRORS.append(f"post: pin census drift after writes: {token!r} x{got} (expected x{expected})")
CHANGES.append("post: MODELSEL pin census unchanged by the fix #35 writes")

OWED.append("OWED-35-1 (call map): the call map is generator-owned and NOT regenerated by the build — fix35.py does not assert it. The coordinator regenerates it after the build (fix28/callmap/generate_call_map.py, EXPECTED skills 76 -> 77 — the EXPECTED bump is part of weave35) and rebuilds so the staged copy flows into the built tree; verify35.py asserts the regenerated map (kitchen called; uncalled set unchanged).")
OWED.append("OWED-35-2 (live use): kitchen routing, the layer map, and the scripted-evidence discipline are file-level rules; whether Cursor runs them as written is decided by live project use (the fix #30 live-test pattern), not by this build.")
OWED.append("OWED-35-3 (factory side): the factory's round-14 amendment (decision B geometry + R-7 wording) is committed on the factory side at 4f82e38 and its bundle regenerated (hackathon-ecc-factory-round14.bundle, 91,200,859 bytes); the parity targets asserted here are the amended manifest values. Nothing in this fix pushes or uploads either tree.")

DECISIONS = [
    "DECISION-35-1 (D35-1, role decisions): where the two trees' role decisions conflicted, the REGULAR tree's decisions win (ui-ux-pro-max stays lookup-only; Taste leads); where content was richer in the factory (the inventory catalog, browser-qa wording), the factory's content wins. Pins and drone machinery are untouched in both trees.",
    "DECISION-35-2 (D35-2, numbering): the factory's inventory section numbering wins — MotionSites takes §13 and the fix #34 sections renumber to §14/§15/§16; the §14/§15 headers carry the factory's literal 'Factory round N' forms (capital F is outside the parity normalization, so the literal form is what parity requires).",
    "DECISION-35-3 (D35-3, browser-qa): the factory's stricter MOTION-QA / CONTRACT-QA wording wins; provenance is re-cited '(fix #35, ...)' in the regular tree (the _F34 ID stems are unchanged).",
    "DECISION-35-4 (D35-4, IDs): the only new rule ID is KITCHEN_F35; ported IDs keep their _F34 forms; the ported decision cites in the inventory use the stem DECISION-F-35 (see D35-10 for why the hyphenated F form is required).",
    "DECISION-35-5 (D35-5, build-time inventory): ALL inventory edits run at build time in fix35.py, because fix34.py asserts the old §13/§14/§15 inventory headers earlier in the same build; the staged inventory keeps the fix #34 state.",
    "DECISION-35-6 (D35-6, canonical parenthetical — Anish's decision B): the canonical DESIGNPKG-AUTO parenthetical is '(design-taste-frontend / ui-ux-pro-max / less-flat-ui / polish-pass / motion-foundations / motion-patterns / motion-advanced / make-interfaces-feel-better / design-system / motionsites-web-builder / kitchen / motion-principles / threeui / getlayers / gsap / react-bits / hairline-create / hairline-adopt, with the design-lead deciding which leads)'; fix32.py is NOT edited (its lead scan passes on this geometry). The Taste palette-first list keeps kitchen LAST per the SPEC (it scans clean).",
    "DECISION-35-7 (D35-7, A9 placement): fix #34 placed Taste's motion bullet after a blank line where the factory carries it directly under the depth D19 line; weave35 A9 (apply-a9.py) moves the blank line to after the bullet — a placement-only correction inside the parity file.",
    "DECISION-35-8 (D35-8, exclusion allowlist): verify35's factory-exclusion census (and fix35.py's post-assertion) carries a needle-pinned allowlist for exactly two lines in skills/orchestrate/references/design-inventory.md — the §15 Home line's factory-routing clause and the §16 bullet's factory-variant clause — the only 'orchestrator-briefing' occurrences fix #35 intentionally introduces (they are what makes those lines drop under the parity normalization, as the factory's own lines do). Any other occurrence is a defect.",
    "DECISION-35-10 (D35-10, defect found at build run 2): the inventory's ported decision cites were first written DECISION-D35, which the factory's DECISION-F-192 normalization renders 'DECISION-X' — but the factory's own DECISION-F-170 renders 'DECISION-X#', because the F-\\d+ substitution runs BEFORE the DECISION rule and eats the hyphenated number first. Parity therefore requires the hyphenated form on the regular side too: the cites are DECISION-F-35 (and DECISION-F-35/F-35 in §14). The pre-fix35 census normalizer also differed from the factory's in two smaller ways (case-insensitive drop test; per-line substitution); fix35.py and verify35.py now embed the factory's _norm byte-for-byte.",
    "DECISION-35-9 (D35-9, defect found at build run 1): fix34.py's pre-state census asserts exactly 76 built skills, but kitchen is a staged skill and flows through the STEP 2 loop before fix34.py runs, so the built tree already carries 77 at that census and the build stopped there. Amended fix34.py's census 76 -> 77 (with an in-file D35-9 comment and its census CHANGES line updated); no other fix34 assertion changed — its README/coverage pre- and post-states are unaffected because fix35.py runs after it. Same pattern as fix #33 amending fix24.py's stale anchor. fix32.py is NOT edited (per the task).",
    "APPROVAL (recorded): Anish approved in plain words on Fri Nov 20, 2026, 21:02 CT: 'go ahead and run the build machinery' — build.sh, its fix scripts, hooks-bearing content, the verifier, and git operations in the scratch-repo, in both plugin trees. This fix ran under that approval. No push to GitHub and no upload was made or is authorized by it.",
]

log = ["# fix35 patch log", "", "## Decisions", ""]
log += [f"- {d}" for d in DECISIONS]
log += ["", "## Changes", ""]
log += [f"- {c}" for c in CHANGES]
if OWED:
    log += ["", "## OWED", ""] + [f"- {o}" for o in OWED]
if ERRORS:
    log += ["", "## ERRORS", ""] + [f"- {e}" for e in ERRORS]
write(os.path.join(PLUGIN_ROOT, "fix35", "fix35-patch-log.md"), "\n".join(log) + "\n")

if ERRORS:
    for e in ERRORS:
        print(f"fix35: ERROR {e}")
    print(f"fix35: {len(ERRORS)} ERROR(S)")
    sys.exit(1)
print(f"fix35: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix35: {len(OWED)} OWED item(s) recorded in the patch log")
print("fix35: OK")
