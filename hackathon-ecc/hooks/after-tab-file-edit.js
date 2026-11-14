#!/usr/bin/env node
const { readStdin, runExistingHook, transformToHookPayload, hookEnabled } = require('./adapter');
readStdin().then(raw => {
  if (!hookEnabled('post:tab-edit:format', ['standard', 'strict'])) {
    process.stdout.write(raw);
    return;
  }
  try {
    const input = JSON.parse(raw);
    const hookInput = transformToHookPayload(input, {
      tool_input: { file_path: input.file_path || input.path || input.file || '' }
    });
    runExistingHook('post-edit-format.js', JSON.stringify(hookInput));
  } catch {
    // Formatting is advisory, so malformed payloads fail open.
  }
  process.stdout.write(raw);
}).catch(() => process.exit(0));
