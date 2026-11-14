# Dry-run #39 — Fix #24 (re-weave + dial in for Cursor)

- **Date:** 2026-11-13, ~06:05–06:40 CST. Worker: dry-run #39 agent (fix #24), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix24/dryrun39/`. No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone. `fix11/fix11-stage.py` never run.
- **Verdict: DRY-RUN #39: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run through the tightened §6 assertions passes every directly-measured assertion at all 4 widths and all 13 states, with coverage complete; one MINOR finding (the pre-documented panel-top stagger, still undeclared — see §3.3); the other dry-run #38 MINOR (iris-disc bleed) is now CLEARED by a declaration in the decision record. Leg 3: /demo gates all pass (58/59 checks; the single FAIL is the known environmental caveat, a live `qa.mjs` exit-0 owed to the live smoke test — see §4.3). Leg 4 (NEW, Cursor-readiness): 37/37 statically-checkable fix #24 behaviors pass; the live-only items are listed as OWED in §5, never claimed verified. verify24.py re-run this session: **105/105, exit 0**.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,070 lines, md5 `b0b2645a7d647f96296f9e9c45e09ef5`**. Matches the task's stated gate numbers.
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** (`hooks/hooks.json` `hooks` list = 15); trigger keys **64** (same computation verify24 uses: `coverage.withTriggers == len(triggers) == 64`).
- Banned terms: **0** in the built tree (independent grep this session over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, excl. `node_modules`, returned no files; verify24 also passes this).
- verify24.py re-run this session: **105/105 checks pass, exit 0** (full output: `fix24/dryrun39/verify24-run.log`). Prior verifiers at their expected tails, as recorded by verify24 itself (fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76, fix20 164/169, fix21 96/102, fix22 366/369, fix23 196/211 excl. manifest).
- Audit #71 ZERO blocking / Sweep #32 CLEAN taken as given from the task (not re-run by this worker; verify24 + this dry-run are the independent legs).

## 1. Leg 1 — Fixtures: 101/101

### 1.1 Dry-run #37 list, re-run verbatim against the build #4 tree: 42/42

Runner `dryrun39-fixtures.py` is a verbatim copy of `fix23/dryrun38/dryrun38-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun39-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. No fixture findings; fix #24 changed nothing under these checks.

### 1.2 Fix #23 fixtures, re-run verbatim: 59/59

Runner `dryrun39-f23.py` is a verbatim copy of `fix23/dryrun38/dryrun38-f23.py` (the task names only the #37-list copy, but the fix #23 list is the regression leg for the tightened §6 rules, so it was re-run too — same method, no adaptation). Output: `dryrun39-f23-output.txt`, **59/59 fix #23 fixture expectations met, exit 0**. All verbatim anchors still present, including the type-audit thresholds, the ambition/memorability paragraphs, the alignment assertions, and the inventory currency rule.

**Adaptations: none.** No fixture referenced text fix #24 intentionally changed, so no fixture was adapted. (The fix #24 rewordings — orchestrate step 6 F-09, FILM_F tokens, picker pointer — sit outside both fixture runners' anchors.)

## 2. Leg 2 — Home Run render re-run through the tightened §6 assertions

### 2.1 What ran (live, this session) — and the environment fault found first

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`; fonts are local static woff2, no network needed). Log: `fix24/dryrun39/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].**
- Prior results preserved before the re-run at `fix24/dryrun39/prior-align-audit-results.json` (the harness overwrites `qa/align-audit-results.json` in place).
- Analysis `dryrun39-align.py` (output `dryrun39-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).

**Environment fault (sandbox, not the plugin or the render):** the first three harness runs all crashed with `page.goto: Page crashed` at the first navigation, and probes showed the renderer dying within ~300–500 ms of commit whenever `app.js` executed, while the same page survived 3 s+ with JavaScript disabled and survived with `app.js` route-blocked. Direct shell invocation gave the cause: `Less than 64MB of free space in temporary directory for shared memory files: 19` — **`/tmp` is 97% full (20 MB free of 512 MB)**, filled by fix #24 coordinator scratch (`/tmp/ecc-repo-clean` 300 MB, `/tmp/fix24-test2` 56 MB, `/tmp/fix24-test` 56 MB, `/tmp/skill-add` 39 MB, `/tmp/uipro` 30 MB). Chrome's shared-memory files need `/tmp` space; with 20 MB free the renderer crashes on load. Nothing in the render or the plugin changed — dry-run #38 ran when `/tmp` had room. I did **not** delete anyone's scratch. Workaround, same harness method otherwise: ran the harness (and all later Chrome work) with `TMPDIR=<dryrun39>/chrome-tmp` (a directory on the 145 GB-free home disk). The harness then ran clean, exit 0. Flag for the parent: `/tmp` hygiene before the next Chrome-dependent run — the same fault would hit the live `qa.mjs` / record steps in Leg 3 and any smoke-test work in this VM.

### 2.2 Per-assertion results (fresh run, 52 measurements = 4 widths × 13 states)

| Assertion | Result | Measurement |
|---|---|---|
| (a) OVERFLOW — doc | PASS | `docOverflowX == 0` in 52/52 |
| (a) OVERFLOW — leaf text | PASS | 0 leaf text elements with `scrollWidth > clientWidth + 1` |
| (b) CENTER — phone frame | PASS | `viewportCenterOffset` 0 at all 52 (max \|offset\| 0) — incl. 900/768 stacked |
| (c) NAV — gaps / labels / bar | PASS | adjacent tab gaps equal ±2px in 52/52; every label center == tab center; tabbar centered in phone ±2px in 52/52 |
| (d) GRID — children + feed cards | PASS | full-width children share one left/right edge ±2px; narrower children left-aligned or centered, in 52/52; feed cards share one left/right edge per width |
| (e) CLIP — beyond frame | **PASS (was MINOR in #38)** | `.iris-disc` beyond the phone frame in 8 measurements (trip + trip-wrongcode × 4 widths); bleed now DECLARED in the decision record — see §2.3 |
| (f) LABELS — SVG / stamps / status | PASS | route-map + branch-strip: 0 overlaps, 0 out-of-bounds in 52/52; stamp offsets all 0 (n=12); statusbar insets symmetric; **status vertical centers delta 0 at 1440/900/390** (probe: time h=22 vs icons h=12 explains the 5px top difference) |
| (g) ACTIONS — code boxes | PASS | code-box group offset on its panel 0 in all 8 trip measurements |
| (h) PANELS — gutters | PASS | desktop gutters symmetric 44/44 in 13/13 at 1440 |
| (h) PANELS — tops | **FLAG (MINOR)** | top delta **26px** at 1440 (left top 232 vs right top 206), no stagger recorded — see §2.3 |
| COVER_F23 — matrix | PASS | required 39/39 cells present (1440/900/390 × 13 states); bonus width 768 also measured (52 total) |
| COVER_F23 — screenshots | PASS | a screenshot exists for every measured cell (54 shots) |

States covered at every width: home, home-bottom (scrolled), detail, offer, offer-accepted, trip, trip-wrongcode, trip-delivered, branches, trips, you, post, post-done. **No unverified width, no unverified flow state — no BLOCKING coverage gap.**

Fresh vs prior results JSON: identical except 3 measurements (`1440`/`768`/`390-trip-wrongcode`), and only in the individual code-box input rects (1–4px shifts); the group geometry is identical in all 3 (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged. (Dry-run #38 saw the same pattern in 4 measurements.)

### 2.3 The two dry-run #38 MINOR findings — one cleared, one still open

1. **CLEARED — ALIGN_F23_CLIP, `.iris-disc` beyond the phone frame.** The decision record now carries the declaration (`docs/design-tokens.md:202–205`): "Declared bleed (ALIGN_F23_CLIP): the iris ring intentionally expands beyond the phone frame during the 0.7s open (scale 1.6 end-state) and is invisible at rest (opacity 0, pointer-events none); page overflow stays 0 at all widths." That is exactly the clearing text dry-run #38 proposed. This dry-run did not write it (check-only task) — it was present when this run read the file. The 6e assertion now PASSES.
2. **MINOR (unchanged) — ALIGN_F23_PANELS, desktop side-panel top delta 26px.** Left panel top 232, right panel top 206 at 1440, in all 13 states. Cause is not drift: `.desk` is `display: flex; align-items: center` (`styles.css:87–88`), so the panels are vertically centered; left h=436, right h=489, and (489−436)/2 = 26.5 ≈ 26. Gutters are symmetric 44/44. What is missing is one recorded line stating the panels are vertically centered (so tops differ by height) rather than top-aligned. The 900/768 numbers (−548) are meaningless in the stacked layout and were not asserted. Clearing text (for the coordinator, same as #38): a decision-record line that the desk vertically centers the flanking panels.

Strict-reading note, recorded honestly: under a strict literal reading of ALIGN_F23_PANELS ("tops aligned ±2px unless a stagger is recorded"), this item flags because the declaration is absent. I classify it MINOR rather than blocking because there is no visible defect (vertically-centered panels with symmetric gutters), it was pre-documented as a conditional before this dry-run, and the only blocking criterion the task names for this leg is an unverified width or state, of which there are none. The parent may adjudicate it as blocking; the one-line clearing text above is the fix in either case.

## 3. Leg 3 — /demo gates

### 3.1 Gates (each PASS, with file:line evidence)

| Gate | Result | Evidence |
|---|---|---|
| /demo callable ONLY on explicit invocation — 0 auto-invocations anywhere in the pipeline | PASS | 13/13 removal checks in the demo checker; `skills/orchestrate/SKILL.md` step 5d `DEMOGATE_O4_F22` + "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline"; step 6 `DEMOGATE_O9_F22` + "A demo video is filmed only when the user invokes `/demo` explicitly"; `skills/orch-build-mvp/SKILL.md` `DEMOGATE_B2S1_F22` + "`/demo` is not filmed here"; `skills/orch-change-feature/SKILL.md` `DEMOGATE_B3S1_F22`; `rules/hackathon-mode.mdc:12` `DEMOGATE_H2_F22` + "/demo is never part of this sequence"; `commands/demo.md` still dispatches all `/demo` forms to pitch-deck-video (explicit path intact); `skills/pitch-deck-video/SKILL.md` carries no DEMOGATE token (removal did not touch it); fix #24 `build.sh` blocks add no auto-invocation wording (verify24 passes the /demo-gate checks) |
| Narration-key prompt fires ONLY when the user asked for a demo video | PASS | `skills/orchestrate/SKILL.md` step 0: "ONLY when the user asked for a demo video" + "If the user did NOT ask for a demo video, do NOT send this prompt"; `rules/hackathon-mode.mdc` §7: "only when the user asked for a demo video" + same guard; `skills/orch-build-mvp/SKILL.md` `DEMOGATE_B2S7_F22` with the same condition (also re-checked statically in Leg 4, L4-4d) |
| Contract intact — first-build sequence is deploy → commit → README, no /demo in it | PASS | `rules/hackathon-mode.mdc:12`: end-of-project run is "(after deploy, commit, and README)" with no `/demo` in the §3 sequence; `rules/hackathon-mode.mdc:12` full sequence ends "deploy → README → final report" with "/demo is never part of this sequence"; `skills/orchestrate/SKILL.md` step 6 order sentence (`DEMOGATE_O9_F22`) |
| Runtime hard cap under 2:10 (130s) from narration, absolute max 2:30 (150s) | PASS (with the estimated-duration caveat below) | Fixture total **84.1s** from live `src/vo-durations.json` (LEAD 0.7 + sum(dur+gap) 81.7 + TAIL 1.7), under 130s and within 150s; `music.gain.under` 0.14 (≤ 0.20); opener earns its seconds from the Wow budget inside the cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-runs #37/#38. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run. The voice rules themselves hold statically (default Rachel `21m00Tcm4TlvDq8ikWAM`, no key written anywhere, fallback chain present) and the fixture spent $0 under the $10 cap.

### 3.2 Live-vs-not-executed record (exactly what ran, and what did not)

Fixture: `fix24/dryrun39/sample-app/` ("Pantry Pal", `index.html` + `plan.html`, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards) and `fix24/dryrun39/demo-sample-video/` (fresh copy of the build #4 `pitch-deck-video/template/` + the Dry-run #37/38 `shots.json`: 12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme pulled from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block with opener concept 5 + "Editorial light" + 3 kinetic-type rows + 2 camera-move rows). The template copy diffed against the built template is byte-identical except the fixture `shots.json` (which replaces the template's Acme `shots.json`) — the same shape as the prior runs. Both HTTP servers started for the exercises (8323 render, 5180 sample app) were stopped after use.

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund` with npm cache in dryrun39 scratch (`npm-install.log`) | **exit 0, 257 packages added** (same count as the prior runs) |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording (filming entry point) | `node scripts/record.mjs` (`record-run.log`) | **exit 1 at `chromium.launch()`**: "Executable doesn't exist at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`". Entry point resolves; only the Playwright browser binary is missing. Playwright install was NOT re-attempted (the prior runs already established the CDN closes the connection at ~90%). Environmental, same as the prior runs. |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 1 — the known environmental caveat (see §3.3).** Prints "rendering 12 stills…", then fails on `Command failed: npx -p @remotion/cli@4.0.526 remotion still …` — the `-p` invocation resolved and ran; the inner still render failed on the runtime Google Fonts fetch. |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** — prints the `remotion render` usage (the `build.mjs` render form). |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Network control | `curl` to the font URL | Reachable via curl (404 on a placeholder path = server responds); only Chrome's direct fetch fails in this sandbox (same control as rerun2/#38). |

**Not executed live (no footage, no render, no video):** filming (`record.mjs` take — blocked on the missing Playwright binary, environment), `frames.mjs`, the Remotion render (`build.mjs --render` / `npm run all` end-to-end), contact sheets, the 10-second mix listen (no bed, no rendered video), and the per-beat A/V stills verification. The A/V table in `demo-av-table.md` is completed as far as the app source allows; all stills cells remain **UNVERIFIED (no stills)** — `out/qa/` is empty. Music fetch: not attempted (`yt-dlp` is not installed; the skill's design is warn-and-continue without a bed).

Note: the `qa.mjs` / Remotion runs in this leg also used `TMPDIR=<dryrun39>/chrome-tmp` (see §2.1) — without it Chrome would have crashed on the full `/tmp` before even reaching the fonts fetch.

### 3.3 The single failing check — 58/59, environmental (OWED, not a plugin FAIL)

Checker `dryrun39-demo.py` (verbatim copy of the #38 checker; output `dryrun39-demo-output.txt`): **58/59 /demo contract checks met** — 35/35 original contract checks, 13/13 removal checks, 10/11 Remotion checks. The one FAIL is **`demo-remotion-qa-live`: `node scripts/qa.mjs` exits 1, not 0.**

Attribution (verified live, same as #38): the `-p` invocation resolves and executes — no "could not determine executable to run" anywhere in `qa-run.log`; Remotion launches, bundles the composition, and begins rendering ("rendering 12 stills…"). The exit-1 cause is the composition's **runtime Google Fonts fetch**: the template's `src/fonts.ts` loads Hanken Grotesk / Instrument Serif / JetBrains Mono via `@remotion/google-fonts`, which fetches from `fonts.gstatic.com` at render time; inside Chrome in this sandbox that fetch fails (`net::ERR_SSL_PROTOCOL_ERROR` on all three woff2 files, `qa-run.log`) while the same host responds via `curl`. Per the task, this is **an owed item for the live smoke test in Anish's Cursor, not a FAIL** of the /demo gates: the invocation path, the removal gates, the contract, and the runtime cap all hold; a live film and a full live `qa.mjs` exit-0 are not provable in this sandbox. The template's live font fetch (vs the plugin's self-hosted-static-fonts stance) remains the coordinator's open observation from rerun2 — flagged, not fixed, by this dry-run.

## 4. Leg 4 — Cursor-readiness (fix #24, NEW): 37/37

Runner `dryrun39-leg4.py` (output `dryrun39-leg4-output.txt`, **37/37, exit 0**). Every check was verified from the built-tree files or from a command run this session, with file:line evidence below. verify24.py (105/105 this session) independently asserts most of these; the Leg 4 runner re-checks them with its own assertions plus the live C-1 hook pipe tests.

| # | Check | Result | Evidence |
|---|---|---|---|
| L4-1a | Picker prerequisite verbatim once in the built tree (orchestrate step 4) | PASS | `skills/orchestrate/SKILL.md:85` — "Select **Grok 4.7 High** in Cursor's model picker before the first build — the orchestrator itself runs as Grok 4.7 High (`grok-4.7-high`) — or the design pin may silently fall back to another model." Count in orchestrate = 1 |
| L4-1b | Picker pointers only elsewhere | PASS | "see the picker note in step 4" ×3 in orchestrate (:14, :24, :119); "see the picker note in orchestrate SKILL.md step 4" in `skills/orch-build-mvp/SKILL.md:41`; "see the picker note in `skills/orchestrate/SKILL.md` step 4" in `README.md:68` |
| L4-2a | Exactly 19 dual-cited agent path lines in commands/ | PASS | Count = 19 (same regex as verify24) |
| L4-2b | plan.md:199 house form, not doubled | PASS | "Use the `architect` agent (`agents/ecc-architect.md`) only when…" present once; no doubled parenthetical |
| L4-2c | No path-only Agent lines left in commands/ | PASS | 0 occurrences of `- Agent: \`agents/ecc-` |
| L4-3 | General-subagent fallback paragraph in common-agents.mdc | PASS | "## If a named agent does not resolve (fix #24)" + "spawn a general subagent on `cursor-grok-4.6-high-fast`" |
| L4-4a | /demo never automatic (O4 + H2) | PASS | DEMOGATE_O4_F22 in orchestrate + "NEVER dispatched by this pipeline"; DEMOGATE_H2_F22 in hackathon-mode + "/demo is never part of this sequence" |
| L4-4b | /demo explicit invocation only (O9) | PASS | DEMOGATE_O9_F22 + "A demo video is filmed only when the user invokes `/demo` explicitly" (orchestrate step 6 + :348) |
| L4-4c | /demo not filmed in orch-build-mvp / orch-change-feature | PASS | DEMOGATE_B2S1_F22 + "`/demo` is not filmed here"; DEMOGATE_B3S1_F22 |
| L4-4d | Narration-key prompt ONLY when a demo video was asked for | PASS | "ONLY when the user asked for a demo video" + "If the user did NOT ask for a demo video, do NOT send this prompt" (orchestrate step 0); same guard in hackathon-mode §7; DEMOGATE_B2S7_F22 in orch-build-mvp |
| L4-4e | First-build order deploy → commit → README, no /demo | PASS | "Order: verify → polish → deploy → commit → README → final report" (orchestrate step 6); "deploy → commit → README" (hackathon-mode) |
| L4-5a–c | Resume guards in orchestrate steps 0–2 | PASS | :58 "Resume guard (fix #24)" + "do NOT re-grill"; :60 "if `docs/scope.md` already exists, verify it and proceed — do NOT re-run `hackathon-scope`"; :61 "if the planner-approved list already exists … do NOT re-run Phases 0–3" |
| L4-5d | Grill-me handoff line | PASS | `skills/grill-me/SKILL.md` "After Grilling": "orchestrate does not re-grill" + "orchestrate steps 0–2 verify the record, scope, and expansion briefs exist and do not re-run them" |
| L4-6a | Inventory pointer in Taste step 4a | PASS | "Read `new-skills/orchestrate/references/design-inventory.md` FIRST — before any deal" (Taste SKILL.md step 4a, also :256) |
| L4-6b | Inventory pointer in ui-ux-pro-max | PASS | "read the design inventory (`skills/orchestrate/references/design-inventory.md`)" (`skills/ui-ux-pro-max/SKILL.md:91`) |
| L4-7a | FILM_F1/FILM_F5/FILM_F6 in pitch-deck-video | PASS | "coverage (FILM_F1)" :241; "the per-beat A/V table (FILM_F5)" :404; "never extra runtime (FILM_F6)" :405 |
| L4-7b | No bare film (F1)/(F5)/(F6) left in pitch-deck-video | PASS | "coverage (F1)" absent; "(F5)" and "(F6)" absent from the skill |
| L4-8a | F-09 orchestrate step 6 wording | PASS | "`readme-writer` reads the deployed URL from the ledger and, if a video was filmed, the video file path `<app-name>-video/out/demo.mp4`" (orchestrate SKILL.md:97) |
| L4-8b | readme-writer reads URL/video path from the ledger | PASS | "take them from `.hackathon/run-ledger.md`" (`skills/readme-writer/SKILL.md:95`) |
| L4-9a–c | tts.mjs Windows forms | PASS | :134 comment "(Windows PowerShell: `py -m pip install piper-tts`)"; :180 error string "(Windows PowerShell: py -m pip install piper-tts)"; `process.env.USERPROFILE` fallback in the piper models dataDir |
| L4-10 | C-1 hook pipe tests (`scripts/hooks/block-no-verify.js`, Cursor-format JSON on stdin) | PASS | 6 BLOCKED cases exit 2, 5 ALLOWED cases exit 0, 1 documented GAP exit 0, 1 sanity case exit 2 — see §4.1 |

### 4.1 C-1 hook pipe tests (run live this session)

Hook input is Cursor-format JSON `{"tool_input": {"command": "..."}}` piped to `node scripts/hooks/block-no-verify.js`; exit 2 = blocked, 0 = allowed.

| Command fed to the hook | Expected | Observed |
|---|---|---|
| `powershell -Command "git commit --no-verify -m test"` | BLOCKED (2) | **exit 2** |
| `powershell -c "git commit --no-verify -m test"` | BLOCKED (2) | **exit 2** |
| `pwsh -Command "git push --no-verify"` | BLOCKED (2) | **exit 2** |
| `cmd /c git commit --no-verify -m test` | BLOCKED (2) | **exit 2** |
| `cmd /c "git commit -n -m test"` (short flag) | BLOCKED (2) | **exit 2** |
| `powershell -Command "git commit --no-veri -m test"` (long-flag prefix) | BLOCKED (2) | **exit 2** |
| `powershell -Command "git commit -m test"` (clean) | ALLOWED (0) | **exit 0** |
| `powershell -Command "npm test"` | ALLOWED (0) | **exit 0** |
| `cmd /c git push origin main` (clean) | ALLOWED (0) | **exit 0** |
| `cmd /c npm run build` | ALLOWED (0) | **exit 0** |
| `git commit -m test` (plain clean) | ALLOWED (0) | **exit 0** |
| `git commit --no-verify -m test` (plain bypass, sanity) | BLOCKED (2) | **exit 2** |
| `powershell -EncodedCommand <base64 UTF-16LE of "git commit --no-verify -m test">` | **NOT blocked (documented gap)** | **exit 0** — confirmed: the scanner cannot read base64, exactly as documented in the hook source (`powershellRole`) and `fix24/MANIFEST.md` §6. Recorded as a gap, not a pass of the blocking behavior. |

### 4.2 Runner bug fixed in the runner, not the plugin (same pattern as dry-run #38 §2.3)

One checker error, fixed in `dryrun39-leg4.py`; the built text was correct: the L4-1b check asserted the orch-build-mvp pointer as "see the picker note in step 4", but the actual pointer at `skills/orch-build-mvp/SKILL.md:41` reads "see the picker note in orchestrate SKILL.md step 4". Fixed the assertion string; re-run is 37/37.

## 5. OWED to the live smoke test — live-only items, never claimed verified

Per `fix24/MANIFEST.md` §5/§6 and `LIVE_SMOKE_TEST.md` §15. Nothing below was verified by this dry-run; each needs the live smoke test in Anish's Cursor.

- **D-6 Stop/SessionStart contradiction:** four hook headers say "Cursor has no Stop/SessionStart hook event" while `hooks.json` registers both. Neither side picked; owed to Cursor docs / the live smoke test.
- **C-5 timeout-300 unit:** the timeout unit is unverified live (seconds vs ms ambiguity in the hook config).
- **C-6 hook cwd/node/event names:** hook working directory, node availability, and event names as Cursor actually invokes them.
- **D-9 `.ecc/settings.json` pickup:** unverified whether Cursor reads it.
- **E-7 gate hook without Git Bash:** gate-hook behavior on a Windows Cursor install without Git Bash.
- **General-subagent fallback pin behavior:** whether a general subagent spawned on `cursor-grok-4.6-high-fast` actually runs on that pin when the named agent does not resolve (the fallback paragraph is present statically — L4-3 — but the pin behavior is live-only).
- **Live `qa.mjs` exit-0 + live film:** the full Remotion render and a filmed demo video (Leg 3 §3.3 environmental FAIL is the sandbox side of this same item).
- **F-14 post-report /demo stale README** (parent call, manifest §5) and **S1 styles.csv header** (80 vs 89 rows; needs a parent verifier-change decision) are open parent adjudications, not smoke-test items, but likewise not resolved by this dry-run.
- **Prior open items carried forward:** Netlify row touch-up after Dec 4, 2026; pip pinning; fix #17 R1/R4 unverified; pitch-deck-video template-fonts self-host follow-up; fresh bundle needed before any push (do NOT push b2444de).

## 6. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression) | 42 | PASS (42/42) |
| 1 — Fixtures (fix #23) | 59 | PASS (59/59) |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | PASS on all measured geometry + coverage complete; **1 MINOR finding** (§2.3: panel-top stagger undeclared); iris-disc bleed MINOR from #38 is **CLEARED** |
| 3 — /demo gates | 59 | PASS on all four gates; **58/59 checks**, 1 FAIL is the known environmental caveat (OWED) |
| 4 — Cursor-readiness (fix #24) | 37 | PASS (37/37), incl. 13 live C-1 hook pipe tests |
| verify24.py (re-run this session) | 105 | **105/105, exit 0** |
| **Total** | **101 fixtures + 59 demo checks + 52 render measurements + 37 leg-4 checks** | **PASS** |

**DRY-RUN #39: PASS**

## 7. Notes for the coordinator / parent (not findings on the fix #24 rules)

1. The one leg-2 MINOR clears with one decision-record line in the render's `docs/design-tokens.md` (clearing text in §2.3). The render predates fix #23, so it is not a fix #24 regression; it is the one conditional item left from the disposition.
2. **`/tmp` is 97% full (20 MB free)** — Chrome crashes on load until `TMPDIR` is redirected (see §2.1). The fill is fix #24 coordinator scratch (`/tmp/ecc-repo-clean` 300 MB, `/tmp/fix24-test2` 56 MB, `/tmp/fix24-test` 56 MB, `/tmp/skill-add` 39 MB, `/tmp/uipro` 30 MB). Nothing was deleted by this dry-run. Clean `/tmp` (or keep `TMPDIR` redirected) before the next Chrome-dependent run in this VM — otherwise the harness, `qa.mjs`, and any smoke-test filming will crash the same way.
3. The template's runtime Google Fonts fetch (§3.3) still stands: a render depending on a live `fonts.gstatic.com` fetch fails in any restricted network even with a working invocation. Whether the template should self-host its fonts (or the skill should record the network requirement) is still the coordinator's call.
4. No credentials were written anywhere. No key was used in the /demo exercise (no voice provider existed). The two HTTP servers started for the exercises (8323 render, 5180 sample app) were both stopped after use.

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix24/dryrun39-report.md` (this report)
- `~/workspace/hackathon-plugin/fix24/dryrun39/dryrun39-fixtures.py` + `dryrun39-fixtures-output.txt` (42/42, verbatim Dry-run #37 list)
- `~/workspace/hackathon-plugin/fix24/dryrun39/dryrun39-f23.py` + `dryrun39-f23-output.txt` (59/59 fix #23 fixtures)
- `~/workspace/hackathon-plugin/fix24/dryrun39/dryrun39-align.py` + `dryrun39-align-output.txt` (leg-2 assertion analysis) + `status-center-probe.mjs` + `status-center-probe-output.txt` (status centers delta 0)
- `~/workspace/hackathon-plugin/fix24/dryrun39/align-run.log` (harness run: 52 measurements, 54 shots, 0 console errors, 0 failed requests) + `prior-align-audit-results.json` (pre-re-run baseline) + `chrome-tmp/` (TMPDIR used for all Chrome runs — see §2.1)
- `~/workspace/hackathon-plugin/fix24/dryrun39/dryrun39-demo.py` + `dryrun39-demo-output.txt` (58/59)
- `~/workspace/hackathon-plugin/fix24/dryrun39/sample-app/` + `demo-sample-video/` (template copy + `shots.json` + live `src/vo-durations.json`; `node_modules/` from the live `npm install`, exit 0, 257 packages) + `npm-cache/`
- `~/workspace/hackathon-plugin/fix24/dryrun39/demo-av-table.md` (per-beat A/V table; stills column UNVERIFIED)
- `~/workspace/hackathon-plugin/fix24/dryrun39/npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `qa-exit.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`
- `~/workspace/hackathon-plugin/fix24/dryrun39/dryrun39-leg4.py` + `dryrun39-leg4-output.txt` (37/37 Cursor-readiness checks incl. C-1 hook pipe tests)
- `~/workspace/hackathon-plugin/fix24/dryrun39/verify24-run.log` (verify24 re-run: 105/105, exit 0)
- `~/workspace/hackathon-plugin/fix24/SPEC.md` (§§0–4), `fix24/PARENT-GUIDANCE.md`, `fix24/MANIFEST.md`
- `~/workspace/hackathon-plugin/fix23/dryrun38-report.md` + fixture/demo scripts (Dry-run #38 lists reused verbatim)
- `build.sh` measured this session: **24,070 lines, md5 `b0b2645a7d647f96296f9e9c45e09ef5`**; counts **166/72/123/87/15**; trigger keys **64**; banned terms **0**
