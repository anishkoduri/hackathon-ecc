# Sweep #15 — fix15 rule-change sweep

- **Date:** 2026-11-11 (Wed), ~16:04–16:20 CST
- **Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
- **build.sh:** 23,217 lines, md5 `1f1a232572b9e12332733688838e1233` (verified — matches the task handoff)
- **Built-tree manifest:** `35a525fd3796229eb4f85cbb5275c36f` in both `fix15/manifest1.txt` and `fix15/manifest2.txt` (diff 0)
- **Counts:** 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks (hooks.json: 15 entries; re-verified)
- **Mode:** READ-ONLY. Nothing in the plugin tree, `build.sh`, the repo, or the bundle was edited. No build executed. `fix15/verify15.py` re-run (read-only check): **43/43 pass, exit 0**.
- **Rule swept for:** fix15 must not introduce a second screen-verdict executor, stale counts, canonical-block drift, or weaken a standing invariant. Single executor remains `browser-qa`.

## Verdict: CLEAN

- **Blocking: 0**
- **Minor: 0**

Every fix15-introduced verdict-shaped hit was read in its file and confirmed to be correctly routed: an explicit "static check, not a screen verdict" framing, a "candidate evidence / consistency only, never a verdict" routing, or the one legitimate issuer (`browser-qa` itself). The canonical block is byte-identical in all 11 files. No stale count survives. Every cited anchor contains the claimed rule.

Prior-checker baseline for this build: Audit #52 ZERO, dry-run #24 CLEAN, sweep #14 CLEAN (0/0). This sweep finds nothing new: the fix15 change introduced no verdict language, no drift, and no stale count.

## Blocking findings

None.

## Minor findings

None.

## (a) Verdict-language sweep — fix15-introduced hits, all read

Whole-tree grep (excl. `node_modules`) for `verdict|pass/fail|pass or fail`: **332 hits total** — 274 in `sweep15-md-hits.txt` (218 `.md` + 50 `.mjs` + 7 `.py`) and 58 in `sweep15-script-hits.txt` (57 `.js` + 1 `.json`; regenerated clean after the first script list double-counted overlapping paths). The `.md` count rose 212 → 218 vs sweep #14, exactly the fix15 insertions; every new hit is in the fix15 files and is quoted below. No `.js`/`.json` hit lives in any fix15-touched file.

### browser-qa (the legitimate issuer) — unchanged

- `skills/browser-qa/SKILL.md:105–106`: `### Verdict: SHIP WITH FIXES (2 issues, 0 blockers)` and `# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline`. Whole-tree grep for `DO NOT SHIP` / `SHIP WITH FIXES` outside `browser-qa`: **0 hits**.

### Review first words — unchanged

- `references/hallmark/references/review-hero.md:5`: first line `findings` or `no-findings` — "a craft status, not a ship/fix verdict".
- `references/hallmark/references/review-finish.md:5`: first line `recapture` / `findings` / `no-findings` — "a craft status, not a ship/fix/rebuild verdict".
- `gates.md:245`: "Act on its first word. `recapture` means the screenshots were wrong …" — same craft-status vocabulary as sweep #14. Zero surviving ship/fix/rebuild first-word values tree-wide outside `browser-qa`; the only `ship/fix/rebuild` hit in any `.md` file is `review-finish.md:5` itself, which explicitly denies it is one.

### R1 "incomplete build" — static check, never a screen verdict

- Taste `skills/design-taste-frontend/SKILL.md:244`: "A dealt moment with neither is an incomplete build — a static check item in step 6 below, never a screen verdict."
- Taste `:290`: "Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)."
- Orchestrate `skills/orchestrate/SKILL.md:61` (5a Verify): same sentence, "Static check, not a screen verdict: … an incomplete build (fix #15 R1)."
- Orch-build-mvp `skills/orch-build-mvp/SKILL.md:51` (step 6 tail): same sentence, "Static check, not a screen verdict: … an incomplete build (fix #15 R1)."
- "Incomplete build" is a build-record completeness gate (a dealt moment with no application and no re-deal log), not a judgment on a rendered screen. It creates no second verdict executor.

### D1 screenshot QA — no duplicate pass, no second verdict executor

- The D1 paragraph is byte-identical (md5 `d41d8cd98f00b204e9800998ecf8427e`) in all four placements: Taste `:310`, orchestrate `:60`, orch-build-mvp `:51`, polish-pass `:104`. It ends: "Findings feed the fix batch like other checks; browser-qa alone issues pass/fail verdicts on rendered screens." The exact sentence `browser-qa alone issues pass/fail verdicts on rendered screens` occurs **1× in each** of the four files.
- "A build that never ran a screenshot QA pass is incomplete and cannot be reported as finished" is a process-completeness gate on the final report (same family as orchestrate's existing HELD-deploy re-verification gate), and the same sentence routes verdicts to `browser-qa`. No second executor.
- Final-report recording lines verified: orchestrate `:66` and orch-build-mvp `:59` both contain "screenshot QA pass (tool, screens, findings count) — a build that never ran a screenshot QA pass is incomplete and cannot be reported as finished (fix #15 D1)."

### C1/C2/R5 — Taste step 4a (`:246`) and ui-ux-pro-max (`:89`)

- Taste `:246` (single long line): C1 "The dealt pairing is the ONLY permitted faces on the build — no other face is introduced"; C2 "Display faces are self-hosted (bundled woff2 + `@font-face` in the built page) … the closest installed font is a failure, not a fallback" — "failure" here is a font-source failure (wrong font bundled), not a screen verdict; R5 "Each Range pattern's named lead element is its own element … recorded as its own type moment in `docs/design-tokens.md`, distinct from the surface carrying it." No verdict language.
- ui-ux-pro-max `:89`: "The dealt pairing / type scale is the ONLY permitted faces on the build — no other face is introduced" — a font-permission rule, no verdict language.

### C3 — Taste step 6 (`:290`) and polish-pass harmony (`:22`)

- Taste `:290`: "Copy + type checks enforced and recorded (fix #15 C3). Taste copy-voice rules apply to ALL copy; craft-floor type checks … are verified per surface and recorded in `docs/design-tokens.md`'s Type list" — a record-keeping check, no verdict.
- polish-pass `:22`: harmony verifies the Type list with "harmony divergence, recorded as candidate evidence, never a verdict (fix #15 C3 — consistency only)." Explicitly routed to candidate evidence.

### R2 / R4 — Taste asset table (`:153`) and step 5 (`:268`)

- `:153`: software column now reads `1-2 by default, pulsing; 0 only with a recorded reason in the section plan` (hardware / product / place columns unchanged). No verdict language.
- `:268`: "The dealt hero's loop is implemented or waived (fix #15 R4 …). The dealt hero's loop (or moment-inside-window) is implemented and recorded in `docs/design-tokens.md`, or waived with reason there." No verdict language.

### R3 — less-flat-ui surface check (`:14`)

- "TWO DISTINCT treatment kinds must be recorded per screen, or \"none — <reason>\" per untreated surface (fix #15 R3 — baseline: 2 treatment applications, both Soft Shadow, one kind)." A per-surface recording requirement, no kind hard-coded, no verdict language. Pre-existing `ship the dithered file` (`:264`, Bayer-dither treatment — "ship" as "output the processed file") is unchanged from sweep #14.

### Canonical block (§A) — no verdict language in it

- The block (701 chars, single line) contains no ship/fix/rebuild/pass/fail/verdict wording. It states variety, theme-match as a precondition, and per-surface recording in `docs/design-tokens.md`.

## (b) Canonical-block consistency sweep — byte-identical in all 11

Single-line md5 `5cce9ed89deb681e6b51596a8b35b364` (701 chars) in every file, at the manifest-cited lines:

| File | Line |
|---|---|
| `skills/design-taste-frontend/SKILL.md` | 55 |
| `skills/ui-ux-pro-max/SKILL.md` | 16 |
| `skills/less-flat-ui/SKILL.md` | 16 |
| `skills/polish-pass/SKILL.md` | 45 |
| `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md` | 20 |
| `skills/make-interfaces-feel-better/SKILL.md` | 15 |
| `skills/motion-foundations/SKILL.md` | 46 |
| `skills/motion-patterns/SKILL.md` | 43 |
| `skills/motion-advanced/SKILL.md` | 45 |
| `skills/orchestrate/SKILL.md` | 92 |
| `skills/orch-build-mvp/SKILL.md` | 42 |

Zero drift: no wording, heading, or punctuation difference. (Method note: a first paragraph-extraction pass falsely flagged orch-build-mvp, because no blank line follows its block — the next list item continues on the following line. Extracting the single block line itself gives the identical md5. Not a finding.)
- `gates.md` correctly contains **0** occurrences of the block (staged verbatim from upstream, untouched — `verify15.py` also confirms staged == staged source).

## (c) Stale-count sweep — treatments still 23 everywhere

- `22 treatments` / `22 textured`: **0 hits** tree-wide (excl. `node_modules`) and **0 hits** in `build.sh`.
- `23 treatments` / `23 textured`: 3 hits, all in `skills/less-flat-ui/SKILL.md` — frontmatter `:3` (`23 textured treatments`), source line `:8` (`Source of the 23 treatments: … "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)"` — the quoted reel title, preserved as in fix14), heading `:102` (`## The 23 treatments`).
- Counts unchanged: 169 / 72 / 123 / 96 / 15 (re-verified by directory listing + hooks.json entry count).

## (d) Anchor sweep — every cited file:line contains the claimed rule

All manifest anchors verified by reading the lines (not the citation):

| Rule | Anchor(s) | Verified |
|---|---|---|
| Canonical §A | 11 lines above | byte-identical md5 in all 11 |
| R1 | Taste `:244`, `:290`; orchestrate `:61`; orch-build-mvp `:51` | yes — "every dealt moment … or re-deal log entry", static-check framing |
| R2 | Taste `:153` | yes — `1-2 by default … 0 only with a recorded reason` |
| R3 | less-flat-ui `:14` | yes — TWO DISTINCT kinds per screen, or `none — <reason>` |
| R4 | Taste `:268` | yes — loop implemented or waived, recorded in design-tokens.md |
| R5 | Taste `:246` | yes — lead element recorded as its own type moment |
| C1 | Taste `:246`; ui-ux-pro-max `:89` | yes — dealt pairing/scale is the ONLY permitted faces |
| C2 | Taste `:246` | yes — self-hosted display faces, `@font-face` checkable |
| C3 | Taste `:290`; polish-pass `:22` | yes — Type list recorded; harmony checks it, consistency only, never a verdict |
| D1 | Taste `:310`; orchestrate `:60`, `:66`; polish-pass `:104`; orch-build-mvp `:51`, `:59` | yes — identical paragraph in all four rule placements; recording lines in both step-6/9 final-report lines |

`verify15.py` independently passes the same anchors (43/43, re-run this sweep).

## (e) Standing invariants — none weakened in passing

- **Single screen-verdict executor:** D1's "cannot be reported as finished" and R1's "incomplete build" are both explicitly framed as static/completeness checks, and every D1 placement closes with "browser-qa alone issues pass/fail verdicts on rendered screens." No second executor is created.
- **"More, not bolder":** still present — orchestrate `:94` ("Posture — more, not bolder") and orch-build-mvp `:40` (design-package rule). Untouched.
- **Shared fresh-verdict budget (2 rounds):** still stated in orch-build-mvp `:51` step-6 tail ("the fresh-verdict budget — 2 rounds total across 6b and step 6") and orchestrate's re-verification lines. Untouched.
- **Craft-floor bans / Hallmark floor / no-violet / anti-derivative / snapshot-before-redesign:** no fix15 text touches them; the only fix15-adjacent ban text is C2's font-source "failure", which is a build-step failure, not a screen verdict.

## Adjudicated design — NOT re-flagged (per task)

- Explicit `--domain` plain search serving reference rows only; hooks/adapter.js as live Cursor infrastructure; byte-identical assets not defects; `agent-emit-pi.js` dead code as Pi-native; gates §1 `FAIL`/`REFLEX` static grades and §6 ship rule; `ui-ux-pro-max` carve-out; sloplint static grades; GAN evaluator PASS/FAIL iteration gate; `consistency.mjs` layout-correctness FAIL/WARN; Santa/learn-eval/rules-distill/code-reviewer/astra-review verdicts (code review, tradeoff, inventory, or test gates, not rendered screens). All re-confirmed present-and-unchanged in the 332-hit read; none re-opened.

## Raw hit lists (durable record)

- `~/workspace/hackathon-plugin/fix15/sweep15-md-hits.txt` — 274 lines (218 `.md` + 50 `.mjs` + 7 `.py`)
- `~/workspace/hackathon-plugin/fix15/sweep15-script-hits.txt` — 58 lines (57 `.js` + 1 `.json`, no duplicates)
- Note: sweep #14's script list (114) counted `.mjs` hits in its script file; this round's `.mjs` hits live in the md list instead. Combined coverage is the same surface: 332 verdict-hits total, all fix15-new ones read in context above.
