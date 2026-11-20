# Fix #34 — MANIFEST (close record)

**What:** content port of the factory variant's rounds 10–13 into the REGULAR
plugin, minus all drone machinery, adapted to regular conventions (regular
rules win conflicts). Decisions: `fix34/SPEC.md` (D34-1..D34-12). Mechanism:
`fix34/fix34.py` wired into build.sh after fix32.py; staged sources via
`fix34/stage34.py` + `fix34/weave34.py` (working copies in the canonical
`fix34/` dir). Verifier: `fix34/verify34.py`.

**Parent:** d22d9f4 (fix #33 close). **Counts before → after:** skills
72 → 76; agents 45 → 45; rules 48 → 48; commands 55 → 55; hooks 15 → 15;
trigger keys 48 → 48 (coverage 72/48 → 76/48; the four new skills carry no
trigger keys, following the fix #31 design-skill precedent — D34-10).
**Pin census (unchanged):** cursor-grok-4.6-high-fast ×72; "Grok 4.7 High"
×2 (strategic-compact); grok-4.7-high ×0; extra-high ×0.

## Per-item port log

Transferred (adaptations noted; everything else verbatim from factory
c85e549 final states):

1. **motion-principles skill** — verbatim except: rule ID MOTIONPRINCIPLES_F170
   → _F34 (D34-1); inventory cite repointed to the regular inventory's new §13
   (the regular inventory had no §0/§13 — see item 8).
2. **threeui skill** — verbatim except: THREEUI_F171 → _F34; cite → §13.
   Catalog + install guide only; MIT; free Community edition only;
   @designcodeio/threeui; no vendored source.
3. **prebuild-research skill + research phase** — skill verbatim except:
   RESEARCHBRIEF_F177 → _F34; cite → §14; the factory's CAPTIVATION_F32
   citations (an excluded factory-only rule) replaced by the regular tree's
   own anti-derivative rule in prose (×2); trigger-precedent line repointed
   from the factory round to the fix #31 design-skill precedent. Weaving:
   orchestrate step 1.5 (after scope, before expansion) + the research-brief
   reuse rule in step 2; hackathon-mode sequence names the step;
   hackathon-scope's scoping handoff names prebuild-research as the next
   step (caught by dry-run #54, item M-1 — the factory's sentence ported
   into the regular staged file, which is now byte-identical to the
   factory's);
   feature-expansion Phase 0 reads the brief first + records taken/dropped
   per idea. Caps as the factory's final state: ≤4 searches + ≤4 fetches,
   docs/research-brief.md ≤ ~600 tokens, primary sources only, per-line
   sources.
4. **Design contract + restatement gate** — Taste step 4a issues
   docs/design-contract.md (Hosting / Palette tokens / Type scale / Spacing
   scale / Motion specs citing motion-principles / Components with inventory
   citations / States / Deviations), DESIGNCONTRACT_F175 → _F34; literal
   implementation, deviations recorded with D19 reasons. Restatement gate
   adapted to the regular flow (no dispatch): orchestrate step 3 — the
   executing agent restates the contract's key values in its plan before the
   slice builds; a mismatch stops at the plan; a mismatch first found by QA
   counts as the gate skipped. Orchestrate step 5a checks the gate +
   contract. Palette line edited surgically: the factory's per-skill glosses
   were NOT imported (its "ui-ux-pro-max — general design intelligence"
   contradicts fix #32's lookup-only demotion; regular rule wins).
5. **Hosting** — HOSTING_F178 → _F34: deploy-fast gains the factory hosting
   section (Vercel/Netlify static-friendly, SPA fallback ships with the
   build, design wins conflicts recorded as Deviations). deploy-fast's
   Netlify PRICING row is byte-untouched (asserted in fix34.py; its touch-up
   is dated Dec 4, 2026 and is not this job).
6. **code-mode framework minus dispatch** — skill + 4 helpers (cm_census,
   cm_read, cm_report, cm_write); cm_dispatch.py deleted at staging.
   CODEMODE_F181 / SCRIPT-FIRST_F182 / SCRIPT-GATE_F183 → _F34 forms.
   Adaptations: §5 rewritten — script-first applies to the regular
   orchestrator's own mechanical work, full stop (no CLI/drone leg exists
   here); §1 helper table drops the cm_dispatch row ("Five" → "Four");
   §2 drops the fan-out bullet and the PARALLEL-CALLS_F154 paragraph
   (dispatch machinery), replaced by prose batching discipline; §4 item 4
   bars network calls from scripts; §6 keeps only the census shape (the
   factory census locks tied to drone/briefing files excluded); the 500 E3
   cap rationale reworded off the drone-return comparison (also in
   cm_report.py's docstring); cm_census.py docstring de-factored. The
   honesty boundary stays, reworded vendor-free (the shipped tree bans
   vendor names — the factory text named the vendor and its product; the
   boundary's substance is unchanged, evidence basis recorded in SPEC.md).
   Audit/dry-run scrubs (round 34b): a leftover "raw dispatch envelopes"
   clause, "(R86)"/"(R87's…)" factory decision tags, and "never all five"
   → "never all four" corrected.
7. **MOTION-QA + CONTRACT-QA** — browser-qa gains both verdict blocks
   (MOTION-QA_F172 / CONTRACT-QA_F176 → _F34), applied by fix34.py at build
   time chained on fix31's MOTION-QA anchor text; browser-qa stays the sole
   verdict executor.
8. **Full-weave end state** — DESIGNPKG-AUTO enumerations in orchestrate +
   hackathon-mode name all four new skills, inserted after
   `motionsites-web-builder` (NOT appended: appending broke fix32's
   lead-attribution scan geometry — D34-5; blocks byte-identical in both
   files). Design inventory gains §13 (Motion Principles, ThreeUI, layer
   roles), §14 (Pre-build Research, Design Contract), §15 (code-mode) as
   bolded row text (the regular inventory's own style). Cross-references
   both ways: research ↔ code-mode (prebuild-research §"When NOT to use"
   ↔ code-mode §2), contract ↔ research brief, expansion ↔ research +
   inventory. Call map regenerated (all four new skills called, strong
   invokers; uncalled set unchanged: context-budget, vite-patterns).
   Generator fix (sweep #57): section headings were hardcoded literals —
   "## Skills (72)" survived the count update; headings now emit from
   EXPECTED, docstring counts updated, verify34 §17i guards the class.
   Rule-ID integrity: the ten ported IDs are each defined exactly once in
   the regular tree; no factory _F1xx forms remain (verifier §17 + sweep).

**Excluded completely (factory-only):** drone-reasoning / drone-coding
agents + OpenRouter pins; openrouter-drones skill; orchestrator-briefing
skill + ALL dispatch machinery (brief gate, per-slice context, scripted CLI
dispatch, drone return-cap rules); cm_dispatch helper; factory census locks
tied to drone/briefing files; the factory's fast-tier removal (regular
executor agents keep their cursor-grok-4.6-high-fast pins — verified in the
staged diff adjudication); the factory README's round-12 code-mode bullet
(anchor text absent in the regular README; code-mode is named in the README
provenance note instead).

## Verification loop

- **Builds:** 7 runs against the logged target
  `fix34/fakehome34/workspace/hackathon-plugin/hackathon-ecc` (fake HOME on
  real disk, fix33 pattern). Run 1 FAIL (fix32 lead-scan, enumeration
  geometry → D34-5); run 2 exit 0 but 72 skills (build.sh STEP 2 staged
  loop is an explicit name list — the four new skills added); run 3 killed
  by a service restart, rerun failed on a stray __pycache__ (cleaned);
  runs 4–7 exit 0, "fix34: OK" (21 changes), counts 76/45/48/55/15.
- **Verifier:** verify34 run 1 = 611/614 (banned vendor terms in code-mode
  → reworded vendor-free; CUT-sweep allow-list line numbers renumbered to
  the shifted lines by exact content match) → run 2 = 614/614 → run 3 =
  **615/615** (§17i added by the sweep fix).
- **Regression scans:** fix32 scan suites r4 (77 PASS lines) + r5 (101 PASS
  lines), repointed at the fix34 tree — **ALL PASS**, twice.
- **Audit #115: PASS** (no blocking). Two minors (code-mode dispatch-envelope
  remnant; R86/R87 tags) fixed in round 34b.
- **Sweep #57: 1 defect → fixed → CLEAN.** The stale "## Skills (72)"
  call-map heading (generator hardcode). Everything else clean: zero factory
  residue (the four FACTORY hits are fix #29's own regular text,
  byte-identical to fix33; openrouter hits are a pre-existing icon catalog,
  identical in fix33), counts correct, no broken references, banned terms
  allowlist-only, no hygiene issues, diff surface entirely in scope.
- **Dry-run #54:** the regular flow walks clean end to end (research →
  expansion → contract → restatement gate → build checks → MOTION-QA /
  CONTRACT-QA → hosting deploy). Findings: M-1 hackathon-scope handoff
  (fixed, see item 3); M-2 code-mode "five" (fixed). **B-1 adjudicated OUT
  OF SCOPE:** the GLOBAL-ROUTING_F29 block's drone/factory wording is
  fix #29's own pre-existing regular text — byte-identical between the
  fix33 and fix34 built trees (verified by extracted comparison); rewriting
  it would be an unapproved regime change, not a port item. Recorded here
  plainly as a dry-run finding against pre-existing text. O-1 (Taste cites
  a staged path twice) is likewise pre-existing in fix33; no action.
- **Staged-diff adjudication:** every staged file shared by both trees was
  diffed factory-vs-regular; all remaining diffs are intended adaptations,
  excluded drone machinery, or pre-fix34 divergence (incl. files where the
  regular tree is ahead, e.g. the fix #33 MODELSEL checks).

## Output-tree repair

The final build regenerated `hackathon-ecc/` from the intact regular
sources; the canonical tree was synced from the verified scratch build.
The round-12 partial upstream tree (155 skills, no README/manifests) is
gone: the canonical output is back to the regular shape — README +
manifests present, 76 skills / 45 agents / 48 rules / 55 commands / 15
hooks.

## Owed / not done

- **OWED-34-1 (call map):** no standing caller names `threeui` (install-
  time only, by design) — recorded in fix34-patch-log.md.
- **OWED-34-2 (live use):** the ported flow (research step, contract +
  restatement gate, MOTION-QA / CONTRACT-QA, script-first on the
  orchestrator's mechanical work) is verified by construction, verifier,
  audit, sweep, and dry-run walk — it has not yet run in a live build.
  First live use is the confirmation, per the tree's smoke-test precedent.
- Not done, by design: no upload, no push (Anish's Windows step); the
  deploy-fast Netlify pricing touch-up stays dated Dec 4, 2026.
