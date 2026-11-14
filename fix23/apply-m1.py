#!/usr/bin/env python3
"""Fix #23 M1 applier (Audit #70, MINOR).

Inserts ONE runtime-patch block into build.sh immediately BEFORE the
line `# STEP 5 — Counts` (after the CORE block, which is required: the
anchor text only exists because the §9 block runs first). The block
adds one sentence to the DYNAMIC-BQA-01 paragraph in the built
skills/browser-qa/SKILL.md, mode `after`, anchored count==1 on the
paragraph's FAILS sentence.

The sentence (Audit #70's wording):
  "If the harness cannot drive an interaction the job calls for, record
  that interaction as unverified — a gap, never a silent pass; the
  Dynamic row is not ✓ on an interaction never driven."
It carries no DYNAMIC_F23 token, so token counts do not change.

Usage: python3 fix23/apply-m1.py   (from ~/workspace/hackathon-plugin)
Idempotent: refuses if its marker comment is already in build.sh.
Never edit the built tree directly: the sentence lands via build.sh.
"""
import hashlib
import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
BUILT_BQA = os.path.join(PLUGIN, "hackathon-ecc/skills/browser-qa/SKILL.md")
MARKER = "# --- fix23 M1: DYNAMIC-BQA-01 undrivable-interaction disposition"
STEP5 = "# STEP 5 — Counts"
ANCHOR = ("A control that does not respond, or a state that changes "
          "without motion, FAILS the build.")
KEY_PHRASE = "record that interaction as unverified"

BLOCK = r'''# --- fix23 M1: DYNAMIC-BQA-01 undrivable-interaction disposition (Audit #70) ---
# Audit #70 M1 (MINOR): the DYNAMIC-BQA-01 live check tells the executor
# to sort, filter, expand, and drag where the job calls for it but gives
# no disposition for an interaction the harness cannot drive. This block
# records an undrivable interaction as unverified -- a gap, never a
# silent pass. Placement: before STEP 5 (after the CORE block); the
# anchor text only exists because the §9 block runs first. The added
# sentence carries no DYNAMIC_F23 token, so token counts do not change.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]

subs = [
  ('DYNAMIC-BQA-01-M1', 'skills/browser-qa/SKILL.md', 'A control that does not respond, or a state that changes without motion, FAILS the build.', ' If the harness cannot drive an interaction the job calls for, record that interaction as unverified — a gap, never a silent pass; the Dynamic row is not ✓ on an interaction never driven.', 'after'),  # 'DYNAMIC-BQA-01-M1'
]
for pid, rel, old, add, mode in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix23 M1 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    if mode == 'after':
        new = old + add
    elif mode == 'before':
        new = add.rstrip('\n') + '\n\n' + old
    else:  # replace
        new = add
    open(p, "w").write(t.replace(old, new))
print("fix23 M1 upstream block applied")
PYEOF
'''


def main():
    text = open(BUILD_SH, encoding="utf-8").read()
    # Idempotency guard: refuse if the marker is already present.
    if MARKER in text:
        print("REFUSED: fix23 M1 marker already present in build.sh "
              "(already applied)")
        sys.exit(1)
    # Placement anchor: exactly one STEP 5 Counts line.
    n_step5 = text.count(STEP5 + "\n")
    assert n_step5 == 1, \
        "STEP 5 anchor count=%d (expected 1)" % n_step5
    # Preflight: anchor resolves count==1 against the CURRENT built tree,
    # and the sentence is not already there.
    bqa = open(BUILT_BQA, encoding="utf-8").read()
    n_anchor = bqa.count(ANCHOR)
    assert n_anchor == 1, \
        "M1 anchor count=%d in built browser-qa SKILL.md (expected 1)" \
        % n_anchor
    assert KEY_PHRASE not in bqa, \
        "M1 sentence already present in built browser-qa SKILL.md"
    # The added sentence itself must not contain the token.
    added = BLOCK.split("' If the harness cannot drive")[1].split("', 'after'")[0]
    assert "DYNAMIC_F23" not in added, "added sentence carries DYNAMIC_F23"
    new_text = text.replace(STEP5 + "\n", BLOCK + STEP5 + "\n", 1)
    assert new_text != text
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new_text)
    lines = new_text.count("\n") + (0 if new_text.endswith("\n") else 1)
    md5 = hashlib.md5(new_text.encode("utf-8")).hexdigest()
    print("fix23 M1 block inserted before STEP 5 Counts")
    print("build.sh now %d lines, md5 %s" % (lines, md5))


if __name__ == "__main__":
    main()
