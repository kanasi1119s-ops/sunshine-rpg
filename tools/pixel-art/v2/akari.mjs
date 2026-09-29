// 灯里の歪み（序章のボス・v2）: 歪んだ灯り石に呑まれた、巨大な古い角灯。割れたガラスの内側で、暗い炎が目を開く。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, eye, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0b0814"), RIM = pal.rgb("縁明", "#2a2340"), SHD = pal.rgb("影", "#15101f");
  const IRON = pal.ramp("鉄", 235, 0.16, 5, 0.1, 0.62);
  const GLASS = pal.ramp("ガラス", 32, 0.45, 4, 0.16, 0.5);
  const VIO = pal.ramp("歪み", 278, 0.5, 4, 0.14, 0.62);
  const FIRE = pal.ramp("炎", 38, 0.9, 4, 0.34, 0.86);
  const EYE = pal.ramp("目", 345, 0.8, 3, 0.3, 0.66);
  const CHAIN = pal.ramp("鎖", 240, 0.1, 3, 0.16, 0.5);
  const g = makeGrid();
  const cx = 128;
  groundShadow(g, cx, 243, 84, 9, SHD);
  // 下がる鎖と黒い根（本体の後ろ）
  for (const [x1, y1, bend] of [[52, 246, -34], [92, 250, -10], [164, 250, 10], [204, 246, 34], [128, 252, 0]]) limb(g, bezier([cx + (x1 - cx) * 0.35, 200], [x1 + bend, 226], [x1, y1]), 8, 3, VIO, { ambient: 0.2 });
  // 角灯の本体（六角のガラス）
  const body = heightField([{ cx, cy: 128, rx: 66, ry: 74, h: 1 }, { cx, cy: 118, rx: 50, ry: 62, h: 0.9 }], 5);
  const cell = (x, y) => { const u = (x - cx) / 66; return Math.abs(((u * 3) % 1 + 1) % 1 - 0.5); };
  paintField(g, body, GLASS, { ambient: 0.32, tex: (x, y, lum) => (cell(x, y) > 0.46 ? -0.4 : 0) + (hash(x >> 2, y >> 2) < 0.05 ? -0.12 : 0) });
  // 縦の鉄枠（縦に3本、六角の稜）
  for (const dx of [-42, 0, 42]) for (let y = 62; y <= 196; y++) {
    const u = dx / 66, half = Math.sqrt(Math.max(0, 1 - u * u)) * 74; if (Math.abs(y - 128) > half * 0.98) continue;
    for (let t = -2; t <= 2; t++) put(g, y, cx + dx + t, IRON[t < -0 ? 3 : t === 0 ? 2 : 1]);
  }
  // 内側で燃える暗い炎（炎の核、紫のふちどり）
  paintField(g, heightField([{ cx, cy: 132, rx: 34, ry: 46, h: 1 }, { cx: cx + 4, cy: 112, rx: 20, ry: 34 }], 6), FIRE, { ambient: 0.5, gain: 0.8, tex: (x, y) => Math.sin((x + y * 0.4) * 0.35) * 0.09 });
  for (let y = 70; y < 190; y++) for (let x = 84; x < 172; x++) { const n = ((x - cx) / 40) ** 2 + ((y - 132) / 54) ** 2; if (n > 0.86 && n < 1.08 && g[y][x] >= 0 && FIRE.includes(g[y][x])) put(g, y, x, VIO[n > 1 ? 1 : 2]); }
  // 大きな一つ目
  eye(g, cx, 128, 20, 17, EYE, OUT, 0);
  // 上の飾りと吊り輪
  paintField(g, heightField([{ cx, cy: 62, rx: 58, ry: 16, h: 1 }, { cx, cy: 44, rx: 30, ry: 18, h: 1 }], 5), IRON, { ambient: 0.3 });
  ellipsoid(g, cx, 26, 15, 15, IRON, { ambient: 0.25 });
  for (let a = 0; a < 6.283; a += 0.02) for (const rr of [8, 9]) { const x = cx + Math.cos(a) * rr, y = 26 + Math.sin(a) * rr; put(g, y, x, OUT); }
  // 底の受け皿
  paintField(g, heightField([{ cx, cy: 204, rx: 62, ry: 15, h: 1 }, { cx, cy: 214, rx: 36, ry: 13, h: 1 }], 5), IRON, { ambient: 0.28 });
  // ひび割れ（紫の光が漏れる）
  let x = 86, y = 82; for (let i = 0; i < 46; i++) { x += hash(i, 3) < 0.5 ? 1 : 0; y += 1 + (hash(i, 9) < 0.35 ? 1 : 0); if (g[y]?.[x] >= 0 && GLASS.includes(g[y][x])) { put(g, y, x, VIO[3]); put(g, y, x - 1, VIO[1]); } }
  x = 176; y = 150; for (let i = 0; i < 36; i++) { x -= hash(i, 5) < 0.5 ? 1 : 0; y += 1; if (g[y]?.[x] >= 0 && GLASS.includes(g[y][x])) { put(g, y, x, VIO[3]); put(g, y, x + 1, VIO[1]); } }
  // 割れて浮かぶガラス片
  for (const [sx, sy, w, h] of [[36, 90, 8, 18], [220, 82, 7, 16], [26, 160, 6, 12], [232, 150, 8, 15], [66, 30, 5, 10]]) {
    for (let r = -h; r <= h; r++) for (let c = -w; c <= w; c++) { const d = Math.abs(c) / w + Math.abs(r) / h; if (d > 1) continue; put(g, sy + r, sx + c, d > 0.8 ? GLASS[0] : c < 0 && r < 0 ? GLASS[3] : c < 0 ? GLASS[2] : GLASS[1]); }
  }
  despeckle(g);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M0-灯里の歪み", g)]; })();
