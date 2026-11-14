# Fix #22 process report — §9 Mobbin + §10 directives

**Date:** Nov 12, 2026. **Agent:** fix #22 process-additions implementer (Mobbin + directives).
**Scope:** SPEC §9 (Mobbin as pattern research, three touchpoints) and §10
(directives, not descriptions, six placements). No disposition rows were added or
changed — per the task, Mobbin and directives are process additions recorded
separately; the 144-item disposition table stands unchanged.

## 1. Mobbin access method (verified Nov 12, 2026)

Web search re-verified the coordinator's determination the same day (sources:
Mobbin pricing page via third-party pricing summaries checked Oct–Nov 2026):

- **Free tier: $0.** Limited apps/sites (latest few), **no search, no Flows,
  no Animations, 3 collections**, limited copying/downloads.
- **Official integration is Pro+ at $10/month billed yearly** ($120/year; $45/quarter
  also offered) — NOT on the free tier. **REST API is Team/Enterprise only**
  ($16/member/month billed yearly and up).
- **Therefore plugin access is WEB BROWSING ONLY on the free tier.** No API assumed,
  no paid integration assumed, no paid subscription, no paid account, no account
  creation that costs money. The paywall case is common — the recorded-gap fallback
  (design proceeds from the skills alone, gap recorded, build NEVER blocked) is the
  operative path, not an edge case. Every rule text below states this.
- No Mobbin integration tool name is written anywhere in the rule texts (per the
  task constraint); the texts say "web browsing only, no API/MCP on the free tier".

## 2. §9 Mobbin — per-touchpoint placement (all three done, staged edits)

| # | Touchpoint | Anchor | Placement (file:line) |
|---|---|---|---|
| 1 | Direction research — orchestrate design-package step | MOBBIN_RESEARCH_F22 | `new-skills/orchestrate/SKILL.md:62` — step 3 Slice, inserted after the H2 accent-hierarchy sentence, before "A UI brief with no named design components … is not ready to dispatch." Named research step, CATEGORY + PATTERN level only, categories consulted recorded in the decision record, direction then generated through the package skills; no-copy boundary, free-tier-only + recorded-gap fallback, platform match, theme-match precondition, D19 six dimensions. |
| 2a | Build pattern reference — Taste half | MOBBIN_PATTERN_F22 | `new-skills/design-taste-frontend/SKILL.md:443` — step 5 Build, appended after the dealt-hero's-loop sentence. MAY consult the matching pattern for structure/states/conventions, then implement through Taste theme-matched with a D19 reason; dealt moments may be informed by real patterns but are generated through Taste; no-copy boundary, free-tier-only + recorded-gap fallback, platform match, theme-match precondition, D19 six dimensions. |
| 2b | Build pattern reference — ui-ux-pro-max half | MOBBIN_PATTERN_F22 | Patch spec P1 in `fix22/process-patches.md` — target `skills/ui-ux-pro-max/SKILL.md` (built-tree line 92, after the "Generated direction" paragraph). Same rule, app-surface wording (direction = dealt theme or the named direction in MASTER.md). Build.sh-patched skill: patch spec only, no direct edit. |
| 3 | QA convention check — polish-pass | MOBBIN_QA_F22 | `round2-skills/polish-pass/SKILL.md:104` — new non-negotiable #8, after the harmony check (#7). Category-convention check (e.g. checkout shows the total before the pay button; destructive actions confirm); gaps are CANDIDATE EVIDENCE for `browser-qa`, NEVER a verdict (screen-verdicts rule, fix #13e); appended to `.hallmark/candidate-evidence.md`; no-copy boundary, free-tier-only + recorded-gap fallback, platform match, theme-match precondition, D19 six dimensions. |

## 3. §10 directives — per-placement coverage (all six done or covered-by-form)

| # | Placement | Anchor | Location |
|---|---|---|---|
| 1 | Orchestrate — implementer briefs carry exact values | DIRECTIVES_F22 | `new-skills/orchestrate/SKILL.md:64` — step 4 Build, appended to the "Design package in every UI brief" sentence. Briefs carry DIRECTIVES (exact tokens/measurements/type/copy/motion/layout + named skill); prose-only FAILS the handoff check; directive without D19 reason incomplete; implementers do not re-interpret (recorded gap instead); on-skill innovation recorded AS a directive. |
| 2 | Taste — handoff / frozen system | DIRECTIVES_F22 | `new-skills/design-taste-frontend/SKILL.md:389` — step 4a, after "on divergence this file wins." `docs/design-tokens.md` lists directives per surface (surface → directive + D19 reason); prose-only FAILS; directive without D19 incomplete; no re-interpretation. |
| 3 | ui-ux-pro-max — every component spec is a directive | DIRECTIVES_F22 | Patch spec P2 in `fix22/process-patches.md` — target `skills/ui-ux-pro-max/SKILL.md` (built-tree line 112, after the fix #20 X1 paragraph). MASTER.md component entries record directive + experience + D19 lines. |
| 4 | Hallmark — theme-deal output | DIRECTIVES_F22 | `new-skills/design-taste-frontend/SKILL.md:389` (step 4a, same rule as #2: the dealt theme is recorded as tokens + moments, exact values, not prose) + pointer line at `new-skills/design-taste-frontend/SKILL.md:242` (end of the "Deal a Hallmark theme" paragraph). See §5 for the home justification. |
| 5 | GAN planner / generator / evaluator | DIRECTIVES_F22 | Patch specs P3/P4/P5 in `fix22/process-patches.md` — targets `agents/ecc-gan-planner.md` (built-tree line 44, new bullet after Direction source), `agents/ecc-gan-generator.md` (built-tree lines 25–30, new paragraph after Key Principles), `agents/ecc-gan-evaluator.md` (built-tree line 132, new rule after the "Write feedback" line). Planner: spec design direction as directives. Generator: execute verbatim, flag gaps, never improvise. Evaluator: every feedback item is a directive with exact replacement values; scoring untouched, no screen-distinctiveness verdict. GAN agents are build.sh-embedded: patch specs only. |
| 6 | polish-pass — fix directives | DIRECTIVES_F22 | `round2-skills/polish-pass/SKILL.md:100` — non-negotiable #6 "Be concrete", extended. Every fix is a DIRECTIVE (exact old value → exact new value + named skill + D19 reason); prose-only fix FAILS the handoff check; implementers execute verbatim. |

## 4. Covered-by-form (no edit — verified, not assumed)

- **motion-* skills (motion-foundations / motion-patterns / motion-advanced):**
  covered-by-form. Verified in the built tree Nov 12: `motion-patterns` code examples
  already express motion as exact token values (`motionTokens.duration.normal/slow/fast`,
  `motionTokens.easing.smooth`); `motion-foundations` defines the shared `motionTokens`
  object (duration, easing, distance, scale) and states "All token values come from
  `motionTokens`. Hardcoded durations and easings in component files are forbidden."
  That IS the directive form — no motion edit was made, per SPEC §10 rule 4.
- **less-flat-ui (global skill, `~/workspace/cursor-skills/less-flat-ui/SKILL.md`):**
  covered-by-form. Treatments are already classes + values (e.g. shared `.grain`
  overlay class, `backgrounds.css` referenced by class) and are recorded per surface
  in `docs/design-tokens.md` with the six D19 dimension lines. NOT edited — it is a
  global skill outside the plugin, per the task. Verified Nov 12 (30 sections;
  treatment-recording rule with D19 requirement present).
- **browser-qa:** already issues direct pass/fail verdicts — that is the model per
  SPEC §10; no change needed and none made (screen-verdicts rule untouched).

## 5. Hallmark home justification

The directive requirement for the theme deal lives in **Taste step 4a**
(`new-skills/design-taste-frontend/SKILL.md:389`), with a one-line pointer at the
end of the "Deal a Hallmark theme" paragraph (`:242`) — NOT in any file under
`references/hallmark/`. Reasons:

1. The theme deal's **output contract** lives in Taste, not in Hallmark's files:
   step 4a is where the dealt theme is recorded (first two lines of
   `docs/design-tokens.md` = theme slug + Tokens block + palette balance) and where
   the frozen system is written. A rule about how that output is recorded belongs
   where the recording happens.
2. The files under `references/hallmark/` (theme catalog, `gates.md`,
   `hallmark-floor.md`, reviewer prompts) are **Hallmark-upstream content**
   (MIT, nutlope / Together AI, v2.0.0 — see `references/hallmark/PROVENANCE.md`).
   Editing a theme file or gate file to add a plugin process rule would fork
   upstream catalog content and would not bind the deal flow, which Taste owns.
3. The pointer at `:242` keeps the deal paragraph itself aware of the rule without
   duplicating it: the deal runs in step 4, the recording rule sits in step 4a where
   the deal's output lands.

## 6. Verification performed by this agent

- Every anchor grepped before insertion: each occurred **exactly once** in its file
  (orchestrate Mobbin anchor 1, orchestrate directives anchor 1, Taste Mobbin anchor 1,
  Taste step-4a anchor 1, Taste Hallmark-floor anchor 1 with the fuller form,
  polish-pass #6 anchor 1, polish-pass #7 anchor 1; patch-target anchors each 1 in
  the built tree).
- After editing, re-grepped: `MOBBIN_RESEARCH_F22` ×1 (orchestrate:62),
  `MOBBIN_PATTERN_F22` ×1 staged (Taste:443) + ×1 patch spec (P1),
  `MOBBIN_QA_F22` ×1 (polish-pass:104), `DIRECTIVES_F22` ×1 orchestrate (:64),
  ×2 Taste (:242 pointer + :389 rule), ×1 polish-pass (:100), ×1 per GAN/ui-ux-pro-max
  patch spec (P2–P5). No anchor occurs twice in any one file except the intentional
  Taste pointer + rule pair.
- Banned terms: the seven inserted staged texts were extracted and scanned
  case-insensitively for the seven banned terms — **0 hits**. No Mobbin integration tool name appears in any new text. No model pin
  touched; no font rule, screen-verdicts rule, marketplace manifest, or Audit #4
  backup touched; `hackathon-ecc/` never edited; `build.sh` never run or edited;
  `fix11/fix11-stage.py` never run; `less-flat-ui` and motion-* skills never edited.
- No disposition file touched (disposition-A/B/CD/E/F/G unchanged); no new skill
  created (no "mobbin" skill, no directives skill).
- Wave-1 overlap check: the edited files already carried wave-1 fix #22 text
  (orchestrate PRINCIPLES_F22/LAWS_F22 + H2; Taste TRENDS_F22 + finish-gate pointer;
  polish-pass SLOP_F22/UNSLOP_F22/H1/H2). All new text was added adjacent to, never
  over, that text; no wave-1 sentence was modified or duplicated.

## 7. Deviations proposed

**None.** No §9 or §10 rule proved unworkable. Two notes for the coordinator (not
deviations):

1. **SPEC §11 (free GitHub asset libraries — Lenis/GSAP/Vanta/React Bits) appeared
   in MEMORY.md during this task** (added Nov 12 ~17:06, after this task was assigned).
   It is OUT of scope for this agent — no §11 work was attempted, and nothing in this
   report covers it. It needs its own implementation assignment.
2. **GAN evaluator scope note:** the P5 spec explicitly confines the directive rule to
   feedback items, leaving scoring untouched and restating that the evaluator never
   issues a screen-distinctiveness verdict. This is a clarification inside the spec,
   not a change to SPEC §10 — the evaluator is a design bot for its fix directives,
   while its scores stay rubric-governed.

## 8. Files delivered

- `~/workspace/hackathon-plugin/fix22/process-patches.md` — patch specs P1–P5
  (ui-ux-pro-max Mobbin + directives; GAN planner/generator/evaluator directives).
- `~/workspace/hackathon-plugin/fix22/process-report.md` — this file.
- Staged edits: `~/workspace/hackathon-plugin/new-skills/orchestrate/SKILL.md`
  (lines 62, 64), `~/workspace/hackathon-plugin/new-skills/design-taste-frontend/SKILL.md`
  (lines 242, 389, 443), `~/workspace/hackathon-plugin/round2-skills/polish-pass/SKILL.md`
  (lines 100, 104).
