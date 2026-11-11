#!/usr/bin/env python3
"""Fix program #13e — ASSEMBLER (coordinator).

Inserts the fix13e patch block into build.sh LAST, just before STEP 5
(after the fix13d block). The block patches the files with no staged
sources (upstream ECC patched at build time):
  1A-1C  ui-ux-pro-max SKILL.md — captivating bar + anti-generic bar become
         design guidance / candidate evidence; craft-floor ban qualifier.
  2a-2m  GAN rubric rows rewritten (direction + code only); rubric-validation
         step on every path (planner, orch-build-mvp, gan-build Phase 1/2,
         gan-harness.sh, evaluator Step 1, gan-design Setup 3); gan-design
         :36 reworded true. Validation failure = ADD THE NOTE (coordinator:
         missing-file case falls back to the canonical skill rubric — 2i/2k).
  11a-11d claude -p residue scoped (skill :30, :179 heading, :185/:188/:191/
         :194 commands, gan-harness.sh :2 header).
  C3-2/5/6 orch-build-mvp 6b fresh verdict run + steps 7/8 hold.
  C4-6 design-system Mode 3 evidence destination. C4-7 browser-qa read step.
  C5-4/5 orch-build-mvp :40/:49 verdict attribution.
  5a-5f  GAN decision B: direction from the design-lead (Grok) BEFORE the
         loop; GAN agents are executors (frontmatter pins stay composer).
  5g    Shipped README picker note (post-STEP-4 patch, Prerequisites).
  6a    design-system Mode 1: package-generated direction, no competitors.
  7a-7c orch-add-feature / orch-fix-defect / orch-refine-code skills: design-
         package rule mirrored from orch-change-feature :36.

Preflight: every anchor is verified count==1 against the CURRENT built
tree (post-fix13d) before assembly. The block's own inner asserts re-verify
each anchor count==1 at build time and fail the build loudly on mismatch.
Idempotency guard: refuses to run if a fix13e block is already in build.sh.
Backup: run `cp build.sh build.sh.before-fix13e` before this script.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)          # ~/workspace/hackathon-plugin
BUILD_SH = os.path.join(PLUGIN_ROOT, "build.sh")
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")
STEP5_ANCHOR = "\n# STEP 5 — Counts\n"

BLOCK = r"""# --- fix13e: Audit #45 blocking/minor + dry-run #17 blocking/minor — screen verdicts, GAN rubric validation, fresh verdict budget + deploy hold ---
# (ui-ux-pro-max / gan-style-harness / gan agents / gan-design / gan-build /
#  gan-harness.sh / orch-build-mvp / design-system / browser-qa / orch-add-feature /
#  orch-fix-defect / orch-refine-code / shipped README have no staged sources;
#  they are upstream ECC patched here). Placement: LAST, just before STEP 5
#  (after the fix13d block).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # 1A ui-ux-pro-max captivating bar: design guidance, not a screen verdict.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''**Captivating bar for dashboard/app surfaces:** the primary view must have one unmistakable visual anchor a user remembers after leaving the page. Test: after closing the page, the user can describe that one anchor — its form and what it showed — without reopening it; if nothing is memorable, the surface fails even if every other check passes. Enforced fail criterion (the brief names the anchor; Verify checks it as pass/fail): after closing the page, a user can describe that one anchor — its form and what it showed — without reopening it. If no anchor can be named, the surface FAILS.''',
   r'''**Captivating bar for dashboard/app surfaces (design guidance, not a screen verdict):** the primary view must have one unmistakable visual anchor a user remembers after leaving the page. Test (design guidance for the builder): after closing the page, the user can describe that one anchor — its form and what it showed — without reopening it. The brief names the anchor; Verify records whether an anchor can be named as candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable — this skill never states a screen pass/fail.'''),
  # 1B ui-ux-pro-max anti-generic bar: design guidance + candidate evidence.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''**Anti-generic bar:** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above; if a surface looks like a default template, it fails even if every checklist item passes. Enforced fail criteria (the brief and Verify check these as pass/fail against the recorded named direction): (1) Direction trace — every primary screen visibly traces to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product fails. (2) Memorable anchor — the primary view carries the one unmistakable anchor from the captivating bar above; if no anchor can be named, the surface FAILS. (3) Not a default template — a surface that looks like a default template fails even if every checklist item passes.''',
   r'''**Anti-generic bar (design guidance, not a screen verdict):** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above. Design guidance the brief and Verify record as candidate evidence for `browser-qa` (checked against the recorded named direction): (1) Direction trace — every primary screen should visibly trace to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product is candidate evidence for `browser-qa`. (2) Memorable anchor — the primary view should carry the one unmistakable anchor from the captivating bar above; if no anchor can be named, record that as candidate evidence for `browser-qa`. (3) Not a default template — a surface that looks like a default template is candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail.'''),
  # 1C ui-ux-pro-max :87 craft-floor bans are static/code-level checks.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''its bans are absolute — a pinned brief never overrides a ban''',
   r'''its bans are absolute as static/code-level checks — a pinned brief never overrides a ban — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone)'''),
  # 2a GAN rubric rows rewritten: direction recorded + code-level trace only.
  ("skills/gan-style-harness/SKILL.md",
   r'''### Design Quality (weight: 0.3)
- 1-3: Generic, template-like, "AI slop" aesthetics
- 4-6: Competent but unremarkable, follows conventions
- 7-8: Distinctive, cohesive visual identity in the recorded direction and its code-level application — screen distinctiveness itself is judged ONLY by browser-qa, never here
- 9-10: Could pass for a professional designer's work

### Originality (weight: 0.2)
- 1-3: Default colors, stock layouts, no personality
- 4-6: Some custom choices, mostly standard patterns
- 7-8: Clear creative vision, unique approach in the recorded direction — screen distinctiveness itself is judged ONLY by browser-qa, never here
- 9-10: Surprising, delightful, genuinely novel''',
   r'''### Design Quality (weight: 0.3)
- 1-3: No named direction recorded, or tokens, type, and spacing in the code do not trace to any recorded direction
- 4-6: A direction is recorded but only partly applied in code — some tokens, type, or spacing trace to it, the rest do not
- 7-8: Direction recorded and applied in code — tokens, type, and spacing trace to it coherently across the app
- 9-10: Direction recorded and applied with professional-level craft in code — tokens, type, and spacing trace to it consistently, including edge states

### Originality (weight: 0.2)
- 1-3: Code-level choices do not trace to the recorded direction — defaults throughout, no direction-specific decisions in code
- 4-6: Some code-level choices trace to the recorded direction, most do not
- 7-8: Clear creative direction recorded and applied in code — direction-specific choices in tokens, type, and spacing throughout
- 9-10: Direction recorded and applied in code in a surprising, inventive way — direction-specific choices throughout, including details and edge states'''),
  # 2b GAN evaluator key behaviors: template-ness wording removed.
  ("skills/gan-style-harness/SKILL.md",
   r'''  1. **Design Quality** — Does it feel like a coherent whole?
  2. **Originality** — Custom decisions vs. template/AI patterns?''',
   r'''  1. **Design Quality** — Is the recorded direction applied coherently in code (tokens, type, and spacing trace to it)?
  2. **Originality** — Do the code-level choices trace to the recorded direction rather than defaults?'''),
  # 2c GAN anti-pattern #1: penalties scoped to code-level only.
  ("skills/gan-style-harness/SKILL.md",
   r'''1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns.''',
   r'''1. **Evaluator too lenient** — If the evaluator passes everything on iteration 1, your rubric is too generous. Tighten scoring criteria and add explicit penalties for common AI patterns (code-level direction-application failures only — never screen distinctiveness, which is judged ONLY by `browser-qa`).'''),
  # 2d GAN planner: validate the rubric it writes before handoff.
  ("agents/ecc-gan-planner.md",
   r'''4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric this agent writes must carry that deferral.''',
   r'''4. Also write a concise `gan-harness/eval-rubric.md` with the evaluation criteria in a format the Evaluator can consume directly — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric this agent writes must carry that deferral. Before handing off, re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never hand off a rubric without it.'''),
  # 2e orch-build-mvp step 4: validate the rubric before driving the loop.
  ("skills/orch-build-mvp/SKILL.md",
   r'''The `eval-rubric.md` you write must carry the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric — screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop) — every rubric written on any path must carry that deferral.''',
   r'''The `eval-rubric.md` you write must carry the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric — screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop) — every rubric written on any path must carry that deferral. Before driving `/gan-build`, re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never start the loop on a rubric without it.'''),

  # 2f gan-build Phase 2: evaluator validates the rubric before scoring.
  ("commands/gan-build.md",
   r'''    - Read eval-rubric.md and spec.md
    - Test the live application (mode: playwright/screenshot/code-only)''',
   r'''    - Read eval-rubric.md and spec.md
    - Validate `gan-harness/eval-rubric.md` before scoring: confirm the screen-distinctiveness scoping note is at its top; if it is missing, prepend the note (copied from the `gan-style-harness` SKILL.md rubric) to the rubric file, record the repair in the feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
    - Test the live application (mode: playwright/screenshot/code-only)'''),
  # 2g gan-build Phase 1: name the --skip-planner rubric gap explicitly.
  ("commands/gan-build.md",
   r'''### Phase 1: Planning (Planner Agent)
Unless `--skip-planner` is set:''',
   r'''### Phase 1: Planning (Planner Agent)
Unless `--skip-planner` is set (with `--skip-planner`, no rubric is written here — the existing `gan-harness/eval-rubric.md` is used as-is and is validated in Phase 2 before any scoring):'''),
  # 2h gan-harness.sh planner prompt: deferral requirement (fourth writer).
  ("scripts/gan-harness.sh",
   r'''2. gan-harness/eval-rubric.md — Evaluation criteria for the Evaluator''',
   r'''2. gan-harness/eval-rubric.md — Evaluation criteria for the Evaluator. Put the screen-distinctiveness scoping note at the top of eval-rubric.md (copy it from the gan-style-harness skill's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by browser-qa in the visual loop) — every rubric written on any path must carry that deferral.'''),
  # 2i gan-harness.sh Phase 1: shell-side rubric validation on --skip-planner.
  ("scripts/gan-harness.sh",
   r'''if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then
  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"''',
   r'''if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then
  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"
  # Rubric validation (screen-distinctiveness deferral): a skipped planner means
  # the rubric on disk may be stale or hand-written. If it does not carry the
  # scoping note, prepend it and log the repair — the evaluator never scores
  # screen distinctiveness.
  if [ ! -f "${HARNESS_DIR}/eval-rubric.md" ]; then
    warn "No gan-harness/eval-rubric.md found — nothing to validate; the evaluator will fall back to the canonical rubric in the gan-style-harness skill and record the missing file."
  elif ! grep -q "Screen distinctiveness is NOT scored here" "${HARNESS_DIR}/eval-rubric.md"; then
    { printf '%s\n\n' "**Screen distinctiveness is NOT scored here.** Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by \`browser-qa\` in the visual loop — never by this evaluator. The Design Quality and Originality rows below score the recorded direction and its code-level application only."; cat "${HARNESS_DIR}/eval-rubric.md"; } > "${HARNESS_DIR}/eval-rubric.md.tmp" && mv "${HARNESS_DIR}/eval-rubric.md.tmp" "${HARNESS_DIR}/eval-rubric.md"
    warn "eval-rubric.md lacked the screen-distinctiveness scoping note — prepended it before scoring."
  fi'''),
  # 2j gan-harness.sh evaluator prompt: validate the rubric before scoring.
  ("scripts/gan-harness.sh",
   r'''1. Read gan-harness/eval-rubric.md for scoring criteria
2. Read gan-harness/spec.md for feature requirements''',
   r'''1. Read gan-harness/eval-rubric.md for scoring criteria
1a. Validate the rubric before scoring: confirm gan-harness/eval-rubric.md carries the screen-distinctiveness scoping note at its top ("Screen distinctiveness is NOT scored here" — judged ONLY by browser-qa); if it does not, prepend that note to the rubric file, note the repair in your feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
2. Read gan-harness/spec.md for feature requirements'''),
  # 2k GAN evaluator Step 1: single enforcement point on every path.
  ("agents/ecc-gan-evaluator.md",
   r'''### Step 1: Read the Rubric
```
Read gan-harness/eval-rubric.md for project-specific criteria
Read gan-harness/spec.md for feature requirements
Read gan-harness/generator-state.md for what was built
```''',
   r'''### Step 1: Read the Rubric
```
Read gan-harness/eval-rubric.md for project-specific criteria
Read gan-harness/spec.md for feature requirements
Read gan-harness/generator-state.md for what was built
Validate gan-harness/eval-rubric.md before scoring: confirm it carries the screen-distinctiveness scoping note at its top; if it does not, prepend the note (copied from the gan-style-harness skill's rubric) to the rubric file, record the repair in your feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness. If the rubric file does not exist, score against the Evaluation Rubric in the `gan-style-harness` skill (which carries the scoping note) and record the missing file in your feedback file.
```'''),
  # 2l gan-design :36: assertion reworded true (conditional on Setup validation).
  ("commands/gan-design.md",
   r'''- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md`, which carries that deferral.''',
   r'''- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md` only after the Setup step-3 validation confirms it carries that deferral (a rubric without the deferral is repaired before scoring — see Setup step 3).'''),
  # 2m gan-design Setup step 3: validate the rubric before the loop starts.
  ("commands/gan-design.md",
   r'''3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral.''',
   r'''3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral. Validate it before the loop starts: re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never start the loop on a rubric without it.'''),
  # 11a gan-style-harness :30: scope the claude -p reference.
  ("skills/gan-style-harness/SKILL.md",
   r'''- Quick single-file fixes (use standard `claude -p`)''',
   r'''- Quick single-file fixes (Claude Code only — use standard `claude -p` there; in this plugin use the Cursor agent loop, never `claude -p`)'''),
  # 11b gan-style-harness :179 heading: scope it in the heading itself.
  ("skills/gan-style-harness/SKILL.md",
   r'''### Via Claude Code (Manual)''',
   r'''### Via Claude Code (Manual — Claude Code only, never executed in this plugin)'''),
  # 11c gan-style-harness commands: scope each claude -p command in place.
  ("skills/gan-style-harness/SKILL.md",
   r'''```bash
# Step 1: Plan
claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. Write spec to spec.md"

# Step 2: Generate (iteration 1)
claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000."

# Step 3: Evaluate (iteration 1)
claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://localhost:3000. Score against the rubric. Write feedback to feedback-001.md"

# Step 4: Generate (iteration 2 — reads feedback)
claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores."

# Repeat steps 3-4 until pass threshold met
```''',
   r'''```bash
# Step 1: Plan
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. Write spec to spec.md"

# Step 2: Generate (iteration 1)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000."

# Step 3: Evaluate (iteration 1)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://localhost:3000. Score against the rubric. Write feedback to feedback-001.md"

# Step 4: Generate (iteration 2 — reads feedback)
# Claude Code only — never executed in this plugin; upstream documentation only.
claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores."

# Repeat steps 3-4 until pass threshold met
```'''),
  # 11d gan-harness.sh :2 header: state the loop truth.
  ("scripts/gan-harness.sh",
   r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI.''',
   r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI. The plugin's GAN loop runs in Cursor via /gan-build and never executes this script; this script is the upstream Claude Code invocation path only.'''),

  # C3-2 orch-build-mvp 6b: fresh verdict run + budget.
  ("skills/orch-build-mvp/SKILL.md",
   r'''**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-6 every-route visual loop on the redesigned screens BEFORE the step-7 commit and step-8 deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.''',
   r'''**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the step-7 commit and step-8 deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-6 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them; the redesign decision follows `browser-qa`'s verdict. If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see steps 7/8): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy.'''),
  # C3-5 orch-build-mvp step 7: commit hold.
  ("skills/orch-build-mvp/SKILL.md",
   r'''7. **Commit — orch-pipeline Phase 6.** Commit the scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting; see hackathon-mode §7).''',
   r'''7. **Commit — orch-pipeline Phase 6.** Before committing, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the commit of the redesign is HELD: do not commit the redesigned files in this run, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign (this is a safety hold, not a user question — it never asks the user anything). Otherwise, commit the scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting; see hackathon-mode §7).'''),
  # C3-6 orch-build-mvp step 8: deploy hold.
  ("skills/orch-build-mvp/SKILL.md",
   r'''8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Deploy the working MVP — record the production URL and the deploy path used in `.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) — then film the LOCAL app from the project dir (`APP_DIR` to the app dir)''',
   r'''8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Before deploying, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Otherwise, deploy the working MVP — record the production URL and the deploy path used in `.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) — then film the LOCAL app from the project dir (`APP_DIR` to the app dir)'''),
  # C4-6 design-system Mode 3: slop evidence destination.
  ("skills/design-system/SKILL.md",
   r'''Record slop findings with the screen and pattern for `browser-qa` to judge.''',
   r'''Append slop findings to `.hallmark/candidate-evidence.md` with the screen and pattern for `browser-qa` to judge.'''),
  # C4-7 browser-qa: read candidate-evidence.md before every verdict.
  ("skills/browser-qa/SKILL.md",
   r'''Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop:''',
   r'''Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop: before rendering a verdict in any round, read `.hallmark/candidate-evidence.md` if it exists in the project root and treat its entries as candidate evidence (screen + what reads as a template), never as a verdict; the orchestrator passes this file as a standing input to the visual loop, not from memory.'''),
  # C5-4 orch-build-mvp :40: verdict attribution.
  ("skills/orch-build-mvp/SKILL.md",
   r'''The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.''',
   r'''The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); on `browser-qa`'s verdict, a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.'''),
  # C5-5 orch-build-mvp step 6: verdict attribution.
  ("skills/orch-build-mvp/SKILL.md",
   r'''`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named direction recorded AND visibly applied; a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference); fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating).''',
   r'''`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named direction recorded AND visibly applied; on `browser-qa`'s verdict, a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference); fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating).'''),
  # 5a GAN planner description: records the supplied direction.
  ("agents/ecc-gan-planner.md",
   r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and design direction. (Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)"''',
   r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, and evaluation criteria, and records the design direction supplied by the design-lead (model grok-4.7-high) before the loop — the planner records the direction, it does not generate or re-derive one. (Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)"'''),
  # 5b GAN planner :44 Direction source: supplied, not generated.
  ("agents/ecc-gan-planner.md",
   r'''- **Direction source**: [named direction generated through the design package skills (`ui-ux-pro-max` direction / dealt Hallmark theme) — never specific sites/apps to draw from; the anti-derivative rule forbids basing the design on a searched external reference]''',
   r'''- **Direction source**: [the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` BEFORE this loop — copied here, not generated: the planner records the supplied direction and never re-derives one from a searched reference or a fresh invention; if no direction is recorded, record the brief's stated default, marked assumed, and proceed — never a searched external reference, per the anti-derivative rule]'''),
  # 5c GAN planner guideline 2: record the supplied tokens.
  ("agents/ecc-gan-planner.md",
   r'''2. **Specify exact colors** — Not "blue theme" but "#1a73e8 primary, #f8f9fa background"''',
   r'''2. **Record the supplied direction's exact tokens** — copy the colours, type and layout from the design-lead's recorded direction in `docs/design-tokens.md` (not "blue theme" but "#1a73e8 primary, #f8f9fa background"); do not invent a new palette — the planner records the direction, it does not generate one'''),
  # 5d gan-build Phase 1 launch: direction from the design-lead.
  ("commands/gan-build.md",
   r'''1. Launch the `gan-planner` agent as a Cursor subagent with the user's brief''',
   r'''1. Launch the `gan-planner` agent as a Cursor subagent with the user's brief, plus the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` — the direction comes from the design-lead BEFORE the loop; the planner records it in the spec and the loop executes under it, it does not generate or re-derive a direction on its own'''),
  # 5e gan-design :12: brief carries the design-lead's direction.
  ("commands/gan-design.md",
   r'''A two-agent loop (Generator + Evaluator) focused on frontend design quality. No planner — the brief IS the spec.''',
   r'''A two-agent loop (Generator + Evaluator) focused on frontend design quality. No planner — the brief IS the spec, and the brief carries the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` — the direction comes from the design-lead BEFORE the loop; the loop executes under it and does not re-derive a direction on its own.'''),
  # 5f gan-design :39: generator executes inside the recorded direction.
  ("commands/gan-design.md",
   r'''The Generator is told: "Your PRIMARY goal is visual excellence. A stunning half-finished app beats a functional ugly one. Push for creative leaps — unusual layouts, custom animations, distinctive color work."''',
   r'''The Generator is told: "Your PRIMARY goal is visual excellence within the recorded direction. A stunning half-finished app beats a functional ugly one. Push for creative leaps — unusual layouts, custom animations, distinctive color work — inside the design-lead's direction, never by re-deriving a new direction."'''),
  # 5g Shipped README: Grok 4.7 High picker note (post-STEP-4 patch).
  ("README.md",
   r'''- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate (run the gate explicitly — it does not auto-run on stop in Cursor).''',
   r'''- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate (run the gate explicitly — it does not auto-run on stop in Cursor).
- **Before the first build — Grok 4.7 High in the model picker:** the plugin pins its design role to `grok-4.7-high`. Cursor's subagent model allowlist is coupled to the model-picker dropdown, so select **Grok 4.7 High** in Cursor's model picker before the first build, or the design pin may silently fall back to another model. This is a one-time setup note, not a mid-build ask. File-level pin only — whether it holds is decided by the live smoke test (`LIVE_SMOKE_TEST.md` §14).'''),
  # 6a design-system Mode 1: package-generated direction, no competitors.
  ("skills/design-system/SKILL.md",
   r'''3. Research 3 competitor sites for inspiration (via browser MCP)''',
   r'''3. Generate the direction through the design package skills (`ui-ux-pro-max` direction / `design-taste-frontend` / dealt Hallmark theme) and record it in `design-tokens.md` — never competitor sites and never a searched external reference (orchestrate row-10 anti-derivative rule)'''),
  # 7a orch-add-feature skill: design-package rule (mirror orch-change-feature :36).
  ("skills/orch-add-feature/SKILL.md",
   r'''4. Add `security-reviewer` if the feature touches a security trigger.''',
   r'''4. Add `security-reviewer` if the feature touches a security trigger.
5. **UI change / build-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a new feature that builds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.'''),
  # 7b orch-fix-defect skill: design-package rule (mirror orch-change-feature :36).
  ("skills/orch-fix-defect/SKILL.md",
   r'''4. Add `security-reviewer` if the defect sits in a security-sensitive path.''',
   r'''4. Add `security-reviewer` if the defect sits in a security-sensitive path.
5. **UI change / rebuild-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a fix that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.'''),
  # 7c orch-refine-code skill: design-package rule as step 4 (commit renumbers to 5).
  ("skills/orch-refine-code/SKILL.md",
   r'''3. Stop at **Gate 1** (restructure plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. Commit as `refactor:` — the diff must be behavior-neutral.''',
   r'''3. Stop at **Gate 1** (restructure plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. **UI change / rebuild-a-surface rule.** If the change touches UI — including a restructure that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
5. Commit as `refactor:` — the diff must be behavior-neutral.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix13e anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    open(p, "w").write(t.replace(old, new))
print("fix13e upstream block applied")
PYEOF

"""

# Preflight anchors: (rel path in built tree, old text fragment, label)
PREFLIGHT = [
    ("skills/ui-ux-pro-max/SKILL.md",
     "if nothing is memorable, the surface fails even if every other check passes.",
     "1A captivating bar"),
    ("skills/ui-ux-pro-max/SKILL.md",
     "if a surface looks like a default template, it fails even if every checklist item passes.",
     "1B anti-generic bar"),
    ("skills/ui-ux-pro-max/SKILL.md",
     "its bans are absolute — a pinned brief never overrides a ban",
     "1C craft-floor bans"),
    ("skills/gan-style-harness/SKILL.md",
     "- 1-3: Generic, template-like, \"AI slop\" aesthetics",
     "2a rubric rows"),
    ("skills/gan-style-harness/SKILL.md",
     "Custom decisions vs. template/AI patterns?",
     "2b key behaviors"),
    ("skills/gan-style-harness/SKILL.md",
     "add explicit penalties for common AI patterns.",
     "2c anti-pattern #1"),
    ("agents/ecc-gan-planner.md",
     "4. Also write a concise `gan-harness/eval-rubric.md`",
     "2d planner validation"),
    ("skills/orch-build-mvp/SKILL.md",
     "every rubric written on any path must carry that deferral.",
     "2e orch step-4 validation"),
    ("commands/gan-build.md",
     "- Read eval-rubric.md and spec.md",
     "2f gan-build Phase 2 validation"),
    ("commands/gan-build.md",
     "### Phase 1: Planning (Planner Agent)",
     "2g gan-build Phase 1 skip note"),
    ("scripts/gan-harness.sh",
     "2. gan-harness/eval-rubric.md — Evaluation criteria for the Evaluator",
     "2h harness planner prompt"),
    ("scripts/gan-harness.sh",
     'if [ "$SKIP_PLANNER" = "true" ] && [ -f "${HARNESS_DIR}/spec.md" ]; then',
     "2i harness Phase 1 validation"),
    ("scripts/gan-harness.sh",
     "1. Read gan-harness/eval-rubric.md for scoring criteria",
     "2j harness evaluator prompt"),
    ("agents/ecc-gan-evaluator.md",
     "### Step 1: Read the Rubric",
     "2k evaluator Step 1 validation"),
    ("commands/gan-design.md",
     "the evaluator scores against `eval-rubric.md`, which carries that deferral.",
     "2l gan-design :36"),
    ("commands/gan-design.md",
     "3. Write a design-focused `gan-harness/eval-rubric.md`",
     "2m gan-design Setup step 3"),
    ("skills/gan-style-harness/SKILL.md",
     "- Quick single-file fixes (use standard `claude -p`)",
     "11a :30 claude -p"),
    ("skills/gan-style-harness/SKILL.md",
     "### Via Claude Code (Manual)",
     "11b manual heading"),
    ("skills/gan-style-harness/SKILL.md",
     "# Step 1: Plan\nclaude -p --model sonnet",
     "11c manual commands"),
    ("scripts/gan-harness.sh",
     "# Claude Code only — this script shells out to 'claude -p'",
     "11d harness header"),
    ("skills/orch-build-mvp/SKILL.md",
     "re-runs the step-6 every-route visual loop on the redesigned screens BEFORE the step-7 commit",
     "C3-2 orch 6b fresh run"),
    ("skills/orch-build-mvp/SKILL.md",
     "7. **Commit — orch-pipeline Phase 6.** Commit the scaffold",
     "C3-5 orch step 7 hold"),
    ("skills/orch-build-mvp/SKILL.md",
     "8. **Deploy via `deploy-fast`, then film via `/demo`",
     "C3-6 orch step 8 hold"),
    ("skills/design-system/SKILL.md",
     "Record slop findings with the screen and pattern for `browser-qa` to judge.",
     "C4-6 design-system destination"),
    ("skills/browser-qa/SKILL.md",
     "Each round: capture screenshots, then judge the rendered UI on typography",
     "C4-7 browser-qa read step"),
    ("skills/orch-build-mvp/SKILL.md",
     "The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop",
     "C5-4 orch :40 attribution"),
    ("skills/orch-build-mvp/SKILL.md",
     "`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop",
     "C5-5 orch step 6 attribution"),
    ("agents/ecc-gan-planner.md",
     "Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and design direction.",
     "5a planner description"),
    ("agents/ecc-gan-planner.md",
     "- **Direction source**: [named direction generated through the design package skills",
     "5b planner Direction source"),
    ("agents/ecc-gan-planner.md",
     '2. **Specify exact colors** — Not "blue theme"',
     "5c planner guideline 2"),
    ("commands/gan-build.md",
     "1. Launch the `gan-planner` agent as a Cursor subagent with the user's brief",
     "5d gan-build launch"),
    ("commands/gan-design.md",
     "No planner — the brief IS the spec.",
     "5e gan-design brief-is-spec"),
    ("commands/gan-design.md",
     'Push for creative leaps — unusual layouts,',
     "5f gan-design generator instruction"),
    ("README.md",
     "- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate",
     "5g shipped README picker note"),
    ("skills/design-system/SKILL.md",
     "3. Research 3 competitor sites for inspiration (via browser MCP)",
     "6a design-system Mode 1"),
    ("skills/orch-add-feature/SKILL.md",
     "4. Add `security-reviewer` if the feature touches a security trigger.",
     "7a orch-add-feature rule"),
    ("skills/orch-fix-defect/SKILL.md",
     "4. Add `security-reviewer` if the defect sits in a security-sensitive path.",
     "7b orch-fix-defect rule"),
    ("skills/orch-refine-code/SKILL.md",
     "4. Commit as `refactor:` — the diff must be behavior-neutral.",
     "7c orch-refine-code rule"),
]


def main():
    with open(BUILD_SH) as f:
        sh = f.read()
    assert "fix13e: Audit #45 blocking/minor" not in sh, "fix13e block already in build.sh — refusing (idempotency guard)"
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
    print("fix13e block inserted into build.sh (LAST, just before STEP 5)")


if __name__ == "__main__":
    main()
