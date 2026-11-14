# Pip pinning — fix #26 §1

Worker A (pip pinning). Date checked: **2026-11-14** (PyPI JSON API,
`https://pypi.org/pypi/<pkg>/json`, latest stable release per package).

## Baseline (verified before starting)

- `build.sh`: 24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae` — matches the
  fix #26 SPEC §0 baseline. Work proceeded.
- Built tree: `~/workspace/hackathon-plugin/hackathon-ecc/`.
- Enumeration: `grep -rn "pip install"` over the built tree returns **42 lines,
  0 containing `==`**. The 42 below are the complete set; nothing was added or
  dropped to fit a count.

## Classification rules (applied uniformly)

- **(a) Real install line** — the line's primary function is to instruct
  installing one or more named packages: a runnable install command, a
  dependency/requirements line, a CI run step, or a setup docstring/header
  comment whose content IS the install command.
- **(b) Prose/mention only** — the install text is embedded in something else:
  an inline code comment, a runtime error/log message, or prose about
  installing. Pinning these would change runtime strings or example code,
  not what gets installed. Left unpinned by design, not owed.
- **(c) `pip install -r requirements.txt`** — pinned via the requirements
  file, not the line. Note: **no `requirements.txt` file exists anywhere in
  the built tree** (`find` returns none), so these lines refer to the user's
  own project requirements file; there is nothing in the plugin to pin here.
- **(d) Forbidden-command list / policy / troubleshooting-table mention** —
  a placeholder (`pip install X`), a policy exclusion, or a table cell. Not
  pinnable by nature. Left as-is.

## Reconciliation vs the Audit #37 scope (17)

My category-(a) count is **20, not 17 — a +3 discrepancy, reported, not
forced**. The Audit #37 report file itself was not found in this workspace
(no `audit37` report; only the "17 unpinned install lines" statement carried
in the fix20/fix21 manifests), so its exact enumeration could not be
recovered and re-checked. The most likely reconciliation, as a hypothesis
only: 20 − 1 (the two-line `tts.mjs:134–135` comment counted once) − 2 (the
two hook-script header/docstring lines, `gateguard-fact-force.js:19` and
`insaits-security-monitor.py:13`) = 17. All 20 (a) lines are pinned anyway:
every one of them is a real install instruction for a named package, and
pinning to today's latest changes nothing about what pip installs today.

## Pins chosen (all resolved, none invented)

| Package | Pinned version | Source |
|---|---|---|
| bandit | 1.9.4 | PyPI JSON, 2026-11-14 |
| black | 26.10.1 | PyPI JSON, 2026-11-14 |
| celery | 5.7.0 | PyPI JSON, 2026-11-14 |
| django-celery-beat | 2.9.0 | PyPI JSON, 2026-11-14 |
| django-celery-results | 2.6.0 | PyPI JSON, 2026-11-14 |
| flower | 2.2.0 | PyPI JSON, 2026-11-14 |
| gateguard-ai | 0.6.2 | PyPI JSON, 2026-11-14 |
| insa-its | 4.9.10 | PyPI JSON, 2026-11-14 |
| mypy | 2.4.1 | PyPI JSON, 2026-11-14 |
| opencv-python | 5.0.0.93 | PyPI JSON, 2026-11-14 |
| opencv-python-headless | 5.0.0.93 | PyPI JSON, 2026-11-14 |
| Pillow | 13.0.0 | PyPI JSON, 2026-11-14 |
| pip-audit | 2.10.1 | PyPI JSON, 2026-11-14 |
| piper-tts | 1.8.0 | PyPI JSON, 2026-11-14 |
| pyautogui | 0.9.54 | PyPI JSON, 2026-11-14 |
| pytest | 9.2.0 | PyPI JSON, 2026-11-14 |
| pytest-cov | 7.1.0 | PyPI JSON, 2026-11-14 |
| pytest-django | 4.14.0 | PyPI JSON, 2026-11-14 |
| pytest-html | 4.2.0 | PyPI JSON, 2026-11-14 |
| pytest-repeat | 0.9.4 | PyPI JSON, 2026-11-14 |
| pytest-timeout | 2.5.0 | PyPI JSON, 2026-11-14 (see note) |
| python-pptx | 1.0.2 | PyPI JSON, 2026-11-14 |
| pywinauto | 0.6.9 | PyPI JSON, 2026-11-14 |
| ruff | 0.17.5 | PyPI JSON, 2026-11-14 |
| safety | 3.8.1 | PyPI JSON, 2026-11-14 |
| uv | 0.13.8 | PyPI JSON, 2026-11-14 |
| yt-dlp | 2026.10.26 | PyPI JSON, 2026-11-14 |

Notes:

- **pytest-timeout:** PyPI `info.version` reports 2.4.0, but the releases list
  contains a stable 2.5.0 with files. pip installs the newest stable, so the
  pin is `==2.5.0` (what pip would install today).
- **opencv-python / opencv-python-headless 5.0.0.93:** a major-version step
  from the 4.x line; it is the current latest, so the pin records today's
  install, per the "do not change what gets installed" rule.
- **yt-dlp 2026.10.26:** CalVer date version, current latest.
- **Owed lines: none.** Every (a) line resolved to a real version; no pin
  was invented and nothing is owed for lack of a version.

## Origin tracing (how each line gets into the built tree)

- `build.sh` STEP 1 installs the ECC Developer profile; STEP 2 copies the
  upstream tree verbatim (`cp -r "$ECC_SRC/skills/."`, agents, rules,
  commands, `scripts/`, `hooks/`). Upstream skills have **no staged source**
  in this repo: `new-skills/`, `round2-skills/`, `rewritten-skills/`,
  `new-rules/` contain none of the eight upstream skills below, none of the
  hook scripts, and none of the agents. Those lines can only be pinned by a
  build-time patch (fix26.py), specified in `pip-patches.md`.
- The **only** staged source among the (a) lines is
  `new-skills/pitch-deck-video/`, copied verbatim by build.sh:230. Its 7 (a)
  lines were edited in place (staged edits below).
- **fix24-owned line:** `skills/plankton-code-quality/SKILL.md:81`
  (`py -m pip install uv ruff`) does not come from upstream text: fix24.py
  E-2 writes it into the built tree at build time (verified: fix24.py
  `p()` joins the built plugin dir, and the E-2 `sub()` inserts the Windows
  install branch). Its pin is specified in `pip-patches.md` flagged
  FIX24-OWNED so the coordinator updates that replacement (or patches the
  built text once) instead of adding a duplicate patch.

## Staged edits (applied — new-skills/pitch-deck-video/)

All 7 staged (a) lines pinned. Line numbers are the **staged** file's; the
staged `SKILL.md:843` is built-tree `:788` — the F-14 sibling worker added a
§7 section above it, shifting staged numbers. Anchors are exact text, so the
shift is harmless.

| Staged file:line | Old → New |
|---|---|
| `SKILL.md:843` | `` `pip install piper-tts` `` → `` `pip install piper-tts==1.8.0` ``; `` `py -m pip install piper-tts` `` → `` `py -m pip install piper-tts==1.8.0` ``; `` `.tools\Scripts\pip install piper-tts` `` → `` `.tools\Scripts\pip install piper-tts==1.8.0` `` (all three mentions on the one line; this is the first-build `piper-tts` line, built-tree `:788`) |
| `references/shots-reference.md:247` | `` `pip install piper-tts` `` → `` `pip install piper-tts==1.8.0` `` |
| `references/troubleshooting.md:212` | `` `pip install piper-tts` `` → `` `pip install piper-tts==1.8.0` `` |
| `references/troubleshooting.md:232` | `` `.tools/bin/pip install yt-dlp` `` → `` `.tools/bin/pip install yt-dlp==2026.10.26` `` |
| `references/troubleshooting.md:233` | `` `.\.tools\Scripts\pip install yt-dlp` `` → `` `.\.tools\Scripts\pip install yt-dlp==2026.10.26` `` |
| `template/scripts/tts.mjs:134` | `` `pip install piper-tts` `` → `` `pip install piper-tts==1.8.0` `` |
| `template/scripts/tts.mjs:135` | `` `py -m pip install piper-tts` `` → `` `py -m pip install piper-tts==1.8.0` `` |

Verified after editing: `grep -rn "pip install"` over staged
`pitch-deck-video/` returns only the pinned lines plus `tts.mjs:180`
(the (b) error string, deliberately left). The built tree was **not** edited.

## Upstream lines (patch specs in pip-patches.md)

13 (a) lines, all with a file / anchor / old → new spec for the coordinator's
fix26.py build-time patch assembly:

| Built-tree file:line | Packages pinned |
|---|---|
| `skills/django-verification/SKILL.md:429` | ruff, black, mypy, pytest, pytest-django, pytest-cov, bandit, safety, pip-audit |
| `skills/frontend-slides/html-template.md:324` | Pillow |
| `skills/frontend-slides/scripts/extract-pptx.py:9` | python-pptx |
| `skills/django-celery/SKILL.md:26` | celery[redis], django-celery-results, django-celery-beat |
| `skills/django-celery/SKILL.md:411` | flower |
| `skills/generating-python-installer/SKILL.md:627` | opencv-python-headless |
| `skills/plankton-code-quality/SKILL.md:81` | uv, ruff — FIX24-OWNED (see above) |
| `skills/windows-desktop-e2e/SKILL.md:55` | pywinauto, pytest, pytest-html, Pillow, pytest-timeout |
| `skills/windows-desktop-e2e/SKILL.md:651` | pywinauto, pytest, pytest-html, Pillow |
| `skills/windows-desktop-e2e/SKILL.md:755` | pyautogui, Pillow, opencv-python |
| `skills/windows-desktop-e2e/SKILL.md:880` | pytest-repeat |
| `scripts/hooks/gateguard-fact-force.js:19` | gateguard-ai |
| `scripts/hooks/insaits-security-monitor.py:13` | insa-its |

Maintenance note: these pins live in fix26.py (build-time patch on the built
tree), not in staged sources, because no staged source exists for upstream
skills. A future rebuild from a newer ECC checkout re-applies them only if
fix26.py still runs; if upstream ever pins these lines itself, the patch
anchors will stop matching and the coordinator will see it as a failed
anchor, not a silent drift.

## Full 42-line classification table

Built-tree paths are relative to `hackathon-ecc/`. Line numbers are the
current built tree's.

| # | File:line | Class | Pin / reason |
|---|---|---|---|
| 1 | `skills/bengali-nlp/SKILL.md:87` — `import regex  # pip install regex` | (b) | Inline code comment; mention only |
| 2 | `skills/bengali-nlp/SKILL.md:139` — `# - bnlp (pip install bnlp_toolkit)` | (b) | Comment in a tokenizer list; mention only |
| 3 | `skills/bengali-nlp/SKILL.md:207` — `# Preferred: use PyICU ... (pip install PyICU)` | (b) | Code comment; mention only |
| 4 | `skills/django-verification/SKILL.md:428` — `pip install -r requirements.txt` | (c) | Pinned via requirements file |
| 5 | `skills/django-verification/SKILL.md:429` — `pip install ruff black mypy pytest pytest-django pytest-cov bandit safety pip-audit` | (a) | Pinned — see patch spec P-01 |
| 6 | `skills/frontend-slides/html-template.md:324` — `` `pip install Pillow` `` | (a) | `Pillow==13.0.0` — patch spec P-02 |
| 7 | `skills/frontend-slides/scripts/extract-pptx.py:9` — `Requires: pip install python-pptx` | (a) | `python-pptx==1.0.2` — patch spec P-03 |
| 8 | `skills/python-patterns/SKILL.md:546` — `# pip install isort` | (b) | Comment in an import-sorting example; mention only |
| 9 | `skills/django-celery/SKILL.md:26` — `pip install 'celery[redis]' django-celery-results django-celery-beat` | (a) | Pinned — patch spec P-04 |
| 10 | `skills/django-celery/SKILL.md:411` — `pip install flower` | (a) | `flower==2.2.0` — patch spec P-05 |
| 11 | `skills/generating-python-installer/SKILL.md:150` — `py -3.12-32 -m pip install -r requirements.txt` | (c) | Pinned via requirements file |
| 12 | `skills/generating-python-installer/SKILL.md:627` — `pip install opencv-python-headless` | (a) | `opencv-python-headless==5.0.0.93` — patch spec P-06 |
| 13 | `skills/plankton-code-quality/SKILL.md:81` — `py -m pip install uv ruff` | (a) | `uv==0.13.8 ruff==0.17.5` — patch spec P-07, FIX24-OWNED |
| 14 | `skills/windows-desktop-e2e/SKILL.md:55` — `pip install pywinauto pytest pytest-html Pillow pytest-timeout` | (a) | Pinned — patch spec P-08 |
| 15 | `skills/windows-desktop-e2e/SKILL.md:610` — `pip install -r requirements.txt;` | (c) | Pinned via requirements file |
| 16 | `skills/windows-desktop-e2e/SKILL.md:651` — `run: pip install pywinauto pytest pytest-html Pillow` | (a) | Pinned — patch spec P-09 |
| 17 | `skills/windows-desktop-e2e/SKILL.md:755` — `pip install pyautogui Pillow opencv-python` | (a) | Pinned — patch spec P-10 |
| 18 | `skills/windows-desktop-e2e/SKILL.md:880` — `pip install pytest-repeat` | (a) | `pytest-repeat==0.9.4` — patch spec P-11 |
| 19 | `skills/pitch-deck-video/SKILL.md:788` — `` `pip install piper-tts` `` (+ Windows variants, one line) | (a) | `piper-tts==1.8.0` (all three mentions) — STAGED EDIT, staged `:843` |
| 20 | `skills/pitch-deck-video/references/shots-reference.md:247` — `` `pip install piper-tts` `` | (a) | `piper-tts==1.8.0` — STAGED EDIT |
| 21 | `skills/pitch-deck-video/references/troubleshooting.md:212` — `` `pip install piper-tts` `` | (a) | `piper-tts==1.8.0` — STAGED EDIT |
| 22 | `skills/pitch-deck-video/references/troubleshooting.md:232` — `.tools/bin/pip install yt-dlp` | (a) | `yt-dlp==2026.10.26` — STAGED EDIT |
| 23 | `skills/pitch-deck-video/references/troubleshooting.md:233` — `.\.tools\Scripts\pip install yt-dlp` | (a) | `yt-dlp==2026.10.26` — STAGED EDIT |
| 24 | `skills/pitch-deck-video/template/scripts/tts.mjs:134` — `Install with \`pip install piper-tts\`` | (a) | `piper-tts==1.8.0` — STAGED EDIT |
| 25 | `skills/pitch-deck-video/template/scripts/tts.mjs:135` — `` `py -m pip install piper-tts` `` | (a) | `piper-tts==1.8.0` — STAGED EDIT |
| 26 | `skills/pitch-deck-video/template/scripts/tts.mjs:180` — error string `install with: pip install piper-tts (Windows PowerShell: py -m pip install piper-tts)` | (b) | Runtime error message; install text is embedded guidance, not an install step. Left unpinned |
| 27 | `agents/ecc-agent-evaluator.md:33` — `Forbidden: ... \`pip install\` ...` | (d) | Forbidden-command list; bare `pip install` with no package |
| 28 | `agents/ecc-django-build-resolver.md:77` — table: `` `pip install X` `` | (d) | Troubleshooting table; `X` is a placeholder, not pinnable |
| 29 | `agents/ecc-django-build-resolver.md:79` — table: `pip install --upgrade pip`, then `pip install -r requirements.txt` | (d) | Troubleshooting table; pip itself + a (c) line |
| 30 | `agents/ecc-django-build-resolver.md:85` — `pip install --force-reinstall -r requirements.txt` | (c) | Pinned via requirements file |
| 31 | `agents/ecc-django-build-resolver.md:94` — `pip install -r requirements.txt` | (c) | Pinned via requirements file |
| 32 | `agents/ecc-django-build-resolver.md:182` — table: `` `pip install psycopg2-binary` `` | (d) | Troubleshooting table cell; a fix-pattern example, not an install step |
| 33 | `agents/ecc-django-build-resolver.md:229` — `Prefer \`pip install --upgrade\` over manual ...` | (b) | Prose about resolving conflicts; no package named |
| 34 | `agents/ecc-opensource-packager.md:137` — `{npm install \| pip install -r requirements.txt \| cargo build \| go mod download}` | (c) | Template alternative; the pip branch is `-r` |
| 35 | `scripts/hooks/gateguard-fact-force.js:19` — `Full package with config support: pip install gateguard-ai` | (a) | `gateguard-ai==0.6.2` — patch spec P-12 |
| 36 | `scripts/hooks/insaits-security-monitor.py:13` — `pip install insa-its` | (a) | `insa-its==4.9.10` — patch spec P-13 |
| 37 | `scripts/hooks/insaits-security-monitor.py:205` — `log.warning("Not installed. Run: pip install insa-its")` | (b) | Runtime log warning; message text, not an install step |
| 38 | `scripts/hooks/insaits-security-wrapper.js:78` — stderr `... pip install insa-its` | (b) | Runtime stderr message; message text, not an install step |
| 39 | `manifests/pi-core.json:25` — `"... (npx, pip install, curl\|sh)"` | (d) | Policy exclusion text; bare `pip install`, no package |
| 40 | `manifests/pi-core.json:223` — `"manim-video": "niche video production; pip installs at runtime"` | (d) | Manifest note; no install command |
| 41 | `manifests/pi-core.json:297` — `"windows-desktop-e2e": "niche Windows desktop automation; pip installs at runtime"` | (d) | Manifest note; no install command |
| 42 | `manifests/pi-core.json:407` — `"(pip install <dep>)"` in safety semantics | (d) | Policy text; `<dep>` is a placeholder, not pinnable |

Counts: (a) 20 · (b) 8 · (c) 6 · (d) 8 · total 42.

## Flags for the coordinator (verify26 + fix26.py)

1. **verify24 E-5 will fail after this fix unless codified.** `fix24/verify24.py:389`
   asserts the exact unpinned Windows yt-dlp line in
   `skills/pitch-deck-video/references/troubleshooting.md`. That line is now
   pinned in the staged source (`yt-dlp==2026.10.26`). No other prior
   verifier asserts any pip line (checked verify20–verify25 for `pip
   install` and package names; only fix24 E-5 hits). The coordinator must
   codify this as a known tail in verify26 (SPEC §9 allows codified tails;
   the §3 verifier edit is the only authorized verifier edit, so if
   codifying E-5 needs a verifier change it is a parent adjudication, not
   mine to make).
2. **Verify-criterion scoping.** SPEC §1's "grep for unpinned `pip install`
   lines = 0 in the built tree" can only hold when scoped to category (a):
   a naive tree-wide grep will still match the 8 (b) lines (real package
   names in comments/messages), the 6 (c) lines (`-r requirements.txt`),
   and the 8 (d) lines (placeholders/policy text) — none of which are
   pinnable. verify26 should assert zero unpinned (a) lines (the 20 listed
   above, each carrying `==`) and assert the (b)/(c)/(d) lines listed in the
   table are unchanged.
3. **No fix*.py was edited, no verifier was edited, build.sh was not run,
   the built tree was not edited, nothing was committed, bundled, or pushed.**
   fix11/fix11-stage.py was not re-run.
