# Fix #34 SPEC — port the factory variant's rounds 10–13 content into the regular plugin (minus the drone machinery)

Approved by Anish Nov 19, 2026 (baseline save + port decision). One bounded
job on top of fix33 (d22d9f4), then stop. The regular build's output tree
(`hackathon-ecc/`) was damaged by the factory round-12 incident (partial
upstream-shaped tree, 155 skills, no README/manifests); building fix #34
from the intact staged sources regenerates it — that regeneration is the
repair. The factory tree (`factory-cursor/` at c85e549) is READ-ONLY input.

## What transfers

1. **motion-principles skill** + weaving (Taste consult rule, gsap
   why-pointer, browser-qa MOTION-QA six-criterion verdict, inventory).
2. **threeui skill** + inventory entry (catalog + install guide only, MIT,
   free Community edition only, `@designcodeio/threeui`, no vendored source).
3. **prebuild-research skill + the research phase**: orchestrate step 1.5
   (after scope, before expansion), hackathon-mode's sequence names it,
   feature-expansion Phase 0 reads the brief first and records taken/dropped
   per idea; caps ≤4 searches + ≤4 fetches, brief `docs/research-brief.md`
   ≤ ~600 tokens, primary sources only, per-line sources.
4. **The design contract**: Taste step 4a issues `docs/design-contract.md`
   (Hosting / Palette tokens / Type scale / Spacing scale / Motion specs
   citing motion-principles / Components with inventory citations / States /
   Deviations); literal implementation; deviations recorded with D19
   reasons; restatement gate in the regular flow; browser-qa CONTRACT-QA.
5. **Hosting**: the contract's Hosting line (Vercel/Netlify, static-friendly,
   SPA fallback ships with the build, design wins conflicts recorded as
   Deviations); deploy-fast gains the hosting section. The Netlify PRICING
   row stays byte-untouched (its touch-up is dated Dec 4, 2026).
6. **code-mode framework, minus dispatch**: skill + helper library excluding
   `cm_dispatch`; script-first rule + review-before-run gate + 500 E3 cap
   applied to the regular orchestrator's own mechanical work. The honesty
   boundary (the pattern, not Anthropic's Code Mode feature) stays.
7. **Full-weave end state for the regular skill set**: enumerations complete
   (DESIGNPKG-AUTO names the new skills), rule-ID integrity for the ported
   IDs, cross-references both ways (research ↔ code-mode; contract ↔
   research brief; expansion ↔ research + inventory), call map / trigger
   coverage per regular precedent.

## What does NOT transfer (factory-only)

drone-reasoning / drone-coding agents + OpenRouter pins; openrouter-drones
skill; orchestrator-briefing + ALL dispatch machinery (brief gate, per-slice
context, scripted CLI dispatch, drone return-cap rules as drone rules);
`cm_dispatch`; factory census locks tied to drone/briefing files; the
factory's fast-tier removal (regular executes on Grok 4.6 High Fast by
design). References to excluded machinery inside ported files are adapted
out and recorded (MANIFEST port log).

## Decisions

- **D34-1 — Rule-ID renumbering.** The regular tree numbers rule IDs by fix
  (`MODELSEL_F33`, `NO-GUESSING_F29`, `INVENTORY_F23`, `DESIGNPKG-AUTO_F27`).
  Factory IDs are renumbered, never imported: MOTIONPRINCIPLES_F170→
  MOTIONPRINCIPLES_F34; THREEUI_F171→THREEUI_F34; MOTION-QA_F172→
  MOTION-QA_F34; DESIGNCONTRACT_F175→DESIGNCONTRACT_F34; CONTRACT-QA_F176→
  CONTRACT-QA_F34; RESEARCHBRIEF_F177→RESEARCHBRIEF_F34; HOSTING_F178→
  HOSTING_F34; CODEMODE_F181→CODEMODE_F34; SCRIPT-FIRST_F182→
  SCRIPT-FIRST_F34; SCRIPT-GATE_F183→SCRIPT-GATE_F34. "Factory round N"
  attributions become "fix #34".
- **D34-2 — code-mode applicability.** The factory skill's CLI-drone leg
  does not exist here: script-first applies to the orchestrator's own
  mechanical work, full stop (§5 rewritten). The `cm_dispatch` helper, the
  §1 table row, the §2 fan-out bullet shape, gate item 4's CLI approval,
  and worked shape B are removed; §6 keeps the census shape. The 500 E3
  cap rationale is kept with the drone comparison reworded to a generic
  full-work-return comparison. PARALLEL-CALLS_F154 (factory-only) is
  replaced by the regular batching discipline stated in prose.
- **D34-3 — prebuild-research precedent + CAPTIVATION.** The no-trigger-key
  precedent cited is the regular tree's own (fix #31 design skills:
  flow/inventory-invoked), not orchestrator-briefing. CAPTIVATION_F32 does
  not exist in the regular tree; its two cites become the anti-derivative
  rule named in prose (the rule itself is regular text).
- **D34-4 — Inventory sections.** Regular inventory has §1–§12 + the closing
  AMBITION section and NO §0 layer map. The port adds §13 (Motion
  Principles, ThreeUI — with the factory §0 treatment carried as the rows'
  bolded Layer role lines), §14 (Pre-build Research, the Design Contract),
  §15 (code-mode execution entry). The factory's §13 MotionSites section is
  factory lineage and is NOT ported. Ported skills' inventory cites are
  repointed (§14→§13, §15→§14).
- **D34-5 — DESIGNPKG-AUTO enumeration position.** The new names are
  inserted after `motionsites-web-builder`, NOT appended after
  `hairline-adopt` as the factory did: appending pushes `hairline-adopt`
  outside fix32's lead-scan 60-char attribution span for the control line
  "the design-lead deciding which leads" and fails the build gate
  (measured: build run 1, fix32 2 errors; probe-verified the enumeration
  insertion alone trips it, the repositioned insertion + glosses scan
  clean). The enumeration is a set, not an order; membership is what the
  weave requires. Applied byte-identically in orchestrate +
  hackathon-mode (the D33-2 shared-block rule).
- **D34-6 — Taste palette-first line.** Edited surgically (bare names into
  the package list). The factory line's role glosses are NOT imported:
  its "`ui-ux-pro-max` — general design intelligence" gloss contradicts
  fix #32's lookup-only demotion (regular rule wins), and the factory
  line's rewritten citation tail (with its Kitchen sentence) does not
  exist in the regular line's structure.
- **D34-7 — Restatement gate placement.** The phrase lives in factory
  Taste step 4a + factory orchestrate step 3 + step 5a. Regular port:
  Taste step 4a (the contract paragraph), orchestrate step 3 (the gate
  paragraph before the inventory paragraph, factory order), step 5a
  (static checks). Factory's step-3 brief text is drone-flavored
  (BRIEF-POINTER_F32) and is not ported. "Before dispatch" becomes
  "before the slice builds" — the regular flow's executing agent
  restates in its plan; a mismatch stops at the plan/brief.
- **D34-8 — Trigger coverage.** coverage.skills 72 → 76, withTriggers
  stays 48, no new trigger keys (fix #31 precedent for design skills;
  prebuild-research and code-mode are flow-invoked by name — recorded in
  the skills themselves and inventory §14/§15).
- **D34-9 — browser-qa verdicts are build-time patches.** browser-qa is
  upstream-derived in the regular tree; MOTION-QA + CONTRACT-QA are
  applied by fix34.py at build time (the fix #27/#31 pattern), anchored
  on the Beat-v5 dimension line + report row (both verified present
  exactly once in the regular built file). CONTRACT-QA's anchors chain
  on MOTION-QA's inserted text, so the motion patch runs first.
- **D34-10 — README.** Four count lines 72 → 76 (the fix #31 shapes); the
  Hackathon workflow bullet names `prebuild-research` after
  `hackathon-scope` (the factory round-11 placement); a fix #34
  provenance note goes before the fix #31 note. The factory's round-12
  code-mode README bullet edit is NOT ported: its anchor text ("plus
  Playwright MCP for browser QA") does not exist in the regular README —
  code-mode is named in the provenance note instead.
- **D34-11 — Call map.** Regenerated after the build with
  `fix28/callmap/generate_call_map.py` (EXPECTED skills 72 → 76 in the
  scratch-repo copy), then rebuilt so the staged map flows into the
  built tree (the fix #32 sequence; closes the fix34 analog of
  OWED-31-3 by construction). fix34.py records this as OWED-34-1;
  verify34.py asserts the regenerated map.
- **D34-12 — Build target discipline.** Builds run in fix34/fakehome34
  (fake HOME on real disk, fix33 pattern) with PLUGIN_DIR =
  fakehome34/workspace/hackathon-plugin/hackathon-ecc, logged in every
  build log. Sync-back = built tree + fix34/fix34-patch-log.md into
  fix34/scratch-repo, then the built tree into the canonical
  `~/workspace/hackathon-plugin/hackathon-ecc/` (the repair). The
  factory tree is never a build target and is never written.
  fix11/fix11-stage.py is never run.

## Counts

Before (fix33): skills 72, agents 45, rules 48, commands 55, hooks 15,
trigger keys 48 (coverage 72/48).
After (fix #34): skills 76 (+motion-principles, threeui, prebuild-research,
code-mode), agents 45, rules 48, commands 55, hooks 15, trigger keys 48
(coverage 76/48).

## Evidence basis for code-mode (the factory's R85–R88, restated)

Anthropic's Code Mode docs + code-execution-with-MCP + programmatic tool
calling; Cloudflare's Code Mode posts. All vendor savings figures are
vendor-reported and none are adopted as plugin claims; the ported skill
carries this boundary in its header note and Files list, pointing here.
