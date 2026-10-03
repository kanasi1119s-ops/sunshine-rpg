// ドット絵エディタ（tools/pixel-editor/index.html。Artifact「ドット絵エディタ」と同じもの）を、ヘッドレスブラウザで実際にマウス操作して絵を描く。
// 使い方: [EDITOR=<editor.html>] node editor-draw.mjs <絵.txt> <パレット.json> <出力PNG> [--ref 下絵.png] [--zoom 16] [--wide] [--import]
//   --import: マウスで塗る代わりに、エディタの「貼り付けて読み込む」で読み込む（大きな絵向け。直し描きは同じように行う）
//   --wide: 256×256 など大きな絵のとき（画面を広くし、エディタの並びの幅の上限を外す）。--zoom は6以上にする
//   絵.txt: 1文字=1ドットの文字グリッド（'.'は透明）。パレットJSON: {"文字":"#rrggbb"}
//   --ref を付けると下絵（トレース用）としてエディタに読み込み、下絵を重ねた画面も <出力>-trace.png に残す。
// 出力: <出力PNG>（エディタのキャンバスの画面）、<出力>.rows.txt（エディタが書き出した配列。描いた結果が文字グリッドと同じか確認する）
import { chromium } from "playwright-core";
import fs from "fs";
import { fileURLToPath } from "url";
const [txt, palPath, out, ...rest] = process.argv.slice(2);
const opt = (k, d) => (rest.includes(k) ? rest[rest.indexOf(k) + 1] : d);
const ref = opt("--ref", null), zoom = Number(opt("--zoom", 16)), wide = rest.includes("--wide"), viaImport = rest.includes("--import");
const rows = fs.readFileSync(txt, "utf8").split("\n").filter((l) => l.trim() !== "" && !l.startsWith("#"));
const pal = JSON.parse(fs.readFileSync(palPath, "utf8"));
const H = rows.length, W = Math.max(...rows.map((r) => r.length));
const syms = Object.keys(pal);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await (await browser.newContext({ viewport: wide ? { width: 2600, height: 2600 } : { width: 1500, height: 2000 } })).newPage();
await p.route(/fonts\./, (r) => r.abort());
const editorPath = process.env.EDITOR || fileURLToPath(new URL("../pixel-editor/index.html", import.meta.url)); // 指定がなければ、リポジトリの中のエディタ
await p.goto("file://" + editorPath);
// --wide: 大きな絵（256×256 など）のとき、キャンバスが画面に収まるよう、エディタの並びの幅の上限を外す
if (wide) await p.addStyleTag({ content: ".layout{max-width:none!important;grid-template-columns:220px max-content 300px!important}.canvas-wrap{max-height:none!important;overflow:visible!important}" });
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
// 色を選ぶと、ページがスクロールしてキャンバスの位置が変わることがある（縦に長い絵で食い違いが出た）。
// そのため、色を選ぶたびにキャンバスを画面に入れ直し、位置を測り直す
let box = null, cw = 0;
const measure = async () => { await p.locator("#gridCanvas").scrollIntoViewIfNeeded(); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / W; };
await measure();
const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
// --import: 大きな絵は、1ドットずつのマウス操作だと非常に時間がかかる（256×256で1枚30分以上）。
// そのときは、エディタの「貼り付けて読み込む」に配列を入れて読み込ませる（色はパレット欄で設定済み）。
if (viaImport) {
  const edRows = rows.map((r) => [...r.padEnd(W, ".")].map((ch) => (ch === "." || ch === " " ? "." : map[ch])).join(""));
  await p.fill("#importRows", JSON.stringify(edRows));
  await p.click("#importBtn");
  await p.waitForTimeout(500);
}
const symRows = await p.$$("#symbolList .symbol-row");
for (const ch of (viaImport ? [] : syms)) {
  let started = false;
  for (let r = 0; r < H; r++) {
    let c = 0;
    while (c < W) {
      if (rows[r][c] === ch) {
        let e = c; while (e + 1 < W && rows[r][e + 1] === ch) e++;
        if (!started) { await (await p.$$("#symbolList .symbol-row .sym"))[syms.indexOf(ch) + 1].click(); await measure(); started = true; }
        const [x0, y0] = cell(r, c), [x1] = cell(r, e);
        await p.mouse.move(x0, y0); await p.mouse.down(); if (e > c) await p.mouse.move(x1, y0, { steps: (e - c) * 2 + 2 }); await p.mouse.up(); c = e + 1;
      } else c++;
    }
  }
}
await p.waitForTimeout(300);
// 直し描き: 書き出しと文字グリッドを比べ、違うマスだけ1マスずつ塗り直す（最大3回）。
// 縦に長い絵などで、マウスの位置が1マスずれることがあるため
const readBack = async () => JSON.parse((await p.$eval("#exportRows", (t) => t.value)).replace(/,\s*\]/, "]"));
for (let pass = 0; pass < 3; pass++) {
  const cur = await readBack();
  const fixes = [];
  for (let r = 0; r < H; r++) for (let c = 0; c < W; c++) {
    const wantCh = (rows[r][c] ?? ".") === " " ? "." : (rows[r][c] ?? ".");
    const wantSym = wantCh === "." ? "." : map[wantCh];
    if (cur[r][c] !== wantSym) fixes.push([r, c, wantCh]);
  }
  if (!fixes.length) break;
  for (const ch of [...new Set(fixes.map((f) => f[2]))]) {
    const rowsSym = await p.$$("#symbolList .symbol-row .sym");
    await (ch === "." ? rowsSym[0] : rowsSym[syms.indexOf(ch) + 1]).click();
    await measure();
    for (const [r, c] of fixes.filter((f) => f[2] === ch)) {
      const [x, y] = cell(r, c);
      await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.up();
    }
  }
  await p.waitForTimeout(200);
}
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
