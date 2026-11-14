#!/usr/bin/env python3
"""Append the DEMOGATE_B2S7 runtime patch to fix22.py.

B2S7: orch-build-mvp narration-key paragraph (SKILL.md line 32) — Sweep #30b
re-run minor finding 2: the paragraph still assumes a video will be filmed
("if narration will need a key", "the video renders music-only/silent",
"step 8 `/demo` time", "Key handoff to step 8") — unlike orchestrate step 0
(O-2a), it was never conditioned on the user having asked for a video, and
step 8 no longer films via /demo at all (DEMOGATE_B2S1/B2S2). The patch
conditions the prompt on a requested video and re-points the key handoff at
a user-invoked /demo. orch-build-mvp is ECC-derived, so this goes through
fix22.py as a mode="replace" runtime patch (same form as B2S1–B2S6).

The old text is the full line-32 paragraph, extracted from the CURRENT built
tree; the new text is built from it by four targeted replacements plus the
DEMOGATE_B2S7_F22 token appended at the end. Run once, then run
`python3 fix22/fix22.py` (B2S7 APPLIED, the rest SKIPPED-ALREADY) and rebuild.
"""
import os

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
FIX22 = os.path.join(PLUGIN, "fix22")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")

PID = "DEMOGATE_B2S7"
REL = "skills/orch-build-mvp/SKILL.md"
TOKEN = "DEMOGATE_B2S7_F22"
BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]

REPLACEMENTS = [
    # Condition the prompt on a requested video.
    ("At the start of the run (step 1), if narration will need a key and none is set (no `ELEVENLABS_API_KEY` in the environment, no MiniMax credentials), issue the single `pitch-deck-video` narration-key prompt once",
     "At the start of the run (step 1), if the user asked for a demo video and narration will need a key and none is set (no `ELEVENLABS_API_KEY` in the environment, no MiniMax credentials), issue the single `pitch-deck-video` narration-key prompt once. If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed"),
    # No "step 8 /demo time" — step 8 no longer films.
    ("Do NOT re-prompt at step 8 `/demo` time: the single early prompt covers the run, and `/demo` uses the key if present, else falls back to music-only/silent.",
     "Do NOT re-prompt at `/demo` time: the single early prompt covers the run, and a user-invoked `/demo` uses the key if present, else falls back to music-only/silent."),
    # Key handoff is to a user-invoked /demo, not "step 8".
    ("**Key handoff to step 8:** if the user replies with a key mid-run, hold it in working context ONLY and pass it to the step-8 `/demo` via the dispatch: the step-8 dispatch carries an explicit env instruction",
     "**Key handoff to a user-invoked `/demo`:** if the user replies with a key mid-run, hold it in working context ONLY and pass it to `/demo` via the dispatch if the user asks for a video: the `/demo` dispatch carries an explicit env instruction"),
    # The re-render is after a user-invoked /demo, not "step 8".
    ("If the key arrives after step 8 already rendered but before the step-9 final report, re-run the video script step",
     "If the key arrives after the user-invoked `/demo` already rendered but before the step-9 final report, re-run the video script step"),
]


def main():
    path = os.path.join(BUILT, REL)
    lines = open(path, encoding="utf-8").read().split("\n")
    # Line 32 (1-based) is the narration-key paragraph.
    old = lines[31]
    assert old.startswith("**Narration-key prompt — once, at the start of the standalone run, never blocking.**"), \
        f"line 32 is not the narration-key paragraph: {old[:80]!r}"
    assert TOKEN not in old
    new = old
    for i, (o, n) in enumerate(REPLACEMENTS):
        cnt = new.count(o)
        assert cnt == 1, f"replacement {i}: old count={cnt}: {o[:80]!r}"
        new = new.replace(o, n)
        print(f"replacement {i} applied")
    new = new + f" (fix #22 /demo gate, {TOKEN})"
    assert TOKEN in new
    low = new.lower()
    for b in BANNED:
        assert b not in low, f"banned term {b!r}"

    f22 = os.path.join(FIX22, "fix22.py")
    src = open(f22, encoding="utf-8").read()
    assert src.count(f'"{PID}"') == 0, f"{PID} already in fix22.py"
    anchor = "PATCHES = ["
    assert src.count(anchor) == 1
    const = f'{PID} = """{new}"""'
    src = src.replace(anchor, const + "\n\n" + anchor, 1)
    idx = src.find(anchor)
    close = src.find("\n]\n", idx)
    assert close != -1
    tup = f'    ("{PID}", "{REL}", {old!r}, {PID}, "replace", "{TOKEN}"),'
    src = src[:close] + "\n" + tup + src[close:]
    open(f22, "w", encoding="utf-8").write(src)
    print(f"fix22.py: appended {PID} constant + runtime tuple (old_len={len(old)}, new_len={len(new)})")


if __name__ == "__main__":
    main()
