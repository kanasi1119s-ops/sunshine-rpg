// 使い方: node live.mjs <エディタHTML> <部品モジュール> <出力フォルダ>
// ドット絵エディタを実際に起動し、マウス操作で描いていく途中の画面を、一定の筆数ごとに撮る（録画ではなく画面写真）。
import { chromium } from "playwright-core";
import fs from "fs";
// 自分のパソコンで「描いている様子」を見るとき:  HEADED=1 node live.mjs   （引数を省くと、同梱の editor.html と akari.mjs を使う）
import { fileURLToPath, pathToFileURL } from "url";
const here = (f) => fileURLToPath(new URL(f, import.meta.url));
const [a1, a2, a3] = process.argv.slice(2);
const editorPath = a1 ?? here("../editor.html"), mod = a2 ?? here("./akari.mjs"), out = a3 ?? here("./live-out");
const HEADED = process.env.HEADED === "1";
fs.mkdirSync(out, { recursive: true });
const { PIECES } = await import(pathToFileURL(mod).href);
const piece = PIECES[0], g = piece.build(), N = g.length;
fs.writeFileSync(`${out}/grid.json`, JSON.stringify(g));
const launchOpts = HEADED
  ? { headless: false, slowMo: Number(process.env.SLOWMO || 0), ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: "chrome" }) }
  : { executablePath: process.env.CHROME_PATH || "/opt/pw-browsers/chromium" };
const browser = await chromium.launch(launchOpts);
const ctx = await browser.newContext({ viewport: { width: 1500, height: 1150 } });
const PACE = Number(process.env.PACE || 0); // 1筆ごとの待ち時間(ms)。見やすくしたいときは 5〜20
const p = await ctx.newPage();
await p.route(/fonts\./, (r) => r.abort());
await p.goto(pathToFileURL(editorPath).href);
await p.selectOption("#templateSelect", "blank");
await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(N));
await p.fill("#gridH", String(N));
await p.click("#resizeBtn");
await p.uncheck("#symmetry");
await p.uncheck("#showShading");
await p.evaluate(() => { const z = document.getElementById("zoom"); z.value = 4; z.dispatchEvent(new Event("input", { bubbles: true })); });
for (let i = 0; i < piece.pal.length - 4; i++) await p.click("#addSymbolBtn");
await p.waitForFunction((n) => document.querySelectorAll("#symbolList .sym").length >= n, piece.pal.length + 1);
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
for (let i = 0; i < piece.pal.length; i++) {
  await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, piece.pal[i][1]);
  await li[i].fill(piece.pal[i][0]);
}
let shot = 0;
const snap = async (label) => { await p.screenshot({ path: `${out}/live-${String(++shot).padStart(2, "0")}.png` }); console.log("shot", shot, label); };
await snap("パレット設定後（まだ何も描いていない）");
let box = await p.locator("#gridCanvas").boundingBox();
let cw = box.width / N;
const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
const pick = async (k) => { const s = await p.$$("#symbolList .sym"); await s[k + 1].click(); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / N; };
// 面積の大きい色から、横の一筆ずつマウスでなぞって描く
const count = new Map();
for (const row of g) for (const k of row) if (k >= 0) count.set(k, (count.get(k) || 0) + 1);
const order = [...count.keys()].sort((a, b) => count.get(b) - count.get(a));
let strokes = 0;
for (const k of order) {
  await pick(k);
  for (let r = 0; r < N; r++) {
    let c = 0;
    while (c < N) {
      if (g[r][c] === k) {
        let e = c;
        while (e + 1 < N && g[r][e + 1] === k) e++;
        const [x0, y0] = cell(r, c), [x1] = cell(r, e);
        await p.mouse.move(x0, y0);
        await p.mouse.down();
        if (e > c) await p.mouse.move(x1, y0, { steps: (e - c + 1) * 3 });
        await p.mouse.up();
        c = e + 1;
        strokes++;
        if (PACE) await p.waitForTimeout(PACE);
        if (strokes % (HEADED ? 100000 : 1200) === 0) await snap(`${strokes}筆目（色${piece.pal[k][0]}）`);
      } else c++;
    }
  }
}
await p.waitForTimeout(500);
await snap("完成");
await p.locator("#gridCanvas").screenshot({ path: `${out}/final-canvas.png` });
fs.writeFileSync(`${out}/export.txt`, await p.inputValue("#exportRows"));
console.log("done", strokes);
await browser.close();
