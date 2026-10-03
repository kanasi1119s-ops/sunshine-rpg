// 追加の戦闘背景（src/render/battle-backdrop-extra.ts）をヘッドレスブラウザで描き、PNGに保存する。
// 使い方: node tools/backdrop-preview/render.mjs [kind ...]   （省略すると6つ全部）
// 出力: tools/backdrop-preview/out/<kind>.png（400×225 を2倍）。塗り残しがあれば桃色で出て、数も表示する。
// 事前に必要: playwright-core（/opt/node-tools/node_modules/playwright-core か tools/pixel-practice の node_modules）と /opt/pw-browsers/chromium
import { createRequire, stripTypeScriptTypes } from "module";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const require = createRequire(import.meta.url);
let chromium;
for (const p of ["playwright-core", path.join(root, "tools/pixel-practice/node_modules/playwright-core"), "/opt/node-tools/node_modules/playwright-core"]) {
  try {
    ({ chromium } = require(p));
    break;
  } catch {
    // 次の候補へ
  }
}
if (!chromium) throw new Error("playwright-core が見つかりません");

const src = fs.readFileSync(path.join(root, "src/render/battle-backdrop-extra.ts"), "utf8");
const js = stripTypeScriptTypes(src, { mode: "strip" }).replace(/export /g, "");
const all = ["forest", "swamp", "coast", "sky", "lava", "shrine"];
const kinds = process.argv.length > 2 ? process.argv.slice(2) : all;
fs.mkdirSync(path.join(here, "out"), { recursive: true });

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const page = await browser.newPage();
await page.setContent("<body></body>");
await page.addScriptTag({ content: js + "\nwindow.paintExtraBackdrop = paintExtraBackdrop;" });
for (const kind of kinds) {
  const res = await page.evaluate((k) => {
    const c = document.createElement("canvas");
    c.width = 400;
    c.height = 225;
    const ctx = c.getContext("2d");
    ctx.fillStyle = "#ff00ff";
    ctx.fillRect(0, 0, 400, 225);
    window.paintExtraBackdrop(k, ctx, 400, 225);
    const d = ctx.getImageData(0, 0, 400, 225).data;
    let miss = 0;
    for (let i = 0; i < d.length; i += 4) if (d[i] === 255 && d[i + 1] === 0 && d[i + 2] === 255) miss++;
    const o = document.createElement("canvas");
    o.width = 800;
    o.height = 450;
    const octx = o.getContext("2d");
    octx.imageSmoothingEnabled = false;
    octx.drawImage(c, 0, 0, 800, 450);
    return { data: o.toDataURL("image/png"), miss };
  }, kind);
  fs.writeFileSync(path.join(here, "out", kind + ".png"), Buffer.from(res.data.split(",")[1], "base64"));
  console.log(kind, "塗り残し:", res.miss);
}
await browser.close();
