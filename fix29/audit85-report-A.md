# Audit #85-A — Fix #29 (adaptable orchestration): routing coverage / dispatch census, round 6

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** routing coverage / dispatch census — verify the audit #84-A fix (84-A1) landed correctly in the built tree; re-derive the dispatcher set from scratch with fresh verb hunts; check the 10-skill routing set; spot-check the 9 MANIFEST §2(c) reconciliations; independently confirm GLOBAL-ROUTING byte-identity staged vs built.
**Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md` (§2 in full, incl. the §2(b) gan-design + planner rows and all 9 §2(c) reconciliations), `fix29/audit84-report-A.md`, `fix29/fix29.py` (§5e/§5f), `fix29/verify29.py` (84-A1 checks at :1472–1477), `fix29/build-log-run6.txt`, `fix29/verify29-run10.log`.
**Method:** re-checked the 84-A1 file:line in the built tree (`hackathon-ecc/`); re-ran `python3 fix29/verify29.py` independently; grepped the whole built tree (`skills/`, `rules/`, `commands/`, `agents/`, `*.md`/`*.mdc`) for the base pattern plus fresh verb sweeps (`spin up`/`kick off`/`fire off`/`offload`/`enlist`/`recruit`/`bring in`/`call in`, `task/assign … agent/drone/worker`, full `dispatch` triage, full `agents/` verb sweep); read every new hit in context. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.

## Verdict: PASS — 0 blocking, 0 minor

84-A1 is verified fixed in full — the factory pointer is in `commands/gan-design.md:10`, placed exactly where the fix specified (after the arg-parse block, before `## GAN-Style Design Harness`), it names the step-0 inline reading and defers the loop to the gan-build pointer, the file now carries a `_F29` token, the MANIFEST §2(b) record covers it, and verify29 now guards both the pointer line and token presence. No new live implementation dispatch was found anywhere in the fresh hunt, the 10-skill routing set is intact with no missing or extra member, all 9 §2(c) reconciliations match the live tree, and GLOBAL-ROUTING is byte-identical staged vs built. Nothing in this round meets the blocking or minor bar, and no finding is invented to avoid PASS.

## Findings

None. (No numbered findings — the tree is clean on this half's scope.)

## §1 — #84-A disposition: the finding re-checked

| #84-A | Status | Evidence |
|---|---|---|
| 84-A1 (minor): `commands/gan-design.md` still carries 0 `_F29` tokens | **VERIFIED-FIXED** | `commands/gan-design.md:10` now carries the factory pointer verbatim: "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the design-lead is invoked inline as the orchestrator in Setup step 0 (not spawned as a drone — a spawned execution must carry a director brief); the generator/evaluator loop below runs as factory drones per the `/gan-build` pointer, each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria." Placement is exactly as specified: arg-parse block ends `:8` (blank `:9`), pointer `:10` (blank `:11`), `## GAN-Style Design Harness` `:12`. `grep -c "_F29" commands/gan-design.md` = **1** (was 0). The pointer mirrors `gan-build.md:12` in form (same bold lead, same seven-field brief enumeration, same no-guessing + verify-against-acceptance-criteria tail) with the two required adaptations: step-0 inline reading named instead of a planner/generator/evaluator enumeration, and the loop deferred to "the `/gan-build` pointer" instead of `gan-style-harness`. The step-0 parenthetical is still present verbatim at `:19` (line shifted from `:17` by the pointer insertion — see the observation in §6). MANIFEST §2(b) `commands/gan-design.md` row now records the 84-A1 fix explicitly ("fix29.py §5e now also adds a one-line factory pointer mirroring gan-build.md:12 after the arg-parse block (step-0 inline reading named, loop defers to the gan-build pointer); verify29 asserts the pointer line and `_F29` presence in the file"). verify29.py:1475–1477 now asserts both halves: the pointer line (`count(...) == 1`) and `"_F29" in _gd`. fix29.py §5e implements the pointer exactly as specified (anchor on the `--pass-threshold` line + `## GAN-Style Design Harness` header, pointer inserted between). |

## §2 — Fresh hunt: dispatch census re-derived from scratch

Base pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files**. This reconciles exactly with #84-A's 167/49 once the grep case is pinned down: #84-A's counts are **case-insensitive** — my case-sensitive re-count is 157, and case-insensitive is 168. The +1 vs #84-A is exactly the one-line gan-design pointer, whose "not spawned as a drone" adds one "spawned" hit (gan-design goes 1 → 2 base hits; every other file's count is identical to #84-A's census table). Whole-tree base pattern: **170 hits** (168 + 2 `README.md` documentation hits), consistent with #84-A's 169 + 1 pointer hit. No other tree change since run 5 exists (build run 6 = 29 changes, 28 + the §5e pointer; the 84-B fixes were verifier-only), so no count delta comes from new dispatch text.

New-verb sweeps (all `*.md`/`*.mdc`, skills/rules/commands/agents), each read in context:

- **`spin up|kick off|fire off|offload|enlist|recruit|bring in|call in`:** 0 agent-shaped hits. `react-performance:96` ("kick off all promises"), `typescript-patterns:281` ("call in a stack"), `click-path-audit:34` ("every function call in the handler"), `integration:8, :85` ("working call in the demo path", "a slow call in a timed slot"), `effects-creative.md:33, :106` ("rotors that spin up" — design copy), `mobile-ship android-store.md:13` ("tester recruitment" — human testers), `ui-ux-pro-max:359` ("never fire off-screen" — animation), `react-native-performance.mdc:33` ("offload to Reanimated worklets" — code offload), `react-coding-style.mdc:86` ("inline the call instead"). All code/design/process language, no agent dispatch.
- **`task (the|a|an) … agent | assign … agent|drone|worker`:** 1 hit, `orchestrate/references/patterns.md:13` ("assign non-overlapping scopes" — pattern description inside the routed skill, fan-out guard, not a new edge).
- **Full `dispatch` triage (case-insensitive, all hits not already covered):** no new dispatch edge. Residuals are all previously triaged: `frontend-patterns:282–293` (`Dispatch<Action>`, `useReducer` — React code), `react-testing:93` (`fireEvent` dispatches a synthetic event), `orch-build-mvp:34, :87` (`/demo` dispatch — user-invoked video command, dispatched by the orchestrator under the factory rules via the dispatch-prompt templates, inside the routed skill), `feature-expansion:47, :55` ("Dispatch four brainstorm subagents in parallel" — Phase 1 ideation, no file writes; analysis-only, and the skill is in the routing set via Phase 4 in any case), `feature-expansion:194` (call-map row, documentation), `design-taste-frontend` asset READMEs / `effects-objects.md:167` (`dispatchEvent` — DOM code), `themes/newsprint.md:9` ("dispatch" as a theme keyword), `orchestrate:31, :62, :68, :76, :87, :89, :103, :137, :187, :201, :215, :246, :250, :335, :352` (routing/model-hierarchy/dispatch-composition language inside the routed skill, including "dispatch scout" at `:201` — scout is read-only reconnaissance dispatched by the orchestrator under the factory rules), `orchestrate/references/call-map.md:33, :40, :52` (documentation of dispatch paths).
- **`agents/*.md` role files, dispatch verbs (`dispatch|launch|spawn|delegate|invoke`):** clean. `ecc-a11y-architect.md:35` ("Invoke specific logic to generate semantic code") — self-instruction to the role itself, out (as in prior rounds). `ecc-react-reviewer.md:33, :79` — read-only review agents, out. `ecc-gan-planner.md:44` — the 83-A2 site, re-routed (§1 of #84-A, still in place — see §4). `ecc-typescript-reviewer.md:44` — code guidance about `exec`/`spawn`, out. `scout.md:3` — role description ("before work is delegated"), read-only, dispatched BY the orchestrator. `ecc-code-reviewer.md:24`, `ecc-python-reviewer.md:18`, `ecc-rag-pipeline-reviewer.md:3`, `ecc-seo-specialist.md:18`, `ecc-typescript-reviewer.md:18` — "When invoked:" boilerplate / description text, no dispatch of another agent.
- **Reference files:** no new dispatch. The only in-scope reference dispatch remains `redesign.md:68` (routed). All other reference hits are the previously triaged verification/review/copy sites.

**No new implementation dispatch found.** The only dispatch-shaped line added since #84-A is the 84-A1 pointer itself — routing text, not a new dispatch edge. The call map was not re-run (no fix adds a dispatch edge; #80-A's restore stands).

## §3 — The 10-skill routing set: confirmed, no missing, no extra

`GLOBAL-ROUTING_F29` present in all 10 routing-set skills plus `rules/hackathon-mode.mdc`; tree-wide **16 files, 19 occurrences** (was 15/18 in #84-A; +1 file / +1 occurrence is exactly the gan-design pointer). `"Factory routing (fix #29"` occurs ×1 in exactly **11 files** (was 10; +1 is gan-design). Counts re-confirmed: **67 skills / 45 agents / 48 rules / 55 commands**. `ui-ux-pro-max/` still **0 `_F29` tokens**; no `deepseek-`/`qwen-` model slugs in the built tree outside the GLOBAL-ROUTING forward-reference wording itself (model pins unchanged — fix #30's work, not this fix's).

| Skill | Routing present | Evidence |
|---|---|---|
| orchestrate | yes | GLOBAL-ROUTING block `SKILL.md:36` + step-4 factory bridge `:93` |
| orch-pipeline | yes | factory paragraph `SKILL.md:62` |
| orch-build-mvp | yes | pointer `SKILL.md:13` |
| orch-add-feature | yes | pointer `SKILL.md:13` |
| orch-change-feature | yes | pointer `SKILL.md:13` |
| orch-fix-defect | yes | pointer `SKILL.md:13` |
| orch-refine-code | yes | pointer `SKILL.md:13` + step-2 qualification `:34` |
| feature-expansion | yes | factory paragraph `SKILL.md:139` |
| gan-style-harness | yes | factory paragraph `SKILL.md:14` |
| design-taste-frontend | yes | factory paragraph `redesign.md:68` + pointer `SKILL.md:455` |

Covered by reference (not in the set, governed by it): `rules/common-agents.mdc:26` factory line; `commands/gan-build.md:12` pointer; `commands/gan-design.md:10` pointer + `:19` pin; `agents/ecc-gan-planner.md:44` re-route; `commands/orch-refine-code.md:33` mirror; `commands/orchestrate.md`, `orch-build-mvp.md`, `orch-add-feature.md`, `orch-change-feature.md`, `orch-fix-defect.md` route to the routed skills. MANIFEST §2(b) records all three design-direction sites (gan-build:26, gan-design step 0, planner fallback).

## §4 — Spot-check: the 9 reconciliations in MANIFEST §2(c) vs the live tree

All 9 spot-checked; all match the tree text.

1. **Belief-in-the-brief vs NO-GUESSING (5 copies):** `"pick the reasonable option"` = 5 hits, all carrying the identical carve-out ("applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified…") plus the tie-breaker ("When in doubt which side… / When in doubt, return the question"): `orch-pipeline:72`, `orch-build-mvp:70`, `feature-expansion:151`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92` (read in full at all five sites; the two `dispatch-prompt.md` copies carry the carve-out inline, the second in parenthetical form). First-build carve-out: `"instead of NEEDS_CONTEXT"` = **0**; `"state the assumption you made and proceed"` = **0** tree-wide; scope sentence ("for carrying out the briefed approach only…") at all 4 drone-side sites (`dispatch-prompt.md:96, :117, :212, :236`); tie-breaker in the governing carve-out (`dispatch-prompt.md:52`); `agents/deep-reasoner.md:17` carries the rewritten NEEDS_CONTEXT line + identical NO-GUESSING bound + tie-breaker (read verbatim). Matches.
2. **Merge-order fallback vs partition-by-boundary (3 sites):** the "applies only if partitioning failed" bridge present at all 3 — `orchestrate:93`, `feature-expansion:139`, `orch-build-mvp:71`. Matches.
3. **Feature-expansion Team shape vs factory cap:** Phase 4 paragraph (`feature-expansion:139`) states the factory queue under Cursor's cap (read in full; "one implementer per feature, up to 4 in parallel" with the harness-gate clause). Matches.
4. **Feature-expansion brief format vs DIRECTOR-BRIEF:** format item 2 names "the files explicitly OUT of scope (named; `none` if genuinely none)"; item 4 split into 4a acceptance criteria (`:148`) and 4b verification steps (`:149`); item 9 return format (`:154`). Matches (items read in full).
5. **GAN evaluator vs VERIFY-MERGE:** ORCHESTRATOR-CHECK wiring order verified live by index arithmetic — EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484 (same indices #83-B/#84-A recorded); planner-spec check at `gan-build.md:30` with cap "**at most two correction re-dispatches**"; `"at most one correction"` = **0** in the built tree; GENERATE block carries `Verification steps:` (TDD tests + acceptance criteria, output pasted) and `Return format:` (status first, then files changed, test output, concerns) plus the files-out-of-scope line — 7/7 present. Skill mirrors intact (`gan-style-harness:69` Architecture note, `:155` Scoring bullet). Matches.
6. **Orchestrate contract vs DIRECTOR-BRIEF:** seventh field `Verification steps:` in the contract core (`orchestrate:235`, read in full: "Verification steps: <the exact steps/commands the executor runs to verify — distinct from the acceptance check>") and templates; "files explicitly out of scope" in Constraints; no-drop rule present (`dispatch-prompt.md:4`: "delete no DIRECTOR-BRIEF field — a field with nothing to list is written as `none`, never deleted"). Matches.
7. **"Correction brief" constructed:** construction sentences in all four fix loops — `feature-expansion:158`, `orch-pipeline:74`, orchestrate ladder `:252`, GAN ORCHESTRATOR-CHECK (`gan-build.md:63`) + planner-spec 3a (`:30`). Matches.
8. **Slot refill harness-gate:** `"slots refill per wave"` = 5 hits — `orch-pipeline:62`, `feature-expansion:139`, `gan-style-harness:14`, `orchestrate:93`, `redesign.md:68`. Matches.
9. **Staged-vs-built drift by design:** not re-proven end to end this round (fix16 anchor); the recorded drift lines are unchanged in the built tree and verify29 check 7e (the narrow `_F29`-line identity check) passes — see §5. No contradiction with the tree found.

## §5 — GLOBAL-ROUTING block byte-identity (independent, not via the verifier)

- **orchestrate:** staged `new-skills/orchestrate/SKILL.md:36` md5 `bdf1720f69f9b50e3791a14c68f5c5ea` = built `skills/orchestrate/SKILL.md:36`; `diff` clean.
- **hackathon-mode:** staged `new-rules/hackathon-mode.mdc:45` md5 `39a22e9247be839a841ffbea3ad19918` = built `rules/hackathon-mode.mdc:45`; `diff` clean.
- Cross-file `diff` (hackathon-mode's leading `"- "` list marker stripped) clean — the two blocks are identical modulo the established DESIGNPKG-AUTO marker convention.
- Both match the values recorded by audits #80-A/#81-A/#82-A/#83-A/#84-A. No byte-identity break. (Note for the next auditor: the staged sources live at `~/workspace/hackathon-plugin/new-skills/` and `~/workspace/hackathon-plugin/new-rules/`, not under `hackathon-ecc/`.)

## §6 — Checked and clean

- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **289/289, exit 0** (independently re-run; includes the two new 84-A1 checks, both PASS in `verify29-run10.log`).
- **84-A1 verified fixed** in full (§1) — pointer placement, token presence, MANIFEST record, verifier guards.
- **83-A2 still fixed** (§4 via planner `:44` re-read; old phrase `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"` = 0 hits).
- **GLOBAL-ROUTING block md5s:** orchestrate `bdf1720f…`, hackathon-mode `39a22e92…` (staged = built, matching all prior rounds).
- **Census:** 10 skills; 16 files carry `GLOBAL-ROUTING_F29` (19 occurrences); `"Factory routing (fix #29"` ×1 in exactly 11 files; counts 67/45/48/55.
- **All 9 §2(c) reconciliations match the live tree** (§4).
- **Excluded set still holds** (council, click-path-audit, verification-only dispatch, polish-pass reference files, `common-patterns.mdc:11`, `common-agents.mdc:42`); newly triaged this round — feature-expansion Phase 1 brainstorm dispatch (`:47, :55`, ideation-only), `orchestrate:201` "dispatch scout" (read-only, inside the routed skill), `/demo` dispatches from `orch-build-mvp:34, :87` (orchestrator-dispatched under the factory rules), `ecc-a11y-architect.md:35` self-instruction, `ecc-react-reviewer.md:33` read-only review invocation — all out of scope with reasons in §2 / the census table.
- **82-A2 cap alignment holds** (`"at most one correction"` 0×; `"at most two correction re-dispatches"` 1× at `gan-build.md:30`).
- **Model pins unchanged** (`ui-ux-pro-max` 0 `_F29`; no deepseek-/qwen- slugs outside the GLOBAL-ROUTING forward-reference wording).
- **Build run 6:** exit 0, fix29.py 29 changes, 0 errors (build-log-run6.txt); the only tree change vs run 5 is the §5e gan-design pointer (the 84-B fixes were verifier-only).
- **Call map:** not re-run (no #84 fix adds a dispatch edge; #80-A's restore stands).

**Observation (not a finding):** the gan-design step-0 parenthetical moved from `:17` to `:19` when the pointer was inserted at `:10`. MANIFEST §3's historical entries (and audit #83-A/#84-A) cite `:17`, which was correct for the run-5 tree; the §2(b) row itself cites no line number for gan-design, so the live record is accurate. Future cites should use `:19` for the parenthetical and `:10` for the pointer. Also for the next auditor: the base-pattern counts in rounds 1–5 are case-insensitive (a case-sensitive re-count gives 157, not 167 — the delta is capital-`D` "Delegate" headings in `orchestrate:225, :362`, `verification-before-completion:74, :94`, and the `Implementers execute … verbatim` lines in `ui-ux-pro-max:264`, `polish-pass:102`, `design-taste-frontend:413, :455`).

## Grep counts (for the record)

- Base dispatch pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files** (167 in #84-A + 1 = the gan-design pointer's "spawned"; case-sensitive count is 157 — see §6 observation).
- Whole-tree base pattern: **170 hits** (168 + 2 `README.md` documentation hits).
- `"Factory routing (fix #29"`: **11 files ×1** (was 10; +1 gan-design).
- `GLOBAL-ROUTING_F29`: **16 files, 19 occurrences** (was 15/18; +1 gan-design).
- `"slots refill per wave"`: **5 hits**.
- `"pick the reasonable option"`: **5 hits, all 5 carved + tie-breaker**.
- `"state the assumption you made and proceed"`: **0 hits tree-wide**.
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"at most one correction"`: **0 hits in the built tree**; `"at most two correction re-dispatches"`: **1 hit** (`commands/gan-build.md:30`).
- `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"`: **0 hits** (83-A2 fix still in place).
- `_F29` in `commands/gan-design.md`: **1** (was 0 — 84-A1 fixed); `_F29` in `skills/ui-ux-pro-max/`: **0**.
- `"dispatch to the design skill"`: **2 sites only** (`commands/gan-build.md:26`, `commands/gan-design.md:19`) — no third copy exists.
- GLOBAL-ROUTING block md5s: orchestrate `bdf1720f69f9b50e3791a14c68f5c5ea`, hackathon-mode `39a22e9247be839a841ffbea3ad19918` (staged = built).
- GAN wiring order indices: EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484.

## Census table — every dispatch hit, in/out of scope + reason

Base-pattern files (49, case-insensitive). "Covered by reference" = governed by a routed skill's factory rules via an explicit pointer/pin, not carrying its own factory paragraph. Counts are case-insensitive line counts; deltas vs #84-A are noted where they occur.

| File (base hits) | Disposition | Reason |
|---|---|---|
| skills/orchestrate/SKILL.md (40) | IN SCOPE, routed | GLOBAL-ROUTING block :36 + step-4 factory bridge :93 |
| skills/feature-expansion/SKILL.md (26) | IN SCOPE, routed | Factory paragraph :139; Phase 1 brainstorm dispatch (:47, :55) is ideation only, no file writes |
| skills/polish-pass/reference/impeccable-critique.md (11) | OUT | Verification-only Assessments A/B, "leave it as found" |
| skills/orchestrate/references/dispatch-prompt.md (7) | IN SCOPE, routed | Brief templates composing routed dispatches; carries Belief + first-build reconciliations |
| skills/orch-pipeline/SKILL.md (6) | IN SCOPE, routed | Factory paragraph :62 |
| skills/orch-build-mvp/SKILL.md (6) | IN SCOPE, routed | Pointer :13 |
| skills/council/SKILL.md (6) | OUT | Analysis/decisions only, no implementation work |
| rules/common-agents.mdc (5) | COVERED BY REFERENCE | Factory line :26; :42 launch is read-only 3-agent review |
| rules/hackathon-mode.mdc (4) | IN SCOPE (carrier) | GLOBAL-ROUTING block :45 |
| commands/gan-build.md (4) | COVERED BY REFERENCE | Factory pointer :12; step-0 pin :26 |
| skills/orchestrate/references/call-map.md (3) | OUT | Documentation (hook table + trigger phrases) |
| skills/design-taste-frontend/SKILL.md (3) | IN SCOPE, routed | Redesign pointer :455; hero/finish review read-only |
| skills/verification-before-completion/SKILL.md (2) | OUT | Verification-only dispatch |
| skills/motionsites-web-builder/references/techniques/depth-and-interaction.md (2) | OUT | "Spawns thumbnails" = CSS animation, not agents |
| skills/design-taste-frontend/references/hallmark/references/gates.md (2) | OUT | Read-only hero/finish review gates |
| skills/design-taste-frontend/references/gate.md (2) | OUT | Read-only review gate |
| commands/pm2.md (2) | OUT | `child_process.spawn` — process spawn, not agent dispatch |
| commands/plan.md (2) | OUT | Planning only; second verification pass read-only |
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
| skills/design-taste-frontend/references/hallmark/references/redesign.md (1) | IN SCOPE, routed | Factory paragraph :68 (one subagent per page past three pages) |
| skills/design-taste-frontend/references/copy-voice.md (1) | OUT | Fresh-reader subagent = read-only copy review |
| skills/ai-feature-spec/SKILL.md (1) | OUT | "Invoke this skill" = skill invocation, no agent dispatch |
| rules/ponytail.mdc (1) | OUT | Subagent return-message contract reference; no dispatch |
| rules/common-development-workflow.mdc (1) | OUT | Planning delegation ("use the architect agent when the user explicitly asks you to delegate planning"), user-gated, planning-only |
| rules/common-code-review.mdc (1) | OUT | Link text "Agent delegation"; no dispatch |
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

New-verb-only sites (no base-pattern hit; found by the fresh sweeps in §2):

| Site | Disposition | Reason |
|---|---|---|
| rules/common-patterns.mdc:11 | OUT | Parallel agents to evaluate options — analysis/planning only, no file writes |
| commands/plan-prd.md:67 | OUT | Handoff to `/plan` — planning, not implementation |
| commands/save-session.md:14 | OUT | Handoff of context to a future session, not a dispatch |
| skills/browser-qa/SKILL.md:22 | OUT | Handoff to `systematic-debugging` (no agent-dispatch lines of its own); browser-qa is verification-only |
| skills/pitch-deck-video/references/openmontage/montage.md:108 | OUT | Archive.org-only fan-out = research/media gathering |
| skills/track-picker/SKILL.md:3 | OUT | Generates an integration plan — planning only |
| skills/polish-pass/reference/impeccable-onboard.md:243 | OUT | Handoff to `/impeccable polish` — verification/polish pass |
| skills/orch-pipeline/SKILL.md:16 | IN SCOPE | "Invoke an operation skill" — routed skill invoking routed skills |
| skills/verification-loop/SKILL.md:15 | OUT | "Invoke this skill" — skill invocation; verification-only |
| skills/delivery-gate/SKILL.md:41 | OUT | Hook-install note, not a dispatch |
| agents/ecc-react-reviewer.md:33, :79 | OUT | Invoke review agents on a PR — read-only review |
| agents/ecc-a11y-architect.md:35 | OUT | Self-instruction to the role itself, not a dispatch of another agent |
| agents/ecc-code-reviewer.md:24, ecc-python-reviewer.md:18, ecc-seo-specialist.md:18, ecc-typescript-reviewer.md:18 | OUT | "When invoked:" boilerplate — the role being invoked, not dispatching |
| commands/demo.md:13 | OUT | "Dispatched `/demo`" = command-invocation note |
| commands/loop-start.md:2 | OUT | Loop-setup description (prints commands to launch/monitor a loop) |
| commands/orch-add-feature.md:7, orch-change-feature.md:7, orch-fix-defect.md:7 | COVERED BY REFERENCE | "Manually launch the orchestrator" — user launches the routed orchestrator skill |
| commands/prp-prd.md:86, :129, :295, :322 | OUT | Parallel investigations / phases in a planning doc — planning, not agent dispatch |
| commands/quality-gate.md:44–45 | OUT | Hook dispatcher script registry — observability plumbing, not agent dispatch |
| skills/context-budget/SKILL.md:52 | OUT | Prohibition ("Never launch a provider CLI…") |
| skills/app-scaffold/SKILL.md:54, :67, :76 | OUT | Launching Docker Desktop — process/app launch |
| skills/contract-first/SKILL.md:19, :256 | OUT | Frontend/backend work proceeding in parallel — coordination note, no agent dispatch |
| skills/production-audit/SKILL.md (launch lines) | OUT | Product-launch language in a readiness audit |
| skills/e2e-testing/SKILL.md:108 | OUT | `fullyParallel: true` — test-runner config |
| skills/click-path-audit/SKILL.md:167 | OUT | "Launch parallel agents per page" — read-only audit |
| skills/react-performance/SKILL.md:30, skills/typescript-patterns/SKILL.md:354 | OUT | Render / `Promise.allSettled` fan-out — code parallelism |
| skills/react-performance/SKILL.md:96, skills/typescript-patterns/SKILL.md:281, skills/click-path-audit/SKILL.md:34, skills/integration/SKILL.md:8, :85 | OUT | "kick off promises", "call in a stack", "function call in the handler", "working call in the demo path" — code language, no agent dispatch |
| skills/design-taste-frontend/assets/** READMEs, themes/dusk.md:67 | OUT | "Cards fan out" / "a hand-off in a well" — design copy |
| skills/design-taste-frontend/references/effects-creative.md:33, :106 | OUT | "Rotors that spin up" — design copy |
| skills/mobile-ship/references/android-store.md:13 | OUT | Tester recruitment — human testers, not agents |
| skills/ui-ux-pro-max/SKILL.md:359 | OUT | "Never fire off-screen" — animation language |
| rules/react-native-performance.mdc:33 | OUT | "Offload to Reanimated worklets" — code offload |
| agents/ecc-performance-optimizer.md:254, agents/ecc-refactor-cleaner.md:39 | OUT | `Promise.all` / detection tools in parallel — code parallelism |
| skills/orchestrate/SKILL.md:103, :205, :209, :211, :213, :221, :233, :260, :264; references/patterns.md:13, :26; dispatch-prompt.md:23 | IN SCOPE | Inside the routed skill / routed templates — fan-out, dispatch-composition and handoff rules, not new edges |
| skills/orchestrate/SKILL.md:93, :250, :400 | IN SCOPE | Step-4 factory bridge, NEEDS_CONTEXT re-dispatch, Gotchas fallback (dispatched through dispatch-prompt templates) |
| skills/orchestrate/SKILL.md:201 | IN SCOPE | "Dispatch scout" — read-only reconnaissance dispatched by the orchestrator under the factory rules |
| skills/orch-build-mvp/SKILL.md:34, :87 | IN SCOPE | `/demo` dispatch — user-invoked video command, dispatched by the orchestrator under the factory rules via dispatch-prompt templates |
| skills/feature-expansion/SKILL.md:47, :55 | OUT (skill in set) | "Dispatch four brainstorm subagents in parallel" — Phase 1 ideation, no file writes; skill routed via Phase 4 |
| skills/design-taste-frontend/references/hallmark/PROVENANCE.md:30; skills/polish-pass/reference/impeccable-PROVENANCE.md; skills/polish-pass/reference/lenses/*.md | OUT | Provenance notes / verification lenses — no dispatch |
| commands/sessions.md:294 | OUT | Parallel tmux/worktree runs — session bookkeeping |
| rules/arkts-hooks.mdc, react-native-patterns.mdc, react-patterns.mdc, react-testing.mdc, web-hooks.mdc, web-patterns.mdc; skills/frontend-patterns/SKILL.md, motion-patterns/SKILL.md, react-patterns/SKILL.md, react-testing/SKILL.md, mobile-ship/**, pitch-deck-video/**, app-scaffold/reference/**, e2e-testing/SKILL.md, hackathon-pitch/**, frontend-slides/** | OUT | "Launch"/"parallel"/"isolated" as product launch, code parallelism, or design-pattern language — no agent dispatch in any of them |
