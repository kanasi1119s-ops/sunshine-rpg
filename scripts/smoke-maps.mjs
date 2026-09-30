// 全地図の見た目・エラーの点検（開発用）。
// 使い方: `npm run dev` で開発サーバー（例: http://localhost:5173）を起動したまま、別のターミナルで
//   node scripts/smoke-maps.mjs [URL] [出力フォルダ]
// 事前に `playwright-core` と、Chromium の実行ファイルの場所（環境変数 CHROMIUM_PATH）が必要。
// 開発ビルドだけにある入口（`window.__sunshine`、`src/main.ts`）から、すべての地図へ移動して画面を保存し、
// ブラウザのエラーを数える。エラーがあれば、終了コード1で終わる。
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";

const url = process.argv[2] ?? "http://localhost:5173/";
const out = process.argv[3] ?? "smoke-maps";
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
const errors = [];
page.on("pageerror", (e) => errors.push(`PAGE ${e}`));
page.on("console", (m) => m.type() === "error" && !m.text().includes("404") && errors.push(`CONSOLE ${m.text()}`));
await page.goto(url);
await page.waitForTimeout(800);
await page.evaluate(() => window.__sunshine.startNew());
const ids = await page.evaluate(() => window.__sunshine.mapIds);
for (const id of ids) {
  await page.evaluate((mapId) => window.__sunshine.warp(mapId, 2, 2), id);
  await page.waitForTimeout(250);
  await page.screenshot({ path: `${out}/${id}.png`, clip: { x: 0, y: 60, width: 1000, height: 580 } });
}
await browser.close();
console.log(`${ids.length}か所の地図を確認しました。エラー: ${errors.length}件`);
for (const e of errors.slice(0, 20)) {
  console.log(e);
}
process.exit(errors.length > 0 ? 1 : 0);
