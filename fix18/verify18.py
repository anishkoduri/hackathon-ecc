#!/usr/bin/env python3
"""verify18.py -- checks fix #18 in the BUILT tree (read-only).

Run after a build: python3 fix18/verify18.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. SKILL.md: F6 caps + allocation table, Edge beat, How growth,
     step-3 features/cuts + best states, step-4 theme.source + stack,
     step-6 coverage / A-V table / gorgeousness / runtime / mix;
     old 1:30-1:50 regime gone.
  2. shots-reference.md: features/cuts rows + section, arch node stack,
     theme.source + vignette, under-gain guidance, gapMs note.
  3. Seed JSONs (shots.example.json + shots.json): features/cuts,
     Edge shot, stack labels, arch line naming the stack.
  4. Arch.tsx: stack type + render.
  5. qa.mjs: coverage table, theme-vs-seed, A/V skeleton, under warning,
     runtime print + BLOCKING over 2:10, exit code.
  6. demo.md: under 2:10, no 1:30-1:50.
  7. Counts unchanged post-fix17: 166/72/123/87/15.
  8. No banned terms (fix #16 scrub) in the built skill tree.
  9. build.sh post-fix18 fix-up (23,276 lines, md5 5cdd2278... -- fix18
     edits staged sources only, PLUS the fix-up's build.sh patches:
     README heredoc + hackathon-pitch cross-reference patches). Updated
     by fix #19 to the post-fix19 values (23,314 lines, a8d3d3c6...) and
     by fix #20 to the post-fix20 values (23,349 lines, e5ff7d6c...) and
     by fix #20's weaving pass to the post-weave20 values (23,582 lines,
     766a35e4...) — baseline updates, same precedent, not anchor changes.
     Updated by fix #20's fix-up pass (audit #62 + sweep #25) to the
     post-fixup20 values (23,582 lines, 766a35e4...) — same precedent.
     Updated by fix #20's second fix-up pass (sweep #26) to the
     post-fixup20b values (23,582 lines, 766a35e4...) — same precedent.
     Updated by fix #20's third fix-up pass (sweep #27 + steers #3/#4/#5/#6)
     to the post-fixup20c values (23,609 lines, 3c7b45bb...) — same precedent.
     Updated by fix #20's fourth fix-up pass (sweep #28 MINOR-1) to the
     post-fixup20d values (23,609 lines, 785fb405...) — same precedent.
     Updated by fix #21 to the
     post-fix21 values (23,647 lines, 8dfacb47...) — same precedent.
 10. fix15/verify15.py 43/43 + fix17/verify17.py 59/59 still pass.
"""
import hashlib
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


skill = read("skills/pitch-deck-video/SKILL.md")
ref = read("skills/pitch-deck-video/references/shots-reference.md")
arch = read("skills/pitch-deck-video/template/src/scenes/Arch.tsx")
qa = read("skills/pitch-deck-video/template/scripts/qa.mjs")
demo = read("commands/demo.md")

# 1. SKILL.md — F6 caps + allocation.
check("F6 caps: under 2:10 (130s) hard rule", "under 2:10 (130 seconds) — hard rule" in skill)
check("F6 caps: absolute max 2:30 never exceeded", "Absolute max 2:30 (150 seconds), never exceeded" in skill)
check("F6 caps: measured durations, never estimates", "computed from the MEASURED narration durations" in skill)
check("F6 allocation: budget-before-lines rule", "Write the time budget before writing the lines." in skill)
check("F6 allocation: How/features 55-65 largest share", "How / features | 6–9 | 55–65" in skill and "The LARGEST share" in skill)
check("F6 allocation: Edge 8-10, Proof 12-15, Close 6-8", "Edge (uniqueness) | 1 | 8–10" in skill and "Proof (arch + stack) | 1–2 | 12–15" in skill and "Close | 1 | 6–8" in skill)
check("F6 allocation: Problem 8-10, Wow 14-18", "Problem | 1 | 8–10" in skill and "Wow | 1–2 | 14–18" in skill)

# 2. SKILL.md — arc (F3 Edge, F1 How growth).
check("F3 Edge beat present as beat 3", "3. **Edge** — one beat, one sentence" in skill)
check("F3 Edge: alternative named or implied", 'with the alternative named or clearly implied ("unlike X, this…")' in skill)
check("F3 Edge: never invent a competitor claim", "never invent a competitor claim" in skill)
check("F1 How grows: one beat per remaining must-have feature", "PLUS one beat per remaining must-have feature" in skill)
check("F1 shown rule: visible AND named", "A feature counts as shown only if it is visible on camera AND named in its beat" in skill)
check("Arc is now 6 beats (Proof 5, Close 6)", "5. **Proof**" in skill and "6. **Close**" in skill)

# 3. SKILL.md — step 3 (F1 + F4 best states).
check("F1 step 3: features array from scope must-haves", "Write the list into `shots.json` as a `features` array" in skill)
check("F1 step 3: cuts array with reason", "cut the least important features into the `cuts` array with a reason" in skill)
check("F4 step 3: best-looking state per beat", "best-looking state that shows the claim" in skill)
check("F4 step 3: never an empty state on camera", "Never put an empty state on camera to stand for a full one" in skill)

# 4. SKILL.md — step 4 (F2 stack + F4 source).
check("F4 step 4: theme.source recorded", "record the token source (file + values) in `shots.json` as `theme.source`" in skill)
check("F2 step 4: stack label per arch node", "give each node its `stack` label" in skill)
check("F2 step 4: stack from package.json + decision record, never invented", "taken from the app's `package.json` + `docs/decision-record.md` / `docs/scope.md`, never invented" in skill)
check("F2 step 4: spoken stack line, one phrase", 'name the stack in one spoken phrase ("Built on Next.js, GPT-5, and Supabase")' in skill)

# 5. SKILL.md — step 6 (F1/F4/F5/F6 QA).
check("F1 step 6: coverage table complete", "Coverage table complete" in skill)
check("F5 step 6: per-beat A/V table, no is BLOCKING", "Per-beat A/V table" in skill and 'A \'no\' is a BLOCKING finding' in skill)
check("F4 step 6: gorgeousness checks (a)(b)(c)", "no generic seed look" in skill and "best-looking states" in skill and "`theme.vignette` 0 for light apps" in skill)
check("F6 step 6: runtime over 2:10 BLOCKING", "over 2:10 is BLOCKING (re-cut)" in skill)
check("F5 step 6: 10-second mix listen", "listen to a 10-second sample from the middle of the video" in skill)
check("F5 step 6: under-gain 0.20 warning", "warns if `music.gain.under` exceeds 0.20" in skill)
check("F4 step 6: theme check fails QA if seeded", "the theme check fails the QA if `shots.json` still carries the seed theme" in skill)

# 6. SKILL.md — old regime gone.
check("Old regime gone: no 1:30-1:50, no 2:00 cap, no 90-110s", "1:30–1:50" not in skill and "2:00 cap" not in skill and "90–110 seconds" not in skill)
check("Pacing updated: 12-16 beats under 2:10", "12–16 beats under 2:10, a beat averages 7–9 seconds" in skill)

# 7. shots-reference.md.
check("F1 ref: features row", "`features` | One entry per must-have feature" in ref)
check("F1 ref: cuts row", "`cuts` | Must-have features deliberately left out" in ref)
check("F1 ref: features/cuts section", "## features / cuts" in ref)
check("F2 ref: arch nodes section + optional stack", "## cards — arch nodes" in ref and "optional `stack` label" in ref)
check("F4 ref: theme.source + vignette documented", "record the source (file + values) in `theme.source`" in ref and "`theme.vignette` (0–1, default 0.3)" in ref)
check("F5 ref: under-gain guidance", "under` above 0.20 risks burying the voice" in ref)
check("F6 ref: gapMs counts toward the 2:10 total", "counts toward the 2:10 total" in ref)

# 8. Seed JSONs (built).
for rel in ("skills/pitch-deck-video/template/shots.example.json",
            "skills/pitch-deck-video/template/shots.json"):
    data = json.loads(read(rel))
    short = rel.split("/")[-1]
    check(f"Seed {short}: features + cuts arrays", bool(data.get("features")) and bool(data.get("cuts")))
    check(f"Seed {short}: shot order hook/setup/result/edge/arch/close",
          [s["id"] for s in data["shots"]] == ["hook", "setup", "result", "edge", "arch", "close"])
    check(f"Seed {short}: stack labels on Ranker/Scheduler/Writer",
          [n.get("stack") for n in data["cards"]["arch"]["nodes"]] == [None, "GPT-5", "Next.js 15", "GPT-5", None])
    check(f"Seed {short}: arch line names the stack",
          "Next.js and GPT-5" in data["shots"][4]["say"])
    check(f"Seed {short}: edge shot is an app shot with a focus",
          data["shots"][3]["kind"] == "app" and "focus" in data["shots"][3]["do"][0])

# 9. Arch.tsx.
check("F2 Arch.tsx: Node type gains optional stack", "stack?: string" in arch)
check("F2 Arch.tsx: stack rendered under the label in mono", "{n.stack ? <div style={{ fontFamily: FONT.mono" in arch)

# 10. qa.mjs.
check("F1 qa.mjs: coverage table printed", "Coverage table (feature → beat)" in qa)
check("F1 qa.mjs: missing-beat flag is BLOCKING", "MISSING BEAT" in qa and "produced no footage" in qa)
check("F4 qa.mjs: seed theme constants", "SEED_THEME = { bg: '#0d0a24', accent: '#ffc93c', card: '#161141' }" in qa)
check("F4 qa.mjs: theme check fails without theme.source", "still carries the seed theme with no recorded theme.source" in qa)
check("F4 qa.mjs: vignette printed", "Vignette: theme.vignette" in qa)
check("F5 qa.mjs: per-beat A/V table skeleton", "Per-beat A/V table" in qa and "supports it: ___" in qa)
check("F5 qa.mjs: under-gain warning over 0.20", "over 0.20" in qa and "underGain" in qa)
check("F6 qa.mjs: total runtime printed from measured narration", "Total runtime (measured narration + gaps + lead/tail)" in qa)
check("F6 qa.mjs: BLOCKING over 130s, ceiling 150s", "over the 2:10 (130s) hard rule" in qa and "2:30 (150s) absolute ceiling" in qa)
check("qa.mjs: BLOCKING findings exit non-zero", "process.exitCode = 1" in qa)

# 11. demo.md.
check("demo.md: under 2:10, no 1:30-1:50", "under 2:10" in demo and "1:30–1:50" not in demo)

# 11b. Fix-up (audit #58 MINOR-1 + sweep #21 cross-references).
check("Fix-up MINOR-1: allocation totals 103-126s", "Totals: 103–126s of content" in skill)
check("Fix-up Arch.tsx: stack label in accent color (SPEC F2 literal)", "color: C.accent, marginTop: 8" in arch)
check("Fix-up cross-ref: canonical statement under 2:10",
      "the demo video is under 2:10 (hard rule; absolute max 2:30)" in read("rules/hackathon-mode.mdc")
      and "the demo video is under 2:10 (hard rule; absolute max 2:30)" in read("skills/hackathon-scope/SKILL.md"))
check("Fix-up cross-ref: hackathon-pitch under 2:10, no old length",
      "under 2:10" in read("skills/hackathon-pitch/SKILL.md")
      and "1:30–1:50" not in read("skills/hackathon-pitch/SKILL.md")
      and "under 2:10" in read("skills/hackathon-pitch/assets/pitch-script-template.md"))
check("Fix-up cross-ref: README /demo under 2:10",
      "generate a narrated product demo video, under 2:10, of the app" in read("README.md"))
old_len = subprocess.run(
    ["grep", "-r", "1:30–1:50", "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("Fix-up cross-ref: old length 1:30-1:50 is 0 tree-wide (built)", old_len == "")

# 12. Counts unchanged post-fix17.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 13. No banned terms in the built skill tree (excl. node_modules).
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")

# 14. build.sh unchanged by fix18 (staged sources only).
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",
      len(build_lines) == 23647
      and hashlib.md5(build.encode("utf-8")).hexdigest() == "8dfacb47a2a6698d47e4b4a5f8d9126c")
check("build.sh still contains fix15 + fix17 block markers",
      "fix15 upstream block applied" in build and "fix17 upstream block applied" in build)

# 15. fix15 + fix17 verifiers still pass.
for name, script in (("fix15", "fix15/verify15.py"), ("fix17", "fix17/verify17.py")):
    r = subprocess.run(["python3", script], cwd=PLUGIN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    check(f"{name} verifier still passes ({tail})", r.returncode == 0)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
