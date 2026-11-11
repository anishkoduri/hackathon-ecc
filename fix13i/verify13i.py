#!/usr/bin/env python3
"""verify13i.py — present/gone checks for fix #13i against the BUILT tree."""
import os
import sys

BUILT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "hackathon-ecc")
fails = []
n_checks = 0


def check(rel, s, want, label):
    global n_checks
    n_checks += 1
    t = open(os.path.join(BUILT, rel)).read()
    n = t.count(s)
    if n != want:
        fails.append(f"{label}: {rel}: {s[:70]!r} count={n} want={want}")
        print(f"FAIL {label}: {rel}: {s[:70]!r} count={n} want={want}")
    else:
        print(f"ok   {label}: {rel}: {s[:60]!r} x{n}")


ORCH = "skills/orchestrate/SKILL.md"
MVP = "skills/orch-build-mvp/SKILL.md"
POLISH = "skills/polish-pass/reference/polish.md"
GATES = "skills/design-taste-frontend/references/hallmark/references/gates.md"
RFIN = "skills/design-taste-frontend/references/hallmark/references/review-finish.md"
RHERO = "skills/design-taste-frontend/references/hallmark/references/review-hero.md"
TASTE = "skills/design-taste-frontend/SKILL.md"
PSKILL = "skills/polish-pass/SKILL.md"

# B1 — snapshot excludes live run state (both engines).
for f, tag in ((ORCH, "orch"), (MVP, "mvp")):
    check(f, "copy the WHOLE tree EXCEPT `.hackathon/` and"
             " `.hallmark/candidate-evidence.md`", 1, f"B1 {tag}: exclusion")
    check(f, "never snapshotted and never restored by a revert", 1,
          f"B1 {tag}: never snapshotted")
    check(f, "Two redesigns never share an id", 1, f"B1/M3 {tag}: uniqueness")
    check(f, "are NEVER overwritten by a revert", 1, f"B1 {tag}: revert1")
    check(f, "the round spent on the failed re-verification stays spent", 1,
          f"B1 {tag}: revert3")
    check(f, "which are never in the manifest by design and are never a"
             " coverage failure", 1, f"B1 {tag}: coverage exception")
    check(f, "when the tree has no repo, verify against the snapshot manifest"
             " alone", 1, f"M4 {tag}: no-repo fallback")
    check(f, "fresh-verdict rounds used: 0/2", 1, f"M5 {tag}: 0/2 init")
    check(f, "copy the WHOLE tree into", 0, f"B1 {tag}: old rule gone")
    check(f, "the snapshot is the whole tree, so this restores the verified"
             " state exactly", 0, f"B1 {tag}: old revert1 gone")
    check(f, "verify with `git status` plus a diff restricted", 0,
          f"M4 {tag}: old verify gone")
    check(f, "after the run, the orchestrator records `fresh-verdict rounds"
             " used: N/2`", 0, f"M7 {tag}: dup sentence gone")
# M1 orchestrate pointer.
check(ORCH, "the 5c and step-6 checks below consult the entry", 1, "M1: pointer")
check(ORCH, "the 5c/Verify-step-6 checks below", 0, "M1: old pointer gone")
# M2 Verify-step renumber.
check(ORCH, "Verify step 4a. **Any diff that touches a UI surface", 1, "M2: 4a")
check(ORCH, "**Verify step 4b. Adversarial audit", 1, "M2: 4b")
check(ORCH, "Verify step 4. **Any diff", 0, "M2: old 4 gone")
check(ORCH, "**Verify step 4. Adversarial", 0, "M2: old 4b gone")
# M7 new wording.
check(ORCH, "the round definition in 5b states the ledger update", 1, "M7: orch")
check(MVP, "the round definition in 6b states the ledger update", 1, "M7: mvp")
# Audit M1 polish.md links.
for name in ("impeccable-detector-rules.json", "impeccable-critique.md",
             "impeccable-craft-floor.md", "impeccable-onboard.md",
             "impeccable-extract.md"):
    check(POLISH, f"[{name}]({name})", 1, f"AuditM1: {name}")
    check(POLISH, f"[reference/{name}](reference/{name})", 0,
          f"AuditM1 gone: {name}")
# polish-pass SKILL.md:92 prefix must NOT have changed.
check(PSKILL, "[reference/impeccable-craft-floor.md](reference/impeccable-craft-floor.md)",
      1, "AuditM1: SKILL.md prefix intact")
# DR-M6 detector carve-out.
check(POLISH, "icon-tile-stack", 1, "M6: rule named")
check(POLISH, "never rewrite a template pattern on the detector's say-so alone",
      1, "M6: carve-out")
# Sweep M1 gates.md:68.
check(GATES, "The wireframe read is candidate evidence of a generated look,"
             " for `browser-qa` to weigh at a glance.", 1, "SweepM1: gate 68")
# Sweep M2/M3 first-word vocabulary.
check(RFIN, "First line: one of `recapture`", 1, "SweepM2: finish def")
check(RFIN, "`findings` (craft findings follow", 1, "SweepM2: findings")
check(RFIN, "`no-findings` (nothing owed)", 1, "SweepM2: no-findings")
check(RFIN, "`rebuild` (the first viewport fails", 0, "SweepM2: rebuild gone")
check(RFIN, "`fix` (findings follow), `ship` (nothing owed)", 0,
      "SweepM2: fix/ship gone")
check(RHERO, "First line: `findings` or `no-findings`", 1, "SweepM3: hero def")
check(RHERO, "First line: `ship` or `fix`", 0, "SweepM3: old def gone")
check(ORCH, "Act on its first word (`recapture` / `findings` / `no-findings`)"
            " for the gates", 1, "SweepM2: orch consumer")
check(MVP, "Act on its first word (`recapture` / `findings` / `no-findings`)"
           " for its gates", 1, "SweepM2: mvp consumer")
check(TASTE, "Act on its first word (`no-findings` / `findings`) for the craft"
             " findings", 1, "SweepM3: taste consumer")
check(GATES, "a finding names a first-viewport wholesale failure", 1,
      "SweepM2: gates scoring")
check(GATES, "`hero-review: findings \u00b7 4 findings \u00b7 4 resolved`", 1,
      "SweepM2: gates stamp")
check(GATES, "when the first word was `rebuild`", 0, "SweepM2: old scoring gone")
check(GATES, "`hero-review: fix \u00b7", 0, "SweepM2: old stamp gone")
check(ORCH, "Act on its first word (`recapture` / `rebuild` / `fix` / `ship`)",
      0, "SweepM2: old vocab orch gone")
check(MVP, "Act on its first word (`recapture` / `rebuild` / `fix` / `ship`)",
      0, "SweepM2: old vocab mvp gone")
check(TASTE, "Act on its first word (`ship` / `fix`)", 0,
      "SweepM3: old vocab taste gone")

print(f"\n{n_checks} checks, {len(fails)} failures.")
if fails:
    sys.exit(1)
print("verify13i: ALL PASS")
