# Fix #23 §4/§5 — Disposition (worker W3: hero + functionality)

Baseline: build.sh 23,774 lines, md5 `4799a819791b9c3ec4c19136ad698397`
(unchanged at end of this work — verified). No bundle, no commit, no push.
`build.sh` was NOT run; `apply-w3.py` was NOT executed as `__main__`
(anchors + generated block verified read-only only). `fix11/fix11-stage.py`
not run. Built tree untouched. `~/workspace/cursor-skills/less-flat-ui`
untouched. `/demo` wiring / DEMOGATE tokens untouched. No bare
`grok-4.6-high-fast` anywhere in new text (no model names used at all).

## Interpretation notes (recorded, not silent)

- **Hallmark theme-deal output:** the deal output the build consumes is
  the Picks block (`.hallmark/picks.md` — Material + Signature rows),
  whose format is defined in Taste step 4, and the hero review
  (`references/hallmark/references/review-hero.md`) is where it is read.
  The hero-moment line was therefore added in BOTH places: the Picks-block
  instruction in Taste step 4 (Hero-moment row) and the hero review's
  inputs + question list. No theme file was edited (the 50 theme files
  carry `pictured:` hero shapes, not a per-build moment row — the moment
  is per-build, so it lives in the per-build Picks block, not the catalog).
- **"F2 stack labels stand" (§5):** covered, unchanged. No edit in this
  change touches stack labels; the functionality rule names the stack
  where the mechanism is shown (FUNC_F23) and the ui-ux-pro-max pointer
  routes to it. No separate placement needed.
- **Orchestrate:** NOT edited (another worker owns it). The §4/§5
  design-package lines are delivered as `fix23/orch-lines-w3.py`
  (`ORCH_LINES_W3`) for the integration worker to insert mechanically
  into orchestrate step 3 (see that file's docstring for the anchor).

## Placement table — every §4/§5 item

| # | SPEC item | Placement (file + anchor token) | Status |
|---|---|---|---|
| 4.1 | Hero gets a dealt amazing moment: dealt moment + distinctive composition + motion, recorded in the decision record | `new-skills/design-taste-frontend/SKILL.md`, House rules, after "Captivating hero — the bar" paragraph — **HERO_F23** | new |
| 4.2 | Hero is the highest-weight browser-qa surface; a merely adequate hero fails F6 | Taste **HERO_F23** (same paragraph) + `fix23/apply-w3.py` runtime sub **HERO-BQA_F23** (`skills/browser-qa/SKILL.md`, after visual-loop paragraph) | new |
| 4.3 | Calibration: app home/feed surface IS the hero surface, bar calibrated to the product's job, moment serves the job not decoration | Taste **HERO_F23** + `fix23/orch-lines-w3.py` **HERO_F23** + runtime sub **HERO-BQA_F23** | new |
| 4.4 | "Amazing" never a generic hero section pasted onto an app that does not need one; never louder ("more, not bolder" stands) | Taste **HERO_F23** + runtime sub **HERO-BQA_F23** | new |
| 4.5 | Hero-moment line written to the Picks block (Hero-moment row, alongside Material + Signature) | Taste step 4, Picks-block sentence — **HERO_F23**; consumed by `new-skills/design-taste-frontend/references/hallmark/references/review-hero.md` inputs line — **HERO-REVIEW_F23** (token cited in text as HERO_F23; file anchor is the inputs line) | new |
| 4.6 | Hero review judges the hero against the dealt moment | `review-hero.md`, new question bullet after the signature bullet — **HERO_F23** | new |
| 4.7 | Checklist: first screen carries the dealt moment | Taste §5 Checklist, First-screen bullet — **HERO_F23** | new |
| 4.8 | Static check: hero-moment line + Picks Hero-moment row present (completeness only; verdict is browser-qa's) | Taste step 6, new "Fix #23 static checks" paragraph — **HERO_F23** | new |
| 4.9 | Orchestrate design-package step: dealt hero moment recorded per UI slice brief; brief without one is not ready | `fix23/orch-lines-w3.py`, `ORCH_LINES_W3` — **HERO_F23** (insert into orchestrate step 3, after Depth-strategy paragraph; see file docstring) | staged for integration |
| 5.1 | Design surfaces technical depth: mechanism diagram / live figures / pipeline / data flowing / stack / live system state, first-class, theme-matched | Taste step 4a, after Anti-generic paragraph — **FUNC_F23** | new |
| 5.2 | R2 strengthened: every build shows its mechanism early — hero surface or first screen after it, never buried | Taste **FUNC_F23** + `references/diagrams.md` **FUNC-DIAG_F23** + runtime sub **FUNC-BQA_F23** (`skills/browser-qa/SKILL.md`, Phase 3 step 5) | new |
| 5.3 | F2 stack labels stand | Covered, unchanged — no edit touches stack labels; stack is named where the mechanism is shown (FUNC_F23) | covered |
| 5.4 | Decision record states the functionality story: what is technically new, and how the design shows it | Taste **FUNC_F23** + `fix23/orch-lines-w3.py` **FUNC_F23** | new |
| 5.5 | A build that looks good but hides what the thing does fails | Taste **FUNC_F23** + runtime sub **FUNC-BQA_F23** | new |
| 5.6 | Not a generic "add a diagram": mechanism must be THIS build's (its pipeline, its data, its stack; own names, real figures) | Taste **FUNC_F23** + `references/diagrams.md` **FUNC-DIAG_F23** + runtime sub **FUNC-UIPRO_F23** (`skills/ui-ux-pro-max/SKILL.md`, after Element-variety paragraph) + runtime sub **FUNC-BQA_F23** | new |
| 5.7 | App/dashboard surfaces get the functionality rule via ui-ux-pro-max (pointer, not restatement — full rule lives in Taste) | `fix23/apply-w3.py` runtime sub **FUNC-UIPRO_F23** | new (pointer) |
| 5.8 | Static check: functionality story recorded + mechanism visible early (completeness only; verdict is browser-qa's) | Taste step 6, "Fix #23 static checks" paragraph — **FUNC_F23** | new |
| 5.9 | Orchestrate design-package step: functionality story named per UI slice brief; brief without one is not ready | `fix23/orch-lines-w3.py`, `ORCH_LINES_W3` — **FUNC_F23** | staged for integration |

## Anchor tokens (all `_F23`)

- `HERO_F23` — Taste SKILL.md (hero rule, Picks row, checklist, static check), review-hero.md, orch-lines-w3.py
- `HERO-BQA_F23` — browser-qa runtime sub (apply-w3.py)
- `FUNC_F23` — Taste SKILL.md (functionality rule, checklist, static check), orch-lines-w3.py
- `FUNC-DIAG_F23` — Taste references/diagrams.md
- `FUNC-UIPRO_F23` — ui-ux-pro-max runtime sub (apply-w3.py)
- `FUNC-BQA_F23` — browser-qa runtime sub (apply-w3.py)

## Files changed

1. `~/workspace/hackathon-plugin/new-skills/design-taste-frontend/SKILL.md`
   — 5 insertions (HERO_F23 rule; Picks Hero-moment row; FUNC_F23 rule;
   Fix #23 static checks; Checklist First-screen line). Staged source;
   flows through build.sh copy (staged-vs-built diff remains only the
   frontmatter description rewrite + these edits).
2. `~/workspace/hackathon-plugin/new-skills/design-taste-frontend/references/diagrams.md`
   — 1 insertion (FUNC-DIAG_F23).
3. `~/workspace/hackathon-plugin/new-skills/design-taste-frontend/references/hallmark/references/review-hero.md`
   — 2 insertions (Hero-moment row in inputs; hero-moment question).
4. `~/workspace/hackathon-plugin/fix23/apply-w3.py` (new) — inserts ONE
   runtime-patch block into build.sh before `# STEP 5 — Counts`
   (3 subs, all mode `after`).
5. `~/workspace/hackathon-plugin/fix23/orch-lines-w3.py` (new) —
   `ORCH_LINES_W3` constant for mechanical insertion into orchestrate
   step 3.
6. `~/workspace/hackathon-plugin/fix23/disposition-w3.md` (this file).

## Anchor verification (against the CURRENT built tree, before writing)

All runtime anchors verified count==1 by grep, then re-verified by
AST-extracting the exact strings from `apply-w3.py` and counting them in
the built files (read-only; the script itself was never executed):

| Sub | Anchor (head) | count | Token absent |
|---|---|---|---|
| FUNC-UIPRO_F23 | "Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit)." | 1 | yes |
| HERO-BQA_F23 | "Never claim visual verification without actually inspecting the rendered interface." | 1 | yes |
| FUNC-BQA_F23 | "4. Check dark mode if applicable" | 1 | yes |

`# STEP 5 — Counts` count==1 in build.sh; marker
`fix23-W3 upstream block applied` absent; fix22 block present (W3 block
sits after it). Generated block: 3 subs, all 5-tuples, mode `after`,
compiles OK; in-order simulation against the built tree applies cleanly
and all three tokens land. No banned terms in any new rule text (the only
banned-term strings in W3 files are the `BANNED` scanner tuple in
`apply-w3.py` itself, mirroring fix22.py).

**No anchor failed to resolve count==1. Nothing left unverified except
the items below.**

## Could not verify / open items for the coordinator

- `apply-w3.py` was NOT run (per task); the integration worker runs it
  (`--apply`). Its preflight re-verifies everything at run time.
- `orch-lines-w3.py` was NOT inserted into orchestrate SKILL.md (per
  task); the integration worker inserts `ORCH_LINES_W3` mechanically at
  the anchor in the file's docstring.
- The staged Taste edits reach the built tree only when build.sh runs
  (integration); the staged-vs-built diff was confirmed to be only the
  known frontmatter rewrite plus these edits.
- verify23.py / audit / sweep / dry-run are the coordinator's loops, not
  this worker's.
