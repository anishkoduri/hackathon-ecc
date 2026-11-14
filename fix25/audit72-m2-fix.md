# Audit #72 M2 fix — mobile-ship launch-marketing.md reword

**Date:** 2026-11-13. **Worker:** M2-fix worker. **Finding:** Audit #72 M2
(`fix25/audit72-report.md`): `skills/mobile-ship/references/launch-marketing.md:15`
prescribed `@remotion/google-fonts` as the promo-video font mechanism — a stale
instruction that would reintroduce the removed loader if followed. Prose
mentions do not count against the §4(b) self-host requirement (decision
recorded in the audit), but the line itself had to be reworded.

## The reword

**File (staged source):**
`round2-skills/mobile-ship/references/launch-marketing.md:15`
(build copies `round2-skills/mobile-ship` wholesale into the built tree —
`build.sh:234-236`, `cp -r`; no build.sh edit needed or made)

**Old text:**
`  - Fonts: Google Fonts under the OFL, via `@remotion/google-fonts`.`

**New text:**
`  - Fonts: Google Fonts under the OFL, self-hosted as vendored woff2 via `@remotion/fonts` + `staticFile` (the pitch-deck-video template pattern).`

One-line reword; surrounding section untouched. The new text deliberately
contains no `@remotion/google-fonts` string. The mechanism named matches the
template as built: `template/src/fonts.ts` imports `loadFont` from
`@remotion/fonts` and `staticFile` from `remotion`, loading vendored woff2
from `public/fonts/` (SPEC §4(b) pattern, verified in Audit #72 §4(b)).

## Frozen-text check (before editing)

- Grep for `launch-marketing` and for `google-fonts` across all
  `fix*/verify*.py`, `audit-scripts/`, and `fix25/fix25.py`: **0 hits**
  (both greps rc=1). The line is not frozen and not verifier-asserted.
- Grep for `@remotion/google-fonts` in `build.sh`: **0 hits** (only
  unrelated `google-fonts` domain text in ui-ux-pro-max at :7426, :7439,
  :13297, :13310, :23705). The staged file is the only source of the line.
- No pitch-deck-video template file, verify*.py file, or
  design-inventory.md was touched. `fix11/fix11-stage.py` never run.

## Rebuild (run 4)

- Command: `bash build.sh > fix25/build-log-run4.txt 2>&1` from
  `~/workspace/hackathon-plugin`. **Exit 0.**
- `build.sh`: **24,079 lines, md5 `f19483f50e89998f8b9dc052ed5d5fae`** —
  unchanged by the build. Diff vs `build.sh.before-fix23`: **+305/−0**
  (0 deletions, 305 additions) — additions-only intact.
- fix16: **ERRORS: 0, NOTES: 38, CHANGES: 649, REMOVALS: 88** — identical
  to run 2. JS syntax failures 0, JSON failures 0.
- fix25 patch: **14 change(s), `fix25: OK`**.
- Banned terms in the built tree: **TOTAL BANNED-TERM HITS: 0**.
- Counts (build log tail): skills **166**, agents **72**, rules **123**,
  commands **87**, hooks **15** — unchanged.

## Built-tree confirmation

- `hackathon-ecc/skills/mobile-ship/references/launch-marketing.md:15`
  reads the new text (verified by direct read). `diff` staged vs built
  file: clean.
- Remaining `@remotion/google-fonts` hits in the built tree
  (`grep -rn "@remotion/google-fonts" hackathon-ecc/ --exclude-dir=node_modules`):
  exactly **1**:
  - `hackathon-ecc/skills/pitch-deck-video/template/src/fonts.ts:2` —
    provenance comment (`// families live from Google Fonts via
    `@remotion/google-fonts`, which fetched …`), intentional, stays per
    the Audit #72 M2 decision. Code, not prose: it is a comment, loads
    nothing.
- No import, no package.json dependency, no fetch anywhere in the built
  tree references `@remotion/google-fonts` (Audit #72 §4(b) already
  established 0 for imports/deps/fetches; this fix removes the last prose
  prescription).

## Could not verify / owed

- Nothing owed by this fix. Re-sweep and verify25 own the follow-up
  assertions (per task: no audit/sweep/dry-run/verify run here).
