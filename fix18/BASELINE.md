# Fix program #18 — BASELINE (analysis phase, Nov 11, 2026)

What a current `/demo` run produces against Anish's 7 criteria, verified
from the staged sources (`new-skills/pitch-deck-video/`, byte-identical
to the built tree — `build.sh:222–226` copies it verbatim, no runtime
patches).

## The 7 criteria, scored

| # | Criterion | Verdict | Why (file:line) |
| --- | --- | --- | --- |
| 1 | Shows functionality — the real product doing things live | **YES** | Film mode drives the real app with Playwright; `SKILL.md:459` "Don't film anything stubbed." |
| 2 | Addresses the problem, in the user's words | **YES** | `SKILL.md:104` "Open on the problem in the user's words, before the product name exists." Arc beat 1 is Problem (`SKILL.md:118–120`). |
| 3 | Includes ALL features of the program | **NO** | Arc is Problem 1 + Wow 1 + How 2–4 + Proof 1 + Close 1 (`SKILL.md:118–131`) — the wow plus ONE golden-path task. "Never two features in one beat" (`SKILL.md:125`) constrains, never covers. `grep feature` finds only lines 125 and 203. Seed has 5 beats (`template/shots.example.json`). |
| 4 | Names the tech stack | **NO** | Arch beat is model-vs-code only (`SKILL.md:92–96`, `:126–128`). `Arch.tsx` nodes are `{label, note, kind}` with no stack field. Zero "stack" occurrences in the skill. |
| 5 | States what makes it unique | **NO** | No differentiation beat exists. The wow (`SKILL.md:120–121`) is "the product doing the impossible thing" — not a comparison with alternatives. Zero "unique"/"competitor"/"differentiation" in the skill. |
| 6 | Visually gorgeous, above all | **NOT GUARANTEED** | Theme pull is an instruction (`SKILL.md:92–94`), not a check; QA is functional-only (`SKILL.md:170–186`, `qa.mjs`). Seed theme is fixed dark purple (`shots.example.json`: `bg #0d0a24`, `accent #ffc93c`) and ships if the pull is skipped. Bonus trap: `timeline.ts` vignette default 0.3 is heavy on light apps. Nothing requires best-looking states on camera. |
| 7 | Voice/audio matches the visuals | **PARTIAL** | Sync is architected (`timeline.ts:9–11`, measured narration; `SKILL.md:451` `<Screen />` Don't). But the caption-frame match is a manual read-the-sheets check with no enforcement (`SKILL.md:182`, `qa.mjs` check 4), and there is no audio-mix check at all — music is gain numbers only (`Video.tsx:71–88`, seed `under` 0.14). |

## Score

**2 yes, 1 partial, 4 no.** The skill is strong exactly where the audit
brief said (functionality, problem, sync architecture) and missing exactly
where it said (features, stack, uniqueness, gorgeousness bar, A/V
enforcement).

## Two refinements found during verification (beyond the brief)

1. **The arc under-counts its own beat budget.** Arc minimum is 6 beats
   (1+1+2+1+1) but the budget is 12–16 beats (`SKILL.md:100`, `:135`),
   so 4–10 beats are unspecified — today they pad the golden path. F1
   spends them on the remaining features instead.
2. **The seed is the same in both template files.** `template/shots.json`
   differs from `shots.example.json` only in the tts provider
   (MiniMax/Ukrainian_WiseScholar vs ElevenLabs/Rachel) — the dark-purple
   seed theme is identical in both, so the G4 trap applies whichever seed
   a project starts from.

## Baseline reference points (for the implementation re-trace)

- Seed storyboard: 5 beats — hook (card), setup (app), result (app),
  arch (card), close (card). No Edge beat, no feature coverage, no
  stack labels.
- Seed arch nodes: "Your goal" (in), "Ranker" (llm), "Scheduler" (code),
  "Writer" (llm), "Your week" (out) — labels + notes only.
- Seed music gain: open 0.34 / under 0.14 / close 0.30.
- QA as shipped: stills-only contact sheets; 5 printed checks (warnings
  empty, failures empty, right page, no spinners/skeletons/empty states,
  claims match screen, captions legible); no theme, coverage, or audio
  check of any kind.
