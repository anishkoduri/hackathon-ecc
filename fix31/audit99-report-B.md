# Audit #99-B — verifier + leg-5 re-run + regression (fix #31, round 3)

**Verdict: PASS — 0 blocking, 0 minor.**

Auditor B (half B: the verifier, the leg-5 re-run, regression), round 3.
Re-audit of the round-2 fix of finding 98-B1 (call-map regeneration).
Read-only except this report. Method: read `fix31/SPEC.md`,
`fix31/MANIFEST.md`, `fix31/audit98-report-B.md` (§6 cascade),
`fix31/audit98-report-A.md`, `fix31/sweep42-report.md` in full;
independently re-ran verify31 (380/380, exit 0, byte-identical to the
recorded run 3); direct grep/md5/count verification of the built tree
rather than trust; full sidecar JSON diff pre- vs post-regeneration;
per-file `diff` of the fix #30 built tree
(`fix31/scratch-repo/hackathon-ecc`, 67 skills) against the run-3
built tree (`hackathon-ecc`); and a full read of the leg-5 re-run
output against the round-1 record. The real tree was never edited by
this audit. `build.sh` was not run; the generator was not run;
`fix11/fix11-stage.py` was not run; nothing was committed or pushed.

**Headline:** the 98-B1 fix is complete and exactly as specified.
verify31 check 10g now expects 72 and nothing else in the verifier
changed; verify31 re-runs 380/380 on my own run, byte-identical to
run 3; the regenerated sidecar carries exactly the 5 new called
skills with the STRONG invokers and the two new-skill edges audit
#98-B predicted, and nothing else changed in it except two
generator-correct artifacts (see Observations); the leg-5 re-run is
0 BROKEN with the counts this audit's task specified; the round-1
evidence is untouched; and the run-3 built tree regresses clean on
every number in this half. No findings.

## Findings

| # | Severity | Finding |
|---|---|---|
| — | — | None. 0 blocking, 0 minor. |

## §1 verify31.py check 10g — PASS (only change is 10g)

- Check 10g (`fix31/verify31.py:1561–1580` area) now asserts the
  sidecar counts equal `{"skills": 72, "agents": 45, "rules": 48,
  "commands": 55, "hooks": 15, "triggers": 49}` (line 1573) and the
  check name reads "call-map sidecar exists with counts
  72/45/48/55/15/49 and 0 uncalled rules" (line 1576). The
  `uncalled.rules == []` assertion is unchanged.
- **Nothing else changed:** the only occurrences of `67` left in
  `verify31.py` are the three legitimate ones — the docstring
  history "skills 67 -> 72" (:24), the stale-string list containing
  `"67 skills"` (:550, :558 — the check that still asserts zero
  `"67 skills"` tree-wide, intact), and the patch-log check
  `"coverage.skills 67 -> 72"` (:2330, :2332). No other 67→72 edit
  crept in. Independent confirmation: `diff
  fix31/verify31-run2.txt fix31/verify31-run3.txt` shows exactly
  one differing line — the 10g check name, 67→72. The check count
  is still 380 (see §2).

## §2 Independent verify31 re-run — PASS

- `python3 fix31/verify31.py hackathon-ecc` run by me:
  **380/380 checks pass, exit 0**, output byte-identical to
  `fix31/verify31-run3.txt` (`diff` silent). Run 3 is not trusted
  on the coordinator's word; it reproduces exactly.
- `fix31/verify31-run3.txt` md5 `d3ac4f33d8901ea4ad90f3d81b2c97b5`
  differs from run 2 (`ae1a392acdb1014954a64ce8f466865f`) by that
  single 10g line only (§1) — as expected for a one-line verifier
  edit.

## §3 The leg-5 re-run — PASS

Read `fix31/leg5-rerun/leg5-rerun-output.txt` in full:

- **17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN**, exit 0
  (summary line `{'STATIC-OK': 19, 'EXERCISED': 17, 'DORMANT': 5}`,
  `BROKEN: 0`). The only `BROKEN` string in the file is the
  summary line itself (:44); there are no BROKEN finding lines.
- `counts:skills -- map=72 tree=72` and `skills:map-agrees -- map
  skills=72 tree skills=72; diff=[]` — both present, the exact
  lines the 2 round-1 BROKEN lines asserted against.
- **It used the regenerated sidecar:** the runner
  (`fix31/leg5-rerun/dryrun46-leg5-rerun.py`, byte-identical to the
  round-1 runner — `diff` silent, so the copy is faithful) sets
  `MAP_PATH` to `fix28/callmap/call-map-data.json` (:32) and its
  docstring says it exercises the paths in that file. The output
  values (map=72) are only producible from the regenerated sidecar
  (the pre-regen backup says 67). Its DORMANT `uncalled:count`
  line reads "regenerated map expects 17", and
  `second-order:count` "regenerated map expects 7" — both match
  the regenerated sidecar (§4).
- **Round-1 evidence untouched:** `fix31/dryrun46/dryrun46-leg5-output.txt`
  (mtime 2026-11-17 04:22 UTC, before the re-run at 04:52) still
  shows the 2 BROKEN lines (`counts:skills -- map=67 tree=72` and
  `skills:map-agrees -- map skills=67 tree skills=72; diff=
  ['getlayers', 'gsap', 'hairline-adopt', 'hairline-create',
  'react-bits']`) and the `BROKEN: 2` summary — the historical
  record, preserved. md5 `39761f5338cbdbae6622079e0413cef0`.
- The `wire:epic-dormant-in-use` DORMANT line (:34) is still just
  a disregarded runner line, repeating the adjudicated-false epic
  premise ("epic-* + prune commands were DROPPED in fix #27 §1(b)
  — no epic commands exist in the tree … not executed here by
  decision"). It is not a finding and it changed nothing: it is
  DORMANT, not BROKEN, and the premise it repeats is the one
  already adjudicated false in round 2.

## §4 The regenerated sidecar — PASS (exactly the predicted delta)

`fix28/callmap/call-map-data.json` vs the pre-regen backup
(`fix31/call-map-data-pre-regen.json`), compared field by field:

- counts: `{'skills': 72, 'agents': 45, 'rules': 48, 'commands': 55,
  'hooks': 15, 'triggers': 49}` — only skills 67→72.
- Elements: 72 skills; the 5 new keys are exactly `getlayers`,
  `gsap`, `hairline-adopt`, `hairline-create`, `react-bits`; no
  key lost; **no called-status changed** for any pre-existing
  element in any kind.
- All 5 new skills `called: true`, with STRONG invokers from
  `rules/hackathon-mode.mdc`, `skills/design-taste-frontend/
  SKILL.md`, `skills/orchestrate/SKILL.md` (built + staged) and
  INVENTORY from `design-inventory.md` §12 — exactly the
  DESIGNPKG-AUTO edges audit #98-B §6(c) predicted.
- Both new-skill edges present: `hairline-create` lists
  `skills/hairline-adopt/SKILL.md` [strong] (built + staged), and
  `react-bits` lists `skills/gsap/SKILL.md` [strong] (built +
  staged) — audit #98-B §6(d), confirmed in the data.
- Uncalled sets identical pre/post: skills 2 (`context-budget`,
  `vite-patterns`), agents 9, commands 6, rules 0, hooks 0,
  triggers 0 (total 17, matching the leg-5 re-run DORMANT line).
  Second-order orphans identical: agents 3, commands 4 (total 7).
  `weak_only`, `trigger_only`, `flow_invisible_commands`,
  `hooks_extra_files` all identical.
- Pre-existing invoker growth is confined to 5 skills gaining
  invoker files (`git-workflow`, `integration`,
  `motion-foundations`, `motion-patterns`, `ui-ux-pro-max`) and 2
  commands (`plan`, `pr`), all from the new skills' own files or
  the regenerated inventory — plus the two artifacts in
  Observations (1). The regen log (`fix31/regen31-run1.txt`)
  agrees: generator EXPECTED 72, all counts OK, 1,354 corpus
  files scanned, map + data written, exit 0.
- The regenerated map `.md` diff vs the pre-regen copy is 38
  lines: counts table 67→72, "Skills (67)"→"(72)" header, the 5
  new rows, and grown invoker lists on the changed rows — matching
  MANIFEST §3. Staged map (`new-skills/orchestrate/references/
  call-map.md`) is byte-identical to the built map.

## §5 Regression on the run-3 built tree — PASS

- **DESIGNPKG-AUTO:** 3,463 chars in both files, md5
  `6f74770f3e897b3115caecd6177ed90d`, byte-identical between
  `skills/orchestrate/SKILL.md:35` and `rules/hackathon-mode.mdc:44`
  — unchanged from audits #97-B/#98-B.
- **GLOBAL-ROUTING:** 2,285 chars in both files, md5
  `68206505a08f90474dc4931b0e5fb6bb`, byte-identical — the fix #29
  golden md5, unchanged.
- **Pin census** (whole tree excl. `node_modules`, occurrence
  counts): `grok-4.7-extra-high` ×49, `Grok 4.7 Extra High` ×22,
  `cursor-grok-4.6-high-fast` ×70, `grok-4.7-high` ×0,
  `Grok 4.7 High` ×0, bare `grok-4.6-high-fast` ×0 — exactly the
  SPEC census.
- **Counts:** skills 72, agents 45, rules 48, commands 55, hooks
  15 (`hooks/hooks.json`, 15 event keys), trigger keys 49
  (coverage `{'skills': 72, 'withTriggers': 49}`).
- **README:** `72` in all 4 count lines (:13, :37, :39, :41) plus
  the fix #31 provenance note at :29 with all four `_F31` tokens.
- **Zero `"67 skills"` tree-wide** in the built tree (excl.
  `node_modules`) — 0 hits.
- **grill-me untouched:** `diff -rq` of `skills/grill-me/` vs
  the fix #30 tree is silent.
- **GetLayers weight at all 6 sites:** "consulted FIRST" language
  present in DESIGNPKG-AUTO (both files), the palette-first
  paragraph (`design-taste-frontend/SKILL.md:224`), the
  orchestrate inventory paragraph (:70), inventory §12 (intro +
  GetLayers row leads "Consulted FIRST"), and the getlayers skill
  (framing header + dedicated Priority section); `getlayers` is
  first in the DESIGNPKG-AUTO palette list and in the palette-first
  paragraph; the USED/CONSIDERED-AND-REJECTED citation sentence
  appears exactly once in each of the three flow paragraphs
  (orchestrate, hackathon-mode, design-taste-frontend).
- **Build run 3:** `fix31/build-log-run3.txt` ends `fix31: OK` /
  `build complete`, `BUILD EXIT: 0`, STEP 5 counts 72/45/48/55/15.

## §6 Full-tree diff vs the fix #30 built tree — PASS

`diff -rq --exclude=node_modules fix31/scratch-repo/hackathon-ecc
hackathon-ecc` finds exactly:

- **7 differing files:** `README.md` (4 count lines 67→72 +
  provenance note only), `manifests/context-packs/
  skill-triggers@1.json` (coverage 67→72 only),
  `rules/hackathon-mode.mdc` (DESIGNPKG-AUTO :44 only),
  `skills/design-taste-frontend/SKILL.md` (palette-first :224
  only), `skills/orchestrate/SKILL.md` (DESIGNPKG-AUTO :35 +
  inventory paragraph :70 only),
  `skills/orchestrate/references/design-inventory.md` (:34 and
  :146 usage-skill pointers + new §12, lines 167–185 only),
  `skills/orchestrate/references/call-map.md` (the regenerated
  map — the one file added to the diff by this round's fix).
- **5 added skill dirs:** `skills/getlayers/` (1 file),
  `skills/gsap/` (1), `skills/react-bits/` (1),
  `skills/hairline-create/` (14), `skills/hairline-adopt/` (2).
- Nothing else. No routing (#29), debloat (#28), design-package,
  or grill-me text changed; the `commands/` tree is untouched
  (all 7 epic commands ship, `/prune` absent — not re-filed).

## §7 The generator edit and the commit — recorded, not yet in the commit tree

The generator edit (`fix28/callmap/generate_call_map.py:100`,
`EXPECTED` skills 67→72) is outside the built tree, as expected —
`fix28/` is a fix dir. It is recorded for the commit in
`fix31/MANIFEST.md` §3 (call-map regeneration bullet) and §6
(OWED-31-3 SUPERSEDED), in `fix31/regen31-run1.txt`, and in the
workspace files themselves (generator + regenerated sidecar +
regenerated staged map). **But it is not yet in the commit tree:**
`fix31/scratch-repo` (git repo at fix #30 commit `cfb15f9`, the
commit source) still holds EXPECTED 67, sidecar counts 67, and
staged map counts 67 throughout `fix28/` and `new-skills/`.
This is an observation, not a finding — MANIFEST §8 (commit /
bundle) is still blank and no commit has been assembled — but the
commit assembly must sync `fix28/callmap/` (generator +
sidecar) and `new-skills/orchestrate/references/call-map.md`
from the workspace into the scratch-repo, or the committed tree
would be internally inconsistent: verify31 check 10g reads the
sidecar from the repo root's `fix28/callmap/` and would fail
against a committed 67 sidecar while the built map says 72.

## §8 Tested and NOT filed

- **OWED-30-6** (allow-listed verify30 check-9b smuggled name):
  recorded known limitation — not re-filed.
- **Dry-run epic/`/prune` error:** only `/prune` was dropped in
  fix #27; all 7 epic commands ship (empty `commands/` diff, §6)
  — not re-filed.
- **OWED-31-4** (vendored hairline-create "six figures" upstream
  text) and **OWED-31-1/31-2** (live behavior unverified; GetLayers
  MCP unwired): carried as recorded — not re-filed.
- **97-A1 (GetLayers $199):** confirmed fixed in rounds 1–2;
  nothing in this round re-opens it — not re-filed.

## §9 Observations (not findings)

1. **MANIFEST §3's "7 pre-existing skills gained invokers only"
   compresses three change types.** The JSON diff shows 6 skills
   with invoker changes (5 gained invoker files + `orchestrate`,
   whose invokers `gan-style-harness/SKILL.md` and
   `orch-pipeline/SKILL.md` went weak→strong with no new files)
   and a 7th changed skill, `error-handling`, whose `flow` list
   only flipped order (`['build', 'on-request …']` →
   `['on-request …', 'build']`, same two values — a set-ordering
   artifact in the generator output, no semantic change). The
   7th skill is the flow flip, not an invoker gain. The
   `orchestrate` tier upgrade is generator-correct: those two
   files were byte-identical between the fix #30 and fix #31
   trees, but the fix #29 GLOBAL-ROUTING text inside them
   contains `skills/orchestrate/references/dispatch-prompt.md`
   path mentions, which are STRONG under the generator's rules —
   the pre-regen backup was the fix #28-era sidecar, never
   regenerated through #29/#30 (counts were unchanged, so the
   tier drift went unnoticed). The regenerated map is more
   accurate than the backup, not less. No called status changed
   anywhere. Wording nuance in the MANIFEST only; the fix is
   unaffected.
2. **Commit-tree sync outstanding** — see §7. The regeneration
   is complete in the workspace; the scratch-repo still needs the
   `fix28/` + staged-map sync at commit assembly.
3. **The leg-5 re-run was leg 5 only, correctly scoped.** No
   other dry-run leg reads the call map or the sidecar, and the
   regeneration changed no other leg input; the round-2
   no-re-dry-run rationale (sweep #42 §(j)) is unaffected by this
   round's fix, which is itself the leg-5 input.

## §10 SPEC §7 Verification — judgment

- The audit loop is at round 3 (this report + the parallel #99-A);
  sweep #43 is parallel round-3 work. Round 2's single minor
  (98-B1) was fixed post-hoc and **re-audited here** — this report
  is that re-audit, so the fix #27 convention (a minor fixed
  post-hoc without a re-audit ⇒ SPEC Verification NOT MET as
  written) is satisfied on half B's side: the regeneration is
  re-verified in full (§§1–6), the verifier re-run is
  independent, and the leg-5 re-run clears the exact 2 BROKEN
  lines the finding rested on.
- **SPEC §7 Verification is MET as written on this half's scope,
  and MET as a whole if and only if audit #99-A and sweep #43
  land clean.** What would still block it: a finding in either
  sibling round-3 report that is fixed post-hoc without a further
  re-audit/re-sweep, or a finding in either sibling that is not
  fixed at all. Nothing in half B blocks it. (The §7 commit-sync
  note is a commit-assembly step, not a §7 verification criterion;
  it does not block the MET judgment, but the parent should not
  treat the fix as shippable until the sync in §7 is done.)

## §11 Methodology note

- Independent re-run: `python3 fix31/verify31.py hackathon-ecc`
  → **380/380, exit 0**, output byte-identical to
  `fix31/verify31-run3.txt` (`diff` silent).
- Block comparisons used direct extraction from the built files
  with md5 (`DESIGNPKG-AUTO 6f74770f…`, `GLOBAL-ROUTING
  68206505…`), not the verifier's assertions.
- Sidecar comparison used a field-by-field JSON diff of
  `fix28/callmap/call-map-data.json` against
  `fix31/call-map-data-pre-regen.json` (elements, invokers,
  tiers, called status, uncalled, second-order, weak-only,
  flow) — not the generator's summary.
- Tree diff baseline is `fix31/scratch-repo/hackathon-ecc` (the
  fix #30 built tree, 67 skills); the file-list diff shows only
  the 7 files in §6 changed and the 5 new skill dirs added.
- The real tree was never edited by this audit; the only file
  written is this report.
