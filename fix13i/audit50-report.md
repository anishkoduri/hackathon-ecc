# Audit #50 — fix round #13i — REPORT

## Verdict: ZERO ERRORS

- **Blocking: 0**
- **Minor: 0**
- All 12 fix #13i items (1 blocking + 11 minor) verified present and correct in the built tree, with file:line evidence below.
- Cross-check: `fix13i/verify13i.py` re-run — **63/63 pass**.
- Independent audit script: `/tmp/audit50.py` — **87/87 checks pass** (after correcting 3 of my own first-pass expectations against the actual lines; see "Expectations corrected" — the tree was not changed).

## Build identity (verified first)

- `~/workspace/hackathon-plugin/build.sh`: **23,117 lines**, md5 `cb12ab81c3334dba68054ba18c1d4f15` — matches the task statement.
- Built-tree manifest `fix13i/manifest1.txt`: `eecb5315311c70d9675951db4b37ff7f`; `manifest1.txt` vs `manifest2.txt` diff = 0 (two clean builds).
- Size: **57 MB**.
- Counts (recounted independently): **169 skills** (`skills/*/SKILL.md`), **72 agents**, **123 rules** (`.mdc`), **96 commands**, **15 hooks** (`.js` under `hooks/`, excluding `adapter.js`; `hooks/` also holds `adapter.js` + `hooks.json`).
- `fix13i/build-patch-i.txt`: 58 lines, 9 subs, placed last before STEP 5 (after the fix13h block); contains **0** occurrences of "ask the user" / "approval gate" / "wait for" — no new gate, wait point, or user question introduced.

## Method

Read-only audit. Independent Python script (`/tmp/audit50.py`, kept out of the plugin tree) plus direct line reads of every file cited. No finding rests on `verify13i.py`; it was re-run only as a cross-check.

Process note: the first version of my script hung twice — root cause was quadratic string concatenation (`whole += ...` over ~50 MB of tree text), not the tree. Fixed with list-join; the full run then took ~9 s. Nothing in the plugin tree was touched.

## (1) Every fix #13i item — present and correct

### B1 — whole-tree snapshot excludes live run state; revert never restores it

`skills/orchestrate/SKILL.md:60` and `skills/orch-build-mvp/SKILL.md:53` (both engines, same wording):

- Snapshot: "copy the whole tree, except `.hackathon/` and `.hallmark/candidate-evidence.md`, to `.hackathon/redesign-snapshot/<redesign-id>/`" — both paths excluded in both engines.
- Reasons stated: "The exclusions have two reasons: the snapshot directory lives inside the tree being copied, so a literal whole-tree copy would copy the snapshot into itself; and `.hackathon/` and `.hallmark/candidate-evidence.md` hold live run state, not tree state — the run ledger and the candidate-evidence markings are never snapshotted and never restored by a revert."
- Coverage: excluded paths "are never in the manifest by design and are never a coverage failure."
- Revert (1): excluded paths "are NEVER overwritten by a revert, so the ledger's `fresh-verdict rounds used: N/2` line and the `Superseded by redesign <redesign-id> — do not re-judge` markings survive a revert as written."
- Revert (2): delete redesign-created files "other than the excluded run-state paths (`.hackathon/`, `.hallmark/candidate-evidence.md`), which are never deleted."
- Revert (3): "the ledger's `fresh-verdict rounds used: N/2` line is untouched by the revert — run state is never restored — so the round spent on the failed re-verification stays spent."
- Revert (4): keep the deploy/commit hold.
- `git checkout` hits (orchestrate:60, mvp:53) are the explanatory warning only: "never from version control alone (`git checkout` restores HEAD, not the verified state, and never deletes untracked files…)" — **not re-flagged**, per parent note.

### DR-M3 — redesign-id uniqueness (both engines, :60 / :53)

"Two redesigns never share an id: if a snapshot directory or a `re-verification <redesign-id>:` ledger entry with that id already exists, append `-2`, `-3`, … until the id is unused."

### DR-M4 — git-status no-repo fallback (both engines, :60 / :53)

"when the tree has no repo, verify against the snapshot manifest alone — each restored path diffed against its snapshot copy and its recorded hash — the manifest check is the fallback and the authority, `git status` is only a convenience."

### DR-M5 — fresh-verdict budget initialized to 0/2 (both engines, :60 / :53)

`fresh-verdict rounds used: 0/2` present; the round-definition text states the line is created at ledger creation (Gate 1, before Verification) and created as `0/2` before spending if missing.

### M1 — polish.md link fixes

`skills/polish-pass/reference/polish.md:18,19,39,40` — all five `reference/…` links now prefix-free, read directly:
- :18 `[impeccable-detector-rules.json](impeccable-detector-rules.json)`; :19 `[impeccable-critique.md](impeccable-critique.md)`; :39 `[impeccable-craft-floor.md](impeccable-craft-floor.md)`; :40 `[impeccable-onboard.md](impeccable-onboard.md)` and `[impeccable-extract.md](impeccable-extract.md)`.
- Zero hits for `reference/impeccable-detector-rules.json`, `reference/impeccable-critique.md`, `reference/impeccable-craft-floor.md`, `reference/impeccable-onboard.md`, `reference/impeccable-extract.md` in polish.md.
- `skills/polish-pass/SKILL.md:92` correctly keeps its `reference/` prefix (verified present).

### DR-M1 — 5c/step-6 pointer (orchestrate:60)

"the 5c and step-6 checks below" present; old wording "the 5c/Verify-step-6 checks below" 0 hits.

### DR-M2 — Verify step 4a/4b (orchestrate:187, :191)

"Verify step 4a" (blind UI reviewer) at :187, "Verify step 4b" (adversarial audit) at :191; bare "Verify step 4" (not followed by a/b) 0 hits in orchestrate.

### DR-M6 — detector icon-tile-stack carve-out (polish.md:49)

"a template-pattern finding (e.g. `icon-tile-stack`, rules.json:175) is appended to `.hallmark/candidate-evidence.md` and fixed only on `browser-qa`'s verdict; never rewrite a template pattern on the detector's say-so alone." Verified present at :49.

### DR-M7 — duplicated ledger sentence removed (orchestrate:195, mvp:49)

"after the run, the orchestrator records `fresh-verdict rounds used: N/2`" is **0 hits** in both engines; both step-6 fresh-run paragraphs now read "the round definition in 5b/6b states the ledger update, and the orchestrator consults that line before spending more."

### Sweep M1 — gates.md gate 68 (gates.md:225)

Appended: "The wireframe read is candidate evidence of a generated look, for `browser-qa` to weigh at a glance." (also present at :233, same gate text echoed in the gate's detail — both read, both consistent).

### Sweep M2 — review-finish first word + consumers

- `skills/design-taste-frontend/references/hallmark/references/review-finish.md:5`: "First line: one of `recapture` … `findings` (craft findings follow — a first viewport that fails the idea or the theme wholesale is named explicitly among them), `no-findings` … The first word is a craft status, not a ship/fix/rebuild verdict."
- Consumers updated: orchestrate:195 and mvp:49 — "Act on its first word (`recapture` / `findings` / `no-findings`)"; `gates.md:245` — "Send the recaptures back for one scoring round only when a finding names a first-viewport wholesale failure or a Floor gate" and stamp record `hero-review: findings · 4 findings · 4 resolved`.
- Old vocab gone: `recapture` / `rebuild` / `fix` and `ship` / `fix` first-word forms 0 hits in both engines.

### Sweep M3 — review-hero first word + consumer

- `skills/design-taste-frontend/references/hallmark/references/review-hero.md:5`: first line "`findings` or `no-findings`"; "The word is a craft status, not a ship/fix verdict."
- Consumer: `skills/design-taste-frontend/SKILL.md:314` — "Act on its first word (`no-findings` / `findings`) for the craft findings"; old "Act on its first word (`ship` / `fix`)" 0 hits.

## (2) Counts and build identity — clean

See "Build identity" above. All counts match the task statement exactly.

## (3) Frontmatter parses

All 169 skills + 72 agents + 123 rules parsed as YAML frontmatter with no errors and no missing frontmatter.

## (4) Internal markdown links resolve (file-relative)

- Excluding `node_modules/` (third-party dependencies, out of scope): **all links resolve** except 2 pre-existing template references, both outside fix #13i scope and intentional — see "Pre-existing observations", not findings.
- Inside `node_modules/`, 15 further unresolvable links exist in vendored dependency READMEs (e.g. `@iarna/toml`, `ajv`, `sql.js` docs) — third-party content, not plugin content, not flagged.

## (5) Supply-chain pins hold

All present in the built tree: playwright@1.65.0, CBM v0.12.1, remotion@4.0.542, ecc-universal@2.2.3, ccg-workflow@3.7.4, vercel@65.14.0, @railway/cli@5.71.0, supabase@3.1.0, supabase-js@2.119.0, ssr@0.12.7, impeccable@4.8.0, puppeteer-core@25.17.0, Hallmark SHA `7e213cb6feb4ef82733bd66a0600b2e54ca0994c`. **No `@latest` in `scripts/`**. OpenMontage `runtime-fetch.md` unpinned clone left as documented opt-in — not counted, per task.

## (6) SSML truth intact

- `skills/pitch-deck-video/SKILL.md:337,345`: break tags v2 family only, ceiling 3 s per break (`<break time="3.0s" />` is the ceiling; at most 3 s per break, one per line at most).
- `skills/pitch-deck-video/references/shots-reference.md:216`: v3/v4 models do not support break tags (unsupported).
- `skills/pitch-deck-video/SKILL.md:541`: "`eleven_turbo_v2_5` is deprecated, never select it."

## (7) Grok 4.7 High pin + picker instruction intact

- `skills/orch-build-mvp/SKILL.md:40` and `skills/orchestrate/SKILL.md:57`: design role pinned to `grok-4.7-high` (slug form only — never bracket syntax); "select Grok 4.7 High in Cursor's model picker before the first build, or the pin may silently fall back — file-level pin only, the live smoke test decides." Orchestrate:57 adds the setup-note clarification (pre-build setup, never pauses the build, never asks mid-build). Also `orchestrate/SKILL.md:86,154` carry the `grok-4.7-high` design-lead tier pin.

## (8) Posture, auto-approval, deferred-six intact

- "more, not bolder" posture present (both engines, :40 mvp / :57 orch — same sentence as the Grok pin).
- Auto-approval / auto-expansion wording present; expansion Phases 0–3 run "with no user approval gate" (orchestrate:52).
- Deferred-six END-ONLY carve-out present, including the `(END-ONLY — …)` em-dash form.

## (9) No new approval gate, wait point, or user question from fix #13i

- `build-patch-i.txt`: 0 hits for "ask the user" / "approval gate" / "wait for".
- All 12 items are wording/mechanics corrections inside existing steps; no new skill, agent, rule, command, or hook; counts unchanged from fix #13h.

## (10) Adjudicated design NOT re-flagged

Verified present but not flagged, as instructed: orch-pipeline "two human gates" wording; `hooks/adapter.js` live infrastructure; byte-identical assets; `scripts/lib/agent-emit-pi.js` dead code deliberate (file exists at `scripts/lib/`); description-only command frontmatter; qc_patch `ecc-code-reviewer` → `code-reviewer`; `--domain` plain search reference-only; montage/explainer ask-first opt-ins; `themes/terminal.md` material header; frontend-slides on-demand; direction lenses + live/generate decided out; `(END-ONLY — …)` em-dash form; `git checkout` warning text (see B1).

## Pre-existing observations (NOT findings — no action, outside fix #13i scope)

1. `skills/readme-writer/references/readme-template.md:62` — `![Demo screenshot](docs/screenshot.png)` has no such file in the tree. It is a template line explicitly marked `<!-- PLACEHOLDER: replace with your real screenshot path -->`; the template is a scaffold the agent fills in, not a resolvable doc link. Unchanged by fix #13i (0 hits for `screenshot.png` in both `build.sh` and `build.sh.before-fix13i` — the file is written from staged source).
2. `agents/ecc-opensource-packager.md:210` — `[LICENSE](LICENSE)` refers to a LICENSE file the agent generates as pipeline output (Step 5: Add LICENSE), not a repo file. Unchanged by fix #13i (same hit count in `build.sh.before-fix13i` and `build.sh`).

## Expectations corrected (audit-script fixes, not tree defects)

1. My script first expected the literal word "self-referential" in the snapshot rule; the actual wording is "a literal whole-tree copy would copy the snapshot into itself" — same meaning, verified in both engines.
2. My script first expected the literal phrase "never overwrites the live ledger"; the actual revert wording is "are NEVER overwritten by a revert" — verified in both engines.
3. My script first looked for `agent-emit-pi.js` under `hooks/`; it lives at `scripts/lib/agent-emit-pi.js` — present.
4. My script's first link check included `node_modules/` vendored READMEs; those are third-party dependency docs, excluded from the plugin link check.

## What remains

Nothing. Audit #50 is **ZERO ERRORS** — fix round #13i is complete and correct in the built tree. The loop's remaining gates are Dry-run #22 and the single-executor sweep (not this audit's scope).
