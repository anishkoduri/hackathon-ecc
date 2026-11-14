#!/usr/bin/env python3
"""Second demogate follow-up: three stale demo-as-pipeline-step mentions the
first demogate pass missed (found by the coordinator's post-rebuild grep).

- O-9a/b: orchestrate step 6 (line 82) — the README video-path input assumed
  a video always exists, and the "Order:" sentence still listed demo video
  as a pipeline step.
- H-2: hackathon-mode line 12 — the first-build sequence still listed
  "deploy → demo → README" and described the narration-key prompt as
  unconditional (O-2a made it conditional on a requested video).
- H-3: hackathon-mode line 61 — the §7 carve-out timing parenthetical still
  said "after deploy/demo/commit/README".

All edits are validated count==1 before replacing. Run once.
"""
import os

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]

EDITS = [
    # O-9a: orchestrate step 6 — README video-path input is conditional.
    ("new-skills/orchestrate/SKILL.md",
     "passing it the deployed URL from the ledger and the video file path `<app-name>-video/out/demo.mp4` as inputs, so the README links the real URL and video instead of a placeholder",
     "passing it the deployed URL from the ledger and, if a video was filmed, the video file path `<app-name>-video/out/demo.mp4` as inputs, so the README links the real URL and the video (when one exists) instead of a placeholder"),
    # O-9b: orchestrate step 6 — Order sentence drops the demo-video step.
    ("new-skills/orchestrate/SKILL.md",
     "Order: verify → polish → deploy → demo video → commit → README → final report.",
     "Order: verify → polish → deploy → commit → README → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order; fix #22 /demo gate, DEMOGATE_O9_F22.)"),
    # H-2: hackathon-mode line 12 — first-build sequence drops demo; the
    # narration-key prompt is conditional on a requested video (cf. O-2a).
    ("new-rules/hackathon-mode.mdc",
     "The first-build sequence is: grill → narration-key prompt (orchestrate sends it immediately after grill-me, before scoping — orchestrate step 0; it also fires on the skip-grilling path, at the start of the build either way) → scope → expansion (Phases 0–3) → build (orchestrate drives; expansion Phases 4–6 inside) → verify → polish → deploy → demo → README → final report (written to `docs/final-report.md` in the project and delivered as the reply).",
     "The first-build sequence is: grill → narration-key prompt (orchestrate sends it immediately after grill-me, before scoping — orchestrate step 0; only when the user asked for a demo video; it also fires on the skip-grilling path, at the start of the build either way) → scope → expansion (Phases 0–3) → build (orchestrate drives; expansion Phases 4–6 inside) → verify → polish → deploy → README → final report (written to `docs/final-report.md` in the project and delivered as the reply). /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (fix #22 /demo gate, DEMOGATE_H2_F22)."),
    # H-3: hackathon-mode line 61 — carve-out timing drops demo.
    ("new-rules/hackathon-mode.mdc",
     "it runs once, after deploy/demo/commit/README, and never gates a feature.)",
     "it runs once, after deploy/commit/README, and never gates a feature.)"),
]


def main():
    cache = {}
    for rel, old, new in EDITS:
        path = os.path.join(PLUGIN, rel)
        if path not in cache:
            cache[path] = open(path, encoding="utf-8").read()
        t = cache[path]
        n = t.count(old)
        assert n == 1, f"{rel}: old count={n}: {old[:80]!r}"
        low = new.lower()
        for b in BANNED:
            assert b not in low, f"{rel}: banned term {b!r}"
        cache[path] = t.replace(old, new)
        print(f"applied: {rel}: {old[:60]!r}...")
    for path, t in cache.items():
        open(path, "w", encoding="utf-8").write(t)
        print("wrote", path)


if __name__ == "__main__":
    main()
