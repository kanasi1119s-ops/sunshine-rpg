// ドット絵エディタ（tools/pixel-editor/index.html）で、文字グリッドの絵を「描いていく様子」を動画にする。
// 使い方: node tools/pixel-practice/editor-record.mjs <絵.txt> <パレット.json> <出力フォルダ> [--zoom 3] [--face face.json] [--steps 40]
//   色ごとに少しずつ描き足す（外側の縁取り → 面積の大きい色 → 細かい色）。各段階でエディタの画面を撮る。
//   --face を付けると、目・口はいったん空けておき、最後にペンでマウス操作して1ドットずつ描く（手で描く様子）。
//   出力: <出力フォルダ>/frames/00000.png …（画面の写真）と、最後に「文字グリッドとの食い違い」を表示する。
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { chromium } from "playwright-core";
const [txt, palPath, outDir, ...rest] = process.argv.slice(2);
const opt = (k, d) => (rest.includes(k) ? rest[rest.indexOf(k) + 1] : d);
const zoom = Number(opt("--zoom", 3)), facePath = opt("--face", null), STEPS = Number(opt("--steps", 40)), ref = opt("--ref", null), firstPath = opt("--first", null);
const rows = fs.readFileSync(txt, "utf8").split("\n").filter((l) => l.trim() !== "" && !l.startsWith("#"));
const pal = JSON.parse(fs.readFileSync(palPath, "utf8"));
const H = rows.length, W = Math.max(...rows.map((r) => [...r].length));
const grid = rows.map((r) => [...r.padEnd(W, ".")]);
const syms = Object.keys(pal);
fs.mkdirSync(path.join(outDir, "frames"), { recursive: true });
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await (await browser.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 })).newPage();
await p.route(/fonts\./, (r) => r.abort());
await p.goto("file://" + fileURLToPath(new URL("../pixel-editor/index.html", import.meta.url)));
await p.evaluate(() => localStorage.clear());
await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(W)); await p.fill("#gridH", String(H)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");
await p.evaluate((z) => { const e = document.getElementById("zoom"); e.value = z; e.dispatchEvent(new Event("input", { bubbles: true })); }, zoom);
for (let i = 4; i < syms.length; i++) await p.click("#addSymbolBtn");
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
const symList = await p.$$eval("#symbolList .symbol-row .sym", (els) => els.map((e) => e.textContent).filter((t) => t !== "消"));
const map = {};
for (let i = 0; i < syms.length; i++) {
  map[syms[i]] = symList[i];
  await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, pal[syms[i]]);
  await li[i].fill(syms[i]);
}
// --ref: 元の絵を下絵として薄く重ね、その上からなぞっていく（トレース）
if (ref) { await p.setInputFiles("#refFile", ref); await p.waitForTimeout(300); await p.evaluate(() => { const o = document.getElementById("refOpacity"); o.value = 45; o.dispatchEvent(new Event("input", { bubbles: true })); }); }
await p.locator("#gridCanvas").scrollIntoViewIfNeeded();
let n = 0;
const shot = async (hold = 1) => { await p.$eval("#gridCanvas", (e) => e.scrollIntoView({ block: "center", inline: "center" })); const buf = await p.screenshot(); for (let k = 0; k < hold; k++) fs.writeFileSync(path.join(outDir, "frames", String(n++).padStart(5, "0") + ".png"), buf); };
await shot(6);
// 顔（目・口）はあとで手で描く
const face = new Set();
if (facePath) {
  const f = JSON.parse(fs.readFileSync(facePath, "utf8"));
  for (const [x0, y0] of f.eyes) for (let dy = 0; dy < f.eh; dy++) for (let dx = -1; dx <= f.ew; dx++) face.add(`${y0 + dy},${x0 + dx}`);
  const [fx0, fy0, fx1, fy1] = f.face; const my = Math.round(fy0 + (fy1 - fy0) * 0.73);
  for (let x = fx0; x <= fx1; x++) for (let y = my - 1; y <= my + 1; y++) face.add(`${y},${x}`);
}
// 描く順: 外側の縁取り（透明のとなりの色）→ 面積の大きい色から
const count = {}, edge = {};
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  const ch = grid[y][x]; if (ch === ".") continue;
  count[ch] = (count[ch] ?? 0) + 1;
  const nb = [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]].some(([yy, xx]) => yy < 0 || xx < 0 || yy >= H || xx >= W || grid[yy][xx] === ".");
  if (nb) edge[ch] = (edge[ch] ?? 0) + 1;
}
const first = firstPath ? new Set(JSON.parse(fs.readFileSync(firstPath, "utf8"))) : new Set();   // --first: 先に描く色（なぞった線・縁取り）
const order = Object.keys(count).sort((a, b) => (first.has(b) - first.has(a)) || ((edge[b] ?? 0) / count[b] > 0.5) - ((edge[a] ?? 0) / count[a] > 0.5) || count[b] - count[a]);
const per = Math.max(1, Math.ceil(order.length / STEPS));
const shown = new Set();
const importRows = async () => {
  const edRows = grid.map((r, y) => r.map((ch, x) => (ch !== "." && shown.has(ch) && !face.has(`${y},${x}`) ? map[ch] : ".")).join(""));
  await p.fill("#importRows", JSON.stringify(edRows)); await p.click("#importBtn"); await p.waitForTimeout(120);
};
for (let i = 0; i < order.length; i += per) {
  order.slice(i, i + per).forEach((c) => shown.add(c));
  await importRows(); await shot(2);
}
await shot(6);
// 顔をペンで描く（1ドットずつクリック）
if (face.size) {
  const box = await p.locator("#gridCanvas").boundingBox(); const cw = box.width / W;
  const todo = [...face].map((k) => k.split(",").map(Number)).filter(([y, x]) => y >= 0 && x >= 0 && y < H && x < W && grid[y][x] !== ".");
  const byCh = {};
  for (const [y, x] of todo) (byCh[grid[y][x]] ??= []).push([y, x]);
  let k = 0;
  for (const ch of Object.keys(byCh)) {
    await (await p.$$("#symbolList .symbol-row .sym"))[syms.indexOf(ch) + 1].click();
    // 色を選ぶとページが動くことがあるので、キャンバスの位置を測り直す（editor-draw.mjs と同じ）
    await p.locator("#gridCanvas").scrollIntoViewIfNeeded(); const bx = await p.locator("#gridCanvas").boundingBox(); const cw2 = bx.width / W;
    for (const [y, x] of byCh[ch]) {
      await p.mouse.move(bx.x + x * cw2 + cw2 / 2, bx.y + y * cw2 + cw2 / 2); await p.mouse.down(); await p.mouse.up();
      if (++k % 3 === 0) await shot(1);
    }
  }
  await shot(8);
}
// 確かめ: 書き出しと文字グリッドが同じか
const exported = JSON.parse((await p.$eval("#exportRows", (t) => t.value)).replace(/,\s*\]/, "]"));
let bad = 0;
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const want = grid[y][x] === "." ? "." : map[grid[y][x]]; if (exported[y][x] !== want) bad++; }
if (ref) { await p.click("#refClearBtn"); await p.waitForTimeout(150); }
await p.locator("#gridCanvas").screenshot({ path: path.join(outDir, "editor-final.png") });
await shot(18);
console.log(`エディタで描く様子: ${W}x${H}、${n} 枚、文字グリッドとの食い違い ${bad} マス`);
await browser.close();
