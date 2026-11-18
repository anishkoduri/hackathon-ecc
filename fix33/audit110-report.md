# Audit #110 — Fix #33 (unpin the orchestrator): re-audit of the fix-33b round

**Auditor:** re-auditor (single focused auditor).
**Date:** Tue Nov 17, 2026.
**Base:** `dd106ade` (fix #32 close). Scratch repo `~/workspace/hackathon-plugin/fix33/scratch-repo`.
**Audits under re-audit:** #109-A (PASS, 2 minor: A-M1, A-M2) and #109-B (PASS, 4 minor: B-M1–B-M4).
**Fix round audited:** `fix33/fix-round-33b-report.md` (read, but every claim re-verified from scratch; nothing taken on trust).
**Verdict: NOT PASS** — all six #109 minors are genuinely fixed, the verifier and both scan suites re-run green, and the tree is unchanged except for the single expected build.sh comment line. But the fix round introduced a new stale number of exactly the class it was fixing: the scratch-repo diff stat is now **+136/−109**, and two living docs still state **+135/−109** (MANIFEST.md:60, fix33-implementation-report.md:200). One trivial fix (two one-character edits) stands between this and PASS. Nothing was edited or committed by this audit.

## 1. Finding

### 110-M1 (minor, blocking under the verdict rules) — diff stat stale in two docs after the fix round's own +1 line

- **Measured now:** `git diff --stat` in `fix33/scratch-repo` = **33 files changed, 136 insertions(+), 109 deletions(-)**. HEAD `dd106ade5f6043ec4ed613919e7908172d8eadce`, confirmed.
- **Still written in two places:**
  - `fix33/MANIFEST.md:60` — "`git (scratch-repo):` 33 files changed, **+135/−109**." (in "What changed", describing the current tree)
  - `fix33/fix33-implementation-report.md:200` — "`git status` (scratch-repo): 33 files changed, **+135/−109**."
- **Cause:** the fix-33b round's build.sh comment reflow added exactly one insertion line (33 files, +135 → +136, deletions unchanged at 109). The round's own report (§8) records the new stat correctly ("After this round: 33 files changed, +136/−109"), but the round did not update these two lines.
- **Fix:** change `+135` to `+136` in both lines. No tree impact — this is docs staleness only, same class as A-M1/B-M4. Per the brief's verdict rules ("any leftover stale number = NOT PASS"), this blocks PASS even though it is trivial.

## 2. What verified clean (with numbers)

### 2.1 A-M1 + B-M4 — build.sh literal counts corrected (SPEC §1(b) + implementation report §2(d))

Independent measurement of `scratch-repo/build.sh` (post-fix33):

| Pattern | Pre-fix33 (`git show dd106ade:build.sh`) | Post-fix33 (measured) | SPEC §1(b) / report §2(d) now state |
|---|---|---|---|
| `grok-4.7-high` (ID) | 56 | **48** | 48 |
| `Grok 4.7 High` (PROSE) | 5 | **6** | 6 |
| `grok-4.7-extra-high` (XID) | 1 | **1** | 1 |
| `Grok 4.7 Extra High` (XPROSE) | 0 | **0** | 0 |

Line accounting (measured): ID on 44 lines, PROSE on 4 lines, 3 lines carry both (build.sh:22208, :22687, :24139) → 45 ID+PROSE lines; the XID sits on its own line (:24130), so the union over all four patterns is 46 lines. SPEC's "(45 lines)" is the ID+PROSE line count with the XID listed separately — coherent and accurate.
Reconciliation from `git diff dd106ade -- build.sh`: ID −10 removed / +2 added = −8 net (56→48); PROSE −0 / +1 = +1 (5→6). Removed ID: 6 STEP-5 audit2_patch anchors (D33-15) + 2 opus mapping (dict entry + comment) + old fix30 header comment (1) + old inline-keep comment (1). Added ID: fix30-retirement block (1) + fix33 comment block :24139 (1). PROSE +1 from the fix33 comment block. Matches the reconciliation now recorded in SPEC §1(b). The 56/5 figures survive only inside that reconciliation sentence, correctly labeled pre-fix33.

### 2.2 A-M2 — build.sh fix33 comment block corrected

`scratch-repo/build.sh:24145–24148` now reads "asserts the fast-worker pin unchanged (**71 pre-state, 72 post-state** — +1 in the agent.schema.json description, D33-17), the GLOBAL-ROUTING + DESIGNPKG-AUTO blocks untouched, and **MODELSEL_F33** present." No `(70)` remains anywhere in build.sh (`grep 'unchanged (70)'` empty). MODELSEL_F33 is mentioned in the comment (verified present by grep).
Comment edit changed nothing else: the full `git diff dd106ade -- build.sh` has 9 hunks — opus mapping, six STEP-5 anchor lines (one hunk each per agent pair), and the fix30-retirement/fix33-comment block — all pre-existing fix33 changes except the one-line reflow inside the fix33 comment. Post-edit build.sh census re-measured: ID 48 / PROSE 6 / XID 1 — unchanged, so the comment edit introduced no pin text. build.sh was not run (no rebuild), as the round states.

### 2.3 B-M1 — OWED-33-4 recorded, no guardrail woven into direct commands

- SPEC.md §6 carries OWED-33-4 (direct commands carry no Auto ask; orchestrate-only by deliberate design D33-19; primary cold start covered via orchestrate step 0; no regression vs the pre-fix33 MODEL-PIN check; weaving it into the direct commands belongs to a future round if ever wanted).
- MANIFEST.md OWED section carries the same OWED-33-4 entry in short form.
- `grep -rn MODELSEL` over the built direct commands (`hackathon-ecc/commands/`, `orch-build-mvp`, `orch-add-feature`, `orch-fix-defect`, `orch-change-feature`, `orch-refine-code`) = **0 hits**. The only `MODELSEL` file in the built tree is `hackathon-ecc/skills/orchestrate/SKILL.md` (2×: L14 identity, L62 MODEL check), same in staged `new-skills/orchestrate/SKILL.md`. No guardrail was woven anywhere it was not already. The stated rule remains orchestrate-only, now explicitly recorded as such.

### 2.4 B-M2 — r5 adjacency requirement recorded and reproduced both ways

- MANIFEST.md Verification section (lines ~131–137) states the requirement: r5 passes 100/100 only with `fix32.py` + `fix32-patch-log.md` adjacent to the script; an in-place run from fix33/ crashes with `FileNotFoundError`.
- Reproduced in place: `python3 scan32-r5-test-fix33.py` from `fix33/` crashes with `FileNotFoundError: .../fix33/fix32.py` (line 849 opens `fix32.py` relative to the script dir) — confirming the note is accurate.
- Reproduced with siblings: copy of the script + `scratch-repo/fix32/fix32.py` + `scratch-repo/fix32/fix32-patch-log.md` in `/tmp/audit110-r5/` → **100 PASS, RESULT: ALL PASS, exit 0** (probe dir deleted after). BASE is a hardcoded absolute path to the scratch-repo built tree, so the run scored the real tree.
- r4 re-runs in place: **76 PASS, RESULT: ALL PASS, exit 0**.

### 2.5 B-M3 — DECISION-33-5 corrected in both live fix33.py copies; patch logs untouched

- `fix33/fix33.py:449` and `scratch-repo/fix33/fix33.py:449` both now read: "hackathon-mode L42 **carries no pointer** (D33-19: the pointer was never woven — the guardrail home is orchestrate-only)."
- Both copies md5-identical: `1533f4e8f56f3ab9a200f6a4d894014a` (matches the fix-round report's stated value).
- `grep -rn 'carries the pointer'` over the live fix33.py copies: **0 hits**. The stale wording survives only in the two historical patch logs (`fix33/fix33-patch-log.md:44` and `scratch-repo/fix33/fix33-patch-log.md:44`, md5-identical `ddef5b7aa229ceff138d3cf3e450960c`) — **not rewritten**, as required — and in the MANIFEST note that explains them (Verification section, lines ~138–145: historical record, superseded by D33-19).

### 2.6 Canonical fix31.py investigation — story verified

- `git diff dd106ade -- fix31/fix31.py` (scratch repo): the ONLY change is the `EXPECT_PIN` census update (`{OLD_ID: 0, OLD_PROSE: 0, FAST_ID: 70, NEW_ID: 49, NEW_PROSE: 22}` → `{OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}`) plus the comment explaining it (fix30 retired, orchestrator unpinned, 2 OLD_PROSE are the strategic-compact keeps, FAST 72 = 71 pre-existing + 1 schema description, D33-16/D33-17). No other hunk.
- Required, not gratuitous: fix31.py runs after fix33.py in the build and asserts the census; the old EXPECT_PIN (49 NEW_ID / 22 NEW_PROSE) would fail loudly on the post-unpin tree.
- Canonical copy md5-identical to scratch: `cae364c594befc6a303ecd0ceed3d447` (both). Pre-fix33 HEAD version md5 `241e6bcd7804e2e45ab517b3af462cba`. MANIFEST "What changed" fix31.py bullet records the investigation outcome and the reason the canonical edit stays (LEFT as-is; canonical tree is the stale pre-commit snapshot; builds never run from it).

### 2.7 Verifier + scans re-run (independent)

| Check | Command | Result |
|---|---|---|
| verify33 | `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` | **526/526 checks pass, exit 0** |
| Scan r4 | `python3 scan32-r4-test-fix33.py` (from fix33/) | **ALL PASS, 76 checks, exit 0** |
| Scan r5 | copy + `fix32.py` + `fix32-patch-log.md` alongside in `/tmp/audit110-r5/` | **ALL PASS, 100 checks, exit 0** |
| Scan r5 in place | `python3 scan32-r5-test-fix33.py` (from fix33/) | **Crashes, FileNotFoundError for `fix32.py`** — expected, see §2.4 |

### 2.8 Diff stat + nothing else changed

- `git diff --stat`: **33 files changed, +136/−109**. File list is exactly the audit-#109 expected set (staged: `LIVE_SMOKE_TEST.md`, `README.md`, `build.sh`, `fix30/live-test-prompt.md`, `fix31/fix31.py`, `new-rules/hackathon-mode.mdc`, `new-skills/orchestrate/SKILL.md`, `new-skills/orchestrate/agents/deep-reasoner.md`, `new-skills/orchestrate/references/agent-TEMPLATE.md` + built `hackathon-ecc/` mirrors). `git status --short`: 33 modified + untracked `fix32/`, `fix33/` only.
- The only delta vs the audit-#109 state is the build.sh comment reflow: +136 vs +135 insertions, deletions unchanged at 109 — exactly one added line, as the fix-round report §8 states. No other tracked file changed; no new file entered the diff.

### 2.9 Unpin still holds (spot-check)

Built tree (`scratch-repo/hackathon-ecc/`): `grok-4.7-high` **x0**, `grok-4.7-extra-high` **x0**, `Grok 4.7 High` **x2** (strategic-compact keeps), `Grok 4.7 Extra High` **x0**, `cursor-grok-4.6-high-fast` **x72**. Agent `model:` inventory: **41 × `cursor-grok-4.6-high-fast` + 4 × `inherit`** = 45 agents. `model: inherit` in exactly the four chat-model agents: `deep-reasoner.md`, `ecc-architect.md`, `ecc-healthcare-reviewer.md`, `ecc-spec-miner.md`. Staged `new-skills/orchestrate/agents/deep-reasoner.md:4` reads `model: inherit`.

## 3. Observations (not findings)

- **fakehome33's fix33.py still carries the stale DECISION-33-5 string** (`fix33/fakehome33/workspace/hackathon-plugin/fix33/fix33.py:449`, "carries the pointer"). This is the frozen build-time snapshot from runs 5–6, not a live copy — the task defines the live copies as the fix dir + scratch-repo mirror, both corrected (§2.5). Same principle as the patch logs: a build snapshot is not rewritten. No action.
- `fix20/SPEC.md:356` contains "carries the pointers" — unrelated fix-20 history text, different phrase, out of scope.
- The fix-round report itself is accurate throughout (its §8 before/after stat +135 → +136 is the correct current figure); the staleness is confined to the two lines in §1.

## 4. Commands / results (exact)

- `cd fix33/scratch-repo && git rev-parse HEAD` → `dd106ade5f6043ec4ed613919e7908172d8eadce`
- `git diff --stat` → `33 files changed, 136 insertions(+), 109 deletions(-)`; `git status --short` → 33 modified + untracked `fix32/`, `fix33/` only
- `grep -o` counts on `scratch-repo/build.sh`: ID 48, PROSE 6, XID 1, XPROSE 0; `git show dd106ade:build.sh` same patterns: 56 / 5 / 1 / 0
- Line counts: ID on 44 lines, PROSE on 4 lines, 3 lines both → 45 ID+PROSE lines; XID on :24130; union 46 lines
- Diff ± accounting: ID −10/+2, PROSE −0/+1 (from `git diff dd106ade -- build.sh` added/removed lines)
- `grep 'unchanged (70)' build.sh` → empty; comment block :24145–24148 reads "71 pre-state, 72 post-state" + MODELSEL_F33 present
- `grep -rn MODELSEL` over built direct commands → 0; only `hackathon-ecc/skills/orchestrate/SKILL.md` carries it (2×)
- `md5sum fix33/fix33.py scratch-repo/fix33/fix33.py` → both `1533f4e8f56f3ab9a200f6a4d894014a`; `:449` reads "carries no pointer (D33-19 …)"
- `md5sum fix33-patch-log.md` (both copies) → `ddef5b7aa229ceff138d3cf3e450960c`, still carry stale wording at :44
- `git diff dd106ade -- fix31/fix31.py` → EXPECT_PIN census + comment only; `md5sum` canonical + scratch fix31.py → both `cae364c594befc6a303ecd0ceed3d447`; HEAD version `241e6bcd7804e2e45ab517b3af462cba`
- `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` → `526/526 checks pass`, exit 0
- `python3 scan32-r4-test-fix33.py` → 76 PASS, `RESULT: ALL PASS`, exit 0
- `python3 scan32-r5-test-fix33.py` in place → `FileNotFoundError` for `fix32.py`; `/tmp/audit110-r5/` with siblings → 100 PASS, `RESULT: ALL PASS`, exit 0 (probe dir deleted)
- Built census: ID 0, XID 0, PROSE 2, XPROSE 0, fast 72; agent `model:` 41 fast + 4 inherit

## 5. What remains owed (not this fix's defects)

- **110-M1:** update `+135` → `+136` in MANIFEST.md:60 and fix33-implementation-report.md:200 (two one-character edits; no rebuild, no re-verification needed beyond re-reading the stat).
- Carried forward from #109: OWED-33-1 (live test of `inherit`), OWED-33-2 (factory plan doc), OWED-33-3 (cost accounting), OWED-33-4 (direct-command Auto ask — now recorded), OWED-30-3 (live test).
