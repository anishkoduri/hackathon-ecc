# Fix #28 — MANIFEST

**Scope:** cut all remaining bloat that does not affect the plugin and is just there
(fix #27 §5 open items: per-language rule files for cut languages, unpruned
install manifests, dead-weight audit of the whole built tree).
**Status: DONE locally — committed + bundled, NOT pushed (no GitHub auth in
sandbox). Audit #79 PASS, sweep #37 CLEAN, dry-run #43 PASS, verify28
110/110. Commit hash + bundle details in the coordinator's final report
(this manifest is the pre-push record and does not contain its own commit's
hash, per the fix #26 convention).**

## Results

| Count | Before (fix #27) | After (fix #28) |
|---|---|---|
| Skills | 67 | 67 (unchanged) |
| Agents | 45 | 45 (unchanged) |
| Rules | 123 | **48** (75 cut) |
| Commands | 55 | 55 (unchanged) |
| Hooks | 15 | 15 (unchanged) |
| Trigger keys | 49 | 49 (unchanged) |
| Install modules | 16 | **14** |
| Install module paths | 184 | **84** |
| Install components | 57 | **55** |
| Install profiles | research 8 / full 16 | research **7** / full **14** |
| Dead scripts removed | — | **135 files, 1,301,859 bytes (~1.24 MiB)** |

**Cut:** 75 per-language rule files (36 KEEP / 68 CUT / 7 NEEDS-DECISION from the
123-file inventory; the 7 NEEDS-DECISION files were CUT — see §2), 100 dead
skill paths from `install-modules.json` (+ `skill-unified-memory` and
`business-content` modules deleted with their reference chains, §2), 135 dead
script files, the `codebase-memory-mcp` entry from `mcp.json`.

**Kept deliberately:** `scripts/lib/orchestration-session.js` +
`scripts/lib/tmux-worktree-orchestrator.js` (runtime-dead but the whole
orchestration module; cutting deletes a profile module — parent decision);
`scripts/ci/validate-skills.js` (documented CI tool, manifest-listed); the 22
misleading install components (4 dead `skill:*` + 18 dead lang/framework —
kept with description corrections, since deletion changes selector behaviour
to throw `Unknown install component`); `motionsites-web-builder` module
membership (an addition, not a prune — parent decision); the `dart-security`
native-manifest guidance (ported, not lost — audit #77-A1, §3).

**Builds:** run 1 FAILED (latent `MS_SRC` bug — fixed in build.sh), run 2
FAILED (`install-profiles.json` is a name-keyed dict, not a list — fixed in
fix28.py), runs 3–6 PASSED (exit 0, counts 67/45/48/55/15).
**verify28.py: 110/110, exit 0** (run 5, on the run-6 tree).
**Audit loop:** #77 NOT PASS → fixed → #78 NOT PASS → fixed → **#79 PASS**
(0 blocking, 0 minor).
**Sweep #36: NOT CLEAN** (0 blocking, 1 minor 36-B1 — fixed, see §3; re-sweep
#37 pending).
**Dry-run #43: PASS** (all 5 legs; report `fix28/dryrun43/dryrun43-report.md`).
**Build run 7 (after the 36-B1 fix): PASSED** (exit 0, counts 67/45/48/55/15);
built tree BYTE-IDENTICAL to run 6 (full-tree md5 diff, excl. node_modules).
**verify28 run 6: 110/110, exit 0** (run-7 tree). **verify27 re-run: 76/79**,
failing ONLY on the codified tails (see §4).
**Sweep #37: CLEAN** (0 blocking, 0 minor — re-sweep after the 36-B1 fix;
report `fix28/sweep37-report.md`). **SPEC §6 sweep criterion: MET via #37.**
Commit + bundle pending (see §7).

## §1 Scope

Per fix28/SPEC.md (§0–§7, following the fix #27 pattern):

1. **(a) Per-language rule files.** Cut the rule files for languages whose
   skills were cut in fix #27 (OWED-11/M7). Rules 123 → 48. NEVER cut rules
   with live dispatches, the alwaysApply rules, `hackathon-mode`, or any rule
   the live tree dispatches to. Each cut verified zero live dispatches.
   Correction found by audit #77: the 12 alwaysApply rules are 10 `common-*`
   + `hackathon-mode` + `ponytail` (not 9 as first stated).
2. **(b) Install manifests.** Prune paths for removed skills in
   `install-modules.json` / `install-components.json`; resolve the
   `install-profiles.json` reference to `skill-unified-memory` properly
   (module + `full`-profile entry + `skill:unified-memory` component +
   `workflow-quality` dependency, atomically — a partial prune throws
   `Unknown install module`; a left dependency breaks all 7 profiles).
   Same treatment for `business-content` (5/5 dead) + `capability:content` +
   `research`/`full` entries. `pi-core.json`: NO change.
3. **(c) Dead-weight audit.** Whole built tree audited for stale docs, dead
   references, orphaned files, unused scripts. Cut only what is provably
   dead; when in doubt, KEEP and record why.

Hard constraints (all kept): fix dirs fix13–fix27 STAY (audit trail); NEVER
re-run fix11/fix11-stage.py; build.sh is the source of truth, staged sources
only, never the built tree directly except via fix28.py; commits author Anish
Koduri <akoduri05@gmail.com> ONLY, NO "Co-authored-by: Cursor" trailer, no AI
tool as contributor/author anywhere; do NOT push (no GitHub auth in sandbox)
— commit locally + verified git bundle; lock-in rule — if a cut would lower
quality or break live behavior, flag it and keep it (applied: dart-security
port, orchestration-module keep).

Build mechanics: main `~/workspace/hackathon-plugin/` is the BUILD area
(build.sh hardcodes `PLUGIN_ROOT="$HOME/workspace/hackathon-plugin"`), NOT a
git repo. `fix28/scratch-repo` is only the commit workspace (clone, origin =
fix27/scratch-repo local path). All implementation and builds happen in the
main copy; changes sync into scratch-repo for the commit. Env-redirected
builds (TMPDIR / UIPRO_DIR / MS_DIR / SKILL_SRC to disk under
`fix28/scratch-tmp/`); ECC_REPO stays hardcoded to /tmp/ecc-repo-clean
(missing after the /tmp wipe — `fetch_repo` re-clones from GitHub).

## §2 Disposition table

### (a) Rules: 123 → 48 (75 cut)

Inventory: `fix28/analysis/rule-inventory.md` (1,140 lines). 12 alwaysApply,
36 KEEP, 68 CUT, 7 NEEDS-DECISION.

| Family | Disposition |
|---|---|
| cpp / csharp / fsharp / golang / java / kotlin / perl / php / ruby / rust / swift (5 files each) | CUT |
| angular (3), dart (4), nuxt (2), vue (4) | CUT |
| angular-hooks, angular-testing, dart-security, nuxt-coding-style, nuxt-patterns, nuxt-testing, vue-hooks (the 7 NEEDS-DECISION) | CUT — zero dispatches, no kept skill serves the language; their only effect on kept-stack files is injecting wrong-framework guidance. **Exception:** dart-security's native-manifest bullets were PORTED, not lost (audit #77-A1, §3). |
| python (6), typescript (5), react (5), react-native (8), arkts (5), web (7) | KEEP. Arkts stays on live family-glob dispatch from kept agent `ecc-harmonyos-app-resolver.md:181`. Python stays on `**/*.py` glob match despite zero literal dispatches. |
| 12 alwaysApply (10 `common-*` + `hackathon-mode` + `ponytail`) | KEEP |

Fixes, not cuts: `react-patterns.mdc:194` pointed at CUT skill `accessibility`
— reworded to `frontend-a11y`. `verify27.py:269–275` asserted exactly 123
rules (moved to 48 in verify28). `build.sh` names 21 CUT/ND rule files in
patch calls — those run at STEP 3 before fix28.py deletes the files, so they
apply harmlessly.

Call-map consequence: `vite-patterns` is now uncalled (its only invokers were
cut nuxt/vue rules) — recorded as INTENTIONALLY DORMANT in
`fix28/callmap/wiring-list.md` (17 uncalled + 7 second-order orphans, 0
wire-ins). `/quality-gate` and `/sessions` lost their "always-on (Cursor
event)" flow labels because the only invokers conferring them were cut dead
scripts that never ran — not a behavior loss.

### (b) Install manifests: 16 → 14 modules, 184 → 84 paths, 57 → 55 components

Analysis: `fix28/analysis/install-manifests.md`. The 100 dead skill paths
equal verify27.py's CUT_SKILLS set exactly (verified programmatically).

| Item | Disposition |
|---|---|
| 100 dead skill paths in `install-modules.json` | CUT |
| `skill-unified-memory` module + `full`-profile entry + `skill:unified-memory` component + `workflow-quality` dependency | DELETED atomically (decision (a)) |
| `business-content` module (5/5 dead) + `capability:content` + `research`/`full` entries | DELETED atomically (same treatment) |
| `workflow-quality` `dependencies` key | EMPTIED to `[]`, never deleted — `install-manifests.js` `resolveModule` (:611, also :636) iterates `module.dependencies` unconditionally; deleting the key crashes every profile resolve (caught by verify28 run 1). SPEC §2(a) item 5 corrected to prescribe `[]` (audit #78-B1). No other dangling dependency refs exist. |
| `pi-core.json` | NO CHANGE (all 30 skills + 18 commands exist; `unified-memory` at :229 is an exclude-reason log) |
| 22 misleading components (4 dead `skill:*` + 18 dead lang/framework) | KEPT with description corrections — deletion changes selector behaviour to throw `Unknown install component` |
| Kept skill `motionsites-web-builder` in no module (reachable only via synthetic component) | NOT ADDED to a module — one-line add to `hackathon.paths` is a parent decision (flagged in the analysis) |

`plan.js:155–157` confirmed verbatim: missing source → `return []`, silent
skip. verify27.py asserts only one manifest thing (pi-core M-new-4, lines
540–548). 8 suggested verifier extensions in the analysis report.

### (c) Dead scripts: 135 files, 1,301,859 bytes (~1.24 MiB, 58% of `scripts/`)

Analysis: `fix28/analysis/dead-weight.md` (280 lines). Liveness closure: 243
files under scripts/+hooks/, 101 reachable, 142 unreachable, 7 excluded → 135.

| Cluster | Files | What |
|---|---|---|
| A — scripts/hooks/ | 42 | Unwired Claude Code PostToolUse/PreToolUse dispatcher subtree (headers say "not wired… it never runs") |
| B — scripts/lib/ | 60 | Whole dead subsystems (control-pane, plan-canvas, eval-harness, context-profile, agent-proximity, gateguard libs, session-adapters, skill-improvement, worktree-lifecycle) |
| C — lib orphans | 33 | Orphaned lib files |
| Plus `mcp.json:17-18` | 1 entry | `codebase-memory-mcp` entry removed |

Zero live dispatches to CUT skills/agents/commands in scope. Hooks/ 17 vs 15
explained: 15 hook events + `hooks/adapter.js` (shared loader) +
`hooks/hooks.json` (manifest).

Fixes, not cuts: **F1** `commands/sessions.md:295` pointed at removed
`scripts/hooks/cost-tracker.js` — the cost-tracker clause was DROPPED (the
worker's suggested target `post-bash-command-log.js` is itself in the CUT set;
no surviving cost-metrics mechanism exists). **F2** live
`scripts/hooks/evaluate-session.js:57` reads CUT
`skills/continuous-learning/config.json` (guarded read, logs orphan lines) —
dead `path`/`readFile` imports removed, header retitled "Session Evaluator",
log prefix `[ContinuousLearning]` → `[SessionEvaluator]` (audit #77-B3).
**F4** README.md:11 still listed codebase-memory MCP server while :28 says
it was cut — phrase removed.

Deliberately KEPT: `scripts/lib/orchestration-session.js` +
`scripts/lib/tmux-worktree-orchestrator.js` (runtime-dead but the whole
orchestration module; cutting deletes a profile module — parent decision);
`scripts/ci/validate-skills.js` (documented CI tool, manifest-listed).

Implementation warning (kept): build.sh:186/192/209 copies scripts/, hooks/,
mcp.json wholesale — deletions must be in fix28.py (runs after the copies),
not hand edits. build.sh:14592 `node --check`s CUT candidate
`harness-adapter-compliance.js` — runs BEFORE the fix28.py invocation
(~24090), so the file still exists at check time.

### (d) fix28.py + build.sh

`fix28/fix28.py` (+ `fix28/fix28.py.template`, durable source — keep in sync).
Lists generated from the analysis files, not hand-typed: 75 rules, 135
scripts, manifest dead paths verified against disk 94+6=100. Sections: rules
removal, manifest JSON edits (deterministic, exact anchors asserted),
dead-script removal, mcp.json edit, README patches (count lines 67/45/48/55;
:11 codebase-memory phrase removal; fix #28 provenance note after the :28
line carrying CUTRULES_F28/MANIFEST28_F28/DEADSCRIPTS_F28/README48_F28
tokens), F1/F2/react-patterns text patches, stale-count scan (tokens "123
rules", "121 rules as-shipped"; call map excluded — generator-owned).
Anchor tokens `_F28`: CUTRULES_F28, MANIFEST28_F28, DEADSCRIPTS_F28,
EVALSESS_F28, README48_F28, REACTA11Y_F28, NDMISFIRE_F28, ORCHKEEP_F28, plus
DARTSEC_F28 (added for the audit #77 port). Token homes: 4 in README note,
EVALSESS in evaluate-session.js, DARTSEC_F28 in react-native-security.mdc, 3
in the patch log only (REACTA11Y via OWED-28-6, NDMISFIRE via rules-cut line,
ORCHKEEP via OWED-28-1).

Build.sh hook added to BOTH main build.sh and scratch-repo build.sh (+14
lines after fix27's block, before STEP 5). Two build fixes (not cuts):
run 1 — `MS_SRC` hardcoded to `/tmp/hack-skills/skills`, does NOT follow
env-redirectable `MS_DIR`; fixed at build.sh:25 in both copies
(`MS_SRC="${MS_DIR:-/tmp/hack-skills}/skills"`, default unchanged without the
redirect). Run 2 — `install-profiles.json` `profiles` is a name-keyed DICT,
not a list of `{"id"}` objects; fixed in fix28.py + template
(`_pby_id = _profs["profiles"]`).

Call map: generator copied to `fix28/callmap/generate_call_map.py` (EXPECTED
rules 123→48, all `fix25` paths → `fix28`). Regenerated after run 3
(copy-aside → run → diff → restore). Generator exit 0, all counts match
(67/45/48/55/15/49), uncalled rules 0. Two generator defects found and fixed
(not hand-edited into the map): hardcoded `section("Rules (123)")` header and
the B6 note naming 4 loader files fix #28 cut (reworded to past tense + fix
#28 removal note); also fixed the generator docstring "123 rules". Diff vs
pre-regeneration map is exactly the intended class (75 cut-rule rows gone,
kept rows pruned of cut-rule invokers, dead-script invokers dropped,
`frontend-a11y` gained the `react-patterns.mdc` dispatch). Run 4 built the
regenerated map ("fix #28 §1", "## Rules (48)", zero "123"). Sidecar:
`fix28/callmap/call-map-data.json`. Aside copy kept:
`fix28/callmap/call-map-before.md`.

OWED items from the build (patch log, 6): OWED-28-1..6; OWED-28-4 = call map
pending regeneration (done — see above); OWED-28-5 = build.sh
RULE_DIRS/RULE_FILES rewriter still lists cut families, no-op, left alone.

## §3 Audit-loop record

### Audit #77: NOT PASS (report `fix28/audit77-report.md`) — 1 blocking, 3 minor

- **77-A1 BLOCKING:** `dart-security.mdc` cut removes genuine kept-stack
  guidance — its Android/iOS manifest sections (`android:exported="false"` +
  intent-filter review, `FLAG_SECURE`, `NSAppTransportSecurity`, Info.plist
  usage descriptions, data-protection entitlement,
  `network_security_config.xml`, HTTP request timeouts) have zero hits
  anywhere in the kept tree (auditor grepped + read kept
  `react-native-security.mdc` in full), and the globs
  `**/AndroidManifest.xml` / `**/Info.plist` occur in Expo prebuild output
  (kept mobile path, `mobile-ship/SKILL.md:83`). SPEC §1(b)'s "removes no
  correct behavior" was false for this file. The other 6 NEEDS-DECISION files
  cleared (all framework-specific; generic lines duplicate kept alwaysApply
  rules; vue-hooks' only effect was the misfire itself).
- **77-B1:** 4 live hook files describe cut `run-with-flags.js` as caller in
  comments (block-no-verify.js:1266, post-edit-format.js:31,
  quality-gate.js:140, stop-format-typecheck.js:239) — comment-only.
- **77-B2:** `schemas/capsule-envelope.schema.json:5` names cut
  `eval-harness/envelope.js` as "the enforcing implementation" (description
  string).
- **77-B3:** F2 left unused `path`/`readFile` imports in `evaluate-session.js`
  + stale "Continuous Learning" header/prefix (valid JS, `node --check`
  passes).
- Verified clean: dispatch hunt (independent sweep incl. hooks/scripts/
  manifests/schemas, zero live), vite-patterns dormancy stands, posttooluse/
  control-pane unwiring correct, F1/F2/F4/react-patterns correct.

**Fixes for #77 (in fix28.py + template, §5d–§5g):** 77-A1 — ported the 9
framework-neutral manifest/network bullets into kept
`rules/react-native-security.mdc` as a new "Native Manifests" section
(DARTSEC_F28) + 2 network bullets into its Network section + the two manifest
globs added to frontmatter so guidance loads on those files (NOT a full
restore — the ~80% Flutter content stays cut). SPEC §1(b) corrected to record
the exception honestly. 77-B1 — reworded all 4 comments. 77-B2 — schema
description reworded (dropped the Mirrors/enforcing clause). 77-B3 — removed
dead imports, retitled header to "Session Evaluator" and log prefix
`[ContinuousLearning]` → `[SessionEvaluator]` (2 occurrences;
`learnedSkillsPath` still used, kept). verify28 gained check 10h (4 checks)
+ BASE abspath fix (`.` as arg broke log/sidecar paths; now 110/110 even
with `.`).

Run 6 PASSED (exit 0) with all #77 fixes. verify28 run 4: 109/110 — check 12
failed on 1 hit: the port's own intro line ("Ported from the cut
`dart-security` rule") triggers the extended sweep. Fixed by adding the
designed prose-history allow-list entry
(`rules/react-native-security.mdc:47`), not by hiding provenance.
**verify28 run 5: 110/110, exit 0.**

### Audit #78: NOT PASS (report `fix28/audit78-report.md`) — 0 blocking, 1 minor

- **78-B1:** SPEC §2(a) item 5 still prescribed deleting `workflow-quality`'s
  `dependencies` key entirely ("do not leave `dependencies: []`"), the
  opposite of the shipped `[]` fix — following it would crash all 7 profile
  resolves. Fixed: SPEC item 5 corrected to prescribe emptying to `[]`,
  citing install-manifests.js:611/:636 and the verify28-run-1 catch, noting
  the Audit #6 pop-the-field convention does not apply here.
- Everything else cleared (all 84 paths exist, zero dangling refs, zero
  `skill-unified-memory`/`business-content` hits in tree, 22 kept components
  correctly described, 10-file liveness spot-check holds, both build fixes
  correct incl. template parity, weaving intact incl. D19 ×339, call map
  consistent). Auditor re-ran verify28: 106/106.

### Audit #79: PASS (report `fix28/audit79-report.md`) — 0 blocking, 0 minor

Re-audit verified all fixes: SPEC corrections, DARTSEC port bullet-by-bullet
(9 bullets trace to verbatim source bullets; Flutter-term grep returns only
the port-note lines; globs added; coherent with the file), B1/B2/B3 landed,
re-sweep clean (75 CUT rules absent — only 2 stem hits: allow-listed DARTSEC
note + deliberate `vue-patterns` component keep; 135 dead scripts absent —
only 3 prose hits), verify28 110/110 on both the standard invocation and `.`
from inside `hackathon-ecc/`, call map regenerated and matching.

### Sweep #36: NOT CLEAN (report `fix28/sweep36-report.md`) — 0 blocking, 1 minor

- **36-B1 MINOR:** staged edit-sources still carry imperative dispatches to
  CUT skills; the shipped tree is correct only because fix27.py rewrites them
  at build time. `new-skills/orchestrate/SKILL.md:104` dispatches to CUT
  `conventional-commit-review`; `new-skills/integration/SKILL.md:21,46,60,122`
  dispatch to CUT `skill-scout` / `mcp-server-patterns`;
  `new-skills/orchestrate/SKILL.md:8,114,381` list CUT `codehealth-mcp` /
  `santa-method` / `security-scan` as deferred checks. Built tree clean on
  every one (fix27.py rewrites them; verify28 check 10 guards the patched
  text). MINOR, not BLOCKING — but the edit source contradicts the shipped
  tree, and correctness depends on patch anchors in another file.
- Checked and cleared: weaving coherence CLEAN (all 20 `_F27` tokens present;
  no CUT rule file or dead script carried any `_F27` token; DESIGNPKG-AUTO /
  PALETTE-FIRST / ALWAYSLEAD / GRILLHDR / THEME-START / D19 routing lines
  read in kept files; 4+ skills still route design decisions through the
  design package); stale counts CLEAN (zero hits for all seven stale strings
  in built tree and staged sources; stock-ECC line "144 skills, 69 agents,
  121 rules, 94 commands" present unchanged at README.md:11); dangling
  references CLEAN in shipped tree (CUT rule filenames 0 hits; rule stems
  only 2 prose hits; dead scripts only 2 prose hits; CUT-skill path forms 0;
  removed agents 0; dropped commands 0; backticked CUT skills 22 hits, all
  prose-history/negative); README CLEAN (counts 67/45/48/55 everywhere;
  fix #28 note present exactly once with all four tokens).

**Fix for 36-B1 (fix #28, post-sweep — NOT fixed post-hoc without
verification; re-sweep #37 pending):** the 8 staged lines were aligned with
the patched text by copying the built tree's lines into the staged files
(byte-identical at those lines; `conventional-commit-review`,
`codehealth-mcp`, `santa-method`, `security-scan` now ABSENT from both staged
files; the remaining `skill-scout` / `mcp-server-patterns` hits are the
REROUTE notes themselves, prose-history as in the built tree). The 8
now-redundant fix27.py `sub()` calls were retired (6f(a) 1 call, 6g
orchestrate 3 calls, 7g B9 4 calls) with comments citing sweep #36-B1; the
orch-build-mvp 6g call and the security-review 6f(b) call STAY — those files
are ECC-origin, not staged sources, so the patch is their only mechanism.
verify27.py still asserts the re-routes / deferred lists in the built tree,
so a regression would fail verification loudly.

**Scoping note (same diff, deliberately NOT fixed):** the staged-vs-built
diff for these two files has 4 further hunks — orchestrate :99/:272/:279
(`code-reviewer` → house form `code-reviewer` agent
(`agents/ecc-code-reviewer.md`)) and integration :3 (build.sh
`replace_desc_line` scoping rewrite, verbatim at build.sh:592–594). These
contain no CUT-skill dispatch and are assembly patches by design (upstream
renames / scope clarifications), not fix #27-cut fallout — aligning them
would mean editing build.sh's patch table, out of scope for fix #28. The
re-sweep brief asks it to confirm this scoping (zero CUT dispatches in staged
sources), not byte-identity between staged and built files. **Correction
(sweep #37):** the orchestrate renames are done by `fix24/fix24.py`'s
house-form normalizer (invoked at build.sh:24064), not by build.sh itself —
substance unchanged, no CUT-skill dispatch in any hunk.

### Sweep #37: CLEAN (report `fix28/sweep37-report.md`) — 0 blocking, 0 minor

Re-sweep of the run-7 built tree + staged sources, same scope as #36. The
sweeper verified independently (own greps/diffs/reads; re-ran verify28.py
itself: 110/110, exit 0):

- **36-B1 re-check — FIXED:** all 8 aligned lines carry the patched text and
  are byte-identical to the built lines. Whole-staged-dirs grep for the 6 CUT
  names returns exactly the 4 integration REROUTE "was cut" notes;
  `conventional-commit-review`, `codehealth-mcp`, `santa-method`,
  `security-scan` occur zero times in staged sources. All 8 retired fix27.py
  sub() calls confirmed gone by reading the code; the 6f(b) security-review
  and orch-build-mvp 6g calls correctly stay.
- **Scoping (BY DESIGN, not findings):** the only 4 staged-vs-built hunks
  are orchestrate :99/:272/:279 (fix24 house-form renames) and integration :3
  (build.sh:592–594 `replace_desc_line`). No CUT-skill dispatch in any hunk.
- **Weaving:** all 20 `_F27` tokens present; DESIGNPKG-AUTO / palette-first /
  ALWAYSLEAD / grill-me-first / /demo under-2:10 local-only /
  Hallmark-as-starting-point / D19 all intact; DARTSEC port well-formed.
- **Stale counts, dangling refs, README:** zero stale counts in built tree +
  staged sources; 0 CUT rule files on disk, 0 removed-agent / 0
  dropped-command path refs, all 135 dead scripts absent, manifests 14/84/55,
  no `codebase-memory-mcp` in mcp.json; README counts 67/45/48/55 everywhere,
  fix #28 note exactly once with all four tokens.
- **One honest limit (recorded in the report §(h), not a finding):** the
  run-7-vs-run-6 byte-identity claim couldn't be fully re-verified by the
  sweeper (no run-6 tree is retained). It rests on the coordinator's md5 diff
  (2,259 files, excl. `node_modules`, zero differences — lists at
  `/tmp/f28run6/tree-md5.txt` and `/tmp/f28run7-md5.txt`, ephemeral); the
  sweeper verified instead that both staged files diff against their built
  counterparts with only the 4 expected assembly hunks, and that verify28
  passes 110/110 on the run-7 tree itself.

**SPEC §6 criterion verdict: MET** — sweep CLEAN and weaving-coherence CLEAN,
closing the open item from sweep #36.

### Dry-run #43: PASS (report `fix28/dryrun43/dryrun43-report.md`)

All five legs ran against the fix #28 run-6 built tree (starting state verified
this session: build.sh 24,119 lines, md5 `06e3611b…`; counts 67/45/48/55/15,
triggers 49; verify28 run 5: 110/110; regenerated call map md5 `b066413a…`).

- **Leg 1 — Fixtures: 101/101** (42/42 dry-run #37 regression + 59/59 fix #23),
  both runners verbatim copies of #42's.
- **Leg 2 — Home Run render: all 17 §6 assertions PASS, 0 flags** — 52
  measurements, 13 states × 4 widths, 0 console errors, 0 failed requests;
  status vertical centers delta 0. Fix #28 touches no render files (verified:
  zero `cold-start-render` refs in fix28.py/SPEC; render mtimes Nov 13; only
  build.sh hit is the pre-existing fix #23 comment). Fresh vs prior JSON
  differs only in the 4 trip-wrongcode input rects (1–3px shake timing, group
  offset 0) — the known pattern. Campus Eats benchmark: **6/7 static PASS;
  dimension 7 (alignment) OWED**, never passed — no Campus Eats render exists.
  R1/R4 stay OWED as defined.
- **Leg 3 — /demo: 59/59** — `qa.mjs` exit 0 twice, 12/12 stills + 2 sheets,
  0 Google Fonts requests; npm install exit 0; record 75.5s/8 moves; frames
  2281 (76.0s); Remotion 4.0.526 checks all exit 0; Playwright installer first
  try. Same 2 non-blocking record warnings as #41/#42.
- **Leg 4 — Cursor-readiness: 37/37** verbatim, incl. 13 live C-1 hook pipe
  tests.
- **Leg 5 — Call-graph: 17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN**
  against the regenerated fix28 map. Uncalled is 17 (was 16): `vite-patterns`
  is newly uncalled — traced cause: its only strong invokers in the fix #27
  map were the 9 CUT nuxt/vue rule files, so the cut working as specified,
  not a regression. Second-order orphans unchanged at 7. Technical-depth
  fixture: **11/11 + 6/6** (echo p95 3 ms). /test-coverage Steps 1–2: 5
  passed, calc.py 68.2%.

Findings: none blocking. Two first-run incidents, both non-plugin: a service
restart killed the first align-harness attempt mid-run (re-ran clean), and Leg
5's first run flagged `wire:test-coverage` BROKEN only because the companion
exercise hadn't been run yet in that session (re-ran green after it). Grok pins
50/70 with bare 0 (down from #42's 56/74 — delta traced to pin mentions in the
cut files); banned terms 3 hits, all allow-listed MotionSites, 0 unallowed.
Scratch bulk cleaned (9.3 MB kept); no servers left running. No plugin, build,
render, or verifier file was edited.

**Observation carried from #42 — REFUTED, no fix:** the report repeats that
README.md:67-68 "still lists the dropped `/epic-*` commands as shipping".
That premise is wrong and was already corrected in the fix #27 MANIFEST: all 7
epic commands (`epic-claim`, `epic-decompose`, `epic-publish`, `epic-review`,
`epic-sync`, `epic-unblock`, `epic-validate`) are KEPT and ship — verified
this session by direct listing of `hackathon-ecc/commands/` (all 7 files
present) and `fix27/verify27.py:201–202` (KEPT_COMMANDS). The README listing
is accurate; the dry-run worker repeated the already-refuted claim without
checking the fix27 manifest correction.

### Build run 7 (after the 36-B1 fix): PASSED, tree byte-identical

- Build run 7: exit 0, `build complete`, counts 67/45/48/55/15. Build log:
  `fix28/build-log-run7.txt` (ERRORS: 0, CHANGES: 649, REMOVALS: 88; the 10
  "error" lines in the log are benign file paths / prose / "Errors (0)").
- **Built tree byte-identical to run 6:** full-tree md5 diff (2,259 files,
  excl. `node_modules`) — zero differences. The 36-B1 staged alignment +
  fix27.py patch retirements change nothing shipped, as designed.
- fix27 patch log: `## Errors (0)`, "skills removed: 100 dirs" present; the 8
  retired orchestrate/integration patch entries are gone (remaining
  `conventional-commit-review` / `skill-scout` / `mcp-server-patterns` hits
  are the CUT roster, the KEPT orch-build-mvp + prp-commit + skill-create
  patches, the pi-core list, and the OWED-13 census text). fix28 patch log:
  `## Errors (0)`; REACTA11Y/NDMISFIRE/ORCHKEEP tokens present (3).
- **verify28 run 6: 110/110, exit 0** (`fix28/verify28-run6.log`, run-7 tree).
- **verify27 re-run (diagnostic, retired verifier):
  `fix28/verify27-rerun-after36B1.log` — 76/79, exit 1**, failing ONLY on the
  three codified tails predicted by SPEC §6: counts (123 rules), README count
  line (123 rules), check 12b (28 "allow-listed file missing" hits — exactly
  the 28 CUT rule files named in verify27's ALLOW_LIST; zero live dispatches).
  Check 12 (main sweep) PASSED; all content checks (orchestrate re-route,
  deferred lists, B9 integration, trigger notes) PASSED — the 36-B1 fix broke
  nothing. (SPEC §6 also predicted a manifest-counts failure; it did not
  occur — verify27's manifest check covers only pi-core M-new-4, which is
  unchanged. Fewer failures than predicted, not a problem.)

## §4 SPEC §6 criterion statuses (honest)

| Criterion (SPEC §6) | Status |
|---|---|
| Audit #77 (or next number): ZERO blocking, ZERO minor | **MET via #79** — #77 NOT PASS (1 blocking, 3 minor) → fixed → #78 NOT PASS (0 blocking, 1 minor) → fixed → #79 PASS (0 blocking, 0 minor). All three reports standalone in `fix28/`. |
| Sweep #36 (or next number): CLEAN, weaving-coherence CLEAN | **MET via #37** — #36 NOT CLEAN (1 open minor, 36-B1) → fixed → **#37 CLEAN (0 blocking, 0 minor)**, weaving coherence CLEAN. |
| Dry-run #43 (or next number): PASS | **MET** — PASS, all 5 legs (see §3). The carried `/epic-*` observation was refuted (epic commands KEPT and shipping); no fix needed. |
| verify28.py: checks for every placement, exit 0 | **MET** — 110/110, exit 0 (run 5 on run-6 tree; **run 6: 110/110 on run-7 tree** after the 36-B1 fix). Counts asserted: skills 67, agents 45, rules 48, commands 55, hooks 15, triggers 49; modules 14 / paths 84 / components 55; profiles research 7 / full 14; 75 CUT rules absent + 48 kept present; 135 dead scripts absent; mcp.json no `codebase-memory-mcp`; README 67/45/48/55; F1/F2/F4/react-patterns re-asserted; `resolveInstallPlan` succeeds for every profile; pi-core M-new-4 re-run unchanged; no CUT skill name in any manifest `paths` array. |
| Prior verifiers: re-run; verify27.py expected to FAIL only on the codified tails | **MET as a diagnostic** — verify27.py re-run after build run 7 (`fix28/verify27-rerun-after36B1.log`): **76/79, failing ONLY on the codified tails** (counts 123 rules, README 123-rules line, check 12b's 28 missing allow-listed CUT rule files). verify27.py is RETIRED/superseded by verify28.py (same precedent as fix #27 §4: verify26/verify25 retired). |
| Banned terms: 0 in the built tree (same list as fix #27). Grok pins only: `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never bare `grok-4.6-high-fast`. | **MET** — verify28 asserts; run 5 clean. Re-assert on run 7. |
| Anchor tokens: new `_F28` family (`CUTRULES_F28`, `MANIFEST28_F28`, `DEADSCRIPTS_F28`, `EVALSESS_F28`, `README48_F28`, `REACTA11Y_F28`, `NDMISFIRE_F28`, `ORCHKEEP_F28`) — census reconciles staged + built. | **MET** — verify28 check 7 asserts; run 5 clean. Plus DARTSEC_F28 (audit #77 port). |
| Manifest: fix28/MANIFEST.md with disposition table, anchor tokens, open parent adjudications, dry-run caveat if any check is environment-limited. | **THIS FILE** — disposition §2, tokens §2(d), open adjudications §5. Dry-run caveat: see §3 (pending). |
| Builds use the fix #26 env-redirected invocation; staged sources only; build.sh source of truth; only build.sh edit is the fix28.py invocation. | **MET with two noted exceptions:** build.sh:25 `MS_SRC` fix (latent bug, run 1) and the fix28.py hook are the only build.sh edits. Staged sources only, except via fix28.py (and the 36-B1 staged-file alignment + fix27.py patch retirements, §3). Never re-ran fix11/fix11-stage.py. |

## §5 Open parent adjudications

1. **Orchestration module keep** (dead-weight audit): `orchestration-session.js`
   + `tmux-worktree-orchestrator.js` are runtime-dead but the whole
   orchestration module; cutting deletes a profile module. Parent decision
   whether to cut the module outright.
2. **22 install components kept** (4 dead `skill:*` + 18 dead lang/framework):
   kept with description corrections because deletion throws `Unknown install
   component`. Parent decision whether deletion (with the selector-behaviour
   change) is acceptable.
3. **`motionsites-web-builder` module membership:** kept skill in no module
   (reachable only via synthetic component). One-line add to
   `hackathon.paths` is a parent decision (addition, not prune).
4. **36-B1 scoping (assembly patches):** orchestrate :99/:272/:279
   (`fix24/fix24.py` house-form normalizer, invoked at build.sh:24064) and
   integration :3 (build.sh `replace_desc_line`) still differ staged-vs-built
   by design. Parent decision if staged alignment of assembly patches is
   ever wanted — not recommended; they are the assembly mechanism.

## §6 Owed / environment-limited items (recorded, not verified)

- **OWED-28-5:** build.sh RULE_DIRS/RULE_FILES rewriter still lists cut
  families — no-op, left alone.
- **OWED-28-1..6** (patch log): OWED-28-4 (call map regeneration) DONE;
  others are record-only (see fix28.py patch log).
- **`vite-patterns` intentionally dormant** (only invokers were cut nuxt/vue
  rules) — recorded in `fix28/callmap/wiring-list.md`, not a defect.
- **verify27.py / verify26.py / verify25.py:** RETIRED on the reduced tree
  (verify27 fails on the codified tails only, by design); verify28.py is the
  live verifier. Re-run of verify27 after build run 7 is a diagnostic, not a
  gate.
- **Call-map generator** (`fix28/callmap/generate_call_map.py`): does NOT
  byte-reproduce the staged file (known fix26 incident); copy-aside → run →
  diff → restore procedure used. Two generator defects fixed (Rules (123)
  header, B6 note).
- **`/tmp/ecc-repo-clean` missing** (tmp wiped again); `fetch_repo` re-clones
  from GitHub each build. Durable upstream clones at
  `fix26/scratch-clones/` (uipro 6ae86f6, hack-skills f210c6d, chwezi d7d85b6
  — all match pins). `ecc-repo-clean` durable copy is EMPTY (0 entries).

## §7 Push

- Remote: `github.com/anishkoduri/hackathon-ecc`, branch `main`. Pre-fix HEAD:
  `b7d0f75` (fix #27). **Do NOT push from the sandbox (no GitHub auth).**
- Method: sync the working copy's changes into `fix28/scratch-repo`, commit
  as Anish Koduri <akoduri05@gmail.com> with NO "Co-authored-by: Cursor"
  trailer and no AI tool listed as contributor/author, create a verified git
  bundle (`git bundle verify` OK). Anish pulls the bundle from his Windows
  machine and pushes, as with fix #27: `git pull <bundle> main` +
  `git push origin main`.
- The commit hash and bundle path/size are verified by the coordinator after
  committing and reported in the final report (this manifest is the pre-push
  record, per the fix #26 convention — it does not contain its own commit's
  hash).
- Sync record (main → scratch-repo, verified before commit): built tree
  `hackathon-ecc/` (rsync `--delete`, incl. `node_modules` — 0 diffs after
  sync, excl. and incl. node_modules); `build.sh` (already identical, md5
  06e3611b…); regenerated `new-skills/orchestrate/references/call-map.md`;
  `fix28/` (excl. `scratch-repo/`, `scratch-tmp/`, `__pycache__`,
  `dryrun43-scratch/`); the 36-B1 files (`new-skills/orchestrate/SKILL.md`,
  `new-skills/integration/SKILL.md`, `fix27/fix27.py`); plus
  `fix27/fix27-patch-log.md` (regenerated run-7 log, tracked) and
  `fix16/fix16-run-log.md` (build-regenerated log; run-7 version differs only
  by one bullet line moving 499 → 494 — content identical, ordering noise).
  Two sync mistakes caught and fixed before commit: a stray
  `new-skills/orchestrate/call-map.md` from a mis-aimed `cp` (deleted), and
  the fix16 log initially unsynced (a multi-source `cp` to a file target
  fails silently under `&&` chaining — copied individually after).
