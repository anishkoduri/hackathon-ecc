---
description: Run the ECC formatter quality gate for a single file and report remediation steps.
---

# Quality Gate Command

Operator entry point for the formatter quality gate — manual run (`scripts/hooks/quality-gate.js`).

## How it actually works

The gate is a single-file formatter check driven by hook input, not CLI flags:

- The script reads the target from the hook's stdin JSON
  (`tool_input.file_path`); it does not take a path argument.
- Behavior toggles are environment variables:
  - `ECC_QUALITY_GATE_FIX=true` - apply formatting fixes instead of check-only
  - `ECC_QUALITY_GATE_STRICT=true` - log formatter failures as gate failures
- Coverage by file type:
  - `.ts/.tsx/.js/.jsx/.json/.md` - Biome `check` or Prettier `--check`,
    whichever the project ships (JS/TS under Biome is skipped here because
    JS/TS formatting happens at stop via `stop-format-typecheck.js`, which
    batch-formats accumulated edits; `post-edit-format` covers Tab edits only)
  - `.go` - `gofmt`
  - `.py` - `ruff format`
- Lint and type checks are not part of this gate. END-ONLY: only at the very end of the project or on explicit user ask, use the `verification-loop` skill for lint/type/test pipelines. The language verification skills run end-of-feature (before PR, after major refactoring, pre-deploy) — this gate does not defer them; only their security phases are END-ONLY. Mid-build, use `verification-before-completion` instead.

## Usage

To run the gate manually against one file, pipe hook-style JSON into the
script (set the env toggles first if you want fix or strict behavior):

```bash
echo '{"tool_input":{"file_path":"src/example.ts"}}' \
  | ECC_QUALITY_GATE_FIX=true node scripts/hooks/quality-gate.js
```

Then report formatter findings and concrete remediation steps.

## Notes

There is no automatic hook wiring for this gate in this plugin: the gate
is manually invoked as shown above. `hooks/hooks.json` registers Cursor
events only and has no entry that invokes `scripts/hooks/quality-gate.js`.
The `scripts/hooks/posttooluse-dispatcher.js` script does list a
`post:quality-gate` entry in its internal registry, but that dispatcher is
not referenced by `hooks/hooks.json` or anything else in the plugin, so it
never runs — do not rely on it. Run the gate manually when you need it.

## Arguments

$ARGUMENTS:

- `[path]` optional file to check. The script itself takes no CLI
  arguments - when a path is given, substitute it as `tool_input.file_path`
  in the stdin JSON shown above before running the command
