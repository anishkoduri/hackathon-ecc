# Audit #109-A — Fix #33 (unpin the orchestrator): correctness of the fix + the tree

**Auditor:** A-auditor (correctness of the fix itself + the tree).
**Date:** Tue Nov 17, 2026.
**Base:** `dd106ade` (fix #32 close). Scratch repo `~/workspace/hackathon-plugin/fix33/scratch-repo`.
**Worker report audited:** `fix33/fix33-implementation-report.md` (read, but every claim re-verified from scratch; nothing taken on trust).
**Verdict: PASS** — the unpin is complete and correct, verifier and scans pass, guardrail + model-recording + live-test prompt are as specified, and the canonical-tree shortfall is adjudicated (not real — see §2). Two minor docs inaccuracies only (A-M1, A-M2); no blocking findings. Nothing was edited or committed by this audit.

## 1. What verified clean (with numbers)

### 1.1 Tree + HEAD
- `git rev-parse HEAD` in `fix33/scratch-repo` = `dd106ade5f6043ec4ed613919e7908172d8eadce`. Correct.
- `git status` / `git diff --stat`: **33 files changed, +135/−109** — exactly as the worker reported. File list is exactly the expected set: staged (`LIVE_SMOKE_TEST.md`, `README.md`, `build.sh`, `fix30/live-test-prompt.md`, `fix31/fix31.py`, `new-rules/hackathon-mode.mdc`, `new-skills/orchestrate/SKILL.md`, `new-skills/orchestrate/agents/deep-reasoner.md`, `new-skills/orchestrate/references/agent-TEMPLATE.md`) + built `hackathon-ecc/` mirrors of the same edits. No unexpected file. Untracked: `fix32/` and `fix33/` only.
- `fix32/scratch-repo` untouched: HEAD `dd106ade`, `git status` shows only the pre-existing untracked `fix32/` dir, zero modified files.

### 1.2 Verifier re-run (independent)
- `python3 fix33/verify33.py <built-plugin-dir>` (argument form, from `fix33/`, against `scratch-repo/hackathon-ecc`): **526/526 checks pass, exit 0** — reproduced, not just read from `verify33-run3.txt`.
- Scan suites re-run: r4 **76/76 PASS, ALL PASS** (reproduced in place); r5 **100/100 PASS, ALL PASS** (reproduced — see the invocation note in §4; the script needs `fix32.py` + `fix32-patch-log.md` adjacent to it, so it was run from a `/tmp` copy with those two siblings; BASE is a hardcoded absolute path to the scratch-repo built tree, so the run still scored the real tree).
- §16 checks spot-read in `verify33.py` (lines 3430–3610): genuine per-site assertions, not tautologies — 16a census via independent `count_in_tree` (incl. the 69+1+2=72 fast split), 16b exact model-agnostic strings at every §1(c) pin site, 16c guardrail strings, 16e staged census with the single :132 keep asserted by line, 16g import-guard property, 16h live-test prompt, 16i agent `model:` lines, 16j opus mapping + three generated agents, 16k byte-identity guards.

### 1.3 Pin inventory from scratch (independent grep)
Built tree (`scratch-repo/hackathon-ecc`):
- `grok-4.7-high` **x0**, `"Grok 4.7 High"` **x2**, `grok-4.7-extra-high` **x0**, `"Grok 4.7 Extra High"` **x0**, `cursor-grok-4.6-high-fast` **x72**, bare `grok-4.6-high-fast` **x0**. Exactly the worker's post-state.
- The only 2 PROSE hits, eyeballed individually:
  - `skills/strategic-compact/SKILL.md:68` — "`500k Grok 4.7 High`" as a context-window example for a real model. Factual example, not orchestrator identity. **Keep, correct.**
  - `skills/strategic-compact/SKILL.md:102` — "`Grok 4.7 High, Grok 4.6 High Fast, ...`" listing which models lost todo/task tools in Cursor 2.1.233. Factual model list, not orchestrator identity. **Keep, correct.**
- No `"Grok 4.7"` prose anywhere else in the built tree states the orchestrator's model (checked: remaining `orchestrator…Grok` hits are all "Grok 4.6 High" = the fast tier, in the hierarchy paragraphs). No `MODEL-PIN` remnant anywhere in staged or built text. No `"Extra High"` string anywhere in the built tree — the build introduced zero `grok-4.7-extra-high`.
- Staged live sources (`new-skills/`, `new-rules/`, `README.md`, `LIVE_SMOKE_TEST.md`): only hit is `LIVE_SMOKE_TEST.md:132` — "`Grok 4.7 Extra High is the default for this test`" — the classified test-baseline keep. **Correct.** A wider sweep of the whole scratch repo outside `hackathon-ecc/`, `fix*/`, `build.sh`, `FACTORY_CURSOR_PLAN.md` finds pin text only there plus `fix*/` history docs (never edited, out of scope by design).

### 1.4 `model: inherit` mechanism
- Present in exactly the four chat-model agents, staged + built: `agents/deep-reasoner.md:4`, `agents/ecc-architect.md:4`, `agents/ecc-healthcare-reviewer.md:4`, `agents/ecc-spec-miner.md:4`. All other built-agent `model:` lines: **41 × `cursor-grok-4.6-high-fast`**, **4 × `inherit`** = 45 agents, matching the 45-agent count. Zero `model: grok-4.7-high` anywhere in the built tree.
- In-tree evidence for the semantics: staged `deep-reasoner.md` L7 comment states "`inherit` is the Cursor default for subagents: same model as the parent agent (see Cursor docs, Subagents)"; orchestrate L93 picker note states "chat-model subagents carry `model: inherit` and run on the same model"; agent-TEMPLATE.md now instructs "`inherit` for a chat-model role (it runs on the model selected in this chat)". The mechanism is stated at the three places that matter (agent frontmatter, template, orchestrate skill). No remaining agent frontmatter or rule pins the orchestrator to a specific model.
- Honest limit recorded as **OWED-33-1**: `inherit` is doc-verified, not live-verified. The live test is Anish's run, not this audit's. The worker's report and SPEC both state this plainly; it is not hidden.

### 1.5 Guardrail (MODELSEL_F33) + D33-19
- `MODELSEL_F33` appears exactly 2× in orchestrate (staged + built): **L14** identity paragraph and **L62** MODEL check. L14 reads: "if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback (see the MODEL check in step 0)." L62 repeats the rule with the ledger form. L93 picker note carries the pre-build form ("if the picker is on Auto, the orchestrator asks the user to pick a specific model before proceeding"). Reads as specified.
- **D33-19 verified true:** `new-rules/hackathon-mode.mdc` contains zero occurrences of `MODELSEL` / `MODEL check` — L42 is the hierarchy paragraph in model-agnostic wording with no pointer. SPEC §2 D33-5 and D33-19 now correctly record the guardrail home as orchestrate-only and label the original pointer claim a SPEC error, not a tree defect. No other orchestrator-identity site lacks the guardrail: the only identity statements are orchestrate L14/L62/L93 (guarded) and the hierarchy paragraphs (which defer to orchestrate by reference to the picker note / MODEL check). No tree change is owed for the pointer.

### 1.6 Cost accounting (OWED-33-3 adjudication)
- The MODEL check (orchestrate L62, staged + built) records the actual selected model in the run ledger (`MODEL: <name>` — the actual selected model) and states: "A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool."
- **Adjudication: sufficient for this fix, not a blocking gap.** The fix's scope is removing the plugin's assumption of the orchestrator's identity; the MODEL check supplies exactly the fact a cost decision needs (which model actually ran) at the point of use, and forbids the specific failure the old pin caused (assuming Grok/pool). A full cost-accounting rule would be a new feature, not a fix-#33 defect. OWED-33-3 is correctly carried as an open item, not a defect. (The factory's COST-ACCOUNTING is separate, factory round 4's job.)

### 1.7 Live-test prompt
- `fix30/live-test-prompt.md`: canonical and scratch-repo copies md5-identical (`cd679e5e7ecd5f5ace654294ada24b47`).
- Title: "Fix #33 live-test prompt — selected-model orchestrator (Grok 4.7 Extra High selected for the test)". Header states: select **Grok 4.7 Extra High** in the model picker before starting — "this is Anish's default, and the test's baseline: since fix #33 the orchestrator runs on whatever model is selected, so the test verifies the SELECTED model runs the parent." Pass criterion: "the parent agent ran the model selected in the picker (Grok 4.7 Extra High for this test) on both Task A and Task B". Tasks A/B unchanged. As specified.

### 1.8 Drones + fast tier untouched
- Fast tier: 72 `cursor-grok-4.6-high-fast` occurrences (71 pre-existing + 1 in the new schema description, D33-17 — the description names the fast tier; no fast pin added or removed). All 45 agents' `model:` lines are `inherit` (4) or fast (41). `model-route.md` merged line keeps fast for deterministic low-risk mechanical changes.
- Drones: no `deepseek`/`qwen` model slugs in the built tree. The only DeepSeek/Qwen mentions are by name in the pre-existing GLOBAL-ROUTING prose (factory dispatch, unchanged) plus a `deepseek-harness-setup` manifest key description and a code comment — none is a model pin. Drone pins live in the factory tree, untouched by this fix. `FACTORY_CURSOR_PLAN.md` still pins the orchestrator (OWED-33-2, factory round 4's job — correctly excluded, verifier scope D33-7).

### 1.9 Build integrity
- Build log run 6: `fix33: 31 change(s)`, `fix33: OK`, `fix32: OK`, `BUILD EXIT: 0` trailer present. Run 5 likewise exit 0. The fix33 patch log shows **31 changes / 0 errors**, pre-state census `grok-4.7-high x25, 'Grok 4.7 High' x7, fast x71, XID x0, XPROSE x0` and post-state `ID x0, PROSE x2 (keeps), XID x0, XPROSE x0, fast x72` — matching the SPEC's measured census (D33-16/D33-17).
- Global less-flat-ui source md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines — verified unchanged. Fake-HOME copy is a real directory (`drwxrwx---`), never a symlink. Fake HOME is `fix33/fakehome33` on real disk, not `/tmp`.
- Build.sh functional sites: opus mapping `"opus": "inherit"` (line 169) with comment "opus -> inherit (the model selected in this chat, fix #33)"; no `fix30/fix30.py` invocation remains (only the retirement comment block); six STEP 5 audit2_patch anchor lines now `model: inherit` (build.sh:10164/:10174/:10806/:10816/:11441/:11452). The remaining `model: grok-4.7-high` lines in build.sh (astra-review heredoc :7825 + STEP 5 astra anchor :11592/:11599/:11615) are old-side source text that fix29 rewrites and fix33.py unpins downstream — the built `astra-review.md` reads `Model: inherit` (:41), proving the pipeline. **No stale rename re-pins the orchestrator**: fix30 is retired, no `grok-4.7-extra-high` is introduced by the build (built-tree XID x0, XPROSE x0).
- fix31.py / fix32.py `EXPECT_PIN` = `{OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}`; both copies of each md5-identical (fix31 `cae364c594befc6a303ecd0ceed3d447`, fix32 `2cc17cec8120209b3142417693cdac43`); fix33.py canonical + scratch md5-identical (`c8bfd3e0bd72dfa7fc0bc8b47ccc4047`).

## 2. Canonical-tree shortfall — adjudication: MISFRAMING, not real

The worker's honest shortfall — "the verifier's staged checks pass for the scratch-repo tree (the deliverable); they would fail against the canonical tree, whose staged sources were not unpinned — the commit leg owns that merge" — is **not a defect and nothing is owed beyond the normal commit leg**.

Evidence:
- The canonical tree `~/workspace/hackathon-plugin/` is **not a git repo** (no `.git`); it is the old built snapshot (fix #31 tree: built tree still carries 49 `grok-4.7-extra-high`; staged `new-skills/orchestrate/SKILL.md` still carries 15 `grok-4.7-high`). It is, by the task brief's own statement, "the OLD built tree (fix #31) — do NOT expect it to be unpinned."
- The fix #32 precedent, verified from the commit itself: `git show dd106ade` in the scratch repo touches **27 `hackathon-ecc/` files plus staged sources (`new-skills/`, `new-rules/`) and `build.sh`** — i.e. the fix-#32 commit carried the built tree AND the staged sources together, straight from the scratch-repo working tree. No `fix*/` dir was in that commit (only `fix28/callmap` files appear under `fix*`). The fix-#33 commit leg does exactly the same thing: commit the 33 tracked-file changes already sitting in `fix33/scratch-repo`. There is no "merge" to own and no extra step: the staged edits and the built-tree edits are both already in the scratch repo, in the same 33-file diff.
- The canonical tree is updated when Anish installs the new bundle — that is the established install path, not a fix-#33 debt. The verifier failing against the canonical tree is therefore the expected pre-commit state, not a shortfall of this fix.

**What the commit leg must do (exact):** commit the 33 tracked modified files in `fix33/scratch-repo` (the `+135/−109` diff), leaving the untracked `fix32/` and `fix33/` dirs in place (same as fix #32, whose `fix32/` was likewise untracked and uncommitted — the build needs `fix32/fix32.py` and `fix33/fix33.py` at `$PLUGIN_ROOT` at build time). Nothing else.

## 3. Findings

### Blocking — none (A-B: none)

No surviving orchestrator pin, no verifier failure, no guardrail defect, no stale rename, no live-test prompt error.

### Minor — 2 (docs inaccuracies; neither changes the tree)

- **A-M1 — SPEC §1(b) + implementation report §2(d) state stale build.sh literal counts.** Both say build.sh carries "56 ID + 5 PROSE occurrences (52 lines)". Measured post-fix33: **48 ID + 6 PROSE + 1 XID**. Reconciliation (all accounted for): D33-15 removed 6 ID (the six STEP 5 anchor `model:` lines → `inherit`) and the opus-mapping change removed 2 ID (dict entry + mapping comment) — 56 − 8 = 48; the new fix33 invocation comment block at build.sh:24139 adds 1 PROSE (`"Grok 4.7 High"`) — 5 + 1 = 6. The 56/5 figures are the pre-fix33 numbers, presented without a "pre-fix33" label in a keep-list table that otherwise describes the current tree. Fix: label them pre-fix33 or update to 48/6. No tree impact — the remaining 48 ID are old-side anchors/heredocs and the built tree proves none of them survives into output.
- **A-M2 — build.sh fix33 invocation comment block carries a stale fast count.** It says fix33.py "asserts the fast-worker pin unchanged (70)". The fix33 build's measured fast counts are **71 pre-state / 72 post-state** (D33-16/D33-17: 70 + 1 staged-weave mention, + 1 schema-description mention). Comment only; the functional census in fix33.py is correct (71/72) and the build passes on it. Fix: change "(70)" to "(71 pre-state, 72 post-state)" or drop the number.

## 4. Observations (not findings)

- **r5 invocation quirk (reproduced, not a defect).** `scan32-r5-test-fix33.py` line 849 opens `fix32.py` adjacent to itself and line ~854 reads `fix32-patch-log.md` from the same directory, so running it in place in `fix33/` fails with `FileNotFoundError` (`fix33/fix32.py` does not exist). The worker's `scan32-r5-run-fix33.txt` (ALL PASS) is genuine: reproduced 100/100 PASS by running a copy from `/tmp` with `fix32.py` + `fix32-patch-log.md` alongside. Worth one line in the MANIFEST so the next auditor doesn't mistake the in-place failure for a scan failure.
- **Verifier leaves tiny /tmp litter.** Four `fix33guard33*` dirs (~60–68K each, copies of `fix33.py` + `__pycache__`) sit in `/tmp` — leftovers of verify33's 16g import-guard check (one per verifier run: worker runs 1–3 + this audit's re-run). Trivial size (~260K total on a 512M tmpfs at 62%), no pollution issue for the build, but the check should clean up after itself.
- **Canonical-tree edits outside the scratch repo.** The worker also updated two canonical files outside the scratch repo: `~/workspace/hackathon-plugin/fix31/fix31.py` and `~/workspace/hackathon-plugin/fix30/live-test-prompt.md` (both now md5-identical to their scratch copies, as the report states). Harmless — the canonical tree is the stale snapshot that the fix-#33 bundle install will replace — but note that canonical `fix31.py` now asserts the post-unpin census against a still-pinned canonical tree, so a build run from the canonical tree would fail at fix31's census. Nobody should build from the canonical tree; builds run from scratch-repo clones.
- **`/tmp` is 62% full (315M used) but the fix33 build did not use it** (fake HOME on real disk, TMPDIR/NPM_CONFIG_CACHE redirected to `fix33/.tmp` / `fix33/.npm-cache`). No ENOSPC risk from this fix.

## 5. Commands / results (exact)

- `cd fix33/scratch-repo && git rev-parse HEAD` → `dd106ade5f6043ec4ed613919e7908172d8eadce`
- `git diff --stat` → `33 files changed, 135 insertions(+), 109 deletions(-)`; `git status --short` → 33 modified + untracked `fix32/`, `fix33/` only
- `cd fix33 && python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc` → `526/526 checks pass`, exit 0
- `python3 scan32-r4-test-fix33.py` → 76 PASS, `RESULT: ALL PASS`; r5 (from `/tmp/audit109-r5` with `fix32.py` + `fix32-patch-log.md` alongside) → 100 PASS, `RESULT: ALL PASS`
- Built census: `grep -rho` → ID 0, PROSE 2 (strategic-compact :68/:102), XID 0, XPROSE 0, fast 72, bare fast 0
- Staged live: only `LIVE_SMOKE_TEST.md:132` keep; `MODEL-PIN` x0 staged+built; `model: grok-4.7-high` x0 built; agent `model:` values 41 fast + 4 inherit
- `build.sh`: ID occurrences 48, PROSE 6, XID 1; opus mapping `"opus": "inherit"`; no `fix30/fix30.py` invocation; STEP 5 anchors 6× `model: inherit`
- Build log run 6: `fix33: 31 change(s)`, `fix33: OK`, `BUILD EXIT: 0`; patch log: 31 changes / 0 errors
- less-flat-ui global md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines; fake-HOME copy a real directory
- Live-test prompt md5 `cd679e5e7ecd5f5ace654294ada24b47` (canonical = scratch)
- `git show dd106ade --stat` → 27 `hackathon-ecc/` files + staged + `build.sh`; no `fix*/` dir in the commit
- `~/workspace/hackathon-plugin` is not a git repo; canonical built tree still 49 XID (fix #31 tree, as expected)

## 6. What remains owed (not this fix's defects)

- **OWED-33-1:** `inherit` doc-verified, not live-verified — the updated live-test prompt is Anish's run (OWED-30-3, carried forward).
- **OWED-33-2:** `FACTORY_CURSOR_PLAN.md` still pins the orchestrator — factory round 4.
- **OWED-33-3:** no cost-accounting text in the regular tree — adjudicated sufficient for this fix (§1.6); a cost rule would be a new feature.
- Commit leg: commit the 33 tracked files from `fix33/scratch-repo` (§2). No bundle/push in this fix (per brief).
