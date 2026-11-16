# Fix #28 SPEC — Cut all remaining bloat that provably does not affect the plugin

## §0 Origin

Anish, Nov 16, 2026, ~2:00 PM CST: "Cut all bloat that doesn't affect the
plugin and is just there."

Baseline: fix #27 tree, commit `b7d0f75` (67 skills / 45 agents / 123 rules /
55 commands / 15 hooks; 49 trigger keys; install manifests 16 modules /
184 paths / 57 components). Fix #27's MANIFEST §5 named the known bloat this
fix closes: (§5.1) the ~80 per-language rule files for cut languages
(OWED-11/M7); (§5.2) install-modules.json / install-components.json left
unpruned (M-new-4). This fix adds the third class the fix #27 work did not
cover: dead scripts under `scripts/` proven unreachable by a liveness
closure.

Evidence base (read before implementing): `fix28/analysis/rule-inventory.md`
(all 123 rules, per-file verdicts), `fix28/analysis/install-manifests.md`
(per-module/component/profile verdicts + the skill-unified-memory trace),
`fix28/analysis/dead-weight.md` (135 dead script files + findings F1/F2/F4).
Staged sources are the edit source for staged files; ECC/marketplace-origin
files are patched at build time by `fix28/fix28.py` (same pattern as
`fix27/fix27.py`), invoked by build.sh after fix27 and before STEP 5 Counts.
Never re-run `fix11/fix11-stage.py`. Never edit the built tree directly
outside fix28.py. build.sh is the source of truth.

Coordinator decision (recorded here so the audit can challenge it): the 7
NEEDS-DECISION rule files are CUT, not kept (§1(b)). Their only effect on
kept-stack files is injecting wrong-framework guidance (see §1(b)); cutting
them removes noise, not correct behavior. If the audit loop finds a genuine
quality loss in any of the 7, that file is restored and the manifest records
it.

## §1 Rules — 123 → 48 (75 files cut)

### §1(a) The cut (68 files, clean)

The 68 CUT files from `fix28/analysis/rule-inventory.md` §7. Every row meets
all three criteria: (a) zero live dispatches (literal-path, bare-name, and
family-glob greps all 0 hits outside call-map.md / build.sh / verify27.py),
(b) no kept skill/agent/command serves the language, (c) globs cannot match
kept-stack files (Next.js/React + TypeScript frontend, FastAPI/Python
backend, Expo/React Native mobile path).

| Family | CUT files |
|---|---|
| angular (3) | `angular-coding-style.mdc`, `angular-patterns.mdc`, `angular-security.mdc` |
| cpp (5) | `cpp-coding-style.mdc`, `cpp-hooks.mdc`, `cpp-patterns.mdc`, `cpp-security.mdc`, `cpp-testing.mdc` |
| csharp (5) | `csharp-coding-style.mdc`, `csharp-hooks.mdc`, `csharp-patterns.mdc`, `csharp-security.mdc`, `csharp-testing.mdc` |
| dart (4) | `dart-coding-style.mdc`, `dart-hooks.mdc`, `dart-patterns.mdc`, `dart-testing.mdc` |
| fsharp (5) | `fsharp-coding-style.mdc`, `fsharp-hooks.mdc`, `fsharp-patterns.mdc`, `fsharp-security.mdc`, `fsharp-testing.mdc` |
| golang (5) | `golang-coding-style.mdc`, `golang-hooks.mdc`, `golang-patterns.mdc`, `golang-security.mdc`, `golang-testing.mdc` |
| java (5) | `java-coding-style.mdc`, `java-hooks.mdc`, `java-patterns.mdc`, `java-security.mdc`, `java-testing.mdc` |
| kotlin (5) | `kotlin-coding-style.mdc`, `kotlin-hooks.mdc`, `kotlin-patterns.mdc`, `kotlin-security.mdc`, `kotlin-testing.mdc` |
| nuxt (2) | `nuxt-hooks.mdc`, `nuxt-security.mdc` |
| perl (5) | `perl-coding-style.mdc`, `perl-hooks.mdc`, `perl-patterns.mdc`, `perl-security.mdc`, `perl-testing.mdc` |
| php (5) | `php-coding-style.mdc`, `php-hooks.mdc`, `php-patterns.mdc`, `php-security.mdc`, `php-testing.mdc` |
| ruby (5) | `ruby-coding-style.mdc`, `ruby-hooks.mdc`, `ruby-patterns.mdc`, `ruby-security.mdc`, `ruby-testing.mdc` |
| rust (5) | `rust-coding-style.mdc`, `rust-hooks.mdc`, `rust-patterns.mdc`, `rust-security.mdc`, `rust-testing.mdc` |
| swift (5) | `swift-coding-style.mdc`, `swift-hooks.mdc`, `swift-patterns.mdc`, `swift-security.mdc`, `swift-testing.mdc` |
| vue (4) | `vue-coding-style.mdc`, `vue-patterns.mdc`, `vue-security.mdc`, `vue-testing.mdc` |

Machine-readable list: `fix28/analysis/cut-rules-list.txt` (75 lines
including §1(b)).

### §1(b) The 7 NEEDS-DECISION files — CUT on the misfire argument

`angular-hooks.mdc`, `angular-testing.mdc`, `dart-security.mdc`,
`nuxt-coding-style.mdc`, `nuxt-patterns.mdc`, `nuxt-testing.mdc`,
`vue-hooks.mdc`. None has a live dispatch or a kept-skill link. Each has a
glob that can match a kept-stack file:

- `angular-hooks.mdc` / `angular-testing.mdc`: `**/*.spec.ts`, `**/*.test.ts`
  match kept-stack Vitest/Jest test files.
- `dart-security.mdc`: `**/AndroidManifest.xml`, `**/Info.plist` occur in
  Expo prebuild output.
- `nuxt-coding-style.mdc` / `nuxt-patterns.mdc` / `nuxt-testing.mdc`:
  `**/pages/**` matches a Next.js Pages Router project.
- `vue-hooks.mdc`: `**/*.ts`, `**/*.tsx` match every TypeScript file in the
  kept Next.js frontend — the broadest collision.

Today each of these files loads wrong-framework guidance onto kept-stack
files (Angular TestBed rules on Vitest tests, Vue hooks rules on every TS
file, Nuxt page conventions on Next.js pages, Dart security rules on Expo
native files). No kept build has a file of the file's own framework, so the
guidance is never correct for the file it loads on. Cutting removes that
noise. **Correction (audit #77-A1):** the "removes no correct behavior"
claim was false for one file — `dart-security.mdc`'s Android/iOS manifest
sections (`android:exported`, intent-filter review, `FLAG_SECURE`,
`NSAppTransportSecurity`, usage descriptions, data-protection entitlement,
`network_security_config.xml`, request timeouts) have no equivalent in the
kept tree and did load on Expo prebuild `AndroidManifest.xml` /
`Info.plist` files. Per this section's own instruction, the genuine
kept-stack use is preserved, not by restoring the Flutter file (~80% of
it is wrong-framework noise) but by porting the framework-neutral bullets
into kept `rules/react-native-security.mdc`, including the two manifest
globs so the guidance loads on those files (`DARTSEC_F28`, fix28.py §5d).
The other 6 files are cleared by audit #77 with no genuine loss. The
lock-in ceiling does not move: no kept skill, agent, command, or rule
loses a dependency.

### §1(c) What stays — 48 rules

- **NEVER CUT (12 alwaysApply):** the 10 `common-*` files +
  `hackathon-mode.mdc` + `ponytail.mdc`. Correction to the task brief, which
  said 9: frontmatter verification shows 12 (`hackathon-mode.mdc:27` names
  9 and cites code-review separately; `ponytail.mdc` is the 12th, surviving
  on alwaysApply alone with zero textual dispatches).
- **KEEP (36):** python (6), typescript (5), react (5), react-native (8),
  arkts (5), web (7). Python stays on `**/*.py` glob match to the kept
  FastAPI backend despite zero literal dispatches. Arkts stays on the live
  family-glob dispatch from kept agent `ecc-harmonyos-app-resolver.md:181`
  (`rules/arkts-*.mdc`). Web stays on glob overlap (`**/*.tsx`, `**/*.css`,
  `**/*.html`).

### §1(d) Mechanism — build-time removal in fix28.py

Rules are ECC-origin (`build.sh:176` copies `$ECC_SRC/rules/.`, plus staged
`new-rules/ponytail.mdc` + `hackathon-mode.mdc` at :257–258, both KEPT), so
removal happens in fix28.py on the built tree, after fix27, before STEP 5
Counts — same pattern as fix27.py §1. Do NOT delete from build.sh STEP 2:
the STEP 3 patches assume the full tree. The 21 build.sh patch calls naming
CUT/NEEDS-DECISION rule files (§6 of the rule inventory) run at STEP 3,
before fix28.py deletes the files, so they still apply harmlessly; no
build.sh change is needed for them. (Precedent: fix #27's builds already
pass with dead ruby/swift patches targeting agents removed in fix #27.)
The `RULE_DIRS`/`RULE_FILES` rewriter (build.sh:416–442) is left alone: no
kept file references a CUT rule in old or new form, so it is a no-op for
these families; pruning it is cosmetic.

Side effect, recorded: cutting the 75 files also removes 29 of the 31
dangling OWED-11/M7 `See skill: <cut-skill>` pointers in verify27.py's
ALLOW_LIST. The 2 that stay are in KEEP file `react-patterns.mdc:194`
(reworded, §4(d)) and NEVER CUT file `hackathon-mode.mdc:37–38` (negative
prose, "deliberately NOT wired" — stays as-is).

## §2 Install manifests — 16 → 14 modules, 184 → 84 paths, 57 → 55 components

Per `fix28/analysis/install-manifests.md` §6. All edits are one atomic
change in fix28.py (deterministic JSON edits, exact lists from the report —
not a re-run of the Audit #6/#7 logic, which is recorded in the report §8
as the alternative encoding; deterministic edits are auditable and asserted
by verify28.py).

### §2(a) install-modules.json

1. `framework-language.paths`: delete the 51 dead paths (§1b of the
   report); keep the 21 listed there, in original order.
2. `database.paths`: delete the 7 dead paths; keep `["skills/postgres-patterns"]`.
3. **Delete the entire `skill-unified-memory` module object.**
4. `workflow-quality.paths`: delete the 29 dead paths; keep the 14 listed
   there, in original order.
5. `workflow-quality`: **empty the `"dependencies":
   ["skill-unified-memory"]` list to `[]` — do NOT delete the key.**
   `install-manifests.js` `resolveModule` (:611) and
   `selectResolvedModule` (:636) iterate `module.dependencies`
   unconditionally, so a missing key throws `TypeError:
   module.dependencies is not iterable` for all 7 profiles (caught by
   verify28 run 1). An empty list resolves cleanly. Leaving the
   *value* would break all 7 profiles (`resolveModule` throws `Unknown
   install module` — report §5d failure mode 2); the Audit #6
   convention of popping the field when empty does not apply here.
   (Corrected per audit #78-B1: this item originally prescribed
   deleting the field, which is the breaking edit.)
6. `workflow-quality.description`: replace the text naming the legacy
   continuous-learning v1 path and the unified-memory workflow with
   `"Evaluation, TDD, verification, compaction, learning, and memory skills."`
7. `security.paths`: delete `skills/mcp-dependency-review` and
   `skills/security-scan`; keep `["skills/security-review"]`.
8. **Delete the entire `business-content` module object.**
9. `agentic-patterns.paths`: delete `skills/opensource-pipeline`; keep the 7.
10. `hackathon.paths`: delete the 4 dead paths; keep the 21 listed there.
11. `hackathon.description`: drop "brainstorming, " from the skill list.
12. No change to `rules-core`, `agents-core`, `commands-core`,
    `hooks-runtime`, `platform-configs`, `research-apis`, `orchestration`,
    `shared-script-utils`. (`"version": 1` unchanged.)

### §2(b) install-components.json

1. **Delete the entire `skill:unified-memory` component object.**
2. **Delete the entire `capability:content` component object.**
3. No other component is deleted. The 4 dead single-skill components
   (`skill:continuous-learning`, `skill:windows-desktop-e2e`,
   `skill:coding-standards`, `skill:vue-patterns`) and the 18 dead
   language/framework components (`lang:go/java/cpp/c/kotlin/arkts/perl/
   ruby/rust/csharp/fsharp`, `framework:angular/vue/django/springboot/
   quarkus/rails/laravel`) are KEPT under build.sh's Audit #7
   any-module-survives rule, with description corrections (item 4 below).
   Deleting them would change selector behaviour (request → `Unknown
   install component` throw instead of installing the shared module) — a
   behaviour change, not bloat removal. Deletion stays a parent-callable
   stricter alternative; the exact edit is removing those component
   objects.
4. Description corrections for kept components (exact replacements in
   report §6b item 4): `skill:continuous-learning`, `lang:python`, the 18
   dead language/framework components (append the "(Guidance for this
   language/framework was removed in fix #27; ...)" note),
   `skill:windows-desktop-e2e`, `skill:coding-standards`,
   `skill:vue-patterns`.

### §2(c) install-profiles.json

1. `research.modules`: delete `"business-content"` (8 → 7). Description:
   drop "and content-oriented" (research-only wording).
2. `full.modules`: delete `"skill-unified-memory"` and `"business-content"`
   (16 → 14). Description stays accurate.
3. No change to `minimal`, `opencode`, `core`, `developer`, `security`.

### §2(d) pi-core.json — NO CHANGE

All 30 `skills.include` and 18 `commands.include` entries exist. The
`unified-memory` entry at :229 is an exclude-reason log, not a reference.
Do not touch the `exclude` map (it also lists 15 kept skills as reason
logs).

## §3 Dead scripts — 135 files (~1.24 MiB) + 1 config entry

Per `fix28/analysis/dead-weight.md` §1. Proved by a liveness closure over
the built tree (roots: the 15 `hooks.json` commands + every kept `.md` +
README; edges: require/import, `runExistingHook`, `node scripts/...`,
segmented `path.join` loads, `loadRuntimeModule`, bare-dir requires). Of
243 files under `scripts/` + `hooks/`, 101 reachable, 142 unreachable, 7
excluded → **135 CUT candidates totalling 1,301,859 bytes (58% of
`scripts/` by bytes)**. Machine-readable list:
`fix28/analysis/dead-scripts-list.txt` (135 lines, verified: all 135 exist
on disk in the fix #27 tree, total exactly 1,301,859 bytes).

- **Cluster A — `scripts/hooks/` (42 files, 384,784 B):** the unwired Claude
  Code PostToolUse/PreToolUse dispatcher subtree (their own headers say
  "not wired … it never runs"; `commands/quality-gate.md` confirms the
  posttooluse dispatcher never runs) + hookify runtime, observe-runner,
  mcp-health-check, plan-canvas hooks, governance/gateguard hooks.
- **Cluster B — `scripts/lib/` subsystems (60 files, 651,505 B):** whole
  dead directories — control-pane, plan-canvas, eval-harness,
  context-profile/*, agent-proximity, gateguard-* libs, session-adapters,
  skill-improvement, worktree-lifecycle.
- **Cluster C — `scripts/lib/` orphans (33 files, 265,570 B):** singletons
  with zero incoming edges (memory-vault, nasiko-release, powershell-
  destructive-command, session-bridge, skill-evolution/index.js barrel,
  terminal-welcome, etc.).
- Cut whole clusters: do not cut a single file from a cluster and leave its
  dead referrers — the closure proves every referrer of every CUT file is
  itself dead, so the whole set goes at once.
- **Config row:** `mcp.json:17-18` — the `codebase-memory-mcp` server entry
  for the CUT `codebase-memory` skill. Its only occurrence in the tree is
  itself; no kept skill/agent/command references the server; the binary is
  not installed by the plugin. Delete the key in fix28.py.

### §3(a) Mechanism — build-time removal in fix28.py

`build.sh:186/192/209` copies `scripts/`, `hooks/`, `mcp.json` wholesale
from ECC, so built-tree-only deletions would be undone by the next rebuild.
fix28.py (running after the copies, before STEP 5) deletes the 135 files +
the mcp.json key on every build — same pattern as fix27.py's skill
removals. No build.sh exclusion list is needed.

Ordering note (dead-weight §6.3, resolved): `build.sh:14591-14593` runs
`node --check` on `context-profile-interactive.js`, `harness-adapter-
compliance.js`, `llm-summary.js`. That block runs at line ~14592, BEFORE
the fix28.py invocation (~24090), so all three files still exist at check
time. The first and third are already absent from the final built tree
(removed under decision D12 by a later step) and fix #27's 8 builds passed
with this layout — the --check block tolerates it. fix28.py's removal of
`harness-adapter-compliance.js` happens after the checks. No build.sh
change.

## §4 Fixes (not cuts)

### §4(a) F1 — `commands/sessions.md:295` points at a removed script

> "…and the cost metrics emitted by `scripts/hooks/cost-tracker.js`."

`cost-tracker.js` does not exist (removed under decision D12; `hooks/stop.js`
had its cost-tracker block removed in the same decision). Correction to the
dead-weight report's suggested reword: it proposes re-pointing at
`scripts/hooks/post-bash-command-log.js`, but that file is itself in the §3
CUT set (unwired, never runs) — there is NO surviving cost-metrics
mechanism. Fix: **drop the clause** ("combine `/sessions info` and
`git diff --stat`"). sessions.md is a kept command file (ECC-origin), so
the fix is a build-time text patch in fix28.py.

### §4(b) F2 — live stop hook reads a CUT skill's config

`scripts/hooks/evaluate-session.js:55-77` loads
`skills/continuous-learning/config.json` — the skill dir was CUT in fix
#27, so the path can never exist. The read is guarded (falls back to
defaults), but every long session's stop then logs two orphan
`[ContinuousLearning]` lines for a learning system whose skills were
removed. Fix in fix28.py: delete the config-load block (defaults already
apply: `minSessionLength = 10`, `learnedSkillsPath =
getLearnedSkillsDir()`), delete the two misleading log lines ("Session has
N messages - evaluate for extractable patterns" / "Save learned skills
to: …"), and update the file header's purpose line (it no longer extracts
patterns). Do NOT cut `evaluate-session.js` itself — it is a live stop-hook
entry point invoked by `hooks/stop.js:22`.

### §4(c) F4 — README stale routing claim

`README.md:11` still lists "the chrome-devtools, playwright, and
codebase-memory MCP servers" while `README.md:28` says codebase-memory was
cut in fix #27. Fix: remove the `mcp.json` entry (§3) AND delete "and
codebase-memory" from README.md:11. README.md:28 is prose history ("was
cut") — KEEP.

### §4(d) `rules/react-patterns.mdc:194` — dangling CUT-skill pointer in a KEPT rule

> "For accessibility see `skills/accessibility/SKILL.md`."

`accessibility` is a CUT skill. Reword to `skills/frontend-a11y/SKILL.md`
(the fix #27 M-new-1 re-point pattern). react-patterns.mdc is KEEP, so
this is a build-time text patch in fix28.py, not a cut.

### §4(e) README count lines → 67 / 45 / 48 / 55

fix28.py updates the STEP 4 README count lines in the built tree (same
pattern as fix27.py §5): README.md:13 "67 skills, 45 agents, 123 rules,
and 55 commands in total (42 agents as-shipped + 3 staged orchestrate
agents; 121 rules as-shipped + 2 new rules — `hackathon-mode`,
`ponytail`; …)" → "67 skills, 45 agents, 48 rules, and 55 commands in
total (42 agents as-shipped + 3 staged orchestrate agents; 46 rules
as-shipped + 2 new rules — `hackathon-mode`, `ponytail`; …)". README.md:11's
"144 skills, 69 agents, 121 rules, 94 commands" is the stock-ECC figure —
NOT touched. The other count mentions ("67 skills widen the routing
surface", "56 MB and 67 skills", "67 skills, 45 agents, 55 commands")
are unchanged by this fix (skills/agents/commands do not move).

## §5 What is NOT cut (deliberate KEEPs, with reasons)

- **`scripts/lib/orchestration-session.js` + `scripts/lib/tmux-worktree-
  orchestrator.js` (25,784 B):** runtime-dead (zero incoming edges) BUT
  both are the entire `paths` of the `orchestration` module in
  install-modules.json. Cutting them empties the module → the module must
  be deleted → `developer` profile loses a module and the
  `capability:orchestration` component must be deleted. That changes the
  install surface (a profile loses a module) for ~26 KB. Deferred as a
  parent decision; recorded here, not silently kept.
- **`scripts/ci/validate-skills.js` (13,234 B):** zero runtime invokers,
  but a documented CI/dev entry point (README.md:67-68 names it; listed in
  install-modules.json `commands-core` paths). Dev-only, explicitly
  documented — not dead weight by the task's bar.
- **The 22 misleading install components (§2(b) item 3):** kept with
  description corrections; deletion changes selector behaviour.
- **`motionsites-web-builder` module membership:** the kept skill is in no
  module (reachable only via the synthetic `skill:motionsites-web-builder`
  component). Adding `"skills/motionsites-web-builder"` to
  `hackathon.paths` is an addition, not a prune — parent decision, not
  done here.
- **The 48 kept rules (§1(c)), all 67 skills, 45 agents, 55 commands, 15
  hooks, 49 trigger keys:** unchanged.
- **Prose-history mentions** ("was cut", "deliberately NOT wired",
  negative mentions): not cut candidates. **Duplicates:** all 37 md5-
  identical groups are KEEP — both copies are referenced (Taste icon/photo
  alias sets); dedup needs path rewrites, not a cut. **Type declarations**
  (4 `.d.ts` files): type surface of live modules, KEEP. **`.gitkeep`
  files (3, 0-byte):** directory placeholders, KEEP.
- **Fix dirs (fix10–fix27), build.sh backups, `audit-scripts/`,
  `LIVE_SMOKE_TEST.md`:** audit trail / dev-only, never shipped — not cut
  candidates (same logic as the hard rule).
- **build.sh `RULE_DIRS`/`RULE_FILES` rewriter:** left alone (§1(d)).

## §6 Verification criteria

- Audit #77 (or next number): ZERO blocking, ZERO minor. Standalone
  report file in `fix28/` (per the AGENTS.md record-keeping rule).
  Auditors must specifically hunt for LIVE dispatches to cut files — fix
  #27 audit #74 caught 14 live dispatches to removed skills; that is the
  failure mode to prevent. The audit must adjudicate the §1(b) 7-file
  misfire call file by file.
- Sweep #36 (or next number): CLEAN, weaving-coherence CLEAN for the
  whole tree. Standalone report file in `fix28/`.
- Dry-run #43 (or next number): PASS — Leg 1 fixtures, Leg 2 render
  re-run, Leg 3 /demo, Leg 4 Cursor-readiness, Leg 5 call-graph.
- verify28.py: checks for every placement, exit 0. Counts asserted:
  skills 67, agents 45, rules 48, commands 55, hooks 15, triggers 49;
  install modules 14 / paths 84 / components 55; profiles `research` 7 /
  `full` 14; the 75 CUT rule files absent + 48 kept present; the 135 dead
  script files absent; mcp.json has no `codebase-memory-mcp` key; README
  count lines 67/45/48/55; F1/F2/F4/react-patterns patches re-asserted;
  `resolveInstallPlan` succeeds for every profile (exercises the `Unknown
  install module` throw path directly); pi-core M-new-4 check re-run
  unchanged; no CUT skill name in any manifest `paths` array.
- Prior verifiers: re-run; verify27.py is expected to FAIL only on the
  codified tails (rules 123 → 48, README counts, the 29 orphaned
  ALLOW_LIST entries, manifest counts). Recorded as RETIRED/superseded by
  verify28.py, same precedent as fix #27 §4 (verify26/verify25 retired).
- Banned terms: 0 in the built tree (same list as fix #27). Grok pins
  only: `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- Anchor tokens: new `_F28` family (`CUTRULES_F28`, `MANIFEST28_F28`,
  `DEADSCRIPTS_F28`, `EVALSESS_F28`, `README48_F28`, `REACTA11Y_F28`,
  `NDMISFIRE_F28`, `ORCHKEEP_F28`) — census reconciles staged + built.
- Manifest: fix28/MANIFEST.md, with the disposition table, the anchor
  tokens, the open parent adjudications, and the dry-run caveat if any
  check is environment-limited.
- Builds use the fix #26 env-redirected invocation (TMPDIR / UIPRO_DIR /
  MS_DIR / SKILL_SRC to disk under fix28/scratch-tmp/; ECC_REPO stays
  hardcoded to /tmp/ecc-repo-clean — `fetch_repo` re-clones from GitHub if
  /tmp was wiped, as in fix #27 run 1). Never re-run fix11/fix11-stage.py.
  Staged sources only, never the built tree. build.sh is the source of
  truth. The only build.sh edit is adding the fix28.py invocation after
  fix27's block (same pattern as fix27's +12 lines).

## §7 Non-goals

- Do not re-litigate fixes #14–#27 adjudications (theme cage, orchestration
  pins, grill-me, DESIGNPKG-AUTO, palette-first, MotionSites, Animaster,
  epic-commands reachability, the B6 documentation-only disposition,
  benchmark Dim 7 owed, Netlify row touch-up due after Dec 4, 2026).
- Do not rewrite frozen verifier-asserted texts — except the verifier
  succession (verify27.py → verify28.py) and the README count lines in
  §4(e), both authorized here.
- Do not pre-decide the smoke test's live questions. Do not build a
  Campus Eats render. Do not add a live-render requirement anywhere.
- No new skill, command, rule, agent, hook, or trigger unless the manifest
  justifies it — this fix only removes. (If an implementer finds a
  genuinely new skill is needed, that is a parent decision, not an
  implementer call.)
- No bundle, no commit, no push by the fix workers — the coordinator
  handles the commit + bundle after the loops are clean.
