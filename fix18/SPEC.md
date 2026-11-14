# Fix program #18 — SPEC (analysis phase)

**Status:** ANALYSIS ONLY — Nov 11, 2026. No staged source or `build.sh`
touched. Implementation is a separate, fresh coordinator spawn (do not
expect this analysis agent to be resumed).

**Ask (Anish, Nov 11):** check the video demo creation skill
(`pitch-deck-video`, the `/demo` skill) so a demo video will actually be
good: it must include all the features of the program, actually show
functionality, address the problem, name the tech stack, say what makes
the product unique, be above all visually gorgeous, and have voice/audio
matching what the visuals show. Seven criteria, in that order.
**Follow-up (Anish, Nov 11, ~16:41 CST):** hard rules — the video is
under 2:10, absolute max 2:30 — and add time allocation so the important
parts get the time they deserve. Recorded as F6 below.

## 0 · Sequencing gate — read before implementing

- Fix #16 (Grok-only re-pin + Claude/Codex scrub) is RUNNING and fix #17's
  implementation is queued after it. **Do NOT touch any plugin file until
  BOTH are closed.** Verify: `~/workspace/hackathon-plugin/fix16/MANIFEST.md`
  AND `fix17/MANIFEST.md` both exist, AND `build.sh`'s md5 matches the
  latest of those two manifests.
- State at analysis time (Nov 11, ~16:40 CST): fix16 has no MANIFEST.md
  (only `INVENTORY.md`, `fix16.py`); fix17 has analysis only
  (`INVENTORY-V4.md`, `PARENT-GUIDANCE.md`, `SKILL-MAP.md`,
  `SPEC-DRAFT.md`). `build.sh` is 23,213 lines, md5
  `42dd82b46545da9650a1f4f4cb52aba0`.
- Staged sources for this skill: `~/workspace/hackathon-plugin/new-skills/pitch-deck-video/`
  (`SKILL.md`, `references/shots-reference.md`, `template/`).
  `build.sh:222–226` copies it verbatim into the built tree
  (`skills/pitch-deck-video/` + `commands/demo.md`) — **no runtime
  patches exist for this skill**, so every change is a staged-source
  edit; staged `SKILL.md` is byte-identical to the built-tree copy
  (verified by `diff -q` during analysis).
- The `template/` directory is runtime code for the video project (Remotion
  + scripts), not just docs: changes to `template/scripts/qa.mjs`,
  `template/src/scenes/Arch.tsx`, or `template/shots.example.json` are
  real code changes — re-verify them in the audit like any other code,
  and keep the template rendering from its seed before the first
  recording (the skill's own invariant).

## 1 · Verified findings (each read from the files, not assumed)

### Strengths — all confirmed, must stay intact

- **S1 Shows functionality.** Film mode drives the real app live with
  Playwright (clicks, types, waits for real results) — `SKILL.md` step 5
  and `references/shots-reference.md` actions table. Don't:
  `SKILL.md:459` "Don't film anything stubbed. If a button returns
  'connect the backend', leave it out…".
- **S2 Addresses the problem.** Narration rule `SKILL.md:104`: "Open on
  the problem in the user's words, before the product name exists." Arc
  beat 1 (`SKILL.md:118–120`) is Problem, one beat, "The pain, not the
  category."
- **S3 A/V sync is architected in.** `template/src/timeline.ts:9–11`:
  "Scene lengths come from the measured audio; the footage is stretched
  to fit it; the camera moves come from element boxes measured during the
  recording." Don't: `SKILL.md:451` "Don't put `<Screen />` inside a
  `<Sequence>`" (the documented sync bug: footage subtly out of sync
  with the voice).
- **S4 QA asks whether each caption lands on a supporting frame.**
  `SKILL.md:170–186` step 6: warnings empty, "does each caption land on
  a frame that supports it? Any blank or white frames? Is small text
  legible, or does it need a `focus`?" `template/scripts/qa.mjs`
  prints the same five checks (warnings empty, failures empty, shot on
  the right page, no spinners/skeletons/empty states, claims match
  screen, captions legible).

### Gaps — all confirmed (no finding in the brief failed verification)

- **G1 All features — NOT covered.** The arc (`SKILL.md:118–131`) is
  Problem 1 + Wow 1 + How 2–4 + Proof 1 + Close 1: the wow plus ONE
  golden-path task. "Never two features in one beat" (`SKILL.md:125`)
  is a constraint, not a coverage rule, and nothing enumerates the full
  feature list or verifies every feature appears. `grep feature` across
  the skill finds only lines 125 and 203 ("A feature was rewritten").
  The template seed has only 5 beats (hook/setup/result/arch/close —
  `template/shots.example.json`, `shots` array). A video from this skill
  shows the wow + one task, not the whole program.
  - Refinement found in verification: the arc's minimum is 6 beats but
    the beat budget is 12–16 (`SKILL.md:100`, `:135`), so 4–10 beats are
    currently unspecified — in practice they pad the golden path. F1
    directs those beats at the remaining features instead.
  - Feature source exists and is citable: `docs/scope.md` holds the
    must-have/cut lists (`rewritten-skills/hackathon-scope/SKILL.md:9,43`),
    and step 3 (`SKILL.md:63`) already reads `docs/scope.md` +
    `docs/decision-record.md` and screenshots every route.
- **G2 Tech stack — never named.** The arch card beat is only "which
  boxes are model calls and which are deterministic code"
  (`SKILL.md:92–96`, `:126–128`). The seed arch line is "What is a model
  call and what is not. This is the credibility beat."
  (`template/shots.example.json`, arch shot). `template/src/scenes/Arch.tsx`
  renders each node as `{label, note, kind}` only (`kind` → model/code/
  input/output labels) — there is no stack field anywhere. Zero
  occurrences of "stack" in `SKILL.md`, `shots-reference.md`, or
  `shots.example.json` (verified by grep).
- **G3 Uniqueness — no beat for it.** No beat requires saying what makes
  this different from the alternative. The wow (`SKILL.md:120–121`) is
  "the product doing the impossible thing, live" — not differentiation.
  Zero occurrences of "unique" (except shot-id uniqueness,
  `shots-reference.md:26`), "competitor", or "differentiation" in the
  skill; "different"/"alternative" hits are all unrelated (a different
  wow, a different artefact, cheaper alternatives = cost alternatives).
- **G4 Visually gorgeous — no aesthetic bar.** QA is functional only
  (S4 above). Pulling theme colors/fonts from the app's own design tokens
  is an instruction, not a check: `SKILL.md:92–94` "Pull the
  `theme.colors` from the app's own design tokens so the cards and the
  footage read as one piece." `template/src/theme.ts` reads colors/fonts
  from `shots.json`, and the seed theme in `shots.example.json` is the
  fixed dark-purple set (`bg #0d0a24`, `accent #ffc93c`, Hanken Grotesk /
  Instrument Serif / JetBrains Mono) — if the agent skips the pull, the
  video ships that seed and looks generic. Nothing requires the footage
  to show the app's best-looking states: step 3 screenshots every route
  only to verify the scoped wow, not to pick best states.
  - Refinement: a second seed-default trap — `template/src/timeline.ts`
    sets `VIGNETTE` default 0.3 ("Darkens the frame edges. Reads well on
    a dark app, heavy on a light one — set theme.vignette to 0 to turn it
    off"). A light app filmed with the default vignette looks heavy.
- **G5 A/V match — manual check, no enforcement; no audio-mix check.**
  The caption-frame match is a read-the-sheets check (`SKILL.md:182`,
  `qa.mjs` check 4 "every claim in the narration matches what is on
  screen") with no enforcement — nothing blocks shipping on a mismatch.
  Music mix is gain numbers only: `shots-reference.md` music block
  (`gain: {open, under, close}`, seed 0.34 / 0.14 / 0.30) applied by
  `template/src/Video.tsx:71–88` via an interpolate; there is no
  loudness measurement and no listen-check anywhere in the pipeline
  (`qa.mjs` is stills-only).

## 2 · Baseline — what a current /demo run produces (7 criteria)

| # | Criterion | Today | Evidence |
| --- | --- | --- | --- |
| 1 | Shows functionality (real app, live) | YES | S1 |
| 2 | Addresses the problem (in the user's words) | YES | S2 |
| 3 | Includes ALL features of the program | NO | G1 — wow + one golden-path task only |
| 4 | Names the tech stack | NO | G2 — arch beat is model-vs-code only |
| 5 | States what makes it unique | NO | G3 — no differentiation beat |
| 6 | Visually gorgeous (above all) | NOT GUARANTEED | G4 — theme pull is an instruction, QA is functional-only, seed theme ships if skipped |
| 7 | Voice/audio matches the visuals | PARTIAL | S3 + G5 — sync is architected; caption-frame match is manual/unenforced; no mix check |

## 3 · Rules (F1–F5)

### F1 — Feature coverage: every must-have feature is shown or explicitly cut

- **Step 3 addition (before storyboarding).** Enumerate the feature
  list from `docs/scope.md`'s must-have list plus every route
  screenshotted in step 3 (a route with no must-have feature behind it
  is not a feature). Write the list into `shots.json` as a `features`
  array — `[{name, beat}]`, one entry per must-have feature, `beat`
  being the shot id that shows it — and a `cuts` array —
  `[{name, reason}]` for any must-have feature deliberately left out of
  the video.
- **Arc change.** How grows: golden-path beats (2–4, unchanged) PLUS
  one beat per remaining must-have feature, drawn from the 12–16 beat
  budget. "Never two features in one beat" (`SKILL.md:125`) STAYS — the
  fix is that the budget's spare beats go to features, not to padding
  the golden path. A feature is "shown" only if it is visible on camera
  AND named (narration or on-screen caption) in its beat.
- **Cap governs.** The F6 hard cap (under 2:10; see F6) governs:
  if the feature count would push the video past it, the agent cuts the
  least important features into the `cuts` array with a reason, and says
  so in the final report. A feature cut from the video is a reported
  decision, never a silent omission.
- **QA enforcement.** `qa.mjs` prints a coverage table (feature →
  beat, plus the cuts list) and flags any feature whose beat id is
  missing from `shots.json` or whose beat produced no footage. The
  skill's step-6 QA list gains the coverage line: "coverage table
  complete — every must-have feature has a beat or a recorded cut."
- **Files:** `SKILL.md` step 3 + arc + step 6; `shots-reference.md`
  (document `features` / `cuts`); `shots.example.json` (seed arrays,
  with one example entry each); `template/scripts/qa.mjs` (coverage
  table + missing-beat flag).

### F2 — Tech stack: arch nodes carry their stack label; one spoken line names it

- **Node field.** `cards.arch.nodes[]` gains an optional `stack` label
  (e.g. `"Next.js 15"`, `"GPT-5"`, `"Supabase"`) — the concrete
  framework / model / service / infra that box runs on, not a category.
  `template/src/scenes/Arch.tsx` renders the stack label under each
  node label (mono, accent color). `shots-reference.md` documents the
  field; the seed example shows stack labels on its nodes.
- **Spoken line.** The arch beat's narration must name the stack in one
  spoken phrase ("Built on Next.js, GPT-5, and Supabase") — one phrase,
  not a list read aloud (the "Never list" narration rule stays).
- **Source of truth.** The stack comes from the app's `package.json` +
  `docs/decision-record.md` / `docs/scope.md` (the integration skill
  names the API there) — never invented. If the app has no recorded
  stack, the arch beat says the framework only and notes the gap in the
  final report.
- **Files:** `SKILL.md` step 4 (arch paragraph); `shots-reference.md`
  (arch node field); `template/src/scenes/Arch.tsx` (render `stack`);
  `template/shots.example.json` (seed nodes + seed arch line).

### F3 — Uniqueness: a dedicated Edge beat after the wow

- **New arc beat, position 3 (after Wow, before How).** "Edge" — one
  beat, one sentence, the one thing no alternative does, in the user's
  words, with the alternative named or clearly implied ("unlike X,
  this…"). Shown live where possible (a `focus` on the differentiating
  element, or the wow footage carrying it). The arc becomes Problem 1 +
  Wow 1 + Edge 1 + How 2–4 + Proof 1 + Close 1 (7–9 beats minimum).
- **Source of truth.** The Edge claim comes from `docs/decision-record.md`
  / `docs/scope.md` (the wow test: "does this make a judge stop and
  stare?") or from the user. If none is recorded, the agent asks for one
  line; it never invents a competitor claim — the fallback is stating
  the wow's distinguishing fact, not a fabricated comparison.
- **Files:** `SKILL.md` arc (new beat 3, renumber How/Proof/Close);
  `shots-reference.md` if the beat needs a field (it does not — it is a
  normal `app`/`card` shot); seed example gains an Edge shot between
  the wow and the How beats.

### F4 — Visual bar: theme pull is a check; gorgeousness is QA'd

- **Theme check (enforced).** `qa.mjs` compares the project's
  `shots.json` theme against the seed theme (`shots.example.json`:
  `bg #0d0a24`, `accent #ffc93c`) and fails the QA if the theme is
  identical to the seed without a recorded reason. The agent must record
  the app's token source (file + values) in the video project; a
  deliberate "seed theme kept" needs the app-token citation showing the
  app's tokens genuinely match it.
- **Gorgeousness QA.** Step 6 gains three explicit checks, read off the
  contact sheets: (a) no generic seed look — cards read as the app's own
  palette/fonts, not the seed's; (b) footage shows the app's
  best-looking states — populated data, the prettiest route, the wow at
  its best, chosen from the step-3 screenshots; never an empty state on
  camera; (c) vignette matches the app — `theme.vignette` 0 for light
  apps, recorded choice either way.
- **Step 3 addition.** Screenshots are used to pick the best state per
  beat, not only to verify the wow: for each beat, the shot's state is
  the best-looking state that shows the claim (populated, visually rich).
  The existing Don't stays: never describe a screen as full when this
  account's version of it is empty.
- **Files:** `SKILL.md` step 3 + step 6; `template/scripts/qa.mjs`
  (theme comparison + the three gorgeousness checks printed in the QA
  read); `shots-reference.md` (theme + vignette fields).

### F5 — A/V match: per-beat check enforced; music mix checked

- **Per-beat A/V table (blocking).** `qa.mjs` prints a per-shot table —
  shot id → the claim in its `say` line → stills support it (yes/no) —
  and the agent completes it while reading the contact sheets. The
  completed table is recorded in the video project (qa notes) and a
  "no" is a BLOCKING finding: re-film or rewrite the line; the video
  does not ship with an unmatched claim. This replaces the current
  single-line manual check (`SKILL.md:182`) with the same check made
  per-beat and blocking.
- **Audio-mix check.** After render, listen to a 10-second sample from
  the middle of the video (where the music is `under` the voice) and
  confirm the narration is intelligible over the bed; record the check.
  Script guard: `qa.mjs` (or `build.mjs`) warns if
  `music.gain.under` exceeds 0.20 — the seed is 0.14, and above 0.20 the
  bed risks burying the voice.
- **Files:** `SKILL.md` step 6; `template/scripts/qa.mjs` (per-shot
  table skeleton + `under`-gain warning); `shots-reference.md` (music
  gain guidance).

### F6 — Hard runtime rules + time allocation (Anish, Nov 11)

This REPLACES the skill's current time regime (`SKILL.md:100`:
1:30–1:50 total, under a 2:00 cap, leave 10 seconds of room).

- **Hard rule: the video is under 2:10 (130 seconds).** The total is
  computed from the MEASURED narration durations (`src/vo-durations.json`,
  the same derivation the edit already uses), plus `gapMs` per beat and
  the card durations — never from estimates. `qa.mjs` prints the total
  and a total over 2:10 is a BLOCKING finding: re-cut (shorten lines,
  drop a low-priority feature beat into the `cuts` array per F1, tighten
  a beat) — the video does not ship over 2:10.
- **Absolute max 2:30 (150 seconds), never exceeded.** No approval,
  no exception, no "one more beat" may push a video past 2:30. If a
  storyboard would exceed 2:30 even after cutting, the storyboard is
  re-cut (fewer features, shorter lines), never extended. The 2:10
  hard rule is the working limit; 2:30 is the ceiling that no version
  of the video may cross.
- **Time allocation — the important parts get the time they deserve.**
  The 130-second budget is divided across the arc by importance, not
  evenly. The allocation table below is the default the storyboard must
  follow (times are narration + gaps for that section, in seconds):

  | Section | Beats | Seconds | Why |
  | --- | --- | --- | --- |
  | Problem | 1 | 8–10 | The pain, in the user's words — short, sharp |
  | Wow | 1–2 | 14–18 | The opening, the reason to keep watching — deserves time |
  | Edge (uniqueness) | 1 | 8–10 | One sentence, the differentiator |
  | How / features | 6–9 | 55–65 | The LARGEST share — every feature shown, the program proved |
  | Proof (arch + stack) | 1–2 | 12–15 | Credibility beat, stack named aloud |
  | Close | 1 | 6–8 | One sentence left on screen |
  | Unallocated room | — | ~10 | The existing leave-room rule, kept |

  Totals: 103–126s of content + ~10s room ≈ under 2:10. The
  features' share is the largest because F1 spends the spare beats
  there. A beat that runs past ~12 seconds is two ideas and must be
  split (existing rule, `SKILL.md:135`) — the allocation table is
  enforced per section, not per beat.
- **Where the time comes from.** The allocation is written into the
  storyboard step (step 4): before writing `shots.json`, the agent
  writes the section budget first, then writes lines to fit it — never
  the reverse (writing lines and discovering the total afterwards). If
  a section's lines would exceed its budget, shorten the lines or move
  a feature to `cuts` (F1); do not borrow from another section's
  budget without recording it in the final report.
- **Files:** `SKILL.md` (caps paragraph + allocation table in step 4);
  `template/scripts/qa.mjs` (total-runtime print + blocking check over
  2:10, ceiling note at 2:30); `shots-reference.md` (total/gapMs note).

## 4 · What stays untouched

Functionality (live Playwright filming, stub ban), problem-first opening,
measured-narration derivation and the `<Screen />` Don't, voice rules
(sample check + fallback chain + ask-once key prompt), budget governance
($10 cap, $0.50 approval threshold, decision log), local-only filming
(never a deployed URL), the remaining Don'ts, and the three modes (film
default; montage/explainer opt-in). The 12–16 beat count stays; the time
cap is replaced by F6 (under 2:10 hard, absolute max 2:30). F1/F3 spend
the existing budget, they do not extend it.

## 5 · Verification plan for the implementation coordinator

1. Apply this SPEC to the staged sources listed in §3; rebuild with
   `bash ~/workspace/hackathon-plugin/build.sh` TWICE — both exit 0,
   diff 0.
2. Audit + dry-run + sweep until clean (bar: the latest clean numbers at
   the time — read `fix16/MANIFEST.md` and `fix17/MANIFEST.md`).
3. Storyboard re-trace (the functional proof): take a real recorded scope
   with a must-have list — the Home Run app from the Nov 11 smoke test
   is the standing example — and trace a `/demo` storyboard under the new
   rules. Verify all 7 criteria from §2: coverage table complete (or
   cuts recorded with reasons), stack named in arch nodes + spoken line,
   Edge beat present, theme pulled from the app's tokens (not the seed),
   per-beat A/V table complete, mix check recorded. Verify F6 too: the
   traced storyboard's total (from measured line lengths) is under 2:10
   with the allocation table followed (features 55–65s, the largest
   share). A re-trace is a dry-run, not a full render (a full render needs the app running and
   a voice key); the trace checks the storyboard + `shots.json` + QA
   outputs, which is where all five gaps live.
4. Write `fix18/MANIFEST.md`: verified gap list, every rule changed
   (file:line), build.sh lines + md5, audit/dry-run/sweep numbers, and
   the re-trace result against the 7 criteria.

## 6 · Files to change (staged sources)

- `new-skills/pitch-deck-video/SKILL.md` — step 3, step 4 (theme +
  arch), arc (Edge beat + How growth), step 6 (coverage, gorgeousness,
  per-beat A/V, mix check).
- `new-skills/pitch-deck-video/references/shots-reference.md` —
  `features`/`cuts` fields, arch node `stack`, theme/vignette, music
  gain guidance.
- `new-skills/pitch-deck-video/template/shots.example.json` — seed
  `features`/`cuts`, stack-labelled arch nodes, Edge shot, seed arch
  line naming the stack.
- `new-skills/pitch-deck-video/template/src/scenes/Arch.tsx` — render
  the `stack` label.
- `new-skills/pitch-deck-video/template/scripts/qa.mjs` — coverage table
  + missing-beat flag, theme-vs-seed comparison, per-shot A/V table
  skeleton, `under`-gain warning, total-runtime print + blocking check
  over 2:10 (F6).
- `new-skills/pitch-deck-video/commands/demo.md` — only if the arc
  change needs a wording touch (it should not: the command defers to
  the skill).

## 7 · Out of scope / do-not-touch

- No commit, no git bundle, no GitHub touch, no Campus Eats artifact
  touch. No new inventory (no new skills, commands, or modes).
- Do not weaken the 12–16 beat count, the F6 time rules, the voice rules, the
  budget governance, or the local-only filming rule. Do not re-flag
  adjudicated items; never re-run `fix11/fix11-stage.py`.
- Fix #16/#17 rules (Grok-only pins, Claude/Codex scrub, fix #17's
  back-ported render rules) are separate programs — do not re-do them
  here; if a pitch-deck-video file carries a Claude/Codex mention, the
  #16 scrub owns it, and this program only touches the same file for its
  own rules.
