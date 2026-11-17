import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/playwright-core");
const SHELL = "/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell";
const browser = await chromium.launch({ executablePath: SHELL, args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--no-proxy-server"] });
const page = await browser.newPage();
const errors = [];
page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
page.on("pageerror", (e) => errors.push(String(e)));
await page.setViewportSize({ width: 1440, height: 900 });
await page.goto("http://localhost:5181/", { waitUntil: "networkidle" });
await page.waitForTimeout(2500);
const r = await page.evaluate(() => ({
  h1: document.querySelector("h1")?.textContent ?? null,
  h1Chars: document.querySelectorAll("h1 span, h1 div").length,
  canvas: !!document.querySelector("canvas.soffit-canvas"),
  canvasSize: (() => { const c = document.querySelector("canvas.soffit-canvas"); return c ? [c.width, c.height] : null; })(),
  terminalSvg: !!document.querySelector("#figure svg"),
  terminalText: document.querySelector("#figure")?.textContent?.slice(0, 120) ?? null,
  cta: document.querySelector(".hero-cta a")?.textContent ?? null,
  features: document.querySelectorAll("#features article").length,
  bodyText: document.body.innerText.slice(0, 200),
}));
console.log(JSON.stringify({ errors, ...r }, null, 2));
await page.screenshot({ path: "/home/hatch/workspace/hackathon-plugin/fix31/dryrun46/leg8-shot.png" });
await browser.close();
console.log("LEG8 PROBE DONE");
