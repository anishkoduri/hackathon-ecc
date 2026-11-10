#!/usr/bin/env node
/**
 * Backward-compatible doc warning hook entrypoint — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event).
 * Kept for consumers that still reference pre-write-doc-warn.js directly.
 */

'use strict';

// doc-file-warning.js guards its stdin entrypoint behind require.main; call main() explicitly.
require('./doc-file-warning.js').main();
