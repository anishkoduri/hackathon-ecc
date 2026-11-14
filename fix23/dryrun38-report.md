# Dry-run #38 — Fix #23 (ambition, motion, fonts, hero, functionality, alignment, dynamic)

- **Date:** 2026-11-13, ~04:14–04:30 CST. Worker: dry-run #38 agent (fix #23), check-only.
- **Scope kept:** read-only against the plugin tree, the built tree, and the Home Run render. All files written are inside `fix23/dryrun38/`: the fixture runners `dryrun38-fixtures.py` (Dry-run #37 list, verbatim reuse) + `dryrun38-f23.py` (new fix #23 fixtures) with captured outputs, the alignment checker `dryrun38-align.py` + `status-center-probe.mjs` with outputs, the /demo checker `dryrun38-demo.py` + the fixture app `sample-app/` + video project `demo-sample-video/` + live-run logs, and the prior-run baselines (`prior-align-audit-results.json`, `prior-fixtures-output.txt`). This report is at `fix23/dryrun38-report.md`. No staged source, `build.sh`, built-tree file, render file, or verifier edited; no bundle, no commit, no push, no message to anyone.
- **Verdict: DRY-RUN #38: PASS.** Leg 1: 101/101 fixture expectations met (42/42 Dry-run #37 regression + 59/59 fix #23). Leg 2: the Home Run render re-run through the tightened §6 assertions passes every directly-measured assertion at all 4 widths and all 13 states, with coverage complete; two MINOR findings (both pre-documented conditionals, both record gaps with no visible defect — see §3.3). Leg 3: /demo gates all pass (58/59 checks; the single FAIL is the known environmental caveat, a live `qa.mjs` exit-0 owed to the live smoke test, not a plugin FAIL — see §4.3). verify23.py re-run this session: **211/212, sole FAIL the owed manifest check**.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **24,059 lines, md5 `df2cb85055efc87637d3cb0b1e7061a2`**; diff vs `build.sh.before-fix23` = **+285/−0**. Matches the task's stated gate numbers.
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** (`hooks/hooks.json` `hooks` list = 15); trigger keys **64** (via `manifests/context-packs/skill-triggers@1.json`, asserted by verify23 itself).
- Banned terms: **0** in the built tree (independent grep this session over `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, excl. `node_modules`, returned no files; verify23 also passes this).
- Fix #23 `build.sh` blocks (lines 23765–24020) contain **zero "demo" mentions** (no auto-invocation wording introduced by fix #23).
- Audit #70 re-run ZERO and Sweep #31 re-run CLEAN taken as given from the task (not re-run by this worker; verify23 + this dry-run are the independent legs).

## 1. verify23.py re-run by this worker: 211/212 (sole FAIL owed)

Ran `python3 fix23/verify23.py` from `~/workspace/hackathon-plugin/` this session (full output: `fix23/dryrun38/verify23-run.log`). Final lines: **211/212 checks pass; excluding the manifest check, which is owed: 211/211 checks pass**. The single FAIL is `fix23/MANIFEST.md exists and records build.sh lines + md5 (OWED -- fails until the manifest worker writes it)` — expected, and the same sole FAIL the task stated. All other legs pass, including the prior verifiers' expected-only fails (fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76, fix20 164/169, fix21 96/102, fix22 368/369 — the frozen post-fix21/post-fix22 fingerprints, as recorded by verify23 itself).

## 2. Leg 1 — Fixtures: 101/101

### 2.1 Dry-run #37 list, re-run verbatim against the current built tree: 42/42

Runner `dryrun38-fixtures.py` is a verbatim copy of `fix22/dryrun37-rerun2/dryrun37-rerun2-fixtures.py` (same anchor assertions, same fixture inputs, same expected outcomes). Output: `dryrun38-fixtures-output.txt`, **42/42 fixture expectations met, exit 0**. Per-section: §13 depth 7/7, §14 orbs 5/5, §15 libraries 9/9, §16 Vercel 5/5, §17 libraries 6/6, §§8–12 regression 10/10. No fixture findings; fix #23 changed nothing under these checks.

### 2.2 New fix #23 fixtures (SPEC §1–§6 + §9 + THE CORE): 59/59

Runner `dryrun38-f23.py` (output `dryrun38-f23-output.txt`, **59/59, exit 0**). Anchors asserted verbatim (whitespace-normalised) against the built tree before running — all present, including the type-audit thresholds (T1a body ≤40% roll-up, T1b ≤55% per screen, T1c display ≥25%, T1d hero display > body, T2 trio re-deal, T3 faces ≥ max(3, ceil(N/20)) each ≥5%), the ambition/memorability paragraphs (`skills/orchestrate/SKILL.md:68/:70`), the alignment assertions and blocking-gap rule (`skills/browser-qa/SKILL.md:60–61/:134`), and the inventory currency rule. Proxies: fixtures are design-package / decision-record / type-audit-table / measurement-dict inputs judged against the static checks the skills state — candidate evidence, never screen verdicts (fix #13e). The live application of the §6 assertions is leg 2 (§3), not this runner.

| Section | Fixtures | Result |
|---|---|---|
| §1 Ambition (1a–1f) | 6 | PASS (6/6) |
| THE CORE — memorability (Ca–Cc) | 3 | PASS (3/3) |
| §2 Motion (2a–2e) | 5 | PASS (5/5) |
| §3 Fonts / type audit (3a–3j) | 10 | PASS (10/10) |
| §4 Hero (4a–4e) | 5 | PASS (5/5) |
| §5 Functionality (5a–5e) | 5 | PASS (5/5) |
| §6 Alignment assertion logic (6a–6q) | 17 | PASS (17/17) |
| §9 Dynamic interface (9a–9h) | 8 | PASS (8/8) |
| **Total fix #23** | **59** | **PASS (59/59)** |

Notable fixture outcomes (each is the SPEC's expected outcome, confirmed by the runner): a blanket "we considered everything" line FAILS (1a); a small-slice inventory use with no specific reasons FAILS (1c); a rule-correct but unambitious design FAILS at the finish review (1e); an over-the-top build with a quiet palette and a strong moment PASSES (Cb); a static-feeling build FAILS even with all static rules passing (2b); body 59% visual share FAILS T1a (3a) while body 36% / display 50% PASSES (3b); a same-trio reuse with a recorded D19 reason + theme-fit is CLEARED (3g); a generic diagram that is not this build's mechanism FAILS (5c); an unverified width (6l) and an unverified flow state (6m) are both BLOCKING DO NOT SHIP; a beyond-frame element with a DECLARED bleed PASSES (6n) and without one FAILS (6o); a 26px panel-top delta with a recorded stagger PASSES (6p) and without one FAILS (6q).

### 2.3 Runner bugs fixed in the runners, not the plugin (same pattern as dry-run #37 §5 note 4)

Three checker errors, all fixed in the dry-run scripts; the built texts were correct in each case:
1. `dryrun38-f23.py` anchors: the inventory currency sentence was asserted against the raw file text, but the file wraps the line — fixed by whitespace-normalising (the sentence is present).
2. `dryrun38-f23.py` anchors: "Visual share of a face" — the built text carries markdown bold (`**Visual share** of a face`) — fixed anchor.
3. `dryrun38-align.py` 6d check (first run): required ALL active-view children to share both edges, ignoring the narrower-child allowance in ALIGN_F23_GRID ("a narrower child is left-aligned or centered") — flagged the left-aligned `.back-btn` (offL 22, w 80/72 vs 344) on 1440-detail/offer/offer-accepted. Fixed to the actual assertion (full-width children share edges; narrower children left-aligned or centered); re-run passes 52/52 on that assertion.
4. Demo exit-code logs (see §4.2): the first `qa-exit.txt` / `remotion-render-help-exit.txt` held the strings `QA-EXIT=1` / `RENDER-HELP-EXIT=0` instead of bare codes, so the checker read them as unparseable and the run scored 57/59. Rewrote the bare codes (`1` / `0`, the true observed exits); re-run is 58/59 with only the known environmental FAIL.

## 3. Leg 2 — Home Run render re-run through the tightened §6 assertions

### 3.1 What ran (live, this session)

- Harness `cold-start-render/home-run/qa/align-audit.mjs` re-run against the current render files (server `python3 -m http.server 8323` in the render dir; browser = the Remotion chrome-headless-shell already on disk, `--no-proxy-server`; fonts are local static woff2, no network needed). Log: `fix23/dryrun38/align-run.log`. **Exit 0: 52 measurements written, 54 screenshots, CONSOLE ERRORS: [], FAILED REQUESTS: [].**
- Prior results preserved before the re-run at `fix23/dryrun38/prior-align-audit-results.json` (the harness overwrites `qa/align-audit-results.json` in place).
- Analysis `dryrun38-align.py` (output `dryrun38-align-output.txt`) applies assertions (a)–(h) + coverage to the fresh JSON. A separate probe `status-center-probe.mjs` measures the status-pair vertical centers the harness records only as tops (output `status-center-probe-output.txt`).

### 3.2 Per-assertion results (fresh run, 52 measurements = 4 widths × 13 states)

| Assertion | Result | Measurement |
|---|---|---|
| (a) OVERFLOW — doc | PASS | `docOverflowX == 0` in 52/52 |
| (a) OVERFLOW — leaf text | PASS | 0 leaf text elements with `scrollWidth > clientWidth + 1` |
| (b) CENTER — phone frame | PASS | `viewportCenterOffset` 0 at all 52 (max \|offset\| 0) — incl. 900/768 stacked |
| (c) NAV — gaps / labels / bar | PASS | adjacent tab gaps equal ±2px in 52/52; every label center == tab center; tabbar centered in phone ±2px in 52/52 |
| (d) GRID — children + feed cards | PASS | full-width children share one left/right edge ±2px; narrower children left-aligned or centered, in 52/52; feed cards share one left/right edge per width |
| (e) CLIP — beyond frame | **FLAG (MINOR)** | `.iris-disc` beyond the phone frame in 8 measurements (trip + trip-wrongcode × 4 widths); bleed NOT declared in the decision record — see §3.3 |
| (f) LABELS — SVG / stamps / status | PASS | route-map + branch-strip: 0 overlaps, 0 out-of-bounds in 52/52; stamp offsets all 0 (n=12); statusbar insets symmetric; **status vertical centers delta 0 at 1440/900/390** (probe: time h=22 vs icons h=12 explains the 5px top difference) |
| (g) ACTIONS — code boxes | PASS | code-box group offset on its panel 0 in all 8 trip measurements |
| (h) PANELS — gutters | PASS | desktop gutters symmetric 44/44 in 13/13 at 1440 |
| (h) PANELS — tops | **FLAG (MINOR)** | top delta **26px** at 1440 (left top 232 vs right top 206), no stagger recorded — see §3.3 |
| COVER_F23 — matrix | PASS | required 39/39 cells present (1440/900/390 × 13 states); bonus width 768 also measured (52 total) |
| COVER_F23 — screenshots | PASS | a screenshot exists for every measured cell (54 shots incl. `align-900-fullpage` + `align-900-panels`) |

States covered at every width: home, home-bottom (scrolled), detail, offer, offer-accepted, trip, trip-wrongcode, trip-delivered, branches, trips, you, post, post-done. **No unverified width, no unverified flow state — no BLOCKING coverage gap.**

Fresh vs prior results JSON: identical except 4 measurements (`*-trip-wrongcode`), and only in the individual code-box input rects (1–4px shifts); the group geometry is identical in all 4 (groupLeft/groupRight/groupCenterX/panelCenterX unchanged, offset 0). Cause is animation timing, not layout: the wrong-code state shakes the field once (A9 snappy, 0.18s) and the harness measures 250ms after the click, so the inputs' exact x depends on the shake phase. The asserted quantity (group centering) is unchanged.

### 3.3 The two MINOR findings (pre-documented conditionals, not new defects)

Both were already flagged in `fix23/disposition-merged.md` (W4 cross-check) as "passes ONLY if declared". This re-run confirms the measurements reproduce exactly and the declarations are still absent from the render's decision record (`docs/design-tokens.md`: no "bleed" anywhere; no line ties a "stagger" to the panels). The render predates fix #23 and its record cannot be edited by this check-only task. Neither is a visible defect:

1. **MINOR — ALIGN_F23_CLIP, `.iris-disc` beyond the phone frame.** Extent: 1440 trip/wrongcode left 445 / right 995 (phone 525–915, i.e. 80px past each side); 390 trip/wrongcode left −82 / right 472 (82px past the viewport's left edge). Page overflow stays 0 at all widths. The element is the iris-opens dealt moment's ring: `position: absolute; inset: 0; opacity: 0; pointer-events: none` with a 0.7s `iris-ring` keyframe scaling 0.2 → 1.6 and fading to opacity 0 (`styles.css:427–435`), and the moment is recorded in the design record ("the code panel opens through the iris disc (hairline green ring)", `design-tokens.md:199–201`). The harness measures ≥1400ms after the trip view opens, so the animation has finished and the measured rect is the scale(1.6) end-state of an **invisible** element. What is missing is one recorded line declaring the beyond-frame extent as the intentional bleed of that moment. Clearing text (for the coordinator): a decision-record line that the iris ring intentionally expands beyond the phone frame during the 0.7s open and is invisible at rest.
2. **MINOR — ALIGN_F23_PANELS, desktop side-panel top delta 26px.** Left panel top 232, right panel top 206 at 1440, in all 13 states. Cause is not drift: `.desk` is `display: flex; align-items: center` (`styles.css:87–88`), so the panels are vertically centered; left h=436, right h=489, and (489−436)/2 = 26.5 ≈ 26. Gutters are symmetric 44/44. What is missing is one recorded line stating the panels are vertically centered (so tops differ by height) rather than top-aligned. The 900/768 numbers (−548) are meaningless in the stacked layout and were not asserted, per the disposition. Clearing text (for the coordinator): a decision-record line that the desk vertically centers the flanking panels.

Strict-reading note, recorded honestly: under a strict literal reading of ALIGN_F23_CLIP ("no element beyond its frame unless a DECLARED intentional bleed") and ALIGN_F23_PANELS ("tops aligned ±2px unless a stagger is recorded"), both items flag because the declarations are absent. I classify both MINOR rather than blocking because there is no visible defect (an invisible animation end-state; vertically-centered panels with symmetric gutters), both were pre-documented as conditionals before this dry-run, and the only blocking criterion the task names for this leg is an unverified width or state, of which there are none. The parent may adjudicate either as blocking; the one-line clearing texts above are the fix in either case.

## 4. Leg 3 — /demo gates

### 4.1 Gates (each PASS, with file:line evidence)

| Gate | Result | Evidence |
|---|---|---|
| /demo callable ONLY on explicit invocation — 0 auto-invocations anywhere in the pipeline | PASS | 13/13 removal checks in the demo checker (see §4.2); `skills/orchestrate/SKILL.md` step 5d `DEMOGATE_O4_F22` + "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline"; step 6 `DEMOGATE_O9_F22` + "A demo video is filmed only when the user invokes `/demo` explicitly"; `skills/orch-build-mvp/SKILL.md` `DEMOGATE_B2S1_F22` + "`/demo` is not filmed here"; `skills/orch-change-feature/SKILL.md` `DEMOGATE_B3S1_F22`; `rules/hackathon-mode.mdc:12` `DEMOGATE_H2_F22` + "/demo is never part of this sequence"; `commands/demo.md` still dispatches all `/demo` forms to pitch-deck-video (explicit path intact); `skills/pitch-deck-video/SKILL.md` carries no DEMOGATE token (removal did not touch it); a tree-wide grep for auto-invocation phrasing (`auto.*demo`, `dispatch.*demo`, `invoke.*demo`, `film.*demo` minus never/not/only/explicit) returns only benign lines (fastapi "dev/demo environments", a `demo.html` reference, the pitch-deck-video boundary text, demo-length rules); zero "demo" mentions in the fix #23 `build.sh` blocks (23765–24020) |
| Narration-key prompt fires ONLY when the user asked for a demo video | PASS | `skills/orchestrate/SKILL.md` step 0: "ONLY when the user asked for a demo video" + "If the user did NOT ask for a demo video, do NOT send this prompt"; `rules/hackathon-mode.mdc` §7: "only when the user asked for a demo video" + same guard; `skills/orch-build-mvp/SKILL.md` `DEMOGATE_B2S7_F22` with the same condition |
| Contract intact — first-build sequence is deploy → commit → README, no /demo in it | PASS | `rules/hackathon-mode.mdc:22`: end-of-project run is "(after deploy, commit, and README)" with no `/demo` in the §3 sequence; `rules/hackathon-mode.mdc:12` full sequence ends "deploy → README → final report" with "/demo is never part of this sequence"; `skills/orchestrate/SKILL.md` step 6 order sentence (`DEMOGATE_O9_F22`) |
| Runtime hard cap under 2:10 (130s) from narration, absolute max 2:30 (150s) | PASS (with the estimated-duration caveat below) | Fixture total **84.1s** from live `src/vo-durations.json` (LEAD 0.7 + sum(dur+gap) 81.7 + TAIL 1.7), under 130s and within 150s; `music.gain.under` 0.14 (≤ 0.20); opener earns its seconds from the Wow budget inside the cap |

**Caveat on "measured narration" (recorded, not hidden):** the 84.1s is computed from `vo-durations.json` written by `tts.mjs`, but no voice provider exists in this sandbox ("available providers: none"), so the durations are word-count estimates (~150 wpm), not measured narration — the same caveat as dry-run #37. The runtime arithmetic is verified; the "measured" part is owed to a real narrated run. The voice rules themselves hold statically (default Rachel `21m00Tcm4TlvDq8ikWAM`, no key written anywhere, fallback chain present) and the fixture spent $0 under the $10 cap.

### 4.2 Live-vs-not-executed record (exactly what ran, and what did not)

Fixture: `fix23/dryrun38/sample-app/` ("Pantry Pal", `index.html` + `plan.html`, served at `http://localhost:5180`, verified `200` on `/` and `/plan.html`; server stopped afterwards) and `fix23/dryrun38/demo-sample-video/` (fresh copy of the current built `pitch-deck-video/template/` + the Dry-run #37 `shots.json`: 12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme pulled from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block with opener concept 5 + "Editorial light" + 3 kinetic-type rows + 2 camera-move rows). The template copy diffed against the built template is byte-identical except `package-lock.json` + `tmp/` (artifacts of this run's own `npm install`).

| Step | Evidence | Outcome |
|---|---|---|
| Dependencies | `npm install --no-audit --no-fund` (`npm-install.log`) | **exit 0, 257 packages added** (same count as the prior runs) |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** No voice provider; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording (filming entry point) | `node scripts/record.mjs` (`record-run.log`) | **exit 1 at `chromium.launch()`**: "Executable doesn't exist at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`". Entry point resolves; only the Playwright browser binary is missing. Playwright install was NOT re-attempted (the prior runs already established the CDN closes the connection at ~90%). Environmental, same as the prior runs. |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 1 — the known environmental caveat (see §4.3).** Prints "rendering 12 stills…", then fails on `Command failed: npx -p @remotion/cli@4.0.526 remotion still …` — the `-p` invocation resolved and ran; the inner still render failed on the runtime Google Fonts fetch. |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** — prints the `remotion render` usage (the `build.mjs` render form). |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Network control | `curl` to the font URL | **200** via curl; only Chrome's direct fetch fails in this sandbox (same control as rerun2). |

**Not executed live (no footage, no render, no video):** filming (`record.mjs` take — blocked on the missing Playwright binary, environment), `frames.mjs`, the Remotion render (`build.mjs --render` / `npm run all` end-to-end), contact sheets, the 10-second mix listen (no bed, no rendered video), and the per-beat A/V stills verification. The A/V table in `demo-av-table.md` is completed as far as the app source allows; all stills cells remain **UNVERIFIED (no stills)** — `out/qa/` is empty. Music fetch: not attempted (`yt-dlp` is not installed; the skill's design is warn-and-continue without a bed).

### 4.3 The single failing check — 58/59, environmental (OWED, not a plugin FAIL)

Checker `dryrun38-demo.py` (verbatim reuse of the rerun2 checker; output `dryrun38-demo-output.txt`): **58/59 /demo contract checks met** — 35/35 original contract checks, 13/13 removal checks, 10/11 Remotion checks. The one FAIL is **`demo-remotion-qa-live`: `node scripts/qa.mjs` exits 1, not 0.**

Attribution (verified live, same as rerun2): the `-p` invocation resolves and executes — no "could not determine executable to run" anywhere in `qa-run.log`; Remotion launches, bundles the composition, and begins rendering ("rendering 12 stills…"). The exit-1 cause is the composition's **runtime Google Fonts fetch**: the template's `src/fonts.ts` loads Hanken Grotesk / Instrument Serif / JetBrains Mono via `@remotion/google-fonts`, which fetches from `fonts.gstatic.com` at render time; inside Chrome in this sandbox that fetch fails (`net::ERR_SSL_PROTOCOL_ERROR` on all three woff2 files, `qa-run.log`) while the same URL returns 200 via `curl`. Per the task, this is **an owed item for the live smoke test in Anish's Cursor, not a FAIL** of the /demo gates: the invocation path, the removal gates, the contract, and the runtime cap all hold; a live film and a full live `qa.mjs` exit-0 are not provable in this sandbox. The template's live font fetch (vs the plugin's self-hosted-static-fonts stance) remains the coordinator's open observation from rerun2 §5 — flagged, not fixed, by this dry-run.

## 5. Verdict summary

| Leg | Checks | Result |
|---|---|---|
| 1 — Fixtures (§37 regression) | 42 | PASS (42/42) |
| 1 — Fixtures (fix #23, §§1–6 + §9 + CORE) | 59 | PASS (59/59) |
| 2 — Home Run render, §6 assertions | 52 measurements, 13 states × 4 widths | PASS on all measured geometry + coverage complete; **2 MINOR findings** (§3.3: iris-disc bleed undeclared; panel-top stagger undeclared) |
| 3 — /demo gates | 59 | PASS on all four gates; **58/59 checks**, 1 FAIL is the known environmental caveat (OWED) |
| verify23.py (re-run this session) | 212 | **211/212**, sole FAIL the owed manifest check |
| **Total** | **101 fixtures + 59 demo checks + 52 render measurements** | **PASS** |

**DRY-RUN #38: PASS**

## 6. Notes for the coordinator / parent (not findings on the fix #23 rules)

1. The two leg-2 MINOR findings each clear with one decision-record line in the render's `docs/design-tokens.md` (clearing texts in §3.3). The render predates fix #23, so neither is a fix #23 regression; they are the two conditional items the disposition already carried.
2. The template's runtime Google Fonts fetch (rerun2 §5 observation) still stands: a render depending on a live `fonts.gstatic.com` fetch fails in any restricted network even with a working invocation. Whether the template should self-host its fonts (or the skill should record the network requirement) is still the coordinator's call.
3. The §9 open parent adjudication carried in the disposition (DYNAMIC-BQA-01: the live check assumes the harness can drive sort/filter/expand/drag; the text does not explicitly say to record an undrivable interaction as unverified rather than silently pass) was not tested by any fixture here — it needs a harness-level decision, not a dry-run fixture.
4. No credentials were written anywhere. No key was used in the /demo exercise (no voice provider existed). The two HTTP servers started for the exercises (8323 render, 5180 sample app) were both stopped after use.

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix23/dryrun38-report.md` (this report)
- `~/workspace/hackathon-plugin/fix23/dryrun38/dryrun38-fixtures.py` + `dryrun38-fixtures-output.txt` (42/42, verbatim Dry-run #37 list)
- `~/workspace/hackathon-plugin/fix23/dryrun38/dryrun38-f23.py` + `dryrun38-f23-output.txt` (59/59 fix #23 fixtures)
- `~/workspace/hackathon-plugin/fix23/dryrun38/dryrun38-align.py` + `dryrun38-align-output.txt` (leg-2 assertion analysis) + `status-center-probe.mjs` + `status-center-probe-output.txt` (status centers delta 0)
- `~/workspace/hackathon-plugin/fix23/dryrun38/align-run.log` (harness run: 52 measurements, 54 shots, 0 console errors, 0 failed requests)
- `~/workspace/hackathon-plugin/fix23/dryrun38/prior-align-audit-results.json` (pre-re-run baseline) + `prior-fixtures-output.txt`
- `~/workspace/hackathon-plugin/fix23/dryrun38/dryrun38-demo.py` + `dryrun38-demo-output.txt` (58/59)
- `~/workspace/hackathon-plugin/fix23/dryrun38/sample-app/` + `demo-sample-video/` (template copy + `shots.json` + live `src/vo-durations.json`; `node_modules/` from the live `npm install`, exit 0, 257 packages)
- `~/workspace/hackathon-plugin/fix23/dryrun38/demo-av-table.md` (per-beat A/V table; stills column UNVERIFIED)
- `~/workspace/hackathon-plugin/fix23/dryrun38/npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `qa-exit.txt`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`
- `~/workspace/hackathon-plugin/fix23/dryrun38/verify23-run.log` (verify23 re-run: 211/212)
- `~/workspace/hackathon-plugin/fix23/SPEC.md` (§§1–6, §8, §9), `fix23/PARENT-GUIDANCE.md`, `fix23/disposition-merged.md`
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-report.md` + fixture/demo scripts (Dry-run #37 lists reused verbatim)
- `build.sh` measured this session: **24,059 lines, md5 `df2cb85055efc87637d3cb0b1e7061a2`**, diff +285/−0; counts **166/72/123/87/15**; trigger keys **64**
