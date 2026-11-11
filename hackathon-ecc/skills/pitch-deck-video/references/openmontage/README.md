<!-- Adapted from OpenMontage (https://github.com/calesthio/OpenMontage), AGPL-3.0. See LICENSE in this directory. -->

# OpenMontage material staged for pitch-deck-video

Condensed, AGPL-3.0-licensed material from OpenMontage
(calesthio/OpenMontage) backing the two opt-in `/demo` modes (montage
and explainer) and the screen-demo reference. Film mode does not use
any of this; it stays the default and is unaffected.

## Files staged (78,519 bytes total, plus this README)

| File | Bytes | What it is |
| --- | --- | --- |
| `LICENSE` | 34,523 | Verbatim AGPL-3.0 licence text from upstream |
| `documentary-montage.yaml` | 7,730 | Montage pipeline manifest, verbatim (plus a 3-line attribution header) |
| `animated-explainer.yaml` | 9,378 | Explainer pipeline manifest, verbatim (plus header) |
| `screen-demo.yaml` | 8,388 | Screen-demo pipeline manifest, verbatim (plus header) |
| `montage.md` | 5,438 | Condensed montage director notes (brief, slots, clip retrieval, edit/compose rules) |
| `explainer.md` | 5,109 | Condensed explainer director notes (proposal gate, cost estimate, script/voice, assets) |
| `screen-demo.md` | 3,791 | Condensed screen-demo notes, plus how it relates to film mode |
| `runtime-fetch.md` | 4,162 | What was NOT staged and how the agent fetches it at runtime |

## What was deliberately left out

- The whole repo: a depth-1 clone is ~163 MB / 2,285 files. Only the
  three manifests and condensed notes are staged.
- Full director skills (~6,000 lines across the three pipelines):
  condensed into the three `.md` notes; fetch at runtime per
  `runtime-fetch.md` if a run needs the full text.
- Tool implementations (`direct_clip_search`, `corpus_builder`,
  `clip_search`, `tts_selector`, `video_compose`, `cost_tracker`):
  Python tools, not part of the Node/Remotion template. The ElevenLabs
  REST shape and Piper invocation they define are already re-implemented
  in `template/scripts/tts.mjs`.
- Schemas, styles/playbooks, remotion-composer, ink-theater, backlot,
  docs, tests, assets, `.git`, `node_modules`: out of scope.
- Paid video/image providers (Runway, Veo, Kling, FLUX, etc.): nothing
  staged; proposed at runtime behind the budget governance in `SKILL.md`.

## Licence

All material here is AGPL-3.0 (see `LICENSE`). Every staged file
carries an attribution header. Fine for local hackathon use; AGPL is
stricter than MIT if someone hosted a modified version as a service
(they would have to offer the source). Do not strip the headers.
