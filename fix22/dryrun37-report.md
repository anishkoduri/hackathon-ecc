# Dry-run #37 — Fix #22 weave, §§13–17 + §§8–12 regression + /demo

- **Date:** 2026-11-13, early morning CST. Worker: dry-run agent (fix #22), check-only.
- **Scope kept:** read-only against the plugin tree and the built tree. All files written are inside `fix22/dryrun37/`: the fixture runner `dryrun37-fixtures.py` + captured output `dryrun37-output.txt`, the /demo checker `dryrun37-demo.py` + captured output `dryrun37-demo-output.txt`, the /demo fixture app `sample-app/`, the video project copy `demo-sample-video/` (template copy + dry-run `shots.json` + live `src/vo-durations.json`), the A/V table `demo-av-table.md`, and the live-run logs (`npm-install.log`, `playwright-install.log`, `playwright-install2.log`, `playwright-install3.log`, `qa-run.log`). This report is at `fix22/dryrun37-report.md`. No staged source, `build.sh`, built-tree file, or verifier edited; no commit, no bundle, no GitHub touch, no message to Anish.
- **Verdict: DRY-RUN #37: PASS.** All 42 fixture expectations met (see §3) and all 35 /demo contract checks met (see §4). No fixture findings. One live-exercise finding for the coordinator is recorded in §5 (a `qa.mjs` invocation defect in the pitch-deck-video template, found while running /demo live) — it is not a §13–§17 rule defect and does not change the verdict.

## 0. Method — Dry-run #36 followed

1. Re-ran the fix verifier this session (`fix22/verify22.py`).
2. Grepped the built tree for the rule anchors the fixtures judge against; the fixture runner asserts those anchor phrases verbatim (whitespace-normalised, because the built files wrap long lines) against the built tree at run time (read, never retyped from memory) before running any fixture.
3. Applied the check logic stated in the built skill texts to small fixture inputs. Each fixture prints an explicit PASS/FAIL from the script itself: PASS means the observed outcome matched the SPEC's expected outcome.
4. A fixture is a finding ONLY if the observed outcome differs from the SPEC's expected outcome.

Starting state confirmed this session: `build.sh` = **23,758 lines, md5 `306dd648ab9dc4bee0e019a896e26f64`** (matches the task's stated gate numbers); built tree carries all eleven `_F22` anchor tokens (`DEPTH_F22` 8 files, `ORBS_F22` 6, `R3F_F22` 5, `LIQGLASS_F22` 4, `SHADERGRAD_F22` 3, `LIQLOGO_F22` 3, `WEBGL_ONE_F22` 6, `VERCEL_F22` 4, `CASBERRY_F22` 5, `ORIGINKIT_F22` 3, `DAISYUI_F22` 3).

## 1. Rule presence — verify22.py re-run by this worker: PASS (368/368, exit 0)

Re-ran `python3 fix22/verify22.py` from `~/workspace/hackathon-plugin/` this session. Final line: **368/368 checks pass**. The run's tail also records the older verifiers as passing except for their stale post-fix21 `build.sh` fingerprints (fix19 71/76, fix20 164/169, fix21 96/102 on that leg) — expected after a new fix changes `build.sh`, and recorded as PASS lines by verify22 itself, not as failures. This dry-run does not re-litigate those fingerprint checks; verify22 is the governing verifier for fix #22 and it passes 368/368.

Anchor phrases asserted verbatim (whitespace-normalised) by the fixture runner — all present in the built tree (the runner prints `anchors: all rule texts present verbatim in the built tree`):

- §13 depth: D1–D6 sentences in `skills/polish-pass/reference/slop-checklist.md` ("A design package with no depth strategy named FAILS this check", "`flat by choice — <reason>`", "depth applied as decoration with no theme reason FAILS", "3D motion and no reduced-motion fallback FAILS", "3D that hurts text contrast FAILS", "six dimension lines and no Depth line"); "Depth — the seventh dimension" + "all seven dimension lines" in `skills/orchestrate/SKILL.md`; `depthTokens` in `skills/motion-foundations/SKILL.md`.
- §14 orbs: the five fixture phrases in `skills/motion-patterns/SKILL.md` ("a generic spinner" FAILS / "a state-matched orb" PASSES / "a mismatched orb state" FAILS / "an orb used as decoration" FAILS / "an orb that does not respect reduced motion" FAILS); `thinking-orbs@0.3.2` in `skills/ui-ux-pro-max/SKILL.md`; "a Casberry export pasted without review FAILS the security check" in `skills/motion-foundations/SKILL.md`.
- §15: "a surface stacking two WebGL-heavy effects FAILS this check" + "one theme-matched WebGL effect + static fallback PASSES" + "a Casberry particle export" in the slop checklist; "R3F v9 FAILS the pairing check" in motion-foundations; "a build installing legacy `shadergradient` v1 FAILS the version check" + "the URL IS the config" + "a build using the animated logo with no static fallback FAILS the check" in `skills/design-taste-frontend/SKILL.md`; "Unpinned versions (\"latest\") FAIL the pin check" in ui-ux-pro-max.
- §16: "pinned snapshot" + commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1` in `skills/polish-pass/reference/vercel-checklist.md`; **absent** from that file: any `raw.githubusercontent` URL and the words "Fetch the latest guidelines" (also absent from all of `skills/`); "Covered by:" in the checklist; V-AN3 already-covered row in `fix22/vercel-dedupe.md`; D19-reason clearance in `skills/polish-pass/SKILL.md`.
- §17: "DAILY LIMIT: 10 component fetches per key per day" + "proceed from the skills alone, record the gap, never pay for Pro ($79/yr) or Ultimate ($99/yr)" + "A build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check" in motion-patterns; "A build shipping daisyUI's default theme unexamined FAILS" in `skills/design-system/SKILL.md` and design-taste-frontend.
- Regression (§§8–12, dry-run #36 anchors re-asserted): ACCENT_F22 sprawl, H2 accentuation, Mobbin source/never-blocked, directives handoff, layoutId / dropdown 150–250ms / 30ms stagger / React Bits React-only, Vanta reduced-motion, Bang one-world / 30px / style-direction.

## 2. Proxies — recorded explicitly

- **All §13–§17 and regression fixtures are decision-record / design-package / token / handoff / composition inputs judged against the static checks the skills state.** Depth, orb, WebGL, Vercel, and export-review findings are static checks producing candidate evidence, never screen verdicts (fix #13e). The runner models the FLAG/CLEAR outcome of the static check, not a verdict on a rendered screen.
- **§16 fixture 16d** ("finding with no D19 reason is REPORTED") is modelled as the check producing a fixable finding (file:line + rule id + paired `Fix:`) rather than silently dropping it — the runner returns True when the finding is produced and reported.
- **§17 fixture 17b** (OriginKit cap) is modelled as the cap path being followed (proceed from the skills alone, record the gap, never pay) — the "graceful hit" is the correct outcome, not a build failure.
- **/demo is a separate live exercise (§4), not a runner fixture.** Its contract checks are asserted by `dryrun37-demo.py` against the fixture files; the live-vs-not-executed record is in §4.2.

## 3. Per-fixture tables

Judging skill/check column gives the built-tree anchor (file:line where a line is stable). "Observed" is the script's output for that fixture, quoted or paraphrased from `fix22/dryrun37/dryrun37-output.txt`.

### §13 Depth (SPEC §13 verification (a)–(f) + Depth-dimension check)

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 13a | Design package with no depth strategy named | `slop-checklist.md` D1 ("A design package with no depth strategy named FAILS this check") | FAIL | FAIL | PASS |
| 13b | Package naming `flat by choice — <reason>` | `slop-checklist.md` D1 justified use | PASS | PASS | PASS |
| 13c | Deliberate depth: layered hero + parallax + elevation values + theme-matched + 7 D19 lines incl. a `Depth:` line | `slop-checklist.md` D1/D2/D4/D5/D6 + `orchestrate/SKILL.md:122` (seventh dimension) | PASS | PASS | PASS |
| 13d | 3D motion with no reduced-motion fallback | `slop-checklist.md` D4 ("no reduced-motion fallback FAILS") | FAIL | FAIL | PASS |
| 13e | 3D hurting text contrast (no scrim, no 4.5:1) | `slop-checklist.md` D5 ("hurts text contrast FAILS") | FAIL | FAIL | PASS |
| 13f | Depth as decoration with no theme reason | `slop-checklist.md` D2 ("depth applied as decoration with no theme reason FAILS") | FAIL | FAIL | PASS |
| 13g | Decision-record entry with six lines and no Depth line | `slop-checklist.md` D6 ("six dimension lines and no Depth line") | FAIL | FAIL | PASS |

### §14 Thinking Orbs (SPEC §14 verification (a)–(e))

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 14a | Generic spinner for an AI/agent wait | `motion-patterns/SKILL.md` ("a generic spinner" FAILS) | FAIL | FAIL | PASS |
| 14b | State-matched orb (`searching` while retrieving) | `motion-patterns/SKILL.md` ("a state-matched orb" PASSES) | PASS | PASS | PASS |
| 14c | Mismatched orb state (`solving` while the app is just loading a page) | `motion-patterns/SKILL.md` ("a mismatched orb state" FAILS) | FAIL | FAIL | PASS |
| 14d | Orb used as decoration (logo/background, nothing waiting) | `motion-patterns/SKILL.md` ("an orb used as decoration" FAILS) | FAIL | FAIL | PASS |
| 14e | Orb that animates under `prefers-reduced-motion` instead of a frozen one-frame orb | `motion-patterns/SKILL.md` ("an orb that does not respect reduced motion" FAILS) | FAIL | FAIL | PASS |

### §15 Libraries (SPEC §15 verification (a)–(g); task's two extra PASS cases as 15h/15i)

Letter note: the SPEC's (a)–(g) are used as labelled. The task named two additional PASS cases (R3F v9 on React 19; ShaderGradient v2 with URL config) that the SPEC's list does not include as fixtures; they run here as 15h and 15i so both lists are covered.

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 15a | Surface stacking two WebGL-heavy effects (R3F scene + Vanta) | `slop-checklist.md` WEBGL_ONE_F22 ("stacking two WebGL-heavy effects FAILS this check") | FAIL | FAIL | PASS |
| 15b | One theme-matched WebGL effect + static fallback | `slop-checklist.md` WEBGL_ONE_F22 justified use ("one theme-matched WebGL effect + static fallback PASSES") | PASS | PASS | PASS |
| 15c | React 18 build installing R3F v9 | `motion-foundations/SKILL.md:160` ("R3F v9 FAILS the pairing check") | FAIL | FAIL | PASS |
| 15d | Build installing legacy `shadergradient` v1 (1.3.5) | `design-taste-frontend/SKILL.md:134` ("installing legacy `shadergradient` v1 FAILS the version check") | FAIL | FAIL | PASS |
| 15e | Animated logo with no static fallback | `design-taste-frontend/SKILL.md:435` ("animated logo with no static fallback FAILS the check") | FAIL | FAIL | PASS |
| 15f | Library effect applied with no theme reason | `ui-ux-pro-max/SKILL.md` (theme-match precondition) | FAIL | FAIL | PASS |
| 15g | Unpinned ("latest") library version | `ui-ux-pro-max/SKILL.md` ("Unpinned versions (\"latest\") FAIL the pin check") | FAIL | FAIL | PASS |
| 15h | React 19 build installing R3F v9 (paired) | `motion-foundations/SKILL.md` pairing rule (v9 ↔ React 19) | PASS | PASS | PASS |
| 15i | ShaderGradient v2 with URL-as-config (customize URL + preset name) | `design-taste-frontend/SKILL.md:134` ("the URL IS the config") | PASS | PASS | PASS |

### §16 Vercel guidelines (SPEC §16 verification (a)–(e))

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 16a | Build whose polish-pass fetches rules from a live URL | `vercel-checklist.md` (contains no fetch instruction and no unpinned URL; "Fetch the latest guidelines" absent from `skills/`) | FAIL | FAIL | PASS |
| 16b | Build checked against the pinned snapshot | `vercel-checklist.md` ("pinned snapshot" + commit `4ecfb9f`, 2026-10-05, recorded at the top) | PASS | PASS | PASS |
| 16c | Vercel finding on code with a recorded D19 reason + theme-fit | `vercel-checklist.md` + `polish-pass/SKILL.md` ("cleared by a recorded D19 reason + theme-fit") | CLEARED and recorded | CLEARED | PASS |
| 16d | Vercel finding with no D19 reason | `vercel-checklist.md` (file:line + rule id + paired `Fix:` guidance; findings are reported, never silently dropped) | REPORTED as a fixable finding | REPORTED | PASS |
| 16e | Rule claimed as new that duplicates an existing Impeccable rule (V-AN3, `transition: all`) | `vercel-checklist.md` ("Covered by:" pointer) + `fix22/vercel-dedupe.md` (V-AN3 already-covered) | FAILS the dedupe check | FAIL | PASS |

### §17 Libraries (SPEC §17 verification (a)–(f))

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 17a | Casberry export, one-WebGL rule + reviewed line by line | `motion-patterns/SKILL.md` ("The export is the surface's one WebGL-heavy effect" + "reviewed as untrusted code") + `slop-checklist.md` L17-07 justified use | PASS | PASS | PASS |
| 17b | Build needing 12 OriginKit fetches in a day | `motion-patterns/SKILL.md` ("DAILY LIMIT: 10 component fetches per key per day" + "proceed from the skills alone, record the gap, never pay for Pro ($79/yr) or Ultimate ($99/yr)") | Hits the cap gracefully | Graceful cap | PASS |
| 17c | daisyUI component shipped with the default theme unexamined | `design-system/SKILL.md` + `design-taste-frontend/SKILL.md:140` ("A build shipping daisyUI's default theme unexamined FAILS") | FAIL | FAIL | PASS |
| 17d | daisyUI component re-themed to the brand deal | `design-system/SKILL.md` ("re-themed through the brand / theme deal") | PASS | PASS | PASS |
| 17e | Origin UI cited when the build means OriginKit | `motion-patterns/SKILL.md` ("A build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check") | FAIL | FAIL | PASS |
| 17f | Casberry exported code pasted without review | `motion-foundations/SKILL.md` ("a Casberry export pasted without review FAILS the security check") + `slop-checklist.md` ("A build pasting exported code blind FAILS the security check") | FAIL | FAIL | PASS |

### §§8–12 regression (subset of dry-run #36, one–two fixtures per section)

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 8-H1a | Three competing accent hues + accent on non-action elements | `slop-checklist.md` ACCENT_F22 sprawl flag | FAIL sprawl check | FAIL | PASS |
| 8-H2b | Declared first/second/third accent hierarchy + means + D19 each | `orchestrate/SKILL.md` ACCENTUATION_F22 | PASS | PASS | PASS |
| 9a | Decision record cites a Mobbin URL as its design source | `orchestrate/SKILL.md` MOBBIN_RESEARCH_F22 | FAIL | FAIL | PASS |
| 9b | Mobbin categories consulted; direction generated through Taste | `orchestrate/SKILL.md` + `design-taste-frontend/SKILL.md` MOBBIN_PATTERN_F22 | PASS | PASS | PASS |
| 10a | Handoff is prose-only, no exact values | `orchestrate/SKILL.md` DIRECTIVES_F22 ("FAILS the handoff check") | FAIL | FAIL | PASS |
| 10b | Handoff with exact tokens/values/copy + D19 reason | `orchestrate/SKILL.md` DIRECTIVES_F22 | PASS | PASS | PASS |
| 11a | Vanta background with no reduced-motion fallback | `design-taste-frontend/SKILL.md:127` VANTA_F22 ("MUST disable under `prefers-reduced-motion: reduce`") | FAIL | FAIL | PASS |
| 11c | GSAP effect directed by name + exact parameters, pinned `3.15.1`, theme-matched | `ui-ux-pro-max/SKILL.md` GSAP rule | PASS | PASS | PASS |
| 12a | Composition built as slides with fades, static camera, no persistent subject | `pitch-deck-video/SKILL.md` BANG_ANTISLIDE_F22 | FAIL anti-slide | FAIL | PASS |
| 12b | One continuous world + moving camera + persistent subject, text ≥30px, style direction theme-matched | `pitch-deck-video/SKILL.md` BANG_ONEWORLD_F22 / BANG_STYLES_F22 | PASS | PASS | PASS |

## 4. /demo fixture — invocation path exercised live on a sample app

### 4.1 Fixture

- **Sample app:** `fix22/dryrun37/sample-app/` — "Pantry Pal", a static two-page HTML app (`index.html` pantry list + `plan.html` planned week), served locally at `http://localhost:5180` (verified `200` on `/` and `/plan.html` while running; server stopped afterwards).
- **Video project:** `fix22/dryrun37/demo-sample-video/` — a copy of the built `pitch-deck-video/template/` plus a dry-run `shots.json` written for the sample app: 12 beats in the skill's arc (problem, wow, **edge at position 3**, 6 How/feature beats, arch, close), a `features` array of 6 must-haves (each beat id present), one recorded cut with a reason, arch nodes with stack labels (the sample app has no model calls and no framework, so the arch beat states that explicitly — the skill's own fallback), `theme.source` recorded from the app's own tokens (cream `#f6f1e7`, green `#2e5d3a`, orange accent `#e07b39`; not the seed theme), `theme.vignette: 0` recorded, `music.gain.under: 0.14`, and a `bang` block recording opener concept 5 (Journey inside the UI) + style direction "Editorial light", each with a theme reason, plus kinetic-type rows (3) and camera-move rows (2) with exact parameters.
- **Contract checker:** `dryrun37-demo.py` asserts the pipeline files, the build order (`tts → record → frames` in `build.mjs`), local-only filming, F1–F6, voice rules, the $10 cap, and the Bang rules against the fixture files. **Result: 35/35 checks met** (`dryrun37-demo-output.txt`).

### 4.2 Live-vs-not-executed record (exactly what ran, and what did not)

**Executed live in this environment:**

| Step | Command / evidence | Outcome |
|---|---|---|
| Sample app served | `python3 -m http.server 5180` in `sample-app/`; `curl` | `200` on `/` and `/plan.html` |
| Dependencies | `npm install --no-audit --no-fund` in the video project (`npm-install.log`) | **exit 0, 257 packages added** |
| Narration | `node scripts/tts.mjs` in the video project | **exit 0.** Voice preflight: "available providers: none (no ELEVENLABS_API_KEY, no MiniMax credentials, no Piper, no say)". Narration skipped; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key was used or written anywhere. |
| Recording (filming entry point) | `node scripts/record.mjs` | **Not completed — fails at `chromium.launch()`**: "Executable doesn't exist at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`". The filming entry point resolves (script parses, reads `shots.json`, reaches the launch call); the only missing piece is the browser binary. |
| Browser install, attempt 1 | `npx playwright install chromium` (`playwright-install.log`) | **exit 1.** Headless-shell download failed at ~70% with `ENOSPC: no space left on device` — the 512M `/tmp` tmpfs (380M used, 133M free) could not hold the 186.8 MiB download. |
| Browser install, attempt 2 | Same, with `TMPDIR` redirected to the fixture dir on `/home/hatch` (146G free) (`playwright-install2.log`) | **exit 1.** Reached ~90% of `chrome-linux64.zip`, then "Download failed: server closed connection" from `cdn.playwright.dev`. |
| Browser install, attempt 3 | `npx playwright install chromium-headless-shell` (`playwright-install3.log`) | **exit 1.** Reached ~90% of `chrome-headless-shell-linux64.zip` (114.3 MiB), then "Download failed: server closed connection" from `cdn.playwright.dev`. No browser binary exists on disk; no system Chrome/Firefox exists either. |
| QA | `node scripts/qa.mjs` (`qa-run.log`) | **exit 1, before printing any QA checks.** It shells out to `npx remotion@4.0.542 still …`; npx fails with "could not determine executable to run" (npm's `getBinFromManifest` — the `remotion@4.0.542` package carries no bin; the CLI lives in `@remotion/cli`). See §5 note 1. |
| Still render (local binary) | `npx --no-install remotion still src/index.ts Demo … --frame=111` | **exit 1, no still file.** Log shows Google-Fonts fetch failures (`ERR_SSL_PROTOCOL_ERROR` from `fonts.gstatic.com`) and "TypeError Failed to fetch"; the render needs a headless browser, which is unavailable (same blocker as recording). |

**Not executed live (no footage, no render, no video):**

- Filming (`record.mjs` take), `frames.mjs`, the Remotion render (`build.mjs --render` / `npm run all` end-to-end), contact sheets, the 10-second mix listen (no bed exists and no video was rendered, so there is no middle-of-video audio to listen to), and the per-beat A/V stills verification. The A/V table in `demo-av-table.md` is completed as far as the app source allows: every beat's claim and expected frame are stated from the sample app, and every "stills support it?" cell is marked **UNVERIFIED (no stills)**.
- Music fetch: not attempted (`yt-dlp` is not installed; the skill's design is warn-and-continue without a bed, and no bed was needed for this fixture).

**What the invocation path shows:** `/demo` → scaffold (template copy) → `shots.json` (parsed and accepted by `tts.mjs`) → `build.mjs` (single entry point; order `tts → record → frames` verified in the script text) → narration (executed, estimated durations) → recording (entry point reached, blocked only on the browser binary) → frames/render (not reached, blocked on the recording). No pipeline step is missing: every file exists in the template copy, the order is wired, and the failures are environmental (browser download) plus the `qa.mjs` invocation defect in §5 note 1 — not a missing step in the filming path.

### 4.3 Contract items (each asserted by `dryrun37-demo.py`, 35/35)

- **Films the REAL app locally:** `app.url` is `http://localhost:5180`; no deployed URL anywhere in `shots.json`.
- **F1 feature coverage:** 6/6 features have a beat id present in `shots.json`; all 6 feature beats are `kind: app` (filmed footage, not cards); 1 cut recorded with a reason.
- **F2 stack labels:** arch code node carries its stack label ("static HTML — no runtime code"); the arch beat states there are no model calls and no framework, per the skill's fallback ("If the app has no recorded stack, the arch beat says the framework only and notes the gap").
- **F3 Edge at position 3:** `shots[2].id == "edge"`; arc is problem, wow, edge, how, proof, close.
- **F4 theme pull + gorgeousness checks:** `theme.source` recorded; theme is not the seed theme (bg `#f6f1e7` vs seed `#0d0a24`); `theme.vignette: 0` recorded. Gorgeousness itself (cards read as the app's palette; footage shows best-looking states) is **not verified from stills** — no stills exist; the theme-pull half is verified, the footage half is not.
- **F5 blocking A/V table + 10s mix listen:** `qa.mjs` prints the per-beat A/V table and the skill states kinetic type and camera moves go IN the table as rows of their own; the fixture's `bang` block records 3 kinetic-type rows and 2 camera-move rows with exact parameters, and the completed table is in `demo-av-table.md` (stills column unverified — see §4.2). `music.gain.under` is 0.14 (≤ 0.20). The 10-second mix listen was **not done** (no rendered video, no bed).
- **F6 measured runtime under 2:10 / absolute max 2:30:** total from `vo-durations.json` is **84.1s** (LEAD 0.7 + sum(dur + gap) 81.7 + TAIL 1.7) — under 2:10 (130s) and within the 2:30 (150s) absolute max. **Caveat:** the durations are *estimated* (word-count based, ~150 wpm), not measured narration — no voice provider existed in this environment, so `tts.mjs` wrote estimates. The runtime arithmetic is verified; the "measured" part is not, and would change on a real narrated run.
- **Voice rules:** default voice is ElevenLabs Rachel (`21m00Tcm4TlvDq8ikWAM`); no API key is written anywhere in the fixture (provider name only); the fallback chain (ElevenLabs → Piper → `say`, per line at runtime) is present in the skill. The chain was **not exercised with a real voice** — preflight found no provider at all, so the run built music-only/silent with estimated lengths, exactly as the skill prescribes.
- **$10 budget cap:** cap stated in the skill; this fixture spent **$0** (no paid provider used — no key, no Piper, no Runway/Veo/HeyGen). First-paid-use approval rule present in the skill.
- **Local-only filming:** verified above.
- **Bang rules woven in:** anti-slide checks, one-world/camera/persistent-subject architecture, style-direction menu with theme-reason enforcement, opener-concept menu, kinetic typography as §10 directives, and "filmed How/features beats stay filmed" are all present in the skill; the fixture records its opener concept, style direction, kinetic-type rows, and camera-move rows with theme reasons and exact parameters. The opener earns its seconds from the Wow budget inside the 130s cap (84.1s total), never extra runtime.

## 5. Notes for the coordinator / parent (not findings on the §13–§17 rules)

1. **`npm run qa` cannot execute as written — a template defect surfaced by the live /demo exercise.** `template/scripts/qa.mjs:42` shells out to `npx remotion@4.0.542 still …`. In this environment that fails with npm error "could not determine executable to run" (`getBinFromManifest` — the `remotion@4.0.542` package manifest carries no bin; the CLI entry point lives in `@remotion/cli`). The registry fetch itself succeeded (HTTP 200 on `registry.npmjs.org/remotion`), so this is not a network failure — the package named has no executable. Two further skews: the template's `package.json` pins `@remotion/cli` at **4.0.526**, while `qa.mjs` calls `remotion@4.0.542`. Suggested coordinator check: whether `qa.mjs` should call the locally installed CLI (`npx --no-install remotion still …` / the project's own `remotion` bin) or `npx @remotion/cli@<pinned>`, and align the version with the package.json pin. This blocks the QA step (stills + the printed F1/F4/F5/F6 checks) on any machine, browser or not — it is a pitch-deck-video template issue, not a §13–§17 rule defect, and it does not change this dry-run's verdict.
2. **Live filming was blocked by the environment, not the plugin.** Three browser-download attempts failed: once on the 512M `/tmp` tmpfs (ENOSPC at ~70%), twice on `cdn.playwright.dev` closing the connection at ~90% of a 114–187 MiB download (TMPDIR redirected to a disk with 146G free). No system Chrome/Firefox exists on this VM. A machine with a working browser download would film the fixture as written; the fixture itself is ready (`shots.json` accepted by `tts.mjs`, selectors verified against the served app). The A/V stills verification and the 10-second mix listen remain owed on a real render.
3. **Remotion still-rendering also needs the browser, and the template fetches Google Fonts at render time.** The local-binary still attempt failed with exit 1 and no output file; its log shows repeated `ERR_SSL_PROTOCOL_ERROR` fetching `fonts.gstatic.com` woff2 files plus "TypeError Failed to fetch". Even with a browser, this environment's font fetch would need checking — the skill's self-hosted-static-fonts stance (fix #19/#21) is about the build's fonts, but the template's `@remotion/google-fonts` dependency fetches at render time.
4. **Two runner bugs, fixed in the runner, not the plugin (same pattern as dry-run #36 §2).** The first run stopped in `anchors()` on a mis-targeted assertion (the Casberry "pasted without review" phrase lives in motion-foundations, not motion-patterns). The second run stopped on a wrapped anchor ("MUST disable under `prefers-reduced-motion: reduce`" — the `: reduce` suffix was omitted). Both were checker errors; the built texts were correct. Final runner passes 42/42, confirmed on three runs; the demo checker passes 35/35, confirmed on two runs.
5. **Older verifiers' stale fingerprints (same note as dry-run #36).** verify22's regression leg notes fix19/fix20/fix21 pass except for their stale post-fix21 `build.sh` fingerprints (expected: `build.sh` changed under fix #22). verify22 itself is 368/368.

## 6. Verdict summary

| Section | Fixtures | Result |
|---|---|---|
| §13 depth (a)–(f) + Depth-dimension check | 7 | PASS (7/7) |
| §14 Thinking Orbs (a)–(e) | 5 | PASS (5/5) |
| §15 libraries (a)–(g) + 15h/15i | 9 | PASS (9/9) |
| §16 Vercel guidelines (a)–(e) | 5 | PASS (5/5) |
| §17 libraries (a)–(f) | 6 | PASS (6/6) |
| §§8–12 regression (H1/H2, Mobbin, directives, §11, Bang) | 10 | PASS (10/10) |
| /demo fixture (invocation path + contract items) | 35 checks | PASS (35/35) — live film blocked by environment (see §4.2); contract items hold statically |
| **Total** | **42 fixtures + 35 demo checks** | **PASS (42/42, 35/35, each confirmed on re-run)** |

**DRY-RUN #37: PASS**

## Files / evidence used (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix22/SPEC.md` (§§8–17 — fixture definitions and expected outcomes)
- `~/workspace/hackathon-plugin/fix22/depth-patches.md` §6 (§13 fixture check phrases)
- `~/workspace/hackathon-plugin/fix22/orbs-patches.md` §1 (§14 fixture check phrases)
- `~/workspace/hackathon-plugin/fix22/libraries15-patches.md` (§15 integrator checklist §7 + report) and `fix22/libraries17-patches.md` §9 (§17 fixture check phrases)
- `~/workspace/hackathon-plugin/fix22/vercel-patches.md` §8 (§16 fixture check phrases) + `fix22/vercel-dedupe.md` (136 rows)
- `~/workspace/hackathon-plugin/fix22/dryrun36-report.md` + `fix22/dryrun36/dryrun36-fixtures.py` (method + regression fixture format)
- `~/workspace/hackathon-plugin/fix22/verify22.py` (re-run this session: **368/368**, exit 0)
- `~/workspace/hackathon-plugin/fix22/dryrun37/dryrun37-fixtures.py` (written this session; run: **42/42 fixture expectations met**, exit 0, confirmed on three runs)
- `~/workspace/hackathon-plugin/fix22/dryrun37/dryrun37-output.txt` (captured script output)
- `~/workspace/hackathon-plugin/fix22/dryrun37/dryrun37-demo.py` (written this session; run: **35/35 /demo contract checks met**, confirmed on two runs)
- `~/workspace/hackathon-plugin/fix22/dryrun37/dryrun37-demo-output.txt` (captured script output)
- `~/workspace/hackathon-plugin/fix22/dryrun37/sample-app/` (fixture app: `index.html`, `plan.html`)
- `~/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/` (template copy + dry-run `shots.json` + live `src/vo-durations.json`; `node_modules/` from the live `npm install`, exit 0, 257 packages)
- `~/workspace/hackathon-plugin/fix22/dryrun37/demo-av-table.md` (per-beat A/V table; stills column honestly UNVERIFIED)
- `~/workspace/hackathon-plugin/fix22/dryrun37/npm-install.log`, `playwright-install.log`, `playwright-install2.log`, `playwright-install3.log`, `qa-run.log` (live-run evidence)
- Built tree (read-only greps + runner anchor assertions this session): `hackathon-ecc/skills/polish-pass/reference/slop-checklist.md` (DEPTH_F22 D1–D6, WEBGL_ONE_F22, CASBERRY_F22 export-review, ORBS_F22 check); `hackathon-ecc/skills/polish-pass/reference/vercel-checklist.md` (VERCEL_F22, pin `4ecfb9f`); `hackathon-ecc/skills/polish-pass/SKILL.md`; `hackathon-ecc/skills/orchestrate/SKILL.md` (DEPTH_F22 seventh dimension); `hackathon-ecc/skills/design-taste-frontend/SKILL.md` (SHADERGRAD_F22, LIQLOGO_F22, DAISYUI_F22, VANTA_F22); `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md` (ORBS_F22 pin, pin check); `hackathon-ecc/skills/motion-foundations/SKILL.md` (R3F_F22 pairing, depthTokens, CASBERRY_F22); `hackathon-ecc/skills/motion-patterns/SKILL.md` (ORBS_F22 phrases, ORIGINKIT_F22 cap + distinction); `hackathon-ecc/skills/design-system/SKILL.md` (DAISYUI_F22); `hackathon-ecc/skills/pitch-deck-video/SKILL.md` + `template/` (BANG_*_F22, F1–F6, voice, $10 cap, local-only)
- `build.sh` measured this session: **23,758 lines, md5 `306dd648ab9dc4bee0e019a896e26f64`**
