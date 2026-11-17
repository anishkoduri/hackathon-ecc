#!/usr/bin/env python3
"""Fix #30 — model routing pin change: Grok 4.7 High -> Grok 4.7 Extra High
(orchestrator pin only).

Run by build.sh as a patch step (after fix29.py, before STEP 5 Counts):
    python3 "$PLUGIN_ROOT/fix30/fix30.py" "$PLUGIN_DIR"

Operates on the BUILT tree only. Replaces the orchestrator pin
grok-4.7-high -> grok-4.7-extra-high and the prose "Grok 4.7 High" ->
"Grok 4.7 Extra High" everywhere in the built tree, then asserts the
result exactly. Exits non-zero on any error so the build fails rather
than shipping a half-renamed tree.

SPEC fix30/SPEC.md (re-scoped Nov 16, 2026): the brain is Grok 4.7 on
Extra High in Cursor, on the pool. Scope: the pin change + the
verifier's pin assertions (verify30.py). No other behavior changes: no
#28 debloat change, no design-package change, no grill-me change, no
alwaysApply change, no drone routing added — the full drone factory
(custom subagents, CLI dispatch, OpenRouter setup skill) lives in the
separate factory copy per FACTORY_CURSOR_PLAN.md.

WHY BUILD-TIME ONLY (staged sources + build.sh inline NOT changed):
fix16.py, fix24.py and fix29.py all anchor on text containing
grok-4.7-high and abort the build on anchor mismatch (fix16's
common-performance sentence else-branch ERRORS if neither the old nor
the new sentence is found; fix24's _DESIGN_LEAD_OLD anchor; fix29's
line-424 OLD anchor). Renaming the pin in staged sources or in
build.sh's inline content would break those anchors. Precedent: fix
#16 itself performed the Claude -> Grok pin change at build time via
fix16.py, with staged/upstream sources keeping the old text. So
fix30.py performs the rename on the built tree, last in build order
(after fix29.py, before STEP 5 Counts — nothing after this point
writes pin text; STEP 5 Counts only echoes counts), and the resulting
staged-vs-built pin drift is BY DESIGN — recorded as OWED-30-1
(staged: 19 new-skills + 2 new-rules ID occurrences, plus 15 staged
prose occurrences; build.sh inline: 54 pre-existing ID occurrences on
50 lines, plus 5 prose occurrences — all keep the old pin). Same class
as OWED-29-5's 41 lines.

Census (measured Nov 16, 2026 on the fix29 built tree; asserted exactly
— any drift fails loudly and no file is written):
  grok-4.7-high             x49  (48 in .md/.mdc + 1 in schemas/agent.schema.json:36 enum)
  "Grok 4.7 High"           x22  (prose; 11 lines, some carrying 2)
  cursor-grok-4.6-high-fast x70  (unchanged — the fast-worker pin is NOT touched)
  bare grok-4.6-high-fast   x0
  grok-4.7-extra-high       x0   (pre-rename)
  "Grok 4.7 Extra High"     x0   (pre-rename)

Prose judgment (recorded as OWED-30-5): all 22 prose occurrences
change, including skills/strategic-compact/SKILL.md:68 (the "500k Grok
4.7 High" context-window example) and :102 (the Cursor 2.1.233
todo-tools note) — the note's operative claim (todo tools absent on
the plugin's models) is preserved by its "and newer" clause. The other
20 are direct references to the orchestrator tier.

Anchor tokens: none new. The GLOBAL-ROUTING block (fix #29) is
re-asserted byte-identical in orchestrate + hackathon-mode as a
regression guard — it carries no pin and the rename must not touch it.
"""
import os
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []

OLD_ID = "grok-4.7-high"
NEW_ID = "grok-4.7-extra-high"
OLD_PROSE = "Grok 4.7 High"
NEW_PROSE = "Grok 4.7 Extra High"
FAST_ID = "cursor-grok-4.6-high-fast"
FAST_BARE = "grok-4.6-high-fast"

# Exact pre-rename census (see docstring). Any drift fails loudly.
EXPECT = {
    OLD_ID: 49,
    OLD_PROSE: 22,
    FAST_ID: 70,
    NEW_ID: 0,
    NEW_PROSE: 0,
}

SKIP_DIRS = {"node_modules", ".git"}


def p(rel):
    return os.path.join(BASE, rel)


def exists(f):
    return os.path.exists(f)


def _walk_files():
    """All files under BASE except SKIP_DIRS, as (path, text-or-None).

    A file that is not valid UTF-8 is returned with text=None; the
    caller byte-checks it for pin text instead of silently skipping it
    (a pin hiding in a binary file must fail loudly, not pass the
    census by being unreadable).
    """
    for _root, _dirs, _files in os.walk(BASE):
        _dirs[:] = [d for d in _dirs if d not in SKIP_DIRS]
        for _name in sorted(_files):
            _path = os.path.join(_root, _name)
            try:
                with open(_path, encoding="utf-8") as _fh:
                    yield _path, _fh.read()
            except (UnicodeDecodeError, OSError):
                yield _path, None


def _count_in(text):
    return {
        OLD_ID: text.count(OLD_ID),
        OLD_PROSE: text.count(OLD_PROSE),
        FAST_ID: text.count(FAST_ID),
        NEW_ID: text.count(NEW_ID),
        NEW_PROSE: text.count(NEW_PROSE),
    }


def _bare_fast_count(text):
    """Occurrences of grok-4.6-high-fast NOT preceded by 'cursor-'."""
    _n = 0
    _i = 0
    while True:
        _i = text.find(FAST_BARE, _i)
        if _i < 0:
            return _n
        if not text[max(0, _i - 7):_i].endswith("cursor-"):
            _n += 1
        _i += len(FAST_BARE)


# ---------------------------------------------------------------- 1. Census (pre-rename, no writes)
_totals = {k: 0 for k in EXPECT}
_totals["bare_fast"] = 0
_binary_skipped = []
for _path, _text in _walk_files():
    if _text is None:
        _raw = open(_path, "rb").read()
        for _needle in (OLD_ID, OLD_PROSE, NEW_ID, NEW_PROSE, FAST_ID):
            if _needle.encode("utf-8") in _raw:
                ERRORS.append(
                    f"census: pin text {_needle!r} found in non-UTF-8 file "
                    f"{os.path.relpath(_path, BASE)} — refusing to guess")
        _binary_skipped.append(os.path.relpath(_path, BASE))
        continue
    _c = _count_in(_text)
    for _k in _totals:
        if _k in _c:
            _totals[_k] += _c[_k]
    _totals["bare_fast"] += _bare_fast_count(_text)
for _k, _want in EXPECT.items():
    if _totals[_k] != _want:
        ERRORS.append(
            f"census: {_k} found {_totals[_k]}x, expected {_want}x — "
            f"tree drifted from the fix29 census; refusing to rename")
if _totals["bare_fast"] != 0:
    ERRORS.append(
        f"census: bare {FAST_BARE} found {_totals['bare_fast']}x, expected 0x")
CHANGES.append(
    f"census: {OLD_ID} x{_totals[OLD_ID]}, {OLD_PROSE!r} x{_totals[OLD_PROSE]}, "
    f"{FAST_ID} x{_totals[FAST_ID]}, bare {FAST_BARE} x{_totals['bare_fast']}, "
    f"{NEW_ID} x{_totals[NEW_ID]}, {NEW_PROSE!r} x{_totals[NEW_PROSE]}, "
    f"{len(_binary_skipped)} non-UTF-8 file(s) skipped (byte-checked, no pin text)")
if ERRORS:
    # Fail before writing anything.
    _log_lines = ["# fix30 run log", "",
                  f"## Errors ({len(ERRORS)})"]
    _log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
    _log_lines += ["", "## Changes (0)", "- none", "",
                   "## Command decisions (0)", "- none", "",
                   "## OWED (0)", "- none"]
    _log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix30")
    os.makedirs(_log_dir, exist_ok=True)
    with open(os.path.join(_log_dir, "fix30-patch-log.md"), "w",
              encoding="utf-8") as _fh:
        _fh.write("\n".join(_log_lines) + "\n")
    print(f"fix30: {len(ERRORS)} ERROR(S) in census — no files written",
          file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------- 2. Rename (ID first, then prose)
for _path, _text in _walk_files():
    if _text is None:
        continue
    _n_id = _text.count(OLD_ID)
    _n_prose = _text.count(OLD_PROSE)
    if _n_id == 0 and _n_prose == 0:
        continue
    _new = _text.replace(OLD_ID, NEW_ID).replace(OLD_PROSE, NEW_PROSE)
    with open(_path, "w", encoding="utf-8") as _fh:
        _fh.write(_new)
    CHANGES.append(
        f"{os.path.relpath(_path, BASE)}: pin renamed "
        f"({OLD_ID} x{_n_id}, {OLD_PROSE!r} x{_n_prose})")

# ---------------------------------------------------------------- 3. Post-assertions (re-census the renamed tree)
_post = {k: 0 for k in EXPECT}
_post["bare_fast"] = 0
for _path, _text in _walk_files():
    if _text is None:
        continue
    _c = _count_in(_text)
    for _k in _post:
        if _k in _c:
            _post[_k] += _c[_k]
    _post["bare_fast"] += _bare_fast_count(_text)
if _post[OLD_ID] != 0:
    ERRORS.append(f"post: {OLD_ID} still present {_post[OLD_ID]}x after rename")
if _post[OLD_PROSE] != 0:
    ERRORS.append(f"post: {OLD_PROSE!r} still present {_post[OLD_PROSE]}x after rename")
if _post[NEW_ID] != EXPECT[OLD_ID]:
    ERRORS.append(
        f"post: {NEW_ID} found {_post[NEW_ID]}x, expected {EXPECT[OLD_ID]}x")
if _post[NEW_PROSE] != EXPECT[OLD_PROSE]:
    ERRORS.append(
        f"post: {NEW_PROSE!r} found {_post[NEW_PROSE]}x, expected {EXPECT[OLD_PROSE]}x")
if _post[FAST_ID] != EXPECT[FAST_ID]:
    ERRORS.append(
        f"post: {FAST_ID} found {_post[FAST_ID]}x, expected {EXPECT[FAST_ID]}x "
        f"(fast-worker pin must be unchanged)")
if _post["bare_fast"] != 0:
    ERRORS.append(f"post: bare {FAST_BARE} found {_post['bare_fast']}x, expected 0x")
CHANGES.append(
    f"post: {NEW_ID} x{_post[NEW_ID]}, {NEW_PROSE!r} x{_post[NEW_PROSE]}, "
    f"{OLD_ID} x{_post[OLD_ID]}, {OLD_PROSE!r} x{_post[OLD_PROSE]}, "
    f"{FAST_ID} x{_post[FAST_ID]} (unchanged), bare {FAST_BARE} x{_post['bare_fast']}")

# ---------------------------------------------------------------- 4. Regression guard: GLOBAL-ROUTING block untouched
_F29_TOKENS = ("ORCHESTRATOR-ONLY_F29", "FACTORY-DISPATCH_F29",
               "DIRECTOR-BRIEF_F29", "NO-GUESSING_F29", "VERIFY-MERGE_F29",
               "GLOBAL-ROUTING_F29", "COST-AWARE_F29")


def _block(text):
    _i = text.find("**GLOBAL-ROUTING")
    if _i < 0:
        return None
    _j = text.find("\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]


_orch_p = p("skills/orchestrate/SKILL.md")
_hm_p = p("rules/hackathon-mode.mdc")
if not exists(_orch_p) or not exists(_hm_p):
    ERRORS.append("guard: orchestrate SKILL.md or hackathon-mode.mdc missing")
else:
    _b1 = _block(open(_orch_p, encoding="utf-8").read())
    _b2 = _block(open(_hm_p, encoding="utf-8").read())
    if _b1 is None or _b2 is None:
        ERRORS.append("guard: GLOBAL-ROUTING block not found in orchestrate or hackathon-mode")
    elif _b1 != _b2:
        ERRORS.append("guard: GLOBAL-ROUTING block differs between orchestrate and hackathon-mode")
    else:
        CHANGES.append("guard: GLOBAL-ROUTING block byte-identical in orchestrate + hackathon-mode (rename did not touch it)")
    for _tok in _F29_TOKENS:
        if _b1 is None or _tok not in _b1:
            ERRORS.append(f"guard: GLOBAL-ROUTING block missing token {_tok}")

# ---------------------------------------------------------------- Decisions + OWED (recorded, not patched blindly)
DECISIONS = [
    "DECISION-30-1 (SPEC re-scope): the rename is build-time only, last in build order (after fix29.py, before STEP 5 Counts). Staged sources (new-skills 19 + new-rules 2 ID occurrences, plus 15 staged prose occurrences) and build.sh inline content (54 pre-existing ID occurrences on 50 lines, plus 5 prose occurrences) keep the old pin because fix16.py, fix24.py and fix29.py anchor on that text and abort the build on anchor mismatch. Precedent: fix #16 performed the Claude -> Grok pin change at build time via fix16.py. The staged-vs-built pin drift is by design (OWED-30-1).",
    "DECISION-30-2 (prose): all 22 'Grok 4.7 High' prose occurrences change to 'Grok 4.7 Extra High', including skills/strategic-compact/SKILL.md:68 (the '500k Grok 4.7 High' context-window example) and :102 (the Cursor 2.1.233 todo-tools note) — the note's operative claim is preserved by its 'and newer' clause. Uniformity over a carve-out: a mixed tree (some prose old, some new) would read as a half-finished rename and break the exact-count assertions. Recorded as OWED-30-5 for the audit to challenge.",
    "DECISION-30-3 (census strictness): the pre-rename census asserts exact counts (49/22/70/0) and refuses to write on any drift. A partial rename is worse than a failed build — the build must fail loudly rather than ship a tree where some files say high and others say extra-high.",
]
OWED = [
    "OWED-30-1 (SPEC re-scope, by design): staged-vs-built pin drift — staged sources keep the old pin (new-skills/ 19 ID + 12 prose occurrences, new-rules/ 2 ID + 3 prose occurrences) and build.sh inline content keeps it (54 pre-existing ID occurrences on 50 lines + 5 prose occurrences; the fix30 hook block itself adds 2 meta-mentions). Syncing staged to the built text would break the fix16/fix24/fix29 anchors and fail the build. Same class as OWED-29-5's 41 lines. verify30 asserts the pins in the BUILT tree only.",
    "OWED-30-2 (OWED-29-4 override): the DeepSeek/Qwen model assignment in the GLOBAL-ROUTING block stays a forward reference — the drone assignment lives in the factory copy per FACTORY_CURSOR_PLAN.md, NOT in #30. verify30 still asserts no deepseek-/qwen- model slugs in the built tree and the names occur only in the GLOBAL-ROUTING block (check 9b, unchanged).",
    "OWED-30-3 (SPEC Honest limits): live Extra High behavior is unverified until Anish runs the live-test prompt (fix30/live-test-prompt.md) in Cursor — pass = Extra High ran the parent on both tasks. The live smoke test is still skipped since Nov 15.",
    "OWED-30-4 (SPEC §6, same as OWED-29-1): the call map (skills/orchestrate/references/call-map.md) is generator-owned and NOT regenerated in this fix — the pin change adds no new dispatch edges and counts are unchanged (67/45/48/55/15/49); the fix28 map stands.",
    "OWED-30-5 (prose judgment, audit to challenge): skills/strategic-compact/SKILL.md:68 and :102 prose changed to 'Grok 4.7 Extra High' (see DECISION-30-2). If the audit finds either line should have kept 'Grok 4.7 High' (historical note / context-window example), the fix is a two-line carve-out in fix30.py plus updated census counts — not a re-scope.",
]

# ---------------------------------------------------------------- main / run log
_log_lines = ["# fix30 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
_log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
_log_lines += ["", f"## OWED ({len(OWED)})"]
_log_lines += [f"- {o}" for o in OWED] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix30")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix30-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix30: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
print(f"fix30: {len(OWED)} OWED item(s) recorded in the patch log")
if ERRORS:
    print(f"fix30: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix30: OK")
