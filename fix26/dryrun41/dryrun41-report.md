# Dry-run #41 — Fix #26 (close the small open items)

- **Date:** 2026-11-14, ~21:32–22:05 CST. Worker: dry-run #41 agent (fix #26), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix26/dryrun41/` (plus scratch under `fix26/dryrun41-scratch/`, cleaned at the end). No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run.
- **Verdict: DRY-RUN #41: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run passes all 17 §6 assertions at all 4 widths and all 13 states with 0 flags; the Campus Eats v5 benchmark passes 6 of 7 dimensions statically, with dimension 7 (alignment) OWED, never passed (no live Campus Eats render exists to measure). Leg 3: **59/59** — `qa.mjs` exits 0 twice on the rebuilt plugin with self-hosted template fonts, 12/12 stills rendered, 0 Google Fonts requests; the Playwright installer failed environmentally twice (see §3.2) and the recording was recovered with a curl download, not a plugin change. Leg 4: 37/37 Cursor-readiness, incl. the 13 live C-1 hook pipe tests. Leg 5 (call-graph): 17 EXERCISED / 22 STATIC-OK / 5 DORMANT / 0 BROKEN — no MINOR this run (the dry-run #40 `/loop-status` MINOR stays fixed: 0 hits in the built tree); the technical-depth fixture (real-time collaborative editor, sequence CRDT) re-run passes 11/11 automated checks + 6/6 live browser probe checks.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,088 lines, md5 `e05bdc66599b694398e11f0d00dfdafd`**. Matches the task's stated gate numbers (freshly rebuilt, run 3, exit 0).
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks**, trigger keys **64** (from `manifests/context-packs/skill-triggers@1.json` `triggers` dict).
- Banned terms: **0** in the built tree (independent grep this session over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, excl. `node_modules`, returned no files).
- Grok pins: `grok-4.7-high` ×54, `cursor-grok-4.6-high-fast` ×103, bare `grok-4.6-high-fast` ×0 (same as fix #25).
- Pip pinning spot-check (§1 of the fix): a crude `grep 'pip install [a-z]'` finds 6 unpinned-looking lines in the built tree, but all 6 are classified in `fix26/pip-pinning.md` as non-install lines — (b) prose/mention or runtime strings ×5 (`bengali-nlp/SKILL.md:87,:139`; `python-patterns/SKILL.md:546`; `tts.mjs:180` error string, deliberately left unpinned; `insaits-security-monitor.py:205` log warning) and (d) troubleshooting-table mention ×1 (`ecc-django-build-resolver.md:182`). 0 unpinned category-(a) real install lines remain. No finding.
- Audit #73 / Sweep #34 / verify26.py are parallel fix #26 workers, not re-run here.

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build tree: 42/42

Runner `dryrun41-fixtures.py` is a verbatim copy of `fix25/dryrun40/dryrun40-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun41-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #26 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun41-f23.py` is a verbatim copy of `fix25/dryrun40/dryrun40-f23.py`. Output: `dryrun41-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present.

**Adaptations: none.**

## 2. Leg 2 — Home Run render re-run + Campus Eats v5 benchmark

### 2.1 Render re-run (live, this session): all 17 assertions PASS, 0 flags

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`). Log: `fix26/dryrun41/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].**
- Prior results preserved before the re-run at `fix26/dryrun41/prior-align-audit-results.json` (the harness overwrites `qa/align-audit-results.json` in place).
- Analysis `dryrun41-align.py` (output `dryrun41-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).
- All Chrome work ran with `TMPDIR=<dryrun41-scratch>/chrome-tmp` (see §6: `/tmp` was 73% full at session start).

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

Fresh vs prior results JSON: identical except **4 measurements** (all four `trip-wrongcode`, one per width), and only in the individual code-box input rects (1–4px shifts); the group geometry is identical in both (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #40 saw the same pattern in 2 measurements; #39 in 3; #38 in 4.)

### 2.2 Campus Eats v5 benchmark — 6/7 static PASS, dimension 7 OWED

Full re-trace: `fix26/dryrun41/dryrun41-benchmark.md` (fresh verification of the v5 figures, rule traces, per-dimension table). Summary:

- **Benchmark file re-read this session** (178 lines, frozen at v5): kind sums re-added — literal 31+8+1+17+1+2+0+1 = **61**, stricter **60**; dynamic inventory 8 items, 1 drive, 2 surfaces, all as recorded.
- **Dynamic-count boundary re-derived** from `fix17/INVENTORY-V4.md` (#47–#50, #54 hover micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item for item, with the defensible range **6–13** (narrow/broad) unchanged.
- **Rule traces for the 7 re-trace additions re-checked in the rebuilt tree:** R1 (`design-taste-frontend/SKILL.md:407`), R4 (`fix15/SPEC.md:91`), CREATIVE_F25 (`feature-expansion/SKILL.md:58,92,98`), E1, M3 (`make-interfaces-feel-better/SKILL.md:125`). All hold.
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

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7 is OWED.** `~/workspace/cold-start-render/campus-eats/` contains only `docs/design-tokens.md` (verified by listing this session; matches `fix26/dim7-note.md`) — no `index.html`, no CSS, no JS, no assets, so browser-qa cannot run the ALIGN_F23 matrix on it. Disposition per fix26/SPEC.md §6: RECORDED DECISION (owed, with the reason), not a pass. No Campus Eats render was built. The Home Run 52-measurement / 0-problem run is live alignment evidence about Home Run, not Campus Eats, and is not counted toward dimension 7.

**R1/R4 scope note (fix26/r1r4-note.md, verified this session):** the #67/#68 applications are paper re-trace additions, scored statically — NOT measurements of a live render. The Home Run render implements iris-opens in a different placement (trip code-panel reveal, `index.html:179–180`, `styles.css:433–446`, `app.js:192`) and implements no hero loop at all (zero `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval` hits across its `index.html`/`styles.css`/`app.js`; zero `loop` hits in its decision record). Fix #17 R1/R4 stay OWED as defined. The 6/7 re-trace result is unaffected: it never claimed a live verification of #67/#68.

## 3. Leg 3 — /demo: 59/59

Checker `dryrun41-demo.py` (verbatim copy of the #40 checker; output `dryrun41-demo-output.txt`): **59/59 /demo contract checks met, exit 0** — 35/35 original contract checks, 13/13 removal checks, 11/11 Remotion checks. The `qa.mjs` live check passes again.

### 3.1 The evidence (what actually ran, in order)

Fixture: `fix26/dryrun41/demo-sample-video/` — a **fresh copy of the rebuilt template** from the built tree (diffed against it: byte-identical except the fixture `shots.json`) + the Dry-run #37/38/39/40 `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block) + `fix26/dryrun41/sample-app/` (Pantry Pal, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards). Template facts in the copy: `package.json` carries `"@remotion/fonts": "4.0.526"` and **no** `@remotion/google-fonts`; `src/fonts.ts` uses `loadFont` + `staticFile('fonts/….woff2')`; `public/fonts/` holds exactly the 3 woff2 files. (`@remotion/google-fonts` still appears as a raw string 2× in `fonts.ts` — the intentional provenance header comment — and 1× in `mobile-ship` prose; zero imports, zero dependencies. That is the build worker's caveat 1, for the audit to decide; it is not a font fetch.)

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund`, cache in dryrun41 scratch (`npm-install.log`) | **exit 0**; `@remotion/fonts` present in `node_modules`, `@remotion/google-fonts` absent |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording | `node scripts/record.mjs` (`record-run.log`) | **exit 0. Take: 77.9s, 8 camera moves.** `capture/marks.json`: all 10 app beats + `__end`; **all 6 feature beats filmed**; `capture/out/take.webm` 3.3 MB. See §3.2 for how the browser binary was obtained after the installer failed twice. |
| Frames | `node scripts/frames.mjs` (`frames-run.log`) | **exit 0. 2347 frames (78.2s).** |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 0 — TWICE.** First run exit 0; re-run (`qa-run2.log`) exit 0 with a clean capture. **"No BLOCKING findings from the automated checks." 12/12 stills rendered** (`out/qa/00111_problem.png` … `02408_close.png`) **+ 2 ffmpeg contact sheets. `grep -ci "fonts.googleapis\|fonts.gstatic" qa-run.log` → 0; same for the re-run log.** |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Gates | demo checker 35/35 + 13/13 | /demo callable only on explicit invocation, narration-key prompt only on a requested video, first-build order deploy → commit → README with no /demo, runtime **84.1s** from live `vo-durations.json` (under 130s hard / 150s absolute), $0 spent under the $10 cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37–#40. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run.

### 3.2 The Playwright installer failed twice — environmental, recovered without touching the plugin

Dry-runs #37–#39 recorded the Playwright CDN closing the connection at ~90%; dry-run #40 got through on a retry. This run hit the same failure **twice**: `npx playwright install chromium-headless-shell` (revision 1243, Chrome Headless Shell 153.0.8010.12, 114.3 MiB) failed at ~90% on all 5 internal retries, then again on a full second attempt (`pw-install.log`, `pw-install-retry.log`: "Download failed: server closed connection", exit 1 both times). **This is environmental, not a tree defect** — the CDN, not the plugin, closes the connection; the same installer binary worked in #40.

Recovery, all environment-side, no plugin file touched:

1. `curl -L -C -` downloaded the same zip from the same CDN in ~18s, complete (119,809,080 bytes, `zipfile.testzip()` clean, 287 entries) — the CDN serves the file fine to curl; only Playwright's built-in downloader stalls on it (`curl-dl.log`).
2. The zip was extracted by hand into `pw-browsers/chromium_headless_shell-1243/` (the layout Playwright expects); a launch probe confirmed Playwright accepts it (`chromium.launch()` → version 153.0.8010.12, closed OK).
3. `record.mjs` also needs Playwright's ffmpeg binary (`ffmpeg-1011/ffmpeg-linux`); the system ffmpeg (`/usr/bin/ffmpeg`, 8.1.2) was symlinked into that path — Playwright invokes it for video recording only.

Nothing in the template was modified to make the recording work. If the CDN fails again on another machine, the recording step is environment-blocked again — but the font FAIL that `qa.mjs` itself hit is gone regardless: `qa.mjs` uses Remotion's own chrome-headless-shell, and its still renders no longer fetch Google Fonts. A repeat of this leg needs one `npm install`, the curl download above (or a retry of the installer), and the ffmpeg symlink.

### 3.3 A runner bug of mine, found and fixed in the runner (same pattern as #40 §5.1)

The first checker run reported **57/59** with `demo-remotion-qa-live` and `demo-remotion-render-form-live` FAIL — but both live runs had exited 0. Cause: my own exit-code files contained the text `qa exit=0` / `render-help exit=0` instead of the bare `0` the checker parses with `int(...)` (dry-run #40's files held bare `0`). The files were corrected to the actually-observed bare exit codes and the checker re-run to **59/59**. No plugin file, log, or live result was altered; the two FAILs were a harness formatting error, recorded here, not hidden.

### 3.4 What is NOT claimed by the 59/59

- **No full render** (`build.mjs --render` / `npm run all` end-to-end) was run — the stills + contact sheets + A/V table are the verified output; a rendered `demo.mp4` is owed to the live smoke test.
- **The 10-second mix listen was not done** — the fixture has no music bed (`musicBed: false`) and no narration (no voice provider), so there is no mix to listen to. The A/V table (`demo-av-table.md`) is completed from the viewed stills: **all 12 beats' claims match what is on screen** (pantry list shows the six ingredients; week plan shows "6 dinners · $0 extra · 1 pot"; Monday curry 25 minutes; Tuesday chickpea rice 20 minutes; leftover remix; arch diagram shows "static HTML — no runtime code"; close card shows the serif "Pantry Pal" in the self-hosted Instrument Serif face).
- **Record warnings (minor, not BLOCKING):** `capture/marks.json` carries 2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped ("Execution context was destroyed, most likely because of a navigation"). The footage for both beats exists (marks present, stills render); only the mid-shot click actions did not execute — a navigation race in `record.mjs`, not a missing beat. Same warnings as #40. `qa.mjs` itself reports "No BLOCKING findings".
- A live film in Anish's Cursor is still owed by the smoke test, as before — but the sandbox side of it (fonts + recording + QA exit 0) is now proven here again.

## 4. Leg 4 — Cursor-readiness (fix #24): 37/37

Runner `dryrun41-leg4.py` (verbatim copy of the #40 runner except one documented expectation update below; output `dryrun41-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with the same file:line evidence as #40 (picker prerequisite verbatim once in orchestrate step 4; 19 dual-cited agent path lines; general-subagent fallback; all four /demo gates; resume guards; inventory pointers in Taste + ui-ux-pro-max; FILM_F1/F5/F6; F-09 step 6 wording; tts.mjs Windows forms; **13 live C-1 hook pipe tests**: 6 BLOCKED exit 2, 5 ALLOWED exit 0, 1 documented base64 GAP exit 0, 1 sanity BLOCKED exit 2).

**The one runner-expectation update (documented, not hidden):** the first run was **36/37** — `L4-9a tts.mjs Windows PowerShell pip form (comment)` FAILED because the checker asserted the verbatim pre-fix-#26 string `` `py -m pip install piper-tts` ``, while fix #26 §1 pip pinning intentionally changed that comment to `` `py -m pip install piper-tts==1.8.0` `` (`tts.mjs:134–135`; recorded in `fix26/pip-pinning.md:124–125, :189–190`). The Windows PowerShell guidance is still present and correct — now pinned, which is the point of the fix. The checker's expectation was updated in the dry-run copy only (`dryrun41-leg4.py`, with an inline comment citing the pinning record) to assert the pinned form, and the leg re-run to **37/37**. No plugin file was touched. (L4-9b passes unchanged: the `:180` error string was deliberately left unpinned — `pip-pinning.md:191`, reason (b), runtime message not an install step.)

## 5. Leg 5 — Call-graph: 17 EXERCISED, 22 STATIC-OK, 5 DORMANT, 0 BROKEN

Runner `dryrun41-leg5.py` (verbatim copy of the #40 runner; output `dryrun41-leg5-output.txt`, **exit 0**). It reads `fix25/callmap/call-map-data.json` and, for every element, either runs the dispatch path, resolves it statically, or records it dormant/owed. Outcome meanings as in #40. The fix #26 §1–§8 edits caused **no movement** vs #40 except the expected one: the #40 MINOR is gone (see below).

| Category | Count | What was exercised / checked |
|---|---|---|
| Counts agree | 6 STATIC-OK | Map counts 166/72/123/87/15/64 all match the tree (skills dirs, agent files, `.mdc` rules, command files, `hooks.json` events, `skill-triggers@1.json` `triggers` dict) |
| Commands resolve | 86/87 STATIC-OK + 7 reviewed non-dispatch refs | Every command file's named skills/agents/commands resolve. Same 7 refs verified by reading to be non-dispatch mentions as in #40. |
| Skills load | 166/166 STATIC-OK | Every skill has a non-empty `SKILL.md` with frontmatter; map skill keys == tree skill dirs. Live invocation of each on-request skill is OWED. |
| Hooks run live | **15/15 EXERCISED** | Every `hooks.json` event ran with synthetic Cursor-format JSON stdin (cwd = built tree, `HOME` = scratch fake-home, `TMPDIR` redirected): all exit 0 with valid JSON output. Includes `sessionStart` (see ck wire below) and `beforeShellExecution` (dispatches to the C-1 hook, already pipe-tested in Leg 4). |
| Fix #25 wires | 1 EXERCISED (ck) + 2 STATIC-OK + 1 EXERCISED (test-coverage) | **ck: EXERCISED** — `hooks/session-start.js` run on the REAL built tree with fake stdin `{}` and fake `$HOME`: exit 0, output JSON carries the full ck (Context Keeper) brief (7,599 B stdout this run vs 7,573 B in #40 — the fix #26 §8 cost-line corrections change the brief size slightly). **prp-commit: STATIC-OK** — Phase 3 + orchestrate step 6 name `conventional-commit-review` + `ecc-commit-reviewer`; both resolve; live commit drafting OWED. **ecc-recipes: STATIC-OK** — RECIPES_F25 lookup present; skill resolves; all 8 epic/`/prune` commands named; live lookup OWED. **/test-coverage Steps 1–2: EXERCISED** — see §5.1. |
| Uncalled | 52 DORMANT | 24 skills, 21 agents, 7 commands — exactly the map; every one has zero calling invokers. |
| Second-order orphans | 13 DORMANT | 8 skills, 4 agents, 1 command (`/python-review`) — exactly the map; every orphan's invokers resolve to uncalled elements or reference files. |
| Triggers | 64 STATIC-OK | All 64 keys resolve; no live Cursor entry point for the consumer (parent decision item, unchanged — fix #26 §5 records it documentation-only) — live firing OWED. |
| Epic commands | 8 DORMANT-in-use | Reachable through the recipes lookup but dormant IN USE (need a genuine multi-week epic run); not executed here by decision. |

**Paths exercised vs not executed vs owed (summary):** EXERCISED 17 (15 hooks + ck wire + /test-coverage measurement). NOT EXECUTED by decision 65 (52 uncalled + 13 second-order orphans, all with recorded dormant reasons; the 8 epic/`/prune` commands counted inside the reachable set are dormant-in-use). OWED to the live smoke test: live execution of the 87 commands, live invocation of the 166 on-request skills, live commit drafting via prp-commit, live recipes lookup, live trigger firing, and live Cursor behaviour of the ck wire (the scratch + built-tree runs prove the Node mechanics only).

**No MINOR this run.** The dry-run #40 MINOR (`/loop-status` alias) was fixed in fix #25 option (b) and stays fixed: **0 `loop-status` hits** anywhere in the built tree (verified by grep this session).

**Fix #26 §8 verified in the built tree (spot-check, not a leg item):** the ck cost lines now read ~1k tokens/session (`skills/ck/SKILL.md:159`, `skills/ck/hooks/session-start.mjs:6, :90`). The remaining `~100 tokens` at `session-start.mjs:129` is the compact 5-line summary block itself, a different quantity — not the stale line.

**First-run note (companion exercise, same pattern as #40):** the first Leg 5 run reported 16 EXERCISED / 1 BROKEN (`wire:test-coverage` — "no coverage.json from the companion exercise"). That is the runner's check that the companion exercise was run, not a plugin defect. The exercise was then run (§5.1) and the leg re-run to the result above.

### 5.1 /test-coverage Steps 1–2 exercised live

Scratch pytest project `leg5-testcov/` (verbatim copy of the #40 fixture; see `dryrun41-leg5-testcov.md`): `pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py` (5 tests, deliberately not covering `mul` or `untested_helper`). Ran the command's Step 1 detection + Step 2 measurement: `pytest --cov=src --cov-report=json`, **exit 0, 5 passed** — `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly as the wire specifies. Identical outcome to #40. Step 3 generation stays in the fix loop by design and was not run.

### 5.2 Technical-depth fixture: real-time collaborative editor — re-run PASS

Fixture: `fix26/dryrun41/leg5-collab/` (verbatim copy of the #40 fixture — `crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`). Re-run, not rebuilt: the CRDT, server, and demo are unchanged from #40.

- **Results: `test.mjs` 11/11 checks pass, exit 0; `probe.mjs` 6/6 live browser checks pass, exit 0** (type A→B, type B→A, offline divergence, offline merge, cross-collaborator undo, presence badge). Screenshot `demo-shot.png` re-taken by the probe run.
- **Budgets measured again:** keystroke → remote echo p95 3 ms (budget < 150 ms); 100-op burst local insert 2.4 ms / remote apply 0.3 ms (budget < 500 ms); 10,000-char document build 64.9 ms, merge 102.9 ms, converged. All within budget, same order as #40 (echo p95 40–70 ms there — faster this run; localhost timing noise, not a regression).
- No fixture defects found on re-run; nothing was changed in the fixture.

## 6. Environment notes (sandbox, not the plugin)

- `/tmp` was **73% full (370 MB used, 143 MB free)** at session start — `/tmp/ecc-repo-clean` (300 MB), `/tmp/skill-add` (29 MB, pinned clones — never touched), `/tmp/uipro` (30 MB). **No Chrome work used `/tmp`:** `TMPDIR` was redirected to `fix26/dryrun41-scratch/chrome-tmp` for every harness, probe, and Remotion run. Nothing crashed on shared memory. At session end `/tmp` read **0% used** — it was emptied by something outside this run (this run wrote only three small files there, all removed in cleanup); noted, not claimed as this run's doing.
- The Playwright browser install failed twice on the CDN (see §3.2); recovered with a curl download + manual layout + system-ffmpeg symlink. The installer flakiness is the same failure dry-runs #37–#39 recorded.
- **Cleanup performed at the end:** deleted the reinstallable scratch bulk — `demo-sample-video/node_modules/` (665 MB), `demo-sample-video/public/frames/` (187 MB of 2,347 frame JPEGs — regenerable from `capture/out/take.webm` via `frames.mjs`; `src/frames.json` with the 2347 count kept), `scratch-npm-cache/` (295 MB), `pw-browsers/` (376 MB, the downloaded browser binary + zip), `dryrun41-scratch/pylibs/` (pytest-cov install), `dryrun41-scratch/chrome-tmp/` contents, runner scratch `fake-home/` + `chrome-tmp/`, and `/tmp/dryrun41-*.log` + `/tmp/dryrun41-pw-test.mjs`. Kept: all scripts, logs, reports, the fixture `shots.json` + `src/vo-durations.json` + `src/frames.json`, `capture/` (marks + take.webm + failures), `out/qa/` (12 stills + 2 sheets), the collab fixture sources + test/probe outputs + screenshot, and the Leg 5 test-coverage project + `coverage.json`. A repeat of Leg 3 needs one `npm install`, the §3.2 curl download (or a retry of the installer), and the ffmpeg symlink. Total kept: 8.9 MB.
- No servers left running (ports 8323 and 5180 verified dead at the end).

## 7. OWED to the live smoke test — live-only items, never claimed verified

Carried from dry-run #40 §7, plus this run's additions:

- **Benchmark dimension 7 (alignment):** the Campus Eats re-trace cannot be alignment-scored without a live Campus Eats render + browser-qa run (§2.2). Closed as a RECORDED DECISION per fix26/SPEC.md §6, not a pass.
- **Fix #17 R1/R4:** OWED as defined (§2.2). The Home Run render applies iris-opens in a different placement and has no hero loop; a live Campus Eats render implementing #67/#68 would be needed, and none will be built (Anish's Nov 11 call).
- **Live `qa.mjs` exit-0 + live film + rendered `demo.mp4` in Anish's Cursor** (the sandbox side — fonts, recording, QA exit 0 — is now proven again; the Cursor side is not).
- **Measured (not estimated) narration runtime** and the **10-second mix listen** (no voice provider, no bed in the sandbox).
- **Live execution of the 87 commands, live invocation of the 166 on-request skills, live commit drafting, live recipes lookup, live trigger firing, live Cursor behaviour of the ck wire** (§5).
- Prior open items carried forward: D-6 Stop/SessionStart contradiction; C-5 timeout-300 unit; C-6 hook cwd/node/event names; D-9 `.ecc/settings.json` pickup; E-7 gate hook without Git Bash; general-subagent fallback pin behaviour; F-14 post-report /demo stale README (fixed in fix #26 per `fix26/f14-note.md` — the dry-run does not re-verify the fix itself, only that Leg 3's gates still hold); Netlify row touch-up after Dec 4, 2026; fresh bundle needed before any push (do NOT push b2444de).

## 8. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression + fix #23) | 101 | **PASS (101/101)** |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | **PASS on all 17 assertions, 0 flags** |
| 2 — Campus Eats v5 benchmark | 7 dimensions | **6 PASS statically; dimension 7 (alignment) OWED** |
| 3 — /demo gates + Remotion | 59 | **PASS (59/59) — qa.mjs exit 0 twice, 12/12 stills, 0 font requests** |
| 4 — Cursor-readiness (fix #24) | 37 | **PASS (37/37)**, incl. 13 live C-1 hook pipe tests |
| 5 — Call-graph | 45 checks | **17 EXERCISED, 22 STATIC-OK, 5 DORMANT, 0 BROKEN**; no MINOR |
| 5 — Technical depth (collab editor, re-run) | 11 automated + 6 live | **PASS (11/11 + 6/6)**, budgets measured (echo p95 3 ms < 150 ms; burst < 3 ms < 500 ms; 10k doc merged in 102.9 ms) |
| 5 — /test-coverage Steps 1–2 | 1 exercise | **EXERCISED** (calc.py 68.2%, listed below 80%) |

**DRY-RUN #41: PASS** — with benchmark dimension 7 owed (§2.2) and fix #17 R1/R4 owed as defined (§2.2). No BLOCKING finding in any leg. The two first-run non-passes (Leg 4 L4-9a stale verbatim expectation vs the authorized pip pin; Leg 5 test-coverage companion exercise not yet run) were both harness-side, traced to their causes, and re-run green — see §4 and §5.

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-report.md` (this report)
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-fixtures.py` + `dryrun41-fixtures-output.txt` (42/42)
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-f23.py` + `dryrun41-f23-output.txt` (59/59)
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-align.py` + `dryrun41-align-output.txt` (17 PASS, 0 flags) + `status-center-probe.mjs` + `status-center-probe-output.txt` (centers delta 0) + `align-run.log` (52 measurements, 0 console errors, 0 failed requests) + `prior-align-audit-results.json`
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-benchmark.md` (v5 re-trace: 68/66, per-dimension table, dynamic-count re-derivation with the 6–13 range, Dim 7 owed, R1/R4 scope note)
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-demo.py` + `dryrun41-demo-output.txt` (59/59) + `demo-av-table.md` (12/12 beats verified from stills; mix listen unexecuted)
- `~/workspace/hackathon-plugin/fix26/dryrun41/sample-app/` + `demo-sample-video/` (fresh built-template copy + fixture `shots.json` + live `src/vo-durations.json` + `src/frames.json`; `capture/` with marks + take.webm + failures; `out/qa/` with 12 stills + 2 sheets; `node_modules/` + `public/frames/` removed in cleanup — see §6) + `npm-install.log`, `tts-run.log`, `record-run.log`, `frames-run.log`, `qa-run.log`, `qa-run2.log`, `qa-exit.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `pw-install.log`, `pw-install-retry.log`, `curl-dl.log`
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-leg4.py` + `dryrun41-leg4-output.txt` (37/37; L4-9a expectation updated for the pinned piper line — see §4)
- `~/workspace/hackathon-plugin/fix26/dryrun41/dryrun41-leg5.py` + `dryrun41-leg5-output.txt` (17 EXERCISED / 22 STATIC-OK / 5 DORMANT / 0 BROKEN; exit 0) + `leg5-testcov/` + `coverage.json` + `leg5-testcov-run.log` + `dryrun41-leg5-testcov.md`
- `~/workspace/hackathon-plugin/fix26/dryrun41/leg5-collab/` (`crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`, `demo-shot.png`) + `leg5-collab-test-output.txt` (11/11) + `leg5-collab-probe-output.txt` (6/6)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-report.md` + fixture/demo scripts (Dry-run #40 lists reused verbatim except the two documented runner updates in §3.3/§4)
- `build.sh` measured this session: **24,088 lines, md5 `e05bdc66599b694398e11f0d00dfdafd`**; counts **166/72/123/87/15**, triggers **64**; banned terms **0**; Grok pins 54/103, bare 0
