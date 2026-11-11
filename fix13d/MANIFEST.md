# MANIFEST — Fix program #13d (coordinator): Audit #44 minors + dry-run #16 blocking/minor

Finding source: Audit #44 on the fix-#13c build — 0 blocking / 4 minor. Dry-run #16 (Campus Eats) on the same build — 2 blocking / 3 minor, NOT CLEAN. This round fixes all 7 consolidated items, then Audit #45 + dry-run #17 run on the same build.

## 0. Build record

- `build.sh` pre-fix13d: 22,361 lines, md5 `a1fade6ce94bf120bdcbc39b19726f0b`. Backup: `build.sh.before-fix13d` (same md5).
- `build.sh` post-fix13d: 22,450 lines (+89), md5 `0bcef5757b58c7ffaeb317943eaac03d`. `bash -n` OK.
- Rebuilds: build 1 exit 0; build 2 exit 0. **Manifest diff between build 1 and build 2 = 0 (reproducible).** Manifests: `fix13d/manifest-build1.txt`, `fix13d/manifest-build2.txt` (3,383 files each). Logs `fix13d/build1.log`, `fix13d/build2.log` are from the FINAL rebuild pair (after the S2c-tail correction below; the first pair's logs were overwritten by the re-run).
- Counts: **169 skills, 72 agents, 123 rules, 96 commands, 15 wired hook events (16 scripts incl. adapter.js) — UNCHANGED.** Size: **57 MB — UNCHANGED.** No new skills/agents/rules/commands. No pins touched. No zip/upload. Repo/bundle untouched.
- Scripts: `fix13d/fix13d.py` (staged-source edits, two-phase: all 25 anchors verified count==1 before any write; (f) anchors re-verified after) + `fix13d/fix13d-assemble.py` (build.sh block insertion, 14 preflight anchors count==1 against the post-fix13c built tree; idempotency guard; backup).

## 1. The 7 items — re-traced in the built pre-fix13d tree, all CONFIRMED

- **Item 1 CONFIRMED (BLOCKING)** — `skills/polish-pass/SKILL.md:22` harmony check (2) direction-application ("the screen visibly traces to the named direction… rather than looking like a default template… A screen that fails direction-application is a generic-template finding… it caps Persona fit per scoring.md"), `:96` non-negotiable 7, first-build final-polish paragraph; `reference/polish.md` Step 2:4 (generic-template diagnosis = FINDING), Step 2:7 (:24, same test), Step 3 (below-Level-6 diagnosis = FINDING); `reference/scoring.md:55` (generic look caps Persona-fit at 6 + FINDING routing). Sequencing gap CONFIRMED: orchestrate step 5b final polish sits between Verification (5a) and Deploy (5c) with no re-verify step; orch-build-mvp 6b → 7 commit → 8 deploy likewise.
- **Item 2 CONFIRMED (BLOCKING)** — `agents/ecc-gan-evaluator.md:31` ("DO penalize heavily for AI-slop aesthetics (generic gradients, stock layouts)"), `:94` ("AI-slop indicators"), `:116` ("4-5: Functional but clearly AI-generated, tutorial-quality").
- **Item 3 CONFIRMED (BLOCKING)** — three rubric writers, none carrying the :118 deferral: planner Process step 4 (`agents/ecc-gan-planner.md:107`), orch-build-mvp step 4 (`skills/orch-build-mvp/SKILL.md:38`), gan-design Setup step 3 (`commands/gan-design.md:19`). `commands/gan-design.md:36` asserts "the evaluator scores against `eval-rubric.md`, which carries that deferral" — FALSE on the gan-design path (its own Setup writes the rubric without the note) and on the other two paths.
- **Item 4 CONFIRMED (minor)** — `gates.md:§3` 6-axis pre-emit self-critique (:38 "anything under 3 triggers a revision first"; Specificity 3 = "fits the category", 5 = "could belong to no other product"), `review-finish.md:13` ("Seen before: the page, or a section, reads as a template…") + :15 polish variant ("whether anything still reads as machine-made"), `review-hero.md:11` ("Does anything read as a template…") + custom-run model test. Invoked as verdicts: Taste SKILL.md:314 ("Act on its first word (`ship` / `fix`); findings join the fix batch") and orchestrate step 6 (:195: 6-axis "any axis under 3 joins the fix list"; finish review "Act on its first word (`recapture` / `rebuild` / `fix` / `ship`); findings join the fix batch").
- **Item 5 CONFIRMED (minor)** — `agents/ecc-gan-planner.md:44`: "- **Inspiration**: [specific sites/apps to draw from]".
- **Item 6 CONFIRMED (minor)** — `agents/ecc-gan-evaluator.md:3`, `agents/ecc-gan-planner.md:3`, `agents/ecc-gan-generator.md:3`, `skills/gan-style-harness/SKILL.md:3` all say Claude Code only / no Cursor equivalent, yet the agents carry Cursor model pins (`composer-2.5[fast=false]`), `commands/gan-build.md` launches them "as a Cursor subagent", `rules/hackathon-mode.mdc:§5` says the skill "does not run in Cursor", while `orch-build-mvp:40` drives the GAN loop in Cursor.
- **Item 7 CONFIRMED (observation)** — `skills/app-scaffold/reference/best-practices.md:119`: `npm install -D supabase` unpinned while the deps above it are pinned (`@supabase/supabase-js@2.119.0`, `@supabase/ssr@0.12.7`).

## 2. Item-6 truth determination (from the files)

- The upstream skill's `claude -p` CLI invocation path (`gan-style-harness/SKILL.md:183-192`, `:30`; `scripts/gan-harness.sh`, whose own header says it shells out to `claude -p`/`claude mcp` and "will not run in a Cursor-only install with no `claude` CLI") does NOT run in Cursor and is never executed by this plugin.
- The GAN LOOP as implemented here DOES run in Cursor: `commands/gan-build.md` (Phases 1–2) + `commands/gan-design.md` launch the `ecc-gan-*` agents "as a Cursor subagent", and the agents carry Cursor model pins (`composer-2.5[fast=false]`). The skill contributes the harness design, prompts, and rubric (the planner writes `eval-rubric.md` from it).
- Therefore `orch-build-mvp:40` driving the GAN loop in Cursor is NOT an inconsistency — the stale frontmatter wording is. The wording was fixed (B4d/B5/B5b/B7 + S6); orch-build-mvp:40 is untouched on this item.

## 3. Changes — file:line IN THE BUILT PLUGIN (all verified by grep)

### Staged sources (fix13d.py)
- **polish-pass SKILL.md:22** — harmony check is consistency ONLY ("Harmony checks consistency ONLY: it does NOT judge whether a screen reads as a default template — that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop"); consistency-suggests-not-applied → candidate evidence for `browser-qa`; generic-template finding + Persona-fit cap exist ONLY on `browser-qa`'s verdict. **:24-ish diagnosis paragraph** — same routing + "re-verified by `browser-qa` before deploy". **First-build final polish paragraph** — same routing. **Non-negotiable 7** — "consistency only" + candidate evidence. "direction-application": **0** in the file.
- **polish.md Step 2:4 / Step 2:7 / Step 3 / Lenses preamble** — generic-template diagnosis = candidate evidence for `browser-qa`; FINDING exists only on its verdict; redesign re-verified before deploy. "direction-application": **0** in the file (see §3b for the tail correction).
- **scoring.md:55** — Persona-fit cap + FINDING route through `browser-qa`'s verdict ("a generic-template diagnosis exists ONLY when `browser-qa`'s verdict says so"). **3-tells rule** — tells stay findings; the overall-Score cap at 6 for a template look applies only on `browser-qa`'s verdict.
- **gates.md §3** — scoping note: the critique judges the planned page's IDEA (no screen exists pre-emit); Specificity is candidate evidence for `browser-qa`, never a verdict; the other five axes join the fix list as craft judgments.
- **hallmark-floor.md 6-axis section** — same scope, condensed.
- **review-hero.md** — first line (`ship`/`fix`) rests on craft questions only; template question + custom-run model test record candidate evidence for `browser-qa`, never drive the first word.
- **review-finish.md** — "Seen before" + polish-variant "machine-made" record candidate evidence; first word rests on gates/plain defects/copy/layout.
- **app-scaffold best-practices.md:119** — `npm install -D supabase@3.1.0       # optional: CLI pinned per-project (3.1.0)` (3.1.0 is the supply-chain pin; cf. deploy-fast:122, app-scaffold SKILL.md:61/:73).
- **hackathon-mode.mdc:38** — gan parenthetical now the precise truth (CLI path does not run in Cursor; loop runs in Cursor via `/gan-build` + `ecc-gan-*` agents; skill still cannot lead design).
- **orchestrate SKILL.md step 5b** — "Re-verify before deploy: if final polish routes a redesign … `browser-qa` re-runs the step-5 every-route visual loop on the redesigned screens BEFORE the 5c deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy." **Step 6** — 6-axis "EXCEPT Specificity, which is candidate evidence for `browser-qa`"; finish-review template observations route to `browser-qa` re-inspection in the step-5 loop before polish/deploy; only its verdict decides whether a fix is owed. **Step-5 visual loop (:193)** — "Candidate evidence in: if `.hallmark/hero-review.md` exists, its template observations are input to your verdict… Evidence never overrides your verdict — you make the call."
- **design-taste-frontend SKILL.md:314** — hero-review invocation: ship/fix acts on craft findings; template observations are candidate evidence recorded in `.hallmark/hero-review.md` for `browser-qa`'s visual loop.

### Build.sh block fix13d (LAST, just before STEP 5; STEP 5 at build.sh:22441)
- **orch-build-mvp step 4** — orchestrator-written `eval-rubric.md` must carry the scoping note. **6b** — re-verify before step-7 commit and step-8 deploy.
- **ecc-gan-planner Process step 4** — planner-written rubric must carry the scoping note. **:44** — "Inspiration" line replaced with "Direction source" (named direction generated through the package skills; never specific sites/apps; anti-derivative rule cited). Old "Inspiration" line: **0**.
- **ecc-gan-evaluator :31 / :94 / :116** — AI-slop language scoped to the rubric deferral ("as the rubric allows", code-level only, never screen distinctiveness). **Frontmatters** (planner/generator/evaluator :3) — "(Cursor subagent — launched by `/gan-build` [/ `/gan-design`]; the upstream `claude -p` path is Claude Code only and is never executed here.)" Old "(Claude Code only — no Cursor equivalent in this plugin)": **0** in all three agent files.
- **gan-design Setup step 3** — design-focused rubric must carry the scoping note. **:36 assertion now TRUE on all three rubric paths** (planner B3, orch-build-mvp B1, gan-design B6); :36 itself unchanged.
- **gan-style-harness :3** — frontmatter truth (CLI path Claude Code only; loop runs in Cursor via `/gan-build` + agents; skill contributes design/prompts/rubric, "never the CLI commands"). **"Via Claude Code (Manual)" section** — note that those commands are NOT executed in this plugin.
- **design-system Mode 3** — slop findings are candidate evidence for `browser-qa`, never a distinctiveness verdict ("Whether a named direction is recorded AND visibly applied … is judged ONLY by `browser-qa` in the visual loop").

### Correction found during verification (same round, before Audit #45)
- **S2c-tail:** my S2c staged anchor ended before the final sentence of Step 2:7, leaving "and do not pass direction-application on any screen." in the staged (and first-build) polish.md — a residue referencing a test that no longer exists. Fixed in the staged source (→ "and do not pass any screen on consistency against an unrecorded direction."), then rebuilt twice (exit 0, manifest diff 0). "direction-application": **0** in both polish files in the final build.

## 4. Single-executor sweep (built tree) — "exactly ONE executor" must hold tree-wide

Mechanism applied everywhere: a check that observes template-ness on a rendered screen records it as **candidate evidence** for `browser-qa` (screen + detail) in its output file/report; `browser-qa`'s visual loop is the ONLY verdict on the distinctiveness bar; a fix is owed only on its verdict.

- **Defers (fixed this round):** polish Harmony (consistency only + evidence); GAN evaluator + rubric rows (rubric deferral, fix13c + B3/B1/B6); Hallmark 6-axis Specificity + hero/finish template observations (evidence); design-system Mode 3 (evidence).
- **Checked, not a judge (file:line):**
  - Blind reviewer — `orchestrate/SKILL.md:187-189` + `references/dispatch-prompt.md:177-182`: checks only the recorded direction in the diff; "does NOT judge the built screens — it cannot see them"; screen distinctiveness judged ONLY by `browser-qa`.
  - sloplint — `orch-build-mvp` step 6 + `orchestrate` step 6: enforces numbered gates (objective code/render tells); "a sloplint app-scope pass does NOT prove distinctiveness".
  - `gate.mjs` (Taste finish gate, `design-taste-frontend/SKILL.md:291-296`, `:410`) — runs the numbered gates until `GATE: PASS`/`GATE: OPEN`; enforces gate FAILs, does not check the direction record, does not verdict the bar.
  - design-system Mode 2 — 10 dimensions (color consistency, typography, spacing, component consistency, responsive, dark mode, animation, a11y, density, polish; SKILL.md:37-52): none is template-ness. Mode 1 generates a system (not a judgment).
  - `ui-ux-pro-max` anti-generic bar citation (`orchestrate:193`) — the bar's DEFINITION is cited from ui-ux-pro-max; the executor named in the same sentence is `browser-qa`. Definition citation, not an executor.
  - `ui-ux-pro-max/scripts/core.py:698-700` (`_style_identity`) — BM25 search/ranking over style CSV rows (resolves a style identity from a query); operates on data rows, never sees screens.
  - `vibe-code-tells.md:36` — each tell is a code-level finding with a fix under its Lens; pattern evidence, not a verdict.
  - `impeccable-critique.md` — persona scoring; no template/generic verdict language (hits are "generic persona descriptions", "generic questions", scaffolding templates). Its Persona-fit scoring uses `scoring.md`, now routed through `browser-qa`.
  - Hallmark gates prose (§9 section rhythm, §38iii accented word) — design guidance / gate rules enforced by sloplint as static tells, not the bar verdict.
  - Photos/moments curation data (`photos.json`, `moments/*.json` "reads as a template") — photo-curation metadata about stock imagery, not screen verdicts.
- **Left as adjudicated (fix13c):** `frontend-slides/SKILL.md:26` (slide-deck style guideline, not a screen judge); `gan-style-harness/SKILL.md:269` results table (Anthropic's published results, descriptive); `commands/gan-design.md:39` generator prompt (generation instruction, not a judge).

## 5. Regression greps (built tree)

- Grok pin intact: `grok-4.7-high` ×4 in orchestrate SKILL.md; `grok-4.7[` bracket syntax: **0** tree-wide. Posture "more, not bolder": ×1 in orch-build-mvp, ×1 in orchestrate. "SOLE executor": orch-build-mvp step 4 + step 6 (×2). `gan-style-harness` :118 scoping note intact (×1). Old evaluator lines: "DO penalize heavily for AI-slop aesthetics (generic gradients, stock layouts)" (bare): **0**. Old "Claude Code only — it drives the `claude` CLI" (skill/mode): **0**. Counts/size unchanged (see §0). No new gates/waits/questions; §7 + deferred-six carve-out untouched; pins + SSML truth untouched; no fix11-stage.py re-run; no pip pinning pass.

## 6. Held back, with reasons

- No numeric distinctiveness score (per fix #13 brief; the bar is recorded-direction-AND-visibly-applied + not derivative, a finding on failure).
- No new skills/agents/rules/commands. No new gates/waits/questions. Deferred-six §3/§7 carve-out, auto-expansion/auto-approval, Grok pin + picker instruction, anti-derivative rule, "more, not bolder" posture, CBM phrasing, direction lenses/live-generate, frontend-slides untouched. No supply-chain pins or SSML truth touched. No fix11-stage.py re-run. No pip pinning pass. No bundle/repo touching.
- `scripts/gan-harness.sh` left as is: its own header already states the truth (Claude Code only, shells out to `claude -p`, will not run in a Cursor-only install); the plugin never executes it. Removing shipped-but-unused upstream infrastructure is out of scope.
- `gan-design.md:36` not reworded: it is now TRUE on every rubric-writing path (B1/B3/B6), so no correction is needed.

## 7. Next: Audit #45 + dry-run #17 (spawned in parallel after the build)
