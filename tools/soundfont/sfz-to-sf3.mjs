// 使い方: node tools/soundfont/sfz-to-sf3.mjs <SFZ> <出力名> [--program 27] [--seconds 6] [--q 4] [--rr 2] [--stereo] [--shift -12]
//        [--only 正規表現] [--exclude 正規表現] [--gain dB] [--loop] [--fade 0.6] [--release 0.5] [--outdir assets-src/soundfont/extra]
// 無料で商用利用できる SFZ 音源（CC0・CC BY など。docs/assets-credits.md で規約を確かめたもの）を、作曲ソフト用の小さな SF3 にする汎用の道具。
//   assets-src/soundfont/extra/<出力名>.sf3 を書く。ゲーム本体には入れない（作曲ソフト専用）。
//   build-bass.mjs / build-drums.mjs / build-guitar.mjs が 1 つの音源ごとに書いていた変換を、SFZ の読み取りから一般化したもの。
// 読み取る SFZ の書き方: <control> default_path / <global> <master> <group> <region> の継承、
//   key / lokey / hikey / pitch_keycenter / lovel / hivel / sample / lorand / hirand / seq_position / seq_length /
//   loop_mode / loop_start / loop_end / offset / end / tune / volume / pan / trigger / #define $変数。
//   trigger=release（弾いた音を離したときの雑音）と、ピッチを変える効果（pitch_keytrack=0 など）は読み捨てる。
// 作りかた:
//   (1) 領域ごとに、強さ（lovel〜hivel）とキー（lokey〜hikey）が同じものを 1 つの「セル」にまとめる。
//   (2) セルの中に同じ条件のサンプルが複数ある（ラウンドロビン）ときは、--rr 個まで残し、強さの値（1〜127）の 1 つずつにどれかを割り当てる。
//       人間味づけ（human）で強さが少しずれると、弾くたびに違う録音が鳴る（build-fsbs.mjs と同じ考え方）。--rr 1 なら 1 つだけ。
//   (3) 各サンプルを ffmpeg で 44.1kHz に変えて読み、先頭の --seconds 秒で切り、最後に --fade 秒のフェードをかける。
//       ループのある音（--loop を付けたとき）は、ループ範囲が切った長さに入っているものだけ残す。
//   (4) Vorbis（--q）に圧縮して SF3 にする。
// 耳での確かめは別（作曲ソフトで鳴らして聞く）。この道具は録音の音程（自己相関）と長さ・ゾーン数を表示するだけ。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
import { loadBank, compressBank, timecents, BasicSoundBank, GeneratorTypes, emptyPresetFrom, SR } from "./lib.mjs";
import { BasicSample, SampleTypes } from "spessasynth_core";

const args = process.argv.slice(2);
const flags = new Set(["--stereo", "--loop"]);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--") && !flags.has(args[i - 1])));
const [sfzPath, outName] = pos;
if (!sfzPath || !outName) { console.error("使い方: node tools/soundfont/sfz-to-sf3.mjs <SFZ> <出力名> [--program 27] [--seconds 6] [--q 4] [--rr 2] [--stereo] [--only RE] [--exclude RE] [--loop]"); process.exit(1); }
const PROGRAM = Number(opt("--program", 27));
const SECONDS = Number(opt("--seconds", 6));
const Q = Number(opt("--q", 4));
const RR = Number(opt("--rr", 2));
const STEREO = args.includes("--stereo");
const KEEP_LOOP = args.includes("--loop");
const FADE = Number(opt("--fade", 0.6));
const RELEASE = Number(opt("--release", 0.5));
const GAIN = Number(opt("--gain", 0));
const SHIFT = Number(opt("--shift", 0)); // 半音。キー範囲と根音キーを一緒にずらす（ベースのように SFZ が「1オクターブ上の記譜」で書いてあるとき --shift -12）
const ONLY = opt("--only") ? new RegExp(opt("--only"), "i") : null;
const EXCLUDE = opt("--exclude") ? new RegExp(opt("--exclude"), "i") : null;
const OUT = path.resolve(opt("--outdir", "assets-src/soundfont/extra"));

// ---------- SFZ の読み取り ----------
const NOTE = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, b: 11 };
const noteNum = (v) => {
  if (v === undefined) return undefined;
  if (/^-?\d+$/.test(v)) return Number(v);
  const m = /^([a-gA-G])([#b]?)(-?\d+)$/.exec(v);
  if (!m) return undefined;
  return 12 * (Number(m[3]) + 1) + NOTE[m[1].toLowerCase()] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
};
function parseSfz(file) {
  const dir = path.dirname(file);
  let text = fs.readFileSync(file, "utf8").replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
  const defs = {};
  text = text.replace(/#define\s+(\$\w+)\s+(\S+)/g, (_, k, v) => { defs[k] = v; return ""; });
  for (const [k, v] of Object.entries(defs)) text = text.split(k).join(v);
  text = text.replace(/#include\s+"([^"]+)"/g, (_, f) => {
    const p = path.join(dir, f.replace(/\\/g, "/"));
    return fs.existsSync(p) ? fs.readFileSync(p, "utf8") : "";
  });
  const regions = [];
  const scope = { control: {}, global: {}, master: {}, group: {} };
  const re = /<(control|global|master|group|region|curve|effect|sample)>|([A-Za-z_][\w]*)=([^\n]*?)(?=\s+[A-Za-z_][\w]*=|\s*<|\s*$)/gm;
  let cur = null;
  let m;
  while ((m = re.exec(text))) {
    if (m[1]) {
      const h = m[1];
      if (h === "control") { cur = scope.control = {}; }
      else if (h === "global") { scope.global = {}; scope.master = {}; scope.group = {}; cur = scope.global; }
      else if (h === "master") { scope.master = {}; scope.group = {}; cur = scope.master; }
      else if (h === "group") { scope.group = {}; cur = scope.group; }
      else if (h === "region") { cur = {}; regions.push({ ...scope.global, ...scope.master, ...scope.group, __own: cur, __control: scope.control }); }
      else cur = {};
    } else if (cur) {
      cur[m[2]] = m[3].trim();
      if (regions.length && cur === regions[regions.length - 1].__own) { /* 領域の中の値 */ }
    }
  }
  return regions.map((r) => {
    const o = { ...r, ...r.__own };
    delete o.__own;
    const control = o.__control;
    delete o.__control;
    const dp = (control.default_path ?? "").replace(/\\/g, "/");
    return { ...o, __dir: path.join(dir, dp) };
  });
}

const regions = parseSfz(path.resolve(sfzPath)).filter((r) => r.sample);
const cells = new Map();
let skipped = 0;
for (const r of regions) {
  if ((r.trigger ?? "attack") !== "attack") { skipped++; continue; }
  const rel = r.sample.replace(/\\/g, "/");
  if (ONLY && !ONLY.test(rel)) { skipped++; continue; }
  if (EXCLUDE && EXCLUDE.test(rel)) { skipped++; continue; }
  const file = path.join(r.__dir, rel);
  if (!fs.existsSync(file)) { skipped++; continue; }
  let lo = noteNum(r.lokey ?? r.key), hi = noteNum(r.hikey ?? r.key);
  const center = noteNum(r.pitch_keycenter ?? r.key ?? "60"); // SFZ の既定は 60（C4）
  if (lo === undefined || hi === undefined || center === undefined) { skipped++; continue; }
  lo += SHIFT; hi += SHIFT;
  const lv = Number(r.lovel ?? 0), hv = Number(r.hivel ?? 127);
  const id = `${lo}-${hi}/${lv}-${hv}`;
  if (!cells.has(id)) cells.set(id, { lo, hi, center: center + SHIFT, lv, hv, alts: [] });
  cells.get(id).alts.push({ file, tune: Number(r.tune ?? 0), loopMode: r.loop_mode, loopStart: Number(r.loop_start ?? 0), loopEnd: Number(r.loop_end ?? 0), offset: Number(r.offset ?? 0), gain: Number(r.volume ?? 0), rel: rel });
}
if (!cells.size) throw new Error("使える領域がありません（--only / --exclude / sample のパスを確かめる）");

// ---------- 音の読み込み ----------
const decode = (file, offsetFrames) => {
  const ss = offsetFrames ? ["-ss", String(offsetFrames / 44100)] : [];
  const buf = execFileSync("ffmpeg", ["-v", "error", ...ss, "-i", file, "-t", String(SECONDS), "-ac", STEREO ? "2" : "1", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  const all = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  const g = 10 ** (GAIN / 20);
  if (!STEREO) { for (let i = 0; i < all.length; i++) all[i] *= g; return [all]; }
  const n = all.length >> 1, L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = all[2 * i] * g; R[i] = all[2 * i + 1] * g; }
  return [L, R];
};
const fade = (d, looped) => {
  if (looped) return d;
  const f = Math.min(d.length, Math.round(FADE * SR));
  for (let i = 0; i < f; i++) d[d.length - f + i] *= 1 - i / f;
  return d;
};

const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: outName };
const preset = emptyPresetFrom(base, out, { program: 27 });
preset.program = PROGRAM;
preset.name = outName;
const inst = preset.zones[0].instrument;
while (inst.zones.length) inst.deleteZone(0, true);

const cache = new Map();
let nSamples = 0, nZones = 0, longest = 0;
const addSmp = (alt, cell) => {
  const k = alt.file + "|" + alt.offset;
  if (cache.has(k)) return cache.get(k);
  const chans = decode(alt.file, alt.offset);
  const looped = KEEP_LOOP && alt.loopMode === "loop_continuous" && alt.loopEnd > 0 && alt.loopEnd < chans[0].length;
  const key = cell.center;
  const cents = Math.round(alt.tune);
  const name = path.basename(alt.file).replace(/\.\w+$/, "").slice(0, 18);
  const rg = 10 ** ((alt.gain || 0) / 20);
  if (rg !== 1) chans.forEach((c) => { for (let i = 0; i < c.length; i++) c[i] *= rg; });
  chans.forEach((c) => fade(c, looped));
  let res;
  if (chans.length === 1) {
    const s = new BasicSample(name, SR, key, cents, SampleTypes.monoSample, looped ? alt.loopStart : 0, looped ? alt.loopEnd : 0);
    s.setAudioData(chans[0], SR);
    out.addSamples(s);
    res = { smp: [s], looped };
  } else {
    const l = new BasicSample(name + " L", SR, key, cents, SampleTypes.leftSample, looped ? alt.loopStart : 0, looped ? alt.loopEnd : 0);
    const r = new BasicSample(name + " R", SR, key, cents, SampleTypes.rightSample, looped ? alt.loopStart : 0, looped ? alt.loopEnd : 0);
    l.setAudioData(chans[0], SR); r.setAudioData(chans[1], SR);
    l.setLinkedSample(r, SampleTypes.leftSample);
    out.addSamples(l, r);
    res = { smp: [l, r], looped };
  }
  longest = Math.max(longest, chans[0].length / SR);
  nSamples++;
  cache.set(k, res);
  return res;
};
const setupZone = (z, cell, looped) => {
  z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.002));
  z.setGenerator(GeneratorTypes.holdVolEnv, timecents(0.001));
  z.setGenerator(GeneratorTypes.decayVolEnv, timecents(1));
  z.setGenerator(GeneratorTypes.sustainVolEnv, 0);
  z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
  z.setGenerator(GeneratorTypes.reverbEffectsSend, 0);
  z.setGenerator(GeneratorTypes.initialFilterQ, 0);
  z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(RELEASE));
  z.setGenerator(GeneratorTypes.overridingRootKey, cell.center);
  if (looped) z.setGenerator(GeneratorTypes.sampleModes, 1);
};
const lows = [...cells.values()].reduce((a, c) => Math.min(a, c.lo), 127);
const highs = [...cells.values()].reduce((a, c) => Math.max(a, c.hi), 0);
for (const cell of cells.values()) {
  const alts = cell.alts.slice(0, Math.max(1, RR));
  const keyRange = { min: cell.lo === lows && cell.lo > 28 ? 28 : cell.lo, max: cell.hi === highs && cell.hi < 96 ? 96 : cell.hi };
  if (alts.length === 1) {
    const { smp, looped } = addSmp(alts[0], cell);
    for (const s of smp) {
      const z = inst.createZone(s);
      z.keyRange = keyRange;
      z.velRange = { min: Math.max(cell.lv, 0), max: Math.min(cell.hv, 127) };
      setupZone(z, cell, looped);
      nZones++;
    }
  } else {
    for (let v = Math.max(cell.lv, 1); v <= Math.min(cell.hv, 127); v++) {
      const { smp, looped } = addSmp(alts[v % alts.length], cell);
      for (const s of smp) {
        const z = inst.createZone(s);
        z.keyRange = keyRange;
        z.velRange = { min: v, max: v };
        setupZone(z, cell, looped);
        nZones++;
      }
    }
  }
}
out.flush();
await compressBank(out, Q);
const buf = out.writeSF2({});
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `${outName}.sf3`);
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "セル:", cells.size, "サンプル:", nSamples, "ゾーン:", nZones, "最長:", longest.toFixed(1) + "秒", "読み捨て:", skipped, "program:", PROGRAM);
