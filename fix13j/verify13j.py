#!/usr/bin/env python3
"""Verify fix #13j in the BUILT tree (present/gone checks, both engines)."""
import os
import sys

BUILT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "hackathon-ecc")

PRESENT = [
    # Orchestrate :60 — intro.
    ("skills/orchestrate/SKILL.md",
     "record the snapshot manifest \u2014 the file list + per-file hashes \u2014 in"
     " `docs/run-ledger-appendix.md` (one line per file: relative path + hash),"
     " with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path +"
     " appendix file + line count)"),
    # Orchestrate :60 — snapshot rule.
    ("skills/orchestrate/SKILL.md",
     "record the snapshot manifest \u2014 the snapshot path + the full file list"
     " (excluding those two paths) + per-file hashes, one line per file \u2014 in"
     " `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, and record"
     " a one-line pointer in `.hackathon/run-ledger.md` (snapshot path + appendix"
     " file + line count). The manifest lives in the appendix, never in the ledger"
     " itself: a whole-tree file list is a bulky load, and the ledger stays a short"
     " run-state file \u2014 bulky records go to the appendix (one line per item)"
     " with a one-line pointer in the ledger."),
    # Orchestrate :60 — coverage check names the manifest file.
    ("skills/orchestrate/SKILL.md",
     "compares the design skill's changed-file list against the snapshot manifest"
     " in `docs/run-ledger-appendix.md` (the `<redesign-id>` section);"),
    # Orchestrate :60 — revert (2) identification names the manifest file.
    ("skills/orchestrate/SKILL.md",
     "or by comparing the post-redesign tree against the snapshot manifest in"
     " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) \u2014 then"
     " restore"),
    # Orchestrate :60 — revert (2) no-repo fallback names the manifest file.
    ("skills/orchestrate/SKILL.md",
     "when the tree has no repo, verify against the snapshot manifest in"
     " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) alone"),
    # Standalone :53 — intro.
    ("skills/orch-build-mvp/SKILL.md",
     "record the snapshot manifest \u2014 the file list + per-file hashes \u2014 in"
     " `docs/run-ledger-appendix.md` (one line per file: relative path + hash),"
     " with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path +"
     " appendix file + line count)"),
    # Standalone :53 — snapshot rule.
    ("skills/orch-build-mvp/SKILL.md",
     "record the snapshot manifest \u2014 the snapshot path + the full file list"
     " (excluding those two paths) + per-file hashes, one line per file \u2014 in"
     " `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, and record"
     " a one-line pointer in `.hackathon/run-ledger.md` (snapshot path + appendix"
     " file + line count). The manifest lives in the appendix, never in the ledger"
     " itself: a whole-tree file list is a bulky load, and the ledger stays a short"
     " run-state file \u2014 bulky records go to the appendix (one line per item)"
     " with a one-line pointer in the ledger."),
    # Standalone :53 — coverage check names the manifest file.
    ("skills/orch-build-mvp/SKILL.md",
     "compares the design skill's changed-file list against the snapshot manifest"
     " in `docs/run-ledger-appendix.md` (the `<redesign-id>` section);"),
    # Standalone :53 — revert (2) identification names the manifest file.
    ("skills/orch-build-mvp/SKILL.md",
     "or by comparing the post-redesign tree against the snapshot manifest in"
     " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) \u2014 then"
     " restore"),
    # Standalone :53 — revert (2) no-repo fallback names the manifest file.
    ("skills/orch-build-mvp/SKILL.md",
     "when the tree has no repo, verify against the snapshot manifest in"
     " `docs/run-ledger-appendix.md` (the `<redesign-id>` section) alone"),
    # Guardrails intact: 20-line cap still present in orchestrate :8.
    ("skills/orchestrate/SKILL.md",
     "The **stage ledger** stays a short run-state file (20 lines max)"),
    # Guardrails intact: per-id entries + budget line still in the ledger.
    ("skills/orchestrate/SKILL.md", "fresh-verdict rounds used: 0/2"),
    ("skills/orch-build-mvp/SKILL.md", "fresh-verdict rounds used: 0/2"),
]

GONE = [
    ("skills/orchestrate/SKILL.md",
     "record the file list + per-file hashes in `.hackathon/run-ledger.md`"),
    ("skills/orch-build-mvp/SKILL.md",
     "record the file list + per-file hashes in `.hackathon/run-ledger.md`"),
    ("skills/orchestrate/SKILL.md",
     "record the snapshot path + the full file list (excluding those two paths)"
     " + per-file hashes in `.hackathon/run-ledger.md`."),
    ("skills/orch-build-mvp/SKILL.md",
     "record the snapshot path + the full file list (excluding those two paths)"
     " + per-file hashes in `.hackathon/run-ledger.md`."),
    ("skills/orchestrate/SKILL.md",
     "verify against the snapshot manifest alone"),
    ("skills/orch-build-mvp/SKILL.md",
     "verify against the snapshot manifest alone"),
    ("skills/orchestrate/SKILL.md",
     "compares the design skill's changed-file list against the snapshot"
     " manifest;"),
    ("skills/orch-build-mvp/SKILL.md",
     "compares the design skill's changed-file list against the snapshot"
     " manifest;"),
    ("skills/orchestrate/SKILL.md",
     "against the snapshot manifest \u2014 then restore"),
    ("skills/orch-build-mvp/SKILL.md",
     "against the snapshot manifest \u2014 then restore"),
]


def main():
    fails = 0
    for rel, s in PRESENT:
        t = open(os.path.join(BUILT, rel)).read()
        n = t.count(s)
        if n != 1:
            print(f"FAIL present {rel}: count={n}: {s[:70]!r}")
            fails += 1
    for rel, s in GONE:
        t = open(os.path.join(BUILT, rel)).read()
        n = t.count(s)
        if n != 0:
            print(f"FAIL gone {rel}: count={n}: {s[:70]!r}")
            fails += 1
    total = len(PRESENT) + len(GONE)
    if fails:
        print(f"verify13j: {total - fails}/{total} pass, {fails} FAIL")
        sys.exit(1)
    print(f"verify13j: {total}/{total} pass")


if __name__ == "__main__":
    main()
