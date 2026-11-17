# Fix #29 (DRAFT SPEC) — Adaptable orchestration: forced orchestrator, dynamic drone fan-out, director-grade briefs

**Status:** DRAFT spec, written Nov 16, 2026. Starts after fix #28 lands. Prerequisite for fix #30 (model transfer: Carbon brain + dual drones). Do not start while #28 runs (two agents must never edit the plugin tree at once).

## Goal

Make the plugin maximally adaptable: every prompt is answered by the orchestrator model; the orchestrator runs a factory dispatch, a queue of independent single-task drones, spawning a drone per task, retiring it on completion, and dispatching the next queued task into the freed slot; drones are directed so precisely that they execute exactly what the orchestrator wants, so system-level output matches orchestrator-level performance at drone cost. This routing is forced throughout the plugin: every skill uses it when making something.

## Rules / mechanisms

1. **ORCHESTRATOR-ONLY** (extends `ALWAYSLEAD_F27`): every user-prompt response comes from the orchestrator model. Drones never answer the user directly and never decide scope. All drone output flows back through the orchestrator, which verifies and presents it.
2. **FACTORY-DISPATCH:** the orchestrator keeps a queue of independent single-task jobs and dispatches drones into free slots: one drone per task, retired on completion, the next queued task dispatched into the freed slot, like a factory line. The orchestrator picks the best drone model per task (DeepSeek for reasoning, Qwen for coding, per fix #30) and the concurrency by decomposability. Cap = what the harness supports (see Honest limits). Never split work that shares files or mutable state across drones: partition by file/module boundary. The orchestrator merges and verifies all drone output.
3. **DIRECTOR-BRIEFS:** every drone brief must carry the exact goal, the files in scope (and explicitly out of scope), constraints, acceptance criteria, verification steps, and what to return. A brief missing any of these is incomplete and the drone must not start. Brief precision is the whole mechanism: the brief is written so completely that the drone only executes, it never has to judge. **NO-GUESSING:** if a brief leaves a decision unspecified, the drone stops and returns the question to the orchestrator instead of guessing. The drone never invents scope, files, or acceptance criteria.
4. **VERIFY-AND-MERGE:** the orchestrator verifies every drone output against the brief's acceptance criteria (plus browser-qa for visual work, audits for code). Failed output goes back to a drone with a correction brief. The orchestrator never silently accepts below-bar work and never presents unverified drone output as its own.
5. **GLOBAL-ROUTING** (same pattern as `DESIGNPKG-AUTO`): this routing is automatic for ALL making/building work in every skill, not opt-in. Byte-identical statement in orchestrate + hackathon-mode, with a weaving check in the sweep.
6. **COST-AWARE:** fan-out is bounded by efficiency, not just speed. Ten drones on a small job wastes tokens because each drone carries its own context. The orchestrator must justify N>3 in one line (what partitions justify it). Drones carry minimal context: only the files and facts their partition needs.

## Honest limits (design constraints, not bugs)

- **More drones is not always faster.** Parallelism helps only on independent work; coordination, merging, and verification grow with N, and each drone is its own model session, so five parallel drones use roughly five times the tokens of one agent doing the same work in sequence. The cap follows the harness, and the default is the smallest concurrency that fits the queue.
- **The gap lives in unspecified parts, not in execution.** A precisely briefed drone executes exactly what the orchestrator wants. Where the brief is incomplete or reality surprises the drone, the no-guessing rule sends it back to the orchestrator and verification catches the rest. System-level orchestrator performance comes from brief precision + verification, not from drone intelligence.
- **Cursor cannot run this factory reliably (verified Nov 16, 2026; count corrected same day).** Two hard limits: (a) per-subagent model selection is unreliable, the Task tool's available models are coupled to the last-clicked dropdown and specific model IDs get rejected or silently fall back to the parent/fast model, so deterministic Carbon-to-DeepSeek/Qwen routing cannot run reliably in Cursor IDE (confirmed still broken in Cursor forum thread 176252, Nov 2026); (b) in-IDE parallelism runs up to 8 agents in isolated git worktrees, but extras wait for the entire first batch to finish instead of filling slots as they free up, so factory slot-refill does not work, and parallel agents do not coordinate with each other. Cloud Agents run 8-10+ in isolated VMs but are a separate product surface, not the in-IDE plugin. The harness decision (stay in Cursor simplified vs switch terminal) is open, pending Anish's call. Claude Code terminal runs this pattern natively (Task tool, per-subagent model, up to 20 concurrent by default) but only with Claude models on Pro/API; OpenCode terminal preserves the Carbon/DeepSeek/Qwen stack via API keys. Either switch means porting the plugin, which is a real project, not a flip of a switch.

## Scope

- Add the routing rules + anchor tokens (`ORCHESTRATOR-ONLY_F29`, `FACTORY-DISPATCH_F29`, `DIRECTOR-BRIEF_F29`, `NO-GUESSING_F29`, `VERIFY-MERGE_F29`, `GLOBAL-ROUTING_F29`, `COST-AWARE_F29`); weave into orchestrate, hackathon-mode, and every skill that dispatches implementation work.
- Update the verifier with checks for the routing statements + a fan-out/brief-completeness check.
- Do NOT change: model pins (that is fix #30), the debloat from #28, the design package, grill-me.
- Constraints: author Anish Koduri <akoduri05@gmail.com> only, NO `Co-authored-by: Cursor` trailer, no AI tool as contributor/author; build.sh is the source of truth; staged sources only; never re-run fix11/fix11-stage.py; fix dirs stay; do NOT push (create a verified git bundle for the Windows pull).

## Verification

- Audit loop (at least 2 rounds) + sweep + dry-run, with HONEST verdicts: record NOT MET as written if the final audit or sweep carries a minor fixed post-hoc without a re-audit/re-sweep, per the fix #27 convention.
- The dry-run must include a factory leg: a queue of independent tasks dispatched through slots with retire-and-refill, verifying partitioning (no shared files), brief completeness, no-guessing behavior, and orchestrator merge/verification.
- Live test (Anish, in Cursor, after fix #30): the orchestrator runs a multi-part build and reports N drones, partitions, and verification outcomes.
