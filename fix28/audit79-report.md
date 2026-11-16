# Audit #79 (round 2, re-audit) — fix #28 — INDEPENDENT AUDIT REPORT

**Verdict: AUDIT #79: PASS**

All round-1 fixes verified landed correctly in the rebuilt tree (build run 6),
and the regression re-sweep finds no new live dispatch, no stale count, and no
regression in previously clean areas. Zero blocking, zero minor findings.

**Method.** Read-only (report file only). I did not trust the coordinator's
claims: I read `fix28/audit77-report.md` and `fix28/audit78-report.md` in full,
re-read SPEC §1(b) and §2(a) item 5 as corrected, `fix28/fix28.py` §2a and
§5d–§5g, and `fix28/fix28-patch-log.md` (0 errors, 26 changes), then verified
each item against the actual built tree (`hackathon-ecc/`) and the pre-cut
source (`fix28/scratch-repo/hackathon-ecc/rules/dart-security.mdc`). I re-ran
`fix28/verify28.py` myself twice (both invocations, see (d)), and ran my own
independent sweeps (CUT-rule stems, precise-path dead-script forms, fix #27
strong-form names) over the built tree.

---

## BLOCKING findings

None. (Numbered 79-Ax: none issued.)

## MINOR findings

None. (Numbered 79-Bx: none issued.)

---

## Verified round-1 fixes

### (a) 78-B1 (SPEC defect) — FIXED, verified in SPEC, code, and built tree

- `fix28/SPEC.md` §2(a) item 5 now reads: *empty the `"dependencies":
  ["skill-unified-memory"]` list to `[]` — do NOT delete the key*, citing
  `install-manifests.js` `resolveModule` (:611) and `selectResolvedModule`
  (:636) iterating `module.dependencies` unconditionally, and noting the
  Audit #6 pop-the-field convention does not apply here. It carries the
  correction note: *"(Corrected per audit #78-B1: this item originally
  prescribed deleting the field, which is the breaking edit.)"*
- Ground truth confirmed in the built tree: `hackathon-ecc/scripts/lib/
  install-manifests.js:611` — `for (const dependencyId of module.dependencies)
  {` inside `resolveModule`, and `:636` — the same unconditional iteration
  in `selectResolvedModule`. A missing key would throw `TypeError:
  module.dependencies is not iterable`.
- Shipped code matches: `fix28/fix28.py:235-243` asserts the pre-value is
  `["skill-unified-memory"]`, then `_wq["dependencies"] = []` with the
  comment *"Empty the list, do NOT delete the key … (verify28 run 1 caught
  this: TypeError, module.dependencies is not iterable)"*.
- Built manifest matches: `manifests/install-modules.json` —
  `workflow-quality.dependencies == []` (verified by JSON read), 14 modules /
  84 paths, and every one of the 14 modules carries a `dependencies` key.
  `resolveInstallPlan` succeeds for all 7 profiles + the 55-component set
  (verify28 check 10f, re-run here).
- No other SPEC section still prescribes the old edit: the only other
  `dependencies` mentions in SPEC are inside item 5 itself, and the only
  "deleting the field" text is line 164 inside the correction note, which
  calls it the breaking edit. The `delete the … paths` hits elsewhere in
  §2(a) are path-list prunes, not the key.

### (b) 77-A1 (BLOCKING, dart-security port) — FIXED, verified bullet by bullet

Read the built `hackathon-ecc/rules/react-native-security.mdc` in full and
compared it against the pre-cut `fix28/scratch-repo/hackathon-ecc/rules/
dart-security.mdc` (135 lines).

1. **Every ported bullet has a source bullet; no Flutter content smuggled
   in.** The port consists of 9 bullets, all traceable to source:
   - Native Manifests section (7 bullets): the 4 Android-Specific bullets
     (required permissions; `android:exported="false"`; intent-filter review;
     `FLAG_SECURE`) are verbatim from `dart-security.mdc:98-104`; the 3
     iOS bullets (usage descriptions; `NSAppTransportSecurity` disallowing
     arbitrary loads; data-protection entitlement) are verbatim from
     `:106-111` and the Network Security `NSAppTransportSecurity` bullet
     at `:33-36`.
   - Network & Data section (2 bullets): `network_security_config.xml`
     cleartext block and request timeouts are verbatim from source
     `:33-36`.
   - Correctly NOT ported: `flutter_secure_storage`, Dio, `sqflite`/`drift`,
     `webview_flutter`, `flutter build --obfuscate`, `flutter_dotenv`,
     `--dart-define`, `local_auth`, `flutter analyze`. A case-insensitive
     grep for `flutter|dart|dio|sqflite|drift|webview|obfuscat|secure_storage|
     local_auth` over the built file returns only lines 47–49 — the port
     note itself ("Ported from the cut `dart-security` rule … not
     Flutter-specific. (DARTSEC_F28)").
2. **Manifest globs added.** Frontmatter now reads `**/*.ts`, `**/*.tsx`,
   `**/AndroidManifest.xml`, `**/Info.plist` — the two manifest globs are
   new (source file carried the same two globs alongside `**/*.dart` /
   `**/pubspec.yaml`, which were correctly not carried over).
3. **Coherent as React Native / Expo guidance.** The port note frames the
   section ("Expo prebuild generates these files; the hardening below applies
   to them"). No Dart-isms remain outside the note. No contradiction with the
   rest of the file: "HTTPS only; reject cleartext" (Network & Data) is
   consistent with the `network_security_config.xml` cleartext bullet and the
   `NSAppTransportSecurity` bullet (same rule, two platforms); "Request the
   minimum device permissions" (Permissions & Privacy) is consistent with,
   not duplicative of, the manifest "Declare only required permissions"
   bullet (one is runtime requests, the other is the manifest declaration).
   The `fix28.py` §5d patch text matches the built file exactly (all three
   `sub()` anchors: globs, network bullets, Native Manifests section before
   `## Dependencies`).
4. **The other 6 NEEDS-DECISION files still stand cut, no genuine loss.**
   All 6 absent from the built tree (`angular-hooks`, `angular-testing`,
   `nuxt-coding-style`, `nuxt-patterns`, `nuxt-testing`, `vue-hooks`), plus
   `dart-security.mdc` itself. Spot-checked two against audit #77's
   reasoning, reading the pre-cut files: `angular-testing.mdc` is 12 hits
   for `TestBed|fakeAsync|HttpTestingController` and ends with `See skill:
   \`angular-developer\`` — a CUT skill, so cutting also removes a dangling
   pointer, as #77 said; `vue-hooks.mdc` prescribes `vue-tsc --noEmit`
   ("Plain `tsc` … must not be the typecheck hook for this project") and
   `eslint-plugin-vue` — wrong-framework for kept-stack TS files, so
   cutting is a fix, as #77 said. Nothing changed since round 1.
- **SPEC §1(b) records the exception honestly.** The Correction (audit
  #77-A1) paragraph is present: the "removes no correct behavior" claim
  *"was false for one file"*, naming the exact manifest bullets, the port
  into `rules/react-native-security.mdc` including the two manifest globs
  (`DARTSEC_F28`, fix28.py §5d), and clearing the other 6 per audit #77.

### (c) 77-B1/B2/B3 — FIXED, verified in the built tree

- **77-B1:** `grep -rn "run-with-flags"` over the 4 hook files returns zero
  hits. Reworded lines confirmed: `block-no-verify.js:1266` ("Exportable
  run() for in-process execution."), `post-edit-format.js:31` and
  `quality-gate.js:140` ("Core logic — exported for in-process use and
  testability"), `stop-format-typecheck.js:239` ("Exported for in-process
  execution (rather than spawnSync),"). Matches `fix28.py` §5e exactly.
- **77-B2:** `schemas/capsule-envelope.schema.json:5` now reads
  `"description": "One append-only journal entry recorded by the ECC
  eval-harness capsule."` — no `envelope.js`, no "enforcing implementation"
  claim. Matches `fix28.py` §5f exactly.
- **77-B3:** `scripts/hooks/evaluate-session.js` — no `path` / `readFile`
  imports (grep for `ContinuousLearning|readFile|require('path')` returns
  zero hits), header retitled to `Session Evaluator`, log prefix is
  `[SessionEvaluator]` (3 occurrences: error line, short-session log; the
  §5g `count=2` replacement covered the two log lines, the error line was
  already in the new form). `node --check` passes. Read the whole file:
  it is coherent as a hook — `fs` is still used (`fs.existsSync`), all
  remaining destructured imports (`getLearnedSkillsDir`, `ensureDir`,
  `countInFile`, `log`) are used, defaults apply (`minSessionLength = 10`,
  `learnedSkillsPath = getLearnedSkillsDir()`), exits 0 for missing
  transcript or short sessions, and the long-session path exits 0 per the
  header ("the evaluator now only enforces the minimum session length and
  exits"). Matches `fix28.py` §5g exactly.

### (d) Regression re-sweep — CLEAN

- **verify28.py re-run by this auditor, correct invocation** (from
  `~/workspace/hackathon-plugin`, no args): **110/110 checks pass**, exit 0
  — including the three new round-2 checks (10h DARTSEC port, B1, B2, B3)
  and check 12 / 12b (0 un-allow-listed, 47 allow-listed, 288 generic
  bare-word noise lines; 0 imperative dispatches hiding in allow-listed
  lines). Matches `fix28/verify28-run5.log` (110/110).
- **BASE-abspath verifier fix — FIXED.** Running `python3 ../fix28/
  verify28.py .` from inside `hackathon-ecc/` now yields **110/110, exit 0**
  — round 1's 102/106 invocation artifact is gone. The fix is
  `verify28.py:110`: `BASE = os.path.abspath(BASE)` with the comment
  *"audit #77 invocation note: \".\" as arg broke log/sidecar paths"*.
  No check fails on the `.` invocation now; nothing is path-dependent in a
  way that breaks.
- **Independent CUT-rule sweep** (all 75 stems from `fix28.py` CUT_RULES,
  whole built tree excl. `node_modules`): only 2 stems hit anywhere —
  `dart-security` → only `rules/react-native-security.mdc` (the DARTSEC
  port note, allow-listed line 47, see below) and `vue-patterns` → only
  `manifests/install-components.json:426` (the deliberate §2(b) keep,
  `skill:vue-patterns` with the "(Removed in fix #27…)" note, adjudicated
  in audits #77/#78). All 75 CUT rule files absent on disk; all 48 kept
  rules present.
- **Independent dead-script sweep** (all 135 paths from `fix28.py`
  DEAD_SCRIPTS): all 135 absent on disk. Precise-path-form grep (full
  relative path and parent-dir/basename) over the whole built tree finds
  only 3 hits, all adjudicated prose, none a dispatch: `scripts/hooks/
  context-routing-index.js` and `scripts/lib/context-pack-registry.js` in
  the call map's B6 note (past-tense documentation of the removed chain,
  cleared by audit #78), and `scripts/hooks/posttooluse-dispatcher.js` in
  `commands/quality-gate.md:44-47`, which explicitly states the dispatcher
  *"is not referenced by `hooks/hooks.json` or anything else in the plugin,
  so it never runs"* (cleared by audit #77). (A loose bare-stem sweep
  returns 34 apparent hits, but every one is a generic filename substring
  — `server.js`, `index.js`, `config.js`, `graph.js` — in unrelated files,
  not a reference to the cut file; the precise-path sweep is the correct
  test and it is clean apart from the 3 prose hits.)
- **Independent fix #27 sweep** (100 CUT skills / 27 removed agents / 32
  dropped commands from `fix27/verify27.py`, strong forms: backticked name,
  `skill: <name>`, `skills/<name>/`, `agents/<name>.md`, `/<name>`): 36
  hits in `skills/ agents/ commands/ rules/` (excl. call map), every one
  adjudicated non-live — "was cut in fix #27" / "NOT invoked" / "NOT wired"
  prose-history or negative mentions (`delivery-gate`, `feature-expansion`,
  `integration`, `orchestrate`, `hackathon-mode.mdc:37-38`), plus generic
  word noise (`accessibility` inside data-file URLs in
  `ui-ux-pro-max/data/*`). No live dispatch to any fix #27 CUT element.
  This agrees with verify28 check 12's 0 un-allow-listed verdict.
- **New allow-list entry — genuine and correctly numbered.** verify28.py's
  ALLOW_LIST has `"rules/react-native-security.mdc": {47: "prose-history:
  'Ported from the cut \`dart-security\` rule' (DARTSEC_F28 port note)"}`.
  Built-file line 47 is exactly that sentence (`sed -n '47p'` confirms).
  It is genuinely non-live: a prose sentence inside a `.mdc` rule file,
  naming the cut rule only as the source of the port; it contains no
  dispatch verb, no `skill:`/`use`/`load`/`invoke` instruction, and check
  12b re-scans it for imperative dispatches (0 found). The allow-list count
  moved 46 → 47 solely because of this one entry.

### (e) Call map still matches the rebuilt tree — VERIFIED regenerated

- Built copy `hackathon-ecc/skills/orchestrate/references/call-map.md`:
  header `# Call map — hackathon-ecc (fix #28 §1)` and `GENERATED by
  \`fix28/callmap/generate_call_map.py\` from the built tree`; counts table
  67 / 45 / 48 / 55 / 15 / 49; `## Rules (48)`; **zero** occurrences of
  `123` anywhere in the file; `react-native-security` row present
  (`:220`, `[struct-rule-globs]` + `react-patterns` + skill invokers);
  zero mentions of `dart-security`, `angular-testing`, or `vue-hooks`.
- It is the regenerated copy, not a stale one: `fix28/callmap/
  call-map-before.md` (the pre-regeneration snapshot) still shows
  `## Rules (123)` and 8 cut-rule mentions, while the built copy shows
  `(48)` and 0 — the built copy differs from the pre-regen snapshot in
  exactly the regenerated direction. Sidecar `fix28/callmap/
  call-map-data.json` counts are exactly `{skills: 67, agents: 45, rules:
  48, commands: 55, hooks: 15, triggers: 49}` with `uncalled.rules == []`,
  matching the map. Counts confirmed directly on disk: skills 67, agents
  45, rules 48, commands 55, `hooks/hooks.json` registers 15 events.
  Build log run 6 ends `fix28: OK` with counts 67/45/48/55/15 and
  `build complete`.

---

## Notes / observations (checked and cleared)

- `fix28/fix28-patch-log.md`: `## Errors (0)`, 26 changes, including the
  §5d DARTSEC port (3 anchors), §5e (4 hook rewords), §5f (schema), §5g
  (4 evaluate-session edits). The run-6 build log shows the same anchors
  applied.
- The DARTSEC port note's phrase "the cut `dart-security` rule" is the only
  occurrence of the string `dart-security` in the entire built tree
  (outside the note, zero hits) — the port adds guidance, not a pointer
  back to a cut file.
- The `vue-patterns` hit in `install-components.json` is the only
  fix #28 CUT-rule stem surviving anywhere besides the DARTSEC note, and
  it is the deliberate SPEC §2(b) keep, not a dispatch.
- No live-browser or Cursor-session check was needed or performed; every
  item in scope was verifiable from the files on disk.
- Nothing in this audit re-litigates fix #27 adjudications, the vite-patterns
  dormancy call, or the B6 documentation-only disposition beyond confirming
  the round-1 fixes and the absence of regressions from the fix edits.
