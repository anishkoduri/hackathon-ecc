<!-- Adapted from OpenMontage (https://github.com/calesthio/OpenMontage), AGPL-3.0. See LICENSE in this directory. -->

# Animated Explainer (opt-in mode)

Source: OpenMontage `pipeline_defs/animated-explainer.yaml` (v2.0,
production, staged verbatim here) and
`skills/pipelines/explainer/*.md` (research, proposal, script, scene,
asset, edit, compose, publish directors) plus
`skills/meta/voice-performance-director.md`, condensed. Full director
skills are NOT staged; fetch them at runtime if needed
(see `runtime-fetch.md`).

## What it is

A fully AI-produced explainer video from a topic: researched, scripted,
narrated, and animated (motion-graphics scenes, not filmed footage).
Budget default $2.00, max wall time 20 minutes.

## When to offer it

When the thing to explain is an idea, not a screen: a concept, how the
system works under the hood, an architecture story. Ask the user first;
film stays the default.

## Stages

| Stage | Does | Approval gate |
| --- | --- | --- |
| research | map the landscape (at least 3 existing pieces), at least 3 data points, at least 3 genuinely different angles, at least 5 cited sources | no |
| proposal | 3+ concept options, mood board, runtime selection, itemised cost estimate; user approves before anything is generated | yes |
| script | hook, setup, build, climax, landing; word count within 10% of the duration target; one enhancement cue per 8-10s | yes |
| scene_plan | full script duration covered, no gaps; at least 3 different scene types; every asset uses a tool from the production plan | yes |
| assets | narration + visuals generated; total cost within the approved budget | yes |
| edit | cuts reference valid assets, subtitles on, music ducked, no timeline gaps | no |
| compose | Remotion or HyperFrames render (must match the proposal; a silent swap is a critical governance violation), audio mix | no |
| publish | metadata, chapter markers, export bundle | yes |

## The proposal is the whole point

Nothing downstream runs until the user approves the proposal. Present
concepts progressively (research summary, then mood board, then concept
options) and let the user mix elements across concepts. Each concept
must be genuinely different in insight, not just title: different
narrative structure (myth-busting, problem/solution, data narrative,
comparison, timeline, journey, analogy, debate, tutorial, story),
different hook pattern, grounded in different research findings. At
least one concept should take a creative risk.

Runtime selection is part of the proposal: present BOTH Remotion and
HyperFrames with brief-specific analysis when both are available,
recommend one, wait for approval, and log the choice. Remotion fits
when the scene stack is text cards, stat cards, charts, and spring
transitions; HyperFrames fits kinetic typography and custom HTML motion
graphics; word-level/karaoke captions force Remotion. For
reference-driven work, produce a 10-15 second sample (hook + one middle
scene, real voice, real style, music snippet) and get it approved
before the full production.

## Cost estimate (itemised, shown before approval)

Show per-item costs, the budget cap, and headroom for revisions. If over
budget, list specific savings. OpenMontage's indicative prices:

| Choice | Premium | Standard | Free |
| --- | --- | --- | --- |
| TTS | ElevenLabs $0.18-0.30 | OpenAI TTS $0.05-0.15 | Piper local $0.00 |
| Visuals | AI video clips $0.10-0.50/clip | AI images $0.02-0.04/image | Diagrams/code $0.00 |
| Music | music_gen $0.10/track | — | user library $0.00 |

Production paths: Premium ~$1.50-2.50, Standard ~$0.50-1.00, Budget
~$0.05-0.15, Free $0.00. If Remotion is available, design scenes around
its animated components (text_card, stat_card, chart, callout,
comparison, kpi_grid) instead of generating an image per scene: cheaper
and higher quality than Ken Burns pan-and-zoom.

## Script and voice

Write spoken language, not essay language: short sentences, light
contractions, clear punctuation. Carry a concrete `voice_performance`
plan from script to assets (performance intent, pacing profile, energy
curve, pause policy, per-section delivery cues with pace, energy,
emphasis words, and pause timings), never just "read naturally".
ElevenLabs: lower `stability` and moderate `style` for expressive
narration, `speed` in 0.7-1.2, `similarity_boost` high enough to keep
the voice. Sample gate: generate a sample from the most
performance-sensitive section, listen, adjust, then batch. If the
provider, voice, speed, or model changes after sample approval, take a
new sample.

The voice performance plan, in full (from OpenMontage's
`skills/meta/voice-performance-director.md` — the film mode's
voice-direction section in `SKILL.md` is the same plan applied to
`shots.json` narration):

```json
{
  "performance_intent": "Warm, decisive product narrator with human pauses.",
  "pacing_profile": "conversational",
  "energy_curve": "measured hook, warmer middle, more deliberate close",
  "pause_policy": "Use short pauses after setup lines and longer pauses before reversals or important claims.",
  "provider_notes": {
    "elevenlabs": "Use lower stability and moderate style for expressive narration."
  }
}
```

Per-section delivery cues (one delivery idea per section — if a section
needs three emotional turns, split it):

```json
{
  "pace": "measured",
  "energy": "curious",
  "emphasis_words": ["not", "process"],
  "pause_before_seconds": 0.2,
  "pause_after_seconds": 0.7,
  "delivery_note": "Set up the contrast, then slow down on the final phrase.",
  "provider_text": "This is not just another tool. <break time=\"0.6s\"/> It is a process."
}
```

Writing rules: use silence as structure — a pause before reversals,
after surprising claims, and before the final takeaway. Keep pause tags
purposeful: too many breaks sound theatrical and slow. Never leave a
direction as just "natural", "engaging", or "expressive" unless it is
paired with exact pace, emphasis, pause, or energy cues.

Sample gate, in order: generate the sample from the most
performance-sensitive section, not automatically the first; verify voice,
pace, pauses, emphasis, and emotional arc; if the sample is flat, adjust
the `voice_performance` plan or provider settings before generating the
rest; record the approved sample path and provider settings in the asset
manifest. Quality failures: a narration-led script with no
`voice_performance` plan; section directions that only say "read
naturally"; a provider, voice, speed, or model change after sample
approval without a new sample; final narration generated from raw script
text while structured `provider_text` or `delivery_cues` were present.

Word count is the pacing budget: TTS pacing is fixed, so count the
words — 250 words for a 60-second video is the failure case, either the
audio rushes or the video runs 100 seconds. Every section needs at
least one enhancement cue (a visual direction, not a podcast script);
density is at least one cue every 8-10 seconds.

## Assets

Required tools: `tts_selector` (narration) and `image_selector`
(visuals). Optional: `video_selector`, `diagram_gen`, `code_snippet`,
`math_animate`, `music_gen`. All asset files must exist on disk, the
narration must cover all script sections and apply the approved voice
performance plan, and image style must stay consistent across scenes.
Music: check the user's music library first, then royalty-free search,
then generation; surface the music situation at proposal time, never as
a surprise at the asset stage.
