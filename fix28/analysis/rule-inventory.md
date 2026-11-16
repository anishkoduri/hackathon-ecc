# Fix #28 — Rule inventory: all 123 rules in `hackathon-ecc/rules/`

Date: 2026-11-16. Read-only analysis (no file edited, moved, or deleted).
Source tree: `~/workspace/hackathon-plugin/fix27/scratch-repo` at commit `b7d0f75` (fix #27 tree).
Built plugin tree: `hackathon-ecc/` inside that repo. The fix #28 working copy
`~/workspace/hackathon-plugin/fix28/scratch-repo` was diffed against it: `diff -rq` on
`hackathon-ecc/rules/` returned empty, same HEAD `b7d0f75` — this inventory applies to both.
Cross-reference: `~/workspace/hackathon-plugin/fix27/skill-inventory.md` (fix #27 CUT list, 91 skills).

## Headline counts

| Verdict | Count |
|---|---|
| NEVER CUT (alwaysApply) | 12 |
| KEEP | 36 |
| CUT | 68 |
| NEEDS-DECISION | 7 |
| **Total** | **123** |

Cutting all 68 CUT files would leave 55 rules (12 alwaysApply + 36 KEEP + 7 NEEDS-DECISION).
Cutting CUT + all 7 NEEDS-DECISION would leave 48 rules (61% smaller than 123).
Every CUT below requires two implementation-time updates (see §5–§6): the `verify27.py`
counts check asserts exactly 123 rules, and `build.sh` contains patch calls naming
21 of the CUT/NEEDS-DECISION files — both must be updated or the build/verify breaks.

## Method (evidence-first)

1. **Census.** Frontmatter (`globs`, `alwaysApply`) read from all 123 `.mdc` files in
   `hackathon-ecc/rules/`. 12 files carry `alwaysApply: true`; 30 carry `alwaysApply: false`;
   81 carry no `alwaysApply` key at all (Cursor default: not always-applied).
2. **Literal-path hunt.** For every rule `<fam>-<kind>.mdc`, grepped the scope below for
   three patterns: `<stem>.mdc`, `<fam>/<kind>.md` (old ECC nested form), `rules/<stem>`.
   Full command (loop over all 123 stems; output saved at `/tmp/rule-hunt.txt`):
   `grep -rn --exclude-dir=node_modules -e "${stem}\.mdc" -e "${fam}/${kind}\.md" -e "rules/${stem}" <scope> verify27.py`
3. **Bare-name hunt.** `grep -rnw <stem>` for every stem over the same scope, excluding the
   rule file itself, `call-map.md`, `build.sh`, `verify27.py` — catches prose pointers such as
   'see the typescript-patterns rule' and `skill:`-style references. Hits that turned out to
   name a *skill* of the same name (e.g. `skills/python-patterns/`, `skill: python-patterns`)
   were classified as skill references, NOT rule dispatches, and are called out per row.
4. **Family-glob hunt.** `grep -rn -e 'rules/[a-z-]*-\*.mdc' -e 'rules/[a-z-]*/' -e '[a-z-]*-\*.mdc'`
   over the scope — catches `rules/typescript-*.mdc`, `rules/react-*.mdc`, `rules/arkts-*.mdc`,
   `rules/react-native/` style dispatches that name a whole family instead of one file.
5. **Scope.** Built tree `hackathon-ecc/{skills,agents,commands,rules,hooks,manifests,README.md,mcp.json,
   schemas,scripts}` + staged sources `new-skills/ new-rules/ rewritten-skills/ round2-skills/`
   + `build.sh` + `~/workspace/hackathon-plugin/fix27/verify27.py`.
6. **Classification.** A hit counts as a LIVE dispatch only if it is imperative / a path
   reference / a glob that routes to the rule (e.g. 'Rules: `rules/react-patterns.mdc`',
   'see rules/typescript-patterns.mdc', 'refer to the `rules/arkts-*.mdc` rule files', an
   'extends [x.mdc](x.mdc)' link, a 'per `rules/common-testing.mdc`' citation). These do NOT
   count: the generated `call-map.md` inventory (see §4), `build.sh` patch text (build-time,
   see §6), `verify27.py` allow-list entries (verifier bookkeeping, see §5), prose history
   ('was cut', 'is not used'), and pointers *from* a rule *to* a cut skill (OWED-11/M7 — the
   reverse direction; deleting the rule deletes the pointer too).
7. **Kept-stack glob test.** Criterion (c): a CUT candidate's globs must not match files in a
   hackathon build of the kept stack (Next.js/React + TypeScript frontend, FastAPI/Python
   backend, Expo/React Native mobile path). Kept-stack file types checked: `.ts/.tsx/.js/.jsx`,
   `.py`, `.css/.scss/.html`, `pages/` (Next.js Pages Router), `AndroidManifest.xml`, `Info.plist`
   (Expo prebuild output), `*.test.ts/*.spec.ts` (Vitest/Jest).

### Method limits (same blind spot as the fix #27 skill inventory)

- Cursor loads a non-alwaysApply rule by **glob match with no textual reference**, so a rule
  with zero dispatches can still load whenever a matching file is open — that is exactly what
  criterion (c) guards, and why the 7 NEEDS-DECISION files are not CUT on dispatches alone.
- Cursor/agents can also route by a rule file's **description** with no textual reference;
  that cannot be detected by grep. The 68 CUT files all have language-specific descriptions
  for stacks with no kept consumer, so description-routing to them from a kept-stack build is
  not a live path in practice, but it is not provable from text alone.

## §1 — The alwaysApply rules: 12, not 9 (correction to the task brief)

The brief said 'the 9 alwaysApply rules and hackathon-mode.mdc'. The frontmatter says
otherwise — verified by `grep -l 'alwaysApply: true' *.mdc` (12 files):

| # | File | Frontmatter |
|---|---|---|
| 1 | `common-agents.mdc` | `alwaysApply: true`, globs: (none) |
| 2 | `common-code-review.mdc` | `alwaysApply: true`, globs: (none) |
| 3 | `common-coding-style.mdc` | `alwaysApply: true`, globs: (none) |
| 4 | `common-development-workflow.mdc` | `alwaysApply: true`, globs: (none) |
| 5 | `common-git-workflow.mdc` | `alwaysApply: true`, globs: (none) |
| 6 | `common-hooks.mdc` | `alwaysApply: true`, globs: (none) |
| 7 | `common-patterns.mdc` | `alwaysApply: true`, globs: (none) |
| 8 | `common-performance.mdc` | `alwaysApply: true`, globs: (none) |
| 9 | `common-security.mdc` | `alwaysApply: true`, globs: (none) |
| 10 | `common-testing.mdc` | `alwaysApply: true`, globs: (none) |
| 11 | `hackathon-mode.mdc` | `alwaysApply: true`, globs: (none) |
| 12 | `ponytail.mdc` | `alwaysApply: true`, globs: (none) |

Why the brief said 9: `rules/hackathon-mode.mdc:27` names nine ECC alwaysApply rules in a
parenthetical — '(testing, development workflow, coding style, git workflow, security, patterns,
performance, common-agents, hooks)' — and then cites code review separately ('code review
applies per rules/common-code-review.mdc'). 9 named + code-review = the 10 `common-*` files.
`ponytail.mdc` (empty `globs:`, `alwaysApply: true`) is the 12th. **All 12 are NEVER CUT.**
Note `ponytail.mdc` has no textual dispatch anywhere (grep for `ponytail.mdc`, `rules/ponytail`,
and bare `ponytail` returned only the README.md:13 counts line) — it survives on alwaysApply
alone, which is the correct reason: it is the always-on lean-code-discipline rule.

## §2 — Family summary

| Family | Files | NEVER CUT | KEEP | CUT | NEEDS-DECISION |
|---|---|---|---|---|---|
| angular | 5 | 0 | 0 | 3 | 2 |
| arkts | 5 | 0 | 5 | 0 | 0 |
| common | 10 | 10 | 0 | 0 | 0 |
| cpp | 5 | 0 | 0 | 5 | 0 |
| csharp | 5 | 0 | 0 | 5 | 0 |
| dart | 5 | 0 | 0 | 4 | 1 |
| fsharp | 5 | 0 | 0 | 5 | 0 |
| golang | 5 | 0 | 0 | 5 | 0 |
| java | 5 | 0 | 0 | 5 | 0 |
| kotlin | 5 | 0 | 0 | 5 | 0 |
| nuxt | 5 | 0 | 0 | 2 | 3 |
| perl | 5 | 0 | 0 | 5 | 0 |
| php | 5 | 0 | 0 | 5 | 0 |
| ponytail | 1 | 1 | 0 | 0 | 0 |
| python | 6 | 0 | 6 | 0 | 0 |
| react | 13 | 0 | 13 | 0 | 0 |
| react-native | 0 | 0 | 0 | 0 | 0 |
| ruby | 5 | 0 | 0 | 5 | 0 |
| rust | 5 | 0 | 0 | 5 | 0 |
| swift | 5 | 0 | 0 | 5 | 0 |
| typescript | 5 | 0 | 5 | 0 | 0 |
| vue | 5 | 0 | 0 | 4 | 1 |
| web | 7 | 0 | 7 | 0 | 0 |
| hackathon-mode | 1 | 1 | 0 | 0 | 0 |
| **Total** | **123** | **12** | **36** | **68** | **7** |

## §3 — Full per-file table (123 rows)

Columns: file | family | alwaysApply? | globs | live dispatches found (file:line or NONE) | kept-skill link? | verdict + reason.
Globs are quoted verbatim from frontmatter; `—` means no globs key (alwaysApply files).
'NONE' in dispatches means: the literal-path grep, the bare-name grep, and the family-glob grep
all returned 0 hits outside `call-map.md`, `build.sh`, and `verify27.py` (see §4–§6 for what
those three sources contain and why they do not count).

| file | family | alwaysApply? | globs | live dispatches | kept-skill link? | verdict |
|---|---|---|---|---|---|---|
| `angular-coding-style.mdc` | angular | — (no key) | `**/*.component.ts`, `**/*.component.html`, `**/*.service.ts`, `**/*.directive.ts`, `**/*.pipe.ts`, `**/*.guard.ts`, `**/*.resolver.ts` | NONE | None. angular-developer CUT in fix #27 (skill-inventory.md). | **CUT** — Zero dispatches; no kept skill serves Angular; globs are Angular-convention filenames (*.component.ts, *.service.ts, *.module.ts, *.store.ts, *.routes.ts, *.interceptor.ts, *.directive.ts, *.pipe.ts, *.guard.ts, *.resolver.ts, *.component.html) that cannot occur in a Next.js/FastAPI/Expo build. |
| `angular-hooks.mdc` | angular | — (no key) | `**/*.component.ts`, `**/*.component.html`, `**/*.service.ts`, `**/*.directive.ts`, `**/*.pipe.ts` | NONE | None. angular-developer CUT in fix #27 (skill-inventory.md). | **NEEDS-DECISION** — Globs include **/*.spec.ts, which CAN match a kept-stack test file (Jest/Vitest default testMatch includes *.spec.ts). Angular-only otherwise; needs a decision on whether to cut or narrow the globs first. |
| `angular-patterns.mdc` | angular | — (no key) | `**/*.component.ts`, `**/*.component.html`, `**/*.service.ts`, `**/*.store.ts` | NONE | None. angular-developer CUT in fix #27 (skill-inventory.md). | **CUT** — Zero dispatches; no kept skill serves Angular; globs are Angular-convention filenames (*.component.ts, *.service.ts, *.module.ts, *.store.ts, *.routes.ts, *.interceptor.ts, *.directive.ts, *.pipe.ts, *.guard.ts, *.resolver.ts, *.component.html) that cannot occur in a Next.js/FastAPI/Expo build. |
| `angular-security.mdc` | angular | — (no key) | `**/*.component.ts`, `**/*.component.html`, `**/*.service.ts` | NONE | None. angular-developer CUT in fix #27 (skill-inventory.md). | **CUT** — Zero dispatches; no kept skill serves Angular; globs are Angular-convention filenames (*.component.ts, *.service.ts, *.module.ts, *.store.ts, *.routes.ts, *.interceptor.ts, *.directive.ts, *.pipe.ts, *.guard.ts, *.resolver.ts, *.component.html) that cannot occur in a Next.js/FastAPI/Expo build. |
| `angular-testing.mdc` | angular | — (no key) | `**/*.spec.ts` | NONE | None. angular-developer CUT in fix #27 (skill-inventory.md). | **NEEDS-DECISION** — Globs **/*.spec.ts + **/*.test.ts CAN match kept-stack test files (Vitest/Jest .test.ts). Needs a decision: cut, or narrow globs to Angular-only first. |
| `arkts-coding-style.mdc` | arkts | — (no key) | `**/*.ets`, `**/*.ts`, `**/module.json5`, `**/oh-package.json5` | NONE | Kept agent ecc-harmonyos-app-resolver (HarmonyOS resolver). No kept skill. | **KEEP** — Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs include **/*.ts which matches kept-stack files. |
| `arkts-hooks.mdc` | arkts | — (no key) | `**/*.ets`, `**/*.ts`, `**/module.json5` | NONE | Kept agent ecc-harmonyos-app-resolver (HarmonyOS resolver). No kept skill. | **KEEP** — Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs include **/*.ts which matches kept-stack files. |
| `arkts-patterns.mdc` | arkts | — (no key) | `**/*.ets` | NONE | Kept agent ecc-harmonyos-app-resolver (HarmonyOS resolver). No kept skill. | **KEEP** — Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs include **/*.ts which matches kept-stack files. |
| `arkts-security.mdc` | arkts | — (no key) | `**/*.ets`, `**/*.ts` | NONE | Kept agent ecc-harmonyos-app-resolver (HarmonyOS resolver). No kept skill. | **KEEP** — Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs include **/*.ts which matches kept-stack files. |
| `arkts-testing.mdc` | arkts | — (no key) | `**/*.ets`, `**/*.ts` | NONE | Kept agent ecc-harmonyos-app-resolver (HarmonyOS resolver). No kept skill. | **KEEP** — Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs include **/*.ts which matches kept-stack files. |
| `common-agents.mdc` | common | true | — | rules/common-code-review.mdc:128 (cross-link 'Agent delegation'); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-code-review.mdc` | common | true | — | rules/hackathon-mode.mdc:27 + staged new-rules/hackathon-mode.mdc:27 ('code review applies per rules/common-code-review.mdc'); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-coding-style.mdc` | common | true | — | 15x 'extends common-coding-style.mdc' backlinks from *-coding-style.mdc (e.g. rules/angular-coding-style.mdc:14, rules/react-coding-style.mdc:12); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-development-workflow.mdc` | common | true | — | skills/orch-pipeline/SKILL.md:63,113 ('per rules/common-development-workflow.mdc'); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-git-workflow.mdc` | common | true | — | rules/common-code-review.mdc:127 (cross-link 'Commit standards'); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-hooks.mdc` | common | true | — | 14x 'extends common-hooks.mdc' backlinks from *-hooks.mdc (e.g. rules/angular-hooks.mdc:12, rules/web-hooks.mdc:13); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-patterns.mdc` | common | true | — | 17x 'extends common-patterns.mdc' backlinks from *-patterns.mdc + react-hooks.mdc:14 + web-design-quality.mdc:13; alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-performance.mdc` | common | true | — | rules/react-native-performance.mdc:8, rules/web-performance.mdc:13, rules/web-testing.mdc:36; alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-security.mdc` | common | true | — | skills/orch-pipeline/SKILL.md:105 ('Per rules/common-security.mdc'); rules/hackathon-mode.mdc:23 + new-rules/hackathon-mode.mdc:23; 18x 'extends common-security.mdc' backlinks; alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `common-testing.mdc` | common | true | — | skills/orch-pipeline/SKILL.md:123 ('coverage >= 80% per rules/common-testing.mdc'); 18x 'extends common-testing.mdc' backlinks; alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `cpp-coding-style.mdc` | cpp | — (no key) | `**/*.cpp`, `**/*.hpp`, `**/*.cc`, `**/*.hh`, `**/*.cxx`, `**/*.h` | NONE | None. cpp-coding-standards, cpp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C++; globs **/*.cpp/*.hpp/*.cc/*.hh/*.cxx/*.h + CMakeLists.txt cannot match kept-stack files. |
| `cpp-hooks.mdc` | cpp | — (no key) | `**/*.cpp`, `**/*.hpp`, `**/*.cc`, `**/*.hh`, `**/*.cxx`, `**/*.h` | NONE | None. cpp-coding-standards, cpp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C++; globs **/*.cpp/*.hpp/*.cc/*.hh/*.cxx/*.h + CMakeLists.txt cannot match kept-stack files. |
| `cpp-patterns.mdc` | cpp | — (no key) | `**/*.cpp`, `**/*.hpp`, `**/*.cc`, `**/*.hh`, `**/*.cxx`, `**/*.h` | NONE | None. cpp-coding-standards, cpp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C++; globs **/*.cpp/*.hpp/*.cc/*.hh/*.cxx/*.h + CMakeLists.txt cannot match kept-stack files. |
| `cpp-security.mdc` | cpp | — (no key) | `**/*.cpp`, `**/*.hpp`, `**/*.cc`, `**/*.hh`, `**/*.cxx`, `**/*.h` | NONE | None. cpp-coding-standards, cpp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C++; globs **/*.cpp/*.hpp/*.cc/*.hh/*.cxx/*.h + CMakeLists.txt cannot match kept-stack files. |
| `cpp-testing.mdc` | cpp | — (no key) | `**/*.cpp`, `**/*.hpp`, `**/*.cc`, `**/*.hh`, `**/*.cxx`, `**/*.h` | NONE | None. cpp-coding-standards, cpp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C++; globs **/*.cpp/*.hpp/*.cc/*.hh/*.cxx/*.h + CMakeLists.txt cannot match kept-stack files. |
| `csharp-coding-style.mdc` | csharp | — (no key) | `**/*.cs` | NONE | None. dotnet-patterns, csharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C#/.NET; globs **/*.cs/*.csx/*.csproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `csharp-hooks.mdc` | csharp | — (no key) | `**/*.cs`, `**/*.csx`, `**/*.csproj`, `**/*.sln`, `**/Directory.Build.props` | NONE | None. dotnet-patterns, csharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C#/.NET; globs **/*.cs/*.csx/*.csproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `csharp-patterns.mdc` | csharp | — (no key) | `**/*.cs` | NONE | None. dotnet-patterns, csharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C#/.NET; globs **/*.cs/*.csx/*.csproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `csharp-security.mdc` | csharp | — (no key) | `**/*.cs`, `**/*.csx`, `**/*.csproj` | NONE | None. dotnet-patterns, csharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C#/.NET; globs **/*.cs/*.csx/*.csproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `csharp-testing.mdc` | csharp | — (no key) | `**/*.cs`, `**/*.csx` | NONE | None. dotnet-patterns, csharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves C#/.NET; globs **/*.cs/*.csx/*.csproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `dart-coding-style.mdc` | dart | — (no key) | `**/*.dart`, `**/pubspec.yaml` | NONE | None. dart-flutter-patterns, flutter-dart-code-review CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Dart/Flutter; globs **/*.dart + pubspec.yaml + analysis_options.yaml cannot match kept-stack files. |
| `dart-hooks.mdc` | dart | — (no key) | `**/*.dart`, `**/pubspec.yaml` | NONE | None. dart-flutter-patterns, flutter-dart-code-review CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Dart/Flutter; globs **/*.dart + pubspec.yaml + analysis_options.yaml cannot match kept-stack files. |
| `dart-patterns.mdc` | dart | — (no key) | `**/*.dart` | NONE | None. dart-flutter-patterns, flutter-dart-code-review CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Dart/Flutter; globs **/*.dart + pubspec.yaml + analysis_options.yaml cannot match kept-stack files. |
| `dart-security.mdc` | dart | — (no key) | `**/*.dart`, `**/pubspec.yaml`, `**/AndroidManifest.xml` | NONE | None. dart-flutter-patterns, flutter-dart-code-review CUT in fix #27. | **NEEDS-DECISION** — Globs include **/AndroidManifest.xml and **/Info.plist, which DO occur in an Expo React Native build (kept mobile path via mobile-ship / react-native-patterns). Needs a decision: cut, or narrow globs to *.dart-only first. |
| `dart-testing.mdc` | dart | — (no key) | `**/*.dart`, `**/pubspec.yaml` | NONE | None. dart-flutter-patterns, flutter-dart-code-review CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Dart/Flutter; globs **/*.dart + pubspec.yaml + analysis_options.yaml cannot match kept-stack files. |
| `fsharp-coding-style.mdc` | fsharp | — (no key) | `**/*.fs` | NONE | None. fsharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves F#; globs **/*.fs/*.fsx/*.fsproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `fsharp-hooks.mdc` | fsharp | — (no key) | `**/*.fs`, `**/*.fsx`, `**/*.fsproj`, `**/*.sln`, `**/*.slnx`, `**/Directory.Build.props` | NONE | None. fsharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves F#; globs **/*.fs/*.fsx/*.fsproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `fsharp-patterns.mdc` | fsharp | — (no key) | `**/*.fs` | NONE | None. fsharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves F#; globs **/*.fs/*.fsx/*.fsproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `fsharp-security.mdc` | fsharp | — (no key) | `**/*.fs`, `**/*.fsx`, `**/*.fsproj` | NONE | None. fsharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves F#; globs **/*.fs/*.fsx/*.fsproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `fsharp-testing.mdc` | fsharp | — (no key) | `**/*.fs`, `**/*.fsx` | NONE | None. fsharp-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves F#; globs **/*.fs/*.fsx/*.fsproj/*.sln + appsettings*.json cannot match kept-stack files. |
| `golang-coding-style.mdc` | golang | false | `**/*.go`, `**/go.mod`, `**/go.sum` | NONE | None. golang-patterns, golang-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Go; globs **/*.go + go.mod/go.sum cannot match kept-stack files. |
| `golang-hooks.mdc` | golang | false | `**/*.go`, `**/go.mod`, `**/go.sum` | NONE | None. golang-patterns, golang-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Go; globs **/*.go + go.mod/go.sum cannot match kept-stack files. |
| `golang-patterns.mdc` | golang | false | `**/*.go`, `**/go.mod`, `**/go.sum` | NONE | None. golang-patterns, golang-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Go; globs **/*.go + go.mod/go.sum cannot match kept-stack files. |
| `golang-security.mdc` | golang | false | `**/*.go`, `**/go.mod`, `**/go.sum` | NONE | None. golang-patterns, golang-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Go; globs **/*.go + go.mod/go.sum cannot match kept-stack files. |
| `golang-testing.mdc` | golang | false | `**/*.go`, `**/go.mod`, `**/go.sum` | NONE | None. golang-patterns, golang-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Go; globs **/*.go + go.mod/go.sum cannot match kept-stack files. |
| `hackathon-mode.mdc` | hackathon-mode | true | — | README.md:20,54; skills/ui-ux-pro-max/SKILL.md:318 ('see rules/hackathon-mode.mdc S5'); + bare 'hackathon-mode SN' refs in deploy-fast/SKILL.md:186, feature-expansion/SKILL.md:35,126,145,152, grill-me/SKILL.md:39,42, hackathon-pitch/SKILL.md:32; alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `java-coding-style.mdc` | java | — (no key) | — (empty) | NONE | None. java-coding-standards, jpa-patterns, springboot-*, quarkus-*, mybatis-patterns, tinystruct-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Java; globs **/*.java + pom.xml/build.gradle cannot match kept-stack files. |
| `java-hooks.mdc` | java | — (no key) | `**/*.java`, `**/pom.xml`, `**/build.gradle` | NONE | None. java-coding-standards, jpa-patterns, springboot-*, quarkus-*, mybatis-patterns, tinystruct-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Java; globs **/*.java + pom.xml/build.gradle cannot match kept-stack files. |
| `java-patterns.mdc` | java | — (no key) | — (empty) | NONE | None. java-coding-standards, jpa-patterns, springboot-*, quarkus-*, mybatis-patterns, tinystruct-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Java; globs **/*.java + pom.xml/build.gradle cannot match kept-stack files. |
| `java-security.mdc` | java | — (no key) | — (empty) | NONE | None. java-coding-standards, jpa-patterns, springboot-*, quarkus-*, mybatis-patterns, tinystruct-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Java; globs **/*.java + pom.xml/build.gradle cannot match kept-stack files. |
| `java-testing.mdc` | java | — (no key) | — (empty) | NONE | None. java-coding-standards, jpa-patterns, springboot-*, quarkus-*, mybatis-patterns, tinystruct-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Java; globs **/*.java + pom.xml/build.gradle cannot match kept-stack files. |
| `kotlin-coding-style.mdc` | kotlin | false | `**/*.kt`, `**/*.kts`, `**/build.gradle.kts` | NONE | None. kotlin-patterns, kotlin-testing, kotlin-coroutines-flows, kotlin-exposed-patterns, kotlin-ktor-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Kotlin; globs **/*.kt/*.kts + build.gradle.kts cannot match kept-stack files. |
| `kotlin-hooks.mdc` | kotlin | false | `**/*.kt`, `**/*.kts`, `**/build.gradle.kts` | NONE | None. kotlin-patterns, kotlin-testing, kotlin-coroutines-flows, kotlin-exposed-patterns, kotlin-ktor-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Kotlin; globs **/*.kt/*.kts + build.gradle.kts cannot match kept-stack files. |
| `kotlin-patterns.mdc` | kotlin | false | `**/*.kt`, `**/*.kts`, `**/build.gradle.kts` | NONE | None. kotlin-patterns, kotlin-testing, kotlin-coroutines-flows, kotlin-exposed-patterns, kotlin-ktor-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Kotlin; globs **/*.kt/*.kts + build.gradle.kts cannot match kept-stack files. |
| `kotlin-security.mdc` | kotlin | false | `**/*.kt`, `**/*.kts`, `**/build.gradle.kts` | NONE | None. kotlin-patterns, kotlin-testing, kotlin-coroutines-flows, kotlin-exposed-patterns, kotlin-ktor-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Kotlin; globs **/*.kt/*.kts + build.gradle.kts cannot match kept-stack files. |
| `kotlin-testing.mdc` | kotlin | false | `**/*.kt`, `**/*.kts`, `**/build.gradle.kts` | NONE | None. kotlin-patterns, kotlin-testing, kotlin-coroutines-flows, kotlin-exposed-patterns, kotlin-ktor-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Kotlin; globs **/*.kt/*.kts + build.gradle.kts cannot match kept-stack files. |
| `nuxt-coding-style.mdc` | nuxt | — (no key) | `**/nuxt.config.*`, `**/app.config.*`, `**/app.vue`, `**/pages/**`, `**/layouts/**` | NONE | None. nuxt4-patterns CUT in fix #27. | **NEEDS-DECISION** — Globs include **/pages/**, which DOES match a Next.js Pages Router project. Needs a decision: cut, or narrow globs to Nuxt-only paths first. |
| `nuxt-hooks.mdc` | nuxt | — (no key) | `**/nuxt.config.*`, `**/app.config.*`, `**/server/**/*.ts` | NONE | None. nuxt4-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Nuxt/Vue; globs are Nuxt-convention paths (nuxt.config.*, app.config.*, app.vue, *.vue, server/**/*.ts) that cannot match kept-stack files. |
| `nuxt-patterns.mdc` | nuxt | — (no key) | `**/nuxt.config.*`, `**/app.config.*`, `**/app.vue`, `**/server/**/*.ts`, `**/pages/**` | NONE | None. nuxt4-patterns CUT in fix #27. | **NEEDS-DECISION** — Globs include **/pages/** (Next.js Pages Router collision) and **/middleware/**. Needs a decision: cut, or narrow globs first. |
| `nuxt-security.mdc` | nuxt | — (no key) | `**/nuxt.config.*`, `**/app.config.*` | NONE | None. nuxt4-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Nuxt/Vue; globs are Nuxt-convention paths (nuxt.config.*, app.config.*, app.vue, *.vue, server/**/*.ts) that cannot match kept-stack files. |
| `nuxt-testing.mdc` | nuxt | — (no key) | `**/nuxt.config.*`, `**/server/**/*.ts`, `**/pages/**`, `**/layouts/**` | NONE | None. nuxt4-patterns CUT in fix #27. | **NEEDS-DECISION** — Globs include **/pages/** (Next.js Pages Router collision). Needs a decision: cut, or narrow globs first. |
| `perl-coding-style.mdc` | perl | — (no key) | `**/*.pl`, `**/*.pm`, `**/*.t`, `**/*.psgi` | NONE | None. perl-patterns, perl-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Perl; globs **/*.pl/*.pm/*.t/*.psgi/*.cgi cannot match kept-stack files. |
| `perl-hooks.mdc` | perl | — (no key) | `**/*.pl`, `**/*.pm`, `**/*.t`, `**/*.psgi` | NONE | None. perl-patterns, perl-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Perl; globs **/*.pl/*.pm/*.t/*.psgi/*.cgi cannot match kept-stack files. |
| `perl-patterns.mdc` | perl | — (no key) | `**/*.pl`, `**/*.pm`, `**/*.t`, `**/*.psgi` | NONE | None. perl-patterns, perl-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Perl; globs **/*.pl/*.pm/*.t/*.psgi/*.cgi cannot match kept-stack files. |
| `perl-security.mdc` | perl | — (no key) | `**/*.pl`, `**/*.pm`, `**/*.t`, `**/*.psgi` | NONE | None. perl-patterns, perl-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Perl; globs **/*.pl/*.pm/*.t/*.psgi/*.cgi cannot match kept-stack files. |
| `perl-testing.mdc` | perl | — (no key) | `**/*.pl`, `**/*.pm`, `**/*.t`, `**/*.psgi` | NONE | None. perl-patterns, perl-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Perl; globs **/*.pl/*.pm/*.t/*.psgi/*.cgi cannot match kept-stack files. |
| `php-coding-style.mdc` | php | false | `**/*.php`, `**/composer.json` | NONE | None. laravel-patterns, laravel-tdd, laravel-verification, laravel-plugin-discovery CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves PHP; globs **/*.php + composer.json/phpstan/psalm/phpunit configs cannot match kept-stack files. |
| `php-hooks.mdc` | php | false | `**/*.php`, `**/composer.json`, `**/phpstan.neon`, `**/phpstan.neon.dist`, `**/psalm.xml` | NONE | None. laravel-patterns, laravel-tdd, laravel-verification, laravel-plugin-discovery CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves PHP; globs **/*.php + composer.json/phpstan/psalm/phpunit configs cannot match kept-stack files. |
| `php-patterns.mdc` | php | false | `**/*.php`, `**/composer.json` | NONE | None. laravel-patterns, laravel-tdd, laravel-verification, laravel-plugin-discovery CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves PHP; globs **/*.php + composer.json/phpstan/psalm/phpunit configs cannot match kept-stack files. |
| `php-security.mdc` | php | false | `**/*.php`, `**/composer.lock`, `**/composer.json` | NONE | None. laravel-patterns, laravel-tdd, laravel-verification, laravel-plugin-discovery CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves PHP; globs **/*.php + composer.json/phpstan/psalm/phpunit configs cannot match kept-stack files. |
| `php-testing.mdc` | php | false | `**/*.php`, `**/phpunit.xml`, `**/phpunit.xml.dist`, `**/composer.json` | NONE | None. laravel-patterns, laravel-tdd, laravel-verification, laravel-plugin-discovery CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves PHP; globs **/*.php + composer.json/phpstan/psalm/phpunit configs cannot match kept-stack files. |
| `ponytail.mdc` | ponytail | true | — | NONE (no textual dispatch; README.md:13 mentions it only in the counts line); alwaysApply | n/a - alwaysApply. | **NEVER CUT** — alwaysApply: true (verified in frontmatter) - out of scope for fix #28 by task constraint. |
| `python-coding-style.mdc` | python | false | `**/*.py`, `**/*.pyi` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `python-fastapi.mdc` | python | — (no key) | `**/app/**/*.py`, `**/fastapi/**/*.py` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `python-hooks.mdc` | python | false | `**/*.py`, `**/*.pyi` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `python-patterns.mdc` | python | false | `**/*.py`, `**/*.pyi` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `python-security.mdc` | python | false | `**/*.py`, `**/*.pyi` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `python-testing.mdc` | python | false | `**/*.py`, `**/*.pyi` | NONE | Kept skills python-patterns, python-testing, fastapi-patterns; kept agents ecc-python-reviewer, ecc-fastapi-reviewer; kept commands python-review, fastapi-review. NOTE: none of them textually references a python-*.mdc path - the link is stack-fit, not a dispatch. | **KEEP** — Globs **/*.py match the kept FastAPI backend; kept Python/FastAPI skills+agents+commands serve the language. Zero literal dispatches, but criterion (c) fails so not a CUT candidate. |
| `react-coding-style.mdc` | react | — (no key) | `**/*.tsx`, `**/*.jsx`, `**/components/**/*.ts`, `**/components/**/*.js`, `**/hooks/**/*.ts` | agents/ecc-react-build-resolver.md:212; agents/ecc-react-reviewer.md:160; commands/react-build.md:187 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-hooks.mdc` | react | — (no key) | `**/*.tsx`, `**/*.jsx`, `**/hooks/**/*.ts`, `**/hooks/**/*.js`, `**/use-*.ts` | agents/ecc-react-reviewer.md:160; skills/react-patterns/SKILL.md:56; rules/react-coding-style.mdc:82; rules/react-patterns.mdc:12 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-accessibility.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9 (names all 8 RN rules); rules/react-patterns.mdc:189 (names all 8 RN rules) | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-coding-style.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-hooks.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-patterns.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-performance.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-production-readiness.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-security.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-native-testing.mdc` | react | — (no key) | `**/*.ts` | skills/react-native-patterns/SKILL.md:9; rules/react-patterns.mdc:189 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-patterns.mdc` | react | — (no key) | `**/*.tsx`, `**/*.jsx`, `**/components/**/*.ts`, `**/components/**/*.js`, `**/app/**/*.tsx` | agents/ecc-react-build-resolver.md:212; agents/ecc-react-reviewer.md:160; commands/react-build.md:187 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-security.mdc` | react | — (no key) | `**/*.tsx`, `**/*.jsx`, `**/components/**/*.ts`, `**/app/**/*.ts` | agents/ecc-react-reviewer.md:160 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `react-testing.mdc` | react | — (no key) | `**/*.test.tsx`, `**/*.test.jsx`, `**/*.spec.tsx`, `**/*.spec.jsx`, `**/__tests__/**/*.ts` | agents/ecc-react-reviewer.md:160; commands/react-test.md:16,264; skills/react-testing/SKILL.md:358 | Kept skills react-patterns, react-testing, react-performance, frontend-patterns, frontend-a11y; kept agents ecc-react-build-resolver, ecc-react-reviewer; kept commands react-build, react-review, react-test. | **KEEP** — Live dispatch from kept agents/commands/skills (see dispatches column); globs match the kept Next.js frontend. |
| `ruby-coding-style.mdc` | ruby | — (no key) | `**/*.rb`, `**/*.rake`, `**/Gemfile`, `**/*.gemspec` | NONE | None. rails-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Ruby/Rails; globs **/*.rb/*.rake + Gemfile/config.ru/config/routes.rb cannot match kept-stack files. |
| `ruby-hooks.mdc` | ruby | — (no key) | `**/*.rb`, `**/*.rake`, `**/Gemfile`, `**/Gemfile.lock` | NONE | None. rails-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Ruby/Rails; globs **/*.rb/*.rake + Gemfile/config.ru/config/routes.rb cannot match kept-stack files. |
| `ruby-patterns.mdc` | ruby | — (no key) | `**/*.rb`, `**/*.rake`, `**/Gemfile`, `**/app/**/*.erb` | NONE | None. rails-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Ruby/Rails; globs **/*.rb/*.rake + Gemfile/config.ru/config/routes.rb cannot match kept-stack files. |
| `ruby-security.mdc` | ruby | — (no key) | `**/*.rb`, `**/*.rake`, `**/Gemfile`, `**/Gemfile.lock`, `**/config/routes.rb` | NONE | None. rails-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Ruby/Rails; globs **/*.rb/*.rake + Gemfile/config.ru/config/routes.rb cannot match kept-stack files. |
| `ruby-testing.mdc` | ruby | — (no key) | `**/*.rb`, `**/*.rake`, `**/Gemfile`, `**/test/**/*.rb`, `**/spec/**/*.rb` | NONE | None. rails-patterns CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Ruby/Rails; globs **/*.rb/*.rake + Gemfile/config.ru/config/routes.rb cannot match kept-stack files. |
| `rust-coding-style.mdc` | rust | — (no key) | — (empty) | NONE | None. rust-patterns, rust-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Rust; globs **/*.rs + Cargo.toml cannot match kept-stack files. |
| `rust-hooks.mdc` | rust | — (no key) | `**/*.rs` | NONE | None. rust-patterns, rust-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Rust; globs **/*.rs + Cargo.toml cannot match kept-stack files. |
| `rust-patterns.mdc` | rust | — (no key) | — (empty) | NONE | None. rust-patterns, rust-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Rust; globs **/*.rs + Cargo.toml cannot match kept-stack files. |
| `rust-security.mdc` | rust | — (no key) | — (empty) | NONE | None. rust-patterns, rust-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Rust; globs **/*.rs + Cargo.toml cannot match kept-stack files. |
| `rust-testing.mdc` | rust | — (no key) | — (empty) | NONE | None. rust-patterns, rust-testing CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Rust; globs **/*.rs + Cargo.toml cannot match kept-stack files. |
| `swift-coding-style.mdc` | swift | false | `**/*.swift`, `**/Package.swift` | NONE | None. No Swift skill survived fix #27; build.sh patches naming swift rules target removed agents (see S6). | **CUT** — Zero dispatches; no kept skill serves Swift; globs **/*.swift + Package.swift cannot match kept-stack files. |
| `swift-hooks.mdc` | swift | false | `**/*.swift`, `**/Package.swift` | NONE | None. No Swift skill survived fix #27; build.sh patches naming swift rules target removed agents (see S6). | **CUT** — Zero dispatches; no kept skill serves Swift; globs **/*.swift + Package.swift cannot match kept-stack files. |
| `swift-patterns.mdc` | swift | false | `**/*.swift`, `**/Package.swift` | NONE | None. No Swift skill survived fix #27; build.sh patches naming swift rules target removed agents (see S6). | **CUT** — Zero dispatches; no kept skill serves Swift; globs **/*.swift + Package.swift cannot match kept-stack files. |
| `swift-security.mdc` | swift | false | `**/*.swift`, `**/Package.swift` | NONE | None. No Swift skill survived fix #27; build.sh patches naming swift rules target removed agents (see S6). | **CUT** — Zero dispatches; no kept skill serves Swift; globs **/*.swift + Package.swift cannot match kept-stack files. |
| `swift-testing.mdc` | swift | false | `**/*.swift`, `**/Package.swift` | NONE | None. No Swift skill survived fix #27; build.sh patches naming swift rules target removed agents (see S6). | **CUT** — Zero dispatches; no kept skill serves Swift; globs **/*.swift + Package.swift cannot match kept-stack files. |
| `typescript-coding-style.mdc` | typescript | false | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` | skills/typescript-patterns/SKILL.md:10 ('see the TypeScript rules - rules/typescript-coding-style.mdc and rules/typescript-patterns.mdc'); rules/react-coding-style.mdc:12 (extends) | Kept skill typescript-patterns; kept agent ecc-typescript-reviewer. | **KEEP** — Live dispatch from kept skill typescript-patterns + react-* 'extends' backlinks; globs **/*.ts(x) match the kept frontend. |
| `typescript-hooks.mdc` | typescript | false | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` | NONE literal; covered by family glob skills/typescript-patterns/SKILL.md:590 ('rules/typescript-*.mdc') | Kept skill typescript-patterns; kept agent ecc-typescript-reviewer. | **KEEP** — Live dispatch from kept skill typescript-patterns + react-* 'extends' backlinks; globs **/*.ts(x) match the kept frontend. |
| `typescript-patterns.mdc` | typescript | false | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` | skills/typescript-patterns/SKILL.md:10; rules/react-hooks.mdc:14 (extends); rules/react-patterns.mdc:12 (extends) | Kept skill typescript-patterns; kept agent ecc-typescript-reviewer. | **KEEP** — Live dispatch from kept skill typescript-patterns + react-* 'extends' backlinks; globs **/*.ts(x) match the kept frontend. |
| `typescript-security.mdc` | typescript | false | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` | rules/react-security.mdc:11 (extends) | Kept skill typescript-patterns; kept agent ecc-typescript-reviewer. | **KEEP** — Live dispatch from kept skill typescript-patterns + react-* 'extends' backlinks; globs **/*.ts(x) match the kept frontend. |
| `typescript-testing.mdc` | typescript | false | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx` | rules/react-testing.mdc:12 (extends) | Kept skill typescript-patterns; kept agent ecc-typescript-reviewer. | **KEEP** — Live dispatch from kept skill typescript-patterns + react-* 'extends' backlinks; globs **/*.ts(x) match the kept frontend. |
| `vue-coding-style.mdc` | vue | — (no key) | — (empty) | NONE | None. vue-patterns, ui-to-vue CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Vue; globs **/*.vue only - cannot match kept-stack files. |
| `vue-hooks.mdc` | vue | — (no key) | `**/*.vue`, `**/*.ts` | NONE | None. vue-patterns, ui-to-vue CUT in fix #27. | **NEEDS-DECISION** — Globs include **/*.ts and **/*.tsx, which match EVERY TypeScript file in the kept Next.js frontend - the broadest collision in this inventory. Needs a decision: cut, or narrow globs to *.vue-only first. |
| `vue-patterns.mdc` | vue | — (no key) | — (empty) | NONE | None. vue-patterns, ui-to-vue CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Vue; globs **/*.vue only - cannot match kept-stack files. |
| `vue-security.mdc` | vue | — (no key) | — (empty) | NONE | None. vue-patterns, ui-to-vue CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Vue; globs **/*.vue only - cannot match kept-stack files. |
| `vue-testing.mdc` | vue | — (no key) | — (empty) | NONE | None. vue-patterns, ui-to-vue CUT in fix #27. | **CUT** — Zero dispatches; no kept skill serves Vue; globs **/*.vue only - cannot match kept-stack files. |
| `web-coding-style.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-design-quality.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-hooks.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | rules/nuxt-hooks.mdc:18 only (old-form pointer 'mirror web/hooks.md' from a CUT candidate - not a keeping dispatch) | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-patterns.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-performance.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-security.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |
| `web-testing.mdc` | web | — (no key) | `**/*.css`, `**/*.scss`, `**/*.sass`, `**/*.less`, `**/*.html`, `**/*.tsx`, `**/*.jsx`, `**/*.vue` | NONE | No single owning skill. Generic frontend; kept design skills ui-ux-pro-max, design-taste-frontend, less-flat-ui, frontend-patterns are adjacent, not owners. | **KEEP** — Globs include **/*.tsx, **/*.jsx, **/*.css, **/*.html - they match kept-stack files, so criterion (c) fails; cutting would change which rules load on every frontend file. Zero literal dispatches (only the nuxt-hooks:18 pointer from a CUT candidate). |

## §4 — What the three excluded sources actually contain (and why they do not count)

### 4a. `skills/orchestrate/references/call-map.md` (generated inventory, not a dispatch)

Every rule appears in the call-map, but only as a **self-entry**: each rule stem has a row
whose only file is its own path, tagged `[struct-rule-globs]` (or `[struct-rule-always]` for
the 12 alwaysApply files), e.g. call-map.md:189 `| \`angular-coding-style\` |
rules/angular-coding-style.mdc [struct-rule-globs] | always-on (rule) |`. That row records that
the file *exists* and loads by glob — it is not a dispatch *to* the file, and it exists for
every rule including the ones nothing references. The `common-*` rows additionally list the
'extends common-X.mdc' backlinks — those are references *from* a language rule *to* a common
rule (the reverse direction), already counted in §3 for the common files. No call-map row for
a kept skill/agent/command lists a CUT-candidate rule file as a [strong] reference.
The staged copy `new-skills/orchestrate/references/call-map.md` is identical in this respect.

### 4b. `build.sh` (build-time patch text, not a runtime dispatch)

`build.sh` names rule files in two ways: (i) patch calls targeting a rule file
(e.g. `qc_patch(f"{base}/rules/angular-hooks.mdc", …)` at line 8482) and (ii) patch *content*
strings that rewrite a reference into its `rules/<fam>-<kind>.mdc` form (e.g. lines 1412–1424
rewrite `ruby/coding-style` → `rules/ruby-coding-style.mdc` inside `agents/ecc-ruby-reviewer.md`).
Neither is a live dispatch: a patch target is a file the build *edits*, and patch content is
text the build *writes*. The ruby/swift cases prove the point — their patch targets
(`agents/ecc-ruby-reviewer.md`, `agents/ecc-swift-build-resolver.md`,
`agents/ecc-swift-reviewer.md`; build.sh:1405,1431,1449) are **absent from the built tree**
(removed in fix #27), and the built tree contains zero references to `ruby-*.mdc` or
`swift-*.mdc`. Build.sh patch calls are, however, an **implementation constraint** (see §6):
61 distinct rule files are named in build.sh, including 21 CUT/NEEDS-DECISION files — the
implementation step must remove/retarget those patch calls or the rebuild breaks.

### 4c. `verify27.py` (verifier bookkeeping, not a dispatch)

- **Counts check** (verify27.py:269–275): asserts exactly `(67 skills, 45 agents, 123 rules,
  55 commands)`. Cutting any rule breaks this check until the verifier is updated (see §5).
- **Token reads**: `NOCOAUTHOR_F27` in `rules/common-git-workflow.mdc` (:366–367, :460–461),
  `DEFER3_F27` / `PALETTE-FIRST_F27` in `rules/hackathon-mode.mdc` (:372–373, :384–385) — all
  in NEVER CUT files.
- **B7 check** (:521): reads `rules/react-native-security.mdc` and asserts `security-scan` is
  not in it — a KEEP file, unaffected by the CUT list.
- **ALLOW_LIST** (:750–842): keys 31 rule files by the dangling `See skill: <cut-skill>`
  pointers inside them (OWED-11/M7, e.g. `rules/golang-patterns.mdc:44`,
  `rules/angular-patterns.mdc:249`, `rules/rust-testing.mdc:154`). These are pointers *from*
  the rule *to* a skill fix #27 cut — the reverse direction, not a dispatch to the rule.
  Cutting those rule files *removes* the dangling pointer, which is a side benefit. One
  exception stays live: `rules/react-patterns.mdc:194` points at CUT skill `accessibility`
  ('For accessibility see skills/accessibility/SKILL.md') and react-patterns.mdc is KEEP —
  that line needs a reword, not a cut (flagged for the fix #28 implementation step).

### 4d. Staged sources add nothing beyond the built tree

- `new-rules/hackathon-mode.mdc:23,27` mirrors the built `rules/hackathon-mode.mdc:23,27` exactly.
- `new-skills/orchestrate/references/call-map.md` mirrors the built call-map.
- `rewritten-skills/` and `round2-skills/` contain **zero** `.mdc` references
  (`grep -rn '\.mdc' rewritten-skills round2-skills` → 0 hits).
- `hackathon-ecc/manifests/` contains **zero** references to any rule file (`grep -rn 'rules/'`
  and `grep -rn '\.mdc'` → 0 hits). Note, separately, that `manifests/install-modules.json`
  still lists CUT *skills* (`skills/cpp-testing`, `skills/csharp-testing`, `skills/fsharp-testing`,
  `skills/golang-patterns`, `skills/golang-testing`, `skills/kotlin-patterns`, `skills/kotlin-testing`,
  `skills/perl-patterns`, `skills/perl-testing`, `skills/rust-patterns`, `skills/rust-testing`,
  `skills/vue-patterns`) — stale manifest entries from fix #27, unrelated to rules, flagged
  here so fix #28 can clean them in the same pass if in scope.
- `hackathon-ecc/hooks/`, `schemas/`, `scripts/`, `mcp.json` contain no rule-file references;
  the only `.mdc` hits in `scripts/` are generic extension handling (`cursor-project.js:19`,
  `gateguard-target-class.js:39`) and an unrelated scaffold path (`install-executor.js:136–137`).

## §5 — Verifier impact: what must change if the CUT list is applied

- `verify27.py:269–275` asserts 123 rules. After cutting 68, the count is 55 (or 48 if the 7
  NEEDS-DECISION files are also cut). The verifier (or its fix #28 successor) must be updated
  to the new count, and the README count line (README.md:13: '67 skills, 45 agents, 123 rules,
  and 55 commands') must be updated in the same step.
- The ALLOW_LIST entries for deleted rule files become dead entries (harmless, but should be
  pruned). Cutting the 68 CUT files orphans the entries for 25 rule files: golang-coding-style /
  patterns / testing, kotlin-coding-style / patterns / testing, angular-patterns, cpp-coding-style /
  patterns / security / testing, dart-patterns, java-coding-style / patterns / testing,
  nuxt-hooks / nuxt-security, perl-coding-style / patterns / testing, rust-coding-style / patterns /
  security / testing. If the 4 NEEDS-DECISION files in the allow-list (angular-testing,
  nuxt-coding-style / patterns / testing) are also cut, 4 more entries go dead — 29 of the 31
  rule files in the allow-list in total. The remaining two (react-patterns.mdc:194, KEEP, and
  hackathon-mode.mdc:37–38, NEVER CUT) stay live.
- No other verify27.py check names a CUT/NEEDS-DECISION file.

## §6 — Build impact: `build.sh` patch calls naming CUT/NEEDS-DECISION files

`grep -oE 'rules/[a-z0-9-]+\.mdc' build.sh | sort -u` → 61 distinct rule files named in
build.sh (patch targets + patch content). Of those, these 21 are CUT or NEEDS-DECISION and
their patch calls must be removed/retargeted by the implementation step:

- CUT (19): `dart-hooks.mdc`, `nuxt-hooks.mdc`, `ruby-hooks.mdc`, `rust-hooks.mdc`, `java-hooks.mdc`,
  `kotlin-hooks.mdc`, `golang-hooks.mdc`, `fsharp-hooks.mdc`, `csharp-hooks.mdc`, `php-hooks.mdc`,
  `perl-hooks.mdc`, `swift-hooks.mdc`, `swift-patterns.mdc`, `swift-testing.mdc`,
  `rust-security.mdc`, `golang-security.mdc`, `java-security.mdc`, `perl-security.mdc`,
  `php-security.mdc`.
- NEEDS-DECISION (2): `angular-hooks.mdc`, `vue-hooks.mdc`.
- KEEP files named in build.sh (no action): all `common-*`, `hackathon-mode.mdc`,
  `ponytail.mdc`, `python-hooks.mdc`, `python-security.mdc`, `typescript-hooks.mdc`,
  `react-patterns.mdc`, `react-security.mdc`, `react-testing.mdc`, `react-native-*.mdc`,
  `arkts-coding-style.mdc`, `arkts-hooks.mdc`, `arkts-security.mdc`, `web-hooks.mdc`,
  `web-design-quality.mdc`.
- Dead patch text already in build.sh (pre-existing, not caused by this cut): the ruby/swift
  patches at build.sh:1405–1466, 11299–11471, 15031 target agents removed in fix #27
  (`agents/ecc-ruby-reviewer.md`, `agents/ecc-swift-build-resolver.md`,
  `agents/ecc-swift-reviewer.md`); the implementation step should confirm whether those
  patch functions tolerate a missing target or fail the build.

## §7 — CUT-candidate summary (68 files)

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

Common evidence for every CUT row: (a) literal-path grep returned 0 hits outside
call-map.md/build.sh/verify27.py; (b) bare-name grep returned 0 hits outside those sources
(manifest `skills/<name>` hits are skill references, not rule references — see §4d);
(c) no kept skill/agent/command serves the language (fix #27 CUT list + kept
agents/commands census: the only kept language-specific agents are
ecc-harmonyos-app-resolver, ecc-python-reviewer, ecc-fastapi-reviewer,
ecc-react-build-resolver, ecc-react-reviewer, ecc-typescript-reviewer, ecc-pytorch-build-resolver;
the only kept language-specific commands are fastapi-review, python-review, react-build,
react-review, react-test); (d) globs cannot match kept-stack files (see per-row reasons).
Two extra notes: cutting the 68 CUT files also removes 25 of the 31 dangling OWED-11/M7
'See skill: <cut-skill>' pointers documented in verify27.py (cutting CUT + the 7
NEEDS-DECISION files removes 29 of 31; the two that stay are in KEEP file
react-patterns.mdc:194 — see §4c — and NEVER CUT file hackathon-mode.mdc:37–38); and the `rules/<lang>/` old-form references inside
build.sh's RULE_DIRS/RULE_FILES rewriter (build.sh:416–417) cover these families, so the
rewriter's family list should be pruned in the same pass to avoid rewriting references to
files that no longer exist.

## §8 — KEEP list (36 files) with reasons

| Family | Files | Reason (one line each in §3) |
|---|---|---|
| python (6) | python-coding-style, python-fastapi, python-hooks, python-patterns, python-security, python-testing | Globs `**/*.py` match the kept FastAPI backend; kept Python/FastAPI skills, agents, and commands serve the language. Zero literal dispatches — the only KEEP family with no textual dispatch at all; it survives on criterion (c) + kept-skill link. |
| typescript (5) | typescript-coding-style, typescript-hooks, typescript-patterns, typescript-security, typescript-testing | Live dispatch: typescript-patterns/SKILL.md:10 + family glob :590 `rules/typescript-*.mdc`; react-* rules extend the typescript rules. |
| react (5) | react-coding-style, react-hooks, react-patterns, react-security, react-testing | Live dispatch from kept agents (ecc-react-build-resolver:212, ecc-react-reviewer:160), commands (react-build:187, react-test:16,264, react-review:170 glob), and skills (react-patterns:56, react-testing:358). |
| react-native (8) | react-native-accessibility, react-native-coding-style, react-native-hooks, react-native-patterns, react-native-performance, react-native-production-readiness, react-native-security, react-native-testing | Live dispatch: react-native-patterns/SKILL.md:9 (names all 8) + react-patterns.mdc:189 (names all 8). |
| arkts (5) | arkts-coding-style, arkts-hooks, arkts-patterns, arkts-security, arkts-testing | Live family-glob dispatch from kept agent ecc-harmonyos-app-resolver.md:181 (`rules/arkts-*.mdc`); globs also include `**/*.ts`, which matches kept-stack files. |
| web (7) | web-coding-style, web-design-quality, web-hooks, web-patterns, web-performance, web-security, web-testing | Globs include `**/*.tsx`, `**/*.jsx`, `**/*.css`, `**/*.html` — they match kept-stack files, so criterion (c) fails. Zero literal dispatches; the only pointer is nuxt-hooks.mdc:18 (from a CUT candidate). |

## §9 — NEEDS-DECISION list (7 files) with reasons

- `angular-hooks.mdc` — Globs include **/*.spec.ts, which CAN match a kept-stack test file (Jest/Vitest default testMatch includes *.spec.ts). Angular-only otherwise; needs a decision on whether to cut or narrow the globs first.
- `angular-testing.mdc` — Globs **/*.spec.ts + **/*.test.ts CAN match kept-stack test files (Vitest/Jest .test.ts). Needs a decision: cut, or narrow globs to Angular-only first.
- `dart-security.mdc` — Globs include **/AndroidManifest.xml and **/Info.plist, which DO occur in an Expo React Native build (kept mobile path via mobile-ship / react-native-patterns). Needs a decision: cut, or narrow globs to *.dart-only first.
- `nuxt-coding-style.mdc` — Globs include **/pages/**, which DOES match a Next.js Pages Router project. Needs a decision: cut, or narrow globs to Nuxt-only paths first.
- `nuxt-patterns.mdc` — Globs include **/pages/** (Next.js Pages Router collision) and **/middleware/**. Needs a decision: cut, or narrow globs first.
- `nuxt-testing.mdc` — Globs include **/pages/** (Next.js Pages Router collision). Needs a decision: cut, or narrow globs first.
- `vue-hooks.mdc` — Globs include **/*.ts and **/*.tsx, which match EVERY TypeScript file in the kept Next.js frontend - the broadest collision in this inventory. Needs a decision: cut, or narrow globs to *.vue-only first.

Decision needed from the user/coordinator for each: cut as-is (accepting the glob collision),
or narrow its globs to the framework-only paths first and then cut. None of the 7 has a live
dispatch or a kept-skill link; the only blocker is the glob overlap with kept-stack files.

## §10 — Family-glob dispatches (for the record)

- **typescript**: Family glob: skills/typescript-patterns/SKILL.md:590 `rules/typescript-*.mdc` (covers all 5, incl. typescript-hooks.mdc which has no literal hit). skills/react-native-patterns/SKILL.md:11 also mentions 'ECC's existing `typescript/` rules' (loose family pointer).
- **react**: Family glob: commands/react-review.md:170 `rules/react-*.mdc` (covers all 5).
- **react-native**: Family dir ref: skills/react-native-patterns/SKILL.md:9 `rules/react-native/` ruleset (covers all 8).
- **arkts**: Family glob: agents/ecc-harmonyos-app-resolver.md:181 'refer to the `rules/arkts-*.mdc` rule files' (covers all 5) - LIVE dispatch from a kept agent.

Plus: `skills/react-native-patterns/SKILL.md:9` (`rules/react-native/` ruleset) and
`rules/react-patterns.mdc:183` (a *proposal* — 'propose a dedicated `rules/nextjs/` track' —
prose, not a dispatch; no nextjs rules exist).

## Appendix — grep log (commands run; all read-only)

```
cd ~/workspace/hackathon-plugin/fix27/scratch-repo/hackathon-ecc/rules
grep -l 'alwaysApply: true' *.mdc            # 12 files (see S1)
grep -l 'alwaysApply: false' *.mdc           # 30 files
# 81 files carry no alwaysApply key at all
for f in *.mdc; do awk 'NR==1 && /^---/{p=1;next} p && /^---/{exit} p' "$f"; done  # frontmatter dump, /tmp/rule-frontmatter.txt
cd ~/workspace/hackathon-plugin/fix27/scratch-repo
# literal-path hunt, per stem (123x):
grep -rn --exclude-dir=node_modules -e "${stem}\.mdc" -e "${fam}/${kind}\.md" -e "rules/${stem}" \
  hackathon-ecc/skills hackathon-ecc/agents hackathon-ecc/commands hackathon-ecc/rules \
  hackathon-ecc/hooks hackathon-ecc/manifests hackathon-ecc/README.md hackathon-ecc/mcp.json \
  hackathon-ecc/schemas hackathon-ecc/scripts new-skills new-rules rewritten-skills \
  round2-skills build.sh ~/workspace/hackathon-plugin/fix27/verify27.py
#  -> /tmp/rule-hunt.txt (123 sections); non-map/non-build/non-verify hits: 136 lines,
#     all accounted for in S3 (common-* backlinks, hackathon-mode, typescript/react/react-native)
# bare-name hunt, per stem (123x): grep -rnw <stem> <same scope>
#  -> only skill-name hits (python-patterns/python-testing in skills/manifests), the
#     portswigger URL for web-security, README + skill 'hackathon-mode SN' refs, and
#     stale CUT-skill entries in manifests/install-modules.json (see S4d)
# family-glob hunt:
grep -rn --exclude-dir=node_modules -e 'rules/[a-z-]*-\*.mdc' -e 'rules/[a-z-]*/' -e '[a-z-]*-\*.mdc' <scope>
#  -> typescript-*.mdc (SKILL.md:590), react-*.mdc (react-review.md:170), arkts-*.mdc
#     (ecc-harmonyos-app-resolver.md:181), react-native/ (SKILL.md:9); rest are prose/scripts
grep -rn 'rules/' hackathon-ecc/skills hackathon-ecc/agents hackathon-ecc/commands \
  hackathon-ecc/hooks hackathon-ecc/README.md  # 23 hits, all in S3
grep -rn '\.mdc' hackathon-ecc/manifests hackathon-ecc/hooks hackathon-ecc/schemas \
  hackathon-ecc/scripts hackathon-ecc/mcp.json  # only generic .mdc handling in scripts/
grep -rn '\.mdc' rewritten-skills round2-skills new-skills new-rules  # 0 outside call-map + staged hackathon-mode
diff -rq fix27/scratch-repo/hackathon-ecc/rules fix28/scratch-repo/hackathon-ecc/rules  # empty
```

## Appendix — files consulted

- `~/workspace/hackathon-plugin/fix27/skill-inventory.md` (fix #27 CUT list of 91 skills; kept-skill cross-reference)
- `~/workspace/hackathon-plugin/fix27/verify27.py` (counts check :269–275; token checks :366–385, :460–461; B7 :521; CUT-name sweep + ALLOW_LIST :653–842)
- `~/workspace/hackathon-plugin/fix27/scratch-repo/build.sh` (patch targets, RULE_DIRS/RULE_FILES :406–417, ruby/swift patches :1405–1466)
- `hackathon-ecc/skills/orchestrate/references/call-map.md` (generated inventory; method note on [struct-rule-*] entries)

## Appendix — full frontmatter census (verbatim, all 123 files)

Globs shown in full here; the §3 table truncates very long glob lists at 220 characters.

```
=== angular-coding-style.mdc ===
globs:
  - "**/*.component.ts"
  - "**/*.component.html"
  - "**/*.service.ts"
  - "**/*.directive.ts"
  - "**/*.pipe.ts"
  - "**/*.guard.ts"
  - "**/*.resolver.ts"
  - "**/*.module.ts"
=== angular-hooks.mdc ===
globs:
  - "**/*.component.ts"
  - "**/*.component.html"
  - "**/*.service.ts"
  - "**/*.directive.ts"
  - "**/*.pipe.ts"
  - "**/*.spec.ts"
=== angular-patterns.mdc ===
globs:
  - "**/*.component.ts"
  - "**/*.component.html"
  - "**/*.service.ts"
  - "**/*.store.ts"
  - "**/*.routes.ts"
=== angular-security.mdc ===
globs:
  - "**/*.component.ts"
  - "**/*.component.html"
  - "**/*.service.ts"
  - "**/*.interceptor.ts"
=== angular-testing.mdc ===
globs:
  - "**/*.spec.ts"
  - "**/*.test.ts"
=== arkts-coding-style.mdc ===
globs:
  - "**/*.ets"
  - "**/*.ts"
  - "**/module.json5"
  - "**/oh-package.json5"
  - "**/build-profile.json5"
=== arkts-hooks.mdc ===
globs:
  - "**/*.ets"
  - "**/*.ts"
  - "**/module.json5"
  - "**/oh-package.json5"
=== arkts-patterns.mdc ===
globs:
  - "**/*.ets"
  - "**/*.ts"
=== arkts-security.mdc ===
globs:
  - "**/*.ets"
  - "**/*.ts"
  - "**/module.json5"
=== arkts-testing.mdc ===
globs:
  - "**/*.ets"
  - "**/*.ts"
  - "**/ohosTest/**"
=== common-agents.mdc ===
description: "Agent orchestration: available agents, parallel execution, multi-perspective analysis"
alwaysApply: true
=== common-code-review.mdc ===
description: "Code review standards: mandatory review triggers, checklist, security review triggers"
alwaysApply: true
=== common-coding-style.mdc ===
description: "ECC coding style: immutability, file organization, error handling, validation"
alwaysApply: true
=== common-development-workflow.mdc ===
description: "Development workflow: plan, TDD, review, commit pipeline"
alwaysApply: true
=== common-git-workflow.mdc ===
description: "Git workflow: conventional commits, PR process"
alwaysApply: true
=== common-hooks.mdc ===
description: "Hooks system: types, auto-accept permissions, progress tracking best practices"
alwaysApply: true
=== common-patterns.mdc ===
description: "Common patterns: repository, API response, skeleton projects"
alwaysApply: true
=== common-performance.mdc ===
description: "Performance: model selection, context management, build troubleshooting"
alwaysApply: true
=== common-security.mdc ===
description: "Security: mandatory checks, secret management, response protocol"
alwaysApply: true
=== common-testing.mdc ===
description: "Testing requirements: 80% coverage, TDD workflow, test types"
alwaysApply: true
=== cpp-coding-style.mdc ===
globs:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
=== cpp-hooks.mdc ===
globs:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
=== cpp-patterns.mdc ===
globs:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
=== cpp-security.mdc ===
globs:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
=== cpp-testing.mdc ===
globs:
  - "**/*.cpp"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.hh"
  - "**/*.cxx"
  - "**/*.h"
  - "**/CMakeLists.txt"
=== csharp-coding-style.mdc ===
globs:
  - "**/*.cs"
  - "**/*.csx"
=== csharp-hooks.mdc ===
globs:
  - "**/*.cs"
  - "**/*.csx"
  - "**/*.csproj"
  - "**/*.sln"
  - "**/Directory.Build.props"
  - "**/Directory.Build.targets"
=== csharp-patterns.mdc ===
globs:
  - "**/*.cs"
  - "**/*.csx"
=== csharp-security.mdc ===
globs:
  - "**/*.cs"
  - "**/*.csx"
  - "**/*.csproj"
  - "**/appsettings*.json"
=== csharp-testing.mdc ===
globs:
  - "**/*.cs"
  - "**/*.csx"
  - "**/*.csproj"
=== dart-coding-style.mdc ===
globs:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/analysis_options.yaml"
=== dart-hooks.mdc ===
globs:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/analysis_options.yaml"
=== dart-patterns.mdc ===
globs:
  - "**/*.dart"
  - "**/pubspec.yaml"
=== dart-security.mdc ===
globs:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/AndroidManifest.xml"
  - "**/Info.plist"
=== dart-testing.mdc ===
globs:
  - "**/*.dart"
  - "**/pubspec.yaml"
  - "**/analysis_options.yaml"
=== fsharp-coding-style.mdc ===
globs:
  - "**/*.fs"
  - "**/*.fsx"
=== fsharp-hooks.mdc ===
globs:
  - "**/*.fs"
  - "**/*.fsx"
  - "**/*.fsproj"
  - "**/*.sln"
  - "**/*.slnx"
  - "**/Directory.Build.props"
  - "**/Directory.Build.targets"
=== fsharp-patterns.mdc ===
globs:
  - "**/*.fs"
  - "**/*.fsx"
=== fsharp-security.mdc ===
globs:
  - "**/*.fs"
  - "**/*.fsx"
  - "**/*.fsproj"
  - "**/appsettings*.json"
=== fsharp-testing.mdc ===
globs:
  - "**/*.fs"
  - "**/*.fsx"
  - "**/*.fsproj"
=== golang-coding-style.mdc ===
description: "Go coding style extending common rules"
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
=== golang-hooks.mdc ===
description: "Go hooks extending common rules"
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
=== golang-patterns.mdc ===
description: "Go patterns extending common rules"
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
=== golang-security.mdc ===
description: "Go security extending common rules"
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
=== golang-testing.mdc ===
description: "Go testing extending common rules"
globs: ["**/*.go", "**/go.mod", "**/go.sum"]
alwaysApply: false
=== hackathon-mode.mdc ===
description: Hackathon mode — full ECC process, grill-me first, UI pairing, audits deferred to the end
alwaysApply: true
=== java-coding-style.mdc ===
globs:
  - "**/*.java"
=== java-hooks.mdc ===
globs:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/build.gradle.kts"
=== java-patterns.mdc ===
globs:
  - "**/*.java"
=== java-security.mdc ===
globs:
  - "**/*.java"
=== java-testing.mdc ===
globs:
  - "**/*.java"
=== kotlin-coding-style.mdc ===
description: "Kotlin coding style extending common rules"
globs: ["**/*.kt", "**/*.kts", "**/build.gradle.kts"]
alwaysApply: false
=== kotlin-hooks.mdc ===
description: "Kotlin hooks extending common rules"
globs: ["**/*.kt", "**/*.kts", "**/build.gradle.kts"]
alwaysApply: false
=== kotlin-patterns.mdc ===
description: "Kotlin patterns extending common rules"
globs: ["**/*.kt", "**/*.kts", "**/build.gradle.kts"]
alwaysApply: false
=== kotlin-security.mdc ===
description: "Kotlin security extending common rules"
globs: ["**/*.kt", "**/*.kts", "**/build.gradle.kts"]
alwaysApply: false
=== kotlin-testing.mdc ===
description: "Kotlin testing extending common rules"
globs: ["**/*.kt", "**/*.kts", "**/build.gradle.kts"]
alwaysApply: false
=== nuxt-coding-style.mdc ===
globs:
  - "**/nuxt.config.*"
  - "**/app.config.*"
  - "**/app.vue"
  - "**/pages/**"
  - "**/layouts/**"
  - "**/middleware/**"
=== nuxt-hooks.mdc ===
globs:
  - "**/nuxt.config.*"
  - "**/app.config.*"
  - "**/server/**/*.ts"
  - "**/*.vue"
=== nuxt-patterns.mdc ===
globs:
  - "**/nuxt.config.*"
  - "**/app.config.*"
  - "**/app.vue"
  - "**/server/**/*.ts"
  - "**/pages/**"
  - "**/middleware/**"
=== nuxt-security.mdc ===
globs:
  - "**/nuxt.config.*"
  - "**/app.config.*"
  - "**/server/**/*.ts"
=== nuxt-testing.mdc ===
globs:
  - "**/nuxt.config.*"
  - "**/server/**/*.ts"
  - "**/pages/**"
  - "**/layouts/**"
  - "**/middleware/**"
=== perl-coding-style.mdc ===
globs:
  - "**/*.pl"
  - "**/*.pm"
  - "**/*.t"
  - "**/*.psgi"
  - "**/*.cgi"
=== perl-hooks.mdc ===
globs:
  - "**/*.pl"
  - "**/*.pm"
  - "**/*.t"
  - "**/*.psgi"
  - "**/*.cgi"
=== perl-patterns.mdc ===
globs:
  - "**/*.pl"
  - "**/*.pm"
  - "**/*.t"
  - "**/*.psgi"
  - "**/*.cgi"
=== perl-security.mdc ===
globs:
  - "**/*.pl"
  - "**/*.pm"
  - "**/*.t"
  - "**/*.psgi"
  - "**/*.cgi"
=== perl-testing.mdc ===
globs:
  - "**/*.pl"
  - "**/*.pm"
  - "**/*.t"
  - "**/*.psgi"
  - "**/*.cgi"
=== php-coding-style.mdc ===
description: "PHP coding style extending common rules"
globs: ["**/*.php", "**/composer.json"]
alwaysApply: false
=== php-hooks.mdc ===
description: "PHP hooks extending common rules"
globs: ["**/*.php", "**/composer.json", "**/phpstan.neon", "**/phpstan.neon.dist", "**/psalm.xml"]
alwaysApply: false
=== php-patterns.mdc ===
description: "PHP patterns extending common rules"
globs: ["**/*.php", "**/composer.json"]
alwaysApply: false
=== php-security.mdc ===
description: "PHP security extending common rules"
globs: ["**/*.php", "**/composer.lock", "**/composer.json"]
alwaysApply: false
=== php-testing.mdc ===
description: "PHP testing extending common rules"
globs: ["**/*.php", "**/phpunit.xml", "**/phpunit.xml.dist", "**/composer.json"]
alwaysApply: false
=== ponytail.mdc ===
description: Ponytail, lean code discipline. Write the smallest efficient code for approved features; never cut scope.
globs:
alwaysApply: true
=== python-coding-style.mdc ===
description: "Python coding style extending common rules"
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
=== python-fastapi.mdc ===
globs:
  - "**/app/**/*.py"
  - "**/fastapi/**/*.py"
  - "**/*_api.py"
=== python-hooks.mdc ===
description: "Python hooks extending common rules"
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
=== python-patterns.mdc ===
description: "Python patterns extending common rules"
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
=== python-security.mdc ===
description: "Python security extending common rules"
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
=== python-testing.mdc ===
description: "Python testing extending common rules"
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
=== react-coding-style.mdc ===
globs:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/components/**/*.ts"
  - "**/components/**/*.js"
  - "**/hooks/**/*.ts"
  - "**/hooks/**/*.js"
=== react-hooks.mdc ===
globs:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/hooks/**/*.ts"
  - "**/hooks/**/*.js"
  - "**/use-*.ts"
  - "**/use-*.tsx"
=== react-native-accessibility.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-coding-style.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-hooks.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-patterns.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-performance.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-production-readiness.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-security.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-native-testing.mdc ===
globs:
  - "**/*.ts"
  - "**/*.tsx"
=== react-patterns.mdc ===
globs:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/components/**/*.ts"
  - "**/components/**/*.js"
  - "**/app/**/*.tsx"
  - "**/pages/**/*.tsx"
=== react-security.mdc ===
globs:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/components/**/*.ts"
  - "**/app/**/*.ts"
  - "**/pages/**/*.ts"
=== react-testing.mdc ===
globs:
  - "**/*.test.tsx"
  - "**/*.test.jsx"
  - "**/*.spec.tsx"
  - "**/*.spec.jsx"
  - "**/__tests__/**/*.ts"
  - "**/__tests__/**/*.tsx"
=== ruby-coding-style.mdc ===
globs:
  - "**/*.rb"
  - "**/*.rake"
  - "**/Gemfile"
  - "**/*.gemspec"
  - "**/config.ru"
=== ruby-hooks.mdc ===
globs:
  - "**/*.rb"
  - "**/*.rake"
  - "**/Gemfile"
  - "**/Gemfile.lock"
  - "**/config/routes.rb"
=== ruby-patterns.mdc ===
globs:
  - "**/*.rb"
  - "**/*.rake"
  - "**/Gemfile"
  - "**/app/**/*.erb"
  - "**/config/routes.rb"
=== ruby-security.mdc ===
globs:
  - "**/*.rb"
  - "**/*.rake"
  - "**/Gemfile"
  - "**/Gemfile.lock"
  - "**/config/routes.rb"
  - "**/config/credentials*.yml.enc"
=== ruby-testing.mdc ===
globs:
  - "**/*.rb"
  - "**/*.rake"
  - "**/Gemfile"
  - "**/test/**/*.rb"
  - "**/spec/**/*.rb"
  - "**/config/routes.rb"
=== rust-coding-style.mdc ===
globs:
  - "**/*.rs"
=== rust-hooks.mdc ===
globs:
  - "**/*.rs"
  - "**/Cargo.toml"
=== rust-patterns.mdc ===
globs:
  - "**/*.rs"
=== rust-security.mdc ===
globs:
  - "**/*.rs"
=== rust-testing.mdc ===
globs:
  - "**/*.rs"
=== swift-coding-style.mdc ===
description: "Swift coding style extending common rules"
globs: ["**/*.swift", "**/Package.swift"]
alwaysApply: false
=== swift-hooks.mdc ===
description: "Swift hooks extending common rules"
globs: ["**/*.swift", "**/Package.swift"]
alwaysApply: false
=== swift-patterns.mdc ===
description: "Swift patterns extending common rules"
globs: ["**/*.swift", "**/Package.swift"]
alwaysApply: false
=== swift-security.mdc ===
description: "Swift security extending common rules"
globs: ["**/*.swift", "**/Package.swift"]
alwaysApply: false
=== swift-testing.mdc ===
description: "Swift testing extending common rules"
globs: ["**/*.swift", "**/Package.swift"]
alwaysApply: false
=== typescript-coding-style.mdc ===
description: "TypeScript coding style extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
=== typescript-hooks.mdc ===
description: "TypeScript hooks extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
=== typescript-patterns.mdc ===
description: "TypeScript patterns extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
=== typescript-security.mdc ===
description: "TypeScript security extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
=== typescript-testing.mdc ===
description: "TypeScript testing extending common rules"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
=== vue-coding-style.mdc ===
globs:
  - "**/*.vue"
=== vue-hooks.mdc ===
globs:
  - "**/*.vue"
  - "**/*.ts"
  - "**/*.tsx"
=== vue-patterns.mdc ===
globs:
  - "**/*.vue"
=== vue-security.mdc ===
globs:
  - "**/*.vue"
=== vue-testing.mdc ===
globs:
  - "**/*.vue"
=== web-coding-style.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-design-quality.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-hooks.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-patterns.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-performance.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-security.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
=== web-testing.mdc ===
globs:
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
```
