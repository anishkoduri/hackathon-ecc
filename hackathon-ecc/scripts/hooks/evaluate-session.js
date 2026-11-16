#!/usr/bin/env node
/**
 * Session Evaluator
 *
 * Cross-platform (Windows, macOS, Linux)
 *
 * Runs on Stop hook. Pattern extraction was removed with the
 * continuous-learning skills (fix #27); the evaluator now only enforces
 * the minimum session length and exits.
 * Reads transcript_path from stdin JSON (Cursor hook input).
 *
 * Why Stop hook instead of UserPromptSubmit:
 * - Stop runs once at session end (lightweight)
 * - UserPromptSubmit runs every message (heavy, adds latency)
 */

const fs = require('fs');
const {
  getLearnedSkillsDir,
  ensureDir,
  countInFile,
  log
} = require('../lib/utils');

// Read hook input from stdin (Cursor provides transcript_path via stdin JSON)
const MAX_STDIN = 1024 * 1024;
let stdinData = '';
process.stdin.setEncoding('utf8');

process.stdin.on('data', chunk => {
  if (stdinData.length < MAX_STDIN) {
    const remaining = MAX_STDIN - stdinData.length;
    stdinData += chunk.substring(0, remaining);
  }
});

process.stdin.on('end', () => {
  main().catch(err => {
    console.error('[SessionEvaluator] Error:', err.message);
    process.exit(0);
  });
});

async function main() {
  // Parse stdin JSON to get transcript_path
  let transcriptPath = null;
  try {
    const input = JSON.parse(stdinData);
    transcriptPath = input.transcript_path;
  } catch {
    // Fallback: try env var for backwards compatibility
    transcriptPath = process.env.ECC_TRANSCRIPT_PATH;
  }

  // Default configuration (the continuous-learning skill that owned the
  // config file was cut in fix #27, so defaults always apply — EVALSESS_F28)
  let minSessionLength = 10;
  let learnedSkillsPath = getLearnedSkillsDir();

  // Ensure learned skills directory exists
  ensureDir(learnedSkillsPath);

  if (!transcriptPath || !fs.existsSync(transcriptPath)) {
    process.exit(0);
  }

  // Count user messages in session (allow optional whitespace around colon)
  const messageCount = countInFile(transcriptPath, /"type"\s*:\s*"user"/g);

  // Skip short sessions
  if (messageCount < minSessionLength) {
    log(`[SessionEvaluator] Session too short (${messageCount} messages), skipping`);
    process.exit(0);
  }


  process.exit(0);
}
