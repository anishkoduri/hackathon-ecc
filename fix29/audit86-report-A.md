# Audit #86-A — Fix #29 (adaptable orchestration): routing coverage / dispatch census, round 7

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** routing coverage / dispatch census — verify the audit #85-B1 tree fix landed correctly in the built tree; re-derive the dispatcher set from scratch with fresh verb hunts; check the 10-skill routing set; spot-check the 9 MANIFEST §2(c) reconciliations; independently confirm GLOBAL-ROUTING byte-identity staged vs built.
**Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md` (§2 in full, incl. the §2(b) gan-design + planner rows and all 9 §2(c) reconciliations), `fix29/audit85-report-A.md`, `fix29/verify29.py` (85-B1 check at :724–730, gan-build pointer check at :1478–1479, KEPT lists at :225–282), `fix29/build-log-run7.txt`, `fix29/verify29-run12.log`.
**Method:** re-checked the 85-B1 file:line in the built tree (`hackathon-ecc/`) and diffed staged vs built; re-ran `python3 fix29/verify29.py` independently; re-ran the base-pattern census (case-insensitive) and compared per-file counts against #85-A's table; ran fresh verb sweeps for dispatch verbs NOT in the base-pattern set (`invoke`, `hand off`/`handoff`, `farm out`, `call upon`, `summon`, `stand up`, `spin off`, `parallelize`, `multi-agent`, `swarm`, `crew`, `fleet`, `executor`/`worker`, `parallel agents`, full `commands/` + `agents/` verb sweep for `dispatch|launch|spawn|delegate|invoke`); read every new hit in context; enumerated every command mentioning `agent` and triaged each. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.

## Verdict: NOT PASS — 1 blocking, 0 minor

85-B1 is verified fixed in full — the redesign paragraph now names the failed criterion in its correction-brief path, staged and built copies are byte-identical, and no other `_F29` line in the paragraph changed. The census reconciles exactly with #85-A (168 base-pattern hits / 49 files, 11 `Factory routing` files, GLOBAL-ROUTING in 16 files / 19 occurrences), the 10-skill routing set is intact, all 9 §2(c) reconciliations match the live tree, GLOBAL-ROUTING md5s match all prior rounds, and the verifier re-runs at 292/292.

The one blocking finding is a live implementation dispatch no prior round ever triaged: `commands/react-build.md:7` invokes the file-writing `react-build-resolver` agent with zero `_F29` coverage anywhere on its path. It escaped all six prior rounds for the same structural reason as 83-A1 (gan-design): its dispatch verb — "invokes" — is not in the base-pattern grep set, and neither #84-A's nor #85-A's wider sweeps record triaging it ('react-build' occurs 0× across audit80–85 reports and the MANIFEST, outside verify29's KEPT census lists, which are not routing coverage). Per the verdict rules a live implementation dispatch with no routing coverage is blocking, and the fix's own precedent (MANIFEST §2(b): gan-build/gan-design got pointers precisely as "the actual launch site of the code-writing" agent) puts a command launch site of a code-writing agent in scope.

## Findings

### 86-A1 (blocking): `commands/react-build.md` dispatches the file-writing `react-build-resolver` agent with no routing coverage

**Evidence.**

- `commands/react-build.md:7`: "This command invokes the **react-build-resolver** agent to incrementally fix React build errors with minimal changes." The command's whole purpose is the launch: the description repeats it ("Fix React build failures … Invokes the react-build-resolver agent for minimal, surgical fixes"), and the worked example shows file edits (`src/components/UserCard.tsx`, `src/pages/Home.tsx`) plus a dependency install, ending in "Files modified: 2".
- `agents/ecc-react-build-resolver.md:2–3, :24–32`: the role is a file-writing agent, not a reviewer — model `cursor-grok-4.6-high-fast` (drone tier), mission "to fix React build failures … with **minimal, surgical** [fixes]", Core Responsibilities "Fix JSX/TSX compile errors (missing `@types/react`, wrong JSX transform, missing imports)", "Resolve bundler configuration issues", "Handle missing dependencies". Every responsibility is a project-file change.
- `grep -c _F29` = **0** in `commands/react-build.md` and **0** in `agents/ecc-react-build-resolver.md`. No verify29 check mentions react-build routing (the two `react-build` hits in verify29.py:239/:271 are KEPT_AGENTS / KEPT_COMMANDS census lists from the fix #28 debloat, not coverage assertions).
- Not covered by reference anywhere else:
  - `rules/common-agents.mdc` (alwaysApply) governs "this list" — exactly 8 agents (`ecc-architect`, `ecc-tdd-guide`, `ecc-code-reviewer`, `ecc-security-reviewer`, `ecc-build-error-resolver`, `ecc-e2e-runner`, `ecc-refactor-cleaner`, `ecc-doc-updater`). `react-build-resolver` is **not** in it; only the generic `build-error-resolver` is (`common-agents.mdc:17`). MANIFEST §2(b)'s record of the common-agents coverage enumerates the same governed agents — the resolver is not among them.
  - No routed skill invokes `/react-build` or the resolver. The only mentions are Related-pointer lines (`skills/react-patterns/SKILL.md:270`, `skills/react-performance/SKILL.md:568`) and call-map rows — pointers, not dispatch instructions, in unrouted skills.
  - The command's own stop conditions (stop after 3 attempts on the same error; re-run the build after each fix) are self-verification by the agent, not orchestrator verification against a brief's acceptance criteria, and there is no director brief at all: no files in/out of scope, no acceptance criteria, no NO-GUESSING bound on a drone-tier model making surgical edits.
- Never triaged before: `grep -rn 'react-build' fix29/audit8*-report-*.md fix29/MANIFEST.md` returns nothing (the MANIFEST's only `react-build` mentions are none; the audit reports likewise). The #84-A report claims an `invoke` sweep that "surfaced only out-of-scope sites" but names no commands/ result, and #85-A's census table has no react-build row — the written record does not show this site was ever examined.

**Why it matters.** The GLOBAL-ROUTING block itself states the rule: "a dispatch with no factory routing is off-skill improvisation and fails the audit." The fix already applied that rule to command launch sites: gan-build got its pointer as the launch site of the code-writing gan-generator (80-A6) and gan-design got one as the twin step-0 launch site (84-A1). `/react-build` is the same shape — the actual launch site of a code-writing agent — with no pointer, no brief structure, and no verification path. A user running `/react-build` gets a drone-tier agent editing project files under a one-line task description, which is exactly the unbriefed execution fix #29 exists to eliminate.

**Concrete fix (mirrors the gan-build precedent).** Add a one-line factory pointer to `commands/react-build.md` after the `:7` invocation line, mirroring `commands/gan-build.md:12` in form: the resolver runs as a single-task factory drone with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (the re-run build is evidence, not the verdict). Add a verify29 assertion for the pointer line and `_F29` presence in the file, mirroring the 84-A1 checks (verify29.py:1475–1477 pattern). Record the site in MANIFEST §2(b) alongside gan-build/gan-design. (Alternative considered and rejected: adding `react-build-resolver` to the common-agents governed list alone — the gan precedent is the launch-site pointer, and the list's factory line is framed as governing "this list", so the pointer is the consistent treatment.)

**Scope note — the boundary held.** This is the only command with this shape. Every other agent-invoking command was checked and is out of scope for a recorded reason (see census table): review-only agents (`fastapi-review`, `python-review`, `react-review`, `review-pr`, `code-review`, `astra-review`), analysis/design/review only with inline implementation (`feature-dev`), inline with no dispatch (`build-fix`, `prp-implement`, `prp-plan`, `prp-prd`, `prp-commit`, `prp-pr`, `plan` — which explicitly forbids subagent delegation by default), and the already-covered gan/orch-* commands. No skill contains an "invoke(s) the X agent" dispatch line at all.

## §1 — #85-B1 disposition: the finding re-checked

| #85-B1 | Status | Evidence |
|---|---|---|
| 85-B1 (tree): `redesign.md:68` correction-brief path does not name the failed criterion | **VERIFIED-FIXED** | Built `skills/design-taste-frontend/references/hallmark/references/redesign.md:68` now carries the clause verbatim: "sends failed output back with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (VERIFY-MERGE_F29)". Staged `new-skills/design-taste-frontend/references/hallmark/references/redesign.md:68` carries the identical clause; `diff` staged vs built is **clean — the two files are byte-identical**, so no other `_F29` line in the paragraph changed (check 7e confirmed independently, not via the verifier). The clause matches the construction sentences at the other five consumption sites word-for-word (feature-expansion:158, orch-pipeline:74, orchestrate ladder :252, gan-build ORCHESTRATOR-CHECK :63, gan-build planner-spec 3a :30). verify29.py:724–730 asserts it (the 85-B1 check). |

## §2 — Fresh hunt: dispatch census re-derived from scratch

Base pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files** — identical to #85-A, with identical per-file counts (see census table). Whole-tree base pattern: **170 hits** (168 + 2 `README.md` documentation hits). The only tree change since run 6 is the 85-B1 staged redesign edit, which adds no dispatch verb, so a zero delta is exactly what is expected.

Fresh-verb sweeps (all `*.md`/`*.mdc`, skills/rules/commands/agents), each read in context:

- **`farm out|call upon|summon|spin off|parallelize|swarm|crew of|fleet of`:** 0 agent-shaped hits. `react-performance:243` ("Parallelize nested fetches with Promise.all") — code parallelism. `commands/sessions.md:19` ("operator-surface context for a swarm") — session bookkeeping. `multi-agent` hits are all descriptions of the already-routed GAN harness (`gan-style-harness:3, :10, :12, :228`, `gan-build.md:16`, `ecc-gan-*.md:17`) or the read-only PR-review command (`commands/review-pr.md:2`, `commands/code-review.md:2` — "for a multi-agent pass use /review-pr", review-only).
- **`stand up`:** 2 hits, both scaffold language inside routed skills (`orch-build-mvp:38`, `orch-pipeline:70` — "stand up the first end-to-end slice"), not agent dispatch.
- **`hand off|handoff`:** all previously triaged or non-dispatch — skill-to-skill handoffs (`browser-qa:22` → systematic-debugging, `systematic-debugging:20`, `plan-prd.md:2, :67` → /plan planning, `save-session.md:14` future-session context, `polish-pass/reference/impeccable-onboard.md:243` → /impeccable polish verification pass, `track-picker:3` integration plan), documentation handoffs (`orch-pipeline:109–111`, `dispatch-prompt.md:16, :78`, `orchestrate:239, :264, :369, :394`), and design copy (`motion-advanced:444, :446`, `frontend-slides:106, :185`). No new dispatch.
- **`parallel agents|parallel subagents|concurrent agents|subagents|drones`:** 2 hits, both previously triaged out — `click-path-audit:167` ("Launch parallel agents per page", read-only audit) and `common-patterns.mdc:11` ("Use parallel agents to evaluate options", analysis/planning only, no file writes).
- **`executor|worker`:** all code parallelism (`python-patterns:457–479` ThreadPool/ProcessPoolExecutor, `typescript-patterns:390–412` worker pool, `vite-patterns:335` webworker target, `e2e-testing:111` test-runner workers, `production-audit:68` background workers, Cloudflare Workers) or inside the routed skill (`orchestrate:22–31` executor model table, `orchestrate:62` etc.). No new dispatch.
- **Full `invoke` triage (the 86-A1 hunt):** every "invoke(s) the X agent" line in commands/ is accounted for — review-only (`fastapi-review.md:7`, `python-review.md:7`, `react-review.md:7`), the blind-review read-only dispatch (`astra-review.md:24`, triaged in prior rounds), the covered gan/orch commands, and the one live implementation dispatch, **`react-build.md:7`** (§Findings, 86-A1). No skill contains an "invoke(s) the X agent" line. `agents/` "invoke" hits are role-being-invoked boilerplate (`ecc-code-reviewer.md:24`, `ecc-python-reviewer.md:18`, `ecc-seo-specialist.md:18`, `ecc-typescript-reviewer.md:18`, `ecc-rag-pipeline-reviewer.md:3`), the previously triaged read-only review pairing (`ecc-react-reviewer.md:33, :79, :159`), or the routed GAN roles.
- **Full `commands/` + `agents/` verb sweep (`dispatch|launch|spawn|delegate|invoke`):** every remaining hit triaged (see census table). Newly triaged this round beyond 86-A1: `commands/review-pr.md` full read (multi-perspective PR review, read-only, out); `commands/feature-dev.md` full read (explorer/architect/reviewer agents only, implementation phase inline, out); `commands/build-fix.md` full read (inline fix loop, no agent dispatch, out); `commands/prp-implement.md` (no dispatch lines, inline, out); `commands/react-test.md:265` (Related pointer to review/TDD agents, out); `agents/ecc-mle-reviewer.md:35–42` and `agents/ecc-build-error-resolver.md:114–118` (conditional "Use X" lane pointers — see observation in §6).

**The 86-A1 escape class.** The base-pattern set (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`) cannot see "invokes the X agent". That is the same structural escape as 83-A1 (gan-design's "dispatch" was not in the base set). The fix's census method has now missed one live dispatch per escape class in two different verb families; the verifier's census lists (KEPT_AGENTS / KEPT_COMMANDS) enumerate the resolver and the command but assert nothing about routing coverage of either.

## §3 — The 10-skill routing set: confirmed, no missing, no extra

`GLOBAL-ROUTING_F29` present in all 10 routing-set skills plus `rules/hackathon-mode.mdc`; tree-wide **16 files, 19 occurrences** (unchanged from #85-A). `"Factory routing (fix #29"` occurs ×1 in exactly **11 files** (unchanged). Counts re-confirmed: **67 skills / 45 agents / 48 rules / 55 commands**. `ui-ux-pro-max/` still **0 `_F29` tokens**; no `deepseek-`/`qwen-` model slugs in the built tree outside the GLOBAL-ROUTING forward-reference wording itself (model pins unchanged — fix #30's work, not this fix's).

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

Covered by reference (not in the set, governed by it): `rules/common-agents.mdc:26` factory line (8 listed agents only — see 86-A1); `commands/gan-build.md:12` pointer; `commands/gan-design.md:10` pointer + `:19` pin; `agents/ecc-gan-planner.md:44` re-route; `commands/orch-refine-code.md:33` mirror; `commands/orchestrate.md`, `orch-build-mvp.md`, `orch-add-feature.md`, `orch-change-feature.md`, `orch-fix-defect.md` route to the routed skills. NOT covered: `commands/react-build.md` + `agents/ecc-react-build-resolver.md` (86-A1).

## §4 — Spot-check: the 9 reconciliations in MANIFEST §2(c) vs the live tree

All 9 spot-checked; all match the tree text. (86-A1 is a coverage gap, not a reconciliation contradiction — no reconciliation text mentions react-build.)

1. **Belief-in-the-brief vs NO-GUESSING (5 copies):** `"pick the reasonable option"` = 5 hits, at `orch-pipeline:72`, `orch-build-mvp:70`, `feature-expansion:151`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92` (the first two grep lines are the containing paragraphs; all five carry the identical carve-out plus tie-breaker, as in #85-A). First-build carve-out: `"instead of NEEDS_CONTEXT"` = **0**; `"state the assumption you made and proceed"` = **0** tree-wide; scope sentence (`"for carrying out the briefed approach only"`) = 4 hits in `dispatch-prompt.md`; `agents/deep-reasoner.md:17` carries the rewritten NEEDS_CONTEXT line + identical NO-GUESSING bound + tie-breaker (read verbatim). Matches.
2. **Merge-order fallback vs partition-by-boundary (3 sites):** the "applies only if partitioning failed" bridge present at all 3 — `orchestrate:93`, `feature-expansion:139`, `orch-build-mvp:71`. Matches.
3. **Feature-expansion Team shape vs factory cap:** Phase 4 paragraph (`feature-expansion:139`) states the factory queue under Cursor's cap ("one implementer per feature, up to 4 in parallel" with the harness-gate clause). Matches.
4. **Feature-expansion brief format vs DIRECTOR-BRIEF:** item 2 names "the files explicitly OUT of scope"; item 4 split into 4a acceptance criteria (`:148`-area) and 4b verification steps; item 9 return format (`:154`-area). Matches (items read in full at `:140–160`).
5. **GAN evaluator vs VERIFY-MERGE:** ORCHESTRATOR-CHECK wiring order verified live by index arithmetic — EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484 (identical to #83-B/#84-A/#85-A); planner-spec check at `gan-build.md:30` with cap "**at most two correction re-dispatches**"; `"at most one correction"` = **0** in the built tree; GENERATE block carries `Verification steps:` and `Return format:` (both confirmed present inside the `# GENERATE`–`# Wait for generator` slice by direct check). Skill mirrors intact (`gan-style-harness:69` Architecture note, `:155` Scoring bullet). Matches.
6. **Orchestrate contract vs DIRECTOR-BRIEF:** seventh field `Verification steps:` in the contract core (`orchestrate:235`, "distinct from the acceptance check"); "files explicitly out of scope" in Constraints (`orchestrate:232`); no-drop rule present (`dispatch-prompt.md:4`: "delete no DIRECTOR-BRIEF field — a field with nothing to list is written as `none`, never deleted"). Matches.
7. **"Correction brief" constructed:** construction sentences carrying the full naming clause ("naming the failed acceptance criterion and the required correction, distinct from the original brief") at all six sites — `feature-expansion:158`, `orch-pipeline:74`, orchestrate ladder `:252`, GAN ORCHESTRATOR-CHECK (`gan-build.md:63`), planner-spec 3a (`:30`), and now redesign `:68` (85-B1 fixed). Matches — the redesign site is the sixth, closing the gap 85-B1 named.
8. **Slot refill harness-gate:** `"slots refill per wave"` = 5 hits — `orch-pipeline:62`, `feature-expansion:139`, `gan-style-harness:14`, `orchestrate:93`, `redesign.md:68`. Matches.
9. **Staged-vs-built drift by design:** not re-proven end to end this round (fix16 anchor); the recorded drift lines are unchanged in the built tree and verify29 check 7e (the narrow `_F29`-line identity check) passes — see §5. No contradiction with the tree found.

## §5 — GLOBAL-ROUTING block byte-identity (independent, not via the verifier)

- **orchestrate:** staged `new-skills/orchestrate/SKILL.md:36` md5 `bdf1720f69f9b50e3791a14c68f5c5ea` = built `skills/orchestrate/SKILL.md:36`; `diff` clean.
- **hackathon-mode:** staged `new-rules/hackathon-mode.mdc:45` md5 `39a22e9247be839a841ffbea3ad19918` = built `rules/hackathon-mode.mdc:45`; `diff` clean.
- Cross-file `diff` (hackathon-mode's leading `"- "` list marker stripped) clean — the two blocks are identical modulo the established DESIGNPKG-AUTO marker convention.
- Both match the values recorded by audits #80-A through #85-A. No byte-identity break.
- **85-B1 staged-vs-built identity (check 7e, independent):** `diff new-skills/design-taste-frontend/references/hallmark/references/redesign.md hackathon-ecc/skills/design-taste-frontend/references/hallmark/references/redesign.md` is clean — the files are byte-identical, so the naming clause landed in both and no other `_F29` line in the paragraph changed.

## §6 — Checked and clean

- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **292/292, exit 0** (independently re-run; includes the 85-B1 check, which passes).
- **85-B1 verified fixed** in full (§1) — naming clause, staged = built byte-identical, verify29 guard present (verify29.py:724–730).
- **84-A1 still fixed** (gan-design pointer `:10`, `_F29` count in the file = 1, step-0 pin `:19` present verbatim).
- **83-A2 still fixed** (planner `:44` re-route in place; old phrase `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"` = 0 hits).
- **GLOBAL-ROUTING block md5s:** orchestrate `bdf1720f…`, hackathon-mode `39a22e92…` (staged = built, matching all prior rounds).
- **Census:** 10 skills; 16 files carry `GLOBAL-ROUTING_F29` (19 occurrences); `"Factory routing (fix #29"` ×1 in exactly 11 files; counts 67/45/48/55.
- **All 9 §2(c) reconciliations match the live tree** (§4).
- **82-A2 cap alignment holds** (`"at most one correction"` 0×; `"at most two correction re-dispatches"` 1× at `gan-build.md:30`).
- **Model pins unchanged** (`ui-ux-pro-max` 0 `_F29`; no deepseek-/qwen- slugs outside the GLOBAL-ROUTING forward-reference wording).
- **Build run 7:** exit 0, fix29.py 29 changes, 0 errors (build-log-run7.txt); verify29-run12.log 292/292.
- **Call map:** not re-run (no fix adds a dispatch edge; #80-A's restore stands). Note: the call map's textual scan lists `/react-build` and `ecc-react-build-resolver` as invokers/invokees but, like the redesign.md:68 dispatch, a map row is not routing coverage — the map documents the edge; it does not govern it.

**Observation (not a finding, not counted):** `agents/ecc-mle-reviewer.md:35–42` ("Reuse Existing Review Lanes") and `agents/ecc-build-error-resolver.md:114–118` contain conditional "Use X" lane pointers naming file-writing agents (`pytorch-build-resolver`, `build-error-resolver`, `refactor-cleaner`, `doc-updater`). These are referral notes inside read-only review/resolver roles ("use X when [condition]"), not executed dispatch steps in a workflow — the same class as `react-patterns:270`'s Related pointer. The named agents are governed when actually dispatched via `common-agents.mdc` (build-error-resolver, refactor-cleaner, doc-updater are listed) or routed skills. `pytorch-build-resolver` is not in the common-agents list and has no command launch site; no executed dispatch of it was found. Revisit trigger: if a future fix routes review-lane escalation through factory drones, these pointers become dispatch edges and need the pointer treatment. Not a finding now because no dispatch is executed from them.

## Grep counts (for the record)

- Base dispatch pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/agents): **168 hits in 49 files** (identical to #85-A; per-file counts identical).
- Whole-tree base pattern: **170 hits** (168 + 2 `README.md` documentation hits).
- `"Factory routing (fix #29"`: **11 files ×1** (unchanged).
- `GLOBAL-ROUTING_F29`: **16 files, 19 occurrences** (unchanged).
- `"slots refill per wave"`: **5 hits**.
- `"pick the reasonable option"`: **5 hits, all 5 carved + tie-breaker**.
- `"state the assumption you made and proceed"`: **0 hits tree-wide**.
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"at most one correction"`: **0 hits in the built tree**; `"at most two correction re-dispatches"`: **1 hit** (`commands/gan-build.md:30`).
- `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"`: **0 hits** (83-A2 fix still in place).
- `_F29` in `commands/gan-design.md`: **1**; `_F29` in `skills/ui-ux-pro-max/`: **0**.
- `"dispatch to the design skill"`: **2 sites only** (`commands/gan-build.md` step 0, `commands/gan-design.md:19`) — no third copy exists.
- `_F29` in `commands/react-build.md`: **0**; `_F29` in `agents/ecc-react-build-resolver.md`: **0** (86-A1).
- `"react-build"` occurrences across `fix29/audit80-report-*.md` … `audit85-report-*.md` + `MANIFEST.md`: **0** (86-A1 never triaged before).
- GLOBAL-ROUTING block md5s: orchestrate `bdf1720f69f9b50e3791a14c68f5c5ea`, hackathon-mode `39a22e9247be839a841ffbea3ad19918` (staged = built).
- GAN wiring order indices: EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484.
- Verifier independently re-run: **292/292, exit 0**.

## Census table — every dispatch hit, in/out of scope + reason

Base-pattern files (49, case-insensitive). "Covered by reference" = governed by a routed skill's factory rules via an explicit pointer/pin, not carrying its own factory paragraph. Counts are case-insensitive line counts; all identical to #85-A.

| File (base hits) | Disposition | Reason |
|---|---|---|
| skills/orchestrate/SKILL.md (40) | IN SCOPE, routed | GLOBAL-ROUTING block :36 + step-4 factory bridge :93 |
| skills/feature-expansion/SKILL.md (26) | IN SCOPE, routed | Factory paragraph :139; Phase 1 brainstorm dispatch (:47, :55) is ideation only, no file writes |
| skills/polish-pass/reference/impeccable-critique.md (11) | OUT | Verification-only Assessments A/B, "leave it as found" |
| skills/orchestrate/references/dispatch-prompt.md (7) | IN SCOPE, routed | Brief templates composing routed dispatches; carries Belief + first-build reconciliations |
| skills/orch-pipeline/SKILL.md (6) | IN SCOPE, routed | Factory paragraph :62 |
| skills/orch-build-mvp/SKILL.md (6) | IN SCOPE, routed | Pointer :13 |
| skills/council/SKILL.md (6) | OUT | Analysis/decisions only, no implementation work |
| rules/common-agents.mdc (5) | COVERED BY REFERENCE | Factory line :26; :42 launch is read-only 3-agent review. Governs the 8 listed agents only (see 86-A1) |
| rules/hackathon-mode.mdc (4) | IN SCOPE (carrier) | GLOBAL-ROUTING block :45 |
| commands/gan-build.md (4) | COVERED BY REFERENCE | Factory pointer :12; step-0 pin :26 |
| skills/orchestrate/references/call-map.md (3) | OUT | Documentation (hook table + trigger phrases) |
| skills/design-taste-frontend/SKILL.md (3) | IN SCOPE, routed | Redesign pointer :455; hero/finish review read-only |
| skills/verification-before-completion/SKILL.md (2) | OUT | Verification-only dispatch |
| skills/motionsites-web-builder/references/techniques/depth-and-interaction.md (2) | OUT | "Spawns thumbnails" = CSS animation, not agents |
| skills/design-taste-frontend/references/hallmark/references/gates.md (2) | OUT | Read-only hero/finish review gates |
| skills/design-taste-frontend/references/gate.md (2) | OUT | Read-only review gate |
| commands/pm2.md (2) | OUT | `child_process.spawn` — process spawn, not agent dispatch |
| commands/plan.md (2) | OUT | Planning only; explicitly "Do not delegate to a subagent by default"; second verification pass read-only |
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
| skills/design-taste-frontend/references/hallmark/references/redesign.md (1) | IN SCOPE, routed | Factory paragraph :68 (one subagent per page past three pages); 85-B1 naming clause VERIFIED-FIXED |
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
| **commands/react-build.md:7 (+ description :2)** | **IN SCOPE, NOT COVERED — 86-A1 (blocking)** | **Invokes `react-build-resolver` to fix build errors with minimal surgical file edits; 0 `_F29` in command and agent file; resolver not in the common-agents governed list; no routed skill invokes it; never triaged in rounds 1–6** |
| commands/fastapi-review.md:7, python-review.md:7, react-review.md:7 | OUT | Invoke review-only agents (fastapi/python/react reviewer) — read-only |
| commands/review-pr.md:2 + Steps | OUT | Multi-perspective PR review using specialized review agents — read-only (full file read this round) |
| commands/code-review.md:2 | OUT | Step-by-step PRP checklist review; multi-agent pass defers to /review-pr — read-only |
| commands/feature-dev.md:17, :29, :41 | OUT | code-explorer (analysis), code-architect (design), code-reviewer (review) only; implementation phase inline — no implementation dispatch (full file read this round) |
| commands/build-fix.md | OUT | Inline fix loop (Read/Edit tools), no agent dispatch (full file read this round) |
| commands/prp-implement.md, prp-plan.md, prp-prd.md, prp-commit.md, prp-pr.md | OUT | No agent/dispatch/invoke/launch/spawn lines — inline workflow |
| commands/react-test.md:265 | OUT | Related pointer to review/TDD agents — reference, not a dispatch |
| commands/loop-start.md:2 | OUT | Loop-setup description (prints commands to launch/monitor a loop) |
| commands/quality-gate.md:44–45 | OUT | Hook dispatcher script registry — observability plumbing, not agent dispatch |
| commands/epic-claim.md, epic-decompose.md, epic-publish.md, epic-review.md, epic-sync.md, epic-unblock.md, epic-validate.md, test-coverage.md, update-docs.md, refactor-clean.md, resume-session.md, skill-create.md, update-codemaps.md, issue-review.md, learn.md, model-route.md, checkpoint.md, auto-update.md, setup-pm.md, pr.md | OUT | No agent/dispatch/invoke/launch/spawn lines at all (all 20 checked this round) |
| commands/astra-review.md:24 | OUT | Blind review dispatched to deep-reasoner as fresh subagent — read-only |
| commands/orch-add-feature.md:7, orch-change-feature.md:7, orch-fix-defect.md:7, orch-build-mvp.md:7, orch-refine-code.md:7 | COVERED BY REFERENCE | "Manually launch the orchestrator" — user launches the routed orchestrator skill |
| commands/orch-refine-code.md:26, :33 | COVERED BY REFERENCE | refactor-cleaner sweep qualified as single-task factory drone with director brief |
| commands/gan-build.md:27, :39, :52 | COVERED BY REFERENCE | Planner/generator/evaluator launches under the :12 factory pointer |
| commands/pm2.md:103 | OUT | `child_process.spawn` — process spawn |
| rules/common-patterns.mdc:11 | OUT | Parallel agents to evaluate options — analysis/planning only, no file writes |
| rules/common-agents.mdc:42 | OUT | "Launch 3 agents in parallel" — security/performance/type-checking, read-only, governed in-file by the :26 factory line + :38 read-only rule |
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
| agents/ecc-mle-reviewer.md:35–42 | OUT (see §6 observation) | Conditional "Use X" lane pointers (incl. file-writing agents) inside a read-only review role — referral notes, not executed dispatch |
| agents/ecc-build-error-resolver.md:114–118 | OUT (see §6 observation) | Conditional escalation pointers ("Code needs refactoring → use `refactor-cleaner`") — referral notes, not executed dispatch |
| skills/react-patterns/SKILL.md:270, skills/react-performance/SKILL.md:568 | OUT | Related pointer naming `react-build-resolver` for build/bundler errors — reference, not a dispatch instruction |
| skills/click-path-audit/SKILL.md:167 | OUT | "Launch parallel agents per page" — read-only audit |
| skills/orchestrate/SKILL.md:103, :205, :209, :211, :213, :221, :233, :260, :264; references/patterns.md:13, :26; dispatch-prompt.md:23 | IN SCOPE | Inside the routed skill / routed templates — fan-out, dispatch-composition and handoff rules, not new edges |
| skills/orchestrate/SKILL.md:93, :250, :400 | IN SCOPE | Step-4 factory bridge, NEEDS_CONTEXT re-dispatch, Gotchas fallback (dispatched through dispatch-prompt templates) |
| skills/orchestrate/SKILL.md:201 | IN SCOPE | "Dispatch scout" — read-only reconnaissance dispatched by the orchestrator under the factory rules |
| skills/orch-build-mvp/SKILL.md:34, :87 | IN SCOPE | `/demo` dispatch — user-invoked video command, dispatched by the orchestrator under the factory rules via dispatch-prompt templates |
| skills/feature-expansion/SKILL.md:47, :55 | OUT (skill in set) | "Dispatch four brainstorm subagents in parallel" — Phase 1 ideation, no file writes; skill routed via Phase 4 |
| skills/orch-build-mvp/SKILL.md:38, skills/orch-pipeline/SKILL.md:70 | IN SCOPE | "Stand up the first end-to-end slice" — scaffold language inside routed skills, not agent dispatch |
| skills/design-taste-frontend/references/hallmark/PROVENANCE.md:30; skills/polish-pass/reference/impeccable-PROVENANCE.md; skills/polish-pass/reference/lenses/*.md | OUT | Provenance notes / verification lenses — no dispatch |
| commands/sessions.md:294 | OUT | Parallel tmux/worktree runs — session bookkeeping |
| commands/sessions.md:19 | OUT | "Operator-surface context for a swarm" — session bookkeeping |
| skills/react-performance/SKILL.md:243 | OUT | "Parallelize nested fetches with Promise.all" — code parallelism |
| skills/python-patterns/SKILL.md:457–479, skills/typescript-patterns/SKILL.md:390–412, skills/vite-patterns/SKILL.md:335, skills/e2e-testing/SKILL.md:111, skills/production-audit/SKILL.md:68 | OUT | ThreadPool/ProcessPoolExecutor, worker pools, webworker target, test-runner workers, background workers — code parallelism |
| skills/frontend-slides/SKILL.md:106, :185; skills/motion-advanced/SKILL.md:444, :446; skills/tdd-workflow/SKILL.md:22; skills/orchestrate/SKILL.md:85, :239, :264, :369, :394; skills/orchestrate/references/dispatch-prompt.md:16, :78; skills/orch-pipeline/SKILL.md:109, :111; skills/feature-expansion/SKILL.md:176, :216; skills/pitch-deck-video/SKILL.md:232, :269, :836; skills/polish-pass/SKILL.md:102; skills/ui-ux-pro-max/SKILL.md:264, :348; skills/systematic-debugging/SKILL.md:20; commands/epic-validate.md:7; commands/plan-prd.md:2, :67; commands/save-session.md:14; agents/ecc-gan-evaluator.md:134; agents/ecc-gan-planner.md:46, :109; agents/ecc-homelab-architect.md:31; agents/ecc-rag-pipeline-reviewer.md:54, :56 | OUT | "Handoff" as skill-to-skill transfer, documentation handoff, or design copy — no agent dispatch in any of them |
| rules/arkts-hooks.mdc, react-native-patterns.mdc, react-patterns.mdc, react-testing.mdc, web-hooks.mdc, web-patterns.mdc; skills/frontend-patterns/SKILL.md, motion-patterns/SKILL.md, react-patterns/SKILL.md, react-testing/SKILL.md, mobile-ship/**, pitch-deck-video/**, app-scaffold/reference/**, e2e-testing/SKILL.md, hackathon-pitch/**, frontend-slides/** | OUT | "Launch"/"parallel"/"isolated" as product launch, code parallelism, or design-pattern language — no agent dispatch in any of them |
