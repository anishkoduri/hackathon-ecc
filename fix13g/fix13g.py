#!/usr/bin/env python3
"""Fix round #13g — staged-source edits + preflight of the build patch.

Staged sources edited here (verified staged == built by diff before writing):
- new-skills/orchestrate/SKILL.md (B3 definition + ledger lines, M3 budget
  check, M5 supersede scoping, M4 revert diff — orchestrate half)
- new-skills/design-taste-frontend/references/hallmark/references/gates.md
  (Audit M3: Step 4/7 home named in the staged-scope note)
- round2-skills/polish-pass/reference/craft-floor.md (Sweep M2: template
  bans scoped to candidate evidence)
- round2-skills/polish-pass/reference/impeccable-critique.md (Sweep M3:
  specificity assessment only to candidate evidence)

ECC-base files (no staged source) are NOT edited here. Their edits live in
fix13g/build-patch-g.txt: a build.sh patch block in the fix13e/fix13f format
(python heredoc, subs + count==1 asserts), to be inserted LAST, just before
STEP 5 (after the fix13f block). Files it covers:
skills/orch-build-mvp/SKILL.md (B1 step-6 fresh run + render fallback, B2
sloplint landing run, B3 definition + ledger lines, B4 step-8 deploy,
M3 budget check, M4 revert diff, M5 supersede), commands/gan-build.md
(M1 predicate, M2 step 0 under --skip-planner), commands/gan-design.md
(M1 wrong-object fix), skills/orch-change-feature/SKILL.md (M6 re-upload
condition), rules/web-design-quality.mdc (Sweep M1).

Two-phase: ALL anchors (staged subs + build-patch old-strings, checked
against the CURRENT built tree) are verified count==1 BEFORE any write.
On failure the script exits non-zero having written nothing.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")

# Shared wording -----------------------------------------------------------
ROUND_DEF = (
    " **What a 'round' is (definition — same in both engines):** one `browser-qa`"
    " verdict run (one inspect-and-render-verdict pass on the screens in scope)."
    " The orchestrator is the counter: after every verdict run that draws on this"
    " budget, it updates the single ledger line `fresh-verdict rounds used: N/2` in"
    " `.hackathon/run-ledger.md` (N = rounds consumed so far in this run, out of 2)"
    " and consults that line before spending another round — never spend from"
    " working-context memory."
)

# (relative path, old text, new text, label) — staged sources only.
SUBS = [
# ------------------------------------------------- B3 (orchestrate 5b: definition)
("new-skills/orchestrate/SKILL.md",
 """on the fresh-verdict budget — 2 rounds total across 5b and step 6 (ONE shared budget, not two: rounds the step-6 finish-review re-inspection consumes count against the same 2; if both rounds are already spent there, no fresh round remains here) — on the redesigned screens only, at most 1 fix round per problem list; this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them""",
 """on the fresh-verdict budget — 2 rounds total across 5b and step 6 (ONE shared budget, not two: rounds the step-6 finish-review re-inspection consumes count against the same 2; if both rounds are already spent there, no fresh round remains here) — on the redesigned screens only, at most 1 fix round per problem list (a fix round costs one round: the re-verdict run that closes it); this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them""" + ROUND_DEF,
 "B3 orchestrate 5b: 'round' defined, orchestrator named counter, ledger line required"),
# ------------------------------------------------- B3 (orchestrate 5b: ledger line)
("new-skills/orchestrate/SKILL.md",
 """the redesign decision follows `browser-qa`'s verdict.""",
 """the redesign decision follows `browser-qa`'s verdict. After the run, the orchestrator records `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` (see the round definition above) and consults that line before spending more.""",
 "B3 orchestrate 5b: ledger line after the fresh run"),
# ------------------------------------------------- M3 + M5 (orchestrate 5b: budget check + supersede)
("new-skills/orchestrate/SKILL.md",
 """BEFORE any redesign file is overwritten), then the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the 5c deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on the fresh-verdict budget""",
 """BEFORE any redesign file is overwritten), then checks the remaining fresh-verdict budget in `.hackathon/run-ledger.md` (`fresh-verdict rounds used: N/2`): if no rounds remain, HOLD immediately without building — do NOT build the redesign, record `re-verification: BLOCKED` (no fresh-verdict rounds remain) in the ledger and the final report, and keep the hold; the tree stays the verified state. Otherwise the design skill builds it, the orchestrator marks the candidate-evidence entries about the redesigned screens as superseded in `.hallmark/candidate-evidence.md` (`Superseded by redesign <redesign-id> — do not re-judge`), and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the 5c deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md` — scoped to evidence about the redesigned screens only, never stale evidence about the pre-redesign screens — on the fresh-verdict budget""",
 "M3+M5 orchestrate 5b: budget check before building; superseded entries marked, fresh run scoped"),
# ------------------------------------------------- M4 (orchestrate snapshot rule: coverage check)
("new-skills/orchestrate/SKILL.md",
 """and record the snapshot path + file list in `.hackathon/run-ledger.md`. File-copy, not git: the tree may be uncommitted or have no repo at all, and a copy is deterministic to revert (copy the snapshot files back over the tree at their recorded relative paths). The snapshot is scratch under `.hackathon/` (never committed); keep it until the final report is delivered.""",
 """and record the snapshot path + file list in `.hackathon/run-ledger.md`. File-copy, not git: the tree may be uncommitted or have no repo at all, and a copy is deterministic to revert (copy the snapshot files back over the tree at their recorded relative paths). The snapshot is scratch under `.hackathon/` (never committed); keep it until the final report is delivered. After the build, the orchestrator compares the design skill's changed-file list against the snapshot file list; any file the redesign touched outside the enumeration is recorded in `.hackathon/run-ledger.md` as a snapshot-coverage gap before the fresh verdict runs (restored on revert per step (2) below, or named as unreverted if no copy exists).""",
 "M4 orchestrate snapshot rule: changed-file list checked against the snapshot"),
# ------------------------------------------------- M4 (orchestrate revert steps: diff tree vs snapshot)
("new-skills/orchestrate/SKILL.md",
 """**Revert steps on a failed re-verification:** (1) copy every file in the snapshot back over the tree at its recorded relative path; (2) confirm the reverted files match the snapshot (re-read or diff); (3) record `re-verification: BLOCKED` + snapshot path + reverted files in the ledger and final report; (4) keep the deploy/commit hold — the redesign is not deployed, not committed, not filmed, and not reported as landed.""",
 """**Revert steps on a failed re-verification:** (1) copy every file in the snapshot back over the tree at its recorded relative path; (2) confirm the reverted files match the snapshot (re-read or diff) AND diff the tree against the snapshot directory to catch any file the redesign touched outside the snapshot enumeration — any such file is restored from version control if the tree is under it (`git checkout -- <file>` where the file was committed), otherwise named in the ledger and final report as a snapshot-coverage gap (the hold stands regardless); (3) record `re-verification: BLOCKED` + snapshot path + reverted files in the ledger and final report; (4) keep the deploy/commit hold — the redesign is not deployed, not committed, not filmed, and not reported as landed.""",
 "M4 orchestrate revert steps: diff tree against the snapshot directory"),
# ------------------------------------------------- B3 (orchestrate step 6: ledger line)
("new-skills/orchestrate/SKILL.md",
 """The ORCHESTRATOR runs the fresh verdict run on the affected screens (the fresh-verdict budget — 2 rounds total across 5b and step 6, at most 1 fix round per problem list; rounds consumed here count against the same 2), before polish/deploy, and only `browser-qa`'s verdict decides whether a fix is owed.""",
 """The ORCHESTRATOR runs the fresh verdict run on the affected screens (the fresh-verdict budget — 2 rounds total across 5b and step 6, at most 1 fix round per problem list; rounds consumed here count against the same 2; after the run, the orchestrator records `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` (see the round definition in 5b) and consults that line before spending more), before polish/deploy, and only `browser-qa`'s verdict decides whether a fix is owed.""",
 "B3 orchestrate step 6: ledger line after the fresh run"),
# ------------------------------------------------- Audit M3 (gates.md staged-scope note)
("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
 """a citation to an unstaged file is never a reason to stop the build.""",
 """a citation to an unstaged file is never a reason to stop the build. The 'Step 4' / 'Step 7' walk named in the next paragraph is the upstream Hallmark build/review walk (the unstaged Hallmark build-playbook), not steps in this plugin. In this plugin's staged flow: §1–§3 drive the pre-emit pass (gates.md §3), §4 the build, §5 the Finish checks and the judged clauses at the finish review, §6 the two reviews (hero + finish).""",
 "Audit M3 gates.md: Step 4/7 home named in the staged-scope note"),
# ------------------------------------------------- Sweep M2 (craft-floor :111: template split)
("round2-skills/polish-pass/reference/craft-floor.md",
 """Each of these marks a UI as generated rather than designed. Remove or rewrite the element; do not just tone it down. Each ban is a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone).""",
 """Each of these marks a UI as generated rather than designed. Each ban is a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone). Non-template bans (accessibility, dark patterns, copy, effects, type): remove or rewrite the element; do not just tone it down. Template-pattern bans (the centered-everything hero, the hero-metric template, grids of identical cards, equal-weight text-only feature sections): do NOT fix on this check alone — append the finding (screen + pattern) to `.hallmark/candidate-evidence.md` for `browser-qa`; it is fixed only on `browser-qa`'s verdict, or when the project's design notes explicitly allow the pattern.""",
 "Sweep M2 craft-floor :111: template-pattern bans to candidate evidence, not must-fix"),
# ------------------------------------------------- Sweep M2 (craft-floor :168: scope must-fix)
("round2-skills/polish-pass/reference/craft-floor.md",
 """4. Scan for every Ban. Any remaining ban is a finding in the report; the polish pass is not done until it is fixed or the project's design notes explicitly allow it.""",
 """4. Scan for every Ban. Any remaining non-template ban is a finding in the report; the polish pass is not done until it is fixed or the project's design notes explicitly allow it. A remaining template-pattern ban is done when it is appended to `.hallmark/candidate-evidence.md` (screen + pattern) for `browser-qa` — it is fixed only on `browser-qa`'s verdict or a design-notes exception, never on this check alone.""",
 "Sweep M2 craft-floor :168: must-fix compulsion scoped to non-template bans"),
# ------------------------------------------------- Sweep M3 (critique :142: assessment only to evidence)
("round2-skills/polish-pass/reference/impeccable-critique.md",
 """Record the outcome as candidate evidence for `browser-qa`'s visual-loop verdict, not as a verdict: the assessment informs the Priority fixes, but only `browser-qa`'s verdict can establish a generic-template finding.""",
 """Record the outcome as candidate evidence for `browser-qa`'s visual-loop verdict, not as a verdict: the specificity assessment goes only to `.hallmark/candidate-evidence.md` (screen + what reads as a template) and never into the Priority fixes as a template finding; Priority fixes carry a generic-template item only when `browser-qa`'s verdict has established it — other Priority fixes carry non-specificity issues only.""",
 "Sweep M3 critique :142: specificity assessment only to candidate evidence"),
]

# Old-strings from build-patch-g.txt, verified count==1 against the CURRENT
# built tree (preflight only — this script does not apply them).
PATCH_ANCHORS = [
 ("skills/orch-build-mvp/SKILL.md",
  "on the fresh-verdict budget — 2 rounds total across 6b and step 6 (ONE shared budget, not two: rounds the step-6 finish-review re-inspection consumes count against the same 2; if both rounds are already spent there, no fresh round remains here) — on the redesigned screens only, at most 1 fix round per problem list; this budget is separate from the step-6 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them"),
 ("skills/orch-build-mvp/SKILL.md",
  "the redesign decision follows `browser-qa`'s verdict."),
 ("skills/orch-build-mvp/SKILL.md",
  "BEFORE any redesign file is overwritten), then the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the step-7 commit and step-8 deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on the fresh-verdict budget"),
 ("skills/orch-build-mvp/SKILL.md",
  "and record the snapshot path + file list in `.hackathon/run-ledger.md`. File-copy, not git: the tree may be uncommitted or have no repo at all, and a copy is deterministic to revert (copy the snapshot files back over the tree at their recorded relative paths). The snapshot is scratch under `.hackathon/` (never committed); keep it until the final report is delivered."),
 ("skills/orch-build-mvp/SKILL.md",
  "**Revert steps on a failed re-verification:** (1) copy every file in the snapshot back over the tree at its recorded relative path; (2) confirm the reverted files match the snapshot (re-read or diff); (3) record `re-verification: BLOCKED` + snapshot path + reverted files in the ledger and final report; (4) keep the deploy/commit hold — the redesign is not deployed, not committed, not filmed, and not reported as landed."),
 ("skills/orch-build-mvp/SKILL.md",
  "a sloplint app-scope pass does NOT prove distinctiveness (that check lives only in the visual loop above). Then, on a build with a landing page, run the Hallmark landing audit as candidate-evidence generation for `browser-qa` (not a verdict): the 6-axis pre-emit self-critique"),
 ("skills/orch-build-mvp/SKILL.md",
  "and the Hallmark finish review in a fresh context (`skills/design-taste-frontend/references/hallmark/references/review-finish.md`), whose template observations (`Seen before`, machine-made) are likewise appended to `.hallmark/candidate-evidence.md` for `browser-qa`; its gates, plain defects, copy, and layout findings join the fix batch (same capped 2-round fix loop)."),
 ("skills/orch-build-mvp/SKILL.md",
  "A standalone first build's landing page otherwise produces no gates Specificity evidence or finish-review template observations for candidate evidence. Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on."),
 ("skills/orch-build-mvp/SKILL.md",
  "and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). The demo films and the README describes the verified tree: after a revert that is the pre-redesign verified state, never the held redesign. Otherwise, deploy the working MVP"),
 ("skills/orch-build-mvp/SKILL.md",
  "Have the first UI slice in the GAN loop write `docs/design-tokens.md` from its design system (per orchestrate's no-landing fallback) so later slices brief from real tokens."),
 ("commands/gan-build.md",
  "0. Design-direction check (cold start) — BEFORE launching the planner, check whether `docs/design-tokens.md` carries a direction recorded by the design-lead (model `grok-4.7-high`): if it does, pass it to the planner as in step 1;"),
 ("commands/gan-build.md",
  "### Phase 1: Planning (Planner Agent)\nUnless `--skip-planner` is set (with `--skip-planner`, no rubric is written here — the existing `gan-harness/eval-rubric.md` is used as-is and is validated in Phase 2 before any scoring):\n0. Design-direction check (cold start)"),
 ("commands/gan-design.md",
  "the brief IS the spec, and the brief carries the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` (Setup step 0 records it first on a cold start)"),
 ("commands/gan-design.md",
  "0. Design-direction check (cold start) — BEFORE writing the spec or rubric, check whether the brief carries a direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md`: if it does, proceed as below;"),
 ("skills/orch-change-feature/SKILL.md",
  "After re-filming, IF a hosted video link exists (in the Devpost submission, the README, or the final report), re-upload the new video to the same YouTube/Vimeo host (upload HOURS before the deadline — processing can take several hours, per `devpost-autofiller`) and update the video LINK wherever it appears (the Devpost submission and the README if it embeds it) — text updates alone leave the judge-visible artefact stale, so the link must point at the re-uploaded video, not the pre-removal one."),
 ("rules/web-design-quality.mdc",
  "Do not ship generic template-looking UI. Frontend output should look intentional, opinionated, and specific to the product."),
 ("rules/web-design-quality.mdc",
  "## Anti-Template Policy"),
 ("rules/web-design-quality.mdc",
  "### Banned Patterns"),
 ("rules/web-design-quality.mdc",
  "- [ ] Does it avoid looking like a default Tailwind or shadcn template?"),
]


def main():
    # Phase 1 — verify every staged anchor count==1 (preflight, no writes).
    failures = []
    for rel, old, _new, label in SUBS:
        txt = open(os.path.join(PLUGIN_ROOT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != 1:
            failures.append(f"STAGED {label}: count={n}")
    # Phase 1b — verify every build-patch anchor count==1 in the built tree.
    for rel, old in PATCH_ANCHORS:
        txt = open(os.path.join(BUILT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != 1:
            failures.append(f"PATCH-ANCHOR {rel}: count={n} :: {old[:60]!r}")
    if failures:
        print("PREFLIGHT FAILED — wrote nothing:")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print(f"Preflight OK: {len(SUBS)} staged subs + {len(PATCH_ANCHORS)} patch anchors, all count==1.")

    # Phase 2 — apply staged subs.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        txt = open(p, encoding="utf-8").read()
        assert txt.count(old) == 1, label
        open(p, "w", encoding="utf-8").write(txt.replace(old, new))
        print(f"  applied: {label}")
    print(f"Wrote {len(SUBS)} staged subs. Built tree untouched; build.sh untouched.")


if __name__ == "__main__":
    main()
