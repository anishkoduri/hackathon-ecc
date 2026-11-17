# Audit #99-A — map regeneration re-audit (fix #31, round 3, half A)

**Verdict: PASS — 0 blocking, 0 minor.**

Auditor A (half A: the map regeneration itself), round 3.
Re-audit of the fix for round-2 finding 98-B1 (OWED-31-3 premise fails —
the DESIGNPKG-AUTO additions ARE dispatch edges under the call-map
generator's own rules, so the fix28 call map had to be regenerated).
The regeneration was done by the coordinator Nov 17, 2026; this audit
re-derives it independently and does not trust the coordinator's claims.
Read-only on the plugin tree except this report. No file was edited,
no generator run, no build run, no commit, no push. `build.sh` and
`fix11/fix11-stage.py` were not run.

**Headline:** the regeneration is correct in every substantive respect.
The generator edit is exactly the 3 claimed lines (verified by diff
against the fix #28 committed form); the regenerated sidecar adds
exactly the 5 new skills, all `called: true` with the motionsites
precedent's invoker pattern plus the two new-skill edges; no other
element changed called status; the uncalled / second-order-orphan /
weak-only / flow-invisible / trigger-only sets are identical to the
pre-regen backup; the map `.md` diff is exactly 38 lines with the
claimed scope; staged map == built map (md5 `a2e7454e14a0e36feac9fbd031c14e29`);
build run 3 ends exit 0 with counts 72/45/48/55/15; verify31 run 3 is
380/380. One observation (O-1, not a finding): the 7th changed skill
gained no invoker, only a flow-stage reorder — the map is right, only
the MANIFEST §3 shorthand is loose.

## Findings

| # | Severity | Finding |
|---|---|---|
| — | — | None. 0 blocking, 0 minor. |

## §1 Generator rules re-derived — the 5 new skills MUST be called

Read `fix28/callmap/generate_call_map.py` in full (docstring + `tokenise()`
+ `scan()` + `summarize()` + `render_map()` + `main()`).

- **Docstring tiers (lines 22–27):** STRONG is a backticked `` `name` ``,
  `skill:name`, a path `skills/<name>/` or a `/command` slash form (etc.);
  INVENTORY is a listing in `references/design-inventory.md`. "Called"
  for a skill is ≥1 STRONG, INVENTORY, or TRIGGER invoker.
- **`scan()` implements exactly that:** a skill name in a file's
  backticked-token set (or `skills/` path set, `rel_skill`, quoted,
  frontmatter-word, or skill-adjacent sets) is a STRONG invoker unless
  it is the skill's own file; the built inventory file counts as
  INVENTORY instead of STRONG; a staged inventory copy counts as STRONG.
- **Independent check with the generator's own `tokenise()`** (module
  imported read-only; the generator itself was NOT run): all 6 files
  `hackathon-ecc/skills/orchestrate/SKILL.md`,
  `hackathon-ecc/rules/hackathon-mode.mdc`,
  `hackathon-ecc/skills/design-taste-frontend/SKILL.md` (built) and
  `new-skills/orchestrate/SKILL.md`, `new-rules/hackathon-mode.mdc`,
  `new-skills/design-taste-frontend/SKILL.md` (staged) have all 5 new
  skill names in their backticked-token sets. The inventory file
  reaches the same 5 via `skills/<name>/` path + `<name>/SKILL.md`
  forms (STRONG-tier tokens; `getlayers`/`gsap`/`react-bits` are not
  backticked there, `hairline-create`/`hairline-adopt` are).
- **Motionsites precedent — confirmed in the regenerated sidecar:**
  `motionsites-web-builder` is `called: true` with exactly 6 STRONG
  invokers (the same 3 built + 3 staged files above) and flow
  `build; design package; build (orchestrated dispatch)`. Every one
  of the 5 new skills carries that same 6-STRONG pattern **plus** an
  inventory invoker (built `design-inventory.md` [inventory], staged
  copy [strong]) — a superset of the precedent. Under the generator's
  own rules there is no reading on which motionsites is called and
  the 5 new skills are not. 98-B1's premise fix is therefore
  correctly implemented, not merely asserted.

## §2 Sidecar diff vs backup — counts, 5 rows, no status change

Compared `fix28/callmap/call-map-data.json` (regenerated) against
`fix31/call-map-data-pre-regen.json` (backup) with a full recursive
diff (every element, every field, top-level keys included).

- **Counts:** regenerated `{"skills": 72, "agents": 45, "rules": 48,
  "commands": 55, "hooks": 15, "triggers": 49}`; backup identical
  except `"skills": 67`. All other counts unchanged.
- **Backup authenticity:** the backup map's md5 is
  `b066413a1a7dd6efcd8571c8abf93942` — the exact md5 audit #98-B
  recorded for the fix28 map — so the backup is the genuine
  pre-regen file.
- **Added elements:** exactly the 5 new skills (`getlayers`, `gsap`,
  `react-bits`, `hairline-create`, `hairline-adopt`). Zero added or
  removed agents, rules, commands, hooks, or triggers.
- **Called status:** no element changed `called` in either direction
  (true→true or false→false everywhere). The 5 new skills are all
  `called: true`, `weak_only: false`.
- **Sets identical:** uncalled skills `context-budget, vite-patterns`;
  uncalled agents 9; unclaimed rules 0; uncalled commands 6
  (`astra-review, ecc-guide, fastapi-review, issue-review, loop-start,
  pm2`); uncalled hooks 0; uncalled triggers 0; weak-only skills
  `context-budget, vite-patterns`, weak-only agents none;
  second-order orphans agents 3 (`ecc-docs-lookup, ecc-fastapi-reviewer,
  ecc-mle-reviewer`) + commands 4 (`harness-audit, python-review,
  skill-create, skill-health`); trigger-only `[]`;
  flow-invisible commands = the same 6 uncalled commands;
  `hooks_extra_files` identical. All byte-identical to the backup.
- **The 5 new rows (invokers, from the regenerated sidecar):**
  - `getlayers` — STRONG from hackathon-mode, design-taste-frontend,
    orchestrate (built + staged); INVENTORY from built
    design-inventory §12 (+ staged copy STRONG). Flow: build; design
    package; build (orchestrated dispatch).
  - `gsap` — same 6 STRONG + INVENTORY, plus pre-existing STRONG hits
    (`motion-patterns/SKILL.md`, `ui-ux-pro-max/SKILL.md`, icon/index
    JSON fixtures — library mentions predating fix #31, as 98-B
    recorded). Same flow as above.
  - `react-bits` — same 6 STRONG + INVENTORY, plus the new-skill edge
    `skills/gsap/SKILL.md` [strong] (built + staged). Same flow.
  - `hairline-create` — same 6 STRONG + INVENTORY, plus the new-skill
    edge `skills/hairline-adopt/SKILL.md` [strong] (built + staged).
    Same flow.
  - `hairline-adopt` — same 6 STRONG + INVENTORY. Same flow.
  - All five flows match the motionsites flow exactly.
- **Pre-existing elements whose invokers changed (7 skills + 2 commands
  in the map rows; see O-1 for the precise split):**
  - `git-workflow` — gained STRONG from staged
    `new-skills/orchestrate/SKILL.md` only (`:105`, the
    `` `git-workflow` `` skill + `skills/git-workflow/SKILL.md` path;
    the built copy already had it as STRONG in the old map). Called
    unchanged (true).
  - `integration` — gained WEAK only, from `skills/getlayers/SKILL.md`
    (built + staged; bare word "integration" in the getlayers text).
    Called unchanged (true).
  - `motion-foundations` — gained STRONG from `skills/gsap/SKILL.md`
    (built + staged; backticked `` `motion-foundations` `` + the
    `skills/motion-foundations/SKILL.md` path). Called unchanged.
  - `motion-patterns` — gained STRONG from `skills/gsap/SKILL.md` and
    `skills/react-bits/SKILL.md` (built + staged; path references).
    Called unchanged.
  - `orchestrate` — two invokers upgraded WEAK→STRONG:
    `skills/gan-style-harness/SKILL.md` and
    `skills/orch-pipeline/SKILL.md` (fix #29 GLOBAL-ROUTING text now
    names orchestrate in STRONG-tier forms, e.g. "orchestrate SKILL.md").
    No new invoker path; called unchanged. This is a genuine
    current-tree fact the stale fix28 sidecar predates, not a regen
    error.
  - `ui-ux-pro-max` — gained STRONG from `skills/gsap/SKILL.md` and
    `skills/react-bits/SKILL.md` (built + staged; path references).
    Called unchanged.
  - `error-handling` — invokers identical; only its `flow` list order
    flipped (`build; on-request (trigger…)` → `on-request (trigger…);
    build`). Same stage set, no semantic change (see O-1).
  - Commands `plan` and `pr` — gained WEAK only (`plan`: +4 weak from
    getlayers SKILL.md + design-inventory, built + staged; `pr`: +4
    weak from hairline-create `kernel.js` + `examples/terrain.js`,
    built + staged). Called true→true for both; their STRONG invokers
    are untouched.
- **No other field changed anywhere:** the recursive diff found no
  other element-field difference (agent names, hook scripts/downstream,
  trigger phrases, `fm_name_mismatch`, etc. all identical).

## §3 Map `.md` diff vs backup — exactly 38 lines, claimed scope only

`diff fix31/call-map-pre-regen.md new-skills/orchestrate/references/call-map.md | wc -l` → **38**.

The 38 lines are exactly: counts table `| skills | 67 | 67 |` →
`| skills | 72 | 72 |`; `## Skills (67)` → `## Skills (72)`; the 5 new
rows (`getlayers`, `gsap`, `hairline-adopt`, `hairline-create`,
`react-bits`); the grown invoker lists on `git-workflow`,
`motion-foundations`, `motion-patterns`, `orchestrate`,
`ui-ux-pro-max`; and the `error-handling` flow-order row. Nothing else.

- `## Rules (48)` present (line 190), `| rules | 48 | 48 |` present,
  `fix #28` present (2 occurrences), zero `123` in the regenerated map
  (`grep -c 123` → 0). Counts table reads 72/45/48/55/15/49 with
  Expected equal to Count on every row.
- No other section header, count, or row changed.

## §4 The two new-skill edges — confirmed in the source skill files

- **hairline-adopt → hairline-create:** framing header
  `skills/hairline-adopt/SKILL.md:7` — "by invoking the
  `` `hairline-create` `` skill in this plugin"; vendored upstream text
  `:20` — "Invoke `/hairline-create` with the file's path…". Backticked
  name + slash form = STRONG under the generator's rules. Built and
  staged copies identical (both lines present in both).
- **gsap → react-bits:** `skills/gsap/SKILL.md:19` — "For components,
  use `` `react-bits` `` (React/Next)…"; `:91` — "Do NOT reach for it
  for a component (use `` `react-bits` ``…)". Backticked = STRONG.
  Built and staged copies identical.
- Both edges appear in the regenerated sidecar as STRONG invokers
  (built + staged), as listed in §2.

## §5 Staged map == built map; build run 3

- `md5sum new-skills/orchestrate/references/call-map.md
  hackathon-ecc/skills/orchestrate/references/call-map.md` →
  `a2e7454e14a0e36feac9fbd031c14e29` for **both** — the md5 the
  coordinator claimed, confirmed independently.
- `fix31/build-log-run3.txt` (1,335 lines): tail counts block reads
  `skills: 72 / agents: 45 / rules: 48 / commands: 55 / hooks: 15`,
  ends `fix31: OK` / `build complete` / `BUILD EXIT: 0`. (Note: the
  log contains no literal "STEP 5" string; the counts block is the
  STEP 5 output the task refers to.)
- Timestamps are in the right order: regen log + sidecar + staged map
  Nov 17 04:49, build-log-run3 + verify31-run3 Nov 17 04:52.
- `fix31/verify31-run3.txt`: **380/380 checks pass**, including check
  10g — "PASS call map regenerated for fix #28: Rules (48), counts
  table 48, zero '123'" and "PASS call-map sidecar exists with counts
  72/45/48/55/15/49 and 0 uncalled rules".

## §6 Generator edit — exactly the 3 claimed places; fails loudly by design

- Diffed the current `fix28/callmap/generate_call_map.py` against its
  fix #28 committed form (`fix28/scratch-repo` git HEAD `98d72af`,
  `git show HEAD:fix28/callmap/generate_call_map.py`). The diff is
  exactly 3 lines, all `67` → `72`:
  - `:18` docstring — "(72 skills / 45 agents / 48 rules / 55 commands
    / 15 hooks / 49 trigger keys)";
  - `:100` — `EXPECTED = {"skills": 72, "agents": 45, "rules": 48,
    "commands": 55, "hooks": 15, "triggers": 49}`;
  - `:833` — `section("Skills (72)", "skills", …)`.
  No `67` remains anywhere in the file; all other counts (45/48/55/15/49)
  are unchanged in EXPECTED, the docstring, and the section headers
  (`Agents (45)`, `Rules (48)`, `Commands (55)`, `Hooks (15)`,
  `Trigger keys (49)`). Nothing else in the generator changed.
- **Fails loudly on a count mismatch by design (read, not run):**
  `main()` sets `failed = True` on any EXPECTED mismatch, prints
  `COUNT MISMATCH — failing` to stderr, and returns exit 1. The
  generator was NOT run with a wrong EXPECTED, per the task.
- **Regen log** `fix31/regen31-run1.txt`: all six counts OK
  (72/45/48/55/15/49), `corpus files scanned: 1354`, map + data written
  to the claimed paths, uncalled/second-order/weak-only lines matching
  the sidecar. The log carries no explicit exit-code line; "exit 0"
  is the coordinator's claim, corroborated by the all-OK counts and
  the correct outputs it produced (plus the passing build run 3 and
  verify31 run 3 that followed).

## Observations (not findings)

- **O-1 — the 7th changed skill gained no invoker.** MANIFEST §3 says
  "7 pre-existing skills … gained invokers only". Strictly, 6 gained
  invokers and the 7th (`error-handling`) only reordered its flow
  stages (same set, §2). The map is correct either way and the
  substance of the claim — no called-status change, all benign —
  holds for all 7; only the "gained invokers" shorthand is loose for
  `error-handling`. No action required beyond optionally tightening
  that sentence; not filed as a finding.
- **O-2 — inherited generator quirk, unchanged here.** On a count
  mismatch `main()` writes the map + sidecar *before* returning exit
  1, so a failed run still overwrites the outputs and then fails
  loudly. That is the fix #28 committed behavior (the diff in §6
  proves it was not introduced by this fix), and no mismatch occurred
  here. Not in this fix's scope; recorded only so it is not mistaken
  for a regeneration defect.

## Checked and NOT re-filed (per task)

- OWED-30-6; the dry-run epic/`/prune` error (only `/prune` was
  dropped in fix #27; all 7 epic commands ship); OWED-31-4 ("six
  figures" upstream text); OWED-31-1/31-2 (live behavior / MCP
  unwired, carried). None was re-filed.
- 98-B1 itself is the finding this regeneration fixes; this report is
  its re-audit, not a re-filing.

## SPEC §7 verification criteria — status (this half)

- The round-2 minor (98-B1) was fixed post-hoc by the regeneration and
  is **re-audited here** — this report is that re-audit, so the fix #27
  convention is satisfied on half A's side: the regenerated map,
  sidecar, generator edit, staged/built equality, build run 3, and
  verify31 run 3 all re-verify clean.
- Whether SPEC Verification is MET as a whole depends on the parallel
  round-3 work (audit #99-B, sweep #43) landing clean, which is
  outside this half's scope — pending, not failed.

## Methodology note

- Independent sidecar comparison: full recursive JSON diff of the
  regenerated sidecar vs the backup (not the coordinator's summary);
  invoker-level diffs printed per path with old→new kinds.
- Independent rule re-derivation: the generator's own `tokenise()`
  imported read-only and applied to the six DESIGNPKG-AUTO/palette
  files and the inventory file; the generator binary itself was never
  executed.
- Generator diff: against the fix #28 committed file from
  `fix28/scratch-repo` git HEAD `98d72af` (the plugin root itself is
  not a git repository).
- Map diff, md5s, build-log tail, and verify31-run3 tail read directly
  from disk. The only file written is this report.
