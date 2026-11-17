# Dry-run #44 — Fix #29 (factory routing: ORCHESTRATOR-ONLY / FACTORY-DISPATCH / DIRECTOR-BRIEF / NO-GUESSING / VERIFY-MERGE / GLOBAL-ROUTING / COST-AWARE)

- **Date:** 2026-11-16 evening CST (Nov 17 ~02:00–03:30 UTC). Worker: dry-run #44 agent (fix #29), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix29/dryrun44/` (plus scratch under `fix29/dryrun44-scratch/`, cleaned at the end). No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run.
- **Verdict: DRY-RUN #44: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run passes all 17 §6 assertions at all 4 widths and all 13 states with 0 flags; the Campus Eats v5 benchmark passes 6 of 7 dimensions statically, with dimension 7 (alignment) OWED, never passed (no live Campus Eats render exists to measure). Leg 3: **59/59** — `qa.mjs` exits 0 twice on the rebuilt plugin with self-hosted template fonts, 12/12 stills rendered, 0 Google Fonts requests; the Playwright installer worked first try on the corrected command (see §3.2). Leg 4: 37/37 Cursor-readiness, incl. the 13 live C-1 hook pipe tests. Leg 5 (call-graph): 17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN against the fix28 map (unchanged, md5 `b066413a…`); the technical-depth fixture (real-time collaborative editor, sequence CRDT) re-run passes 11/11 automated checks + 6/6 live browser probe checks. Leg 6 (factory, the fix #29 leg): **27/27** — a 6-task queue across 4 skills exercised statically: partitions disjoint, all 6 briefs carry all 7 DIRECTOR-BRIEF fields, an unspecified decision returns NEEDS_CONTEXT, all 8 correction-brief construction sites name the failed criterion, retire-and-refill simulated with the Cursor harness gate recorded honestly, N=6 justified in one line.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,132 lines, md5 `c711c225022631286ffd1d7139bb5b19`**. (Was 24,119 / `06e3611b…` in #43; +13 lines = the fix29.py invocation block added after fix28's, per fix29/SPEC.md scope.)
- Counts verified: **67 skills / 45 agents / 48 rules / 55 commands / 15 hooks**, trigger keys **49** (from `manifests/context-packs/skill-triggers@1.json` `triggers` dict; `hooks.json` holds 15 events at `hackathon-ecc/hooks/hooks.json`). Counts unchanged by fix #29, as specified.
- verify29.py re-run this session: **315/315 checks pass, exit 0** (`fix29/dryrun44/verify29-rerun44.log`). Build log run 12 ends `build complete`, `fix29: 33 change(s)`, `fix29: OK`.
- Call map: `skills/orchestrate/references/call-map.md` md5 **`b066413a1a7dd6efcd8571c8abf93942`** — byte-identical to the fix28 map, as OWED-29-1 records (no new dispatch edges in fix #29); its counts table reads 67/45/48/55/15/49.
- `_F29` tokens (files carrying each, built tree excl. `node_modules`): ORCHESTRATOR-ONLY_F29 11, FACTORY-DISPATCH_F29 4, DIRECTOR-BRIEF_F29 7, NO-GUESSING_F29 9, VERIFY-MERGE_F29 6, GLOBAL-ROUTING_F29 18, COST-AWARE_F29 6 — matching sweep #38's census (GLOBAL-ROUTING_F29 24 occurrences in 18 files).
- Banned terms: raw grep over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` (excl. `node_modules`) returns **2 hits lowercase** — `skills/motionsites-web-builder/SKILL.md:25` and `:38` (upstream fetch URLs containing `Motionsites-AI/claude-skill`); with `grep -a`, a third hit appears at `skills/motionsites-web-builder/LICENSE:1` ("MotionSites Web Builder — Claude skill", capitalised). **3 hits total, all allow-listed MotionSites provenance, 0 unallowed.** (The plain-grep undercount of the LICENSE line is the same binary-handling quirk audit #93-A recorded: plain shell grep skips lines in this tree that `grep -a` finds.)
- Grok pins: `grok-4.7-high` ×**49**, `cursor-grok-4.6-high-fast` ×70, bare `grok-4.6-high-fast` ×0 (lookbehind grep). Down from #43's 50/70 by exactly one occurrence, **traced, not assumed**: `agents/ecc-gan-planner.md` went 3 → 2 — the removed third mention was the "invoke the design-lead (model `grok-4.7-high`)" clause in `:44`, deleted by the audit #83-A2 planner-fallback re-route (fix29.py §5f: the planner now stops and returns NEEDS_CONTEXT instead of invoking the design-lead). The pin itself is unchanged; the mention went with the removed instruction. Only the two allowed pin forms remain; bare count is still 0.
- Audit #94 / sweep #38 are parallel fix #29 workers, not re-run here.

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build tree: 42/42

Runner `dryrun44-fixtures.py` is a verbatim copy of `fix28/dryrun43/dryrun43-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun44-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #29 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun44-f23.py` is a verbatim copy of `fix28/dryrun43/dryrun43-f23.py`. Output: `dryrun44-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present.

**Adaptations: none.** (The leg5 runner's `MAP_PATH` still points at the fix28 map by design — see §5.)

## 2. Leg 2 — Home Run render re-run + Campus Eats v5 benchmark

### 2.1 Fix #29 touches no render files — verified, not assumed

- `fix29/fix29.py` and `fix29/SPEC.md` contain **zero** references to `cold-start-render`. The single `cold-start-render` hit in `build.sh` is the pre-existing fix #23 comment at `:23907` (the ALIGN_F23 block), not a fix #29 edit. No file under `fix29/` outside the `scratch-repo/` audit-trail history mentions `home-run` / `Home Run`.
- Render file mtimes predate fix #29: `index.html` Nov 13 02:46, `styles.css` Nov 13 03:00, `app.js` Nov 13 02:43, `qa/align-audit.mjs` Nov 13 03:00. (`qa/align-audit-results.json` was Nov 16 21:06 — dry-run #43's run — until this leg overwrote it; the prior file was preserved first at `fix29/dryrun44/prior-align-audit-results.json`.)

### 2.2 Render re-run (live, this session): all 17 assertions PASS, 0 flags

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`). Log: `fix29/dryrun44/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].** No interruption this run (unlike #43's mid-run service restart).
- Analysis `dryrun44-align.py` (output `dryrun44-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).
- All Chrome work ran with `TMPDIR=<dryrun44-scratch>/chrome-tmp` (`/tmp` was 62% full at session start).

| Assertion | Result | Measurement |
|---|---|---|
| (a) OVERFLOW — doc | PASS | `docOverflowX == 0` in 52/52 |
| (a) OVERFLOW — leaf text | PASS | 0 leaf text elements with `scrollWidth > clientWidth + 1` |
| (b) CENTER — phone frame | PASS | `viewportCenterOffset` 0 at all 52 (max \|offset\| 0) — incl. 900/768 stacked |
| (c) NAV — gaps / labels / bar | PASS | adjacent tab gaps equal ±2px in 52/52; every label center == tab center; tabbar centered in phone ±2px in 52/52 |
| (d) GRID — children + feed cards | PASS | full-width children share one left/right edge ±2px; narrower children left-aligned or centered, in 52/52; feed cards share one left/right edge per width |
| (e) CLIP — beyond frame | PASS | `.iris-disc` beyond the phone frame in 8 measurements (trip + trip-wrongcode × 4 widths); bleed DECLARED in the decision record |
| (f) LABELS — SVG / stamps / status | PASS | route-map + branch-strip: 0 overlaps, 0 out-of-bounds in 52/52; stamp offsets all 0 (n=12); statusbar insets symmetric; **status vertical centers delta 0 at 1440/900/390** (probe: time h=22 vs icons h=12 explains the 5px top difference) |
| (g) ACTIONS — code boxes | PASS | code-box group offset on its panel 0 in all 8 trip measurements |
| (h) PANELS — gutters | PASS | desktop gutters symmetric 44/44 in 13/13 at 1440 |
| (h) PANELS — tops | PASS | top delta **26px** at 1440, **stagger DECLARED in the decision record** (the dry-run #39 MINOR, cleared in #40, stays cleared) |
| COVER_F23 — matrix | PASS | required 39/39 cells present (1440/900/390 × 13 states); bonus width 768 also measured (52 total) |
| COVER_F23 — screenshots | PASS | a screenshot exists for every measured cell (54 shots) |

States covered at every width: home, home-bottom (scrolled), detail, offer, offer-accepted, trip, trip-wrongcode, trip-delivered, branches, trips, you, post, post-done. **No unverified width, no unverified flow state — no BLOCKING coverage gap.**

Fresh vs prior results JSON: identical except **2 measurements** (1440-trip-wrongcode and 390-trip-wrongcode), and only in the individual code-box input rects (8px shift at 1440, 1px at 390); the group geometry is identical in both (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #43 saw the same pattern in 4 measurements; #42 in 4; #41 in 4; #40 in 2; #39 in 3; #38 in 4.)

### 2.3 Campus Eats v5 benchmark — 6/7 static PASS, dimension 7 OWED

Full re-trace: `fix29/dryrun44/dryrun44-benchmark.md` (fresh verification of the v5 figures, rule traces, per-dimension table). Summary:

- **Benchmark file re-read this session** (178 lines, frozen at v5): kind sums re-added — literal 31+8+1+17+1+2+0+1 = **61**, stricter **60**; dynamic inventory 8 items, 1 drive, 2 surfaces, all as recorded.
- **Dynamic-count boundary re-derived** from `fix17/INVENTORY-V4.md` (#47–#50, #54 hover micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item for item, with the defensible range **6–13** (narrow/broad) unchanged.
- **Rule traces for the 7 re-trace additions re-checked in the fix29 built tree:** R1 (`design-taste-frontend/SKILL.md:409` — same line as #43; text unchanged), R4 (`fix15/SPEC.md:91`), CREATIVE_F25 (`feature-expansion/SKILL.md:59,93,99` — same lines as #43; anchor texts identical), E1, M3 (`make-interfaces-feel-better/SKILL.md:127` — same line as #43; anchor text identical). All hold. (Fix #29 touches none of these files; every anchor sits at the same line as #43.)
- **Re-trace: 68 literal / 66 stricter** (v5 61/60 + the same 7 rule-traced additions #67–#73). Kinds 7 → 8, five kinds above v5.

| # | Dimension | v5 | Re-trace | Result |
|---|---|---|---|---|
| 1 | Element count | 61 / 60 | **68 / 66** | **PASS** (≥ 62 / ≥ 61) |
| 2 | Variety | 7 kinds, Effect 0 | **8 kinds, 5 above v5**, no drops | **PASS** |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop | Full inventory **+ hero loop AND second moment applied** | **PASS (static)**; strength verdict OWED to browser-qa |
| 4 | Motion | 17 / 16 | **19 / 17** | **PASS** (≥ 18 / ≥ 17) |
| 5 | Dynamic interface | 8 items; 1 drive | **10 items; 2 drives** | **PASS (static)**; live behaviour OWED. Sensitivity: fails only under the narrow (6) reading |
| 6 | Functionality | 2 live-data surfaces | **3 surfaces**; mechanism on hero/first screen | **PASS (static)**; live verdict OWED (FUNC-BQA_F23) |
| 7 | Alignment | NONE RECORDED | **— cannot be scored** | **OWED, never passed** |

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7 is OWED.** `~/workspace/cold-start-render/campus-eats/` contains only `docs/design-tokens.md` (verified by listing this session) — no `index.html`, no CSS, no JS, no assets, so browser-qa cannot run the ALIGN_F23 matrix on it. Disposition per fix28/SPEC.md §7: RECORDED DECISION (owed, with the reason), not a pass. No Campus Eats render was built. The Home Run 52-measurement / 0-problem run is live alignment evidence about Home Run, not Campus Eats, and is not counted toward dimension 7.

**R1/R4 scope note (fix26/r1r4-note.md, verified this session):** the #67/#68 applications are paper re-trace additions, scored statically — NOT measurements of a live render. The Home Run render implements iris-opens in a different placement (trip code-panel reveal, `index.html:179–180`, `styles.css:433–446`, `app.js:192`) and implements no hero loop at all (zero `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval` hits across its `index.html`/`styles.css`/`app.js`; zero `loop` hits in its decision record). Fix #17 R1/R4 stay OWED as defined. The 6/7 re-trace result is unaffected: it never claimed a live verification of #67/#68.

## 3. Leg 3 — /demo: 59/59

Checker `dryrun44-demo.py` (verbatim copy of the #43 checker; output `dryrun44-demo-output.txt`): **59/59 /demo contract checks met, exit 0** — 35/35 original contract checks, 13/13 removal checks, 11/11 Remotion checks. The `qa.mjs` live check passes again.

### 3.1 The evidence (what actually ran, in order)

Fixture: `fix29/dryrun44/demo-sample-video/` — a **fresh copy of the rebuilt template** from the built tree (diffed against it: byte-identical except the fixture `shots.json`, the `package-lock.json` written by this run's `npm install`, and the live `src/frames.json` + `src/vo-durations.json`; the template's own `capture/` and `public/frames/` output dirs were not copied) + the Dry-run #37/38/39/40/41/42/43 `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block) + `fix29/dryrun44/sample-app/` (Pantry Pal, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards). Template facts in the copy: `package.json` carries `"@remotion/fonts": "4.0.526"` and **no** `@remotion/google-fonts`; `src/fonts.ts` uses `loadFont` + `staticFile('fonts/….woff2')`; `public/fonts/` holds exactly the 3 woff2 files. (`@remotion/google-fonts` still appears as a raw string 2× in `fonts.ts` — the intentional provenance header comment — and 1× in `mobile-ship` prose; zero imports, zero dependencies. That is the build worker's caveat 1, for the audit to decide; it is not a font fetch.)

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund`, cache in dryrun44 scratch (`npm-install.log`) | **exit 0**; `@remotion/fonts` present in `node_modules`, `@remotion/google-fonts` absent |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording | `node scripts/record.mjs` (`record-run.log`) | **exit 0. Take: 75.5s, 8 camera moves.** `capture/marks.json`: all 10 app beats + `__end`; **all 6 feature beats filmed**; `capture/out/take.webm` 3.6 MB. Playwright installer worked first try on the corrected command (see §3.2). |
| Frames | `node scripts/frames.mjs` (`frames-run.log`) | **exit 0. 2274 frames (75.8s).** (vs #43's 2281 / 76.0s — one frame of timing difference, not a defect.) |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 0 — TWICE.** First run exit 0; re-run (`qa-run2.log`, exit in `qa-exit2.txt`) exit 0 with a clean capture. **"No BLOCKING findings from the automated checks" in both logs. 12/12 stills rendered** (`out/qa/00111_problem.png` … `02408_close.png`) **+ 2 ffmpeg contact sheets. `grep -ci "fonts.googleapis\|fonts.gstatic" qa-run.log` → 0; same for the re-run log.** |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Gates | demo checker 35/35 + 13/13 | /demo callable only on explicit invocation, narration-key prompt only on a requested video, first-build order deploy → commit → README with no /demo, runtime **84.1s** from live `vo-durations.json` (under 130s hard / 150s absolute), $0 spent under the $10 cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37–#43. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run.

### 3.2 The Playwright installer worked first try — after one self-inflicted bad flag

This run's first installer invocation used an invalid flag (`npx playwright install chromium-headless-shell --with-deps=false`, exit 1, "unknown option") — my error, not installer flakiness. The corrected command `npx playwright install chromium-headless-shell` (with `PLAYWRIGHT_BROWSERS_PATH` under dryrun44-scratch) **exited 0 on the first attempt** (`pw-install.log`), downloading both the shell and ffmpeg into `dryrun44-scratch/pw-browsers/`. No curl recovery, no manual layout, no symlink needed. The installer flakiness dry-runs #37–#42 recorded remains environmental and intermittent; this run happened to get through (as did #43).

### 3.3 What is NOT claimed by the 59/59

- **No full render** (`build.mjs --render` / `npm run all` end-to-end) was run — the stills + contact sheets + A/V table are the verified output; a rendered `demo.mp4` is owed to the live smoke test.
- **The 10-second mix listen was not done** — the fixture has no music bed (`musicBed: false`) and no narration (no voice provider), so there is no mix to listen to. The A/V table (`demo-av-table.md`) is completed from the viewed stills: **all 12 beats' claims match what is on screen** (pantry list shows the six ingredients; week plan shows "6 dinners · $0 extra · 1 pot"; Monday curry 25 minutes; Tuesday chickpea rice 20 minutes; leftover remix; arch diagram shows "static HTML — no runtime code"; close card shows the serif "Pantry Pal" in the self-hosted Instrument Serif face).
- **Record warnings (minor, not BLOCKING):** `capture/marks.json` carries 2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped ("Execution context was destroyed, most likely because of a navigation"). The footage for both beats exists (marks present, stills render); only the mid-shot click actions did not execute — a navigation race in `record.mjs`, not a missing beat. Same warnings as #41/#42/#43. `qa.mjs` itself reports "No BLOCKING findings".
- A live film in Anish's Cursor is still owed by the smoke test, as before — but the sandbox side of it (fonts + recording + QA exit 0) is now proven here again.

## 4. Leg 4 — Cursor-readiness (fix #24): 37/37

Runner `dryrun44-leg4.py` (verbatim copy of the #43 runner, no expectation updates needed; output `dryrun44-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with the same file:line evidence as #43 (picker prerequisite verbatim once in orchestrate step 4; 4 dual-cited agent path lines; general-subagent fallback; all four /demo gates; resume guards; inventory pointers in Taste + ui-ux-pro-max; FILM_F1/F5/F6; F-09 step 6 wording; tts.mjs Windows forms; **13 live C-1 hook pipe tests**: 6 BLOCKED exit 2, 5 ALLOWED exit 0, 1 documented base64 GAP exit 0, 1 sanity BLOCKED exit 2).

## 5. Leg 5 — Call-graph: 17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN

Runner `dryrun44-leg5.py` (copy of the #43 runner with no adaptations needed this time; output `dryrun44-leg5-output.txt`, **exit 0**). It reads the fix28 map `fix28/callmap/call-map-data.json` (counts 67/45/48/55/15/49 — the map stands per OWED-29-1, since fix #29 adds no dispatch edges) and, for every element, either runs the dispatch path, resolves it statically, or records it dormant/owed. Outcome meanings as in #43. Nothing moved vs #43: fix #29 changed no counts and no dispatch edges.

| Category | Count | What was exercised / checked |
|---|---|---|
| Counts agree | 6 STATIC-OK | Map counts 67/45/48/55/15/49 all match the tree (skills dirs, agent files, `.mdc` rules, command files, `hooks.json` events, `skill-triggers@1.json` `triggers` dict) |
| Commands resolve | 55/55 STATIC-OK + 4 reviewed non-dispatch refs | Every command file's named skills/agents/commands resolve. The 4 reviewed refs (learn `skills/learned/` placeholder; react-review + save-session `/api` code paths; skill-create GitHub App) are non-dispatch mentions, verified by reading. (Same 4 as #43.) |
| Skills load | 67/67 STATIC-OK | Every skill has a non-empty `SKILL.md` with frontmatter; map skill keys == tree skill dirs. Live invocation of each on-request skill is OWED. |
| Hooks run live | **15/15 EXERCISED** | Every `hooks.json` event ran with synthetic Cursor-format JSON stdin (cwd = built tree, `HOME` = scratch fake-home, `TMPDIR` redirected): all exit 0 with valid JSON output. Includes `sessionStart` (see ck wire below) and `beforeShellExecution` (dispatches to the C-1 hook, already pipe-tested in Leg 4). |
| Fix #25 wires | 1 EXERCISED (ck) + 2 STATIC-OK + 1 EXERCISED (test-coverage) | **ck: EXERCISED** — `hooks/session-start.js` run on the REAL built tree with fake stdin `{}` and fake `$HOME`: exit 0, output JSON carries the full ck (Context Keeper) brief. **prp-commit: STATIC-OK** — Phase 3 + orchestrate step 6 name `git-workflow` + `ecc-commit-reviewer`; both resolve; live commit drafting OWED. **ecc-recipes: STATIC-OK** — the skill was CUT; the REROUTE_F27 replacement lookup is present in orchestrate :136; live lookup OWED. **/test-coverage Steps 1–2: EXERCISED** — see §5.1. |
| Uncalled | 17 DORMANT | 2 skills (`context-budget` — deliberately uncalled, the live usage meter; `vite-patterns` — uncalled since the fix #28 cut, see #43 §5), 9 agents, 6 commands — exactly the map; every one has zero calling invokers. (Same 17 as #43.) |
| Second-order orphans | 7 DORMANT | 3 agents, 4 commands (`harness-audit`, `python-review`, `skill-create`, `skill-health`) — exactly the map; every orphan's invokers resolve to uncalled elements or neutral reference files. (Same 7 as #43.) |
| Triggers | 49 STATIC-OK | All 49 keys resolve; no live Cursor entry point for the consumer (parent decision item, unchanged — fix #26 §5 records it documentation-only) — live firing OWED. |
| Epic commands | 0 — dropped | The 8 epic/`/prune` commands were DROPPED in fix #27 §1(b); no dormant-in-use set remains in the tree. |

**Paths exercised vs not executed vs owed (summary):** EXERCISED 17 (15 hooks + ck wire + /test-coverage measurement). NOT EXECUTED by decision 22 (17 uncalled + 7 second-order orphans, all with recorded dormant reasons; the epic commands no longer exist to be dormant-in-use) — the summary counts 5 DORMANT outcome lines (uncalled:count, uncalled:zero-invokers, second-order:count, second-order:invokers-uncalled, epic-dormant-in-use). OWED to the live smoke test: live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting via prp-commit, live recipes-lookup replacement (REROUTE_F27), live trigger firing, and live Cursor behaviour of the ck wire (the scratch + built-tree runs prove the Node mechanics only).

**No MINOR this run.** The dry-run #40 MINOR (`/loop-status` alias) was fixed in fix #25 option (b) and stays fixed: **0 `loop-status` hits** anywhere in the built tree (verified by grep this session).

**Runner adaptations for fix #29: none.** The #43 runner ran verbatim (its `MAP_PATH` already points at the fix28 map, which stands per OWED-29-1, and its uncalled expectation of 17 still holds).

### 5.1 /test-coverage Steps 1–2 exercised live

Scratch pytest project `leg5-testcov/` (verbatim copy of the #43 fixture; see `dryrun44-leg5-testcov.md`): `pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py` (5 tests, deliberately not covering `mul` or `untested_helper`). Ran the command's Step 1 detection + Step 2 measurement: `pytest --cov=src --cov-report=json`, **exit 0, 5 passed** — `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly as the wire specifies. Identical outcome to #40/#41/#42/#43. Step 3 generation stays in the fix loop by design and was not run. (One environment note: the first `pip install --target=~/…` put the libs somewhere unexpected; re-install with the absolute path worked — see §7.)

### 5.2 Technical-depth fixture: real-time collaborative editor — re-run PASS

Fixture: `fix29/dryrun44/leg5-collab/` (verbatim copy of the #43 fixture — `crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`). Re-run, not rebuilt: the CRDT, server, and demo are unchanged from #43.

- **Results: `test.mjs` 11/11 checks pass, exit 0; `probe.mjs` 6/6 live browser checks pass, exit 0** (type A→B, type B→A, offline divergence, offline merge, cross-collaborator undo, presence badge). Screenshot `demo-shot.png` re-taken by the probe run.
- **Budgets measured again:** keystroke → remote echo p95 4 ms (budget < 150 ms); 100-op burst local insert 1.5 ms / remote apply 0.2 ms (budget < 500 ms); 10,000-char document build 26.9 ms, merge 25.7 ms, converged. All within budget, same order as #43 (echo p95 3 ms there; 4 ms here is localhost timing noise, not a regression).
- No fixture defects found on re-run; nothing was changed in the fixture.

## 6. Leg 6 — Factory leg (the fix #29 leg): 27/27

Runner `dryrun44-leg6.py` (new for this dry run; output `dryrun44-leg6-output.txt`, **27/27 checks pass, exit 0**). The leg exercises the routing design **statically** — live Cursor per-model dispatch and slot refill at scale are harness-gated (OWED-29-2) and are NOT claimed as verified live. The script reads the routing text live from the built tree and asserts the sentences that do the work, then runs a 6-task sample queue through those rules as written. Full briefs: `dryrun44-leg6-briefs.md`.

### 6.1 The queue

Sample build "Pantry Pal v2" — 6 independent single-task jobs spanning **4 skills** (orch-pipeline, gan-style-harness, feature-expansion, design-taste-frontend redesign):

| Task | Skill | Work | Write set |
|---|---|---|---|
| T1 | orch-pipeline | Implement planWeek(): 6 dinners, $0 extra | `src/planner/week.ts` |
| T2 | orch-pipeline | Pantry inventory load + quantities | `src/pantry/inventory.ts` |
| T3 | gan-style-harness | Generator pass: WeekView component per spec | `src/ui/WeekView.tsx` |
| T4 | feature-expansion | Feature: leftover remix | `src/planner/remix.ts` |
| T5 | feature-expansion | Feature: cost tracker | `src/planner/cost.ts` |
| T6 | design-taste-frontend | Redesign /plan page (Hallmark flow) | `src/ui/PlanPage.tsx` |

Shared files (`src/planner/types.ts`, `gan-harness/spec.md`, `docs/design-tokens.md`, `src/ui/tokens.css`) are read-only / out of scope for every drone.

### (a) Partitioning — PASS

- Write sets are pairwise disjoint across all 6 tasks (shared = ∅, checked in the script).
- Shared files appear only as reads / out-of-scope, never in two write sets.
- Rule live in the tree: the GLOBAL-ROUTING golden block states work "is partitioned by file/module boundary so no two drones share files or mutable state".
- Redesign single-writer rule live: `redesign.md:68` lists the shared stylesheet/tokens files out of scope in every page brief and passes the tokens file read-only.

### (b) Brief completeness — PASS

- The contract names all seven DIRECTOR-BRIEF fields live: `dispatch-prompt.md:15` — Goal, Inputs, Constraints (incl. files out of scope), Interface, Acceptance check, Verification steps, Return format. `Interface:` is present in exactly 4 sections (recon / mechanical / reasoning / worked example — the 93-B2 fix, verified live).
- All **6 constructed briefs carry all 7 fields** (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return); every brief names files explicitly out of scope (incl. shared `tokens.css`).
- Incomplete-brief rule live: GLOBAL-ROUTING block — "an incomplete brief means the drone does not start".

### (c) No-guessing — PASS

- T5's brief deliberately leaves the **cost display format (currency symbol / decimals)** unspecified. Fed to the no-guessing rule, the drone returns **`NEEDS_CONTEXT`** naming it instead of guessing a format.
- Exact routing text traced (all read live from the built tree):
  - `agents/deep-reasoner.md:17`: "If the task is under-specified, return NEEDS_CONTEXT naming exactly what is missing — do not guess." (+ the NO-GUESSING bound + tie-breaker on the same line)
  - The carve-out sentence ("never to a decision the brief leaves unspecified") occurs **7× tree-wide**: the 5 Belief copies (`dispatch-prompt.md:34` + `:94` preamble, `orch-build-mvp:70`, `orch-pipeline:72`, `feature-expansion:151`) + 2 bounded quotations (`dispatch-prompt.md:149` reasoning template, `deep-reasoner.md:17`).
  - Tie-breaker live: "When in doubt which side an ambiguity falls on, return the question — a returned question is never a stall."
  - GLOBAL-ROUTING block: the drone "stops and returns the question to the orchestrator instead of guessing".
  - First-build carve-out reconciled: `dispatch-prompt.md` (5 sites) — NEEDS_CONTEXT goes to the orchestrator, "which resolves it by stated assumption" — never the user mid-build.
- **Script-expectation correction, recorded honestly:** the first run of the leg-6 script failed this check at 26/27 because the script asserted the carve-out sentence occurs 5× (one per Belief copy). The tree is correct: the sentence is quoted at 2 additional bounded sites, so the true count is 7. The script's expectation was corrected to 7 with the breakdown above; the re-run passes 27/27. No tree text was touched — the error was in the dry-run script, not the plugin.

### (d) Merge / verification — PASS (all 8 construction sites exercised)

Each site was fed a failing drone output; the script asserts the site's live sentence names the failed acceptance criterion and constructs the correction brief:

| # | Site | Failing input fed | Routing text (live) |
|---|---|---|---|
| 1 | orch-pipeline:74 (Phase 5 Review fix loop) | T1 returns 5 dinners, failing "planWeek() returns 6 dinners" | "the re-dispatch carries a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief" |
| 2 | feature-expansion:158 (fix loop) | T4 remix() returns no Wednesday dinner | Same construction sentence (capped at 2 rounds) |
| 3 | orchestrate:252 (escalation ladder) | fast-worker misses the acceptance check twice | Same construction sentence ("No third mechanical retry") |
| 4 | gan-build:30 (planner-spec check 3a) | Planner spec lacks per-feature acceptance criteria | "the planner is re-dispatched with a correction brief naming the failed criterion and the required correction … (at most two correction re-dispatches…)" |
| 5 | gan-build:63 (ORCHESTRATOR-CHECK) | T3 rubric 7.4 pass BUT WeekView lacks the 25-minute label | "A rubric pass with a failed acceptance criterion is a fail: the generator is re-dispatched with a correction brief naming the failed criterion…" |
| 6 | react-build:18 (step 6 Orchestrator Verify) | Resolver reports green build but with an unexplained `// @ts-ignore` | "On a failed criterion, re-dispatch the resolver with a correction brief naming the failed acceptance criterion… (at most two correction re-dispatches…)" |
| 7 | astra-review:35 (second blind pass) | Second blind pass finds a failed acceptance criterion in the fix | "On a failed criterion, re-dispatch the fixer with a correction brief naming the failed acceptance criterion… (at most two correction re-dispatches…)" |
| 8 | redesign.md:68 (page-drone verify) | T6 page output fails "matches recorded direction tokens" | "sends failed output back with a correction brief naming the failed acceptance criterion and the required correction, distinct from the original brief" |

Also verified live: gan-build.md wiring order **EVALUATE < ORCHESTRATOR-CHECK < CHECK SCORE** (the verify step gates the score, not just presence); "a rubric pass at or above 7.0 with a failed acceptance criterion is a fail"; the two-round correction cap is stated at ≥4 of the 8 sites; GLOBAL-ROUTING: "unverified drone output is never presented as the orchestrator's own".

### (e) Slot retire-and-refill — simulated, harness gate recorded honestly

- **Designed factory (per-completion refill):** with 4 slots and the 6-job queue, the simulation dispatches T1–T4, retires T1 on completion and dispatches T5 into the freed slot, retires T2 and dispatches T6, then retires T3–T6. All 6 jobs drain; retire order T1–T6. The mechanism as designed works on the queue.
- **Cursor reality (per-wave refill):** the same queue runs as waves — wave 1 T1–T4, wave 2 T5–T6, no mid-wave refill. The harness-gate clause ("in Cursor, slots refill per wave, not per completion — the factory lights up fully on the later port, not in Cursor") is present in **5/5 factory paragraphs** (orch-pipeline:62, feature-expansion:139, gan-style-harness:14, redesign.md:68, orchestrate step 4 at :93).
- **OWED-29-2, stated in the routing text itself:** "the factory lights up fully on the later port, not in Cursor". Live per-model dispatch and slot refill at scale are NOT claimed verified here — the factory lights up fully on the later port, and the live test (Anish, in Cursor, after fix #30) is where per-model dispatch is exercised.

### (f) COST-AWARE — PASS

- N=6 justified in **one line**: "Six disjoint file partitions (week.ts, inventory.ts, WeekView.tsx, remix.ts, cost.ts, PlanPage.tsx) justify N=6."
- Minimal context: each brief carries only its partition's files (write set == in-scope set for all 6 briefs; no whole-tree dump).
- Rule live: GLOBAL-ROUTING COST-AWARE_F29 — "the orchestrator justifies N>3 in one line".

## 7. Environment notes (sandbox, not the plugin)

- `/tmp` was **62% full (316 MB used, 197 MB free)** at session start. **No Chrome work used `/tmp`:** `TMPDIR` was redirected to `fix29/dryrun44-scratch/chrome-tmp` for every harness, probe, and Remotion run. Nothing crashed on shared memory.
- The Playwright browser install worked first try on the corrected command (see §3.2) — the CDN flakiness dry-runs #37–#42 recorded is intermittent, not gone.
- **No service restart interrupted this run** (unlike #43's killed align-harness attempt). No leg was interrupted by the environment.
- **Two self-inflicted incidents, both recovered, no impact on any leg:**
  - The first Playwright install used an invalid `--with-deps=false` flag (exit 1); the corrected command exited 0 (§3.2).
  - While stopping the Leg 3 sample-app server, `pkill -f "http.server 5180"` matched my own shell's command line and killed the shell (SIGTERM). The server (pid 98004) was then killed directly by pid; port 5180 confirmed dead afterwards.
  - The first `pip install --target=~/…/pylibs` for the Leg 5 test-coverage exercise reported success but the libs did not land at the expected path; re-install with the absolute path worked and the measurement used those libs. Cause not chased; no impact on the result.
- **Cleanup performed at the end:** deleted the reinstallable scratch bulk — `demo-sample-video/node_modules/` (753 MB), `demo-sample-video/public/frames/` (182 MB of 2,274 frame JPEGs — regenerable from `capture/out/take.webm` via `frames.mjs`; `src/frames.json` with the 2274 count kept), `dryrun44-scratch/npm-cache/` (97 MB), `dryrun44-scratch/pw-browsers/` (266 MB, the downloaded browser binary + ffmpeg), `dryrun44-scratch/pylibs/` (17 MB), `dryrun44-scratch/chrome-tmp/` contents, runner scratch `fake-home/`. Kept: all scripts, logs, reports, the fixture `shots.json` + `src/vo-durations.json` + `src/frames.json`, `capture/` (marks + take.webm + failures), `out/qa/` (12 stills + 2 sheets), the collab fixture sources + test/probe outputs + screenshot, and the Leg 5 test-coverage project + `coverage.json`. A repeat of Leg 3 needs one `npm install` and the Playwright install (or a retry of the installer). Total kept: 26 MB.
- No servers left running (ports 8323 and 5180 verified dead at the end).

## 8. OWED to the live smoke test — live-only items, never claimed verified

Carried from dry-run #43 §7, plus this run's additions:

- **Benchmark dimension 7 (alignment):** the Campus Eats re-trace cannot be alignment-scored without a live Campus Eats render + browser-qa run (§2.3). Closed as a RECORDED DECISION per fix28/SPEC.md §7, not a pass.
- **Fix #17 R1/R4:** OWED as defined (§2.3). The Home Run render applies iris-opens in a different placement and has no hero loop; a live Campus Eats render implementing #67/#68 would be needed, and none will be built (Anish's Nov 11 call).
- **Leg 6 live factory behavior (OWED-29-2):** per-model dispatch (DeepSeek/Qwen per task, fix #30) and slot refill at scale in Cursor. The dry-run factory leg verifies the design statically (27/27); live dispatch is harness-gated and lights up fully on the later port. The live test (Anish, in Cursor, after fix #30): the orchestrator runs a multi-part build and reports N drones, partitions, and verification outcomes.
- **Live `qa.mjs` exit-0 + live film + rendered `demo.mp4` in Anish's Cursor** (the sandbox side — fonts, recording, QA exit 0 — is now proven again; the Cursor side is not).
- **Measured (not estimated) narration runtime** and the **10-second mix listen** (no voice provider, no bed in the sandbox).
- **Live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting, live REROUTE_F27 lookup, live trigger firing, live Cursor behaviour of the ck wire** (§5).
- Prior open items carried forward: D-6 Stop/SessionStart contradiction; C-5 timeout-300 unit; C-6 hook cwd/node/event names; D-9 `.ecc/settings.json` pickup; E-7 gate hook without Git Bash; general-subagent fallback pin behaviour; F-14 post-report /demo stale README (fixed in fix #26 per `fix26/f14-note.md` — the dry-run does not re-verify the fix itself, only that Leg 3's gates still hold); Netlify row touch-up after Dec 4, 2026; fresh bundle needed before any push.

## 9. Observations for the audit (not leg failures)

- **`hackathon-ecc/README.md:67-68` still lists the dropped `/epic-*` commands as shipping** ("The plugin's Node scripts (`/harness-audit`, the `/epic-*` commands, `validate-skills.js`) ship with their dependencies vendored…"). Stale prose from the fix #27 cut, carried into the fix #29 tree unchanged — the commands no longer exist. Likewise orchestrate :136's REROUTE note still names the epic commands as machinery a build must not dispatch (prose-history, Audit #76 B3). Neither dispatches anything, so neither fails a leg; both are doc staleness for the fix to note. (Same observation as dry-run #42 §5 and #43 §8 — re-verified live this session.)
- **Grok pin count 50 → 49 is a documented fix #29 change, not a regression** (§0): the lost mention is the removed "invoke the design-lead (model `grok-4.7-high`)" clause in `ecc-gan-planner.md:44` (audit #83-A2). No model pin changed.

## 10. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression + fix #23) | 101 | **PASS (101/101)** |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | **PASS on all 17 assertions, 0 flags** |
| 2 — Campus Eats v5 benchmark | 7 dimensions | **6 PASS statically; dimension 7 (alignment) OWED** |
| 3 — /demo gates + Remotion | 59 | **PASS (59/59) — qa.mjs exit 0 twice, 12/12 stills, 0 font requests; Playwright installer worked first try on the corrected command** |
| 4 — Cursor-readiness (fix #24) | 37 | **PASS (37/37)**, incl. 13 live C-1 hook pipe tests |
| 5 — Call-graph | 41 checks | **17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN** (fix28 map stands; uncalled 17, second-order 7) |
| 5 — Technical depth (collab editor, re-run) | 11 automated + 6 live | **PASS (11/11 + 6/6)**, budgets measured (echo p95 4 ms < 150 ms; burst < 2 ms < 500 ms; 10k doc merged in 25.7 ms) |
| 5 — /test-coverage Steps 1–2 | 1 exercise | **EXERCISED** (calc.py 68.2%, listed below 80%) |
| 6 — Factory (fix #29 leg) | 27 checks | **PASS (27/27)** — 6 tasks / 4 skills; partitions disjoint; 6/6 briefs 7/7 fields; NEEDS_CONTEXT on the unspecified decision; 8/8 correction-brief sites name the failed criterion; refill simulated with the Cursor harness gate recorded; N=6 justified in one line |

**DRY-RUN #44: PASS** — with benchmark dimension 7 owed (§2.3), fix #17 R1/R4 owed as defined (§2.3), and live factory behavior owed per OWED-29-2 (§6(e)). No BLOCKING finding in any leg. The only first-run non-pass was in the dry-run's own Leg 6 script (a wrong count expectation, 5 vs the true 7 carve-out occurrences — §6(c)); the tree was correct and the corrected script passes 27/27. Two observations for the audit, not leg failures: README.md:67-68 still lists the dropped `/epic-*` commands as shipping (§9), and the Grok pin count moved 50 → 49 via the documented #83-A2 re-route (§0/§9).

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-report.md` (this report)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-fixtures.py` + `dryrun44-fixtures-output.txt` (42/42)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-f23.py` + `dryrun44-f23-output.txt` (59/59)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-align.py` + `dryrun44-align-output.txt` (17 PASS, 0 flags) + `status-center-probe.mjs` + `status-center-probe-output.txt` (centers delta 0) + `align-run.log` (52 measurements, 0 console errors, 0 failed requests) + `prior-align-audit-results.json`
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-benchmark.md` (v5 re-trace: 68/66, per-dimension table, dynamic-count re-derivation with the 6–13 range, Dim 7 owed, R1/R4 scope note)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-demo.py` + `dryrun44-demo-output.txt` (59/59) + `demo-av-table.md` (12/12 beats verified from stills; mix listen unexecuted)
- `~/workspace/hackathon-plugin/fix29/dryrun44/sample-app/` + `demo-sample-video/` (fresh built-template copy + fixture `shots.json` + live `src/vo-durations.json` + `src/frames.json`; `capture/` with marks + take.webm + failures; `out/qa/` with 12 stills + 2 sheets; `node_modules/` + `public/frames/` removed in cleanup — see §7) + `npm-install.log`, `tts-run.log`, `record-run.log`, `frames-run.log`, `qa-run.log`, `qa-run2.log`, `qa-exit.txt`, `qa-exit2.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `pw-install.log`
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-leg4.py` + `dryrun44-leg4-output.txt` (37/37; verbatim, no expectation updates needed)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-leg5.py` + `dryrun44-leg5-output.txt` (17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN; exit 0; no adaptations needed — fix28 map stands) + `leg5-testcov/` + `coverage.json` + `leg5-testcov-run.log` + `dryrun44-leg5-testcov.md`
- `~/workspace/hackathon-plugin/fix29/dryrun44/leg5-collab/` (`crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`, `demo-shot.png`) + `leg5-collab-test-output.txt` (11/11) + `leg5-collab-probe-output.txt` (6/6)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-leg6.py` + `dryrun44-leg6-output.txt` (27/27; exit 0) + `dryrun44-leg6-briefs.md` (the 6 constructed director briefs + COST-AWARE line)
- `~/workspace/hackathon-plugin/fix29/dryrun44/verify29-rerun44.log` (verify29 re-run this session: 315/315, exit 0)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-report.md` + fixture/demo scripts (Dry-run #43 lists reused verbatim except the documented Leg 6 addition and the Leg 5 test-coverage re-run)
- `build.sh` measured this session: **24,132 lines, md5 `c711c225022631286ffd1d7139bb5b19`**; counts **67/45/48/55/15**, triggers **49**; banned terms **3 hits, all allow-listed MotionSites, 0 unallowed** (LICENSE hit needs `grep -a`); Grok pins 49/70, bare 0 (delta from 50/70 traced to the #83-A2 planner re-route); call map md5 `b066413a1a7dd6efcd8571c8abf93942`; verify29 re-run **315/315**
