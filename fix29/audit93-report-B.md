# Audit #93-B — brief/verify coherence + verifier honesty (fix #29, round 14)

**Verdict: NOT PASS — 0 blocking, 2 minor (93-B1, 93-B2).**

Auditor B (brief/verify coherence + verifier honesty). Read-only except this report.
Method: read `fix29/verify29.py` end to end (2,084 lines); independently re-ran it —
**311/311, exit 0** (real tree). All mutations below ran on a scratch mirror at
`/tmp/a93b/built` (real copy of the built tree + symlinks to the real `fix28/`,
`fix29/`, `new-rules/`, `new-skills/` so checks 7e/10g/11/11b run meaningfully —
the #92-B pattern), with a **fresh copy per mutation — no restores**. Mirror
baseline 311/311. 33 mutation runs + 1 demo-verifier run. Scratch removed after.
The real tree was never edited by this audit.

## §1 Disposition of the #92-B fixes — all VERIFIED-FIXED

Reproduced the coordinator's nine scratch mutations on fresh mirrors (one fresh
copy per mutation). Every one fails exactly its intended check at 310/311.

| Fix | Reproduction | Result |
|---|---|---|
| 92-B1 OP paragraph | M-OP1: COST-AWARE sentence deleted from `orch-pipeline:62` | **310/311**, exactly the OP full-paragraph check (verify29.py:1504) |
| 92-B1 OP paragraph | M-OP2: VERIFY-MERGE sentence deleted from `orch-pipeline:62` | **310/311**, exactly the OP full-paragraph check (:1504) |
| 92-B1 gan paragraph | M-GAN1: COST-AWARE sentence deleted from `gan-style-harness:14` | **310/311**, exactly the gan full-paragraph check (:1538) |
| 92-B1 gan paragraph | M-GAN2: NO-GUESSING sentence deleted from `gan-style-harness:14` | **310/311**, exactly the gan full-paragraph check (:1538) |
| 92-B1 gan paragraph | M-GAN3: VERIFY-MERGE tail deleted from `gan-style-harness:14` | **310/311**, exactly the gan full-paragraph check (:1538) |
| 92-B2 OC body | M-OC1: ORCHESTRATOR-CHECK body line deleted, header kept (`gan-build.md:63`) | **310/311**, exactly the OC body check (:1661) |
| 92-B3 ORC skill | M-ORC1: step-2 exception substring moved from skill `:13` to EOF | **310/311**, exactly the step-2 exception check (:1596) |
| 92-B3 ORC command | M-ORC2: step-3 exception moved from command `:26` to EOF | **310/311**, exactly the step-3 exception check (:1608) |
| 92-B4 planner | F37: fallback sentence moved out of the Direction-source line (`:44`) to EOF | **310/311**, exactly the B4 check (:1759) |

The 92-B1 fix is genuinely full-line, not a longer opening clause: the asserted
strings equal the file lines exactly (OP 1,259 chars, gan 1,604 chars, verified by
direct comparison — earlier awk lengths of 1,265/1,612 are byte counts of the
multibyte em-dashes, not character counts; the MANIFEST's 1,259/1,604 figures are
correct). Same for the OC body line (809 chars, exact).

## §2 New findings — 93-B1, 93-B2 (both minor)

### 93-B1 (minor, verifier): the gan-build planner-spec 3a check is lead-only

- verify29.py:1667–1668 asserts only
  `_gb_ph1.count("3a. Orchestrator checks the planner's spec against the brief before Phase 2") == 1`
  — the first ~90 characters of the 616-character line `commands/gan-build.md:30`.
  The rest of the line is unasserted: the match criteria ("the spec's files,
  scope, and acceptance criteria must match the brief's goal, files in/out of
  scope, constraints, and acceptance criteria") and the failure path ("If the
  spec fails the check, the planner is re-dispatched with a correction brief
  naming the failed criterion and the required correction, distinct from the
  original brief (at most two correction re-dispatches, per the plugin's 2-round
  fix-loop convention; if the spec still fails, stop and report the failure with
  evidence)").
- The tail's key phrases occur 0× in verify29.py: "must match the brief",
  "2-round fix-loop", "If the spec fails the check", "stop and report the failure
  with evidence". "re-dispatched with a correction brief naming the failed
  criterion" occurs 1× — in the ORCHESTRATOR-CHECK body check (:1662), a
  different line (the generator's re-dispatch, not the planner's).
- Demonstrated (both **311/311**, green):
  - H1: delete the entire `:30` tail after "before Phase 2" (keep the asserted lead).
  - H1b: delete only the failure-path sentence (keep the lead and the match criteria).
- This is the 92-B2 defect one line up: the 92-B2 fix asserted the full
  ORCHESTRATOR-CHECK body line, but the planner-spec check — the 81-B2 fix's
  planner half, and one of the eight VERIFY-MERGE construction sites
  (`gan-build.md:30`) — is still label-only. A rebuild that dropped the
  planner's correction-brief path would pass silently; the site would no longer
  construct a correction brief while the check stays green.
- Fix (verifier-only): assert the full `:30` line in `_gb_ph1` (87-B1 pattern),
  exactly as the 92-B2 fix did for the OC body line. No tree change needed.

### 93-B2 (minor, tree + verifier): recon and reasoning templates lack the Interface slot, and 7d(b) never asserts it

- The seven-field contract (dispatch-prompt.md:15) is "Goal, Inputs, Constraints
  (incl. files out of scope), Interface, Acceptance check, Verification steps,
  Return format", and :15 states it "binds every implementation dispatch (recon,
  mechanical, reasoning)". The contract-core check 7d(a) asserts all seven slots
  including `Interface:` (verify29.py:830).
- But the recon and reasoning templates carry only 6 of the 7 slots — direct
  per-section counts (`Interface:` occurrences): skeleton 0 (names it in the
  enumeration only), **recon 0, mechanical 1, reasoning 0**, blind reviewer 0,
  worked example 1. No `Interface` in any other spelling appears in the file
  (grep `-i interface` hits only :15, :23, :105, :225).
- verify29.py:871–872, the 7d(b) tuple, is
  `("Goal:", "Inputs:", "Constraints:", "Acceptance check:", "Verification steps:", "files out of scope", "Return format:")`
  — seven entries, but `Interface:` is not one of them; `files out of scope`
  (a sub-element of Constraints) is substituted for it. The comment above it
  still claims "Each template now asserts all seven field labels" (#84-B1).
- Demonstrated: the current tree passes 311/311 with the slot absent (real-tree
  and mirror baselines). Decisive cross-check: a scratch copy of verify29.py
  with `"Interface:"` added to the tuple fails at **313/316**, exactly the recon,
  reasoning, and blind-reviewer `carries Interface:` checks (mechanical and
  worked example pass).
- Scope is recon + reasoning only. The blind reviewer is exempt by design: :15
  gives it its own contract ("verification gate — with Verification steps and
  files-out-of-scope slots"), and it is not an implementation brief. The
  second-pass template is exempt (opinion-only). So the correct fix asserts
  `Interface:` for the three implementation templates + worked example, not for
  all five sections.
- This corrects two standing claims: #84-B1's "Each template now asserts all
  seven field labels" (the tuple never did) and #92-B §6's "All five
  dispatch-prompt templates that carry briefs … 7/7" (recon, reasoning, and blind
  reviewer are 6/7 on the contract's own enumeration; blind reviewer by design).
  Same class as 81-A1/B6 (worked example missing Verification steps).
- Fix: add an `Interface:` line to the recon and reasoning templates (`none` per
  the contract's no-drop rule — "a field with nothing to list is written as
  `none`, never deleted" — or the mechanical wording where it applies; the
  coordinator decides the wording), and add `"Interface:"` to the 7d(b) tuple
  for the implementation templates + worked example (keep blind reviewer and
  second-pass on their own recorded contracts). Tree + verifier.

## §3 Nits (not counted)

None. The fix16 citation precision note from #92-B Nit 1 re-verified (see §5):
`sub(` starts at `fix16/fix16.py:3807`, the anchor string is at `:3808`, the call
spans 3807–3809, and `fix29.py:438`'s "fix16.py:3808" citation remains correct as
the anchor-string line. No change needed.

## §4 Tested and NOT filed — adjudications and fresh-hunt greens

### #92-B §4 adjudications re-confirmed at sentence level

| Item | Mutation | Result | Standing |
|---|---|---|---|
| Orchestrate step-4 merge-order bridge | N1: bridge clause out of :93 to EOF | **310/311**, exactly the 7e orchestrate check | Adjudication STANDS |
| Fast-worker preamble bound | N10: short-form tie-breaker sentence out of dispatch-prompt :92 to EOF | **310/311**, exactly the 7e dispatch-prompt check | Adjudication holds |
| Reasoning-template NEEDS_CONTEXT line (:144) | N12: "If under-specified: return NEEDS_CONTEXT naming exactly what is missing — do not guess." out of its template to EOF | **310/311**, exactly the 7e dispatch-prompt check | Adjudication holds (same known 7e residual: a staged-source deletion would pass 7e) |
| Redesign.md correction-brief clause | N13: correction-brief sentence out of :68 to EOF | **310/311**, exactly the 7e redesign check | Adjudication STANDS |

### F35 fragility note — re-tested, mechanism still holds, gap has NOT opened

F35 (hackathon-mode GLOBAL-ROUTING block line :45 → EOF) still fails at
**310/311**, and the failing check is still check 12 only
("CUT-name sweep: zero live dispatches …"), not any GLOBAL-ROUTING check: the
move shifts `ALLOW_NAMES:47` (`intent-driven-development` / `product-lens`) to
line 46, uncovered by the allow-list, so the sweep flags it. The block's own
checks (count == 1, byte-identity, golden pin) are all position-blind, and
hackathon-mode carries exactly one `_F29` line, so 7e is vacuous for a
whole-line move. The catch therefore still depends entirely on the check-12
allow-list entry sitting below the moved line; if that entry were ever
re-mapped, the move would pass. This remains a demonstrated catch with a fragile
mechanism, not a demonstrated gap — recorded, not filed, as in #92-B.

### Fresh hunt — green mutations, not filed

| Mutation | Result | Why not filed |
|---|---|---|
| H6: OC body line moved within the `_gb_loop` slice (just before `# CHECK SCORE`) | 311/311 | Span granularity is step-level by design (F14/F19 class); the move is one line past a blank line inside the step, no semantic change |
| H7: unbounded phrase "state the assumption you made and proceed" planted as a comment in `hooks/adapter.js` | 311/311 | Check scope is skills/rules/commands/agents by design (81-B1/B8(ii)); no brief text lives in hooks/ or README, and fix29.py writes only to the four dirs — not a regression path |
| H8: GENERATE Verification-steps line moved within the `_gen` slice | 311/311 | Span granularity (F14 class) |
| H10: astra-review pointer moved within the Step 3 slice (just before `## Verdict`) | 311/311 | Span granularity (90-B5 pattern) |
| H13: correction-brief clause deleted from gan Architecture note `:69` only | 311/311 | Mirror restatement: the rule is guarded in full by the gan factory-paragraph full-line check (:1538); the note check claims only prefix presence. The 90-B3 per-site rule applies to the rubric-pass sentence, which IS asserted per-site |
| H14: correction-brief clause deleted from gan Scoring bullet `:155` only | 311/311 | Same as H13 |
| H15: FE format item-4b elaboration tail deleted ("Verification is tests AND running it … pre-MVP …") | 311/311 | Elaboration of the asserted procedure fragment, not a DIRECTOR-BRIEF field; the pass-bar/procedure rule stays asserted |
| H18: FE format item-2 tail deleted (first-build file-layout instruction after the OUT-of-scope fragment) | 311/311 | First-build layout instruction, not a DIRECTOR-BRIEF field; the in-scope/out-of-scope naming stays asserted |
| H16: OP carve-out header substring (`**Bounded by NO-GUESSING …**`) → EOF | 311/311 | F10 adjudication stands: label-only, operative body stays and is guarded by the 81-B8 order check + 89-B3 window |
| H17: OBM carve-out header substring → EOF | 311/311 | Same adjudication as F10/H16 |
| F11a: whole OP factory paragraph `:62` → EOF | 311/311 | Carried-forward adjudication stands: paragraph is self-contained; the new 92-B1 full-line check asserts content, not position |
| F36: whole redesign.md `:68` line → EOF | 311/311 | Same adjudication as F11a (single `_F29` line, 7e vacuous for a whole-line move) |

### Fresh-hunt controls — caught, as expected

| Mutation | Result | What it proves |
|---|---|---|
| H3: partitioning sentence deleted from orchestrate `:93` | **310/311**, exactly the 7e orchestrate check | Step-4 paragraph edits are 7e-guarded (single 8,020-char `_F29` line) |
| H4 (M-FE1 repeat): COST-AWARE sentence deleted from FE `:139` | **310/311**, exactly the 7e feature-expansion check | FE paragraph edits are 7e-guarded |
| H5 (M-RD1 repeat): COST-AWARE sentence deleted from redesign `:68` | **310/311**, exactly the 7e redesign check | Redesign paragraph edits are 7e-guarded |
| H9: deep-reasoner `:17` tie-breaker substring → EOF | **310/311**, exactly the 7e deep-reasoner check | The `:17` line edit trips 7e (single `_F29` line in the file) |

A systematic scan of every long string literal in verify29.py's 10i checks
confirms the pattern: all other full-line assertions (OP/gan paragraphs,
common-agents line, gan-build/gan-design/react-build/astra pointers, OC body,
GENERATE Verification steps, react-build step 6, astra `:33`) equal their file
lines exactly; the remaining substring assertions (step-0 parentheticals,
`_CORR_BRIEF`, the FE Collect bridge, the orch-refine-code step-2
qualification, the planner fallback sentence) assert the operative fix #29
content in full — only the 3a check (93-B1) and the 7d(b) tuple (93-B2) leave
operative fix #29 content unasserted.

## §5 Verifier-honesty table (verify29.py, read end to end, 2,084 lines)

| Check area | Scoping | Status |
|---|---|---|
| 7c GLOBAL-ROUTING block + golden pin (85-B3) | Block extraction + byte-compare vs `fix29/global-routing-block.txt` | Clean (md5 `68206505` in orchestrate, hackathon-mode, golden) |
| 7c Belief carve-outs, order (81-B8), tie-breaker windows (89-B3, 88-B2) | 600-char windows / paragraph slice | Clean |
| 7c merge-order bridges | FE Collect + OBM Reconcile section-scoped (89-B2); orchestrate step-4 7e-guarded (N1); ladder scoped (90-B2) | Clean |
| 7c correction-brief construction | FE/OP section-scoped (89-B2); ladder scoped (90-B2); redesign 7e-guarded (N13) | Clean |
| 7c harness-gate clause | Paragraph-scoped via `_para_with` (85-B2) | Clean (H3/H4/H5 controls exact) |
| 7c factory-paragraph bodies | Full-line assertions (92-B1) | Clean (M-OP1/2, M-GAN1/2/3 exact) |
| 7d(a) contract core | Fenced-block extraction; no-drop + `none` mechanism (87-B2) | Clean — 7/7 incl. `Interface:` |
| 7d(b) templates | Per-section field labels (84-B1); reasoning + second-pass section-scoped (90-B1) | **93-B2** (`Interface:` never asserted per-template; recon + reasoning lack the slot) |
| 7d(c) FE format | Item-sliced (87-B2) | Clean (H15/H18 are elaboration tails, not fields) |
| 7d(d) contract refs | Paragraph-scoped (90-B4) | Clean |
| 7d "state the assumption" file-set + unbounded phrase 0× | Tree-wide file-set equality + 0× grep | Clean, with the noted H7 scope (4 dirs by design) |
| 7e staged-vs-built | Order-sensitive line comparison, 7 staged files | Clean, with noted limitation: order-sensitivity is vacuous for single-`_F29`-line files (DTF SKILL.md — fixed by the 91-B5 span scope; deep-reasoner, redesign, hackathon-mode — see §4) |
| 9b model pins | Tree-wide grep + occurrence counts (86-B1) + golden pin | Clean |
| 10i gan mirrors | Section-scoped (90-B3); loop order (82-B2); GENERATE slice (83-B1, 89-B1) | Clean except H13/H14 mirror tails (not filed, §4) |
| 10i gan-build loop wiring | ORCHESTRATOR-CHECK body (92-B2) + order (82-B2) | Clean except **93-B1** (planner-spec 3a lead-only) |
| 10i pointers | Full-line + span-scoped (87-B1, 90-B5, 91-B4–B8) | Clean |
| 10i gan step-0 pins | Step-0-scoped (91-B1/B2) | Clean |
| 10i planner-spec 3a | Phase-1-scoped (91-B3) | **93-B1** (scoped, but lead-only) |
| 10i orch-refine-code | Line-sliced step 2 / step 3 (90-B6); exceptions span-scoped (92-B3) | Clean (M-ORC1/2 exact) |
| 10i astra-review | Step-3-scoped (90-A1) | Clean |
| 10i planner fallback | Direction-source line (92-B4) | Clean (F37 exact) |
| 11b fix29 patch log | Census + 0-errors assertions | Clean |

## §6 Fresh hunt — checked and clean (except 93-B2)

- **DIRECTOR-BRIEF, all 7 fields.** Contract core 7/7 distinct slots +
  files-out-of-scope + no-drop + `none` mechanism (re-checked by direct read).
  Mechanical template 7/7; worked example 7/7; feature-expansion format 7/7
  (items 1, 2, 3, 4a, 4b, 9). GAN GENERATE block 7/7 present (3 labeled slots +
  4 via the spec.md reference) — the reference is real: the planner writes
  per-feature "[Feature]: [description, acceptance criteria]" into
  `gan-harness/spec.md` (`agents/ecc-gan-planner.md:29`, `:51–52`, `:56`, `:60`);
  the GENERATE block reads spec.md (`commands/gan-build.md:40`) and cites "the
  acceptance criteria from the spec" (`:46`). **Recon and reasoning are 6/7
  (Interface missing) — 93-B2.** Blind reviewer 6/7 + its own recorded
  verification-gate contract (exempt per dispatch-prompt.md:15); second-pass
  exempt (opinion-only).
- **NO-GUESSING.** Exactly 5 Belief copies tree-wide (orch-pipeline:72,
  feature-expansion:151, orch-build-mvp:70, dispatch-prompt.md:34 + :92), all
  carved with the tie-breaker; distances re-measured 137–142 chars (carve-out)
  and 356–361 chars (tie-breaker), matching #92-B. Unbounded phrase "state the
  assumption you made and proceed" 0× tree-wide (skills/rules/commands/agents).
  "state the assumption" in exactly the 6 known bounded files (deep-reasoner,
  orchestrate SKILL.md, dispatch-prompt.md, polish-pass SKILL.md +
  impeccable-critique.md, systematic-debugging). "instead of NEEDS_CONTEXT" 0×.
- **VERIFY-MERGE.** All 8 construction sites verify against the brief's
  acceptance criteria with a correction-brief path naming the failed criterion
  (orchestrate ladder :252, feature-expansion :158, orch-pipeline Phase 5 Review
  :74, gan ORCHESTRATOR-CHECK :63 + planner-spec 3a :30, react-build step 6 :18,
  redesign :68, astra-review :35). **Caveat:** the `:30` site's correction-brief
  path is the 93-B1 gap — the site exists in the tree but the verifier does not
  guard its operative half.
- **Harness-gate clause** ("in Cursor, slots refill per wave, not per
  completion") in all 5 factory paragraphs (orch-pipeline :62,
  feature-expansion :139, gan :14, redesign :68, orchestrate step 4 :93).
- **Counts / pins / identity.** 67/45/48/55. GLOBAL-ROUTING block md5 `68206505`
  in orchestrate, hackathon-mode, and the golden file (2,285 chars).
  `fix29.py` byte-identical to its template (`fbd459c7…`). "Factory routing (fix
  #29" in 13 files; `GLOBAL-ROUTING_F29` 24 raw occurrences — both matching the
  run-10 counts. No deepseek-/qwen- slugs (0), bare `grok-4.6-high-fast` 0,
  `grok-4.7-high` ×49.

## §7 Staged-vs-built drift re-check

- Direct `diff` of all 7 staged files vs built (counting `^[<>]` lines):
  orchestrate 6, dispatch-prompt 0, deep-reasoner 0, feature-expansion 22,
  design-taste-frontend SKILL.md 11, redesign.md 0, hackathon-mode 2 — **41 diff
  lines across 4 files**, exactly the MANIFEST §2(c)(9)/OWED-29-5 enumeration.
- fix16 anchor logic unchanged: `sub(` starts at `fix16/fix16.py:3807`; the
  anchor string is at `:3808` (`"(its upstream \`claude -p\` invocation path
  does not run in Cursor"`); the call spans 3807–3809. `fix29.py:438` cites
  "fix16.py:3808" — correct as the anchor-string line. Syncing staged
  hackathon-mode:38 to the built text would still break the build.

## §8 Methodology note

- Fresh-copy-per-mutation harness: `/tmp/a93b/pristine` (one copy of the built
  tree) re-copied to `/tmp/a93b/built` for each of 33 runs (baseline + 9
  reproductions + 5 §4 re-verifications + 18 fresh-hunt/control runs) plus 1
  demo-verifier run (patched verify29.py copy in `/tmp/a93b-driver/`, real
  verify29.py untouched); symlinks in `/tmp/a93b/` point at the real `fix28/`,
  `fix29/`, `new-rules/`, `new-skills/` so checks 7e/10g/11/11b run
  meaningfully. No in-place restores anywhere in this audit. Mirror baseline
  311/311; real-tree re-run 311/311.
- One driver error in the first pass, in the harness (not the verifier): H8's
  `_gen` end marker is `"# Wait for generator to finish"`, not `"# Wait for
  generator"` (verify29.py uses substring `.index()`, the driver used exact
  equality) — fixed and re-run with the exact result (H8 → 311/311).
- F11b/F35 check-12 collateral: moving a line above an allow-listed line shifts
  the allow-list line numbers, so check 12 fails alongside the intended check.
  The failure sets are still exact for the intended checks; the check-12 failure
  is a known line-number sensitivity of the allow-list — except in F35, where it
  is the *only* catch (see §4).
- No conclusion in this report rests on a green result alone without a named
  mutation: every filed finding names the exact deletion and the verify29.py
  line it evades; every tested-not-filed green is listed in §4 with its reason.
- Scratch removed (`/tmp/a93b/`, `/tmp/a93b-driver/` deleted). Real tree untouched.
