// 使い方: node slice.mjs <出力JSON> [枚数(既定1000)] — 参考ドット絵ライブラリ（assets-src/pixel-library/。規約確認済みの CC0・ぴぽや素材）から、
// 模写の練習用に「1つずつのスプライト」を切り出して、練習用データ（JSON）を作る。データはリポジトリの外（作業用の場所）に置く。素材の複製をリポジトリに入れないため。
// 切り出し: 説明に「32×32」などの1コマの大きさがあれば、その格子で。なければ、透明でない部分のまとまり（連結成分）で。
// 選び方: 1ファイルから取る数に上限をつけ、カテゴリと素材元がかたよらないようにする。同じ絵（左右反転を含む）は1つだけ。色は26色以内にまとめる。
import fs from "fs"; import path from "path"; import crypto from "crypto";
import { readPng } from "../png-read.mjs";
const [out, nArg, minArg, maxArg, catArg] = process.argv.slice(2); const N = Number(nArg ?? 1000); const MINS = Number(minArg ?? 0), MAXS = Number(maxArg ?? 96), CATS = catArg ? catArg.split(",") : null;
const LIB = path.resolve(new URL("../../../assets-src/pixel-library/", import.meta.url).pathname);
const csv = fs.readFileSync(path.join(LIB, "manifest.csv"), "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(Boolean);
const parseRow = (l) => { const o = []; let cur = "", q = false; for (const ch of l) { if (ch === '"') q = !q; else if (ch === "," && !q) { o.push(cur); cur = ""; } else cur += ch; } o.push(cur); return o; };
const head = parseRow(csv[0]); const rows = csv.slice(1).map((l) => Object.fromEntries(parseRow(l).map((v, i) => [head[i], v])));
const hex = (r, g, b) => "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");
function cellsOf(img, desc) {
  const { width: W, height: H, pixels: P } = img; const a = (x, y) => P[(y * W + x) * 4 + 3] >= 128;
  const m = /(\d+)×(\d+)/.exec(desc ?? ""); const list = [];
  const push = (x0, y0, x1, y1) => { // 透明の余白を切り詰める
    let X0 = x1, Y0 = y1, X1 = x0, Y1 = y0; for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) if (a(x, y)) { if (x < X0) X0 = x; if (x > X1) X1 = x; if (y < Y0) Y0 = y; if (y > Y1) Y1 = y; }
    if (X1 < X0) return; const w = X1 - X0 + 1, h = Y1 - Y0 + 1; if (w < 6 || h < 6 || w > MAXS || h > MAXS || Math.max(w, h) < MINS) return; list.push({ x: X0, y: Y0, w, h }); };
  const transparentShare = (() => { let t = 0; for (let i = 3; i < P.length; i += 4) if (P[i] < 128) t++; return t / (W * H); })();
  if (m && Number(m[1]) >= 8 && Number(m[1]) <= 96 && W % Number(m[1]) === 0 && H % Number(m[2]) === 0 && transparentShare > 0.05) { const cw = Number(m[1]), ch = Number(m[2]); for (let y = 0; y < H; y += ch) for (let x = 0; x < W; x += cw) push(x, y, x + cw, y + ch); return list; }
  if (transparentShare > 0.15) { // 連結成分（2ドットの隙間はつなぐ）
    const seen = new Uint8Array(W * H); const near = (x, y) => { for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) { const X = x + dx, Y = y + dy; if (X >= 0 && Y >= 0 && X < W && Y < H && a(X, Y)) return true; } return false; };
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { if (seen[y * W + x] || !a(x, y)) continue; const st = [[x, y]]; seen[y * W + x] = 1; let X0 = x, X1 = x, Y0 = y, Y1 = y; while (st.length) { const [cx, cy] = st.pop(); for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) { const X = cx + dx, Y = cy + dy; if (X < 0 || Y < 0 || X >= W || Y >= H || seen[Y * W + X] || !a(X, Y)) continue; seen[Y * W + X] = 1; st.push([X, Y]); if (X < X0) X0 = X; if (X > X1) X1 = X; if (Y < Y0) Y0 = Y; if (Y > Y1) Y1 = Y; } } push(X0, Y0, X1 + 1, Y1 + 1); }
    void near; return list; }
  if (W <= 64 && H <= 64) { push(0, 0, W, H); return list; }
  const T = m ? Number(m[1]) : 16; for (let y = 0; y + T <= H; y += T) for (let x = 0; x + T <= W; x += T) list.push({ x, y, w: T, h: T }); return list;   // 不透明のタイル集: 16の格子
}
function toPiece(img, c) {
  const { width: W, pixels: P } = img; const cnt = new Map(); const px = [];
  for (let y = 0; y < c.h; y++) for (let x = 0; x < c.w; x++) { const i = ((c.y + y) * W + c.x + x) * 4; if (P[i + 3] < 128) { px.push(null); continue; } const h = hex(P[i], P[i + 1], P[i + 2]); px.push(h); cnt.set(h, (cnt.get(h) ?? 0) + 1); }
  if (cnt.size > (MINS >= 48 ? 140 : 90)) return null;   // 写真のように色が多い（アンチエイリアスやグラデーションの多い）ものは、ドット絵の練習に向かないので除く
  let cols = [...cnt.keys()]; const rgb = (h) => [1, 3, 5].map((k) => parseInt(h.slice(k, k + 2), 16)); const dist = (a, b) => { const x = rgb(a), y = rgb(b); return (x[0] - y[0]) ** 2 * 2 + (x[1] - y[1]) ** 2 * 4 + (x[2] - y[2]) ** 2 * 3; };
  const count = new Map(cnt); const map = new Map(cols.map((h) => [h, h]));
  while (count.size > 26) { const least = [...count.entries()].sort((x, y) => x[1] - y[1])[0][0]; const best = [...count.keys()].filter((h) => h !== least).sort((x, y) => dist(least, x) - dist(least, y))[0]; count.set(best, count.get(best) + count.get(least)); count.delete(least); for (const [k, v] of map) if (v === least) map.set(k, best); }
  const uniq = [...new Set(map.values())]; const sym = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; const pal = {}; uniq.forEach((h, i) => (pal[sym[i]] = h)); const back = new Map(uniq.map((h, i) => [h, sym[i]]));
  const rowsOut = []; for (let y = 0; y < c.h; y++) { let r = ""; for (let x = 0; x < c.w; x++) { const h = px[y * c.w + x]; r += h === null ? "." : back.get(map.get(h)); } rowsOut.push(r); }
  return { rows: rowsOut, pal };
}
const flip = (rs) => rs.map((r) => [...r].reverse().join(""));
const cand = [];
let nf = 0; for (const r of rows) { if (CATS && !CATS.includes(r.category)) continue; if (++nf % 25 === 0) console.log("処理中", nf, "/", rows.length, "候補", cand.length); let img; try { img = readPng(path.join(LIB, r.file)); } catch { continue; } let cells = cellsOf(img, r.description); if (cells.length > 12) { const st = cells.length / 12; cells = Array.from({ length: 12 }, (_, i) => cells[Math.floor(i * st)]); } for (const c of cells) { const p = toPiece(img, c); if (!p) continue; const opaque = p.rows.join("").replace(/\./g, "").length; if (opaque < 40) continue; cand.push({ file: r.file, category: r.category, desc: r.description, license: r.license, author: r.author, ...p, w: c.w, h: c.h, opaque }); } }
console.log("候補", cand.length);
// 同じ絵（色の違いは無視した形＋色の並び、左右反転を含む）を除く
const seen = new Set(); const uniq = []; for (const c of cand) { const key = (rs) => crypto.createHash("md5").update(rs.join("|") + JSON.stringify(Object.values(c.pal))).digest("hex"); const k1 = key(c.rows), k2 = key(flip(c.rows)); if (seen.has(k1) || seen.has(k2)) continue; seen.add(k1); uniq.push(c); }
console.log("重複を除いた", uniq.length);
// 1ファイルから取る数に上限をつけて、カテゴリごとにまんべんなく選ぶ
let cap = 2; let chosen = []; for (; cap <= 60; cap += (MINS >= 48 ? 1 : 1)) { const perFile = new Map(); chosen = []; const byCat = new Map(); for (const c of uniq) { const k = c.file; if ((perFile.get(k) ?? 0) >= cap) continue; perFile.set(k, (perFile.get(k) ?? 0) + 1); chosen.push(c); } if (chosen.length >= N) break; }
// 多すぎるときは、カテゴリごとの割合を保って間引く
if (chosen.length > N) { const step = chosen.length / N; chosen = Array.from({ length: N }, (_, i) => chosen[Math.floor(i * step)]); }
chosen.sort((a, b) => a.opaque - b.opaque);
chosen.forEach((c, i) => (c.id = "pr-" + String(i + 1).padStart(4, "0")));
const cats = {}; for (const c of chosen) cats[c.category] = (cats[c.category] ?? 0) + 1; console.log("選んだ", chosen.length, "1ファイルの上限", cap, JSON.stringify(cats));
const sizes = chosen.map((c) => c.w * c.h); console.log("平均の面積", Math.round(sizes.reduce((a, b) => a + b, 0) / sizes.length), "最大", Math.max(...sizes), "不透明ドット合計", chosen.reduce((a, c) => a + c.opaque, 0));
fs.mkdirSync(path.dirname(out), { recursive: true }); fs.writeFileSync(out, JSON.stringify(chosen)); console.log("→", out);
