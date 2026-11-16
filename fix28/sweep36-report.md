# Sweep #36 — fix #28 — INDEPENDENT SWEEP REPORT

**Verdict: SWEEP #36: NOT CLEAN** — 0 blocking, 1 minor (36-B1, staged-source
dispatches that are patch-covered in the shipped tree, not fixed post-hoc and
not re-swept).

**Scope.** Weaving coherence across the whole built tree + stale-count sweep +
broader dangling-reference sweep (built tree AND staged sources) + README
consistency + SPEC §7/§6 criterion cross-check. Read-only except this report
(and scratch under `fix28/sweep36-scratch/`, removed at the end). I did not
trust the coordinator's claims: every item below was verified by my own greps
and file reads against `hackathon-ecc/` (build run 6), the staged sources, and
`fix28/scratch-repo/` (pre-cut tree). `verify28.py` was NOT re-run as the
sweep; its run-5 log (110/110) was read as a claim and spot-checked instead.
No live-browser or Cursor-session check was needed or performed.

---

## BLOCKING findings

None. (Numbered 36-Ax: none issued.)

---

## MINOR findings

### 36-B1 — Staged edit-sources still carry imperative dispatches to CUT skills; the shipped tree is correct only because fix27.py rewrites them at build time

The built tree is clean (see "checked and cleared"), but the staged sources
— the edit source for staged files — still contain live-form dispatches to
skills cut in fix #27. They are neutralised on every build by fix27.py
patches and guarded by verify28.py check 10, so nothing wrong ships; but an
editor working from the staged source reads (and could extend) the wrong
text, and the correctness of the shipped tree depends on patch anchors that
live in a different file from the text they fix.

Evidence (staged `new-skills/`, each line verified by diff against the built
file, which carries the patched text):

- `new-skills/orchestrate/SKILL.md:104` — "draft each commit message with the
  `conventional-commit-review` skill (`skills/conventional-commit-review/SKILL.md`)"
  — `conventional-commit-review` is a CUT skill. Built
  `hackathon-ecc/skills/orchestrate/SKILL.md:104` re-routes to `git-workflow`
  (fix27.py:448–456, "conventional-commit-review skill — re-route to the kept
  git-workflow"); `grep conventional-commit-review` over the built file
  returns nothing.
- `new-skills/integration/SKILL.md:21, 46, 60, 122` — imperative dispatches
  to CUT skills `skill-scout` (:46, :122 — "Use `skill-scout` to search…")
  and `mcp-server-patterns` (:21, :60 — "Use `mcp-server-patterns` for the
  server setup…"). Built file re-routes all four to `documentation-lookup` /
  hand-rolled `api-integration` (verify28 check 10 B9 asserts the new text).
- `new-skills/orchestrate/SKILL.md:8, 114, 381` — the deferred-check lists
  still name CUT skills `codehealth-mcp`, `santa-method`, `security-scan`
  (e.g. :381 "one line per deferred check (`verification-loop`,
  `production-audit`, `delivery-gate`, `codehealth-mcp`, `santa-method`,
  `security-scan`)"). Built file lists only the three kept checks (verify28
  DEFER3_F27 checks assert this).

Why MINOR, not BLOCKING: the shipped tree contains zero of these dispatches
(verified: `skills/<cut>/` path forms 0 hits, backticked CUT-skill hits all
adjudicated prose-history/negative — see below), and verify28.py check 10
re-asserts the patched texts on every build, so a patch-anchor drift would
fail verification loudly rather than ship silently. The fix is editorial, not
a rebuild: bring the three staged files into line with the patched text (or
record the patch-dependence explicitly next to each staged line), so the edit
source stops contradicting the shipped tree. No re-sweep was run after
writing this finding — it is reported open, not fixed post-hoc.

---

## Notes / observations (checked and cleared)

### (a) Weaving coherence — CLEAN

- **All 20 `_F27` tokens present in the built tree** (own census, excl.
  `node_modules`): DESIGNPKG-AUTO, CEILING, DELRISK, CHECKSRC, AUDITGUIDE,
  NOCOAUTHOR, THEME-START, ALWAYSLEAD, IMPL46, GRILLHDR, CAPTURE1,
  TESTNOTBQA, DEFER3, W2, W3, W4, TESTPASS, REROUTE, MOTIONSITES,
  PALETTE-FIRST — each in at least one file. No `_F27` token was removed by
  the fix #28 cut: **no CUT rule file carried any `_F27` token** (checked
  each of the 75 files in `fix28/analysis/cut-rules-list.txt` against
  `fix28/scratch-repo/hackathon-ecc/rules/`; the only pre-cut rule files with
  `_F27` are KEPT `common-git-workflow.mdc` and `hackathon-mode.mdc`), and no
  dead script under `fix28/scratch-repo/hackathon-ecc/scripts/` carried one.
- **Design-package auto-routing intact, read not counted:**
  `rules/hackathon-mode.mdc:44` and `skills/orchestrate/SKILL.md:35` carry
  the full DESIGNPKG-AUTO_F27 paragraph (design decision → always a
  design-package skill; design-lead Taste decides; theme deal is the starting
  point, THEME-START_F27; palette first, PALETTE-FIRST_F27). At least 4 kept
  skills still route design decisions through the package, routing lines
  read: `orchestrate` (slice briefs name design components per surface,
  routing-table row 10), `orch-build-mvp/SKILL.md:41` ("Design package on
  every UI slice"), `feature-expansion/SKILL.md:152,196` ("Any feature that
  touches UI goes through the full design package"), `design-taste-frontend/
  SKILL.md:224` (palette-first inventory before the direction is finalised),
  plus `ui-ux-pro-max` (design-package references throughout, e.g. :29, :182,
  :212).
- **Orchestrator-leads-every-prompt (ALWAYSLEAD_F27)** present in
  `rules/hackathon-mode.mdc:12,48` and `skills/orchestrate/SKILL.md:14,59,61,
  120` (Grok 4.7 High pin, orchestrate leads every multi-piece run for the
  life of the project, not only the first build).
- **Grill-me first-prompt behavior intact:** `skills/grill-me/SKILL.md`
  frontmatter ("Runs FIRST, right after the user sends the first project
  prompt"), `hackathon-mode.mdc:12,60,62` and `orchestrate/SKILL.md:57`
  (precondition check on `docs/decision-record.md` / explicit skip,
  GRILLHDR_F27; one-question grill-now-or-proceed exception; first build runs
  fully autonomously after grill-me).
- **/demo filming rules intact:** `commands/demo.md:2,9,11` — video under
  2:10, films the local app from the project directory, never a deployed URL.
- **Hallmark-as-starting-point (THEME-START_F27)** present in 7 kept files:
  `hackathon-mode.mdc`, `orch-build-mvp`, `feature-expansion`,
  `design-taste-frontend`, `orchestrate`, `polish-pass/reference/
  slop-checklist.md`, `ui-ux-pro-max`.
- **D19 reasoned decisions intact:** "D19" occurs in `hackathon-mode.mdc`
  (x2), `orchestrate/SKILL.md` (x29), `design-taste-frontend/SKILL.md` (x33).
- **DARTSEC port does not break weaving:** `rules/react-native-security.mdc`
  frontmatter parses as YAML with globs `**/*.ts`, `**/*.tsx`,
  `**/AndroidManifest.xml`, `**/Info.plist`; the Native Manifests section
  (lines 45–60) and network bullets are coherent Expo guidance; the only
  `dart-security` mention in the whole built tree is the port note itself
  (line 47, `(DARTSEC_F28)` line 49); no Flutter/Dart content outside the
  note (the apparent line-49 hit is the substring "dart" inside the token
  `DARTSEC_F28` itself). It is a security rule with no design-package
  routing, so no weaving link passes through it.
- **Counts re-verified on disk:** 67 skills / 45 agents / 48 rules / 55
  commands; `hooks/hooks.json` registers 15 events.

### (b) Stale-count sweep — CLEAN

Zero occurrences in the built tree (excl. `node_modules`) of "123 rules",
"121 rules as-shipped", "166 skills", "72 agents", "87 commands",
"66 skills", "60 commands" (own grep; verify28 check 6 agrees). Zero in the
staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`) for the same seven strings. The stock-ECC line "144 skills, 69
agents, 121 rules, 94 commands" is present and unchanged at
`README.md:11` — upstream stock text, not our counts, correctly not counted
as a failure. Built call map has 0 occurrences of "123";
`fix28/callmap/call-map-before.md` still shows "123" (2 hits) as the
pre-regeneration snapshot, by design and out of scope — not flagged, per the
task brief.

### (c) Dangling-reference sweep — CLEAN in the shipped tree

Own grep sweeps with pattern files built from the `fix28/verify28.py` lists
(100 CUT skills, 27 removed agents, 32 dropped commands, 75 CUT rules, 135
dead scripts), over the built tree and the staged dirs:

- **CUT rule filenames:** 0 hits in the built tree. **CUT rule stems:** 2
  hits, both adjudicated non-live — `dart-security` only in
  `rules/react-native-security.mdc:47` (the DARTSEC port note, prose-history;
  verify28 check 12 allow-listed) and `vue-patterns` only in
  `manifests/install-components.json:426` (`skill:vue-patterns`, the
  deliberate SPEC §2(b) keep with the "(Removed in fix #27…)" note, not a
  dispatch). All 75 CUT rule files absent on disk; all 48 kept rules present.
- **Dead scripts (precise-path form):** 2 hits, both prose, none a dispatch
  — `scripts/hooks/context-routing-index.js` +
  `scripts/lib/context-pack-registry.js` in the call map's B6 note
  (past-tense documentation of the removed chain, "removed as dead weight in
  fix #28"), and `scripts/hooks/posttooluse-dispatcher.js` in
  `commands/quality-gate.md:44–47`, which explicitly states the dispatcher
  "is not referenced by `hooks/hooks.json` or anything else in the plugin, so
  it never runs". All 135 dead script files absent on disk. (A loose
  bare-stem sweep would return generic-filename noise — `server.js`,
  `index.js`, `config.js` — in unrelated files; the precise-path sweep is the
  correct test, as audit #79 also found.)
- **CUT skills, path form (`skills/<name>/`):** 0 hits in the built tree.
  **Backticked CUT skills in the built tree:** 22 hits excl. the call map,
  every one adjudicated non-live — "was cut in fix #27" / "NOT invoked" /
  "deliberately NOT wired" / "does not require" prose-history or negative
  mentions (`hackathon-mode.mdc:37–38,46`, `delivery-gate`, `feature-expansion`
  REROUTE_F27 notes, `integration` REROUTE_F27 notes, `orchestrate`
  `ecc-recipes` note, `ecc-spec-miner` "does not require
  `codebase-onboarding`", `README.md:28` "was cut"). No live dispatch.
  **Backticked CUT skills in hooks/scripts/manifests/schemas/mcp.json/
  package.json:** 0 hits.
- **Removed agents (`agents/<name>.md`):** 0 hits in the built tree.
  **Dropped commands (`commands/<name>.md`):** 0 hits in the built tree.
- **Manifests:** 14 modules / 84 paths / 55 components re-verified by JSON
  read; no module path names a CUT skill; the only CUT-named component is
  the deliberate `skill:vue-patterns` keep above. `mcp.json` has no
  `codebase-memory-mcp` key (chrome-devtools + playwright only).
- **Staged dirs:** 1 `skills/<name>/` path-form hit (the 36-B1
  `conventional-commit-review` line, patch-covered — see above); 0 CUT-rule
  stems; 1 dead-script precise-path hit (the call-map B6 note in the staged
  call-map copy, same prose as the built copy). The 21 backticked CUT-skill
  hits in staged dirs are the 36-B1 pre-patch lines plus "was cut" /
  "NOT wired" prose already present in the built tree. `new-rules/` and
  `round2-skills/` / `rewritten-skills/` carry no CUT-skill dispatch.
- **Observation, cleared:** `new-skills/codebase-memory/SKILL.md` still
  exists as a staged source and `build.sh:222` copies it into the tree, but
  fix27.py removes it on every build — the built tree has no
  `codebase-memory` skill (67-skill count confirms). Same copy-then-remove
  pattern as the 36-B1 files; no action beyond the 36-B1 recommendation.

### (d) README consistency — CLEAN

Every count the README states about the plugin reads 67 skills / 45 agents /
48 rules / 55 commands (line 13: "67 skills, 45 agents, 48 rules, and 55
commands in total (42 agents as-shipped + 3 staged orchestrate agents; 46
rules as-shipped + 2 new rules — `hackathon-mode`, `ponytail` …)"; lines 36,
38, 40 use 67 skills / 45 agents / 55 commands consistently). The fix #28
provenance note is present exactly once at line 29 with all four tokens
(`CUTRULES_F28` `MANIFEST28_F28` `DEADSCRIPTS_F28` `README48_F28`, one
occurrence each). No inconsistency found. (`_F28` tokens `REACTA11Y`,
`NDMISFIRE`, `ORCHKEEP` live only in the patch log by design — confirmed
absent from the built tree, as verify28 check 7 states; `EVALSESS_F28` is in
`scripts/hooks/evaluate-session.js`.)

### (e) SPEC §7 criterion cross-check — NOT MET as written

Note on numbering: the task brief cites "SPEC §7 (audit/sweep/dry-run/verify
criteria)"; in the SPEC as written that material is **§6 Verification
criteria** (§7 is Non-goals). The sweep's own criterion in §6 reads: "Sweep
#36 (or next number): CLEAN, weaving-coherence CLEAN for the whole tree."

- Weaving coherence, taken alone: **CLEAN** — all 20 `_F27` tokens present,
  design-package routing read in 4+ kept skills, grill-me / /demo / theme /
  D19 / ALWAYSLEAD all intact (see (a)).
- The sweep criterion as written: **NOT MET** — the sweep is NOT CLEAN
  because it carries one open minor (36-B1), reported here and not fixed
  post-hoc, with no re-sweep run. This follows the fix #27 precedent
  recorded in MEMORY.md: a sweep carrying a minor is recorded NOT MET as
  written rather than claimed as a pass that did not happen. The minor does
  not touch the shipped tree, so the criterion's weaving-coherence half is
  met; the overall "CLEAN" half is not, until 36-B1 is fixed in the staged
  sources (or explicitly accepted as patch-dependent by a parent decision)
  and a re-sweep confirms it.

### Other

- `fix28/verify28-run5.log`: 110/110 PASS (read, not re-run by this sweep).
  Build log run 6 ends `build complete`, counts 67/45/48/55/15.
- No file was edited, created, or deleted except this report; scratch files
  under `fix28/sweep36-scratch/` were removed at the end of the sweep.
  `build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing was
  committed, pushed, or messaged.
