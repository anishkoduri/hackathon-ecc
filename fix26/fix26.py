#!/usr/bin/env python3
"""Fix #26 — build-time patches (UPSTREAM halves).

Run by build.sh as a patch step (after fix25, before STEP 5):
    python3 "$PLUGIN_ROOT/fix26/fix26.py" "$PLUGIN_DIR"

Operates on the BUILT tree only (upstream ECC files, which have no staged
source). Staged-source halves are edited directly in new-skills/ /
round2-skills/ / rewritten-skills/ / new-rules/ and flow through the
STEP 2 copy. Every anchor asserts count==1 and fails loudly on mismatch;
the script exits non-zero on any error so the build fails rather than
shipping a half-patched tree.

§8 ck wire KEEP (parent decision at the fix #25 close): the ck wire stays,
at its true cost (~1k tokens/session, not ~100). The wire itself is
unchanged — only the stale cost claims are corrected here, to the live
measurement (7,382 chars / 890 words merged with an empty ck store):
- session-start.mjs header (:6-7): "~100 tokens" + "still small at ~50
  lines" — the hook always injects the full SKILL.md (169 lines, 825
  words, 6,377 chars in the run-5 built tree) plus the summary block.
- session-start.mjs :90: "now only ~50 lines" — same error, same fix.
- ck SKILL.md :159: "~100 tokens per session" — the ~100-token figure is
  the compact summary block alone, not the session total.
- session-start.mjs :129 "Compact summary block (~100 tokens)" is LEFT
  UNCHANGED: the block is 4 short lines (typically ~30 words / ~40
  tokens, up to ~50 words / ~70 tokens with long goal/next lines), so
  ~100 tokens is a fair ceiling for the block alone — and the empty-store
  measurement never fires the block, so nothing contradicts it. See
  fix26/ck-note.md for the full adjudication.
- ck is upstream (no staged source; build.sh audit_patch already touches
  its SKILL.md), so the corrections live here as build-time patches.

§1 pip pins: the 13 upstream install lines below (P-01–P-13, see
fix26/pip-patches.md for the specs and fix26/pip-pinning.md for the
42-line classification). Versions resolved from PyPI 2026-11-14.
"""
import os
import sys

BASE = sys.argv[1]
CHANGES = []
ERRORS = []


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def exists(f):
    return os.path.exists(f)


def p(rel):
    return os.path.join(BASE, rel)


def sub(f, old, new, count=1):
    """Exact replacement; record an error if the anchor does not match."""
    text = read(f)
    n = text.count(old)
    if n != count:
        ERRORS.append(f"{f}: anchor found {n}x, expected {count}x :: {old[:120]!r}")
        return False
    write(f, text.replace(old, new))
    CHANGES.append(f"{f} — {old[:80]!r} -> {new[:80]!r}")
    return True


# ---------------------------------------------------------------- §8 ck cost lines (KEEP at the measured ~1k tokens/session)
# Parent decision at the fix #25 close: KEEP the ck wire at its true cost.
# The .mjs always injects the full SKILL.md (169 lines in the run-5 built
# tree) plus the compact summary — ~1k tokens/session, not ~100. The
# "~50 lines" / "~100 tokens" claims below are corrected to the measured
# cost; the :129 summary-block claim is left alone (see the docstring).
f = p("skills/ck/hooks/session-start.mjs")
if exists(f):
    sub(f,
        " * Injects ~100 tokens (not ~2,500 like v1).\n"
        " * SKILL.md is injected separately (still small at ~50 lines).",
        " * Injects ~1k tokens per session (not ~2,500 like v1): the full SKILL.md\n"
        " * (~170 lines) plus the compact summary below.")
    sub(f,
        "  // Load skill (always inject — now only ~50 lines)",
        "  // Load skill (always inject the full SKILL.md, ~170 lines, ~1k tokens/session)")
f = p("skills/ck/SKILL.md")
if exists(f):
    sub(f,
        "The hook injects ~100 tokens per session (compact 5-line summary). It also detects",
        "The hook injects ~1k tokens per session (the full SKILL.md plus the compact 5-line summary). It also detects")


# --- §1 pip pins (Audit #37 scope; versions resolved from PyPI 2026-11-14) ---
# 20 real install lines pinned in total: 7 staged (new-skills/pitch-deck-video/,
# piper-tts==1.8.0 + yt-dlp==2026.10.26, edited directly) + the 13 upstream
# lines below, patched here on the built text. Audit #37 said 17; its
# enumeration is unrecoverable (no report file — only the count survives in
# fix20/fix21 MANIFEST.md), and the grep classification in fix26/pip-pinning.md
# finds 20 real lines (reconciliation hypothesis there: the tts.mjs 2-line
# comment counted once + 2 hook header/docstring lines excluded = 17).
# P-07 is fix24.py E-2 output — patched here on the built text, once only;
# fix24.py itself is NOT edited. Pins are the current latest (what pip
# installs today), so nothing about what gets installed changes.
f = p("skills/django-verification/SKILL.md")
if exists(f):
    sub(f,
        "pip install ruff black mypy pytest pytest-django pytest-cov bandit safety pip-audit",
        "pip install ruff==0.17.5 black==26.10.1 mypy==2.4.1 pytest==9.2.0 pytest-django==4.14.0 pytest-cov==7.1.0 bandit==1.9.4 safety==3.8.1 pip-audit==2.10.1")
f = p("skills/frontend-slides/html-template.md")
if exists(f):
    sub(f,
        "**Dependency:** `pip install Pillow`",
        "**Dependency:** `pip install Pillow==13.0.0`")
f = p("skills/frontend-slides/scripts/extract-pptx.py")
if exists(f):
    sub(f,
        "Requires: pip install python-pptx",
        "Requires: pip install python-pptx==1.0.2")
f = p("skills/django-celery/SKILL.md")
if exists(f):
    sub(f,
        "pip install 'celery[redis]' django-celery-results django-celery-beat",
        "pip install 'celery[redis]==5.7.0' django-celery-results==2.6.0 django-celery-beat==2.9.0")
    sub(f,
        "pip install flower",
        "pip install flower==2.2.0")
f = p("skills/generating-python-installer/SKILL.md")
if exists(f):
    sub(f,
        "pip install opencv-python-headless",
        "pip install opencv-python-headless==5.0.0.93")
f = p("skills/plankton-code-quality/SKILL.md")
if exists(f):
    sub(f,
        "py -m pip install uv ruff",
        "py -m pip install uv==0.13.8 ruff==0.17.5")
f = p("skills/windows-desktop-e2e/SKILL.md")
if exists(f):
    sub(f,
        "pip install pywinauto pytest pytest-html Pillow pytest-timeout",
        "pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow==13.0.0 pytest-timeout==2.5.0")
    sub(f,
        "      run: pip install pywinauto pytest pytest-html Pillow",
        "      run: pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow==13.0.0")
    sub(f,
        "pip install pyautogui Pillow opencv-python",
        "pip install pyautogui==0.9.54 Pillow==13.0.0 opencv-python==5.0.0.93")
    sub(f,
        "pip install pytest-repeat",
        "pip install pytest-repeat==0.9.4")
f = p("scripts/hooks/gateguard-fact-force.js")
if exists(f):
    sub(f,
        " * Full package with config support: pip install gateguard-ai",
        " * Full package with config support: pip install gateguard-ai==0.6.2")
f = p("scripts/hooks/insaits-security-monitor.py")
if exists(f):
    sub(f,
        "  pip install insa-its",
        "  pip install insa-its==4.9.10")


# ---------------------------------------------------------------- main
_log_lines = ["# fix26 run log", "",
              f"## Errors ({len(ERRORS)})"]
_log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
_log_lines += ["", f"## Changes ({len(CHANGES)})"]
_log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
_log_dir = os.path.join(os.path.dirname(BASE.rstrip("/")), "fix26")
os.makedirs(_log_dir, exist_ok=True)
with open(os.path.join(_log_dir, "fix26-patch-log.md"), "w", encoding="utf-8") as _fh:
    _fh.write("\n".join(_log_lines) + "\n")
print(f"fix26: {len(CHANGES)} change(s)")
for c in CHANGES:
    print(f"  - {c}")
if ERRORS:
    print(f"fix26: {len(ERRORS)} ERROR(S)", file=sys.stderr)
    for e in ERRORS:
        print(f"  ! {e}", file=sys.stderr)
    sys.exit(1)
print("fix26: OK")
