// 使い方: node tools/soundfont/build-aux-percussion.mjs <入力のドラム音源.sf3> <出力.sf3> [--vcsl <VCSLの置き場>] [--wp <FreePatsのWorldPercussion.sf2>] [--q 4]
// ドラム音源（drums-*.sf3）の「補助打楽器」のキー（クラップ・タンバリン・カウベル・ボンゴ・コンガ・アゴゴ・カバサ・マラカス・シェイカー・
// ギロ・クラベス・ウッドブロック・トライアングル・スレイベル・ベルツリー・カスタネット）を、無料で商用利用できる実際の録音に差しかえる。
//   これまでの drums-*.sf3 は、キット（キック・スネア・ハイハット・タム・シンバル）だけが Muldjord Kit の録音で、
//   上の補助打楽器は GeneralUser GS（GM 標準の合成寄りの小さな音）のままだった。タンバリンやカウベルが「ゲーム機の音」に聞こえる原因。
//   ここでは VCSL（Versilian Community Sample Library。CC0）と FreePats の World percussion（CC0）の録音に置きかえる。
// 元素材（どちらも CC0。クレジット不要。docs/assets-credits.md に記録）:
//   VCSL: https://github.com/sgossner/VCSL （Idiophones/Struck Idiophones/ の Cowbells・Tambourine 1/2・Claps・Cabasa・Agogo Bells・Claves・
//         Guiro・Woodblock・Triangles・Sleigh Bells・Bell Tree・Shaker）
//   FreePats World percussion: https://freepats.zenvoid.org/Percussion/world-and-rare-percussion.html （Bongo・Conga・Maracas・Castanets・Egg shaker）
// 作りかた: 各キーに、強さの層（弱・中・強）とラウンドロビンを割り当てる。録音は ffmpeg で 44.1kHz モノにして、頭を揃え、先頭の数秒で切り、
//   元の音（GeneralUser GS）のそのキーの山（ピーク）に合わせて音量をそろえる。Vorbis（--q）で圧縮するのは追加した音だけ（元のキットの音は圧縮し直さない）。
// 耳での確かめは別（作曲ソフトで鳴らして聞く）。
import fs from "fs";
import path from "path";
import os from "os";
import { execFileSync } from "child_process";
import { SoundBankLoader, BasicSample, SampleTypes, GeneratorTypes, BasicSoundBank, BasicInstrument } from "spessasynth_core";
import { timecents } from "./lib.mjs";

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--")));
const [inFile, outFile] = pos;
if (!inFile || !outFile) { console.error("使い方: node tools/soundfont/build-aux-percussion.mjs <drums.sf3> <out.sf3> [--vcsl DIR] [--wp WorldPercussion.sf2]"); process.exit(1); }
const VCSL = opt("--vcsl", "/tmp/vcsl");
const WP = opt("--wp", "");
const Q = Number(opt("--q", 4));
const SR = 44100;
const ID = path.join(VCSL, "Idiophones", "Struck Idiophones");

// キー → 層のリスト。layer = { src: ファイル or "wp:<サンプル名の前方一致>", vel: [最小,最大], sec: 長さ, ref: 元の音との比較に使うか }
// 強さの層は 3 つまで（弱 1-60・中 61-100・強 101-127）。同じ層に複数あるものはラウンドロビン（強さの値の偶奇などで振り分け）。
const L = (dir, file, vel, sec = 1.5) => ({ src: path.join(ID, dir, file), vel, sec });
const SOFT = [1, 60], MID = [61, 100], LOUD = [101, 127], ALL = [1, 127];
const MAP = {
  39: { name: "クラップ", layers: [L("Claps", "SoloClap_vl1.wav", SOFT, 1.2), L("Claps", "SoloClap_vl2.wav", MID, 1.2), L("Claps", "SoloClap_vl3.wav", LOUD, 1.2), L("Claps", "SoloClap_vl4.wav", LOUD, 1.2)] },
  54: { name: "タンバリン", layers: [L("Tambourine 1", "Tamb1_Hit_v1_rr1_Mid.wav", SOFT, 1.2), L("Tambourine 2", "Tamb2_Hit_v1_rr1_Mid.wav", SOFT, 1.2), L("Tambourine 1", "Tamb1_Hit_v2_rr1_Mid.wav", MID, 1.4), L("Tambourine 2", "Tamb2_Hit_v2_rr2_Mid.wav", MID, 1.4), L("Tambourine 1", "Tamb1_Hit_v2_rr1_Mid.wav", LOUD, 1.4), L("Tambourine 2", "Tamb2_Hit_v2_rr2_Mid.wav", LOUD, 1.4)] },
  56: { name: "カウベル", layers: [L("Cowbells", "Cowbell1_Hit_v2_rr1_Mid.wav", SOFT, 1.5), L("Cowbells", "Cowbell1_Hit_v3_rr1_Mid.wav", MID, 1.5), L("Cowbells", "Cowbell1_Hit_v4_rr1_Mid.wav", LOUD, 1.5)] },
  67: { name: "ハイアゴゴ", layers: [L("Agogo Bells", "Agogo_High_v1_rr1_Mid.wav", SOFT, 1.5), L("Agogo Bells", "Agogo_High_v2_rr1_Mid.wav", MID, 1.5), L("Agogo Bells", "Agogo_High_v3_rr1_Mid.wav", LOUD, 1.5)] },
  68: { name: "ローアゴゴ", layers: [L("Agogo Bells", "Agogo_Low_v1_rr1_Mid.wav", [1, 80], 1.5), L("Agogo Bells", "Agogo_Low_v2_rr1_Mid.wav", [81, 127], 1.5)] },
  69: { name: "カバサ", layers: [L("Cabasa", "Cabasa1_Hit_rr1_Mid.wav", ALL, 0.6), L("Cabasa", "Cabasa1_Hit_rr2_Mid.wav", ALL, 0.6)] },
  73: { name: "ギロ（短）", layers: [L("Guiro", "Guiro_Hit_rr1_Mid.wav", ALL, 0.8), L("Guiro", "Guiro_Hit_rr2_Mid.wav", ALL, 0.8)] },
  74: { name: "ギロ（長）", layers: [L("Guiro", "Guiro_Med_rr1_Mid.wav", ALL, 1.2)] },
  75: { name: "クラベス", layers: [L("Claves", "Claves1_Hit_v1_rr1_Mid.wav", SOFT, 0.8), L("Claves", "Claves1_Hit_v2_rr1_Mid.wav", MID, 0.8), L("Claves", "Claves1_Hit_v3_rr1_Mid.wav", LOUD, 0.8)] },
  76: { name: "ハイウッドブロック", layers: [L("Woodblock", "wood_click_pp_rr1.wav", SOFT, 0.5), L("Woodblock", "wood_click_mp.wav", MID, 0.5), L("Woodblock", "wood_click_f_rr1.wav", LOUD, 0.5)] },
  80: { name: "ミュートトライアングル", layers: [L("Triangles", "Triangle1_HitM_v1_rr2_Mid.wav", SOFT, 0.8), L("Triangles", "Triangle1_HitM_v1_rr4_Mid.wav", MID, 0.8), L("Triangles", "Triangle3_HitM_v1_rr2_Mid.wav", LOUD, 0.8)] },
  81: { name: "オープントライアングル", layers: [L("Triangles", "Triangle3_Hit_v2_rr2_Mid.wav", ALL, 3), L("Triangles", "Triangle6_Hit_v2_rr1_Mid.wav", ALL, 3)] },
  82: { name: "シェイカー", layers: [L("Shaker, Small", "Mid_Shaker_Slap_rr1.wav", SOFT, 0.6), L("Shaker, Small", "Mid_Shaker_Slap_rr2.wav", MID, 0.6), L("Shaker, Large", "LShaker_Hit_rr1_Mid.wav", LOUD, 0.7)] },
  83: { name: "スレイベル", layers: [L("Sleigh Bells", "Sleighbells_Hit_rr1_Mid.wav", ALL, 2), L("Sleigh Bells", "Sleighbells_Hit_rr2_Mid.wav", ALL, 2)] },
  84: { name: "ベルツリー", layers: [L("Bell Tree/Stroke", "BellTree_Stroke_3_Mid.wav", ALL, 3.5)] },
  // FreePats World percussion（"wp:" はサンプルのMIDIキー番号。World percussion の割りあては README.txt のとおり）
  60: { name: "ハイボンゴ", layers: [{ src: "wp:52", vel: ALL, sec: 0.7 }] },
  61: { name: "ローボンゴ", layers: [{ src: "wp:53", vel: ALL, sec: 0.8 }] },
  62: { name: "ミュートハイコンガ", layers: [{ src: "wp:65", vel: ALL, sec: 0.5 }] },
  63: { name: "オープンハイコンガ", layers: [{ src: "wp:63", vel: ALL, sec: 1 }] },
  64: { name: "ローコンガ", layers: [{ src: "wp:64", vel: ALL, sec: 1 }] },
  70: { name: "マラカス", layers: [{ src: "wp:67", vel: ALL, sec: 0.4 }, { src: "wp:68", vel: ALL, sec: 0.4 }] },
  85: { name: "カスタネット", layers: [{ src: "wp:61", vel: ALL, sec: 0.6 }] },
};
const KEYS = Object.keys(MAP).map(Number);

await BasicSoundBank.isSF3DecoderReady;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "auxperc-"));
const decode = (file, sec) => {
  const buf = execFileSync("ffmpeg", ["-v", "error", "-i", file, "-t", String(sec), "-ac", "1", "-ar", String(SR), "-af", "highpass=f=30", "-f", "f32le", "-"], { maxBuffer: 1 << 28 });
  return new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
};
// 録音の頭の無音を詰める（-50dB を下回る間）
const trimHead = (d) => {
  const th = 10 ** (-50 / 20);
  let i = 0;
  while (i < d.length && Math.abs(d[i]) < th) i++;
  return d.subarray(Math.max(0, i - 24));
};
const fadeOut = (d, sec) => {
  const f = Math.min(d.length, Math.round(sec * SR));
  for (let i = 0; i < f; i++) d[d.length - f + i] *= 1 - i / f;
  return d;
};
const peakOf = (d) => { let p = 0; for (const x of d) p = Math.max(p, Math.abs(x)); return p; };

// World percussion のサンプル（SF2）から、キーごとの録音を取り出す
let wpBank = null;
const wpSamples = (key) => {
  if (!WP) return [];
  wpBank ??= SoundBankLoader.fromArrayBuffer(fs.readFileSync(WP).buffer.slice(0));
  const out = [];
  for (const z of wpBank.instruments[0].zones) {
    if (z.keyRange.min <= key && z.keyRange.max >= key) out.push(z.sample);
  }
  // ラウンドロビンの全部ではなく、先頭から最大 4 つ
  return [...new Set(out)].slice(0, 4);
};

const bank = SoundBankLoader.fromArrayBuffer(fs.readFileSync(inFile).buffer.slice(0));
// 元の音（GeneralUser GS）の、そのキーのピークを調べる（音量合わせの基準）
const refPeak = new Map();
for (const p of bank.presets.filter((x) => x.isGMGSDrum)) {
  for (const pz of p.zones) for (const iz of pz.instrument.zones) {
    for (let k = iz.keyRange.min; k <= iz.keyRange.max; k++) if (KEYS.includes(k) && !refPeak.has(k)) refPeak.set(k, peakOf(iz.sample.getAudioData()));
  }
  break;
}

const make = (key) => {
  const spec = MAP[key];
  const items = [];
  for (const ly of spec.layers) {
    let data, rate = SR;
    if (ly.src.startsWith("wp:")) {
      const ss = wpSamples(Number(ly.src.slice(3)));
      if (!ss.length) continue;
      for (const s of ss) {
        const d = Float32Array.from(s.getAudioData());
        items.push({ data: d.subarray(0, Math.round(s.sampleRate * ly.sec)), rate: s.sampleRate, vel: ly.vel, name: s.name });
      }
      continue;
    }
    if (!fs.existsSync(ly.src)) { console.warn("見つかりません:", ly.src); continue; }
    data = trimHead(decode(ly.src, ly.sec + 0.2));
    items.push({ data, rate, vel: ly.vel, name: path.basename(ly.src, ".wav") });
  }
  if (!items.length) return null;
  // 音量: その中の最も大きい録音のピークを、元の音のピーク（無ければ 0.5）に合わせる。強弱の差は録音のまま残す
  const peak = Math.max(...items.map((i) => peakOf(i.data)));
  const target = Math.min(0.9, (refPeak.get(key) ?? 0.5));
  const g = peak > 0 ? target / peak : 1;
  for (const it of items) {
    it.data = fadeOut(Float32Array.from(it.data, (x) => x * g), Math.min(0.15, it.data.length / it.rate / 3));
  }
  return items;
};

const encode = async (audio, rate) => {
  const raw = path.join(tmp, "in.f32"), ogg = path.join(tmp, "out.ogg");
  fs.writeFileSync(raw, Buffer.from(audio.buffer, audio.byteOffset, audio.byteLength));
  execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "f32le", "-ar", String(rate), "-ac", "1", "-i", raw, "-c:a", "libvorbis", "-q:a", String(Q), ogg]);
  return new Uint8Array(fs.readFileSync(ogg));
};

const made = new Map();
for (const k of KEYS) { const it = make(k); if (it) made.set(k, it); }
let nNew = 0;
// 元のドラム音源は、種類ごとの入れもの（Misc. Percussion・Hand Perc・Percussion など。プリセットごとに 8 つ前後）に分かれていて、
// プリセット側のキー範囲で振り分けている。補助打楽器のキーに当たる単独キーのゾーンを、すべての入れものから消し、
// 新しい入れもの "AuxPerc" を 1 つ作って、プリセット全体（キー範囲は制限なし）に足す。
const insts = new Set();
for (const preset of bank.presets.filter((x) => x.isGMGSDrum)) for (const pz of preset.zones) insts.add(pz.instrument);
let removed = 0;
for (const inst of insts) {
  for (let i = inst.zones.length - 1; i >= 0; i--) {
    const z = inst.zones[i];
    if (z.keyRange.min === z.keyRange.max && made.has(z.keyRange.min)) { inst.deleteZone(i, true); removed++; }
  }
}
const aux = new BasicInstrument();
aux.name = "AuxPerc";
const asciiName = { 39: "Clap", 54: "Tambourine", 56: "Cowbell", 67: "AgogoHi", 68: "AgogoLo", 69: "Cabasa", 73: "GuiroS", 74: "GuiroL", 75: "Claves", 76: "WoodblockHi", 80: "TriangleMute", 81: "TriangleOpen", 82: "Shaker", 83: "SleighBells", 84: "BellTree", 60: "BongoHi", 61: "BongoLo", 62: "CongaMute", 63: "CongaHi", 64: "CongaLo", 70: "Maracas", 85: "Castanets" };
for (const [key, items] of made) {
  // 強さの層ごとに、同じ層の録音をラウンドロビンで割り当てる（強さの値ごとにどれか 1 つ）
  for (let v = 1; v <= 127; v++) {
    const cands = items.filter((i) => v >= i.vel[0] && v <= i.vel[1]);
    if (!cands.length) continue;
    const it = cands[v % cands.length];
    if (!it.smp) {
      it.smp = new BasicSample(`${asciiName[key]} ${it.name}`.replace(/[^\x20-\x7e]/g, "").slice(0, 20), it.rate, 60, 0, SampleTypes.monoSample, 0, 0);
      it.smp.setAudioData(it.data, it.rate);
      bank.addSamples(it.smp);
      nNew++;
    }
    const z = aux.createZone(it.smp);
    z.keyRange = { min: key, max: key };
    z.velRange = { min: v, max: v };
    z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.001));
    z.setGenerator(GeneratorTypes.holdVolEnv, timecents(0.001));
    z.setGenerator(GeneratorTypes.decayVolEnv, timecents(1));
    z.setGenerator(GeneratorTypes.sustainVolEnv, 0);
    z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.4));
    z.setGenerator(GeneratorTypes.overridingRootKey, 60);
    z.setGenerator(GeneratorTypes.scaleTuning, 0);
  }
}
bank.addInstruments(aux);
for (const preset of bank.presets.filter((x) => x.isGMGSDrum)) {
  const pz = preset.createZone(aux);
  pz.keyRange = { min: 0, max: 127 };
}
bank.removeUnusedElements();
// 追加した音（まだ圧縮されていないもの）だけを Vorbis にする
for (const s of bank.samples) if (!s.isCompressed) await s.compressSample(encode);
bank.flush();
const buf = bank.writeSF2({});
fs.writeFileSync(outFile, Buffer.from(buf));
fs.rmSync(tmp, { recursive: true });
console.log("書き出し:", outFile, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "消した元ゾーン:", removed, "差しかえたキー:", [...made.keys()].join(","), "追加サンプル:", nNew);
