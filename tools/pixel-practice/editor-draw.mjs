// ドット絵エディタ（Artifact「ドット絵エディタ」の index.html を手元に保存したもの）を、ヘッドレスブラウザで実際にマウス操作して絵を描く。
// 使い方: EDITOR=<editor.html> node editor-draw.mjs <絵.txt> <パレット.json> <出力PNG> [--ref 下絵.png] [--zoom 16]
//   絵.txt: 1文字=1ドットの文字グリッド（'.'は透明）。パレットJSON: {"文字":"#rrggbb"}
//   --ref を付けると下絵（トレース用）としてエディタに読み込み、下絵を重ねた画面も <出力>-trace.png に残す。
// 出力: <出力PNG>（エディタのキャンバスの画面）、<出力>.rows.txt（エディタが書き出した配列。描いた結果が文字グリッドと同じか確認する）
import { chromium } from "playwright-core";
import fs from "fs";
const [txt, palPath, out, ...rest] = process.argv.slice(2);
const opt = (k, d) => (rest.includes(k) ? rest[rest.indexOf(k) + 1] : d);
const ref = opt("--ref", null), zoom = Number(opt("--zoom", 16));
const rows = fs.readFileSync(txt, "utf8").split("\n").filter((l) => l.trim() !== "" && !l.startsWith("#"));
const pal = JSON.parse(fs.readFileSync(palPath, "utf8"));
const H = rows.length, W = Math.max(...rows.map((r) => r.length));
const syms = Object.keys(pal);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await (await browser.newContext({ viewport: { width: 1500, height: 1400 } })).newPage();
await p.route(/fonts\./, (r) => r.abort());
await p.goto("file://" + process.env.EDITOR);
await p.evaluate(() => localStorage.clear());
await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(W)); await p.fill("#gridH", String(H)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");
await p.evaluate((z) => { const e = document.getElementById("zoom"); e.value = z; e.dispatchEvent(new Event("input", { bubbles: true })); }, zoom);
// パレット: 既定の4色を使い回し、足りない分を「色を追加」で足す。記号は後で editor の state に合わせて書き換えられないので、エディタ側の記号を使う
for (let i = 4; i < syms.length; i++) await p.click("#addSymbolBtn");
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
const symList = await p.$$eval("#symbolList .symbol-row .sym", (els) => els.map((e) => e.textContent).filter((t) => t !== "消"));
const map = {}; // 練習用の文字 → エディタの記号
for (let i = 0; i < syms.length; i++) {
  map[syms[i]] = symList[i];
  await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, pal[syms[i]]);
  await li[i].fill(syms[i]);
}
if (ref) { await p.setInputFiles("#refFile", ref); await p.waitForTimeout(300); await p.evaluate(() => { const o = document.getElementById("refOpacity"); o.value = 45; o.dispatchEvent(new Event("input", { bubbles: true })); }); }
const box = await p.locator("#gridCanvas").boundingBox(); const cw = box.width / W;
const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
const symRows = await p.$$("#symbolList .symbol-row");
for (const ch of syms) {
  let started = false;
  for (let r = 0; r < H; r++) {
    let c = 0;
    while (c < W) {
      if (rows[r][c] === ch) {
        let e = c; while (e + 1 < W && rows[r][e + 1] === ch) e++;
        if (!started) { await (await p.$$("#symbolList .symbol-row .sym"))[syms.indexOf(ch) + 1].click(); started = true; }
        const [x0, y0] = cell(r, c), [x1] = cell(r, e);
        await p.mouse.move(x0, y0); await p.mouse.down(); if (e > c) await p.mouse.move(x1, y0, { steps: (e - c) * 2 + 2 }); await p.mouse.up(); c = e + 1;
      } else c++;
    }
  }
}
await p.waitForTimeout(300);
if (ref) await p.locator("#gridCanvas").screenshot({ path: out.replace(/\.png$/, "-trace.png") });
await p.click("#refClearBtn");
await p.waitForTimeout(150);
await p.locator("#gridCanvas").screenshot({ path: out });
const exported = await p.$eval("#exportRows", (t) => t.value);
const got = JSON.parse(exported.replace(/,\s*\]/, "]")).map((r) => [...r].map((s) => (s === "." ? "." : Object.keys(map).find((k) => map[k] === s) ?? "?")).join(""));
fs.writeFileSync(out + ".rows.txt", got.join("\n") + "\n");
const want = rows.map((r) => r.padEnd(W, ".").replace(/ /g, "."));
const bad = want.reduce((n, r, y) => n + [...r].filter((ch, x) => ch !== got[y][x]).length, 0);
console.log(`エディタで描画: ${W}x${H}、文字グリッドとの食い違い ${bad} マス`);
await browser.close();
