# Re-audit #111-B — fix #33 round 33c (adversarial bypass-hunt + independent verification)

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`; built tree `scratch-repo/hackathon-ecc/`
- **Round under audit:** fix round 33c (fixes audit #110 110-M1, sweep #53 S-M1/S-M2, dry-run #50 D-1/D-2)
- **Method:** independent re-runs of verify33.py + scans r4/r5; planted-violation probes in a full probe copy (never the real tree); full reads of all five orch-* command files, all five orch-* skill files, orch-pipeline, orchestrate (staged + built), hackathon-mode (staged + built), gan-build / gan-design / astra-review / orchestrate commands; own grep enumeration of all 55 commands + the 48 trigger-routed skills; own frontmatter model inventory; build.sh re-pin check.
- **Verdict: NOT PASS** — 6 blocking findings, 3 minor. The round's central claim is false for 2 of the 5 orch-* commands, and the independent entry-point enumeration found 4 more uncovered entry points into orchestrated work on Auto.

## Verdict summary

The verifier and both scan suites pass, the re-sequence is real on the main paths, and the unpin holds. But the choke-point claim — the thing round 33c exists to establish — does not survive a routing trace:

- **B-B1:** `/orch-change-feature` removal branch never runs the orch-pipeline engine, so the Step 0 MODEL check never fires on a removal. Deletion + commit + redeploy proceed on Auto.
- **B-B2:** `/orch-build-mvp` step 1 runs "orch-pipeline Phases 0–2 ONLY" and explicitly "does NOT run the full orch-pipeline engine". Step 0 (where the MODEL check lives) is not a phase, so it never runs on this path either.
- **B-B3–B-B6:** `/feature-dev`, `/react-build`, trigger-routed `grill-me`, and trigger-routed `feature-expansion` are uncovered entry points into orchestrated work on Auto, found by independent enumeration (not in the round's 9-file inventory).

Per the brief's verdict rules, any bypassable entry point or any orch-* command not actually flowing through the choke point is NOT PASS. B-B1 and B-B2 alone falsify the round's headline claim ("Step 0 is the shared choke point for all five orch-* commands… no cold start bypasses the ask", fix-round-33c-report §1.3 / SPEC D33-22).

What round 33c *did* fix is real and verified below: D-1 is closed on the main first-prompt and `/orchestrate` paths, D-2 is closed for `/gan-build`, `/gan-design`, `/astra-review`, and the three orch-* main paths (add/fix/refine), 110-M1/S-M1 (stale diff stat) is closed, and the verifier genuinely detects planted guardrail violations (probes A/B/C).

## Findings

### B-B1 (blocking) — `/orch-change-feature` removal branch bypasses the choke point

The command file routes removal requests *around* the engine:

- `commands/orch-change-feature.md:7` — the L7 pointer: "the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying)".
- `commands/orch-change-feature.md:27` — "If `$ARGUMENTS` asks to remove a feature — including a one-prompt removal of a first-build feature — follow the skill's `Removing a feature` section **instead of the change steps below**".
- `skills/orch-change-feature/SKILL.md:45` — `## Removing a feature` is a self-contained 6-step procedure (find files → delete → verify references → tests → redeploy → deliver report). It never invokes `orch-pipeline`, never mentions Step 0, and contains **zero** occurrences of `MODEL` (grep). The skill's engine invocation lives only in `## How It Works` step 1 (`SKILL.md:34`: "Run the `orch-pipeline` engine with the settings above"), which the removal branch explicitly skips.
- Contrast inside the same skill: `## Landing redesigns` (`SKILL.md:41`) says "The engine steps above still run". The removal section carries no such sentence.

Walk, direct invocation with Auto selected: `/orch-change-feature remove the voting widget` → command L7 pointer asserts the engine runs its check first → L27 routes to the removal section instead → the removal section traces the feature with `code-explorer`, deletes code/tests/routes/UI, commits, redeploys, delivers the final report. No Auto ask fires anywhere on this path. The L7 pointer is a dangling reference on this path: it describes an engine invocation that never happens.

Reachable a second way: the trigger manifest routes prose removals straight to the skill — `skill:orch-change-feature` triggers include "remove a feature" / "remove this feature" (`manifests/context-packs/skill-triggers@1.json`), bypassing the command file entirely. The orchestrate-routed removal (one-prompt removal of a first-build feature) is *not* affected — the MODEL check already fired upstream in orchestrate's pre-grill block — but the direct command and direct trigger paths are.

This is the same class as dry-run D-2, surviving inside the exact set of files round 33c claimed to close.

### B-B2 (blocking) — `/orch-build-mvp` step 1 never runs Step 0, so the MODEL check never fires

- `skills/orch-build-mvp/SKILL.md:36` — "1. Run orch-pipeline Phases 0–2 ONLY (Intake/Research/Plan) with the settings above … This step **does NOT run the full orch-pipeline engine** (phase mask 0→6): the later numbered steps ARE orch-pipeline Phases 3–6, each running once — orch-build-mvp step 3 is Phase 3 (Scaffold), step 4 is Phase 4 (Implement, GAN loop), step 6 is Phase 5 (Review), step 7 is Phase 6 (Commit)."
- The MODEL check lives in orch-pipeline `## Step 0 — Classify size`, built `skills/orch-pipeline/SKILL.md:43`. Step 0 is the classifier section that *precedes* `## The phases`; it is not Phase 0, not Phase 1, not Phase 2. No orch-build-mvp step runs Step 0: step 1 runs Phases 0–2, steps 3/4/6/7 run Phases 3/4/5/6. `MODEL` occurs zero times in `skills/orch-build-mvp/SKILL.md` (grep).
- The fix round's own report contradicts its own claim here: "each orch-* skill's step 1 runs the engine; orch-build-mvp runs Phases 0–2 in step 1" (fix-round-33c-report §1.3). The second clause concedes step 1 does not run the engine. SPEC D33-22 repeats the same self-contradiction verbatim.
- The command file's pointer (`commands/orch-build-mvp.md:7`, same Step 0 wording as the other four) is therefore false on this path, exactly as in B-B1.

Walk, direct invocation with Auto selected: `/orch-build-mvp` → skill step 1 reads the record/scope, extracts scope, orders thin vertical slices, ends at Gate 1 → step 2 expansion Phases 0–3 → step 4 drives `/gan-build … --skip-planner`. The downstream `/gan-build` drive *does* hit gan-build's own L5 full check — but only at step 4, after scoping, slicing, Gate 1, and expansion brainstorming have already run on Auto. The guardrail's "before anything else" / "before proceeding = any work" (D33-21) is not met on this path. Reachable also via the `skill:orch-build-mvp` triggers ("build an mvp", "turn this spec into an mvp"), which load the skill directly.

Note the asymmetry the round missed: the iteration-2 fix moved the check from Intake to Step 0 precisely because "the size classifier runs before the phases list — an Intake check would not precede all entry work". That move is what strands orch-build-mvp: its step 1 runs phases, not the classifier. The verifier's §16m checks are textual only (see §"Why the verifier misses B-B1/B-B2") and cannot see this.

### B-B3 (blocking) — `/feature-dev` starts orchestrated build work on Auto with no guardrail

Not in the round's 9-file inventory. `commands/feature-dev.md` is the standalone version of the orch-add-feature flow (the orch-add-feature skill itself says so: "Related: `/feature-dev` is a standalone version of this flow"):

- `:17` dispatches `code-explorer` to analyze the code; `:29` dispatches `code-architect` to design; `### 5. Implementation` (`:33`) implements the feature ("implement the feature following the approved design", TDD, small commits); `:41` dispatches `code-reviewer`.
- Zero occurrences of `MODELSEL_F33` / `MODEL check` in the file. No MODEL check anywhere on the path.

A user who runs `/feature-dev` instead of `/orch-add-feature` gets the same multi-agent build work with no Auto ask. This is a D-2-class bypass outside the inventoried set.

### B-B4 (blocking) — `/react-build` dispatches a factory drone and edits code on Auto with no guardrail

- `commands/react-build.md:9` — "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the react-build-resolver runs as a single-task factory drone with a director brief …" The command then runs the build, parses errors, and fixes incrementally ("Fix Incrementally: One error at a time, re-running build after each change"), with orchestrator verification and re-dispatch.
- Zero occurrences of `MODELSEL_F33` / `MODEL check` in the file.

Factory-drone implementation work on Auto, no ask. D-2-class bypass outside the inventoried set.

### B-B5 (blocking, bounded harm) — trigger-routed `grill-me` runs grill-me with no MODEL check

Task §4 asked for *every* path that reaches grill-me. The trigger path bypasses the pre-grill block:

- `manifests/context-packs/skill-triggers@1.json`: `skill:grill-me` triggers are "grill me", "ask me questions about my idea", "question me about my project", "interview me about my idea", "first hackathon idea", "what should i build". A user typing any of these loads `skills/grill-me/SKILL.md` directly.
- `skills/grill-me/SKILL.md` contains **zero** occurrences of `MODELSEL_F33` (grep). The skill runs the full Q&A and writes `docs/decision-record.md` with no model ask.
- Neither hackathon-mode §1 nor the orchestrate pre-grill block is on this path: hackathon-mode L12's MODEL check is conditioned on "the first hackathon project prompt", and the orchestrate skill is not loaded by a bare "grill me".

This is the D-1 shape surviving on a second path: grill-me proceeds on Auto without the ask, which D33-21 explicitly defines as "proceeding". Harm is bounded: grill-me is Q&A only (no code, no dispatch), and when the flow later reaches orchestrate / a first build prompt, the pre-grill MODEL check fires before any build work. Blocking because the entry point is bypassable under the brief's rule, but the harm is the Q&A itself, not a build on Auto.

### B-B6 (blocking) — trigger-routed `feature-expansion` dispatches 4 brainstorm subagents on Auto with no guardrail

- `manifests/context-packs/skill-triggers@1.json`: `skill:feature-expansion` triggers include "expand this", "flesh it out", "make it much better", "take it further", "add more features".
- `skills/feature-expansion/SKILL.md:55` — "Dispatch four brainstorm subagents **in parallel, in one message**", plus a `code-explorer` subagent when the codebase is unfamiliar (`:49`). Zero occurrences of `MODELSEL_F33` in the skill.
- The skill is split across flows (Phases 0–3 pre-build, Phases 4–6 inside orchestrate or orch-build-mvp), so the downstream build routing for a standalone post-first-build trigger is ambiguous in the skill text — but the Phase 1 dispatch itself is 4+ subagents on Auto with no ask, and the decided table "goes straight into the build" (`:133`) with no user approval step.

Dispatch work on Auto, no guardrail. D-2-class bypass outside the inventoried set.

### B-M1 (minor) — "Phase 0" vs "Step 0" wording slips in SPEC, patch log, and verifier

The operative check is in orch-pipeline **Step 0** (classifier), not Phase 0 (Intake). Three places say Phase 0:

- SPEC.md D33-22: "pointing at the operative check (orch-pipeline Phase 0 / the orchestrate skill)".
- `fix33/fix33-patch-log.md` DECISION-33-22: same "orch-pipeline Phase 0" phrase.
- `verify33.py` §16m: the section comment ("orch-pipeline Phase 0 (the shared choke point…)") and the check name at L3696 ("points at the orch-pipeline Phase 0 MODEL check").

Tree behavior is unaffected (the checks assert the Step 0 pointer phrase, which is correct). Docs/comment inaccuracy only.

### B-M2 (minor) — build.sh still writes the `grok-4.7-high` design-role pin; fix33.py scrubs it after

- `scratch-repo/build.sh:22208` (fix13-A patch): the *new* text written into `skills/orch-build-mvp/SKILL.md` contains "The design role runs on model `grok-4.7-high` (slug form only …)". The same stale pin is in the new text for orch-change-feature (`:22219`) and the other orch-* skills. The patch log confirms fix33.py unpins all five ("skills/orch-*-feature/SKILL.md: unpinned ('The design role runs on model `grok-4.7-high`' …)").
- Net effect on the shipped tree is nil (built-tree grep: zero `grok-4.7-high` outside the two strategic-compact keeps; verifier §16b would catch a miss). But the unpin of these prose lines is not in build.sh's own logic — it depends on fix33.py running after build.sh's patches. A build run without fix33.py reintroduces 5+ prose pins. Latent re-pin path, defense-in-depth note, not a live defect.

### B-M3 (minor) — review-only multi-agent dispatches carry no guardrail

- `/review-pr` (`commands/review-pr.md:19`) runs six specialized review agents; `/plan` dispatches an optional second deep-reasoner verification pass; the `skill:council` triggers ("should we do x or y", "go or no-go") dispatch Skeptic/Pragmatist/Critic subagents (`skills/council/SKILL.md:53`). None carries a MODEL check.
- Review/deliberation only: no code written, no commit, no deploy. Outside the orchestration-family scope the fix claimed, and the harm (a reviewer running on Auto-resolved model) is lower than a build on Auto. Minor; recorded for the coordinator to scope, not verdict-driving.

## Choke-point trace (per orch-* command)

Claim under test: "orch-pipeline Step 0 is the shared choke point for the five orch-* commands" (fix-round-33c-report §1.3, SPEC D33-22). The choke point itself is genuine: built `skills/orch-pipeline/SKILL.md:41-43`, `## Step 0 — Classify size (right-sizing)` opens with the full MODEL check as its first content, before the size classifier ("Ceremony scales to blast radius") and before Phase 0 Intake. The question is whether each orch-* path actually *reaches* it.

| Command | Command-file routing line | Skill step 1 | Reaches Step 0? |
|---|---|---|---|
| `/orch-add-feature` | `commands/orch-add-feature.md:7` pointer; "Invoke the `orch-add-feature` skill … (via the shared `orch-pipeline` engine)" | `skills/orch-add-feature/SKILL.md:31`: "1. Run the `orch-pipeline` engine with the settings above." | **Yes** — engine runs, Step 0 first. |
| `/orch-fix-defect` | `commands/orch-fix-defect.md:7` pointer; "Invoke the `orch-fix-defect` skill … (via the shared `orch-pipeline` engine)" | `skills/orch-fix-defect/SKILL.md:33`: "1. Run the `orch-pipeline` engine with the settings above." | **Yes** — engine runs, Step 0 first. |
| `/orch-refine-code` | `commands/orch-refine-code.md:7` pointer; "Invoke the `orch-refine-code` skill … (via the shared `orch-pipeline` engine — except the step-3 refactor-cleaner sweep, which the skill dispatches directly…)" | `skills/orch-refine-code/SKILL.md:33`: "1. Run the `orch-pipeline` engine with the settings above." Step 2's direct refactor-cleaner dispatch comes *after* step 1. | **Yes** — engine runs first; the direct dispatch is post-Step-0. |
| `/orch-change-feature` (change path) | `commands/orch-change-feature.md:7` pointer; "Invoke the `orch-change-feature` skill … (via the shared `orch-pipeline` engine)" | `skills/orch-change-feature/SKILL.md:34`: "1. Run the `orch-pipeline` engine with the settings above." | **Yes** (change path only). |
| `/orch-change-feature` (removal path) | `commands/orch-change-feature.md:27`: "follow the skill's `Removing a feature` section **instead of the change steps below**" | `skills/orch-change-feature/SKILL.md:45` `## Removing a feature`: 6 self-contained steps, no engine invocation, zero `MODEL` occurrences. | **No — B-B1.** |
| `/orch-build-mvp` | `commands/orch-build-mvp.md:7` pointer; "Invoke the `orch-build-mvp` skill — standalone only … (via the shared `orch-pipeline` engine — its numbered steps ARE orch-pipeline Phases 0–6…)" | `skills/orch-build-mvp/SKILL.md:36`: "1. Run orch-pipeline Phases 0–2 ONLY … This step **does NOT run the full orch-pipeline engine**." Later steps are Phases 3–6. Step 0 is not a phase and is never run. | **No — B-B2.** |

Score: **3 of 5 commands flow through the choke point on their main path; 2 of 5 do not on at least one reachable path.** A pointer without a routing edge is not coverage, and here the pointers at L7 actively misdescribe two paths.

## Entry-point coverage table (independent enumeration)

Method: all 55 files in `commands/` read or grepped for subagent/dispatch/code-writing behavior, plus the 48 trigger entries in `manifests/context-packs/skill-triggers@1.json`, plus `skills/orchestrate/references/dispatch-prompt.md` (downstream factory template — no independent entry; drones are dispatched only by the orchestrator, which is covered upstream). "Guardrail fires before work?" means the MODEL check (or a pointer to a check that actually runs on that path) executes before any work step.

| Entry point | What it starts | Guardrail present? | Fires before work? | Finding |
|---|---|---|---|---|
| First hackathon project prompt (hackathon-mode §1) | grill-me → scope → expansion → orchestrate build | Yes — L12 MODEL check first | Yes | — (D-1 closed here) |
| `/orchestrate` (command + skill) | orchestrate skill, full build | Yes — cmd L7 pointer + skill pre-grill block L52 | Yes | — |
| Prose "orchestrate / delegate / fan out" (`skill:orchestrate` triggers) | orchestrate skill | Yes — skill pre-grill block L52 | Yes | — |
| `/orch-add-feature` | orch-pipeline engine | Yes — L7 pointer, engine Step 0 runs | Yes | — |
| `/orch-fix-defect` | orch-pipeline engine | Yes — L7 pointer, engine Step 0 runs | Yes | — |
| `/orch-refine-code` | orch-pipeline engine (+ direct drone sweep at step 2, after Step 0) | Yes — L7 pointer, engine Step 0 runs first | Yes | — |
| `/orch-change-feature` (change) | orch-pipeline engine | Yes — L7 pointer, engine Step 0 runs | Yes | — |
| `/orch-change-feature` (removal) | delete → test → commit → redeploy → report | Pointer only; engine never runs | **No** | **B-B1** |
| `/orch-build-mvp` | Phases 0–2 → expansion → GAN loop → review → commit → deploy | Pointer only; Step 0 never runs | **No** (check first fires at step-4 `/gan-build` drive, after scoping/slicing/Gate 1/expansion) | **B-B2** |
| `/gan-build` | planner → generator → evaluator loop | Yes — full check L5, before arg parsing / Phase 0 | Yes | — (D-2 closed here) |
| `/gan-design` | design loop | Yes — full check L5, before Setup step 0 | Yes | — (D-2 closed here) |
| `/astra-review` | blind review + fix cycle | Yes — full check L6, before Step 1 Scope | Yes | — (D-2 closed here) |
| `/feature-dev` | code-explorer → code-architect → implement (TDD) → code-reviewer | No | **No** | **B-B3** |
| `/react-build` | factory drone (react-build-resolver) fix loop | No | **No** | **B-B4** |
| Prose "grill me" etc. (`skill:grill-me` triggers) | grill-me Q&A + decision record | No | **No** | **B-B5** |
| Prose "expand this / make it much better" (`skill:feature-expansion` triggers) | 4 brainstorm subagents + code-explorer; decided table → build | No | **No** | **B-B6** |
| `/review-pr` | 6 review agents | No | No (review-only) | B-M3 |
| `/plan` (optional 2nd deep-reasoner pass) | plan + optional reviewer subagent | No | No (review-only) | B-M3 |
| Prose "should we do x or y" (`skill:council` triggers) | 3 council subagents | No | No (deliberation-only) | B-M3 |
| `/prp-implement`, `/build-fix`, `/refactor-clean` | inline code edits, no subagent dispatch | No | No — but inline, no orchestration; out of the guardrail's harm model (no subagent on an unknown fallback) | Observation, not a finding |
| `/demo` | pitch-deck-video skill, inline (0 subagent mentions) | No | No — inline video work, no dispatch | Observation |
| Prose "scope the mvp" (`skill:hackathon-scope` triggers) | scope doc write, inline (0 subagent mentions) | No | No — inline planning/write | Observation |
| `/code-review`, `/fastapi-review`, `/python-review`, `/react-review`, `/harness-audit`, `/issue-review`, `/test-coverage`, `/quality-gate`, `/plan`, `/plan-prd`, `/prp-plan`, `/prp-prd`, `/prp-commit`, `/prp-pr`, `/pr`, `/epic-*`, `/checkpoint`, `/aside`, `/learn`, `/ecc-guide`, `/pm2`, `/resume-session`, `/save-session`, `/sessions`, `/setup-pm`, `/skill-create`, `/skill-health`, `/update-codemaps`, `/update-docs`, `/loop-start`, `/model-route`, `/auto-update` | review / docs / session / meta / advisory only; no subagent dispatch, no code writes (verified by grep: 0 subagent/dispatch mentions in each) | No | N/A — no orchestrated work starts here | — |

Note on `/demo`: it is user-invoked only and never part of the first-build sequence (fix #22 gate); its work is inline skill execution, not orchestration. Not counted as a bypass.

## Why the verifier misses B-B1/B-B2

§16m (`verify33.py:3675-3717`) is purely textual:

- Presence: `MODELSEL_F33` in each of the 9 command files; the full ask string in gan-build/gan-design/astra-review and orch-pipeline.
- Pointer phrase: "the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying)" in each orch-* command file.
- Line order *within each command file*: the MODELSEL line precedes "## What It Does" (or the first work step). For orch-change-feature, the removal branch lives *inside* "What It Does", so the check passes while the branch it routes to never runs the engine. For orch-build-mvp, the check passes because the pointer precedes "## What It Does" — nothing asserts the skill's step 1 runs Step 0.
- The orch-pipeline checks assert the check *is* the first content of Step 0 — true — but nothing asserts any orch-* skill *executes* Step 0.

The verifier proves the guardrail text exists in the right places; it does not prove the routing edges. That is exactly the gap this audit's trace was assigned to close, and the trace finds two missing edges.

## Re-sequence verification (D-1, every grill-me path)

- **First prompt path — CLOSED.** Built `rules/hackathon-mode.mdc:12`: "the MODEL check (fix #33, MODELSEL_F33) runs first — before grill-me … Then run `grill-me` FIRST among build steps … grill-me is the first BUILD step, and the MODEL check is not build work." First-build sequence reads "MODEL check → grill → narration-key prompt → …". §7 (`:61`): "plus the MODEL check just before it (fix #33, MODELSEL_F33), the one question that precedes grill-me". Staged copies identical on these lines (verified by read; staged-vs-built diff is only the known `claude -p` → `CLI-subprocess` scrub at L38).
- **`/orchestrate` path — CLOSED.** Built `skills/orchestrate/SKILL.md:52` pre-grill block: "**MODEL check — first, before grill-me (fix #33, MODELSEL_F33):** in the first reply, state the model … Grill-me does not start until a specific model is picked — the MODEL check is a precondition, not a build step, so grill-me stays FIRST among build steps." L14 cross-ref: "(see the MODEL check below — it runs before grill-me)". L64 step 0 is a back-reference only: "**MODEL check (fix #33):** already ran before grill-me … if the model is still Auto … stop and ask again". L95 picker note points at "the MODEL check, before grill-me". `MODELSEL_F33` exactly 2x (L14 + L52), staged + built. "Skip the grilling" path: the MODEL check precedes the skip too (it runs first, before grill-me; skipping grill-me does not skip the check).
- **Direct grill-me trigger path — OPEN (B-B5).** See finding above.
- **dispatch-prompt.md** (`skills/orchestrate/references/dispatch-prompt.md`): all 6 grill-me mentions are "after grill-me" carve-out references in drone-brief templates (e.g. `:50`, `:97`, `:118`, `:150`, `:216`, `:240`) — it never invokes grill-me. It is downstream of the orchestrator in all flows. No bypass here.
- **Other grill-me references** (feature-expansion, hackathon-scope, design-taste-frontend, deploy-fast, integration, pitch-deck-video, polish-pass, council, call-map.md): all are mentions of the decision record / "after grill-me" sequencing, not invocations. No other file runs grill-me.

## Pin scan (unpin holds)

- Frontmatter `model:` inventory across `agents/*.md` (built tree): **4× `model: inherit` + 41× `model: cursor-grok-4.6-high-fast`**, zero others. Matches the expected 4+41.
- `grok-4.7-high` / `Grok 4.7 High` in the built tree: only the two known keeps in `skills/strategic-compact/SKILL.md:68` and `:102` (factual model examples — context-window size, Cursor 2.1.233 todo-tool removal — not orchestrator identity). Zero `grok-4.7-extra-high` / `Grok 4.7 Extra High`.
- `schemas/agent.schema.json` enum is `["cursor-grok-4.6-high-fast", "inherit"]` (verified in the 565/565 run, §16i).
- build.sh: opus → `inherit` mapping at `:160-181` (`mapping = {"sonnet": "cursor-grok-4.6-high-fast", "opus": "inherit", "haiku": "cursor-grok-4.6-high-fast"}`); no re-pin path in the build logic. The `grok-4.7-high` strings in build.sh are old-text match patterns in audit patches (e.g. `:4246` common-performance old text; `:11588` astra-review old text) or new text that fix33.py subsequently scrubs (see B-M2). No surviving pin in the shipped tree.

## D-1 / D-2 closure walk

- **D-1 (MODEL-AUTO ordering) — CLOSED on the main paths, OPEN on the trigger path.** Walk: user on Auto sends the first project prompt → hackathon-mode L12 MODEL check fires first ("tell the user to pick a specific model before grill-me starts") → orchestrate pre-grill block L52 repeats it in the first reply → grill-me does not start until a specific model is picked. The dry-run #50 leg-1 failure (grill-me ran before the step-0 check) cannot recur on this path. The surviving shape is B-B5 (direct "grill me" trigger).
- **D-2 (direct-command bypass) — CLOSED for gan-build/gan-design/astra-review and 3 orch-* main paths; OPEN for 2 orch-* paths.** Walk `/gan-build` with Auto: `commands/gan-build.md:5` full check ("before anything else … If the selected model is Auto … tell the user to pick a specific model before proceeding") sits before arg parsing and before `### Phase 0: Setup`; Phase 1 step 0 (design-direction check) cannot run first. Same for `/gan-design` L5 (before `### Setup`) and `/astra-review` L6 (before `## Step 1: Scope`). Walk `/orch-add-feature`, `/orch-fix-defect`, `/orch-refine-code` with Auto: L7 pointer → skill step 1 runs the engine → Step 0 check L43 fires before the size classifier and Phase 0. Walk `/orch-build-mvp` with Auto: B-B2 — no check before step-4's `/gan-build` drive. Walk `/orch-change-feature remove …` with Auto: B-B1 — no check at all. OWED-33-4 must therefore be re-opened, not left SUPERSEDED: the deferral was fixed for the inventoried main paths only.

## What verified clean (numbers)

- **verify33.py: 565/565, exit 0** — independent re-run against the scratch-repo built tree: `python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc`. (Note: run with no argument it defaults to `~/workspace/hackathon-plugin/hackathon-ecc` and fails/crashes on the wrong tree — the explicit BASE argument is required; the fix report's 565/565 was reproduced only with the explicit path.)
- **Scan r4: 76/76, ALL PASS, exit 0.** Scan r5: **100/100, ALL PASS, exit 0** (run from a probe dir with fix32.py + fix32-patch-log.md adjacent, per the B-M2 note; probe dir deleted after).
- **Verifier probe (planted violations, full probe copy at `fix33/audit111b-probe/`, deleted after):**
  - Clean copy: **565/565, exit 0** (confirms the probe harness itself is faithful).
  - Probe A — deleted the MODEL check line from probe `commands/gan-build.md:5`: **562/565, exit 1**, exactly the 3 related §16m checks fail ("MODELSEL_F33 present in commands/gan-build.md", "full MODEL check ask at the entry of commands/gan-build.md", "MODEL check precedes the first work step in commands/gan-build.md").
  - Probe B — swapped L12 order in probe staged `new-rules/hackathon-mode.mdc` (MODEL clause after "run `grill-me` FIRST", the round-33c iteration-1 wording): **564/565, exit 1**, exactly the 1 L12 §16l check fails.
  - Probe C — deleted the MODEL check line from probe `skills/orch-pipeline/SKILL.md:43` (Step 0): **563/565, exit 1**, exactly the 2 Step 0 §16m checks fail ("full MODEL check ask opens orch-pipeline Step 0", "MODEL check is the first content of orch-pipeline Step 0").
  - The verifier therefore detects missing guardrail *text* precisely. It does not detect missing routing *edges* (B-B1/B-B2) — see "Why the verifier misses" above.
- **Diff stat:** `git diff --stat` vs HEAD `dd106ade`: **40 files changed, +166/−115** — matches MANIFEST.md:62 and fix33-implementation-report.md:203. 110-M1/S-M1 closed; grep for stale `+135`/`+136` in SPEC.md, MANIFEST.md, fix33.py, verify33.py, fix33-implementation-report.md: **zero live matches**.
- **fix33.py change arithmetic reconciles:** REPLACEMENTS = 35 entries (AST count: 25 pre-33c + 10 new) + 1 census line + 5 post/guard lines = **41** log entries, matching the patch-log "Changes (41)" header and the run-9 "fix33: 41 changes, 0 errors". The report's "(25 + 10 new replacements)" parenthetical is consistent with 35; no discrepancy.
- **Staged-vs-built diffs are only the known build transformations:** orchestrate differs in 3 lines, all `code-reviewer` → `code-reviewer` agent (`agents/ecc-code-reviewer.md`) path rewrites (L102, L276, L283); hackathon-mode differs in 1 line, the fix16 `claude -p` → `CLI-subprocess` scrub (L38).
- **Build log run 9:** `BUILD EXIT: 0`; run-7/8/9 sequence and the run-8 `--delete` incident are as reported (not re-litigated here).
- **Census:** 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks (verifier §16a, passing).

## Observations (not findings)

- O-1: `weave33.py` still contains the old L62 MODEL-check text (noted in the fix report as a deliberate historical-script freeze; it is not run by build.sh). No action.
- O-2: The fix report's §6 note that the run-7 562/565 result was overwritten by the run-9 565/565 pass is accurate; the 562/565 figure survives only in the report and MANIFEST. No action.
- O-3: The live test of the guardrail in a real Cursor chat (fix33/live-test-prompt.md) is still owed and can only be done by Anish on Windows. Static verification cannot close OWED-33-1 (`model: inherit` doc-verified, not live-verified) or OWED-30-3.
- O-4: The `/tmp` probe-copy attempt failed first (512 MB tmpfs filled at 100% by the 353 MB scratch-repo copy); the probe was redone under `fix33/audit111b-probe/` on the home disk and the probe dir was deleted after the probes. The real tree was never modified by this audit.

## Fix direction (for the coordinator)

- B-B1: put the full MODEL check at the top of the `## Removing a feature` section (or route the removal branch through orch-pipeline Step 0 first). The L7 pointer then reads true on both branches. Add a verifier check that no section in an orch-* skill bypasses step 1 — e.g. assert every `## ` section after `How It Works` in orch-change-feature either names the engine or is covered by a check.
- B-B2: run Step 0 (or the full check) at orch-build-mvp step 1 before Phases 0–2, or move the operative check to a location both step-1 formulations execute. Correct SPEC D33-22's self-contradictory sentence and re-open OWED-33-4 until both paths are covered.
- B-B3/B-B4: same mechanism as gan-build — full MODEL check at the entry of `commands/feature-dev.md` and `commands/react-build.md`.
- B-B5: add the MODEL check to `skills/grill-me/SKILL.md` (or route the `skill:grill-me` triggers through hackathon-mode §1). This is the cheapest close: one block in the skill.
- B-B6: add the MODEL check to `skills/feature-expansion/SKILL.md` Phase 0, before the Phase 1 dispatch.
- B-M1: correct "Phase 0" → "Step 0" in SPEC D33-22, the patch-log DECISION-33-22 string, and the verify33.py §16m comment/check name.
- B-M2: consider moving the design-role unpin into build.sh itself (or a build.sh comment noting fix33.py must run after the fix13-A patch) so the pin cannot return if fix33.py is skipped.
- Verifier extension (recommended): add routing-edge checks — e.g. assert `skills/orch-build-mvp/SKILL.md` step 1 references Step 0 (or contains the check), and assert no orch-* skill contains a top-level section that performs work without routing through the engine. Textual presence checks alone allowed B-B1/B-B2 through a 565/565 pass.

## Files checked (built tree unless noted)

`commands/orch-*.md` (all 5, full), `commands/orchestrate.md`, `commands/gan-build.md`, `commands/gan-design.md`, `commands/astra-review.md`, `commands/feature-dev.md`, `commands/react-build.md`, `commands/prp-implement.md`, `commands/build-fix.md`, `commands/refactor-clean.md`, `commands/plan.md`, `commands/review-pr.md`, `commands/code-review.md`, `commands/demo.md`, `commands/model-route.md`, `commands/loop-start.md`, `commands/epic-decompose.md` + grep over the other 37 command files; `skills/orch-pipeline/SKILL.md`, `skills/orch-add-feature/SKILL.md`, `skills/orch-fix-defect/SKILL.md`, `skills/orch-change-feature/SKILL.md`, `skills/orch-refine-code/SKILL.md`, `skills/orch-build-mvp/SKILL.md` (full); `skills/orchestrate/SKILL.md` (staged + built, L14/L52/L62/L64/L95), `rules/hackathon-mode.mdc` (staged + built, L12/§7), `skills/grill-me/SKILL.md`, `skills/feature-expansion/SKILL.md`, `skills/council/SKILL.md`, `skills/gan-style-harness/SKILL.md`, `skills/orchestrate/references/dispatch-prompt.md`, `skills/orchestrate/references/call-map.md`; `manifests/context-packs/skill-triggers@1.json` (all 48 entries); `schemas/agent.schema.json` (via verifier); `build.sh` (opus mapping L160-181; audit-patch old-text hits L4246/L11588; fix13-A new-text pin L22208/L22219); `fix33/fix33.py` (REPLACEMENTS AST count 35), `fix33/fix33-patch-log.md` (41 entries), `fix33/SPEC.md` (D33-20..D33-24), `fix33/MANIFEST.md:62`, `fix33/verify33.py` (§16l L3622-3671, §16m L3675-3717), `fix33/audit110-report.md`, `fix33/sweep53-report.md`, `fix33/dryrun50-report.md`, `fix33/build-log-run9.txt`, `fix33/verify33-run33c.txt`, `fix33/scan32-r4-run-fix33c.txt`, `fix33/scan32-r5-run-fix33c.txt`.

## Exact commands / results

```
# independent re-runs (real tree, explicit BASE)
python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc
  -> 565/565 checks pass, EXIT 0
python3 scan32-r4-test-fix33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc
  -> RESULT: ALL PASS (76 checks), EXIT 0
# r5 from probe dir with fix32.py + fix32-patch-log.md adjacent
python3 scan32-r5-test-fix33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc
  -> RESULT: ALL PASS (100 checks), EXIT 0
# probe copy (full scratch-repo copy under fix33/audit111b-probe/, deleted after)
python3 verify33.py <probe>/hackathon-ecc            -> 565/565, EXIT 0 (clean)
# Probe A: delete probe commands/gan-build.md:5     -> 562/565, EXIT 1 (exactly 3 §16m FAILs)
# Probe B: swap L12 order, probe new-rules/hackathon-mode.mdc
                                                      -> 564/565, EXIT 1 (exactly 1 §16l FAIL)
# Probe C: delete probe skills/orch-pipeline/SKILL.md:43
                                                      -> 563/565, EXIT 1 (exactly 2 §16m FAILs)
cd scratch-repo && git rev-parse --short HEAD        -> dd106ade
git diff --stat HEAD | tail -1                        -> 40 files changed, 166 insertions(+), 115 deletions(-)
grep -rh "^model:" hackathon-ecc/agents/ | sort | uniq -c
  -> 41 model: cursor-grok-4.6-high-fast / 4 model: inherit
grep -rn "MODELSEL_F33" hackathon-ecc/skills/grill-me/SKILL.md hackathon-ecc/skills/feature-expansion/SKILL.md
  -> 0 matches in both
```

Nothing was edited or committed by this audit. The probe copy under `fix33/audit111b-probe/` was deleted after the probes; probe logs are at `/tmp/audit111b-verify-probeclean.txt`, `/tmp/audit111b-verify-probeA.txt`, `/tmp/audit111b-verify-probeB.txt`, `/tmp/audit111b-verify-probeC.txt` (ephemeral).
