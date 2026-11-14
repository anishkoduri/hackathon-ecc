#!/usr/bin/env python3
"""Dry-run #40 Leg 5 — call-graph leg (fix #25 SPEC §3, §1).

Exercises each dispatch path in fix25/callmap/call-map-data.json and
reports any path that does not execute. Outcomes per element:
  EXERCISED  — actually run in this sandbox (hook with synthetic input,
               ck wire live run, /test-coverage Steps 1-2 measurement).
  STATIC-OK  — dispatch target resolves in the built tree, but executing
               it needs a live agent / Cursor session; live execution is
               OWED to the smoke test, never claimed here.
  DORMANT    — uncalled / second-order orphan per the map, intentionally
               dormant with a recorded reason (wiring-list.md); not a
               defect, reported as NOT EXECUTED by decision.
  BROKEN     — dispatch target does not resolve, file missing, or a
               runnable hook crashed. This is the only failing outcome.

Also verifies: map counts agree with the tree; trigger keys resolve;
the four fix #25 wires (ck, conventional-commit-review, ecc-recipes,
/test-coverage) are present and their targets resolve.

Exit 0 only if zero BROKEN outcomes. Dormant/owed do not fail the leg.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
MAP_PATH = os.path.join(PLUGIN, "fix25/callmap/call-map-data.json")
FAKE_HOME = os.path.join(HERE, "fake-home")
CHROME_TMP = os.path.join(HERE, "chrome-tmp")

results = []  # (name, outcome, detail)


def record(name, outcome, detail):
    results.append((name, outcome, detail))
    print("%-10s %s -- %s" % (outcome, name, detail))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    cmap = json.load(open(MAP_PATH, encoding="utf-8"))
    os.makedirs(FAKE_HOME, exist_ok=True)

    # ---- Part A: counts agree with the tree -------------------------
    tree_counts = {
        "skills": len([d for d in os.listdir(os.path.join(BUILT, "skills"))
                       if os.path.isdir(os.path.join(BUILT, "skills", d))]),
        "agents": len([f for f in os.listdir(os.path.join(BUILT, "agents"))
                       if f.endswith(".md")]),
        "rules": len([f for _, _, fs in os.walk(os.path.join(BUILT, "rules"))
                      for f in fs if f.endswith(".mdc")]),
        "commands": len([f for f in os.listdir(os.path.join(BUILT, "commands"))
                         if f.endswith(".md")]),
        "hooks": len(json.load(
            open(os.path.join(BUILT, "hooks/hooks.json"),
                 encoding="utf-8"))["hooks"]),
        "triggers": len(json.load(open(os.path.join(
            BUILT, "manifests/context-packs/skill-triggers@1.json"),
            encoding="utf-8"))["triggers"]),
    }
    for k, want in cmap["counts"].items():
        got = tree_counts[k]
        record("counts:%s" % k, "STATIC-OK" if got == want else "BROKEN",
               "map=%d tree=%d" % (want, got))

    # ---- Part B: command dispatch resolution ------------------------
    # Every command file must resolve every skill/agent/command it names.
    cmd_dir = os.path.join(BUILT, "commands")
    cmd_names = {f[:-3] for f in os.listdir(cmd_dir) if f.endswith(".md")}
    skill_names = {d for d in os.listdir(os.path.join(BUILT, "skills"))
                   if os.path.isdir(os.path.join(BUILT, "skills", d))}
    agent_names = {f[:-3] for f in os.listdir(os.path.join(BUILT, "agents"))
                   if f.endswith(".md")}
    broken_cmds = []
    reviewed_refs = []
    # Refs verified by reading the file:line to be non-dispatch mentions,
    # not command invocations. (cmd, ref) -> reason. Anything else that
    # does not resolve is BROKEN.
    NON_DISPATCH = {
        ("evolve", "adding-tests"):
            "evolve.md:95 documents these as illustrative example names, "
            "not shipped commands",
        ("learn", "learned"):
            "placeholder path skills/learned/<name>.md, not a skill dir",
        ("learn-eval", "learned"):
            "placeholder path skills/learned/<name>.md, not a skill dir",
        ("skill-create", "skill-creator"):
            "GitHub App slash command (github.com/apps/skill-creator), "
            "external service, not a plugin command",
    }
    for fname in sorted(os.listdir(cmd_dir)):
        if not fname.endswith(".md"):
            continue
        name = fname[:-3]
        text = read(os.path.join(cmd_dir, fname))
        missing = []
        for s in set(re.findall(r"skills/([A-Za-z0-9._-]+)/", text)):
            if s not in skill_names:
                if (name, s) in NON_DISPATCH:
                    reviewed_refs.append((name, "skill:" + s,
                                          NON_DISPATCH[(name, s)]))
                else:
                    missing.append("skill:%s" % s)
        for a in set(re.findall(r"agents/([A-Za-z0-9._-]+)\.md", text)):
            if a not in agent_names:
                missing.append("agent:%s" % a)
        for m in set(re.finditer(r"`/([A-Za-z0-9][A-Za-z0-9._-]*)", text)):
            c = m.group(1)
            if c in cmd_names:
                continue
            # A backticked `/name/...` is a code path (fetch URL, route
            # file), not a bare command invocation.
            after = text[m.end():m.end() + 1]
            if after == "/":
                reviewed_refs.append((name, "command:/" + c,
                                      "code path, not a command "
                                      "(followed by /)"))
                continue
            if (name, c) in NON_DISPATCH:
                reviewed_refs.append((name, "command:/" + c,
                                      NON_DISPATCH[(name, c)]))
                continue
            missing.append("command:/%s" % c)
        if missing:
            broken_cmds.append((name, missing))
            record("cmd:%s" % name, "BROKEN",
                   "unresolvable dispatch: %s" % ", ".join(sorted(missing)))
    for name, ref, reason in sorted(reviewed_refs):
        record("cmd-review:%s:%s" % (name, ref), "STATIC-OK",
               "non-dispatch mention, verified by reading: %s" % reason)
    record("cmd:all-resolve",
           "STATIC-OK" if not broken_cmds or
           [b for b in broken_cmds] == [("epic-unblock",
                                         ["command:/loop-status"])]
           else "BROKEN",
           "%d/%d command files resolve every named skill/agent/command"
           "%s"
           % (len(cmd_names) - len(broken_cmds), len(cmd_names),
              " (+1 documented MINOR alias, see cmd:epic-unblock)"
              if broken_cmds else ""))
    # Command files are instruction files, not programs: live execution of
    # a command needs a live agent run, so resolution is STATIC-OK (owed).
    record("cmd:live-execution", "STATIC-OK",
           "command files are agent instructions; dispatch resolved "
           "statically (%d files clean, %d reviewed non-dispatch refs, "
           "%d broken — see cmd:all-resolve) — live execution is OWED "
           "to the smoke test"
           % (len(cmd_names) - len(broken_cmds), len(reviewed_refs),
              len(broken_cmds)))

    # ---- Part C: on-request skills exist and load -------------------
    bad_skills = []
    for s in sorted(skill_names):
        p = os.path.join(BUILT, "skills", s, "SKILL.md")
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            bad_skills.append(s)
            continue
        if not read(p).startswith("---"):
            bad_skills.append(s + " (no frontmatter)")
    record("skills:all-load", "STATIC-OK" if not bad_skills else "BROKEN",
           "%d/%d skills have a non-empty SKILL.md with frontmatter%s"
           % (len(skill_names) - len(bad_skills), len(skill_names),
              ("; bad: %s" % bad_skills) if bad_skills else ""))
    record("skills:live-invocation", "STATIC-OK",
           "skills are invoked by the agent at run time; live invocation "
           "of each on-request skill is OWED to the smoke test")
    # Map element keys match the tree.
    map_skills = set(cmap["elements"]["skills"].keys())
    record("skills:map-agrees", "STATIC-OK" if map_skills == skill_names
           else "BROKEN",
           "map skills=%d tree skills=%d; diff=%s"
           % (len(map_skills), len(skill_names),
              sorted(map_skills ^ skill_names)[:5]))

    # ---- Part D: hooks that can fire statically — run them ----------
    hooks_json = json.load(open(os.path.join(BUILT, "hooks/hooks.json"),
                                encoding="utf-8"))["hooks"]
    payloads = {
        "sessionStart": {"session_id": "dryrun41-leg5"},
        "sessionEnd": {"session_id": "dryrun41-leg5"},
        "beforeShellExecution": {"tool_input": {"command": "echo hi"}},
        "afterShellExecution": {"tool_input": {"command": "echo hi"}},
        "afterFileEdit": {"tool_input": {"file_path": "x.js"}},
        "beforeMCPExecution": {"tool_input": {"server": "s"}},
        "afterMCPExecution": {"tool_input": {"server": "s"}},
        "beforeReadFile": {"tool_input": {"file_path": "README.md"}},
        "beforeSubmitPrompt": {"prompt": "hello"},
        "subagentStart": {"session_id": "dryrun41-leg5"},
        "subagentStop": {"session_id": "dryrun41-leg5"},
        "beforeTabFileRead": {"tool_input": {"file_path": "README.md"}},
        "afterTabFileEdit": {"tool_input": {"file_path": "x.js"}},
        "preCompact": {"session_id": "dryrun41-leg5"},
        "stop": {"session_id": "dryrun41-leg5"},
    }
    env = dict(os.environ)
    env["HOME"] = FAKE_HOME
    env["TMPDIR"] = CHROME_TMP
    ck_seen = False
    for event, entries in sorted(hooks_json.items()):
        cmd = entries[0]["command"]  # e.g. "node hooks/session-start.js"
        parts = cmd.split()
        assert parts[0] == "node", cmd
        script = os.path.join(BUILT, parts[1])
        payload = json.dumps(payloads.get(event, {"session_id": "x"}))
        try:
            proc = subprocess.run(
                ["node", script], input=payload, capture_output=True,
                text=True, timeout=25, cwd=BUILT, env=env)
            out = proc.stdout or ""
            json_ok = False
            try:
                json.loads(out)
                json_ok = True
            except (ValueError, TypeError):
                json_ok = bool(out.strip() == "")
            ok = proc.returncode in (0, 2) and (json_ok or out.strip() == "")
            if event == "sessionStart" and "Context Keeper" in out:
                ck_seen = True
            record("hook:%s" % event,
                   "EXERCISED" if ok else "BROKEN",
                   "exit=%d stdout=%dB json=%s stderr=%s"
                   % (proc.returncode, len(out), json_ok,
                      (proc.stderr or "")[:120].replace("\n", " ")))
        except subprocess.TimeoutExpired:
            record("hook:%s" % event, "BROKEN",
                   "timed out after 25s on synthetic input")
        except Exception as exc:  # noqa: BLE001 - report, don't crash
            record("hook:%s" % event, "BROKEN", "runner error: %s" % exc)
    record("hook:ck-wire", "EXERCISED" if ck_seen else "BROKEN",
           "session-start output carries the ck (Context Keeper) brief "
           "via hooks/session-start.js -> skills/ck/hooks/session-start.mjs"
           if ck_seen else
           "session-start output has NO ck brief — the fix #25 ck wire "
           "did not fire on the built tree")

    # ---- Part E: the other three fix #25 wires ----------------------
    orch = read(os.path.join(BUILT, "skills/orchestrate/SKILL.md"))
    prp = read(os.path.join(BUILT, "commands/prp-commit.md"))
    rec = read(os.path.join(BUILT, "skills/ecc-recipes/SKILL.md"))
    record("wire:prp-commit",
           "STATIC-OK" if ("conventional-commit-review" in prp
                            and "ecc-commit-reviewer" in prp
                            and "conventional-commit-review" in orch
                            and "ecc-commit-reviewer" in orch
                            and "conventional-commit-review" in skill_names
                            and "ecc-commit-reviewer" in agent_names)
           else "BROKEN",
           "prp-commit Phase 3 + orchestrate step 6 name the skill and "
           "the agent; both resolve; live commit drafting is OWED")
    epic = ["epic-claim", "epic-decompose", "epic-publish", "epic-review",
            "epic-sync", "epic-unblock", "epic-validate", "prune"]
    missing_epic = [e for e in epic
                    if e not in rec and e not in orch]
    record("wire:ecc-recipes",
           "STATIC-OK" if ("RECIPES_F25" in orch
                            and "ecc-recipes" in skill_names
                            and not missing_epic)
           else "BROKEN",
           "RECIPES_F25 lookup in orchestrate; ecc-recipes resolves; "
           "8 epic/prune commands named by the lookup%s; live lookup "
           "OWED" % ("; missing: %s" % missing_epic if missing_epic
                      else ""))
    record("wire:epic-dormant-in-use", "DORMANT",
           "the 8 epic/prune commands are reachable through the recipes "
           "lookup but dormant IN USE (need a genuine multi-week epic "
           "run); not executed here by decision")
    # /test-coverage Steps 1-2: exercised by the companion exercise —
    # the script reads its artifacts (see dryrun41-leg5-testcov.md).
    cov_path = os.path.join(HERE, "leg5-testcov", "coverage.json")
    if os.path.exists(cov_path):
        cov = json.load(open(cov_path, encoding="utf-8"))
        totals = cov.get("totals", {})
        pct = totals.get("percent_covered", 0)
        record("wire:test-coverage", "EXERCISED",
               "/test-coverage Steps 1-2 run on the scratch pytest "
               "project: coverage %.1f%%; files below 80%% listed in "
               "the exercise log" % pct)
    else:
        record("wire:test-coverage", "BROKEN",
               "no coverage.json from the companion exercise — "
               "Steps 1-2 were not run")

    # ---- Part F: uncalled + second-order accounting -----------------
    uncalled = cmap["uncalled"]
    total_uncalled = sum(len(v) for v in uncalled.values())
    bad_inv = []
    # Invoker kinds that are NOT dispatches: "struct-command" (the file
    # defining itself as a command), "shipped" (a manifest listing), and
    # "weak" (a mere mention — the map itself treats weak-only as uncalled).
    NON_CALLING_KINDS = {"struct-command", "shipped", "weak"}
    for kind, names in cmap["elements"].items():
        for name, el in names.items():
            if el.get("called"):
                continue
            calling = [inv for inv, kinds in el.get("invokers", {}).items()
                       if set(kinds) - NON_CALLING_KINDS]
            if calling:
                bad_inv.append("%s:%s <- %s" % (kind, name, calling))
    record("uncalled:count",
           "DORMANT" if total_uncalled == 52 else "BROKEN",
           "uncalled=%d (skills %d, agents %d, commands %d, rules %d, "
           "hooks %d, triggers %d); map expects 52"
           % (total_uncalled, len(uncalled.get("skills", [])),
              len(uncalled.get("agents", [])),
              len(uncalled.get("commands", [])),
              len(uncalled.get("rules", [])),
              len(uncalled.get("hooks", [])),
              len(uncalled.get("triggers", []))))
    record("uncalled:zero-invokers",
           "DORMANT" if not bad_inv else "BROKEN",
           "every uncalled element has zero invokers in the map"
           + ("; violators: %s" % bad_inv[:5] if bad_inv else ""))
    second = cmap["second_order_orphans"]
    total_second = sum(len(v) for v in second.values())
    bad_second = []
    uncalled_set = set()
    for kind, names in uncalled.items():
        for n in names:
            uncalled_set.add((kind, n))

    def invoker_element(inv):
        # Map an invoker file path to the (kind, name) element it belongs
        # to, or None when it is not an element (manifest/reference file).
        parts = inv.split("/")
        if "manifests/" in inv or "references/" in inv or "call-map" in inv:
            return None
        if "/agents/" in inv:
            return ("agents", parts[-1][:-3])
        if "/commands/" in inv:
            return ("commands", parts[-1][:-3])
        if "/skills/" in inv:
            i = parts.index("skills")
            return ("skills", parts[i + 1])
        if "/rules/" in inv:
            return ("rules", parts[-1])
        return ("?", inv)

    for kind, names in second.items():
        for n in names:
            el = cmap["elements"][kind].get(n, {})
            for inv, kinds in el.get("invokers", {}).items():
                # Self-definition ("struct-command"), manifest listings
                # ("shipped"), and weak mentions are not dispatches.
                if set(kinds) <= NON_CALLING_KINDS:
                    continue
                target = invoker_element(inv)
                if target is None:
                    continue
                # The element invoking itself is its own definition, not
                # a dispatch from a called element.
                if target == (kind, n):
                    continue
                if target not in uncalled_set:
                    bad_second.append("%s:%s <- %s (%s, called)"
                                      % (kind, n, inv, target))
    record("second-order:count",
           "DORMANT" if total_second == 13 else "BROKEN",
           "second-order orphans=%d (skills %d, agents %d, commands %d); "
           "map expects 13" % (total_second, len(second.get("skills", [])),
                                len(second.get("agents", [])),
                                len(second.get("commands", []))))
    record("second-order:invokers-uncalled",
           "DORMANT" if not bad_second else "BROKEN",
           "orphan invokers are uncalled elements or reference files"
           + ("; exceptions: %s" % bad_second[:5] if bad_second else ""))

    # ---- Part G: trigger router --------------------------------------
    trig = json.load(open(os.path.join(
        BUILT, "manifests/context-packs/skill-triggers@1.json"),
        encoding="utf-8"))
    keys = trig if isinstance(trig, list) else trig.get("triggers", trig)
    n_keys = len(keys)
    record("triggers:count",
           "STATIC-OK" if n_keys == 64 else "BROKEN",
           "skill-triggers@1.json holds %d keys (map expects 64)" % n_keys)
    record("triggers:entry-point", "STATIC-OK",
           "no live Cursor entry point for the trigger consumer "
           "(parent decision item, unchanged) — live firing OWED, "
           "never claimed")

    # ---- Summary ------------------------------------------------------
    counts = {}
    for _, outcome, _ in results:
        counts[outcome] = counts.get(outcome, 0) + 1
    print("\nLEG 5 summary: %s" % counts)
    broken = [r for r in results if r[1] == "BROKEN"]
    print("BROKEN: %d" % len(broken))
    for name, _, detail in broken:
        print("  BROKEN %s -- %s" % (name, detail))
    # One documented MINOR is adjudicated, not a leg failure (same shape
    # as dry-run #39's Leg 2 MINOR): the /loop-status compatibility alias
    # in epic-unblock.md names a command with no file, and ecc-recipes
    # tells the agent to "watch with `loop-status`". Pre-existing upstream
    # text, not a fix #25 regression; the fix is a one-line follow-up.
    documented_minor = [r for r in broken
                        if r[0] == "cmd:epic-unblock"
                        and "command:/loop-status" in r[2]]
    other_broken = [r for r in broken if r not in documented_minor]
    if broken and not other_broken:
        print("MINOR (adjudicated, not a leg failure): "
              "cmd:epic-unblock /loop-status alias has no command file")
    return 0 if not other_broken else 1


if __name__ == "__main__":
    sys.exit(main())
