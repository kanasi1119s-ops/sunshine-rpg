// C4-ガイド（第2章加入・風唱系）: 硝子湖の交易商人の息子。早口で損得に敏い、軽やかな若者。
// 風にあおられた砂色の髪、青緑のマフラー、クリーム色のベスト、腰の財布。右手で金貨をはじく。
// 頭は会話の顔として (x90〜166, y8〜98) が切り出されるので、その範囲に顔を大きく収める。
import { createPalette, makeGrid, heightField, paintField, outline, despeckle, groundShadow, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

// ---- この絵だけで使う部品 ----
const pip = (poly, x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
/** 高さ場を別の紙に塗り、マスクの内側だけ写す（服の一部だけ塗る・はみ出しを切るため） */
function vol(g, parts, ramp, { box, mask = null, k = 5, ...opts }) {
  const t = makeGrid(); paintField(t, heightField(parts, k), ramp, { ...opts, box });
  for (let y = Math.max(0, box[1]); y < Math.min(W, box[3]); y++) for (let x = Math.max(0, box[0]); x < Math.min(W, box[2]); x++) if (t[y][x] >= 0 && (!mask || mask(x, y))) g[y][x] = t[y][x];
}
/** 太さが変わる折れ線の管。pts=[[x,y,r]...] */
function tube(g, pts, ramp, opts = {}) {
  const parts = []; let last = null;
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0, r0] = pts[i], [x1, y1, r1] = pts[i + 1], n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0)));
    for (let s = 0; s <= n; s++) { const t = s / n, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t, r = r0 + (r1 - r0) * t; if (last && Math.hypot(x - last[0], y - last[1]) < Math.max(0.8, r * 0.3)) continue; parts.push({ cx: x, cy: y, rx: r, ry: r }); last = [x, y]; }
  }
  const m = Math.max(...pts.map((p) => p[2])) + 3;
  const box = [Math.floor(Math.min(...pts.map((p) => p[0])) - m), Math.floor(Math.min(...pts.map((p) => p[1])) - m), Math.ceil(Math.max(...pts.map((p) => p[0])) + m), Math.ceil(Math.max(...pts.map((p) => p[1])) + m)];
  vol(g, parts, ramp, { ...opts, box });
}
const ell = (g, cx, cy, rx, ry, ramp, opts = {}) => vol(g, [{ cx, cy, rx, ry }], ramp, { ...opts, box: [Math.floor(cx - rx) - 2, Math.floor(cy - ry) - 2, Math.ceil(cx + rx) + 3, Math.ceil(cy + ry) + 3] });
function line(g, x0, y0, x1, y1, k) { const n = Math.ceil(Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0))); for (let i = 0; i <= n; i++) { const t = n ? i / n : 0; put(g, y0 + (y1 - y0) * t, x0 + (x1 - x0) * t, k); } }
function fillPoly(g, pts, fn) {
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  for (let y = Math.floor(Math.min(...ys)); y <= Math.ceil(Math.max(...ys)); y++) for (let x = Math.floor(Math.min(...xs)); x <= Math.ceil(Math.max(...xs)); x++) if (pip(pts, x + 0.5, y + 0.5)) { const k = fn(x, y); if (k !== null && k !== undefined) put(g, y, x, k); }
}
/** 目。まぶたの線・虹彩・白目・ハイライト。side: -1 左目 / +1 右目 */
function eyeF(g, cx, cy, w, h, C, side) {
  for (let y = -h; y <= h; y++) {
    const hw = Math.round(w * Math.sqrt(Math.max(0, 1 - (y / (h + 0.6)) ** 2)));
    for (let x = -hw; x <= hw; x++) {
      const ix = (x - side * 0.6) / (w * 0.62), iy = y / (h + 0.3);
      let k = C.white;
      if (ix * ix + iy * iy <= 1) k = y < -h * 0.25 ? C.irisDk : C.iris;
      if (Math.abs(x - side * 0.6) <= 1 && y >= -Math.floor(h * 0.4) && y <= Math.floor(h * 0.55)) k = C.dark;
      put(g, cy + y, cx + x, k);
    }
  }
  // 上まぶた（太い暗線。外側の端がすこし下がる）
  for (let x = -w - 1; x <= w + 1; x++) { const up = Math.round(Math.abs(x) / w * 1.2 * (Math.sign(x) === side ? 1 : 0.5)); put(g, cy - h - 1 + up, cx + x, C.dark); if (Math.abs(x) < w) put(g, cy - h + up, cx + x, C.dark); }
  put(g, cy - h + 2, cx - 2 + (side > 0 ? 0 : -0), C.hi); put(g, cy - h + 2, cx - 1, C.hi); put(g, cy - h + 3, cx - 2, C.hi);
}

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0e0a16"), RIM = pal.rgb("縁明", "#3b2c40");
  const SKIN = pal.ramp("肌", 24, 0.5, 4, 0.36, 0.8, 22);
  const HAIR = pal.ramp("髪", 36, 0.62, 4, 0.15, 0.68, 30);
  const TEAL = pal.ramp("マフラー", 176, 0.72, 3, 0.26, 0.55, 18);
  const VEST = pal.ramp("ベスト", 46, 0.4, 3, 0.4, 0.84, 22);
  const TUN = pal.ramp("上衣", 226, 0.42, 3, 0.2, 0.46, 22);
  const BRN = pal.ramp("革", 22, 0.42, 4, 0.14, 0.44, 24);
  const GOLD = pal.rgb("金", "#f6c945");
  const WHITE = pal.rgb("白", "#f7f3ee");
  const EYEIR = TEAL[1], EYEDK = TEAL[0];
  const C = { dark: OUT, iris: EYEIR, irisDk: EYEDK, white: WHITE, hi: WHITE };
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 246, 52, 6, BRN[0]);

  // ---------- 足・靴 ----------
  tube(g, [[116, 162, 12], [114, 205, 10], [113, 232, 8.5]], BRN, { ambient: 0.28, gain: 1.0 });      // ズボン（革色より明るく見えるよう別に塗る）
  tube(g, [[141, 162, 12], [143, 205, 10], [144, 232, 8.5]], BRN, { ambient: 0.28, gain: 1.0 });
  // ズボンを一段明るい砂色に（革のランプの上側を使う）
  for (let y = 165; y < 226; y++) for (let x = 96; x < 162; x++) { const k = g[y][x]; const i = BRN.indexOf(k); if (i >= 0) g[y][x] = BRN[clamp(i + 1, 0, 3)]; }
  // ブーツ
  ell(g, 111, 240, 14, 8.5, BRN, { ambient: 0.18 }); ell(g, 148, 240, 14, 8.5, BRN, { ambient: 0.18 });
  for (const bx of [113, 143]) { for (let x = -9; x <= 9; x++) { put(g, 228, bx + x, BRN[3]); put(g, 229, bx + x, BRN[2]); put(g, 230, bx + x, BRN[0]); } }

  // ---------- マフラーの流れる先（左うしろへ） ----------
  tube(g, [[108, 100, 7], [88, 106, 7.5], [66, 114, 7], [50, 128, 6], [44, 144, 4], [40, 152, 2]], TEAL, { ambient: 0.3, gain: 0.7 });
  tube(g, [[104, 106, 6], [84, 116, 6], [70, 128, 5], [66, 142, 3.5]], TEAL, { ambient: 0.18, gain: 0.7 });

  // ---------- 首・胴 ----------
  tube(g, [[128, 84, 9], [128, 102, 10]], SKIN, { ambient: 0.16, gain: 1.0 });
  const torso = [{ cx, cy: 130, rx: 26, ry: 32 }, { cx, cy: 110, rx: 32, ry: 14 }, { cx, cy: 150, rx: 23, ry: 16 }];
  const tbox = [90, 92, 168, 176];
  vol(g, torso, TUN, { box: tbox, ambient: 0.12, gain: 1.2 });
  // ベスト（前が開いて、上衣が見える）
  const open = (x, y) => Math.abs(x - cx) < Math.min(9, (y - 104) * 0.32 + 1);
  vol(g, torso, VEST, { box: tbox, mask: (x, y) => !open(x, y) && y > 100, ambient: 0.14, gain: 1.3, tex: (x, y) => (Math.abs(x - cx) < 3 ? -0.05 : 0) });
  // ベストの縁の影（前の合わせ目）
  for (let y = 106; y < 150; y++) { const w = Math.min(9, (y - 104) * 0.32 + 1); put(g, y, Math.round(cx - w), VEST[0]); put(g, y, Math.round(cx + w), VEST[0]); put(g, y, Math.round(cx - w) - 1, VEST[1]); }
  // 上衣のひも
  for (let y = 112; y < 148; y += 5) { put(g, y, cx - 1, TUN[2]); put(g, y, cx + 1, TUN[2]); put(g, y + 1, cx, TUN[0]); }
  // ベルト
  for (let y = 150; y < 158; y++) for (let x = 100; x <= 156; x++) { const half = 24 + (y - 150) * 0.6; if (Math.abs(x - cx) > half) continue; put(g, y, x, y === 150 ? BRN[3] : y < 153 ? BRN[2] : y < 156 ? BRN[1] : BRN[0]); }
  for (let y = 149; y <= 158; y++) for (let x = cx - 5; x <= cx + 5; x++) put(g, y, x, y === 149 || x === cx - 5 ? WHITE : y >= 157 || x === cx + 5 ? BRN[0] : GOLD);
  for (let y = 152; y <= 155; y++) for (let x = cx - 2; x <= cx + 2; x++) put(g, y, x, BRN[1]);
  // ベストのポケットと、ズボンのしわ
  line(g, 108, 134, 118, 134, VEST[0]); line(g, 108, 134, 108, 141, VEST[0]); line(g, 109, 142, 117, 142, VEST[1]);
  for (const [x0, y0] of [[112, 186], [143, 190], [113, 208], [144, 212]]) { line(g, x0, y0, x0 + 6, y0 + 2, BRN[0]); line(g, x0 + 1, y0 - 1, x0 + 5, y0, BRN[3]); }
  // 財布（右の腰、ひもで口をしばる）
  ell(g, 147, 166, 9, 10, BRN, { ambient: 0.22, gain: 1.1 });
  for (let x = 141; x <= 153; x++) { put(g, 158, x, BRN[3]); put(g, 159, x, BRN[0]); }
  put(g, 172, 144, GOLD); put(g, 172, 145, GOLD); put(g, 171, 144, WHITE);

  // ---------- 左手は腰に（ひじが外へ）----------
  tube(g, [[99, 106, 9.5], [86, 128, 8.5], [88, 145, 7.5]], TUN, { ambient: 0.14, gain: 1.2 });
  tube(g, [[88, 145, 7.5], [98, 155, 6.5]], TUN, { ambient: 0.2, gain: 0.9 });
  line(g, 84, 130, 92, 136, TUN[0]); line(g, 83, 133, 90, 138, TUN[0]);
  ell(g, 105, 156, 5.5, 5, SKIN, { ambient: 0.2 });
  for (let x = 95; x <= 100; x++) { put(g, 150, x, VEST[1]); }
  // ---------- 右手は金貨をはじく ----------
  tube(g, [[157, 106, 9.5], [168, 128, 8.5], [172, 136, 7.5]], TUN, { ambient: 0.14, gain: 1.2 });
  tube(g, [[172, 136, 7.5], [180, 122, 6.3]], TUN, { ambient: 0.14, gain: 1.2 });
  line(g, 166, 130, 173, 128, TUN[0]); line(g, 168, 134, 175, 131, TUN[0]);
  ell(g, 182, 116, 6, 6.5, SKIN, { ambient: 0.2 });
  for (let x = -1; x <= 3; x++) put(g, 112, 179 + x, SKIN[0]);
  // 金貨
  for (let y = -6; y <= 6; y++) for (let x = -6; x <= 6; x++) { const d = Math.hypot(x, y * 1.0); if (d > 6) continue; put(g, 101 + y, 186 + x, d > 4.6 ? BRN[1] : (x + y < -2 ? WHITE : (x + y > 3 ? BRN[3] : GOLD))); }
  for (let y = -2; y <= 2; y++) put(g, 101 + y, 186 + 1, BRN[2]);
  // 金貨のきらめき
  for (const [dx, dy] of [[0, -10], [0, -9], [0, -11], [-1, -10], [1, -10]]) put(g, 101 + dy, 186 + dx, WHITE);

  // ---------- 首のマフラー（わ） ----------
  tube(g, [[108, 98, 7], [118, 106, 8.5], [128, 108, 9], [138, 106, 8.5], [148, 98, 7]], TEAL, { ambient: 0.28, gain: 0.8 });
  // 結び目
  ell(g, 112, 104, 8, 7.5, TEAL, { ambient: 0.3, gain: 0.9 });
  for (let i = 0; i < 6; i++) { put(g, 100 + i, 120 - i * 2 - 2, TEAL[0]); }
  // 首かざりのひも（笛）
  line(g, 122, 110, 128, 128, BRN[0]); line(g, 134, 110, 128, 128, BRN[0]);
  ell(g, 128, 132, 3.6, 5, [GOLD, GOLD, WHITE], { ambient: 0.4 });
  put(g, 133, 128, BRN[0]);

  // ---------- 頭 ----------
  // 耳
  ell(g, 98, 68, 4.5, 6, SKIN, { ambient: 0.3 }); ell(g, 158, 68, 4.5, 6, SKIN, { ambient: 0.12 });
  put(g, 68, 98, SKIN[0]); put(g, 69, 158, SKIN[0]);
  // 顔（すこし角のとれた卵形）
  vol(g, [{ cx, cy: 55, rx: 30, ry: 33 }, { cx, cy: 72, rx: 24, ry: 19, h: 0.9 }], SKIN, { box: [90, 14, 168, 96], ambient: 0.3, gain: 1.6, k: 6 });
  // 顔の下（あごの下の影と首）
  for (let x = 108; x <= 148; x++) { const yb = 89 - Math.round(Math.sqrt(Math.max(0, 1 - ((x - cx) / 21) ** 2)) * 2); put(g, yb + 1, x, SKIN[0]); }
  // 目・眉・鼻・口
  eyeF(g, cx - 13, 66, 6, 6, C, -1); eyeF(g, cx + 13, 66, 6, 6, C, 1);
  // 眉（右がすこし上がる、ずるがしこい顔）
  for (let x = -7; x <= 6; x++) { put(g, 55 + Math.round(x * 0.08) - (x > 2 ? 1 : 0), cx - 13 + x, HAIR[0]); put(g, 56 - (x > 2 ? 1 : 0), cx - 13 + x + 1, HAIR[1]); }
  for (let x = -6; x <= 7; x++) { put(g, 52 - Math.round(x * 0.35) + 1, cx + 13 + x, HAIR[0]); put(g, 53 - Math.round(x * 0.35) + 1, cx + 13 + x - 1, HAIR[1]); }
  for (let y = 70; y <= 78; y++) { put(g, y, cx - 1, SKIN[y < 75 ? 1 : 0]); }
  put(g, 78, cx, SKIN[0]); put(g, 78, cx + 1, SKIN[0]); put(g, 78, cx - 1, SKIN[2]);
  put(g, 74, cx - 3, SKIN[3]); put(g, 75, cx - 3, SKIN[3]);
  // 口: ニッと笑う（右がつり上がる）
  for (let x = -7; x <= 8; x++) { const yy = 83 - Math.round(Math.max(0, Math.abs(x - 1) - 3) * 0.5) + (x > 3 ? -1 : 0); put(g, yy, cx + x, OUT); }
  put(g, 82, cx + 9, SKIN[0]); put(g, 81, cx + 10, SKIN[0]);
  for (let x = -3; x <= 4; x++) put(g, 84, cx + x, x < 2 ? WHITE : SKIN[1]);
  for (let x = -2; x <= 3; x++) put(g, 85, cx + x, SKIN[1]);
  // ほほの赤み
  for (const [dx, dy] of [[-19, 73], [-18, 74], [-17, 73], [19, 73], [18, 74], [17, 73]]) put(g, dy, cx + dx, SKIN[1]);

  // ---------- 髪（風に流れる。左うしろへなびく） ----------
  const hair = [{ cx, cy: 46, rx: 35, ry: 34 }, { cx: cx - 6, cy: 34, rx: 34, ry: 24 }];
  // 前髪の生え際: ギザギザの房が右目の上へ流れる
  const tri = (v) => Math.abs((v % 1 + 1) % 1 - 0.5) * 2;
  const fringe = (x) => 44 + 12 * clamp((x - 96) / 66, 0, 1) + 11 * tri((x - 96) / 17 + 0.5);
  const hairMask = (x, y) => { const dx = x - cx; if (Math.abs(dx) > 34) return false; if (y < fringe(x)) return true; if (Math.abs(dx) > 27 && y < 70 - (Math.abs(dx) - 27) * 2.2) return true; return false; };
  vol(g, hair, HAIR, { box: [86, 4, 172, 96], mask: hairMask, ambient: 0.1, gain: 1.5, tex: (x, y) => { const s = Math.sin(x * 0.55 - y * 0.42); return (s > 0.9 ? 0.1 : s < -0.9 ? -0.09 : 0); } });
  // 髪の房（風でなびく、左うしろへ）
  const lock = (pts, ramp) => tube(g, pts, ramp, { ambient: 0.14, gain: 1.4, tex: (x, y) => (Math.sin(x * 0.5 - y * 0.4) > 0.9 ? 0.1 : 0) });
  lock([[104, 40, 9], [84, 38, 7], [66, 44, 4.5], [54, 54, 1.4]], HAIR);
  lock([[100, 54, 8], [82, 60, 6], [68, 70, 4], [60, 82, 1.2]], HAIR);
  lock([[114, 22, 8], [96, 14, 6], [80, 12, 3.5], [68, 16, 1.2]], HAIR);
  lock([[132, 16, 7], [120, 8, 5], [108, 6, 2.5], [100, 8, 1]], HAIR);
  // 房のつけ根がつくる、明るい帯
  for (let x = 106; x <= 148; x++) { const y = Math.round(cx - x > 0 ? 24 + (x - 106) * 0.0 : 22); if (g[y]?.[x] === HAIR[2]) put(g, y, x, HAIR[3]); }

  // 前髪の下の影（額に落ちる）
  for (let x = 96; x <= 160; x++) { const y = Math.round(fringe(x)); if (SKIN.includes(g[y + 1]?.[x])) put(g, y + 1, x, SKIN[0]); if (SKIN.includes(g[y + 2]?.[x]) && (x % 2 === 0)) put(g, y + 2, x, SKIN[1]); }

  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C4-ガイド", g)]; })();
