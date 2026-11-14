# Audit #46 — hackathon-ecc post-fix13e build

Auditor: subagent (read-only; no plugin file edited, build.sh not run).
Build under test: `~/workspace/hackathon-plugin/hackathon-ecc/`, build.sh 22,716 lines.
Prior build (fix #13d): Audit #45: 3 blocking / 3 minor; dry-run #17: 3 blocking / 8 minor.

## Counts + size, verified

| Item | Expected | Found |
|---|---|---|
| Skills (`skills/*/SKILL.md`) | 169 | 169 |
| Agents (`agents/*.md`) | 72 | 72 |
| Rules (`rules/*.mdc`) | 123 | 123 |
| Commands | 96 | 96 |
| Hook events wired (`hooks/hooks.json`) | 15 | 15 |
| Hook scripts (incl. `adapter.js`) | 16 | 16 |
| Size | 57 MB | 57 MB (50,586,587 bytes) |
| build.sh lines | 22,716 | 22,716 |

No new skills, agents, rules, or commands. No new approval gates, wait points, or user questions in the first-build flow, one-prompt changes, or removal flows (§7 auto-approval preserved; the only sanctioned first-build user prompt remains the narration-key prompt, which never blocks). The deploy/commit HOLD is a safety hold only: orchestrate SKILL.md:61/:64 and orch-build-mvp SKILL.md:55/:56 each state it "never asks the user anything" and records `re-verification: BLOCKED` instead of deploying/committing.

## Fix #13e items — verified present in the built tree

1. **ui-ux-pro-max reframed** — SKILL.md:14 captivating bar "(design guidance, not a screen verdict)… Only `browser-qa`'s pass/fail verdict… decides"; :87 craft-floor bans "absolute as static/code-level checks… never a pass/fail verdict on a rendered screen"; :91 anti-generic bar "(design guidance, not a screen verdict)… Only `browser-qa`'s pass/fail verdict… decides".
2. **GAN rubric rewritten** — `skills/gan-style-harness/SKILL.md:118-130`: "Screen distinctiveness is NOT scored here… judged ONLY by `browser-qa`"; Design Quality / Originality rows score recorded direction + code-level trace only; key behaviors (:100-107) and anti-pattern #1 (:253) scoped to code-level direction-application. Rubric-validation step present on every path: planner `agents/ecc-gan-planner.md:107`, orch-build-mvp SKILL.md:39 (step 4), gan-build `commands/gan-build.md:23` (Phase 1 `--skip-planner` note) + `:47` (Phase 2), gan-harness.sh `:205-213` (planner prompt + Phase 1 shell check) + `:291` (evaluator prompt 1a), evaluator `agents/ecc-gan-evaluator.md:48` (Step 1), gan-design `commands/gan-design.md:19` (Setup 3) + `:36` (reworded true — conditional on Setup step-3 validation). Missing-rubric fallback present: evaluator `:48` ("If the rubric file does not exist, score against the Evaluation Rubric in the `gan-style-harness` skill…") and gan-harness.sh `:209-210`. `commands/gan-design.md:36` no longer asserts an unconditional deferral. Planner `agents/ecc-gan-planner.md:44` carries direction from the design-lead, no "Inspiration:" line (0 `Inspiration:` hits in gan files).
3. **Fresh verdict run + HOLD** — orchestrate SKILL.md:60 (5b) and orch-build-mvp SKILL.md:53 (6b): fresh budget "up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list… separate from the step-5/step-6 visual loop's consumed caps"; HOLD in orchestrate :61 (5c) + :64 (step 6) and orch-build-mvp :55 (step 7) + :56 (step 8). 0 hits for "within the existing visual-loop caps" — the old re-verify sentences are gone.
4. **`.hallmark/candidate-evidence.md` canonical** — named in orchestrate :193/:195, gates.md `:40`, Taste SKILL.md:314, design-system SKILL.md:56, polish-pass SKILL.md:22/:24/:85/:96 and polish.md :7/:20/:24/:35, review-hero.md:11, review-finish.md:15. browser-qa SKILL.md:68 reads it before every verdict.
5. **GAN decision B** — direction from design-lead (`grok-4.7-high`) BEFORE the loop: `commands/gan-build.md:24`, `commands/gan-design.md:12`, `agents/ecc-gan-planner.md:44`. All three GAN agents `model: composer-2.5[fast=false]`. Picker note in shipped README:68 (Prerequisites, after the Taste bullet).
6. **design-system Mode 1** — SKILL.md:27: "Generate the direction through the design package skills… never competitor sites and never a searched external reference".
7. **Design-package rule** — orch-add-feature SKILL.md:33, orch-fix-defect SKILL.md:36, orch-refine-code SKILL.md:35, mirroring orch-change-feature SKILL.md:36.
8. **polish Step 6 template consistency-only** — polish.md:81 "Direction-application is `browser-qa`'s verdict, cited not judged"; :83 generic-template section "only on `browser-qa`'s visual-loop verdict".
9. **Hallmark scope airtight** — gates.md:38/:40, hallmark-floor.md:62-63/:67, review-hero.md:9/:11/:16, review-finish.md:9/:13/:15.
10. **Code-level proxies qualified** — craft-floor bans via ui-ux-pro-max :87 + polish scoring.md:54; vibe-code-tells `skills/polish-pass/reference/patterns/vibe-code-tells.md:36` ("list each tell as a static/code-level finding… never a generic-template finding on its own"); sloplint.mjs header (:2) + 38iii comment (:2961), gate logic unchanged; scoring.md:43/:54/:55/:56/:59 (Level ladder and caps apply to polish's own Score, Persona-fit/template caps only on `browser-qa`'s verdict).
11. **claude -p residue scoped** — gan-style-harness SKILL.md:30 ("Claude Code only — … never `claude -p`"), :179 heading ("Via Claude Code (Manual — Claude Code only, never executed in this plugin)"), :185/:188/:191/:194 commands each commented "Claude Code only — never executed in this plugin; upstream documentation only"; gan-harness.sh:2 header. (Other `claude -p` hits live only in plankton-code-quality / skill-comply upstream docs, outside this item's scope.)

## Standing invariants — verified intact

- Grok 4.7 High pin: `grok-4.7-high` slug form only, **0** `grok-4.7[` bracket uses; picker instruction in orchestrate SKILL.md:57, orch-build-mvp SKILL.md:40, README:68, and the orch-*/gan files.
- Anti-derivative rule ("never based on a searched external reference") and "more, not bolder" posture present in ui-ux-pro-max SKILL.md:87/:91 and all four orch-* design-package rules.
- Deferred-six §3/§7 carve-out intact (`rules/hackathon-mode.mdc:20-22`, `:58`); auto-expansion/auto-approval intact (orchestrate SKILL.md:55/:57, hackathon-mode.mdc:12).
- CBM phrasing: v0.12.1 pins present (`skills/codebase-memory/SKILL.md:51/:70`); README:29 (not bundled, user installs once); OpenMontage opt-in under /demo (`commands/demo.md:22-23`, `skills/pitch-deck-video/SKILL.md:469`).
- Direction lenses / live-generate still out (`skills/polish-pass/reference/impeccable-critique.md:165`, `skills/polish-pass/SKILL.md:109/:113`); frontend-slides on-demand (no auto-run wiring found; deck built only on request).
- Supply-chain pins: create-next-app@16.4.6, @angular/cli@22.2.6, playwright@1.65.0, remotion@4.0.542, ecc-universal@2.2.3, ccg-workflow@3.7.4, vercel@65.14.0, @railway/cli@5.71.0, supabase@3.1.0, supabase-js@2.119.0, ssr@0.12.7, impeccable@4.8.0, puppeteer-core@25.17.0, Hallmark SHA 7e213cb6feb4ef82733bd66a0600b2e54ca0994c, shadcn@4.23.0 (in `skills/ui-ux-pro-max/data/stacks/shadcn.csv`), nuxt@4.0.3 (in `skills/ui-ux-pro-max/data/stacks/nuxt-ui.csv`), and all 6 clone SHAs in build.sh (`ECC_PIN`, `UIPRO_PIN`, `MARKETPLACE_PIN`, `CHWEZI_PIN`, `FLECTO_PIN`, `AGENTSKILLS_PIN`).
- SSML truth intact (`skills/pitch-deck-video/SKILL.md:335-352`, `:539-541`): v2 family only, ≤3s per break; v3/v4 unsupported; turbo v2.5 deprecated, never select.
- No fix11-stage.py re-run residue (no `fix11-stage` reference in build.sh); critique.md fix-#12 edits intact (`skills/polish-pass/reference/impeccable-critique.md:222` "warmer / more playful / more distinctive", 0 "warmer/bolder" hits tree-wide); no pip pinning changes (single `pip install` hit in build.sh is a comment, :21881); no bundle/repo touching (build.sh only clones upstream repos to pinned SHAs).

## BLOCKING

- B1 — `skills/design-taste-frontend/SKILL.md:53`: "**Captivating hero — the bar:** the hero's first view must make the product's most surprising moment visible immediately. Test: a first-time visitor can name, in 5 seconds and without scrolling, the one surprising thing this product does; if they cannot, the hero fails even if every other check passes." — A pass/fail verdict on a rendered screen (the hero's first view), stated as Taste's own bar with no "(design guidance, not a screen verdict)" qualification and no deferral to `browser-qa`. This is a second judge of screen distinctiveness/memorability, the same class fix #13e item 1 reworded in ui-ux-pro-max :14/:91; orchestrate :193 folds "design-taste-frontend's captivating-hero bar" into the bar `browser-qa` executes, but Taste :53 still lets the building skill fail the hero itself.

## MINOR

- M1 — `agents/ecc-gan-evaluator.md` Step 3A: "Does it feel like a real product or a tutorial project?" — The first-impression prompt still invites a screen-level tutorial-product judgment that feeds the 1–10 score, at odds with the "code-level trace only" scoping (Step 3C and the Step 4 calibration are scoped, but 3A is not).
- M2 — Two separately-described fresh verdict budgets with no stacking rule: orchestrate SKILL.md:60 (5b polish-routed redesign, "up to 2 verdict rounds") and orchestrate SKILL.md:195 (step-6 finish-review template observations, "up to 2 verdict rounds on the affected screens only… a fresh budget, not the step-5 loop's consumed caps"). If both triggers fire in one run, up to 4 fresh verdict rounds could run; nothing states whether they share one budget or stack. (Neither contradicts the step-5 caps; the ambiguity is only between the two fresh budgets.)

## Held back / not checked

- Live smoke test: whether the `grok-4.7-high` file-level pin actually holds in Cursor is decided by `LIVE_SMOKE_TEST.md` §14, not by a read-only audit.
- The separate single-executor sweep worker's findings (independent check; this report is my own sweep only).
- The tree-wide second-judge sweep was grep-based over "distinctiveness", "reads as a default template", "fails the bar / fails even if", and the known producer files — not a line-by-line read of all 169 skills.
- CBM "standalone" wording: the substance is verified (skill present, v0.12.1 pins, README:29 not-bundled/user-installs-once, OpenMontage opt-in under /demo), but the literal word "standalone" was not located in `skills/codebase-memory/SKILL.md`; not raised as a finding.

## Verdict

AUDIT #46: 1 BLOCKING / 2 MINOR
