'use strict';

const policy = require('./github-coordination/policy');
const parsing = require('./github-coordination/parsing');
const ghApi = require('./github-coordination/gh-api');
const state = require('./github-coordination/state');
const actions = require('./github-coordination/actions');
const store = require('./github-coordination/store');

module.exports = {
  DEFAULT_CONFIG_FILE: policy.DEFAULT_CONFIG_FILE,
  DEFAULT_CONFIG_PATH: policy.DEFAULT_CONFIG_PATH,
  DEFAULT_POLICY: policy.DEFAULT_POLICY,
  DEFAULT_SCHEMA_VERSION: policy.DEFAULT_SCHEMA_VERSION,
  loadPolicy: policy.loadPolicy,

  extractCoordinationState: parsing.extractCoordinationState,
  extractIssueReferences: parsing.extractIssueReferences,
  extractTasks: parsing.extractTasks,
  mergeIssueBody: parsing.mergeIssueBody,
  renderCoordinationState: parsing.renderCoordinationState,

  commentIssue: ghApi.commentIssue,
  editIssue: ghApi.editIssue,
  getIssue: ghApi.getIssue,
  listIssues: ghApi.listIssues,
  normalizeIssueNumber: ghApi.normalizeIssueNumber,
  normalizeLabels: ghApi.normalizeLabels,
  normalizeRepo: ghApi.normalizeRepo,
  runGh: ghApi.runGh,
  runGhJson: ghApi.runGhJson,

  buildIssueComment: state.buildIssueComment,
  buildIssueStateFromAction: state.buildIssueStateFromAction,
  defaultCoordinationState: state.defaultCoordinationState,
  desiredLabelsForState: state.desiredLabelsForState,
  getCoordinationState: state.getCoordinationState,
  mapStateToWorkItemStatus: state.mapStateToWorkItemStatus,
  slugifySegment: state.slugifySegment,
  summarizeStateForOutput: state.summarizeStateForOutput,
  syncIssueLabels: state.syncIssueLabels,
  verifyDependenciesClosed: state.verifyDependenciesClosed,

  applyClaim: actions.applyClaim,
  applyDecompose: actions.applyDecompose,
  applyPublish: actions.applyPublish,
  applyReview: actions.applyReview,
  applySync: actions.applySync,
  applyUnblock: actions.applyUnblock,
  applyValidate: actions.applyValidate,
  formatCollection: actions.formatCollection,
  formatSummary: actions.formatSummary,

  epicWorkItemId: store.epicWorkItemId,
  openStore: store.openStore,
  upsertCoordinationWorkItem: store.upsertCoordinationWorkItem,
};

// --- CLI dispatch (Audit #5, Fixer A) -------------------------------------
// The /epic-* commands document this invocation:
//   node scripts/lib/github-coordination.js <verb> ...
// This file is otherwise a pure CommonJS library (41 exports, no
// process.argv handling), so executed directly it exited 0 having done
// nothing. The dispatch below maps each verb to its exported apply*
// function. It is guarded by `require.main === module`, so requiring this
// file as a library has no side effects: no argv parsing, no `gh` calls,
// no state-store access, no output, no process exit.

const fs = require('fs');
const path = require('path');

const CLI_VERBS = {
  claim: { fn: actions.applyClaim, needsIssue: true },
  decompose: { fn: actions.applyDecompose, needsIssue: true },
  publish: { fn: actions.applyPublish, needsIssue: true },
  review: { fn: actions.applyReview, needsIssue: true },
  sync: { fn: actions.applySync, needsIssue: false },
  unblock: { fn: actions.applyUnblock, needsIssue: false },
  validate: { fn: actions.applyValidate, needsIssue: true },
};

function cliUsage() {
  return [
    'Usage: node scripts/lib/github-coordination.js <verb> [issue-number] --repo <owner/repo> [options]',
    '',
    'Verbs:',
    '  claim <issue-number>     --repo <owner/repo> [--actor <login>] [--branch <name>]',
    '                             [--status <status>] [--review <state>] [--validation <state>]',
    '  decompose <issue-number> --repo <owner/repo>',
    '  publish <issue-number>   --repo <owner/repo>',
    '  review <issue-number>    --repo <owner/repo> --review <approved|requested|changes-requested>',
    '  sync                     --repo <owner/repo> [--state <state>] [--limit <n>]',
    '  unblock                  --repo <owner/repo> [--limit <n>]',
    '  validate <issue-number>  --repo <owner/repo>',
    '',
    'Options:',
    '  --repo <owner/repo>      GitHub repository (required)',
    '  --actor, --owner <login> Claim owner (claim only)',
    '  --branch <name>          Branch for the claim (claim only)',
    '  --status <status>        Coordination status override (claim only)',
    '  --review <state>         Review state: approved, requested, changes-requested',
    '  --validation <state>     Validation state override (claim only)',
    '  --project-state <state>  Project state override (claim only)',
    '  --state <state>          Issue state filter for sync (default: all)',
    '  --limit <n>              Max issues to list (sync, unblock)',
    '  --config, --config-path <path>  Policy file (default: <cwd>/config/github-native-coordination.json)',
    '  --dry-run                Read and compute, but do not write to GitHub or the local cache',
    '  --no-store               Skip opening the local SQLite state store',
    '  --json                   Print the raw result as JSON instead of the formatted summary',
    '  -h, --help               Show this usage',
    '',
    'Requires the `gh` CLI to be installed and authenticated.',
  ].join('\n');
}

function parseCliArgs(argv) {
  const args = [...argv];
  if (args.length === 0) {
    throw new Error('no verb given');
  }
  if (args[0] === 'help' || args[0] === '-h' || args[0] === '--help') {
    return { help: true };
  }
  const verb = args.shift();
  const spec = CLI_VERBS[verb];
  if (!spec) {
    throw new Error(`unknown verb: ${verb}`);
  }
  const options = {};
  const positionals = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '-h' || arg === '--help') {
      return { help: true };
    }
    if (arg.startsWith('--')) {
      const eq = arg.indexOf('=');
      const name = eq === -1 ? arg.slice(2) : arg.slice(2, eq);
      const inlineValue = eq === -1 ? null : arg.slice(eq + 1);
      const takeValue = () => {
        if (inlineValue !== null) {
          return inlineValue;
        }
        if (i + 1 >= args.length) {
          throw new Error(`--${name} requires a value`);
        }
        return args[++i];
      };
      switch (name) {
        case 'repo':
          options.repo = takeValue();
          break;
        case 'actor':
        case 'owner':
          options.actor = takeValue();
          break;
        case 'branch':
          options.branch = takeValue();
          break;
        case 'status':
          options.status = takeValue();
          break;
        case 'review':
          options.review = takeValue();
          break;
        case 'validation':
          options.validation = takeValue();
          break;
        case 'project-state':
          options.projectState = takeValue();
          break;
        case 'config':
        case 'config-path':
          options.configPath = takeValue();
          break;
        case 'state':
          options.state = takeValue();
          break;
        case 'limit': {
          const limit = Number(takeValue());
          if (!Number.isFinite(limit) || limit <= 0) {
            throw new Error('--limit requires a positive number');
          }
          options.limit = Math.trunc(limit);
          break;
        }
        case 'dry-run':
          options.dryRun = true;
          break;
        case 'no-store':
          options.noStore = true;
          break;
        case 'json':
          options.json = true;
          break;
        default:
          throw new Error(`unknown option: --${name}`);
      }
    } else if (arg.startsWith('-') && arg !== '-') {
      throw new Error(`unknown option: ${arg}`);
    } else {
      positionals.push(arg);
    }
  }
  if (spec.needsIssue && positionals.length !== 1) {
    throw new Error(`${verb} requires exactly one <issue-number> argument`);
  }
  if (!spec.needsIssue && positionals.length > 0) {
    throw new Error(`${verb} takes no positional arguments, got: ${positionals.join(' ')}`);
  }
  return { verb, issueNumber: positionals[0] || null, options };
}

function printCliResult(verb, result, options) {
  if (options.json) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }
  if (verb === 'sync' || verb === 'unblock') {
    process.stdout.write(actions.formatCollection(result));
    return;
  }
  process.stdout.write(actions.formatSummary(result));
  if (verb === 'validate') {
    const lines = [`Valid: ${result.ok ? 'yes' : 'no'}`];
    for (const check of result.validations || []) {
      lines.push(`Check ${check.check}: ${check.ok ? 'ok' : 'FAILED'} (${check.detail})`);
    }
    if (result.missingDependencies && result.missingDependencies.length > 0) {
      lines.push(`Missing dependencies: ${result.missingDependencies.join(', ')}`);
    }
    process.stdout.write(`${lines.join('\n')}\n`);
  }
  if (verb === 'decompose' && typeof result.dependencyCount === 'number') {
    process.stdout.write(`Dependency references: ${result.dependencyCount}\n`);
  }
}

async function runCli(argv) {
  let parsed;
  try {
    parsed = parseCliArgs(argv);
  } catch (error) {
    process.stderr.write(`[github-coordination] ${error.message}\n\n${cliUsage()}\n`);
    return 2;
  }
  if (parsed.help) {
    process.stdout.write(`${cliUsage()}\n`);
    return 0;
  }
  const { verb, options } = parsed;
  if (!options.repo) {
    process.stderr.write(`[github-coordination] --repo <owner/repo> is required\n\n${cliUsage()}\n`);
    return 2;
  }
  const spec = CLI_VERBS[verb];
  let issueNumber = null;
  if (spec.needsIssue) {
    try {
      issueNumber = ghApi.normalizeIssueNumber(parsed.issueNumber);
    } catch (error) {
      process.stderr.write(`[github-coordination] ${error.message}\n`);
      return 2;
    }
  }

  // Open the local SQLite state store so the apply* functions can record
  // the coordination snapshot (their documented "local cache" step). The
  // store is optional: the actions tolerate a null store (upsert returns
  // null). Only open it when the store can actually accept a write: the
  // store validates work items against
  // <plugin-root>/schemas/state-store.schema.json (see
  // scripts/lib/state-store/schema.js), and that file IS shipped in
  // this plugin build. Opening the store anyway would fail later, inside
  // the apply* call — after the GitHub writes already landed — and turn a
  // successful verb into exit 1. So when the schema is absent, warn once
  // and continue without the local cache; the verbs still perform their
  // GitHub action and print their result.
  let storeInstance = null;
  if (options.noStore) {
    storeInstance = null;
  } else if (!fs.existsSync(path.join(__dirname, '..', '..', 'schemas', 'state-store.schema.json'))) {
    process.stderr.write('[github-coordination] Warning: local state store schema not found at <plugin-root>/schemas/state-store.schema.json; continuing without local cache.\n');
    storeInstance = null;
  } else {
    try {
      storeInstance = await store.openStore();
    } catch (error) {
      process.stderr.write(`[github-coordination] Warning: local state store unavailable (${error.message}); continuing without local cache.\n`);
      storeInstance = null;
    }
  }

  try {
    const context = { store: storeInstance };
    const result = spec.needsIssue
      ? spec.fn(options.repo, issueNumber, options, context)
      : spec.fn(options.repo, options, context);
    printCliResult(verb, result, options);
    return 0;
  } catch (error) {
    process.stderr.write(`[github-coordination] ${verb} failed: ${error.message}\n`);
    return 1;
  } finally {
    if (storeInstance && typeof storeInstance.close === 'function') {
      try {
        storeInstance.close();
      } catch (_error) {
        // A close failure must not mask the verb result.
      }
    }
  }
}

if (require.main === module) {
  runCli(process.argv.slice(2)).then(
    (code) => { process.exitCode = code; },
    (error) => {
      process.stderr.write(`[github-coordination] ${error.message}\n`);
      process.exitCode = 1;
    },
  );
}
