# Dry-run #37 RE-RE-RUN — Fix #22 weave, new build (post Remotion `-p` fix + further /demo-removal completion)

- **Date:** 2026-11-13, ~02:00–02:20 UTC (evening CST Nov 12 / early Nov 13). Worker: dry-run #37 re-re-run agent, check-only.
- **Scope kept:** read-only against the plugin tree and the built tree. All files written are inside `fix22/dryrun37-rerun2/`: the fixture runner `dryrun37-rerun2-fixtures.py` + captured output `dryrun37-rerun2-output.txt`, the /demo checker `dryrun37-rerun2-demo.py` + captured output `dryrun37-rerun2-demo-output.txt`, the /demo fixture app `sample-app/` (copy of the prior re-run's), the video project copy `demo-sample-video/` (fresh copy of the NEW built `pitch-deck-video/template/` + the prior re-run's `shots.json` + live `src/vo-durations.json`), the A/V table `demo-av-table.md` (copied from the prior re-run; stills column still UNVERIFIED — no stills exist), and the live-run logs (`npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `qa-exit.txt`, `remotion-still-probe.log`, `remotion-still-proxy-probe.log`, `chrome-direct-probe.log`, `remotion-p-help.log`, `remotion-render-help.log` + `remotion-render-help-exit.txt`, `remotion-local-help.log`, `tmp/proxy-chrome.sh`). This report is at `fix22/dryrun37-rerun2/dryrun37-rerun2-report.md`. No staged source, `build.sh`, built-tree file, or verifier edited; no commit, no bundle, no GitHub touch, no message to anyone.
- **Verdict: DRY-RUN #37 RE-RE-RUN: FAIL — 1 of 59 /demo checks fails.** All 42 §13–§17 + §§8–12 fixtures pass (42/42), all 35 original /demo contract checks pass (35/35), and the /demo-removal verification passes 13/13 (the prior 8 + the 5 new sites). **The prior re-run's single finding is RESOLVED:** the Remotion invocation form is corrected and executes live — `npx -p @remotion/cli@4.0.526 remotion …` resolves at both call sites, the `still` command runs, Remotion auto-downloads its headless-shell browser, bundles the composition, and gets as far as rendering before failing. But `qa.mjs` still does **not** exit 0 (exit 1): the failure moved downstream to the composition's **runtime Google Fonts fetch**, which fails inside Chrome in this sandbox (SSL handshake failure; a direct Chrome probe hung >2 min and was killed; `curl` to the same URL returns 200). The literal key check — "`qa.mjs` exits 0 with the `-p` form" — is therefore **not met in this environment**, even though the invocation defect that caused the prior FAIL is fixed. See §5 for the precise attribution and what is owed on a normal network.

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **23,774 lines, md5 `4799a819791b9c3ec4c19136ad698397`** — matches the task's stated gate numbers.
- `fix22/verify22.py` re-run this session: **368/368 checks pass**, exit 0 (same stale-fingerprint note as the prior runs: fix19 71/76, fix20 164/169, fix21 96/102 on the regression leg — expected after `build.sh` changed, recorded as PASS lines by verify22 itself).
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** (`hooks/hooks.json` `hooks` list = 15).
- **What changed since the prior re-run, verified from the files, not assumed:**
  - `template/scripts/build.mjs:335` now calls `run('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'render', …])` and `template/scripts/qa.mjs:42` now calls `execFileSync('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'still', …])`. The fresh template copy diffed against the built template is byte-identical (diff exit 0, excluding the added fixture `shots.json`).
  - **0 bare `npx @remotion/cli@4.0.526` invocations** anywhere in the built tree (walked, excluding `node_modules`) and **0 `remotion@4.0.542`** anywhere in the built tree.
  - /demo-removal completion: `hackathon-mode.mdc:22` now reads "(after deploy, commit, and README)" with no `/demo` in the §3 end-of-project sentence; the §7 narration-key paragraph (line 59) is conditional ("only when the user asked for a demo video" / "If the user did NOT ask for a demo video, do NOT send this prompt"); `orch-build-mvp` line 32 carries the conditioned narration-key paragraph with `DEMOGATE_B2S7_F22`; step 8 (line 83) says "Do NOT film via `/demo` here" and "If the user asked for one, film the LOCAL app from the project dir after deploy". `orchestrate` step 0 (line 58) is likewise conditional ("ONLY when the user asked for a demo video").

## 1. /demo auto-invocation removal — verified at all 6 sites + follow-ups (13/13 checks)

All anchors asserted verbatim (whitespace-normalised) by `dryrun37-rerun2-demo.py` against the NEW built tree:

| Site | Anchor found in the new build | Result |
|---|---|---|
| orchestrate step 5d | `DEMOGATE_O4_F22` + "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline" — runs ONLY on explicit user invocation (or an explicit demo-video request) | PASS |
| orchestrate step 6 (follow-up) | `DEMOGATE_O9_F22` + "A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order" | PASS |
| orchestrate step 0 (new) | Narration-key prompt "ONLY when the user asked for a demo video"; "If the user did NOT ask for a demo video, do NOT send this prompt" | PASS |
| orch-build-mvp step 8 | `DEMOGATE_B2S1_F22` + "`/demo` is not filmed here" — ONLY when the user invokes it explicitly; films the LOCAL app, never the deployed URL (`DEMOGATE_B2S2_F22`) | PASS |
| orch-build-mvp step 9 (follow-up) | `DEMOGATE_B2S3_F22`–`B2S6_F22` present; README before final report, report notes "no demo video was filmed" when none was requested | PASS |
| orch-build-mvp narration-key (new, B2S7) | `DEMOGATE_B2S7_F22` + "if the user asked for a demo video" + "If the user did NOT ask for a demo video, do NOT send this prompt" | PASS |
| orch-build-mvp step 8 handoff (new) | "Do NOT film via `/demo` here" + "If the user asked for one, film the LOCAL app from the project dir after deploy" | PASS |
| orch-change-feature step 5 | `DEMOGATE_B3S1_F22` + "If the user asks for a re-film, re-film via `/demo --rebuild`" + "no re-film happens here"; done-condition is re-filmed video OR flagged-stale (`DEMOGATE_B3S5_F22`); narration continuity + re-upload rules (`B3S2`–`B3S4`, `B3S6`) | PASS |
| hackathon-mode §7 mandate | `DEMOGATE_H1_F22`: "The first build does NOT film `/demo` automatically"; `DEMOGATE_H2_F22`: "/demo is never part of this sequence" (line 12 sequence); line 61 §7 timing text (narration-key prompt scheduled here, sent by orchestrate) intact | PASS |
| hackathon-mode :22 (new) | Line 22: end-of-project run is "(after deploy, commit, and README)" — no `/demo` in the §3 sequence | PASS |
| hackathon-mode §7 conditional (new) | "only when the user asked for a demo video" + "If the user did NOT ask for a demo video, do NOT send this prompt" | PASS |
| commands/demo.md dispatch note | Still dispatches to pitch-deck-video (`/demo`, `/demo <path>`, `/demo --rebuild`, `--script`, `--render`, `--montage`/`--explainer` opt-in); key-via-dispatch rule intact | PASS |
| dispatch-prompt.md Environment field | Environment field carries `ELEVENLABS_API_KEY=<redacted>` "on a /demo dispatch when a narration key was received mid-build"; omit when not needed; never in a file/log/ledger | PASS |

**Explicit invocation still reaches the filming pipeline — proved, not assumed:** `commands/demo.md` still loads the pitch-deck-video skill with all `/demo` forms; the pitch-deck-video skill itself carries **no** `DEMOGATE` token and no "never automatic" / "NEVER dispatched" language (checked in the runner); the template copy's pipeline files are all present and `build.mjs` still runs `tts → record → frames` in that order (demo-path checks, §4); `tts.mjs` executed live and accepted the fixture `shots.json` (§4.2). The removal removed only the automatic dispatches, not the on-demand path.

## 2. Fixtures — 42/42 (re-run against the NEW built tree)

Same fixture structure as the prior runs, re-derived from the SPEC (expected PASS/FAIL per fixture is the SPEC's expected outcome; "FLAG/FAIL" strings are expected-outcome labels, not failures). All rule anchors re-asserted verbatim against the new built tree before running — all present. Condensed per-section results (full per-fixture tables are in the first run's report; the inputs, judging checks, and observed outcomes are identical here — see `dryrun37-rerun2-output.txt`):

| Section | Fixtures | Result |
|---|---|---|
| §13 depth (a)–(f) + Depth-dimension check | 7 (13a–13g) | PASS (7/7) |
| §14 Thinking Orbs (a)–(e) | 5 (14a–14e) | PASS (5/5) |
| §15 libraries (a)–(g) + 15h/15i | 9 (15a–15i) | PASS (9/9) |
| §16 Vercel guidelines (a)–(e) | 5 (16a–16e) | PASS (5/5) |
| §17 libraries (a)–(f) | 6 (17a–17f) | PASS (6/6) |
| §§8–12 regression (H1/H2, Mobbin, directives, §11, Bang) | 10 (8-H1a, 8-H2b, 9a, 9b, 10a, 10b, 11a, 11c, 12a, 12b) | PASS (10/10) |
| **Total** | **42** | **PASS (42/42, exit 0)** |

Proxies (same as the prior runs, recorded explicitly): fixtures are decision-record / design-package / token / handoff / composition inputs judged against the static checks the skills state — static checks producing candidate evidence, never screen verdicts (fix #13e). §16d models "reported as a fixable finding" as the check producing the finding; §17b models the OriginKit cap path as the graceful outcome. No fixture findings.

## 3. /demo — 58/59 checks (35/35 original + 13/13 removal + 10/11 Remotion)

### 3.1 Fixture (same as the prior runs, fresh copies)

- **Sample app:** `fix22/dryrun37-rerun2/sample-app/` — "Pantry Pal" (`index.html` + `plan.html`), served locally at `http://localhost:5180` (verified `200` on `/` and `/plan.html` while running; server stopped afterwards).
- **Video project:** `fix22/dryrun37-rerun2/demo-sample-video/` — fresh copy of the NEW built `pitch-deck-video/template/` + the prior re-run's `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme pulled from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block with opener concept 5 + "Editorial light" + 3 kinetic-type rows + 2 camera-move rows).
- **Checker:** `dryrun37-rerun2-demo.py` — the prior re-run's checks with the Remotion assertions updated to the `-p` form plus 5 new removal checks. **Result: 58/59** (`dryrun37-rerun2-demo-output.txt`).

### 3.2 Original 35 checks — all pass

Invocation path resolves end-to-end (all 9 pipeline files present; `build.mjs` order `tts → record → frames`; `package.json` `all` = `node scripts/build.mjs`); local-only filming (`http://localhost:5180`); F1 6/6 coverage, all filmed; F2 stack labels + no-model-calls fallback; F3 edge at `shots[2]`; F4 theme source recorded, not the seed theme, vignette recorded; F5 A/V table in skill + kinetic/camera rows recorded, mix gain 0.14 (≤ 0.20); F6 total **84.1s** from `vo-durations.json` (LEAD 0.7 + sum(dur+gap) 81.7 + TAIL 1.7) — under 2:10 (130s) and within the 2:30 absolute max (same estimated-duration caveat as the prior runs: no voice provider existed, so durations are word-count estimates, not measured narration); voice default Rachel (`21m00Tcm4TlvDq8ikWAM`), no key written anywhere, fallback chain present; $10 cap present, $0 spent; Bang rules present and recorded. Gorgeousness-from-stills and the 10-second mix listen remain unverified (no stills, no render — see §4.2).

### 3.3 Removal 13/13 — all pass (see §1)

### 3.4 Remotion fix — 10/11 pass

- Text-level 6/6: 0 `remotion@4.0.542` anywhere in the built tree (walked, excluding `node_modules`); 0 bare `npx @remotion/cli@4.0.526` anywhere in the built tree; `build.mjs` calls `npx -p @remotion/cli@4.0.526 remotion render`; `qa.mjs` calls `npx -p @remotion/cli@4.0.526 remotion still`; template `package.json` pins `@remotion/cli` at `4.0.526`; installed `node_modules/@remotion/cli/package.json` carries the three-bin entry (`remotion`, `remotionb`, `remotiond`).
- Live-resolution 4/5: `npx -p @remotion/cli@4.0.526 remotion --help` → exit 0, prints `@remotion/cli 4.0.526` (PASS); `npx -p @remotion/cli@4.0.526 remotion render --help` → exit 0 (PASS — the exact `build.mjs` render form); `npx --no-install remotion --help` → exit 0 (PASS); `node scripts/qa.mjs` → the `-p` invocation **resolves past npx** — no "could not determine executable to run" anywhere in `qa-run.log` (PASS, `demo-remotion-qa-invocation`); **`node scripts/qa.mjs` exits 1, not 0 (FAIL — `demo-remotion-qa-live`)**, on the downstream font fetch (§5).

## 4. Live-vs-not-executed record (exactly what ran, and what did not)

**Executed live in this environment:**

| Step | Command / evidence | Outcome |
|---|---|---|
| Sample app served | `python3 -m http.server 5180` in `sample-app/`; `curl` | `200` on `/` and `/plan.html`; server stopped after the exercise |
| Dependencies | `npm install --no-audit --no-fund` in the video project, `TMPDIR` redirected to the disk-backed rerun2 `tmp/` (`npm-install.log`) | **exit 0, 257 packages added** (same count as the prior runs) |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** "available providers: none (no ELEVENLABS_API_KEY, no MiniMax credentials, no Piper, no say)". Narration skipped; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording (filming entry point) | `node scripts/record.mjs` (`record-run.log`) | **exit 1 at `chromium.launch()`**: "Executable doesn't exist at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`". Entry point resolves (script parses, reads `shots.json`, reaches the launch call); only the Playwright browser binary is missing. (Playwright install was NOT re-attempted this run — the prior runs already established the CDN closes the connection at ~90%.) |
| QA (the key check) | `node scripts/qa.mjs` (`qa-run.log`, exit in `qa-exit.txt`) | **exit 1.** Prints "rendering 12 stills…", then fails on `Command failed: npx -p @remotion/cli@4.0.526 remotion still src/index.ts Demo …/out/qa/00111_problem.png --frame=111 --log=error` — the `-p` invocation resolved and ran; the inner still render failed with `TypeError Failed to fetch` while loading Google Fonts (see §5). No "could not determine executable to run". |
| Still probe (direct) | `npx -p @remotion/cli@4.0.526 remotion still src/index.ts Demo /tmp/probe-still.png --frame=111 --log=verbose` (`remotion-still-probe.log`) | **exit 1**, same cause, with the full trace: "Ensuring browser executable / Ensured browser is available" (Remotion auto-downloaded `chrome-headless-shell` into `node_modules/.remotion/`), "Opening browser: …/chrome-headless-shell", bundling 100%, then `[chrome] handshake failed; … net_error -107` and `Browser failed to load https://fonts.gstatic.com/… (Fetch): net::ERR_SSL_PROTOCOL_ERROR`, then `TypeError Failed to fetch` at `@remotion/google-fonts` `HankenGrotesk.mjs`. |
| Still probe (proxy wrapper) | Same still via `--browser-executable ../tmp/proxy-chrome.sh`, a diagnostic-only wrapper that launches the same shell with the sandbox egress proxy from the environment (`remotion-still-proxy-probe.log`) | **exit 1**, same cause: log still shows the font URLs failing with `net::ERR_SSL_PROTOCOL_ERROR`. The wrapper was used ("Opening browser: …/proxy-chrome.sh") but did not unblock Chrome's fetch. |
| Direct Chrome probe | The wrapper shell headless `--dump-dom` of a font URL (`chrome-direct-probe.log`) | **Hung >2 minutes, killed** (SIGTERM; log holds only zygote socket-closed lines from the kill). Chrome cannot complete the fetch in this sandbox at all, even via the proxy. |
| Remotion `-p` `--help` | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Remotion render form | `npx -p @remotion/cli@4.0.526 remotion render --help` (`remotion-render-help.log`, exit in `remotion-render-help-exit.txt`) | **exit 0** — prints the `remotion render` usage. |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526`. |
| Network control | `curl` to the same font URL and to `registry.npmjs.org` | **200 both.** Node/npm egress works; only Chrome's direct fetch fails/hangs in this sandbox. |

**Not executed live (no footage, no render, no video):**

- Filming (`record.mjs` take — blocked on the missing Playwright browser binary, environment), `frames.mjs`, the Remotion render (`build.mjs --render` / `npm run all` end-to-end), contact sheets, the 10-second mix listen (no bed, no rendered video), and the per-beat A/V stills verification. The A/V table in `demo-av-table.md` is completed as far as the app source allows; all 19 "stills support it?" cells remain **UNVERIFIED (no stills)** — `out/qa/` is empty.
- Music fetch: not attempted (`yt-dlp` is not installed; the skill's design is warn-and-continue without a bed, and no bed was needed for this fixture).
- **No still was produced in this run, and no live film is claimed.** The invocation path now resolves up to and including a launched Remotion render; the remaining blockers are environmental (see §5).

## 5. The single failing check — attribution (not a plugin invocation defect)

**`demo-remotion-qa-live`: `node scripts/qa.mjs` exits 1, not 0.** The cause is NOT the invocation form the prior re-run failed on:

- The prior re-run's finding is **resolved and proven live**: `qa.mjs:42` now calls `npx -p @remotion/cli@4.0.526 remotion still …`; the command resolves (no "could not determine executable to run"), Remotion launches its auto-downloaded headless shell, bundles the composition, and begins rendering. The `render` form in `build.mjs:335` is likewise proven to resolve (`render --help` exits 0).
- The exit-1 cause is the composition's **runtime Google Fonts fetch**: the template's `src/fonts.ts` loads Hanken Grotesk / Instrument Serif / JetBrains Mono via `@remotion/google-fonts`, which `fetch()`es the font files from `fonts.gstatic.com` at render time. Inside Chrome in this sandbox that fetch fails (`net::ERR_SSL_PROTOCOL_ERROR`, `net_error -107`) and the render throws `TypeError Failed to fetch`. The same URL returns 200 via `curl`, and a direct headless-Chrome fetch of it hangs for 2+ minutes — Chrome's egress is blocked in this sandbox while Node/npm egress works.
- A diagnostic proxy wrapper for Chrome (reads the sandbox proxy from the environment at run time; no credential written anywhere) did **not** unblock it — the still failed identically. Remotion 4.0.526's CLI config exposes no generic Chromium-flags setting (`Config.setChromiumFlags` does not exist in this version; only `setBrowserExecutable` / `setChromiumIgnoreCertificateErrors` / `setChromiumDisableWebSecurity` / `setChromiumOpenGlRenderer` etc.), so there is no shipped-config way to hand Chrome the proxy; the wrapper probe was the only route tried.
- **What this means:** on a machine with normal network (where Chrome can reach `fonts.gstatic.com`), `qa.mjs` with the `-p` form should exit 0 — **but that is not proven here**, and this dry-run does not claim it. The literal key check as specified ("`qa.mjs` exits 0") is not met in this environment, so the verdict stays FAIL on that one check.
- **Observation for the coordinator (not a verdict driver):** the template fetches its fonts live at render time, while the plugin's standing font rule (fix #19/#21) is self-hosted static fonts. A render that depends on a live Google Fonts fetch fails in any restricted network, even with a working invocation. Whether the template should self-host its fonts (or the skill should record the network requirement) is the coordinator's call — this dry-run flags it, it does not fix it.

## 6. Other notes

1. **No runner bugs this run.** Both scripts passed on their first run (fixtures 42/42, demo 58/59); the single demo FAIL is a genuine live outcome, not a checker error — confirmed by three independent live executions (`qa.mjs` itself, the direct still probe, and the proxy-wrapper still probe) plus the direct-Chrome hang.
2. **The Playwright browser binary is still missing** (`~/.cache/ms-playwright/` holds only a partial directory listing; `record.mjs` fails at `chromium.launch()` exactly as in the prior runs). Remotion now supplies its own headless shell for stills/renders, so the QA/render path no longer depends on Playwright — but filming (`record.mjs`) still does.
3. **Older verifiers' stale fingerprints (same note as the prior runs).** verify22's regression leg notes fix19/fix20/fix21 pass except for their stale post-fix21 `build.sh` fingerprints (expected: `build.sh` changed under fix #22). verify22 itself is 368/368.
4. **No credentials were written anywhere.** The diagnostic proxy wrapper reads the sandbox proxy from the environment at run time; no proxy value appears in any file in this directory or in this report.

## 7. Verdict summary

| Section | Checks | Result |
|---|---|---|
| §13 depth | 7 | PASS (7/7) |
| §14 Thinking Orbs | 5 | PASS (5/5) |
| §15 libraries | 9 | PASS (9/9) |
| §16 Vercel guidelines | 5 | PASS (5/5) |
| §17 libraries | 6 | PASS (6/6) |
| §§8–12 regression | 10 | PASS (10/10) |
| /demo original contract (F1–F6, voice, $10 cap, local-only, Bang, invocation path) | 35 | PASS (35/35) — live film blocked by environment (see §4) |
| /demo removal verification (6 sites + follow-ups incl. :22, §7 conditional, B2S7, step-8 handoff, orchestrate step 0) | 13 | PASS (13/13) |
| /demo Remotion fix (text + pin + bin presence + live `-p`/local/render forms + invocation resolves) | 10 | PASS (10/10) |
| /demo Remotion fix (live `qa.mjs` exits 0) | 1 | **FAIL (0/1) — `node scripts/qa.mjs` exits 1 on the runtime Google Fonts fetch inside Chrome (environment-blocked); the invocation itself resolves and executes** |
| **Total** | **42 fixtures + 59 demo checks** | **FAIL — 42/42 fixtures, 58/59 demo checks** |

**DRY-RUN #37 RE-RE-RUN: FAIL** (one check: `qa.mjs` does not exit 0 in this sandbox — cause is the environment-blocked runtime font fetch, §5; the prior re-run's Remotion-invocation finding is resolved)

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-report.md` (this report)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-fixtures.py` (run: **42/42**, exit 0)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-output.txt`
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-demo.py` (run: **58/59**)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/dryrun37-rerun2-demo-output.txt`
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/sample-app/` (fixture app: `index.html`, `plan.html`)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/demo-sample-video/` (fresh template copy + `shots.json` + live `src/vo-durations.json`; `node_modules/` from the live `npm install`, exit 0, 257 packages; `node_modules/.remotion/chrome-headless-shell/` auto-downloaded by Remotion during the still probe)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/demo-av-table.md` (per-beat A/V table; stills column UNVERIFIED)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun2/npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `qa-exit.txt`, `remotion-still-probe.log`, `remotion-still-proxy-probe.log`, `chrome-direct-probe.log`, `remotion-p-help.log`, `remotion-render-help.log`, `remotion-render-help-exit.txt`, `remotion-local-help.log`, `tmp/proxy-chrome.sh` (live-run evidence; the wrapper is diagnostic-only and reads the proxy from the environment)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-report.md` + `fix22/dryrun37-rerun/dryrun37-rerun-fixtures.py` + `fix22/dryrun37-rerun/dryrun37-rerun-demo.py` (prior re-run — fixture structure reused, results re-derived)
- `~/workspace/hackathon-plugin/fix22/SPEC.md` (§§8–17), `fix22/verify22.py` (re-run this session: **368/368**, exit 0)
- `build.sh` measured this session: **23,774 lines, md5 `4799a819791b9c3ec4c19136ad698397`**
