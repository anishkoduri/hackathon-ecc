# Fix round #13e — spec D (items 5, 6, 7, 9)

Worker D. All re-traces done in the BUILT tree (`~/workspace/hackathon-plugin/hackathon-ecc/`).
Staged Hallmark sources verified identical to the built copies (`diff -q` silent for all four files),
so item-9 specs are staged-file specs. Items 5/6/7 targets are upstream ECC with NO staged
source (checked `new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/` — no hits),
so those specs are build.sh-patch specs against the built-tree text.

Reframing applied throughout: `browser-qa` is the SOLE executor of pass/fail VERDICTS on
rendered screens. Everything else is design guidance, candidate evidence, or a static check,
worded as such, never as a pass/fail verdict on a screen.

Citation corrections vs the parent brief (all else confirmed):
- hallmark-floor.md: the unscoped trigger sentence spans **:62–63**, not :64–65
  (:64–65 are the stamp line; the scope note is :67, not :40). Spec 9b anchors :62–63.
- Item 7: all three skills DO exist in the built tree (`skills/orch-add-feature/SKILL.md`
  45 lines, `skills/orch-fix-defect/SKILL.md` 43 lines, `skills/orch-refine-code/SKILL.md`
  44 lines); the parent's "no staged" note was about staged sources, which is correct —
  there is no staged source for any of them, so all three are build.sh-patch specs.
  The three commands also exist in the built tree (36/40/41 lines) and also carry no
  design-package rule — but the mirror pattern is skill-only: `orch-change-feature`'s
  rule lives ONLY in its skill (`commands/orch-change-feature.md` has 0 design-package
  hits), so item 7 specs the three skills only. The engine already expects it:
  `skills/orch-pipeline/SKILL.md:120` ("the design package was named in the brief").

## 5a — agents/ecc-gan-planner.md (description) [build.sh patch]
Re-trace: `agents/ecc-gan-planner.md:3` confirmed. The planner's role is still to generate
the design direction itself ("Expands a one-line prompt into a full product specification
with features, sprints, evaluation criteria, and design direction"), which lets the loop
re-derive direction on its own. Under decision B the direction comes from the design-lead
(model `grok-4.7-high`) BEFORE the loop; the planner records it.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and design direction. (Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)"
```
NEW (verbatim, in a code fence):
```
description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, and evaluation criteria, and records the design direction supplied by the design-lead (model grok-4.7-high) before the loop — the planner records the direction, it does not generate or re-derive one. (Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)"
```

## 5b — agents/ecc-gan-planner.md [build.sh patch]
Re-trace: `agents/ecc-gan-planner.md:44` confirmed. #13d already landed the anti-derivative
wording here ("never specific sites/apps to draw from"), but the template still has the
planner GENERATE the direction ("named direction generated through the design package skills").
Under decision B the direction is supplied, not generated.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
- **Direction source**: [named direction generated through the design package skills (`ui-ux-pro-max` direction / dealt Hallmark theme) — never specific sites/apps to draw from; the anti-derivative rule forbids basing the design on a searched external reference]
```
NEW (verbatim, in a code fence):
```
- **Direction source**: [the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` BEFORE this loop — copied here, not generated: the planner records the supplied direction and never re-derives one from a searched reference or a fresh invention; if no direction is recorded, record the brief's stated default, marked assumed, and proceed — never a searched external reference, per the anti-derivative rule]
```

## 5c — agents/ecc-gan-planner.md [build.sh patch]
Re-trace: `agents/ecc-gan-planner.md:95` confirmed (Guidelines §2). As worded ("Specify exact
colors") it instructs the planner to invent the palette — i.e. to generate direction.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
2. **Specify exact colors** — Not "blue theme" but "#1a73e8 primary, #f8f9fa background"
```
NEW (verbatim, in a code fence):
```
2. **Record the supplied direction's exact tokens** — copy the colours, type and layout from the design-lead's recorded direction in `docs/design-tokens.md` (not "blue theme" but "#1a73e8 primary, #f8f9fa background"); do not invent a new palette — the planner records the direction, it does not generate one
```

## 5d — commands/gan-build.md [build.sh patch]
Re-trace: `commands/gan-build.md:24` confirmed (Phase 1, step 1). The launch hands the planner
only the user's brief, so a standalone `/gan-build` run lets the planner originate direction.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
1. Launch the `gan-planner` agent as a Cursor subagent with the user's brief
```
NEW (verbatim, in a code fence):
```
1. Launch the `gan-planner` agent as a Cursor subagent with the user's brief, plus the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` — the direction comes from the design-lead BEFORE the loop; the planner records it in the spec and the loop executes under it, it does not generate or re-derive a direction on its own
```

## 5e — commands/gan-design.md [build.sh patch]
Re-trace: `commands/gan-design.md:12` confirmed. "No planner — the brief IS the spec" leaves
the brief as the sole direction source with no design-lead step, so the loop can re-derive
direction from a bare brief.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
A two-agent loop (Generator + Evaluator) focused on frontend design quality. No planner — the brief IS the spec.
```
NEW (verbatim, in a code fence):
```
A two-agent loop (Generator + Evaluator) focused on frontend design quality. No planner — the brief IS the spec, and the brief carries the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` — the direction comes from the design-lead BEFORE the loop; the loop executes under it and does not re-derive a direction on its own.
```

## 5f — commands/gan-design.md [build.sh patch]
Re-trace: `commands/gan-design.md:39` confirmed. "Push for creative leaps — unusual layouts,
custom animations, distinctive color work" instructs the generator to originate direction
(a new colour/layout direction) rather than execute the recorded one.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
The Generator is told: "Your PRIMARY goal is visual excellence. A stunning half-finished app beats a functional ugly one. Push for creative leaps — unusual layouts, custom animations, distinctive color work."
```
NEW (verbatim, in a code fence):
```
The Generator is told: "Your PRIMARY goal is visual excellence within the recorded direction. A stunning half-finished app beats a functional ugly one. Push for creative leaps — unusual layouts, custom animations, distinctive color work — inside the design-lead's direction, never by re-deriving a new direction."
```

## 5g — README.md (built tree) [post-STEP-4 patch in build.sh — NOT a heredoc edit]
Re-trace: built `README.md` has **0 `grok` hits** (verified by grep), while the picker
instruction lives only in the repo-root `~/workspace/hackathon-plugin/README.md:17`.
Chosen method: a post-STEP-4 patch step in build.sh (applied to the generated README after
the STEP 4 heredoc at `build.sh:18324`), NOT an edit to the heredoc itself — the anchor below
exists in the heredoc too (`build.sh:18391`, same text), so the patch anchor will exist at
build time either way. Placement: `## Prerequisites` section of the shipped README, as a new
bullet immediately after the Taste bullet — the setup section, next to the other first-build
prerequisites, before `## Install`.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate (run the gate explicitly — it does not auto-run on stop in Cursor).
```
NEW (verbatim, in a code fence):
```
- **Taste** needs Node 22+ and Chrome/Edge/Chromium for its finish gate (run the gate explicitly — it does not auto-run on stop in Cursor).
- **Before the first build — Grok 4.7 High in the model picker:** the plugin pins its design role to `grok-4.7-high`. Cursor's subagent model allowlist is coupled to the model-picker dropdown, so select **Grok 4.7 High** in Cursor's model picker before the first build, or the design pin may silently fall back to another model. This is a one-time setup note, not a mid-build ask. File-level pin only — whether it holds is decided by the live smoke test (`LIVE_SMOKE_TEST.md` §14).
```

## 6a — skills/design-system/SKILL.md [build.sh patch]
Re-trace: `skills/design-system/SKILL.md:27` confirmed ("3. Research 3 competitor sites for
inspiration (via browser MCP)"). Whole-Mode-1-section check: grep for
`competitor|inspir|reference|Research|search|external` over the whole file returns ONLY
:27, and `browser|MCP` over the whole file returns ONLY :27 plus the already-reframed
Mode 3 scope note at :56 (which names no competitor/inspiration source). No other
competitor/inspiration language exists in Mode 1 (steps 1–2 scan/extract from the own
codebase; steps 4–6 propose tokens, rationale, preview). design-system is upstream ECC
(no staged source), so this is a build.sh-patch spec.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
3. Research 3 competitor sites for inspiration (via browser MCP)
```
NEW (verbatim, in a code fence):
```
3. Generate the direction through the design package skills (`ui-ux-pro-max` direction / `design-taste-frontend` / dealt Hallmark theme) and record it in `design-tokens.md` — never competitor sites and never a searched external reference (orchestrate row-10 anti-derivative rule)
```

## 7a — skills/orch-add-feature/SKILL.md [build.sh patch]
Re-trace: `skills/orch-add-feature/SKILL.md:32` confirmed (How It Works step 4, the last step
before the Example). 0 hits for `design package|design-tokens|ui-ux-pro-max` in this file
(verified by grep). The brief the orchestrator sends is governed by this skill's How It
Works list — the mirror of `orch-change-feature/SKILL.md:36` (step 5 there). The new step 5
below mirrors that wording, adapted to a net-new feature.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
4. Add `security-reviewer` if the feature touches a security trigger.
```
NEW (verbatim, in a code fence):
```
4. Add `security-reviewer` if the feature touches a security trigger.
5. **UI change / build-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a new feature that builds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
```

## 7b — skills/orch-fix-defect/SKILL.md [build.sh patch]
Re-trace: `skills/orch-fix-defect/SKILL.md:35` confirmed (How It Works step 4, the last step
before the Example). 0 hits for `design package|design-tokens|ui-ux-pro-max` in this file
(verified by grep). Same mirror as 7a, adapted to a fix that rebuilds a surface.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
4. Add `security-reviewer` if the defect sits in a security-sensitive path.
```
NEW (verbatim, in a code fence):
```
4. Add `security-reviewer` if the defect sits in a security-sensitive path.
5. **UI change / rebuild-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a fix that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
```

## 7c — skills/orch-refine-code/SKILL.md [build.sh patch]
Re-trace: `skills/orch-refine-code/SKILL.md:34–35` confirmed (How It Works steps 3–4). 0 hits
for `design package|design-tokens|ui-ux-pro-max` in this file (verified by grep). Unlike
7a/7b, step 4 here is the terminal commit step, so the rule cannot be appended after it —
it is inserted as new step 4 (before the change lands) and the commit step renumbers to 5.
Same mirror as 7a/7b, adapted to a restructure that rebuilds a surface.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
3. Stop at **Gate 1** (restructure plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. Commit as `refactor:` — the diff must be behavior-neutral.
```
NEW (verbatim, in a code fence):
```
3. Stop at **Gate 1** (restructure plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7).
4. **UI change / rebuild-a-surface rule.** If the change touches UI — including a restructure that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). The direction is generated through the package skills, never based on a searched external reference: if the design search returns only a marketing page, that is not a direction — the skills generate it instead. Posture is more, not bolder: more design decisions made deliberately through the skills, more craft. Verify the rebuilt surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only the recorded direction): a finding, minor at least, when it carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.
5. Commit as `refactor:` — the diff must be behavior-neutral.
```

## 9a — references/hallmark/references/gates.md [staged: new-skills/design-taste-frontend/references/hallmark/references/gates.md]
Re-trace: `gates.md:38` confirmed ("Before the sweep, score the planned page 1 to 5 on six
axes; anything under 3 triggers a revision first."). The :40 scope note below it already
governs the Specificity axis, but :38 as a bare sentence can still be read as a screen
verdict (any axis under 3 → revise). Reword :38 to point at the scope note so the note
governs it; the :40 scope note itself is unchanged.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first.
```
NEW (verbatim, in a code fence):
```
Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first — under the scope note below: this critique is a design input, not a distinctiveness verdict; only the five craft axes join the fix list, and a Specificity score under 3 is recorded as candidate evidence for `browser-qa`, never a verdict on its own.
```

## 9b — references/hallmark/references/hallmark-floor.md [staged: new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md]
Re-trace: parent citation corrected — the unscoped trigger sentence spans **:62–63**
("Before the sweep, score the planned page 1-5 on six axes; anything under 3 / triggers a
revision first."), :64–65 are the stamp line, and the scope note is :67 (not :40).
Same fix as 9a: point the trigger sentence at the Scope note below so the note governs it;
the :67 Scope note itself is unchanged.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first.
```
NEW (verbatim, in a code fence):
```
Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first — under the Scope note below (Specificity is candidate evidence for `browser-qa`, never a verdict; only the five craft axes join the fix list).
```

## 9c — references/hallmark/references/review-hero.md [staged: new-skills/design-taste-frontend/references/hallmark/references/review-hero.md]
Re-trace: `review-hero.md:9` confirmed ("- Does the headline say something only this product
could say, in seven words or fewer?"). What #13d already landed: the first-word sentence
(:5) already scopes ship/fix to the craft questions and says template observations never
drive it, and the template bullet (:11) already records template reads as candidate
evidence. What it did NOT do: the headline question itself is still worded as a
specificity/distinctiveness test ("only this product could say") sitting among the
first-word-driving craft questions, so it can still be read as driving the first word.
This spec reframes it as copy craft and routes the competitor-page case to candidate evidence.
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
- Does the headline say something only this product could say, in seven words or fewer?
```
NEW (verbatim, in a code fence):
```
- Does the headline say something only this product could say, in seven words or fewer? (Copy craft — whether the headline carries the product's own nouns and claim. A headline that would pass unchanged on a competitor's page is recorded as candidate evidence for `browser-qa`, not a finding of this review, and never drives the first word.)
```

## 9d — references/hallmark/references/review-finish.md [staged: new-skills/design-taste-frontend/references/hallmark/references/review-finish.md]
Re-trace: `review-finish.md:9` confirmed (467-char line). As written, the whole parenthetical
— mass/layout items (head and line adrift, narrow column, small section head) AND template
tells (empty coloured box, drawn illustration, counting marks) — "outranks every detail
finding", i.e. the template tells join the ranking as findings on their own. Split it:
mass/layout items keep outranking detail findings as craft; template tells are recorded as
candidate evidence for `browser-qa` instead. The copy sentence at the end of :9 is unchanged
(see Checked list).
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
Scroll the 1440 full page one screen at a time before ranking: a screen with nothing big enough to be its reason (a head and a line adrift, a narrow column beside an empty half, a section head under 40px, an empty coloured box or a drawn illustration where a photograph or the product should be, a row of counting marks) outranks every detail finding (`layout.md` § 8). Then the copy: name any head that would pass unchanged on a competitor's page (`craft.md` § 6).
```
NEW (verbatim, in a code fence):
```
Scroll the 1440 full page one screen at a time before ranking: a screen with nothing big enough to be its reason as a matter of mass and layout (a head and a line adrift, a narrow column beside an empty half, a section head under 40px) outranks every detail finding (`layout.md` § 8) — but a screen whose only mass problem is a template tell (an empty coloured box or a drawn illustration where a photograph or the product should be, a row of counting marks) is recorded as candidate evidence for `browser-qa` instead, never a finding of this review. Then the copy: name any head that would pass unchanged on a competitor's page (`craft.md` § 6).
```

## 9e — references/hallmark/references/review-finish.md [staged: new-skills/design-taste-frontend/references/hallmark/references/review-finish.md]
Re-trace: `review-finish.md:15` polish sentence confirmed ("...in at most five findings —
recorded as candidate evidence for `browser-qa`, not as findings of this review."). The
self-contradiction stands: "findings" that are "not findings". Resolve with one consistent
wording: observations, not findings, not joining the fix list. Anchor is the polish sentence
only (the redesign half of :15 is untouched).
Anchor check: old text occurs exactly 1 time in the target file (verified by python count).
OLD (verbatim, in a code fence):
```
On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, in at most five findings — recorded as candidate evidence for `browser-qa`, not as findings of this review.
```
NEW (verbatim, in a code fence):
```
On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, recording at most five observations as candidate evidence for `browser-qa` — observations, not findings of this review, and they do not join the fix list.
```

---

## Item-5 decision: (B) — design direction comes from the design-lead (Grok) BEFORE the loop
Reason: pinning all three GAN agents to `grok-4.7-high` would misassign a design-role model
to code implementation (generator) and Playwright testing/scoring (evaluator); the Grok pin
is for the design role only, and the loop's direction must be supplied, not generated.
Specs 5a–5f implement B (planner description + Direction-source + guideline 2, gan-build
Phase 1 launch, gan-design brief-is-spec + generator instruction); the three GAN agent
frontmatter `model:` lines stay `composer-2.5[fast=false]` (verified at
`agents/ecc-gan-planner.md:4`, `agents/ecc-gan-generator.md:4`, `agents/ecc-gan-evaluator.md:4`).
README placement (spec 5g): post-STEP-4 patch in build.sh, new bullet in the shipped
README's `## Prerequisites` section immediately after the Taste bullet (repo-root
`README.md:17` text copied verbatim); the built README had 0 `grok` hits before this change.

## orch-change-feature:36 quote mirrored for item 7
`skills/orch-change-feature/SKILL.md:36` (step 5, "UI change / rebuild-a-surface rule"):
"If the change touches UI — including a one-prompt change, a redesign, or a removal that
rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md
row 10): name the applicable design components in the brief (app/dashboard/components:
`ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat;
landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`;
new design-system work: + `design-system`; legacy style drift: + `inherit-legacy-style`),
record the direction in the decision record / run ledger (the lightest-weight record that
exists for this flow — one line, a stated default from the brief's mood/domain if silent,
marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the
applicable package components before the change lands. The design role runs on model
`grok-4.7-high` (slug form only). The direction is generated through the package skills,
never based on a searched external reference: if the design search returns only a marketing
page, that is not a direction — the skills generate it instead. Posture is more, not bolder:
more design decisions made deliberately through the skills, more craft. Verify the rebuilt
surface against the distinctiveness bar through `browser-qa`'s visual loop on the rebuilt
surface (the single executor of the bar — see orch-pipeline Review; the reviewer checks only
the recorded direction): a finding, minor at least, when it carries no named direction, no
applied theme/tokens, reads as a default template, or is derivative (the design is based on
a searched external reference) — within the existing fix caps. Pure backend/logic changes
with no visual surface are exempt."

## Checked, not changed
- `new-skills/design-taste-frontend/references/hallmark/references/gates.md:14` — Ledger "never counts toward the verdict": bookkeeping grade, not a screen verdict.
- `gates.md:95` gate 8 ("The AI template…") + `gates.md:191` judged clause "8 and 32, repetition" — repetition checks against the build log (a static comparison, not a rendered-screen verdict); their Step-7 judged application runs through the finish review, whose first word is already scoped to exclude template observations (`review-finish.md:5`).
- `gates.md:199` "23, footprint by eye… undeclared sprawl still fails" — a Reflex gate's grade (static/render gate check), not a screen-distinctiveness verdict.
- `gates.md:245` "Act on its first word" — the reviews' first word is scoped by `review-hero.md:5` / `review-finish.md:5` to craft/gates/defects only.
- `gates.md:40` scope note + `hallmark-floor.md:67` Scope note — already airtight; specs 9a/9b only point the trigger sentences at them.
- `review-hero.md:5` first-word sentence + `:11` template bullet + `:16` custom run — already record-as-candidate-evidence; 9c closes only the headline question's own wording.
- `review-finish.md:5` first-word sentence + `:13` "Seen before" — already candidate-evidence scoped.
- `review-finish.md:9` copy sentence ("name any head that would pass unchanged on a competitor's page") — kept as-is: copy craft (generic-head finding per `craft.md` §6, same family as Floor gate 19 copy tells), not a screen-distinctiveness verdict. Judgment call — parent may still want it routed to candidate evidence.
- `review-finish.md:13` "Clean: …a screen has nothing worth looking at" — mass/layout craft observation, not a template verdict.
- `skills/design-system/SKILL.md:56` Mode 3 scope note — already reframed in #13d; whole-file grep confirms :27 is the only competitor/inspiration language.
- `agents/ecc-gan-planner.md:105` Process step 2 ("read any existing examples or specs in the codebase") — own-codebase reading, not an external reference.
- `agents/ecc-gan-planner.md:107` eval-rubric deferral + `agents/ecc-gan-evaluator.md:31/:94/:116` deferrals — already reframed in #13d.
- `skills/orch-pipeline/SKILL.md:72` reviewer checks recorded direction only + `:120` "the design package was named in the brief" — engine expectation item 7 now satisfies; engine text needs no edit.
- `commands/orch-change-feature.md` — 0 design-package hits, rule lives in the skill only; this is the mirror pattern for item 7 (skill-only specs), not a gap.
- `commands/orch-add-feature.md`, `commands/orch-fix-defect.md`, `commands/orch-refine-code.md` — same mirror pattern; not specced, per the orch-change-feature precedent.
- `skills/orch-build-mvp/SKILL.md:40` Grok pin + direction-through-package-skills wording — already correct; not touched.
- `agents/ecc-gan-planner.md:4`, `agents/ecc-gan-generator.md:4`, `agents/ecc-gan-evaluator.md:4` (`model: composer-2.5[fast=false]`) — left as-is per decision B.

## Blocked / held back
- None blocked. Every OLD anchor verified to occur exactly once (16/16 via python count).
- Held back as a judgment call, not a spec: `review-finish.md:9`'s copy sentence (generic-head
  finding) was kept as a craft finding rather than routed to candidate evidence — see Checked
  list; parent decides if it should also be reworded.
- Held back by design (decision B): no spec pins any GAN agent to `grok-4.7-high` (option A
  rejected — see decision above).
