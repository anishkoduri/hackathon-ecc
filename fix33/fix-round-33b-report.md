# Fix round #33b — audit #109 minor findings (all six fixed, nothing else)

**Date:** Tue Nov 17, 2026.
**Base:** fix #33 implementation + verification done; audit #109-A PASSED (2 minor findings), audit #109-B PASSED (4 minor findings), 0 blocking.
**Scope of this round:** fix all six minor findings and nothing else. Docs + one comment + one prose string only. No behavior change, no rebuild (build.sh was NOT run), no scope expansion. Nothing committed.

## 1. Finding A-M1 + B-M4 (same issue) — stale build.sh literal counts in SPEC §1(b) + implementation report §2(d)

**The issue:** both quoted build.sh as "56 ID + 5 PROSE" — those are the PRE-fix33 numbers, presented without a pre-fix33 label in a keep-list table that otherwise describes the current tree.

**Independent measurement (this round, before editing):** `grep -o` occurrence counts on `scratch-repo/build.sh`, plus `git show dd106ade:build.sh` for the pre-fix33 baseline:

| Pattern | Pre-fix33 (HEAD dd106ade) | Post-fix33 (measured) | Auditors' numbers |
|---|---|---|---|
| `grok-4.7-high` (ID) | 56 | **48** | 48 — agrees |
| `Grok 4.7 High` (PROSE) | 5 | **6** | 6 — agrees |
| `grok-4.7-extra-high` (XID) | 1 | **1** | 1 — agrees |
| `Grok 4.7 Extra High` (XPROSE) | 0 | **0** | 0 — agrees |

Occurrence counts, not line counts: ID on 44 lines, PROSE on 4 lines, 3 lines carry both (build.sh:22208, :22687, :24139) — 45 lines total. My measurement agrees with both auditors; no STOP was needed.

**Full reconciliation (from `git diff dd106ade -- build.sh`, this round):** ID −10 removed / +2 added = −8 net. Removed: 6 STEP-5 audit2_patch anchor lines (D33-15) + 2 opus mapping (dict entry + comment) + old fix30 header comment (1) + old inline-keep comment (1). Added: fix30-retirement comment block (1) + fix33 comment block :24139 (1). PROSE +1 (fix33 comment block :24139). XID net 0 (old fix30 header 1 → new retirement block 1). Note: the auditors' shorthand "56−8=48" is the net figure; the full ± accounting above is what the diff actually shows, and it is the reconciliation now recorded in the SPEC.

**Changes:**
- `fix33/SPEC.md:44` (§1(b) keep-list table) — "56 ID + 5 PROSE occurrences (52 lines) + 1 XID" → "48 ID + 6 PROSE occurrences (45 lines) + 1 XID", with the measured post-fix33 label and the full reconciliation.
- `fix33/fix33-implementation-report.md:64` (§2(d) keep-list table) — same count correction, noted as measured post-fix33 with the 56/5 figures labeled pre-fix33.

## 2. Finding A-M2 — stale fast count in the build.sh fix33 comment block

**The issue:** the comment said fix33.py "asserts the fast-worker pin unchanged (70)". Measured fast counts are 71 pre-state / 72 post-state (fix33.py EXPECT FAST_ID 71, post-assertion EXPECT+1 = 72; patch log pre-state fast x71, post-state x72 — D33-16/D33-17).

**Change (COMMENT ONLY, `scratch-repo/build.sh:24145–24148`):**
- Old: `asserts the fast-worker pin unchanged (70), / the GLOBAL-ROUTING + DESIGNPKG-AUTO blocks untouched, and MODELSEL_F33`
- New: `asserts the fast-worker pin unchanged (71 / pre-state, 72 post-state — +1 in the agent.schema.json description, / D33-17), the GLOBAL-ROUTING + DESIGNPKG-AUTO blocks untouched, and / MODELSEL_F33 present.`

The reflow added one line; the comment text otherwise unchanged (MODELSEL_F33 kept — verified present by grep after the edit). No functional line touched; build.sh was NOT run. Post-edit build.sh census re-checked: ID 48 / PROSE 6 / XID 1 — unchanged, so the comment edit introduced no pin text.

## 3. Finding B-M1 — direct-command entry points carry no Auto ask (recorded as OWED, NOT fixed by expanding scope)

**The issue:** `/gan-build`, `/gan-design`, `/astra-review`, and the `/orch-*` pipelines carry no MODEL check and no Auto ask — `MODELSEL_F33` exists only in `skills/orchestrate/SKILL.md`. The stated rule ("the orchestrator tells the user to pick a specific model before proceeding") is unconditional in wording while enforcement is orchestrate-only.

**Why OWED, not a defect:** by deliberate design (D33-19, orchestrate-only home); the primary cold start is covered (hackathon-mode first build enters orchestrate step 0, which carries the MODEL check); the scope matches the pre-fix33 MODEL-PIN check, which was also orchestrate-only — not a regression; no false identity is asserted on those paths (they all say "the model selected in this chat", true whatever Auto resolves to). No guardrail was woven into any gan/orch command in this round.

**Changes:**
- `fix33/SPEC.md:222` (§6) — new **OWED-33-4** entry (next number after OWED-33-1/2/3): what it is, why it is owed rather than a defect, and that weaving the guardrail into the direct commands belongs to a future round if ever wanted.
- `fix33/MANIFEST.md:172–176` (OWED section) — same OWED-33-4 entry, short form.

## 4. Finding B-M2 — repointed r5 scan suite crashes in place (verification-artifact note)

**The issue:** `scan32-r5-test-fix33.py` opens `fix32.py` (line 849) and `fix32-patch-log.md` relative to its own directory, but neither file exists in `fix33/` — an in-place run crashes with `FileNotFoundError`. It passes 100/100 only with those two files copied alongside. The test was NOT rewritten.

**Verification (this round):** copied `scan32-r5-test-fix33.py` + `scratch-repo/fix32/fix32.py` + `scratch-repo/fix32/fix32-patch-log.md` to a probe dir (`/tmp/fix33b-r5/`, deleted after) and ran it there — **100 PASS, RESULT: ALL PASS, exit 0**. BASE is a hardcoded absolute path to the scratch-repo built tree, so the run scored the real tree. (r4 re-runs in place — see §7.)

**Change:**
- `fix33/MANIFEST.md:131–137` (Verification section) — note stating the exact requirement: r5 runs 100/100 only with `fix32.py` + `fix32-patch-log.md` adjacent to the script; an in-place run from fix33/ crashes with `FileNotFoundError`. No SPEC note: the SPEC does not document verification runs, so there was nothing to annotate there.

## 5. Finding B-M3 — stale DECISION-33-5 string in fix33.py (and patch logs)

**The issue:** fix33.py's DECISION-33-5 string still said "hackathon-mode L42 carries the pointer" — the exact claim D33-19 corrected (the pointer was never woven; guardrail home is orchestrate-only). The string appeared once each in `fix33.py`, `fix33/fix33-patch-log.md`, and `scratch-repo/fix33/fix33-patch-log.md`, contradicting DECISION-33-19 in the same file.

**Changes:**
- `fix33/fix33.py:449` AND `scratch-repo/fix33/fix33.py:449` (both copies, kept md5-identical — see below) — "hackathon-mode L42 carries the pointer." → "hackathon-mode L42 carries no pointer (D33-19: the pointer was never woven — the guardrail home is orchestrate-only)." Future patch-log output is now right.
- `fix33/MANIFEST.md:138–145` (Verification section) — note that the run-5/run-6 patch-log copies (fix33/ and scratch-repo/fix33/, md5-identical `ddef5b7aa229ceff138d3cf3e450960c`) carry the stale D33-5 wording as a historical record, superseded by D33-19. The existing patch logs were NOT rewritten.

**Sync check:** both fix33.py copies md5-identical after the edit (`1533f4e8f56f3ab9a200f6a4d894014a`). No remaining "carries the pointer" in any live file — only the two historical patch logs and the MANIFEST note that explains them.

## 6. Audit #109-A observation — canonical fix31.py edit (investigation)

**The question:** the implementation worker updated canonical `~/workspace/hackathon-plugin/fix31/fix31.py` outside the scratch repo (md5-identical to the scratch copy). Was that legitimate, or unintentional/unneeded?

**Findings:**
- Scratch-repo change vs HEAD (`git diff dd106ade -- fix31/fix31.py`): ONLY the `EXPECT_PIN` census update (`{OLD_ID: 0, OLD_PROSE: 0, FAST_ID: 70, NEW_ID: 49, NEW_PROSE: 22}` → `{OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}`) plus the comment explaining it. This is a **legitimate, required fix33 change**: fix31.py runs after fix33.py in the build and asserts the pin census — with fix30 retired and the tree unpinned, the old EXPECT_PIN would fail loudly on the post-unpin tree (build runs 2–3 proved the census must follow the unpin).
- Canonical copy: md5-identical to the scratch copy (`cae364c594befc6a303ecd0ceed3d447`); the pre-fix33 canonical state equals the HEAD version (`241e6bcd7804e2e45ab517b3af462cba`). So the canonical edit mirrors the legitimate scratch-repo change exactly.
- **Outcome: LEFT AS-IS, reason recorded.** The canonical copy was synced to stay md5-identical to the scratch copy. The canonical tree is the stale pre-commit snapshot the fix33 bundle install will replace, and builds never run from it — so the consequence audit #109-A noted (canonical fix31.py would fail a build run from the canonical tree against its still-pinned tree) is expected pre-commit state, not a defect. No revert. The scratch-repo fix31.py was not touched.
- Same pattern noted for canonical fix32.py (md5-identical to scratch, `2cc17cec8120209b3142417693cdac43`) — likewise left as-is. The canonical `fix30/live-test-prompt.md` update was instructed and is legitimate — left untouched, per the brief.

**Change:**
- `fix33/MANIFEST.md:41–52` ("What changed" fix31.py bullet) — NOTE recording the investigation outcome and the reason the canonical edit stays.

## 7. Re-runs after all edits (nothing broke)

| Check | Command | Result |
|---|---|---|
| Verifier | `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` | **526/526 checks pass, exit 0** |
| Scan r4 | `cd fix33 && python3 scan32-r4-test-fix33.py` | **ALL PASS, 76 checks, exit 0** (re-runs in place) |
| Scan r5 | probe dir with `fix32.py` + `fix32-patch-log.md` alongside (see §4) | **ALL PASS, 100 checks, exit 0** |

The verifier re-run covers the build.sh comment edit (A-M2) and the fix33.py string edit (B-M3): both pass 526/526, proving no check depends on the old comment text or the old DECISION-33-5 string. build.sh was NOT run (no rebuild — a comment cannot change build output).

## 8. Diff stat — before / after

Before this round (audit #109 state): **33 files changed, +135/−109**, HEAD `dd106ade`.
After this round: **33 files changed, +136/−109**.

The only tracked-file change in this round is `build.sh` (+1 insertion line from the comment reflow, 57 → 58 changed lines). No other tracked file changed; no new file entered the diff; `git status` still shows only the 33 modified files plus untracked `fix32/` and `fix33/` dirs. The fix33.py edit lives in the untracked `fix33/` dirs (fix dir + scratch-repo mirror), and the SPEC/MANIFEST/implementation-report edits live in the untracked fix dir — none of them touch the tracked diff. Nothing committed.

## 9. Files changed in this round (complete list)

- `fix33/SPEC.md` — §1(b) counts (line 44), OWED-33-4 (line 222).
- `fix33/fix33-implementation-report.md` — §2(d) counts (line 64).
- `fix33/scratch-repo/build.sh` — fix33 comment block (lines 24145–24148), comment only.
- `fix33/fix33.py` + `fix33/scratch-repo/fix33/fix33.py` — DECISION-33-5 string (line 449, both copies, md5-identical).
- `fix33/MANIFEST.md` — OWED-33-4 (lines 172–176), B-M2 note (lines 131–137), B-M3 patch-log note (lines 138–145), canonical-fix31 investigation note (lines 41–52).
- This report: `fix33/fix-round-33b-report.md`, copied to `scratch-repo/fix33/fix-round-33b-report.md` (md5-identical).

Deliberately NOT touched: drones, fast tier, fix31/fix32 bundles, factory round3 bundle, the historical patch logs, any gan/orch command, the canonical tree (except the already-recorded fix31.py state, which was investigated and left as-is).
