// 使い方: node render32.mjs <モジュール> <出力PNG> — 32×32の絵を、拡大(16倍)と実寸(3倍)で並べて見る
import { chromium } from "playwright-core"; import { PAL, validate } from "./sprite.mjs"; import { pathToFileURL } from "url"; import path from "path"; import fs from "fs";
const [mod, out] = process.argv.slice(2); const m = await import(pathToFileURL(path.resolve(mod)).href); const rows = m.rows; const PALX = { ...PAL, ...(m.pal ?? {}) }; validate(rows);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage();
const d = await p.evaluate(({ rows, PAL }) => { const Z = 16, c = document.createElement("canvas"); c.width = 32 * Z + 32 * 3 * 3 + 40; c.height = 32 * Z; const x = c.getContext("2d"); x.fillStyle = "#3d3160"; x.fillRect(0, 0, c.width, c.height);
  rows.forEach((r, y) => [...r].forEach((ch, xx) => { if (PAL[ch]) { x.fillStyle = PAL[ch]; x.fillRect(xx * Z, y * Z, Z, Z); x.fillRect(32 * Z + 20 + xx * 3, 20 + y * 3, 3, 3); x.fillRect(32 * Z + 20 + xx * 3, 140 + y * 3, 3, 3); } }));
  x.fillStyle = "#4a7a3a"; x.fillRect(32 * Z + 20 + 40, 260, 120, 30); return c.toDataURL("image/png"); }, { rows, PAL: PALX });
fs.writeFileSync(out, Buffer.from(d.split(",")[1], "base64")); await b.close();
