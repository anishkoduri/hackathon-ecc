# Sweep #37 — fix #28 — INDEPENDENT RE-SWEEP REPORT

**Verdict: SWEEP #37: CLEAN** — 0 blocking, 0 minor. Finding 36-B1 is
confirmed fixed in the staged sources; the run-7 built tree passes every
check in the sweep #36 scope.

**Scope.** Re-sweep of the run-7 built tree (`hackathon-ecc/`) + staged
sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`), same scope as sweep #36: 36-B1 re-check, staged-vs-built
scoping check, weaving coherence, stale-count sweep, dangling-reference
sweep, README consistency, SPEC §6 criterion cross-check. Read-only
except this report. I did not trust the coordinator's claims: every item
below was verified by my own greps, diffs, and file reads. `verify28.py`
was re-run by me (110/110, exit 0 — see below), not merely read.
`verify27.py` was re-run by the coordinator after the 36-B1 fix and its
log was read (76/79, failing only on the codified tails — see (f)). No
live-browser or Cursor-session check was needed or performed. `build.sh`
was not run; `fix11/fix11-stage.py` was not run; nothing was committed,
pushed, or messaged.

---

## BLOCKING findings

None. (Numbered 37-Ax: none issued.)

---

## MINOR findings

None. (Numbered 37-Bx: none issued.)

---

## Notes / observations (checked and cleared)

### (a) 36-B1 re-check — FIXED, confirmed in the staged sources

All 8 aligned lines now carry the patched text, and the staged sources
contain zero live dispatches to CUT skills:

- `new-skills/orchestrate/SKILL.md:104` now reads "draft each commit
  message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`)"
  — the `conventional-commit-review` dispatch is gone. Line 8 and line
  114 list only the three kept deferred checks
  (`verification-loop`, `production-audit`, `delivery-gate`, DEFER3_F27);
  line 381 likewise lists only the three kept checks. All four lines are
  byte-identical to the built file's lines 8, 104, 114, 381 (verified by
  `sed -n` read of both files).
- `new-skills/integration/SKILL.md:21, 46, 60, 122` now carry the
  re-routes (`documentation-lookup` for discovery,
  hand-rolled `api-integration` for server setup) with the REROUTE_F27
  "was cut" notes. All four lines are byte-identical to the built file's
  lines 21, 46, 60, 122.
- Whole-staged-dirs grep for the six 36-B1 CUT names
  (`conventional-commit-review`, `skill-scout`, `mcp-server-patterns`,
  `codehealth-mcp`, `santa-method`, `security-scan`) over `new-skills/`,
  `round2-skills/`, `rewritten-skills/`, `new-rules/` returns exactly 4
  hits — the four integration REROUTE "was cut" notes above, and nothing
  else. `conventional-commit-review`, `codehealth-mcp`,
  `santa-method`, and `security-scan` occur zero times anywhere in the
  staged dirs. The remaining `skill-scout` / `mcp-server-patterns` hits
  are ONLY the REROUTE notes themselves, as required.
- `fix27.py` retirement verified by reading the code, not just the
  comments: the 6f(a) orchestrate `conventional-commit-review` sub() is
  gone (comment block at :448–453 only, no sub() call follows it); the
  three 6g orchestrate deferred-list sub() calls are gone (comment block
  at :472–479 only); the four 7g B9 integration sub() calls are gone
  (comment block at :693–697 only). The calls that stay are present and
  live: 6f(b) `security-review` sub() (:454–461) and the 6g
  `orch-build-mvp` deferred-list sub() (:480–486) — both ECC-origin
  files, where the patch is the only mechanism. Count reconciles: 1 + 3
  + 4 = 8 retired, as claimed.

### (b) Scoping check — the 4 remaining staged-vs-built hunks are BY DESIGN

Own `diff` of each staged file against its built counterpart shows
exactly 4 hunks, no others:

- `orchestrate` :99, :272, :279 — bare `` `code-reviewer` `` becomes
  house form `` `code-reviewer` agent (`agents/ecc-code-reviewer.md`) ``
  (and `security-reviewer` likewise at :279). No CUT-skill dispatch in
  any of the three hunks; `ecc-code-reviewer` is the kept ECC agent.
  Mechanism verified: the rename is **not** in `build.sh` itself and
  not in `fix27.py`/`fix28.py` — it is `fix24/fix24.py`'s house-form
  normalizer (fix24.py:364 logs the exact "house form:" lines seen in
  the run-7 build log at :2018–2020, e.g. :403–404 for the code-reviewer
  rewrite), invoked by `build.sh:24064`. Correction to the task brief's
  shorthand ("build.sh renames"): build.sh invokes fix24.py, which does
  the rewrite. The substance is unchanged — a build-time assembly patch,
  by design.
- `integration` :3 — the frontmatter `description:` scoping rewrite
  (sponsor-track / track-picker scoping). Verified verbatim as
  `build.sh:592–594` `replace_desc_line("integration", …)` — old string
  matches the staged line exactly, new string matches the built line
  exactly. No CUT-skill dispatch in either version.

### (c) Weaving coherence — CLEAN

- **All 20 `_F27` tokens present in the built tree** (own census, excl.
  `node_modules`): DESIGNPKG-AUTO (2 files), CEILING (2), DELRISK (2),
  CHECKSRC (3), AUDITGUIDE (3), NOCOAUTHOR (2), THEME-START (7),
  ALWAYSLEAD (2), IMPL46 (1), GRILLHDR (4), CAPTURE1 (1), TESTNOTBQA
  (1), DEFER3 (3), W2 (2), W3 (4), W4 (1), TESTPASS (1), REROUTE (11),
  MOTIONSITES (3), PALETTE-FIRST (3).
- **Design-package auto-routing intact, read not counted:**
  `rules/hackathon-mode.mdc:44` and `skills/orchestrate/SKILL.md:35`
  carry the full DESIGNPKG-AUTO_F27 paragraph (design decision → always
  a design-package skill; design-lead Taste decides; theme deal is the
  starting point, THEME-START_F27; palette first, PALETTE-FIRST_F27).
  `skills/design-taste-frontend/SKILL.md:224` carries the palette-first
  inventory rule; `skills/orchestrate/SKILL.md:138` (routing-table row
  10) names design components per UI surface.
- **Orchestrator-leads-every-prompt (ALWAYSLEAD_F27)** present in
  `rules/hackathon-mode.mdc:12,48` (grill-me first on any first project
  prompt; orchestrate leads every multi-piece run for the life of the
  project).
- **Grill-me first-prompt behavior intact:** `hackathon-mode.mdc:12`
  (run `grill-me` FIRST, before scoping/building/expansion; skip via
  "skip the grilling" / "just build it").
- **/demo filming rules intact:** `commands/demo.md:9,11` — video under
  2:10, films the local app from the project directory, never a deployed
  URL.
- **Hallmark-as-starting-point (THEME-START_F27)** present in 7 files
  (census count above, same set as #36).
- **D19 reasoned decisions intact:** "D19" occurs x29 in
  `skills/orchestrate/SKILL.md` and x33 in
  `skills/design-taste-frontend/SKILL.md`.
- **DARTSEC port well-formed:** `rules/react-native-security.mdc`
  frontmatter parses with globs `**/*.ts`, `**/*.tsx`,
  `**/AndroidManifest.xml`, `**/Info.plist`; the Native Manifests
  section (lines 45–60) is coherent Expo guidance (`android:exported`,
  intent filters, `FLAG_SECURE`, `NSAppTransportSecurity`); the only
  `dart-security` mention is the port note itself (line 47,
  `(DARTSEC_F28)` line 49).
- **Counts re-verified on disk:** 67 skills / 45 agents / 48 rules / 55
  commands; `hooks/hooks.json` registers 15 events.

### (d) Stale-count sweep — CLEAN

Zero occurrences in the built tree (excl. `node_modules`) of "123 rules",
"121 rules as-shipped", "166 skills", "72 agents", "87 commands",
"66 skills", "60 commands" (own grep). Zero in the staged sources
(`new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/`)
for the same seven strings. The stock-ECC line "144 skills, 69 agents,
121 rules, 94 commands" is present and unchanged at `README.md:11` —
upstream stock text, not our counts, correctly not counted as a failure.

### (e) Dangling-reference sweep — CLEAN

Own greps using the `fix28/verify28.py` lists (100 CUT skills, 27
removed agents, 32 dropped commands, 75 CUT rules, 135 dead scripts),
over the built tree and the staged dirs:

- **CUT rule filenames:** 0 files on disk in `hackathon-ecc/rules/`
  (all 75 absent; all 48 kept present per verify28). **CUT rule stems
  in the built tree:** 2 hits, both adjudicated non-live as in #36 —
  `dart-security` only in `rules/react-native-security.mdc:47` (the
  DARTSEC port note, prose-history) and `vue-patterns` only in
  `manifests/install-components.json:426` (`skill:vue-patterns`, the
  deliberate SPEC §2(b) keep with the "(Removed in fix #27…)" note, not
  a dispatch).
- **Dead scripts:** all 135 files absent on disk (0 present). Precise-path
  hits in prose only, as in #36: `scripts/hooks/context-routing-index.js`
  + `scripts/lib/context-pack-registry.js` in the call map's B6 note
  (past-tense documentation of the removed chain) and
  `scripts/hooks/posttooluse-dispatcher.js` in
  `commands/quality-gate.md:44–47` (explicitly states the dispatcher
  "is not referenced by `hooks/hooks.json` or anything else in the
  plugin, so it never runs"). No live reference.
- **CUT skills, path form (`skills/<name>/`):** 0 hits in the built tree
  for the 36-B1 names (and verify28 check 12, re-run by me, asserts 0
  un-allow-listed CUT-name hits tree-wide). **Backticked CUT skills
  (the 6 36-B1 names) in the built tree:** 4 hits excl. the call map —
  the four integration REROUTE "was cut" notes, prose-history only. No
  live dispatch. **Backticked CUT skills in hooks/scripts/manifests/
  schemas/mcp.json/package.json:** 0 hits (verify28 check 12 covers
  this; re-run passed).
- **Removed agents (`agents/<name>.md`):** 0 hits in the built tree (all
  27 names). **Dropped commands (`commands/<name>.md`):** 0 hits in the
  built tree (all 32 names). **Staged dirs:** 0 removed-agent and 0
  dropped-command path refs.
- **Manifests:** 14 modules / 84 paths / 55 components re-verified by
  JSON read; no module path names a CUT skill; the only CUT-named
  component is the deliberate `skill:vue-patterns` keep above.
  `mcp.json` has no `codebase-memory-mcp` key (grep 0 hits for
  `codebase-memory` in `mcp.json`; no `codebase-memory-mcp` anywhere in
  the built tree excl. `node_modules`).
- **Observation, cleared (carried from #36):**
  `new-skills/codebase-memory/SKILL.md` still exists as a staged source
  and `build.sh:222` copies it into the tree, but fix27.py removes it on
  every build — the built tree has no `codebase-memory` skill (0 hits
  under `hackathon-ecc/skills/`; the 67-skill count confirms). Same
  copy-then-remove pattern as the 36-B1 files; with 36-B1 now fixed in
  the staged sources, this is the only remaining instance of the
  pattern, and it is not a dispatch to a CUT skill — no action.

### (f) README consistency — CLEAN

Every count the README states about the plugin reads 67 skills / 45
agents / 48 rules / 55 commands (line 13: "67 skills, 45 agents, 48
rules, and 55 commands in total (42 agents as-shipped + 3 staged
orchestrate agents; 46 rules as-shipped + 2 new rules — `hackathon-mode`,
`ponytail` …)"; lines 36, 38, 40 use 67 skills / 45 agents / 55 commands
consistently). The fix #28 provenance note is present exactly once at
line 29 with all four tokens (`CUTRULES_F28` `MANIFEST28_F28`
`DEADSCRIPTS_F28` `README48_F28`, one occurrence each). No
inconsistency found.

### (g) Verifier runs — my own re-runs

- **`verify28.py`, re-run by me: 110/110 checks pass, exit 0.**
  (Tail: "PASS CUT-name sweep: zero live dispatches…", "PASS check 12b:
  no imperative dispatch to a CUT skill/agent/command hides in an
  allow-listed line", "110/110 checks pass".)
- **`verify27.py` diagnostic re-run (coordinator's log
  `fix28/verify27-rerun-after36B1.log`, read not re-run): 76/79**,
  failing ONLY on the three codified tails — counts (123 rules), README
  count line (123 rules), and check 12b (28 allow-listed lines for the
  missing CUT rule files). This matches the coordinator's claim exactly;
  no other failures.
- **Build log run 7** (`fix28/build-log-run7.txt`, read): ends `build
  complete`, counts 67/45/48/55/15.

### (h) Byte-identity claim — spot-checked, not fully re-verifiable

The coordinator's claim that the run-7 built tree is byte-identical to
the run-6 tree could not be independently re-verified in full: no run-6
built tree is retained anywhere in the workspace
(`fix28/scratch-repo/` is the pre-cut tree, not a run-6 build), so there
is nothing to diff run 7 against. What I did verify instead: (a) my own
diff of both staged files against their built counterparts shows ONLY
the 4 expected assembly hunks (§(b) above) — i.e. the staged sources
and the shipped tree agree everywhere except documented build-time
patches; (b) my own `verify28.py` re-run passes 110/110 against the
run-7 tree. This is a limit on verifying the coordinator's
reproducibility claim, not a finding against the tree — the tree I swept
is the run-7 tree itself, and it passes every check. If the parent wants
the identity claim itself proven, a rebuild would have to be compared
against a retained run-7 snapshot; that was out of scope for this sweep
(build.sh was not to be re-run).

### SPEC §6 criterion verdict — MET

Note on numbering (as in #36): the task brief cites "SPEC §6 (not §7 —
§7 is Non-goals)"; the sweep's own criterion in §6 reads: "Sweep #36
(or next number): CLEAN, weaving-coherence CLEAN for the whole tree."

- Weaving coherence, taken alone: **CLEAN** — all 20 `_F27` tokens
  present, design-package routing read in the kept skills, grill-me /
  /demo / theme / D19 / ALWAYSLEAD all intact (see (c)).
- The sweep criterion as written: **MET** — this sweep is CLEAN (0
  blocking, 0 minor), 36-B1 is fixed in the staged sources and confirmed
  by re-sweep, and weaving coherence is CLEAN. This closes the open item
  that made sweep #36 NOT MET as written.

### Other

- No file was edited, created, or deleted except this report.
  `build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing was
  committed, pushed, or messaged.
