#!/usr/bin/env python3
"""verify19.py -- checks fix #19 in the BUILT tree (read-only).

Run after a build: python3 fix19/verify19.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. F2/F3/F4/D19 anchors present in Taste (built), ui-ux-pro-max (built,
     app mirrors), orchestrate (built).
  2. C2_NEW present in Taste + the F2/F3/F4 app note in ui-ux-pro-max;
     the old C2 sentence is GONE.
  3. STATIC19 present x3 (Taste step 6, orchestrate Verify 5a,
     orch-build-mvp step 6).
  4. POLISH_F19 present in polish-pass; TYPESET_F19 present and the old
     system-ui-legitimising sentence GONE from the typeset lens;
     LF_D19 present in less-flat-ui.
  5. D19_ROUTING + D19_REVIEWER present in orchestrate.
  6. Canonical block (fix #15) still verbatim x1 in all 11 files; D1 rule
     still present in Taste/orchestrate/polish-pass/orch-build-mvp.
  7. `system-ui` inventory by file class: zero in built-tree `*.md` rule
     files AFTER subtracting the placed fix19 rule texts (the rules
     themselves name `system-ui` as the banned token, so a literal
     tree-wide zero is wrong — see fix19/MANIFEST.md); zero in theme
     Tokens blocks; zero in the shipping templates (start.mjs, theme.mjs,
     shots.json x2); assets/ occurrences recorded at the 129 baseline;
     total remaining 147 (129 assets + 12 dev/QA tooling + 3 detectors +
     3 reference data) — with an explicit fail if any inventoried
     occurrence sits in a template that ships into built pages.
  8. Counts unchanged post-fix18: 166/72/123/87/15.
  9. No banned terms (fix #16 scrub) in the built skill tree (excl.
     node_modules).
 10. build.sh is the post-fix19 file (lines + md5 as recorded in
     fix19/MANIFEST.md) and still contains the fix15 + fix17 + fix19
     blocks intact. Updated by fix #20 to the post-fix20 values
     (23,349 lines, e5ff7d6ca7374c9de8348b1763b71f7e, fix20 block, 35
     lines) and by fix #20's weaving pass to the post-weave20 values
     (23,582 lines, 766a35e47e83f921b4e30e8b4da36efd, weave20 block, 165
     lines) — baseline updates, same precedent as fix #19's update of
     verify15/17/18, not anchor changes. Updated by fix #20's fix-up
     pass (audit #62 + sweep #25) to the post-fixup20 values (23,582
     lines, 766a35e47e83f921b4e30e8b4da36efd, fixup20 block, 39 lines) —
     same precedent. Updated by fix #20's second fix-up pass
     (sweep #26) to the post-fixup20b values (23,582 lines,
     766a35e47e83f921b4e30e8b4da36efd, fixup20b block, 27 lines;
     Batch E comment, +2 lines) — same precedent. Updated by fix #20's
     third fix-up pass (sweep #27 + steers #3/#4/#5/#6) to the
     post-fixup20c values (23,609 lines,
     3c7b45bbfca8dbe10d10b9eb4b445160, fixup20c block, 27 lines) —
     same precedent. Updated by fix #20's fourth fix-up pass
     (sweep #28 MINOR-1) to the post-fixup20d values (23,609 lines,
     785fb40580a4d91f7a480e1cdbc21f24, comment-only lowercase-LAST
     normalization, 20 lines; no block appended) — same precedent.
     Updated by fix #21 to the post-fix21 values (23,647 lines,
     8dfacb47a2a6698d47e4b4a5f8d9126c, fix21 block, 38 lines) — same
     precedent. The typeset-lens checkbox
     check was likewise updated by fix #20: fix #20 supersedes the
     fix19 checkbox, so the check now asserts the fix20 checkbox is
     present and the fix19 one is gone (and the check-7 subtraction
     list swaps in the fix20 checkbox text). Updated by fix #21: fix #21
     supersedes the fix20 checkbox, so the check now asserts the fix21
     checkbox is present and the fix20 one is gone (and the check-7
     subtraction list swaps in the fix21 checkbox text).
 11. verify15.py 43/43, verify17.py 59/59, verify18.py 72/72 (run as
     subprocesses, exit 0 required).
"""
import difflib
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix15"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix17"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix18"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix19"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix20"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix21"))
from fix15 import CANONICAL, D1_RULE  # noqa: E402
from fix17 import STATIC_CHECKS, E1_RULE  # noqa: E402
from fix18 import FEATURES_CUTS_SECTION  # noqa: E402
from fix19 import (F2_RULE, F3_RULE, F4_RULE, D19_RULE, STATIC19,  # noqa: E402
                   C2_NEW, C2_OLD, D19_ROUTING, D19_REVIEWER,
                   POLISH_F19, TYPESET_F19, TYPESET_OLD,
                   TYPESET_CHECKBOX_NEW, TYPESET_CHECKBOX_OLD, LF_D19,
                   F2_APP, F3_APP, F4_APP, D19_APP, C1_APP_NOTE,
                   START_MJS_OLD, THEME_MJS_OLD, SHOTS_SANS_OLD)
from fix20 import TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX20  # noqa: E402
from fix21 import TYPESET_CHECKBOX21_NEW as TYPESET_CHECKBOX21  # noqa: E402

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


taste = read("skills/design-taste-frontend/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
lessflat = read("skills/less-flat-ui/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
typeset = read("skills/polish-pass/reference/lenses/typeset.md")
orch = read("skills/orchestrate/SKILL.md")
mvp = read("skills/orch-build-mvp/SKILL.md")
start_mjs = read("skills/design-taste-frontend/scripts/start.mjs")
theme_mjs = read("skills/design-taste-frontend/references/hallmark/scripts/theme.mjs")
shots = read("skills/pitch-deck-video/template/shots.json")
shots_ex = read("skills/pitch-deck-video/template/shots.example.json")

# 1. F2/F3/F4/D19 in Taste, ui-ux-pro-max (app mirrors), orchestrate.
check("F2 Taste step 4a: static bundled files only",
      F2_RULE in taste)
check("F3 Taste step 4a: font choice unique and interesting, forced",
      F3_RULE in taste)
check("F4 Taste step 4a: plain/body text uses Tiempos",
      F4_RULE in taste)
check("D19 Taste step 4a: thought-out reason, full experience",
      D19_RULE in taste)
check("F2/F3/F4/D19 orchestrate design-package rule",
      F2_RULE in orch and F3_RULE in orch and F4_RULE in orch
      and D19_RULE in orch)
check("F2_APP ui-ux-pro-max anti-generic bar",
      F2_APP in uipro)
check("F3_APP ui-ux-pro-max anti-generic bar",
      F3_APP in uipro)
check("F4_APP ui-ux-pro-max anti-generic bar",
      F4_APP in uipro)
check("D19_APP ui-ux-pro-max anti-generic bar",
      D19_APP in uipro)
check("D19_APP orch-build-mvp step 4",
      D19_APP in mvp)
check("D19 six dimensions named in Taste (Motion/Theme/Texture/Visuals/Techniques/Colors)",
      all(d in taste for d in
          ["Motion", "Theme", "Texture", "Visuals", "Techniques", "Colors"]))
check("D19 explicit-none form named in Taste",
      "none — <reason>" in taste)

# 2. C2 replacement + C1 app note.
check("C2_NEW present in Taste step 4a",
      C2_NEW in taste)
check("old C2 sentence GONE from Taste",
      C2_OLD not in taste)
check("C1 app note present in ui-ux-pro-max type-scale step",
      C1_APP_NOTE in uipro)

# 3. STATIC19 x3.
check("STATIC19 Taste step 6", STATIC19 in taste)
check("STATIC19 orchestrate Verify 5a", STATIC19 in orch)
check("STATIC19 orch-build-mvp step 6", STATIC19 in mvp)
check("STATIC19 sits after the fix17 checks in Taste step 6",
      taste.find(STATIC19) > taste.find(STATIC_CHECKS))
check("STATIC19 sits after the fix17 checks in orchestrate 5a",
      orch.find(STATIC19) > orch.find(STATIC_CHECKS))
check("STATIC19 sits after the fix17 checks in orch-build-mvp step 6",
      mvp.find(STATIC19) > mvp.find(STATIC_CHECKS))
check("STATIC19 in orchestrate 5a is before the 5b bullet (not injected into it)",
      orch.find(STATIC19) < orch.find("**5b. Final polish**"))

# 4. Polish-pass / typeset lens / less-flat-ui.
check("POLISH_F19 present in polish-pass harmony",
      POLISH_F19 in polish)
check("TYPESET_F19 present in typeset lens",
      TYPESET_F19 in typeset)
check("old system-ui-legitimising sentence GONE from typeset lens",
      TYPESET_OLD not in typeset)
check("typeset lens checkbox updated (fix #21 supersedes the fix20 checkbox)",
      TYPESET_CHECKBOX21 in typeset and TYPESET_CHECKBOX_FIX20 not in typeset)
check("LF_D19 present in less-flat-ui record section",
      LF_D19 in lessflat)

# 5. D19 routing + reviewer in orchestrate.
check("D19_ROUTING present in orchestrate routing line",
      D19_ROUTING in orch)
check("D19_REVIEWER present in orchestrate blind-reviewer check",
      D19_REVIEWER in orch)

# 6. Fix #15 anchors intact (canonical block + D1) + fix18 anchor.
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
check("D1 rule still in Taste step 6", D1_RULE in taste)
check("D1 rule still in orchestrate step 5", D1_RULE in orch)
check("D1 rule still in polish-pass Capture", D1_RULE in polish)
check("D1 rule still in orch-build-mvp step 6", D1_RULE in mvp)
check("fix18 FEATURES_CUTS_SECTION still in pitch-deck-video shots-reference.md",
      FEATURES_CUTS_SECTION in read("skills/pitch-deck-video/references/shots-reference.md"))
check("fix17 E1 rule still in Taste step 4a", E1_RULE in taste)

# 7. system-ui inventory by file class.
# The fix19 rule texts themselves name `system-ui` as the banned token
# (F2_RULE x3, STATIC19 x1, C2_NEW x1, POLISH_F19 x1, TYPESET_F19 x1,
# F2_APP x1), plus the CURRENT typeset checkbox (fix #21's, which
# superseded fix20's TYPESET_CHECKBOX_NEW 1-for-1 and names `system-ui`
# once, so the *.md mention total stays 14) — a literal *.md zero is
# wrong: subtract the placed rule texts, then assert zero remains.
RULE_TEXTS_WITH_SYSTEM_UI = [F2_RULE, F2_APP, STATIC19, C2_NEW, POLISH_F19,
                             TYPESET_F19, TYPESET_CHECKBOX21]


def md_system_ui_after_rules(rel):
    text = read(rel)
    for rule in RULE_TEXTS_WITH_SYSTEM_UI:
        text = text.replace(rule, "")
    return text.count("system-ui")


md_files = []
for root, _dirs, files in os.walk(BASE):
    if "node_modules" in root:
        continue
    for f in files:
        if f.endswith(".md"):
            md_files.append(os.path.relpath(os.path.join(root, f), BASE))
leftover = {rel: md_system_ui_after_rules(rel) for rel in md_files}
leftover = {k: v for k, v in leftover.items() if v}
check("system-ui zero in *.md rule files after subtracting placed rule texts",
      leftover == {})
if leftover:
    print("   leftover system-ui in .md files: %r" % (leftover,))

theme_files = sorted(glob.glob(os.path.join(
    BASE, "skills/design-taste-frontend/references/hallmark/references/themes/*.md")))
theme_hits = sum(open(p, encoding="utf-8").read().count("system-ui")
                 for p in theme_files)
check("system-ui zero in all 30 theme files (Tokens blocks stripped)",
      theme_hits == 0)
check("system-ui zero in start.mjs (stack fallback)",
      "system-ui" not in start_mjs)
check("old start.mjs stack GONE", START_MJS_OLD not in start_mjs)
check("system-ui zero in theme.mjs CUSTOM_TOKENS",
      "system-ui" not in theme_mjs)
check("old theme.mjs font line GONE", THEME_MJS_OLD not in theme_mjs)
check("system-ui zero in pitch-deck-video shots.json",
      "system-ui" not in shots)
check("system-ui zero in pitch-deck-video shots.example.json",
      "system-ui" not in shots_ex)
check("old shots.json sans stack GONE", SHOTS_SANS_OLD not in shots)
check("old shots.example.json sans stack GONE", SHOTS_SANS_OLD not in shots_ex)


def grep_count(paths, extra_args=()):
    r = subprocess.run(["grep", "-r", "-o", "system-ui", "--exclude-dir=node_modules"]
                       + list(extra_args) + paths,
                       cwd=BASE, capture_output=True, text=True)
    return len(r.stdout.splitlines()) if r.stdout.strip() else 0


assets_n = grep_count(["skills/design-taste-frontend/assets"])
check("assets/ demo occurrences recorded at the 129 baseline",
      assets_n == 129)
tooling_n = grep_count([
    "skills/design-taste-frontend/scripts/fx-gallery.template.html",
    "skills/design-taste-frontend/scripts/fx-lab.template.html",
    "skills/design-taste-frontend/scripts/moments.mjs",
    "skills/design-taste-frontend/references/hallmark/scripts/sloplint-render.mjs",
    "scripts/lib/control-pane/control-plane-view-ui.js",
    "scripts/lib/control-pane/proximity-viz.js",
    "scripts/lib/control-pane/ui.js"])
check("dev/QA tooling occurrences recorded at 12", tooling_n == 12)
detectors_n = grep_count([
    "skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs",
    "skills/design-taste-frontend/scripts/consistency.mjs"])
check("detector occurrences kept at 3 (sloplint/consistency name the ban)",
      detectors_n == 3)
data_n = grep_count(["skills/ui-ux-pro-max/data/styles.csv"])
check("reference-data occurrences recorded at 3 (styles.csv)", data_n == 3)
# The 14 remaining *.md mentions are the fix19 rule texts themselves
# naming `system-ui` as the banned token (Taste 5, orchestrate 4,
# typeset lens 2, orch-build-mvp 1, polish-pass 1, ui-ux-pro-max 1) —
# all covered by the subtraction check above, not font stacks.
md_mentions_n = grep_count(["."], extra_args=("--include=*.md",))
check("*.md rule-text mentions of system-ui number exactly 14",
      md_mentions_n == 14)
total_n = grep_count(["."])
check("total remaining system-ui is 161 (129 + 12 + 3 + 3 + 14 rule-text mentions)",
      total_n == 161
      and total_n == assets_n + tooling_n + detectors_n + data_n + md_mentions_n)

# 8. Treatments still 23; staged-vs-standalone less-flat-ui diff still 4 hunks
# (patch 4 is the weave20 design-decision pointer — baseline update by fix
# #20's weaving pass, same precedent as the build.sh pin bump).
nums = [int(m) for m in re.findall(r"^### (\d+)\. ", lessflat, re.M)]
check("less-flat-ui treatments still number 1..23 exactly", nums == list(range(1, 24)))
check("patch 4 intact: weave20 design-decision pointer at check-every-surface",
      "**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate." in lessflat)
source_lf = open(os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md"),
                 encoding="utf-8").read()
sm = difflib.SequenceMatcher(None, source_lf.splitlines(), lessflat.splitlines())
nonequal = [op for op in sm.get_opcodes() if op[0] != "equal"]
check("staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks",
      len(nonequal) == 4)

# 9. Counts unchanged post-fix18.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 10. No banned terms in the built skill tree (excl. node_modules).
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")

# 11. build.sh post-fix21 (23,647 lines, md5 8dfacb47..., fix21 block,
# 38 lines). Updated by fix #21 from the post-fixup20d values,
# same baseline-update precedent as fix #19's update of
# verify15/17/18 — a baseline update, not an anchor change.
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",
      len(build_lines) == 23647
      and hashlib.md5(build.encode("utf-8")).hexdigest() == "8dfacb47a2a6698d47e4b4a5f8d9126c")
check("build.sh has MORE lines than post-fix19 (23,314)",
      len(build_lines) > 23314)
check("build.sh contains the fix20 block marker",
      "fix20 upstream block applied" in build)
check("build.sh contains the fix19 block marker",
      "fix19 upstream block applied" in build)
check("build.sh still contains the fix17 block marker",
      "fix17 upstream block applied" in build)
check("build.sh still contains the fix15 block marker",
      "fix15 upstream block applied" in build)

# 12. verify15/17/18 still pass.
for name, script, expected in (("fix15", "fix15/verify15.py", "43/43"),
                               ("fix17", "fix17/verify17.py", "59/59"),
                               ("fix18", "fix18/verify18.py", "72/72")):
    r = subprocess.run(["python3", script], cwd=PLUGIN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    check(f"{name} verifier still passes ({tail})", r.returncode == 0)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
