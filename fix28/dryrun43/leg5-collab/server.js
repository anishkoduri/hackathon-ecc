// Minimal WebSocket sync server for the collab-editor fixture.
// No dependencies: Node built-ins only (http + crypto for the handshake,
// raw frame encode/decode for text messages). Broadcasts CRDT ops and
// presence to every other connected client; keeps an append-only op log
// (ops.jsonl) so a reloaded client re-syncs and the document survives a
// server restart. Presence messages are ephemeral (never logged).
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DIR = __dirname;
const LOG = path.join(DIR, 'ops.jsonl');
const PORT = Number(process.env.PORT || 8901);

let opLog = [];
try {
  if (fs.existsSync(LOG)) {
    opLog = fs.readFileSync(LOG, 'utf8').split('\n')
      .filter(Boolean).map((l) => JSON.parse(l));
  }
} catch (e) { console.error('op log replay failed:', e.message); }

const clients = new Set();

function wsAccept(key) {
  return crypto.createHash('sha1')
    .update(key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');
}

// Decode one (unfragmented, possibly masked) text frame. Returns
// {text, bytesConsumed} or null if the buffer holds an incomplete frame.
function decodeFrame(buf) {
  if (buf.length < 2) return null;
  const fin = (buf[0] & 0x80) !== 0;
  const opcode = buf[0] & 0x0f;
  const masked = (buf[1] & 0x80) !== 0;
  let len = buf[1] & 0x7f;
  let off = 2;
  if (len === 126) { if (buf.length < 4) return null; len = buf.readUInt16BE(2); off = 4; }
  else if (len === 127) { if (buf.length < 10) return null; len = Number(buf.readBigUInt64BE(2)); off = 10; }
  const maskLen = masked ? 4 : 0;
  if (buf.length < off + maskLen + len) return null;
  let payload = buf.slice(off + maskLen, off + maskLen + len);
  if (masked) {
    const mask = buf.slice(off, off + 4);
    payload = Buffer.from(payload);
    for (let i = 0; i < payload.length; i++) payload[i] ^= mask[i % 4];
  }
  if (opcode === 9) return { text: null, ping: true, bytesConsumed: off + maskLen + len };
  if (opcode === 8) return { text: null, close: true, bytesConsumed: off + maskLen + len };
  if (!fin || opcode !== 1) return { text: null, bytesConsumed: off + maskLen + len };
  return { text: payload.toString('utf8'), bytesConsumed: off + maskLen + len };
}

function encodeFrame(text) {
  const payload = Buffer.from(text, 'utf8');
  const len = payload.length;
  let header;
  if (len < 126) { header = Buffer.from([0x81, len]); }
  else if (len < 65536) { header = Buffer.alloc(4); header[0] = 0x81; header[1] = 126; header.writeUInt16BE(len, 2); }
  else { header = Buffer.alloc(10); header[0] = 0x81; header[1] = 127; header.writeBigUInt64BE(BigInt(len), 2); }
  return Buffer.concat([header, payload]);
}

function broadcast(sender, text) {
  for (const c of clients) {
    if (c !== sender && !c.destroyed) c.write(encodeFrame(text));
  }
}

const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/demo.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(fs.readFileSync(path.join(DIR, 'demo.html')));
  } else if (req.url === '/crdt.js') {
    res.writeHead(200, { 'Content-Type': 'text/javascript' });
    res.end(fs.readFileSync(path.join(DIR, 'crdt.js')));
  } else if (req.url === '/state') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ops: opLog.length, clients: clients.size }));
  } else {
    res.writeHead(404); res.end('not found');
  }
});

server.on('upgrade', (req, socket) => {
  const key = req.headers['sec-websocket-key'];
  if (!key) { socket.destroy(); return; }
  socket.write(
    'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n' +
    'Connection: Upgrade\r\nSec-WebSocket-Accept: ' + wsAccept(key) + '\r\n\r\n');
  clients.add(socket);
  // Sync: send the whole op log so a fresh/reconnected client converges.
  socket.write(encodeFrame(JSON.stringify({ kind: 'sync', ops: opLog })));
  let buf = Buffer.alloc(0);
  socket.on('data', (chunk) => {
    buf = Buffer.concat([buf, chunk]);
    for (;;) {
      const frame = decodeFrame(buf);
      if (!frame) break;
      buf = buf.slice(frame.bytesConsumed);
      if (frame.ping) { socket.write(Buffer.from([0x8a, 0x00])); continue; }
      if (frame.close) { socket.destroy(); break; }
      if (frame.text === null) continue;
      let msg;
      try { msg = JSON.parse(frame.text); } catch { continue; }
      if (msg.kind === 'op') {
        opLog.push(msg.op);
        try { fs.appendFileSync(LOG, JSON.stringify(msg.op) + '\n'); } catch {}
        broadcast(socket, frame.text);
      } else if (msg.kind === 'presence') {
        broadcast(socket, frame.text); // ephemeral: never logged
      }
    }
  });
  socket.on('close', () => clients.delete(socket));
  socket.on('error', () => clients.delete(socket));
});

server.listen(PORT, () => {
  console.log(`collab fixture server on http://localhost:${PORT}/ (ops in log: ${opLog.length})`);
});
