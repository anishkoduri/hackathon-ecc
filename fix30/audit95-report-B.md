# Audit #95-B — scope compliance + verifier coverage + no factory creep (fix #30, round 1)

**Verdict: NOT PASS — 0 blocking, 1 minor.**

Auditor B (scope compliance + verifier coverage + no factory creep).
Read-only except this report. Method: read `fix30/SPEC.md` in full,
`fix30/fix30.py` (303 lines), `fix30/verify30.py` (2,164 lines) in full,
and `fix30/live-test-prompt.md`; independently re-ran verify30 —
**318/318, exit 0** (real tree); direct counts and greps; file-list +
pin-normalized content diff of the fix29 built tree
(`fix30/scratch-repo/hackathon-ecc`) against the rebuilt fix30 tree
(`hackathon-ecc`); GLOBAL-ROUTING block vs the golden copy
`fix29/global-routing-block.txt`; 7e liveness mutations M1/M2 on a disk
mirror under `fix30/scratch-tmp/a95b/` (fresh copy per mutation, mirror
verified byte-identical to the real tree afterwards and removed). The
real tree was never edited by this audit.

## §1 Findings

### B1 (minor) — Check 9b's name claim is false as written: two benign DeepSeek/Qwen names live outside the grep scope

Check 9b's headline assertion (verify30.py:1169) is
"DeepSeek/Qwen names occur only in the GLOBAL-ROUTING block
(orchestrate + hackathon-mode)", and its comment claims the grep "is
now tree-wide over the same scope as the slug check" (audit #84-B2
widening). It is not tree-wide. The name grep
(`grep -rn -E "DeepSeek|Qwen" skills agents commands rules hooks
README.md`, verify30.py:1163) covers six dirs only. A
case-sensitive `DeepSeek|Qwen` grep over the whole built tree
(excluding `node_modules`) returns **7 hits in 7 files**, not 5 in 5:

| File:line | Hit | Nature |
|---|---|---|
| `skills/orchestrate/SKILL.md:36` | GLOBAL-ROUTING block, 1× DeepSeek + 1× Qwen | Intended forward reference |
| `rules/hackathon-mode.mdc:45` | GLOBAL-ROUTING block, 1× DeepSeek + 1× Qwen | Intended forward reference |
| `skills/design-taste-frontend/assets/icons/demo.html:48` | DeepSeek icon chip | Allow-listed icon data (`_DSQ_ALLOW`) |
| `skills/design-taste-frontend/assets/icons/demo/icons-credits.json:1056` | `"name": "DeepSeek"` | Allow-listed icon data |
| `skills/design-taste-frontend/assets/icons/index.json:1298` | `"name": "DeepSeek"` | Allow-listed icon data |
| `manifests/pi-core.json:243` | `"deepseek-harness-setup": "configures an external DeepSeek provider and Cursor-specific credentials and hook integration"` | **Outside the grep scope — not seen by 9b** |
| `scripts/lib/install/content-transform.js:4` | `// transforms (Cursor manual-plugin namespace, Qwen/Antigravity/Copilot frontmatter, …) are removed with their host adapters.` | **Outside the grep scope — not seen by 9b** |

Both out-of-scope hits are benign and pre-existing (byte-identical
lines in the fix29 scratch tree, `fix30/scratch-repo/hackathon-ecc`,
line 243 and line 4 respectively): the pi-core.json hit is an
*exclusion* note for an unshipped upstream skill (negative mention,
the same class as check 12's allow-listed negatives), and the
content-transform.js hit is a comment about host transforms that were
*removed*. Neither is a live dispatch, a model slug, or a drone
assignment, and fix #30 changed neither line (pi-core.json differs
between the fix29 and fix30 trees only by the pin rename —
normalized diff clean, §3). The slug half of 9b is clean: no
`deepseek/` or `qwen/` anywhere, no `deepseek-v3` / `qwen3` model IDs
anywhere, `deepseek-`/`qwen-` strings only as `logos:deepseek-icon`
icon data.

The defect is the verifier's, not the tree's: the check passes while
its headline claim is literally false, and the gap is load-bearing in
exactly the direction 9b exists to guard — a live DeepSeek/Qwen
reference planted in `manifests/` (e.g. an install-profile description
or a pi-core include entry naming a drone model) or in `scripts/`
would pass 9b today. This is the #84-B2 shape one step further: that
round widened the grep because a reference in `references/` or
`commands/` passed; the same widening is now owed for `manifests/`
and `scripts/`.

**Required fix:** widen the 9b name grep (and, for symmetry, the slug
grep) to the whole built tree minus `node_modules`, with an explicit
allow-list for the two benign hits above (same `_DSQ_ALLOW` pattern),
and correct the "tree-wide" comment to state the actual scope. Then
re-audit: a re-run of verify30 plus a direct full-tree
`DeepSeek|Qwen` grep must show exactly the two GLOBAL-ROUTING lines
plus the allow-listed hits. Per the fix #27 convention, if this minor
is fixed post-hoc without a re-audit, the verdict stands as NOT MET
as written.

## §2 Nits (not counted)

- verify30.py's header docstring lists check 13 ("[30] fix30 patch
  log") before the 7c paragraph, and the tail of the check-12b
  description ("within 120 characters after the verb, except negated
  verbs…") lands after the check-13 paragraph. Cosmetic comment
  ordering only; the checks execute in numeric order (13 is the last
  check in the file, verify30.py:2159) and all 318 pass. Not a finding.

## §3 Scope compliance — no behavior change beyond routing

- **Counts (direct listing, not just the verifier):** skills 67,
  agents 45, rules 48, commands 55, hook events 15
  (`hooks/hooks.json`), trigger keys 49 — all as specified.
- **File-list diff, fix29 built tree vs fix30 rebuilt tree:** `find`
  file lists are **identical** (zero added, zero removed files). The
  only `diff -rq` differences are the 7 known empty untracked dirs
  under `scripts/lib/` (`agent-proximity`, `control-pane`,
  `eval-harness`, `plan-canvas`, `session-adapters`,
  `skill-improvement`, `worktree-lifecycle` — 0 files, 7 empty dirs,
  present only in the rebuilt tree) and 25 files whose content
  differs.
- **All 25 differing files differ ONLY by the pin rename.** After
  normalizing `grok-4.7-high` → `grok-4.7-extra-high` and `Grok 4.7
  High` → `Grok 4.7 Extra High` in the fix29 copies, all 25 diffs are
  empty: README.md, `agents/` (deep-reasoner, ecc-architect,
  ecc-gan-planner, ecc-healthcare-reviewer, ecc-spec-miner),
  `commands/` (astra-review, gan-build, gan-design, model-route),
  `manifests/pi-core.json`, `rules/` (common-agents,
  common-performance, hackathon-mode), `schemas/agent.schema.json`,
  `skills/` (gan-style-harness, orch-add-feature, orch-build-mvp,
  orch-change-feature, orch-fix-defect, orch-refine-code,
  orchestrate, orchestrate/references/agent-TEMPLATE.md,
  strategic-compact). The pin-occurrence sets match exactly after the
  same normalization.
- **No factory creep.** No new skill, agent, command, rule, or hook
  (file lists identical). No custom drone subagents (agents/ set
  identical to fix29). No CLI dispatch rule: the only
  dispatch-adjacent matches for `cli dispatch|drone subagent` are
  false positives in pre-existing fix29 prose (redesign.md:68,
  orchestrate SKILL.md:93 factory-queue text). No OpenRouter setup
  skill: `openrouter` occurs in the built tree only as icon data
  (`design-taste-frontend/assets/icons/` — demo.html:48 chip,
  icons-credits.json:3511–3520, index.json:1326–1328 + the
  `logos:openrouter-icon` sprite); no `openrouter.ai/api/v1` URL, no
  Override-OpenAI-Base-URL instruction, no API key handling anywhere
  in skills/agents/commands/rules. `commands/model-route.md` is a
  pre-existing recommendation command (present in the fix29 tree,
  differs only by the pin rename) that now recommends
  `grok-4.7-extra-high` for implementation/architecture — a pin
  update, not a dispatch mechanism.
- **fix30.py == fix30.py.template** (byte-identical). build.sh hooks
  fix30.py immediately after fix29.py and before STEP 5 Counts
  (build.sh:24124–24133), as the SPEC requires.
- **Pin census (independent grep, whole tree excl. node_modules):**
  `grok-4.7-extra-high` ×49, `grok-4.7-high` ×0, `Grok 4.7 Extra
  High` ×22, `Grok 4.7 High` ×0, `cursor-grok-4.6-high-fast` ×70,
  bare `grok-4.6-high-fast` ×0 — exactly the SPEC census.
  `fix30.py`'s pre-rename census (49/22/70/0) matches the fix29
  tree, and its post-rename assertions match the rebuilt tree.
- **OWED-30-5 prose judgment (challenged, not filed):**
  `skills/strategic-compact/SKILL.md:68` ("500k Grok 4.7 Extra High"
  context-window example) and `:102` ("Cursor 2.1.233 removed the
  todo/task tools by default on Grok 4.7 Extra High, Grok 4.6 High
  Fast, and newer") both renamed uniformly; the :102 operative claim
  is preserved by its "and newer" clause. A mixed tree would break
  the exact-count assertions; the uniform rename is coherent.

## §4 Verifier coverage — checks 9, 9b, 13, 7e (read in full)

verify30.py is 2,164 lines, read end to end for the new/changed
checks; the inherited checks were spot-read against the #94-B record
(verify30.py carries verify29.py's checks with the pin assertions
updated).

### Check 9 (verify30.py:1104–1133) — exact pin counts. Clean.

Counts via `grep -ro` over `.` excluding `node_modules`, asserted
exactly (49/0/22/0/70), plus the bare-fast filter (lines containing
`cursor-grok-4.6-high-fast` removed before asserting zero bare
occurrences). No substring-aliasing hazard: `grok-4.7-extra-high`
does not contain `grok-4.7-high`, and `Grok 4.7 Extra High` does not
contain `Grok 4.7 High`, so the old-pin zero counts are real zeros,
confirmed by the independent grep in §3. The bare-fast count was
re-verified with a position-aware check (occurrence preceded by
`cursor-` or not): 70 total, 0 bare.

### Check 9b (verify30.py:1136–1173) — NOT CLEAN. See B1.

The slug half is clean (no `deepseek/`/`qwen/` slugs; occurrence
counts 1× DeepSeek + 1× Qwen per GLOBAL-ROUTING block, the #86-B1
defense-in-depth, re-verified directly). The name half is clean
*within its six dirs* but its scope excludes `manifests/` and
`scripts/`, where two benign names live (§1, B1). The check's
headline claim therefore overstates what it proves.

### Check 13 (verify30.py:2152–2160) — patch-log assertions. Clean.

Asserts the log exists with `## Errors (0)` and the census strings
`grok-4.7-high x49`, `'Grok 4.7 High' x22`,
`cursor-grok-4.6-high-fast x70`, `grok-4.7-extra-high x49`. All five
strings verified present in `fix30/fix30-patch-log.md` by direct
grep; the log records 27 changes (census + 25 renamed files + post
+ GLOBAL-ROUTING guard), 0 errors, 3 decisions, 5 OWED items. The
per-file rename tallies in the log sum to the census (ID 49, prose
22) and match the 25-file diff in §3.

### Check 7e (verify30.py:1021–1057) — pin normalization is pin-only. PROVEN by mutation.

The code: for each of the 7 staged/built pairs, take the `_F29`
lines in order, normalize the built lines with
`.replace("grok-4.7-extra-high", "grok-4.7-high").replace("Grok 4.7
Extra High", "Grok 4.7 High")` (verify30.py:1051–1052), then require
order-sensitive equality with the staged lines and a non-empty list.
Staged-vs-built `_F29` line counts re-verified directly for all 7
pairs (orchestrate 4/4, dispatch-prompt 10/10, deep-reasoner 1/1,
feature-expansion 2/2, design-taste-frontend 1/1, redesign 1/1,
hackathon-mode 1/1) with normalized equality holding in every case.

Liveness, on the disk mirror (fresh copy per mutation, §8):

| Mutation | Result | What it proves |
|---|---|---|
| M1: one NON-PIN word in an `_F29` line — `agents/deep-reasoner.md:17`, `under-specified` → `underspecified` (verify30.py contains zero occurrences of `under-specified`, so no other check reads that word) | **317/318**, exactly the 7e check for `agents/deep-reasoner.md` | The normalization does not mask non-pin edits; a one-word drift fails exactly its 7e check |
| M2: one PIN only in an `_F29` line — `skills/orchestrate/SKILL.md:93`, first `grok-4.7-extra-high` → `grok-4.7-high` | **317/318**, exactly the check-9 ID-count check (`grok-4.7-high` ×1, `grok-4.7-extra-high` ×48); the 7e orchestrate check **passes** | The normalization masks exactly the pin: a pin-only change passes 7e while check 9 still catches the count drift |

M1 + M2 together prove the normalization is pin-only: it forgives
the one by-design difference (the pin) and nothing else. The known
7e residual from #94-B stands unchanged and is not a #30 regression:
order-sensitivity is vacuous for a whole-line move in a
single-`_F29`-line file (deep-reasoner, redesign, hackathon-mode) —
M1 shows the line-content trip still works in that case, and no #30
change touches line order.

## §5 GLOBAL-ROUTING block — byte-identical, golden-pinned

- Block appears exactly once in `skills/orchestrate/SKILL.md:36`
  and once in `rules/hackathon-mode.mdc:45`.
- Both blocks are 2,285 chars and byte-identical to each other and
  to the golden copy `fix29/global-routing-block.txt` (extracted the
  way verify30.py does it, from the `**GLOBAL-ROUTING` marker — the
  hackathon-mode line carries a `- ` list prefix, which the
  extraction strips; a naive whole-line compare differs by those 2
  chars and is not a finding).
- DeepSeek 1× + Qwen 1× per block (occurrence counts, #86-B1).
- The block's "(fix #30 assigns DeepSeek to reasoning-heavy work and
  Qwen to coding work)" sentence is the OWED-29-4 forward reference
  itself, unchanged since fix29 (golden-pinned): no drone assignment
  is implemented in #30, and the drone work lives in the factory copy
  per the SPEC re-scope and FACTORY_CURSOR_PLAN.md. Recorded, not
  filed — see §7.

## §6 Live-test prompt — matches the SPEC

`fix30/live-test-prompt.md` gives one reasoning-heavy task (Task A:
merge-order decision doc, `DECISION.md`) and one repo-scale coding
task (Task B: TypeScript task queue, 4 files + tests, run end to
end), and requires a per-task report stating (1) which model ran the
parent, (2) which model ran each subagent, (3) whether any subagent
fell back. Pass criterion: **the parent ran Grok 4.7 Extra High on
both Task A and Task B** (model indicator); subagent models are
information-only. That matches the SPEC exactly (pass = Extra High
ran the parent). The prompt also states the pre-condition (select
Grok 4.7 Extra High in the picker first) and notes the live smoke
test for real project behavior is still skipped since Nov 15. The
live test itself is Anish's run in Cursor and is unverified here, as
expected at this stage.

## §7 Tested and NOT filed — adjudications and fresh-hunt greens

- **OWED-29-4 override (forward reference).** The DeepSeek/Qwen
  assignment in the GLOBAL-ROUTING block stays a forward reference;
  the drone assignment lives in the factory copy, NOT in #30. The
  block text is byte-identical to the fix29 golden copy, so #30
  introduced no new assignment claim. Not filed.
- **Dry-run #44 /prune error.** Already adjudicated: only `/prune`
  was dropped in fix #27; all 7 epic commands ship
  (`epic-claim`, `epic-decompose`, `epic-publish`, `epic-review`,
  `epic-sync`, `epic-unblock`, `epic-validate` all in the kept set,
  all present on disk). Not re-filed.
- **SPEC "585 mentions".** That was the fix28-tree whole-tree count.
  The fix29-tree recount (49 ID + 22 prose) is confirmed by
  independent grep (§3) and by fix30.py's pre-rename census. Not a
  finding.
- **No MANIFEST.md for fix #30.** That is the coordinator's next
  step after the audit loop, not a finding.
- **Live smoke test skipped since Nov 15.** Live behavior is
  unverified until real project use; the live-test prompt (§6) is
  the check for that. Not a finding against this fix.
- **Icon-data DeepSeek/OpenRouter names.** `demo.html:48`,
  `icons-credits.json:1056`, `index.json:1298` (plus
  `logos:openrouter-icon` entries) are pre-existing icon-dataset
  data, not model references or dispatches. Not filed.
- **Lowercase `qwen` bytes in a binary image**
  (`skills/design-taste-frontend/assets/photos/img/m138547195-1200.webp`,
  offset 30418): compressed image data, not text; the
  case-sensitive name grep correctly does not match it. Not filed.
- **Check 9's `grep -ro` scope** includes `manifests/`,
  `schemas/`, and `scripts/` (whole tree minus `node_modules`), so
  the pin counts are genuinely tree-wide — unlike 9b's name grep
  (B1). Clean.
- **Staged-vs-built pin drift (OWED-30-1)** is by design: staged
  sources keep `grok-4.7-high` (fix16/24/29 anchors abort the build
  on mismatch) and build.sh inline keeps it (50 occurrences);
  fix30.py renames only the built tree, last in build order. The
  7e normalization (§4) is the compensating check, and M1/M2 prove
  it is pin-only. Not a finding.

## §8 Methodology note

- Independent re-run: `python3 fix30/verify30.py hackathon-ecc` →
  **318/318, exit 0** (real tree), matching the recorded build run.
- Tree diff: `fix30/scratch-repo/hackathon-ecc` is the fix29 built
  tree; its file list vs the rebuilt `hackathon-ecc` is identical,
  and all 25 content-differing files normalize to identical under
  the pin substitution (§3).
- Mirror harness: `fix30/scratch-tmp/a95b/` (disk, not /tmp, per the
  /tmp-full lesson) — `pristine` (full copy of the built tree),
  `built` (working copy, fresh `cp -r` from pristine per mutation),
  symlinks to the real `fix28/`, `fix29/`, `new-rules/`,
  `new-skills/`, `fix30/` so checks 7e/10g/11/11b/13 run
  meaningfully. Mirror baseline **318/318** before mutation. No
  in-place restores anywhere in this audit. After M1/M2, `pristine`
  was verified byte-identical to the real tree (`diff -rq`,
  including `node_modules`) and the whole `a95b/` directory was
  removed. The sibling `fix30/scratch-tmp/a95a/` belongs to the
  parallel auditor-A run and was left untouched.
- First mirror attempt failed on setup, not on substance: `cp -a`
  exits non-zero on "failed to preserve ownership" in this sandbox,
  which broke the `&&` chain before the symlinks and baseline ran;
  the run was redone with `cp -r` and the correct relative verify
  path. No conclusion rests on the aborted attempt.
- The real tree was never edited by this audit; the only file
  written is this report.
