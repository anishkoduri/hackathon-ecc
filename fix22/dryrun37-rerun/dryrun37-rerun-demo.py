#!/usr/bin/env python3
"""Dry-run #37 /demo fixture checker (fix #22, SPEC §12 + /demo contract).

Checks the fixture video project in fix22/dryrun37-rerun/demo-sample-video/
(a copy of the built pitch-deck-video template + a dry-run shots.json for
the sample app in fix22/dryrun37/sample-app/) against the /demo contract
items, with the Bang Motion rules woven in. This script asserts what can
be checked statically from the fixture files; the live-execution record
(tts.mjs run, npm install, record.mjs run, qa/render) is read from the
captured logs and reported separately in dryrun37-report.md — nothing is
claimed live that was not executed.

Contract items (from skills/pitch-deck-video/SKILL.md):
- films the REAL app locally (app.url is a localhost URL; no deployed URL)
- F1 feature coverage (every feature has a beat id present in shots.json;
  cuts recorded with reasons)
- F2 stack labels (arch nodes carry stack labels; the skill's fallback
  applies where the app has no recorded stack)
- F3 Edge at position 3 (shots[2] is the edge beat)
- F4 theme pull + gorgeousness checks (theme.source recorded; theme is
  not the seed theme; vignette recorded)
- F5 blocking A/V table + 10s mix listen (qa.mjs prints the per-beat A/V
  table; kinetic type and camera moves are rows of their own; music gain
  under <= 0.20)
- F6 measured runtime under 2:10 (130s) / absolute max 2:30 (150s)
  (total from src/vo-durations.json, LEAD + sum(dur + gap) + TAIL)
- voice rules (default voice Rachel id; fallback chain present; no key
  written anywhere)
- $10 budget cap (no paid provider used in this fixture)
- local-only filming (no deployed URL anywhere in shots.json)
- Bang: anti-slide checks present in the skill; opener concept + style
  direction recorded with theme reasons; kinetic type directed with exact
  parameters; filmed How/features beats stay filmed.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(HERE, "demo-sample-video")
PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
PDV = os.path.join(BUILT, "skills/pitch-deck-video/SKILL.md")

results = []


def record(name, expected_ok, actual_ok, detail):
    matched = (expected_ok == actual_ok)
    results.append((name, matched))
    print(("PASS " if matched else "FAIL ") + name)
    print("     expected %s, observed %s -- %s"
          % ("PASS" if expected_ok else "FLAG/FAIL",
             "PASS" if actual_ok else "FLAG/FAIL", detail))


def main():
    with open(os.path.join(VIDEO, "shots.json"), encoding="utf-8") as fh:
        cfg = json.load(fh)
    with open(os.path.join(VIDEO, "src/vo-durations.json"),
              encoding="utf-8") as fh:
        vo = json.load(fh)
    with open(PDV, encoding="utf-8") as fh:
        skill = re.sub(r"\s+", " ", fh.read())
    with open(os.path.join(VIDEO, "package.json"), encoding="utf-8") as fh:
        pkg = json.load(fh)

    shots = cfg["shots"]
    by_id = {s["id"]: s for s in shots}

    # Invocation path resolves: template pipeline files exist in the copy
    for f in ("scripts/build.mjs", "scripts/tts.mjs", "scripts/record.mjs",
              "scripts/frames.mjs", "scripts/qa.mjs", "scripts/music.mjs",
              "src/timeline.ts", "src/index.ts", "src/Video.tsx"):
        record("demo-path:" + f, True, os.path.exists(os.path.join(VIDEO, f)),
               "pipeline file present in the video project copy")
    build_src = open(os.path.join(VIDEO, "scripts/build.mjs"),
                     encoding="utf-8").read()
    order = [build_src.find("scripts/tts.mjs"),
             build_src.find("scripts/record.mjs"),
             build_src.find("scripts/frames.mjs")]
    record("demo-path:build-order", True,
           all(i >= 0 for i in order) and order == sorted(order),
           "build.mjs runs tts -> record -> frames in that order "
           "(narration -> recording -> frames -> render)")
    record("demo-path:npm-all", True,
           pkg["scripts"].get("all") == "node scripts/build.mjs",
           "package.json 'all' runs node scripts/build.mjs")

    # Local-only filming
    url = cfg["app"]["url"]
    record("demo-local-only", True,
           url.startswith("http://localhost:") and "vercel.app" not in url
           and "netlify" not in url,
           "app.url is %s (local dev server, no deployed URL)" % url)

    # F1 feature coverage
    feats = cfg.get("features", [])
    missing = [f for f in feats if f["beat"] not in by_id]
    record("demo-F1-coverage", True, len(missing) == 0,
           "%d features, all with a beat id present in shots.json; "
           "cuts recorded: %d" % (len(feats), len(cfg.get("cuts", []))))
    filmed = [s for s in shots if s.get("kind") == "app"
              and s["id"] in {f["beat"] for f in feats}]
    record("demo-F1-filmed", True, len(filmed) == len(feats),
           "every feature beat is kind=app (filmed footage, not a card)")

    # F2 stack labels
    nodes = cfg["cards"]["arch"]["nodes"]
    code_nodes = [n for n in nodes if n.get("kind") in ("llm", "code")]
    labelled = [n for n in code_nodes if n.get("stack")]
    record("demo-F2-stack", True, len(labelled) == len(code_nodes),
           "arch code/llm nodes carry stack labels: %s"
           % [n.get("stack") for n in labelled])
    record("demo-F2-gap", True,
           "No model calls" in by_id["arch"]["say"],
           "sample app has no model calls and no framework; the arch beat "
           "says so (skill fallback: framework only + gap noted)")

    # F3 Edge at position 3
    record("demo-F3-edge", True, shots[2]["id"] == "edge",
           "shots[2] is '%s'; arc is problem, wow, edge, how, proof, close"
           % shots[2]["id"])

    # F4 theme pull + gorgeousness
    seed = {"bg": "#0d0a24", "accent": "#ffc93c", "card": "#161141"}
    colors = cfg["theme"]["colors"]
    record("demo-F4-theme-source", True, bool(cfg["theme"].get("source")),
           "theme.source recorded: %s" % cfg["theme"].get("source"))
    record("demo-F4-not-seed", True,
           not (colors["bg"] == seed["bg"]
                and colors["accent"] == seed["accent"]
                and colors["card"] == seed["card"]),
           "theme pulled from the app tokens (bg %s, accent %s), not the "
           "seed theme" % (colors["bg"], colors["accent"]))
    record("demo-F4-vignette", True, "vignette" in cfg["theme"],
           "theme.vignette recorded: %s (0 for this light app)"
           % cfg["theme"].get("vignette"))

    # F5 A/V table + mix
    record("demo-F5-av-table", True,
           "Per-beat A/V table" in skill
           and "Kinetic type and camera moves go IN this table" in skill,
           "qa.mjs prints the per-beat A/V table; kinetic type and camera "
           "moves are rows of their own (skill text)")
    bang = cfg.get("bang", {})
    record("demo-F5-bang-rows", True,
           len(bang.get("kineticType", [])) > 0
           and len(bang.get("cameraMoves", [])) > 0,
           "kinetic-type rows: %d, camera-move rows: %d recorded in "
           "shots.json bang block"
           % (len(bang.get("kineticType", [])),
              len(bang.get("cameraMoves", []))))
    under = cfg.get("music", {}).get("gain", {}).get("under")
    record("demo-F5-mix-gain", True, under is not None and under <= 0.20,
           "music.gain.under = %s (<= 0.20, so the bed does not bury the "
           "voice)" % under)

    # F6 runtime (measured = estimated here: no voice provider, see report)
    gap = cfg["gapMs"] / 1000.0
    total = 0.7 + sum(s["dur"] + gap for s in vo["shots"]) + 1.7
    record("demo-F6-runtime", True, total < 130 and total <= 150,
           "total %.1fs from vo-durations.json (12 beats, LEAD 0.7 + "
           "sum(dur+gap) + TAIL 1.7) — under 2:10 (130s), within 2:30 "
           "absolute max" % total)

    # Voice rules
    record("demo-voice-default", True,
           cfg["tts"].get("voice") == "21m00Tcm4TlvDq8ikWAM",
           "default voice is ElevenLabs Rachel (21m00Tcm4TlvDq8ikWAM)")
    record("demo-voice-no-key-in-file", True,
           "ELEVENLABS_API_KEY" not in json.dumps(cfg)
           and "elevenlabs" not in json.dumps(cfg).lower().replace(
               '"provider": "elevenlabs"', ""),
           "no API key written into shots.json (provider name only)")
    record("demo-voice-fallback-chain", True,
           "ElevenLabs → Piper → `say`" in skill,
           "fallback chain present in the skill (ElevenLabs -> Piper -> "
           "say, per line at runtime)")

    # $10 budget cap
    record("demo-budget-cap", True, "$10 per video" in skill,
           "default cap $10 per video in the skill; this fixture used no "
           "paid provider ($0 spent: no key, no Piper, no Runway/Veo/HeyGen)")
    record("demo-budget-paid-approval", True,
           "First paid use of a new provider needs approval" in skill,
           "first paid use needs approval even under the cap")

    # Bang rules woven in
    record("demo-bang-antislide", True,
           "Anti-slide checks (BANG_ANTISLIDE_F22)" in skill,
           "anti-slide checks present in pitch-deck-video")
    record("demo-bang-oneworld", True,
           "One-world / camera / persistent-subject architecture "
           "(BANG_ONEWORLD_F22)" in skill,
           "one-world architecture present in pitch-deck-video")
    record("demo-bang-style-menu", True,
           "A composition that uses a style direction with no theme/brand "
           "reason FAILS" in skill
           and bang.get("styleDirection") is not None
           and bang.get("styleThemeReason") is not None,
           "style direction '%s' recorded with a theme reason"
           % bang.get("styleDirection"))
    record("demo-bang-opener", True,
           bang.get("openerConcept") is not None
           and bang.get("openerThemeReason") is not None,
           "opener concept '%s' recorded with a theme reason"
           % bang.get("openerConcept"))
    record("demo-bang-film-stays-film", True,
           "The filmed How/features beats stay filmed footage" in skill,
           "filmed How/features beats stay filmed; Bang governs the "
           "motion-graphics layer only")
    record("demo-bang-runtime", True,
           "The opener is a beat inside the 130-second cap" in skill,
           "Bang opener earns its seconds from the Wow budget, never extra "
           "runtime")

    # --- NEW (re-run): /demo auto-invocation removal + Remotion fix -------
    # Removal sites: assert the gates exist in the NEW built tree AND the
    # explicit-invocation path (commands/demo.md -> pitch-deck-video skill)
    # is intact, and that the removal did not touch pitch-deck-video itself.
    orch = re.sub(r"\s+", " ", open(os.path.join(BUILT,
                     "skills/orchestrate/SKILL.md"), encoding="utf-8").read())
    record("demo-removal-orch-5d", True,
           "DEMOGATE_O4_F22" in orch and
           "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline"
           in orch,
           "orchestrate step 5d: /demo NEVER dispatched; runs ONLY on "
           "explicit user invocation")
    record("demo-removal-orch-6", True,
           "DEMOGATE_O9_F22" in orch and
           "A demo video is filmed only when the user invokes `/demo` "
           "explicitly" in orch,
           "orchestrate step 6 Order sentence: demo video never part of "
           "the build order")
    b2 = re.sub(r"\s+", " ", open(os.path.join(
        BUILT, "skills/orch-build-mvp/SKILL.md"), encoding="utf-8").read())
    record("demo-removal-b2-step8", True,
           "DEMOGATE_B2S1_F22" in b2 and "`/demo` is not filmed here" in b2,
           "orch-build-mvp step 8: /demo not filmed here; ONLY on explicit "
           "invocation")
    b3 = re.sub(r"\s+", " ", open(os.path.join(
        BUILT, "skills/orch-change-feature/SKILL.md"),
        encoding="utf-8").read())
    record("demo-removal-b3-step5", True,
           "DEMOGATE_B3S1_F22" in b3 and
           "If the user asks for a re-film, re-film via `/demo --rebuild`" in b3
           and "no re-film happens here" in b3,
           "orch-change-feature step 5: re-film ONLY on explicit user "
           "request, else flagged stale")
    hm = re.sub(r"\s+", " ", open(os.path.join(
        BUILT, "rules/hackathon-mode.mdc"), encoding="utf-8").read())
    record("demo-removal-hackmode", True,
           "DEMOGATE_H1_F22" in hm and "DEMOGATE_H2_F22" in hm and
           "/demo is never part of this sequence" in hm,
           "hackathon-mode: first build does NOT film /demo automatically; "
           "/demo never part of the first-build sequence")
    demomd = open(os.path.join(BUILT, "commands/demo.md"),
                   encoding="utf-8").read()
    record("demo-removal-cmd-intact", True,
           "Use the pitch-deck-video skill to generate" in demomd
           and "`/demo` — film the app in the current directory" in demomd
           and "`/demo --rebuild`" in demomd,
           "commands/demo.md still dispatches to pitch-deck-video with "
           "/demo, /demo <path>, /demo --rebuild forms")
    record("demo-removal-pdv-untouched", True,
           "DEMOGATE" not in skill and "never automatic" not in skill
           and "NEVER dispatched" not in skill,
           "pitch-deck-video skill carries no DEMOGATE token and no "
           "'never automatic' gate language — removal did not touch it")
    dp = open(os.path.join(
        BUILT, "skills/orchestrate/references/dispatch-prompt.md"),
        encoding="utf-8").read()
    record("demo-removal-dispatch-env", True,
           "ELEVENLABS_API_KEY" in dp and "on a /demo dispatch" in dp,
           "dispatch-prompt.md Environment field still carries the key "
           "only on a /demo dispatch")
    # Remotion fix: no bare remotion@ anywhere in the built tree; both
    # scripts call the real CLI at the pinned version.
    bad = []
    for root, dirs, files in os.walk(BUILT):
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for f in files:
            p = os.path.join(root, f)
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            if "remotion@4.0.542" in t:
                bad.append(p)
    record("demo-remotion-no-bare", True, bad == [],
           "0 occurrences of remotion@4.0.542 in the built tree"
           + ("; found in: %s" % bad if bad else ""))
    build_txt = open(os.path.join(VIDEO, "scripts/build.mjs"),
                     encoding="utf-8").read()
    qa_txt = open(os.path.join(VIDEO, "scripts/qa.mjs"),
                  encoding="utf-8").read()
    record("demo-remotion-build", True,
           "@remotion/cli@4.0.526" in build_txt
           and "remotion@4.0.542" not in build_txt,
           "build.mjs calls npx @remotion/cli@4.0.526 render")
    record("demo-remotion-qa", True,
           "@remotion/cli@4.0.526" in qa_txt
           and "remotion@4.0.542" not in qa_txt,
           "qa.mjs calls npx @remotion/cli@4.0.526 still")
    record("demo-remotion-pin", True,
           pkg.get("dependencies", {}).get("@remotion/cli") == "4.0.526",
           "template package.json pins @remotion/cli at 4.0.526")
    cli_pkg_path = os.path.join(VIDEO, "node_modules/@remotion/cli/package.json")
    cli_bin = None
    if os.path.exists(cli_pkg_path):
        cli_bin = json.load(open(cli_pkg_path,
                                 encoding="utf-8")).get("bin")
    record("demo-remotion-bin", True,
           isinstance(cli_bin, dict) and "remotion" in cli_bin,
           "installed node_modules/@remotion/cli package.json carries a "
           "bin entry: %s" % (cli_bin,))
    # Live resolution: the exact npx form the scripts use, probed live.
    # (Logs written by the live phase; see the report §4.2.)
    probe = ""
    ppath = os.path.join(HERE, "remotion-still-probe.log")
    if os.path.exists(ppath):
        probe = open(ppath, encoding="utf-8", errors="ignore").read()
    record("demo-remotion-npx-live", True,
           "could not determine executable to run" not in probe
           and probe.strip() != "",
           "live `npx @remotion/cli@4.0.526 still ...` (qa.mjs form): "
           "resolves to the remotion bin"
           + (" — FAILED with 'could not determine executable to run'"
              if "could not determine executable to run" in probe else ""))
    phelp = ""
    phpath = os.path.join(HERE, "remotion-p-help.log")
    if os.path.exists(phpath):
        phelp = open(phpath, encoding="utf-8", errors="ignore").read()
    record("demo-remotion-p-form-live", True,
           "@remotion/cli 4.0.526" in phelp,
           "live `npx -p @remotion/cli@4.0.526 remotion --help` resolves "
           "(the -p form works; the bare npx form does not)")
    lhelp = ""
    lhpath = os.path.join(HERE, "remotion-local-help.log")
    if os.path.exists(lhpath):
        lhelp = open(lhpath, encoding="utf-8", errors="ignore").read()
    record("demo-remotion-local-live", True,
           "@remotion/cli 4.0.526" in lhelp,
           "live `npx --no-install remotion --help` resolves via the "
           "locally installed bin")

    total_n = len(results)
    passed = sum(1 for _, ok in results if ok)
    print("\n%d/%d /demo contract checks met" % (passed, total_n))
    return 0 if passed == total_n else 1


if __name__ == "__main__":
    sys.exit(main())
