#!/usr/bin/env python3
"""Re-apply the 12 orchestrate staged edits from demogate-apply.py.

BUG in demogate-apply.py: `olines` was read during VALIDATION (pre-edit
snapshot of new-skills/orchestrate/SKILL.md). The staged loop applied
O-1..O-8 and wrote the file, then the O-4 step wrote "\\n".join(olines) --
the PRE-edit content with only line 80 replaced -- clobbering all 12
orchestrate staged edits. O-4 itself survived; every other file's staged
edit survived (O-4 only rewrites orchestrate). This script re-applies
exactly those 12 edits (tuples copied verbatim from demogate-apply.py
STAGED) and verifies O-4 line 80 is intact. Run once.
"""
import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")

EDITS = [
    # O-1
    ("(narration-key prompt → scope → expansion Phases 0–3 → slice → build via the routing table incl. row 10 → verify → polish → deploy → demo LOCAL → README → final report)",
     "(narration-key prompt — only when the user asked for a demo video → scope → expansion Phases 0–3 → slice → build via the routing table incl. row 10 → verify → polish → deploy → README → final report). /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (fix #22 /demo gate)."),
    # O-2a
    ("This is the ONE sanctioned user prompt during the first build besides grill-me itself (hackathon-mode §7 schedules it here); it never blocks the build. Send it once, in one message, whether grill-me ran or the user chose the skip path (\"skip the grilling\" / \"just build it\") — it fires at the start of the build either way.",
     "This is the ONE sanctioned user prompt during the first build besides grill-me itself (hackathon-mode §7 schedules it here) — and ONLY when the user asked for a demo video; it never blocks the build. If the user's request explicitly asks for a demo video (or the user invoked `/demo`), send it once, in one message, whether grill-me ran or the user chose the skip path (\"skip the grilling\" / \"just build it\") — it fires at the start of the build either way. If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed; if the user later asks for a video, `/demo` prompts for the key at the point the video is confirmed (see `commands/demo.md`)."),
    # O-2b
    ("and that the build continues regardless — the video will be built either way, and if the key arrives later a re-run produces the narrated cut.",
     "and that the build continues regardless — if the key arrives later a re-run produces the narrated cut."),
    # O-2c
    ("pass it as the `ELEVENLABS_API_KEY` env var to the `tts` run at /demo time — via the /demo dispatch (step 5d), which carries an explicit env instruction",
     "pass it as the `ELEVENLABS_API_KEY` env var to the `tts` run at /demo time — via the /demo dispatch, which carries an explicit env instruction"),
    # O-2d
    ("If the key arrives after /demo already rendered but before the final report,",
     "If the key arrives after the user-invoked /demo already rendered but before the final report,"),
    # O-3
    ("5. **Verify → polish → deploy → demo, in that order** — four sub-steps inside this one step, never reordered (polish runs after verification and before deploy; deploy runs before demo).",
     "5. **Verify → polish → deploy, in that order** — three sub-steps inside this one step, never reordered (polish runs after verification and before deploy)."),
    # O-5
    ("The 5d demo and the step-6 README/final report film and report the verified tree: after a revert that is the pre-redesign verified state, never the held redesign.",
     "The step-6 README/final report reports the verified tree: after a revert that is the pre-redesign verified state, never the held redesign."),
    # O-6
    ("**End-of-project checks (before the final report).** After deploy, demo, commit, and README, run the six deferred checks by name",
     "**End-of-project checks (before the final report).** After deploy, commit, and README, run the six deferred checks by name"),
    # O-7a
    ("Orchestrate owns the whole-build final report. After deploy, the demo video, and the README, write it to `docs/final-report.md` in the project AND deliver it as the reply",
     "Orchestrate owns the whole-build final report. After deploy and the README, write it to `docs/final-report.md` in the project AND deliver it as the reply"),
    # O-7b
    ("Sequence: verify → polish → deploy → demo video (`/demo` / `pitch-deck-video` films the LOCAL app from the project dir, per orchestrate step 5 above; orchestrate sequences it, it does not film it) → README (`readme-writer`, orchestrate step 6) → final report.",
     "Sequence: verify → polish → deploy → README (`readme-writer`, orchestrate step 6) → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this sequence; if one was filmed, the report carries its handoff below.)"),
    # O-8a
    ("- **Demo video handoff** — the video file path (`<app-name>-video/out/demo.mp4`) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\"",
     "- **Demo video handoff (only if a video was filmed)** — the video file path (`<app-name>-video/out/demo.mp4`) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\""),
    # O-8b
    ("and the music credit (`public/music/SOURCE.txt`).",
     "and the music credit (`public/music/SOURCE.txt`). If no video was filmed (the user did not invoke `/demo`), this handoff is omitted and the report notes that no demo video was filmed."),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]


def main():
    t = open(ORCH, encoding="utf-8").read()
    for i, (old, new) in enumerate(EDITS):
        n = t.count(old)
        assert n == 1, f"edit {i}: old count={n}: {old[:80]!r}"
        low = new.lower()
        for b in BANNED:
            assert b not in low, f"edit {i}: banned term {b!r}"
        t = t.replace(old, new)
        print(f"applied edit {i}")
    # O-4 must still be intact at line 80.
    lines = t.split("\n")
    assert lines[79].startswith("   **Demo — never automatic (fix #22 /demo gate, DEMOGATE_O4_F22)."), \
        f"O-4 line 80 damaged: {lines[79][:80]!r}"
    open(ORCH, "w", encoding="utf-8").write(t)
    print("wrote", ORCH, f"({len(lines)} lines); O-4 line 80 intact")


if __name__ == "__main__":
    main()
