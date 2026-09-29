// 使い方: node tools/soundfont/trim-soundfont.mjs <入力.sf3> <出力.sf3> — ゲームで使う楽器（GMの番号）とドラムだけを残した小さなサウンドフォントを作る。
// 元: FluidR3 Mono GM（MITライセンス。assets-src/soundfont/LICENSE-FluidR3.md）。使う楽器の番号は src/audio/gm-map.ts と同じ。
import fs from "fs";
import { SoundBankLoader, BasicSoundBank } from "spessasynth_core";

const [input, output] = process.argv.slice(2);
const PROGRAMS = (process.env.GM_PROGRAMS || "0,4,6,9,11,14,27,29,30,33,38,48,80,89,96,122,123").split(",").map(Number);
await BasicSoundBank.isSF3DecoderReady;
const bank = SoundBankLoader.fromArrayBuffer(fs.readFileSync(input).buffer.slice(0));
console.log("元の楽器数:", bank.presets.length, "サンプル数:", bank.samples.length);
const out = new BasicSoundBank();
out.soundBankInfo = { ...bank.soundBankInfo };
const DRUM_KITS = (process.env.GM_DRUMS || "0,8,16,24,25,32").split(",").map(Number);
const keep = bank.presets.filter((p) => (!p.isGMGSDrum && p.bankMSB === 0 && PROGRAMS.includes(p.program)) || (p.isGMGSDrum && DRUM_KITS.includes(p.program)));
console.log("残す楽器:", keep.map((p) => `${p.isGMGSDrum ? "drum" : p.bankMSB}:${p.program}:${p.name}`).join(", "));
for (const p of keep) out.clonePreset(p);
out.flush();
const buf = out.writeSF2({});
fs.writeFileSync(output, Buffer.from(buf));
console.log("書き出し:", output, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");
