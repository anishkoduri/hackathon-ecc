# Audit #82-B — Fix #29 (brief / verify coherence + verifier, round 3)

- **Date:** Mon Nov 16, 2026
- **Auditor scope (Auditor B):** verify every audit #81-B finding (81-B1–81-B8) against the built tree; hunt for new brief/verify gaps with fresh eyes; audit the verifier (`fix29/verify29.py`, re-run independently); harness honesty (B13 rejection re-check). Read-only; no file under `~/workspace/hackathon-plugin/` was edited except this report.
- **Sources read in full:** `fix29/SPEC.md`, `fix29/MANIFEST.md`, `fix29/audit80-report-A.md`, `fix29/audit80-report-B.md`, `fix29/audit81-report-A.md`, `fix29/audit81-report-B.md`, `fix29/verify29.py` (§7c/7d/7e, §10i gan checks), the built routing text in `skills/orchestrate/SKILL.md` (GLOBAL-ROUTING block :36, step 4 :93, contract core :227, escalation ladder :250–252, Verification stage :270–286), `skills/orchestrate/references/dispatch-prompt.md` (whole file), `commands/gan-build.md` (whole file), `skills/gan-style-harness/SKILL.md` (:14, :69, :153–155), `agents/deep-reasoner.md`, `agents/fast-worker.md`, `agents/scout.md`, `fix16/fix16.py` (`sub()` :51–60, hackathon-mode anchor :3807–3809, `main()` exit :4274–4280), `build.sh` (:23222 fix16 run).
- **Verifier re-run by this auditor:** `python3 fix29/verify29.py` → **255/255, exit 0** (confirmed independently, not taken from the coordinator's log).

## Verdict: NOT PASS — 0 blocking, 2 minor

All eight #81-B findings are verified fixed in substance, with exact file:line evidence below — including both blocking items: the deep-reasoner role file is rewritten to NEEDS_CONTEXT + bound + tie-breaker with the unbounded phrase at 0× tree-wide (81-B1), and the GAN loop that actually runs now has the ORCHESTRATOR-CHECK step, the planner-spec check, and the CHECK SCORE gate wired into its pseudocode, mirrored in the skill's loop wiring (81-B2). The verifier's new checks were false-pass-hunted individually and hold, with one genuine weakness (82-B2: the GAN wiring checks assert presence, not order — the step could move after CHECK SCORE and still pass). The one remaining live brief gap is the GAN generator launch block, still below 7/7 as a standalone brief (82-B1) — the 81-B2 fix wired the loop but never touched the launch block's own fields.

---

## #81-B disposition — every finding re-checked

| #81-B | Status | Evidence |
|---|---|---|
| 81-B1 (blocking): deep-reasoner assume-and-proceed | **VERIFIED-FIXED** | `agents/deep-reasoner.md:17` rewritten: "If the task is under-specified, return NEEDS_CONTEXT naming exactly what is missing — do not guess. (Bounded by NO-GUESSING_F29: 'state the assumption and proceed' applies only to carrying out the briefed approach, never to a decision the brief leaves unspecified — … returned to the orchestrator as a question, not guessed. When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall.)" Exact phrase `"state the assumption you made and proceed"`: **0× tree-wide** (whole-tree grep, this auditor). The staged source `new-skills/orchestrate/agents/deep-reasoner.md` carries the identical line (diff of the `_F29` lines: identical). No other `agents/` role file carries unbounded assume/proceed language (see fresh hunt below). |
| 81-B2 (blocking): GAN loop terminates on rubric score | **VERIFIED-FIXED** | `commands/gan-build.md`: `# ORCHESTRATOR-CHECK` step sits between `# EVALUATE` and `# CHECK SCORE` (:61): orchestrator checks generator output against the brief's acceptance criteria and re-checks the evaluator's pass/fail call; rubric pass + failed criterion = fail → generator re-dispatched with a correction brief naming the failed criterion, consuming one iteration within `max_iterations`, skipping CHECK SCORE; a rubric fail the orchestrator finds actually passes = re-check, not loop exit. `# CHECK SCORE — runs only after the orchestrator check above passes` (gate note present). Planner-spec check `3a.` at end of Phase 1 (:30, incl. the `--skip-planner` path against the existing spec) with the same correction-brief failure path to the planner, capped at one correction re-dispatch, then stop-and-report. Mirror in the skill: Architecture note `gan-style-harness/SKILL.md:69` ("**Orchestrator check (fix #29, VERIFY-MERGE_F29):** the orchestrator sits outside the loop …") + Scoring bullet `:155`. The wiring produces a genuine orchestrator-against-acceptance-criteria verdict with a correction-brief trigger — not paragraph text alone. Residual: the verifier asserts the step's presence, not its position (82-B2). |
| 81-B3 (minor): orchestrate step 5 constructs no correction brief; manifest inheritance claim unsupported | **VERIFIED-FIXED** | `skills/orchestrate/SKILL.md:252` (escalation ladder step 1): "The re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief (fix #29, VERIFY-MERGE_F29)." `"correction brief"` occurs in orchestrate SKILL.md exactly 2× (:36 GLOBAL-ROUTING block + :252 ladder) — the ladder construction is the only one outside the block, matching verify29's `count == 1` assertion on the construction sentence. `"Phase 5 Review"` is 0× in orchestrate SKILL.md, and MANIFEST §2(c)(7) now correctly claims inheritance only for orch-build-mvp step 6. |
| 81-B4 (minor): carve-out drone-side sites lack scope sentence; actor contradiction | **VERIFIED-FIXED** | All four drone-side sites now open with the scope sentence — `dispatch-prompt.md:96` (mechanical preamble), `:117` ("Before you begin"), `:212` and `:236` (worked example ×2): "for carrying out the briefed approach only, state the assumption — the safe/reversible option — and proceed instead of asking the USER; a decision the brief leaves unspecified still returns NEEDS_CONTEXT to the orchestrator, which resolves it by stated assumption." (`_dp.count("for carrying out the briefed approach only, state the assumption") == 4`, verified by this auditor's grep.) Governing status-vocabulary carve-out (`:51–55`) reconciles the actor: "The drone states assumptions only for execution detail; for an unspecified decision the orchestrator states the assumption." The reasoning template's "the assumption-and-proceed is the orchestrator's, not the drone's" (:144–147) now reads consistently with that reconciliation — it governs the unspecified-decision case, while the drone states assumptions only for execution detail. |
| 81-B5 (minor): tie-breaker never reached the carve-out texts | **VERIFIED-FIXED** | Governing status-vocabulary carve-out (`dispatch-prompt.md:51–55`) now carries: "When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall." Verify29 asserts it in the carve-out slice (`_fb_carve`). |
| 81-B6 (minor): worked example lacks Verification steps; count check blind | **VERIFIED-FIXED** | Worked example (`dispatch-prompt.md:210–221`) now carries `Verification steps:` (re-run the acceptance check; `grep -rn "src/auth/session.go" .` must return nothing; confirm the five functions import from `src/session`) and a `files out of scope:` label in Constraints (`src/auth/tokens.go, src/auth/store.go`). Verify29 7d now asserts per-template presence (6 sections × 2 fields) instead of bare counts. |
| 81-B7 (minor): blind-reviewer exemption has no verification procedure | **VERIFIED-FIXED (option (a))** | Blind-reviewer template now carries `Verification steps:` ("The orchestrator re-reads each cited `path:line` and confirms the defect reproduces or the property was checked; a finding that does not reproduce is dropped, not fixed.") and a `files out of scope:` slot in Constraints. Skeleton sentence (:15) updated: the blind-reviewer contract is "verification gate — with Verification steps and files-out-of-scope slots". The procedure is real: it states who verifies (the orchestrator), what (each cited `path:line`), and the consequence of non-reproduction (dropped, not fixed). The second-pass exemption still holds with its new NEEDS_CONTEXT line (`dispatch-prompt.md:160`: "If the task body leaves a decision unspecified, return `NEEDS_CONTEXT` naming it — do not guess.") — the asymmetry 81-A5 named is closed: both passes on the verbatim-identical task body now return NEEDS_CONTEXT when under-specified, so the disagreement-stop rule can no longer fire on a missing-input signal. |
| 81-B8 (minor, verifier): 7d/7c file-scoped or count-based; 7e order-insensitive | **VERIFIED-FIXED** | 7c Belief grep widened to `skills rules commands agents` with no `--include` filter (`verify29.py:641–650`, count == 5). Carve-out-order assertion added (see false-pass hunt below — distances 28–142 chars, all genuinely bound). 7d phrase assertion replaced by tree-wide 0× + known-bounded-sites file-set assertion (exact 6-file list — verified by this auditor's independent grep). 7d counts replaced by per-template presence (6 sections). 7e order-sensitive (unsorted list comparison) + deep-reasoner pair (7 staged files — verified complete: exactly 7 staged files carry `_F29`, all in the list). |

---

## New findings

### 82-B1 — MINOR — the GAN generator launch block is still below 7/7 as a standalone brief (81-B2 residual: the loop was wired, the launch block's own fields were not)

**Evidence.**

- `commands/gan-build.md` GENERATE block (:36–45): the generator's dispatch text names the spec + tokens file (files in), files out of scope (81-A7 fix), TDD + commit (constraints), and the spec as the work definition — but carries **no `Verification steps` slot** (what the generator itself runs to verify — the TDD tests are the procedure, but they are never labelled as the verification procedure and no step says "run X, paste output") and **no return-format slot** (what the generator returns — its output is implicit in commits and the files the evaluator then reads).
- The requirement exists in prose at three places: the command's own pointer (:12, "each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return)"), the skill paragraph (`gan-style-harness:14`, "Generator and evaluator briefs follow the seven-field contract"), and the GLOBAL-ROUTING block. None of them is instantiated in the launch block itself.
- Contrast the evaluator launch block in the same file, which is closer: it writes feedback to `feedback/feedback-{iteration}.md` (a return) and runs the live app + repo tests (a verification procedure), even though neither is labelled as a DIRECTOR-BRIEF field.

**Why it matters.** `/gan-build` is the executed path, and the GENERATE block is the only dispatch text the command itself gives the generator drone. A generator brief composed from the launch block alone is a 5/7 brief: it omits exactly the two fields DIRECTOR-BRIEF_F29 requires to be distinct slots, and the omission is invisible to the verifier — no check reads the launch block for fields (the 7d per-template checks cover `dispatch-prompt.md` only; the gan checks in §10i assert the paragraph, the mirror notes, and the loop wiring). Minor, not blocking: the orchestrator composes the brief from the spec under the skill's seven-field-contract reference, and the loop now verifies the output against the acceptance criteria, so the gap is a missing instantiation in the dispatch text, not a missing verification path.

**Fix.** Add two lines to the GENERATE block: a `Verification steps:` line (the exact checks the generator runs before finishing — the TDD tests it wrote, plus the acceptance criteria from the spec) and a `Return format:` line (status first, then files changed, test output, concerns — mirroring the mechanical template). Add a verify29 check asserting both lines in `commands/gan-build.md`.

### 82-B2 — MINOR (verifier) — the GAN wiring checks assert presence, not order: the ORCHESTRATOR-CHECK step could move after CHECK SCORE and still pass

**Evidence.**

- `verify29.py:1435–1441`: `check("commands/gan-build.md Phase 2 has the ORCHESTRATOR-CHECK step", _gb.count("# ORCHESTRATOR-CHECK") == 1)`, `check("... CHECK SCORE runs only after the orchestrator check", _gb.count("# CHECK SCORE — runs only after the orchestrator check above passes") == 1)`. Both are substring counts on the whole file — neither asserts the step sits *between* EVALUATE and CHECK SCORE.
- The live order is correct today (verified by reading `gan-build.md`: EVALUATE block, then `# ORCHESTRATOR-CHECK`, then `# CHECK SCORE`) — so this is a verifier weakness, not a live defect. But the order is the whole point of 81-B2: if a later edit moved the ORCHESTRATOR-CHECK block below CHECK SCORE, the loop would `Break` on a rubric pass before the check ever ran, re-introducing the exact 81-B2 failure mode, and verify29 would still pass 255/255.
- The planner-spec check is less exposed: its `3a.` label pins it between steps 3 and 4 of Phase 1 by numbering, so a move would break the numbering. The ORCHESTRATOR-CHECK step has no such positional anchor — it is a comment line inside the pseudocode.

**Why it matters.** 81-B8(iv) made the carve-out-order assertion precisely because order-insensitivity had already let a detached bound pass silently. The same lesson applies here: the property that matters is *where* the step executes in the loop, and the check asserts only *that* it exists.

**Fix.** In verify29, assert index order in `commands/gan-build.md`: `_gb.index("# EVALUATE") < _gb.index("# ORCHESTRATOR-CHECK") < _gb.index("# CHECK SCORE")`. (One line; no tree change needed.)

---

## Verifier false-pass hunt — the NEW checks, each tested

- **Per-template presence (7d, `verify29.py:780–800`).** Section boundaries genuinely isolate each template: skeleton (`## Skeleton` → `## Template — recon`), recon, mechanical, reasoning (`## Template — reasoning` → `## Template — second`), blind reviewer (`## Template — blind reviewer` → `## Worked example`), worked example (`## Worked example` → `## Common mistakes`). I read every section: each carries its own `Verification steps` and `files out of scope` inside its own fenced block — no field is borrowed from a neighboring section. The one boundary worth noting is the skeleton slice, which also sweeps in the status-vocabulary section (it sits between the two headers) — but that section contains neither field string, so the skeleton's pass comes from its own line 15, not from the carve-out text. **Holds.**
- **Tree-wide 0× phrase + known-bounded-sites file-set (7d).** Independent whole-tree grep for `"state the assumption"` returns exactly the 6 expected files (`agents/deep-reasoner.md`, `skills/orchestrate/SKILL.md`, `skills/orchestrate/references/dispatch-prompt.md`, `skills/polish-pass/SKILL.md`, `skills/polish-pass/reference/impeccable-critique.md`, `skills/systematic-debugging/SKILL.md`) — no missing file, no extra file. The expected set is exactly right. **Holds.** (Note: the file-set assertion is exact-equality by design — a future legitimate bounded site will fail it until the list is updated. That is the intended tripwire, not a defect.)
- **Carve-out-order assertion (7c, 600-char window).** Measured distances from each `"pick the reasonable option"` occurrence to the following `"applies only to carrying out the briefed approach"`: orch-pipeline 142, feature-expansion 142, orch-build-mvp 142, dispatch-prompt Belief line 142, dispatch-prompt preamble 111. All genuinely bound, well inside the window. One check artifact, not a defect: the `while` loop also matches the phrase *inside the carve-out's own quotation* ("'pick the reasonable option' applies only to…"), producing a second hit per file at distance 28 — a self-match that passes trivially. It does not weaken the check (the Belief-sentence hit is checked separately and passes on its own merit), but the loop is counting 10 substring hits for 5 grep lines. The 600-char window is generous against the observed 111–142 chars; given the single-line paragraph structure, a drift within the window would still be on the same line, so the practical binding is the line itself. **Holds.**
- **Order-sensitive 7e.** The unsorted comparison is correct and safe: `_F29` lines are copied verbatim by the build (no build transform reorders lines — the fix16 scrubs and agent-citation normalizations touch lines that contain no `_F29` token; the four `_F29` lines in built orchestrate SKILL.md are :36, :93, :227, :252, none of them among the transformed :100/:273/:280). The deep-reasoner pair is byte-identical staged-vs-built (diff of the `_F29` lines: identical). No false-fail risk from a build transform. **Holds.**
- **GAN rubric-pass count (`== 3`, `verify29.py:1361–1362`).** Counts within `_gan` (the skill file) only: exactly 3 — factory paragraph (:14), Architecture orchestrator-check note (:69), Scoring bullet (:155). All three sites exist and the count is right. **Holds.** Nit (not a finding): the MANIFEST's "the phrase now occurs 3×" is true of the skill file but not tree-wide — the phrase also occurs once in `commands/gan-build.md:61` (the ORCHESTRATOR-CHECK step), so tree-wide it is 4× in the built tree (plus the fix29.py patch strings). The check itself is scoped correctly; the manifest sentence needs the "in the skill" qualifier.

---

## Fresh hunt — new brief/verify gaps

- **Unbounded assume/proceed, whole tree:** `"state the assumption you made and proceed"` 0×; `"use your judgment"` / `"use your judgement"` 0× in `skills/` + `rules/` + `commands/` + `agents/` (and 0× whole-tree for "use your judgment" when combined with the "pick the reasonable option" sweep, which returned only the 5 bounded Belief copies). `"state the assumption"` 11 hits in 6 files — all in known bounded sites (see file-set above). No new unbounded language found.
- **`agents/` role files:** every `guess`/`assume` hit is a prohibition or an adversarial stance, not an instruction to guess: `ecc-harmonyos-app-resolver.md:146` "never guess", `ecc-network-troubleshooter.md:123` "Prefer evidence over guesses", `ecc-spec-miner.md:87,190,212` "never guess / never invent behavior", `fast-worker.md:16` "stop and return that — do not invent an answer", `scout.md:16,18` "no judgment calls / bounded honest map beats an unbounded guess", `ecc-code-reviewer.md:18` "assume every claim … is unproven" (adversarial review stance, not scope guessing). `deep-reasoner.md:17` is now bounded. Clean.
- **Every fix loop constructs a correction brief naming the failed criterion:** feature-expansion fix loop (`:158`), orch-pipeline Phase 5 Review (`:74`), orchestrate escalation ladder step 1 (`:252`), gan-build ORCHESTRATOR-CHECK (`:61`) + planner-spec check 3a (`:30`). orch-build-mvp step 6 inherits via Phase 5 Review (`orch-build-mvp:72` routes Verify through "orch-pipeline Phase 5 (Review)"). The only other re-dispatch sites in the routing set are NEEDS_CONTEXT re-dispatches (`orchestrate:250`, `dispatch-prompt.md:44` — supply the missing context, re-dispatch the same tier), which are not failure paths and correctly carry no correction brief. Orchestrate's visual loop (Verify step 5) routes failed work through the same escalation ladder, so it is covered by the ladder's construction sentence rather than needing its own. **All fix loops construct the brief.**
- **Orchestrator-level assumption language, re-checked:** `orchestrate:221` (hard rule — stated assumptions for trivial/reversible work, high-stakes irreversibles wait/escalate), `:290` (blind-parallel disagreement — orchestrator picks the safe/reversible option, recorded in the final report). Both remain orchestrator moves, not drone instructions. Clean.

---

## Field-coverage table — updated from #81-B

Legend: ● = present as a distinct field/slot · ◐ = required only by prose assertion, pointer, or reference · ○ = absent.

| Skill / brief | Goal | Files IN | Files OUT | Constraints | Acceptance criteria | Verification steps | What to return |
|---|---|---|---|---|---|---|---|
| orchestrate contract core (`SKILL.md:227`) | ● | ● (exact paths) | ● | ● | ● | ● | ● |
| dispatch-prompt recon / mechanical / reasoning templates | ● | ● | ● | ● | ● | ● | ● |
| dispatch-prompt worked example (:210–221) | ● | ● | ● | ● | ● | ● | ● — **now 7/7 (was 6/7)** |
| dispatch-prompt second-pass template (exempt, opinion) | ◐ (Task) | ○ | ○ | ● | ○ | ○ | ● (opinion format) — now carries a NEEDS_CONTEXT line |
| dispatch-prompt blind-reviewer template (exempt, verification gate) | ● | ● (acceptance criteria only) | ● | ● | ○ ("n/a — you are the check") | ● | ● — **now 6/7 formal; the acceptance-check slot is the gate itself by design** |
| hackathon-mode (rule; block :45) | ● (block states all 7) | ● | ● | ● | ● | ● | ● — requirement text only; a rule, not a format |
| orch-pipeline (:62) | ◐ paragraph + reference to dispatch-prompt contract | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-build-mvp (:13 pointer + :70 step 4) | ◐ via pointer; step-4 briefs use feature-expansion's format (● per that format) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-add-feature / orch-change-feature / orch-fix-defect (:13) | ◐ via pointer | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| orch-refine-code (:13 pointer; :35 step 2) | ◐ via pointer; step-2 sweep brief names all 7 inline ● | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) | ◐ / ● (step 2) |
| feature-expansion (format :143–152) | ● item 1 | ● item 2 | ● item 2 | ● item 3 | ● item 4a | ● item 4b | ● item 9 |
| gan-style-harness (:14) | ◐ paragraph + reference | ◐ | ◐ | ◐ | ◐ (rubric, not brief criteria) | ◐ | ◐ |
| gan generator brief (`commands/gan-build.md` GENERATE block) | ◐ (one-line brief) | ◐ (spec + tokens) | ● (out-of-scope line) | ◐ | ◐ (spec + rubric) | ○ | ○ — **still below 7/7 (82-B1)** |
| gan evaluator block (`commands/gan-build.md` EVALUATE) | ◐ | ◐ (rubric + spec) | ○ | ◐ | ◐ (rubric) | ◐ (runs live app + tests, unlabeled) | ◐ (writes feedback file, unlabeled) |
| design-taste-frontend redesign (`redesign.md:68`) | ● (paragraph enumeration) | ● | ● | ● | ● | ● | ● — paragraph list, not a fill-in template |
| common-agents.mdc (:26, covered by reference) | ◐ (factory line; defers to block) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |

Net vs round 2: **five formats now carry all 7 fields as distinct slots** (contract core, three dispatch-prompt implementation templates, feature-expansion format, worked example, redesign paragraph enumeration). Remaining below 7/7: the gan generator launch block (5/7 — 82-B1), the blind reviewer (6/7 formal, acceptance-check-by-design), the second-pass template (exempt, opinion-only), and everything carried only by paragraph assertion or reference.

---

## Harness honesty — B13 rejection re-checked and confirmed

The coordinator's rejection of the 80-B13 sync fix is **correct**, verified end to end by this auditor:

- `fix16/fix16.py:3807–3809` anchors on the staged wording: `sub(os.path.join(BASE, "rules/hackathon-mode.mdc"), "(its upstream \`claude -p\` invocation path does not run in Cursor", "(its upstream CLI-subprocess invocation path does not run in Cursor")` — default `count=1` (`sub()` def, `fix16.py:51–60`: on mismatch it appends to `ERRORS` and returns False).
- `fix16.py:4274–4280`: `main()` returns `1 if ERRORS else 0`, `sys.exit(main())` — a missed anchor fails the run.
- `build.sh:23222` runs `python3 "$PLUGIN_ROOT/fix16/fix16.py" "$PLUGIN_DIR"` on every build (last build step). Syncing staged `hackathon-mode.mdc:38` to the built text would make the anchor match 0× → `ERRORS` non-empty → exit 1 → build fails. (Manifest cites `:3807`; the `sub(` call is on line 3807 and the anchor string itself on line 3808 — the one-line citation nit from #81-B stands, substance unchanged.)
- Staged-vs-built drift confirmed by direct read in round 2 and unchanged since; the narrow replacement (check 7e) holds: exactly 7 staged files carry `_F29`, all 7 in the 7e list, none in `round2-skills/` or `rewritten-skills/`.

---

## Checked and clean

- **Verifier re-run:** 255/255, exit 0, re-run independently.
- **GLOBAL-ROUTING block:** byte-identical in `orchestrate:36` and `hackathon-mode:45`; all 7 `_F29` tokens in the block and in all 10 in-scope skills.
- **All five "pick the reasonable option" copies carved + tie-breaker** (whole-tree grep: exactly 5 lines — `orch-pipeline:72`, `feature-expansion:151`, `orch-build-mvp:70`, `dispatch-prompt.md:34`, `dispatch-prompt.md:92`).
- **"instead of NEEDS_CONTEXT": 0 hits** in the whole built tree. **"drop fields that are genuinely N/A": 0 hits** tree-wide.
- **"use your judgment" / "use judgement": 0 hits** in `skills/`, `rules/`, `commands/`, `agents/`.
- **`agents/fast-worker.md:16` and `agents/scout.md` are clean** — fast-worker says the opposite of guessing; scout says "a bounded honest map beats an unbounded guess".
- **Polish-pass / systematic-debugging carve-outs re-checked, no finding:** `polish-pass/SKILL.md:38,76,97`, `impeccable-critique.md:216`, `systematic-debugging/SKILL.md:93` govern the pass runner's own routing decisions in orchestrator context (or enumerate safe defaults), not drone brief instructions — same reading as #81-B, unchanged by the round-3 edits.
- **Correction briefs constructed in all four fix loops** (feature-expansion, orch-pipeline Phase 5, orchestrate ladder, gan ORCHESTRATOR-CHECK + planner-spec check) — see fresh hunt above.
- **Counts unchanged:** 67 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 triggers (verify29 checks 1–5 pass).
- **Model pins unchanged:** no `deepseek/` or `qwen/` slugs; `DeepSeek`/`Qwen` names only in the two GLOBAL-ROUTING blocks (verify29 9b passes).
- **Manifest §2(c)(7) correction verified:** inheritance claimed only for orch-build-mvp step 6; orchestrate's ladder constructs the brief itself.

## Grep counts (for the record)

- `"pick the reasonable option"` whole built tree: **5** lines (all carved + tie-breaker).
- `"state the assumption you made and proceed"`: **0** tree-wide.
- `"state the assumption"` whole built tree: **11** — `dispatch-prompt.md` ×4 (bounded first-build carve-outs), `orchestrate/SKILL.md:221` (orchestrator-level hard rule), `agents/deep-reasoner.md:17` (bounded), `polish-pass/SKILL.md` ×3 + `polish-pass/reference/impeccable-critique.md:216` + `systematic-debugging/SKILL.md:93` (pass-runner carve-outs).
- `"instead of NEEDS_CONTEXT"`: **0**.
- `"correction brief"` in `skills/` + `rules/` + `commands/`: **13** — GLOBAL-ROUTING block ×2 (`orchestrate:36`, `hackathon-mode:45`), routing paragraphs ×4 (`orch-pipeline:62`, `feature-expansion:139`, `gan:14`, `redesign.md:68`), fix-loop constructions ×7 (`feature-expansion:158`, `orch-pipeline:74`, `orchestrate:252`, `gan-style-harness:69` + `:155`, `gan-build.md:30` (3a) + `:61`).
- `"When in doubt"` (tie-breaker form): **7** sites (5 Belief copies + preamble short form + governing first-build carve-out).
- `"Verification steps"` in `dispatch-prompt.md`: **6** (skeleton, recon, mechanical, reasoning, blind reviewer, worked example); `"files out of scope"`: **6** (same six sections).
- `"a rubric pass at or above 7.0 with a failed acceptance criterion is a fail"`: **3** in `gan-style-harness/SKILL.md` (:14, :69, :155); **4** in the built tree (+ `gan-build.md:61`).
- `"The evaluator pass IS the verify step for GAN work"`: **0** (old substitution gone).
- Staged files carrying `_F29`: **7**, all in verify29's 7e list.
