# Dry-run #50 — fix #33 (unpin the orchestrator) — SIMULATED

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade` (fix #32 close + fix33 working changes, uncommitted); built tree `scratch-repo/hackathon-ecc/`
- **Method:** SIMULATED only. No live Cursor session ran, no model was invoked, no file was edited. Each leg was walked by reading the routing rules, agent frontmatter, guardrail, and skill files as the orchestrator would and recording what the tree dictates, quoting file + line evidence.
- **Context:** audit #109-A PASSED (2 minor) + #109-B PASSED (4 minor); fix round 33b corrected all six; verify33.py **526/526, exit 0** (run 3).
- **Verdict: NOT PASS** — 7 of 9 legs pass as written; 2 legs fail (D-1, D-2 below).

## Verdict summary

| Leg | Result |
|---|---|
| 1. MODEL-AUTO (guardrail) | **FAIL — D-1** (guardrail text present and blocks scoping/design/dispatch, but grill-me does NOT wait: it runs before the step-0 MODEL check) |
| 2. MODEL-SELECTED (unpin working) | PASS |
| 3. MODEL-OTHER | PASS |
| 4. MODEL-UNKNOWN | PASS (same guardrail as Auto; shares the D-1 ordering note) |
| 5. GUARDRAIL-COLD-START (/gan-build direct) | **FAIL — D-2** (genuine bypass; OWED-33-4) |
| 6. COST-RECORDING | PASS |
| 7. DRONE-UNCHANGED | PASS (with a versioned-pin caveat, see leg) |
| 8. DEMOTION-REGRESSION (fix #32 holds) | PASS |
| 9. LIVE-TEST | PASS |

**Limits (state up front):** `model: inherit` is doc-verified, not live-verified (OWED-33-1) — Cursor docs say `inherit` is the subagent default ("same model as the parent agent"), but the plugin has never run with `model: inherit` on these agents. The live test (leg 9) is the verification. Nothing in this dry run proves `inherit` resolves in a live Cursor install.

---

## Leg 1 — MODEL-AUTO: FAIL (D-1)

**Scenario:** user opens a chat with the model picker on Auto and prompts "build a habit tracker app".

**What the tree dictates, in order:**

1. `rules/hackathon-mode.mdc:12` — "After the user sends the first hackathon project prompt, run `grill-me` FIRST, before any scoping, building, or expansion." Grill-me is sequenced FIRST, with no model exception.
2. The guardrail text itself is present and correct. `skills/orchestrate/SKILL.md:14` (identity paragraph, token `MODELSEL_F33`):
   > "You are the **orchestrator** — the session's main model: the orchestrator runs on the model selected in this chat (fix #33, MODELSEL_F33 — selected in the model picker before the first build; see the picker note in step 4). … if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback (see the MODEL check in step 0)."
3. The MODEL check fires at step 0, `skills/orchestrate/SKILL.md:62`:
   > "0. **Narration-key prompt (the orchestrator sends it — immediately after grill-me, before scoping, at the start of the build).** **MODEL check (fix #33, MODELSEL_F33):** in the first reply, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding (see L14); do not silently orchestrate on an unknown fallback. A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool."
4. The picker note, `skills/orchestrate/SKILL.md:93` (inside step 4, Build): "Before the first build — select a specific model in the model picker (pre-build setup, not a mid-build ask): … and if the picker is on Auto, the orchestrator asks the user to pick a specific model before proceeding (see the MODEL check in step 0)."
5. `MODELSEL_F33` occurs exactly 2× in orchestrate (L14 + L62), staged and built — confirmed by audit #109-B §4.

**Why this leg FAILS as written:** the leg requires the Auto ask to fire BEFORE proceeding with "grill-me, design package, dispatch all wait". The tree as written sequences it otherwise: grill-me runs FIRST (hackathon-mode L12), and the MODEL check is step 0 "immediately after grill-me" (orchestrate L62 heading). Audit #109-B §4 states the same sequence: "grill → narration-key prompt (orchestrate step 0) → scope → expansion → build". So on Auto, the grill-me Q&A runs before any Auto ask fires; the ask blocks scoping, the design package, and dispatch — but **grill-me does not wait**. L14's "before proceeding" is a standing instruction in the identity paragraph, not a step sequenced before grill-me, so nothing in the tree orders the ask ahead of grill-me. No step silently proceeds on an unknown fallback past step 0 — the silent-fallback prohibition itself holds — but the leg's stated condition (grill-me waits) is not what the tree dictates.

**D-1 (failure):** on Auto, grill-me runs before the MODEL check fires; the guardrail's ask is sequenced at step 0, after grill-me, not before it.

## Leg 2 — MODEL-SELECTED: PASS

**Scenario:** user selects Grok 4.7 Extra High and prompts "build a habit tracker app".

- The orchestrator runs on the selected model. `skills/orchestrate/SKILL.md:14`: "the orchestrator runs on the model selected in this chat (fix #33, MODELSEL_F33…)".
- Chat-model subagents carry `model: inherit`. `agents/deep-reasoner.md:3-4`: "description: Reasoning-heavy executor running on the model selected in this chat (`model: inherit`)." / "model: inherit". The same `model: inherit` line is present in `agents/ecc-architect.md:4`, `agents/ecc-healthcare-reviewer.md:4`, `agents/ecc-spec-miner.md:4` (4 inherit agents total; the other 41 agents are `model: cursor-grok-4.6-high-fast`).
- MODEL check records the actual model. `skills/orchestrate/SKILL.md:62`: "record it in the run ledger (`MODEL: <name>` — the actual selected model)" — so the ledger reads `MODEL: Grok 4.7 Extra High`.
- Normal flow proceeds: grill-me first (hackathon-mode L12) → design package forced for any UI/UX (`skills/orchestrate/SKILL.md:35` DESIGNPKG-AUTO; hackathon-mode L31-32, Taste leads) → build (orchestrate step 4, L93).
- No rule re-pins or contradicts the selection: grep of the built tree finds zero `grok-4.7-high` and zero `Grok 4.7 Extra High` (the only surviving "Grok 4.7 High" prose is the two strategic-compact keeps, `skills/strategic-compact/SKILL.md:68` and `:102`, which are factual model examples, not orchestrator identity). `commands/model-route.md:16-17` merges to: "the model selected in this chat: default for implementation and refactors, architecture, deep review, ambiguous requirements". `schemas/agent.schema.json:36` enum is `["cursor-grok-4.6-high-fast", "inherit"]` — Extra High removed, so a re-pin cannot pass validation.

## Leg 3 — MODEL-OTHER: PASS

**Scenario:** user selects a different specific model (e.g. Claude Sonnet) and prompts the same.

- Same routing as leg 2: the orchestrator runs on "the model selected in this chat" (orchestrate L14); `model: inherit` subagents run on the same model as the parent (deep-reasoner L7 comment: "`inherit` is the Cursor default for subagents: same model as the parent agent").
- MODEL check records it: orchestrate L62, `MODEL: <name>` — the actual selected model, so the ledger would read `MODEL: Claude Sonnet` (or whatever the picker shows).
- Cost is priced for THAT model — or marked unknown if unrecorded. Orchestrate L62: "cost is marked unknown, never assumed to be Grok/pool." No text anywhere in the built tree assumes Grok or the pool for cost; the regular tree has no cost-accounting system at all (SPEC D33-6 / OWED-33-3, a finding, not a fix33 defect).
- Nothing assumes Grok/pool: the only Grok mentions left in the built tree are the fast tier (`cursor-grok-4.6-high-fast`, x72) and the two strategic-compact keeps.

## Leg 4 — MODEL-UNKNOWN: PASS

**Scenario:** the selected model cannot be determined (e.g. a new chat where the model is unrecorded).

- Guardrail fires the same as Auto. Orchestrate L14: "if the selected model is Auto, **or the model cannot be determined to be a specific model**, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback". L62 repeats the same disjunction verbatim.
- Cost marked unknown, never assumed Grok/pool (L62, quoted in leg 1).
- Note: the D-1 ordering caveat applies here too — the ask fires at step 0, after grill-me — but this leg's stated condition (guardrail fires the same as Auto; cost unknown) holds as written, so it passes.

## Leg 5 — GUARDRAIL-COLD-START (/gan-build direct, Auto): FAIL (D-2)

**Scenario:** user invokes `/gan-build` directly with Auto selected.

**What the tree dictates:**

- `commands/gan-build.md` contains **zero** occurrences of `MODELSEL_F33`, `MODEL check`, or "pick a specific model" (grep across `commands/` + `skills/orch-*/SKILL.md` finds the guardrail only in `skills/orchestrate/SKILL.md`). Its only model text is the unpinned phrasing: `commands/gan-build.md:26` "(on the model selected in this chat)".
- Its cold start is its own path, not orchestrate step 0. `commands/gan-build.md` Phase 1 step 0 is a "Design-direction check (cold start) — BEFORE launching the planner, read `docs/decision-record.md` FIRST" — it reads the grill-me record and launches the `gan-planner` agent; it never invokes the orchestrate skill, never reaches orchestrate step 0, and never asks about the model.
- No other file routes `/gan-build` through orchestrate step 0: grep for `gan-build` outside its own command file finds only `commands/gan-design.md:35` ("Same as `/gan-build` Phase 2"), `commands/orch-build-mvp.md:31` (the orch pipeline drives `/gan-build` — i.e. `/gan-build` is downstream of an orch command, not routed through orchestrate step 0), and an unrelated design-skills exclusion in hackathon-mode L38.
- `commands/gan-design.md` is the same: its Setup step 0 is a design-direction check reading `docs/decision-record.md`; the design-lead "is invoked inline as the orchestrator in Setup step 0 (not spawned as a drone)". No Auto ask.
- The same holds for `/astra-review` (its verdict block now reads `Model: inherit`, `commands/astra-review.md:41`) and the `/orch-*` pipelines — none carries the guardrail (audit #109-B §4 / B-M1).

**D-2 (failure):** a direct `/gan-build` invocation with Auto selected genuinely bypasses the guardrail — the command does not route through orchestrate step 0, so no Auto ask fires and the build loop proceeds on whatever Auto resolves to. This is the recorded OWED-33-4 (guardrail is orchestrate-only by deliberate design, D33-19; the primary cold start via hackathon-mode first build is covered because it enters orchestrate step 0). Per the dry-run brief, a genuine bypass is a FAILED leg, not a hidden pass — recorded here as such. It is not a regression (the pre-fix33 MODEL-PIN check was also orchestrate-only), and no false identity is asserted on this path (the command says "the model selected in this chat", which is true whatever Auto resolves to) — but the leg as written fails.

## Leg 6 — COST-RECORDING: PASS

- **MODEL-SELECTED leg:** orchestrate L62 records the actual selected model in the run ledger: `MODEL: <name>` — the actual selected model. The run ledger is `.hackathon/run-ledger.md` (referenced as the ledger location in orchestrate L62's KEY-RECEIPT sentence and L66, "the expansion section of `.hackathon/run-ledger.md`"). On the leg-2 walk the ledger reads `MODEL: Grok 4.7 Extra High`.
- **MODEL-UNKNOWN leg:** L62: "A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool." So the ledger records the model as unverified and cost as unknown — no Grok/pool assumption is written anywhere.
- Rule text and record location both confirmed from the file (orchestrate L62). No separate cost-accounting system exists in the regular tree (OWED-33-3).

## Leg 7 — DRONE-UNCHANGED: PASS (with caveat)

**Scenario:** orchestrator briefs a reasoning drone + a coding drone for a multi-file task.

- Dispatch path is GLOBAL-ROUTING, `skills/orchestrate/SKILL.md:36`: "Every prompt is answered by the orchestrator model; drones never answer the user directly and never decide scope… The orchestrator keeps a queue of independent single-task jobs and dispatches drones into free slots… the orchestrator picks the best drone model for the task (fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work)… Every drone brief carries the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return". The block is byte-identical to the fix32 text (verify33 §16k; audit #109-B §6), and `git diff dd106ade` touches no `*openrouter*`, `*drone*`, or `*dispatch*` path.
- The unpin changed nothing on this path: the decides-tier `model: inherit` change touches only the orchestrator/design-lead/deep-reasoner agents; drone assignment text is untouched.
- **Caveat (honest scope note, not a fail of this leg):** the versioned pins named in the brief — reasoning DeepSeek V4.1 Flash 1017, coding Qwen3 Coder 30B — do **not** appear as model slugs anywhere in the regular built tree. The built tree names only "DeepSeek" and "Qwen" in the GLOBAL-ROUTING sentence above (verify33.py header notes the assignment "stays a forward reference (OWED-29-4…)"), and no `deepseek`/`qwen` slugs exist in the built tree (SPEC §1(d)). The versioned drone pins live in the factory tree / fix30 SPEC, not in this regular tree — so this leg confirms the dispatch path is intact and unchanged by fix33, but it cannot (and does not claim to) verify the versioned drone IDs from the regular tree itself.

## Leg 8 — DEMOTION-REGRESSION: PASS

**Scenario:** "design the dashboard for a clinic operations app".

- Routing still goes to Taste. Orchestrate routing-table row 10 (`skills/orchestrate/SKILL.md:135`): "a dashboard/app surface goes to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` as its lookup inventory and `less-flat-ui` texture where it fits, per hackathon-mode §5)."
- `rules/hackathon-mode.mdc:31-32`: "Every build — a full company or landing-page build, a dashboard/app surface, or a component — is led by `design-taste-frontend` (fix #32: the design lead for every surface). `ui-ux-pro-max` is the lookup inventory the lead consults after the direction is set; it never leads."
- `skills/ui-ux-pro-max/SKILL.md` frontmatter description: "LOOKUP ONLY (fix #32). … it is never the design lead. … Do NOT use to set a design direction, lead a dashboard/app/component build… (use design-taste-frontend for that)".
- DESIGNPKG-AUTO still byte-identical in orchestrate + hackathon-mode (verify33 §16k, 526/526 run 3). Counts unchanged: 72 skills / 45 agents (verified by directory listing). Fix #33 did not regress fix #32. (The trigger-key deletion and 72/48 coverage counts are verifier-covered; this leg confirms the behavioral routing, which matches.)

## Leg 9 — LIVE-TEST: PASS

**File:** `fix30/live-test-prompt.md` (canonical + scratch-repo copy, md5-identical per audit #109-B §5).

- Selection stated explicitly, header + L1: "Run this in Cursor after fix #33 lands… Before starting, select **Grok 4.7 Extra High** in the model picker — this is Anish's default, and the test's baseline: since fix #33 the orchestrator runs on whatever model is selected, so the test verifies the SELECTED model runs the parent."
- Title: "Fix #33 live-test prompt — selected-model orchestrator (Grok 4.7 Extra High selected for the test)".
- Pass criterion matches: "PASS: the parent agent ran the model selected in the picker (**Grok 4.7 Extra High** for this test) on both Task A and Task B (the model indicator says so). … FAIL: the parent ran anything other than the selected model on either task (e.g. it fell back to Grok 4.7 High, or to Auto)."
- Tasks A (reasoning-heavy decision doc, `DECISION.md`) and B (repo-scale TypeScript task queue, `src/queue.ts` / `src/worker.ts` / `src/index.ts` / `test/queue.test.ts`) unchanged; the required end-of-run report states, per task, which model ran the parent (from the chat model indicator) and which model ran each subagent, reporting only what the indicators actually showed.
- What Anish must do: fresh Cursor chat in a scratch project, select Grok 4.7 Extra High first, paste the prompt, run both tasks, report the indicators. Still owed (OWED-30-3, carried forward).

---

## Failures (numbered)

- **D-1 (leg 1, MODEL-AUTO ordering):** the Auto ask is sequenced at orchestrate step 0, *after* grill-me (orchestrate L62 heading "immediately after grill-me"; hackathon-mode L12 grill-me FIRST). The leg requires grill-me to wait for the ask; the tree does not order it that way. The ask does block scoping, design package, and dispatch, and no silent fallback is permitted past step 0 — the failure is the grill-me ordering only.
- **D-2 (leg 5, GUARDRAIL-COLD-START bypass):** direct `/gan-build` (and `/gan-design`, `/astra-review`, `/orch-*`) invocations do not route through orchestrate step 0 and carry no Auto ask — genuine bypass, recorded as OWED-33-4. Not a regression (pre-fix33 MODEL-PIN check was also orchestrate-only); follow-up belongs to a future round if ever wanted.

## Gaps / notes for the coordinator

1. **D-1 vs the audits:** both audit #109 reports PASSED while describing the same sequence (audit #109-B §4: "grill → narration-key prompt (orchestrate step 0)"). The audits judged the guardrail covered because the MODEL check sits in the primary cold-start path; this dry run fails leg 1 only because the leg as written additionally requires grill-me to wait. If the coordinator's intent is "the ask fires before any *build* work", D-1 is a wording/sequencing note, not a tree defect; if the intent is literally "grill-me waits", the tree needs a re-sequence (ask before grill-me) — a fix-round decision.
2. **D-2 is already OWED-33-4** — no new finding, but this dry run confirms the bypass by walking the command file rather than by grep alone.
3. **Leg 7 caveat:** versioned drone pins (DeepSeek V4.1 Flash 1017 / Qwen3 Coder 30B) are not present as slugs in the regular built tree; the dispatch path is unchanged, but the pins themselves are verifiable only in the factory tree / fix30 SPEC.
4. **Staged vs built line numbers:** SPEC cites staged line numbers (e.g. picker note at orchestrate L93); in the built tree the picker note is also inside L93 (the step-4 Build line), so the citations hold in both copies. `MODELSEL_F33` is 2× in both.
5. **OWED-33-1 stands:** `model: inherit` is doc-verified, not live-verified; this simulated run cannot verify it. The live test (leg 9) remains owed to Anish.
6. Verify33 526/526 and both scan suites green do not cover D-1/D-2 — they assert the guardrail text exists and the direct commands are unpinned-model-agnostic, not the entry-point sequencing. That is why the dry-run legs caught what the verifier did not.

## Files checked (built tree, `scratch-repo/hackathon-ecc/`)

`skills/orchestrate/SKILL.md` (L14, L35, L36, L62, L93, L135); `agents/deep-reasoner.md`, `agents/ecc-architect.md`, `agents/ecc-healthcare-reviewer.md`, `agents/ecc-spec-miner.md`; `commands/gan-build.md`, `commands/gan-design.md`, `commands/astra-review.md`, `commands/model-route.md`, `commands/orch-build-mvp.md`; `rules/hackathon-mode.mdc` (L12, L31-32, L42, L44-45); `schemas/agent.schema.json:35-36`; `skills/ui-ux-pro-max/SKILL.md`, `skills/design-taste-frontend/SKILL.md`; `skills/strategic-compact/SKILL.md:68,102`; `fix30/live-test-prompt.md`; SPEC.md §2/§3/§6, MANIFEST.md, audit109-report-A/B.md, verify33-run3.txt.
