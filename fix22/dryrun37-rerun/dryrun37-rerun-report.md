# Dry-run #37 RE-RUN — Fix #22 weave, new build (post /demo-removal + Remotion fix)

- **Date:** 2026-11-13, ~01:50–02:00 UTC (evening CST Nov 12 / early Nov 13). Worker: dry-run #37 re-run agent, check-only.
- **Scope kept:** read-only against the plugin tree and the built tree. All files written are inside `fix22/dryrun37-rerun/`: the fixture runner `dryrun37-rerun-fixtures.py` + captured output `dryrun37-rerun-output.txt`, the /demo checker `dryrun37-rerun-demo.py` + captured output `dryrun37-rerun-demo-output.txt`, the /demo fixture app `sample-app/` (fresh copy of the first run's), the video project copy `demo-sample-video/` (fresh copy of the NEW built `pitch-deck-video/template/` + the first run's `shots.json` + live `src/vo-durations.json`), the A/V table `demo-av-table.md` (copied from the first run; stills column still UNVERIFIED — no stills exist), and the live-run logs (`npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `playwright-install.log`, `remotion-help.log`, `remotion-still-probe.log`, `remotion-p-help.log`, `remotion-local-help.log`). This report is at `fix22/dryrun37-rerun/dryrun37-rerun-report.md`. No staged source, `build.sh`, built-tree file, or verifier edited; no commit, no bundle, no GitHub touch, no message to anyone.
- **Verdict: DRY-RUN #37 RE-RUN: FAIL — 1 of 51 /demo checks fails.** All 42 §13–§17 + §§8–12 fixtures pass (42/42) and all 35 original /demo contract checks pass (35/35). The /demo-removal verification passes 8/8. The Remotion fix is **incomplete**: the package name and version are corrected in the text (0 `remotion@4.0.542` in the built tree, both scripts now call `@remotion/cli@4.0.526`, pin matches), but the invocation **still cannot execute as written** — `npx @remotion/cli@4.0.526 still …` fails live with npm's "could not determine executable to run", because `@remotion/cli` carries three bins (`remotion`, `remotionb`, `remotiond`) and bare `npx <package>` cannot pick one. `qa.mjs` itself fails on exactly this (see §5, the single finding). The correct forms were verified live and work: `npx -p @remotion/cli@4.0.526 remotion …` and the locally installed bin (`npx --no-install remotion …`).

## 0. Starting state — verified this session, not trusted from the task

- `build.sh` = **23,773 lines, md5 `e9462b57429acd914cd0aacdebc486d0`** — matches the task's stated gate numbers.
- `fix22/verify22.py` re-run this session: **368/368 checks pass**, exit 0 (same stale-fingerprint note as the first run: fix19 71/76, fix20 164/169, fix21 96/102 on the regression leg — expected after `build.sh` changed, recorded as PASS lines by verify22 itself).
- Counts verified: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks**. (Hooks = 15 entries in `hooks/hooks.json`; the `hooks/` directory lists 17 files because it also holds `adapter.js` and `hooks.json` themselves — not a discrepancy.)
- **What changed since the first run, verified by diff, not assumed:** diffing the fresh template copy against the first run's template copy (`--exclude=node_modules --exclude=out`, plus `shots.json` reused as the fixture input) shows **exactly two files differ**: `scripts/build.mjs:335` and `scripts/qa.mjs:42`, each changing only `remotion@4.0.542` → `@remotion/cli@4.0.526`. No other template file changed. The removal touched orchestrate / orch-build-mvp / orch-change-feature / hackathon-mode / commands/demo.md / dispatch-prompt.md only — none of which is in the pitch-deck-video template or skill.

## 1. /demo auto-invocation removal — verified at all 6 sites + follow-ups (8/8 checks)

All anchors asserted verbatim (whitespace-normalised) by `dryrun37-rerun-demo.py` against the NEW built tree:

| Site | Anchor found in the new build | Result |
|---|---|---|
| orchestrate step 5d | `DEMOGATE_O4_F22` + "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline" — runs ONLY on explicit user invocation (or an explicit demo-video request) | PASS |
| orchestrate step 6 (follow-up) | `DEMOGATE_O9_F22` + "A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order" | PASS |
| orch-build-mvp step 8 | `DEMOGATE_B2S1_F22` + "`/demo` is not filmed here" — ONLY when the user invokes it explicitly; films the LOCAL app, never the deployed URL (`DEMOGATE_B2S2_F22`) | PASS |
| orch-build-mvp step 9 (follow-up) | `DEMOGATE_B2S3_F22`–`B2S6_F22` present; README before final report, report notes "no demo video was filmed" when none was requested | PASS |
| orch-change-feature step 5 | `DEMOGATE_B3S1_F22` + "If the user asks for a re-film, re-film via `/demo --rebuild`" + "no re-film happens here"; done-condition is re-filmed video OR flagged-stale (`DEMOGATE_B3S5_F22`); narration continuity + re-upload rules (`B3S2`–`B3S4`, `B3S6`) | PASS |
| hackathon-mode §7 mandate | `DEMOGATE_H1_F22`: "The first build does NOT film `/demo` automatically"; `DEMOGATE_H2_F22`: "/demo is never part of this sequence" (line 12 sequence); line 61 §7 timing text (narration-key prompt scheduled here, sent by orchestrate) intact | PASS |
| commands/demo.md dispatch note | Still dispatches to pitch-deck-video (`/demo`, `/demo <path>`, `/demo --rebuild`, `--script`, `--render`, `--montage`/`--explainer` opt-in); key-via-dispatch rule intact | PASS |
| dispatch-prompt.md Environment field | Environment field carries `ELEVENLABS_API_KEY=<redacted>` "on a /demo dispatch when a narration key was received mid-build"; omit when not needed; never in a file/log/ledger | PASS |

**Explicit invocation still reaches the filming pipeline — proved, not assumed:** `commands/demo.md` still loads the pitch-deck-video skill with all `/demo` forms; the pitch-deck-video skill itself carries **no** `DEMOGATE` token and no "never automatic" / "NEVER dispatched" language (checked in the runner); the template copy's pipeline files are all present and `build.mjs` still runs `tts → record → frames` in that order (demo-path checks, §4); `tts.mjs` executed live and accepted the fixture `shots.json` (§4.2). The removal removed only the automatic dispatches, not the on-demand path.

## 2. Fixtures — 42/42 (re-run against the NEW built tree)

Same fixture structure as the first run, re-derived from the SPEC (expected PASS/FAIL per fixture is the SPEC's expected outcome; "FLAG/FAIL" strings are expected-outcome labels, not failures). All rule anchors re-asserted verbatim against the new built tree before running — all present. Condensed per-section results (full per-fixture tables are in the first run's report; the inputs, judging checks, and observed outcomes are identical here — see `dryrun37-rerun-output.txt`):

| Section | Fixtures | Result |
|---|---|---|
| §13 depth (a)–(f) + Depth-dimension check | 7 (13a–13g) | PASS (7/7) |
| §14 Thinking Orbs (a)–(e) | 5 (14a–14e) | PASS (5/5) |
| §15 libraries (a)–(g) + 15h/15i | 9 (15a–15i) | PASS (9/9) |
| §16 Vercel guidelines (a)–(e) | 5 (16a–16e) | PASS (5/5) |
| §17 libraries (a)–(f) | 6 (17a–17f) | PASS (6/6) |
| §§8–12 regression (H1/H2, Mobbin, directives, §11, Bang) | 10 (8-H1a, 8-H2b, 9a, 9b, 10a, 10b, 11a, 11c, 12a, 12b) | PASS (10/10) |
| **Total** | **42** | **PASS (42/42, exit 0)** |

Proxies (same as the first run, recorded explicitly): fixtures are decision-record / design-package / token / handoff / composition inputs judged against the static checks the skills state — static checks producing candidate evidence, never screen verdicts (fix #13e). §16d models "reported as a fixable finding" as the check producing the finding; §17b models the OriginKit cap path as the graceful outcome. No fixture findings.

## 3. /demo — 50/51 checks (35/35 original + 15/16 new)

### 3.1 Fixture (same as the first run, fresh copies)

- **Sample app:** `fix22/dryrun37-rerun/sample-app/` — "Pantry Pal" (`index.html` + `plan.html`), served locally at `http://localhost:5180` (verified `200` on `/` and `/plan.html` while running; server stopped afterwards).
- **Video project:** `fix22/dryrun37-rerun/demo-sample-video/` — fresh copy of the NEW built `pitch-deck-video/template/` + the first run's `shots.json` (12 beats, edge at position 3, 6 features, 1 recorded cut, arch fallback, theme pulled from the app's own tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block with opener concept 5 + "Editorial light" + 3 kinetic-type rows + 2 camera-move rows).
- **Checker:** `dryrun37-rerun-demo.py` — the first run's 35 checks plus 16 new checks (8 removal, 8 Remotion). **Result: 50/51** (`dryrun37-rerun-demo-output.txt`).

### 3.2 Original 35 checks — all pass

Invocation path resolves end-to-end (all 9 pipeline files present; `build.mjs` order `tts → record → frames`; `package.json` `all` = `node scripts/build.mjs`); local-only filming (`http://localhost:5180`); F1 6/6 coverage, all filmed; F2 stack labels + no-model-calls fallback; F3 edge at `shots[2]`; F4 theme source recorded, not the seed theme, vignette recorded; F5 A/V table in skill + kinetic/camera rows recorded, mix gain 0.14 (≤ 0.20); F6 total **84.1s** from `vo-durations.json` (LEAD 0.7 + sum(dur+gap) 81.7 + TAIL 1.7) — under 2:10 (130s) and within the 2:30 absolute max (same estimated-duration caveat as the first run: no voice provider existed, so durations are word-count estimates, not measured narration); voice default Rachel (`21m00Tcm4TlvDq8ikWAM`), no key written anywhere, fallback chain present; $10 cap present, $0 spent; Bang rules present and recorded. Gorgeousness-from-stills and the 10-second mix listen remain unverified (no stills, no render — see §4.2).

### 3.3 New checks — 15/16 pass

- Removal 8/8 (see §1).
- Remotion text-level 5/5: 0 `remotion@4.0.542` anywhere in the built tree (walked, excluding `node_modules`); `build.mjs` uses `@remotion/cli@4.0.526`; `qa.mjs` uses `@remotion/cli@4.0.526`; template `package.json` pins `@remotion/cli` at `4.0.526`; installed `node_modules/@remotion/cli/package.json` carries a bin entry — and that entry is the crux: **`{"remotion": "remotion-cli.js", "remotionb": "remotionb-cli.js", "remotiond": "remotiond-cli.js"}` — three bins**, while `node_modules/remotion/package.json` has `bin: undefined` (confirming the original diagnosis that the `remotion` package carries no executable).
- Remotion live-resolution 2/3: `npx -p @remotion/cli@4.0.526 remotion --help` → exit 0, prints `@remotion/cli 4.0.526` (PASS); `npx --no-install remotion --help` → exit 0, same (PASS); **`npx @remotion/cli@4.0.526 still …` (the exact form in `qa.mjs`/`build.mjs`) → exit 1, "could not determine executable to run" (FAIL — demo-remotion-npx-live).**

## 4. Live-vs-not-executed record (exactly what ran, and what did not)

**Executed live in this environment:**

| Step | Command / evidence | Outcome |
|---|---|---|
| Sample app served | `python3 -m http.server 5180` in `sample-app/`; `curl` | `200` on `/` and `/plan.html`; server stopped after the exercise |
| Dependencies | `npm install --no-audit --no-fund` in the video project, `TMPDIR` redirected to the disk-backed rerun `tmp/` (`npm-install.log`) | **exit 0, 257 packages added** (same count as the first run) |
| Narration | `node scripts/tts.mjs` (`tts-run.log`) | **exit 0.** "available providers: none (no ELEVENLABS_API_KEY, no MiniMax credentials, no Piper, no say)". Narration skipped; estimated beat lengths written to `src/vo-durations.json` (12 shots, narration total with gaps **81.7s**). No key used or written anywhere. |
| Recording (filming entry point) | `node scripts/record.mjs` (`record-run.log`) | **exit 1 at `chromium.launch()`**: "Executable doesn't exist at `~/.cache/ms-playwright/chromium_headless_shell-1243/...`". Entry point resolves (script parses, reads `shots.json`, reaches the launch call); only the browser binary is missing. |
| Remotion bin probe | `npx @remotion/cli@4.0.526 still src/index.ts Demo … --frame=111 --log=error` (`remotion-still-probe.log`) | **exit 1: "could not determine executable to run"** — the exact qa.mjs form does not resolve. |
| Remotion `-p` form | `npx -p @remotion/cli@4.0.526 remotion --help` (`remotion-p-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526` + available commands. |
| Remotion local bin | `npx --no-install remotion --help` (`remotion-local-help.log`) | **exit 0** — prints `@remotion/cli 4.0.526` + available commands. |
| QA | `node scripts/qa.mjs` (`qa-run.log`) | **exit 1.** Prints "rendering 12 stills…", then fails on `Command failed: npx @remotion/cli@4.0.526 still src/index.ts Demo …/out/qa/00111_problem.png --frame=111 --log=error` with npm error "could not determine executable to run" (npm debug log: `getBinFromManifest`, `pkgid @remotion/cli@4.0.526`). The QA step still cannot execute as written. |
| Browser install | `npx playwright install chromium-headless-shell`, `TMPDIR` on disk with 146G free (`playwright-install.log`) | **exit 1.** Reached ~90% of `chrome-headless-shell-linux64.zip` (114.3 MiB), then "Download failed: server closed connection" from `cdn.playwright.dev` (twice in the log — the installer retried once). This time the /tmp ENOSPC limit was NOT a factor (disk-backed TMPDIR); the failure is the CDN closing the connection, same as the first run's attempts 2–3. No browser binary exists on disk; no system Chrome/Firefox exists either. |

**Not executed live (no footage, no render, no video):**

- Filming (`record.mjs` take), `frames.mjs`, the Remotion render (`build.mjs --render` / `npm run all` end-to-end), contact sheets, the 10-second mix listen (no bed, no rendered video), and the per-beat A/V stills verification. The A/V table in `demo-av-table.md` is completed as far as the app source allows; every "stills support it?" cell remains **UNVERIFIED (no stills)**.
- Music fetch: not attempted (`yt-dlp` is not installed; the skill's design is warn-and-continue without a bed, and no bed was needed for this fixture).
- **/demo is therefore NOT verified as working on the basis of wiring alone:** the invocation path resolves up to the recording entry point and the narration step, but the render/QA path is blocked by the still-unexecutable Remotion invocation (a plugin defect, §5) and filming is blocked by the environment (no browser binary).

## 5. The single finding (for the coordinator — not fixed by this worker)

**The Remotion fix is incomplete: `npx @remotion/cli@4.0.526 <cmd>` cannot execute, because `@remotion/cli` exposes three binaries.**

- The coordinator changed the package specifier (`remotion@4.0.542` → `@remotion/cli@4.0.526`) and aligned the version with the template's pin — both verified correct in the text.
- But npm's `npx <package>@<version> <args>` resolves the executable from the package manifest's `bin` field, and when `bin` is an object with **multiple** entries, `getBinFromManifest` throws "could not determine executable to run" (confirmed in the npm debug log: `at getBinFromManifest (…/libnpmexec/lib/get-bin-from-manifest.js:17:23)`, `pkgid @remotion/cli@4.0.526`). `@remotion/cli@4.0.526` ships three bins: `remotion`, `remotionb`, `remotiond`.
- Affected call sites (unchanged in form, only the specifier changed): `template/scripts/qa.mjs:42` (`npx @remotion/cli@4.0.526 still …`) and `template/scripts/build.mjs:335` (`npx @remotion/cli@4.0.526 render …`). Both fail the same way; `qa.mjs` was run live and fails on it, and the render call in `build.mjs` would fail identically (not reached live — filming blocks first — but the invocation form is the same and was probed live with `still`).
- Verified-working alternatives (both exit 0 live): `npx -p @remotion/cli@4.0.526 remotion still|render …` (explicit binary after `-p`) or the locally installed bin (`npx --no-install remotion still|render …`, i.e. the project's own `remotion` binary — the first run's suggested form). Either form needs the coordinator to pick one and apply it at both call sites, then this re-run's `demo-remotion-npx-live` check should be re-run against the corrected form.
- This is a pitch-deck-video template issue, not a §13–§17 rule defect, and it does not change any of the 42 fixture outcomes. It does change this re-run's verdict, because verifying this fix was one of the re-run's two stated purposes and the invocation still does not resolve.

## 6. Other notes

1. **Live filming was blocked by the environment, not the plugin** (same as the first run, minus the /tmp limit): the Playwright download reaches ~90% and `cdn.playwright.dev` closes the connection, even with TMPDIR on a disk with 146G free. A machine with a working browser download would film the fixture as written (`shots.json` accepted by `tts.mjs`, selectors verified against the served app). The A/V stills verification and the 10-second mix listen remain owed on a real render.
2. **No runner bugs this run.** Both scripts passed on their first run (fixtures 42/42, demo 50/51); the single demo FAIL is a genuine plugin finding, not a checker error — confirmed by two independent live executions (the probe and `qa.mjs` itself) plus the npm debug-log stack.
3. **Older verifiers' stale fingerprints (same note as the first run).** verify22's regression leg notes fix19/fix20/fix21 pass except for their stale post-fix21 `build.sh` fingerprints (expected: `build.sh` changed under fix #22). verify22 itself is 368/368.

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
| /demo removal verification (6 sites + follow-ups + explicit-path intact) | 8 | PASS (8/8) |
| /demo Remotion fix (text + pin + bin presence + live `-p`/local forms) | 7 | PASS (7/7) |
| /demo Remotion fix (live bare-npx invocation) | 1 | **FAIL (0/1) — `npx @remotion/cli@4.0.526 still` → "could not determine executable to run"** |
| **Total** | **42 fixtures + 51 demo checks** | **FAIL — 42/42 fixtures, 50/51 demo checks** |

**DRY-RUN #37 RE-RUN: FAIL** (one finding: the Remotion invocation form; see §5)

## Files / evidence (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-report.md` (this report)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-fixtures.py` (run: **42/42**, exit 0)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-output.txt`
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-demo.py` (run: **50/51**)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/dryrun37-rerun-demo-output.txt`
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/sample-app/` (fixture app: `index.html`, `plan.html`)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/demo-sample-video/` (fresh template copy + `shots.json` + live `src/vo-durations.json`; `node_modules/` from the live `npm install`, exit 0, 257 packages)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/demo-av-table.md` (per-beat A/V table; stills column UNVERIFIED)
- `~/workspace/hackathon-plugin/fix22/dryrun37-rerun/npm-install.log`, `tts-run.log`, `record-run.log`, `qa-run.log`, `playwright-install.log`, `remotion-help.log`, `remotion-still-probe.log`, `remotion-p-help.log`, `remotion-local-help.log` (live-run evidence)
- `~/workspace/hackathon-plugin/fix22/dryrun37-report.md` + `fix22/dryrun37/dryrun37-fixtures.py` + `fix22/dryrun37/dryrun37-demo.py` (first run — fixture structure reused, results re-derived)
- `~/workspace/hackathon-plugin/fix22/SPEC.md` (§§8–17), `fix22/verify22.py` (re-run this session: **368/368**, exit 0)
- `build.sh` measured this session: **23,773 lines, md5 `e9462b57429acd914cd0aacdebc486d0`**
