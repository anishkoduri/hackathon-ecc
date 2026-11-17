# Audit #94-B — brief/verify coherence + verifier honesty (fix #29, round 15)

**Verdict: PASS — 0 blocking, 0 minor.**

Auditor B (brief/verify coherence + verifier honesty). Read-only except this report.
Method: read `fix29/verify29.py` end to end (2,103 lines); independently re-ran it —
**315/315, exit 0** (real tree). All mutations below ran on a scratch mirror
(real copy of the built tree + symlinks to the real `fix28/`, `fix29/`,
`new-rules/`, `new-skills/` so checks 7e/10g/11/11b run meaningfully — the
#92-B/#93-B pattern), with a **fresh copy per mutation — no restores**.
Mirror baseline 315/315 (twice: once on the /tmp mirror, once on the
relocated disk mirror after the /tmp-full incident, §8). 38 mutation runs
(35 distinct + 3 clean re-runs) + 1 final mirror baseline. Scratch removed
after. The real tree was never edited by this audit.

## §1 Disposition of the #93-B fixes — both VERIFIED-FIXED

Reproduced the coordinator's scratch mutations on fresh mirrors (one fresh
copy per mutation). Every one fails exactly its intended check.

| Fix | Reproduction | Result |
|---|---|---|
| 93-B1 full-line 3a check | H1: delete the entire `gan-build.md:30` tail after the lead ("3a. Orchestrator checks the planner's spec against the brief before Phase 2") | **314/315**, exactly the B1 full-line check (verify29.py:1686) |
| 93-B1 full-line 3a check | H1b: delete only the failure-path sentence ("If the spec fails the check, … stop and report the failure with evidence.") | **314/315**, exactly the B1 check (:1686) |
| 93-B1 full-line 3a check | H1c (new probe, beyond the coordinator's two): delete only the match-criteria sentence ("the spec's files, scope, and acceptance criteria must match the brief's goal, …") | **314/315**, exactly the B1 check (:1686) |
| 93-B2 recon Interface | Delete the recon `Interface:` line (`dispatch-prompt.md:70`) | **314/315**, exactly the recon Interface check (verify29.py:887) |
| 93-B2 reasoning Interface | Delete the reasoning `Interface:` line (`dispatch-prompt.md:139`) | **314/315**, exactly the reasoning Interface check (:887) |
| 93-B2 pre-build sanity | Delete both Interface lines (tree without the Interface slots) | **313/315**, exactly the recon + reasoning Interface checks — the coordinator's 313/315 run reproduced exactly |

String-level confirmation (not just check behaviour): the 93-B1 asserted
string in verify29.py:1686–1687 is byte-equal to the file line
(`commands/gan-build.md:30`, 616 chars, verified by direct comparison).
The 93-B2 Interface lines are byte-identical staged-vs-built
(`dispatch-prompt.md` staged == built, md5 `08aca7a8…` both).

## §2 New findings

None. 0 blocking, 0 minor.

## §3 Nits (not counted)

None.

## §4 Tested and NOT filed — adjudications and fresh-hunt greens

### #93-B §4 adjudications re-confirmed at sentence level

| Item | Mutation | Result | Standing |
|---|---|---|---|
| Orchestrate step-4 merge-order bridge | N1: bridge clause out of `:93` to EOF | **314/315**, exactly the 7e orchestrate check | Adjudication STANDS |
| Fast-worker preamble bound | N10: short-form tie-breaker sentence out of `dispatch-prompt.md:94` to EOF | **314/315**, exactly the 7e dispatch-prompt check | Adjudication holds |
| Reasoning-template NEEDS_CONTEXT line | N12: "If under-specified: return NEEDS_CONTEXT naming exactly what is missing — do not guess." out of `:149` to EOF | **314/315**, exactly the 7e dispatch-prompt check | Adjudication holds (same known 7e residual: a staged-source deletion would pass 7e) |
| Redesign.md correction-brief clause | N13: correction-brief sentence out of `:68` to EOF | **314/315**, exactly the 7e redesign check | Adjudication STANDS |

Citation update (not a finding): the fast-worker preamble short-form
tie-breaker is now at `dispatch-prompt.md:94` and the reasoning NEEDS_CONTEXT
sentence at `:149` — both shifted +2 from the #93-B citations (:92 / :144)
by the Interface-line additions in build run 12. The sentences and the
adjudications are unchanged.

### F35 fragility note — re-tested, mechanism still holds, gap has NOT opened

F35 (hackathon-mode GLOBAL-ROUTING block line `:45` → EOF) still fails at
**314/315**, and the failing check is still check 12 only
("CUT-name sweep: zero live dispatches …"), not any GLOBAL-ROUTING check: the
move shifts `ALLOW_NAMES:47` (`intent-driven-development` / `product-lens`)
to line 46, uncovered by the allow-list, so the sweep flags it. The block's
own checks (count == 1, byte-identity, golden pin) are all position-blind,
and hackathon-mode carries exactly one `_F29` line, so 7e is vacuous for a
whole-line move. The catch therefore still depends entirely on the check-12
allow-list entry sitting below the moved line; if that entry were ever
re-mapped, the move would pass. This remains a demonstrated catch with a
fragile mechanism, not a demonstrated gap — recorded, not filed, as in
#92-B/#93-B.

### Fresh hunt — every check class probed, all caught or adjudicated-green

| Mutation | Result | Why not filed / what it proves |
|---|---|---|
| F-A: "Interface, " deleted from the skeleton enumeration (`dispatch-prompt.md:15`) | **313/315**, exactly the skeleton check + the 7e dispatch-prompt check | Both intended: the enum line carries `DIRECTOR-BRIEF_F29`, so 7e trips alongside. Skeleton check is live. |
| F-B: "Interface:" deleted from the contract-core fenced block | **314/315**, exactly the contract-core Interface check | 7d(a) live per-field. |
| F-C: second-pass NEEDS_CONTEXT line deleted (`:167`) | **314/315**, exactly the 90-B1 second-pass check | Section-scoped check live. |
| F-D: tie-breaker deleted from the governing first-build carve-out (`:52`) | **314/315**, exactly the 81-B5 carve-out tie-breaker check | Per-slice assertion live; the Belief-paragraph copy does not mask it. |
| F-E: scope sentence deleted from the mechanical preamble | **314/315**, exactly the mechanical-preamble scope check (89-B4) | Per-site presence live. |
| F-F: OP contract-ref sentence moved out of the factory paragraph to EOF | **312/315**, exactly the two 7d(d)/10i contract-ref checks + the 92-B1 full-paragraph check | All three intended; the sentence is asserted in both sections and the full line. |
| F-G: "reasoning-heavy work goes to DeepSeek" planted at EOF of `gan-build.md` | **313/315**, exactly the two 9b checks (line-count + occurrence-count) | 84-B2 widening + 86-B1 occurrence count both live. |
| F-H: "claude" planted at EOF of `orchestrate/SKILL.md` | **314/315**, exactly the check-8 banned-terms check | Check 8 live. |
| F-I: "Use the `codebase-memory` skill" planted at EOF of `orchestrate/SKILL.md` | **314/315**, exactly the check-12 CUT sweep | Check 12 live. |
| F-J: bare `grok-4.6-high-fast` planted at EOF of `orchestrate/SKILL.md` | **314/315**, exactly the bare-grok check | Check 9 live. |
| F-K: old "The evaluator pass IS the verify step" sentence planted at EOF of `gan-style-harness/SKILL.md` | **314/315**, exactly the old-substitution-gone check | 80-B2 guard live. |
| F-L: FE format item 9 return-format content replaced with "status only" | **314/315**, exactly the item-9 check | 7d(c) item-sliced check live. |
| F-M: orch-refine-code step-2 factory-drone qualification moved to EOF | **314/315**, exactly the step-2 check (90-B6) | Line-sliced check live. |
| F-N: astra-review pointer moved within the Step 3 slice (just before `## Verdict`) | **315/315** | Span granularity is step-level by design (H10 class); no semantic change. |
| F-O: `agents/fast-worker.md:16` bound line deleted ("stop and return that — do not invent an answer") | **315/315** | Pre-existing ECC role text, not a fix #29 addition: verify29.py contains zero mentions of `agents/fast-worker.md` — no check asserts the agent file's own bound; the fix #29 coverage is the dispatch-prompt preamble check (N10). Not a fix #29 regression path. |
| F-P: "`none`" mechanism deleted from the contract-core no-drop rule (`orchestrate:227`) | **313/315**, exactly the 87-B2 `none` check + the 7e orchestrate check | Both intended: the no-drop line carries `DIRECTOR-BRIEF_F29`. |
| F-R: `# CHECK SCORE` line moved before `# EVALUATE` | **313/315**, exactly the 82-B2 order check + the 92-B2 OC-body check | Both intended: moving CHECK SCORE before EVALUATE empties the `_gb_loop` slice, so the body check fails alongside the order check. The order assertion is live. |
| F-S: whole OP factory paragraph `:62` → EOF | **315/315** | F11a adjudication stands: paragraph is self-contained; the 92-B1 full-line check asserts content, not position. |
| F-T: "files out of scope" deleted from the reasoning Constraints line | **314/315**, exactly the reasoning "files out of scope" check | 7d(b) per-field live. |
| F-U: "Goal:" relabelled in the mechanical template | **314/315**, exactly the mechanical Goal check | 7d(b) per-field live. |
| F-V: "Verification steps:" relabelled in the worked example | **314/315**, exactly the worked-example Verification-steps check | 7d(b) per-field live. |
| F-W: second "Qwen" appended to the orchestrate GLOBAL-ROUTING block line | **311/315**, exactly the byte-identity check, the golden-pin check, the 7e orchestrate check, and the 86-B1 occurrence check | All four intended: block-content guards + occurrence count all live. See §8 for the first-attempt transient (extra 12b failure, not reproduced on the clean re-run). |
| F-Z: one trigger key deleted from `skill-triggers@1.json` | **314/315**, exactly the trigger-count check | Check 5 live. |

No other check class in verify29.py (2,103 lines, read end to end) leaves
operative fix #29 content unasserted: the remaining substring assertions
(step-0 parentheticals, `_CORR_BRIEF`, the FE Collect bridge, the
orch-refine-code step-2 qualification, the planner fallback sentence) assert
their operative content in full, and the full-line assertions (OP/gan
paragraphs, common-agents line, all four pointers, OC body, planner-spec
3a, GENERATE Verification steps, react-build step 6, astra `:33`) equal
their file lines exactly — the 93-B1 string was verified byte-equal
(616 chars) and the 92-B1 paragraph strings were verified exact in #93-B.

## §5 Verifier-honesty table (verify29.py, read end to end, 2,103 lines)

| Check area | Scoping | Status |
|---|---|---|
| 7c GLOBAL-ROUTING block + golden pin (85-B3) | Block extraction + byte-compare vs `fix29/global-routing-block.txt` | Clean (md5 `68206505` in orchestrate, hackathon-mode, golden; F-W exact) |
| 7c Belief carve-outs, order (81-B8), tie-breaker windows (89-B3, 88-B2) | 600-char windows / paragraph slice | Clean (F-D, N10 exact) |
| 7c merge-order bridges | FE Collect + OBM Reconcile section-scoped (89-B2); orchestrate step-4 7e-guarded (N1); ladder scoped (90-B2) | Clean |
| 7c correction-brief construction | FE/OP section-scoped (89-B2); ladder scoped (90-B2); redesign 7e-guarded (N13) | Clean |
| 7c harness-gate clause | Paragraph-scoped via `_para_with` (85-B2) | Clean |
| 7c factory-paragraph bodies | Full-line assertions (92-B1) | Clean (F-F exact) |
| 7d(a) contract core | Fenced-block extraction; no-drop + `none` mechanism (87-B2) | Clean — 7/7 incl. `Interface:` (F-B, F-P exact) |
| 7d(b) templates | Per-section field labels (84-B1); `Interface:` for implementation templates + worked example (93-B2); reasoning + second-pass section-scoped (90-B1) | Clean — **93-B2 VERIFIED-FIXED** (H1-series, B2, PREBUILD, F-A/F-C/F-T/F-U/F-V exact) |
| 7d(c) FE format | Item-sliced (87-B2) | Clean (F-L exact) |
| 7d(d) contract refs | Paragraph-scoped (90-B4) | Clean (F-F exact) |
| 7d "state the assumption" file-set + unbounded phrase 0× | Tree-wide file-set equality + 0× grep | Clean, with the noted F-O scope (agent file itself unasserted — pre-existing text, §4) |
| 7e staged-vs-built | Order-sensitive line comparison, 7 staged files | Clean, with noted limitation: order-sensitivity is vacuous for single-`_F29`-line files (DTF SKILL.md — fixed by the 91-B5 span scope; deep-reasoner, redesign, hackathon-mode — see F35) |
| 9b model pins | Tree-wide grep + occurrence counts (86-B1) + golden pin | Clean (F-G, F-W exact) |
| 10i gan mirrors | Section-scoped (90-B3); loop order (82-B2); GENERATE slice (83-B1, 89-B1) | Clean (F-R exact) |
| 10i gan-build loop wiring | ORCHESTRATOR-CHECK body (92-B2) + order (82-B2) + planner-spec 3a full line (93-B1) | Clean — **93-B1 VERIFIED-FIXED** (H1/H1b/H1c exact) |
| 10i pointers | Full-line + span-scoped (87-B1, 90-B5, 91-B4–B8) | Clean (F-N span granularity, §4) |
| 10i gan step-0 pins | Step-0-scoped (91-B1/B2) | Clean |
| 10i planner-spec 3a | Phase-1-scoped (91-B3) + full line (93-B1) | Clean |
| 10i orch-refine-code | Line-sliced step 2 / step 3 (90-B6); exceptions span-scoped (92-B3) | Clean (F-M exact) |
| 10i astra-review | Step-3-scoped (90-A1) | Clean |
| 10i planner fallback | Direction-source line (92-B4) | Clean |
| 11b fix29 patch log | Census + 0-errors assertions | Clean |
| Checks 5/8/9/12/12b | Counts / greps / sweep | Clean (F-G/F-H/F-I/F-J/F-Z exact) |

## §6 Fresh hunt — checked and clean

- **DIRECTOR-BRIEF, all 7 fields (direct per-section counts).** Contract
  core 7/7 distinct slots + files-out-of-scope + no-drop + `none`
  mechanism. Recon **7/7**, mechanical 7/7, reasoning **7/7**, worked
  example 7/7 — the 93-B2 fix holds by direct count, not just by the
  verifier. Feature-expansion format 7/7 (items 1, 2, 3, 4a, 4b, 9 — item
  2 carries both the in-scope files and the explicit OUT-of-scope
  naming). GAN GENERATE block 7/7 present (3 labeled slots — Files out
  of scope, Verification steps, Return format — + 4 via the spec.md
  reference) — the reference is real: the planner writes per-feature
  "[Feature]: [description, acceptance criteria]" into
  `gan-harness/spec.md` (`agents/ecc-gan-planner.md:29`, `:51–52`) and
  the GENERATE block reads spec.md (`commands/gan-build.md:40`) and
  cites "the acceptance criteria from the spec" (`:46`). Skeleton
  names all 7 in its enumeration (0 labeled slots, by design). Blind
  reviewer 6/7 (no `Interface:`, exempt by design per
  `dispatch-prompt.md:15`); second-pass 1/7 (exempt, opinion-only).
- **NO-GUESSING.** Exactly 5 Belief copies tree-wide (orch-pipeline:72,
  feature-expansion:151, orch-build-mvp:70, dispatch-prompt.md:34 + :94),
  all carved with the tie-breaker; distances re-measured 137–142 chars
  (carve-out) and 356–361 chars (tie-breaker), matching #92-B/#93-B
  (the @28 hits are the documented self-match inside the carve-out's
  own quotation). Unbounded phrase "state the assumption you made and
  proceed" 0× tree-wide (skills/rules/commands/agents).
  "state the assumption" in exactly the 6 known bounded files
  (deep-reasoner, orchestrate SKILL.md, dispatch-prompt.md, polish-pass
  SKILL.md + impeccable-critique.md, systematic-debugging).
  "instead of NEEDS_CONTEXT" 0×.
- **VERIFY-MERGE.** All 8 construction sites verify against the brief's
  acceptance criteria with a correction-brief path naming the failed
  criterion (orchestrate ladder :252, feature-expansion :158,
  orch-pipeline Phase 5 Review :74, gan ORCHESTRATOR-CHECK :63 +
  planner-spec 3a :30, react-build step 6 :18, redesign :68,
  astra-review :35). The `:30` site's operative half is now guarded by
  the 93-B1 full-line check (H1/H1b/H1c).
- **Harness-gate clause** ("in Cursor, slots refill per wave, not per
  completion") in all 5 factory paragraphs (orch-pipeline :62,
  feature-expansion :139, gan :14, redesign :68, orchestrate step 4 :93).
- **Counts / pins / identity.** 67/45/48/55. GLOBAL-ROUTING block md5
  `68206505` in orchestrate, hackathon-mode, and the golden file
  (2,285 chars). `fix29.py` byte-identical to its template
  (`fbd459c7…`). No deepseek-/qwen- model slugs (the only `deepseek-`
  strings are the three allow-listed `logos:deepseek-icon` icon-data
  entries; `qwen-` 0×); bare `grok-4.6-high-fast` 0; `grok-4.7-high` ×49.

## §7 Standing-claim corrections — confirmed in the record

- The MANIFEST's **#84-B1** record now carries the #93-B2 correction
  note ("the fix as implemented asserted 6 labels per template — the
  tuple substituted 'files out of scope' … for `Interface:`"), and the
  **#92-B** record carries the #93-B2 correction ("the 'all 7 fields in
  every format' claim was wrong for `Interface:`") — both verified by
  grep (MANIFEST.md:408 and the #92-B record). The #93-B fixes section
  also records them under "Standing-claim corrections".
- verify29.py's 7d(b) comment records the correction (verify29.py:875–877:
  "the tuple above never asserted `Interface:` — recon and reasoning
  carried only 6 of the 7 slots while the check claimed all seven field
  labels (#84-B1's 'all seven field labels' was wrong for Interface;
  #92-B §6's 'all five templates 7/7' likewise)").

## §8 Methodology note

- Fresh-copy-per-mutation harness: `/tmp/a94b/pristine` (one copy of the
  built tree) re-copied to `/tmp/a94b/built` for each of the first 12 runs
  (baseline + 9 reproductions + N1/N10/N12/N13/F35), with symlinks in
  `/tmp/a94b/` at the real `fix28/`, `fix29/`, `new-rules/`, `new-skills/`
  so checks 7e/10g/11/11b run meaningfully. No in-place restores anywhere
  in this audit.
- **/tmp-full incident:** mid-run the driver died with "No space left on
  device" — /tmp is a 512 MB tmpfs and was at 100% (303 MB
  `/tmp/ecc-repo-clean`, 94 MB `/tmp/a94a` belonging to the parallel
  auditor-A run, 104 MB my own mirror). Per AGENTS.md this tmpfs fills
  fast; I deleted only my own `/tmp/a94b` (104 MB, freeing /tmp to 62%)
  and relocated the harness to the disk-backed
  `fix29/scratch-tmp/a94b/` (the established env-redirected scratch
  location), re-creating pristine from the real tree. The remaining 23
  mutations ran there; the first 12 results stand (recorded before the
  incident). Scratch removed after (`fix29/scratch-tmp/a94b/`,
  `/tmp/a94b-driver/`, `/tmp/a94b` all deleted). Real tree untouched.
- **F-W transient (not a finding):** the first batch-2 attempt at F-W
  reported 310/315 with five failures — the four expected ones plus an
  extra check-12b failure. A clean sequential re-run of F-W (nothing
  else touching the scratch dir) reported **311/315** with exactly the
  four expected failures, and the final mirror baseline re-run was
  **315/315** with 12b passing. The extra 12b failure did not
  reproduce; it fails strict (the verifier failing more, never less),
  so it is not a false-pass and not a finding. Recorded here so a
  future round can re-check 12b stability if it ever recurs.
- **Harness race (own goal, caught):** a manual F-W reproduction I ran
  while the re-run driver was also using the same scratch dir raced on
  `rmtree`/`copytree` (FileNotFoundError `resolve.d.ts`) and produced a
  meaningless 315/315. Both the manual run and that driver invocation
  were discarded; the three mutations were re-run cleanly, sequentially,
  with nothing else touching the scratch dir (F-R 313/315, F-W 311/315,
  F-Z 314/315 — all exactly their intended checks). No conclusion in
  this report rests on the raced runs.
- No conclusion in this report rests on a green result alone without a
  named mutation: every filed finding would have named the exact
  deletion and the verify29.py line it evades; there are none. Every
  tested-not-filed green is listed in §4 with its reason.
