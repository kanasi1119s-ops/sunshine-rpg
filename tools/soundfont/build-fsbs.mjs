// 使い方: node tools/soundfont/build-fsbs.mjs <FSBSのSF2> <id> [--program 27] [--seconds 6] [--q 4] [--rr 2]
// FreePats の「FSBS Electric Guitar」（Fender の基本モデルのエレキを直接録音。CC0）の SF2 を、作曲ソフト用の小さな SF3 にする。
//   assets-src/soundfont/extra/guitar-fsbs-<id>.sf3 を書く。ゲーム本体には入れない（作曲ソフト専用）。
//   元の SF2 は 1 音あたり 10〜40 秒・ラウンドロビン 4・強弱 2 段で 200〜400MB あるので、
//   (1) 先頭の --seconds 秒だけ切って最後に 0.8 秒のフェードをかけ、(2) ラウンドロビンを --rr 個に絞り、(3) Vorbis（--q）に圧縮する。
//   強さ 1〜127 の 1 つずつに、強弱グループ（soft = 〜92、強 = 93〜）の中のラウンドロビンを割り当てる（元の割り当てと同じ考え方。
//   人間味づけ（human）で強さが少しずれると、弾くたびに違う録音が鳴る）。
//   direct（生のDI）は、作曲ソフトのアンプ（NAM）に通す前提の音。clean / jazz / dist は、元作者がアンプ・エフェクトを通した音。
// 元素材: FreePats https://freepats.zenvoid.org/ElectricGuitar/clean-electric-guitar.html （CC0 1.0）。記録は docs/assets-credits.md
// 作りかたは tools/soundfont/build-guitar.mjs（Karoryfer のギター）に倣った。新しいファイルだけで、既存の音源・登録には触らない。
import fs from "fs";
import path from "path";
import { loadBank, compressBank, timecents, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";
import { BasicSample, SampleTypes } from "spessasynth_core";

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const [src, id] = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
if (!src || !id) { console.error("使い方: node tools/soundfont/build-fsbs.mjs <SF2> <id> [--program 27] [--seconds 6] [--q 4] [--rr 2]"); process.exit(1); }
const PROGRAM = Number(opt("--program", 27));
const SECONDS = Number(opt("--seconds", 6));
const Q = Number(opt("--q", 4));
const RR = Number(opt("--rr", 2));
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const bank = loadBank(path.resolve(src));

// 元の割り当てを読む: サンプル名 → { キー範囲, 強弱グループ, ラウンドロビン番号, 左右 }
const parse = (name) => {
  const m = /^([A-G]#?\d)_s\d_(soft_)?(\d+)(?:_(L|R))?$/.exec(name);
  if (!m) return null;
  return { note: m[1], soft: !!m[2], rr: Number(m[3]), ch: m[4] ?? "M" };
};
const groups = new Map(); // "キー範囲" → { soft:[{rr,L,R}], hard:[...] }
for (const z of bank.instruments[0].zones) {
  const p = parse(z.sample.name);
  if (!p) continue;
  const key = `${z.keyRange.min}-${z.keyRange.max}`;
  if (!groups.has(key)) groups.set(key, { min: z.keyRange.min, max: z.keyRange.max, root: z.sample.originalKey, soft: new Map(), hard: new Map() });
  const g = groups.get(key);
  const set = p.soft ? g.soft : g.hard;
  if (!set.has(p.rr)) set.set(p.rr, {});
  set.get(p.rr)[p.ch] = z.sample;
}
if (!groups.size) throw new Error("FSBS の名前の形のサンプルが見つかりません");

const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: `Guitar FSBS ${id}` };
const cut = (data, rate) => {
  const n = Math.min(data.length, Math.round(SECONDS * rate));
  const d = new Float32Array(n);
  d.set(data.subarray(0, n));
  const f = Math.min(n, Math.round(0.8 * rate));
  for (let i = 0; i < f; i++) d[n - f + i] *= 1 - i / f;
  return d;
};
const added = new Map(); // 元サンプル → 新サンプル（または [L,R]）
const addSample = (orig) => {
  if (added.has(orig)) return added.get(orig);
  const rate = orig.sampleRate;
  const mk = (suffix, type) => {
    const s = new BasicSample(orig.name + suffix, rate, orig.originalKey, orig.pitchCorrection ?? 0, type, 0, 0);
    return s;
  };
  const a = orig.getAudioData();
  const s = mk("", SampleTypes.monoSample);
  s.setAudioData(cut(a, rate), rate);
  out.addSamples(s);
  added.set(orig, s);
  return s;
};
const mono = (set) => {
  // 左右に分かれている元（dist）は左右を平均して 1 本にする（作曲ソフト側で広げる）
  const m = new Map();
  for (const [rr, ch] of set) {
    if (ch.M) m.set(rr, ch.M);
    else if (ch.L && ch.R) {
      const l = ch.L.getAudioData(), r = ch.R.getAudioData();
      const n = Math.min(l.length, r.length);
      const d = new Float32Array(n);
      for (let i = 0; i < n; i++) d[i] = (l[i] + r[i]) / 2;
      const fake = Object.create(ch.L);
      fake.getAudioData = () => d;
      fake.name = ch.L.name.replace(/_L$/, "");
      m.set(rr, fake);
    }
  }
  return m;
};

const preset = emptyPresetFrom(base, out, { program: 27 });
preset.program = PROGRAM;
preset.name = `Guitar FSBS ${id}`;
const inst = preset.zones[0].instrument;
while (inst.zones.length) inst.deleteZone(0, true);
let zones = 0, samples = 0;
const keys = [...groups.values()].sort((a, b) => a.min - b.min);
const lo = keys[0].min, hi = keys[keys.length - 1].max;
for (const g of keys) {
  const soft = [...mono(g.soft)].sort((a, b) => a[0] - b[0]).slice(0, RR).map((x) => x[1]);
  const hard = [...mono(g.hard)].sort((a, b) => a[0] - b[0]).slice(0, RR).map((x) => x[1]);
  for (let v = 1; v <= 127; v++) {
    let grp = v <= 92 ? soft : hard;
    if (!grp.length) grp = v <= 92 ? hard : soft;
    if (!grp.length) continue;
    const orig = grp[v % grp.length];
    const had = added.has(orig);
    const smp = addSample(orig);
    if (!had) samples++;
    const z = inst.createZone(smp);
    z.keyRange = { min: g.min === lo ? 28 : g.min, max: g.max === hi ? 96 : g.max };
    z.velRange = { min: v, max: v };
    z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.002));
    z.setGenerator(GeneratorTypes.holdVolEnv, timecents(0.001));
    z.setGenerator(GeneratorTypes.decayVolEnv, timecents(1));
    z.setGenerator(GeneratorTypes.sustainVolEnv, 0);
    z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
    z.setGenerator(GeneratorTypes.initialFilterQ, 0);
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.5));
    z.setGenerator(GeneratorTypes.overridingRootKey, g.root);
    zones++;
  }
}
out.flush();
await compressBank(out, Q);
const buf = out.writeSF2({});
const file = path.join(OUT, `guitar-fsbs-${id}.sf3`);
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "キー範囲:", keys.length, "サンプル:", samples, "ゾーン:", zones, "program:", PROGRAM);
