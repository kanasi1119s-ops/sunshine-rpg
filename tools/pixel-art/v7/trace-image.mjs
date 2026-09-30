// 使い方: node trace-image.mjs <画像.png> <出力JSON> [大きさ(既定256)] [色数(既定26)] [白の閾値(既定236)]
// 練習用: 参考の絵を、ドット絵エディタで描くための「マス目のデータ（rows と palette）」に変える（縮小→背景を透明に→26色以内にまとめる）。
// 出力はエディタ描き込み（batch-practice.mjs の形式: [{id, rows, pal, ...}]）。**練習用であり、リポジトリ・ゲーム・SNSには出さない**（出力は作業用の場所に置く）。
import fs from "fs"; import { readPng } from "../png-read.mjs";
const [inp, out, sizeArg, colArg, thArg] = process.argv.slice(2); const SIZE = Number(sizeArg ?? 256), NCOL = Number(colArg ?? 26), TH = Number(thArg ?? 236);
const img = readPng(inp); const { width: W, height: H, pixels: P } = img;
const isBg = (i) => { const a = P[i + 3]; if (a < 40) return true; const r = P[i], g = P[i + 1], b = P[i + 2]; return r >= TH && g >= TH && b >= TH - 6 && Math.max(r, g, b) - Math.min(r, g, b) <= 22; };   // ほぼ白（彩度が低い）
// 背景（ほぼ白）を透明にする。手足のすきまに囲まれた白も、背景として抜く
const bg = new Uint8Array(W * H); for (let k = 0; k < W * H; k++) if (isBg(k * 4)) bg[k] = 1;
let X0 = W, X1 = 0, Y0 = H, Y1 = 0; for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!bg[y * W + x]) { if (x < X0) X0 = x; if (x > X1) X1 = x; if (y < Y0) Y0 = y; if (y > Y1) Y1 = y; }
const cw = X1 - X0 + 1, ch = Y1 - Y0 + 1, sc = SIZE / Math.max(cw, ch); const OW = Math.max(1, Math.round(cw * sc)), OH = Math.max(1, Math.round(ch * sc));
console.log("元の絵の範囲", cw, "×", ch, "→", OW, "×", OH);
// 面積平均で縮小（背景は数えない）
const cells = []; for (let oy = 0; oy < OH; oy++) for (let ox = 0; ox < OW; ox++) {
  const sx0 = X0 + ox / sc, sx1 = X0 + (ox + 1) / sc, sy0 = Y0 + oy / sc, sy1 = Y0 + (oy + 1) / sc; let r = 0, g = 0, b = 0, n = 0, tot = 0;
  for (let y = Math.floor(sy0); y < Math.ceil(sy1); y++) for (let x = Math.floor(sx0); x < Math.ceil(sx1); x++) { if (x < 0 || y < 0 || x >= W || y >= H) continue; const w = (Math.min(x + 1, sx1) - Math.max(x, sx0)) * (Math.min(y + 1, sy1) - Math.max(y, sy0)); tot += w; const k = y * W + x; if (bg[k]) continue; const i = k * 4; r += P[i] * w; g += P[i + 1] * w; b += P[i + 2] * w; n += w; }
  cells.push(n / Math.max(tot, 1e-9) >= 0.5 && n > 0 ? [r / n, g / n, b / n] : null); }
// 色を減らす（メディアンカット）
const pts = cells.filter(Boolean); const boxes = [pts]; while (boxes.length < NCOL) { let bi = 0, bs = -1; boxes.forEach((bx, i) => { if (bx.length < 2) return; const rg = [0, 1, 2].map((c) => Math.max(...bx.map((p) => p[c])) - Math.min(...bx.map((p) => p[c]))); const s = Math.max(...rg) * Math.sqrt(bx.length); if (s > bs) { bs = s; bi = i; } }); if (bs < 0) break; const bx = boxes[bi]; const rg = [0, 1, 2].map((c) => Math.max(...bx.map((p) => p[c])) - Math.min(...bx.map((p) => p[c]))); const ax = rg.indexOf(Math.max(...rg)); bx.sort((a, b) => a[ax] - b[ax]); const mid = bx.length >> 1; boxes.splice(bi, 1, bx.slice(0, mid), bx.slice(mid)); }
const pal = boxes.filter((b) => b.length).map((bx) => bx.reduce((s, p) => [s[0] + p[0], s[1] + p[1], s[2] + p[2]], [0, 0, 0]).map((v) => Math.round(v / bx.length)));
const nearest = (p) => { let bi = 0, bd = 1e18; pal.forEach((c, i) => { const d = (c[0] - p[0]) ** 2 * 2 + (c[1] - p[1]) ** 2 * 4 + (c[2] - p[2]) ** 2 * 3; if (d < bd) { bd = d; bi = i; } }); return bi; };
let idx = cells.map((p) => (p ? nearest(p) : -1));
// 点々のざらつきをならす（3×3の多数決で、孤立した1ドットを周りの色にする）
for (let pass = 0; pass < 2; pass++) { const nx = idx.slice(); for (let y = 1; y < OH - 1; y++) for (let x = 1; x < OW - 1; x++) { const c = idx[y * OW + x]; if (c < 0) continue; const nb = [idx[(y - 1) * OW + x], idx[(y + 1) * OW + x], idx[y * OW + x - 1], idx[y * OW + x + 1]]; if (nb.includes(c)) continue; const cnt = {}; for (const q of nb) if (q >= 0) cnt[q] = (cnt[q] || 0) + 1; const best = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0]; if (best && best[1] >= 2) nx[y * OW + x] = +best[0]; } idx = nx; }
const sym = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; const palOut = {}; pal.forEach((c, i) => (palOut[sym[i]] = "#" + c.map((v) => v.toString(16).padStart(2, "0")).join("")));
const rows = []; for (let y = 0; y < OH; y++) { let r = ""; for (let x = 0; x < OW; x++) { const c = idx[y * OW + x]; r += c < 0 ? "." : sym[c]; } rows.push(r); }
const opaque = rows.join("").replace(/\./g, "").length;
fs.writeFileSync(out, JSON.stringify([{ id: "trace-0001", file: inp, category: "練習（トレース）", w: OW, h: OH, rows, pal: palOut, opaque, license: "練習用（公開しない）" }]));
console.log("色数", pal.length, "不透明", opaque, "→", out);
