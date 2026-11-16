# Audit #77 (round 1) — fix #28 — INDEPENDENT AUDIT REPORT

**Verdict: AUDIT #77: NOT PASS**

One blocking finding (77-A1): the cut of `dart-security.mdc` removes native-manifest
hardening guidance that has no equivalent in any kept rule or skill, and that did load
on real kept-stack files (Expo prebuild `AndroidManifest.xml` / `Info.plist`). The
SPEC §1(b) claim that cutting the 7 NEEDS-DECISION files "removes no correct behavior"
is false for this file. Everything else audited passes, including the full live-dispatch
hunt, the vite-patterns challenge, the dead-script unwiring check, and F1/F2/F4/react-patterns.

**Method.** Read-only. I did not trust the coordinator's claims: I re-ran
`fix28/verify28.py` myself (106/106 on the correct invocation, see Notes), ran my own
broad CUT-name sweep over `skills/ agents/ commands/ rules/ hooks/ scripts/ manifests/
schemas/ README.md mcp.json package.json` (verify28 check 12 covers only the first
four), read all 7 NEEDS-DECISION rule files in the pre-cut tree
(`fix28/scratch-repo/hackathon-ecc/rules/`), read the pre-cut `posttooluse-dispatcher.js`
and `control-pane/ui.js`, and verified F1/F2/F4/react-patterns line by line in the built
tree (`hackathon-ecc/`, counts confirmed directly: 67 skills / 45 agents / 48 rules /
55 commands / 15 hooks).

---

## BLOCKING findings

### 77-A1 — `dart-security.mdc` cut removes kept-stack-applicable native-manifest guidance with no equivalent anywhere (SPEC §1(b) misfire call is wrong for this file)

**Evidence — what the cut file contained** (`fix28/scratch-repo/hackathon-ecc/rules/dart-security.mdc`,
pre-cut tree; 135 lines, globs `**/*.dart`, `**/pubspec.yaml`, `**/AndroidManifest.xml`,
`**/Info.plist`):

> `dart-security.mdc:98-104` (Android-Specific):
> "Declare only required permissions in `AndroidManifest.xml`"
> "Export Android components (`Activity`, `Service`, `BroadcastReceiver`) only when
> necessary; add `android:exported="false"` where not needed"
> "Review intent filters — exported components with implicit intent filters are
> accessible by any app"
> "Use `FLAG_SECURE` for screens displaying sensitive data (prevents screenshots)"

> `dart-security.mdc:106-111` (iOS-Specific):
> "Declare only required usage descriptions in `Info.plist` (`NSCameraUsageDescription`, etc.)"
> "Set `NSAppTransportSecurity` in `Info.plist` to disallow arbitrary loads"
> "Enable data protection entitlement for sensitive files"

> `dart-security.mdc:33-36` (Network Security):
> "Configure Android `network_security_config.xml` to block cleartext traffic"
> "Set request timeouts on all HTTP clients — never leave defaults"

**Evidence — no equivalent in the kept tree.** Grep over kept `skills/ agents/ commands/
rules/ README.md` (excluding `call-map.md`, excluding `node_modules`) returns **zero**
hits for `android:exported`, `FLAG_SECURE`, `allowBackup`, `intent-filter`,
`NSAppTransportSecurity`, and zero `WebView` guidance in any kept React Native file.
Grep for `timeout` in `rules/common-security.mdc`, `rules/react-native-security.mdc`,
`rules/react-security.mdc`, `rules/web-security.mdc`, `skills/security-review/SKILL.md`
returns zero hits. The kept `rules/react-native-security.mdc` (read in full) covers
only: bundle-is-public, `expo-secure-store`, `EXPO_PUBLIC_*` config, "HTTPS only;
reject cleartext", Zod validation of deep links, minimum permissions, `expo-doctor`.
It has no manifest-level item at all. The kept `rules/common-security.mdc`
(alwaysApply) covers generic principles (no hardcoded secrets, validate inputs,
parameterized queries) but no native-manifest mechanism. `skills/security-review/SKILL.md`
and `skills/react-native-patterns/SKILL.md` are likewise silent on manifests/ATS/exported.

**Evidence — the guidance did load on kept-stack files.** The globs
`**/AndroidManifest.xml` and `**/Info.plist` occur in Expo prebuild output, and
prebuild is part of the kept mobile path: `skills/mobile-ship/SKILL.md:83` references
prebuild ("Metro/prebuild crashes on latest Node"). So in a kept-stack Expo build
these files exist and the rule loaded on them. This is the one NEEDS-DECISION file
whose misfire was *partial*: the Dart/Flutter ~80% (`flutter_secure_storage`, Dio,
`sqflite`/`drift`, `webview_flutter` v4 API, `flutter build apk --obfuscate`) is
wrong-framework noise, but the Android/iOS manifest sections are framework-neutral
native guidance, correct for Expo native files.

**Why it matters.** SPEC §1(b) / `NDMISFIRE_F28` claims cutting the 7 files "removes
no correct behavior". For `dart-security.mdc` that is false: ~10 bullets of native
hardening that an agent opening an Expo `AndroidManifest.xml` or `Info.plist` used to
receive are gone, with no replacement. The loss is narrow (manifest hardening + HTTP
timeouts, not the Flutter content), so the proportionate fix is **not** a full restore
of the Flutter file — it is to port the manifest bullets into the kept
`rules/react-native-security.mdc` (framework-correct form: `expo-secure-store` /
`app.json` config-plugin equivalents where they exist, `android:exported`,
intent-filter review, `FLAG_SECURE`, `NSAppTransportSecurity`, usage descriptions,
data-protection entitlement, cleartext config, request timeouts), or equivalently to
restore `dart-security.mdc` with its globs narrowed to the two manifest patterns only.
Either fix closes this finding; the audit loop's own SPEC §1(b) instruction ("any file
the audit shows carrying a genuine kept-stack use is restored") anticipates exactly this.

**The other 6 NEEDS-DECISION files are cleared** (no genuine loss — see Notes).

---

## MINOR findings

### 77-B1 — Four live hook files still describe the cut `run-with-flags.js` as their caller (stale comments, not live dispatches)

- `scripts/hooks/block-no-verify.js:1266` — "Exportable run() for in-process execution via run-with-flags.js."
- `scripts/hooks/post-edit-format.js:31` — "Core logic — exported so run-with-flags.js can call directly"
- `scripts/hooks/quality-gate.js:140` — "Core logic — exported so run-with-flags.js can call directly."
- `scripts/hooks/stop-format-typecheck.js:239` — "Exported so run-with-flags.js uses require() instead of spawnSync,"

`scripts/hooks/run-with-flags.js` is in the CUT set (DEAD_SCRIPTS) and is absent from
the built tree; grep confirms no `require`/`import` of it anywhere — these are
comment-only mentions, so nothing executes a missing path. But they misdescribe the
exports' consumer: nothing calls these `run()` exports in-process now. Fix: reword to
"exported for testability / in-process use" or delete the clauses.

### 77-B2 — Kept schema still names a cut script as "the enforcing implementation"

`schemas/capsule-envelope.schema.json:5`:

> "description": "One append-only journal entry recorded by the ECC eval-harness capsule. Mirrors scripts/lib/eval-harness/envelope.js, which is the enforcing implementation."

`scripts/lib/eval-harness/envelope.js` is in the CUT set and absent from the built
tree (the whole `eval-harness/` lib dir is cut). This is a JSON description string —
no code loads it — so it is not a live dispatch, but it asserts a cut file is the
enforcing implementation of a shipped schema. Fix: reword the description to drop the
path claim (e.g. "One append-only journal entry recorded by the ECC eval-harness capsule.").

### 77-B3 — F2 edit left dead imports and a stale title in the live `evaluate-session.js`

`scripts/hooks/evaluate-session.js:17` — `const path = require('path');` (now unused;
the only `path.join` use was the removed config load) and `:22` — `readFile` in the
`../lib/utils` destructure (now unused; the only `readFile` use was the removed config
read). `node --check` passes and behavior is coherent (see Notes), so this is
cosmetic dead code left by the F2 patch. The file header still reads "Continuous
Learning - Session Evaluator" and log lines still use the `[ContinuousLearning]`
prefix, which is now a misnomer for a file whose header itself says pattern extraction
was removed. Fix: delete the two unused imports; optionally retitle the header/prefix.

---

## Notes / observations (checked and cleared)

- **(a) Live-dispatch hunt — PASS.** My own re-run of `fix28/verify28.py` (correct
  invocation, from `~/workspace/hackathon-plugin`, no args): **106/106 checks pass**,
  including check 12 ("0 un-allow-listed, 46 allow-listed, 288 generic bare-word noise
  lines") and check 12b (0 imperative dispatches hiding in allow-listed lines). I
  independently re-ran the strong-form sweep over a *broader* scope than check 12
  (adding `hooks/ scripts/ manifests/ schemas/ README.md mcp.json package.json`): no
  live dispatch to any CUT skill/agent/command/rule in `skills/ agents/ commands/
  rules/` beyond the 46 allow-listed lines, and every extra broad-scope hit adjudicated
  non-live:
  - `manifests/pi-core.json` (~40 lines): CUT names appear only as keys of the
    `exclude` map with reason strings (e.g. `"continuous-learning": "Cursor-only
    hooks-based continuous learning (deprecated)"`). No code in the built tree
    consumes `pi-core.json` (only `call-map.md` mentions it); SPEC §2(d) "NO CHANGE"
    is correct — these are reason logs, not references.
  - `manifests/install-components.json:378,394,410,426`: the 4 kept dead-skill
    components (`skill:continuous-learning`, `skill:windows-desktop-e2e`,
    `skill:coding-standards`, `skill:vue-patterns`) are the deliberate SPEC §2(b)
    item-3 keep; each description carries "(Removed in fix #27; resolves to the
    shared … module.)" and maps to an existing module (`workflow-quality` /
    `framework-language`); `resolveInstallPlan` passes for all profiles + the full
    55-component set.
  - `scripts/hooks/evaluate-session.js:8,57` and `scripts/lib/resolve-ecc-root.js:23`:
    prose-history comments naming cut skills ("was cut in fix #27", sentinel-moved
    note) — not dispatches. The resolve-ecc-root comment is explicitly asserted by
    verify28 check M6.
  - `README.md:28`: "`codebase-memory` was cut in fix #27" — prose history, explicitly
    kept per SPEC §4(c).
  - Dead-script full-path refs: grep for `post-bash-command-log.js`,
    `hookify-runtime.js`, `observe-runner.js`, `session-bridge.js`, `memory-vault.js`,
    `gateguard-fact-force.js`, `control-pane/server.js`, `skill-evolution/index.js`,
    `context-profile-interactive.js`, `harness-adapter-compliance.js`, `llm-summary.js`
    returns **zero** hits in the built tree (excl. `call-map.md`). The only
    dead-script mentions anywhere are the comment/note items in 77-B1/B2 and the
    `quality-gate.md:44` note (see (d)).
  - Counts verified directly on disk: skills 67, agents 45, commands 55, rules 48,
    hooks 15 events; all 75 CUT rules and all 135 DEAD_SCRIPTS absent from the built tree.
- **(b) The other 6 NEEDS-DECISION files — cleared, no genuine loss.**
  - `angular-hooks.mdc` (25 lines): `ng lint` / `ng build` / Prettier-after-edit —
    Angular-only; its "configure as an afterFileEdit hook" text was aspirational
    (no such `hooks.json` entry exists). No kept-stack use.
  - `angular-testing.mdc` (164 lines): entirely TestBed / CDK harnesses /
    `RouterTestingHarness` / `fakeAsync` / `HttpTestingController` / pipes-guards —
    Angular-only. Its two generic lines ("test behaviour, not implementation",
    "Target ≥80%") duplicate kept alwaysApply `common-testing.mdc` and
    `react-testing.mdc`. Its final line ("See skill: `angular-developer`") pointed
    at a CUT skill — cutting the file also removes that dangling pointer.
  - `nuxt-coding-style.mdc`, `nuxt-patterns.mdc`, `nuxt-testing.mdc`: 100% Nuxt
    (`useFetch`/`useAsyncData`/`$fetch`, Nitro `server/api/*`, `definePageMeta`,
    auto-imports, `@nuxt/test-utils`, `mountSuspended`/`mockNuxtImport`). No
    Next.js-usable guidance; the one arguably generic line (nuxt-patterns module-scope
    `ref()` SSR leak) is Vue-framed and has no actionable kept-stack form.
  - `vue-hooks.mdc` (45 lines): 100% Vue (`vue-tsc`, `eslint-plugin-vue`, SFC
    sequencing). Its only kept-stack effect was the misfire itself — telling every
    `.ts`/`.tsx` file to typecheck with `vue-tsc`, which is wrong for Next.js (plain
    `tsc` is correct there; kept typescript rules cover it). Cutting is a fix.
- **(c) vite-patterns — coordinator's INTENTIONALLY DORMANT judgment STANDS.**
  Pre-cut tree grep: the only invokers of `vite-patterns` outside its own SKILL.md
  and the manifests were the 9 cut nuxt/vue rule files, each a one-line
  "ECC skills: `…, vite-patterns, …`" cross-reference (e.g.
  `rules/nuxt-coding-style.mdc:45`, `rules/vue-hooks.mdc:44`). Those are topical
  cross-refs inside files that themselves only loaded on `.vue`/Nuxt files — not a
  dispatch mechanism for Vite work: no kept file, command, or agent routes to
  `vite-patterns`, and no kept flow step does Vite config work (kept "vite" mentions
  are Vitest test-runner references, e.g. `skills/typescript-patterns/SKILL.md:519,550`,
  which do not dispatch to the skill). `fix28/callmap/call-map-data.json` confirms
  `vite-patterns: {called: false, invokers: {manifests only}}`. Do not wire it to
  replace the cut cross-references.
- **(d) /quality-gate + /sessions "always-on (Cursor event)" labels — correctly dropped, no behavior loss.**
  - `scripts/hooks/posttooluse-dispatcher.js` header (pre-cut tree): "Not wired in
    this Cursor plugin — it never runs". Zero referrers in the built tree; the only
    mention is `commands/quality-gate.md:44-47`, which itself documents that the
    dispatcher "is not referenced by `hooks/hooks.json` or anything else in the
    plugin, so it never runs — do not rely on it." `hooks/hooks.json` registers 15
    Cursor events and has no PostToolUse/PreToolUse event at all.
  - `scripts/lib/control-pane/ui.js`: its only "sessions" mentions are its own dead
    dashboard rendering (`:373` `<div id="sessions">`, `:504-510,723`
    `renderSessions(snapshot.sessions)` — a sessions *listing* in a dead web UI, not
    an invocation of the `/sessions` command). Nothing requires
    `control-pane/server.js` (zero hits outside its own directory in the pre-cut
    tree). The call-map generator counting it as a `/sessions` invoker was a
    generator artifact; cutting it removes no live path.
  - `scripts/lib/plan-canvas/sessions.js` + `ui.js`: zero references outside the
    `plan-canvas/` directory in the pre-cut tree. `/plan` and `/aside` losing those
    invokers is likewise not a behavior loss.
- **(e) F1/F2/F4/react-patterns — all verified correct.**
  - F1: `commands/sessions.md:295` now reads "For command-center style monitoring,
    combine `/sessions info` and `git diff --stat`." Zero `cost-tracker` in the file.
    No surviving cost-metrics source exists anywhere: the only remaining
    `cost-tracker` mention in the tree is `skills/pitch-deck-video/SKILL.md:870`,
    which explicitly says "(the tracker script and config are not shipped in this
    plugin)" — accurate prose, not a source. The dead-weight report's suggested
    re-point target (`post-bash-command-log.js`) is itself cut, so dropping the
    clause (rather than re-pointing) was the right call.
  - F2: `scripts/hooks/evaluate-session.js` — `node --check` passes; logic is
    coherent (defaults `minSessionLength = 10`, `learnedSkillsPath =
    getLearnedSkillsDir()`; exits 0 for missing transcript or short sessions; the
    long-session path now just exits 0, matching the new header "the evaluator now
    only enforces the minimum session length and exits"). Config-load block and
    both orphan `[ContinuousLearning]` log lines are gone (also asserted by verify28
    check 10c). Leftovers are 77-B3 only.
  - F4: `README.md:11` now reads "and the chrome-devtools and playwright MCP
    servers"; `mcp.json` contains only `chrome-devtools` + `playwright`. ✓
  - react-patterns: `rules/react-patterns.mdc:194` now reads "For accessibility see
    `skills/frontend-a11y/SKILL.md`." and `skills/frontend-a11y/SKILL.md` exists. ✓
- **(f) Spot-checks of verify28 check-12 — confirmed.** `golang-patterns`: 0 hits
  anywhere in the built tree. `vue-hooks`: 0 hits anywhere. `continuous-learning`:
  only the adjudicated items (allow-listed `commands/learn.md:2` negative
  distinction; evaluate-session/resolve-ecc-root prose-history comments; pi-core
  exclude logs; install-components deliberate keep). `cost-tracker`: only the
  accurate pitch-deck-video note above. The sweep's verdict (0 un-allow-listed)
  holds; note check 12's scope is `skills/ agents/ commands/ rules/` only, and my
  broader scope found nothing live beyond the adjudicated items.
- **Invocation note (not a finding).** Running `verify28.py` with `.` as the built-dir
  argument from inside `hackathon-ecc/` yields 102/106 — the 4 failures are the
  checks that resolve `fix28/fix28-patch-log.md` and the call-map sidecar relative
  to the plugin root, plus the installer resolution, all of which break when BASE is
  the built dir itself. The documented invocation (from `~/workspace/hackathon-plugin`,
  no argument) yields **106/106**. No tree defect.

---

## Summary for the coordinator

- **77-A1 (BLOCKING):** port the `dart-security.mdc` native-manifest bullets
  (`android:exported="false"` + intent-filter review, `FLAG_SECURE`,
  `NSAppTransportSecurity`, Info.plist usage descriptions, data-protection
  entitlement, `network_security_config.xml` cleartext block, HTTP request timeouts)
  into kept `rules/react-native-security.mdc` (or restore `dart-security.mdc` with
  globs narrowed to `**/AndroidManifest.xml` + `**/Info.plist` only). Do not restore
  the full Flutter file.
- **77-B1:** reword the 4 `run-with-flags.js` comments in live hook files.
- **77-B2:** reword `schemas/capsule-envelope.schema.json:5` to drop the
  "enforcing implementation" claim about the cut `eval-harness/envelope.js`.
- **77-B3:** drop the unused `path` / `readFile` imports in `evaluate-session.js`
  (and optionally retitle its "Continuous Learning" header/prefix).
- Everything else in scope is verified clean, including the check-12 sweep
  (independently re-run: 106/106), the vite-patterns dormancy call, the
  posttooluse/control-pane unwiring, and F1/F2/F4/react-patterns.
