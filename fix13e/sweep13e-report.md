# Sweep 13e — Single-executor sweep (fix round #13e)

**Build under test:** `~/workspace/hackathon-plugin/hackathon-ecc/` (post-fix13e build).
**Rule under test:** `browser-qa` is the SOLE executor of pass/fail VERDICTS on rendered screens (generic / template / derivative). Everything else is design guidance, candidate evidence, or a static/code-level check — worded as such, never as a pass/fail verdict on a screen.
**Method:** read SOURCE skills (SKILL.md + references + scripts), not citations; grepped for `verdict / pass/fail / FAIL / finding / judge / score / penalize / template / generic / slop / "reads as"`. Read-only; no plugin file edited, `build.sh` not run.

**Verdict: SWEEP: 12 BLOCKING / 7 MINOR**

## Key observation

The sole-executor claim is asserted but not true tree-wide. `browser-qa/SKILL.md:68` says "No other step judges screen distinctiveness", but the Hallmark render tier (`sloplint-render.mjs`) and the Step-7 judged gates (`gates.md` §5) both judge rendered screens for template/generic traits and compel fixes — and they do so on landing pages AND app screens: the static tier's `APP_SKIP` (`sloplint.mjs:798-799`) skips template gates 8, 9, 81, 82, 83, 85 in app scope, but the render tier's pushes for gates 80–83, 85 carry no scope guard. Enforcement lines: `design-taste-frontend/SKILL.md:312` ("Fix every `FAIL`; fix or waive every `REFLEX`"), `orchestrate/SKILL.md:195` (step 6, same), `hallmark-floor.md:54-55`, `gates.md:247` ("Nothing ships with an open `FAIL` or an open `REFLEX`").

## BLOCKING list (second judges)

**B1 — `skills/design-taste-frontend/SKILL.md:53`**
> "**Captivating hero — the bar:** the hero's first view must make the product's most surprising moment visible immediately. Test: a first-time visitor can name, in 5 seconds and without scrolling, the one surprising thing this product does; if they cannot, the hero fails even if every other check passes."
Why: states the rendered hero FAILS — an unqualified pass/fail verdict on a rendered screen, with no deferral to `browser-qa`. (Contrast `ui-ux-pro-max/SKILL.md:14/:91`, which were reworded with an explicit deferral; this one was not.)

**B2 — `skills/design-taste-frontend/references/hallmark/references/gates.md:95` + `:191` (gate 8, class J)**
> "| 8 | Reflex | J | The AI template (hero, three features, call to action, footer), or the same shape as one of the last three logged builds |" / "**8 and 32, repetition.** … The same composition twice in a row on one page is the template; …"
Why: a judged-at-Step-7 clause that declares the built page IS "the template". Findings join the fix list; a Reflex finding must be fixed or waived. (Gate 32 in the same clause is Ledger/NOTE-only and is NOT flagged.)

**B3 — `gates.md:193` (gate 9, class J)**
> "**9, section rhythm.** … A page that climbs the same rung at every seam reads as a template; …"
Why: judged clause stating the rendered page reads as a template; joins the Step-7 fix list as a Reflex finding.

**B4 — `gates.md:233` (gates 80–82, class R/J)**
> "**80 to 82, pictures.** … Each reads as generated at a glance."
Why: judged clause stating the rendered page reads as generated; enforced by the render tier as REFLEX (B7–B9) and by the Step-7 walk.

**B5 — `gates.md:117` + `:235` (gate 83, class R)**
> "| 83 | Reflex | R | The photo wall: below the hero, photographs cover more than about a third of the page at 1440 …, so it reads as a stock gallery. …" / "**83, the photo wall.** … reads as a stock gallery, …"
Why: the rendered page is judged to read as a stock gallery; enforced by the render tier as REFLEX (B10).

**B6 — `gates.md:119` + `:239` (gate 85, class R)**
> "| 85 | Reflex | R | The stock close: …" / "**85 and the stock anatomy.** … could this exact sequence of sections sit under a different business's name? If it could, the page has no anatomy of its own yet."
Why: judged clause stating the rendered page's section sequence is stock/template anatomy; enforced by the render tier as REFLEX (B11).

**B7 — `skills/design-taste-frontend/references/hallmark/scripts/sloplint-render.mjs:859` (gate 80, REFLEX)**
> "if (drawn.length) push(80, 'REFLEX', `drawn illustration: ${drawn.slice(0, 3).join('; ')}`, …)"
Why: the render tier (Puppeteer, rendered page) issues a REFLEX grade on a rendered screen for a generated tell; `SKILL.md:312` / `gates.md:247` compel fix-or-waive and block shipping. No scope guard (runs in app scope too).

**B8 — `sloplint-render.mjs:877` (gate 81, REFLEX)**
> "if (empty.length) push(81, 'REFLEX', `${empty.length} empty picture${…}: …`, …)"
Why: same as B7 — render-tier REFLEX on a rendered screen for the empty-picture (template) tell.

**B9 — `sloplint-render.mjs:903` (gate 82, REFLEX)**
> "if (marks.length) push(82, 'REFLEX', `counting device: …`, …)"
Why: same as B7 — render-tier REFLEX on a rendered screen for the counting-device (generated) tell.

**B10 — `sloplint-render.mjs:916` (gate 83, REFLEX)**
> "if (share > (photoShape ? 0.45 : 0.36) && n >= 3) push(83, 'REFLEX', `photographs cover ${…}% of the page below the hero …`, …)"
Why: same as B7 — render-tier REFLEX on a rendered screen for the photo-wall / "reads as a stock gallery" tell.

**B11 — `sloplint-render.mjs:925` (gate 85, REFLEX)**
> "if (hit) push(85, 'REFLEX', `the page closes on an email sign-up${…}`, …)"
Why: same as B7 — render-tier REFLEX on a rendered screen for the stock-close (template anatomy) tell.

**B12 — `skills/polish-pass/reference/impeccable-critique.md:140` (+ `:56`, `:62`)**
> "#### Design Specificity Verdict" / "**Start here.** Does the result feel authored for this product, or category-interchangeable?" / "Return: design-specificity verdict, heuristic scores, …"
Why: the Impeccable critique playbook returns a literal "design-specificity verdict" judging whether the rendered design is category-interchangeable (= generic). It runs from `polish.md:19` whenever any Dimension scores below 6, and its Priority fixes fold into the Lens plan — so the verdict compels fixes. Not `browser-qa`, not candidate evidence.

## MINOR list (wording still reads as a verdict)

**M1 — `skills/design-taste-frontend/SKILL.md:283` + `references/layout-v4.md:296`**
> "Every `check.mjs` finding fails the page (no `--no-stress`)."
Reword: "Every `check.mjs` finding is a layout defect to fix; only `browser-qa` renders a pass/fail verdict on the page." (check.mjs measures rendered layout — correctness, not distinctiveness — so MINOR, not BLOCKING.)

**M2 — `skills/design-taste-frontend/references/layout-v4.md:182`**
> "A hero fails with a picture out to one viewport edge, a hero taller than the screen, the visual above the text on a phone, words over the busy part of a picture, a second float card, a slogan, a caption under the picture."
Reword: "A hero breaks the composition with a picture out to one viewport edge, …" (layout guidance, not a fail verdict.)

**M3 — `skills/design-taste-frontend/references/hallmark/scripts/sloplint-render.mjs:1-10` (missing header) + `:680` (gate 23 FAIL) + `references/gates.md:199`**
> (no scope note in the file, unlike `sloplint.mjs:2`) / "push(23, 'FAIL', `accent paints ~${pct.toFixed(1)}% of the 1280x800 viewport (> ${failAt}%)`, …)" / "**23, footprint by eye.** … undeclared sprawl still fails."
Reword: add a `sloplint.mjs:2`-style header scoping render-tier grades as rendered-measurement checks for craft/correctness, and reword the gate-23 clause to "undeclared sprawl is recorded as a craft finding". (Gate 23 is accent footprint — craft, not template — so MINOR; the template gates in the same file are BLOCKING B7–B11.)

**M4 — `skills/polish-pass/SKILL.md:24` + `reference/polish.md:20`**
> "If the diagnosis shows the look itself is the problem — the UI is a generic template, …" / "A generic-template diagnosis (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, …"
Reword: "If the evidence suggests the look itself may be the problem — the UI may read as a generic template — append it as candidate evidence …" (the routing is correct; the word "diagnosis" states the UI IS a generic template.)

**M5 — `agents/ecc-gan-generator.md:107`**
> "The Evaluator will specifically penalize these patterns. **Avoid them:**" (followed by generic gradients, stock hero sections, generic card grids, "AI-generated" decorative SVG patterns)
Reword: "The rubric scores code-level application of the recorded direction only; avoid these patterns because they show the direction was not applied in code." (The evaluator's own file, `ecc-gan-evaluator.md:31/:95`, carries the code-level qualifier; the generator's line drops it and attributes a generic-pattern penalty to the evaluator.)

**M6 — `skills/design-taste-frontend/references/hallmark/references/redesign.md:40`**
> "Look at the screenshots before you weigh the findings, so the linter does not write the verdict, then give the read in four lines: what the page is for …; what reads as generated (the worst tells, by gate); what is broken."
Reword: "…; what may read as generated (candidate evidence for `browser-qa`: screen + tell); what is broken." (The audit's read states what reads as generated on the rendered page.)

**M7 — `skills/design-taste-frontend/references/hallmark/references/gates.md:189` (gate 6b, class J)**
> "**6b, the hero shape.** A hero built around one centred object is a composition; four things stacked on the centre line is a default."
Reword: "…; four things stacked on the centre line is the default composition to avoid — prefer at most two centred elements with one breaking alignment." (Composition guidance worded as "is a default".)

## Checked list (item by item)

### ui-ux-pro-max
- `skills/ui-ux-pro-max/SKILL.md:14` — OK — captivating bar explicitly "design guidance, not a screen verdict"; defers to `browser-qa`.
- `skills/ui-ux-pro-max/SKILL.md:87` — OK — craft-floor bans are "absolute as static/code-level checks … never a pass/fail verdict on a rendered screen".
- `skills/ui-ux-pro-max/SKILL.md:91` — OK — anti-generic bar is candidate evidence; "Only `browser-qa`'s pass/fail verdict … decides".
- `skills/ui-ux-pro-max/SKILL.md:137` — OK — routing note; design-system 10-dimension score is a consistency audit, not a screen verdict.
- `skills/ui-ux-pro-max/references/` — OK — no verdict hits (only form-submission failure wording).
- `skills/ui-ux-pro-max/data/*.csv` headers — OK — no verdict language in headers; rows are search data, none states a screen verdict.

### design-taste-frontend
- `skills/design-taste-frontend/SKILL.md:53` — BLOCKING (B1).
- `skills/design-taste-frontend/SKILL.md:227` — OK — "the pairing fails `hero-lines`" is a checker id (layout check), not a distinctiveness verdict.
- `skills/design-taste-frontend/SKILL.md:283` — MINOR (M1).
- `skills/design-taste-frontend/SKILL.md:295` — OK — GATE: PASS/OPEN loop aggregates layout/copy/perf correctness checks, not distinctiveness.
- `skills/design-taste-frontend/SKILL.md:312` — OK as an instruction line; it is the enforcement point for B7–B11 (cited there, not a separate finding).
- `skills/design-taste-frontend/SKILL.md:314` — OK — hero review: template observations are candidate evidence, "never fix-batch verdicts".
- `skills/design-taste-frontend/SKILL.md:379-387` — OK — checklist; "Your eyes … reads as a professional company site" is guidance, no verdict.
- `references/gates.md:14` — OK — Ledger (gate 32) "Reports at `NOTE`, never counts toward the verdict".
- `references/gates.md:18` — OK — grade taxonomy; the template gates that use it are flagged separately (B2–B6).
- `references/gates.md:38/:40` — OK — pre-emit critique: Specificity is candidate evidence, "never a verdict on its own".
- `references/gates.md:95` — BLOCKING (B2, with :191).
- `references/gates.md:96` (gate 9 table row) — OK — the row states the tell only; the template verdict is the judged clause :193 (B3).
- `references/gates.md:114-117` (gates 80–83 rows) — BLOCKING (B4/B5, with judged clauses :233/:235).
- `references/gates.md:119` (gate 85 row) — BLOCKING (B6, with judged clause :239).
- `references/gates.md:189` — MINOR (M7).
- `references/gates.md:191` — BLOCKING (B2; gate 32 half is OK per :14).
- `references/gates.md:193` — BLOCKING (B3).
- `references/gates.md:199` — MINOR (M3).
- `references/gates.md:203, :217, :219, :221, :223, :227` (38iii, 63, 65, 66, 67, 69) — OK — element-level machine-made pattern bans (one word, punctuation, a look, a label style, repetition), same class as the craft-floor slop tells; no whole-screen template verdict.
- `references/gates.md:205, :207, :209, :211, :213, :215, :225, :229, :231, :237` (44, 46b, 47c, 54, 58, 62, 68, 70, 77–79, 84) — OK — craft/correctness/honesty judgments, not template verdicts.
- `references/gates.md:247` — OK as a rule line; enforcement point for B7–B11 (cited there).
- `references/hallmark-floor.md:54-55, :62-67` — OK — sloplint enforcement line; Specificity scoped to candidate evidence.
- `references/review-hero.md:5, :11, :16` — OK — template observations → `.hallmark/candidate-evidence.md`, "never drive" the first word.
- `references/review-finish.md:5, :9, :13, :15, :17` — OK — same routing; "Seen before" is candidate evidence, "never a finding of this review".
- `references/redesign.md:40` — MINOR (M6).
- `references/redesign.md:42, :56, :66, :69, :73` — OK — audit reports findings by tier; :69 ("Gate 8 judges the composition") is supporting evidence for B2.
- `references/hallmark/scripts/sloplint.mjs:2` — OK — header qualifies FAIL/REFLEX/WARN as "static-check grades, not pass/fail verdicts on rendered screens".
- `references/hallmark/scripts/sloplint.mjs:798-799` — OK — APP_SKIP skips template gates 8, 9, 81, 82, 83, 85 in app scope (static tier).
- `references/hallmark/scripts/sloplint-render.mjs:859, :877, :903, :916, :925` — BLOCKING (B7–B11).
- `references/hallmark/scripts/sloplint-render.mjs:680` — MINOR (M3).
- `references/hallmark/scripts/sloplint-render.mjs` other pushes (26a, 34, 40, 41, 44b, 44d, 58, 62, 71–79) — OK — rendered correctness/craft measurements (contrast, scroll, fold, word budget), not template/generic verdicts.
- `references/layout-v4.md:182` — MINOR (M2).
- `references/layout-v4.md:296` — MINOR (M1).
- `references/moments.md:30` — OK — "reads as a template trick" describes a technique to avoid (guidance).
- `references/cards.md:79` — OK — "Never a generic dashboard" is build guidance.
- `references/copy.md:25, :32`, `copy-registers.md`, `copy-tells.md`, `copy-voice.md`, `references/gate.md` — OK — copy-lint is a static check ("runs it on the page as a static check"); gate.mjs/check.mjs FAILs are correctness checks.
- `scripts/gate.mjs`, `scripts/theme.mjs`, `scripts/consistency.mjs` — OK — no verdict/template/distinctiveness language in comments.
- `assets/photos/photos.json:338` — OK — "reads as a template: c142" is a photo-library rejection note (curation metadata), not a screen verdict.
- `assets/moments/index.json:743`, `assets/moments/window-parallax/meta.json:12` — OK — retired moment note ("reads as a template trick"), design guidance.
- `references/hallmark/references/themes/*.md` — OK — "not a … template" lines are theme-identity descriptions, not verdicts on a built screen.

### polish-pass
- `skills/polish-pass/SKILL.md:22` — OK — harmony rule: consistency ONLY, per-screen pass/fail on consistency; template finding exists only on `browser-qa`'s verdict.
- `skills/polish-pass/SKILL.md:24` — MINOR (M4).
- `skills/polish-pass/SKILL.md:33, :85` — OK — generic-template finding only on `browser-qa`'s verdict; redesign routed only then.
- `skills/polish-pass/SKILL.md:89, :92, :93, :96` — OK — detector findings are "evidence to verify, not verdicts"; harmony never verdicts distinctiveness.
- `reference/polish.md:7, :18, :19` — OK — diagnosis appended as candidate evidence; critique playbook triggered on Dimension < 6 (see B12 for the playbook itself).
- `reference/polish.md:20` — MINOR (M4).
- `reference/polish.md:24` — OK — harmony consistency-only, defers to `browser-qa`.
- `reference/polish.md:31` — OK — design-system finding routed, not a verdict.
- `reference/polish.md:35` — OK — Level-6 (template) baseline appended as candidate evidence; finding only on `browser-qa` verdict.
- `reference/polish.md:56` — OK — independent re-score gate is a quality score (Overall < 8 → fix Priority fixes); the template cap applies only on `browser-qa`'s verdict.
- `reference/polish.md:79-84` — OK — report template: direction-application "cited not judged"; generic-template findings only on `browser-qa`'s verdict.
- `reference/scoring.md:43, :47, :54-59` — OK — Level placement is "an internal scoring anchor … not a pass/fail verdict"; Persona-fit/template caps apply only on `browser-qa`'s verdict.
- `reference/craft-floor.md:5, :111, :126-144` — OK — bans are static/code-level checks and candidate evidence, "never a pass/fail verdict on a rendered screen".
- `reference/patterns/vibe-code-tells.md:3, :36` — OK — tells are "static/code-level signal and candidate evidence … not a pass/fail verdict".
- `reference/impeccable-critique.md:56, :62, :140` — BLOCKING (B12).
- `reference/impeccable-critique.md:222` — OK — reworded in fix #13c ("warmer / more playful / more distinctive"); not re-flagged.
- `reference/impeccable-critique.md:115-140` (heuristics scoring) — OK — usability scoring, not a distinctiveness verdict.
- `reference/impeccable-craft-floor.md:48` — OK — "the closest installed font is a failure, not a fallback" is a static font-choice rule.
- `reference/impeccable-detector-rules.json` — OK — 62 rule descriptions are static-detection patterns (incl. rule [20] "the universal AI feature-card template"); findings are evidence per SKILL.md:93.

### gan-style-harness
- `skills/gan-style-harness/SKILL.md:101-109` — OK — Design Quality / Originality score the recorded direction and its code-level application only.
- `skills/gan-style-harness/SKILL.md:118` — OK — rubric scope note: "Screen distinctiveness is NOT scored here … judged ONLY by `browser-qa`".
- `skills/gan-style-harness/SKILL.md:147, :234` — OK — weighted score / 7.0 pass threshold is the harness quality bar on rubric criteria, distinctiveness excluded.
- `skills/gan-style-harness/SKILL.md:255` — OK — "add explicit penalties for common AI patterns (code-level direction-application failures only — never screen distinctiveness …)".
- `skills/gan-style-harness/SKILL.md:277` — OK — results table ("Generic AI slop" vs "Distinctive, polished") is a marketing comparison, not a verdict on a built screen.
- `skills/gan-style-harness/SKILL.md:181-198` — OK — `claude -p` path documented only, never executed here.
- `agents/ecc-gan-planner.md:44` — OK — direction source is the design-lead (Grok `grok-4.7-high`) in `docs/design-tokens.md`, "copied here, not generated"; the old "Inspiration: [specific sites/apps to draw from]" line is gone.
- `agents/ecc-gan-planner.md:98` — OK — anti-AI-slop directives are build guidance.
- `agents/ecc-gan-planner.md:107` — OK — rubric validation requires the distinctiveness deferral on all paths.
- `agents/ecc-gan-generator.md:107` — MINOR (M5).
- `agents/ecc-gan-generator.md:21, :28, :49, :72, :109-120, :131, :138` — OK — build guidance ("Avoid them" list); "Don't self-evaluate … The Evaluator judges."
- `agents/ecc-gan-evaluator.md:21, :25, :31, :43-48, :83, :95, :111-117, :124-154, :183, :187, :232` — OK — scores against the rubric with distinctiveness explicitly excluded; `:154` "Verdict: PASS / FAIL (threshold: 7.0)" is the harness quality-bar verdict on rubric criteria, not a screen-distinctiveness verdict.
- `commands/gan-build.md:23, :47, :49, :55-60, :83` — OK — score loop; `--skip-planner` path validated in Phase 2 before any scoring.
- `commands/gan-design.md:19, :21, :34-39` — OK — design rubric carries the deferral; "would this win a design award?" prompt is scoped by it.
- `scripts/gan-harness.sh:80-90, :95-98, :205-213, :226-228` — OK — score extraction + rubric validation that prepends the scoping note if missing.

### orchestrate / orch-* / dispatch
- `skills/orchestrate/SKILL.md:57, :59-61, :64` — OK — design package in every UI brief; fresh `browser-qa` verdict budget (up to 2 rounds, at most 1 fix round) + deploy/commit HOLD on unverified redesigns.
- `skills/orchestrate/SKILL.md:189` — OK — blind reviewer checks only the recorded direction; "Screen-level distinctiveness is judged ONLY by `browser-qa`".
- `skills/orchestrate/SKILL.md:193` — OK — step-5 visual loop: `browser-qa` is "the SOLE executor of this bar"; candidate evidence in via `.hallmark/candidate-evidence.md`.
- `skills/orchestrate/SKILL.md:195` — OK as a step; its "Fix every `FAIL`" line is the enforcement point for B7–B11 (cited there). (Note: its step-6 finish-review routing of template observations to candidate evidence is correct; the judged gates it walks are B2–B6.)
- `skills/orchestrate/SKILL.md:197, :285-287` — OK — `browser-qa` detects, `systematic-debugging` diagnoses; report records the Verify distinctiveness outcome.
- `skills/orchestrate/references/dispatch-prompt.md:162-190` — OK — blind reviewer: "Do NOT judge the built screens … Screen-level distinctiveness is judged by `browser-qa` … No approve/reject verdict."
- `skills/orch-build-mvp/SKILL.md:39, :40, :49, :53, :55, :56` — OK — design package on every UI slice; sole executor; fresh budget + HOLDs before commit/deploy.
- `skills/orch-pipeline/SKILL.md:72, :120` — OK — reviewer checks the direction is RECORDED only; distinctiveness in `browser-qa`'s visual loop.
- `skills/orch-change-feature/SKILL.md:36`, `skills/orch-add-feature/SKILL.md:33`, `skills/orch-fix-defect/SKILL.md:36`, `skills/orch-refine-code/SKILL.md:35` — OK — design-package rule present in all four; verification "through `browser-qa`'s visual loop … (the single executor of the bar)".
- `commands/orch-*.md` (add-feature, fix-defect, refine-code, change-feature, build-mvp, orchestrate) — OK — thin wrappers invoking the skills; no verdict language of their own.

### design-system / browser-qa / other design skills
- `skills/design-system/SKILL.md:27` — OK — Mode 1 generates direction through the package skills, "never competitor sites and never a searched external reference".
- `skills/design-system/SKILL.md:37-52` — OK — Mode 2 scores 10 consistency dimensions; no template verdict.
- `skills/design-system/SKILL.md:54-56, :64-78` — OK — Mode 3: "**Scope — pattern evidence, not a distinctiveness verdict** … candidate evidence for `browser-qa`, never a verdict".
- `skills/browser-qa/SKILL.md:68` — OK — the designated sole executor (its "No other step judges screen distinctiveness" assertion is contradicted by B2–B11 — see Key observation).
- `skills/browser-qa/SKILL.md:3, :20-22, :41, :89, :105-106` — OK — SHIP / DO-NOT-SHIP is `browser-qa`'s own verdict; "caller caps rounds (max 3…)" is the step-5 loop cap, consistent with the fresh-budget separation in orchestrate:60.
- `skills/less-flat-ui/SKILL.md:118, :171, :392, :413` — OK — texture guidance; "text will fail contrast" is an accessibility static check.
- `skills/make-interfaces-feel-better/SKILL.md:17` — OK — "feels … generic" is a user complaint that triggers the skill, not a verdict.
- `skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`, `skills/motion-advanced/SKILL.md` — OK — no verdict/template/distinctiveness hits.
- `skills/inherit-legacy-style/SKILL.md:123-128` — OK — "FAIL: Do NOT …" are process prohibitions for the skill, not screen verdicts.
- `skills/frontend-slides/SKILL.md:26, :165, :181` — OK — anti-pattern guidance ("avoid generic purple-gradient … template-looking decks") + checklist.
- `skills/loop-design-check/SKILL.md` — OK — loop-design judgments (judge independence, exit conditions), not screen verdicts.
- `skills/api-design/SKILL.md` — OK — HTTP failure statuses, not screen verdicts.

### Whole-tree grep
- Grep for `distinctiveness | AI slop | ai-slop | reads as a template | default template` across `skills/ agents/ commands/ rules/ hooks/` (excluding node_modules): only the GAN agents/commands outside the listed skills match — all checked above. No other skill states a template/generic verdict.

## Not re-flagged (adjudicated design)
Byte-identical assets; `hooks/adapter.js` live infrastructure; `agent-emit-pi.js` dead code; 71/96 command files with only `description:` frontmatter; qc_patch `ecc-code-reviewer` → `code-reviewer`; stale `triggersDigest` by design; `--domain plain` search reference-only; montage/explainer ask-first opt-ins; `themes/terminal.md` material header; `orch-pipeline` "two human gates" wording. None of these was counted above. `impeccable-critique.md:222` ("warmer / more playful / more distinctive") was verified fixed in #13c and is not re-flagged.

## SWEEP: 12 BLOCKING / 7 MINOR
