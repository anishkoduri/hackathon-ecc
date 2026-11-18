# Sweep #54 — Fix #33 (unpin the orchestrator): whole-tree re-sweep

**Sweeper:** sweep #54 (whole scratch-repo tree, staged + built).
**Date:** Tue Nov 17, 2026.
**Base:** `dd106ade` (fix #32 close). Scratch repo `~/workspace/hackathon-plugin/fix33/scratch-repo`.
**Context:** fix round 33c fixed audit #110 (110-M1), sweep #53 (S-M1 + S-M2), and dry-run #50 (D-1 + D-2); re-audit #111 A + B ran in parallel. This sweep re-verified every round-33c claim from scratch and enumerated entry points independently rather than trusting the "9 direct commands" count.
**Did not edit or commit anything.** All probes were reads/greps plus independent re-runs of the verifier and scan suites. The `/tmp/sweep54-r5*` probe dirs were deleted after use. `git status` in the scratch repo is unchanged after this sweep.

## Verdict: NOT CLEAN — 1 minor finding, 0 blocking

The tree itself is clean: no surviving orchestrator pin, no guardrail bypass, no re-sequence failure, no demotion regression, no build inconsistency. The single finding is a docs-only wording slip of exactly the class round 33c was fixing — the iteration-2 "Step 0, not Intake" update was applied to the mechanism sentences but missed the pointer-target labels in six live spots. The tree, the command pointers, and the verifier's assertions all say Step 0; only the labels say Phase 0. Per the sweep verdict rules, any real finding means NOT CLEAN, so this sweep does **not** end clean.

## 1. Finding

### S-M1 (minor) — "orch-pipeline Phase 0" named as the MODEL check's location in six live spots; the check sits at Step 0

- **Measured truth (this sweep):** the operative check is the first content of orch-pipeline **Step 0** (`hackathon-ecc/skills/orch-pipeline/SKILL.md:43`, section heading L41, classifier text "Ceremony scales to blast radius" after it). **Phase 0 is Intake** — a different section (`## The phases`, L60). The five orch-* command files point at "(Step 0, before classifying)" (L7 each), and the verifier's §16m assertions test the Step 0 pointer text and Step 0 ordering.
- **Still written in six live spots:**
  1. `fix33/SPEC.md:108` (D33-22): "…pointing at the operative check (orch-pipeline Phase 0 / the orchestrate skill)…" — in the same sentence that correctly says "orch-pipeline Step 0 (the shared choke point…)" and "it sits at Step 0, not Intake". Internally contradictory.
  2. `fix33/SPEC.md:233` (§6 OWED-33-4): "…(full ask in gan-build/gan-design/astra-review + orch-pipeline Phase 0; …)".
  3. `fix33/fix33.py:516` (DECISION-33-22 string): same "(orch-pipeline Phase 0 / the orchestrate skill)" parenthetical.
  4. `fix33/fix33.py:525` (OWED-33-4 string): "…(full ask in gan-build/gan-design/astra-review + orch-pipeline Phase 0; …)".
  5. `fix33/fix33-patch-log.md:71, :80` — generated from the fix33.py strings above, so the same wording.
  6. `fix33/verify33.py:3696` (§16m check name): "`… points at the orch-pipeline Phase 0 MODEL check`" — and the §16m header comment `:3677–3679`: "full ask at the gan/astra entries and in orch-pipeline Phase 0 (the shared choke point…)".
- **Why it is minor, not blocking:** the verifier's assertions behind the mislabeled check name test the *correct* thing — line 3696's check asserts the pointer string "the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying)" is present, and the Step 0 check asserts the MODEL check opens Step 0 before the classifier. No behavior, no tree text, and no verification outcome changes. It is a label/doc staleness only.
- **Cause:** round 33c report §4 item 3 claimed "SPEC D33-22, §3(h), MANIFEST D33-22, and the fix33.py DECISION-33-22 string were updated to match (Step 0, not Intake)". The update landed in the mechanism sentences (SPEC §3(h) correctly says "Step 0 (before the size classifier)"; MANIFEST D33-22 correctly says "orch-pipeline Step 0"; MANIFEST:139 correctly describes the move as "from orch-pipeline Phase 0 Intake to Step 0") but missed the pointer-target parentheticals and the §16m labels.
- **Fix:** replace "Phase 0" with "Step 0" in SPEC.md:108, SPEC.md:233, fix33.py:516, fix33.py:525, verify33.py:3677–3679, verify33.py:3696. The patch log regenerates from fix33.py on the next rebuild; do not hand-edit it. No rebuild is needed for the SPEC/verify33.py label fixes beyond re-running the verifier to confirm the count is unchanged (565/565).
- **Scope check:** a full grep for the check-location phrase finds it nowhere else as a wrong location. The other "Phase 0" hits are correct: MANIFEST:139 (describes the move), 33c-report L110/L227 (describe the move), verify33.py:3705 + gan-build's "### Phase 0: Setup" (a real section heading used as a line-order anchor), and the Intake references in the Step 0 paragraph itself.

## 2. What swept clean (with numbers)

### 2.1 Surviving pins — none

Built tree (`scratch-repo/hackathon-ecc/`, independent `grep -rho` counts):

| Pattern | Found | Expected |
|---|---|---|
| `grok-4.7-high` (ID) | 0 | 0 |
| `Grok 4.7 High` (PROSE) | 2 | 2 (keeps only) |
| `grok-4.7-extra-high` (XID) | 0 | 0 |
| `Grok 4.7 Extra High` (XPROSE) | 0 | 0 |
| `cursor-grok-4.6-high-fast` (FAST) | 72 | 72 |
| bare `grok-4.6-high-fast` (lookbehind check) | 0 | 0 |
| `Extra High` (any) | 0 | 0 |
| `MODEL-PIN` (retired ledger format) | 0 | 0 |

The 2 PROSE hits eyeballed individually, both in `skills/strategic-compact/SKILL.md`: `:68` ("500k Grok 4.7 High", context-window example) and `:102` ("Grok 4.7 High, Grok 4.6 High Fast, …", factual list of models that lost todo/task tools). **Keep, correct.**

Agent `model:` inventory (built, 45/45 files carry a line): **41 × `cursor-grok-4.6-high-fast` + 4 × `inherit`** (`deep-reasoner.md`, `ecc-architect.md`, `ecc-healthcare-reviewer.md`, `ecc-spec-miner.md`). Zero `model: grok-4.7-high` anywhere in the built tree.

### 2.2 Entry points — enumerated independently, all 9 covered, no tenth found

All 55 files in `hackathon-ecc/commands/` were listed and checked for `MODELSEL_F33`. Exactly the 9 claimed files carry it, and no other command file does:

| File | MODELSEL_F33 | Guardrail line | First work step after it |
|---|---|---|---|
| `commands/gan-build.md` | 1 | L5, full ask | `### Phase 0: Setup` (after L5) |
| `commands/gan-design.md` | 1 | L5, full ask | `### Setup` (after L5) |
| `commands/astra-review.md` | 1 | L6, full ask | `# Deep Review` L8, `## Step 1: Scope` L12 |
| `commands/orch-add-feature.md` | 1 | L7, full Auto conditional inline | `## What It Does` L25 |
| `commands/orch-build-mvp.md` | 1 | L7, full Auto conditional inline | `## What It Does` L24 |
| `commands/orch-change-feature.md` | 1 | L7, full Auto conditional inline | `## What It Does` (after L7) |
| `commands/orch-fix-defect.md` | 1 | L7, full Auto conditional inline | `## What It Does` (after L7) |
| `commands/orch-refine-code.md` | 1 | L7, full Auto conditional inline | `## What It Does` (after L7) |
| `commands/orchestrate.md` | 1 | L7, full Auto conditional inline | `$ARGUMENTS` (after L7) |

- The other 46 command files score 0 for `MODELSEL_F33`. The build-ish ones were checked for routing into orchestrated work: `feature-dev`, `react-build`, `build-fix`, `loop-start`, `prp-implement`, `prp-plan`, `resume-session`, `demo`, `auto-update`, `setup-pm`, `model-route` — **zero** references to orchestrate / orch-pipeline / gan-build / gan-design / astra-review / deep-reasoner / drone dispatch. `plan.md` and `code-review.md` grep hits were description text only. `review-pr.md` mentions `/orchestrate` as a routing pointer *to* the guarded path ("for the adversarially-verified pass use /orchestrate"), not a bypass.
- `skills/orchestrate/references/dispatch-prompt.md`: 0 `MODELSEL_F33` / MODEL-check hits — correct, it is a template the orchestrator uses after the pre-grill check fires; its only `model:` line is L211, the mechanical-tier worked example (`model: cursor-grok-4.6-high-fast` for the fast-worker role).
- Skill entries: the skills whose text says the user invokes them directly are `orch-build-mvp` ("runs only when the user invokes `/orch-build-mvp` directly"), `orch-pipeline`, and `orchestrate` — all guarded paths. The other matches (`ck`, `context-budget`, `hairline-create`, `pitch-deck-video`) are utility skills, not orchestrated-build entries.

### 2.3 Orch-pipeline choke point — verified structurally, not on trust

- `skills/orch-pipeline/SKILL.md`: `## Step 0 — Classify size` at L41; the MODEL check at **L43 is the first content of the section**, before the classifier prose ("Ceremony scales to blast radius" follows the check). The phases list starts later (`## The phases`, L60); Phase 0 Intake is inside it. A check at Intake would not have preceded the classifier — the Step 0 placement is genuine.
- The five orch-* skills: four say "Run the `orch-pipeline` engine" in step 1 (whole engine, Step 0 included); `orch-build-mvp` step 1 runs "orch-pipeline Phases 0–2 ONLY" and its later steps run Phases 3–6, with the phase mask at L25. Its entry is covered at the command level regardless (see O-2).
- The orch-* command L7 lines are stronger than the "one-line pointer" description: each states the full Auto conditional inline ("if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback"), prefixed by the pointer ("the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying)"). The command entry is self-contained even apart from the engine. `commands/orchestrate.md` L7 likewise states the full conditional and points at "the orchestrate skill's MODEL check runs first, before grill-me".
- Downstream `/gan-build` drive (`orch-build-mvp` step 4, `--skip-planner`, skill L64): re-enters `gan-build.md`, whose L5 full check fires again — after the model is already picked, so it passes silently. No second ask, no bypass.

### 2.4 Re-sequence (D33-20/D33-21) — real

- Staged + built `skills/orchestrate/SKILL.md` (identical lines in both): **L14** cross-ref "(see the MODEL check below — it runs before grill-me)"; **L52** pre-grill block "**MODEL check — first, before grill-me (fix #33, MODELSEL_F33):** … Grill-me does not start until a specific model is picked"; **L64** step 0 back-reference ("already ran before grill-me … if the model is still Auto … stop and ask again"); **L95** picker note "(see the MODEL check, before grill-me)". `MODELSEL_F33` exactly 2× in orchestrate (L14 + L52), staged + built. No operative MODEL check remains in step 0.
- Staged + built `rules/hackathon-mode.mdc`: **L12** — "the MODEL check (fix #33, MODELSEL_F33) runs first — before grill-me: … tell the user to pick a specific model before grill-me starts. Then run `grill-me` FIRST among build steps … grill-me is the first BUILD step, and the MODEL check is not build work." The MODEL clause textually precedes "grill-me FIRST". **§7 L61** — "…plus the MODEL check just before it (fix #33, MODELSEL_F33), the one question that precedes grill-me…".
- D33-21 wording present in both files ("MODEL check is a precondition, not a build step, so grill-me stays FIRST among build steps").

### 2.5 Consistency — stat, demotion, call-map, decisions

- **Diff stat:** `git diff --stat HEAD` in `fix33/scratch-repo` = **40 files changed, 166 insertions(+), 115 deletions(-)**. HEAD `dd106ade5f6043ec4ed613919e7908172d8eadce`, confirmed. `git status --short`: 40 modified + untracked `fix32/`, `fix33/` only. The 7 new files vs the pre-33c 33-file diff are exactly the five `commands/orch-*.md` + `commands/orchestrate.md` + `skills/orch-pipeline/SKILL.md`.
- **Stat quotes:** MANIFEST.md:62 and fix33-implementation-report.md:203 both read "40 files changed, +166/−115". Grep for `+135` / `+136` over SPEC.md, MANIFEST.md, fix33-implementation-report.md, fix33.py, verify33.py: **zero hits**. The only `+135`/`+136` hits in the fix dir are in `fix-round-33c-report.md` itself, as as-of-then historical statements about the pre-round stat — the same class as the 33b report's §8 lines, deliberately left.
- **Trigger manifest** `hackathon-ecc/manifests/context-packs/skill-triggers@1.json`: **48 trigger keys**, coverage `skills 72 / withTriggers 48`. `ui-ux-pro-max` appears nowhere in it (0 hits); `skill:design-taste-frontend` present. Counts: skills 72, agents 45, rules 48, commands 55, hooks 15 (16 `.js` files + `hooks.json`).
- **Call-map:** `skills/orchestrate/references/call-map.md` counts 72/45/48/55/15, matching the fix28 sidecar `fix28/callmap/call-map-data.json`; verifier §15 checks pass inside this sweep's independent 565/565 re-run. The fix33 diff touches no call-map file.
- **D33-20…D33-24 each have their in-tree effect:** D33-20 re-sequence (§2.4 above); D33-21 "proceeding" definition (§2.4); D33-22 direct-command weave (§2.2–2.3); D33-23 OWED-33-4 SUPERSEDED (SPEC §6 L233 + MANIFEST OWED section, kept not deleted); D33-24 verifier 565 checks (§16l 9 + §16m 29; §16c check 4 asserts the pre-grill location; §16f asserts D33-20…D33-24 + OWED-33-4 SUPERSEDED).
- **SPEC §3(h)** correctly says "Step 0 (before the size classifier)" for the guardrail weave; **MANIFEST D33-22** correctly says "orch-pipeline Step 0". fix33.py has 35 REPLACEMENTS tuples producing 41 applied changes (patch log lists 41 change bullets, 0 errors).

### 2.6 Untouched areas — drones + fast tier byte-identical except documented changes

- `git diff --name-only dd106ade` contains no `*openrouter*`, `*drone*`, or `*dispatch*` path. No `deepseek`/`qwen` slugs in the built tree (same pre-existing caveat as dry-run #50 leg 7: the versioned drone pins live in the factory tree / fix30 SPEC, not this tree).
- `git diff dd106ade -- fix31/fix31.py`: ONLY the `EXPECT_PIN` census update (`{OLD_ID: 0, OLD_PROSE: 0, FAST_ID: 70, NEW_ID: 49, NEW_PROSE: 22}` → `{OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}`) plus the explanatory comment. fix31.py copies md5-identical (`cae364c594befc6a303ecd0ceed3d447`, canonical + scratch); fix32.py copies md5-identical (`2cc17cec8120209b3142417693cdac43`). No bundle files appear in the diff.
- Fix #32 demotion files changed by fix33: only the files the unpin intentionally touches. `skills/ui-ux-pro-max/SKILL.md` is untouched (still "LOOKUP ONLY (fix #32)") and is not in the diff list. `strategic-compact/SKILL.md` diff is exactly the two keep lines in High form (D33-16).
- Staged vs built byte-diff for the fix33-touched staged files is only the known classes: orchestrate differs at L102/L276/L283 (fix27 `code-reviewer` → `agents/ecc-code-reviewer.md` agent-link rewrite); hackathon-mode differs at L38 only (fix16 `claude -p` → CLI-subprocess scrub). Both pre-existing at HEAD, not fix33 regressions.

### 2.7 Dead / broken references — none found

- No remaining reference to the retired fix30 rename as a current mechanism: the only `fix30`/`fix #30` mentions in the built tree are the GLOBAL-ROUTING drone-assignment sentence ("fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work") — pre-existing, about drones, not the rename. build.sh carries only the retirement comment block (L24129–24136) and the fix33 invocation (L24152); no `fix30/fix30.py` invocation remains.
- No reference to "step 0" meaning the old MODEL-check location as operative, except SPEC §3(a)'s old-text quotes (L117/L125) — the pre-fix wording being replaced, correct as history.
- All cross-reference line numbers verified real in the built tree: orchestrate L14/L52/L64/L95, hackathon-mode L12/§7 L61, gan-build L5, gan-design L5, astra-review L6, orch-* L7, orchestrate.md L7, orch-pipeline L43. `weave33.py`'s old L62 text is addressed in §2.8.

### 2.8 Build artifacts — clean

- `__pycache__` in the scratch-repo tree: only the 4 known inherited fix31 dry-run dirs (`fix31/dryrun46/leg5-testcov/{src,tests}/__pycache__`, `fix31/leg5-rerun/leg5-testcov/{src,tests}/__pycache__`). No other `__pycache__` anywhere in the tree.
- Symlinks: exactly one — `hackathon-ecc/node_modules/.bin/js-yaml -> ../js-yaml/bin/js-yaml.js`. Tracked in git, unchanged vs `dd106ade`, a normal npm `.bin` link. Built `less-flat-ui` is a real directory (`drwxrwx---`), never a symlink.
- No reference to a fake HOME under /tmp anywhere in the staged or built tree (0 hits). The single repo-wide hit for that path string is `fix33/sweep53-report.md:108,164` — the sweep-53 report's own sentence stating the check result, inside the untracked `fix33/` dir, not a build path. See O-3.
- Global less-flat-ui source pristine: md5 `cef0249fbf37ba096c688ce78fa4377f`, **534 lines** — verified unchanged.
- Run-8 rsync accident left no residue: the durable clones at `fix26/scratch-clones/` are intact (`hack-skills`, `uipro`, `skill-add`, plus `ecc-repo-clean`, all populated). `weave33.py` holds the old L62 MODEL-check text (L59, L118) as claimed — and the claim that it is not run is verified: build.sh contains no `weave33` reference, and a repo-wide grep for `weave33` outside `fix33/` returns zero. Historical one-off, not a finding.

### 2.9 Fix-round verification — the six #109 minors stay fixed, 110-M1/S-M1/D-1/D-2 fixed

Spot-checked each: A-M1/B-M4 (build.sh counts 48 ID / 6 PROSE / 1 XID, SPEC §1(b) agrees); A-M2 (comment "71 pre-state, 72 post-state"); B-M2 (r5 adjacency note in MANIFEST, reproduced both ways — in-place crash, with-siblings pass); B-M3 (DECISION-33-5 "carries no pointer" in both live fix33.py copies); the canonical fix31.py story (§2.6); 110-M1/S-M1 (stat now +166/−115, §2.5); D-1/S-M2 (re-sequence, §2.4); D-2/OWED-33-4 (direct-command weave, §2.2–2.3).

## 3. Independent re-runs (this sweep)

| Check | Command | Result |
|---|---|---|
| Verifier | `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` | **565/565 checks pass, exit 0** (reproduced, not read from run33c) |
| Scan r4 | `python3 scan32-r4-test-fix33.py` (from `fix33/`) | **ALL PASS, 76 checks, exit 0** (re-runs in place) |
| Scan r5 | copy + `fix32.py` + `fix32-patch-log.md` alongside in `/tmp/sweep54-r5c` (deleted after) | **ALL PASS, 100 checks, exit 0** |
| Build log run 9 | tail + grep | **BUILD EXIT: 0**; `fix33: 41 change(s)`, `fix33: OK`, `fix31: OK`, `fix32: OK` |
| Patch log | `fix33-patch-log.md` | `## Changes (41)`, 41 bullets, **Errors (0)**; md5 `4d31215dba852f0c86b19381ee7990cc` both copies |
| fix33.py copies | md5 | `8e878b28fe287534afff27f6ca92a9a4` both copies |

## 4. Observations (not findings)

- **O-1 — The orch-* command L7 lines are stronger than the "one-line pointer" description.** Each states the full Auto conditional inline, not just a pointer (see §2.3). The D33-22 wording ("one-line guardrail reference") understates them; the tree is better than the description. No action needed.
- **O-2 — orch-build-mvp's skill file never names Step 0.** It has zero "Step 0"/"classify" mentions and zero MODELSEL; its guardrail coverage rests on the command file's L7 full ask plus the engine's Step 0. The skill states it runs only when the user invokes `/orch-build-mvp` directly, so the command is the entry and this is not a bypass — but if the skill were ever invocable without its command, Step 0's firing would rest on "run Phases 0–2" implying engine entry. Worth one line in the skill if it is ever edited for another reason; not a finding now.
- **O-3 — The fake-HOME-path grep is self-referential.** Any sweep report that writes the literal path string into `scratch-repo/fix33/` creates the next grep's only hit (sweep53's report did this; this report deliberately phrases the check without the literal string in the synced copy). Future legs: exclude `fix33/` from that grep, or phrase the report without the literal.
- **O-4 — 35 REPLACEMENTS tuples, 41 applied changes.** The counts reconcile (some tuples apply more than one change; the patch log lists 41 bullets) — no discrepancy.
- **O-5 — Adjudicated items re-confirmed as recorded, not re-reported.** OWED-33-1 (`model: inherit` doc-verified, live test owed to Anish); OWED-33-2 (`FACTORY_CURSOR_PLAN.md` still pins — factory round 4); OWED-33-3 (no cost-accounting text — adjudicated sufficient); run-7 562/565 output overwritten by run 9 (figure survives in the 33c report + MANIFEST); run-8 rsync accident recovered with the rule recorded (§2.8).

## 5. What remains owed (not this sweep's defects)

- **S-M1 fix:** replace "Phase 0" with "Step 0" in SPEC.md:108, SPEC.md:233, fix33.py:516, fix33.py:525, verify33.py:3677–3679, verify33.py:3696. Patch log regenerates from fix33.py on the next rebuild. Re-run the verifier after (expect 565/565 unchanged — only a check name and a comment change there). No tree change, no rebuild needed for the fix itself.
- **OWED-33-1:** live test (Anish's run in Cursor, updated prompt).
- **OWED-33-2:** factory plan doc unpin (factory round 4).
- **OWED-33-3:** cost accounting (new feature if ever wanted).
- Commit leg: commit the 40 tracked files from `fix33/scratch-repo` (+166/−115), leaving untracked `fix32/` and `fix33/` in place. No bundle/push in this fix.

## 6. Commands / results (exact)

- `cd fix33/scratch-repo && git rev-parse HEAD` → `dd106ade5f6043ec4ed613919e7908172d8eadce`; `git diff --stat HEAD` → `40 files changed, 166 insertions(+), 115 deletions(-)`; `git status --short` → 40 modified + untracked `fix32/`, `fix33/` only (unchanged after this sweep)
- Built census: `grep -rho` → ID 0, PROSE 2 (strategic-compact :68/:102), XID 0, XPROSE 0, fast 72, bare fast 0; `Extra High` 0; `MODEL-PIN` 0
- Agent `model:` inventory: built 41 fast + 4 inherit (45/45 with a line)
- `MODELSEL_F33` in built tree: 12 files — the 9 command files + `rules/hackathon-mode.mdc` + `skills/orch-pipeline/SKILL.md` + `skills/orchestrate/SKILL.md`; staged: orchestrate + hackathon-mode only
- Orchestrate MODELSEL 2× staged + built (L14 + L52); step-0 back-ref L64; picker note L95; hackathon-mode L12 MODEL clause before "grill-me FIRST"; §7 L61 "the one question that precedes grill-me"
- Direct commands: gan-build L5, gan-design L5, astra-review L6 (< `# Deep Review` L8, < `## Step 1: Scope` L12), orch-* L7 (< `## What It Does`), orchestrate.md L7; orch-pipeline MODEL check L43, first content of Step 0 (heading L41)
- Commands enumeration: 55 files in `commands/`; 46 score 0 for `MODELSEL_F33`; build-ish non-9 commands score 0 for orch/gan/dispatch references; `review-pr.md` points *to* `/orchestrate`
- Trigger manifest: triggers dict 48 keys, coverage skills 72 / withTriggers 48; `ui-ux-pro-max` 0 hits
- Call-map: `call-map.md` 72/45/48/55/15; sidecar `fix28/callmap/call-map-data.json`
- `git diff --name-only dd106ade | grep -i 'openrouter\|drone\|dispatch'` → empty; `git diff dd106ade -- fix31/fix31.py` → EXPECT_PIN census + comment only
- fix31.py copies md5 `cae364c594befc6a303ecd0ceed3d447`; fix32.py copies md5 `2cc17cec8120209b3142417693cdac43`; fix33.py copies md5 `8e878b28fe287534afff27f6ca92a9a4`; patch-log copies md5 `4d31215dba852f0c86b19381ee7990cc`
- `verify33.py` → 565/565 exit 0; r4 → 76 PASS ALL PASS; r5 (with siblings, probe dir deleted) → 100 PASS ALL PASS; build-log-run9 → BUILD EXIT: 0, fix33 41 changes, fix31 OK, fix32 OK
- less-flat-ui global md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines; built + fake-HOME copies real directories; fake-HOME-under-/tmp path in staged/built tree 0 (sole repo-wide hit is sweep53-report.md's own sentence, untracked `fix33/`)
- `__pycache__`: only the 4 known fix31 dry-run dirs; symlinks: only tracked `node_modules/.bin/js-yaml`, unchanged vs HEAD
- `weave33.py`: no reference in build.sh; repo-wide grep outside `fix33/` → zero; old L62 text present (L59, L118) as historical one-off
- S-M1: `grep -rn 'orch-pipeline Phase 0'` over live docs → SPEC.md:108, SPEC.md:233, fix33.py:516, fix33.py:525, fix33-patch-log.md:71/:80, verify33.py:3677–3679/:3696; all other "Phase 0" hits are correct (move descriptions, real headings, Intake references)
