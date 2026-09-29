// 使い方: node tools/pixel-art/import-pipoya.mjs — ぴぽや「フィールドマップセット１」の地形（自動タイル）から、
// 128×128の地形テクスチャ（色は最大24色に減らす）を作り、tools/pixel-art/pipoya-terrain.json に書く。
// export-game-data.mjs が読み込んで、同名の地形テクスチャを置き換える。素材の規約は docs/assets-credits.md・assets-src/pipoya/LICENSE-pipoya.md。
import fs from "fs";
import { readPng } from "./png-read.mjs";

const BASE = new URL("../../assets-src/pipoya/", import.meta.url).pathname;
// キー → [元ファイル, 自動タイル内のタイル番号（省略時は、上下左右がいちばん自然につながる1枚を自動で選ぶ）, 128に並べるときのずらし量]
const SOURCES = {
  "terrain:grass-a": ["pipo-map001plus/640x480/pipo-map001_at-kusa.png", 4],
  "terrain:grass-b": ["pipo-map001plus/640x480/pipo-map001_at-kusa.png", 4, 16],
  "terrain:dirt": ["pipo-map001/640x480/pipo-map001_at-miti.png", 4],
  "terrain:water": ["pipo-map001/640x480/pipo-map001_at-umi.png", 4],
  "terrain:forest": ["pipo-map001/640x480/pipo-map001_at-mori.png", 4],
};
const COLORS = 24;

function tileAt(png, n) {
  const t = new Uint8Array(32 * 32 * 3);
  for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) {
    const s = ((n * 32 + y) * 32 + x) * 4, d = (y * 32 + x) * 3;
    t[d] = png.pixels[s]; t[d + 1] = png.pixels[s + 1]; t[d + 2] = png.pixels[s + 2];
  }
  return t;
}
/** 上下・左右の端どうしの色の差（小さいほど、並べたときの継ぎ目が目立たない）。 */
function seamError(t) {
  let e = 0;
  for (let i = 0; i < 32; i++) for (let c = 0; c < 3; c++) {
    e += Math.abs(t[(i * 32) * 3 + c] - t[(i * 32 + 31) * 3 + c]);
    e += Math.abs(t[i * 3 + c] - t[(31 * 32 + i) * 3 + c]);
  }
  return e;
}
/** メディアンカット法で色を減らす。 */
function quantize(pixels, count) {
  let boxes = [pixels.map((_, i) => i)];
  while (boxes.length < count) {
    boxes.sort((a, b) => b.length - a.length);
    const box = boxes.shift();
    if (box.length < 2) { boxes.push(box); break; }
    let best = 0, span = -1;
    for (let c = 0; c < 3; c++) {
      const v = box.map((i) => pixels[i][c]);
      const s = Math.max(...v) - Math.min(...v);
      if (s > span) { span = s; best = c; }
    }
    box.sort((a, b) => pixels[a][best] - pixels[b][best]);
    const mid = box.length >> 1;
    boxes.push(box.slice(0, mid), box.slice(mid));
  }
  return boxes.map((box) => [0, 1, 2].map((c) => Math.round(box.reduce((s, i) => s + pixels[i][c], 0) / box.length)));
}
function encode(cells) {
  let s = "", prev = null, n = 0;
  const flush = () => { if (prev !== null) s += prev + (n > 1 ? n.toString(36) : ""); };
  for (const k of cells) {
    const ch = String.fromCharCode(65 + k);
    if (ch === prev) n++; else { flush(); prev = ch; n = 1; }
  }
  flush();
  return s;
}

const out = {};
for (const [key, [file, tileNo, shift = 0]] of Object.entries(SOURCES)) {
  const png = readPng(BASE + file);
  const count = png.height / 32;
  let pick = tileNo;
  if (pick == null) {
    let bestE = Infinity;
    for (let n = 0; n < count; n++) { const e = seamError(tileAt(png, n)); if (e < bestE) { bestE = e; pick = n; } }
  }
  const tile = tileAt(png, pick);
  const px = [];
  for (let y = 0; y < 128; y++) for (let x = 0; x < 128; x++) {
    const sx = (x + shift) % 32, sy = (y + shift) % 32, s = (sy * 32 + sx) * 3;
    px.push([tile[s], tile[s + 1], tile[s + 2]]);
  }
  const pal = quantize(px, COLORS);
  const cells = px.map((p) => {
    let best = 0, bd = Infinity;
    pal.forEach((q, i) => { const d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2; if (d < bd) { bd = d; best = i; } });
    return best;
  });
  const hex = pal.map((q) => "#" + q.map((v) => v.toString(16).padStart(2, "0")).join(""));
  out[key] = { size: 128, palette: hex, rle: encode(cells) };
  console.log(key, file, "tile", pick, "colors", pal.length);
}
fs.writeFileSync(new URL("./pipoya-terrain.json", import.meta.url), JSON.stringify(out));
