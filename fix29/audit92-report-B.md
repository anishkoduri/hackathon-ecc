# Audit #92-B — brief/verify coherence + verifier honesty (fix #29, round 13)

**Verdict: NOT PASS — 0 blocking, 4 minor (92-B1–B4). All four are verifier-only; the tree is currently correct on every point.**

Auditor B (brief/verify coherence + verifier honesty). Read-only except this report.
Method: read `fix29/verify29.py` end to end (2,053 lines); independently re-ran it —
**310/310, exit 0** (real tree, before any scratch work). All mutations below ran on a
scratch mirror at `/tmp/a92b/built` (real copy of the built tree + symlinks to the real
`fix28/`, `fix29/`, `new-rules/`, `new-skills/` so checks 7e/10g/11/11b run meaningfully —
the #91-B pattern), with a **fresh copy per mutation — no restores**, so the #91-B
round-1 restore-order hazard is avoided by construction. Mirror baseline 310/310;
scratch removed after. The real tree was never edited by this audit.

## §1 Disposition of the #91-B fixes — all VERIFIED-FIXED

Reproduced the coordinator's N2–N9 scratch mutations on fresh mirrors (one fresh copy
per mutation). Every one fails exactly its intended check(s) at 309/310, except N6b
(308/310, expected — see below).

| Fix | Reproduction | Result |
|---|---|---|
| 91-B1 gan-build step-0 pin | N2: parenthetical deleted from `gan-build.md:26` | **309/310**, exactly the B1 check (verify29.py:1626) |
| 91-B2 gan-design step-0 pin | N3: line :19 moved to EOF | **309/310**, exactly the B2 check (:1669) |
| 91-B3 planner-spec 3a | N4: line :30 moved to EOF | **309/310**, exactly the B3 check (:1642) |
| 91-B4 wrapper pointers | N5: `orch-build-mvp` pointer :13 moved to EOF | **309/310**, exactly the orch-build-mvp wrapper check (:1527) |
| 91-B5 DTF pointer, span-scoped | N6: line :455 moved to EOF | **309/310**, exactly the B5 check (:817–819) |
| 91-B5 clause deletion | N6b: clause deleted, line in place | **308/310**, B5 + 7e DTF — expected, see below |
| 91-B6 gan-build pointer | N7: director-brief/no-guessing/verification middle deleted from :12 | **309/310**, exactly the B6 check (:1618) |
| 91-B7 gan-design pointer | N8: loop-clause tail deleted from :10 | **309/310**, exactly the B7 check (:1680) |
| 91-B8 common-agents line | N9: operative middle deleted from :26 | **309/310**, exactly the B8 check (:1602) |

**91-B5 in its FINAL span-scoped form — confirmed.** N6 moves the whole :455 line to
EOF and fails exactly the B5 check. The span scope (`"4. **Deal, never choose by
taste.**"` → `"5. **Build.**"`, verify29.py:817) is what catches it: both markers
verified unique in the file (1 occurrence each), and the check asserts the pointer
clause on the redesign-flow line *inside that span*. The coordinator's record — that
the auditor's literal fix (assert the clause on the line) passed 310/310 on the EOF
move because the clause travels with the line — is consistent with this result: the
span, not the line content, is the property that matters, and the span check holds.

**N6b adjudication — confirmed.** Deleting the clause with the line in place fails
B5 plus the 7e DTF check (308/310). Expected: the clause sits on the file's single
`_F29` line (`design-taste-frontend/SKILL.md` carries exactly one), so editing it
trips 7e too — the same adjudication as the auditor's N1/N10/N12/N13.

**Nits 2+3 — confirmed fixed.** MANIFEST §2(c)(9)/OWED-29-5 now reads 41 diff lines
across 4 files, and a direct staged-vs-built diff run by this audit reproduces it
exactly: orchestrate 6, dispatch-prompt 0, deep-reasoner 0, feature-expansion 22,
design-taste-frontend SKILL.md 11, redesign.md 0, hackathon-mode 2 (see §7).
`fix29.py:438` cites `:274/:281` and `fix16.py:3808`; `fix29.py` md5 == template
(`fbd459c7…`). Nit 1 deliberately not fixed (see §4, F10).

## §2 New findings — 92-B1–B4 (all minor, verifier-only)

Same presence-not-position / fragment-only class as 83-B1/85-B2/87-B2/88-B1/89-B1–B4/
90-B1–B6/91-B1–B8. Tree currently correct on every point; each finding is demonstrated
by a scratch mutation (tree untouched) that leaves verify29 green at 310/310.

### 92-B1 (minor, verifier): the orch-pipeline and gan-style-harness factory-paragraph bodies are unasserted

- verify29.py:1500 asserts only the orch-pipeline paragraph's **opening clause**
  (`"**Factory routing (fix #29, GLOBAL-ROUTING_F29):** every phase dispatches through
  the factory"`, count == 1); :1530 does the same for the gan paragraph. The bodies
  are single long lines (:62, :14) whose operative sentences have no assertion at all.
  Grep over verify29.py: `"one drone per job, retired on completion"` 0×,
  `"an incomplete brief means the drone does not start"` 0×,
  `"stops and returns the question to the orchestrator instead of guessing"` 0×,
  `"verifies every drone output against the brief"` 0×, the paragraph COST-AWARE
  sentences 0×. The field-list and orchestrator-only sentences occur in verify29.py
  exactly once each — in the GLOBAL-ROUTING **block** check, never in the paragraphs.
  The only paragraph-scoped assertions are the harness-gate clause (85-B2) and the
  seven-field contract reference (90-B4); the gan paragraph additionally has the
  evaluator-input / re-check / planner-spec count checks and the paragraph-scoped
  rubric rule (90-B3).
- Demonstrated (all 310/310):
  - M-OP1: delete the COST-AWARE sentence from `orch-pipeline:62` ("fan-out is
    bounded by efficiency, N>3 justified in one line, drones carrying minimal
    context (COST-AWARE_F29).").
  - M-OP2: delete the VERIFY-MERGE sentence from `orch-pipeline:62` ("The
    orchestrator verifies every drone output against the brief's acceptance criteria
    and sends failed output back with a correction brief (VERIFY-MERGE_F29); ").
  - M-GAN1: delete the COST-AWARE sentence from `gan-style-harness:14`.
  - M-GAN2: delete the NO-GUESSING sentence from `gan-style-harness:14` ("A drone
    that hits a decision its brief leaves unspecified stops and returns the question
    to the orchestrator instead of guessing (NO-GUESSING_F29). ").
  - M-GAN3: delete the VERIFY-MERGE tail from `gan-style-harness:14` ("; failed
    output goes back with a correction brief naming the failed criterion
    (VERIFY-MERGE_F29)").
- This is the 91-B6/B7/B8 defect one level up: the pointer checks were fixed by
  asserting the full line, but the two factory paragraphs still have fragment-only
  (opening-clause) assertions. A rebuild that dropped NO-GUESSING, VERIFY-MERGE, or
  COST-AWARE from either skill's routing paragraph would pass silently.
- The asymmetry is exactly the 7e coverage gap, proven by the controls: the same
  COST-AWARE deletion in feature-expansion :139 (M-FE1) and redesign :68 (M-RD1)
  fails at 309/310, exactly the 7e check — those files are staged, so any edit trips
  7e. Orch-pipeline and gan-style-harness are ECC-origin, outside 7e, so nothing
  guards their paragraph bodies.
- Fix (verifier-only): assert the full paragraph line in each file (87-B1 pattern —
  the lines are single-line paragraphs, as the gan-build/gan-design pointers are),
  or add per-sentence assertions for the queue sentence, field list,
  incomplete-brief rule, no-guessing sentence, verify sentence, COST-AWARE sentence,
  and orchestrator-only sentence. No tree change needed.

### 92-B2 (minor, verifier): the gan-build ORCHESTRATOR-CHECK step is header-only

- verify29.py:1636–1637 asserts only `_gb.count("# ORCHESTRATOR-CHECK") == 1`.
  The body line — "After each evaluator pass, the orchestrator checks the generator's
  output against the brief's acceptance criteria … A rubric pass with a failed
  acceptance criterion is a fail: the generator is re-dispatched with a correction
  brief naming the failed criterion and the required correction, distinct from the
  original brief — the re-dispatch is the next iteration's GENERATE, consuming one
  iteration within max_iterations…" — is asserted nowhere. The 82-B2 order check
  constrains only the header's position, and the CHECK SCORE gate line asserts only
  its own text. The body is the 81-B2 fix itself (the orchestrator verdict +
  correction-brief re-dispatch); the header alone proves the step exists, not that
  it does anything.
- Demonstrated (M-OC1): deleting the whole body line (keeping the `# ORCHESTRATOR-CHECK`
  header) leaves verify29 at **310/310**.
- Fix (verifier-only): assert the body line (or its operative sentences — the
  against-acceptance-criteria verdict and the correction-brief re-dispatch) inside
  the EVALUATE → CHECK SCORE span (82-B2 pattern). No tree change needed.

### 92-B3 (minor, verifier): the orch-refine-code step-2/step-3 exception sentences are whole-file counts

- verify29.py:1584 asserts the skill exception (`"Except the step-2
  refactor-cleaner sweep, which is dispatched directly as a single-task factory drone
  — see step 2."`, count == 1, whole file); :1591 does the same for the command
  mirror (`"except the step-3 refactor-cleaner sweep, which the skill dispatches
  directly as a single-task factory drone"`, count == 1, whole file). Each exception's
  function is adjacency to the pointer it qualifies (81-A4: without it the pointer
  overclaims that all work runs "through the shared engine").
- Demonstrated: M-ORC1 (exception substring moved from the skill's :13 pointer line
  to EOF) and M-ORC2 (mirror exception moved from the command's :26 to EOF) each
  leave verify29 at **310/310**. The pointer checks still pass (the full-pointer
  assertion does not include the exception), so the 81-A4 defect returns silently.
- Fix (verifier-only): scope each exception to its operative span — skill: the header
  block (`_wt_head` pattern) or the pointer line itself; command: the usage/intro
  span containing :26 (or the step-3 slice). No tree change needed.

### 92-B4 (minor, verifier): the ecc-gan-planner fallback sentence is a whole-file `in`

- verify29.py:1728–1729 asserts `"STOP and return NEEDS_CONTEXT naming the missing
  direction to the orchestrator instead of invoking the design-lead itself" in _gp`
  — whole file. The sentence is the fallback branch of the Direction-source slot
  (`agents/ecc-gan-planner.md:44`, one long bracketed line); moving it out leaves the
  slot reading "if no direction is recorded, do NOT invent one…" with no action, and
  the sentence sits at EOF as a free-floating instruction. Same class as 90-B1
  (template sentences as whole-file `in` checks).
- Demonstrated (F37): moving the sentence from the :44 bracket to EOF leaves verify29
  at **310/310**. Deletion is caught (the `in` check fails); position is not.
- Fix (verifier-only): scope to the Direction-source bullet — e.g. assert the sentence
  on the line containing `"**Direction source**"` (line-content pattern: the sentence
  and the slot share line :44, so co-location is the property that matters). No tree
  change needed.

## §3 Nits (not counted)

- **Nit 1 — precision on the fix16 citation (not a finding).** The #91-B report's
  "the anchor `sub(` call is at :3808" is off by one: `sub(` starts at
  `fix16/fix16.py:3807`; line 3808 carries the anchor string
  (`"(its upstream \`claude -p\` invocation path does not run in Cursor"`). The
  `fix29.py:438` citation "fix16.py:3808" is correct as the anchor-string line, and
  the call spans 3807–3809 (comment 3805–3806). No change needed; recorded so the
  next citation round does not "correct" :3808 to :3807.

## §4 Tested and NOT filed — adjudications and fresh-hunt greens

### #91-B §4 adjudications re-confirmed at sentence level

| Item | Mutation | Result | Standing |
|---|---|---|---|
| Orchestrate step-4 merge-order bridge | N1: bridge clause out of :93 to EOF | **309/310**, exactly the 7e orchestrate check | Adjudication STANDS |
| Fast-worker preamble bound | N10: short-form tie-breaker sentence out of :92 to EOF | **309/310**, exactly the 7e dispatch-prompt check | Adjudication holds |
| Reasoning-template NEEDS_CONTEXT line (:144) | N12: NEEDS_CONTEXT sentence out of its template to EOF | **309/310**, exactly the 7e dispatch-prompt check | Adjudication holds (same known 7e residual: a staged-source deletion would pass 7e) |
| Redesign.md correction-brief clause | N13: correction-brief sentence out of :68 to EOF | **309/310**, exactly the 7e redesign check | Adjudication STANDS |

### Fresh hunt — green mutations, not filed

| Mutation | Result | Why not filed |
|---|---|---|
| F10 (Nit 1): orch-pipeline carve-out header substring → EOF | 310/310 | Known cosmetic gap, deliberately unfixed per #91-B Nit 1: the operative body (carve-out sentence + tie-breaker) stays in place and is guarded by the 81-B8 order check + 89-B3 window |
| F11a: whole orch-pipeline factory paragraph :62 → EOF | 310/310 | #91-B §4 adjudication: whole-factory-paragraph relocations stay self-contained (every paragraph-scoped check uses `_para_with`, which finds the paragraph wherever it sits) |
| F11c: whole gan-style-harness paragraph :14 → EOF | 310/310 | Same adjudication as F11a |
| F36: whole redesign.md :68 line → EOF | 310/310 | Same adjudication as F11a (paragraph is self-contained; its internal checks are paragraph-scoped or whole-file `in`) |
| F11b: whole feature-expansion paragraph :139 → EOF | 308/310, 7e FE + check-12 | Caught — by 7e order-sensitivity (FE has 2 `_F29` lines). The second failure is check-12 collateral: the move shifts the allow-listed lines below :139 (192/194/196/197/208/215), the known line-number sensitivity of the check-12 allow-list |
| F14: DTF pointer line moved within the step-4→step-5 span | 310/310 | Span granularity is step-level by design (the B5 fix); within-span moves are not distinguished |
| F15: wrapper pointer moved within the header block (to file top) | 310/310 | Header-block granularity is the scoped property (91-B4); within-block moves are not distinguished |
| F19: gan-build 3a line moved within Phase 1 | 310/310 | Phase-1 granularity is the scoped property (91-B3); within-phase moves are not distinguished |
| F21: gan-build step-0 parenthetical moved within line :26 | 310/310 | Step-0 granularity is the scoped property (91-B1); within-step moves are not distinguished |
| F29: recon "Acceptance check:" body deleted, label kept | 310/310 | Settled property per 87-B2: a template slot is a labeled placeholder by design; label presence is the asserted property |
| F34: deep-reasoner.md:17 whole line → EOF | 310/310 | Co-location is the property, not file position: the bound and the under-specified instruction share the line and travel together; nothing is detached. The file carries exactly one `_F29` line, so 7e is vacuous for a whole-line move — but no check needs to pin bullet order in this role file |
| F35: hackathon-mode GLOBAL-ROUTING block line :45 → EOF | 309/310, check-12 only | **Caught, but only by collateral** — see note below; not filed, because the verifier does fail this mutation as written |
| F37 | — | Filed as 92-B4 (see §2) |

**F35 note (observed fragility, not a counted finding).** Moving the hackathon-mode
block line to EOF fails at 309/310, but the failing check is check 12, not any
GLOBAL-ROUTING check: the move shifts `ALLOW_NAMES:47` (`intent-driven-development` /
`product-lens`) to line 46, and the sweep flags it — full-output capture quotes
`rules/hackathon-mode.mdc:46: intent-driven-development,product-lens`. The block's own
checks (count == 1, byte-identity, golden pin) are all position-blind, and
hackathon-mode carries exactly one `_F29` line, so 7e is vacuous for a whole-line move
(the orchestrate block is order-guarded by 7e; the hackathon-mode twin is not). The
catch therefore depends on the check-12 allow-list entry sitting below the moved line;
if that entry were ever re-mapped, the move would pass. This is a demonstrated catch
with a fragile mechanism, not a demonstrated gap — recorded here so a future audit can
re-test it if `ALLOW_NAMES:47` changes. The block is a self-contained rule statement
whose meaning does not depend on its neighbours (unlike the filed pointer/clause
cases), which is why it is not filed alongside 92-B4.

## §5 Verifier-honesty table (verify29.py, read end to end, 2,053 lines)

| Check area | Scoping | Status |
|---|---|---|
| 7c GLOBAL-ROUTING block + golden pin (85-B3) | Block extraction + byte-compare vs `fix29/global-routing-block.txt` | Clean (md5 `68206505` in orchestrate, hackathon-mode, golden) |
| 7c Belief carve-outs, order (81-B8), tie-breaker windows (89-B3, 88-B2) | 600-char windows / paragraph slice | Clean |
| 7c merge-order bridges | FE Collect + OBM Reconcile section-scoped (89-B2); orchestrate step-4 7e-guarded (N1); ladder scoped (90-B2) | Clean |
| 7c correction-brief construction | FE/OP section-scoped (89-B2); ladder scoped (90-B2); redesign 7e-guarded (N13) | Clean |
| 7c harness-gate clause | Paragraph-scoped via `_para_with` (85-B2) | Clean (F1/F1b exact) |
| 7c factory-paragraph bodies | Opening clause only (count == 1) | **92-B1** (OP :62, gan :14 bodies unasserted) |
| 7d(a) contract core | Fenced-block extraction; no-drop + `none` mechanism (87-B2) | Clean (F17 exact) |
| 7d(b) templates | Per-section field labels (84-B1); reasoning + second-pass section-scoped (90-B1, F3 exact); scope sentences per-site (89-B4) | Clean |
| 7d(c) FE format | Item-sliced (87-B2) | Clean (F9 exact) |
| 7d(d) contract refs | Paragraph-scoped (90-B4, F2 exact) | Clean |
| 7d "state the assumption" file-set + unbounded phrase 0× | Tree-wide file-set equality + 0× grep | Clean (F30 exact) |
| 7e staged-vs-built | Order-sensitive line comparison, 7 staged files | Clean, with noted limitation: order-sensitivity is vacuous for single-`_F29`-line files (DTF SKILL.md — fixed by the 91-B5 span scope; deep-reasoner, redesign, hackathon-mode — see §4) |
| 9b model pins | Tree-wide grep + occurrence counts (86-B1) + golden pin | Clean |
| 10i gan mirrors | Section-scoped (90-B3, F13 exact); loop order (82-B2, F5 exact); GENERATE slice (83-B1, 89-B1) | Clean except **92-B2** (ORCHESTRATOR-CHECK body unasserted) |
| 10i gan-build loop wiring | ORCHESTRATOR-CHECK order-guarded; CHECK SCORE gate order-guarded | Clean except 92-B2 |
| 10i pointers | Full-line + span-scoped (87-B1, 90-B5, 91-B4–B8; F7/F8/F25/F26 exact) | Clean |
| 10i gan step-0 pins | Step-0-scoped (91-B1/B2; N2/N3 exact) | Clean |
| 10i planner-spec 3a | Phase-1-scoped (91-B3; N4 exact) | Clean |
| 10i orch-refine-code | Line-sliced step 2 / step 3 (90-B6, F4 exact) | Clean except **92-B3** (exception sentences whole-file) |
| 10i astra-review | Step-3-scoped (90-A1, F8/F26 exact) | Clean |
| 10i planner fallback | Whole-file `in` | **92-B4** |
| 11b fix29 patch log | Census + 0-errors assertions | Clean |

## §6 Fresh hunt — checked and clean

- **DIRECTOR-BRIEF, all 7 fields.** Contract core 7/7 distinct slots + files-out-of-scope
  + no-drop + `none` mechanism (re-checked by direct read, not just the verifier).
  All five dispatch-prompt templates that carry briefs (recon, mechanical, reasoning,
  blind reviewer, worked example) 7/7; the second-pass template is exempt by design
  (opinion-only, carries a NEEDS_CONTEXT line instead). Feature-expansion format 7/7
  (items 1, 2, 3, 4a, 4b, 9). GAN GENERATE block 7/7 present (3 labeled slots +
  4 via the spec.md reference) — the reference is real: the planner writes per-feature
  "[Feature]: [description, acceptance criteria]" into `gan-harness/spec.md`
  (`agents/ecc-gan-planner.md:29`, `:51–52`, `:56`, `:60`); the GENERATE block reads
  spec.md (`commands/gan-build.md:40`) and cites "the acceptance criteria from the
  spec" (:46).
- **NO-GUESSING.** Exactly 5 Belief copies tree-wide (orch-pipeline:72,
  feature-expansion:151, orch-build-mvp:70, dispatch-prompt.md:34 + :92), all carved
  with the tie-breaker; distances re-measured 137–142 chars (carve-out) and 356–361
  chars (tie-breaker), matching #91-B. Unbounded phrase "state the assumption you made
  and proceed" 0× tree-wide. "state the assumption" in exactly the 6 known bounded
  files (deep-reasoner, orchestrate SKILL.md, dispatch-prompt.md, polish-pass SKILL.md
  + impeccable-critique.md, systematic-debugging). "instead of NEEDS_CONTEXT" 0×.
- **VERIFY-MERGE.** All 8 construction sites verify against the brief's acceptance
  criteria with a correction-brief path naming the failed criterion (orchestrate
  ladder :252, feature-expansion :158, orch-pipeline Phase 5 Review :74, gan
  ORCHESTRATOR-CHECK :63 + planner-spec 3a :30, react-build step 6 :18, redesign :68,
  astra-review :35). (Three further grep hits in `gan-style-harness` :14/:69/:155 are
  mirror restatements of the same rule, not separate construction sites.)
- **Harness-gate clause** ("in Cursor, slots refill per wave, not per completion") in
  all 5 factory paragraphs (orch-pipeline :62, feature-expansion :139, gan :14,
  redesign :68, orchestrate step 4 :93).
- **Counts / pins / identity.** 67/45/48/55. GLOBAL-ROUTING block md5 `68206505` in
  orchestrate, hackathon-mode, and the golden file. `fix29.py` byte-identical to its
  template (`fbd459c7…`). "Factory routing (fix #29" in 13 files; `GLOBAL-ROUTING_F29`
  24 raw occurrences in 18 files — both matching the run-10 counts. No deepseek-/qwen-
  slugs (0), bare `grok-4.6-high-fast` 0, `grok-4.7-high` ×49.

## §7 Staged-vs-built drift re-check

- Direct `diff` of all 7 staged files vs built (counting `^[<>]` lines):
  orchestrate 6, dispatch-prompt 0, deep-reasoner 0, feature-expansion 22,
  design-taste-frontend SKILL.md 11, redesign.md 0, hackathon-mode 2 — **41 diff lines
  across 4 files**, exactly the MANIFEST §2(c)(9)/OWED-29-5 enumeration. All are the
  recorded by-design build-time transforms (agent-citation expansions,
  `claude -p` → CLI-subprocess, FE content rewrites, DTF description block).
- fix16 anchor logic unchanged: the anchor string is at `fix16/fix16.py:3808`
  (`"(its upstream \`claude -p\` invocation path does not run in Cursor"`), inside the
  `sub(` call spanning 3807–3809; build.sh runs fix16 every build. Syncing staged
  hackathon-mode:38 to the built text would still break the build.

## §8 Methodology note

- Fresh-copy-per-mutation harness: `/tmp/a92b/pristine` (one copy of the built tree)
  re-copied to `/tmp/a92b/built` for each of 60 runs (55 mutations + 3 re-runs +
  M-GAN3 + the F35 full-output capture); symlinks in `/tmp/a92b/` point at the real
  `fix28/`, `fix29/`, `new-rules/`, `new-skills/` so checks 7e/10g/11/11b run
  meaningfully. No in-place restores anywhere in this audit. Mirror baseline 310/310.
- Three driver errors in the first pass, all in the harness (not the verifier), fixed
  and re-run with exact results: F5 (the `# CHECK SCORE` line is indented inside the
  code fence — the driver's `startswith` missed it; fixed to `strip().startswith`),
  F10 (the carve-out header is a substring of the long Belief line :72, not a
  standalone line — fixed to a substring move), F27 (the FE fix-loop sentence starts
  with capital "The re-dispatch…", the driver used lowercase "the…" — fixed to the
  `_CORR_BRIEF` substring). Re-runs: F5 → 309/310 exactly the order check; F10 →
  310/310 (Nit 1 confirmed); F27 → 309/310 exactly the 7c FE correction-brief check.
- F11b/F35 check-12 collateral: moving a line above an allow-listed line shifts the
  allow-list line numbers, so check 12 fails alongside the intended check. The failure
  sets are still exact for the intended checks; the check-12 failure is a known
  line-number sensitivity of the allow-list (verify29.py's own comment requires
  re-running the census on line shifts), not a second independent catch of the moved
  text — except in F35, where it is the *only* catch (see §4).
- No conclusion in this report rests on a green result alone without a named mutation:
  every filed finding names the exact deletion/move and the verify29.py line it
  evades; every tested-not-filed green is listed in §4 with its reason.
- Scratch removed (`/tmp/a92b/`, `/tmp/a92b-driver/` deleted). Real tree untouched.
