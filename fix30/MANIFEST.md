# Fix #30 — MANIFEST

**Scope:** model routing pin change — orchestrator pin `grok-4.7-high` →
`grok-4.7-extra-high` in the built tree only, plus the verifier's pin
assertions (fix30/SPEC.md, re-scoped Nov 16, 2026).
**Status: DONE locally — audit loop CLOSED (#96 PASS both halves); sweep #40
CLEAN (0 blocking, 0 minor); dry-run #45 PASS (7 legs). Next: commit,
bundle.**

## Results

| Count | Before (fix #29) | After (fix #30) |
|---|---|---|
| Skills | 67 | 67 (unchanged) |
| Agents | 45 | 45 (unchanged) |
| Rules | 48 | 48 (unchanged) |
| Commands | 55 | 55 (unchanged) |
| Hooks | 15 | 15 (unchanged) |
| Trigger keys | 49 | 49 (unchanged) |
| `grok-4.7-high` (ID, built tree) | 49 | **0** |
| `grok-4.7-extra-high` (ID, built tree) | 0 | **49** |
| `"Grok 4.7 High"` (prose, built tree) | 22 | **0** |
| `"Grok 4.7 Extra High"` (prose, built tree) | 0 | **22** |
| `cursor-grok-4.6-high-fast` (fast-worker pin) | 70 | 70 (unchanged) |
| Bare `grok-4.6-high-fast` | 0 | 0 (unchanged) |
| Files renamed | — | **24** |
| verify30.py checks | 315 (verify29) | **318, exit 0** |

**Changed:** the orchestrator pin in 24 built-tree files (49 ID + 22 prose
occurrences — per-file counts in §2(a)); the verifier's pin assertions
(verify30.py check 9 exact counts, check 9b widened to whole-tree scope
per audit #95-B1, check 13 fix30 patch-log check, check 7e pin
normalization for the staged-vs-built _F29 identity check); the build.sh
hook (+11 lines: fix30.py invocation after fix29.py, before STEP 5
Counts); the SPEC conformance edits (re-scoped counts, Carbon live-test
paragraph, `verify29.py` typo, prerequisites superseded, SPEC.md:38
Carbon open item struck through); the live-test prompt
(fix30/live-test-prompt.md).
**NOT changed:** counts (67/45/48/55/15/49); the #28 debloat; the design
package; grill-me; the alwaysApply rules; any behavior beyond model
routing; the factory (no custom drone subagents, no CLI dispatch rule,
no OpenRouter setup skill — those go in the factory copy per
FACTORY_CURSOR_PLAN.md); staged sources (old pin by design, OWED-30-1);
build.sh inline content (old pin by design, OWED-30-1); the call map
(fix28 map stands, md5 `b066413a…`).

## §1 Scope

Per the re-scoped fix30/SPEC.md (Nov 16, 2026): the brain is Grok 4.7 on
Extra High in Cursor, on the pool (Anish chose this over OpenCode /
Hydrogen / Carbon because Cursor is the best value per token). Carbon is
OUT, Grok-via-OpenRouter brain is OUT, Hydrogen brain is OUT, the $5
Google Cloud prepay is OUT, no Google API key in Cursor.

The rename is **build-time only, last in build order** (fix30.py runs
after fix29.py, before STEP 5 Counts — nothing after it writes pin text).
Staged sources and build.sh inline keep `grok-4.7-high` because fix16.py,
fix24.py and fix29.py anchor on that text and abort the build on anchor
mismatch (verified live by audit #95-A: fix16 `HIGH` + common-performance
else-branch ERROR, fix24 `_DESIGN_LEAD_OLD` :433, fix29 :424 OLD anchor).
Precedent: fix #16 itself performed the Claude → Grok pin change at
build time via fix16.py, with staged/upstream sources keeping the old
text. The staged-vs-built pin drift is by design (OWED-30-1, same class
as OWED-29-5's 41 lines).

Census (measured Nov 16, 2026 on the fix29 built tree; asserted exactly
by fix30.py — any drift fails loudly and no file is written):
`grok-4.7-high` x49 (48 in .md/.mdc + 1 in schemas/agent.schema.json:36
enum), `"Grok 4.7 High"` x22 (prose; 11 lines, some carrying 2),
`cursor-grok-4.6-high-fast` x70 (unchanged), bare
`grok-4.6-high-fast` x0, `grok-4.7-extra-high` x0 pre-rename,
`"Grok 4.7 Extra High"` x0 pre-rename. The SPEC's earlier "585 mentions"
was the fix28-tree whole-tree count, not the live-plugin scope —
corrected in the SPEC (audit #95-B confirmed the recount).

Prose judgment (OWED-30-5, accepted by audit #95-A): all 22 prose
occurrences change, including skills/strategic-compact/SKILL.md:68 (the
"500k Grok 4.7 High" context-window example — a base-model property) and
:102 (the Cursor 2.1.233 todo-tools note — the operative claim is
preserved by its "and newer" clause). The other 20 are direct references
to the orchestrator tier.

## §2 Disposition table

### (a) The rename set: 24 files (per-file ID + prose counts, from fix30-patch-log.md)

| File | ID | Prose |
|---|---|---|
| skills/orchestrate/SKILL.md | 15 | 12 |
| commands/astra-review.md | 3 | 1 |
| agents/deep-reasoner.md | 3 | 0 |
| commands/gan-design.md | 3 | 0 |
| skills/gan-style-harness/SKILL.md | 3 | 0 |
| agents/ecc-gan-planner.md | 2 | 0 |
| commands/gan-build.md | 2 | 0 |
| commands/model-route.md | 2 | 0 |
| rules/common-performance.mdc | 2 | 0 |
| rules/hackathon-mode.mdc | 2 | 3 |
| README.md | 1 | 3 |
| agents/ecc-architect.md | 1 | 0 |
| agents/ecc-healthcare-reviewer.md | 1 | 0 |
| agents/ecc-spec-miner.md | 1 | 0 |
| rules/common-agents.mdc | 1 | 0 |
| schemas/agent.schema.json | 1 | 0 |
| skills/orch-add-feature/SKILL.md | 1 | 0 |
| skills/orch-build-mvp/SKILL.md | 1 | 0 |
| skills/orch-change-feature/SKILL.md | 1 | 0 |
| skills/orch-fix-defect/SKILL.md | 1 | 0 |
| skills/orch-refine-code/SKILL.md | 1 | 0 |
| skills/orchestrate/references/agent-TEMPLATE.md | 1 | 0 |
| manifests/pi-core.json | 0 | 1 |
| skills/strategic-compact/SKILL.md | 0 | 2 |
| **Total** | **49** | **22** |

Tallies reconcile exactly with the census (audit #95-A, #96-B, sweep #39,
sweep #40 — all independent recounts agree). The GLOBAL-ROUTING block
(byte-identical in orchestrate + hackathon-mode, md5 `68206505…` in all
five sources incl. the golden copy) carries no pin and was not touched
by the rename (fix30.py guard asserts this every build).

### (b) Deliberately NOT renamed (by design, OWED-30-1)

- Staged sources keep the old pin: new-skills/ 19 ID + 12 prose
  occurrences, new-rules/ 2 ID + 3 prose occurrences. Syncing staged to
  the built text would break the fix16/fix24/fix29 anchors and fail the
  build.
- build.sh inline content keeps the old pin: 54 pre-existing ID
  occurrences on 50 lines (4 double-occurrence lines: 22682, 22771,
  22786, 23701) + 5 prose occurrences; the fix30 hook block itself adds
  2 meta-mentions (56 ID total in the file).
- The "50 occurrences" figure in the first fix30.py draft was the
  `grep -c` LINE count, not the occurrence count — corrected to 54 in
  all three records (docstring, DECISION-30-1, OWED-30-1) per sweep #39-B1
  / audit #95-A1, verified by audit #96-A's independent recount and
  sweep #40.

### (c) Conflicts found and reconciled (not silently overwritten)

- **Check 7e vs the rename:** skills/orchestrate/SKILL.md:93 carries
  both `_F29` tokens and the pin, so the rename broke the staged-vs-built
  _F29 identity check (verify30 first failed it on the test tree).
  Resolution: verify30.py check 7e pin-normalizes the built _F29 lines
  (extra-high → high, Extra High prose → High prose) before comparing —
  only the pin is normalized; any other staged-vs-built difference still
  fails. Proven live by audit #95-B (M1 non-pin word change → 7e fails;
  M2 pin-only change → 7e passes, check 9 fails instead).
- **Check 9b scope gap (audit #95-B1):** the name/slug grep covered only
  6 dirs while its comment claimed "tree-wide" — a full-tree grep found
  two benign pre-existing names outside its scope
  (manifests/pi-core.json:243 "deepseek-harness-setup" provider note;
  scripts/lib/install/content-transform.js:4 Qwen in a removed-transforms
  comment). Resolution: both greps widened to whole-tree ("." minus
  node_modules); the name allow-list is file-level for the 3 icon-data
  files and file+line for the 2 benign hits (a planted reference
  elsewhere in either file must still fail). Proven live by audit #96-B
  (planted name in manifests/ → 316/318 on exactly the 9b name checks;
  planted slug in scripts/ → 317/318 on exactly the slug check; new file
  in hooks/ → 316/318; Qwen on a new line in the allow-listed file →
  316/318). Residual (audit #96-B §7, recorded as OWED-30-6, not filed):
  a second name smuggled INSIDE an allow-listed line itself passes —
  the occurrence check counts only non-allow-listed lines.
- **OWED-29-4 override:** fix29/MANIFEST.md §5 called the DeepSeek/Qwen
  assignment a fix #30 forward reference; the factory plan overrides
  that — the drone assignment lives in the factory copy, NOT in #30.
  Recorded as OWED-30-2. verify30 check 9b still asserts no
  deepseek-/qwen- model slugs and names only in the GLOBAL-ROUTING
  block (+ the 2 allow-listed benign hits).
- **SPEC "585 mentions":** the fix28-tree whole-tree count; the fix29-tree
  recount is 49 ID + 22 prose. Corrected in the SPEC.

### (d) fix30.py + build.sh

`fix30/fix30.py` (+ `fix30/fix30.py.template`, durable source — keep in
sync; md5 `bd3559d0…` after the round-1 fixes). Sections: §1 exact
pre-rename census (refuses to write on any drift; non-UTF-8 files are
byte-checked for pin text instead of silently skipped — 154 files);
§2 the rename (ID first, then prose; per-file change records); §3
post-assertions (old ID 0, new ID 49, old prose 0, new prose 22,
fast-worker 70 unchanged, bare fast 0); §4 GLOBAL-ROUTING regression
guard (block byte-identical in orchestrate + hackathon-mode, all 7 _F29
tokens present). DECISION-30-1/2/3 + OWED-30-1..5 in the log.

Build.sh hook added after fix29's block, before STEP 5 (+11 lines).
Only build.sh edit is the fix30.py invocation. Build logs run 1 and run 2
are byte-identical apart from the fix30 record text (audit #96-A: md5
`92e758ea…` for the non-fix30 lines — the tree is unchanged by the
round-1 fixes, which were record/verifier-only).

Call map: NOT regenerated in this fix (OWED-30-4). The pin change adds
no new dispatch edges and counts are unchanged, so the fix28 map stands;
dry-run #45 leg 5 confirms 17 EXERCISED / 19 STATIC-OK / 5 DORMANT /
0 BROKEN against it.

## §3 Audit-loop record

### Audit #95 (round 1) — NOT PASS on both halves, sweep #39 NOT CLEAN

- **#95-A — NOT PASS (0 blocking, 2 minor).** Recount reconciles exactly
  (49/22/70/0); verifier re-run 318/318; build-time design proven live
  (one anchor per script with abort paths; hook placement; fix30.py ==
  template; GLOBAL-ROUTING md5 `68206505…`); liveness on a disk mirror
  (revert one pin → 317/318 on exactly the ID check; delete one pin on
  a pre-rename mirror → fix30.py exit 1, census error, no files
  written). Findings: **95-A1** OWED-30-1 count wrong in 3 places ("50"
  is the line count; actual 54 ID on 50 lines + 5 build.sh prose + 15
  staged prose omitted); **95-A2** SPEC.md:38 Carbon open item stale
  (no superseded marker).
- **#95-B — NOT PASS (0 blocking, 1 minor).** Scope compliance verified
  (counts; file lists identical vs the fix29 tree; 24 differing files
  normalize clean under the pin rename; no drone subagents, no CLI
  dispatch, no OpenRouter setup skill); 7e liveness proven (M1/M2);
  GLOBAL-ROUTING byte-identical to the golden copy (2,285 chars).
  Finding: **95-B1** check 9b scope gap (6 dirs, not tree-wide; 2 benign
  names outside scope — see §2(c)).
- **Sweep #39 — NOT CLEAN (0 blocking, 1 minor).** Pin census reproduced
  exactly; verifier re-run 318/318; counts confirmed; call-map md5
  unchanged; fix30.py == template; hook placement correct; SPEC
  operative sections clean. Finding: **39-B1** — same count error as
  95-A1. SPEC Verification section recorded NOT MET as written (live
  test outstanding — expected pre-live-test state).

Fixes applied by the coordinator (single editor): 50 → 54 in fix30.py
(docstring, DECISION-30-1, OWED-30-1) + template kept in sync; verify30.py
check 9b widened to whole-tree scope with the file+line allow-list;
SPEC.md:38 struck through + SUPERSEDED. Rebuild run 2 (exit 0);
verify30.py re-run 318/318.

### Audit #96 (round 2) — PASS on both halves, sweep #40 CLEAN

- **#96-A — PASS (0 blocking, 0 minor).** Both round-1 fixes verified as
  landed by independent recount (build.sh 54 ID on 50 lines, doubles at
  22682/22771/22786/23701; prose 5; staged 19+2 ID, 12+3 prose; patch log
  regenerated by run 2 carries the corrected figures; no stale "50
  occurrences" in any live file); SPEC.md:38 struck through; build logs
  run1/run2 byte-identical; verifier re-run 318/318; pin census exact;
  0 tree files newer than build-log-run2.txt. Caveat recorded: SPEC
  Verification section still NOT MET as written (live test outstanding)
  and sweep #39's NOT CLEAN stands until a re-sweep confirms the count
  fix (done by sweep #40 below). Observation (not a finding): a pre-fix
  scratch snapshot at fix30/scratch-tmp/fix30/fix30-patch-log.md still
  carried the old "50" text — removed by the coordinator after the
  audit; nothing read it.
- **#96-B — PASS (0 blocking, 0 minor).** 95-B1 VERIFIED-FIXED by code
  read AND liveness (baseline 318/318; planted name in manifests/ →
  316/318 on exactly the 9b name checks; planted slug in scripts/ →
  317/318 on exactly the slug check; bonus probes: new file in hooks/ →
  316/318; Qwen on a new line in the allow-listed file → 316/318).
  Residual recorded not filed (§7): a second name smuggled INSIDE an
  allow-listed line passes (OWED-30-6).
- **Sweep #40 (re-sweep) — CLEAN (0 blocking, 0 minor).** 39-B1 verified
  fixed by independent recount; pin census reproduced exactly; verifier
  re-run 318/318; check 12b passed first attempt (no transient
  recurrence); stale counts / dangling refs / README all clean; SPEC
  scope MET, Verification NOT MET as written solely because the live
  test is outstanding; dry-run #45 epic-premise error recorded as
  already adjudicated, not re-filed.

### Dry-run #45 — PASS (7 legs)

Leg 1 fixtures 101/101 (42/42 #37 regression + 59/59 fix #23); leg 2
Home Run render 17/17 assertions, 0 flags (52 measurements, 13 states ×
4 widths), Campus Eats 6/7 static with dimension 7 OWED; leg 3 /demo
59/59 (qa.mjs exit 0 twice, 12/12 stills, 0 Google Fonts requests);
leg 4 Cursor-readiness 37/37 incl. 13 live C-1 hook pipe tests; leg 5
call-graph 17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN, collab
fixture 11/11 + 6/6; leg 6 factory re-run 27/27; leg 7 pin leg (NEW)
32/32 — route table + orchestrate table resolve thinking roles to
`grok-4.7-extra-high`, mechanical to `cursor-grok-4.6-high-fast`; schema
enum validates the new pin and rejects the old; 45/45 agent pins
in-enum (4 extra-high, 41 fast); 14-step simulated trace clean; old pin
x0 trace-wide and tree-wide. Static only — live Cursor behavior OWED to
Anish's live-test prompt (OWED-30-3). Three first-run non-passes were in
the dry-run's own scripts, not the tree; corrected with re-runs passing.

- **Dry-run #45 epic-premise error — adjudicated by the coordinator:**
  the report's §10 observation ("README.md:69 still lists the dropped
  `/epic-*` commands") and its leg-5 "epic-dormant-in-use" line repeat
  dry-run #42/#43/#44's error, already adjudicated in fix27/MANIFEST.md
  and fix29/MANIFEST.md §5 — and re-filed despite an explicit
  do-not-re-file instruction in the dry-run brief. Only `/prune` was
  dropped in fix #27; all 7 epic commands ship (epic-claim,
  epic-decompose, epic-publish, epic-review, epic-sync, epic-unblock,
  epic-validate — verified live in `commands/`; 0 `prune`).
  README.md:69 is accurate. The PASS verdict is unaffected (0 BROKEN,
  all legs pass on the actual tree). Do not re-file in fix #31.

## §4 SPEC §6 criterion statuses (honest)

The SPEC's Verification section is the criterion source (scope +
verification sections). Statuses, evaluated at close:

- **Audit loop (at least 2 rounds) — MET.** 2 rounds (#95, #96). Final
  round #96 PASS on both halves (0 blocking, 0 minor). No tree or
  verifier change was made after #96, so no post-hoc fix without
  re-audit exists at close.
- **Sweep — MET.** Sweep #40 CLEAN (0 blocking, 0 minor) after #39's
  single minor was fixed and re-swept. No tree change after the sweep
  (the MANIFEST write and the commit touch no built-tree file), so no
  post-hoc fix without re-sweep exists at close.
- **Dry-run — MET.** Dry-run #45 PASS on all 7 legs, incl. the new pin
  leg 32/32.
- **Live test (Anish, in Cursor, after the fix lands) — OWED, not done.**
  Recorded as OWED-30-3. It needs Anish at his Windows machine with
  the fix #30 bundle installed.
- **verify30.py — 318/318, exit 0** (re-run independently by audit #95-A,
  #95-B, #96-A, #96-B, sweep #39, sweep #40, and dry-run #45 — all
  318/318).

**Verification section as written: NOT MET as written.** Unlike fix #29,
the live test is part of fix #30's own Verification section and it has
not run yet (it is Anish's step, after the fix lands). Everything else
in the section — audit loop, sweep, dry-run, verifier — is MET. This is
the expected pre-live-test state, not a tree defect.

## §5 Open parent adjudications

- **OWED-29-4 override (parent decision, carried):** the DeepSeek/Qwen
  assignment in the GLOBAL-ROUTING block stays a forward reference —
  the drone assignment lives in the factory copy per
  FACTORY_CURSOR_PLAN.md, NOT in #30. No model pins beyond the
  orchestrator change in this fix.
- **Live test (Anish, after fix #30 lands):** run fix30/live-test-prompt.md
  in Cursor — one reasoning-heavy task + one repo-scale coding task,
  report which model ran each. Pass = Extra High ran the parent
  (OWED-30-3). The live factory test from fix29 (OWED-29-2) stays owed
  behind it (harness-gated).
- **Dry-run #45 epic-premise error — adjudicated by the coordinator:**
  see §3. Do not re-file in fix #31.
- **Verifier fragility carried forward:** F35 (hackathon-mode
  GLOBAL-ROUTING block move caught only via check-12 `ALLOW_NAMES:47`
  collateral) — re-test if ALLOW_NAMES:47 ever changes. F-O
  (`agents/fast-worker.md:16` unasserted — pre-existing ECC text, not a
  fix #30 regression path). Check-12b transient (one non-reproduced
  extra failure in #94-B's first attempt; clean re-runs since, incl.
  sweep #40 first attempt) — re-check 12b stability if it recurs.
  NEW: 9b allow-listed-line residual (audit #96-B §7, OWED-30-6).
- **Call map (OWED-30-4):** fix28 map stands (md5 `b066413a…`); fix #30
  adds no dispatch edges, so no regeneration was done. If fix #31 adds
  a dispatch edge, regenerate then.
- **Live smoke test still skipped** (since Nov 15) — live behavior
  (55 commands, 67 skills, triggers, subagent model behavior)
  UNVERIFIED until real project use. The dry-run legs verify the
  sandbox side only.

## §6 Owed / environment-limited items (recorded, not verified)

- **OWED-30-1 (corrected per sweep #39-B1 / audit #95-A1):** staged-vs-built
  pin drift — staged sources keep the old pin (new-skills/ 19 ID + 12
  prose, new-rules/ 2 ID + 3 prose) and build.sh inline content keeps
  it (54 pre-existing ID occurrences on 50 lines + 5 prose; the fix30
  hook block itself adds 2 meta-mentions). Syncing staged to the built
  text would break the fix16/fix24/fix29 anchors and fail the build.
  Same class as OWED-29-5's 41 lines. verify30 asserts the pins in the
  BUILT tree only.
- **OWED-30-2 (OWED-29-4 override):** the DeepSeek/Qwen model assignment
  in the GLOBAL-ROUTING block stays a forward reference — the drone
  assignment lives in the factory copy per FACTORY_CURSOR_PLAN.md, NOT
  in #30. verify30 still asserts no deepseek-/qwen- model slugs in the
  built tree and the names occur only in the GLOBAL-ROUTING block (+ the
  2 allow-listed benign hits, audit #95-B1).
- **OWED-30-3 (SPEC Honest limits):** live Extra High behavior is
  unverified until Anish runs the live-test prompt
  (fix30/live-test-prompt.md) in Cursor — pass = Extra High ran the
  parent on both tasks. The live smoke test is still skipped since
  Nov 15.
- **OWED-30-4 (same as OWED-29-1):** the call map
  (skills/orchestrate/references/call-map.md) is generator-owned and NOT
  regenerated in this fix — the pin change adds no new dispatch edges
  and counts are unchanged (67/45/48/55/15/49); the fix28 map stands.
- **OWED-30-5 (prose judgment, audit to challenge — accepted by #95-A):**
  skills/strategic-compact/SKILL.md:68 and :102 prose changed to
  "Grok 4.7 Extra High" (see §1). If a future audit finds either line
  should have kept "Grok 4.7 High", the fix is a two-line carve-out in
  fix30.py plus updated census counts — not a re-scope.
- **OWED-30-6 (audit #96-B §7, recorded not filed):** a second DeepSeek/Qwen
  name smuggled INSIDE an allow-listed 9b line itself (e.g. a second
  "DeepSeek" within manifests/pi-core.json:243) passes verify30, because
  the occurrence check counts only non-allow-listed lines. A live slug
  on that line still fails the no-allow-list slug check, and exploiting
  it requires editing a pinned line. Hardening suggestion (not applied —
  it would need a verifier change + re-audit for a non-finding):
  assert the two allow-listed lines byte-equal to their fix29 text.

## §7 Push

- Remote: `github.com/anishkoduri/hackathon-ecc`, branch `main`. Pre-fix
  HEAD: `a268041` (fix #29). **Do NOT push from the sandbox (no GitHub
  auth).**
- Method: sync the working copy's changes into `fix30/scratch-repo`,
  commit as Anish Koduri <akoduri05@gmail.com> with NO
  "Co-authored-by: Cursor" trailer and no AI tool listed as
  contributor/author, create a verified git bundle (`git bundle verify`
  OK). Anish pulls the bundle from his Windows machine and pushes, as
  with fix #27/#28/#29: `git pull <bundle> main` + `git push origin main`.
- The commit hash and bundle path/size are verified by the coordinator
  after committing and reported in the final report (this manifest is
  the pre-push record, per the fix #26 convention — it does not contain
  its own commit's hash).
