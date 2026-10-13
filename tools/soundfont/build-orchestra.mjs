// 使い方: node --experimental-strip-types tools/soundfont/build-orchestra.mjs [probe] [orchestra]
// オーケストラ楽器（弦・金管・木管・ティンパニ・ハープ・マリンバなど）の SoundFont を作る（assets-src/soundfont/extra/orchestra.sf3）。
//   元素材: VSCO 2 Community Edition（Versilian Studios。CC0。https://github.com/sgossner/VSCO-2-CE）
//   環境変数 VSCO にフォルダを渡す（約1GB。gitには入れない）。必要な「伸ばす音」の録音だけを取り出して使う。
//   伸ばす音は、中ほどをくり返し再生（ループ）できるようにして、長い音符でも途切れないようにしている。
//   音の高さは、ファイル名の音名ではなく、録音そのものから測る（ライブラリごとに「ド＝C3」「ド＝C4」とばらばらなため）。
//   probe を付けると、測った音の高さの一覧だけを表示する（SoundFont は作らない）。
import fs from "fs";
import path from "path";
import { SR, decodeMono, loadBank, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";
import { BasicSample, SampleTypes } from "spessasynth_core";

const VSCO = process.env.VSCO ?? "/tmp/vsco";
const OUT = path.resolve("assets-src/soundfont/extra");
const NOTE = /(?<![A-Za-z])([A-G])(#|b)?(-?\d)(?![0-9])/;
const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** 楽器の定義。dirs: 録音のフォルダ（VSCO からの相対）。programs: 入れかえる GM のプログラム番号。 */
const SETS = [
  { id: "violin", programs: [40], dirs: ["Strings/Solo Violin/Arco Vib"], loop: true, range: [55, 100], q: 4 },
  { id: "viola", programs: [41], dirs: ["Strings/Viola Section/susvib"], loop: true, range: [48, 91], q: 4 },
  { id: "cello", programs: [42], dirs: ["Strings/Cello Section/susvib"], loop: true, range: [36, 81], q: 4 },
  { id: "bass", programs: [43], dirs: ["Strings/Solo Contrabass/SusVib"], loop: true, range: [28, 67], q: 4 },
  { id: "vlnsec", programs: [], dirs: ["Strings/Violin Section/susVib"], loop: true, range: [55, 96], q: 4 },
  { id: "pizz", programs: [45], dirs: ["Strings/Violin Section/Pizz"], loop: false, maxSec: 2.5, range: [55, 100], q: 4 },
  { id: "harp", programs: [46], dirs: ["Strings/Harp"], loop: false, maxSec: 6, range: [24, 103], q: 4 },
  { id: "timpani", programs: [47], dirs: ["Percussion/Timpani"], loop: false, maxSec: 4, range: [38, 57], q: 4, fromFile: /Hit/ },
  { id: "trumpet", programs: [56], dirs: ["Brass/Trumpet/sus"], loop: true, range: [52, 88], q: 4 },
  { id: "trombone", programs: [57], dirs: ["Brass/Tenor Trombone/sus"], loop: true, range: [34, 76], q: 4 },
  { id: "tuba", programs: [58], dirs: ["Brass/Tuba/sus"], loop: true, range: [24, 65], q: 4 },
  { id: "horn", programs: [60], dirs: ["Brass/F Horn/sus"], loop: true, range: [34, 79], q: 4 },
  { id: "oboe", programs: [68], dirs: ["Woodwinds/Oboe/Sus"], loop: true, range: [58, 93], q: 4 },
  { id: "bassoon", programs: [70], dirs: ["Woodwinds/Bassoon/sus"], loop: true, range: [34, 76], q: 4 },
  { id: "clarinet", programs: [71], dirs: ["Woodwinds/Clarinet/susLong"], loop: true, range: [50, 94], q: 4 },
  { id: "piccolo", programs: [72], dirs: ["Woodwinds/Piccolo/Sus"], loop: true, range: [74, 108], q: 4 },
  { id: "flute", programs: [73], dirs: ["Woodwinds/Flute/susNV"], loop: true, range: [59, 102], q: 4 },
  { id: "organ", programs: [19, 20], dirs: ["Keys/Organ/Loud"], loop: true, range: [28, 100], q: 4 },
  { id: "marimba", programs: [12], dirs: ["Percussion/Marimba"], loop: false, maxSec: 3, range: [36, 96], q: 4 },
  { id: "glock", programs: [9], dirs: ["Percussion/Glock"], loop: false, maxSec: 4, range: [72, 108], q: 4 },
];
/** 合奏の楽器。いくつかの録音を、高さで受けもちを分ける。 */
const ENSEMBLES = [
  { programs: [48, 49], parts: [["cello", 0, 54], ["viola", 55, 66], ["vlnsec", 67, 127]] },
  { programs: [61], parts: [["tuba", 0, 40], ["trombone", 41, 55], ["horn", 56, 66], ["trumpet", 67, 127]] },
];

/** 音の高さ（MIDIのノート番号）を、自己相関で測る。測れなければ null。 */
function detectMidi(data) {
  const n = Math.min(data.length, SR * 1.2);
  const start = Math.min(Math.floor(SR * 0.35), Math.max(0, n - 20000));
  const N = Math.min(14000, n - start);
  if (N < 4000) return null;
  const x = data.subarray(start, start + N);
  const minLag = Math.floor(SR / 4500), maxLag = Math.min(Math.floor(SR / 24), N >> 1);
  let e0 = 0;
  for (let i = 0; i < N - maxLag; i++) e0 += x[i] * x[i];
  if (e0 < 1e-9) return null;
  const r = new Float32Array(maxLag + 2);
  for (let lag = minLag; lag <= maxLag + 1; lag++) {
    let s = 0, e1 = 0;
    for (let i = 0; i < N - maxLag - 1; i++) { s += x[i] * x[i + lag]; e1 += x[i + lag] * x[i + lag]; }
    r[lag] = s / Math.sqrt(e0 * e1 + 1e-12);
  }
  let best = 0;
  for (let lag = minLag + 1; lag <= maxLag; lag++) if (r[lag] > best && r[lag] >= r[lag - 1] && r[lag] >= r[lag + 1]) best = r[lag];
  if (best < 0.5) return null;
  for (let lag = minLag + 1; lag <= maxLag; lag++) {
    if (r[lag] >= best * 0.9 && r[lag] >= r[lag - 1] && r[lag] >= r[lag + 1]) {
      const a = r[lag - 1], b = r[lag], c = r[lag + 1];
      const d = a - 2 * b + c;
      const off = d ? (0.5 * (a - c)) / d : 0;
      return 69 + 12 * Math.log2(SR / (lag + off) / 440);
    }
  }
  return null;
}

/** ファイル名から、音名・強さ・好みの順位を読む。 */
function parseName(file) {
  const base = path.basename(file, ".wav");
  const m = NOTE.exec(base);
  const pc = m ? (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12 : null;
  const octave = m ? Number(m[3]) : null;
  let dyn = 3;
  const v = /(?:^|_)v(\d)(?:_|$)/.exec(base);
  if (v) dyn = Number(v[1]);
  else if (/_pp(?:_|$)/.test(base)) dyn = 1;
  else if (/_p(?:_|$)/.test(base) || /quiet/i.test(base)) dyn = 2;
  else if (/_mp(?:_|$)/.test(base)) dyn = 3;
  else if (/_mf(?:_|$)/.test(base)) dyn = 4;
  else if (/_ff(?:_|$)/.test(base)) dyn = 6;
  else if (/_f(?:_|$)/.test(base) || /loud/i.test(base)) dyn = 5;
  const rr = /rr(\d)/.exec(base) ?? /_(\d)(?:_|$)/.exec(base.replace(/^.*?_v\d/, ""));
  const rrn = rr ? Number(rr[1]) : 1;
  return { base, pc, octave, dyn, rrn };
}

function listFiles(set) {
  const out = [];
  for (const d of set.dirs) {
    const dir = path.join(VSCO, d);
    if (!fs.existsSync(dir)) throw new Error("見つかりません: " + dir);
    for (const f of fs.readdirSync(dir)) if (f.toLowerCase().endsWith(".wav") && (!set.fromFile || set.fromFile.test(f))) out.push(path.join(dir, f));
  }
  return out;
}

const CLEAN = "highpass=f=22,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.012";

/** 1つの楽器の録音を読み、音の高さごとに、弱い／強い2つの層を選ぶ。 */
function loadSet(set) {
  const files = listFiles(set).map((f) => ({ f, ...parseName(f) }));
  // 音の高さのグループ（音名・オクターブで分ける。timpaniのように音名がないものは、ファイルごと）
  const groups = new Map();
  for (const x of files) {
    const g = x.pc === null ? x.base.replace(/_v\d.*/, "") : `${x.pc}/${x.octave}`;
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(x);
  }
  const picked = [];
  for (const [g, list] of groups) {
    const dyns = [...new Set(list.map((x) => x.dyn))].sort((a, b) => a - b);
    const pickDyn = (d) => list.filter((x) => x.dyn === d).sort((a, b) => a.rrn - b.rrn || a.base.localeCompare(b.base))[0];
    const soft = pickDyn(dyns[0]);
    const loud = dyns.length > 1 ? pickDyn(dyns[dyns.length - 1]) : null;
    picked.push({ g, soft, loud });
  }
  return picked;
}

function processFile(set, x) {
  let data = decodeMono(x.f, set.loop ? 7 : (set.maxSec ?? 4) + 0.5, CLEAN);
  const maxLen = Math.floor(SR * (set.loop ? 5 : (set.maxSec ?? 4)));
  if (data.length > maxLen) data = data.slice(0, maxLen);
  const midi = detectMidi(data);
  return { data, midi };
}

/** 元の録音の音名（ファイル名）と、測った高さ（midi）から、鍵盤の番号を決める。 */
function resolveRoot(x, midi, set) {
  if (set.id === "timpani") { const m = /Timpani(\d)/.exec(x.base); if (m) return { root: [0, 30, 34, 37, 40, 44][Number(m[1])], cents: 0 }; } // 5つの太鼓の高さ（測った値をならしたもの）
  if (midi === null) return null;
  if (x.pc === null) return { root: Math.round(midi), cents: 0 };
  // ファイル名の音名と同じ音名で、測った高さにいちばん近い音
  let best = null;
  for (let k = x.pc; k < 128; k += 12) if (best === null || Math.abs(k - midi) < Math.abs(best - midi)) best = k;
  if (Math.abs(best - midi) > 1.6) return null; // 倍音を測った可能性。使わない
  // 録音の音名が半音ずれているものや、チューニングのずれは、測った高さに合わせる（伸ばす音の楽器だけ。鐘や太鼓は倍音が複雑で測りにくいので触らない）
  if (!set.loop) return { root: best, cents: 0 };
  const root = Math.round(midi);
  return { root, cents: Math.max(-49, Math.min(49, Math.round((root - midi) * 100))) };
}

function applyLoop(data, set) {
  const n = data.length;
  const fadeTail = Math.min(Math.floor(SR * 0.35), n >> 2);
  if (!set.loop || n < SR * 1.6) {
    // 余韻を自然に消す
    const f = Math.min(Math.floor(SR * 0.4), n >> 1);
    for (let i = 0; i < f; i++) data[n - 1 - i] *= i / f;
    return { data, ls: 0, le: 0 };
  }
  const le = n;
  const ls = Math.floor(n * 0.42);
  const X = Math.min(Math.floor(SR * 0.3), ls >> 1, (le - ls) >> 1);
  void fadeTail;
  // ループの終わりの手前を、ループの始まりの手前の音と混ぜて、つなぎ目の音を滑らかにする
  for (let i = 0; i < X; i++) {
    const t = i / X;
    const a = Math.cos((t * Math.PI) / 2), b = Math.sin((t * Math.PI) / 2);
    data[le - X + i] = data[le - X + i] * a + data[ls - X + i] * b;
  }
  return { data, ls, le: le - 1 };
}

function buildSet(set) {
  const picked = loadSet(set);
  const items = [];
  for (const { g, soft, loud } of picked) {
    for (const [layer, x] of [["soft", soft], ["loud", loud]]) {
      if (!x) continue;
      const { data, midi } = processFile(set, x);
      const rr = resolveRoot(x, midi, set);
      const root = rr ? rr.root : null;
      if (process.env.VERBOSE) console.log("   ", path.basename(x.f), "測定", midi === null ? "-" : midi.toFixed(2), "→", root);
      if (root === null) { console.warn("  高さを測れず除外:", path.basename(x.f)); continue; }
      items.push({ x, layer, root, cents: rr.cents, ...applyLoop(data, set), g });
    }
  }
  // 録音の音量はライブラリごとにばらばらなので、楽器ごとにそろえる（強い層の中央値が rms 0.09、弱い層は 0.05 になるように。強弱の差は残す）
  const rmsOf = (d) => { const a = Math.floor(SR * 0.1), b = Math.min(d.length, Math.floor(SR * 1.4)); let t = 0; for (let i = a; i < b; i++) t += d[i] * d[i]; return Math.sqrt(t / Math.max(1, b - a)); };
  const hasLoud = new Set(picked.filter((q) => q.loud).map((q) => q.g));
  // 音ごとに、はかる区間（ループがあればその中、なければ頭から1.4秒）の大きさをそろえる。隣の音と大きさがばらつくと、旋律がでこぼこに聞こえるため
  const measure = (it) => {
    const a = it.le > 0 ? it.ls : Math.floor(SR * 0.1), b2 = it.le > 0 ? it.le : Math.min(it.data.length, Math.floor(SR * 1.4));
    let t = 0; for (let i = a; i < b2; i++) t += it.data[i] * it.data[i];
    return Math.sqrt(t / Math.max(1, b2 - a));
  };
  const lim = 30;
  let gainSum = 0;
  for (const it of items) {
    const target = it.layer === "soft" && hasLoud.has(it.g) ? 0.065 : 0.085;
    let pk = 0;
    for (let i = 0; i < it.data.length; i++) pk = Math.max(pk, Math.abs(it.data[i]));
    const r = measure(it);
    const g = r > 1e-5 ? Math.min(target / r, lim, 0.97 / pk) : 1;
    gainSum += g;
    for (let i = 0; i < it.data.length; i++) it.data[i] *= g;
  }
  // ピークの制限で大きくできなかった音が混じると、そこだけ小さく聞こえる。同じ層の中で、小さい側の4分位に比べて 3dB より大きい音は、そこまで下げる
  for (const layer of ["soft", "loud"]) {
    const grp = items.filter((it) => (it.layer === "soft" && hasLoud.has(it.g)) === (layer === "soft"));
    if (grp.length < 4) continue;
    const lv = grp.map((it) => measure(it)).sort((x, y) => x - y);
    const cap = lv[Math.floor(lv.length / 4)] * 1.41;
    for (const it of grp) {
      const r = measure(it);
      if (r > cap) { const g2 = cap / r; for (let i = 0; i < it.data.length; i++) it.data[i] *= g2; }
    }
  }
  const gain = gainSum / items.length;
  console.log("  音量そろえ", set.id, (20 * Math.log10(gain)).toFixed(1) + "dB");
  return items;
}

const arg = process.argv.slice(2);
const probe = arg.includes("probe");
const only = arg.filter((a) => SETS.some((s) => s.id === a));

const results = new Map();
for (const set of SETS) {
  if (only.length && !only.includes(set.id)) continue;
  if (!fs.existsSync(path.join(VSCO, set.dirs[0]))) { console.warn("素材がないので飛ばします:", set.id); continue; }
  const items = buildSet(set);
  results.set(set.id, items);
  const roots = [...new Set(items.map((i) => i.root))].sort((a, b) => a - b);
  console.log(set.id.padEnd(9), "録音", String(items.length).padStart(3), "音域", roots[0], "-", roots[roots.length - 1], roots.join(","));
}
if (probe) process.exit(0);

const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Orchestra (VSCO 2 CE)" };

/** 音の高さの並びから、各録音が受けもつ鍵盤の範囲を決める（隣との真ん中で分ける）。 */
function keyRanges(roots, [lo, hi]) {
  const sorted = [...new Set(roots)].sort((a, b) => a - b);
  const map = new Map();
  sorted.forEach((r, i) => {
    const a = i === 0 ? 0 : Math.ceil((sorted[i - 1] + r) / 2 + 0.01);
    const b = i === sorted.length - 1 ? 127 : Math.floor((r + sorted[i + 1]) / 2);
    map.set(r, [a, b]);
  });
  void lo; void hi;
  return map;
}

const smpCache = new Map();
function sampleOf(set, it) {
  const k = set.id + "/" + it.x.base + "/" + it.layer;
  if (smpCache.has(k)) return smpCache.get(k);
  const s = new BasicSample(`${set.id} ${it.x.base}`.slice(0, 40), SR, it.root, it.cents ?? 0, SampleTypes.monoSample, it.ls, it.le);
  s.setAudioData(it.data, SR);
  out.addSamples(s);
  smpCache.set(k, s);
  return s;
}

function addZones(inst, set, items, window) {
  const ranges = keyRanges(items.map((i) => i.root), set.range);
  let n = 0;
  const hasLoud = new Set(items.filter((i) => i.layer === "loud").map((i) => i.root));
  for (const it of items) {
    const kr = ranges.get(it.root);
    const lo = Math.max(kr[0], window?.[0] ?? 0), hi = Math.min(kr[1], window?.[1] ?? 127);
    if (lo > hi) continue;
    const z = inst.createZone(sampleOf(set, it));
    z.keyRange = { min: lo, max: hi };
    const twoLayers = hasLoud.has(it.root);
    // 弱い層と強い層は、真ん中でかさねる（切りかえの段差を、重なる音のなめらかな入れかわりにする）
    z.velRange = it.layer === "loud" ? { min: 66, max: 127 } : { min: 1, max: twoLayers ? 104 : 127 };
    z.setGenerator(GeneratorTypes.overridingRootKey, it.root);
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(set.loop ? 0.45 : 0.9));
    z.setGenerator(GeneratorTypes.attackVolEnv, timecents(set.id === "organ" ? 0.01 : 0.005));
    if (it.le > 0) z.setGenerator(GeneratorTypes.sampleModes, 1);
    n++;
  }
  return n;
}

function emptyInstrument(program, name) {
  // game.sf3 は容量を減らすために一部の楽器を省いている。無い番号は、あるひとつの楽器の入れものを写して番号をつけかえる
  const have = base.presets.some((q) => !q.isGMGSDrum && q.bankMSB === 0 && q.program === program);
  const preset = emptyPresetFrom(base, out, { program: have ? program : 48 });
  preset.program = program;
  while (preset.zones.length > 1) preset.deleteZone(preset.zones.length - 1); // 元の楽器が複数の音を重ねている場合、2つ目以降は捨てる
  preset.zones[0].velRange = { min: 0, max: 127 }; // 残した1つ目は「いちばん強い音だけ」の割りあてだったので、全部の強さで鳴るように広げる
  preset.zones[0].keyRange = { min: 0, max: 127 };
  preset.name = name;
  const inst = preset.zones[0].instrument;
  while (inst.zones.length) inst.deleteZone(0, true);
  // 元の楽器の共通設定（音が減衰して消える設定・フィルター・音量の補正など）を捨てて、録音そのままの音にする
  inst.globalZone.generators = [];
  preset.globalZone.generators = preset.globalZone.generators.filter((g) => g.type !== 48);
  return inst;
}

let total = 0;
for (const set of SETS) {
  const items = results.get(set.id);
  if (!items?.length || !set.programs.length) continue;
  for (const p of set.programs) {
    const inst = emptyInstrument(p, `${set.id}`);
    total += addZones(inst, set, items);
  }
}
for (const e of ENSEMBLES) {
  for (const p of e.programs) {
    const inst = emptyInstrument(p, "ensemble");
    for (const [id, lo, hi] of e.parts) {
      const set = SETS.find((s) => s.id === id);
      const items = results.get(id);
      if (items?.length) total += addZones(inst, set, items, [lo, hi]);
    }
  }
}
out.flush();
await compressBank(out, 4);
const buf = out.writeSF2({});
const file = path.join(OUT, "orchestra.sf3");
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "ゾーン:", total);
