# Fix #18 — manifest (pitch-deck-video: the 7 video criteria)

- **Status:** CLOSED. Audit #59 CLEAN (0/0), dry-run #29 PASS, sweep #22 CLEAN.
- **Engine:** `fix18/fix18.py` (preflight + staged edits; 33 subs, all count==1 asserts) + `fix18/fix18_fixup.py` (fix-up round; 9 subs, sequential count asserts).
- **`build.sh`:** 23,276 lines, md5 `5cdd22787dfd56aed0b360e49dae60f2` (post-fix-up; pre-fix-up `1a999d763e6ec1fb16985d346b106df0`, post-fix17). Backup `build.sh.before-fix18`. Line count unchanged by fix18 (all fix-up edits are same-line substitutions).
- **Counts:** 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks — unchanged.
- **Goal (Anish):** check the video demo creation skill (`pitch-deck-video`, `/demo`) so a demo video is actually good: all features, real functionality, the problem, the tech stack, what makes it unique, visually gorgeous above all, voice/audio matching the visuals. Plus the hard runtime rules (under 2:10, absolute max 2:30, time allocation).

## 1. What changed — every rule change (file:line, anchor → addition)

Full rule texts live in `fix18/fix18.py` (constants STEP3_ADD, STEP4_THEME_ARCH, CAPS_F6, ALLOCATION_F6, ARC_F1F3, STEP6_QA, FEATURES_CUTS_SECTION, ARCH_NODES_SECTION, SEED_FEATURES_CUTS, SEED_EDGE_SHOT, QA_COMPUTE, QA_TAIL) and `fix18/fix18_fixup.py`. Line numbers are the BUILT tree after build 4.

### Staged sources (edited directly; build.sh copies pitch-deck-video verbatim)

| # | File (built line) | Anchor (old) | Addition (new) |
|---|---|---|---|
| 1 | `new-skills/pitch-deck-video/SKILL.md` → :3 | Frontmatter "Generates a narrated 1:30–1:50 product demo" | "Generates a narrated product demo, under 2:10," (F6) |
| 2 | SKILL.md → :75/:77 | Step-3 paragraph end ("…only the screenshots tell you that.") | F1 feature enumeration (`features`/`cuts` arrays, "shown" rule, cap governance) + F4 best-state selection per beat |
| 3 | SKILL.md → :97 | Step-4 theme/arch paragraph ("Pull the `theme.colors`…") | F4 `theme.source` record + F2 arch-node `stack` labels (from `package.json` + decision record, never invented) + spoken stack line, one phrase |
| 4 | SKILL.md → :101 | Caps bullet (1:30–1:50, 2:00 cap) | F6: under 2:10 (130s) hard rule from MEASURED durations, absolute max 2:30 never exceeded, leave ~10s room |
| 5 | SKILL.md → :102–114 | Before "Narration rules that matter:" | F6 allocation table + budget-before-lines rule (Problem 8–10, Wow 14–18, Edge 8–10, How/features 55–65 largest, Proof 12–15, Close 6–8, ~10s room) |
| 6 | SKILL.md → :137–140 | Arc 1–5 (Problem/Wow/How/Proof/Close) | F3 Edge beat 3 (one sentence, alternative named or implied, never invent a competitor claim) + F1 How grows: one beat per remaining must-have feature from the 12–16 beat budget; 6 beats total |
| 7 | SKILL.md → :135 | Pacing "12–16 beats over 90–110 seconds" | "12–16 beats under 2:10" (F6) |
| 8 | SKILL.md → :196–201 | Step-6 QA list (warnings empty, caption-frame manual check) | F1 coverage line, F5 per-beat A/V table (a "no" is BLOCKING), F4 gorgeousness checks (a)(b)(c), F6 runtime line, F5 10-second mix listen, F4 theme-pulled line |
| 9 | `references/shots-reference.md` → :19–20 | Top-level table `shots` row | `features` + `cuts` rows documented |
| 10 | shots-reference.md → :36 | Before "## Actions" | "## features / cuts" section (source, "shown" rule, cap governance) |
| 11 | shots-reference.md → :41–42 | Before "## app" | "## cards — arch nodes" section (optional `stack` field, Arch.tsx render, spoken phrase) |
| 12 | shots-reference.md | `theme` row | `theme.source` + `theme.vignette` (0–1, default 0.3; 0 for light apps) |
| 13 | shots-reference.md | `gapMs` row | Gap counts toward the 2:10 total (qa.mjs prints it, over 2:10 BLOCKING) |
| 14 | shots-reference.md | Music paragraph end | `under` above 0.20 warning + step-6 mix check |
| 15 | `template/shots.example.json` + `template/shots.json` (both, identical except tts) | After `tagline` | Seed `features` (1 entry → `result`) + `cuts` (1 entry, 2:10-cap reason) |
| 16 | Both seed JSONs | Arch nodes Ranker/Scheduler/Writer | `stack` labels: Ranker "GPT-5", Scheduler "Next.js 15", Writer "GPT-5" (in/out nodes: no stack — field is optional) |
| 17 | Both seed JSONs | Arch `say` | "…Built on Next.js and GPT-5 — this is the credibility beat." (F2 spoken line) |
| 18 | Both seed JSONs | Before `arch` shot | Seed Edge shot (`id: "edge"`, kind `app`, `focus` on the differentiating element) — shot order now hook/setup/result/edge/arch/close |
| 19 | `template/src/scenes/Arch.tsx` → :10 | `type Node = { label; note; kind }` | `stack?: string` added to the Node type |
| 20 | Arch.tsx → :41 | After the node-label div | Stack label rendered under the label (mono 15px, accent color — SPEC F2 literal; fix-up corrected the kind tone) |
| 21 | `template/scripts/qa.mjs` → :99–138 | End print block (5 manual checks) | F6 total-runtime print (LEAD 0.7 + Σ(dur+gap) + TAIL 1.7, same derivation as timeline.ts TOTAL) + BLOCKING over 130s / ceiling 150s; F1 coverage table + missing-beat flag; F4 theme-vs-seed comparison (seed bg #0d0a24 / accent #ffc93c / card #161141; FAIL without `theme.source`) + vignette print; F5 per-shot A/V table skeleton; F5 `under`-gain warning over 0.20; `process.exitCode = 1` on any BLOCKING finding |
| 22 | `commands/demo.md` → :2, :9 | "1:30–1:50" (×2) | "under 2:10" (F6 regime change) |

### Fix-up round (after audit #58 + sweep #21; `fix18_fixup.py`, 9 subs)

| # | File (built line) | Anchor (old) | Change (new) |
|---|---|---|---|
| 23 | SKILL.md → :114 | "Totals: 113–126s of content" (MINOR-1) | "Totals: 103–126s of content" — rows sum to 103–126 (8+14+8+55+12+6=103; 10+18+10+65+15+8=126). The SPEC's own arithmetic error, corrected in `fix18/SPEC.md` §F6 too |
| 24 | Arch.tsx → :41 | Stack div `color: col` (kind tone) | `color: C.accent` — SPEC F2 "(mono, accent color)" literal (audit #58 observation) |
| 25 | `new-rules/hackathon-mode.mdc` → :48 | Canonical "the demo video is 1:30–1:50" | "the demo video is under 2:10 (hard rule; absolute max 2:30)" — the canonical statement still claims governance, now over the new regime |
| 26 | `rewritten-skills/hackathon-scope/SKILL.md` → :17 | Same restatement | Same replacement |
| 27 | `build.sh` → :18368 (README heredoc) | "- `/demo` — generate a narrated 1:30–1:50 product demo video" | "- `/demo` — generate a narrated product demo video, under 2:10, of the app" |
| 28 | `build.sh` → :13406 (Fix-4 patch NEW side) | "- Video (demo video, 1:30–1:50)…" | "- Video (demo video, under 2:10)…" (the patch itself INTRODUCED the old length; its NEW side is the fix) |
| 29 | `build.sh` → :20079 (Gap-39 comment) + :20084 (Gap-39 NEW) + :21138/21139 (Batch-F old/new) | Line-32 text with "1:30–1:50" (×2 per occurrence; 3 occurrences + comment) | "(under 2:10, pitch-deck-video / /demo)" + "the demo video is under 2:10 (hard rule; absolute max 2:30)" in all four spots. The line-32 canonical tail is WRITTEN by Gap-39's patch (upstream has only the short sentence), so the fix goes in the patch strings — no separate patch needed. Order matters: the comment was fixed before the fragment replace (it holds the same fragment) |

## 2. Baseline → final (7 criteria)

| # | Criterion | Baseline | Final | Evidence |
|---|---|---|---|---|
| 1 | Shows functionality (real app, live) | YES | YES (unchanged) | Film mode + stub ban intact (S1) |
| 2 | Addresses the problem (user's words) | YES | YES (unchanged) | Problem-first opening intact (S2) |
| 3 | Includes ALL features | NO | YES | F1: `features`/`cuts` + coverage table; dry-run #29 coverage complete, 7 features, 0 cuts |
| 4 | Names the tech stack | NO | YES (rule); PARTIAL (trace) | F2: stack labels + spoken line. Trace partial only because no stack is recorded anywhere in the Home Run standing record — the F2 fallback was applied correctly (see §3) |
| 5 | States what makes it unique | NO | YES | F3: Edge beat; dry-run Edge present, alternative named |
| 6 | Visually gorgeous (above all) | NOT GUARANTEED | GUARANTEED (checked) | F4: theme-as-check + 3 gorgeousness QA checks; dry-run theme pulled, seed absent |
| 7 | Voice/audio matches visuals | PARTIAL | ENFORCED | F5: per-beat A/V table BLOCKING + 10s mix listen + under-gain warning; dry-run skeleton only (no live render in this VM — see §3) |

**Score: 2 yes / 1 partial / 4 no → all 7 covered by enforced rules; the trace confirms 5 full passes + 2 honest partials that need a live run.**

## 3. Re-trace — dry-run #29 (PASS)

Home Run storyboard under the new rules (full report: `fix18/dryrun29-report.md`). No `docs/scope.md` exists in this workspace — the must-have list was reconstructed from the standing record (Anish's final build report, Nov 11 ~01:10 CST, recorded in `memory/2026-11-11.md`) and the report says so. 7 features, 0 cuts, 16 beats (budget max — any added must-have forces a cut or merge).

| Section | Beats | Seconds (estimated) | Band | Verdict |
|---|---|---|---|---|
| Problem | 1 | 8.24 | 8–10 | in band |
| Wow | 1–2 | 16.88 | 14–18 | in band |
| Edge | 1 | 9.84 | 8–10 | in band |
| How / features | 6–9 | 60.56 | 55–65 | in band, largest share |
| Proof (arch + stack) | 1–2 | 13.68 | 12–15 | in band |
| Close | 1 | 7.04 | 6–8 | in band |
| Room | — | 11.36 | ~10 | — |
| **Total** | **16** | **118.64s** | **under 130s** | **PASS, no re-cut needed** |

Basis stated: 150 wpm = 2.5 words/sec, whitespace-split counts; these are ESTIMATES, not measured TTS durations. Criterion 4 trace partial: arch says "phone-first web app" only — no stack item is recorded anywhere in the standing record (checked the build-report memory entry, fix13 manifest, tree-wide grep), so none was invented; a real run reads the app's `package.json`. Criterion 7 trace partial: A/V table is a skeleton until real QA; mix listen not performed; theme hex/font values are flagged stand-ins (the record gives the palette description, not token values).

### qa.mjs functional test (built tree, stubbed `npx`/`ffmpeg` on PATH; re-verified by the coordinator)

- Baseline: exit 0. Prints total 118.6s, complete coverage table (all "filmed"), "Theme: pulled from the app tokens", "Vignette: theme.vignette = 0", A/V skeleton for all 16 shots, "No BLOCKING findings from the automated checks."
- (a) seed theme, no source → exit 1: `BLOCKING — theme: shots.json still carries the seed theme with no recorded theme.source`
- (b) total 136.6s → exit 1: `BLOCKING — runtime: 136.6s over the 2:10 (130s) hard rule — re-cut`
- (c) feature beat id deleted → exit 1: `BLOCKING — coverage: feature "Shared request record + shared fee policy" → beat "how-missing" missing from shots.json` (row shows `MISSING BEAT`)
- (d) `music.gain.under` 0.25 → exit 0 with `WARNING: music.gain.under is 0.25 (over 0.20) — the bed risks burying the voice…` (warning only, no BLOCKING)

## 4. Checker results — audit / dry-run / sweep

| Check | Result | Report |
|---|---|---|
| Audit #58 (first round) | **NOT CLEAN — 0 blocking, 1 minor** (MINOR-1: allocation totals 113 vs 103) | `fix18/audit58-report.md` |
| Dry-run #29 | **PASS** — 16-beat trace, 118.64s, all sections in band; criteria 4 + 7 partial with documented trace limits | `fix18/dryrun29-report.md` |
| Sweep #21 (post-build 2) | **NOT CLEAN — 1 finding** (`1:30–1:50` survives in 5 cross-references) | `fix18/sweep21-report.md` |
| Audit #59 (re-audit after fix-up) | **CLEAN — 0 blocking, 0 minor** | `fix18/audit59-report.md` |
| Sweep #22 (re-sweep after fix-up) | **CLEAN (0/0)** — old length 0 tree-wide + 0 in build.sh; pins match fix16; build.sh inventory delta 0 | `fix18/sweep22-report.md` |

### The fix-up (between first and second checker rounds)

- **Faults:** (1) SPEC's own totals arithmetic (113 vs 103) copied into SKILL.md:114. (2) Five cross-references outside pitch-deck-video still stated the old regime — including the canonical statement in hackathon-mode §6, which claims to govern.
- **Changes:** `fix18_fixup.py` (9 subs) + SPEC.md totals line. Staged edits: SKILL.md totals, Arch.tsx accent, `new-rules/hackathon-mode.mdc`, `rewritten-skills/hackathon-scope/SKILL.md`. build.sh edits: README heredoc, Fix-4 NEW side, Gap-39 comment + NEW, Batch-F old + new (line-32 text, 3 occurrences). `build.sh` baseline updated in `fix15/verify15.py`, `fix17/verify17.py`, `fix18/verify18.py` (md5 only — baseline update, NOT an anchor change; fix #16/#17 precedent).
- **Check:** changed-files set build 1 → build 3 is exactly the 7 fix-up files (README, hackathon-mode.mdc, hackathon-pitch SKILL.md + template, hackathon-scope SKILL.md, pitch-deck-video SKILL.md + Arch.tsx); vs fix17 final, exactly 12 changed entries (7 + 5). No other built file changed.

### Builds (build.sh, all exit 0)

| Build | Lines (md5) | Manifest hash | Diff vs previous | Note |
|---|---|---|---|---|
| 1 | 23,276 (`1a999d76…`) | `4c62aa1a…` | — (first post-fix18) | 2,665 files; ERRORS: 0 |
| 2 | 23,276 (`1a999d76…`) | `4c62aa1a…` | 0 | audit #58 / dry-run #29 / sweep #21 taken here |
| 3 | 23,276 (`5cdd2278…`) | `ea1c12e3…` | exactly 7 entries (fix-up) | post-fix-up |
| 4 | 23,276 (`5cdd2278…`) | `ea1c12e3…` | 0 | final; verify18 72/72, verify15 43/43, verify17 59/59 |

### Verifiers

- **`fix18/verify18.py`: 72/72 PASS** (66 original + 6 fix-up checks: totals 103–126, accent color, 3 cross-ref checks, old-length-0 tree-wide).
- **`fix15/verify15.py`: 43/43 PASS** (baseline check #8 updated to the post-fix-up build record).
- **`fix17/verify17.py`: 59/59 PASS** (baseline check #12 updated to the post-fix-up build record).

## 5. Standing rules — no regressions (all sweep-verified)

- Staged sources only edited, except the build.sh patches for upstream hackathon-pitch + the README heredoc (the established mechanism for those files); built tree edited only by build.sh. Build.sh is the source of truth.
- `fix11/fix11-stage.py` NOT re-run. Fix #15 canonical variety + theme-match block verbatim ×11 (11 files) — intact. Fix #17 anchors — E1 identical ×4 (md5 `e9d21025…`), sticker exceptions A+B, M1/M2, less-flat-ui treatments 1..23.
- Fix #16 Grok pins untouched: whole-tree `grok-4.7-high` 52 occ / 45 lines, `cursor-grok-4.6-high-fast` 100 occ / 99 lines; bare `grok-4.6-high-fast` 0; bracket syntax 0; `effort=` 0; `reasoning_effort` 2 (rules/common-performance.mdc:30, skills/orchestrate/SKILL.md:160); banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5) 0. build.sh exception inventory re-derived: 798 lines (389 OLD-side, 52 comment, 355 NEW-side transient, 0 heredoc, 2 build-time `.claude/skills/` paths) — delta 0 vs fix16 sweep #18.
- Untouched per SPEC §4: voice rules (sample check, fallback chain, ask-once key prompt), $10 budget cap + $0.50 threshold, local-only filming, the Don'ts, the three modes, 12–16 beat count. F1/F3 spend the existing beat budget; they do not extend it.
- Deliberately NOT changed (noted, not defects): the three 90-second ElevenLabs quota examples (SKILL.md:420/:529, shots-reference.md:242) — typical-length figures in the voice sections, not the cap. The `(0:30-1:30)` / `(1:30-2:30)` minute markers in hackathon-scope:24–25 and storytelling.md:309–310 — live-demo / pitch-script timestamps, not the video length. `qa.mjs` blocks only `> 130`, so exactly 130.0s passes "under 2:10" — SPEC enforcement is "over 2:10", measure-zero boundary (audit #58 adjudication).

## 6. Decisions and deviations

- **Cross-reference fix-up (binding decision by this coordinator):** SPEC §6 scoped fix18 to pitch-deck-video files, but the sweep found the old regime repeated in 5 files outside that scope — including the canonical statement that claims to govern. Leaving them would leave the plugin self-contradictory (a rule overriding the new skill rule). Fixed as part of F6 ("this REPLACES the skill's current time regime"), not as a scope expansion: the regime is replaced everywhere it is stated, and the canonical statement now states the new regime.
- **SPEC totals correction:** the SPEC's own "113–126s" was wrong (rows sum to 103–126); corrected in both SPEC.md §F6 and SKILL.md:114. Note the table max (126s) + ~10s room exceeds 130s on paper — the room figure is approximate and the QA `> 130` block is the binding constraint, not the totals line.
- **Arch.tsx accent literal:** the first implementation used the node kind tone for the stack label; the SPEC says "(mono, accent color)" — made literal (`C.accent`) in the fix-up.
- **Pre-existing staged/built drift (NOT fixed, NOT fix18's):** `new-rules/hackathon-mode.mdc` staged :38 still reads "upstream `claude -p` invocation path" while the built tree reads "upstream CLI-subprocess invocation path" — the documented fix16 build-time scrub (`fix16/MANIFEST.md:771`; `build.sh:23204` runs `fix16.py` on the built tree as the last step). Built side is compliant (0 banned terms); staged side is upstream text the scrub rewrites at build time. A future program could move the rewrite into the staged source if literal staged==built is ever required.

## 7. Artifacts and evidence files

- `fix18/fix18.py` — engine (preflight + 33 edits; count==1 asserts; self-checks: seed JSONs parse, `node --check qa.mjs`, banned-term scan, old-regime gone).
- `fix18/fix18_fixup.py` — fix-up engine (9 subs, sequential count asserts incl. a count==3 replace).
- `fix18/verify18.py` — 72/72.
- `fix18/SPEC.md`, `fix18/BASELINE.md` — inputs (SPEC totals line corrected in the fix-up).
- `fix18/audit58-report.md`, `fix18/dryrun29-report.md`, `fix18/sweep21-report.md`, `fix18/audit59-report.md`, `fix18/sweep22-report.md`, `fix18/build1-4.log`, `fix18/manifest1-4.txt`, `fix18/manifest1-4-files.txt`, `build.sh.before-fix18`.
- Test harness evidence (dry-run worker): `/tmp/fix18-qatest/` (traced project + synthetic vo-durations/marks), `/tmp/fix18-stubbin/` (npx/ffmpeg stubs), `/tmp/qa-baseline.log`, `/tmp/qa-neg.log` (coordinator re-runs).
- The Campus Eats artifact was NOT touched.

## 8. Left open

- **Fix #18 needs a live render to fully close criteria 4 + 7:** the trace could not name Home Run's stack (unrecorded anywhere — a real `/demo` run reads the app's `package.json`) and could not complete the per-beat A/V table or the 10-second mix listen (no live app, voice key, or Remotion in this VM). The rules + QA enforcement are in place; the first real `/demo` run (the live smoke test in Anish's Cursor) is what proves them end to end.
- No commit, no bundle, no GitHub touch was made by this fix (per instructions).
- The live smoke test in Anish's Cursor remains a separate open item (not part of fix #18).
- Two process notes from the checker rounds: (1) audit #58's delivery carried a killed subprocess record (SIGTERM, session proc_67f1c397f7ee) — incidental, report delivered, verdict unaffected (all checks re-runnable; verify18 passes 72/72). (2) sweep #22's delivery carried a failed exec (exit 128) — incidental, report delivered with all numbers re-run.
