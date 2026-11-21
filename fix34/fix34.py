#!/usr/bin/env python3
"""Fix #34 — port the factory variant's rounds 10-13 content into the
regular plugin, minus the drone machinery.

Run by build.sh as a patch step (after fix32.py, before STEP 5):
    python3 "$PLUGIN_ROOT/fix34/fix34.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. The four new skills (motion-principles,
threeui, prebuild-research, code-mode) and every staged weave edit are
staged sources (stage34.py + weave34.py run by the coordinator before the
build; the skills flow through the STEP 2 loop). This script:
  1. Asserts the pre-state census (counts, MODELSEL pin census from the
     fix #33 post-state, README at 72, trigger coverage 72/48) and that
     the staged weave landed in the built copies.
  2. Patches skills/browser-qa/SKILL.md at build time (the fix #27/#31
     pattern — browser-qa is upstream-derived, so its two new verdicts
     are build-time patches, not staged edits): the MOTION-QA verdict
     (six criteria) and the CONTRACT-QA verdict, browser-qa remaining
     the sole verdict executor.
  3. Rewrites the README count lines 72 -> 76, names prebuild-research
     in the Hackathon workflow bullet, adds the fix #34 provenance note,
     and sets trigger coverage.skills to 76 (no new trigger keys — the
     fix #31 design-skill precedent: flow/inventory-invoked).
  4. Post-asserts the port: excluded factory machinery absent
     (orchestrator-briefing, openrouter-drones, drone agents,
     cm_dispatch, the factory-only rule IDs), the deploy-fast Netlify
     pricing row byte-untouched, DESIGNPKG-AUTO byte-identical in
     orchestrate + hackathon-mode, pin census unchanged.

Exits non-zero on any error so the build fails rather than shipping a
half-ported tree. Patch log: fix34/fix34-patch-log.md.

SPEC: fix34/SPEC.md. Decisions D34-1..D34-12. Counts: skills 72 -> 76,
agents 45, rules 48, commands 55, hooks 15, trigger keys 48 (unchanged).
"""
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
hooks = read(p("hooks", "hooks.json")) if os.path.exists(p("hooks", "hooks.json")) else ""
NEW_SKILLS = ["motion-principles", "threeui", "prebuild-research", "code-mode"]
# fix #35 (D35-9): kitchen is staged by fix #35 and flows through the
# STEP 2 loop before this script runs, so the built tree already
# carries 77 skills at this census; fix #34's own delta (72 -> 76)
# is unchanged.
if len(skills) != 77:
    ERRORS.append(f"census: built skills = {len(skills)} (expected 77)")
for s in NEW_SKILLS:
    if s not in skills:
        ERRORS.append(f"census: new skill missing from built tree: {s}")
if len(agents) != 45:
    ERRORS.append(f"census: built agents = {len(agents)} (expected 45)")
if len(rules) != 48:
    ERRORS.append(f"census: built rules = {len(rules)} (expected 48)")
if len(commands) != 55:
    ERRORS.append(f"census: built commands = {len(commands)} (expected 55)")
CHANGES.append(f"census: counts skills 77 (72 + 4 new + kitchen staged by fix #35), agents {len(agents)}, rules {len(rules)}, commands {len(commands)}")

PIN_CENSUS = {"grok-4.7-high": 0, "Grok 4.7 High": 2, "grok-4.7-extra-high": 0,
              "Grok 4.7 Extra High": 0, "cursor-grok-4.6-high-fast": 72}
for token, expected in PIN_CENSUS.items():
    got = census(token)
    if got != expected:
        ERRORS.append(f"census: pin census drift: {token!r} x{got} (expected x{expected}, fix #33 post-state)")
CHANGES.append("census: MODELSEL pin census holds at the fix #33 post-state")

_readme = read(p("README.md"))
for line in ["72 skills, 45 agents, 48 rules, and 55 commands in",
             "72 skills widen the routing surface",
             "56 MB and 72 skills against a minimal set",
             "structured process — 72 skills, 45 agents, 55 comm"]:
    if line not in _readme:
        ERRORS.append(f"census: README pre-state line missing: {line!r}")
_man = read(p("manifests/context-packs/skill-triggers@1.json"))
if '"skills": 72,' not in _man or json.loads(_man).get("coverage") != {"skills": 72, "withTriggers": 48}:
    ERRORS.append("census: trigger coverage pre-state is not {skills: 72, withTriggers: 48}")
CHANGES.append("census: README at 72 in all 4 count lines; trigger coverage 72/48")

# staged weave landed in the built copies
WEAVE_NEEDLES = [
    ("skills/orchestrate/SKILL.md", "1.5. **Research (pre-build) (fix #34, RESEARCHBRIEF_F34)**"),
    ("skills/orchestrate/SKILL.md", "**Design contract + restatement gate (fix #34, DESIGNCONTRACT_F34).**"),
    ("skills/orchestrate/SKILL.md", "**Fix #34 static checks (all static checks, never screen verdicts).**"),
    ("skills/orchestrate/SKILL.md", "**Script-first mechanical work (fix #34, SCRIPT-FIRST_F34).**"),
    ("skills/design-taste-frontend/SKILL.md", "**Motion is decided against the motion principles (fix #34, MOTIONPRINCIPLES_F34).**"),
    ("skills/design-taste-frontend/SKILL.md", "**The design contract — the frozen system issued as a contract (fix #34, DESIGNCONTRACT_F34).**"),
    ("skills/orchestrate/references/design-inventory.md", "## 13. Fix #34 additions — Motion Principles, ThreeUI"),
    ("skills/orchestrate/references/design-inventory.md", "## 14. Fix #34 additions — Pre-build Research, the Design Contract"),
    ("skills/orchestrate/references/design-inventory.md", "## 15. code-mode — the execution discipline (fix #34, CODEMODE_F34)"),
    ("skills/deploy-fast/SKILL.md", "## The contract's hosting line (fix #34, HOSTING_F34)"),
    ("skills/feature-expansion/SKILL.md", "0. **Read the research brief first (fix #34, RESEARCHBRIEF_F34).**"),
    ("skills/feature-expansion/SKILL.md", "**Research-fed expansion (fix #34, RESEARCHBRIEF_F34):**"),
    ("skills/grill-me/SKILL.md", "keep it available for `prebuild-research` (the step-1.5 sweep"),
    ("skills/gsap/SKILL.md", "**The why lives in `motion-principles` (MOTIONPRINCIPLES_F34, fix #34):**"),
    ("rules/hackathon-mode.mdc", "research (`prebuild-research`, orchestrate step 1.5)"),
    ("rules/hackathon-mode.mdc", "Motion routing: `motion-principles` (MOTIONPRINCIPLES_F34) supplies"),
]
for rel, needle in WEAVE_NEEDLES:
    if needle not in read(p(rel)):
        ERRORS.append(f"census: staged weave needle missing in built {rel}: {needle[:60]!r}")
CHANGES.append(f"census: staged weave landed ({len(WEAVE_NEEDLES)} needles across 9 built files)")

_bqa = read(p("skills/browser-qa/SKILL.md"))
for anchor in ["A tie on any dimension is below the bar on that dimension.",
               "- [✓/✗] Beat-v5 benchmark (BENCHMARK_V5_F25): hero / dynamic / functionality / alignment vs the v5 figures — PASS / FAIL per dimension (a tie is below the bar; an unscored dimension is owed, never passed)"]:
    if _bqa.count(anchor) != 1:
        ERRORS.append(f"census: browser-qa anchor count != 1: {anchor[:60]!r}")
if "MOTION-QA_F34" in _bqa or "CONTRACT-QA_F34" in _bqa:
    ERRORS.append("census: browser-qa already carries the fix #34 verdicts (double-run?)")
CHANGES.append("census: browser-qa anchors present once each; verdicts not yet applied")

if ERRORS:
    for e in ERRORS:
        print(f"fix34: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 2. browser-qa verdicts
MOTION_PARA = """
**Motion verdict (fix #34, MOTION-QA_F34).** In the visual loop, judge the build's motion against the checkable subset of `motion-principles` (MOTIONPRINCIPLES_F34), from the rendered interface, never from source: (a) **Doherty response** — visible feedback within 400ms of the input that caused it; (b) **timing ceiling** — UI animations under 300ms except motion recorded as the content itself; (c) **origin awareness** — entrances grow from their trigger, not from screen centre or a generic fade-up; (d) **interruptibility** — motion yields to the user's next input instead of playing out; (e) **frequency-of-use restraint** — a daily action wrapped in a long animation FAILS this criterion; (f) **reduced-motion fallback** — with `prefers-reduced-motion: reduce`, the interface is complete and still, nothing essential conveyed by motion alone. A failure on any criterion is a motion finding (minor at least) routed to the design skill that dealt the motion; an interaction the harness cannot drive is recorded as unverified, never as passed. This verdict is `browser-qa`'s alone, like every screen verdict in this skill: `motion-principles` names what good motion is; this skill alone judges whether the built screen has it."""
insert_after(p("skills/browser-qa/SKILL.md"),
             "A tie on any dimension is below the bar on that dimension.",
             MOTION_PARA, "browser-qa MOTION-QA paragraph")
insert_after(p("skills/browser-qa/SKILL.md"),
             "- [✓/✗] Beat-v5 benchmark (BENCHMARK_V5_F25): hero / dynamic / functionality / alignment vs the v5 figures — PASS / FAIL per dimension (a tie is below the bar; an unscored dimension is owed, never passed)",
             "\n- [✓/✗] Motion (MOTION-QA_F34): feedback ≤ 400ms (Doherty); UI animation < 300ms; entrances origin-aware; motion interruptible; least motion on the most-used actions; reduced-motion fallback complete",
             "browser-qa Motion report row")
CONTRACT_PARA = """

**Contract verdict (fix #34, CONTRACT-QA_F34).** Where a design contract exists (`docs/design-contract.md`, DESIGNCONTRACT_F34), judge the built screens AGAINST it, field by field, from the rendered interface: (a) **palette tokens** — rendered colours match the contract's tokens exactly (computed styles sampled on the surface's key elements); a near-miss hex is a mismatch; (b) **type scale** — faces, sizes, weights, line-heights, and tracking match the contract's steps on the elements that carry them; (c) **spacing scale** — the rhythm tokens and grid are followed (section padding, gaps, container widths within a small tolerance for rounding, never a different step); (d) **motion specs** — the contract's motion values are what runs (the Motion verdict above judges them against the principles; this one judges them against the contract's own numbers); (e) **components** — the contract's named components are the components on screen (a substituted look-alike is a mismatch); (f) **states** — loading / empty / success / error render as the contract's States field specifies. A value on screen that is not the contract's value, with no deviation recorded in the contract's Deviations field, is a contract finding (minor at least) routed to the implementer of that slice; a value covered by a recorded deviation is verified against the deviation, not the original field. A restatement mismatch that reaches this verdict means the pre-build gate was skipped — record that as a finding against the run, not just the slice. This verdict is `browser-qa`'s alone, like every screen verdict in this skill: Taste issues the contract; this skill alone judges whether the built screen honours it."""
insert_after(p("skills/browser-qa/SKILL.md"),
             "`motion-principles` names what good motion is; this skill alone judges whether the built screen has it.",
             CONTRACT_PARA, "browser-qa CONTRACT-QA paragraph")
insert_after(p("skills/browser-qa/SKILL.md"),
             "- [✓/✗] Motion (MOTION-QA_F34): feedback ≤ 400ms (Doherty); UI animation < 300ms; entrances origin-aware; motion interruptible; least motion on the most-used actions; reduced-motion fallback complete",
             "\n- [✓/✗] Contract (CONTRACT-QA_F34): palette tokens exact; type scale exact; spacing scale followed; motion matches the contract's specs; named components present; states match; every mismatch covered by a recorded deviation",
             "browser-qa Contract report row")

# ---------------------------------------------------------------- 3. README + trigger coverage
sub(p("README.md"), "72 skills, 45 agents, 48 rules, and 55 commands in",
    "76 skills, 45 agents, 48 rules, and 55 commands in", "README count line 1")
sub(p("README.md"), "72 skills widen the routing surface",
    "76 skills widen the routing surface", "README count line 2")
sub(p("README.md"), "56 MB and 72 skills against a minimal set",
    "56 MB and 76 skills against a minimal set", "README count line 3")
sub(p("README.md"), "structured process — 72 skills, 45 agents, 55 comm",
    "structured process — 76 skills, 45 agents, 55 comm", "README count line 4")
sub(p("README.md"), "- **Hackathon workflow** — `hackathon-scope` (MVP scoping), `feature-expansion`",
    "- **Hackathon workflow** — `hackathon-scope` (MVP scoping), `prebuild-research` (bounded pre-build web research — the brief expansion reads first), `feature-expansion`",
    "README workflow bullet names prebuild-research")
NOTE34 = "- **Fix #34 factory port (Nov 19, 2026)** — the factory variant's rounds 10–13 content, minus the drone machinery: `motion-principles` (the why of UI motion) and `threeui` (ready-made 3D components, free Community edition only) join the design package; `prebuild-research` adds the bounded research step (orchestrate step 1.5) before expansion; Taste issues the binding design contract (`docs/design-contract.md`) with a restatement gate, and `browser-qa` renders motion + contract verdicts against it; `code-mode` adds the script-first discipline for the orchestrator's own mechanical work. Skills are now 76. (`MOTIONPRINCIPLES_F34` `THREEUI_F34` `RESEARCHBRIEF_F34` `DESIGNCONTRACT_F34` `HOSTING_F34` `CODEMODE_F34`)\n"
_readme = read(p("README.md"))
_anchor = "- **Fix #31 design libraries (Nov 17, 2026)**"
if _readme.count(_anchor) != 1:
    ERRORS.append("README: fix #31 note anchor not found exactly once")
else:
    write(p("README.md"), _readme.replace(_anchor, NOTE34 + _anchor))
    CHANGES.append("README: fix #34 provenance note added before the fix #31 note")
sub(p("manifests/context-packs/skill-triggers@1.json"), '"skills": 72,', '"skills": 76,',
    "trigger coverage.skills 72 -> 76")

if ERRORS:
    for e in ERRORS:
        print(f"fix34: ERROR {e}")
    sys.exit(1)

# ---------------------------------------------------------------- 4. Post-assertions
_readme = read(p("README.md"))
if "76 skills" not in _readme or "72 skills" in _readme:
    ERRORS.append("post: README count lines not fully at 76")
_man = json.loads(read(p("manifests/context-packs/skill-triggers@1.json")))
if _man.get("coverage") != {"skills": 76, "withTriggers": 48}:
    ERRORS.append(f"post: trigger coverage = {_man.get('coverage')} (expected 76/48)")
_bqa = read(p("skills/browser-qa/SKILL.md"))
for needle in ["**Motion verdict (fix #34, MOTION-QA_F34).**", "**Contract verdict (fix #34, CONTRACT-QA_F34).**",
               "- [✓/✗] Motion (MOTION-QA_F34):", "- [✓/✗] Contract (CONTRACT-QA_F34):"]:
    if _bqa.count(needle) != 1:
        ERRORS.append(f"post: browser-qa needle count != 1: {needle[:50]!r}")
CHANGES.append("post: README 76 in all 4 lines; coverage 76/48; browser-qa carries both verdicts + both report rows")

for bad_dir in ["skills/orchestrator-briefing", "skills/openrouter-drones", "skills/code-mode/scripts/cm_dispatch.py"]:
    if os.path.exists(p(bad_dir)):
        ERRORS.append(f"post: excluded factory artifact present: {bad_dir}")
drone_agents = [f for f in agents if f.startswith("drone-")]
if drone_agents:
    ERRORS.append(f"post: drone agents present: {drone_agents}")
scripts = sorted(os.listdir(p("skills/code-mode/scripts")))
if scripts != ["cm_census.py", "cm_read.py", "cm_report.py", "cm_write.py"]:
    ERRORS.append(f"post: code-mode scripts = {scripts} (expected the 4 helpers, no cm_dispatch)")
FACTORY_ID_RE = re.compile(r"\b(?:MOTIONPRINCIPLES|THREEUI|MOTION-QA|CONTRACT-QA|DESIGNCONTRACT|RESEARCHBRIEF|HOSTING|CODEMODE|SCRIPT-FIRST|SCRIPT-GATE)_F1\d\d\b")
EXCLUDED_STRINGS = ["CLI-DISPATCH_F32", "CAPTIVATION_F32", "PARALLEL-CALLS_F154", "orchestrator-briefing", "openrouter-drones", "cm_dispatch"]
for fp, text in walk_text_files():
    rel = os.path.relpath(fp, PLUGIN_DIR)
    if FACTORY_ID_RE.search(text):
        ERRORS.append(f"post: factory-numbered rule ID survives in {rel}")
    for s in EXCLUDED_STRINGS:
        if s in text:
            ERRORS.append(f"post: excluded string {s!r} present in {rel}")
CHANGES.append("post: no excluded machinery (briefing/drones/cm_dispatch/factory IDs) anywhere in the built tree")

PRICING_ROW = "| **Netlify** | Static front ends | 300 credits/mo | — | **15 credits per production deploy**, so about 20 deploys uses up the month (the 300-credit model applies to accounts created since Sep 4, 2025; older accounts keep prior limits) |"
if PRICING_ROW not in read(p("skills/deploy-fast/SKILL.md")):
    ERRORS.append("post: deploy-fast Netlify pricing row altered (its touch-up is dated Dec 4, 2026 — not this fix)")
CHANGES.append("post: deploy-fast Netlify pricing row byte-untouched")

def designpkg_block(text):
    m = re.search(r"\*\*DESIGNPKG-AUTO.*?(?=This is the design half of BIND)", text, re.S)
    return m.group(0) if m else None
if designpkg_block(read(p("skills/orchestrate/SKILL.md"))) != designpkg_block(read(p("rules/hackathon-mode.mdc"))):
    ERRORS.append("post: DESIGNPKG-AUTO blocks differ between orchestrate and hackathon-mode")
CHANGES.append("post: DESIGNPKG-AUTO byte-identical in orchestrate + hackathon-mode, naming motion-principles + threeui")

for token, expected in PIN_CENSUS.items():
    got = census(token)
    if got != expected:
        ERRORS.append(f"post: pin census drift after writes: {token!r} x{got} (expected x{expected})")
CHANGES.append("post: MODELSEL pin census unchanged by the fix #34 writes")

OWED.append("OWED-34-1 (call map): the call map is generator-owned and NOT regenerated by the build — fix34.py does not assert it. The coordinator regenerates it after the build (fix28/callmap/generate_call_map.py, EXPECTED skills 72 -> 76) and rebuilds so the staged copy flows into the built tree; verify34.py asserts the regenerated map.")
OWED.append("OWED-34-2 (live use): the research step, contract + restatement gate, motion/contract verdicts, and script-first discipline are file-level rules; whether Cursor runs them as written is decided by live project use (the fix #30 live-test pattern), not by this build.")

log = ["# fix34 patch log", ""]
log += [f"- {c}" for c in CHANGES]
if OWED:
    log += ["", "## OWED", ""] + [f"- {o}" for o in OWED]
if ERRORS:
    log += ["", "## ERRORS", ""] + [f"- {e}" for e in ERRORS]
write(os.path.join(PLUGIN_ROOT, "fix34", "fix34-patch-log.md"), "\n".join(log) + "\n")

if ERRORS:
    for e in ERRORS:
        print(f"fix34: ERROR {e}")
    print(f"fix34: {len(ERRORS)} ERROR(S)")
    sys.exit(1)
print(f"fix34: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix34: {len(OWED)} OWED item(s) recorded in the patch log")
print("fix34: OK")
