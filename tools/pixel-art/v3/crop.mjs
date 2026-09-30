// 使い方: node crop.mjs <画像> <x> <y> <w> <h> <倍率> <出力> — 参考画像の一部を拡大して見る（座標の目盛りつき）
import fs from "fs"; import { chromium } from "playwright-core";
const [f, x, y, w, h, Z, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage();
const u = "data:image/png;base64," + fs.readFileSync(f).toString("base64");
const d = await p.evaluate(async ({ u, x, y, w, h, Z }) => { const i = await new Promise((r) => { const m = new Image(); m.onload = () => r(m); m.src = u; });
  const c = document.createElement("canvas"); c.width = w * Z + 24; c.height = h * Z + 24; const k = c.getContext("2d"); k.imageSmoothingEnabled = false; k.fillStyle = "#3d3160"; k.fillRect(0, 0, c.width, c.height);
  k.drawImage(i, x, y, w, h, 24, 24, w * Z, h * Z); k.fillStyle = "#fff"; k.font = "10px monospace";
  for (let a = 0; a < w; a += 4) { k.fillText(String(a), 24 + a * Z, 10); k.fillRect(24 + a * Z, 14, 1, 10); } for (let a = 0; a < h; a += 4) { k.fillText(String(a), 0, 24 + a * Z + 9); k.fillRect(14, 24 + a * Z, 10, 1); }
  return c.toDataURL("image/png"); }, { u, x: +x, y: +y, w: +w, h: +h, Z: +Z });
fs.writeFileSync(out, Buffer.from(d.split(",")[1], "base64")); await b.close();
