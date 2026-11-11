<!-- Adapted from OpenMontage (https://github.com/calesthio/OpenMontage), AGPL-3.0. See LICENSE in this directory. -->

# Documentary Montage (opt-in mode)

Source: OpenMontage `pipeline_defs/documentary-montage.yaml` (v1.0, beta,
staged verbatim here) and `skills/pipelines/documentary-montage/*.md`
(idea, scene, asset, edit, compose, executive-producer), condensed.
Full director skills are NOT staged; fetch them at runtime if needed
(see `runtime-fetch.md`).

## What it is

A retrieval-first thematic montage: real-world footage (not generated)
arranged by narrative beat, with music sync and a uniform colour grade
across mixed-era footage. Tone reference: Adam Curtis / Chris Marker /
Errol Morris tone poems. Budget default $1.00, max wall time 60 minutes.

## When to offer it

When the video needs to make someone feel something the screen recording
cannot: the problem the product solves, or a story about the people it
serves. It is a mood/story piece, not a product proof. Ask the user
first; film stays the default.

## Inputs: the brief

One thematic question in ONE sentence ("What does it feel like to come
home?", "What happens in a city at 4am?"), ONE tone register, a duration
and shape, a music plan (mandatory; silent only if the user explicitly
opts out), and an end-tag plan (mandatory; one philosophical closing
line, rendered as a Remotion end-card). Narration is OPTIONAL: music,
visuals, and the end-tag can carry the piece alone.

Tone registers: elegiac (long holds, muted colour, slow cuts), urgent
(short cuts, hard sync, motion-heavy), reverent (stately, symmetrical,
patient), wry (ironic juxtaposition), dreamlike (slow dissolves,
repeated motifs, non-linear).

Minimum fields the brief must carry: `topic`, `thematic_question` (one
sentence), `tone` (one register from the fixed list), `duration_seconds`
plus `shape` (concrete numbers / enum values), `sources_allowed`,
`generated_clips_allowed` (false unless the user approved generated
clips), `narration` (the TTS provider and voice if used, or `"none"`
recorded explicitly — never leave the field missing), `music_plan`
(mandatory: a real source, or `source: "none"` plus an explicit opt-out
reason from the user), `end_tag_plan` (mandatory: a non-empty closing
line, or `null` with an explicit opt-out reason), `era_mix`, and
`target_platform`.

`era_mix` is a documentary-specific field: `"modern"` biases slot
sources toward Pexels and other contemporary stock; `"vintage"` biases
toward Archive.org Prelinger — at least 60% of slots must list
`archive_org` as a preferred source; `"any"` leaves the mix open for
the scene director to decide per slot.

## Stages

| Stage | Does | Approval gate |
| --- | --- | --- |
| idea | thematic question, tone, duration/shape, music + end-tag plans | yes |
| scene_plan | slot list: each slot is an intention plus 2-3 short search queries; at least 2 slots marked hero; era_mix reflected in preferred sources | yes |
| assets | one clip per slot, with provenance; see below | yes |
| edit | cut order, holds, transitions, music config, end-tag timing | yes |
| compose | Remotion render, uniform LUT, music mix, end-tag render | no |

## Writing slots (scene plan)

Think like a location scout, not a stock librarian. "Rain streaking
sideways across a bus window at blue hour, passengers' faces in soft
focus, traffic lights bleeding red and green through the glass" is a
slot; "rain in the city montage, 15 clips" is not. Slot descriptions use
concrete noun-and-adjective language because CLIP ranks the description,
not the short search queries.

Slot count follows tone and duration:

| Tone | Average hold | Slots per 60s |
| --- | --- | --- |
| elegiac | 4.0s | ~15 |
| reverent | 3.5s | ~17 |
| dreamlike | 3.0s | ~20 |
| wry | 2.0s | ~30 |
| urgent | 1.2s | ~50 |

## Finding clips (assets)

Two paths. Fast path first for hackathon-scale work (under ~30 slots):

- **Fast path:** `direct_clip_search` fans the slot queries across all
  providers and downloads 2-3 clips per query. No CLIP embeddings, no
  corpus index. Inspect the thumbnails, map the best clip to each slot
  by eye. Reuse clips from earlier acts before downloading more; that
  saved 40-50% of download time in production. Fill gaps with rewritten
  queries, and only then fall back to the standard path for those slots.
- **Standard path:** `corpus_builder` builds a corpus (budget 8-12x the
  slot count, e.g. ~150 candidates for 15 slots), then `clip_search`
  ranks each slot description against it. Accept CLIP ViT-B/32 cosine
  >= 0.30 outright; 0.22-0.30 needs human judgement; below 0.22, grow
  the corpus (max 2 growth passes per slot), do not force a pick.
  Always pass `exclude_ids` so one clip cannot win two slots, and run
  `diversify` over the final list so adjacent picks are not visually
  identical.

Sources: Pexels, Pixabay Video, Coverr, Mixkit, Archive.org (Prelinger
et al.), NARA, Library of Congress, Pond5 public-domain (needs
`POND5_API_KEY`), Videvo, NASA, ESA, JAXA, NOAA, Dareful, Wikimedia,
Unsplash (image-only, support source, not the backbone). For vintage
briefs, run a separate Archive.org-only fan-out and aim for at least
60% of picks from Archive.org. For children's/fairy-tale content,
source-lock to Pixabay Video only (its fantasy-animation depth) and
rewrite queries with fantasy keywords.

Provenance is non-negotiable: every picked clip records provider,
original URL, and licence in the asset manifest, plus a `rejected_picks`
log with reasons. Stock licences: Pexels and Pixabay are free for
commercial use with no attribution required (cannot sell unaltered,
cannot imply endorsement).

## Edit rules

Hero slots hold longest, mid-sequence cutaways shortest. No two adjacent
cuts share subject AND scale. At most 4 distinct transition values.
Music is mandatory unless the brief records an explicit opt-out. The
end-tag renders by default as an overlay (ProRes 4444 with alpha on the
final scenes); fallback is a card appended after the body. Total
duration must match the brief within 10%.

## Compose rules

`render_runtime` is locked to `remotion` on this pipeline: the end-tag
stack depends on Remotion CinematicRenderer components, and there is no
HyperFrames parity yet. Do not silently swap to ffmpeg or HyperFrames.
Output must pass ffprobe validation; verify the end-tag text is visible
over footage, not over black.
