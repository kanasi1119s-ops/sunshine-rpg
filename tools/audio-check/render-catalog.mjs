// 使い方: node tools/audio-check/render-catalog.mjs [--raw] <出力フォルダ> [曲ID ...]   （--raw: ピークをそろえず、ゲーム内の実際の大きさのまま書き出す）
// ゲームのBGM一覧（catalog＋src/audio/songs）の曲を、作曲ソフトと同じ音（実楽器版）でWAVに書き出す。IDを省略すると全曲。
// 書き出したWAVは `python3 tools/audio-check/analyze.py フォルダ/*.wav` で測れる。事前に `node tools/composer/build.mjs`（作曲ソフトの再ビルド）。
import { createServer } from "vite";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const argv = process.argv.slice(2);
const raw = argv.includes("--raw");
const [outDir, ...ids] = argv.filter((a) => a !== "--raw");
if (!outDir) {
  console.error("使い方: node tools/audio-check/render-catalog.mjs <出力フォルダ> [曲ID ...]");
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });
const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
const { allEntries, getTrack } = await server.ssrLoadModule("/src/audio/catalog.ts");
await server.ssrLoadModule("/src/audio/user-songs.ts");
const targets = ids.length ? ids : allEntries().map((e) => e.id);
const scores = targets.map((id) => [id, getTrack(id)]);
await server.close();

let pw;
for (const t of ["playwright", "/opt/node-tools/node_modules/playwright/index.mjs", path.join(execSync("npm root -g", { encoding: "utf8" }).trim(), "playwright/index.mjs")]) {
  try { pw = await import(t); break; } catch { /* 次を試す */ }
}
if (!pw) throw new Error("Playwright が見つかりません");
const browser = await pw.chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required"] });
try {
  const page = await browser.newPage();
  await page.goto("file://" + path.join(ROOT, "dist-composer/index.html"));
  await page.waitForFunction(() => "__composer" in window);
  for (const [id, score] of scores) {
    const file = path.join(outDir, `${id}.wav`);
    if (fs.existsSync(file)) continue;
    const b64 = await page.evaluate(([s, e, o]) => window.__composer.renderWav(s, e, o), [score, "real", { raw }]);
    fs.writeFileSync(file, Buffer.from(b64, "base64"));
    console.log("書き出し:", id);
  }
} finally {
  await browser.close();
}
