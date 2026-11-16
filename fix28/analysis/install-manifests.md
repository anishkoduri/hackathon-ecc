# Fix #28 — Install-manifest analysis (install-modules / install-components / install-profiles / pi-core)

Date: 2026-11-16. Read-only analysis. No file was edited, moved, or deleted.

Scope: the built plugin tree at `~/workspace/hackathon-plugin/fix27/scratch-repo/hackathon-ecc/`
(fix #27 tree, commit `b7d0f75`), manifests at `hackathon-ecc/manifests/`.
Authoritative CUT list: `~/workspace/hackathon-plugin/fix27/skill-inventory.md`;
ground truth for existence is the built `hackathon-ecc/skills/` directory (67 dirs).

## Headline result

- **100 dead skill paths** across `install-modules.json` — exactly the 100 skills cut in
  fix #27. Verified programmatically: the set of dead `skills/<name>` paths equals
  `verify27.py`'s `CUT_SKILLS` set exactly (100 == 100, no differences either way).
- **2 modules become empty and must be deleted whole:** `skill-unified-memory`
  (1/1 paths dead) and `business-content` (5/5 paths dead).
- **2 components must be deleted** (their module sets become entirely empty):
  `skill:unified-memory` and `capability:content`.
- **2 profiles must lose entries:** `research` drops `business-content` (8 → 7 modules);
  `full` drops `skill-unified-memory` **and** `business-content` (16 → 14 modules).
- **1 dependency must be pruned:** `workflow-quality.dependencies` is
  `["skill-unified-memory"]` — leaving it after deleting the module breaks **all 7
  profiles** (see §5d, failure mode 2).
- After the prune: **16 → 14 modules, 184 → 84 paths, 57 → 55 components**,
  profiles unchanged except `research` and `full`.
- **`pi-core.json`: NO CHANGE.** All 30 `skills.include` and all 18
  `commands.include` entries exist on disk; see §4.
- **Decision on `skill-unified-memory`: option (a)** — remove the module from
  `install-modules.json` AND remove its id from every profile that lists it
  (only `full`), AND remove the `skill:unified-memory` component, AND remove
  `workflow-quality`'s dependency on it. Justification in §5e. A paths-only prune
  that leaves a dangling profile reference is NOT acceptable — it would throw at
  install time (failure mode 1, §5d); a paths-only prune that leaves an *empty*
  module behind is likewise not acceptable — it preserves a false install surface
  and contradicts the build's own Audit #6 prune rule (drop zero-path modules).

## Method and ground truth

- Listed `hackathon-ecc/skills/` (67 dirs) and checked every `paths` entry in
  `install-modules.json` with `os.path.exists` against the built tree.
- Module path totals: 166 skill paths + 18 non-skill paths = 184. The 166 skill
  paths are exactly the pre-fix-#27 skill catalog (fix27.py's M-new-4 comment
  confirms: "exactly the 166 pre-cut skill paths, 100 CUT + 66 kept").
- Two inventory-vs-disk discrepancies, resolved in favour of the disk +
  `verify27.py` (both agree with each other):
  - `gan-style-harness`: the inventory marked it CUT, but it is **kept** on disk
    and is in `verify27.py`'s `KEPT_SKILLS`. It stays in `agentic-patterns`.
  - `growth-log`: REVIEW in the inventory, **kept** on disk and in `KEPT_SKILLS`.
    It stays in `workflow-quality`.
- One gap found (not a prune — see §7): `motionsites-web-builder` is a kept
  skill on disk (in `KEPT_SKILLS`) but appears in **no** module. It is still
  installable as a single skill via the synthetic `skill:motionsites-web-builder`
  component (see §5c, synthetic components), but no module or profile includes it.

## 1. `install-modules.json` — per-module tables

16 modules, 184 paths. Dead = path does not exist under `hackathon-ecc/`.

### 1a. Modules with no dead paths — KEEP unchanged

| module | paths | dead | verdict |
|---|---|---|---|
| `rules-core` | `rules` | 0 | KEEP. Directory exists. Caveat: the dir still holds ~80 per-language rule files for cut languages (fix #27 MANIFEST §5 item 1, open adjudication). They cannot be pruned through this manifest — the path is the whole directory — and cutting them changes the alwaysApply surface, which needs a parent decision. Out of scope here. |
| `agents-core` | `agents` | 0 | KEEP. Directory exists with the 45 kept agents. The `agent:*` components that name agents with no matching file (`agent:planner`, `agent:fsharp-reviewer` — no `ecc-planner.md` / `ecc-fsharp-reviewer.md` on disk) are labels resolving to this whole directory, not file pointers; see §2. |
| `commands-core` | `commands`, `scripts/harness-audit.js`, `scripts/skills-health.js`, `scripts/lib/skill-evolution`, `scripts/ci/validate-skills.js` | 0 | KEEP. All five paths exist (55 kept commands). |
| `hooks-runtime` | `hooks`, `scripts/hooks`, `scripts/lib` | 0 | KEEP. All exist. |
| `platform-configs` | `scripts/auto-update.js`, `scripts/setup-package-manager.js`, `scripts/lib/package-manager.js` | 0 | KEEP. All exist. |
| `research-apis` | `skills/documentation-lookup` | 0 | KEEP. Skill exists. |
| `orchestration` | `scripts/lib/orchestration-session.js`, `scripts/lib/tmux-worktree-orchestrator.js` | 0 | KEEP. Both exist. |
| `shared-script-utils` | `scripts/lib/utils.js`, `scripts/lib/agent-data-home.js`, `scripts/lib/path-safety.js` | 0 | KEEP. All exist. |

### 1b. `framework-language` — PRUNE 51 of 72 paths, KEEP module

| | |
|---|---|
| Dead (51) — REMOVE | `skills/android-clean-architecture`, `skills/angular-developer`, `skills/bengali-nlp`, `skills/coding-standards`, `skills/compose-multiplatform-patterns`, `skills/csharp-testing`, `skills/fsharp-testing`, `skills/cpp-coding-standards`, `skills/cpp-testing`, `skills/dart-flutter-patterns`, `skills/django-patterns`, `skills/django-tdd`, `skills/django-verification`, `skills/dotnet-patterns`, `skills/frontend-design-direction`, `skills/i18n-sync`, `skills/golang-patterns`, `skills/golang-testing`, `skills/java-coding-standards`, `skills/kotlin-coroutines-flows`, `skills/kotlin-exposed-patterns`, `skills/kotlin-ktor-patterns`, `skills/kotlin-patterns`, `skills/kotlin-testing`, `skills/laravel-plugin-discovery`, `skills/laravel-patterns`, `skills/laravel-tdd`, `skills/laravel-verification`, `skills/mcp-server-patterns`, `skills/nestjs-patterns`, `skills/perl-patterns`, `skills/perl-testing`, `skills/quarkus-patterns`, `skills/quarkus-tdd`, `skills/quarkus-verification`, `skills/rails-patterns`, `skills/rust-patterns`, `skills/rust-testing`, `skills/springboot-patterns`, `skills/springboot-tdd`, `skills/springboot-verification`, `skills/ui-to-vue`, `skills/vue-patterns`, `skills/accessibility`, `skills/bun-runtime`, `skills/django-celery`, `skills/flutter-dart-code-review`, `skills/generating-python-installer`, `skills/hexagonal-architecture`, `skills/nuxt4-patterns`, `skills/tinystruct-patterns` |
| Kept (21) | `skills/api-design`, `skills/backend-patterns`, `skills/contract-first`, `skills/design-system`, `skills/fastapi-patterns`, `skills/frontend-a11y`, `skills/frontend-patterns`, `skills/frontend-slides`, `skills/make-interfaces-feel-better`, `skills/motion-advanced`, `skills/motion-foundations`, `skills/motion-patterns`, `skills/nextjs-turbopack`, `skills/python-patterns`, `skills/python-testing`, `skills/react-native-patterns`, `skills/react-patterns`, `skills/react-performance`, `skills/react-testing`, `skills/typescript-patterns`, `skills/vite-patterns` |
| Verdict | PRUNE paths, KEEP module. 21 live skills remain; its `dependencies` (`rules-core`, `agents-core`, `commands-core`, `platform-configs`) all survive. Description ("Core framework, language, and application-engineering skills.") stays accurate — no edit needed. |

### 1c. `database` — PRUNE 7 of 8 paths, KEEP module

| | |
|---|---|
| Dead (7) — REMOVE | `skills/clickhouse-io`, `skills/database-migrations`, `skills/jpa-patterns`, `skills/mybatis-patterns`, `skills/mysql-patterns`, `skills/prisma-patterns`, `skills/redis-patterns` |
| Kept (1) | `skills/postgres-patterns` |
| Verdict | PRUNE paths, KEEP module. One live skill remains; `dependencies` (`platform-configs`) survives. Note: `database-migrations`, `prisma-patterns`, `redis-patterns` were REVIEW in the inventory and were cut in the final fix #27 tree — they are gone from disk, so the prune stands regardless of the review outcome. |

### 1d. `skill-unified-memory` — DELETE module whole

| | |
|---|---|
| Contents | Single path: `skills/unified-memory`. Description: "Single-skill unified-memory guidance; requires the separately installed ecc-universal CLI runtime." |
| Dead | 1/1 — `skills/unified-memory` does not exist (`unified-memory` is in `CUT_SKILLS`; skill-inventory: "Shared context between agents via Memory Vault; duplicates ck and is unreachable [orphan]"). |
| Verdict | **DELETE the entire module object.** Full trace in §5; chain fix in §6. |

### 1e. `workflow-quality` — PRUNE 29 of 43 paths, KEEP module, PRUNE dependency + description

| | |
|---|---|
| Dead (29) — REMOVE | `skills/agent-sort`, `skills/agent-introspection-debugging`, `skills/ai-regression-testing`, `skills/code-tour`, `skills/continuous-learning`, `skills/continuous-learning-v2`, `skills/dev-team`, `skills/hookify-rules`, `skills/iterative-retrieval`, `skills/plankton-code-quality`, `skills/skill-scout`, `skills/skill-stocktake`, `skills/story-lifecycle`, `skills/windows-desktop-e2e`, `skills/agent-self-evaluation`, `skills/architecture-decision-records`, `skills/brownfield-retrospective`, `skills/codebase-onboarding`, `skills/codehealth-mcp`, `skills/ecc-recipes`, `skills/inherit-legacy-style`, `skills/intent-driven-development`, `skills/living-docs-governance`, `skills/loop-design-check`, `skills/product-lens`, `skills/repo-scan`, `skills/rules-distill`, `skills/santa-method`, `skills/conventional-commit-review` |
| Kept (14) | `skills/council`, `skills/e2e-testing`, `skills/error-handling`, `skills/production-audit`, `skills/strategic-compact`, `skills/tdd-workflow`, `skills/verification-loop`, `skills/browser-qa`, `skills/ck`, `skills/click-path-audit`, `skills/context-budget`, `skills/delivery-gate`, `skills/growth-log`, `skills/git-workflow` |
| Verdict | PRUNE paths, KEEP module. **Must also delete** `"dependencies": ["skill-unified-memory"]` (see §5d, failure mode 2 — this is not optional). **Must also edit the description:** it currently reads "…including the legacy continuous-learning v1 path. The unified-memory workflow requires the separately installed ecc-universal CLI runtime." Both named things are gone; proposed replacement in §6a item 6. |

### 1f. `security` — PRUNE 2 of 3 paths, KEEP module

| | |
|---|---|
| Dead (2) — REMOVE | `skills/mcp-dependency-review`, `skills/security-scan` |
| Kept (1) | `skills/security-review` |
| Verdict | PRUNE paths, KEEP module. `dependencies` (`workflow-quality`) survives. |

### 1g. `business-content` — DELETE module whole

| | |
|---|---|
| Contents | `skills/article-writing`, `skills/content-engine`, `skills/investor-materials`, `skills/investor-outreach`, `skills/market-research` |
| Dead | 5/5 — all cut in fix #27 (writing/investor/market skills, none on disk). |
| Verdict | **DELETE the entire module object.** Parallel case to `skill-unified-memory`: it is referenced by `capability:content` (§2) and by the `research` and `full` profiles (§3). All three references must go with it. No live `.js`/`.md` reference to `business-content` exists outside the three manifests (verified by grep over the live tree). |

### 1h. `agentic-patterns` — PRUNE 1 of 8 paths, KEEP module

| | |
|---|---|
| Dead (1) — REMOVE | `skills/opensource-pipeline` |
| Kept (7) | `skills/gan-style-harness`, `skills/orch-add-feature`, `skills/orch-build-mvp`, `skills/orch-change-feature`, `skills/orch-fix-defect`, `skills/orch-pipeline`, `skills/orch-refine-code` |
| Verdict | PRUNE path, KEEP module. (`gan-style-harness` stays — see Method note.) |

### 1i. `hackathon` — PRUNE 4 of 25 paths, KEEP module, edit description

| | |
|---|---|
| Dead (4) — REMOVE | `skills/agents-md-generator`, `skills/brainstorming`, `skills/codebase-memory`, `skills/dispatching-parallel-agents` |
| Kept (21) | `skills/ai-feature-spec`, `skills/api-integration`, `skills/app-scaffold`, `skills/deploy-fast`, `skills/design-taste-frontend`, `skills/devpost-autofiller`, `skills/feature-expansion`, `skills/grill-me`, `skills/hackathon-pitch`, `skills/hackathon-scope`, `skills/integration`, `skills/less-flat-ui`, `skills/mobile-ship`, `skills/orchestrate`, `skills/pitch-deck-video`, `skills/polish-pass`, `skills/readme-writer`, `skills/systematic-debugging`, `skills/track-picker`, `skills/ui-ux-pro-max`, `skills/verification-before-completion` |
| Verdict | PRUNE paths, KEEP module. **Description edit:** it reads "Hackathon workflow skills: scoping, brainstorming, orchestration, shipping, pitching, and demo-video production." `brainstorming` was REVIEW in the inventory and is cut in the final tree — remove the word "brainstorming, " (proposed text in §8). |

### 1j. Module totals after the prune

| module | paths before → after |
|---|---|
| `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`, `platform-configs`, `research-apis`, `orchestration`, `shared-script-utils` | unchanged (18 paths total) |
| `framework-language` | 72 → 21 |
| `database` | 8 → 1 |
| `skill-unified-memory` | 1 → **module deleted** |
| `workflow-quality` | 43 → 14 (+ dependency deleted, description edited) |
| `security` | 3 → 1 |
| `business-content` | 5 → **module deleted** |
| `agentic-patterns` | 8 → 7 |
| `hackathon` | 25 → 21 (+ description edited) |
| **Total** | **16 modules / 184 paths → 14 modules / 84 paths** |

No other module `dependencies` / `optionalDependencies` reference a deleted
module: the only dependency edge into a deleted module is
`workflow-quality → skill-unified-memory` (verified: every other dependency
names a surviving module).

## 2. `install-components.json` — per-component verdicts

57 components. Components reference modules, not skill paths directly, so a
component is *dead* only when **all** of its modules are deleted, and
*misleading* when its named skill/language/framework has no surviving content
in the modules it resolves to. The build already encodes a rule for this:
`build.sh`'s Audit #7 connectivity prune keeps a component iff **any** of its
modules survives (`any(m in _kept_ids for m in c["modules"])`). This analysis
follows that same rule for deletions, and flags the misleading-but-surviving
components separately instead of guessing a prune (per the KEEP-when-in-doubt
constraint).

### 2a. DELETE (all modules deleted) — 2 components

| component | modules | evidence |
|---|---|---|
| `skill:unified-memory` (`family: skill`, "Cross-harness memory guidance that requires the separately installed ecc-universal CLI runtime.") | `["skill-unified-memory"]` | Its only module is deleted (§1d). If kept, requesting this component would resolve to the deleted module and throw `Unknown install module` (see §5d). |
| `capability:content` (`family: capability`, "Business, writing, market, investor communication, and reusable voice-system skills.") | `["business-content"]` | Its only module is deleted (§1g). Same throw if kept and requested. |

### 2b. KEEP — components resolving to a surviving module (55 components)

- **Baseline (6):** `baseline:rules`, `baseline:agents`, `baseline:commands`,
  `baseline:hooks`, `baseline:platform`, `baseline:workflow` — all resolve to
  surviving modules. KEEP unchanged.
- **Capability (4 of 6):** `capability:database` → `database` (survives with
  `postgres-patterns`); `capability:security` → `security` (survives with
  `security-review`); `capability:research` → `research-apis` (unchanged);
  `capability:orchestration` → `orchestration` (unchanged); `capability:agentic`
  → `agentic-patterns` (survives). KEEP unchanged. (`capability:content` is
  deleted, §2a.)
- **Single-skill, kept skill (6):** `skill:tdd-workflow`, `skill:verification-loop`,
  `skill:strategic-compact`, `skill:frontend-patterns`, `skill:backend-patterns`,
  `skill:security-review` — the named skill exists on disk and in the resolved
  module. KEEP unchanged.
- **Agent (12):** all `agent:*` → `agents-core` (survives). KEEP. Two are
  name-mismatched but not dead — see below.
- **Language / framework (27):** all resolve to `framework-language` (survives
  with 21 skills), alone or with `security` (survives). KEEP under the Audit #7
  any-module rule. The misleading ones are listed in §2c with proposed
  description fixes; deletion is a stricter alternative for the parent to call
  (see §2c).

### 2c. KEEP but misleading — description fixes proposed (no deletion)

These components' named skill/language/framework has **zero** surviving content
in the module(s) they resolve to, so today they silently install unrelated
skills. E.g. selecting `lang:go` installs `framework-language` — 21
TypeScript/Python/React skills and zero Go. Deleting them would change selector
behaviour (a request would throw `Unknown install component` instead of
installing the shared module), so per KEEP-when-in-doubt they are **kept**, with
the exact description corrections in §8. If the parent prefers deletion, the
edit is mechanical (delete the component object); the affected set is listed
here so the decision can be taken in one place.

- **Dead single-skill components (4):** `skill:continuous-learning` (also
  mentions `continuous-learning-v2` in its description — "prefer
  continuous-learning-v2 for new installs" — both skills are cut),
  `skill:windows-desktop-e2e`, `skill:coding-standards`, `skill:vue-patterns`.
  Each resolves to a surviving module (`workflow-quality` /
  `framework-language`), which is why the module-level prune cannot catch them
  — this matches the Audit #8 comment in `build.sh` ("Orphans: the named skills
  do not exist in the plugin, so no module prune can catch them"), which already
  deleted 4 such orphans (`skill:deep-research`, `skill:eval-harness`,
  `skill:osint-investigation`, `skill:plan-canvas`). These 4 are the same class
  of orphan and are the strongest deletion candidates after §2a.
- **Dead language/framework components (18):** `lang:go`, `lang:java`,
  `lang:cpp`, `lang:c`, `lang:kotlin`, `lang:arkts`, `lang:perl`, `lang:ruby`,
  `lang:rust`, `lang:csharp`, `lang:fsharp`, `framework:angular`,
  `framework:vue`, `framework:django`, `framework:springboot`,
  `framework:quarkus`, `framework:rails`, `framework:laravel`. All resolve
  through `framework-language` (+ `security` for `framework:quarkus`,
  `lang:perl`, `lang:ruby`, `framework:rails`, `framework:laravel`), which
  contains no content for the named language/framework after the prune.
  (The surviving `security-review` inside `security` is not Perl/Rails/Laravel
  content, so it does not save these components.)
- **Kept language/framework components with stale wording (2):**
  `lang:python` ("Python and Django-oriented engineering guidance") —
  Django is gone, Python survives; `framework:quarkus` description is generic
  enough but see the dead list above. `lang:typescript`, `framework:react`,
  `framework:nextjs` are accurate as-is (TypeScript/React/Next.js skills survive).
- **Name-mismatched agent components (2):** `agent:planner` and
  `agent:fsharp-reviewer` resolve to `agents-core`, but no `ecc-planner.md` or
  `ecc-fsharp-reviewer.md` exists on disk (45 agents verified by listing).
  They are labels for the shared agent library, not file pointers; KEEP, note
  the mismatch. (All other `agent:*` names have a matching agent file, e.g.
  `agent:harmonyos-app-resolver` → `ecc-harmonyos-app-resolver.md`.)

## 3. `install-profiles.json` — per-profile verdicts

7 profiles. A profile is affected only if it lists a deleted module.

| profile | modules before | verdict |
|---|---|---|
| `minimal` | `rules-core`, `agents-core`, `commands-core`, `platform-configs`, `workflow-quality` | KEEP unchanged. All 5 modules survive. |
| `opencode` | `commands-core`, `platform-configs`, `workflow-quality` | KEEP unchanged. |
| `core` | `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`, `platform-configs`, `workflow-quality` | KEEP unchanged. |
| `developer` | `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`, `platform-configs`, `workflow-quality`, `framework-language`, `database`, `orchestration`, `hackathon` | KEEP unchanged. All 10 modules survive (shrunk, not emptied). |
| `security` | `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`, `platform-configs`, `workflow-quality`, `security` | KEEP unchanged. `security` survives with `security-review`. |
| `research` | `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`, `platform-configs`, `workflow-quality`, `research-apis`, `business-content` | **REMOVE `"business-content"`** (8 → 7 modules). The profile's description ("Research and content-oriented setup…") still mentions content; proposed description edit in §8 (drop "and content-oriented" or reword to research-only). |
| `full` | `rules-core`, `agents-core`, `shared-script-utils`, `commands-core`, `hooks-runtime`, `platform-configs`, `framework-language`, `database`, `workflow-quality`, `skill-unified-memory`, `security`, `research-apis`, `business-content`, `orchestration`, `agentic-patterns`, `hackathon` | **REMOVE `"skill-unified-memory"` AND `"business-content"`** (16 → 14 modules). This is the only profile listing `skill-unified-memory` (line 85). |

No profile lists any other removed module, and no profile becomes empty.

## 4. `pi-core.json` — NO CHANGE

- `skills.include`: 30 entries, **all 30 exist** in `hackathon-ecc/skills/`
  (verified against disk). `commands.include`: 18 entries, **all 18 exist** in
  `hackathon-ecc/commands/`.
- `unified-memory` appears once, at line 229, as an `exclude` reason entry:
  `"unified-memory": "ECC memory vault (session save/resume family)"`. That is
  a reason log for why the upstream catalog entry is not in the Pi subset — not
  a live reference. **Do not remove it.**
- Same caution for the `exclude` map generally: it lists 15 names that are
  *kept* skills in this plugin (`browser-qa`, `ck`, `context-budget`,
  `delivery-gate`, `documentation-lookup`, `frontend-slides`,
  `gan-style-harness`, `growth-log`, `orch-add-feature`, `orch-build-mvp`,
  `orch-change-feature`, `orch-fix-defect`, `orch-pipeline`, `orch-refine-code`,
  `strategic-compact`). Those entries document why each upstream skill is not
  in the 30-skill Pi subset (e.g. Cursor-only mechanics, SaaS wrappers). They
  are not errors and not dangling references. Do not "fix" them.
- `verify27.py` already asserts the pi-core prune (see §9); nothing further
  is needed here.

## 5. The `skill-unified-memory` trace, end to end

### 5a. What the module contains

`install-modules.json:212-221` (exact):

```json
{
  "id": "skill-unified-memory",
  "kind": "skills",
  "description": "Single-skill unified-memory guidance; requires the separately installed ecc-universal CLI runtime.",
  "paths": ["skills/unified-memory"],
  "targets": ["cursor"],
  "dependencies": ["platform-configs"],
  "defaultInstall": false,
  "cost": "light",
  "stability": "stable"
}
```

One skill, one path. The skill is gone: `hackathon-ecc/skills/unified-memory/`
does not exist; `unified-memory` is in fix #27's CUT list (skill-inventory:
"Shared context between agents via Memory Vault; duplicates ck and is
unreachable [orphan]"). 0 of its paths survive — the module is 100% dead.

### 5b. Every reference to the module id `skill-unified-memory`

Live tree (`hackathon-ecc/`, verified by grep — no `.js` or `.md` file references
it):

| location | form | action in fix #28 |
|---|---|---|
| `manifests/install-modules.json:212` | module definition (above) | DELETE the module object |
| `manifests/install-modules.json:281` | `"skill-unified-memory"` in `workflow-quality.dependencies` | DELETE the dependency (delete the whole `dependencies` field — it becomes empty) |
| `manifests/install-components.json:382` | `"skill-unified-memory"` in the `skill:unified-memory` component's `modules` | DELETE the component object (§2a) |
| `manifests/install-profiles.json:85` | `"skill-unified-memory"` in the `full` profile's `modules` | DELETE the entry from `full` (§3) |
| `manifests/pi-core.json:229` | `"unified-memory"` as an `exclude`-reason key | KEEP — reason log, not a reference (§4) |

No other live reference exists. In particular, `scripts/lib/install-manifests.js`
does not name the module, and no kept skill, agent, command, rule, or hook
references it.

Historical / non-live occurrences (do **not** edit — frozen records of earlier
fixes, not the live install surface):

- `build.sh:16971, 16983` — embedded Audit #10 patch text quoting the old
  `install-profiles.json` `full` list (which is why the stale id is baked into
  the build script's history, not its live output).
- `scratch-repo/fix22/ecc-check/` — frozen copy of the old manifests plus its
  tests (`tests/lib/install-manifests.test.js`, `tests/scripts/install-apply.test.js`),
  which assert the old module. Historical only.
- `scratch-repo/fix13*/build*.log`, `fix14–fix27/build-log-*.txt` — old build
  logs ("Selected modules: … skill-unified-memory …"). Historical only.
- `fix27/MANIFEST.md` §5 item 2, `fix27/audit76-report.md:79`,
  `fix27/fix27-round3-patch-log.md:161`, `fix27/fix27.py:1039-1046` — the fix #27
  decision record for leaving the manifests unpruned (M-new-4). Historical only.

### 5c. The silently-skips-missing-paths behaviour — confirmed in code

`hackathon-ecc/scripts/lib/install/plan.js`, `materializeScaffoldOperation`,
lines 154–157 (the task's cited lines check out exactly):

```js
const sourcePath = path.join(sourceRoot, operation.sourceRelativePath);
if (!fs.existsSync(sourcePath)) {
  return [];
}
```

A manifest path that does not exist produces **zero operations, no warning, no
error**. The same guard exists for directories in `listFilesRecursive`
(plan.js:58–60: `if (!fs.existsSync(dirPath)) { return []; }`). This is why
the 100 stale paths are harmless *at install time today* — and also why they
are invisible: nothing fails, so nothing flags them.

Two related machinery facts that bound the prune:

1. **The live single-skill surface is derived from disk, not from the
   manifests.** `scripts/lib/install-manifests.js:128-162`,
   `addSyntheticSkillComponents`, iterates `listSkillDirectoryIds(repoRoot)`
   (the actual `skills/` directory) and synthesizes a `skill:<id>` component
   (and a `skill-<id>` module if missing) for each skill dir present. Since
   `skills/unified-memory/` is gone, no synthetic `skill:unified-memory` is
   generated — the declared component in `install-components.json` is the only
   thing still advertising it. Deleting the declared component therefore
   removes the *only* route by which the dead skill can be selected.
2. **Manifest loading does NOT validate references.**
   `loadInstallManifests` (install-manifests.js:239–290) only checks that
   `optionalDependencies` is an array of declared dependency ids; it does not
   check that profile modules, component modules, or dependency ids exist.
   Validation happens at plan time, in `resolveInstallPlan` — which is exactly
   where a partial prune breaks (next section).

### 5d. Why a naive prune breaks: the two failure modes

**Failure mode 1 — module deleted, profile reference left.**
`resolveInstallPlan` (install-manifests.js:508–513) pushes the `full` profile's
module ids into `requestedModuleIds`, then `resolveModule` (install-manifests.js
~571–574) does:

```js
const module = manifests.modulesById.get(moduleId);
if (!module) {
  throw new Error(`Unknown install module: ${moduleId}`);
}
```

So installing profile `full` would throw
`Unknown install module: skill-unified-memory` and abort the install. The
silent skip in plan.js never gets a chance to run — resolution throws first.
**A paths-only prune that deletes the module but leaves
`install-profiles.json:85` is therefore not a prune at all; it is a
regression in the `full` profile.** This is the exact trap fix #27's
M-new-4 record warned about.

**Failure mode 2 — module deleted, `workflow-quality` dependency left.**
`workflow-quality.dependencies` is `["skill-unified-memory"]`, and
`resolveModule` recurses into dependencies for every module it resolves.
`workflow-quality` is in **all 7 profiles**, so leaving the dependency would
throw `Unknown install module: skill-unified-memory` for every profile, not
just `full`. The dependency deletion is as mandatory as the profile edit.

**Failure mode 3 (non-breaking, misleading) — paths pruned, empty module left.**
If the single path were removed but the module object kept, resolution would
succeed and install nothing for that module: the `full` profile would
advertise unified-memory guidance that silently installs zero files. That is
the "misleading module" fix #27 flagged, and it is also what the build's own
Audit #6 prune rule already forbids (drop modules left with zero paths —
`build.sh`, Audit #6 section). Not acceptable as the fix #28 outcome.

### 5e. Decision: option (a)

**Remove the module from `install-modules.json` AND remove its id from every
profile that lists it (only `full`), AND remove the `skill:unified-memory`
component, AND remove `workflow-quality`'s dependency on it.** All four edits
are one atomic change; any subset breaks (modes 1–2) or misleads (mode 3).

- **Why not (b) re-point?** There is no kept equivalent module. The closest
  surviving memory skill is `ck` ("Per-project memory for Cursor") — but `ck`
  is already inside `workflow-quality`, which `full` already includes, and it
  is a different thing: per-project Cursor memory, not cross-harness unified
  memory requiring the separately installed ecc-universal CLI runtime. There
  is nothing to re-point *to* that would preserve the meaning of the
  reference; re-pointing would just mislabel `workflow-quality`.
- **Why not (c) leave in place?** It would preserve a false install surface
  (a `full`-profile module and a selectable component for a skill that does
  not exist and installs nothing), contradict fix #28's purpose, and be
  reverted by the next application of the build's own Audit #6 prune rule,
  which drops zero-path modules. The only genuine argument for (c) — that the
  stale entries are harmless at install time — is true today only because
  plan.js silently skips missing paths; it is not a reason to keep shipping
  them once the fix is being done coherently with verifier coverage.

The `business-content` chain gets the identical (a) treatment: delete module +
delete `capability:content` component + delete its entries from `research`
and `full`.

## 6. Exact proposed JSON edits

Apply as one atomic change. Notation: `−` remove, `~` edit. Path lists are
complete — every dead path named in §1 is removed, every kept path stays in
its original order.

### 6a. `install-modules.json` (16 → 14 modules, 184 → 84 paths)

1. `framework-language.paths`: delete the 51 dead paths listed in §1b; keep
   the 21 listed there, in original order.
2. `database.paths`: delete the 7 dead paths in §1c; keep `["skills/postgres-patterns"]`.
3. **Delete the entire `skill-unified-memory` module object** (§1d).
4. `workflow-quality.paths`: delete the 29 dead paths in §1e; keep the 14
   listed there, in original order.
5. `workflow-quality`: **delete the `"dependencies": ["skill-unified-memory"]`
   field entirely** (do not leave `"dependencies": []` — the build's Audit #6
   prune logic pops the field when it becomes empty; follow that convention).
6. `workflow-quality.description`: replace
   `"Evaluation, TDD, verification, compaction, learning, and cross-harness memory skills, including the legacy continuous-learning v1 path. The unified-memory workflow requires the separately installed ecc-universal CLI runtime."`
   with
   `"Evaluation, TDD, verification, compaction, learning, and memory skills."`
7. `security.paths`: delete `skills/mcp-dependency-review` and
   `skills/security-scan`; keep `["skills/security-review"]`.
8. **Delete the entire `business-content` module object** (§1g).
9. `agentic-patterns.paths`: delete `skills/opensource-pipeline`; keep the 7
   in §1h.
10. `hackathon.paths`: delete the 4 dead paths in §1i; keep the 21 listed there.
11. `hackathon.description`: replace
    `"Hackathon workflow skills: scoping, brainstorming, orchestration, shipping, pitching, and demo-video production."`
    with
    `"Hackathon workflow skills: scoping, orchestration, shipping, pitching, and demo-video production."`
12. No change to `rules-core`, `agents-core`, `commands-core`, `hooks-runtime`,
    `platform-configs`, `research-apis`, `orchestration`, `shared-script-utils`.
    (`"version": 1` unchanged.)

### 6b. `install-components.json` (57 → 55 components)

1. **Delete the entire `skill:unified-memory` component object.**
2. **Delete the entire `capability:content` component object.**
3. No other component is deleted in this fix. (The 4 dead single-skill
   components and 18 dead language/framework components of §2c are kept with
   description corrections below; deletion is a parent-callable stricter
   alternative — the exact deletion edit is just removing those component
   objects, no other file changes, since none of them is the sole referrer of
   a surviving module.)
4. Description corrections for kept components (exact replacements):
   - `skill:continuous-learning`: replace `"Legacy v1 Stop-hook session pattern extraction skill; prefer continuous-learning-v2 for new installs."` with `"Legacy v1 Stop-hook session pattern extraction skill. (Removed in fix #27; resolves to the shared workflow-quality module.)"` — or delete the component per §2c.
   - `lang:python`: replace `"Python and Django-oriented engineering guidance. Currently resolves through the shared framework-language module."` with `"Python engineering guidance. Currently resolves through the shared framework-language module."`
   - `lang:go`, `lang:java`, `lang:cpp`, `lang:c`, `lang:kotlin`, `lang:arkts`, `lang:perl`, `lang:ruby`, `lang:rust`, `lang:csharp`, `lang:fsharp`, `framework:angular`, `framework:vue`, `framework:django`, `framework:springboot`, `framework:quarkus`, `framework:rails`, `framework:laravel`: append to each description `" (Guidance for this language/framework was removed in fix #27; resolves to the shared framework-language module.)"` — or delete the component per §2c.
   - `skill:windows-desktop-e2e`, `skill:coding-standards`, `skill:vue-patterns`:
     append `" (Removed in fix #27; resolves to the shared workflow-quality / framework-language module.)"` as appropriate — or delete per §2c.
   - `research` profile description is covered in §6c; no component description
     changes are needed for the kept baseline/capability/agent components.

### 6c. `install-profiles.json` (only `research` and `full` change)

1. `research.modules`: delete `"business-content"` (8 → 7). Description:
   replace `"Research and content-oriented setup for investigation, synthesis, and publishing workflows."` with `"Research-oriented setup for investigation and synthesis workflows."`
2. `full.modules`: delete `"skill-unified-memory"` and `"business-content"`
   (16 → 14). Description ("Complete ECC install with all currently classified
   modules.") stays accurate.
3. No change to `minimal`, `opencode`, `core`, `developer`, `security`.

### 6d. `pi-core.json`

**No edits.**

## 7. KEEP items with reasons (summary)

| item | reason |
|---|---|
| `rules-core` / `agents-core` / `commands-core` / `hooks-runtime` / `platform-configs` / `research-apis` / `orchestration` / `shared-script-utils` modules | Every listed path exists on disk (verified). |
| `framework-language`, `database`, `workflow-quality`, `security`, `agentic-patterns`, `hackathon` modules | Each retains live skills after the prune (21 / 1 / 14 / 1 / 7 / 21); all their dependencies survive. |
| 55 of 57 components, incl. the 4 dead `skill:*` and 18 dead language/framework components (§2c) | They resolve to surviving modules under the build's own Audit #7 any-module-survives rule; deleting them changes selector behaviour (request → `Unknown install component` throw) rather than saving bytes. Kept with description corrections; deletion is flagged as a parent decision, not assumed. |
| `agent:planner`, `agent:fsharp-reviewer` | Labels resolving to the surviving `agents-core` directory; no file pointer is broken. |
| All profiles except `research` / `full` | Every module they list survives. |
| `pi-core.json` entire file | No dead references; `unified-memory` and the 15 kept-skill names in `exclude` are reason logs, not references (§4). |
| `motionsites-web-builder` — NOT added to any module in this fix | It is a kept skill with no module home, but adding it to `hackathon` (its natural home) is an addition, not a prune, and was not tasked. Flagged for the parent: one-line addition of `"skills/motionsites-web-builder"` to `hackathon.paths` would make it installable via the hackathon module; until then it is reachable only via the synthetic `skill:motionsites-web-builder` component. |

## 8. Implementation note — where the fix must be encoded

**Do not just hand-edit the JSONs in `scratch-repo/hackathon-ecc/manifests/`.**
`fix27.py`'s header states it is "Run by build.sh as a patch step (after
fix26, before STEP 5 Counts)" and "never edit build.sh or any staged skill
here" — i.e. the built tree is regenerated by `build.sh`, and a hand edit to
the built JSONs would be overwritten on the next rebuild. The fix #28
implementation should be a patch step in the same pattern (a `fix28.py` run by
`build.sh` after the fix #27 skill cuts, or an equivalent new `build.sh`
section), applying the §6 edits to the built manifests.

Two existing `build.sh` mechanisms are directly relevant:

1. **The Audit #6 embedded prune** (`build.sh`, Audit #6 section) already
   implements exactly the `install-modules.json` part of §6a: drop every
   `paths` entry that does not exist, drop modules left with zero paths, prune
   `dependencies`/`optionalDependencies` naming a dropped module. It runs
   against the tree *before* the fix #27 skill cuts (when the 166 paths still
   exist), which is why it pruned nothing in fix #27. Re-running that same
   logic **after** the skill cuts produces §6a items 1–5 and 7–10
   automatically (16 → 14 modules, 184 → 84 paths — the projection was
   verified in §1j). The description edits (§6a items 6, 11) and the
   `install-components.json` / `install-profiles.json` follow-ups are the
   parts that need new code.
2. **The Audit #7 connectivity prune** (`build.sh`, Audit #7 section) already
   implements the profile/component follow-up: drop every profile module and
   every component whose module id is not in the pruned module set. Re-run
   after the cuts, it produces §6b items 1–2 and §6c items 1–2 automatically
   (components 57 → 55 — note the current 57 already reflects the Audit #8
   orphan deletion, so the Audit #8 hard assert `assert _comp_before == 61`
   runs *earlier* in `build.sh` and is unaffected by a later fix #28 step, as
   long as the fix #28 step is ordered after it).
3. The §2c description corrections and the §7 `motionsites-web-builder`
   question are new decisions with no existing encoding; they need explicit
   new patch code (or a parent decision to defer them).

## 9. What `verify27.py` asserts about these manifests (for the fix #28 verifier)

`~/workspace/hackathon-plugin/fix27/verify27.py` (1,028 lines) asserts
**exactly one thing** about the manifests, and it is only about `pi-core.json`:

- **Lines 540–548 (M-new-4):**
  ```python
  _picore = json.load(open(os.path.join(BASE, "manifests/pi-core.json"), encoding="utf-8"))
  _picore_skills = set(_picore.get("skills", {}).get("include", []))
  _picore_cmds = {_c[:-3] if _c.endswith(".md") else _c
                  for _c in _picore.get("commands", {}).get("include", [])}
  check("M-new-4 pi-core.json: skills.include has no CUT skills, commands.include has no dropped commands",
        not (_picore_skills & set(CUT_SKILLS))
        and not (_picore_cmds & set(DROPPED_COMMANDS)))
  ```
  I.e. no `skills.include` entry is in `CUT_SKILLS` (100) and no
  `commands.include` entry (minus `.md`) is in `DROPPED_COMMANDS` (32).
  It passes on the current tree and is unaffected by this fix (no pi-core
  change is proposed).
- **Nothing else in `verify27.py` asserts anything about
  `install-modules.json`, `install-components.json`, or
  `install-profiles.json`.** That absence is precisely why fix #27 could
  leave them unpruned without failing (M-new-4). Related module-level
  asserts that the fix #28 verifier can reuse as inputs (lines 223–228):
  `len(CUT_SKILLS) == 100`, `len(KEPT_SKILLS) == 67`,
  `len(REMOVED_AGENTS) == 27`, `len(KEPT_AGENTS) == 45`,
  `len(DROPPED_COMMANDS) == 32`, `len(KEPT_COMMANDS) == 55`,
  `len(F27_TOKENS) == 20`, no CUT/KEPT overlap, `"growth-log" in KEPT_SKILLS`.

Suggested fix #28 verifier extensions (not implemented here — read-only task):

1. Every `paths` entry in `install-modules.json` exists on disk.
2. No module has zero paths; `skill-unified-memory` and `business-content`
   are absent from all three manifests; `workflow-quality` has no
   `dependencies` naming a deleted module.
3. Every module id in every profile and every component exists in
   `install-modules.json` (catches failure modes 1–2 by construction).
4. `install-profiles.json: full` has 14 modules; `research` has 7.
5. `install-components.json` has 55 components.
6. `resolveInstallPlan` succeeds for every profile (exercises the
   `Unknown install module` throw path directly — the strongest check).
7. `pi-core.json` M-new-4 check re-run unchanged.
8. No `CUT_SKILLS` name appears in any manifest `paths` array; no
   `DROPPED_COMMANDS` name appears in any manifest path.
