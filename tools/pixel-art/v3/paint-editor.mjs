// 使い方: node paint-editor.mjs <スプライトのモジュール> <出力フォルダ> [下絵PNG]
// ドット絵エディタ（../editor.html）を起動し、32×32のグリッドに、マウスで一筆ずつ描く。下絵（お手本）を薄く重ねて比べることもできる。
// 出力: editor-*.png（エディタ画面の写真）、canvas.png（キャンバスだけ）、export.txt（エディタの書き出し）
import { chromium } from "playwright-core"; import { PAL } from "./sprite.mjs"; import { pathToFileURL, fileURLToPath } from "url"; import path from "path"; import fs from "fs";
const [mod, out, ref] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const rows = (await import(pathToFileURL(path.resolve(mod)).href)).rows, N = rows.length;
const used = [...new Set(rows.join("").split("").filter((c) => c !== "." && PAL[c]))];
const editor = fileURLToPath(new URL("../editor.html", import.meta.url));
const HEADED = process.env.HEADED === "1";
const b = await chromium.launch(HEADED ? { headless: false, channel: "chrome" } : { executablePath: process.env.CHROME_PATH || "/opt/pw-browsers/chromium" });
const p = await (await b.newContext({ viewport: { width: 1500, height: 1000 } })).newPage();
await p.route(/fonts\./, (r) => r.abort()); await p.goto(pathToFileURL(editor).href);
await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(N)); await p.fill("#gridH", String(N)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");
await p.evaluate(() => { const z = document.getElementById("zoom"); z.value = 16; z.dispatchEvent(new Event("input", { bubbles: true })); });
for (let i = 0; i < used.length - 4; i++) await p.click("#addSymbolBtn");
await p.waitForFunction((n) => document.querySelectorAll("#symbolList .sym").length >= n, used.length + 1);
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
for (let i = 0; i < used.length; i++) { await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, PAL[used[i]]); await li[i].fill(used[i]); }
if (ref) { await p.setInputFiles("#refFile", ref); await p.waitForTimeout(400); await p.evaluate(() => { const o = document.getElementById("refOpacity"); o.value = 35; o.dispatchEvent(new Event("input", { bubbles: true })); }); await p.screenshot({ path: `${out}/editor-0-ref.png` }); await p.click("#refClearBtn"); }
let box = await p.locator("#gridCanvas").boundingBox(), cw = box.width / N;
const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
const pick = async (k) => { const s = await p.$$("#symbolList .sym"); await s[k + 1].click(); await p.locator("#gridCanvas").scrollIntoViewIfNeeded(); await p.waitForTimeout(60); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / N; };
let strokes = 0;
for (let k = 0; k < used.length; k++) { await pick(k);
  for (let r = 0; r < N; r++) { let c = 0; while (c < N) { if (rows[r][c] === used[k]) { let e = c; while (e + 1 < N && rows[r][e + 1] === used[k]) e++; const [x0, y0] = cell(r, c), [x1] = cell(r, e); await p.mouse.move(x0, y0); await p.mouse.down(); if (e > c) await p.mouse.move(x1, y0, { steps: (e - c + 1) * 3 }); await p.mouse.up(); c = e + 1; strokes++; if (HEADED && process.env.PACE) await p.waitForTimeout(+process.env.PACE); } else c++; } } }
await p.waitForTimeout(400);
await p.screenshot({ path: `${out}/editor-1-done.png` }); await p.locator("#gridCanvas").screenshot({ path: `${out}/canvas.png` });
fs.writeFileSync(`${out}/export.txt`, await p.inputValue("#exportRows")); console.log("strokes", strokes, "colors", used.length); await b.close();
