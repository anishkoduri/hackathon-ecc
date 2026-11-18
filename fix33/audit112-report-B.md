# Re-audit #112-B — fix #33 round 33d (adversarial bypass re-trace + independent verification)

- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Tree:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`; built tree `scratch-repo/hackathon-ecc/`
- **Round under audit:** fix round 33d (fixes audit #111-B B-B1..B-B6 + B-M1/B-M2/B-M3, audit #111-A A-M1/A-M2)
- **Method:** full re-reads of all six bypass paths (command file → skill file → engine step) in the run-10 built tree; staged-vs-built diffs for the two staged skills; own grep enumeration of all 55 commands + all 48 trigger-routed skills + all `skills/*/references/` files for dispatch instructions; build.sh fix13-A/fix13e patch-table read in code; independent re-runs of verify33.py + scans r4/r5; planted-violation probes in a full probe copy (never the real tree); own frontmatter model inventory + pin census.
- **Verdict: NOT PASS** — 1 blocking finding (1 new bypass), 0 minor. All six of the #111-B bypasses are genuinely closed and B-M2 is fixed at the root, but the new-bypass hunt found one more uncovered dispatch path the round did not inventory.

## Verdict summary

Round 33d did the work it claimed on the six known bypasses. Each re-trace below quotes the operative check in place before the first work step on its path, and the verifier detects a planted deletion of two of them with exactly the related checks failing. B-M2 is fixed at the root: build.sh no longer writes the design-role pin anywhere, the five fix33.py scrub tuples are gone, and the built orch-* skills contain zero `grok-4.7-high`. The unpin and the demotion hold, and the verifier + both scan suites pass.

But the hunt found a seventh path of the same class, one level deeper than the 33c/33d inventories went — inside a skill reference file, not a skill file:

- **B-N1:** trigger-routed `design-taste-frontend` → its `## Redesign` section (`SKILL.md:454`) routes a full-page redesign to `references/hallmark/references/redesign.md` → past three pages at restyle/full depth, "give each page to its own subagent" — factory drones that write code. Zero `MODELSEL_F33` anywhere in the design-taste-frontend skill (staged or built). No MODEL check fires on this path.

Per the brief's verdict rules, any new bypass is NOT PASS, blocking. B-N1 is narrower than B-B1..B-B6 (it needs a 4+ page redesign at restyle/full depth; a 1–3 page redesign works inline and never dispatches), but it is the same class as B-B6 — a trigger-routed skill dispatching code-writing subagents on Auto with no ask — and its harm (code-writing drones) is strictly greater than B-B5's (Q&A only), which was blocking in audit #111-B. The primary in-flow routes into the redesign are covered (orch-change-feature Landing redesigns run the engine's Step 0 first; orchestrate's polish-routed redesign sits downstream of the pre-grill check); only the standalone skill-load path is open.

## Findings

### B-N1 (blocking) — trigger-routed Hallmark redesign fans out page drones past three pages with no MODEL check

The chain, read end to end in the run-10 built tree:

1. Entry. `manifests/context-packs/skill-triggers@1.json` routes `skill:design-taste-frontend` from "design a landing page", "redesign the landing page", "landing page design", "company page design", "design the dashboard", "redesign the app ui", "dashboard design", "app interface design".
2. Skill routing. Built `skills/design-taste-frontend/SKILL.md:454`:
   > "**Redesign of an existing page (keeping content + wiring).** When the job is a full-page redesign that keeps every fact, link, form, field, handler, route, id, and test hook, follow the Hallmark redesign flow (`references/hallmark/references/redesign.md`) — factory routing for the redesign flow lives there: page subagents are single-task factory drones with director briefs (GLOBAL-ROUTING_F29)."
   The staged copy (`new-skills/design-taste-frontend/SKILL.md:454`) carries the identical line.
3. The dispatch. Built `skills/design-taste-frontend/references/hallmark/references/redesign.md`, `## Build` section ("More than one page" paragraph):
   > "Past three pages, give each page to its own subagent where the harness has them, with that tokens file, the page's files and this file. **Factory routing (fix #29, GLOBAL-ROUTING_F29):** each page subagent is a single-task factory drone with a director brief (DIRECTOR-BRIEF_F29): the goal, the page's files in scope and explicitly out of scope, constraints, acceptance criteria, verification steps, and what to return — an incomplete brief means the drone does not start."
   Each page drone builds its page — code-writing dispatch, not review.
4. No guardrail anywhere on the path. `grep -rn "MODELSEL_F33" hackathon-ecc/skills/design-taste-frontend/` → zero matches (exit 1); `grep -c "MODELSEL_F33" new-skills/design-taste-frontend/SKILL.md` → 0. The redesign.md file itself contains zero `MODEL check` / `MODELSEL_F33` occurrences. The six skill files in the built tree that contain `MODELSEL_F33` are exactly `feature-expansion`, `grill-me`, `orch-build-mvp`, `orch-change-feature`, `orch-pipeline`, `orchestrate` — design-taste-frontend is not among them.

Walk, direct invocation with Auto selected: user types "redesign the app ui" on a 5-page app → design-taste-frontend loads → :454 routes to the Hallmark redesign flow → the redesign's Picks block is shown and the build proceeds → past three pages, one factory drone per page is dispatched with a director brief → pages are rebuilt on Auto. No model ask fires anywhere on this path. The redesign flow's own "The ask" (three questions: what must stay / what is wrong / anything new to show) precedes the build but does not resolve Auto — answering "go ahead" does not pick a model.

Scope notes (why this is narrow but still blocking):

- **Conditional on >3 pages.** At restyle/full depth with 1–3 pages the design-lead works inline; no subagent is dispatched and nothing in the guardrail's harm model fires. The file's own worked example is exactly 3 pages (`Redesign · full · 3 pages`), which does not fan out. The bypass opens only at 4+ pages.
- **Depth-gated.** Polish depth never fans out (the sweep fixes in place); only restyle and full do.
- **Loading gate.** redesign.md's header says it loads "only when the user names Hallmark with `redesign` or `audit`". SKILL.md:454 routes *any* full-page redesign job there, so the strictest reading still reaches the dispatch whenever Hallmark is named, and arguably whenever a full-page redesign is requested. The header narrows the entry; it does not close the path.
- **Reachability footing.** Per `skills/orchestrate/references/call-map.md` method note B6, `skill-triggers@1.json` itself has no live Cursor entry point (the loader chain was removed as dead weight in fix #28) — the manifest is a documentation-only reference table. The trigger paths in this audit (B-B5/B-B6 in #111, B-N1 here) therefore rest on Cursor's description routing (call-map blind spot B1: "Cursor can fire a skill from its SKILL.md description with no textual reference anywhere"), which is exactly the footing audit #111-B and round 33d already accepted for B-B5/B-B6. B-N1 stands on no weaker footing than the six bypasses round 33d just closed.
- **Covered in-flow routes.** The two routes the plugin itself drives into this flow are covered: orch-change-feature `## Landing redesigns` ("The engine steps above still run" — engine Step 0 first) and orchestrate's polish-routed redesign (downstream of the pre-grill MODEL check). Only the standalone skill-load path is open — the same shape as B-B5/B-B6.

Fix direction (for the coordinator): the same mechanism as B-B5/B-B6 — weave the full MODEL check (MODELSEL_F33 wording) at the entry of `skills/design-taste-frontend/SKILL.md` (staged source, flows into the built tree), before the redesign routing at :454, or at the top of `redesign.md` itself so every load of the flow is covered including the orch-driven ones (which would then re-fire and pass silently once a model is picked). Add a §16n-style verifier check asserting the check precedes the fan-out paragraph. Note for the fix worker: the skill's hero/finish review subagents (`gates.md:243`) and the manual-gate / fresh-reader subagents (`gate.md:179-180`, `copy-voice.md:173`) are review-only and stay in the B-M3/OWED-33-5 class — only the page-drone fan-out writes code.

## Per-bypass re-trace (B-B1..B-B6 — all CLOSED)

### B-B1 — `/orch-change-feature` removal branch — CLOSED

- Built `skills/orch-change-feature/SKILL.md:45` (`## Removing a feature`), `:47` — the MODEL check is the section's first content, before step 1 (delete):
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
- The check precedes every removal step: step 1 trace/delete, step 2 verify references, step 3 tests, step 4 commit (with the never-commit-broken rule), step 5 redeploy + bounded deploy poll, step 6 final report. All six steps follow :47 in the same section.
- Trigger path covered: `skill:orch-change-feature` ("remove a feature" / "remove this feature") loads the skill directly; the agent reaching the `Removing a feature` section hits :47 before any removal step. The command file's L7 pointer (`commands/orch-change-feature.md:7`, "the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying)") is now supplemented by the operative check in the section itself, and L27's routing ("follow the skill's `Removing a feature` section instead of the change steps below") lands on the check.
- Change path unchanged and still covered (skill step 1 runs the engine → Step 0). Landing-redesigns section still routes through the engine ("The engine steps above still run").

### B-B2 — `/orch-build-mvp` step 1 runs Step 0 — CLOSED

- Built `skills/orch-build-mvp/SKILL.md:36` (step 1, one long line):
  > "1. Run orch-pipeline Step 0 first (Classify size — the MODEL check, fix #33, MODELSEL_F33, is the first content of Step 0 and runs before anything else: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback), then Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan)."
- Both mechanisms the audit allowed are present: the routing edge (Step 0 named first) AND the operative ask restated inline at step 1's entry. No scoping, slicing, or Gate 1 precedes the check — all of that text comes after the Step 0 clause inside the same step-1 line, and expansion is step 2, after step 1.
- Command file corrected the same way (`commands/orch-build-mvp.md:29`): "This is orch-build-mvp step 1 = orch-pipeline Step 0 (MODEL check + Classify) first, then Phases 0–2 only — it never runs the full engine."
- The sentence "This step does NOT run the full orch-pipeline engine (phase mask 0→6)" still follows in step 1 — now true and harmless, since Step 0 is invoked explicitly before the phases rather than via the full engine. The downstream step-4 `/gan-build` drive still re-checks after the model is picked (passes silently).
- Caveat recorded as observation O-2 (not a finding): two paragraphs textually precede step 1 — the "Precondition" file-existence check and the "Narration-key prompt" paragraph ("At the start of the run (step 1), if the user asked for a demo video…"). See Observations.

### B-B3 — `/feature-dev` — CLOSED

- Built `commands/feature-dev.md:5` (right after the frontmatter):
  > "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."
- First work step is the `code-explorer` dispatch at `:19` ("use `code-explorer` agent (`agents/ecc-code-explorer.md`) to analyze the relevant existing code"). Phase 1 Discovery (clarifying questions, `:11-17`) also follows the check. The check precedes all dispatch.

### B-B4 — `/react-build` — CLOSED

- Built `commands/react-build.md:5`, same full MODEL check text as B-B3, right after the frontmatter.
- Factory routing / drone dispatch at `:11` ("the react-build-resolver runs as a single-task factory drone with a director brief…"). The check precedes it. Drone pins and dispatch mechanisms untouched (verified by read — the file's factory-routing paragraph and fix loop are unchanged apart from the inserted check).

### B-B5 — trigger-routed `grill-me` — CLOSED

- Staged `new-skills/grill-me/SKILL.md:8` and built `hackathon-ecc/skills/grill-me/SKILL.md:8`, identical: full MODEL check as the first content under `# Grill Me` (`:6`), before `## When to Use` and `## Workflow` (`:24`).
- Staged-vs-built diff: **identical** (`diff` silent). The trigger path ("grill me", "ask me questions about my idea", … in `skill-triggers@1.json`) loads the skill directly and hits the check before any question is asked.

### B-B6 — trigger-routed `feature-expansion` — CLOSED

- Staged `new-skills/feature-expansion/SKILL.md:6` and built `hackathon-ecc/skills/feature-expansion/SKILL.md:6`, identical check line: full MODEL check as the first content of the file body (after the frontmatter).
- The check precedes the decision-record read (`:8`, "Before proposing anything, read `docs/decision-record.md`…"), Phase 0 grounding (`:45`), and the Phase 1 dispatch (`:55`, "Dispatch four brainstorm subagents **in parallel, in one message**" — the four-lens dispatch the audit flagged — plus the `code-explorer` subagent at Phase 0 step 3 for an unfamiliar codebase).
- Staged-vs-built diff is NOT byte-identical (see observation O-3), but the MODEL check line itself is byte-identical in both copies and every differing line is a pre-existing build transformation (agent-path insertions), not a 33d edit. The guardrail flows intact.

## B-M2 re-verification — FIXED AT THE ROOT

- build.sh fix13-A header comment updated (`:22197`, "the Grok pin is gone — the design role runs on the model selected in this chat"). New text read in code:
  - `:22208` (orch-build-mvp): "The design role runs on the model selected in this chat (the design-lead tier inherits the chat model — see the picker note in orchestrate SKILL.md step 4)."
  - `:22219` (orch-change-feature) and the fix13e block 7a/7b/7c (`:22696` orch-add-feature, `:22701` orch-fix-defect, `:22707` orch-refine-code): "The design role runs on the model selected in this chat."
- `grep -c "grok-4.7-high" build.sh` → **39** (was 44, matches the 33d report). `grep "The design role runs on model" build.sh` → **zero** matches — no pin-form design-role writing remains anywhere in build.sh. The remaining 39 lines are old-side anchors (e.g. `:4246` common-performance old text, `:7825`/`:11592` astra-review STEP 5 anchor lines, `:22662-23035` gan-build/gan-design/gan-planner old text, `:22687` the old picker-note text) or comments — all still scrubbed downstream by fix33.py where they reach the built tree.
- fix33.py scrub tuples gone: `grep "design role runs on model" fix33.py` → zero matches. `REPLACEMENTS` = **35** tuples (AST count), `MODELSEL_F33` 30 occurrences in fix33.py (old-side anchors for the README/gan-planner/astra-review sites + the new guardrail tuples and D33-25..D33-28 decision strings). DECISION-33-25/26/27/28 strings present and accurate.
- Built orch-* skills: `grep -rn "grok-4.7-high" skills/orch-*/SKILL.md commands/orch-*.md` → zero matches.
- fix24.py G-4 consequence verified independently: `grep "slug form only" fix24/fix24.py` → zero matches (the removed sub is gone); "select Grok 4.7 High" survives exactly once in fix24.py (the `:581` README F-1/F-2 old-side anchor, which must stay) and zero times in build.sh.
- Built-tree census (verifier §13, passing): ID 0, PROSE 2 (the strategic-compact keeps at `:68`/`:102`), XID 0, XPROSE 0, fast 72.

## New-bypass hunt (independent enumeration)

Method: all 55 `commands/*.md` grepped for subagent/dispatch/agent mentions; all 48 trigger keys in `skill-triggers@1.json` enumerated and each skill grepped for subagent/dispatch mentions; all `skills/*/references/**/*.md` grepped for subagent/dispatch instructions; the five orch-* skills re-read in full for "instead of" branches and "Phases X–Y ONLY" carve-outs.

| Entry point / site | What it starts | Guardrail? | Verdict |
|---|---|---|---|
| `/orch-add-feature`, `/orch-fix-defect`, `/orch-refine-code` | orch-pipeline engine (step 1) | Yes — Step 0 first; refine-code's step-2 direct refactor-cleaner dispatch is post-Step-0 | Clean |
| `/orch-change-feature` change path | engine | Yes — Step 0 | Clean |
| `/orch-change-feature` removal path | removal section | Yes — :47 check (B-B1 fix) | Clean |
| `/orch-build-mvp` | Step 0 then Phases 0–2 | Yes — step 1 (B-B2 fix) | Clean |
| `/orchestrate`, first prompt, `skill:orchestrate` | orchestrate pre-grill block | Yes — L52 | Clean |
| `/gan-build`, `/gan-design`, `/astra-review` | GAN loop / review | Yes — full check at entry | Clean |
| `/feature-dev`, `/react-build` | dispatch / factory drone | Yes — entry check (B-B3/B-B4 fix) | Clean |
| `skill:grill-me`, `skill:feature-expansion` | Q&A / 4 brainstorm subagents | Yes — skill-entry check (B-B5/B-B6 fix) | Clean |
| `skill:orch-*` (all 5) | engine / removal / Step 0 | Yes — via skill step 1 or section check | Clean |
| `skill:gan-style-harness` ("gan build", "build with the gan harness") | harness design/rubric only — its Usage routes through `/gan-build` / `/gan-design` | Yes — via the checked commands; the skill "contributes the harness design, prompts, and rubric, never the CLI commands" and contains no dispatch instruction of its own | Clean |
| `skill:app-scaffold`, `skill:deploy-fast`, `skill:polish-pass` | scaffold / deploy / polish, inline (zero agent/subagent mentions in any of the three skills) | N/A — inline work, no subagent dispatch (same class as `/prp-implement`, `/build-fix` in #111) | Clean (observation) |
| `skill:hackathon-scope`, `skill:ai-feature-spec`, `skill:api-integration`, `skill:tdd-workflow`, `skill:git-workflow`, `skill:readme-writer`, `skill:devpost-autofiller`, `skill:hackathon-pitch`, `skill:pitch-deck-video`, `skill:browser-qa`, `skill:click-path-audit`, `skill:verification-before-completion`, `skill:security-review`, `skill:systematic-debugging`, `skill:design-system`, `skill:frontend-*`, `skill:motion-*`, `skill:less-flat-ui`, `skill:make-interfaces-feel-better`, `skill:mobile-ship`, `skill:backend-patterns`, `skill:postgres-patterns`, `skill:python-*`, `skill:typescript-patterns`, `skill:api-design`, `skill:error-handling`, `skill:track-picker`, `skill:frontend-slides` | inline skill work (0 subagent/dispatch mentions in each SKILL.md) | N/A — no dispatch | Clean |
| `/review-pr`, `/react-review`, `/fastapi-review`, `/code-review`, `/python-review`, `/harness-audit`, `/plan` (optional 2nd deep-reasoner pass), `skill:council` | review / deliberation subagents only | No | B-M3 class (OWED-33-5, recorded not fixed) — unchanged |
| Hallmark hero/finish review subagents (`design-taste-frontend/references/hallmark/references/gates.md:243`), manual-gate subagent (`gate.md:179-180`), fresh-reader subagent (`copy-voice.md:173`) | review subagents inside the design flow | No | B-M3 class (review-only) — unchanged |
| `/prp-implement`, `/build-fix`, `/refactor-clean`, `/demo`, `/model-route`, `/loop-start`, `/quality-gate`, `/prp-commit` (commit-reviewer presents the message, never runs `git commit`), `/prp-plan`, `/prp-prd`, `/prp-pr`, `/epic-*`, `/checkpoint`, `/aside`, `/learn`, `/ecc-guide`, `/pm2`, `/resume-session`, `/save-session`, `/sessions`, `/setup-pm`, `/skill-create`, `/skill-health`, `/update-codemaps`, `/update-docs`, `/test-coverage`, `/react-test` | inline / docs / session / meta / advisory; no subagent dispatch of build work (verified by grep) | N/A | Clean |
| `skill:design-taste-frontend` → Hallmark redesign, **>3 pages** | **one factory drone per page, code-writing** | **No** | **B-N1 (blocking)** |
| `skill:verification-loop`, `skill:production-audit`, `skill:delivery-gate` | END-ONLY deferred skills (0 dispatch mentions; trigger note documents the deferral) | N/A | Clean |

Other carve-outs checked: the only "does NOT run the full orch-pipeline engine" in the tree is orch-build-mvp `:36`, now Step-0-first; the only "instead of the change steps below" is orch-change-feature `:27`, now covered at the section. No other orch-* skill contains an alternate branch (re-read orch-add-feature, orch-fix-defect, orch-refine-code in full). `skills/orchestrate/references/dispatch-prompt.md` remains downstream-only (drones dispatched by the orchestrator, covered upstream).

## What verified clean (numbers)

- **verify33.py: 586/586, exit 0** — independent re-run against the scratch-repo built tree (`python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc`). §16n's 21 checks all pass, including the B-M2 build.sh/fix24.py assertions and the patch-log assertions (D33-25..D33-35, OWED-33-5, OWED-33-4 RE-OPENED).
- **Scan r4: ALL PASS (76/76, exit 0).** Scan r5: **ALL PASS (100/100)** — run from a probe dir with `fix32.py` + `fix32-patch-log.md` adjacent to the script (in-place run from fix33/ crashes with `FileNotFoundError: fix32.py`, same as audit #111-B's B-M2 note; the probe-dir run passes).
- **Verifier probes (full probe copy at `fix33/audit112b-probe/repo/`, deleted after):**
  - Clean copy: **586/586, exit 0** (probe harness faithful).
  - Probe A — deleted the MODEL check line from probe `skills/orch-change-feature/SKILL.md:47` (Removing section): **584/586**, exactly the 2 related §16n B-B1 FAILs ("MODELSEL_F33 present in skills/orch-change-feature/SKILL.md", "full MODEL check ask is the first content of the Removing a feature section").
  - Probe B — deleted the MODEL check line from probe `commands/feature-dev.md:5`: **584/586, exit 1**, exactly the 2 related §16n B-B3 FAILs ("full MODEL check ask at the entry of commands/feature-dev.md", "MODEL check precedes the first work step in commands/feature-dev.md"). Probe B output saved at `/tmp/audit112b-probeB.txt` (ephemeral).
  - The verifier therefore detects a missing bypass guardrail precisely. It does not detect a missing routing edge into a file it does not check (B-N1 lives in a reference file §16n never looks at) — the same static-presence limit the round itself states in SPEC D33-35.
- **Diff stat:** `git diff --stat` vs HEAD `dd106ade`: **47 files changed, +196/−126** — matches MANIFEST.md:67 and the round-33d report §5.
- **Frontmatter inventory (built `agents/*.md`): 4× `model: inherit` + 41× `model: cursor-grok-4.6-high-fast`**, zero others. Matches the expected 4+41.
- **Triggers / coverage:** 48 trigger keys in `skill-triggers@1.json` (counted from the JSON); coverage 72 skills / 48 with triggers (verifier §16a, passing); 72 skill dirs on disk.
- **md5 sync:** `fix33.py` canonical + scratch `cda0e5be0c9ed0030f73fddf07c527c0`; `fix33-patch-log.md` canonical + scratch `8ae4664f7a64a1bf5ae6fd7cfa044ea0`; `fix-round-33d-report.md` canonical + scratch `c7ba60150f05f5e65e69023ecdb0af88` — all as claimed.
- **Verifier-limit honesty:** SPEC D33-35 states the limit ("§16l/§16m/§16n are static presence + line-order checks within files, not proof of execution") and the round-33d report §6 repeats it. Honestly recorded; this audit's manual re-trace is what caught B-N1, not the verifier.

## Observations (not findings)

- O-1: `weave33.py` still contains the old L62 MODEL-check text (deliberate historical-script freeze, not run by build.sh). No action. (Carried from #111.)
- O-2: orch-build-mvp's narration-key prompt paragraph textually precedes step 1 ("At the start of the run (step 1), if the user asked for a demo video…"), and the "Precondition" file-existence check does too. A strict top-down reading could issue the single narration-key user prompt before the step-1 MODEL check. This is not a bypass under the guardrail's harm model: the narration prompt dispatches nothing, builds nothing, and asks the user for an env key — it is not orchestration on an unknown fallback, and none of the named sub-steps (scoping/slicing/Gate 1/expansion) precedes the check. Noted so the ordering ambiguity is on the record, not because it opens a path.
- O-3: the round-33d report's "Staged source flows verbatim" for feature-expansion is loose as a blanket statement: staged-vs-built diff shows ~10 differing lines (description line, the "ECC process applies" vs "No planning documents" paragraph, and `code-reviewer` → `code-reviewer` agent (`agents/ecc-code-reviewer.md`) path insertions). The MODEL check line itself is byte-identical, and every differing line is a pre-existing build transformation (the same agent-path rewrite class as orchestrate's known staged-vs-built diff), not a 33d edit. Not a finding — the guardrail flows intact — but the report's wording overstates it. (grill-me staged==built exactly.)
- O-4: SPEC §3(e) (16f) still says "fast 70" where the true pre-state fast count is 71 — disclosed in the round-33d report §6 as known and out of scope, left as-is. Carried, not re-litigated.
- O-5: the live test of the guardrail in a real Cursor chat is still owed and can only be done by Anish on Windows. Static verification cannot close OWED-33-1 or OWED-30-3.
- O-6: a leftover `fix33/audit112-probe/` directory (not this audit's — this audit used `audit112b-probe/`, deleted after the probes) was present in fix33/ during this audit. Left untouched.

## Fix direction (for the coordinator)

- B-N1: weave the full MODEL check (MODELSEL_F33 wording) at the entry of `skills/design-taste-frontend/SKILL.md` (staged source — the :454 redesign routing is identical staged and built, so one staged edit covers both copies), before the redesign routing, or at the top of `redesign.md` itself so every load of the flow is covered. Add a §16n-style verifier check asserting the check precedes the ">3 pages" fan-out paragraph. The check re-firing on the orch-driven redesign routes passes silently once a model is picked — no second ask.
- Verifier extension (recommended, same lesson as B-B1/B-B2): §16n asserts presence + order inside inventoried files only. A reference-file dispatch (redesign.md) sailed through a 586/586 pass. Consider a check that no `references/` file reachable from a trigger-routed skill instructs a code-writing dispatch without a MODEL check on the path — or at minimum, add the design-taste-frontend entry + redesign fan-out to the §16n inventory.

## Files checked (built tree unless noted)

`commands/orch-change-feature.md`, `commands/orch-build-mvp.md`, `commands/feature-dev.md`, `commands/react-build.md` (full); `skills/orch-change-feature/SKILL.md` (full), `skills/orch-build-mvp/SKILL.md` (full through step 9), `skills/orch-add-feature/SKILL.md` (full), `skills/orch-fix-defect/SKILL.md` (full), `skills/orch-refine-code/SKILL.md` (full), `skills/orch-pipeline/SKILL.md` (Step 0), `skills/grill-me/SKILL.md` (staged + built, diffed), `skills/feature-expansion/SKILL.md` (staged + built, diffed), `skills/design-taste-frontend/SKILL.md` (staged + built, :454), `skills/design-taste-frontend/references/hallmark/references/redesign.md` (full), `.../gates.md` (:243-245), `.../gate.md` (:179-180), `.../copy-voice.md` (:173), `skills/gan-style-harness/SKILL.md` (full), `skills/council/SKILL.md`, `skills/orchestrate/references/call-map.md` (method notes B1/B6, dispatch table), `skills/orchestrate/references/dispatch-prompt.md` (prior-audit finding, not re-read in full); `manifests/context-packs/skill-triggers@1.json` (all 48 keys); grep over all 55 `commands/*.md` and all 48 trigger skills' `SKILL.md` files; grep over all `skills/*/references/` for subagent/dispatch; `build.sh` fix13-A (`:22197-22219`) + fix13e block (`:22690-22715`) + full `grok-4.7-high` census (39 lines); `fix33/fix33.py` (REPLACEMENTS AST count 35, D33-25..28 strings, scrub-tuple absence); `fix33/fix24.py` G-4 parenthetical grep; `fix33/SPEC.md` (D33-25..D33-35, §3), `fix33/MANIFEST.md:67`, `fix33/verify33.py` (§16n, §13), `fix33/audit111-report-B.md`, `fix33/fix-round-33d-report.md`, `fix33/build-log-run10.txt` (not re-litigated).

## Exact commands / results

```
# independent re-runs (real tree, explicit BASE)
python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc
  -> 586/586 checks pass, EXIT 0
python3 scan32-r4-test-fix33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc
  -> RESULT: ALL PASS (76 checks), EXIT 0
# r5 from probe dir with fix32.py + fix32-patch-log.md adjacent to the script
python3 scan32-r5-test-fix33.py <probe>/hackathon-ecc
  -> RESULT: ALL PASS (100 checks)
# (in-place r5 from fix33/ crashes FileNotFoundError: fix32.py — same as audit #111-B note)
# probe copy (full scratch-repo copy under fix33/audit112b-probe/repo/, deleted after)
python3 verify33.py <probe>/repo/hackathon-ecc        -> 586/586, EXIT 0 (clean)
# Probe A: delete probe skills/orch-change-feature/SKILL.md:47
  -> 584/586 (exactly 2 §16n B-B1 FAILs)
# Probe B: delete probe commands/feature-dev.md:5   -> 584/586, EXIT 1
  (exactly 2 §16n B-B3 FAILs; output /tmp/audit112b-probeB.txt)
cd scratch-repo && git rev-parse --short HEAD        -> dd106ade
git diff --stat HEAD | tail -1                        -> 47 files changed, 196 insertions(+), 126 deletions(-)
grep -rh "^model:" hackathon-ecc/agents/ | sort | uniq -c
  -> 41 model: cursor-grok-4.6-high-fast / 4 model: inherit
grep -rn "grok-4.7-high" hackathon-ecc/skills/orch-*/SKILL.md hackathon-ecc/commands/orch-*.md
  -> 0 matches
grep -c "grok-4.7-high" scratch-repo/build.sh        -> 39
grep "The design role runs on model" scratch-repo/build.sh scratch-repo/fix33/fix33.py (fix33.py path: fix33/fix33.py)
  -> 0 matches in both
grep -rn "MODELSEL_F33" hackathon-ecc/skills/design-taste-frontend/
  -> 0 matches
grep -c "MODELSEL_F33" scratch-repo/new-skills/design-taste-frontend/SKILL.md
  -> 0
python3 -c "import json; ..." skill-triggers@1.json  -> 48 trigger keys
md5sum fix33.py (canonical + scratch)                 -> cda0e5be0c9ed0030f73fddf07c527c0 (identical)
md5sum fix33-patch-log.md (canonical + scratch)       -> 8ae4664f7a64a1bf5ae6fd7cfa044ea0 (identical)
```

Nothing was edited or committed by this audit. The probe copy under `fix33/audit112b-probe/` was deleted after the probes; probe B output is at `/tmp/audit112b-probeB.txt` (ephemeral).
