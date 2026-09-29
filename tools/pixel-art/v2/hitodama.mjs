// 火照ノ一（序章〜第1章のザコ・v2）: 灯り石の火が化けた、揺らめく炎の霊。暗い煤をまとい、芯だけが黄色く燃える。
import { createPalette, makeGrid, heightField, outline, despeckle, groundShadow, eye, hash, put, clamp, smoothstep, W, toPieceFile } from "./lib2.mjs";

const cubic = (p0, p1, p2, p3, t) => { const u = 1 - t; return [u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0], u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]]; };
// 値ノイズ（なめらかな塊）
const vnoise = (x, y, s) => { const gx = x / s, gy = y / s, x0 = Math.floor(gx), y0 = Math.floor(gy), fx = gx - x0, fy = gy - y0, sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy); const a = hash(x0, y0), b = hash(x0 + 1, y0), c = hash(x0, y0 + 1), d = hash(x0 + 1, y0 + 1); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy; };

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#120810"), RIM = pal.rgb("縁明", "#4a1a26"), SHD = pal.rgb("影", "#1a0f1c");
  const SOOT = pal.ramp("煤", 305, 0.26, 4, 0.08, 0.28, 30);
  const FIRE = pal.ramp("炎", 16, 0.9, 6, 0.2, 0.84, 30);
  const EYE = pal.ramp("目", 188, 0.8, 3, 0.45, 0.86, 10);
  const g = makeGrid();
  const cx = 128;

  // ---- 炎の形（高さ場）: 曲がった背骨に沿って太さを変える ----
  const parts = [];
  const spine = (p0, p1, p2, p3, R, n, bottomRound = 0.5) => {
    for (let i = 0; i <= n; i++) {
      const t = i / n, [x, y] = cubic(p0, p1, p2, p3, t);
      const r = R * Math.pow(Math.max(0, 1 - Math.pow(t, 1.35)), 0.85) * (bottomRound + (1 - bottomRound) * smoothstep(0, 0.22, t));
      if (r > 1.2) parts.push({ cx: x, cy: y, rx: r, ry: r * 1.05, h: 1 });
    }
  };
  spine([128, 200], [150, 165], [104, 130], [116, 84], 47, 40);      // 主たる炎（先が左へ曲がる）
  spine([92, 196], [70, 176], [72, 150], [64, 124], 17, 18, 0.7);    // 左の小さな舌
  spine([166, 198], [188, 180], [184, 156], [194, 130], 19, 18, 0.7); // 右の舌
  spine([128, 214], [118, 222], [136, 226], [150, 214], 14, 10, 0.9);  // 足もとのゆらぎ
  const hf = heightField(parts, 7);
  let hmax = 0; for (let y = 60; y < 240; y++) for (let x = 40; x < 220; x++) hmax = Math.max(hmax, hf(x, y));

  groundShadow(g, cx + 2, 232, 46, 6, SHD);

  // ---- 塗り（自分で光る炎なので、縁が暗く芯が明るい。光は左上からわずかに） ----
  for (let y = 60; y < 240; y++) for (let x = 40; x < 220; x++) {
    const h = hf(x, y); if (h < 0.05) continue;
    let v = h / hmax;
    // 揺らぎの帯（左上から右下へ流れる）
    v += Math.sin(y * 0.19 + x * 0.07) * 0.045 + (vnoise(x, y, 7) - 0.5) * 0.09;
    // 左上が少し明るく、右下は煤で暗い
    v += (-(x - cx) * 0.0011 - (y - 150) * 0.0009);
    // 上へ行くほど煤けて暗くなる（炎の先は黒ずむ）
    v -= smoothstep(150, 90, y) * 0.16;
    // 芯を下寄りに（炎の根もとが最も熱い）
    v += smoothstep(120, 200, y) * 0.07;
    let k;
    const soot = vnoise(x + 31, y + 7, 11);
    if (v < 0.13) k = SOOT[v < 0.05 ? 0 : v < 0.09 ? 1 : 2];
    else if (v < 0.3) k = soot > 0.62 && v < 0.24 ? SOOT[3] : FIRE[0];
    else if (v < 0.5) k = FIRE[1];
    else if (v < 0.66) k = FIRE[2];
    else if (v < 0.8) k = FIRE[3];
    else if (v < 0.92) k = FIRE[4];
    else k = FIRE[5];
    // 大きな煤のよごれ（右下の外炎に重なる）
    if (v < 0.58 && soot > 0.7 && x > cx - 10) k = v < 0.4 ? SOOT[1] : FIRE[0];
    put(g, y, x, k);
  }

  // ---- 顔: 煤の仮面と、小さな青白い目 ----
  for (let y = 146; y <= 190; y++) for (let x = 78; x <= 180; x++) {
    if (g[y][x] < 0) continue;
    const nx = (x - 129) / 43, ny = (y - 168 + Math.abs(x - 129) * 0.16 * -1 + (x < 129 ? 0 : 0)) / 15;
    const d = nx * nx + ny * ny;
    if (d < 1) g[y][x] = d < 0.6 ? SOOT[0] : d < 0.85 ? SOOT[1] : SOOT[2];
  }
  eye(g, 112, 168, 6, 8, EYE, SOOT[0], 0.16);
  eye(g, 146, 166, 6, 8, EYE, SOOT[0], -0.16);
  // 怒った眉（暗い煤の斜め線）
  for (let i = 0; i < 16; i++) { put(g, 150 - Math.round(i * 0.55), 104 + i, SOOT[0]); put(g, 151 - Math.round(i * 0.55), 104 + i, SOOT[1]); put(g, 145 + Math.round(i * 0.55) , 146 + i, SOOT[0]); put(g, 146 + Math.round(i * 0.55), 146 + i, SOOT[1]); }
  // 小さな口（熱い裂け目）
  for (let x = 118; x <= 140; x++) { const y = 186 + Math.round(Math.abs(x - 129) * 0.22); if (g[y][x] >= 0) { put(g, y, x, FIRE[5]); put(g, y - 1, x, SOOT[0]); } }

  // ---- 舞い上がる火の粉（2〜3ドットのかたまり。孤立させない） ----
  for (const [sx, sy, s] of [[70, 100, 2], [152, 76, 2], [200, 104, 3]]) for (let r = 0; r < s; r++) for (let c = 0; c < s; c++) put(g, sy + r, sx + c, r + c === 0 ? FIRE[5] : FIRE[3]);

  despeckle(g, 3);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "E0-火照ノ一", g)]; })();
