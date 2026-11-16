# Dry-run #42, Leg 5 — /test-coverage Steps 1–2 exercise note

Command exercised: `commands/test-coverage.md` (the fix #25 wire:
orchestrate Verify step 1, TESTCOV_F25, runs the command's Steps 1–2
measurement only — Step 3 test generation stays in the fix loop).

Scratch project: `leg5-testcov/` — verbatim copy of the dry-run #41
fixture (a Python project with a `pyproject.toml` pytest indicator,
`src/calc.py` with 6 functions, `tests/test_calc.py` with 5 tests
deliberately NOT covering `mul` or `untested_helper`).

Step 1 (detect + run): `pytest --cov=src --cov-report=json` — exit 0,
5 passed. pytest-cov installed into `dryrun42-scratch/pylibs/`
(system pytest 9.2.0 has no coverage plugin); the install is scratch
only and is deleted with the cleanup.

Step 2 (parse + list below 80%, worst-first): `coverage.json` —
`src/calc.py` **68.2%** (15/22 statements, 7 missing lines: mul's body
and untested_helper's branches), `src/__init__.py` 100%, total 68.2%.
Files below 80%: `src/calc.py` (68.2%) — exactly the under-covered file
the fixture was built to expose. The measurement lists the file; the
fix loop (add tests under tdd-workflow) is out of scope for this
exercise, per the wire's scoping (Steps 1–2 only).

Identical outcome to dry-runs #40 and #41 (68.2%, 5 passed) — no
regression from the fix #27 §1–§8 edits.
