#!/usr/bin/env node
const {
  hookEnabled,
  mergeSessionStartOutputs,
  normalizeSessionStartOutput,
  readStdin,
  runExistingHook,
  transformToHookPayload,
} = require('./adapter');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
readStdin().then(raw => {
  let input = {};
  try {
    const parsed = JSON.parse(raw || '{}');
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      input = parsed;
    }
  } catch {
    // The Cursor env helper handles malformed input and supplies a safe default.
  }
  const transformedInput = transformToHookPayload(input);
  const hookInput = {
    ...transformedInput,
    hook_event_name: 'SessionStart',
    source: 'startup',
  };
  let outputs = [];
  if (!hookEnabled('session:start', ['minimal', 'standard', 'strict'])) {
    process.stdout.write(JSON.stringify({}));
    return;
  }

  const envResult = runExistingHook('cursor-session-env.js', raw, {
    forwardStderr: true,
  });
  if (envResult && envResult.status === 0 && envResult.stdout) {
    try {
      outputs = [...outputs, normalizeSessionStartOutput(envResult.stdout)];
    } catch {
      console.error('[Cursor Hook] Ignoring invalid Cursor session environment output');
    }
  }

  const sessionEnv = outputs[0]?.env || {};
  const sessionResult = runExistingHook('session-start.js', hookInput, {
    env: {
      ...sessionEnv,
      ...(transformedInput.session_id
        ? { ECC_SESSION_ID: transformedInput.session_id }
        : {}),
    },
    forwardStderr: true,
  });
  if (sessionResult && sessionResult.status === 0 && sessionResult.stdout) {
    try {
      outputs = [
        ...outputs,
        normalizeSessionStartOutput(sessionResult.stdout, { shared: true }),
      ];
    } catch {
      console.error('[Cursor Hook] Ignoring invalid shared SessionStart output');
    }
  }
  // fix #25 §1: ck (Context Keeper) SessionStart brief — the ck skill's
  // SessionStart hook (skills/ck/hooks/session-start.mjs) has no other
  // caller in this plugin; run it here so its brief reaches the session.
  // The .mjs is ESM (run it with node directly — runExistingHook only
  // resolves scripts/hooks/*) and reads stdin JSON ({session_id});
  // hookInput carries session_id (adapter transformToHookPayload).
  // It prints {additionalContext} (camelCase); normalize only reads
  // additional_context (snake_case), so convert before merging through
  // the same outputs array. Fail-soft throughout: a missing hook, a
  // non-zero exit, or unparsable output is a stderr note, never a broken
  // session start. Inherits the session:start gate above (disabling
  // session:start disables ck too).
  try {
    const ckHook = path.join(__dirname, '..', 'skills', 'ck', 'hooks', 'session-start.mjs');
    if (fs.existsSync(ckHook)) {
      const ckResult = spawnSync(process.execPath, [ckHook], {
        input: JSON.stringify(hookInput),
        stdio: ['pipe', 'pipe', 'pipe'],
        encoding: 'utf8',
        timeout: 15000,
        cwd: process.cwd(),
      });
      if (ckResult && ckResult.status === 0 && ckResult.stdout) {
        try {
          const ckJson = JSON.parse(ckResult.stdout);
          if (typeof ckJson.additionalContext === 'string' && ckJson.additionalContext) {
            outputs = [...outputs, { additional_context: ckJson.additionalContext }];
          }
        } catch {
          console.error('[Cursor Hook] Ignoring invalid ck SessionStart output');
        }
      } else if (ckResult && ckResult.error) {
        console.error('[Cursor Hook] ck SessionStart hook failed: ' + ckResult.error.message + '; continuing');
      } else if (ckResult && Number.isInteger(ckResult.status) && ckResult.status !== 0) {
        console.error('[Cursor Hook] ck SessionStart hook exited with code ' + ckResult.status + '; continuing');
      }
    }
  } catch {
    console.error('[Cursor Hook] ck SessionStart hook skipped');
  }
  process.stdout.write(JSON.stringify(mergeSessionStartOutputs(outputs)));
}).catch(() => process.exit(0));
