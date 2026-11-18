# Sweep #53 — Fix #33 (unpin the orchestrator): whole-tree sweep

**Sweeper:** sweep #53 (whole scratch-repo tree, staged + built).
**Date:** Tue Nov 17, 2026.
**Base:** `dd106ade` (fix #32 close). Scratch repo `~/workspace/hackathon-plugin/fix33/scratch-repo`.
**Context:** audit #109-A PASSED (2 minor) + #109-B PASSED (4 minor); fix round 33b corrected all six; re-audit #110 and dry-run #50 ran in parallel (their reports landed in `scratch-repo/fix33/` during this sweep; this sweep's verdict is independent, but its findings were cross-checked against them — see §6).
**Did not edit or commit anything.** All probes were reads/greps plus independent re-runs of the verifier and scan suites (which write only their own stdout). The `/tmp/sweep53-r5` probe dir was deleted after use. `git status` in the scratch repo is unchanged after this sweep.

## Verdict: NOT CLEAN — 2 minor findings, 0 blocking

The tree itself is clean: no surviving orchestrator pin, no stale rename, no guardrail absence, no demotion regression, no build inconsistency. Both findings are docs/wording staleness of exactly the class the fix-33b round was fixing — one is a new stale number the round itself introduced (already flagged by re-audit #110 as 110-M1, independently re-verified here), the other is a guardrail-sequencing overstatement the dry-run surfaced (D-1, independently re-verified here). Neither changes tree behavior. Per the sweep verdict rules, any real finding means NOT CLEAN, so this sweep does **not** end clean.

## 1. Findings

### S-M1 (minor) — diff stat stale in two living docs after the fix-33b round's own +1 line

- **Measured now (twice, this sweep):** `git diff --stat HEAD` in `fix33/scratch-repo` = **33 files changed, 136 insertions(+), 109 deletions(-)**. HEAD `dd106ade5f6043ec4ed613919e7908172d8eadce`, confirmed.
- **Still written in two places that describe the current tree:**
  - `fix33/MANIFEST.md:60` — "`git (scratch-repo):` 33 files changed, **+135/−109**."
  - `fix33/fix33-implementation-report.md:200` — "`git status` (scratch-repo): 33 files changed, **+135/−109**."
- **Cause:** the fix-33b round's build.sh comment reflow (A-M2 fix) added exactly one insertion line (+135 → +136, deletions unchanged at 109). The round's own report (§8) records the new stat correctly ("After this round: 33 files changed, +136/−109"), but the round did not update these two lines.
- **Fix:** change `+135` to `+136` in both lines. No tree impact — docs staleness only, same class as A-M1/B-M4 (which this round was supposed to eliminate).
- **Scope check:** a full `grep -rn '+135'` over the fix dir finds the number elsewhere only where it is correct as a historical statement — audit #109-A/B (the stat at audit time), the fix-round report §8 "Before this round" line, and re-audit #110's own description of the stale lines. The staleness is confined to the two lines above. (The `scratch-repo/fix33/` copies of the audit reports carry the same historical figures, correctly as-of then.)
- **Cross-check:** re-audit #110 found this independently as 110-M1 (its sole finding, verdict NOT PASS). This sweep re-verified it from scratch rather than taking it on trust.

### S-M2 (minor) — guardrail sequencing: on Auto, grill-me runs before the MODEL check fires

- **Facts (verified from the tree, this sweep):**
  - `new-rules/hackathon-mode.mdc:12` (staged; same in built): "After the user sends the first hackathon project prompt, run `grill-me` FIRST, before any scoping, building, or expansion."
  - `hackathon-ecc/skills/orchestrate/SKILL.md:62` (built; same in staged): step 0 is the "Narration-key prompt (the orchestrator sends it — **immediately after grill-me**, before scoping, at the start of the build)" and carries the **MODEL check (fix #33, MODELSEL_F33)**.
  - `skills/orchestrate/SKILL.md:14` (identity paragraph): "if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model **before proceeding**".
- **Gap:** the ask is sequenced at step 0, *after* grill-me — nothing in the tree orders it ahead of grill-me, so on Auto the grill-me Q&A runs before any Auto ask fires. The ask does block scoping, the design package, and dispatch, and no silent fallback is permitted past step 0 — the silent-fallback prohibition itself holds. The failure is the grill-me ordering only: L14's "before proceeding" reads as if the ask precedes all work, but grill-me is work that precedes it.
- **Not a fix33 regression:** the pre-fix33 tree at HEAD sequences it identically — `git show dd106ade:hackathon-ecc/skills/orchestrate/SKILL.md` L62 is the same step-0 heading ("immediately after grill-me") carrying the old MODEL-PIN check. Fix #33 renamed the check and reworded it; it did not move it.
- **What is owed:** a coordinator decision. If the intent is "the ask fires before any *build* work", this is a wording/sequencing note: qualify D33-5 / L14 so "before proceeding" is explicitly "before scoping, design, or dispatch (step 0, after grill-me)". If the intent is literally "grill-me waits", the tree needs a re-sequence (ask before grill-me) — a fix-round decision, not a sweep edit.
- **Cross-check:** dry-run #50 found this independently as D-1 (leg 1 FAIL) and reached the same coordinator-decision framing. This sweep re-verified the line evidence from scratch.

## 2. What swept clean (with numbers)

### 2.1 Surviving pins — none

Built tree (`scratch-repo/hackathon-ecc/`, independent `grep -rho` counts):

| Pattern | Found | Expected |
|---|---|---|
| `grok-4.7-high` (ID) | 0 | 0 |
| `Grok 4.7 High` (PROSE) | 2 | 2 (keeps only) |
| `grok-4.7-extra-high` (XID) | 0 | 0 |
| `Grok 4.7 Extra High` (XPROSE) | 0 | 0 |
| `cursor-grok-4.6-high-fast` (FAST) | 72 | 72 (71 + 1 schema description, D33-17) |
| bare `grok-4.6-high-fast` (lookbehind check) | 0 | 0 |
| `Extra High` (any) | 0 | 0 |
| `MODEL-PIN` (retired ledger format) | 0 | 0 |

The 2 PROSE hits eyeballed individually, both in `skills/strategic-compact/SKILL.md`:
- `:68` — "`500k Grok 4.7 High`" — context-window example for a real model. Factual example, not orchestrator identity. **Keep, correct.**
- `:102` — "`Grok 4.7 High, Grok 4.6 High Fast, ...`" — factual list of models that lost todo/task tools in Cursor 2.1.233. **Keep, correct.**

Staged live sources (`new-skills/`, `new-rules/`, `README.md`, `LIVE_SMOKE_TEST.md`, `round2-skills/`, `rewritten-skills/`): only hit is `LIVE_SMOKE_TEST.md:132` — "`Grok 4.7 Extra High is the default for this test`" — the classified test-baseline keep. **Correct.** Repo-wide `grok-4.7|Grok 4.7` grep outside `hackathon-ecc/`, `fix*/`, `audit-scripts/`, `build.sh`, `FACTORY_CURSOR_PLAN.md`, `LIVE_SMOKE_TEST.md`: **zero** hits. `FACTORY_CURSOR_PLAN.md` keeps match the documented factory-round-4 scope exactly (ID x1, XID x2, XPROSE x2 — OWED-33-2, unchanged).

Case-insensitive `grok` sweep of the built tree: every remaining hit eyeballed and benign — the 41 fast-tier `model:` lines, `Grok 4.6 High` prose (fast tier), `ngrok` substrings, Grok brand/icon references in `design-taste-frontend` asset credit files. Zero "Brain: Grok" / "parent agent, Grok" / "orchestrator is Grok" hits (the single "runs on Grok" substring hit is `LIVE_SMOKE_TEST.md:134`, "Fast tier runs on Grok 4.6 High Fast" — the fast tier, not the orchestrator).

### 2.2 Agent frontmatter inventory — exactly 4 `inherit`, 41 fast, 0 other

- Built `hackathon-ecc/agents/`: 45/45 files carry a `model:` line (line 4 in every file). `model: inherit` x4 — `deep-reasoner.md`, `ecc-architect.md`, `ecc-healthcare-reviewer.md`, `ecc-spec-miner.md`. `model: cursor-grok-4.6-high-fast` x41. Zero `model: grok-4.7-high` anywhere in the built tree.
- Staged agents: 3/3 carry a `model:` line — `deep-reasoner.md:4` `inherit`, `fast-worker.md:4` fast, `scout.md:4` fast.
- Whole-tree `^model:` grep finds only these plus the two `agent-TEMPLATE.md` copies (L4 `CHANGE-ME` template: "`inherit` for a chat-model role … or pin exactly one Grok model ID for a fixed tier …"), `audit-scripts/` history, and build.sh machinery lines.
- `agents/ecc-gan-planner.md` frontmatter is fast while its prose (:3, :44) says the design-lead works "on the model selected in this chat" — as SPEC'd (§1(c): its `model:` is fast; the design-lead is invoked inline as the orchestrator, orchestrate L28), not a miss.

### 2.3 Stale rename — retired, no re-pin path

- `fix30/fix30.py` invocation: **gone** from build.sh. Only the retirement comment block remains (L24129–24136). `fix33/fix33.py` invoked at L24152, in fix #30's old slot (after fix29, before fix31).
- Opus mapping (build.sh L160–181): `"opus": "inherit"` with comment "opus -> inherit (the model selected in this chat, fix #33)". Read in code, not just grepped.
- `grok-4.7-high` in build.sh: 48 occurrences, all on lines ≤ 24139, **none after the fix33 invocation (L24151)** — verified with `awk 'NR>24151 && /grok-4.7-high|Grok 4.7 High|extra-high/'` (empty). All are old-side anchors/heredoc sources that write pin text before fix33.py runs; fix33.py replaces exactly that text and the built census is 0. `grok-4.7-extra-high` in build.sh: 1 occurrence (L24130, retirement comment only). `Grok 4.7 High` in build.sh: 6, matching the corrected SPEC §1(b) (48 ID + 6 PROSE + 1 XID).
- Six STEP 5 `audit2_patch` anchor lines now `model: inherit` (build.sh:10164/:10174/:10806/:10816/:11441/:11452). The remaining `model: grok-4.7-high` lines in build.sh (astra-review heredoc :7825 + STEP 5 astra anchor :11592/:11599/:11615) are old-side source text that fix29 rewrites and fix33.py unpins downstream — the built `astra-review.md` reads `Model: inherit` (:41), proving the pipeline.
- Build logs run 5 and run 6 both end `BUILD EXIT: 0`; run 6 shows `fix33: 31 change(s)`, `fix33: OK`, `fix32: OK`. Patch log: 31 changes / 0 errors, pre-state census ID x25 / PROSE x7 / fast x71 / XID x0 / XPROSE x0, post-state ID x0 / PROSE x2 (keeps) / fast x72 — matching SPEC D33-16/D33-17.

### 2.4 Consistency — demotion intact, guardrail as specified, live-test prompt exact

- Trigger manifest `hackathon-ecc/manifests/context-packs/skill-triggers@1.json`: **48 trigger keys**, coverage `skills 72 / withTriggers 48`. `ui-ux-pro-max` appears nowhere in the triggers (demotion: lookup-only, no trigger key); `skill:design-taste-frontend` is present. Counts: skills 72, agents 45, rules 48, commands 55, hooks 15 (hooks.json lists 15 entries; the 17 files in `hooks/` are 16 `.js` + `hooks.json` — same 17 files as the fix32 tree, no change).
- Call-map: verify33 §15 checks `skills/orchestrate/references/call-map.md` against the fix28 sidecar `call-map-data.json` with counts 72/45/48/55/15/48 and 0 uncalled rules — passed in this sweep's independent verifier re-run (526/526). The fix33 diff touches no callmap file.
- `MODELSEL_F33` exactly 2× in orchestrate, staged + built: **L14** identity paragraph and **L62** MODEL check, worded as specified (Auto / cannot-be-determined disjunction, "tell the user to pick a specific model before proceeding", "do not silently orchestrate on an unknown fallback", ledger `MODEL: <name>`, "cost is marked unknown, never assumed to be Grok/pool"). L93 picker note carries the pre-build form. `hackathon-mode.mdc` contains zero `MODELSEL` / `MODEL check` occurrences (staged + built) — D33-19 verified true, guardrail home is orchestrate-only.
- Live-test prompt (`fix30/live-test-prompt.md`): canonical and scratch-repo copies md5-identical (`cd679e5e7ecd5f5ace654294ada24b47`). Title states the selection; header says select **Grok 4.7 Extra High** before starting ("this is Anish's default, and the test's baseline"); PASS = "the parent agent ran the model selected in the picker (Grok 4.7 Extra High for this test) on both Task A and Task B". Tasks A/B unchanged.
- Per-site spot-checks (all as SPEC §3(c)): schema enum `["cursor-grok-4.6-high-fast", "inherit"]` with the `inherit` description (:35–36); model-route merged to one chat-model line (:16–17); GAN harness `GAN_*_MODEL` examples all "set it to the model selected in this chat" (:83/:96/:113); astra-review :24/:32/:41 (incl. `Model: inherit`); gan-planner :3/:44; pi-core.json:333 "(model selected in this chat)"; built README:69 picker note; common-agents :34 (`inherit` for the chat-model agents); common-performance :13/:30; all five orch-* design-role lines ("The design role runs on the model selected in this chat").
- DESIGNPKG-AUTO and GLOBAL-ROUTING blocks byte-identical between orchestrate and hackathon-mode (verify33 §16k passed in re-run; GLOBAL-ROUTING block compared identical directly). The staged-vs-built line differences found at orchestrate L100/L274/L281 and hackathon-mode L38 are **pre-existing at HEAD** (verified via `git show dd106ade:` — staged lacks the `agents/ecc-code-reviewer.md` link the built copy carries, and staged says "upstream `claude -p` invocation path" where built says "upstream CLI-subprocess invocation path"): the known fix27 agent-rewrite and fix16 scrub diff classes, not fix33 regressions.
- Staged vs built byte-identical for the fix33-touched staged files except those known classes: `deep-reasoner.md` IDENTICAL, `agent-TEMPLATE.md` IDENTICAL.
- Dispatch-prompt (`skills/orchestrate/references/dispatch-prompt.md`): 0 pin text. Its only `model:` pin is L211, the mechanical-tier worked example (`model: cursor-grok-4.6-high-fast` for the fast-worker role — correct); reasoning templates route to the named deep-reasoner, which carries `model: inherit` in frontmatter. No bypass of an orchestrator decision (the parent is already running).

### 2.5 Untouched areas — drones + fast tier byte-identical except documented changes

- `git diff dd106ade` touches no `*openrouter*`, `*drone*`, or `*dispatch*` path. `fast-worker.md` / `scout.md` (built + staged) diffs are empty.
- Fast count reconciles: 70 (fix30 tree) + 1 (staged weave, orchestrate L93 picker note) + 1 (schema description, D33-17) = 72. No fast pin added or removed.
- No `deepseek`/`qwen` model slugs in the built tree. The only DeepSeek/Qwen mentions are by name in the pre-existing GLOBAL-ROUTING prose (factory dispatch, unchanged). (Caveat carried from dry-run #50 leg 7: the versioned drone pins DeepSeek V4.1 Flash 1017 / Qwen3 Coder 30B do not appear as slugs in the regular built tree — they live in the factory tree / fix30 SPEC. The dispatch path is intact and unchanged; the versioned IDs are not verifiable from this tree. Pre-existing, not a fix33 change.)
- Fix #32 demotion files changed by fix33: only the files the unpin intentionally touches (orchestrate, hackathon-mode, deep-reasoner, TEMPLATE, gan-planner, astra-review, gan-build/design, model-route, common-agents/performance, schema, gan-style-harness, orch-* skills, pi-core, READMEs, strategic-compact, build.sh, fix31.py, live-test prompt). Every change in the 33-file diff is unpin-related: model wording, the census constants, or the build.sh comment. `skills/ui-ux-pro-max/SKILL.md` untouched (still "LOOKUP ONLY (fix #32)").
- `strategic-compact/SKILL.md` diff is exactly the two keep lines, Extra High → High form (consequence of fix30's retirement, D33-16) — the only change to that file.
- `fix31/fix31.py` diff vs HEAD is ONLY the `EXPECT_PIN` census update + comment (verified hunk by hunk). `fix32/fix32.py` is untracked at HEAD (no tracked diff exists for it, expected — same as fix #32); both copies (canonical + scratch) carry `EXPECT_PIN = {OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}` and the D33-18 anchor wording, md5-identical (`2cc17cec8120209b3142417693cdac43`). fix31.py copies md5-identical (`cae364c594befc6a303ecd0ceed3d447`). fix33.py copies md5-identical (`1533f4e8f56f3ab9a200f6a4d894014a`). Patch-log copies md5-identical (`ddef5b7aa229ceff138d3cf3e450960c`).

### 2.6 Dead / broken references — none found

- No remaining reference to the retired fix30 rename as a current mechanism: the only `fix30`/`fix #30` mentions in the built tree are the GLOBAL-ROUTING drone-assignment sentence ("fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work") — pre-existing, about drones, not the rename.
- No reference to `grok-4.7-extra-high` as a current value anywhere in staged or built text (0 occurrences).
- Cross-references checked exist in the built tree: `skills/orchestrate/references/design-inventory.md`, `dispatch-prompt.md`, `agent-TEMPLATE.md`, `agents/deep-reasoner.md`, `rules/hackathon-mode.mdc`, `commands/model-route.md`, `schemas/agent.schema.json`.
- `fix33.py`: `_dirs` sorted (D33-12, lines 122–123), `__main__` guard present (D33-14, line 503; module level `BASE = ''` / `ROOT = ''`), pre-state census constants `OLD_ID: 25` etc. match the measured census.

### 2.7 Build artifacts — clean except known items

- `__pycache__` in the scratch-repo tree: only the 4 known inherited fix31 dry-run dirs (`fix31/dryrun46/leg5-testcov/{src,tests}/__pycache__`, `fix31/leg5-rerun/leg5-testcov/{src,tests}/__pycache__`). No other `__pycache__` anywhere in the tree.
- Symlinks: exactly one — `hackathon-ecc/node_modules/.bin/js-yaml -> ../js-yaml/bin/js-yaml.js`. It is tracked in git (`git ls-files` lists it), unchanged vs `dd106ade` (empty diff), a normal npm `.bin` link — not a fix33 artifact. Built `less-flat-ui` is a real directory (`drwxrwx---`), never a symlink.
- `/tmp/fakehome` in the tree: **0** hits. (`/tmp/` appears only in pre-existing build-log/output paths in agent/skill docs, e.g. `ecc-gan-evaluator.md` tee paths and `mobile-ship` build logs — unrelated to the fake HOME.)
- Global less-flat-ui source pristine: md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines — verified unchanged. Fake HOME is `fix33/fakehome33` on real disk (its less-flat-ui copy is a real directory), not `/tmp`.
- `/tmp` is 62% full (318M/512M) and now holds 9 `fix33guard33*` dirs (~60–68K each) — verifier 16g import-guard litter, one per verifier run (worker runs + audits + this sweep's re-run). Trivial size, no build risk, but the check still does not clean up after itself (audit #109-A observation, unchanged).

### 2.8 Fix-round verification — the six #109 minors are fixed

Spot-checked each, independently:

| Finding | Fix verified |
|---|---|
| A-M1 + B-M4 (stale build.sh counts) | SPEC §1(b) line 44 now reads "48 ID + 6 PROSE occurrences (45 lines) + 1 XID", measured post-fix33, with the full ± reconciliation; implementation report §2(d) likewise corrected. Re-measured build.sh this sweep: ID 48 / PROSE 6 / XID 1 — agrees. |
| A-M2 (stale fast count in build.sh comment) | build.sh:24145–24148 now reads "(71 pre-state, 72 post-state — +1 in the agent.schema.json description, D33-17)". Comment only; census re-checked unchanged (ID 48 / PROSE 6 / XID 1). |
| B-M1 (direct-command guardrail gap) | Recorded as OWED-33-4 in SPEC §6 (line 222) and MANIFEST OWED section (line 172) — not fixed by scope expansion, by deliberate design. See observation O-1. |
| B-M2 (r5 not re-runnable in place) | MANIFEST Verification section lines 131–137 note the exact requirement (needs `fix32.py` + `fix32-patch-log.md` adjacent). Re-verified this sweep: r5 passes 100/100 only with siblings alongside (see §3). |
| B-M3 (stale DECISION-33-5 string) | fix33.py:449 (both copies, md5-identical) now reads "hackathon-mode L42 carries no pointer (D33-19 …)". Zero "carries the pointer" in any live file. MANIFEST notes the run-5/run-6 patch-log copies carry the stale wording as a historical record (md5 `ddef5b7aa229ceff138d3cf3e450960c`, both copies identical) — deliberately not rewritten. |
| Canonical fix31.py investigation | MANIFEST "What changed" fix31.py bullet records the investigation outcome (canonical edit mirrors a legitimate scratch-repo change; left as-is; builds never run from the canonical tree). |

The canonical fix31.py story holds: scratch-repo change vs HEAD is only the `EXPECT_PIN` census update (verified hunk by hunk, §2.5). Diff stat is now **33 files, +136/−109** — the +1 is the fix-33b build.sh comment reflow only (see S-M1 for the two docs that still say +135).

## 3. Independent re-runs (this sweep)

| Check | Command | Result |
|---|---|---|
| Verifier | `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` | **526/526, exit 0** (reproduced, not read from run3) |
| Scan r4 | `python3 scan32-r4-test-fix33.py` (from `fix33/`) | **ALL PASS, 76 checks, exit 0** (re-runs in place) |
| Scan r5 | copy + `fix32.py` + `fix32-patch-log.md` alongside in `/tmp/sweep53-r5` (deleted after) | **ALL PASS, 100 checks, exit 0** |
| Build logs | run 5 + run 6 tails | **BUILD EXIT: 0** both |

## 4. Observations (not findings)

- **O-1 — D-2 / OWED-33-4 confirmed, already owed.** Direct `/gan-build`, `/gan-design`, `/astra-review`, and `/orch-*` invocations carry no MODEL check and no Auto ask: `grep -rln 'MODELSEL_F33|MODEL check'` over `commands/` + all `skills/orch-*/` returns nothing, and `gan-build.md`/`gan-design.md`/`astra-review.md` each score 0 for `MODELSEL_F33|MODEL check`. `/gan-build` Phase 1 step 0 is its own cold-start direction check (reads the decision record, launches `gan-planner`); it never invokes the orchestrate skill or reaches orchestrate step 0. This is the recorded OWED-33-4 (deliberate orchestrate-only design, D33-19; not a regression — the pre-fix33 MODEL-PIN check was also orchestrate-only; no false identity is asserted on those paths). Dry-run #50 confirmed the same bypass as D-2. No new finding; the owed item stands as recorded.
- **O-2 — Verifier `/tmp` litter grows with every re-run.** 9 `fix33guard33*` dirs now sit in `/tmp` (audit #109-A noted 4). ~60–68K each, ~600K total on a 512M tmpfs at 62% — trivial, but the 16g check should clean up after itself.
- **O-3 — r5 is still not self-contained.** It passes 100/100 only with `fix32.py` + `fix32-patch-log.md` copied alongside (B-M2, documented in the MANIFEST but not fixed — the script was deliberately not rewritten). A future re-run from `fix33/` alone still crashes with `FileNotFoundError`.
- **O-4 — OWED-33-1 / OWED-33-2 / OWED-33-3 stand.** `model: inherit` is doc-verified, not live-verified (live test owed to Anish); `FACTORY_CURSOR_PLAN.md` still pins the orchestrator (factory round 4); no cost-accounting text in the regular tree (adjudicated sufficient, MODEL check records the actual model and marks cost unknown).
- **O-5 — Parallel legs agree with this sweep.** Re-audit #110 (NOT PASS, sole finding 110-M1) matches S-M1 exactly; dry-run #50 (NOT PASS, D-1/D-2) matches S-M2 and O-1. No parallel-leg finding was contradicted by this sweep, and no sweep finding contradicts them.

## 5. What remains owed (not this sweep's defects)

- **S-M1 fix:** two one-character edits (`+135` → `+136` in MANIFEST.md:60 and fix33-implementation-report.md:200). No rebuild, no re-verification beyond re-reading the stat.
- **S-M2 decision:** coordinator decides whether D33-5/L14 wording is qualified ("before scoping, design, or dispatch — step 0, after grill-me") or the tree is re-sequenced (ask before grill-me).
- **OWED-33-1:** live test (Anish's run in Cursor, updated prompt).
- **OWED-33-2:** factory plan doc unpin (factory round 4).
- **OWED-33-3:** cost accounting (new feature if ever wanted).
- **OWED-33-4:** direct-command Auto ask (future round if ever wanted).
- Commit leg: commit the 33 tracked files from `fix33/scratch-repo` (+136/−109), leaving untracked `fix32/` and `fix33/` in place. No bundle/push in this fix.

## 6. Commands / results (exact)

- `cd fix33/scratch-repo && git rev-parse HEAD` → `dd106ade5f6043ec4ed613919e7908172d8eadce`; `git diff --stat HEAD` → `33 files changed, 136 insertions(+), 109 deletions(-)`; `git status --short` → 33 modified + untracked `fix32/`, `fix33/` only (unchanged after this sweep)
- Built census: `grep -rho` → ID 0, PROSE 2 (strategic-compact :68/:102), XID 0, XPROSE 0, fast 72, bare fast 0; `Extra High` 0; `MODEL-PIN` 0
- Staged live census: only `LIVE_SMOKE_TEST.md:132` keep; repo-wide outside built/fix/build/factory/smoke: 0 hits
- Agent `model:` inventory: built 41 fast + 4 inherit (45/45 with a line); staged 1 inherit + 2 fast (3/3)
- build.sh: ID 48 / PROSE 6 / XID 1; opus `"opus": "inherit"`; no `fix30/fix30.py` invocation; `awk 'NR>24151 && /grok-4.7-high|Grok 4.7 High|extra-high/'` → empty; STEP 5 anchors 6× `model: inherit`
- `MODELSEL_F33`: 2× orchestrate staged + built (L14 + L62); 0× hackathon-mode; 0× commands/ + orch-* skills (D-2 check)
- Trigger manifest: 48 keys, coverage skills 72 / withTriggers 48; `ui-ux-pro-max` absent, `skill:design-taste-frontend` present
- `verify33.py` → 526/526 exit 0; r4 → 76 PASS ALL PASS; r5 (with siblings) → 100 PASS ALL PASS
- less-flat-ui global md5 `cef0249fbf37ba096c688ce78fa4377f`, 534 lines; built + fake-HOME copies real directories; `/tmp/fakehome` in tree 0
- `__pycache__`: only the 4 known fix31 dry-run dirs; symlinks: only tracked `node_modules/.bin/js-yaml`, unchanged vs HEAD
- Live-test prompt md5 `cd679e5e7ecd5f5ace654294ada24b47` (canonical = scratch); fix33.py copies md5 `1533f4e8f56f3ab9a200f6a4d894014a`; patch logs md5 `ddef5b7aa229ceff138d3cf3e450960c`
- S-M1: `grep -rn '+135'` → MANIFEST.md:60, fix33-implementation-report.md:200 (living docs); all other hits are correct historical statements
- S-M2: hackathon-mode L12 "run `grill-me` FIRST"; orchestrate L62 "immediately after grill-me"; HEAD L62 identical sequencing with the old MODEL-PIN check
