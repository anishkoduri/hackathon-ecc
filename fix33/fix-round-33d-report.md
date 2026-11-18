# Fix #33 — Round 33d report (audit #111-A / #111-B findings)

Date: Nov 17, 2026. Fix worker, round 33d. Audit #111-B returned NOT PASS
(6 BLOCKING findings B-B1..B-B6 + 3 minor); audit #111-A had 2 minor
(A-M1, A-M2 — same as sweep #54's S-M1). This round fixes ALL of them.
No commit. Report copied to `scratch-repo/fix33/` md5-identical.

## 0. What was wrong

Round 33c's choke-point claim — "each skill's step 1 runs the engine, so
orch-pipeline Step 0 covers all five orch-* commands" — was false for 2 of
the 5 orch-* commands, and 4 more entry points were never in the 33c
inventory at all. Dry-run #51 PASSED while missing these bypasses: its
leg-5 "routing nuance" note recorded the orch-build-mvp soft link (step 1
"Phases 0–2 ONLY, not the full engine") but passed it anyway because the
command-file L7 ask and the downstream /gan-build re-check covered it in
practice. The re-audit enumerated entry points independently and found the
bypasses. This round weaves the guardrail at each bypass itself — same
MODELSEL_F33 mechanism, no redesign of the command/skill system.

The guardrail (unchanged): on Auto/undetermined, the orchestrator tells
the user to pick a specific model BEFORE ANY work (grill-me included,
D33-21), never silently orchestrates on an unknown fallback. Standard
wording, as in gan-build L5 / orch-pipeline L43:
"**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the
model the orchestrator is running on and record it in the run ledger
(`MODEL: <name>` — the actual selected model). If the selected model is
Auto, or the model cannot be determined to be a specific model, tell the
user to pick a specific model before proceeding; do not silently
orchestrate on an unknown fallback."

## 1. Findings fixed

### B-B1 — `/orch-change-feature` removal branch (D33-25)
- Finding: command L27 routes removals to the skill's `Removing a feature`
  section "instead of the change steps below"; that section (skill L45) is
  6 self-contained steps with zero MODEL occurrences and never invokes the
  engine. Deletion + commit + redeploy proceeded on Auto. Also reachable
  via the `skill:orch-change-feature` "remove a feature" trigger.
- Fix: full MODEL check woven at the top of the `## Removing a feature`
  section itself, as its first content, before step 1 (delete).
  - `scratch-repo/hackathon-ecc/skills/orch-change-feature/SKILL.md:45`
    (`## Removing a feature`), `:47` (MODEL check) — fix33.py built-tree
    replacement (orch-* skills are built-tree-only).
  - Command file unchanged (its L7 guardrail reference + L27 routing
    already point at the section; the section now carries the operative
    check — a pointer without a routing edge is not coverage, and this
    section had no edge to the engine).

### B-B2 — `/orch-build-mvp` step 1 never runs Step 0 (D33-26)
- Finding: skill L36 said "Run orch-pipeline Phases 0–2 ONLY… This step
  does NOT run the full orch-pipeline engine." Step 0 is the classifier
  section, not a phase; no step ran it. First check fired only at step 4's
  `/gan-build` drive, after scoping/slicing/Gate 1/expansion.
- Fix (mechanism chosen of the two the audit allowed): step 1 runs
  orch-pipeline Step 0 FIRST, then Phases 0–2 — step 1 names Step 0
  explicitly AND restates the MODEL ask at step 1's entry, so the check
  fires before scoping/slicing/Gate 1/expansion even if Step 0 is read as
  classifier-only. Routing edge + operative ask both present.
  - `scratch-repo/hackathon-ecc/skills/orch-build-mvp/SKILL.md:36`
    (step 1, one long line) — fix33.py built-tree replacement.
  - `scratch-repo/hackathon-ecc/commands/orch-build-mvp.md:29` — step-1
    sentence corrected the same way ("step 1 = orch-pipeline Step 0
    (MODEL check + Classify) first, then Phases 0–2 only").
  - The 33c report §1.3 sentence ("each skill's step 1 runs the engine")
    and SPEC D33-22's repeat of it are corrected, not deleted (correction
    banner in `fix-round-33c-report.md` §1.3; D33-22 carries a
    "[Corrected in round 33d…]" note).

### B-B3 — `/feature-dev` (D33-27)
- Finding: standalone feature flow (code-explorer → code-architect →
  implement TDD → code-reviewer), no guardrail; outside the round-33c
  9-file inventory.
- Fix: full MODEL check at the command entry, before any dispatch.
  - `scratch-repo/hackathon-ecc/commands/feature-dev.md:5` (MODEL check,
    right after the frontmatter); first work step is the code-explorer
    dispatch at `:19` — check precedes it. fix33.py built-tree replacement.

### B-B4 — `/react-build` (D33-28)
- Finding: factory-drone fix loop, no guardrail.
- Fix: full MODEL check at the command entry, before any dispatch.
  - `scratch-repo/hackathon-ecc/commands/react-build.md:5` (MODEL check,
    right after the frontmatter); factory routing / drone dispatch at
    `:11` — check precedes it. fix33.py built-tree replacement. Drone
    pins and dispatch mechanisms untouched — only the guardrail ask added.

### B-B5 — trigger-routed `grill-me` (D33-29)
- Finding: "grill me" etc. load the skill directly; zero MODELSEL_F33 —
  the D-1 shape survived on this path. Harm bounded (Q&A only; the check
  still fired before any build work), but the trigger path must still ask
  before proceeding.
- Fix: full MODEL check at the grill-me skill's entry.
  - Staged `scratch-repo/new-skills/grill-me/SKILL.md:8` (first content
    under `# Grill Me` at `:6`); built
    `scratch-repo/hackathon-ecc/skills/grill-me/SKILL.md:8`, before
    `## Workflow` at `:24`. Staged source flows verbatim into the built
    tree; no fix33.py tuple needed or added.

### B-B6 — trigger-routed `feature-expansion` (D33-30)
- Finding: "make it much better" dispatches 4 brainstorm subagents, no
  guardrail.
- Fix: full MODEL check at the skill's entry, before Phase 0 grounding
  and the Phase 1 dispatch.
  - Staged `scratch-repo/new-skills/feature-expansion/SKILL.md:6` (first
    content of the file body, after the frontmatter); built
    `scratch-repo/hackathon-ecc/skills/feature-expansion/SKILL.md:6`,
    before the decision-record read (`:8`), Phase 0 (`:45`), and the
    Phase 1 four-subagent dispatch (`:55`/`57`). Staged source flows
    verbatim; no fix33.py tuple. Not a user approval gate for features
    (the "no user approval gate" rule is about the feature list, not the
    model ask) — no conflict.

### B-M2 — latent re-pin path (D33-31)
- Finding: build.sh fix13-A still wrote the `grok-4.7-high` design-role
  pin into the orch-* skills; fix33.py scrubbed it after. If fix33.py
  were skipped, the pin would return.
- Fix: build.sh fix13-A (+ fix13e block) now writes model-agnostic
  wording instead of the pin; the five fix33.py scrub tuples are removed;
  pre-state census ID 25 → 20 (PROSE x7, fast x71 unchanged).
  - `scratch-repo/build.sh:22197` (fix13-A header comment, updated),
    `:22208` (orch-build-mvp: "The design role runs on the model selected
    in this chat (the design-lead tier inherits the chat model — see the
    picker note in orchestrate SKILL.md step 4)."), `:22219`
    (orch-change-feature), `:22696` (orch-add-feature), `:22701`
    (orch-fix-defect), `:22707` (orch-refine-code — the last four read
    "The design role runs on the model selected in this chat.").
  - Verified in code: no other build.sh patch writes the pin into any
    skill. Remaining build.sh `grok-4.7-high` lines (39, was 44) target
    only rules/common-performance.mdc (old-side anchors),
    commands/astra-review.md, agents/ecc-gan-planner.md,
    commands/gan-build.md, commands/gan-design.md, README.md, or
    comments. "The design role runs on model `grok-4.7-high`" occurrences
    in build.sh: 0.
  - Required consequence (same class as D33-15/D33-18): fix24.py's G-4
    `sub()` anchored on the fix13-A parenthetical "(slug form only —
    never bracket syntax; select Grok 4.7 High…)" which no longer exists
    — that one sub removed with an explanatory comment
    (`scratch-repo/fix24/fix24.py`, hunk `@@ -266,9 +266,14 @@`); the
    other two G-4 subs untouched. Canonical + scratch copies md5-identical
    (`2aa3de92d46263f58aa268a1b4f79c87`). Old parenthetical now 0
    occurrences in fix24.py and build.sh (survives only in historical
    fix13-assemble.py and in fix24.py:581, a different sub — the README
    F-1/F-2 old-side anchor, which must stay). The fix13/fix13e-assemble.py
    copies still carry the old text — historical assemble scripts never
    invoked by build.sh, left as history.
  - Verified after rebuild: built orch-* skills contain zero
    `grok-4.7-high` (skills + commands). The built design-role text is
    byte-identical to the old scrubbed text, so §16b passes unchanged.

### A-M1 — stale guardrail-home line numbers (D33-32)
- Correct home measured in the current built orchestrate skill: pre-grill
  block L52 / step-0 back-reference L64 / picker note L95. Fixed in SPEC
  D33-5 + §3(c) Guards, MANIFEST summary + section header ("D33-1…D33-35"),
  implementation-report D33-5, fix33.py DECISION-33-19 string, verify33.py
  §16c check name ("L93 picker note" → "L95"). "Step-0 procedure" →
  "pre-grill block". Historical pre-33c mentions correctly framed as
  history were NOT findings — left alone.

### A-M2 + S-M1 + B-M1 — "Phase 0" vs "Step 0" (D33-33)
- The orch-pipeline MODEL check sits at Step 0 (the classifier section),
  NOT Phase 0 (Intake). Fixed in SPEC D33-22 + §6 OWED-33-4, fix33.py
  DECISION-33-22 + OWED-33-4 strings, verify33.py §16m header comment +
  check names. Reworded "Step 0 is the first thing the engine does, before
  the size classifier" → the MODEL check is the first content of Step 0,
  before the classifier's scoring text (Step 0 IS the classifier). The
  patch log corrected itself on the rebuild. The 3 remaining "Phase 0"
  mentions in the regenerated patch log are all legitimate ("before Phase
  0 Intake", "Phase 0 grounding", "NOT Phase 0 (Intake)").

### B-M3 — review-only dispatches (D33-34, NOT fixed)
- `/review-pr`, `/plan` second pass, `skill:council` carry no guardrail
  and get none — review/deliberation only, no code written, no commit, no
  deploy, no dispatch of build work. Outside claimed scope. Recorded as
  OWED-33-5 (observation) in SPEC §6 + MANIFEST + fix33.py.

### OWED-33-4 — re-opened, then fixed again
- Was marked SUPERSEDED/FIXED by round 33c — that status is now WRONG.
  Re-opened (RE-OPENED by audit #111-B, listing B-B1..B-B6) in SPEC §6 +
  MANIFEST + fix33.py OWED string, history kept not deleted, and marked
  fixed again in round 33d (D33-25/D33-26 + §16n + the §3 trace below).

## 2. New decisions (D33-25…D33-35)

| # | Decision |
| --- | --- |
| D33-25 | B-B1: full MODEL check at the top of the orch-change-feature `Removing a feature` section (fix33.py built-tree replacement). |
| D33-26 | B-B2: orch-build-mvp step 1 runs orch-pipeline Step 0 first, then Phases 0–2; step 1 names Step 0 explicitly AND restates the MODEL ask. Command step-1 sentence corrected the same way. |
| D33-27 | B-B3: full MODEL check at the entry of `commands/feature-dev.md` (fix33.py built-tree replacement). |
| D33-28 | B-B4: full MODEL check at the entry of `commands/react-build.md` (fix33.py built-tree replacement); drone pins/dispatch untouched. |
| D33-29 | B-B5: full MODEL check at the entry of the grill-me skill (staged source, flows verbatim). |
| D33-30 | B-B6: full MODEL check at the entry of the feature-expansion skill (staged source, flows verbatim). |
| D33-31 | B-M2: build.sh fix13-A/fix13e write model-agnostic design-role wording; 5 fix33.py scrub tuples removed; census ID 25 → 20; fix24.py G-4 sub removed. |
| D33-32 | A-M1: guardrail-home line numbers L52/L64/L95; "step-0 procedure" → "pre-grill block". |
| D33-33 | A-M2/S-M1/B-M1: "Phase 0" → "Step 0"; Step 0 IS the classifier. |
| D33-34 | B-M3: review-only dispatches → OWED-33-5, not fixed. |
| D33-35 | Verifier §16n (21 checks, routing-aware); count 565 → 586. Verifier-limit honesty in SPEC. |

fix33.py: REPLACEMENTS stays 35 tuples (5 scrub tuples out, 5 new
guardrail tuples in), so the patch-log "Changes (41)" stays 41. EXPECT
OLD_ID 25 → 20. fix33.py canonical + scratch copies md5-identical
(`cda0e5be0c9ed0030f73fddf07c527c0`).

## 3. Per-bypass trace (manual, built run-10 tree — not the verifier alone)

All paths traced by reading the built files; line numbers are the run-10
built tree. Trigger file: `hackathon-ecc/manifests/context-packs/skill-triggers@1.json`.

- **B-B1:** `/orch-change-feature` → `commands/orch-change-feature.md:27`
  (removal branch routes to the skill's `Removing a feature` section)
  → `skills/orch-change-feature/SKILL.md:45` (`## Removing a feature`)
  → `:47` full MODEL check, first content of the section, before step 1
  (delete). Trigger path: `skill-triggers@1.json:229`
  `skill:orch-change-feature` ("remove a feature", "remove this feature")
  → loads the skill directly → same section, same check. The section never
  invokes the engine; the command's L7 pointer alone could not cover it.
- **B-B2:** `/orch-build-mvp` → `commands/orch-build-mvp.md:29` (step 1 =
  orch-pipeline Step 0 first, then Phases 0–2) → `skills/orch-build-mvp/SKILL.md:36`
  (step 1 runs Step 0 first, MODEL ask restated inline, before scoping /
  slicing / Gate 1 / expansion) → `skills/orch-pipeline/SKILL.md:41`
  (`## Step 0 — Classify size`) → `:43` full MODEL check, first content
  of Step 0. The downstream /gan-build drive at step 4 still re-checks
  after the model is picked and passes silently — no second ask.
- **B-B3:** `/feature-dev` → `commands/feature-dev.md:5` full MODEL check
  at entry → `:19` first work step (code-explorer dispatch). Check
  precedes all dispatch.
- **B-B4:** `/react-build` → `commands/react-build.md:5` full MODEL check
  at entry → `:11` factory routing / drone dispatch. Check precedes all
  dispatch. Drone pins and dispatch untouched.
- **B-B5:** "grill me" → `skill-triggers@1.json:160` `skill:grill-me`
  ("grill me", "ask me questions about my idea", …) → loads
  `skills/grill-me/SKILL.md` → `:8` full MODEL check (under `# Grill Me`,
  `:6`) → `:24` `## Workflow`. Check precedes the workflow.
- **B-B6:** "make it much better" → `skill-triggers@1.json:121`
  `skill:feature-expansion` ("make it much better", "expand this", …) →
  loads `skills/feature-expansion/SKILL.md` → `:6` full MODEL check →
  `:8` decision-record read → `:45` Phase 0 grounding → `:55`/`57`
  Phase 1 four-subagent dispatch. Check precedes all of it.

## 4. Rebuild + verification (run 10)

Build invocation (exact, per MANIFEST; fake HOME on real disk, NOT /tmp;
re-sync WITHOUT `--delete` — run 8's accident):

```
rsync -a --exclude=.git --exclude=hackathon-ecc --exclude='fix*/dryrun*' \
  --exclude='*/demo-sample-video' --exclude='*.webm' --exclude=.npm-cache \
  --exclude=.tmp --exclude=__pycache__ --exclude='fix32/scratch-repo' \
  ~/workspace/hackathon-plugin/fix33/scratch-repo/ \
  ~/workspace/hackathon-plugin/fix33/fakehome33/workspace/hackathon-plugin/
cd ~/workspace/hackathon-plugin/fix33/fakehome33/workspace/hackathon-plugin
HOME=~/workspace/hackathon-plugin/fix33/fakehome33 \
MS_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/hack-skills \
UIPRO_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/uipro \
SKILL_SRC=~/workspace/hackathon-plugin/fix26/scratch-clones/skill-add \
TMPDIR=~/workspace/hackathon-plugin/fix33/.tmp \
NPM_CONFIG_CACHE=~/workspace/hackathon-plugin/fix33/.npm-cache \
bash build.sh > ~/workspace/hackathon-plugin/fix33/build-log-run10.txt 2>&1
echo "BUILD EXIT: $?" >> ~/workspace/hackathon-plugin/fix33/build-log-run10.txt
```

- **Run 10 — BUILD EXIT: 0** (1,366-line log). fix24 OK (113 changes —
  one fewer than run 9's 114: the removed G-4 sub), fix33 OK (41
  changes), fix31 OK, fix32 OK. No errors / tracebacks. Sync-back: built
  tree (`hackathon-ecc/`, rsync `--delete`) + `fix33/fix33-patch-log.md`
  only; historical logs NOT synced back.
- **Pre-build verifier: 568/586, exit 1** (`fix33/verify33-run33d-prebuild.txt`,
  expected). The 18 FAILs were exactly the new §16n checks (16: B-B1 ×2,
  B-B2 ×5, B-B3 ×2, B-B4 ×2, B-B5 ×2, B-B6 ×2) + the §13 x20 census +
  the §16n patch-log assertions (D33-25..35, OWED-33-5/OWED-33-4
  RE-OPENED) — all against the un-rebuilt run-9 tree. The B-M2 checks
  passed pre-build (they assert on build.sh/fix24.py sources, already
  edited) and the B-B5/B-B6 staged checks passed — so the new checks are
  meaningful: they fail exactly where the fixes are not yet built in.
- **Post-build verifier, first run: 585/586, exit 1.** The single FAIL was
  the check-12 CUT-name sweep — NOT a §16n check. Cause: the B-B6
  insertion added 2 lines at the top of `skills/feature-expansion/SKILL.md`,
  shifting its allow-listed lines +2, so 6 prose-history mentions fell
  off the line-number allow-list (check-12b: 0 imperative dispatches
  hiding in allow-listed lines — no live dispatch anywhere). Fixed
  verifier-side only: the 8 feature-expansion allow-list entries
  re-numbered in verify33.py (49→51, 100→102, 192→194, 194→196, 196→198,
  197→199, 208→210, 215→217), each line's content re-read in the rebuilt
  file and its justification kept with it. No tree change, no rebuild.
  Recorded in SPEC §3(i) as verifier maintenance from D33-30.
- **Final verifier: 586/586, exit 0** (`fix33/verify33-run33d.txt`, 0 FAILs).
  CUT-name sweep back to 0 un-allow-listed, 47 allow-listed, 287 generic
  bare-word noise lines.
- **Scan r4: ALL PASS (76/76, exit 0)** (`scan32-r4-run-fix33d.txt`).
- **Scan r5: ALL PASS (100/100, exit 0)** (`scan32-r5-run-fix33d.txt`;
  run with fix32.py + fix32-patch-log.md adjacent in a probe dir per the
  B-M2 note, probe dir deleted after).
- **Patch log regenerated** (`fix33/fix33-patch-log.md`, md5-identical in
  fix33/ and scratch-repo/fix33/, `8ae4664f7a64a1bf5ae6fd7cfa044ea0`):
  census "grok-4.7-high x20, 'Grok 4.7 High' x7, fast x71 pre"; Changes
  (41); D33-25..D33-35 recorded; OWED-33-5 recorded; OWED-33-4 RE-OPENED
  by audit #111-B, fixed again in round 33d; Step 0 labels corrected.
- **Built tree:** 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks
  (hooks.json; 17 files in `hooks/` — 15 hook .js files + adapter.js +
  hooks.json). Census: ID 0, PROSE 2 (keeps), XID 0, XPROSE 0, fast 72,
  bare 0.
- **less-flat-ui:** global source unchanged, md5
  `cef0249fbf37ba096c688ce78fa4377f`, 534 lines, verified before and after
  the build; built less-flat-ui is a real directory, never a symlink.
- **Drones, fast tier, fix31/fix32 bundles, factory round3 bundle:**
  untouched (fix31/fix32 ran OK in the build; their bundles unchanged).

## 5. Diff stat

`git diff --stat` in scratch-repo: **47 files changed, +196/−126**
(was 40 files, +166/−115 at run 9; pre-build intermediate after the source
edits was 43 files, +184/−124). The 7 new files are the two staged skills
(`new-skills/grill-me/SKILL.md`, `new-skills/feature-expansion/SKILL.md`),
`fix24/fix24.py` (G-4 sub removal — the file was clean before this round;
HEAD already carried the G-4 anchor), and the four built files they feed
(`hackathon-ecc/skills/grill-me/SKILL.md`,
`hackathon-ecc/skills/feature-expansion/SKILL.md`,
`hackathon-ecc/commands/feature-dev.md`,
`hackathon-ecc/commands/react-build.md`). The remaining 33d edits landed
in files already in the diff (build.sh, orch-change-feature skill,
orch-build-mvp skill + command). Stat is quoted identically in
MANIFEST.md:67 and fix33-implementation-report.md:230; no stale
+166/−115 quote remains in any live doc (the 33c report's copy is that
round's history).

## 6. Honest shortfalls

- **The verifier is static, not execution proof.** §16l/§16m/§16n assert
  presence + line order within files. They cannot prove a skill actually
  executes Step 0 or that a trigger loads the skill. The re-audit re-traces
  manually; this round's own trace is §3 above. (Stated in SPEC D33-35.)
- **The §12 CUT allow-list is line-number based and fragile to
  top-of-file insertions.** The B-B6 insertion broke it (see §4); any
  future top insertion in an allow-listed file will break the sweep again
  the same way. The fix is mechanical (re-run the census, re-number), and
  the check-12b companion catches a live dispatch hiding in an
  allow-listed line — but the fragility itself is unchanged.
- **SPEC §3(e) (16f) says "fast 70" where the true pre-state fast count is
  71** — known, out of scope, left as-is per the task (do not fix audit
  observations, only the items listed). Mentioned here so it is not lost.
- **fix13/fix13e-assemble.py historical copies still carry the old pin
  text** — never invoked by build.sh, left as history.
- **fix24 change count dropped 114 → 113** — expected (one G-4 sub
  removed), not a regression.
- **B-B2 is belt-and-suspenders by design:** step 1 both names Step 0 and
  restates the MODEL ask inline, so the check fires even if Step 0 is
  read as classifier-only. §16n asserts both the routing edge and the
  inline ask.

## 7. Files changed / deliverables

- `fix33/SPEC.md` (D33-25…D33-35, §3(i) round-33d subsection, OWED-33-4
  RE-OPENED + OWED-33-5, §1(b) build.sh row, census x20)
- `fix33/MANIFEST.md` (run-10 entry, diff stat, verifier 586/586)
- `fix33/fix33-implementation-report.md` (run-10 row, diff stat, §5
  verifier counts)
- `fix33/fix33.py` (census 25→20, 5 scrub tuples out / 5 guardrail tuples
  in, DECISION-33-19/22 corrected, D33-25…35, OWED-33-4/33-5) — canonical
  + scratch md5-identical
- `fix33/verify33.py` (§16n 21 checks, §13 x20, §16c L95, §16m Step 0,
  §12 allow-list re-numbering) — 586 checks
- `fix33/fix33-patch-log.md` (regenerated, run 10)
- `scratch-repo/build.sh` (fix13-A/fix13e design-role unpin)
- `scratch-repo/fix24/fix24.py` (G-4 sub removed) — canonical + scratch
  md5-identical
- `scratch-repo/new-skills/grill-me/SKILL.md`,
  `scratch-repo/new-skills/feature-expansion/SKILL.md` (MODEL check at entry)
- `fix33/fix-round-33c-report.md` §1.3 (correction banner — original
  wording preserved in git history)
- Logs: `fix33/build-log-run10.txt`, `fix33/verify33-run33d-prebuild.txt`,
  `fix33/verify33-run33d.txt`, `fix33/scan32-r4-run-fix33d.txt`,
  `fix33/scan32-r5-run-fix33d.txt`
- This report: `fix33/fix-round-33d-report.md` (+ scratch-repo copy,
  md5-identical)
