// 灯り草（序章〜第1章のザコ・v2）: 先端が灯りのように光る草の魔物。根を足のように張り、花のような口で獲物を待つ。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, eye, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#08120f"), RIM = pal.rgb("縁明", "#1f4a3e"), SHD = pal.rgb("影", "#0f1a17");
  const LEAF = pal.ramp("葉", 160, 0.34, 5, 0.06, 0.42, 34);
  const PET = pal.ramp("花びら", 325, 0.46, 4, 0.1, 0.44, 34);
  const ROOT = pal.ramp("根", 28, 0.32, 4, 0.1, 0.42, 24);
  const GLOW = [pal.rgb("灯暗", "#9a3f12"), pal.rgb("灯橙", "#f08a20"), pal.rgb("灯黄", "#ffd44a"), pal.rgb("灯芯", "#fff6c0")];
  const MOUTH = [pal.rgb("口", "#3a0a1c"), pal.rgb("舌", "#a01e3c"), pal.rgb("舌明", "#e04a5a")];
  const TOOTH = [pal.rgb("歯影", "#9d9484"), pal.rgb("歯", "#efe6c8")];
  const g = makeGrid();
  const cx = 128, GY = 224;
  groundShadow(g, cx + 4, GY + 3, 56, 7, SHD);

  // 葉（ふくらんだ細長い形）
  const leaf = (pts, rmax, ramp, opts = {}) => {
    const n = pts.length, parts = pts.map(([x, y], i) => { const t = i / (n - 1); return { cx: x, cy: y, rx: Math.max(1.5, rmax * Math.sin(Math.PI * (0.12 + 0.88 * t)) ** 0.8), ry: Math.max(1.5, rmax * Math.sin(Math.PI * (0.12 + 0.88 * t)) ** 0.8) * 0.8 }; });
    paintField(g, heightField(parts, 5), ramp, { ambient: 0.22, ...opts });
    // 中央の葉脈（影の色）
    for (let i = 1; i < n - 2; i++) { const [x, y] = pts[i]; if (g[Math.round(y)]?.[Math.round(x)] >= 0) put(g, y + 1, x, ramp[0]); }
  };

  // 根の足（本体の後ろ側から、ひざを曲げて地面へ）
  const rootLeg = (x0, y0, kx, ky, fx, w) => {
    limb(g, bezier([x0, y0], [kx, ky], [fx, GY - 3], 20), w, w * 0.55, ROOT, { ambient: 0.2 });
    for (const dx of [-9, -2, 6]) limb(g, bezier([fx, GY - 5], [fx + dx * 0.6, GY - 1], [fx + dx, GY + 1], 6), 3.4, 1.4, ROOT, { ambient: 0.2 }); // 根の先の爪
  };
  rootLeg(118, 198, 84, 200, 72, 8);
  rootLeg(138, 198, 176, 200, 186, 8);
  rootLeg(122, 202, 100, 218, 104, 7);
  rootLeg(134, 202, 158, 218, 152, 7);

  // 灯りの触手（先に光る玉）。花びらの後ろから伸びる
  const lures = [
    { pts: bezier([128, 104], [96, 96], [92, 70], 26), r: 10, tip: [92, 70] },
    { pts: bezier([100, 148], [56, 142], [48, 116], 20), r: 6, tip: [48, 116] },
    { pts: bezier([156, 148], [200, 138], [206, 112], 20), r: 6, tip: [206, 112] },
  ];
  for (const l of lures) limb(g, l.pts, 4.5, 2.6, LEAF, { ambient: 0.2 });

  // 球根の胴と茎
  paintField(g, heightField([{ cx, cy: 184, rx: 30, ry: 26, h: 1 }, { cx, cy: 156, rx: 15, ry: 34, h: 0.9 }], 5), LEAF, { ambient: 0.22, tex: (x, y) => (hash(x >> 2, y >> 2) < 0.14 ? -0.07 : 0) + (Math.sin((x - cx) * 0.55) * 0.05) });
  // 球根のすじ（縦のくぼみ）
  for (const dx of [-13, 0, 13]) for (let y = 172; y < 206; y++) { const x = cx + dx + Math.round(Math.sin((y - 170) * 0.09) * 2); if (g[y][x] >= 0 && LEAF.includes(g[y][x])) put(g, y, x + 1, LEAF[Math.max(0, LEAF.indexOf(g[y][x]) - 1)]); }
  // 大きな葉（左右に垂れる）
  leaf(bezier([120, 172], [78, 150], [56, 176], 16), 13, LEAF);
  leaf(bezier([136, 170], [180, 146], [204, 174], 16), 13, LEAF);

  // 花びら（外側は暗い紫、口のまわりで明るく）
  const CY = 132;
  const petals = [[-176, 8], [-158, 14], [-138, 6], [-118, 2], [-99, 8], [-81, 8], [-62, 2], [-42, 6], [-22, 14], [-4, 8], [24, 14], [156, 14]];
  for (const [deg, len] of petals) {
    const a = deg * Math.PI / 180, L = 44 + len * 0.5, pts = [];
    for (let i = 0; i <= 8; i++) { const t = i / 8, rr = 14 + (L - 14) * t; pts.push([cx + Math.cos(a) * rr, CY + Math.sin(a) * rr * 0.9 + (deg > 0 ? t * t * 12 : 0)]); }
    limb(g, pts, 5, 9.5, PET, { ambient: 0.16 });
  }
  // がく（花の中心の土台）
  ellipsoid(g, cx, CY + 2, 30, 27, LEAF, { ambient: 0.25 });

  // 口（口の中は暗い赤、舌、上下の歯）
  const MY = CY + 8, mrx = 22, mry = 15;
  for (let y = MY - mry; y <= MY + mry; y++) for (let x = cx - mrx; x <= cx + mrx; x++) {
    const d = ((x - cx) / mrx) ** 2 + ((y - MY) / mry) ** 2; if (d >= 1) continue;
    put(g, y, x, d > 0.82 ? MOUTH[0] : (x - cx) ** 2 / 90 + (y - MY - 5) ** 2 / 26 < 1 ? (x - cx < -4 ? MOUTH[2] : MOUTH[1]) : MOUTH[0]);
  }
  for (let x = cx - mrx + 3; x <= cx + mrx - 3; x++) {
    const d = ((x - cx) / mrx) ** 2, top = MY - Math.sqrt(Math.max(0, 1 - d)) * mry, bot = MY + Math.sqrt(Math.max(0, 1 - d)) * mry, ph = (x - cx + 100) % 6;
    const tl = 6 - Math.abs(ph - 2.5) * 2.2; // 山型の歯
    for (let i = 0; i < tl; i++) { put(g, top + 1 + i, x, ph < 3 ? TOOTH[1] : TOOTH[0]); }
    const tl2 = 4 - Math.abs(((x - cx + 103) % 7) - 3) * 1.4;
    for (let i = 0; i < tl2; i++) put(g, bot - 1 - i, x, ((x - cx + 103) % 7) < 3 ? TOOTH[1] : TOOTH[0]);
  }
  // 目（がくの上に、小さく光る）
  eye(g, cx - 14, CY - 12, 4, 5, [GLOW[1], GLOW[2], GLOW[3]], MOUTH[0], 0.2);
  eye(g, cx + 14, CY - 12, 4, 5, [GLOW[1], GLOW[2], GLOW[3]], MOUTH[0], -0.2);

  // 灯り玉（暗い橙のふち→黄→白い芯）。光は左上
  for (const l of lures) {
    const [tx, ty] = l.tip, r = l.r;
    for (let y = -r - 1; y <= r + 1; y++) for (let x = -r - 1; x <= r + 1; x++) {
      const d = Math.hypot(x, y) / r; if (d > 1) continue;
      const dd = Math.hypot(x + r * 0.28, y + r * 0.3) / r; // 芯は少し左上寄り
      put(g, ty + y, tx + x, dd < 0.34 ? GLOW[3] : dd < 0.68 ? GLOW[2] : d < 0.85 ? GLOW[1] : GLOW[0]);
    }
    // 玉の根もとの萼（受け皿）
    for (let x = -Math.round(r * 0.5); x <= Math.round(r * 0.5); x++) put(g, ty + r + 1 + 1, tx + x + 4, LEAF[2]);
  }

  despeckle(g, 3);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "E1-灯り草", g)]; })();
