// 使い方: node tools/audio-check/layer-report.mjs assets-src/ai-songs/<曲ID>.json
// パートのグループ（ドラム・ベース・ギター・シンセ・鍵盤・弦／パッド／合唱・ブラス・鐘ほか）を1つずつ抜いた版を書き出して測り、
// 「どの層が、音量（LUFS）・つぶれ（PLR）・左右の相関に効いているか」を表にする（ミキサー役・アレンジャー役の診断）。
// 結果の読み方: 抜いたときに PLR が大きく上がる層は、つぶれの主因（持続音の層の足し過ぎなど）。LUFS が大きく下がる層は、音量の主役。
// 事前に node tools/composer/build.mjs。1グループにつき書き出し約30秒。
import { execFileSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";

const ROOT = path.resolve(new URL("../../", import.meta.url).pathname);
const file = process.argv[2];
if (!file) {
  console.error("使い方: node tools/audio-check/layer-report.mjs assets-src/ai-songs/<曲ID>.json");
  process.exit(1);
}
const song = JSON.parse(fs.readFileSync(file, "utf8"));
const GROUPS = {
  ドラム: ["kick", "snare", "hihat", "crash", "tom"],
  ベース: ["bass", "slap", "sub808"],
  ギター: ["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"],
  "シンセ・リード": ["lead", "keys"],
  "弦・パッド・合唱": ["strings", "pad", "choir"],
  ピアノ: ["piano", "harp", "harpsichord"],
  "ブラス・鐘ほか": ["brass", "bell", "kalimba", "panflute", "ocarina", "shakuhachi", "koto", "shamisen", "banjo", "sitar", "fiddle", "bagpipe"],
};
const present = Object.entries(GROUPS).filter(([, ins]) => song.parts.some((p) => ins.includes(p.instrument)));
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "layers-"));
const variants = [["全部", () => true], ...present.map(([name, ins]) => [`${name}を抜く`, (p) => !ins.includes(p.instrument)])];
const wavs = [];
for (const [i, [label, keep]] of variants.entries()) {
  const parts = song.parts.filter(keep);
  if (!parts.length) continue;
  const f = path.join(dir, `v${i}.json`);
  fs.writeFileSync(f, JSON.stringify({ ...song, parts }));
  execFileSync("node", ["tools/composer/song.mjs", "build", f, "--out", dir, "--wav"], { cwd: ROOT, stdio: "ignore" });
  wavs.push([label, path.join(dir, `v${i}.wav`)]);
}
const measured = JSON.parse(execFileSync("python3", ["tools/audio-check/analyze.py", ...wavs.map(([, w]) => w)], { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], maxBuffer: 1 << 26 }));
const rows = wavs.map(([label, w]) => [label, measured[path.basename(w)]]);
const base = rows[0][1];
const f1 = (x) => (x >= 0 ? "+" : "") + x.toFixed(1);
console.log(`# 層ごとの寄与: ${song.title}（全部 = I ${base.I} LUFS／PLR ${base.PLR}／相関 ${base.corr}／LRA ${base.LRA}）`);
console.log("注意: WAVはピークを-1dBにそろえて書き出される。PLR・相関・重心は有効、I（LUFS）は「ピークをそろえたあとの」相対値。\n");
console.log("| 版 | I(LUFS) | ΔI | PLR | ΔPLR | 相関 | 重心(Hz) |\n|---|---|---|---|---|---|---|");
for (const [label, v] of rows) console.log(`| ${label} | ${v.I} | ${label === "全部" ? "-" : f1(v.I - base.I)} | ${v.PLR} | ${label === "全部" ? "-" : f1(v.PLR - base.PLR)} | ${v.corr} | ${v.centroid_Hz} |`);
const worst = rows.slice(1).sort((a, b) => b[1].PLR - a[1].PLR)[0];
if (worst) console.log(`\n→ 抜くと PLR が最も上がる層: 「${worst[0].replace("を抜く", "")}」（PLR ${f1(worst[1].PLR - base.PLR)}）。つぶれ（PLR ${base.PLR}）を直すなら、まずこの層の音量・音数・音域を見直す。`);
fs.rmSync(dir, { recursive: true, force: true });
