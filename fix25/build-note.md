# Fix #25, Phase 3a — build note (build worker)

Build run 2026-11-13 ~01:40–01:50 CT. Two builds were run: run 1
(log `fix25/build-log-run1.txt`) completed clean; run 2 was a re-run
after the call-map regeneration so the built tree carries the
post-rebuild map (log `fix25/build-log.txt`). Both runs identical on
every reported number. No re-run-once failure pattern occurred —
neither run hit a broken anchor. `fix11/fix11-stage.py` never run.
No skill, verifier, or staged source was edited by the build worker;
the only staged write was the generator's own output
(`new-skills/orchestrate/references/call-map.md` +
`fix25/callmap/call-map-data.json`), which is the generator's
sanctioned function.

## Build state (final, run 2)

- `build.sh`: **24,079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae** —
  unchanged by the build (build does not modify `build.sh`).
- Diff vs `build.sh.before-fix23`: **+305/−0** (additions only).
  Baseline pre-fix25 was 24,070 / b0b2645a…; worker C's +9-line
  fix25.py invocation accounts for +9 of the +305.
- fix16 (from `fix25/build-log.txt`): **ERRORS: 0, NOTES: 38,
  CHANGES: 649, REMOVALS: 88.** JS syntax failures 0, JSON failures 0,
  "TOTAL BANNED-TERM HITS: 0".
- fix25 patch (`fix25/fix25.py`): **14 change(s)**, exit 0, "fix25: OK".
- Counts (build log + STEP 5): skills **166**, agents **72**, rules
  **123**, commands **87**, hooks **15**; plugin.json hackathon-ecc
  1.0.0. Build exit code 0 both runs.
- Banned terms in the built tree (`hackathon-ecc/`, excl.
  node_modules, case-insensitive
  claude|codex|anthropic|opus|sonnet|haiku|composer-2.5): **0**.
  Grok pins only: `grok-4.7-high` ×54,
  `cursor-grok-4.6-high-fast` ×103, bare `grok-4.6-high-fast` ×0.

## Placement checklist (all read from the built tree, run 2)

- **Call map**: `skills/orchestrate/references/call-map.md` present;
  counts table 166/72/123/87/15/64; uncalled summary "52 elements"
  (`:40`); staged copy byte-identical to built copy (`diff` clean).
- **Benchmark**: `skills/orchestrate/references/design-benchmark-v5.md`
  present (11,751 B).
- **Template fonts**: `skills/pitch-deck-video/template/public/fonts/`
  holds exactly 3 files — `HankenGrotesk.woff2` (34,704 B),
  `InstrumentSerif.woff2` (21,032 B), `JetBrainsMono.woff2`
  (30,376 B). `template/src/fonts.ts` imports `loadFont` from
  `@remotion/fonts` (`:22`) + `staticFile` from `remotion` (`:23`),
  `loadFont` ×5, no `@remotion/google-fonts` import.
  `template/package.json` has `"@remotion/fonts": "4.0.526"` and no
  `@remotion/google-fonts`.
- **S1**: `skills/ui-ux-pro-max/SKILL.md:3` (frontmatter) and `:8`
  both read "89 searchable styles (51 active)"; "80 searchable"
  occurrences in the file: 0. Staged + built
  `design-inventory.md` both carry "89 searchable styles" ×1.
- **ck wire**: `hooks/session-start.js:10` requires `child_process`
  (`spawnSync`); `:79` builds the path to
  `skills/ck/hooks/session-start.mjs`; `:81` spawns it
  (`spawnSync(process.execPath, [ckHook], …)`). `skills/ck/SKILL.md:157`
  carries the "already wired" note.
- **Orchestrate tokens** (`skills/orchestrate/SKILL.md`):
  `RECIPES_F25` ×1, `TESTCOV_F25` ×1, `BENCHMARK_V5_F25` ×3,
  `TECHDEPTH_F25` ×3, `ADAPT_F25` ×1, `REASON_F25` ×3.
  `PLATFORM_F25` ×0 in orchestrate — expected: it lives in
  `skills/grill-me/SKILL.md:33` and
  `skills/hackathon-scope/SKILL.md:49` (worker B's homes).
- **Inventory close**: `INVENTORY_F23` ×1 in each of
  `skills/orch-{add-feature,change-feature,fix-defect,refine-code,
  build-mvp,pipeline}/SKILL.md`.
- **browser-qa benchmark line**: `skills/browser-qa/SKILL.md:83`
  ("Beat-v5 benchmark verdict … BENCHMARK_V5_F25") and `:115`
  (output-format checklist line).
- **prp-commit Phase 3**: `commands/prp-commit.md:59` drafts the
  message with `conventional-commit-review` and has
  `ecc-commit-reviewer` check it.

## Call-map regeneration (post-rebuild)

`python3 fix25/callmap/generate_call_map.py` — **exit 0**, counts
assert 166/72/123/87/15/64, corpus 1,710 files scanned.

- **Uncalled: 52** (24 skills, 21 agents, 7 commands, 0 rules,
  0 hooks, 0 triggers) — exactly worker B's post-rebuild
  expectation (53 → 52).
- **Second-order orphans: 13** (8 skills, 4 agents, 1 command
  `/python-review`) — unchanged from worker B's pre-rebuild map.
- The single element that changed vs the pre-rebuild map is **`ck`**:
  now called, invoker `hooks/session-start.js [strong]`, flow
  "always-on (Cursor event)" (map `:87`). All other diffs vs the
  pre-rebuild map are the build-time wires gaining their second
  invokers: `conventional-commit-review` +
  `ecc-commit-reviewer` gain `commands/prp-commit.md [strong]`;
  `orchestrate` gains `browser-qa/SKILL.md [strong]`;
  `tdd-workflow` gains `orchestrate/SKILL.md [strong]`
  (TESTCOV_F25); the 8 epic/`/prune` commands gain
  `orchestrate/SKILL.md [strong]` (RECIPES_F25).
- Uncalled skills (24): agents-md-generator, bengali-nlp,
  brownfield-retrospective, context-budget, dev-team, django-celery,
  generating-python-installer, i18n-sync, investor-materials,
  investor-outreach, kotlin-exposed-patterns, kotlin-ktor-patterns,
  laravel-plugin-discovery, laravel-verification,
  living-docs-governance, mybatis-patterns, quarkus-verification,
  repo-scan, rules-distill, springboot-verification, story-lifecycle,
  tinystruct-patterns, ui-to-vue, windows-desktop-e2e.
  Uncalled agents (21) and commands (7: astra-review,
  fastapi-review, gradle-build, issue-review, learn-eval,
  marketing-campaign, pm2) match worker A's dormant list minus the
  wired items.

## Caveats / owed (not failures of this build)

1. **`@remotion/google-fonts` string still appears 2× in the built
   tree** (excl. node_modules) — both are prose mentions, not code:
   - `skills/pitch-deck-video/template/src/fonts.ts:2` — worker D's
     intentional header comment explaining the old loader.
   - `skills/mobile-ship/references/launch-marketing.md:15` —
     pre-existing staged text (`round2-skills/mobile-ship/`,
     untouched by fix #25): "Fonts: Google Fonts under the OFL,
     via `@remotion/google-fonts`."
   Zero imports, zero package.json dependencies. The task's "must be
   0" criterion is therefore met for code/deps but not for raw
   string hits; verify25/audit to decide whether prose mentions
   count. Not edited here (build worker does not edit sources).
2. **A stale binary match exists outside the built tree**: a
   `grep -r` over the plugin root (not `hackathon-ecc/`) hits
   `audit-scripts/__pycache__/gen_audit8_patches.cpython-312.pyc`.
   It is not in the shipped plugin and was not investigated further.
3. **Two builds, one log overwritten**: run 1's log is preserved at
   `fix25/build-log-run1.txt`; `fix25/build-log.txt` is run 2's log.
   Both runs agree on every number above.
4. `/tmp` was 1% used before the build; no test copies were made
   there. Upstream clones untouched.
5. NOT run (per task): audit, sweep, dry-run, verify25 — later
   workers own those. Post-rebuild verifier tails (verify23 → 196/212,
   verify24 → 101/105 per worker C's prediction) are for verify25 to
   measure, not claimed here.
