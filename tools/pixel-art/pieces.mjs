// 10点のドット絵（64×64）。palette の並び順が、エディタ上の記号の並び順（色番号）になる。
import { N, hash, makeGrid, put, get, rect, ellipse, toneOf, outline, shadow, refine } from "./lib.mjs";

const E = 0; // 縁取り色は常に色番号0

/** 葉のかたまりを重ねた樹冠・茂み。 */
function leafMass(g, blobs, ramp, seedBase = 0) {
  blobs.sort((a, b) => a[1] - b[1]);
  for (const [cx, cy, r] of blobs) {
    ellipse(g, cx, cy, r, r * 0.92, (rr, c, nx, ny, d, light) => {
      let t = toneOf(ramp, light, d, 0.16, [c + seedBase, rr]);
      if (d > 0.86) t = ramp[0];
      return t;
    });
  }
}

const tree = () => {
  const g = makeGrid();
  // pal: 0縁 1-5緑 6-8幹(明中暗) 9影
  shadow(g, 33, 58, 26, 5, 9);
  for (let r = 38; r <= 58; r++) { const w = r > 54 ? 7 : 5; for (let c = 32 - w; c <= 32 + w; c++) put(g, r, c, c < 30 ? 6 : c > 34 ? 8 : 7); }
  for (const [r, c] of [[56, 22], [57, 23], [56, 42], [57, 41], [58, 20], [58, 44]]) put(g, r, c, 8);
  const G = [1, 2, 3, 4, 5];
  leafMass(g, [[32, 14, 12], [18, 24, 11], [46, 24, 11], [32, 26, 13], [22, 36, 9], [42, 36, 9], [32, 38, 10], [26, 10, 7], [40, 12, 7]], G);
  outline(g, E, [9]);
  refine(g, [[1,2,3,4,5],[6,7,8]]);
  return g;
};
const treePal = [["縁", "#0a1a10"], ["葉1", "#124018"], ["葉2", "#1f6a1f"], ["葉3", "#33962a"], ["葉4", "#66c238"], ["葉5", "#b4ec5c"], ["幹明", "#8a5a2e"], ["幹中", "#62401e"], ["幹暗", "#3a2210"], ["影", "#1d4a1c"]];

const rock = () => {
  const g = makeGrid();
  // pal: 0縁 1-5岩 6-7苔 8影
  shadow(g, 33, 55, 28, 6, 8);
  const R = [1, 2, 3, 4, 5];
  ellipse(g, 32, 38, 26, 18, (r, c, nx, ny, d, light) => {
    let t = light > 0.45 ? 4 : light > 0.05 ? 3 : light > -0.35 ? 2 : 1;
    const facet = Math.floor((c + r * 0.6) / 9) % 3;                       // 面の切り替え
    if (facet === 0) t = Math.min(4, t + 1); else if (facet === 2) t = Math.max(1, t - 1);
    if (d > 0.9) t = 0; if (hash(c, r) < 0.1) t = Math.max(0, t - 1);
    return R[t];
  }, 2.6);
  ellipse(g, 46, 46, 12, 9, (r, c, nx, ny, d, light) => R[light > 0 ? 3 : d > 0.85 ? 0 : 2], 2.4);
  for (const [cx, cy, rx] of [[22, 24, 8], [34, 22, 6], [44, 27, 5]]) ellipse(g, cx, cy, rx, 3, (r, c, nx, ny) => (hash(c, r) < 0.85 ? (ny < 0 ? 7 : 6) : null));
  outline(g, E, [8]);
  refine(g, [[1,2,3,4,5],[6,7]]);
  return g;
};
const rockPal = [["縁", "#14161a"], ["岩1", "#3a3f46"], ["岩2", "#5c636b"], ["岩3", "#858d94"], ["岩4", "#aab2b6"], ["岩5", "#d4dadb"], ["苔", "#3f9a26"], ["苔明", "#7fcb35"], ["影", "#1d4a1c"]];

const well = () => {
  const g = makeGrid();
  // pal: 0縁 1-5石 6-8木(明中暗) 9水暗 10水 11屋根暗 12屋根 13屋根明 14影 15縄
  shadow(g, 33, 59, 24, 4, 14);
  const S = [1, 2, 3, 4, 5];
  // 井戸の胴（円筒）
  for (let r = 38; r <= 56; r++) for (let c = 14; c <= 50; c++) {
    const nx = (c - 32) / 18; if (Math.abs(nx) > 1) continue;
    const curve = Math.sqrt(1 - nx * nx);
    if (r > 38 + 5 * (1 - curve) * 0 + 0 && r > 38 + (1 - curve) * 0) {
      const bottom = 56 + (1 - curve) * -4 + 3 * (1 - curve);
      if (r > 56 - 3 * (1 - curve)) continue;
    }
    let t = nx < -0.5 ? 4 : nx < 0 ? 3 : nx < 0.5 ? 2 : 1;
    if ((r + Math.floor(c / 6) * 2) % 6 === 0) t = Math.max(0, t - 1);
    if ((c + (Math.floor(r / 6) % 2) * 3) % 6 === 0) t = Math.max(0, t - 1);
    put(g, r, c, S[t]);
  }
  ellipse(g, 32, 38, 19, 7, (r, c, nx, ny, d) => (d > 0.72 ? S[4] : d > 0.55 ? S[2] : 9)); // 縁と水面
  ellipse(g, 32, 38, 12, 4, (r, c, nx, ny) => (hash(c >> 1, r) < 0.25 ? 10 : 9));
  // 支柱と屋根
  for (const x0 of [15, 47]) for (let r = 12; r <= 40; r++) for (let c = x0; c <= x0 + 2; c++) put(g, r, c, c === x0 ? 6 : c === x0 + 1 ? 7 : 8);
  for (let r = 4; r <= 15; r++) { const h = 3 + (r - 4) * 2.4; for (let c = Math.round(32 - h); c <= Math.round(32 + h); c++) { let t = c < 32 ? 12 : 11; if ((r + Math.floor(c / 4)) % 3 === 0) t = c < 32 ? 13 : 12; if (c < 32 - h + 2) t = 13; put(g, r, c, t); } }
  rect(g, 16, 16, 16, 48, 11);
  // 滑車と縄・桶
  rect(g, 17, 32, 30, 32, 15); rect(g, 30, 29, 35, 35, 7); rect(g, 30, 29, 30, 35, 6); rect(g, 35, 29, 35, 35, 8);
  outline(g, E, [14]);
  refine(g, [[1,2,3,4,5],[6,7,8],[11,12,13],[9,10]]);
  return g;
};
const wellPal = [["縁", "#14161a"], ["石1", "#45454a"], ["石2", "#6a6a64"], ["石3", "#8f8f88"], ["石4", "#b4b4ac"], ["石5", "#d8d8d0"], ["木明", "#8a5a2e"], ["木中", "#62401e"], ["木暗", "#3a2210"], ["水暗", "#0f3f5c"], ["水", "#3fa5b0"], ["屋根暗", "#64221f"], ["屋根", "#b0432e"], ["屋根明", "#ee8a55"], ["影", "#1d4a1c"], ["縄", "#c8b078"]];

const chest = () => {
  const g = makeGrid();
  // pal: 0縁 1-3木(暗中明) 4-5金属(暗明) 6金 7金明 8影
  shadow(g, 33, 55, 26, 5, 8);
  // 箱の胴
  for (let r = 34; r <= 54; r++) for (let c = 10; c <= 54; c++) { let t = c < 30 ? 3 : c < 44 ? 2 : 1; if ((c - 10) % 9 === 0) t = 1; if (hash(c, r) < 0.07) t = Math.max(1, t - 1); if (r > 51) t = 1; put(g, r, c, t); }
  // ふた（かまぼこ形）
  ellipse(g, 32, 34, 23, 16, (r, c, nx, ny, d, light) => (r > 34 ? null : (d > 0.9 ? 1 : light > 0.3 ? 3 : light > -0.2 ? 2 : 1)));
  for (let c = 9; c <= 55; c++) { put(g, 34, c, 5); put(g, 35, c, 4); }
  // 金具の帯
  for (const x0 of [12, 49]) for (let r = 20; r <= 54; r++) { const top = r < 34 ? Math.abs(x0 - 32) < 22 : true; if (r < 34) { const nx = (x0 + 1 - 32) / 23; const ymax = 34 - 16 * Math.sqrt(Math.max(0, 1 - nx * nx)); if (r < ymax) continue; } put(g, r, x0, 5); put(g, r, x0 + 1, 5); put(g, r, x0 + 2, 4); }
  // 錠前
  rect(g, 32, 28, 42, 36, 6); rect(g, 32, 28, 33, 36, 7); rect(g, 40, 28, 42, 36, 4); rect(g, 36, 31, 39, 33, 1);
  for (const [r, c] of [[38, 13], [38, 50], [47, 13], [47, 50]]) put(g, r, c, 7);
  outline(g, E, [8]);
  refine(g, [[1,2,3],[4,5],[6,7]]);
  return g;
};
const chestPal = [["縁", "#1a1010"], ["木暗", "#4a2a12"], ["木中", "#7a4a24"], ["木明", "#a06a38"], ["金属暗", "#4a4a52"], ["金属明", "#9a9aa4"], ["金", "#e8b830"], ["金明", "#fff0a0"], ["影", "#1d4a1c"]];

const lamp = () => {
  const g = makeGrid();
  // pal: 0縁 1-3鉄(暗中明) 4-8光(暗→明) 9影 10ガラス縁
  shadow(g, 33, 59, 14, 3, 9);
  // 光のにじみ（ディザ）
  ellipse(g, 32, 22, 26, 22, (r, c, nx, ny, d) => (d > 0.5 && (r + c) % 2 === 0 && hash(c, r) < 0.55 * (1 - d) * 1.6 ? 4 : null));
  for (let r = 34; r <= 58; r++) for (let c = 30; c <= 34; c++) put(g, r, c, c === 30 ? 3 : c < 33 ? 2 : 1);
  rect(g, 55, 26, 58, 38, 2); rect(g, 55, 26, 55, 38, 3); rect(g, 58, 26, 58, 38, 1);
  // ランタンの枠と灯り石
  rect(g, 12, 22, 34, 42, 1); rect(g, 12, 22, 12, 42, 3);
  for (let r = 15; r <= 31; r++) for (let c = 25; c <= 39; c++) { const d = Math.hypot((c - 32) / 8, (r - 23) / 9); put(g, r, c, d < 0.35 ? 8 : d < 0.7 ? 7 : d < 1 ? 6 : 5); }
  for (let r = 15; r <= 31; r++) { put(g, r, 32, 2); }
  for (let i = 0; i < 8; i++) { put(g, 12 - i / 2, 22 + i, 3); put(g, 12 - i / 2, 42 - i, 2); }
  rect(g, 4, 30, 8, 34, 2); rect(g, 8, 26, 11, 38, 3); rect(g, 11, 22, 11, 42, 2);
  rect(g, 34, 22, 36, 42, 2);
  outline(g, E, [9, 4]);
  refine(g, [[1,2,3],[4,5,6,7,8]]);
  return g;
};
const lampPal = [["縁", "#10101a"], ["鉄暗", "#2a2a34"], ["鉄中", "#4a4a58"], ["鉄明", "#7a7a8a"], ["光0", "#8a6a1a"], ["光1", "#d89a20"], ["光2", "#f8c840"], ["光3", "#fff0a0"], ["光4", "#ffffff"], ["影", "#1d4a1c"]];

const signAndBarrel = () => {
  const g = makeGrid();
  // pal: 0縁 1-3木 4-5鉄 6板明 7板 8板暗 9影 10文字
  shadow(g, 32, 59, 28, 4, 9);
  // 標識柱
  for (let r = 6; r <= 58; r++) for (let c = 14; c <= 19; c++) put(g, r, c, c < 16 ? 3 : c < 18 ? 2 : 1);
  // 矢印板
  for (let r = 10; r <= 24; r++) for (let c = 16; c <= 48; c++) { const tip = c > 40 ? Math.abs(r - 17) > (48 - c) * 1.1 : false; if (tip) continue; put(g, r, c, r < 12 ? 6 : r > 22 ? 8 : 7); }
  for (const c of [22, 30, 36]) for (let r = 14; r <= 20; r++) put(g, r, c + (r % 3), 10); // 文字風の線
  put(g, 12, 18, 4); put(g, 22, 18, 4);
  // 樽
  ellipse(g, 46, 44, 13, 14, (r, c, nx, ny, d, light) => { if (d > 1) return null; const band = [-0.6, 0.55].some((b) => Math.abs(ny - b) < 0.12); let t = nx < -0.4 ? 3 : nx < 0.2 ? 2 : 1; if (Math.floor((c + 2) / 3) % 2 === 0) t = Math.max(1, t - 1); if (band) t = nx < 0 ? 5 : 4; return t; }, 2.4);
  ellipse(g, 46, 32, 11, 3, (r, c, nx, ny, d) => (d > 0.7 ? 4 : 2));
  outline(g, E, [9]);
  refine(g, [[1,2,3],[6,7,8],[4,5]]);
  return g;
};
const signPal = [["縁", "#1a1010"], ["木暗", "#4a2a12"], ["木中", "#7a4a24"], ["木明", "#a06a38"], ["鉄暗", "#3a3a44"], ["鉄明", "#8a8a98"], ["板明", "#e6c890"], ["板", "#c89c58"], ["板暗", "#8a6634"], ["影", "#1d4a1c"], ["文字", "#4a2a12"]];

const bush = () => {
  const g = makeGrid();
  // pal: 0縁 1-5緑 6花桃 7花黄 8花白 9影
  shadow(g, 32, 56, 27, 5, 9);
  leafMass(g, [[32, 30, 14], [16, 38, 10], [48, 38, 10], [24, 26, 9], [42, 26, 9], [32, 44, 12]], [1, 2, 3, 4, 5], 3);
  const cols = [6, 7, 8];
  for (let i = 0; i < 20; i++) { const c = 10 + Math.floor(hash(i, 3) * 44), r = 22 + Math.floor(hash(i, 4) * 30); if (get(g, r, c) > 0 && get(g, r, c) < 6) { const k = cols[i % 3]; put(g, r, c, k); put(g, r, c + 1, k); put(g, r - 1, c, k); put(g, r + 1, c, k); put(g, r, c - 1, k); put(g, r, c, 7); } }
  outline(g, E, [9]);
  refine(g, [[1,2,3,4,5]]);
  return g;
};
const bushPal = [["縁", "#0a1a10"], ["葉1", "#124018"], ["葉2", "#1f6a1f"], ["葉3", "#33962a"], ["葉4", "#66c238"], ["葉5", "#b4ec5c"], ["花桃", "#ff86a4"], ["花黄", "#ffe25a"], ["花白", "#ffffff"], ["影", "#1d4a1c"]];

const stump = () => {
  const g = makeGrid();
  // pal: 0縁 1-4木肌 5-7年輪(暗中明) 8苔 9影
  shadow(g, 32, 57, 28, 5, 9);
  // 丸太（横倒し）
  for (let r = 40; r <= 54; r++) for (let c = 8; c <= 52; c++) { const ny = (r - 47) / 7.5; let t = ny < -0.5 ? 4 : ny < 0 ? 3 : ny < 0.6 ? 2 : 1; if (hash(c >> 2, r) < 0.16 && (c + r) % 3 === 0) t = Math.max(1, t - 1); put(g, r, c, t); }
  ellipse(g, 52, 47, 5, 8, (r, c, nx, ny, d) => (Math.floor(d * 4) % 2 === 0 ? 6 : 5));
  // 切り株
  for (let r = 22; r <= 52; r++) for (let c = 22 + (r < 26 ? 0 : 0); c <= 46; c++) { const nx = (c - 34) / 12; let t = nx < -0.4 ? 4 : nx < 0.3 ? 3 : 2; if (r > 48) t = 1; if (hash(c, r >> 1) < 0.2 && c % 2) t = Math.max(1, t - 1); put(g, r, c, t); }
  for (const [r, c] of [[50, 20], [51, 21], [50, 48], [51, 47], [52, 19], [52, 49]]) put(g, r, c, 1);
  ellipse(g, 34, 22, 13, 5, (r, c, nx, ny, d) => (d > 0.85 ? 5 : Math.floor(Math.hypot(nx * 1.2, ny * 2.4) * 4) % 2 === 0 ? 7 : 6));
  for (const [cx, cy] of [[24, 28], [26, 34], [43, 30]]) ellipse(g, cx, cy, 3, 2, () => 8);
  outline(g, E, [9]);
  refine(g, [[1,2,3,4],[5,6,7]]);
  return g;
};
const stumpPal = [["縁", "#1a1010"], ["木肌1", "#3a2210"], ["木肌2", "#62401e"], ["木肌3", "#8a5a2e"], ["木肌4", "#b07840"], ["年輪暗", "#a06a38"], ["年輪", "#d8a868"], ["年輪明", "#f0d090"], ["苔", "#3f9a26"], ["影", "#1d4a1c"]];

const bridge = () => {
  const g = makeGrid();
  // pal: 0縁 1-5水 6-8板(暗中明) 9欄干 10泡
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) { let t = 3 + (((c >> 1) + (r >> 1) + (r >> 2)) % 4 === 0 ? 1 : ((c >> 1) + (r >> 1)) % 4 === 2 ? -1 : 0); if (hash(c, r) < 0.04) t = 5; if (r < 4 || r > 59) t = 2; put(g, r, c, t); }
  // 橋板（横向きの板を並べる。1枚ずつ色を変え、継ぎ目を暗くする）
  for (let r = 12; r <= 51; r++) for (let c = 6; c <= 57; c++) {
    const plank = Math.floor((r - 12) / 5), inP = (r - 12) % 5;
    let k = plank % 3 === 0 ? 8 : plank % 3 === 1 ? 7 : 8;
    if (inP === 0) k = 8; else if (inP === 4) k = 6;
    if (hash(c >> 2, plank) < 0.5 && (c + plank * 7) % 16 === 0) k = 6;     // 板の継ぎ目
    if (hash(c, r) < 0.05) k = Math.max(6, k - 1);
    put(g, r, c, k);
  }
  // 橋の影と欄干
  rect(g, 52, 6, 56, 57, 2);
  for (const r0 of [8, 50]) { rect(g, r0, 4, r0 + 3, 59, 9); rect(g, r0, 4, r0, 59, 8); rect(g, r0 + 3, 4, r0 + 3, 59, 6); for (let c = 6; c <= 57; c += 12) rect(g, r0 - 2, c, r0 + 6, c + 2, 7); }
  for (const c of [4, 57]) for (let r = 6; r <= 11; r++) put(g, r, c, 10);
  outline(g, E, []);
  refine(g, [[1,2,3,4,5],[6,7,8]]);
  return g;
};
const bridgePal = [["縁", "#101820"], ["水1", "#0f3f5c"], ["水2", "#1a6d8c"], ["水3", "#2f8fa8"], ["水4", "#5cc0c8"], ["水5", "#d0f4ee"], ["板暗", "#4a2a12"], ["板中", "#7a4a24"], ["板明", "#b07840"], ["欄干", "#62401e"], ["泡", "#ffffff"]];

const cave = () => {
  const g = makeGrid();
  // pal: 0縁 1-5岩 6闇 7苔 8影 9光
  shadow(g, 32, 60, 30, 3, 8);
  const R = [1, 2, 3, 4, 5];
  ellipse(g, 32, 38, 30, 24, (r, c, nx, ny, d, light) => {
    if (r > 58) return null;
    let t = light > 0.4 ? 4 : light > 0.0 ? 3 : light > -0.4 ? 2 : 1; if ((r + Math.floor(c / 3)) % 4 === 0) t = Math.max(0, t - 1); if (hash(c, r) < 0.1) t = Math.min(4, t + 1); if (d > 0.9) t = 0; return R[t];
  }, 2.2);
  // 洞口（アーチ）
  ellipse(g, 32, 48, 14, 16, (r, c, nx, ny, d) => (r > 56 ? null : d > 0.88 ? 1 : 6), 2.4);
  for (let r = 30; r <= 58; r++) for (let c = 18; c <= 46; c++) if (get(g, r, c) === 6 && (r + c) % 5 === 0 && hash(c, r) < 0.4) put(g, r, c, 1);
  // 洞口の上のつらら石（下向きの石筍）
  for (let c = 20; c <= 44; c += 4) { const len = 3 + Math.floor(hash(c, 1) * 5); for (let i = 0; i < len; i++) { put(g, 33 + i, c + (i < 2 ? 0 : 0), 3); put(g, 33 + i, c + 1, i < len - 1 ? 2 : -1); } }
  // 苔と光（奥）
  for (let c = 12; c <= 52; c++) if (hash(c, 9) < 0.5) put(g, 20 + Math.floor(hash(c, 2) * 10), c, 7);
  for (let r = 50; r <= 57; r++) for (let c = 30; c <= 34; c++) if (hash(c, r) < 0.6) put(g, r, c, 9);
  outline(g, E, [8]);
  refine(g, [[1,2,3,4,5]]);
  return g;
};
const cavePal = [["縁", "#14100e"], ["岩1", "#2a2428"], ["岩2", "#4a4046"], ["岩3", "#71646a"], ["岩4", "#9c8c90"], ["岩5", "#c8bcbc"], ["闇", "#0a0810"], ["苔", "#3f7a26"], ["影", "#1d4a1c"], ["光", "#5a8a78"]];

export const PIECES = [
  { name: "01-大木", pal: treePal, build: tree },
  { name: "02-岩", pal: rockPal, build: rock },
  { name: "03-井戸", pal: wellPal, build: well },
  { name: "04-宝箱", pal: chestPal, build: chest },
  { name: "05-街灯", pal: lampPal, build: lamp },
  { name: "06-標識と樽", pal: signPal, build: signAndBarrel },
  { name: "07-花の茂み", pal: bushPal, build: bush },
  { name: "08-切り株と丸太", pal: stumpPal, build: stump },
  { name: "09-木の橋", pal: bridgePal, build: bridge },
  { name: "10-洞窟の入口", pal: cavePal, build: cave },
];
