#!/usr/bin/env python3
"""Fix #31 — design-library additions: GetLayers, GSAP, React Bits, Hairline
illustrations.

Run by build.sh as a patch step (after fix30.py, before STEP 5 Counts):
    python3 "$PLUGIN_ROOT/fix31/fix31.py" "$PLUGIN_DIR"

The five new skills are STAGED sources (new-skills/getlayers,
new-skills/gsap, new-skills/react-bits, new-skills/hairline-create,
new-skills/hairline-adopt) and flow into the built tree through the
STEP 2 new-skills loop (build.sh); the palette-first / DESIGNPKG-AUTO /
inventory weave is also staged (fix31/weave31.py, run once by the
coordinator) and flows through the STEP 2 copy. This script operates on
the BUILT tree only and does three things:

  1. Census (no writes): asserts the staged weave landed (the five
     skills exist with SKILL.md + frontmatter; DESIGNPKG-AUTO is
     byte-identical in orchestrate + hackathon-mode and names all five
     skills; the palette-first paragraph names them; the inventory has
     §12), asserts the fix30 pin census still holds exactly (the weave
     adds no pin text), and runs the LICENSE checks (no vendored
     GetLayers content, no embedded React Bits component source, no
     vendored GSAP source, no frozen GetLayers/React Bits counts).
  2. Writes: README count lines 67 -> 72 (four lines) + the fix #31
     provenance note; trigger-file coverage.skills 67 -> 72
     (withTriggers stays 49 — the new skills get no trigger keys,
     same as MotionSites in fix #27).
  3. Post-assertions: re-census everything in (1) plus the README /
     trigger writes; zero "67 skills" remains in the built tree.

Exits non-zero on any error so the build fails rather than shipping a
half-woven tree.

SPEC fix31/SPEC.md: four resources, all free-tier only, no paid plans
purchased. (1) GetLayers (getlayers.ai) — FREE SET ONLY; the MCP
requires Full Stack Lifetime and is NOT wired; reference only,
no vendored content; a layer is a foundation, never shipped unchanged.
(2) GSAP — 100% free incl. all former Club plugins, public npm;
NOT OSI open source (Webflow "Standard no charge" licence); install
from npm at build time, never vendor source. (3) React Bits — MIT +
Commons Clause (may NOT sell/sublicense/redistribute the components);
catalog + install guide, no embedded source. (4) Hairline
illustrations (Lucas Marques) — MIT; 33 interactive isometric SVG
figures; skills hairline-create + hairline-adopt vendored as reference.
Hairline UI (hairlineui.com) is a DIFFERENT product and NOT in scope.

Version notes (measured Nov 17, 2026; the SPEC's Nov 16 figures were
already stale): GSAP npm latest is 3.15.1, NOT the SPEC's 3.15.0 — the
skill pins gsap@3.15.1, matching the inventory's existing pin
(DECISION-31-2). GetLayers live counts drifted in one day (llms.txt:
62 templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088
gradients, vs the SPEC's 50 / 114 / 10 / 276 / 1,088) — which is why
the skill carries NO counts and the verifier forbids the frozen Nov 16
figures (DECISION-31-3). @lucasmarkes/hairline npm latest is 0.5.1
(MIT, ESM-only).

Anchor tokens (_F31): GETLAYERS_F31, GSAP_F31, REACTBITS_F31,
HAIRLINE_F31. GETLAYERS/GSAP/REACTBITS live in the DESIGNPKG-AUTO
gloss (orchestrate + hackathon-mode) and in their skills' framing
headers; HAIRLINE_F31 lives in the DESIGNPKG-AUTO gloss and in both
hairline skills' framing headers. The five skills are named in the
DESIGNPKG-AUTO package list + palette list (both files), in the
design-taste-frontend palette-first paragraph, in the orchestrate
inventory paragraph, and in the inventory §12.
"""
import json
import os
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []

NEW_SKILLS = ("getlayers", "gsap", "react-bits", "hairline-create",
              "hairline-adopt")
F31_TOKENS = ("GETLAYERS_F31", "GSAP_F31", "REACTBITS_F31", "HAIRLINE_F31")
# Frozen Nov 16 GetLayers figures (SPEC) — already stale Nov 17; the skill
# must not carry them (counts drift weekly; read llms.txt live).
FROZEN_GETLAYERS = ("50 templates", "114 WebGL", "114 3D",
                    "276 backgrounds", "10 animated sections")
# Pin census from fix30 (must still hold exactly — the weave adds no pin text).
OLD_ID = "grok-4.7-high"
NEW_ID = "grok-4.7-extra-high"
OLD_PROSE = "Grok 4.7 High"
NEW_PROSE = "Grok 4.7 Extra High"
FAST_ID = "cursor-grok-4.6-high-fast"
FAST_BARE = "grok-4.6-high-fast"
EXPECT_PIN = {OLD_ID: 0, OLD_PROSE: 0, FAST_ID: 70,
              NEW_ID: 49, NEW_PROSE: 22}

SKIP_DIRS = {"node_modules", ".git"}


def p(rel):
    return os.path.join(BASE, rel)


def exists(f):
    return os.path.exists(f)


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def sub(f, old, new, count=1):
    """Replace old with new in file f; assert old occurs exactly `count` times."""
    if not exists(f):
        ERRORS.append(f"{f}: missing file")
        return
    _t = read(f)
    _n = _t.count(old)
    if _n != count:
        ERRORS.append(
            f"{os.path.relpath(f, BASE)}: expected {count}x {old[:60]!r}, found {_n}x")
        return
    write(f, _t.replace(old, new))
    CHANGES.append(f"{os.path.relpath(f, BASE)}: substituted {old[:50]!r} ...")


def _walk_files():
    for _root, _dirs, _files in os.walk(BASE):
        _dirs[:] = [d for d in _dirs if d not in SKIP_DIRS]
        for _name in sorted(_files):
            _path = os.path.join(_root, _name)
            try:
                with open(_path, encoding="utf-8") as _fh:
                    yield _path, _fh.read()
            except (UnicodeDecodeError, OSError):
                yield _path, None


def _block(text, marker):
    _i = text.find(marker)
    if _i < 0:
        return None
    _j = text.find("\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]


# ---------------------------------------------------------------- 1. Census (no writes)
# 1a. The five new skills exist with SKILL.md + frontmatter name/description.
for _s in NEW_SKILLS:
    _f = p(f"skills/{_s}/SKILL.md")
    if not exists(_f):
        ERRORS.append(f"census: skills/{_s}/SKILL.md missing from the built tree")
        continue
    _t = read(_f)
    if not _t.startswith("---\nname: " + _s + "\n"):
        ERRORS.append(f"census: skills/{_s}/SKILL.md frontmatter name is not {_s!r}")
    if "description:" not in _t.split("---", 2)[1]:
        ERRORS.append(f"census: skills/{_s}/SKILL.md frontmatter has no description")
    if _s in ("hairline-create", "hairline-adopt"):
        if "HAIRLINE_F31" not in _t:
            ERRORS.append(f"census: skills/{_s}/SKILL.md carries no HAIRLINE_F31")
    elif _s == "getlayers" and "GETLAYERS_F31" not in _t:
        ERRORS.append("census: skills/getlayers/SKILL.md carries no GETLAYERS_F31")
    if _s == "getlayers":
        # Direction update (Anish, Nov 16 ~10:02 PM): GetLayers prompts carry
        # first-class weight — consulted FIRST, priority language in the skill.
        for _w in ("first-class, high-priority source", "consulted FIRST",
                   "Priority in the palette-first flow"):
            if _w not in _t:
                ERRORS.append(f"census: skills/getlayers/SKILL.md lacks weight language {_w!r}")
    elif _s == "gsap" and "GSAP_F31" not in _t:
        ERRORS.append("census: skills/gsap/SKILL.md carries no GSAP_F31")
    elif _s == "react-bits" and "REACTBITS_F31" not in _t:
        ERRORS.append("census: skills/react-bits/SKILL.md carries no REACTBITS_F31")
# Hairline vendored companions: the create skill ships its engine + checks.
for _req in ("skills/hairline-create/kernel.js",
             "skills/hairline-create/bench.html",
             "skills/hairline-create/build.mjs",
             "skills/hairline-create/validate.mjs",
             "skills/hairline-create/examples/terrain.js",
             "skills/hairline-create/LICENSE",
             "skills/hairline-adopt/LICENSE"):
    if not exists(p(_req)):
        ERRORS.append(f"census: {_req} missing from the built tree")
if not ERRORS:
    CHANGES.append("census: all 5 new skills present with SKILL.md + frontmatter; "
                  "hairline engine/checks/examples/LICENSE vendored")

# 1b. DESIGNPKG-AUTO byte-identical in orchestrate + hackathon-mode, names
#     all five skills, carries all four _F31 tokens.
_orch = read(p("skills/orchestrate/SKILL.md"))
_hm = read(p("rules/hackathon-mode.mdc"))
_b1 = _block(_orch, "**DESIGNPKG-AUTO")
_b2 = _block(_hm, "**DESIGNPKG-AUTO")
if _b1 is None or _b2 is None:
    ERRORS.append("census: DESIGNPKG-AUTO block not found in orchestrate or hackathon-mode")
elif _b1 != _b2:
    ERRORS.append("census: DESIGNPKG-AUTO block differs between orchestrate and hackathon-mode")
else:
    CHANGES.append("census: DESIGNPKG-AUTO block byte-identical in orchestrate + hackathon-mode")
for _s in NEW_SKILLS:
    if _b1 is None or _s not in _b1:
        ERRORS.append(f"census: DESIGNPKG-AUTO block does not name {_s}")
for _tok in F31_TOKENS:
    if _b1 is None or _tok not in _b1:
        ERRORS.append(f"census: DESIGNPKG-AUTO block missing token {_tok}")
# Weight (direction update, Anish Nov 16 ~10:02 PM): GetLayers is consulted
# FIRST in the palette inventory — the palette list must START with
# getlayers, the priority sentence and the citation sentence must be present.
if _b1 is not None:
    _pal = _b1.split("the available component/design sources (", 1)
    if len(_pal) != 2 or not _pal[1].startswith("`getlayers`"):
        ERRORS.append("census: DESIGNPKG-AUTO palette list does not start with getlayers")
    if "consulted FIRST in the palette inventory" not in _b1:
        ERRORS.append("census: DESIGNPKG-AUTO block lacks the GetLayers priority sentence")
    if "GetLayers layers are cited the same way" not in _b1:
        ERRORS.append("census: DESIGNPKG-AUTO block lacks the GetLayers citation sentence")

# 1c. Palette-first paragraph (design-taste-frontend) names all five skills;
#     GetLayers is named FIRST, with the citation sentence.
_dtf = read(p("skills/design-taste-frontend/SKILL.md"))
if "PALETTE-FIRST_F27" not in _dtf:
    ERRORS.append("census: design-taste-frontend carries no PALETTE-FIRST_F27")
for _s in NEW_SKILLS:
    if _s not in _dtf:
        ERRORS.append(f"census: design-taste-frontend palette paragraph does not name {_s}")
if "`getlayers` FIRST" not in _dtf:
    ERRORS.append("census: design-taste-frontend does not consult getlayers FIRST in the palette inventory")
if "GetLayers layers are cited the same way" not in _dtf:
    ERRORS.append("census: design-taste-frontend lacks the GetLayers citation sentence")

# 1d. Inventory: §12 present; §1/§9 pointers present; orchestrate inventory
#     paragraph names the fix #31 additions.
_inv = read(p("skills/orchestrate/references/design-inventory.md"))
if "## 12. Fix #31 additions" not in _inv:
    ERRORS.append("census: design-inventory.md has no §12 (fix #31 additions)")
for _needle in ("skills/gsap/SKILL.md", "skills/react-bits/SKILL.md",
                "skills/getlayers/SKILL.md", "skills/hairline-create/SKILL.md",
                "skills/hairline-adopt/SKILL.md"):
    if _needle not in _inv:
        ERRORS.append(f"census: design-inventory.md does not reference {_needle}")
if "the fix #31 additions" not in _orch:
    ERRORS.append("census: orchestrate inventory paragraph does not name the fix #31 additions")
if "consulted FIRST in the palette inventory" not in _orch:
    ERRORS.append("census: orchestrate inventory paragraph lacks the GetLayers weight")
if "Consulted FIRST in the palette inventory" not in _inv:
    ERRORS.append("census: design-inventory §12 GetLayers row lacks the Consulted-FIRST weight")
if "carry the most weight in the palette-first flow" not in _inv:
    ERRORS.append("census: design-inventory §12 intro lacks the GetLayers weight note")

# 1e. Pin census still exact (the weave adds no pin text) + zero pin text in
#     the new skills.
_totals = {k: 0 for k in EXPECT_PIN}
_totals["bare_fast"] = 0
for _path, _text in _walk_files():
    if _text is None:
        continue
    for _k in EXPECT_PIN:
        _totals[_k] += _text.count(_k)
    _i = 0
    while True:
        _i = _text.find(FAST_BARE, _i)
        if _i < 0:
            break
        if not _text[max(0, _i - 7):_i].endswith("cursor-"):
            _totals["bare_fast"] += 1
        _i += len(FAST_BARE)
for _k, _want in EXPECT_PIN.items():
    if _totals[_k] != _want:
        ERRORS.append(f"census: pin {_k} found {_totals[_k]}x, expected {_want}x")
if _totals["bare_fast"] != 0:
    ERRORS.append(f"census: bare {FAST_BARE} found {_totals['bare_fast']}x, expected 0x")
for _s in NEW_SKILLS:
    _t = read(p(f"skills/{_s}/SKILL.md"))
    for _pin in (OLD_ID, NEW_ID, OLD_PROSE, NEW_PROSE):
        if _pin in _t:
            ERRORS.append(f"census: pin text {_pin!r} in skills/{_s}/SKILL.md (new skills carry no pins)")
if not ERRORS:
    CHANGES.append(
        f"census: pin census holds ({NEW_ID} x{_totals[NEW_ID]}, {NEW_PROSE!r} "
        f"x{_totals[NEW_PROSE]}, {FAST_ID} x{_totals[FAST_ID]}, {OLD_ID} x0, "
        f"{OLD_PROSE!r} x0); zero pin text in the 5 new skills")

# 1f. LICENSE checks (no vendored content).
_gl = read(p("skills/getlayers/SKILL.md"))
if "getlayers_start" in _gl or "getlayers_search" in _gl or "getlayers_materialize" in _gl:
    ERRORS.append("license: getlayers skill invokes getlayers_* MCP tools (the MCP is not wired — prompt path only)")
if "mcp.getlayers.ai" in _gl and "NOT wired" not in _gl and "No MCP" not in _gl:
    ERRORS.append("license: getlayers skill references the MCP without the not-wired guard")
for _fig in FROZEN_GETLAYERS:
    if _fig in _gl:
        ERRORS.append(f"license: frozen GetLayers count {_fig!r} in skills/getlayers/SKILL.md (counts drift — read llms.txt live)")
# No React Bits component source anywhere in the new skill dir (only the
# skill doc itself + nothing else — the dir must contain exactly SKILL.md).
_rb_files = sorted(os.listdir(p("skills/react-bits")))
if _rb_files != ["SKILL.md"]:
    ERRORS.append(f"license: skills/react-bits/ must contain only SKILL.md, found {_rb_files}")
for _path, _text in _walk_files():
    if _text is None:
        continue
    _rel = os.path.relpath(_path, BASE)
    if _rel.startswith("skills/react-bits/") and _rel != "skills/react-bits/SKILL.md":
        ERRORS.append(f"license: unexpected file in react-bits skill dir: {_rel}")
    if _rel.startswith("skills/gsap/") and _rel != "skills/gsap/SKILL.md":
        ERRORS.append(f"license: unexpected file in gsap skill dir: {_rel} (GSAP source is never vendored)")
    if _rel.startswith("skills/getlayers/") and _rel != "skills/getlayers/SKILL.md":
        ERRORS.append(f"license: unexpected file in getlayers skill dir: {_rel} (no GetLayers content vendored)")
# No GSAP source vendored anywhere in the built tree (the package is
# npm-only). Precise: a GSAP source file (gsap.js / gsap.min.js / gsap.ts).
# (skills/design-taste-frontend/assets/icons/demo/gsap.svg is an icon, not
# source, and must NOT trip this check.)
for _path, _text in _walk_files():
    if _text is None:
        continue
    _rel = os.path.relpath(_path, BASE)
    if os.path.basename(_path).lower() in ("gsap.js", "gsap.min.js", "gsap.ts"):
        ERRORS.append(f"license: vendored GSAP source file: {_rel}")
if not ERRORS:
    CHANGES.append("license: no MCP calls / no frozen GetLayers counts; react-bits + gsap + "
                  "getlayers skill dirs contain only their SKILL.md (no vendored source)")

# 1g. README + trigger pre-state (67, about to become 72).
_readme = read(p("README.md"))
if "67 skills, 45 agents, 48 rules, and 55 commands in total" not in _readme:
    ERRORS.append("census: README count line does not show 67 skills (pre-patch state unexpected)")
_trig = json.load(open(p("manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
if _trig["coverage"]["skills"] != 67 or _trig["coverage"]["withTriggers"] != 49:
    ERRORS.append(f"census: trigger coverage pre-state is {_trig['coverage']}, expected skills 67 / withTriggers 49")
if ERRORS:
    _log_lines = ["# fix31 run log", "",
                  f"## Errors ({len(ERRORS)})"]
    _log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
    _log_lines += ["", "## Changes (0)", "- none", "",
                   "## Command decisions (0)", "- none", "",
                   "## OWED (0)", "- none"]
    _log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix31")
    os.makedirs(_log_dir, exist_ok=True)
    with open(os.path.join(_log_dir, "fix31-patch-log.md"), "w",
              encoding="utf-8") as _fh:
        _fh.write("\n".join(_log_lines) + "\n")
    print(f"fix31: {len(ERRORS)} ERROR(S) in census — no files written",
          file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------- 2. Writes: README + trigger
sub(p("README.md"),
    "67 skills, 45 agents, 48 rules, and 55 commands in total",
    "72 skills, 45 agents, 48 rules, and 55 commands in total")
sub(p("README.md"),
    "67 skills widen the routing surface",
    "72 skills widen the routing surface")
sub(p("README.md"),
    "56 MB and 67 skills against a minimal set",
    "56 MB and 72 skills against a minimal set")
sub(p("README.md"),
    "structured process — 67 skills, 45 agents, 55 commands,",
    "structured process — 72 skills, 45 agents, 55 commands,")
# Fix #31 provenance note, appended after the codebase-memory line (:28),
# following the fix28 pattern. Carries the four built-tree _F31 tokens.
_lines = read(p("README.md")).split("\n")
_idx = next((i for i, _ln in enumerate(_lines)
             if _ln.startswith("- **Codebase memory**")), None)
if _idx is None:
    ERRORS.append("README: codebase-memory note line not found for fix31 note insert")
else:
    _note = ("- **Fix #31 design libraries (Nov 17, 2026)** — GetLayers (free set only), "
             "GSAP, React Bits, and Hairline illustrations added to the palette-first "
             "inventory. Skills are now 72. "
             "(`GETLAYERS_F31` `GSAP_F31` `REACTBITS_F31` `HAIRLINE_F31`)")
    if _note in _lines:
        ERRORS.append("README: fix31 note line already present (double run?)")
    else:
        _lines.insert(_idx + 1, _note)
        write(p("README.md"), "\n".join(_lines))
        CHANGES.append("README: fix31 provenance note added after the codebase-memory line")

_tf = p("manifests/context-packs/skill-triggers@1.json")
with open(_tf, encoding="utf-8") as _fh:
    _trig = json.load(_fh)
_trig["coverage"]["skills"] = 72
_trig["coverage"]["withTriggers"] = len(_trig["triggers"])
with open(_tf, "w", encoding="utf-8") as _fh:
    json.dump(_trig, _fh, indent=1, ensure_ascii=True)
    _fh.write("\n")
CHANGES.append("trigger coverage.skills 67 -> 72 (withTriggers stays 49 — no trigger keys for the new skills)")

# ---------------------------------------------------------------- 3. Post-assertions
_readme = read(p("README.md"))
for _line in ("72 skills, 45 agents, 48 rules, and 55 commands in total",
              "72 skills widen the routing surface",
              "56 MB and 72 skills against a minimal set",
              "structured process — 72 skills, 45 agents, 55 commands,"):
    if _line not in _readme:
        ERRORS.append(f"post: README missing 72-count line: {_line[:50]!r}")
_stale67 = _readme.count("67 skills")
if _stale67:
    ERRORS.append(f"post: README still says '67 skills' {_stale67}x")
if "144 skills, 69 agents, 121 rules, 94 commands" not in _readme:
    ERRORS.append("post: README stock-ECC line (144 skills ...) was disturbed")
_trig = json.load(open(_tf, encoding="utf-8"))
if _trig["coverage"]["skills"] != 72 or _trig["coverage"]["withTriggers"] != 49:
    ERRORS.append(f"post: trigger coverage is {_trig['coverage']}, expected skills 72 / withTriggers 49")
# Zero "67 skills" anywhere in the built tree (README was the only carrier).
for _path, _text in _walk_files():
    if _text is None:
        continue
    if "67 skills" in _text:
        ERRORS.append(f"post: stale '67 skills' in {os.path.relpath(_path, BASE)}")
        break
# DESIGNPKG-AUTO + GLOBAL-ROUTING guards (post).
_b1 = _block(read(p("skills/orchestrate/SKILL.md")), "**DESIGNPKG-AUTO")
_b2 = _block(read(p("rules/hackathon-mode.mdc")), "**DESIGNPKG-AUTO")
if _b1 is None or _b1 != _b2:
    ERRORS.append("post: DESIGNPKG-AUTO block no longer byte-identical in orchestrate + hackathon-mode")
_g1 = _block(read(p("skills/orchestrate/SKILL.md")), "**GLOBAL-ROUTING")
_g2 = _block(read(p("rules/hackathon-mode.mdc")), "**GLOBAL-ROUTING")
if _g1 is None or _g1 != _g2:
    ERRORS.append("post: GLOBAL-ROUTING block no longer byte-identical in orchestrate + hackathon-mode")
if not ERRORS:
    CHANGES.append("post: README 72 in all 4 lines, zero '67 skills' tree-wide; trigger "
                  "coverage 72/49; DESIGNPKG-AUTO + GLOBAL-ROUTING blocks byte-identical")

# ---------------------------------------------------------------- Decisions + OWED
DECISIONS = [
    "DECISION-31-1 (SPEC scope): five new skills, not four — Hairline is two skills (hairline-create + hairline-adopt) per the SPEC; GetLayers, GSAP, and React Bits are one skill each. Skills 67 -> 72; agents 45, rules 48, commands 55, hooks 15, triggers 49 unchanged.",
    "DECISION-31-2 (GSAP version): the SPEC's 3.15.0 (Apr 2026) is superseded — npm latest is 3.15.1 (verified Nov 17, 2026), matching the inventory's existing pin. The skill pins gsap@3.15.1. The SPEC is corrected with a strikethrough note (audit #97-A to confirm).",
    "DECISION-31-3 (GetLayers counts): live counts drifted in one day (llms.txt Nov 17: 62 templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088 gradients vs the SPEC's 50 / 114 / 10 / 276 / 1,088) — the SPEC's own no-frozen-counts rule is confirmed necessary. The skill carries NO counts; verify31 forbids the frozen Nov 16 figures.",
    "DECISION-31-4 (staged weave, not built-tree patching): the palette / DESIGNPKG-AUTO / inventory edits are staged sources (fix31/weave31.py, run once) flowing through the STEP 2 copy — the same pattern as fix29's staged halves. fix31.py only asserts the built tree + updates the generated files (README, trigger) that no staged source owns.",
    "DECISION-31-5 (GSAP skills not vendored): the official gsap-skills repo (8 skills, MIT) is reference, not vendored — vendoring 8 skills would take the count to 80 for API detail this plugin's single gsap skill routes to by link. The skill's reference table names the skill per need. If a future fix finds agents need the API text in-tree, vendoring is a separate decision.",
    "DECISION-31-6 (React Bits install): the CLI installs from the live repo (per the SPEC), not the fix22 pinned commit — the installed copy in the project IS the pin, recorded in the decision record. The fix22 commit stays as the reviewed baseline in the skill and the inventory.",
    "DECISION-31-7 (GetLayers weight — direction update, Anish Nov 16 ~10:02 PM): GetLayers prompts are a first-class, high-priority source in the palette-first flow — consulted FIRST, before the other palette sources, and the direction leans on the layers heavily as its foundation. Visible three ways: ordering (getlayers first in every palette list), priority language (in the skill + the DESIGNPKG-AUTO gloss + the inventory §12), and the citation check (the direction names the GetLayers layers USED or CONSIDERED-AND-REJECTED with a D19 reason, same as every inventory entry). Weight is about consultation order and foundation weight, NOT about forcing a layer: a surface with no fitting free layer records `not considered — <reason>`, same as any entry. Constraints unchanged: free set only, no vendored content, foundation not finished brand.",
]
OWED = [
    "OWED-31-1 (SPEC Honest limits): live behavior of the four resources is unverified until real project use — the live smoke test is still skipped since Nov 15. The dry-run design leg (dry-run #46) is static + install-verified, not a live Cursor build.",
    "OWED-31-2 (GetLayers MCP): the MCP stays unwired — it requires the Full Stack Lifetime plan. If Anish ever buys Full Stack, MCP wiring is a separate decision; the skill's prompt path is the free path.",
    "OWED-31-3 (call map, same as OWED-30-4): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the new skills are leaf resources (invoked by the design-lead), not dispatchers; no new orchestration edges, so the fix28 map stands. If the audit finds the DESIGNPKG-AUTO additions are dispatch edges, regeneration is the fix.",
    "OWED-31-4 (Hairline 'six figures' text): the vendored hairline-create SKILL.md says 'The six figures of @lucasmarkes/hairline are the bar' — upstream's text about the original six; the library now ships 33 figures. Left as upstream wrote it (the vendored copy is unmodified apart from the framing header).",
]

# ---------------------------------------------------------------- main / run log
_log_lines = ["# fix31 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
_log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
_log_lines += ["", f"## OWED ({len(OWED)})"]
_log_lines += [f"- {o}" for o in OWED] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix31")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix31-patch-log.md"), "w",
          encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix31: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix31: {len(OWED)} OWED item(s) recorded in the patch log")
if ERRORS:
    print(f"fix31: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix31: OK")
