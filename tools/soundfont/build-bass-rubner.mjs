// 使い方: RUBNER=<dsmolken.double-bass のフォルダ> node --experimental-strip-types tools/soundfont/build-bass-rubner.mjs
// ジャズのウッドベース（1958年 Otto Rubner のコントラバスのピチカート。D. Smolken。royalty-free）を、SoundFont（assets-src/soundfont/extra/bass-upright-rubner.sf3）にする。
// 元素材（約530MB）はgitに入れない: git clone https://github.com/sfzinstruments/dsmolken.double-bass
// 2026-10-27 の直し: これまでは GM 33 だけに入れていたが、曲の「ロック」設定（style 未指定）ではベースが GM 34 で鳴るため、
//   ウッドベースは一度も鳴らず、標準のベース（ゆっくり立ち上がるシンセ寄りの音）になっていた。32・33・34 のすべてに入れる。
// 強さは 3層（弱 1〜74・中 75〜120・強 121〜127）。録音は各層のラウンドロビン a を使う。1音ずつ 3.2 秒で切り、終わりをなめらかに消す。
import fs from "fs";
import path from "path";
import { decodeMono, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const SRC = process.env.RUBNER ?? "/home/claude/sfzinstruments/dsmolken.double-bass";
const OUT = path.resolve("assets-src/soundfont/extra");
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const PROGRAMS = [32, 33, 34];
const LAYERS = [{ id: "p", lo: 1, hi: 74 }, { id: "m", lo: 75, hi: 120 }, { id: "f", lo: 121, hi: 127 }];
const SEC = 3.2;

// SFZ から、音ごとの鍵盤の範囲と基準の音を読む（ノイズ類は使わない）
const notes = new Map();
let cur = null;
for (const raw of fs.readFileSync(path.join(SRC, "_pizz.sfz"), "utf8").split("\n")) {
  const line = raw.replace(/\/\/.*$/, "").trim();
  if (line.startsWith("<region>")) cur = {}; else if (line.startsWith("<")) { cur = null; continue; }
  if (!cur) continue;
  for (const m of line.matchAll(/(\w+)=(.*?)(?=\s+\w+=|$)/g)) cur[m[1]] = m[2].trim();
  if (cur.sample && cur.lokey && cur.hikey && cur.pitch_keycenter) {
    const m = /^pizz\/pizz_([a-z]+\d)_([pmf])a\.wav$/.exec(cur.sample);
    if (m) notes.set(m[1], { lo: Number(cur.lokey), hi: Number(cur.hikey), root: Number(cur.pitch_keycenter) });
  }
}
const list = [...notes.entries()].sort((a, b) => a[1].root - b[1].root);
console.log("音の数:", list.length, list.map(([n]) => n).join(" "));
// 最低音と最高音は、鍵盤の端まで広げる（録音より低い／高い音が無音にならないように）
list[0][1].lo = 21;
list[list.length - 1][1].hi = 84;

const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Bass Upright Rubner (D. Smolken)" };
const samples = [];
for (const [name, k] of list) {
  for (const L of LAYERS) {
    const file = path.join(SRC, "pizz", `pizz_${name}_${L.id}a.wav`);
    if (!fs.existsSync(file)) { console.warn("無い:", file); continue; }
    const data = decodeMono(file, SEC);
    const fade = Math.min(data.length, Math.round(0.4 * 44100));
    for (let i = 0; i < fade; i++) data[data.length - 1 - i] *= i / fade;
    const smp = monoSample(`pizz_${name}_${L.id}`, data, k.root);
    out.addSamples(smp);
    samples.push({ smp, ...k, vlo: L.lo, vhi: L.hi });
  }
}
let zones = 0;
for (const program of PROGRAMS) {
  const preset = emptyPresetFrom(base, out, { program });
  preset.name = "Bass Upright Rubner";
  const inst = preset.zones[0].instrument;
  while (inst.zones.length) inst.deleteZone(0, true);
  for (const s of samples) {
    const z = inst.createZone(s.smp);
    z.keyRange = { min: s.lo, max: s.hi };
    z.velRange = { min: s.vlo, max: s.vhi };
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.3));
    z.setGenerator(GeneratorTypes.overridingRootKey, s.root);
    zones++;
  }
}
out.flush();
await compressBank(out, 6);
const buf = out.writeSF2({});
const file = path.join(OUT, "bass-upright-rubner.sf3");
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "ゾーン:", zones);
