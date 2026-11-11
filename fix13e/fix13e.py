#!/usr/bin/env python3
"""Fix program #13e — staged-source edits (durable sources of truth).

Consolidated from worker specs A/C/D (spec_A.md, spec_C.md, spec_D.md).
Reframing: browser-qa is the SOLE executor of pass/fail VERDICTS on rendered
screens; everything else is design guidance, candidate evidence, or a static /
code-level check, worded as such, never as a screen pass/fail.

Coordinator decisions (recorded here, see MANIFEST.md):
- C4-19 + 9e MERGED into one spec (9e-merged): their OLD anchors overlap
  (C4-19's OLD is a strict substring of 9e's OLD). The merged NEW carries both
  the observations wording and the `.hallmark/candidate-evidence.md` destination.
- review-finish.md:9 copy sentence ("name any head that would pass unchanged
  on a competitor's page") CONFIRMED as a craft finding (worker D's call):
  a static copy-craft check, same family as Floor gate 19 copy tells, not a
  rendered-screen verdict.
- No seed template for `.hallmark/candidate-evidence.md`: per-project runtime
  file, created on first append; all specs read it "if it exists".

Two-phase: ALL anchors are verified count==1 across all files BEFORE any
write. On failure the script exits non-zero having written nothing. After
applying, the pre-existing build.sh (f) polish-pass patch anchors are
re-verified count==1 in the staged SKILL.md (fix13d Phase 3).
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (relative path, old text, new text, label)
SUBS = [
# ---------------------------------------------------------------- 8A (A)
("round2-skills/polish-pass/reference/polish.md",
 """| Screen | Consistency vs recorded direction | Direction-application | Result |
|---|---|---|---|
| <screen> | <pass/fail + evidence> | <pass/fail + evidence> | <pass/fail> |""",
 """| Screen | Consistency vs recorded direction | Result |
|---|---|---|
| <screen> | <consistent / inconsistent + evidence> | <pass/fail on consistency only> |

Direction-application is `browser-qa`'s verdict, cited not judged: record it here only if `browser-qa` has already rendered it on the screen, with the verdict cited; otherwise leave it out.""",
 "8A polish.md Step 6 template: consistency only"),
# ---------------------------------------------------------------- 8B (A)
("round2-skills/polish-pass/reference/polish.md",
 """### Generic-template findings
- <screen>: <what makes it a default template> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if none)""",
 """### Generic-template findings (only on `browser-qa`'s visual-loop verdict)
- <screen>: <`browser-qa`'s verdict + evidence> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if no `browser-qa` verdict; candidate evidence alone is recorded under Harmony check / "Still short of 10/10", not here)""",
 "8B polish.md Generic-template findings: verdict qualifier"),
# ---------------------------------------------------------------- 8C (A)
("round2-skills/polish-pass/reference/polish.md",
 """that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop.""",
 """that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY, in the visual loop.""",
 "8C polish.md :24 bar wording: screen verdicts"),
# ---------------------------------------------------------------- 10A-1 (A)
("round2-skills/polish-pass/reference/craft-floor.md",
 """Each of these marks a UI as generated rather than designed. Remove or rewrite the element; do not just tone it down.""",
 """Each of these marks a UI as generated rather than designed. Remove or rewrite the element; do not just tone it down. Each ban is a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone).""",
 "10A-1 craft-floor Bans intro: static checks"),
# ---------------------------------------------------------------- 10A-2 (A)
("round2-skills/polish-pass/reference/craft-floor.md",
 """Bans hold unless the project's design notes explicitly record an exception; accessibility and dark-pattern bans never yield.""",
 """Bans hold as static/code-level checks unless the project's design notes explicitly record an exception; accessibility and dark-pattern bans never yield. A ban is a code-level finding and candidate evidence for `browser-qa`, never a pass/fail verdict on a rendered screen.""",
 "10A-2 craft-floor precedence: static checks"),
# ---------------------------------------------------------------- 10A-3 (A)
("round2-skills/polish-pass/reference/craft-floor.md",
 """Floor (every item must pass)""",
 """Floor (every item must pass as a static/code-level check)""",
 "10A-3 craft-floor Floor heading: static checks"),
# ---------------------------------------------------------------- 10B (A)
("round2-skills/polish-pass/reference/patterns/vibe-code-tells.md",
 """Signals that a UI was generated and shipped without a designer's eye. Each one costs trust with any Persona who has seen a hundred AI-built apps. This pass names every tell it finds and removes the ones a polish fix covers; the rows marked "report" are restyles, so they go in the report as redesign items instead. They complement the bans in [../craft-floor.md](../craft-floor.md).""",
 """Signals that a UI was generated and shipped without a designer's eye. Each tell is a static/code-level signal and candidate evidence for `browser-qa`, not a pass/fail verdict on a rendered screen. Each one costs trust with any Persona who has seen a hundred AI-built apps. This pass names every tell it finds and removes the ones a polish fix covers; the rows marked "report" are restyles, so they go in the report as redesign items instead. They complement the bans in [../craft-floor.md](../craft-floor.md).""",
 "10B vibe-code-tells intro: static signals"),
# ---------------------------------------------------------------- 10C (A)
("round2-skills/polish-pass/reference/patterns/vibe-code-tells.md",
 """3. In the polish report, list each tell as a finding under Consistency, Hierarchy & clarity, or Color & theming, with its fix.""",
 """3. In the polish report, list each tell as a static/code-level finding under Consistency, Hierarchy & clarity, or Color & theming, with its fix. A tell — or three or more tells — is candidate evidence for `browser-qa`, never a generic-template finding on its own; that finding exists only on `browser-qa`'s visual-loop verdict (see scoring.md).""",
 "10C vibe-code-tells :36: static findings"),
# ---------------------------------------------------------------- 10D (A)
("new-skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs",
 """/* sloplint: Hallmark's mechanical gate checker. Zero dependencies, Node 18+. Gate ids and tiers: references/gates.md. */""",
 """/* sloplint: Hallmark's mechanical gate checker (static/code-level checks on source only). Zero dependencies, Node 18+. Gate ids and tiers: references/gates.md. Its FAIL/REFLEX/WARN grades are static-check grades, not pass/fail verdicts on rendered screens — screen distinctiveness is judged only by `browser-qa` in the visual loop. */""",
 "10D sloplint header: static checks"),
# ---------------------------------------------------------------- 10E (A)
("new-skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs",
 """function check38c(ctx) {""",
 """// Gate 38iii is a static/code-level check on the source (an accented word inside a heading); its FAIL/REFLEX grade is not a pass/fail verdict on a rendered screen — that verdict is `browser-qa`'s alone.
function check38c(ctx) {""",
 "10E sloplint 38iii comment: static check"),
# ---------------------------------------------------------------- 10F-1 (A)
("round2-skills/polish-pass/reference/scoring.md",
 """Before scoring Dimensions, place the surface on this ladder for its mode. It anchors the overall Score; Dimension scores explain *why* it sits there.""",
 """Before scoring Dimensions, place the surface on this ladder for its mode. It anchors the overall Score; Dimension scores explain *why* it sits there. This Level placement is an internal scoring anchor for polish's own Score, not a pass/fail verdict on a rendered screen; a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict.""",
 "10F-1 scoring Level ladder intro: internal anchor"),
# ---------------------------------------------------------------- 10F-2 (A)
("round2-skills/polish-pass/reference/scoring.md",
 """- The **overall Score is a judgment, not an average.** It's capped by the worst blocker: any Dimension ≤3 caps overall at 6; any craft-floor ban ([craft-floor.md](craft-floor.md)) present caps overall at 7.""",
 """- The **overall Score is a judgment, not an average.** It's capped by the worst blocker: any Dimension ≤3 caps overall at 6; any craft-floor ban ([craft-floor.md](craft-floor.md)) present caps overall at 7. (A ban present is a static/code-level finding; the cap records that finding in polish's own Score — it is not a pass/fail verdict on a rendered screen.)""",
 "10F-2 scoring ban cap: static finding"),
# ---------------------------------------------------------------- 10F-3 (A)
("round2-skills/polish-pass/reference/scoring.md",
 """- The overall Score can't exceed the surface's Level by more than 1.""",
 """- The overall Score can't exceed the surface's Level by more than 1. (Level is polish's internal scoring anchor, not a pass/fail verdict on a rendered screen.)""",
 "10F-3 scoring Level cap: internal anchor"),
# ---------------------------------------------------------------- 10b-1 (A)
("round2-skills/polish-pass/SKILL.md",
 """that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop.""",
 """that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY, in the visual loop.""",
 "10b-1 polish-pass SKILL.md :22 bar wording: screen verdicts"),

# ---------------------------------------------------------------- C3-1 (C)
("new-skills/orchestrate/SKILL.md",
 """**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-5 every-route visual loop on the redesigned screens BEFORE the 5c deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.""",
 """**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the 5c deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them; the redesign decision follows `browser-qa`'s verdict. If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see 5c): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy.""",
 "C3-1 orchestrate 5b: fresh verdict run + budget"),
# ---------------------------------------------------------------- C3-3 (C)
("new-skills/orchestrate/SKILL.md",
 """   - **5c. Deploy** — deploy the app (`deploy-fast`). Before the final deploy, run the `security-review` pre-deployment checklist (deploy-fast Timing rule) and record pass/blockers in the final report.""",
 """   - **5c. Deploy** — deploy the app (`deploy-fast`). Before the final deploy, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Before the final deploy, run the `security-review` pre-deployment checklist (deploy-fast Timing rule) and record pass/blockers in the final report.""",
 "C3-3 orchestrate 5c: deploy hold"),
# ---------------------------------------------------------------- C3-4 (C)
("new-skills/orchestrate/SKILL.md",
 """6. **Commit, README, then final report** — commit each landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2 auto-approves in a first build) before writing the final report;""",
 """6. **Commit, README, then final report** — commit each landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2 auto-approves in a first build) before writing the final report; if a polish-routed redesign failed re-verification, its files are not committed in this run — record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign (this is a safety hold, not a user question — it never asks the user anything).""",
 "C3-4 orchestrate step 6: commit hold"),
# ---------------------------------------------------------------- C4-1 (C)
("new-skills/orchestrate/SKILL.md",
 """**Candidate evidence in:** if `.hallmark/hero-review.md` exists, its template observations are input to your verdict (look where they point); step-6 template observations reach you the same way on re-inspection. Evidence never overrides your verdict — you make the call.""",
 """**Candidate evidence in:** `.hallmark/candidate-evidence.md` is a standing input to the visual loop: before rendering a verdict, read it if it exists in the project root and treat its entries as candidate evidence (screen + what reads as a template), never as a verdict — every producer appends there (polish-pass, design-system slop findings, Taste hero-review template observations, gates Specificity, step-6 finish-review template observations). If `.hallmark/hero-review.md` exists, its template observations are already copied there; step-6 template observations reach you the same way on re-inspection. Evidence never overrides your verdict — you make the call.""",
 "C4-1 orchestrate :193 visual-loop input: candidate-evidence.md"),
# ---------------------------------------------------------------- C4-2 (C)
("new-skills/orchestrate/SKILL.md",
 """record a Specificity score under 3 (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar (see gates.md §3).""",
 """append a Specificity score under 3 to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar (see gates.md §3).""",
 "C4-2 orchestrate :195 Specificity destination"),
# ---------------------------------------------------------------- C4-3 (C)
("new-skills/orchestrate/SKILL.md",
 """route them to `browser-qa`, which re-inspects the affected screens in the step-5 visual loop (within the existing caps) before polish/deploy, and only its verdict decides whether a fix is owed.""",
 """append them to `.hallmark/candidate-evidence.md` for `browser-qa`, which re-inspects the affected screens on the fresh verdict run (up to 2 verdict rounds on the affected screens only, at most 1 fix round per problem list — a fresh budget, not the step-5 loop's consumed caps) before polish/deploy, and only its verdict decides whether a fix is owed.""",
 "C4-3 orchestrate :195 finish-review route: destination + fresh budget"),
# ---------------------------------------------------------------- C5-1 (C)
("new-skills/orchestrate/SKILL.md",
 """and the anti-generic bar (`ui-ux-pro-max`: if a surface looks like a default template, it fails even if every checklist item passes).""",
 """and the anti-generic bar (`browser-qa`'s visual-loop bar: on `browser-qa`'s verdict, a surface that reads as a default template fails the bar even if every checklist item passes — `ui-ux-pro-max` supplies the design guidance that builds the direction, never the verdict).""",
 "C5-1 orchestrate :193 citation re-pointed to browser-qa"),
# ---------------------------------------------------------------- C5-2 (C)
("new-skills/orchestrate/SKILL.md",
 """A design check FAILS (a finding, minor at least) when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).""",
 """On `browser-qa`'s verdict, a design check FAILS (a finding, minor at least) when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).""",
 "C5-2 orchestrate :193 FAILS sentence: verdict attribution"),
# ---------------------------------------------------------------- C5-3 (C)
("new-skills/orchestrate/SKILL.md",
 """The distinctiveness judgment on the primary screens happens in the step-5 visual loop (`browser-qa`, sole executor) — do not re-judge it here; a finding, minor at least, when a screen carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — routed to the fix loop within the existing caps.""",
 """The distinctiveness judgment on the primary screens happens in the step-5 visual loop (`browser-qa`, sole executor) — do not re-judge it here; on `browser-qa`'s verdict, a finding, minor at least, when a screen carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — routed to the fix loop within the existing caps.""",
 "C5-3 orchestrate :195 app-screen paragraph: verdict attribution"),
# ---------------------------------------------------------------- C4-4 (C)
("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
 """a Specificity score under 3 is recorded (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar.""",
 """a Specificity score under 3 is appended to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar.""",
 "C4-4 gates.md :40 Specificity destination"),
# ---------------------------------------------------------------- C4-5 (C)
("new-skills/design-taste-frontend/SKILL.md",
 """which are candidate evidence for `browser-qa`, never fix-batch verdicts: record them in `.hallmark/hero-review.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge.""",
 """which are candidate evidence for `browser-qa`, never fix-batch verdicts: append them to `.hallmark/candidate-evidence.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge.""",
 "C4-5 Taste :314 template observations to candidate-evidence.md"),
# ---------------------------------------------------------------- C4-8 (C)
("round2-skills/polish-pass/SKILL.md",
 """record that as candidate evidence for `browser-qa` (screen + which tokens diverge), not a generic-template finding.""",
 """append that to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (screen + which tokens diverge), not a generic-template finding.""",
 "C4-8 polish-pass SKILL.md :22 evidence destination"),
# ---------------------------------------------------------------- C4-9 (C)
("round2-skills/polish-pass/SKILL.md",
 """Apply the polish fixes that fit, then record the per-screen evidence as candidate evidence for `browser-qa` (which screens, what suggests the direction is not applied) — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands and is re-verified by `browser-qa` before deploy.""",
 """Apply the polish fixes that fit, then append the per-screen evidence to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (which screens, what suggests the direction is not applied) — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands and is re-verified by `browser-qa` before deploy.""",
 "C4-9 polish-pass SKILL.md :24 evidence destination"),
# ---------------------------------------------------------------- C4-10 (C)
("round2-skills/polish-pass/SKILL.md",
 """a look that itself is the problem is recorded as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy), not redesigned here.""",
 """a look that itself is the problem is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy), not redesigned here.""",
 "C4-10 polish-pass SKILL.md :85 evidence destination"),
# ---------------------------------------------------------------- C4-11 (C)
("round2-skills/polish-pass/SKILL.md",
 """a screen whose consistency suggests the direction is not applied is recorded as candidate evidence for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s visual-loop verdict; route it to the design skill then, never a silent note.""",
 """a screen whose consistency suggests the direction is not applied is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s visual-loop verdict; route it to the design skill then, never a silent note.""",
 "C4-11 polish-pass SKILL.md :96 evidence destination"),
# ---------------------------------------------------------------- C4-12 (C)
("round2-skills/polish-pass/reference/polish.md",
 """if the diagnosis calls for one, that is a redesign: record the per-screen evidence as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.""",
 """if the diagnosis calls for one, that is a redesign: append the per-screen evidence to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.""",
 "C4-12 polish.md :7 evidence destination"),
# ---------------------------------------------------------------- C4-13 (C)
("round2-skills/polish-pass/reference/polish.md",
 """is recorded as candidate evidence for `browser-qa` with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.""",
 """is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.""",
 "C4-13 polish.md :20 evidence destination"),
# ---------------------------------------------------------------- C4-14 (C)
("round2-skills/polish-pass/reference/polish.md",
 """is recorded as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy.""",
 """is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy.""",
 "C4-14 polish.md :24 evidence destination"),
# ---------------------------------------------------------------- C4-15 (C)
("round2-skills/polish-pass/reference/polish.md",
 """record the generic-template diagnosis as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps""",
 """append the generic-template diagnosis to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps""",
 "C4-15 polish.md :35 evidence destination"),
# ---------------------------------------------------------------- C4-16 (C)
("round2-skills/polish-pass/reference/scoring.md",
 """Polish's own observation of an AI-template look is candidate evidence for `browser-qa` (record which screens and how), never the cap or the FINDING on its own.""",
 """Polish's own observation of an AI-template look is candidate evidence for `browser-qa` (append which screens and how to `.hallmark/candidate-evidence.md`), never the cap or the FINDING on its own.""",
 "C4-16 scoring.md :55 evidence destination"),
# ---------------------------------------------------------------- C4-17 (C)
("round2-skills/polish-pass/reference/scoring.md",
 """Three or more tells are candidate evidence for `browser-qa` that the surface reads as a template;""",
 """Three or more tells are candidate evidence for `browser-qa` (append screen + tells to `.hallmark/candidate-evidence.md`) that the surface reads as a template;""",
 "C4-17 scoring.md :56 evidence destination"),
# ---------------------------------------------------------------- C4-18 (C)
("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
 """**Record what reads as a template as candidate evidence for `browser-qa` (screen + what it reads as) — it is not a finding of this review and does not drive its first word: `browser-qa` alone executes the distinctiveness bar in the visual loop.**""",
 """**Append what reads as a template to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (screen + what it reads as) — it is not a finding of this review and does not drive its first word: `browser-qa` alone executes the distinctiveness bar in the visual loop.**""",
 "C4-18 review-hero.md :11 evidence destination"),

# ---------------------------------------------------------------- 9a (D)
("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
 """Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first.""",
 """Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first — under the scope note below: this critique is a design input, not a distinctiveness verdict; only the five craft axes join the fix list, and a Specificity score under 3 is recorded as candidate evidence for `browser-qa`, never a verdict on its own.""",
 "9a gates.md :38 trigger sentence scoped by note"),
# ---------------------------------------------------------------- 9b (D)
("new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md",
 """Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first.""",
 """Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first — under the Scope note below (Specificity is candidate evidence for `browser-qa`, never a verdict; only the five craft axes join the fix list).""",
 "9b hallmark-floor.md :62-63 trigger sentence scoped by note"),
# ---------------------------------------------------------------- 9c (D)
("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
 """- Does the headline say something only this product could say, in seven words or fewer?""",
 """- Does the headline say something only this product could say, in seven words or fewer? (Copy craft — whether the headline carries the product's own nouns and claim. A headline that would pass unchanged on a competitor's page is recorded as candidate evidence for `browser-qa`, not a finding of this review, and never drives the first word.)""",
 "9c review-hero.md :9 headline question: copy craft"),
# ---------------------------------------------------------------- 9d (D)
("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
 """Scroll the 1440 full page one screen at a time before ranking: a screen with nothing big enough to be its reason (a head and a line adrift, a narrow column beside an empty half, a section head under 40px, an empty coloured box or a drawn illustration where a photograph or the product should be, a row of counting marks) outranks every detail finding (`layout.md` § 8). Then the copy: name any head that would pass unchanged on a competitor's page (`craft.md` § 6).""",
 """Scroll the 1440 full page one screen at a time before ranking: a screen with nothing big enough to be its reason as a matter of mass and layout (a head and a line adrift, a narrow column beside an empty half, a section head under 40px) outranks every detail finding (`layout.md` § 8) — but a screen whose only mass problem is a template tell (an empty coloured box or a drawn illustration where a photograph or the product should be, a row of counting marks) is recorded as candidate evidence for `browser-qa` instead, never a finding of this review. Then the copy: name any head that would pass unchanged on a competitor's page (`craft.md` § 6).""",
 "9d review-finish.md :9 template tells are evidence, not findings"),
# ---------------------------------------------------------------- 9e-merged (D + C4-19 merged — coordinator)
("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
 """On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, in at most five findings — recorded as candidate evidence for `browser-qa`, not as findings of this review.""",
 """On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, recording at most five observations as candidate evidence for `browser-qa` in `.hallmark/candidate-evidence.md` — observations, not findings of this review, and they do not join the fix list.""",
 "9e-merged review-finish.md :15 observations + destination (merges C4-19)"),
]

# Pre-existing build.sh (f) polish-pass patch anchors — must still be count==1
# in the staged SKILL.md after the edits above (fix13d Phase 3).
F_ANCHORS = [
    "a new look belongs to ui-ux-pro-max and less-flat-ui, not this skill.",
    "The plugin already has `ui-ux-pro-max` and `less-flat-ui` for design direction and surface treatments. Those skills own the look.",
    "If the user asks for a new look outright, that is not this skill: say so and point them at `ui-ux-pro-max`.",
    "| A new look, direction, or visual style (\"redesign\", \"revamp\", \"make it look different\") | `ui-ux-pro-max` / `less-flat-ui` — not this skill |",
]


def main():
    texts = {}
    # Phase 1 — verify every anchor before writing anything.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        if p not in texts:
            with open(p, encoding="utf-8") as f:
                texts[p] = f.read()
        n = texts[p].count(old)
        assert n == 1, f"VERIFY {label}: anchor count={n} (expected 1) in {rel}: {old[:80]!r}"
        print(f"verify OK: {label}")
    # Phase 2 — apply.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        texts[p] = texts[p].replace(old, new, 1)
    for p, t in texts.items():
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    # Phase 3 — re-verify build.sh (f) anchors in the staged polish SKILL.md.
    staged = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/SKILL.md")
    t = open(staged, encoding="utf-8").read()
    for a in F_ANCHORS:
        n = t.count(a)
        assert n == 1, f"(f) anchor count={n} (expected 1) after edits: {a[:60]!r}"
        print(f"(f) anchor OK: {a[:50]!r}")
    print(f"fix13e staged edits applied ({len(SUBS)} substitutions)")


if __name__ == "__main__":
    main()
