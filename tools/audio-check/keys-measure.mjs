// 鍵盤・シンセ系の音を、短いフレーズで 1 つずつ WAV に書き出し、音の数値（帯域・高域・ステレオ幅・立ち上がり・減衰・PLR）を測る道具。
// 使い方: node tools/audio-check/keys-measure.mjs <ケース.json> <出力フォルダ> [--only id,id] [--force]
//   ケース.json: [{ id, instrument, patch?, amp?, recipe?, reverb?, chorus?, bright?, volume?, mode: "chord"|"sus"|"lead"|"bass"|"arp", pan? }, ...]
//   - chord＝和音のコンピング（短く切る・離す。エレピ／ピアノ向け）／sus＝長くのばす和音（パッド・弦・オルガン）／lead＝旋律／bass＝低音／arp＝分散和音
//   - Chromium は 1 つだけ開き、1 曲ずつ順に書き出す（同時に複数動かさない）。曲ごとに <id>.wav と <id>.json（数値）を出力フォルダに書く。
//   - 数値は tools/audio-check/keys-metrics.py が出す。dist-composer は src/audio の変更では自動で作り直されないので、先に node tools/composer/build.mjs を実行すること。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
import { openSongKit, ROOT } from "../composer/song-lib.mjs";

const [casesFile, outDir, ...rest] = process.argv.slice(2);
if (!casesFile || !outDir) {
  console.error("使い方: node tools/audio-check/keys-measure.mjs <ケース.json> <出力フォルダ> [--only id,id] [--force]");
  process.exit(1);
}
const only = rest.includes("--only") ? rest[rest.indexOf("--only") + 1].split(",") : null;
const force = rest.includes("--force");
const cases = JSON.parse(fs.readFileSync(casesFile, "utf8")).filter((c) => !only || only.includes(c.id));
fs.mkdirSync(outDir, { recursive: true });

// 4 つの和音（Am7 Fmaj7 Cmaj7 G）を 2 小節ずつ。BPM 90・4/4 で 8 小節（約 21 秒）
const CHORDS = [["E4", "G4", "C5"], ["F4", "A4", "E5"], ["E4", "G4", "B4"], ["D4", "G4", "B4"]];
const ROOTS = ["A", "F", "C", "G"];
const LEAD = ["E5:1.5", "D5:0.5", "C5:1", "D5:1", "E5:2", "G5:1", "E5:1", "D5:4", "C5:1.5", "D5:0.5", "E5:1", "G5:1", "A5:2", "G5:1", "E5:1", "D5:4"];
const rep = (n, s) => Array.from({ length: n }, () => s).join(" ");

function phrase(c, v) {
  const mode = c.mode ?? "chord";
  if (mode === "chord") return CHORDS.map((ch) => `${ch[v]}:1.5 ${ch[v]}:0.5 ${ch[v]}:2 ${ch[v]}:1 R:1 ${ch[v]}:1 R:1`).join(" ");
  if (mode === "sus") return CHORDS.map((ch) => `${ch[v]}:4_ ${ch[v]}:4`).join(" ");
  if (mode === "arp") return CHORDS.map((ch) => rep(2, [0, 1, 2, 1, 0, 1, 2, 1].map((i) => `${ch[i % 3]}:0.5`).join(" "))).join(" ");
  if (mode === "lead") return LEAD.join(" ");
  if (mode === "bass") return ROOTS.map((r) => `${r}2:1.5 ${r}2:0.5 ${r}3:1 ${r}2:1 ${r}2:2 ${r}2:1 R:1`).join(" ");
  throw new Error("mode が不明: " + mode);
}

function songOf(c) {
  const mode = c.mode ?? "chord";
  const voices = mode === "chord" || mode === "sus" ? 3 : 1;
  const parts = [];
  for (let v = 0; v < voices; v++) {
    const p = {
      instrument: c.instrument, role: `${c.id}-${v}`, volume: c.volume ?? (voices === 3 ? 0.1 : 0.2), pan: c.pan ?? (voices === 3 ? [-0.3, 0, 0.3][v] : 0),
      amp: c.amp ?? "auto", sustain: c.sustain ?? 1, notes: phrase(c, v),
    };
    for (const k of ["patch", "recipe", "reverb", "chorus", "bright", "duck", "doubleDetune", "widen", "echo"]) if (c[k] !== undefined) p[k] = c[k];
    parts.push(p);
  }
  return { title: c.id, description: "鍵盤・シンセ測定用の短いフレーズ", bpm: 90, beats: 4, chords: "Am7 Fmaj7 Cmaj7 G", barsPerChord: 2, repeats: 1, autoAccompaniment: false, instrumentCheck: false, parts };
}

const todo = cases.filter((c) => force || !fs.existsSync(path.join(outDir, c.id + ".wav")));
const kit = await openSongKit();
let browser;
try {
  const { aiSongToScore } = await kit.load("/src/audio/ai-song.ts");
  if (todo.length) {
    const { createRequire } = await import("module");
    const globalRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
    const { chromium } = await import(path.join(globalRoot, "playwright/index.mjs"));
    browser = await chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required"] });
    const page = await browser.newPage();
    page.setDefaultTimeout(0);
    await page.goto("file://" + path.join(ROOT, "dist-composer/index.html"), { timeout: 600000 });
    await page.waitForFunction(() => "__composer" in window, undefined, { timeout: 600000 });
    await page.evaluate(() => window.__composer.setOverlays("std", "std", "std"));
    for (const c of todo) {
      const t0 = Date.now();
      const { score, warnings } = aiSongToScore(songOf(c));
      for (const w of warnings) console.log(`  注意(${c.id}): ${w}`);
      const b64 = await page.evaluate(([s]) => window.__composer.renderWav(s, "real", { raw: true }), [score]);
      fs.writeFileSync(path.join(outDir, c.id + ".wav"), Buffer.from(b64, "base64"));
      console.log(`書き出し ${c.id} (${((Date.now() - t0) / 1000).toFixed(1)}秒)`);
    }
  }
} finally {
  if (browser) await browser.close();
  await kit.close();
}
const wavs = cases.map((c) => path.join(outDir, c.id + ".wav")).filter((f) => fs.existsSync(f));
const run = (extra) => execFileSync("python3", [path.join(ROOT, "tools/audio-check/keys-metrics.py"), ...wavs, ...extra], { encoding: "utf8", maxBuffer: 1 << 28 });
fs.writeFileSync(path.join(outDir, "metrics.json"), run([]));
const tableText = run(["--table"]);
fs.writeFileSync(path.join(outDir, "metrics.txt"), tableText);
console.log(tableText);
