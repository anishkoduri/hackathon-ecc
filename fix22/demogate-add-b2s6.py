#!/usr/bin/env python3
"""Append the DEMOGATE_B2S6 runtime patch to fix22.py.

B2S6: orch-build-mvp step 9 (line 84) — the §3 carve-out timing parenthetical
still said "after deploy/demo/commit/README". Same one-word fix as H-3,
but orch-build-mvp is ECC-derived, so it goes through fix22.py as a
mode="replace" runtime patch (same form as DEMOGATE_B2S1–B2S5 / B3S1–B3S7).
Old text is a short literal phrase, verified count==1 in the CURRENT built
tree; new text carries the DEMOGATE_B2S6_F22 token. Run once, then run
`python3 fix22/fix22.py` (B2S6 APPLIED, the rest SKIPPED-ALREADY) and rebuild.
"""
import os

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
FIX22 = os.path.join(PLUGIN, "fix22")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")

PID = "DEMOGATE_B2S6"
REL = "skills/orch-build-mvp/SKILL.md"
OLD = "it runs once, after deploy/demo/commit/README, and never gates a feature."
NEW = "it runs once, after deploy/commit/README, and never gates a feature. (fix #22 /demo gate, DEMOGATE_B2S6_F22)"
TOKEN = "DEMOGATE_B2S6_F22"
BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]


def main():
    path = os.path.join(BUILT, REL)
    t = open(path, encoding="utf-8").read()
    n = t.count(OLD)
    assert n == 1, f"old count={n} in {REL}"
    assert TOKEN not in t, f"token {TOKEN} already in {REL}"
    assert TOKEN in NEW
    low = NEW.lower()
    for b in BANNED:
        assert b not in low, f"banned term {b!r}"

    f22 = os.path.join(FIX22, "fix22.py")
    src = open(f22, encoding="utf-8").read()
    assert src.count(f'"{PID}"') == 0, f"{PID} already in fix22.py"
    anchor = "PATCHES = ["
    assert src.count(anchor) == 1
    const = f'{PID} = """{NEW}"""'
    src = src.replace(anchor, const + "\n\n" + anchor, 1)
    idx = src.find(anchor)
    close = src.find("\n]\n", idx)
    assert close != -1
    tup = f'    ("{PID}", "{REL}", {OLD!r}, {PID}, "replace", "{TOKEN}"),'
    src = src[:close] + "\n" + tup + src[close:]
    open(f22, "w", encoding="utf-8").write(src)
    print(f"fix22.py: appended {PID} constant + runtime tuple")


if __name__ == "__main__":
    main()
