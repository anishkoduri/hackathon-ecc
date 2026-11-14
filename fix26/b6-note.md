# §5 — Trigger router B6 (fix #26)

## Verdict: DOCUMENTATION-ONLY

`manifests/context-packs/skill-triggers@1.json` is a documentation-only
reference table — which skill answers which user phrasing — not a live
routing table. No live consumer exists in the built tree. The file stays
maintained as a reference; nothing is wired.

This closes the fix #25 MANIFEST §5 open item ("maintain or
documentation-only?") and the wiring-list §E parent decision. The live
smoke test cannot clear this (there is no Cursor event to fire it) and
was not relied on.

## Evidence (all greps run in the built tree `hackathon-ecc/`)

### (1) All 64 keys resolve to real skill dirs

`manifests/context-packs/skill-triggers@1.json` holds 64 keys under its
`triggers` object, all of the form `skill:<name>`. Stripping the prefix,
every name resolves to `skills/<name>/`:

- trigger keys: 64
- unresolved (missing skill dir): none
- keys without the `skill:` prefix: none

### (2) Trigger-only count 0

`fix25/callmap/call-map-data.json` has `"trigger_only": []` (empty), and
the staged call map's "Trigger-only" section reads "0 elements called
only via trigger keys". No skill depends solely on a trigger key.

### (3) The consumer chain — real code, dead end

- `scripts/lib/context-pack-registry.js:12` defines
  `TRIGGERS_PATH = 'manifests/context-packs/skill-triggers@1.json'`, and
  `loadSkillTriggers` reads it (`:130–142`).
- `scripts/lib/context-selection.js:4` requires `./context-pack-registry`
  (`loadSkillTriggers`) and calls it at `:315` and `:340`.
- `scripts/lib/context-selection.js` is required only by:
  - `scripts/lib/context-profile-commands.js:75` (lazy `require` inside a
    function — `resolveTaskContext`), and
  - `scripts/lib/context-routing-index.js:10` and `:99`.
- `scripts/lib/context-profile-commands.js` has NO requirers anywhere in
  the tree (grep over `*.js` / `*.mjs` / `*.md` / `*.json`, excl.
  `node_modules`) — that branch is dead.
- `scripts/lib/context-routing-index.js` is required only by the two
  `scripts/hooks` consumers below — see (4).
- No `package.json` / `bin` entry point and no test file references
  `context-selection`, `context-routing-index`, or `loadSkillTriggers`.

### (4) hooks/*.js — no hook invokes the chain

- `grep -rn "context-" hooks/*.js` → 0 hits.
- The 15 registered hooks (`hooks/hooks.json`) invoke, via
  `runExistingHook`, only: `cursor-session-env.js`, `session-start.js`,
  `session-end-marker.js`, `evaluate-session.js`, `post-edit-accumulator.js`,
  `post-edit-console-warn.js`, `design-quality-check.js`,
  `post-edit-format.js`, `block-no-verify.js`,
  `pre-bash-dev-server-block.js`, `pre-compact.js`. Neither
  `context-routing-index.js` nor `context-prompt-suggestions.js` is among
  them, and no `hooks/*.js` file requires anything under `scripts/lib/`
  (only `./adapter`).
- `scripts/hooks/session-start.js`, `session-start-bootstrap.js`,
  `plugin-hook-bootstrap.js`, `lifecycle-hook-bootstrap.js` contain zero
  references to `context-routing`, `context-selection`, `skill-triggers`,
  or `context-pack`.
- `scripts/hooks/context-routing-index.js` (header: "SessionStart hook
  (register with \"async\": true)") is NOT registered: `hooks.json`
  `sessionStart` runs only `node hooks/session-start.js`, which runs
  `cursor-session-env.js` + `scripts/hooks/session-start.js` — never the
  routing-index builder.
- The only references to `context-prompt-suggestions` /
  `context-routing-index` by name anywhere are the call-map B6 bullet
  itself and `context-profile-commands.js:94` (which requires the lib
  file, and itself has no requirers).

### (5) `scripts/hooks/context-prompt-suggestions.js` header — upstream-only confirmed

Lines 4–10:

> `UserPromptSubmit hook — Upstream-only (not wired in this Cursor plugin — Cursor has no UserPromptSubmit event): suggest up to three skills from the managed profile's routing index. ...`

It requires `../lib/context-routing-index` at `:53`, but nothing invokes
the file itself (see (4)).

## Change made

- Staged call map `new-skills/orchestrate/references/call-map.md:38` (B6
  bullet): reworded to record the disposition — "fix #26:
  DOCUMENTATION-ONLY" — and to state the file is a documentation-only
  reference table, not a live routing table, with a pointer to this note.
  One line edited in place; no other call-map line touched.

## Follow-up for the coordinator (not done here — out of this task's scope)

The B6 bullet in the staged call map is generator-templated:
`fix25/callmap/generate_call_map.py:753–761` emits the same text. A
generator re-run will overwrite the `:38` hand edit unless the template
is updated to match. The generator template (and the per-element
"on-request (trigger-routed; no live Cursor entry — see method note B6)"
flow strings at `:597`, `:609`) should be updated to the
DOCUMENTATION-ONLY wording, or the disposition recorded where the
generator reads it.
