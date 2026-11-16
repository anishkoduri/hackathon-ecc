# Fix #27 — Staged-source patch log (staged-edits worker)

Source of truth: `fix27/SPEC.md` (§2, §3, §4, §5(a), §5(b), §5(c), §5(d), §5(f), §6).
Anchors re-read in the staged files before editing (staged line numbers differ
trivially from the audit's shipped-tree anchors; all anchors below are the
staged file's own text). 47 edits, 7 files. No build run, no built-tree edits,
no fix26/ or other fix-dir touches, no fix11 re-run.

Token census (grep, post-edit):
- `new-skills/orchestrate/SKILL.md`: THEME-START_F27×4, ALWAYSLEAD_F27×4,
  IMPL46_F27×2, CEILING_F27×4, DELRISK_F27×3, CHECKSRC_F27×2, AUDITGUIDE_F27×2,
  GRILLHDR_F27×1, DESIGNPKG-AUTO_F27×3, W2_F27×5, W3_F27×6, W4_F27×2
- `new-skills/design-taste-frontend/SKILL.md`: THEME-START_F27×4, W3_F27×1
- `new-rules/hackathon-mode.mdc`: THEME-START_F27×1, ALWAYSLEAD_F27×2,
  DELRISK_F27×2, DESIGNPKG-AUTO_F27×1
- `rewritten-skills/hackathon-scope/SKILL.md`: CEILING_F27×1, CHECKSRC_F27×1,
  AUDITGUIDE_F27×1, GRILLHDR_F27×1
- `new-skills/feature-expansion/SKILL.md`: W3_F27×1
- `new-skills/grill-me/SKILL.md`: GRILLHDR_F27×1
- `round2-skills/polish-pass/SKILL.md`: W3_F27×1

Banned-term check: no banned term introduced. The only hit in the edited
files is the pre-existing `claude -p` in `hackathon-mode.mdc:38` (untouched
line, pre-dates this fix). No bare `grok-4.6-high-fast` anywhere in the edited
files (all fast-tier pins use the `cursor-` slug form).

## 1. new-skills/orchestrate/SKILL.md — 31 edits

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §3 :14 | "The mechanics work under any lead model … but the pin is Grok 4.7 High." → deleted; "The orchestrator runs on Grok 4.7 High — the pin is binding, not a preference. If the session is not on Grok 4.7 High, say so in the first reply and proceed only as the fallback the user accepts — never silently." | ALWAYSLEAD_F27 |
| 2 | §4(b) :18 | Second-strong-tier-pass bullet → appended "Single pass by default: the second pass runs only when the first pass flags genuine uncertainty or when two genuinely different priors exist (routing row 8). Record a skipped second pass in the ledger." | W2_F27 |
| 3 | §4(a) roster | Team table → added row: implementation tier \| cursor-grok-4.6-high-fast \| slice-builder implementers for fully-specified slices — grok-4.7-high only where the slice still contains a design decision | IMPL46_F27 |
| 4 | §5(f) :54 | Precondition-check paragraph → appended "If the check finds no record and no explicit skip, that is itself a finding: state in the first reply that grill-me did not run and why (no trigger / no record), and ask the user whether to grill now (one prompt) or proceed — the one-question exception to §7. Do not silently proceed on a raw prompt." | GRILLHDR_F27 |
| 5 | §3 :50-56 | After "One build engine per run … never both." → added "Orchestrate leads every multi-piece run for the life of the project, not only the first build: the first-build sequence (grill → scope → expansion → build) applies to the first build, and the routing table + verification stage apply to every later run." | ALWAYSLEAD_F27 |
| 6 | §3 step 0 | Step 0 lead → added "MODEL-PIN check: in the first reply, state the model the orchestrator is running on and record it in the run ledger (`MODEL-PIN: grok-4.7-high \| other: <name>`). A pin that cannot be verified is recorded as unverified, not assumed held. Skill text cannot enforce the pin — Cursor-side enforcement would need a plugin-level model default, not more prose." | ALWAYSLEAD_F27 |
| 7 | §5(b) step 0 | "This is the ONE sanctioned user prompt during the first build besides grill-me itself" → "This is one of the two sanctioned user prompts during the first build besides grill-me itself (the other is the deliverable-at-risk flag, DELRISK_F27 …)" | DELRISK_F27 |
| 8 | §6 step 3 | "Design package in every UI slice brief:" → "Design package in every brief that contains a design decision:" — extended to every slice that makes a design decision, plus any non-UI slice that makes a visual call, the demo-video template, and docs/diagram work | DESIGNPKG-AUTO_F27 |
| 9 | §4(d) :66 | Inventory paragraph → "… USED vs CONSIDERED-AND-REJECTED … — only for entries actually considered for this build; untouched sections record one line (`not considered — <reason>`)" | W4_F27 |
| 10 | §4(d) :68 | AMBITION paragraph → same bound appended ("… never a blanket line — and only for entries actually considered for this build (untouched sections record one line, `not considered — <reason>`)") | W4_F27 |
| 11 | §4(c) step 3 | "the design-lead re-deals or redesigns until the table beats v5; a v5-level design does not proceed to build on a 'good enough' reading" → "re-deals or redesigns at most 2 times; after that the trailing dimension is recorded as owed with its cause (which is also the ceiling flag …) and the build proceeds on the best honest path, never on a 'good enough' reading that hides the gap" | W3_F27, CEILING_F27 |
| 12 | §4(a) :89 | "Slice-builder implementers spawn on the implementation tier — model `grok-4.7-high`" → "model `cursor-grok-4.6-high-fast` for fully-specified slices; `grok-4.7-high` only where the slice still contains a design decision — design-lead work stays 4.7" | IMPL46_F27 |
| 13 | §6 step 4 | "Design package in every UI brief (same rule as step 3)" → "Design package in every brief that contains a design decision (same rule as step 3, DESIGNPKG-AUTO_F27)" | DESIGNPKG-AUTO_F27 |
| 14 | §4(c) 5a | After "run after every implementer wave (per wave, per the Verification stage below)." → added "Per-wave reviewer cap: small waves get the step-1 cheap check only by default; the step-2 and step-4a reviewers run per wave only while waves are large — reviewer the exception, not the default." | W3_F27 |
| 15 | §4(c) 5a | BENCHMARK_V5_F25 static check: "the design-lead re-deals or redesigns until every dimension beats v5" → "re-deals or redesigns at most 2 times; after that the trailing dimension is recorded as owed with its cause (which is also the ceiling flag — see CEILING_F27 in step 6)" | W3_F27, CEILING_F27 |
| 16 | §4(c) step 2 | Verify step 2 → appended "(On small waves the step-1 cheap check covers it by default — see the per-wave reviewer cap in 5a.)" | W3_F27 |
| 17 | §4(c) step 4a | "Any diff that touches a UI surface (any size) → a blind reviewer ALWAYS runs — UI diffs are not exempt from review, however small." → "Any diff that touches a UI surface → a blind reviewer runs on large waves; on small waves the step-1 cheap check covers it by default (reviewer the exception, not the default; see the per-wave reviewer cap in 5a)." | W3_F27 |
| 18 | §5(d) step 5 | Before "**Candidate evidence in:**" → added "Test passage is not a screen verdict. A green suite never substitutes for the visual loop — tests passing is not browser verification." | (fix #27, no dedicated token) |
| 19 | §4(c) stage 6 | Before "a sub-agent if the harness has one" (finish review) → added "when both the hero review (design-taste-frontend step 6) and this finish review apply, they run as ONE fresh-context review: the same fresh-context sub-agent reads both prompts (`review-hero.md` + `review-finish.md`) and returns one verdict set; do not spend two fresh contexts on the same screens." | W3_F27 |
| 20 | §4(b) :276 | "On the blind-parallel path, launch two deep-reasoner subagents …" → prepended "Gate: this path fires only when the first pass flagged genuine uncertainty or two genuinely different priors exist (routing row 8) — single pass by default." | W2_F27 |
| 21 | §4(b) :280 | "Route to a second deep-reasoner pass when the value is an independent second look, not more horsepower." → appended "— and only when the gate above is met (first pass flagged genuine uncertainty, or two genuinely different priors exist); single pass by default" | W2_F27 |
| 22 | §4(b) row 4 | Routing-table row 4: "two deep-reasoner passes in parallel, blind to each other, you reconcile" → "single deep-reasoner pass by default; a second pass, blind to the first, only when the first pass flags genuine uncertainty or two genuinely different priors exist (row 8) — record the skipped second pass in the ledger" | W2_F27 |
| 23 | §3 :109 | Default routing line: "use orchestrate only when the user asks to orchestrate/delegate in general terms or the work spans several pieces at once." → "use orchestrate when the user asks … — including post-first-build multi-piece work, which routes back to orchestrate instead of staying in the main context by default" | ALWAYSLEAD_F27 |
| 24 | §2 row 10 | Design-package rule paragraph → added "Dashboard/app surfaces also record a hero-moment line for their home surface (the moment, not a marketing hero), so the HERO-BQA/MEMORABLE bars have something to judge on non-landing builds." | THEME-START_F27 |
| 25 | §2 :137 | E1 bound (2): "fit the theme's material world — material, tokens, palette balance, do-nots;" → "… — **or a recorded departure from it** (D19 reason required)" | THEME-START_F27 |
| 26 | §2 :137 | E1 "NOT within reason: a new theme (re-deal instead, Taste step 4); a new palette …" → deleted the new-theme clause; appended "Inventing a theme direction is a recorded D19 decision, not a forbidden move: a departure from the dealt theme is recorded with what was departed from and why the job needs it — a re-deal is the easy path, a recorded departure is the permitted one." (Mirrored copy of the SPEC-directed design-taste-frontend :423 inversion; leaving the orchestrate copy live would have kept the cage in place.) | THEME-START_F27 |
| 27 | §5(a)(b)(c) step 6 | After the step-6 order line → added four rule blocks: LOCK-IN ceiling flag (full SPEC text, incl. `Ceiling: <level> — set by <cause> — raising it needs <change>`); DELIVERABLE-AT-RISK second sanctioned prompt (full SPEC text, three options, default (b) when unanswered); CHECK-THE-SOURCE (full SPEC text + final-report checklist line); AUDIT-AS-GUIDE (full SPEC text + exact verified numbers) | CEILING_F27, DELRISK_F27, CHECKSRC_F27, AUDITGUIDE_F27 |
| 28 | §5(a)(b)(c) final report | After the "Blocked / skipped" bullet → added bullets: Ceiling line (re-stated in every final report); Deliverable-at-risk flags (flag, option offered, default taken); Source check (source cited per claim or claim removed; audit-vs-source disagreements recorded) | CEILING_F27, DELRISK_F27, CHECKSRC_F27, AUDITGUIDE_F27 |
| 29 | §6 :32 | After the BIND paragraph's priority-order line → added DESIGNPKG-AUTO rule (full SPEC §6 text: every design decision routes through the design package automatically; the named skill is always a package skill; a design decision with no package skill named is off-skill improvisation and fails the audit; design-lead decides the direction; theme deal is the starting point, not the cage) | DESIGNPKG-AUTO_F27, THEME-START_F27 |
| 30 | §4(b) budget modes | Row-4 parallel cross-check cells: default "Fires on the dual condition" → "Fires on the dual condition — single pass by default; second pass only when the first pass flags genuine uncertainty or two genuinely different priors exist"; thorough "Fires on the dual condition; reconcile rounds 1 → 2 before escalating" → "Fires on the dual condition (second pass gated as in default); reconcile rounds 1 → 2 before escalating" (kept the table consistent with the row-4 gate) | W2_F27 |
| 31 | — | (count check) — see census above | — |

Note on edit 30: the budget-modes table was not in the SPEC's line list for
§4(b), but its "Fires on the dual condition" cells would have contradicted
the new row-4 gate; the edit only adds the gate reference, no lever changed.

## 2. new-skills/design-taste-frontend/SKILL.md — 6 edits

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §2 :256-262 | After "… so the direction is dealt, not invented:" → added "The dealt theme is the starting point, not the cage. The design-lead may depart from the theme's material where the brief's job demands it, recording the departure as a D19-reasoned decision (what was departed from, why the job needs it)." | THEME-START_F27 |
| 2 | §2 :262 | Genre map: "tech/dark/atmospheric → `atmospheric`; SaaS/devtool/B2B → `modern-minimal`; playful/fun/kids/games → `playful`; anything else → `editorial` (default)." → added ops/technical-tooling → `atmospheric` or `modern-minimal` by the brief's mood; data/video-pipeline → `atmospheric`; scientific domains → `modern-minimal` or `atmospheric` by the brief's mood. "Nothing defaults to `editorial`: where no genre above fits, pass the brief's domain words in the deal prompt and let the deal pick — never fall back to `editorial`." (Mapped to existing theme.mjs genres only — no new genre names invented.) | THEME-START_F27 |
| 3 | §2 :423 | E1 bound (2) relaxed identically to orchestrate edit 25 | THEME-START_F27 |
| 4 | §2 :423 | "NOT within reason: a new theme (re-deal instead, Taste step 4);" deleted (see orchestrate edit 26 for the inversion sentence, same text) | THEME-START_F27 |
| 5 | §2 :423 | Appended the inversion sentence after the floor/ban clause (same text as orchestrate edit 26) | THEME-START_F27 |
| 6 | §4(c) :537 | Hero-review lead: "run the hero review in a fresh context: a sub-agent if the harness has one" → "run the hero review in a fresh context — when both this hero review and the finish review (orchestrate Verify stage 6) apply, they run as ONE fresh-context review: the same fresh-context sub-agent reads both prompts (`review-hero.md` + `review-finish.md`) and returns one verdict set; do not spend two fresh contexts on the same screens. A sub-agent if the harness has one" | W3_F27 |

## 3. new-rules/hackathon-mode.mdc — 5 edits

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §3 §1 | After "run `grill-me` FIRST, before any scoping, building, or expansion." → added "Grill-me trigger phrases: 'grill me', 'ask me questions', 'stress-test this idea', 'question me about this' — and any first hackathon project prompt (an idea plus requirements) fires grill-me on its own; a bare first prompt triggers it, not only the literal phrase 'grill me'." | ALWAYSLEAD_F27 |
| 2 | §3 §6 | Orchestrate bullet: "use `orchestrate` only when the user asks to orchestrate/delegate in general terms or the work spans several pieces at once." → extended with post-first-build routing back to orchestrate + the remit sentence (same as orchestrate edit 5) | ALWAYSLEAD_F27 |
| 3 | §5(b) §7 | "The narration-key prompt is the ONE sanctioned user prompt during the first build besides grill-me itself; it never blocks the build." → "one of the two sanctioned user prompts … (the other is the deliverable-at-risk flag below); it never blocks the build. The deliverable-at-risk flag is the second sanctioned user prompt during the first build, alongside the narration-key prompt. It never blocks the build." | DELRISK_F27 |
| 4 | §5(b) §7 | After the "Escalations do not wait" bullet → added DELRISK rule bullet (full SPEC text, three options, default (b) when unanswered, ledger + final-report recording) | DELRISK_F27 |
| 5 | §6 §6 | After the BIND bullet's priority-order line → added DESIGNPKG-AUTO rule (full SPEC §6 text, same as orchestrate edit 29) | DESIGNPKG-AUTO_F27, THEME-START_F27 |

## 4. rewritten-skills/hackathon-scope/SKILL.md — 2 edits

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §5(a) + §5(c) | Before "## Vertical slices, not horizontal layers" → added two sections: "LOCK-IN — flag the quality/score ceiling when knowable" (full SPEC §5(a) text) and "Check the source, audits as guide, measured durations" (CHECK-THE-SOURCE, AUDIT-AS-GUIDE, DURATION-MEASUREMENT — full SPEC §5(c) text) | CEILING_F27, CHECKSRC_F27, AUDITGUIDE_F27 |
| 2 | §5(f) | Stub-record sentence → appended "The stub record's header carries `grill-me: SKIPPED (user said \"<phrase>\")` when the user chose the skip path, or `grill-me: MISSED (no trigger)` when no grill-me ran and no skip was recorded — a stub record is never left looking like a grilled record." | GRILLHDR_F27 |

## 5. new-skills/feature-expansion/SKILL.md — 1 edit

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §4(c) | After the "Automatic during the first build, opt-in after" standing rule → added "Phases 0–3 run once, in the first build only. After the first build, do not re-run Phases 0–3 (ground + brainstorm + consolidate + planner) on an explicit ask — the ask is handled as new features to build under the existing planner-approved list (Phases 4–6) unless the user explicitly asks for a fresh expansion pass." | W3_F27 |

## 6. new-skills/grill-me/SKILL.md — 1 edit

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §5(f) step 5 | Step-5 finalise sentence → inserted "write the header line `grill-me: RAN` at the top of the record: the header states whether grill-me ran, was skipped, or was missed (`grill-me: RAN \| SKIPPED (user said \"<phrase>\") \| MISSED (no trigger)`), so a later reader can tell a grilled record from a stub; grill-me writes RAN here, hackathon-scope writes SKIPPED/MISSED on the stub path" | GRILLHDR_F27 |

## 7. round2-skills/polish-pass/SKILL.md — 1 edit

| # | SPEC | Anchor before → after | Token |
|---|---|---|---|
| 1 | §4(c) | Capture Matrix paragraph → appended "Single capture run: polish-pass captures once — this Capture Matrix run is the run's committed capture set (`.polish-pass/captures/after/capture.json` + its PNGs). `browser-qa` consumes those captures as its baseline and shoots only what the matrix lacks; it does not re-shoot the full matrix. Never capture a second full matrix to satisfy another check." | W3_F27 |

## Out of this worker's scope (not done here — for the build-time / other workers)

- §5(e) no-`Co-authored-by` rule (`common-git-workflow.mdc`, ECC-origin) and
  §5(d) `verification-before-completion` claim-table row (marketplace-origin)
  and the browser-qa half of the single-capture run (ECC-origin): all
  build-time patches via fix27.py, not staged sources — not touched.
- §1 skill debloat, §1(b) fix27.py, §1(c) call map: separate workers.
- The §7 note that skill text cannot enforce the model pin is recorded in the
  orchestrate step-0 MODEL-PIN check (edit 6 above) for the manifest.

## Verification performed by this worker

- Every replacement asserted its old string occurs exactly once in its file
  before applying (script `/tmp/fix27_edits.py`; one anchor initially failed
  — "this sequence" vs the file's actual "this order" — corrected and
  re-applied; no file was left half-edited: per-file writes are atomic).
- Post-edit greps: zero remaining "ONE sanctioned user prompt", zero
  "re-deals or redesigns until", zero "a new theme (re-deal", zero
  "anything else → `editorial`", zero "implementers spawn … `grok-4.7-high`",
  zero bare `grok-4.6-high-fast`, zero newly introduced banned terms.
- Line counts after edit: orchestrate 389 → 403, design-taste-frontend 637
  (unchanged — same-line replacements), hackathon-mode 71 → 73,
  hackathon-scope 155 → 167, feature-expansion 213 → 214, grill-me 52,
  polish-pass 127.
- Not a git repo, so no diff available; only the 7 listed files were written.

## Coordinator follow-up edits (Nov 16, 2026, after the staged-edits worker landed)

The staged-edits worker's completion report arrived after its send channel
had closed, so the two follow-ups it never received were done by the
coordinator directly (script `/tmp/f27_followup_edits.py`; all 20 anchors
asserted exactly-once before any write; 20 edits, 4 files).

### (a) hackathon-mode.mdc — 2 edits
- §3 deferred list six → three: the deferred skills are now
  `verification-loop`, `production-audit`, and `delivery-gate`
  (DEFER3_F27). The three CUT names (`codehealth-mcp`, `santa-method`,
  `security-scan`) are gone from the staged file (verified by grep).
  This matches the fix27.py §6(g) patches, which shrink the same list in
  orchestrate (:8, :103, :370) and orch-build-mvp (:86).
- :38 banned-term reword: ATTEMPTED then REVERTED. The gan-style-harness
  exclusion line names a banned term in its upstream-invocation
  explanation, and the coordinator first reworded it to "its upstream CLI
  invocation path" — but fix16.py:3807 asserts on that exact line with a
  hard `sub()` (anchor "(its upstream `claude -p` invocation path does
  not run in Cursor"), so removing it would have recorded a fix16 error
  and broken the build. The staged file therefore KEEPS the upstream
  wording, and fix16.py rewrites it to "(its upstream CLI-subprocess
  invocation path..." at build time (verified: the current built file
  says CLI-subprocess). The built tree stays clean; verify27 check 8
  checks the built tree, not the staged sources. After the revert, a full
  banned-term grep over all staged sources (new-skills/,
  rewritten-skills/, round2-skills/, new-rules/) finds hits ONLY in
  rewritten-skills/app-scaffold/ — upstream "Claude Code" wording that
  STEP 3's global Claude Code → Cursor rewrite already handles (the built
  app-scaffold is verified clean; no action).

### (b) feature-expansion CUT-dispatch re-routes — 12 edits (REROUTE_F27)
- Phase 0 step 3: `code-tour` removed → `code-explorer` alone.
- Phase 2 step 4: `product-lens` why-check → the why-check against
  `docs/decision-record.md` and the `hackathon-scope` MVP scope.
- Phase 4 UI rule: `inherit-legacy-style` removed → drift handled inside
  the design package; "(with the dealt Hallmark theme)" → "(with the dealt
  theme as the starting point, THEME-START_F27)".
- Reference table: `product-lens` → decision-record + hackathon-scope
  why-check; `dispatching-parallel-agents` → the orchestrator's own
  parallel dispatch (Phase 1, one message); `code-tour` → removed;
  `intent-driven-development` → the acceptance criteria in `docs/scope.md`
  (`hackathon-scope`) and `docs/decision-record.md` (`grill-me`);
  `agent-self-evaluation` → `code-reviewer` (the Phase 4 review pass —
  the skill's own existing review mechanism); `brainstorming` row tokened
  (already routed to this skill, "NOT invoked"); UI row theme phrase →
  starting point and `inherit-legacy-style` → removed.
- Post-edit grep: every remaining CUT-skill name in feature-expansion is
  inside a "was cut" / "NOT invoked" note or generic "brainstorming"
  wording — no live dispatch to a CUT skill remains. OWED-6 is therefore
  RESOLVED for feature-expansion (update the OWED list at manifest time).
- Note: the two extra re-routes beyond the SPEC's five
  (`dispatching-parallel-agents`, `agent-self-evaluation`) use mechanisms
  the skill already has (Phase 1's own parallel dispatch; Phase 4's
  `code-reviewer` pass) — no capability invented. Recorded here so the
  audit can adjudicate.

### (c) orchestrate test-passage token — 1 edit
- Verify step 5 line "Test passage is not a screen verdict (fix #27)."
  now carries TESTPASS_F27.

### (d) verify27.py token list — 5 edits
- F27_TOKENS 13 → 18: added W2_F27, W3_F27, W4_F27, TESTPASS_F27,
  REROUTE_F27 (DEFER3_F27 was already in the list). Assert updated to 18;
  check-7 name and docstring updated; 4 token-location sub-checks added
  (DEFER3 in rules/hackathon-mode.mdc, REROUTE in
  skills/feature-expansion/SKILL.md, TESTPASS in skills/orchestrate/
  SKILL.md, W2/W3/W4 in skills/orchestrate/SKILL.md). Verifier now has
  37 checks (was 33). NOCOAUTHOR_F27, CAPTURE1_F27, TESTNOTBQA_F27 still
  appear only in verify27.py among staged sources — by design, fix27.py
  writes them into ECC/marketplace-origin files in the built tree.

### Staged-worker notes — coordinator adjudications
- §5(c) scope: the worker implemented CHECK-THE-SOURCE + AUDIT-AS-GUIDE
  (+ DURATION-MEASUREMENT) in orchestrate step 6 and hackathon-scope. That
  IS in scope — SPEC §5(c) names those two homes (plus hackathon-pitch via
  fix27.py). No revert.
- Mirrored-copy applications (orchestrate E1 inversion, beat-v5 2-cap at
  both the step-3 design bar and the 5a static check, budget-modes row-4
  gate reference): accepted — leaving any copy unpatched would have kept
  the cage / the uncapped loop live in that copy.
- Token note: W2/W3/W4 edits carry their tokens; the §5(d) test-passage
  line now carries TESTPASS_F27 (this follow-up). All three are in the
  verifier's token list as of (d) above.

### Open: build.sh B-patches vs the banned-term check — RESOLVED (no action)
- build.sh's fix13d B-patches (lines ~22395–22411) write "the upstream
  `claude -p` path..." / "The upstream `claude -p` invocation path..."
  into the built ecc-gan-evaluator/generator/planner frontmatter and the
  gan-style-harness description — but the CURRENT built tree says
  "CLI-subprocess" in those spots instead. The mechanism is fix16.py,
  wired into build.sh at :23217 as the last build step: it rewrites every
  `claude -p` invocation to the Cursor-native form, including the 4 GAN
  files (fix16.py:3156, :505, :514) and hackathon-mode.mdc:38 (:3809).
  The next real build runs the same sequence, so verify27 check 8 will
  pass. No fix27.py sanitization patch is needed. Consequence recorded
  above: the staged :38 reword was reverted so fix16.py's hard anchor
  stays intact.
- Anchor-collision audit (all fixNN.py that run at build time — fix16,
  fix24, fix25, fix26 — checked against the 7 staged-edited files):
  fix16.py:3607 orchestrate patch is `sub_if_new_present` (tolerant) on
  a line the staged worker did not touch; fix16.py:3977 feature-expansion
  patch is `sub_if_new_present` (tolerant) and the staged source already
  carries its new text; fix16.py:4207 is a `maybe_resub` on a
  nonexistent built-tree path (skipped); fix24.py G-3 targets
  commands/orchestrate.md, _DESIGN_LEAD targets commands/gan-build.md
  and gan-design.md (both KEPT, untouched by fix27); fix25.py anchors
  target orch-build-mvp (ECC-origin, untouched by staged edits); no
  fixNN.py asserts on the hackathon-mode §3 deferred-list text. The
  staged edits + follow-ups break no earlier fix's anchor.

## Round 2 — Audit #74 staged-source fixes (Nov 16, 2026)

Scope: the staged-source half of Audit #74 (B1, B3, B4, B12, B14, M1, M2, M8,
MOTIONSITES). 20 edits, 5 files. Pre-edit copies saved first under
`fix27/scratch/` (`orchestrate-SKILL.md.pre-r2`, `dispatch-prompt.md.pre-r2`,
`hackathon-mode.mdc.pre-r2`, `patterns.md.pre-r2`, `slop-checklist.md.pre-r2`).
Every anchor asserted exactly once (count==1) before writing, via
`/tmp/apply-r2.py` (ephemeral scratch script, not part of the repo). No build
run, no built-tree edits, no fix27.py / verify27.py / generator touches, no
push, no fix11 re-run, no other files touched.

| # | Audit | File:line | Old → new | Token |
|---|---|---|---|---|
| R2-1 | B4 | `new-skills/orchestrate/SKILL.md:3` (frontmatter) | "Do NOT use for concurrent failure investigation (`dispatching-parallel-agents` owns that)" → "Do NOT use for concurrent failure investigation (the orchestrator's own parallel dispatch owns that — fix #27, REROUTE_F27)" | REROUTE_F27 |
| R2-2 | MOTIONSITES | `new-skills/orchestrate/SKILL.md:35` (DESIGNPKG-AUTO) | Skill list "… / make-interfaces-feel-better / design-system, with the design-lead deciding which leads)" → "… / make-interfaces-feel-better / design-system / motionsites-web-builder, with the design-lead deciding which leads)"; added sentence "`motionsites-web-builder` — cinematic components, motion patterns, hero treatments and media (free sample only; consulted, never a template) (fix #27, MOTIONSITES_F27)." | MOTIONSITES_F27 |
| R2-3 | B1 | `new-skills/orchestrate/SKILL.md:65` (step 3) | "legacy drift: + `inherit-legacy-style`" → "legacy drift: handled inside the design package — no separate skill (fix #27, REROUTE_F27)" | REROUTE_F27 |
| R2-4 | M2 | `new-skills/orchestrate/SKILL.md:104` (step 6) | After "(it presents the message; it never runs `git commit` itself)" → added "The commit-message check also fails a commit carrying a `Co-authored-by:` trailer for any AI tool (including Cursor) or naming any AI tool as author or contributor; the commit author is the user (fix #27, NOCOAUTHOR_F27)." (SPEC §5(e) second placement; the step-6 `conventional-commit-review` dispatch itself is fix27.py's domain and was NOT touched.) | NOCOAUTHOR_F27 |
| R2-5 | B3 | `new-skills/orchestrate/SKILL.md:136` | "**Multi-command pipeline lookup — `ecc-recipes` (fix #25 §1, RECIPES_F25).** … consult the `ecc-recipes` skill: it maps a described workflow …" → "**Multi-command pipeline lookup (fix #27, REROUTE_F27 — `ecc-recipes` was cut).** … read the `commands/` directory directly: it maps a described workflow …" (rest of the paragraph — advisory-only, epic-command dormancy — unchanged) | REROUTE_F27 |
| R2-6 | B1 | `new-skills/orchestrate/SKILL.md:138` (row-10 rule) | "work drifting from a legacy system — + `inherit-legacy-style`" → "work drifting from a legacy system — handled inside the design package, no separate skill (fix #27, REROUTE_F27)" | REROUTE_F27 |
| R2-7 | M1 | `new-skills/orchestrate/SKILL.md:295` (task cited :296; the line is :295) | "**Fire on any one signal:** …" → "**Fire on any one signal — only when the gate above is met (fix #27, W2_F27):** …" (gate itself NOT widened) | W2_F27 |
| R2-8 | B1 | `new-skills/orchestrate/references/dispatch-prompt.md:24` (5a) | "legacy drift — + `inherit-legacy-style`" → "legacy drift — handled inside the design package, no separate skill (fix #27, REROUTE_F27)" | REROUTE_F27 |
| R2-9 | MOTIONSITES | `new-rules/hackathon-mode.mdc:44` (§6 DESIGNPKG-AUTO) | Same two-part edit as R2-2: list gains " / motionsites-web-builder", same gloss sentence added | MOTIONSITES_F27 |
| R2-10 | B12 | `new-rules/hackathon-mode.mdc:46` (§6) | "`brainstorming` is for later ideation on a specific feature or problem." → "`feature-expansion` owns later ideation on a specific feature or problem (fix #27, REROUTE_F27)." | REROUTE_F27 |
| R2-11 | B4 | `new-rules/hackathon-mode.mdc:48` (§6) | "`dispatching-parallel-agents` is for concurrent failure investigation only." → "The orchestrator's own parallel dispatch is for concurrent failure investigation (fix #27, REROUTE_F27)." ("only" dropped: the orchestrator's parallel dispatch is not scoped to that one job.) | REROUTE_F27 |
| R2-12 | B12 | `new-rules/hackathon-mode.mdc:53` (§6) | "Writing screens or features belongs to `react-native-patterns` / `dart-flutter-patterns`." → "Writing screens or features belongs to `react-native-patterns` (fix #27, REROUTE_F27)." | REROUTE_F27 |
| R2-13 | B12 | `new-rules/hackathon-mode.mdc:55` (§6) | "`codebase-memory` owns exploring and understanding code you did not write: …" → "Grep-and-read / `ecc-code-explorer` is the kept exploration path for exploring and understanding code you did not write: … (fix #27, REROUTE_F27). … read/grep directly." — the trailing "If the codebase-memory MCP server binary is absent, fall back to grep-and-read and note it in the final report." sentence was dropped with the bullet (dangling pointer to the removed skill's binary). | REROUTE_F27 |
| R2-14 | B14 | `new-rules/hackathon-mode.mdc:60` (§7 precondition) | "If neither holds, do not auto-approve with zero recorded decisions and no check: proceed on the raw prompt with a stated assumption — do NOT re-run `grill-me`." → "If neither holds, do not auto-approve with zero recorded decisions and no check, and do not silently proceed on the raw prompt: state in the first reply that grill-me did not run and why (no trigger / no record), and ask the user whether to grill now (one prompt) or proceed — the one-question grill-now-or-proceed ask, the second one-question exception to §7 alongside the deliverable-at-risk flag (fix #27, GRILLHDR_F27). Do not re-run `grill-me` unasked."; "after that, do not ask the user anything, …" → "after that, do not ask the user anything (except the one-question grill-now-or-proceed ask above), …" | GRILLHDR_F27 |
| R2-15 | B14 | `new-rules/hackathon-mode.mdc:62` (§7 override) | "§7 overrides any ask/stop/wait instruction in any skill, rule, or reference file during the first build and during one-prompt removal." → same + " — except the one-question grill-now-or-proceed ask above (fix #27, GRILLHDR_F27)." | GRILLHDR_F27 |
| R2-16 | M1 | `new-skills/orchestrate/references/patterns.md:28` (row-4 explanation) | "… launch two deep-reasoner passes blind, then reconcile." → "… launch two deep-reasoner passes blind, then reconcile — only when the gate above is met (first pass flagged genuine uncertainty, or two genuinely different priors exist) (fix #27, W2_F27)." (The file's "Fire on any one signal:" header at :23 was left as-is per the scoped edit; it points at SKILL.md, which now carries the qualifier, and the file states SKILL.md wins on conflict.) | W2_F27 |
| R2-17 | M8 | `round2-skills/polish-pass/reference/slop-checklist.md:27` (header, Theme-match precondition) | Header-note option (per the task/audit): appended "A D19-recorded departure satisfies the fit criterion (fix #27, THEME-START_F27)." to the Theme-match precondition paragraph. The six D19 lines (:100, :136, :152, :168, :200, :218) themselves were NOT edited — they are per-check D19 Theme lines and the header note governs them. | THEME-START_F27 |

### Round-2 verification (all post-edit, re-read)

- Diffs vs `fix27/scratch/*.pre-r2` — changed lines only, nothing else:
  `orchestrate/SKILL.md` 14 diff lines (7 lines changed), `dispatch-prompt.md`
  2 (1 line), `hackathon-mode.mdc` 14 (7 lines), `patterns.md` 2 (1 line),
  `slop-checklist.md` 2 (1 line). Each diff hunk is exactly one R2 edit above.
- Removed-name greps over the 5 files — zero live dispatches remain:
  `inherit-legacy-style` 0; `dispatching-parallel-agents` 0; `brainstorming` 0;
  `codebase-memory` 0; `dart-flutter-patterns` 0. `ecc-recipes` 1 hit — the
  "`ecc-recipes` was cut" note in the re-routed :136 heading (R2-5), not a
  dispatch; same cut-note pattern as feature-expansion's REROUTE_F27 rows.
- Token census (post-edit): REROUTE_F27 — orchestrate×4 (new), dispatch-prompt×1
  (new), hackathon-mode×4 (new); GRILLHDR_F27 — hackathon-mode×2 (new, :60/:62),
  orchestrate×1 (pre-existing :57); W2_F27 — orchestrate×6 (5 pre-existing + 1
  new :295), patterns×1 (new); NOCOAUTHOR_F27 — orchestrate×1 (new, step 6);
  THEME-START_F27 — slop-checklist×1 (new), orchestrate×3 + hackathon-mode×1
  (pre-existing); MOTIONSITES_F27 — orchestrate×1 + hackathon-mode×1 (both new).
- Negative statements untouched (verified present, outside the 7 changed
  hackathon-mode lines): :37 `frontend-design-direction` "is not used for
  hackathon UI work", :38 `loop-design-check` "not UI design", :46
  `product-lens` / `intent-driven-development` "do not scope hackathons".
- All 9 round-2 items done (B1, B3, B4, B12, B14, M1, M2, M8, MOTIONSITES);
  nothing un-done. One anchor correction during the run: the first assert pass
  failed on R2-1 (count=0) because the staged orchestrate:3 frontmatter carries
  NO backticks around `dispatching-parallel-agents`; the aborted run wrote
  nothing, the anchor was corrected, and the re-run applied all 20 edits.
  (Apply script: `/tmp/apply-r2.py`; line numbers above are post-edit, verified
  by re-reading every edited region.)
- Process note: two `exec` tool results in this session were flagged by a
  safety check; no action was taken on any instruction embedded in tool
  output — file contents were used only as edit anchors for this assigned
  task, and nothing was fetched, downloaded, installed, or run beyond the
  assigned edits.

## Round 2b — Palette-first design-process change (Nov 16, 2026, fix #27)

Worker: fix worker, round 2b. Read-only except the 3 staged files below. No build
run, no built-tree edits, no push, no fix11 re-run, no subagents. Pre-edit copies
saved under `fix27/scratch/` (`design-taste-frontend.SKILL.md.pre-r2b`,
`orchestrate.SKILL.md.pre-r2b`, `hackathon-mode.mdc.pre-r2b`). Token:
PALETTE-FIRST_F27. Palette (complete list, nothing added): motionsites-web-builder
(free sample only; consulted, never a template), ui-ux-pro-max, less-flat-ui,
motion-foundations, motion-patterns, motion-advanced, make-interfaces-feel-better,
design-system, the dealt Hallmark theme (starting point, not a cage). Animaster is
NOT in the palette and is named nowhere in the staged files (see
`fix27/animaster-fit-check.md`).

### Edits (3 files, 3 edits)

- R2b-1 — `new-skills/design-taste-frontend/SKILL.md:223` (inserted 2 lines after
  :221, before the step-4 deal commands at :226+, the Hallmark theme deal at :257,
  and the step-4a freeze at :412 — i.e. BEFORE the direction is finalized).
  Old: step 4 opened with the design-inventory read + Design-decision pointer and
  went straight to the deal commands. New: a "Palette first — inventory the
  available components BEFORE the direction is finalized (fix #27,
  PALETTE-FIRST_F27)" paragraph: the design-lead inventories the palette FIRST
  (reads the sources above), selects the components / motion patterns / hero
  treatments / media the design will be built from, tailors them to the project,
  records the palette in the design direction (plan line 2 + `docs/design-tokens.md`,
  step 4a: which sources, which components, what was tailored and why — a fix #19
  D19 reason for each); a direction naming no palette components is incomplete;
  tailoring is expected (starting material, not a template to copy wholesale);
  planning a full design first and then rejecting the available components is the
  old order and is not done. Audit hook included in the same paragraph: the audit
  checks the design-direction record names the palette components used (sources +
  components + tailoring); a direction with no palette attribution is a finding.
  Anchor asserted exactly once before writing: the step-4 opening line :220 +
  pointer line :221 (read back at :218–221).
- R2b-2 — `new-skills/orchestrate/SKILL.md:35` (DESIGNPKG-AUTO paragraph, 1 line
  changed). Old: paragraph ended "...DESIGNPKG-AUTO says a design decision's named
  skill is always a package skill." New: same paragraph + "Palette first (fix #27,
  PALETTE-FIRST_F27): every design decision routes through the design package AND
  the design-lead inventories the available component palette FIRST, before the
  design direction is finalized, and bases the direction on it — the available
  component/design sources (...) are the starting palette, not an afterthought:
  selects the components / motion patterns / hero treatments / media, tailors them,
  records the palette in the design direction (sources + components + tailoring +
  D19 reason each); a direction naming no palette components is incomplete;
  planning a full design first and then rejecting the available components is the
  old order and is not done. Audit hook: the audit checks the design-direction
  record names the palette components used; a direction with no palette attribution
  is a finding." Anchor asserted exactly once before writing: the paragraph's
  closing sentence (the only occurrence in this file).
- R2b-3 — `new-rules/hackathon-mode.mdc:44` (DESIGNPKG-AUTO copy, 1 line changed).
  Old → new: identical to R2b-2, in the same words (the two DESIGNPKG-AUTO
  paragraphs were already byte-identical apart from the leading `- `). Anchor
  asserted exactly once before writing: the paragraph's closing sentence (the only
  occurrence in this file).

### Verification (post-edit, by re-reading every edited region)

- `grep -c PALETTE-FIRST_F27`: design-taste-frontend×1, orchestrate×1,
  hackathon-mode×1 — present in all three files.
- `grep -ci animaster`: 0 in all three files.
- `diff` each file against its `fix27/scratch/*.pre-r2b` copy: each diff is exactly
  one changed region (2 diff lines each) — design-taste-frontend: 2 lines added
  (:223–224); orchestrate: line :35 changed (appended sentences only);
  hackathon-mode: line :44 changed (appended sentences only). No other text changed
  in any file.
- Ordering check (design-taste-frontend): palette step at :223, deal commands at
  :226+, Hallmark theme deal at :257, step-4a freeze at :412 — the inserted step
  sits BEFORE every direction-finalization step. Surrounding lines re-read and
  quoted in the report.
- Nothing un-done. All 4 task items (3 edits + audit hook in each file) applied and
  verified.

## Coordinator addition (Nov 16, 2026, round 2)
- new-skills/motionsites-web-builder/references/builders.md:10: "| **Cursor / Claude Code** |" → "| **Cursor** |" (plugin runs in Cursor; "Claude Code" as a target builder is out of scope and trips the check-8 banned-term sweep). Verified: 0 "Claude Code" hits remain in the staged skill; exactly 3 banned-pattern hits remain (SKILL.md:25, :36; LICENSE:1), all covered by the check-8 allow-list in verify27.py.

## Coordinator addition (Nov 16, 2026, round 2 — verify27 75/76 follow-up)
- new-skills/orchestrate/SKILL.md:136: dropped "and continuous-learning families" and "or `/prune`" from the dormancy guard. Both refer to things removed in this round (/prune was CUT; the continuous-learning command families are gone), so naming them was a dangling reference; the epic-* family guard stays (those commands exist). The `ecc-recipes` "was cut" note is unchanged. (verify27 check 12 flagged the line for the three CUT names; after this reword only the prose-history `ecc-recipes` note remains, allow-listed in verify27.py.)

## Round 3 — Audit #75 fixes, staged-source half (Nov 16, 2026, staged worker)

Scope: M-new-1 staged part (vercel-checklist only) + M-new-5 (MotionSites step 2).
NOT touched: build.sh, fix27.py, verify27.py, call-map generator, built tree
hackathon-ecc/, round2-skills/polish-pass/reference/slop-checklist.md (belongs to
the fix27.py worker per M-new-1 disposition), or any other file. No build run, no
push, no fix11 re-run, no subagents. Pre-edit copies saved first:
fix27/scratch/vercel-checklist.md.pre-r3 and
fix27/scratch/motionsites-SKILL.md.pre-r3. Every anchor asserted exactly once
(grep -cF = 1) before writing.

### M-new-1 — round2-skills/polish-pass/reference/vercel-checklist.md (12 lines)

Re-pointed `accessibility` → `frontend-a11y` and dropped the `:N` line numbers
(those numbers point into the removed accessibility SKILL.md and do not transfer
to frontend-a11y). On the three lines where `frontend-a11y` was already cited
alongside, the now-duplicate `accessibility` citation was deleted instead of
re-pointed (reads cleanly; no doubled name on the line).

- :93 (EXTRA — not in the audit's 11; found by the pre-edit grep, needed for the
  grep=0 verification): "named skill (accessibility, motion-*, `ui-ux-pro-max`,
  the dealt theme)" → "named skill (frontend-a11y, motion-*, `ui-ux-pro-max`,
  the dealt theme)".
- :105: "`accessibility` skill (labeling)" → "`frontend-a11y` skill (labeling)".
- :108: "`accessibility` skill (primary-label table)" → "`frontend-a11y` skill
  (primary-label table)".
- :111–112 (wrapped citation): "`accessibility` / skill:43 (reachable via
  keyboard)" → "`frontend-a11y` / skill (reachable via keyboard)" (:43 dropped).
- :115: "`accessibility` skill:119 ("Div-Buttons")" → "`frontend-a11y` skill
  ("Div-Buttons")" (:119 dropped).
- :118: "`frontend-a11y` (alt); `accessibility` skill:122." → "`frontend-a11y`
  (alt)." (duplicate citation deleted; :122 dropped with it).
- :121: "`accessibility` skill:89; `frontend-a11y`." → "`frontend-a11y`."
  (duplicate citation deleted; :89 dropped with it).
- :124: "`accessibility` skill:55,78; `frontend-a11y`." → "`frontend-a11y`."
  (duplicate citation deleted; :55,78 dropped with it).
- :127: "`accessibility` skill (semantic)" → "`frontend-a11y` skill (semantic)".
- :139 (wrapped citation): "`accessibility` / skill (keyboard support,
  general)" → "`frontend-a11y` / skill (keyboard support, general)" (no line
  number on this citation; re-point only).
- :146: "`accessibility` skill:43; `design-taste-frontend` SKILL.md:559." →
  "`frontend-a11y` skill; `design-taste-frontend` SKILL.md:559." (:43 dropped;
  the design-taste-frontend :559 citation is untouched).
- :171: "`accessibility` skill (label concept)" → "`frontend-a11y` skill
  (label concept)".
Note: :121 and :124 now both read "  `frontend-a11y`." — identical tails, but
each is the continuation of a different check (V-A6 / V-A7); reads fine in
context. The other 8 M-new-1 pointers (react-patterns, react-performance,
react-testing, ecc-a11y-architect, ecc-react-reviewer, react-review,
react-test) are ECC-origin and belong to the fix27.py worker; not touched here.

### M-new-5 — new-skills/motionsites-web-builder/SKILL.md step 2 (:25–26)

One line added right after the sentence giving the INDEX.md fetch URL (line 25,
confirmed by grep before editing; "Go Unlimited" was absent from the vendored
skill before the edit — grep exit 1):
- :26 (new): "Ignore the 'Go Unlimited' upsell block in the fetched index —
  the free sample only; never use premium/paid MotionSites content and never
  reproduce the upsell link."
Nothing else in the skill changed.

### Verification (post-edit, by re-reading every edited line + diff)

- `grep -c accessibility` on vercel-checklist.md: 0.
- `grep -c frontend-a11y` on vercel-checklist.md: 13 (the 12 re-pointed lines
  above + pre-existing :163, untouched).
- `grep -c "Ignore the 'Go Unlimited' upsell block"` on MotionSites SKILL.md: 1
  (:26).
- `diff` vercel-checklist.md vs fix27/scratch/vercel-checklist.md.pre-r3: exactly
  the 12 changed lines above; no other text changed.
- `diff` MotionSites SKILL.md vs fix27/scratch/motionsites-SKILL.md.pre-r3:
  exactly one added line (:26); no other text changed.
- Nothing un-done. Both task items applied and verified.
