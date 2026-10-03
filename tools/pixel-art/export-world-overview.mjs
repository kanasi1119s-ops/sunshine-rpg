// 使い方: node tools/pixel-art/export-world-overview.mjs
// 全体フィールドの全体図（V キー）の絵を、ゲームが読む形に書き出す（2026-10-04）。
// 元: assets-src/field/world-overview.txt（エディタ用の文字グリッド。1文字＝1マス、356×267）と .json（色）。
// 人間が用意した全体フィールドの見本の絵を、地図と同じ大きさ（1マス＝1ドット）に縮めて26色にし、ドット絵エディタで描いて確かめたもの。
import fs from "fs";
const dir = new URL("../../assets-src/field/", import.meta.url);
const rows = fs.readFileSync(new URL("world-overview.txt", dir), "utf8").trim().split("\n");
const colors = JSON.parse(fs.readFileSync(new URL("world-overview.json", dir), "utf8"));
const names = Object.keys(colors).sort();
const palette = names.map((n) => colors[n]);
let rle = "", prev = null, n = 0;
const flush = () => { if (prev !== null) rle += prev + (n > 1 ? n.toString(36) : ""); };
for (const row of rows) for (const ch of row) {
  const c = String.fromCharCode(65 + names.indexOf(ch));
  if (c === prev) n++; else { flush(); prev = c; n = 1; }
}
flush();
fs.writeFileSync(new URL("../../src/game/map/world/world-overview.generated.ts", import.meta.url), `// 自動生成: tools/pixel-art/export-world-overview.mjs（手で編集しない）
/** 全体フィールドの全体図（1マス＝1ドット）。色番号A〜Zと続く数（36進数）。 */
export const WORLD_OVERVIEW = { width: ${rows[0].length}, height: ${rows.length}, palette: ${JSON.stringify(palette)}, rle: ${JSON.stringify(rle)} };
`);
console.log("書き出し:", rows[0].length, "×", rows.length, palette.length, "色");
