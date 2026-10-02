// 使い方: node tools/audio-check/layer-report-catalog.mjs <曲ID> [<曲ID> ...]
// ゲームのBGM（catalog＋src/audio/songs）を、楽器のグループごとに抜いた版で書き出して測る（layer-report.mjs の、ゲームの曲版）。
// どの層が、つぶれ（PLR）・音量（LUFS）・左右の相関に効いているかを表にする。事前に node tools/composer/build.mjs。
import { createServer } from "vite";
import { execFileSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const ids = process.argv.slice(2);
if (!ids.length) { console.error("使い方: node tools/audio-check/layer-report-catalog.mjs <曲ID> ..."); process.exit(1); }
const GROUPS = {
  ドラム: ["kick", "snare", "hihat", "crash", "tom", "cowbell"],
  ベース: ["bass", "slap", "sub808"],
  ギター: ["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"],
  "シンセ・リード": ["lead", "keys"],
  "弦・パッド・合唱": ["strings", "pad", "choir"],
  "ピアノほか鍵盤": ["piano", "harp", "harpsichord"],
  "ブラス・鐘ほか": ["brass", "bell", "chime"],
};
const server = await createServer({ root: ROOT, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
const { getTrack } = await server.ssrLoadModule("/src/audio/catalog.ts");
await server.ssrLoadModule("/src/audio/user-songs.ts");
const scores = ids.map((id) => [id, getTrack(id)]);
await server.close();
let pw;
for (const t of ["playwright", "/opt/node-tools/node_modules/playwright/index.mjs", path.join(execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim(), "playwright/index.mjs")]) {
  try { pw = await import(t); break; } catch { /* 次 */ }
}
if (!pw) throw new Error("Playwright が見つかりません");
const browser = await pw.chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required"] });
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "layers-cat-"));
try {
  const page = await browser.newPage();
  await page.goto("file://" + path.join(ROOT, "dist-composer/index.html"));
  await page.waitForFunction(() => "__composer" in window);
  for (const [id, score] of scores) {
    const present = Object.entries(GROUPS).filter(([, ins]) => score.tracks.some((t) => t.instrument && ins.includes(t.instrument)));
    const variants = [["全部", () => true], ...present.map(([n, ins]) => [`${n}を抜く`, (t) => !(t.instrument && ins.includes(t.instrument))])];
    const wavs = [];
    for (const [i, [label, keep]] of variants.entries()) {
      const tracks = score.tracks.filter(keep);
      if (!tracks.some((t) => t.notes.some((n) => n.note !== "R"))) continue;
      const b64 = await page.evaluate(([s, e]) => window.__composer.renderWav(s, e), [{ ...score, tracks }, "real"]);
      const f = path.join(dir, `${id}-${i}.wav`);
      fs.writeFileSync(f, Buffer.from(b64, "base64"));
      wavs.push([label, f]);
    }
    const measured = JSON.parse(execFileSync("python3", ["tools/audio-check/analyze.py", ...wavs.map(([, w]) => w)], { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], maxBuffer: 1 << 26 }));
    const rows = wavs.map(([label, w]) => [label, measured[path.basename(w)]]);
    const base = rows[0][1];
    const f1 = (x) => (x >= 0 ? "+" : "") + x.toFixed(1);
    console.log(`\n# 層ごとの寄与: ${id}（全部 = I ${base.I} LUFS／PLR ${base.PLR}／相関 ${base.corr}／LRA ${base.LRA}）\n| 版 | I | ΔI | PLR | ΔPLR | 相関 | 重心(Hz) |\n|---|---|---|---|---|---|---|`);
    for (const [label, v] of rows) console.log(`| ${label} | ${v.I} | ${label === "全部" ? "-" : f1(v.I - base.I)} | ${v.PLR} | ${label === "全部" ? "-" : f1(v.PLR - base.PLR)} | ${v.corr} | ${v.centroid_Hz} |`);
  }
} finally {
  await browser.close();
  fs.rmSync(dir, { recursive: true, force: true });
}
