# Dry-run #52 — fix #33 (unpin the orchestrator), round 33d re-run — SIMULATED

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`; built tree `scratch-repo/hackathon-ecc/` (run-10 build, exit 0; verify33.py **586/586, exit 0** per `verify33-run33d.txt`)
- **Method:** SIMULATED only. No live Cursor session ran, no model was invoked, no file was edited. Each leg was walked by reading the routing rules, agent frontmatter, guardrail, and skill files as the orchestrator would and recording what the tree dictates, quoting file + line evidence. All nine legs from dry-runs #50/#51 were re-walked from the tree, not carried forward, PLUS the six bypass legs (6–11). **On every leg that routes through a skill file, the trace went INTO the skill file** — the error dry-run #51 made (trusting command-file pointers without tracing the skill) was not repeated.
- **Context:** fix round 33d landed after re-audit #111-B (NOT PASS, 6 blocking B-B1..B-B6 + 3 minor) found bypasses dry-run #51 missed while PASSing. Round 33d claims to close all six bypasses plus B-M2/A-M1/A-M2, rebuild run 10 exit 0, verifier extended to 586 checks (§16n, 21 checks).
- **Verdict: PASS** — all 15 legs pass as written. **All six #111-B bypasses are CLOSED** (legs 6–11). No D-numbered failure.

## Verdict summary

| Leg | Result |
|---|---|
| 1. MODEL-AUTO (guardrail ordering) | PASS |
| 2. MODEL-SELECTED (unpin working) | PASS |
| 3. MODEL-OTHER | PASS |
| 4. MODEL-UNKNOWN | PASS |
| 5. GUARDRAIL-COLD-START (direct commands + all five orch-*) | PASS — traced INTO each orch-* skill, through orch-pipeline Step 0 |
| 6. BYPASS-REMOVAL (B-B1 re-test) | **PASS — B-B1 CLOSED** |
| 7. BYPASS-MVP (B-B2 re-test) | **PASS — B-B2 CLOSED** (with a sequencing nuance, see leg) |
| 8. BYPASS-FEATURE-DEV (B-B3 re-test) | **PASS — B-B3 CLOSED** |
| 9. BYPASS-REACT-BUILD (B-B4 re-test) | **PASS — B-B4 CLOSED** |
| 10. BYPASS-GRILL-TRIGGER (B-B5 re-test) | **PASS — B-B5 CLOSED** |
| 11. BYPASS-EXPANSION (B-B6 re-test) | **PASS — B-B6 CLOSED** |
| 12. COST-RECORDING | PASS |
| 13. DRONE-UNCHANGED | PASS (same versioned-pin caveat as #50/#51) |
| 14. DEMOTION-REGRESSION (fix #32 holds) | PASS |
| 15. LIVE-TEST | PASS |

**Limits (state up front):** `model: inherit` is doc-verified, not live-verified (OWED-33-1) — Cursor docs say `inherit` is the subagent default ("same model as the parent agent"), but the plugin has never run with `model: inherit` on these agents. The live test (leg 15) is the verification. Nothing in this dry run proves `inherit` resolves in a live Cursor install. Simulated only: no live Cursor session ran and no model was invoked.

---

## Leg 1 — MODEL-AUTO: PASS

**Scenario:** user opens a chat with the model picker on Auto and prompts "build a habit tracker app".

**What the tree dictates, in order:**

1. The MODEL check fires first, before grill-me. `skills/orchestrate/SKILL.md:52` (pre-grill block under `## Run`, headed `**MODEL check — first, before grill-me (fix #33, MODELSEL_F33):**`):
   > "in the first reply, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding (see L14); do not silently orchestrate on an unknown fallback. … Grill-me does not start until a specific model is picked — the MODEL check is a precondition, not a build step, so grill-me stays FIRST among build steps."
2. `skills/orchestrate/SKILL.md:14` (identity paragraph) cross-references it: "… tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback (see the MODEL check below — it runs before grill-me)."
3. `rules/hackathon-mode.mdc:12` — the MODEL clause textually precedes "grill-me FIRST":
   > "After the user sends the first hackathon project prompt, the MODEL check (fix #33, MODELSEL_F33) runs first — before grill-me: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before grill-me starts. Then run `grill-me` FIRST among build steps, before any scoping, building, or expansion; grill-me is the first BUILD step, and the MODEL check is not build work."
4. `rules/hackathon-mode.mdc:61` (§7) names the MODEL check as the one question preceding grill-me: "… plus the MODEL check just before it (fix #33, MODELSEL_F33), the one question that precedes grill-me …"
5. The first-build sequence is restated as MODEL check first. `skills/orchestrate/SKILL.md:62`: "the first-build sequence (MODEL check → grill → scope → expansion → build)".
6. Step 0 is a back-reference, not the operative check. `skills/orchestrate/SKILL.md:64`: "**MODEL check (fix #33):** already ran before grill-me (see the MODEL check above) — if the model is still Auto … stop and ask again; do not proceed."
7. The picker note agrees. `skills/orchestrate/SKILL.md:95` (step 4): "… and if the picker is on Auto, the orchestrator asks the user to pick a specific model before proceeding (see the MODEL check, before grill-me)."
8. `MODELSEL_F33` occurs exactly 2× in orchestrate (L14 + L52) and 2× in hackathon-mode (L12 + L61) — verified by grep on the built tree.

**Walked outcome:** on Auto, the orchestrator's first reply is the MODEL ask; grill-me does not start until a specific model is picked. No scoping, design package, or dispatch happens first, and no silent fallback is permitted. The only text sequenced before the MODEL check in the orchestrate skill is the passive `skills/orchestrate/SKILL.md:10` "Start of run — read the decision record first" (a file read before planning/delegating, not user-facing work and not grill-me). It does not ask, build, or grill, so it does not violate "before proceeding" as the leg defines it.

## Leg 2 — MODEL-SELECTED: PASS

**Scenario:** user selects Grok 4.7 Extra High and prompts "build a habit tracker app".

- The orchestrator runs on the selected model. `skills/orchestrate/SKILL.md:14`: "the orchestrator runs on the model selected in this chat (fix #33, MODELSEL_F33…)".
- Chat-model subagents carry `model: inherit`. `agents/deep-reasoner.md:3-4`: "description: Reasoning-heavy executor running on the model selected in this chat (`model: inherit`)." / "model: inherit". The same `model: inherit` line is present in `agents/ecc-architect.md:4`, `agents/ecc-healthcare-reviewer.md:4`, `agents/ecc-spec-miner.md:4` (4 inherit agents total; the other 41 agents are `model: cursor-grok-4.6-high-fast` — verified by `grep -rh "^model:" agents/ | sort | uniq -c`: 41 fast / 4 inherit).
- MODEL check records the actual model. `skills/orchestrate/SKILL.md:52`: "record it in the run ledger (`MODEL: <name>` — the actual selected model)" — so the ledger reads `MODEL: Grok 4.7 Extra High`.
- Normal flow proceeds: MODEL check → grill-me first among build steps (hackathon-mode L12) → design package forced for any UI/UX (`skills/orchestrate/SKILL.md:35` DESIGNPKG-AUTO; hackathon-mode L31-32, Taste leads) → build (orchestrate step 4, L95).
- No rule re-pins or contradicts the selection: grep of the built orch-* skills and commands finds zero `grok-4.7-high` and zero `Grok 4.7 High` (the only surviving "Grok 4.7 High" prose is the two strategic-compact keeps, `skills/strategic-compact/SKILL.md:68` and `:102`, factual model examples, not orchestrator identity). `schemas/agent.schema.json` enum is `["cursor-grok-4.6-high-fast", "inherit"]` — Extra High removed, so a re-pin cannot pass validation. B-M2 (build.sh fix13-A writing the pin, fix33.py scrubbing after) is closed at source per the 33d report: build.sh now writes model-agnostic design-role wording and the five fix33.py scrub tuples are removed; the built orch-* skills contain zero pins, verified by grep above.

## Leg 3 — MODEL-OTHER: PASS

**Scenario:** user selects a different specific model (e.g. Claude Sonnet) and prompts the same.

- Same routing as leg 2: the orchestrator runs on "the model selected in this chat" (orchestrate L14); `model: inherit` subagents run on the same model as the parent (deep-reasoner comment: "`inherit` is the Cursor default for subagents: same model as the parent agent").
- MODEL check records it: orchestrate L52, `MODEL: <name>` — the actual selected model, so the ledger would read `MODEL: Claude Sonnet` (or whatever the picker shows).
- Cost is priced for THAT model — or marked unknown if unrecorded. Orchestrate L52: "cost is marked unknown, never assumed to be Grok/pool." No text anywhere in the built tree assumes Grok or the pool for cost; the regular tree has no cost-accounting system at all (SPEC D33-6 / OWED-33-3, a finding, not a fix33 defect).
- Nothing assumes Grok/pool: the only Grok mentions left in the built tree are the fast tier (`cursor-grok-4.6-high-fast`) and the two strategic-compact keeps.

## Leg 4 — MODEL-UNKNOWN: PASS

**Scenario:** the selected model cannot be determined (e.g. a new chat where the model is unrecorded).

- Guardrail fires the same as Auto, and before grill-me. Orchestrate L14: "if the selected model is Auto, **or the model cannot be determined to be a specific model**, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback". L52 repeats the same disjunction verbatim, and its tail ("Grill-me does not start until a specific model is picked") applies to the unknown case exactly as to Auto.
- Cost marked unknown, never assumed Grok/pool (L52, quoted in leg 1).

## Leg 5 — GUARDRAIL-COLD-START (direct commands): PASS

**Scenario:** user invokes `/gan-build`, `/gan-design`, `/astra-review` directly with Auto selected; then the same walk for `/orchestrate` and each of the five `/orch-*` commands. This leg traces the routing INTO each orch-* skill file and through orch-pipeline Step 0 — it does not trust the command-file L7 pointer line alone.

**Full MODEL check at the entry of the three standalone commands (before any work step):**

- `commands/gan-build.md:5` (right after frontmatter, before `$ARGUMENTS` parsing at L7 and Phase 0 Setup):
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
- `commands/gan-design.md:5` — identical full check, before `$ARGUMENTS` parsing (L7) and `### Setup` step 0.
- `commands/astra-review.md:6` — identical full check, before `# Deep Review` (L8) and `## Step 1: Scope` (L12).
- `commands/orchestrate.md:7` carries the same entry ask, pointing at the orchestrate skill's pre-grill check ("the orchestrate skill's MODEL check runs first, before grill-me"), before `$ARGUMENTS` and before the "Show the plan first" instruction.

**The five orch-* commands — routing traced INTO the skill files:**

- Each orch-* command file carries the ask at its entry (built L7), *before* `## What It Does` and before the skill invocation. E.g. `commands/orch-add-feature.md:7`:
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
  Identical L7 text in `commands/orch-build-mvp.md`, `commands/orch-change-feature.md`, `commands/orch-fix-defect.md`, `commands/orch-refine-code.md`.
- The engine routing is genuine for the four operation skills, verified inside each skill file (not from the command pointer):
  - `skills/orch-add-feature/SKILL.md:31`: "1. Run the `orch-pipeline` engine with the settings above."
  - `skills/orch-fix-defect/SKILL.md:33`: same step-1 line.
  - `skills/orch-refine-code/SKILL.md:33`: same step-1 line; its direct `refactor-cleaner` dispatch is step 2 (`:34`, "For dead-code / duplication sweeps, delegate to the `refactor-cleaner` agent … Dispatched as a single-task factory drone …"), i.e. AFTER step 1 runs the engine.
  - `skills/orch-change-feature/SKILL.md:34`: same step-1 line (change path only; the removal branch is leg 6).
  - Section-header grep confirms none of add/fix/refine has a bypass section: each skill contains only `## When to Use`, `## Operation settings`, `## How It Works`, `## Example` — no second work section that skips step 1.
- The engine's first section is `## Step 0 — Classify size` (`skills/orch-pipeline/SKILL.md:41`), whose first content is the full MODEL check at L43 (quoted in leg 5 of #51; re-read verbatim this run). The size classifier itself starts at L45 ("Ceremony scales to blast radius"), *after* the check — so the check precedes all entry work including classification.
- `/orch-build-mvp`: command L7 pointer + skill step 1 now runs Step 0 first — traced in full in leg 7.
- `MODELSEL_F33` is present in all 9 command files (gan-build, gan-design, astra-review, the five orch-*, orchestrate.md) plus `skills/orch-pipeline/SKILL.md:43`, `skills/orchestrate/SKILL.md:14,52`, and `rules/hackathon-mode.mdc:12,61` — verified by grep.

**Walked outcome:** a direct `/gan-build` (or `/gan-design`, `/astra-review`, any `/orch-*`, `/orchestrate`) invocation with Auto selected hits the ask at the command's entry, and for the orch-* commands the traced routing confirms the engine's Step 0 check actually runs on the path (add/fix/refine/change-path via skill step 1; build-mvp via its Step-0-first step 1; change-removal via its own in-section check, leg 6).

## Leg 6 — BYPASS-REMOVAL (B-B1 re-test): PASS — B-B1 CLOSED

**Scenario:** `/orch-change-feature remove the notifications feature` with Auto selected; also the `skill:orch-change-feature` "remove a feature" trigger path.

**Trace INTO the skill file (the step #51 missed):**

- `commands/orch-change-feature.md:27` routes removals: "If `$ARGUMENTS` asks to remove a feature — including a one-prompt removal of a first-build feature — follow the skill's `Removing a feature` section **instead of the change steps below**".
- `skills/orch-change-feature/SKILL.md:45` is `## Removing a feature`. Its FIRST content is now the full MODEL check at `:47`:
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
- The first removal step follows at `:51` ("1. Find the feature's files from the final report's feature-to-files inventory, or, if there is no inventory, trace the feature with `code-explorer` first…"), deletion at `:52` (step 2, "Delete its tests, implementation code, routes, and UI…"), commit at `:54` (step 4, "Run the tests and the app … then commit…"), redeploy at `:55` (step 5, "After the commit, re-deploy…"), report at `:56` (step 6). **Every removal step — find, delete, verify, test/commit, redeploy, report — sits after the :47 check.** No removal step precedes it.
- `MODEL` occurs exactly once in the whole skill file — the :47 check (grep). The change path is unaffected: skill `:34` step 1 still runs the engine, and `## Landing redesigns` (`:41`) still says "The engine steps above still run".
- Trigger path: `manifests/context-packs/skill-triggers@1.json:229` `skill:orch-change-feature` triggers include "remove a feature" / "remove this feature" — the trigger loads the skill directly, bypassing the command file, and lands in the same `## Removing a feature` section, whose first content is the same :47 check. The trigger bypass is closed too, because the check lives in the section, not in the command file.

**Walked outcome:** on Auto, a direct removal (command or trigger) hits the MODEL ask before any file is traced, deleted, committed, or redeployed. **B-B1 is closed.** Note (not a fail): the command file's L7 pointer still states "the `orch-pipeline` engine runs its MODEL check first" — on the removal branch the engine never runs, so that pointer sentence remains literally inaccurate as a description of the mechanism. It is now harmless (the section carries its own operative check, which is what actually fires), but the pointer text itself was not corrected in round 33d.

## Leg 7 — BYPASS-MVP (B-B2 re-test): PASS — B-B2 CLOSED

**Scenario:** `/orch-build-mvp` on Auto; also the `skill:orch-build-mvp` triggers ("build an mvp", "turn this spec into an mvp", `skill-triggers@1.json:222`).

**Trace INTO the skill file (the step #51's "routing nuance" missed):**

- `skills/orch-build-mvp/SKILL.md:36` (step 1, first numbered step under `## How It Works`, `:30`) now reads, in full:
  > "1. Run orch-pipeline Step 0 first (Classify size — the MODEL check, fix #33, MODELSEL_F33, is the first content of Step 0 and runs before anything else: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback), then Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan). This step does NOT run the full orch-pipeline engine (phase mask 0→6): the later numbered steps ARE orch-pipeline Phases 3–6, each running once — orch-build-mvp step 3 is Phase 3 (Scaffold), step 4 is Phase 4 (Implement, GAN loop), step 6 is Phase 5 (Review), step 7 is Phase 6 (Commit). Nothing is run twice and nothing is redone."
- Step 1 therefore carries BOTH the routing edge (runs Step 0 first, which opens with the full check at `skills/orch-pipeline/SKILL.md:43`) AND the operative ask restated inline — so the check fires before the scoping/slicing text that follows in the same line, before Gate 1, before the step-2 expansion, and before the step-4 `/gan-build` drive (`skills/orch-build-mvp/SKILL.md:64`, "Drive the build with `/gan-build … --skip-planner`"), which still re-checks at `commands/gan-build.md:5` as a second ask.
- The command file agrees: `commands/orch-build-mvp.md:29` — "This is orch-build-mvp step 1 = orch-pipeline Step 0 (MODEL check + Classify) first, then Phases 0–2 only — it never runs the full engine." And its L7 pointer is now true on this path.
- Whole-skill read: the only text before step 1 is the frontmatter/description (`:1-6`), the header + factory-routing note (`:8-15`, descriptive, no work), `## When to Use` (`:17-20`), `## Operation settings` (`:22-28`, including the "First move (phase 0 → 2)" settings description at `:26-28`, which *describes* what step 1 does rather than executing it), and two preamble paragraphs under `## How It Works` — the L32 precondition (a file-existence check: "check that `docs/decision-record.md` exists … OR the user explicitly chose the skip path") and the L34 narration-key prompt paragraph. Neither is a numbered sub-step; L32 is a passive existence check, not scoping/slicing/dispatch/build work.
- **Sequencing nuance (recorded honestly, not a fail):** the L34 narration-key paragraph sits textually before step 1 and says the prompt fires "at the start of the run (step 1)" — but only if the user asked for a demo video, it never blocks, and it is a hackathon-mode §7-sanctioned prompt. Step 1's own first clause is "Run orch-pipeline Step 0 first", so within step 1 the MODEL check is first; and on the `/orch-build-mvp` command path the L7 check fires before the skill is even invoked. On the direct-trigger path the L34-vs-Step-0 ordering is not *explicitly* sequenced in the skill text (unlike orchestrate, where the pre-grill check at L52 precedes the narration-key step 0 at L64). No scoping, slicing, Gate 1, expansion, dispatch, or build step precedes the check on any path — the leg's stated condition is met — but audit #112 may want to judge whether the L34 paragraph should carry an explicit "after the MODEL check" sequencing line.

**Walked outcome:** on Auto, step 1 runs Step 0 first and the MODEL ask fires before any scoping, slicing, Gate 1, or expansion. **B-B2 is closed.** The #51 "soft link" is now a hard edge plus an inline ask.

## Leg 8 — BYPASS-FEATURE-DEV (B-B3 re-test): PASS — B-B3 CLOSED

**Scenario:** `/feature-dev` on Auto.

- `commands/feature-dev.md:5` (right after the frontmatter, first content of the file body) carries the full MODEL check:
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
- The first work step is the `code-explorer` dispatch at `:19` ("use `code-explorer` agent (`agents/ecc-code-explorer.md`) to analyze the relevant existing code", under `### 2. Codebase Exploration`, `:17`). Between the check and that dispatch there is only the intro line (`:7`, "A structured feature-development workflow…") and `### 1. Discovery` (`:11-15`: read the request, identify requirements, "ask clarifying questions if the request is ambiguous") — all after the :5 check. The later dispatches (`code-architect` `:31`, implementation `:35-39`, `code-reviewer` `:43`) are all further downstream.
- Nothing routes elsewhere first: the file is self-contained; no earlier dispatch, no skill load, no engine invocation precedes :5.

**Walked outcome:** on Auto, the ask fires at entry, before Discovery questions, before the code-explorer dispatch, and before any design/implementation/review work. **B-B3 is closed.**

## Leg 9 — BYPASS-REACT-BUILD (B-B4 re-test): PASS — B-B4 CLOSED

**Scenario:** `/react-build` on Auto.

- `commands/react-build.md:5` (right after the frontmatter) carries the full MODEL check (same wording as leg 8).
- The factory routing / drone dispatch is at `:11`: "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the react-build-resolver runs as a single-task factory drone with a director brief…". The command's own summary at `:9` ("This command invokes the **react-build-resolver** agent…") and the work steps (`## What This Command Does`, `:13-20`: detect build system, run build, parse errors, fix incrementally, orchestrator verify) all follow the :5 check.
- Drone pins/dispatch unchanged: the resolver agent is `agents/ecc-react-build-resolver.md`, `model: cursor-grok-4.6-high-fast` (`:4`) — the fast tier, untouched by fix33/33d. The 33d weave added only the guardrail ask; no dispatch line, brief format, or pin was altered (verified: the :11 factory-routing text and the `:190` agent reference are the pre-33d mechanism).

**Walked outcome:** on Auto, the ask fires at entry, before the factory drone is dispatched and before any build/fix work. **B-B4 is closed.**

## Leg 10 — BYPASS-GRILL-TRIGGER (B-B5 re-test): PASS — B-B5 CLOSED

**Scenario:** user types "grill me" (trigger-routed, not the command) on Auto.

- Trigger routing verified in the manifest: `manifests/context-packs/skill-triggers@1.json:160` `skill:grill-me` triggers are "grill me", "ask me questions about my idea", "question me about my project", "interview me about my idea", "first hackathon idea", "what should i build". The trigger loads `skills/grill-me/SKILL.md` — the same file (only two copies exist in the repo: staged `new-skills/grill-me/SKILL.md` and built `hackathon-ecc/skills/grill-me/SKILL.md`, md5-identical, `1577980e823b43d5ee9b6e8e612e1649`).
- The built skill's first content under `# Grill Me` (`:6`) is the full MODEL check at `:8` (same wording as legs 8–9). It precedes `## Workflow` (`:24`), the `## When to Use` / `## When NOT to Use` sections (`:12-22`), and therefore precedes the first question (Workflow step 2–3, `:26-28`, "Ask exactly one question at a time… Ask the mandatory first questions in the fixed order…").
- The check also fires on the skip path: if the user says "skip the grilling", the skill is still loaded and its :8 check is its first content, before the `## When NOT to Use` skip evaluation is acted on. Neither hackathon-mode §1 nor the orchestrate pre-grill block is on this path — and neither is needed, because the skill now carries its own check.
- `MODELSEL_F33` occurs exactly 1× in the grill-me skill (`:8`).

**Walked outcome:** on Auto, a bare "grill me" hits the MODEL ask before any question is asked and before any decision is recorded. **B-B5 is closed.** The D-1 shape does not survive on this path.

## Leg 11 — BYPASS-EXPANSION (B-B6 re-test): PASS — B-B6 CLOSED

**Scenario:** user types "make it much better" (trigger-routed) on Auto.

- Trigger routing verified in the manifest: `manifests/context-packs/skill-triggers@1.json:121` `skill:feature-expansion` triggers include "expand this", "flesh it out", "make it much better", "take it further", "add more features". The trigger loads `skills/feature-expansion/SKILL.md`.
- The built skill's first content of the file body (after the frontmatter, `:1-4`) is the full MODEL check at `:6` (same wording as legs 8–10). It precedes:
  - the decision-record read at `:8` ("Before proposing anything, read `docs/decision-record.md` for this project…"),
  - Phase 0 grounding at `:45` ("### Phase 0 — Ground in what exists (5 minutes, main agent)"), including the `code-explorer` subagent in Phase 0 step 3 (`:51`),
  - the Phase 1 four-subagent dispatch at `:57` ("Dispatch four brainstorm subagents **in parallel, in one message**", under `### Phase 1 — Brainstorm with subagents (parallel, four lenses)`, `:55`).
- Staged vs built: the two copies differ (md5 `845746a24cccb9beebc8ed0f9e6503fd` staged vs `058e7ae6b0b9fed644e1081abedee2f7` built) — but the diff is only the known build transformations (agent-path rewrites, e.g. `code-explorer` → `code-explorer` agent (`agents/ecc-code-explorer.md`) at `:51`/`:139`/`:198`, and the ECC-process wording at `:35-36`). The MODEL check line at `:6` is byte-identical in both copies, so the "staged flows verbatim" claim in the 33d report is slightly overstated in general but true for the guardrail itself. Not a fail; recorded so the coordinator is not misled by the "verbatim" wording.
- `MODELSEL_F33` occurs exactly 1× in the feature-expansion skill (`:6`).

**Walked outcome:** on Auto, a "make it much better" trigger hits the MODEL ask before the decision-record read, before Phase 0 grounding, and before the Phase 1 dispatch of four brainstorm subagents. **B-B6 is closed.**

## Leg 12 — COST-RECORDING: PASS

- **MODEL-SELECTED leg:** orchestrate L52 records the actual selected model in the run ledger: `MODEL: <name>` — the actual selected model. The run ledger is `.hackathon/run-ledger.md` (referenced as the ledger location in orchestrate L68, "the expansion section of `.hackathon/run-ledger.md`", and L52's own "record it in the run ledger"). On the leg-2 walk the ledger reads `MODEL: Grok 4.7 Extra High`.
- **MODEL-UNKNOWN leg:** L52: "A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool." So the ledger records the model as unverified and cost as unknown — no Grok/pool assumption is written anywhere.
- Rule text and record location both confirmed from the file (orchestrate L52 + L68). No separate cost-accounting system exists in the regular tree (OWED-33-3).

## Leg 13 — DRONE-UNCHANGED: PASS (with caveat)

**Scenario:** orchestrator briefs a reasoning drone + a coding drone for a multi-file task.

- Dispatch path is GLOBAL-ROUTING, `skills/orchestrate/SKILL.md:36`: "Every prompt is answered by the orchestrator model; drones never answer the user directly and never decide scope… The orchestrator keeps a queue of independent single-task jobs and dispatches drones into free slots… the orchestrator picks the best drone model for the task (fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work)… Every drone brief carries the exact goal, the files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return". The block is unchanged by fix33/33d (the 33d weave touched only guardrail text: the orch-change-feature removal section, orch-build-mvp step 1 + command, feature-dev/react-build entries, grill-me/feature-expansion entries, build.sh design-role wording).
- The unpin changed nothing on this path: the decides-tier `model: inherit` change touches only the orchestrator/design-lead/deep-reasoner agents; drone assignment text is untouched. The react-build resolver still pins the fast tier (`agents/ecc-react-build-resolver.md:4`, `model: cursor-grok-4.6-high-fast`).
- **Caveat (honest scope note, unchanged from #50/#51, not a fail of this leg):** the versioned pins named in the brief — reasoning DeepSeek V4.1 Flash 1017, coding Qwen3 Coder 30B — do **not** appear as model slugs anywhere in the regular built tree (grep for `DeepSeek V4` / `Qwen3 Coder` returns zero matches; the built tree names only "DeepSeek" and "Qwen" in the GLOBAL-ROUTING sentence above). The versioned drone pins live in the factory tree / fix30 SPEC, not in this regular tree — so this leg confirms the dispatch path is intact and unchanged by fix33/33d, but it cannot (and does not claim to) verify the versioned drone IDs from the regular tree itself.

## Leg 14 — DEMOTION-REGRESSION: PASS

**Scenario:** "design the dashboard for a clinic operations app".

- Routing still goes to Taste. Orchestrate routing-table row 10 (`skills/orchestrate/SKILL.md:137`): "a dashboard/app surface goes to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` as its lookup inventory and `less-flat-ui` texture where it fits, per hackathon-mode §5)."
- `rules/hackathon-mode.mdc:31-32`: "Every build — a full company or landing-page build, a dashboard/app surface, or a component — is led by `design-taste-frontend` (fix #32: the design lead for every surface). `ui-ux-pro-max` is the lookup inventory the lead consults after the direction is set; it never leads." / "`ui-ux-pro-max` is the lookup-only design inventory for dashboards and apps (fix #32)… consulted by the design-lead after the direction is set, never the design lead."
- `skills/ui-ux-pro-max/SKILL.md:3` frontmatter description: "LOOKUP ONLY (fix #32). … it is never the design lead. … Do NOT use to set a design direction, lead a dashboard/app/component build… (use design-taste-frontend for that)".
- DESIGNPKG-AUTO still present in orchestrate L35 and hackathon-mode. Counts unchanged: 72 skills / 45 agents / 55 commands / 48 rules (verified by directory listing). Fix #33 + round 33d did not regress fix #32. Browser-qa remains the sole executor of pass/fail screen verdicts (orchestrate L287: "the distinctiveness check lives ONLY in the Verify-step-5 visual loop (`browser-qa`, the sole executor)").

## Leg 15 — LIVE-TEST: PASS

**File:** `scratch-repo/fix30/live-test-prompt.md` (read in full; md5 `cd679e5e7ecd5f5ace654294ada24b47`, unchanged from dry-run #50/#51).

- Selection stated explicitly, header + L6: "Before starting, select **Grok 4.7 Extra High** in the model picker — this is Anish's default, and the test's baseline: since fix #33 the orchestrator runs on whatever model is selected, so the test verifies the SELECTED model runs the parent."
- Pass criterion matches: L45-47: "**PASS:** the parent agent ran the model selected in the picker (**Grok 4.7 Extra High** for this test) on both Task A and Task B (the model indicator says so)." L51-52: "**FAIL:** the parent ran anything other than the selected model on either task (e.g. it fell back to Grok 4.7 High, or to Auto)."
- Tasks A (reasoning-heavy decision doc, `DECISION.md`) and B (repo-scale TypeScript task queue, `src/queue.ts` / `src/worker.ts` / `src/index.ts` / `test/queue.test.ts`) unchanged; the required end-of-run report states, per task, which model ran the parent (from the chat model indicator) and which model ran each subagent, reporting only what the indicators actually showed. Subagent routing is explicitly not part of the pass criterion (L48-50: "subagent routing is a known Cursor limitation … only the parent matters").
- What Anish must do: fresh Cursor chat in a scratch project, select Grok 4.7 Extra High first, paste the prompt, run both tasks, report the indicators. Still owed (OWED-30-3, carried forward). The prompt was not changed by round 33d and needs no change: the guardrail re-sequence and the bypass weaves do not alter what the live test must prove.

---

## Failures (numbered)

None. No D-numbered failure. D-1 (dry-run #50) stays fixed (leg 1); D-2 (dry-run #50) stays fixed (leg 5); B-B1..B-B6 (audit #111-B) are all closed (legs 6–11).

## Gaps / notes for the coordinator

1. **Leg 7 nuance (for audit #112 to judge):** `skills/orch-build-mvp/SKILL.md:34` (narration-key prompt, "at the start of the run (step 1)") sits textually before step 1 (`:36`), and step 1's first clause is "Run orch-pipeline Step 0 first". On the command path the L7 check fires before the skill loads, so there is no ordering question there; on the direct-trigger path the L34-vs-Step-0 order is not explicitly sequenced in the skill. The prompt is conditional (demo video requested only), never blocks, and is a §7-sanctioned prompt — not scoping, slicing, Gate 1, expansion, dispatch, or build work — so it does not fail leg 7 as written. A one-line "after the MODEL check" sequencing note in L34 would remove the ambiguity entirely.
2. **Leg 6 note:** `commands/orch-change-feature.md:7` still states the engine runs its MODEL check first. On the removal branch the engine never runs; the operative check is the in-section one at skill `:47`. Harmless now, but the pointer sentence is still literally inaccurate for that branch. A wording correction (or a pointer to the section check) would make L7 true on both branches.
3. **Leg 11 note:** staged vs built `feature-expansion` is not byte-identical ("flows verbatim" in the 33d report is overstated); the differences are the known build transforms and the :6 guardrail line is identical in both. Grill-me staged vs built IS md5-identical.
4. **Leg 13 caveat (carried from #50/#51):** versioned drone pins (DeepSeek V4.1 Flash 1017 / Qwen3 Coder 30B) are not present as slugs in the regular built tree; the dispatch path is unchanged, but the pins themselves are verifiable only in the factory tree / fix30 SPEC.
5. **OWED-33-1 stands:** `model: inherit` is doc-verified, not live-verified; this simulated run cannot verify it. The live test (leg 15) remains owed to Anish.
6. **OWED-33-5 (out of scope, not a fail):** review-only dispatches (`/review-pr`, `/plan` second pass, `skill:council`) still carry no guardrail by design (D33-34). This dry run did not re-litigate that scoping decision.
7. Verify33 586/586 + both scan suites green now cover the re-sequence (§16l), the direct-command weave (§16m), and the routing-aware bypass checks (§16n) — and this dry run independently re-confirms all three areas by walking the tree, including the skill files the verifier's textual checks cannot execute.

## Files checked (built tree, `scratch-repo/hackathon-ecc/`, unless noted)

`skills/orchestrate/SKILL.md` (L10, L14, L35, L36, L52, L62, L64, L68, L95, L137, L287); `skills/orch-pipeline/SKILL.md` (L41-47); `skills/orch-add-feature/SKILL.md` (L31, section headers), `skills/orch-build-mvp/SKILL.md` (L8-36, L64, full read), `skills/orch-change-feature/SKILL.md` (L34, L41-47, L51-56, section headers, MODEL grep), `skills/orch-fix-defect/SKILL.md` (L33, section headers), `skills/orch-refine-code/SKILL.md` (L33-34, section headers); `skills/grill-me/SKILL.md` (L6-8, L12-28; staged copy md5-checked), `skills/feature-expansion/SKILL.md` (L6-8, L45, L51, L55-57; staged copy diffed); `agents/deep-reasoner.md`, `agents/ecc-architect.md`, `agents/ecc-healthcare-reviewer.md`, `agents/ecc-spec-miner.md`, `agents/ecc-react-build-resolver.md:4`; `commands/gan-build.md` (L5, L7), `commands/gan-design.md` (L5), `commands/astra-review.md` (L6, L12), `commands/orch-add-feature.md` (L7), `commands/orch-build-mvp.md` (L7, L29), `commands/orch-change-feature.md` (L7, L27), `commands/orch-fix-defect.md` (L7), `commands/orch-refine-code.md` (L7), `commands/orchestrate.md` (L7), `commands/feature-dev.md` (L5, L11-19, L31-43), `commands/react-build.md` (L5, L9-11, L13-20, L190); `rules/hackathon-mode.mdc` (L12, L31-32, L61, L63); `manifests/context-packs/skill-triggers@1.json` (L121, L160, L222, L229); `schemas/agent.schema.json` (enum, via prior verification); `skills/ui-ux-pro-max/SKILL.md:3`; `scratch-repo/fix30/live-test-prompt.md` (md5 `cd679e5e7ecd5f5ace654294ada24b47`); `fix33/SPEC.md` (D33-25…D33-35, OWED-33-4/33-5), `fix33/verify33-run33d.txt` (586/586), `fix33/fix-round-33d-report.md`, `fix33/audit111-report-B.md` (read in full), `fix33/dryrun50-report.md`, `fix33/dryrun51-report.md`.
