# Drone-Factory Cursor Variant — Implementation Plan

**Written:** Mon Nov 16, 2026, ~7:30 PM CT. **Status:** plan only — no tree edits yet.
**Owner:** Anish. **Rule:** two agents must never edit the same plugin tree at once.

## 0. Decisions this plan rests on (all made Nov 16, 2026)

- **Brain: Grok 4.7 on Extra High, in Cursor, on the pool.** Chosen over OpenCode / Hydrogen because Cursor is the best value per token: $30/mo buys ~$3,100–3,700/mo of Grok API value at his pace (~323M tokens/week vs ~274–383M observed Premium weekly capacity). No other subscription covers his volume. Accepted costs: the pool drains faster (expect to hit the limit mid-week on heavy weeks), and subagents still won't run Extra High (Cursor's per-subagent routing is broken; parent-only).
- **Drones: DeepSeek V3.2 (reasoning) + Qwen3 Coder 30B A3B Instruct (coding), via OpenRouter.** Added to Cursor through Override OpenAI Base URL at `https://openrouter.ai/api/v1/cursor` (the dedicated endpoint — plain `/api/v1` breaks tool calls), model IDs `deepseek/deepseek-v3.2` and `qwen/qwen3-coder-30b-a3b-instruct`. They bill to OpenRouter credits (~$0.21/$0.31 DeepSeek, $0.15/$0.60 Qwen), not the pool. Default effort (medium) is fine for drones. The normal provider-key BYOK route is chat-only; the OpenRouter override route is the exception and its docs say the models work in the chat and agent panel.
- **OpenCode stays as the fallback** for when the pool runs out. `~/workspace/your_files/opencode-setup.md` is unchanged by this plan.
- **Sequencing: finish the regular version first, save it, then fork a new copy for the factory.** The factory does NOT go into the regular plugin. Fix #29 stays as specced (best-effort routing in Cursor); the factory mechanisms live only in the copy.
- **Dispatch is orchestrator-only (Anish, Nov 16, ~7:34 PM CT):** Anish does NOT open new chats himself. The orchestrator opens drone sessions and picks the model. The two automated mechanisms in §2 (custom subagents, CLI) are the only dispatch routes — there is no manual fallback.

## 1. Goals — better, faster, cheaper

- **Better output:** the orchestrator (Extra High) plans, writes precise briefs, and verifies every drone output (VERIFY-MERGE). Drones execute exact briefs and stop with a question instead of guessing (NO-GUESSING).
- **Faster output:** drones run in parallel (FACTORY-DISPATCH), one independent single task each; a finished drone's slot is handed to the next task.
- **Cheaper output:** bulk implementation tokens go through the OpenRouter drones instead of the pool's Grok. Only the orchestrator's planning / briefing / verification tokens use the pool. Brief tokens count too — the efficiency rules in §2 keep every brief small, so instructing a drone never costs more than the work itself.

## 2. Architecture — how the factory actually works in Cursor

- **Orchestrator:** the parent agent, Grok 4.7 Extra High, in Cursor.
- **Drones:** one of three dispatch mechanisms, tried in this order. The live test (Phase 4) decides which ones actually work; a mechanism that fails is recorded and skipped, never silently accepted.
  1. **Custom subagents** — `.cursor/agents/drone-reasoning.md` (model `deepseek/deepseek-v3.2`) and `.cursor/agents/drone-coding.md` (model `qwen/qwen3-coder-30b-a3b-instruct`), both `is_background: true`. Cursor's docs say the frontmatter `model` field is honored for a different model family. The known bug is effort-level pinning within Grok, so a different family may stick. UNVERIFIED for OpenRouter IDs.
  2. **cursor-agent CLI fan-out** — the orchestrator runs `cursor-agent --force -p "<brief>" --model <id>` from its terminal. Each call is a fresh agent session (a new chat) in the folder; it does the brief, prints the result, and the orchestrator verifies and merges it. Several run in the background for parallelism. Community-discovered, not formally documented. UNVERIFIED for OpenRouter IDs and on his Windows machine. CLI usage draws from the same weekly pool for pool models; for OpenRouter models it should bill to OpenRouter credits (unverified).
  **No manual step.** Anish does not open new chats himself — the orchestrator opens drone sessions and picks the model. The two mechanisms above are the only dispatch routes.
  - **Not mechanisms:** `/multitask` (subagents inherit the parent model), "Use Multiple Models" (best-of-N competition, not orchestration), the Cursor Router (Teams/Enterprise only; does not control subagents).
- **Rules carried over from fix #29 (harness-agnostic):** ORCHESTRATOR-ONLY, FACTORY-DISPATCH (queue, one drone per task, retire-and-refill, partition by file/module boundary, cap = harness = 8 parallel agents in Cursor), DIRECTOR-BRIEF (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return; an incomplete brief means the drone does not start), NO-GUESSING, VERIFY-MERGE, GLOBAL-ROUTING (automatic for all making/building work), COST-AWARE (justify N>3 in one line; minimal drone context).
- **OpenRouter setup skill:** a new skill that walks the user through Settings > Models > API Keys > OpenAI API Key (paste the OpenRouter key) > Override OpenAI Base URL = `https://openrouter.ai/api/v1/cursor` > + Add model (the two IDs) > verify (pick the model in a chat, send a test prompt, confirm it answers and bills to OpenRouter). It must state: the key is NEVER written into the plugin or any file — the user enters it in Settings only. Caveats to include: Auto and Composer 2 may not route through the key (pick drone models explicitly); Cursor sends no reasoning effort through the override, so drones run at default effort; Zero Data Retention does not apply to BYOK traffic; the key is sent to Cursor's backend with each request and is not stored there.
- **Cost accounting:** extend the existing cost tracker to record, per build, pool % used (orchestrator) + OpenRouter tokens/$ per drone. Each build report carries one line: pool X%, OpenRouter $Y.

### Prompting, efficiency, and smart routing

- **Orchestrator prompting skill** (new skill, e.g. `orchestrator-briefing`): how the orchestrator instructs drones. One-shot, not a conversation — brief in, result out, no back-and-forth (each round-trip costs tokens and context). The brief template: goal in one line; files in/out of scope as paths (never pasted content — the drone reads them); constraints as bullets; acceptance criteria as checkable items; verification steps; what to return and in what format. Correction briefs send only the delta (what was wrong + the exact fix), never the full brief again. If a drone returns a question (NO-GUESSING), the orchestrator answers it in one line and re-issues the brief once.
- **Efficiency — briefs stay small:** a brief has a budget (proposed: ~300 words / ~1,500 tokens; anything over it must be split or justified — an over-budget brief is usually a sign the task is too big for one drone). The orchestrator never pastes file contents into a brief; it names paths. Shared context goes in a file once and every drone reads it, instead of being pasted into each brief. Drones return only the result in the requested format (files changed, diff summary, test output) — no explanations, no restating the brief, no status chatter. The orchestrator does trivial work itself: if the task is smaller than the brief would be, do it directly instead of spawning a drone. The orchestrator verifies by reading the actual files (VERIFY-MERGE), not by having the drone paste file contents back.
- **Smart routing — which drone does what:**
  - DeepSeek V3.2 (`drone-reasoning`): reasoning-heavy work — complex logic, algorithm design, debugging a subtle bug, structured data, multi-step tool chains, code review that needs judgment. 164K context; $0.21/$0.31.
  - Qwen3 Coder 30B (`drone-coding`): mechanical / repo-scale coding — implement a specified feature, write tests, refactor to a pattern, bulk edits, boilerplate. 262K context (best for repo-scale); $0.15/$0.60, the cheaper of the two.
  - Orchestrator itself (Grok 4.7 Extra High): planning, decomposition, briefs, verification/merging, and anything smaller than a brief. Never route thinking work to a drone, and never route drone work to the orchestrator (the expensive model doing cheap work).
  - Tiebreaker: reasoning-heavy → DeepSeek; mechanical/repo-scale → Qwen; both → the orchestrator judges which dominates and says so in one line (carried over from the fix30 tiebreaker).
  - Parallel vs sequential: independent tasks go to separate drones in parallel; a task that depends on another drone's output goes after it, with that output as its input.
  - No-drone rule: a single-file trivial change, or work where the orchestrator already has the context loaded, is done directly — spawning a drone would re-read the same files and cost more.

## 3. Phases

### Phase 0 — Fix #29 lands (IN FLIGHT)
- Coordinator 9ed6eacd, running since ~3:45 PM CT Nov 16. Verify when it reports: commit on top of 98d72af, author Anish Koduri only, no `Co-authored-by` trailer, verified bundle, audit/sweep/dry-run reports present. **No other tree edit starts until #29's report is in.**

### Phase 1 — Finish the regular version
- **1a. Re-scope fix #30** (SPEC updated Nov 16 — see the RE-SCOPE note in `fix30/SPEC.md`): orchestrator pin `grok-4.7-high` → `grok-4.7-extra-high` everywhere it appears (585 mentions in the fix28 tree), plus verifier pin assertions updated. Drone routing stays #29's best-effort. Carbon is out, Grok-via-OpenRouter brain is out, Hydrogen brain is out, the $5 Google Cloud prepay is out. Live test: orchestrator on one reasoning-heavy task + one repo-scale coding task, reporting which model ran; pass = Extra High ran the parent.
- **1b. Run fix #30** (coordinator, same discipline as #27–#29: audit loop ≥2 rounds + sweep + dry-run, HONEST verdicts, standalone report files, commit + verified bundle, NO push).
- **1c. Run fix #31** (design libraries per `fix31/SPEC.md`: GetLayers free set only, GSAP, React Bits, Hairline illustrations; audit loop + sweep + dry-run with a design leg using at least one item from each source; commit + verified bundle, NO push).
- **1d. Save the regular version:** final commit on top of the #31 commit; one verified bundle of the whole tree at that commit. Record the commit hash + bundle path in this plan and in MEMORY. This is the fork point. Do not push.

### Phase 2 — Fork
- Copy the saved regular tree to `~/workspace/hackathon-plugin/factory-cursor/` (a full plugin tree, not a patch). Record the base commit hash, fork date, and a MANIFEST line stating it is the factory variant forked from that commit. The copy gets its own SPEC (`FACTORY_SPEC.md`) and its own verifier (`verify-factory.py`).
- **Concurrency rule:** one agent edits one tree at a time. The regular tree and the factory tree are different directories, so one agent may work in each — never two agents in the same tree.

### Phase 3 — Implement the factory in the copy
- **3a. OpenRouter setup skill** (new skill, e.g. `openrouter-drones`): the setup steps, the `/cursor` endpoint, both model IDs, verification steps, and all caveats from §2. Woven into orchestrate + hackathon-mode as a prerequisite: the factory requires the drones to be installed before dispatch.
- **3b. Custom subagents:** `.cursor/agents/drone-reasoning.md` and `.cursor/agents/drone-coding.md` with the `model` frontmatter, `is_background: true`, and the DIRECTOR-BRIEF contract in their instructions (what a brief must contain, NO-GUESSING, what to return).
- **3c. CLI dispatch rule** (e.g. `CLI-DISPATCH_F32`): the orchestrator may spawn drones via `cursor-agent --force -p "<brief>" --model <id>` from its terminal, one per task, backgrounded; output is captured, verified (VERIFY-MERGE), merged; failures go back with a correction brief. Include the Windows notes (`cursor-agent --help` to verify it is on PATH via the Cursor install; `--force` auto-approves writes).
- **3d. Weave:** GLOBAL-ROUTING (from #29) now binds the two dispatch mechanisms in priority order (custom subagent → CLI), with a fallback rule: if the first fails (model falls back to Auto/Composer/Grok, or the CLI errors), the orchestrator records the failure and uses the second — never silently accepts a wrong model. If both fail, the factory is not viable in Cursor (see Phase 4). Which mechanism ran each drone is recorded in the build log.
- **3e. Cost accounting** (from §2): pool % + OpenRouter $ per build.
- **3f. `verify-factory.py`:** passes only if all of these hold — both subagent files exist with the exact model IDs; the CLI dispatch rule exists; the OpenRouter setup skill exists and contains the `/cursor` endpoint and both IDs; no API key or secret appears anywhere in the copy (grep for `sk-or-` and key-like values); the orchestrator pin is `grok-4.7-extra-high`; the #29 factory rules are present and byte-identical in orchestrate + hackathon-mode; the routing table exists and names both drones with their task types; the brief template exists; the efficiency rule exists with the brief budget stated.
- **3g. Orchestrator prompting skill** (e.g. `orchestrator-briefing`): the brief template, one-shot discipline, correction-brief deltas, and the one-line answer to a drone's question. Woven into orchestrate + hackathon-mode alongside DIRECTOR-BRIEF.
- **3h. Brief-efficiency rule** (e.g. `BRIEF-EFFICIENCY_F32`): the brief budget (~300 words / ~1,500 tokens, split or justify if over), paths-not-pasted-content, shared context in a file once, result-only returns, and the do-it-yourself threshold for trivial work.
- **3i. Smart-routing rule + table** (e.g. `SMART-ROUTING_F32`): the routing table from §2 (DeepSeek = reasoning, Qwen = mechanical/repo-scale, orchestrator = planning/verification/trivial), the tiebreaker, parallel-vs-sequential, and the no-drone rule. The drone subagent files and the CLI dispatch rule reference it, so every dispatch decision cites the row it used.

### Phase 4 — Live test (Anish in Cursor; the "actually works" proof)
- **Baseline first:** run a fixed benchmark build (proposed: a small landing page — hero, one component, one test; Anish may name a different one) with Grok-only (no factory). Record wall-clock time, pool % used, and quality notes.
- **Then the same build through the factory,** once per automated dispatch mechanism (custom subagent, CLI). Record for each: which model actually ran each drone (subagent task card / CLI output), wall-clock time, pool % used, OpenRouter spend.
- **Pass criteria:** (i) at least one AUTOMATED dispatch mechanism runs the chosen drone models (not Auto/Composer/Grok); (ii) factory wall-clock < Grok-only wall-clock; (iii) factory pool % + OpenRouter $ is cheaper in real money than the Grok-only run's API value; (iv) output quality at least as good (orchestrator verify-merge + a short quality checklist in the SPEC).
- **If a mechanism fails,** record it honestly and fall back. **If NO mechanism works,** the factory is not viable in Cursor: say so immediately (lock-in rule) and the fallback is OpenCode for drones, or Grok-only in Cursor. Never silently accept a failed mechanism.

### Phase 5 — Audit, sweep, dry-run, save
- Audit loop ≥2 rounds + sweep + dry-run with a factory leg (a real build through the factory, at least one drone of each type). Honest verdicts; standalone report files. Commit as Anish Koduri only, no trailer. Verified bundle. NO push. The copy's MANIFEST records the live-test results (which mechanisms passed/failed) so the next session knows what actually works.

## 4. Risks (with mitigations)

- **R1 — Custom-subagent model field may not stick for OpenRouter IDs** (the `<available_subagent_models>` bug). Mitigation: CLI dispatch; manual fallback; live test decides; record honestly.
- **R2 — CLI pattern is community-discovered, undocumented; may differ on Windows** (PATH, auth, `--force` behavior). Mitigation: verify `cursor-agent --help` first; one test call before building on it.
- **R3 — OpenRouter override:** Auto/Composer 2 may not route through the key; effort is default. Mitigation: pick drone models explicitly; drones are fine at default effort.
- **R4 — Pool drain:** the Extra High orchestrator drains the pool faster; any drone on a pool model drains it faster still. Mitigation: drones are OpenRouter (not pool); track pool % per build; OpenCode fallback when the pool runs out.
- **R5 — Two trees, one editor at a time.** Mitigation: the concurrency rule in Phase 2.
- **R6 — Secrets:** the OpenRouter key must never be written into the plugin or any file. Mitigation: `verify-factory.py` greps for key patterns; the setup skill only documents Settings entry.
- **R7 — Scope creep:** the factory copy must not re-do #29/#30/#31's work. Mitigation: the copy starts from the saved regular version; factory work only adds the drone mechanisms + setup skill + dispatch rules + cost accounting.

## 5. What does NOT change

- The regular version's pins, design package, grill-me, #28 debloat, and the #31 design libraries are inherited by the copy untouched.
- OpenCode setup stays as the fallback; `opencode-setup.md` is not changed by this plan.
- No push from the sandbox; Anish pushes from Windows when he chooses.
- No paid plans purchased. OpenRouter credits are his existing key (top up $5–10 if needed).

## 6. Open items (need Anish)

- Fork location/name: proposed `~/workspace/hackathon-plugin/factory-cursor/`.
- Benchmark build for the live test: proposed a small landing page (hero, one component, one test).
- Phase 1 scope: proposed to include #30 + #31 (both already specced). Alternative: stop the regular version at #29.
- The CLI live test needs him at his Windows machine (`cursor-agent --help` + one test call).
