# F-14 — post-report /demo stale README (fix #26 §2)

## Mechanism chosen: (a) the /demo run updates the README itself after filming

New step 7 in `pitch-deck-video` (`README_UPDATE_F26`): once QA passes and
`out/demo.mp4` exists, the /demo run (1) records `demo video:
<app-name>-video/out/demo.mp4` in `.hackathon/run-ledger.md`, and (2) makes
a surgical, idempotent edit to the existing `README.md` at the project root
so it links the video. First match wins: already links the path → do
nothing; has a video placeholder (`<!-- 🎥 Demo video: ... -->` comment or
`TODO: add demo link` / `TODO: add video`) → replace it with the real link;
has the readme-writer badge-button block → add a matching Demo Video
button to that row (same black `for-the-badge` shields style, plus the
`<!-- 🎥 Demo video: <path> -->` comment); otherwise insert a
`## Demo video` section after the title block (or at the top if there is no
`# ` heading). If no `README.md` exists, /demo writes none — authoring a
README is readme-writer's job — and records the video path in the /demo
return instead. Re-cuts (`--rebuild` / `--script` / `--render`) re-run the
step; the path is unchanged, so it is a no-op. The final report is NOT
rewritten by /demo (orchestrate-owned, point-in-time); the /demo return
carries the video path as the handoff input for it.

## Why (a) fits and (b) does not

- (b) — re-running the README step / readme-writer after /demo — would
  re-scan the repo, re-interview (readme-writer Step 3 asks the builder a
  batch of questions, which blocks an unattended /demo run), and rewrite
  the whole README, risking overwriting user edits made since the first
  build. readme-writer is a full-authoring skill, not an updater.
- /demo is often invoked standalone, with no orchestrate run in progress,
  so there is no "README step" to re-run — the update has to live inside
  /demo itself.
- /demo knows exactly when the video exists (it just rendered it) and the
  exact repo-relative path, so the edit is mechanical and idempotent.
- The ledger record keeps the existing convention working both ways:
  readme-writer Step 2 already reads the video path from the ledger in a
  first build, so a later readme-writer run also picks the video up.
- No new gate, no approval, no auto-/demo: the edit is a mechanical step
  inside /demo's own run, and /demo still runs ONLY on explicit user
  invocation (fix #22 gates DEMOGATE_O4_F22 / DEMOGATE_O9_F22 stand —
  nothing in this fix dispatches /demo from orchestrate or from the first
  build). No user-approval gate is added to the first build.

## Baseline verified before starting

`build.sh`: 24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae` — matches
the SPEC baseline. Re-verified after the edits: unchanged (same line count
and md5). No edit touched the built tree (`hackathon-ecc/`), no verifier
was edited, `build.sh` was not run, nothing was committed, bundled, or
pushed. Banned-term grep over all four edited files: 0 matches (full
banned-term list from the SPEC, case-insensitive). No model pins were
added or changed.

## Edits (staged sources only)

### 1. `new-skills/pitch-deck-video/SKILL.md:217–270` (inserted, new step 7)

Old: step 6 (QA) ended at the troubleshooting paragraph and the file went
straight to `## Motion-graphics layer ...` — no step linked a filmed video
back into the README.

New: `### 7 · Link the video into the README (fix #26 F-14,
README_UPDATE_F26)` — the five-rule step described under "Mechanism
chosen" above (ledger record first; first-match-wins README edit with
rules a–d; no README → write none, report the path; re-cuts are a no-op;
final report not rewritten). The video link uses the readme-writer house
style from `rewritten-skills/readme-writer/references/readme-template.md`
(badge-button row + `<!-- 🎥 Demo video: <path> -->` comment) and the
repo-relative path `<app-name>-video/out/demo.mp4`.

### 2. `new-skills/pitch-deck-video/commands/demo.md:9` (edited)

Old: `... write shots.json, build, and QA by looking at the contact sheets
— do not skip the QA step.`

New: `... write shots.json, build, and QA by looking at the contact sheets
— do not skip the QA step — then link the video into the README per the
skill's step 7 (README_UPDATE_F26), so a /demo run after the final report
does not leave the README stale.`

Why: the command is the /demo entry point; without this line the new skill
step would not run on invocation.

### 3. `new-skills/orchestrate/SKILL.md:101` (edited, step 6 clause)

Old: `... so the README links the real URL and the video (when one exists)
instead of a placeholder; it describes the verified tree, never a held
redesign; then write the final report ...`

New: `... so the README links the real URL and the video (when one exists)
instead of a placeholder; a video filmed later by an explicit ` + "`/demo`" + `
run is linked into the README by that run (pitch-deck-video step 7,
README_UPDATE_F26), not by re-running this step; it describes the verified
tree, never a held redesign; then write the final report ...`

Why: step 6 previously implied the README only ever gets the video if one
was filmed before step 6 ran. The clause records the post-report path so
orchestrate's sequence and /demo's step 7 agree. The fix #22 gate sentence
in the same line ("A demo video is filmed only when the user invokes
`/demo` explicitly — it is never part of this order") is untouched.

### 4. `rewritten-skills/readme-writer/SKILL.md:95` (edited, Step 2)

Old: `... — when the ledger names them, write the real links, never a
` + "`<!-- TODO: add demo link -->`" + ` placeholder.`

New: same sentence, plus ` A video filmed later, by an explicit /demo run
after the README was written, is linked into the README by that run
(pitch-deck-video step 7, README_UPDATE_F26) — readme-writer is not
re-run just for the video link.`

Why: keeps readme-writer consistent with the new mechanism — it stays the
first-build author (reading the ledger), and the later-video case is owned
by /demo step 7, not by re-invoking readme-writer.

## Deliberate boundary

The final report (`docs/final-report.md`) is intentionally NOT updated by
/demo. It is orchestrate-owned and the done signal for the first build; a
/demo run editing it would expand the fix's scope and risk overwriting
orchestrate-owned content. The /demo return already carries the video path
plus the narration record as the handoff input, so nothing is lost — the
report just stays point-in-time, and SPEC §2 names the README only.

## Anchor token

`README_UPDATE_F26` — present in all four edited files.
