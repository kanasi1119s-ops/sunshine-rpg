// 使い方: node render.mjs <テキスト> <出力PNG> — 文字の絵を、色の割り当てに従って拡大PNGにする（v3: 1ドットずつ手で置く方式の確認用）
import fs from "fs"; import { chromium } from "playwright-core";
const PAL = { o:"#1b1224", H:"#3a1f2a", h:"#6b3a2e", g:"#9a5a3a", G:"#c98a52", S:"#b56a5a", s:"#e0967a", t:"#f4c09a", T:"#fbe0c0", E:"#2a1a3a", W:"#fff5e6", I:"#4a6ab0", M:"#a04a4a", J:"#1e2a5a", j:"#2f4a8a", k:"#4a72b8", K:"#7aa4d8", C:"#e8dcc0", A:"#ffb830" };
const [src, out] = process.argv.slice(2); const rows = fs.readFileSync(src, "utf8").trim().split("\n");
const bad = rows.filter((r) => r.length !== 64); if (bad.length) console.log("幅が64でない行:", rows.map((r,i)=>[i,r.length]).filter(([,l])=>l!==64).map(([i,l])=>`${i}:${l}`).join(" "));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage();
const d = await p.evaluate(({ rows, PAL }) => { const Z = 8, c = document.createElement("canvas"); c.width = 64 * Z; c.height = rows.length * Z; const x = c.getContext("2d"); x.fillStyle = "#3d3160"; x.fillRect(0, 0, c.width, c.height); rows.forEach((r, y) => [...r].forEach((ch, xx) => { if (PAL[ch]) { x.fillStyle = PAL[ch]; x.fillRect(xx * Z, y * Z, Z, Z); } })); return c.toDataURL("image/png"); }, { rows, PAL });
fs.writeFileSync(out, Buffer.from(d.split(",")[1], "base64")); await b.close(); console.log("rows", rows.length);
