# Sweep #33 fixes — Fix #25 (sweep-fix worker)

Both Sweep #33 MINOR findings fixed in staged sources, then rebuilt.
No audit/sweep/dry-run/verify run (re-sweep worker owns verification).
No `build.sh` line edited, no verifier edited, no pitch-deck-video
template file touched, no design-inventory.md touched.
`fix11/fix11-stage.py` never run.

## MINOR 1 — REASON_F25 "step-2 reviewer" claim had no backing check

**Side fixed: added the backing check** (the :149 claim was left as
written). Reason: the claim names two real checkers; the 5a static
check existed, the reviewer check did not. Adding the check makes the
claim true and keeps the reviewer in the enforcement SPEC §4(f) wants,
instead of weakening the claim to a single checker.

**Frozen-text check (done BEFORE editing):**
- The Verify step 2 sentence I would have edited is the frozen
  `D19_REVIEWER` text: `fix19/fix19.py:124` defines it, and
  `fix19/verify19.py:191-192` asserts it verbatim (`D19_REVIEWER in
  orch`). It is the sentence "The reviewer also checks each UI
  decision's recorded reason covers all six fix #19 D19 dimensions …
  is a finding, minor at least."
- No verifier asserts the :149 REASON_F25 paragraph itself, nor the
  "The reviewer does NOT judge the built screens" sentence, nor the
  trap-table row (checked fix19–fix24 verifiers + fix25/fix25.py).
- Fix chosen: APPEND a new sentence immediately AFTER the frozen
  `D19_REVIEWER` sentence, leaving it byte-identical. Verified after
  the edit (Python substring check, staged AND built):
  `D19_REVIEWER`, `D19_RULE`, `D19_ROUTING` all still present
  byte-identical.

**File:** `new-skills/orchestrate/SKILL.md:266` (Verify step 2,
Design-direction record check paragraph)

**Old text** (end of the frozen sentence → next sentence):
> …a missing dimension, or a reason covering only layout/structure, is a finding, minor at least. The reviewer does NOT judge the built screens…

**New text** (one sentence inserted between them):
> …a missing dimension, or a reason covering only layout/structure, is a finding, minor at least. The reviewer also checks the three-part reasoning block — INFERRED / CHOSEN / REJECTED (REASON_F25) — on the decision-record entries presented in the diff; an entry missing any of the three lines is a finding, minor at least. The reviewer does NOT judge the built screens…

Scoping note: the sentence says "on the decision-record entries
presented in the diff", matching the dispatch template's mechanism
(`dispatch-prompt.md`: the direction/record is "present in the diff")
and the existing D19 check's shape — a presence check, never a
quality verdict, per :149. Whole-record coverage stays the 5a static
check's job (:96).

**Claim/check agreement now:** :149 "checked by the step-2 reviewer
and the step-5a static check" — reviewer check now exists (:266),
5a check already existed (:96). REASON_F25 occurrences in orchestrate:
4 → 5 (staged and built).

**Observation for the re-sweep (not changed, out of the one-line
scope):** `new-skills/orchestrate/references/dispatch-prompt.md`'s
`[UI diff:]` reviewer block mirrors the design-direction check but
does not name the three-part block. The SKILL.md instruction is the
authority; the template is the dispatched prompt. Re-sweep to decide
whether the template needs the matching line. Also: no verify25.py
exists yet, so no verifier asserts the new sentence — the verify
worker owns that.

## MINOR 2 — Scope-trap "Edge case obsession" row vs TECHDEPTH_F25

**File:** `rewritten-skills/hackathon-scope/SKILL.md:90` (scope-traps
table)

**Old text:**
> | **Edge case obsession** | "What if the user enters X" | Demo doesn't enter X |

**New text:**
> | **Edge case obsession** | "What if the user enters X" | Demo doesn't enter X — that is a cut, not a handling: record what was cut and why in the cut list (TECHDEPTH_F25) |

The row now defers to TECHDEPTH_F25 by name, matching the
TECHDEPTH_F25 section in the same file (:65: "'Demo doesn't enter X'
is not a handling; it is a cut, and it goes in the cut list below
with its reason"). The trap table is upstream-verbatim text, so only
the antidote cell was qualified — no other cell touched.
TECHDEPTH_F25 occurrences in hackathon-scope: 2 → 3 (staged and
built). "Demo doesn't enter X" now occurs 2× in the file (trap row +
TECHDEPTH section), both consistent.

## Rebuild (run 3)

- Command: `bash build.sh` from `~/workspace/hackathon-plugin`,
  log `fix25/build-log-run3.txt` (1,105 lines). **Exit 0.**
- `build.sh`: **24,079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae** —
  unchanged by the build. Diff vs `build.sh.before-fix23`: **+305/−0**
  (additions only, intact).
- fix16 (from the run-3 log): **ERRORS: 0, NOTES: 38, CHANGES: 649,
  REMOVALS: 88. TOTAL BANNED-TERM HITS: 0.**
- fix25 patch: **14 change(s), "fix25: OK"**. Counts: skills 166,
  commands 87, hooks 15; plugin.json hackathon-ecc 1.0.0.

## Built-tree confirmation (read from `hackathon-ecc/`, run 3)

- `skills/orchestrate/SKILL.md:266` carries the new reviewer
  sentence; `:149` carries the claim unchanged; frozen
  `D19_REVIEWER` / `D19_RULE` / `D19_ROUTING` all present
  byte-identical (Python substring check on the built file).
- `skills/hackathon-scope/SKILL.md:90` carries the qualified trap
  row; TECHDEPTH_F25 ×3 in the built file.
- Staged-vs-built: hackathon-scope is byte-identical. Orchestrate
  differs on exactly 3 lines (:96, :261, :268) — the pre-existing
  build-time agent-link expansion (bare `` `code-reviewer` `` →
  `` `code-reviewer` agent (`agents/ecc-code-reviewer.md`) ``),
  present in the run-2 built tree as well (sweep §6 anchors 7–10);
  not caused by this fix. The two edited lines (:149, :266) are
  identical staged vs built.
