#!/usr/bin/env python3
"""Verify fix #13h in the BUILT plugin tree (post-rebuild present/gone checks)."""
import os
import sys

BUILT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hackathon-ecc")

# (relative path, substring, expected count, label)
CHECKS = []
def present(rel, s, n, label):
    CHECKS.append((rel, s, n, label))
def gone(rel, s, label):
    CHECKS.append((rel, s, 0, label))

O = "skills/orchestrate/SKILL.md"
M = "skills/orch-build-mvp/SKILL.md"
GB = "commands/gan-build.md"
GD = "commands/gan-design.md"
GT = "skills/design-taste-frontend/references/hallmark/references/gates.md"
ICF = "skills/polish-pass/reference/impeccable-craft-floor.md"
PM = "skills/polish-pass/reference/polish.md"
PS = "skills/polish-pass/SKILL.md"
T = "skills/design-taste-frontend/SKILL.md"
CR = "skills/polish-pass/reference/impeccable-critique.md"
UX = "skills/ui-ux-pro-max/SKILL.md"

# B1
present(O, "If the Hallmark audit produces no candidate evidence (no Specificity under 3, no template observations), no fresh round is spent — record that in the ledger (rounds used unchanged).", 1, "B1 orchestrate guard present")
# B2 both engines
for f, tag in [(O, "orchestrate"), (M, "standalone")]:
    present(f, "SNAPSHOTS the whole tree", 1, f"B2 {tag}: whole-tree snapshot intro")
    present(f, "copy the WHOLE tree into", 1, f"B2 {tag}: whole-tree copy")
    present(f, "per-file hashes", 2, f"B2 {tag}: hashes recorded (intro + rule)")
    present(f, "snapshot-integrity failure", 1, f"B2 {tag}: manifest integrity failure")
    present(f, "delete every file the redesign created that the snapshot does not contain", 1, f"B2 {tag}: created files deleted on revert")
    present(f, "never from version control alone", 1, f"B2 {tag}: never git alone")
    present(f, "diff restricted to snapshot-listed paths", 1, f"B2 {tag}: verify diff restricted")
    gone(f, "copy every file the redesign will touch", f"B2 {tag}: brief-enumerated snapshot gone")
    gone(f, "git checkout -- <file>", f"B2 {tag}: git-checkout restore gone")
    gone(f, "diff the tree against the snapshot directory", f"B2 {tag}: unimplementable diff gone")
    # M1 / M2
    gone(f, "memory.;", f"M1 {tag}: typo gone")
    present(f, "working-context memory; the redesign decision", 1, f"M1 {tag}: fixed sentence")
    gone(f, "(see the round definition above) and consults that line before spending more.", f"M2 {tag}: dup ledger sentence gone")
    # M9
    present(f, "`re-verification <redesign-id>: PASSED`", 2 if f == O else 3, f"M9 {tag}: PASSED keyed")
    present(f, "`re-verification <redesign-id>: BLOCKED`", 6 if f == O else 7, f"M9 {tag}: BLOCKED keyed")
    gone(f, "`re-verification: PASSED`", f"M9 {tag}: plain PASSED gone")
    gone(f, "`re-verification: BLOCKED`", f"M9 {tag}: plain BLOCKED gone")
    # M7 / M8
    present(f, "passing `.hallmark/hero-review.md` to the fresh-verdict run as an input file (via `.hallmark/candidate-evidence.md`)", 1, f"M7a {tag}: hero-review to fresh run")
    gone(f, "to the browser-qa visual loop as an input file", f"M7a {tag}: visual-loop routing gone")
    present(f, "the page's HTML or component source", 1, f"M7b {tag}: HTML source in finish-review inputs")
    present(f, "Resolved in visual loop — do not re-judge", 2, f"M8 {tag}: resolved-marking present")
# M3 orchestrate only
present(O, "**Verify step 5. Visual iteration loop", 1, "M3 orchestrate: Verify step 5 header")
present(O, "**Verify step 6. Hallmark audit", 1, "M3 orchestrate: Verify step 6 header")
present(O, "Verify step 1. **Cheaply verifiable**", 1, "M3 orchestrate: Verify step 1 header")
present(O, "Verify step 2. **Not cheaply verifiable**", 1, "M3 orchestrate: Verify step 2 header")
present(O, "Verify step 3. **Large", 1, "M3 orchestrate: Verify step 3 header")
present(O, "Verify step 4. **Any diff that touches a UI surface", 1, "M3 orchestrate: Verify step 4 (UI) header")
present(O, "**Verify step 4. Adversarial audit", 1, "M3 orchestrate: Verify step 4 (audit) header")
present(O, "2 rounds total across 5b and Verify step 6", 2, "M3 orchestrate: budget refs renamed")
present(O, "browser-qa's Verify-step-5 captures", 1, "M3 orchestrate: captures renamed")
present(O, "the Verify-step-5 visual loop", 3, "M3 orchestrate: visual-loop refs renamed (x3)")
present(O, "this app-screen audit IS the Verify-step-6 design audit", 1, "M3 orchestrate: design-audit renamed")
gone(O, ", step-6 finish-review template observations", "M3 orchestrate: old step-6 ref gone")
gone(O, "browser-qa's step-5 captures", "M3 orchestrate: old step-5 ref gone")
present(O, "6. **Commit, README, then final report**", 1, "M3 orchestrate: own step 6 untouched")
present(O, "the step-6 README/final report", 1, "M3 orchestrate: own step-6 ref untouched")
present(O, "per orchestrate step 5 above", 1, "M3 orchestrate: own step-5 ref untouched")
# M5
present(O, "The hold blocks only the redesign: deploy the reverted verified tree and record its URL and deploy path", 1, "M5 orchestrate: deploy reverted tree")
# M6 standalone
present(M, "run sloplint on the landing page before the Hallmark landing audit", 1, "M6 standalone: sloplint ordering unambiguous")
gone(M, "first run sloplint on the landing page", "M6 standalone: confusing 'first' gone")
# B3 gan-build / gan-design
present(GB, "read `docs/decision-record.md` FIRST", 1, "B3 gan-build: record read first")
present(GB, "if neither the record nor the tokens file carries a direction", 1, "B3 gan-build: cold start only when neither carries one")
present(GB, "Precedence on divergence: the decision record wins over `gan-harness/spec.md`", 1, "B3 gan-build: precedence rule")
present(GB, "Read spec.md and `docs/design-tokens.md`", 1, "B3 gan-build: generator reads tokens file")
present(GB, "step 0 reads the decision record first and adopts its direction when one exists", 1, "B3 gan-build: skip-planner path reads record")
present(GB, "from `docs/decision-record.md` when the record carries one, else from the design-lead", 1, "B3 gan-build: step 1 record-first")
present(GD, "read `docs/decision-record.md` FIRST", 1, "B3 gan-design: record read first")
present(GD, "Precedence on divergence: the decision record wins over the spec", 1, "B3 gan-design: precedence rule")
present(GD, "the brief RESTATES the design direction from `docs/decision-record.md` when the record carries one", 1, "B3 gan-design: intro record-first")
# M4 gates
present(GT, "The 'Step 6' (hero review) and 'Step 7' (finish review) numbers in §6 are the upstream Hallmark build/review walk's own numbering, not steps in this plugin.", 1, "M4 gates: §6 numbers named")
# B4
present(ICF, "except the two page-level template patterns below (same-size cards as the page structure; the hero-metric template), which are candidate evidence for `browser-qa`, never a rewrite on this check alone", 1, "B4 craft floor :30 exception")
present(ICF, "As a page-level template pattern this is candidate evidence for `browser-qa`", 2, "B4 craft floor :34/:35 routed")
present(PM, "its bans are absolute as static/code-level checks", 1, "B4 polish.md gloss corrected")
gone(PM, "its bans are absolute; where the two floors disagree", "B4 polish.md old gloss gone")
present(PS, "its bans are absolute as static/code-level checks", 1, "B4 polish-pass SKILL gloss corrected")
gone(PS, "its bans are absolute (a pinned brief never overrides a ban); where the two floors disagree", "B4 polish-pass SKILL old gloss gone")
present(T, "its bans are absolute as static/code-level checks", 1, "B4 Taste gloss corrected")
present(T, "and except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite on this check alone", 1, "B4 Taste template exception")
present(T, "Hallmark gate 2b's guarded single-hue gradient-text ramp is permitted", 1, "B4 Taste gate-2b exception preserved")
present(UX, "its bans are absolute as static/code-level checks", 1, "B4 ui-ux-pro-max carve-out intact (untouched)")
# M10 critique
present(CR, "Minor polish only; informs candidate evidence, never a ship verdict", 1, "M10 critique Excellent reworded")
present(CR, "Major UX issues; core experience broken — record as candidate evidence for `browser-qa`", 1, "M10 critique Poor reworded")
present(CR, "Redesign indicated, not decided; unusable in current state — record as candidate evidence for `browser-qa`", 1, "M10 critique Critical reworded")
present(CR, "The bands inform candidate evidence for `browser-qa`; only `browser-qa`'s verdict establishes a finding.", 1, "M10 critique bands framed as evidence")
gone(CR, "Minor polish only; ship it", "M10 critique ship-it gone")
gone(CR, "Redesign needed; unusable in current state", "M10 critique redesign-needed gone")
gone(CR, "Major UX overhaul required", "M10 critique overhaul-required gone")
# M11
present(PM, "Record per-screen consistency (consistent / diverges, with the tokens cited) for the report.", 1, "M11 polish.md Step 7 record")
present(PM, "<consistent / diverges (tokens cited)>", 1, "M11 polish.md table")
gone(PM, "Record per-screen pass/fail for the report.", "M11 polish.md old record gone")
gone(PM, "<pass/fail on consistency only>", "M11 polish.md old table cell gone")
present(PS, "record per-screen consistency (consistent / diverges, with the tokens cited)", 2, "M11 polish-pass SKILL records (harmony + :96)")
gone(PS, "record per-screen pass/fail", "M11 polish-pass SKILL old records gone")
present(PS, "pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY", 1, "M11 polish-pass SKILL distinctiveness-bar sentence untouched")
present(PM, "pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY", 1, "M11 polish.md distinctiveness-bar sentence untouched")

def main():
    failures = []
    for rel, s, want, label in CHECKS:
        txt = open(os.path.join(BUILT, rel), encoding="utf-8").read()
        n = txt.count(s)
        if n != want:
            failures.append(f"{label}: count={n} want={want} :: {s[:60]!r}")
    if failures:
        print(f"VERIFY FAILED ({len(failures)} of {len(CHECKS)}):")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print(f"VERIFY OK: all {len(CHECKS)} built-tree checks passed.")


if __name__ == "__main__":
    main()
