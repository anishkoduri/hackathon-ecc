#!/usr/bin/env python3
"""verify21.py -- checks fix #21 in the BUILT tree (read-only).

Run after a build: python3 fix21/verify21.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. F4_TIGHT/F7 anchors present in Taste (built) and orchestrate
     (built), after the X1 rule in each.
  2. F4_TIGHT_APP/F7_APP present in ui-ux-pro-max (built) and
     orch-build-mvp (built), after X1_APP in each.
  3. STATIC21 present x3 (Taste step 6, orchestrate Verify 5a,
     orch-build-mvp step 6); after STATIC20 in each; in orchestrate
     before the 5b bullet; STATIC21 contains the F7 per-element item.
  4. POLISH_F21 present in polish-pass; TYPESET_F21 present in the
     typeset lens; TYPESET_CHECKBOX21_NEW present and the fix20
     checkbox GONE.
  5. Fix20 anchors intact: F4_SCOPE/F5/F6/B1/X1 still present verbatim
     in Taste and orchestrate; F4_SCOPE_APP/F5_APP/F6_APP/B1_APP/X1_APP
     still present in ui-ux-pro-max and orch-build-mvp; STATIC20 still
     present x3. Fix19 anchors intact: F4_RULE still present verbatim
     in Taste and orchestrate; F4_APP still present in ui-ux-pro-max;
     STATIC19 still present x3; D19_RULE still present in Taste and
     orchestrate; D19_APP still present in ui-ux-pro-max and
     orch-build-mvp.
  6. Canonical block (fix #15) still verbatim x1 in all 11 files; D1 rule
     still present in Taste/orchestrate/polish-pass/orch-build-mvp.
  7. vantage.md UNCHANGED in the built tree (display and body still
     Geologica) — this fix governs the deal, it does not rewrite theme
     data; the scope rule text names the collision handling.
  8. Counts unchanged post-fix20: 166/72/123/87/15.
  9. No banned terms (fix #16 scrub) in the built skill tree (excl.
     node_modules).
 10. build.sh is the post-fix21 file: it contains the fix15 + fix17 +
     fix19 + fix20 + fix21 blocks intact and has MORE lines than post-fix20
     (23,609). Lines + md5 are matched against fix21/MANIFEST.md WHEN
     that MANIFEST exists — the coordinator writes the MANIFEST (not the
     fix21 worker), so until it exists this check records the measured
     lines + md5 for the coordinator and passes on the marker/line-count
     evidence; see fix21.py's docstring.
 11. verify15.py 44/44, verify17.py 60/60, verify18.py 72/72,
     verify19.py 76/76, verify20.py 169/169 (run as subprocesses,
     exit 0 required).
 12. Interconnection: the F4_TIGHT/F7 tokens resolve to defining
     phrases in the built tree; every §10 pointer line still targets
     the design-package rule, which carries the new rules (the
     pointer chain is connected, no dead end, no duplicate pointer
     lines added by this fix).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
for sub in ("fix15", "fix17", "fix18", "fix19", "fix20", "fix21"):
    sys.path.insert(0, os.path.join(PLUGIN, sub))
from fix15 import CANONICAL, D1_RULE  # noqa: E402
from fix17 import E1_RULE  # noqa: E402
from fix18 import FEATURES_CUTS_SECTION  # noqa: E402
from fix19 import (F4_RULE, D19_RULE, STATIC19, F4_APP, D19_APP,  # noqa: E402
                   TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX19)
from fix20 import (F4_SCOPE, F5, F6, B1, X1, STATIC20,  # noqa: E402
                   F4_SCOPE_APP, F5_APP, F6_APP, B1_APP, X1_APP,
                   POLISH_F20, POLISH_F20_BX1, TYPESET_F20,
                   TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_FIX20)
from fix21 import (F4_TIGHT, F7, STATIC21,  # noqa: E402
                   F4_TIGHT_APP, F7_APP, POLISH_F21, TYPESET_F21,
                   TYPESET_CHECKBOX21, TYPESET_CHECKBOX21_NEW)

BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


taste = read("skills/design-taste-frontend/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
typeset = read("skills/polish-pass/reference/lenses/typeset.md")
orch = read("skills/orchestrate/SKILL.md")
mvp = read("skills/orch-build-mvp/SKILL.md")

# 1. F4_TIGHT/F7 in Taste and orchestrate, after X1.
for label, text in (("Taste step 4a", taste),
                    ("orchestrate design-package rule", orch)):
    check(f"F4_TIGHT {label}: Tiempos rule is long body + small text only", F4_TIGHT in text)
    check(f"F7 {label}: every text element gets an artistic font design decision", F7 in text)
    check(f"fix21 rules sit after the X1 rule in {label}",
          text.find(F4_TIGHT) > text.find(X1)
          and text.find(F7) > text.find(F4_TIGHT))
check("F4_TIGHT names long-length body text and small incidental text only",
      "LONG-LENGTH body text and SMALL incidental text only" in taste
      and "LONG-LENGTH body text and SMALL incidental text only" in orch)
check("F4_TIGHT: the body face is never a default for text generally",
      "They are NOT a default for text generally" in taste
      and "They are NOT a default for text generally" in orch)
check("F7: a blanket 'all text' line is not a class decision",
      "a blanket 'all text' line is not a class decision" in taste
      and "a blanket 'all text' line is not a class decision" in orch)
check("F7: the font decision is the D19 reason for that text element's font choice",
      "the font decision is the D19 reason for that text element's font choice" in taste
      and "the font decision is the D19 reason for that text element's font choice" in orch)

# 2. App mirrors in ui-ux-pro-max and orch-build-mvp, after X1_APP.
for label, text in (("ui-ux-pro-max anti-generic bar", uipro),
                    ("orch-build-mvp step 4", mvp)):
    check(f"F4_TIGHT_APP {label}", F4_TIGHT_APP in text)
    check(f"F7_APP {label}", F7_APP in text)
    check(f"fix21 app mirrors sit after X1_APP in {label}",
          text.find(F4_TIGHT_APP) > text.find(X1_APP)
          and text.find(F7_APP) > text.find(F4_TIGHT_APP))

# 3. STATIC21 x3, after STATIC20, before 5b in orchestrate, F7 item.
check("STATIC21 Taste step 6", STATIC21 in taste)
check("STATIC21 orchestrate Verify 5a", STATIC21 in orch)
check("STATIC21 orch-build-mvp step 6", STATIC21 in mvp)
check("STATIC21 sits after STATIC20 in Taste step 6",
      taste.find(STATIC21) > taste.find(STATIC20))
check("STATIC21 sits after STATIC20 in orchestrate 5a",
      orch.find(STATIC21) > orch.find(STATIC20))
check("STATIC21 sits after STATIC20 in orch-build-mvp step 6",
      mvp.find(STATIC21) > mvp.find(STATIC20))
check("STATIC21 in orchestrate 5a is before the 5b bullet (not injected into it)",
      orch.find(STATIC21) < orch.find("**5b. Final polish**"))
check("STATIC21 contains the F7 per-element item (every text element carries its recorded decision)",
      "(F7) Every text element in the Type list" in STATIC21
      and "(F7) Every text element in the Type list" in taste)

# 4. Polish-pass / typeset lens.
check("POLISH_F21 present in polish-pass harmony", POLISH_F21 in polish)
check("POLISH_F21 sits after POLISH_F20 in polish-pass",
      polish.find(POLISH_F21) > polish.find(POLISH_F20))
check("TYPESET_F21 present in typeset lens", TYPESET_F21 in typeset)
check("TYPESET_F21 sits after TYPESET_F20 in the typeset lens",
      typeset.find(TYPESET_F21) > typeset.find(TYPESET_F20))
check("typeset lens checkbox updated to fix #21 (fix20 checkbox gone)",
      TYPESET_CHECKBOX21_NEW in typeset
      and TYPESET_CHECKBOX_FIX20 not in typeset)
check("typeset lens checkbox names the fix #21 F7 per-element decision",
      "every text element has a recorded artistic font decision (fix #21 F7)" in typeset)

# 5. Fix20 anchors intact.
for label, text in (("Taste", taste), ("orchestrate", orch)):
    check(f"F4_SCOPE still verbatim in {label}", F4_SCOPE in text)
    check(f"F5 still verbatim in {label}", F5 in text)
    check(f"F6 still verbatim in {label}", F6 in text)
    check(f"B1 still verbatim in {label}", B1 in text)
    check(f"X1 still verbatim in {label}", X1 in text)
for label, text in (("ui-ux-pro-max", uipro), ("orch-build-mvp", mvp)):
    check(f"F4_SCOPE_APP still verbatim in {label}", F4_SCOPE_APP in text)
    check(f"F5_APP still verbatim in {label}", F5_APP in text)
    check(f"F6_APP still verbatim in {label}", F6_APP in text)
    check(f"B1_APP still verbatim in {label}", B1_APP in text)
    check(f"X1_APP still verbatim in {label}", X1_APP in text)
check("STATIC20 still present in Taste step 6", STATIC20 in taste)
check("STATIC20 still present in orchestrate Verify 5a", STATIC20 in orch)
check("STATIC20 still present in orch-build-mvp step 6", STATIC20 in mvp)
# Fix19 anchors intact.
check("F4_RULE still verbatim in Taste", F4_RULE in taste)
check("F4_RULE still verbatim in orchestrate", F4_RULE in orch)
check("D19_RULE still verbatim in Taste", D19_RULE in taste)
check("D19_RULE still verbatim in orchestrate", D19_RULE in orch)
check("F4_APP still verbatim in ui-ux-pro-max", F4_APP in uipro)
check("STATIC19 still present in Taste step 6", STATIC19 in taste)
check("STATIC19 still present in orchestrate Verify 5a", STATIC19 in orch)
check("STATIC19 still present in orch-build-mvp step 6", STATIC19 in mvp)
check("D19_APP still verbatim in ui-ux-pro-max", D19_APP in uipro)
check("D19_APP still verbatim in orch-build-mvp", D19_APP in mvp)

# 6. Fix #15 anchors intact (canonical block + D1) + fix17/fix18 anchors.
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

# 7. vantage.md UNCHANGED (display and body still Geologica).
vantage = read("skills/design-taste-frontend/references/hallmark/references/themes/vantage.md")
check("vantage.md still names Geologica for display AND body (unchanged)",
      '--font-display: "Geologica"; --font-body: "Geologica";' in vantage)
check("F4_TIGHT names the role-scoping from fix #20 (collision handling)",
      "the role-scoping from fix #20 stands" in taste)

# 8. Counts unchanged post-fix20.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 9. No banned terms in the built skill tree (excl. node_modules).
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")
if hits:
    print("   banned-term files: %r" % (hits,))

# 10. build.sh post-fix21.
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()
check("build.sh contains the fix21 block marker",
      "fix21 upstream block applied" in build)
check("build.sh still contains the fix20 block marker",
      "fix20 upstream block applied" in build)
check("build.sh still contains the fix19 block marker",
      "fix19 upstream block applied" in build)
check("build.sh still contains the fix17 block marker",
      "fix17 upstream block applied" in build)
check("build.sh still contains the fix15 block marker",
      "fix15 upstream block applied" in build)
check("build.sh has MORE lines than post-fix20 (23,609)",
      len(build_lines) > 23609)
manifest_path = os.path.join(PLUGIN, "fix21/MANIFEST.md")
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    check("fix21/MANIFEST.md records build.sh lines + md5",
          bool(m_lines and m_md5))
    if m_lines and m_md5:
        check(f"build.sh is {m_lines.group(1)} lines, md5 {m_md5.group(1)} (post-fix21)",
              len(build_lines) == int(m_lines.group(1))
              and build_md5 == m_md5.group(1))
else:
    print(f"   NOTE: fix21/MANIFEST.md not yet written by the coordinator; "
          f"measured build.sh lines={len(build_lines)}, md5={build_md5}")
    check("build.sh lines + md5 measured for the coordinator's MANIFEST "
          f"(lines={len(build_lines)}, md5={build_md5})", True)

# 11. verify15/17/18/19/20 still pass.
for name, script in (("fix15", "fix15/verify15.py"),
                     ("fix17", "fix17/verify17.py"),
                     ("fix18", "fix18/verify18.py"),
                     ("fix19", "fix19/verify19.py"),
                     ("fix20", "fix20/verify20.py")):
    r = subprocess.run(["python3", script], cwd=PLUGIN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    check(f"{name} verifier still passes ({tail})", r.returncode == 0)

# 12. Interconnection: F4_TIGHT/F7 tokens resolve; the §10 pointer chain
# still targets the design-package rule, which carries the new rules.
def _tree_has(phrase):
    r = subprocess.run(["grep", "-r", "-F", "-q", phrase, "skills"],
                       cwd=BASE, capture_output=True, text=True)
    return r.returncode == 0


check("interconnection: F4_TIGHT token resolves to a defining phrase in the built tree",
      _tree_has("Long body and small text only"))
check("interconnection: F7 token resolves to a defining phrase in the built tree",
      _tree_has("Every text element gets an artistic font design decision"))
check("interconnection: the design-package rule exists in built orchestrate",
      "**Design-package rule (row 10" in orch)
check("interconnection: the design-package rule carries the new F4_TIGHT/F7 rules (no dead end)",
      F4_TIGHT in orch and F7 in orch)
WEAVE_MARKER = "Design-decision pointer:"
_pointer_hits = 0
_pointer_bad = []
for _skill in os.listdir(os.path.join(BASE, "skills")):
    _text = read(f"skills/{_skill}/SKILL.md")
    for _line in _text.split("\n"):
        if WEAVE_MARKER in _line:
            _pointer_hits += 1
            if "design-package rule" not in _line:
                _pointer_bad.append((_skill, "no design-package-rule target"))
check(f"interconnection: all {_pointer_hits} design-decision pointer lines still target the design-package rule (no duplicate lines added)",
      _pointer_hits == 32 and not _pointer_bad)
if _pointer_bad:
    print("   bad pointers: %r" % (_pointer_bad,))

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
