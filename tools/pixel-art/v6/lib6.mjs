// v6: マップを歩く人物（主人公・仲間・町の人）の 4方向×3コマ ドット絵（16×24、2頭身）を作る道具（2026-09-30）。
// 人間の決定: 大きさは案A（16×24）、人物1人＝12コマ（下・左・右・上 × 歩き3コマ）で1点と数える。
// 描くのは 下（正面）・左（横）・上（後ろ）の3方向。右は左を左右反転して作る（片手の持ち物など、左右で違う物がある人物は right を自分で描き直す）。
// 歩きは 1→2→3→2 の往復。足元の線は全コマで同じ高さ。体は歩きで最大1ドット動く。目は歩きの間に変えない。目には必ず白いハイライトを入れる。
export const W = 16, H = 24;
export const DIRS = ["down", "left", "right", "up"];
class G {
  constructor() { this.g = Array.from({ length: H }, () => Array(W).fill(".")); }
  put(x, y, c) { if (x >= 0 && x < W && y >= 0 && y < H && c) this.g[y][x] = c; }
  get(x, y) { return x >= 0 && x < W && y >= 0 && y < H ? this.g[y][x] : "."; }
  rect(x0, y0, x1, y1, c) { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) this.put(x, y, c); }
  row(y, x0, x1, c) { this.rect(x0, y, x1, y, c); }
  px(list, c) { for (const [x, y] of list) this.put(x, y, c); }
  /** 外周の縁取り（4近傍）。 */
  outline(c) { const l = []; for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (this.g[y][x] === "." && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => this.get(x + dx, y + dy) !== ".")) l.push([x, y]); for (const [x, y] of l) this.g[y][x] = c; }
  rows() { return this.g.map((r) => r.join("")); }
}
export const mirrorRows = (rows) => rows.map((r) => [...r].reverse().join(""));
// 髪型: short / spiky / long / twin（ふたつ結び）/ bun（おだんご）/ bald / bob / pony（ポニーテール）
// 服: tunic（上着＋ズボン）/ robe（ローブ）/ dress（ワンピース）/ apron / armor（鎧）/ coat（長い上着）
// 小物: hat（つば広の帽子）/ cap（ぼうし）/ hood / band（はちまき）/ glasses / beard / scarf / cape / bag / staff は別途
const defaults = { hair: "short", outfit: "tunic", acc: [], eyes: "std" };
function frameShape(f) { return { bob: f === 1 ? 0 : 1, lift: f === 0 ? "L" : f === 2 ? "R" : null }; }

export function drawFront(o, f) {
  const g = new G(), { bob, lift } = frameShape(f), B = bob;
  const hairLong = ["long", "twin", "bob", "pony"].includes(o.hair);
  // ---- 髪（後ろ髪。頭より後ろ・体の横）
  if (o.hair === "long") { g.rect(3, 6 + B, 4, 15 + B, "h"); g.rect(11, 6 + B, 12, 15 + B, "h"); g.rect(3, 6 + B, 3, 14 + B, "H"); }
  if (o.hair === "twin") { g.rect(2, 8 + B, 3, 14 + B, "H"); g.rect(12, 8 + B, 13, 14 + B, "H"); g.px([[2, 15 + B], [13, 15 + B]], "h"); g.px([[3, 7 + B], [12, 7 + B]], "T"); }
  if (o.hair === "bob") { g.rect(3, 6 + B, 3, 11 + B, "H"); g.rect(12, 6 + B, 12, 11 + B, "H"); g.rect(4, 11 + B, 4, 11 + B, "h"); g.rect(11, 11 + B, 11, 11 + B, "h"); }
  // ---- 脚
  const skirt = o.outfit === "robe" || o.outfit === "dress" || o.outfit === "coat";
  if (skirt) {
    const c1 = o.outfit === "coat" ? "P" : "C";
    g.rect(4, 17 + B, 11, 20, c1); g.rect(4, 17 + B, 4, 20, "k"); g.rect(11, 17 + B, 11, 20, "c"); g.row(20, 4, 11, "c");
    if (o.outfit !== "coat") { g.px([[3, 20], [12, 20]], "c"); }
    g.px([[6, 21], [7, 21], [8, 21], [9, 21]], "F");
    g.px(lift === "L" ? [[5, 21]] : [[5, 22]], "F"); g.px(lift === "R" ? [[10, 21]] : [[10, 22]], "F");
    g.px(lift === "L" ? [[6, 22]] : lift === "R" ? [[9, 22]] : [[6, 22], [9, 22]], "F");
  } else {
    const legTop = 18 + B;
    g.rect(5, legTop, 7, 20, "P"); g.rect(8, legTop, 10, 20, "P"); g.rect(8, legTop, 8, 20, "p"); g.rect(7, legTop, 7, 20, "p");
    // 靴（持ち上げた足は1ドット短い）
    g.rect(5, 21, 7, lift === "L" ? 21 : 22, "F"); g.rect(8, 21, 10, lift === "R" ? 21 : 22, "F"); g.px([[5, lift === "L" ? 21 : 22], [10, lift === "R" ? 21 : 22]], "f");
    if (lift === "L") g.rect(5, 20, 7, 20, "P");
    if (lift === "R") g.rect(8, 20, 10, 20, "P");
  }
  // ---- 胴と腕
  const armSwing = f === 0 ? -1 : f === 2 ? 1 : 0;   // 腕は足と逆に振る（±1ドット）
  const body = o.outfit === "armor" ? { m: "M", l: "N", d: "m" } : { m: "C", l: "k", d: "c" };
  g.rect(5, 12 + B, 10, 17 + B, body.m); g.rect(5, 12 + B, 5, 17 + B, body.l); g.rect(10, 12 + B, 10, 17 + B, body.d); g.row(17 + B, 5, 10, body.d);
  if (o.outfit === "apron") { g.rect(6, 13 + B, 9, 17 + B, "W"); g.rect(9, 13 + B, 9, 17 + B, "w"); g.row(13 + B, 6, 9, "W"); }
  if (o.outfit === "tunic" || o.outfit === "coat") { g.row(16 + B, 5, 10, "T"); g.px([[7, 16 + B], [8, 16 + B]], "A"); }
  if (o.outfit === "robe") { g.px([[7, 13 + B], [8, 13 + B], [7, 14 + B], [8, 15 + B]], "T"); g.rect(7, 12 + B, 8, 12 + B, "S"); }
  if (o.outfit === "dress") { g.row(15 + B, 5, 10, "T"); }
  if (o.outfit === "armor") { g.rect(7, 14 + B, 8, 16 + B, "m"); g.px([[7, 14 + B], [8, 14 + B]], "N"); g.rect(4, 12 + B, 5, 13 + B, "N"); g.rect(10, 12 + B, 11, 13 + B, "M"); }
  const sleeve = o.outfit === "armor" ? "M" : "C", sl = o.outfit === "armor" ? "N" : "k", sd = o.outfit === "armor" ? "m" : "c";
  const la = 13 + B + Math.max(0, armSwing) * 0, ra = 13 + B;
  g.rect(3, 13 + B + (armSwing < 0 ? 0 : 0), 4, 15 + B, sleeve); g.rect(3, 13 + B, 3, 15 + B, sl); g.rect(11, 13 + B, 12, 15 + B, sleeve); g.rect(12, 13 + B, 12, 15 + B, sd);
  const lh = 16 + B + (armSwing === 1 ? -1 : armSwing === -1 ? 0 : 0) + (armSwing === -1 ? 0 : 0), rh = 16 + B + (armSwing === -1 ? -1 : 0);
  g.rect(3, 16 + B + (armSwing === 1 ? -1 : 0), 4, 16 + B + (armSwing === 1 ? -1 : 0), "S"); g.rect(11, 16 + B + (armSwing === -1 ? -1 : 0), 12, 16 + B + (armSwing === -1 ? -1 : 0), "S");
  g.px([[3, 16 + B + (armSwing === 1 ? -1 : 0) + 1 - 1]], "S");
  // ---- 頭
  const hr = { 1: [5, 10], 2: [4, 11], 3: [4, 11], 4: [4, 11], 5: [4, 11], 6: [4, 11], 7: [4, 11], 8: [4, 11], 9: [4, 11], 10: [5, 10] };
  for (const [y, [a, b]] of Object.entries(hr)) g.row(+y + B, a, b, "S");
  g.row(10 + B, 5, 10, "s"); g.px([[4, 9 + B], [11, 9 + B]], "s");
  // 髪（前）
  const hairShape = {
    short: { top: 4, side: 6 }, spiky: { top: 4, side: 5 }, long: { top: 4, side: 9 }, twin: { top: 4, side: 6 }, bun: { top: 4, side: 6 }, bald: { top: 0, side: 0 }, bob: { top: 4, side: 8 }, pony: { top: 4, side: 6 },
  }[o.hair];
  if (o.hair !== "bald") {
    for (let y = 1; y <= hairShape.top; y++) g.row(y + B, hr[y][0], hr[y][1], "H");
    g.rect(4, 1 + B, 4, hairShape.side + B, "H"); g.rect(11, 1 + B, 11, hairShape.side + B, "H");
    g.row(1 + B, 5, 10, "g"); g.px([[6, 2 + B], [7, 2 + B]], "g");
    g.px([[4, 4 + B], [11, 4 + B]], "h"); g.row(hairShape.top + B, 6, 9, "h");
    // 前髪のすきま（ぎざぎざ）
    if (o.hair === "spiky") { g.px([[6, 4 + B], [9, 4 + B]], "S"); g.px([[3, 2 + B], [12, 2 + B], [5, 0 + B], [10, 0 + B], [7, 0 + B]], "H"); }
    else g.px([[7, 4 + B], [8, 4 + B]], "S");
    if (o.hair === "bun") { g.rect(6, -1 + B < 0 ? 0 : 0, 9, 0, "H"); g.px([[7, 0], [8, 0]], "g"); }
    if (o.hair === "pony") { g.rect(12, 3 + B, 13, 9 + B, "H"); g.rect(13, 5 + B, 13, 10 + B, "h"); g.px([[12, 3 + B]], "T"); }
    if (o.hair === "twin") { g.px([[3, 4 + B], [12, 4 + B]], "T"); }
  } else { g.row(1 + B, 5, 10, "g"); g.row(2 + B, 4, 11, "S"); }
  // 顔（目は2×2・左上に白いハイライト）
  const ey = 6 + B;
  if (o.eyes === "closed") { g.px([[5, ey + 1], [6, ey + 1], [9, ey + 1], [10, ey + 1]], "E"); g.px([[5, ey], [10, ey]], "W"); }
  else { g.px([[5, ey], [9, ey]], "W"); g.px([[6, ey], [10, ey], [5, ey + 1], [6, ey + 1], [9, ey + 1], [10, ey + 1]], "E"); }
  g.px([[7, 9 + B], [8, 9 + B]], "n"); g.px([[4, 8 + B], [11, 8 + B]], "B");
  // 小物
  for (const a of o.acc) accFront(g, a, B, o);
  g.outline("O");
  // 落ち影
  for (const [x, y] of [[5, 23], [6, 23], [7, 23], [8, 23], [9, 23], [10, 23]]) if (g.get(x, y) === ".") g.put(x, y, "D");
  return g.rows();
}
function accFront(g, a, B, o) {
  if (a === "hat") { g.rect(2, 1 + B, 13, 2 + B, "a"); g.rect(5, -0 + B, 10, 0 + B, "a"); g.rect(2, 2 + B, 13, 2 + B, "A"); g.rect(4, 1 + B, 11, 1 + B, "a"); g.rect(5, 1 + B, 5, 1 + B, "A"); }
  if (a === "cap") { g.rect(4, 1 + B, 11, 3 + B, "a"); g.row(3 + B, 4, 11, "A"); g.row(1 + B, 5, 10, "a"); }
  if (a === "hood") { g.rect(3, 1 + B, 12, 3 + B, "a"); g.rect(3, 4 + B, 4, 9 + B, "a"); g.rect(11, 4 + B, 12, 9 + B, "a"); g.row(1 + B, 5, 10, "A"); }
  if (a === "band") { g.row(3 + B, 4, 11, "A"); g.px([[12, 3 + B], [12, 4 + B]], "A"); }
  if (a === "glasses") { g.rect(5, 6 + B, 6, 7 + B, "E"); g.rect(9, 6 + B, 10, 7 + B, "E"); g.px([[5, 6 + B], [9, 6 + B]], "W"); g.row(6 + B, 7, 8, "m"); g.px([[4, 6 + B], [11, 6 + B]], "m"); }
  if (a === "beard") { g.rect(5, 9 + B, 10, 10 + B, "h"); g.rect(4, 8 + B, 4, 9 + B, "h"); g.rect(11, 8 + B, 11, 9 + B, "h"); g.px([[7, 8 + B], [8, 8 + B]], "H"); g.px([[7, 9 + B], [8, 9 + B]], "n"); }
  if (a === "scarf") { g.rect(4, 11 + B, 11, 12 + B, "A"); g.px([[8, 13 + B], [8, 14 + B]], "A"); g.row(12 + B, 4, 11, "T"); }
  if (a === "bag") { g.rect(4, 12 + B, 5, 16 + B, "T"); g.rect(9, 15 + B, 11, 17 + B, "A"); g.px([[10, 15 + B], [10, 16 + B]], "T"); }
  if (a === "cape") { g.rect(3, 12 + B, 4, 19, "a"); g.rect(11, 12 + B, 12, 19, "a"); }
}

export function drawBack(o, f) {
  const g = new G(), { bob, lift } = frameShape(f), B = bob;
  const skirt = o.outfit === "robe" || o.outfit === "dress" || o.outfit === "coat";
  const hairLong = ["long", "twin", "bob", "pony"].includes(o.hair);
  if (o.acc.includes("cape")) { g.rect(3, 12 + B, 12, 20, "a"); g.rect(3, 12 + B, 3, 20, "A"); g.rect(12, 12 + B, 12, 20, "a"); g.row(20, 3, 12, "a"); }
  if (skirt) {
    const c1 = o.outfit === "coat" ? "P" : "C";
    g.rect(4, 17 + B, 11, 20, c1); g.rect(4, 17 + B, 4, 20, "k"); g.rect(11, 17 + B, 11, 20, "c"); g.row(20, 4, 11, "c");
    g.px(lift === "L" ? [[5, 21]] : [[5, 22]], "F"); g.px(lift === "R" ? [[10, 21]] : [[10, 22]], "F"); g.px(lift === "L" ? [[6, 22]] : lift === "R" ? [[9, 22]] : [[6, 22], [9, 22]], "F"); g.px([[6, 21], [9, 21]], "F");
  } else {
    const legTop = 18 + B; g.rect(5, legTop, 10, 20, "P"); g.rect(8, legTop, 8, 20, "p"); g.rect(7, legTop, 7, 20, "p");
    g.rect(5, 21, 7, lift === "L" ? 21 : 22, "F"); g.rect(8, 21, 10, lift === "R" ? 21 : 22, "F");
    if (lift === "L") g.rect(5, 20, 7, 20, "P"); if (lift === "R") g.rect(8, 20, 10, 20, "P");
  }
  const armSwing = f === 0 ? 1 : f === 2 ? -1 : 0;
  const body = o.outfit === "armor" ? { m: "M", l: "N", d: "m" } : { m: "C", l: "k", d: "c" };
  g.rect(5, 12 + B, 10, 17 + B, body.m); g.rect(10, 12 + B, 10, 17 + B, body.d); g.row(17 + B, 5, 10, body.d); g.rect(5, 12 + B, 5, 17 + B, body.l);
  if (o.outfit === "tunic" || o.outfit === "coat") g.row(16 + B, 5, 10, "T");
  if (o.outfit === "dress") g.row(15 + B, 5, 10, "T");
  if (o.outfit === "apron") { g.px([[7, 15 + B], [8, 15 + B], [7, 14 + B], [8, 16 + B]], "W"); }
  if (o.outfit === "robe") g.rect(7, 13 + B, 8, 16 + B, "c");
  const sleeve = o.outfit === "armor" ? "M" : "C", sl = o.outfit === "armor" ? "N" : "k", sd = o.outfit === "armor" ? "m" : "c";
  g.rect(3, 13 + B, 4, 15 + B, sleeve); g.rect(3, 13 + B, 3, 15 + B, sl); g.rect(11, 13 + B, 12, 15 + B, sleeve); g.rect(12, 13 + B, 12, 15 + B, sd);
  g.rect(3, 16 + B + (armSwing === 1 ? -1 : 0), 4, 16 + B + (armSwing === 1 ? -1 : 0), "S"); g.rect(11, 16 + B + (armSwing === -1 ? -1 : 0), 12, 16 + B + (armSwing === -1 ? -1 : 0), "S");
  if (o.acc.includes("bag")) { g.rect(6, 13 + B, 9, 17 + B, "A"); g.rect(6, 13 + B, 9, 13 + B, "T"); g.rect(9, 14 + B, 9, 17 + B, "T"); }
  // 頭（後ろ）
  const hr = { 1: [5, 10], 2: [4, 11], 3: [4, 11], 4: [4, 11], 5: [4, 11], 6: [4, 11], 7: [4, 11], 8: [4, 11], 9: [4, 11], 10: [5, 10] };
  if (o.hair === "long") { g.rect(3, 5 + B, 12, 15 + B, "H"); g.rect(3, 5 + B, 3, 15 + B, "g"); g.rect(12, 5 + B, 12, 15 + B, "h"); g.row(15 + B, 4, 11, "h"); g.px([[7, 13 + B], [8, 13 + B], [7, 10 + B], [8, 11 + B]], "h"); }
  for (const [y, [a, b]] of Object.entries(hr)) g.row(+y + B, a, b, o.hair === "bald" ? "S" : "H");
  if (o.hair !== "bald") { g.row(1 + B, 5, 10, "g"); g.row(2 + B, 5, 8, "g"); g.rect(11, 3 + B, 11, 9 + B, "h"); g.row(10 + B, 5, 10, "h"); g.px([[7, 6 + B], [8, 7 + B], [6, 8 + B], [9, 8 + B]], "h"); }
  else { g.row(10 + B, 5, 10, "s"); g.row(1 + B, 5, 10, "g"); }
  if (o.hair !== "bald" && !hairLong) g.row(10 + B, 5, 10, "s"), g.rect(6, 10 + B, 9, 10 + B, "s");
  if (o.hair === "twin") { g.rect(2, 8 + B, 3, 14 + B, "H"); g.rect(12, 8 + B, 13, 14 + B, "H"); g.px([[3, 7 + B], [12, 7 + B]], "T"); }
  if (o.hair === "bob") { g.rect(3, 6 + B, 12, 11 + B, "H"); g.rect(3, 6 + B, 3, 11 + B, "g"); g.row(11 + B, 4, 11, "h"); }
  if (o.hair === "bun") { g.rect(6, 0, 9, 0, "H"); }
  if (o.hair === "pony") { g.rect(7, 9 + B, 9, 14 + B, "H"); g.rect(9, 9 + B, 9, 14 + B, "h"); g.px([[8, 8 + B]], "T"); }
  if (o.hair === "spiky") g.px([[3, 2 + B], [12, 2 + B], [5, 0 + B], [10, 0 + B], [7, 0 + B]], "H");
  for (const a of o.acc) accBack(g, a, B);
  g.outline("O");
  for (const [x, y] of [[5, 23], [6, 23], [7, 23], [8, 23], [9, 23], [10, 23]]) if (g.get(x, y) === ".") g.put(x, y, "D");
  return g.rows();
}
function accBack(g, a, B) {
  if (a === "hat") { g.rect(2, 1 + B, 13, 2 + B, "a"); g.rect(5, 0 + B, 10, 0 + B, "a"); g.rect(2, 2 + B, 13, 2 + B, "A"); g.rect(4, 1 + B, 11, 1 + B, "a"); }
  if (a === "cap") { g.rect(4, 1 + B, 11, 4 + B, "a"); g.row(4 + B, 4, 11, "A"); }
  if (a === "hood") { g.rect(3, 1 + B, 12, 10 + B, "a"); g.row(1 + B, 5, 10, "A"); g.row(10 + B, 4, 11, "A"); }
  if (a === "band") { g.row(3 + B, 4, 11, "A"); g.px([[11, 4 + B], [11, 5 + B], [12, 5 + B]], "A"); }
  if (a === "scarf") { g.rect(4, 11 + B, 11, 12 + B, "A"); g.row(12 + B, 4, 11, "T"); g.px([[10, 13 + B], [10, 14 + B], [10, 15 + B]], "A"); }
}
export function drawSide(o, f) {   // 左向き
  const g = new G(), { bob, lift } = frameShape(f), B = bob;
  const skirt = o.outfit === "robe" || o.outfit === "dress" || o.outfit === "coat";
  const hairLong = ["long", "twin", "bob", "pony"].includes(o.hair);
  // 奥の腕（体の後ろ）
  const swing = f === 0 ? 1 : f === 2 ? -1 : 0;   // + なら手前の腕が前
  const body = o.outfit === "armor" ? { m: "M", l: "N", d: "m" } : { m: "C", l: "k", d: "c" };
  if (o.acc.includes("cape")) { g.rect(9, 12 + B, 12, 20, "a"); g.rect(12, 12 + B, 12, 20, "A"); }
  if (o.hair === "long") { g.rect(8, 5 + B, 12, 15 + B, "h"); g.rect(11, 5 + B, 12, 15 + B, "H"); g.row(15 + B, 9, 12, "h"); }
  if (o.hair === "twin") { g.rect(9, 8 + B, 11, 14 + B, "H"); g.px([[10, 7 + B]], "T"); g.px([[11, 12 + B], [11, 13 + B], [11, 14 + B]], "h"); }
  if (o.hair === "pony") { g.rect(11, 3 + B, 13, 8 + B, "H"); g.rect(12, 8 + B, 13, 12 + B, "h"); g.px([[11, 3 + B]], "T"); }
  if (o.hair === "bob") { g.rect(8, 6 + B, 12, 11 + B, "H"); g.row(11 + B, 8, 12, "h"); }
  g.rect(8 - swing * 2, 13 + B, 9 - swing * 2, 15 + B, body.d); g.rect(8 - swing * 2, 16 + B, 9 - swing * 2, 16 + B, "S");
  // 脚
  if (skirt) {
    const c1 = o.outfit === "coat" ? "P" : "C";
    g.rect(5, 17 + B, 10, 20, c1); g.rect(5, 17 + B, 5, 20, "k"); g.rect(10, 17 + B, 10, 20, "c"); g.row(20, 5, 10, "c");
    const fx = f === 0 ? [4, 5] : f === 2 ? [8, 9] : [6, 7]; g.rect(fx[0], 21, fx[1] + 1, 22, "F"); g.rect(f === 1 ? 8 : (f === 0 ? 9 : 5), 21, f === 1 ? 9 : (f === 0 ? 10 : 6), f === 1 ? 22 : 21, "F");
  } else {
    const legTop = 18 + B;
    const front = f === 0 ? 4 : f === 2 ? 8 : 6, back = f === 0 ? 9 : f === 2 ? 5 : 7;    // 手前の足と奥の足の左端
    g.rect(back, legTop, back + 2, 20, "p"); g.rect(back, 21, back + 2, f === 1 ? 22 : 21, "f");
    g.rect(front, legTop, front + 2, 20, "P"); g.rect(front - 1, 21, front + 2, 22, "F");
    if (f === 1) g.rect(back, 21, back + 2, 22, "f");
  }
  // 胴
  g.rect(6, 12 + B, 9, 17 + B, body.m); g.rect(6, 12 + B, 6, 17 + B, body.l); g.rect(9, 12 + B, 9, 17 + B, body.d); g.row(17 + B, 6, 9, body.d);
  if (o.outfit === "tunic" || o.outfit === "coat") g.row(16 + B, 6, 9, "T");
  if (o.outfit === "dress") g.row(15 + B, 6, 9, "T");
  if (o.outfit === "apron") g.rect(6, 13 + B, 7, 17 + B, "W");
  if (o.outfit === "armor") { g.rect(6, 12 + B, 8, 13 + B, "N"); }
  // 手前の腕
  const sleeve = o.outfit === "armor" ? "M" : "C", sl = o.outfit === "armor" ? "N" : "k";
  const ax = 7 + swing * 2 - (swing ? 0 : 0);
  g.rect(ax, 13 + B, ax + 1, 15 + B, sleeve); g.rect(ax, 13 + B, ax, 15 + B, sl); g.rect(ax, 16 + B, ax + 1, 16 + B, "S");
  if (o.acc.includes("bag")) { g.rect(8, 15 + B, 10, 17 + B, "A"); g.px([[9, 15 + B]], "T"); }
  // 頭（左向き）: 顔は左、後頭部は右
  const hr = { 1: [5, 10], 2: [4, 11], 3: [4, 11], 4: [4, 11], 5: [4, 11], 6: [4, 11], 7: [4, 11], 8: [4, 11], 9: [4, 11], 10: [5, 10] };
  for (const [y, [a, b]] of Object.entries(hr)) g.row(+y + B, a, b, "S");
  g.px([[3, 8 + B]], "S"); g.px([[10, 10 + B], [9, 10 + B]], "s"); g.row(10 + B, 5, 8, "s");
  if (o.hair !== "bald") {
    for (let y = 1; y <= 3; y++) g.row(y + B, hr[y][0], hr[y][1], "H");
    g.rect(8, 4 + B, 11, 9 + B, "H"); g.rect(11, 4 + B, 11, 9 + B, "h"); g.row(10 + B, 9, 10, "h");
    g.row(4 + B, 4, 7, "H"); g.px([[4, 4 + B], [4, 5 + B]], "h"); g.row(1 + B, 5, 10, "g"); g.px([[6, 2 + B], [7, 2 + B]], "g"); g.px([[7, 4 + B]], "h");
    if (o.hair === "spiky") g.px([[3, 2 + B], [12, 2 + B], [5, 0 + B], [10, 0 + B], [7, 0 + B]], "H");
    if (o.hair === "bun") g.rect(6, 0, 9, 0, "H");
  } else { g.row(1 + B, 5, 10, "g"); g.row(2 + B, 4, 11, "S"); }
  const ey = 6 + B; g.px([[5, ey]], "W"); g.px([[6, ey], [5, ey + 1], [6, ey + 1]], "E"); if (o.eyes === "closed") { g.px([[5, ey], [6, ey]], "S"); g.px([[5, ey + 1], [6, ey + 1]], "E"); g.px([[5, ey]], "W"); }
  g.px([[4, 9 + B]], "n"); g.px([[5, 8 + B]], "B");
  for (const a of o.acc) accSide(g, a, B);
  g.outline("O");
  for (const [x, y] of [[5, 23], [6, 23], [7, 23], [8, 23], [9, 23], [10, 23]]) if (g.get(x, y) === ".") g.put(x, y, "D");
  return g.rows();
}
function accSide(g, a, B) {
  if (a === "hat") { g.rect(2, 1 + B, 13, 2 + B, "a"); g.rect(5, 0 + B, 10, 0 + B, "a"); g.rect(2, 2 + B, 13, 2 + B, "A"); g.rect(4, 1 + B, 11, 1 + B, "a"); }
  if (a === "cap") { g.rect(4, 1 + B, 11, 3 + B, "a"); g.rect(2, 3 + B, 6, 3 + B, "A"); g.row(3 + B, 7, 11, "A"); }
  if (a === "hood") { g.rect(4, 1 + B, 12, 4 + B, "a"); g.rect(8, 5 + B, 12, 10 + B, "a"); g.row(1 + B, 5, 10, "A"); }
  if (a === "band") { g.row(3 + B, 4, 11, "A"); g.px([[11, 4 + B], [12, 4 + B], [12, 5 + B]], "A"); }
  if (a === "glasses") { g.rect(4, 6 + B, 6, 7 + B, "E"); g.px([[4, 6 + B]], "W"); g.row(6 + B, 7, 9, "m"); }
  if (a === "beard") { g.rect(4, 9 + B, 8, 10 + B, "h"); g.px([[3, 9 + B]], "h"); g.px([[4, 9 + B]], "n"); }
  if (a === "scarf") { g.rect(5, 11 + B, 10, 12 + B, "A"); g.row(12 + B, 5, 10, "T"); g.px([[10, 13 + B], [10, 14 + B]], "A"); }
}
export const PAL_KEYS = { O: "outline", D: "shadow", S: "skin", s: "skinShade", E: "eye", W: "eyeLight", n: "mouth", B: "blush", H: "hair", h: "hairDark", g: "hairLight", C: "cloth", c: "clothDark", k: "clothLight", T: "trim", P: "pants", p: "pantsDark", F: "boots", f: "bootsDark", A: "accent", a: "accent2", M: "metal", N: "metalLight", m: "metalDark", w: "aprondark" };
/** 12コマ（下・左・右・上 × 3コマ）を作る。frames[dir][0..2]。右は左の反転（o.rightRedraw が true なら左右で違う物のため手描き用にそのまま反転して出す）。 */
export function makeSheet(spec) {
  const o = { ...defaults, ...spec, acc: spec.acc ?? [] };
  const frames = { down: [0, 1, 2].map((f) => drawFront(o, f)), left: [0, 1, 2].map((f) => drawSide(o, f)), up: [0, 1, 2].map((f) => drawBack(o, f)) };
  frames.right = frames.left.map(mirrorRows);
  return frames;
}
/** 12コマを1枚のシート（48×96、行=向き 下・左・右・上、列=コマ）にする。歩きの順番は 1→2→3→2 */
export function sheetRows(frames) { const rows = []; for (const d of DIRS) for (let y = 0; y < H; y++) rows.push(frames[d].map((fr) => fr[y]).join("")); return rows; }
export function palFrom(p) {
  const pal = {};
  const map = { O: p.outline ?? "#1c1426", D: p.shadow ?? "#2a1f3a", S: p.skin[1], s: p.skin[0], E: p.eye ?? "#2a1e3a", W: "#ffffff", n: p.mouth ?? "#a04a4a", B: p.blush ?? p.skin[2] ?? "#f08a8a",
    h: p.hair[0], H: p.hair[1], g: p.hair[2], c: p.cloth[0], C: p.cloth[1], k: p.cloth[2], T: p.trim ?? "#e0c070", p: p.pants[0], P: p.pants[1], f: p.boots[0], F: p.boots[1],
    A: p.accent ?? "#d08a28", a: p.accent2 ?? p.cloth[0], M: "#8a90a0", N: "#c4c8d4", m: "#5a6070" };
  return { ...map, w: p.apron ?? "#c8c0b0", W: "#ffffff", ...(p.apronMain ? {} : {}), };
}
