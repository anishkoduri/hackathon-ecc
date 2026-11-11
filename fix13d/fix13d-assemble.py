#!/usr/bin/env python3
"""Fix program #13d — ASSEMBLER (coordinator).

Inserts the fix13d patch block into build.sh LAST, just before STEP 5
(after the fix13c block). The block patches the files with no staged
sources (upstream ECC patched at build time):
  B1  orch-build-mvp step 4 :38 — the eval-rubric.md the orchestrator writes
      must carry the screen-distinctiveness scoping note (deferral).
  B2  orch-build-mvp 6b — re-verify sequencing: a redesign routed from final
      polish is re-verified by browser-qa's step-6 visual loop BEFORE the
      step-7 commit and step-8 deploy.
  B3  ecc-gan-planner Process step 4 :107 — the eval-rubric.md it writes must
      carry the scoping note. B3b :44 — "Inspiration: [specific sites/apps
      to draw from]" replaced with a non-derivative direction source.
  B4  ecc-gan-evaluator :31 / :94 / :116 — AI-slop language scoped to the
      rubric deferral (penalizes only as the rubric allows, never as screen
      distinctiveness). B4d :3 — frontmatter truth (Cursor subagent).
  B5  ecc-gan-generator :3 + ecc-gan-planner :3 — frontmatter truth.
  B6  gan-design Setup step 3 :19 — the design-focused eval-rubric.md it
      writes must carry the scoping note. (Its :36 assertion — "the evaluator
      scores against eval-rubric.md, which carries that deferral" — becomes
      TRUE on every path once B1/B3/B6 land, so :36 itself is not changed.)
  B7  gan-style-harness :3 — frontmatter truth (upstream `claude -p` path is
      Claude Code only; the loop runs in Cursor via /gan-build + ecc-gan-*
      agents). B7b — "Via Claude Code (Manual)" section note: those commands
      are NOT executed in this plugin.
  B8  design-system Mode 3 — slop findings are candidate evidence for
      browser-qa, never a distinctiveness verdict.

Item-6 truth determination (from the files): the upstream skill's `claude -p`
CLI invocation path (SKILL.md:183-192, :30; scripts/gan-harness.sh, whose
own header says it shells out to `claude -p` and will not run in a
Cursor-only install) does NOT run in Cursor and is never executed by this
plugin. The GAN LOOP as implemented here DOES run in Cursor:
commands/gan-build.md + gan-design.md launch the ecc-gan-* agents "as a
Cursor subagent", and the agents carry Cursor model pins
(composer-2.5[fast=false]). The skill contributes the harness design,
prompts, and rubric (the planner writes eval-rubric.md from it). So
orch-build-mvp:40 driving the GAN loop in Cursor is NOT an inconsistency —
the wording in the three agent frontmatters + the skill frontmatter +
hackathon-mode §5 is. The wording is fixed here (and in fix13d.py S6);
orch-build-mvp:40 is untouched on this item.

Preflight: every anchor is verified count==1 against the CURRENT built
tree (post-fix13c) before assembly. The block's own inner asserts re-verify
each anchor count==1 at build time and fail the build loudly on mismatch.
Idempotency guard: refuses to run if a fix13d block is already in build.sh.
Backup: run `cp build.sh build.sh.before-fix13d` before this script.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)          # ~/workspace/hackathon-plugin
BUILD_SH = os.path.join(PLUGIN_ROOT, "build.sh")
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")
STEP5_ANCHOR = "\n# STEP 5 — Counts\n"

BLOCK = r"""# --- fix13d: Audit #44 minors + dry-run #16 blocking/minor — single executor, rubric deferral, GAN truth ---
# (orch-build-mvp / gan agents / gan-design / gan-style-harness / design-system
#  have no staged sources; they are upstream ECC patched here). Placement:
#  LAST, just before STEP 5 (after the fix13c block).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # B1 orch-build-mvp step 4: orchestrator-written rubric carries the deferral.
  ("skills/orch-build-mvp/SKILL.md",
   r'''so later slices brief from real tokens.''',
   r'''so later slices brief from real tokens. The `eval-rubric.md` you write must carry the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric — screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop) — every rubric written on any path must carry that deferral.'''),
  # B2 orch-build-mvp 6b: re-verify before commit/deploy.
  ("skills/orch-build-mvp/SKILL.md",
   r'''6b. **Final polish — after verification and before the step-7 commit.** Run `polish-pass` on the built UI (same role as orchestrate step 5b: it implements the subset that materially increases quality without destabilizing the build, at most one fix round per item) and carry its 10 highest-impact remaining improvements into the step-9 final report.''',
   r'''6b. **Final polish — after verification and before the step-7 commit.** Run `polish-pass` on the built UI (same role as orchestrate step 5b: it implements the subset that materially increases quality without destabilizing the build, at most one fix round per item) and carry its 10 highest-impact remaining improvements into the step-9 final report. **Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-6 every-route visual loop on the redesigned screens BEFORE the step-7 commit and step-8 deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.'''),
  # B3 gan-planner Process step 4: planner-written rubric carries the deferral.
  ("agents/ecc-gan-planner.md",
   r'''4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly''',
   r'''4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric this agent writes must carry that deferral.'''),
  # B3b gan-planner :44: Inspiration line is derivative — replace with a
  # non-derivative direction source.
  ("agents/ecc-gan-planner.md",
   r'''- **Inspiration**: [specific sites/apps to draw from]''',
   r'''- **Direction source**: [named direction generated through the design package skills (`ui-ux-pro-max` direction / dealt Hallmark theme) — never specific sites/apps to draw from; the anti-derivative rule forbids basing the design on a searched external reference]'''),
  # B4 gan-evaluator :31: AI-slop penalty scoped to the rubric deferral.
  ("agents/ecc-gan-evaluator.md",
   r'''- DO penalize heavily for AI-slop aesthetics (generic gradients, stock layouts)''',
   r'''- DO penalize heavily for AI-slop aesthetics as the rubric allows — code-level application of the recorded direction only (generic gradients, stock layouts that ignore the recorded direction) — never as screen distinctiveness: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop'''),
  # B4b gan-evaluator :94: Design Audit AI-slop indicators scoped the same way.
  ("agents/ecc-gan-evaluator.md",
   r'''   - AI-slop indicators (generic gradients, stock patterns)''',
   r'''   - AI-slop indicators as the rubric allows (generic gradients, stock patterns that ignore the recorded direction) — code-level evidence only, never a screen-distinctiveness verdict'''),
  # B4c gan-evaluator :116: calibration 4-5 scoped to the rubric's code rows.
  ("agents/ecc-gan-evaluator.md",
   r'''- 4-5: Functional but clearly AI-generated, tutorial-quality''',
   r'''- 4-5: Functional but clearly AI-generated on the rubric's code-level rows, tutorial-quality (screen distinctiveness is not scored here — that is `browser-qa`'s alone)'''),
  # B4d gan-evaluator :3 frontmatter truth.
  ("agents/ecc-gan-evaluator.md",
   r'''(Claude Code only — no Cursor equivalent in this plugin)''',
   r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''),
  # B5 gan-generator :3 frontmatter truth.
  ("agents/ecc-gan-generator.md",
   r'''(Claude Code only — no Cursor equivalent in this plugin)''',
   r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''),
  # B5b gan-planner :3 frontmatter truth.
  ("agents/ecc-gan-planner.md",
   r'''(Claude Code only — no Cursor equivalent in this plugin)''',
   r'''(Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''),
  # B6 gan-design Setup step 3: design-focused rubric carries the deferral.
  ("commands/gan-design.md",
   r'''3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality''',
   r'''3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral.'''),
  # B7 gan-style-harness :3 frontmatter truth.
  ("skills/gan-style-harness/SKILL.md",
   r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (Claude Code only \u2014 this skill drives the `claude` CLI and does not run in Cursor)''',
   r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (The upstream `claude -p` invocation path is Claude Code only and does not run in Cursor; in this plugin the harness loop runs in Cursor through `/gan-build` + `/gan-design` and the `ecc-gan-*` agents as Cursor subagents — the skill contributes the harness design, prompts, and rubric, never the CLI commands.)'''),
  # B7b gan-style-harness "Via Claude Code (Manual)" section: those commands
  # are NOT executed in this plugin.
  ("skills/gan-style-harness/SKILL.md",
   r'''### Via Claude Code (Manual)

```bash
# Step 1: Plan''',
   r'''### Via Claude Code (Manual)

> In this plugin these `claude -p` commands are NOT executed — the loop runs in Cursor via `/gan-build` (planner/generator/evaluator as Cursor subagents). The rubric and prompts above are the operative parts; this section documents the upstream invocation path only.

```bash
# Step 1: Plan'''),
  # B8 design-system Mode 3: slop findings are evidence, not a verdict.
  ("skills/design-system/SKILL.md",
   r'''### Mode 3: AI Slop Detection

Identifies generic AI-generated design patterns:''',
   r'''### Mode 3: AI Slop Detection

Identifies generic AI-generated design patterns. **Scope — pattern evidence, not a distinctiveness verdict:** the patterns below are code-level evidence (they exist in the code); a slop finding — including "Generic hero with centered text over stock gradient" — is candidate evidence for `browser-qa`, never a verdict that a screen reads as a default template. Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by `browser-qa` in the visual loop. Record slop findings with the screen and pattern for `browser-qa` to judge.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix13d anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    open(p, "w").write(t.replace(old, new))
print("fix13d upstream block applied")
PYEOF

"""

# Preflight anchors: (rel path in built tree, old text, label)
PREFLIGHT = [
    ("skills/orch-build-mvp/SKILL.md",
     "so later slices brief from real tokens.",
     "B1 step-4 rubric write"),
    ("skills/orch-build-mvp/SKILL.md",
     "6b. **Final polish — after verification and before the step-7 commit.**",
     "B2 step 6b"),
    ("agents/ecc-gan-planner.md",
     "4. Also write a concise `gan-harness/eval-rubric.md`",
     "B3 planner Process step 4"),
    ("agents/ecc-gan-planner.md",
     "- **Inspiration**: [specific sites/apps to draw from]",
     "B3b planner Inspiration line"),
    ("agents/ecc-gan-evaluator.md",
     "- DO penalize heavily for AI-slop aesthetics (generic gradients, stock layouts)",
     "B4 evaluator :31"),
    ("agents/ecc-gan-evaluator.md",
     "AI-slop indicators (generic gradients, stock patterns)",
     "B4b evaluator :94"),
    ("agents/ecc-gan-evaluator.md",
     "- 4-5: Functional but clearly AI-generated, tutorial-quality",
     "B4c evaluator :116"),
    ("agents/ecc-gan-evaluator.md",
     "(Claude Code only — no Cursor equivalent in this plugin)",
     "B4d evaluator frontmatter"),
    ("agents/ecc-gan-generator.md",
     "(Claude Code only — no Cursor equivalent in this plugin)",
     "B5 generator frontmatter"),
    ("agents/ecc-gan-planner.md",
     "(Claude Code only — no Cursor equivalent in this plugin)",
     "B5b planner frontmatter"),
    ("commands/gan-design.md",
     "3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality",
     "B6 gan-design Setup step 3"),
    ("skills/gan-style-harness/SKILL.md",
     "Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (Claude Code only",
     "B7 skill frontmatter"),
    ("skills/gan-style-harness/SKILL.md",
     "### Via Claude Code (Manual)",
     "B7b Via Claude Code section"),
    ("skills/design-system/SKILL.md",
     "### Mode 3: AI Slop Detection\n\nIdentifies generic AI-generated design patterns:",
     "B8 design-system Mode 3"),
]


def main():
    with open(BUILD_SH) as f:
        sh = f.read()
    assert "fix13d: Audit #44 minors" not in sh, "fix13d block already in build.sh — refusing (idempotency guard)"
    assert STEP5_ANCHOR in sh, "STEP 5 anchor not found in build.sh"
    for rel, old, label in PREFLIGHT:
        p = os.path.join(BUILT, rel)
        t = open(p).read()
        n = t.count(old)
        assert n == 1, f"preflight {label}: anchor count={n} (expected 1) in {rel}"
        print(f"preflight OK: {label}")
    sh = sh.replace(STEP5_ANCHOR, "\n" + BLOCK + STEP5_ANCHOR, 1)
    with open(BUILD_SH, "w") as f:
        f.write(sh)
    print("fix13d block inserted into build.sh (LAST, just before STEP 5)")


if __name__ == "__main__":
    main()
