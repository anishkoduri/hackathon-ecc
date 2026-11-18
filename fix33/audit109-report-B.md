# Audit #109-B — fix #33 (unpin the orchestrator): adversarial pin-scan + independent verification

**Auditor:** B (adversarial pin-scan + independent verification)
**Date:** Tue Nov 17, 2026
**Base:** `dd106ade` (fix #32 close) — confirmed via `git rev-parse HEAD` in `fix33/scratch-repo`: `dd106ade5f6043ec4ed613919e7908172d8eadce`
**Tree audited:** `~/workspace/hackathon-plugin/fix33/scratch-repo` (staged + built `hackathon-ecc/`). The canonical `~/workspace/hackathon-plugin/hackathon-ecc/` is the old fix #31 tree and was NOT audited as the fix33 tree, per the brief.
**Did not edit or commit anything.** All probes ran against `/tmp` copies (small files) or a real-disk probe dir under `fix33/` that has been deleted; the real tree was never modified (verified: `git status` unchanged after probing).

## Verdict: PASS

The verifier and both scan suites re-run green from scratch, the adversarial scan finds **no realized orchestrator-model pin** anywhere in the staged or built tree, the frontmatter inventory is complete (45/45 built agents + 3/3 staged agents carry a `model:` line; the 4 chat-model agents are `inherit`, the rest are the untouched fast pin), the Auto guardrail covers the primary cold-start path, and the build.sh rename is genuinely retired (no fix30 invocation; no `grok-4.7-high` occurrence after the fix33 invocation line). Four minor findings (B-M1–B-M4, all docs/reproducibility, none a tree defect) are listed below. None blocks.

## 1. Independent re-runs (from scratch)

| Check | Command | Result |
|---|---|---|
| verify33 | `cd fix33 && python3 verify33.py ~/workspace/hackathon-plugin/fix33/scratch-repo/hackathon-ecc` | **526/526, exit 0** (matches worker's run 3; my run log `/tmp/audit109B-verify33-run.txt`) |
| Scan r4 | `python3 scan32-r4-test-fix33.py` (from `fix33/`) | **ALL PASS, 76 checks, exit 0** |
| Scan r5 | `python3 scan32-r5-test-fix33.py` (from `fix33/`) | **Crashes, FileNotFoundError for `fix32.py`** — see B-M2. Re-run with `fix32.py` + `fix32-patch-log.md` copied alongside the script in `/tmp/audit109B/`: **ALL PASS, 100 checks, exit 0** |
| Build logs | `tail` of `build-log-run5.txt`, `build-log-run6.txt` | **BUILD EXIT: 0** both |

## 2. Adversarial pin-scan (independent, whole tree)

### 2a. Built-tree census (own `grep -o` counts, `scratch-repo/hackathon-ecc/`)

| Pattern | Count | Expected |
|---|---|---|
| `grok-4.7-high` (ID) | 0 | 0 |
| `Grok 4.7 High` (PROSE) | 2 | 2 (keeps only) |
| `grok-4.7-extra-high` (XID) | 0 | 0 |
| `Grok 4.7 Extra High` (XPROSE) | 0 | 0 |
| `cursor-grok-4.6-high-fast` (FAST) | 72 | 72 (71 + 1 schema description, D33-17) |
| bare `grok-4.6-high-fast` (python lookback check) | 0 | 0 |
| `grok-4.7` / `Grok 4.7` (any) | 0 / 2 | keeps only |
| `Extra High` | 0 | 0 |
| `GROK`, `grok_4`, `grok 4.7` (case/underscore variants) | 0 | 0 |

The 2 PROSE hits are both in `skills/strategic-compact/SKILL.md`, eyeballed:
- `:68` — "`500k Grok 4.7 High`" — context-window example for a real model, not orchestrator identity. KEEP justified.
- `:102` — "`Grok 4.7 High, Grok 4.6 High Fast, ...`" — factual list of models that lost todo/task tools in Cursor 2.1.233. KEEP justified.

Case-insensitive `grok` sweep over the whole built tree: every remaining hit eyeballed and benign — the 41 fast-tier `model:` lines, `Grok 4.6 High` prose (fast tier name, untouched by design), `ngrok` substrings, Grok brand/logo references in design assets (`design-taste-frontend` icons/cards/heroes/moment.js, "x.ai Grok Bot" reference recording). No other orchestrator-model statement exists.

Prose identity statements (`orchestrator runs on`, `orchestrator.*Grok`, `Brain: Grok`, `parent agent, Grok`, `the orchestrator is Grok`, `runs on Grok`): all hits in staged + built say "the model selected in this chat" (orchestrate L14/L31/L62/L93, hackathon-mode L42, README :69, LIVE_SMOKE_TEST :132/:134). **Zero** "Brain: Grok" / "parent agent, Grok" / "orchestrator is Grok" hits.

### 2b. Staged live sources census (`new-skills/`, `new-rules/`, `README.md`, `LIVE_SMOKE_TEST.md`, `round2-skills/`, `rewritten-skills/`)

Only one pin-text hit in the entire staged live scope: `LIVE_SMOKE_TEST.md:132` — "`Grok 4.7 Extra High is the default for this test`" — the documented keep (test baseline; the test selects Extra High explicitly). `round2-skills/` and `rewritten-skills/` contain no pin text. Repo-wide `Grok 4.7|grok-4.7` grep outside `hackathon-ecc/`, `fix*/`, `audit-scripts/`, `build.sh`, `FACTORY_CURSOR_PLAN.md`, `LIVE_SMOKE_TEST.md`: **zero** hits. `FACTORY_CURSOR_PLAN.md` keeps (ID x1, XID x2, XPROSE x2) match the documented factory-round-4 scope exactly.

### 2c. build.sh — rename retired, no re-pin path (read, not just grepped)

- `fix30/fix30.py` invocation: **gone**. Only comment mentions remain (L24129–24136, retirement record).
- `fix33/fix33.py` invoked at L24151, in fix30's old slot (after fix29, before fix31).
- Opus mapping (L160–181): `"opus": "inherit"` with comment "opus -> inherit (the model selected in this chat, fix #33)"; print line updated accordingly.
- `grok-4.7-high` in build.sh: **48 occurrences, all on lines ≤ 24139, none after the fix33 invocation (L24151)** — verified with `awk 'NR>24151 && /grok-4.7-high|Grok 4.7 High|extra-high/'` (empty). Spot-checked clusters: L4246/4296 (common-performance heredoc source), L7825/7832 (astra-review heredoc + `model: grok-4.7-high` frontmatter, STEP 5 anchor old-side per D33-15), L11592/11599/11615 (astra-review STEP 5 anchor, intentionally unchanged), L22208+ (fix16/24/29 PROC patch old-side anchors, e.g. PROC-P3 gan-planner), L23706, L24129/24139 (fix30-retirement + fix33 comment blocks). All are old-side anchors or heredoc sources that write pin text **before** fix33.py runs; fix33.py replaces exactly that text (census 25 ID + 5 PROSE) and the built census is 0. No code path after fix33 re-introduces a pin; fix31/fix32 censuses assert the post-unpin state and the build passed.
- `grok-4.7-extra-high` in build.sh: 1 occurrence (L24130, retirement comment only). `Grok 4.7 High` in build.sh: 6 (see B-M4).

## 3. `model: inherit` coverage — full frontmatter inventory

### Built tree `hackathon-ecc/agents/` — 45/45 files carry a `model:` line (line 4 in every file)

**`model: inherit` (4 — exactly as claimed):**
`deep-reasoner.md`, `ecc-architect.md`, `ecc-healthcare-reviewer.md`, `ecc-spec-miner.md`

**`model: cursor-grok-4.6-high-fast` (41 — fast tier, unchanged):**
`ecc-a11y-architect.md`, `ecc-agent-evaluator.md`, `ecc-build-error-resolver.md`, `ecc-chief-of-staff.md`, `ecc-code-architect.md`, `ecc-code-explorer.md`, `ecc-code-reviewer.md`, `ecc-code-simplifier.md`, `ecc-comment-analyzer.md`, `ecc-commit-reviewer.md`, `ecc-database-reviewer.md`, `ecc-doc-updater.md`, `ecc-docs-lookup.md`, `ecc-e2e-runner.md`, `ecc-fastapi-reviewer.md`, `ecc-gan-evaluator.md`, `ecc-gan-generator.md`, `ecc-gan-planner.md`, `ecc-harmonyos-app-resolver.md`, `ecc-homelab-architect.md`, `ecc-loop-operator.md`, `ecc-mle-reviewer.md`, `ecc-network-architect.md`, `ecc-network-config-reviewer.md`, `ecc-network-troubleshooter.md`, `ecc-performance-optimizer.md`, `ecc-pr-test-analyzer.md`, `ecc-python-reviewer.md`, `ecc-pytorch-build-resolver.md`, `ecc-rag-pipeline-reviewer.md`, `ecc-react-build-resolver.md`, `ecc-react-reviewer.md`, `ecc-refactor-cleaner.md`, `ecc-security-reviewer.md`, `ecc-seo-specialist.md`, `ecc-silent-failure-hunter.md`, `ecc-tdd-guide.md`, `ecc-type-design-analyzer.md`, `ecc-typescript-reviewer.md`, `fast-worker.md`, `scout.md`

No built agent file lacks a `model:` line; no built agent carries any other model value. A whole-tree `^model:` grep finds only these 45 files plus `skills/orchestrate/references/agent-TEMPLATE.md` (whose L4 is the `CHANGE-ME` template: "`inherit` for a chat-model role … or pin exactly one Grok model ID for a fixed tier … a role with no `model:` line … is not admitted to the roster").

Note: `agents/ecc-gan-planner.md` frontmatter is fast (`cursor-grok-4.6-high-fast`) while its prose (:3, :44) says the design-lead works "on the model selected in this chat" — this is as SPEC'd (§1(c): its `model:` is fast; the design-lead is invoked inline as the orchestrator, orchestrate L28), not a miss.

### Staged agents — 3/3 carry a `model:` line

`new-skills/orchestrate/agents/deep-reasoner.md:4` — `model: inherit`; `fast-worker.md:4` — `model: cursor-grok-4.6-high-fast`; `scout.md:4` — `model: cursor-grok-4.6-high-fast`. No other agent files exist under `new-skills/`.

### Other files naming the orchestrator's model

None besides the already-listed sites: orchestrate SKILL.md (L14/L24/L25/L28/L29/L31/L35/L62/L93/L135/L141/L183/L244/L405), hackathon-mode L42/L44, README :69, `commands/astra-review.md` (`Model: inherit`, :41), `commands/model-route.md` (merged chat-model line), `rules/common-agents.mdc:34`, `rules/common-performance.mdc:13/:30`, `schemas/agent.schema.json:35–36` (enum `["cursor-grok-4.6-high-fast", "inherit"]`, description naming `inherit` + fast tier), `skills/gan-style-harness/SKILL.md:83/:96/:113` (GAN_*_MODEL examples), `skills/orch-*/SKILL.md` design-role lines, `manifests/pi-core.json:333`, `commands/gan-build.md:26`, `commands/gan-design.md:14/:19`. All model-agnostic; all verified by direct read/grep.

## 4. Guardrail stress (MODELSEL_F33)

Read in full: orchestrate SKILL.md L14 (identity), L62 (MODEL check), L93 (picker note). `MODELSEL_F33` count is 2x in both staged and built orchestrate (L14 + L62), as asserted by fix33.py.

- **Auto selected:** covered in all three sites. L14: "if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding, and do not silently orchestrate on an unknown fallback (see the MODEL check in step 0)." L62 and L93 carry the same rule.
- **Model undetermined / cannot be determined:** covered in L14 and L62 ("or the model cannot be determined to be a specific model").
- **"Before proceeding" + forbids silent fallback:** yes, verbatim in L14 and L62 ("do not silently orchestrate on an unknown fallback"; L93: "the orchestrator asks the user to pick a specific model before proceeding").
- **hackathon-mode L42 pointer:** confirmed absent (0 matches for `MODEL check|MODELSEL|Auto` on L42 in both staged and built copies) — consistent with D33-19 (SPEC correction; no pointer was ever woven). This is a SPEC error the worker corrected, not a tree defect.
- **Cold-start paths:**
  - **hackathon-mode first build (primary entry point): COVERED.** The first-build sequence (hackathon-mode L12) is grill → narration-key prompt ("orchestrate sends it … orchestrate step 0") → scope → expansion → build (orchestrate drives). The MODEL check lives in orchestrate step 0 (L62), so the cold start enters the step that carries the check.
  - **dispatch-prompt:** not an entry point — it is a template the orchestrator uses; its model-tier calibration routes to named agents (fast-worker pinned explicitly, deep-reasoner via the routing table). No pin, no bypass of an orchestrator decision (the parent is already running).
  - **Direct commands (/gan-build, /gan-design, /astra-review, /orch-* pipelines): NO Auto ask fires** — only `skills/orchestrate/SKILL.md` contains `MODELSEL_F33` / "MODEL check" in the built tree. See B-M1.

## 5. Live-test prompt + MODEL check (cost)

- `fix30/live-test-prompt.md`: states explicitly "Before starting, select **Grok 4.7 Extra High** in the model picker — this is Anish's default, and the test's baseline: since fix #33 the orchestrator runs on whatever model is selected, so the test verifies the SELECTED model runs the parent." Pass = "the parent agent ran the model selected in the picker (Grok 4.7 Extra High for this test) on both Task A and Task B (the model indicator says so)"; fail includes falling back "to Grok 4.7 High, or to Auto". Canonical and scratch-repo copies are md5-identical (`cd679e5e7ecd5f5ace654294ada24b47`). Tasks A/B unchanged.
- MODEL check (orchestrate L62): records the actual model in the run ledger (`MODEL: <name>` — the actual selected model); "A model that cannot be verified is recorded as unverified, not assumed held; cost is marked unknown, never assumed to be Grok/pool." Reachable from the orchestrator flow via step 0 in the first-build sequence (see §4). No cost-accounting system exists in the regular tree (OWED-33-3, a finding, not a fix33 defect).

## 6. Drones + fast tier untouched

- `git diff dd106ade` (scratch-repo, 33 files, +135/−109): no changes to any `*openrouter*`, `*drone*`, or `*dispatch*` path; `git diff` for `fast-worker.md` / `scout.md` (built + staged) is empty.
- The GLOBAL-ROUTING block (hackathon-mode L45) is byte-identical to the fix32 text, including the drone assignment ("fix #30 assigns DeepSeek to reasoning-heavy work and Qwen to coding work"); `git diff dd106ade -- hackathon-ecc/rules/hackathon-mode.mdc` touches only the hierarchy line (L42) and DESIGNPKG-AUTO (L44). No `deepseek`/`qwen` model slugs appear in the built tree beyond that pre-existing assignment sentence and unrelated icon-credit entries.
- Fast count reconciles: 70 (fix30 tree) + 1 (staged weave, orchestrate L93 picker note) + 1 (schema description, D33-17) = 72.
- `fix31.py` / `fix32.py` `EXPECT_PIN = {OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}` verified in all four copies (canonical + scratch-repo, both scripts).

## 7. Scan-function probe (planted pin, /tmp copies only — real tree never touched)

- **Import guard:** importing a `/tmp` copy of fix33.py with junk argv leaves `BASE == ''` and `ROOT == ''` (D33-14 holds).
- **fix33.py census vs planted pins:** running it against a `/tmp` copy of the post-fix33 tree with a planted `model: grok-4.7-high` (ecc-architect) or a planted prose pin (`Grok 4.7 High` in orch-add-feature) exits 1 with census-drift errors. Note the census is a **pre-state exact-match gate** (it expects 25 ID / 7 PROSE / 71 fast), so it fails on the clean post-tree too (control run, exit 1) — it proves drift detection, not post-state pin detection. The post-state pin detection is verify33 §9/§16a, probed next.
- **verify33 vs planted pin (in-situ copy on real disk, correct PLUGIN_ROOT):** post-tree + one planted `grok-4.7-high` line → **524/526, exit 1**, failing exactly the two pin-census checks ("no orchestrator pin: grok-4.7-high x0 …" and "fix33 built census (16a)"). The scan genuinely flags a planted pin.
- **Negative control:** clean in-situ copy → **526/526, exit 0**. Model-agnostic lines do not flag.
- (Process note: full-tree copies do not fit /tmp — 512 MB tmpfs filled, `cp: No space left on device` — so the in-situ probes ran from a real-disk dir under `fix33/`, deleted afterwards. The earlier `/tmp` fix33.py import probes used only the single script file.)

## Findings

### B-M1 (minor) — Direct-command entry points bypass the Auto ask; guardrail is orchestrate-only

`/gan-build`, `/gan-design`, `/astra-review`, and the `/orch-*` pipelines (`orch-build-mvp`, `orch-add-feature`, `orch-fix-defect`, `orch-change-feature`, `orch-refine-code`) carry no MODEL check and no Auto ask — `MODELSEL_F33` appears nowhere in the built tree except `skills/orchestrate/SKILL.md`. If the user invokes one of these directly with the picker on Auto, the design-lead/deep-reasoner runs inline (or via `model: inherit`) with no prompt to pick a specific model. The primary cold start is covered (hackathon-mode first build enters orchestrate step 0), and this scope is identical to the pre-fix33 MODEL-PIN check, which was also orchestrate-only — so it is **not a regression introduced by fix33**, and no false identity is asserted on those paths (they all say "the model selected in this chat", which is true whatever Auto resolves to). It is also the SPEC's deliberate scope (D33-19, orchestrate-only home). Recorded as minor: the stated rule ("the orchestrator tells the user to pick a specific model before proceeding") is unconditional in wording while enforcement is orchestrate-only. Recommended follow-up: record as OWED — either add a one-line Auto pointer to the direct-command entry points or explicitly scope the guardrail to orchestrate runs. Not a fix33 defect; does not change the verdict.

### B-M2 (minor) — Repointed r5 suite is not re-runnable in place from `fix33/`

`scan32-r5-test-fix33.py` resolves `fix32.py` (line 849) and `fix32-patch-log.md` relative to its own directory (`os.path.dirname(os.path.abspath(__file__))`), but neither file exists in `fix33/` — running it there crashes with `FileNotFoundError` after 76 checks (my run) instead of completing. It passes 100/100 only when run with those two files copied alongside (verified in `/tmp/audit109B/`). The worker's run log shows ALL PASS, so the worker must have run it that way, but the deliverable as stored is not self-contained; a future re-run from `fix33/` alone fails. Verification artifact only, not a tree defect. (r4 re-runs in place, 76/76.)

### B-M3 (minor) — Stale DECISION-33-5 text in fix33.py and the patch logs

`fix33.py`'s DECISION-33-5 string still says "hackathon-mode L42 carries the pointer" — the exact claim D33-19 corrected as never woven (grep-confirmed absent, §4). The string appears once each in `fix33.py`, `fix33/fix33-patch-log.md`, and `scratch-repo/fix33/fix33-patch-log.md`. The SPEC was corrected; the script's decision text was not. Minor docs inaccuracy inside a log; the tree and the guardrail are correct. (DECISION-33-19 in the same file states the correction, so the log contradicts itself.)

### B-M4 (minor) — SPEC §1(b) build.sh pin counts are stale post-D33-15

SPEC §1(b) claims build.sh holds "56 ID + 5 PROSE occurrences (52 lines) + 1 XID". Measured now: ID x48, PROSE x6, XID x1. The direction of change is consistent with the documented edits (six STEP-5 anchor lines → `inherit` per D33-15, opus mapping dict + comment → `inherit`, fix33 comment block adds one PROSE mention at L24139), but the SPEC figure was never updated after those edits and the exact arithmetic does not reconcile to the unit. Functional conclusion unaffected (all 48 occurrences are pre-fix33-invocation old-side anchors; built census is 0). Minor docs staleness.

## Observations (not findings)

- **OWED-33-1 stands:** `model: inherit` is doc-verified (Cursor docs, Subagents), not live-verified; the updated live-test prompt is still owed Anish's run in Cursor. Nothing in this audit verifies runtime behavior.
- **OWED-33-2 stands:** `FACTORY_CURSOR_PLAN.md` still pins the orchestrator (ID x1, XID x2, XPROSE x2, verified) — factory round 4's job, out of this fix's scope.
- **fix33.py's census is a pre-state gate, not a post-state detector** (see §7): running fix33.py against the finished tree fails by design. That is the intended fail-loud behavior, not a defect; post-state detection is verify33's job and it works (524/526 on a planted pin).
- **Worker's numbers all reproduced independently:** verifier 526/526, r4 76/76, r5 100/100 (with siblings, B-M2), built census ID 0 / PROSE 2 / XID 0 / XPROSE 0 / fast 72 / bare 0, staged 0/0/0/1 keep, git status 33 files changed +135/−109, HEAD `dd106ade`, live-test prompt md5-identical across copies, `fix32/` + `fix33/` untracked in scratch-repo as documented.

## Commands run (exact)

- `cd fix33 && python3 verify33.py <scratch-repo>/hackathon-ecc` → 526/526 exit 0
- `python3 scan32-r4-test-fix33.py` → ALL PASS (76), exit 0; `python3 scan32-r5-test-fix33.py` → FileNotFoundError (B-M2); `/tmp` copy + `fix32.py` + `fix32-patch-log.md` alongside → ALL PASS (100), exit 0
- Built/staged census: `grep -ro` counts per pattern; python bare-fast lookback check → 0; case-insensitive `grok` sweep of built tree, all hits eyeballed
- `grep -rn '^model:'` across built + staged trees (full inventory, §3)
- `grep -n 'fix30/fix30.py' / 'fix33/fix33.py' / 'opus' / 'extra-high' build.sh`; `awk 'NR>24151 && /grok-4.7-high|Grok 4.7 High|extra-high/' build.sh` → empty
- `sed -n '42p'` hackathon-mode (staged + built) → 0 pointer matches; `grep -c MODELSEL_F33` orchestrate → 2 staged, 2 built
- `git diff dd106ade --stat` + per-path diffs (drones/fast/hackathon-mode)
- Probes: import guard (`BASE ''`/`ROOT ''`); fix33.py on `/tmp` tree copies with planted ID/prose pins → exit 1; verify33 on in-situ real-disk copies: planted pin → 524/526 exit 1 (exactly §9 + §16a fail), clean → 526/526 exit 0
- `md5sum` live-test prompt (canonical vs scratch) → identical; `grep EXPECT_PIN` in all four fix31/fix32 copies → `{OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72, NEW_ID: 0, NEW_PROSE: 0}`
