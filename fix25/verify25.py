#!/usr/bin/env python3
"""verify25.py -- checks fix #25 in the BUILT tree (read-only).

Run after a build: python3 fix25/verify25.py
Exits 0 only if every check passes.

Fix #25 is the "called, weaved, works" turn: a call map proving every
skill/agent/rule/command/hook/trigger is invoked or intentionally
dormant, four wire-ins, the §2 inventory-bypass close, the §4(a)
authorized verifier updates (S1 header 80 -> 89, verify13h M3 for the
F-04 rename), the §4(b) template-fonts self-host, the §4(d) beat-
Campus-Eats-v5 design bar, the §4(e) technical-depth rules, the §4(f)
adaptive/creative rules, plus the post-loop fixes (Sweep #33 minors:
step-2 reviewer backing check at orchestrate :266, trap-row qualifier
at hackathon-scope :90; Audit #72 M2: launch-marketing.md :15 reword;
dry-run #40 Leg 5 MINOR: /loop-status references removed, option (b)).

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc
(+ build.sh where the SPEC says so):

  1. Global: build.sh fingerprint (24,079 lines, md5 f19483f5...);
     diff vs build.sh.before-fix23 additions only (+314/-0); counts
     166/72/123/87/15, trigger keys 64; banned terms 0; Grok pins only
     (grok-4.7-high x54, cursor-grok-4.6-high-fast x103, bare x0).
  2. §1 call map: present in the built tree, counts table agrees with
     the tree, uncalled 52 (24 skills / 21 agents / 7 commands),
     second-order orphans 13 (8 skills / 4 agents / 1 command),
     call-map-data.json agrees, every dormant name carries a reason in
     fix25/callmap/wiring-list.md, all four wire-ins landed.
  3. §2 weave: INVENTORY_F23 x1 in all six orch-* files; no off-skill
     improvisation path; frozen texts byte-identical (D19_RULE,
     D19_ROUTING, POLISH_F19, D19_REVIEWER).
  4. §4(a) S1: header "89 searchable styles (51 active)" at
     ui-ux-pro-max :3 and :8; inventory line agrees; csv is the source.
  5. §4(b) template fonts: 3 woff2 in the built template public/fonts/;
     fonts.ts uses @remotion/fonts + staticFile; package.json has
     @remotion/fonts and NO @remotion/google-fonts dependency; the
     single remaining "@remotion/google-fonts" string in the built tree
     is the fonts.ts:2 provenance comment; launch-marketing.md:15
     prescribes the self-hosted fonts.
  6. §4(d) design bar: design-benchmark-v5.md present (178 lines), v5
     figures as recorded (61 literal / 60 stricter, kind split),
     thresholds in orchestrate 5a + polish-pass + browser-qa + Taste.
  7. §4(e) technical depth: TECHDEPTH_F25 in hackathon-scope /
     feature-expansion / orchestrate; no-silent-rescope with cut lines;
     the trap-row qualifier at hackathon-scope :90.
  8. §4(f) adaptive + creative: ADAPT_F25 / REASON_F25 /
     substance-creativity in grill-me / orchestrate / feature-expansion;
     the step-2 reviewer sentence at orchestrate :266.
  9. Loop-status fix (option (b)): 0 "loop-status" hits in the built
     tree; command count still 87 (no new command file shipped).
 10. Cross-cutting: banned terms 0; Grok pins only; counts unchanged;
     /demo gates intact (never automatic, callable only); no new skill;
     frozen texts intact; _F25 token census; _F23 census as re-measured
     on the run-5 tree (INVENTORY 11/11, FUNC-BQA 4/4, ALIGN 18/24,
     COVER 7/7, BLOCK 6/6, 24 files -- moved from the fix24 codified
     counts by authorized fix #25 edits; see the manifest §4).
 11. Prior-verifier regression leg: fix15/17/18/19/20/21/22/23/24/13h
     re-run. EXPECTED fails are ONLY the codified tails below. Any fail
     outside that pattern is a REAL regression. Exact tails are
     asserted so a new fail changes the count:
       fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76,
       fix20 164/169, fix21 96/102, fix22 366/369,
       fix23 194/211 excl. manifest (moved from 196/211: the COVER_F23
         7-vs-4 and BLOCK_F23 6-vs-5 census checks, traced to the
         TESTCOV_F25 paragraph + design-benchmark-v5.md),
       fix24 98/104 excl. manifest (moved from 101/104: its two _F23
         census checks -- INVENTORY 11/11, FUNC-BQA 4/4, ALIGN 18/24,
         24 files -- plus the fix23-leg cascade),
       verify13h 6/97 fail (2 B2 + M3 :61, :62, :70, :71 -- the three
         F-04 checks :57, :63, :66 pass after worker C's update).
 12. Manifest check (fix22 pattern): runs once fix25/MANIFEST.md exists.
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
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()

# 1. Global fingerprint / counts / pins / banned terms.
check("build.sh is 24,079 lines, md5 f19483f50e89998f8b9dc052ed5d5fae (post-fix25)",
      len(build_lines) == 24079
      and build_md5 == "f19483f50e89998f8b9dc052ed5d5fae")
_diff = subprocess.run(
    ["diff", "build.sh.before-fix23", "build.sh"],
    cwd=PLUGIN, capture_output=True, text=True).stdout
_diff_add = sum(1 for ln in _diff.splitlines() if ln.startswith(">"))
_diff_del = sum(1 for ln in _diff.splitlines() if ln.startswith("<"))
check("diff vs build.sh.before-fix23 is additions only (+314/-0)",
      _diff_add == 314 and _diff_del == 0)
if _diff_del:
    print(f"   deletions in diff: {_diff_del}")
check("fix25 run log: 17 changes, fix25 OK (run 5)",
      "fix25: 17 change(s)" in open(
          os.path.join(PLUGIN, "fix25/build-log-run5.txt"), encoding="utf-8").read()
      and "fix25: OK" in open(
          os.path.join(PLUGIN, "fix25/build-log-run5.txt"), encoding="utf-8").read())


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

# 2. §1 call map.
check("call map present in the built tree (skills/orchestrate/references/call-map.md)",
      os.path.isfile(os.path.join(
          BASE, "skills/orchestrate/references/call-map.md")))
check("call-map counts table agrees with the tree (166/72/123/87/15/64)",
      "| skills | 166 | 166 |" in callmap
      and "| agents | 72 | 72 |" in callmap
      and "| rules | 123 | 123 |" in callmap
      and "| commands | 87 | 87 |" in callmap
      and "| hooks | 15 | 15 |" in callmap
      and "| triggers | 64 | 64 |" in callmap)
check("call map: uncalled 52 elements (24 skills / 21 agents / 7 commands)",
      "## Uncalled summary — 52 elements with no dispatch path" in callmap
      and "skills: 24 uncalled" in callmap
      and "agents: 21 uncalled" in callmap
      and "commands: 7 uncalled" in callmap)
check("call map: second-order orphans 13 (8 skills / 4 agents / 1 command)",
      "## Second-order orphans — 13 called elements" in callmap)
_mapdata = json.load(open(os.path.join(
    PLUGIN, "fix25/callmap/call-map-data.json"), encoding="utf-8"))
check("call-map-data.json counts agree (166/72/123/87/15/64)",
      _mapdata["counts"] == {"agents": 72, "commands": 87, "hooks": 15,
                             "rules": 123, "skills": 166, "triggers": 64})
check("call-map-data.json: uncalled 24/21/7, orphans 8/4/1",
      (len(_mapdata["uncalled"]["skills"]), len(_mapdata["uncalled"]["agents"]),
       len(_mapdata["uncalled"]["commands"])) == (24, 21, 7)
      and (len(_mapdata["second_order_orphans"]["skills"]),
           len(_mapdata["second_order_orphans"]["agents"]),
           len(_mapdata["second_order_orphans"]["commands"])) == (8, 4, 1))
_wiring = open(os.path.join(PLUGIN, "fix25/callmap/wiring-list.md"),
               encoding="utf-8").read()
_dormant = []
for _cat in ("skills", "agents", "commands"):
    _dormant += _mapdata["uncalled"][_cat]
    _dormant += _mapdata["second_order_orphans"][_cat]
_missing = [n for n in _dormant if n not in _wiring]
if _missing:
    print(f"   dormant names missing from wiring-list.md: {_missing}")
check("every dormant name (52 uncalled + 13 orphans) carries a reason in wiring-list.md",
      len(_dormant) == 65 and not _missing)
check("wire W1: ck called via hooks/session-start.js (spawns session-start.mjs)",
      "skills/ck/hooks/session-start.mjs" in session_start
      and "spawnSync(process.execPath, [ckHook]" in session_start
      and "`ck` | hooks/session-start.js [strong]" in callmap)
check("wire W1: ck SKILL.md carries the already-wired note",
      "already wired" in ck_skill
      and "hooks/session-start.js` runs `skills/ck/hooks/session-start.mjs`" in ck_skill)
check("wire W2: conventional-commit-review via /prp-commit Phase 3 + orchestrate step 6",
      "Draft the message with the `conventional-commit-review` skill" in prp_commit
      and "draft each commit message with the `conventional-commit-review` skill" in orch
      and "ecc-commit-reviewer` agent" in prp_commit
      and "ecc-commit-reviewer` agent" in orch)
check("wire W3: ecc-recipes lookup in orchestrate (RECIPES_F25)",
      "RECIPES_F25" in orch
      and "consult the `ecc-recipes` skill" in orch)
check("wire W4: /test-coverage in orchestrate Verify step 1 (TESTCOV_F25, Steps 1-2)",
      "TESTCOV_F25" in orch
      and "run the `/test-coverage` command's measurement (its Steps 1–2" in orch)

# 3. §2 weave.
_orch_stars = {}
for _fn in ("orch-add-feature", "orch-change-feature", "orch-fix-defect",
            "orch-refine-code", "orch-build-mvp", "orch-pipeline"):
    _orch_stars[_fn] = read(f"skills/{_fn}/SKILL.md").count("INVENTORY_F23")
check("§2 inventory close: INVENTORY_F23 x1 in all six orch-* files",
      all(v == 1 for v in _orch_stars.values()))
if any(v != 1 for v in _orch_stars.values()):
    print(f"   INVENTORY_F23 per orch-* file: {_orch_stars}")
check("§2 no off-skill improvisation path (no judgment phrases in orchestrate/Taste/polish-pass)",
      all(p not in orch + taste + polish for p in (
          "use your judgment", "best judgment", "decide for yourself",
          "whatever you think", "your own discretion")))
check("§2 recorded-gap fallback present (binding routes through a named skill)",
      "no off-skill improvisation" in orch
      and "recorded-gap fallback" in orch)
check("frozen D19_RULE byte-identical in orchestrate + Taste",
      D19_RULE in orch and D19_RULE in taste)
check("frozen D19_ROUTING byte-identical in orchestrate (routing :163)",
      D19_ROUTING in orch)
check("frozen D19_REVIEWER byte-identical in orchestrate",
      D19_REVIEWER in orch)
check("frozen POLISH_F19 byte-identical in polish-pass",
      POLISH_F19 in polish)
check("D19 lead sentence still exactly 1x in orchestrate",
      orch.count("Every UI decision carries a thought-out reason across the FULL experience") == 1)

# 4. §4(a) S1.
check("S1: ui-ux-pro-max header '89 searchable styles (51 active)' at :3 and :8",
      "89 searchable styles (51 active)" in uipro.splitlines()[2]
      and "89 searchable styles (51 active)" in uipro.splitlines()[7])
check("S1: '80 searchable' occurrences 0 in ui-ux-pro-max",
      uipro.count("80 searchable") == 0)
check("S1: inventory line agrees (89 rows, header 89, csv is source)",
      csv_rows("skills/ui-ux-pro-max/data/styles.csv") == 89
      and "89 rows in `data/styles.csv`" in inv
      and "89 searchable styles, 51 active" in inv
      and "the csv is the inventory source" in inv)

# 5. §4(b) template fonts.
_fonts_dir = os.path.join(BASE, "skills/pitch-deck-video/template/public/fonts")
_fonts = sorted(os.listdir(_fonts_dir)) if os.path.isdir(_fonts_dir) else []
_sizes = {f: os.path.getsize(os.path.join(_fonts_dir, f)) for f in _fonts}
check("template fonts: exactly 3 woff2 files in the built template public/fonts/",
      _fonts == ["HankenGrotesk.woff2", "InstrumentSerif.woff2", "JetBrainsMono.woff2"])
if _fonts != ["HankenGrotesk.woff2", "InstrumentSerif.woff2", "JetBrainsMono.woff2"]:
    print(f"   fonts dir: {_fonts}")
check("template fonts: woff2 sizes match the vendored files (34704 / 21032 / 30376)",
      _sizes.get("HankenGrotesk.woff2") == 34704
      and _sizes.get("InstrumentSerif.woff2") == 21032
      and _sizes.get("JetBrainsMono.woff2") == 30376)
check("fonts.ts uses @remotion/fonts loadFont + staticFile (3 vendored URLs)",
      "from '@remotion/fonts'" in fonts_ts
      and "from 'remotion'" in fonts_ts
      and fonts_ts.count("staticFile('fonts/") == 3
      and "@remotion/google-fonts" not in fonts_ts.replace(
          "// families live from Google Fonts via `@remotion/google-fonts`, which fetched", ""))
check("package.json has @remotion/fonts and NO @remotion/google-fonts dependency",
      '"@remotion/fonts": "4.0.526"' in fonts_pkg
      and "@remotion/google-fonts" not in fonts_pkg)
_gf_hits = grep_tree("@remotion/google-fonts")
check("exactly 1 '@remotion/google-fonts' string in the built tree: fonts.ts:2 provenance comment",
      len(_gf_hits) == 1
      and _gf_hits[0][0] == "skills/pitch-deck-video/template/src/fonts.ts"
      and _gf_hits[0][1] == 2)
if len(_gf_hits) != 1:
    print(f"   @remotion/google-fonts hits: {_gf_hits}")
check("launch-marketing.md:15 prescribes the self-hosted template fonts",
      "self-hosted as vendored woff2 via `@remotion/fonts` + `staticFile`" in launch_mkt.splitlines()[14])

# 6. §4(d) design bar.
check("design-benchmark-v5.md present in the built tree (178 lines)",
      len(bench.splitlines()) == 178)
check("benchmark v5 figures: 61 literal / 60 stricter, kind split (counts table)",
      "| **Total** | **54** | **+7** | **61** | **60** |" in bench
      and "| Component | 28 | +3 (coin stack, bus-pass ticket, sticker sheet) | **31** | 31 |" in bench
      and "| Treatment | 6 | +2 (washi, marker checks ×3 as ONE feature) | **8** | 8 |" in bench
      and "| Visual | 1 | 0 | **1** | 1 |" in bench
      and "| Motion | 15 | +2 (sticker-peel, confetti) | **17** | 16 |" in bench
      and "| Moment | 1 | 0 | **1** | 1 |" in bench
      and "| Type | 2 | 0 | **2** | 2 |" in bench
      and "| Effect | 0 | 0 | **0** | 0 |" in bench
      and "| Diagram | 1 | 0 | **1** | 1 |" in bench)
check("benchmark: iris-opens dealt but unapplied (SPEC §4(d) discrepancy resolved)",
      "iris-opens" in bench and "no recorded application" in bench)
check("benchmark thresholds in orchestrate bar paragraph + step 5a",
      "BENCHMARK_V5_F25" in orch
      and "≥ 62 literal / ≥ 61 stricter" in orch
      and "Motion ≥ 18 / ≥ 17 stricter" in orch
      and "≥ 9 interactive items with ≥ 2 cross-surface drives" in orch
      and "≥ 3 live-data surfaces" in orch)
check("benchmark thresholds in polish-pass (non-negotiable 5 + variety pointer)",
      bench.count("BENCHMARK_V5_F25") >= 0  # benchmark file itself
      and "BENCHMARK_V5_F25" in polish
      and "count ≥ 62 literal / ≥ 61 stricter" in polish)
check("benchmark live verdict in browser-qa (:83 + :115 output-format line)",
      "Beat-v5 benchmark verdict" in bqa
      and "BENCHMARK_V5_F25" in bqa
      and "Beat-v5 benchmark (BENCHMARK_V5_F25)" in bqa)
check("benchmark pointer at the Taste deal point",
      "BENCHMARK_V5_F25" in taste
      and "beat v5 on all seven dimensions" in taste)

# 7. §4(e) technical depth.
check("TECHDEPTH_F25 in hackathon-scope (3) / orchestrate (3) / feature-expansion (2)",
      scope.count("TECHDEPTH_F25") == 3
      and orch.count("TECHDEPTH_F25") == 3
      and fe.count("TECHDEPTH_F25") == 2)
check("TECHDEPTH: Technical-substance section in hackathon-scope (architecture/algorithm/budget/3+ edge cases)",
      "Technical substance — hard ideas get hard builds" in scope
      and "at least 3 named per CORE flow" in scope
      and "Performance budget" in scope)
check("TECHDEPTH: no-silent-rescope with cut lines (scope + orchestrate + expansion)",
      "cut substance: <what> — <why>" in scope
      and "cut-substance lines (what was cut, why)" in orch
      and "the decision record carries the same cut line" in orch
      and "reports the cut with its reason" in fe)
check("TECHDEPTH: trap-row qualifier at hackathon-scope :90",
      "Demo doesn't enter X — that is a cut, not a handling" in scope.splitlines()[89]
      and "(TECHDEPTH_F25)" in scope.splitlines()[89])

# 8. §4(f) adaptive + creative.
check("ADAPT_F25 in grill-me step 2 + orchestrate (specified-ness postures)",
      "ADAPT_F25" in grill and "ADAPT_F25" in orch
      and "EXECUTION posture" in grill and "REASONING posture" in grill)
check("REASON_F25: three-part block in grill-me step 5 + orchestrate :149 + 5a + :266",
      grill.count("REASON_F25") == 1
      and orch.count("REASON_F25") == 5
      and "INFERRED" in orch and "CHOSEN" in orch and "REJECTED" in orch)
check("step-2 reviewer sentence at orchestrate :266 (REASON_F25 backing check)",
      "The reviewer also checks the three-part reasoning block" in orch.splitlines()[265]
      and "REASON_F25" in orch.splitlines()[265]
      and "an entry missing any of the three lines is a finding, minor at least" in orch.splitlines()[265])
check(":149 claim now has both named checkers real (step-2 reviewer :266 + 5a :96)",
      "checked by the step-2 reviewer and the step-5a static check (REASON_F25)" in orch)
check("CREATIVE_F25 substance-creativity in feature-expansion (Lens B / UI-only slate / balance)",
      fe.count("CREATIVE_F25") == 3
      and "Substance first" in fe
      and "No UI-only slate" in fe
      and "at least one substance item" in fe)

# 9. Loop-status fix (option (b)).
_loop_hits = grep_tree("loop-status")
check("loop-status: 0 hits in the built tree (references removed, option (b))",
      len(_loop_hits) == 0)
if _loop_hits:
    print(f"   loop-status hits: {_loop_hits}")
check("loop-status: command count still 87 (no new command file shipped)",
      count_dir("commands") == 87)
check("loop-status: epic-unblock.md ends at step 4, no alias section",
      "Compatibility aliases" not in read("commands/epic-unblock.md")
      and "loop-status" not in read("commands/epic-unblock.md"))
check("loop-status: ecc-recipes loop-* row no longer names a monitor command",
      "watch with `loop-status`" not in read("skills/ecc-recipes/SKILL.md")
      and "monitor `loop-status`" not in read("skills/ecc-recipes/SKILL.md"))

# 10. Cross-cutting.
check("FILM_F1/F5/F6 x1 each in pitch-deck-video (unchanged from fix #24)",
      pitch.count("FILM_F1") == 1 and pitch.count("FILM_F5") == 1
      and pitch.count("FILM_F6") == 1)
check("/demo gates intact: never automatic, callable only, not part of the first-build order",
      "DEMOGATE_O4_F22" in orch and "DEMOGATE_O9_F22" in orch
      and "/demo is never part of this sequence" in orch
      and "ONLY when the user asked for a demo video" in orch)
check("deferred six still end-of-project only",
      "End-of-project checks" in orch
      and all(s in orch for s in ("production-audit", "delivery-gate",
                                  "codehealth-mcp", "verification-loop",
                                  "santa-method", "security-scan")))
check("THE CORE + 'more, not bolder' stand in orchestrate",
      "Memorable is the bar" in orch and "more, not bolder" in orch)
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
check("_F25 token census in the built tree: RECIPES 1, TESTCOV 1, PLATFORM 2, "
      "BENCHMARK 10, TECHDEPTH 8, ADAPT 2, REASON 6, CREATIVE 3",
      (_f25_occ["RECIPES_F25"], _f25_occ["TESTCOV_F25"], _f25_occ["PLATFORM_F25"],
       _f25_occ["BENCHMARK_V5_F25"], _f25_occ["TECHDEPTH_F25"], _f25_occ["ADAPT_F25"],
       _f25_occ["REASON_F25"], _f25_occ["CREATIVE_F25"]) == (1, 1, 2, 10, 8, 2, 6, 3))
if tuple(_f25_occ[t] for t in ("RECIPES_F25", "TESTCOV_F25", "PLATFORM_F25",
                               "BENCHMARK_V5_F25", "TECHDEPTH_F25", "ADAPT_F25",
                               "REASON_F25", "CREATIVE_F25")) != (1, 1, 2, 10, 8, 2, 6, 3):
    print(f"   _F25 census: {dict(_f25_occ)}")
# _F23 census as re-measured on the run-5 tree (moved from the fix24
# codified counts by authorized fix #25 edits; see manifest §4).
_f23_lines = Counter()
_f23_occ = Counter()
_f23_files = set()
for _d in ("skills", "agents", "commands", "rules", "hooks"):
    for _root, _dirs, _files in os.walk(os.path.join(BASE, _d)):
        _dirs[:] = [x for x in _dirs if x != "node_modules"]
        for _fn in _files:
            _p = os.path.join(_root, _fn)
            try:
                _t = open(_p, encoding="utf-8", errors="strict").read()
            except (UnicodeDecodeError, ValueError):
                continue
            if "_F23" in _t:
                _f23_files.add(os.path.relpath(_p, BASE))
            for _tok in ("INVENTORY_F23", "AMBITION_F23", "MOTION_F23",
                         "TYPEAUDIT_F23", "TRIO_F23", "HERO-BQA_F23",
                         "FUNC-BQA_F23", "FUNC-UIPRO_F23", "ALIGN_F23",
                         "MEMORABLE_F23", "COVER_F23", "BLOCK_F23"):
                if _tok in _t:
                    _f23_occ[_tok] += _t.count(_tok)
                    _f23_lines[_tok] += sum(1 for _ln in _t.splitlines() if _tok in _ln)
check("_F23 census post-fix25: INVENTORY 11/11, AMBITION 7/8, MOTION 9/12, "
      "TYPEAUDIT 15/19, TRIO 4/4",
      (_f23_lines["INVENTORY_F23"], _f23_occ["INVENTORY_F23"]) == (11, 11)
      and (_f23_lines["AMBITION_F23"], _f23_occ["AMBITION_F23"]) == (7, 8)
      and (_f23_lines["MOTION_F23"], _f23_occ["MOTION_F23"]) == (9, 12)
      and (_f23_lines["TYPEAUDIT_F23"], _f23_occ["TYPEAUDIT_F23"]) == (15, 19)
      and (_f23_lines["TRIO_F23"], _f23_occ["TRIO_F23"]) == (4, 4))
check("_F23 census post-fix25: HERO-BQA 4/4, FUNC-BQA 4/4, FUNC-UIPRO 2/2, "
      "ALIGN 18/24, MEMORABLE 5/6, COVER 7/7, BLOCK 6/6, 24 files",
      (_f23_lines["HERO-BQA_F23"], _f23_occ["HERO-BQA_F23"]) == (4, 4)
      and (_f23_lines["FUNC-BQA_F23"], _f23_occ["FUNC-BQA_F23"]) == (4, 4)
      and (_f23_lines["FUNC-UIPRO_F23"], _f23_occ["FUNC-UIPRO_F23"]) == (2, 2)
      and (_f23_lines["ALIGN_F23"], _f23_occ["ALIGN_F23"]) == (18, 24)
      and (_f23_lines["MEMORABLE_F23"], _f23_occ["MEMORABLE_F23"]) == (5, 6)
      and (_f23_lines["COVER_F23"], _f23_occ["COVER_F23"]) == (7, 7)
      and (_f23_lines["BLOCK_F23"], _f23_occ["BLOCK_F23"]) == (6, 6)
      and len(_f23_files) == 24)
if len(_f23_files) != 24:
    print(f"   _F23 files: {len(_f23_files)}")

# 11. Prior-verifier regression leg. EXPECTED fails are ONLY the codified
# tails. Any fail outside that pattern is a REAL regression.
_FPRINT21 = ("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c",
             "build.sh is 23647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c")
_FPRINT22 = "build.sh is 23774 lines, md5 4799a819791b9c3ec4c19136ad698397"
_FPRINT23 = ("build.sh is 24,059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2",
             "build.sh is 24059 lines, md5 df2cb85055efc87637d3cb0b1e7061a2")
_FPRINT24 = ("build.sh is 24,070 lines, md5 b0b2645a7d647f96296f9e9c45e09ef5",
             "build.sh is 24070 lines, md5 b0b2645a7d647f96296f9e9c45e09ef5")
_DIFF23 = "diff vs build.sh.before-fix23 is additions only (+285/-0)"
_DIFF24 = "diff vs build.sh.before-fix23 is additions only (+296/-0)"
_PINS23 = "grok-4.7-high in 26 files, cursor-grok-4.6-high-fast in 85"
_LFUI_DIFF = "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks"
_B3 = "B3 conflict flag carried (30ms vs Rule 5 floor)"
_B15 = "B15 conflict flag carried (0.8x vs quick-reference 60-70%)"
_S1_OLD = "S1 styles.csv discrepancy asserted as-is (80 header / 89 rows, csv is source)"
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


def _allowed_fail(line):
    return (any(p in line for p in _FPRINT21)
            or _FPRINT22 in line
            or any(p in line for p in _FPRINT23)
            or any(p in line for p in _FPRINT24)
            or _DIFF23 in line
            or _DIFF24 in line
            or _PINS23 in line
            or _LFUI_DIFF in line
            or _B3 in line
            or _B15 in line
            or _S1_OLD in line
            or any(p in line for p in _F23_OLD)
            or _F23_MANIFEST in line
            or _F22_LEG_368 in line
            or any(p in line for p in _F24_CENSUS)
            or _F24_MANIFEST in line
            or "fix23 verifier: only expected fails, tail is" in line
            or "fix24 verifier: only expected fails, tail is" in line
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
        ("fix24", "fix24/verify24.py", "excluding the manifest check, which is owed: 98/104 checks pass")):
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

# 12. Manifest check (fix22 pattern). Runs once fix25/MANIFEST.md exists;
# FAILS until the manifest worker writes it. Reported separately as owed.
manifest_path = os.path.join(PLUGIN, "fix25/MANIFEST.md")
_manifest_ok = False
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    _manifest_ok = bool(m_lines and m_md5
                        and int(m_lines.group(1)) == len(build_lines)
                        and m_md5.group(1) == build_md5)
check("fix25/MANIFEST.md exists and records build.sh lines + md5 "
      "(OWED -- fails until the manifest worker writes it)",
      _manifest_ok)

failed = [n for n, ok in checks if not ok]
_manifest_failed = not _manifest_ok
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
if _manifest_failed:
    print(f"excluding the manifest check, which is owed: "
          f"{len(checks) - len(failed)}/{len(checks) - 1} checks pass")
sys.exit(1 if failed else 0)
