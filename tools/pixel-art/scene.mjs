// 使い方: SCALE=2 PIECESET=terrain node scene.mjs <出力PNG> — 地形6種を並べた確認用の場面を作る。
import { chromium } from "playwright-core";
const { PIECES } = await import("./terrain.mjs");
const d = Object.fromEntries(PIECES.map((p) => [p.name.slice(0, 2), { pal: p.pal.map((x) => x[1]), g: p.build() }]));
const layout = [["T5", "T1", "T1"], ["T1", "T2", "T1"], ["T4", "T6", "T3"]];
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await b.newPage({ viewport: { width: 800, height: 800 } });
await page.setContent(`<body style="margin:0;background:#000"><canvas id=c width=384 height=384 style="width:768px;height:768px;image-rendering:pixelated"></canvas></body>`);
await page.evaluate(({ d, layout }) => {
  const x = document.getElementById("c").getContext("2d");
  layout.forEach((row, ry) => row.forEach((key, rx) => { const t = d[key]; t.g.forEach((line, r) => line.forEach((k, c) => { if (k >= 0) { x.fillStyle = t.pal[k]; x.fillRect(rx * 128 + c, ry * 128 + r, 1, 1); } })); }));
}, { d, layout });
await page.screenshot({ path: process.argv[2] });
await b.close();
