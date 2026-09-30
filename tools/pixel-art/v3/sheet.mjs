// 使い方: node sheet.mjs <出力PNG> <倍率> <画像...> — 参考画像を拡大して横に並べる（見るだけ。ゲームには使わない）
import fs from "fs"; import { chromium } from "playwright-core";
const [out, Z, ...files] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage();
const urls = files.map((f) => "data:image/png;base64," + fs.readFileSync(f).toString("base64"));
const d = await p.evaluate(async ({ urls, Z }) => { const imgs = await Promise.all(urls.map((u) => new Promise((r) => { const i = new Image(); i.onload = () => r(i); i.src = u; })));
  const w = imgs.reduce((s, i) => s + i.width * Z + 12, 0), h = Math.max(...imgs.map((i) => i.height * Z)); const c = document.createElement("canvas"); c.width = w; c.height = h; const x = c.getContext("2d"); x.imageSmoothingEnabled = false; x.fillStyle = "#3d3160"; x.fillRect(0, 0, w, h);
  let ox = 0; for (const i of imgs) { x.drawImage(i, ox, 0, i.width * Z, i.height * Z); ox += i.width * Z + 12; } return c.toDataURL("image/png"); }, { urls, Z: Number(Z) });
fs.writeFileSync(out, Buffer.from(d.split(",")[1], "base64")); await b.close();
