# Audit #76 — Fix #27, round 3 (targeted re-audit after the Audit #75 fixes)

**Date:** Nov 16, 2026
**Auditor:** independent subagent audit (read-only; no plugin file edited, no build run, no call-map generator run, no push, no fix11 re-run, no subagents)
**Scope:** the fix #27 updated repo in `~/workspace/hackathon-plugin/` — built tree `hackathon-ecc/`, staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/`), `fix27/SPEC.md`, `fix27/audit75-report.md`, `fix27/fix27.py`, `fix27/verify27.py`, `fix27/fix27-patch-log.md`, `fix27/fix27-round3-patch-log.md`, `fix27/build-log-run6.txt`, `fix27/verify27-run4.log`, `fix25/callmap/generate_call_map.py` (read, not run).
**Method:** read Audit #75 and the SPEC §7 criteria in full; read the round-3 patch log and fix27.py §8a–§8c in full; re-ran `verify27.py` myself (twice); counted the built tree directly; read every Audit #75 B-new-1 / M-new-1–M-new-6 item in the built tree at its cited lines; ran my own CUT-name sweep over `skills/`, `agents/`, `commands/`, `rules/`; re-ran the check-12b detector myself against the old :119 line and against all 82 allow-listed lines; re-ran the prior verifiers verify26.py / verify25.py; read `scripts/lib/install-manifests.js` and `scripts/lib/install/plan.js` to judge the install-manifest leave-unpruned decision.

## Verdict

**BLOCKING: 0, MINOR: 1**

Round 3 landed everything Audit #75 asked for: the blocking `coding-standards` dispatch is reworded and its allow-list entry is gone, all 19 `accessibility` re-points landed, OWED-13's count/enumeration/closing sentence are corrected, pi-core.json is pruned and now verifier-asserted, the MotionSites ignore-upsell line is in place, the check-10b `memory-learning-skill` assertion exists and passes, check 8's content-based allow is provably narrow, and verify27.py passes 79/79 on my own re-run with counts and call map exact. The single minor finding is a record staleness of one line in the same OWED-13 record M-new-2 just corrected: its generic-noise breakdown still says "accessibility 132" when the count is now 131, because the staged worker also re-pointed a 12th vercel-checklist line (:93) that the census had counted as noise — a correct fix that no record mentions. Nothing ships broken; nothing is hidden by the verifier.

---

## BLOCKING findings

None.

---

## MINOR findings

### M-new-7. OWED-13's generic-noise breakdown is stale by one line, and the 12th vercel re-point is unrecorded

`fix27/fix27.py:1086` / `fix27/fix27-patch-log.md:157` (OWED-13) still say: "Generic bare-word noise (accessibility 132, projects 156, promote 4, brainstorming 3, evolve 1, prune 1 lines)".

My own CUT-name sweep (see Regression) counts the noise lines as **accessibility 131**, projects 156, promote 4, brainstorming 3, evolve 1, prune 1 — total 293 lines, matching verify27.py's own "293 generic bare-word noise lines". The other five numbers are exact; only `accessibility` is off by one.

The cause is a correct fix the record does not mention. The staged worker re-pointed a **12th** vercel-checklist line beyond the 11 M-new-1 listed: `skills/polish-pass/reference/vercel-checklist.md:93`, which in the round-2 tree read "named skill (accessibility, motion-*, `ui-ux-pro-max`, the dealt theme)" and now reads "named skill (frontend-a11y, motion-*, `ui-ux-pro-max`, the dealt theme)" (verified in both the staged `round2-skills/polish-pass/reference/vercel-checklist.md:93` and the built copy — the file is byte-identical staged vs built, md5 `edb22b15076db97f4be0a04ba771fad7`). That line was a bare-word routing reference — "the deliberate path for each flagged item runs through the named skill (…)" — that the census counted as generic noise rather than a strong match (no backticks, no `skill`-adjacent form: "skill (accessibility" defeats both of verify27.py's `skill`-adjacency patterns), so it carried no allow-list entry and needed no removal; the count arithmetic (103 → 83 via −1 −8 −11) is unaffected. I confirmed the loss against the round-2 scratch tree (`fix27/scratch/f27r2-test/`): its noise count was 294 with accessibility 132 — exactly OWED-13's numbers — and the only truly vanished noise line between that tree and the live tree is vercel-checklist:93 (the other diff, `skills/design-taste-frontend/SKILL.md:411` → `:413`, is the same line renumbered by a +2 shift, still noise). Note the round-3 log's staged-sim note ("the sim vercel-checklist keeps one bare generic 'accessibility' (:93)") describes the simulation, not the live staged edit, which went one line further.

This is a record inaccuracy only — the tree is correct and the verifier counts are correct — minor by this audit's definition.

**Must change:** in `fix27/fix27.py` OWED-13 (and the generated patch log), change "accessibility 132" to "accessibility 131" and add one sentence recording that vercel-checklist:93 was also re-pointed to `frontend-a11y` in round 3 (a bare-word routing reference the census counted as noise, not one of the 11 allow-listed citations).

---

## Audit #75 items — verified one by one

### B-new-1. `coding-standards` dispatch in `ecc-typescript-reviewer.md:119` — FIXED, and check 12b discriminates

- Built `agents/ecc-typescript-reviewer.md:119` (read in full): "For detailed TypeScript and JavaScript patterns, use the `typescript-patterns` skill, plus `frontend-patterns` or `backend-patterns` based on the code being reviewed." `coding-standards` is gone; the line routes to the kept stack only (`typescript-patterns`, `frontend-patterns`/`backend-patterns`, all kept — `skills/frontend-a11y` exists, `skills/accessibility` does not).
- The whole-line allow-list entry for `:119` is GONE from `verify27.py`: parsed `ALLOW_LIST`/`ALLOW_NAMES` literals give 82 whole-line entries across 43 files + 1 name-scoped line (`rules/hackathon-mode.mdc:46`, 2 names) = 83 allow-listed lines, and `119 in ALLOW_LIST["agents/ecc-typescript-reviewer.md"]` is False (the file has no allow entry at all).
- Check 12b exists (`fix27/verify27.py:933-1024`, named exactly "check 12b: no imperative dispatch to a CUT skill/agent/command hides in an allow-listed line") and passes on my own re-run (`check-12b: 0 imperative dispatch(es) hiding in allow-listed lines`, part of 79/79, exit 0).
- **Discriminating power tested independently by this auditor.** I extracted `_imperative_dispatch_12b` and its regexes from `verify27.py` (parse-only, no verifier run) into `/tmp/audit76/test12b.py` and ran it against the old line in a scratch file (plugin untouched):
  - OLD :119 line → `('use', 'coding-standards')` — FAILS, as required.
  - NEW :119 line (read from the built tree) → `None` — passes.
  - All 82 allow-listed lines re-scanned with the same function → 0 hits.
- Judgment on the three pinned readings (a) negation-as-substring ("cannot run" counts as negated), (b) verb inside backticks/hyphenated compound is not imperative, (c) a CUT name annotated "was cut"/"NOT invoked" is a historical note: the deviation from the literal rule as first specified is documented in the check-12b comment and in the round-3 log, and the both-ways test above proves the check still catches the B-new-1 class while passing on the fixed tree. The strict-literal alternative (rewording `feature-expansion/SKILL.md:100` and `rules/hackathon-mode.mdc:38` first) remains open but is not a defect in the shipped check — not a finding.

### M-new-1. `accessibility` → `frontend-a11y` re-points (19 lines) — FIXED

All 19 lines read in the built tree:

- **Vercel checklist (11):** `skills/polish-pass/reference/vercel-checklist.md:105, :108, :111, :115, :118, :121, :124, :127, :139, :146, :171` — every line now cites `` `frontend-a11y` `` (e.g. :115 "Covered in part by: `frontend-a11y` skill (\"Div-Buttons\")", :118 "`frontend-a11y` (alt)"). The staged copy is byte-identical: md5 `edb22b15076db97f4be0a04ba771fad7` for both `round2-skills/polish-pass/reference/vercel-checklist.md` and the built copy; the 11 lines are identical staged vs built.
- **ECC-origin (8):** `skills/react-patterns/SKILL.md:254` (cross-link now `[skills/frontend-a11y/SKILL.md](../frontend-a11y/SKILL.md)`), `skills/react-performance/SKILL.md:566` (skills-list entry now `[frontend-a11y](../frontend-a11y/SKILL.md)`), `skills/react-testing/SKILL.md:247` (cross-link to `frontend-a11y`) and `:359` (skills-list entry), `agents/ecc-a11y-architect.md:148` ("See skill `frontend-a11y` to transform raw UI requirements…"), `agents/ecc-react-reviewer.md:161`, `commands/react-review.md:169`, `commands/react-test.md:263` (skills-list entries now `` `skills/frontend-a11y/` ``).
- **Zero `accessibility` skill references remain in those files:** fixed-string grep for `skills/accessibility`, `../accessibility`, `accessibility/SKILL` over `skills/`, `agents/`, `commands/`, `rules/`, `manifests/` returns exactly 2 hits, neither in the 19 files: `rules/react-patterns.mdc:194` ("For accessibility see `skills/accessibility/SKILL.md`" — the known M7 rules pointer, carried to the rules-debloat follow-up, not part of M-new-1) and `manifests/install-modules.json` (the unpruned upstream catalog — see M-new-4). The remaining bare-word "accessibility" hits in the 19 files are ordinary English prose ("accessibility-first composition", "accessibility assertions with axe", "accessibility tree", etc.) — not skill references, correctly not counted.
- **Allow-list entries gone:** the 11 vercel entries and the 8 ECC entries are all absent from `verify27.py`'s `ALLOW_LIST` (each file reports ABSENT for the removed lines; the vercel file has no entries at all). Counted from the literals: 82 whole-line + 1 name-scoped = 83.
- **Call map gained the invokers:** `skills/orchestrate/references/call-map.md:88` (`frontend-a11y` row) now lists as STRONG invokers `agents/ecc-a11y-architect.md`, `agents/ecc-react-reviewer.md`, `commands/react-review.md`, `commands/react-test.md`, `polish-pass/reference/vercel-checklist.md`, `react-patterns/SKILL.md`, `react-performance/SKILL.md`, `react-testing/SKILL.md` (plus the trigger and the staged copies). The kept `frontend-a11y` skill dir exists; the removed `skills/accessibility/` dir does not.

### M-new-2. OWED-13 record — FIXED (count, enumeration, closing sentence)

- `fix27/fix27.py:1086` (OWED-13) and the generated `fix27/fix27-patch-log.md:157` (identical text) now read "82 whole-line allow-list entries + 1 name-scoped line = 83 allow-listed lines, counted from verify27.py's ALLOW_LIST/ALLOW_NAMES literals after the round-3 removals (102 whole-line + 1 name-scoped = 103 before round 3; -1 typescript-reviewer:119, -8 accessibility pointers, -11 vercel-checklist citations)". I counted the literals myself: **82 whole-line + 1 name-scoped = 83** — matches.
- `skills/orchestrate/SKILL.md:136` is enumerated ("prose-history: 'ecc-recipes was cut' REROUTE note, B3").
- The vercel enumeration is reworded to past tense: "skills/polish-pass/reference/vercel-checklist.md:105, :108, :111, :115, :118, :121, :124, :127, :139, :146, :171 (citations re-pointed to frontend-a11y in round 3 by the staged worker; their 11 allow-list entries removed once the re-point landed)". The 11 lines remain enumerated as census history, explicitly marked re-pointed — that is the rewording Audit #75's coordinator note asked for, not a live claim.
- Closing sentence is past tense: "The 9 staged-owned live dispatches listed in the round-2 record — skills/orchestrate/SKILL.md:3 (B4), :65 (B1), :136 (B3), :138 (B1), skills/orchestrate/references/dispatch-prompt.md:24 (B1), rules/hackathon-mode.mdc:46 brainstorming (B12), :48 (B4), :53 (B12), :55 (B12) — LANDED in round 2 (verified in the built tree, audit #75 B1/B3/B4/B12/B14); none of the 9 is outstanding."
- Residual (see M-new-7): the generic-noise breakdown inside OWED-13 ("accessibility 132, …") is stale by one line — the live count is 131 — because the staged worker also re-pointed vercel-checklist:93, which the census had counted as noise. The count, enumeration, and closing sentence M-new-2 asked for are all correct; only the noise breakdown lags.

### M-new-3. Prior verifiers — crashes confirmed; retirement still unrecorded (open manifest item, not a finding)

- Re-run by this auditor: `fix26/verify26.py` crashes — `FileNotFoundError: …/skills/django-verification/SKILL.md` (same as Audits #74/#75); `fix25/verify25.py` crashes — `KeyError: 'skills'` at `second_order_orphans` (`fix25/verify25.py:260`, same as before).
- Nothing now falsely claims the §7 prior-verifier criterion passed. The only record is `fix27/fix27-round3-patch-log.md` Un-done #1 ("verify26.py / verify25.py still crash on the reduced tree (audit #75); no `fix27/MANIFEST.md`, Sweep #35, or Dry-run #42 exists yet … Coordinator / manifest worker's"). `fix27/fix27.py`'s OWED list and `fix27/fix27-patch-log.md` still say nothing about them, and the manifest where the retirement belongs does not exist (see SPEC §7 below). Per the task brief this is recorded as an open manifest item, not a blocking finding.

### M-new-4. Install / Pi manifests — pi-core pruned and asserted; install-modules/components left unpruned, decision recorded and SOUND

- **pi-core.json pruned — confirmed:** `manifests/pi-core.json` `skills.include` 30 entries (was 93), `commands.include` 18 entries (was 24). Counted against verify27.py's KEPT/CUT lists: 0 CUT skills in `skills.include`, 0 dropped commands in `commands.include`; every remaining entry exists in the built tree (all 30 skill dirs and all 18 command files verified present). `learn-eval.md` and `project-init.md` sit in `commands.exclude`, not `include` — Audit #75's ":369/:382 as included commands" reading was wrong, as the round-3 log says; the fix27.py §8c prune asserts the include list is clean of them. The description's claim ("skills.include lists the shipped subset only") is true again: every remaining entry is shipped.
- **New pi-core assertion exists and passes:** `fix27/verify27.py:540-547` asserts `not (_picore_skills & set(CUT_SKILLS)) and not (_picore_cmds & set(DROPPED_COMMANDS))`; it passes on my re-run ("PASS M-new-4 pi-core.json: skills.include has no CUT skills, commands.include has no dropped commands", part of 79/79). This closes the verifier gap the round-3 log's Un-done #4 flagged.
- **install-modules.json / install-components.json left unpruned — confirmed and judged sound:** counted myself — install-modules.json carries exactly 100 CUT skill paths out of 166 skill paths (184 paths total incl. non-skill paths); install-components.json carries the 5 CUT skill components (`skill:unified-memory`, `skill:continuous-learning`, `skill:windows-desktop-e2e`, `skill:coding-standards`, `skill:vue-patterns`) plus 1 `continuous-learning-v2` mention in the `skill:continuous-learning` component description. The reason is recorded in `fix27/fix27.py:1022-1045` (§8c comment, carried into the generated patch log as the "M-new-4 decision" CHANGES entry) and in `fix27/fix27-round3-patch-log.md`.
- **Soundness check (read the machinery myself):** `scripts/lib/install-manifests.js:233-250` is `loadInstallManifests`, which reads all three manifests — but its only callers are `scripts/lib/install-lifecycle.js:1044, :1591` (install-time lifecycle); the other modules that require `install-manifests.js` (`scripts/lib/context-profile-support.js:6`, `scripts/lib/harness-capabilities.js:3`, `scripts/auto-update.js:10`) import only the `SUPPORTED_INSTALL_TARGETS` constant, and no JSON is read at require time. `scripts/lib/install/plan.js:37` reads `install-modules.json` at plan time, and `plan.js:155-157` silently skips a missing source (`if (!fs.existsSync(sourcePath)) return [];`), so a stale CUT path installs nothing and fails nothing. The live single-skill surface is derived from the actual `skills/` directory at load time (`addSyntheticSkillComponents`, `install-manifests.js:117-152`). The round-3 log's further points check out: `skill:coding-standards` maps to the `framework-language` module, which would no longer contain it after a paths-only prune, and `install-profiles.json:85` still lists `skill-unified-memory` in a profile module list (verified — the string occurs once, in a module list), so removing that module would break profile resolution. A coherent prune would change installer behaviour with no verifier coverage in this fix, and SPEC §1(b) never tasked fix27 with it. **Judgment: leaving them unpruned is sound.** Caveat (not a finding): the stale entries are visible in install-time listings — a user installing a profile that references `skill-unified-memory` silently gets a profile without that skill — but that is install-time metadata staleness of the class Audit #74's M3/M5, not a live dispatch, and the decision is now recorded.

### M-new-5. MotionSites step-2 ignore-upsell line — FIXED, vendored skill still clean

- Built `skills/motionsites-web-builder/SKILL.md:26` (step 2, read in the built tree): "Ignore the 'Go Unlimited' upsell block in the fetched index — the free sample only; never use premium/paid MotionSites content and never reproduce the upsell link." It sits directly under the fetch URL at :25. The staged copy carries the same line at :25–26.
- **Vendored skill still has zero promo/UTM content of its own:** grep over the built `skills/motionsites-web-builder/` for `utm_`, `Go Unlimited`, `Sponsored by` returns only the framing header's own disclosure of the removal (`SKILL.md:6`) and the new :26 ignore line — both anti-promo, not promo. One `utm` hit in the whole skill dir (the word "UTM-link rule" inside the :6 disclosure). Zero UTM links, zero "Sponsored by" blocks, zero upsell nudges in the shipped copy.

### M-new-6. verify27.py check-10b `memory-learning-skill` assertion — EXISTS AND PASSES

- `fix27/verify27.py:530-539` asserts the `memory-learning-skill` re-point: `id: 'memory-learning-skill'` ×1, `path: 'skills/growth-log/SKILL.md'` ×1, `description: 'Growth log skill exists'` ×1, `pass: fileExists(rootDir, 'skills/growth-log/SKILL.md')` ×1, `fix: 'Add skills/growth-log/SKILL.md for memory evolution flow.'` ×1, and zero `skills/continuous-learning-v2/SKILL.md` in `scripts/harness-audit.js`. It passes on my own re-run ("PASS B7 harness-audit.js: memory-learning-skill check re-pointed at growth-log (id kept)", part of 79/79, exit 0).

---

## Coordinator follow-ups (not in Audit #75)

### (a) Check 8 rewritten to a content-based allow — CONFIRMED NARROW

- `fix27/verify27.py:390-417`: the banned-term allow is now content-based — any hit containing `raw.githubusercontent.com/Motionsites-AI/claude-skill` is allowed, plus `("skills/motionsites-web-builder/LICENSE", 1)` by file+line. The comment records why: the M-new-5 insert shifted the media line 36 → 38 and broke a line-number allow.
- **Narrowness verified by my own grep** over the same scope check 8 uses (`skills/`, `agents/`, `commands/`, `rules/`, `hooks/`, `README.md`, `--exclude-dir=node_modules`, banned terms `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, case-insensitive): exactly 3 hits in the whole built tree — `SKILL.md:25` (examples fetch URL), `SKILL.md:38` (media fetch URL), `LICENSE:1` (upstream license title). No other "claude" hit exists for the URL-substring allow to exempt, and the URL substring appears in no other line. The allow cannot hide a different banned-term hit because there is none.

### (b) Media-shelf URL line at SKILL.md:38, staged == built — CONFIRMED

- `SKILL.md:38` in BOTH copies reads: "3. **The media shelf:** fetch `media/MEDIA.md` at use time from `https://raw.githubusercontent.com/Motionsites-AI/claude-skill/main/plugins/motionsites-web-builder/skills/motionsites-web-builder/media/MEDIA.md`, plus the numbered contact sheets `media/sheet-*.jpg` (same base URL; fetch to view, do not vendor)…". md5 of the whole file is identical staged vs built: `4220fb98d58fcb2c9a5d284e23754c08` for both `new-skills/motionsites-web-builder/SKILL.md` and `hackathon-ecc/skills/motionsites-web-builder/SKILL.md`. The M-new-5 insert shifted the line from 36 to 38 as expected.

---

## Regression

- **verify27.py re-run by this auditor (twice): 79/79, exit 0** — matches `fix27/verify27-run4.log` exactly, including the sweep line ("0 un-allow-listed, 83 allow-listed, 293 generic bare-word noise lines") and check 12b ("0 imperative dispatch(es) hiding in allow-listed lines"). The check-10b `memory-learning-skill` and M-new-4 pi-core assertions both pass in my runs.
- **Counts counted directly from the built tree:** 67 skills / 45 agents / 123 rules / 55 commands; `hooks/hooks.json` has 15 event keys; trigger keys 49 (`coverage.skills` 67). Build run 6 (`fix27/build-log-run6.txt`) records "fix27: OK", then 67/45/123/55, hooks 15, "build complete".
- **Call map is the regenerated one:** counts table `skills/orchestrate/references/call-map.md:8-14` reads 67/45/123/55/15/49 (all "Expected" matching); the `frontend-a11y` row (:88) carries the new STRONG invokers (see M-new-1); no rows for the 5 cut commands (grep for `learn-eval`, `project-init` returns 0; grep for `/projects`, `promote`, `prune` returns 0); B6 DOCUMENTATION-ONLY note intact (:38); staged md5 == built md5 **`d82aec31bd98831533afd850f2861927`** (both `new-skills/orchestrate/references/call-map.md` and the built copy). The `motionsites-web-builder` row (:104) is present with its STRONG invokers.
- **No NEW live dispatch to a CUT skill/agent/command introduced by round 3:** my own CUT-name sweep over `skills/`, `agents/`, `commands/`, `rules/` (376 matching lines; strong-form classifier written by this auditor, run over grep hits): **0 un-allow-listed hits, 83 allow-listed flagged lines, 293 generic bare-word noise lines** — exactly matching verify27.py check 12's own report (0 / 83 / 293). Cross-check on the round-2 scratch tree (`fix27/scratch/f27r2-test/`): the same sweep finds **28 un-allow-listed hits** — precisely the 9 round-3 lines (:119 + 8 M-new-1) + the 8 staged-owned dispatches (orchestrate:3, :65, :138, dispatch-prompt:24, hackathon-mode:46, :48, :53, :55) + the 11 vercel citations — proving the sweep discriminates rather than rubber-stamping. I also scanned all 293 noise lines for the words skill/agent/command: 9 lines match, all ordinary prose (frontmatter descriptions, "accessibility enforcement", "accessibility test scaffolding", "run the typecheck command") — no hidden routing reference remains in the noise (the one that was there, vercel-checklist:93, was re-pointed; see M-new-7).

---

## SPEC §7 criteria — judged

| Criterion | Verdict | Evidence |
|---|---|---|
| Audit #76 (or next number): ZERO blocking, ZERO minor | **NOT MET** | This audit (#76): BLOCKING 0, MINOR 1 (M-new-7). |
| Sweep #35 (or next number): CLEAN, weaving-coherence CLEAN | **NOT MET** | No sweep file exists in `fix27/` (no `MANIFEST.md`, sweep, or dry-run files at all as of this audit). |
| Dry-run #42 (or next number): PASS | **NOT MET** | No dry-run file exists in `fix27/`. |
| verify27.py: checks for every placement, exit 0 | **MET** | 79/79, exit 0, re-run twice by this auditor (matches `verify27-run4.log`). New in round 3: check 12b (discriminating power proven above), check-10b `memory-learning-skill` assertion, pi-core prune assertion. |
| Prior verifiers: fails only the codified tails | **NOT MET** | verify26/verify25 crash (see M-new-3); retirement unrecorded — open manifest item. |
| Banned terms: 0 in the built tree | **MET with the allow-listed exception** | 0 except the 3 MotionSites lines (SKILL.md:25, :38; LICENSE:1), each genuinely un-rewordable (see coordinator follow-up (a)). |
| Grok pins only | **MET** | `grok-4.7-high` ×56, `cursor-grok-4.6-high-fast` ×74, bare `grok-4.6-high-fast` ×0 (verify27 check 9, re-run). |
| Counts: 67 / 45 / 123 / 55, hooks 15, triggers 49 | **MET** | Counted directly (see Regression). |
| Anchor tokens: 20 `_F27` tokens | **MET** | All 20 present (verify27 check 7, re-run). |
| Manifest: fix27/MANIFEST.md | **NOT MET** | Does not exist yet. |

The manifest, sweep #35, and dry-run #42 do not exist yet — open items, not blocking findings on the tree itself (the tree is what this audit judges; the missing verification artifacts are recorded here and in Open items).

---

## Checks passed (verified clean, with evidence)

1. **verify27.py re-run by this auditor (twice): 79/79, exit 0** (same as `fix27/verify27-run4.log`).
2. **Counts + exact dir sets:** 67/45/123/55, hooks 15, triggers 49; skill dir set exactly the 67 KEPT skills; all 100 CUT skill dirs, 27 removed agents, 32 dropped commands absent (verify27 checks 1–4 + direct listing).
3. **All 20 `_F27` tokens present**, including MOTIONSITES_F27 and PALETTE-FIRST_F27 in their three files each.
4. **B-new-1 fixed** (line reworded, allow entry removed, check 12b added and proven discriminating by this auditor's own both-ways test).
5. **M-new-1 fixed** (all 19 re-points read in the built tree; zero skill references to `accessibility` remain in those files; allow entries gone; call-map row gained the invokers).
6. **M-new-2 fixed** (OWED-13 count 82+1=83 counted from the literals, orchestrate:136 enumerated, vercel enumeration reworded to past tense, closing sentence past tense).
7. **M-new-4 fixed** (pi-core pruned 93→30 / 24→18, 0 CUT/dropped remaining, learn-eval/project-init in exclude, new verifier assertion passes; install-modules/components leave-unpruned decision recorded and judged sound against the install machinery).
8. **M-new-5 fixed** (ignore-upsell line at SKILL.md:26 in the built tree; vendored skill still promo/UTM-free).
9. **M-new-6 fixed** (check-10b `memory-learning-skill` assertion exists and passes).
10. **Coordinator follow-ups verified** (check 8 content-based allow is narrow — exactly 3 banned-term hits in the whole tree, all allowed; media-shelf line at SKILL.md:38, staged md5 == built md5 `4220fb98d58fcb2c9a5d284e23754c08`).
11. **Call map regenerated** (counts table, no cut-command rows, frontend-a11y + motionsites rows with STRONG invokers, B6 note intact, staged md5 == built md5 `d82aec31bd98831533afd850f2861927`).
12. **Banned terms 0** except the 3 allow-listed MotionSites lines; **Grok pins only** (56/74, bare 0).
13. **My own CUT-name sweep: 0 un-allow-listed, 83 allow-listed, 293 noise** — identical to check 12's own numbers; the same sweep finds 28 hits on the round-2 tree, so it discriminates. The 9 noise lines containing skill/agent/command words are all prose.
14. **Checked and NOT a finding:** the check-12b readings (a)–(c) deviation from the literal rule (documented, both-ways-proven); the install-manifests silent-skip caveat (install-time listing staleness, recorded decision); the OWED-13 vercel enumeration remaining as past-tense census history; `rules/react-patterns.mdc:194` `accessibility` pointer (M7, carried to the rules-debloat follow-up).

## Open items carried forward

- **Manifest / sweep / dry-run still to run:** `fix27/MANIFEST.md` does not exist; Sweep #35 (CLEAN, weaving-coherence CLEAN) and Dry-run #42 (PASS) have not run. SPEC §7 requires all three. The prior-verifier retirements (M-new-3) and the OWED-13 record should be folded into the manifest when written.
- **Rules (123) NOT cut** — per SPEC §1(d), the per-language rule families for cut languages remain a follow-up debloat candidate; their dangling skill pointers are M7 (record verified accurate in OWED-11).
- **Prior verifiers** — verify26.py / verify25.py are obsolete against the reduced tree (M-new-3); decide whether to update them or record them as retired in the manifest.
- **Install / Pi manifests** — pi-core.json is pruned; install-modules.json / install-components.json are deliberately left unpruned as upstream-catalog artifacts (M-new-4 decision recorded in fix27.py §8c; a coherent prune would need a modules + components + profiles change with installer test coverage).
- **Netlify row touch-up** (due after Dec 4, 2026) — unchanged, still open from fix #26.

## Verdict

**NOT PASS — BLOCKING: 0, MINOR: 1.** Round 3 fixed everything Audit #75 blocked on, including the blocking dispatch, and added a check 12b whose discriminating power this auditor proved independently. The one minor finding (M-new-7) is a one-line staleness in the OWED-13 noise breakdown plus an unrecorded 12th vercel re-point — both in the record, neither in the shipped tree. Fix the record, and this fix is clean pending the still-missing manifest, sweep #35, and dry-run #42.
