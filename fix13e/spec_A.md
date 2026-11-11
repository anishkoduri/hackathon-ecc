# Fix round #13e — Worker A spec (items 1, 8, 10)

Reframing applied throughout: `browser-qa` is the SOLE executor of pass/fail VERDICTS on rendered screens. Everything else is design guidance, candidate evidence, or a static/code-level check, worded as such, never as a screen pass/fail. No new gates, waits, or user questions are added by any spec below. No new skills/agents/rules/commands.

Target paths are given as built-tree paths under `~/workspace/hackathon-plugin/hackathon-ecc/`; staged paths are relative to `~/workspace/hackathon-plugin/`.

---

## 1A — skills/ui-ux-pro-max/SKILL.md [build.sh patch]

Re-trace: built-tree `skills/ui-ux-pro-max/SKILL.md:14` confirmed. The captivating bar states a screen "fails" and an "Enforced fail criterion (the brief names the anchor; Verify checks it as pass/fail)". No staged source exists (build.sh:265 copies from `$UIPRO_DIR`); patch at build time via the `audit_patch` block for ui-ux-pro-max files.

Anchor check: old text occurs exactly 1 time in the target file (full line 14, verified by count; the line contains the unique substring "if nothing is memorable, the surface fails even if every other check passes.").

OLD (verbatim, in a code fence):
```
**Captivating bar for dashboard/app surfaces:** the primary view must have one unmistakable visual anchor a user remembers after leaving the page. Test: after closing the page, the user can describe that one anchor — its form and what it showed — without reopening it; if nothing is memorable, the surface fails even if every other check passes. Enforced fail criterion (the brief names the anchor; Verify checks it as pass/fail): after closing the page, a user can describe that one anchor — its form and what it showed — without reopening it. If no anchor can be named, the surface FAILS.
```

NEW (verbatim, in a code fence):
```
**Captivating bar for dashboard/app surfaces (design guidance, not a screen verdict):** the primary view must have one unmistakable visual anchor a user remembers after leaving the page. Test (design guidance for the builder): after closing the page, the user can describe that one anchor — its form and what it showed — without reopening it. The brief names the anchor; Verify records whether an anchor can be named as candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable — this skill never states a screen pass/fail.
```

---

## 1B — skills/ui-ux-pro-max/SKILL.md [build.sh patch]

Re-trace: built-tree `skills/ui-ux-pro-max/SKILL.md:91` confirmed. The anti-generic bar states "if a surface looks like a default template, it fails even if every checklist item passes" and "Enforced fail criteria (the brief and Verify check these as pass/fail against the recorded named direction): (1) Direction trace — … a screen that could belong to any product fails. (2) Memorable anchor — … if no anchor can be named, the surface FAILS. (3) Not a default template — … fails even if every checklist item passes." No staged source exists (build.sh:265); patch at build time.

Anchor check: old text occurs exactly 1 time in the target file (full line 91, verified by count; the line contains the unique substring "if a surface looks like a default template, it fails even if every checklist item passes.").

OLD (verbatim, in a code fence):
```
**Anti-generic bar:** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above; if a surface looks like a default template, it fails even if every checklist item passes. Enforced fail criteria (the brief and Verify check these as pass/fail against the recorded named direction): (1) Direction trace — every primary screen visibly traces to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product fails. (2) Memorable anchor — the primary view carries the one unmistakable anchor from the captivating bar above; if no anchor can be named, the surface FAILS. (3) Not a default template — a surface that looks like a default template fails even if every checklist item passes.
```

NEW (verbatim, in a code fence):
```
**Anti-generic bar (design guidance, not a screen verdict):** avoid generic AI-dashboard aesthetics — excessive gradients, repetitive same-size cards, decorative clutter. Earn distinction through deliberate typography, spacing, alignment, and contrast, plus the one memorable anchor from the captivating bar above. Design guidance the brief and Verify record as candidate evidence for `browser-qa` (checked against the recorded named direction): (1) Direction trace — every primary screen should visibly trace to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product is candidate evidence for `browser-qa`. (2) Memorable anchor — the primary view should carry the one unmistakable anchor from the captivating bar above; if no anchor can be named, record that as candidate evidence for `browser-qa`. (3) Not a default template — a surface that looks like a default template is candidate evidence for `browser-qa`. Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail.
```

---

## 1C — skills/ui-ux-pro-max/SKILL.md [build.sh patch]

Re-trace: built-tree `skills/ui-ux-pro-max/SKILL.md:87` confirmed. The Step 2 design-system paragraph says of the Impeccable craft floor "its bans are absolute — a pinned brief never overrides a ban". A ban is a code-level proxy, not a screen verdict; qualify it so the absolute wording cannot be read as a second screen judge. No staged source exists (build.sh:265); patch at build time.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
its bans are absolute — a pinned brief never overrides a ban
```

NEW (verbatim, in a code fence):
```
its bans are absolute as static/code-level checks — a pinned brief never overrides a ban — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone)
```

---

## 8A — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]

Re-trace: built-tree `skills/polish-pass/reference/polish.md:77` (table header) and `:79` (row) confirmed; staged file is identical to the built file (diff clean). The Step 6 report template demands a "Direction-application" pass/fail column and a "Result" pass/fail, i.e. polish-pass judging direction-application. Remove that column; the template records consistency vs the recorded direction only. Direction-application is `browser-qa`'s verdict, cited not judged.

Anchor check: old text occurs exactly 1 time in the target file (lines 77–79 block, verified by count).

OLD (verbatim, in a code fence):
```
| Screen | Consistency vs recorded direction | Direction-application | Result |
|---|---|---|---|
| <screen> | <pass/fail + evidence> | <pass/fail + evidence> | <pass/fail> |
```

NEW (verbatim, in a code fence):
```
| Screen | Consistency vs recorded direction | Result |
|---|---|---|
| <screen> | <consistent / inconsistent + evidence> | <pass/fail on consistency only> |

Direction-application is `browser-qa`'s verdict, cited not judged: record it here only if `browser-qa` has already rendered it on the screen, with the verdict cited; otherwise leave it out.
```

---

## 8B — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]

Re-trace: built-tree `skills/polish-pass/reference/polish.md:81–82` confirmed; staged file identical to built. The "Generic-template findings" template section as written ("<what makes it a default template>") lets the report assert a template finding with no "only on browser-qa's verdict" qualifier. Add the qualifier; candidate evidence alone does not belong in this section.

Anchor check: old text occurs exactly 1 time in the target file (lines 81–82 block, verified by count).

OLD (verbatim, in a code fence):
```
### Generic-template findings
- <screen>: <what makes it a default template> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if none)
```

NEW (verbatim, in a code fence):
```
### Generic-template findings (only on `browser-qa`'s visual-loop verdict)
- <screen>: <`browser-qa`'s verdict + evidence> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if no `browser-qa` verdict; candidate evidence alone is recorded under Harmony check / "Still short of 10/10", not here)
```

---

## 8C — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]

Re-trace: built-tree `skills/polish-pass/reference/polish.md:24` (Step 2 item 7, harmony check) confirmed; staged file identical to built. The sentence already scopes the bar to the visual loop ("executed by `browser-qa` ONLY in the visual loop") but does not say in so many words that it is a pass/fail verdict on rendered screens. Qualify it explicitly so the "SOLE executor" claim is literally true as a screen-verdict claim.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop.
```

NEW (verbatim, in a code fence):
```
that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY, in the visual loop.
```

---

## 10A-1 — skills/polish-pass/reference/craft-floor.md [staged: round2-skills/polish-pass/reference/craft-floor.md]

Re-trace: built-tree `skills/polish-pass/reference/craft-floor.md:111` confirmed (parent cited :109 for the Bans heading; the scoping sentence is added to the :111 intro sentence, leaving the :109 heading unchanged). Staged file identical to built. The bans are code-level proxies: scope the whole Bans section as static/code-level checks whose findings are candidate evidence for `browser-qa`, not screen verdicts. This covers the parent-cited :126 (centered-everything hero template) and :130 (hero-metric template) rows, which are pattern descriptions under this intro and need no separate change. Gate logic / ban list unchanged.

Anchor check: old text occurs exactly 1 time in the target file (the :111 sentence, verified by count).

OLD (verbatim, in a code fence):
```
Each of these marks a UI as generated rather than designed. Remove or rewrite the element; do not just tone it down.
```

NEW (verbatim, in a code fence):
```
Each of these marks a UI as generated rather than designed. Remove or rewrite the element; do not just tone it down. Each ban is a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone).
```

---

## 10A-2 — skills/polish-pass/reference/craft-floor.md [staged: round2-skills/polish-pass/reference/craft-floor.md]

Re-trace: built-tree `skills/polish-pass/reference/craft-floor.md:5` confirmed: "Bans hold unless the project's design notes explicitly record an exception; accessibility and dark-pattern bans never yield." Qualify the precedence rule as a static/code-level rule, not a screen verdict.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
Bans hold unless the project's design notes explicitly record an exception; accessibility and dark-pattern bans never yield.
```

NEW (verbatim, in a code fence):
```
Bans hold as static/code-level checks unless the project's design notes explicitly record an exception; accessibility and dark-pattern bans never yield. A ban is a code-level finding and candidate evidence for `browser-qa`, never a pass/fail verdict on a rendered screen.
```

---

## 10A-3 — skills/polish-pass/reference/craft-floor.md [staged: round2-skills/polish-pass/reference/craft-floor.md]

Re-trace: built-tree `skills/polish-pass/reference/craft-floor.md:18` confirmed: "## Floor (every item must pass)". "Must pass" reads as a verdict; scope it to static/code-level checks. Checklist items themselves unchanged.

Anchor check: old text occurs exactly 1 time in the target file (the :18 heading text without its `##` marker, verified by count).

OLD (verbatim, in a code fence):
```
Floor (every item must pass)
```

NEW (verbatim, in a code fence):
```
Floor (every item must pass as a static/code-level check)
```

---

## 10B — skills/polish-pass/reference/patterns/vibe-code-tells.md [staged: round2-skills/polish-pass/reference/patterns/vibe-code-tells.md]

Re-trace: built-tree `skills/polish-pass/reference/patterns/vibe-code-tells.md:3` confirmed; staged file identical to built. The intro ("Signals that a UI was generated… This pass names every tell it finds…") does not state the tells' status. Scope them as static/code-level signals and candidate evidence, not a screen verdict.

Anchor check: old text occurs exactly 1 time in the target file (full line 3, verified by count).

OLD (verbatim, in a code fence):
```
Signals that a UI was generated and shipped without a designer's eye. Each one costs trust with any Persona who has seen a hundred AI-built apps. This pass names every tell it finds and removes the ones a polish fix covers; the rows marked "report" are restyles, so they go in the report as redesign items instead. They complement the bans in [../craft-floor.md](../craft-floor.md).
```

NEW (verbatim, in a code fence):
```
Signals that a UI was generated and shipped without a designer's eye. Each tell is a static/code-level signal and candidate evidence for `browser-qa`, not a pass/fail verdict on a rendered screen. Each one costs trust with any Persona who has seen a hundred AI-built apps. This pass names every tell it finds and removes the ones a polish fix covers; the rows marked "report" are restyles, so they go in the report as redesign items instead. They complement the bans in [../craft-floor.md](../craft-floor.md).
```

---

## 10C — skills/polish-pass/reference/patterns/vibe-code-tells.md [staged: round2-skills/polish-pass/reference/patterns/vibe-code-tells.md]

Re-trace: built-tree `skills/polish-pass/reference/patterns/vibe-code-tells.md:36` confirmed ("3. In the polish report, list each tell as a finding under Consistency, Hierarchy & clarity, or Color & theming, with its fix."). A "finding" here must not become a template verdict on its own; qualify it as a static/code-level finding and restate the browser-qa-only rule for a generic-template finding.

Anchor check: old text occurs exactly 1 time in the target file (full line 36, verified by count).

OLD (verbatim, in a code fence):
```
3. In the polish report, list each tell as a finding under Consistency, Hierarchy & clarity, or Color & theming, with its fix.
```

NEW (verbatim, in a code fence):
```
3. In the polish report, list each tell as a static/code-level finding under Consistency, Hierarchy & clarity, or Color & theming, with its fix. A tell — or three or more tells — is candidate evidence for `browser-qa`, never a generic-template finding on its own; that finding exists only on `browser-qa`'s visual-loop verdict (see scoring.md).
```

---

## 10D — skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs [staged: new-skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs]

Re-trace: built-tree `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs:2` confirmed; staged file identical to built. Scope the whole checker in its header comment: its FAIL/REFLEX/WARN grades are static-check grades on source, not pass/fail verdicts on rendered screens. Gate logic, tiers, and FAIL/REFLEX behaviour unchanged. This header scoping covers gates 2, 63, 65, and 74 (see Checked list for their re-trace); only gate 38iii gets an additional per-gate comment (10E).

Anchor check: old text occurs exactly 1 time in the target file (full line 2, verified by count).

OLD (verbatim, in a code fence):
```
/* sloplint: Hallmark's mechanical gate checker. Zero dependencies, Node 18+. Gate ids and tiers: references/gates.md. */
```

NEW (verbatim, in a code fence):
```
/* sloplint: Hallmark's mechanical gate checker (static/code-level checks on source only). Zero dependencies, Node 18+. Gate ids and tiers: references/gates.md. Its FAIL/REFLEX/WARN grades are static-check grades, not pass/fail verdicts on rendered screens — screen distinctiveness is judged only by `browser-qa` in the visual loop. */
```

---

## 10E — skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs [staged: new-skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs]

Re-trace: built-tree `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs:2963` confirmed: `report('38iii', 'FAIL', …)` inside `check38c` (:2961–2965); tier for 38iii is `reflex` (:813), so `report()` downgrades the FAIL to REFLEX (:913–916). `APP_SKIP` (:798–799) does NOT contain `38iii` (nor `2`, `74`, `63`, `65`), so gate 38iii fires in app scope. Add a code comment above the check function only; the `report()` call, its grade, and all gate logic are unchanged.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
function check38c(ctx) {
```

NEW (verbatim, in a code fence):
```
// Gate 38iii is a static/code-level check on the source (an accented word inside a heading); its FAIL/REFLEX grade is not a pass/fail verdict on a rendered screen — that verdict is `browser-qa`'s alone.
function check38c(ctx) {
```

---

## 10F-1 — skills/polish-pass/reference/scoring.md [staged: round2-skills/polish-pass/reference/scoring.md]

Re-trace: built-tree `skills/polish-pass/reference/scoring.md:43` confirmed; staged file identical to built. The Level ladder intro ("Before scoring Dimensions, place the surface on this ladder…") does not state the ladder's status. A Level placement (Level 2 = template at :47) is polish's internal scoring anchor, not a screen verdict; the Level+1 cap at :59 (10F-3) rests on it. Qualify the intro.

Anchor check: old text occurs exactly 1 time in the target file (full line 43, verified by count).

OLD (verbatim, in a code fence):
```
Before scoring Dimensions, place the surface on this ladder for its mode. It anchors the overall Score; Dimension scores explain *why* it sits there.
```

NEW (verbatim, in a code fence):
```
Before scoring Dimensions, place the surface on this ladder for its mode. It anchors the overall Score; Dimension scores explain *why* it sits there. This Level placement is an internal scoring anchor for polish's own Score, not a pass/fail verdict on a rendered screen; a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict.
```

---

## 10F-2 — skills/polish-pass/reference/scoring.md [staged: round2-skills/polish-pass/reference/scoring.md]

Re-trace: built-tree `skills/polish-pass/reference/scoring.md:54` confirmed: "any craft-floor ban … present caps overall at 7." The cap records a static/code-level finding in polish's own Score; qualify it so the cap cannot be read as a screen verdict. Scoring behaviour (the cap itself) unchanged.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
- The **overall Score is a judgment, not an average.** It's capped by the worst blocker: any Dimension ≤3 caps overall at 6; any craft-floor ban ([craft-floor.md](craft-floor.md)) present caps overall at 7.
```

NEW (verbatim, in a code fence):
```
- The **overall Score is a judgment, not an average.** It's capped by the worst blocker: any Dimension ≤3 caps overall at 6; any craft-floor ban ([craft-floor.md](craft-floor.md)) present caps overall at 7. (A ban present is a static/code-level finding; the cap records that finding in polish's own Score — it is not a pass/fail verdict on a rendered screen.)
```

---

## 10F-3 — skills/polish-pass/reference/scoring.md [staged: round2-skills/polish-pass/reference/scoring.md]

Re-trace: built-tree `skills/polish-pass/reference/scoring.md:59` confirmed: "The overall Score can't exceed the surface's Level by more than 1." Qualify the Level cap the same way as 10F-1 (Level is an internal scoring anchor, not a screen verdict). Scoring behaviour unchanged.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
- The overall Score can't exceed the surface's Level by more than 1.
```

NEW (verbatim, in a code fence):
```
- The overall Score can't exceed the surface's Level by more than 1. (Level is polish's internal scoring anchor, not a pass/fail verdict on a rendered screen.)
```

---

## 10b-1 — skills/polish-pass/SKILL.md [staged: round2-skills/polish-pass/SKILL.md]

Re-trace: built-tree `skills/polish-pass/SKILL.md:22` (harmony rule) confirmed; staged file's line 22 is identical to the built file's line 22 (the staged/built diff touches only lines 3, 15, 24, 31 — design-taste-frontend mentions added by build.sh). Same qualification as 8C: the sentence already scopes the bar to the visual loop; make the screen-verdict wording explicit.

Anchor check: old text occurs exactly 1 time in the target file (verified by count).

OLD (verbatim, in a code fence):
```
that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop.
```

NEW (verbatim, in a code fence):
```
that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY, in the visual loop.
```

---

## Checked, not changed

- `skills/ui-ux-pro-max/SKILL.md:59` — "Verify the returned domain/category… Retry once… Do not persist unverified output." Search-result verification, not a screen pass/fail. No other screen pass/fail language in the skill file (grep for fail/FAIL/pass/fail over the whole file returns only :14, :59, :91).
- `skills/ui-ux-pro-max/references/pro-rules.md`, `references/quick-reference.md` — only form/validation-failure language ("Failed forms retain inline field errors", "After failed submission…"); no screen pass/fail. `data/*.csv` rows are upstream search data, not skill prose; not patched.
- `skills/polish-pass/reference/polish.md` Step 2 item 4, Step 3, and "Still short of 10/10" — already word the generic-template diagnosis as candidate evidence for `browser-qa` with the finding existing only on its verdict; no direction-application pass/fail demand outside the Step 6 template (8A/8B) and :24 (8C).
- `skills/polish-pass/reference/craft-floor.md:126` (centered-everything hero template) and `:130` (hero-metric template) — pattern descriptions under the Bans intro; covered by the 10A-1 scoping, no separate change.
- `skills/polish-pass/reference/craft-floor.md:167–168` ("Walk the Floor checklist… Fix failures before claiming any Score improvement" / "Scan for every Ban… the polish pass is not done until it is fixed") — a fix-completion rule for the pass's own code edits and its own Score claim, not a pass/fail verdict on a rendered screen.
- `skills/polish-pass/reference/scoring.md:55` — Persona-fit cap already qualified: applies only on `browser-qa`'s visual-loop verdict; polish's own observation is candidate evidence only.
- `skills/polish-pass/reference/scoring.md:56` — vibe-code-tell cap already qualified: cap applies only on `browser-qa`'s generic-template verdict, never on tell count alone.
- `skills/polish-pass/reference/scoring.md:57` (cold-read cap) and `:58` (uncaptured-state cap) — polish's own Dimension/Score caps on its internal Score, not distinctiveness verdicts.
- `skills/polish-pass/SKILL.md:24` — generic-template FINDING exists only on `browser-qa`'s visual-loop verdict; already qualified.
- `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` gate 2 — `check2` reports `2a` FAIL (:1186, tier `floor` at :812, stays FAIL) and `2b` FAIL (:1187, tier `reflex`, becomes REFLEX); `2`/`2a`/`2b` not in `APP_SKIP` (:798–799), so they fire in app scope. Covered by the 10D header scoping; no per-gate change.
- `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` gate 63 — `check63` reports FAIL at :2461, :2462, :2463, :2474; tier `floor` (:805), stays FAIL; `63` not in `APP_SKIP`, so it fires in app scope. Covered by the 10D header scoping; no per-gate change.
- `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` gate 65 — `check65` reports FAIL at :2508; tier `reflex` (:809), becomes REFLEX; `65` is in `PAGE_ONLY` (:795) but NOT in `APP_SKIP`, so it fires in app scope. Covered by the 10D header scoping; no per-gate change.
- `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` gate 74 — CORRECTION to the parent citation: gate 74 reports `WARN`, not FAIL — `check65Tailwind` :3188 and `checkTailwind` :3834 both call `report(74, 'WARN', …)`; tier `reflex` (:816) only converts FAIL to REFLEX, so a WARN stays WARN. `74` not in `APP_SKIP`, so it fires in app scope. Covered by the 10D header scoping; no per-gate change. (Orchestrate step 6's "Fix every FAIL" therefore does not literally cover gate 74's WARNs; that wording is orchestrate's, outside worker-A items.)
- `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs:901–921` (`report()`) — the FAIL→REFLEX downgrade for reflex-tier gates is the mechanism, not verdict language; unchanged.
- `skills/browser-qa/SKILL.md:68` — "this skill is the SOLE executor of the distinctiveness bar inside the visual loop" on the ACTUAL rendered interface (Playwright, desktop + mobile). This is the canonical screen-verdict claim itself, already scoped to rendered screens; no change.
- `skills/gan-style-harness/SKILL.md:118` ("Screen distinctiveness is NOT scored here… judged ONLY by `browser-qa`"), `:123`, `:129` (rows score the recorded direction and code-level application only) — already qualified; GAN items, not worker-A items.
- `skills/design-system/SKILL.md:56` — "Scope — pattern evidence, not a distinctiveness verdict"; already qualified.
- `skills/design-taste-frontend/references/hallmark/references/gates.md:40` — "Scope — this critique is a design input, not a distinctiveness verdict"; already qualified.
- `agents/ecc-gan-evaluator.md:31`, `agents/ecc-gan-planner.md:107`, `commands/gan-design.md:19`, `commands/gan-design.md:36` — each already scopes screen distinctiveness to `browser-qa` only; GAN items, not worker-A items.
- `skills/orchestrate/SKILL.md:195` — "the distinctiveness check lives ONLY in the step-5 visual loop (`browser-qa`, the sole executor)" and "do not re-judge it here"; already visual-loop scoped (see Blocked/held for the explicit "rendered screens" wording, which belongs to the owning worker).
- `skills/orch-build-mvp/SKILL.md:40` and `:49` — "executed by `browser-qa` ONLY, in step 6's every-route visual loop" / "SOLE executor of the distinctiveness bar inside the loop"; already visual-loop scoped (see Blocked/held for the explicit "rendered screens" wording, which belongs to the owning worker).
- `skills/orch-pipeline/SKILL.md:72`, `:120` and `skills/orch-change-feature/SKILL.md:36` — bar-pass/finding references attributed to the (browser-qa) bar; held for the owning worker, not reworded here.

## Blocked / held back

- `skills/orchestrate/SKILL.md:193` — NOT spec'd by worker A (orchestrate is outside items 1/8/10; staged source `new-skills/orchestrate/SKILL.md`). It cites the ui-ux-pro-max anti-generic bar as "(ui-ux-pro-max: if a surface looks like a default template, it fails even if every checklist item passes)". Once spec 1B lands, that quoted wording no longer exists in ui-ux-pro-max — the citation goes stale. The owning worker / parent should re-point the citation at `browser-qa`'s visual-loop bar (which already carries the fail language in orchestrate:193 itself: "A design check FAILS (a finding, minor at least) when screens carry no named direction…"). Flagged, not changed here.
- `skills/orch-build-mvp/SKILL.md:40`, `:49` and `skills/orchestrate/SKILL.md:193`, `:195` — NOT qualified by worker A to the literal phrase "sole executor of pass/fail verdicts on rendered screens". They already say "SOLE executor … inside the visual loop", which is the same scope in substance, but the explicit "rendered screens" wording is left to the owning worker (these are upstream-ECC / orchestrate files outside items 1/8/10) to avoid duplicate/conflicting specs.
- No other blocks. All 17 specs above have unique anchors (count = 1, verified). No spec adds a gate, wait, user question, skill, agent, rule, or command, and no spec touches the Grok pin, anti-derivative rule, "more, not bolder" posture, CBM phrasing, deferred-six carve-out, auto-approval, or supply-chain pins.
