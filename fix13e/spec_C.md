# spec_C.md — fix round #13e, worker C (items 3 + 4 + follow-up §5)

Reframing (applies to every change below): `browser-qa` is the SOLE executor of
pass/fail VERDICTS on rendered screens. Everything else is design guidance,
candidate evidence, or a static check, worded as such, never as a pass/fail
verdict on a screen.

Conventions: every OLD anchor below was counted with `python str.count` against
its patch-target file (staged file for staged specs, built-tree file for
build.sh-patch specs) and occurs exactly once. Staged-vs-built note:
`new-skills/orchestrate/SKILL.md` == built; `gates.md` staged == built;
polish-pass reference files staged == built; `round2-skills/polish-pass/SKILL.md`
and `new-skills/design-taste-frontend/SKILL.md` staged differ from built only in
frontmatter/description + pointer lines, none of which any anchor below touches.
`browser-qa`, `orch-build-mvp`, `design-system` have NO staged source: they are
upstream ECC, copied at build.sh:120 (`cp -r "$ECC_SRC/skills/." "$PLUGIN_DIR/skills/"`)
from the ECC Developer install, and patched at build time (same pattern as the
fix13b python-subs block) — so their specs are build.sh-patch specs.

## Item 3 — polish has no verdict run for its new evidence; caps consumed; no deploy hold

### C3-1 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:60 confirmed. Quote: "the design
skill builds it and `browser-qa` re-runs the step-5 every-route visual loop on the
redesigned screens BEFORE the 5c deploy — within the existing visual-loop caps; an
unverified redesign never reaches deploy." Parent citation correct. The step-5 loop
already ran before 5b and its caps (max 3 rounds total, at most 2 fix rounds per
problem list, :193) can be exhausted — no fresh run is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-5 every-route visual loop on the redesigned screens BEFORE the 5c deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.
```
NEW (verbatim, in a code fence):
```
**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the 5c deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-5 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them; the redesign decision follows `browser-qa`'s verdict. If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see 5c): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy.
```

### C3-2 — skills/orch-build-mvp/SKILL.md [build.sh patch]
Re-trace: built-tree skills/orch-build-mvp/SKILL.md:53 confirmed. Quote: "the design
skill builds it and `browser-qa` re-runs the step-6 every-route visual loop on the
redesigned screens BEFORE the step-7 commit and step-8 deploy — within the existing
visual-loop caps; an unverified redesign never reaches deploy." Parent citation
correct. Same defect as C3-1: the step-6 loop already ran before 6b.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-6 every-route visual loop on the redesigned screens BEFORE the step-7 commit and step-8 deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.
```
NEW (verbatim, in a code fence):
```
**Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and the orchestrator runs a fresh `browser-qa` verdict run on the redesigned screens BEFORE the redesign decision and BEFORE the step-7 commit and step-8 deploy: `browser-qa` renders its verdict on the redesigned screens and the candidate evidence in `.hallmark/candidate-evidence.md`, on a FRESH budget of up to 2 verdict rounds on the redesigned screens only, at most 1 fix round per problem list — this budget is separate from the step-6 visual loop's consumed caps (max 3 rounds total, at most 2 fix rounds per problem list) and is not drawn from them; the redesign decision follows `browser-qa`'s verdict. If the fresh run's final verdict still fails, or no rounds remain, the redesign is held (see steps 7/8): record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; an unverified redesign never reaches deploy.
```

### C3-3 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:61 confirmed. Quote: "deploy the app
(`deploy-fast`). Before the final deploy, run the `security-review` pre-deployment
checklist (deploy-fast Timing rule) and record pass/blockers in the final report."
No re-verification check, no hold: 5c deploys whatever polish routed. Parent
citation (:61) correct.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
   - **5c. Deploy** — deploy the app (`deploy-fast`). Before the final deploy, run the `security-review` pre-deployment checklist (deploy-fast Timing rule) and record pass/blockers in the final report.
```
NEW (verbatim, in a code fence):
```
   - **5c. Deploy** — deploy the app (`deploy-fast`). Before the final deploy, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Before the final deploy, run the `security-review` pre-deployment checklist (deploy-fast Timing rule) and record pass/blockers in the final report.
```

### C3-4 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:64 confirmed. Quote: "commit each
landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2
auto-approves in a first build) before writing the final report". Step 6 runs after
5c deploy, so a held deploy alone does not stop an unverified redesign being
committed — the hold must also cover the commit.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
6. **Commit, README, then final report** — commit each landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2 auto-approves in a first build) before writing the final report;
```
NEW (verbatim, in a code fence):
```
6. **Commit, README, then final report** — commit each landed slice as a conventional `feat:` commit via orch-pipeline Phase 6 (Gate 2 auto-approves in a first build) before writing the final report; if a polish-routed redesign failed re-verification, its files are not committed in this run — record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign (this is a safety hold, not a user question — it never asks the user anything).
```

### C3-5 — skills/orch-build-mvp/SKILL.md [build.sh patch]
Re-trace: built-tree skills/orch-build-mvp/SKILL.md:55 confirmed. Quote: "Commit the
scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit;
auto-approves during a hackathon first build after grill-me, or a one-prompt removal
of a first-build feature — proceed without waiting; see hackathon-mode §7)." Gate 2
auto-approves with no re-verification check. Parent citation correct.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
7. **Commit — orch-pipeline Phase 6.** Commit the scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting; see hackathon-mode §7).
```
NEW (verbatim, in a code fence):
```
7. **Commit — orch-pipeline Phase 6.** Before committing, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the commit of the redesign is HELD: do not commit the redesigned files in this run, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report; Gate 2 auto-approval never covers an unverified redesign (this is a safety hold, not a user question — it never asks the user anything). Otherwise, commit the scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting; see hackathon-mode §7).
```

### C3-6 — skills/orch-build-mvp/SKILL.md [build.sh patch]
Re-trace: built-tree skills/orch-build-mvp/SKILL.md:56 confirmed. Quote: "Deploy the
working MVP — record the production URL and the deploy path used in
`.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only,
or blocked with the failing command and error)". Step 8 deploys unconditionally. Parent
citation correct.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Deploy the working MVP — record the production URL and the deploy path used in `.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) — then film the LOCAL app from the project dir (`APP_DIR` to the app dir)
```
NEW (verbatim, in a code fence):
```
8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Before deploying, run the named re-verification check (unconditionally, whenever a polish-routed redesign exists): was it re-verified and did `browser-qa`'s fresh verdict pass? If no, or no fresh rounds remain, the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). Otherwise, deploy the working MVP — record the production URL and the deploy path used in `.hackathon/run-ledger.md` (Vercel CLI link, git-linked push, Railway, static-only, or blocked with the failing command and error) — then film the LOCAL app from the project dir (`APP_DIR` to the app dir)
```

## Item 4 — candidate evidence has no durable route into browser-qa

### C4-1 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:193 confirmed. Quote: "**Candidate
evidence in:** if `.hallmark/hero-review.md` exists, its template observations are
input to your verdict (look where they point); step-6 template observations reach you
the same way on re-inspection." Parent citation correct: no file, ledger line, or
dispatch input is named. This is the visual loop's input list — the destination is
named here by construction.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
**Candidate evidence in:** if `.hallmark/hero-review.md` exists, its template observations are input to your verdict (look where they point); step-6 template observations reach you the same way on re-inspection. Evidence never overrides your verdict — you make the call.
```
NEW (verbatim, in a code fence):
```
**Candidate evidence in:** `.hallmark/candidate-evidence.md` is a standing input to the visual loop: before rendering a verdict, read it if it exists in the project root and treat its entries as candidate evidence (screen + what reads as a template), never as a verdict — every producer appends there (polish-pass, design-system slop findings, Taste hero-review template observations, gates Specificity, step-6 finish-review template observations). If `.hallmark/hero-review.md` exists, its template observations are already copied there; step-6 template observations reach you the same way on re-inspection. Evidence never overrides your verdict — you make the call.
```

### C4-2 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:195 confirmed. Quote: "record a
Specificity score under 3 (screen + what reads as a template) for `browser-qa`'s
visual loop, which alone executes the distinctiveness bar (see gates.md §3)."
Parent citation (:195) correct; no destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
record a Specificity score under 3 (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar (see gates.md §3).
```
NEW (verbatim, in a code fence):
```
append a Specificity score under 3 to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar (see gates.md §3).
```

### C4-3 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:195 confirmed. Quote: "route them to
`browser-qa`, which re-inspects the affected screens in the step-5 visual loop
(within the existing caps) before polish/deploy, and only its verdict decides whether
a fix is owed." This is also the step-6 sentence that sends template observations to
re-inspection on the step-5 loop's CONSUMED caps with no fresh run named (item 3
scope, same line) — it gets the destination AND the fresh-budget wording here.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
route them to `browser-qa`, which re-inspects the affected screens in the step-5 visual loop (within the existing caps) before polish/deploy, and only its verdict decides whether a fix is owed.
```
NEW (verbatim, in a code fence):
```
append them to `.hallmark/candidate-evidence.md` for `browser-qa`, which re-inspects the affected screens on the fresh verdict run (up to 2 verdict rounds on the affected screens only, at most 1 fix round per problem list — a fresh budget, not the step-5 loop's consumed caps) before polish/deploy, and only its verdict decides whether a fix is owed.
```

### C4-4 — skills/design-taste-frontend/references/hallmark/references/gates.md [staged: new-skills/design-taste-frontend/references/hallmark/references/gates.md]
Re-trace: built-tree gates.md:40 confirmed. Quote: "a Specificity score under 3 is
recorded (screen + what reads as a template) for `browser-qa`'s visual loop, which
alone executes the distinctiveness bar." Parent citation (:40) correct; no
destination is named. Staged file == built file.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
a Specificity score under 3 is recorded (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar.
```
NEW (verbatim, in a code fence):
```
a Specificity score under 3 is appended to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar.
```

### C4-5 — skills/design-taste-frontend/SKILL.md [staged: new-skills/design-taste-frontend/SKILL.md]
Re-trace: built-tree skills/design-taste-frontend/SKILL.md:314 confirmed. Quote:
"which are candidate evidence for `browser-qa`, never fix-batch verdicts: record them
in `.hallmark/hero-review.md` with the screen and what reads as a template, for
`browser-qa`'s visual loop to judge." Parent claim verified: Taste does write
hero-review.md. But hero-review.md is the HERO review's record (craft findings +
settlements, read by the finish review in Verify) — it is the wrong home for
non-hero evidence, and `browser-qa` never reads it (0 hits for `hero-review` in
skills/browser-qa/SKILL.md). Template observations move to the canonical file;
hero-review.md keeps the craft findings and their settlements (that sentence is
unchanged by this spec).
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
which are candidate evidence for `browser-qa`, never fix-batch verdicts: record them in `.hallmark/hero-review.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge.
```
NEW (verbatim, in a code fence):
```
which are candidate evidence for `browser-qa`, never fix-batch verdicts: append them to `.hallmark/candidate-evidence.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge.
```

### C4-6 — skills/design-system/SKILL.md [build.sh patch]
Re-trace: built-tree skills/design-system/SKILL.md:56 confirmed. Quote: "Record slop
findings with the screen and pattern for `browser-qa` to judge." No destination is
named. `design-system` has no staged source (upstream ECC, build.sh-patch).
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
Record slop findings with the screen and pattern for `browser-qa` to judge.
```
NEW (verbatim, in a code fence):
```
Append slop findings to `.hallmark/candidate-evidence.md` with the screen and pattern for `browser-qa` to judge.
```

### C4-7 — skills/browser-qa/SKILL.md [build.sh patch]
Re-trace: built-tree skills/browser-qa/SKILL.md:68 confirmed. Quote: "Each round:
capture screenshots, then judge the rendered UI on typography, hierarchy, spacing,
alignment, color, contrast, responsiveness, and distinctiveness — this skill is the
SOLE executor of the distinctiveness bar inside the visual loop:". Source located:
`browser-qa` has no staged source; it is upstream ECC copied at build.sh:120 and
patched at build time (same pattern as the fix13b python-subs block, which patched
this same file). `browser-qa` SKILL.md has 0 hits for `run-ledger`, `hero-review`,
and `candidate evidence` — it currently reads no evidence file at all.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop:
```
NEW (verbatim, in a code fence):
```
Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, responsiveness, and distinctiveness — this skill is the SOLE executor of the distinctiveness bar inside the visual loop: before rendering a verdict in any round, read `.hallmark/candidate-evidence.md` if it exists in the project root and treat its entries as candidate evidence (screen + what reads as a template), never as a verdict; the orchestrator passes this file as a standing input to the visual loop, not from memory.
```

### C4-8 — skills/polish-pass/SKILL.md [staged: round2-skills/polish-pass/SKILL.md]
Re-trace: built-tree skills/polish-pass/SKILL.md:22 confirmed. Quote: "record that as
candidate evidence for `browser-qa` (screen + which tokens diverge), not a
generic-template finding." No destination is named. Patch target is the staged file
(staged SKILL.md differs from built only in frontmatter/description + pointer lines;
this anchor is identical in both).
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
record that as candidate evidence for `browser-qa` (screen + which tokens diverge), not a generic-template finding.
```
NEW (verbatim, in a code fence):
```
append that to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (screen + which tokens diverge), not a generic-template finding.
```

### C4-9 — skills/polish-pass/SKILL.md [staged: round2-skills/polish-pass/SKILL.md]
Re-trace: built-tree skills/polish-pass/SKILL.md:24 confirmed. Quote: "Apply the
polish fixes that fit, then record the per-screen evidence as candidate evidence for
`browser-qa` (which screens, what suggests the direction is not applied)". No
destination is named. Anchor is the staged/built-shared prefix (ends "...before
deploy."); the staged tail ("point them at `ui-ux-pro-max`.") is untouched.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
Apply the polish fixes that fit, then record the per-screen evidence as candidate evidence for `browser-qa` (which screens, what suggests the direction is not applied) — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands and is re-verified by `browser-qa` before deploy.
```
NEW (verbatim, in a code fence):
```
Apply the polish fixes that fit, then append the per-screen evidence to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (which screens, what suggests the direction is not applied) — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands and is re-verified by `browser-qa` before deploy.
```

### C4-10 — skills/polish-pass/SKILL.md [staged: round2-skills/polish-pass/SKILL.md]
Re-trace: built-tree skills/polish-pass/SKILL.md:85 confirmed. Quote: "a look that
itself is the problem is recorded as candidate evidence for `browser-qa`". No
destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
a look that itself is the problem is recorded as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy), not redesigned here.
```
NEW (verbatim, in a code fence):
```
a look that itself is the problem is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy), not redesigned here.
```

### C4-11 — skills/polish-pass/SKILL.md [staged: round2-skills/polish-pass/SKILL.md]
Re-trace: built-tree skills/polish-pass/SKILL.md:96 confirmed. Quote: "a screen whose
consistency suggests the direction is not applied is recorded as candidate evidence
for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s
visual-loop verdict; route it to the design skill then, never a silent note." No
destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
a screen whose consistency suggests the direction is not applied is recorded as candidate evidence for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s visual-loop verdict; route it to the design skill then, never a silent note.
```
NEW (verbatim, in a code fence):
```
a screen whose consistency suggests the direction is not applied is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s visual-loop verdict; route it to the design skill then, never a silent note.
```

### C4-12 — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]
Re-trace: built-tree skills/polish-pass/reference/polish.md:7 confirmed. Quote:
"record the per-screen evidence as candidate evidence for `browser-qa` — a
generic-template finding exists only on `browser-qa`'s visual-loop verdict". No
destination is named. Staged reference files == built.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
if the diagnosis calls for one, that is a redesign: record the per-screen evidence as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.
```
NEW (verbatim, in a code fence):
```
if the diagnosis calls for one, that is a redesign: append the per-screen evidence to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.
```

### C4-13 — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]
Re-trace: built-tree skills/polish-pass/reference/polish.md:20 confirmed. Quote: "is
recorded as candidate evidence for `browser-qa` with per-screen evidence — a
generic-template FINDING exists only on `browser-qa`'s visual-loop verdict". No
destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
is recorded as candidate evidence for `browser-qa` with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.
```
NEW (verbatim, in a code fence):
```
is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.
```

### C4-14 — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]
Re-trace: built-tree skills/polish-pass/reference/polish.md:24 confirmed. Quote: "is
recorded as candidate evidence for `browser-qa` (which screen, which tokens diverge)
— a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict".
No destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
is recorded as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy.
```
NEW (verbatim, in a code fence):
```
is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy.
```

### C4-15 — skills/polish-pass/reference/polish.md [staged: round2-skills/polish-pass/reference/polish.md]
Re-trace: built-tree skills/polish-pass/reference/polish.md:35 confirmed. Quote:
"record the generic-template diagnosis as candidate evidence for `browser-qa` — a
FINDING exists only on `browser-qa`'s visual-loop verdict". No destination is named.
("for a redesign within the existing caps" here governs the redesign build's fix
loop, not a verdict run — left unchanged.)
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
record the generic-template diagnosis as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps
```
NEW (verbatim, in a code fence):
```
append the generic-template diagnosis to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps
```

### C4-16 — skills/polish-pass/reference/scoring.md [staged: round2-skills/polish-pass/reference/scoring.md]
Re-trace: built-tree skills/polish-pass/reference/scoring.md:55 confirmed. Quote:
"Polish's own observation of an AI-template look is candidate evidence for
`browser-qa` (record which screens and how), never the cap or the FINDING on its
own." No destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
Polish's own observation of an AI-template look is candidate evidence for `browser-qa` (record which screens and how), never the cap or the FINDING on its own.
```
NEW (verbatim, in a code fence):
```
Polish's own observation of an AI-template look is candidate evidence for `browser-qa` (append which screens and how to `.hallmark/candidate-evidence.md`), never the cap or the FINDING on its own.
```

### C4-17 — skills/polish-pass/reference/scoring.md [staged: round2-skills/polish-pass/reference/scoring.md]
Re-trace: built-tree skills/polish-pass/reference/scoring.md:56 confirmed. Quote:
"Three or more tells are candidate evidence for `browser-qa` that the surface reads
as a template". No destination is named.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
Three or more tells are candidate evidence for `browser-qa` that the surface reads as a template;
```
NEW (verbatim, in a code fence):
```
Three or more tells are candidate evidence for `browser-qa` (append screen + tells to `.hallmark/candidate-evidence.md`) that the surface reads as a template;
```

### C4-18 — skills/design-taste-frontend/references/hallmark/references/review-hero.md [staged: new-skills/design-taste-frontend/references/hallmark/references/review-hero.md]
Re-trace: built-tree review-hero.md:11 confirmed. Quote: "**Record what reads as a
template as candidate evidence for `browser-qa` (screen + what it reads as) — it is
not a finding of this review and does not drive its first word: `browser-qa` alone
executes the distinctiveness bar in the visual loop.**" No destination is named.
Staged file == built file.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
**Record what reads as a template as candidate evidence for `browser-qa` (screen + what it reads as) — it is not a finding of this review and does not drive its first word: `browser-qa` alone executes the distinctiveness bar in the visual loop.**
```
NEW (verbatim, in a code fence):
```
**Append what reads as a template to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (screen + what it reads as) — it is not a finding of this review and does not drive its first word: `browser-qa` alone executes the distinctiveness bar in the visual loop.**
```

### C4-19 — skills/design-taste-frontend/references/hallmark/references/review-finish.md [staged: new-skills/design-taste-frontend/references/hallmark/references/review-finish.md]
Re-trace: built-tree review-finish.md:15 confirmed. Quote: "in at most five findings
— recorded as candidate evidence for `browser-qa`, not as findings of this review."
No destination is named. Staged file == built file.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
in at most five findings — recorded as candidate evidence for `browser-qa`, not as findings of this review.
```
NEW (verbatim, in a code fence):
```
in at most five findings — appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, not as findings of this review.
```

## Follow-up §5 — re-point the :193 citation; literal verdict qualification (per worker A note)

Worker A noted orchestrate SKILL.md:193 quotes `ui-ux-pro-max`'s OLD wording inside
the distinctiveness-bar paragraph; once worker A's spec 1B lands (rewording the
`ui-ux-pro-max` bars to guidance/evidence), that :193 citation goes stale. Worker A
deliberately left orchestrate :193/:195 and orch-build-mvp :40/:49 to this worker.
Judgment: yes, the literal qualification is needed in all five places below. The
:193/:195/:40/:49 sentences state a screen "fails" or a "finding, minor at least"
without naming the verdict-maker in the sentence itself; a later reader or auditor
quoting the sentence alone can read it as the citing skill issuing the verdict. The
bar headers already name `browser-qa` as sole executor, but the operative
fail/finding clause must carry the attribution literally for the tree-wide claim
("exactly one verdict-maker") to hold sentence by sentence.

### C5-1 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:193 confirmed. Quote: "and the
anti-generic bar (`ui-ux-pro-max`: if a surface looks like a default template, it
fails even if every checklist item passes)." This attributes the fail to
`ui-ux-pro-max`'s bar; after worker A's 1B the `ui-ux-pro-max` bar is guidance /
evidence, not a verdict, so the citation goes stale.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
and the anti-generic bar (`ui-ux-pro-max`: if a surface looks like a default template, it fails even if every checklist item passes).
```
NEW (verbatim, in a code fence):
```
and the anti-generic bar (`browser-qa`'s visual-loop bar: on `browser-qa`'s verdict, a surface that reads as a default template fails the bar even if every checklist item passes — `ui-ux-pro-max` supplies the design guidance that builds the direction, never the verdict).
```

### C5-2 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:193 confirmed (same line, later
sentence). Quote: "A design check FAILS (a finding, minor at least) when screens carry
no named direction, no applied theme/tokens, read as a default template, or are
derivative (the design is based on a searched external reference)." The sentence
states the fail with no verdict-maker named in it.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
A design check FAILS (a finding, minor at least) when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).
```
NEW (verbatim, in a code fence):
```
On `browser-qa`'s verdict, a design check FAILS (a finding, minor at least) when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference).
```

### C5-3 — skills/orchestrate/SKILL.md [staged: new-skills/orchestrate/SKILL.md]
Re-trace: built-tree skills/orchestrate/SKILL.md:195 confirmed (app-screen paragraph).
Quote: "The distinctiveness judgment on the primary screens happens in the step-5
visual loop (`browser-qa`, sole executor) — do not re-judge it here; a finding, minor
at least, when a screen carries no named direction, no applied theme/tokens, reads as
a default template, or is derivative (the design is based on a searched external
reference) — routed to the fix loop within the existing caps." The finding clause as
written reads as this step issuing the finding.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
The distinctiveness judgment on the primary screens happens in the step-5 visual loop (`browser-qa`, sole executor) — do not re-judge it here; a finding, minor at least, when a screen carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — routed to the fix loop within the existing caps.
```
NEW (verbatim, in a code fence):
```
The distinctiveness judgment on the primary screens happens in the step-5 visual loop (`browser-qa`, sole executor) — do not re-judge it here; on `browser-qa`'s verdict, a finding, minor at least, when a screen carries no named direction, no applied theme/tokens, reads as a default template, or is derivative (the design is based on a searched external reference) — routed to the fix loop within the existing caps.
```

### C5-4 — skills/orch-build-mvp/SKILL.md [build.sh patch]
Re-trace: built-tree skills/orch-build-mvp/SKILL.md:40 confirmed (step-4 design-package
bullet). Quote: "The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's
every-route visual loop (browser-qa is the SOLE executor of the bar) — a named
direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a
finding, minor at least, when screens carry no named direction, no applied
theme/tokens, read as a default template, or are derivative (the design is based on a
searched external reference) — within the existing fix caps." The finding clause is
unattached to the verdict in the sentence itself. ("within the existing fix caps"
here governs the finding's fix loop, not a verdict run — left unchanged.)
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.
```
NEW (verbatim, in a code fence):
```
The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); on `browser-qa`'s verdict, a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.
```

### C5-5 — skills/orch-build-mvp/SKILL.md [build.sh patch]
Re-trace: built-tree skills/orch-build-mvp/SKILL.md:49 confirmed (step 6). Quote:
"`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named
direction recorded AND visibly applied; a finding, minor at least, when screens carry
no named direction, no applied theme/tokens, read as a default template, or are
derivative — the design is based on a searched external reference); fix and re-inspect
within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per
problem list; if the app cannot run, record that as blocked with evidence instead of
iterating)." Same unattached finding clause as C5-4.
Anchor check: old text occurs exactly 1 time in the target file.
OLD (verbatim, in a code fence):
```
`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named direction recorded AND visibly applied; a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference); fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating).
```
NEW (verbatim, in a code fence):
```
`browser-qa` is the SOLE executor of the distinctiveness bar inside the loop (a named direction recorded AND visibly applied; on `browser-qa`'s verdict, a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative — the design is based on a searched external reference); fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating).
```

## Decisions

### (1) Item-3 decisions
- Fresh budget (decided): a fresh `browser-qa` verdict run of up to **2 verdict rounds on
  the redesigned / affected screens only, at most 1 fix round per problem list** — a
  budget separate from, and not drawn from, the step-5/step-6 visual loop's consumed
  caps (max 3 rounds total, at most 2 fix rounds per problem list). Rationale for the
  numbers: 2 rounds is the minimum that allows verdict → one fix → final verdict on a
  narrow screen set; 1 fix round keeps the post-polish loop from becoming a second
  full visual loop. If the second verdict still fails, or no rounds remain, the
  redesign is held.
- HOLD vs REVERT (decided): **HOLD**. One-line reason: no snapshot of the pre-redesign
  state is named anywhere in either pipeline, so a revert cannot be executed reliably,
  while a hold is enforceable with the existing ledger / `BLOCKED` record and never
  ships unverified screens. HOLD as wired (C3-3–C3-6): the deploy/commit of the
  redesign does not run, `re-verification: BLOCKED` is recorded in
  `.hackathon/run-ledger.md` and the final report, and nothing about the redesign is
  asked of the user.
- Full list of "within the existing visual-loop caps" hits in the built tree (grep,
  exactly 2) and their replacements:
  - `skills/orchestrate/SKILL.md:60` (5b) → replaced by C3-1 (fresh-budget wording).
  - `skills/orch-build-mvp/SKILL.md:53` (6b) → replaced by C3-2 (fresh-budget wording).
  - Related (not the exact phrase): orchestrate :195 finish-review "within the
    existing caps" → replaced by C4-3 with the same fresh budget. The remaining
    "within the existing caps" / "within the same caps" phrases govern fix loops
    (orch-build-mvp :40, :49; polish.md :35; orchestrate :195 app-screen paragraph)
    and are left — see Checked list.
- Step-6 sentences sending a redesign to deploy without re-verification (checked):
  - orchestrate Verify step 6 (:195) finish-review sentence routed template
    observations to re-inspection "within the existing caps" — fixed by C4-3.
  - orchestrate Verify step 6 (:195) app-screen paragraph routed findings "to the
    fix loop within the existing caps" with no fresh verdict named — qualified by
    C5-3; any redesign from it re-verifies under C3-1 before deploy.
  - orch-build-mvp step 6 (:49) itself names no polish redesign and no deploy; the
    polish redesign path is 6b, fixed by C3-2.

### (2) Item-4 decision
- Canonical destination (decided): **`.hallmark/candidate-evidence.md`** (new file in
  the project root; 0 hits in the built tree — it does not already exist). One-line
  reason: it is the only candidate that is evidence-only and screen-scoped — not
  hero-only like `.hallmark/hero-review.md` (Taste :314, hero findings + settlements,
  read by the finish review; `browser-qa` never reads it, 0 hits) and not a stage
  ledger like `.hackathon/run-ledger.md` (one-line check-outcome pointers per
  orchestrate :58, which `browser-qa` never reads, 0 hits for `run-ledger` /
  `hero-review` / `candidate evidence` in skills/browser-qa/SKILL.md). Format: one
  line per observation — screen + what reads as a template + source. Routing does not
  depend on memory: producers append there by instruction (C4-2–C4-6, C4-8–C4-19),
  the visual loop lists it as a standing input (C4-1), and `browser-qa` reads it
  before every verdict (C4-7).
- `.hallmark/hero-review.md` is the right home for HERO evidence only (craft findings
  + settlements, read by the finish review); it is not the home for non-hero /
  app-screen evidence — hence template observations are copied out to
  `.hallmark/candidate-evidence.md` (C4-5) while hero-review.md keeps the hero
  review's own findings.
- Full list of "record for browser-qa" hits (grep `for browser-qa` / `for \`browser-qa`
  over skills/ agents/ commands/ rules/, 21 lines) and disposition:
  - `skills/design-system/SKILL.md:56` → C4-6.
  - `skills/design-taste-frontend/SKILL.md:314` → C4-5.
  - `skills/design-taste-frontend/references/hallmark/references/gates.md:40` → C4-4.
  - `skills/design-taste-frontend/references/hallmark/references/review-hero.md:5` → checked, not changed (scope statement only).
  - `skills/design-taste-frontend/references/hallmark/references/review-hero.md:11` → C4-18.
  - `skills/design-taste-frontend/references/hallmark/references/review-hero.md:16` → checked, not changed (scope statement only).
  - `skills/design-taste-frontend/references/hallmark/references/review-finish.md:5` → checked, not changed (scope statement only).
  - `skills/design-taste-frontend/references/hallmark/references/review-finish.md:13` → checked, not changed (scope statement only).
  - `skills/design-taste-frontend/references/hallmark/references/review-finish.md:15` → C4-19.
  - `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md:67` → checked, not changed (scope statement pointing to gates.md §3, covered by C4-4).
  - `skills/orchestrate/SKILL.md:195` (one grep line, three points) → Specificity sentence C4-2; finish-review route C4-3; app-screen paragraph C5-3.
  - `skills/polish-pass/reference/polish.md:7` → C4-12.
  - `skills/polish-pass/reference/polish.md:20` → C4-13.
  - `skills/polish-pass/reference/polish.md:24` → C4-14.
  - `skills/polish-pass/reference/polish.md:35` → C4-15.
  - `skills/polish-pass/reference/scoring.md:55` → C4-16.
  - `skills/polish-pass/reference/scoring.md:56` → C4-17.
  - `skills/polish-pass/SKILL.md:22` → C4-8.
  - `skills/polish-pass/SKILL.md:24` → C4-9.
  - `skills/polish-pass/SKILL.md:85` → C4-10.
  - `skills/polish-pass/SKILL.md:96` → C4-11.

### (3) Checked, not changed
- `skills/orchestrate/SKILL.md:193` bar header ("can FAIL — applies here; `browser-qa`
  is the SOLE executor of this bar inside the visual loop") — already names the
  verdict-maker; citation re-pointed in C5-1, FAILS sentence qualified in C5-2.
- `skills/orchestrate/SKILL.md:195` Specificity sentence — already literally qualified
  ("which alone executes the distinctiveness bar"); destination added in C4-2.
- `skills/orchestrate/SKILL.md:58` step-5 header (Verification outcomes to
  `docs/run-ledger-appendix.md` + pointer in `.hackathon/run-ledger.md`) — check
  outcomes, not per-screen evidence; ledger is not the candidate-evidence route.
- `skills/orchestrate/references/dispatch-prompt.md` — no `browser-qa` dispatch
  template or input list exists there; the visual-loop input list lives in orchestrate
  :193 (C4-1) and `browser-qa`'s own read step (C4-7); no spec needed.
- `skills/orch-build-mvp/SKILL.md:49` "within the same caps as orchestrate" — governs
  the step-6 visual loop itself, not a polish re-verification; left.
- `skills/orch-build-mvp/SKILL.md:40` / `:49` "within the existing fix caps" — govern
  the finding's fix loop, not a verdict run; left (finding clause qualified in
  C5-4 / C5-5).
- `skills/polish-pass/reference/polish.md:35` "for a redesign within the existing caps"
  — redesign build's fix loop, not a verdict run; left.
- `skills/polish-pass/reference/scoring.md:55` tail ("record which screens fail and
  how", on `browser-qa`'s verdict) — the verdict's own report; no separate
  destination needed.
- `skills/browser-qa/SKILL.md:68` "FAILS — report it as a distinctiveness finding" —
  `browser-qa`'s own verdict language; correct under the reframing, unchanged except
  for the read step added in C4-7.
- `skills/design-taste-frontend/SKILL.md:314` hero-review.md write sentence ("Write
  the hero review's findings to `.hallmark/hero-review.md` ... the finish review in
  Verify reads this file") — craft findings + settlements stay there; only template
  observations move (C4-5).
- `skills/design-system/SKILL.md:56` scope clause ("candidate evidence for
  `browser-qa`, never a verdict that a screen reads as a default template") — already
  follows the reframing; only the recording destination added (C4-6).
- `skills/design-taste-frontend/references/hallmark/references/review-hero.md:5` and
  `:16`, `review-finish.md:5` and `:13`, `hallmark-floor.md:67` — scope statements
  only, no recording action; destinations live in the recording sentences they
  reference (C4-18, C4-19, C4-4).

### (4) Blocked / held back
- None of the 30 specs is blocked: every OLD anchor was verified to occur exactly
  once in its patch-target file (25/25 in the first check run, 5/5 in the follow-up
  check run).
- Held back (needs a parent decision, not a spec): `.hallmark/candidate-evidence.md`
  itself is a per-project runtime file created by the first append; no template/seed
  for it exists in the plugin, and this worker did not create one — parent to confirm
  whether a seed template belongs in the plugin or the file is created on first
  append (all specs read it "if it exists", so either choice works).
- Held back: no spec for orch-pipeline / orch-change-feature / orch-add-feature /
  orch-fix-defect / orch-refine-code verdict wording — outside items 3/4 and the
  worker-A follow-up; if the audit finds the same unattached finding clauses there,
  that is a separate worker's scope.
