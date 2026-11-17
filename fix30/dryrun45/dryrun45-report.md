# Dry-run #45 — Fix #30 (orchestrator pin: grok-4.7-high → grok-4.7-extra-high)

- **Date:** 2026-11-16 evening CST (Nov 17 ~03:00–04:30 UTC). Worker: dry-run #45 agent (fix #30), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix30/dryrun45/` (plus scratch under `fix30/dryrun45-scratch/`, cleaned at the end). No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run. `build.sh` never run (build run 2 already completed, exit 0, `fix30/build-log-run2.txt`).
- **Verdict: DRY-RUN #45: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run passes all 17 §6 assertions at all 4 widths and all 13 states with 0 flags; the Campus Eats v5 benchmark passes 6 of 7 dimensions statically, with dimension 7 (alignment) OWED, never passed (no live Campus Eats render exists to measure). Leg 3: **59/59** — `qa.mjs` exits 0 twice on the rebuilt plugin with self-hosted template fonts, 12/12 stills rendered, 0 Google Fonts requests; the Playwright installer worked first try. Leg 4: 37/37 Cursor-readiness, incl. the 13 live C-1 hook pipe tests. Leg 5 (call-graph): 17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN against the fix28 map (unchanged, md5 `b066413a…`); the technical-depth fixture (real-time collaborative editor, sequence CRDT) re-run passes 11/11 automated checks + 6/6 live browser probe checks. Leg 6 (factory, the fix #29 leg): **27/27** — a 6-task queue across 4 skills exercised statically: partitions disjoint, all 6 briefs carry all 7 DIRECTOR-BRIEF fields, an unspecified decision returns NEEDS_CONTEXT, all 8 correction-brief construction sites name the failed criterion, retire-and-refill simulated with the Cursor harness gate recorded honestly, N=6 justified in one line. Leg 7 (NEW, the fix #30 pin leg): **32/32** — the orchestrator pin resolves to `grok-4.7-extra-high` end to end in a simulated sample build: route table, orchestrate routing table, schema enum (the new pin validates, the old pin does not), all 45 agent frontmatter pins in-enum, fast-worker pin intact at 70, old pin x0 everywhere in the trace and tree-wide. Static only — no live Cursor session; the live test is Anish's `fix30/live-test-prompt.md`, out of scope here.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,144 lines, md5 `4179be09c9e050b34ae70763f6ad0b15`**. (Was 24,132 / `c711c225…` in #44; +12 lines = the fix30.py invocation block added after fix29's, per fix30/SPEC.md scope.)
- Counts verified: **67 skills / 45 agents / 48 rules / 55 commands / 15 hooks**, trigger keys **49** (from `manifests/context-packs/skill-triggers@1.json` `triggers` dict; `hooks.json` holds 15 events under its `hooks` key). Counts unchanged by fix #30, as specified.
- verify30.py re-run this session: **318/318 checks pass, exit 0** (`fix30/dryrun45/verify30-rerun45.log`). Build log run 2 ends `build complete`, `fix30: OK`.
- Call map: `skills/orchestrate/references/call-map.md` md5 **`b066413a1a7dd6efcd8571c8abf93942`** — byte-identical to the fix28 map, as OWED-30-4 records (no new dispatch edges in fix #30); its counts table reads 67/45/48/55/15/49.
- Grok pins (built tree, excl. `node_modules`): **`grok-4.7-extra-high` ×49, `grok-4.7-high` ×0, `Grok 4.7 Extra High` ×22, `Grok 4.7 High` ×0, `cursor-grok-4.6-high-fast` ×70, bare `grok-4.6-high-fast` ×0** — exactly the SPEC counts. The rename is complete; the fast-worker pin is untouched.
- Banned terms: raw grep over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` (excl. `node_modules`) returns **2 hits lowercase** — `skills/motionsites-web-builder/SKILL.md:25` and `:38` (upstream fetch URLs containing `Motionsites-AI/claude-skill`); with `grep -a`, a third hit appears at `skills/motionsites-web-builder/LICENSE:1` ("MotionSites Web Builder — Claude skill", capitalised). **3 hits total, all allow-listed MotionSites provenance, 0 unallowed.** (Same binary-handling quirk audit #93-A recorded: plain shell grep skips lines in this tree that `grep -a` finds.)
- Audit #95 / sweep #39 are parallel fix #30 workers, not re-run here.

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build tree: 42/42

Runner `dryrun45-fixtures.py` is a verbatim copy of `fix29/dryrun44/dryrun44-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun45-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #30 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun45-f23.py` is a verbatim copy of `fix29/dryrun44/dryrun44-f23.py`. Output: `dryrun45-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present.

**Adaptations: one, in the Leg 4 runner only (§4).** The Leg 6 runner needed one path repair (§6): my copy sed replaced the legitimate cross-reference `fix29/global-routing-block.txt` with `dryrun45/global-routing-block.txt`; restored to the fix29 path (the GLOBAL-ROUTING block is a fix29 artifact, unchanged in #30). No other runner needed adaptation. (The leg5 runner's `MAP_PATH` still points at the fix28 map by design — see §5.)

## 2. Leg 2 — Home Run render re-run + Campus Eats v5 benchmark

### 2.1 Fix #30 touches no render files — verified, not assumed

- `fix30/fix30.py` and `fix30/SPEC.md` contain **zero** references to `cold-start-render`. The single `cold-start-render` hit in `build.sh` is the pre-existing fix #23 comment at `:23907` (the ALIGN_F23 block), not a fix #30 edit. No file under `fix30/` outside the `scratch-repo/` audit-trail history mentions `home-run` / `Home Run`.
- Render file mtimes predate fix #30: `index.html` Nov 13 02:46, `styles.css` Nov 13 03:00, `app.js` Nov 13 02:43, `qa/align-audit.mjs` Nov 13 03:00. (`qa/align-audit-results.json` was Nov 16 21:06 — dry-run #44's run — until this leg overwrote it; the prior file was preserved first at `fix30/dryrun45/prior-align-audit-results.json`.)
- One path correction, recorded: the render lives at `~/workspace/cold-start-render/home-run/`, not under the plugin tree — the first preserve attempt used the wrong base path and failed; the retry from the correct path succeeded before the harness ran.

### 2.2 Render re-run (live, this session): all 17 assertions PASS, 0 flags

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`). Log: `fix30/dryrun45/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].** No interruption this run.
- Analysis `dryrun45-align.py` (output `dryrun45-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).
- All Chrome work ran with `TMPDIR=<dryrun45-scratch>/chrome-tmp` (`/tmp` was 62% full at session start).

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

Fresh vs prior results JSON: identical except **2 measurements** (1440-trip-wrongcode and 390-trip-wrongcode), and only in the individual code-box input rects (7px shift at 1440, 1px at 390); the group geometry is identical in both (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #44 saw the same pattern in 2 measurements; #43 in 4; #42 in 4; #41 in 4; #40 in 2; #39 in 3; #38 in 4.)

### 2.3 Campus Eats v5 benchmark — 6/7 static PASS, dimension 7 OWED

Full re-trace: `fix30/dryrun45/dryrun45-benchmark.md` (fresh verification of the v5 figures, rule traces, per-dimension table). Summary:

- **Benchmark file re-read this session** (178 lines, frozen at v5): kind sums re-added — literal 31+8+1+17+1+2+0+1 = **61**, stricter **60**; dynamic inventory 8 items, 1 drive, 2 surfaces, all as recorded.
- **Dynamic-count boundary re-derived** from `fix17/INVENTORY-V4.md` (#47–#50, #54 hover micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item for item, with the defensible range **6–13** (narrow/broad) unchanged.
- **Rule traces for the 7 re-trace additions re-checked in the fix30 built tree:** R1 (`design-taste-frontend/SKILL.md:409` — same line as #43/#44; text unchanged), R4 (`fix15/SPEC.md:91`), CREATIVE_F25 (`feature-expansion/SKILL.md:59,93,99` — same lines as #43/#44; anchor texts identical), E1, M3 (`make-interfaces-feel-better/SKILL.md:127` — same line as #43/#44; anchor text identical). All hold. (Fix #30 touches none of these files; every anchor sits at the same line as #44.)
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

Checker `dryrun45-demo.py` (verbatim copy of the #44 checker; output `dryrun45-demo-output.txt`): **59/59 /demo contract checks met, exit 0** — 35/35 original contract checks, 13/13 removal checks, 11/11 Remotion checks. The `qa.mjs` live check passes again.

### 3.1 The evidence (what actually ran, in order)

Fixture: `fix30/dryrun45/demo-sample-video/` — a **fresh copy of the rebuilt template** from the built tree (diffed against it: byte-identical except the fixture `shots.json`, the `package-lock.json` written by this run's `npm install`, and the live `src/frames.json` + `src/vo-durations.json`; the template's own `capture/` and `public/frames/` output dirs were not copied) + the Dry-run #37/38/39/40/41/42/43/44 `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block) + `fix30/dryrun45/sample-app/` (Pantry Pal, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards). Template facts in the copy: `package.json` carries `"@remotion/fonts": "4.0.526"` and **no** `@remotion/google-fonts`; `src/fonts.ts` uses `loadFont` + `staticFile('fonts/….woff2')`; `public/fonts/` holds exactly the 3 woff2 files. (`@remotion/google-fonts` still appears as a raw string 2× in `fonts.ts` — the intentional provenance header comment — and 1× in `mobile-ship` prose; zero imports, zero dependencies. That is the build worker's caveat 1, for the audit to decide; it is not a font fetch.)

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund`, cache in dryrun45 scratch (`npm-install.log`) | **exit 0**; `@remotion/fonts` present in `node_modules`, `@remotion/google-fonts` absent |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording | `node scripts/record.mjs` (`record-run.log`) | **exit 0. Take: 75.4s, 8 camera moves.** `capture/marks.json`: all 9 app beats + `__end` (10 marks; the other 3 beats are cards, not filmed footage); **all 6 feature beats filmed**; `capture/out/take.webm` 3.6 MB. Playwright installer worked first try (see §3.2). |
| Frames | `node scripts/frames.mjs` (`frames-run.log`) | **exit 0. 2281 frames (76.0s).** (vs #44's 2274 / 75.8s — seven frames of timing difference, not a defect.) |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 0 — TWICE.** First run exit 0; re-run (`qa-run2.log`, exit in `qa-exit2.txt`) exit 0 with a clean capture. **"No BLOCKING findings from the automated checks" in both logs. 12/12 stills rendered** (`out/qa/00111_problem.png` … `02408_close.png`) **+ 2 ffmpeg contact sheets. `grep -ci "fonts.googleapis\|fonts.gstatic" qa-run.log` → 0; same for the re-run log.** |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Gates | demo checker 35/35 + 13/13 | /demo callable only on explicit invocation, narration-key prompt only on a requested video, first-build order deploy → commit → README with no /demo, runtime **84.1s** from live `vo-durations.json` (under 130s hard / 150s absolute), $0 spent under the $10 cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37–#44. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run.

### 3.2 The Playwright installer worked first try

`npx playwright install chromium-headless-shell` (with `PLAYWRIGHT_BROWSERS_PATH` under dryrun45-scratch) **exited 0 on the first attempt** (`pw-install.log`), downloading both the shell and ffmpeg into `dryrun45-scratch/pw-browsers/`. No curl recovery, no manual layout, no symlink needed. The installer flakiness dry-runs #37–#42 recorded remains environmental and intermittent; this run happened to get through (as did #43/#44).

### 3.3 What is NOT claimed by the 59/59

- **No full render** (`build.mjs --render` / `npm run all` end-to-end) was run — the stills + contact sheets + A/V table are the verified output; a rendered `demo.mp4` is owed to the live smoke test.
- **The 10-second mix listen was not done** — the fixture has no music bed (`musicBed: false`) and no narration (no voice provider), so there is no mix to listen to. The A/V table (`demo-av-table.md`) is completed from the viewed stills: **all 12 beats' claims match what is on screen** (pantry list shows the six ingredients; week plan shows "6 dinners · $0 extra · 1 pot"; Monday curry 25 minutes; Tuesday chickpea rice 20 minutes; leftover remix; arch diagram shows "static HTML — no runtime code"; close card shows the serif "Pantry Pal" in the self-hosted Instrument Serif face).
- **Record warnings (minor, not BLOCKING):** `capture/marks.json` carries 2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped ("Execution context was destroyed, most likely because of a navigation"). The footage for both beats exists (marks present, stills render); only the mid-shot click actions did not execute — a navigation race in `record.mjs`, not a missing beat. Same warnings as #41/#42/#43/#44. `qa.mjs` itself reports "No BLOCKING findings".
- A live film in Anish's Cursor is still owed by the smoke test, as before — but the sandbox side of it (fonts + recording + QA exit 0) is now proven here again.

## 4. Leg 4 — Cursor-readiness (fix #24): 37/37

Runner `dryrun45-leg4.py` (output `dryrun45-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with the same file:line evidence as #44 (4 dual-cited agent path lines; general-subagent fallback; all four /demo gates; resume guards; inventory pointers in Taste + ui-ux-pro-max; FILM_F1/F5/F6; F-09 step 6 wording; tts.mjs Windows forms; **13 live C-1 hook pipe tests**: 6 BLOCKED exit 2, 5 ALLOWED exit 0, 1 documented base64 GAP exit 0, 1 sanity BLOCKED exit 2).

**One script-expectation update, tree verified correct first (same class as #44 §6(c)):** the first run came back 36/37 on L4-1a — the runner's verbatim picker sentence still said "Select **Grok 4.7 High** in Cursor's model picker before the first build", but fix30.py renamed that sentence to "Grok 4.7 Extra High" (prose x22). Before touching the runner I verified the tree: the new verbatim occurs exactly 1× in orchestrate SKILL.md, and "Grok 4.7 High" occurs 0× tree-wide. The `verb` expectation was updated to the Extra High wording; the re-run passes 37/37. No tree text was touched — the error was in the dry-run script, not the plugin.

## 5. Leg 5 — Call-graph: 17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN

Runner `dryrun45-leg5.py` (copy of the #44 runner with the one path repair noted in §1; output `dryrun45-leg5-output.txt`, **exit 0**). It reads the fix28 map `fix28/callmap/call-map-data.json` (counts 67/45/48/55/15/49 — the map stands per OWED-30-4, since fix #30 adds no dispatch edges) and, for every element, either runs the dispatch path, resolves it statically, or records it dormant/owed. Outcome meanings as in #44. Nothing moved vs #44: fix #30 changed no counts and no dispatch edges.

| Category | Count | What was exercised / checked |
|---|---|---|
| Counts agree | 6 STATIC-OK | Map counts 67/45/48/55/15/49 all match the tree (skills dirs, agent files, `.mdc` rules, command files, `hooks.json` events, `skill-triggers@1.json` `triggers` dict) |
| Commands resolve | 55/55 STATIC-OK + 4 reviewed non-dispatch refs | Every command file's named skills/agents/commands resolve. The 4 reviewed refs (learn `skills/learned/` placeholder; react-review + save-session `/api` code paths; skill-create GitHub App) are non-dispatch mentions, verified by reading. (Same 4 as #44.) |
| Skills load | 67/67 STATIC-OK | Every skill has a non-empty `SKILL.md` with frontmatter; map skill keys == tree skill dirs. Live invocation of each on-request skill is OWED. |
| Hooks run live | **15/15 EXERCISED** | Every `hooks.json` event ran with synthetic Cursor-format JSON stdin (cwd = built tree, `HOME` = scratch fake-home, `TMPDIR` redirected): all exit 0 with valid JSON output. Includes `sessionStart` (see ck wire below) and `beforeShellExecution` (dispatches to the C-1 hook, already pipe-tested in Leg 4). |
| Fix #25 wires | 1 EXERCISED (ck) + 2 STATIC-OK + 1 EXERCISED (test-coverage) | **ck: EXERCISED** — `hooks/session-start.js` run on the REAL built tree with fake stdin `{}` and fake `$HOME`: exit 0, output JSON carries the full ck (Context Keeper) brief. **prp-commit: STATIC-OK** — Phase 3 + orchestrate step 6 name `git-workflow` + `ecc-commit-reviewer`; both resolve; live commit drafting OWED. **ecc-recipes: STATIC-OK** — the skill was CUT; the REROUTE_F27 replacement lookup is present in orchestrate :136; live lookup OWED. **/test-coverage Steps 1–2: EXERCISED** — see §5.1. |
| Uncalled | 17 DORMANT | 2 skills (`context-budget` — deliberately uncalled, the live usage meter; `vite-patterns` — uncalled since the fix #28 cut, see #43 §5), 9 agents, 6 commands — exactly the map; every one has zero calling invokers. (Same 17 as #44.) |
| Second-order orphans | 7 DORMANT | 3 agents, 4 commands (`harness-audit`, `python-review`, `skill-create`, `skill-health`) — exactly the map; every orphan's invokers resolve to uncalled elements or neutral reference files. (Same 7 as #44.) |
| Triggers | 49 STATIC-OK | All 49 keys resolve; no live Cursor entry point for the consumer (parent decision item, unchanged — fix #26 §5 records it documentation-only) — live firing OWED. |
| Epic commands | 0 — dropped | The 8 epic/`/prune` commands were DROPPED in fix #27 §1(b); no dormant-in-use set remains in the tree. |

**Paths exercised vs not executed vs owed (summary):** EXERCISED 17 (15 hooks + ck wire + /test-coverage measurement). NOT EXECUTED by decision 22 (17 uncalled + 7 second-order orphans, all with recorded dormant reasons; the epic commands no longer exist to be dormant-in-use) — the summary counts 5 DORMANT outcome lines (uncalled:count, uncalled:zero-invokers, second-order:count, second-order:invokers-uncalled, epic-dormant-in-use). OWED to the live smoke test: live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting via prp-commit, live recipes-lookup replacement (REROUTE_F27), live trigger firing, and live Cursor behaviour of the ck wire (the scratch + built-tree runs prove the Node mechanics only).

**No MINOR this run.** The dry-run #40 MINOR (`/loop-status` alias) was fixed in fix #25 option (b) and stays fixed: **0 `loop-status` hits** anywhere in the built tree (verified by grep this session).

**Runner adaptations for fix #30: one path repair only** (see §1 — the `fix29/global-routing-block.txt` cross-reference). The #44 runner otherwise ran verbatim (its `MAP_PATH` already points at the fix28 map, which stands per OWED-30-4, and its uncalled expectation of 17 still holds).

### 5.1 /test-coverage Steps 1–2 exercised live

Scratch pytest project `leg5-testcov/` (verbatim copy of the #44 fixture; see `dryrun45-leg5-testcov.md`): `pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py` (5 tests, deliberately not covering `mul` or `untested_helper`). Ran the command's Step 1 detection + Step 2 measurement: `pytest --cov=src --cov-report=json`, **exit 0, 5 passed** — `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly as the wire specifies. Identical outcome to #40/#41/#42/#43/#44. Step 3 generation stays in the fix loop by design and was not run. (One environment note: the copied fixture carried a stray `~` directory from #44's first pip-install incident — a literal-tilde `--target` artifact — removed before the run; the fresh install with the absolute path worked first try. No impact on the measurement.)

### 5.2 Technical-depth fixture: real-time collaborative editor — re-run PASS

Fixture: `fix30/dryrun45/leg5-collab/` (verbatim copy of the #44 fixture — `crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`). Re-run, not rebuilt: the CRDT, server, and demo are unchanged from #44.

- **Results: `test.mjs` 11/11 checks pass, exit 0; `probe.mjs` 6/6 live browser checks pass, exit 0** (type A→B, type B→A, offline divergence, offline merge, cross-collaborator undo, presence badge). Screenshot `demo-shot.png` re-taken by the probe run.
- **Budgets measured again:** keystroke → remote echo p95 **58 ms** (budget < 150 ms); 100-op burst local insert 2.2 ms / remote apply 0.5 ms (budget < 500 ms); 10,000-char document build 299.0 ms, merge 62.3 ms, converged. All within budget. (The echo p95 and doc-build times are slower than #44's 4 ms / 26.9 ms — the probe ran while `frames.mjs` was rendering 2,281 frames concurrently on 1.5 shared CPUs, so this is CPU contention, not a regression; nothing exceeds its budget and every check passes.)
- No fixture defects found on re-run; nothing was changed in the fixture.

## 6. Leg 6 — Factory leg (the fix #29 leg, re-run): 27/27

Runner `dryrun45-leg6.py` (output `dryrun45-leg6-output.txt`, **27/27 checks pass, exit 0**). The leg exercises the routing design **statically** — live Cursor per-model dispatch and slot refill at scale are harness-gated (OWED-29-2) and are NOT claimed as verified live. The script reads the routing text live from the built tree and asserts the sentences that do the work, then runs a 6-task sample queue through those rules as written. Full briefs: `dryrun45-leg6-briefs.md` (body identical to #44's — same queue, same routing text).

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

## 7. Leg 7 — Pin leg (NEW, the fix #30 leg): 32/32

Runner `dryrun45-leg7.py` (new for this dry run; output `dryrun45-leg7-output.txt`, **32/32 checks pass, exit 0**). The leg traces the orchestrator pin end to end in a **simulated** sample build (the Leg 6 Pantry Pal v2 queue, 6 tasks / 4 skills) through the routing text live in the built tree. **This leg is static: no live Cursor session exists in this sandbox, so nothing here claims the pin holds at runtime in Cursor.** The live test is Anish's `fix30/live-test-prompt.md` (out of scope here); per the patch log (OWED-30-3), live Extra High behavior is unverified until he runs it.

### 7a. Model-route table — PASS

`commands/model-route.md`: the mechanical row resolves to `cursor-grok-4.6-high-fast`; the default row ("default for implementation and refactors") and the architecture row ("architecture, deep review, ambiguous requirements") both resolve to `grok-4.7-extra-high`; the file names the old pin 0× (ID and prose).

### 7b. Schema enum — PASS

- `schemas/agent.schema.json` model enum is exactly `["cursor-grok-4.6-high-fast", "grok-4.7-extra-high"]`.
- **The new pin validates** (`grok-4.7-extra-high` ∈ enum); **the old pin does NOT validate** (`grok-4.7-high` ∉ enum — a doc pinning it fails validation). The schema file contains no old-prose mention.
- **45/45 agent files carry a `model:` frontmatter line, and all 45 values are in the enum.** Exactly **4 agents pin `grok-4.7-extra-high`**: `deep-reasoner.md`, `ecc-architect.md`, `ecc-healthcare-reviewer.md`, `ecc-spec-miner.md`. The other **41 pin `cursor-grok-4.6-high-fast`**; 41 + 4 = 45.

### 7c. Orchestrate routing table — PASS

- Orchestrator row → `grok-4.7-extra-high` (`:24`); deep-reasoner row → `grok-4.7-extra-high` (`:25`); design-lead row → `grok-4.7-extra-high` (`:28`); implementation tier row → `cursor-grok-4.6-high-fast` (`:29`).
- Fallback paragraph (`:244`) pins each tier by slug: deep-reasoner `grok-4.7-extra-high`, fast-worker `cursor-grok-4.6-high-fast`, scout `cursor-grok-4.6-high-fast`, design-lead `grok-4.7-extra-high` (slug form only).
- MODEL-PIN ledger line (`:62`) records `MODEL-PIN: grok-4.7-extra-high | other: <name>`; the picker sentence names Grok 4.7 Extra High exactly once; the model hierarchy (`:31`) states "Grok 4.7 Extra High decides, Grok 4.6 High executes" and that the orchestrator, design-lead, deep-reasoner, and every big-decision role run on Grok 4.7 Extra High.
- `orchestrate/SKILL.md` names the old pin 0×.

### 7d. Simulated dispatch trace — PASS

All 14 simulated steps resolve to a schema-enum model:

| Step | Role | Resolves to |
|---|---|---|
| S0 grill-me + planning | orchestrator | `grok-4.7-extra-high` |
| S0 MODEL-PIN ledger record | orchestrator | `grok-4.7-extra-high` |
| S1 T1 planWeek algorithm decision | deep-reasoner | `grok-4.7-extra-high` |
| S1 T6 redesign direction | design-lead | `grok-4.7-extra-high` |
| S2 T1–T6 implementation (6 steps) | fast-worker tier | `cursor-grok-4.6-high-fast` |
| S3 verify T3 WeekView | ecc-code-reviewer | `cursor-grok-4.6-high-fast` |
| S3 verify T1 planWeek | ecc-tdd-guide | `cursor-grok-4.6-high-fast` |
| S4 correction re-dispatch T1 | fast-worker tier | `cursor-grok-4.6-high-fast` |
| S5 fallback if a named agent is missing | general subagent | either tier by role (fallback paragraph, §7c) |

Every thinking step (orchestrator, MODEL-PIN, deep-reasoner, design-lead) resolves to `grok-4.7-extra-high`; every fully-specified implementation/verification step resolves to `cursor-grok-4.6-high-fast`. No thinking work is routed to a drone tier; no mechanical work is routed to the orchestrator tier — the cost-sanity condition in fix30/SPEC.md holds on the trace.

### 7e. Old-pin sweep — PASS

**0 old-pin references in the 24 traced files** (model-route, schema, orchestrate + dispatch-prompt, gan-build, gan-design, astra-review, feature-expansion, gan-style-harness, redesign, orch-pipeline, design-taste-frontend, hackathon-mode, common-agents, README, pi-core.json, plus the traced agent files). **Tree-wide: `grok-4.7-high` ×0, `Grok 4.7 High` ×0** (built tree, excl. `node_modules`). Note the boundary, stated honestly: staged sources and `build.sh` inline content keep the old pin **by design** (fix30 patch log DECISION-30-1 / OWED-30-1 — fix16/24/29 anchors); the sweep covers the built tree only, which is what ships.

### 7f. Fast-worker pin intact — PASS

`cursor-grok-4.6-high-fast` ×**70** tree-wide (unchanged from #44); bare `grok-4.6-high-fast` ×**0** (substring count equals the `cursor-`-prefixed count, so every occurrence carries the prefix).

### 7g. Census reconciliation — PASS

- ID census: `grok-4.7-extra-high` ×**49** (SPEC: 49). Per-file: orchestrate 15, gan-style-harness 3, gan-design 3, astra-review 3, deep-reasoner 3, hackathon-mode 2, common-performance 2, model-route 2, gan-build 2, ecc-gan-planner 2, + 12 files ×1.
- Prose census: `Grok 4.7 Extra High` ×**22** (SPEC: 22). Per-file: orchestrate 12, hackathon-mode 3, README 3, strategic-compact 2, pi-core 1, astra-review 1.
- Patch-log agreement: `fix30-patch-log.md` post census reads "grok-4.7-extra-high x49, 'Grok 4.7 Extra High' x22, grok-4.7-high x0, 'Grok 4.7 High' x0, cursor-grok-4.6-high-fast x70 (unchanged)"; the per-file rename lines in the log sum to ID 49 + prose 22.

**Script-expectation correction, recorded honestly:** the first run of the leg-7 script failed 7g-patchlog-agrees at 30/31 because the script asserted the log contains the wording "49 ID + 22 prose renamed" / "fast-worker pin unchanged at 70" — the log records the same facts in its own post-census wording instead. The script's expectation was corrected to the log's real wording plus a per-file-sum check; the re-run passes 32/32. No tree text was touched — the error was in the dry-run script, not the plugin. (Same class as #44 §6(c).)

**What Leg 7 does NOT claim:** that Cursor honors the pin at runtime. The orchestrate text itself says it plainly (`:93`, `:62`): "File-level pin only — the live smoke test decides whether the pin holds; do not claim it is verified working" and "Skill text cannot enforce the pin". The live test (Anish, `fix30/live-test-prompt.md`) decides; until then the pin is verified **in the text**, not in Cursor.

## 8. Environment notes (sandbox, not the plugin)

- `/tmp` was **62% full (317 MB used, 196 MB free)** at session start, unchanged at the end. **No Chrome work used `/tmp`:** `TMPDIR` was redirected to `fix30/dryrun45-scratch/chrome-tmp` for every harness, probe, and Remotion run. Nothing crashed on shared memory.
- The Playwright browser install worked first try (see §3.2) — the CDN flakiness dry-runs #37–#42 recorded is intermittent, not gone.
- **No service restart interrupted this run.** No leg was interrupted by the environment.
- **Two self-inflicted incidents, both recovered, no impact on any leg:**
  - The first Leg 2 preserve attempt used the wrong base path (plugin tree instead of `~/workspace/cold-start-render/`); the retry from the correct path succeeded before the harness ran.
  - A background `find /` for the chrome-headless-shell was started before the hardcoded harness path was checked; killed once the on-disk path was confirmed (the find itself had already located nothing new — the shell lives at the fix22 path the harness hardcodes).
  - The copied Leg 5 fixture carried a stray `~` directory from #44's pip-install incident (see §5.1); removed before the run.
- **Cleanup performed at the end:** deleted the reinstallable scratch bulk — `demo-sample-video/node_modules/` (665 MB), `demo-sample-video/public/frames/` (183 MB of 2,281 frame JPEGs — regenerable from `capture/out/take.webm` via `frames.mjs`; `src/frames.json` with the 2281 count kept), `dryrun45-scratch/npm-cache/` (295 MB), `dryrun45-scratch/pw-browsers/` (266 MB, the downloaded browser binary + ffmpeg), `dryrun45-scratch/pylibs/` (17 MB), `dryrun45-scratch/chrome-tmp/` contents, runner scratch `fake-home/`. Kept: all scripts, logs, reports, the fixture `shots.json` + `src/vo-durations.json` + `src/frames.json`, `capture/` (marks + take.webm + failures), `out/qa/` (12 stills + 2 sheets), the collab fixture sources + test/probe outputs + screenshot, and the Leg 5 test-coverage project + `coverage.json`. A repeat of Leg 3 needs one `npm install` and the Playwright install (or a retry of the installer). Total kept: 9.4 MB.
- No servers left running (ports 8323 and 5180 verified dead at the end).

## 9. OWED to the live smoke test — live-only items, never claimed verified

Carried from dry-run #44 §8, plus this run's additions:

- **Leg 7 live pin behavior (OWED-30-3):** whether Cursor honors `grok-4.7-extra-high` for the orchestrator / design-lead / deep-reasoner at runtime, and whether per-subagent model choice holds. The dry-run pin leg verifies the text statically (32/32); the live test is Anish's `fix30/live-test-prompt.md` — pass = Extra High ran the parent on both tasks, visible in the model indicator.
- **Benchmark dimension 7 (alignment):** the Campus Eats re-trace cannot be alignment-scored without a live Campus Eats render + browser-qa run (§2.3). Closed as a RECORDED DECISION per fix28/SPEC.md §7, not a pass.
- **Fix #17 R1/R4:** OWED as defined (§2.3). The Home Run render applies iris-opens in a different placement and has no hero loop; a live Campus Eats render implementing #67/#68 would be needed, and none will be built (Anish's Nov 11 call).
- **Leg 6 live factory behavior (OWED-29-2):** per-model dispatch (DeepSeek/Qwen per task, fix #30) and slot refill at scale in Cursor. The dry-run factory leg verifies the design statically (27/27); live dispatch is harness-gated and lights up fully on the later port. The live test (Anish, in Cursor, after fix #30): the orchestrator runs a multi-part build and reports N drones, partitions, and verification outcomes.
- **Live `qa.mjs` exit-0 + live film + rendered `demo.mp4` in Anish's Cursor** (the sandbox side — fonts, recording, QA exit 0 — is now proven again; the Cursor side is not).
- **Measured (not estimated) narration runtime** and the **10-second mix listen** (no voice provider, no bed in the sandbox).
- **Live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting, live REROUTE_F27 lookup, live trigger firing, live Cursor behaviour of the ck wire** (§5).
- Prior open items carried forward: D-6 Stop/SessionStart contradiction; C-5 timeout-300 unit; C-6 hook cwd/node/event names; D-9 `.ecc/settings.json` pickup; E-7 gate hook without Git Bash; general-subagent fallback pin behaviour; F-14 post-report /demo stale README (fixed in fix #26 per `fix26/f14-note.md` — the dry-run does not re-verify the fix itself, only that Leg 3's gates still hold); Netlify row touch-up after Dec 4, 2026; fresh bundle needed before any push.

## 10. Observations for the audit (not leg failures)

- **`hackathon-ecc/README.md:69` still lists the dropped `/epic-*` commands as shipping** ("`/epic-*` commands, `validate-skills.js`) ship with their dependencies vendored…"). Stale prose from the fix #27 cut, carried into the fix #30 tree unchanged — the commands no longer exist. Likewise orchestrate :136's REROUTE note still names the epic commands as machinery a build must not dispatch (prose-history, Audit #76 B3). Neither dispatches anything, so neither fails a leg; both are doc staleness for the fix to note. (Same observation as dry-run #42 §5, #43 §8, and #44 §9 — re-verified live this session.)
- **OWED-30-5 prose judgment, for the audit to challenge:** `skills/strategic-compact/SKILL.md:68` (the "500k Grok 4.7 Extra High" context-window example) and `:102` (the Cursor 2.1.233 todo-tools note) were renamed to Extra High per DECISION-30-2 (uniformity over a carve-out). If the audit finds either line should have kept "Grok 4.7 High" (historical note / context-window example), the fix is a two-line carve-out in fix30.py plus updated census counts — not a re-scope. Recorded here so the audit sees it; it does not fail a leg.
- **Staged-vs-built pin drift is by design, not a miss** (OWED-30-1): staged sources keep the old pin (new-skills/ 19 ID + 12 prose, new-rules/ 2 ID + 3 prose) and `build.sh` inline content keeps it (54 pre-existing ID occurrences on 50 lines + 5 prose; the fix30 hook block itself adds 2 meta-mentions). Syncing staged to the built text would break the fix16/fix24/fix29 anchors and fail the build. verify30 asserts the pins in the BUILT tree only — which is what this dry run re-verified (Leg 7 §7e).

## 11. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression + fix #23) | 101 | **PASS (101/101)** |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | **PASS on all 17 assertions, 0 flags** |
| 2 — Campus Eats v5 benchmark | 7 dimensions | **6 PASS statically; dimension 7 (alignment) OWED** |
| 3 — /demo gates + Remotion | 59 | **PASS (59/59) — qa.mjs exit 0 twice, 12/12 stills, 0 font requests; Playwright installer worked first try** |
| 4 — Cursor-readiness (fix #24) | 37 | **PASS (37/37)**, incl. 13 live C-1 hook pipe tests (after one dry-run-script expectation update, §4) |
| 5 — Call-graph | 41 checks | **17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN** (fix28 map stands; uncalled 17, second-order 7) |
| 5 — Technical depth (collab editor, re-run) | 11 automated + 6 live | **PASS (11/11 + 6/6)**, budgets measured (echo p95 58 ms < 150 ms; burst < 3 ms < 500 ms; 10k doc merged in 62.3 ms) |
| 5 — /test-coverage Steps 1–2 | 1 exercise | **EXERCISED** (calc.py 68.2%, listed below 80%) |
| 6 — Factory (fix #29 leg, re-run) | 27 checks | **PASS (27/27)** — 6 tasks / 4 skills; partitions disjoint; 6/6 briefs 7/7 fields; NEEDS_CONTEXT on the unspecified decision; 8/8 correction-brief sites name the failed criterion; refill simulated with the Cursor harness gate recorded; N=6 justified in one line |
| 7 — Pin leg (NEW, fix #30) | 32 checks | **PASS (32/32)** — route table + orchestrate table resolve thinking roles to `grok-4.7-extra-high`, mechanical roles to `cursor-grok-4.6-high-fast`; schema enum validates the new pin and rejects the old; 45/45 agent pins in-enum (4 extra-high, 41 fast); 14-step simulated trace resolves clean; old pin x0 in the trace and tree-wide; fast-worker x70 intact; census 49/22 reconciled to the patch log. **Static only — live Cursor behavior OWED to Anish's live-test prompt.** |

**DRY-RUN #45: PASS** — with benchmark dimension 7 owed (§2.3), fix #17 R1/R4 owed as defined (§2.3), live factory behavior owed per OWED-29-2 (§6(e)), and live Extra High behavior owed per OWED-30-3 (§7). No BLOCKING finding in any leg. The only first-run non-passes were in the dry-run's own scripts (Leg 4's stale "Grok 4.7 High" verbatim — §4; Leg 6's mangled cross-reference path — §1; Leg 7's wrong patch-log wording — §7); the tree was correct in all three cases and the corrected scripts pass. Three observations for the audit, not leg failures: README.md:69 still lists the dropped `/epic-*` commands as shipping (§10), the OWED-30-5 strategic-compact prose judgment (§10), and the by-design staged-vs-built pin drift (§10).

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-report.md` (this report)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-fixtures.py` + `dryrun45-fixtures-output.txt` (42/42)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-f23.py` + `dryrun45-f23-output.txt` (59/59)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-align.py` + `dryrun45-align-output.txt` (17 PASS, 0 flags) + `status-center-probe.mjs` + `status-center-probe-output.txt` (centers delta 0) + `align-run.log` (52 measurements, 0 console errors, 0 failed requests) + `prior-align-audit-results.json`
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-benchmark.md` (v5 re-trace: 68/66, per-dimension table, dynamic-count re-derivation with the 6–13 range, Dim 7 owed, R1/R4 scope note)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-demo.py` + `dryrun45-demo-output.txt` (59/59) + `demo-av-table.md` (12/12 beats verified from stills; mix listen unexecuted)
- `~/workspace/hackathon-plugin/fix30/dryrun45/sample-app/` + `demo-sample-video/` (fresh built-template copy + fixture `shots.json` + live `src/vo-durations.json` + `src/frames.json`; `capture/` with marks + take.webm + failures; `out/qa/` with 12 stills + 2 sheets; `node_modules/` + `public/frames/` removed in cleanup — see §8) + `npm-install.log`, `tts-run.log`, `record-run.log`, `frames-run.log`, `qa-run.log`, `qa-run2.log`, `qa-exit.txt`, `qa-exit2.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `pw-install.log`
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-leg4.py` + `dryrun45-leg4-output.txt` (37/37; one expectation update — the picker verbatim, §4)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-leg5.py` + `dryrun45-leg5-output.txt` (17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN; exit 0; one path repair — §1/§6) + `leg5-testcov/` + `coverage.json` + `leg5-testcov-run.log` + `dryrun45-leg5-testcov.md`
- `~/workspace/hackathon-plugin/fix30/dryrun45/leg5-collab/` (`crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`, `demo-shot.png`) + `leg5-collab-test-output.txt` (11/11) + `leg5-collab-probe-output.txt` (6/6)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-leg6.py` + `dryrun45-leg6-output.txt` (27/27; exit 0) + `dryrun45-leg6-briefs.md` (the 6 constructed director briefs + COST-AWARE line)
- `~/workspace/hackathon-plugin/fix30/dryrun45/dryrun45-leg7.py` + `dryrun45-leg7-output.txt` (32/32; exit 0 — the new fix #30 pin leg)
- `~/workspace/hackathon-plugin/fix30/dryrun45/verify30-rerun45.log` (verify30 re-run this session: 318/318, exit 0)
- `~/workspace/hackathon-plugin/fix29/dryrun44/dryrun44-report.md` + fixture/demo scripts (Dry-run #44 lists reused verbatim except the documented Leg 4 expectation update, Leg 6 path repair, and the new Leg 7)
- `build.sh` measured this session: **24,144 lines, md5 `4179be09c9e050b34ae70763f6ad0b15`**; counts **67/45/48/55/15**, triggers **49**; banned terms **3 hits, all allow-listed MotionSites, 0 unallowed** (LICENSE hit needs `grep -a`); Grok pins extra-high 49/22, old pin 0/0, fast-worker 70, bare 0; call map md5 `b066413a1a7dd6efcd8571c8abf93942`; verify30 re-run **318/318**
