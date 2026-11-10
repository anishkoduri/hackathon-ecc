#!/usr/bin/env node
/**
 * Hook-enabled check — Claude Code-only helper (not wired in this Cursor plugin — invoked only from Claude Code hook configurations).
 */
'use strict';

const { isHookEnabled } = require('../lib/hook-flags');

const [, , hookId, profilesCsv] = process.argv;
if (!hookId) {
  process.stdout.write('yes');
  process.exit(0);
}

process.stdout.write(isHookEnabled(hookId, { profiles: profilesCsv }) ? 'yes' : 'no');
