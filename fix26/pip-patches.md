# Pip patch specs — fix #26 §1 (upstream lines, build-time patch)

Worker A (pip pinning). For the coordinator's fix26.py build-time patch
assembly. All paths are relative to the built plugin dir (`hackathon-ecc/`).
All versions were resolved from the PyPI JSON API on **2026-11-14** (latest
stable release; see `pip-pinning.md` for the version table). Anchors are
exact text; line numbers are the current built tree's and may shift — match
on the anchor, not the number.

Provenance: every file below comes from the upstream ECC tree copied verbatim
by build.sh STEP 2 (`cp -r "$ECC_SRC/skills/."`, agents, `scripts/`,
`hooks/`). There is no staged source for any of them in `new-skills/`,
`round2-skills/`, `rewritten-skills/`, or `new-rules/`, so a staged edit was
not possible. The one exception is P-07 (see its flag).

How to apply: exact-string replacement of OLD by NEW in the named built-tree
file (same `sub()` pattern fix24.py uses). Each OLD must occur exactly once
in its file; if an anchor fails to match, stop and report it — do not guess
a nearby line. After applying, the built tree must contain zero unpinned
category-(a) `pip install` lines (see `pip-pinning.md` § "Flags for the
coordinator" for the verify scoping note).

---

## P-01 — `skills/django-verification/SKILL.md:429`

- Anchor: the `pip install` line in the CI/lint tooling block (directly
  below the `pip install -r requirements.txt` line at :428).
- OLD:
  `pip install ruff black mypy pytest pytest-django pytest-cov bandit safety pip-audit`
- NEW:
  `pip install ruff==0.17.5 black==26.10.1 mypy==2.4.1 pytest==9.2.0 pytest-django==4.14.0 pytest-cov==7.1.0 bandit==1.9.4 safety==3.8.1 pip-audit==2.10.1`

## P-02 — `skills/frontend-slides/html-template.md:324`

- OLD:
  `**Dependency:** \`pip install Pillow\``
- NEW:
  `**Dependency:** \`pip install Pillow==13.0.0\``

## P-03 — `skills/frontend-slides/scripts/extract-pptx.py:9`

- OLD:
  `Requires: pip install python-pptx`
- NEW:
  `Requires: pip install python-pptx==1.0.2`

## P-04 — `skills/django-celery/SKILL.md:26`

- OLD:
  `pip install 'celery[redis]' django-celery-results django-celery-beat`
- NEW:
  `pip install 'celery[redis]==5.7.0' django-celery-results==2.6.0 django-celery-beat==2.9.0`
- Note: the extras bracket stays attached to the pinned celery
  (`celery[redis]==5.7.0` is the standard pip spelling).

## P-05 — `skills/django-celery/SKILL.md:411`

- OLD:
  `pip install flower`
- NEW:
  `pip install flower==2.2.0`

## P-06 — `skills/generating-python-installer/SKILL.md:627`

- OLD:
  `pip install opencv-python-headless`
- NEW:
  `pip install opencv-python-headless==5.0.0.93`

## P-07 — `skills/plankton-code-quality/SKILL.md:81` — FIX24-OWNED

- OLD (as written into the built tree by fix24.py E-2):
  `py -m pip install uv ruff`
- NEW:
  `py -m pip install uv==0.13.8 ruff==0.17.5`
- FLAG — do not duplicate: this line is not upstream text. fix24.py E-2
  inserts it at build time (the Windows install branch; verified in
  fix24.py, `p()` joins the built plugin dir). The pin must be applied by
  EITHER updating the fix24.py E-2 replacement string OR a single fix26.py
  patch on the resulting built text — one of the two, not both. If the
  coordinator patches the built text, the anchor above is the line fix24.py
  produces. verify24 E-2 asserts only the "Windows (PowerShell) first"
  heading, not this line's text, so pinning it does not break that check.

## P-08 — `skills/windows-desktop-e2e/SKILL.md:55`

- OLD:
  `pip install pywinauto pytest pytest-html Pillow pytest-timeout`
- NEW:
  `pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow==13.0.0 pytest-timeout==2.5.0`
- Note: pytest-timeout pins to 2.5.0, the newest stable release with files
  on PyPI (see `pip-pinning.md` note — `info.version` still reports 2.4.0).

## P-09 — `skills/windows-desktop-e2e/SKILL.md:651`

- Anchor: the CI `run:` step (indented; distinct from :55 by the `run:` prefix).
- OLD:
  `      run: pip install pywinauto pytest pytest-html Pillow`
- NEW:
  `      run: pip install pywinauto==0.6.9 pytest==9.2.0 pytest-html==4.2.0 Pillow==13.0.0`

## P-10 — `skills/windows-desktop-e2e/SKILL.md:755`

- OLD:
  `pip install pyautogui Pillow opencv-python`
- NEW:
  `pip install pyautogui==0.9.54 Pillow==13.0.0 opencv-python==5.0.0.93`

## P-11 — `skills/windows-desktop-e2e/SKILL.md:880`

- OLD:
  `pip install pytest-repeat`
- NEW:
  `pip install pytest-repeat==0.9.4`

## P-12 — `scripts/hooks/gateguard-fact-force.js:19`

- Anchor: the header comment line "Full package with config support".
- OLD:
  ` * Full package with config support: pip install gateguard-ai`
- NEW:
  ` * Full package with config support: pip install gateguard-ai==0.6.2`

## P-13 — `scripts/hooks/insaits-security-monitor.py:13`

- Anchor: the module docstring "Setup:" block.
- OLD:
  `  pip install insa-its`
- NEW:
  `  pip install insa-its==4.9.10`

---

## Coverage check

- Patch specs above: 13 (P-01–P-13).
- Staged edits (already applied in `new-skills/pitch-deck-video/`, see
  `pip-pinning.md`): 7 lines.
- Total category-(a) lines pinned: 20. Owed: none.
- Not patched, by design: the 8 (b) prose/mention lines, 6 (c) `-r` lines,
  and 8 (d) policy/table lines in the 42-line table in `pip-pinning.md`.
