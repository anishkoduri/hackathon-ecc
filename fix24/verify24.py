#!/usr/bin/env python3
"""verify24.py -- checks fix #24 in the BUILT tree (read-only).

Run after a build: python3 fix24/verify24.py
Exits 0 only if every check passes.

Fix #24 is a coherence fix: it re-weaves the whole plugin as one system
and dials it in for Cursor. It adds no new skill/command/rule/agent/hook
and no new anchor-token family; it removes contradictions, aligns counts,
wires orphan anchors, and makes agent references robust to either Cursor
resolution. Checks, against ~/workspace/hackathon-plugin/hackathon-ecc
(+ build.sh where the SPEC says so):

  1. SS1(a) pointers/anchors: orphan tokens A1-A9 resolved (ANIM_TOKENS_F22
     in the inventory; FUNC-UIPRO/FUNC-BQA/HERO-BQA/MOBBIN_QA cited from
     orchestrate; TRIO_F23 in typeset.md + browser-qa; BANG_* index + headings;
     ALIGN_F23_* sub-checks in browser-qa; slop-checklist link fixed;
     screen-demo.yaml SYNTHETIC note; DEMOGATE pairings recorded).
  2. SS1(b) dedupe/contradiction: C1 APCA informational; C2 Rule 5 vs B3
     scope split; C3 B15 exitFactor single source of truth; C4b seven
     dimensions in every editable spot with the frozen six-texts intact;
     C5 commit in the first-build sequence; C6 FILM_F1 disambiguated;
     C7 MOTION_F23 scope qualifiers; S1 styles.csv 80/89 discrepancy
     asserted as-is (OWED, verifier change is a parent decision).
  3. SS1(c) one-story flow: F-01 resume guards; F-02 step-0 executor;
     F-03 Verify steps 1-4b named in 5a; F-04 Verify stage 6 (not step 6);
     F-05 Gate-1 anchor gone; F-06 count-convention lines; F-07 final-report
     +4 bullets; F-08 step-6 order governs; F-09 readme-writer ledger;
     F-10 inventory pointers (Taste step 4a + ui-ux-pro-max); F-11
     feature-expansion Phase 4 inventory clause; F-12 single Lenses block;
     F-13 5b Hallmark redesign.md wire; F-15 F6 qualifier (verify23
     substring survives). F-14 is a parent call -- asserted via the manifest.
  4. SS2(a) agent refs: 19 path lines dual-cited in commands/ (+ plan.md:199
     already house form); house-form invocations; general-purpose gone
     (general subagent); design-lead invocations gone; fallback paragraph;
     duplicate architect row merged.
  5. SS2(b) pins: 72 agent frontmatter pins slug-form Grok (4 x 4.7-high,
     68 x cursor-4.6-high-fast); picker prerequisite stated once in
     orchestrate step 4, pointers elsewhere.
  6. SS2(c) hooks: C-1 powershellRole/cmdRole; C-2/C-3 header notes;
     D-8 harness-audit reword; D-9 angular mcp note. D-6 recorded open.
  7. SS2(d) Claude scrub: D-1 10x Upstream-only; D-2 zero Cursor-only in
     scripts/hooks/; banned terms 0.
  8. SS2(e) Windows paths: E-1/E-2/E-3/E-4/E-5/E-6/E-7.
  9. SS2(f) loading: README Updating section, single authoritative place.
 10. SS2(g) commands: G-1/G-2/G-3/G-4; /demo gates intact.
 11. Global: build.sh fingerprint (24,070 lines, md5 b0b2645a...); diff
     vs build.sh.before-fix23 additions only (+296/-0); counts
     166/72/123/87/15, trigger keys 64; banned terms 0; bare
     grok-4.6-high-fast absent; Grok pin file counts 27/86 (common-agents.mdc
     gained both pins via the fix #24 fallback paragraph); /demo gates.
 12. Prior-verifier regression leg: fix15/17/18/19/20/21/22/23 re-run.
     EXPECTED fails are ONLY: the frozen post-fix21 build.sh fingerprint
     line(s), the post-fix22 build.sh fingerprint line, the post-fix23
     build.sh fingerprint line + its diff-count line + its pin-count line
     (all three are intended fix #24 changes, recorded in the manifest),
     verify22's B3/B15 conflict-flag checks (fix #24's C2/C3 adjudications
     replaced the flags by design), verify23's eleven exact _F23 count
     checks (fix #24's SPEC-mandated orphan citations moved the counts;
     the new counts are asserted in §11), verify23's manifest check
     (its manifest records fix23's build.sh) and its fix22-leg line
     (carries fix22's new tail), the less-flat-ui diff-hunk pattern, and
     cascades of those. Two fix #24 worker errors were caught by this leg
     and REVERTED, not excused: I-DESIGN's C4b seven-edit inside the frozen
     POLISH_F19 text and I-ORCH's C4b seven-edit inside the frozen
     D19_ROUTING line (Worker B's "routing:163 is editable" call was wrong
     -- verify19 asserts D19_ROUTING verbatim). Both lines are byte-identical
     to the frozen constants again; the count-convention line governs the
     seven reading. See the manifest §4.
 13. Manifest check (fix22 pattern): runs once fix24/MANIFEST.md exists.
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
from fix19 import D19_RULE, D19_ROUTING, F2_RULE  # noqa: E402

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


def count_substring_in_tree(sub, dirs=("skills", "agents", "commands", "rules", "hooks")):
    n = 0
    for d in dirs:
        for root, _dirs, files in os.walk(os.path.join(BASE, d)):
            _dirs[:] = [x for x in _dirs if x != "node_modules"]
            for fn in files:
                try:
                    t = open(os.path.join(root, fn), encoding="utf-8", errors="strict").read()
                except (UnicodeDecodeError, ValueError):
                    continue
                n += t.count(sub)
    return n


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
gates = read("skills/design-taste-frontend/references/hallmark/references/gates.md")
fe = read("skills/feature-expansion/SKILL.md")
grill = read("skills/grill-me/SKILL.md")
readme_writer = read("skills/readme-writer/SKILL.md")
demo = read("commands/demo.md")
orch_cmd = read("commands/orchestrate.md")
common_agents = read("rules/common-agents.mdc")
plankton = read("skills/plankton-code-quality/SKILL.md")
auto_update = read("skills/ecc-recipes/SKILL.md")
bnv = read("scripts/hooks/block-no-verify.js")
harness = read("scripts/harness-audit.js")
angular_mcp = read("skills/angular-developer/references/mcp.md")
readme = read("README.md")
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()

# 1. SS1(a) pointers/anchors.
check("A1 ANIM_TOKENS_F22 cited in the inventory",
      "ANIM_TOKENS_F22" in inv)
check("A2/A3/A4/A6 orphans cited from orchestrate SKILL.md",
      "FUNC-UIPRO_F23" in orch and "FUNC-BQA_F23" in orch
      and "HERO-BQA_F23" in orch and "MOBBIN_QA_F22" in orch)
check("A5 TRIO_F23 in typeset.md + browser-qa citation",
      "TRIO_F23" in typeset and "TRIO_F23" in bqa)
check("A7 BANG_* index line + four section headings in pitch-deck-video",
      "BANG_ANTISLIDE_F22" in pitch and "BANG_ONEWORLD_F22" in pitch
      and "BANG_KINETIC_F22" in pitch and "BANG_EXPLAINER_F22" in pitch
      and "grouped under six tokens" in pitch)
check("A8 ALIGN_F23_* sub-checks cited from browser-qa",
      all(s in bqa for s in ("ALIGN_F23_NAV", "ALIGN_F23_LABELS",
                             "ALIGN_F23_CLIP", "ALIGN_F23_ACTIONS",
                             "ALIGN_F23_PANELS")))
check("A9 DEMOGATE pairings recorded (O4<->H2, O9<->H1)",
      "DEMOGATE locator pairings (fix #24): O4 pairs with H2, O9 pairs with H1" in orch)
check("C1 slop-checklist link fixed (lenses/typeset.md)",
      "[reference/lenses/typeset.md](lenses/typeset.md)" in slop
      and "(reference/lenses/typeset.md)" not in slop)
check("C2 SYNTHETIC mode documented inoperable in runtime-fetch.md",
      "synthetic-screen-recording" in read(
          "skills/pitch-deck-video/references/openmontage/runtime-fetch.md")
      and "Does NOT ship in the plugin" in read(
          "skills/pitch-deck-video/references/openmontage/runtime-fetch.md"))

# 2. SS1(b) dedupe/contradiction + staleness.
check("C1 APCA informational, WCAG 4.5:1 stands (gates.md)",
      "an APCA pass does not clear a WCAG fail" in gates
      and "APCA Lc values are informational only" in gates)
check("C2 Rule 5 scope: container-level staggerChildren only",
      "Rule 5" in mp and "container-level `staggerChildren`" in mp
      and "Rule 5's 0.05s floor governs container-level `staggerChildren`" in mp
      and "Rule 5's 0.05s floor governs container-level `staggerChildren`" in mf)
check("C2 B3 0.03s governs per-row settle steps",
      "B3 governs per-row settle steps" in mf
      and "per-row settle steps under B3" in mp)
check("C3 B15 exitFactor is the single source of truth (Rule 8)",
      "`motionTokens.exitFactor` (B15) is the single source of truth" in mp
      and "`motionTokens.exitFactor` (B15) is the single source of truth" in mf
      and "Defers to `motionTokens.exitFactor` (B15, 0.8" in qr)
check("C4b seven dimensions in orchestrate DIRECTIVES (routing line stays frozen six)",
      "every directive carries its fix #19 D19 reason (seven dimensions)" in orch
      and "across all six full-experience dimensions" in orch
      and D19_ROUTING in orch)
check("C4b seven dimensions in Taste trends + polish-pass + checklists",
      "seven" in taste.split("Trend menu")[1].split("##")[0]
      and "seven" in slop and "seven" in unslop and "seven" in vercel)
check("C4b seven dimensions in ui-ux-pro-max DIRECTIVES + less-flat-ui LIQGLASS",
      "seven fix #19" in uipro and "seven fix #19" in lessflat)
check("C4b frozen six-texts intact (D19_RULE byte-identical)",
      D19_RULE in orch and D19_RULE in taste)
check("C4b frozen DEPTH_F22 extension lines intact",
      "The six dimensions above are unchanged" in orch
      and "The six dimensions above are unchanged" in taste)
check("C5 commit in the first-build sequence (orchestrate step 6)",
      "6. **Commit, README, then final report**" in orch)
check("C5 commit in hackathon-mode §7",
      "Proceed with the plan and commit" in hm)
check("C6 FILM_F1 disambiguated in pitch-deck-video",
      "coverage (FILM_F1)" in pitch and "coverage (F1)" not in pitch)
check("C6 font-rule pointers unchanged (F2/F3/F4/F5/F6 are font rules)",
      "F2/F3/F4/F5/F6/D19/B1/X1" in pitch)
check("C7 MOTION_F23 scope qualifiers (orchestrate + ui-ux-pro-max + foundations)",
      "on Taste landing pages the scroll ban stands" in orch
      and "on Taste landing pages the scroll ban stands" in uipro
      and "motion-governed surfaces" in mf)
check("S1 styles.csv discrepancy asserted as-is (80 header / 89 rows, csv is source)",
      "80 searchable styles" in read("skills/ui-ux-pro-max/SKILL.md")
      and csv_rows("skills/ui-ux-pro-max/data/styles.csv") == 89
      and "89 rows in `data/styles.csv`" in inv
      and "80 searchable styles, 51 active" in inv)
check("S5 fix22 SPEC reconciles 142 + H1 + H2 = 144",
      "144 items (142 + H1 + H2)" in open(
          os.path.join(PLUGIN, "fix22/SPEC.md"), encoding="utf-8").read())

# 3. SS1(c) one-story flow.
check("F-01 resume guards in orchestrate steps 0-2",
      "Resume guard (fix #24)" in orch
      and "steps 0–2 do NOT re-run work" in orch)
check("F-01 grill-me After Grilling line (no re-grill)",
      "after grilling" in grill.lower())
check("F-02 step 0 narration-key prompt executor is the orchestrator",
      "Narration-key prompt (the orchestrator sends it" in orch)
check("F-03 Verify steps 1-4b named in step 5a, per-wave vs once",
      "Verify steps 1–4b run per wave; the static checks below run once (fix #24)" in orch)
check("F-04 Verify stage 6 (not step 6) vs orchestrate step 6",
      "Verify stage 6 (Hallmark audit)" in orch
      and "Verify step 6" not in orch)
check("F-05 Gate-1 anchor gone, start-of-build step 0 named",
      "Gate 1" not in orch
      and "at the start of the build — orchestrate step 0" in orch)
check("F-06 count-convention lines (Taste + polish-pass)",
      "wherever a frozen rule text says 'six dimensions', read seven" in taste
      and "wherever a frozen rule text says 'six dimensions', read seven" in polish)
check("F-07 final report +4 bullets",
      "Inventory used vs considered-and-rejected" in orch
      and "Memorable moment + browser-qa verdict" in orch
      and "Type-audit result" in orch
      and "Re-verification entries" in orch)
check("F-08 step-6 order governs (others defer to step 6)",
      "full build order: see step 6" in orch)
check("F-09 readme-writer reads URL/video path from the ledger",
      "take them from `.hackathon/run-ledger.md`" in readme_writer)
check("F-10 inventory pointers (Taste step 4a + ui-ux-pro-max)",
      "Read `new-skills/orchestrate/references/design-inventory.md` FIRST" in taste
      and "read the design inventory (`skills/orchestrate/references/design-inventory.md`)" in uipro)
check("F-11 feature-expansion Phase 4 UI rule names the inventory",
      "UI decisions route through the design inventory" in fe)
check("F-12 single Lenses block in polish-pass SKILL.md",
      lines_with("## Lenses", polish) == 1)
check("F-13 5b wires the Hallmark redesign procedure",
      "following the Hallmark redesign procedure (`skills/design-taste-frontend/references/hallmark/references/redesign.md`)" in orch)
check("F-15 F6 qualifier appended, verify23 substring survives",
      "F6 is the PRIMARY gate (fix #23" in orch
      and "below memorable (THE CORE)" in orch)
check("inventory §10 cross-note (duplicates §1-§4, those govern)",
      "Cross-note: this section duplicates §1/§2/§3/§4 entries" in inv)
check("inventory themes clarified (50 files + README + index.json)",
      "(50 theme files + README.md (51 .md files) + `index.json`)" in inv)

# 4. SS2(a) agent references.
def _dual_cited_lines():
    n = 0
    for fn in os.listdir(os.path.join(BASE, "commands")):
        if fn.endswith(".md"):
            t = open(os.path.join(BASE, "commands", fn), encoding="utf-8").read()
            n += len(re.findall(r"- (?:Agent|Companion agent): `[a-z0-9-]+` \(`agents/ecc-[a-z0-9-]+\.md`\)", t))
    return n


check("agent path lines dual-cited in commands/ (19)",
      _dual_cited_lines() == 19)
check("plan.md:199 already house form, not doubled",
      "Use the `architect` agent (`agents/ecc-architect.md`) only when" in read("commands/plan.md")
      and "(`agents/ecc-architect.md`) (`agents/ecc-architect.md`)" not in read("commands/plan.md"))
check("no path-only Agent lines left in commands/",
      count_substring_in_tree("- Agent: `agents/ecc-", ("commands",)) == 0)
check("general-purpose agent type gone (general subagent)",
      "general-purpose" not in read("skills/skill-stocktake/SKILL.md")
      and "general-purpose" not in read("skills/rules-distill/SKILL.md")
      and "general subagent" in read("skills/skill-stocktake/SKILL.md")
      and "general subagent" in read("skills/rules-distill/SKILL.md"))
check("design-lead invocations gone (design-skill dispatch)",
      "INVOKE the design-lead" not in read("commands/gan-build.md")
      and "INVOKE the design-lead" not in read("commands/gan-design.md")
      and "dispatch to the design skill for that surface" in read("commands/gan-build.md"))
check("fallback paragraph in common-agents.mdc",
      "## If a named agent does not resolve (fix #24)" in common_agents
      and "spawn a general subagent on `cursor-grok-4.6-high-fast`" in common_agents)
check("duplicate architect row merged in common-agents.mdc",
      "| architect (`agents/ecc-architect.md`) | Implementation planning + system design |" in common_agents
      and sum(1 for ln in common_agents.splitlines() if ln.startswith("| architect")) == 1)
check("house-form invocations cite both forms (spot: tdd-guide, code-reviewer)",
      "`tdd-guide` agent (`agents/ecc-tdd-guide.md`)" in orch
      and "`code-reviewer` agent (`agents/ecc-code-reviewer.md`)" in orch)

# 5. SS2(b) model pins.
_agent_pins = {}
for _fn in os.listdir(os.path.join(BASE, "agents")):
    if _fn.endswith(".md"):
        _t = open(os.path.join(BASE, "agents", _fn), encoding="utf-8").read()
        _m = re.search(r"^model:\s*(\S+)\s*$", _t, re.M)
        if _m:
            _agent_pins[_fn] = _m.group(1)
check("all 72 agents carry a frontmatter model: pin",
      len(_agent_pins) == 72)
check("model pins: 4 x grok-4.7-high, 68 x cursor-grok-4.6-high-fast",
      list(_agent_pins.values()).count("grok-4.7-high") == 4
      and list(_agent_pins.values()).count("cursor-grok-4.6-high-fast") == 68)
check("zero bare grok-4.6-high-fast pins, zero bracket syntax in agents/",
      all("grok-4.6-high-fast" not in v or v.startswith("cursor-") for v in _agent_pins.values())
      and all("[" not in v for v in _agent_pins.values()))
check("picker prerequisite stated once (orchestrate step 4, verbatim)",
      orch.count("Select **Grok 4.7 High** in Cursor's model picker before the first build") == 1)
check("picker pointers elsewhere (orchestrate + orch-build-mvp + README)",
      orch.count("see the picker note in step 4") >= 3
      and "see the picker note in `skills/orchestrate/SKILL.md` step 4" in readme)
check("build.sh model mapping intact (grok-4.7-high / cursor-grok-4.6-high-fast)",
      "grok-4.7-high" in build and "cursor-grok-4.6-high-fast" in build)

# 6. SS2(c) hooks.
check("C-1 powershellRole + cmdRole in block-no-verify.js",
      "function powershellRole(words, budget)" in bnv
      and "function cmdRole(words, budget)" in bnv
      and "PowerShell/cmd are handled by powershellRole/cmdRole below (fix #24, C-1)" in bnv)
check("C-1 PowerShell/cmd wired into commandRole",
      "lowerName === 'powershell'" in bnv and "lowerName === 'cmd'" in bnv)
check("C-2 auto-tmux-dev.js header note (unwired + dead)",
      "fix #24: unwired and dead in this plugin" in read("scripts/hooks/auto-tmux-dev.js"))
check("C-3 desktop-notify.js header note (BurntToast not declared)",
      "fix #24: unwired in this plugin; the Windows branch needs the BurntToast module" in read("scripts/hooks/desktop-notify.js"))
check("D-8 harness-audit reword (upstream-only path, parity cannot pass here)",
      "Upstream-only path; does not ship in this Cursor plugin" in harness
      and "safeRead(rootDir, '.opencode/commands/harness-audit.md')" in harness)
check("D-9 angular mcp Gemini CLI scope note",
      "Not a Cursor path: the Gemini CLI is a separate Google tool" in angular_mcp)
check("hooks.json still registers 15 events, stop timeout 300",
      len(json.load(open(os.path.join(BASE, "hooks/hooks.json"), encoding="utf-8"))["hooks"]) == 15)

# 7. SS2(d) Claude scrub.
check("D-1 ten Upstream-only repairs present",
      count_substring_in_tree("Upstream only — no Cursor equivalent in this plugin") == 10)
check("D-2 zero Cursor-only left in scripts/hooks/",
      count_substring_in_tree("Cursor-only", ("scripts/hooks",)) == 0 if os.path.isdir(os.path.join(BASE, "scripts/hooks")) else False)
check("D-3 plankton settings.json claim softened (OWED to smoke test)",
      "whether Cursor reads `.ecc/settings.json` is decided by the live smoke test (LIVE_SMOKE_TEST.md §15), not asserted here (fix #24 D-9)" in plankton)
check("D-5 continuous-learning-v2 parenthetical swapped",
      "Cursor hooks capture prompts + tool use (upstream only)" in read("skills/continuous-learning-v2/SKILL.md"))

# 8. SS2(e) Windows paths.
check("E-1 pitch-deck-video APP_DIR PowerShell form",
      "$env:APP_DIR='/path/to/app'; npm run all" in pitch)
check("E-2 plankton Windows install branch first",
      "Windows (PowerShell) first — the plugin runs on Windows:" in plankton)
check("E-3 app-scaffold Docker Windows form",
      "Windows: launch Docker Desktop from the Start menu" in read(
          "skills/app-scaffold/reference/troubleshooting.md"))
check("E-4 auto-update PowerShell first + ecc-recipes PowerShell first",
      "Windows (PowerShell):" in read("commands/auto-update.md")
      and "Windows (PowerShell):" in read("skills/ecc-recipes/SKILL.md")
      and "$cmdDir = $null" in read("skills/ecc-recipes/SKILL.md"))
check("E-5 pitch-deck-video venv Windows form",
      "Windows (PowerShell): `python -m venv .tools; .\\.tools\\Scripts\\pip install yt-dlp`" in read(
          "skills/pitch-deck-video/references/troubleshooting.md"))
check("E-6 brew/chmod macOS-scoped",
      "macOS only — `brew install ruby`" in read("skills/mobile-ship/references/local-builds.md")
      and "(macOS/Linux; on Windows use Git Bash for this step" in read("agents/ecc-opensource-packager.md")
      and "SwiftLint is macOS-only" in read("agents/ecc-swift-reviewer.md"))
check("E-7 Taste gate hook Git Bash prerequisite + OWED",
      "Git Bash installed; whether it fires at all on Windows without Git Bash is untested, OWED to the live smoke test" in read(
          "skills/design-taste-frontend/references/gate.md"))

# 9. SS2(f) loading.
check("F-1/F-2 README Updating section, single authoritative place",
      readme.count("## Updating") == 1
      and "clone the repo directly into `~/.cursor/plugins/local/hackathon-ecc`" in readme
      and "Never symlink" in readme)
check("F-2 copy install path (rebuild + re-copy, no git pull without .git)",
      "if the plugin dir is a plain copy (no `.git` inside it), `git pull` cannot work there" in readme)

# 10. SS2(g) command surface.
check("G-1 direct invocation defined in demo.md",
      "**Direct invocation** means the user typed `/demo` at the prompt" in demo)
check("G-2 demo.md env check once, music-only/silent fallback, never prompt on dispatched run",
      "check the environment once for `ELEVENLABS_API_KEY`; if present, use it, else fall back to music-only/silent" in demo
      and "Never prompt on a dispatched run" in demo)
check("G-3 orchestrate.md Show-the-plan-first qualified",
      "**Show the plan first** (after grill-me and the narration-key prompt on a first build" in orch_cmd)
check("G-4 orch-build-mvp step-8 Environment-field dispatch line",
      "The `/demo` dispatch carries the Environment field naming `ELEVENLABS_API_KEY`" in obm)
check("DEMOGATE tokens present at every site (O4/O9, B2S1, B3S1, H1/H2)",
      "DEMOGATE_O4_F22" in orch and "DEMOGATE_O9_F22" in orch
      and "DEMOGATE_B2S1_F22" in obm and "DEMOGATE_B3S1_F22" in ocf
      and "DEMOGATE_H1_F22" in hm and "DEMOGATE_H2_F22" in hm)
check("narration-key prompt fires ONLY when the user asked for a demo video",
      "ONLY when the user asked for a demo video" in orch
      and "only when the user asked for a demo video" in hm
      and "If the user did NOT ask for a demo video, do NOT send this prompt" in obm)
check("first-build sequence intact: /demo never part of the order",
      "/demo is never part of this sequence" in orch
      and "/demo is never part of this sequence" in hm)

# 11. Global.
check("build.sh is 24,070 lines, md5 b0b2645a7d647f96296f9e9c45e09ef5 (post-fix24)",
      len(build_lines) == 24070
      and build_md5 == "b0b2645a7d647f96296f9e9c45e09ef5")
_diff = subprocess.run(
    ["diff", "build.sh.before-fix23", "build.sh"],
    cwd=PLUGIN, capture_output=True, text=True).stdout
_diff_add = sum(1 for ln in _diff.splitlines() if ln.startswith(">"))
_diff_del = sum(1 for ln in _diff.splitlines() if ln.startswith("<"))
check("diff vs build.sh.before-fix23 is additions only (+296/-0)",
      _diff_add == 296 and _diff_del == 0)
if _diff_del:
    print(f"   deletions in diff: {_diff_del}")
check("fix24 build.sh block present + wired before STEP 5 Counts",
      "fix #24: coherence re-weave + Cursor dial-in (build-time patch)" in build
      and "python3 \"$PLUGIN_ROOT/fix24/fix24.py\" \"$PLUGIN_DIR\"" in build)
check("fix24 run log written by the build (fix24/fix24-run-log.md)",
      os.path.isfile(os.path.join(PLUGIN, "fix24/fix24-run-log.md")))
check("fix24 block order: fix23 M1 block < fix24 block < STEP 5 Counts",
      build.index("fix23 M1 upstream block applied") < build.index("fix24/fix24.py") < build.index("# STEP 5 — Counts"))


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
check("Grok pins: grok-4.7-high in 27 files, cursor-grok-4.6-high-fast in 86 "
      "(common-agents.mdc gained both via the fix #24 fallback paragraph)",
      len(_g47.splitlines()) == 27 and len(_c46.splitlines()) == 86)
check("LIVE_SMOKE_TEST.md §15 exists (fix #24 Cursor-readiness)",
      "## 15. Fix #24 Cursor-readiness" in open(
          os.path.join(PLUGIN, "LIVE_SMOKE_TEST.md"), encoding="utf-8").read())

# _F23 token census after fix #24's orphan citations (verify23's exact
# counts moved by design -- the SPEC mandates the citations; the new counts
# are asserted here so the change is verified, not just excused).
_f23_lines = Counter()
_f23_occ = Counter()
_f23_files = set()
for _d in ("skills", "agents", "commands", "rules", "hooks"):
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [x for x in _dirs if x != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            if "_F23" in _t:
                _f23_files.add(os.path.relpath(_p, BASE))
            for _tok in ("INVENTORY_F23", "AMBITION_F23", "MOTION_F23",
                         "TYPEAUDIT_F23", "TRIO_F23", "HERO-BQA_F23",
                         "FUNC-BQA_F23", "FUNC-UIPRO_F23", "ALIGN_F23",
                         "MEMORABLE_F23"):
                if _tok in _t:
                    _f23_occ[_tok] += _t.count(_tok)
                    _f23_lines[_tok] += sum(
                        1 for _ln in _t.splitlines() if _tok in _ln)
check("_F23 census post-fix24: INVENTORY 5/5, AMBITION 7/8, MOTION 9/12, "
      "TYPEAUDIT 15/19, TRIO 4/4",
      (_f23_lines["INVENTORY_F23"], _f23_occ["INVENTORY_F23"]) == (5, 5)
      and (_f23_lines["AMBITION_F23"], _f23_occ["AMBITION_F23"]) == (7, 8)
      and (_f23_lines["MOTION_F23"], _f23_occ["MOTION_F23"]) == (9, 12)
      and (_f23_lines["TYPEAUDIT_F23"], _f23_occ["TYPEAUDIT_F23"]) == (15, 19)
      and (_f23_lines["TRIO_F23"], _f23_occ["TRIO_F23"]) == (4, 4))
check("_F23 census post-fix24: HERO-BQA 4/4, FUNC-BQA 3/3, FUNC-UIPRO 2/2, "
      "ALIGN 15/21, MEMORABLE 5/6, 18 files",
      (_f23_lines["HERO-BQA_F23"], _f23_occ["HERO-BQA_F23"]) == (4, 4)
      and (_f23_lines["FUNC-BQA_F23"], _f23_occ["FUNC-BQA_F23"]) == (3, 3)
      and (_f23_lines["FUNC-UIPRO_F23"], _f23_occ["FUNC-UIPRO_F23"]) == (2, 2)
      and (_f23_lines["ALIGN_F23"], _f23_occ["ALIGN_F23"]) == (15, 21)
      and (_f23_lines["MEMORABLE_F23"], _f23_occ["MEMORABLE_F23"]) == (5, 6)
      and len(_f23_files) == 18)

# 12. Prior-verifier regression leg. EXPECTED fails are ONLY: the frozen
# post-fix21 build.sh fingerprint line(s), the post-fix22 build.sh
# fingerprint line, the post-fix23 build.sh fingerprint line + its
# diff-count line + its pin-count line (all three are intended fix #24
# changes -- the wire block, +11 lines, and the fallback paragraph's two
# pin mentions -- recorded in the manifest), the less-flat-ui diff-hunk
# pattern, and cascades of those. Any fail outside that pattern is a REAL
# regression. Exact tails are asserted so a new fail changes the count.
_FPRINT21 = ("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c",
             "build.sh is 23647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c")
_FPRINT22 = "build.sh is 23774 lines, md5 4799a819791b9c3ec4c19136ad698397"
_FPRINT23 = ("build.sh is 24,059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2",
             "build.sh is 24059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2")
_DIFF23 = "diff vs build.sh.before-fix23 is additions only (+285/-0)"
_PINS23 = "grok-4.7-high in 26 files, cursor-grok-4.6-high-fast in 85"
_LFUI_DIFF = "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks"
# Intended fix #24 changes (recorded in the manifest, §4/§5): the C2/C3
# adjudications replaced verify22's B3/B15 conflict flags, and the SPEC-
# mandated orphan citations moved verify23's exact _F23 counts (new counts
# are asserted in §11 above). fix23's manifest check fails because its
# manifest records fix23's build.sh, and its fix22-leg line carries fix22's
# new tail.
_B3 = "B3 conflict flag carried (30ms vs Rule 5 floor)"
_B15 = "B15 conflict flag carried (0.8x vs quick-reference 60-70%)"
_F23_COUNTS = ("INVENTORY_F23: 4 lines in the built tree",
               "AMBITION_F23: 6 lines / 7 occurrences in the built tree",
               "MEMORABLE_F23: 4 lines / 5 occurrences in the built tree",
               "MOTION_F23: 9 lines / 10 occurrences in the built tree",
               "TYPEAUDIT_F23: 14 lines / 18 occurrences in the built tree",
               "TRIO_F23: 1 line in the built tree (orchestrate design-package step)",
               "HERO-BQA_F23: 3 lines in the built tree",
               "FUNC-BQA_F23: 2 lines in the built tree (browser-qa + Taste)",
               "FUNC-UIPRO_F23: 1 line in the built tree (ui-ux-pro-max pointer)",
               "ALIGN_F23: 15 lines / 16 occurrences in the built tree",
               "17 files carry _F23 tokens in the built tree")
_F23_MANIFEST = "fix23/MANIFEST.md exists and records build.sh lines + md5"
_F22_LEG_366 = "fix22 verifier: only expected fails, tail is 366/369"


def _allowed_fail(line):
    return (any(p in line for p in _FPRINT21)
            or _FPRINT22 in line
            or any(p in line for p in _FPRINT23)
            or _DIFF23 in line
            or _PINS23 in line
            or _LFUI_DIFF in line
            or _B3 in line
            or _B15 in line
            or any(p in line for p in _F23_COUNTS)
            or _F23_MANIFEST in line
            or _F22_LEG_366 in line
            or re.match(r"FAIL fix\d+ verifier still passes", line))


for name, script, tail in (
        ("fix15", "fix15/verify15.py", "42/44 checks pass"),
        ("fix17", "fix17/verify17.py", "58/60 checks pass"),
        ("fix18", "fix18/verify18.py", "69/72 checks pass"),
        ("fix19", "fix19/verify19.py", "71/76 checks pass"),
        ("fix20", "fix20/verify20.py", "164/169 checks pass"),
        ("fix21", "fix21/verify21.py", "96/102 checks pass"),
        ("fix22", "fix22/verify22.py", "366/369 checks pass"),
        ("fix23", "fix23/verify23.py", "excluding the manifest check, which is owed: 196/211 checks pass")):
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

# 13. Manifest check (fix22 pattern). Runs once fix24/MANIFEST.md exists;
# FAILS until the manifest worker writes it. Reported separately as owed.
manifest_path = os.path.join(PLUGIN, "fix24/MANIFEST.md")
_manifest_ok = False
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    _manifest_ok = bool(m_lines and m_md5
                        and int(m_lines.group(1)) == len(build_lines)
                        and m_md5.group(1) == build_md5)
check("fix24/MANIFEST.md exists and records build.sh lines + md5 "
      "(OWED -- fails until the manifest worker writes it)",
      _manifest_ok)

failed = [n for n, ok in checks if not ok]
_manifest_failed = not _manifest_ok
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
if _manifest_failed:
    print(f"excluding the manifest check, which is owed: "
          f"{len(checks) - len(failed)}/{len(checks) - 1} checks pass")
sys.exit(1 if failed else 0)
