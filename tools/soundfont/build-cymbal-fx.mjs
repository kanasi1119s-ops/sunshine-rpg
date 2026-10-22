// 使い方: node tools/soundfont/build-cymbal-fx.mjs <cymbal-fx-prep.py の作業フォルダ>
// 本物のシンバルの効果音（逆再生・スウェル・長い一打）を、作曲ソフトの楽器 cymbalFx（GM 127）の SF3 にする。合成音は使わない。
//   assets-src/soundfont/extra/fx-cymbal-real.sf3
// 鍵盤（SF3 の中の並び。曲の中では音名で書けば、書き出し〔midi-export.ts〕が長さに合う鍵盤を選ぶ）:
//   36〜44: 逆再生クラッシュ（長さ 0.25・0.35・0.5・0.7・1・1.4・2・2.8・4 秒）
//   48〜56: 逆再生チャイナ（同じ長さ）
//   60〜70: スウェル（サスペンデッドシンバルのマレットのロールのクレッシェンド。0.25〜8 秒の 11 段）
//   72＝クラッシュ1の一打・73＝クラッシュ2・74＝チャイナ1・75＝チャイナ2・76＝サスペンデッドシンバルのふちの強打・77＝ロールのディミヌエンド（約21秒）
// 元: CrocellKit（DrumGizmo。CC BY 4.0）とオスロ大学 fourMs Lab の Cymbal percussion（CC BY 4.0）。どちらもクレジット必要。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";
import { loadBank, compressBank, timecents, BasicSoundBank, GeneratorTypes, emptyPresetFrom, SR, stereoPair } from "./lib.mjs";

const work = process.argv[2] ?? "/tmp/cymfx";
const list = JSON.parse(fs.readFileSync(path.join(work, "out/list.json"), "utf8"));
const read = (name) => {
  const buf = execFileSync("ffmpeg", ["-v", "error", "-i", path.join(work, "out", name + ".wav"), "-ac", "2", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 30 });
  const all = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
  const n = all.length >> 1, L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = all[2 * i]; R[i] = all[2 * i + 1]; }
  return [L, R];
};
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Real Cymbal FX (CrocellKit / UiO fourMs, CC BY 4.0)" };
// GM 119（Reverse Cymbal）の入れものを写して 127 に。元の楽器の全体設定（コーラス・減り方など）は消す
const p = emptyPresetFrom(base, out, { program: 119 });
p.program = 127; p.name = "Real Cymbal FX";
while (p.zones.length > 1) p.deleteZone(p.zones.length - 1);
p.zones[0].keyRange = { min: 0, max: 127 }; p.zones[0].velRange = { min: 0, max: 127 };
p.globalZone.generators.length = 0; p.globalZone.modulators.length = 0; p.zones[0].generators.length = 0;
const inst = p.zones[0].instrument;
while (inst.zones.length) inst.deleteZone(0, true);
inst.globalZone.generators.length = 0; inst.globalZone.modulators.length = 0;

const HITS = { "hit-crash": 72, "hit-crash2": 73, "hit-china": 74, "hit-china2": 75, "hit-susp": 76, "roll-dim": 77 };
const keyOf = (it) => {
  const idx = list.lens.indexOf(it.len);
  if (it.kind === "revcrash") return 36 + idx;
  if (it.kind === "revchina") return 48 + idx;
  if (it.kind === "swell") return 60 + idx;
  return HITS[it.name];
};
let n = 0;
for (const it of list.items) {
  const key = keyOf(it);
  if (key === undefined) continue;
  const [L, R] = read(it.name);
  const [l, r] = stereoPair(it.name, L, R, key);
  out.addSamples(l, r);
  for (const s of [l, r]) {
    const z = inst.createZone(s);
    z.keyRange = { min: key, max: key };
    z.setGenerator(GeneratorTypes.overridingRootKey, key);
    z.setGenerator(GeneratorTypes.pan, s === l ? -500 : 500);
    // 逆再生・スウェルは「山」で終わるので離したらすぐ止める。一打は鳴らしきる（シンバルの余韻はすぐ止めない）
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(it.kind === "hit" ? 4 : 0.03));
    z.setGenerator(GeneratorTypes.reverbEffectsSend, 0);
    z.setGenerator(GeneratorTypes.chorusEffectsSend, 0);
  }
  n++;
}
out.flush();
await compressBank(out, 5);
const buf = out.writeSF2({});
const dst = path.resolve("assets-src/soundfont/extra/fx-cymbal-real.sf3");
fs.writeFileSync(dst, Buffer.from(buf));
console.log("書き出し:", dst, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "音:", n);
