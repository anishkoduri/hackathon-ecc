#!/usr/bin/env python3
"""fix18_fixup.py -- fix-up round for fix #18 (after audit #58 MINOR-1 and
sweep #21 cross-references).

Usage: python3 fix18/fix18_fixup.py     (preflight + apply + self-check)
Exits non-zero if any anchor count differs from expected.

Fix-up items:
  1. MINOR-1: allocation-table totals line is arithmetically wrong —
     rows sum to 103–126s, not 113–126s (SPEC's own error, copied verbatim).
     Fix in staged SKILL.md (SPEC.md fixed by hand alongside).
  2. Sweep #21: `1:30–1:50` survives in 5 cross-references outside
     pitch-deck-video. The canonical statement (hackathon-mode §6) claims
     to govern, so leaving them contradicts F6. Fixed:
     - staged: new-rules/hackathon-mode.mdc, rewritten-skills/hackathon-scope
     - build.sh: README heredoc, Fix-4 patch NEW (pitch-script-template),
       Gap-39 comment + Gap-39 NEW + Batch-F old/new (the line-32 text,
       which Gap 39's patch WRITES — upstream has only the short sentence).
  3. Audit observation: Arch.tsx stack label uses the node kind tone;
     SPEC F2 says "(mono, accent color)" — made literal (C.accent).

Each entry: (base, rel, old, new, expected_count). Bases: STAGED =
new-skills/pitch-deck-video, PLUGIN = plugin root, BUILD = build.sh.
"""
import hashlib
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
STAGED = os.path.join(PLUGIN, "new-skills/pitch-deck-video")

OLD_MD5 = "1a999d763e6ec1fb16985d346b106df0"

FIXUP_SUBS = [
    # 1. MINOR-1 totals line (staged skill).
    (STAGED, "SKILL.md",
     "Totals: 113–126s of content",
     "Totals: 103–126s of content", 1),
    # 3. Arch.tsx stack label: kind tone -> literal accent (SPEC F2).
    (STAGED, "template/src/scenes/Arch.tsx",
     "color: col, marginTop: 8",
     "color: C.accent, marginTop: 8", 1),
    # 2a. Canonical statement (staged rule, verbatim copy).
    (PLUGIN, "new-rules/hackathon-mode.mdc",
     "the demo video is 1:30–1:50",
     "the demo video is under 2:10 (hard rule; absolute max 2:30)", 1),
    # 2b. Scope restatement (staged restored original, verbatim copy).
    (PLUGIN, "rewritten-skills/hackathon-scope/SKILL.md",
     "the demo video is 1:30–1:50",
     "the demo video is under 2:10 (hard rule; absolute max 2:30)", 1),
    # 2c. README heredoc (build.sh writes the plugin README).
    (PLUGIN, "build.sh",
     "- `/demo` — generate a narrated 1:30–1:50 product demo video of the app",
     "- `/demo` — generate a narrated product demo video, under 2:10, of the app", 1),
    # 2d. Fix-4 patch NEW side (pitch-script-template.md template line).
    (PLUGIN, "build.sh",
     '"- Video (demo video, 1:30–1:50), recorded after the final deploy: [path or link, not a local file only]"),',
     '"- Video (demo video, under 2:10), recorded after the final deploy: [path or link, not a local file only]"),', 1),
    # 2e. Gap-39 comment (must run before 2g: it holds the same fragment).
    (PLUGIN, "build.sh",
     "  # demo video is 1:30–1:50. The canonical statement lives in",
     "  # demo video is under 2:10 (hard rule; absolute max 2:30). The canonical statement lives in", 1),
    # 2f. Line-32 fragment 1: appears in Gap-39 NEW, Batch-F old, Batch-F new.
    (PLUGIN, "build.sh",
     "(1:30–1:50, pitch-deck-video / /demo)",
     "(under 2:10, pitch-deck-video / /demo)", 3),
    # 2g. Line-32 fragment 2: same 3 spots (comment already fixed by 2e).
    (PLUGIN, "build.sh",
     "the demo video is 1:30–1:50",
     "the demo video is under 2:10 (hard rule; absolute max 2:30)", 3),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]


def read(base, rel):
    with open(os.path.join(base, rel), encoding="utf-8") as f:
        return f.read()


def main():
    # Single sequential pass: each sub's count is asserted on the text as
    # left by the previous subs (2e must run before 2g — the Gap-39 comment
    # holds the same fragment as the three line-32 spots).
    cache = {}
    for base, rel, old, new, want in FIXUP_SUBS:
        key = (base, rel)
        if key not in cache:
            cache[key] = read(base, rel)
        n = cache[key].count(old)
        if n != want:
            print(f"FAIL {rel}: anchor count {n} (want {want}): {old[:80]!r}")
            sys.exit(1)
        cache[key] = cache[key].replace(old, new)
        assert new in cache[key], rel
    for (base, rel), text in cache.items():
        with open(os.path.join(base, rel), "w", encoding="utf-8") as f:
            f.write(text)
    print(f"applied {len(FIXUP_SUBS)} fix-up subs across {len(cache)} files")

    # Self-checks.
    build = read(PLUGIN, "build.sh")
    assert "1:30–1:50" not in build, "old length survives in build.sh"
    assert build.count("under 2:10 (hard rule; absolute max 2:30)") >= 4, "regime text missing"
    assert len(build.splitlines()) == 23276, "build.sh line count moved"
    new_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()
    assert new_md5 != OLD_MD5, "build.sh md5 unchanged — fix-up did not land"
    print(f"build.sh still 23,276 lines; md5 {OLD_MD5[:8]}… -> {new_md5}")
    for base, rel in ((STAGED, "SKILL.md"), (PLUGIN, "new-rules/hackathon-mode.mdc"),
                      (PLUGIN, "rewritten-skills/hackathon-scope/SKILL.md")):
        assert "1:30–1:50" not in read(base, rel), rel
    skill = read(STAGED, "SKILL.md")
    assert "Totals: 103–126s of content" in skill, "totals line not fixed"
    assert "color: C.accent, marginTop: 8" in read(STAGED, "template/src/scenes/Arch.tsx")
    print("self-checks pass: no 1:30–1:50 left in build.sh or the edited staged files")


if __name__ == "__main__":
    main()
