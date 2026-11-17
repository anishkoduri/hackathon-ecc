# Audit #95-A — Fix #30 (Grok 4.7 Extra High orchestrator pin), round 1

**Date:** Mon 2026-11-16
**Auditor scope (Auditor A):** pin-rename correctness + verifier + build-time design — independently recount the pins in the built tree; list every renamed file with per-file counts and reconcile against `fix30/fix30-patch-log.md`; independently re-run `verify30.py`; prove liveness of `fix30.py` / `verify30.py` by mutation on a disk mirror; check `fix30.py` == `fix30.py.template`, the GLOBAL-ROUTING block guard, and that no file outside the built tree was renamed; spot-check one anchor per script (fix16/24/29) for the build-time-only claim; challenge the prose judgment (OWED-30-5) and the SPEC conformance edits; check the live-test prompt.
**Sources read in full:** `fix30/SPEC.md`, `fix30/fix30.py` (303 lines), `fix30/fix30-patch-log.md`, `fix30/live-test-prompt.md`, `fix30/build-log-run1.txt` (fix30 section + tail), `fix30/verify30.py` (pin checks §9/§9b, 7e §1011–1060, patch-log check §13, header check list), `build.sh` hook block (:24122–24133) and STEP 5 Counts (:24135+).
**Method:** independent Python `str.count` counter over the whole built tree (UTF-8 files counted, 154 non-UTF-8 files byte-checked for pin text) AND `grep -r -a -n -i -E` (never `-I`, never without `-i`, per the audit #94 methodology lesson); per-file counts compared line-for-line against the patch log; `python3 fix30/verify30.py hackathon-ecc` re-run independently; liveness mutations on a disk mirror under `fix30/scratch-tmp/a95a/` (not `/tmp`); anchor strings read in `fix16/fix16.py`, `fix24/fix24.py`, `fix29/fix29.py` with their abort paths; counts by directory listing; GLOBAL-ROUTING block md5 in all five sources. Read-only on the real tree; no file under `~/workspace/hackathon-plugin/` was edited except this report. Build script not run. Scratch mirror removed after (see §4).

## Verdict: NOT PASS — 0 blocking, 2 minor

The rename itself is exactly right: the independent recount reproduces the census to the occurrence (extra-high x49, prose x22, fast-worker x70, old pin x0, bare fast x0), all 25 renamed files reconcile per-file against the patch log, the verifier re-runs at **318/318, exit 0**, and both liveness mutations fail exactly their intended check. The two minors are documentation-only: (F1) the by-design drift record states build.sh inline keeps the old pin at "50 occurrences" — the true count is 54 ID occurrences (56 including the fix30 hook's own 2 self-referential mentions) on 50 lines, and the record omits the 5 build.sh prose and 15 staged prose occurrences that also keep the old pin; (F2) SPEC.md:38 still lists a Carbon open item with no superseded marker although Carbon is OUT. Neither touches the tree. Per the fix #27 convention the fixes need a re-audit in round 2; this verdict is NOT MET as written until then.

## Findings

| # | Severity | Finding |
|---|---|---|
| 95-A1 | minor | **OWED-30-1 drift count is wrong as written (3 places).** `fix30.py` docstring, DECISION-30-1 and OWED-30-1 all say build.sh inline keeps `grok-4.7-high` at "50 occurrences". Actual: **54 ID occurrences** outside the fix30 hook block (56 including the hook's own 2 mentions at build.sh:24123/:24128), on **50 lines** — the "50" is the `grep -c` line count, not the occurrence count. The four double-occurrence lines are 22682, 22771, 22786, 23701 (2x each). The record also omits the **5 build.sh prose** occurrences ("Grok 4.7 High", lines 22203 x1, 22678 x1, 22682 x3) and the **15 staged prose** occurrences (new-skills/orchestrate 12, new-rules/hackathon-mode 3) that keep the old pin by design. The substantive claim (staged + build.sh keep the old pin because fix16/24/29 anchor on it) is true and proven (§3); only the exact counts as recorded are wrong/incomplete. Fix: correct the three records to 54 ID (+5 prose) for build.sh and 19+2 ID (+15 prose) for staged. Documentation-only; no tree change, no rebuild needed. |
| 95-A2 | minor | **SPEC.md:38 Carbon open item is stale.** "Carbon's standing vs Grok 4.7 High on Anish's actual work (unverified; the floor assumes Carbon clears it as a frontier model)" still sits under Open items with no superseded marker, while the Decision (§9) and Prerequisites (§17–20) sections are explicitly marked SUPERSEDED and the re-scope note says Carbon is OUT. The item is moot — Carbon will never be the brain — and reads as live work to a future reader. Fix: strike it or mark it superseded like the rest of the Carbon material. SPEC-doc-only. |

## §1 Independent recount (reconciles exactly with the patch log)

Python counter over `hackathon-ecc/` (all files except `node_modules`/`.git`; 154 non-UTF-8 files byte-checked, no pin text in any):

| Token | Independent count | Patch-log census/post |
|---|---|---|
| `grok-4.7-extra-high` | **49** | 49 |
| `grok-4.7-high` | **0** | 0 |
| `Grok 4.7 Extra High` | **22** | 22 |
| `Grok 4.7 High` | **0** | 0 |
| `cursor-grok-4.6-high-fast` | **70** | 70 (unchanged) |
| bare `grok-4.6-high-fast` | **0** | 0 |

Cross-check with `grep -r -a -n -i -E`: 49 lines carry an orchestrator pin/prose token (44 lines ID + 11 lines prose, 6 lines carrying both); `grep -r -a -n "grok-4.7-extra-high"` = 44 lines / 49 occurrences; `"Grok 4.7 Extra High"` = 11 lines / 22 occurrences; `"grok-4.7-high"` = 0; `"Grok 4.7 High"` = 0; `"cursor-grok-4.6-high-fast"` = 68 lines / 70 occurrences. The Python counter and grep agree on every total.

Per-file renamed counts (ID / prose) — all 25 reconcile with `fix30-patch-log.md`:

| File | ID | Prose |
|---|---|---|
| README.md | 1 | 3 |
| rules/common-agents.mdc | 1 | 0 |
| rules/common-performance.mdc | 2 | 0 |
| rules/hackathon-mode.mdc | 2 | 3 |
| skills/strategic-compact/SKILL.md | 0 | 2 |
| skills/gan-style-harness/SKILL.md | 3 | 0 |
| skills/orch-add-feature/SKILL.md | 1 | 0 |
| skills/orch-build-mvp/SKILL.md | 1 | 0 |
| skills/orch-change-feature/SKILL.md | 1 | 0 |
| skills/orch-fix-defect/SKILL.md | 1 | 0 |
| skills/orch-refine-code/SKILL.md | 1 | 0 |
| skills/orchestrate/SKILL.md | 15 | 12 |
| skills/orchestrate/references/agent-TEMPLATE.md | 1 | 0 |
| agents/deep-reasoner.md | 3 | 0 |
| agents/ecc-architect.md | 1 | 0 |
| agents/ecc-gan-planner.md | 2 | 0 |
| agents/ecc-healthcare-reviewer.md | 1 | 0 |
| agents/ecc-spec-miner.md | 1 | 0 |
| commands/astra-review.md | 3 | 1 |
| commands/gan-build.md | 2 | 0 |
| commands/gan-design.md | 3 | 0 |
| commands/model-route.md | 2 | 0 |
| schemas/agent.schema.json | 1 | 0 |
| manifests/pi-core.json | 0 | 1 |
| **Total** | **49** | **22** |

No other file in the built tree carries an orchestrator pin or prose token. The fast-worker pin appears in 40+ additional files at x1–x9 each (e.g. orchestrate x9, gan-style-harness x6, fast-worker/scout x3 each, most `agents/ecc-*.md` x1 each) — untouched by the rename, as designed; `fix30.py` replaces only `grok-4.7-high` → `grok-4.7-extra-high` then `"Grok 4.7 High"` → `"Grok 4.7 Extra High"`, in that order, and neither replacement can touch the fast-worker slug (no shared substring) or double-apply (the new strings contain neither old string).

## §2 Verifier (independently re-run: 318/318, exit 0)

- `python3 fix30/verify30.py hackathon-ecc` re-run by this auditor: **318/318 checks pass, exit 0**.
- 315 → 318 reconciliation: verify29's check 9 was a single presence check ("Grok pins present: grok-4.7-high and cursor-grok-4.6-high-fast occur"); verify30's check 9 is four exact-count checks (bare-fast x0, ID extra-high x49 + old x0, prose x22 + old x0, fast-worker x70) — +3. Check 13 is the patch-log check in both verifiers (fix29 log → fix30 log, 1 → 1, no net change). Net +3, as recorded.
- Check 9 code read in full (verify30.py:1089–1135): counts via `grep -ro` per token, `len(splitlines())` = occurrence count (one match per output line). The grep calls carry no `-I` (nothing is silently dropped) and are case-sensitive exact strings, which is correct here — `"grok-4.7-high"` is not a substring of `"grok-4.7-extra-high"` and `"Grok 4.7 High"` is not a substring of `"Grok 4.7 Extra High"`, so neither count leaks into the other. One robustness note, not a finding: the greps lack `-a`, but I tested `grep -ro` against a binary file containing the pin and it still prints the match; and the 154 non-UTF-8 files contain no pin text (byte-checked by fix30.py's census and by my counter), so no count on this tree depends on `-a`.
- Check 7e pin-normalization present and correct (verify30.py:1044–1052): built `_F29` lines are normalized with `.replace("grok-4.7-extra-high", "grok-4.7-high").replace("Grok 4.7 Extra High", "Grok 4.7 High")` before the staged-vs-built comparison, with the comment naming OWED-30-1 and the reason (orchestrate/SKILL.md:93 carries both `_F29` tokens and the pin — verified live: built :93 is the 7,956-char step-4 line carrying `GLOBAL-ROUTING_F29` and `grok-4.7-extra-high` / `Grok 4.7 Extra High`, while staged :93 carries the old pin). Only the pin is normalized — any other staged-vs-built difference still fails. The mirror baseline (§4) passing 7e at 318/318 proves the normalization works end to end.
- Check 13 (verify30.py:2144–2160) asserts the patch log exists with `## Errors (0)`, `grok-4.7-high x49`, `'Grok 4.7 High' x22`, `cursor-grok-4.6-high-fast x70`, `grok-4.7-extra-high x49` — all present in the real log.

## §3 Build-time design (claim (1) verified real, one anchor per script)

- **fix16** — `HIGH = "grok-4.7-high"` (fix16.py:30) is the replacement constant; the common-performance effort-controls sentence (fix16.py:375) is written in the new-sentence form and the else-branch appends an ERROR if neither the old nor the new sentence is found; `main()` returns 1 if ERRORS (fix16.py:4276) and the build exits on it. Anchor real, abort real.
- **fix24** — `_DESIGN_LEAD_OLD` (fix24.py:433) is the full design-lead sentence containing `(model \`grok-4.7-high\`)`; the anchor helper appends an ERROR on count mismatch (fix24.py:63) and the script ends `sys.exit(1)` on ERRORS (fix24.py:619). Anchor real, abort real. fix24.py:575 also anchors the picker note (`Grok 4.7 High` prose + `grok-4.7-high` slug) for the README/hackathon-mode rewrite.
- **fix29** — the :424 OLD anchor (fix29.py:424) is the astra-review fix-routing line containing `` `grok-4.7-high` `` (the NEW form at :425 appends the GLOBAL-ROUTING paragraph); anchor mismatch appends an ERROR (fix29.py:96), `sys.exit(1)` on ERRORS (fix29.py:463). Anchor real, abort real. fix29.py:370 carries the same pin in the gan-planner fallback anchor.
- Renaming the pin in staged sources or build.sh inline would therefore break at least one anchor in each of the three scripts and fail the build — the build-time-only design is necessary, not merely convenient, and the precedent (fix #16 did Claude → Grok at build time via fix16.py) is correctly cited.
- **No file outside the built tree was renamed:** staged sources still say the old pin — new-skills/ ID x19 (orchestrate 15, deep-reasoner 3, agent-TEMPLATE 1) + prose x12, new-rules/ ID x2 + prose x3; build.sh inline still says the old pin — ID x54 outside the fix30 hook block (x56 including the hook's own 2 self-referential mentions at :24123/:24128) + prose x5 (see F1 for the count correction); `fix30/scratch-repo/hackathon-ecc` (the coordinator's scratch copy of the fix29 tree) still reads ID x49 / extra-high x0 — the build wrote only the real tree.
- **build.sh hook placement and wording:** the fix30 block (build.sh:24122–24133) sits immediately after the fix29 invocation (:24121) and immediately before STEP 5 Counts (:24135+); the comment states the 49 ID + 22 prose census, the fast-worker-unchanged (70) and GLOBAL-ROUTING-untouched assertions, the build-time-only rationale (fix16/24/29 anchors, fix #16 precedent), and the fail-loudly behavior. All accurate. Nothing after fix30 writes pin text — STEP 5 only echoes counts (`skills:`, `agents:`, `rules:`, `commands:`, `hooks:`, `plugin.json:`, `marketplace.json:`, `build complete:`), matching the build-log tail (counts 67/45/48/55/15, `fix30: OK` before them).
- **`fix30.py` == `fix30.py.template`:** md5 `157f6c0912331e4111280834ae4478e1` for both.
- **GLOBAL-ROUTING guard:** fix30.py §4 re-asserts the block byte-identical in orchestrate + hackathon-mode and all 7 `_F29` tokens present; independently verified — the block is 2,285 bytes, stripped md5 `68206505a08f90474dc4931b0e5fb6bb` in built orchestrate, built hackathon-mode, staged orchestrate, staged hackathon-mode, and the golden `fix29/global-routing-block.txt` (same md5 as audit #94-A). The rename did not touch it.
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 triggers (directory listings + `hooks.json` hooks dict + `skill-triggers@1.json` triggers dict). **0 files** in `hackathon-ecc/` are newer than `fix30/build-log-run1.txt` — no tree change since build run 1.

## §4 Liveness (disk mirror, both mutations fail exactly as intended)

Mirror built on disk under `fix30/scratch-tmp/a95a/` (142 GB free; tree is 53 MB) — `cp -a` reported ownership-preservation warnings only; `diff -r -q` confirmed the copy byte-identical to the real tree. The mirror layout adds absolute symlinks for `new-skills`, `new-rules`, `fix29`, `fix28` (needed by verify30's `_PLUGIN_ROOT` reads) and a copy of the real patch log under `a95a/fix30/`.

**Methodology note (my own false baseline, recorded so the next round does not repeat it):** my first mirror baseline was 305/318 because the symlinks were relative (`../../../../fix29` resolves to `~/workspace/fix29` from `a95a/`, not the plugin root) — the 13 failures were exactly the 2 golden-block checks, the 7 7e checks, the call-map sidecar check, and the 3 fix28/fix29 patch-log checks, all layout artifacts. Absolute symlinks fixed it; baseline **318/318**. The real tree was never written by any mutation step.

| Mutation | Result |
|---|---|
| (a) Revert one built pin: `agents/ecc-architect.md` `grok-4.7-extra-high` → `grok-4.7-high` (x1) on the mirror, run verify30 | **317/318** — exactly one failure: "orchestrator pin is grok-4.7-extra-high x49 and old grok-4.7-high is 0". No other check moved. File restored from the real tree; mirror re-verified **318/318**. |
| (b) Delete one pin occurrence on a pre-rename mirror (`fix30/scratch-repo/hackathon-ecc` copy, census verified 49/22/70/0/0 before use): `agents/ecc-architect.md:4` `model: grok-4.7-high` → `model: REMOVED`, run `fix30.py` | **Exit 1**, exactly one error: "census: grok-4.7-high found 48x, expected 49x — tree drifted from the fix29 census; refusing to rename", "no files written". `diff -r` against the scratch-repo tree afterwards shows **only** the intentional `ecc-architect.md` edit — fix30.py wrote nothing. Its error log landed in `a95a/pre-del/fix30/`, not the real `fix30/` dir (real patch log untouched, still Errors 0, mtime Nov 17 02:58). |
| Control: `fix30.py` on a pristine pre-rename copy | **Exit 0, 27 changes**; the renamed tree differs from the real `hackathon-ecc/` in **zero file contents** (`diff -r -q` shows only 7 "Only in" script dirs — `scripts/lib/{agent-proximity,control-pane,eval-harness,plan-canvas,session-adapters,skill-improvement,worktree-lifecycle}` — present in the real tree but absent from the scratch-repo copy; all seven are pin-free in the real tree, 0 pin hits, so the gap is pre-existing in the scratch copy and irrelevant to the census). The rename is deterministic and reproduces the shipped tree exactly. |

After the mutations the mirror was verified byte-identical to the real tree (`diff -r -q` silent) and **removed** (`fix30/scratch-tmp/a95a/` no longer exists; `fix30/scratch-tmp/` holds only its pre-existing contents).

## §5 Prose judgment (OWED-30-5) — accepted, no finding

Both challenged lines were read in the built tree and the staged original:

- **strategic-compact/SKILL.md:68** — "e.g. 500k Grok 4.7 Extra High, or a new 1M-window model family". The 500k context window is a property of the Grok 4.7 base model, not of the High vs Extra High reasoning-effort tier; the example's operative point (a large-window model whose id lacks a `[1m]` marker) is unchanged by the rename. Keeping "High" here would have left a stale tier name in a live configuration example. Rename correct.
- **strategic-compact/SKILL.md:102** — "Cursor **2.1.233 removed the todo/task tools by default** on Grok 4.7 Extra High, Grok 4.6 High Fast, current models and newer". The note's operative claim (todo tools absent on the plugin's models; write the plan to a file before compacting) is preserved by the "and newer" clause, as DECISION-30-2 states — Extra High is the current tier and is named explicitly. The historical-version framing ("2.1.233 removed…") is slightly re-aimed at the current tier, but the instruction the reader must follow is identical either way. Rename correct; no carve-out needed.

The other 20 prose occurrences are direct references to the orchestrator tier (orchestrate x12, hackathon-mode x3, README x3, astra-review x1, pi-core x1) and unambiguously mean the current pin.

## §6 SPEC conformance + live-test prompt

- **Re-scope:** the SPEC's top note supersedes the Carbon decision; the new scope (pin change in the built tree only, 49 ID + 22 prose, verifier pin assertions, no drone routing, factory copy separate) matches what was built. The stale "585" whole-tree count is explicitly corrected in the SPEC to the fix29-tree recount.
- **Prerequisites superseded:** marked as such (§17); the $5 prepay / Google API key items are OUT, the OpenRouter drone setup is correctly placed in the factory copy, not #30. Verified.
- **"verify29.py" typo:** no such string exists in SPEC.md — §25 correctly says "the Grok-pin checks from verify29" and "add a `verify30.py`". Nothing to fix.
- **Carbon live-test paragraph:** the Verification section's live test correctly describes Extra High on both tasks. The one leftover is F2 (SPEC.md:38 open item, unmarked).
- **Live-test prompt** (`fix30/live-test-prompt.md`, 61 lines): one reasoning-heavy task (Task A — merge-order decision doc with failure modes and verification steps, no code yet) + one repo-scale coding task (Task B — in-memory task queue, 4 files + tests, run end to end), each followed by a report of which model ran the parent and each subagent; pass = Grok 4.7 Extra High ran the parent on both tasks, subagent models informational only (per-subagent selection is a known Cursor limitation). Matches the SPEC's pass criterion. Scratch project, model picker pre-selected, small by design to save pool tokens. Live test itself is still unrun (OWED-30-3) — Anish runs it in Cursor; not an audit finding.

## §7 Checked and clean

- `fix30.py` census, post-assertions, and guard all present and strict (exact counts, refuse-before-write on census drift, post-rename re-census, fast-worker-unchanged assertion, GLOBAL-ROUTING guard). The control run (§4) proves the census accepts the true pre-rename tree and the refusal path writes nothing.
- verify30 check 9b unchanged: no `deepseek-`/`qwen-` model slugs in the built tree; DeepSeek/Qwen names occur only in the GLOBAL-ROUTING block (one of each per block). The 154 non-UTF-8 files were byte-checked by fix30.py's census (no pin text) and independently by this auditor's counter.
- Build log run 1: exit 0, `fix30: 27 change(s)`, `fix30: 5 OWED item(s) recorded`, `fix30: OK`; the patch-log change list matches the run-1 log line-for-line (census line, 25 renamed files, post line, guard line).
- No scope creep in the tree: counts unchanged (67/45/48/55/15/49), no drone routing added (no `deepseek/`/`qwen/` slugs), no design-package / grill-me / alwaysApply change asserted by this audit's pin scope (the verifier's 318 checks, including the fix #27/#28/#29 regression checks, all pass).
- OWED-30-2 (DeepSeek/Qwen forward reference stays), OWED-30-3 (live test unrun), OWED-30-4 (call map not regenerated — the pin change adds no dispatch edges) are recorded and accurate; OWED-30-1 is accurate in substance but its counts need the F1 correction; OWED-30-5 is resolved by §5.
