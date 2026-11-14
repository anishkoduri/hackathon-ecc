# Dry-run #29 — Home Run storyboard re-trace under fix #18 rules

**Date:** Nov 11, 2026 (evening CST) · **Worker:** DRY-RUN / RE-TRACE, fix program #18
**Skill under test (built tree):** `~/workspace/hackathon-plugin/hackathon-ecc/skills/pitch-deck-video/`
**Spec:** `~/workspace/hackathon-plugin/fix18/SPEC.md` §5 step 3

## 0 · Source of the must-have list — READ THIS FIRST

**There is NO `docs/scope.md` in this workspace.** The must-have list below was
reconstructed from the standing record of the Home Run build: the final build
report pasted by Anish on Nov 11, ~01:10 CST (agent running as Composer 2.5 Fast),
recorded in `memory/2026-11-11.md` (the "Home Run smoke-test build FINISHED" entry).
That report is the only source used for the app's features, demo path, numbers,
and design tokens. Where the record is silent, this trace says so instead of
inventing (see §7, gaps).

Reconstructed facts used (all from that record):
- Phone-first web app, running at `http://localhost:5174`, project path on Anish's
  Windows machine `C:\Users\heman\home-run` (`npm run dev`).
- One account can order or deliver; both sides share a single request record.
- Demo path, clicked through in the browser: Jordan Hale views Maya Chen's
  Trader Joe's run first under Recommended ("On your trip"); fee from the shared
  policy only — Houston $22 + perishable $4 + keep cold $5 = $31, merchandise
  excluded; offer sent, Maya accepts, pays Trader Joe's herself and sends order
  name / reference / pickup window; her delivery code is on her screen only;
  Jordan marks picked up, then arriving, and enters the code — a wrong code does
  NOT complete the run, the right code does, and the simulated $31 moves from
  Maya's balance to Jordan's.
- Posting covers store pickups (real Houston, Austin, Dallas, San Antonio
  branches + H-E-B in The Woodlands) and personal items.
- Runners sort Latest / Closest / Recommended, post trips, and see favorites,
  notifications, history; "Reset demo data" on the You tab restores the seed.
- Per-trip run totals: Jordan's Houston trip = Maya's $31 run + Katy package
  $26 = $57 if both taken.
- When an offer moves the delivery fee, the screen states the policy amount and
  how far the offer is above/below it.
- Recorded assumptions: no live places/payments API (local store catalog,
  simulated money).
- Design: the design search "kept returning a marketing page," so the app used
  "the verified block style and the warm bakery palette instead of that layout."

## 1 · Features + cuts (F1)

`shots.json` `features` (7 entries — the task's bullets, with the demo-path steps
grouped as ONE golden-path feature set and the You-tab items grouped as ONE
feature, since they share one tab and one beat):

| # | Feature (must-have, reconstructed) | Beat |
| --- | --- | --- |
| 1 | Shared request record + shared fee policy | `how4` |
| 2 | Golden path: offer → accept → merchant pay → pickup → arriving → delivery code (wrong rejected, right completes; simulated $31 Maya → Jordan) | `how1` * |
| 3 | Two pickup types: store runs + personal items | `how5` |
| 4 | Real branch catalog: Houston / Austin / Dallas / San Antonio + H-E-B The Woodlands | `how6` |
| 5 | Sort: Latest / Closest / Recommended | `how7` |
| 6 | Trips with per-trip run totals | `how8` |
| 7 | You tab: favorites, notifications, history + demo reset | `how9` |

\* The golden-path feature spans three beats: `how1` (offer → accept), `how2`
(pay → pickup → arriving), `how3` (code check → $31 moves). The `features`
entry records `how1` as the entry beat; the entry carries a `note` field naming
the continuation beats. `qa.mjs` checks the recorded beat id exists and was
filmed; all three beats are app shots with marks (see §6).

**Cuts: none.** Zero must-haves were cut — all 7 reconstructed features fit in
16 beats and 118.6s (see §5). Sub-details folded into their feature's beat
rather than cut: "one account can order or deliver" is shown by the golden path
itself (Maya orders, Jordan delivers, one record); the offer-vs-policy display
("screen states the policy amount and how far the offer is above/below it") is
named in the `how4` line and shown in its footage.

## 2 · Arc — every beat's say line

Beat budget 12–16; this trace uses **16 beats** (the max): Problem 1 + Wow 2 +
Edge 1 + How 9 + Proof 2 + Close 1. (Wow takes 2 beats because one Wow line at
14–18s would breach the ~12s-per-beat split rule; Proof takes 2 because a
single arch line long enough for the 12–15s band would likewise breach it.)

| Beat | Kind | Say line |
| --- | --- | --- |
| `problem` | card | You're driving to Houston anyway, and someone back in College Station needs groceries from that same Trader Joe's right now. |
| `wow1` | app | Jordan's driving to Houston anyway. He opens Home Run, and Maya's Trader Joe's run is right there — on his trip. |
| `wow2` | app | Thirty-one dollars, and the fee isn't a guess — it's the shared policy: twenty-two for Houston, four perishable, five keep-cold. |
| `edge` | app | Unlike a delivery app, there's no dispatcher and no surge — one shared record, one shared fee, and the runner's already going that way. |
| `how1` | app | Jordan offers to take the run. Maya accepts — one record, both sides, no second thread. |
| `how2` | app | Maya pays Trader Joe's herself, sends the pickup window, and Jordan marks it picked up. |
| `how3` | app | The wrong code bounces. The right code completes it, and thirty-one dollars moves to Jordan. |
| `how4` | app | One request record for both sides. The fee comes only from the shared policy — any offer above it says so. |
| `how5` | app | Post a store run, or a personal item — a package from Katy rides the same trip. |
| `how6` | app | Real branches, not placeholders — Houston, Austin, Dallas, San Antonio, plus H-E-B in The Woodlands. |
| `how7` | app | Runners sort by Latest, Closest, or Recommended — the run on your trip surfaces first. |
| `how8` | app | Post your trip, and each one totals its runs — fifty-seven dollars on Jordan's Houston trip. |
| `how9` | app | The You tab holds favorites, notifications, history — and reset demo data brings the seed back. |
| `proof1` | card (arch) | Built as a phone-first web app — no model calls, just the record, the policy, and the code check. |
| `proof2` | app | Simulated money, real logic — thirty-one dollars moves on screen, nothing leaves a wallet. |
| `close` | card | Home Run. The trip you're already taking, carrying the groceries someone else needs — that's the run. |

Rules check per line: one idea per beat; numbers said out loud ($31, $22/$4/$5,
$57, Katy $26 implied via the $57 total); UI never narrated (no "here we click
…"); problem in the user's words as far as the record allows (see §7 — no
verbatim problem quote exists in the standing record, so the line is drafted in
his register, not claimed as a quote).

### Edge beat (F3)

`edge`, one sentence, alternative named ("a delivery app" — DoorDash/Uber Eats
class, clearly implied; no specific competitor is named anywhere in the standing
record, so none is invented): no dispatcher, no surge — one shared record, one
shared fee, on a trip the runner is already taking. Shown live with a `focus`
on the Trader Joe's run in the list. Source: the build report's fee-policy and
shared-record facts; the differentiation claim itself (already-going-that-way +
shared record + shared fee vs a dispatched delivery app) is the trace's reading
of those recorded facts, not a quote from `docs/decision-record.md` (which does
not exist in this workspace).

### Arch beat (F2) — stack gap recorded

`proof1` (arch card). Nodes, from the app's recorded flow only — **no `stack`
labels on any node, because no stack item is recorded anywhere in the standing
record.** The build report records a phone-first web app at `localhost:5174`
run with `npm run dev`; it does not record a framework, model, service, or
infra (no `package.json`, no decision record in this workspace). Localhost port
5174 was NOT cited as a framework claim. Per F2, the arch beat therefore says
the framework only, and the gap is recorded here:

| Node | Kind | Note |
| --- | --- | --- |
| Maya's request | in | one shared record, both sides |
| Fee policy | code | Houston $22 + perishable $4 + keep-cold $5 = $31 |
| Sort + match | code | Latest / Closest / Recommended; on your trip |
| Delivery-code check | code | wrong code rejected, right code completes |
| Simulated ledger | code | $31 moves Maya → Jordan, no real money |
| Run complete | out | both sides see the same finished record |

No model-call (`llm`) node exists: nothing in the record indicates an LLM in
the loop, so the arch honestly shows an all-code pipeline — which is itself the
credibility point (`proof1` says so aloud). **Spoken stack phrase** (one phrase,
in `proof1`): "Built as a phone-first web app" — the framework only, per the F2
fallback. **Gap:** a real `/demo` run must pull the stack from the app's
`package.json` (on Anish's machine) and label the nodes; until then the arch
cannot name Next.js / React / Vite or anything else without inventing it.

### Theme (F4)

Pulled from the app's tokens **as described in the build report** — "the verified
block style and the warm bakery palette" — NOT the seed theme. Token source
recorded in `shots.json` as `theme.source`:

> Home Run final build report (pasted by Anish, Nov 11 ~01:10 CST; recorded in
> memory/2026-11-11.md): 'the verified block style and the warm bakery palette'.
> Exact token hex values are NOT in the standing record — the app's design-tokens
> file lives on Anish's Windows machine (C:\Users\heman\home-run), not in this
> workspace. Hex/font values below are warm-bakery stand-ins for this trace; a
> real /demo run must replace them from the app's tokens.

Trace values (stand-ins, light app → `theme.vignette = 0`, recorded choice):
`bg #FBF3E4`, `bgDeep #F3E6CE`, `card #FFF9EF`, `line #E8D9BE`,
`lineStrong #D9C49A`, `text #2E1F14`, `textSoft #4A3423`, `textMuted #8A7360`,
`accent #C05621` (terracotta), `accent2 #B7791F`, `accent3 #7A5C2E`,
`captionBg rgba(46,31,20,0.78)`, `captionText #FFF9EF`; fonts Inter / Fraunces /
JetBrains Mono (stand-ins). Seed theme (`bg #0d0a24`, `accent #ffc93c`,
`card #161141`) appears nowhere in the traced `shots.json`.

## 3 · Per-beat A/V table — skeleton (F5)

Printed by `qa.mjs` (see §6). To be completed while reading the contact sheets
at a real QA — **there was no live render in this trace** (no running app, no
voice key, Remotion/ffmpeg stubbed), so every row below is "not yet filmed"
and the table is a skeleton, exactly as the task specifies. A "no" at QA is
BLOCKING.

| Shot | Claim in the `say` line | Stills support it? |
| --- | --- | --- |
| `problem` [card] | Someone in College Station needs groceries from the same Trader Joe's you're driving to | ___ (TBD at QA) |
| `wow1` [app] | Maya's Trader Joe's run appears first under Recommended, "On your trip" | ___ |
| `wow2` [app] | $31 fee = shared policy $22 + $4 + $5 | ___ |
| `edge` [app] | One shared record, one shared fee, runner already going that way | ___ |
| `how1` [app] | Offer → Maya accepts; one record, both sides | ___ |
| `how2` [app] | Maya pays the merchant, sends pickup window; Jordan marks picked up | ___ |
| `how3` [app] | Wrong code rejected, right code completes, $31 moves to Jordan | ___ |
| `how4` [app] | One record; fee only from policy; offer above policy says so | ___ |
| `how5` [app] | Store run or personal item (Katy package) on the same trip | ___ |
| `how6` [app] | Real branches: Houston, Austin, Dallas, San Antonio, H-E-B The Woodlands | ___ |
| `how7` [app] | Sort Latest / Closest / Recommended; trip run surfaces first | ___ |
| `how8` [app] | Trip totals its runs: $57 on Jordan's Houston trip | ___ |
| `how9` [app] | You tab: favorites, notifications, history, reset demo data | ___ |
| `proof1` [card] | Phone-first web app; no model calls; record/policy/code check | ___ |
| `proof2` [app] | Simulated $31 moves on screen; no real money | ___ |
| `close` [card] | Tagline left on screen | ___ |

`do` actions in the traced `shots.json` are trace skeletons built from the
report's named UI ("Recommended", "On your trip", "Reset demo data", "You" tab)
— the app's real routes/selectors must be confirmed against screenshots at a
live run (step 3 of the skill). The `how3` code-entry `type` uses a placeholder
`0000` as the wrong code; the real wrong/right codes come from the live demo
account at record time.

## 4 · Runtime math (F6)

**Basis, stated explicitly:** speaking rate **150 wpm = 2.5 words/sec**;
word count = whitespace-split tokens of each `say` line as written in
`shots.json` (a standalone "—" counts as a token under this rule — that is why
the counts below differ slightly from a hand count). Duration per line =
words ÷ 2.5. Beat = line duration + `gapMs` 240ms. Total = LEAD 0.7s +
Σ(line + gap) + TAIL 1.7s. **These are estimates, not measured TTS durations**
— the real pipeline computes the total from measured narration in
`src/vo-durations.json`; this trace's `vo-durations.json` is synthetic with
durations set to these estimates.

| Beat | Section | Words | Line (s) | + gap (s) |
| --- | --- | --- | --- | --- |
| `problem` | Problem | 20 | 8.00 | 8.24 |
| `wow1` | Wow | 21 | 8.40 | 8.64 |
| `wow2` | Wow | 20 | 8.00 | 8.24 |
| `edge` | Edge | 24 | 9.60 | 9.84 |
| `how1` | How | 16 | 6.40 | 6.64 |
| `how2` | How | 15 | 6.00 | 6.24 |
| `how3` | How | 15 | 6.00 | 6.24 |
| `how4` | How | 21 | 8.40 | 8.64 |
| `how5` | How | 17 | 6.80 | 7.04 |
| `how6` | How | 15 | 6.00 | 6.24 |
| `how7` | How | 15 | 6.00 | 6.24 |
| `how8` | How | 16 | 6.40 | 6.64 |
| `how9` | How | 16 | 6.40 | 6.64 |
| `proof1` | Proof | 19 | 7.60 | 7.84 |
| `proof2` | Proof | 14 | 5.60 | 5.84 |
| `close` | Close | 17 | 6.80 | 7.04 |

Section totals (narration + gaps) vs the F6 allocation table:

| Section | Beats | Traced | Budget | Verdict |
| --- | --- | --- | --- | --- |
| Problem | 1 | 8.24s | 8–10s | ✓ in budget |
| Wow | 2 | 16.88s | 14–18s | ✓ in budget |
| Edge | 1 | 9.84s | 8–10s | ✓ in budget |
| How / features | 9 | 60.56s | 55–65s | ✓ in budget, **largest share** |
| Proof (arch + stack) | 2 | 13.68s | 12–15s | ✓ in budget |
| Close | 1 | 7.04s | 6–8s | ✓ in budget |
| Content (narration + gaps) | 16 | 116.24s | 113–126s | ✓ |
| **Total (LEAD 0.7 + content + TAIL 1.7)** | — | **118.64s** | **under 2:10 (130s)** | ✓ **11.36s of room** |

No section is over budget, so **no re-cut was needed** and no feature was moved
to `cuts` for time. Total is 118.64s — under the 2:10 hard rule and far under
the 2:30 absolute ceiling. Room (11.36s) is close to the ~10s target. Longest
single beat is `edge` at 9.84s — no beat approaches the ~12s split rule.

## 5 · 7-criteria verdict table (+ F6)

| # | Criterion | Verdict | Evidence in this trace |
| --- | --- | --- | --- |
| 1 | Shows functionality (real app, live) | **PASS (by design)** | All 13 app shots are film-mode Playwright shots against the local app (`http://localhost:5174`); no stubbed action is filmed. Not executable here — no live app in this VM (see §7). |
| 2 | Addresses the problem, in the user's words | **PASS with a caveat** | `problem` opens on the pain before the product name exists. Caveat: no verbatim problem quote exists in the standing record, so the line is drafted in his register, not a quote (§7). |
| 3 | Includes ALL features of the program | **PASS** | 7 reconstructed must-haves → 7 `features` entries, each with a beat; `qa.mjs` coverage table complete, all "filmed"; cuts = none (§6). Caveat: the list is reconstructed from the build report, not `docs/scope.md`, which does not exist here. |
| 4 | Names the tech stack | **PARTIAL — gap recorded** | Arch nodes carry no `stack` labels and the spoken line names only "phone-first web app": no stack item is recorded in the standing record, and the trace invents none (§2, §7). The F2 fallback (framework only + gap in the report) is applied. |
| 5 | States what makes it unique | **PASS** | Dedicated `edge` beat after the wow, alternative named ("a delivery app"), one sentence, in the user's words as far as the record allows. |
| 6 | Visually gorgeous (above all) | **PASS (trace-level)** | Theme pulled from the app's described tokens (warm bakery palette + verified block style), `theme.source` recorded, seed absent, vignette 0 for the light app. Caveat: exact hex/font values are stand-ins (§2, §7); gorgeousness checks (b) best-looking states and (c) vignette are QA reads off real sheets, not yet performed. |
| 7 | Voice/audio matches the visuals | **PARTIAL — skeleton only** | Per-beat A/V table skeleton printed by `qa.mjs` (§3) but completable only at real QA; mix check not performed (no render). `music.gain.under` = 0.14 (≤ 0.20), so the `qa.mjs` under-gain guard does not fire. |
| F6 | Hard runtime rules + allocation | **PASS** | Total 118.64s < 130s; every section inside its allocation band; How is the largest share (60.56s); no beat over ~12s. |

## 6 · `qa.mjs` functional test

**Tested file:** `~/workspace/hackathon-plugin/hackathon-ecc/skills/pitch-deck-video/template/scripts/qa.mjs`
(md5 `facbd77b9a77d3fbc88819ef09816464`, identical in the built tree and the
test copy).

**Harness:** built template copied to `/tmp/fix18-qatest/`; traced `shots.json`
written in; synthetic `src/vo-durations.json` (durations = the estimated line
lengths from §4, `gapMs` 240); synthetic `capture/marks.json` (one mark per
app shot — 13 marks, warnings empty). `npx` and `ffmpeg` are NOT installed
for the test project, so both were stubbed on PATH (`/tmp/fix18-stubbin/`):
fake `npx` creates the `.png` arg passed to it and exits 0; fake `ffmpeg`
creates the last-arg sheet png and exits 0. No real Remotion render happened;
the stubs exist only to let `qa.mjs`'s checks run.

### Baseline run — `node scripts/qa.mjs` in `/tmp/fix18-qatest/`

**Exit code: 0.** Rendered 16 stills, 3 contact sheets
(`out/qa/sheet_01.png`–`sheet_03.png`).

Observed output (exact lines that matter):

```
Total runtime (measured narration + gaps + lead/tail): 118.6s — hard rule under 2:10 (130s), absolute ceiling 2:30 (150s).
```

```
Coverage table (feature → beat):
  Shared request record + shared fee policy → how4 — filmed
  Golden path: offer → accept → merchant pay → pickup → arriving → delivery code (wrong rejected, right completes; simulated $31 Maya → Jordan) → how1 — filmed
  Two pickup types: store runs + personal items → how5 — filmed
  Real branch catalog: Houston / Austin / Dallas / San Antonio + H-E-B The Woodlands → how6 — filmed
  Sort: Latest / Closest / Recommended → how7 — filmed
  Trips with per-trip run totals → how8 — filmed
  You tab: favorites, notifications, history + demo reset → how9 — filmed
  Cuts (recorded, with reasons):
  (none)
```

```
Theme: pulled from the app tokens — source recorded: Home Run final build report (…)
Vignette: theme.vignette = 0
```

Per-beat A/V table skeleton printed for all 16 shots (`supports it: ___`).
Final line: `No BLOCKING findings from the automated checks.` No under-gain
warning (under = 0.14).

### Negative tests (same harness, one change each)

| Test | Change | Exit | Exact BLOCKING / warning line observed |
| --- | --- | --- | --- |
| (a) seed theme | Theme colors reverted to seed (`bg #0d0a24`, `accent #ffc93c`, `card #161141`) and `theme.source` deleted | **1** | `BLOCKING — theme: shots.json still carries the seed theme with no recorded theme.source` (also printed: `Theme: identical to the seed theme — no theme.source recorded`) |
| (b) over runtime | `how4` line lengthened (+45 words) and its `vo-durations.json` dur set 8.40 → 26.40s | **1** | `Total runtime (measured narration + gaps + lead/tail): 136.6s — hard rule under 2:10 (130s), absolute ceiling 2:30 (150s). BLOCKING: over 2:10 — re-cut.` and `BLOCKING — runtime: 136.6s over the 2:10 (130s) hard rule — re-cut` |
| (c) missing beat | `features[0].beat` changed to `how-missing` (not in `shots.json`) | **1** | Coverage row: `Shared request record + shared fee policy → how-missing — MISSING BEAT`; `BLOCKING — coverage: feature "Shared request record + shared fee policy" → beat "how-missing" missing from shots.json` |
| (d) hot bed | `music.gain.under` set to 0.25 | **0** | `WARNING: music.gain.under is 0.25 (over 0.20) — the bed risks burying the voice. Do the 10-second mix listen from the middle of the video and confirm the narration is intelligible over it.` — warning only; final line `No BLOCKING findings from the automated checks.` |

All four negative tests behave as the SPEC requires: (a)–(c) block with exit 1
and the exact expected finding; (d) warns without blocking (exit 0). Note the
baseline runtime printed by `qa.mjs` (118.6s) matches the §4 hand computation
(118.64s) to rounding.

## 7 · Findings, gaps, and what a real /demo run still needs

1. **No `docs/scope.md` exists in this workspace** — the must-have list is a
   reconstruction from the Nov 11 final build report (memory record). If the
   real scope listed more must-haves, this trace under-covers them. A real
   `/demo` run starts from the app's actual `docs/scope.md`.
2. **Stack gap (criterion 4, partial).** No framework/model/service is recorded
   for Home Run anywhere in the standing record (checked: the build-report
   memory entry, `fix13/MANIFEST.md`, and a tree-wide grep — only SPEC.md and
   the fix13 manifest even mention "home run"). The trace invents none; the
   arch says "phone-first web app" only. Real run: pull from the app's
   `package.json` + decision record.
3. **Theme values are stand-ins (criterion 6, trace-level).** The record gives
   the palette's description ("verified block style and the warm bakery
   palette"), not token hex values. The traced hex/fonts are plausible
   warm-bakery picks, flagged as such in `theme.source`. Real run: replace
   from the app's `docs/design-tokens.md` (or equivalent).
4. **Problem/Edge lines are not verbatim quotes.** The standing record contains
   no verbatim user wording for the problem or the differentiator; the lines
   are drafted in Anish's register from the recorded facts. Real run: confirm
   the wording with him (F3 fallback: ask for one line rather than invent a
   competitor claim — the trace's "delivery app" alternative is generic and
   implied by the product, not a named competitor).
5. **No live verification was possible in this trace.** The Home Run app runs on
   Anish's Windows machine, not in this VM; there is no voice key and no
   Remotion install here. So: the `do` selectors are skeletons to confirm
   against step-3 screenshots; the A/V table is uncompleted (skeleton only);
   the 10-second mix listen was not performed; `vo-durations.json` is
   synthetic estimates, not measured TTS. The SPEC's step-3 note anticipates
   exactly this: a re-trace checks storyboard + `shots.json` + QA outputs,
   not a full render.
6. **Beats at the budget max.** 16 beats is the top of the 12–16 budget. Any
   feature added by a real scope (beyond the 7 reconstructed here) would force
   a cut into `cuts` or a merge — the cap governs, per F1/F6.

## 8 · Trace artefacts (this run)

- Traced `shots.json`: `/tmp/fix18-qatest/shots.json` (16 shots, 7 features, 0 cuts)
- Synthetic `src/vo-durations.json` + `capture/marks.json`: `/tmp/fix18-qatest/src/vo-durations.json`, `/tmp/fix18-qatest/capture/marks.json`
- Baseline QA log: `/tmp/fix18-qatest-qa.log` (exit 0)
- Negative-test logs: `/tmp/fix18-neg-a-qa.log` (exit 1), `/tmp/fix18-neg-b-qa.log` (exit 1), `/tmp/fix18-neg-c-qa.log` (exit 1), `/tmp/fix18-neg-d-qa.log` (exit 0)
- Stub binaries: `/tmp/fix18-stubbin/npx`, `/tmp/fix18-stubbin/ffmpeg`
- This report: `~/workspace/hackathon-plugin/fix18/dryrun29-report.md`
