# fix29 run log

## Errors (0)
- none

## Changes (33)
- skills/orch-pipeline/SKILL.md: patched anchor :: 'each phase names its operating skill before delegating; a decision with no named'
- skills/orch-pipeline/SKILL.md: patched anchor :: "if a detail is ambiguous, they pick the reasonable option and note it, they don'"
- skills/orch-pipeline/SKILL.md: patched anchor :: 'findings route to the capped 2-round fix loop (max 3 rounds total); if the app c'
- skills/orch-build-mvp/SKILL.md: patched anchor :: 'Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.'
- skills/orch-add-feature/SKILL.md: patched anchor :: 'Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.'
- skills/orch-fix-defect/SKILL.md: patched anchor :: 'Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.'
- skills/orch-refine-code/SKILL.md: patched anchor :: 'Thin wrapper over the shared\nengine in [`orch-pipeline`](../orch-pipeline/SKILL.'
- skills/orch-change-feature/SKILL.md: patched anchor :: 'Thin wrapper over the\nshared engine in [`orch-pipeline`](../orch-pipeline/SKILL.'
- skills/gan-style-harness/SKILL.md: patched anchor :: 'creating an adversarial feedback loop that drives quality far beyond what a sing'
- skills/gan-style-harness/SKILL.md: patched anchor :: '## The Three Agents'
- skills/gan-style-harness/SKILL.md: patched anchor :: '- **Max iterations** = 15 (configurable, typically 5-15 sufficient)'
- census: GLOBAL-ROUTING block byte-identical in orchestrate + hackathon-mode
- census: all 10 in-scope skills + hackathon-mode carry GLOBAL-ROUTING_F29; all 7 _F29 tokens in the block
- skills/orch-build-mvp/SKILL.md: patched anchor :: "if a detail is ambiguous, they pick the reasonable option and note it, they don'"
- skills/orch-build-mvp/SKILL.md: patched anchor :: 'If two implementers in the same wave touched the same files, decide the merge or'
- skills/orch-refine-code/SKILL.md: patched anchor :: '2. For dead-code / duplication sweeps, delegate to the `refactor-cleaner` agent '
- skills/orch-refine-code/SKILL.md: patched anchor :: 'The orchestrator answers every prompt; drones never answer the user or decide sc'
- commands/orch-refine-code.md: patched anchor :: 'Dead-code/dup sweeps\n   delegate to `refactor-cleaner` agent (`agents/ecc-refact'
- commands/orch-refine-code.md: patched anchor :: 'The skill\n(via the shared `orch-pipeline` engine) will:'
- rules/common-agents.mdc: patched anchor :: "No user prompt needed — subject to the orchestrate skill's routing rule, which g"
- commands/gan-build.md: patched anchor :: '## GAN-Style Harness Build'
- commands/gan-build.md: patched anchor :: '- Read spec.md and `docs/design-tokens.md` (the tokens file carries the decision'
- commands/gan-build.md: patched anchor :: '3. Display the spec summary to the user\n4. Proceed to Phase 2'
- commands/gan-build.md: patched anchor :: '    # Wait for evaluator to finish\n\n    # CHECK SCORE'
- commands/gan-build.md: patched anchor :: '    - Ensure dev server is running\n    - Commit changes'
- commands/gan-build.md: patched anchor :: 'and record it in `docs/design-tokens.md`, then launch the planner with that reco'
- commands/gan-design.md: patched anchor :: 'and record it in `docs/design-tokens.md`, then restate that recorded direction i'
- commands/gan-design.md: patched anchor :: '3. `--pass-threshold N` — (optional, default 7.5) weighted score to pass (higher'
- agents/ecc-gan-planner.md: patched anchor :: 'if this agent is ever launched with no direction recorded, invoke the design-lea'
- commands/react-build.md: patched anchor :: 'This command invokes the **react-build-resolver** agent to incrementally fix Rea'
- commands/react-build.md: patched anchor :: '5. **Report Summary**: Show what was fixed and what remains'
- commands/astra-review.md: patched anchor :: '- Fixes go to **fast-worker** (`cursor-grok-4.6-high-fast`) for mechanical fixes'
- commands/astra-review.md: patched anchor :: '- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to '

## Command decisions (0)
- none

## OWED (5)
- OWED-29-1 (SPEC §6): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the routing adds no new dispatch edges (no new skill invocations), counts are unchanged (67/45/48/55/15/49), and the fix28 map stands. Verified by regenerating twice with the fix28 generator copy and diffing: 2-line diff (error-handling purpose-order noise + one pre-existing git-workflow staged invoker), neither a fix #29 edge; the fix28 map was restored byte-identical (md5 b066413a…) — see MANIFEST §2(d).
- OWED-29-2 (SPEC Honest limits): live factory behavior (per-model dispatch, slot refill at scale) is harness-gated — in Cursor, per-subagent model selection is unreliable and in-IDE parallelism caps around 4 with no slot refill. The dry-run factory leg verifies the design statically (partitioning, brief completeness, no-guessing, merge/verification), not live Cursor dispatch. It lights up fully on the later port.
- OWED-29-3 (SPEC §1 scope rule, corrected by audit #80-A1): council and click-path-audit dispatch parallel/review subagents but no implementation work, so they carry no factory routing line (audit #80-A rows 15-16 confirm). design-taste-frontend was wrongly in this list — its Hallmark redesign flow dispatches implementation subagents, so it is in the routing set (10 skills) with the paragraph in redesign.md. Recorded for the audit to challenge: if the audit finds an implementation dispatch in council or click-path-audit, it belongs in the routing set.
- OWED-29-4 (fix #30 handoff): the DeepSeek/Qwen model assignment in the GLOBAL-ROUTING block is a forward reference to fix #30; no model pins change in this fix. verify29 asserts the Grok pins are unchanged and no deepseek-/qwen- model slugs exist in the built tree.
- OWED-29-5 (audit #80-B13, partially rejected; enumeration corrected per audit #91-B nit 2): the 41 staged-vs-built diff lines across 4 files (orchestrate :100/:274/:281 agent-citation expansions, hackathon-mode :38 `claude -p` -> CLI-subprocess, feature-expansion 11 changed lines, design-taste-frontend description block 5 lines -> 6) are BY-DESIGN build-time transforms, NOT synced — fix16.py:3808 anchors on the staged `claude -p` wording with count==1 and fails the build (exit 1) if the anchor misses, so syncing staged to the built text would break the build. No full-file staged-vs-built identity check is added; verify29 instead asserts the _F29 lines are byte-identical staged-vs-built (the actual fix #29 regression risk).
