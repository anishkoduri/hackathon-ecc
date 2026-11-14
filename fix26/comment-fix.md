# §3 — Stale build.sh fix25 comment (fix #26)

## Before (`build.sh:24061–24067`, 7 lines)

```sh
# --- fix #25: build-time patches (S1 styles.csv header 80 -> 89) ---
# fix25/fix25.py patches the built tree in place, same pattern as fix24/fix24.py:
# §4(a) S1 corrects the ui-ux-pro-max header (frontmatter :3 + body :8) from
# "80 searchable styles" to "89 searchable styles (51 active)" — the csv has
# 89 rows (51 active re-counted from the Status column) and is the source.
# Runs after fix24, before STEP 5. Exits non-zero on anchor errors (set -euo
# pipefail stops the build); the run log lands in fix25/fix25-patch-log.md.
```

The comment described fix25.py as "§4(a) S1" only. The script also carries
the §1 wires, the §2 inventory close, the §4(d) browser-qa line, and the
loop-status reference removals.

## After (`build.sh:24061–24067`, 7 lines — same count)

```sh
# --- fix #25: build-time patches (§1 wires, §2 inventory, §4 S1/benchmark) ---
# fix25/fix25.py patches the built tree in place, same pattern as fix24/fix24.py:
# §1 wires ck (session-start.js runs skills/ck/hooks/session-start.mjs) and
# /prp-commit via conventional-commit-review; §2 closes the orch-* inventory
# bypass; §4(a) S1 header 80 -> 89 styles; §4(d) browser-qa beat-v5 line;
# loop-status dangling references removed. Runs after fix24, before STEP 5;
# exits non-zero on anchor errors; run log in fix25/fix25-patch-log.md.
```

Line count: 7 → 7 (header + 6 comment lines → header + 6 comment lines).
No lines added or removed. The header line (:24061) was reworded in place
alongside the six comment lines (:24062–24067), since it also said "S1"
only — still the same line count.

## Accuracy note — which wires the script carries

The task brief lists the §1 wires as W1 ck, W2 conventional-commit-review,
W3 ecc-recipes, W4 /test-coverage. Only W1 and W2 live in fix25.py itself:
W3 (RECIPES_F25) and W4 (TESTCOV_F25) are staged edits in
`new-skills/orchestrate/SKILL.md`, not build-time patches. The new comment
therefore names only the script's own wires (ck + /prp-commit), which is
what the script actually does.

## Verifier

`verify25.py` diff numbers were NOT updated in this change, per the task:
the coordinator measures the final diff after the rebuild and updates
them. The §3 edit changes 7 build.sh lines in place (0 net lines), so the
expected diff movement is confined to the fix25-block region.
