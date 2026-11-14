# Audit #59 — fix #18 re-audit (after the fix-up round)

- **Verdict: CLEAN — 0 blocking, 0 minor.**
- **Date:** Nov 11, 2026 (evening CST). Re-audit after audit #58 (0 blocking, 1 minor: MINOR-1) and sweep #21 (5 stale cross-references). Both were addressed in one fix-up round driven by `fix18/fix18_fixup.py` (9 subs, read in full by the auditor).
- **Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/` vs `fix18/SPEC.md` (§F6 totals line corrected to 103–126s) + the standing rules. The auditor re-grepped and re-read every item below; `verify18.py` / the fix-up engine's self-checks were not taken on trust (verifiers re-run by the auditor: §5).
- **Builds:** `fix18/build3.log` + `fix18/build4.log` both end `build complete`, `ERRORS: 0` (`:901` in both). Manifest hash re-computed by the auditor: `sha256sum fix18/manifest4-files.txt` = `ea1c12e3c25e77c1b9186664a42c74ab6ec9b1ce9444253bb1c9e5f16e735429` — matches the claimed hash and `fix18/manifest4.txt` contents; `manifest3-files.txt` hashes to the same value (builds 3+4 diff 0). 2,665 files.
- **Staged vs built:** `diff -r new-skills/pitch-deck-video/ hackathon-ecc/skills/pitch-deck-video/` → only output `Only in new-skills/pitch-deck-video/: commands` (the known structural path difference; `commands/demo.md` staged == built). No file content differs.

## 1 · MINOR-1 fixed — allocation totals line reads "103–126s"

- `hackathon-ecc/skills/pitch-deck-video/SKILL.md:114`: "Totals: **103–126s** of content + ~10s room ≈ under 2:10."
- `fix18/SPEC.md:291` (§F6): same corrected line, "Totals: 103–126s of content + ~10s room ≈ under 2:10."
- **Recomputed by the auditor from the table rows** (`SKILL.md:104–113`, identical to SPEC §F6): min = 8 (Problem) + 14 (Wow) + 8 (Edge) + 55 (How) + 12 (Proof) + 6 (Close) = **103**; max = 10 + 18 + 10 + 65 + 15 + 8 = **126**. Correct. (See Obs-2 for the max+room arithmetic.)

## 2 · Sweep #21 cross-references fixed — "1:30–1:50" is 0 tree-wide

Tree-wide grep (`--exclude-dir=node_modules`, en dash AND hyphen forms) across the built tree **and** the staged sources (`new-skills/`, `new-rules/`, `rewritten-skills/`): **0 hits** for `1:30–1:50` and `1:30-1:50`. `build.sh` itself: 0 hits. `2:00 cap`, `90–110`, `90-110`: 0 hits tree-wide.

All five sweep-#21 sites now state the new regime (auditor-read, exact lines):

| Site | Line | Text (verified) |
| --- | --- | --- |
| `rules/hackathon-mode.mdc` | :48 | "Demo lengths (canonical — this is the one place that says which length governs what): the live demo storyboard is 2–4 min; the demo video is under 2:10 (hard rule; absolute max 2:30); the pitch storyboard is under 90s. Where another skill states a different length, this statement governs." — still claims governance, now consistent with what it governs. |
| `skills/hackathon-scope/SKILL.md` | :17 | "Which length governs what: the live demo storyboard is 2–4 min; the demo video is under 2:10 (hard rule; absolute max 2:30); the pitch storyboard is under 90 seconds." |
| `skills/hackathon-pitch/SKILL.md` | :32 | "This is the pitch storyboard (under 90s) — not the live demo storyboard (2–4 min) and not the demo video (under 2:10, pitch-deck-video / /demo). Demo lengths are canonical in hackathon-mode §6: the live demo storyboard is 2–4 min; the demo video is under 2:10 (hard rule; absolute max 2:30); the pitch storyboard is under 90s. Where another skill states a different length, the hackathon-mode statement governs." |
| `skills/hackathon-pitch/assets/pitch-script-template.md` | :79 | "- Video (demo video, under 2:10), recorded after the final deploy: [path or link, not a local file only]" |
| `README.md` | :44 | "- `/demo` — generate a narrated product demo video, under 2:10, of the app" |

- **Pitch line-32 coherence (checked, not just grepped):** the canonical tail ("Demo lengths are canonical in hackathon-mode §6: … Where another skill states a different length, the hackathon-mode statement governs.") and the feature-removal tail ("After a feature removal (`orch-change-feature` step 5), refresh the pitch narrative, scripts, and this storyboard …") are both present, as two distinct sentences with no duplicated clause. The line reads coherently end to end.
- **Non-findings, for the record:** `skills/hackathon-scope/SKILL.md:24–25` still contains `1:30` — as `(0:30-1:30)` and `(1:30-2:30)` minute markers inside the 2–4 min **live demo** storyboard outline, not the video length. Not an old-regime remnant. The three deliberate 90-second voice-quota examples (audit #58 §3) are unchanged.

## 3 · Arch.tsx stack label now uses the accent color literally (SPEC F2)

- `skills/pitch-deck-video/template/src/scenes/Arch.tsx:41`: `{n.stack ? <div style={{ fontFamily: FONT.mono, fontSize: 15, letterSpacing: '0.08em', color: C.accent, marginTop: 8 }}>{n.stack}</div> : null}` — `color: C.accent` literally, mono, under the node label. Audit #58 Obs-2 (kind-tone color) is closed; the fix-up sub replaced `color: col` with `color: C.accent` (fixup sub #2 in `fix18_fixup.py`).
- `Arch.tsx:10`: `stack?: string` in `Node` — unchanged. `col` (`:17`) is still used for the kind label (`:37`), which is the correct remaining use.
- Seed JSONs unchanged from audit #58 (hashes identical): stack labels Ranker `GPT-5`, Scheduler `Next.js 15`, Writer `GPT-5`; arch `say` names the stack aloud.

## 4 · Changed-files set vs fix17 final manifest — exactly the fix18 files

`diff fix17/manifest4-files.txt fix18/manifest4-files.txt`: **exactly 12 changed entries, 2,665 files on both sides, no adds/removes** — the original 7 pitch-deck-video files + the 5 fix-up files, nothing else:

| File | fix18/manifest4 hash (live re-checked) |
| --- | --- |
| `commands/demo.md` | `596c5572…` (unchanged from audit #58) |
| `skills/pitch-deck-video/SKILL.md` | `567fcded…` (was `5fd1740f…` — MINOR-1 totals line) |
| `skills/pitch-deck-video/references/shots-reference.md` | `b4194884…` (unchanged) |
| `skills/pitch-deck-video/template/scripts/qa.mjs` | `684503dd…` (unchanged) |
| `skills/pitch-deck-video/template/shots.example.json` | `b8e0ed41…` (unchanged) |
| `skills/pitch-deck-video/template/shots.json` | `58b8a5e1…` (unchanged) |
| `skills/pitch-deck-video/template/src/scenes/Arch.tsx` | `5f764874…` (was `6fa61b44…` — accent-color fix) |
| `README.md` | `d66294e2…` (fix-up) |
| `rules/hackathon-mode.mdc` | `3330964c…` (fix-up) |
| `skills/hackathon-pitch/SKILL.md` | `52253bab…` (fix-up) |
| `skills/hackathon-pitch/assets/pitch-script-template.md` | `91aa6251…` (fix-up) |
| `skills/hackathon-scope/SKILL.md` | `038a0ce9…` (fix-up) |

- The two changed hashes among the original 7 are exactly the two files the fix-up touched (SKILL.md totals line, Arch.tsx accent); the other five original-7 hashes are byte-identical to audit #58. No other file changed anywhere in the 2,665-file tree.
- **Note on `build.sh` md5:** `5cdd22787dfd56aed0b360e49dae60f2` (23,276 lines) vs audit #58's `1a999d763e6ec1fb16985d346b106df0`. The md5 moved because the fix-up edited build.sh's README heredoc and the Fix-4 / Gap-39 patches (fixup subs 2c, 2d, 2e, 2f, 2g — read in the engine, `fix18/fix18_fixup.py:36–77`, 9 subs total as claimed); the line count is unchanged at 23,276 and the engine's own self-check asserts exactly this. Not a regression.

## 5 · Re-verification on the new built tree

### F1–F6 — all present, wording correct (re-grepped on the new tree)

- **F1:** `SKILL.md:75` (step 3, `features [{name, beat}]` + `cuts [{name, reason}]` enumeration), `:138` (How grows by one beat per remaining must-have; "Never two features in one beat" stays), `:196` (step 6, coverage line + BLOCKING on missing beat / no footage). `shots-reference.md:19–20,36–45`; seeds `shots.example.json:3–14` / `shots.json:3–14` (one example entry each); `qa.mjs:85–96,112–116` (coverage table + flags).
- **F2:** `SKILL.md:97` (step 4, stack label from `package.json` + decision-record/scope, never invented; one spoken phrase; no-recorded-stack fallback), `:139` (arc Proof). `shots-reference.md:139`; `Arch.tsx:10,41` (§3); seeds stack-labelled + arch `say` "Built on Next.js and GPT-5 — this is the credibility beat."
- **F3:** `SKILL.md:137` (Edge beat 3, after Wow, before How; one sentence, alternative named/implied, never invent a competitor claim); How/Proof/Close renumbered 4/5/6 (`:138–140`); arc minimum 7–9. Edge shot in both seeds.
- **F4:** `SKILL.md:77` (step 3, best state per beat), `:97` (theme.source record), `:198` (gorgeousness checks a/b/c), `:201` (theme check fails QA on seed theme with no source). `qa.mjs:99–102` (SEED_THEME triple `#0d0a24`/`#ffc93c`/`#161141`, seed + no source → BLOCKING), `:118–119` (theme/vignette print). `shots-reference.md:11` (theme.source + vignette).
- **F5:** `SKILL.md:197` (per-beat A/V table, "no" is BLOCKING), `:200` (10-second mix listen; `qa.mjs` warns if `music.gain.under` > 0.20). `qa.mjs:105,120` (under-gain warning), `:121–123` (per-shot A/V skeleton + blocking instruction). `shots-reference.md:273` (gain guidance). Stills checks intact (`qa.mjs:131–137`).
- **F6:** `SKILL.md:101` ("12–16 beats; the video is under 2:10 (130 seconds) — hard rule… Absolute max 2:30 (150 seconds), never exceeded… Leave ~10 seconds of room"), `:102` ("Write the time budget before writing the lines."), `:103–114` (allocation table + corrected totals line, §1), `:146` (pacing, ~12s split rule). Frontmatter `:6` + `commands/demo.md:3,8` ("under 2:10"). `qa.mjs:77–80,103–104,111` (total from measured narration + gaps + lead/tail; `> 130` BLOCKING, `> 150` second BLOCKING line). `shots-reference.md:14` (gapMs counts toward the 2:10 total).

### Untouched list — intact on the new tree

- Voice rules: sample check (`SKILL.md:389`), fallback chain (`:522`), ask-once key prompt (`:410,426` — "ask once, never twice").
- Budget governance: "$10 per video" cap (`:575`), "$0.50" approval threshold (`:577`), decision log.
- Local-only filming: "Never set it to a deployed URL, and never film a deployed product" (`:167–168`, `commands/demo.md:10`).
- Don'ts: stub ban (`:476`), `<Screen />` in `<Sequence>` Don't, hand-tuned-timings Don't, warnings-list Don't.
- Three modes: film default, montage + explainer opt-in (`SKILL.md:483–486` Modes section).
- 12–16 beat count: `SKILL.md:101,138,146`.

### No regressions

- Grok pins (whole built tree, excl. `node_modules`): `grok-4.7-high` **52 occurrences / 45 lines**; `cursor-grok-4.6-high-fast` **100 occurrences / 99 lines** — identical to fix16 manifest. Untouched.
- Banned terms, per-term tree-wide grep excl. `node_modules` (`skills agents commands rules hooks README.md`): `claude` 0, `codex` 0, `anthropic` 0, `opus` 0, `sonnet` 0, `haiku` 0, `composer-2.5` 0.
- Counts: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** — match fix17 final.
- `build.sh`: **23,276 lines, md5 `5cdd22787dfd56aed0b360e49dae60f2`** (md5 moved only via the fix-up's build.sh edits, §4 note; lines unchanged).
- Fix15 canonical block verbatim ×11: auditor re-derived from `fix15/fix15.py` against all 11 files — count 1 in each, all pass.
- Fix17 anchors intact (auditor re-grepped): E1 "Push boundaries" ×1 in each of the 4 files (design-taste-frontend, orchestrate, orch-build-mvp, ui-ux-pro-max); sticker "Scoped exceptions" section at `sticker.md:88` with motion line `:74` pointing at it; fail-safe note at `motion-patterns:271` (`useScrollRevealSafe`, 1 hit); "Fix #17 static checks" paragraph in 3 files (per verify17).
- **Verifiers re-run by the auditor on the new tree:** `fix18/verify18.py` **72/72 pass** (includes verify15 43/43 and verify17 59/59 in its output); `fix15/verify15.py` **43/43 pass**; `fix17/verify17.py` **59/59 pass** — all exit 0.
- Adjudicated items not re-flagged (fix16/fix17 manifests): scoped sticker exceptions A/B, `remotion-composer` naming, E1/M1/M2 wording. `fix11/fix11-stage.py` not run.

## Findings

**None.** 0 blocking, 0 minor. MINOR-1 and both sweep-#21 items are confirmed fixed in the built tree, with no other file changed and no regression in any re-verified rule.

## Observations (not counted as findings)

- **Obs-1 — qa.mjs exactly-130.0s boundary (adjudicated, audit #58).** `qa.mjs:103` blocks only when `totalSec > 130`, so a total of exactly 130.0s would pass a rule worded "under 2:10". SPEC enforcement is "over 2:10"; measured durations are floats, so exactly 130.0 is a measure-zero edge. Not counted, per the task's adjudication.
- **Obs-2 — Max allocation + room exceeds the hard rule (already noted in audit #58).** Table max 126s + ~10s room ≈ 136s > 130s hard rule. This is not new and not a defect in the fix-up: the per-section bands are correct, and the QA block (`qa.mjs:103`, `> 130` BLOCKING) is the binding constraint that forces a re-cut when a storyboard actually lands there. The dry-run #29 trace landed at 118.6s with 11.36s room, inside the rule.
- **Obs-3 — `build.sh` md5 moved, lines did not (§4).** Expected consequence of the fix-up's five build.sh subs; the engine asserts the line count (23,276) and the absence of `1:30–1:50` in build.sh, and the auditor re-confirmed both independently.
