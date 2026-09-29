// 使い方: node --experimental-strip-types tools/soundfont/trim-soundfont.mjs <入力.sf3> <出力.sf3> — ゲームで使う楽器（GMの番号）とドラムだけを残した小さなサウンドフォントを作る。
// 元: FluidR3 Mono GM（MITライセンス。assets-src/soundfont/LICENSE-FluidR3.md）。使う楽器の番号は src/audio/gm-map.ts と同じ。
import fs from "fs";
import { SoundBankLoader, BasicSoundBank } from "spessasynth_core";

const [input, output] = process.argv.slice(2);
// 使う楽器・ドラムセットは src/audio/gm-map.ts が決める（実行: node --experimental-strip-types tools/soundfont/trim-soundfont.mjs …）
const { USED_GM_PROGRAMS, DRUM_KITS: KITS } = await import("../../src/audio/gm-map.ts");
const PROGRAMS = process.env.GM_PROGRAMS ? process.env.GM_PROGRAMS.split(",").map(Number) : USED_GM_PROGRAMS;
await BasicSoundBank.isSF3DecoderReady;
const bank = SoundBankLoader.fromArrayBuffer(fs.readFileSync(input).buffer.slice(0));
console.log("元の楽器数:", bank.presets.length, "サンプル数:", bank.samples.length);
const out = new BasicSoundBank();
out.soundBankInfo = { ...bank.soundBankInfo };
const DRUM_KITS = process.env.GM_DRUMS ? process.env.GM_DRUMS.split(",").map(Number) : KITS;
const keep = bank.presets.filter((p) => (!p.isGMGSDrum && p.bankMSB === 0 && PROGRAMS.includes(p.program)) || (p.isGMGSDrum && DRUM_KITS.includes(p.program)));
console.log("残す楽器:", keep.map((p) => `${p.isGMGSDrum ? "drum" : p.bankMSB}:${p.program}:${p.name}`).join(", "));
for (const p of keep) out.clonePreset(p);
out.flush();
const buf = out.writeSF2({});
fs.writeFileSync(output, Buffer.from(buf));
console.log("書き出し:", output, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");
