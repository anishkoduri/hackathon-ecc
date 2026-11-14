'use strict';

// Unreferenced cross-harness reference table: this file describes the
// UPSTREAM ECC repo layout, not this plugin's layout. The paths it cites
// (scripts/session-inspect.js, scripts/build-opencode.js,
// scripts/agent-convert.js, scripts/orchestration-status.js,
// scripts/observability-readiness.js,
// scripts/dsh/generate-hooks-config.js, tests/scripts/build-opencode.test.js,
// tests/scripts/dsh-generate-hooks-config.test.js,
// rules/common/,
// docs/architecture/cross-harness.md, .opencode/*, .pi/*, tests/lib/*,
// tests/pi/*) are upstream paths, not plugin paths, and most of those files
// are not shipped in this plugin. Do not treat the paths in the table below
// as files that exist here. Kept as reference only; nothing in the plugin
// requires this module.

const fs = require('fs');
const path = require('path');

const MATRIX_BLOCK_START = '<!-- harness-adapter-compliance:matrix-start -->';
const MATRIX_BLOCK_END = '<!-- harness-adapter-compliance:matrix-end -->';

const COMPLIANCE_STATES = Object.freeze({
  Native: 'ECC can install or verify the surface directly for this harness.',
  'Adapter-backed': 'ECC has a thin adapter, plugin, or package surface, but parity differs by harness.',
  'Instruction-backed': 'ECC can provide the guidance and files, but the harness does not expose the runtime hook/session surface ECC needs for enforcement.',
  'Reference-only': 'The tool is useful as a design pressure or external runtime, but ECC does not yet ship a direct installer or adapter for it.',
});

const REQUIRED_FIELDS = Object.freeze([
  'id',
  'harness',
  'state',
  'supported_assets',
  'unsupported_surfaces',
  'install_or_onramp',
  'verification_commands',
  'risk_notes',
  'last_verified_at',
  'owner',
  'source_docs',
]);

function freezeRecord(record) {
  return Object.freeze({
    ...record,
    supported_assets: Object.freeze(record.supported_assets.slice()),
    unsupported_surfaces: Object.freeze(record.unsupported_surfaces.slice()),
    install_or_onramp: Object.freeze(record.install_or_onramp.slice()),
    verification_commands: Object.freeze(record.verification_commands.slice()),
    risk_notes: Object.freeze(record.risk_notes.slice()),
    source_docs: Object.freeze(record.source_docs.slice()),
  });
}

const ADAPTER_RECORDS = Object.freeze([
  {
    id: 'cursor',
    harness: 'Cursor',
    state: 'Adapter-backed',
    supported_assets: [
      'Cursor rules',
      'project-local skills',
      'hook adapter',
      'shared scripts',
    ],
    unsupported_surfaces: ['Cursor hook events and rule loading differ from Cursor'],
    install_or_onramp: ['`./install.sh --profile minimal --target cursor`'],
    verification_commands: [
      '`node tests/lib/install-targets.test.js`',
      '`npm run harness:audit -- --format json`',
    ],
    risk_notes: ['Cursor adapters must preserve existing project rules and avoid silent overwrite.'],
    last_verified_at: '2026-05-12',
    owner: 'ECC maintainers',
    source_docs: [
      '.cursor/',
      'scripts/lib/install-targets/cursor-project.js',
      'tests/lib/install-targets.test.js',
    ],
  },
].map(freezeRecord));

function toTextList(value) {
  return Array.isArray(value) ? value.join('; ') : String(value || '');
}

function escapeMarkdownCell(value) {
  return toTextList(value).replace(/\|/g, '\\|').trim();
}

function renderMarkdownTable(records = ADAPTER_RECORDS) {
  const lines = [
    '| Harness or runtime | State | Supported assets | Unsupported or different surfaces | Install or onramp | Verification command | Risk notes |',
    '| --- | --- | --- | --- | --- | --- | --- |',
  ];

  for (const record of records) {
    lines.push([
      record.harness,
      record.state,
      record.supported_assets,
      record.unsupported_surfaces,
      record.install_or_onramp,
      record.verification_commands,
      record.risk_notes,
    ].map(escapeMarkdownCell).join(' | ').replace(/^/, '| ').replace(/$/, ' |'));
  }

  return lines.join('\n');
}

function renderStateTable() {
  const lines = [
    '| State | Meaning |',
    '| --- | --- |',
  ];

  for (const [state, meaning] of Object.entries(COMPLIANCE_STATES)) {
    lines.push(`| ${escapeMarkdownCell(state)} | ${escapeMarkdownCell(meaning)} |`);
  }

  return lines.join('\n');
}

function validateAdapterRecords(records = ADAPTER_RECORDS) {
  const errors = [];
  const ids = new Set();

  records.forEach((record, index) => {
    const label = record?.id || `record[${index}]`;

    for (const field of REQUIRED_FIELDS) {
      if (!Object.prototype.hasOwnProperty.call(record, field)) {
        errors.push(`${label}: missing required field ${field}`);
      }
    }

    if (typeof record.id !== 'string' || !/^[a-z0-9-]+$/.test(record.id)) {
      errors.push(`${label}: id must be a lowercase slug`);
    } else if (ids.has(record.id)) {
      errors.push(`${label}: duplicate id`);
    } else {
      ids.add(record.id);
    }

    if (!Object.prototype.hasOwnProperty.call(COMPLIANCE_STATES, record.state)) {
      errors.push(`${label}: unknown state ${record.state}`);
    }

    for (const field of [
      'supported_assets',
      'unsupported_surfaces',
      'install_or_onramp',
      'verification_commands',
      'risk_notes',
      'source_docs',
    ]) {
      if (!Array.isArray(record[field]) || record[field].length === 0) {
        errors.push(`${label}: ${field} must be a non-empty array`);
        continue;
      }

      record[field].forEach((value, valueIndex) => {
        if (typeof value !== 'string' || !value.trim()) {
          errors.push(`${label}: ${field}[${valueIndex}] must be a non-empty string`);
        }
      });
    }

    if (typeof record.harness !== 'string' || !record.harness.trim()) {
      errors.push(`${label}: harness must be a non-empty string`);
    }

    if (typeof record.owner !== 'string' || !record.owner.trim()) {
      errors.push(`${label}: owner must be a non-empty string`);
    }

    if (typeof record.last_verified_at !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(record.last_verified_at)) {
      errors.push(`${label}: last_verified_at must be YYYY-MM-DD`);
    }
  });

  return errors;
}

function extractMatrixBlock(markdown) {
  const normalized = String(markdown).replace(/\r\n/g, '\n');
  const start = normalized.indexOf(MATRIX_BLOCK_START);
  const end = normalized.indexOf(MATRIX_BLOCK_END);

  if (start < 0 || end < 0 || end <= start) {
    return null;
  }

  return normalized.slice(start + MATRIX_BLOCK_START.length, end).trim();
}

function validateDocumentation(options = {}) {
  const repoRoot = options.repoRoot || path.resolve(__dirname, '..', '..');
  const docPath = options.docPath || path.join(repoRoot, 'docs', 'architecture', 'harness-adapter-compliance.md');
  const errors = [];
  const source = fs.readFileSync(docPath, 'utf8');
  const actual = extractMatrixBlock(source);
  const expected = renderMarkdownTable();

  if (actual === null) {
    errors.push(`missing matrix block markers in ${path.relative(repoRoot, docPath)}`);
  } else if (actual !== expected) {
    errors.push(`matrix block in ${path.relative(repoRoot, docPath)} is not generated from adapter records`);
  }

  return errors;
}

module.exports = {
  ADAPTER_RECORDS,
  COMPLIANCE_STATES,
  MATRIX_BLOCK_END,
  MATRIX_BLOCK_START,
  REQUIRED_FIELDS,
  extractMatrixBlock,
  renderMarkdownTable,
  renderStateTable,
  validateAdapterRecords,
  validateDocumentation,
};
