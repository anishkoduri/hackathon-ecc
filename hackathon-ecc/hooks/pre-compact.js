#!/usr/bin/env node
const { readStdin, runExistingHook, transformToHookPayload, hookEnabled } = require('./adapter');
readStdin().then(raw => {
  try {
    const hookInput = JSON.parse(raw || '{}');
    if (hookEnabled('pre:compact', ['standard', 'strict'])) {
      runExistingHook('pre-compact.js', transformToHookPayload(hookInput));
    }
  } catch {
    // PreCompact is advisory; malformed payloads fail open.
  }
  process.stdout.write(raw);
}).catch(() => process.exit(0));
