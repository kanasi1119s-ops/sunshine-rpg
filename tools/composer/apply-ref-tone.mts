// 曲（AIソング形式の JSON）に参考の音を当てて、上書きする（書き出しの --ref-tone と同じ処理を、先に JSON へ入れておくための道具）。
// 使い方: npx tsx tools/composer/apply-ref-tone.mts <曲.json> <参考の音の id> [出力.json]
import fs from "fs";
import { REF_TONES, applyRefToneToSong } from "../../src/audio/ref-tones";
const [src, id, out] = process.argv.slice(2);
const tone = REF_TONES[id];
if (!src || !tone) { console.error(`使い方: apply-ref-tone.mts <曲.json> <${Object.keys(REF_TONES).join("|")}> [出力.json]`); process.exit(1); }
const song = applyRefToneToSong(JSON.parse(fs.readFileSync(src, "utf8")), tone);
fs.writeFileSync(out ?? src, JSON.stringify(song));
console.log(`参考の音「${tone.label}」を当てました → ${out ?? src}`);
