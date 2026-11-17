# Audit #91-B — brief/verify coherence + verifier honesty (fix #29, round 12)

**Verdict: NOT PASS — 0 blocking, 8 minor (91-B1–B8). All eight are verifier-only; the tree is currently correct on every point.**

Auditor B (brief/verify coherence + verifier honesty). Read-only except this report.
Method: read `fix29/verify29.py` end to end (2,010 lines); independently re-ran it —
**309/309, exit 0** (real tree, before any scratch work). All mutations below ran on a
scratch copy at `/tmp/a91b/built` (real copy of the built tree + a real copy of
`new-skills/orchestrate/` for staged mirrors, symlinks to the real `fix28/`, `fix29/`,
`new-rules/`, `new-skills/` so checks 7e/10g/11/11b run meaningfully — the #88-B/#89-B/#90-B
pattern). Scratch baseline 309/309; final baseline re-run after all mutations 309/309;
scratch removed after. The real tree was never edited by this audit.

## §1 Disposition of the #90 fixes — all VERIFIED-FIXED

### 90-A1 (blocking, tree) — VERIFIED-FIXED in full

- Built `commands/astra-review.md:34` carries the factory pointer verbatim, immediately
  after the `:32` fix-cycle line; `:35` carries the extended second blind pass verbatim:
  verifies "against the fix brief's acceptance criteria", "a zero-blocker verdict with a
  failed acceptance criterion is a fail", and re-dispatches "with a correction brief naming
  the failed acceptance criterion and the required correction, distinct from the original
  brief (at most two correction re-dispatches; …)".
- The three new astra-review checks pass (309/309). Reproduced in scratch (R9): moving
  the pointer line :34 and the :33 line :35 to EOF → **307/309**, failing exactly the two
  Step-3-scoped checks (pointer in full, second blind pass) — no collateral.
- Correction-brief construction sites are now **eight** (orchestrate ladder :252,
  feature-expansion :158, orch-pipeline Phase 5 Review, gan ORCHESTRATOR-CHECK :63 +
  planner-spec 3a :30, react-build step 6 :18, redesign :68, astra-review :35), all naming
  the failed criterion. "Factory routing (fix #29" is in **13 files**; `GLOBAL-ROUTING_F29`
  is **24 raw occurrences in 18 files** — matching the coordinator's run-10 counts.

### 90-B1–B6 (verifier-only) — all VERIFIED-FIXED

Reproduced by re-running the coordinator's T-mutations on the scratch mirror (round 2,
clean harness; see §8 for the round-1 harness bug, which did not affect these results
beyond one systematic +1 artifact that round 2 eliminates):

| Fix | Reproduction | Result |
|---|---|---|
| 90-B1 reasoning + second-pass section-scoped (`_dp_section`) | R1: both sentences out of their template sections | **307/309**, exactly the two 90-B1 checks |
| 90-B2 ladder scoped to the escalation-ladder section | R2c: whole line :252 moved past the `### Mixing…` section boundary (the coordinator's T-k shape) | **308/309**, exactly the ladder check |
| 90-B3 gan mirrors section-scoped + rubric-pass split 1→3 | R3 (round 1): Architecture :69 + Scoring :155 lines out of section | **304/309**, exactly the four gan checks (3 rubric-pass per-site + note/bullet — see note below) |
| 90-B4 contract refs paragraph-scoped (`_para_with`) | R4 (round 1): both contract-ref sentences out of their factory paragraphs | **304/309**, exactly the four contract-ref checks (7d(d) + 10i per file) |
| 90-B5 pointers scoped to operative spans | R5 react-build pointer → EOF; R6 common-agents :26 → EOF; R7 gan-build :12 + gan-design :10 → EOF | **307/309** (R5: exactly the pointer check), **306/309** (R6: exactly factory-line + COST-AWARE), **305/309** (R7: exactly the three pointer/COST-AWARE checks) |
| 90-B6 orch-refine-code line-sliced to step 2 / step 3 | R8 (round 1): skill step-2 qualification + command step-3 mirror to EOF | **306/309**, exactly the two orch-refine-code checks |

Note on R3–R8: these ran in round 1, whose restore bug (§8) left exactly one extra
failure in every run (the 90-B1 reasoning check, 308/309 baseline). The failure *sets*
are nonetheless exact: each run failed the intended checks plus that one artifact, and
nothing else. Round-2 re-runs of R1/R2c on the clean harness match exactly, confirming
the harness, not the fixes, was at fault. The 90-B2 step-4-bridge half of the old
adjudication is addressed separately in §4 (N1).

## §2 New findings — 91-B1–B8 (all minor, verifier-only)

Same presence-not-position class as 83-B1/85-B2/87-B2/88-B1/88-B2/89-B1–B4/90-B1–B6.
Tree currently correct on every point; each finding is demonstrated by a scratch
mutation (tree untouched) that leaves verify29 green at 309/309.

### 91-B1 (minor, verifier): the gan-build step-0 parenthetical has NO check at all

- The 82-A1 inline-invocation pin in `commands/gan-build.md:26` —
  "(the design-lead is invoked inline as the orchestrator here, not spawned as a drone —
  a spawned execution must carry a director brief)" — is asserted **nowhere** in verify29.py.
  The string "invoked inline" occurs in verify29.py exactly once: line 1631, the
  **gan-design** check. The gan-build twin (the original 82-A1 fix) has no assertion.
- Demonstrated (N2): deleting the parenthetical from `gan-build.md:26` in scratch leaves
  verify29 at **309/309**. No sibling catches it: the gan-build pointer check asserts
  only the pointer line; gan-build is ECC-origin (no 7e coverage).
- Fix (verifier-only): add a step-0-scoped check in 10i, mirroring the gan-design one:
  `_gb_step0 = _gb[_gb.index("0. Design-direction check"):_gb.index("1. Launch the `gan-planner`")]`,
  then assert `_gb_step0.count("(the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief)") == 1`.

### 91-B2 (minor, verifier): the gan-design step-0 parenthetical is a whole-file count

- verify29.py:1631 asserts `_gd.count("…invoked inline…") == 1` — whole-file, not
  step-0-scoped like its sibling pointer check (`_gd_head`, 90-B5).
- Demonstrated (N3): moving the parenthetical from `gan-design.md:19` to EOF leaves
  verify29 at **309/309**. If the pin drifted to the Loop section, step 0 would read as
  a spawn again and no check would fire.
- Fix (verifier-only): scope to the step-0 slice,
  `_gd[_gd.index("0. Design-direction check"):_gd.index("1. Create `gan-harness/`")]`,
  and assert the parenthetical inside it.

### 91-B3 (minor, verifier): the gan-build planner-spec check is a whole-file count

- verify29.py:1607 asserts `_gb.count("3a. Orchestrator checks the planner's spec against the brief before Phase 2") == 1`.
- Demonstrated (N4): moving the 3a line (:30) to EOF leaves verify29 at **309/309**.
  The 82-B2 note ("its `3a.` label pins it by numbering") does not hold: the label
  travels with the line, so a relocated 3a still passes while sitting after Phase 2,
  where "before Phase 2" is incoherent. The ORCHESTRATOR-CHECK order assertion (82-B2)
  does not cover this line.
- Fix (verifier-only): scope to the Phase 1 slice,
  `_gb[_gb.index("### Phase 1: Planning (Planner Agent)"):_gb.index("### Phase 2: Generator-Evaluator Loop")]`,
  and assert the 3a line inside it.

### 91-B4 (minor, verifier): the five orch-* wrapper pointers are whole-file counts

- verify29.py:1511 asserts `_wt.count(_WRAPPER_POINTER) == 1` per wrapper skill, with no
  positional scope — the 90-B5 scoping covered the four command/rule pointers but not
  these five. The pointer's function is attachment to the thin-wrapper intro ("this
  operation runs through the shared `orch-pipeline` engine…"); at EOF it qualifies nothing.
- Demonstrated (N5): moving the `orch-build-mvp` pointer line (:13) to EOF leaves
  verify29 at **309/309**. The other four share the identical check (same loop, same
  string, pointer at :13 in all five); one was mutated, all five are filed.
- Fix (verifier-only): scope each to the header block, e.g.
  `_wt_head = _wt[:_wt.index("## When to Use")]` (first `##` heading is at :17 in
  orch-build-mvp, :15 in the other four; the pointer is at :13 in all five) and count
  `_WRAPPER_POINTER` inside it.

### 91-B5 (minor, verifier): the design-taste-frontend SKILL.md:455 pointer is a whole-file `in`

- verify29.py:809 asserts `"factory routing for the redesign flow lives there" in
  read("skills/design-taste-frontend/SKILL.md")` — whole-file. The pointer's function is
  attachment to the redesign-flow invocation at :455 ("follow the Hallmark redesign flow
  … — factory routing for the redesign flow lives there").
- Demonstrated (N6): moving line :455 to EOF leaves verify29 at **309/309**. 7e cannot
  guard this one: `design-taste-frontend/SKILL.md` carries exactly **one** `_F29` line,
  so a whole-line move preserves the `_F29` line list (same vacuity as the ladder :252
  case that 90-B2 fixed).
- Fix (verifier-only): assert the pointer clause on the redesign-flow line itself, e.g.
  extract the line containing "follow the Hallmark redesign flow" and assert
  "factory routing for the redesign flow lives there" inside it (the 7d(c) `_fe_item`
  line pattern).

### 91-B6 (minor, verifier): the gan-build pointer check is fragment-only

- verify29.py:1593 asserts only `"the planner, generator, and evaluator passes below
  run as factory drones per `gan-style-harness`"` — a fragment of the :12 pointer line.
  The director-brief enumeration, the no-guessing clause, and the orchestrator-verification
  clause are unasserted (the COST-AWARE sentence is asserted separately at :1595).
- Demonstrated (N7): deleting the middle of the pointer line —
  " — each with a director brief (goal, files in/out of scope, constraints, acceptance
  criteria, verification steps, what to return), no-guessing, and orchestrator verification
  against the brief's acceptance criteria (a rubric pass with a failed acceptance criterion
  is a fail)" — leaves verify29 at **309/309**. Same class as 87-B1 (react-build
  prefix-only pointer, fixed by asserting the full pointer).
- Fix (verifier-only): assert the full pointer line in `_gb_head` (87-B1 pattern); keep
  the separate COST-AWARE check as defense-in-depth.

### 91-B7 (minor, verifier): the gan-design pointer check is prefix-only

- verify29.py:1638 asserts only `"**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the
  design-lead is invoked inline as the orchestrator in Setup step 0"` — the head of the
  :10 pointer line. The loop clause that follows ("; the generator/evaluator loop below
  runs as factory drones per the `/gan-build` pointer, each with a director brief (goal,
  files in/out of scope, constraints, acceptance criteria, verification steps, what to
  return), no-guessing, and orchestrator verification against the brief's acceptance
  criteria.") is unasserted.
- Demonstrated (N8): deleting that tail leaves verify29 at **309/309**. Same class as
  87-B1.
- Fix (verifier-only): assert the full pointer line in `_gd_head`.

### 91-B8 (minor, verifier): the common-agents factory-line check is lead-clause-only

- verify29.py:1581 asserts only `"Implementation-agent dispatch follows the factory
  routing in orchestrate's GLOBAL-ROUTING block (fix #29, GLOBAL-ROUTING_F29)"` — the
  head of the :26 line. The operative middle (": every implementation dispatch carries
  a director brief, no-guessing applies, and the orchestrator verifies the output against
  the brief's acceptance criteria before use.") is unasserted (the COST-AWARE sentence
  is asserted separately at :1585).
- Demonstrated (N9): deleting that middle leaves verify29 at **309/309**. Same class as
  87-B1.
- Fix (verifier-only): assert the full :26 line in `_ca_imm` (87-B1 pattern); keep the
  separate COST-AWARE check as defense-in-depth.

## §3 Nits (not counted)

- **Nit 1 — carve-out header position (N11).** The `"**Bounded by NO-GUESSING (fix #29,
  NO-GUESSING_F29):**"` count==1 checks (orch-pipeline, feature-expansion,
  orch-build-mvp) are whole-file. Moving the orch-pipeline header alone to EOF leaves
  verify29 at **309/309**. Cosmetic only: the operative body (carve-out sentence +
  tie-breaker) stays in place and is guarded by the 81-B8 order check and the 89-B3
  600-char window. No fix required; optionally scope the header check to the Belief
  paragraph.
- **Nit 2 — drift record understates staged-vs-built drift.** MANIFEST §2(c)(9) and
  fix29.py OWED-29-5 say "exactly 4 diff lines" (orchestrate :100/:274/:281,
  hackathon-mode :38). The actual staged-vs-built diff is **41 diff lines across 4
  files**: orchestrate 3 changed lines, hackathon-mode 1, feature-expansion 11
  (:3 brainstorming sentence, :33–34 ECC-process rewrite, :12/:49/:137/:164/:196/
  :198/:199/:217 agent-citation expansions), design-taste-frontend SKILL.md
  description block 5 lines → 6 (:9–14). All are by-design build-time transforms, not
  regressions: the content rewrites are encoded in build.sh (:580 FE :3, :622 DTF
  description, :746 FE :33–34), the citation expansions are the same class as the
  recorded orchestrate ones, and the built files are newer than staged (run 10,
  Nov 17 00:25 vs staged Nov 16 22:09) — i.e. the build produced them, this is not
  post-build staged drift. No fix29 property is affected (`_F29` lines byte-identical).
  Fix: correct the §2(c)(9)/OWED-29-5 enumeration. (Also: staged DTF SKILL.md carries
  the pointer at :454, built at :455 — a 1-line shift from the description block; 7e
  compares line texts, not numbers, so it passes.)
- **Nit 3 — stale citations in fix29.py OWED-29-5.** Still cites orchestrate
  ":100/:273/:280" (live :274/:281 — the manifest already corrected this; the fix29.py
  text was not updated) and "fix16.py:3807" (the anchor `sub(` call is at :3808; the
  call spans 3805–3809). Fix the citations.

## §4 Tested and NOT filed — adjudications confirmed at sentence level

The #90-B methodology note says F-B/F-E2/F-C-class mutations are sentence-level moves,
not line moves. I applied that standard to the adjudicated items; all four hold even
at sentence level, because in each case the target sentence shares its line with a
`_F29` token and 7e compares `_F29` lines byte-identically — any sentence-level move
must edit the `_F29` line itself:

| Item | Mutation | Result | Standing |
|---|---|---|---|
| Orchestrate step-4 merge-order bridge (89-B2 adjudication) | N1: bridge clause out of :93 to EOF | **308/309**, exactly the 7e orchestrate check | Adjudication STANDS, stronger than the line-move demonstration |
| Fast-worker preamble bound (89-B/90-B proxy-guarded) | N10: short-form tie-breaker sentence out of :92 to EOF | **308/309**, exactly the 7e dispatch-prompt check | Adjudication holds — the sentence shares line :92 with the `_F29` bound marker; the bound itself is additionally guarded by the 81-B8 order check |
| Reasoning-template NEEDS_CONTEXT line (:144) | N12: line's NEEDS_CONTEXT sentence out of its template to EOF | **308/309**, exactly the 7e dispatch-prompt check | Not filed — no direct check asserts this line, but it shares line :144 with the `_F29` bound marker, so 7e guards it against any build-time move/edit. Residual (same as every 7e-guarded item): a staged-source deletion would pass 7e; that is the known 7e limitation, not a new class |
| Redesign.md checks (90-B adjudication) | N13: correction-brief clause out of :68 to EOF | **308/309**, exactly the 7e redesign check | Adjudication STANDS at sentence level |

Also re-confirmed by code-read (not re-mutated): the Belief-line carve-out `in` checks
are guarded by the 81-B8 order loop (carve-out must follow every Belief occurrence
within 600 chars), and whole-factory-paragraph relocations stay self-contained (every
paragraph-scoped check uses `_para_with`, which finds the paragraph wherever it sits).

## §5 Verifier-honesty table (verify29.py, read end to end, 2,010 lines)

| Check area | Scoping | Status |
|---|---|---|
| 7c GLOBAL-ROUTING block + golden pin (85-B3) | Block extraction + byte-compare vs `fix29/global-routing-block.txt` | Clean |
| 7c Belief carve-outs, order (81-B8), tie-breaker windows (89-B3, 88-B2) | 600-char windows / paragraph slice | Clean |
| 7c merge-order bridges | FE Collect + OBM Reconcile section-scoped (89-B2); orchestrate step-4 7e-guarded (N1); ladder scoped (90-B2, R2c) | Clean |
| 7c correction-brief construction | FE/OP section-scoped (89-B2); ladder scoped (90-B2); redesign 7e-guarded (N13) | Clean |
| 7c harness-gate clause | Paragraph-scoped via `_para_with` (85-B2) | Clean |
| 7d(a) contract core | Fenced-block extraction; no-drop + ``none`` mechanism (87-B2) | Clean |
| 7d(b) templates | Per-section field labels (84-B1); reasoning + second-pass section-scoped (90-B1, R1); scope sentences per-site (89-B4) | Clean |
| 7d(c) FE format | Item-sliced (87-B2) | Clean |
| 7d(d) contract refs | Paragraph-scoped (90-B4, R4) | Clean |
| 7d "state the assumption" file-set + unbounded phrase 0× | Tree-wide file-set equality + 0× grep | Clean |
| 7e staged-vs-built | Order-sensitive line comparison, 7 staged files | Clean, with noted limitation: order-sensitivity is vacuous for single-`_F29`-line files (DTF SKILL.md — see 91-B5) |
| 9b model pins | Tree-wide grep + occurrence counts (86-B1) + golden pin | Clean |
| 10i gan mirrors | Section-scoped (90-B3, R3); loop order (82-B2); GENERATE slice (83-B1, 89-B1) | Clean |
| 10i gan-build loop wiring | ORCHESTRATOR-CHECK order-guarded; CHECK SCORE gate order-guarded | Clean except 91-B3 (planner-spec 3a unscoped) |
| 10i pointers | react-build full + head-scoped (87-B1, 90-B5); astra Step-3-scoped (90-A1) | **91-B4** (wrappers unscoped), **91-B5** (DTF unscoped), **91-B6/91-B7/91-B8** (fragment/prefix/lead-clause-only) |
| 10i gan-build step-0 pin | — | **91-B1** (no check at all) |
| 10i gan-design step-0 pin | Whole-file count | **91-B2** (unscoped) |
| 10i orch-refine-code | Line-sliced step 2 / step 3 (90-B6, R8) | Clean |
| 10i astra-review | Step-3-scoped (90-A1, R9) | Clean |
| 11b fix29 patch log | Census + 0-errors assertions | Clean |

## §6 Fresh hunt — checked and clean

- **DIRECTOR-BRIEF, all 7 fields.** Contract core 7/7 distinct slots + files-out-of-scope
  + no-drop + ``none`` mechanism (re-checked by direct read, not just the verifier).
  All five dispatch-prompt templates (recon, mechanical, reasoning, blind reviewer,
  worked example) 7/7. Feature-expansion format 7/7 (items 1, 2, 3, 4a, 4b, 9).
  GAN GENERATE block 7/7 present (3 labeled slots + 4 via the spec.md reference) —
  the reference is real: the planner writes per-feature "[Feature]: [description,
  acceptance criteria]" into `gan-harness/spec.md` (`agents/ecc-gan-planner.md:51–52`,
  `:56`, `:60`); the GENERATE block reads spec.md (`commands/gan-build.md:40`) and
  cites "the acceptance criteria from the spec" (:46).
- **NO-GUESSING.** Exactly 5 Belief copies tree-wide (orch-pipeline, feature-expansion,
  orch-build-mvp, dispatch-prompt.md ×2), all carved with the tie-breaker; distances
  re-measured 111–142 chars (carve-out) and 356–361 chars (tie-breaker). Unbounded
  phrase "state the assumption you made and proceed" 0× tree-wide. "state the
  assumption" in exactly the 6 known bounded files (deep-reasoner, orchestrate
  SKILL.md, dispatch-prompt.md, polish-pass SKILL.md + impeccable-critique.md,
  systematic-debugging). "instead of NEEDS_CONTEXT" 0×.
- **VERIFY-MERGE.** All 8 consumption sites verify against the brief's acceptance
  criteria with a correction-brief path naming the failed criterion (see §1).
- **Harness-gate clause** ("in Cursor, slots refill per wave, not per completion") in
  all 5 factory paragraphs (orch-pipeline :62, feature-expansion :139, gan :14,
  redesign :68, orchestrate step 4 :93).
- **Counts / pins / identity.** 67/45/48/55. GLOBAL-ROUTING block md5 `68206505` in
  orchestrate, hackathon-mode, and the golden file. `fix29.py` byte-identical to its
  template. No deepseek-/qwen- slugs (0), bare `grok-4.6-high-fast` 0,
  `grok-4.7-high` ×49.

## §7 Staged-vs-built drift re-check

- fix16 anchor logic unchanged: `fix16.py:51–60` `sub(f, old, new, count=1)` appends to
  ERRORS (build fails) on any anchor miss; the hackathon-mode anchor is at
  `fix16.py:3808`; build.sh:23222 runs fix16 every build.
- The 4 recorded drift lines are exactly as recorded: orchestrate :100/:274/:281
  (agent-citation expansions), hackathon-mode :38 (`claude -p` → CLI-subprocess).
- Additional drift exists but is by-design (see Nit 2): the true total is 41 diff lines
  across 4 files, all build-time transforms; the "exactly 4" enumeration in the manifest
  needs correcting, not the tree.

## §8 Methodology note — round-1 harness bug (corrected, no effect on conclusions)

The round-1 mutation script restored multi-snapshot mutations in forward order, so a
same-file double snapshot (R1, two dispatch-prompt.md edits) restored the
post-first-mutation text last, leaving the reasoning-template sentence deleted in the
scratch tree for all subsequent round-1 runs. Every round-1 run therefore carried one
systematic extra failure (the 90-B1 reasoning check; round-1 final baseline 308/309).
Round 1's *failure sets* are still exact (each run failed its intended checks plus that
one artifact), and round 2 — fresh scratch copy, restores in reverse order — reproduces
R1 and R2c exactly (307/309, 308/309) and confirms N1–N13 cleanly, with final baseline
309/309. No conclusion in this report rests on round-1 numbers alone: R3–R8 are
reported with the artifact disclosed, and every new finding (91-B1–B8) was confirmed
on the clean round-2 harness at 309/309 green.
