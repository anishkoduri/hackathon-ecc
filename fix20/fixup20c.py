#!/usr/bin/env python3
"""Fix-up #20c (Nov 12, 2026) — steers #3/#4/#5 + sweep #27 leftovers.

Applies after audit #64 (ZERO ERRORS), dry-run #33 (13/13 PASS), and
sweep #27 (NOT CLEAN — 1 finding + observations). See SPEC.md section 12.

 1. Sweep #27 FINDING 1: build.sh:23475 still cites "hackathon-mode
    section 37" inside the embedded weave20 block (weave20.py was fixed,
    the inserted copy was not). One-line comment fix in build.sh.
 2. MINOR-3 re-opened: the false "placed LAST — just before STEP 5"
    claim persists in ~60 more build.sh block headers (fix #4-era
    boilerplate). All placement-"LAST" phrases are normalized (64
    replacements, line count unchanged — validated on a /tmp copy first);
    only the two TRUE "runs LAST (after every audit_patch …" lines
    remain. The fix #20 program's own generator strings are updated to
    match the normalized embedded copies (weave20.py BLOCK header,
    fix20.py / fixup20.py / fixup20b.py block headers); docstrings
    describing the historical action are left as-is. fix15/17/18/19
    generators are left historical (one-shot, not regenerated).
 3. fixup20b.py re-import fix: import the amended F5/F5_APP texts as
    the NEW values and derive the OLD values by reversing the
    substitution (the fixup20.py reversal pattern). Import succeeds
    after this; a re-RUN is still refused by preflight (one-shot).
 4. H1 model hierarchy (steer #3.2): Grok 4.7 High decides, Grok 4.6
    High executes — full text in orchestrate (before "## Setup") and
    hackathon-mode §6, plus a pointer in the design-package rule.
 5. OVERDRIVE expansion (steer #3.3): 5–9 candidates per lens, 7–12
    shortlisted features (~1.75x) — full rule in feature-expansion
    (before Phase 0), Phase 1 + Phase 2 volume lines updated, pointers
    in orchestrate step 2 and hackathon-mode §1. Anti-drift bound
    explicit; 7–12 is a cap, not a quota; overflow to docs/expansion.md.
 6. BIND + INNOV (steers #4 + #5): binding routing (the skills are the
    only path; the audit/dry-run FAIL off-skill work) and on-skill
    innovation (creativity BASED OFF the skills; the audit/dry-run do
    NOT fail it; channels the fix #17 E1 push). Full texts in
    orchestrate and hackathon-mode §6; pointers in the design-package
    rule and in the built orch-build-mvp / orch-pipeline files.

Scope: no F-rule constant changes (fix20.py untouched), no Grok-pin
changes, no new skills/agents/rules/commands, no canonical-block
change. The 32 woven pointers are NOT re-edited: they invoke the
design-package rule, which now carries the BIND/INNOV + H1 pointers
(SPEC section 12.4). Every substitution asserts count==1 (comment
subs assert their probed per-phrase counts).
"""
import hashlib
import os
import shutil
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
FEAT = os.path.join(PLUGIN, "new-skills/feature-expansion/SKILL.md")
HKM = os.path.join(PLUGIN, "new-rules/hackathon-mode.mdc")
FIX20_PY = os.path.join(PLUGIN, "fix20/fix20.py")
FIXUP20_PY = os.path.join(PLUGIN, "fix20/fixup20.py")
FIXUP20B_PY = os.path.join(PLUGIN, "fix20/fixup20b.py")
WEAVE20_PY = os.path.join(PLUGIN, "fix20/weave20.py")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]

# --- the new rules (verify20.py imports these constants) --------------------
H1_RULE = """**Model hierarchy — Grok 4.7 High decides, Grok 4.6 High executes (fix #20 H1).** Grok 4.7 High (`grok-4.7-high`) is the ORCHESTRATOR and the main mind behind big decisions: the orchestrator, the design-lead, the deep-reasoner, and every big-decision role run on Grok 4.7 High. Grok 4.6 High (`cursor-grok-4.6-high-fast`) are the underlings — fast execution workers: scout, fast-worker, and the other composer-tier agents execute fully-specified work and never decide. A 4.6 worker that faces a decision routes it up to the 4.7 mind (orchestrator / deep-reasoner / design-lead); it never decides on its own. A dispatch that puts a big decision on a 4.6 model, or execution a 4.6 worker could do on a 4.7 model, is a routing error — a static check item, never a screen verdict."""

BIND_RULE = """**Binding routing — the skills are the only path (fix #20 BIND).** Every decision routes through a NAMED skill: the operating skill for the work is named in the brief before the work starts, and the work is done by that skill's rules. A decision with no named operating skill is not a decision — it is refused and routed to the skill that owns it; where NO skill owns it, the recorded-gap fallback below applies. Work produced without a named skill in its brief is an incomplete build — a static check item, never a screen verdict — unless it is a recorded-gap fallback (below). Grok executes THROUGH the package, never replaces it (fix #13: every design decision is made BY a named package skill): no freelance work, no off-skill improvisation. The audit and the dry-run FAIL any decision or work done outside a named skill where a skill exists and was bypassed — that is off-skill improvisation. **Recorded-gap fallback (fix #20):** binding never blocks needed work. When a needed step has no skill covering it, the agent does NOT stop: it records the gap in the decision record (what was needed, why no skill covers it), does the work by the closest skill's principles (building off the skills), and flags it so the gap can become a skill later. A needed step done through the recorded-gap fallback PASSES the audit/dry-run — it is not off-skill improvisation. Priority order: (1) everything needed gets done, (2) on the skills wherever a skill exists, (3) through the recorded-gap fallback where none does."""

INNOV_RULE = """**Innovation builds on the skills (fix #20 INNOV).** Binding routing does not kill creativity: agents stay creative and innovative — but BASED OFF the skills. An original element or approach that extends, combines, or pushes a skill's principles is on-skill innovation: it PASSES, recorded with its fix #19 D19 reason (what skill principle it builds on, why the extension serves the surface). Innovation extends, combines, and pushes the skills; it never bypasses them. This channels the fix #17 E1 creativity push (trailblazing, not dumb) through the skills rather than suppressing it. The audit and the dry-run FAIL off-skill improvisation but do NOT fail on-skill innovation."""

OVERDRIVE_RULE = """**OVERDRIVE expansion (fix #20).** Expansion runs in OVERDRIVE: about 75% more features/tools surfaced per build (~1.75x the old volume) — each brainstorm lens returns 5–9 candidates (was 3–5), the shortlist keeps 7–12 features (was 4–7). The anti-drift bound stays and is explicit: expansion stays anchored to the original idea and the grill-me decision record (Phase 0 grounding pastes them inline); expansion PROPOSES, the planner APPROVES / TWEAKS / REJECTS (Phase 3) — a feature that contradicts a recorded decision is rejected, never tweaked around it; a feature that does not fit the one coherent product story is tweaked or rejected; nothing that drifts from the OG idea gets built. 7–12 is a CAP, not a quota — never pad to reach it; fewer exceptional features still beat many mediocre ones. With 7–12 features the proposal table usually exceeds the 20-line ledger — that is expected; the full table goes in `docs/expansion.md` and the ledger carries a one-line pointer (the existing overflow rule); never cut features to fit the ledger."""

# --- short pointers -----------------------------------------------------------
H1_PTR = (" **Model hierarchy (fix #20 H1):** the design-lead decides on Grok 4.7 High; "
          "executors implement on Grok 4.6 High — no big decision runs on a 4.6 worker, "
          "no execution a 4.6 worker could do runs on the 4.7 mind.")
BIND_PTR = (" **Binding (fix #20 BIND/INNOV):** this rule's skill set IS the named operating "
            "skill for the slice — a UI decision made outside it is refused and routed here; "
            "an original element built on these skills' principles is on-skill innovation "
            "and passes with its D19 reason.")
MVP_BIND = (" **Binding routing (fix #20 BIND/INNOV):** every slice brief names its operating "
            "skill before work starts (this rule names the design components); a decision with "
            "no named skill is refused and routed; on-skill innovation — an original element "
            "built on these skills' principles, recorded with its D19 reason — passes, "
            "off-skill improvisation fails.")
PIPE_BIND = (" **Binding routing (fix #20 BIND/INNOV):** each phase names its operating skill "
             "before delegating; a decision with no named skill is refused and routed; on-skill "
             "innovation passes with its D19 reason, off-skill improvisation fails.")
ORCH_OD_PTR = (" **OVERDRIVE (fix #20):** 7–12 shortlisted features, about 75% more than the old "
               "4–7 (~1.75x) — anchored to the original idea + decision record, planner-approved, "
               "anti-drift bound explicit; 7–12 is a cap, not a quota.")
FEAT_P1_NEW = ("Each returns 5–9 candidates, no more — a long list is a sign nobody prioritized. "
               "**OVERDRIVE (fix #20):** about 75% more candidates per lens than the old 3–5 (~1.75x) "
               "— the brainstorm runs wider, still anchored to the original idea and the grill-me "
               "decision record.")
FEAT_P2_NEW = ("Keep it to 7–12 features (fix #20 OVERDRIVE — about 75% more than the old 4–7, "
               "~1.75x). More than that means nothing was prioritized. 7–12 is a CAP, not a quota — "
               "never pad to reach it; fewer exceptional features still beat many mediocre ones. "
               "With 7–12 features the proposal table usually exceeds the 20-line ledger — that is "
               "expected: the full table goes in `docs/expansion.md` (the existing overflow rule) "
               "and the ledger carries a one-line pointer; never cut features to fit the ledger.")

# --- staged-source subs: (path, old, new, marker) ---------------------------
# marker: a short distinctive string of the NEW text; must be absent before
# applying and present exactly once after (insertions carry the anchor in
# `new`, so the plain "new not in text" check does not apply to them).
ORCH_BLOCK = H1_RULE + "\n\n" + BIND_RULE + "\n\n" + INNOV_RULE
STAGED_SUBS = [
    # orchestrate: H1/BIND/INNOV block before "## Setup" (after the team table).
    (ORCH, "## Setup (one-time)",
     ORCH_BLOCK + "\n\n## Setup (one-time)",
     "Model hierarchy — Grok 4.7 High decides, Grok 4.6 High executes"),
    # orchestrate: H1 + BIND pointers in the design-package rule paragraph.
    (ORCH,
     "Small changes, one-prompt changes, redesigns, UI fixes, and removal flows that rebuild a surface are UI slices under this rule — they record the direction in the decision record / run ledger (the lightest-weight record that exists for that flow) and run the applicable package components. No UI slice builds on an unstated direction.",
     "Small changes, one-prompt changes, redesigns, UI fixes, and removal flows that rebuild a surface are UI slices under this rule — they record the direction in the decision record / run ledger (the lightest-weight record that exists for that flow) and run the applicable package components. No UI slice builds on an unstated direction." + H1_PTR + BIND_PTR,
     "Model hierarchy (fix #20 H1):"),
    # orchestrate step 2: OVERDRIVE pointer.
    (ORCH,
     "produce the planner-approved list of features and tools, in line with the decision record, with no user approval gate.",
     "produce the planner-approved list of features and tools, in line with the decision record, with no user approval gate." + ORCH_OD_PTR,
     "OVERDRIVE (fix #20):** 7–12 shortlisted features"),
    # feature-expansion: full OVERDRIVE rule before Phase 0.
    (FEAT, "### Phase 0 — Ground in what exists (5 minutes, main agent)",
     OVERDRIVE_RULE + "\n\n### Phase 0 — Ground in what exists (5 minutes, main agent)",
     "**OVERDRIVE expansion (fix #20).**"),
    # feature-expansion Phase 1: 3–5 -> 5–9 candidates.
    (FEAT,
     "Each returns 3–5 candidates, no more — a long list is a sign nobody prioritized.",
     FEAT_P1_NEW,
     "Each returns 5–9 candidates, no more"),
    # feature-expansion Phase 2: 4–7 -> 7–12 features.
    (FEAT,
     "Keep it to 4–7 features. More than that means nothing was prioritized.",
     FEAT_P2_NEW,
     "Keep it to 7–12 features (fix #20 OVERDRIVE"),
    # hackathon-mode §6: H1/BIND/INNOV bullets after the section heading.
    (HKM,
     "## 6. Skill routing — when two skills could apply\n\n- `grill-me` owns the first project prompt.",
     "## 6. Skill routing — when two skills could apply\n\n- " + H1_RULE + "\n- " + BIND_RULE + "\n- " + INNOV_RULE + "\n- `grill-me` owns the first project prompt.",
     "Model hierarchy — Grok 4.7 High decides, Grok 4.6 High executes"),
    # hackathon-mode §1: OVERDRIVE pointer next to the expansion sentence.
    (HKM,
     "producing the planner-approved list;",
     "producing the planner-approved list (fix #20 OVERDRIVE: the shortlist keeps 7–12 features, about 75% more than the old 4–7 — a cap, not a quota, anchored to the original idea and the decision record, planner-approved, anti-drift bound explicit);",
     "fix #20 OVERDRIVE: the shortlist keeps 7–12 features"),
]

# --- generator-string subs: (path, old, new) — emitted build.sh headers -------
GEN_SUBS = [
    (WEAVE20_PY,
     "# build — this block runs LAST, just before STEP 5, after the fix20 block.",
     "# build — this block runs before STEP 5, after the fix20 block."),
    (FIXUP20_PY,
     "#  upstream halves are patched here. Placement: LAST, just before STEP 5",
     "#  upstream halves are patched here. Placement: before STEP 5"),
    (FIX20_PY,
     "# Placement: LAST, just before STEP 5 (after the fix19 block).",
     "# Placement: before STEP 5 (after the fix19 block)."),
    (FIXUP20B_PY,
     "#  upstream halves are patched here. Placement: LAST, just before STEP 5",
     "#  upstream halves are patched here. Placement: before STEP 5"),
]

# --- fixup20b.py re-import fix: (path, old, new) -------------------------------
FIXUP20B_IMPORT_SUBS = [
    (FIXUP20B_PY,
     "from fix20 import F5, F5_APP  # noqa: E402 — fix20.py holds the fixup20-amended texts",
     "from fix20 import F5 as F5_NEW2, F5_APP as F5_APP_NEW2  # noqa: E402 — fix20.py holds the fixup20b-amended texts"),
    (FIXUP20B_PY,
     "F5_NEW2 = F5.replace(_F5_EX_OLD, _F5_EX_NEW, 1)\n"
     "assert F5_NEW2 != F5 and _F5_EX_OLD not in F5_NEW2",
     "F5 = F5_NEW2.replace(_F5_EX_NEW, _F5_EX_OLD, 1)\n"
     "assert F5 != F5_NEW2 and _F5_EX_OLD in F5  # reversed: fix20.py now holds the amended text"),
    (FIXUP20B_PY,
     "F5_APP_NEW2 = F5_APP.replace(_F5A_EX_OLD, _F5A_EX_NEW, 1)\n"
     "assert F5_APP_NEW2 != F5_APP and _F5A_EX_OLD not in F5_APP_NEW2",
     "F5_APP = F5_APP_NEW2.replace(_F5A_EX_NEW, _F5A_EX_OLD, 1)\n"
     "assert F5_APP != F5_APP_NEW2 and _F5A_EX_OLD in F5_APP  # reversed: fix20.py now holds the amended text"),
]

# --- build.sh comment subs: (old, new, expected-count) — replace-all ----------
# Counts probed on a /tmp copy of build.sh (23,582 lines) before writing this
# engine; total 64 replacements, line count unchanged.
BUILD_SH_COMMENT_SUBS = [
    ("placed LAST — just before STEP 5", "placed — just before STEP 5", 15),
    ("placed LAST in build.sh, just before STEP 5", "placed in build.sh, before STEP 5", 16),
    ("Placement: LAST, just before STEP 5", "Placement: before STEP 5", 14),
    ("Placement: LAST, after the Batch F block, just before STEP 5.",
     "Placement: after the Batch F block, before STEP 5.", 5),
    ("runs LAST, just before STEP 5", "runs before STEP 5", 3),
    ("patch block placed LAST, just before STEP 5", "patch block placed before STEP 5", 1),
    ("this block runs LAST,\n# just before STEP 5, AFTER the weave1 block",
     "this block runs\n# just before STEP 5, AFTER the weave1 block", 1),
    ("Placement: LAST, just\n#  before STEP 5 (after the fix13-A/B blocks).",
     "Placement: before STEP 5\n#  (after the fix13-A/B blocks).", 1),
    ("hackathon-mode section 37", "hackathon-mode section 5", 1),
    ("placed LAST — just before\n# STEP 5", "placed — just before\n# STEP 5", 2),
    ("placed LAST — just\n# before STEP 5", "placed — just\n# before STEP 5", 1),
    ("placed LAST —\n# just before STEP 5", "placed —\n# just before STEP 5", 1),
    ("placed LAST in build.sh, just\n# before STEP 5",
     "placed in build.sh, just\n# before STEP 5", 1),
    ("Placement:\n#  LAST, just before STEP 5 (after the fix13c block).",
     "Placement:\n#  before STEP 5 (after the fix13c block).", 1),
    ("Patch blocks run LAST, just before STEP 5", "Patch blocks run before STEP 5", 1),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, new) -----------
_MVP_TAIL = "its Design Quality / Originality rows defer to browser-qa (see `gan-style-harness`)."
_PIPE_ANCHOR = "Each phase delegates — it does not do the work inline."
BUILD_SUBS = [
    ("skills/orch-build-mvp/SKILL.md", _MVP_TAIL, _MVP_TAIL + MVP_BIND),
    ("skills/orch-pipeline/SKILL.md", _PIPE_ANCHOR, _PIPE_ANCHOR + PIPE_BIND),
]


def build_sh_block():
    """The fixup20c patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fixup20c: H1 hierarchy + BIND/INNOV binding + OVERDRIVE pointers ---")
    lines.append("# (steers #3/#4/#5 follow-up to fix #20, Nov 12. Built-file pointers in")
    lines.append("#  orch-build-mvp / orch-pipeline; staged halves are edited by")
    lines.append("#  fix20/fixup20c.py. Placement: before STEP 5 (after the fix20, weave20,")
    lines.append("#  fixup20, and fixup20b blocks). Each substitution asserts exactly one")
    lines.append("#  match in the BUILT file and fails the build loudly.)")
    lines.append("""python3 - "$PLUGIN_DIR" <<'PYEOF'""")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for rel, old, new in BUILD_SUBS:
        lines.append("  (%s," % repr(rel))
        lines.append("   %s," % repr(old))
        lines.append("   %s)," % repr(new))
    lines.append("]")
    lines.append("for rel, old, new in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("""    assert n == 1, f'fixup20c anchor not found exactly once in {rel}: {old[:70]!r} (count={n})'""")
    lines.append("""    open(p, "w").write(t.replace(old, new))""")
    lines.append("""print("fixup20c upstream block applied")""")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def _once(text, anchor, where):
    n = text.count(anchor)
    assert n == 1, f"anchor count={n} in {where}: {anchor[:70]!r}"
    return n


def preflight():
    """Check every anchor count==1 before writing anything."""
    btext = open(BUILD_SH, encoding="utf-8").read()
    lines = btext.splitlines()
    md5 = hashlib.md5(btext.encode("utf-8")).hexdigest()
    assert (len(lines), md5) == (23582, "766a35e47e83f921b4e30e8b4da36efd"), \
        f"PREFLIGHT build.sh is {len(lines)} lines md5 {md5}, expected 23582 / 766a35e4… (post-fixup20b)"
    for path, old, _new, marker in STAGED_SUBS:
        _once(open(path, encoding="utf-8").read(), old, path)
        assert marker not in open(path, encoding="utf-8").read(), \
            f"PREFLIGHT {path}: marker already present: {marker[:50]!r}"
    for path, old, _new in GEN_SUBS + FIXUP20B_IMPORT_SUBS:
        text = open(path, encoding="utf-8").read()
        _once(text, old, path)
        assert _new not in text, f"PREFLIGHT {path}: amended text already present"
    for old, _new, n in BUILD_SH_COMMENT_SUBS:
        assert btext.count(old) == n, \
            f"PREFLIGHT build.sh: comment phrase count={btext.count(old)}, expected {n}: {old[:60]!r}"
    for rel, old, _new in BUILD_SUBS:
        _once(open(os.path.join(BUILT, rel), encoding="utf-8").read(), old,
              f"built {rel}")
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fixup20c upstream block applied" not in btext, \
        "PREFLIGHT build.sh: fixup20c block already present"
    assert "fixup20b upstream block applied" in btext, \
        "PREFLIGHT build.sh: fixup20b block marker missing"
    blobs = [new for _, _, new, _ in STAGED_SUBS]
    blobs += [new for _, _, new in GEN_SUBS + FIXUP20B_IMPORT_SUBS]
    blobs += [new for _, new, _ in BUILD_SH_COMMENT_SUBS]
    blobs += [new for _, _, new in BUILD_SUBS]
    blobs.append(build_sh_block())
    for blob in blobs:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fixup20c addition"
    print("preflight OK: staged + gen + import subs, %d comment subs, %d build subs, banned-term scan clean"
          % (len(BUILD_SH_COMMENT_SUBS), len(BUILD_SUBS)))


def apply_subs(subs):
    grouped = {}
    for item in subs:
        path, old, new = item[0], item[1], item[2]
        grouped.setdefault(path, []).append((old, new))
    for path, pairs in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old, new in pairs:
            assert text.count(old) == 1, f"APPLY {path}: anchor count!=1"
            text = text.replace(old, new, 1)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(pairs)} substitution(s) applied")


def apply_comment_subs():
    text = open(BUILD_SH, encoding="utf-8").read()
    total = 0
    for old, new, n in BUILD_SH_COMMENT_SUBS:
        assert text.count(old) == n, f"APPLY build.sh: comment phrase count!= {n}"
        text = text.replace(old, new)
        total += n
    open(BUILD_SH, "w", encoding="utf-8").write(text)
    print(f"build.sh: {total} comment replacements applied")
    return total


def self_checks():
    """After the edits: every new text present, old texts gone, hygiene holds."""
    for path, old, new, marker in STAGED_SUBS:
        text = open(path, encoding="utf-8").read()
        assert text.count(marker) == 1, f"SELF-CHECK {path}: marker missing: {marker[:50]!r}"
        assert new in text, f"SELF-CHECK {path}: amended text missing"
    for path, old, new in GEN_SUBS + FIXUP20B_IMPORT_SUBS:
        text = open(path, encoding="utf-8").read()
        assert new in text, f"SELF-CHECK {path}: amended text missing"
        assert old not in text, f"SELF-CHECK {path}: old text still present"
    # OLD volume lines gone from feature-expansion.
    ftext = open(FEAT, encoding="utf-8").read()
    assert "Each returns 3–5 candidates" not in ftext, "SELF-CHECK feature-expansion: old 3–5 line survives"
    assert "Keep it to 4–7 features" not in ftext, "SELF-CHECK feature-expansion: old 4–7 line survives"
    assert "a feature that contradicts a recorded decision is rejected" in ftext, \
        "SELF-CHECK feature-expansion: anti-drift guard damaged"
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "hackathon-mode section 37" not in btext, "SELF-CHECK build.sh: section 37 survives"
    last_lines = [ln for ln in btext.split("\n") if "LAST" in ln]
    assert len(last_lines) == 2 and all("runs LAST (after every" in ln for ln in last_lines), \
        f"SELF-CHECK build.sh: unexpected LAST lines remain: {last_lines!r}"
    assert "fixup20c upstream block applied" in btext, "SELF-CHECK build.sh: fixup20c block missing"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    assert btext.find("fixup20c upstream block applied") > btext.find("fixup20b upstream block applied"), \
        "SELF-CHECK build.sh: fixup20c block must sit after the fixup20b block"
    # fixup20b.py must import again now.
    import subprocess
    r = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, 'fix20'); import fixup20b; print('fixup20b imports OK')"],
                       cwd=PLUGIN, capture_output=True, text=True)
    assert r.returncode == 0, f"SELF-CHECK fixup20b import still fails: {r.stderr[-400:]}"
    print("self-checks OK: all fixup20c amendments present; build.sh hygiene holds; fixup20b imports")
    print(r.stdout.strip())


def main():
    preflight()
    shutil.copy2(BUILD_SH, BUILD_SH + ".before-fixup20c")
    apply_subs(STAGED_SUBS)
    apply_subs(GEN_SUBS)
    apply_subs(FIXUP20B_IMPORT_SUBS)
    apply_comment_subs()
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1
    block = build_sh_block()
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print("build.sh: fixup20c block appended (%d upstream subs, before STEP 5)"
          % len(BUILD_SUBS))
    self_checks()


if __name__ == "__main__":
    main()
