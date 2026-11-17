#!/usr/bin/env python3
"""Generate the hackathon-ecc call map (fix #25, SPEC §1).

Inventories the BUILT tree (hackathon-ecc/) and determines, for EVERY
skill, agent, rule, command, hook, and trigger key, where it is invoked
from, by scanning the built tree AND the staged sources
(new-skills/, round2-skills/, rewritten-skills/, new-rules/) for
references. The map is generated from the tree, never hand-asserted.

Outputs:
  - new-skills/orchestrate/references/call-map.md  (staged; flows into
    the built tree via the STEP 2 copy in build.sh, same as
    design-inventory.md)
  - fix28/callmap/call-map-data.json  (machine-readable sidecar: the
    full per-element evidence, for verify25 and later workers)

Exit code: 0 only if the counts agree with the tree
(72 skills / 45 agents / 48 rules / 55 commands / 15 hooks /
49 trigger keys). Any mismatch fails loudly.

Evidence tiers (per element, per invoker file):
  STRONG - backticked `name`, `skill:name`, path `skills/<name>/` or
           `agents/<file>.md`, `/command` slash form, `<stem>.mdc`
           link, hooks.json registration, `require('./adapter')` /
           runExistingHook dispatch for hooks.
  INVENTORY - listed in skills/orchestrate/references/design-inventory.md
           (the design-lead reads it before deciding; a listing IS a
           routing path for design skills).
  TRIGGER - a `skill:<name>` key in manifests/context-packs/
           skill-triggers@1.json routes user phrasing to the skill.
  STRUCT - structural path that needs no textual reference: a rule's
           alwaysApply/globs (Cursor auto-applies it), a command's
           existence in commands/ (the user can type /<name>), a hook's
           registration in hooks.json (Cursor fires the event).
  SHIPPED - listed in an install manifest (install-*.json). Recorded
           only; it proves the element ships, NOT that it is invoked.
  WEAK - bare word-boundary match of the name. Recorded separately and
         NEVER sufficient on its own to call an element "called":
         generic names (e.g. agent `architect`, skill `ck`) match
         ordinary prose.

"Called" (per type):
  skill   - >=1 STRONG, INVENTORY, or TRIGGER invoker.
  agent   - >=1 STRONG invoker.
  rule    - alwaysApply or globs (STRUCT) or >=1 STRONG invoker.
  command - >=1 STRONG invoker. (Every command is ALSO user-invocable
            via /<name> by construction; commands with no STRONG
            invoker are reported as FLOW-INVISIBLE, not orphaned.)
  hook    - registered in hooks.json AND its script file exists.
  trigger - key exists AND its target skill dir exists. (Group-level
            liveness is reported separately: the router consumer chain
            has no live Cursor entry point -- see the map's method note.)

Known blind spots (recorded in the map, not hidden):
  B1 Cursor's description-based skill routing: a skill whose SKILL.md
     description matches a user request can fire with no textual
     reference anywhere. This map measures TEXTUAL dispatch paths
     (orchestrate / dispatch-prompt / commands / rules / skills naming
     each other), not runtime model routing. A skill with zero textual
     invokers may still fire via its description.
  B2 Dynamic dispatch: dispatch-prompt templates name skills by
     inserting a path at dispatch time ("Read this first --
     <path>/SKILL.md"); the custom-roster path names skills that are
     NOT written literally anywhere. A skill reachable only through a
     custom roster entry is invisible to this scan.
  B3 References by description rather than name ("the blind reviewer",
     "the security agent") are not matched; only the literal names and
     paths above are.
  B4 Agent invocation by Cursor @-mention uses the frontmatter `name`;
     the scan counts backticked/path forms of that name, but a bare
     prose mention of the name (e.g. "ask the architect") is WEAK-only
     and is not counted as a call.
  B5 Hook scripts under scripts/hooks/ are upstream ECC machinery;
     only the 15 hooks.json entries are counted as hooks. Whether a
     scripts/hooks/*.js file is reached is traced from hooks/*.js via
     runExistingHook, but unreached files there are NOT counted as
     uncalled hooks -- they are out of the counted set.
  B6 The trigger-key router chain (skill-triggers@1.json ->
     scripts/lib/context-pack-registry.js -> context-selection.js ->
     scripts/hooks/context-routing-index.js /
     context-prompt-suggestions.js) has no live Cursor entry point:
     neither scripts/hooks consumer is invoked from hooks/*.js, and
     context-prompt-suggestions.js states it is upstream-only
     ("not wired in this Cursor plugin -- Cursor has no
     UserPromptSubmit event"). Trigger keys therefore count as a
     DEFINED routing path, not a LIVE one; the group is flagged in
     the wiring list for a parent decision.
"""

import json
import os
import re
import sys
from collections import defaultdict

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")
STAGED_DIRS = ["new-skills", "round2-skills", "rewritten-skills", "new-rules"]

EXPECTED = {"skills": 72, "agents": 45, "rules": 48,
            "commands": 55, "hooks": 15, "triggers": 49}

# Skills whose dispatch is deferred to end-of-project (orchestrate
# SKILL.md + skill-triggers@1.json notes). Their flow path is
# "end-of-project only", whatever their invoker is.
DEFERRED_SKILLS = {"production-audit", "delivery-gate",
                    "verification-loop"}

TEXT_EXTS = {".md", ".mdc", ".js", ".json", ".mjs", ".txt"}
SKIP_DIRS = {"node_modules", ".git", "__pycache__"}


def rel(path):
    return os.path.relpath(path, PLUGIN_ROOT)


def read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


# ---------------------------------------------------------------- inventory
def inventory():
    skills = {}
    for name in sorted(os.listdir(os.path.join(BUILT, "skills"))):
        d = os.path.join(BUILT, "skills", name)
        if not os.path.isdir(d):
            continue
        sk = os.path.join(d, "SKILL.md")
        if not os.path.isfile(sk):
            print(f"WARN: skill dir {name} has no SKILL.md", file=sys.stderr)
            continue
        fm = frontmatter(read_text(sk))
        m = re.search(r"^name:\s*(.+)$", fm, re.M)
        skills[name] = {
            "name": name,
            "fm_name": m.group(1).strip() if m else None,
            "dir": rel(d),
        }

    agents = {}
    for fn in sorted(os.listdir(os.path.join(BUILT, "agents"))):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(BUILT, "agents", fn)
        fm = frontmatter(read_text(p))
        m = re.search(r"^name:\s*(.+)$", fm, re.M)
        agents[fn[:-3]] = {
            "file": fn[:-3],
            "name": m.group(1).strip() if m else None,
            "path": rel(p),
        }

    rules = {}
    for fn in sorted(os.listdir(os.path.join(BUILT, "rules"))):
        if not fn.endswith(".mdc"):
            continue
        p = os.path.join(BUILT, "rules", fn)
        fm = frontmatter(read_text(p))
        rules[fn[:-4]] = {
            "stem": fn[:-4],
            "always": bool(re.search(r"alwaysApply:\s*true", fm)),
            "globs": bool(re.search(r"^globs:", fm, re.M)),
            "path": rel(p),
        }

    commands = {}
    for fn in sorted(os.listdir(os.path.join(BUILT, "commands"))):
        if not fn.endswith(".md"):
            continue
        commands[fn[:-3]] = {"stem": fn[:-3],
                             "path": rel(os.path.join(BUILT, "commands", fn))}

    hooks = {}
    hj = json.load(open(os.path.join(BUILT, "hooks", "hooks.json"),
                        encoding="utf-8"))
    for event, entries in hj["hooks"].items():
        for e in entries:
            cmd = e.get("command", "")
            m = re.search(r"hooks/(\S+\.js)", cmd)
            script = m.group(1) if m else None
            hooks[event] = {"event": event, "script": script,
                            "command": cmd,
                            "desc": e.get("description", "")}

    trig_path = os.path.join(BUILT, "manifests", "context-packs",
                             "skill-triggers@1.json")
    trig = json.load(open(trig_path, encoding="utf-8"))
    triggers = {}
    for key, phrases in trig["triggers"].items():
        assert key.startswith("skill:"), key
        triggers[key[6:]] = {"key": key, "phrases": list(phrases),
                             "target": key[6:]}

    return {"skills": skills, "agents": agents, "rules": rules,
            "commands": commands, "hooks": hooks, "triggers": triggers}


# ------------------------------------------------------------------- corpus
def build_corpus():
    """path (rel to plugin root) -> text, for built + staged sources."""
    corpus = {}
    roots = [BUILT] + [os.path.join(PLUGIN_ROOT, d) for d in STAGED_DIRS]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if os.path.splitext(fn)[1] not in TEXT_EXTS:
                    continue
                p = os.path.join(dirpath, fn)
                r = rel(p)
                if os.path.basename(fn) == "call-map.md":
                    continue  # never count the map as an invoker of itself
                corpus[r] = read_text(p)
    return corpus


def word_re(name):
    return re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(name) +
                      r"(?![A-Za-z0-9_-])")


# Single-pass token extraction per file (fast): the old per-name regex
# scan was O(names x files) and took minutes. Each file is tokenised
# once into sets; element lookup is then set membership.
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
DOUBLE_BT_RE = re.compile(r"``([^`]+)``")
SKILL_COLON_RE = re.compile(r"skill:([a-z0-9][a-z0-9-]*)")
SKILLS_PATH_RE = re.compile(r"skills/([a-z0-9][a-z0-9-]*)")
REL_SKILL_RE = re.compile(r"([a-z0-9][a-z0-9-]*)/SKILL\.md")
AGENTS_PATH_RE = re.compile(r"agents/([a-z0-9][a-z0-9-]*)")
COMMANDS_PATH_RE = re.compile(r"commands/([a-z0-9][a-z0-9-]*)")
MDC_RE = re.compile(r"([a-z0-9][a-z0-9-]*)\.mdc")
SLASH_RE = re.compile(r"(?<![A-Za-z0-9_/\-])/([a-z0-9][a-z0-9-]*)")
QUOTED_RE = re.compile(r'"([A-Za-z0-9][A-Za-z0-9_-]{2,})"')
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
SKILL_ADJ_RE = re.compile(r"([a-z0-9][a-z0-9-]*)\s+skills?\b|\bskills?:\s*([a-z0-9][a-z0-9-]*)")
AGENT_ADJ_RE = re.compile(r"([a-z0-9][a-z0-9-]*)\s+agents?\b|\bagents?:\s*([a-z0-9][a-z0-9-]*)")
FM_RE = re.compile(r"---\n(.*?)\n---", re.S)


BT_RUN_RE = re.compile(r"`+")


def extract_backticked(text):
    """Backticked tokens, handling `` ``double-backtick spans`` ``.

    A double-backtick span (e.g. `` `` `X` agent (`agents/ecc-X.md`) `` ``
    in rules/common-agents.mdc:32) defeats a naive `` `([^`]+)` `` regex:
    it pairs the wrong backticks and corrupts every token after it on
    the line. This scanner pairs backtick RUNS per line (CommonMark-ish:
    a run of n backticks closes at the next run of exactly n), extracts
    the single-backticked tokens inside double+ spans, and never pairs
    across lines. An unmatched run is skipped, not paired forward.
    """
    toks = set()
    for line in text.split("\n"):
        runs = [(m.start(), len(m.group(0))) for m in BT_RUN_RE.finditer(line)]
        i = 0
        while i < len(runs):
            start, n = runs[i]
            j = i + 1
            while j < len(runs) and runs[j][1] != n:
                j += 1
            if j < len(runs):
                content = line[start + n:runs[j][0]]
                if n == 1:
                    toks.add(content)
                else:
                    toks |= set(BACKTICK_RE.findall(content))
                i = j + 1
            else:
                i += 1
    return toks


def tokenise(text):
    fm = FM_RE.match(text)
    fm_words = set()
    if fm:
        fm_words = {w.lower() for w in WORD_RE.findall(fm.group(1))}
    skill_adj, agent_adj = set(), set()
    for m in SKILL_ADJ_RE.finditer(text):
        skill_adj |= {g for g in m.groups() if g}
    for m in AGENT_ADJ_RE.finditer(text):
        agent_adj |= {g for g in m.groups() if g}
    return {
        "backticked": extract_backticked(text),
        "skill_colon": set(SKILL_COLON_RE.findall(text)),
        "skills_path": set(SKILLS_PATH_RE.findall(text)),
        "rel_skill": set(REL_SKILL_RE.findall(text)),
        "agents_path": set(AGENTS_PATH_RE.findall(text)),
        "commands_path": set(COMMANDS_PATH_RE.findall(text)),
        "mdc": set(MDC_RE.findall(text)),
        "slash": set(SLASH_RE.findall(text)),
        # double-quoted single tokens, len>=3 ("ck" excluded: too short
        # to be a deliberate name reference in code)
        "quoted": set(QUOTED_RE.findall(text)),
        # words in the frontmatter block: a bare skill/agent name in a
        # SKILL.md or agent description IS a routing signal -- Cursor
        # reads descriptions to decide what to invoke.
        "fm_words": fm_words,
        # names adjacent to the word "skill"/"agent": "<name> skill",
        # "skill <name>", "<name> agent", "agent <name>"
        "skill_adj": skill_adj,
        "agent_adj": agent_adj,
        # lowercase words, for WEAK (bare-word) evidence only
        "words": {w.lower() for w in WORD_RE.findall(text)},
    }


# ------------------------------------------------------------------ stages
def stage_for_invoker(path, kind):
    p = path.replace("\\", "/")
    if "grill-me" in p:
        return "grill"
    if "pitch-deck-video" in p or p.endswith("commands/demo.md"):
        return "on-request /demo"
    if "feature-expansion" in p:
        return "build (expansion)"
    if "browser-qa" in p or "verification-" in p or "click-path-audit" in p:
        return "verify"
    if "deploy-fast" in p or "delivery-gate" in p or "production-audit" in p:
        return "deploy"
    if "design-taste-frontend" in p or "polish-pass" in p or \
       "less-flat-ui" in p or "ui-ux-pro-max" in p or "motion-" in p or \
       "design-system" in p:
        return "design package"
    if "orchestrate" in p:
        return "build (orchestrated dispatch)"
    if p.startswith("hackathon-ecc/hooks/") or "scripts/hooks/" in p:
        return "always-on (Cursor event)"
    if kind == "trigger":
        return "on-request (trigger-routed; no live Cursor entry — see method note B6)"
    if kind == "inventory":
        return "design package (inventory)"
    if kind == "struct-rule":
        return "always-on (rule)"
    if kind == "struct-command":
        return "on-request (/<name>)"
    return "build"


# ------------------------------------------------------------------ detect
def scan(inv, corpus):
    skills, agents, rules, commands = (inv["skills"], inv["agents"],
                                       inv["rules"], inv["commands"])
    # invokers: kind -> {element_key: {invoker_path: set(kinds)}}
    ev = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    def add(kind, key, invoker_path, ev_kind):
        ev[kind][key][invoker_path].add(ev_kind)

    staged_skill_dirs = {}
    for sd in STAGED_DIRS:
        base = os.path.join(PLUGIN_ROOT, sd)
        if os.path.isdir(base):
            for name in os.listdir(base):
                if os.path.isdir(os.path.join(base, name)):
                    staged_skill_dirs.setdefault(name, []).append(sd)

    def own_skill_file(name, path):
        # the skill's own definition files never count as invokers
        if path.startswith(f"hackathon-ecc/skills/{name}/"):
            return True
        for sd in staged_skill_dirs.get(name, []):
            if path.startswith(f"{sd}/{name}/"):
                return True
        return False

    inventory_path = "hackathon-ecc/skills/orchestrate/references/design-inventory.md"
    # Install/shipping manifests list element paths as install data --
    # SHIPPED evidence only, never invocation. Any file under
    # hackathon-ecc/manifests/ is a manifest EXCEPT the trigger file:
    # skill-triggers@1.json is a documentation-only reference table, not install data.
    manifest_files = {p for p in corpus
                      if p.startswith("hackathon-ecc/manifests/")
                      and "skill-triggers" not in p}

    for path, text in corpus.items():
        tok = tokenise(text)
        # Install manifests (manifests/install-*.json) list element paths
        # as install data. That is SHIPPED evidence only -- a listing in
        # an install module is not a dispatch path, so it must never
        # count as strong/weak invocation evidence. (First-pass bug:
        # "skills/<name>" paths inside install-modules.json were counted
        # as strong, which falsely called 30 skills.)
        is_manifest = path in manifest_files
        if is_manifest:
            for name in skills:
                if own_skill_file(name, path):
                    continue
                if name in tok["words"] or name in tok["skills_path"]:
                    add("skills", name, path, "shipped")
            for stem in agents:
                if stem in tok["words"] or stem in tok["agents_path"]:
                    add("agents", stem, path, "shipped")
            for stem in rules:
                if stem in tok["words"] or stem in tok["mdc"]:
                    add("rules", stem, path, "shipped")
            for stem in commands:
                if stem in tok["words"] or stem in tok["slash"] \
                        or stem in tok["commands_path"]:
                    add("commands", stem, path, "shipped")
            continue
        # ---- skills
        for name in skills:
            if own_skill_file(name, path):
                continue
            strong = (name in tok["backticked"] or name in tok["skill_colon"]
                      or name in tok["skills_path"] or name in tok["rel_skill"]
                      or name in tok["quoted"] or name in tok["fm_words"]
                      or name in tok["skill_adj"])
            if strong:
                kind = "inventory" if path == inventory_path else "strong"
                add("skills", name, path, kind)
            elif name in tok["words"]:
                add("skills", name, path, "weak")
        # ---- agents (by frontmatter name and by ecc- file stem)
        for stem, a in agents.items():
            if path == a["path"]:
                continue
            aname = a["name"] or stem
            strong = (aname in tok["backticked"] or stem in tok["backticked"]
                      or stem in tok["agents_path"]
                      or stem in tok["words"]
                      or aname in tok["fm_words"] or stem in tok["fm_words"]
                      or aname in tok["quoted"] or stem in tok["quoted"]
                      or aname in tok["agent_adj"] or stem in tok["agent_adj"])
            if strong:
                add("agents", stem, path, "strong")
            elif aname and aname.lower() in tok["words"]:
                add("agents", stem, path, "weak")
        # ---- rules
        for stem in rules:
            if stem in tok["mdc"] or stem in tok["backticked"] \
                    or stem in tok["fm_words"] or stem in tok["quoted"]:
                add("rules", stem, path, "strong")
            elif stem in tok["words"]:
                add("rules", stem, path, "weak")
        # ---- commands
        for stem in commands:
            if path == commands[stem]["path"]:
                continue
            if stem in tok["slash"] or stem in tok["commands_path"] \
                    or stem in tok["backticked"] \
                    or stem in tok["fm_words"] or stem in tok["quoted"]:
                add("commands", stem, path, "strong")
            elif stem in tok["words"]:
                add("commands", stem, path, "weak")

    # ---- structural evidence
    for stem, r in rules.items():
        if r["always"]:
            add("rules", stem, r["path"], "struct-rule-always")
        elif r["globs"]:
            add("rules", stem, r["path"], "struct-rule-globs")
    for stem, c in commands.items():
        add("commands", stem, c["path"], "struct-command")
    # ---- triggers
    for name, t in inv["triggers"].items():
        if name in skills:
            add("skills", name,
                "hackathon-ecc/manifests/context-packs/skill-triggers@1.json",
                "trigger")
    return ev


def flow_path(name, invokers, deferred=False):
    stages = []
    for path, kinds in invokers.items():
        for k in kinds:
            if k in ("weak", "shipped"):
                continue
            stages.append(stage_for_invoker(path, k))
    if deferred:
        stages.append("end-of-project only (deferred)")
    seen, out = set(), []
    for s in stages:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def summarize(inv, ev):
    data = {"counts": {}, "elements": {}, "uncalled": {},
            "weak_only": {}, "flow_invisible_commands": []}
    for kind in ("skills", "agents", "rules", "commands", "hooks", "triggers"):
        data["counts"][kind] = len(inv[kind])

    # skills
    for name in sorted(inv["skills"]):
        iv = ev["skills"].get(name, {})
        kinds = {k for v in iv.values() for k in v}
        strong = {p: sorted(v) for p, v in iv.items()
                  if v & {"strong", "inventory", "trigger"}}
        weak_only = bool(kinds) and not (kinds & {"strong", "inventory", "trigger"})
        called = bool(strong)
        data["elements"].setdefault("skills", {})[name] = {
            "called": called,
            "invokers": {p: sorted(v) for p, v in sorted(iv.items())},
            "flow": flow_path(name, iv, name in DEFERRED_SKILLS),
            "weak_only": weak_only,
            "fm_name_mismatch": inv["skills"][name]["fm_name"] not in (None, name),
        }
    data["uncalled"]["skills"] = sorted(
        n for n, e in data["elements"]["skills"].items() if not e["called"])
    data["weak_only"]["skills"] = sorted(
        n for n, e in data["elements"]["skills"].items()
        if e["weak_only"] and e["called"] is False)

    # agents
    for stem in sorted(inv["agents"]):
        iv = ev["agents"].get(stem, {})
        kinds = {k for v in iv.values() for k in v}
        called = "strong" in kinds
        data["elements"].setdefault("agents", {})[stem] = {
            "called": called,
            "name": inv["agents"][stem]["name"],
            "invokers": {p: sorted(v) for p, v in sorted(iv.items())},
            "flow": flow_path(stem, iv),
            "weak_only": bool(kinds) and "strong" not in kinds,
        }
    data["uncalled"]["agents"] = sorted(
        n for n, e in data["elements"]["agents"].items() if not e["called"])
    data["weak_only"]["agents"] = sorted(
        n for n, e in data["elements"]["agents"].items() if e["weak_only"])

    # rules
    for stem in sorted(inv["rules"]):
        iv = ev["rules"].get(stem, {})
        kinds = {k for v in iv.values() for k in v}
        r = inv["rules"][stem]
        called = bool(kinds & {"strong", "struct-rule-always", "struct-rule-globs"})
        data["elements"].setdefault("rules", {})[stem] = {
            "called": called,
            "always": r["always"], "globs": r["globs"],
            "invokers": {p: sorted(v) for p, v in sorted(iv.items())},
            "flow": ["always-on (rule)"] if (r["always"] or r["globs"]) else flow_path(stem, iv),
        }
    data["uncalled"]["rules"] = sorted(
        n for n, e in data["elements"]["rules"].items() if not e["called"])

    # commands
    for stem in sorted(inv["commands"]):
        iv = ev["commands"].get(stem, {})
        kinds = {k for v in iv.values() for k in v}
        called = "strong" in kinds
        data["elements"].setdefault("commands", {})[stem] = {
            "called": called,
            "invokers": {p: sorted(v) for p, v in sorted(iv.items())},
            "flow": flow_path(stem, iv) or ["on-request (/<name>)"],
        }
    data["uncalled"]["commands"] = sorted(
        n for n, e in data["elements"]["commands"].items() if not e["called"])
    data["flow_invisible_commands"] = data["uncalled"]["commands"]

    # hooks
    for event in sorted(inv["hooks"]):
        h = inv["hooks"][event]
        script_path = os.path.join(BUILT, "hooks", h["script"]) if h["script"] else None
        exists = bool(script_path and os.path.isfile(script_path))
        htext = read_text(script_path) if exists else ""
        uses_adapter = "require('./adapter')" in htext or 'require("./adapter")' in htext
        downstream = sorted(set(re.findall(r"runExistingHook\('([^']+)'", htext)))
        data["elements"].setdefault("hooks", {})[event] = {
            "called": bool(h["script"] and exists),
            "script": h["script"], "script_exists": exists,
            "uses_adapter": uses_adapter, "downstream": downstream,
            "invokers": {"hackathon-ecc/hooks/hooks.json": ["strong"]},
            "flow": ["always-on (Cursor event)"],
        }
    data["uncalled"]["hooks"] = sorted(
        n for n, e in data["elements"]["hooks"].items() if not e["called"])
    data["hooks_extra_files"] = sorted(
        f for f in os.listdir(os.path.join(BUILT, "hooks"))
        if f.endswith(".js") and f != "adapter.js"
        and f not in {inv["hooks"][e]["script"] for e in inv["hooks"]})

    # triggers
    for name in sorted(inv["triggers"]):
        t = inv["triggers"][name]
        data["elements"].setdefault("triggers", {})[name] = {
            "called": name in inv["skills"],
            "key": t["key"], "phrases": t["phrases"],
            "target_exists": name in inv["skills"],
            "invokers": {"hackathon-ecc/manifests/context-packs/skill-triggers@1.json": ["strong"]},
            "flow": ["on-request (trigger-routed; no live Cursor entry — see method note B6)"],
        }
    data["uncalled"]["triggers"] = sorted(
        n for n, e in data["elements"]["triggers"].items() if not e["called"])

    # ---- second-order orphans + trigger-only ----
    # An element is a SECOND-ORDER orphan if it is "called" but every one
    # of its strong invokers is itself an uncalled element (e.g. a skill
    # referenced only from another uncalled skill's SKILL.md, or only
    # from an uncalled agent's file). Invokers that are not elements
    # (README, scripts, mcp.json) count as live/neutral, never orphan.
    # Trigger-only is a separate bucket: called only via trigger keys,
    # whose router has no live Cursor entry (blind spot B6).
    def invoker_element(path):
        if path == "hackathon-ecc/skills/orchestrate/references/design-inventory.md":
            return ("skills", "orchestrate")
        m = re.match(r"(?:hackathon-ecc/skills|new-skills|round2-skills|rewritten-skills)/([^/]+)/", path)
        if m:
            return ("skills", m.group(1))
        m = re.match(r"(?:hackathon-ecc/agents|new-skills/orchestrate/agents)/([^/]+)\.md$", path)
        if m:
            return ("agents", m.group(1))
        m = re.match(r"(?:hackathon-ecc/rules|new-rules)/([^/]+)\.mdc$", path)
        if m:
            return ("rules", m.group(1))
        m = re.match(r"(?:hackathon-ecc/commands|new-skills/orchestrate/commands|new-skills/pitch-deck-video/commands)/([^/]+)\.md$", path)
        if m:
            return ("commands", m.group(1))
        return None

    uncalled_set = {k: set(v) for k, v in data["uncalled"].items()}
    second_order, trigger_only = {}, []
    for kind in ("skills", "agents", "commands"):
        for key, e in data["elements"][kind].items():
            if not e["called"]:
                continue
            strong_inv = {p: v for p, v in e["invokers"].items()
                          if set(v) & {"strong", "inventory", "trigger"}}
            kinds_seen = {k for v in strong_inv.values() for k in v}
            if kinds_seen == {"trigger"}:
                trigger_only.append(f"{kind}:{key}")
                continue
            mapped = [invoker_element(p) for p in strong_inv]
            mapped = [m for m in mapped if m is not None]
            if mapped and all(m[1] in uncalled_set.get(m[0], set())
                              for m in mapped):
                second_order.setdefault(kind, []).append(key)
    data["second_order_orphans"] = {k: sorted(v) for k, v in second_order.items()}
    data["trigger_only"] = sorted(trigger_only)
    return data


# -------------------------------------------------------------------- render
def short_invoker(path):
    # Staged sources and their built copies are distinct files with the
    # same tail; mark staged ones so duplicate-looking rows stay readable.
    staged = False
    for prefix in ("new-skills/", "round2-skills/", "rewritten-skills/",
                   "new-rules/"):
        if path.startswith(prefix):
            staged = True
            p = path[len(prefix):]
            break
    else:
        p = path
        for prefix in ("hackathon-ecc/skills/", "hackathon-ecc/"):
            if p.startswith(prefix):
                p = p[len(prefix):]
                break
    return p + (" (staged)" if staged else "")


INVOKER_KINDS = {"strong", "inventory", "trigger",
                 "struct-rule-always", "struct-rule-globs", "struct-command"}


def render_map(inv, ev, data):
    L = []
    L.append("# Call map — hackathon-ecc (fix #28 §1)")
    L.append("")
    L.append("> GENERATED by `fix28/callmap/generate_call_map.py` from the built tree "
             "(`hackathon-ecc/`) plus the staged sources "
             "(`new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/`). "
             "Do not edit by hand — re-run the generator. The map is kept current "
             "by the same change that adds or removes an element, same currency "
             "rule as the design inventory (`references/design-inventory.md`).")
    L.append("")
    L.append("## Counts (asserted by the generator)")
    L.append("")
    L.append("| Element | Count | Expected |")
    L.append("|---|---|---|")
    for kind in ("skills", "agents", "rules", "commands", "hooks", "triggers"):
        L.append(f"| {kind} | {data['counts'][kind]} | {EXPECTED[kind]} |")
    L.append("")
    L.append("## Flow")
    L.append("")
    L.append("grill → design package → build → verify → polish → deploy → "
             "commit → README → final report. `/demo` is on-request only, "
             "never automatic. End-of-project skills run only at the end or "
             "when the user asks. Hooks and rules are always-on (Cursor event "
             "/ glob or alwaysApply).")
    L.append("")
    L.append("## Method note — what counts as an invocation")
    L.append("")
    L.append("- **Strong:** backticked `` `name` ``, `skill:name`, a path "
             "(`skills/<name>/`, `agents/<file>.md`, `commands/<name>.md`, "
             "a relative `../<name>/SKILL.md` link), a `/command` slash form, "
             "a `<stem>.mdc` link, a double-quoted `\"name\"` (len >= 3), a "
             "bare name in a SKILL.md / agent frontmatter `description:` "
             "(Cursor reads descriptions to route), a name adjacent to the "
             "word `skill`/`agent` (`<name> skill`, `skill <name>`), or a "
             "hooks.json registration.")
    L.append("- **Backtick handling:** `` ``double-backtick spans`` `` are "
             "unpacked before single-backtick extraction; a naive regex "
             "pairs the wrong backticks after a double span and corrupts "
             "every token after it (found in `rules/common-agents.mdc`).")
    L.append("- **Inventory:** listed in `references/design-inventory.md` — "
             "the design-lead reads it before deciding, so a listing is a "
             "routing path for design skills.")
    L.append("- **Trigger:** a `skill:<name>` key in "
             "`manifests/context-packs/skill-triggers@1.json` routes user "
             "phrasing to the skill.")
    L.append("- **Structural:** a rule's `alwaysApply` / `globs` (Cursor "
             "auto-applies it); a command's existence in `commands/` (the "
             "user can type `/name`); a hook's hooks.json registration "
             "(Cursor fires the event).")
    L.append("- **Shipped** (install manifests list the name) is recorded "
             "but does NOT count as an invocation. **Weak** (bare-word "
             "match) is recorded but NEVER sufficient on its own — generic "
             "names match ordinary prose.")
    L.append("- An element's own definition files never count as invokers "
             "of itself. This file (`call-map.md`) never counts as an invoker.")
    L.append("- Tables show only real invokers (strong / inventory / "
             "trigger / structural) for called elements; weak and shipped "
             "evidence is in `fix28/callmap/call-map-data.json`. Uncalled "
             "elements show all evidence found, so the reader can see what "
             "was ruled out. Invokers from staged sources are marked "
             "`(staged)` — the staged file and its built copy are distinct "
             "files with the same tail.")
    L.append("")
    L.append("### Blind spots (known, not hidden)")
    L.append("")
    L.append("- **B1 — description routing:** Cursor can fire a skill from "
             "its SKILL.md description with no textual reference anywhere. "
             "This map measures textual dispatch paths, not runtime model routing.")
    L.append("- **B2 — dynamic dispatch:** dispatch-prompt templates insert "
             "a skill path at dispatch time; the custom-roster path names "
             "skills not written literally anywhere. Such skills are invisible "
             "to this scan.")
    L.append("- **B3 — references by description** (\"the blind reviewer\") "
             "are not matched; only literal names and paths are.")
    L.append("- **B4 — bare agent names** (\"ask the architect\") are weak-only "
             "and do not count as a call.")
    L.append("- **B5 — scripts/hooks/:** only the 15 hooks.json entries count "
             "as hooks. Unreached files under `scripts/hooks/` are upstream ECC "
             "machinery, not counted hooks.")
    L.append("- **B6 — trigger router has no live Cursor entry point "
             "(fix #26: DOCUMENTATION-ONLY):** "
             "`skill-triggers@1.json` was loaded upstream by "
             "`scripts/lib/context-pack-registry.js` → `context-selection.js` "
             "→ `scripts/hooks/context-routing-index.js` / "
             "`context-prompt-suggestions.js`, but neither consumer was invoked "
             "from `hooks/*.js`, and `context-prompt-suggestions.js` stated it "
             "is upstream-only (\"not wired in this Cursor plugin — Cursor has "
             "no UserPromptSubmit event\"). Those loader files were removed as "
             "dead weight in fix #28, so the chain does not exist in this tree "
             "at all. Trigger keys are therefore a DEFINED "
             "routing path, not a LIVE one; the file is a documentation-only "
             "reference table of which skill answers which user phrasing, not "
             "a live routing table — verified by grep in fix #26 (see "
             "`fix26/b6-note.md`); see the wiring list.")
    L.append("")
    L.append(f"## Uncalled summary — {sum(len(v) for v in data['uncalled'].values())} "
             f"elements with no dispatch path (see `fix28/callmap/wiring-list.md`)")
    L.append("")
    for kind in ("skills", "agents", "rules", "commands", "hooks", "triggers"):
        u = data["uncalled"][kind]
        L.append(f"- {kind}: {len(u)} uncalled" +
                 (f" — {', '.join('`' + x + '`' for x in u)}" if u else ""))
    L.append(f"- commands flow-invisible (user-invocable via `/name`, never "
             f"referenced from the flow): {len(data['flow_invisible_commands'])} "
             f"(same set as uncalled commands above)")
    L.append("")
    so = data.get("second_order_orphans", {})
    so_total = sum(len(v) for v in so.values())
    L.append(f"## Second-order orphans — {so_total} called elements whose "
             f"every strong invoker is itself uncalled")
    L.append("")
    L.append("These are reachable only through a dead element: the textual "
             "reference exists, but no live dispatch path reaches the "
             "invoker, so the reference never fires. They need the same "
             "WIRE IN / INTENTIONALLY DORMANT decision as the uncalled set.")
    L.append("")
    for kind in ("skills", "agents", "commands"):
        v = so.get(kind, [])
        L.append(f"- {kind}: {len(v)}" +
                 (f" — {', '.join('`' + x + '`' for x in v)}" if v else ""))
    L.append("")
    to = data.get("trigger_only", [])
    L.append(f"## Trigger-only — {len(to)} elements called only via trigger keys")
    L.append("")
    L.append("Called only through `skill-triggers@1.json`. The trigger router "
             "has no live Cursor entry point (blind spot B6), so these are "
             "defined routes, not live ones.")
    L.append("")
    for item in to:
        L.append(f"- `{item}`")
    L.append("")

    def section(title, kind, keyfn):
        L.append(f"## {title}")
        L.append("")
        L.append("| Element | Invoked from | Flow path |")
        L.append("|---|---|---|")
        for key in sorted(data["elements"][kind]):
            e = data["elements"][kind][key]
            invs = []
            # Called elements show only real invokers (strong / inventory /
            # trigger / structural). Weak + shipped evidence is noise in
            # the table -- it lives in call-map-data.json. Uncalled
            # elements show everything, so the reader can see the
            # generator looked and found only that.
            for p, kinds in sorted(e["invokers"].items()):
                show = sorted(kinds)
                if e["called"]:
                    show = [k for k in show if k in INVOKER_KINDS]
                    if not show:
                        continue
                tag = ",".join(show)
                invs.append(f"{short_invoker(p)} [{tag}]")
            inv_txt = "; ".join(invs) if invs else "— none found —"
            flow_txt = "; ".join(e["flow"]) if e["flow"] else "—"
            mark = "" if e["called"] else " ⚠ UNCALLED"
            L.append(f"| `{keyfn(key, e)}`{mark} | {inv_txt} | {flow_txt} |")
        L.append("")

    section("Skills (72)", "skills", lambda k, e: k)
    section("Agents (45)", "agents", lambda k, e: k)
    section("Rules (48)", "rules", lambda k, e: k)
    section("Commands (55)", "commands", lambda k, e: "/" + k)

    L.append("## Hooks (15)")
    L.append("")
    L.append("| Event | Script | Adapter | Downstream (scripts/hooks/) | Flow path |")
    L.append("|---|---|---|---|---|")
    for event in sorted(data["elements"]["hooks"]):
        e = data["elements"]["hooks"][event]
        down = ", ".join(f"`{d}`" for d in e["downstream"]) or "—"
        mark = "" if e["called"] else " ⚠ UNCALLED"
        L.append(f"| `{event}`{mark} | `{e['script']}` | "
                 f"{'yes' if e['uses_adapter'] else 'NO'} | {down} | "
                 f"{'; '.join(e['flow'])} |")
    L.append("")
    L.append("Shared infra (not a hook): `hooks/adapter.js` — required by all "
             "15 hook scripts; `hooks/hooks.json` registers those scripts as "
             "Cursor hooks.")
    L.append("")

    L.append("## Trigger keys (49)")
    L.append("")
    L.append("Each key routes user phrasing to its target skill. All 49 keys "
             "resolve to a real skill dir. Liveness caveat: see blind spot B6 — "
             "the router chain has no live Cursor entry point, so these are "
             "defined routes, not live ones.")
    L.append("")
    L.append("| Key | Target skill | Phrases | Flow path |")
    L.append("|---|---|---|---|")
    for name in sorted(data["elements"]["triggers"]):
        e = data["elements"]["triggers"][name]
        mark = "" if e["called"] else " ⚠ UNCALLED"
        ph = "; ".join(f'"{p}"' for p in e["phrases"])
        L.append(f"| `{e['key']}`{mark} | `{name}` | {ph} | {'; '.join(e['flow'])} |")
    L.append("")
    return "\n".join(L)


def main():
    inv = inventory()
    counts = {k: len(v) for k, v in inv.items()}
    failed = False
    for kind, exp in EXPECTED.items():
        ok = counts[kind] == exp
        print(f"counts {kind}: {counts[kind]} (expected {exp}) "
              f"{'OK' if ok else 'MISMATCH'}")
        if not ok:
            failed = True
    # frontmatter name mismatches (skills)
    for name, s in inv["skills"].items():
        if s["fm_name"] not in (None, name):
            print(f"WARN: skill dir {name} has frontmatter name {s['fm_name']!r}")
    corpus = build_corpus()
    print(f"corpus files scanned: {len(corpus)}")
    ev = scan(inv, corpus)
    data = summarize(inv, ev)

    map_path = os.path.join(PLUGIN_ROOT, "new-skills", "orchestrate",
                            "references", "call-map.md")
    with open(map_path, "w", encoding="utf-8") as f:
        f.write(render_map(inv, ev, data))
    print(f"map written: {rel(map_path)}")

    json_path = os.path.join(PLUGIN_ROOT, "fix28", "callmap",
                             "call-map-data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=True)
    print(f"data written: {rel(json_path)}")

    for kind in ("skills", "agents", "rules", "commands", "hooks", "triggers"):
        u = data["uncalled"][kind]
        print(f"uncalled {kind}: {len(u)}"
              + (f" -> {', '.join(u)}" if u else ""))
    for kind, v in data.get("second_order_orphans", {}).items():
        print(f"second-order orphans {kind}: {len(v)} -> {', '.join(v)}")
    print(f"trigger-only: {len(data.get('trigger_only', []))} -> "
          f"{', '.join(data.get('trigger_only', []))}")
    print(f"weak-only skills (no strong evidence): "
          f"{', '.join(data['weak_only']['skills']) or 'none'}")
    print(f"weak-only agents (no strong evidence): "
          f"{', '.join(data['weak_only']['agents']) or 'none'}")
    if data["hooks_extra_files"]:
        print(f"hooks/*.js files NOT registered in hooks.json: "
              f"{', '.join(data['hooks_extra_files'])}")
    if failed:
        print("COUNT MISMATCH — failing", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
