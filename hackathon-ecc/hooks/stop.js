#!/usr/bin/env node
const {
  createStopFormatTypecheckOptions,
  hookEnabled,
  readStdin,
  runExistingHook,
  transformToHookPayload,
} = require('./adapter');
readStdin().then(raw => {
  const input = JSON.parse(raw || '{}');
  const hookInput = transformToHookPayload(input);
  const sharedOptions = {
    env: hookInput.session_id
      ? { ECC_SESSION_ID: hookInput.session_id }
      : {},
  };

  if (hookEnabled('stop:session-end', ['minimal', 'standard', 'strict'])) {
    runExistingHook('session-end.js', hookInput, sharedOptions);
  }
  if (hookEnabled('stop:evaluate-session', ['minimal', 'standard', 'strict'])) {
    runExistingHook('evaluate-session.js', hookInput, sharedOptions);
  }
  if (hookEnabled('stop:format-typecheck', ['standard', 'strict'])) {
    runExistingHook(
      'stop-format-typecheck.js',
      hookInput,
      createStopFormatTypecheckOptions(sharedOptions.env)
    );
  }
  if (hookEnabled('stop:check-console-log', ['standard', 'strict'])) {
    runExistingHook('check-console-log.js', hookInput, {
      ...sharedOptions,
      forwardStderr: true,
    });
  }

  process.stdout.write(raw);
}).catch(() => process.exit(0));
