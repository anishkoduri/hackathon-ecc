---
name: pitch-deck-video
description: "Use when the user wants a demo video, launch video, product walkthrough, hackathon submission video, or screen recording of a local web app — especially if they say the video must be re-doable after the UI changes. Generates a narrated product demo, under 2:10, by driving the real app with Playwright and cutting the edit from measured narration, so a rebuild after a frontend change takes ~2 minutes and one command. Also offers two opt-in OpenMontage modes on request: montage (real archival and stock footage cuts) and explainer (scripted animated scenes). Film stays the default."
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

Before storyboarding, enumerate the feature list: every must-have from `docs/scope.md`'s must-have list, plus every route screenshotted above (a route with no must-have feature behind it is not a feature). Write the list into `shots.json` as a `features` array — `[{name, beat}]`, one entry per must-have feature, `beat` being the shot id that shows it — and a `cuts` array — `[{name, reason}]` for any must-have feature deliberately left out of the video. A feature is 'shown' only if it is visible on camera AND named (narration or on-screen caption) in its beat. If the feature count would push the video past the 2:10 cap (step 4), cut the least important features into the `cuts` array with a reason — a feature cut from the video is a reported decision, never a silent omission.

Use the screenshots to pick the best state per beat, not only to verify the wow: for each beat, the shot's state is the best-looking state that shows the claim — populated data, the prettiest route, the wow at its best. Never put an empty state on camera to stand for a full one (the Don't below stays: never describe a screen as full when this account's version of it is empty).

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
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

Start from `template/shots.example.json`. See `references/shots-reference.md`
for every field and action.

Pull the `theme.colors` from the app's own design tokens so the cards and the footage read as one piece, and record the token source (file + values) in `shots.json` as `theme.source` — the QA step fails the video if the theme is still the seed theme with no recorded source. Fill `cards.arch.nodes` with the real architecture — which boxes are model calls and which are deterministic code — and give each node its `stack` label: the concrete framework / model / service / infra that box runs on (e.g. `"Next.js 15"`, `"GPT-5"`, `"Supabase"`), taken from the app's `package.json` + `docs/decision-record.md` / `docs/scope.md`, never invented. That beat is what separates a demo from a wrapper, and judges look for it. Its narration must name the stack in one spoken phrase ("Built on Next.js, GPT-5, and Supabase") — one phrase, not a list read aloud (the 'Never list' rule stays). If the app has no recorded stack, the arch beat says the framework only and notes the gap in the final report.

Narration rules that matter:

- **12–16 beats; the video is under 2:10 (130 seconds) — hard rule.** The total is computed from the MEASURED narration durations (`src/vo-durations.json`), plus `gapMs` per beat and the card durations — never from estimates. Over 2:10 is a BLOCKING finding in QA: re-cut (shorten lines, drop a low-priority feature beat into the `cuts` array, tighten a beat). Absolute max 2:30 (150 seconds), never exceeded — no approval, no exception, no 'one more beat' may push a video past it; if a storyboard would exceed 2:30 even after cutting, re-cut it (fewer features, shorter lines), never extend it. Leave ~10 seconds of room. Lengths by artefact: the video is under 2:10; the live demo storyboard is 2–4 min; the pitch storyboard is <90s. Do not mix them up — the video cap governs this skill, the longer live-demo storyboard and the shorter pitch storyboard belong to the pitch, not the video.
**Write the time budget before writing the lines.** Before writing `shots.json`, write the section budget first, then write lines to fit it — never the reverse (writing lines and discovering the total afterwards). The 130-second budget is divided across the arc by importance, not evenly (times are narration + gaps for that section, in seconds):

| Section | Beats | Seconds | Why |
| --- | --- | --- | --- |
| Problem | 1 | 8–10 | The pain, in the user's words — short, sharp |
| Wow | 1–2 | 14–18 | The opening, the reason to keep watching — deserves time |
| Edge (uniqueness) | 1 | 8–10 | One sentence, the differentiator |
| How / features | 6–9 | 55–65 | The LARGEST share — every feature shown, the program proved |
| Proof (arch + stack) | 1–2 | 12–15 | Credibility beat, stack named aloud |
| Close | 1 | 6–8 | One sentence left on screen |
| Unallocated room | — | ~10 | The existing leave-room rule, kept |

Totals: 103–126s of content + ~10s room ≈ under 2:10. The features' share is the largest because the spare beats go to features (step 3). If a section's lines would exceed its budget, shorten the lines or move a feature to `cuts`; do not borrow from another section's budget without recording it in the final report.

- **One idea per beat.** The beat ends when the idea does.
- **Say the number.** "Six people scored, Priya wins" beats "it picks someone."
- **Never narrate the UI.** Not "here we click Approve" — say what it means.
- **Open on the problem in the user's words**, before the product name exists.
- **Close on one sentence** you want left on screen.

### Storyboard craft — lead with the wow moment
**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate.

The storyboard is the video's argument, and it opens with the single most
captivating moment of the product — the scoped wow moment from `docs/scope.md` (step 3), not a new one derived from the screenshots. Before writing any other beat, name it in one concrete sentence:
"the opening shot must show X doing Y" (for example, "the opening shot
must show the calendar filling itself the moment Priya picks a time").
If you cannot state the wow moment that concretely, you do not have a
storyboard yet — go back to `docs/scope.md` for the scoped wow, then to the screenshots to verify it renders on screen. The wow moment is beat
one, not the finale: a judge who is bored by beat three never sees beat
twelve.

The arc after the wow moment, in order:

1. **Problem** — one beat, in the user's words, before the product name exists. The pain, not the category.
2. **Wow** — the opening shot above: the product doing the impossible thing, live, with the number said out loud.
3. **Edge** — one beat, one sentence: the one thing no alternative does, in the user's words, with the alternative named or clearly implied ("unlike X, this…"). Shown live where possible — a `focus` on the differentiating element, or the wow footage carrying it. The Edge claim comes from `docs/decision-record.md` / `docs/scope.md` (the wow test: "does this make a judge stop and stare?") or from the user. If none is recorded, ask for one line; never invent a competitor claim — the fallback is stating the wow's distinguishing fact, not a fabricated comparison.
4. **How** — two to four beats along the golden path: one user, one task, each beat one action and one outcome. Never two features in one beat. PLUS one beat per remaining must-have feature from the `features` array (step 3), drawn from the 12–16 beat budget — the budget's spare beats go to features, not to padding the golden path. A feature counts as shown only if it is visible on camera AND named in its beat.
5. **Proof** — the arch card beat: which boxes are model calls and which are deterministic code, each node labelled with its stack, and the stack named aloud in one phrase. This is the credibility beat; judges look for it, and it is what separates a demo from a wrapper.
6. **Close** — one sentence left on screen (the tagline, said out loud).

Shot design per beat: one beat is one screen (or one `focus` move within
a screen). If a beat needs two screens, it is two beats. Any text that
would be illegible at 1080p gets a `focus` — a dense list, a side panel,
a drawer — and a `{"focus": null}` before navigating away. Pacing: at
12–16 beats under 2:10, a beat averages 7–9 seconds; a beat
whose line runs past ~12 seconds is two ideas and must be split. Cut
setup out of every beat with `{"cut": true}` after the navigation and
loading steps, so no beat opens on a spinner.

### 5 · Build

```sh
# POSIX / Git Bash
APP_DIR=/path/to/app npm run all
```

```powershell
# PowerShell (Windows)
$env:APP_DIR='/path/to/app'; npm run all
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

Check: **`capture/marks.json → warnings` is empty** (a missing selector is a warning, not a crash — you still get a video, and a list of what broke). Then read the `qa.mjs` printout and work through it in order:

- **Coverage table complete** — every must-have feature has a beat or a recorded cut (`shots.json` `features` / `cuts`). A feature whose beat id is missing from `shots.json` or whose beat produced no footage is a BLOCKING finding.
- **Per-beat A/V table** — for every shot, the claim in its `say` line against the stills: does the frame support it? Complete the table `qa.mjs` prints while reading the contact sheets and record it in the video project (qa notes). A 'no' is a BLOCKING finding: re-film or rewrite the line; the video does not ship with an unmatched claim. Kinetic type and camera moves go IN this table as rows of their own (a kinetic title is a claim the frame must support; a camera move is a claim about what the frame shows).
- **Anti-slide checks** — the motion-graphics layer section below: one continuous world, a moving camera, a persistent subject, numbers inside the scene, at most two text levels, varied transitions, no text under 30px on a 1080-wide stage. A 'no' on any check is BLOCKING: re-cut the composition, never ship a slide deck with fades.
- **Gorgeousness** — (a) no generic seed look: the cards read as the app's own palette/fonts, not the seed theme; (b) footage shows the app's best-looking states: populated data, the prettiest route, the wow at its best, chosen from the step-3 screenshots — never an empty state on camera; (c) vignette matches the app: `theme.vignette` 0 for light apps, recorded choice either way.
- **Runtime** — `qa.mjs` prints the total from the measured narration; over 2:10 is BLOCKING (re-cut), and 2:30 is the absolute ceiling no version may cross.
- **Mix** — listen to a 10-second sample from the middle of the video (where the music is `under` the voice) and confirm the narration is intelligible over the bed; record the check. `qa.mjs` warns if `music.gain.under` exceeds 0.20 — above that the bed risks burying the voice.
- **Theme pulled, not seeded** — the theme check fails the QA if `shots.json` still carries the seed theme with no recorded `theme.source`.

Then the stills themselves: does each caption land on a frame that supports it? Any blank or white frames? Is small text legible, or does it need a `focus`?

`references/troubleshooting.md` has every failure this pipeline has actually hit
and the fix for each. Read it before debugging from scratch.

### 7 · Link the video into the README (fix #26 F-14, README_UPDATE_F26)

A /demo run usually happens AFTER the first build's README and final report
already exist — orchestrate step 6 writes the README before any video is
filmed, because /demo runs only on explicit invocation (fix #22 gate). So
the /demo run itself links the video into the README once QA passes and
`out/demo.mp4` exists. No re-run of readme-writer, no re-run of the README
step, no new gate, no approval: this is a mechanical edit inside /demo's
own run, and /demo still runs only when the user invokes it explicitly.

The video path is repo-relative from the project root:
`<app-name>-video/out/demo.mp4` — the same path readme-writer reads from
the ledger in a first build. The README links that file path (committed,
it plays on the repo host); the video is never uploaded from here — the
hosted-URL swap (YouTube/Vimeo, paste into Devpost) stays the user's step
from the final-report handoff.

1. **Record it in the ledger first.** Write (or update) the line
   `demo video: <app-name>-video/out/demo.mp4` in
   `.hackathon/run-ledger.md`, so a later readme-writer run reads the
   video path from the ledger per its Step 2.
2. **Update the README — first match wins, and the edit is idempotent:**
   a. If the README already links this video path, do nothing.
   b. Else if it carries a video placeholder — the
      `<!-- 🎥 Demo video: ... -->` comment or a `TODO: add demo link` /
      `TODO: add video` marker — replace the placeholder with the real
      link, keeping the surrounding badge-button markup.
   c. Else if it has the readme-writer house-style badge-button block
      (`**Live demo:**` followed by a `<p align="center">` button row),
      add a matching Demo Video button to that row:
      ```html
      <p align="center">
        <a href="<app-name>-video/out/demo.mp4">
          <img src="https://img.shields.io/badge/Demo%20Video-000000?style=for-the-badge" alt="Demo Video"/>
        </a>
      </p>
      ```
      plus the `<!-- 🎥 Demo video: <app-name>-video/out/demo.mp4 -->`
      comment line beside it, per the readme-template convention.
   d. Else insert a `## Demo video` section carrying the link, directly
      after the title block (the first `# ` heading plus its tagline
      blockquote, if any); if the README has no `# ` heading, put the
      section at the top.
3. **No README, no README written.** If no `README.md` exists at the
   project root, do NOT write one — authoring a README is readme-writer's
   job, not /demo's. Record the video path in the /demo return instead,
   so the user can run readme-writer.
4. **Re-cuts are a no-op.** `--rebuild`, `--script`, and `--render`
   re-run this step too; the path is unchanged, so rule 2a applies and
   the README is left untouched.
5. **The final report is not rewritten here.** The report is
   orchestrate-owned and point-in-time; the /demo return carries the
   video path as the handoff input for it, but /demo does not edit
   `docs/final-report.md`.

## Motion-graphics layer — one continuous world, not slides (Bang Motion port, fix #22 §12)

Ported — distilled, in English — from Bang Motion, an agent skill that turns a
coding agent into a motion designer. **Source pin (verified live Nov 12,
2026):** repo `https://github.com/bangtutorial/bang-motion`, MIT licence,
commit `c1aa65e921c970d858705fcb4a53a8294d1a4131` (current HEAD; 3 commits, all
dated Sep 15, 2026; created Sep 5, 2026; no GitHub release or tag — the
`1.19.0` version exists only as a badge/manifest version). Upstream's own
output loads GSAP 3.12.5 and Three.js 0.161.0 from jsDelivr and fonts from
Google, and does not play offline. **Staleness caveat, not a blocker:** the
repo has been quiet since Sep 15, 2026 — one open pull request (a second-output
proposal, unmerged since Sep 23, 2026) and one open issue. The rules below are
ported into this skill; the repo is not a live dependency and needs no upstream
updates. **Language note:** upstream's README is in English; its SKILL.md
(~39 KB, ~10k tokens), changelog, and most reference files are in Indonesian
— the port is in English. **Explainer-count resolution:** upstream's subtitle
says five explainer styles, but its README lists six, each with its own
starter — six is the true count; the port lists six.

**Boundary — film stays film.** `/demo` films the LOCAL app from the project
directory via Playwright; the deployed-URL path stays removed. These rules
govern the motion-graphics layer only: the opener, the transitions between
beats, kinetic title/hero text, and the close. The How/features beats stay
filmed footage of the real app, and motion graphics never replace feature
coverage (FILM_F1). A composition that replaces filmed app footage with generated
motion graphics FAILS QA.

The ported rules below are grouped under six tokens: anti-slide checks (BANG_ANTISLIDE_F22), one-world / camera / persistent-subject architecture (BANG_ONEWORLD_F22), the style-direction menu (BANG_STYLES_F22), opener concepts (BANG_OPENERS_F22), kinetic typography (BANG_KINETIC_F22), and explainer styles (BANG_EXPLAINER_F22).

**No second toolchain.** Bang Motion's output is a vanilla `index.html` plus
GSAP and Three.js; this skill's output is Remotion (React) plus OpenMontage.
Port the RULES into this skill's Remotion compositions (`template/src/scenes/`,
`template/src/parts/`) — do not import a second video pipeline, and do not add
a separate motion skill. (Upstream's own Remotion-output proposal has sat
unmerged since Sep 23, 2026 — there is no upstream Remotion output to import.)

**Pinned versions, never unpinned latest.** The plugin pins **GSAP 3.15.1** (GreenSock Standard "no charge" licence — free, all plugins included; NOT MIT) for all GSAP use, §11 and §12 alike — GSAP converges on this ONE pinned version. Bang's reference implementation used GSAP 3.12.5 / Three.js 0.161.0; those are Bang's versions as found, not the plugin pins. Three.js is scoped, not single-version: Vanta scenes pin `three@0.134.0` (the README-documented pair), general hand-written three.js scenes keep the existing pin `three@0.185.1`; Bang's 0.161.0 is recorded here as Bang's version only, not a plugin pin (this supersedes the earlier alignment flag expecting one three.js version — see fix22 integrator report: the scoped pins are deliberate per §11, libraries-report D3–D4). Vendor locally where the build is offline-first, and keep fonts self-hosted and static (fix #19/#21) — no unpinned CDN loads in the video project.

### Anti-slide checks (BANG_ANTISLIDE_F22)

Structural checks the agent verifies in its own composition code, alongside
the `qa.mjs` checks in step 6. A 'no' on any check is BLOCKING.

1. **One continuous world** — the video is one world, not slides with fades.
   Beats change because the world or the camera moves, never because a section
   fades out and another fades in.
2. **A camera that actually moves** — push-through → glide → settle, or a
   flowing world with parallax. A static frame with a fade is a slide.
3. **A subject that persists** — the hero (the product, or its hero element)
   stays on screen across scenes; it is carried through the transitions, not
   replaced by a new frame.
4. **Numbers live inside the scene** — a stat is part of the world (on the
   device, in the environment, attached to the subject), never a floating
   overlay on top of it.
5. **At most two text levels per frame** — a headline plus at most one
   supporting line. A third level means the beat is two ideas: split it.
6. **Varied transitions, never the same fade twice** — at least two transition
   types across the video, one of them with real depth (a camera move through
   depth, not a flat block wiping the frame). The background is layered, never
   flat. Motion runs every second — no dead stills between beats.
7. **No text under 30px on a 1080-wide stage** — the smallest on-screen text
   in the motion-graphics layer is 30px at 1920×1080 render width. Smaller
   text gets a `focus` (step 4) or is cut.

D19 reason — Motion: a moving camera and a persistent subject are what make
the video read as a film rather than a deck; Theme: the world is built from
the app's own theme, so continuity is brand continuity; Texture: none — these
checks govern structure, not surface treatment; Visuals: numbers inside the
scene and two text levels keep every frame readable at a glance; Techniques:
checks are verified in composition code, the same standing as the `qa.mjs`
checks; Colors: none — no color decision is made by these checks.

### One-world / camera / persistent-subject architecture (BANG_ONEWORLD_F22)

Build the Remotion composition as **one world the camera travels through**,
not a sequence of independent slides. The opener, Edge, and close beats are
built this way: the camera pushes through the opening world, glides to the
Edge claim, and settles on the close sentence, with the product (or its hero
element) persisting as the subject throughout. The filmed How/features beats
stay filmed footage — the one-world architecture governs how the composition
moves *between and around* them (the camera carries the viewer out of the
opener into the first filmed beat and back out to the close), not the footage
itself. If a beat cannot be reached by a camera move from the previous beat,
the composition is slides: re-block it.

D19 reason — Motion: one world plus a travelling camera is the architecture
that makes the anti-slide checks pass structurally instead of by inspection;
Theme: the world is the app's theme made spatial, so the theme deal decides
its look; Texture: none — texture is a surface decision inside the world, not
the architecture; Visuals: a persistent subject gives the eye one thing to
follow across the whole video; Techniques: implemented in the Remotion
composition (`template/src/scenes/`), camera moves driven by measured
element boxes where the filmed app is involved; Colors: none — the palette
comes from the theme, not the architecture.

### Style-direction menu, 10 (BANG_STYLES_F22)

A menu, never defaults. The look comes from the build's brand and theme deal
(fix #20 B1 + Taste), never from a template or a starter. Consult the menu;
the theme decides. Each direction is a skin: background, typography, signature
motion.

| Direction | Signature motion |
| --- | --- |
| Cinematic dark | push-through, light in front of the lens |
| Poster color-block | block wipes, text slamming the frame edge |
| Editorial light | calm slides, lines that draw |
| Paper & print | objects flying in and landing |
| Retro / analog | controlled glitch, rough zoom, freeze |
| Brutalist mono | hard cuts, shifting blocks, blinking cursor |
| Pastel playful | elastic bounce, blooming shapes |
| Luxury dark | slow motion, sweeping light, depth |
| Flat pop with photos | cutouts popping in, brand fields snapping on the beat |
| Grainy gradient | layers opening, camera travelling through the shapes |

A composition that uses a style direction with no theme/brand reason FAILS
QA — the direction must be traceable to the dealt theme in
`docs/design-tokens.md`, with a D19 reason.

D19 reason — Motion: each direction carries its signature motion, so the
choice of look is also a choice of how the video moves; Theme: the direction
is chosen to match the dealt theme, never because it is trending; Texture:
none — texture treatments come from less-flat-ui, not from the style menu;
Visuals: the menu keeps ten distinct looks apart so videos stop looking the
same; Techniques: menu entry recorded as a directive (direction + exact
tokens), per §10; Colors: the palette is derived from the brand, never
inherited from a starter.

### Opener concepts, 19 (BANG_OPENERS_F22)

A concept menu for the opener (Wow) beat — chosen through the design package,
theme-matched, with a D19 reason recorded. One line each; the concept is a
structure, never a script to copy.

1. One continuous shot — the camera never cuts through the opening.
2. Pure typography — the tagline carries the opener alone.
3. Problem → gone — the pain, then it vanishes.
4. Before / after — the old way, then the product way.
5. Journey inside the UI — travel through the app's own interface.
6. Product macro — extreme close-up on the product or its craft.
7. Object metaphor — an object stands in for the idea (security, cloud,
   finance).
8. Living number — a milestone or performance figure, alive in the scene.
9. One feature, fully demoed — the single clear edge, shown end to end.
10. Diegetic question → answer — a question asked inside the world, answered
    by the product.
11. Rhythmic collage — cuts on the beat, music-led.
12. Logo as stage — the logo shape is the stage the opener plays on.
13. Object relay — an object passed along a chain (delivery, marketplaces).
14. Brand system showcase — the brand's own system on display.
15. Claim → how → result — the claim, the mechanism, the payoff.
16. Living UI ecosystem — the product's workflows as one living system.
17. Flat pop with photos — photo cutouts and brand fields, campaign energy.
18. Through the gradient shapes — travel through glowing shapes.
19. Product tour with claims — the tour, with each claim said out loud.

D19 reason — Motion: the concept decides how the opener moves before a frame
is built; Theme: the concept must fit the dealt theme — a brutalist concept
on a luxury theme fails the match; Texture: none — texture is applied inside
the chosen concept, not chosen by it; Visuals: a concept menu stops every
opener from being the same push-in on a logo; Techniques: concept recorded as
a directive (concept + exact beats and timings), per §10; Colors: none — the
palette comes from the theme, not the concept.

### Kinetic typography (BANG_KINETIC_F22)

Kinetic type for title/hero text in the video: text that moves as part of the
scene, not static titles. Direct it per §10 — every kinetic moment is a
directive with effect + exact parameters, never prose: effect name, duration,
easing, distance or scale, and a settle hold. Techniques, distilled:

- **Word slam on the beat** — a word lands on a music beat (scale 1.15 →
  1.0, 120ms, ease-out), then holds still.
- **Split-text reveal** — the line splits into words; words enter staggered
  40ms apart from below (24px rise, 200ms, ease-out).
- **Mask reveal** — the line is uncovered by a moving mask (300ms,
  ease-in-out), left to right.
- **Scale pop** — the key word pops (scale 0.9 → 1.0, 180ms, ease-out) while
  the rest of the line stays put.
- **Letter stagger** — letters enter one by one (30ms stagger, 12px rise)
  for the close sentence only, never for a line the viewer must read fast.

Rules: kinetic type only on title/hero text — the opener, the Edge claim,
the close sentence. Text **settles fully still before its hold** so it can be
read; a line that is still moving while the viewer reads it fails. Never
kinetic type over filmed footage while the narration carries a claim — the
footage is the claim there. Every kinetic move and every camera move goes IN
the per-beat A/V table (FILM_F5). The opener is a beat inside the 130-second cap,
never extra runtime (FILM_F6): a Bang-style opener earns its seconds from the Wow
budget in step 4, it does not extend the video.

D19 reason — Motion: kinetic type is motion applied to the words themselves,
so the title is part of the scene's movement; Theme: the effect and its
parameters match the dealt theme's motion character (a luxury theme does not
slam words); Texture: none — kinetic type is type in motion, not a surface
treatment; Visuals: type that moves on the beat is what the eye remembers
after the video ends; Techniques: directed per §10 (effect + exact
parameters), verified in the A/V table; Colors: none — the type color comes
from the theme palette, not the effect.

### Explainer styles (BANG_EXPLAINER_F22)

Six styles, each with its own upstream starter. They inform the motion
treatment of the explainer/How beats — how a how-it-works beat moves — not a
second output format. `/demo` stays Remotion; no explainer is ever built as a
separate video.

| Style | How it treats a How beat |
| --- | --- |
| Continuous action | one subject that never leaves; the camera changes viewpoint instead of cutting |
| Cartoon collage | flat cutouts and handwriting on cream paper; the beat is assembled, not filmed |
| Visual journalism | real photos with source tags, highlighter, dashed annotations — evidence on screen |
| White catalog | white grid, product cutouts, mixed typography — the feature as a catalogue entry |
| Vintage sketch | sepia paper, engraving art, classic serifs — the story as history |
| Cartoon stage | one living stage per scene, jointed characters, no captions — the beat is played, not told |

Use a style only where the beat is an idea being explained (the arch/proof
beat, a concept beat) — never to restage filmed app footage. The style choice
is theme-matched with a D19 reason, like every other motion decision.

D19 reason — Motion: each style is a way of moving through an explanation,
so the style is a motion decision; Theme: the style must match the dealt
theme — visual journalism on a pastel playful theme fails the match;
Texture: none — texture treatments come from less-flat-ui, not the explainer
style; Visuals: the styles keep explanatory beats from all looking like the
same card carousel; Techniques: style recorded as a directive (style +
which beats it governs), per §10; Colors: none — the palette comes from the
theme, not the style.

## Re-cutting after the UI changes

This is the point of the whole thing.

```sh
# POSIX / Git Bash
APP_DIR=/path/to/app npm run all
```

```powershell
# PowerShell (Windows)
$env:APP_DIR='/path/to/app'; npm run all
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
  local Piper TTS: the `piper` binary, zero keys (`pip install piper-tts==1.8.0` — POSIX; on Windows PowerShell: `py -m pip install piper-tts==1.8.0` or `.tools\Scripts\pip install piper-tts==1.8.0` —
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
