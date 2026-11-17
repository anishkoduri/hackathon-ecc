# fix30 run log

## Errors (0)
- none

## Changes (27)
- census: grok-4.7-high x49, 'Grok 4.7 High' x22, cursor-grok-4.6-high-fast x70, bare grok-4.6-high-fast x0, grok-4.7-extra-high x0, 'Grok 4.7 Extra High' x0, 154 non-UTF-8 file(s) skipped (byte-checked, no pin text)
- README.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x3)
- rules/common-agents.mdc: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- rules/common-performance.mdc: pin renamed (grok-4.7-high x2, 'Grok 4.7 High' x0)
- rules/hackathon-mode.mdc: pin renamed (grok-4.7-high x2, 'Grok 4.7 High' x3)
- skills/strategic-compact/SKILL.md: pin renamed (grok-4.7-high x0, 'Grok 4.7 High' x2)
- skills/gan-style-harness/SKILL.md: pin renamed (grok-4.7-high x3, 'Grok 4.7 High' x0)
- skills/orch-add-feature/SKILL.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- skills/orch-build-mvp/SKILL.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- skills/orch-change-feature/SKILL.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- skills/orch-fix-defect/SKILL.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- skills/orch-refine-code/SKILL.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- skills/orchestrate/SKILL.md: pin renamed (grok-4.7-high x15, 'Grok 4.7 High' x12)
- skills/orchestrate/references/agent-TEMPLATE.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- agents/deep-reasoner.md: pin renamed (grok-4.7-high x3, 'Grok 4.7 High' x0)
- agents/ecc-architect.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- agents/ecc-gan-planner.md: pin renamed (grok-4.7-high x2, 'Grok 4.7 High' x0)
- agents/ecc-healthcare-reviewer.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- agents/ecc-spec-miner.md: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- commands/astra-review.md: pin renamed (grok-4.7-high x3, 'Grok 4.7 High' x1)
- commands/gan-build.md: pin renamed (grok-4.7-high x2, 'Grok 4.7 High' x0)
- commands/gan-design.md: pin renamed (grok-4.7-high x3, 'Grok 4.7 High' x0)
- commands/model-route.md: pin renamed (grok-4.7-high x2, 'Grok 4.7 High' x0)
- schemas/agent.schema.json: pin renamed (grok-4.7-high x1, 'Grok 4.7 High' x0)
- manifests/pi-core.json: pin renamed (grok-4.7-high x0, 'Grok 4.7 High' x1)
- post: grok-4.7-extra-high x49, 'Grok 4.7 Extra High' x22, grok-4.7-high x0, 'Grok 4.7 High' x0, cursor-grok-4.6-high-fast x70 (unchanged), bare grok-4.6-high-fast x0
- guard: GLOBAL-ROUTING block byte-identical in orchestrate + hackathon-mode (rename did not touch it)

## Command decisions (3)
- DECISION-30-1 (SPEC re-scope): the rename is build-time only, last in build order (after fix29.py, before STEP 5 Counts). Staged sources (new-skills 19 + new-rules 2 ID occurrences, plus 15 staged prose occurrences) and build.sh inline content (54 pre-existing ID occurrences on 50 lines, plus 5 prose occurrences) keep the old pin because fix16.py, fix24.py and fix29.py anchor on that text and abort the build on anchor mismatch. Precedent: fix #16 performed the Claude -> Grok pin change at build time via fix16.py. The staged-vs-built pin drift is by design (OWED-30-1).
- DECISION-30-2 (prose): all 22 'Grok 4.7 High' prose occurrences change to 'Grok 4.7 Extra High', including skills/strategic-compact/SKILL.md:68 (the '500k Grok 4.7 High' context-window example) and :102 (the Cursor 2.1.233 todo-tools note) — the note's operative claim is preserved by its 'and newer' clause. Uniformity over a carve-out: a mixed tree (some prose old, some new) would read as a half-finished rename and break the exact-count assertions. Recorded as OWED-30-5 for the audit to challenge.
- DECISION-30-3 (census strictness): the pre-rename census asserts exact counts (49/22/70/0) and refuses to write on any drift. A partial rename is worse than a failed build — the build must fail loudly rather than ship a tree where some files say high and others say extra-high.

## OWED (5)
- OWED-30-1 (SPEC re-scope, by design): staged-vs-built pin drift — staged sources keep the old pin (new-skills/ 19 ID + 12 prose occurrences, new-rules/ 2 ID + 3 prose occurrences) and build.sh inline content keeps it (54 pre-existing ID occurrences on 50 lines + 5 prose occurrences; the fix30 hook block itself adds 2 meta-mentions). Syncing staged to the built text would break the fix16/fix24/fix29 anchors and fail the build. Same class as OWED-29-5's 41 lines. verify30 asserts the pins in the BUILT tree only.
- OWED-30-2 (OWED-29-4 override): the DeepSeek/Qwen model assignment in the GLOBAL-ROUTING block stays a forward reference — the drone assignment lives in the factory copy per FACTORY_CURSOR_PLAN.md, NOT in #30. verify30 still asserts no deepseek-/qwen- model slugs in the built tree and the names occur only in the GLOBAL-ROUTING block (check 9b, unchanged).
- OWED-30-3 (SPEC Honest limits): live Extra High behavior is unverified until Anish runs the live-test prompt (fix30/live-test-prompt.md) in Cursor — pass = Extra High ran the parent on both tasks. The live smoke test is still skipped since Nov 15.
- OWED-30-4 (SPEC §6, same as OWED-29-1): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the pin change adds no new dispatch edges and counts are unchanged (67/45/48/55/15/49); the fix28 map stands.
- OWED-30-5 (prose judgment, audit to challenge): skills/strategic-compact/SKILL.md:68 and :102 prose changed to 'Grok 4.7 Extra High' (see DECISION-30-2). If the audit finds either line should have kept 'Grok 4.7 High' (historical note / context-window example), the fix is a two-line carve-out in fix30.py plus updated census counts — not a re-scope.
