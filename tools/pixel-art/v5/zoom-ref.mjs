// 使い方: node zoom-ref.mjs <出力PNG> <倍率> <参考PNG...> — 参考のドット絵を拡大して1枚にする（見て学ぶ用）。NODE_PATH=/opt/node22/lib/node_modules/playwright/node_modules
import { chromium } from "/opt/node22/lib/node_modules/playwright/node_modules/playwright-core/index.mjs";
import { pathToFileURL } from "url";
const [out, scale, ...files] = process.argv.slice(2);
const html = `<body style="margin:0;background:#556;display:flex;gap:10px;align-items:flex-start;padding:8px">${files.map(f=>`<img src="${pathToFileURL(f).href}" style="image-rendering:pixelated;zoom:${scale}">`).join("")}</body>`;
import fs from "fs"; fs.writeFileSync(out+".html", html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1500, height: 900 } });
await p.goto(pathToFileURL(out+".html").href); await p.waitForTimeout(300);
await p.screenshot({ path: out, fullPage: true }); await b.close();
