// 実験の歪み（第3章のボス・v2）: 鉱山の地下の実験装置が歪んだ怪物。檻状の胴の中で、青緑の核が脈打つ。
// 垂れ下がる鎖の腕、錆びた配管、鉄仮面の頭。有機物（肉の管）が檻の中から絡みつく。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

const vnoise = (x, y, s) => { const fx = x / s, fy = y / s, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy; const a = hash(ix, iy), b = hash(ix + 1, iy), c = hash(ix, iy + 1), d = hash(ix + 1, iy + 1); const sx = tx * tx * (3 - 2 * tx), sy = ty * ty * (3 - 2 * ty); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy; };

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0a0810"), RIM = pal.rgb("縁明", "#2c2a44"), SHD = pal.rgb("影", "#110e1a");
  const IRON = pal.ramp("鉄", 228, 0.2, 5, 0.1, 0.66);
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
  const head = heightField([{ cx, cy: 48, rx: 32, ry: 27, h: 1 }, { cx, cy: 40, rx: 22, ry: 24, h: 0.9 }, { cx, cy: 66, rx: 20, ry: 11, h: 0.8 }], 5);
  paintField(g, head, IRON, { ambient: 0.28, tex: (x, y) => (Math.abs(x - cx) < 1 ? -0.25 : 0) });
  // 目の溝と、光る目（大きな左目・小さな右目）
  for (let y = 44; y <= 58; y++) for (let x = 100; x <= 156; x++) { const a = (x - cx) / 28, b = (y - 51) / 7; if (a * a + b * b < 1) put(g, y, x, OUT); }
  const glowEye = (ex, ey, rx, ry) => { for (let y = -ry; y <= ry; y++) for (let x = -rx; x <= rx; x++) { const d = (x / rx) ** 2 + (y / ry) ** 2; if (d <= 1) put(g, ey + y, ex + x, CORE[d < 0.25 ? 3 : d < 0.6 ? 2 : 1]); } };
  glowEye(118, 51, 9, 5); glowEye(142, 52, 6, 4);
  // 口の格子（歯の板）
  for (let x = 114; x <= 142; x += 4) for (let y = 62; y <= 72; y++) put(g, y, x, y > 68 ? IRON[1] : OUT);
  for (let x = 112; x <= 144; x++) put(g, 62, x, OUT);
  // 頭の鋲・縁
  for (const [x, y] of [[104, 36], [152, 36], [110, 60], [146, 60]]) { put(g, y, x, IRON[4]); put(g, y + 1, x, IRON[1]); put(g, y, x + 1, IRON[2]); }

  // ---- 肩（大きな鉄の塊）と首の配管 ----
  const shoulderL = heightField([{ cx: 66, cy: 96, rx: 27, ry: 19, h: 1 }, { cx: 62, cy: 90, rx: 20, ry: 14, h: 0.9 }], 5);
  const shoulderR = heightField([{ cx: 190, cy: 96, rx: 27, ry: 19, h: 1 }, { cx: 186, cy: 90, rx: 20, ry: 14, h: 0.9 }], 5);
  paintField(g, shoulderL, IRON, { ambient: 0.26, tex: (x, y) => ((x + y) % 13 === 0 ? -0.18 : 0) });
  paintField(g, shoulderR, IRON, { ambient: 0.26, tex: (x, y) => ((x + y) % 13 === 0 ? -0.18 : 0) });
  limb(g, bezier([104, 72], [128, 82], [152, 72], 16), 6, 6, RUST, { ambient: 0.22 });
  for (const [x, y] of [[54, 86], [70, 100], [178, 86], [194, 100], [62, 108], [186, 108]]) { put(g, y, x, IRON[4]); put(g, y + 1, x, IRON[1]); put(g, y, x + 1, IRON[2]); put(g, y + 1, x + 1, IRON[0]); }

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
  const wL = heightField([{ cx: 36, cy: 212, rx: 20, ry: 17, h: 1 }, { cx: 32, cy: 206, rx: 13, ry: 11, h: 0.9 }], 5);
  paintField(g, wL, IRON, { ambient: 0.26, tex: (x, y) => ((y - 200) % 9 === 0 ? -0.2 : 0) });
  for (let a = 0; a < 6; a++) { const sx = 22 + a * 5; for (let t = 0; t < 5 - Math.abs(2 - a) * 1; t++) put(g, 226 + t, sx, IRON[t < 2 ? 3 : 1]); }
  const wR = heightField([{ cx: 220, cy: 206, rx: 18, ry: 16, h: 1 }, { cx: 216, cy: 200, rx: 12, ry: 10, h: 0.9 }], 5);
  paintField(g, wR, IRON, { ambient: 0.26, tex: (x, y) => ((y - 196) % 9 === 0 ? -0.2 : 0) });
  limb(g, bezier([222, 218], [236, 232], [222, 244], 10), 5, 3, CHAIN, { ambient: 0.25 });
  // 錘の中にも核と同じ光の割れ目
  for (const [wx, wy] of [[26, 204], [216, 196]]) for (let i = 0; i < 16; i++) { const x = wx + Math.round(i * 0.6 + (hash(i, wx) < 0.4 ? 1 : 0)), y = wy + i; if (g[y]?.[x] >= 0 && inIron(g[y][x])) { put(g, y, x, CORE[3]); put(g, y, x + 1, CORE[1]); } }

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
