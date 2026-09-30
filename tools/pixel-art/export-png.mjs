// 使い方: SCALE=4 PIECESET=boss node export-png.mjs <出力フォルダ> — 部品を等倍のPNGとして書き出す（ギャラリー用）。
import { chromium } from "playwright-core";
import fs from "fs";
const out = process.argv[2];
fs.mkdirSync(out, { recursive: true });
const { PIECES } = await import(process.env.PIECESET === "terrain" ? "./terrain.mjs" : process.env.PIECESET === "boss" ? "./bosses.mjs" : process.env.PIECESET === "guard" ? "./guardians.mjs" : process.env.PIECESET === "chars" ? "./characters.mjs" : "./pieces.mjs");
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await b.newPage();
for (const p of PIECES) {
  const g = p.build(), pal = p.pal.map((x) => x[1]), n = g.length;
  const data = await page.evaluate(({ g, pal, n }) => {
    const c = document.createElement("canvas"); c.width = n; c.height = n; const x = c.getContext("2d");
    g.forEach((row, r) => row.forEach((k, cc) => { if (k >= 0 && pal[k]) { x.fillStyle = pal[k]; x.fillRect(cc, r, 1, 1); } }));
    return c.toDataURL("image/png");
  }, { g, pal, n });
  fs.writeFileSync(`${out}/${p.name}.png`, Buffer.from(data.split(",")[1], "base64"));
}
await b.close();
console.log("exported", PIECES.length);
