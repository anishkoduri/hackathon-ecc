# Dry-run #46, Leg 5 — /test-coverage Steps 1–2 (re-run of the #44 fixture)

Scratch pytest project `leg5-testcov/` (verbatim copy of the #44 fixture):
`pyproject.toml` pytest indicator, `src/calc.py` (6 functions), `tests/test_calc.py`
(5 tests, deliberately not covering `mul` or `untested_helper`).

- `python3 -m pytest --cov=src --cov-report=json`: exit 0, **5 passed**.
- `src/calc.py` **68.2%** (15/22 statements), listed below 80% worst-first, exactly
  as the wire specifies. Identical outcome to #40/#41/#42/#43/#44/#45.
- Step 3 generation stays in the fix loop by design and was not run.
