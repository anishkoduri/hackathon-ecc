#!/usr/bin/env node
const { readStdin, runExistingHook, transformToHookPayload, hookEnabled } = require('./adapter');
readStdin().then(raw => {
  const input = JSON.parse(raw || '{}');
  const hookInput = transformToHookPayload(input);
  if (hookEnabled('session:end:marker', ['minimal', 'standard', 'strict'])) {
    runExistingHook('session-end-marker.js', hookInput);
  }
  process.stdout.write(raw);
}).catch(() => process.exit(0));
