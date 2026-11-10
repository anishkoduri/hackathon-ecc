#!/usr/bin/env node
/**
 * Claude Code-only: PostToolUse bash-dispatch entry point (runPostBash).
 * Not wired in this Cursor plugin — it never runs (its only reference is the ASYNC_HOOKS list in the likewise unwired scripts/hooks/posttooluse-dispatcher.js).
 */
'use strict';

const { runPostBash } = require('./bash-hook-dispatcher');

let raw = '';
const MAX_STDIN = 1024 * 1024;

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => {
  if (raw.length < MAX_STDIN) {
    const remaining = MAX_STDIN - raw.length;
    raw += chunk.substring(0, remaining);
  }
});

process.stdin.on('end', () => {
  const result = runPostBash(raw);
  if (result.stderr) {
    process.stderr.write(result.stderr);
  }
  process.stdout.write(result.output);
  process.exitCode = result.exitCode;
});
