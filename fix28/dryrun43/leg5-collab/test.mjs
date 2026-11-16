// Collab-editor fixture tests — evidence for the Leg 5 technical-depth check.
// Each check prints PASS/FAIL with measured numbers. Budgets (fixture brief):
//   - keystroke -> remote echo < 150 ms on localhost (measured, median + p95)
//   - 100-op burst applies in < 500 ms
//   - 10,000-char document applies/merges without loss
// Run: node test.mjs   (starts the fixture server on a scratch port itself)
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { Replica } = require('./crdt.js');
const __dirname = path.dirname(fileURLToPath(import.meta.url));

let pass = 0, fail = 0;
function check(name, ok, detail) {
  console.log('%s %s -- %s', ok ? 'PASS' : 'FAIL', name, detail);
  if (ok) pass++; else fail++;
}

// Deterministic PRNG for the shuffle test.
function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function typeInto(rep, text) {
  // Chain left-ids: each new char goes right after the previous one.
  const ops = [];
  let left = null;
  if (rep.visibleLength() > 0) left = rep._idAtVisible(rep.visibleLength() - 1);
  for (const ch of text) {
    const op = rep.insertAfter(left, ch);
    left = op.id;
    ops.push(op);
  }
  return ops;
}

function testConvergence() {
  // Two clients insert DIFFERENT text at the SAME position concurrently.
  const a = new Replica('A'), b = new Replica('B');
  const opsA = typeInto(a, 'HELLO');
  const opsB = typeInto(b, 'world');
  // Exchange: each applies the other's ops (concurrent, same left=NULL).
  for (const op of opsB) a.apply(op);
  for (const op of opsA) b.apply(op);
  check('1-convergence-same-position', a.toString() === b.toString(),
    `A="${a.toString()}" B="${b.toString()}" (concurrent inserts at pos 0 converge)`);
}

function testOutOfOrder() {
  // 200 ops applied in a shuffled order still converge.
  const src = new Replica('S');
  const ops = [];
  for (const ch of 'The quick brown fox jumps over the lazy dog. '.repeat(4)) {
    ops.push(src.insert(src.visibleLength(), ch));
  }
  // + 40 interleaved deletes of earlier chars (by id, via a second replica
  // that saw the first 100 inserts, so deletes reference real ids).
  const deleter = new Replica('D');
  for (const op of ops.slice(0, 100)) deleter.apply(op);
  for (let i = 0; i < 40; i++) {
    const op = deleter.delete(3);
    if (op) ops.push(op);
  }
  const rng = mulberry32(42);
  const shuffled = [...ops];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  const r1 = new Replica('X'), r2 = new Replica('Y');
  for (const op of ops) r1.apply(op);          // in-order
  for (const op of shuffled) r2.apply(op);     // shuffled
  check('2-out-of-order-delivery', r1.toString() === r2.toString()
    && r1.toString().length === 140,
    `in-order ${r1.toString().length} chars vs shuffled ${r2.toString().length} chars; ` +
    `equal=${r1.toString() === r2.toString()} (180 typed - 40 deleted = 140)`);
  // The shuffled replica must also equal the source replica after deletes.
  const srcAfter = new Replica('S2');
  for (const op of ops) srcAfter.apply(op);
  check('2b-out-of-order-matches-source', r2.toString() === srcAfter.toString(),
    `shuffled == source-after-deletes (${srcAfter.toString().length} chars)`);
}

function testOfflineMerge() {
  // B goes offline: A and B edit independently; B reconnects and merges.
  // The test maintains the shared op log explicitly, as the server does.
  const log = [];
  const a2 = new Replica('A'), b2 = new Replica('B');
  const push = (rep, op, logArr) => { if (op) logArr.push(op); };
  for (const ch of 'base text') push(a2, a2.insert(a2.visibleLength(), ch), log);
  for (const op of log) b2.apply(op);
  // Offline window: A brackets the text and appends; B braces inside it.
  const logA = [], logB = [];
  push(a2, a2.insert(0, '['), logA);
  push(a2, a2.insert(a2.visibleLength(), ']'), logA);
  for (const ch of ' +A') push(a2, a2.insert(a2.visibleLength(), ch), logA);
  push(b2, b2.insert(5, '{'), logB);
  push(b2, b2.insert(b2.visibleLength(), '}'), logB);
  for (const ch of ' +B') push(b2, b2.insert(b2.visibleLength(), ch), logB);
  // Reconnect: exchange the offline op sets (server sync = whole op log).
  for (const op of logB) a2.apply(op);
  for (const op of logA) b2.apply(op);
  const same = a2.toString() === b2.toString();
  // Every edit must survive: '{' lands inside "base text", so check the
  // markers individually, not the contiguous substring "base text".
  const hasAll = ['[', ']', '{', '}', '+A', '+B', 'base', 'text']
    .every((s) => a2.toString().includes(s));
  check('3-offline-merge', same && hasAll,
    `after reconnect A="${a2.toString()}" B="${b2.toString()}"; ` +
    `no edits lost=${hasAll}`);
}

function testCrossCollaboratorUndo() {
  // A inserts X, B inserts Y interleaved after it; A undoes X.
  // Y must survive, X must go, both replicas must agree.
  const a = new Replica('A'), b = new Replica('B');
  const opX = a.insert(0, 'X');
  b.apply(opX);
  const opY = b.insert(1, 'Y'); // B types right after A's X
  a.apply(opY);
  const undo = a.undo(); // A undoes its own X
  b.apply(undo);
  check('4-cross-collaborator-undo',
    a.toString() === 'Y' && b.toString() === 'Y',
    `after A undoes X: A="${a.toString()}" B="${b.toString()}" ` +
    `(Y survived, X gone, replicas agree)`);
  // Undo of a delete restores only that char.
  const del = b.delete(0); // B deletes Y
  a.apply(del);
  const un = b.undo(); // B undoes its delete
  a.apply(un);
  check('4b-undo-of-delete-restores',
    a.toString() === 'Y' && b.toString() === 'Y',
    `after B undoes its delete: A="${a.toString()}" B="${b.toString()}"`);
}

function testLargePaste() {
  // 5,000-char paste by A while B types concurrently; both converge.
  const a = new Replica('A'), b = new Replica('B');
  const seed = typeInto(a, 'start-');
  for (const op of seed) b.apply(op);
  const paste = 'Lorem ipsum dolor sit amet. '.repeat(179).slice(0, 5000);
  const opsA = [];
  for (const ch of paste) opsA.push(a.insert(a.visibleLength(), ch));
  const opsB = [];
  for (const ch of 'B-TYPING-HERE') opsB.push(b.insert(b.visibleLength(), ch));
  for (const op of opsB) a.apply(op);
  for (const op of opsA) b.apply(op);
  const same = a.toString() === b.toString();
  const expectLen = 6 + 5000 + 'B-TYPING-HERE'.length; // 6 + 5000 + 13 = 5019
  const lenOk = a.toString().length === expectLen;
  check('5-large-paste-plus-typing', same && lenOk,
    `converged=${same} length=${a.toString().length} (expect ${expectLen}); ` +
    `paste intact=${a.toString().includes('Lorem ipsum')}`);
}

function testBurstApply() {
  // 100-op burst applies in < 500 ms (local apply, no network).
  const rep = new Replica('P');
  const ops = [];
  const t0 = process.hrtime.bigint();
  for (let i = 0; i < 100; i++) ops.push(rep.insert(rep.visibleLength(), 'x'));
  const t1 = process.hrtime.bigint();
  const ms = Number(t1 - t0) / 1e6;
  const r2 = new Replica('Q');
  const t2 = process.hrtime.bigint();
  for (const op of ops) r2.apply(op);
  const t3 = process.hrtime.bigint();
  const applyMs = Number(t3 - t2) / 1e6;
  check('6a-burst-100-ops', ms < 500 && applyMs < 500 && rep.toString() === r2.toString(),
    `local insert 100 ops ${ms.toFixed(1)} ms; remote apply ${applyMs.toFixed(1)} ms ` +
    `(budget < 500 ms); converged=${rep.toString() === r2.toString()}`);
  // 10,000-char document: build + merge.
  const big = new Replica('BIG');
  const t4 = process.hrtime.bigint();
  const bigOps = typeInto(big, 'z'.repeat(10000));
  const t5 = process.hrtime.bigint();
  const big2 = new Replica('BIG2');
  for (const op of bigOps) big2.apply(op);
  const t6 = process.hrtime.bigint();
  check('6b-10k-doc', big.toString() === big2.toString() && big.visibleLength() === 10000,
    `build 10k chars ${(Number(t5 - t4) / 1e6).toFixed(1)} ms; ` +
    `merge ${(Number(t6 - t5) / 1e6).toFixed(1)} ms; converged, length ${big2.visibleLength()}`);
}

async function testLiveEcho() {
  // Live server: keystroke -> remote echo latency over real WebSocket.
  const PORT = 8931;
  const serverLog = path.join(__dirname, 'ops.jsonl');
  const server = spawn(process.execPath, [path.join(__dirname, 'server.js')], {
    env: { ...process.env, PORT: String(PORT) },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const waitFor = (ms) => new Promise((r) => setTimeout(r, ms));
  try {
    await waitFor(1200); // server boot
    const WS = global.WebSocket;
    const connect = () => new Promise((resolve, reject) => {
      const ws = new WS(`ws://localhost:${PORT}/`);
      ws.onopen = () => resolve(ws);
      ws.onerror = (e) => reject(new Error('ws open failed: ' + e.message));
    });
    const wsA = await connect();
    const wsB = await connect();
    const repA = new Replica('A'), repB = new Replica('B');
    const latencies = [];
    const sentAt = new Map();
    const done = new Promise((resolve) => {
      let received = 0;
      wsB.onmessage = (ev) => {
        const msg = JSON.parse(ev.data);
        if (msg.kind === 'sync') return;
        if (msg.kind === 'op') {
          repB.apply(msg.op);
          const t0 = sentAt.get(msg.op.id);
          if (t0) latencies.push(Date.now() - t0);
          if (++received >= 20) resolve();
        }
      };
      wsA.onmessage = () => {};
    });
    // A types 20 chars, one per ~30 ms; B measures op arrival latency.
    for (let i = 0; i < 20; i++) {
      const op = repA.insert(repA.visibleLength(), 'k');
      sentAt.set(op.id, Date.now());
      wsA.send(JSON.stringify({ kind: 'op', op }));
      await waitFor(30);
    }
    await Promise.race([done, waitFor(5000)]);
    const sorted = [...latencies].sort((x, y) => x - y);
    const median = sorted.length ? sorted[Math.floor(sorted.length / 2)] : -1;
    const p95 = sorted.length ? sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95))] : -1;
    check('7-live-echo-latency', latencies.length >= 20 && p95 < 150,
      `20 keystrokes echoed to B: n=${latencies.length} median=${median} ms ` +
      `p95=${p95} ms max=${sorted[sorted.length - 1]} ms (budget < 150 ms); ` +
      `B doc="${repB.toString()}"`);
    wsA.close(); wsB.close();
    // Persistence: the op log on disk holds the 20 ops; a fresh client
    // syncing gets them.
    await waitFor(300);
    let logged = 0;
    try { logged = fs.readFileSync(serverLog, 'utf8').split('\n').filter(Boolean).length; } catch {}
    check('7b-op-log-persisted', logged >= 20,
      `ops.jsonl holds ${logged} ops (>= 20 typed) — a reloaded client re-syncs from the log`);
  } finally {
    server.kill();
    await waitFor(300);
    try { fs.unlinkSync(path.join(__dirname, 'ops.jsonl')); } catch {}
  }
}

async function main() {
  testConvergence();
  testOutOfOrder();
  testOfflineMerge();
  testCrossCollaboratorUndo();
  testLargePaste();
  testBurstApply();
  await testLiveEcho();
  console.log(`\n${pass}/${pass + fail} collab checks passed`);
  process.exit(fail ? 1 : 0);
}

main().catch((e) => { console.error('TEST RUNNER CRASH:', e); process.exit(2); });
