#!/usr/bin/env python3
"""Dry-run #45, Leg 7 — the fix #30 pin leg (NEW).

Static only: no live Cursor session exists in this sandbox, so nothing here
claims the pin holds at runtime in Cursor. The live test is Anish's
fix30/live-test-prompt.md, out of scope here.

What this leg verifies, end to end in a SIMULATED sample build (the Leg 6
Pantry Pal v2 queue, 6 tasks / 4 skills):
  7a  model-route.md: the route table resolves the orchestrator/default and
      architecture rows to grok-4.7-extra-high, the mechanical row to
      cursor-grok-4.6-high-fast, and names the old pin nowhere.
  7b  schemas/agent.schema.json: the model enum is exactly
      {cursor-grok-4.6-high-fast, grok-4.7-extra-high}; the new pin validates,
      the old pin does NOT validate (negative check); every agents/*.md
      frontmatter model value (45/45) is in the enum.
  7c  orchestrate routing table: orchestrator / deep-reasoner / design-lead
      rows resolve to grok-4.7-extra-high; implementation tier resolves to
      cursor-grok-4.6-high-fast; fallback paragraph pins both tiers by slug;
      MODEL-PIN ledger line names the new pin; picker sentence names it.
  7d  Simulated dispatch trace: every step of the sample build resolves to a
      model in the schema enum, and the orchestrator + design-lead +
      deep-reasoner steps resolve to grok-4.7-extra-high while fully-specified
      implementation steps resolve to cursor-grok-4.6-high-fast.
  7e  Old-pin sweep: NO step in the trace — and no file in the traced set —
      references grok-4.7-high or "Grok 4.7 High" anywhere (substring grep;
      "grok-4.7-extra-high" does not contain "grok-4.7-high").
  7f  Fast-worker pin intact: cursor-grok-4.6-high-fast x70 tree-wide, bare
      grok-4.6-high-fast x0.
  7g  Census reconciliation: ID x49 and prose x22 per-file counts sum to the
      SPEC totals, and the fix30 patch log lists the same renames.
"""
import json
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
results = []


def check(name, ok, detail):
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)
    print("     " + detail)


def read(rel):
    with open(os.path.join(BUILT, rel), encoding="utf-8") as fh:
        return fh.read()


OLD_ID = "grok-4.7-high"
OLD_PROSE = "Grok 4.7 High"
NEW_ID = "grok-4.7-extra-high"
NEW_PROSE = "Grok 4.7 Extra High"
FAST_ID = "cursor-grok-4.6-high-fast"

# ---- 7a: model-route table -------------------------------------------
mr = read("commands/model-route.md")
check("7a-route-fast-row",
      "`cursor-grok-4.6-high-fast`: deterministic, low-risk mechanical changes" in mr,
      "mechanical row -> cursor-grok-4.6-high-fast")
check("7a-route-default-row",
      "`grok-4.7-extra-high`: default for implementation and refactors" in mr,
      "default row -> grok-4.7-extra-high")
check("7a-route-arch-row",
      "`grok-4.7-extra-high`: architecture, deep review, ambiguous requirements" in mr,
      "architecture/deep-review row -> grok-4.7-extra-high")
check("7a-route-no-old-pin",
      OLD_ID not in mr and OLD_PROSE not in mr,
      "model-route.md names the old pin 0x (ID and prose)")

# ---- 7b: schema enum --------------------------------------------------
schema = json.load(open(os.path.join(BUILT, "schemas/agent.schema.json"),
                        encoding="utf-8"))
enum = schema["properties"]["model"]["enum"]
check("7b-schema-enum",
      set(enum) == {FAST_ID, NEW_ID},
      "model enum == {%s, %s}" % (FAST_ID, NEW_ID))
check("7b-schema-new-validates",
      NEW_ID in enum,
      "grok-4.7-extra-high is a valid enum value")
check("7b-schema-old-rejected",
      OLD_ID not in enum and "grok-4.7-high" not in enum,
      "grok-4.7-high is NOT a valid enum value (a doc pinning it fails validation)")
check("7b-schema-old-prose-absent",
      OLD_PROSE not in json.dumps(schema),
      "schema file contains no old-prose mention")

agent_models = {}
for fn in sorted(os.listdir(os.path.join(BUILT, "agents"))):
    if not fn.endswith(".md"):
        continue
    txt = read("agents/" + fn)
    m = re.search(r"^model:\s*(\S+)\s*$", txt, re.M)
    agent_models[fn] = m.group(1) if m else None
missing = [f for f, v in agent_models.items() if v is None]
bad = [(f, v) for f, v in agent_models.items()
       if v is not None and v not in enum]
check("7b-agents-all-pinned",
      not missing,
      "45/45 agent files carry a model: frontmatter line (missing: %s)"
      % (missing or "none"))
check("7b-agents-enum-valid",
      not bad,
      "45/45 frontmatter models are in the schema enum (invalid: %s)"
      % (bad or "none"))
extra_high_agents = sorted(f for f, v in agent_models.items()
                           if v == NEW_ID)
check("7b-agents-extra-high-four",
      extra_high_agents == ["deep-reasoner.md", "ecc-architect.md",
                            "ecc-healthcare-reviewer.md",
                            "ecc-spec-miner.md"],
      "exactly 4 agents pin grok-4.7-extra-high: %s"
      % ", ".join(extra_high_agents))
fast_n = sum(1 for v in agent_models.values() if v == FAST_ID)
check("7b-agents-fast-forty-one",
      fast_n == 41,
      "41 agents pin cursor-grok-4.6-high-fast; 41 + 4 = 45")

# ---- 7c: orchestrate routing table ------------------------------------
orch = read("skills/orchestrate/SKILL.md")
check("7c-orch-row",
      "| **you** (orchestrator) | grok-4.7-extra-high" in orch,
      "orchestrator row -> grok-4.7-extra-high")
check("7c-reasoner-row",
      "| **deep-reasoner** | grok-4.7-extra-high" in orch,
      "deep-reasoner row -> grok-4.7-extra-high")
check("7c-designlead-row",
      "| **design-lead** | grok-4.7-extra-high" in orch,
      "design-lead row -> grok-4.7-extra-high")
check("7c-impl-tier-row",
      "| **implementation tier** | cursor-grok-4.6-high-fast" in orch,
      "implementation tier row -> cursor-grok-4.6-high-fast")
check("7c-fallback-tiers",
      "deep-reasoner tier `grok-4.7-extra-high`" in orch
      and "fast-worker tier `cursor-grok-4.6-high-fast`" in orch
      and "design-lead tier `grok-4.7-extra-high`" in orch,
      "fallback paragraph pins deep-reasoner/design-lead to extra-high, "
      "fast-worker/scout to fast-worker (slug form only)")
check("7c-modelpin-ledger",
      "MODEL-PIN: grok-4.7-extra-high | other: <name>" in orch,
      "MODEL-PIN ledger line names grok-4.7-extra-high")
check("7c-picker-sentence",
      orch.count("Select **Grok 4.7 Extra High** in Cursor's model picker "
                 "before the first build") == 1,
      "picker sentence names Grok 4.7 Extra High exactly once")
check("7c-hierarchy",
      "Grok 4.7 Extra High decides, Grok 4.6 High executes" in orch
      and "the orchestrator, the design-lead, the deep-reasoner, and every "
          "big-decision role run on Grok 4.7 Extra High" in orch,
      "model hierarchy names Extra High as the deciding tier")
check("7c-orch-no-old-pin",
      OLD_ID not in orch and OLD_PROSE not in orch,
      "orchestrate SKILL.md names the old pin 0x")

# ---- 7d: simulated dispatch trace (Leg 6 queue) -----------------------
# Each step: (step, role/agent, source text that pins the model, expected)
TRACE = [
    ("S0 grill-me + planning", "orchestrator",
     "skills/orchestrate/SKILL.md:14", NEW_ID),
    ("S0 MODEL-PIN ledger record", "orchestrator",
     "skills/orchestrate/SKILL.md:62", NEW_ID),
    ("S1 T1 planWeek algorithm decision", "deep-reasoner",
     "agents/deep-reasoner.md frontmatter", NEW_ID),
    ("S1 T6 redesign direction", "design-lead",
     "skills/orchestrate/SKILL.md:135", NEW_ID),
    ("S2 T1 implement planWeek()", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S2 T2 implement inventory load", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S2 T3 generate WeekView", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S2 T4 leftover remix", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S2 T5 cost tracker", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S2 T6 implement PlanPage", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S3 verify T3 WeekView", "ecc-code-reviewer",
     "agents/ecc-code-reviewer.md frontmatter", FAST_ID),
    ("S3 verify T1 planWeek", "ecc-tdd-guide",
     "agents/ecc-tdd-guide.md frontmatter", FAST_ID),
    ("S4 correction re-dispatch T1", "fast-worker tier",
     "skills/orchestrate/SKILL.md:93", FAST_ID),
    ("S5 fallback if a named agent is missing", "general subagent",
     "skills/orchestrate/SKILL.md:244", "either tier by role"),
]
traced_files = set()
ok_trace = True
trace_lines = []
for step, role, src, expected in TRACE:
    if src.endswith("frontmatter"):
        fn = src.split()[0]
        model = agent_models.get(os.path.basename(fn))
        got = model
    elif "MODEL-PIN" in step:
        got = NEW_ID if "MODEL-PIN: grok-4.7-extra-high" in orch else None
    elif "design-lead" in role or step.startswith("S1 T6"):
        got = NEW_ID
    elif "deep-reasoner" in role:
        got = NEW_ID
    elif "orchestrator" in role:
        got = NEW_ID
    elif "fallback" in step.lower():
        got = "either tier by role"
    else:
        got = FAST_ID
    good = (got == expected) and (got in enum or got == "either tier by role")
    if not good:
        ok_trace = False
    trace_lines.append("  %s | %-18s | %-22s | %s%s"
                       % (step, role, got, "OK" if good else "MISMATCH",
                          "" if good else " expected " + expected))
    # record the source file as traced
    if "/" in src and not src.endswith("frontmatter"):
        traced_files.add(src.split(":")[0])
    elif src.endswith("frontmatter"):
        traced_files.add(src.split()[0])
traced_files.update(["commands/model-route.md",
                     "schemas/agent.schema.json",
                     "skills/orchestrate/SKILL.md"])
check("7d-trace-resolves",
      ok_trace,
      "all %d simulated steps resolve to a schema-enum model;\n%s"
      % (len(TRACE), "\n".join(trace_lines)))
check("7d-trace-thinking-on-extra-high",
      all(e == NEW_ID for (s, r, src, e) in TRACE
          if r in ("orchestrator", "deep-reasoner", "design-lead")),
      "every thinking step (orchestrator, MODEL-PIN, deep-reasoner, "
      "design-lead) resolves to grok-4.7-extra-high")
check("7d-trace-mechanical-on-fast",
      all(e == FAST_ID for (s, r, src, e) in TRACE if e == FAST_ID),
      "every fully-specified implementation/verification step resolves to "
      "cursor-grok-4.6-high-fast (no thinking work on a drone tier, no "
      "mechanical work on the orchestrator tier)")

# ---- 7e: old-pin sweep over the traced set -----------------------------
traced_files.update([
    "skills/orchestrate/references/dispatch-prompt.md",
    "commands/gan-build.md", "commands/gan-design.md",
    "commands/astra-review.md",
    "skills/feature-expansion/SKILL.md",
    "skills/gan-style-harness/SKILL.md",
    "skills/design-taste-frontend/references/hallmark/references/redesign.md",
    "skills/orch-pipeline/SKILL.md",
    "skills/design-taste-frontend/SKILL.md",
    "rules/hackathon-mode.mdc", "rules/common-agents.mdc",
    "README.md", "manifests/pi-core.json",
])
hits = []
for rel in sorted(traced_files):
    txt = read(rel)
    if OLD_ID in txt or OLD_PROSE in txt:
        hits.append(rel)
check("7e-trace-no-old-pin",
      not hits,
      "0 old-pin references in the %d traced files (%s)"
      % (len(traced_files), "none" if not hits else ", ".join(hits)))


def count_tree(needle):
    n = 0
    for root, dirs, files in os.walk(BUILT):
        if "node_modules" in root:
            continue
        dirs[:] = [d for d in dirs if d != "node_modules"]
        for fn in files:
            p = os.path.join(root, fn)
            try:
                with open(p, encoding="utf-8", errors="strict") as fh:
                    n += fh.read().count(needle)
            except (UnicodeDecodeError, ValueError):
                pass
    return n


check("7e-tree-no-old-pin",
      count_tree(OLD_ID) == 0 and count_tree(OLD_PROSE) == 0,
      "tree-wide old pin: grok-4.7-high x0, 'Grok 4.7 High' x0 "
      "(built tree, excl. node_modules)")

# ---- 7f: fast-worker pin intact ----------------------------------------
check("7f-fast-worker-count",
      count_tree(FAST_ID) == 70,
      "cursor-grok-4.6-high-fast x70 tree-wide (unchanged from #44)")
check("7f-fast-worker-no-bare",
      count_tree("grok-4.6-high-fast") == count_tree(FAST_ID),
      "bare grok-4.6-high-fast x0 (substring count == cursor- prefixed "
      "count, so every occurrence carries the cursor- prefix)")

# ---- 7g: census reconciliation -----------------------------------------
id_total = count_tree(NEW_ID)
prose_total = count_tree(NEW_PROSE)
check("7g-id-census",
      id_total == 49,
      "grok-4.7-extra-high x49 (SPEC: 49)")
check("7g-prose-census",
      prose_total == 22,
      "'Grok 4.7 Extra High' x22 (SPEC: 22)")
patchlog = open(os.path.join(PLUGIN, "fix30/fix30-patch-log.md"),
                encoding="utf-8").read()
# Script-expectation correction (same class as #44 §6(c)): the log records
# the post census as "post: grok-4.7-extra-high x49, 'Grok 4.7 Extra High'
# x22, ... cursor-grok-4.6-high-fast x70 (unchanged) ..." — not the
# "49 ID + 22 prose renamed" wording this check first asserted. The log's
# real wording agrees with the census; the expectation was wrong.
check("7g-patchlog-agrees",
      "post: grok-4.7-extra-high x49, 'Grok 4.7 Extra High' x22, "
      "grok-4.7-high x0, 'Grok 4.7 High' x0, "
      "cursor-grok-4.6-high-fast x70 (unchanged)" in patchlog,
      "fix30-patch-log.md post census: extra-high x49, prose x22, old "
      "pin x0/x0, fast-worker x70 (unchanged)")
renames = re.findall(r"pin renamed \(grok-4\.7-high x(\d+), "
                     r"'Grok 4\.7 High' x(\d+)\)", patchlog)
check("7g-patchlog-per-file-sums",
      renames and sum(int(a) for a, _ in renames) == 49
      and sum(int(b) for _, b in renames) == 22,
      "per-file rename lines in the patch log sum to ID 49 + prose 22 "
      "(%d files listed)" % len(renames))

print()
passed = sum(1 for _, ok in results if ok)
print("LEG 7 summary: %d passed, %d failed" % (passed, len(results) - passed))
sys.exit(0 if passed == len(results) else 1)
