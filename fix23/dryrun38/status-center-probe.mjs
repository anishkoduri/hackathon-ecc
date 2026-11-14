/* Dry-run #38 leg 2 probe: status-pair vertical CENTERS (ALIGN_F23_LABELS:
   "status pairs judged by vertical CENTERS, not tops"). The align harness
   records tops only, so this probe measures .status-time and .status-icons
   bounding rects at 1440/900/390 and compares centerY. */
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/playwright-core");
const SHELL = "/home/hatch/workspace/hackathon-plugin/fix22/dryrun37/demo-sample-video/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell";
const browser = await chromium.launch({
  executablePath: SHELL,
  args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--no-proxy-server"],
});
const page = await browser.newPage();
for (const w of [1440, 900, 390]) {
  await page.setViewportSize({ width: w, height: 900 });
  await page.goto("http://localhost:8323/index.html", { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  const m = await page.evaluate(() => {
    const r = (el) => { const b = el.getBoundingClientRect(); return { top: Math.round(b.top), h: Math.round(b.height), centerY: Math.round(b.top + b.height / 2) }; };
    const t = r(document.querySelector(".status-time"));
    const i = r(document.querySelector(".status-icons"));
    const sb = r(document.querySelector(".statusbar"));
    return { time: t, icons: i, bar: sb, centerDelta: Math.round((t.top + t.h / 2) - (i.top + i.h / 2)) };
  });
  console.log(JSON.stringify({ width: w, ...m }));
}
await browser.close();
console.log("STATUS-CENTER PROBE DONE");
