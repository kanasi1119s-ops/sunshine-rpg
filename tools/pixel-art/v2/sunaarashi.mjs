// 砂嵐の歪み（第4章のボス・v2）: 砂漠の砂嵐が形をもったもの。渦を巻く砂の体、ぼろ布の外套、仮面のような空洞の顔、周りを回る瓦礫。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

const vnoise = (x, y, s) => { const fx = x / s, fy = y / s, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy; const a = hash(ix, iy), b = hash(ix + 1, iy), c = hash(ix, iy + 1), d = hash(ix + 1, iy + 1); const sx = tx * tx * (3 - 2 * tx), sy = ty * ty * (3 - 2 * ty); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy; };
const inPoly = (poly, x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
function slab(g, poly, ramp, { bias = 0, seam = null } = {}) {
  const xs = poly.map((p) => p[0]), ys = poly.map((p) => p[1]); const x0 = Math.floor(Math.min(...xs)), x1 = Math.ceil(Math.max(...xs)), y0 = Math.floor(Math.min(...ys)), y1 = Math.ceil(Math.max(...ys));
  const n = ramp.length;
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    if (!inPoly(poly, x + 0.5, y + 0.5)) continue;
    const u = ((x - x0) / Math.max(1, x1 - x0)) * 0.55 + ((y - y0) / Math.max(1, y1 - y0)) * 0.75;
    let v = (1 - u / 1.3) * (n - 1.2) + bias;
    const tl = !inPoly(poly, x - 0.5, y + 0.5) || !inPoly(poly, x + 0.5, y - 0.5);
    const br = !inPoly(poly, x + 1.5, y + 0.5) || !inPoly(poly, x + 0.5, y + 1.5);
    if (br) v -= 1.2; else if (tl) v += 1.1;
    if (seam && seam(x, y)) v -= 1;
    put(g, y, x, ramp[clamp(Math.round(v), 0, n - 1)]);
  }
}

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0d0810"), RIM = pal.rgb("縁明", "#3a2434"), SHD = pal.rgb("影", "#1a1018");
  const SAND = pal.ramp("砂", 32, 0.46, 5, 0.09, 0.6);
  const CLOTH = pal.ramp("布", 352, 0.32, 4, 0.08, 0.38);
  const BONE = pal.ramp("骨", 40, 0.34, 5, 0.16, 0.86);
  const VIO = pal.ramp("光", 285, 0.85, 4, 0.34, 0.8);
  const ROCK = pal.ramp("瓦礫", 24, 0.16, 4, 0.12, 0.5);
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 240, 96, 8, SHD);

  // ---- 後ろの瓦礫（渦の奥を回る） ----
  const rock = (pts, bias = 0) => { slab(g, pts, ROCK, { bias }); };
  rock([[24, 52], [44, 40], [58, 50], [52, 68], [30, 70]], -0.3);
  rock([[206, 30], [232, 26], [240, 44], [220, 56]], -0.5);
  rock([[10, 156], [26, 148], [34, 162], [22, 176]], -0.4);

  // ---- 後ろのぼろ布（風になびく外套の裾） ----
  const zig = (pts) => pts;
  slab(g, [[150, 104], [196, 92], [246, 108], [232, 120], [250, 132], [226, 140], [240, 154], [210, 154], [216, 168], [176, 156], [150, 150]], CLOTH, { bias: -0.5, seam: (x, y) => (x * 2 - y * 3 + 900) % 15 === 0 });
  slab(g, [[106, 112], [66, 100], [16, 92], [30, 106], [8, 116], [34, 124], [14, 140], [44, 142], [40, 158], [80, 150], [106, 152]], CLOTH, { bias: -0.6, seam: (x, y) => (x * 2 + y * 3) % 15 === 0 });

  // ---- 砂の渦（逆円すい。上が広く、下は土の上でほどける） ----
  const parts = [];
  for (let y = 40; y <= 232; y += 8) {
    const t = (y - 40) / 192, rx = 84 * Math.pow(1 - t, 0.85) + 16 + (y < 60 ? 8 : 0), lean = 10 * Math.sin(t * 5 + 0.6) - t * 8;
    parts.push({ cx: cx + lean, cy: y, rx, ry: 15, h: 1 });
  }
  const hf0 = heightField(parts, 5);
  const hf = (x, y) => { const h = hf0(x, y); if (h <= 0) return 0; return h - (h < 0.4 ? 0.2 * vnoise(x - y * 0.6, y * 2.2, 7) : 0); };
  const asin = (v) => Math.asin(clamp(v, -1, 1));
  paintField(g, hf, SAND, {
    ambient: 0.14, gain: 0.9, thr: 0.03,
    tex: (x, y) => {
      const t = (y - 40) / 192, half = 84 * Math.pow(1 - clamp(t, 0, 1), 0.85) + 16, u = (x - cx) / half;
      const ph = y * 0.15 + asin(u) * 2.6 + Math.sin(y * 0.05) * 1.5, s = Math.sin(ph) + (u > 0.35 ? -0.4 * (u - 0.35) : 0);
      return (s > 0.6 ? 0.2 : s < -0.35 ? -0.22 : 0) + (Math.abs(s - 0.6) < 0.12 && (x + y) % 2 === 0 ? 0.12 : 0) + (Math.abs(s + 0.35) < 0.12 && (x + y) % 2 === 0 ? -0.12 : 0) + (hash(x >> 1, y >> 1) < 0.07 ? -0.08 : 0);
    },
  });
  // 渦の筋（明るい細い帯が巻き付く）
  for (let k = 0; k < 6; k++) {
    const y0 = 56 + k * 28;
    for (let a = -1.35; a <= 1.35; a += 0.014) {
      const t = (y0 + 20 - 40) / 192, half = 84 * Math.pow(1 - clamp(t, 0, 1), 0.85) + 16, x = cx + Math.sin(a) * half * 0.98, y = y0 + a * 9 + (Math.cos(a) * 12);
      const on = g[Math.round(y)]?.[Math.round(x)]; if (on >= 0 && SAND.includes(on) && (a > -1.2) && (Math.floor(a * 5 + k) % 4 !== 0)) { put(g, y, x, SAND[a < -0.2 ? 4 : 3]); put(g, y + 1, x, SAND[1]); }
    }
  }
  // 下の砂だまり
  const mh = heightField([{ cx, cy: 236, rx: 84, ry: 10, h: 1 }, { cx: cx - 20, cy: 232, rx: 44, ry: 10, h: 1 }], 5); paintField(g, (x, y) => { const h = mh(x, y); return h <= 0 ? 0 : h - (h < 0.5 ? 0.3 * vnoise(x - y * 3, y * 3, 6) : 0); }, SAND, { ambient: 0.16, thr: 0.04, tex: (x, y) => (hash(x >> 1, y) < 0.1 ? 0.1 : 0) });

  // ---- 胸の裂け目（紫の光と、骨の肋） ----
  const rift = [[118, 128], [132, 122], [140, 142], [134, 172], [122, 190], [114, 166], [112, 146]];
  for (let y = 120; y <= 192; y++) for (let x = 108; x <= 146; x++) if (inPoly(rift, x + 0.5, y + 0.5)) { const d = Math.hypot((x - 126) / 14, (y - 158) / 34); put(g, y, x, d < 0.28 ? VIO[3] : d < 0.55 ? VIO[2] : d < 0.8 ? VIO[1] : VIO[0]); }
  for (let y = 136; y <= 178; y += 8) { limb(g, bezier([114 + (y % 16 ? 0 : 1), y - 2], [126, y + 4], [140, y - 2], 10), 2.4, 2.4, BONE, { ambient: 0.35 }); }
  // 裂け目の縁は暗い布で締める
  for (let y = 116; y <= 196; y++) for (let x = 102; x <= 152; x++) { if (g[y][x] < 0) continue; if (VIO.includes(g[y][x]) || BONE.includes(g[y][x])) continue; if ([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1]].some(([a, b]) => VIO.includes(g[y + a]?.[x + b]))) put(g, y, x, CLOTH[x < 124 ? 1 : 0]); }

  // ---- 外套の肩・フード ----
  slab(g, [[84, 66], [104, 40], [128, 34], [154, 40], [174, 66], [186, 108], [176, 128], [168, 144], [154, 130], [148, 152], [134, 132], [124, 148], [112, 130], [100, 146], [92, 128], [76, 138], [72, 106]], CLOTH, { bias: -0.3, seam: (x, y) => (x + y * 2) % 21 === 0 || (x * 2 - y + 700) % 17 === 0 });
  // ぼろの裾（フードのふち）: 布の細片

  // ---- 仮面（浮かぶ。まわりは空洞） ----
  const MASK = [[102, 52], [154, 52], [160, 82], [146, 114], [128, 128], [110, 114], [96, 82]];
  // 仮面の後ろの闇（空洞）
  for (let y = 44; y <= 136; y++) for (let x = 88; x <= 168; x++) if (inPoly([[100, 46], [156, 46], [168, 82], [150, 120], [128, 136], [106, 120], [88, 82]], x + 0.5, y + 0.5)) put(g, y, x, y < 60 ? SHD : OUT);
  slab(g, MASK, BONE, { bias: 0.5 });
  // 眉の板と頬のひび
  slab(g, [[104, 58], [152, 58], [150, 66], [106, 66]], BONE, { bias: -0.3 });
  // 目の穴（つり上がる）と紫の光
  const hole = (pts) => { for (let y = 60; y <= 100; y++) for (let x = 96; x <= 160; x++) if (inPoly(pts, x + 0.5, y + 0.5)) put(g, y, x, OUT); };
  hole([[106, 74], [126, 80], [124, 92], [110, 88]]); hole([[130, 80], [150, 74], [146, 88], [132, 92]]);
  const glow = (pts, y0, y1) => { for (let y = y0; y <= y1; y++) for (let x = 100; x <= 156; x++) if (inPoly(pts, x + 0.5, y + 0.5)) put(g, y, x, VIO[y - y0 < (y1 - y0) * 0.4 ? 3 : y - y0 < (y1 - y0) * 0.75 ? 2 : 1]); };
  glow([[110, 77], [123, 81], [122, 88], [112, 85]], 77, 88); glow([[133, 81], [146, 77], [144, 85], [134, 88]], 77, 88);
  // 口: 縦の裂け目
  for (let y = 100; y <= 118; y++) { put(g, y, 127, OUT); put(g, y, 128, OUT); if (y % 4 === 0) { put(g, y, 126, OUT); put(g, y, 129, OUT); } }
  // 鼻の稜線
  for (let y = 84; y <= 98; y++) put(g, y, 128 - (y > 90 ? 0 : 0), BONE[y % 2 ? 1 : 0]);
  // ひび
  for (let i = 0; i < 22; i++) { const x = 146 - Math.round(i * 0.4) - (i % 3 === 0 ? 1 : 0), y = 60 + i; if (g[y]?.[x] >= 0 && BONE.includes(g[y][x])) put(g, y, x, BONE[0]); }
  // 額の角（砂を切る）
  slab(g, [[104, 52], [108, 30], [116, 52]], BONE, { bias: -0.2 }); slab(g, [[140, 52], [148, 26], [152, 52]], BONE, { bias: -0.5 });

  // ---- 腕（布に包まれた腕と骨の手） ----
  limb(g, bezier([82, 118], [40, 140], [34, 102], 20), 11, 6, CLOTH, { ambient: 0.22 });
  limb(g, bezier([176, 120], [222, 128], [224, 138], 20), 11, 6, CLOTH, { ambient: 0.22 });
  ellipsoid(g, 30, 98, 8, 7, BONE, { ambient: 0.3 }); ellipsoid(g, 226, 134, 8, 7, BONE, { ambient: 0.3 });
  for (const [hx, hy, dirs] of [[30, 98, [[-10, -12], [-16, -4], [-16, 6], [-8, 14]]], [[226], 134, [[10, -8], [17, 0], [16, 10], [8, 17]]]].map((a) => [Array.isArray(a[0]) ? a[0][0] : a[0], a[1], a[2]])) for (const [dx, dy] of dirs) limb(g, bezier([hx, hy], [hx + dx * 0.5 + 1, hy + dy * 0.5 - 1], [hx + dx, hy + dy], 6), 2.6, 1.2, BONE, { ambient: 0.35 });

  // ---- 前で回る瓦礫（大きめ）と砂の軌跡 ----
  const orbit = (rx, ry, y0, a0, a1, kk) => { for (let a = a0; a < a1; a += 0.01) { const x = cx + Math.cos(a) * rx, y = y0 + Math.sin(a) * ry; if (g[Math.round(y)]?.[Math.round(x)] < 0 || g[Math.round(y)]?.[Math.round(x)] === undefined) { put(g, y, x, kk[0]); put(g, y + 1, x, kk[1]); } } };
  rock([[184, 176], [206, 168], [222, 184], [210, 204], [188, 200]], 0);
  rock([[42, 196], [62, 186], [76, 200], [64, 216], [46, 214]], -0.2);
  rock([[194, 60], [206, 52], [214, 64], [204, 74]], 0.2);
  slab(g, [[30, 214], [70, 200], [76, 212], [36, 228]], ROCK, { bias: 0.2, seam: (x, y) => (x + y) % 9 === 0 });
  // 瓦礫のひび
  for (const [sx, sy] of [[192, 180], [50, 192]]) for (let i = 0; i < 10; i++) { const x = sx + Math.round(i * 0.6), y = sy + i; if (ROCK.includes(g[y]?.[x])) put(g, y, x, ROCK[0]); }

  despeckle(g);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M4-砂嵐の歪み", g)]; })();
