---
description: Generate a narrated 1–2 minute product demo video of the hackathon project. Use when the user wants a demo video, launch video, product walkthrough, or hackathon submission video.
---

<!-- Build note: place this file at hackathon-ecc/commands/demo.md so it is invoked as /demo. It loads the pitch-deck-video skill. -->

# Demo video

Use the pitch-deck-video skill to generate a narrated 1–2 minute product demo video of the app in the current directory, or of the app path given after /demo. Follow that skill exactly: scaffold its template next to the app, learn the app from screenshots before writing any narration, write shots.json, build, and QA by looking at the contact sheets — do not skip the QA step.

Pass through the arguments as the skill defines them:

- `/demo` — film the app in the current directory
- `/demo <path-to-app>` — film a specific app
- `/demo --rebuild` — re-record and re-cut an existing video project
- `/demo --script` — narration changed only; reuse the last take
- `/demo --render` — cards/captions changed only; re-render
