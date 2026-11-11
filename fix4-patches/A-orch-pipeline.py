# --- Fix program #4, Batch A: orch-pipeline — one-engine rule + Phase 4
# implementer belief + numbering disambiguation ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST in build.sh, just before STEP 5, after the GATE /
# carve-out / Batch E / Batch F / Fix-program-#3 Batch A patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/orch-pipeline/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. The patch agent inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # DD1 — one build engine per run: orch-build-mvp is the STANDALONE
  # pipeline delegating to this engine; orchestrate is the first-build
  # engine and never invokes orch-build-mvp (so never reaches this engine
  # through it) in the same run.
  ("skills/orch-pipeline/SKILL.md", r'''The `orch-*` skills are thin wrappers. They do not re-implement any work — they
classify the request, choose which phases of *this* pipeline run, and delegate
each phase to an existing ECC agent or command. This file is that pipeline.''', r'''The `orch-*` skills are thin wrappers. They do not re-implement any work — they
classify the request, choose which phases of *this* pipeline run, and delegate
each phase to an existing ECC agent or command. This file is that pipeline.

**One build engine per run:** `orch-build-mvp` is the STANDALONE pipeline that delegates to this engine — it runs only when the user invokes `/orch-build-mvp` directly. Orchestrate IS the first-build engine and never invokes `orch-build-mvp` (and so never reaches this engine through it) in the same run. One engine per run, never both.'''),
  # Operation family: orch-build-mvp is standalone; record/scope is the
  # default input, the spec doc only the fallback.
  ("skills/orch-pipeline/SKILL.md", r'''| `orch-build-mvp` | mvp | bootstrap from a design/spec doc | ingest doc → vertical slices |''', r'''| `orch-build-mvp` | mvp | bootstrap from a design/spec doc (standalone only — user-invoked) | ingest record/scope by default (spec doc only as standalone fallback) → vertical slices |'''),
  # Phase 0 (Intake): numbering disambiguation — orch-pipeline Phases 0–6
  # are not orch-build-mvp steps and not feature-expansion phases.
  ("skills/orch-pipeline/SKILL.md", r'''The pipeline ingests the record/scope at Phase 0; they are the handoff from grill-me and hackathon-scope.''', r'''The pipeline ingests the record/scope at Phase 0; they are the handoff from grill-me and hackathon-scope. Numbering: Phases 0–6 here are orch-pipeline phases — not orch-build-mvp steps (which map 1:1 onto them: orch-build-mvp steps 1/3/4/6/7 are Phases 0–2/3/4/5/6) and not feature-expansion phases.'''),
  # Phase 4 (Implement): DD8 belief in the brief + expansion Phase 4
  # brief format in a standalone orch-build-mvp run.
  ("skills/orch-pipeline/SKILL.md", r'''- **4. Implement (TDD)** — drive each task through the `tdd-guide` agent (or the `tdd-workflow` skill):
  red → green → refactor. Honor the operation's first-move rule.''', r'''- **4. Implement (TDD)** — drive each task through the `tdd-guide` agent (or the `tdd-workflow` skill):
  red → green → refactor. Honor the operation's first-move rule. **Belief in the brief:** implementers trust the brief and build it — they do not second-guess the plan, hedge, or wait for reassurance; they commit to the approach and make it work; if a detail is ambiguous, they pick the reasonable option and note it, they don't stall. In a standalone `orch-build-mvp` run, this phase builds the approved expansions per the feature-expansion Phase 4 brief format (Tool/API cell + UI rule + capped 2-round fix loop + per-feature `code-reviewer` pass).'''),
  # Phase 6 (Commit): numbering disambiguation — orch-pipeline Phase 6 is
  # not orch-build-mvp step 6 (Verify) and not expansion Phase 6.
  ("skills/orch-pipeline/SKILL.md", r'''- **6. Commit** — conventional commits (`feat:` / `fix:` / `refactor:` / …), one
  per logical chunk. → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature).''', r'''- **6. Commit** — conventional commits (`feat:` / `fix:` / `refactor:` / …), one
  per logical chunk. → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature). (Orch-pipeline Phase 6 = Commit — not orch-build-mvp step 6, which is Verify, and not feature-expansion Phase 6, which feeds the final report; orch-build-mvp step 5 is Reconcile, which has no orch-pipeline phase of its own.)'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix4 batch A: orch-pipeline one-engine + Phase 4 belief + numbering applied")
PYEOF
