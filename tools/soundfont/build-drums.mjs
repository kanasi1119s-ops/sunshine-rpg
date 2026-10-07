// 使い方: node tools/soundfont/build-drums.mjs
// Muldjord Kit（Lars Muldjord / DrumGizmo。CC BY 4.0）の元素材を、GMのドラムセット（0・8・16・32）の音を入れかえる小さなSoundFontにする。
//   assets-src/soundfont/extra/drums-muldjord.sf3（標準）と、ジャンル別の drums-rock / drums-metal / drums-jpop .sf3（同じ録音のまぜ方・音の長さ・イコライザー・コンプレッサーを変えたもの）
// 使い方: node --experimental-strip-types tools/soundfont/build-drums.mjs [std|rock|metal|jpop ...]（省略は全部）
// 元素材: 設定ファイル（Data/）は assets-src/soundfont/extra/src/muldjord/ に置いてある。録音（Samples/、約340MB）は大きいので git には入れない。
//   git clone https://github.com/sfzinstruments/DrumGizmo.MuldjordKit し、環境変数 MULDJORD_SAMPLES に DrumGizmo/MuldjordKit/Samples のパスを渡す。
// 元はマイク16本ぶんの録音。ここでは各ドラムを「近くのマイク＋オーバーヘッド＋部屋の音」をまぜたステレオ1組にし、
// 強さ（ベロシティ）の層ごとに1つずつ（ラウンドロビンは使わない）、必要な長さだけ切り出す。
import fs from "fs";
import path from "path";
import { decodeMono, filterStereo, loadBank, stereoPair, timecents, compressBank, SR, BasicSoundBank, GeneratorTypes } from "./lib.mjs";

const SRC = path.resolve("assets-src/soundfont/extra/src/muldjord");
const OUT = path.resolve("assets-src/soundfont/extra");
const SAMPLES = process.env.MULDJORD_SAMPLES ?? "/home/claude/sfzinstruments/drumgizmo.muldjordkit/DrumGizmo/MuldjordKit/Samples";
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));

// 元の速度の層（$v51l など）
const VEL = {};
for (const m of fs.readFileSync(path.join(SRC, "Data/macro.txt"), "utf8").matchAll(/#define \$(v\d+)([lh]) (\d+)/g)) (VEL[m[1]] ??= {})[m[2]] = Number(m[3]);

// 楽器ごとの設定: GMのキー、使う近接マイクと音量、近接マイクの左右の位置(-1〜1)、切り出す長さ(秒)、同じ「ハイハットのグループ」か
const KIT = {
  KdrumL:      { keys: [35], close: { KdrumL: 0.9, KdrumR: 0.9 }, pan: 0, sec: 0.9 },
  KdrumR:      { keys: [36], close: { KdrumL: 0.9, KdrumR: 0.9 }, pan: 0, sec: 0.9 },
  Snare:       { keys: [38, 40], close: { Snare_top: 0.8, Snare_bottom: 0.25 }, pan: 0, sec: 0.9 },
  SnareRest:   { keys: [37], close: { Snare_top: 0.8, Snare_bottom: 0.25 }, pan: 0, sec: 0.6 },
  HihatClosed: { keys: [42, 44], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.45, exclusive: 1 },
  HihatOpen:   { keys: [46], close: { Hihat: 0.55 }, pan: -0.35, sec: 1.8, exclusive: 1 },
  Tom4:        { keys: [41, 43], close: { Tom4: 0.7 }, pan: 0.4, sec: 1.6 },
  Tom3:        { keys: [45], close: { Tom3: 0.7 }, pan: 0.2, sec: 1.6 },
  Tom2:        { keys: [47], close: { Tom2: 0.7 }, pan: -0.1, sec: 1.6 },
  Tom1:        { keys: [48, 50], close: { Tom1: 0.7 }, pan: -0.3, sec: 1.6 },
  CrashL:      { keys: [49], close: {}, pan: 0, sec: 3.0 },
  CrashR:      { keys: [57], close: {}, pan: 0, sec: 3.0 },
  RideR:       { keys: [51], close: { RideR: 0.5 }, pan: 0.4, sec: 2.2 },
  RideL:       { keys: [59], close: { RideL: 0.5 }, pan: -0.3, sec: 2.2 },
  RideRBell:   { keys: [53], close: { RideR: 0.5 }, pan: 0.4, sec: 1.8 },
  RideLBell:   { keys: [55], close: { RideL: 0.5 }, pan: -0.3, sec: 1.8 },
  China:       { keys: [52], close: {}, pan: 0, sec: 2.5 },
};
// ジャンル別のまぜ方。overhead／amb＝オーバーヘッド・部屋のマイクの量、kick／snare／tom／hat＝各ドラムの近接マイクの倍率、cym＝シンバルの長さの倍率、sec＝全体の長さの倍率、eq＝仕上げのフィルター（ffmpeg）
const PROFILES = {
  std:   { out: "drums-muldjord", label: "標準", overhead: 1.0, amb: 0.45, kick: 1, snare: 1, tom: 1, hat: 1, cym: 1, sec: 1, eq: "" },
  rock:  { out: "drums-rock", label: "ロック", overhead: 1.0, amb: 0.85, kick: 1.1, snare: 1.1, tom: 1.1, hat: 1, cym: 1.2, sec: 1.2,
    eq: "equalizer=f=90:t=q:w=1:g=2,equalizer=f=5000:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1.5" },
  metal: { out: "drums-metal", label: "メタル", overhead: 0.6, amb: 0.1, kick: 1.7, snare: 1.5, tom: 1.4, hat: 1, cym: 0.6, sec: 0.7,
    eq: "highpass=f=35,equalizer=f=60:t=q:w=1:g=3,equalizer=f=450:t=q:w=1.5:g=-3,equalizer=f=3500:t=q:w=1:g=4,acompressor=threshold=-22dB:ratio=4:attack=2:release=50:makeup=2" },
  jpop:  { out: "drums-jpop", label: "J-POP", overhead: 0.9, amb: 0.25, kick: 1.2, snare: 1.3, tom: 1.0, hat: 1.1, cym: 0.8, sec: 0.85,
    eq: "highpass=f=40,equalizer=f=90:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=3,equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=4:release=80:makeup=1.5" },
};
const which = process.argv.slice(2).filter((a) => a in PROFILES);
/** 近接マイクの倍率（楽器の種類で選ぶ） */
const kindOf = (inst) => (inst.startsWith("Kdrum") ? "kick" : inst.startsWith("Snare") ? "snare" : inst.startsWith("Tom") ? "tom" : inst.startsWith("Hihat") ? "hat" : "cym");

/** 元の region ファイルから、強さの層ごとの最初のサンプル番号を取り出す。 */
function layers(name) {
  const found = new Map();
  for (const line of fs.readFileSync(path.join(SRC, "Data/region", name + ".txt"), "utf8").split("\n")) {
    const m = /<region>\s+lovel=\$(v\d+)l hivel=\$(v\d+)h.*sample=\$instr\/(\d+)-/.exec(line);
    if (m && !found.has(m[1])) found.set(m[1], { v: m[1], idx: Number(m[3]) });
  }
  return [...found.values()].map((x) => ({ ...x, lo: VEL[x.v].l, hi: VEL[x.v].h }));
}

function hit(inst, idx, cfg, prof) {
  const sec = cfg.sec * prof.sec * (kindOf(inst) === "cym" ? prof.cym : 1);
  cfg = { ...cfg, sec };
  const file = (mic) => path.join(SAMPLES, inst, `${idx}-${inst}-${mic}.flac`);
  const read = (mic) => decodeMono(file(mic), cfg.sec);
  const len = Math.round(cfg.sec * SR);
  const L = new Float32Array(len), R = new Float32Array(len);
  const add = (buf, gl, gr) => { for (let i = 0; i < Math.min(len, buf.length); i++) { L[i] += buf[i] * gl; R[i] += buf[i] * gr; } };
  add(read("OHL"), prof.overhead, 0); add(read("OHR"), 0, prof.overhead);
  add(read("AmbL"), prof.amb, 0); add(read("AmbR"), 0, prof.amb);
  const ang = ((cfg.pan + 1) * Math.PI) / 4; // 一定パワーのパン
  const boost = prof[kindOf(inst)];
  for (const [mic, g] of Object.entries(cfg.close)) add(read(mic), g * boost * Math.cos(ang) * 1.2, g * boost * Math.sin(ang) * 1.2);
  const [fl, fr] = filterStereo(L, R, prof.eq);
  L.set(fl.subarray(0, len)); R.set(fr.subarray(0, len));
  // 終わりを 0.12秒かけて静かにする
  const fade = Math.round(0.12 * SR);
  for (let i = 0; i < fade; i++) { const g = i / fade; L[len - 1 - i] *= g; R[len - 1 - i] *= g; }
  return [L, R];
}

async function build(name, prof) {
  // 1. 全部の音をまぜて作り、全体の大きさ（山）をそろえる
  const made = [];
  let peak = 0;
  for (const [inst, cfg] of Object.entries(KIT)) {
    const ls = layers(inst);
    for (const l of ls) {
      const [L, R] = hit(inst, l.idx, cfg, prof);
      for (const b of [L, R]) for (const v of b) peak = Math.max(peak, Math.abs(v));
      made.push({ inst, cfg, ...l, L, R });
    }
    console.log(inst, "層:", ls.length);
  }
  const gain = 0.95 / peak;
  for (const m of made) for (const b of [m.L, m.R]) for (let i = 0; i < b.length; i++) b[i] *= gain;

  // 2. 音源を組み立てる（GMのドラムセットの入れものを写し、鳴らすキーだけ入れかえる。ほかのキー（カウベルなど）は元のまま）
  const out = new BasicSoundBank();
  out.soundBankInfo = { ...base.soundBankInfo, name: `Drums Muldjord Kit ${prof.label} (CC BY 4.0)` };
  const mine = new Set(Object.values(KIT).flatMap((k) => k.keys));
  const done = new Set();
  // 音のデータは1回だけ作り、4つのドラムセットで共有する
  for (const m of made) {
    [m.l, m.r] = stereoPair(`${m.inst} v${m.lo}`, m.L, m.R, m.cfg.keys[0]);
    out.addSamples(m.l, m.r);
  }
  for (const program of [0, 8, 16, 32]) {
    const src = base.presets.find((p) => p.isGMGSDrum && p.program === program);
    if (!src) continue;
    const preset = out.clonePreset(src);
    for (const pz of preset.zones) {
      const inst = pz.instrument;
      if (done.has(inst)) continue;
      done.add(inst);
      for (let i = inst.zones.length - 1; i >= 0; i--) {
        const r = inst.zones[i].keyRange;
        if ([...mine].some((k) => k >= r.min && k <= r.max)) inst.deleteZone(i, true);
      }
      for (const m of made) {
        const { l, r } = m;
        for (const key of m.cfg.keys) {
          for (const smp of [l, r]) {
            const z = inst.createZone(smp);
            z.keyRange = { min: key, max: key };
            z.velRange = { min: m.lo, max: m.hi };
            z.setGenerator(GeneratorTypes.scaleTuning, 0);
            z.setGenerator(GeneratorTypes.pan, smp === l ? -500 : 500);
            z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.3));
            if (m.cfg.exclusive) z.setGenerator(GeneratorTypes.exclusiveClass, m.cfg.exclusive);
          }
        }
      }
    }
  }
  out.flush();
  await compressBank(out, 4);
  const buf = out.writeSF2({});
  const file = path.join(OUT, prof.out + ".sf3");
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");

}
for (const name of which.length ? which : Object.keys(PROFILES)) await build(name, PROFILES[name]);
