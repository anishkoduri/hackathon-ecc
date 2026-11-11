#!/usr/bin/env python3
"""Fix program #13f — worker 2 (orchestration mechanics).

Staged-source edits (this script): new-skills/orchestrate/SKILL.md only —
that is the one in-scope file with a staged source (build.sh:219 copies it
verbatim; staged == built, verified by diff before writing).

ECC-base files (no staged source — upstream ECC copied from
/tmp/ecc-dev-install/.cursor and patched at build time) are NOT edited here.
Their edits live in fix13f/build-patch-w2.txt: a build.sh patch block in the
fix13e-assemble.py format (python heredoc, subs + count==1 asserts), to be
inserted LAST, just before STEP 5 (after the fix13e block). The files it
covers: skills/orch-build-mvp/SKILL.md, commands/gan-build.md,
commands/gan-design.md, agents/ecc-gan-planner.md,
agents/ecc-gan-evaluator.md, agents/ecc-gan-generator.md,
skills/orch-change-feature/SKILL.md.

Two-phase: ALL anchors (staged subs + build-patch old-strings, checked
against the CURRENT built tree) are verified count==1 BEFORE any write.
On failure the script exits non-zero having written nothing.

Items covered here (staged): B5 (orchestrate half), B1-orchestrate,
Audit M2 + dry-run M1 (orchestrate half: stacking rule + step-6 owner/
failure/wiring), Dry-run M2 (orchestrate half: PASSED record + step-6 named
check). Items covered in build-patch-w2.txt: B5 (orch-build-mvp half),
Audit M2 + dry-run M1 (orch-build-mvp 6b half), Dry-run M2 (orch-build-mvp
half), Dry-run M3, B6, Dry-run M4, Audit M1, Dry-run M5, Sweep M5.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGED = os.path.join(PLUGIN_ROOT, "new-skills/orchestrate/SKILL.md")
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")

# Snapshot rule definition (orchestrate wording; orch-build-mvp carries the
# same rule with "6b" in place of "5b" — see build-patch-w2.txt).
SNAPSHOT_RULE_ORCH = (
    " **Snapshot-before-redesign (file-copy snapshot — the cheap robust mechanism):**"
    " before the design skill overwrites any file, copy every file the redesign will touch"
    " (the redesigned screens' source files, enumerated from the polish routing / redesign brief)"
    " into `.hackathon/redesign-snapshot/<redesign-id>/` (one directory per redesign;"
    " `<redesign-id>` is the polish finding's short id, e.g. `landing-template`), preserving relative paths,"
    " and record the snapshot path + file list in `.hackathon/run-ledger.md`."
    " File-copy, not git: the tree may be uncommitted or have no repo at all, and a copy is deterministic to revert"
    " (copy the snapshot files back over the tree at their recorded relative paths)."
    " The snapshot is scratch under `.hackathon/` (never committed); keep it until the final report is delivered."
    " **Revert steps on a failed re-verification:** (1) copy every file in the snapshot back over the tree at its"
    " recorded relative path; (2) confirm the reverted files match the snapshot (re-read or diff);"
    " (3) record `re-verification: BLOCKED` + snapshot path + reverted files in the ledger and final report;"
    " (4) keep the deploy/commit hold — the redesign is not deployed, not committed, not filmed, and not reported as landed."
)

# (relative path, old text, new text, label) — staged sources only.
SUBS = [
# ---------------------------------------------------------------- B1 (:193)
("new-skills/orchestrate/SKILL.md",
 """apply the captivating/wow test (does a screen make a judge stop and stare — hackathon-scope's wow test, feature-expansion Lens D, design-taste-frontend's captivating-hero bar)""",
 """apply the captivating/wow test (does a screen make a judge stop and stare — hackathon-scope's wow test, feature-expansion Lens D; design-taste-frontend's captivating-hero bar is design guidance and candidate evidence feeding the verdict, never a bar `browser-qa` executes on its own)""",
 "B1 orchestrate :193: Taste captivating-hero bar re-pointed to candidate evidence"),
# ---------------------------------------------------------------- B5 (5b: snapshot before redesign)
("new-skills/orchestrate/SKILL.md",
 """if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run""",
 """if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the orchestrator first SNAPSHOTS the screens being redesigned (see the snapshot rule at the end of this bullet — copy the affected files to `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list in `.hackathon/run-ledger.md`, BEFORE any redesign file is overwritten), then the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run""",
 "B5 orchestrate 5b: snapshot BEFORE any redesign file is overwritten"),
# ------------------------------------------------- Audit M2 + dry-run M1 (5b: stacking rule)
("new-skills/orchestrate/SKILL.md",
 """on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them""",
 """on the fresh-verdict budget — 2 rounds total across 5b and step 6 (ONE shared budget, not two: rounds the step-6 finish-review re-inspection consumes count against the same 2; if both rounds are already spent there, no fresh round remains here) — on the redesigned screens only, at most 1 fix round per problem list; this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them""",
 "Audit M2 orchestrate 5b: ONE total fresh-verdict budget across 5b and step 6"),
# ------------------------------------------------- B5 + Dry-run M2 (5b: revert + PASSED record)
("new-skills/orchestrate/SKILL.md",
 """If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see 5c): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy.""",
 """If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see 5c): REVERT the redesigned screens to the snapshot (copy the snapshot files back over the tree, per the revert steps at the end of this bullet), record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report (with the snapshot path and the reverted files), and keep the hold — an unverified redesign never reaches deploy, and the tree the later steps film and report is the reverted, verified state. If the fresh run's final verdict passes, record `re-verification: PASSED` in `.hackathon/run-ledger.md` and the final report (with the screens re-verified); the 5c/step-6 checks below consult that ledger entry, not working-context memory.""" + SNAPSHOT_RULE_ORCH,
 "B5+Dry-run M2 orchestrate 5b: revert on fail, PASSED record on pass, snapshot rule"),
# ---------------------------------------------------------------- B5 (5c: verified tree)
("new-skills/orchestrate/SKILL.md",
 """do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Before the final deploy, run the `security-review`""",
 """do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). The 5d demo and the step-6 README/final report film and report the verified tree: after a revert that is the pre-redesign verified state, never the held redesign. Before the final deploy, run the `security-review`""",
 "B5 orchestrate 5c: deploy hold + verified tree filmed/reported"),
# ---------------------------------------------------------------- B5 (5d: film verified tree)
("new-skills/orchestrate/SKILL.md",
 """If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL.""",
 """If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL. `/demo` films the verified tree as it stands after any revert (see 5b) — a held redesign is never in the filmed tree.""",
 "B5 orchestrate 5d: film the verified tree after any revert"),
# ------------------------------------------------- Dry-run M2 (step 6: named check + revert)
("new-skills/orchestrate/SKILL.md",
 """if a polish-routed redesign failed re-verification, its files are not committed in this run — record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign""",
 """Before committing, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass — consult the `re-verification: PASSED` / `re-verification: BLOCKED` entry in `.hackathon/run-ledger.md`, not working-context memory. If a polish-routed redesign failed re-verification, its files are not committed in this run — they were already reverted to the snapshot (see 5b), so the tree being committed is the verified state — record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign""",
 "Dry-run M2 orchestrate step 6: named re-verification check (mirrors orch-build-mvp :55)"),
# ---------------------------------------------------------------- B5 (step 6: README verified tree)
("new-skills/orchestrate/SKILL.md",
 """so the README links the real URL and video instead of a placeholder""",
 """so the README links the real URL and video instead of a placeholder; it describes the verified tree, never a held redesign""",
 "B5 orchestrate step 6: README describes the verified tree"),
# ------------------------------------------------- Audit M2 + dry-run M1 (step 6: owner/fail/wiring)
("new-skills/orchestrate/SKILL.md",
 """append them to `.hallmark/candidate-evidence.md` for `browser-qa`, which re-inspects the affected screens on the fresh verdict run (up to 2 verdict rounds on the affected screens only, at most 1 fix round per problem list — a fresh budget, not the step-5 loop's consumed caps) before polish/deploy, and only its verdict decides whether a fix is owed.""",
 """append them to `.hallmark/candidate-evidence.md` for `browser-qa`. The ORCHESTRATOR runs the fresh verdict run on the affected screens (the fresh-verdict budget — 2 rounds total across 5b and step 6, at most 1 fix round per problem list; rounds consumed here count against the same 2), before polish/deploy, and only `browser-qa`'s verdict decides whether a fix is owed. If that run's final verdict still fails, the template finding stands and routes into the 5b redesign/hold/revert path: it becomes a polish-routed redesign in 5b (snapshot BEFORE the redesign is built, re-verification on the same shared budget, hold + revert to the snapshot on failure).""",
 "Audit M2 + dry-run M1 orchestrate step 6: owner (orchestrator), failure outcome, wiring into 5b"),
]

# Old-strings from build-patch-w2.txt, verified count==1 against the CURRENT
# built tree (preflight only — this script does not apply them).
PATCH_ANCHORS = [
 ("skills/orch-build-mvp/SKILL.md",
  "if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run"),
 ("skills/orch-build-mvp/SKILL.md",
  "on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-6 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them"),
 ("skills/orch-build-mvp/SKILL.md",
  "If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see steps 7/8): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy."),
 ("skills/orch-build-mvp/SKILL.md",
  "Before committing, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass?"),
 ("skills/orch-build-mvp/SKILL.md",
  "If no, or no fresh rounds remain, the commit of the redesign is HELD: do not commit the redesigned files in this run, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign"),
 ("skills/orch-build-mvp/SKILL.md",
  "Before deploying, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass?"),
 ("skills/orch-build-mvp/SKILL.md",
  "If no, or no fresh rounds remain, the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Otherwise, deploy the working MVP"),
 ("skills/orch-build-mvp/SKILL.md",
  "If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL."),
 ("skills/orch-build-mvp/SKILL.md",
  "a sloplint app-scope pass does NOT prove distinctiveness (that check lives only in the visual loop above). Review findings are fixed inside the capped 2-round fix loop"),
 ("commands/gan-build.md",
  "### Phase 1: Planning (Planner Agent)\nUnless `--skip-planner` is set (with `--skip-planner`, no rubric is written here — the existing `gan-harness/eval-rubric.md` is used as-is and is validated in Phase 2 before any scoring):\n1. Launch the `gan-planner` agent"),
 ("commands/gan-build.md",
  "plus the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` — the direction comes from the design-lead BEFORE the loop"),
 ("agents/ecc-gan-planner.md",
  "if no direction is recorded, record the brief's stated default, marked assumed, and proceed — never a searched external reference, per the anti-derivative rule"),
 ("commands/gan-design.md",
  "### Setup\n1. Create `gan-harness/` directory"),
 ("commands/gan-design.md",
  "the brief IS the spec, and the brief carries the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md`"),
 ("agents/ecc-gan-evaluator.md",
  "#### A. First Impression (30 seconds)\n- Does the page load without errors?\n- What's the immediate visual impression?\n- Does it feel like a real product or a tutorial project?\n- Is there a clear visual hierarchy?"),
 ("agents/ecc-gan-generator.md",
  "The Evaluator will specifically penalize these patterns. **Avoid them:**"),
 ("skills/orch-change-feature/SKILL.md",
  "and update the video LINK wherever it appears (the Devpost submission and the README if it embeds it) — text updates alone leave the judge-visible artefact stale, so the link must point at the re-uploaded video, not the pre-removal one; ELSE (no hosted video link exists"),
 ("skills/orch-change-feature/SKILL.md",
  "the re-uploaded video link if a hosted video existed, else the honest hosting note from step 5"),
]


def main():
    # Phase 1 — verify every staged anchor count==1 (preflight, no writes).
    staged_txt = open(STAGED, encoding="utf-8").read()
    failures = []
    for rel, old, _new, label in SUBS:
        n = staged_txt.count(old)
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
        assert staged_txt.count(old) == 1, label
        staged_txt = staged_txt.replace(old, new)
        print(f"  applied: {label}")
    open(STAGED, "w", encoding="utf-8").write(staged_txt)
    print(f"Wrote {STAGED} ({len(SUBS)} subs). Built tree untouched; build.sh untouched.")


if __name__ == "__main__":
    main()
