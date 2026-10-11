// 使い方: node tools/audio-check/check-groove.mjs <曲.json> [...] [--edition real]
// リズム・グルーヴの点検（docs/sound/rhythm-groove-guide.md §10 の10）。AIソング形式のJSONを読んで、次を知らせる。
//   エラー（終了コード1）: 格子 g: が4文字の倍数でない／三連 t: が3文字の倍数でない／パートの合計が小節の倍数でない（以降がずれる）。
//   注意: push が ±0.05 拍を超える／キックの push が 0 でない／ベースの push が 0〜+0.01 拍の外／human がジャンルの上限や 30ms を超える／
//         ドラムの volume が 0.18 を超える／beats 6 に swing／ハイハットが全部 x のベタ打ち／同じ小節が8回以上／シンコペ率が 0% か 90% 超。
import fs from "fs";
import { checkGroove } from "./groove-lib.mjs";

const args = process.argv.slice(2);
const edIdx = args.indexOf("--edition");
const edition = edIdx >= 0 ? args[edIdx + 1] : "modern";
const files = args.filter((a, i) => !a.startsWith("--") && (edIdx < 0 || i !== edIdx + 1));
if (!files.length) { console.log("使い方: node tools/audio-check/check-groove.mjs <曲.json> [...] [--edition real]"); process.exit(2); }
let errors = 0, warns = 0;
for (const f of files) {
  let song;
  try { song = JSON.parse(fs.readFileSync(f, "utf8")); } catch (e) { console.log(`× ${f}: 読めません: ${e.message}`); errors++; continue; }
  for (const it of checkGroove(song, { edition })) {
    console.log(`${it.level === "error" ? "×" : "△"} ${f}: ${it.msg}`);
    if (it.level === "error") errors++; else warns++;
  }
}
if (!errors && !warns) console.log("○ リズム・グルーヴの点検で気になる点はありません");
process.exitCode = errors ? 1 : 0;
