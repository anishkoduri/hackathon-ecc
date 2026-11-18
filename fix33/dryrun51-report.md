# Dry-run #51 — fix #33 (unpin the orchestrator), round 33c re-run — SIMULATED

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade` (fix #32 close + fix33 working changes, uncommitted); built tree `scratch-repo/hackathon-ecc/`
- **Method:** SIMULATED only. No live Cursor session ran, no model was invoked, no file was edited. Each leg was walked by reading the routing rules, agent frontmatter, guardrail, and skill files as the orchestrator would and recording what the tree dictates, quoting file + line evidence. All nine legs from dry-run #50 were re-walked from the tree, not carried forward.
- **Context:** fix round 33c landed after dry-run #50 (NOT PASS, D-1 + D-2), audit #110 (NOT PASS, 110-M1), and sweep #53 (NOT CLEAN, S-M1 + S-M2). Rebuild run 9 exit 0; verify33.py **565/565, exit 0** (`verify33-run33c.txt`).
- **Verdict: PASS** — all 9 legs pass as written. **D-1 is FIXED** (leg 1) and **D-2 is FIXED** (leg 5).

## Verdict summary

| Leg | Result |
|---|---|
| 1. MODEL-AUTO (guardrail ordering) | **PASS — D-1 FIXED** (MODEL check now fires before grill-me) |
| 2. MODEL-SELECTED (unpin working) | PASS |
| 3. MODEL-OTHER | PASS |
| 4. MODEL-UNKNOWN | PASS |
| 5. GUARDRAIL-COLD-START (direct commands) | **PASS — D-2 FIXED** (guardrail present at every direct-command entry; orch-* routing traced, not just pointer-trusted) |
| 6. COST-RECORDING | PASS |
| 7. DRONE-UNCHANGED | PASS (with the same versioned-pin caveat as #50, see leg) |
| 8. DEMOTION-REGRESSION (fix #32 holds) | PASS |
| 9. LIVE-TEST | PASS |

**Limits (state up front):** `model: inherit` is doc-verified, not live-verified (OWED-33-1) — Cursor docs say `inherit` is the subagent default ("same model as the parent agent"), but the plugin has never run with `model: inherit` on these agents. The live test (leg 9) is the verification. Nothing in this dry run proves `inherit` resolves in a live Cursor install.

---

## Leg 1 — MODEL-AUTO: PASS (D-1 FIXED)

**Scenario:** user opens a chat with the model picker on Auto and prompts "build a habit tracker app".

**What the tree dictates, in order:**

1. The MODEL check fires first, before grill-me. `skills/orchestrate/SKILL.md:52` (new pre-grill block under `## Run`, headed `**MODEL check — first, before grill-me (fix #33, MODELSEL_F33):**`):
   > "in the first reply, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding (see L14); do not silently orchestrate on an unknown fallback. … Grill-me does not start until a specific model is picked — the MODEL check is a precondition, not a build step, so grill-me stays FIRST among build steps."
2. `skills/orchestrate/SKILL.md:14` (identity paragraph) now cross-references the pre-grill check accurately:
   > "… tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback (see the MODEL check below — it runs before grill-me)."
3. `rules/hackathon-mode.mdc:12` — the MODEL clause now textually precedes "grill-me FIRST":
   > "After the user sends the first hackathon project prompt, the MODEL check (fix #33, MODELSEL_F33) runs first — before grill-me: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before grill-me starts. Then run `grill-me` FIRST among build steps, before any scoping, building, or expansion; grill-me is the first BUILD step, and the MODEL check is not build work."
4. `rules/hackathon-mode.mdc:61` (§7) names the MODEL check as the one question preceding grill-me:
   > "The user answers questions during grill-me (the first few minutes) — plus the MODEL check just before it (fix #33, MODELSEL_F33), the one question that precedes grill-me; after that, do not ask the user anything…"
5. The first-build sequence is restated as MODEL check first. `skills/orchestrate/SKILL.md:62`: "the first-build sequence (MODEL check → grill → scope → expansion → build)".
6. Step 0 is now a back-reference, not the operative check. `skills/orchestrate/SKILL.md:64`: "**MODEL check (fix #33):** already ran before grill-me (see the MODEL check above) — if the model is still Auto, or cannot be determined to be a specific model, at this point, stop and ask again; do not proceed."
7. The picker note agrees. `skills/orchestrate/SKILL.md:95` (step 4): "…and if the picker is on Auto, the orchestrator asks the user to pick a specific model before proceeding (see the MODEL check, before grill-me)."
8. `MODELSEL_F33` still occurs exactly 2× in orchestrate (L14 + L52), staged and built — verified by grep on both copies; staged `new-skills/orchestrate/SKILL.md` L52 / L14 / L64 match the built lines verbatim.

**Walked outcome:** on Auto, the orchestrator's first reply is the MODEL ask; grill-me does not start until a specific model is picked. No scoping, design package, or dispatch happens first, and no silent fallback is permitted. This is the exact reversal of the #50 failure (grill-me ran first; the check was step 0 "immediately after grill-me"). **D-1 is fixed.**

**Note (not a fail):** the only text sequenced before the MODEL check in the skill file is the passive `skills/orchestrate/SKILL.md:10` "Start of run — read the decision record first" (a file read before planning/delegating, not user-facing work and not grill-me). It does not ask, build, or grill, so it does not violate "before proceeding" as the leg defines it. Also note `hackathon-mode.mdc:63` (§7 override: "§7 overrides any ask/stop/wait instruction … except the one-question grill-now-or-proceed ask") — the MODEL ask is carved out by §7's own L61 text naming it as the question preceding grill-me, so the override does not swallow it; the two lines are consistent as written.

## Leg 2 — MODEL-SELECTED: PASS

**Scenario:** user selects Grok 4.7 Extra High and prompts "build a habit tracker app".

- The orchestrator runs on the selected model. `skills/orchestrate/SKILL.md:14`: "the orchestrator runs on the model selected in this chat (fix #33, MODELSEL_F33…)".
- Chat-model subagents carry `model: inherit`. `agents/deep-reasoner.md:3-4`: "description: Reasoning-heavy executor running on the model selected in this chat (`model: inherit`)." / "model: inherit". The same `model: inherit` line is present in `agents/ecc-architect.md:4`, `agents/ecc-healthcare-reviewer.md:4`, `agents/ecc-spec-miner.md:4` (4 inherit agents total; the other 41 agents are `model: cursor-grok-4.6-high-fast`).
- MODEL check records the actual model. `skills/orchestrate/SKILL.md:52`: "record it in the run ledger (`MODEL: <name>` — the actual selected model)" — so the ledger reads `MODEL: Grok 4.7 Extra High`.
- Normal flow proceeds: MODEL check → grill-me first among build steps (hackathon-mode L12) → design package forced for any UI/UX (`skills/orchestrate/SKILL.md:35` DESIGNPKG-AUTO; hackathon-mode L31-32, Taste leads) → build (orchestrate step 4, L95).
- No rule re-pins or contradicts the selection: grep of the built tree finds zero `grok-4.7-high` and zero `Grok 4.7 Extra High` (the only surviving "Grok 4.7 High" prose is the two strategic-compact keeps, `skills/strategic-compact/SKILL.md:68` and `:102`, which are factual model examples, not orchestrator identity). `schemas/agent.schema.json:36` enum is `["cursor-grok-4.6-high-fast", "inherit"]` — Extra High removed, so a re-pin cannot pass validation.

## Leg 3 — MODEL-OTHER: PASS

**Scenario:** user selects a different specific model (e.g. Claude Sonnet) and prompts the same.

- Same routing as leg 2: the orchestrator runs on "the model selected in this chat" (orchestrate L14); `model: inherit` subagents run on the same model as the parent (deep-reasoner L7 comment: "`inherit` is the Cursor default for subagents: same model as the parent agent").
- MODEL check records it: orchestrate L52, `MODEL: <name>` — the actual selected model, so the ledger would read `MODEL: Claude Sonnet` (or whatever the picker shows).
- Cost is priced for THAT model — or marked unknown if unrecorded. Orchestrate L52: "cost is marked unknown, never assumed to be Grok/pool." No text anywhere in the built tree assumes Grok or the pool for cost; the regular tree has no cost-accounting system at all (SPEC D33-6 / OWED-33-3, a finding, not a fix33 defect).
- Nothing assumes Grok/pool: the only Grok mentions left in the built tree are the fast tier (`cursor-grok-4.6-high-fast`, 66 mentions across skills/agents/commands/rules) and the two strategic-compact keeps.

## Leg 4 — MODEL-UNKNOWN: PASS

**Scenario:** the selected model cannot be determined (e.g. a new chat where the model is unrecorded).

- Guardrail fires the same as Auto, and now before grill-me. Orchestrate L14: "if the selected model is Auto, **or the model cannot be determined to be a specific model**, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback". L52 repeats the same disjunction verbatim, and its tail ("Grill-me does not start until a specific model is picked") applies to the unknown case exactly as to Auto — unlike #50, where this leg passed only with the D-1 ordering caveat attached, the caveat no longer applies.
- Cost marked unknown, never assumed Grok/pool (L52, quoted in leg 1).

## Leg 5 — GUARDRAIL-COLD-START (direct commands): PASS (D-2 FIXED)

**Scenario:** user invokes `/gan-build` directly with Auto selected; then the same walk for `/gan-design`, `/astra-review`, and each of the five `/orch-*` commands plus `/orchestrate`.

**Full MODEL check at the entry of the three standalone commands (before any work step):**

- `commands/gan-build.md:5` (right after frontmatter, before `$ARGUMENTS` parsing at L7 and Phase 0 Setup at L20):
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
  Its old cold start (Phase 1 step 0, L27-28, the design-direction check reading `docs/decision-record.md`) now sits *after* this check, so it cannot run on Auto before the ask.
- `commands/gan-design.md:5` — identical full check, before `$ARGUMENTS` parsing (L7) and `### Setup` step 0 (L21).
- `commands/astra-review.md:6` — identical full check, before `# Deep Review` (L8) and `## Step 1: Scope` (L12).

**The five orch-* commands — routing traced, not just pointer-trusted:**

- Each orch-* command file carries the ask at its entry (built L7), *before* `## What It Does` (L24-25) and before the skill invocation. E.g. `commands/orch-add-feature.md:7`:
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
  Identical L7 text in `commands/orch-build-mvp.md`, `commands/orch-change-feature.md`, `commands/orch-fix-defect.md`, `commands/orch-refine-code.md`. (The 33c report calls these "one-line pointers"; the actual text is stronger — it contains the operative ask itself, not just a pointer to it.)
- The engine routing is genuine for the four operation skills. Each command's "What It Does" invokes its skill "via the shared `orch-pipeline` engine" (e.g. `commands/orch-add-feature.md:27-28`), and each skill's step 1 is "Run the `orch-pipeline` engine with the settings above" (`skills/orch-add-feature/SKILL.md:31`; same at `skills/orch-change-feature/SKILL.md:34`, `skills/orch-fix-defect/SKILL.md:33`, `skills/orch-refine-code/SKILL.md:33`). The engine's first section is `## Step 0 — Classify size` (`skills/orch-pipeline/SKILL.md:41`), whose first content is the full MODEL check at L43:
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
  The size classifier itself starts at L45 ("Ceremony scales to blast radius"), *after* the check — so the check precedes all entry work including classification.
- `commands/orchestrate.md:7` carries the same entry ask, pointing at the orchestrate skill's pre-grill check ("the orchestrate skill's MODEL check runs first, before grill-me"), before `$ARGUMENTS` (L13) and before the "Show the plan first" instruction (L11).
- `MODELSEL_F33` is present in all 9 command files (gan-build, gan-design, astra-review, the five orch-*, orchestrate.md) plus `skills/orch-pipeline/SKILL.md:43`, `skills/orchestrate/SKILL.md:14,52`, and `rules/hackathon-mode.mdc:12,61` — verified by grep.

**Walked outcome:** a direct `/gan-build` (or `/gan-design`, `/astra-review`, any `/orch-*`, `/orchestrate`) invocation with Auto selected hits the ask at the command's entry, before arg parsing, classification, design-direction checks, or any phase. **D-2 is fixed.** This matches SPEC D33-22/D33-23 (OWED-33-4 SUPERSEDED/FIXED).

**Routing nuance (recorded honestly, not a fail):** for `/orch-build-mvp` specifically, the engine link is the weakest of the five — its skill step 1 runs "orch-pipeline Phases 0–2 ONLY … This step does NOT run the full orch-pipeline engine" (`skills/orch-build-mvp/SKILL.md:36`), and Step 0 (Classify) is not a phase, so a strictly literal reading of step 1 could skip the engine's Step 0 check. The leg still passes because (a) the command file's own L7 line carries the operative ask and fires before the skill is ever invoked, and (b) the downstream drive re-checks: orch-build-mvp step 4 drives `/gan-build … --skip-planner` (`skills/orch-build-mvp/SKILL.md:64`), and `commands/gan-build.md:5` re-runs the full check at that command's entry. If a future round wants the engine link airtight for orch-build-mvp, the fix is one line in its skill step 1 naming Step 0 — but no bypass exists on the current tree, so this is a hardening note, not a failure.

## Leg 6 — COST-RECORDING: PASS

- **MODEL-SELECTED leg:** orchestrate L52 records the actual selected model in the run ledger: `MODEL: <name>` — the actual selected model. The run ledger is `.hackathon/run-ledger.md` (referenced as the ledger location in orchestrate L68, "the expansion section of `.hackathon/run-ledger.md`", and L96). On the leg-2 walk the ledger reads `MODEL: Grok 4.7 Extra High`.
- **MODEL-UNKNOWN leg:** L52: "A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool." So the ledger records the model as unverified and cost as unknown — no Grok/pool assumption is written anywhere.
- Rule text and record location both confirmed from the file (orchestrate L52 + L68). No separate cost-accounting system exists in the regular tree (OWED-33-3).

## Leg 7 — DRONE-UNCHANGED: PASS (with caveat)

**Scenario:** orchestrator briefs a reasoning drone + a coding drone for a multi-file task.

- Dispatch path is GLOBAL-ROUTING, `skills/orchestrate/SKILL.md:36`: "Every prompt is answered by the orchestrator model; drones never answer the user directly and never decide scope… The orchestrator keeps a queue of independent single-task jobs and dispatches drones into free slots… the orchestrator picks the best drone model for the task (fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work)… Every drone brief carries the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return". The block is unchanged by fix33/33c (the re-sequence touched the MODEL check placement and the direct-command weave only; no `*openrouter*`, `*drone*`, or `*dispatch*` path changed).
- The unpin changed nothing on this path: the decides-tier `model: inherit` change touches only the orchestrator/design-lead/deep-reasoner agents; drone assignment text is untouched.
- **Caveat (honest scope note, unchanged from #50, not a fail of this leg):** the versioned pins named in the brief — reasoning DeepSeek V4.1 Flash 1017, coding Qwen3 Coder 30B — do **not** appear as model slugs anywhere in the regular built tree (grep for `DeepSeek V4` / `Qwen3 Coder` returns zero matches; the built tree names only "DeepSeek" and "Qwen" in the GLOBAL-ROUTING sentence above). The versioned drone pins live in the factory tree / fix30 SPEC, not in this regular tree — so this leg confirms the dispatch path is intact and unchanged by fix33, but it cannot (and does not claim to) verify the versioned drone IDs from the regular tree itself.

## Leg 8 — DEMOTION-REGRESSION: PASS

**Scenario:** "design the dashboard for a clinic operations app".

- Routing still goes to Taste. Orchestrate routing-table row 10 (`skills/orchestrate/SKILL.md:137`): "a dashboard/app surface goes to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` as its lookup inventory and `less-flat-ui` texture where it fits, per hackathon-mode §5)."
- `rules/hackathon-mode.mdc:31-32`: "Every build — a full company or landing-page build, a dashboard/app surface, or a component — is led by `design-taste-frontend` (fix #32: the design lead for every surface). `ui-ux-pro-max` is the lookup inventory the lead consults after the direction is set; it never leads." / "`ui-ux-pro-max` is the lookup-only design inventory for dashboards and apps (fix #32)… consulted by the design-lead after the direction is set, never the design lead."
- `skills/ui-ux-pro-max/SKILL.md` frontmatter description: "LOOKUP ONLY (fix #32). … it is never the design lead. … Do NOT use to set a design direction, lead a dashboard/app/component build… (use design-taste-frontend for that)".
- DESIGNPKG-AUTO still present in orchestrate L35 and hackathon-mode. Counts unchanged: 72 skills / 45 agents / 55 commands / 48 rules (verified by directory listing). Fix #33 + round 33c did not regress fix #32.

## Leg 9 — LIVE-TEST: PASS

**File:** `scratch-repo/fix30/live-test-prompt.md` (read in full; same file dry-run #50 verified, md5 `cd679e5e7ecd5f5ace654294ada24b47`).

- Selection stated explicitly, header + L1: "Run this in Cursor after fix #33 lands… Before starting, select **Grok 4.7 Extra High** in the model picker — this is Anish's default, and the test's baseline: since fix #33 the orchestrator runs on whatever model is selected, so the test verifies the SELECTED model runs the parent."
- Title: "Fix #33 live-test prompt — selected-model orchestrator (Grok 4.7 Extra High selected for the test)".
- Pass criterion matches: "PASS: the parent agent ran the model selected in the picker (**Grok 4.7 Extra High** for this test) on both Task A and Task B (the model indicator says so). … FAIL: the parent ran anything other than the selected model on either task (e.g. it fell back to Grok 4.7 High, or to Auto)."
- Tasks A (reasoning-heavy decision doc, `DECISION.md`) and B (repo-scale TypeScript task queue, `src/queue.ts` / `src/worker.ts` / `src/index.ts` / `test/queue.test.ts`) unchanged; the required end-of-run report states, per task, which model ran the parent (from the chat model indicator) and which model ran each subagent, reporting only what the indicators actually showed.
- What Anish must do: fresh Cursor chat in a scratch project, select Grok 4.7 Extra High first, paste the prompt, run both tasks, report the indicators. Still owed (OWED-30-3, carried forward). The prompt was not changed by round 33c and needs no change: the guardrail re-sequence does not alter what the live test must prove.

---

## Failures (numbered)

None. D-1 and D-2 from dry-run #50 are both fixed on the current tree (legs 1 and 5 above).

## Gaps / notes for the coordinator

1. **D-1 fix verified by re-sequence, not rewording:** the operative MODEL check physically moved to orchestrate L52 (pre-grill block under `## Run`), hackathon-mode L12 now orders the MODEL clause before "grill-me FIRST", and §7 L61 names it as the one question preceding grill-me. Staged and built copies agree line-for-line on L12/L14/L52/L64.
2. **D-2 fix verified by tracing, not grep alone:** all 9 direct-command files carry the ask at entry; the orch-pipeline Step 0 choke point (L43, before the classifier at L45) was traced through each orch-* skill's step 1. The one soft link is orch-build-mvp's step 1 ("Phases 0–2 ONLY, not the full engine") — covered in practice by its own command-file L7 ask and by the downstream `/gan-build` L5 re-check. Optional hardening: one line in `skills/orch-build-mvp/SKILL.md:36` naming Step 0.
3. **Leg 7 caveat (carried from #50):** versioned drone pins (DeepSeek V4.1 Flash 1017 / Qwen3 Coder 30B) are not present as slugs in the regular built tree; the dispatch path is unchanged, but the pins themselves are verifiable only in the factory tree / fix30 SPEC.
4. **OWED-33-1 stands:** `model: inherit` is doc-verified, not live-verified; this simulated run cannot verify it. The live test (leg 9) remains owed to Anish.
5. **Minor count note:** directory listing gives 72 skills / 45 agents / 48 rules / 55 commands; the hooks directory lists 17 entries vs the 33c report's "15 hooks" census figure — the discrepancy was not chased (no leg depends on the hook count), but the coordinator may want the census figure reconciled.
6. Verify33 565/565 + both scan suites green now cover the re-sequence (§16l) and the direct-command weave (§16m) — the two areas the dry run caught in #50 are verifier-covered in 33c, and this dry run independently re-confirms both by walking the tree.

## Files checked (built tree, `scratch-repo/hackathon-ecc/`)

`skills/orchestrate/SKILL.md` (L10, L14, L35, L36, L52, L62, L64, L68, L95, L96, L137); `skills/orch-pipeline/SKILL.md` (L41-47); `skills/orch-add-feature/SKILL.md` (L31), `skills/orch-build-mvp/SKILL.md` (L25, L36, L64), `skills/orch-change-feature/SKILL.md` (L34), `skills/orch-fix-defect/SKILL.md` (L33), `skills/orch-refine-code/SKILL.md` (L33); `agents/deep-reasoner.md`, `agents/ecc-architect.md`, `agents/ecc-healthcare-reviewer.md`, `agents/ecc-spec-miner.md`; `commands/gan-build.md` (L5, L7, L20, L27-28), `commands/gan-design.md` (L5, L21), `commands/astra-review.md` (L6, L12), `commands/orch-add-feature.md` (L7, L27-28), `commands/orch-build-mvp.md` (L7), `commands/orch-change-feature.md` (L7), `commands/orch-fix-defect.md` (L7), `commands/orch-refine-code.md` (L7), `commands/orchestrate.md` (L7, L11, L13); `rules/hackathon-mode.mdc` (L12, L31-32, L61, L63); `schemas/agent.schema.json:36`; `skills/ui-ux-pro-max/SKILL.md`, `skills/design-taste-frontend/SKILL.md`; `scratch-repo/fix30/live-test-prompt.md`; `fix33/SPEC.md` (D33-20..D33-24, OWED-33-4 SUPERSEDED), `fix33/verify33-run33c.txt` (565/565).
