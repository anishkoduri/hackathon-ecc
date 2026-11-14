#!/usr/bin/env python3
"""Dry-run #39 Leg 4 — fix #24 Cursor-readiness, statically checkable items.

Checks every statically-checkable fix #24 behavior against the build #4
built tree (~/workspace/hackathon-plugin/hackathon-ecc) and runs the C-1
hook pipe tests against scripts/hooks/block-no-verify.js by piping
Cursor-format JSON to node. Live-only items are NOT checked here; they are
listed as OWED in the dry-run report (LIVE_SMOKE_TEST.md §15).

Each check prints PASS/FAIL with file:line evidence. Exit 0 iff all pass.
"""
import base64
import json
import os
import re
import subprocess
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
HOOK = os.path.join(BUILT, "scripts/hooks/block-no-verify.js")

results = []


def check(name, ok, detail):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + " -- " + detail)


def read(rel):
    with open(os.path.join(BUILT, rel), encoding="utf-8") as fh:
        return fh.read()


def hook_run(command):
    """Pipe Cursor-format JSON to the hook; return (exit_code, stderr)."""
    payload = json.dumps({"tool_input": {"command": command}})
    p = subprocess.run(["node", HOOK], input=payload.encode(),
                       capture_output=True, timeout=60)
    return p.returncode, p.stderr.decode(errors="ignore").strip()


def main():
    orch = read("skills/orchestrate/SKILL.md")
    readme = read("README.md")
    obm = read("skills/orch-build-mvp/SKILL.md")
    hm = read("rules/hackathon-mode.mdc")
    grill = read("skills/grill-me/SKILL.md")
    taste = read("skills/design-taste-frontend/SKILL.md")
    uipro = read("skills/ui-ux-pro-max/SKILL.md")
    pdv = read("skills/pitch-deck-video/SKILL.md")
    tts = read("skills/pitch-deck-video/template/scripts/tts.mjs")
    common = read("rules/common-agents.mdc")
    rw = read("skills/readme-writer/SKILL.md")

    # L4-1 picker prerequisite verbatim once, pointers elsewhere.
    verb = "Select **Grok 4.7 High** in Cursor's model picker before the first build"
    check("L4-1a picker verbatim once in orchestrate",
          orch.count(verb) == 1,
          "orchestrate SKILL.md count=%d (step 4, :85)" % orch.count(verb))
    check("L4-1b picker pointers elsewhere",
          orch.count("see the picker note in step 4") >= 3
          and "see the picker note in `skills/orchestrate/SKILL.md` step 4" in readme
          and "see the picker note in orchestrate SKILL.md step 4" in obm,
          "orch pointers=%d; README:68 pointer present; orch-build-mvp pointer present"
          % orch.count("see the picker note in step 4"))

    # L4-2 dual-cited agent path lines in commands/ == 19; plan.md:199 house form.
    n = 0
    for fn in os.listdir(os.path.join(BUILT, "commands")):
        if fn.endswith(".md"):
            t = read("commands/" + fn)
            n += len(re.findall(
                r"- (?:Agent|Companion agent): `[a-z0-9-]+` "
                r"\(`agents/ecc-[a-z0-9-]+\.md`\)", t))
    check("L4-2a dual-cited agent path lines in commands/ == 19",
          n == 19, "count=%d" % n)
    plan = read("commands/plan.md")
    check("L4-2b plan.md:199 house form, not doubled",
          "Use the `architect` agent (`agents/ecc-architect.md`) only when" in plan
          and "(`agents/ecc-architect.md`) (`agents/ecc-architect.md`)" not in plan,
          "house form present once")
    tree_hits = 0
    for d in ("commands",):
        for fn in os.listdir(os.path.join(BUILT, d)):
            if fn.endswith(".md"):
                tree_hits += read(d + "/" + fn).count("- Agent: `agents/ecc-")
    check("L4-2c no path-only Agent lines left in commands/",
          tree_hits == 0, "path-only lines=%d" % tree_hits)

    # L4-3 general-subagent fallback paragraph in common-agents.mdc.
    check("L4-3 fallback paragraph in common-agents.mdc",
          "## If a named agent does not resolve (fix #24)" in common
          and "spawn a general subagent on `cursor-grok-4.6-high-fast`" in common,
          "heading + fallback line present")

    # L4-4 /demo gates intact.
    check("L4-4a /demo never automatic (orchestrate O4 + hackathon-mode H2)",
          "DEMOGATE_O4_F22" in orch and "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline" in orch
          and "DEMOGATE_H2_F22" in hm and "/demo is never part of this sequence" in hm,
          "O4 + H2 tokens present")
    check("L4-4b /demo explicit invocation only (step 6 O9 + final report)",
          "DEMOGATE_O9_F22" in orch
          and "A demo video is filmed only when the user invokes `/demo` explicitly" in orch,
          "O9 token + explicit-only wording present")
    check("L4-4c /demo not filmed in orch-build-mvp / orch-change-feature",
          "DEMOGATE_B2S1_F22" in obm and "`/demo` is not filmed here" in obm
          and "DEMOGATE_B3S1_F22" in read("skills/orch-change-feature/SKILL.md"),
          "B2S1 + B3S1 tokens present")
    check("L4-4d narration-key prompt ONLY when a demo video was asked for",
          "ONLY when the user asked for a demo video" in orch
          and "If the user did NOT ask for a demo video, do NOT send this prompt" in orch
          and "only when the user asked for a demo video" in hm
          and "DEMOGATE_B2S7_F22" in obm,
          "guard in orchestrate step 0, hackathon-mode §7, orch-build-mvp B2S7")
    check("L4-4e first-build order deploy -> commit -> README, no /demo in it",
          "Order: verify → polish → deploy → commit → README → final report" in orch
          and "deploy → commit → README" in hm,
          "order lines present without /demo")

    # L4-5 resume guards orchestrate steps 0-2 + grill-me handoff line.
    check("L4-5a resume guard step 0 (narration-key, no re-grill)",
          "Resume guard (fix #24)" in orch.split("0. **Narration-key")[1][:1500]
          if "0. **Narration-key" in orch else False,
          "orchestrate :58 resume guard + 'do NOT re-grill'")
    check("L4-5b resume guard step 1 (scope)",
          "if `docs/scope.md` already exists, verify it and proceed" in orch,
          "orchestrate :60")
    check("L4-5c resume guard step 2 (expansion)",
          "if the planner-approved list already exists" in orch
          and "do NOT re-run Phases 0–3" in orch,
          "orchestrate :61")
    check("L4-5d grill-me handoff line (After Grilling)",
          "orchestrate does not re-grill" in grill
          and "orchestrate steps 0–2 verify the record, scope, and expansion briefs exist" in grill,
          "grill-me SKILL.md 'After Grilling' section")

    # L4-6 inventory pointers: Taste step 4a + ui-ux-pro-max.
    check("L4-6a Taste step 4a reads inventory FIRST",
          "Read `new-skills/orchestrate/references/design-inventory.md` FIRST" in taste,
          "Taste SKILL.md step 4a")
    check("L4-6b ui-ux-pro-max Query Contract points at inventory",
          "read the design inventory (`skills/orchestrate/references/design-inventory.md`)" in uipro,
          "ui-ux-pro-max SKILL.md:91")

    # L4-7 FILM_F1/FILM_F5/FILM_F6 in pitch-deck-video; no bare film (F1)/(F5)/(F6).
    check("L4-7a FILM_F1/FILM_F5/FILM_F6 present",
          "coverage (FILM_F1)" in pdv and "the per-beat A/V table (FILM_F5)" in pdv
          and "never extra runtime (FILM_F6)" in pdv,
          "pitch-deck-video SKILL.md:241,:404,:405")
    check("L4-7b no bare film (F1)/(F5)/(F6) left in pitch-deck-video",
          "coverage (F1)" not in pdv and "(F5)" not in pdv and "(F6)" not in pdv,
          "bare pointers gone")

    # L4-8 F-09 orchestrate step 6 wording + readme-writer ledger source.
    check("L4-8a orchestrate step 6: readme-writer reads URL from the ledger",
          "`readme-writer` reads the deployed URL from the ledger" in orch,
          "orchestrate SKILL.md:97")
    check("L4-8b readme-writer takes deployed URL + video path from ledger",
          "take them from `.hackathon/run-ledger.md`" in rw,
          "readme-writer SKILL.md:95")

    # L4-9 tts.mjs Windows forms. L4-9a expectation updated by dry-run #41:
    # fix #26 §1 pip pinning changed the comment to the pinned form
    # (piper-tts==1.8.0, fix26/pip-pinning.md:124-125); the Windows
    # PowerShell guidance is still present, now pinned. Old verbatim
    # expectation ("py -m pip install piper-tts" without pin) is stale.
    check("L4-9a tts.mjs Windows PowerShell pip form (comment)",
          "Windows PowerShell: `py -m pip install piper-tts==1.8.0`" in tts,
          "tts.mjs:134-135 comment (pinned by fix #26 §1)")
    check("L4-9b tts.mjs Windows PowerShell pip form (error string)",
          "Windows PowerShell: py -m pip install piper-tts" in tts,
          "tts.mjs:180 error string")
    check("L4-9c tts.mjs USERPROFILE fallback for piper models dir",
          "process.env.USERPROFILE" in tts,
          "tts.mjs dataDir uses HOME ?? USERPROFILE")

    # L4-10 C-1 hook pipe tests.
    blocked_cases = [
        ("powershell -Command git commit --no-verify",
         'powershell -Command "git commit --no-verify -m test"'),
        ("powershell -c git commit --no-verify",
         'powershell -c "git commit --no-verify -m test"'),
        ("pwsh -Command git push --no-verify",
         'pwsh -Command "git push --no-verify"'),
        ("cmd /c git commit --no-verify",
         'cmd /c git commit --no-verify -m test'),
        ("cmd /c git commit -n (short flag)",
         'cmd /c "git commit -n -m test"'),
        ("powershell -Command git commit --no-veri (prefix)",
         'powershell -Command "git commit --no-veri -m test"'),
    ]
    for name, cmd in blocked_cases:
        code, err = hook_run(cmd)
        check("L4-10 BLOCKED: " + name, code == 2,
              "exit=%d stderr=%s" % (code, err[:100]))
    allowed_cases = [
        ("powershell -Command clean git commit",
         'powershell -Command "git commit -m test"'),
        ("powershell -Command npm test",
         'powershell -Command "npm test"'),
        ("cmd /c clean git push",
         'cmd /c git push origin main'),
        ("cmd /c npm run build",
         'cmd /c npm run build'),
        ("plain clean git commit",
         'git commit -m test'),
    ]
    for name, cmd in allowed_cases:
        code, err = hook_run(cmd)
        check("L4-10 ALLOWED: " + name, code == 0,
              "exit=%d stderr=%s" % (code, err[:100]))
    # -EncodedCommand base64 (UTF-16LE, as PowerShell expects): documented gap.
    b64 = base64.b64encode("git commit --no-verify -m test".encode("utf-16-le")).decode()
    code, err = hook_run('powershell -EncodedCommand %s' % b64)
    check("L4-10 GAP (documented): -EncodedCommand base64 NOT blocked",
          code == 0,
          "exit=%d (expected 0 = not blocked; scanner cannot read base64)" % code)
    # Plain bypass sanity.
    code, err = hook_run('git commit --no-verify -m test')
    check("L4-10 sanity: plain git commit --no-verify BLOCKED",
          code == 2, "exit=%d" % code)

    total = len(results)
    passed = sum(1 for _, ok in results if ok)
    print("\n%d/%d Leg 4 checks met" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
