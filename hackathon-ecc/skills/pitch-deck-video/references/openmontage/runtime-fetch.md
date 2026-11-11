<!-- Adapted from OpenMontage (https://github.com/calesthio/OpenMontage), AGPL-3.0. See LICENSE in this directory. -->

# Runtime fetch note: what was NOT staged

Only the three pipeline manifests and condensed director notes are
staged in this directory. Everything below is fetched from the
OpenMontage repo at runtime when a montage or explainer run actually
needs it. Do not vendor it into the plugin.

## How to fetch

```sh
git clone --depth 1 https://github.com/calesthio/OpenMontage.git /tmp/openmontage
```

A depth-1 clone measured about 163 MB on 2026-11-10 (the repo is
2,285 files; the 77 MB figure in older notes understates it). Prefer a
sparse checkout of just the paths below if the machine is slow:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/calesthio/OpenMontage.git /tmp/openmontage
git -C /tmp/openmontage sparse-checkout set skills/pipelines/documentary-montage skills/pipelines/explainer skills/pipelines/screen-demo tools AGENT_GUIDE.md
```

## What to fetch, and why it was left out

| Path in OpenMontage | What it is | Why not staged |
| --- | --- | --- |
| `AGENT_GUIDE.md` | Routing, checkpoints, decision-log and runtime-selection governance | 49 KB reference doc; the rules that matter for this skill are summarised in `SKILL.md` (budget governance, decision log) and in the mode notes |
| `skills/pipelines/documentary-montage/*.md` | Full director skills (idea, scene, asset, edit, compose, executive-producer) | ~2,100 lines; condensed into `montage.md` |
| `skills/pipelines/explainer/*.md` | Full director skills (research, proposal, script, scene, asset, edit, compose, publish) | ~2,500 lines; condensed into `explainer.md` |
| `skills/pipelines/screen-demo/*.md` | Full director skills | ~1,000 lines; condensed into `screen-demo.md` |
| `skills/creative/stock-sourcing-usage.md`, `skills/creative/broll-planning.md`, `skills/creative/screen-recording.md` | Stock provider tables, b-roll planning, recording practice | Summarised in `montage.md` (sources, licences) and `screen-demo.md` |
| `skills/meta/voice-performance-director.md` | Voice performance plans, sample gate | Summarised in `explainer.md` (full `voice_performance` plan, delivery cues, sample gate, failure conditions) and applied to film-mode narration in `SKILL.md` ("Voice direction — make it sound human") |
| `tools/video/direct_clip_search.py`, `corpus_builder.py`, `clip_search.py` | Stock footage acquisition + CLIP retrieval | Python tools; this skill's template is Node/Remotion, so they run as an external step, not from the template |
| `tools/audio/tts_selector.py`, `elevenlabs_tts.py`, `piper_tts.py` | TTS provider routing, ElevenLabs + Piper implementations | The ElevenLabs REST shape and Piper invocation are already re-implemented in `template/scripts/tts.mjs`; the Python files are the reference if the port drifts |
| `tools/video/video_compose.py`, `tools/cost_tracker.py`, `lib/checkpoint.py` | Render, budget governance, decision log | Governance rules summarised in `SKILL.md`; no Python runtime in the template |
| `schemas/artifacts/*.schema.json`, `schemas/pipelines/*` | Artifact validation schemas | Only needed for a full OpenMontage run, not for the condensed modes |
| `styles/*.yaml`, `remotion-composer/`, `ink-theater/`, `backlot/`, `docs/`, `tests/` | Playbooks, composer app, review UI, docs, tests | Out of scope for a hackathon demo video |

## What WAS staged, and why

- The three pipeline manifests (verbatim): they are the contract each
  mode runs against (stages, gates, budgets, required skills).
- Three condensed mode notes: the decisions and numbers an agent needs
  without reading ~6,000 lines of director skills.
- `LICENSE`: the full AGPL-3.0 text, so the staged material stays
  compliant. Every staged file carries an attribution header pointing
  at it.

## Deliberately left out entirely

- The whole repo (163 MB, 2,285 files): far beyond what three opt-in
  modes need, and it would bloat the plugin build.
- Video/image generation providers (Runway, Veo, Kling, FLUX, etc.):
  paid, key-gated, and behind the budget governance in `SKILL.md`.
  Nothing about them is staged; the agent proposes them at runtime and
  the user approves before any spend.
- `node_modules`, `.git`, assets, and example media: build artefacts,
  not source.
