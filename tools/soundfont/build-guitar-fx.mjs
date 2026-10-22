// 使い方: EGIPT=<egipt-fetch.py で取り出したフォルダ> node tools/soundfont/build-guitar-fx.mjs
// EG-IPT（M. Fiorini, N. Brochec, J. Borg, R. Pasini、2025。CC BY 4.0・クレジット必要。doi:10.5281/zenodo.15205644）の
// Gibson SG（ハムバッカー・ブリッジ側）の DI 録音（96kHz/24bit）から、「ギターの飾り」の音を選んで1つの SF3 にする。
//   assets-src/soundfont/extra/guitar-fx-egipt.sf3
// DI（アンプを通す前の音）なので、パートの amp（歪みのアンプ・NAM）に通して使う。コーラスは掛けない。
// 中身（どれも作曲ソフトのパートの patch で選ぶ）:
//   guitarFx（GM 15）: 鍵盤で種類を選ぶ（音程は変わらない）
//     C2＝ピックスクレイプ（長い・強い）・C#2＝ピックスクレイプ（長い）・D2＝ピックスクレイプ（短い）・D#2＝ピックスクレイプ（短い2）
//     E2＝指で弦をこする（長い）・F2＝指で弦をこする（短い）・F#2＝弦を手でたたく（ジャッ）・G2＝弦を手でたたく2・G#2＝ボディを手でたたく
//     E3〜E6: ナチュラルハーモニクス（鳴る高さの鍵盤に置いた本物の倍音。録音のある高さ: E3 A3 B3 D4 E4 G4 A4 B4 D5 E5 F#5 G5 B5 E6。間の鍵盤は近い録音の音程をずらす）
//   guitarSlideUp（GM 22）: 書いた音を弾き、約0.4秒後に全音（2半音）上へすべる（A#3〜G5 の録音。外は音程をずらす）
//   guitarSlideDown（GM 64）: 書いた音を弾き、約0.4秒後に全音下へすべる（A#3〜A5）
// 元の録音はリポジトリに入れない（tools/soundfont/egipt-fetch.py で必要な分だけ取り出す）。耳での確かめは別。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
import { loadBank, compressBank, timecents, BasicSoundBank, GeneratorTypes, emptyPresetFrom, SR } from "./lib.mjs";
import { BasicSample, SampleTypes } from "spessasynth_core";

const DIR = process.env.EGIPT ?? "/tmp/egipt/fx";
const OUT = path.resolve("assets-src/soundfont/extra");
const file = (tech, name) => path.join(DIR, `EG-IPT__HB-bridge__DI__${tech}__HB-bridge_${name}_DI.wav`);
const decode = (f, sec, fade) => {
  const buf = execFileSync("ffmpeg", ["-v", "error", "-i", f, "-t", String(sec), "-ac", "1", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  const d = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  // 頭の無音を、出だしの 3ms 手前まで切る
  let pk = 0; for (const v of d) pk = Math.max(pk, Math.abs(v));
  let on = 0; while (on < d.length && Math.abs(d[on]) < pk * 0.05) on++;
  const out = d.slice(Math.max(0, on - Math.round(0.003 * SR)));
  const n = Math.min(out.length, Math.round(fade * SR));
  for (let i = 0; i < n; i++) out[out.length - n + i] *= (1 - i / n) ** 2;
  return { data: out, peak: pk };
};

// 鍵盤の飾り（キー, 技, 名前, 長さ秒, 終わりのフェード秒）
const NOISES = [
  [36, "scratch", "scratch-card_172-65", 3.2, 0.6], [37, "scratch", "scratch-card_172-52", 3.4, 0.6],
  [38, "scratch", "scratch-card_172-58", 0.5, 0.15], [39, "scratch", "scratch-card_172-64", 0.4, 0.12],
  [40, "scratch", "scratch-fingers_169-06", 3.0, 0.6], [41, "scratch", "scratch-fingers_169-16", 0.7, 0.2],
  [42, "palmstrike", "palmstrike-strings_175-04", 1.5, 0.5], [43, "palmstrike", "palmstrike-strings_175-06", 1.5, 0.5],
  [44, "palmstrike", "palmstrike-body_178-06", 1.2, 0.4],
];
// ナチュラルハーモニクス（鳴る高さ, 名前）。音程は測って確かめた（docs/sound/guitar-fx-egipt.md）
const HARM = [[52, "31-02_6s"], [57, "32-02_5s"], [59, "31-04_6s"], [62, "33-02_4s"], [64, "32-04_5s"], [67, "34-02_3s"], [69, "32-06_5s"],
  [71, "31-10_6s"], [74, "34-04_3s"], [76, "36-02_1s"], [78, "35-04_2s"], [79, "34-06_3s"], [83, "36-04_1s"], [88, "36-06_1s"]];
// 全音スライド（弾きはじめの高さ, 名前）
const UP = [];
for (let i = 0; i < 4; i++) UP.push([56 + i, `70-${String(2 + 2 * i).padStart(2, "0")}_3s`]);
for (let i = 0; i < 20; i++) UP.push([60 + i, `71-${String(2 + 2 * i).padStart(2, "0")}_2s`]);
const DOWN = [];
for (let i = 0; i < 4; i++) DOWN.push([58 + i, `70-${String(i === 0 ? 79 : 80 - 2 * i).padStart(2, "0")}_3s`]);
for (let i = 0; i < 20; i++) DOWN.push([62 + i, `71-${String(i === 0 ? 79 : 80 - 2 * i).padStart(2, "0")}_2s`]);

const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Guitar FX EG-IPT (CC BY 4.0)" };
const mk = (name, key, data) => { const s = new BasicSample(name.slice(0, 19), SR, key, 0, SampleTypes.monoSample, 0, 0); s.setAudioData(data, SR); out.addSamples(s); return s; };
const zone = (inst, smp, lo, hi, root, rel) => {
  const z = inst.createZone(smp);
  z.keyRange = { min: lo, max: hi };
  z.setGenerator(GeneratorTypes.overridingRootKey, root);
  z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(rel));
  z.setGenerator(GeneratorTypes.reverbEffectsSend, 0);
  z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
};
// 楽器の入れもの（game.sf3 にある別々の楽器を写して番号をつけかえる。同じものを写すと中身を共有してしまう）
const preset = (srcProgram, program, name) => {
  const p = emptyPresetFrom(base, out, { program: srcProgram });
  p.program = program; p.name = name;
  // 元の楽器は鍵盤の範囲ごとに別の楽器（ゾーン）を重ねているので、最初の1つだけ残して全部の鍵盤に広げる（残すと元の音が混ざる）
  while (p.zones.length > 1) p.deleteZone(p.zones.length - 1);
  p.zones[0].keyRange = { min: 0, max: 127 };
  p.zones[0].velRange = { min: 0, max: 127 };
  const inst = p.zones[0].instrument;
  while (inst.zones.length) inst.deleteZone(0, true);
  // 元の楽器の全体設定（コーラスの送り・音の減り方・フィルターなど）を消す。残すとコーラスが掛かったり、音が消えたりする
  inst.globalZone.generators.length = 0; inst.globalZone.modulators.length = 0;
  p.globalZone.generators.length = 0; p.globalZone.modulators.length = 0;
  p.zones[0].generators.length = 0;
  return inst;
};
// ギターの飾りは、DI の大きさのまま（強さの違いは保つ）だと静かすぎるものがあるので、種類ごとに山を -6dB にそろえる
const norm = (d, pk, target = 0.5) => { const g = target / Math.max(pk, 1e-6); for (let i = 0; i < d.length; i++) d[i] *= g; return d; };

const fx = preset(27, 15, "Guitar FX");
for (const [key, tech, name, sec, fade] of NOISES) {
  const { data, peak } = decode(file(tech, name), sec, fade);
  zone(fx, mk(name, key, norm(data, peak)), key, key, key, Math.min(0.6, fade));
}
HARM.forEach(([key, name], i) => {
  const { data, peak } = decode(file("harmonics", "nat-harmonic_" + name), 4.0, 0.8);
  const lo = i === 0 ? 50 : Math.floor((HARM[i - 1][0] + key) / 2) + 1, hi = i === HARM.length - 1 ? 96 : Math.floor((HARM[i + 1][0] + key) / 2);
  zone(fx, mk("harm " + name, key, norm(data, peak, 0.45)), lo, hi, key, 1.2);
});
const slides = (srcProgram, program, label, list, tech) => {
  const inst = preset(srcProgram, program, label);
  list.forEach(([key, name], i) => {
    const { data, peak } = decode(file("slide", `slide-wholetone_${name}`), 1.6, 0.4);
    const lo = i === 0 ? key - 4 : key, hi = i === list.length - 1 ? key + 4 : key;
    zone(inst, mk(`${tech} ${name}`, key, norm(data, peak)), lo, hi, key, 0.3);
  });
};
slides(29, 22, "Guitar Slide Up", UP, "up");
slides(30, 64, "Guitar Slide Down", DOWN, "dn");
out.flush();
await compressBank(out, 5);
const buf = out.writeSF2({});
const dst = path.join(OUT, "guitar-fx-egipt.sf3");
fs.writeFileSync(dst, Buffer.from(buf));
console.log("書き出し:", dst, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "飾り", NOISES.length, "倍音", HARM.length, "スライド", UP.length + DOWN.length);
