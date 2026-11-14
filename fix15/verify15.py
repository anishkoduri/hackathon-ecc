#!/usr/bin/env python3
"""verify15.py -- checks fix #15 in the BUILT tree (read-only).

Run after a build: python3 fix15/verify15.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. The canonical variety+theme-match block (SPEC section A) is present
     VERBATIM, exactly once, in every target file (11 files), and matches the
     block quoted in fix15/SPEC.md.
  2. R1-R5 anchors present in the files SPEC assigns them to.
  3. C1-C3 anchors present.
  4. D1 anchors present (rule + final-report recording lines).
  5. Treatments still number 1..23 in staged less-flat-ui; staged copy still
     differs from the standalone source by exactly the 3 known runtime-patch
     hunks (fix14).
  6. Counts post-fix16: 166 skills / 72 agents / 123 rules / 87 commands /
     15 hooks (fix #16 deleted 3 skills and 9 commands).
  7. gates.md scrubbed, not upstream-verbatim (coordinator decision, fix-up
     round): staged == built, and the text says "(a subagent in Cursor)" /
     "(in Cursor, ...)" — the fix #15 "untouched" invariant is superseded;
     hallmark-floor.md carries the block (plugin-authored placement).
  8. build.sh is the post-fix17 file (23,276 lines; md5 recorded in the
     checks below) and still contains the 57-line fix15 block intact.
     The pre-fix16 values were 23,217 lines /
     1f1a232572b9e12332733688838e1233; the post-fix16 md5 changed again in
     the fix-up round (README counts + schema sentence in build.sh).
     The post-fix17 values are 23,276 lines /
     0775d6f33c5eeb4cf509fdee1cd319d7 (fix17 block, 55 lines, appended
     before STEP 5); updated by fix #17, following the fix #16 precedent —
     a baseline update, not an anchor change. The post-fix19 values are
     23,314 lines / a8d3d3c6f6d32344d0168c5323d9364b (fix19 block, 38
     lines); updated by fix #19, same precedent. Fix #19 also supersedes
     the C2 sentence itself (SPEC section 3 row 1): the C2 check now
     asserts the fix19 C2_NEW text, keeping the @font-face clause.
     The post-fix20 values are 23,349 lines /
     e5ff7d6ca7374c9de8348b1763b71f7e (fix20 block, 35 lines); updated by
     fix #20, same precedent. The post-weave20 values are 23,582 lines /
     766a35e47e83f921b4e30e8b4da36efd (weave20 block, 165 lines); updated
     by fix #20's weaving pass, same precedent. The post-fixup20 values are 23,582 lines /
     766a35e47e83f921b4e30e8b4da36efd (fixup20 block, 39 lines); updated
     by fix #20's fix-up pass (audit #62 + sweep #25), same precedent.
     The post-fixup20b values are 23,582 lines /
     766a35e47e83f921b4e30e8b4da36efd (fixup20b block, 27 lines; Batch E
     comment, +2 lines); updated by fix #20's second fix-up pass
     (sweep #26), same precedent. The post-fixup20c values are 23,609 lines /
     3c7b45bbfca8dbe10d10b9eb4b445160 (fixup20c block, 27 lines); updated
     by fix #20's third fix-up pass (sweep #27 + steers #3/#4/#5/#6),
     same precedent. The post-fixup20d values are 23,609 lines /
     785fb40580a4d91f7a480e1cdbc21f24 (comment-only lowercase-LAST
     normalization, 20 lines; no block appended); updated by fix #20's
     fourth fix-up pass (sweep #28 MINOR-1), same precedent.
     The post-fix21 values are 23,647 lines /
     8dfacb47a2a6698d47e4b4a5f8d9126c (fix21 block, 38 lines); updated
     by fix #21, same precedent.
"""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix15"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix19"))
from fix15 import CANONICAL, D1_RULE  # noqa: E402  (same constants as the fixer)
from fix19 import C2_NEW  # noqa: E402  (fix #19 supersedes the C2 sentence)

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = os.path.join(PLUGIN, "hackathon-ecc")
SPEC = os.path.join(PLUGIN, "fix15/SPEC.md")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


# 0. The fixer's canonical block matches SPEC.md's quoted block exactly.
spec = open(SPEC, encoding="utf-8").read()
qlines = []
in_block = False
for ln in spec.splitlines():
    if ln.startswith("> **Element variety, all theme-matched.**"):
        in_block = True
    if in_block:
        if ln.startswith("> "):
            qlines.append(ln[2:])
        elif ln.strip() == "":
            break
        else:
            break
spec_block = " ".join(qlines)
# The quoted block wraps across lines; normalise internal whitespace to compare.
norm = lambda s: re.sub(r"\s+", " ", s).strip()
check("CANONICAL in fix15.py matches the block quoted in SPEC.md",
      norm(spec_block) == norm(CANONICAL))

# 1. Canonical block verbatim, exactly once, in all 11 target files.
CANON_TARGETS = [
    "skills/design-taste-frontend/SKILL.md",
    "skills/ui-ux-pro-max/SKILL.md",
    "skills/less-flat-ui/SKILL.md",
    "skills/polish-pass/SKILL.md",
    "skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md",
    "skills/make-interfaces-feel-better/SKILL.md",
    "skills/motion-foundations/SKILL.md",
    "skills/motion-patterns/SKILL.md",
    "skills/motion-advanced/SKILL.md",
    "skills/orchestrate/SKILL.md",
    "skills/orch-build-mvp/SKILL.md",
]
for rel in CANON_TARGETS:
    text = read(rel)
    check(f"canonical block verbatim x1 in {rel}", text.count(CANONICAL) == 1)

# 2. R1-R5 anchors.
taste = read("skills/design-taste-frontend/SKILL.md")
orch = read("skills/orchestrate/SKILL.md")
mvp = read("skills/orch-build-mvp/SKILL.md")
lessflat = read("skills/less-flat-ui/SKILL.md")
check("R1 step 4: every dealt moment applied or re-dealt (Taste)",
      "Every dealt moment is applied or re-dealt (fix #15 R1 — baseline: iris-opens was dealt and never applied)" in taste)
check("R1 step 6 static check (Taste)",
      "Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)." in taste)
check("R1 static check in orchestrate 5a Verify",
      "Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)." in orch)
check("R1 static check in orch-build-mvp step 6 Verify",
      "Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)." in mvp)
check("R2: diagrams 1-2 by default, 0 only with recorded reason (Taste S3 table)",
      "1-2 by default, pulsing; 0 only with a recorded reason in the section plan" in taste
      and "0-2, pulsing | 0-2, pulsing | 0-1, still" not in taste)
check("R3: two distinct treatment kinds per app screen (less-flat-ui)",
      "at least TWO DISTINCT treatment kinds must be recorded per screen" in lessflat
      and "The second kind must be theme-matched (rule A governs the choice)" in lessflat)
check("R4: dealt hero's loop implemented or waived (Taste step 5)",
      "The dealt hero's loop is implemented or waived (fix #15 R4 — baseline: the centred-hero spec's loop inside the window was never applied)" in taste)
check("R5: Range pattern lead element is its own element (Taste step 4a)",
      "Each Range pattern's named lead element is its own element (fix #15 R5 — baseline: the Bento lead tile's lone figure was folded into the tile, not counted)" in taste)

# 3. C1-C3 anchors.
uipro = read("skills/ui-ux-pro-max/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
check("C1 Taste step 4a: dealt pairing is the ONLY permitted faces",
      "The dealt pairing is the ONLY permitted faces on the build — no other face is introduced — and the pairing + its source are recorded in `docs/design-tokens.md` (fix #15 C1)." in taste)
check("C1 ui-ux-pro-max type-scale step: dealt pairing/scale only faces",
      "The dealt pairing / type scale is the ONLY permitted faces on the build — no other face is introduced; record the pairing + its source in `docs/design-tokens.md` (fix #15 C1)." in uipro)
check("C2 Taste step 4a: self-host STATIC display faces, @font-face checkable (fix #19 supersedes the C2 sentence)",
      C2_NEW in taste
      and "the built page contains `@font-face` for the display face, and the tokens file names the source" in taste)
check("C3 Taste step 6: copy + type checks recorded in Type list",
      "Copy + type checks enforced and recorded (fix #15 C3)." in taste
      and "recorded in `docs/design-tokens.md`'s Type list (surface → face/size/measure/contrast)" in taste)
check("C3 polish-pass harmony verifies the Type list (consistency only)",
      "The harmony check also verifies the Type list in `docs/design-tokens.md` (surface → face/size/measure/contrast)" in polish
      and "recorded as candidate evidence, never a verdict (fix #15 C3 — consistency only)" in polish)

# 4. D1 anchors.
check("D1 rule in Taste step 6",
      D1_RULE in taste)
check("D1 rule in orchestrate step 5",
      D1_RULE in orch)
check("D1 final-report line in orchestrate step 6",
      "The final report names the screenshot QA pass (tool, screens, findings count) — a build that never ran a screenshot QA pass is incomplete and cannot be reported as finished (fix #15 D1)." in orch)
check("D1 rule in polish-pass Capture and verification",
      D1_RULE in polish)
check("D1 rule in orch-build-mvp step 6",
      D1_RULE in mvp)
check("D1 final-report line in orch-build-mvp step 9",
      "The final report names the screenshot QA pass (tool, screens, findings count) — a build that never ran a screenshot QA pass is incomplete and cannot be reported as finished (fix #15 D1)." in mvp)

# 5. Treatments still 23; staged less-flat-ui still == standalone + 4 patches
# (patch 4 is the weave20 design-decision pointer at the check-every-surface
# decision — a baseline update by fix #20's weaving pass, same precedent as
# the build.sh pin bump: the diff stays exactly the documented patches).
nums = [int(m) for m in re.findall(r"^### (\d+)\. ", lessflat, re.M)]
check("less-flat-ui treatments still number 1..23 exactly", nums == list(range(1, 24)))
check("patch 1 intact: wow-moment rule",
      "Texture in service of the wow moment, not decoration" in lessflat)
check("patch 2 intact: design-tokens record line in Shared utilities",
      "Record every treatment applied, on which surface, in `docs/design-tokens.md`" in lessflat)
check("patch 3 intact: re-tint warning after the treatments heading",
      "Re-tint every example below to the project's dealt palette" in lessflat)
check("patch 4 intact: weave20 design-decision pointer at check-every-surface",
      "**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate." in lessflat)
source_lf = open(os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md"),
                 encoding="utf-8").read()
sm = difflib.SequenceMatcher(None, source_lf.splitlines(), lessflat.splitlines())
nonequal = [op for op in sm.get_opcodes() if op[0] != "equal"]
check("staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks",
      len(nonequal) == 4)

# 6. Counts post-fix16.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (post-fix16)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 7. gates.md scrubbed (coordinator decision, fix-up round): staged == built
# and the text carries the scrubbed Cursor wording, not upstream's
# "Claude Code". hallmark-floor.md carries the block.
gates_built = read("skills/design-taste-frontend/references/hallmark/references/gates.md")
gates_src = open(os.path.join(PLUGIN, "new-skills/design-taste-frontend/references/hallmark/references/gates.md"),
                 encoding="utf-8").read()
check("gates.md staged == built (scrubbed Cursor wording, one documented hunk)",
      gates_built == gates_src
      and "(a subagent in Cursor)" in gates_built
      and "(in Cursor, `run_in_background: false`)" in gates_built
      and "Claude Code" not in gates_built)
check("canonical block NOT in gates.md", CANONICAL not in gates_built)
check("hallmark-floor.md carries the canonical block (plugin-authored placement)",
      read("skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md").count(CANONICAL) == 1)

# 8. build.sh is the post-fix16 file (23,221 lines, recorded md5) and still
# contains the 57-line fix15 block intact.
import hashlib
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",
      len(build_lines) == 23647
      and hashlib.md5(build.encode("utf-8")).hexdigest() == "8dfacb47a2a6698d47e4b4a5f8d9126c")
block_start = next((i for i, ln in enumerate(build_lines)
                    if ln.startswith("# --- fix15:")), -1)
ins = build_lines[block_start:block_start + 57] if block_start >= 0 else []
check("the 57-line fix15 block is still present intact in build.sh (fix15 header .. PYEOF)",
      len(ins) == 57 and ins[0].startswith("# --- fix15:")
      and ins[-2] == "PYEOF" and ins[-1] == ""
      and "fix15 upstream block applied" in "\n".join(ins))
check("build.sh contains the fix15 block marker",
      "fix15 upstream block applied" in build)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
