// 使い方: node tools/soundfont/strip-unused.mjs <入力.sf3> [<出力.sf3>]   （出力を省くと上書き）
// sfz-to-sf3.mjs が作った SF3 には、元のゲーム音源から写した「使われていないサンプル」（約 95KB）が残る。それを取り除く。音は変わらない。
import fs from "fs";
import { SoundBankLoader, BasicSoundBank } from "spessasynth_core";
const [inFile, outFile = inFile] = process.argv.slice(2);
if (!inFile) { console.error("使い方: node tools/soundfont/strip-unused.mjs <in.sf3> [out.sf3]"); process.exit(1); }
await BasicSoundBank.isSF3DecoderReady;
const bank = SoundBankLoader.fromArrayBuffer(fs.readFileSync(inFile).buffer.slice(0));
const before = bank.samples.length;
bank.removeUnusedElements();
bank.flush();
const buf = bank.writeSF2({});
fs.writeFileSync(outFile, Buffer.from(buf));
console.log(outFile, "サンプル", before, "→", bank.samples.length, (buf.byteLength / 1024 / 1024).toFixed(2) + "MB");
