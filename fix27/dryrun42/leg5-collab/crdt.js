// Real-time collaborative editor fixture — sequence CRDT (RGA-style).
// Dry-run #40, Leg 5 technical-depth check (fix #25 §4(e), TECHDEPTH_F25).
//
// ALGORITHM (named, with invariant): a replicated growable array (RGA).
// Every character is a node {id, left, char, deleted}. `id` is
// "lamport:clientId". Each node's parent is the id of the character to its
// left at insert time (`left`, null = document start). Document order is a
// PRE-ORDER traversal of that tree with siblings sorted by id DESCENDING
// (higher Lamport clock first, clientId breaks ties). The order is a pure
// function of the op set, so:
//   INVARIANT (convergence): any two replicas that have applied the same
//   set of ops — in ANY order, with ANY interleaving — hold the identical
//   document string. Deletes are tombstones (nodes stay, flagged deleted),
//   so an id-addressed undo never disturbs another collaborator's text.
// Off-the-shelf maximalism stands: the transport is a plain WebSocket;
// the substance is the CRDT + merge + undo + presence around it.
'use strict';

function compareId(a, b) {
  // id = "lamport:client". Higher lamport first; tie -> higher client first.
  const [la, ca] = a.split(':');
  const [lb, cb] = b.split(':');
  const na = Number(la), nb = Number(lb);
  if (na !== nb) return nb - na; // descending lamport
  if (ca < cb) return 1;
  if (ca > cb) return -1;
  return 0;
}

class Replica {
  constructor(clientId) {
    this.clientId = clientId;
    this.clock = 0;
    this.nodes = new Map(); // id -> {id, left, char, deleted}
    this.children = new Map(); // parentId ('ROOT' for null) -> [childId, ...] sorted desc by id
    this.children.set('ROOT', []);
    this.undoStack = []; // local ops, for undo (inverse by id)
    this.redoStack = [];
    // Tombstones that arrived BEFORE their insert (out-of-order delivery):
    // a delete/undel for an unseen id is remembered and applied when the
    // insert lands, so no delete is ever lost to ordering.
    this.pendingDel = new Set();
    this.pendingUndel = new Set();
  }

  _parentKey(left) { return left === null ? 'ROOT' : left; }

  _attach(node) {
    this.nodes.set(node.id, node);
    const key = this._parentKey(node.left);
    if (!this.children.has(key)) this.children.set(key, []);
    const sibs = this.children.get(key);
    // insert keeping siblings sorted by id DESCENDING (compareId order)
    let i = 0;
    while (i < sibs.length && compareId(sibs[i], node.id) < 0) i++;
    sibs.splice(i, 0, node.id);
  }

  _tick(remoteLamport) {
    this.clock = Math.max(this.clock, remoteLamport || 0) + 1;
    return this.clock;
  }

  // Local insert of `char` at text position `pos` (0-based, visible chars).
  insert(pos, char) {
    const left = this._idAtVisible(pos - 1); // id left of the gap, null at 0
    return this.insertAfter(left, char);
  }

  // Insert directly after a KNOWN left id (no index scan). Sequential
  // appends chain this: each op's id becomes the next op's left, so
  // building N chars is O(N) total instead of O(N^2) re-scans.
  insertAfter(left, char) {
    const lamport = this._tick(0);
    const op = { type: 'ins', id: `${lamport}:${this.clientId}`, left, char };
    this.apply(op);
    this.undoStack.push(op);
    this.redoStack = [];
    return op;
  }

  // Local delete of the visible char at `pos`. Returns the op or null.
  delete(pos) {
    const id = this._idAtVisible(pos);
    if (id === null) return null;
    const op = { type: 'del', id };
    this.apply(op);
    this.undoStack.push(op);
    this.redoStack = [];
    return op;
  }

  // Undo MY most recent local op, addressed by id (never by position):
  // undo(insert X) = tombstone X; undo(delete Y) = clear Y's tombstone.
  // Another collaborator's interleaved edits are untouched by construction.
  undo() {
    const op = this.undoStack.pop();
    if (!op) return null;
    let inv;
    if (op.type === 'ins') inv = { type: 'del', id: op.id };
    else inv = { type: 'undel', id: op.id };
    this.apply(inv);
    this.redoStack.push(op);
    return inv;
  }

  // Apply a local or remote op. Idempotent: re-applying is a no-op for
  // inserts (node exists) and deletes (tombstone already set).
  apply(op) {
    if (op.type === 'ins') {
      if (this.nodes.has(op.id)) return false;
      const lamport = Number(op.id.split(':')[0]);
      if (lamport > this.clock) this.clock = lamport;
      const deleted = this.pendingDel.has(op.id);
      this.pendingDel.delete(op.id);
      this.pendingUndel.delete(op.id);
      this._attach({ id: op.id, left: op.left, char: op.char, deleted });
      return true;
    }
    if (op.type === 'del') {
      const n = this.nodes.get(op.id);
      this.pendingUndel.delete(op.id);
      if (!n) { this.pendingDel.add(op.id); return true; }
      if (n.deleted) return false;
      n.deleted = true;
      return true;
    }
    if (op.type === 'undel') {
      const n = this.nodes.get(op.id);
      this.pendingDel.delete(op.id);
      if (!n) { this.pendingUndel.add(op.id); return true; }
      if (!n.deleted) return false;
      n.deleted = false;
      return true;
    }
    return false;
  }

  _idAtVisible(visIndex) {
    // id of the visIndex-th visible char, or null if out of range.
    if (visIndex < 0) return null;
    let seen = -1;
    let found = null;
    this._walk((node) => {
      if (node.deleted) return;
      seen++;
      if (seen === visIndex) found = node.id;
    });
    return found;
  }

  _walk(fn) {
    // Iterative pre-order DFS (the tree can be 10k deep for a long
    // document typed char-by-char; recursion overflows the stack).
    const stack = [...(this.children.get('ROOT') || [])].reverse();
    while (stack.length) {
      const id = stack.pop();
      const node = this.nodes.get(id);
      if (!node) continue; // parent arrived before this child: unreachable for now
      fn(node);
      const kids = this.children.get(id) || [];
      for (let i = kids.length - 1; i >= 0; i--) stack.push(kids[i]);
    }
  }

  toString() {
    let out = '';
    this._walk((node) => { if (!node.deleted) out += node.char; });
    return out;
  }

  visibleLength() {
    let n = 0;
    this._walk((node) => { if (!node.deleted) n++; });
    return n;
  }

  // Id of the last visible char (null when the document is empty).
  lastVisibleId() {
    let last = null;
    this._walk((node) => { if (!node.deleted) last = node.id; });
    return last;
  }

  nodeCount() { return this.nodes.size; }
}

module.exports = { Replica, compareId };
