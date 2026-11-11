<!-- Adapted from OpenMontage (https://github.com/calesthio/OpenMontage), AGPL-3.0. See LICENSE in this directory. -->

# Screen Demo (OpenMontage pipeline — reference only)

Source: OpenMontage `pipeline_defs/screen-demo.yaml` (v2.1, production,
staged verbatim here) and `skills/pipelines/screen-demo/*.md`,
condensed. Full director skills are NOT staged; fetch them at runtime
if needed (see `runtime-fetch.md`).

## What it is

A pipeline for turning an existing screen recording into a polished
demo video. Budget default $1.00, max wall time 10 minutes.

## How it relates to this skill's film mode

This skill's film mode already covers this ground better for a live app:
it drives the app with Playwright and cuts the edit from measured
narration, so a rebuild after a frontend change takes about 2 minutes.
OpenMontage's screen-demo instead starts from a finished MP4 and
polishes it. Prefer film. Reach for these notes only when the user hands
over existing footage, or asks for a terminal/install-flow demo that
film mode does not cover.

## Two production modes

| Mode | Source material | Pick when |
| --- | --- | --- |
| `real_capture` | An actual screen recording (MP4) via `screen_recorder`, `cap_recorder`, or `playwright-recording` | Real app UI, live behaviour, browser flows, IDE plugins, the user asked for their own screen |
| `synthetic_terminal` | None. A `terminal_scene` cut authored for Remotion: typed commands, scrolling output, floating command pills, blinking cursor | CLI / terminal / install flow / make targets / git clone / API key config; anything scriptable where every command and output is predictable |

Decision question: "Can I predict every command and its output before
shooting?" Yes means synthetic, no means real capture. Record the mode
in `brief.metadata.production_mode`.

## Stages

| Stage | Does | Approval gate |
| --- | --- | --- |
| idea | brief: what the recording demonstrates, target platform and duration, callout strategy, production mode + runtime lock | yes |
| script | transcribe any voiceover (`transcriber`), annotate key UI actions with timestamps, sections aligned to workflow steps | yes |
| scene_plan | zoom-crop regions for key moments, callout positions that do not obscure important UI (`frame_sampler`) | yes |
| assets | subtitles (`subtitle_gen`), callout overlays, cleaned audio (`audio_enhance`), optional narration (`tts_selector`) | yes |
| edit | smooth minimal zoom-crops, dead time trimmed or sped up, callout timing matched to narration | no |
| compose | `video_compose` + `audio_mixer`; runtime must match the idea stage | no |
| publish | metadata, chapter markers, export bundle | yes |

## Rules worth keeping

- Prioritise procedure over theory; one workflow, one outcome.
- Default to the shortest duration that still teaches the task: 30-60s
  for a quick tip, 60-120s for a focused walkthrough, 120-300s for a
  chaptered tutorial. Do not preserve raw duration by default.
- Use YouTube/LinkedIn for dense desktop UI; 9:16 only if the active
  area survives a narrow crop.
- Runtime by mode: real capture allows Remotion (preferred, mixes
  capture with overlays) or ffmpeg (pure concat/trim); synthetic
  terminal is Remotion only; a synthetic custom-HTML UI demo allows
  Remotion or HyperFrames, presented as a real choice.
- Synthetic terminal pacing rule: pace commands across the full scene.
  An earlier render burned through all commands in 40% of the scene
  time and then froze for the remaining 60%.
- Inspect the source before writing the brief: `frame_sampler` for
  representative frames, `scene_detect` for window switches,
  `transcriber` for whether the recording has narration, system audio,
  or silence. If there is no voiceover, downstream stages must know
  immediately.
