# Sweep #19 — plugin fix program #17 (hackathon-ecc) — CHECK ONLY

- **Date:** Wed 2026-11-11 (evening CT)
- **Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/` (excluding `node_modules/`) + staged sources for fix17 (`fix17/fix17.py`, `fix17/SPEC-DRAFT.md`) + `~/workspace/hackathon-plugin/build.sh`
- **No edits made.** No plugin file touched, `build.sh` not run, Campus Eats artifact not touched, no commit/bundle/GitHub.
- **build.sh identity confirmed:** 23,276 lines, md5 `0775d6f33c5eeb4cf509fdee1cd319d7` (matches the task's stated hash).
- **Sanity re-run (read-only):** `fix17/verify17.py` → **59/59 checks pass**.

## Verdict: CLEAN

- **Blocking: 0**
- **Minor: 0**
- No live banned term, no wrong pin, no E1 permission wording, no band leak, no wording drift, no inventory drift.

---

## 1. Banned terms in the built tree — 0 hits

Pattern (case-insensitive): `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`, run over the whole built tree excluding `node_modules/`.

| Term | Hits in built tree |
|---|---:|
| claude | 0 |
| codex | 0 |
| anthropic | 0 |
| opus | 0 |
| sonnet | 0 |
| haiku | 0 |
| composer-2.5 | 0 |
| **Total** | **0** |

Hit table: empty — there are no hits to list, so no live-vs-exception classification is needed for the built tree. (All 798 build.sh exception lines are classified under check 4 below; none of them ship.)

## 2. Model pins — all slug-only, no wrong pins

| Check | Result |
|---|---:|
| `grok-4.7-high` occurrences (slug form) | 52 (50 + 2 sentence-final `grok-4.7-high.`) |
| `cursor-grok-4.6-high-fast` occurrences | 100 (98 + 2 sentence-final `cursor-grok-4.6-high-fast.`) |
| Bare `grok-4.6-high-fast` (no `cursor-` prefix) | **0** |
| Bracket syntax (`grok-4.7[` / `grok-4.6[`) | **0** |
| Version-suffix residue (`Grok 4.7 High [0-9]`, `grok-4.7-high-[0-9]`, etc.) | **0** |
| Any `effort=` key (bare or `reasoning_effort=`) | **0** |
| `composer-2.5` pin | **0** |
| Any other grok version token (`grep -rhoE 'grok-[0-9][a-z0-9.-]*'`) | only the two sanctioned slugs above |
| Non-Grok model pins (`model: gpt|gemini|claude|sonnet|opus|haiku`) | **0** |

Notes:
- The bare `grok-4.7-high` occurrences are the sanctioned slug form, e.g. `rules/common-performance.mdc:13,30` ("runs on model `grok-4.7-high` (slug form only)"), `skills/gan-style-harness/SKILL.md:79,92,109` (`GAN_*_MODEL=grok-4.7-high` env values), `skills/orch-add-feature/SKILL.md:33`, `skills/orch-build-mvp/SKILL.md:40`, `skills/orch-change-feature/SKILL.md:36`. All 100 `grok-4.6-high-fast` occurrences carry the `cursor-` prefix.
- Display names (not pins): `Grok 4.7 High` ×19, `Grok 4.6 High Fast` ×19, all in prose/picker instructions, no version suffix.
- `reasoning_effort` appears exactly once as prose, `rules/common-performance.mdc:30` ("Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin") — no `=` key anywhere, so there is no bare `effort=` key to flag.

## 3. Fix17 residues — 0 leaks

| Check | Result |
|---|---:|
| "may invent" permission wording (case-insensitive, incl. "MAY invent", "Invention is allowed") | **0** |
| "30–34" / "30-34" band | **0** |
| "SPEC draft" / "SPEC-DRAFT" reference | **0** |
| "v4 motion set" phrase used bare | **0** |

Grounding (why these were the right strings to hunt):
- The superseded band lives only in the SPEC draft: `fix17/SPEC-DRAFT.md:476,490,492` ("target band is **30–34 elements**", "Inside the 30–34 band") — a predicted audit-scope element count for the fix, not a shipped rule. It did not leak into the built tree.
- The draft E1 heading `fix17/SPEC-DRAFT.md:385,407-408` ("the design-lead MAY invent page-specific elements", "Invention is allowed: the design-lead may invent…") is draft wording only. The shipped E1 in all four placements is the active push ("The design-lead MUST push boundaries and aim to be trailblazing…", see check 5).
- The SPEC draft itself flags the anchor problem at `fix17/SPEC-DRAFT.md:520-521` ("'v4-level motion set' has no file anchor… M1–M6 as written…").

Investigated non-findings (not counted as findings):
- `skills/polish-pass/reference/polish.md:35` — "…a product idea or a new direction that polish isn't allowed to invent." Matched the broad "allowed to invent" probe. This is a **prohibition on polish-pass**, not a "may invent" permission for the design-lead, and it is not fix17 E1 wording. E1 governs the design-lead; polish-pass is a different role. Not a residue.
- `skills/make-interfaces-feel-better/SKILL.md:108` — "**Default motion set (fix #17, v4-level).** Every page carries the default motion set — scroll entrances with a 1500ms fail-safe (M1/M2…), hover micro-interactions… (M3), life in existing pieces (M4), and at least one small interactive bit per page… (M5)…" The exact phrase "v4 motion set" does not occur anywhere in the built tree; the nearest wording cites **fix #17** as its source and immediately defines the set as M1–M6, i.e. the M1–M6 rules ARE the definition, per the spec. It is not a bare citation to a nonexistent source. Not a finding.
- Loose spaced-dash probe `30 ?[–—-] ?34` matches only SVG path coordinate pairs (e.g. `-30 -34`) inside `skills/design-taste-frontend/assets/components/fx-map/sample-map.json` map geometry — not a band. Not a finding.

## 4. build.sh banned-term exception inventory — re-derived, delta 0

Total banned-term lines in `build.sh`: **798** — identical to fix16's inventory.

| Class | Count | Meaning | Ships a banned term? |
|---|---:|---|---:|
| (a) OLD-side match pattern | 389 | Upstream text / regex the build patches *away from* | No |
| (b) Comment / build log | 52 | Bash comments + Python comments + `print` log strings | No |
| (c1) NEW-side patch text | 355 | Replacement text written into the tree mid-build by the audit-fix heredocs; rewritten/removed by fix16 (final tree grep = 0) | No |
| (c2) Heredoc file write | 0 | No banned-term hit inside any `cat >` / `cat >>` file-write heredoc | — |
| (c3) Build-time source path | 2 | `:265` `cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" …`, `:298` `cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" …` (verified still at those lines) | No — upstream-layout paths, not shipped text |
| **Total** | **798** | | **0 live pins; 0 shipped banned terms** |

**Delta vs fix16 (798 = 389/52/355/0/2): 0 in every class. No new exception class.**

Method (independent re-derivation, not a copy of the old numbers):
1. Grepped `build.sh` and `build.sh.before-fix17` with the same 7-term case-insensitive pattern: both yield 798 hits.
2. Sorted content diff (line numbers stripped) of the two hit sets: **IDENTICAL** — the fix17 block added zero banned-term lines.
3. Line-number set of the 798 current hits is **identical** to the 798 line numbers in the sweep #18 classified table (`fix16/sweep18-report.md`, "Full build.sh inventory table", 798 rows).
4. Text check: every one of the 798 table rows matches the current `build.sh` line at that number (whitespace/backslash-escaping normalized, table's 150-char truncation respected) — **0 mismatches**.
5. Therefore the sweep #18 class assignments (a=389, b=52, c1=355, c2=0, c3=2) carry over exactly; no re-classification drift is possible on an identical line set.

Per-term line counts (a line can carry >1 term) — identical to sweep #18's re-derived numbers: `claude` 701 lines / 930 occurrences, `codex` 103/126, `anthropic` 5/8, `opus` 22/26, `sonnet` 23/24, `haiku` 13/13, `composer-2.5` 0/0.

Fix17 block check: lines 23212–23264 (`# --- fix17: back-port ALL Campus Eats render feedback …`) contain **0 banned-term hits** and **0 grok/model pins**. The fix17 block added no live pins and no new exception class.

## 5. Fix17 addition exactness — no wording drift

Extracted each rule paragraph from the built tree and compared md5s (Python, exact-string comparison).

| Rule | Placements | Length | md5 | Identical? |
|---|---|---:|---|---|
| E1 ("Push boundaries — be trailblazing, not dumb") | Taste `skills/design-taste-frontend/SKILL.md:254` | 1724 | `e9d210257261` | ✅ all 4 |
| E1 | orchestrate `skills/orchestrate/SKILL.md:94` | 1724 | `e9d210257261` | ✅ |
| E1 | orch-build-mvp `skills/orch-build-mvp/SKILL.md:42` | 1724 | `e9d210257261` | ✅ |
| E1 | ui-ux-pro-max `skills/ui-ux-pro-max/SKILL.md:97` | 1724 | `e9d210257261` | ✅ |
| STATIC_CHECKS ("Fix #17 static checks…") | Taste `skills/design-taste-frontend/SKILL.md:302` | 1471 | `a1dc22d6bf33` | ✅ all 3 |
| STATIC_CHECKS | orchestrate `skills/orchestrate/SKILL.md:61` | 1471 | `a1dc22d6bf33` | ✅ |
| STATIC_CHECKS | orch-build-mvp `skills/orch-build-mvp/SKILL.md:53` | 1471 | `a1dc22d6bf33` | ✅ |
| M1 ("Scroll entrances…") | motion-patterns `skills/motion-patterns/SKILL.md:55` | 946 | `27d0b7e7491d` | ✅ both |
| M1 | motion-foundations `skills/motion-foundations/SKILL.md:60` | 946 | `27d0b7e7491d` | ✅ |
| M2 ("1500ms fail-safe…") | motion-patterns `skills/motion-patterns/SKILL.md:56` | 895 | `f6442f49b761` | ✅ both |
| M2 | motion-foundations `skills/motion-foundations/SKILL.md:61` | 895 | `f6442f49b761` | ✅ |

Cross-check against the staged source: built E1 md5 `e9d210257261` == `fix17/fix17.py` `E1_RULE` md5; built STATIC_CHECKS md5 `a1dc22d6bf33` == `fix17/fix17.py` `STATIC_CHECKS` md5; M1/M2 match `fix17/fix17.py` `M1_RULE` (`fix17.py:85`) / `M2_RULE` (`fix17.py:87`) text as placed at `fix17.py:238,246`. No wording drift anywhere.

Note: an early extraction of the orchestrate STATIC_CHECKS paragraph over-captured (the paragraph sits mid-bullet, so a naive `\n\n` terminator ran past it); the bounded extraction (lead boldface through "a floor/ban break blocks.") gives the identical 1471-char paragraph in all three files. No drift — the over-capture was a tooling artifact, verified and discarded.

## Summary

- Banned terms in built tree: **0**
- Wrong pins / bracket syntax / `effort=` keys / version-suffix residue: **0**
- Fix17 residues (E1 permission wording, 30–34 band, SPEC-draft reference, bare "v4 motion set"): **0**
- build.sh exception inventory: **798 = 389 OLD-side + 52 comment/log + 355 NEW-side transient + 0 heredoc + 2 build-time paths; delta vs fix16 = 0; fix17 block added 0 hits, 0 pins, no new class**
- Exactness: E1 identical ×4, STATIC_CHECKS identical ×3, M1/M2 identical ×2 — all match `fix17/fix17.py` source constants
- `verify17.py` re-run: **59/59 pass**

**Verdict: CLEAN — 0 blocking, 0 minor.**
