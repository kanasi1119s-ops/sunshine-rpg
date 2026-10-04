// エフェクトのコマ（tools/pixel-art/fx/*.py の出力 JSON）を、ドット絵エディタ（tools/pixel-editor/index.html）の
// フレームに1コマずつ入れ、コマの長さもそろえて、作品（.json）・GIF・シート（PNG）として書き出す（2026-10-04）。
// 使い方: node fx-editor.mjs <エフェクト.json> <出力フォルダ>
// 出力: <名前>.project.json（エディタで開ける作品）、<名前>.gif、<名前>.sheet.png、<名前>.editor.png（エディタの画面）
// 必要なもの: playwright-core（npm install --no-save playwright-core）、/opt/pw-browsers/chromium
import { chromium } from "playwright-core";
import { fileURLToPath } from "url";
import fs from "fs";
import path from "path";

const [fxPath, outDir] = process.argv.slice(2);
const FX = JSON.parse(fs.readFileSync(fxPath, "utf8"));
const base = path.basename(fxPath, ".json");
fs.mkdirSync(outDir, { recursive: true });
const W = FX.w, H = FX.h;
const syms = Object.keys(FX.palette);

const editor = process.env.EDITOR || fileURLToPath(new URL("../pixel-editor/index.html", import.meta.url));
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 }, acceptDownloads: true });
const p = await ctx.newPage();
await p.route(/fonts\./, (r) => r.abort());
await p.goto("file://" + editor);
await p.evaluate(() => localStorage.clear());
await p.reload();
const wait = (ms) => p.waitForTimeout(ms);

await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
await p.fill("#gridW", String(W)); await p.fill("#gridH", String(H)); await p.click("#resizeBtn");
await p.uncheck("#symmetry"); await p.uncheck("#showShading");

// パレット
for (let i = 4; i < syms.length; i++) await p.click("#addSymbolBtn");
const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
const edSyms = await p.$$eval("#symbolList .symbol-row .sym", (els) => els.map((e) => e.textContent).filter((t) => t !== "消"));
const map = {};
for (let i = 0; i < syms.length; i++) {
  map[syms[i]] = edSyms[i];
  await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, FX.palette[syms[i]]);
  await li[i].fill(syms[i]);
}

// コマを、絵の大きさ（W×H）いっぱいの配列にもどす（rows: 手前、back: ボスのうしろに描く部分）
const full = (rows, ox, oy) => {
  const g = Array.from({ length: H }, () => Array(W).fill("."));
  rows.forEach((r, y) => [...r].forEach((c, x) => { if (c !== "." && g[oy + y]) g[oy + y][ox + x] = map[c]; }));
  return g.map((r) => r.join(""));
};
const hasBack = FX.frames.some((f) => f.back);
// 奥と手前があるエフェクトは、レイヤー0「うしろ」・レイヤー1「前」に分ける
if (hasBack) {
  await p.fill("#layerName", "うしろ"); await p.dispatchEvent("#layerName", "change");
  await p.click("#layerAdd"); await p.fill("#layerName", "前"); await p.dispatchEvent("#layerName", "change");
}
const importCel = async (l, f, rows) => {
  await p.evaluate(([ll, ff]) => { const c = document.querySelector(`#timeline td.tl-cel[data-l='${ll}'][data-f='${ff}']`); if (c) c.click(); }, [l, f]);
  await p.fill("#importRows", JSON.stringify(rows));
  await p.click("#importBtn");
};
for (let k = 0; k < FX.frames.length; k++) {
  const f = FX.frames[k];
  if (k > 0) { await p.click("#frameAdd"); await wait(60); }
  const fi = await p.evaluate(() => [...document.querySelectorAll("#timeline th.tl-frame")].findIndex((t) => t.classList.contains("active")));
  if (hasBack) {
    await importCel(0, fi, full(f.back || ["."], f.bx || 0, f.by || 0));
    await importCel(1, fi, full(f.rows, f.x, f.y));
  } else {
    await importCel(0, fi, full(f.rows, f.x, f.y));
  }
  await p.fill("#frameDur", String(f.ms)); await p.dispatchEvent("#frameDur", "change");
}
const nFrames = await p.evaluate(() => document.querySelectorAll("#timeline th.tl-frame").length);
await p.evaluate(() => document.querySelector("#timeline th[data-f='0']").click());
await wait(300);
await p.screenshot({ path: path.join(outDir, base + ".editor.png") });

// 書き出し: エディタの画面（モーダル）に出た作品のテキスト・画像を、そのままファイルにする
const closeModal = async () => { await p.keyboard.press("Escape"); await wait(200); await p.evaluate(() => { const m = document.getElementById("modalBack"); if (m) m.hidden = true; }); };
await p.click("#saveProjBtn"); await wait(400);
fs.writeFileSync(path.join(outDir, base + ".project.json"), await p.inputValue("#projJson"));
await closeModal();
const grabImage = async (btn, scale, name) => {
  await p.click(btn); await wait(300);
  if (scale) await p.selectOption("#exScale", String(scale)).catch(() => {});
  await p.locator("#modalBack button.primary").first().click(); await wait(1500);
  const src = await p.$eval("#outBox img", (im) => im.src);
  fs.writeFileSync(path.join(outDir, name), Buffer.from(src.split(",")[1], "base64"));
  await closeModal();
};
await grabImage("#exGifBtn", 2, base + ".gif");
await grabImage("#exSheetBtn", 1, base + ".sheet.png");
console.log(`${FX.name}: エディタのフレーム ${nFrames} / コマ ${FX.frames.length} → ${outDir}`);
await browser.close();
