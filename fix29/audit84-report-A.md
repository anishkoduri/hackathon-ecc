# Audit #84-A — Fix #29 (adaptable orchestration): routing coverage / dispatch census, round 5

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** routing coverage / dispatch census — verify both audit #83-A findings (83-A1, 83-A2) actually landed in the built tree; re-derive the dispatcher set from scratch with fresh verb hunts; check the 10-skill routing set; spot-check the 9 MANIFEST §2(c) reconciliations; independently confirm GLOBAL-ROUTING byte-identity staged vs built.
**Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md` (§2 in full, incl. the §2(b) gan-design + planner rows and all 9 §2(c) reconciliations), `fix29/audit83-report-A.md`, `fix29/fix29.py` (§5d/§5e/§5f), `fix29/verify29.py` (83-A1/A2 checks at :1443–1456), `fix29/fix29-patch-log.md`, `fix29/build-log-run5.txt`.
**Method:** re-checked each 83-A file:line in the built tree (`hackathon-ecc/`); re-ran `python3 fix29/verify29.py` independently; grepped the whole built tree (`skills/`, `rules/`, `commands/`, `agents/`, `*.md`/`*.mdc`) for the base pattern plus fresh verb sweeps (`invoke`, `dispatch to/the/a`, `fan-out`/`farm-out`/`hand-off`, `launch`, `parallel agents`, `fresh-context`, `assign`, `executor`/`worker`, `isolated`); read every new hit in context. Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.

## Verdict: NOT PASS — 0 blocking, 1 minor

83-A2 is verified fixed in full — the planner fallback is genuinely re-routed, the old instruction is gone from the file, and the MANIFEST record covers it. 83-A1 is verified fixed in substance — the parenthetical is in `gan-design.md:17` verbatim and the MANIFEST §2(b) record now names gan-design — but the second half of the assigned A1 check fails: the file still carries **0 `_F29` tokens**, so a token/census-based reading still shows `/gan-design` as uncovered, and no verifier check guards the token (verify29's 83-A1 check asserts only the parenthetical). That is a bounded, one-line fix, hence minor (84-A1), not blocking: the step-0 dispatch is pinned inline by the parenthetical itself, and the build loop is covered by reference via "Same as `/gan-build` Phase 2". No new live implementation dispatch was found anywhere in the fresh hunt.

## §1 — #83-A disposition: every finding re-checked

| #83-A | Status | Evidence |
|---|---|---|
| 83-A1 (minor): gan-design step-0 twin dispatch, no inline pin, 0 `_F29` tokens | **VERIFIED-FIXED IN SUBSTANCE — 1 residual (84-A1)** | `commands/gan-design.md:17` (Setup step 0) now carries the parenthetical verbatim: "(the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief)", identical to `commands/gan-build.md:26`. MANIFEST §2(b) now has a `commands/gan-design.md` row naming it as the twin step-0 site under the same inline-invocation reading with the same revisit trigger, and explicitly correcting audit #80-A row 25's false "No launch/subagent lines" claim. **Residual:** `grep -c "_F29" commands/gan-design.md` = **0**, and `grep -c "Factory routing" commands/gan-design.md` = **0** — the file carries no token at all. See finding 84-A1. |
| 83-A2 (minor): planner fallback instructs the planner drone to invoke the design-lead | **VERIFIED-FIXED** | `agents/ecc-gan-planner.md:44` (Direction source) now reads: "…if this agent is ever launched with no direction recorded, STOP and return NEEDS_CONTEXT naming the missing direction to the orchestrator instead of invoking the design-lead itself — the orchestrator invokes the design-lead inline (per the design-package rule) and re-dispatches this agent with the recorded direction, then copy it here…". The old instruction is gone: `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"` occurs **0×** in the file (and verify29's 83-A2 checks assert exactly this). MANIFEST §2(b) records the site with the re-route and the reason (a drone cannot execute the inline-as-orchestrator reading). fix29.py §5f implements the re-route exactly as specified (option (a)). |

## Findings

### 84-A1 — MINOR: `commands/gan-design.md` still carries 0 `_F29` tokens — the A1 token check fails even though the parenthetical landed

**Evidence.** `grep -c "_F29" commands/gan-design.md` = 0 in the built tree; `grep -rn "_F29" commands/gan-design.md` returns nothing. Its twin `commands/gan-build.md` carries 1 `_F29` token — the factory pointer at `:12` ("**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the planner, generator, and evaluator passes below run as factory drones per `gan-style-harness`…"). `gan-design.md` has no equivalent pointer line anywhere in the file. fix29.py §5e's own comment states the pre-fix condition as "zero _F29 tokens" and the fix it implements adds only the parenthetical — no token. verify29's 83-A1 check (verify29.py:1443–1447) asserts only `count("(the design-lead is invoked inline …") == 1`; nothing in the verifier asserts any `_F29` token in gan-design, so this gap is unguarded and will not fail a future build.

**Why it matters.** The assigned A1 criterion is two-part — parenthetical AND `_F29` tokens in the file — and only the first half is met. The consequence is census-level, not execution-level: every routing-coverage method in this fix keys on token presence (`GLOBAL-ROUTING_F29` census, `"Factory routing (fix #29"` counts, verify29 check 7e), so a reader or auditor grepping for coverage still finds `/gan-design` uncovered, and a reader of `/gan-design` alone sees no token tying the step-0 dispatch to the routing rules — the parenthetical's operative clause ("a spawned execution must carry a director brief") is unanchored to any named token or pointer. Minor, not blocking: the parenthetical itself pins the inline reading (the substantive hazard of 83-A1), the Loop section defers to `/gan-build` Phase 2 whose pointer governs the generator/evaluator passes, and no implementation dispatch is left unbriefed by this gap.

**Fix.** Either (a) add a one-line factory pointer to `gan-design.md` mirroring `gan-build.md:12` (naming the design-lead inline reading for step 0 and deferring the loop to the gan-build pointer), or (b) append the token to the step-0 parenthetical itself. Then add a verify29 assertion for `_F29` presence in `gan-design.md` so the token half of the check is guarded the same way the parenthetical half is.

## §2 — Fresh hunt: dispatch census re-derived from scratch

Base pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, `*.md`/`*.mdc`, skills/rules/commands/agents): **167 hits in 49 files**. This reconciles exactly with #83-A's 155/44 once the `.mdc` files are accounted for: #83-A's count was effectively `*.md`-only (my md-only re-count is 155 hits in 44 files, identical), and the +12 hits / +5 files are the five `.mdc` files (`rules/common-agents.mdc` 5, `rules/hackathon-mode.mdc` 4, `rules/ponytail.mdc` 1, `rules/common-development-workflow.mdc` 1, `rules/common-code-review.mdc` 1) — all previously triaged, none a new dispatch. Whole-tree base pattern: **169 hits** (167 + 2 `README.md` documentation hits), consistent with #83-A's 157 + 12 `.mdc` hits. The only run-5 tree changes are the two #83 fixes (fix29-patch-log.md: 28 changes, 0 errors), so no count delta comes from new dispatch text: §5e adds exactly one base-pattern hit ("spawned" in the new `gan-design.md:17` parenthetical) and §5f adds none.

Wider pattern (`dispatch|launch|parallel|fresh-context|isolated`, same scope): **89 files** (md+mdc) / **80 files** (md-only) vs #83-A's 84. The 84 does not reproduce exactly under either include set, so the delta is a grep-scope artifact in one of the two rounds, not a tree change — the patch log proves only the two #83 fixes touched the tree, and neither adds a wider-pattern dispatch edge (§5f's "re-dispatches" lands in `ecc-gan-planner.md`, which was already in the wider set via "launched by `/gan-build`" in its description). To settle it on merits rather than counts, I triaged by set difference every file in the wider set that is NOT in the base set (60 files, listed via `comm`) plus every agent-shaped hit from the verb sweeps below — none contains an unrecorded implementation dispatch.

New-verb sweeps (all `*.md`/`*.mdc`, skills/rules/commands/agents), each read in context:

- **`invoke … agent|skill|design-lead|deep-reasoner|fast-worker|scout|drone|subagent`:** 7 hits, all triaged. `orch-pipeline/SKILL.md:16` ("Invoke an operation skill") — skill invocation inside the routed skill, in scope. `verification-loop/SKILL.md:15`, `ai-feature-spec/SKILL.md:69` ("Invoke this skill") — skill invocation, not agent dispatch; verification-loop is verification-only. `delivery-gate/SKILL.md:41` — hook-install note, not dispatch. `feature-expansion/SKILL.md:3` (description: "subagents brainstorm new features") — **newly triaged this round:** ideation/brainstorming, no file writes; analysis-only, out of scope (and the skill is in the routing set via Phase 4 in any case). `agents/ecc-react-reviewer.md:33` ("invoke both agents" for a JSX/TSX PR) — read-only review agents, out (as in #83-A).
- **`dispatch to|dispatch the|dispatch a|dispatch an`:** 10 hits. The 6 from #83-A unchanged (orchestrate:93, :250, :400 — all inside the routed skill; gan-build:26; gan-design:17; plan.md:2 — planning only). The 4 additional hits vs #83-A's 6 are all previously-known lines this sweep's pattern now surfaces: `orchestrate/SKILL.md:103` (demo-gate text), `:205` ("enter a dispatch as a file path" — brief-composition guidance inside the routed skill), `dispatch-prompt.md:23` (design package on every UI dispatch — inside the routed template), `commands/astra-review.md:24` ("Dispatch a blind review to the deep-reasoner as a fresh subagent") — read-only blind review, out.
- **`fan-out|farm-out|hand-off|handed off`:** no new dispatch. `browser-qa/SKILL.md:22` ("hand it to `systematic-debugging`") — skill-to-skill handoff for debugging; systematic-debugging has no agent-dispatch lines of its own (MANIFEST §2(b)), out. `plan-prd.md:67` (GENERATE & HAND OFF to `/plan`) — planning, out. `save-session.md:14` (hand off context to a future session) — session continuity, out. `polish-pass/reference/impeccable-onboard.md:243` (hand off to `/impeccable polish`) — verification/polish pass, out. `pitch-deck-video/.../montage.md:108` (Archive.org-only fan-out) — research/media gathering, out. `react-performance:30`, `typescript-patterns:354` (render / `Promise.allSettled` fan-out) — code parallelism, out. `design-taste-frontend` asset READMEs ("cards fan out") and `themes/dusk.md:67` ("a hand-off in a well") — design copy, out. All remaining hits are inside the routed orchestrate skill/templates (`SKILL.md:209, :211, :213, :221, :233, :260, :264`, `references/patterns.md:13, :26`) — in-scope coverage, not new edges.
- **`launch (a|the|an|3|parallel) + agent/subagent/drone` / `parallel agents|subagents|drones|workers`:** 3 agent-shaped hits, all known: `click-path-audit/SKILL.md:167` ("Launch parallel agents per page") — read-only audit, out; `rules/common-agents.mdc:42` ("Launch 3 agents in parallel") — read-only (security/performance/type-checking), governed in-file by the `:26` factory line + `:38` read-only rule, out; `rules/common-patterns.mdc:11` ("Use parallel agents to evaluate options") — analysis/planning only, out (triaged #83-A). Remaining `launch` hits are product/Docker/CLI launches (`app-scaffold:54, :67, :76`, `production-audit` launch language), "Manually launch the orchestrator" (`commands/orch-add-feature.md:7`, `orch-change-feature.md:7`, `orch-fix-defect.md:7` — the user launching the routed orchestrator skill itself, covered by reference), and `context-budget:52` ("Never launch a provider CLI…") — a prohibition.
- **`fresh-context|fresh context`:** all verification/review — `design-taste-frontend/SKILL.md:539`, `gates.md:241`, `PROVENANCE.md:30` (hero/finish review), `orchestrate:253, :295` (second deep-reasoner pass), `dispatch-prompt.md:167` (verification-stage reviewer), `polish-pass/reference/polish.md:58` (independent re-score) — dispatched BY the orchestrator under the factory rules, out.
- **`assign … agent|subagent|drone|worker`:** 1 hit, `orchestrate/references/patterns.md:13` (pattern description inside the routed skill) — no new edge.
- **`executor|worker` agent-shaped:** 0 agent-shaped hits beyond the routed skill's own worker language (`orchestrate` description "use worker subagents", call-map trigger phrases — documentation of the routed skill).
- **`isolated`:** no agent dispatch; `polish-pass/reference/impeccable-critique.md:17, :43–44, :66` (Assessments A/B as isolated sub-agents) — verification-only, "leave it as found", out (as in #83-A). All other hits are code/design uses (isolated shifts, cut-out sets, isolated strings).
- **`agents/*.md` role files, dispatch verbs (`dispatch|launch|spawn|delegate|invoke`):** clean. `ecc-gan-evaluator.md:51` ("Launch Browser Testing") — **newly triaged:** a test step inside the evaluator role, not an agent dispatch; the evaluator is launched as a factory drone under the gan-build pointer. `ecc-a11y-architect.md:35` — self-instruction to the role itself, out (as in #83-A). `ecc-react-reviewer.md:33, :79` — read-only review agents, out. `deep-reasoner.md:9`, `fast-worker.md:9`, `scout.md:10` — role descriptions ("The orchestrator delegates … to you"); they dispatch nothing themselves. `ecc-gan-planner.md:44` — the 83-A2 site, re-routed (§1).
- **Code files (`.js`/`.mjs`/`.json`):** not re-grepped in full this round; #83-A's triage stands and no run-5 change touches code (patch log: all 28 changes are `*.md`/`*.mdc`).
- **Reference files:** `design-taste-frontend/references/copy-voice.md:173` ("a fresh reader … when the run can spare a subagent") — **newly triaged:** read-only copy review, out. `redesign.md:68` — the known in-scope dispatch, routed. `orchestrate/references/design-inventory.md:145` — reference table mentioning implementer briefs, no dispatch of its own, out. `rules/common-development-workflow.mdc:14` ("use the architect agent when the user explicitly asks you to delegate planning") — **newly triaged:** planning delegation, user-gated, no implementation work; out. `motionsites-web-builder/.../depth-and-interaction.md:255, :257` ("spawns thumbnails") — **newly triaged:** CSS animation, out. `commands/pm2.md:102–103` (`child_process` `spawn`) — **newly triaged:** process spawn, out. `rules/ponytail.mdc:9` (subagent return-message contract) — descriptive reference, out. `commands/ecc-guide.md:37, :49` — documentation of the agents directory, out. `agents/ecc-typescript-reviewer.md:44` — code guidance about `exec`/`spawn`, out.

**No new implementation dispatch found.** The only dispatch-shaped lines added since #83-A are the #83 fixes themselves (the gan-design parenthetical, the planner re-route) — routing text, not new dispatch edges. The call map was not re-run (no fix adds a dispatch edge; #80-A's restore stands).

## §3 — The 10-skill routing set: confirmed, no missing, no extra

`GLOBAL-ROUTING_F29` present in all 10 routing-set skills plus `rules/hackathon-mode.mdc`; tree-wide **15 files, 18 occurrences** (identical to #83-A). `"Factory routing (fix #29"` occurs ×1 in exactly 10 files (9 skill paragraphs + `commands/gan-build.md`). Counts re-confirmed: **67 skills / 45 agents / 48 rules / 55 commands**. `ui-ux-pro-max/` still **0 `_F29` tokens**; no `deepseek-`/`qwen-` model slugs in the built tree (model pins unchanged — fix #30's work, not this fix's).

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

Covered by reference (not in the set, governed by it): `rules/common-agents.mdc:26` factory line; `commands/gan-build.md:12` pointer; `commands/gan-design.md:17` pin (+ residual 84-A1); `agents/ecc-gan-planner.md:44` re-route; `commands/orch-refine-code.md:33` mirror; `commands/orchestrate.md`, `orch-build-mvp.md`, `orch-add-feature.md`, `orch-change-feature.md`, `orch-fix-defect.md` route to the routed skills. MANIFEST §2(b) now records **both** gan-build AND gan-design step-0 sites plus the planner fallback — the §2(b) record is complete on the three design-direction sites.

## §4 — Spot-check: the 9 reconciliations in MANIFEST §2(c) vs the live tree

All 9 spot-checked; all match the tree text. (Checked in full: 1, 2, 4, 5, 6, 7, 8; 3 and 9 by their recorded assertions plus the live lines.)

1. **Belief-in-the-brief vs NO-GUESSING (5 copies):** `"pick the reasonable option"` = 5 hits, all carrying the identical carve-out ("applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified…") plus the tie-breaker ("When in doubt which side… / When in doubt, return the question"): `orch-pipeline:72`, `orch-build-mvp:70`, `feature-expansion:151`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92`. First-build carve-out: `"instead of NEEDS_CONTEXT"` = **0**; `"state the assumption you made and proceed"` = **0** tree-wide; scope sentence ("for carrying out the briefed approach only…") at all 4 drone-side sites (`dispatch-prompt.md:96, :117, :212, :236`); tie-breaker in the governing carve-out (`dispatch-prompt.md:52`); `agents/deep-reasoner.md:17` carries the rewritten NEEDS_CONTEXT line + identical NO-GUESSING bound + tie-breaker. Matches.
2. **Merge-order fallback vs partition-by-boundary (3 sites):** the "applies only if partitioning failed" bridge present at all 3 — `orchestrate:93`, `feature-expansion:139`, `orch-build-mvp:71`. Matches.
3. **Feature-expansion Team shape vs factory cap:** Phase 4 paragraph (`feature-expansion:139`) states "one implementer per feature, up to 4 in parallel… IS the factory queue under Cursor's cap (COST-AWARE_F29)". Matches.
4. **Feature-expansion brief format vs DIRECTOR-BRIEF:** format item 2 names "the files explicitly OUT of scope (named; `none` if genuinely none)"; item 4 split into 4a acceptance criteria (`:148`) and 4b verification steps (`:149`); item 9 return format (`:154`). Matches.
5. **GAN evaluator vs VERIFY-MERGE:** ORCHESTRATOR-CHECK wiring order verified live by index arithmetic — EVALUATE 6764 < ORCHESTRATOR-CHECK 7648 < CHECK SCORE 8484 (same indices #83-B recorded); planner-spec check at `gan-build.md:30` with cap "**at most two correction re-dispatches**"; `"at most one correction"` = **0** in the built tree; GENERATE block carries `Verification steps:` (TDD tests + acceptance criteria, output pasted) and `Return format:` (status first, then files changed, test output, concerns) plus the files-out-of-scope line — 7/7 present. Skill mirrors intact (`gan-style-harness:69` Architecture note, `:155` Scoring bullet). Matches.
6. **Orchestrate contract vs DIRECTOR-BRIEF:** seventh field `Verification steps:` in the contract core (`orchestrate:235`) and templates; "files explicitly out of scope" in Constraints; no-drop rule present (`dispatch-prompt.md:4`: "delete no DIRECTOR-BRIEF field — a field with nothing to list is written as `none`, never deleted"). Matches.
7. **"Correction brief" constructed:** construction sentences in all four fix loops — `feature-expansion:158`, `orch-pipeline:74`, orchestrate ladder `:252`, GAN ORCHESTRATOR-CHECK (`gan-build.md:63`) + planner-spec 3a (`:30`). Matches.
8. **Slot refill harness-gate:** `"slots refill per wave"` = 5 hits — `orch-pipeline:62`, `feature-expansion:139`, `gan-style-harness:14`, `orchestrate:93`, `redesign.md:68`. Matches.
9. **Staged-vs-built drift by design:** not re-proven end to end this round (fix16 anchor); the recorded drift lines are unchanged in the built tree and verify29 check 7e (the narrow `_F29`-line identity check) passes — see §5. No contradiction with the tree found.

## §5 — GLOBAL-ROUTING block byte-identity (independent, not via the verifier)

- **orchestrate:** staged `new-skills/orchestrate/SKILL.md:36` md5 `bdf1720f69f9b50e3791a14c68f5c5ea` = built `skills/orchestrate/SKILL.md:36`; `diff` clean.
- **hackathon-mode:** staged `new-rules/hackathon-mode.mdc:45` md5 `39a22e9247be839a841ffbea3ad19918` = built `rules/hackathon-mode.mdc:45`; `diff` clean.
- Both match the values recorded by audits #80-A/#81-A/#82-A/#83-A. Cross-file difference remains only hackathon-mode's leading `"- "` list marker (the established DESIGNPKG-AUTO convention). No byte-identity break.

## Checked and clean

- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **261/261, exit 0** (independently re-run; includes the two new 83-A checks, both PASS in the log).
- **83-A2 verified fixed** in full (§1); **83-A1 verified fixed in substance** with the single token residual filed as 84-A1.
- **GLOBAL-ROUTING block md5s:** orchestrate `bdf1720f…`, hackathon-mode `39a22e92…` (staged = built, matching all prior rounds).
- **Census:** 10 skills; 15 files carry `GLOBAL-ROUTING_F29` (18 occurrences); `"Factory routing (fix #29"` ×1 in exactly 10 files; counts 67/45/48/55.
- **All 9 §2(c) reconciliations match the live tree** (§4).
- **Excluded set still holds** (council, click-path-audit, verification-only dispatch, polish-pass reference files, `common-patterns.mdc:11`, `common-agents.mdc:42`); newly triaged this round — feature-expansion description brainstorm, common-development-workflow planning delegation, copy-voice fresh reader, gan-evaluator "Launch Browser Testing", motionsites "spawns thumbnails", pm2 `child_process` spawn — all out of scope with reasons in §2 / the census table.
- **82-A2 cap alignment holds** (`"at most one correction"` 0×; `"at most two correction re-dispatches"` 1× at `gan-build.md:30`).
- **Model pins unchanged** (`ui-ux-pro-max` 0 `_F29`; no deepseek-/qwen- slugs).
- **Build run 5:** exit 0, fix29.py 28 changes, 0 errors (patch log + build-log-run5.txt); the only new changes vs run 4 are §5e + §5f.
- **Call map:** not re-run (no #83 fix adds a dispatch edge; #80-A's restore stands).

## Grep counts (for the record)

- Base dispatch pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|implementer`, `*.md`/`*.mdc`, skills/rules/commands/agents): **167 hits in 49 files** (155/44 md-only — exactly #83-A's count; +12 hits / +5 files are the `.mdc` files).
- Whole-tree base pattern: **169 hits** (167 + 2 `README.md` documentation hits).
- Wider pattern (`dispatch|launch|parallel|fresh-context|isolated`): **89 files** (md+mdc) / **80 files** (md-only) vs #83-A's 84 — grep-scope artifact, not a tree change (see §2).
- `dispatch to|dispatch the|dispatch a|dispatch an` sweep: **10 hits** (6 from #83-A + 4 known lines: orchestrate:103, :205, dispatch-prompt:23, astra-review:24).
- `"Factory routing (fix #29"`: **10 files ×1**.
- `GLOBAL-ROUTING_F29`: **15 files, 18 occurrences**.
- `"slots refill per wave"`: **5 hits**.
- `"pick the reasonable option"`: **5 hits, all 5 carved + tie-breaker**.
- `"state the assumption you made and proceed"`: **0 hits tree-wide**.
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"at most one correction"`: **0 hits in the built tree**; `"at most two correction re-dispatches"`: **1 hit** (`commands/gan-build.md:30`).
- `"invoke the design-lead (model \`grok-4.7-high\`) to generate it"`: **0 hits** (83-A2 fix confirmed).
- `_F29` in `commands/gan-design.md`: **0** (finding 84-A1); `_F29` in `skills/ui-ux-pro-max/`: **0**.
- `"dispatch to the design skill"`: **2 sites only** (`commands/gan-build.md:26`, `commands/gan-design.md:17`) — no third copy exists.
- GLOBAL-ROUTING block md5s: orchestrate `bdf1720f69f9b50e3791a14c68f5c5ea`, hackathon-mode `39a22e9247be839a841ffbea3ad19918` (staged = built).

## Census table — every dispatch hit, in/out of scope + reason

Base-pattern files (49). "Covered by reference" = governed by a routed skill's factory rules via an explicit pointer/pin, not carrying its own factory paragraph.

| File (base hits) | Disposition | Reason |
|---|---|---|
| skills/orchestrate/SKILL.md (40) | IN SCOPE, routed | GLOBAL-ROUTING block :36 + step-4 factory bridge :93 |
| skills/feature-expansion/SKILL.md (26) | IN SCOPE, routed | Factory paragraph :139; description :3 "subagents brainstorm" is ideation only, no file writes |
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
| commands/gan-design.md (1) | COVERED BY REFERENCE + PINNED | Step-0 pin :17; loop defers to gan-build Phase 2; residual 84-A1 (0 `_F29` tokens) |
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
| skills/design-taste-frontend/assets/** READMEs, themes/dusk.md:67 | OUT | "Cards fan out" / "a hand-off in a well" — design copy |
| agents/ecc-performance-optimizer.md:254, agents/ecc-refactor-cleaner.md:39 | OUT | `Promise.all` / detection tools in parallel — code parallelism |
| skills/orchestrate/SKILL.md:103, :205, :209, :211, :213, :221, :233, :260, :264; references/patterns.md:13, :26; dispatch-prompt.md:23 | IN SCOPE | Inside the routed skill / routed templates — fan-out, dispatch-composition and handoff rules, not new edges |
| skills/orchestrate/SKILL.md:93, :250, :400 | IN SCOPE | Step-4 factory bridge, NEEDS_CONTEXT re-dispatch, Gotchas fallback (dispatched through dispatch-prompt templates) |
| skills/design-taste-frontend/references/hallmark/PROVENANCE.md:30; skills/polish-pass/reference/impeccable-PROVENANCE.md; skills/polish-pass/reference/lenses/*.md | OUT | Provenance notes / verification lenses — no dispatch |
| commands/sessions.md:294 | OUT | Parallel tmux/worktree runs — session bookkeeping |
| rules/arkts-hooks.mdc, react-native-patterns.mdc, react-patterns.mdc, react-testing.mdc, web-hooks.mdc, web-patterns.mdc; skills/frontend-patterns/SKILL.md, motion-patterns/SKILL.md, react-patterns/SKILL.md, react-testing/SKILL.md, mobile-ship/**, pitch-deck-video/**, app-scaffold/reference/**, e2e-testing/SKILL.md, hackathon-pitch/**, frontend-slides/** | OUT | "Launch"/"parallel"/"isolated" as product launch, code parallelism, or design-pattern language — no agent dispatch in any of them |
