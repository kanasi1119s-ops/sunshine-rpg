// 使い方: SALAMANDER=<フォルダ> node --experimental-strip-types tools/soundfont/build-piano.mjs
// グランドピアノの SoundFont を作る（assets-src/soundfont/extra/piano-salamander.sf3）。GMのピアノ（0・1）を入れかえる。
//   元素材: Salamander Grand Piano V3（Alexander Holm。CC BY 3.0。**クレジット表記が必要**。https://github.com/sfzinstruments/SalamanderGrandPiano）
//   使うのは、強さ6（やわらかい）と13（強い）の2層、全88鍵のうち3半音ごとの録音（60ファイル）。モノラルにして約7秒で切る。
import fs from "fs";
import path from "path";
import { SR, decodeMono, loadBank, monoSample, timecents, compressBank, BasicSoundBank, GeneratorTypes, emptyPresetFrom } from "./lib.mjs";

const SRC = path.join(process.env.SALAMANDER ?? "/tmp/salamander", "Samples");
const OUT = path.resolve("assets-src/soundfont/extra");
const PC = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const base = loadBank(path.resolve("src/audio/soundfont/game.sf3"));
const out = new BasicSoundBank();
out.soundBankInfo = { ...base.soundBankInfo, name: "Grand Piano (Salamander V3)" };

const notes = new Map(); // root → { soft, loud }
for (const f of fs.readdirSync(SRC)) {
  const m = /^([A-G])(#?)(\d)v(\d+)\.flac$/.exec(f);
  if (!m) continue;
  const root = 12 * (Number(m[3]) + 1) + PC[m[1]] + (m[2] ? 1 : 0);
  const e = notes.get(root) ?? {};
  e[Number(m[4]) <= 8 ? "soft" : "loud"] = f;
  notes.set(root, e);
}
const roots = [...notes.keys()].sort((a, b) => a - b);
const samples = [];
for (const root of roots) {
  for (const layer of ["soft", "loud"]) {
    const f = notes.get(root)[layer];
    if (!f) continue;
    const data = decodeMono(path.join(SRC, f), 7.5, "highpass=f=20");
    const fade = Math.floor(SR * 2);
    for (let i = 0; i < fade && i < data.length; i++) data[data.length - 1 - i] *= i / fade;
    // 音ごとの大きさをそろえる（頭から1.4秒の rms。弱い層は少し小さく）
    let t = 0; const a0 = Math.floor(SR * 0.05), b0 = Math.min(data.length, Math.floor(SR * 1.4));
    for (let i = a0; i < b0; i++) t += data[i] * data[i];
    let pk = 0; for (let i = 0; i < data.length; i++) pk = Math.max(pk, Math.abs(data[i]));
    const g = Math.min(8, (layer === "loud" ? 0.11 : 0.07) / Math.sqrt(t / Math.max(1, b0 - a0)), 0.97 / pk);
    for (let i = 0; i < data.length; i++) data[i] *= g;
    const smp = monoSample(f.replace(".flac", ""), data, root);
    out.addSamples(smp);
    samples.push({ smp, root, layer });
  }
}
let zones = 0;
for (const program of [0, 1]) {
  const preset = emptyPresetFrom(base, out, { program: 0 });
  preset.program = program;
  while (preset.zones.length > 1) preset.deleteZone(preset.zones.length - 1); // 元の楽器が複数の音を重ねている場合、2つ目以降は捨てる
  preset.zones[0].velRange = { min: 0, max: 127 }; // 残した1つ目は「いちばん強い音だけ」の割りあてだったので、全部の強さで鳴るように広げる
  preset.zones[0].keyRange = { min: 0, max: 127 };
  preset.name = "Grand Piano";
  const inst = preset.zones[0].instrument;
  while (inst.zones.length) inst.deleteZone(0, true);
  // 元の楽器の共通設定（音が減衰して消える設定・フィルター・音量の補正など）を捨てて、録音そのままの音にする
  inst.globalZone.generators = [];
  preset.globalZone.generators = preset.globalZone.generators.filter((g) => g.type !== 48);
  for (const { smp, root, layer } of samples) {
    const i = roots.indexOf(root);
    const lo = i === 0 ? 0 : Math.ceil((roots[i - 1] + root) / 2 + 0.01);
    const hi = i === roots.length - 1 ? 127 : Math.floor((root + roots[i + 1]) / 2);
    const z = inst.createZone(smp);
    z.keyRange = { min: lo, max: hi };
    z.velRange = layer === "loud" ? { min: 60, max: 127 } : { min: 1, max: 100 }; // 重ねて、切りかえの段差をなめらかに
    z.setGenerator(GeneratorTypes.overridingRootKey, root);
    z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(0.5));
    zones++;
  }
}
out.flush();
await compressBank(out, 5);
const buf = out.writeSF2({});
const file = path.join(OUT, "piano-salamander.sf3");
fs.writeFileSync(file, Buffer.from(buf));
console.log("書き出し:", file, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB", "ゾーン:", zones);
