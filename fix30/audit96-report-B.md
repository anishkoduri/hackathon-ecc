# Audit #96-B — scope compliance + verifier coverage + no factory creep (fix #30, round 2 — re-audit)

**Verdict: PASS — 0 blocking, 0 minor.**

Auditor B (scope compliance + verifier coverage + no factory creep).
Read-only except this report. Method: read `fix30/SPEC.md` in full and
`fix30/audit95-report-B.md` in full; read `fix30/verify30.py` check 9b
in full (lines 1136–1195) and spot-read the check-9 pin counts; independently
re-ran verify30 — **318/318, exit 0** (real tree); direct counts and greps;
file-list + pin-normalized content diff of the fix29 built tree
(`fix30/scratch-repo/hackathon-ecc`) against the rebuilt fix30 tree
(`hackathon-ecc`); GLOBAL-ROUTING block vs the golden copy
`fix29/global-routing-block.txt`; 9b liveness mutations A–E on a disk
mirror under `fix30/scratch-tmp/a96b/` (fresh copy per mutation, mirror
verified byte-identical to the real tree afterwards and removed). The
real tree was never edited by this audit.

## §1 Disposition of the #95-B fix — 95-B1 VERIFIED-FIXED

The coordinator widened check 9b exactly as #95-B1 required, and every
reproduction below fails exactly its intended check.

| Required element | Where it landed | Verified how |
|---|---|---|
| Slug greps whole-tree (`.` scope, minus `node_modules`) | verify30.py:1159–1165 (`deepseek/` and `qwen/` greps over `"."`) | Read the code; mutation B fails exactly the slug check |
| Name grep whole-tree (`.` scope, minus `node_modules`) | verify30.py:1177–1180 (`DeepSeek\|Qwen` grep over `"."`) | Read the code; mutations A, C, D fail exactly the 9b name checks |
| Name allow-list file-level for the 3 icon-data files | verify30.py:1168–1172 (`_DSQ_ALLOW`: demo.html, icons-credits.json, index.json) | Read the code; real-tree run passes with all 3 hits present |
| Name allow-list file+line for the 2 benign hits | verify30.py:1173–1176 (`_DSQ_ALLOW_LINES`: `manifests/pi-core.json: {243}`, `scripts/lib/install/content-transform.js: {4}`) | Read the code; mutations A and D fail on NEW lines in those same files |
| "Tree-wide" comment corrected to describe the new scope + the B1 allow-list | verify30.py:1136–1158 (comment now states both greps are whole-tree, names the #84-B2 and #95-B1 history, and lists both allow-listed hits with their line numbers) | Read in full |

String-level confirmation (not just check behaviour): the allow-listed
line numbers match the real tree — `manifests/pi-core.json:243` is the
`"deepseek-harness-setup"` provider note and
`scripts/lib/install/content-transform.js:4` is the Qwen
removed-transforms comment (both confirmed by direct `sed` on the real
tree, and both byte-identical to the fix29 scratch tree, as #95-B
recorded).

Liveness, on the disk mirror (fresh copy per mutation, §8):

| Mutation | Result | What it proves |
|---|---|---|
| A: "DeepSeek" name on a NEW line in `manifests/pi-core.json` (valid JSON entry inserted after :243) | **316/318**, exactly the two 9b name checks (line-count + #86-B1 occurrence-count) | A name planted in `manifests/` on a non-allow-listed line now fails 9b — the exact hole B1 named |
| B: `"qwen/qwen3-coder-30b-a3b-instruct"` slug appended as a comment to `scripts/lib/install/content-transform.js` | **317/318**, exactly the 9b slug check | A slug planted in `scripts/` now fails 9b — the slug grep is genuinely tree-wide, not just the name grep |
| C: "DeepSeek" name in a brand-new file `hooks/audit96b-plant.txt` (a dir never in the old 6-dir scope) | **316/318**, exactly the two 9b name checks | The widening is not just manifests/+scripts/-deep: any new file anywhere in the tree is covered |
| D: "Qwen" name on a NEW line (EOF comment) in `scripts/lib/install/content-transform.js` | **316/318**, exactly the two 9b name checks | The allow-list is file+LINE, not file-wide: a new line in an allow-listed file still fails |
| E2: second "DeepSeek" smuggled INSIDE the allow-listed line itself (`pi-core.json:243`, valid JSON) | **318/318** (passes) | Residual, recorded not filed — see §7. The occurrence check counts only non-allow-listed lines, so a name appended to an allow-listed line itself is invisible to 9b. The slug check (no allow-list) still catches any live `deepseek/` slug on that line. |

The 95-B1 fix is verified as landed, not trusted: the code reads as
specified, the pristine mirror baseline is 318/318, and all four
in-scope mutations fail exactly their intended checks. The two
allow-listed hits still pass on the real tree (318/318, no
false-positive from the widening), and the occurrence-count check
(one DeepSeek + one Qwen per GLOBAL-ROUTING block) still holds.

## §2 New findings

None. 0 blocking, 0 minor.

## §3 Nits (not counted)

None.

## §4 Tested and NOT filed — adjudications and fresh-hunt greens

### #95-B §1 adjudications re-confirmed

- **The two out-of-scope hits are benign and pre-existing.** Both lines
  are byte-identical to the fix29 scratch tree and unchanged by fix
  #30 (the only fix30 change to `pi-core.json` is the prose pin rename,
  §5). The pi-core.json hit is an exclusion note for an unshipped
  upstream skill (negative mention); the content-transform.js hit is a
  comment about host transforms that were removed. Neither is a live
  dispatch, a model slug, or a drone assignment. Not re-filed.
- **The slug half of 9b was already clean in round 1 and stays clean.**
  Direct whole-tree grep: `deepseek/` 0×, `qwen/` 0×, `deepseek-v3` /
  `qwen3` model IDs 0×. The only `deepseek-`/`qwen-` strings are the
  allow-listed `deepseek-harness-setup` key and the
  `logos:deepseek-icon` icon data. Not filed.

### Standing-claim correction (not a finding)

- **#95-B §3's "25 files" is a miscount; the real number is 24.**
  The fix30 patch log lists 24 `pin renamed` lines (plus census +
  post + guard = 27 changes), build-log-run2 lists 24 renamed files,
  and my independent `diff -rq` of the fix29 vs fix30 trees finds
  exactly 24 differing files — all 24 normalize to identical under
  the pin substitution (§5). The per-file tallies in the log sum to
  the census exactly (ID 49, prose 22; re-added by hand from the log).
  Nothing in the tree is wrong; the #95-B report's count was off by
  one. Corrected here for the record.

### Fresh hunt — every 9b-adjacent class probed, all caught or adjudicated-green

- **E2 residual (same-line smuggle on an allow-listed line).** See §1
  table and §7. A bare name appended to an allow-listed line passes
  9b because `_dsq_allowed` exempts the whole line before the
  occurrence count runs. Recorded, not filed: #95-B1's requirement
  was "a planted reference elsewhere in either file must still fail"
  — E2 is on the same line, not elsewhere — and any live model slug
  on that line still fails the slug check, which carries no
  allow-list. Hardening suggestion in §7.
- **First E attempt (invalid JSON, discarded).** Appending
  `" DeepSeek"` after the closing quote of `pi-core.json:243` broke
  JSON parsing and the verifier exited 1 with a `JSONDecodeError`
  traceback from the check that parses the manifest — it fails loud,
  never silent, so it is not a false-pass and not a finding. The
  mutation was redone validly as E2. Recorded in §8.
- **CLI dispatch comment.** `scripts/lib/github-coordination.js:59`
  (`// --- CLI dispatch (Audit #5, Fixer A) ---`) is a pre-existing
  comment header, byte-identical in the fix29 scratch tree — not a
  dispatch mechanism and not a #30 addition. Not filed.
- **OWED-30-5 prose judgment (challenged, not filed).**
  `skills/strategic-compact/SKILL.md:68` and `:102` renamed uniformly
  to "Grok 4.7 Extra High"; the :102 operative claim is preserved by
  its "and newer" clause. Same adjudication as #95-B §3. Not filed.
- **OWED-29-4 override (forward reference).** The DeepSeek/Qwen
  assignment in the GLOBAL-ROUTING block stays a forward reference;
  the drone assignment lives in the factory copy, NOT in #30. The
  block is byte-identical to the fix29 golden copy (§6). Not filed.
- **Dry-run #44 /prune error.** Already adjudicated in #95-B §7; all
  7 epic commands ship and are present on disk. Not re-filed.
- **Live smoke test skipped since Nov 15.** Live Extra High behavior
  is unverified until Anish runs the live-test prompt; the prompt
  itself matches the SPEC (§6 of #95-B, unchanged). Not a finding
  against this fix.
- **Icon-data DeepSeek/OpenRouter names.** `demo.html:48`,
  `icons-credits.json:1056`, `index.json:1298` (plus
  `logos:openrouter-icon` entries) are pre-existing icon-dataset
  data, not model references or dispatches. Not filed.
- **Lowercase `qwen` bytes in a binary image**
  (`skills/design-taste-frontend/assets/photos/img/m138547195-1200.webp`,
  offset 30418): compressed image data, not text; the case-sensitive
  name grep correctly does not match it. Not filed.
- **Staged-vs-built pin drift (OWED-30-1)** is by design: staged
  sources keep `grok-4.7-high` (fix16/24/29 anchors abort the build
  on mismatch) and build.sh inline keeps it; fix30.py renames only
  the built tree, last in build order. The 7e pin-normalization is
  the compensating check, proven pin-only by #95-B's M1/M2. Not a
  finding.

## §5 Scope compliance — no behavior change beyond routing

- **Counts (direct listing, not just the verifier):** skills 67,
  agents 45, rules 48, commands 55, hook events 15
  (`hooks/hooks.json`), trigger keys 49
  (`manifests/context-packs/skill-triggers@1.json`, coverage
  67/49) — all as specified, all identical to the fix29 tree.
- **File-list diff, fix29 built tree vs fix30 rebuilt tree:** `find`
  file lists are **identical** (zero added, zero removed files). The
  only `diff -rq` differences are the 7 known empty untracked dirs
  under `scripts/lib/` (`agent-proximity`, `control-pane`,
  `eval-harness`, `plan-canvas`, `session-adapters`,
  `skill-improvement`, `worktree-lifecycle` — 0 files each, present
  only in the rebuilt tree) and 24 files whose content differs.
- **All 24 differing files differ ONLY by the pin rename.** After
  normalizing `grok-4.7-high` → `grok-4.7-extra-high` and `Grok 4.7
  High` → `Grok 4.7 Extra High` in the fix29 copies, all 24 diffs
  are empty: README.md, `agents/` (deep-reasoner, ecc-architect,
  ecc-gan-planner, ecc-healthcare-reviewer, ecc-spec-miner),
  `commands/` (astra-review, gan-build, gan-design, model-route),
  `manifests/pi-core.json`, `rules/` (common-agents,
  common-performance, hackathon-mode), `schemas/agent.schema.json`,
  `skills/` (gan-style-harness, orch-add-feature, orch-build-mvp,
  orch-change-feature, orch-fix-defect, orch-refine-code,
  orchestrate, orchestrate/references/agent-TEMPLATE.md,
  strategic-compact). (24, not the 25 cited in #95-B §3 — see §4.)
- **No factory creep.** No new skill, agent, command, rule, or hook
  (file lists identical; `agents/` dir listing byte-identical to
  fix29). No custom drone subagents (the 4 agent files mentioning
  "subagent" are pre-existing kept-agent prose; 3 byte-identical to
  fix29, the 4th — ecc-gan-planner — differs only by the pin
  rename). No CLI dispatch: the only match is the pre-existing
  comment header above (§4). No OpenRouter setup skill:
  `openrouter.ai/api/v1` 0×, "Override OpenAI Base URL" 0×,
  `openrouter` outside icon data 0×, no `deepseek/deepseek` or
  `qwen/qwen3` slugs anywhere, no openrouter/drone skill dir.
  `commands/model-route.md` is a pre-existing recommendation command
  (present in the fix29 tree, differs only by the pin rename) that
  now recommends `grok-4.7-extra-high` — a pin update, not a dispatch
  mechanism.
- **Pin census (independent grep, whole tree excl. node_modules):**
  `grok-4.7-extra-high` ×49, `grok-4.7-high` ×0, `Grok 4.7 Extra
  High` ×22, `Grok 4.7 High` ×0, `cursor-grok-4.6-high-fast` ×70,
  bare `grok-4.6-high-fast` ×0 — exactly the SPEC census.
- **Build run 2:** `fix30/build-log-run2.txt` ends `fix30: OK` /
  `build complete`, counts 67/45/48/55/15, post-rename census
  49/22/0/0/70 as specified. Rebuild changed nothing else: the
  rebuilt tree still diffs from fix29 by exactly the 24 pin-rename
  files above.

## §6 GLOBAL-ROUTING block — byte-identical, golden-pinned

- Block appears exactly once in `skills/orchestrate/SKILL.md:36`
  and once in `rules/hackathon-mode.mdc:45`.
- Both blocks are 2,285 chars, md5 `68206505a08f90474dc4931b0e5fb6bb`,
  byte-identical to each other and to the golden copy
  `fix29/global-routing-block.txt` (extracted the way verify30.py
  does it, from the `**GLOBAL-ROUTING` marker — the hackathon-mode
  line carries a `- ` list prefix, which the extraction strips).
- DeepSeek 1× + Qwen 1× per block (occurrence counts, #86-B1).
- Direct whole-tree `DeepSeek|Qwen` grep returns exactly **7 hits in
  7 files**: the 2 GLOBAL-ROUTING lines + the 3 allow-listed icon-data
  files + the 2 allow-listed benign hits. That is the full
  allow-listed universe — no other name exists anywhere in the tree.

## §7 Residual — recorded, not filed: same-line smuggle on an allow-listed line (E2)

Mechanism: `_dsq_allowed` (verify30.py:1183–1195) exempts an entire
grep line when its file+line is allow-listed, and the #86-B1
occurrence-count check sums `DeepSeek`/`Qwen` only over the
post-filter list `_dsq`. A bare name appended to an allow-listed line
itself — e.g. a second "DeepSeek" inside the `pi-core.json:243`
string, or a "Qwen" appended to `content-transform.js:4` — therefore
passes both 9b name checks (E2: **318/318** on a valid-JSON mutation).
The same residual applies in principle to the 3 file-level
icon-data allow-list entries.

Why not filed: (1) #95-B1's requirement was a planted reference
*elsewhere* in either file — E2 is on the same line, outside the
required scope, and mutations A and D prove the required scope holds;
(2) the dangerous form — a live model slug — cannot hide there,
because the slug check greps `deepseek/`/`qwen/` with NO allow-list
(mutation B proves the slug check trips on a planted slug in the
allow-listed file itself); (3) exploiting E2 requires editing one of
exactly 2 pinned lines (or the icon datasets), which any diff review
sees; (4) the check's headline claim as now written is literally
true. This is a demonstrated catch with a narrow residual, in the
F35 class (#94-B §4): a hardening opportunity, not a demonstrated
gap in the tree.

Hardening suggestion for a future round (not required for #30):
assert the two allow-listed lines byte-equal to their fix29 text
(they are pre-existing and should never change), or count
`DeepSeek`/`Qwen` occurrences on those lines explicitly (expect
exactly 1 each). Either closes E2 without touching the tree.

## §8 Methodology note

- Independent re-run: `python3 fix30/verify30.py hackathon-ecc` →
  **318/318, exit 0** (real tree), matching the recorded build run 2.
- Tree diff: `fix30/scratch-repo/hackathon-ecc` is the fix29 built
  tree; its file list vs the rebuilt `hackathon-ecc` is identical,
  and all 24 content-differing files normalize to identical under
  the pin substitution (§5).
- Mirror harness: `fix30/scratch-tmp/a96b/` (disk, not /tmp, per the
  /tmp-full lesson) — `pristine` (full copy of the built tree),
  `built` (working copy, fresh `cp -r` from pristine per mutation),
  symlinks to the real `fix28/`, `fix29/`, `new-rules/`,
  `new-skills/`, `fix30/` so checks 7e/10g/11/11b/13 run
  meaningfully. Mirror baseline **318/318** before mutation. No
  in-place restores anywhere in this audit. After the mutations,
  `pristine` was verified byte-identical to the real tree
  (`diff -rq`, including `node_modules`) and the whole `a96b/`
  directory plus the driver script were removed. The sibling
  `fix30/scratch-tmp/a95a/` / `a95b/` from round 1 were already gone.
- First E attempt failed on setup, not on substance: appending text
  after the closing quote of `pi-core.json:243` produced invalid
  JSON, and the verifier exited 1 with a `JSONDecodeError` from the
  manifest-parsing check — loud failure, never silent. The mutation
  was redone validly as E2 (§1, §4). No conclusion rests on the
  aborted attempt.
- Scratch-tmp note: at cleanup, other entries that were present in
  `fix30/scratch-tmp/` at the start of this audit (`fix28/`,
  `fix29/`, `fix30/`, `new-rules/`, `new-skills/`, `test-tree/`)
  were no longer present; they were not touched by this audit (only
  `a96b/` and the driver were created and removed by me) — most
  likely removed by the parallel round-2 auditor-A run or the
  coordinator. The real tree was never edited by this audit; the only
  file written is this report.
