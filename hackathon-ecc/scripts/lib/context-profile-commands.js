'use strict';

const path = require('node:path');
const fs = require('node:fs');
const { createSourceReader } = require('./context-profile-support');

const COMMANDS = ['resolve', 'set', 'mode', 'status', 'rollback', 'recover', 'routing-index'];
const VALUE_FLAGS = ['--task-input', '--previous', '--expected-digest', '--state-root', '--expected-revision',
  '--target', '--selection', '--include', '--exclude'];

function parse(argv) {
  const args = argv.filter(arg => arg !== '--dry-run');
  const result = { command: args.shift(), include: [], exclude: [], json: false,
    dryRun: argv.includes('--dry-run') || process.env.ECC_DRY_RUN === '1', load: false };
  const seen = new Set();
  for (let index = 0; index < args.length; index++) {
    const arg = args[index];
    if (arg === '--json') result.json = true;
    else if (arg === '--load' && result.command === 'resolve') result.load = true;
    else if (VALUE_FLAGS.includes(arg)) {
      const value = args[++index];
      if (!value || (value.startsWith('-') && !(arg === '--task-input' && value === '-'))) throw new Error(`Missing value for ${arg}`);
      if (seen.has(arg) && !['--include', '--exclude'].includes(arg)) throw new Error(`Duplicate argument: ${arg}`);
      seen.add(arg);
      if (arg === '--include') result.include.push(value);
      else if (arg === '--exclude') result.exclude.push(value);
      else result[arg.slice(2)] = value;
    } else if (!arg.startsWith('-') && !result.profileId && ['resolve', 'set', 'mode'].includes(result.command)) result.profileId = arg;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  const taskCommand = result.command === 'resolve';
  const allowed = taskCommand
    ? ['--task-input', '--previous', '--expected-digest', '--state-root', '--target', '--selection', '--include', '--exclude']
    : result.command === 'set'
      ? ['--state-root', '--expected-revision', '--expected-digest', '--target', '--selection', '--include', '--exclude']
      : ['--state-root', ...(['rollback', 'mode'].includes(result.command) ? ['--expected-revision'] : [])];
  for (const flag of seen) if (!allowed.includes(flag)) throw new Error(`${flag} is unavailable for ${result.command}`);
  if (taskCommand && !result['task-input']) throw new Error(`${result.command} requires --task-input`);
  if (!taskCommand && !result['state-root']) throw new Error(`${result.command} requires --state-root`);
  if (result.command === 'mode' && !['auto', 'manual', 'suggest'].includes(result.profileId)) throw new Error('Choose mode auto, manual, or suggest');
  if (taskCommand && result['state-root']
    && (result.profileId || [...seen].some(flag => ['--target', '--selection', '--include', '--exclude'].includes(flag)))) {
    throw new Error('Stored profile resolution cannot override its profile, mode, target or exclusions');
  }
  if (result['expected-revision'] !== undefined && !/^(0|[1-9][0-9]*)$/.test(result['expected-revision'])) {
    throw new Error('Expected revision must be a nonnegative integer');
  }
  return result;
}

function readInput(file) {
  if (file === '-') {
    const bytes = Buffer.alloc(65537);
    let length = 0;
    while (length < bytes.length) {
      const count = fs.readSync(0, bytes, length, bytes.length - length, null);
      if (!count) break;
      length += count;
    }
    if (length > 65536) throw new Error('Task input exceeds the 65536-byte limit');
    const content = bytes.subarray(0, length);
    const text = content.toString('utf8');
    if (!Buffer.from(text).equals(content) || text.includes('\0')) throw new Error('Task input must be UTF-8 JSON without NUL');
    try { return JSON.parse(text); } catch { throw new Error('Task input must be valid JSON'); }
  }
  const absolute = path.resolve(file);
  const resource = createSourceReader(path.dirname(absolute)).read(path.basename(absolute));
  if (resource.bytes > 65536) throw new Error('Task input exceeds the 65536-byte limit');
  try { return JSON.parse(resource.content.toString('utf8')); }
  catch { throw new Error('Task input must be valid JSON'); }
}

function execute(options) {
  if (options.command === 'resolve') {
    const { resolveTaskContext } = require('./context-selection');
    const stored = options['state-root']
      ? require('./context-profile-store').getStoreStatus({ stateRoot: options['state-root'] }) : null;
    if (stored && (!stored.configured || stored.recoveryRequired)) throw new Error('Configure or recover the stored profile before resolving');
    if (stored) {
      const carrier = require('./context-carriers').planContextCarrier({ profileId: stored.profileId,
        target: stored.target, selectionMode: stored.selectionMode, include: stored.include, exclude: stored.exclude });
      if (carrier.carrierDigest !== stored.carrierDigest) throw new Error('Stored profile source is stale; preview and set the current generation before resolving');
    }
    const input = { task: readInput(options['task-input']),
      profileId: stored?.profileId || options.profileId || 'lean@1', target: stored?.target || options.target || 'cursor',
      selectionMode: stored?.selectionMode || options.selection || 'auto', include: stored?.include || options.include,
      exclude: stored?.exclude || options.exclude,
      load: options.load && !options.dryRun,
      previous: options.previous ? readInput(options.previous) : null,
      expectedDigest: options['expected-digest'] || null };
    return { selection: resolveTaskContext(input) };
  }
  if (options.command === 'routing-index') {
    const routing = require('./context-routing-index');
    return { routing: options.dryRun ? routing.routingIndexStatus(options['state-root'])
      : routing.writeRoutingIndex({ stateRoot: options['state-root'] }) };
  }
  const store = require('./context-profile-store');
  const common = { stateRoot: options['state-root'],
    ...(options['expected-revision'] === undefined ? {} : { expectedRevision: Number(options['expected-revision']) }) };
  if (options.command === 'status') return { store: store.getStoreStatus(common) };
  if (options.command === 'mode') {
    const current = store.getStoreStatus(common);
    if (!current.configured || current.recoveryRequired) throw new Error('Configure or recover the stored profile before changing mode');
    const input = { ...common, expectedRevision: common.expectedRevision ?? current.revision,
      profileId: current.profileId, target: current.target, include: current.include, exclude: current.exclude,
      selectionMode: options.profileId };
    return { store: options.dryRun ? store.previewStore(input) : store.applyStore(input) };
  }
  if (options.command === 'rollback' || options.command === 'recover') {
    if (options.dryRun) return { store: store.getStoreStatus(common), dryRun: true };
    return { store: options.command === 'rollback' ? store.rollbackStore(common) : store.recoverStore(common) };
  }
  const input = { ...common, profileId: options.profileId || 'lean@1', target: options.target || 'cursor',
    selectionMode: options.selection || 'auto', include: options.include, exclude: options.exclude,
    ...(options['expected-digest'] ? { expectedCarrierDigest: options['expected-digest'] } : {}) };
  return { store: options.dryRun ? store.previewStore(input) : store.applyStore(input) };
}

function run(argv) {
  const options = parse(argv);
  const value = execute(options);
  return { schemaVersion: 'ecc.profile-operation.v1', status: 'success',
    summary: options.command === 'resolve' ? 'Task context resolved within the selected profile.'
      : options.command === 'routing-index' ? 'Routing index inspected. Prompt suggestions stay advisory; resolve verifies sources before loading.'
      : 'Managed profile generation inspected. Native activation is a separate provider boundary.',
    activation: value.selection?.activation || 'unobserved', next_actions: [], artifacts: [], ...value };
}

module.exports = { COMMANDS, run };
