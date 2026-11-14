#!/usr/bin/env python3
"""Fix-up #20d (Nov 12, 2026) — sweep #28 MINOR-1, comment-only.

Sweep #28 found that the fixup20c MINOR-3 normalization (SPEC section
12.1, "normalize all of them") missed a lowercase family: 20 build.sh
block headers say "The coordinator inserts this block last, just
before STEP 5." (or "The patch agent inserts …"). The fixup20c probe
only counted uppercase `LAST`, so this family was never counted. Same
false claim, different casing — fixed here with the same minimal
removal ("inserts this block last, just before STEP 5" -> "inserts
this block before STEP 5"; split-line form likewise).

Scope: build.sh comments only. Zero behavior, no staged-source edits,
no new rules, no build.sh block appended (nothing to patch in the
built tree). Line count unchanged (23,609); md5 changes, so the four
earlier verifiers' pins are bumped afterwards (check lines + docstring
sentences + the fix19:330 section label) and all five verifiers are
re-run. See SPEC.md section 12.5.
"""
import hashlib
import os
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]

# (old, new, expected-count) — counts probed on a /tmp copy first.
COMMENT_SUBS = [
    ("inserts this block last, just before STEP 5",
     "inserts this block before STEP 5", 13),
    ("inserts this block last, just\n# before STEP 5",
     "inserts this block\n# before STEP 5", 7),
]


def preflight():
    btext = open(BUILD_SH, encoding="utf-8").read()
    lines = btext.splitlines()
    md5 = hashlib.md5(btext.encode("utf-8")).hexdigest()
    assert (len(lines), md5) == (23609, "3c7b45bbfca8dbe10d10b9eb4b445160"), \
        f"PREFLIGHT build.sh is {len(lines)} lines md5 {md5}, expected 23609 / 3c7b45bb… (post-fixup20c)"
    for old, _new, n in COMMENT_SUBS:
        assert btext.count(old) == n, \
            f"PREFLIGHT build.sh: phrase count={btext.count(old)}, expected {n}: {old[:60]!r}"
    assert "fixup20c upstream block applied" in btext, \
        "PREFLIGHT build.sh: fixup20c block marker missing"
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    print("preflight OK: %d comment subs" % len(COMMENT_SUBS))


def main():
    preflight()
    shutil.copy2(BUILD_SH, BUILD_SH + ".before-fixup20d")
    text = open(BUILD_SH, encoding="utf-8").read()
    total = 0
    for old, new, n in COMMENT_SUBS:
        assert text.count(old) == n, f"APPLY build.sh: phrase count!= {n}"
        text = text.replace(old, new)
        total += n
    open(BUILD_SH, "w", encoding="utf-8").write(text)
    print(f"build.sh: {total} comment replacements applied")
    # self-checks
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert len(btext.splitlines()) == 23609, "SELF-CHECK build.sh: line count changed"
    assert btext.count("inserts this block last") == 0, \
        "SELF-CHECK build.sh: lowercase family survives"
    assert btext.count("last, just before STEP 5") == 0, \
        "SELF-CHECK build.sh: lowercase placement-last survives"
    assert btext.count("hackathon-mode section 37") == 0, \
        "SELF-CHECK build.sh: section 37 survives"
    last_lines = [ln for ln in btext.split("\n") if "LAST" in ln]
    assert len(last_lines) == 2 and all("runs LAST (after every" in ln for ln in last_lines), \
        f"SELF-CHECK build.sh: unexpected LAST lines: {last_lines!r}"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert "fixup20c upstream block applied" in btext, "SELF-CHECK build.sh: fixup20c block missing"
    print("self-checks OK: lowercase family gone; uppercase hygiene holds; lines 23609")
    print("new build.sh md5:", hashlib.md5(btext.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
