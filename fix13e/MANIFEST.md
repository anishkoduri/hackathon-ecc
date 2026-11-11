# MANIFEST — Fix program #13e (coordinator): Audit #45 + dry-run #17, screen-verdict reframing

Finding source: Audit #45 on the fix-#13d build — 3 blocking / 3 minor. Dry-run #17 (Campus Eats) on the same build — 3 blocking / 8 minor, NOT CLEAN. Parent decision: reframe the rule as SCREEN VERDICTS — browser-qa is the sole executor of pass/fail verdicts on rendered screens; everything else is design guidance / candidate evidence / static checks, worded as such, never as a verdict. This round fixes all 11 consolidated items, then Audit #46 + dry-run #18 + a tree-wide single-executor sweep of SOURCE skills run on the same build.

## 0. Build record

- `build.sh` pre-fix13e: 22,450 lines, md5 `0bcef5757b58c7ffaeb317943eaac03d`. Backup: `build.sh.before-fix13e` (same md5).
- `build.sh` post-fix13e: 22,716 lines (+266), md5 `48735a8e4c2d8df570e552598cd47bcb`. `bash -n` OK.
- Rebuilds: build 1 exit 0; build 2 exit 0. **Manifest diff between build 1 and build 2 = 0 (reproducible).** Manifests: `fix13e/manifest-build1.txt`, `fix13e/manifest-build2.txt` (3,383 files each). Logs `fix13e/build1.log`, `fix13e/build2.log`.
- Counts: **169 skills, 72 agents, 123 rules, 96 commands, 15 wired hook events — UNCHANGED.** Size: **57 MB — UNCHANGED.** No new skills/agents/rules/commands. No pins touched. No zip/upload. Repo/bundle untouched.
- Scripts: `fix13e/fix13e.py` (staged-source edits, 41 subs, two-phase: all anchors verified count==1 before any write; (f) anchors re-verified after) + `fix13e/fix13e-assemble.py` (build.sh block insertion, 38 subs, 38 preflight anchors count==1 against the post-fix13d built tree; idempotency guard; backup). Worker specs: `fix13e/spec_A.md` (17), `spec_B.md` (17), `spec_C.md` (30), `spec_D.md` (16).

## 1. The 11 items — re-traced in the built pre-fix13e tree, all CONFIRMED

- **Item 1 CONFIRMED (BLOCKING)** — `skills/ui-ux-pro-max/SKILL.md:14` captivating bar ("if nothing is memorable, the surface fails… If no anchor can be named, the surface FAILS") + `:91` anti-generic bar (three enforced fail criteria). Coordinator spot-verified before delegating.
- **Item 2 CONFIRMED (BLOCKING)** — `skills/gan-style-harness/SKILL.md:118` note exists but `:121` (Design 1–3 "Generic, template-like, 'AI slop' aesthetics") + `:127` (Originality 1–3 "Default colors, stock layouts, no personality") carry NO deferral; only 7–8 rows do. Numeric gate (Design 0.3 + Originality 0.2 = 50%; PASS/FAIL 7.0). No rubric-validation step on any path. `commands/gan-design.md:36` assertion false on the gan-design path + stale/hand-written paths. Citation correction (worker B): `commands/gan-build.md` has only 104 lines, so the brief's `:112` is `agents/ecc-gan-evaluator.md:112`.
- **Item 3 CONFIRMED (BLOCKING)** — orchestrate 5b `:60` + orch-build-mvp 6b `:53` both say "within the existing visual-loop caps" (the loops already ran; caps consumable); 5c `:61` security-review checklist only; orch-build-mvp step 7 `:55` Gate 2 auto-approves; step 8 `:56` unconditional deploy. No re-verification check, no revert, no hold.
- **Item 4 CONFIRMED (minor)** — orchestrate `:195` + gates.md `:40` say "record… for browser-qa's visual loop" with no file/ledger/dispatch input; `.hallmark/hero-review.md` exists (Taste `:314`) but browser-qa never reads it (0 hits for `hero-review` / `candidate evidence` in `skills/browser-qa/SKILL.md`).
- **Item 5 CONFIRMED (minor)** — orch-build-mvp `:40` pins design role to `grok-4.7-high`; all three GAN agents `model: composer-2.5[fast=false]` (`:4` each). Built README 0 `grok` hits; picker note only in repo-root `README.md:17`.
- **Item 6 CONFIRMED (minor)** — `skills/design-system/SKILL.md:27` "Research 3 competitor sites for inspiration (via browser MCP)".
- **Item 7 CONFIRMED (minor)** — `skills/orch-add-feature/SKILL.md` (45 lines), `orch-fix-defect` (43), `orch-refine-code` (44): 0 hits for `design package|design-tokens|ui-ux-pro-max`. All three exist in the built tree (no staged source). Mirror: `orch-change-feature/SKILL.md:36` (skill-only; its command has 0 hits).
- **Item 8 CONFIRMED (minor)** — `skills/polish-pass/reference/polish.md:77` table header + `:79` row (Direction-application pass/fail); `:81–82` generic-template section with no verdict qualifier.
- **Item 9 CONFIRMED (minor)** — gates.md `:38` unscoped trigger sentence above `:40` scope note; hallmark-floor.md `:62–63` (citation correction: parent cited :64–65, which are the stamp line; scope note is :67); review-hero.md `:9` headline question; review-finish.md `:9` + `:15` ("in at most five findings — recorded as candidate evidence… not as findings of this review").
- **Item 10 CONFIRMED (minor)** — craft-floor.md `:109/:126/:130` absolute bans; vibe-code-tells.md `:3/:36`; sloplint.mjs `:2963` gate 38iii FAIL (tier reflex → REFLEX); gates 2/74/63/65 likewise FAIL/REFLEX; 38iii/2/74 NOT in APP_SKIP. Correction (worker A): gate 74 reports WARN, not FAIL (`check65Tailwind` :3188, `checkTailwind` :3834 call `report(74, 'WARN', …)`); reflex tier only converts FAIL→REFLEX. scoring.md `:43–59` (Level ladder, Level 2 = template at :47; `:59` caps overall Score at Level+1).
- **Item 11 CONFIRMED (minor)** — `skills/gan-style-harness/SKILL.md:30` ("Quick single-file fixes (use standard `claude -p`)") unscoped; runnable commands `:185/:188/:191/:194`; `scripts/gan-harness.sh:2` header. Truth per #13d: GAN loop runs in Cursor; only the upstream `claude -p` CLI path does not.

## 2. Decisions (coordinator + workers, with reasons)

- **Item 2 rows: REWRITE, not append-a-deferral** (worker B). The 1–3 rows ARE the screen verdict; a deferral next to a contradictory row leaves the rubric self-contradictory. All 8 Design/Originality rows rewritten to score direction-recorded + code-level trace only. Weights + 7.0 threshold unchanged.
- **Item 2 validation failure: ADD THE NOTE** (worker B). Refusing the dimension would make PASS unreachable (Design + Originality = 50% of the weighted score) and halt the loop. Prepend + record repair in feedback; score code-level only.
- **Item 2 missing-rubric-file case (coordinator): FALL BACK to the canonical skill rubric.** Worker B's spec 2i only warned. Decision: if `gan-harness/eval-rubric.md` does not exist, the evaluator scores against the Evaluation Rubric in the `gan-style-harness` skill (which carries the scoping note after 2a) and records the missing file in its feedback file. Implemented as coordinator adjustments to 2i (warn message) + 2k (fallback sentence). This is reuse of existing canonical content, not new generation.
- **Item 2 gan-design :36: REWORD to be true** (worker B), conditional on Setup step-3 validation + repair.
- **Item 2 fourth rubric writer (worker B): `scripts/gan-harness.sh:209-218`** planner prompt carries no deferral in its own text (inherits only indirectly via "read agents/ecc-gan-planner.md"). Fixed by 2h.
- **Item 3 fresh budget: up to 2 verdict rounds on the redesigned/affected screens only, at most 1 fix round per problem list** (worker C), separate from the consumed step-5/6 caps. Rationale: 2 rounds is the minimum for verdict → one fix → final verdict on a narrow set; 1 fix round keeps the post-polish loop from becoming a second full visual loop.
- **Item 3 HOLD, not REVERT** (worker C). No snapshot of the pre-redesign state is named anywhere, so a revert cannot be executed reliably; a hold is enforceable with the existing ledger / `BLOCKED` record and never ships unverified screens. Wired into orchestrate 5c + step 6 and orch-build-mvp steps 7/8: named re-verification check, `re-verification: BLOCKED` in `.hackathon/run-ledger.md` + final report, never a user question.
- **Item 4 destination: `.hallmark/candidate-evidence.md`** (worker C). New evidence-only, screen-scoped file; one line per observation (screen + what reads as a template + source). Not hero-review.md (hero-only, browser-qa never reads it) and not the run ledger (browser-qa never reads it). Producers append there; the visual loop lists it as a standing input; browser-qa reads it before every verdict. Routing does not depend on memory.
- **Item 4 seed template: NONE** (coordinator). The file is a per-project runtime file created on first append; all specs read it "if it exists". Adding a seed would need new copy behavior in build.sh.
- **Item 5 decision: (B)** (worker D). Direction comes from the design-lead (Grok) BEFORE the loop; GAN agents are executors under it. Pinning all three GAN agents to `grok-4.7-high` would misassign a design-role model to code implementation (generator) and Playwright testing/scoring (evaluator). Agent frontmatter pins stay `composer-2.5[fast=false]`. README picker note via post-STEP-4 patch (Prerequisites, after the Taste bullet).
- **Item 9 review-finish :9 copy sentence: CONFIRMED as a craft finding** (coordinator, worker D's call). "Name any head that would pass unchanged on a competitor's page" is a static copy-craft check (same family as Floor gate 19 copy tells / craft-floor bans), not a rendered-screen verdict. The screen-level template verdict remains browser-qa's.
- **C4-19 + 9e MERGED** (coordinator). C4-19's OLD anchor is a strict substring of 9e's OLD anchor (both review-finish.md:15); applied separately the second would fail. Merged spec carries both the observations wording and the `.hallmark/candidate-evidence.md` destination.
- **7a/7b/7c finding clause (coordinator):** "Verify … through `browser-qa`'s visual loop …: a finding, minor at least, when…" names browser-qa as the executor of the verification in the same sentence, matching the accepted orch-change-feature :36 precedent. Not reworded to the C5 literal form.

## 3. Changes — file:line IN THE BUILT PLUGIN (all verified by grep)

### Staged sources (fix13e.py, 41 subs)
- **ui-ux-pro-max** — none (no staged source; build.sh block).
- **polish.md** — 8A Step 6 template consistency-only (Direction-application column removed; verdict cited not judged); 8B generic-template section qualified to browser-qa's verdict only; 8C :24 bar wording "pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY"; C4-12/13/14/15 evidence destination (`.hallmark/candidate-evidence.md`).
- **craft-floor.md** — 10A-1 Bans intro, 10A-2 precedence, 10A-3 Floor heading: static/code-level checks.
- **vibe-code-tells.md** — 10B intro, 10C :36: static/code-level signals + findings.
- **sloplint.mjs** — 10D header (static checks; gate logic unchanged), 10E 38iii comment (no logic change). `bash -n`/`node --check` OK.
- **scoring.md** — 10F-1 Level ladder intro, 10F-2 ban cap, 10F-3 Level cap: internal scoring anchor; C4-16/17 evidence destination.
- **polish-pass SKILL.md** — 10b-1 :22 bar wording; C4-8/9/10/11 evidence destination.
- **orchestrate SKILL.md** — C3-1 5b fresh verdict run + budget; C3-3 5c deploy hold; C3-4 step 6 commit hold; C4-1 :193 visual-loop input (candidate-evidence.md standing input); C4-2 :195 Specificity destination; C4-3 :195 finish-review route + fresh budget; C5-1 :193 citation re-pointed to browser-qa's visual-loop bar; C5-2 :193 FAILS sentence attribution; C5-3 :195 app-screen paragraph attribution.
- **gates.md** — 9a :38 trigger sentence scoped by the :40 note; C4-4 :40 Specificity destination.
- **hallmark-floor.md** — 9b :62–63 trigger sentence scoped by the :67 Scope note.
- **review-hero.md** — 9c :9 headline question reframed as copy craft; C4-18 :11 evidence destination.
- **review-finish.md** — 9d :9 template tells are evidence, not findings (copy sentence unchanged per decision); 9e-merged :15 observations + destination.
- **design-taste-frontend SKILL.md** — C4-5 :314 template observations to candidate-evidence.md (hero-review.md keeps craft findings + settlements).

### Build.sh block fix13e (LAST, just before STEP 5; STEP 5 at build.sh:22707)
- **ui-ux-pro-max** — 1A captivating bar, 1B anti-generic bar (guidance/evidence, never a screen verdict); 1C :87 bans as static checks.
- **gan-style-harness** — 2a rubric rows rewritten; 2b key behaviors; 2c anti-pattern #1; 11a :30, 11b :179 heading, 11c commands scoped (verbatim, comment added), 11d (via gan-harness.sh).
- **ecc-gan-planner** — 2d Process step 4 validation; 5a description (records supplied direction); 5b :44 Direction source (supplied); 5c guideline 2 (record supplied tokens).
- **ecc-gan-evaluator** — 2k Step 1 validation (single enforcement point; missing-file fallback to the canonical skill rubric).
- **orch-build-mvp** — 2e step 4 validation; C3-2 6b fresh verdict run + budget; C3-5 step 7 commit hold; C3-6 step 8 deploy hold; C5-4 :40, C5-5 step 6 verdict attribution.
- **gan-build** — 2f Phase 2 validation; 2g Phase 1 --skip-planner note; 5d Phase 1 launch (direction from design-lead).
- **gan-design** — 2l :36 reworded true; 2m Setup step 3 validation; 5e :12 brief carries design-lead direction; 5f :39 generator inside the recorded direction.
- **gan-harness.sh** — 2h planner prompt deferral (fourth writer); 2i Phase 1 shell validation (prepend + log; missing file warns + evaluator fallback); 2j evaluator prompt 1a; 11d :2 header (loop runs in Cursor via /gan-build, script never executed). `bash -n` OK.
- **browser-qa** — C4-7 read step (candidate-evidence.md before every verdict).
- **design-system** — C4-6 Mode 3 evidence destination; 6a Mode 1 package-generated direction (0 "Research 3 competitor sites" left).
- **README.md** — 5g picker note (Prerequisites, after Taste bullet; post-STEP-4 patch).
- **orch-add-feature / orch-fix-defect / orch-refine-code skills** — 7a/7b/7c design-package rule (refine-code rule inserted as step 4, commit renumbered to 5).

## 4. Single-executor sweep (built tree)

- #13d sweep (carried): polish Harmony (consistency only + evidence); GAN evaluator + rubric rows (deferral); Hallmark 6-axis Specificity + hero/finish template observations (evidence); design-system Mode 3 (evidence); blind reviewer (recorded direction only); sloplint (numbered gates, static tells); gate.mjs (numbered gates); design-system Mode 2 (10 dimensions, none template-ness); ui-ux-pro-max `_style_identity` (BM25 ranking, never sees screens); vibe-code-tells :36 (code-level findings); impeccable-critique (persona scoring, no template verdict); Hallmark gates prose (design guidance / gate rules); photos/moments data (photo-curation metadata).
- #13e sweep: IN FLIGHT (sweep worker, report `fix13e/sweep13e-report.md`) — re-sweeps SOURCE skills incl. ui-ux-pro-max itself, design-system Mode 2, vibe-code-tells, impeccable-critique, Hallmark gates prose, photos/moments data, and everything #13d checked. Result to be recorded here on return.

## 5. Regression greps (built tree)

- Grok pin intact + extended: `grok-4.7-high` ×4 orchestrate, ×1 orch-build-mvp, ×1 each orch-add-feature / orch-fix-defect / orch-refine-code, ×2 planner, ×1 gan-build, ×1 gan-design, ×1 README. `grok-4.7[` bracket syntax: **0** tree-wide. Posture "more, not bolder": ×1 orch-build-mvp, ×1 orchestrate.
- "within the existing visual-loop caps": **0**. Old GAN rows ("Generic, template-like" / "Default colors, stock layouts, no personality"): **0**. Old "Research 3 competitor sites": **0**. Old "Enforced fail criterion" (ui-ux-pro-max): **0**. Old "in at most five findings — recorded as candidate evidence": **0**.
- `candidate-evidence.md` mentioned in 11 files tree-wide (orchestrate ×3, browser-qa, polish-pass SKILL.md ×4, polish.md ×4, scoring.md ×2, Taste, gates.md, review-hero, review-finish, design-system).
- `gan-harness.sh` `bash -n` OK (`warn()` exists at :59). `sloplint.mjs` `node --check` OK. Refine-code steps renumbered 1–5 correctly.
- Counts/size unchanged (see §0). No new gates/waits/questions; §7 + deferred-six carve-out untouched; pins + SSML truth untouched; no fix11-stage.py re-run; no pip pinning pass.

## 6. Held back, with reasons

- No numeric distinctiveness score (per fix #13 brief; the bar is recorded-direction-AND-visibly-applied + not derivative, a finding on failure).
- No new skills/agents/rules/commands. No new gates/waits/questions. Deferred-six §3/§7 carve-out, auto-expansion/auto-approval, Grok pin + picker instruction, anti-derivative rule, "more, not bolder" posture, CBM phrasing, direction lenses/live-generate, frontend-slides untouched. No supply-chain pins or SSML truth touched. No fix11-stage.py re-run. No pip pinning pass. No bundle/repo touching.
- No seed template for `.hallmark/candidate-evidence.md` (per-project runtime file, created on first append; all specs read it "if it exists").
- `scripts/gan-harness.sh` NOT deleted (upstream Claude Code invocation path; never executed by the Cursor loop; header now states both halves of the truth). `scripts/lib/llm-summary.js` `claude -p` spawn (guarded, falls back to mechanical extraction) + plankton / skill-comply / observer-loop Claude-Code-only paths: reported by worker B, out of this item's scope, no specs written.
- review-finish.md:9 copy sentence kept as a craft finding (see §2 decision).
- Worker C held back: no spec for orch-pipeline / orch-change-feature / orch-add-feature / orch-fix-defect / orch-refine-code verdict wording outside items 3/4 + the worker-A follow-up — if the audit finds the same unattached finding clauses there, that is separate scope (note: 7a/7b/7c DO add the finding clause to the three skills, attributed to browser-qa's visual loop in the same sentence per the orch-change-feature :36 precedent).

## 7. Next: Audit #46 + dry-run #18 + single-executor sweep (spawned in parallel after the build)
