// Live browser probe for the collab demo: loads demo.html in headless
// Chrome, types in pane A, checks pane B converges; exercises offline
// merge and cross-collaborator undo through the page's own controls.
// Run: node probe.mjs (starts the fixture server on port 8901 itself).
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/playwright-core');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const SHELL = '/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell';
const PORT = 8901;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const server = spawn(process.execPath, [path.join(import.meta.dirname, 'server.js')], {
  env: { ...process.env, PORT: String(PORT) },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let pass = 0, fail = 0;
const check = (name, ok, detail) => {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} -- ${detail}`);
  if (ok) pass++; else fail++;
};
try {
  await sleep(1200);
  const browser = await chromium.launch({
    executablePath: SHELL,
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--no-proxy-server'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on('pageerror', (e) => console.log('PAGEERROR:', String(e).split('\n')[0]));
  await page.goto(`http://localhost:${PORT}/`, { waitUntil: 'networkidle' });
  await sleep(1500);
  const text = () => page.evaluate(() => ({ a: window.__A.text(), b: window.__B.text() }));

  // 1. Type in A -> B converges.
  await page.click('#edA');
  await page.keyboard.type('Hello collab', { delay: 40 });
  await sleep(1200);
  let t = await text();
  check('live-type-A-to-B', t.a === 'Hello collab' && t.b === 'Hello collab',
    `A="${t.a}" B="${t.b}"`);

  // 2. Type in B -> A converges.
  await page.click('#edB');
  await page.keyboard.press('End');
  await page.keyboard.type(' +B', { delay: 40 });
  await sleep(1200);
  t = await text();
  check('live-type-B-to-A', t.a === 'Hello collab +B' && t.b === 'Hello collab +B',
    `A="${t.a}" B="${t.b}"`);

  // 3. Offline merge: A offline, type in both, reconnect, merge.
  await page.click('#offA'); // A goes offline
  await sleep(300);
  await page.click('#edA');
  await page.keyboard.press('End');
  await page.keyboard.type(' [A-offline]', { delay: 30 });
  await page.click('#edB');
  await page.keyboard.press('End');
  await page.keyboard.type(' [B-online]', { delay: 30 });
  await sleep(600);
  t = await text();
  check('live-offline-diverged', t.a.includes('[A-offline]') && !t.a.includes('[B-online]')
    && t.b.includes('[B-online]') && !t.b.includes('[A-offline]'),
    `while offline A="${t.a}" B="${t.b}"`);
  await page.click('#offA'); // reconnect
  await sleep(1500);
  t = await text();
  check('live-offline-merge', t.a === t.b && t.a.includes('[A-offline]') && t.a.includes('[B-online]'),
    `after reconnect A="${t.a}" B="${t.b}"`);

  // 4. Cross-collaborator undo: B undoes its own "[B-online]" text is many
  // ops; instead undo one op: type one char in B, undo it, check A agrees.
  await page.click('#edB');
  await page.keyboard.press('End');
  await page.keyboard.type('!', { delay: 30 });
  await sleep(800);
  t = await text();
  const withBang = t.a.endsWith('!') && t.b.endsWith('!');
  await page.click('#undoB');
  await sleep(800);
  t = await text();
  check('live-cross-undo', withBang && t.a === t.b && !t.a.endsWith('!'),
    `after B undoes "!": A="${t.a}" B="${t.b}"`);

  // 5. Presence: B's cursor position is broadcast (A shows a badge).
  await page.click('#edB');
  await page.keyboard.press('Home');
  await sleep(800);
  const presence = await page.evaluate(() => document.getElementById('presenceA').textContent);
  check('live-presence-badge', presence.includes('B is here'),
    `A's presence badge reads: "${presence}"`);

  await page.screenshot({ path: 'demo-shot.png' });
  console.log('screenshot: demo-shot.png');
  await browser.close();
} finally {
  server.kill();
  await sleep(300);
  try { fs.unlinkSync(path.join(import.meta.dirname, 'ops.jsonl')); } catch {}
}
console.log(`\n${pass}/${pass + fail} live probe checks passed`);
process.exit(fail ? 1 : 0);
