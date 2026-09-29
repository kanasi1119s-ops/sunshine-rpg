// 実験の歪み（第3章のボス・v2）: 鉱山の地下の実験装置が歪んだ怪物。檻状の胴の中で、青緑の核が脈打つ。
// 垂れ下がる鎖の腕、錆びた配管、鉄仮面の頭。有機物（肉の管）が檻の中から絡みつく。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

const vnoise = (x, y, s) => { const fx = x / s, fy = y / s, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy; const a = hash(ix, iy), b = hash(ix + 1, iy), c = hash(ix, iy + 1), d = hash(ix + 1, iy + 1); const sx = tx * tx * (3 - 2 * tx), sy = ty * ty * (3 - 2 * ty); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy; };

const inPoly = (poly, x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
/** 多角形の板を、左上が明るい面として塗る（縁の左上は明るく、右下は暗く）。 */
function slab(g, poly, ramp, { bias = 0, seam = null } = {}) {
  const xs = poly.map((p) => p[0]), ys = poly.map((p) => p[1]); const x0 = Math.floor(Math.min(...xs)), x1 = Math.ceil(Math.max(...xs)), y0 = Math.floor(Math.min(...ys)), y1 = Math.ceil(Math.max(...ys));
  const n = ramp.length;
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    if (!inPoly(poly, x + 0.5, y + 0.5)) continue;
    const u = ((x - x0) / Math.max(1, x1 - x0)) * 0.55 + ((y - y0) / Math.max(1, y1 - y0)) * 0.75; // 0(左上)〜1.3(右下)
    let l = 1 - u / 1.3; let v = l * (n - 1.2) + bias;
    const ul = !inPoly(poly, x - 0.5, y - 0.5) || !inPoly(poly, x + 0.5, y - 1.5) && false; const tl = !inPoly(poly, x - 1 + 0.5, y + 0.5) || !inPoly(poly, x + 0.5, y - 1 + 0.5);
    const br = !inPoly(poly, x + 1 + 0.5, y + 0.5) || !inPoly(poly, x + 0.5, y + 1 + 0.5);
    if (br) v -= 1.2; else if (tl) v += 1.1;
    if (seam && seam(x, y)) v -= 1;
    put(g, y, x, ramp[clamp(Math.round(v), 0, n - 1)]);
  }
}
export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0a0810"), RIM = pal.rgb("縁明", "#2c2a44"), SHD = pal.rgb("影", "#110e1a");
  const IRON = pal.ramp("鉄", 228, 0.22, 5, 0.09, 0.56);
  const RUST = pal.ramp("錆", 22, 0.5, 4, 0.14, 0.5);
  const CORE = pal.ramp("核", 168, 0.85, 4, 0.32, 0.82);
  const FLESH = pal.ramp("肉", 335, 0.36, 3, 0.16, 0.42);
  const CHAIN = pal.ramp("鎖", 232, 0.14, 3, 0.16, 0.56);
  const g = makeGrid();
  const cx = 128;
  const inIron = (k) => IRON.includes(k) || CHAIN.includes(k);

  groundShadow(g, cx, 240, 104, 9, SHD);

  // ---- 後ろの配管（肩から頭の上へ、背中から床へ） ----
  limb(g, bezier([92, 96], [40, 70], [58, 24], 30), 8, 6, RUST, { ambient: 0.22 });
  limb(g, bezier([164, 96], [222, 74], [200, 30], 30), 8, 6, RUST, { ambient: 0.22 });
  limb(g, bezier([96, 190], [52, 200], [46, 232], 20), 7, 8, RUST, { ambient: 0.22 });
  limb(g, bezier([160, 190], [206, 200], [214, 232], 20), 7, 8, RUST, { ambient: 0.22 });

  // ---- 土台の鉄板 ----
  const base = heightField([{ cx, cy: 224, rx: 86, ry: 17, h: 1 }, { cx, cy: 214, rx: 66, ry: 14, h: 1 }], 5);
  paintField(g, base, IRON, { ambient: 0.28, tex: (x, y) => ((y - 208) % 12 === 0 ? -0.2 : 0) + (hash(x >> 1, y >> 1) < 0.05 ? 0.1 : 0) });

  // ---- 檻の胴（空洞） ----
  const cavity = (x, y) => {
    const t = (y - 74) / 132; const half = 46 + 6 * Math.sin(clamp(t, 0, 1) * Math.PI) - t * 4;
    return Math.abs(x - cx) < half && y >= 76 && y <= 204;
  };
  for (let y = 70; y <= 206; y++) for (let x = 70; x <= 186; x++) if (cavity(x, y)) put(g, y, x, y < 100 ? SHD : ((x + y) & 1 && y > 190 ? IRON[0] : SHD));
  // 奥の肋骨（背面の暗い板の筋）
  for (let y = 84; y < 200; y += 14) for (let x = 84; x < 172; x++) if (cavity(x, y)) put(g, y, x, IRON[0]);

  // ---- 核（脈打つ光）と、その光のかぶり ----
  const core = heightField([{ cx, cy: 138, rx: 27, ry: 27, h: 1 }, { cx: cx - 6, cy: 130, rx: 15, ry: 15, h: 0.9 }], 6);
  for (let a = 0; a < 6.283; a += 0.012) for (const [rr, k] of [[34, CORE[0]], [38, CORE[0]]]) if (Math.floor(a * 9) % 3 !== 0) { const x = cx + Math.cos(a) * rr, y = 138 + Math.sin(a) * rr; if (cavity(Math.round(x), Math.round(y)) && (g[Math.round(y)][Math.round(x)] < 0 || g[Math.round(y)][Math.round(x)] === SHD || g[Math.round(y)][Math.round(x)] === IRON[0])) put(g, y, x, k); }
  paintField(g, core, CORE, { ambient: 0.5, gain: 0.9, tex: (x, y) => Math.sin(Math.hypot(x - cx, y - 138) * 0.9) * 0.1 });
  // 核の内側の光の筋（脈）
  for (let a = 0; a < 6.283; a += 0.5) { let px = cx, py = 138; for (let i = 0; i < 20; i++) { px += Math.cos(a + Math.sin(i * 0.7 + a) * 0.5) * 1; py += Math.sin(a + Math.sin(i * 0.7 + a) * 0.5) * 1; const d = Math.hypot(px - cx, py - 138); if (d > 24) break; if (d > 8) put(g, py, px, CORE[1]); } }
  for (const [dx, dy] of [[-8, -9], [-7, -9], [-8, -8], [-9, -8]]) put(g, 138 + dy, cx + dx, CORE[3]);
  // 核のまわりで震える光の欠片（まとまった小片）
  for (const [sx, sy, r] of [[cx - 42, 124, 2], [cx + 44, 154, 2], [cx + 36, 108, 1], [cx - 34, 168, 1]]) for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++) if (Math.abs(x) + Math.abs(y) <= r && cavity(sx + x, sy + y)) put(g, sy + y, sx + x, r > 1 ? CORE[2] : CORE[1]);

  // ---- 檻の中の肉の管（有機物）: 核から鉄格子へ絡みつく ----
  const tend = [[[cx - 20, 150], [cx - 48, 160], [cx - 44, 194]], [[cx + 20, 150], [cx + 50, 166], [cx + 40, 196]], [[cx - 18, 122], [cx - 50, 116], [cx - 40, 86]], [[cx + 18, 124], [cx + 50, 110], [cx + 38, 84]], [[cx - 6, 162], [cx - 14, 186], [cx + 4, 202]]];
  for (const [a, b, c] of tend) limb(g, bezier(a, b, c, 22), 5, 3, FLESH, { ambient: 0.3 });
  ellipsoid(g, cx - 40, 198, 9, 6, FLESH, { ambient: 0.3 }); ellipsoid(g, cx + 38, 200, 8, 6, FLESH, { ambient: 0.3 });

  // ---- 檻の縦棒（鉄の円柱、左が明るい） ----
  const bar = (bx, y0, y1, w, ramp) => { for (let y = y0; y <= y1; y++) for (let t = 0; t < w; t++) { const f = t / (w - 1); put(g, y, bx + t, ramp[f < 0.2 ? 3 : f < 0.5 ? 2 : f < 0.8 ? 1 : 0]); } };
  for (const bx of [79, 96, 151, 168]) bar(bx, 78, 202, 6, IRON);
  for (const bx of [111, 139]) bar(bx, 78, 108, 4, IRON), bar(bx, 172, 202, 4, IRON);
  // 外枠の縦フレーム（太い柱）
  for (const [bx, w] of [[70, 9], [177, 9]]) { for (let y = 74; y <= 208; y++) for (let t = 0; t < w; t++) { const f = t / (w - 1); put(g, y, bx + t, IRON[f < 0.15 ? 4 : f < 0.4 ? 3 : f < 0.7 ? 2 : f < 0.88 ? 1 : 0]); } }
  // 横の帯（鋲つき）
  const band = (y0, h, x0, x1, ramp) => { for (let y = 0; y < h; y++) for (let x = x0; x <= x1; x++) { const f = y / (h - 1); let k = ramp[f < 0.2 ? 3 : f < 0.5 ? 2 : f < 0.8 ? 1 : 0]; put(g, y0 + y, x, k); } for (let x = x0 + 5; x < x1 - 3; x += 11) { put(g, y0 + 2, x, ramp[3]); put(g, y0 + 3, x + 1, ramp[0]); put(g, y0 + 2, x + 1, ramp[2]); put(g, y0 + 3, x, ramp[1]); } };
  band(86, 9, 68, 188, IRON); band(190, 10, 68, 188, IRON);
  band(136, 6, 70, 92, IRON); band(136, 6, 164, 186, IRON);
  // 斜めの当て板（錆）
  for (let i = 0; i < 46; i++) { const x = 90 + i * 1, y = 170 - i * 0.8; for (let t = 0; t < 4; t++) if (g[Math.round(y + t)]?.[x] >= 0 && IRON.includes(g[Math.round(y + t)][x])) { /* 棒の上に重ねる */ put(g, y + t, x, RUST[t < 1 ? 2 : t < 3 ? 1 : 0]); } }

  // ---- 頭（鉄仮面）と排気管 ----
  limb(g, bezier([112, 40], [96, 24], [84, 14], 14), 7, 4, RUST, { ambient: 0.25 });
  limb(g, bezier([146, 42], [160, 26], [172, 20], 14), 7, 4, RUST, { ambient: 0.25 });
  const HEAD = [[110, 22], [146, 22], [162, 40], [158, 62], [148, 78], [128, 86], [108, 78], [98, 62], [94, 40]];
  slab(g, HEAD, IRON, { bias: -0.1, seam: (x, y) => x === cx || x === cx - 1 && y < 44 });
  // 額の板（重なり）と、右半分を暗くする
  for (let y = 22; y <= 86; y++) for (let x = cx + 2; x <= 162; x++) if (inPoly(HEAD, x + 0.5, y + 0.5) && ((x * 7 + y * 3) % 11) < 5 && g[y][x] >= 0 && IRON.includes(g[y][x]) && IRON.indexOf(g[y][x]) > 0) g[y][x] = IRON[IRON.indexOf(g[y][x]) - 1];
  slab(g, [[100, 34], [156, 34], [152, 42], [104, 42]], IRON, { bias: -0.3 });
  // 目の溝（つり上がった斜めの目）と、光る目
  const eyeSlot = (pts) => { for (let y = 40; y <= 64; y++) for (let x = 96; x <= 160; x++) if (inPoly(pts, x + 0.5, y + 0.5)) put(g, y, x, OUT); };
  eyeSlot([[102, 50], [126, 54], [126, 62], [104, 58]]); eyeSlot([[130, 54], [154, 50], [152, 58], [130, 62]]);
  const glowPoly = (pts) => { const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]); for (let y = Math.min(...ys); y <= Math.max(...ys); y++) for (let x = Math.min(...xs); x <= Math.max(...xs); x++) if (inPoly(pts, x + 0.5, y + 0.5)) { const d = (y - Math.min(...ys)) / (Math.max(...ys) - Math.min(...ys) + 1); put(g, y, x, CORE[d < 0.35 ? 3 : d < 0.7 ? 2 : 1]); } };
  glowPoly([[106, 52], [124, 55], [124, 60], [107, 57]]); glowPoly([[132, 55], [150, 52], [149, 57], [132, 60]]);
  // 鼻筋の割れ目と光
  for (let y = 62; y < 76; y++) { put(g, y, cx - 1 + (y % 3 === 0 ? 1 : 0), OUT); }
  // あご板（少し開いて、中から核の光がのぞく）
  slab(g, [[108, 84], [148, 84], [140, 100], [128, 104], [116, 100]], IRON, { bias: -0.4 });
  for (let y = 86; y <= 96; y++) for (let x = 112; x <= 144; x++) if (inPoly([[108, 84], [148, 84], [140, 100], [128, 104], [116, 100]], x + 0.5, y + 0.5) && (x - 112) % 6 < 2) put(g, y, x, OUT);
  for (let x = 112; x <= 144; x += 6) { put(g, 86, x, CORE[1]); put(g, 87, x + 1, CORE[1]); }
  // 頭の鋲・冠のとげ
  for (const [x, y] of [[104, 30], [152, 30], [100, 66], [156, 66]]) { put(g, y, x, IRON[4]); put(g, y + 1, x, IRON[1]); put(g, y, x + 1, IRON[2]); }
  for (const [sx, h] of [[116, 12], [128, 18], [140, 12]]) for (let i = 0; i < h; i++) { const w = Math.round((h - i) / 4); for (let t = -w; t <= w; t++) put(g, 22 - i, sx + t, IRON[t < 0 ? 3 : t === 0 ? 2 : 1]); }

  // ---- 肩（大きな鉄の塊）と首の配管 ----
  const SL = [[34, 106], [46, 80], [72, 68], [98, 80], [100, 112], [78, 124], [46, 122]];
  const SR = [[222, 106], [210, 80], [184, 68], [158, 80], [156, 112], [178, 124], [210, 122]];
  slab(g, SL, IRON, { seam: (x, y) => (x + y * 2) % 17 === 0 });
  slab(g, SR, IRON, { bias: -0.5, seam: (x, y) => (x - y * 2 + 400) % 17 === 0 });
  slab(g, [[44, 84], [72, 74], [92, 84], [70, 92]], IRON, { bias: 0.4 });
  slab(g, [[212, 84], [184, 74], [164, 84], [186, 92]], IRON, { bias: -0.2 });
  limb(g, bezier([104, 72], [128, 82], [152, 72], 16), 6, 6, RUST, { ambient: 0.22 });
  for (const [x, y] of [[52, 100], [80, 108], [204, 100], [176, 108], [66, 116], [190, 116]]) { put(g, y, x, IRON[4]); put(g, y + 1, x, IRON[1]); put(g, y, x + 1, IRON[2]); put(g, y + 1, x + 1, IRON[0]); }

  // ---- 鎖 ----
  const chain = (pts, size, ramp, skip0 = 0) => {
    const path = []; for (let i = 0; i < pts.length - 1; i++) { const [x0, y0] = pts[i], [x1, y1] = pts[i + 1]; const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0)); for (let k = 0; k < n; k++) path.push([x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n]); }
    const step = size * 1.35; let acc = 0, idx = 0, last = path[0]; const links = [[path[0], 0]];
    for (let i = 1; i < path.length; i++) { acc += Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]); if (acc >= step) { acc = 0; links.push([path[i], i]); } }
    links.forEach(([p, i], li) => {
      if (li < skip0) return;
      const q = path[Math.min(path.length - 1, i + 2)], o = path[Math.max(0, i - 2)]; let tx = q[0] - o[0], ty = q[1] - o[1]; const tl = Math.hypot(tx, ty) || 1; tx /= tl; ty /= tl; const nx = -ty, ny = tx;
      const face = li % 2 === 0, a = size, b = face ? size * 0.62 : size * 0.26;
      const m = Math.ceil(a) + 2;
      for (let dy = -m; dy <= m; dy++) for (let dx = -m; dx <= m; dx++) {
        const u = dx * tx + dy * ty, v = dx * nx + dy * ny, e = (u / a) ** 2 + (v / b) ** 2;
        if (e > 1) continue; if (face && e < 0.42) continue;
        const l = (dx * -0.6 + dy * -0.8) / (a * 1.0); const inner = face && e < 0.62;
        let s = 1.1 + l * 1.5 - (inner ? 0.7 : 0) + (e > 0.85 ? -0.4 : 0.1);
        put(g, p[1] + dy, p[0] + dx, ramp[clamp(Math.round(s), 0, ramp.length - 1)]);
      }
    });
    return links[links.length - 1][0];
  };
  // 腕の鎖（肩から垂れて、床で重りにつながる）
  const armL = [...bezier([58, 108], [22, 150], [36, 206], 20)];
  const armR = [...bezier([198, 108], [236, 150], [220, 200], 20)];
  chain(armL, 6.4, CHAIN); chain(armR, 6.4, CHAIN);
  // 補助の鎖（胴の下、頭のわき）
  chain(bezier([96, 196], [78, 214], [82, 238], 12), 4.2, CHAIN);
  chain(bezier([160, 196], [178, 214], [174, 238], 12), 4.2, CHAIN);
  chain(bezier([104, 66], [82, 78], [80, 104], 10), 3.6, CHAIN);
  chain(bezier([152, 66], [176, 78], [178, 104], 10), 3.6, CHAIN);
  // 腕の先の重り（左は鉄塊、右は鉤つきの錘）
  const star = (cx0, cy0, ro, ri, n, rot) => Array.from({ length: n * 2 }, (_, i) => { const r = i % 2 ? ri : ro, t = rot + (i * Math.PI) / n; return [cx0 + Math.cos(t) * r, cy0 + Math.sin(t) * r]; });
  slab(g, star(36, 212, 23, 15, 7, 0.3), IRON, { bias: -0.2 });
  ellipsoid(g, 34, 210, 12, 12, IRON, { ambient: 0.3 });
  slab(g, star(220, 206, 21, 14, 6, 0.1), IRON, { bias: -0.4 });
  ellipsoid(g, 218, 204, 11, 11, IRON, { ambient: 0.3 });
  limb(g, bezier([222, 222], [238, 236], [222, 248], 10), 5, 3, CHAIN, { ambient: 0.25 });
  // 錘の中にも核と同じ光の割れ目
  for (const [wx, wy] of [[26, 204], [216, 196]]) for (let i = 0; i < 16; i++) { const x = wx + Math.round(i * 0.6 + (hash(i, wx) < 0.4 ? 1 : 0)), y = wy + i; if (g[y]?.[x] >= 0 && inIron(g[y][x])) { put(g, y, x, CORE[3]); put(g, y, x + 1, CORE[1]); } }

  // 排気管の口（つば）
  slab(g, [[76, 10], [94, 6], [96, 14], [80, 18]], IRON, { bias: -0.3 }); slab(g, [[164, 14], [182, 10], [180, 20], [164, 22]], IRON, { bias: -0.3 });
  // 核の光が土台に落ちる
  for (let y = 200; y < 236; y++) for (let x = 70; x < 190; x++) { const d = ((x - cx) / 46) ** 2 + ((y - 214) / 12) ** 2; const i = IRON.indexOf(g[y][x]); if (d < 1 && i >= 0 && y > 203 && ((x + y) % 2 === 0 || d < 0.12)) g[y][x] = CORE[d < 0.12 ? 1 : 0]; }
  // ---- 錆の染み（鉄の上に、まとまった塊で） ----
  for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { const k = g[y][x]; const i = IRON.indexOf(k); if (i < 0) continue; const n = vnoise(x, y, 9) * 0.65 + vnoise(x, y, 4) * 0.35; if (n > 0.66 && y > 120) g[y][x] = RUST[Math.min(i, 3)]; }
  // ---- ひび割れ（核の光が漏れる） ----
  const crack = (x, y, dir, n) => { for (let i = 0; i < n; i++) { x += dir[0] * (hash(i, x) < 0.6 ? 1 : 0); y += dir[1] * (hash(i, y + 3) < 0.7 ? 1 : 0) + (dir[1] === 0 ? 0 : 0); if (g[y]?.[x] >= 0 && inIron(g[y][x]) || (g[y]?.[x] >= 0 && IRON.includes(g[y][x]))) { put(g, y, x, CORE[3]); put(g, y + 1, x, CORE[1]); } if (dir[0] === 0) y += 0; } };
  crack(60, 86, [1, 1], 20); crack(112, 34, [1, 1], 8); crack(186, 92, [-1, 1], 18); crack(150, 40, [-1, 1], 8);

  despeckle(g);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M3-実験の歪み", g)]; })();
