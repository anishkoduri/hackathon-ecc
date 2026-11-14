# shots.json reference

The one file a human edits. Everything else is generated from it.

## Top level

| key | what it does |
| --- | --- |
| `brand` | Name on the closing card, and available to `textSwaps`. |
| `tagline` | The sentence left on screen at the end. |
| `theme` | `colors` and `fonts` for the cards and captions. Pull from the app's own tokens, and record the source (file + values) in `theme.source` — the QA fails the video if the theme is still the seed theme with no recorded source. `theme.vignette` (0–1, default 0.3) darkens the frame edges: set 0 for light apps and record the choice either way. |
| `tts` | Voice provider and settings. See below. |
| `music` | Background track and mix levels. Optional — delete the block to go without. |
| `gapMs` | Silence added after every line. 200–300 reads well. It counts toward the 2:10 total: measured narration + `gapMs` per beat + card durations + lead/tail — `qa.mjs` prints the total and flags over 2:10 as BLOCKING. |
| `app` | `url`, `width`, `height`, `bg`, `captureScale`, `storageState`, `loadingSelectors`. See below. |
| `textSwaps` | Capture-only copy patches. See below. |
| `cards` | Per-card config: `hook.accent`, `arch.title`, `arch.nodes`, `close.credits`. |
| `shots` | The video, in order. |
| `features` | One entry per must-have feature: `{name, beat}` — `beat` is the shot id that shows it. A feature is 'shown' only if it is visible on camera AND named (narration or caption) in its beat. See below. |
| `cuts` | Must-have features deliberately left out of the video: `{name, reason}`. A cut is a reported decision, never a silent omission — if the feature count would push the video past the 2:10 cap, cut the least important features here. |

## A shot

```json
{ "id": "plan", "kind": "app", "say": "…", "do": [ … ] }
```

- `id` — unique; also the narration filename (`public/vo/<id>.wav`).
- `kind` — `"app"` (footage) or `"card"` (full-screen graphic).
- `say` — one beat of narration. Its measured length *is* the scene length.
- `do` — only for `kind: "app"`.

A `card` shot needs a component registered under the same id in `CARDS` in
`src/Video.tsx`. The template ships `hook`, `arch` and `close`.

## features / cuts

From `docs/scope.md`'s must-have list plus every route screenshotted in step 3 (a route with no must-have feature behind it is not a feature).

```json
"features": [{ "name": "Automatic scheduling", "beat": "result" }],
"cuts": [{ "name": "Admin dashboard", "reason": "would push the video past the 2:10 cap; shown in the live demo instead" }]
```

One entry per must-have feature; `beat` is the shot id that shows it. `qa.mjs` prints the coverage table (feature → beat, plus the cuts list) and flags any feature whose beat id is missing from `shots.json` or whose beat produced no footage. If a feature is cut, say so in the final report.

## Actions

| action | example | notes |
| --- | --- | --- |
| `goto` | `{"goto": "/plan"}` | Clicks the app's own link if there is one, else `pushState`, else a real load. See below. |
| `goto` (hard) | `{"goto": {"to": "/x", "hard": true}}` | Forces a real page load. |
| `settle` | `{"settle": 15000}` | Waits out spinners, skeletons and DOM churn. |
| `cut` | `{"cut": true}` | Re-anchors the shot here; everything before it is setup and is not filmed. |
| `wait` | `{"wait": 800}` | Milliseconds. |
| `waitFor` | `{"waitFor": "text=Result"}` | Wait for an element, 6 s cap. |
| `click` | `{"click": "button:has-text(\"Start\")"}` | Glides the cursor in, presses, releases. |
| `hover` | `{"hover": "text=Career fair"}` | Moves the cursor without clicking. |
| `type` | `{"type": {"sel": "textarea", "text": "…", "delay": 9, "clear": true}}` | `delay` is ms per keystroke. |
| `type` (secret) | `{"type": {"sel": "input[type=password]", "env": "DEMO_PASSWORD"}}` | Reads the value from the environment so it never lands in a file. |
| `scroll` | `{"scroll": {"to": 620, "ms": 1100}}` | Window scroll, eased. `"to": "bottom"` works. |
| `scrollIn` | `{"scrollIn": {"sel": "text=Questions", "ms": 900}}` | Scrolls inside the nearest scrollable ancestor — drawers, panels. |
| `focus` | `{"focus": {"sel": "…", "pad": 300, "max": 1.7, "ms": 900}}` | Records a camera move. `{"focus": null}` pulls back out. |

### focus

The most useful action. It measures the element's box **at record time** and the
timeline zooms the footage to fit it plus `pad`, capped at `max`. Because the box
is measured rather than hardcoded, a layout change moves the shot instead of
breaking it.

Use it whenever text would be too small to read at 1080p — side panels, drawers,
dense lists. Always `{"focus": null}` before navigating away.

Zoom is limited by the taller dimension, so a tall narrow panel will not zoom
much. If it is still illegible, `scrollIn` to the part that matters.

### Selector notes

- `text=Foo` is a case-insensitive substring match, so it matches copy rendered
  uppercase by CSS `text-transform`. Write the selector however you like.
- `has-text()` matches the whole subtree, so `button:has-text("Room")` can hit a
  large ancestor. Scope it: `[role="dialog"] button:has-text("Room")`.
- A failing selector is logged to `capture/marks.json → warnings` and skipped.
  **Read that list after every run.**

### goto, and why it is three strategies

In order: click the app's own `<a href="...">` for the route (real router
navigation, no white frame); else `history.pushState` + `popstate`; else a real
page load. Each of the first two is only accepted if the **page content actually
changes** — a hash of the whole body text, not a prefix, because headers and
sidebars are identical across routes.

That check is not paranoia. Next's App Router updates the URL on `pushState`
**without re-rendering**, so a naive implementation films the previous page under
the next shot's narration and never errors.

`hard: true` when the app's own link opens something other than the route — a
modal or an overlay player rather than the standalone page you want on camera.

### cut

Everything a shot does happens **inside its capture window**, so navigating,
waiting for data and dismissing a banner all get stretched under the narration.
`{"cut": true}` re-anchors the shot at that point: the setup still runs, it just
is not filmed.

```json
"do": [
  { "click": "a[href*=\"/episodes/\"]" },
  { "settle": 20000 },
  { "wait": 900 },
  { "cut": true },
  { "focus": { "sel": "text=Transcript", "pad": 500, "max": 1.4 } }
]
```

Use it in any shot that begins with a load. It is the difference between a beat
that opens on a spinner and one that opens on the product.

### settle

Spinners and skeletons should never be on camera. After every navigation and
click the recorder waits until nothing matching `app.loadingSelectors` is
visible. The default list is `[aria-busy="true"]`, `[role="progressbar"]`,
`[data-loading="true"]`, `.animate-spin`, `.animate-pulse`, `.skeleton`.

Narrow it per app if you get `settle: still loading` warnings — apps use
`animate-pulse` decoratively, and an audio scrubber is often a permanent
`role="progressbar"`. `{"settle": 20000}` as an explicit step for a slow route.

**A page that renders its skeleton with the same labels as its loaded state will
pass `waitFor` too early.** Wait on something that only exists once the data is
in — a computed number, not a heading.

## cards — arch nodes

`cards.arch.nodes[]` is the real architecture: each node is `{label, note, kind}` where `kind` is `in` (input), `llm` (model call), `code` (deterministic code), or `out` (output) — plus an optional `stack` label: the concrete framework / model / service / infra that box runs on (e.g. `"Next.js 15"`, `"GPT-5"`, `"Supabase"`), taken from the app's `package.json` + `docs/decision-record.md` / `docs/scope.md`, never invented. `Arch.tsx` renders the stack label under each node label in mono. The arch beat's narration names the stack in one spoken phrase ("Built on Next.js, GPT-5, and Supabase") — one phrase, not a list read aloud.

## app

```json
{ "url": "http://localhost:5190", "width": 1920, "height": 1080, "bg": "#F6F1EB",
  "hideSelectors": [".debug-panel"],
  "storageState": "/path/to/.auth/user.json",
  "loadingSelectors": ["[aria-busy=\"true\"]", ".animate-spin"] }
```

- **`url`** is the **local** dev-server URL. `/demo` films the local app
  from the project directory — the video is made from the code, not from
  a link. Never set `url` to a deployed URL and never film a deployed
  product; deploying the app is a separate step and its URL goes in the
  final report, not in `shots.json`.

- **`width` / `height`** pin the capture exactly. The video is recorded at the
  same size, and the CSS viewport is never enlarged — a bigger viewport hands
  the app a different breakpoint, and a bigger video canvas does not scale the
  page up, it just pads it with grey. Nothing depends on the monitor you are
  sitting at; headless Chromium ignores it. There is no supported way to capture
  above the output resolution, so keep `focus` zooms at or below about 1.5 —
  beyond that you are upscaling 1080p.
- **`hideSelectors`** hides anything that is dev-only rather than product. Next's
  error and build indicators and Vite's error overlay are hidden by default.
- **`storageState`** is a Playwright storage state, so the recording starts
  logged in and no login flow is on camera. Many repos already save one for
  their own e2e tests — look for `.auth/*.json` before building a login shot.
- **`devCommand`** overrides how the app is started when nothing is serving
  `app.url`. `{port}` is substituted. Without it the app's own `dev` script is
  read and the right port flag inferred (Next, Vite, Remix, Nuxt, Astro,
  SvelteKit, CRA), with `PORT` exported for everything else.
- **`locale`** (default `en-US`) and **`colorScheme`** (default `light`) are
  pinned so the machine you record on cannot change what the video shows. Set
  `colorScheme: "dark"` for an app that follows the system preference.
- **`timezone`** is *not* pinned by default: forcing UTC can shift every date in
  the app by a day. Set it only when you need byte-identical reruns.

## textSwaps

Patches copy in the captured browser only — the app on disk is untouched.

```json
[ { "from": "[Product name]", "to": "Acme" },
  { "from": "Test User", "to": "Alex" },
  { "from": "T", "to": "A", "exact": true } ]
```

For placeholder names a prototype still ships, or a user who is called different
things on different pages. `exact` matches only text nodes whose trimmed value is
exactly `from` — use it for single letters like avatar initials, where a
substring swap would hit everything.

Leave a swap in as a safety net even after the app is fixed; it costs nothing and
catches a regression.

## tts

```json
{ "provider": "minimax", "voice": "Ukrainian_WiseScholar", "model": "speech-2.8-hd",
  "speed": 1.0, "languageBoost": "English", "envFile": "~/some/.env.local",
  "fallback": { "voice": "Samantha", "rate": 178 } }
```

`provider: "say"` skips the API entirely. Voice ids come from MiniMax's system
voice list; the language tag on a voice is a hint, not a restriction — a
Ukrainian-tagged voice reads English fine with `languageBoost: "English"`.

Clips cache on a hash of the voice settings plus the text, so editing one
sentence re-synthesises one clip.

**Provider fallback.** If the configured provider is missing, `tts.mjs`
resolves to the next available voice in the chain (ElevenLabs → Piper →
`say`; MiniMax → Piper → `say`; Piper → `say`; `say` → Piper → ElevenLabs), and if
the chain is exhausted it falls through to any other usable voice (ElevenLabs →
Piper → `say` → MiniMax) before skipping narration. Narration is skipped only when no usable voice exists
at all. If a provider passes preflight but fails at runtime and no fallback
voice can render a line, that line renders silent with an estimated length
and the run continues — the video never aborts on a voice failure.

### ElevenLabs (`provider: "elevenlabs"`)

```json
{ "provider": "elevenlabs", "voice": "21m00Tcm4TlvDq8ikWAM", "model": "eleven_multilingual_v2",
  "speed": 1.0, "stability": 0.5, "similarityBoost": 0.75, "style": 0.0,
  "piperModel": "en_US-lessac-medium" }
```

- `voice` is an ElevenLabs voice ID, not a name (Rachel is
  `21m00Tcm4TlvDq8ikWAM`). `model` defaults to `eleven_multilingual_v2`;
  `eleven_flash_v2_5` is faster. SSML `<break>` tags work on the v2
  family — `eleven_multilingual_v2`, `eleven_flash_v2`, and
  `eleven_flash_v2_5` — so do NOT switch models just for pauses;
  `eleven_turbo_v2_5` is deprecated, never select it, and v3/v4 models do
  NOT support `<break>` tags. Write breaks inline as needed; max 3s per
  break, one per line at most, never an ellipsis as a pause on v2-family
  models (see the voice-direction section in `SKILL.md`).
  `speed` runs 0.7–1.2.
- The key comes ONLY from the `ELEVENLABS_API_KEY` environment variable.
  Never put it in `shots.json` or an env file the project reads.
- Free tier: 10,000 chars/month (about 10 minutes). `scripts/tts.mjs`
  tracks use in `src/elevenlabs-usage.json` and switches a line to Piper
  before it would exceed the month's allowance. A 90-second demo is about
  1,300 chars, so about 7 demos a month on free.
- Free-plan audio is non-commercial and must credit "elevenlabs.io" or
  "11.ai" in the title of anything published from it. If the video will be
  monetised or used commercially, use a paid plan instead.
- Piper fallback: local `piper` binary, zero keys (`pip install piper-tts==1.8.0`,
  then download a voice model; default `en_US-lessac-medium`, voices live
  in `~/.piper/models`). If `piper` is missing it falls through to `say`
  (macOS only). On Windows, Piper is the no-key fallback.
- If a line fell back to Piper (quota or outage) and you later want the
  ElevenLabs voice for it, delete `public/vo/<id>.wav` and re-run; cached
  clips are not re-rendered.
- Voice selection (Rachel default, why it sounds natural, how to pick an
  alternative), delivery direction, and the one-line sample check are in
  `SKILL.md` under "Voice direction — make it sound human".

## music

```json
{ "url": "https://…", "credit": "Title — Artist", "start": 0, "fadeIn": 2.0,
  "gain": { "open": 0.34, "under": 0.14, "close": 0.30 } }
```

Use `"file": "~/Music/bed.wav"` instead of `url` for a local track — simplest,
and no licence ambiguity. `url` is fetched once with yt-dlp and cached.

`open` under the cold open, `under` beneath the narration, `close` for the last
cards. `scripts/music.mjs` cuts the bed to the current video length; it runs
as part of `scripts/build.mjs` right after narration. If the fetch fails the
build logs a warning and the video renders without a music bed rather than
aborting — `src/Video.tsx` skips the music `<Audio>` element when no
`public/music/bed.wav` exists (flagged in `src/vo-durations.json`). `under` above 0.20 risks burying the voice — `qa.mjs` warns on it, and the step-6 mix check (a 10-second listen from the middle of the video) is the confirmation; keep `under` at or below 0.20 unless the listen says otherwise.
