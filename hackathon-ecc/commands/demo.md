---
description: Generate a narrated product demo video, under 2:10, of the hackathon project. Use when the user wants a demo video, launch video, product walkthrough, or hackathon submission video.
---

<!-- Build note: place this file at hackathon-ecc/commands/demo.md so it is invoked as /demo. It loads the pitch-deck-video skill. -->

# Demo video

Use the pitch-deck-video skill to generate a narrated product demo video, under 2:10, of the app in the current directory, or of the app path given after /demo. Follow that skill exactly: scaffold its template next to the app, learn the app from screenshots before writing any narration, write shots.json, build, and QA by looking at the contact sheets — do not skip the QA step — then link the video into the README per the skill's step 7 (README_UPDATE_F26), so a /demo run after the final report does not leave the README stale.

/demo films the local app from the project directory. The video is made from the code, not from a link: never set `shots.json` `app.url` to a deployed URL, and never film a deployed product. Deploying the app is a separate step; its URL goes in the final report, not in `shots.json`.

When narration needs a key and none is set, the skill's narration-key prompt applies. **Direct invocation** means the user typed `/demo` at the prompt (not a `/demo` dispatched from a run — a dispatched `/demo` never prompts, see below): if the user invoked /demo directly, prompt the user once, at the point the video is confirmed, for the ElevenLabs key (free tier, 10,000 chars/month, no credit card), and keep building meanwhile. If this /demo run was invoked with a narration key already provided (via the dispatch's Environment field as an `ELEVENLABS_API_KEY` env instruction), do NOT prompt again — run the `tts` step with that variable set in the process environment. If the dispatch carries no key, check the environment once for `ELEVENLABS_API_KEY`; if present, use it, else fall back to music-only/silent. Never prompt on a dispatched run. Never ask twice, never ask for MiniMax separately, never block on the key. Keys are env vars only, never written to any file.

Pass through the arguments as the skill defines them:

- `/demo` — film the app in the current directory
- `/demo <path-to-app>` — film a specific app
- `/demo --rebuild` — re-record and re-cut an existing video project
- `/demo --script` — narration changed only; reuse the last take
- `/demo --render` — cards/captions changed only; re-render
- `/demo --montage` — same demo, but cut as an OpenMontage documentary montage (real archival/stock footage) instead of filming the app; opt-in, ask the user first
- `/demo --explainer` — same demo, but as a scripted OpenMontage animated explainer; opt-in, ask the user first

## `--rebuild`, and the plain-`/demo` rule

`/demo --rebuild` re-records and re-cuts an existing video project: it locates the existing `<app-name>-video/` directory next to the app, skips the scaffold step entirely, and reuses the project's edited `shots.json` as-is. Never run plain `/demo` over an existing video project — plain `/demo` scaffolds a fresh project, and re-scaffolding over an existing directory would copy the template's seed `shots.json` over the edited one. On an existing project, always use `/demo --rebuild`, and never copy the template's seed `shots.json` over an edited one.

The skill offers three modes: film (default), montage and explainer (both opt-in — ask the user before using either).
