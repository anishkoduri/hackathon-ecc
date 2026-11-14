# Audit #58 — fix #18 (pitch-deck-video / 7 video criteria)

- **Verdict: NOT CLEAN — 0 blocking, 1 minor.**
- **Date:** Nov 11, 2026 (evening CST). Auditor's own re-verification throughout; the engine's self-check and `verify18.py` output were not taken on trust (verifiers re-run by the auditor: `fix15/verify15.py` 43/43, `fix17/verify17.py` 59/59, `fix18/verify18.py` 66/66 — all pass on my runs).
- **Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/` vs `fix18/SPEC.md` + `fix18/BASELINE.md`. Staged sources `new-skills/pitch-deck-video/` are byte-identical to the built skill (`diff -r` clean except the staging `commands/` dir placement; `commands/demo.md` staged == built).
- **Builds:** `fix18/build1.log` + `build2.log` both end `build complete`, ERRORS: 0. Manifest hash `4c62aa1af5701af45764438aef7e62e5bbae80c416b5a575c812935760e3b441` re-computed by the auditor (`sha256sum fix18/manifest1-files.txt` = same value; manifest1 == manifest2, diff 0). 2,665 files.
- **Engine edit count verified:** `fix18/fix18.py` SUBS = 14 text subs + JSON_SUBS 6 × 2 seed files + 3 Arch.tsx + 2 qa.mjs + 2 demo.md = **33 staged edits**, as claimed. (All `count==1` anchors per the engine's preflight; the outcomes below were checked independently in the built tree.)

## 1 · SPEC rules F1–F6 — all present where assigned, wording correct

All paths below are under `hackathon-ecc/skills/pitch-deck-video/` unless stated.

### F1 — Feature coverage
- `SKILL.md:75` (step 3): enumerate every must-have from `docs/scope.md` plus every screenshotted route into `shots.json` `features` `[{name, beat}]` + `cuts` `[{name, reason}]`; "shown" = visible on camera AND named; over-cap features go to `cuts` with a reason, "never a silent omission".
- `SKILL.md:138` (arc How): golden path 2–4 beats "PLUS one beat per remaining must-have feature from the `features` array (step 3), drawn from the 12–16 beat budget — the budget's spare beats go to features, not to padding the golden path"; "Never two features in one beat" stays.
- `SKILL.md:196` (step 6): "Coverage table complete — every must-have feature has a beat or a recorded cut… A feature whose beat id is missing from `shots.json` or whose beat produced no footage is a BLOCKING finding."
- `references/shots-reference.md:19–20` (top-level table) + `:36–45` (`features`/`cuts` section, incl. "qa.mjs prints the coverage table… and flags any feature whose beat id is missing… or whose beat produced no footage").
- Seed: `template/shots.example.json:3–14` and `template/shots.json:3–14` — one example `features` entry (`Get the booked week back` → `result`) + one example `cuts` entry with reason.
- `template/scripts/qa.mjs:85–96` — coverage table + missing-beat / no-footage blocking flags; `:112–116` prints table + cuts list.

### F2 — Tech stack
- `SKILL.md:97` (step 4): each arch node gets its `stack` label ("Next.js 15", "GPT-5", "Supabase"), sourced from `package.json` + `docs/decision-record.md` / `docs/scope.md`, "never invented"; arch narration "must name the stack in one spoken phrase"; no-recorded-stack fallback (framework only + gap noted in final report).
- `SKILL.md:139` (arc Proof): "each node labelled with its stack, and the stack named aloud in one phrase."
- `references/shots-reference.md:139` (arch nodes section): optional `stack` field documented; `Arch.tsx` renders it "under each node label in mono"; spoken phrase required.
- `template/src/scenes/Arch.tsx:9` (`stack?: string` in `Node`) and `:31` (mono 15px stack line under the label, `marginTop: 8`).
- Seeds: `template/shots.example.json:96–107` / `template/shots.json:96–107` — Ranker `GPT-5`, Scheduler `Next.js 15`, Writer `GPT-5` (in/out nodes carry no stack, correctly optional); arch `say` line: "What is a model call and what is not. Built on Next.js and GPT-5 — this is the credibility beat."

### F3 — Uniqueness (Edge beat)
- `SKILL.md:137` (arc beat 3, after Wow, before How): "Edge — one beat, one sentence: the one thing no alternative does, in the user's words, with the alternative named or clearly implied ('unlike X, this…'). Shown live where possible — a `focus` on the differentiating element, or the wow footage carrying it. The Edge claim comes from `docs/decision-record.md` / `docs/scope.md`… If none is recorded, ask for one line; never invent a competitor claim — the fallback is stating the wow's distinguishing fact, not a fabricated comparison." How/Proof/Close renumbered to 4/5/6 (`SKILL.md:138–140`); arc minimum is now 7–9 beats.
- Seeds: `template/shots.example.json:126–138` / `template/shots.json:126–138` — `edge` shot (kind `app`) between `result` and `arch`, `say` "The edge: the one thing no alternative does. Name the alternative, then the difference, in one sentence.", with a `focus` action. No new field needed in `shots-reference.md` (SPEC §F3: it is a normal `app` shot) — correctly absent.

### F4 — Visual bar (theme check + gorgeousness QA)
- `SKILL.md:77` (step 3): screenshots pick "the best state per beat… populated data, the prettiest route, the wow at its best. Never put an empty state on camera…".
- `SKILL.md:97` (step 4): record token source in `theme.source`; "the QA step fails the video if the theme is still the seed theme with no recorded source."
- `SKILL.md:198` (step 6): gorgeousness checks (a) no generic seed look, (b) best-looking states / never an empty state, (c) vignette 0 for light apps, "recorded choice either way".
- `SKILL.md:201` (step 6): "Theme pulled, not seeded — the theme check fails the QA if `shots.json` still carries the seed theme with no recorded `theme.source`."
- `template/scripts/qa.mjs:99–102`: `SEED_THEME = { bg: '#0d0a24', accent: '#ffc93c', card: '#161141' }` (matches both seed themes exactly), seed-identical + no `theme.source` → BLOCKING. `:118` prints theme state + source; `:119` prints vignette (default note "0 for light apps").
- `references/shots-reference.md:11`: `theme.source` + `theme.vignette` (0–1, default 0.3, "set 0 for light apps and record the choice either way").

### F5 — A/V match (per-beat blocking + mix)
- `SKILL.md:197` (step 6): per-beat A/V table, completed while reading the sheets, recorded in qa notes; "A 'no' is a BLOCKING finding: re-film or rewrite the line; the video does not ship with an unmatched claim." This replaces the old single-line check (`SKILL.md:182` in the baseline) — the old line is gone (see §3).
- `SKILL.md:200` (step 6): 10-second mix listen from the middle of the video, narration intelligible over the bed, check recorded; `qa.mjs` warns if `music.gain.under` exceeds 0.20.
- `template/scripts/qa.mjs:120`: `under`-gain warning when `> 0.20` (seed 0.14, both seed JSONs). `:121–123`: per-shot A/V table skeleton (`id [kind] "say…" — supports it: ___`) + "A 'no' is BLOCKING" instruction.
- `references/shots-reference.md:273`: "`under` above 0.20 risks burying the voice — `qa.mjs` warns on it, and the step-6 mix check (a 10-second listen from the middle of the video) is the confirmation; keep `under` at or below 0.20 unless the listen says otherwise."
- `template/scripts/qa.mjs:131–137`: the five original stills checks are still printed in order (warnings empty, right page, no spinners/skeletons/empty states, claims match screen, captions legible) with gorgeousness as check 6 and mix as check 7 — old check 4 ("every claim matches what is on screen") now sits under the per-beat blocking table, as SPEC requires.

### F6 — Hard runtime rules + time allocation
- `SKILL.md:101` (step 4): "12–16 beats; the video is under 2:10 (130 seconds) — hard rule… computed from the MEASURED narration durations (`src/vo-durations.json`), plus `gapMs` per beat and the card durations — never from estimates. Over 2:10 is a BLOCKING finding in QA… Absolute max 2:30 (150 seconds), never exceeded — no approval, no exception, no 'one more beat' may push a video past it… Leave ~10 seconds of room. Lengths by artefact: the video is under 2:10; the live demo storyboard is 2–4 min; the pitch storyboard is <90s."
- `SKILL.md:102–114` (step 4): budget-before-lines rule + allocation table (Problem 1 / 8–10; Wow 1–2 / 14–18; Edge 1 / 8–10; How 6–9 / 55–65 LARGEST share; Proof 1–2 / 12–15; Close 1 / 6–8; room ~10) + borrow-across-sections must be recorded in the final report. Table rows match SPEC §F6 exactly.
- `SKILL.md:146` (pacing): "12–16 beats under 2:10, a beat averages 7–9 seconds; a beat whose line runs past ~12 seconds is two ideas and must be split."
- Frontmatter `SKILL.md:6` + `commands/demo.md:3,8`: "under 2:10" (was 1:30–1:50).
- `references/shots-reference.md:14` (`gapMs`): "It counts toward the 2:10 total: measured narration + `gapMs` per beat + card durations + lead/tail — `qa.mjs` prints the total and flags over 2:10 as BLOCKING."
- `template/scripts/qa.mjs:77–80,103–104,111`: total from measured narration + gaps + lead/tail; `> 130` BLOCKING, `> 150` second BLOCKING line (absolute ceiling); total printed with both limits. Runtime math verified against `template/src/timeline.ts:21–22,52` (see §5).

## 2 · Changed-files set — EXACTLY the 7 pitch-deck-video files

`diff fix18/manifest1-files.txt fix17/manifest4-files.txt` (fix17 **final**, build 4) shows exactly 7 changed entries, 2,665 files on both sides, no adds/removes:

| file | fix18 hash (live re-checked, matches) |
| --- | --- |
| `commands/demo.md` | `596c5572…` |
| `skills/pitch-deck-video/SKILL.md` | `5fd1740f…` |
| `skills/pitch-deck-video/references/shots-reference.md` | `b4194884…` |
| `skills/pitch-deck-video/template/scripts/qa.mjs` | `684503dd…` |
| `skills/pitch-deck-video/template/shots.example.json` | `b8e0ed41…` |
| `skills/pitch-deck-video/template/shots.json` | `58b8a5e1…` |
| `skills/pitch-deck-video/template/src/scenes/Arch.tsx` | `6fa61b44…` |

- Note on the trap: diffing against `fix17/manifest1-files.txt` (fix17 **build 1**, pre-fix-up) shows an 8th diff — `skills/motion-patterns/SKILL.md` (`096206b2…` → `061fd1fc…`). That is the fix17 fix-up (fail-safe pointer), already in fix17's final manifest4 (`061fd1fc…`, identical in both manifests) — **not** a fix18 change. Verified by direct grep of both manifest4/manifest1 files.
- Manifest fidelity: all 7 changed files' live `sha256sum` values match `fix18/manifest1-files.txt` exactly. A stratified sample (every 53rd line, 50 files) re-hashed against the live tree: all OK. (A full-tree `sha256sum -c` was started, ran >3 min under the shared-CPU throttle, and was terminated by the auditor as redundant once manifest1==manifest2 hash equality + the 7 live hashes + the 50-file sample were in hand.)

## 3 · Untouched list intact; old time regime gone

- Voice rules: sample check (`SKILL.md`, "Voice-sample check — one line before the batch"), fallback chain (ElevenLabs → Piper → `say`; MiniMax → Piper → `say`; per-line runtime fallback), ask-once key prompt ("ask once, never twice", `SKILL.md:399–426`) — all present, wording unchanged outside the F6 edits.
- Budget governance: "$10 per video" cap (`SKILL.md:575`), "$0.50" approval threshold (`SKILL.md:577`), decision log — intact.
- Local-only filming: "Never set it to a deployed URL, and never film a deployed product" (`SKILL.md:166–168`, `commands/demo.md:10`) — intact.
- Don'ts: stub ban (`SKILL.md:476`), `<Screen />` in `<Sequence>` Don't, hand-tuned-timings Don't, warnings-list Don't — intact.
- Three modes: film (default), montage + explainer (opt-in, ask first) — `SKILL.md` Modes section + `commands/demo.md:22–24,29–30` — intact.
- 12–16 beat count: `SKILL.md:101,138,146` — intact.
- Old regime grep across the whole skill dir (`1:30|1:50|2:00 cap|90–110|90-110`, plus a bare `2:00` grep): **zero hits** in `SKILL.md`, `demo.md`, `shots-reference.md`, and the template. The only "90-second" occurrences are the three deliberate ElevenLabs free-tier quota examples (typical-length figures, not the cap):
  - `SKILL.md:420` — "A 90-second demo narration is about 1,300 characters" (narration-key prompt; brief cited ~:403 — line drift, same sentence).
  - `SKILL.md:529` — same sentence (ElevenLabs section; brief cited ~:512).
  - `references/shots-reference.md:242` — "A 90-second demo is about 1,300 chars, so about 7 demos a month on free" (brief cited ~:225).
  - No other "90-second" anywhere in the skill. Other "90" hits are only `<90s` (pitch storyboard, new F6 artefact distinction), `ms: 900` action examples, and port `5190` — none are old-regime remnants.

## 4 · No regressions

- Grok pins (whole built tree, excl. `node_modules`): `grok-4.7-high` **52 occurrences / 25 files**; `cursor-grok-4.6-high-fast` **100 occurrences** — identical to the fix16 manifest numbers (52 / 100). Untouched.
- Banned terms, per-term tree-wide grep excl. `node_modules`: `claude` 0, `codex` 0, `anthropic` 0, `opus` 0, `sonnet` 0, `haiku` 0, `composer-2.5` 0. (The only "composer" substring hits are `remotion-composer` in `references/openmontage/` docs — not the banned term `composer-2.5`; not re-flagged.)
- Counts: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** (`ls` counts + `hooks.json` has 15 entries) — match the task's expected numbers and fix17's.
- `build.sh`: **23,276 lines, md5 `1a999d763e6ec1fb16985d346b106df0`** — identical to fix17 final; fix18 has no build.sh block (staged-only fix, per SPEC §0).
- Fix15 canonical block verbatim ×11: auditor re-ran `fix15/verify15.py` — **43/43 pass** (includes the canonical-block ×11 checks).
- Fix17 anchors intact (auditor re-grepped, plus re-ran `fix17/verify17.py` — **59/59 pass**): E1 "Push boundaries — be trailblazing" in 4 files; M1/M2 rules in `motion-patterns:55–56` and `motion-foundations:61`; fail-safe note at `motion-patterns:271` points at `useScrollRevealSafe` (the fix17 fix-up, intact); sticker "Scoped exceptions" section `:88`; "Fix #17 static checks" paragraph in 3 files (Taste, orchestrate, orch-build-mvp).
- Adjudicated items not re-flagged (fix16/fix17 manifests): scoped sticker exceptions A/B, `remotion-composer` naming, E1/M1/M2 wording. `fix11/fix11-stage.py` not run.

## 5 · Code correctness of the template changes

### qa.mjs (read in full)
- **Runtime math matches `timeline.ts`.** `timeline.ts:20–22` uses `LEAD = 0.7`, `TAIL = 1.7`, `GAP = vo.gapMs/1000`, `TOTAL = LEAD + Σ(dur + GAP) + TAIL` (via `SCENES.at(-1).start + dur + TAIL`, `:52`; empty case `LEAD + TAIL`). `qa.mjs:77–80` computes `totalSec = 0.7 + Σ(vo.shots: dur + cfg.gapMs/1000) + 1.7`. The two gap sources cannot diverge in practice: `tts.mjs:270,437` writes `vo-durations.json` with `gapMs: cfg.gapMs`, and the seed `vo-durations.json` has `gapMs: 240` = seed `shots.json` `gapMs: 240`. Empty-shots edge case: both give 2.4s. `music.mjs:40` uses the same LEAD + Σ + TAIL formula. ✓
- **Coverage logic** (`qa.mjs:85–96`): missing beat → BLOCKING; `app` beat with a recording but no mark → BLOCKING; `app` beat with no recording yet → "no recording yet" (not blocking — correct for a pre-record QA run); `card` beat → "card — no footage", not blocking (a card renders visibly, so SPEC's "visible on camera AND named" test is satisfiable there; see Obs-3). Missing `features` array entirely → BLOCKING (`:96`). ✓
- **Theme comparison** (`qa.mjs:99–102`): seed triple matches both seed files exactly (`bg #0d0a24`, `accent #ffc93c`, `card #161141`); seed + no `theme.source` → BLOCKING. Auditor simulated the block on the seed `shots.json`: `themeIsSeed: true`, `theme.source: undefined` → correctly BLOCKING (the seed is meant to fail until tokens are pulled). ✓
- **Mix warning** (`qa.mjs:105,120`): warns only when `under > 0.20`; seed 0.14 → no warning. ✓
- **A/V table** (`:121–123`): skeleton printed per shot from `cfg.shots` (`id [kind] "say…" — supports it: ___`) with the blocking instruction. ✓
- **Exit-code path** (`:125–138`): prints `BLOCKING findings (n)` or "No BLOCKING findings…", sets `process.exitCode = 1` iff `blocking.length`. The stills-rendering code above it is untouched. `node --check qa.mjs` passes. ✓

### Arch.tsx (read in full)
- Type-safe: `Node` gains `stack?: string` (`:9`); render is `{n.stack ? <div …>{n.stack}</div> : null}` (`:31`) — no-stack nodes render exactly as before.
- Layout: 5 nodes × 268px + 4 connectors × 52px + 4 flex gaps × 18px = 1,620px < 1,920px canvas; card is `minHeight: 168` (not fixed height), so the added ~23px stack line grows the card instead of overflowing; title (60px) + gap 56 + card (~190px) ≈ 306px < 1,080px. No layout break. ✓
- Stack label is mono (`FONT.mono`, 15px, `letterSpacing: 0.08em`), under the node label, colored with the node's kind tone (`col`) — see Obs-2.

### Seed JSONs
- Both parse as valid JSON (auditor `json.load`); shot ids `hook,setup,result,edge,arch,close` — unique, in order; all have non-empty `say`; `kind` is `app`/`card`; card shots have **no** `do` list (auditor node check: `card-do: 0`, `dup: false` for both files).
- Edge shot valid under `build.mjs` validation (`build.mjs:66–96`): `kind: app`, single action `focus` — `focus` is in `KNOWN_ACTIONS` (`:65–67`); card shots have no `do` list (validator `:87` forbids it); `app.url` present. Both seeds pass every build.mjs check by inspection + the node check above.
- Only intended difference between the two seeds is the `tts` provider (MiniMax/Ukrainian_WiseScholar vs ElevenLabs/Rachel) — same as the baseline note; the dark-purple seed theme is identical in both, so the F4 theme trap applies whichever seed a project starts from, and the QA theme check now catches it.

## Findings

### MINOR-1 — Allocation-table totals line is arithmetically wrong (SPEC's own error, copied verbatim)

- **Evidence:** `SKILL.md:114` — "Totals: 113–126s of content + ~10s room ≈ under 2:10." The table rows (`SKILL.md:104–113`, identical to SPEC §F6) sum to **103–126s**, not 113–126s: min = 8 (Problem) + 14 (Wow) + 8 (Edge) + 55 (How) + 12 (Proof) + 6 (Close) = **103**; max = 10 + 18 + 10 + 65 + 15 + 8 = **126**. Auditor re-added both ends twice. (Plausible origin: 103 + ~10s room = 113 was folded into the content range by mistake.)
- **Impact:** low — the per-section budgets are correct and sum correctly (max 126 + ~10 room ≈ 136 > 130 is the real binding constraint, already handled by the QA block); the totals line is a summary sentence, and an agent following the section budgets will not go wrong. But the shipped skill states a false arithmetic fact.
- **Fix:** one line in `SKILL.md:114` — "Totals: **103–126s** of content + ~10s room ≈ under 2:10"; correct the same line in `fix18/SPEC.md` §F6 for consistency (the SPEC is the source of the error, so this is a SPEC correction carried into the implementation, not an implementation deviation — the built tree matches the SPEC exactly as written).
- **Severity:** minor, non-blocking. No re-audit of other rules needed after the one-line fix (re-grep the totals line only).

## Observations (not counted as findings)

- **Obs-1 — qa.mjs boundary + gap source.** `qa.mjs:103` blocks only when `totalSec > 130`, so a total of exactly 130.0s would pass a rule worded "under 2:10". Measured durations are floats, so exactly 130.0 is effectively unreachable; not counted. `qa.mjs` reads `cfg.gapMs` where `timeline.ts` reads `vo.gapMs` — provably equal in every real run (`tts.mjs:270,437` copies `cfg.gapMs` into `vo-durations.json`), so no divergence.
- **Obs-2 — Arch.tsx stack color.** SPEC F2 says "mono, accent color"; the code renders the stack in the node's kind tone (`col`: `llm` → accent, `code` → accent2, `out` → accent3, `in` → textMuted). The seed's stacked nodes are `llm`/`code`, so they render in accent/accent2. This meets the SPEC's intent (a mono label under the node label, visually tied to the node's accent family); not counted.
- **Obs-3 — Card-mapped features in qa.mjs.** A feature mapped to a `card` beat reports "card — no footage" and is not BLOCKING. Reasonable: a card beat renders visibly on camera, satisfying SPEC F1's "visible on camera AND named" test; `marks.json` only ever records `app` shots, so flagging cards would false-positive every card-mapped feature.
- **Obs-4 — The `motion-patterns` diff is a fix17 artifact, not fix18.** See §2. Anyone diffing fix18 against `fix17/manifest1-files.txt` (build 1) will see 8 diffs; the correct baseline is `fix17/manifest4-files.txt` (final, build 4), which gives exactly the 7 fix18 files.
- **Obs-5 — `composer` substring.** The 2 "composer" hits under `pitch-deck-video/references/openmontage/` are `remotion-composer`, not the banned term `composer-2.5` (0 hits tree-wide). Not re-flagged.

## What the coordinator must do before closing

1. Fix MINOR-1: `SKILL.md:114` totals line 113 → 103 (and the same line in `fix18/SPEC.md` §F6). Rebuild twice, re-diff, re-grep the totals line.
2. Nothing else is open: no blocking findings, no regressions, no missing SPEC rule, no code defect in the template changes.
