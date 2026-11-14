#!/usr/bin/env python3
"""Demogate round 3 — staged fixes for the Audit #68 re-run (M-1) and the
Sweep #30b re-run (Remotion blocking finding), plus the Audit #68 re-run
observation on hackathon-mode §7's narration-key paragraph.

- M-1: hackathon-mode :22 §3 — "(after deploy, demo, commit, and README)"
  is the last leftover sequence listing demo as a pipeline step.
- H-4a/b: hackathon-mode :59 §7 narration-key paragraph — it never restated
  the "only when the user asked for a demo video" condition (orchestrate
  step 0 is conditional since O-2a; §7 read alone would send the prompt
  unconditionally).
- REMO-2a/b: pitch-deck-video template build.mjs:335 + qa.mjs:42 — bare
  `npx @remotion/cli@4.0.526 <cmd>` fails live: the package carries THREE
  bins (remotion/remotionb/remotiond), so npm cannot determine the
  executable ("could not determine executable to run", verified live by the
  dry-run #37 re-run). Working form (verified live, exit 0):
  `npx -p @remotion/cli@4.0.526 remotion <cmd>`.

All edits validated count==1 before replacing. Run once.
"""
import os

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]

EDITS = [
    # M-1: hackathon-mode :22.
    ("new-rules/hackathon-mode.mdc",
     "The one permitted invocation is the named end-of-project run immediately before the first build's final report (after deploy, demo, commit, and README)",
     "The one permitted invocation is the named end-of-project run immediately before the first build's final report (after deploy, commit, and README)"),
    # H-4a: §7 narration-key paragraph — the prompt is conditional.
    ("new-rules/hackathon-mode.mdc",
     "**Scheduled here, sent by orchestrate:** orchestrate sends it immediately after grill-me, before scoping (orchestrate step 0) — on the grilled path and on the skip-grilling path (\"skip the grilling\" / \"just build it\") alike, at the start of the build either way.",
     "**Scheduled here, sent by orchestrate:** orchestrate sends it immediately after grill-me, before scoping (orchestrate step 0) — only when the user asked for a demo video; on the grilled path and on the skip-grilling path (\"skip the grilling\" / \"just build it\") alike, at the start of the build either way. If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed."),
    # H-4b: §7 — the no-key fallback only applies to a requested video.
    ("new-rules/hackathon-mode.mdc",
     "If no key ever arrives, /demo renders music-only/silent with a note in the final report — no second ask, no stall.",
     "If no key ever arrives, a requested /demo renders music-only/silent with a note in the final report — no second ask, no stall."),
    # REMO-2a: build.mjs render call — name the executable explicitly.
    ("new-skills/pitch-deck-video/template/scripts/build.mjs",
     "run('npx', ['@remotion/cli@4.0.526', 'render',",
     "run('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'render',"),
    # REMO-2b: qa.mjs stills call — name the executable explicitly.
    ("new-skills/pitch-deck-video/template/scripts/qa.mjs",
     "execFileSync('npx', ['@remotion/cli@4.0.526', 'still',",
     "execFileSync('npx', ['-p', '@remotion/cli@4.0.526', 'remotion', 'still',"),
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
