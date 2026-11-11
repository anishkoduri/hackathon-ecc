#!/usr/bin/env python3
"""Fix round #13i — staged-source edits + preflight of the build patch.

Scope (1 blocking + 11 minor, parent-verified in the built tree):
- B1 (blocking): whole-tree snapshot has no `.hackathon/` exclusion; revert
  restores a stale ledger and corrupts the fresh-verdict budget (dry-run B1,
  orchestrate :60, standalone :53). Fix: exclude `.hackathon/` AND
  `.hallmark/candidate-evidence.md` (live run state) from the snapshot copy;
  revert never restores run-state files; the ledger's rounds-used line and the
  `Superseded by redesign` markings survive a revert as written.
- Audit M1: polish.md :18,19,39,40 — 5 links with a `reference/` prefix that
  does not resolve from the file's own directory. Drop the prefix. Do NOT
  touch the identical prefix in polish-pass/SKILL.md:92 (correct there).
- DR-M1: orchestrate :60 "the 5c/Verify-step-6 checks below" misdirects (the
  real checks are 5c :61 and step 6 :64). Fix the pointer.
- DR-M2: Verification stage has TWO items numbered "Verify step 4" (:187
  blind UI reviewer, :191 adversarial audit). Renumber 4a / 4b. Nothing
  dereferences "Verify step 4" elsewhere (verified by grep).
- DR-M3: no uniqueness rule for `<redesign-id>`. Append -2, -3, ... on
  collision.
- DR-M4: revert "verify with `git status`" has no no-repo fallback. Verify
  against the snapshot manifest alone when there is no repo.
- DR-M5: `fresh-verdict rounds used: N/2` never initialized to `0/2`.
  Create it as `0/2` when the run ledger is first created (Gate 1); if
  missing when first consulted, create it as `0/2` before spending.
- DR-M6: polish.md Step 5.2 detector path has no template-pattern carve-out
  (`icon-tile-stack`, rules.json:175). Route to candidate evidence.
- DR-M7: duplicated ledger-update sentence in the step-6 fresh-run
  paragraphs (orchestrate :195, standalone :49). Remove it; the round
  definition in 5b/6b is the single source.
- Sweep M1: gates.md:225 gate 68 wireframe clause declares the rendered
  page reads as a wireframe with no candidate-evidence routing. Route it.
- Sweep M2/M3 (parent decision: REWORD): review-finish.md:5 first word
  `rebuild`/`fix`/`ship` and review-hero.md:5 `ship`/`fix` are ship/fix/
  rebuild verdicts by reviewers other than browser-qa. New vocabulary:
  `recapture` (kept — an instruction, not a verdict), `findings`,
  `no-findings`. Consumers updated in the same round: orchestrate :195,
  standalone :49, Taste :314, gates.md:245 (the §6 walk branches on
  `rebuild` and records `hero-review: fix` in the stamp — both reworded).
  The gates §6 ship rule and the Taste gate are NOT re-adjudicated.

Staged sources edited here (verified staged == built by diff, except Taste
SKILL.md which differs from built only in the pre-existing build-time
frontmatter region — its edited line is verified by built-tree
present-checks after rebuild):
- new-skills/orchestrate/SKILL.md (B1, M1, M2, M3, M4, M5, M7, sweep M2
  consumer)
- round2-skills/polish-pass/reference/polish.md (Audit M1, DR-M6)
- new-skills/design-taste-frontend/references/hallmark/references/gates.md
  (sweep M1, sweep M2 consumer :245)
- new-skills/design-taste-frontend/references/hallmark/references/review-finish.md
  (sweep M2)
- new-skills/design-taste-frontend/references/hallmark/references/review-hero.md
  (sweep M3)
- new-skills/design-taste-frontend/SKILL.md (sweep M3 consumer :314)

ECC-base files (no staged source) are NOT edited here. Their edits live in
fix13i/build-patch-i.txt: a build.sh patch block in the fix13h format
(python heredoc, subs + count==1 asserts), to be inserted LAST, just before
STEP 5 (after the fix13h block). Files it covers:
skills/orch-build-mvp/SKILL.md (B1, M3, M4, M5, M7, sweep M2 consumer).

Two-phase: ALL anchors (staged subs + build-patch old-strings, checked
against the CURRENT built tree) are verified BEFORE any write. On failure
the script exits non-zero having written nothing.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")

# --- Shared wording (identical in both engines) ---------------------------
SNAP_INTRO_OLD = (
    "the orchestrator first SNAPSHOTS the whole tree (see the snapshot rule at"
    " the end of this bullet \u2014 copy the whole tree to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list +"
    " per-file hashes in `.hackathon/run-ledger.md`, BEFORE any redesign file"
    " is overwritten)"
)
SNAP_INTRO_NEW = (
    "the orchestrator first SNAPSHOTS the whole tree (see the snapshot rule at"
    " the end of this bullet \u2014 copy the whole tree, except `.hackathon/`"
    " and `.hallmark/candidate-evidence.md`, to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list +"
    " per-file hashes in `.hackathon/run-ledger.md`, BEFORE any redesign file"
    " is overwritten)"
)
SNAP_RULE_OLD = (
    "before the design skill overwrites any file, copy the WHOLE tree into"
    " `.hackathon/redesign-snapshot/<redesign-id>/` (one directory per redesign;"
    " `<redesign-id>` is the polish finding's short id, e.g. `landing-template`),"
    " preserving relative paths, and record the snapshot path + the full file list"
    " + per-file hashes in `.hackathon/run-ledger.md`. The snapshot covers every"
    " file in the tree, not just the files the redesign brief enumerates \u2014 the"
    " brief enumeration is not the snapshot boundary."
)
SNAP_RULE_NEW = (
    "before the design skill overwrites any file, copy the WHOLE tree EXCEPT"
    " `.hackathon/` and `.hallmark/candidate-evidence.md` into"
    " `.hackathon/redesign-snapshot/<redesign-id>/` (one directory per redesign;"
    " `<redesign-id>` is the polish finding's short id, e.g. `landing-template`),"
    " preserving relative paths, and record the snapshot path + the full file list"
    " (excluding those two paths) + per-file hashes in `.hackathon/run-ledger.md`."
    " The snapshot covers every file in the tree except those two exclusions, not"
    " just the files the redesign brief enumerates \u2014 the brief enumeration is"
    " not the snapshot boundary. The exclusions have two reasons: the snapshot"
    " directory lives inside the tree being copied, so a literal whole-tree copy"
    " would copy the snapshot into itself; and `.hackathon/` and"
    " `.hallmark/candidate-evidence.md` hold live run state, not tree state \u2014 the"
    " run ledger and the candidate-evidence markings are never snapshotted and"
    " never restored by a revert. Two redesigns never share an id: if a snapshot"
    " directory or a `re-verification <redesign-id>:` ledger entry with that id"
    " already exists, append `-2`, `-3`, \u2026 until the id is unused."
)
COVERAGE_OLD = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot manifest; every file the redesign touched is"
    " covered by the whole-tree snapshot, so there is no snapshot-coverage gap by"
    " construction \u2014 a file on the changed-file list that is missing from the"
    " manifest is recorded in `.hackathon/run-ledger.md` as a snapshot-integrity"
    " failure before the fresh verdict runs (and the hold stands until the snapshot"
    " is repaired or the redesign is abandoned)."
)
COVERAGE_NEW = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot manifest; every file the redesign touched is"
    " covered by the whole-tree snapshot, so there is no snapshot-coverage gap by"
    " construction \u2014 a file on the changed-file list that is missing from the"
    " manifest is recorded in `.hackathon/run-ledger.md` as a snapshot-integrity"
    " failure before the fresh verdict runs (and the hold stands until the snapshot"
    " is repaired or the redesign is abandoned) \u2014 except the two excluded"
    " run-state paths (`.hackathon/`, `.hallmark/candidate-evidence.md`), which"
    " are never in the manifest by design and are never a coverage failure."
)
REVERT1_OLD = (
    "(1) copy every file in the snapshot back over the tree at its recorded"
    " relative path (the snapshot is the whole tree, so this restores the verified"
    " state exactly);"
)
REVERT1_NEW = (
    "(1) copy every file in the snapshot back over the tree at its recorded"
    " relative path (the snapshot is the whole tree except `.hackathon/` and"
    " `.hallmark/candidate-evidence.md`, so this restores the verified state"
    " exactly \u2014 except run state: the live `.hackathon/run-ledger.md` and"
    " `.hallmark/candidate-evidence.md` are NEVER overwritten by a revert, so the"
    " ledger's `fresh-verdict rounds used: N/2` line and the `Superseded by"
    " redesign <redesign-id> \u2014 do not re-judge` markings survive a revert as"
    " written);"
)
REVERT2_OLD = (
    "confirm the reverted files match the snapshot (re-read or diff) AND delete"
    " every file the redesign created that the snapshot does not contain \u2014"
    " identify created files from the design skill's changed-file list plus the"
    " `git status` untracked listing, or by comparing the post-redesign tree"
    " against the snapshot manifest \u2014 then restore modified files from the"
    " SNAPSHOT COPY, never from version control alone (`git checkout` restores"
    " HEAD, not the verified state, and never deletes untracked files; nothing is"
    " committed to restore from in the normal first-build timeline), and verify"
    " with `git status` plus a diff restricted to snapshot-listed paths (each"
    " restored path diffed against its snapshot copy)."
)
REVERT2_NEW = (
    "confirm the reverted files match the snapshot (re-read or diff) AND delete"
    " every file the redesign created that the snapshot does not contain \u2014 other"
    " than the excluded run-state paths (`.hackathon/`,"
    " `.hallmark/candidate-evidence.md`), which are never deleted \u2014 identify"
    " created files from the design skill's changed-file list plus the `git status`"
    " untracked listing, or by comparing the post-redesign tree against the"
    " snapshot manifest \u2014 then restore modified files from the SNAPSHOT COPY,"
    " never from version control alone (`git checkout` restores HEAD, not the"
    " verified state, and never deletes untracked files; nothing is committed to"
    " restore from in the normal first-build timeline), and verify with `git status`"
    " (when the tree is a git repo) plus a diff restricted to snapshot-listed paths"
    " (each restored path diffed against its snapshot copy); when the tree has no"
    " repo, verify against the snapshot manifest alone \u2014 each restored path"
    " diffed against its snapshot copy and its recorded hash \u2014 the manifest check"
    " is the fallback and the authority, `git status` is only a convenience."
)
REVERT3_OLD = (
    "(3) record `re-verification <redesign-id>: BLOCKED` + snapshot path +"
    " reverted files in the ledger and final report;"
)
REVERT3_NEW = (
    "(3) record `re-verification <redesign-id>: BLOCKED` + snapshot path +"
    " reverted files in the ledger and final report (the ledger's `fresh-verdict"
    " rounds used: N/2` line is untouched by the revert \u2014 run state is never"
    " restored \u2014 so the round spent on the failed re-verification stays spent);"
)
COUNTER_OLD = (
    "The orchestrator is the counter: after every verdict run that draws on this"
    " budget, it updates the single ledger line `fresh-verdict rounds used: N/2`"
    " in `.hackathon/run-ledger.md` (N = rounds consumed so far in this run, out"
    " of 2) and consults that line before spending another round \u2014 never spend"
    " from working-context memory;"
)
COUNTER_NEW = (
    "The orchestrator is the counter: the line is created as `fresh-verdict rounds"
    " used: 0/2` in `.hackathon/run-ledger.md` when the run ledger is first created"
    " (at Gate 1, before the Verification stage) \u2014 if it is missing when first"
    " consulted, create it as `0/2` before spending, never spend from a missing"
    " line \u2014 and after every verdict run that draws on this budget, it updates"
    " the single ledger line `fresh-verdict rounds used: N/2` in"
    " `.hackathon/run-ledger.md` (N = rounds consumed so far in this run, out of 2)"
    " and consults that line before spending another round \u2014 never spend from"
    " working-context memory;"
)

# --- Staged subs: (staged rel path, old, new) --------------------------------
STAGED = [
    # B1 orchestrate 5b.
    ("new-skills/orchestrate/SKILL.md", SNAP_INTRO_OLD, SNAP_INTRO_NEW),
    ("new-skills/orchestrate/SKILL.md", SNAP_RULE_OLD, SNAP_RULE_NEW),
    ("new-skills/orchestrate/SKILL.md", COVERAGE_OLD, COVERAGE_NEW),
    ("new-skills/orchestrate/SKILL.md", REVERT1_OLD, REVERT1_NEW),
    ("new-skills/orchestrate/SKILL.md", REVERT2_OLD, REVERT2_NEW),
    ("new-skills/orchestrate/SKILL.md", REVERT3_OLD, REVERT3_NEW),
    # M5 orchestrate 5b: budget initialized to 0/2.
    ("new-skills/orchestrate/SKILL.md", COUNTER_OLD, COUNTER_NEW),
    # M1 orchestrate 5b: fix the check pointer.
    ("new-skills/orchestrate/SKILL.md",
     "the 5c/Verify-step-6 checks below consult the entry for that redesign-id",
     "the 5c and step-6 checks below consult the entry for that redesign-id"),
    # M2 orchestrate Verification stage: two "Verify step 4" items -> 4a/4b.
    ("new-skills/orchestrate/SKILL.md",
     "Verify step 4. **Any diff that touches a UI surface (any size)**",
     "Verify step 4a. **Any diff that touches a UI surface (any size)**"),
    ("new-skills/orchestrate/SKILL.md",
     "**Verify step 4. Adversarial audit (a distinct named step \u2014 after the reviewer pass, before deploy).**",
     "**Verify step 4b. Adversarial audit (a distinct named step \u2014 after the reviewer pass, before deploy).**"),
    # M7 orchestrate Verify step 6: duplicated ledger-update sentence removed.
    ("new-skills/orchestrate/SKILL.md",
     "after the run, the orchestrator records `fresh-verdict rounds used: N/2` in"
     " `.hackathon/run-ledger.md` (see the round definition in 5b) and consults"
     " that line before spending more",
     "the round definition in 5b states the ledger update, and the orchestrator"
     " consults that line before spending more"),
    # Sweep M2 consumer, orchestrate Verify step 6: first-word vocabulary.
    ("new-skills/orchestrate/SKILL.md",
     "Act on its first word (`recapture` / `rebuild` / `fix` / `ship`) for the"
     " gates, plain defects, copy, and layout findings; findings join the fix batch",
     "Act on its first word (`recapture` / `findings` / `no-findings`) for the"
     " gates, plain defects, copy, and layout findings; findings join the fix batch"),
    # Audit M1 polish.md: drop the reference/ prefix on the five links.
    ("round2-skills/polish-pass/reference/polish.md",
     "[reference/impeccable-detector-rules.json](reference/impeccable-detector-rules.json)",
     "[impeccable-detector-rules.json](impeccable-detector-rules.json)"),
    ("round2-skills/polish-pass/reference/polish.md",
     "[reference/impeccable-critique.md](reference/impeccable-critique.md)",
     "[impeccable-critique.md](impeccable-critique.md)"),
    ("round2-skills/polish-pass/reference/polish.md",
     "[reference/impeccable-craft-floor.md](reference/impeccable-craft-floor.md)",
     "[impeccable-craft-floor.md](impeccable-craft-floor.md)"),
    ("round2-skills/polish-pass/reference/polish.md",
     "[reference/impeccable-onboard.md](reference/impeccable-onboard.md)",
     "[impeccable-onboard.md](impeccable-onboard.md)"),
    ("round2-skills/polish-pass/reference/polish.md",
     "[reference/impeccable-extract.md](reference/impeccable-extract.md)",
     "[impeccable-extract.md](impeccable-extract.md)"),
    # DR-M6 polish.md Step 5.2: detector template-pattern carve-out.
    ("round2-skills/polish-pass/reference/polish.md",
     "Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`),"
     " and fix real findings the same way.",
     "Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`),"
     " and fix real findings the same way \u2014 EXCEPT a template-pattern finding"
     " (e.g. `icon-tile-stack`: a small rounded-square icon container above a"
     " heading is the universal AI feature-card template): append it to"
     " `.hallmark/candidate-evidence.md` (screen + what reads as a template) for"
     " `browser-qa`, and fix it only on `browser-qa`'s verdict \u2014 never rewrite a"
     " template pattern on the detector's say-so alone."),
    # Sweep M1 gates.md:68 wireframe clause to candidate evidence.
    ("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
     "each holding a library photograph or the product built.",
     "each holding a library photograph or the product built. The wireframe read"
     " is candidate evidence of a generated look, for `browser-qa` to weigh at a"
     " glance."),
    # Sweep M2 consumer, gates.md §6: rebuild branch + stamp record reworded.
    ("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
     "Send the recaptures back for one scoring round only when the first word was"
     " `rebuild` or a finding named a Floor gate; scoring is not a second review."
     " Record the outcome in the stamp, hero first: `hero-review: fix \u00b7 4"
     " findings \u00b7 4 resolved`, then `finish-review: subagent \u00b7 5 findings \u00b7 4"
     " resolved 1 unresolved \u00b7 gap: none`.",
     "Send the recaptures back for one scoring round only when a finding names a"
     " first-viewport wholesale failure or a Floor gate; scoring is not a second"
     " review. Record the outcome in the stamp, hero first: `hero-review: findings"
     " \u00b7 4 findings \u00b7 4 resolved`, then `finish-review: subagent \u00b7 5"
     " findings \u00b7 4 resolved 1 unresolved \u00b7 gap: none`."),
    # Sweep M2 review-finish.md:5 first word reworded.
    ("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
     "First line: one of `recapture` (a screenshot is missing, blank or shows the"
     " wrong thing; list what to recapture and stop), `rebuild` (the first viewport"
     " fails the idea or the theme wholesale), `fix` (findings follow), `ship`"
     " (nothing owed). The first word rests on the gates, the plain defects, the"
     " copy, and the layout \u2014 template observations (`Seen before`, machine-made)"
     " are candidate evidence for `browser-qa` and never drive it.",
     "First line: one of `recapture` (a screenshot is missing, blank or shows the"
     " wrong thing; list what to recapture and stop), `findings` (craft findings"
     " follow \u2014 a first viewport that fails the idea or the theme wholesale is"
     " named explicitly among them), `no-findings` (nothing owed). The first word"
     " is a craft status, not a ship/fix/rebuild verdict \u2014 it rests on the gates,"
     " the plain defects, the copy, and the layout; template observations (`Seen"
     " before`, machine-made) are candidate evidence for `browser-qa` and never"
     " drive it."),
    # Sweep M3 review-hero.md:5 first word reworded.
    ("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
     "First line: `ship` or `fix`. The word rests on the craft questions below"
     " (headline, composition, visual, signature, type) \u2014 template observations"
     " are candidate evidence for `browser-qa` and never drive it.",
     "First line: `findings` or `no-findings`. The word is a craft status, not a"
     " ship/fix verdict \u2014 it rests on the craft questions below (headline,"
     " composition, visual, signature, type); template observations are candidate"
     " evidence for `browser-qa` and never drive it."),
    # Sweep M3 consumer, Taste :314 hero first word.
    ("new-skills/design-taste-frontend/SKILL.md",
     "Act on its first word (`ship` / `fix`) for the craft findings; findings"
     " join the fix batch",
     "Act on its first word (`no-findings` / `findings`) for the craft findings;"
     " findings join the fix batch"),
]

# --- Build-patch anchors: (built rel path, old) — preflight only ------------
# These must exist count==1 in the CURRENT built tree before any write. The
# actual edits live in fix13i/build-patch-i.txt (same old->new pairs).
PATCH_ANCHORS = [
    ("skills/orch-build-mvp/SKILL.md", SNAP_INTRO_OLD),
    ("skills/orch-build-mvp/SKILL.md", SNAP_RULE_OLD),
    ("skills/orch-build-mvp/SKILL.md", COVERAGE_OLD),
    ("skills/orch-build-mvp/SKILL.md", REVERT1_OLD),
    ("skills/orch-build-mvp/SKILL.md", REVERT2_OLD),
    ("skills/orch-build-mvp/SKILL.md", REVERT3_OLD),
    ("skills/orch-build-mvp/SKILL.md", COUNTER_OLD),
    ("skills/orch-build-mvp/SKILL.md",
     "after the run, the orchestrator records `fresh-verdict rounds used: N/2` in"
     " `.hackathon/run-ledger.md` \u2014 see the round definition in 6b \u2014 and"
     " consults that line before spending more"),
    ("skills/orch-build-mvp/SKILL.md",
     "Act on its first word (`recapture` / `rebuild` / `fix` / `ship`) for its"
     " gates, plain defects, copy, and layout findings, which join the fix batch"
     " (same capped 2-round fix loop)"),
]


def fail(msg):
    print(f"PREFLIGHT FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    # Phase 1 — preflight: every staged old-string exists exactly once in the
    # staged file AND in the built file (staged == built for these files,
    # except Taste SKILL.md frontmatter — its edited line is shared, so the
    # built check still applies).
    for rel, old, _new in STAGED:
        staged_path = os.path.join(PLUGIN_ROOT, rel)
        # Map staged path to built path.
        if rel.startswith("new-skills/"):
            built_rel = "skills/" + rel[len("new-skills/"):]
        elif rel.startswith("round2-skills/"):
            built_rel = "skills/" + rel[len("round2-skills/"):]
        else:
            built_rel = rel
        built_path = os.path.join(BUILT, built_rel)
        for label, path in (("staged", staged_path), ("built", built_path)):
            t = open(path).read()
            n = t.count(old)
            if n != 1:
                fail(f"{label} {rel}: anchor count={n} (want 1): {old[:80]!r}")
    # Phase 1b — preflight of build-patch anchors against the built tree.
    for rel, old in PATCH_ANCHORS:
        t = open(os.path.join(BUILT, rel)).read()
        n = t.count(old)
        if n != 1:
            fail(f"build-patch anchor {rel}: count={n} (want 1): {old[:80]!r}")
    print(f"Preflight OK: {len(STAGED)} staged subs + {len(PATCH_ANCHORS)}"
          " build-patch anchors, all count==1. Writing staged edits.")
    # Phase 2 — write staged edits.
    for rel, old, new in STAGED:
        p = os.path.join(PLUGIN_ROOT, rel)
        t = open(p).read()
        assert t.count(old) == 1, f"staged {rel}: anchor drifted: {old[:60]!r}"
        open(p, "w").write(t.replace(old, new))
    print(f"Wrote {len(STAGED)} staged subs.")


if __name__ == "__main__":
    main()
