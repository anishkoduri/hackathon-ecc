# Dry-run #43 — Fix #28 (rules 123 → 48, manifests pruned, 135 dead scripts cut)

- **Date:** 2026-11-16, ~15:00–15:19 CST (21:00–21:19 UTC). Worker: dry-run #43 agent (fix #28), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix28/dryrun43/` (plus scratch under `fix28/dryrun43-scratch/`, cleaned at the end). No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run.
- **Verdict: DRY-RUN #43: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run passes all 17 §6 assertions at all 4 widths and all 13 states with 0 flags; the Campus Eats v5 benchmark passes 6 of 7 dimensions statically, with dimension 7 (alignment) OWED, never passed (no live Campus Eats render exists to measure). Leg 3: **59/59** — `qa.mjs` exits 0 twice on the rebuilt plugin with self-hosted template fonts, 12/12 stills rendered, 0 Google Fonts requests; the Playwright installer worked first try this run (exit 0), so no curl recovery was needed. Leg 4: 37/37 Cursor-readiness, incl. the 13 live C-1 hook pipe tests. Leg 5 (call-graph): 17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN against the regenerated fix28 map; the technical-depth fixture (real-time collaborative editor, sequence CRDT) re-run passes 11/11 automated checks + 6/6 live browser probe checks.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,119 lines, md5 `06e3611ba526136952bee9d7940955ea`**. (Was 24,100 / `ff7fe001…` in #42; +19 lines = the fix28.py invocation block added after fix27's, per fix28/SPEC.md §6.)
- Counts verified: **67 skills / 45 agents / 48 rules / 55 commands / 15 hooks**, trigger keys **49** (from `manifests/context-packs/skill-triggers@1.json` `triggers` dict; hooks.json holds 15 events). The rule cut moved 123 → 48, exactly as fix #28 §1 prescribes; skills/agents/commands/hooks/triggers unchanged.
- verify28.py run 5 log: **110/110 checks pass** (`fix28/verify28-run5.log`). Build log run 6 ends `build complete`.
- Call map: the regenerated fix28 map `skills/orchestrate/references/call-map.md` md5 **`b066413a1a7dd6efcd8571c8abf93942`**; its counts table reads 67/45/48/55/15/49. The machine-readable sidecar is now `fix28/callmap/call-map-data.json` (md5 `6a8bb11fa02769351a8c5b267153d10f`, same counts).
- Banned terms: raw grep over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` (excl. `node_modules`) returns **3 hits in 2 files, all allow-listed** — `skills/motionsites-web-builder/SKILL.md:25` and `:38` (upstream fetch URLs containing `Motionsites-AI/claude-skill`) and `skills/motionsites-web-builder/LICENSE:1` (upstream license title). Same 3 as #42. **0 unallowed hits.**
- Grok pins: `grok-4.7-high` ×50, `cursor-grok-4.6-high-fast` ×70, bare `grok-4.6-high-fast` ×0 (lookbehind grep). Down from #42's 56/74 — the delta is the fix #28 cut itself: the fix #27 scratch tree (`fix28/scratch-repo/hackathon-ecc`) measures 56/74 with the same grep, and the cut scripts/rules carried pin mentions (e.g. 4 cut scripts + cut rule files reference the pins). Only the two allowed pin forms remain; bare count is still 0.
- Cut rules absent: 0 `angular|vue|rust|golang` files under `hackathon-ecc/rules/`; README.md:13 count line reads "67 skills, 45 agents, 48 rules, and 55 commands" per SPEC §4(e).
- Audit #77 / #78 / #79 / verify28.py are parallel fix #28 workers, not re-run here.

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build tree: 42/42

Runner `dryrun43-fixtures.py` is a verbatim copy of `fix27/dryrun42/dryrun42-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun43-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #28 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun43-f23.py` is a verbatim copy of `fix27/dryrun42/dryrun42-f23.py`. Output: `dryrun43-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present.

**Adaptations: none.**

## 2. Leg 2 — Home Run render re-run + Campus Eats v5 benchmark

### 2.1 Fix #28 touches no render files — verified, not assumed

- `fix28/fix28.py` and `fix28/SPEC.md` contain **zero** references to `cold-start-render`. The single `cold-start-render` hit in `build.sh` is the pre-existing fix #23 comment at `:23907` (the ALIGN_F23 block), not a fix #28 edit. No file under `fix28/` outside the `scratch-repo/` audit-trail history mentions `home-run` / `Home Run`.
- Render file mtimes predate fix #28: `index.html` Nov 13 02:46, `styles.css` Nov 13 03:00, `app.js` Nov 13 02:43, `qa/align-audit.mjs` Nov 13 03:00. (`qa/align-audit-results.json` was Nov 16 08:16 — dry-run #42's run — until this leg overwrote it; the prior file was preserved first at `fix28/dryrun43/prior-align-audit-results.json`.)

### 2.2 Render re-run (live, this session): all 17 assertions PASS, 0 flags

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`). Log: `fix28/dryrun43/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].**
- **Interruption, recorded honestly:** the first harness attempt was killed mid-run by a service restart — the log ends at `shot align-768-home-bottom` with `page.waitForTimeout: Target page, context or browser has been closed` at `align-audit.mjs:178`, and the http server died with it. The results JSON was untouched (still #42's file) because the harness writes it only at the end. The server was restarted and the harness re-run clean to the exit-0 result above. The failed attempt was environmental, not a harness or render failure; nothing was claimed from it.
- Analysis `dryrun43-align.py` (output `dryrun43-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).
- All Chrome work ran with `TMPDIR=<dryrun43-scratch>/chrome-tmp` (`/tmp` was 62% full at session start).

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

Fresh vs prior results JSON: identical except **4 measurements** (all four `trip-wrongcode`, one per width), and only in the individual code-box input rects (1–3px shifts); the group geometry is identical in both (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #42 saw the same pattern in 4 measurements; #41 in 4; #40 in 2; #39 in 3; #38 in 4.)

### 2.3 Campus Eats v5 benchmark — 6/7 static PASS, dimension 7 OWED

Full re-trace: `fix28/dryrun43/dryrun43-benchmark.md` (fresh verification of the v5 figures, rule traces, per-dimension table). Summary:

- **Benchmark file re-read this session** (178 lines, frozen at v5): kind sums re-added — literal 31+8+1+17+1+2+0+1 = **61**, stricter **60**; dynamic inventory 8 items, 1 drive, 2 surfaces, all as recorded.
- **Dynamic-count boundary re-derived** from `fix17/INVENTORY-V4.md` (#47–#50, #54 hover micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item for item, with the defensible range **6–13** (narrow/broad) unchanged.
- **Rule traces for the 7 re-trace additions re-checked in the rebuilt tree:** R1 (`design-taste-frontend/SKILL.md:409` — same line as #42; text unchanged), R4 (`fix15/SPEC.md:91`), CREATIVE_F25 (`feature-expansion/SKILL.md:59,93,99` — one line later than #42's 58/92/98; anchor texts identical), E1, M3 (`make-interfaces-feel-better/SKILL.md:127` — two lines later than #42's :125; anchor text identical). All hold. (Fix #28 touches none of these files; the +1/+2 drift vs #42 is build-time patch-application drift.)
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

Checker `dryrun43-demo.py` (verbatim copy of the #42 checker; output `dryrun43-demo-output.txt`): **59/59 /demo contract checks met, exit 0** — 35/35 original contract checks, 13/13 removal checks, 11/11 Remotion checks. The `qa.mjs` live check passes again.

### 3.1 The evidence (what actually ran, in order)

Fixture: `fix28/dryrun43/demo-sample-video/` — a **fresh copy of the rebuilt template** from the built tree (diffed against it: byte-identical except the fixture `shots.json`; the template's own `capture/` and `public/frames/` output dirs were not copied) + the Dry-run #37/38/39/40/41/42 `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block) + `fix28/dryrun43/sample-app/` (Pantry Pal, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards). Template facts in the copy: `package.json` carries `"@remotion/fonts": "4.0.526"` and **no** `@remotion/google-fonts`; `src/fonts.ts` uses `loadFont` + `staticFile('fonts/….woff2')`; `public/fonts/` holds exactly the 3 woff2 files. (`@remotion/google-fonts` still appears as a raw string 2× in `fonts.ts` — the intentional provenance header comment — and 1× in `mobile-ship` prose; zero imports, zero dependencies. That is the build worker's caveat 1, for the audit to decide; it is not a font fetch.)

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund`, cache in dryrun43 scratch (`npm-install.log`) | **exit 0**; `@remotion/fonts` present in `node_modules`, `@remotion/google-fonts` absent |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording | `node scripts/record.mjs` (`record-run.log`) | **exit 0. Take: 75.5s, 8 camera moves.** `capture/marks.json`: all 10 app beats + `__end`; **all 6 feature beats filmed**; `capture/out/take.webm` 3.6 MB. Playwright installer worked first try this run (see §3.2). |
| Frames | `node scripts/frames.mjs` (`frames-run.log`) | **exit 0. 2281 frames (76.0s).** |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 0 — TWICE.** First run exit 0; re-run (`qa-run2.log`, exit in `qa-exit2.txt`) exit 0 with a clean capture. **"No BLOCKING findings from the automated checks" in both logs. 12/12 stills rendered** (`out/qa/00111_problem.png` … `02408_close.png`) **+ 2 ffmpeg contact sheets. `grep -ci "fonts.googleapis\|fonts.gstatic" qa-run.log` → 0; same for the re-run log.** |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Gates | demo checker 35/35 + 13/13 | /demo callable only on explicit invocation, narration-key prompt only on a requested video, first-build order deploy → commit → README with no /demo, runtime **84.1s** from live `vo-durations.json` (under 130s hard / 150s absolute), $0 spent under the $10 cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37–#42. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run.

### 3.2 The Playwright installer worked first try — no recovery needed

Dry-runs #37–#39 recorded the Playwright CDN closing the connection at ~90%; dry-run #40 got through on a retry; dry-run #41 failed twice and recovered with a curl download; dry-run #42 worked first try. This run: `npx playwright install chromium-headless-shell` (Playwright ffmpeg v1011) **exited 0 on the first attempt** (`pw-install.log`), downloading both the shell and ffmpeg into `dryrun43-scratch/pw-browsers/`. No curl recovery, no manual layout, no symlink needed. The installer flakiness remains environmental and intermittent; this run happened to get through.

### 3.3 What is NOT claimed by the 59/59

- **No full render** (`build.mjs --render` / `npm run all` end-to-end) was run — the stills + contact sheets + A/V table are the verified output; a rendered `demo.mp4` is owed to the live smoke test.
- **The 10-second mix listen was not done** — the fixture has no music bed (`musicBed: false`) and no narration (no voice provider), so there is no mix to listen to. The A/V table (`demo-av-table.md`) is completed from the viewed stills: **all 12 beats' claims match what is on screen** (pantry list shows the six ingredients; week plan shows "6 dinners · $0 extra · 1 pot"; Monday curry 25 minutes; Tuesday chickpea rice 20 minutes; leftover remix; arch diagram shows "static HTML — no runtime code"; close card shows the serif "Pantry Pal" in the self-hosted Instrument Serif face).
- **Record warnings (minor, not BLOCKING):** `capture/marks.json` carries 2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped ("Execution context was destroyed, most likely because of a navigation"). The footage for both beats exists (marks present, stills render); only the mid-shot click actions did not execute — a navigation race in `record.mjs`, not a missing beat. Same warnings as #41/#42. `qa.mjs` itself reports "No BLOCKING findings".
- A live film in Anish's Cursor is still owed by the smoke test, as before — but the sandbox side of it (fonts + recording + QA exit 0) is now proven here again.

## 4. Leg 4 — Cursor-readiness (fix #24): 37/37

Runner `dryrun43-leg4.py` (verbatim copy of the #42 runner, no expectation updates needed; output `dryrun43-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with the same file:line evidence as #42 (picker prerequisite verbatim once in orchestrate step 4; 4 dual-cited agent path lines; general-subagent fallback; all four /demo gates; resume guards; inventory pointers in Taste + ui-ux-pro-max; FILM_F1/F5/F6; F-09 step 6 wording; tts.mjs Windows forms; **13 live C-1 hook pipe tests**: 6 BLOCKED exit 2, 5 ALLOWED exit 0, 1 documented base64 GAP exit 0, 1 sanity BLOCKED exit 2).

## 5. Leg 5 — Call-graph: 17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN

Runner `dryrun43-leg5.py` (copy of the #42 runner with the two documented adaptations below; output `dryrun43-leg5-output.txt`, **exit 0**). It reads the regenerated `fix28/callmap/call-map-data.json` (counts 67/45/48/55/15/49) and, for every element, either runs the dispatch path, resolves it statically, or records it dormant/owed. Outcome meanings as in #42. The fix #28 §1–§4 edits moved the uncalled count exactly as the cut predicts (see below); nothing else moved.

| Category | Count | What was exercised / checked |
|---|---|---|
| Counts agree | 6 STATIC-OK | Map counts 67/45/48/55/15/49 all match the tree (skills dirs, agent files, `.mdc` rules, command files, `hooks.json` events, `skill-triggers@1.json` `triggers` dict) |
| Commands resolve | 55/55 STATIC-OK + 4 reviewed non-dispatch refs | Every command file's named skills/agents/commands resolve. The 4 reviewed refs (learn `skills/learned/` placeholder; react-review + save-session `/api` code paths; skill-create GitHub App) are non-dispatch mentions, verified by reading. (Same 4 as #42.) |
| Skills load | 67/67 STATIC-OK | Every skill has a non-empty `SKILL.md` with frontmatter; map skill keys == tree skill dirs. Live invocation of each on-request skill is OWED. |
| Hooks run live | **15/15 EXERCISED** | Every `hooks.json` event ran with synthetic Cursor-format JSON stdin (cwd = built tree, `HOME` = scratch fake-home, `TMPDIR` redirected): all exit 0 with valid JSON output. Includes `sessionStart` (see ck wire below) and `beforeShellExecution` (dispatches to the C-1 hook, already pipe-tested in Leg 4). |
| Fix #25 wires | 1 EXERCISED (ck) + 2 STATIC-OK + 1 EXERCISED (test-coverage) | **ck: EXERCISED** — `hooks/session-start.js` run on the REAL built tree with fake stdin `{}` and fake `$HOME`: exit 0, output JSON carries the full ck (Context Keeper) brief (7,599 B stdout this run — identical to #42). **prp-commit: STATIC-OK** — Phase 3 + orchestrate step 6 name `git-workflow` + `ecc-commit-reviewer`; both resolve; live commit drafting OWED. **ecc-recipes: STATIC-OK** — the skill was CUT; the REROUTE_F27 replacement lookup is present in orchestrate :136; live lookup OWED. **/test-coverage Steps 1–2: EXERCISED** — see §5.1. |
| Uncalled | 17 DORMANT | 2 skills (`context-budget` — deliberately uncalled, the live usage meter; `vite-patterns` — newly uncalled, see below), 9 agents, 6 commands — exactly the map; every one has zero calling invokers. (Was 16 in #42: +1 skill.) |
| Second-order orphans | 7 DORMANT | 3 agents, 4 commands (`harness-audit`, `python-review`, `skill-create`, `skill-health`) — exactly the map; every orphan's invokers resolve to uncalled elements or neutral reference files. (Same 7 as #42.) |
| Triggers | 49 STATIC-OK | All 49 keys resolve; no live Cursor entry point for the consumer (parent decision item, unchanged — fix #26 §5 records it documentation-only) — live firing OWED. |
| Epic commands | 0 — dropped | The 8 epic/`/prune` commands were DROPPED in fix #27 §1(b); no dormant-in-use set remains in the tree. |

**Paths exercised vs not executed vs owed (summary):** EXERCISED 17 (15 hooks + ck wire + /test-coverage measurement). NOT EXECUTED by decision 22 (17 uncalled + 7 second-order orphans, all with recorded dormant reasons; the epic commands no longer exist to be dormant-in-use) — the summary counts 5 DORMANT outcome lines (uncalled:count, uncalled:zero-invokers, second-order:count, second-order:invokers-uncalled, epic-dormant-in-use). OWED to the live smoke test: live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting via prp-commit, live recipes-lookup replacement (REROUTE_F27), live trigger firing, and live Cursor behaviour of the ck wire (the scratch + built-tree runs prove the Node mechanics only).

**No MINOR this run.** The dry-run #40 MINOR (`/loop-status` alias) was fixed in fix #25 option (b) and stays fixed: **0 `loop-status` hits** anywhere in the built tree (verified by grep this session).

**Why `vite-patterns` is newly uncalled (traced, not assumed):** in the fix #27 map (`fix25/callmap/call-map-data.json`) it was `called: true`, and its ONLY calling invokers were the 9 CUT Nuxt/Vue rule files (`rules/nuxt-coding-style.mdc`, `nuxt-hooks.mdc`, `nuxt-patterns.mdc`, `nuxt-testing.mdc`, `vue-coding-style.mdc`, `vue-hooks.mdc`, `vue-patterns.mdc`, `vue-security.mdc`, `vue-testing.mdc` — all in the fix #28 §1 cut set, each a "strong" invoker). Fix #28 cut those rules, so the skill lost its only calling invokers; in the regenerated fix28 map its invokers are only the neutral `install-modules.json` / `pi-core.json` "shipped" entries, and it is `called: false`. That is the cut working exactly as specified, not a regression — no kept file dispatches to it, and the leg's zero-invokers check confirms it. (Its remaining mentions in the tree are its own SKILL.md, call-map.md, and the two manifest "shipped" entries — no live dispatch.)

**Runner adaptations for fix #28 (dry-run copy only, all documented inline, no plugin file touched):**

1. **`MAP_PATH` — `fix25/callmap/call-map-data.json` → `fix28/callmap/call-map-data.json`.** The regenerated map lives under fix28 now.
2. **Uncalled count — 16 → 17** (expectation + detail string), for the `vite-patterns` change above.

### 5.1 /test-coverage Steps 1–2 exercised live

Scratch pytest project `leg5-testcov/` (verbatim copy of the #42 fixture; see `dryrun43-leg5-testcov.md`): `pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py` (5 tests, deliberately not covering `mul` or `untested_helper`). Ran the command's Step 1 detection + Step 2 measurement: `pytest --cov=src --cov-report=json`, **exit 0, 5 passed** — `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly as the wire specifies. Identical outcome to #40/#41/#42. Step 3 generation stays in the fix loop by design and was not run.

### 5.2 Technical-depth fixture: real-time collaborative editor — re-run PASS

Fixture: `fix28/dryrun43/leg5-collab/` (verbatim copy of the #42 fixture — `crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`). Re-run, not rebuilt: the CRDT, server, and demo are unchanged from #42.

- **Results: `test.mjs` 11/11 checks pass, exit 0; `probe.mjs` 6/6 live browser checks pass, exit 0** (type A→B, type B→A, offline divergence, offline merge, cross-collaborator undo, presence badge). Screenshot `demo-shot.png` re-taken by the probe run.
- **Budgets measured again:** keystroke → remote echo p95 3 ms (budget < 150 ms); 100-op burst local insert 0.9 ms / remote apply 0.2 ms (budget < 500 ms); 10,000-char document build 20.8 ms, merge 21.2 ms, converged. All within budget, same order as #42 (echo p95 3 ms there too; burst faster this run — localhost timing noise, not a regression).
- No fixture defects found on re-run; nothing was changed in the fixture.

## 6. Environment notes (sandbox, not the plugin)

- `/tmp` was **62% full (313 MB used, 200 MB free)** at session start. **No Chrome work used `/tmp`:** `TMPDIR` was redirected to `fix28/dryrun43-scratch/chrome-tmp` for every harness, probe, and Remotion run. Nothing crashed on shared memory.
- The Playwright browser install worked first try this run (see §3.2) — the CDN flakiness dry-runs #37–#42 recorded is intermittent, not gone.
- **A service restart mid-run killed the first align-harness attempt** (§2.2): the browser was closed at `align-768-home-bottom` and the http server died with it. The attempt was discarded (its results JSON was never written) and the harness re-run clean. No other leg was interrupted.
- **Cleanup performed at the end:** deleted the reinstallable scratch bulk — `demo-sample-video/node_modules/` (665 MB), `demo-sample-video/public/frames/` (183 MB of 2,281 frame JPEGs — regenerable from `capture/out/take.webm` via `frames.mjs`; `src/frames.json` with the 2281 count kept), `dryrun43-scratch/npm-cache/` (295 MB), `dryrun43-scratch/pw-browsers/` (266 MB, the downloaded browser binary + ffmpeg), `dryrun43-scratch/pylibs/` (pytest-cov install), `dryrun43-scratch/chrome-tmp/` contents, runner scratch `fake-home/`. Kept: all scripts, logs, reports, the fixture `shots.json` + `src/vo-durations.json` + `src/frames.json`, `capture/` (marks + take.webm + failures), `out/qa/` (12 stills + 2 sheets), the collab fixture sources + test/probe outputs + screenshot, and the Leg 5 test-coverage project + `coverage.json`. A repeat of Leg 3 needs one `npm install` and the Playwright install (or a retry of the installer). Total kept: 9.3 MB.
- No servers left running (ports 8323 and 5180 verified dead at the end).

## 7. OWED to the live smoke test — live-only items, never claimed verified

Carried from dry-run #42 §7, plus this run's additions:

- **Benchmark dimension 7 (alignment):** the Campus Eats re-trace cannot be alignment-scored without a live Campus Eats render + browser-qa run (§2.3). Closed as a RECORDED DECISION per fix28/SPEC.md §7, not a pass.
- **Fix #17 R1/R4:** OWED as defined (§2.3). The Home Run render applies iris-opens in a different placement and has no hero loop; a live Campus Eats render implementing #67/#68 would be needed, and none will be built (Anish's Nov 11 call).
- **Live `qa.mjs` exit-0 + live film + rendered `demo.mp4` in Anish's Cursor** (the sandbox side — fonts, recording, QA exit 0 — is now proven again; the Cursor side is not).
- **Measured (not estimated) narration runtime** and the **10-second mix listen** (no voice provider, no bed in the sandbox).
- **Live execution of the 55 commands, live invocation of the 67 on-request skills, live commit drafting, live REROUTE_F27 lookup, live trigger firing, live Cursor behaviour of the ck wire** (§5).
- Prior open items carried forward: D-6 Stop/SessionStart contradiction; C-5 timeout-300 unit; C-6 hook cwd/node/event names; D-9 `.ecc/settings.json` pickup; E-7 gate hook without Git Bash; general-subagent fallback pin behaviour; F-14 post-report /demo stale README (fixed in fix #26 per `fix26/f14-note.md` — the dry-run does not re-verify the fix itself, only that Leg 3's gates still hold); Netlify row touch-up after Dec 4, 2026; fresh bundle needed before any push.

## 8. Observations for the audit (not leg failures)

- **`hackathon-ecc/README.md:67-68` still lists the dropped `/epic-*` commands as shipping** ("The plugin's Node scripts (`/harness-audit`, the `/epic-*` commands, `validate-skills.js`) ship with their dependencies vendored…"). Stale prose from the fix #27 cut, carried into the fix #28 tree unchanged — the commands no longer exist. Likewise orchestrate :136's REROUTE note still names the epic commands as machinery a build must not dispatch (prose-history, Audit #76 B3). Neither dispatches anything, so neither fails a leg; both are doc staleness for the fix to note. (Same observation as dry-run #42 §5.)

## 9. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression + fix #23) | 101 | **PASS (101/101)** |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | **PASS on all 17 assertions, 0 flags** |
| 2 — Campus Eats v5 benchmark | 7 dimensions | **6 PASS statically; dimension 7 (alignment) OWED** |
| 3 — /demo gates + Remotion | 59 | **PASS (59/59) — qa.mjs exit 0 twice, 12/12 stills, 0 font requests; Playwright installer worked first try** |
| 4 — Cursor-readiness (fix #24) | 37 | **PASS (37/37)**, incl. 13 live C-1 hook pipe tests |
| 5 — Call-graph | 41 checks | **17 EXERCISED, 19 STATIC-OK, 5 DORMANT, 0 BROKEN** (regenerated fix28 map; uncalled 17, second-order 7) |
| 5 — Technical depth (collab editor, re-run) | 11 automated + 6 live | **PASS (11/11 + 6/6)**, budgets measured (echo p95 3 ms < 150 ms; burst < 1 ms < 500 ms; 10k doc merged in 21.2 ms) |
| 5 — /test-coverage Steps 1–2 | 1 exercise | **EXERCISED** (calc.py 68.2%, listed below 80%) |

**DRY-RUN #43: PASS** — with benchmark dimension 7 owed (§2.3) and fix #17 R1/R4 owed as defined (§2.3). No BLOCKING finding in any leg. The first-run non-pass (Leg 5 `wire:test-coverage` BROKEN) was a missing companion exercise, not a plugin defect: the test-coverage fixture had not been run yet in this session; once run (5 passed, 68.2%) the leg re-ran green. The only other first-run incident was environmental: a service restart killed the first align-harness attempt mid-run (§2.2); the re-run was clean. One observation for the audit, not a leg failure: README.md:67-68 still lists the dropped `/epic-*` commands as shipping (§8).

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-report.md` (this report)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-fixtures.py` + `dryrun43-fixtures-output.txt` (42/42)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-f23.py` + `dryrun43-f23-output.txt` (59/59)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-align.py` + `dryrun43-align-output.txt` (17 PASS, 0 flags) + `status-center-probe.mjs` + `status-center-probe-output.txt` (centers delta 0) + `align-run.log` (52 measurements, 0 console errors, 0 failed requests) + `prior-align-audit-results.json`
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-benchmark.md` (v5 re-trace: 68/66, per-dimension table, dynamic-count re-derivation with the 6–13 range, Dim 7 owed, R1/R4 scope note)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-demo.py` + `dryrun43-demo-output.txt` (59/59) + `demo-av-table.md` (12/12 beats verified from stills; mix listen unexecuted)
- `~/workspace/hackathon-plugin/fix28/dryrun43/sample-app/` + `demo-sample-video/` (fresh built-template copy + fixture `shots.json` + live `src/vo-durations.json` + `src/frames.json`; `capture/` with marks + take.webm + failures; `out/qa/` with 12 stills + 2 sheets; `node_modules/` + `public/frames/` removed in cleanup — see §6) + `npm-install.log`, `tts-run.log`, `record-run.log`, `frames-run.log`, `qa-run.log`, `qa-run2.log`, `qa-exit.txt`, `qa-exit2.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `pw-install.log`
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-leg4.py` + `dryrun43-leg4-output.txt` (37/37; verbatim, no expectation updates needed)
- `~/workspace/hackathon-plugin/fix28/dryrun43/dryrun43-leg5.py` + `dryrun43-leg5-output.txt` (17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN; exit 0; MAP_PATH + uncalled-expectation adaptations for the fix28 map — see §5) + `leg5-testcov/` + `coverage.json` + `leg5-testcov-run.log` + `dryrun43-leg5-testcov.md`
- `~/workspace/hackathon-plugin/fix28/dryrun43/leg5-collab/` (`crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`, `demo-shot.png`) + `leg5-collab-test-output.txt` (11/11) + `leg5-collab-probe-output.txt` (6/6)
- `~/workspace/hackathon-plugin/fix27/dryrun42/dryrun42-report.md` + fixture/demo scripts (Dry-run #42 lists reused verbatim except the documented runner updates in §5)
- `build.sh` measured this session: **24,119 lines, md5 `06e3611ba526136952bee9d7940955ea`**; counts **67/45/48/55/15**, triggers **49**; banned terms **3 hits, all allow-listed MotionSites, 0 unallowed**; Grok pins 50/70, bare 0 (down from 56/74 in #42, delta traced to the cut files); call map md5 `b066413a1a7dd6efcd8571c8abf93942`; verify28 run 5 **110/110**
