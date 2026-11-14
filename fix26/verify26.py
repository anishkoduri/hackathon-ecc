#!/usr/bin/env python3
"""verify26.py -- checks fix #26 in the BUILT tree (read-only).

Run after a build: python3 fix26/verify26.py
Exits 0 only if every check passes.

Fix #26 is the "close up those small items" turn (SPEC §0-§10): the §1
pip pinning (20 real category-(a) lines: 7 staged in pitch-deck-video,
13 upstream via fix26.py), the §2 F-14 /demo stale-README mechanism
(step 7 links a later-filmed video into the README itself,
README_UPDATE_F26), the §3 stale build.sh fix25 comment rewrite (plus
the fix26 comment itself, Audit #73 M2, and the verify25 docstring,
Audit #73 M1), the §4 variable-font scoped exception recorded as
inventory §11 (VARFONT_F26), the §5 trigger-router B6
DOCUMENTATION-ONLY disposition (plus the generator's :383 comment and
:342 flow emission, Sweep #34 minors 1-2), the §6 benchmark Dim 7
recorded decision OWED (never a pass), the §7 fix #17 R1/R4 OWED
against the Home Run render, and the §8 ck cost lines corrected to the
measured ~1k tokens/session (KEEP).

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc
(+ build.sh where the SPEC says so):

  1. Global: build.sh fingerprint (24,088 lines, md5 e1944a6e...);
     diff vs build.sh.before-fix23 additions only (+314/-0); fix26
     patch log 16 changes / 0 errors (build-log-run4: 16 change(s),
     OK); counts 166/72/123/87/15, trigger keys 64; banned terms 0;
     Grok pins only (grok-4.7-high x54, cursor-grok-4.6-high-fast
     x103, bare x0).
  2. §1 pip pins: 42 `pip install` lines in the built tree, 20 pinned
     (==), 22 unpinned by design ((b)/(c)/(d)); all 13 upstream pins
     present (P-01-P-13); all 7 staged pins present; the yt-dlp line
     that verify24 E-5 asserted unpinned is now pinned; the only
     unpinned named-package line is the tts.mjs:180 error string.
  3. §2 F-14: README_UPDATE_F26 x4 (staged + built); step 7 rules
     (ledger first, idempotent edit, no README, re-cut no-op, final
     report not rewritten); orchestrate :101 clause, readme-writer
     :95, demo.md :9.
  4. §3 comment fix: build.sh fix25 comment matches the comment-fix
     "After" block (7 lines); fix26 comment header names ck + §1 pip
     pins and :24075 names the 13 upstream lines (Audit #73 M2);
     verify25.py docstring says +314/-0, no +305 left (M1).
  5. §4 varfont: VARFONT_F26 x1 in inventory §11 (template only,
     Hanken + JetBrains variable, Instrument static); font sizes
     34704 / 21032 / 30376; app-UI static-only stands.
  6. §5 B6: call-map :38 DOCUMENTATION-ONLY; 128 qualified flow
     strings, 0 bare "on-request (trigger-routed)"; generator :342
     emits the qualified string and :383 calls skill-triggers a
     documentation-only reference table (Sweep #34 minors 1-2);
     call-map-data.json trigger_only [] and counts agree; no "live
     routing table" claim anywhere (outside the B6 "not a live"
     phrasing).
  7. §6/§7 owed records: benchmark Dim 7 "NONE RECORDED (no v5
     figure)", "owed, never claimed statically"; no Campus Eats
     index.html; dim7-note + r1r4-note record OWED, not verified.
  8. §8 ck KEEP: three cost lines corrected to ~1k tokens/session;
     session-start.mjs:129 block figure (~100 tokens) kept; no other
     stale cost claim in the ck tree.
  9. Cross-cutting: _F26 census README_UPDATE_F26 4 / VARFONT_F26 1;
     _F25 census unchanged (1/1/2/10/8/2/6/3); /demo gates intact;
     counts unchanged.
 10. Prior-verifier regression leg: fix15/17/18/19/20/21/22/23/24/25/13h
     re-run. EXPECTED fails are ONLY the codified tails below. Any fail
     outside that pattern is a REAL regression. Exact tails are
     asserted so a new fail changes the count:
       fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76,
       fix20 164/169, fix21 96/102, fix22 366/369,
       fix23 194/211 excl. manifest,
       fix24 97/104 excl. manifest (moved from 98/104: E-5, the
         yt-dlp line verify24.py:389 asserted unpinned is now pinned
         by fix #26 §1 -- see pip-pinning.md flag 1),
       fix25 72/74 excl. manifest (moved from 75/75: the fingerprint
         check (build.sh moved on), the fix24-tail expectation
         (97/104 vs 98/104), and the manifest check (fix25/MANIFEST.md
         records the fix25 fingerprint, now stale by design)),
       verify13h 6/97 fail (2 B2 + M3 :61, :62, :70, :71 -- the three
         F-04 checks :57, :63, :66 pass after worker C's update).
 11. Manifest check (fix22 pattern): runs once fix26/MANIFEST.md exists.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
sys.path.insert(0, os.path.join(PLUGIN, "fix19"))
from fix19 import D19_RULE, D19_ROUTING, D19_REVIEWER, POLISH_F19  # noqa: E402

BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


def read_plugin(rel):
    return open(os.path.join(PLUGIN, rel), encoding="utf-8").read()


def lines_with(token, text):
    return sum(1 for ln in text.splitlines() if token in ln)


def count_occ(token, text):
    return text.count(token)


def csv_rows(rel):
    with open(os.path.join(BASE, rel), encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # minus the header row


def count_substring_in_tree(sub, dirs=("skills", "agents", "commands", "rules", "hooks")):
    n = 0
    for d in dirs:
        for root, _dirs, files in os.walk(os.path.join(BASE, d)):
            _dirs[:] = [x for x in _dirs if x != "node_modules"]
            for fn in files:
                try:
                    t = open(os.path.join(root, fn), encoding="utf-8", errors="strict").read()
                except (UnicodeDecodeError, ValueError):
                    continue
                n += t.count(sub)
    return n


def grep_tree(sub, dirs=("skills", "agents", "commands", "rules", "hooks")):
    hits = []
    for d in dirs:
        for root, _dirs, files in os.walk(os.path.join(BASE, d)):
            _dirs[:] = [x for x in _dirs if x != "node_modules"]
            for fn in files:
                p = os.path.join(root, fn)
                try:
                    t = open(p, encoding="utf-8", errors="strict").read()
                except (UnicodeDecodeError, ValueError):
                    continue
                for i, ln in enumerate(t.splitlines(), 1):
                    if sub in ln:
                        hits.append((os.path.relpath(p, BASE), i, ln))
    return hits


orch = read("skills/orchestrate/SKILL.md")
grill = read("skills/grill-me/SKILL.md")
scope = read("skills/hackathon-scope/SKILL.md")
fe = read("skills/feature-expansion/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
bqa = read("skills/browser-qa/SKILL.md")
taste = read("skills/design-taste-frontend/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
inv = read("skills/orchestrate/references/design-inventory.md")
callmap = read("skills/orchestrate/references/call-map.md")
bench = read("skills/orchestrate/references/design-benchmark-v5.md")
pitch = read("skills/pitch-deck-video/SKILL.md")
fonts_ts = read("skills/pitch-deck-video/template/src/fonts.ts")
fonts_pkg = read("skills/pitch-deck-video/template/package.json")
launch_mkt = read("skills/mobile-ship/references/launch-marketing.md")
prp_commit = read("commands/prp-commit.md")
session_start = read("hooks/session-start.js")
ck_skill = read("skills/ck/SKILL.md")
ck_mjs = read("skills/ck/hooks/session-start.mjs")
readme_writer = read("skills/readme-writer/SKILL.md")
demo_md = read("commands/demo.md")
shots_ref = read("skills/pitch-deck-video/references/shots-reference.md")
trouble = read("skills/pitch-deck-video/references/troubleshooting.md")
tts_mjs = read("skills/pitch-deck-video/template/scripts/tts.mjs")
generator = read_plugin("fix25/callmap/generate_call_map.py")
dim7_note = read_plugin("fix26/dim7-note.md")
r1r4_note = read_plugin("fix26/r1r4-note.md")
verify25_text = read_plugin("fix25/verify25.py")
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()

# 1. Global fingerprint / counts / pins / banned terms.
check("build.sh is 24,088 lines, md5 e1944a6e2b81bf3b869c191633c04aae (post-fix26)",
      len(build_lines) == 24088
      and build_md5 == "e1944a6e2b81bf3b869c191633c04aae")
_diff = subprocess.run(
    ["diff", "build.sh.before-fix23", "build.sh"],
    cwd=PLUGIN, capture_output=True, text=True).stdout
_diff_add = sum(1 for ln in _diff.splitlines() if ln.startswith(">"))
_diff_del = sum(1 for ln in _diff.splitlines() if ln.startswith("<"))
check("diff vs build.sh.before-fix23 is additions only (+314/-0)",
      _diff_add == 314 and _diff_del == 0)
if _diff_del:
    print(f"   deletions in diff: {_diff_del}")
_patchlog = read_plugin("fix26/fix26-patch-log.md")
check("fix26 patch log: 16 changes, 0 errors",
      "## Changes (16)" in _patchlog and "## Errors (0)" in _patchlog)
_run4 = read_plugin("fix26/build-log-run4.txt")
check("fix26 run log (run 4): 16 change(s), fix26 OK",
      "fix26: 16 change(s)" in _run4 and "fix26: OK" in _run4)


def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))


hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged -- no new skill/command/trigger)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))
_triggers = json.load(open(os.path.join(
    BASE, "manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
check("trigger keys still 64 (no new trigger from this fix)",
      _triggers["coverage"]["withTriggers"] == len(_triggers["triggers"]) == 64)
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")
if hits:
    print("   banned-term files: %r" % (hits,))
_bare_grok = subprocess.run(
    ["grep", "-rn", "grok-4.6-high-fast", "skills", "agents", "commands",
     "rules", "hooks", "README.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout
_bare_grok = "\n".join(
    ln for ln in _bare_grok.splitlines() if "cursor-grok-4.6-high-fast" not in ln)
check("bare grok-4.6-high-fast absent (Grok pins only)",
      _bare_grok.strip() == "")
_g47 = subprocess.run(
    ["grep", "-ro", "grok-4.7-high", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
_c46 = subprocess.run(
    ["grep", "-ro", "cursor-grok-4.6-high-fast", ".", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("Grok pins: grok-4.7-high x54, cursor-grok-4.6-high-fast x103 (occurrences)",
      len(_g47.splitlines()) == 54 and len(_c46.splitlines()) == 103)

# 2. §1 pip pins.
_pip_lines = []
for _d in ("skills", "agents", "commands", "rules", "hooks", "scripts", "manifests"):
    _base = os.path.join(BASE, _d)
    if not os.path.isdir(_base):
        continue
    for _root, _dirs, _files in os.walk(_base):
        _dirs[:] = [x for x in _dirs if x != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            for _i, _ln in enumerate(_t.splitlines(), 1):
                if "pip install" in _ln:
                    _pip_lines.append((os.path.relpath(_p, BASE), _i, _ln))
_pip_pinned = [x for x in _pip_lines if "==" in x[2]]
check("pip install lines in the built tree: 42 total, 20 pinned (==), 22 unpinned by design",
      len(_pip_lines) == 42 and len(_pip_pinned) == 20 and len(_pip_lines) - len(_pip_pinned) == 22)
if len(_pip_lines) != 42 or len(_pip_pinned) != 20:
    print(f"   pip lines: {len(_pip_lines)} total, {len(_pip_pinned)} pinned")
# The 13 upstream pins (P-01-P-13) all present in the built tree.
_upstream = {
    "skills/django-verification/SKILL.md": ("ruff==0.17.5", "black==26.10.1", "pytest==9.2.0"),
    "skills/frontend-slides/html-template.md": ("Pillow==13.0.0",),
    "skills/frontend-slides/scripts/extract-pptx.py": ("python-pptx==1.0.2",),
    "skills/django-celery/SKILL.md": ("celery[redis]==5.7.0", "flower==2.2.0"),
    "skills/generating-python-installer/SKILL.md": ("opencv-python-headless==5.0.0.93",),
    "skills/plankton-code-quality/SKILL.md": ("uv==0.13.8", "ruff==0.17.5"),
    "skills/windows-desktop-e2e/SKILL.md": ("pywinauto==0.6.9", "pytest-repeat==0.9.4",
                                            "pyautogui==0.9.54", "pytest-timeout==2.5.0"),
    "scripts/hooks/gateguard-fact-force.js": ("gateguard-ai==0.6.2",),
    "scripts/hooks/insaits-security-monitor.py": ("insa-its==4.9.10",),
}
_missing_pins = [(f, s) for f, strs in _upstream.items()
                 for s in strs if s not in read(f)]
if _missing_pins:
    print(f"   missing upstream pins: {_missing_pins}")
check("§1 upstream pins P-01-P-13 all present in the built tree (13 lines)",
      not _missing_pins)
# The 7 staged pins (pitch-deck-video) present in the built tree.
check("§1 staged pins: piper-tts==1.8.0 x3 on pitch SKILL.md:843",
      pitch.splitlines()[842].count("piper-tts==1.8.0") == 3)
check("§1 staged pins: shots-reference + troubleshooting + tts.mjs (piper-tts x2, no yt-dlp in tts.mjs)",
      "piper-tts==1.8.0" in shots_ref
      and "piper-tts==1.8.0" in trouble
      and trouble.count("yt-dlp==2026.10.26") == 2
      and tts_mjs.count("piper-tts==1.8.0") == 2)
# The yt-dlp line verify24 E-5 asserted unpinned lives in pitch-deck-video
# troubleshooting.md (:232/:233), not windows-desktop-e2e; it is now pinned.
check("§1 yt-dlp pinned (verify24 E-5 line): unpinned E-5 string gone, pinned form x2",
      "pip install yt-dlp`" not in trouble
      and trouble.count("yt-dlp==2026.10.26") == 2)
# The 22 unpinned lines are exactly the audit's independently classified
# (b)/(c)/(d) set (Audit #73, audit73-pip-unpinned.txt); the only one that
# is a bare install command for a named package is the tts.mjs:180
# runtime error string, deliberately left unpinned.
_expected_unpinned = {
    ("skills/bengali-nlp/SKILL.md", 87), ("skills/bengali-nlp/SKILL.md", 139),
    ("skills/bengali-nlp/SKILL.md", 207), ("skills/django-verification/SKILL.md", 428),
    ("skills/python-patterns/SKILL.md", 546),
    ("skills/generating-python-installer/SKILL.md", 150),
    ("skills/windows-desktop-e2e/SKILL.md", 610),
    ("skills/pitch-deck-video/template/scripts/tts.mjs", 180),
    ("agents/ecc-agent-evaluator.md", 33),
    ("agents/ecc-django-build-resolver.md", 77), ("agents/ecc-django-build-resolver.md", 79),
    ("agents/ecc-django-build-resolver.md", 85), ("agents/ecc-django-build-resolver.md", 94),
    ("agents/ecc-django-build-resolver.md", 182), ("agents/ecc-django-build-resolver.md", 229),
    ("agents/ecc-opensource-packager.md", 137),
    ("scripts/hooks/insaits-security-monitor.py", 205),
    ("scripts/hooks/insaits-security-wrapper.js", 78),
    ("manifests/pi-core.json", 25), ("manifests/pi-core.json", 223),
    ("manifests/pi-core.json", 297), ("manifests/pi-core.json", 407),
}
_unpinned_pairs = {(f, i) for (f, i, ln) in _pip_lines if "==" not in ln}
if _unpinned_pairs != _expected_unpinned:
    print(f"   unpinned lines differ: extra={sorted(_unpinned_pairs - _expected_unpinned)} "
          f"missing={sorted(_expected_unpinned - _unpinned_pairs)}")
check("§1 unpinned lines are exactly the 22 classified (b)/(c)/(d) lines (Audit #73)",
      _unpinned_pairs == _expected_unpinned)
_tts180 = [x[2] for x in _pip_lines
           if x[0] == "skills/pitch-deck-video/template/scripts/tts.mjs"
           and x[1] == 180]
check("§1 tts.mjs:180 is the unpinned runtime error string (class (b), deliberate)",
      len(_tts180) == 1 and "pip install piper-tts" in _tts180[0] and "==" not in _tts180[0])

# 3. §2 F-14.
check("README_UPDATE_F26 x4 in the built tree (pitch step 7, demo.md, orchestrate :101, readme-writer :95)",
      count_substring_in_tree("README_UPDATE_F26") == 4
      and "README_UPDATE_F26" in pitch
      and "README_UPDATE_F26" in demo_md
      and "README_UPDATE_F26" in orch
      and "README_UPDATE_F26" in readme_writer)
check("F-14 step 7: ledger first, no new gate, re-cut no-op, final report not rewritten",
      "demo video: <app-name>-video/out/demo.mp4" in pitch
      and ".hackathon/run-ledger.md" in pitch
      and "no new gate, no approval" in pitch
      and "final report is not rewritten" in pitch)
check("F-14 orchestrate :101 clause + readme-writer :95 + demo.md :9 agree",
      "linked into the README by that run (pitch-deck-video step 7, README_UPDATE_F26)" in orch
      and "readme-writer is not re-run just for the video link" in readme_writer
      and "then link the video into the README per the skill's step 7" in demo_md)
check("F-14 /demo gates intact: never automatic, callable only",
      "DEMOGATE_O4_F22" in orch and "DEMOGATE_O9_F22" in orch
      and "/demo is never part of this sequence" in orch)

# 4. §3 comment fix (+ Audit #73 M1/M2).
check("§3 fix25 comment matches the comment-fix 'After' block (7 lines)",
      "§1 wires, §2 inventory, §4 S1/benchmark" in build
      and "loop-status dangling references removed" in build
      and "S1 header 80 -> 89 styles" in build)
check("§3 fix26 comment (M2): header names ck + §1 pip pins, :24075 names the 13 upstream lines",
      "fix #26: build-time patches (ck cost lines + §1 pip pins)" in build
      and "§1 pip pins (13 upstream lines, P-01–P-13) land in the same script." in build
      and "placeholder section" not in build)
check("§3 verify25.py docstring says +314/-0, no +305 left (M1)",
      "+314/-0" in verify25_text and "+305" not in verify25_text)

# 5. §4 varfont.
check("VARFONT_F26 x1 in the built tree (inventory §11 scoped exceptions)",
      count_substring_in_tree("VARFONT_F26") == 1
      and "## 11. Scoped exceptions" in inv
      and "VARFONT_F26" in inv)
check("varfont scope: template only, Hanken + JetBrains variable, Instrument static",
      "Template only" in inv
      and "HankenGrotesk.woff2" in inv and "JetBrainsMono.woff2" in inv
      and "InstrumentSerif.woff2" in inv
      and "App UI fonts stay static-only" in inv)
_fonts_dir = os.path.join(BASE, "skills/pitch-deck-video/template/public/fonts")
_fonts = sorted(os.listdir(_fonts_dir)) if os.path.isdir(_fonts_dir) else []
_sizes = {f: os.path.getsize(os.path.join(_fonts_dir, f)) for f in _fonts}
check("template fonts: woff2 sizes match the vendored files (34704 / 21032 / 30376)",
      _sizes.get("HankenGrotesk.woff2") == 34704
      and _sizes.get("InstrumentSerif.woff2") == 21032
      and _sizes.get("JetBrainsMono.woff2") == 30376)
check("app-UI static-only stands (orchestrate :139 NEVER + F2 check)",
      "A variable font file is NEVER the shipped delivery format" in orch)

# 6. §5 B6.
check("B6 call-map :38 DOCUMENTATION-ONLY (consumer chain, upstream-only, defined not live)",
      "DOCUMENTATION-ONLY" in callmap
      and "trigger router has no live Cursor entry point (fix #26: DOCUMENTATION-ONLY)" in callmap
      and "a DEFINED routing path, not a LIVE one" in callmap
      and "not a live routing table" in callmap)
check("B6 flow strings: 128 qualified, 0 bare 'on-request (trigger-routed)'",
      callmap.count("on-request (trigger-routed; no live Cursor entry — see method note B6)") == 128
      and callmap.count("on-request (trigger-routed)") == 0)
check("B6 generator :342 emits the qualified string, :383 calls skill-triggers documentation-only (Sweep #34 minors)",
      "on-request (trigger-routed; no live Cursor entry — see method note B6)" in generator
      and "skill-triggers@1.json is a documentation-only reference table, not install data." in generator
      and "is a live routing table" not in generator)
_mapdata = json.load(open(os.path.join(
    PLUGIN, "fix25/callmap/call-map-data.json"), encoding="utf-8"))
check("call-map-data.json: trigger_only [] and counts agree (166/72/123/87/15/64)",
      _mapdata.get("trigger_only") == []
      and _mapdata["counts"] == {"agents": 72, "commands": 87, "hooks": 15,
                                 "rules": 123, "skills": 166, "triggers": 64})
check("no 'is a live routing table' claim in the built tree",
      len(grep_tree("is a live routing table")) == 0)

# 7. §6/§7 owed records.
check("Dim 7 owed in the benchmark file (NONE RECORDED, owed never claimed statically)",
      "NONE RECORDED (no v5 figure)" in bench
      and "browser-qa live verdict (owed, never claimed statically)" in bench
      and "records it as a gap (owed), not as a pass" in bench)
check("Dim 7: no Campus Eats render exists (no index.html)",
      not os.path.isfile(os.path.join(
          HOME, "workspace/cold-start-render/campus-eats/index.html")))
check("Dim 7 note records OWED as a decision, not a pass",
      "Dim 7 stays OWED" in dim7_note and "RECORDED DECISION" in dim7_note)
check("R1/R4 note records OWED as defined, not verified",
      "R1 (iris-opens) and R4 (hero loop) are OWED, not verified" in r1r4_note
      and "R1: OWED as defined" in r1r4_note
      and "R4: OWED as defined" in r1r4_note)

# 8. §8 ck KEEP.
check("ck cost lines corrected to ~1k tokens/session (3 lines)",
      "Injects ~1k tokens per session (not ~2,500 like v1)" in ck_mjs
      and "Load skill (always inject the full SKILL.md, ~170 lines, ~1k tokens/session)" in ck_mjs
      and "The hook injects ~1k tokens per session (the full SKILL.md plus the compact 5-line summary)" in ck_skill)
check("ck session-start.mjs:129 block figure (~100 tokens) kept",
      "Compact summary block (~100 tokens)" in ck_mjs.splitlines()[128])
check("ck no other stale cost claims ('~100 tokens' / '~50 lines' only at :129)",
      len([ln for ln in (ck_mjs + ck_skill).splitlines()
           if "~100 tokens" in ln or "~50 lines" in ln]) == 1)
check("ck wire itself untouched (hooks/session-start.js still spawns session-start.mjs)",
      "skills/ck/hooks/session-start.mjs" in session_start)

# 9. Cross-cutting.
_f26_occ = Counter()
for _d in ("skills", "agents", "commands", "rules", "hooks"):
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [x for x in _dirs if x != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            for _tok in ("README_UPDATE_F26", "VARFONT_F26"):
                _f26_occ[_tok] += _t.count(_tok)
check("_F26 token census in the built tree: README_UPDATE_F26 4, VARFONT_F26 1",
      (_f26_occ["README_UPDATE_F26"], _f26_occ["VARFONT_F26"]) == (4, 1))
_f25_occ = Counter()
for _d in ("skills", "agents", "commands", "rules", "hooks"):
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [x for x in _dirs if x != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            for _tok in ("RECIPES_F25", "TESTCOV_F25", "PLATFORM_F25",
                         "BENCHMARK_V5_F25", "TECHDEPTH_F25", "ADAPT_F25",
                         "REASON_F25", "CREATIVE_F25"):
                _f25_occ[_tok] += _t.count(_tok)
check("_F25 token census unchanged: RECIPES 1, TESTCOV 1, PLATFORM 2, "
      "BENCHMARK 10, TECHDEPTH 8, ADAPT 2, REASON 6, CREATIVE 3",
      (_f25_occ["RECIPES_F25"], _f25_occ["TESTCOV_F25"], _f25_occ["PLATFORM_F25"],
       _f25_occ["BENCHMARK_V5_F25"], _f25_occ["TECHDEPTH_F25"], _f25_occ["ADAPT_F25"],
       _f25_occ["REASON_F25"], _f25_occ["CREATIVE_F25"]) == (1, 1, 2, 10, 8, 2, 6, 3))
check("frozen D19 texts intact (orchestrate + Taste + polish-pass)",
      D19_RULE in orch and D19_RULE in taste
      and D19_ROUTING in orch and D19_REVIEWER in orch and POLISH_F19 in polish)

# 10. Prior-verifier regression leg. EXPECTED fails are ONLY the codified
# tails. Any fail outside that pattern is a REAL regression.
_FPRINT21 = ("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c",
             "build.sh is 23647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c")
_FPRINT22 = "build.sh is 23774 lines, md5 4799a819791b9c3ec4c19136ad698397"
_FPRINT23 = ("build.sh is 24,059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2",
             "build.sh is 24059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2")
_FPRINT24 = ("build.sh is 24,070 lines, md5 b0b2645a7d647f96296f9e9c45e09ef5",
             "build.sh is 24070 lines, md5 b0b2645a7d647f96296f9e9c45e09ef5")
_FPRINT25 = ("build.sh is 24,079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae",
             "build.sh is 24079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae")
_DIFF23 = "diff vs build.sh.before-fix23 is additions only (+285/-0)"
_DIFF24 = "diff vs build.sh.before-fix23 is additions only (+296/-0)"
_PINS23 = "grok-4.7-high in 26 files, cursor-grok-4.6-high-fast in 85"
_LFUI_DIFF = "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks"
_B3 = "B3 conflict flag carried (30ms vs Rule 5 floor)"
_B15 = "B15 conflict flag carried (0.8x vs quick-reference 60-70%)"
_S1_OLD = "S1 styles.csv discrepancy asserted as-is (80 header / 89 rows, csv is source)"
_E5 = "E-5 pitch-deck-video venv Windows form"
# verify23's census checks assert the fix23-original counts; all of them
# fail on the current tree by design (fix #24 moved them, fix #25 moved
# three further). The exact old strings are the allow-list.
_F23_OLD = ("INVENTORY_F23: 4 lines in the built tree",
            "AMBITION_F23: 6 lines / 7 occurrences in the built tree",
            "MEMORABLE_F23: 4 lines / 5 occurrences in the built tree",
            "MOTION_F23: 9 lines / 10 occurrences in the built tree",
            "TYPEAUDIT_F23: 14 lines / 18 occurrences in the built tree",
            "TRIO_F23: 1 line in the built tree (orchestrate design-package step)",
            "HERO-BQA_F23: 3 lines in the built tree",
            "FUNC-BQA_F23: 2 lines in the built tree (browser-qa + Taste)",
            "FUNC-UIPRO_F23: 1 line in the built tree (ui-ux-pro-max pointer)",
            "ALIGN_F23: 15 lines / 16 occurrences in the built tree",
            "COVER_F23: 4 lines in the built tree",
            "BLOCK_F23: 5 lines in the built tree",
            "17 files carry _F23 tokens in the built tree")
_F23_MANIFEST = "fix23/MANIFEST.md exists and records build.sh lines + md5"
_F22_LEG_368 = "fix22 verifier: only expected fails, tail is 366/369 checks pass (expected 368/369 checks pass)"
_F24_CENSUS = ("_F23 census post-fix24: INVENTORY 5/5, AMBITION 7/8, MOTION 9/12, TYPEAUDIT 15/19, TRIO 4/4",
               "_F23 census post-fix24: HERO-BQA 4/4, FUNC-BQA 3/3, FUNC-UIPRO 2/2, ALIGN 15/21, MEMORABLE 5/6, 18 files")
_F24_MANIFEST = "fix24/MANIFEST.md exists and records build.sh lines + md5"
_F25_MANIFEST = "fix25/MANIFEST.md exists and records build.sh lines + md5"


def _allowed_fail(line):
    return (any(p in line for p in _FPRINT21)
            or _FPRINT22 in line
            or any(p in line for p in _FPRINT23)
            or any(p in line for p in _FPRINT24)
            or any(p in line for p in _FPRINT25)
            or _DIFF23 in line
            or _DIFF24 in line
            or _PINS23 in line
            or _LFUI_DIFF in line
            or _B3 in line
            or _B15 in line
            or _S1_OLD in line
            or _E5 in line
            or any(p in line for p in _F23_OLD)
            or _F23_MANIFEST in line
            or _F22_LEG_368 in line
            or any(p in line for p in _F24_CENSUS)
            or _F24_MANIFEST in line
            or _F25_MANIFEST in line
            or "fix23 verifier: only expected fails, tail is" in line
            or "fix24 verifier: only expected fails, tail is" in line
            or "fix25 verifier: only expected fails, tail is" in line
            or re.match(r"FAIL fix\d+ verifier still passes", line))


for name, script, tail in (
        ("fix15", "fix15/verify15.py", "42/44 checks pass"),
        ("fix17", "fix17/verify17.py", "58/60 checks pass"),
        ("fix18", "fix18/verify18.py", "69/72 checks pass"),
        ("fix19", "fix19/verify19.py", "71/76 checks pass"),
        ("fix20", "fix20/verify20.py", "164/169 checks pass"),
        ("fix21", "fix21/verify21.py", "96/102 checks pass"),
        ("fix22", "fix22/verify22.py", "366/369 checks pass"),
        ("fix23", "fix23/verify23.py", "excluding the manifest check, which is owed: 194/211 checks pass"),
        ("fix24", "fix24/verify24.py", "excluding the manifest check, which is owed: 97/104 checks pass"),
        ("fix25", "fix25/verify25.py", "excluding the manifest check, which is owed: 72/74 checks pass")):
    r = subprocess.run(["python3", script], cwd=PLUGIN,
                       capture_output=True, text=True)
    _out_tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    _fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    _bad = [ln for ln in _fails if not _allowed_fail(ln)]
    if _bad:
        print(f"   {name} unexpected FAILs: {_bad}")
    check(f"{name} verifier: only expected fails, tail is {_out_tail} "
          f"(expected {tail})",
          not _bad and _out_tail == tail)

# verify13h: expected exactly 6 fails -- 2 B2 + M3 :61, :62, :70, :71.
_r13 = subprocess.run(["python3", "fix13h/verify13h.py"], cwd=PLUGIN,
                      capture_output=True, text=True)
_r13_fails = [ln.strip() for ln in _r13.stdout.splitlines()
              if ln.startswith("  B2 ") or ln.startswith("  M3 ")]
_expected13 = {
    "B2 orchestrate: whole-tree copy: count=0 want=1 :: 'copy the WHOLE tree into'",
    "B2 standalone: whole-tree copy: count=0 want=1 :: 'copy the WHOLE tree into'",
    "M3 orchestrate: Verify step 4 (UI) header: count=0 want=1 :: 'Verify step 4. **Any diff that touches a UI surface'",
    "M3 orchestrate: Verify step 4 (audit) header: count=0 want=1 :: '**Verify step 4. Adversarial audit'",
    "M3 orchestrate: own step-6 ref untouched: count=0 want=1 :: 'the step-6 README/final report'",
    "M3 orchestrate: own step-5 ref untouched: count=0 want=1 :: 'per orchestrate step 5 above'",
}
if set(_r13_fails) != _expected13:
    print(f"   verify13h unexpected fails: {sorted(set(_r13_fails) ^ _expected13)}")
check("verify13h: exactly 6/97 fail (2 B2 + M3 :61, :62, :70, :71; F-04 checks :57, :63, :66 pass)",
      _r13.stdout.startswith("VERIFY FAILED (6 of 97)")
      and set(_r13_fails) == _expected13)

# 11. Manifest check (fix22 pattern). Runs once fix26/MANIFEST.md exists;
# FAILS until the manifest worker writes it. Reported separately as owed.
manifest_path = os.path.join(PLUGIN, "fix26/MANIFEST.md")
_manifest_ok = False
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    _manifest_ok = bool(m_lines and m_md5
                        and int(m_lines.group(1)) == len(build_lines)
                        and m_md5.group(1) == build_md5)
check("fix26/MANIFEST.md exists and records build.sh lines + md5 "
      "(OWED -- fails until the manifest worker writes it)",
      _manifest_ok)

failed = [n for n, ok in checks if not ok]
_manifest_failed = not _manifest_ok
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
if _manifest_failed:
    print(f"excluding the manifest check, which is owed: "
          f"{len(checks) - len(failed)}/{len(checks) - 1} checks pass")
sys.exit(1 if failed else 0)
