#!/usr/bin/env python3
"""verify23.py -- checks fix #23 in the BUILT tree (read-only).

Run after a build: python3 fix23/verify23.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc (+ build.sh
where the SPEC says so):
  1. SS1 Ambition + THE INVENTORY + THE CORE: INVENTORY_F23 present in
     orchestrate SKILL.md + references/design-inventory.md (the inventory
     file exists in the built tree and covers every required group --
     spot-checked entry per group against the actual skill files);
     AMBITION_F23 (used vs considered-and-rejected, small-slice fails,
     F6 primary gate); MEMORABLE_F23 (memorability above F6 -- impressive
     is the floor, memorable is the bar; over-the-top is ambition/impact
     not loudness; browser-qa judges memorability as the top criterion).
     Inventory counts spot-verified against the actual files -- including
     the styles.csv count (89 rows; fix #25 §4(a) corrected the header
     from 80 to 89 searchable styles, 51 active, with this assertion
     updated in the same change; the csv remains the inventory source).
  2. SS2 Motion: MOTION_F23 in orchestrate + the three motion skills +
     make-interfaces-feel-better + ui-ux-pro-max (motion default,
     static-feel fails, token-routed, reduced-motion fallback complete).
  3. SS3 Fonts: TYPEAUDIT_F23 in polish-pass (typeset + slop-checklist +
     SKILL.md) with the exact thresholds T1a (body <=40% build share),
     T1b (<=55% per primary screen), T1c (display/important >=25%),
     T1d (hero display > body), T2 (trio re-deal), T3 (variety floor
     max(3, ceil(N/20)), each face >=5%); TRIO_F23; F7VAR_F23 in
     ui-ux-pro-max; browser-qa type verdict (BQA-TYPEAUDIT);
     orch-build-mvp record checks (ORCH-TYPEAUDIT). D19_RULE text NOT
     rewritten: the fix19 verbatim text is still byte-identical in the
     built tree (imported from fix19/fix19.py, the same source verify19
     asserts) and the diff vs build.sh.before-fix23 is additions only.
  4. SS4 Hero: HERO_F23 in Taste SKILL.md + Picks Hero-moment row +
     Hallmark hero review + browser-qa hero verdict (HERO-BQA_F23); the
     app home/feed calibration and the never-a-generic-hero-section rule.
  5. SS5 Functionality: FUNC_F23 in Taste + FUNC-DIAG_F23 in diagrams.md
     + browser-qa functionality verdict (FUNC-BQA_F23) + ui-ux-pro-max
     pointer (FUNC-UIPRO_F23); F2 stack labels unchanged (covered, no
     edit -- F2_RULE still verbatim in Taste).
  6. SS6 Alignment: ALIGN_F23 in polish-pass reference/alignment.md +
     SKILL.md pointer + browser-qa assertions (ALIGN_F23-A--E);
     COVER_F23 (three widths 1440 / 768-1100 / 390 + every flow state);
     BLOCK_F23 (unverified width/state = NOT shippable, blocking).
  7. SS9 Dynamic: DYNAMIC_F23 in the three motion skills + browser-qa
     live check (DYNAMIC-BQA-01/02) + orchestrate + polish-pass; the
     SS9-vs-SS2 distinction stated (presence vs state-change /
     interactivity).
  8. Global: build.sh fingerprint (24,059 lines, md5 df2cb850...); diff
     vs build.sh.before-fix23 is additions only (+285/-0); counts
     166/72/123/87/15, trigger keys 64; banned terms 0 in the built tree
     (case-insensitive, excl. node_modules); Grok pins only (bare
     grok-4.6-high-fast absent); /demo gates intact -- DEMOGATE tokens
     present at every site, zero "demo" mentions inside the fix23
     build.sh blocks, no new auto-invocation wording; the narration-key
     prompt fires ONLY when the user asked for a demo video.
  9. Prior-verifier regression leg: fix15/17/18/19/20/21/22 re-run.
     EXPECTED fails are ONLY: the frozen post-fix21 build.sh fingerprint
     line(s), the post-fix22 build.sh fingerprint line (fix22's verifier
     newly fails on it -- it expects 23,774 lines / md5 4799a819...),
     the less-flat-ui diff-hunk pattern (6 hunks), and cascades of
     those. Any fail outside that pattern is a REAL regression.
 10. Manifest check (fix22 pattern): runs once fix23/MANIFEST.md exists
     -- FAILS until the manifest worker writes it. Reported separately
     as owed, not as a pass.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
sys.path.insert(0, os.path.join(PLUGIN, "fix19"))
from fix19 import D19_RULE, F2_RULE  # noqa: E402

BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


def lines_with(token, text):
    return sum(1 for ln in text.splitlines() if token in ln)


def csv_rows(rel):
    with open(os.path.join(BASE, rel), encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # minus the header row


# --- tree-wide _F23 token census (line counts + occurrences, grep-style:
# literal substring counts, the same metric the disposition uses) ---
TREE_DIRS = ("skills", "agents", "commands", "rules", "hooks")
_TOKENS = ("INVENTORY_F23", "AMBITION_F23", "MOTION_F23", "TYPEAUDIT_F23",
           "TRIO_F23", "F7VAR_F23", "HERO_F23", "FUNC_F23", "FUNC-DIAG_F23",
           "HERO-BQA_F23", "FUNC-BQA_F23", "FUNC-UIPRO_F23", "ALIGN_F23",
           "COVER_F23", "BLOCK_F23", "DYNAMIC_F23", "MEMORABLE_F23")
_token_lines = Counter()
_token_occ = Counter()
for _d in TREE_DIRS:
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [d for d in _dirs if d != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            for _tok in _TOKENS:
                if _tok in _t:
                    _token_occ[_tok] += _t.count(_tok)
                    _token_lines[_tok] += sum(
                        1 for _ln in _t.splitlines() if _tok in _ln)
TREE_DIRS = ("skills", "agents", "commands", "rules", "hooks")
_files_with_f23 = set()
for _d in TREE_DIRS:
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [d for d in _dirs if d != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            if "_F23" in _t:
                _files_with_f23.add(os.path.relpath(_p, BASE))

mf = read("skills/motion-foundations/SKILL.md")
mp = read("skills/motion-patterns/SKILL.md")
ma = read("skills/motion-advanced/SKILL.md")
mifb = read("skills/make-interfaces-feel-better/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
qr = read("skills/ui-ux-pro-max/references/quick-reference.md")
taste = read("skills/design-taste-frontend/SKILL.md")
orch = read("skills/orchestrate/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
bqa = read("skills/browser-qa/SKILL.md")
obm = read("skills/orch-build-mvp/SKILL.md")
ocf = read("skills/orch-change-feature/SKILL.md")
hm = read("rules/hackathon-mode.mdc")
slop = read("skills/polish-pass/reference/slop-checklist.md")
unslop = read("skills/polish-pass/reference/unslop-fixes.md")
typeset = read("skills/polish-pass/reference/lenses/typeset.md")
align = read("skills/polish-pass/reference/alignment.md")
diag = read("skills/design-taste-frontend/references/diagrams.md")
hero_rev = read("skills/design-taste-frontend/references/hallmark/references/review-hero.md")
inv = read("skills/orchestrate/references/design-inventory.md")
disp = read("skills/orchestrate/references/dispatch-prompt.md")
ds = read("skills/design-system/SKILL.md")
pitch = read("skills/pitch-deck-video/SKILL.md")
lessflat = read("skills/less-flat-ui/SKILL.md")
vercel = read("skills/polish-pass/reference/vercel-checklist.md")
glossary = read("skills/design-taste-frontend/references/design-glossary.md")
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()

# 1. SS1 Ambition + THE INVENTORY + THE CORE.
check("INVENTORY_F23: 4 lines in the built tree",
      _token_lines["INVENTORY_F23"] == 4)
check("INVENTORY_F23 in orchestrate SKILL.md + dispatch-prompt + design-inventory.md",
      "INVENTORY_F23" in orch and "INVENTORY_F23" in disp
      and "INVENTORY_F23" in inv)
check("inventory file exists in the built tree",
      os.path.isfile(os.path.join(
          BASE, "skills/orchestrate/references/design-inventory.md")))
check("inventory covers SS1 groups 1-10",
      all(f"## {n}." in inv for n in range(1, 11)))
check("inventory currency rule: future fixes update it in the same change",
      "kept current" in inv
      and "updates it in the same change" in inv)
check("inventory usage rule: record cites USED vs CONSIDERED-AND-REJECTED",
      "How the record uses this file" in inv
      and "CONSIDERED-AND-REJECTED" in inv
      and "AMBITION_F23" in inv)
check("orchestrate: inventory READ at the design-package step BEFORE deciding",
      "READ `references/design-inventory.md`" in orch
      and "BEFORE deciding" in orch)
check("dispatch-prompt references the inventory (INVENTORY_F23)",
      "design-inventory.md" in disp)
check("AMBITION_F23: 6 lines / 7 occurrences in the built tree",
      _token_lines["AMBITION_F23"] == 6 and _token_occ["AMBITION_F23"] == 7)
check("ambition: design package records USED vs CONSIDERED-AND-REJECTED",
      "RECORDS which inventory elements were USED" in orch
      and "CONSIDERED-AND-REJECTED" in orch)
check("ambition: blanket 'we considered everything' is not a reason, fails",
      '"we considered everything" is not a reason and fails the bar' in orch)
check("ambition: small slice without recorded specific reasons FAILS",
      "uses only a small slice of the available inventory" in orch
      and "FAILS the ambition bar" in orch)
check("ambition: design usable without the package fails",
      "could have been made without the package" in orch
      and "fails the ambition bar" in orch)
check("ambition: MORE elements, MORE motion, MORE decisions -- not louder",
      "Ambition is MORE elements, MORE motion, MORE decisions" in orch
      and '"More, not bolder" stands' in orch)
check("ambition: F6 is the PRIMARY gate in orchestrate step 3 + step-6 extension",
      "F6 (impressive is the governing bar) is the PRIMARY gate" in orch
      and "F6 is the PRIMARY gate (fix #23" in orch
      and "rule-correct but unambitious design fails" in orch)
# Inventory counts, re-derived from the actual files (not copied).
check("inventory ui-ux-pro-max styles: 89 csv rows (header 89, csv is source)",
      csv_rows("skills/ui-ux-pro-max/data/styles.csv") == 89
      and "89 searchable styles" in uipro
      and "89 rows in `data/styles.csv`" in inv
      and "89 searchable styles, 51 active" in inv
      and "the csv is the inventory source" in inv)
check("inventory ui-ux-pro-max palettes 192 / pairings 74 / guidelines 120 / icons 105",
      csv_rows("skills/ui-ux-pro-max/data/colors.csv") == 192
      and csv_rows("skills/ui-ux-pro-max/data/typography.csv") == 74
      and csv_rows("skills/ui-ux-pro-max/data/ux-guidelines.csv") == 120
      and csv_rows("skills/ui-ux-pro-max/data/icons.csv") == 105)
check("inventory ui-ux-pro-max GSAP presets 17 / chart types 25 / stacks 22",
      csv_rows("skills/ui-ux-pro-max/data/motion.csv") == 17
      and csv_rows("skills/ui-ux-pro-max/data/charts.csv") == 25
      and len([f for f in os.listdir(os.path.join(
          BASE, "skills/ui-ux-pro-max/data/stacks"))
          if f.endswith(".csv")]) == 22)
check("inventory ui-ux-pro-max app-interface 32 / landing 34 / products 192 rows",
      csv_rows("skills/ui-ux-pro-max/data/app-interface.csv") == 32
      and csv_rows("skills/ui-ux-pro-max/data/landing.csv") == 34
      and csv_rows("skills/ui-ux-pro-max/data/products.csv") == 192)
_moments = json.load(open(os.path.join(
    BASE, "skills/design-taste-frontend/assets/moments/index.json"),
    encoding="utf-8"))["moments"]
check("inventory Taste moments: 18 in the index, 13 dealt, 5 retired (kinds 4/4/1/7/2)",
      len(_moments) == 18
      and Counter(m["kind"] for m in _moments)
      == {"transition": 4, "text": 4, "hover": 1, "scroll": 7, "liquid": 2}
      and sum(1 for m in _moments if m.get("retired")) == 5)
check("inventory Taste palettes 64 / type 39 (json catalogs)",
      len(json.load(open(os.path.join(
          BASE, "skills/design-taste-frontend/library/palettes.json"),
          encoding="utf-8"))) == 64
      and len(json.load(open(os.path.join(
          BASE, "skills/design-taste-frontend/library/type.json"),
          encoding="utf-8"))) == 39)
_themes = json.load(open(os.path.join(
    BASE, "skills/design-taste-frontend/references/hallmark/references/themes/index.json"),
    encoding="utf-8"))["themes"]
_theme_files = [f for f in os.listdir(os.path.join(
    BASE, "skills/design-taste-frontend/references/hallmark/references/themes"))
    if f.endswith(".md") and f != "README.md"]
check("inventory Hallmark: 50 themes in index.json, 50 theme .md files (+ README)",
      len(_themes) == 50 and len(_theme_files) == 50)
check("inventory Hallmark sloplint scripts + hero/finish reviews exist",
      os.path.isfile(os.path.join(
          BASE, "skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs"))
      and os.path.isfile(os.path.join(
          BASE, "skills/design-taste-frontend/references/hallmark/references/review-hero.md"))
      and os.path.isfile(os.path.join(
          BASE, "skills/design-taste-frontend/references/hallmark/references/review-finish.md")))
check("inventory Impeccable: 62 detector rules in the json",
      len(json.load(open(os.path.join(
          BASE, "skills/polish-pass/reference/impeccable-detector-rules.json"),
          encoding="utf-8"))) == 62)
check("inventory Impeccable craft floor file exists",
      os.path.isfile(os.path.join(
          BASE, "skills/polish-pass/reference/craft-floor.md")))
check("inventory less-flat-ui: all 23 treatments present in the built copy",
      sum(1 for n in range(1, 24)
          if f"### {n}. " in lessflat) == 23
      and "## The 23 treatments" in lessflat)
check("inventory motion: principles A1-A12 + laws A13-A20 in motion-foundations",
      all(f"**A{n} " in mf for n in range(1, 13))
      and all(f"**A{n} " in mf for n in range(13, 21)))
check("inventory motion: B11-B19 rules in motion-patterns",
      all(f"{n}. **" in mp for n in range(11, 20)))
_ma_examples = ma.split("## Code Examples", 1)[1].split("\n## ", 1)[0]
check("inventory motion: 17 motion-advanced code examples",
      sum(1 for ln in _ma_examples.splitlines()
          if ln.startswith("### ")) == 17)
_c_ids = sorted(set(int(x) for x in re.findall(r"C(\d+) —", slop)))
_d_ids = sorted(set(int(x) for x in re.findall(r"D(\d+) —", unslop)))
check("inventory polish-pass: slop checklist C1-C20 (20 checks)",
      _c_ids == list(range(1, 21)))
check("inventory polish-pass: unslop fixes D1-D20 (20 fixes)",
      _d_ids == list(range(1, 21)))
_vercel_rules = vercel.split("## The rules", 1)[1].split("## Anti-patterns", 1)[0]
check("inventory polish-pass: Vercel 16 groups / 104 rules (pinned snapshot)",
      sum(1 for ln in _vercel_rules.splitlines()
          if ln.startswith("### ")) == 16
      and len(set(re.findall(r"V-[A-Z]+[0-9]+", vercel))) == 104)
check("inventory polish-pass: accent checks + one-WebGL rule + orb check + depth check",
      "ACCENT_F22" in slop and "ACCENTUATION_F22" in slop
      and "WEBGL_ONE_F22" in slop and "ORBS_F22" in slop
      and "DEPTH_F22" in slop)
check("inventory design-system: Modes 1-3 + daisyUI component menu",
      "Mode 1" in ds and "Mode 2" in ds and "Mode 3" in ds
      and "DAISYUI_F22" in ds)
check("inventory make-interfaces-feel-better: 9 core principles + motion set M1-M6",
      all(p in mifb for p in (
          "Concentric Radius", "Optical Alignment", "Shadows And Borders",
          "Text Wrapping", "Font Smoothing", "Image Outlines",
          "Transition Scope", "Hit Areas"))
      and "M1" in mifb and "M6" in mifb)
_g_ids = sorted(set(int(x) for x in re.findall(r"\| G(\d+) ", glossary)))
check("inventory fix22 glossary: 20 terms G1-G20",
      _g_ids == list(range(1, 21)))
check("inventory fix22 H1/H2 accents + Mobbin + direct-don't-describe named",
      "ACCENT_F22" in inv and "ACCENTUATION_F22" in inv
      and "MOBBIN_RESEARCH_F22" in inv and "DIRECTIVES_F22" in inv)
for _lib in ("Lenis", "GSAP", "Vanta", "React Bits", "react-three-fiber",
             "liquid-glass-js", "ShaderGradient", "liquid-logo", "Casberry",
             "OriginKit", "daisyUI"):
    check(f"inventory fix22 asset library/tool named: {_lib}", _lib in inv)
check("inventory fix22 running total: 11 libraries/tools (4+4+3)",
      "4 + §15's 4 + §17's 3 = 11" in uipro)
check("inventory fix22 Bang: 10 style directions + 19 opener concepts",
      "10 style directions" in inv and "19 opener concepts" in inv
      and "### Style-direction menu, 10" in pitch
      and "### Opener concepts, 19" in pitch)
check("inventory fix22 Depth tokens: perspective 1000, parallax, tilt 6, elevation",
      "perspective 1000" in inv and "parallax near 0.5" in inv
      and "tilt max 6" in inv and "elevation raised 8" in inv)
_orb_states = ("working", "searching", "solving", "listening", "connecting",
               "weaving", "composing", "breathing", "shaping")
check("inventory fix22 Thinking Orb: 9 states, no 'thinking' state",
      all(f"| `{s}` |" in mp for s in _orb_states)
      and "There is no `thinking` state in the library" in mp)
check("inventory fix22 daisyUI component count agrees with design-system + fix22/MANIFEST.md (68; the 65 in the §17 research count was corrected to the plugin's recorded 68)",
      "68 components" in inv
      and "68 components" in ds
      and "68 components" in open(os.path.join(
          PLUGIN, "fix22/MANIFEST.md"), encoding="utf-8").read())
_sections = [ln for ln in
             read("skills/design-taste-frontend/references/sections-library.md")
             .splitlines() if ln.startswith("## ")]
check("inventory Taste sections library: 45 recipes",
      len([h for h in _sections
           if h != "## What every recipe assumes"]) == 45)
check("inventory Taste backgrounds reference: 111 lines",
      len(read("skills/design-taste-frontend/references/backgrounds.md")
          .splitlines()) == 111)
# THE CORE.
check("MEMORABLE_F23: 4 lines / 5 occurrences in the built tree",
      _token_lines["MEMORABLE_F23"] == 4 and _token_occ["MEMORABLE_F23"] == 5)
check("CORE: memorable is the bar above F6, impressive is the floor",
      "Memorable is the bar" in orch
      and "impressive is the floor, memorable is the bar" in orch)
check("CORE: a build the user would forget the next day FAILS, however rule-correct",
      "a build the user would forget the next day FAILS, however rule-correct" in orch)
check("CORE: browser-qa judges memorability as the TOP criterion",
      "Browser-qa judges memorability as the TOP criterion" in orch
      and "browser-qa judges memorability as the TOP criterion" in bqa)
check("CORE: memorability is dynamic + over the top + wow / striking / stunning",
      "dynamic + over the top + wow + striking + stunning" in orch)
check("CORE: over the top is ambition/impact, not loudness; more-not-bolder governs",
      '"Over the top" is ambition and impact, not loudness for its own sake' in orch
      and "do not just crank weight, color, or size" in orch)
check("CORE: a build can be over the top and quiet in palette; cannot be forgettable",
      "a build can be over the top and quiet in palette" in orch
      and "it cannot be forgettable" in orch)
check("CORE: orchestrate cross-references AMBITION/MOTION/HERO/FUNC/DYNAMIC without restating",
      "The bars below answer to it without restating it" in orch)
check("CORE: browser-qa memorability verdict (MEMORABLE-BQA-01) + report row (MEMORABLE-BQA-02)",
      "Memorability verdict" in bqa
      and "- [✓/✗] Memorability (MEMORABLE_F23)" in bqa
      and "the build is memorable tomorrow, not merely correct today" in bqa)
check("CORE: memorability verdict is browser-qa's alone",
      "no other step judges memorability" in bqa)
check("CORE: polish-pass memorability candidates (MEMORABLE_F23 x2 on one line)",
      polish.splitlines()[100].count("MEMORABLE_F23") == 2
      and "a quiet-palette build with a strong moment is not flagged for being quiet" in polish)

# 2. SS2 Motion.
check("MOTION_F23: 9 lines / 10 occurrences in the built tree",
      _token_lines["MOTION_F23"] == 9 and _token_occ["MOTION_F23"] == 10)
for _name, _txt in (("motion-foundations", mf), ("motion-patterns", mp),
                    ("motion-advanced", ma),
                    ("make-interfaces-feel-better", mifb),
                    ("ui-ux-pro-max", uipro)):
    check(f"motion default in {_name} (MOTION_F23)",
          "MOTION_F23" in _txt)
    _mot_lines = [ln for ln in _txt.splitlines() if "MOTION_F23" in ln]
    check(f"motion default in {_name}: a build that feels static fails",
          any("feels static" in ln for ln in _mot_lines))
    check(f"motion default in {_name}: reduced-motion fallback carried",
          any("reduced-motion" in ln.lower() for ln in _mot_lines))
check("motion default in orchestrate (MOTION_F23)",
      "MOTION_F23" in orch)
check("motion routed through fix22 tokens (stagger 30ms, press scale 0.97, dropdowns 150-250ms)",
      "stagger 30ms" in mf and "press scale 0.97" in mf
      and "dropdowns 150" in mf and "250ms" in mf)
check("motion recorded with D19 reason + token values, directed per SS10",
      "Motion is the default, not an afterthought" in mf
      and any("D19" in ln
              for ln in mf.splitlines() if "MOTION_F23" in ln))
check("motion scope guard: Taste landing pages keep the scroll ban",
      "scroll ban" in mf)
check("motion sub-ids MOTION-01..05 each occur exactly once as a tuple in build.sh",
      all(build.count("('MOTION-0%d'," % n) == 1 for n in range(1, 6)))
check("motion sub-ids MOTION-01..05 occur 0x in the built tree (by design)",
      all(f"MOTION-0{n}" not in mf + mp + ma + mifb + uipro + orch + bqa
          for n in range(1, 6)))

# 3. SS3 Fonts.
check("TYPEAUDIT_F23: 14 lines / 18 occurrences in the built tree",
      _token_lines["TYPEAUDIT_F23"] == 14 and _token_occ["TYPEAUDIT_F23"] == 18)
check("type audit home in the typeset lens (TYPEAUDIT_F23)",
      "Type audit" in typeset and "TYPEAUDIT_F23" in typeset)
check("type audit measures visual share = size x visible characters per face",
      "Visual share" in typeset
      and "size" in typeset and "visible characters" in typeset)
check("type audit records distinct faces, per-face shares, trio-vs-previous-build",
      "records, per build, the distinct faces used" in typeset
      and "whether the trio matches the previous build's trio" in typeset)
check("T1a: body face <= 40% of build visual share",
      "T1a" in typeset and "40%" in typeset)
check("T1b: body face <= 55% on any single primary screen",
      "T1b" in typeset and "55%" in typeset)
check("T1c: display/important faces combined >= 25% of build visual share",
      "T1c" in typeset and "25%" in typeset)
check("T1d: on the hero/home surface, display share exceeds body share",
      "T1d" in typeset
      and "the display face's share exceeds the body face's share" in typeset)
check("T2: trio identical to the previous build's trio FAILS without a recorded reuse reason",
      "T2" in typeset
      and "identical to the previous build's trio" in typeset
      and "recorded reason for the reuse" in typeset)
check("T3: variety floor max(3, ceil(N/20)), each counted face >= 5% share",
      "T3" in typeset and "max(3, ceil(N/20))" in typeset
      and "5% of the build's visual share" in typeset)
check("type-audit clearance: T1a/T1b only by scoped exception, T1c still binding",
      "scoped exception" in typeset and "T1c still binds" in typeset)
check("type-audit clearance: T1c/T1d/T3 have no clearance",
      "T1c, T1d, and T3 have no clearance" in typeset)
check("type audit can FAIL a build: a hit with no clearance is a FAIL",
      "a hit with no recorded clearance is a FAIL" in typeset)
check("slop checklist carries the type-audit section with T1a-T3 + clearance",
      "## Type audit" in slop and "TYPEAUDIT_F23" in slop
      and "T1a" in slop and "T1b" in slop and "T1c" in slop
      and "T1d" in slop and "T2" in slop and "T3" in slop
      and "scoped exception" in slop)
check("polish-pass SKILL.md wires the type audit (non-negotiable 5 + harmony)",
      "TYPEAUDIT_F23" in polish)
check("browser-qa type-audit verdict (BQA-TYPEAUDIT): defaulted typography fails",
      "Type-audit verdict" in bqa and "TYPEAUDIT_F23" in bqa
      and "Typography that reads as defaulted fails here" in bqa
      and "is a distinctiveness finding (minor at least) that FAILS the build" in bqa)
check("browser-qa type verdict restates the thresholds (40/55/25/hero/variety)",
      "over 40% of the build's visual share" in bqa
      and "over 55% on any primary screen" in bqa
      and "under 25% of the build's visual share" in bqa
      and "max(3, ceil(N/20))" in bqa)
check("TRIO_F23: 1 line in the built tree (orchestrate design-package step)",
      _token_lines["TRIO_F23"] == 1 and "TRIO_F23" in orch)
check("orchestrate: Type list feeds the type audit, trio re-dealt per build",
      "the trio is re-dealt per build" in orch
      and "Type list is also the type-audit input" in orch)
check("F7VAR_F23: 2 lines in the built tree (ui-ux-pro-max + slop checklist)",
      _token_lines["F7VAR_F23"] == 2
      and "F7VAR_F23" in uipro and "F7VAR_F23" in slop)
check("F7 strengthened: variety across the build, trio is a pattern not a default",
      "F7 strengthened" in uipro
      and "the decision record must show VARIETY across the build" in uipro
      and 'is a pattern, not a default' in uipro)
check("orch-build-mvp fix23 static checks: type-audit table + trio line + variety floor",
      "Fix #23 static checks" in obm and "TYPEAUDIT_F23" in obm
      and "variety floor" in obm and "trio-vs-previous-build" in obm)
check("F4 stands: body face is long body text and small incidental text only",
      "is for long-length body text and small incidental text only" in typeset)
check("D19_RULE text NOT rewritten: fix19 verbatim text still in Taste + orchestrate",
      D19_RULE in taste and D19_RULE in orch)
check("D19 seventh-dimension extension line intact (fix22, not a rewrite)",
      "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in orch
      and "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in taste)
check("F2 stack labels unchanged: F2_RULE still verbatim in Taste (covered, no edit)",
      F2_RULE in taste)

# 4. SS4 Hero.
check("HERO_F23: 8 lines / 9 occurrences in the built tree",
      _token_lines["HERO_F23"] == 8 and _token_occ["HERO_F23"] == 9)
check("hero: dealt amazing moment (moment + composition + motion) in the decision record",
      "gets a dealt amazing moment" in taste
      and "a dealt moment + a distinctive composition + motion" in taste)
check("hero: highest-weight browser-qa surface; merely adequate fails F6",
      "The hero is the highest-weight" in taste
      or "highest-weight" in taste)
check("hero calibration: app home/feed surface IS the hero surface, bar fits the job",
      "the home/feed surface IS the hero surface" in taste
      and "calibrated to the product" in taste)
check("hero: amazing never means a generic hero section pasted onto an app",
      "generic hero section pasted onto an app" in taste)
check("hero-moment line written to the Picks block (Hero-moment row)",
      "Hero-moment row" in taste
      and "Hero-moment" in taste)
check("hero review judges the hero against the dealt moment (review-hero.md)",
      "HERO_F23" in hero_rev)
check("hero checklist: first screen carries the dealt moment",
      "**First screen:**" in taste
      and "the hero carries its dealt amazing moment (HERO_F23)" in taste)
check("hero static checks in Taste step 6 (completeness only, verdict is browser-qa's)",
      "Fix #23 static checks" in taste and "HERO_F23" in taste)
check("orchestrate: dealt hero moment recorded per UI slice brief; brief without one not ready",
      "Hero moment and functionality story in every UI slice brief" in orch
      and "HERO_F23" in orch)
check("HERO-BQA_F23: 3 lines in the built tree",
      _token_lines["HERO-BQA_F23"] == 3)
check("browser-qa hero verdict: highest weight, merely adequate FAILS F6, calibration",
      "Hero verdict" in bqa and "HERO-BQA_F23" in bqa
      and "carries the highest weight" in bqa
      and "A merely adequate hero" in bqa and "FAILS F6" in bqa
      and "the moment must serve what the user opens the app to do" in bqa)
check("browser-qa hero verdict is browser-qa's alone",
      "no other step judges the hero" in bqa)

# 5. SS5 Functionality.
check("FUNC_F23: 8 lines / 9 occurrences in the built tree",
      _token_lines["FUNC_F23"] == 8 and _token_occ["FUNC_F23"] == 9)
check("functionality: mechanism shown early, first-class, theme-matched",
      "Functionality story" in taste
      and "as a first-class surface, theme-matched, not an afterthought" in taste)
check("functionality: R2 strengthened -- mechanism visible on hero or first screen after it",
      "on the hero surface or the first screen after it" in taste)
check("functionality: mechanism must be THIS build's (own names, real figures)",
      "must be THIS build's mechanism" in taste
      or "THIS build's" in taste)
check("functionality: decision record states the functionality story",
      "functionality story" in taste
      and "what is technically new here" in taste)
check("functionality: a build that hides what the thing does fails",
      "hides what the thing does" in taste)
check("FUNC-DIAG_F23: 4 lines in the built tree (diagrams.md + pointers)",
      _token_lines["FUNC-DIAG_F23"] == 4 and "FUNC-DIAG_F23" in diag)
check("FUNC-BQA_F23: 2 lines in the built tree (browser-qa + Taste)",
      _token_lines["FUNC-BQA_F23"] == 2 and "FUNC-BQA_F23" in bqa)
check("browser-qa functionality check: HOW it works early, THIS build's stack, fails if hidden",
      "Functionality check" in bqa and "FUNC-BQA_F23" in bqa
      and "shows HOW it works early" in bqa
      and "naming THIS build's pipeline, data, and stack" in bqa
      and "hides what the thing does FAILS" in bqa)
check("FUNC-UIPRO_F23: 1 line in the built tree (ui-ux-pro-max pointer)",
      _token_lines["FUNC-UIPRO_F23"] == 1 and "FUNC-UIPRO_F23" in uipro)
check("ui-ux-pro-max functionality pointer: full rule lives in design-taste-frontend",
      "Functionality pointer" in uipro
      and "The full rule lives in `design-taste-frontend` step 4a (FUNC_F23)" in uipro)
check("orchestrate: functionality story named per UI slice brief; brief without one not ready",
      "functionality story" in orch and "FUNC_F23" in orch)
check("Taste step 6 static checks cover functionality (completeness only)",
      "Fix #23 static checks" in taste and "FUNC_F23" in taste)

# 6. SS6 Alignment.
check("ALIGN_F23: 15 lines / 16 occurrences in the built tree",
      _token_lines["ALIGN_F23"] == 15 and _token_occ["ALIGN_F23"] == 16)
check("alignment checklist file exists (polish-pass reference/alignment.md)",
      os.path.isfile(os.path.join(
          BASE, "skills/polish-pass/reference/alignment.md")))
check("alignment checklist is candidate evidence, never a verdict",
      "candidate evidence only" in align)
for _a in ("ALIGN_F23_OVERFLOW", "ALIGN_F23_CENTER", "ALIGN_F23_NAV",
           "ALIGN_F23_GRID", "ALIGN_F23_CLIP", "ALIGN_F23_LABELS",
           "ALIGN_F23_ACTIONS", "ALIGN_F23_PANELS"):
    check(f"alignment assertion {_a} in polish-pass alignment.md",
          _a in align)
check("browser-qa alignment assertions: all 8 prose assertions (a)-(h) present",
      all(s in bqa for s in (
          "No horizontal overflow at any tested width",
          "Hero / phone frame centered in the viewport",
          "Nav items evenly spaced",
          "Card edges aligned to a common left/right grid",
          "No text clipped or overflowing its container",
          "No label collisions",
          "Primary actions centered on their axis",
          "Desktop side panels"))
      and "Alignment assertions" in bqa)
check("alignment tolerances: 0px overflow, <=2px centering/grid/spacing",
      "**0px** for overflow" in align
      and "**≤ 2px** for centering / grid / spacing equality" in align)
check("alignment measurement model: getBoundingClientRect on the live page",
      "getBoundingClientRect()" in align
      and "align-audit.mjs" in align)
check("alignment: no horizontal overflow (scrollWidth - innerWidth == 0)",
      "scrollWidth - innerWidth == 0" in bqa)
check("alignment: hero/phone frame centered <= 2px; mid-band hero GROUP centered",
      "hero GROUP is centered with equal outer margins" in bqa)
check("alignment: declared intentional bleed is the only escape (page overflow still 0)",
      "declared intentional bleed" in bqa
      and "page overflow still 0" in bqa)
check("COVER_F23: 4 lines in the built tree",
      _token_lines["COVER_F23"] == 4)
check("coverage: three widths 1440 / mid 900 (band 768-1100) / mobile 390",
      "1440 desktop, 900 mid-band default probe (band 768" in bqa)
check("coverage: new widths supersede the old 375/768/1440 breakpoints",
      "supersede the 375 / 768 / 1440 breakpoints" in bqa)
check("coverage: EVERY flow state measured + screenshotted, not just happy path",
      "Coverage is MANDATORY for EVERY flow state" in bqa)
check("coverage: breakpoint +-1 probe + mid full-page shot in the matrix",
      "breakpoint" in align and "full-page" in align)
check("BLOCK_F23: 5 lines in the built tree",
      _token_lines["BLOCK_F23"] == 5)
check("blocking gap: unverified width/state is NOT shippable, DO NOT SHIP",
      "is NOT shippable" in bqa and "DO NOT SHIP" in bqa
      and "a blocking finding, not a note" in bqa)
check("blocking gap: empty matrix cell is never SHIP / SHIP WITH FIXES / INCONCLUSIVE-as-pass",
      "never reported as SHIP, SHIP WITH FIXES, or INCONCLUSIVE-as-pass" in bqa)
check("browser-qa Alignment report section + coverage row",
      "### Alignment" in bqa
      and "Coverage: every width" in bqa)
check("orchestrate alignment coverage gate (BLOCK_F23 + COVER_F23)",
      "Alignment coverage gate" in orch and "BLOCK_F23" in orch
      and "COVER_F23" in orch)
check("polish-pass runs the alignment checklist as candidate evidence",
      "ALIGN_F23" in polish)
check("alignment sub-ids ALIGN_F23-A..E each occur exactly once as a tuple in build.sh",
      all(build.count("('ALIGN_F23-%s'," % c) == 1 for c in "ABCDE"))

# 7. SS9 Dynamic.
check("DYNAMIC_F23: 8 lines / 9 occurrences in the built tree",
      _token_lines["DYNAMIC_F23"] == 8 and _token_occ["DYNAMIC_F23"] == 9)
check("dynamic in motion-foundations: state changes choreographed, no-motion gap",
      "State changes are choreographed" in mf
      and "DYNAMIC_F23" in mf)
check("dynamic in motion-patterns: interactive depth, sortable/filterable/expandable/draggable",
      "Interactive depth" in mp and "DYNAMIC_F23" in mp
      and "sortable, filterable, expandable, draggable" in mp)
check("dynamic in motion-advanced: live and interactive pieces",
      "Advanced pieces are live and interactive" in ma
      and "DYNAMIC_F23" in ma)
check("dynamic: state change with no motion is a gap",
      "state change with no motion" in mf.lower()
      or "state that changes without motion" in bqa)
check("dynamic: reduced-motion fallback stays complete in the motion skills",
      all("reduced-motion" in ln.lower()
          for _t in (mf, mp, ma)
          for ln in _t.splitlines() if "DYNAMIC_F23" in ln))
check("browser-qa dynamic live check (DYNAMIC-BQA-01): interacts, confirms response live",
      "Dynamic-interface live check" in bqa and "DYNAMIC_F23" in bqa
      and "sort, filter, expand, and drag" in bqa
      and "live state moves" in bqa)
check("browser-qa dynamic live check FAILS a build whose controls do not respond",
      "A control that does not respond, or a state that changes without motion, FAILS the build" in bqa)
check("browser-qa dynamic live check: undrivable interaction recorded as unverified, never a silent pass (M1)",
      "record that interaction as unverified" in bqa
      and "the Dynamic row is not ✓ on an interaction never driven" in bqa)
check("browser-qa Dynamic report row (DYNAMIC-BQA-02)",
      "- [✓/✗] Dynamic (DYNAMIC_F23)" in bqa)
check("orchestrate dynamic story per surface: what changes, what triggers it, how it moves",
      "Dynamic story in every UI slice brief" in orch
      and "WHAT changes" in orch and "WHAT triggers it" in orch
      and "HOW it moves" in orch)
check("polish-pass reads the dynamic story from the decision record (DYNAMIC_F23 x2)",
      polish.splitlines()[100].count("DYNAMIC_F23") == 2
      and "dynamic story" in polish)
check("SS9-vs-SS2 distinction stated: SS2 is motion-presence, SS9 is state-change/interactivity",
      "This is the state-change and interactivity rule" in orch
      and "is the motion-presence rule" in orch)
check("dynamic sub-ids DYNAMIC-01/02/03 + DYNAMIC-BQA-01 each occur once as a tuple in build.sh",
      all(build.count("('%s'," % s) == 1 for s in
          ("DYNAMIC-01", "DYNAMIC-02", "DYNAMIC-03", "DYNAMIC-BQA-01")))
check("DYNAMIC-BQA-02: one tuple + trailing comment + CORE header mention (3 total)",
      build.count("('DYNAMIC-BQA-02',") == 1
      and build.count("DYNAMIC-BQA-02") == 3)
check("dynamic sub-ids occur 0x in the built tree (by design)",
      all(s not in mf + mp + ma + orch + polish + bqa
          for s in ("DYNAMIC-01", "DYNAMIC-02", "DYNAMIC-03",
                    "DYNAMIC-BQA-01", "DYNAMIC-BQA-02")))

# 8. Global.
check("build.sh is 24,059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2 (post-fix23 + M1)",
      len(build_lines) == 24059
      and build_md5 == "df2cb85055efc87637d3cb0b1e7061a2")
_diff = subprocess.run(
    ["diff", "build.sh.before-fix23", "build.sh"],
    cwd=PLUGIN, capture_output=True, text=True).stdout
_diff_add = sum(1 for ln in _diff.splitlines() if ln.startswith(">"))
_diff_del = sum(1 for ln in _diff.splitlines() if ln.startswith("<"))
check("diff vs build.sh.before-fix23 is additions only (+285/-0)",
      _diff_add == 285 and _diff_del == 0)
if _diff_del:
    print(f"   deletions in diff: {_diff_del}")
check("fix23 build.sh blocks present: W1 + SS3 + W3 + SS6 + SS9 + CORE",
      all(m in build for m in (
          "fix23 W1 upstream block applied",
          "fix23 section 3 upstream block applied",
          "fix23-W3 upstream block applied",
          "fix23 §6 alignment block applied",
          "fix23 section 9 upstream block applied",
          "fix23 CORE upstream block applied")))
def _line_no(marker):
    return next(i for i, ln in enumerate(build_lines) if marker in ln)
check("fix23 block order: SS9 block < CORE block < STEP 5 Counts",
      _line_no("# --- fix23 §9:") < _line_no("# --- fix23 CORE:")
      < _line_no("# STEP 5 — Counts"))
check("17 files carry _F23 tokens in the built tree",
      len(_files_with_f23) == 17)
# Counts unchanged post-fix22.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))


hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged -- no new skill/command/trigger)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))
_triggers = json.load(open(os.path.join(
    BASE, "manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
check("trigger keys still 64 (no new trigger from this fix)",
      _triggers["coverage"]["withTriggers"] == len(_triggers["triggers"]) == 64)
check("every trigger key still resolves to a real skill dir",
      all(os.path.isfile(os.path.join(
          BASE, "skills", _k[len("skill:"):], "SKILL.md"))
          for _k in _triggers["triggers"]))
# Banned terms + Grok pins.
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")
if hits:
    print("   banned-term files: %r" % (hits,))
_bare_grok = subprocess.run(
    ["grep", "-rn", "grok-4.6-high-fast", "skills", "agents", "commands",
     "rules", "hooks", "README.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout
_bare_grok = "\n".join(
    ln for ln in _bare_grok.splitlines() if "cursor-grok-4.6-high-fast" not in ln)
check("bare grok-4.6-high-fast absent (Grok pins only)",
      _bare_grok.strip() == "")
_g47 = subprocess.run(
    ["grep", "-rl", "grok-4.7-high", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_c46 = subprocess.run(
    ["grep", "-rl", "cursor-grok-4.6-high-fast", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("Grok pins: grok-4.7-high in 26 files, cursor-grok-4.6-high-fast in 85",
      len(_g47.splitlines()) == 26 and len(_c46.splitlines()) == 85)
# /demo gates intact.
check("DEMOGATE tokens present at every site (O4/O9, B2S1, B3S1, H1/H2)",
      "DEMOGATE_O4_F22" in orch and "DEMOGATE_O9_F22" in orch
      and "DEMOGATE_B2S1_F22" in obm and "DEMOGATE_B3S1_F22" in ocf
      and "DEMOGATE_H1_F22" in hm and "DEMOGATE_H2_F22" in hm)
_fix23_block = "\n".join(build_lines[23764:24020])  # lines 23765-24020
check("zero 'demo' mentions inside the fix23 build.sh blocks",
      "demo" not in _fix23_block.lower())
check("no new auto-invocation wording inside the fix23 build.sh blocks",
      "auto-invok" not in _fix23_block.lower()
      and "automatically" not in _fix23_block.lower())
check("narration-key prompt fires ONLY when the user asked for a demo video",
      "ONLY when the user asked for a demo video" in orch
      and "only when the user asked for a demo video" in hm
      and "If the user did NOT ask for a demo video, do NOT send this prompt" in obm)
check("first-build sequence intact: /demo never part of the order",
      "/demo is never part of this sequence" in orch
      and "/demo is never part of this sequence" in hm)
check("MEMORABLE-BQA-01: one tuple + trailing comment (2 total); MEMORABLE-BQA-02: + CORE header mention (3 total)",
      build.count("('MEMORABLE-BQA-01',") == 1
      and build.count("MEMORABLE-BQA-01") == 2
      and build.count("('MEMORABLE-BQA-02',") == 1
      and build.count("MEMORABLE-BQA-02") == 3)
check("BQA-TYPEAUDIT / UIPRO-F7VAR / ORCH-TYPEAUDIT: one tuple + trailing comment each (2 total)",
      all(build.count("('%s'," % s) == 1 and build.count(s) == 2
          for s in ("BQA-TYPEAUDIT", "UIPRO-F7VAR", "ORCH-TYPEAUDIT")))
check("BQA sub-ids occur 0x in the built tree (by design)",
      all(s not in bqa + obm + uipro + orch
          for s in ("BQA-TYPEAUDIT", "UIPRO-F7VAR", "ORCH-TYPEAUDIT",
                    "MEMORABLE-BQA-01", "MEMORABLE-BQA-02")))

# 9. Prior-verifier regression leg. EXPECTED fails are ONLY: the frozen
# post-fix21 build.sh fingerprint, the frozen post-fix22 build.sh
# fingerprint (fix22's verifier newly fails on it -- it expects 23,774
# lines / md5 4799a819...), the less-flat-ui diff-hunk pattern (6 hunks),
# and cascades of those. Any fail outside that pattern is a REAL
# regression. Exact tails are asserted so a new fail changes the count.
_FPRINT21 = ("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c",
             "build.sh is 23647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c")
_FPRINT22 = "build.sh is 23774 lines, md5 4799a819791b9c3ec4c19136ad698397"
_LFUI_DIFF = "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks"


def _allowed_fail(line):
    return (any(p in line for p in _FPRINT21)
            or _FPRINT22 in line
            or _LFUI_DIFF in line
            or re.match(r"FAIL fix\d+ verifier still passes", line))


for name, script, tail in (
        ("fix15", "fix15/verify15.py", "42/44 checks pass"),
        ("fix17", "fix17/verify17.py", "58/60 checks pass"),
        ("fix18", "fix18/verify18.py", "69/72 checks pass"),
        ("fix19", "fix19/verify19.py", "71/76 checks pass"),
        ("fix20", "fix20/verify20.py", "164/169 checks pass"),
        ("fix21", "fix21/verify21.py", "96/102 checks pass"),
        ("fix22", "fix22/verify22.py", "368/369 checks pass")):
    r = subprocess.run(["python3", script], cwd=PLUGIN,
                       capture_output=True, text=True)
    _out_tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    _fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    _bad = [ln for ln in _fails if not _allowed_fail(ln)]
    if _bad:
        print(f"   {name} unexpected FAILs: {_bad}")
    check(f"{name} verifier: only expected fails, tail is {_out_tail} "
          f"(expected {tail})",
          not _bad and _out_tail == tail)

# 10. Manifest check (fix22 pattern). Runs once fix23/MANIFEST.md exists;
# FAILS until the manifest worker writes it. Reported separately as owed.
manifest_path = os.path.join(PLUGIN, "fix23/MANIFEST.md")
_manifest_ok = False
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    _manifest_ok = bool(m_lines and m_md5
                        and int(m_lines.group(1)) == len(build_lines)
                        and m_md5.group(1) == build_md5)
check("fix23/MANIFEST.md exists and records build.sh lines + md5 "
      "(OWED -- fails until the manifest worker writes it)",
      _manifest_ok)

failed = [n for n, ok in checks if not ok]
_manifest_failed = not _manifest_ok
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
if _manifest_failed:
    print(f"excluding the manifest check, which is owed: "
          f"{len(checks) - len(failed)}/{len(checks) - 1} checks pass")
sys.exit(1 if failed else 0)
