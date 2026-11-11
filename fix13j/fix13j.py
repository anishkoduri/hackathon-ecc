#!/usr/bin/env python3
"""Fix round #13j — staged-source edits + preflight of the build patch.

Scope (1 minor, parent-verified in the built tree):
- Dry-run M1: snapshot manifest location contradicts the 20-line ledger cap.
  Orchestrate :8 caps the stage ledger at "20 lines max" with bulky loads
  overflowing to `docs/run-ledger-appendix.md` (one line per item) with a
  one-line pointer in the ledger. But the snapshot rule (orchestrate :60,
  standalone :53) records "the snapshot path + the full file list +
  per-file hashes in `.hackathon/run-ledger.md`" — a whole-tree list is
  dozens to hundreds of lines, so the two rules cannot both be followed
  literally. And revert step (2)'s "verify against the snapshot manifest
  alone" names no file if the orchestrator overflows it to the appendix.
  Fix (BOTH engines): the snapshot manifest (snapshot path + full file list
  + per-file hashes, one line per file) lives in `docs/run-ledger-appendix.md`
  under a `<redesign-id>` heading, with a one-line pointer in
  `.hackathon/run-ledger.md` (snapshot path + appendix file + line count);
  revert step (2) and the coverage check NAME the manifest's file.
  Standalone has 0 mentions of `run-ledger-appendix` and no ledger cap, so
  the snapshot rule defines the appendix inline (self-contained wording,
  identical in both engines) — no standalone-wide cap rule is invented.
  The 20-line ledger cap stays intact; per-redesign-id entries and the
  `fresh-verdict rounds used: N/2` line stay in the ledger itself (single
  lines, not bulky loads).

Staged source edited here (verified staged == built by diff):
- new-skills/orchestrate/SKILL.md (all 5 subs)

ECC-base file (no staged source) is NOT edited here. Its edits live in
fix13j/build-patch-j.txt: a build.sh patch block in the fix13i format
(python heredoc, subs + count==1 asserts), to be inserted LAST, just before
STEP 5 (after the fix13i block). File it covers:
skills/orch-build-mvp/SKILL.md (all 5 subs).

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
    " the end of this bullet \u2014 copy the whole tree, except `.hackathon/`"
    " and `.hallmark/candidate-evidence.md`, to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list +"
    " per-file hashes in `.hackathon/run-ledger.md`, BEFORE any redesign file"
    " is overwritten)"
)
SNAP_INTRO_NEW = (
    "the orchestrator first SNAPSHOTS the whole tree (see the snapshot rule at"
    " the end of this bullet \u2014 copy the whole tree, except `.hackathon/`"
    " and `.hallmark/candidate-evidence.md`, to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the snapshot"
    " manifest \u2014 the file list + per-file hashes \u2014 in"
    " `docs/run-ledger-appendix.md` (one line per file: relative path + hash),"
    " with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path +"
    " appendix file + line count), BEFORE any redesign file is overwritten)"
)
SNAP_RULE_OLD = (
    "record the snapshot path + the full file list (excluding those two paths)"
    " + per-file hashes in `.hackathon/run-ledger.md`."
)
SNAP_RULE_NEW = (
    "record the snapshot manifest \u2014 the snapshot path + the full file list"
    " (excluding those two paths) + per-file hashes, one line per file \u2014 in"
    " `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, and record"
    " a one-line pointer in `.hackathon/run-ledger.md` (snapshot path + appendix"
    " file + line count). The manifest lives in the appendix, never in the ledger"
    " itself: a whole-tree file list is a bulky load, and the ledger stays a short"
    " run-state file \u2014 bulky records go to the appendix (one line per item)"
    " with a one-line pointer in the ledger."
)
COVERAGE_OLD = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot manifest;"
)
COVERAGE_NEW = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot manifest in `docs/run-ledger-appendix.md` (the"
    " `<redesign-id>` section);"
)
REVERT2_IDENT_OLD = (
    "or by comparing the post-redesign tree against the snapshot manifest"
    " \u2014 then restore"
)
REVERT2_IDENT_NEW = (
    "or by comparing the post-redesign tree against the snapshot manifest in"
    " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) \u2014 then"
    " restore"
)
REVERT2_NOREPO_OLD = (
    "when the tree has no repo, verify against the snapshot manifest alone"
    " \u2014 each restored path diffed against its snapshot copy and its recorded"
    " hash \u2014 the manifest check is the fallback and the authority, `git"
    " status` is only a convenience."
)
REVERT2_NOREPO_NEW = (
    "when the tree has no repo, verify against the snapshot manifest in"
    " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) alone \u2014"
    " each restored path diffed against its snapshot copy and its recorded hash"
    " \u2014 the manifest check is the fallback and the authority, `git status`"
    " is only a convenience."
)

# --- Staged subs: (staged rel path, old, new) --------------------------------
STAGED = [
    ("new-skills/orchestrate/SKILL.md", SNAP_INTRO_OLD, SNAP_INTRO_NEW),
    ("new-skills/orchestrate/SKILL.md", SNAP_RULE_OLD, SNAP_RULE_NEW),
    ("new-skills/orchestrate/SKILL.md", COVERAGE_OLD, COVERAGE_NEW),
    ("new-skills/orchestrate/SKILL.md", REVERT2_IDENT_OLD, REVERT2_IDENT_NEW),
    ("new-skills/orchestrate/SKILL.md", REVERT2_NOREPO_OLD, REVERT2_NOREPO_NEW),
]

# --- Build-patch anchors: (built rel path, old) — preflight only ------------
# These must exist count==1 in the CURRENT built tree before any write. The
# actual edits live in fix13j/build-patch-j.txt (same old->new pairs).
PATCH_ANCHORS = [
    ("skills/orch-build-mvp/SKILL.md", SNAP_INTRO_OLD),
    ("skills/orch-build-mvp/SKILL.md", SNAP_RULE_OLD),
    ("skills/orch-build-mvp/SKILL.md", COVERAGE_OLD),
    ("skills/orch-build-mvp/SKILL.md", REVERT2_IDENT_OLD),
    ("skills/orch-build-mvp/SKILL.md", REVERT2_NOREPO_OLD),
]


def fail(msg):
    print(f"PREFLIGHT FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    # Phase 1 — preflight: every staged old-string exists exactly once in the
    # staged file AND in the built file (staged == built for orchestrate).
    for rel, old, _new in STAGED:
        staged_path = os.path.join(PLUGIN_ROOT, rel)
        built_rel = "skills/" + rel[len("new-skills/"):]
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
