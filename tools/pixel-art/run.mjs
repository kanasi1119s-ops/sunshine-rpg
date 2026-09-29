// 使い方: node run.mjs <エディタHTMLのパス> <出力フォルダ> [番号...]
// ドット絵エディタ（Artifact）をヘッドレスブラウザで開き、実際にマウスで描いて動画・画像・書き出しデータを残す。
import { chromium } from "playwright-core";
import fs from "fs";
const { PIECES } = await import(process.env.PIECESET === "terrain" ? "./terrain.mjs" : "./pieces.mjs");
import { N } from "./lib.mjs";

const [editorPath, out, ...only] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const list = PIECES.filter((_, i) => only.length === 0 || only.includes(String(i + 1)));
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });

for (const piece of list) {
  const g = piece.build();
  fs.writeFileSync(`${out}/${piece.name}.json`, JSON.stringify(g));
  const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 }, ...(process.env.NOVIDEO ? {} : { recordVideo: { dir: `${out}/video-${piece.name}`, size: { width: 1600, height: 1000 } } }) });
  const p = await ctx.newPage();
  await p.route(/fonts\./, (r) => r.abort());
  await p.goto("file://" + editorPath);
  await p.selectOption("#templateSelect", "blank"); await p.click("#loadTemplateBtn");
  await p.fill("#gridW", String(N)); await p.fill("#gridH", String(N)); await p.click("#resizeBtn");
  await p.uncheck("#symmetry"); await p.uncheck("#showShading");
  await p.evaluate(() => { const z = document.getElementById("zoom"); z.value = 4; z.dispatchEvent(new Event("input", { bubbles: true })); });
  for (let i = 0; i < piece.pal.length - 4; i++) await p.click("#addSymbolBtn");
  const ci = await p.$$("#symbolList input[type=color]"), li = await p.$$("#symbolList input.label");
  for (let i = 0; i < piece.pal.length; i++) {
    await ci[i].evaluate((el, v) => { el.value = v; el.dispatchEvent(new Event("input", { bubbles: true })); }, piece.pal[i][1]);
    await li[i].fill(piece.pal[i][0]);
  }
  let box = await p.locator("#gridCanvas").boundingBox(); let cw = box.width / N;
  const cell = (r, c) => [box.x + c * cw + cw / 2, box.y + r * cw + cw / 2];
  const pick = async (k) => { const s = await p.$$("#symbolList .sym"); await s[k + 1].click(); box = await p.locator("#gridCanvas").boundingBox(); cw = box.width / N; };
  for (let k = 0; k < piece.pal.length; k++) {
    let started = false;
    for (let r = 0; r < N; r++) {
      let c = 0;
      while (c < N) {
        if (g[r][c] === k) {
          let e = c; while (e + 1 < N && g[r][e + 1] === k) e++;
          if (!started) { await pick(k); started = true; }
          const [x0, y0] = cell(r, c), [x1] = cell(r, e);
          await p.mouse.move(x0, y0); await p.mouse.down();
          if (e > c) await p.mouse.move(x1, y0, { steps: e - c + 1 });
          await p.mouse.up(); c = e + 1;
        } else c++;
      }
    }
  }
  await p.waitForTimeout(600);
  await p.screenshot({ path: `${out}/${piece.name}-editor.png` });
  await p.locator("#gridCanvas").screenshot({ path: `${out}/${piece.name}.png` });
  fs.writeFileSync(`${out}/${piece.name}.txt`, await p.inputValue("#exportRows"));
  await ctx.close();
  console.log("done", piece.name);
}
await browser.close();
