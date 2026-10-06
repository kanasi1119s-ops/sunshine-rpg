import { chromium } from "/opt/node-tools/node_modules/playwright/index.mjs";
import fs from "fs";
const OUT = process.argv[2] ?? "frames";   // コマの書き出し先
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 800, height: 900 } });
p.on("pageerror", (e) => console.log("PAGEERR", e.message));
await p.goto("http://localhost:5199/");
await p.waitForTimeout(6000);
await p.evaluate(async () => {
  const tm = await import("/src/game/map/tile-map.ts");
  const w = await import("/src/game/world/world.ts");
  const tr = await import("/src/render/tile-map-renderer.ts");
  const vr = await import("/src/render/vortex-renderer.ts");
  const map = tm.createTileMap(w.WORLD_MAPS["world-map"]);
  const c = document.createElement("canvas");
  c.width = 360;
  c.height = 640;
  const ctx = c.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  // 絵を読みこませる（はじめの数回は描かれないことがあるので、空まわし）
  for (let i = 0; i < 4; i++) {
    const cam = { x: 2660, y: 1700, viewportWidth: 360, viewportHeight: 640 };
    tr.renderTileMap(ctx, map, cam);
    vr.renderBasin(ctx, map, cam, 0);
    vr.renderTowerCloud(ctx, map, cam, 0);
    await new Promise((r) => setTimeout(r, 600));
  }
  window.__reel = { map, c, ctx, tr, vr };
});
const T = 900;
for (let f = 0; f < T; f++) {
  const png = await p.evaluate((f) => {
    const { map, c, ctx, tr, vr } = window.__reel;
    const cx = 177.5 * 16, cy = 135.5 * 16;
    const pan = (f / 899) * 40; // 30秒で40ドット、ゆっくり下へ
    const cam = { x: Math.round(cx - 180), y: Math.round(cy - 470 + pan), viewportWidth: 360, viewportHeight: 640 };
    const now = 200 + (f * 1000) / 30;
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, 360, 640);
    tr.renderTileMap(ctx, map, cam);
    vr.renderBasin(ctx, map, cam, now);
    vr.renderTowerCloud(ctx, map, cam, now);
    vr.renderStorm(ctx, map, cam, now);
    return c.toDataURL("image/png");
  }, f);
  fs.writeFileSync(`${OUT}/f${String(f).padStart(4, "0")}.png`, Buffer.from(png.split(",")[1], "base64"));
  if (f % 150 === 0) console.log("frame", f);
}
await b.close();
