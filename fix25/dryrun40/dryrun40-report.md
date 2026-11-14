# Dry-run #40 — Fix #25 (call map + weave + works, incl. new Leg 5)

- **Date:** 2026-11-13, ~01:33–02:10 CST. Worker: dry-run #40 agent (fix #25), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix25/dryrun40/`. No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run.
- **Verdict: DRY-RUN #40: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run passes all 17 §6 assertions at all 4 widths and all 13 states with 0 flags — the dry-run #39 MINOR (panel-top stagger) is now CLEARED by a declaration; the Campus Eats v5 benchmark passes 6 of 7 dimensions statically, with dimension 7 (alignment) OWED, never passed (no live Campus Eats render exists to measure). Leg 3: **59/59 — the long-standing environmental FAIL is CLEARED**: `qa.mjs` exits 0 twice on the rebuilt plugin with self-hosted template fonts, 12/12 stills rendered, 0 Google Fonts requests. Leg 4: 37/37 Cursor-readiness, incl. the 13 live C-1 hook pipe tests. Leg 5 (NEW, call-graph): 17 paths EXERCISED live, 22 STATIC-OK (live execution owed to the smoke test), 5 DORMANT by decision, 1 MINOR finding (the `/loop-status` alias has no command file); the technical-depth fixture (real-time collaborative editor, sequence CRDT) passes 11/11 automated checks + 6/6 live browser probe checks with measured performance budgets.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae`**. Matches the task's stated gate numbers.
- Diff vs `build.sh.before-fix23`: **+305/−0** (additions only; verified with `diff` `<`/`>` counts, 0 deletions, 305 additions).
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks**, trigger keys **64** (from `manifests/context-packs/skill-triggers@1.json` `triggers` dict).
- Banned terms: **0** in the built tree (independent grep this session over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, excl. `node_modules`, returned no files).
- Audit #72 / Sweep #33 / verify25.py are parallel Phase 3b workers, not re-run here.

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build tree: 42/42

Runner `dryrun40-fixtures.py` is a verbatim copy of `fix24/dryrun39/dryrun39-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun40-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #25 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun40-f23.py` is a verbatim copy of `fix24/dryrun39/dryrun39-f23.py`. Output: `dryrun40-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present.

**Adaptations: none.**

## 2. Leg 2 — Home Run render re-run + Campus Eats v5 benchmark

### 2.1 Render re-run (live, this session): all 17 assertions PASS, 0 flags

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`). Log: `fix25/dryrun40/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].**
- Prior results preserved before the re-run at `fix25/dryrun40/prior-align-audit-results.json` (the harness overwrites `qa/align-audit-results.json` in place).
- Analysis `dryrun40-align.py` (output `dryrun40-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).
- All Chrome work ran with `TMPDIR=<dryrun40>/chrome-tmp` (see §6: `/tmp` was 75% full at session start).

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
| (h) PANELS — tops | **PASS (was MINOR in #39)** | top delta **26px** at 1440, **stagger now DECLARED in the decision record** — see §2.2 |
| COVER_F23 — matrix | PASS | required 39/39 cells present (1440/900/390 × 13 states); bonus width 768 also measured (52 total) |
| COVER_F23 — screenshots | PASS | a screenshot exists for every measured cell (54 shots) |

States covered at every width: home, home-bottom (scrolled), detail, offer, offer-accepted, trip, trip-wrongcode, trip-delivered, branches, trips, you, post, post-done. **No unverified width, no unverified flow state — no BLOCKING coverage gap.**

Fresh vs prior results JSON: identical except **2 measurements** (`1440`/`900-trip-wrongcode`), and only in the individual code-box input rects (3–4px shifts); the group geometry is identical in both (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #38 saw the same pattern in 4 measurements; #39 in 3.)

### 2.2 The dry-run #39 MINOR is CLEARED

**CLEARED — ALIGN_F23_PANELS, desktop side-panel top delta 26px.** The decision record now carries the declaration (`docs/design-tokens.md`, a line tying the stagger to the panels — the align script's `stagger_declared` check, which requires "stagger" and "panel" on the same line, now returns True). This dry-run did not write it (check-only task) — it was present when this run read the file. The 6h assertion now PASSES. Both dry-run #38 MINORs are now cleared (iris-disc bleed cleared in #39, panel-top stagger cleared here). **Leg 2's render half has zero open findings.**

### 2.3 Campus Eats v5 benchmark — 6/7 static PASS, dimension 7 OWED

Full re-trace: `fix25/dryrun40/dryrun40-benchmark.md` (element list, rule traces, per-dimension table). Summary:

- **E's dynamic count of 8 re-derived from the record, item for item** (stepper + live total with the $8→$12 / $10-row-"Fits" probe; Roll a craving; Tried-it stamps; sticker sheet with the Taco-click probe; search bar; marquee pause; sticker-peel; coin stack). **But the boundary is a judgment call, recorded not smoothed over:** E counts state-changing features while excluding pure hover micros (#47–#50, #54) and ambient loops, and no stated distinction separates #60 (peel) and #58 (marquee pause) from the other hover micros. Consistent alternatives from the same record: narrow = **6**, broad = **13**. The beat-v5 criterion (≥ 9) is anchored to E's 8; the re-trace passes it under E's and the broad reading, and would fail under the narrow reading. Cross-surface drives re-derived: **1** (stepper → total + coin stack + $10 row). Live-data surfaces re-derived: **2** (spot list, stepper total). Both stand.
- **Re-trace: 68 literal / 66 stricter** (v5 61/60 + 7 rule-traced additions: #67 iris-opens applied as the section transition, #68 R4 hero loop in the app-frame window, #69 dietary filter chips, #70 budget preset chips, #71 live "N open now" count figure, #72 frosted-glass Effect — the first Effect ever — #73 filter-chip hover micro). Kinds 7 → 8, five kinds above v5.

| # | Dimension | v5 | Re-trace | Result |
|---|---|---|---|---|
| 1 | Element count | 61 / 60 | **68 / 66** | **PASS** (≥ 62 / ≥ 61) |
| 2 | Variety | 7 kinds, Effect 0 | **8 kinds, 5 above v5**, no drops | **PASS** |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop | Full inventory **+ hero loop AND second moment applied** | **PASS (static)**; strength verdict OWED to browser-qa |
| 4 | Motion | 17 / 16 | **19 / 17** | **PASS** (≥ 18 / ≥ 17) |
| 5 | Dynamic interface | 8 items; 1 drive | **10 items; 2 drives** | **PASS (static)**; live behaviour OWED. Sensitivity: fails only under the narrow (6) reading |
| 6 | Functionality | 2 live-data surfaces | **3 surfaces**; mechanism on hero/first screen | **PASS (static)**; live verdict OWED (FUNC-BQA_F23) |
| 7 | Alignment | NONE RECORDED | **— cannot be scored** | **OWED, never passed** |

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7 is OWED.** No live Campus Eats render exists in this workspace (only the v1-era tokens file), so browser-qa cannot run the ALIGN_F23 matrix on it in this sandbox. A leg that cannot score a dimension does not PASS on that dimension — the overall PASS verdict below follows the dry-run #39 precedent (an owed environmental item, not a plugin defect), with the owed dimension stated here, not hidden. The parent may adjudicate otherwise. The Home Run 52-measurement / 0-problem run is live alignment evidence about Home Run, not Campus Eats, and is not counted toward dimension 7.

## 3. Leg 3 — /demo: 59/59 — THE ENVIRONMENTAL FAIL IS CLEARED

Checker `dryrun40-demo.py` (verbatim copy of the #39 checker; output `dryrun40-demo-output.txt`): **59/59 /demo contract checks met, exit 0** — 35/35 original contract checks, 13/13 removal checks, 11/11 Remotion checks. The one FAIL from dry-runs #37–#39 (`demo-remotion-qa-live`) now PASSES.

### 3.1 The evidence (what actually ran, in order)

Fixture: `fix25/dryrun40/demo-sample-video/` — a **fresh copy of the rebuilt template** from the built tree (diffed against it: byte-identical except the fixture `shots.json`) + the Dry-run #37/38/39 `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block) + `fix25/dryrun40/sample-app/` (Pantry Pal, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards). Template facts in the copy: `package.json` carries `"@remotion/fonts": "4.0.526"` and **no** `@remotion/google-fonts`; `src/fonts.ts` uses `loadFont` + `staticFile('fonts/….woff2')`; `public/fonts/` holds exactly the 3 woff2 files. (`@remotion/google-fonts` still appears as a raw string 2× in `fonts.ts` — the intentional provenance header comment — and 1× in `mobile-ship` prose; zero imports, zero dependencies. That is the build worker's caveat 1, for the audit to decide; it is not a font fetch.)

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund`, cache in dryrun40 scratch (`npm-install.log`) | **exit 0**; `@remotion/fonts` present in `node_modules`, `@remotion/google-fonts` absent |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording | `node scripts/record.mjs` (`record-run.log`) | **exit 0. Take: 75.1s, 8 camera moves.** `capture/marks.json`: all 10 app beats + `__end`; **all 6 feature beats filmed**; `capture/out/take.webm` 4.8 MB. See §3.2 for how the missing browser binary was obtained. |
| Frames | `node scripts/frames.mjs` (`frames-run.log`) | **exit 0. 2263 frames (75.4s).** |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 0 — TWICE.** First run exit 0; re-run (`qa-run2.log`) exit 0 with a clean capture. **"No BLOCKING findings from the automated checks." 12/12 stills rendered** (`out/qa/00111_problem.png` … `02408_close.png`) **+ 2 ffmpeg contact sheets. `grep -ci "fonts.googleapis\|fonts.gstatic" qa-run.log` → 0; same for the re-run log.** |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — `@remotion/cli 4.0.526` |
| Gates | demo checker 35/35 + 13/13 | /demo callable only on explicit invocation, narration-key prompt only on a requested video, first-build order deploy → commit → README with no /demo, runtime **84.1s** from live `vo-durations.json` (under 130s hard / 150s absolute), $0 spent under the $10 cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37–#39. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run.

### 3.2 Why the recording worked this time (environment fix, not a plugin change)

Dry-runs #37–#39 could not run `record.mjs`: the Playwright browser binary was missing (`~/.cache/ms-playwright/chromium_headless_shell-1243/…` did not exist) and the prior runs established the Playwright CDN closes the connection at ~90%. This run tried the install once more — **`npx playwright install chromium-headless-shell` succeeded this time** (log `pw-install.log`: `chromium_headless_shell-1243` + ffmpeg downloaded to `dryrun40/pw-browsers/`, exit 0). Nothing in the template was modified to make it work; the environment changed (the CDN answered). If the CDN fails again on another machine, the recording step is environment-blocked again — but the font FAIL that `qa.mjs` itself hit is gone regardless: `qa.mjs` uses Remotion's own chrome-headless-shell, and its still renders no longer fetch Google Fonts.

### 3.3 What is NOT claimed by the 59/59

- **No full render** (`build.mjs --render` / `npm run all` end-to-end) was run — the stills + contact sheets + A/V table are the verified output; a rendered `demo.mp4` is owed to the live smoke test.
- **The 10-second mix listen was not done** — the fixture has no music bed (`musicBed: false`) and no narration (no voice provider), so there is no mix to listen to. The A/V table (`demo-av-table.md`) is completed from the viewed stills: **all 12 beats' claims match what is on screen** (pantry list shows the six ingredients; week plan shows "6 dinners · $0 extra · 1 pot"; Monday curry 25 minutes; Tuesday chickpea rice 20 minutes; leftover remix; arch diagram shows "static HTML — no runtime code"; close card shows the serif "Pantry Pal" in the self-hosted Instrument Serif face).
- **Record warnings (minor, not BLOCKING):** `capture/marks.json` carries 2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped ("Execution context was destroyed, most likely because of a navigation"). The footage for both beats exists (marks present, stills render); only the mid-shot click actions did not execute — a navigation race in `record.mjs`, not a missing beat. `qa.mjs` itself reports "No BLOCKING findings".
- A live film in Anish's Cursor is still owed by the smoke test, as before — but the sandbox side of it (fonts + recording + QA exit 0) is now proven here.

## 4. Leg 4 — Cursor-readiness (fix #24): 37/37

Runner `dryrun40-leg4.py` (verbatim copy of the #39 runner; output `dryrun40-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with the same file:line evidence as #39 (picker prerequisite verbatim once in orchestrate step 4; 19 dual-cited agent path lines; general-subagent fallback; all four /demo gates; resume guards; inventory pointers in Taste + ui-ux-pro-max; FILM_F1/F5/F6; F-09 step 6 wording; tts.mjs Windows forms; **13 live C-1 hook pipe tests**: 6 BLOCKED exit 2, 5 ALLOWED exit 0, 1 documented base64 GAP exit 0, 1 sanity BLOCKED exit 2).

## 5. Leg 5 — Call-graph (NEW) + technical depth

### 5.1 Call-graph: 17 EXERCISED, 22 STATIC-OK, 5 DORMANT, 1 MINOR

Runner `dryrun40-leg5.py` (output `dryrun40-leg5-output.txt`, **exit 0**). It reads `fix25/callmap/call-map-data.json` and, for every element, either runs the dispatch path, resolves it statically, or records it dormant/owed. Outcome meanings: EXERCISED = actually run in this sandbox; STATIC-OK = the dispatch target resolves in the built tree but executing it needs a live agent / Cursor session (live execution OWED, never claimed); DORMANT = uncalled / second-order orphan per the map, intentionally dormant with a recorded reason (NOT EXECUTED by decision, not a defect); BROKEN = target does not resolve or a runnable hook crashed.

| Category | Count | What was exercised / checked |
|---|---|---|
| Counts agree | 6 STATIC-OK | Map counts 166/72/123/87/15/64 all match the tree (skills dirs, agent files, `.mdc` rules, command files, `hooks.json` events, `skill-triggers@1.json` `triggers` dict) |
| Commands resolve | 86/87 STATIC-OK + 7 reviewed non-dispatch refs | Every command file's named skills/agents/commands resolve. 7 refs verified by reading to be non-dispatch mentions: `/adding-tests` (evolve.md:95 documents them as illustrative example names), `skills/learned/<name>.md` (placeholder path, ×2), `` `/api/…` `` code samples (×3: fetch URLs / route files), `/skill-creator` (GitHub App slash command, external). |
| Skills load | 166/166 STATIC-OK | Every skill has a non-empty `SKILL.md` with frontmatter; map skill keys == tree skill dirs. Live invocation of each on-request skill is OWED. |
| Hooks run live | **15/15 EXERCISED** | Every `hooks.json` event ran with synthetic Cursor-format JSON stdin (cwd = built tree, `HOME` = scratch fake-home, `TMPDIR` redirected): all exit 0 with valid JSON output. Includes `sessionStart` (see ck wire below) and `beforeShellExecution` (dispatches to the C-1 hook, already pipe-tested in Leg 4). |
| Fix #25 wires | 1 EXERCISED (ck) + 2 STATIC-OK + 1 EXERCISED (test-coverage) | **ck: EXERCISED** — `hooks/session-start.js` run on the REAL built tree with fake stdin `{}` and fake `$HOME`: exit 0, output JSON carries `additional_context` with the full ck (Context Keeper) brief (7,573 B stdout). The Node mechanics B proved on scratch now hold on the built tree. **prp-commit: STATIC-OK** — Phase 3 + orchestrate step 6 name `conventional-commit-review` + `ecc-commit-reviewer`; both resolve; live commit drafting OWED. **ecc-recipes: STATIC-OK** — RECIPES_F25 lookup present; skill resolves; all 8 epic/`/prune` commands named; live lookup OWED. **/test-coverage Steps 1–2: EXERCISED** — see §5.2. |
| Uncalled | 52 DORMANT | 24 skills, 21 agents, 7 commands — exactly the map; every one has zero calling invokers (self-definitions, manifest listings, and weak mentions do not count as dispatches). |
| Second-order orphans | 13 DORMANT | 8 skills, 4 agents, 1 command (`/python-review`) — exactly the map; every orphan's invokers resolve to uncalled elements or reference files. |
| Triggers | 64 STATIC-OK | All 64 keys resolve; no live Cursor entry point for the consumer (parent decision item, unchanged) — live firing OWED. |
| Epic commands | 8 DORMANT-in-use | Reachable through the recipes lookup but dormant IN USE (need a genuine multi-week epic run); not executed here by decision. |

**Paths exercised vs not executed vs owed (summary):** EXERCISED 17 (15 hooks + ck wire + /test-coverage measurement). NOT EXECUTED by decision 65 (52 uncalled + 13 second-order orphans, all with recorded dormant reasons; the 8 epic/`/prune` commands counted inside the reachable set are dormant-in-use). OWED to the live smoke test: live execution of the 87 commands, live invocation of the 166 on-request skills, live commit drafting via prp-commit, live recipes lookup, live trigger firing, and live Cursor behaviour of the ck wire (the scratch + built-tree runs prove the Node mechanics only).

**The one MINOR finding — `/loop-status` alias has no command file.** `commands/epic-unblock.md:20–22` declares `/loop-status` as a "Compatibility alias", and `skills/ecc-recipes/SKILL.md:81,142` tells the agent to "watch with `loop-status`" — but no `commands/loop-status.md` exists anywhere in the tree, so `/loop-status` resolves to nothing in Cursor. Pre-existing upstream ECC text (not a fix #25 regression); fix #25's ecc-recipes wire makes the reference newly reachable, which is why this leg surfaces it. One-line follow-up: ship a `loop-status` alias file or reword the two references. It does not fail the leg: every dispatch path in the map itself executes or is dormant by decision.

**Runner bugs found and fixed in the runner, not the plugin (same pattern as #39 §4.2):** the first run reported 12 BROKEN; 11 were script errors, verified one by one against the files: the triggers count read the JSON's 9 top-level keys instead of its 64-entry `triggers` dict; "uncalled has invokers" counted self-definitions (`struct-command`), manifest listings (`shipped`), and weak mentions as dispatches; the second-order check matched invoker basenames instead of resolving them to elements; the command regex caught code paths (`` `/api/…` ``), documented example names, a placeholder path, and an external GitHub App command. All four were fixed in `dryrun40-leg5.py` and the run repeated to the result above. The `/loop-status` item survived all four fixes — it is the real finding.

### 5.2 /test-coverage Steps 1–2 exercised live

Scratch pytest project `leg5-testcov/` (see `leg5-testcov-note.md`): `pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py` (5 tests, deliberately not covering `mul` or `untested_helper`). Ran the command's Step 1 detection + Step 2 measurement: `pytest --cov=src --cov-report=json`, **exit 0, 5 passed** — `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly as the wire specifies. Step 3 generation stays in the fix loop by design and was not run.

### 5.3 Technical-depth fixture: real-time collaborative editor — PASS

Fixture: `fix25/dryrun40/leg5-collab/` — `crdt.js` (sequence CRDT, RGA-style), `server.js` (dependency-free WebSocket sync server + append-only op log), `demo.html` (two live clients, presence, offline toggle, undo, paste/burst controls), `test.mjs` (automated checks), `probe.mjs` (live browser probe), `demo-shot.png` (screenshot).

- **Architecture (named):** two browser clients ↔ WebSocket sync server; op log (`ops.jsonl`, append-only, replayed on connect/reconnect) + presence channel (ephemeral, never logged); state lives in each client's replica, the server holds only the log.
- **Algorithm (named, with invariant):** RGA sequence CRDT — each character is a node `{id: "lamport:client", left, char, deleted}`; document order is a pre-order traversal of the parent tree with siblings sorted by id descending. **Invariant: any two replicas that applied the same op set, in any order, hold the identical document.** Deletes are tombstones, so id-addressed undo never disturbs another collaborator's text.
- **System design:** presence (cursor position broadcast per keystroke, shown as a live badge); persistence (document survives a client reload via the server op log; the log survives a server restart); reconnect + merge (offline client queues ops, flushes on reconnect, re-syncs from the log); no permissions claimed (fixture does not implement them — recorded, not implied).
- **Performance budget (named + measured):** keystroke → remote echo **< 150 ms on localhost** — measured median 2–3 ms, p95 40–70 ms across two runs (20 keystrokes each, live WebSocket); **100-op burst applies in < 500 ms** — measured 0.8–0.9 ms local insert, 0.2–0.4 ms remote apply; **10,000-char document** — build 91.6 ms, merge 24.6 ms, converged.
- **Edge cases exercised (≥ 3, each with evidence):** (1) simultaneous insert at the same position by two clients → converged ("worldHELLO" on both); (2) out-of-order delivery — 200 ops shuffled (seeded) + 40 interleaved deletes → identical to the in-order replica (140 chars); (3) offline-then-reconnect merge — both sides edit while disconnected, reconnect, merge with no edits lost; (4) cross-collaborator undo — A undoes its insert after B typed after it, B's text survives, replicas agree; undo-of-delete restores only that char; (5) large paste (5,000 chars) while a collaborator types → converged at 5,019 chars, paste intact.
- **Results: `test.mjs` 11/11 checks pass, exit 0; `probe.mjs` 6/6 live browser checks pass, exit 0** (type A→B, type B→A, offline divergence, offline merge, cross-collaborator undo, presence badge). Screenshot `demo-shot.png` shows both panes converged on the identical 38-char document with presence badges and stats.
- **Bugs the tests caught (fixed in the fixture, recorded honestly):** out-of-order deletes were silently lost (a `del` arriving before its `ins` found no node and vanished) — fixed with pending-tombstone sets; the recursive tree walk overflowed the stack at 10k depth — fixed with an iterative pre-order walk; sequential char-by-char inserts were O(n²) (10k build took 22.2 s) — fixed with an `insertAfter` primitive that chains left-ids (build now 91.6 ms). The demo had two further bugs caught by the probe: a missing `</script>` tag (parse error) and a node-based caret restore that destroyed the caret on every render, reversing typed text — fixed with offset-based caret preservation and a non-destructive presence badge. All three test runs and both probe runs are in the logs; the final run is green on every check.

This is real architecture and algorithmic substance, not a thin demo: the fixture's own tests failed three times on real defects (lost deletes, stack overflow, quadratic build) and each was fixed in the CRDT, not in the test expectations.

## 6. Environment notes (sandbox, not the plugin)

- `/tmp` was **75% full (381 MB used, 132 MB free)** at session start — `/tmp/ecc-repo-clean` (300 MB, fix #24 coordinator scratch, left in place), `/tmp/skill-add` (39 MB, pinned clones — never touched), `/tmp/uipro` (30 MB). **No Chrome work used `/tmp`:** `TMPDIR` was redirected to `fix25/dryrun40/chrome-tmp` for every harness, probe, and Remotion run. Nothing crashed on shared memory.
- The Playwright browser install succeeded this run where dry-runs #37–#39 recorded a CDN failure (see §3.2).
- One cleanup slip, recorded: stopping the sample-app server with `pkill -f "http.server 5180"` also matched my own shell command line and SIGTERMed my own exec session; the server itself was stopped (verified: port 5180 dead, no `http.server` processes). No work was lost.
- **Cleanup performed at the end:** deleted the reinstallable scratch bulk — `demo-sample-video/node_modules/` (~800 MB with the Remotion install), `npm-cache/` (295 MB), `pw-browsers/` (266 MB, the downloaded browser binary), `pylibs/` (17 MB, pytest-cov install), `chrome-tmp/` contents, and `/tmp/dbg*.mjs`. Kept: all scripts, logs, reports, the fixture `shots.json` + `src/vo-durations.json`, `capture/` (marks + take.webm + frames), `out/qa/` (12 stills + 2 sheets), the collab fixture sources + test/probe outputs + screenshot, and the Leg 5 test-coverage project + `coverage.json`. A repeat of Leg 3 needs one `npm install` (network worked) and one `npx playwright install chromium-headless-shell`.

## 7. OWED to the live smoke test — live-only items, never claimed verified

Carried from dry-run #39 §5, plus this run's additions:

- **Benchmark dimension 7 (alignment):** the Campus Eats re-trace cannot be alignment-scored without a live Campus Eats render + browser-qa run (§2.3).
- **Live `qa.mjs` exit-0 + live film + rendered `demo.mp4` in Anish's Cursor** (the sandbox side — fonts, recording, QA exit 0 — is now proven; the Cursor side is not).
- **Measured (not estimated) narration runtime** and the **10-second mix listen** (no voice provider, no bed in the sandbox).
- **Live execution of the 87 commands, live invocation of the 166 on-request skills, live commit drafting, live recipes lookup, live trigger firing, live Cursor behaviour of the ck wire** (§5.1).
- **The `/loop-status` alias** (MINOR finding, §5.1) — needs a one-line follow-up, not a smoke-test run.
- Prior open items carried forward: D-6 Stop/SessionStart contradiction; C-5 timeout-300 unit; C-6 hook cwd/node/event names; D-9 `.ecc/settings.json` pickup; E-7 gate hook without Git Bash; general-subagent fallback pin behaviour; F-14 post-report /demo stale README (parent call); Netlify row touch-up after Dec 4, 2026; pip pinning; fix #17 R1/R4 unverified; fresh bundle needed before any push (do NOT push b2444de).

## 8. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression + fix #23) | 101 | **PASS (101/101)** |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | **PASS on all 17 assertions, 0 flags; both #38 MINORs now CLEARED** |
| 2 — Campus Eats v5 benchmark | 7 dimensions | **6 PASS statically; dimension 7 (alignment) OWED** |
| 3 — /demo gates + Remotion | 59 | **PASS (59/59) — the environmental FAIL is CLEARED; qa.mjs exit 0 twice, 12/12 stills, 0 font requests** |
| 4 — Cursor-readiness (fix #24) | 37 | **PASS (37/37)**, incl. 13 live C-1 hook pipe tests |
| 5 — Call-graph | 45 checks | **17 EXERCISED, 22 STATIC-OK, 5 DORMANT, 1 MINOR** (`/loop-status` alias); exit 0 |
| 5 — Technical depth (collab editor) | 11 automated + 6 live | **PASS (11/11 + 6/6)**, budgets measured (echo p95 40–70 ms < 150 ms; burst < 1 ms < 500 ms; 10k doc merged in 24.6 ms) |
| 5 — /test-coverage Steps 1–2 | 1 exercise | **EXERCISED** (calc.py 68.2%, listed below 80%) |

**DRY-RUN #40: PASS** — with benchmark dimension 7 owed (§2.3) and one MINOR finding (`/loop-status` alias, §5.1). No BLOCKING finding in any leg.

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-report.md` (this report)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-fixtures.py` + `dryrun40-fixtures-output.txt` (42/42)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-f23.py` + `dryrun40-f23-output.txt` (59/59)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-align.py` + `dryrun40-align-output.txt` (17 PASS, 0 flags) + `status-center-probe.mjs` + `status-center-probe-output.txt` (centers delta 0) + `align-run.log` (52 measurements, 0 console errors, 0 failed requests) + `prior-align-audit-results.json`
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-benchmark.md` (v5 re-trace: 68/66, per-dimension table, dynamic-count re-derivation with the 6–13 range)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-demo.py` + `dryrun40-demo-output.txt` (59/59) + `demo-av-table.md` (12/12 beats verified from stills; mix listen unexecuted)
- `~/workspace/hackathon-plugin/fix25/dryrun40/sample-app/` + `demo-sample-video/` (fresh built-template copy + fixture `shots.json` + live `src/vo-durations.json`; `capture/` with marks + take.webm; `out/qa/` with 12 stills + 2 sheets; `node_modules/` removed in cleanup — see §6) + `npm-install.log`, `tts-run.log`, `record-run.log`, `frames-run.log`, `qa-run.log`, `qa-run2.log`, `qa-exit.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `pw-install.log`
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-leg4.py` + `dryrun40-leg4-output.txt` (37/37)
- `~/workspace/hackathon-plugin/fix25/dryrun40/dryrun40-leg5.py` + `dryrun40-leg5-output.txt` (17 EXERCISED / 22 STATIC-OK / 5 DORMANT / 1 MINOR; exit 0) + `leg5-testcov/` + `coverage.json` + `leg5-testcov-run.log` + `leg5-testcov-note.md`
- `~/workspace/hackathon-plugin/fix25/dryrun40/leg5-collab/` (`crdt.js`, `server.js`, `demo.html`, `test.mjs`, `probe.mjs`, `demo-shot.png`) + `leg5-collab-test-output.txt` (11/11) + `leg5-collab-probe-output.txt` (6/6)
- `~/workspace/hackathon-plugin/fix24/dryrun39-report.md` + fixture/demo scripts (Dry-run #39 lists reused verbatim)
- `build.sh` measured this session: **24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae`**, diff **+305/−0**; counts **166/72/123/87/15**, triggers **64**; banned terms **0**
