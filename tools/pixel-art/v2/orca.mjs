// C5-オルカ（第3章加入・地固系）: 鉄鏈鉱山出身の元鉱山労働者。寡黙で頑固、組合の代表だった大柄な男。
// 短く刈った髪と無精ひげ、橙色の首巻き、腕組み、背にツルハシ。全員のなかでいちばん幅が広いシルエット。
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
  const OUT = pal.rgb("縁", "#0d0a12"), RIM = pal.rgb("縁明", "#3a2e3a");
  const SKIN = pal.ramp("肌", 20, 0.46, 4, 0.3, 0.7, 20);
  const HAIR = pal.ramp("髪", 262, 0.1, 4, 0.07, 0.44, 30);
  const ORG = pal.ramp("首巻き", 24, 0.86, 3, 0.34, 0.6, 16);
  const LEA = pal.ramp("革", 24, 0.4, 4, 0.11, 0.4, 24);
  const CLO = pal.ramp("シャツ", 44, 0.26, 3, 0.34, 0.66, 22);
  const STL = pal.ramp("鉄", 220, 0.2, 4, 0.14, 0.7, 30);
  const WHITE = pal.rgb("白", "#f4efe8");
  const C = { dark: OUT, iris: LEA[2], irisDk: LEA[1], white: WHITE, hi: WHITE };
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 246, 66, 6, LEA[0]);

  // ---------- 背中のツルハシ（右うしろ） ----------
  tube(g, [[186, 200, 3.6], [184, 130, 3.8], [184, 62, 3.6]], LEA, { ambient: 0.22, gain: 1.1 });
  for (let y = 84; y < 200; y += 14) { put(g, y, 182, LEA[0]); put(g, y + 1, 183, LEA[0]); }
  tube(g, [[164, 76, 1.4], [174, 62, 3.6], [185, 56, 5], [198, 60, 4.2], [212, 74, 1.4]], STL, { ambient: 0.16, gain: 1.3 });
  for (let x = 178; x <= 192; x++) { put(g, 62, x, STL[3]); }
  line(g, 174, 62, 170, 66, STL[3]);

  // ---------- 脚・ブーツ ----------
  for (const s of [-1, 1]) {
    tube(g, [[cx + s * 15, 164, 14], [cx + s * 16, 205, 12.5], [cx + s * 16, 230, 11]], STL, { ambient: 0.14, gain: 1.2 });
  }
  // ひざ当て
  for (const s of [-1, 1]) { ell(g, cx + s * 16, 203, 9, 9, LEA, { ambient: 0.22, gain: 1.1 }); for (let a = 0; a < 6.3; a += 0.4) put(g, 203 + Math.sin(a) * 6, cx + s * 16 + Math.cos(a) * 6, a < 3.2 ? LEA[3] : LEA[0]); }
  for (const s of [-1, 1]) {
    ell(g, cx + s * 17, 240, 16, 9, LEA, { ambient: 0.14, gain: 1.2 });
    for (let x = -12; x <= 12; x++) { put(g, 229, cx + s * 16 + x, LEA[3]); put(g, 230, cx + s * 16 + x, LEA[1]); put(g, 231, cx + s * 16 + x, LEA[0]); }
    for (let x = 4; x <= 14; x++) put(g, 243, cx + s * 17 + x * (s < 0 ? -1 : 1) - (s < 0 ? 0 : 0), STL[2]);
  }
  // 脚のあいだ
  for (let y = 178; y < 232; y++) for (let x = cx - 3; x <= cx + 3; x++) if (g[y][x] < 0) put(g, y, x, STL[0]);

  // ---------- 首・胴 ----------
  tube(g, [[128, 86, 13], [128, 104, 14]], SKIN, { ambient: 0.16, gain: 1.0 });
  const torso = [{ cx, cy: 132, rx: 36, ry: 34 }, { cx, cy: 112, rx: 42, ry: 15 }, { cx, cy: 150, rx: 33, ry: 18 }];
  const tbox = [78, 90, 180, 178];
  vol(g, torso, CLO, { box: tbox, ambient: 0.12, gain: 1.15 });
  // 革のベスト（前があいて、シャツの合わせが見える）
  const open = (x, y) => Math.abs(x - cx) < 4 + Math.max(0, (y - 108) * 0.06);
  vol(g, torso, LEA, { box: tbox, mask: (x, y) => !open(x, y) && y > 104 && Math.abs(x - cx) < 38 - (y - 104) * 0.08, ambient: 0.14, gain: 1.3 });
  for (let y = 108; y < 156; y++) { const w = 4 + Math.max(0, (y - 108) * 0.06); put(g, y, Math.round(cx - w), LEA[0]); put(g, y, Math.round(cx + w), LEA[0]); }
  // ベストのボタン留めの金具
  for (let y = 116; y < 152; y += 9) { put(g, y, cx, STL[3]); put(g, y, cx + 1, STL[1]); put(g, y - 1, cx, WHITE); }
  // 太いベルトと道具ぶら下げ
  for (let y = 152; y < 162; y++) for (let x = 90; x <= 166; x++) { const half = 33 + (y - 152) * 0.4; if (Math.abs(x - cx) > half) continue; put(g, y, x, y === 152 ? LEA[3] : y < 156 ? LEA[2] : y < 160 ? LEA[1] : LEA[0]); }
  for (let y = 151; y <= 162; y++) for (let x = cx - 7; x <= cx + 7; x++) put(g, y, x, y === 151 || x === cx - 7 ? WHITE : y === 162 || x === cx + 7 ? STL[0] : (x + y) % 5 === 0 ? STL[3] : STL[2]);
  for (let y = 154; y <= 159; y++) for (let x = cx - 3; x <= cx + 3; x++) put(g, y, x, STL[0]);
  // 腰の小さな金づちとカンテラ
  tube(g, [[100, 160, 2.6], [100, 178, 2.6]], LEA, { ambient: 0.2 });
  vol(g, [{ cx: 100, cy: 182, rx: 7, ry: 5 }], STL, { box: [90, 174, 112, 192], ambient: 0.2, gain: 1.2 });
  ell(g, 158, 172, 6, 8, [ORG[0], ORG[1], ORG[2]], { ambient: 0.4 });
  put(g, 168, 156, WHITE); put(g, 168, 157, WHITE);
  for (let x = 153; x <= 163; x++) { put(g, 163, x, STL[1]); put(g, 181, x, STL[0]); }

  // ---------- 腕組み ----------
  // うしろになる前腕（右腕が胸をよこぎる）
  tube(g, [[160, 108, 12], [162, 130, 11.5], [158, 146, 10.5]], CLO, { ambient: 0.14, gain: 1.2 });
  tube(g, [[158, 146, 9.5], [140, 140, 9.2], [112, 128, 8.6]], SKIN, { ambient: 0.16, gain: 1.4 });
  ell(g, 106, 126, 7, 6.5, SKIN, { ambient: 0.3 });
  // 手前の前腕（左腕が上に）
  tube(g, [[96, 108, 12], [94, 130, 11.5], [98, 146, 10.5]], CLO, { ambient: 0.14, gain: 1.2 });
  tube(g, [[100, 146, 9.5], [120, 138, 9.8], [150, 126, 9]], SKIN, { ambient: 0.18, gain: 1.5 });
  ell(g, 154, 126, 7.5, 7, SKIN, { ambient: 0.14, gain: 1.2 });
  for (let k = 0; k < 3; k++) line(g, 151 + k * 3, 122 + (k === 1 ? 0 : 1), 151 + k * 3, 126, SKIN[0]);
  // 革の腕当て（手首に）
  for (let t = 0; t < 16; t++) { const x = 142 - t * 0.0 + 0, y = 128 - t * 0.0; }
  for (const [x0, y0, x1, y1] of [[132, 134, 138, 121], [136, 133, 142, 120]]) line(g, x0, y0, x1, y1, LEA[1]);
  for (const [x0, y0, x1, y1] of [[133, 133, 139, 121], [137, 132, 143, 120]]) line(g, x0, y0, x1, y1, LEA[2]);
  // シャツの袖口のしわ
  line(g, 90, 136, 100, 140, CLO[0]); line(g, 92, 132, 99, 135, CLO[0]); line(g, 156, 136, 165, 134, CLO[0]);
  // 腕のすじ（力こぶの影）
  line(g, 112, 146, 124, 141, SKIN[0]); line(g, 108, 142, 118, 138, SKIN[1]);

  // ---------- 首巻き（橙・要点の鮮やかな色） ----------
  tube(g, [[104, 100, 8], [116, 108, 10], [128, 111, 11], [140, 108, 10], [152, 100, 8]], ORG, { ambient: 0.3, gain: 0.9 });
  fillPoly(g, [[116, 108], [140, 108], [134, 132], [128, 138], [122, 132]], (x, y) => { const t = (y - 108) / 30; const l = (x - 116) / 24; return ORG[clamp(Math.round((1 - t) * 1.2 + (0.5 - l) * 1.0), 0, 2)]; });
  line(g, 123, 118, 128, 136, ORG[0]); line(g, 133, 115, 129, 135, ORG[0]);
  line(g, 118, 110, 138, 110, ORG[0]);

  // ---------- 頭 ----------
  ell(g, 96, 70, 5.5, 7, SKIN, { ambient: 0.3 }); ell(g, 160, 70, 5.5, 7, SKIN, { ambient: 0.12 });
  put(g, 71, 96, SKIN[0]); put(g, 72, 160, SKIN[0]);
  vol(g, [{ cx, cy: 55, rx: 32, ry: 32 }, { cx, cy: 72, rx: 29, ry: 17, h: 0.95 }], SKIN, { box: [90, 14, 168, 96], ambient: 0.32, gain: 1.25, k: 6 });
  // ひたいのしわ・かたい頬のかげ
  for (let x = -12; x <= 12; x++) if (x % 5 !== 0) put(g, 46, cx + x, SKIN[1]);
  // 目（小さく細く、するどい）
  eyeF(g, cx - 14, 65, 4, 3, C, -1); eyeF(g, cx + 14, 65, 4, 3, C, 1);
  // 太い眉（内側がさがる）
  for (let x = -9; x <= 8; x++) for (let t = 0; t < 3; t++) put(g, 52 + Math.round((x + 9) * 0.17) + t, cx - 14 + x, t === 0 ? HAIR[2] : t === 1 ? HAIR[1] : HAIR[0]);
  for (let x = -8; x <= 9; x++) for (let t = 0; t < 3; t++) put(g, 52 + Math.round((8 - x) * 0.17) + t, cx + 14 + x, t === 0 ? HAIR[2] : t === 1 ? HAIR[1] : HAIR[0]);
  // 眉間のしわ
  put(g, 58, cx - 2, SKIN[0]); put(g, 59, cx - 2, SKIN[0]); put(g, 58, cx + 2, SKIN[0]); put(g, 59, cx + 2, SKIN[0]);
  // 目の下のくま
  for (let x = -5; x <= 5; x++) { put(g, 71, cx - 14 + x, SKIN[1]); put(g, 71, cx + 14 + x, SKIN[1]); }
  // 鼻
  for (let y = 66; y <= 76; y++) put(g, y, cx - 1, SKIN[y < 72 ? 1 : 0]);
  for (let x = -5; x <= 4; x++) put(g, 76, cx + x, x < -3 || x > 2 ? SKIN[0] : OUT);
  put(g, 74, cx - 3, SKIN[3]); put(g, 75, cx - 4, SKIN[3]); put(g, 73, cx - 3, SKIN[3]);
  // 傷あと（左のまゆから頬へ）
  line(g, cx - 20, 52, cx - 18, 76, SKIN[3]); line(g, cx - 19, 52, cx - 17, 76, SKIN[0]);
  for (const yy of [58, 63, 69]) { put(g, yy, cx - 21 + Math.round((yy - 52) * 0.1), SKIN[0]); put(g, yy, cx - 19 + Math.round((yy - 52) * 0.1), SKIN[0]); }
  // ひげ（ほほ・鼻の下・あご）: 肌の色をひげの色へ置きかえ、ところどころ肌を残す
  for (let y = 60; y < 96; y++) for (let x = 90; x < 168; x++) {
    const i = SKIN.indexOf(g[y][x]); if (i < 0) continue; const dx = x - cx, ad = Math.abs(dx);
    if (ad > 30) continue;
    const m = (ad > 19 && y > 64 && y > 62 + (ad - 19) * -0.0) || (y > 75 && y < 80 && ad < 18) || (y > 79 && ad > 8) || y > 86;
    if (!m) continue; if (y > 80 && y < 86 && ad < 8) continue;
    if (y < 68 + (ad - 19) * 0.0 && ad > 19 && y < 66) continue;
    put(g, y, x, hash(x, y) < 0.86 ? HAIR[clamp(i, 0, 2)] : SKIN[i]);
  }
  // 口（への字）
  for (let x = -6; x <= 6; x++) put(g, 82 + Math.round(Math.abs(x) * 0.22), cx + x, OUT);
  for (let x = -5; x <= 5; x++) put(g, 83 + Math.round(Math.abs(x) * 0.22), cx + x, SKIN[1]);

  // ---------- 髪（短く刈る。こめかみに白髪） ----------
  const hairY = (x) => 37 + Math.abs(x - cx) * 0.2 + (Math.abs(x - cx) < 7 ? 4 : 0);
  const hairMask = (x, y) => { const dx = Math.abs(x - cx); if (dx > 35) return false; if (y < hairY(x)) return true; if (dx > 29 && y < 62 - (dx - 29) * 1.6) return true; return false; };
  vol(g, [{ cx, cy: 46, rx: 35, ry: 33 }, { cx: cx - 6, cy: 36, rx: 32, ry: 22 }], HAIR, { box: [86, 4, 172, 96], mask: hairMask, ambient: 0.16, gain: 1.6, tex: (x, y) => (hash(x, y) < 0.16 ? 0.12 : hash(x + 7, y) < 0.1 ? -0.1 : 0) });
  // こめかみの白髪
  for (let y = 44; y < 62; y++) for (const s of [-1, 1]) { const x = cx + s * (31 - (y - 44) * 0.06); if (HAIR.includes(g[y][Math.round(x)]) && hash(y, s) < 0.7) { put(g, y, Math.round(x), HAIR[3]); put(g, y, Math.round(x) - s, HAIR[2]); } }

  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C5-オルカ", g)]; })();
