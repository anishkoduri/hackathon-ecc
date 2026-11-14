# Audit #72 — Fix #25 (Phase 3b)

**Verdict: Audit #72: ZERO blocking, 2 minor.**
**Date:** 2026-11-13. **Auditor:** fix #25 audit worker. **Scope:** built tree
`hackathon-ecc/` + `build.sh` against `fix25/SPEC.md` (§0–§6). Read-only audit;
no file was edited. `fix11/fix11-stage.py` never run.

**Format note:** no standalone Audit #71 report file exists in the plugin tree
(searched `fix24/`, `audit-scripts/`; Audit #71 survives only as the summary in
`fix24/MANIFEST.md`: ZERO blocking, 2 minor, both manifest-only). This report
follows that severity discipline: **blocking** = a SPEC violation in the built
tree / build; **minor** = record, verifier-tail, or stale-pointer issues with
no plugin-behavior effect.

## Build baseline (verified, not trusted)

- `build.sh`: **24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae`**;
  diff vs `build.sh.before-fix23`: **+305/−0** (additions-only). ✓
- Counts in the built tree: skills **166**, agents **72**, rules **123**,
  commands **87**; `hooks/hooks.json` **15** events; `skill-triggers@1.json`
  **64** trigger keys, coverage skills 166 / withTriggers 64. ✓
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5,
  case-insensitive, excl. node_modules): **0** in the built tree. ✓
- Grok pins only: `grok-4.7-high` ×54, `cursor-grok-4.6-high-fast` ×103,
  bare `grok-4.6-high-fast` ×0. ✓
- No new skill: counts unchanged from fix #24. No bundle/commit/push
  artifact from this fix: `hackathon-ecc.bundle` is dated Nov 11 (pre-fix25);
  the plugin root is not a git repo. ✓
- `fix25/fix25.py` ran at build: build log shows `fix25: 14 change(s)`,
  `fix25: OK`.

## §1 Called — the call map: PASS

- Map present in the built tree at `skills/orchestrate/references/call-map.md`,
  byte-identical to the staged copy (`diff` clean). Counts table agrees with
  the tree: 166/72/123/87/15/64. ✓
- Uncalled **52** (24 skills, 21 agents, 7 commands, 0 rules, 0 hooks,
  0 triggers); second-order orphans **13** (8 skills, 4 agents, 1 command
  `/python-review`). Matches the build worker's post-rebuild regeneration. ✓
- All four wire-ins landed in the built tree, each verified by reading the
  cited invoker line:
  - `ck` — called, invoker `hooks/session-start.js` [strong]: the patch
    spawns `skills/ck/hooks/session-start.mjs` (path built at `:79`, spawn at
    `:81`), converts `additionalContext` → `additional_context`, fail-soft,
    15 s timeout, inherits the `session:start` gate. The `.mjs` exists in the
    built tree. `skills/ck/SKILL.md:157` carries the "already wired" note. ✓
  - `conventional-commit-review` — called via `commands/prp-commit.md` Phase 3
    (draft with the skill, `ecc-commit-reviewer` checks) and orchestrate
    step 6; `ecc-commit-reviewer` and `git-workflow` (linked second-order
    orphan) are called with it. ✓
  - `ecc-recipes` — called via orchestrate `RECIPES_F25` paragraph
    (`skills/orchestrate/SKILL.md:125`); the 8 epic/`/prune` commands left the
    second-order list. `/learn-eval` correctly NOT lit (ecc-recipes never
    references it). ✓
  - `/test-coverage` — called via orchestrate Verify step 1 (`TESTCOV_F25`,
    measurement Steps 1–2 only) at `skills/orchestrate/SKILL.md:260`. ✓
- Dormant coverage: every one of the 52 uncalled + 13 second-order names was
  cross-checked against `fix25/callmap/wiring-list.md` — **0 missing**; each
  carries a WIRE IN (done) or INTENTIONALLY DORMANT reason. The trigger-router
  group item (B6, all 64 keys resolve, no live Cursor entry point) is recorded
  in the map and the wiring list as a parent decision, not silently dropped. ✓
- Spot-check of invocation claims: 2,120 strong invoker claims in
  `fix25/callmap/call-map-data.json`; a deterministic 51-claim sample (every
  41st, sorted) was verified by grepping the cited invoker file. 51/51 hold
  once the name form is accounted for: the two apparent failures
  (`ecc-pr-test-analyzer` ← `commands/review-pr.md`,
  `ecc-security-reviewer` ← `commands/vue-review.md`) are my checker's
  artifact — both agents are invoked by frontmatter name (`pr-test-analyzer`
  at review-pr.md:22, `security-reviewer` at vue-review.md:37), which the
  generator correctly matches. No dead dispatch path found in the sample. ✓
- The 8 epic/`/prune` commands now read as called via the recipes lookup but
  stay dormant **in use** (dispatch needs a genuine multi-week epic /
  maintenance need). Reachability vs use is recorded in the wiring list; the
  reading is an open parent item (see §Open), not an audit failure.

## §2 Weaved — fix #24 coherence as baseline: PASS

- Fix #24 adjudications spot-checked in the built tree and intact: C2 (B3
  30 ms per-row vs Rule 5 container floor), C3 (B15 `exitFactor` 0.8 single
  source of truth), FILM_F1/F5/F6 naming, Grok pins only, THE CORE +
  "more, not bolder" (orchestrate, 2 hits), /demo gates (below), deferred six
  end-of-project only (orchestrate :8, :103, :370). ✓
- Every decision routes through a named skill (BIND/INNOV, orchestrate
  :32–:34). Design package on every UI surface (orchestrate row 10,
  orch-build-mvp :41, orch-* UI rules); grep for `may skip|can skip|skip the
  design` across orchestrate / Taste / feature-expansion: 0 hits. ✓
- Inventory read BEFORE deciding: orchestrate :66, dispatch-prompt 5a,
  feature-expansion Phase 4, and — the fix #25 §2 close — all six orch-*
  files carry `INVENTORY_F23` ×1 each with the read-before-deciding sentence
  (verified in full in orch-add-feature :33 and the orch-pipeline
  verification bullet). ✓
- No off-skill improvisation path: the only `improvis*` hits in the checked
  files are the recorded-gap rule itself ("improvising around a directive is
  off-skill improvisation and fails"); grep for `use your judgment|best
  judgment|decide for yourself|whatever you think|your own discretion`: 0. ✓
- Frozen texts: the fix #19 D19 lead sentence ("Every UI decision carries a
  thought-out reason across the FULL experience") appears exactly 1× in
  orchestrate; the Depth extension (:147) and the REASON_F25 paragraph (:149)
  extend it without editing it; the count-convention line (:66, "wherever a
  frozen rule text says 'six dimensions', read seven") governs the seven
  reading. `verify19.py` re-run: **71/76**, exactly its codified tail — the
  frozen-text assertions pass. ✓

## §4(a) Verifier updates: PASS with one minor (M1, verifier tails)

Both authorized edits landed; I ran both verifiers myself (do not trust the
note).

- **S1 header:** built `skills/ui-ux-pro-max/SKILL.md:3` (frontmatter) and
  `:8` both read "89 searchable styles (51 active)"; "80 searchable" ×0 in
  the file; inventory `:29` agrees staged + built. "51 active" re-counted
  from `data/styles.csv` myself: **89 rows, 51 active / 29 supplemental /
  9 deprecated, 89 distinct Style IDs** — correct. ✓
- **verify23.py** (run by me): **194/212** (194/211 excl. the owed manifest
  check). The styles check now PASSES (cleared on rebuild, as predicted).
  `verify13h.py` (run by me): **VERIFY FAILED (6 of 97)** — 2 B2 + M3 :61,
  :62, :70, :71 — exactly worker C's after-tail; the three F-04 checks (:57,
  :63, :66) pass. ✓
- **M1 (minor) — verify23/verify24 tails moved 2 / 3 fails beyond the
  predicted codified tails, by census growth from authorized fix25 edits.**
  verify23 is 194/212, not the predicted 196/212. The 2 extra fails vs the
  fix24-codified tail are `COVER_F23` (actual 7 lines vs asserted 4) and
  `BLOCK_F23` (actual 6 vs asserted 5). Cause traced to the files: the
  TESTCOV_F25 paragraph (orchestrate :260) cites `COVER_F23` (+1), and the
  new `design-benchmark-v5.md` cites `COVER_F23` ×2 (:147, :170) and
  `BLOCK_F23` ×1 (:147) — all SPEC-mandated fix25 text, inside verify23's
  census scope (`skills/`). verify24 is **98/105** (98/104 excl. manifest),
  not the predicted 101/105: the 3 extra fails are its two `_F23` census
  checks plus the fix23-leg cascade. The census moves are the same class:
  INVENTORY 5/5 → **11/11** (the §2 inventory close added 6 lines),
  FUNC-BQA 3/3 → **4/4** and ALIGN 15/21 → **18/24** (the browser-qa
  benchmark paragraph cites them), files-with-_F23 18 → **24** (the six
  orch-* files). All other verify24 fails are exactly C's predicted set
  (fingerprint, diff-count, S1, manifest). No plugin text is wrong; the
  verifiers' asserted counts are stale. **Remedy for verify25:** codify the
  new tails — verify23 **194/211** excl. manifest, verify24 **98/104** excl.
  manifest, census INVENTORY 11/11, FUNC-BQA 4/4, ALIGN 18/24, COVER 7/7,
  BLOCK 6/6, 24 files. Severity minor per Audit #71 discipline (record
  issue; SPEC §5 anticipates verify25 codifying the new tails).

## §4(b) Template fonts self-host: PASS with one minor (M2, prose call)

- `skills/pitch-deck-video/template/public/fonts/` holds exactly 3 files,
  all genuine woff2 (`file` magic): HankenGrotesk 34,704 B, InstrumentSerif
  21,032 B, JetBrainsMono 30,376 B. md5s match worker D exactly
  (c501f578… / 9b8dd1ec… / 3c6529cc…). ✓
- `template/src/fonts.ts` imports `loadFont` from `@remotion/fonts` and
  `staticFile` from `remotion`, `loadFont` ×3 with `staticFile('fonts/…')`
  URLs; no `@remotion/google-fonts` import. `template/package.json` has
  `"@remotion/fonts": "4.0.526"` and no `@remotion/google-fonts`. ✓
- **M2 (minor) — decision on the two remaining `@remotion/google-fonts`
  prose mentions: they do NOT count against the self-host requirement.**
  Reason: SPEC §4(b) governs the template's render-time loading behavior —
  imports, dependencies, and fetches — and all of those are 0. The two hits
  are non-code prose: `fonts.ts:2`, an intentional provenance comment
  explaining the old loader (it documents the change, it does not load
  anything); and `skills/mobile-ship/references/launch-marketing.md:15`, a
  pre-existing licences bullet ("Fonts: Google Fonts under the OFL, via
  `@remotion/google-fonts`") outside the template, which no render path
  executes. **But** the mobile-ship line is now a stale instruction: it
  prescribes as the mechanism a loader the plugin no longer ships for the
  template, so a reader following it would reintroduce the removed loader
  in the promo-video path. Minor: reword it to the self-hosted pattern or
  drop the mechanism pointer (a follow-up edit, not a rebuild blocker).
  For completeness, other Google-Fonts fetches in the built tree are
  out of §4(b)'s template scope and were not counted: Taste asset
  demo/lab HTML files still link `fonts.googleapis.com` (Geist, pre-existing
  asset demos), `rules/web-security.mdc` CSP examples name the hosts, and
  ui-ux-pro-max's `google-fonts.csv` is a font catalog, not a fetch.
- Whether the self-host clears the Leg 3 environmental FAIL (59/59) is the
  dry-run worker's verdict, not this audit's; worker D's proof (12/12 stills,
  0 Google-font requests, negative control 404s on local files) was read but
  not re-run here.

## §4(d) Design bar — beat Campus Eats v5: PASS

- Benchmark file present in the built tree:
  `skills/orchestrate/references/design-benchmark-v5.md`, 178 lines,
  byte-identical to staged. Figures verified against worker E's record and
  the file's own table: **61 literal / 60 stricter**; Component 31,
  Treatment 8, Visual 1, Motion 17/16, Moment 1, Type 2, Effect 0,
  Diagram 1; Sticker theme; hero deal `centred`; letters-assemble applied,
  iris-opens dealt-but-unapplied (recorded honestly, with the SPEC's
  "letters-assemble + iris-opens" reading flagged as a discrepancy and
  resolved by making application part of beating v5). Dynamic 8 items /
  1 cross-surface drive / 2 live-data surfaces; no v5 alignment figure
  (bar = ALIGN_F23 matrix). ✓
- Thresholds in all three required homes, all seven dimensions, tie = below
  the bar: orchestrate :70 (bar paragraph), :96 (step 5a static check),
  :364 (final-report beat-v5 table); polish-pass :46 (variety pointer) and
  :101 (non-negotiable 5 benchmark check, candidate evidence only);
  browser-qa :83 (benchmark verdict on the four live dimensions) and :115
  (output-format checklist line); Taste :409 (deal-point pointer). The
  static/live split is preserved everywhere: browser-qa remains the sole
  verdict executor; static checks never render screen verdicts. ✓
- Caveat carried (worker E §8, not a finding): the v5 figures are
  render-history figures, not live-measured (no live v5 artifact in the
  workspace); the dynamic count of 8 is E's enumeration from prose history —
  the dry-run worker must re-derive it. The Leg 2 beat-v5 verdict itself
  belongs to dry-run #40.

## §4(e) Technical depth: PASS

- `TECHDEPTH_F25` in all required homes: hackathon-scope §57 (Technical
  substance block — architecture, named algorithm/data-structure, named
  performance budget or explicit `no budget — <reason>`, ≥3 edge cases per
  CORE flow; **no silent re-scope** rule with `cut substance: <what> —
  <why>` lines in the cut list and the decision record — read in full),
  hackathon-scope :96 (Quiet re-scope trap row), orchestrate :89 (step-4
  implementer-brief paragraph — read in full: architecture slice,
  algorithm choice with why, budget, ≥3 edge cases; arch/algorithm route to
  deep-reasoner, never a fast-worker brief; cut lines; 4b probes the hard
  path), orchestrate :96 (5a static check) and :367 (final report),
  feature-expansion :149 (brief item 8) and :166 (Phase 5 substance
  verification — real path, edge cases, budget, not only the happy path). ✓
- Deferred six NOT un-deferred: substance verification sits in the build-time
  Verify steps and the final report, as required. No new skill created. ✓

## §4(f) Adaptive + creative: PASS

- `ADAPT_F25`: grill-me :25 (specified-ness assessment — EXECUTION posture
  for a big prompt, REASONING posture for a vague one-liner, Source tags
  USER-STATED / INFERRED / ASSUMED — read in full) and orchestrate :87
  (orchestrator + design-lead adapt to the idea; the decision record is the
  authority for a big prompt). ✓
- `REASON_F25`: orchestrate :149 (mandatory INFERRED / CHOSEN / REJECTED
  block per decision-record entry — read in full; extends, does not edit,
  the frozen D19 text), orchestrate :96 (5a static check), grill-me :39
  (step-5 record format). ✓
- `CREATIVE_F25`: feature-expansion :58 (Lens B substance line), :92 (No
  UI-only slate), :98 (balance check — at least one substance item, same
  one-round re-brainstorm cap). Creativity applies to what the product DOES,
  not only how it looks. ✓

## Cross-cutting

- Counts and pins unchanged unless justified: counts unchanged (166/72/123/
  87/15/64); the only count moves are the _F23 census lines in M1, each
  traced to an authorized fix25 edit. ✓
- No re-litigation of fixes #14–#24 adjudications: none found. The C2/C3
  scope splits, FILM_F1/F5/F6, /demo gates, Casberry bar (untouched),
  APCA-informational, THE CORE, inventory, and the deferred six all stand
  as recorded. ✓
- /demo gates stand: orchestrate :99 (DEMOGATE_O4_F22 — never dispatched,
  explicit invocation only, local filming only), :101 (DEMOGATE_O9_F22),
  :56/:58 (narration-key prompt ONLY when the user asked for a demo video;
  `commands/demo.md:13` — never prompt on a dispatched run, never ask
  twice). ✓
- `build.sh` fix25 comment (24060–24068) still describes fix25.py as "§4(a)
  S1" only; the script now also carries the §1 wires, the §2 inventory
  close, and the §4(d) browser-qa line. Deliberately not edited (additions-
  only diff invariant) — recorded here as a known stale comment, not a
  finding.

## Findings

| # | Severity | Location | SPEC clause | Finding |
|---|---|---|---|---|
| M1 | minor | `fix23/verify23.py` tail; `fix24/verify24.py` tail (verifier records, not built-tree text) | SPEC §5 "Prior verifiers: fails must be only the codified tails" | verify23 194/212 (194/211 excl. manifest) vs codified 196/211 — extra fails COVER_F23 (7 vs 4) and BLOCK_F23 (6 vs 5). verify24 98/105 (98/104 excl. manifest) vs predicted 101/105 — extra fails are its two _F23 census checks (INVENTORY 11/11 vs 5/5; FUNC-BQA 4/4 vs 3/3; ALIGN 18/24 vs 15/21; 24 files vs 18) plus the fix23-leg cascade. All moves traced to authorized fix25 edits (TESTCOV_F25 paragraph, design-benchmark-v5.md, §2 inventory close, browser-qa benchmark line). Remedy: verify25 codifies the new tails and census counts. |
| M2 | minor | `hackathon-ecc/skills/mobile-ship/references/launch-marketing.md:15` | SPEC §4(b) | Pre-existing licences bullet still prescribes `@remotion/google-fonts` as the font mechanism for promo videos, while the template no longer ships that loader. Prose mentions do not count against the §4(b) self-host requirement (decision recorded in §4(b) above), but this line is a live instruction that would reintroduce the removed loader if followed. Remedy: reword to the self-hosted pattern or drop the mechanism pointer. |

**Blocking findings: 0. Minor findings: 2.**

## Could not verify / owed (not findings)

- **Live Cursor behavior of the ck wire** (does Cursor fire
  `hooks/session-start.js` on session start in Anish's Cursor, does the
  merged `additional_context` surface): owed to the live smoke test. The
  Node mechanics were proven on scratch by worker B; this audit verified
  only the built-tree placement.
- **Dry-run legs** (Leg 2 beat-v5 re-trace incl. re-deriving the dynamic
  count of 8; Leg 3 /demo 59/59 vs owed; Leg 5 call-graph + hard-idea
  collaborative-editor fixture): owned by dry-run #40, running in parallel.
- **verify25 codification** of the M1 tails/census counts: owned by the
  verify25 worker.
- **Open parent decisions** (recorded, not decided here): ck wire cost
  (~1k tokens/session measured vs ~100 assumed — keep / trim / dormant);
  trigger-router B6 (maintain `skill-triggers@1.json` vs documentation-only);
  epic commands reachable-but-dormant-in-use; the stale `build.sh` fix25
  comment (deliberately unedited).
- **v5 figures** are render-history figures (worker E §8); the benchmark
  file states the caveat in full.
