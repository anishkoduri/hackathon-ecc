# Audit #88-A — Fix #29 (adaptable orchestration): routing coverage / dispatch census, round 9 (first half)

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** routing coverage / dispatch census — verify the audit #87-B1 tree fix landed correctly in the built tree; re-derive the dispatcher set from scratch with fresh verb hunts; check the 10-skill routing set; spot-check the 9 MANIFEST §2(c) reconciliations; independently confirm GLOBAL-ROUTING byte-identity staged vs built.
**Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md` (§2 in full, incl. §2(b) react-build row and all 9 §2(c) reconciliations, §3 audit #87 record), `fix29/audit87-report-A.md`, `fix29/verify29.py` (87-B1 checks at :1560–1574), `fix29/fix29.py` (§5g), `fix29/build-log-run9.txt`, `fix29/verify29-run16.log`.
**Method:** re-checked the 87-B1 file:line in the built tree (`hackathon-ecc/`) and against fix29.py §5g; re-ran `python3 fix29/verify29.py` independently (301/301, exit 0, output in `/tmp/verify88A.log`); re-ran the base-pattern census (case-insensitive) and compared per-file counts against #87-A's table; ran fresh verb sweeps for dispatch verbs NOT in the base-pattern set (every verb the task named: summon, commission, engage, employ, task, assign, order, call on, bring in, set up, arrange, coordinate, marshal, deploy, activate, trigger, kick off, spin up, farm out, hand off, pass off, plus enlist, recruit, call in, stand up, offload, launch, fan out, parallel agents); enumerated every command mentioning `agent` (22 files, case-insensitive) and triaged each; read every new hit in context. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report. Build script not run.

## Verdict: PASS — 0 blocking, 0 minor

87-B1 is verified fixed in full — step 6 (Orchestrator Verify) sits immediately after step 5 (Report Summary) in the built `commands/react-build.md`, carries all the specified elements (verification against the brief's acceptance criteria: build green AND minimal scope AND no unexplained suppressions; a green build with a failed criterion is a fail; failed criterion re-dispatches the resolver with a correction brief naming the failed criterion, capped at two re-dispatches), and "correction brief" now occurs 1× in the file. The MANIFEST §2(b) record covers it, and §2(c)(7) records it as the seventh correction-brief construction site. The census reconciles exactly with #87-A (168 base-pattern hits / 49 files, per-file counts identical), the 10-skill routing set is intact, all 9 §2(c) reconciliations match the live tree, GLOBAL-ROUTING byte-identity holds staged vs built and against the golden file, and the verifier re-runs at 301/301. No new live implementation dispatch was found by any fresh-verb hunt — no fourth escape class.

## Findings

None. No blocking findings, no minor findings.

## §1 — #87-B1 disposition: the finding re-checked

| #87-B1 | Status | Evidence |
|---|---|---|
| 87-B1 (tree): `commands/react-build.md` claimed orchestrator verification in its :9 factory pointer but had no orchestrator verify step and no correction-brief path ("correction brief" 0× in the file); the resolver's own re-run build was the only check (the 81-B2 structural defect) | **VERIFIED-FIXED** | Built `hackathon-ecc/commands/react-build.md:18` now carries step 6, immediately after step 5 (`:17`, "Report Summary"): "6. **Orchestrator Verify**: After the resolver reports, the commanding agent verifies the resolver's output against the brief's acceptance criteria — the build is green AND the changes are minimal in scope AND no suppression (`// @ts-ignore`, disabled type-checking) lacks an explanation. A green build with a failed acceptance criterion is a fail. On a failed criterion, re-dispatch the resolver with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (at most two correction re-dispatches; past that, report the remaining issue as blocked with evidence)." All specified elements present: placed after the resolver's report step ✓; verifies against the brief's acceptance criteria ✓; three criteria named (build green AND minimal scope AND no unexplained suppressions) ✓; green build + failed criterion = fail ✓; re-dispatch with a correction brief naming the failed criterion ✓; cap of two re-dispatches ✓ (matching the plugin's 2-round fix-loop convention, cf. `feature-expansion:158`, `orch-pipeline:74`, `gan-build.md:30`). `grep -c "correction brief" commands/react-build.md` = **1** (was 0). The :9 factory pointer is unchanged and still reads as verified in #87-A (single-task factory drone, director brief with all seven fields, no-guessing, orchestrator verification with the re-run build as evidence not verdict, COST-AWARE) — the pointer's claim is now true of the executed wiring, which is exactly what 87-B1 required. fix29.py §5g implements exactly this insertion with the anchor `"5. **Report Summary**: Show what was fixed and what remains"`; build-log-run9.txt records `fix29: 31 change(s)` / `fix29: OK` (build-log-run9.txt:1247, :1279). verify29.py:1572–1573 asserts the orchestrator verify step and :1570–1571 asserts the full pointer text (extended from prefix-only per 87-B1); both pass in the independent re-run. MANIFEST §2(b) covers the site: the `commands/react-build.md` row (MANIFEST.md:140) records the 87-B1 fix (step 6, the three criteria, the correction brief naming the failed criterion, the two-re-dispatch cap, the full-pointer verify29 assertion), and §2(c)(7) (MANIFEST.md:160) records react-build step 6 as the seventh correction-brief construction site. §3 (MANIFEST.md, audit #87 record) records build run 9 as done with fix29.py at 31 changes and verify29 at 301/301. |

## §2 — Fresh hunt: dispatch census re-derived from scratch

Base pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files** — identical to #87-A, with identical per-file counts (40 orchestrate, 26 feature-expansion, 11 impeccable-critique, 7 dispatch-prompt, 6 orch-pipeline, 6 orch-build-mvp, 6 council, 5 common-agents, 4 hackathon-mode, 4 gan-build, 3 call-map, 3 design-taste-frontend SKILL.md, then 2s and 1s as in #87-A's table; full per-file table reproduced in the census below). The only tree change since run 8 is the react-build step 6, which contains no base-pattern verb — a zero delta is exactly what is expected. ("re-dispatch" occurs 10× tree-wide, all inside already-routed/covered files: `orchestrate:250/:252`, `dispatch-prompt.md:44`, `orch-pipeline:74`, `feature-expansion:158`, `gan-style-harness:155`, `gan-build.md:30/:63`, `react-build.md:18` — the last is the new step 6 itself.)

Reconciliation of the GLOBAL-ROUTING count (a counting-method note, not a tree change):
- `GLOBAL-ROUTING_F29`: **17 files** (same as #87-A) but **23 raw occurrences** vs #87-A's reported 20. The delta is exactly three second mentions on single long lines, each carrying the token twice: `feature-expansion:139` (2), `gan-style-harness:14` (2), `orchestrate:93` (2) — verified by per-line counts. #87-A's 20 was a line/site count (one per line); the raw-occurrence count is 23. No token was added or removed in run 9 (step 6 carries no `_F29` token); the file set is unchanged.
- `"Factory routing (fix #29"`: **12 files ×1** (unchanged from #87-A).
- `grep -c GLOBAL-ROUTING_F29` per skill (lines): orchestrate 2, orch-pipeline 1, orch-build-mvp 2, orch-add-feature 1, orch-change-feature 1, orch-fix-defect 1, orch-refine-code 2, feature-expansion 1, gan-style-harness 1, design-taste-frontend SKILL.md 1 (+ redesign.md 1) — identical to #87-A's table.

Fresh-verb sweeps (all `*.md`/`*.mdc`, skills/rules/commands/agents), each read in context:

- **`summon|commission|engage|employ|call on|bring in|arrange|coordinate|marshal|farm out|pass off|enlist|recruit|call in|kick off` + agent/drone/subagent/worker/executor (either order):** 0 hits. None of these verbs occurs near an agent-shaped noun anywhere in the tree.
- **`assign` + agent/drone/subagent/worker/executor:** 13 raw hits, none a new dispatch. In routed files (`orchestrate:36/:335`, `hackathon-mode.mdc:45`, `patterns.md:13`, `feature-expansion:216` — the handoff execution contract, inside the routed skill); in role files as code words (variable assignment, "assign score 1-5" in `ecc-agent-evaluator.md`, "not assignable to 'Y'" in `ecc-build-error-resolver.md:60`, `innerHTML` assignment, `const`/`let` reassignment). No dispatch.
- **`order` + agent/drone/subagent/worker/executor:** 54 raw hits, none a new dispatch. "merge order" / "in order to" / "implementation order" / SQL `ORDER BY` / focus order / key order — all code or prose words; the only agent-shaped one is `orch-pipeline:68` ("delegate to the `architect` agent"), inside the routed skill under its factory paragraph.
- **`deploy` + agent/drone/subagent/worker/executor:** 29 raw hits, none a new dispatch. All deployment (Vercel/Railway/Cloud Run, "before deploy" timing, `deploy-fast` runbook, "SAFE TO DEPLOY" verdicts, "FastAPI/Node workers" as runtime workers), call-map rows, or "Independent deployability" in role files. No agent dispatch.
- **`trigger` + agent/drone/subagent/worker/executor:** 38 raw hits, none a new dispatch. Trigger phrases (`hackathon-mode.mdc:12` grill-me triggers), event triggers, `call-map.md` trigger rows, "agent failure" in `systematic-debugging:3`. No dispatch.
- **`task` + agent/drone/subagent/worker/executor:** 100 raw hits; triaged outside the already-routed files, the only agent-shaped hits are: `click-path-audit:175` ("Agent 2: Dashboard (Tasks, Notes, Journal, Ideas)" — a page label in the read-only audit), `polish-pass/reference/impeccable-critique.md:17/:43/:45` (verification-only Assessments A/B, already OUT), `polish-pass/reference/lenses/optimize.md:65` (Web Workers — code parallelism), `agents/ecc-*-*.md:11` boilerplate ("Do not output executable code … unless required by the task"), `agents/deep-reasoner.md:14/:17` and `agents/fast-worker.md:16` (role descriptions dispatched BY the orchestrator), `agents/scout.md:14` (read-only role). No new dispatch.
- **`activate|set up|spin up|hand off|stand up` + agent/drone/subagent/worker/executor:** `orch-build-mvp:38` ("Stand up the first end-to-end slice" — scaffold language inside the routed skill), `feature-expansion:218` (ecc-planner "activates proactively" — a role note inside the routed skill, recording that the stock planner was NOT copied in), `effects-creative.md:106` ("rotors spin up" — UI copy), `ecc-gan-generator.md:39` ("Set up project scaffolding" — a step inside the factory drone's own role file, executed under the gan-build pointer), `ecc-gan-planner.md:109` (Evaluator "can consume directly" — a handoff, not a dispatch), role-file "When Activated" headings. No new dispatch.
- **`offload`:** 0 agent-shaped hits (same Reanimated-worklets result as #87-A).
- **Full `invoke(s) the X agent` triage:** exactly the same description-line hits as #87-A — `commands/python-review.md:2/:7` (python-reviewer, review-only), `commands/react-review.md:2/:7` (react-reviewer + typescript-reviewer, review-only), `commands/react-build.md:2/:7` (react-build-resolver — **now covered, §1**), `commands/fastapi-review.md:7` (fastapi-reviewer, review-only), `commands/react-review.md:28` (typescript-reviewer, review-only). No skill contains an "invoke(s) the X agent" dispatch line. `agents/ecc-gan-planner.md:44` is the re-routed Direction-source line (no `invoke the design-lead` instruction remains — see §6).
- **Full `dispatch` triage:** unchanged from #87-A — routed text (orchestrate step 4, feature-expansion Phase 1/Phase 4, gan-build loop, react-build step 6 re-dispatch), React `useReducer` dispatch, DOM `dispatchEvent`, `fireEvent`, hook-dispatcher plumbing, theme keyword lists. No new dispatch.
- **`launch` + agent/drone/subagent:** only two hits outside already-triaged files — `skills/council/SKILL.md:53` ("launched as fresh subagents" — the known analysis-only exclusion, §2(a)) and `agents/ecc-gan-evaluator.md:51` ("Launch Browser Testing" — a test step inside the evaluator role, not an agent dispatch).
- **`fan out` / `parallel agents`:** `rules/common-patterns.mdc:11` ("Use parallel agents to evaluate options" — analysis/planning only, no file writes, already OUT), `skills/click-path-audit/SKILL.md:167` ("Launch parallel agents per page" — read-only audit, already OUT), plus code parallelism (`Promise.allSettled` fan-out, parent-child fan-out, Archive.org fan-out) and UI copy (cards fan out). No new dispatch.

**The escape-class question, answered again.** Rounds 1–8 each found one live dispatch per escape class ("dispatch" in 83-A1, "invokes" in 86-A1). This round's aggressive verb hunt (including every verb the task named, plus `launch`, `fan out`, `parallel agents`, and the `task`/`order`/`deploy`/`trigger`/`assign` co-occurrence sweeps) found no fourth escape class: every remaining verb+agent pairing is inside a routed file, a review-only dispatch, a role description, or code parallelism. The only tree change since run 8 is the step 6 that 87-B1 itself specified, and it governs an already-covered dispatch rather than adding one.

## §3 — The 10-skill routing set: confirmed, no missing, no extra

`GLOBAL-ROUTING_F29` present in all 10 routing-set skills (counts are `grep -c` line counts in the skill's own SKILL.md unless noted):

| Skill | Routing present | Evidence |
|---|---|---|
| orchestrate | yes (2 lines, 3 occurrences) | GLOBAL-ROUTING block `SKILL.md:36` + step-4 factory bridge `:93` (token twice on :93) |
| orch-pipeline | yes (1) | factory paragraph `SKILL.md:62` |
| orch-build-mvp | yes (2) | pointer `SKILL.md:13` + step-5/merge text `:71` |
| orch-add-feature | yes (1) | pointer `SKILL.md:13` |
| orch-change-feature | yes (1) | pointer `SKILL.md:13` |
| orch-fix-defect | yes (1) | pointer `SKILL.md:13` |
| orch-refine-code | yes (2) | pointer `SKILL.md:13` + step-2 qualification `:35` |
| feature-expansion | yes (1 line, 2 occurrences) | factory paragraph `SKILL.md:139` (token twice on :139) |
| gan-style-harness | yes (1 line, 2 occurrences) | factory paragraph `SKILL.md:14` (token twice on :14) |
| design-taste-frontend | yes (1 in SKILL.md + 1 in redesign.md) | factory paragraph `redesign.md:68` + pointer `SKILL.md:455` |

Covered by reference (not in the set, governed by it): `rules/common-agents.mdc:26` factory line (8 listed agents only); `commands/gan-build.md:12` pointer; `commands/gan-design.md:10` pointer + `:19` pin; `commands/react-build.md:9` pointer + `:18` step 6 (**87-B1 verified fixed, §1**); `agents/ecc-gan-planner.md:44` re-route; `commands/orch-refine-code.md:33` mirror; `commands/orchestrate.md`, `orch-build-mvp.md`, `orch-add-feature.md`, `orch-change-feature.md`, `orch-fix-defect.md` route to the routed skills.
Counts re-confirmed: **67 skills / 45 agents / 48 rules / 55 commands**. `ui-ux-pro-max/` still **0 `_F29` tokens**; no `deepseek-`/`qwen-` model slugs in the built tree outside the GLOBAL-ROUTING forward-reference wording itself (0 hits after excluding GLOBAL-ROUTING lines — model pins unchanged, fix #30's work).

## §4 — Spot-check: the 9 reconciliations in MANIFEST §2(c) vs the live tree

All 9 spot-checked; all match the tree text.

1. **Belief-in-the-brief vs NO-GUESSING (5 copies):** `"pick the reasonable option"` = 5 hits, at `orch-pipeline:72`, `orch-build-mvp:70`, `feature-expansion:151`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92` (all five carry the identical carve-out plus tie-breaker, read verbatim). First-build carve-out: `"instead of NEEDS_CONTEXT"` = **0**; `"state the assumption you made and proceed"` = **0** tree-wide; scope sentence (`"for carrying out the briefed approach only"`) = 4 hits in `dispatch-prompt.md`; `agents/deep-reasoner.md:17` carries the rewritten NEEDS_CONTEXT line + identical NO-GUESSING bound + tie-breaker (read verbatim: "If the task is under-specified, return NEEDS_CONTEXT naming exactly what is missing — do not guess."). Matches.
2. **Merge-order fallback vs partition-by-boundary (3 sites):** the "applies only if partitioning failed" bridge present at all 3 — `orchestrate:93`, `feature-expansion:139`, `orch-build-mvp:71`. Matches.
3. **Feature-expansion Team shape vs factory cap:** Phase 4 paragraph (`feature-expansion:139`) states the factory queue under Cursor's cap; Team-shape paragraph at `:141` ("one implementer per feature, up to 4 in parallel", overlapping write scopes sequential) read in full. Matches.
4. **Feature-expansion brief format vs DIRECTOR-BRIEF:** item 2 names "the files explicitly OUT of scope"; item 4 split into 4a acceptance criteria and 4b verification steps; item 9 return format (status, changed files, verification evidence, residual risks, blockers). All read in full at `:140–160`. Matches.
5. **GAN evaluator vs VERIFY-MERGE:** ORCHESTRATOR-CHECK wiring order verified live by index arithmetic — EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484 (identical to #83-B through #87-A); planner-spec check at `gan-build.md:30` with cap "**at most two correction re-dispatches**"; `"at most one correction"` = **0** in the built tree; GENERATE block carries `Verification steps:` and `Return format:` (both confirmed present inside the `# GENERATE`–`# Wait for generator` slice by direct check); the old substitution sentence ("the evaluator pass IS the verify step") is absent from `gan-style-harness/SKILL.md`. Skill mirrors intact (`gan-style-harness:155` Architecture note — the orchestrator-check line, `:69`/`155` region — and the Scoring bullet). Matches.
6. **Orchestrate contract vs DIRECTOR-BRIEF:** seventh field `Verification steps:` in the contract core (`orchestrate:235`, "distinct from the acceptance check"); "files explicitly out of scope" in Constraints (`orchestrate:232`); no-drop rule present (`dispatch-prompt.md:4`: "delete no DIRECTOR-BRIEF field — a field with nothing to list is written as `none`, never deleted"). Matches.
7. **"Correction brief" constructed:** construction sentences at all seven sites — `feature-expansion:158`, `orch-pipeline:74`, orchestrate ladder `:252`, GAN ORCHESTRATOR-CHECK (`gan-build.md:63`), planner-spec 3a (`:30`), redesign `:68` (naming clause "naming the failed acceptance criterion and the required correction" present, verified by grep on the line), and react-build step 6 (`:18`, **new this round, §1**). "correction brief" counts per file: orchestrate 2, orch-pipeline 2, feature-expansion 2, redesign 1, gan-build 2, react-build 1 (the extra hits in the first three are the GLOBAL-ROUTING-block / factory-paragraph mentions, not additional construction sites). Matches — the manifest's "SEVEN sites" claim is now true in the tree.
8. **Slot refill harness-gate:** `"slots refill per wave"` = 5 hits — `orch-pipeline:62`, `feature-expansion:139`, `gan-style-harness:14`, `orchestrate:93`, `redesign.md:68`. Matches.
9. **Staged-vs-built drift by design:** the recorded drift lines are unchanged in the built tree (orchestrate `:100`/`:274`/`:281` agent-citation expansions, hackathon-mode `:38` CLI-subprocess wording — read) and verify29 check 7e (the narrow `_F29`-line identity check) passes — see §5. No contradiction with the tree found. (Not re-proven end to end this round; the fix16 anchor reasoning is unchanged from #80-A/#81-B.)

## §5 — GLOBAL-ROUTING block byte-identity (independent, not via the verifier)

- **Golden file:** `fix29/global-routing-block.txt` md5 `bdf1720f69f9b50e3791a14c68f5c5ea` — matches the value recorded by audits #80-A through #87-A.
- **orchestrate:** staged `new-skills/orchestrate/SKILL.md:36` is byte-identical to built `skills/orchestrate/SKILL.md:36` (line length 2285 chars each); both equal the golden file text (stripped).
- **hackathon-mode:** staged `new-rules/hackathon-mode.mdc:45` is byte-identical to built `rules/hackathon-mode.mdc:45` (line length 2287 chars each, the +2 being the `- ` list marker); both equal the golden file text after stripping the leading `"- "`.
- **Cross-file:** the orchestrate block and the hackathon-mode block are identical modulo the established DESIGNPKG-AUTO `- ` list-marker convention (verified by direct comparison after stripping the leading `"- "`: identical, length 2285 chars each).
- **85-B1 staged-vs-built identity (check 7e, independent):** `diff` of staged vs built `redesign.md` line 68 is clean (identical); the naming clause remains at `redesign.md:68`.
- Note on md5s: the per-line md5 of the orchestrate block line (`68206505…`) differs from the golden md5 because the golden md5 is over the whole block text including its trailing newline (2286 bytes), not a single line — the block-level comparison above is the correct check, and it matches all prior rounds.

## §6 — Checked and clean

- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **301/301, exit 0** (independently re-run; includes both 87-B1 checks, which pass; log at `/tmp/verify88A.log` agrees with `verify29-run16.log`).
- **87-B1 verified fixed** in full (§1) — step placement, all specified elements, `"correction brief"` count 1, fix29.py §5g anchor, verify29 guard present (verify29.py:1570–1574), MANIFEST §2(b) record present and §2(c)(7) seventh-site record present.
- **86-A1 still fixed** (react-build pointer `:9`, `_F29` count in the file = 1, all specified elements present).
- **84-A1 still fixed** (gan-design pointer `:10`, `_F29` count in the file = 1, step-0 pin `:19` present verbatim — the pointer names the inline-as-orchestrator reading and the loop deferral).
- **83-A2 still fixed** (planner `:44` re-route in place; old phrase `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"` = 0 hits).
- **GLOBAL-ROUTING block md5s:** golden `bdf1720f…` (staged = built, matching all prior rounds).
- **Census:** 10 skills; 17 files carry `GLOBAL-ROUTING_F29` (23 raw occurrences — see §2 reconciliation note); `"Factory routing (fix #29"` ×1 in exactly 12 files; counts 67/45/48/55.
- **All 9 §2(c) reconciliations match the live tree** (§4).
- **82-A2 cap alignment holds** (`"at most one correction"` 0×; `"at most two correction re-dispatches"` 1× at `gan-build.md:30`; react-build step 6 uses the same two-cap wording).
- **Model pins unchanged** (`ui-ux-pro-max` 0 `_F29`; no deepseek-/qwen- slugs outside the GLOBAL-ROUTING forward-reference wording).
- **Build run 9:** exit 0, fix29.py 31 changes, 0 errors (build-log-run9.txt:1247 `fix29: 31 change(s)`, :1279 `fix29: OK`; MANIFEST §3 records the same).
- **Call map:** not re-run (no fix adds a dispatch edge; #80-A's restore stands). Note: the react-build step 6 adds no dispatch edge — it governs an existing one (the re-dispatch is the correction path for the already-covered resolver dispatch) — so the fix28 map's standing is unaffected.

**Method note (not a finding, not counted):** my first `sed -n '59p'` read of `commands/prp-commit.md` appeared to contradict #87-A's correction (the visible prefix is the `git-workflow` draft line), because line 59 is one long line and the `ecc-commit-reviewer` clause sits past character 250. A full-line grep confirms #87-A's correction stands: `prp-commit.md:59` does name `ecc-commit-reviewer` ("check the drafted message against those norms before committing; it presents the message, it never runs `git commit` itself") — OUT, review-only. The disposition is unchanged.

**Observation (not a finding, not counted — carried forward from #86-A §6 / #87-A §6):** `agents/ecc-mle-reviewer.md:35–42` ("Reuse Existing Review Lanes") and `agents/ecc-build-error-resolver.md:114–118` contain conditional "Use X" lane pointers naming file-writing agents (`pytorch-build-resolver`, `build-error-resolver`, `refactor-cleaner`, `doc-updater`). These are referral notes inside read-only review/resolver roles, not executed dispatch steps in a workflow — the same class as `react-patterns:270`'s Related pointer. The named agents are governed when actually dispatched via `common-agents.mdc` (build-error-resolver, refactor-cleaner, doc-updater are listed) or routed skills. `pytorch-build-resolver` is not in the common-agents list and has no command launch site; no executed dispatch of it was found (its only mentions are the lane pointer and a call-map row). Revisit trigger unchanged: if a future fix routes review-lane escalation through factory drones, these pointers become dispatch edges and need the pointer treatment. Not a finding now because no dispatch is executed from them. The MANIFEST §2(b) react-build row already records this observation.

## Grep counts (for the record)

- Base dispatch pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files** (identical to #87-A; per-file counts identical).
- Whole-tree base pattern: **170 hits** (168 + 2 `README.md` documentation hits — unchanged from #87-A).
- `"Factory routing (fix #29"`: **12 files ×1** (unchanged).
- `GLOBAL-ROUTING_F29`: **17 files, 23 raw occurrences** (20 lines/sites — see §2 reconciliation note; #87-A reported 20 occurrences on a line/site count).
- `"slots refill per wave"`: **5 hits**.
- `"pick the reasonable option"`: **5 hits, all 5 carved + tie-breaker**.
- `"state the assumption you made and proceed"`: **0 hits tree-wide**.
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"at most one correction"`: **0 hits in the built tree**; `"at most two correction re-dispatches"`: **1 hit** (`commands/gan-build.md:30`); react-build step 6 uses the equivalent "at most two correction re-dispatches" wording.
- `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"`: **0 hits** (83-A2 fix still in place).
- `_F29` in `commands/react-build.md`: **1**; `"correction brief"` in `commands/react-build.md`: **1** (was 0 — 87-B1 fixed); `_F29` in `commands/gan-design.md`: **1**; `_F29` in `skills/ui-ux-pro-max/`: **0**.
- `"dispatch to the design skill"`: **2 sites only** (`commands/gan-build.md` step 0, `commands/gan-design.md:19`) — no third copy exists.
- GLOBAL-ROUTING block md5 (golden file): `bdf1720f69f9b50e3791a14c68f5c5ea` (staged = built).
- GAN wiring order indices: EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484.
- Verifier independently re-run: **301/301, exit 0**.

## Census table — every dispatch hit, in/out of scope + reason

Base-pattern files (49, case-insensitive). "Covered by reference" = governed by a routed skill's factory rules via an explicit pointer/pin, not carrying its own factory paragraph. Counts are case-insensitive line counts; all identical to #87-A.

| File (base hits) | Disposition | Reason |
|---|---|---|
| skills/orchestrate/SKILL.md (40) | IN SCOPE, routed | GLOBAL-ROUTING block :36 + step-4 factory bridge :93 |
| skills/feature-expansion/SKILL.md (26) | IN SCOPE, routed | Factory paragraph :139; Phase 1 brainstorm dispatch (:47, :55) is ideation only, no file writes; Phase 0 code-explorer recon (:49, :196) and the :198 table rows (build-error-resolver, architect, code-architect) are read-only/design inside the routed skill, and build-error-resolver + architect are in the common-agents governed list |
| skills/polish-pass/reference/impeccable-critique.md (11) | OUT | Verification-only Assessments A/B, "leave it as found" |
| skills/orchestrate/references/dispatch-prompt.md (7) | IN SCOPE, routed | Brief templates composing routed dispatches; carries Belief + first-build reconciliations |
| skills/orch-pipeline/SKILL.md (6) | IN SCOPE, routed | Factory paragraph :62 |
| skills/orch-build-mvp/SKILL.md (6) | IN SCOPE, routed | Pointer :13; `:87` readme-writer skill invocation is inline skill use inside the routed skill, not a drone dispatch |
| skills/council/SKILL.md (6) | OUT | Analysis/decisions only, no implementation work (`:53` "launched as fresh subagents" is the external-voices analysis dispatch) |
| rules/common-agents.mdc (5) | COVERED BY REFERENCE | Factory line :26; :42 launch is read-only 3-agent review. Governs the 8 listed agents only |
| rules/hackathon-mode.mdc (4) | IN SCOPE (carrier) | GLOBAL-ROUTING block :45 |
| commands/gan-build.md (4) | COVERED BY REFERENCE | Factory pointer :12; step-0 pin :26 |
| skills/orchestrate/references/call-map.md (3) | OUT | Documentation (hook table + trigger phrases) |
| skills/design-taste-frontend/SKILL.md (3) | IN SCOPE, routed | Redesign pointer :455; hero/finish review read-only |
| skills/verification-before-completion/SKILL.md (2) | OUT | Verification-only dispatch |
| skills/motionsites-web-builder/references/techniques/depth-and-interaction.md (2) | OUT | "Spawns thumbnails" = CSS animation, not agents |
| skills/design-taste-frontend/references/hallmark/references/gates.md (2) | OUT | Read-only hero/finish review gates |
| skills/design-taste-frontend/references/gate.md (2) | OUT | Read-only review gate |
| commands/pm2.md (2) | OUT | `child_process.spawn` — process spawn, not agent dispatch |
| commands/plan.md (2) | OUT | Planning only; explicitly "Do not delegate to a subagent by default"; second verification pass read-only; `:199` architect agent is planning-only and runtime-gated ("only when the local runtime exposes it") |
| commands/orchestrate.md (2) | COVERED BY REFERENCE | Routes to the routed orchestrate skill |
| commands/ecc-guide.md (2) | OUT | Documentation of the agents directory |
| agents/scout.md (2) | OUT | Dispatched BY orchestrator; read-only reconnaissance; dispatches nothing itself |
| commands/gan-design.md (2) | COVERED BY REFERENCE + PINNED | Step-0 pin :19; factory pointer :10 (84-A1 FIXED — now carries `_F29`); loop defers to gan-build Phase 2 |
| skills/ui-ux-pro-max/SKILL.md (1) | OUT | Directive reference ("Implementers execute component directives verbatim"), no dispatch of its own; 0 `_F29` |
| skills/strategic-compact/SKILL.md (1) | OUT | Policy/todo-tool, no agent dispatch |
| skills/react-native-patterns/SKILL.md (1) | OUT | Code-structure guidance, no agent dispatch |
| skills/polish-pass/reference/polish.md (1) | OUT | Verification-only independent re-score |
| skills/polish-pass/SKILL.md (1) | OUT | No implementation dispatch in SKILL.md |
| skills/orchestrate/references/design-inventory.md (1) | OUT | Reference table mentioning implementer briefs; no dispatch |
| skills/orch-refine-code/SKILL.md (1) | IN SCOPE, routed | Pointer :13 + step-2 factory-drone qualification |
| skills/orch-fix-defect/SKILL.md (1) | IN SCOPE, routed | Pointer :13 |
| skills/orch-add-feature/SKILL.md (1) | IN SCOPE, routed | Pointer :13 |
| skills/gan-style-harness/SKILL.md (1) | IN SCOPE, routed | Factory paragraph :14 |
| skills/design-taste-frontend/references/hallmark/references/redesign.md (1) | IN SCOPE, routed | Factory paragraph :68 (one subagent per page past three pages); naming clause still in place |
| skills/design-taste-frontend/references/copy-voice.md (1) | OUT | Fresh-reader subagent = read-only copy review |
| skills/ai-feature-spec/SKILL.md (1) | OUT | "Invoke this skill" = skill invocation, no agent dispatch |
| rules/ponytail.mdc (1) | OUT | Subagent return-message contract reference; no dispatch |
| rules/common-development-workflow.mdc (1) | OUT / COVERED BY REFERENCE | Base hit is the planning delegation ("use the architect agent when the user explicitly asks you to delegate planning"), user-gated, planning-only; the additional "Use X agent" lines (`:19` tdd-guide, `:26` code-reviewer) name agents in the alwaysApply `common-agents.mdc` governed list, so they are covered by that file's :26 factory line |
| rules/common-code-review.mdc (1) | OUT | Link text "Agent delegation"; agent table (`:66`, `:85`) is review-only |
| commands/plan-prd.md (1) | OUT | Delegates decomposition to `/plan` — planning, not implementation |
| commands/orch-refine-code.md (1) | COVERED BY REFERENCE | Command mirror of the skill's step-2 qualification |
| commands/orch-build-mvp.md (1) | COVERED BY REFERENCE | Routes to the routed skill |
| commands/astra-review.md (1) | OUT | Blind review, read-only |
| agents/fast-worker.md (1) | OUT | Role description; dispatched BY orchestrator |
| agents/ecc-typescript-reviewer.md (1) | OUT | Code guidance re `child_process` spawn + review role |
| agents/ecc-gan-planner.md (1) | COVERED BY REFERENCE | Launched by `/gan-build`; fallback re-routed per 83-A2 |
| agents/ecc-gan-generator.md (1) | OUT | Role description; launched as factory drone under gan-build pointer |
| agents/ecc-gan-evaluator.md (1) | OUT | Role description; "Launch Browser Testing" is a test step, not agent dispatch |
| agents/ecc-chief-of-staff.md (1) | OUT | Role file; launch notes triaged in prior rounds, no implementation dispatch |
| agents/deep-reasoner.md (1) | OUT | Role description; dispatched BY orchestrator; :17 carries the NEEDS_CONTEXT bound |

New-verb-only sites (no base-pattern hit; found by the fresh sweeps in §2 and prior rounds):

| Site | Disposition | Reason |
|---|---|---|
| **commands/react-build.md:7 (+ description :2), pointer :9, step 6 :18** | **IN SCOPE, COVERED — 86-A1 + 87-B1 VERIFIED-FIXED (§1)** | **Invokes `react-build-resolver` for minimal surgical file edits; pointer :9 names single-task factory drone, director brief (all 7 fields), no-guessing, orchestrator verification (re-run build as evidence, not verdict), COST-AWARE; `_F29` count 1; step 6 now performs the orchestrator verification against the brief's acceptance criteria with a correction-brief re-dispatch path capped at two** |
| commands/fastapi-review.md:7, python-review.md:7, react-review.md:7 (+ :2 descriptions) | OUT | Invoke review-only agents (fastapi/python/react reviewer) — read-only |
| commands/react-review.md:28 | OUT | "invoke `typescript-reviewer` agent … directly" — review-only |
| commands/prp-commit.md:59 | OUT (record corrected in #87-A, re-verified this round — see §6 method note) | "have the `ecc-commit-reviewer` agent … check the drafted message" — commit-message review only; "it presents the message, it never runs `git commit` itself" — read-only |
| commands/review-pr.md:2 + Steps | OUT | Multi-perspective PR review using specialized review agents — read-only |
| commands/code-review.md:2 | OUT | Step-by-step PRP checklist review; multi-agent pass defers to /review-pr — read-only |
| commands/feature-dev.md:17, :29, :41 | OUT | code-explorer (analysis), code-architect (design), code-reviewer (review) only; implementation phase inline — no implementation dispatch |
| commands/build-fix.md | OUT | Inline fix loop (Read/Edit tools), no agent dispatch |
| commands/prp-implement.md, prp-plan.md, prp-prd.md, prp-pr.md | OUT | No agent/dispatch/invoke/launch/spawn lines — inline workflow (the only "agent" hits are the "PRPs-agentic-eng" attribution) |
| commands/react-test.md:265 | OUT | Related pointer to review/TDD agents — reference, not a dispatch |
| commands/react-test.md:51 | OUT | "Agent:" example-session label, not a dispatch |
| commands/loop-start.md:2 | OUT | Loop-setup description (prints commands to launch/monitor a loop) |
| commands/quality-gate.md:44–45 | OUT | Hook dispatcher script registry — observability plumbing, not agent dispatch |
| commands/epic-claim.md, epic-decompose.md, epic-publish.md, epic-review.md, epic-sync.md, epic-unblock.md, epic-validate.md, test-coverage.md, update-docs.md, refactor-clean.md, resume-session.md, skill-create.md, update-codemaps.md, issue-review.md, learn.md, model-route.md, checkpoint.md, auto-update.md, setup-pm.md, pr.md | OUT | No agent/dispatch/invoke/launch/spawn lines at all |
| commands/astra-review.md:24 | OUT | Blind review dispatched to deep-reasoner as fresh subagent — read-only |
| commands/orch-add-feature.md:7, orch-change-feature.md:7, orch-fix-defect.md:7, orch-build-mvp.md:7, orch-refine-code.md:7 | COVERED BY REFERENCE | "Manually launch the orchestrator" — user launches the routed orchestrator skill |
| commands/orch-refine-code.md:26, :33 | COVERED BY REFERENCE | refactor-cleaner sweep qualified as single-task factory drone with director brief |
| commands/gan-build.md:27, :39, :52 | COVERED BY REFERENCE | Planner/generator/evaluator launches under the :12 factory pointer |
| commands/pm2.md:103 | OUT | `child_process.spawn` — process spawn |
| commands/harness-audit.md:13, :83 | OUT | "agents" as a scope value (`repo|hooks|skills|commands|agents`) — a CLI scope flag, not a dispatch |
| rules/common-patterns.mdc:11 | OUT | Parallel agents to evaluate options — analysis/planning only, no file writes |
| rules/common-agents.mdc:42 | OUT | "Launch 3 agents in parallel" — security/performance/type-checking, read-only, governed in-file by the :26 factory line + :38 read-only rule |
| rules/common-performance.mdc:35 | COVERED BY REFERENCE | "Use **build-error-resolver** agent" in Build Troubleshooting — an implementation dispatch instruction, but build-error-resolver is in the alwaysApply `common-agents.mdc` governed list, so the :26 factory line governs it |
| rules/common-development-workflow.mdc:19, :26 | COVERED BY REFERENCE | "Use **tdd-guide** agent" (TDD, writes tests/code) and "Use **code-reviewer** agent immediately after writing code" — both named agents are in the alwaysApply `common-agents.mdc` governed list, so the :26 factory line governs them |
| rules/common-code-review.mdc:66, :85 | OUT | Agent table / "Use appropriate agent for detailed review" — review-only |
| skills/browser-qa/SKILL.md:22 | OUT | Handoff to `systematic-debugging` (no agent-dispatch lines of its own); browser-qa is verification-only |
| skills/pitch-deck-video/references/openmontage/montage.md:108 | OUT | Archive.org-only fan-out = research/media gathering |
| skills/track-picker/SKILL.md:3 | OUT | Generates an integration plan — planning only |
| skills/polish-pass/reference/impeccable-onboard.md:243 | OUT | Handoff to `/impeccable polish` — verification/polish pass |
| skills/orch-pipeline/SKILL.md:16 | IN SCOPE | "Invoke an operation skill" — routed skill invoking routed skills |
| skills/orch-pipeline/SKILL.md:71 | IN SCOPE | "drive each task through the `tdd-guide` agent" — inside the routed skill, under its factory paragraph |
| skills/orchestrate/SKILL.md:93 | IN SCOPE | "each implementer brief names `tdd-guide` agent" — inside the routed skill, under the GLOBAL-ROUTING block |
| skills/verification-loop/SKILL.md:15 | OUT | "Invoke this skill" — skill invocation; verification-only |
| skills/delivery-gate/SKILL.md:41 | OUT | Hook-install note, not a dispatch |
| skills/orch-build-mvp/SKILL.md:87 | IN SCOPE | "invoke `readme-writer` to write/update the README" — inline skill invocation inside the routed skill, not a drone dispatch; governed by the skill's :13 pointer |
| agents/ecc-react-reviewer.md:33, :79 | OUT | Invoke review agents on a PR — read-only review |
| agents/ecc-a11y-architect.md:35 | OUT | Self-instruction to the role itself, not a dispatch of another agent |
| agents/ecc-code-reviewer.md:24, ecc-python-reviewer.md:18, ecc-seo-specialist.md:18, ecc-typescript-reviewer.md:18 | OUT | "When invoked:" boilerplate — the role being invoked, not dispatching |
| agents/ecc-mle-reviewer.md:35–42 | OUT (see §6 observation) | Conditional "Use X" lane pointers (incl. file-writing agents) inside a read-only review role — referral notes, not executed dispatch |
| agents/ecc-build-error-resolver.md:114–118 | OUT (see §6 observation) | Conditional escalation pointers ("Code needs refactoring → use `refactor-cleaner`") — referral notes, not executed dispatch |
| agents/ecc-docs-lookup.md:3, ecc-rag-pipeline-reviewer.md:3 | OUT | "Invoke for docs/API/setup questions" / "Invoke when the user builds…" — trigger phrases for the role itself, not a dispatch of another agent |
| skills/react-patterns/SKILL.md:270, skills/react-performance/SKILL.md:568 | OUT | Related pointer naming `react-build-resolver` for build/bundler errors — reference, not a dispatch instruction |
| skills/click-path-audit/SKILL.md:167 | OUT | "Launch parallel agents per page" — read-only audit |
| skills/click-path-audit/SKILL.md:175 | OUT | "Agent 2: Dashboard (Tasks, Notes, Journal, Ideas)" — a page label in the read-only audit |
| skills/orchestrate/SKILL.md:103, :205, :209, :211, :213, :221, :233, :260, :264; references/patterns.md:13, :26; dispatch-prompt.md:23 | IN SCOPE | Inside the routed skill / routed templates — fan-out, dispatch-composition and handoff rules, not new edges |
| skills/orchestrate/SKILL.md:93, :250, :400 | IN SCOPE | Step-4 factory bridge, NEEDS_CONTEXT re-dispatch, Gotchas fallback (dispatched through dispatch-prompt templates) |
| skills/orchestrate/SKILL.md:201 | IN SCOPE | "Dispatch scout" — read-only reconnaissance dispatched by the orchestrator under the factory rules |
| skills/orch-build-mvp/SKILL.md:34, :87 | IN SCOPE | `/demo` dispatch — user-invoked video command, dispatched by the orchestrator under the factory rules via dispatch-prompt templates |
| skills/feature-expansion/SKILL.md:47, :55 | OUT (skill in set) | "Dispatch four brainstorm subagents in parallel" — Phase 1 ideation, no file writes; skill routed via Phase 4 |
| skills/feature-expansion/SKILL.md:49, :196 | OUT (skill in set) | "Use `code-explorer` agent … (agent — spawn as a subagent) if the codebase is unfamiliar" — read-only reconnaissance, no file writes; inside the routed skill |
| skills/feature-expansion/SKILL.md:198 | IN SCOPE (skill in set) | Table rows naming `build-error-resolver` (spawn as subagent for build errors during implementation), `architect` / `code-architect` (design questions) — inside the routed skill under its Phase 4 factory paragraph; build-error-resolver and architect are also in the common-agents governed list |
| skills/orch-build-mvp/SKILL.md:38, skills/orch-pipeline/SKILL.md:70 | IN SCOPE | "Stand up the first end-to-end slice" — scaffold language inside routed skills, not agent dispatch |
| skills/design-taste-frontend/references/hallmark/PROVENANCE.md:30; skills/polish-pass/reference/impeccable-PROVENANCE.md; skills/polish-pass/reference/lenses/*.md | OUT | Provenance notes / verification lenses — no dispatch |
| commands/sessions.md:294 | OUT | Parallel tmux/worktree runs — session bookkeeping |
| commands/sessions.md:19 | OUT | "Operator-surface context for a swarm" — session bookkeeping |
| skills/react-performance/SKILL.md:243 | OUT | "Parallelize nested fetches with Promise.all" — code parallelism |
| skills/react-performance/SKILL.md:96 | OUT | "kick off all promises" — promise language, not agent dispatch |
| skills/python-patterns/SKILL.md:457–479, skills/typescript-patterns/SKILL.md:390–412, skills/vite-patterns/SKILL.md:335, skills/e2e-testing/SKILL.md:111, skills/production-audit/SKILL.md:68 | OUT | ThreadPool/ProcessPoolExecutor, worker pools, webworker target, test-runner workers, background workers — code parallelism |
| skills/frontend-patterns/SKILL.md:282–293 | OUT | `dispatch: Dispatch<Action>` / `useReducer` — React state dispatch, not agent dispatch |
| skills/frontend-slides/SKILL.md:106, :185; skills/motion-advanced/SKILL.md:444, :446; skills/tdd-workflow/SKILL.md:22; skills/orchestrate/SKILL.md:85, :239, :264, :369, :394; skills/orchestrate/references/dispatch-prompt.md:16, :78; skills/orch-pipeline/SKILL.md:109, :111; skills/feature-expansion/SKILL.md:176, :216; skills/pitch-deck-video/SKILL.md:232, :269, :836; skills/polish-pass/SKILL.md:102; skills/ui-ux-pro-max/SKILL.md:264, :348; skills/systematic-debugging/SKILL.md:20; commands/epic-validate.md:7; commands/plan-prd.md:2, :67; commands/save-session.md:14; agents/ecc-gan-evaluator.md:134; agents/ecc-gan-planner.md:46, :109; agents/ecc-homelab-architect.md:31; agents/ecc-rag-pipeline-reviewer.md:54, :56 | OUT | "Handoff" as skill-to-skill transfer, documentation handoff, or design copy — no agent dispatch in any of them |
| rules/arkts-hooks.mdc, react-native-patterns.mdc, react-patterns.mdc, react-testing.mdc, web-hooks.mdc, web-patterns.mdc; skills/frontend-patterns/SKILL.md, motion-patterns/SKILL.md, react-patterns/SKILL.md, react-testing/SKILL.md, mobile-ship/**, pitch-deck-video/**, app-scaffold/reference/**, e2e-testing/SKILL.md, hackathon-pitch/**, frontend-slides/** | OUT | "Launch"/"parallel"/"isolated" as product launch, code parallelism, or design-pattern language — no agent dispatch in any of them |
| skills/feature-expansion/SKILL.md:218 | OUT (skill in set) | ecc-planner "activates proactively" — a role note recording the stock planner was NOT copied in; inside the routed skill |
| agents/ecc-gan-generator.md:39 | IN SCOPE (covered) | "Set up project scaffolding" — a step inside the factory drone's own role file, executed under the gan-build :12 pointer |
