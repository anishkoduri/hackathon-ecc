#!/usr/bin/env node
const { hookEnabled, readStdin, runExistingHook, transformToHookPayload } = require('./adapter');
readStdin().then(raw => {
  try {
    const input = JSON.parse(raw);
    const hookInput = transformToHookPayload(input, {
      tool_input: { file_path: input.file_path || input.path || input.file || '' }
    });
    const hookStr = JSON.stringify(hookInput);

    // Accumulate edited paths for batch format+typecheck at stop time.
    if (hookEnabled('post:edit:accumulator', ['standard', 'strict'])) {
      runExistingHook('post-edit-accumulator.js', hookStr);
    }
    if (hookEnabled('post:edit:console-warn', ['standard', 'strict'])) {
      runExistingHook('post-edit-console-warn.js', hookStr, { forwardStderr: true });
    }
    if (hookEnabled('post:edit:design-quality-check', ['standard', 'strict'])) {
      runExistingHook('design-quality-check.js', hookStr, { forwardStderr: true });
    }
  } catch {
    // Cursor post-event hooks fail open on malformed or partial payloads.
  }
  process.stdout.write(raw);
}).catch(() => process.exit(0));
