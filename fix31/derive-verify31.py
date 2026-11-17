#!/usr/bin/env python3
"""Derive fix31/verify31.py from fix30/verify30.py (coordinator tool, run once).

Applies exact replacements (each asserting its count) and appends the new
§14 fix31 checks (skills, _F31 tokens, DESIGNPKG-AUTO + palette-first
weight, inventory §12, license checks, README note, fix31 patch log).
The call-map sidecar check (10g) is deliberately LEFT at 67: the sidecar
describes the fix28 map, which is not regenerated in fix31 (OWED-31-3).
"""
import os
import sys

ROOT = os.path.expanduser("~/workspace/hackathon-plugin")
SRC = os.path.join(ROOT, "fix30", "verify30.py")
DST = os.path.join(ROOT, "fix31", "verify31.py")
ERRORS = []


def rep(text, old, new, count, where):
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{where}: expected {count}x, found {n}x :: {old[:70]!r}")
        return text
    return text.replace(old, new)


t = open(SRC, encoding="utf-8").read()

# --- header / docstring ---
t = rep(t, '"""verify30.py -- checks fix #30 in the BUILT tree (read-only).',
        '"""verify31.py -- checks fix #31 in the BUILT tree (read-only).', 1, "header")
t = rep(t, "Run after a build: python3 fix30/verify30.py [built-plugin-dir]",
        "Run after a build: python3 fix31/verify31.py [built-plugin-dir]", 1, "header")
t = rep(t,
        "Counts unchanged: skills 67, agents 45,\nrules 48, commands 55, hooks 15, trigger keys 49. Call map NOT\nregenerated (no new dispatch edges); the fix28 map stands.",
        "Counts: skills 67 -> 72 (5 new: getlayers, gsap, react-bits,\nhairline-create, hairline-adopt), agents 45, rules 48, commands 55,\nhooks 15, trigger keys 49. Call map NOT regenerated (no new dispatch\nedges — the new skills are leaf resources, not dispatchers); the fix28\nmap stands (OWED-31-3).",
        1, "header counts")
t = rep(t,
        "Build fixes folded in (not cuts): build.sh MS_SRC now follows MS_DIR",
        "Fix #31 (SPEC fix31/SPEC.md): design-library additions — GetLayers\n(prompt-first cinematic layers, free set only, MCP not wired), GSAP\n(timeline/scroll animation, npm install, pin gsap@3.15.1), React Bits\n(animated React components, CLI install, no embedded source), Hairline\nillustrations (MIT, 33 figures; skills hairline-create + hairline-adopt\nvendored). One skill/inventory entry per resource, woven into the\npalette-first flow + single inventory catalog (fix #23). GetLayers\nprompts carry first-class weight (direction update, Anish Nov 16 ~10:02\nPM): consulted FIRST in the palette inventory, the direction leans on\nthem heavily, and the direction cites the layers USED or\nCONSIDERED-AND-REJECTED with a D19 reason.\n\nBuild fixes folded in (not cuts): build.sh MS_SRC now follows MS_DIR",
        1, "header fix31 paragraph")
t = rep(t, "  1. Counts: skills 67, agents 45, rules 48, commands 55; exact dir",
        "  1. Counts: skills 72, agents 45, rules 48, commands 55; exact dir", 1, "doc 1")
t = rep(t, "  2. All 100 CUT skill dirs absent; all 67 KEPT skill dirs present.",
        "  2. All 100 CUT skill dirs absent; all 72 KEPT skill dirs present.", 1, "doc 2")
t = rep(t, "     49 keys remain, coverage.skills == 67, withTriggers == 49.",
        "     49 keys remain, coverage.skills == 72, withTriggers == 49.", 1, "doc 5")
t = rep(t, "  6. README count lines show the new counts (67/45/48/55, 46 rules",
        "  6. README count lines show the new counts (72/45/48/55, 46 rules", 1, "doc 6")
t = rep(t,
        " 11b. [29] fix29 patch log exists with 0 errors and the census line\n     (all 10 in-scope skills).\n\"\"\"",
        " 11b. [29] fix29 patch log exists with 0 errors and the census line\n     (all 10 in-scope skills).\n 14. [31] Fix #31 design libraries: the 5 new skills exist with\n     SKILL.md + frontmatter and no model pin text; all 4 _F31 tokens\n     exist and live in their skills; DESIGNPKG-AUTO is byte-identical\n     in orchestrate + hackathon-mode, names all 5 skills, and carries\n     the GetLayers weight (palette list starts with getlayers, priority\n     sentence, citation sentence); the palette-first paragraph names\n     getlayers FIRST with the citation sentence; the inventory has §12\n     with the GetLayers weight; the getlayers skill carries the\n     first-class weight language and invokes no MCP tools and no frozen\n     counts; react-bits/gsap/getlayers dirs contain only SKILL.md;\n     hairline engine/checks/LICENSE vendored; no vendored GSAP source;\n     README fix31 note present; fix31 patch log exists with 0 errors.\n\"\"\"",
        1, "doc 14")

# --- KEPT_SKILLS + counts ---
t = rep(t, "assert len(CUT_SKILLS) == 100 and len(KEPT_SKILLS) == 67",
        "assert len(CUT_SKILLS) == 100 and len(KEPT_SKILLS) == 72", 1, "kept len")
t = rep(t, '    "frontend-a11y", "frontend-patterns", "frontend-slides", "gan-style-harness",\n    "git-workflow",',
        '    "frontend-a11y", "frontend-patterns", "frontend-slides", "gan-style-harness", "getlayers",\n    "git-workflow",', 1, "kept getlayers")
t = rep(t, '    "grill-me", "growth-log", "hackathon-pitch", "hackathon-scope",',
        '    "grill-me", "growth-log", "gsap", "hackathon-pitch", "hackathon-scope",\n    "hairline-adopt", "hairline-create",',
        1, "kept gsap/hairline")
t = rep(t, '    "python-testing", "react-native-patterns", "react-patterns",',
        '    "python-testing", "react-bits", "react-native-patterns", "react-patterns",', 1, "kept react-bits")
t = rep(t, 'check("counts 67 skills / 45 agents / 48 rules / 55 commands",',
        'check("counts 72 skills / 45 agents / 48 rules / 55 commands",', 1, "check 1 name")
t = rep(t, "      == (67, 45, 48, 55))", "      == (72, 45, 48, 55))", 1, "check 1 tuple")
t = rep(t, "if (len(_skills), len(_agents), len(_rules), len(_commands)) != (67, 45, 48, 55):",
        "if (len(_skills), len(_agents), len(_rules), len(_commands)) != (72, 45, 48, 55):",
        1, "check 1 guard")
t = rep(t, 'check("skills dir set is exactly the 67 KEPT skills",',
        'check("skills dir set is exactly the 72 KEPT skills",', 1, "check 1b name")
t = rep(t, 'check("trigger coverage: skills 67, withTriggers 49",',
        'check("trigger coverage: skills 72, withTriggers 49",', 1, "check 5 name")
t = rep(t, '      _triggers["coverage"]["skills"] == 67',
        '      _triggers["coverage"]["skills"] == 72', 1, "check 5 assert")
t = rep(t, 'check("README count line shows 67 skills, 45 agents, 48 rules, 55 commands (46 rules as-shipped)",',
        'check("README count line shows 72 skills, 45 agents, 48 rules, 55 commands (46 rules as-shipped)",',
        1, "check 6a name")
t = rep(t, '      "67 skills, 45 agents, 48 rules, and 55 commands in total "',
        '      "72 skills, 45 agents, 48 rules, and 55 commands in total "', 1, "check 6a assert")
t = rep(t, 'check("README comparison lines show the new counts (67 / 45 / 55)",',
        'check("README comparison lines show the new counts (72 / 45 / 55)",', 1, "check 6b name")
t = rep(t, '      "67 skills widen the routing surface" in _readme',
        '      "72 skills widen the routing surface" in _readme', 1, "check 6b assert 1")
t = rep(t, '      and "56 MB and 67 skills against a minimal set" in _readme',
        '      and "56 MB and 72 skills against a minimal set" in _readme', 1, "check 6b assert 2")
t = rep(t, '      and "structured process — 67 skills, 45 agents, 55 commands," in _readme)',
        '      and "structured process — 72 skills, 45 agents, 55 commands," in _readme)',
        1, "check 6b assert 3")
t = rep(t, 'for _tok in ("166 skills", "72 agents", "87 commands",\n             "66 skills", "60 commands", "123 rules",\n             "121 rules as-shipped"):',
        'for _tok in ("166 skills", "72 agents", "87 commands",\n             "66 skills", "60 commands", "123 rules", "67 skills",\n             "121 rules as-shipped"):',
        1, "stale tuple")
t = rep(t, '''check("zero '166 skills' / '72 agents' / '87 commands' / '66 skills' / '60 commands' / '123 rules' / '121 rules as-shipped' remain in the built tree",''',
        '''check("zero '166 skills' / '72 agents' / '87 commands' / '66 skills' / '60 commands' / '123 rules' / '67 skills' / '121 rules as-shipped' remain in the built tree",''',
        1, "stale check name")

if ERRORS:
    print("DERIVE FAILED:")
    for e in ERRORS:
        print("  ERROR: " + e)
    sys.exit(1)

# --- append §14 fix31 checks before the final failed/exit block ---
anchor = "failed = [n for n, ok in checks if not ok]"
if t.count(anchor) != 1:
    print(f"DERIVE FAILED: final anchor occurs {t.count(anchor)}x, expected 1")
    sys.exit(1)
section14 = '''
# 14. [31] Fix #31 design libraries.
_NEW31 = ("getlayers", "gsap", "react-bits", "hairline-create", "hairline-adopt")
for _s in _NEW31:
    _f31 = os.path.join(BASE, "skills", _s, "SKILL.md")
    check(f"fix31 skill {_s} exists with SKILL.md", os.path.exists(_f31))
    if os.path.exists(_f31):
        _t31 = open(_f31, encoding="utf-8").read()
        check(f"fix31 skill {_s} frontmatter names {_s}",
              _t31.startswith("---\\nname: " + _s + "\\n"))
        check(f"fix31 skill {_s} carries no model pin text",
              "grok-4.7-high" not in _t31 and "grok-4.7-extra-high" not in _t31
              and "Grok 4.7 High" not in _t31 and "Grok 4.7 Extra High" not in _t31)
# _F31 tokens exist in the built tree and live in their skills.
for _tok in ("GETLAYERS_F31", "GSAP_F31", "REACTBITS_F31", "HAIRLINE_F31"):
    check(f"fix31 anchor token {_tok} exists in the built tree",
          count_in_tree(_tok) + _readme.count(_tok) > 0)
check("fix31 token GETLAYERS_F31 is in skills/getlayers/SKILL.md",
      "GETLAYERS_F31" in read("skills/getlayers/SKILL.md"))
check("fix31 token GSAP_F31 is in skills/gsap/SKILL.md",
      "GSAP_F31" in read("skills/gsap/SKILL.md"))
check("fix31 token REACTBITS_F31 is in skills/react-bits/SKILL.md",
      "REACTBITS_F31" in read("skills/react-bits/SKILL.md"))
check("fix31 token HAIRLINE_F31 is in skills/hairline-create/SKILL.md",
      "HAIRLINE_F31" in read("skills/hairline-create/SKILL.md"))
check("fix31 token HAIRLINE_F31 is in skills/hairline-adopt/SKILL.md",
      "HAIRLINE_F31" in read("skills/hairline-adopt/SKILL.md"))
# DESIGNPKG-AUTO: byte-identical, names all five, carries the weight.
def _dpkg_block(text):
    _i = text.find("**DESIGNPKG-AUTO")
    if _i < 0:
        return None
    _j = text.find("\\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]
_dp1 = _dpkg_block(read("skills/orchestrate/SKILL.md"))
_dp2 = _dpkg_block(read("rules/hackathon-mode.mdc"))
check("DESIGNPKG-AUTO block is byte-identical in orchestrate + hackathon-mode",
      _dp1 is not None and _dp1 == _dp2)
for _s in _NEW31:
    check(f"DESIGNPKG-AUTO block names {_s}",
          _dp1 is not None and _s in _dp1)
check("DESIGNPKG-AUTO palette list starts with getlayers (weight: consulted FIRST)",
      _dp1 is not None and "`getlayers`, `motionsites-web-builder`" in _dp1)
check("DESIGNPKG-AUTO block carries the GetLayers priority sentence",
      _dp1 is not None and "consulted FIRST in the palette inventory" in _dp1)
check("DESIGNPKG-AUTO block carries the GetLayers citation sentence",
      _dp1 is not None and "GetLayers layers are cited the same way" in _dp1)
# Palette-first paragraph (design-taste-frontend).
_dtf31 = read("skills/design-taste-frontend/SKILL.md")
check("palette-first paragraph names getlayers FIRST",
      "`getlayers` FIRST" in _dtf31)
check("palette-first paragraph carries the GetLayers citation sentence",
      "GetLayers layers are cited the same way" in _dtf31)
for _s in _NEW31:
    check(f"palette-first paragraph names {_s}", _s in _dtf31)
# Inventory §12 + weight.
_inv31 = read("skills/orchestrate/references/design-inventory.md")
check("design-inventory has §12 (fix #31 additions)",
      "## 12. Fix #31 additions" in _inv31)
check("design-inventory §12 names the GetLayers weight (Consulted FIRST)",
      "Consulted FIRST in the palette inventory" in _inv31)
for _ref in ("skills/getlayers/SKILL.md", "skills/gsap/SKILL.md",
             "skills/react-bits/SKILL.md", "skills/hairline-create/SKILL.md",
             "skills/hairline-adopt/SKILL.md"):
    check(f"design-inventory §12 references {_ref}", _ref in _inv31)
check("orchestrate inventory paragraph names the fix #31 additions with GetLayers weight",
      "the fix #31 additions" in read("skills/orchestrate/SKILL.md")
      and "consulted FIRST in the palette inventory" in read("skills/orchestrate/SKILL.md"))
# GetLayers skill weight language + license.
_gl31 = read("skills/getlayers/SKILL.md")
check("getlayers skill carries the first-class weight language",
      "first-class, high-priority source" in _gl31
      and "consulted FIRST" in _gl31
      and "Priority in the palette-first flow" in _gl31)
check("getlayers skill invokes no getlayers_* MCP tools",
      "getlayers_start" not in _gl31 and "getlayers_search" not in _gl31
      and "getlayers_materialize" not in _gl31)
for _fig in ("50 templates", "114 WebGL", "276 backgrounds", "10 animated sections"):
    check(f"getlayers skill carries no frozen count {_fig!r}", _fig not in _gl31)
check("react-bits skill dir contains only SKILL.md (no embedded source)",
      sorted(os.listdir(os.path.join(BASE, "skills", "react-bits"))) == ["SKILL.md"])
check("gsap skill dir contains only SKILL.md (no vendored source)",
      sorted(os.listdir(os.path.join(BASE, "skills", "gsap"))) == ["SKILL.md"])
check("getlayers skill dir contains only SKILL.md (no vendored content)",
      sorted(os.listdir(os.path.join(BASE, "skills", "getlayers"))) == ["SKILL.md"])
check("hairline-create ships its engine + checks + LICENSE",
      all(os.path.exists(os.path.join(BASE, "skills", "hairline-create", _f))
          for _f in ("kernel.js", "bench.html", "build.mjs", "validate.mjs",
                     "examples/terrain.js", "LICENSE")))
check("hairline-adopt ships its LICENSE",
      os.path.exists(os.path.join(BASE, "skills", "hairline-adopt", "LICENSE")))
_gsap_vendored = []
for _root, _dirs, _files in os.walk(BASE):
    _dirs[:] = [d for d in _dirs if d != "node_modules"]
    for _fn in _files:
        if _fn.lower() in ("gsap.js", "gsap.min.js", "gsap.ts"):
            _gsap_vendored.append(os.path.join(_root, _fn))
if _gsap_vendored:
    print(f"   vendored GSAP source: {_gsap_vendored}")
check("no vendored GSAP source file (gsap.js / gsap.min.js / gsap.ts) in the built tree",
      not _gsap_vendored)
# README fix31 note.
check("README fix31 provenance note present with the four _F31 tokens",
      "Fix #31 design libraries" in _readme
      and all(_tok in _readme for _tok in ("GETLAYERS_F31", "GSAP_F31", "REACTBITS_F31", "HAIRLINE_F31")))
# fix31 patch log.
_log31_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix31")
_log31_path = os.path.join(_log31_dir, "fix31-patch-log.md")
_log31_ok = False
_log31_text = ""
if os.path.exists(_log31_path):
    _log31_text = open(_log31_path, encoding="utf-8").read()
    _log31_ok = ("## Errors (0)" in _log31_text
                 and "coverage.skills 67 -> 72" in _log31_text
                 and "README: fix31 provenance note added" in _log31_text)
check("fix31/fix31-patch-log.md exists with 0 errors, trigger 67 -> 72, README note added",
      _log31_ok)

'''
t = t.replace(anchor, section14 + anchor, 1)
open(DST, "w", encoding="utf-8").write(t)
import ast
ast.parse(t)
print(f"DERIVE OK: {DST} written, parses OK")
print(f"  checks in verify30: see source; new §14 adds the fix31 checks")
