# Fix #33, round 33c — report (Nov 17, 2026)

Fix worker report for the coordinator. Fixes all findings from audit #110
(NOT PASS, 110-M1), sweep #53 (NOT CLEAN, S-M1 + S-M2), and dry-run #50
(NOT PASS, D-1 + D-2). This round changes TREE BEHAVIOR, so a rebuild +
verifier extension were required. **Nothing committed.**

- Fix dir: `~/workspace/hackathon-plugin/fix33/`
- Scratch repo: `~/workspace/hackathon-plugin/fix33/scratch-repo`,
  git HEAD `dd106ade`
- Pre-round state (audit #109): 33 files, +136/−109 (the fix-33b build.sh
  comment reflow had added one line over the +135/−109 in the docs)
- Post-round state: **40 files changed, +166/−115**

## 1. Findings and what changed

### 1.1 110-M1 + S-M1 (same finding, stale diff stat) — FIXED

MANIFEST.md and fix33-implementation-report.md still said +135/−109; the
measured stat was +136/−109. Fixed by recording the NEW stat after this
round's own edits:

- `fix33/MANIFEST.md:62` — now "40 files changed, +166/−115"
- `fix33/fix33-implementation-report.md:203` — now "40 files changed,
  +166/−115"
- Grep for `+135` / `135/−109` / `+136` / `136/−109` across the fix dir,
  SPEC.md, MANIFEST.md, fix33.py, verify33.py: **zero live matches remain**.
  The `fix-round-33b-report.md` §8 before/after lines (+135 → +136) and the
  audit/sweep leg reports' quotes are historical as-of-then statements and
  were deliberately left alone — they record what was true when written.

### 1.2 D-1 + S-M2 (guardrail sequencing) — FIXED by re-sequencing, not rewording

On Auto, grill-me ran BEFORE the MODEL check fired (hackathon-mode L12
"grill-me FIRST" vs orchestrate L62 "immediately after grill-me"), so
orchestrate L14's "before proceeding" overstated the sequencing. The
phase-2 spec requires the orchestrator to tell the user to pick a specific
model BEFORE PROCEEDING — grill-me is proceeding.

**Changes (staged sources; the staged weave is the mechanism here):**

- `scratch-repo/new-skills/orchestrate/SKILL.md`
  - L14: cross-ref now reads "(see the MODEL check below — it runs before
    grill-me)". L14's "before proceeding" now reads true as written — the
    ask precedes all work.
  - L52 (new block under `## Run`): the operative MODEL check, moved out of
    step 0. It fires in the first reply, before grill-me starts; grill-me
    does not start until a specific model is picked. MODELSEL_F33 still
    appears 2x in orchestrate (L14 + L52).
  - L62: one-engine paragraph sequence now "MODEL check → grill → scope →
    expansion → build".
  - L64 (step 0): the old operative MODEL check replaced with a
    back-reference ("already ran before grill-me — if the model is still
    Auto … stop and ask again").
  - L95 (picker note): cross-ref updated to the pre-grill block.
- `scratch-repo/new-rules/hackathon-mode.mdc`
  - L12: rewritten so the MODEL clause textually precedes "grill-me FIRST":
    "the MODEL check (fix #33, MODELSEL_F33) runs first — before grill-me:
    if the selected model is Auto … tell the user to pick a specific model
    before grill-me starts. Then run `grill-me` FIRST among build steps…"
    The first build sequence now reads "MODEL check → grill →
    narration-key prompt → …".
  - §7 (L61): names the MODEL check as the one question preceding grill-me.

**New decisions (SPEC.md §2):**

- **D33-20 — MODEL check re-sequenced before grill-me.** The MODEL check is
  a PRECONDITION, not a build step. D33-19's "no pointer" stance is revised
  for hackathon-mode L12/§7 only (a pointer, not the operative check — the
  home stays orchestrate); the D33-19 correction itself (the L42 pointer
  was never woven) stands as history.
- **D33-21 — "Proceeding" defined; grill-me-first-for-build-work
  preserved.** "Before proceeding" means before ANY work, grill-me included
  — grill-me is proceeding (D-1). The standing "grill-me FIRST" rule is
  about BUILD work; the model ask is not build work. Both rules now state
  this explicitly.

**Verifier (§16l, 9 checks):** line-order MODEL-check-before-grill-me in
staged + built orchestrate and hackathon-mode; MODELSEL_F33 still 2x in
orchestrate; step-0 back-reference; L14 accuracy; grill-me-first preserved;
§7. §16c check 4 now asserts the bold MODEL check lives in the pre-grill
block.

### 1.3 D-2 + OWED-33-4 (guardrail bypass in direct commands) — FIXED now

`/gan-build`, `/gan-design`, `/astra-review`, `/orch-*` contained zero
MODELSEL_F33 / MODEL-check / Auto-ask text; their cold starts never route
through orchestrate step 0. Dry-run #50 walked `/gan-build` and showed a
full build proceeds on Auto with no ask — the exact harm the guardrail
guards. The coordinator overruled the OWED-33-4 deferral: fixed this round.

**Inventory (grepped, not guessed — 9 files):**
`commands/gan-build.md`, `commands/gan-design.md`, `commands/astra-review.md`,
`commands/orch-add-feature.md`, `commands/orch-build-mvp.md`,
`commands/orch-change-feature.md`, `commands/orch-fix-defect.md`,
`commands/orch-refine-code.md`, `commands/orchestrate.md` (the five orch-*
match the `orch-*` glob; orchestrate.md is the /orchestrate command).

**Mechanism (fix33.py built-tree replacements — these files have no staged
source; they exist only in the built tree, generated by build.sh heredocs +
fix patches):** 10 new REPLACEMENTS (fix33.py change count 31 → 41).

- Full MODEL check (MODELSEL_F33 wording, mirroring orchestrate) at the
  entry of `commands/gan-build.md` (built L5, right after frontmatter,
  before arg parsing), `commands/gan-design.md` (built L5),
  `commands/astra-review.md` (built L6, before `# Deep Review`), and
  `skills/orch-pipeline/SKILL.md` Step 0 (built L43 — see below).
- `skills/orch-pipeline/SKILL.md` Step 0 is the shared choke point for the
  five orch-* commands: Step 0 is the first thing the engine does, before
  the size classifier and before Phase 0 Intake (which always runs). It was
  verified genuine for the five orch-* commands only (each orch-* skill's
  step 1 runs the engine; orch-build-mvp runs Phases 0–2 in step 1 and
  Phases 3–6 in its later steps). gan-build/gan-design/astra-review do NOT
  route through it, so they carry the full ask at their own entries.
  The check sits at Step 0, not Intake, because the size classifier runs
  before the phases list — an Intake check would not precede all entry
  work (this was found by the verifier's own line-order check in iteration
  2; see §4).
- One-line guardrail references (MODELSEL_F33) at the entry of each orch-*
  command file (built L7) and `commands/orchestrate.md` (built L7),
  pointing at the operative check ("the `orch-pipeline` engine runs its
  MODEL check first (Step 0, before classifying)" / "the orchestrate
  skill's MODEL check runs first, before grill-me"). So MODELSEL_F33 is
  present in EVERY direct command file and no cold start bypasses the ask.
- A downstream `/gan-build` drive (orch-build-mvp step 4, `--skip-planner`)
  re-runs the check after the model is already picked, so it passes
  silently — no second ask.

**New decisions (SPEC.md §2, MANIFEST.md, fix33.py patch-log output):**

- **D33-22 — Direct-command guardrail weave** (mechanism + per-command list
  as above).
- **D33-23 — OWED-33-4 SUPERSEDED / FIXED** by D33-22 in this round. The
  history of the deferral-and-reversal stays readable (SPEC.md §6,
  MANIFEST.md, fix33.py OWED list, patch log) — not deleted.

**Verifier (§16m, 29 checks):** MODELSEL_F33 in all 9 command files; full
ask in gan-build/gan-design/astra-review/orch-pipeline Step 0; pointers in
the five orch-* + orchestrate.md command files; guardrail-before-first-work-
step line-order per file (gan-build < "### Phase 0: Setup"; gan-design <
"### Setup"; astra-review < "## Step 1: Scope"; orch-* < "## What It Does";
orchestrate.md < "$ARGUMENTS"; orch-pipeline MODEL check is the first
content of Step 0, before the size classifier).

**D33-24 — Verifier extended.** verify33.py gains §16l + §16m; §16c check 4
split (pre-grill location check + ledger/cost check); §16f asserts
D33-15..D33-24 + OWED-33-4 SUPERSEDED. **Verifier count: 526 → 565.**

## 2. Rebuilds

Invocation (per MANIFEST.md — fake HOME `fix33/fakehome33` on real disk,
NOT /tmp; MS_DIR/UIPRO_DIR/SKILL_SRC at `fix26/scratch-clones`;
TMPDIR/NPM_CONFIG_CACHE at `fix33/.tmp` / `fix33/.npm-cache`):

```sh
# each run, from fix33/fakehome33/workspace/hackathon-plugin:
HOME=~/workspace/hackathon-plugin/fix33/fakehome33 \
MS_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/hack-skills \
UIPRO_DIR=~/workspace/hackathon-plugin/fix26/scratch-clones/uipro \
SKILL_SRC=~/workspace/hackathon-plugin/fix26/scratch-clones/skill-add \
TMPDIR=~/workspace/hackathon-plugin/fix33/.tmp \
NPM_CONFIG_CACHE=~/workspace/hackathon-plugin/fix33/.npm-cache \
bash build.sh > ~/workspace/hackathon-plugin/fix33/build-log-runN.txt 2>&1
echo "BUILD EXIT: $?" >> ~/workspace/hackathon-plugin/fix33/build-log-runN.txt
```

| Run | Result | Notes |
| --- | --- | --- |
| 7 | **EXIT 0** (~161s) | Round 33c first rebuild. fix33: 41 changes, 0 errors, fix33 OK. Pre-rebuild verifier 524/565 (41 expected FAILs against the un-rebuilt tree). Post-rebuild verifier **562/565** — 3 real FAILs, fixed in iteration 2 (see §4). |
| 8 | EXIT 1 (~2s) | Iteration-2 rebuild attempt. Failed at the ui-ux-pro-max copy: the pre-build re-sync used `rsync --delete`, which the MANIFEST invocation does NOT use, and emptied the fakehome's `fix26/scratch-clones/` copies (scratch-repo has no fix26/). See §5 for the root cause. |
| 9 | **EXIT 0** (~127s) | Round 33c rebuild after iteration 2. fix33: 41 changes, 0 errors, fix33 OK; fix31 OK, fix32 OK. |

Sync-back (runs 7 and 9): built tree (`hackathon-ecc/`, rsync `--delete`)
+ `fix33/fix33-patch-log.md` only (both copies md5-identical,
`4d31215dba852f0c86b19381ee7990cc`). The five historical logs
(fix16/fix24/fix25/fix26/fix27) and the fix31/fix32 regenerated logs were
NOT synced back.

## 3. Verification (run 9 tree)

- **verify33.py: 565/565 checks pass, exit 0** (`fix33/verify33-run33c.txt`,
  0 FAILs). Pre-rebuild run was 524/565 (expected — new checks against the
  un-rebuilt tree).
- **Scan r4: ALL PASS** (76 checks, exit 0, `scan32-r4-run-fix33c.txt`).
- **Scan r5: ALL PASS** (100 checks, exit 0, `scan32-r5-run-fix33c.txt`;
  run with fix32.py + fix32-patch-log.md adjacent in a probe dir per the
  B-M2 note, probe dir deleted after).
- **Built tree:** 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks;
  census ID 0, PROSE 2 (keeps), XID 0, XPROSE 0, fast 72, bare 0.
- **Staged-vs-built:** orchestrate staged vs built differ only in the 3
  known build.sh `code-reviewer` → `code-reviewer` agent
  (`agents/ecc-code-reviewer.md`) path rewrites; hackathon-mode differs
  only in the known fix16 `claude -p` → `CLI-subprocess` scrub. Both are
  pre-existing build transformations, covered by the verifier's
  staged/built checks (all passing).
- **less-flat-ui:** global source unchanged, md5
  `cef0249fbf37ba096c688ce78fa4377f`, 534 lines, verified before and after
  the builds; built less-flat-ui is a real directory, never a symlink.
- **Diff stat:** `git diff --stat` in scratch-repo: **40 files changed,
  +166/−115** (was 33 files, +136/−109 pre-round). The 7 new files are the
  five orch-* command files + `commands/orchestrate.md` + the
  `skills/orch-pipeline` skill. Stat is quoted identically in MANIFEST.md:62
  and fix33-implementation-report.md:203; no stale +135/+136 quote remains
  in any live doc.
- **Drones, fast tier, fix31/fix32 bundles, factory round3 bundle:**
  untouched (fix31/fix32 ran OK in the build; their bundles unchanged).

## 4. Iteration 2 — what the first post-rebuild verification caught

Run 7's post-rebuild verifier was 562/565 with 3 real FAILs (plus r4
failing on a hardcoded line number). All three were fixed in iteration 2
and the tree rebuilt as run 9:

1. **CUT-name sweep (check-12):** the allow-listed `ecc-recipes` line in
   `skills/orchestrate/SKILL.md` moved 137 → 139 because the staged
   +2-line insertion shifted everything below it. Fix: verify33.py
   ALLOW_LIST entry 137 → 139. (The verify33.py comment already warns that
   staged-owned files' allow-list line numbers shift with edits — this was
   that case.)
2. **16l hackathon-mode L12 order:** the MODEL clause textually FOLLOWED
   "run `grill-me` FIRST" in the sentence ("…run `grill-me` FIRST … with
   one precondition: the MODEL check … runs before grill-me"), so the
   line-order assertion failed. Fix: rewrote L12 so the MODEL clause comes
   first ("the MODEL check … runs first — before grill-me: … Then run
   `grill-me` FIRST among build steps…") and updated the verifier's phrase
   to "runs first".
3. **16m orch-pipeline order:** the MODEL check was woven into Phase 0
   Intake, but the file's "## Step 0 — Classify size" section precedes the
   phases list, so the check did not precede all entry work (the size
   classifier runs first and states a tier to the user). Fix: moved the
   operative check from Intake to Step 0 (first content of the section,
   built L43, before "Ceremony scales to blast radius"), updated the five
   orch-* pointers to "(Step 0, before classifying)", and updated the
   verifier's Intake check + line-order check. SPEC D33-22, §3(h),
   MANIFEST D33-22, and the fix33.py DECISION-33-22 string were updated to
   match (Step 0, not Intake).
4. **r4/r5 (c2) hardcoded site:** both scan suites hardcode the
   pre-fix site at `skills/orchestrate/SKILL.md:171`; the +2-line staged
   insertion moved it to 173. Fix: sites 171 → 173 in
   `scan32-r4-test-fix33.py`, `scan32-r5-test-fix33.py`, and the verify33.py
   check name that cites the site.

No finding required a redesign: every fix was a line-number update, a
sentence reorder, or a move of the check one section earlier in the same
file. The coordinator's stop condition (bigger redesign than a per-entry
guardrail line) was never triggered.

## 5. Process note — the fakehome `fix26/scratch-clones/` copies (run 8)

Run 8 failed because the pre-build re-sync added `rsync --delete`, which
the MANIFEST invocation does not use. Two facts combine to make that
destructive here:

- scratch-repo has no `fix26/` directory, so `--delete` emptied the
  fakehome's `fix26/scratch-clones/` copies.
- The build invocation sets `HOME` first, so the later `~/workspace/...`
  env paths (`MS_DIR`, `UIPRO_DIR`, `SKILL_SRC`) expand under the fake
  HOME — the build reads those inputs from the fakehome's own
  `fix26/scratch-clones/` copies, not the durable ones at
  `~/workspace/hackathon-plugin/fix26/scratch-clones/`. (Verified by probe:
  with `HOME` set to the fakehome, `UIPRO_DIR=~/workspace/...` expands to
  `…/fakehome33/workspace/hackathon-plugin/fix26/scratch-clones/uipro`.)

Recovery: the three clone dirs (hack-skills, uipro, skill-add) were restored
from the durable copies and the build re-run as run 9 (exit 0). Rule going
forward: **never `--delete` a re-sync into fakehome** — the MANIFEST setup
rsync has no `--delete` for exactly this reason. This note is also recorded
in MANIFEST.md (run 8 entry).

## 6. Honest shortfalls / known stale artifacts

- `weave33.py` (the original staged-weave script) still contains the old
  L62 MODEL-check text and "(see the MODEL check in step 0)" strings. It
  was deliberately NOT updated — it is a historical one-off script, not run
  by build.sh (same precedent as the historical patch logs).
- The fix-33b round's run-5/run-6 patch logs still carry the stale
  DECISION-33-5 wording as historical record (md5
  `ddef5b7aa229ceff138d3cf3e450960c`) — not rewritten; the new run-7 and
  run-9 patch logs carry the corrected D33-5 + D33-20..D33-24.
- The run-7 post-rebuild verifier result (562/565, the 3 iteration-2 FAILs)
  was written to `verify33-run33c.txt` and then overwritten by the run-9
  565/565 pass; the 562/565 figure survives only in this report and in the
  MANIFEST run-7 entry. The pre-rebuild 524/565 result was observed on
  stdout, never saved to a file. The run-7 build log is kept at
  `build-log-run7.txt`.
- The live test of the guardrail in a real Cursor chat (the
  fix33/live-test-prompt.md prompt) is still owed and can only be done by
  Anish on Windows — this round verifies the guardrail text and placement
  statically (565 checks + r4/r5), not by running it.
- D33-19 is not re-litigated: orchestrate remains the guardrail's home for
  the main flow; this round extends the guardrail to the direct commands
  without moving the home.

## 7. Files changed in this round

- Staged: `scratch-repo/new-skills/orchestrate/SKILL.md` (L14, L52 block,
  L62, L64, L95), `scratch-repo/new-rules/hackathon-mode.mdc` (L12, §7 L61)
- `fix33/fix33.py` (31 → 41 REPLACEMENTS; md5
  `8e878b28fe287534afff27f6ca92a9a4`, both copies identical) +
  `scratch-repo/fix33/fix33.py`
- `fix33/verify33.py` (526 → 565 checks; §16l + §16m; CUT allow-list
  137 → 139; check-name site 171 → 173)
- `fix33/SPEC.md` (D33-20..D33-24, §3(e)/(h), §6 OWED-33-4 SUPERSEDED),
  `fix33/MANIFEST.md` (Decisions, OWED-33-4 SUPERSEDED, stat, run 7/8/9
  entries, verify33.py bullet), `fix33/fix33-implementation-report.md`
  (stat, run table rows 7–9, §5 round-33c paragraph)
- `fix33/scan32-r4-test-fix33.py`, `fix33/scan32-r5-test-fix33.py` (site
  171 → 173)
- Built tree (synced back): 7 newly-modified files — the five
  `commands/orch-*.md`, `commands/orchestrate.md`,
  `skills/orch-pipeline/SKILL.md` — plus the staged-weave effects in
  `skills/orchestrate/SKILL.md` and `rules/hackathon-mode.mdc`
- Logs: `fix33/build-log-run7.txt` (EXIT 0), `fix33/build-log-run8.txt`
  (EXIT 1), `fix33/build-log-run9.txt` (EXIT 0), `fix33/verify33-run33c.txt`
  (565/565), `fix33/scan32-r4-run-fix33c.txt`, `fix33/scan32-r5-run-fix33c.txt`,
  `fix33/fix33-patch-log.md` (41 changes, 0 errors; md5
  `4d31215dba852f0c86b19381ee7990cc`, both copies identical)

**Nothing committed.**
