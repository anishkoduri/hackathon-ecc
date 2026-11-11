# Sweep #13j — single-executor screen-verdict sweep

- **Date:** 2026-11-11 (Wed), ~04:01–04:35 CST
- **Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
- **build.sh:** 23,160 lines, md5 `b7432cc6ff576dbdf620b8d26bd87984` (verified — matches the task handoff)
- **Built-tree manifest:** `a188d10d2900e5b022d5ca173627fa07`
- **Counts:** 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- **Mode:** READ-ONLY. Nothing in the plugin tree, `build.sh`, the repo, or the bundle was edited. No pip pinning pass done.
- **Rule swept for (single-executor rule):** `browser-qa` ALONE issues pass/fail verdicts on rendered screens. Everything else is design guidance, candidate evidence, or static checks.

## Verdict: CLEAN

- **Blocking: 0**
- **Minor: 0**

No screen verdict fires outside `browser-qa`. Every verdict-like hit found was read in its file and confirmed to be correctly routed candidate evidence, a static/code-level check, craft guidance, a non-screen verdict (code review, tradeoff, inventory, test/loop gate), or the one legitimate issuer (`browser-qa` itself).

Prior-checker baseline for this build: Audit #50 ZERO ERRORS, dry-run #22 0 blocking / 1 minor, previous sweep CLEAN (0/0). This sweep finds nothing new: the single fix13j change introduced no verdict language.

## Blocking findings

None.

## Minor findings

None.

## (a) Fix13j areas — verified

### Orchestrate step 5b — `skills/orchestrate/SKILL.md:60`

- Snapshot manifest (snapshot path + whole-tree file list + per-file hashes, one line per file) lives in `docs/run-ledger-appendix.md` **under a `<redesign-id>` heading**, with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path + appendix file + line count). Stated twice in the paragraph (the snapshot rule and the snapshot-before-redesign rule) and both wordings agree.
- Revert step (2) **names the manifest file**: "comparing the post-redesign tree against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section)" and "verify against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section) alone".
- Coverage check **names the manifest file**: "the orchestrator compares the design skill's changed-file list against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section)".
- No verdict language crept in. The only verdict words in the paragraph are `browser-qa`'s: "a generic-template finding on `browser-qa`'s verdict", "the orchestrator runs a fresh `browser-qa` verdict run", "the redesign decision follows `browser-qa`'s verdict". The `git checkout` hit is the adjudicated explanatory warning ("`git checkout` restores HEAD, not the verified state, and never deletes untracked files"), not an instruction.
- Exclusions consistent: whole tree except `.hackathon/` and `.hallmark/candidate-evidence.md`; run state never snapshotted/restored.

### Standalone orch-build-mvp step 6b — `skills/orch-build-mvp/SKILL.md:53`

- Identical routing: manifest in `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, one-line pointer in `.hackathon/run-ledger.md`; revert step (2) and the coverage check both name the manifest file in the appendix under the `<redesign-id>` section. Wording matches orchestrate 5b in substance (same exclusions, same `git checkout` explanatory warning, same shared fresh-verdict budget `0/2`, same `re-verification <redesign-id>: PASSED/BLOCKED` ledger entries).
- The two engines are consistent with each other; no divergence found.
- `build.sh:23127` carries the same manifest-under-heading wording; `build.sh:23108` is the fix13j dry-run marker. `build.sh` grep counts: `docs/run-ledger-appendix.md` ×6, `snapshot manifest` ×16.

## (b) Named areas — all verified clean

### Hallmark `gates.md` — `skills/design-taste-frontend/references/hallmark/references/gates.md`

- **§1 (lines 12–20):** Grades `FAIL` / `REFLEX` / `WAIVED` / `WARN` / `ANSWERED` / `NOTE` are static gate grades; Ledger (32) "never counts toward the verdict". Adjudicated static grading, not a screen verdict.
- **§3 (lines 38–40):** Pre-emit critique — "this critique is a design input, not a distinctiveness verdict"; Specificity under 3 is appended to `.hallmark/candidate-evidence.md` for `browser-qa`, "never a verdict on its own".
- **§5 judged clauses (lines ~199–247):** 6b, 8/32, 9, 23, 68, 80–82, 83, 85 each say "candidate evidence … for `browser-qa` to weigh" / "not a template verdict". 38iii, 63, 65, 67 are static/code-level proxies (adjudicated). Remaining judged clauses (11, 16, 44, 46b, 47c, 54, 58, 62, 66, 69, 70, 77–79, 84) are craft judgments, not distinctiveness verdicts. F-checks are "never block" (F9's FAIL half is a static fake-avatar check).
- **§6 (lines ~230–247):** "Nothing ships with an open `FAIL` or an open `REFLEX`" — the adjudicated §6 ship rule; not re-opened. Reviews run in fresh context; first words are the craft-status vocabulary (see below).

### sloplint scope guard — `skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs` / `sloplint-render.mjs`

- `sloplint.mjs:2` header: "Its FAIL/REFLEX/WARN grades are static-check grades, not pass/fail verdicts on rendered screens — screen distinctiveness is judged only by `browser-qa` in the visual loop."
- `sloplint.mjs:798–799` `APP_SKIP` skips gates 1, 6, 8, 9, 32, 42, 44, 46b, 58, 59, 66, 68, 77, 78, 79, 81, 82, 83, 85, F8, F15, F20 in `--scope app` (applied at :905).
- `sloplint-render.mjs:2` header: "Template gates (80, 81, 82, 83, 85) never issue REFLEX verdicts here: on landing pages they emit NOTE candidate evidence for `browser-qa`; on app screens they are skipped"; `:741–748` `templateEvidence()` implements exactly that. Both engines also run sloplint `--render` on the landing page in step 6 (orchestrate Verify step 6, standalone step 6), so the render tier is wired in — no verdict leak anywhere in this area.

### Taste hero bar — `skills/design-taste-frontend/SKILL.md:53`

- "record that as candidate evidence for `browser-qa`, whose visual-loop verdict alone decides whether the hero passes the distinctiveness bar, even if every other check passes." Clean.
- `:242` Impeccable gloss: bans are "absolute as static/code-level checks … a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone)"; "the stricter ban wins" except gate 2b's guarded single-hue gradient-text ramp and page-level template patterns, which are candidate evidence. Clean.
- `:283` / `references/layout-v4.md:294`: "`check.mjs` finding fails the page on layout-correctness grounds … a layout finding is not a distinctiveness verdict — that is `browser-qa`'s alone." Layout-correctness failure is a rendered-layout correctness check, not a distinctiveness/template verdict. Checked, not flagged.
- `:314` hero review dispatch: acts on first word `no-findings` / `findings` for craft findings only.
- `references/layout-v4.md:182`: weak-hero observations are "candidate evidence of a weak hero for `browser-qa` to weigh, not a fail verdict on its own." Clean.
- `references/moments.md:30` (`giant-type-pass` "reads as a template trick") and `references/perf.md:10` ("WebGL off is a proxy, not a verdict") are descriptive, not verdicts. Clean.

### Impeccable craft floor Refuse list — `skills/polish-pass/reference/impeccable-craft-floor.md:30–35`

- "except the two page-level template patterns below (same-size cards as the page structure; the hero-metric template), which are candidate evidence for `browser-qa`, never a rewrite on this check alone". Both patterns repeat the routing: "append it (screen + pattern) to `.hallmark/candidate-evidence.md`; do not rewrite on this check alone." The remaining Refuse items are element-level rewrite guidance (kicker/eyebrow ban, section numbers, modal), not screen verdicts. Clean.

### Critique assessment + Design Health Score bands — `skills/polish-pass/reference/impeccable-critique.md`

- `:56` / `:62`: Design specificity is "candidate evidence for `browser-qa`, not a verdict".
- `:142`: "Record the outcome as candidate evidence for `browser-qa`'s visual-loop verdict, not as a verdict … Priority fixes carry a generic-template item only when `browser-qa`'s verdict has established it".
- `:595` band table: "36–40 | Excellent | Minor polish only; informs candidate evidence, never a ship verdict"; `:601`: "The bands inform candidate evidence for `browser-qa`; only `browser-qa`'s verdict establishes a finding." "Redesign indicated, not decided" (0–11 Critical) is explicitly non-decisive. Clean.
- P0–P3 issue severities (:~605+) are per-issue priorities, not screen verdicts. Clean.

### polish.md bans gloss — `skills/polish-pass/reference/polish.md`

- `:7`: generic-template finding "exists only on `browser-qa`'s visual-loop verdict".
- `:24` (Step 2.7 harmony check): "Harmony does NOT judge whether a screen reads as a default template — that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY".
- `:39` (Step 4.1): bans "absolute as static/code-level checks … never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone); where the two floors disagree, the stricter ban wins — except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite decided here."
- `:51` (Step 5.2): `icon-tile-stack` detector finding is appended to candidate evidence "and fix it only on `browser-qa`'s verdict — never rewrite a template pattern on the detector's say-so alone."
- `:81–84` report template: "Direction-application is `browser-qa`'s verdict, cited not judged" and "Generic-template findings (only on `browser-qa`'s visual-loop verdict)". Clean.

### web-design-quality.mdc Anti-Template Policy — `rules/web-design-quality.mdc`

- Heading itself: "Anti-Template Policy — design guidance, not a ship verdict". Body: "This rule never decides whether a surface ships: a surface that looks like a default template is candidate evidence for `browser-qa` … only `browser-qa`'s pass/fail verdict on the rendered screen decides template-ness." Checklist asks whether a template look "is recorded as candidate evidence … (not decided here)". Clean.

### Critique score bands — `skills/polish-pass/reference/scoring.md`

- Level placement (:43): "an internal scoring anchor for polish's own Score, not a pass/fail verdict on a rendered screen; a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict."
- Persona-fit cap (:55) and tell-count cap (:56): both apply "only on `browser-qa`'s visual-loop verdict", never on polish's own observation or tell count alone.
- Overall-Score cap (:59): "Level is polish's internal scoring anchor, not a pass/fail verdict on a rendered screen." Craft-floor-ban cap (:54) is a static/code-level finding recorded in the Score. Clean — polish's Score is an internal working score, never a ship/redesign decision.

### Harmony consistency records — `skills/polish-pass/SKILL.md:22–24, :96` + `polish.md:24, :81`

- Harmony checks per-screen consistency against the recorded direction only ("consistent / diverges, with the tokens cited"); "Harmony never verdicts screen distinctiveness". A direction-not-applied screen is appended to candidate evidence; a missing direction is a minor finding routed to the design skill, never a screen pass/fail. Clean.

### Detector rules — `skills/polish-pass/scripts/detect.mjs`, `reference/impeccable-detector-rules.json`

- `detect.mjs:4`: "Findings are evidence to verify in context, not verdicts." `icon-tile-stack` is a `warn`-severity static rule; its handling is routed via `polish.md:51` (candidate evidence, fix only on `browser-qa`'s verdict). Clean.
- `reference/patterns/vibe-code-tells.md:3, :36`: each tell is "a static/code-level signal and candidate evidence for `browser-qa`, not a pass/fail verdict"; "A tell — or three or more tells — is candidate evidence for `browser-qa`, never a generic-template finding on its own."
- `reference/craft-floor.md:111, :168`: bans are "a static/code-level check on the source, and a finding under it is candidate evidence for `browser-qa` — never a pass/fail verdict"; template-pattern bans are "done when … appended to `.hallmark/candidate-evidence.md` … fixed only on `browser-qa`'s verdict". Clean.

### Review first words — `references/hallmark/references/review-hero.md:5`, `review-finish.md:5`

- Hero: first line `findings` or `no-findings` — "a craft status, not a ship/fix verdict … template observations are candidate evidence for `browser-qa` and never drive it."
- Finish: first line `recapture` / `findings` / `no-findings` — "a craft status, not a ship/fix/rebuild verdict … template observations (`Seen before`, machine-made) are candidate evidence for `browser-qa` and never drive it." **No surviving ship/fix/rebuild first-word value found anywhere in the tree** (whole-tree `.md` grep for `ship/fix/rebuild` / `ship or fix` outside `browser-qa`: 0 hits).
- Both reviews route every template observation to `.hallmark/candidate-evidence.md`, including the custom-run and polish variants. Clean.

### design-system slop detection — `skills/design-system/SKILL.md:56`

- "Scope — pattern evidence, not a distinctiveness verdict: the patterns below are code-level evidence (they exist in the code); a slop finding — including 'Generic hero with centered text over stock gradient' — is candidate evidence for `browser-qa`, never a verdict that a screen reads as a default template." Clean.

### ui-ux-pro-max carve-out — `skills/ui-ux-pro-max/SKILL.md:14, :91`

- `:14` captivating bar: "design guidance, not a screen verdict … Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable".
- `:91` anti-generic bar: "design guidance, not a screen verdict … Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail." Clean (adjudicated carve-out holds).

### GAN harness / evaluator — `skills/gan-style-harness/SKILL.md:118, :255`, `agents/ecc-gan-evaluator.md`, `commands/gan-build.md:84`

- Harness `:118`: "Screen distinctiveness is NOT scored here … judged ONLY by `browser-qa` in the visual loop … never by this evaluator." Design Quality / Originality rows score the recorded direction and its code-level application only. `:255`: penalties are "code-level direction-application failures only — never screen distinctiveness".
- Evaluator agent `:31, :48, :65, :70, :96, :118`: first impression and slop scoring are "code-level evidence only, never a screen-distinctiveness verdict"; rubric must carry the scoping note before scoring.
- Evaluator `:155` "Verdict: PASS / FAIL (threshold: 7.0)" and `gan-build.md:84` "Result: PASS/FAIL" are the GAN loop's **iteration gate** over rubric rows that exclude screen distinctiveness (score ≥ 7.0 stops iterating; the loop decides iteration, not shipping). The redesign/ship decision still follows `browser-qa`'s verdict in orch-build-mvp steps 6/6b. Checked in context, not flagged — it is a build-loop gate of the same kind as test pass/fail, not a rendered-screen verdict.

### browser-qa (the legitimate issuer) — `skills/browser-qa/SKILL.md:68, :105–106`

- `:68`: "this skill is the SOLE executor of the distinctiveness bar inside the visual loop … treat [candidate-evidence] entries as candidate evidence … never as a verdict … No other step judges screen distinctiveness".
- `:105–106`: the only SHIP / SHIP WITH FIXES / DO NOT SHIP verdict in the tree. Clean — this is the single executor the rule names.

### Orchestrate Verify steps 5–6 — `skills/orchestrate/SKILL.md:193–195`

- Step 5: "`browser-qa` is the SOLE executor of this bar inside the visual loop"; Taste's hero bar is "design guidance and candidate evidence feeding the verdict, never a bar `browser-qa` executes on its own"; step-2 reviewer "checks only the recorded direction, never the screens".
- Step 6: Specificity under 3 and finish-review template observations go to candidate evidence; "only `browser-qa`'s verdict decides whether a fix is owed"; app-scope sloplint "does NOT carry the distinctiveness check". Clean.
- Step 4a reviewer (:189): "never an approve/reject verdict; a clean pass enumerates the properties … it checked." Clean.
- End-of-project checks (:289) "pass/fail and findings count" are deferred code/security checks, not screen verdicts. Clean.

### Other files checked

- `skills/design-taste-frontend/references/hallmark/references/redesign.md:40`: "Look at the screenshots before you weigh the findings, so the linter does not write the verdict"; the read names "what suggests a generated look (the strongest candidate evidence, by gate)". The Picks-block example line ("a centred template in a stock indigo") summarises that read; it decides no ship outcome. Clean.
- `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md:63–67`: Specificity is candidate evidence, "never a distinctiveness verdict"; other five axes join the fix list as craft judgments. Clean.
- `skills/frontend-design-direction/SKILL.md:27`: "reads as flat, generic, templated" appears only as a *when-to-use* trigger (a user-facing symptom description), not as a verdict issued by the skill. Clean.
- `skills/loop-design-check/SKILL.md`: no verdict / pass-fail / ship / template hits at all. Clean.
- `commands/orchestrate.md`, `commands/orch-build-mvp.md`: no verdict / distinctiveness / template / pass-fail hits. Clean.
- `skills/verification-loop/SKILL.md`: no verdict / distinctiveness / template / screen hits. Clean.
- Remaining whole-tree "verdict" hits (agents `ecc-code-reviewer`, `ecc-*-reviewer`, `scout`; skills `council`, `skill-stocktake`, `django/springboot-verification`, `agent-self-evaluation`, `click-path-audit`, `feature-expansion`, `santa-method`, `security-scan`; commands `code-review`, `gan-build`, `santa-loop`, etc.) are code-review, tradeoff, inventory, or test/verification verdicts — none judges a rendered screen's distinctiveness or template-ness. Spot-checked `agents/ecc-code-reviewer.md`, `agents/scout.md`, `skills/click-path-audit/SKILL.md`, `skills/council/SKILL.md`: zero distinctiveness/screen-template hits. Not flagged.

## (c) New verdict-like wording anywhere in the tree

None found. Whole-tree sweeps:

| Grep (excl. `node_modules`) | Hits |
|---|---|
| `verdict\|pass/fail\|pass or fail` — all files incl. scripts (`.md`/`.mjs`/`.py`/data) | 255 total (design-scope `.md` subset: 79 — all read, see `/tmp/sweep13j-md-hits.txt` for the raw list) |
| `verdict` (case-insensitive, `.md` only) by dir | skills 128 · agents 21 · commands 27 · rules 0 · hooks 0 · scripts 0 |
| `is the template\|reads as a template\|generic` — design scope `.md` | covered inside the 79-hit set above; every hit read |
| `SHIP / SHIP WITH FIXES / DO NOT SHIP` (`.md`) | 1 file only: `skills/browser-qa/SKILL.md:105–106` |
| `ship/fix/rebuild` or `ship or fix` (`.md`, excl. `browser-qa`) | 0 |
| `candidate-evidence` mentions | `skills/orchestrate/SKILL.md` ×3 · `skills/orch-build-mvp/SKILL.md` ×2 |
| `run-ledger-appendix.md` in `build.sh` | ×6; `snapshot manifest` ×16 |

## Adjudicated design — NOT re-flagged (per task)

- Static sloplint gates 63 / 65 / 67 / 38iii as code-level proxies, and the gates §1 `FAIL`/`REFLEX` static grades.
- `ui-ux-pro-max` carve-out ("absolute as static/code-level checks … never a pass/fail verdict") — verified still present at `skills/ui-ux-pro-max/SKILL.md:14, :91` (via the Taste :242 gloss and polish :39).
- gates §6 ship rule ("Nothing ships with an open `FAIL` or an open `REFLEX`") and the Taste gate (`references/gate.md`, `gate.mjs` build-round gate) — not re-opened.
- `git checkout` hits in both revert paragraphs — explanatory warning text only, not restore instructions.
- OpenMontage runtime-fetch unpinned clone (documented opt-in) — not flagged.
- Pip pinning pass — separate pending decision, not touched.

## Notes / open items (not findings)

- Step-6 sloplint coverage, verified while reading: both engines run sloplint `--render` on the landing page in step 6 (orchestrate Verify step 6, `skills/orchestrate/SKILL.md:195`; standalone step 6, `skills/orch-build-mvp/SKILL.md:49`) in addition to `--scope app` on app screens. No verdict leak there either way; nothing to fix.
- The GAN evaluator's PASS/FAIL (threshold 7.0) is a loop-iteration gate over code-level rubric rows, documented in the agent file as excluding screen distinctiveness; if a future round ever lets a GAN score decide a redesign without a fresh `browser-qa` verdict, that would be a finding — today it does not.
- Raw grep output for the design-scope `.md` hit set is at `/tmp/sweep13j-md-hits.txt` (79 lines, ephemeral scratch — the per-hit dispositions above are the durable record).
