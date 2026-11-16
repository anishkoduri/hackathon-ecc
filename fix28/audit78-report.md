# Audit #78 — Fix #28 (round 1)

**Verdict: AUDIT #78: NOT PASS** — 0 blocking, 1 minor.

The built tree itself is correct on every item in scope: manifests are
referentially intact, all 84 paths exist, the dead-script closure spot-check
holds, both build fixes are correct in code, weaving is intact, and the
regenerated call map is consistent. The single minor is a durable-record
defect: SPEC §2(a) item 5 prescribes the opposite of the shipped
`dependencies` fix, and following it would crash every profile resolve.
Fixing it is a one-paragraph SPEC correction; no tree change is needed.

Scope audited: (a) install-manifest prune coherence, (b) dead-script
liveness spot-check + deliberate keeps, (c) the two build fixes,
(d) weaving coherence, (e) call-map regeneration quality. All checks were
run against the built tree at `hackathon-ecc/` (build run 5) by reading the
actual files and running independent greps / JSON checks / a live
`resolveInstallPlan` run via `verify28.py` (re-run by this auditor:
**106/106 checks pass**, exit 0). No file was edited; no build was run.

## BLOCKING findings

None. (Numbered 78-Ax: none issued.)

## MINOR findings

### 78-B1 — SPEC §2(a) item 5 prescribes deleting the `dependencies` key; the shipped fix keeps it as `[]`, and the SPEC text would crash every profile if followed

- `fix28/SPEC.md` §2(a) item 5: *"delete the `"dependencies":
  ["skill-unified-memory"]` field entirely (do not leave `"dependencies":
  []` — the Audit #6 convention pops the field when empty). Leaving it
  breaks ALL 7 profiles at install time (`resolveModule` throws `Unknown
  install module` — report §5d failure mode 2)."*
- Shipped code, `fix28/fix28.py` §2a (and identically in
  `fix28/fix28.py.template:238-243`): `_wq["dependencies"] = []`, with the
  comment *"Empty the list, do NOT delete the key: install-manifests.js
  resolveModule iterates module.dependencies unconditionally, so a missing
  key crashes every profile resolve (verify28 run 1 caught this: TypeError,
  module.dependencies is not iterable)."*
- Ground truth in the built tree, `hackathon-ecc/scripts/lib/install-manifests.js:611`:
  `for (const dependencyId of module.dependencies) {` — unconditional
  iteration inside `resolveModule`, repeated at `:636` in
  `selectResolvedModule` (`for (const dependencyId of
  manifests.modulesById.get(moduleId).dependencies)`). A missing key throws
  `TypeError: module.dependencies is not iterable` for every profile that
  resolves `workflow-quality`, i.e. all 7. (Only `dedupeStrings` at `:112-113`
  and the `dependencyCount` summary at `:308` tolerate a missing key.)
- The built tree is correct as shipped: `workflow-quality.dependencies == []`
  (verified in `manifests/install-modules.json`), and `resolveInstallPlan`
  succeeds for all 7 profiles plus the 55-component set (verify28 check 10f,
  re-run by this auditor). The defect is in the durable record only: the
  SPEC was never updated after run 1 discovered the crash, so the SPEC — the
  document a future implementer or auditor would follow — still instructs
  the breaking edit, and misattributes the failure mode (the throw it warns
  about is for a *left-over* dependency value, not for an empty list).
- Why it matters: a future rebuild or fix that re-derives the manifest edit
  from SPEC §2(a) instead of from `fix28.py` reintroduces a crash of all 7
  profiles. Fix: correct SPEC §2(a) item 5 to match the shipped `[]` fix
  and cite `install-manifests.js:611/:636`.

## Notes / observations (checked and cleared)

### (a) Install-manifest prune coherence — CLEARED
- `install-modules.json`: 14 modules / 84 paths; `install-components.json`:
  55 components; profiles `research` 7 / `full` 14 (others unchanged:
  minimal 5, opencode 3, core 6, developer 10, security 7). All match SPEC §2.
- Referential integrity verified independently (not just verify28): every
  profile module id and every component module id exists in
  `install-modules.json` (zero bad refs); every `dependencies` /
  `optionalDependencies` entry names an existing module (zero bad refs);
  **all 84 module paths exist on disk** (zero missing) — this exceeds the
  20-path spot-check, and includes every path of `workflow-quality` (14),
  `hackathon` (21), and `framework-language` (21), each matching the kept
  lists in `fix28/analysis/install-manifests.md` §1b/§1e/§1i exactly.
- Every module has a `dependencies` key (all 14); `workflow-quality` is
  `[]`, all others are their surviving lists — no module is missing the key
  that `resolveModule` iterates unconditionally.
- Deleted modules leave no dangling reference: `grep -rn` over the whole
  built tree (excl. `node_modules`) returns **0 hits** for
  `skill-unified-memory`, `business-content`, `skill:unified-memory`, and
  `capability:content`.
- The 22 kept-but-misleading components are correctly described: all 18
  dead language/framework components carry the exact note *"(Guidance for
  this language/framework was removed in fix #27; resolves to the shared
  framework-language module.)"*; the 4 dead single-skill components
  (`skill:continuous-learning`, `skill:windows-desktop-e2e`,
  `skill:coding-standards`, `skill:vue-patterns`) carry *"(Removed in fix
  #27; resolves to the shared … module.)"*; `lang:python` reads *"Python
  engineering guidance…"* (Django dropped). A sweep of all 55 component
  descriptions for cut-skill names (`unified-memory`,
  `continuous-learning`, `vue-patterns`, `coding-standards`,
  `windows-desktop-e2e`, `accessibility`, `brainstorming`,
  `codebase-memory`, `dispatching-parallel-agents`, `agents-md-generator`,
  `opensource-pipeline`, `security-scan`, `mcp-dependency-review`) found
  zero remaining claims to install a cut skill — the only occurrences are
  inside the "(Removed in fix #27…)" notes themselves.
- `verify28-run3.log` line "profile research OK (8 modules selected)" is
  not a discrepancy: `research` lists 7 modules; the 8th selected module is
  the dependency closure (`shared-script-utils`, via `commands-core` /
  `platform-configs`).

### (b) Dead-script liveness — CLEARED (10 spot-checks across 6 clusters)
All 10 sampled CUT scripts are absent from the built tree and have zero live
references (precise path-form greps, not bare stems):
- hooks dispatcher subtree: `scripts/hooks/posttooluse-dispatcher.js` (1 hit
  only: `commands/quality-gate.md:44`, prose explicitly stating the dispatcher
  *"is not referenced by `hooks/hooks.json` or anything else in the plugin,
  so it never runs"* — not a dispatch), `scripts/hooks/bash-hook-dispatcher.js`
  (0 hits), `scripts/hooks/observe-runner.js` (0 hits).
- `scripts/lib/control-pane/server.js` — 0 hits for `control-pane` anywhere.
- `scripts/lib/eval-harness/gate.js` — 0 hits for `eval-harness/gate`; the 3
  `eval-harness` hits in the tree are a schema description
  (`schemas/capsule-envelope.schema.json:5`) and `pi-core.json` exclude-reason
  logs (`:116`, `:132`) — not references to the cut files.
- `scripts/lib/plan-canvas/server.js` — 0 hits for `plan-canvas/server`; the
  2 `plan-canvas` hits are `pi-core.json` exclude-reason logs (`:182`, `:311`).
- `scripts/lib/agent-proximity/index.js` — 0 hits for `agent-proximity`.
- `scripts/lib/gateguard-state.js`, `scripts/lib/memory-vault.js`,
  `scripts/lib/harness-adapter-compliance.js` — 0 hits each.
- Deliberate keeps verified, reasons accurate:
  - `scripts/lib/orchestration-session.js` + `scripts/lib/tmux-worktree-orchestrator.js`
    both present; each file's **only** reference in the tree is
    `manifests/install-modules.json:220-221`, as the entire `paths` of the
    `orchestration` module. The module survives, `capability:orchestration`
    still maps to it, and the `developer` profile still lists it — cutting
    either file would empty the module exactly as SPEC §5 states. The keep
    reason is accurate.
  - `scripts/ci/validate-skills.js` present; listed in `commands-core`
    paths (`install-modules.json:43`) and named in `README.md:69` as a
    shipped script. The keep reason (documented CI/dev entry point) is
    accurate.
  - `hooks/hooks.json` still registers 15 events; `hooks/adapter.js` present.

### (c) The two build fixes — CLEARED
1. `build.sh` MS_SRC follows MS_DIR (`build.sh:25-30`):
   `MS_SRC="${MS_DIR:-/tmp/hack-skills}/skills"`. Correct and
   backward-compatible: with no env redirect it evaluates to the old
   hardcoded `/tmp/hack-skills/skills`; with `MS_DIR` redirected it follows
   the redirect, fixing the run-1 `"cp: cannot stat ''"` death. The later
   `MS_DIR="${MS_DIR:-/tmp/hack-skills}"` at `:278` uses the same default,
   so the two assignments cannot diverge. No other hardcoded
   `/tmp/hack-skills/skills` remains in `build.sh` (remaining
   `/tmp/hack-skills` hits are the comment, the fix comment, and the two
   default expansions).
2. `fix28.py` §2a `workflow-quality.dependencies = []` instead of deleting
   the key: correct, per `install-manifests.js:611` and `:636` (quoted under
   78-B1). Confirmed no other module is missing its `dependencies` key (all
   14 have it), so no other module can hit the same crash.
   - Template parity: `diff fix28/fix28.py fix28/fix28.py.template` shows
     differences **only** on the four list-assignment lines, where the
     template carries the `__CUT_RULES__` / `__KEPT_RULES__` /
     `__DEAD_SCRIPTS__` / `__MANIFEST_DEAD__` placeholders (the expected
     template pattern). All code — including the `dependencies = []` fix at
     template `:238-243` — is identical. Note: the MS_SRC fix lives in
     `build.sh`, which has no template counterpart, so "both fixes in the
     template" applies to the `fix28.py` fix only; `build.sh` is its own
     source of truth and carries the MS_SRC fix directly.

### (d) Weaving coherence — CLEARED
- Design-package auto-routing: `DESIGNPKG-AUTO_F27` present in kept files
  (`rules/hackathon-mode.mdc:44`, `skills/orchestrate/SKILL.md:35,65,92`).
- Palette-first: `PALETTE-FIRST_F27` present (3 hits, kept files).
- D19 reasoned decisions: `D19` occurs 339 times across the built tree.
- Orchestrator-leads-every-prompt: `ALWAYSLEAD_F27` present (6 hits:
  `rules/hackathon-mode.mdc:12,48`, `skills/orchestrate/SKILL.md:14,59,61,120`).
  No `_F27` token was removed by the cut (all 20 asserted by verify28
  check 7, re-run here).
- Kept arkts rules still dispatch from the kept agent:
  `agents/ecc-harmonyos-app-resolver.md:181` — *"refer to the
  `rules/arkts-*.mdc` rule files"* — intact, and all 5 `arkts-*.mdc` files
  exist with their globs.
- Kept python rules still match `**/*.py`: `python-coding-style`,
  `python-hooks`, `python-patterns`, `python-security`, `python-testing`
  all carry `globs: ["**/*.py", "**/*.pyi"]`; `python-fastapi.mdc` carries
  `**/app/**/*.py`, `**/fastapi/**/*.py`, `**/*_api.py`. Dispatch paths
  intact.
- No severed dispatch path for any kept element was found. One generator
  limitation, not a severed path: the call map lists the arkts rows with
  only their self `[struct-rule-globs]` invoker and does not attribute the
  agent's family-glob `rules/arkts-*.mdc` dispatch (`:181`) to the
  individual arkts rows — the dispatch itself exists and is live; the map
  just cannot expand a glob into per-file invokers.

### (e) Call-map regeneration quality — CLEARED
- `skills/orchestrate/references/call-map.md`: counts table 67/45/48/55/15/49,
  `"## Rules (48)"` present, **zero** occurrences of `123` anywhere in the
  file, header marked fix #28.
- Sidecar `fix28/callmap/call-map-data.json`: `counts` exactly
  `{skills: 67, agents: 45, rules: 48, commands: 55, hooks: 15, triggers: 49}`,
  `uncalled.rules == []`, 48 rule elements — matches the map.
- B6 note reword (call-map.md:38) is accurate in past tense: it states the
  four loader files *"were removed as dead weight in fix #28"* — all four
  are confirmed gone from the built tree:
  `scripts/lib/context-pack-registry.js`, `scripts/lib/context-selection.js`,
  `scripts/hooks/context-routing-index.js`,
  `scripts/hooks/context-prompt-suggestions.js` (all four were also in the
  `DEAD_SCRIPTS` list). The only remaining mention of the loader names is
  the B6 note itself.
- 5 kept-rule rows spot-checked against the actual files; every listed
  invoker exists and mentions the rule:
  - `arkts-patterns` — self `[struct-rule-globs]`; file exists, globs
    `**/*.ets`, `**/*.ts`; plus the agent dispatch above.
  - `common-agents` — `rules/common-code-review.mdc [strong]` mentions
    `common-agents` (1 hit).
  - `common-coding-style` — `rules/arkts-coding-style.mdc`,
    `rules/react-coding-style.mdc`, `rules/react-native-coding-style.mdc`,
    `rules/web-coding-style.mdc` each mention it (1 hit each).
  - `python-patterns` — `agents/ecc-python-reviewer.md:102`
    ("see skill: `python-patterns`"), `rules/python-coding-style.mdc:42`,
    `skills/python-patterns/SKILL.md` all mention it.
  - `react-patterns` — `agents/ecc-react-build-resolver.md`,
    `agents/ecc-react-reviewer.md:160-161`, `commands/react-build.md`,
    `skills/react-patterns/SKILL.md` all mention it.
- Generator hygiene: `fix28/callmap/generate_call_map.py` contains **0**
  occurrences of `"123"` and **0** of `"fix25"` — no stale reference that
  could corrupt a future regeneration.
- `fix28/fix28-patch-log.md`: `## Errors (0)`, 75 rules / 135 scripts
  accounted for, `_F28` tokens present.

## What was NOT checked (open items, none blocking)
- No live-browser or Cursor-session check was needed or performed; every
  item in scope was verifiable from the built tree on disk. The B6
  "documentation-only" disposition itself (fix #26) was out of scope per
  SPEC §7 and was taken as given; only the fix #28 reword's accuracy was
  checked.
- The §1(b) 7-file NEEDS-DECISION misfire call is outside this audit's
  assigned scope (a–e); no view is offered on it here.
