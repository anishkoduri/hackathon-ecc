# Fix #15 — rule-change spec (implementer brief, read with BASELINE.md)

Starting state: build.sh 23,160 lines, md5 `6253677ce02c8625dadb41e1acf32e6b`
(verify this FIRST with `wc -l` + `md5sum` before editing; if it differs, stop
and report). Counts 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks.
Last clean: Audit #52 ZERO, dry-run #24 CLEAN, sweep CLEAN.

Standing constraints (do NOT weaken any of these):
- "More, not bolder" (orchestrate :90, standalone :40).
- browser-qa is the SOLE executor of pass/fail verdicts on rendered screens.
  Everything else is guidance / candidate evidence / static checks, never a verdict.
- Impeccable craft-floor bans are absolute as static checks (no kicker/eyebrow,
  no gradient text; same-size icon+heading+text cards pattern and hero-metric
  template are candidate evidence for browser-qa, never a rewrite on this check
  alone). Hallmark floor binds. No violet. Anti-derivative rule. Snapshot-before-
  redesign. Shared fresh-verdict budget 2 rounds.
- Do NOT re-flag adjudicated items (explicit --domain plain search serves
  reference rows only; hooks/adapter.js is live Cursor infrastructure;
  byte-identical assets are not defects; agent-emit-pi.js dead code is Pi-native).
- NEVER re-run fix11/fix11-stage.py (it would clobber the fix-#12 critique.md edits).
- No new inventory (no new treatments, skills, or themes) unless a genuine gap is
  found — the point is usage of what exists.
- Edit staged sources only (standalone skill sources where the plugin copies them,
  e.g. less-flat-ui lives at ~/workspace/cursor-skills/); NEVER edit the built
  tree directly — the build regenerates it. If a build.sh runtime patch anchor
  must change (as fix14's W2-C1 anchor did), change the anchor, keep the diff
  minimal, save a backup (build.sh.before-fix15).
- Do NOT commit, bundle, touch GitHub, or touch the Campus Eats artifact.

## A. Canonical variety + theme-match rule (verbatim everywhere)

Place this block VERBATIM (same heading, same wording) in EACH of:
`skills/design-taste-frontend/SKILL.md`, `skills/ui-ux-pro-max/SKILL.md`,
`skills/less-flat-ui/SKILL.md` (standalone source), `skills/polish-pass/SKILL.md`,
the Hallmark placement (see below), each motion skill
(`skills/make-interfaces-feel-better/SKILL.md`,
`skills/motion-foundations/SKILL.md`, `skills/motion-patterns/SKILL.md`,
`skills/motion-advanced/SKILL.md`), `skills/orchestrate/SKILL.md`
(design-package rule), and the standalone engine's design-package rule
(`skills/orch-build-mvp/SKILL.md` — it carries the identical rule; mirror it
there too). Adapt only the anchor (where in the file it sits); keep the wording
identical so audits can grep it everywhere. If a file already states part of
this, do not duplicate-contradict: place the block once and adjust the
surrounding sentence to point at it.

> **Element variety, all theme-matched.** Every build applies design elements
> across a wide variety of kinds — treatments, moments, effects, diagrams,
> components, motion, and type moments — never all of one kind: a build whose
> new elements are all one kind has not met this rule. Every element, of
> whatever kind, must match the dealt theme (its material, tokens, palette
> balance, and do-nots): theme-match is a precondition, not a preference — an
> element that clashes with the theme is not applied, and the reason is
> recorded in `docs/design-tokens.md` with the element. Every element
> application is recorded per surface in `docs/design-tokens.md` (surface →
> elements applied, kind, theme-fit).

Hallmark placement: FIRST read
`skills/design-taste-frontend/references/hallmark/PROVENANCE.md` and check
whether `references/hallmark/references/gates.md` and
`references/hallmark/references/hallmark-floor.md` are staged verbatim from
upstream. If a file is staged verbatim, DO NOT edit it — instead place the
block in the Taste SKILL.md Hallmark-deal paragraph (plugin-authored) and note
in the manifest why the Hallmark files themselves were left untouched. If a
file is plugin-authored, place the block there.

## B. The five count-moving rules (each must move the Campus Eats count)

Implement each as an enforceable, checkable rule (a required step or checklist
item with a record, not a wish). Every new number must cite the rule it changes
and the baseline count it raises (BASELINE.md).

- **R1 — every dealt moment is applied or re-dealt.** (Baseline gap: iris-opens
  dealt, never applied.) In Taste step 4 (moments pick) + step 6 check: the
  build record must list one application per dealt moment, or a re-deal log
  entry with reason. A dealt moment with neither is an incomplete build
  (static check item in Taste step 6 / orchestrate Verify step 6 — NOT a
  screen verdict). Expected: +1 Moment (iris-opens).
- **R2 — one diagram by default on software pages.** (Baseline: 0 diagrams.)
  Taste §3 asset table says diagrams "0–2" — change to "1–2 by default; 0 only
  with a recorded reason in the section plan". Software pages only (the
  table's column already scopes it). Expected: +1 Diagram.
- **R3 — two distinct treatment kinds per app screen.** (Baseline: 2 treatment
  applications, both Soft Shadow — one kind.) In less-flat-ui's surface check:
  on app/dashboard surfaces, at least TWO DISTINCT treatment kinds must be
  recorded per screen, or "none — <reason>" per untreated surface. The second
  kind must be theme-matched (rule A governs the choice). Expected:
  +1 Treatment (a second kind, e.g. a re-tinted grainy gradient on an
  app-frame utility surface — the implementer picks the fitting one per the
  theme; do NOT hard-code which kind, only that a second distinct kind is
  required).
- **R4 — the dealt hero's loop is implemented or waived.** (Baseline gap: the
  centred-hero spec's loop inside the window, never applied.) In Taste step 5/6
  (build/check): the dealt hero's loop (or moment-inside-window) is implemented
  and recorded, or waived with reason in design-tokens.md. Expected:
  +1 Motion.
- **R5 — each Range pattern's named lead element is its own element.** (Baseline:
  the Bento lead tile's lone figure was folded into the tile, not counted.)
  In Taste step 4a (frozen system — Range patterns): when a theme Range pattern
  names a lead/hero element (e.g. Sticker's Bento "the lead tile carries the
  lone figure"), that element is recorded as its own type moment in
  design-tokens.md, distinct from the surface carrying it. Expected: +1 Type.

Expected after: 30 elements (+20%), by kind: Component 18, Treatment 3,
Visual 1, Motion 3, Moment 2, Type 2, Effect 0, Diagram 1. If the re-trace
measures less than +4, the deficient rule(s) must be strengthened — a rule
that does not move the count does not count toward the 15–20%.

## C. Fonts + text through the design skills

- **C1 — dealt faces only.** In Taste step 4a (Typography line) and the
  ui-ux-pro-max type-scale step: the dealt pairing (Hallmark theme pairing /
  ui-ux-pro-max type scale) is the ONLY permitted faces on the build; no other
  face is introduced. Record the pairing + its source in design-tokens.md.
- **C2 — self-host display faces.** Display faces are self-hosted (bundled
  woff2 + `@font-face` in the built page) whenever the face's character matters
  — craft floor: the closest installed font is a failure, not a fallback.
  Body faces name their source (self-hosted or link) and fallback stack in
  design-tokens.md. This is a required build step, not a recommendation.
  Checkable: the built page contains `@font-face` for the display face; the
  tokens file names the source.
- **C3 — copy + type checks enforced and recorded.** Taste copy-voice rules
  apply to ALL copy; craft-floor type checks (body measure 65–75ch, obvious
  scale/weight steps, balanced headings, contrast 4.5:1 / 3:1 large) are
  verified per surface and recorded in design-tokens.md's Type list
  (surface → face/size/measure/contrast). The polish-pass harmony check
  verifies the Type list (consistency only — a surface whose type does not
  trace to the recorded pairing/scale is a harmony divergence, recorded as
  candidate evidence, never a verdict). Do not weaken any existing ban to do this.

## D. Mandatory screenshot QA at least once before finish

Wire into EXISTING tooling; do not invent new tooling and do not duplicate runs
that already happen — make the existing run count toward the requirement and add
enforcement + recording where it is missing.

- **D1 — the rule (place in orchestrate step 5/6 finish, Taste step 6, polish-pass
  Verify, standalone step 6/9):** "Before the final report is written, the build
  runs a screenshot QA pass at least once: the rendered page/app is inspected in
  screenshots (desktop + mobile) for whitespace, sizing, spacing, alignment,
  overflow, and collisions. The pass counts toward the requirement from whichever
  existing tooling ran it (Taste shoot.mjs / check.mjs / consistency.mjs,
  polish-pass before/after verification, or browser-qa's visual loop) — do not
  run a duplicate pass to satisfy it; record the run (tool, screens, findings
  count) in the run ledger and the final report. A build that never ran a
  screenshot QA pass is incomplete and cannot be reported as finished. Findings
  feed the fix batch like other checks; browser-qa alone issues pass/fail
  verdicts on rendered screens."
- **D2 — where runs already exist:** orchestrate step 5 Verify runs browser-qa's
  visual loop (screenshots) and Taste step 6 runs shoot/check/consistency —
  those runs already satisfy the "at least once"; what is missing is the
  recording line + the incomplete-build gate. Add those; do not add a second
  screenshot run.
- **D3 — recording:** the run ledger line + final-report line name the tool, the
  screens, and the findings count. A dry-run must verify the check ran at
  least once before the build finished (see §E).

## E. Verification artifacts to produce

- `fix15/fix15.py`: the edits (count==1 asserts like fix14's), + backup
  `build.sh.before-fix15` if build.sh changes.
- `fix15/verify15.py`: checks against the BUILT tree — canonical rule block
  present verbatim in every target file; R1–R5 anchors present; C1–C3 anchors
  present; D1 anchors present; treatments still 23; counts unchanged;
  build.sh diff minimal and documented. All checks must pass.
- Rebuild TWICE with `bash ~/workspace/hackathon-plugin/build.sh`; both exit 0
  and built-tree manifest diff = 0. Record line count + md5 + manifest hash.
- The dry-run (separate worker) re-traces Campus Eats under the new rules and
  counts before/after by kind using BASELINE.md's counting rule. If it measures
  under +4, report which rule(s) failed to move the count and strengthen them
  (iterate with the coordinator) — do not ship a sub-target result.

## F. What the implementer returns

Conclusion + evidence (≤20 lines in the handoff, full detail in fix15 files):
files changed (file:line for every rule), build exit/diff, md5, verify15.py
result, manifest hash, and anything you could not place (with the reason).
Quote actual numbers from tool outputs, not from memory.
