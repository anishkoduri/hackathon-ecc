---
name: pitch-deck-video
description: "Use when the user wants a demo video, launch video, product walkthrough, hackathon submission video, or screen recording of a local web app — especially if they say the video must be re-doable after the UI changes. Generates a narrated 1:30–1:50 product demo by driving the real app with Playwright and cutting the edit from measured narration, so a rebuild after a frontend change takes ~2 minutes and one command. Also offers two opt-in OpenMontage modes on request: montage (real archival and stock footage cuts) and explainer (scripted animated scenes). Film stays the default."
---

# /demo

Generate a narrated product demo video from a running local web app. The edit is
**derived, never hand-timed**, so when the frontend changes you re-record and the
cut follows — no frame numbers to repair.

Built for the case that actually happens: the UI is still moving while you need
the video.

## Usage

```
/demo                                     # film the app in the current directory
/demo <path-to-app>                       # film a specific app
/demo --rebuild                           # re-record and re-cut an existing video project
/demo --script                            # narration changed only; reuse the last take
/demo --render                            # cards/captions changed only; re-render
```

## The shape of it

Four generated files drive everything. Only the first is written by a human.

| file | holds | written by |
| --- | --- | --- |
| `shots.json` | what is said, the voice, the music, the theme, and what the browser does | **you** |
| `src/vo-durations.json` | how long each line actually takes | `scripts/tts.mjs` |
| `capture/marks.json` | when each shot started in the take, and where to look | `scripts/record.mjs` |
| `src/frames.json` | how many frames came out of the take | `scripts/frames.mjs` |

`src/timeline.ts` derives the entire edit from those. Scene lengths come from the
**measured** narration audio. The footage is stretched to fit it. Camera moves
come from element bounding boxes **measured live during the recording**, so a
moved button moves the shot instead of breaking it.

## Workflow

### 1 · Scaffold

Copy `template/` from this skill into `<app-name>-video/` next to the app, then
`npm install`. The template ships seed JSON so it typechecks and renders before
the first recording.

Never edit files under `skills/pitch-deck-video/template/` in the plugin for one project —
that is the shared template. Edit the copy.

### 2 · Check for a saved login first

If the app has auth, look for a Playwright storage state the repo already keeps
for its own e2e tests (`.auth/*.json`, `storageState`, `playwright/.auth/`).
Point `app.storageState` at it and the recording starts logged in with no login
flow on camera. Only build a login shot if there is no such file — and then use
`{"type": {"sel": "…", "env": "DEMO_PASSWORD"}}` so the password is never
written into `shots.json`.

### 3 · Learn the app before writing a word

First read `docs/scope.md` + `docs/decision-record.md` — the scoped wow moment
and the product story live there. The storyboard's opening wow must BE the
scoped wow: name it from the scope, in one concrete sentence, before
storyboarding. Then start the app's dev server and **screenshot every route at
1920×1080, then read the images** — the screenshots verify the scoped wow and
show how it renders on screen; they do not re-derive a different wow. If a
screenshot contradicts the scope (the scoped moment is not visible or not
working), say so in the final report and film what is actually there — do not
silently swap in a different wow. Do not write narration from the source code.
You are writing about what a judge will see, and only the screenshots tell you
that.

```js
// one-off script; Playwright comes with the template
for (const r of routes) {
  await p.goto(base + r, { waitUntil: 'networkidle' });
  await p.waitForTimeout(700);
  await p.screenshot({ path: `/tmp/shots/${r}.png` });
  console.log(r, await p.evaluate(() => document.documentElement.scrollHeight));
}
```

Note the scroll heights: anything past 1080 needs a `scroll` action or it never
appears on camera.

### 4 · Write `shots.json`

Start from `template/shots.example.json`. See `references/shots-reference.md`
for every field and action.

Pull the `theme.colors` from the app's own design tokens so the cards and the
footage read as one piece. Fill `cards.arch.nodes` with the real architecture —
which boxes are model calls and which are deterministic code. That beat is what
separates a demo from a wrapper, and judges look for it.

Narration rules that matter:

- **12–16 beats; the video is 1:30–1:50 total.** Under a 2:00 cap, leave 10 seconds of room. Lengths by artefact: the video is 1:30–1:50; the live demo storyboard is 2–4 min; the pitch storyboard is <90s. Do not mix them up — the video cap governs this skill, the longer live-demo storyboard and the shorter pitch storyboard belong to the pitch, not the video.
- **One idea per beat.** The beat ends when the idea does.
- **Say the number.** "Six people scored, Priya wins" beats "it picks someone."
- **Never narrate the UI.** Not "here we click Approve" — say what it means.
- **Open on the problem in the user's words**, before the product name exists.
- **Close on one sentence** you want left on screen.

### Storyboard craft — lead with the wow moment

The storyboard is the video's argument, and it opens with the single most
captivating moment of the product — the scoped wow moment from `docs/scope.md` (step 3), not a new one derived from the screenshots. Before writing any other beat, name it in one concrete sentence:
"the opening shot must show X doing Y" (for example, "the opening shot
must show the calendar filling itself the moment Priya picks a time").
If you cannot state the wow moment that concretely, you do not have a
storyboard yet — go back to `docs/scope.md` for the scoped wow, then to the screenshots to verify it renders on screen. The wow moment is beat
one, not the finale: a judge who is bored by beat three never sees beat
twelve.

The arc after the wow moment, in order:

1. **Problem** — one beat, in the user's words, before the product name
   exists. The pain, not the category.
2. **Wow** — the opening shot above: the product doing the impossible
   thing, live, with the number said out loud.
3. **How** — two to four beats along the golden path: one user, one task,
   each beat one action and one outcome. Never two features in one beat.
4. **Proof** — the arch card beat: which boxes are model calls and which
   are deterministic code. This is the credibility beat; judges look for
   it, and it is what separates a demo from a wrapper.
5. **Close** — one sentence left on screen (the tagline, said out loud).

Shot design per beat: one beat is one screen (or one `focus` move within
a screen). If a beat needs two screens, it is two beats. Any text that
would be illegible at 1080p gets a `focus` — a dense list, a side panel,
a drawer — and a `{"focus": null}` before navigating away. Pacing: at
12–16 beats over 90–110 seconds, a beat averages 7–9 seconds; a beat
whose line runs past ~12 seconds is two ideas and must be split. Cut
setup out of every beat with `{"cut": true}` after the navigation and
loading steps, so no beat opens on a spinner.

### 5 · Build

```sh
APP_DIR=/path/to/app npm run all
```

Narration → recording → frames → render. It starts the dev server if nothing is serving `app.url`, reading the app's own
`dev` script to work out how that framework takes a port. Set `app.devCommand`
if it needs something specific. Typical full rebuild: **~2 minutes**.

### Which app gets filmed — local only

`/demo` films the local app from the project directory. The video is
made from the code, not from a link.

- `app.url` is the **local** dev-server URL (for example
  `http://localhost:5180`). Never set it to a deployed URL, and never
  film a deployed product: the deployed app is a different artefact from
  the code in front of you, and filming it hides exactly the regressions
  a rebuild is meant to catch.
- `APP_DIR` (or the current directory) is where the app is started from:
  if nothing is serving `app.url`, the build auto-starts the app from
  `APP_DIR`, reading the app's own `dev` script to work out how that
  framework takes a port. Set `app.devCommand` if it needs something
  specific.
- Deploying the app (via `deploy-fast`) is still part of the build, and
  the deployment URL still goes in the final report — but deployment and
  filming are separate steps, and the video always shows the local app.

`shots.json` is validated first, so a duplicate id or an unknown action fails in
two seconds rather than producing a confusing video two minutes later.

### 6 · QA by looking at it — this is not optional

```sh
npm run qa          # one still per shot, stacked into contact sheets
npm run qa 3        # three per shot, when you want to check a transition
```

Then **read the sheets as images**. Scrubbing the video is slow and you will
miss things; a contact sheet takes seconds and catches exactly the failures that
matter.

Check: **`capture/marks.json → warnings` is empty** (a missing selector is a
warning, not a crash — you still get a video, and a list of what broke). Then:
does each caption land on a frame that supports it? Any blank or white frames?
Is small text legible, or does it need a `focus`?

`references/troubleshooting.md` has every failure this pipeline has actually hit
and the fix for each. Read it before debugging from scratch.

## Re-cutting after the UI changes

This is the point of the whole thing.

```sh
APP_DIR=/path/to/app npm run all
```

Most changes need nothing else — moved elements, restyled pages, new copy. What
still needs judgement:

- **A page was deleted or renamed** → repoint or replace that shot.
- **A feature was rewritten** → the narration for that beat is now a claim about
  something that no longer exists. Rewrite the line.
- **A selector genuinely vanished** → check the warnings list and fix it there.

Narration is cached per line, so only edited lines re-synthesise.

### `/demo --rebuild` — re-film an existing video project

`/demo --rebuild` is how an existing video project is re-recorded and
re-cut after the UI changes. It locates the existing
`<app-name>-video/` directory next to the app (the directory plain
`/demo` scaffolded on the first run), **skips the scaffold step
entirely**, and reuses the project's edited `shots.json` as-is — the
narration, voice, music, and shot list the user already approved.

- Never run plain `/demo` over an existing video project: plain `/demo`
  scaffolds a fresh project, and re-scaffolding over an existing
  directory would copy the template's seed `shots.json` over the edited
  one. On an existing project, always use `/demo --rebuild`.
- Never copy the template's seed `shots.json` over an edited one, by
  hand or by re-running the scaffold. If the edited `shots.json` is ever
  lost, it is rebuilt from the last video's narration and the current
  screenshots — not from the seed.
- `--rebuild` re-runs the full pipeline (narration → recording → frames
  → render) from the current `shots.json`; narration lines that did not
  change are served from the per-line cache, so a rebuild after a
  frontend change still takes about 2 minutes.
- The narrower re-cuts: `/demo --script` when only the narration
  changed (reuses the last take — re-synthesises the edited lines and
  retimes the edit, no re-recording), and `/demo --render` when only
  cards or captions changed (re-renders from the existing take and
  narration, no re-recording, no re-synthesis).

## Voice

**The voice is the single biggest quality difference in the finished video, and
the fallback is genuinely poor.** Say so plainly before the first build rather
than after.

### Voice preflight — run before any narration

Before `scripts/tts.mjs` synthesises a line, preflight the voice provider:
check `ELEVENLABS_API_KEY` (set in the environment), the `piper` binary, and
`say` availability (`say` exists on macOS only). `tts.mjs` logs which
providers are available before it starts. If the configured provider is
missing, it resolves to the next available voice in the chain
(ElevenLabs → Piper → `say`; MiniMax → Piper → `say`; Piper → `say`;
`say` → Piper → ElevenLabs), and if that chain is exhausted it falls
through to any other usable voice (ElevenLabs → Piper → `say` → MiniMax)
before skipping narration — narration is skipped only when no usable
voice exists at all. The fallback is **per line, at runtime, not only at
preflight**: a provider that passes preflight but fails while rendering
a line falls through to the next usable voice for that line, and then to
any other usable voice, before that line goes silent. A line renders
silent with an estimated length only when every usable voice has failed
for it — the video never aborts on a voice failure.

**If no voice provider exists at all, the video still builds — without
narration.** `tts.mjs` skips every narration line, writes estimated beat
lengths (word-count based, so scenes keep a sensible length) into
`src/vo-durations.json`, and the video renders music-only/silent. It never
aborts the video for a missing voice. Note the missing narration in the
final report, with what would fix it (an `ELEVENLABS_API_KEY` or Piper
installed), so the user can re-run `npm run script` later for a narrated cut.

- `tts.provider: "minimax"` — good. MiniMax credentials come from the
  environment (`MINIMAX_API_KEY` / `MINIMAX_GROUP_ID`) or from an env
  file the user already has, pointed at by `tts.envFile` — see the
  narration-key prompt below; do not ask about MiniMax separately. Voice
  ids come from MiniMax's system voice list; the language tag on a voice
  is a hint, not a restriction (a Ukrainian-tagged voice reads English
  well with `languageBoost: "English"`).
- `tts.provider: "say"` — macOS's built-in synthesiser, and only the legacy
  voices are usually installed. It is robotic, it mispronounces product names,
  and it is obvious to anyone watching. Usable for checking timing, weak for
  anything a judge or customer will see.
- **A human recording beats both.** Drop `<id>.wav` files into `public/vo/` and
  run `npm run script`; the durations are re-measured and the whole video
  retimes itself with no other edit.

If there is no key, build the video anyway — but tell the user up front that the
voice is the weak part and that either a key or ten minutes with a microphone
fixes it. Do not quietly ship a `say` voiceover as if it were finished.
That holds only where some fallback voice exists: with no voice provider at
all (no key, no Piper, and no `say` — on Windows that means no key and no
Piper), the video still builds, but without narration — music-only/silent,
as above.
With no voice provider available at all (no key and no Piper installed, which
on Windows means no `say` either), the video still builds without narration —
music-only/silent, with estimated beat lengths — and the missing narration is
noted in the final report. It never aborts on the first line for a missing voice.

MiniMax falls back to Piper, then `say`, **per line** if the API is unreachable — and then to any other usable voice, as above — so a run
never fails outright while a voice is available — and with no voice available
at all it skips narration and builds the video without it, as above. If a
provider passes preflight but fails at runtime and no fallback voice can
render a line, that line renders silent with an estimated length and the run
continues — the video never aborts on a voice failure.

### Voice direction — make it sound human

A natural voice is not a setting; it is a voice chosen for conversation
plus lines written to be spoken plus a sample listened to before the
batch. Do all three.

**Voice selection.** The default is ElevenLabs **Rachel**
(`21m00Tcm4TlvDq8ikWAM`, the voice id in `template/shots.example.json`
and the `tts.mjs` default). Rachel is the default because she is
ElevenLabs' long-standing natural conversational voice: a calm, clear
American delivery with ordinary sentence melody, no character affect,
and no newscaster polish — the closest thing in the library to a person
explaining a product to a colleague. That is why she reads a demo script
without sounding like a demo script. To pick an alternative, stay inside
the same class: a natural conversational voice from the ElevenLabs voice
library (warm, measured, adult, neutral accent), never a character,
whisper, or heavily stylised voice — and run the sample check below on
the alternative before committing to it. Record the chosen voice id in
`shots.json` (`tts.voice`); a voice change after sample approval needs a
new sample.

**Write lines to be spoken.** Short sentences (one clause each where
possible), light contractions ("it's", "here's"), clear punctuation,
one delivery idea per beat. Never list: "it does X, Y, and Z" read aloud
is a monotone inventory — split the list across beats, or say the one
item that matters and let the footage show the rest. Put the emphasis
word where a person would put it by writing the sentence around it
("Not a dashboard. A decision." lands; "it is not a dashboard but a
decision" does not). Pause policy: a short pause after a setup line, a
longer pause before a reversal or the one claim the video exists to
make — silence is structure, and a beat that rushes its own punchline
has no punchline.

**Pacing with `<break>` tags — model matters.** SSML `<break>` tags work on
the v2 family — the default `eleven_multilingual_v2`, `eleven_flash_v2`, and
`eleven_flash_v2_5` — up to 3 seconds per break. `eleven_turbo_v2_5` also
takes breaks but is deprecated: never recommend or select it;
`eleven_flash_v2_5` is the fast alternative when speed matters. v3/v4 models
do NOT support `<break>` tags — do not switch to a v3/v4 model expecting
breaks to work; on those, pace with punctuation, sentence length, and ellipses
instead. So: do NOT switch models just for pauses — the default
`multilingual_v2` takes `<break>` tags as written. Write breaks inline, for
example `...end of the setup. <break time="0.8s" /> Here's what it does.`
Rules: at most 3 seconds per break (`<break time="3.0s" />` is the ceiling);
one break per line at most, and only before a reversal, a number, or the
closing line — too many breaks sound theatrical and slow, and excessive breaks
can make the model speed up or introduce artifacts. Punctuation and short
sentences are pauses too: a period is a pause, a comma is a shorter one, a
paragraph break is a beat. Never use an ellipsis (`...`) as a pause mechanism
on the v2-family models — it can be vocalised as a word or sound. Piper and
`say` have no SSML: on those voices, punctuation and sentence length are the
only pacing tools.

**Voice settings — the documented defaults, verified in code.**
`scripts/tts.mjs` sends `stability` 0.5, `similarity_boost` 0.75,
`style` 0.0, `speed` 1.0 unless `shots.json` overrides them; those are
the values to use unless the sample check says otherwise. What each one
does to the sound: lower `stability` gives more variation and a more
expressive read (too low, and the voice wanders); `style` at 0.0 is
neutral — raise it modestly for a more expressive read; keep
`similarity_boost` high enough (around the 0.75 default) that the voice
still sounds like the chosen voice; `speed` runs 0.7–1.2, and 1.0 is the
natural rate — slow a line by rewriting it shorter, not by dropping
speed below ~0.9. The audible target: a person talking at a normal pace,
with variation between sentences, who sounds like the same person in
every beat. If the sample sounds flat, lower `stability` a little and
raise `style` a little, then re-sample — never change the voice, the
model, and the settings all at once, or you will not know which change
fixed it.

**Voice-sample check — one line before the batch.** Before synthesising
the full narration, generate ONE line — the hook, or the most
performance-sensitive beat — and listen to it. Confirm: it sounds like
a person, not a reader; the pace fits the footage; the emphasis lands
on the right word; product names are pronounced right. Only then run
the rest. If the provider, voice, speed, or model changes after sample
approval, take a new sample. A bad voice discovered after the full run
costs a re-render of every line; a bad voice discovered on one line
costs one line.

### The narration-key prompt — ask once, never block

When narration needs a key and none is set — no `ELEVENLABS_API_KEY` in
the environment, and no MiniMax credentials in the environment or an
env file — prompt the user **once**, at the point the demo video is
confirmed (right after grill-me, at the start of the build), so the
whole build is the work done meanwhile. **Invoker: orchestrate sends this
prompt at its step 0 (right after grill-me), using the wording below. In that
flow /demo never re-prompts; it uses the key if present and otherwise falls
back to music-only/silent (see below). When the user invokes /demo directly
(no orchestrate running), /demo sends it once at the point the video is
confirmed. Either way: ask once, never twice.** Say,
in one message:

- What the key is for: ElevenLabs narration for the demo video — the
  voice is the single biggest quality difference in the finished video,
  and without a key the video renders with a robotic fallback voice or
  music-only/silent.
- Where to get it: ElevenLabs free tier — 10,000 characters a month
  (about 10 minutes of audio, about 7 demo narrations), no credit card;
  sign up at elevenlabs.io, then the API key is on the free tier under
  the account / API-keys page. A 90-second demo narration is about
  1,300 characters.
- That the build continues regardless: the video will be built either
  way, and if the key arrives later a re-run of `npm run script`
  produces the narrated cut.

Rules: ask once, never twice, and never for MiniMax separately — the
single narration-key prompt covers it (if the user already has MiniMax
credentials in their environment or an existing env file, that same
reply is where they say so). Never block on the key: while waiting,
continue the build, and inside `/demo` do the storyboard, the shots,
the music, the video structure, and silent/placeholder narration, plus
final-report prep. At `/demo` time, use the key if it is present (env
var `ELEVENLABS_API_KEY` — or MiniMax credentials from the environment
or the user's existing env file); otherwise fall back to
music-only/silent and note the missing narration in the final report.

**Keys are env vars only.** The user provides the key in chat; the agent
uses it as an env var for the `tts` run only. Never write a key into any
file — not `shots.json`, not an env file, not the repo, not a log. The
`tts.envFile` mechanism only ever *reads* an env file the user already
has; it is never a place to store a key the user just gave you.

**Never copy an API key into the project.** `scripts/tts.mjs` reads
`MINIMAX_API_KEY` / `MINIMAX_GROUP_ID` from the environment, and otherwise parses
them out of whatever file `tts.envFile` names — an env file the user
already has, volunteered in the single narration-key prompt above, never
a file you write a key into.

A human recording beats any synthesiser: drop `<id>.wav` files into `public/vo/`
and run `npm run script` — it re-measures them and retimes the whole video.

## Music

`scripts/music.mjs` fetches the track named in `music.url` with yt-dlp and cuts
a bed to the current video length. `scripts/build.mjs` runs it right after
narration, so the bed is part of every full build. If the fetch fails (no
yt-dlp, no network, bad URL), the build logs a warning and the video renders
without a music bed rather than aborting — note it in the final report and
re-run `node scripts/music.mjs` once the track is reachable. **Tell the user to check the track's licence
before publishing** — library tracks are usually free with attribution in the
description and paid without it. The title and URL are saved to
`public/music/SOURCE.txt` so the credit is easy to copy.

## Don'ts

- Don't hand-tune timings. If a beat feels rushed, the narration is too long for
  the shot — fix `shots.json`, not the timeline.
- Don't put `<Screen />` inside a `<Sequence>`. It reads absolute time by design;
  `useCurrentFrame()` inside a Sequence returns Sequence-local frames. This has
  broken the video before and the symptom (footage subtly out of sync with the
  voice) is hard to spot.
- Don't let setup time end up on camera. Navigation, data loading and dismissing
  a banner all happen inside the shot's capture window and get stretched under
  the narration. Put `{"cut": true}` after the setup steps; the footage then
  starts from there.
- Don't film anything stubbed. If a button returns "connect the backend", leave
  it out and tell the user which shot to add once it is wired.
- Don't ship without checking the warnings list.
- Don't narrate a number you can see drifting between runs, and never describe a
  screen as full when this account's version of it is empty. A judge who spots
  one false claim discounts the rest.

## Modes

`/demo` films the app. That is the default and it stays the default. Two
OpenMontage modes are opt-in only: the agent offers them when they fit, and
asks the user before using either. A yes for one video does not carry over
to the next.

- **film (default)** — Playwright drives the real app and the edit is cut
  from measured narration, about 2 minutes to rebuild. Use this whenever
  the point is to prove the product works. The storyboard leads with the
  wow moment (see "Storyboard craft" in `SKILL.md`): the opening shot is
  the single most captivating thing the product does, stated as a
  concrete check before any other beat is written.
- **montage (opt-in)** — OpenMontage Documentary Montage: real archival and
  stock footage cuts (Pexels, Archive.org Prelinger, NASA, Wikimedia)
  chosen by CLIP retrieval against a thematic brief, for a mood or story
  piece. Offer it when the video needs to make someone feel something the
  screen recording cannot, for example the problem the product solves, or
  a story about the people it serves. Needs a thematic question, one tone,
  and a music plan. See `references/openmontage/montage.md` and
  `references/openmontage/documentary-montage.yaml`.
- **explainer (opt-in)** — OpenMontage animated explainer: research-first,
  scripted scenes (animated text cards, stat cards, charts, diagrams) for
  a concept or architecture story. Offer it when the thing to explain is
  an idea, not a screen, for example how the system works under the hood.
  It starts with a proposal (three concepts, itemised cost) that the user
  approves before anything is generated. See
  `references/openmontage/explainer.md` and
  `references/openmontage/animated-explainer.yaml`.

The screen-demo pipeline in `references/openmontage/screen-demo.md` is
what OpenMontage would do with a screen recording. This skill's film mode
already covers that ground better: it drives the app live with Playwright
instead of polishing a pre-recorded MP4, so prefer film and only reach
for the staged screen-demo notes if the user hands over existing footage.

## Narration — ElevenLabs free tier

`tts.provider: "elevenlabs"` is the no-MiniMax-key option with a real
voice. The `shots.json` block and the fallback chain are in
`references/shots-reference.md` under `tts`.

- The key comes ONLY from the `ELEVENLABS_API_KEY` environment variable.
  Never hardcode a key, never write one into `shots.json`, and never
  commit one.
- Free tier: 10,000 characters a month, about 10 minutes of audio, REST
  API only. A 90-second demo narration is about 1,300 characters, so
  about 7 demos a month free. Per-request limits are 10,000 characters
  for `eleven_multilingual_v2` and 40,000 for `eleven_flash_v2_5`;
  narration lines are far shorter, so this never bites.
- `scripts/tts.mjs` tracks use in `src/elevenlabs-usage.json` (month plus
  characters used). Before generating a line it checks the month's total;
  if the line would take it past 10,000, that line falls back to Piper
  instead. Check the remaining quota before starting a video and tell the
  user where it stands. Hand the usage remaining, the narration status per line-set, the `decision-log.md` entries, and the music credit (`public/music/SOURCE.txt`) to the final report via the /demo return — they are inputs to the report's demo-video handoff, not chat-only numbers.
- Free-plan audio is non-commercial. Anything published from it must
  credit "elevenlabs.io" or "11.ai" in the title, not just an end card or
  a description line. That is ElevenLabs' own wording, and an end-card
  credit alone does not meet it. If the video will be monetised or used
  commercially, use a paid plan instead.
- If the quota is exhausted or no key is set, the script falls back to
  local Piper TTS: the `piper` binary, zero keys (`pip install piper-tts`,
  then download a voice model; default `en_US-lessac-medium`). Piper is
  the no-key fallback on Windows, where macOS `say` does not exist. If
  Piper is missing too, it falls through to `say` (macOS only); with no
  voice available at all the run does not error — it preflights, finds
  nothing, skips narration, and builds the video music-only/silent (see
  Voice preflight above). Install Piper or set a key to get narration
  back on a re-run, rather than assuming a fallback exists. The chain
  exists so that one provider failing never kills the run while another
  voice is available.
- Voice settings that matter: `model` defaults to
  `eleven_multilingual_v2` (most reliable); `eleven_flash_v2_5` is faster.
  SSML `<break>` tags work on the v2 family — `eleven_multilingual_v2`,
  `eleven_flash_v2`, and `eleven_flash_v2_5` — so do NOT switch models
  just for pauses; `eleven_turbo_v2_5` is deprecated, never select it, and
  v3/v4 models do NOT support `<break>` tags. See the voice-direction section above for
  the break rules (max 3s per break, one per line at most, never an
  ellipsis as a pause on v2-family models). `stability` 0.5, `similarityBoost` 0.75,
  `style` 0.0, `speed` 1.0 are the defaults (verified against
  `scripts/tts.mjs`); lower stability and moderate style for a more
  expressive read, speed in 0.7 to 1.2. Generate one line and listen
  before batching the rest (the voice-sample check above).

## Budget governance — paid providers only

Free and local paths (Piper, stock footage, Remotion render) cost $0 and
need no approval. Anything paid (Runway, Veo, HeyGen, ElevenLabs beyond
the free tier, and similar) follows these rules — the skill's own budget rules, adapted from OpenMontage's cost-tracker design (the tracker script and config are not shipped in this plugin):

- Estimate the cost before spending, itemised per provider, and show it
  to the user with the cheaper alternatives next to it.
- Default cap: $10 per video. First paid use of a new provider needs
  approval even under the cap.
- Approval threshold: any single paid action estimated above $0.50 pauses
  for the user to approve. Keep 10% of the cap back for retries and
  re-renders.
- Decision log: record every provider choice and its cost in
  `decision-log.md` in the video project dir (provider, model, estimated
  cost, actual cost, why this provider). If a choice changes mid-run,
  append a new entry; do not edit the old one.
- OpenMontage's own per-pipeline defaults are lower ($1 for montage and
  screen-demo, $2 for explainer). Stay inside the $10 skill cap and
  inside the pipeline default for that mode unless the user approves more.

## OpenMontage licence note

The montage, explainer, and screen-demo material staged under
`references/openmontage/` is adapted from OpenMontage
(calesthio/OpenMontage), licensed AGPL-3.0. The licence text is kept at
`references/openmontage/LICENSE` and every staged file carries an
attribution header. That is fine for local hackathon use. AGPL is
stricter than MIT: if someone hosted a modified version as a service,
they would have to offer the source. Do not strip the headers.

---

Original by RoderickQiu (pitch-deck-video-skill), no license file, adapted for hackathon-ecc as pitch-deck-video: invoked as /demo via the demo command (Usage block updated from /pitch-deck-video), and the template path updated to the plugin location.
