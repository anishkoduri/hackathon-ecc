# Sweep #14 — single-executor screen-verdict sweep

- **Date:** 2026-11-11 (Wed), ~15:44–16:10 CST
- **Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
- **build.sh:** 23,160 lines, md5 `6253677ce02c8625dadb41e1acf32e6b` (verified — matches the task handoff)
- **Built-tree manifest:** `39602dd2c80de00b60bb5852a68f1d69` in both `fix14/manifest1.txt` and `fix14/manifest2.txt` (diff 0; both builds exit 0)
- **Counts:** 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks (hooks.json: 15 entries), 57 MB
- **Mode:** READ-ONLY. Nothing in the plugin tree, `build.sh`, the repo, or the bundle was edited. No build executed. No pip pinning pass done.
- **Rule swept for (single-executor rule):** `browser-qa` ALONE issues pass/fail verdicts on rendered screens. Everything else is design guidance, candidate evidence, or static checks.

## Verdict: CLEAN

- **Blocking: 0**
- **Minor: 0**

No screen verdict fires outside `browser-qa`. Every verdict-like hit found was read in its file and confirmed to be correctly routed candidate evidence, a static/code-level check, craft guidance, a non-screen verdict (code review, tradeoff, inventory, test/loop gate), or the one legitimate issuer (`browser-qa` itself).

Prior-checker baseline for this build: Audit #51 ZERO ERRORS, dry-run #23 CLEAN, sweep #13j CLEAN (0/0). This sweep finds nothing new: the single fix14 change introduced no verdict language.

## Blocking findings

None.

## Minor findings

None.

## (a) Fix14 areas — verified

### Soft Shadow treatment #23 — `skills/less-flat-ui/SKILL.md:485–527`

- The full new section was read. It is pure craft guidance: CSS for `.soft-shadow` / `.soft-shadow-sm` / `.soft-shadow-lg` (three layered `box-shadow` values), advice on tinting the shadow colour to the surface, flipping to a faint light glow on dark surfaces, and stacking ("a shadow is a depth cue, not a pattern, so it stacks on top of any other treatment without competing"). The only verdict-shaped words are descriptive craft judgments: "One shadow alone reads flat; three at different blurs read as real depth", "a neutral black shadow on a warm page looks dirty", "a second one reads as a mistake". No ship/fix/rebuild/pass/fail verdict, no approve/reject, no first-word review value anywhere in the new text.
- All 8 fix14 substitutions verified present in the built file: frontmatter `23 textured treatments` (:3); source line `Source of the 23 treatments: … Soft Shadow is the new one from it` (:8); picker row `Premium, soft, wellness, beauty … grainy gradients, soft shadow` (:44); surface rows `Cards and panels` (:61), `Buttons and CTAs` (:62), `Modals and overlays` (:65); heading `## The 23 treatments` (:100); treatment `### 23. Soft shadow` (:485).
- No stale count anywhere: whole-tree grep for `22 treatments` (all files, excl. `node_modules`) returns **0 hits**, and `build.sh` also returns 0. The only surviving `22` is the quoted reel title in the source line itself — `"22 Backgrounds to Make Designs Less Flat (In under 30 seconds)"` (:8) — which fix14.py explicitly preserves as the reel's own title. Correct.
- `build.sh` W2-C1 patch anchor: `## The 23 treatments` appears exactly **2×**, at `build.sh:22069` and `build.sh:22072` (old + new of the same patch). No verdict language in either occurrence.
- Built-vs-source diff: the built file differs from `~/workspace/cursor-skills/less-flat-ui/SKILL.md` only by the pre-existing W2-C1 build patch (3 hunks: a wow-moment bullet at :32, the record-in-`docs/design-tokens.md` sentence at :74, the re-tint/purple-gradient paragraph at :101–102). The Soft Shadow section itself is identical in both. None of the patch hunks contains verdict language.
- Pre-existing verdict-shaped words elsewhere in the file, all read and classified as craft/static checks, not screen verdicts: `UI fix` as a build/change type (:14); `passes contrast (4.5:1 minimum)` (:20) and `text will fail contrast` (:413) — accessibility contrast checks; `ship the dithered file` (:262, Bayer-dither treatment) — "ship" as "output the processed file", not a screen verdict; `Do NOT use when:` / `Do NOT cases` (:22, :14) — treatment-applicability rules. None issues a pass/fail on a rendered screen.

## (b) Named areas — all verified clean

### browser-qa (the legitimate issuer) — `skills/browser-qa/SKILL.md:68, :105–106`

- `:68`: "this skill is the SOLE executor of the distinctiveness bar inside the visual loop … treat [candidate-evidence] entries as candidate evidence … never as a verdict … No other step judges screen distinctiveness".
- `:105–106`: `### Verdict: SHIP WITH FIXES (2 issues, 0 blockers)` and `# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline` — verified still just those lines. Whole-tree grep for `DO NOT SHIP` / `SHIP WITH FIXES` outside `browser-qa`: **0 hits**. `build.sh` contains 0 `DO NOT SHIP` occurrences (`browser-qa` is copied from source, not embedded as a patch string) — no second issuer hiding in the builder. Clean — this is the single executor the rule names.

### Review first words — `references/hallmark/references/review-hero.md:5`, `review-finish.md:5`, `gates.md:243–247`

- Hero: first line `findings` or `no-findings` — "a craft status, not a ship/fix verdict … template observations are candidate evidence for `browser-qa` and never drive it."
- Finish: first line `recapture` / `findings` / `no-findings` — "a craft status, not a ship/fix/rebuild verdict … template observations (`Seen before`, machine-made) are candidate evidence for `browser-qa` and never drive it."
- `gates.md:245`: "Act on its first word. `recapture` means the screenshots were wrong … Otherwise fix what is real … score each finding … `resolved`, `partial` or `unresolved`." Same craft-status vocabulary; the `resolved`/`partial`/`unresolved` scoring is per-finding recapture scoring, not a screen verdict.
- **Zero surviving ship/fix/rebuild first-word values tree-wide outside `browser-qa`**: the only `ship/fix/rebuild` hit in any `.md` file is `review-finish.md:5` itself, which explicitly denies it is one. The other first-line tokens in the tree are agent task-status tokens (`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED` in `skills/orchestrate/references/dispatch-prompt.md:39`, `agent-TEMPLATE.md:35`, `agents/deep-reasoner.md:18`, `agents/fast-worker.md:17`, `agents/scout.md:19`) — completion status of a delegated task, not a screen verdict.
- §6 ship rule (`gates.md:247`): "Nothing ships with an open `FAIL` or an open `REFLEX`" — the adjudicated §6 ship rule; not re-opened.

### Hallmark `gates.md` — `skills/design-taste-frontend/references/hallmark/references/gates.md`

- **§1 (lines 12–20):** Grades `FAIL` / `REFLEX` / `WAIVED` / `WARN` / `ANSWERED` / `NOTE` are static gate grades; Ledger (32) "never counts toward the verdict". Adjudicated static grading, not a screen verdict.
- **§3 (lines 38–40):** Pre-emit critique — "this critique is a design input, not a distinctiveness verdict"; Specificity under 3 is appended to `.hallmark/candidate-evidence.md` for `browser-qa`, "never a verdict on its own".
- **§5 judged clause (line 199):** gate 23 (footprint by eye) is a measure-then-route clause in the same family as the other judged clauses verified in sweep #13j (candidate evidence for `browser-qa` to weigh, never a template verdict). No new judged-clause wording appeared this round.

### sloplint scope guard — `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` / `sloplint-render.mjs`

- `sloplint.mjs:2` header: "Its FAIL/REFLEX/WARN grades are static-check grades, not pass/fail verdicts on rendered screens — screen distinctiveness is judged only by `browser-qa` in the visual loop."
- `sloplint.mjs:978–979`: `const verdict = guard ? guard(ctx) : true;` — a code-level guard-function return (whether a check's guard passes), not a screen verdict.
- `sloplint.mjs:2961`: "Gate 38iii is a static/code-level check on the source … its FAIL/REFLEX grade is not a pass/fail verdict on a rendered screen" (adjudicated).
- `sloplint-render.mjs:2` header: "Its FAIL/REFLEX/WARN grades are render-check grades, not pass/fail verdicts on rendered screens"; `:741–742`: "Template gates (80, 81, 82, 83, 85) never issue REFLEX verdicts here: they are candidate evidence for browser-qa, not a verdict." Clean.

### Taste hero bar + layout checks — `skills/design-taste-frontend/SKILL.md:53, :242, :283, :314`

- `:53`: "record that as candidate evidence for `browser-qa`, whose visual-loop verdict alone decides whether the hero passes the distinctiveness bar, even if every other check passes." Clean — text verified unchanged from sweep #13j.
- `:283`: "`check.mjs` finding fails the page on layout-correctness grounds … a layout finding is not a distinctiveness verdict — that is `browser-qa`'s alone."
- `:314`: hero review dispatch acts on first word `no-findings` / `findings` for craft findings only.
- `references/layout-v4.md:182, :294`: weak-hero observations are "candidate evidence … for `browser-qa` to weigh, not a fail verdict on its own"; `check.mjs` findings "fail the page on layout-correctness grounds, not as a distinctiveness verdict."
- `references/perf.md:10`: "WebGL off is a proxy, not a verdict."
- `references/redesign.md:40`: "Look at the screenshots before you weigh the findings, so the linter does not write the verdict". Clean.
- `references/hallmark-floor.md:63–67`: Specificity is candidate evidence, "never a distinctiveness verdict"; other five axes join the fix list as craft judgments. Clean.

### Layout-correctness checker scripts — `skills/design-taste-frontend/scripts/consistency.mjs`, `perf.mjs`, `photos.mjs`, `gate.mjs`

- `consistency.mjs` (28 hits): per-rule PASS/WARN/FAIL verdicts on rendered-page layout correctness — `flatVerdict` (empty ground / unmounted canvas at a width, :694, :1061–1079), rhythm height-change checks (`SR-2`, :2586–2597, :3269), test verdicts (`:1999–2001`, `:2095`, `:2338`, `:3125`, `:3258`, `:3332–3342`). Header (:2, :22–24): "the faults a reviewer marks by eye, found in a real browser … prints every finding as FAIL or WARN … FAIL: the builder must fix it (or report why it is false)." These are layout-correctness defects (off-grid, stagger, empty ground, section bleed, rhythm change), the same family as the `check.mjs` layout-correctness failure adjudicated in sweep #13j (`SKILL.md:283`, `layout-v4.md:294`) — a layout finding is not a distinctiveness/template verdict. Checked in context, not flagged. `:1347` ("Motion does not change the verdict") and `:1873` / `:3471` / `:10326` / `:11128` are the same per-rule verdicts referenced across checks.
- `perf.mjs` (10 hits): timing verdicts, explicitly capped at WARN (`:15`, `:241`, `:259`, `:433`); `:309` "not a verdict, and shader compile on a real GPU is not measured". Performance timings, not screen distinctiveness.
- `photos.mjs:945–947`: image-weight FAIL ("perf.mjs fails a page whose images pass N KiB") — a performance budget, not a screen verdict.
- `gate.mjs:789`: `// ---- the verdict` — the adjudicated Taste build-round gate printing open FAIL lines for layout checks; not re-opened.

### polish-pass family — `skills/polish-pass/SKILL.md`, `reference/polish.md`, `scoring.md`, `impeccable-critique.md`, `craft-floor.md`, `patterns/vibe-code-tells.md`, `capture.md`, `scripts/detect.mjs`

- `SKILL.md:22–24, :96`: harmony is a per-screen consistency check ("consistent / diverges, with the tokens cited"); "Harmony never verdicts screen distinctiveness" (per sweep #13j's verified wording, unchanged). `:93`: "Treat findings as evidence to verify, not verdicts."
- `polish.md:7, :24, :39, :51, :81–84`: generic-template finding "exists only on `browser-qa`'s visual-loop verdict"; harmony "does NOT judge whether a screen reads as a default template"; bans "absolute as static/code-level checks … never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone)"; report template: "Direction-application is `browser-qa`'s verdict, cited not judged" and "Generic-template findings (only on `browser-qa`'s visual-loop verdict)". Clean.
- `scoring.md:43, :54–56, :59`: Level placement is "an internal scoring anchor for polish's own Score, not a pass/fail verdict on a rendered screen"; persona-fit and tell-count caps apply "only on `browser-qa`'s visual-loop verdict". Clean.
- `impeccable-critique.md:56, :62, :142, :595, :601`: design specificity is "candidate evidence for `browser-qa`, not a verdict"; band table "36–40 | Excellent | Minor polish only; informs candidate evidence, never a ship verdict"; "The bands inform candidate evidence for `browser-qa`; only `browser-qa`'s verdict establishes a finding." Clean.
- `craft-floor.md:5, :111, :168` and `vibe-code-tells.md:3, :36`: bans/tells are "a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict"; template-pattern bans are done when appended to `.hallmark/candidate-evidence.md`, "fixed only on `browser-qa`'s verdict". Clean.
- `capture.md:29, :61`: "matters to the verdict" / "matters to the verdict" — screenshot-capture scoping (which cells to capture for the verdict `browser-qa` will render), not a verdict issued here. Clean.
- `detect.mjs:4`: "Findings are evidence to verify in context, not verdicts." Clean.

### ui-ux-pro-max carve-out + design-system — `skills/ui-ux-pro-max/SKILL.md:14, :87, :91`, `skills/design-system/SKILL.md:56`

- `:14` captivating bar and `:91` anti-generic bar: "design guidance, not a screen verdict … Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails". `:87` is the design-system definition step (hit is incidental wording, no verdict). Adjudicated carve-out holds.
- `design-system/SKILL.md:56`: "Scope — pattern evidence, not a distinctiveness verdict: the patterns below are code-level evidence … a slop finding … is candidate evidence for `browser-qa`, never a verdict". Clean.

### Orchestrate Verify steps 5–6 + re-verification — `skills/orchestrate/SKILL.md`, `skills/orch-build-mvp/SKILL.md`

- Every `verdict` hit in both files is `browser-qa`'s verdict, referenced, never issued: orchestrate `:60–61` (5b/5c: "did `browser-qa`'s fresh verdict pass? If no … the deploy of the redesign is HELD"), `:64`, `:66` (same named re-verification check before commit), `:193–195` (Verify step 5: "`browser-qa` is the SOLE executor of this bar inside the visual loop"; step 6 Hallmark audit), `:289` (end-of-project checks "pass/fail and findings count" — deferred code/security checks, not screen verdicts).
- `:8` (long line, read in full): council go/no-go or tradeoff verdicts are recorded in the stage ledger — "the verdict feeds your synthesis, it is not only a reply to the user" — a tradeoff verdict, not a screen verdict.
- `:174`, `:273`: "get back a checkable artifact, never a bare verdict" / "Demand a checkable artifact, not a verdict" — anti-bare-verdict discipline for delegations.
- `:189` (reviewer dispatch): "never an approve/reject verdict; a clean pass enumerates the properties … it checked." Clean.
- orch-build-mvp `:49, :53, :55–57`: step 6 whole-build verification (code-reviewer + `browser-qa` visual loop named by check), 6b final polish, steps 7–8 re-verification ("did `browser-qa`'s fresh verdict pass"), step 9 deferred end-of-project checks. Same routing as orchestrate. Clean.

### GAN harness / evaluator — `skills/gan-style-harness/SKILL.md` (no hits this round), `agents/ecc-gan-evaluator.md:65, :70, :96, :155`, `commands/gan-build.md:84`

- Evaluator `:65, :70, :96`: first impression and slop scoring are "code-level evidence only, never a screen-distinctiveness verdict"; screen distinctiveness "judged ONLY by `browser-qa` in the visual loop".
- Evaluator `:155` "Verdict: PASS / FAIL (threshold: 7.0)" and `gan-build.md:84` "Result: PASS/FAIL" are the GAN loop's **iteration gate** over rubric rows that exclude screen distinctiveness (score ≥ 7.0 stops iterating; the loop decides iteration, not shipping). Checked in context, not flagged — same disposition as sweep #13j.

### Rules-distill verdicts — `skills/rules-distill/SKILL.md:12, :69, :103–105, :121–124, :140–151, :175, :210, :217, :249, :259`

- Verdict vocabulary is `Append / Revise / New Section / New File / Already Covered / Too Specific` for rule-distillation candidates (`:121`, `:210`, `:217`, `:259` "Verdict: New Section in coding-style.md"). Inventory of rules text, not a rendered screen. Clean.

### Santa / learn-eval / stocktake / council / feature-expansion — code-review, tradeoff, inventory verdicts

- `commands/santa-loop.md` (13 hits) and `skills/santa-method/SKILL.md` (11 hits): the Santa verdict gate — two code reviewers return structured JSON `verdict: PASS | FAIL` per rubric criterion, mapped to NICE/NAUGHTY (`:50–65, :145, :159–184, :189–192`). Code review, not a rendered screen.
- `commands/learn-eval.md` (13 hits): holistic verdicts for learning drafts — `Save / Improve then Save / Absorb into [X] / Drop` (`:80–95, :109–113, :138–140, :145, :153`). Draft-quality verdicts, not screen verdicts.
- `skills/skill-stocktake/SKILL.md` (7 hits): inventory verdicts per skill — `Keep` / etc. (`:129, :167–169, :194, :200, :234, :246`). Skill-inventory verdicts.
- `skills/council/SKILL.md` (5 hits): tradeoff verdicts — "keep the raw positions visible before the verdict", "Present a compact verdict" (`:125, :127, :146, :171, :179`). Deliberation verdicts.
- `skills/feature-expansion/SKILL.md` (4 hits): per-feature verdicts (`:109, :119, :122` "approve vs. reject changes the product's direction", `:125`). Planner tradeoff verdicts.
- `skills/repo-scan/SKILL.md:132, :149`: "Four-level verdicts | Core Asset / Extract & Merge / Rebuild / Deprecate" — module-inventory verdicts. (The word `Rebuild` here is an inventory disposition for a code module, not a screen verdict.)
- `skills/config-gc/SKILL.md:103`: "Age is a signal, not a verdict". Clean.

### Verification loops and test gates — `skills/verification-loop/SKILL.md`, `skills/django-verification/SKILL.md`, `skills/springboot-verification/SKILL.md`, `commands/code-review.md`, `commands/checkpoint.md`, `skills/intent-driven-development/SKILL.md`

- `verification-loop/SKILL.md:3, :118–122`: six-phase verification report — Build/Types/Lint/Tests/Security `[PASS/FAIL]` rows. Test/build gates.
- `springboot-verification/SKILL.md:214–217`: same report shape (Build/Static/Tests/Security). `django-verification/SKILL.md:3`: frontmatter description of the same loop.
- `code-review.md:171`: "Record pass/fail for each" (project-type check command). `checkpoint.md:45`: "Build: [PASS/FAIL]".
- `intent-driven-development/SKILL.md:294, :333`: "Pass/Fail Examples" / "Pass/Fail Rubric" for intent checks. All non-screen gates.

### Click-path, pipeline, sanitizer, security, dependency, self-evaluation — non-screen verdicts

- `skills/click-path-audit/SKILL.md:88, :245`: "VERDICT: BUG — [description]" and "Verdict: Sequential Undo — final state contradicts button intent" — interaction-behavior findings (a button's final state contradicts its intent), not distinctiveness/template verdicts.
- `skills/opensource-pipeline/SKILL.md:116, :128, :145, :200`: `SANITIZATION_REPORT.md` "PASS/FAIL verdict"; "Gate on the section's Unreadable count, not on the verdict"; "Continue to Step 5 only when the verdict is PASS or PASS WITH WARNINGS". Sanitization gate.
- `agents/ecc-opensource-sanitizer.md` (9 hits): "Generates a PASS/FAIL/PASS-WITH-WARNINGS report"; `:336` "Verdict: PASS | FAIL | PASS WITH WARNINGS"; `:371` "The pipeline gate acts on this count, not on the verdict." Sanitization, not a screen.
- `skills/security-scan/SKILL.md:101`: "Auditor (Final Verdict)" — security synthesis.
- `skills/mcp-dependency-review/SKILL.md:61`: "it is not a complete security verdict" — dependency safety, explicitly not a verdict.
- `skills/agent-self-evaluation/SKILL.md:9` and `templates/evaluation-report.md:49`: "This is NOT a pass/fail gate"; "VERDICT: [Deliver as-is / Fix N issues then deliver / Redo from scratch]" — output-quality reflection.
- `agents/ecc-agent-evaluator.md:48, :105, :159, :213`: same deliver/fix/redo verdicts over evaluation axes. Output quality, not a screen.
- `skills/dev-team/SKILL.md:164, :193`: "use `council` if a specific tradeoff needs a verdict"; "Verdict with dissent" — tradeoff verdicts.

### Code-reviewer agents — `agents/ecc-code-reviewer.md`, `agents/ecc-bengali-reviewer.md`, `agents/ecc-vue-reviewer.md`, `agents/ecc-network-config-reviewer.md`, `agents/ecc-kotlin-reviewer.md`, `agents/ecc-healthcare-reviewer.md`, `agents/ecc-flutter-reviewer.md`, `agents/scout.md`

- All `APPROVE / WARNING / BLOCK` verdicts are code-review verdicts over findings (e.g. `ecc-code-reviewer.md:73, :290`; `ecc-bengali-reviewer.md:68, :178–194`; `ecc-vue-reviewer.md:193`; `ecc-network-config-reviewer.md:88`; `ecc-kotlin-reviewer.md:161`; `ecc-flutter-reviewer.md:243`). `ecc-healthcare-reviewer.md:83`: "Verdict: [SAFE TO DEPLOY / NEEDS FIXES / BLOCK — PATIENT SAFETY RISK]" — patient-safety code review, not a screen verdict.
- `agents/scout.md:16`: "Collect, don't judge … no root-cause verdicts." Clean.

### Astra review — `commands/astra-review.md`, `scripts/astra-review.js`, `scripts/lib/astra-review/prompt.js`, `scripts/lib/astra-review/codex.js`

- `astra-review.md:15–16, :68, :103`: "returns a structured verdict, never a patch"; "machine-readable verdict (PASS/FAIL, severity-tagged findings) that can gate a commit or push"; "ASTRA VERDICT: [PASS / FAIL (escalated)]". Code review gating a commit/push.
- `prompt.js` (16 hits): `VERDICTS = ['PASS', 'FAIL']`, verdict parsing/format (`:10, :27, :36, :59, :74, :86, :94, :128, :171, :183, :188, :205–207, :235`). `astra-review.js` (7 hits): runs the review, prints the JSON verdict, exit code by verdict. `codex.js:3`: "return the parsed structured verdict". All code-review plumbing, non-screen.

### Plan-canvas, agent-proximity, eval-harness, hooks — non-screen verdicts

- `scripts/lib/plan-canvas/ui.js` (13 hits) / `sessions.js` (7 hits) / `scripts/hooks/plan-canvas-pending.js` (2 hits): a **plan** verdict UI — the user clicks Approve / Request changes on a plan (`ui.js:287, :408–409, :509–510`; `sessions.js:16–17, :78–80, :268–269`; `plan-canvas-pending.js:187–188`). Plan approval, not a screen verdict.
- `scripts/lib/agent-proximity/index.js` (7 hits): `advise()` returns a `verdict` of agent-collision risk/distance/level (`:132–142`). Multi-agent proximity advisory.
- `scripts/hooks/gateguard-fact-force.js` (2 hits): code comments — "The boundary decided the verdict instead of the command position" (`:124`) and "the verdict has to depend on `dd` being the command" (`:1084`). Destructive-command hook guard logic.
- `skills/agent-self-evaluation/scripts/evaluate.py` (6 hits): "VERDICT: Deliver as-is / Fix N issues then deliver / Redo from scratch" (`:349–360`). Output quality.
- `skills/skill-comply/scripts/grader.py:138`: "Steps already graded, pass or fail." Skill-compliance grading.
- `scripts/lib/eval-harness/receipt.js:53`, `envelope.js:61`, `schemas/capsule-envelope.schema.json:71`: a `verdict` / `gate_verdict` field in eval-harness envelopes. Evaluation-harness plumbing.
- `hooks/` (the 15 hook files + `adapter.js` + `hooks.json`): **0 verdict/pass-fail hits** in any `.md`/`.js` grep — no verdict language in the hook layer at all (same as sweep #13j).

### approve / reject and rebuild — whole-tree vocabulary check

- Design-scope `approve|reject` grep (`design-taste-frontend`, `polish-pass`, `ui-ux-pro-max`, `browser-qa`, `orchestrate`, `orch-build-mvp`, `less-flat-ui`, `design-system`, `gan-style-harness`, `loop-design-check`, `verification-loop`): all hits are code/test/contract vocabulary — GPU shader words a laptop "rejects" (`assets/objects/*/README.md`), "Rejected: a small dialog centred on an empty ground" as a design-pattern exclusion (`effects-creative.md:90`), "Reject dumps" as return-contract discipline (`orchestrate/SKILL.md:114`), "no approve/reject" in the reviewer dispatch (`dispatch-prompt.md:189`), planner "approved expansions" / gate "auto-approves" (`orchestrate/SKILL.md:48, :56–57, :64`), "Reject only what can't be normalized" as form-validation guidance (`polish-pass/reference/patterns/forms.md:82`). No approve/reject verdict on a rendered screen.
- Whole-tree `rebuild` hits are build steps ("rebuild before every gate run", `gate.md:16`; `/demo --rebuild`, `orch-change-feature/SKILL.md:53`; "rebuilds before every gate run", `design-taste-frontend/SKILL.md:181`), asset-index rebuilds (`assets/effects/README.md:124, :129`), or copy-text ("We used to rebuild the rota", `sections-library.md:217`). No rebuild verdict on a screen.

### Other files checked

- `skills/frontend-design-direction/SKILL.md:27` (per sweep #13j): "reads as flat, generic, templated" appears only as a *when-to-use* trigger, not a verdict issued by the skill. Unchanged.
- `skills/loop-design-check/SKILL.md`: no verdict / pass-fail / ship / template hits at all. Clean.
- `commands/orchestrate.md`, `commands/orch-build-mvp.md`: no verdict / distinctiveness / template / pass-fail hits. Clean.
- `skills/verification-loop/SKILL.md`: test/build gates only (see above). Clean.

## (c) New verdict-like wording anywhere in the tree

None found. Whole-tree sweeps (excl. `node_modules`):

| Grep | Hits |
|---|---|
| `verdict\|pass/fail\|pass or fail` — `.md`/`.mjs`/`.py` (the sweep #13j-comparable set) | 268 total (212 `.md` + 56 `.mjs`/`.py`) — every hit read and classified above |
| `verdict\|pass/fail\|pass or fail` — `.md` only, by file | 65 files; largest: `rules-distill` 14 · `santa-loop` 13 · `learn-eval` 13 · `santa-method` 11 · `orchestrate` 11 · `polish.md` 10 · `ecc-opensource-sanitizer` 9 · `skill-stocktake` 7 |
| `verdict\|pass/fail\|pass or fail` — scripts incl. `.js`/`.json` | 114 hits across 21 files — every hit read (see §b script areas) |
| `SHIP / SHIP WITH FIXES / DO NOT SHIP` (`.md`) | 1 file only: `skills/browser-qa/SKILL.md:105–106` |
| `DO NOT SHIP` / `SHIP WITH FIXES` outside `browser-qa` | 0 |
| `ship/fix/rebuild` or `ship or fix` (`.md`, excl. `browser-qa`) | 1 hit, and it is the denial itself: `review-finish.md:5` ("not a ship/fix/rebuild verdict") |
| `22 treatments` (any file, incl. `build.sh`) | 0 — only the quoted reel title `"22 Backgrounds…"` survives at `less-flat-ui/SKILL.md:8` |
| `## The 23 treatments` in `build.sh` | 2× (`:22069`, `:22072`) |
| `verdict\|pass/fail\|pass or fail` in `hooks/` | 0 |
| `candidate-evidence` mentions | unchanged from sweep #13j (orchestrate ×3, orch-build-mvp ×2 routing) |

Raw hit lists (durable record; `/tmp` does not persist between sessions here): `~/workspace/hackathon-plugin/fix14/sweep14-md-hits.txt` (212 lines), `~/workspace/hackathon-plugin/fix14/sweep14-script-hits.txt` (114 lines).

## Adjudicated design — NOT re-flagged (per task)

- Static sloplint gates 63 / 65 / 67 / 38iii as code-level proxies, and the gates §1 `FAIL`/`REFLEX` static grades.
- `ui-ux-pro-max` carve-out ("absolute as static/code-level checks … never a pass/fail verdict") — verified still present at `skills/ui-ux-pro-max/SKILL.md:14, :91`.
- Gates §6 ship rule ("Nothing ships with an open `FAIL` or an open `REFLEX`") and the Taste gate (`references/gate.md`, `gate.mjs` build-round gate) — not re-opened.
- `git checkout` hits in both revert paragraphs — explanatory warning text only, not restore instructions.
- Hooks/adapter.js as live Cursor infrastructure, not Claude Code-only; `scripts/lib/agent-emit-pi.js` dead code as Pi-native; byte-identical assets not defects; 71/96 command files with only `description:` frontmatter not a defect.
- Explicit `--domain` plain search serving reference rows only.
- OpenMontage runtime-fetch unpinned clone (documented opt-in) — not flagged.
- Pip pinning pass — separate pending decision, not touched.

## Notes / open items (not findings)

- The GAN evaluator's PASS/FAIL (threshold 7.0) is a loop-iteration gate over code-level rubric rows, documented in the agent file as excluding screen distinctiveness; if a future round ever lets a GAN score decide a redesign without a fresh `browser-qa` verdict, that would be a finding — today it does not.
- `consistency.mjs`'s per-rule FAIL/WARN verdicts are layout-correctness defects found in a real browser (empty ground, section bleed, rhythm change); they rest on the same adjudicated basis as `check.mjs` (`SKILL.md:283`, `layout-v4.md:294`). If a future round ever let a consistency FAIL decide template-ness/distinctiveness without `browser-qa`, that would be a finding — its own header frames them as "the builder must fix it (or report why it is false)", i.e. defect findings, not distinctiveness verdicts.
- Built `less-flat-ui/SKILL.md` differs from its source only by the pre-existing W2-C1 build patch (3 hunks); the Soft Shadow section is identical in both. No action needed.
- `build.sh` contains no `DO NOT SHIP` literal because `browser-qa` is copied from source rather than embedded as a patch string; the built tree is the authoritative surface and it holds the verdict language only at `browser-qa/SKILL.md:105–106`.
