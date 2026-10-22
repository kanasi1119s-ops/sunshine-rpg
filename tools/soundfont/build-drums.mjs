// 使い方: node tools/soundfont/build-drums.mjs
// Muldjord Kit（Lars Muldjord / DrumGizmo。CC BY 4.0）の元素材を、GMのドラムセット（0・8・16・32）の音を入れかえる小さなSoundFontにする。
//   assets-src/soundfont/extra/drums-muldjord.sf3（標準）と、ジャンル別の drums-rock / drums-metal / drums-jpop .sf3（同じ録音のまぜ方・音の長さ・イコライザー・コンプレッサーを変えたもの）
// 使い方: node --experimental-strip-types tools/soundfont/build-drums.mjs [std|rock|metal|jpop ...]（省略は全部）
// 元素材: 設定ファイル（Data/）は assets-src/soundfont/extra/src/muldjord/ に置いてある。録音（Samples/、約340MB）は大きいので git には入れない。
//   git clone https://github.com/sfzinstruments/DrumGizmo.MuldjordKit し、環境変数 MULDJORD_SAMPLES に DrumGizmo/MuldjordKit/Samples のパスを渡す。
// 元はマイク16本ぶんの録音。ここでは各ドラムを「近くのマイク＋オーバーヘッド＋部屋の音」をまぜたステレオ1組にし、
// 強さ（ベロシティ）の層ごとに1つずつ（ラウンドロビンは使わない）、必要な長さだけ切り出す。
//
// 2026-10-22 CrocellKit（DrumGizmo。録音 JBOSound／サンプリング Lars Muldjord。CC BY 4.0）にも対応（--kit crocell）:
//   node tools/soundfont/build-drums.mjs --kit crocell [crocell crocell-aux]
//   前処理 tools/soundfont/dg-extract.py が、DrumGizmo 本家の形式（楽器の XML と多チャンネル WAV）から、必要な打音の頭だけを取り出して
//   Muldjord と同じ並び（Data/region/*.txt・Data/macro.txt と Samples/<楽器>/<番号>-<楽器>-<マイク>.flac）に直す。
//   Data/ は assets-src/soundfont/extra/src/crocell/ に置く。録音は環境変数 CROCELL_SAMPLES（git には入れない）。
//   crocell-aux は、補助打楽器（タンバリン・カウベルなどの録音）を drums-muldjord-aux.sf3 から引きつぐ。
import fs from "fs";
import path from "path";
import { decodeMono, filterStereo, loadBank, stereoPair, timecents, compressBank, SR, BasicSoundBank, GeneratorTypes } from "./lib.mjs";

const KIT_ID = process.argv.includes("--kit") ? process.argv[process.argv.indexOf("--kit") + 1] : "muldjord";
const SRC = path.resolve(`assets-src/soundfont/extra/src/${KIT_ID}`);
const OUT = path.resolve("assets-src/soundfont/extra");
const SAMPLES = KIT_ID === "crocell"
  ? process.env.CROCELL_SAMPLES ?? "/tmp/crocell/Samples"
  : process.env.MULDJORD_SAMPLES ?? "/home/claude/sfzinstruments/drumgizmo.muldjordkit/DrumGizmo/MuldjordKit/Samples";
// 環境変数: DRUM_RR＝強さの層ごとに使う録音の数（1＝これまでどおり）、DRUM_Q＝Vorbis の品質（0〜10、既定 4）
const RR = Number(process.env.DRUM_RR ?? (KIT_ID === "crocell" ? 2 : 1));
const Q = Number(process.env.DRUM_Q ?? 4);
const gameBank = loadBank(path.resolve("src/audio/soundfont/game.sf3"));

// 元の速度の層（$v51l など）
const VEL = {};
for (const m of fs.readFileSync(path.join(SRC, "Data/macro.txt"), "utf8").matchAll(/#define \$(v\d+)([lh]) (\d+)/g)) (VEL[m[1]] ??= {})[m[2]] = Number(m[3]);

// 楽器ごとの設定: GMのキー、使う近接マイクと音量、近接マイクの左右の位置(-1〜1)、切り出す長さ(秒)、同じ「ハイハットのグループ」か
//   vel: [最小, 最大]＝この楽器の強さの層を、この範囲に詰める（同じキーで、強い打ちだけ別の録音にするとき）
//   release: 鍵盤を離したあとの減り方（秒。省略 0.3）。シンバルは長くして、すぐ止めない（人間の決まり）
const KITS = {
  muldjord: {
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
  },
  // CrocellKit（2018年のメタルのアルバム録音のキット）。GM の番号に合わせ、GM に無いシンバルは 88 番より上の空きキーに置く（docs/sound/drum-keys-crocell.md）
  //   止め打ち（93・94）は、同じクラッシュ（49・57）の余韻を止める（exclusive）。
//   キックは中のマイク（Beta 91A＝アタック）と外のマイク（E602＝胴の重み）をまぜる。スネアのいちばん強い打ち（118〜127）はリムショットの録音
  crocell: {
    KDrumL:        { keys: [35], close: { KDrumInside: 0.75, KDrumOutside: 1.0 }, pan: 0, sec: 1.0 },
    KDrumR:        { keys: [36], close: { KDrumInside: 0.75, KDrumOutside: 1.0 }, pan: 0, sec: 1.0 },
    Snare:         { keys: [38, 40], close: { SnareTop: 0.85, SnareBottom: 0.3 }, pan: 0, sec: 1.0, vel: [1, 117] },
    SnareRimShot:  { keys: [38, 40], close: { SnareTop: 0.85, SnareBottom: 0.3 }, pan: 0, sec: 1.0, vel: [118, 127] },
    SnareRim:      { keys: [37], close: { SnareTop: 0.8, SnareBottom: 0.2 }, pan: 0, sec: 0.5 },
    HihatClosed:   { keys: [42], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.6, exclusive: 1 },
    HihatPedal:    { keys: [44], close: { Hihat: 0.55 }, pan: -0.35, sec: 0.5, exclusive: 1 },
    HihatOpen:     { keys: [46], close: { Hihat: 0.55 }, pan: -0.35, sec: 2.5, exclusive: 1, release: 0.6 },
    HihatSemiOpen: { keys: [95], close: { Hihat: 0.55 }, pan: -0.35, sec: 1.5, exclusive: 1, release: 0.4 },
    FTom2:         { keys: [41], close: { FTom2: 0.75 }, pan: 0.45, sec: 2.0 },
    FTom1:         { keys: [43], close: { FTom1: 0.75 }, pan: 0.3, sec: 2.0 },
    Tom2:          { keys: [45, 47], close: { Tom2: 0.75 }, pan: 0.05, sec: 1.8 },
    Tom1:          { keys: [48, 50], close: { Tom1: 0.75 }, pan: -0.2, sec: 1.8 },
    CrashL:        { keys: [49], close: {}, pan: 0, sec: 5.5, release: 4, exclusive: 2 },
    CrashR:        { keys: [57], close: {}, pan: 0, sec: 5.5, release: 4, exclusive: 3 },
    CrashRXtra:    { keys: [92], close: {}, pan: 0, sec: 5.5, release: 4 },
    CrashLStopped: { keys: [93], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 2 },
    CrashRStopped: { keys: [94], close: {}, pan: 0, sec: 1.2, release: 0.2, exclusive: 3 },
    RideR:         { keys: [51, 59], close: { Ride: 0.45 }, pan: 0.4, sec: 3.5, release: 2 },
    RideRBell:     { keys: [53], close: { Ride: 0.45 }, pan: 0.4, sec: 3.5, release: 2 },
    ChinaR:        { keys: [52], close: {}, pan: 0, sec: 4.5, release: 3 },
    ChinaL:        { keys: [90], close: {}, pan: 0, sec: 4.5, release: 3 },
    SplashR:       { keys: [55], close: {}, pan: 0, sec: 3.0, release: 2.5 },
    SplashL:       { keys: [91], close: {}, pan: 0, sec: 3.0, release: 2.5 },
  },
};
const KIT = KITS[KIT_ID];
if (!KIT) throw new Error(`キットがありません: ${KIT_ID}`);
// ジャンル別のまぜ方。overhead／amb＝オーバーヘッド・部屋のマイクの量、kick／snare／tom／hat＝各ドラムの近接マイクの倍率、cym＝シンバルの長さの倍率、sec＝全体の長さの倍率、eq＝仕上げのフィルター（ffmpeg）
const PROFILES = {
  std:   { out: "drums-muldjord", label: "標準", overhead: 1.0, amb: 0.45, kick: 1, snare: 1, tom: 1, hat: 1, cym: 1, sec: 1, eq: "" },
  rock:  { out: "drums-rock", label: "ロック", overhead: 1.0, amb: 0.85, kick: 1.1, snare: 1.1, tom: 1.1, hat: 1, cym: 1.2, sec: 1.2,
    eq: "equalizer=f=90:t=q:w=1:g=2,equalizer=f=5000:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1.5" },
  metal: { out: "drums-metal", label: "メタル", overhead: 0.6, amb: 0.1, kick: 1.7, snare: 1.5, tom: 1.4, hat: 1, cym: 0.6, sec: 0.7,
    eq: "highpass=f=35,equalizer=f=60:t=q:w=1:g=3,equalizer=f=450:t=q:w=1.5:g=-3,equalizer=f=3500:t=q:w=1:g=4,acompressor=threshold=-22dB:ratio=4:attack=2:release=50:makeup=2" },
  jpop:  { out: "drums-jpop", label: "J-POP", overhead: 0.9, amb: 0.25, kick: 1.2, snare: 1.3, tom: 1.0, hat: 1.1, cym: 0.8, sec: 0.85,
    eq: "highpass=f=40,equalizer=f=90:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=3,equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=4:release=80:makeup=1.5" },
  // 「スープラ」: 乾いて硬い金属スネア（アルミ胴の定番スネアのような、パシッと抜ける高めの音）に寄せた設定。部屋の鳴りを減らし、スネアだけ別のイコライザーと短い余韻にする
  supra: { out: "drums-supra", label: "スープラ", overhead: 0.8, amb: 0.12, kick: 1.15, snare: 1.45, tom: 1.0, hat: 1.05, cym: 0.8, sec: 0.85, snareSec: 0.55, crashSec: 2.2, crashTail: 6,
    eq: "highpass=f=40,equalizer=f=90:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1:g=2,equalizer=f=9000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=4:release=80:makeup=1.5",
    snareEq: "highpass=f=110,equalizer=f=230:t=q:w=1.2:g=1.5,equalizer=f=420:t=q:w=1.5:g=-4,equalizer=f=1800:t=q:w=1.5:g=1.5,equalizer=f=5500:t=q:w=1:g=4.5,equalizer=f=10000:t=q:w=1:g=3,acompressor=threshold=-24dB:ratio=4:attack=1.5:release=45:makeup=2" },
  // CrocellKit: 部屋の鳴りを少し、OH の真ん中のマイクを半分。キックは 55Hz の胴の重みと 4kHz のアタック、400Hz の箱鳴りを少し引く
  crocell: { kit: "crocell", out: "drums-crocell", label: "CrocellKit", overhead: 1.0, ohc: 0.5, amb: 0.4, kick: 1.15, snare: 1.1, tom: 1.0, hat: 1, cym: 1, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    kindEq: { kick: "highpass=f=28,equalizer=f=55:t=q:w=1:g=3,equalizer=f=400:t=q:w=1.5:g=-3,equalizer=f=4000:t=q:w=1:g=2.5" } },
  // 2026-10-22 CrocellKit の「乾いてパンチのある版」（人間「空間を感じすぎる」「NEW ERA みたいなドラム」）。
  // 部屋マイクは使わない・太鼓の OH は少しだけ。作曲ソフトのドラムは1本の通り道を共有して太鼓ごとに fx を掛けられないので、
  // 太鼓ごとの音作り（EQ・1打ごとの圧縮）をここで録音に焼き込む。目標の数値は docs/sound/drum-sound-target.md
  "crocell-punch": { kit: "crocell", out: "drums-crocell-punch", label: "CrocellKit（乾いてパンチ）", overhead: 0.3, ohKind: { kick: 0.12, snare: 0.3, tom: 0.25, hat: 0.5, cym: 0.85 }, ohc: 0, amb: 0,
    kick: 1.35, snare: 0.95, tom: 0.85, hat: 0.9, cym: 0.75, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    snareEq: "highpass=f=90,equalizer=f=190:t=q:w=1:g=3,equalizer=f=650:t=q:w=1.3:g=-7,equalizer=f=5500:t=q:w=1:g=3,equalizer=f=10000:t=q:w=1:g=3,acompressor=threshold=-20dB:ratio=4:attack=3:release=60:makeup=2",
    kindEq: {
      kick: "highpass=f=45,highpass=f=45,equalizer=f=75:t=q:w=1:g=2,equalizer=f=380:t=q:w=1.2:g=-7,equalizer=f=4500:t=q:w=1:g=5,equalizer=f=8000:t=q:w=1:g=6,acompressor=threshold=-18dB:ratio=4:attack=5:release=60:makeup=2",
      tom: "highpass=f=55,equalizer=f=500:t=q:w=1.3:g=-6,equalizer=f=4000:t=q:w=1:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80",
      hat: "highpass=f=300,equalizer=f=9000:t=q:w=1:g=2",
      cym: "highpass=f=250,equalizer=f=3500:t=q:w=1:g=-3,equalizer=f=10000:t=q:w=1:g=3",
    } },
  "crocell-aux": { kit: "crocell", base: "drums-muldjord-aux", out: "drums-crocell-aux", label: "CrocellKit＋録音の小物", overhead: 1.0, ohc: 0.5, amb: 0.4, kick: 1.15, snare: 1.1, tom: 1.0, hat: 1, cym: 1, sec: 1, fade: 0.6,
    eq: "highpass=f=28",
    kindEq: { kick: "highpass=f=28,equalizer=f=55:t=q:w=1:g=3,equalizer=f=400:t=q:w=1.5:g=-3,equalizer=f=4000:t=q:w=1:g=2.5" } },
};
const which = [...new Set(process.argv.slice(2).filter((a, i, all) => all[i - 1] !== "--kit"))].filter((a) => a in PROFILES && (PROFILES[a].kit ?? "muldjord") === KIT_ID);
/** 近接マイクの倍率（楽器の種類で選ぶ） */
const kindOf = (inst) => (/^K[dD]rum/.test(inst) ? "kick" : inst.startsWith("Snare") ? "snare" : inst.startsWith("Tom") ? "tom" : inst.startsWith("Hihat") ? "hat" : "cym");

/** 元の region ファイルから、強さの層ごとの最初のサンプル番号を取り出す。 */
function layers(name) {
  const found = new Map();
  for (const line of fs.readFileSync(path.join(SRC, "Data/region", name + ".txt"), "utf8").split("\n")) {
    const m = /<region>\s+lovel=\$(v\d+)l hivel=\$(v\d+)h.*sample=\$instr\/(\d+)-/.exec(line);
    if (!m) continue;
    if (!found.has(m[1])) found.set(m[1], { v: m[1], idx: Number(m[3]), idxs: [] });
    found.get(m[1]).idxs.push(Number(m[3]));
  }
  // ラウンドロビンの代わり（2026-10-15）: SoundFont にはラウンドロビンがないので、強さの層をさらに RR 個の細い範囲に分け、
  // それぞれに同じ強さの別の録音を入れる。演奏の強さの揺れで毎回ちがう録音が鳴り、同じ音のくり返し（機関銃のような音）を減らす。
  const out = [];
  // vel の指定があるときは、元の層の範囲（1〜127）を、その範囲に詰める
  const squeeze = (v) => (KIT[name]?.vel ? Math.round(KIT[name].vel[0] + ((v - 1) * (KIT[name].vel[1] - KIT[name].vel[0])) / 126) : v);
  for (const x of found.values()) {
    const lo = squeeze(VEL[x.v].l), hi = Math.max(squeeze(VEL[x.v].l), squeeze(VEL[x.v].h));
    const n = Math.max(1, Math.min(RR, x.idxs.length, hi - lo + 1));
    for (let k = 0; k < n; k++) {
      const a = lo + Math.round(((hi - lo + 1) * k) / n), b = lo + Math.round(((hi - lo + 1) * (k + 1)) / n) - 1;
      out.push({ v: x.v, idx: x.idxs[k], lo: a, hi: b });
    }
  }
  return out;
}

function hit(inst, idx, cfg, prof) {
  const sec = cfg.sec * prof.sec * (kindOf(inst) === "cym" ? prof.cym : 1) * (/^Crash/.test(inst) && prof.crashSec ? prof.crashSec : 1) * (kindOf(inst) === "snare" && prof.snareSec ? prof.snareSec : 1);
  cfg = { ...cfg, sec };
  const file = (mic) => path.join(SAMPLES, inst, `${idx}-${inst}-${mic}.flac`);
  const read = (mic) => decodeMono(file(mic), cfg.sec);
  const len = Math.round(cfg.sec * SR);
  const L = new Float32Array(len), R = new Float32Array(len);
  const add = (buf, gl, gr) => { for (let i = 0; i < Math.min(len, buf.length); i++) { L[i] += buf[i] * gl; R[i] += buf[i] * gr; } };
  // ohKind: 楽器の種類ごとの OH（上のマイク）の量。太鼓は近接マイク中心で乾いた音に、シンバルは OH から鳴らす（crocell-punch）
  const oh = prof.ohKind?.[kindOf(inst)] ?? prof.overhead;
  add(read("OHL"), oh, 0); add(read("OHR"), 0, oh);
  add(read("AmbL"), prof.amb, 0); add(read("AmbR"), 0, prof.amb);
  if (prof.ohc && fs.existsSync(file("OHC"))) { const c = read("OHC"); add(c, prof.ohc * 0.7071, prof.ohc * 0.7071); }
  const ang = ((cfg.pan + 1) * Math.PI) / 4; // 一定パワーのパン
  const boost = prof[kindOf(inst)];
  for (const [mic, g] of Object.entries(cfg.close)) add(read(mic), g * boost * Math.cos(ang) * 1.2, g * boost * Math.sin(ang) * 1.2);
  const [fl, fr] = filterStereo(L, R, kindOf(inst) === "snare" && prof.snareEq ? prof.snareEq : prof.kindEq?.[kindOf(inst)] ?? prof.eq);
  L.set(fl.subarray(0, len)); R.set(fr.subarray(0, len));
  // クラッシュの余韻をのばす: 録音の減り方（約-18dB/秒）をゆるやかにするため、時間とともに音量を持ち上げる（上限 +36dB）
  if (/^Crash/.test(inst) && prof.crashTail) {
    for (let i = 0; i < len; i++) { const g = Math.pow(10, Math.min(36, (prof.crashTail * i) / SR) / 20); L[i] *= g; R[i] *= g; }
  }
  // 終わりを 0.12秒かけて静かにする
  const fade = Math.round(Math.min(cfg.sec * 0.4, (/^Crash/.test(inst) && prof.crashSec) || (prof.fade && kindOf(inst) === "cym") ? prof.fade ?? 0.6 : 0.12) * SR);
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
  const base = prof.base ? loadBank(path.join(OUT, prof.base + ".sf3")) : gameBank;
  out.soundBankInfo = { ...gameBank.soundBankInfo, name: KIT_ID === "crocell" ? `Drums ${prof.label} (DrumGizmo CrocellKit, CC BY 4.0)` : `Drums Muldjord Kit ${prof.label} (CC BY 4.0)` };
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
            // クラッシュは、叩いた直後に鍵盤を離しても余韻が鳴り続けるよう、離したあとの減り方を長くする（crashSec のある設定だけ）
            z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(/^Crash/.test(m.inst) && prof.crashSec ? 12 : m.cfg.release ?? 0.3));
            if (m.cfg.exclusive) z.setGenerator(GeneratorTypes.exclusiveClass, m.cfg.exclusive);
          }
        }
      }
    }
  }
  out.flush();
  await compressBank(out, Q);
  const buf = out.writeSF2({});
  const file = path.join(OUT, prof.out + ".sf3");
  fs.writeFileSync(file, Buffer.from(buf));
  console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");

}
for (const name of which.length ? which : Object.keys(PROFILES).filter((n) => (PROFILES[n].kit ?? "muldjord") === KIT_ID)) await build(name, PROFILES[name]);
