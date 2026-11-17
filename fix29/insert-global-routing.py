#!/usr/bin/env python3
"""Insert the GLOBAL-ROUTING block (fix29/global-routing-block.txt)
byte-identically into the two staged files that carry it, after the
DESIGNPKG-AUTO paragraph in each:

  new-skills/orchestrate/SKILL.md  (after line 35, bare paragraph)
  new-rules/hackathon-mode.mdc     (after line 44, "- " bullet)

Byte-identity: both insertions use the same block text from the .txt
file; only the bullet prefix differs (orchestrate's DESIGNPKG-AUTO line
is a bare paragraph, hackathon-mode's is a "- " bullet — same as the
DESIGNPKG-AUTO precedent). Run once; refuses to run twice.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = open(os.path.join(ROOT, "fix29", "global-routing-block.txt"),
             encoding="utf-8").read().strip("\n")
assert BLOCK.startswith("**GLOBAL-ROUTING"), "block text must start with the bold lead"
assert "GLOBAL-ROUTING_F29" in BLOCK
for _t in ("ORCHESTRATOR-ONLY_F29", "FACTORY-DISPATCH_F29",
           "DIRECTOR-BRIEF_F29", "NO-GUESSING_F29", "VERIFY-MERGE_F29",
           "COST-AWARE_F29"):
    assert _t in BLOCK, f"block missing token {_t}"

TARGETS = [
    ("new-skills/orchestrate/SKILL.md", 35, ""),
    ("new-rules/hackathon-mode.mdc", 44, "- "),
]
for rel, lineno, prefix in TARGETS:
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    assert "GLOBAL-ROUTING_F29" not in "\n".join(lines), f"{rel}: block already present"
    assert "DESIGNPKG-AUTO_F27" in lines[lineno - 1], (
        f"{rel}: line {lineno} is not the DESIGNPKG-AUTO paragraph: "
        f"{lines[lineno - 1][:80]!r}")
    lines.insert(lineno, prefix + BLOCK)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"inserted GLOBAL-ROUTING block after {rel}:{lineno}")

# Byte-identity check: the paragraph text (sans bullet prefix) is
# identical in both files.
texts = []
for rel, lineno, prefix in TARGETS:
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    assert lines[lineno].startswith(prefix + "**GLOBAL-ROUTING"), rel
    texts.append(lines[lineno][len(prefix):])
assert texts[0] == texts[1], "GLOBAL-ROUTING block differs between the two files"
print("byte-identity confirmed: orchestrate and hackathon-mode carry the same block")
