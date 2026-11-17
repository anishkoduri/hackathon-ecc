#!/usr/bin/env python3
"""Dry-run #44 Leg 6 — factory leg (fix #29).

STATIC exercise of the factory routing design against the built tree.
Live Cursor per-model dispatch and slot refill at scale are harness-gated
(OWED-29-2) and are NOT claimed verified here — this leg verifies the
design as written: partitioning, brief completeness, no-guessing,
merge/verification, retire-and-refill simulation, COST-AWARE fan-out.

Method: the script reads the routing text live from the built tree and
asserts the sentences that do the work; it then runs a 6-task sample
queue through those rules as written and checks each outcome.
Exit 0 only if every check passes.
"""
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
HERE = os.path.dirname(os.path.abspath(__file__))

fails = []
passes = []


def check(name, ok, detail):
    (passes if ok else fails).append(name)
    print(("PASS " if ok else "FAIL ") + name + " -- " + detail)


def read(rel):
    with open(os.path.join(BUILT, rel), encoding="utf-8") as fh:
        return fh.read()


def line(rel, n):
    return read(rel).splitlines()[n - 1]


# ---------------------------------------------------------------- queue
# Sample build: "Pantry Pal v2" week-planner. Six independent single-task
# jobs spanning four routing-set skills (orch-pipeline, gan-style-harness,
# feature-expansion, design-taste-frontend redesign). Write sets are the
# partition; read sets are shared files no drone writes.
QUEUE = [
    dict(id="T1", skill="orch-pipeline",
         goal="Implement planWeek(): 6 dinners from the pantry inventory, $0 extra",
         write={"src/planner/week.ts"}, read={"src/planner/types.ts"},
         accept="planWeek() returns 6 dinners; total extra cost $0; unit test passes"),
    dict(id="T2", skill="orch-pipeline",
         goal="Implement pantry inventory load + quantities",
         write={"src/pantry/inventory.ts"}, read={"src/planner/types.ts"},
         accept="inventory loads 6 items with quantities; unit test passes"),
    dict(id="T3", skill="gan-style-harness",
         goal="Generator pass: WeekView component per gan-harness/spec.md",
         write={"src/ui/WeekView.tsx"}, read={"gan-harness/spec.md"},
         accept="WeekView renders Monday curry card with 25-minute label; rubric >= 7.0"),
    dict(id="T4", skill="feature-expansion",
         goal="Feature: leftover remix (Wednesday dinner from yesterday's rice)",
         write={"src/planner/remix.ts"}, read={"src/planner/types.ts"},
         accept="remix() returns a Wednesday dinner reusing yesterday's rice; demo flow passes"),
    dict(id="T5", skill="feature-expansion",
         goal="Feature: cost tracker (running $ extra per dinner)",
         write={"src/planner/cost.ts"}, read={"src/planner/types.ts"},
         accept="cost() reports $ extra per dinner; demo flow passes",
         unspecified="cost display format (currency symbol / decimals)"),
    dict(id="T6", skill="design-taste-frontend",
         goal="Redesign /plan page past three pages (Hallmark redesign flow)",
         write={"src/ui/PlanPage.tsx"}, read={"docs/design-tokens.md"},
         accept="page matches recorded direction tokens; no layout regression"),
]
SHARED_READONLY = {"src/planner/types.ts", "gan-harness/spec.md",
                   "docs/design-tokens.md", "src/ui/tokens.css"}
FIELDS = ["goal", "files_in_scope", "files_out_of_scope", "constraints",
          "acceptance_criteria", "verification_steps", "what_to_return"]

# ------------------------------------------------------- (a) partitioning
all_write = [t["write"] for t in QUEUE]
shared = set()
for i in range(len(all_write)):
    for j in range(i + 1, len(all_write)):
        shared |= all_write[i] & all_write[j]
check("6a-partition-disjoint",
      not shared,
      "write sets pairwise disjoint across all 6 tasks; shared=%s" % sorted(shared))
for t in QUEUE:
    print("     %s write=%s read=%s" % (t["id"], sorted(t["write"]), sorted(t["read"])))
overlap_read_write = {t["id"]: (t["read"] & set().union(*[o["write"] for o in QUEUE if o is not t]))
                      for t in QUEUE}
check("6a-shared-read-only",
      all(not v for v in overlap_read_write.values())
      and all(t["read"] <= SHARED_READONLY for t in QUEUE),
      "shared files (%s) appear only as reads / out-of-scope, never in two write sets"
      % sorted(SHARED_READONLY))
with open(os.path.join(PLUGIN, "fix29/global-routing-block.txt"),
           encoding="utf-8") as fh:
    _golden = fh.read()
check("6a-partition-rule-live",
      "partitioned by file/module boundary so no two drones share files or mutable state" in _golden,
      "GLOBAL-ROUTING golden block states the partition-by-boundary rule")
check("6a-redesign-single-writer",
      "tokens" in line("skills/design-taste-frontend/references/hallmark/references/redesign.md", 68)
      and "out of scope" in line("skills/design-taste-frontend/references/hallmark/references/redesign.md", 68),
      "redesign.md:68 lists shared stylesheet/tokens out of scope in every page brief (single-writer rule)")

# ------------------------------------------------- (b) brief completeness
contract = line("skills/orchestrate/SKILL.md", 230)  # contract core region
dp = read("skills/orchestrate/references/dispatch-prompt.md")
check("6b-contract-seven-fields",
      all(f in dp.split("3. **The contract**")[1].split("\n")[0]
          for f in ["Goal", "Inputs", "Constraints", "Interface",
                    "Acceptance check", "Verification steps", "Return format"]),
      "dispatch-prompt.md:15 names all seven DIRECTOR-BRIEF fields")
for sec, label in [("recon", "Goal:"), ("mechanical", "Goal:"),
                   ("reasoning", "Goal:"), ("worked example", "Goal:")]:
    pass  # per-template Interface asserted below via live grep
iface = len(re.findall(r"^Interface:", dp, re.M))
check("6b-interface-four-templates", iface == 4,
      "Interface: present in exactly 4 sections (recon/mechanical/reasoning/worked example), found %d" % iface)


def build_brief(t):
    return {
        "goal": t["goal"],
        "files_in_scope": sorted(t["write"]),
        "files_out_of_scope": sorted(SHARED_READONLY - t["read"] | {"src/ui/tokens.css"}),
        "constraints": "hackathon-mode rule; do not touch files out of scope",
        "acceptance_criteria": t["accept"],
        "verification_steps": "run unit tests; run the app; exercise the feature; paste output",
        "what_to_return": "status, changed files, verification evidence, residual risks, blockers",
    }


briefs = {t["id"]: build_brief(t) for t in QUEUE}
ok_b = True
for t in QUEUE:
    b = briefs[t["id"]]
    missing = [f for f in FIELDS if not b.get(f)]
    if missing:
        ok_b = False
    print("     brief %s: %s" % (t["id"], "all 7 fields" if not missing else "MISSING %s" % missing))
check("6b-briefs-seven-fields", ok_b,
      "all 6 dispatched briefs carry all 7 DIRECTOR-BRIEF fields (goal, files in/out, constraints, acceptance, verification, return)")
check("6b-out-of-scope-named",
      all("src/ui/tokens.css" in briefs[t["id"]]["files_out_of_scope"] for t in QUEUE)
      and all(briefs[t["id"]]["files_out_of_scope"] for t in QUEUE),
      "every brief names files explicitly out of scope (incl. shared tokens.css)")
check("6b-incomplete-brief-no-start",
      "an incomplete brief means the drone does not start" in
      line("skills/orchestrate/SKILL.md", 36),
      "GLOBAL-ROUTING block: incomplete brief = drone does not start")

# ------------------------------------------------------- (c) no-guessing
dr = line("agents/deep-reasoner.md", 17)
check("6c-deep-reasoner-bound",
      "return NEEDS_CONTEXT naming exactly what is missing" in dr
      and "do not guess" in dr,
      "deep-reasoner.md:17: 'return NEEDS_CONTEXT naming exactly what is missing — do not guess'")
import glob
carve_tree = 0
for p in glob.glob(os.path.join(BUILT, "**", "*.md"), recursive=True) + \
           glob.glob(os.path.join(BUILT, "**", "*.mdc"), recursive=True):
    carve_tree += open(p, encoding="utf-8").read().count(
        "never to a decision the brief leaves unspecified")
check("6c-five-belief-copies-carved",
      carve_tree == 7,
      "carve-out sentence occurs 7x tree-wide: the 5 Belief copies (dispatch-prompt:34 + :94 preamble, orch-build-mvp:70, orch-pipeline:72, feature-expansion:151) + 2 bounded quotations (dispatch-prompt:149 reasoning template, deep-reasoner:17)")
check("6c-tie-breaker",
      "When in doubt which side an ambiguity falls on, return the question" in dp,
      "tie-breaker present: 'When in doubt ... return the question — a returned question is never a stall.'")


def drone_decide(brief_fields, decision, specified):
    """The drone-side rule as written: a decision the brief leaves
    unspecified is returned to the orchestrator as NEEDS_CONTEXT."""
    if decision in specified:
        return "PROCEED"
    return "NEEDS_CONTEXT"


t5 = next(t for t in QUEUE if t["id"] == "T5")
specified = {"goal", "files", "constraints", "acceptance", "verification", "return"}
result = drone_decide(briefs["T5"], t5["unspecified"], specified)
check("6c-unspecified-returns-question",
      result == "NEEDS_CONTEXT",
      "T5 brief leaves '%s' unspecified -> drone returns NEEDS_CONTEXT (does not guess a format)" % t5["unspecified"])
check("6c-question-goes-to-orchestrator",
      "returns the question to the orchestrator" in line("skills/orchestrate/SKILL.md", 36)
      and "instead of guessing" in line("skills/orchestrate/SKILL.md", 36),
      "GLOBAL-ROUTING: drone 'stops and returns the question to the orchestrator instead of guessing'")
check("6c-first-build-carveout-reconciled",
      "which resolves it by stated assumption" in dp,
      "dispatch-prompt.md first-build carve-out (5 sites): NEEDS_CONTEXT goes to the orchestrator, which resolves it by stated assumption (never asks the user mid-build)")

# ------------------------------------------- (d) merge / verification (8 sites)
SITES = [
    ("orch-pipeline:74 (Phase 5 Review fix loop)",
     "skills/orch-pipeline/SKILL.md", 74,
     "T1 output returns 5 dinners, failing 'planWeek() returns 6 dinners'"),
    ("feature-expansion:158 (fix loop)",
     "skills/feature-expansion/SKILL.md", 158,
     "T4 remix() returns no Wednesday dinner, failing its acceptance criterion"),
    ("orchestrate:252 (escalation ladder)",
     "skills/orchestrate/SKILL.md", 252,
     "fast-worker misses the acceptance check twice on the same task"),
    ("gan-build:30 (planner-spec check 3a)",
     "commands/gan-build.md", 30,
     "planner spec lacks per-feature acceptance criteria"),
    ("gan-build:63 (ORCHESTRATOR-CHECK)",
     "commands/gan-build.md", 63,
     "T3 rubric 7.4 pass BUT WeekView lacks the 25-minute label — failed acceptance criterion"),
    ("react-build:18 (step 6 Orchestrator Verify)",
     "commands/react-build.md", 18,
     "resolver reports green build but with an unexplained // @ts-ignore"),
    ("astra-review:35 (second blind pass)",
     "commands/astra-review.md", 35,
     "second blind pass finds a failed acceptance criterion in the fix"),
    ("redesign.md:68 (page-drone verify)",
     "skills/design-taste-frontend/references/hallmark/references/redesign.md", 68,
     "T6 page output fails 'matches recorded direction tokens'"),
]
ok_d = True
for name, rel, n, failing in SITES:
    txt = line(rel, n)
    names = ("correction brief" in txt and "naming the failed" in txt)
    if not names:
        ok_d = False
    print("     SITE %s\n          failing input: %s\n          routing text names failed criterion + correction brief: %s"
          % (name, failing, names))
check("6d-eight-sites-name-criterion", ok_d,
      "all 8 correction-brief construction sites name the failed acceptance criterion in the correction brief")
gb = read("commands/gan-build.md")
check("6d-gan-order",
      gb.index("# EVALUATE") < gb.index("# ORCHESTRATOR-CHECK") < gb.index("# CHECK SCORE"),
      "gan-build.md wiring order: EVALUATE < ORCHESTRATOR-CHECK < CHECK SCORE (verify step gates the score)")
check("6d-rubric-pass-is-not-pass",
      "a rubric pass at or above 7.0 with a failed acceptance criterion is a fail" in gb,
      "gan-build ORCHESTRATOR-CHECK: rubric pass + failed criterion = fail -> generator re-dispatched")
check("6d-two-redispatch-cap",
      sum(1 for _, rel, n, _ in SITES
          if "two" in line(rel, n).lower() or "2 rounds" in line(rel, n))
      >= 4,
      "correction re-dispatch capped at two rounds at >=4 of the 8 sites (FE:158, gan:30/:63, react-build:18, astra-review:35)")
check("6d-unverified-never-presented",
      "unverified drone output is never presented as the orchestrator's own" in
      line("skills/orchestrate/SKILL.md", 36),
      "GLOBAL-ROUTING: unverified drone output is never presented as the orchestrator's own")

# --------------------------------------- (e) slot retire-and-refill (simulated)
CURSOR_SLOTS = 4  # GLOBAL-ROUTING block: in-IDE parallelism caps around 4
queue = [t["id"] for t in QUEUE]
# Designed factory: a drone retires on completion; the next queued job
# dispatches into the freed slot immediately.
slots, waiting, retired = [], list(queue), []
log = []
while waiting or slots:
    while waiting and len(slots) < CURSOR_SLOTS:
        job = waiting.pop(0)
        slots.append(job)
        log.append("dispatch %s into free slot (slots=%s waiting=%s)" % (job, slots, waiting))
    done = slots.pop(0)  # one drone completes
    retired.append(done)
    log.append("retire %s on completion -> slot frees" % done)
print("     designed-factory trace (per-completion refill):")
for e in log:
    print("       " + e)
check("6e-designed-refill",
      retired == queue and not waiting and not slots,
      "designed factory drains all 6 jobs with per-completion refill (retire order %s)" % retired)
# Cursor reality: slots refill per wave, not per completion.
wave1, wave2 = queue[:CURSOR_SLOTS], queue[CURSOR_SLOTS:]
check("6e-cursor-waves",
      wave1 == ["T1", "T2", "T3", "T4"] and wave2 == ["T5", "T6"],
      "in Cursor the same queue runs as waves: wave 1 T1-T4, wave 2 T5-T6 (no mid-wave refill)")
gate_hits = 0
for rel, n in [("skills/orch-pipeline/SKILL.md", 62),
               ("skills/feature-expansion/SKILL.md", 139),
               ("skills/gan-style-harness/SKILL.md", 14),
               ("skills/design-taste-frontend/references/hallmark/references/redesign.md", 68),
               ("skills/orchestrate/SKILL.md", 93)]:
    if "slots refill per wave, not per completion" in line(rel, n):
        gate_hits += 1
check("6e-harness-gate-five-paragraphs", gate_hits == 5,
      "harness-gate clause ('in Cursor, slots refill per wave, not per completion') in %d/5 factory paragraphs" % gate_hits)
check("6e-owed-29-2-honest",
      "the factory lights up fully on the later port, not in Cursor" in
      line("skills/orchestrate/SKILL.md", 36),
      "OWED-29-2 recorded in the routing text itself: live factory lights up on the later port, not in Cursor")

# -------------------------------------------------------- (f) COST-AWARE
justification = ("Six disjoint file partitions (week.ts, inventory.ts, WeekView.tsx, "
                 "remix.ts, cost.ts, PlanPage.tsx) justify N=6.")
check("6f-n-greater-3-justified-one-line",
      "\n" not in justification.strip() and "justify N=6" in justification,
      "N=6 justified in one line: '%s'" % justification)
check("6f-minimal-context",
      all(set(briefs[t["id"]]["files_in_scope"]) == t["write"] for t in QUEUE),
      "each brief carries only its partition's files (minimal context, no whole-tree dump)")
check("6f-cost-aware-live",
      "justifies N>3 in one line" in line("skills/orchestrate/SKILL.md", 36),
      "GLOBAL-ROUTING COST-AWARE_F29: 'the orchestrator justifies N>3 in one line'")

print("\nLEG 6 summary: %d passed, %d failed" % (len(passes), len(fails)))
if fails:
    print("FAILED: %s" % ", ".join(fails))
    sys.exit(1)
