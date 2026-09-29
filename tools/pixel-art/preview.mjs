// 使い方: node preview.mjs <出力PNG> — 10点を並べた一覧画像を作る（エディタで描く前の確認用）。
import { chromium } from "playwright-core";
const { PIECES } = await import(process.env.PIECESET === "terrain" ? "./terrain.mjs" : process.env.PIECESET === "boss" ? "./bosses.mjs" : "./pieces.mjs");
const out = process.argv[2];
const D = 64 * Number(process.env.SCALE || 1);
const data = PIECES.map((p) => ({ name: p.name, pal: p.pal.map((x) => x[1]), g: p.build() }));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await b.newPage({ viewport: { width: 1600, height: Number(process.env.VH || 700) } });
await page.setContent(`<body style="margin:0;background:#2a2140;color:#fff;font:12px sans-serif"><div id=w style="display:flex;flex-wrap:wrap;gap:6px;padding:6px"></div></body>`);
await page.evaluate(({ data, D, Z }) => {
  for (const d of data) {
    const box = document.createElement("div"); box.style.textAlign = "center";
    const c = document.createElement("canvas"); c.width = D; c.height = D; c.style.cssText = `width:${Math.max(256, D * Z)}px;height:${Math.max(256, D * Z)}px;image-rendering:pixelated;background:#3d3160`;
    const x = c.getContext("2d");
    d.g.forEach((row, r) => row.forEach((k, cc) => { if (k >= 0) { x.fillStyle = d.pal[k]; x.fillRect(cc, r, 1, 1); } }));
    box.appendChild(c); box.append(d.name); document.getElementById("w").appendChild(box);
  }
}, { data, D, Z: Number(process.env.ZOOM || 1) });
await page.screenshot({ path: out, fullPage: true });
await b.close();
