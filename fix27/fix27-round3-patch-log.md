# fix27 round-3 patch log (audit #75, build-time half)

Date: Nov 16, 2026. Worker: build-time half only — `fix27/fix27.py`,
`fix27/verify27.py`, `fix25/callmap/generate_call_map.py` (read-only, not
touched). The staged half (vercel-checklist 11 lines, MotionSites
SKILL.md step-2 line) belongs to the staged-edits worker and is NOT
touched here. No push, no full build, no fix11 re-run, no subagents.

## Count moves (final — unchanged this round)

- Skills **67** (unchanged), agents **45** (unchanged), rules **123**
  (unchanged), commands **55** (unchanged).
- Trigger keys **49** (unchanged); coverage.skills **67**.
- Tokens **20** (unchanged). No skill/command adds or cuts in this round.

## Patches added to fix27.py

### §8a B-new-1 — typescript-reviewer coding-standards dispatch (BLOCKING)
- `agents/ecc-typescript-reviewer.md:119`: `For detailed TypeScript
  and JavaScript patterns, use the `typescript-patterns` skill, plus
  `coding-standards` and `frontend-patterns` or `backend-patterns`
  based on the code being reviewed.` → `For detailed TypeScript and
  JavaScript patterns, use the `typescript-patterns` skill, plus
  `frontend-patterns` or `backend-patterns` based on the code being
  reviewed.` (drops `coding-standards`; routes to the kept stack only).

### §8b M-new-1 — accessibility → frontend-a11y re-points (ECC-origin part, 8 lines)
- `skills/react-patterns/SKILL.md:254`: `- Cross-link:
  [skills/accessibility/SKILL.md](../accessibility/SKILL.md) covers
  WCAG criteria and pattern libraries` → `- Cross-link:
  [skills/frontend-a11y/SKILL.md](../frontend-a11y/SKILL.md) covers
  WCAG criteria and pattern libraries`.
- `skills/react-performance/SKILL.md:566`: skills-list entry
  `[accessibility](../accessibility/SKILL.md)` →
  `[frontend-a11y](../frontend-a11y/SKILL.md)`.
- `skills/react-testing/SKILL.md:247`: `Cross-link:
  [skills/accessibility/SKILL.md](../accessibility/SKILL.md) for the
  broader a11y testing playbook.` → `Cross-link:
  [skills/frontend-a11y/SKILL.md](../frontend-a11y/SKILL.md) for the
  broader a11y testing playbook.`
- `skills/react-testing/SKILL.md:359`: skills-list entry
  `[accessibility](../accessibility/SKILL.md)` →
  `[frontend-a11y](../frontend-a11y/SKILL.md)`.
- `agents/ecc-a11y-architect.md:148`: `- See skill `accessibility`
  to transform raw UI requirements …` → `- See skill
  `frontend-a11y` to transform raw UI requirements …` (rest of the
  line unchanged).
- `agents/ecc-react-reviewer.md:161`: skills-list entry
  `` `skills/accessibility/` `` → `` `skills/frontend-a11y/` ``.
- `commands/react-review.md:169`: skills-list entry
  `` `skills/accessibility/` `` → `` `skills/frontend-a11y/` ``.
- `commands/react-test.md:263`: skills-list entry
  `` `skills/accessibility/` `` → `` `skills/frontend-a11y/` ``.
- None of the 8 lines carries a `:N` line-number suffix into the
  removed accessibility SKILL.md, so there was no suffix to drop.
  (The 11 vercel-checklist citations are the staged worker's.)

### §8c M-new-4 — prune manifests/pi-core.json
- JSON patch (load / filter / dump, indent 2): `skills.include`
  93 → **30** (removed the 63 CUT skills, listed in the generated
  patch log under "pi-core.json pruned skills"); `commands.include`
  24 → **18** (removed the 6 dropped commands `cpp-test`,
  `flutter-test`, `go-test`, `gradle-build`, `kotlin-test`,
  `rust-test`, listed under "pi-core.json pruned commands").
- In-script guards: errors unless exactly 63 CUT skills / 6 dropped
  commands are found; errors if `learn-eval.md` / `project-init.md`
  appear in `commands.include`; errors if any remaining entry is
  absent from the built tree as a skill dir / command file.
- The description's claim ("skills.include lists the shipped subset
  only") is true again after the prune: every remaining entry is a
  shipped skill/command. The list is a curated subset of the 67 kept
  skills, not the full set, and it never claimed to list all of them.
- **Correction to audit #75's M-new-4 text:** `learn-eval.md` (:369)
  and `project-init.md` (:382) are NOT "mapped as included
  commands" — they sit in `commands.exclude` with reasons
  ("continuous-learning session extraction" / "ECC install-manifest
  onboarding plan"), which is already the correct disposition. There
  was nothing to remove for them; the prune asserts the include list
  is clean of them.
- Diff check (scratch run): the re-dump differs from the original by
  exactly the removed entries (1 insertion + 70 deletions: 69
  removed entry lines + the `"vite-patterns",` → `"vite-patterns"`
  trailing-comma line, now the last skill entry).

## verify27.py changes
- `ALLOW_LIST`: removed 9 whole-line entries — `agents/ecc-typescript-reviewer.md:119`,
  `skills/react-patterns/SKILL.md:254`,
  `skills/react-performance/SKILL.md:566`,
  `skills/react-testing/SKILL.md:247, :359`,
  `agents/ecc-a11y-architect.md:148`,
  `agents/ecc-react-reviewer.md:161`, `commands/react-review.md:169`,
  `commands/react-test.md:263`. The 11 vercel-checklist entries are
  the staged worker's and were NOT touched.
- Check 10b added (M-new-6): `memory-learning-skill` re-point
  assertion — id `'memory-learning-skill'` kept (×1),
  `path: 'skills/growth-log/SKILL.md'` (×1), `description: 'Growth
  log skill exists'` (×1), `pass: fileExists(rootDir,
  'skills/growth-log/SKILL.md')` (×1), `fix: 'Add
  skills/growth-log/SKILL.md for memory evolution flow.'` (×1), and
  zero `skills/continuous-learning-v2/SKILL.md` in
  `scripts/harness-audit.js` (verified: the file contains no other
  mention of that path). Placed next to the existing
  `security-scan-command` check-10b assertion.
- Check 12b added (see below).
- Check 11: the patch-log tolerance now also accepts the round-3
  scratch form `"32 already absent"` (all 32 commands already absent
  in the scratch tree, since the live tree already has round 2
  applied). Same pattern as the existing `"27 already absent"`
  tolerance; the real build still reports `"commands dropped: 32
  files"`.
- Module docstring updated (round-3 summary, checks 10b/12b).

## M-new-2 — OWED-13 update (in fix27.py, carried into the generated patch log)
- Final count: **94 allow-listed lines = 93 whole-line entries + 1
  name-scoped line** (`rules/hackathon-mode.mdc:46`, covering 2
  names: `product-lens`, `intent-driven-development`). Computed by
  parsing the edited `verify27.py`'s `ALLOW_LIST` / `ALLOW_NAMES`
  literals (93 whole-line entries across 44 files; the name-scoped
  count is 1 line / 2 names — the audit's "103" convention counts
  the :46 line once, and verify27.py's own sweep reports allow-listed
  lines the same way: the faithful scratch run reports "94
  allow-listed"). Before round 3 it was 102 whole-line + 1
  name-scoped = 103; the −9 is the B-new-1 entry plus the 8 M-new-1
  entries removed this round.
- `skills/orchestrate/SKILL.md:136` added to the enumeration
  (prose-history: 'ecc-recipes was cut' REROUTE note, B3).
- The 9 re-pointed/reworded lines (8 M-new-1 + :119) removed from
  the enumeration; a sentence records their round-3 treatment.
- Closing sentence reworded to past tense: the 9 staged-owned live
  dispatches (orchestrate:3, :65, :136, :138, dispatch-prompt:24,
  hackathon-mode:46 brainstorming, :48, :53, :55) LANDED in round 2
  (audit #75 B1/B3/B4/B12/B14); none of the 9 is outstanding.
- Verified in the generated scratch patch log
  (`fix27/scratch/fix27/fix27-patch-log.md`): "OWED-13 CORRECTED
  (round 2, updated round 3)", "94 allow-listed lines", "LANDED in
  round 2".

## M-new-4 — manifest decisions (pruned vs left)
- **PRUNED: `manifests/pi-core.json`** — see §8c above. It is a
  plugin-shipped curated profile whose description claims
  `skills.include` lists the shipped subset only; no code reads it
  (only call-map `[shipped]` evidence rows cite it), but the claim
  is now true again. Pruned counts: 63 CUT skills, 6 dropped
  commands; remaining 30 skills all in KEPT_SKILLS, remaining 18
  commands all in KEPT_COMMANDS (verified in the scratch test, not
  just asserted in fix27.py).
- **LEFT UNPRUNED: `manifests/install-modules.json`** — enumerates
  exactly the 166 pre-cut skill paths (100 CUT + 66 kept; the staged
  `motionsites-web-builder` is absent because it is not upstream),
  i.e. the full upstream ECC install catalog, not the plugin's
  shipped subset. The install machinery derives the live
  single-skill surface from the actual `skills/` directory at load
  time (`addSyntheticSkillComponents`,
  `scripts/lib/install-manifests.js:117-152`) and silently skips
  missing source paths at plan time
  (`materializeScaffoldOperation` returns `[]` for a nonexistent
  source, `scripts/lib/install/plan.js:155-157`), so a stale CUT
  path installs nothing and fails nothing. A paths-only prune would
  leave misleading components (e.g. `skill:coding-standards` →
  `framework-language`, which would no longer contain it) and an
  empty `skill-unified-memory` module that
  `install-profiles.json:85` still references in a profile module
  list (removing the module would make profile resolution throw
  "Unknown install module"). A coherent prune would change installer
  behaviour with no verifier coverage in this fix, and SPEC §1(b)
  never tasked fix27 with it. Stale install-time metadata, same
  class as audit #74 M3/M5 — not a live dispatch.
- **LEFT UNPRUNED: `manifests/install-components.json`** — 5 CUT
  skill components (`skill:unified-memory`,
  `skill:continuous-learning`, `skill:windows-desktop-e2e`,
  `skill:coding-standards`, `skill:vue-patterns`), plus one
  `continuous-learning-v2` mention in the `skill:continuous-learning`
  component's description ("prefer continuous-learning-v2 for new
  installs") — 6 textual mentions total. Same reasoning as
  install-modules.json: upstream-catalog components whose modules
  resolve through the same machinery; removing the components
  without removing their modules (or vice versa) leaves dangling
  references either way.
- The LEAVE decision is recorded in fix27.py §8c as a `CHANGES`
  entry so the generated patch log carries it.

## Check 12b — new check (closes the verifier gap B-new-1 proved)
- Rule (as specified): after the sweep, scan every whole-line
  allow-listed line for an imperative dispatch to a CUT name and
  fail if one is found. Imperative dispatch = the line contains a
  verb (use / check / consult / run / invoke / call / load / read,
  word-boundary, case-insensitive) AND a CUT name that is backticked
  OR followed by "skill" / "agent" / "command" within 120
  characters after the verb — EXCEPT when the verb is negated
  (preceded within 15 characters by "not", "never", "n't", or "do
  not").
- **Deviation found by testing, and why.** The literal rule as first
  implemented false-positived on two legitimate allow-listed lines,
  so it could not pass on the post-fix tree as specified:
  - `rules/hackathon-mode.mdc:38`: "…live modes need an interactive
    browser session that cannot run in an unattended build);
    `loop-design-check` and `api-design` (not UI design —
    `loop-design-check` is a loop/process check…". The verb "run" is
    negated by "cannot", and the verb "check" flagged is the noun
    fragment inside the backticked `` `loop-design-check` `` token
    itself.
  - `skills/feature-expansion/SKILL.md:100`: "…check each against
    `docs/decision-record.md` and the `hackathon-scope` MVP scope
    (fix #27, REROUTE_F27 — `product-lens` was cut)…". The verb
    "check" governs the decision record / scope, and
    `` `product-lens` `` sits in a "(… was cut)" historical note
    100 characters later.
- Three readings are pinned down in the check-12b comment and the
  implementation, and no others:
  - (a) Negation is a SUBSTRING search in the 15 characters before
    the verb (the task states word-boundary only for the verbs, not
    for the negation) — so "cannot run" counts as negated.
  - (b) A verb match inside backticks or inside a hyphenated
    compound is not an imperative verb (the "check" in
    `` `loop-design-check` `` and in "Sanity-check" are noun
    fragments of a longer token).
  - (c) A CUT name annotated as cut in the same breath ("was cut" /
    "were cut" / "NOT invoked" within 20 characters after the name)
    is a historical note, not a dispatch target — a live dispatch
    never phrases its target as already cut.
- The check is named exactly "check 12b: no imperative dispatch to
  a CUT skill/agent/command hides in an allow-listed line". A
  missing allow-listed file/line fails loudly (stale allow entry).

## Check-12b both-ways test results
- (i) PASS on the post-fix tree: the faithful scratch run reports
  "check-12b: 0 imperative dispatch(es) hiding in allow-listed
  lines" / "PASS check 12b …" as part of 78/78 (see below). A
  prototype of the detector run over the CURRENT (pre-fix) live
  tree's allow-list flagged exactly one line — the true B-new-1
  dispatch at `agents/ecc-typescript-reviewer.md:119` — once the
  three readings above were applied.
- (ii) FAILS on the synthetic old line: temp tree
  `fix27/scratch/f27r3-12b-test/` (post-fix tree + the OLD :119
  line restored) with a temp verifier copy
  `fix27/scratch/f27r3-verify27-12b-test.py` (shipped verify27.py +
  the :119 allow entry re-added) reports 77/78, exit 1:
  `check-12b hits (1): agents/ecc-typescript-reviewer.md:119:
  imperative dispatch 'use' -> CUT 'coding-standards' :: For
  detailed TypeScript and JavaScript patterns, use the
  `typescript-patterns` skill, plus `coding-standards` and
  `frontend-patterns` or `backend-patterns` base…`
  — while check 12 on the same tree PASSES ("0 un-allow-listed, 95
  allow-listed"), reproducing the exact gap 12b closes.

## Scratch-test evidence
Method: fresh scratch tree `fix27/scratch/f27r3-test/` (copy of the
live built tree), reverted to pre-fix27 with the new
`fix27/scratch/f27r3-revert.py` (reverts the round-1 + round-2
fix27.py text patches, including re-inserting the text the round-2
patches deleted; trigger keys/notes and README restored to the
pre-fix27 forms; the 100 CUT skill dirs / 27 agents / 32 commands
are NOT restored — fix27.py tolerates already-absent removals, and
verify27.py check 11 tolerates the "32 already absent" form).
- fix27.py on scratch: **exit 0, 99 changes, 0 errors**
  (`fix27/scratch/f27r3-fix27-run.log`; run log at
  `fix27/scratch/fix27/fix27-patch-log.md`). Scratch tree after the
  run: 67 skills / 45 agents / 123 rules / 55 commands; trigger
  keys 49, coverage.skills 67; pi-core.json pruned (skills.include
  30, commands.include 18).
- pi-core prune verified against KEPT_SKILLS / KEPT_COMMANDS (from
  verify27.py): remaining 30 skills ⊆ KEPT_SKILLS, 0 CUT; remaining
  18 commands ⊆ KEPT_COMMANDS, 0 dropped; learn-eval/project-init
  absent from include, present in exclude.
- verify27.py on the faithful scratch tree: **78/78 pass, exit 0**.
  Check 12 reports "0 un-allow-listed, 94 allow-listed, 294 generic
  bare-word noise lines" (94 = the OWED-13 count). New
  memory-learning-skill check-10b assertion PASSES. Check 12b
  PASSES (0 hits).
- **Faithful vs staged-sim:** the faithful run passes FULLY with no
  staged-worker failure at all — there is no failure "solely due to
  the staged worker's fixes not being in the scratch tree", because
  the 11 vercel-checklist allow entries were deliberately left in
  verify27.py (the staged worker's), so check 12 still excuses
  those lines, and the MotionSites step-2 line has no verify27
  check. Stated explicitly as the task asked.
- verify27.py on the staged-simulation tree
  (`fix27/scratch/f27r3-test-staged-sim/`, built with
  `fix27/scratch/f27r3-simulate-staged.py`: vercel-checklist 11
  lines re-pointed `accessibility` → `frontend-a11y` with `:N`
  refs dropped; MotionSites SKILL.md step 2 gains the
  ignore-Upsell line): **78/78 pass, exit 0**. Check 12 reports
  "0 un-allow-listed, 83 allow-listed" (94 − 11 vercel lines that no
  longer contain a CUT name; the unused allow entries are harmless).
  The sim vercel-checklist keeps one bare generic "accessibility"
  (:93, "named skill (accessibility, motion-*, …)"), correctly
  counted as noise, not a dispatch.
- Sanity check — edited verify27.py on the LIVE (not yet fixed)
  tree: **77/78, exit 1**, with exactly one failure: check 12 with
  9 un-allow-listed hits, precisely the 9 lines this round fixes
  (:119 + the 8 M-new-1 lines). Check 12b passes there (0 hits)
  because :119 is not allow-listed on the live tree — 12b guards
  the allow-list, check 12 guards everything else.

## generate_call_map.py
- Read-only; not touched. No change needed: the call map is
  generator output, the pi-core.json prune does not change any
  `[shipped]` evidence row (the file still exists), and no verify27
  check reads the map. Not regenerated in the scratch test.

## Un-done (with reasons)
1. **M-new-3 (prior verifiers / manifest / sweep / dry-run)** — not
   in this worker's scope. verify26.py / verify25.py still crash on
   the reduced tree (audit #75); no `fix27/MANIFEST.md`, Sweep #35,
   or Dry-run #42 exists yet. The OWED-13 record is updated, but
   the retirement record belongs in the manifest when written.
   Coordinator / manifest worker's.
2. **M-new-5 (MotionSites step-2 ignore-upsell line)** — the
   staged worker's edit to the vendored SKILL.md. Only simulated
   here (`f27r3-simulate-staged.py`); the live tree still lacks the
   line. No verify27 check covers it.
3. **M-new-1 vercel-checklist half (11 lines)** — the staged
   worker's. Only simulated here; the live tree still cites
   `accessibility`, and its 11 allow entries were deliberately left
   in verify27.py until that worker lands.
4. **No verify27 assertion on the pi-core.json prune.** The prune
   is verified in the scratch test (KEPT-subset check above), but
   nothing in verify27.py would catch a later rebuild that restores
   the CUT entries — the same verifier-gap shape as M-new-6. A
   check asserting `skills.include` ⊆ KEPT_SKILLS and
   `commands.include` ⊆ KEPT_COMMANDS would close it; not added
   because the round-3 task did not ask for it. Suggested follow-up.
5. **install-modules.json / install-components.json left unpruned**
   — deliberate, see M-new-4 above. If the coordinator wants them
   pruned, it needs a coherent installer-catalog change (modules +
   components + profiles together) with installer test coverage,
   not a paths-only edit.
6. **Check-12b reading (c)** ("was cut" / "NOT invoked" note
   exclusion) is a judgment call documented above: it is what lets
   the check pass on `feature-expansion/SKILL.md:100`. If a future
   audit wants the strict literal rule, :100 and hackathon-mode:38
   would need rewording first — the check as written is the
   minimal-principled version that passes on the post-fix tree while
   still catching the B-new-1 class (proven by the both-ways test).

## Coordinator additions (Nov 16, 2026, after Worker D)
- verify27.py check-12 ALLOW_LIST: removed the 11 vercel-checklist entries (105, 108, 111, 115, 118, 121, 124, 127, 139, 146, 171). Worker D left them "until it lands"; the staged re-point HAS landed, so the lines no longer name a CUT skill and the entries are dead. Literal now 82 whole-line + 1 name-scoped = 83 (matches the staged-sim's 83 and the OWED-13 count below).
- fix27.py OWED-13: count corrected 94 → 83 (82 whole-line + 1 name-scoped), with the removal arithmetic (-1 typescript-reviewer:119, -8 accessibility pointers, -11 vercel-checklist citations); vercel enumeration reworded to past tense (re-pointed, entries removed).
- verify27.py new check (M-new-4 follow-up): pi-core.json prune assertion — skills.include has no CUT skills, commands.include has no dropped commands. Worker D noted the prune had no assertion (same gap class as M-new-6); added so a rebuild reverting the prune fails loudly. Total checks 78 → 79.

## Coordinator addition (Nov 16, 2026 — Audit #76 M-new-7)
- fix27.py OWED-13: noise count "accessibility 132" → 131, and the vercel enumeration now includes :93. The staged worker's round-3 grep found a 12th `accessibility` hit at vercel-checklist.md:93 ("named skill (accessibility, motion-*, …)") and re-pointed it to frontend-a11y; the census had counted it as bare-word noise, so the live count is 131. Record-only change (no tree patch).
