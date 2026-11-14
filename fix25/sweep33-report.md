# Sweep #33 — Fix #25, Phase 3b (hackathon-ecc) — CHECK-ONLY report

**SWEEP #33: NOT CLEAN — 0 blocking, 2 minor**

Scope: staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`), the built tree `~/workspace/hackathon-plugin/hackathon-ecc/`
(node_modules excluded everywhere), `build.sh`, `fix25/fix25.py`, and the
fix #25 working files. Check-only: no plugin file edited, no `build.sh`
run, no fix/apply/verify script edited or run. No bundle, commit, push,
or message sent.

Read first, in full: `fix25/SPEC.md` (§0–§6),
`fix25/PARENT-GUIDANCE.md`, `fix24/MANIFEST.md`, `fix25/build-note.md`,
`fix25/callmap/wiring-list.md`, `fix25/verifier-updates.md`,
`fix25/template-fonts.md`, `fix25/design-tech-depth.md`,
`fix25/weave-wiring.md`, `fix25/fix25-run-log.md`. Every number below was
re-derived by the sweeper's own greps/commands listed in §9; nothing was
copied from the Phase 1/2 work notes or the build note without re-running.

Note on the prior round: no `fix24/sweep32-report.md` file exists — the
fix #24 MANIFEST cites "Sweep #32: 0 BLOCKING, 6 MINOR" but no report
file was saved under `fix24/` or anywhere else in the tree (searched).
This report therefore follows the format and severity discipline of
Sweep #31 (`fix23/sweep31-report.md`), the closest surviving prior
round, and re-verifies the fix #24 baseline from the files rather than
from a missing Sweep #32 report.

## 1. Build fingerprint + diff

| Item | Re-derived value | Expected | Result |
|---|---|---|---|
| `build.sh` lines | 24,079 (`wc -l`) | 24,079 | PASS |
| `build.sh` md5 | `f19483f50e89998f8b9dc052ed5d5fae` | same | PASS |
| `build.sh.before-fix23` lines / md5 | 23,774 / `4799a819791b9c3ec4c19136ad698397` | same | PASS |
| `diff build.sh.before-fix23 build.sh` | **+305 / −0** | +305/−0 | PASS |

The fix25 invocation block sits at `build.sh:24062–24068` (comment +
`python3 "$PLUGIN_ROOT/fix25/fix25.py" "$PLUGIN_DIR"`), after the fix24
invocation and before STEP 5 Counts — additions only, as required.

## 2. Anchor table — every `_F25` token re-derived

`grep -rn` / `grep -rho` over staged sources and over the built tree
(`hackathon-ecc/skills|commands|rules|hooks`, excl. node_modules).
Staged counts are lines carrying the token; occurrences are literal
substring counts. Built counts are the same measure on the built copy.

| Token | Staged lines / occ | Built lines / occ | Locations (staged file:line) |
|---|---|---|---|
| RECIPES_F25 | 1 / 1 | 1 / 1 | orchestrate/SKILL.md |
| TESTCOV_F25 | 1 / 1 | 1 / 1 | orchestrate/SKILL.md |
| PLATFORM_F25 | 2 / 2 | 2 / 2 | grill-me/SKILL.md; hackathon-scope/SKILL.md |
| BENCHMARK_V5_F25 | 8 / 8 | 10 / 10 | orchestrate/SKILL.md ×3; design-benchmark-v5.md ×2; polish-pass/SKILL.md ×2; design-taste-frontend/SKILL.md ×1 |
| TECHDEPTH_F25 | 7 / 7 | 7 / 7 | orchestrate/SKILL.md ×3; hackathon-scope/SKILL.md ×2; feature-expansion/SKILL.md ×2 |
| ADAPT_F25 | 2 / 2 | 2 / 2 | grill-me/SKILL.md; orchestrate/SKILL.md |
| REASON_F25 | 4 / 5 | 4 / 5 | grill-me/SKILL.md ×1; orchestrate/SKILL.md ×3 lines (5 occ — one line carries the token twice) |
| CREATIVE_F25 | 3 / 3 | 3 / 3 | feature-expansion/SKILL.md ×3 |
| FILM_F1 / FILM_F5 / FILM_F6 | 1 / 1 each | 1 / 1 each | pitch-deck-video/SKILL.md (unchanged from fix #24) |

- **Built BENCHMARK_V5_F25 is 10, not 8 — explained, not a drift:**
  the extra 2 are the fix25.py browser-qa patch (benchmark verdict
  paragraph + output-format line, `hackathon-ecc/skills/browser-qa/
  SKILL.md:83,:115`). Staged 8 + build-time 2 = built 10. Every other
  token matches staged exactly.
- **No other `_F25` token exists anywhere** (`grep -rho "[A-Z][A-Z0-9_]*_F25"`
  over staged + built: exactly the 8 tokens above, totals
  RECIPES 2, TESTCOV 2, PLATFORM 4, BENCHMARK 18, TECHDEPTH 14,
  ADAPT 4, REASON 10, CREATIVE 6 — staged + built sums reconcile).
  No orphan anchors: every token is defined exactly once per home —
  RECIPES_F25 by its orchestrate lookup paragraph; TESTCOV_F25 by
  orchestrate Verify step 1; PLATFORM_F25 by grill-me step 4 +
  hackathon-scope's platform bullet; BENCHMARK_V5_F25 by
  `design-benchmark-v5.md` (home) with pointers in orchestrate, Taste,
  polish-pass, browser-qa; TECHDEPTH_F25 by hackathon-scope's
  Technical-substance section (home) with pointers in orchestrate and
  feature-expansion; ADAPT_F25 by grill-me step 2 + orchestrate;
  REASON_F25 by grill-me step 5 + orchestrate's reasoning-format rule
  + orchestrate step 5a; CREATIVE_F25 by feature-expansion Lens B /
  UI-only slate / balance check. FILM_F1/F5/F6 definitions live only
  in fix22/SPEC.md:395, per the fix #24 C6 correction — unchanged.
- **D19 frozen text intact:** the fix #19 D19 lead sentence ("Every UI
  decision carries a thought-out reason across the FULL experience")
  appears exactly **1×** in staged orchestrate/SKILL.md. The REASON_F25
  paragraph was added as a new paragraph in the Depth-extension
  pattern, not an edit to the frozen paragraph.
- **Staged = built, byte-for-byte:** `diff -q` clean for both
  `new-skills/orchestrate/references/call-map.md` vs
  `hackathon-ecc/skills/orchestrate/references/call-map.md` and
  `new-skills/orchestrate/references/design-benchmark-v5.md` vs its
  built copy.

## 3. Cross-skill pointer resolution — every new fix #25 pointer

Every pointer introduced by fix #25 (staged text + fix25.py patch
text) resolves to a real file in the built tree:

| Pointer (as written) | Built-tree target | Result |
|---|---|---|
| `references/design-benchmark-v5.md` / `skills/orchestrate/references/design-benchmark-v5.md` (orchestrate:70, Taste:408, polish-pass non-neg. 5, browser-qa:83) | `hackathon-ecc/skills/orchestrate/references/design-benchmark-v5.md` (11,751 B, byte-identical to staged) | PASS |
| `skills/conventional-commit-review/SKILL.md` (orchestrate step 6, prp-commit Phase 3) | exists | PASS |
| `agents/ecc-commit-reviewer.md` (same two sites) | exists | PASS |
| `ecc-recipes` skill (orchestrate RECIPES_F25 paragraph) | `hackathon-ecc/skills/ecc-recipes/SKILL.md` exists | PASS |
| `/test-coverage` command, Steps 1–2 (orchestrate TESTCOV_F25) | `hackathon-ecc/commands/test-coverage.md` exists | PASS |
| `tdd-workflow` as fix-loop owner (same paragraph) | `hackathon-ecc/skills/tdd-workflow/SKILL.md` exists | PASS |
| `skills/ck/hooks/session-start.mjs` (fix25.py ck wire) | exists | PASS |
| `hooks/session-start.js` runs it (ck SKILL.md note) | `hackathon-ecc/hooks/session-start.js:79–81` spawns it | PASS |
| `skills/orchestrate/references/design-inventory.md` (orch-* inventory close) | exists; INVENTORY_F23 ×1 in each of the six built orch-* files | PASS |
| `skills/design-taste-frontend/references/hallmark/references/redesign.md` (orchestrate 5b, pre-existing) | exists | PASS |
| `git-workflow` (linked second-order orphan, via `conventional-commit-review`) | backticked at `hackathon-ecc/skills/conventional-commit-review/SKILL.md:104` | PASS |
| `liquid-glass-design` (the fix #22 dangling-reference model) | **absent** from all live staged sources, the built tree, and `build.sh` — only stale hits in old backup/audit dirs (`hackathon-plugin-fixed-backup-audit4/`, `audit9/backtick-all.txt`, etc.), none of them plugin code | PASS — no recurrence |

## 4. /demo never-automatic re-check

- All six DEMOGATE sites present: DEMOGATE_O4_F22 + DEMOGATE_O9_F22
  (staged orchestrate), DEMOGATE_H1_F22 + DEMOGATE_H2_F22 (staged
  `new-rules/hackathon-mode.mdc:12,:68`), DEMOGATE_B2S1_F22 (built
  orch-build-mvp:85), DEMOGATE_B3S1_F22 (built orch-change-feature:51).
  B2S2–S7 / B3S2–S7 siblings also present, unchanged.
- No fix #25 staged edit adds any `/demo` invocation, narration-key
  prompt, or auto-invocation wording. The narration-key prompt still
  fires ONLY when the user asked for a demo video (orchestrate step 0,
  unchanged).
- The deferred six (`production-audit`, `delivery-gate`,
  `codehealth-mcp`, `verification-loop`, `santa-method`,
  `security-scan`) still run only at end-of-project: orchestrate's
  "End-of-project checks" names all six by name, unchanged in
  standing; no fix #25 text un-defers any of them.

## 5. Weaving-coherence pass — per-section table

Method: for each section, read the placed lines in context and
confirmed (a) the item sits in the SPEC'd flow, not appended at a file
end; (b) its pointers resolve to a real home (§3); (c) it does not
duplicate an existing rule without a recorded distinction; (d) the
fix #25 additions read as part of the one story (grill → design
package → build → verify → polish → deploy → commit → README → final
report), with no bypassable step.

| Section | Placement (re-derived) | Coherence verdict |
|---|---|---|
| §1 call map | `new-skills/orchestrate/references/call-map.md` (staged, generated) — header counts 166/72/123/87/15/64; uncalled summary 52 (24 skills / 21 agents / 0 rules / 7 commands); second-order orphans 13; `ck` row: `hooks/session-start.js [strong]`, flow "always-on (Cursor event)"; epic/`/prune` rows name orchestrate as invoker via RECIPES_F25 | CLEAN. Counts agree with the tree; the 52 matches the build note and worker B's post-rebuild expectation exactly; the map's flow line (:18) names the full sequence (grill → design package → build → verify → polish → deploy → commit → README → final report, /demo on-request only, end-of-project skills end-only). One open note, not a finding: the map does not cite `design-benchmark-v5.md` anywhere (see §8.3) — the map's scope is elements, and the benchmark file cites no skill by backticked name, so the generator cannot list it as an invoker; the benchmark pointers in the skills themselves resolve (§3). |
| §1 wires (RECIPES / TESTCOV / ck / prp-commit) | RECIPES_F25 paragraph before the Design-package rule (orchestrate, routing section); TESTCOV_F25 in Verify step 1 (orchestrate); ck wire in fix25.py + ck SKILL.md note (built :157); conventional-commit-review + ecc-commit-reviewer in orchestrate step 6 and prp-commit Phase 3 (built :59) | CLEAN. Each wire is a real dispatch path named at the step that owns it; the RECIPES_F25 paragraph explicitly gates the epic/`/prune` commands (reachable, dormant in use) so the map's reachability reading does not silently re-activate them; the TESTCOV_F25 wire is scoped to measurement (Steps 1–2), generation stays in the fix loop — the Verify-is-a-check boundary is stated, not blurred. |
| §2 inventory bypass close | INVENTORY_F23 ×1 in all six built orch-* files (4 UI rules + orch-build-mvp design-package paragraph + orch-pipeline Verification bullet); dispatch-prompt.md:24 (§5a) already carried the inventory read for orchestrate's own dispatches; feature-expansion Phase 4 UI rule already carried it | CLEAN. The bypass worker B found (0 inventory mentions in the orch-* family) is closed at every family entry point, and the enforcement point (orch-pipeline Verification bullet) names it. dispatch-prompt.md §5a names the inventory but not the benchmark — not a bypass (see §8.4): the benchmark read is instructed at the design-lead's own steps (orchestrate step 3, Taste step 4a), and the benchmark is enforced whole-build at orchestrate 5a + polish-pass + browser-qa regardless of dispatch. |
| §4(a) S1 | Staged inventory:29 reads "89 searchable styles (51 active)"; built ui-ux-pro-max SKILL.md:3 and :8 both read "89 searchable styles (51 active)" ("89 searchable styles" ×2 in the file); "80 searchable" ×0 in staged sources and ×0 in the built tree | CLEAN. The header, the body line, and the inventory agree; the csv remains the source ("the csv is the inventory source" kept on :29). |
| §4(b) template fonts | Staged `new-skills/pitch-deck-video/template/src/fonts.ts` imports `loadFont` from `@remotion/fonts` (:22) + `staticFile` from `remotion` (:23), `loadFont` ×5, no `@remotion/google-fonts` import; `package.json` has `"@remotion/fonts": "4.0.526"`, no `@remotion/google-fonts`; `public/fonts/` holds the 3 woff2 files | CLEAN (staged side). The self-host is woven, not bolted on: same family names, same fail-closed shape, header comment records why + provenance. The built tree carries it (build note). The 2 raw-string `@remotion/google-fonts` hits left in the built tree are prose only — `fonts.ts:2` (the intentional provenance comment) and `round2-skills/mobile-ship/references/launch-marketing.md:15` (pre-existing staged text, untouched by fix #25) — zero imports, zero deps. Whether prose mentions count against "must be 0" is the build worker's flagged caveat for the audit to decide; this sweep records it, it does not re-decide it (§8.5). |
| §4(d) benchmark | Benchmark file (178 lines, frozen at v5) + orchestrate:70 bar paragraph (before the MEMORABLE paragraph, in the step-3 design-package flow) + orchestrate 5a static check + orchestrate final-report beat-v5 table line + Taste:408 deal-point pointer (immediately after the dealt-moments line) + polish-pass non-negotiable 5 + variety pointer + browser-qa:83/:115 live verdict | CLEAN. All seven dimensions agree across all five homes (count ≥62/≥61 stricter; variety ≥7 kinds, ≥2 above v5; hero inventory + loop or second moment; Motion ≥18/≥17 stricter; ≥9 interactive items, ≥2 cross-surface drives; ≥3 live-data surfaces; 0 alignment problems) — verified by reading each home, not by trusting worker E's §7 counts (which also reconcile: orchestrate 3, polish-pass 2, Taste 1, benchmark file 2, browser-qa 2). The static/live split is preserved everywhere: static dimensions scored from the decision record's table, live dimensions browser-qa's alone, unscored dimensions owed never passed. The SPEC's "letters-assemble + iris-opens" reading is honestly corrected in the benchmark file (iris-opens dealt, no recorded application; applying it is part of beating v5) — the coordinator confirmed this resolution in the run log. The v5 figures carry their provenance caveat in full (§1 + §8 of the benchmark file). |
| §4(e) technical depth | hackathon-scope Technical-substance section (before "Vertical slices") + scope-traps "Quiet re-scope" row + orchestrate step-4 implementer-brief paragraph + orchestrate 5a TECHDEPTH_F25 static check + orchestrate final-report engineering line + feature-expansion brief item 8 + Phase 5 item 2 | CLEAN, with ONE minor tension (MINOR 2, §7): the scope-traps "Edge case obsession" row still prescribes "Demo doesn't enter X" as its antidote with no qualifier, while the new TECHDEPTH_F25 section in the same file says that phrase is a cut, not a handling. Otherwise coherent: "at least 3 named edge cases with handling" is stated identically in scope (per CORE flow), orchestrate step 4 (per slice), orchestrate 5a (per CORE flow), and feature-expansion item 8 (per feature) — different units (flow/slice/feature), all satisfiable together, no contradiction. Off-the-shelf maximalism is explicitly preserved in all three homes (scope section, orchestrate step 4, expansion item 8): substance is the architecture/algorithms/system design AROUND the tools, never a from-scratch rewrite. The no-silent-re-scope rule is stated in scope ("cut substance: <what> — <why>"), orchestrate step 4 (cut line in brief + decision record), orchestrate 5a (a hard idea rebuilt as easy with no cut line is incomplete), and expansion item 8 / Phase 5 (implementer reports the cut with its reason). Enforcement exists in both flows: orchestrate flow via 5a; standalone orch-build-mvp flow via its step 6b polish-pass run (benchmark + substance candidate evidence) and expansion Phase 5, which orch-build-mvp step 6 invokes BY NAME ("Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5"). No whole-build 5a-style static check exists in orch-build-mvp itself — the standalone flow relies on per-feature Phase 5 confirmation; recorded as an observation (§8.6), not a bypass, since Phase 5 item 2 exercises substance per landed feature. |
| §4(f) adaptive + creative | grill-me step 2 ADAPT_F25 (specified-ness assessment + Source tags) + grill-me step 5 REASON_F25 (three-part format + Source tag per entry) + orchestrate ADAPT_F25 paragraph (before step 4 "Build") + orchestrate REASON_F25 paragraph (after the Depth extension, new paragraph, frozen D19 untouched) + feature-expansion Lens B / Lens D / UI-only slate / candidate shape Substance line / balance check / planner rubric | CLEAN, with ONE minor gap (MINOR 1, §7): the REASON_F25 paragraph claims the three lines "are checked by the step-2 reviewer and the step-5a static check" — the 5a check exists, the step-2 reviewer check does not. Otherwise coherent: EXECUTION vs REASONING posture is defined identically in grill-me step 2 and orchestrate (big prompt = execute recorded decisions, do not re-ask; vague one-liner = reason and gap-fill, inferences recorded as INFERRED with reasoning, never as user-stated); the Source tags (USER-STATED / INFERRED / ASSUMED) match in both homes; the decision record is the authority in both ("a proposal that contradicts it loses to it" / "the recorded decision wins"). CREATIVE_F25 is consistent across its homes: Lens B substance line, the UI-only-slate anti-pattern, the balance check's third leg (≥1 substance item, same one-round re-brainstorm cap and terminal rule as the other legs), and the planner rubric's "a 3 here requires a named algorithm, data structure, or system-design move, not just 'uses an API'". |
| THE CORE / "more, not bolder" / anti-derivative | Unchanged in standing: orchestrate:70 MEMORABLE paragraph, :149 F6-primary-gate, "Posture — more, not bolder" paragraph, anti-derivative rule — all re-read, none edited by fix #25 | CLEAN. The §4(d) bar raises the floor (a v5-level design is now BELOW the bar) without restating or contradicting THE CORE: "better" is measured on seven dimensions (count AND variety, hero, motion, dynamic, functionality, alignment), not loudness; polish-pass's memorability paragraph still states "more, not bolder still governs styling". The benchmark's variety dimension (≥2 kinds above v5) is the "more, not bolder" rule expressed as a count. No fix #25 text re-litigates a fix #14–#24 adjudication. |
| C2/C3 scope splits | Built `motion-foundations/SKILL.md:409` (B3 30ms per-row stagger vs Rule 5 container floor) and `:435` (B15 `exitFactor: 0.8` single source of truth) — both re-read, both carry the "Adjudicated fix #24" text | CLEAN. Untouched by fix #25; no fix #25 text restates a stagger or exit factor. |
| Six/seven count convention | Frozen "six" texts byte-identical (D19 lead 1×; X1 "six … dimension lines"; harmony "all six dimension lines"; 5a "(D19) … all six dimension lines"); count-convention lines present in orchestrate:66, Taste:255, polish-pass:23; editable sites say seven (slop-checklist:51, unslop-fixes:12, vercel-checklist:81, orchestrate:89 DIRECTIVES "seven dimensions") | CLEAN. No fix #25 text adds a new "six" statement; the REASON_F25 paragraph carries no count. The convention governs the seven reading exactly as fix #24 adjudicated. |

No section fails coherence except for the two minor items in §7. All
disposition line numbers re-verified current (no drift since the build).

## 6. fix25.py anchor provenance — every anchor verified in its source

`fix25/fix25.py` (298 lines) patches the built tree only; every `sub()`
asserts count==1 and fails loudly. The build log records 14 changes,
0 errors. Each anchor's target text was verified in the file the script
actually patches — the ECC install (`/tmp/ecc-dev-install/.cursor`),
the ui-ux-pro-max upstream (`/tmp/uipro`), or `build.sh`'s own inline
patches — not from the script's comments:

| # | Anchor (file patched) | Proven in source |
|---|---|---|
| 1 | ui-ux-pro-max SKILL.md :3 — `"Searchable local data: 80 searchable styles (51 active)"` | `build.sh:586` `replace_desc_line("ui-ux-pro-max", …)` writes exactly this string (the NEW description); the source string also exists in `/tmp/uipro` template JSONs |
| 2 | ui-ux-pro-max SKILL.md :8 — `"Searchable local UI/UX guidance: 80 searchable styles (51 active)"` | `/tmp/uipro/.claude/skills/ui-ux-pro-max/SKILL.md:8`, verbatim |
| 3 | `hooks/session-start.js` — `"} = require('./adapter');"` | `/tmp/ecc-dev-install/.cursor/hooks/session-start.js` ×1 (build copies hooks from `$ECC_SRC/hooks`, `build.sh:192`) |
| 4 | `hooks/session-start.js` — `process.stdout.write(JSON.stringify(mergeSessionStartOutputs(outputs)));` | same file ×1 |
| 5 | `skills/ck/SKILL.md` — the 3-line `$HOME` paragraph | `/tmp/ecc-dev-install/.cursor/skills/ck/SKILL.md` (lines match verbatim) |
| 6 | `commands/prp-commit.md` — `"Craft a single-line commit message in imperative mood:"` | `/tmp/ecc-dev-install/.cursor/commands/prp-commit.md` ×1 |
| 7–10 | orch-add/change/fix/refine SKILL.md — `"run the applicable package components before the change lands."` | `build.sh` UI-change rules at :22209, :22686, :22691, :22697 (one per file's patch block) — the sentence is introduced by build.sh's own patches, not by the ECC repo clone (verified absent there) |
| 11 | orch-build-mvp SKILL.md — `"Every slice that touches a UI surface names its design components … before building UI"` | `build.sh` ×1 |
| 12 | orch-pipeline SKILL.md — `"- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed …"` | `build.sh` (substring; the built file carries it ×1 — the build log's 0-error run proves the count==1 assertion held) |
| 13 | browser-qa SKILL.md — `"This verdict is \`browser-qa\`'s alone: no other step judges memorability."` | `build.sh:24004`, the fix #23 CORE block (MEMORABLE-BQA-01), inserted after the hero-verdict anchor — absent from both ECC upstream copies, as expected |
| 14 | browser-qa SKILL.md — Memorability output-format line | `build.sh` ×1 (fix #23 CORE block's report row) |

All 14 anchors exist where the script expects them. No anchor was
verified from the script's comments alone. (One correction to worker
C's note, for the record: the `:8` line could not be checked against
upstream "by elimination only" — `/tmp/uipro` is present on this VM
and the line is verbatim at `uipro/.claude/skills/ui-ux-pro-max/
SKILL.md:8`.)

## 7. Findings

### MINOR 1 — REASON_F25 claims a "step-2 reviewer" check that does not exist

- **File:line:** `new-skills/orchestrate/SKILL.md:149`
  (built copy `hackathon-ecc/skills/orchestrate/SKILL.md:149`).
- **Text:** "The three lines are checked by the step-2 reviewer and
  the step-5a static check (REASON_F25) — a static check on the
  record's presence, never a verdict on the reasoning's quality,
  which is the reviewer's and browser-qa's judgment."
- **SPEC clause violated:** §2 — every decision routes through a
  named skill; a named enforcement point must resolve to a real
  check. (Also §4(f): the reasoning format's enforcement.)
- **Evidence (re-read, not asserted):** the step-5a static check
  exists (orchestrate:96, REASON_F25 — "an entry missing any of the
  three lines is an incomplete build"). But no reviewer anywhere is
  instructed to check the three-part block: the only "step-2
  reviewer" in the file is Verify step 2, the blind code-reviewer,
  whose "Design-direction record check (UI diffs)" paragraph checks
  only the named direction and "all six fix #19 D19 dimensions" —
  never INFERRED / CHOSEN / REJECTED — and it receives only the diff
  and the contract's acceptance criteria, not the decision record.
  `grep -rn "step-2 reviewer"` over all staged sources returns only
  :149 itself. `grep -rn "three-part|reasoning format"` over staged
  + built returns only orchestrate:96, orchestrate:149, and
  grill-me:39 (the format definition, not a check). No other file
  (grill-me, feature-expansion, hackathon-scope, polish-pass,
  dispatch-prompt) gives any reviewer a REASON_F25 check.
- **Severity MINOR:** the 5a static check still enforces the format,
  so the rule is not unenforced — the sentence overclaims a second
  checker. Fix is one line: either add the three-part presence check
  to the step-2 reviewer's design-direction record check, or drop
  "the step-2 reviewer and" from :149.

### MINOR 2 — Scope-trap "Edge case obsession" row vs TECHDEPTH_F25

- **File:line:** `rewritten-skills/hackathon-scope/SKILL.md`
  (scope-traps table, "Edge case obsession" row) vs the
  Technical-substance section in the same file (TECHDEPTH_F25).
- **Text:** trap row antidote: "Demo doesn't enter X". TECHDEPTH_F25:
  "Edge cases — at least 3 named per CORE flow, each with its
  handling … 'Demo doesn't enter X' is not a handling; it is a cut,
  and it goes in the cut list below with its reason." And: "A cut
  with no recorded reason is a scope gap, not a decision."
- **SPEC clause violated:** §2 dedupe/contradiction — "the same rule
  stated in two places agrees, or one defers to the other by name."
  Neither side defers by name: the trap row does not point at
  TECHDEPTH_F25, and the TECHDEPTH section does not name the trap
  row (it names the phrase, not the row).
- **Evidence:** both texts re-read in the same file. The two are
  reconcilable — the specific (TECHDEPTH, CORE flows) governs the
  general (trap table) — but an agent following the trap row alone
  would skip CORE-flow edge cases without recording the cut, which is
  exactly the silent re-scope §4(e) forbids. The trap table is
  upstream-verbatim text ("Original by RR-AMATOK, used verbatim"),
  which is why the tension was not caught when the TECHDEPTH section
  was added.
- **Severity MINOR:** the newer, explicit rule governs and is
  unambiguous for anyone who reads the TECHDEPTH section; the trap
  row needs a one-line qualifier, e.g. "(record it as a cut —
  TECHDEPTH_F25)".

## 8. Banned terms, Grok pins, counts

- **Banned terms 0 in the built tree** — `grep -rliE
  "claude|codex|anthropic|opus|sonnet|haiku|composer-2.5"` over
  `hackathon-ecc/skills|agents|commands|rules|hooks|scripts`
  (excl. node_modules): 0 files. **Staged sources carry 18 hits** —
  all pre-existing upstream-verbatim text, none introduced by
  fix #25 (fix #25 touched neither file): 17 in
  `rewritten-skills/app-scaffold/` ("Claude Code workflow" section,
  `SKILL.md:3,8,25,37,207,238` + `reference/workflow.md` +
  `reference/best-practices.md:69` + `templates/package-scripts.json:2`)
  and 1 in `new-rules/hackathon-mode.mdc:38` ("its upstream
  `claude -p` invocation path does not run in Cursor"). All are
  removed at build time by fix16's Claude-scrub — verified: the same
  grep over the built `skills/app-scaffold/` and
  `rules/hackathon-mode.mdc` returns 0. The staged hits are the
  established pattern (upstream verbatim in, scrubbed at build), not
  a fix #25 finding. (The pre-existing non-term `composer-tier` in
  orchestrate is not a banned term.)
- **Grok pins only** — no fix #25 staged edit touches a model pin;
  build note reports `grok-4.7-high` ×54,
  `cursor-grok-4.6-high-fast` ×103, bare `grok-4.6-high-fast` ×0 in
  the built tree (taken from the build log; spot-verified that no
  fix #25 file contains a pin edit).
- **Counts re-derived:** call-map header 166 skills / 72 agents /
  123 rules / 87 commands / 15 hooks / 64 trigger keys; uncalled 52;
  second-order orphans 13 — all matching the build note and worker
  B's post-rebuild expectation. No new skill, command, rule, agent,
  hook, or trigger added by fix #25.

## 9. Open items (carried, explicitly — not findings this round)

1. **No Sweep #32 report file exists** (see the note at the top):
   fix #24's MANIFEST cites Sweep #32 (0 BLOCKING, 6 MINOR) but no
   report file was saved. This sweep re-verified the fix #24
   baseline from the files (C2/C3, FILM_F1/F5/F6, D19 1×, DEMOGATE
   sites, deferred six, count convention) rather than relying on it.
2. **Template-fonts prose mentions** (build worker's caveat 1,
   carried): `@remotion/google-fonts` still appears 2× as raw strings
   in the built tree — both prose, zero imports/deps (`fonts.ts:2`
   provenance comment; `mobile-ship/references/launch-marketing.md:15`
   pre-existing). Whether prose mentions count against the §4(b)
   "must be 0" criterion is for the audit to decide; this sweep
   records it and does not re-decide it.
3. **Benchmark file not cited from the call map** (worker E's §8.7
   flag, not acted on by worker B): the map's scope is elements and
   the generator lists a reference file as an invoker only when it
   cites skills by backticked name (as `design-inventory.md` does);
   `design-benchmark-v5.md` cites no skill that way, so it appears
   nowhere in the map. The benchmark pointers in the skills resolve
   (§3). If the parent wants the map to index the benchmark file,
   the generator needs a reference-file row — a generator change,
   not a skill edit.
4. **dispatch-prompt.md §5a names the inventory but not the
   benchmark:** the benchmark read is instructed at the design-lead's
   own steps (orchestrate step 3, Taste step 4a), and enforced
   whole-build at orchestrate 5a + polish-pass + browser-qa. Not a
   bypass. If a future fix wants the dispatch template to carry the
   benchmark line too, it is a one-line addition.
5. **Skip-grilling stub record vs the REASON_F25 5a check:** when
   grill-me is skipped, hackathon-scope writes a stub decision record
   (undecided items as accepted unknowns) with no stated three-part
   format; the 5a static check ("every decision-record entry carries
   the three-part reasoning block") would flag such entries. The
   check catches it rather than silently passing, so nothing is
   bypassed — but the stub format is unspecified. A one-line
   statement in hackathon-scope (stub entries in REASON_F25 format,
   or the 5a check exempting stub/unknown entries) would close it.
6. **No 5a-style whole-build static check in orch-build-mvp:** the
   standalone flow enforces technical substance via hackathon-scope's
   block + feature-expansion Phase 4 brief item 8 + Phase 5 item 2
   (invoked BY NAME from orch-build-mvp step 6) + polish-pass step
   6b. That is the verification §4(e) asked for; a 5a-equivalent
   static check in orch-build-mvp would be belt-and-braces, not a
   gap.
7. **Carried parent decisions (unchanged from Phase 2):** trigger
   router maintain-vs-documentation-only (B6); ck wire cost ~1k
   tokens/session vs ~100 assumed; epic commands reachable-but-
   dormant-in-use; `build.sh:24062–24067` fix25 comment now stale
   (says "§4(a) S1" only — deliberately not edited, additions-only
   invariant).
8. **Prior open items carried forward (not fix #25 scope):** Netlify
   row in deploy-fast (touch-up due after Dec 4, 2026); pip pinning
   pass; fix #17 R1/R4 unverified; fresh bundle needed before any
   push (do NOT push b2444de).

## 10. Commands run (method)

All run read-only from `~/workspace/hackathon-plugin` (built-tree
greps from `hackathon-ecc/`; upstream greps from `/tmp/ecc-dev-install`
and `/tmp/uipro` — read-only, no test copies made):

- `wc -l build.sh build.sh.before-fix23 && md5sum …` + `diff … | grep -c '^>'` / `'^<'`
- `diff -q` staged vs built for `call-map.md` and `design-benchmark-v5.md`
- Per-token census loop for all 8 `_F25` tokens + FILM_F1/F5/F6 (staged
  and built, lines + occurrences); unique-token census via
  `grep -rho "[A-Z][A-Z0-9_]*_F25" | sort | uniq -c`
- Existence checks for all 11 new-pointer targets in the built tree;
  `grep -n git-workflow` in built conventional-commit-review
- `grep -rn "liquid-glass-design"` over the whole plugin root
  (excl. node_modules/.git)
- `grep -rn "six dimensions|seven dimensions"` over staged sources;
  D19 lead-sentence count in staged orchestrate
- `grep -rn "step-2 reviewer"` and `"three-part|reasoning format"`
  over staged + built
- `grep -rn "80 searchable"` / `"89 searchable styles"` over staged
  and built; `sed` spot-reads of built ui-ux-pro-max :3/:8
- Full reads: staged orchestrate SKILL.md (389 lines, in full),
  grill-me (52), hackathon-scope (155), feature-expansion (213),
  polish-pass (127), design-benchmark-v5.md (178), fix25.py (298);
  spot-reads: Taste:395–434, dispatch-prompt:20–30, built
  browser-qa:83/:115, built prp-commit:59, built
  hooks/session-start.js:79–81, built ck SKILL.md:157, built
  motion-foundations:409/:435, built orch-build-mvp:70–85
- Banned-term greps (staged 18 hits, built 0) with per-file
  attribution; DEMOGATE token census (staged + built)
- fix25.py anchor provenance: each of the 14 anchors checked in its
  source — `/tmp/ecc-dev-install/.cursor/{hooks/session-start.js,
  skills/ck/SKILL.md, commands/prp-commit.md}`,
  `/tmp/uipro/.claude/skills/ui-ux-pro-max/SKILL.md:8`,
  `build.sh:586` (replace_desc_line), `build.sh:22209,22686,22691,
  22697` (orch-* UI-change rules), `build.sh:24004`
  (MEMORABLE-BQA-01); `fix25/fix25-patch-log.md` re-read (14
  changes, 0 errors)
- Call-map header + uncalled/second-order summaries + `ck` row re-read

## Verdict

**SWEEP #33: NOT CLEAN — 0 blocking, 2 minor.**

The fingerprint/diff, anchor census, staged-vs-built identity,
pointer resolution, fix25.py anchor provenance, /demo gates,
deferred-six standing, banned terms, Grok pins, counts, and the
weaving-coherence pass for §1, §2, §4(a), §4(b), §4(d), §4(e), §4(f),
THE CORE, C2/C3, and the six/seven convention all pass. The two
minor findings are both one-line fixes in staged sources: (1) the
REASON_F25 paragraph's "checked by the step-2 reviewer" claim has no
backing reviewer instruction (orchestrate:149); (2) the scope-traps
"Edge case obsession" row prescribes "Demo doesn't enter X" without
deferring to the TECHDEPTH_F25 cut-recording rule in the same file
(hackathon-scope). No blocking finding: no orphan anchor, no dangling
reference, no bypassed step, no contradiction with THE CORE, "more,
not bolder", the frozen D19 texts, or the C2/C3 scope splits.
