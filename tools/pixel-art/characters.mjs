// 256×256 の登場人物（ユーリ・レト・ミナ・コハク・オルカ）。全身の立ち絵。
// 名前・性格・持ち物は docs/story/characters.md に従ったオリジナルのデザイン（既存作品のキャラクターには似せない）。
// 立体感は、ボスと同じ「楕円体の法線と左上からの光」で決める。
import { hash, makeGrid, putNative } from "./lib.mjs";

const W = 256;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const px = (g, r, c, k) => putNative(g, Math.round(r), Math.round(c), k);
const LV = (() => { const v = [-0.55, -0.6, 0.58]; const n = Math.hypot(...v); return v.map((x) => x / n); })();
const lumOf = (nx, ny, d) => nx * LV[0] + ny * LV[1] + Math.sqrt(Math.max(0, 1 - d)) * LV[2];
function toneIdx(len, lum, c, r, jit = 0.06) {
  let t = Math.floor(clamp((lum + 0.45) / 1.35 * len, 0, len - 0.001));
  if (hash(c, r) < jit) t += hash(r, c) < 0.5 ? -1 : 1;
  return clamp(t, 0, len - 1);
}
function ell(g, cx, cy, rx, ry, fn) {
  for (let r = Math.floor(cy - ry); r <= Math.ceil(cy + ry); r++) for (let c = Math.floor(cx - rx); c <= Math.ceil(cx + rx); c++) {
    const nx = (c - cx) / rx, ny = (r - cy) / ry, d = nx * nx + ny * ny; if (d > 1) continue;
    const k = fn(r, c, nx, ny, d, lumOf(nx, ny, d)); if (k !== null && k !== undefined) px(g, r, c, k);
  }
}
const shaded = (ramp, edge = 0, jit = 0.06) => (r, c, nx, ny, d, lum) => (d > 0.86 ? edge : ramp[toneIdx(ramp.length, lum, c, r, jit)]);
/** 先細りの管（腕・脚・髪の束・武器の柄）。縁取り→内側の陰影の順に描く。 */
function taper(g, pts, r0, r1, ramp, edge = 0) {
  const n = pts.length - 1, samples = [];
  for (let s = 0; s < n; s++) { const [x0, y0] = pts[s], [x1, y1] = pts[s + 1], m = Math.max(2, Math.ceil(Math.hypot(x1 - x0, y1 - y0))); for (let i = 0; i < m; i++) samples.push([x0 + (x1 - x0) * i / m, y0 + (y1 - y0) * i / m, r0 + (r1 - r0) * (s + i / m) / n]); }
  for (const [x, y, rad] of samples) ell(g, x, y, rad, rad, () => edge);
  for (const [x, y, rad] of samples) ell(g, x, y, Math.max(0.8, rad - 1.3), Math.max(0.8, rad - 1.3), (r, c, nx, ny, d, lum) => ramp[toneIdx(ramp.length, lum, c, r, 0.04)]);
}
const curve = (p0, p1, p2, steps = 20) => Array.from({ length: steps + 1 }, (_, i) => { const t = i / steps; return [(1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]]; });
const shadowUnder = (g, cx, cy, rx, ry, k) => ell(g, cx, cy, rx, ry, (r, c, nx, ny, d) => (d < 0.55 || hash(c, r) < 0.75 ? k : null));
const rect = (g, x, y, w, h, fn) => { for (let r = y; r < y + h; r++) for (let c = x; c < x + w; c++) { const k = fn(r, c, (c - x) / w, (r - y) / h); if (k !== null && k !== undefined) px(g, r, c, k); } };

// 共通パレット枠: 0縁 1-3肌(暗→明) 4-6髪 7-10服A 11-13服B 14-16革 17-19金属/小物 20-22光/差し色 23虹彩 24白 25影
const P = { edge: 0, skin: [1, 2, 3], hair: [4, 5, 6], A: [7, 8, 9, 10], B: [11, 12, 13], leather: [14, 15, 16], metal: [17, 18, 19], glow: [20, 21, 22], iris: 23, white: 24, shadow: 25 };

/** 台形の胴（肩幅w0→腰幅w1）。左が明るい。 */
function torso(g, y0, y1, w0, w1, ramp, edge = 0) {
  for (let r = y0; r <= y1; r++) { const t = (r - y0) / (y1 - y0), half = w0 + (w1 - w0) * t + Math.sin(t * 3.14) * 3; for (let c = Math.round(128 - half); c <= Math.round(128 + half); c++) { const u = (c - 128) / half; const lum = -u * 0.7 - (t - 0.3) * 0.3 + 0.1; let k = ramp[toneIdx(ramp.length, lum, c, r, 0.05)]; if (Math.abs(u) > 0.94) k = edge; px(g, r, c, k); } }
}
/** 顔（目・眉・鼻・口）。expr で表情を少し変える。 */
function face(g, cx, cy, o = {}) {
  const { eyeGap = 10, eyeY = 0, brow = "flat", mouth = "smile", lash = false } = o;
  for (const sg of [-1, 1]) {
    const ex = cx + sg * eyeGap, ey = cy + eyeY;
    ell(g, ex, ey, 6.4, 5.8, (r, c, nx, ny, d) => (d > 0.8 ? 0 : P.white));
    ell(g, ex + sg * -0.5, ey + 0.5, 4.2, 4.8, (r, c, nx, ny, d, lum) => (d > 0.85 ? 0 : (lum > 0.3 ? P.iris : P.iris)));
    ell(g, ex, ey + 0.5, 2, 2.4, () => 0);
    px(g, ey - 2, ex - 2, P.white); px(g, ey - 2, ex - 1, P.white); px(g, ey - 1, ex - 2, P.white);
    for (let c = -7; c <= 7; c++) { px(g, ey - 5.5 + Math.abs(c) * 0.12, ex + c, 0); if (lash && c * sg > 3) px(g, ey - 7, ex + c, 0); }
    // 眉
    const by = ey - 10;
    for (let c = -7; c <= 7; c++) { const slope = brow === "angry" ? sg * -c * 0.28 * -1 : brow === "soft" ? Math.abs(c) * 0.15 : 0; px(g, by + (brow === "angry" ? (-c * sg) * 0.25 + 2 : slope), ex + c, P.hair[0]); px(g, by + 1 + (brow === "angry" ? (-c * sg) * 0.25 + 2 : slope), ex + c, P.hair[0]); }
  }
  px(g, cy + 9, cx, P.skin[0]); px(g, cy + 10, cx, P.skin[0]); px(g, cy + 10, cx + 1, P.skin[0]);
  const my = cy + 16;
  for (let c = -6; c <= 6; c++) { const curve2 = mouth === "smile" ? -Math.cos(c / 7 * 1.4) * 1.4 + 1.4 : mouth === "smirk" ? (c > 0 ? -c * 0.4 : 0.3) : 0; px(g, my + curve2, cx + c, 0); if (mouth === "smile" && Math.abs(c) < 4) px(g, my + 1.4, cx + c, P.white); }
}
/** 体の土台。脚・胴・首・頭を描き、服の色は呼び出し側から受け取る。stance は左右の脚の開き（[x,y]のずれ）。 */
function body(g, o) {
  const { hw = 22, pants, boots, top, skin = P.skin, headR = [21, 24], headY = 50, legR = [11, 7.5], shoes = 14, torsoW = 28, stance = [[0, 0], [0, 0]], hem = 0 } = o;
  shadowUnder(g, 128, 244, 58 + (torsoW - 28) * 1.4, 8, P.shadow);
  // 脚（長く細く。stance で左右の足の位置をずらす）
  [-1, 1].forEach((sg, i) => {
    const [ox, oy] = stance[i], hx = 128 + sg * hw * 0.5, ax = 128 + sg * hw * 0.62 + ox, ay = 226 + oy;
    taper(g, curve([hx, 148], [(hx + ax) / 2 + ox * 0.3, 188], [ax, ay], 16), legR[0], legR[1], pants);
    ell(g, ax + sg * 2, ay + 7, shoes, 10, shaded(boots));
    ell(g, ax + sg * 6, ay + 12, shoes * 0.9, 6, shaded(boots));
    ell(g, ax, ay - 8, legR[1] + 3.5, 8, shaded(boots));              // ブーツの筒
  });
  // 腰と胴
  ell(g, 128, 148, hw + 4, 15, shaded(pants));
  torso(g, 76, 148, torsoW, hw + 1, top);
  if (hem) torso(g, 148, 148 + hem, hw + 1, hw + 8, top);                 // 上着のすそ
  // 首と頭
  ell(g, 128, 76, 8.5, 10, shaded(skin));
  ell(g, 128, headY, headR[0], headR[1], shaded(skin, 0, 0.04));
  for (const sg of [-1, 1]) ell(g, 128 + sg * (headR[0] - 1), headY + 3, 3.8, 5, shaded(skin));
}
/** 腕（肩→肘→手）。スリーブの色と手の色を指定する。 */
function arm(g, sx, sy, ex, ey, hx, hy, sleeve, skin, r0 = 11, r1 = 8) {
  taper(g, curve([sx, sy], [(sx + ex) / 2, (sy + ey) / 2], [ex, ey], 12), r0, (r0 + r1) / 2, sleeve);
  taper(g, curve([ex, ey], [(ex + hx) / 2, (ey + hy) / 2], [hx, hy], 12), (r0 + r1) / 2, r1, sleeve);
  ell(g, hx, hy + 4, r1 + 2, r1 + 3, shaded(skin));
}
function outlineAll(g, skip) {
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && !skip.includes(g[r][c]);
  const add = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if ((g[r][c] === -1 || skip.includes(g[r][c])) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
  for (const [r, c] of add) g[r][c] = 0;
}
function rimLight(g, skip, col) {
  const bg = (r, c) => r < 0 || r >= W || c < 0 || c >= W || g[r][c] === -1 || skip.includes(g[r][c]);
  const put = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) { const k = g[r][c]; if (k === -1 || k === 0 || skip.includes(k)) continue; if (bg(r, c + 2) && hash(c, r) < 0.7) put.push([r, c]); }
  for (const [r, c] of put) g[r][c] = col;
}
/** 髪の束（根もとから先へ細くなる）。 */
const lock = (g, p0, p1, p2, r0, r1, ramp = P.hair) => taper(g, curve(p0, p1, p2, 14), r0, r1, ramp);

// ======== ユーリ: 16歳。まっすぐで素直な少年。旅装束、左手首に祖父の形見の灯り石の腕輪 ========
const yuri = () => {
  const g = makeGrid();
  // 後ろ: マフラーの端、はねた後ろ髪
  lock(g, [138, 84], [170, 110], [172, 150], 7, 3, P.B); lock(g, [140, 86], [156, 118], [148, 160], 6, 2.5, P.B);
  lock(g, [108, 34], [88, 46], [92, 70], 9, 3); lock(g, [148, 34], [170, 46], [164, 68], 9, 3);
  body(g, { pants: [14, 15, 16], boots: [14, 14, 15], top: P.A, torsoW: 28, hw: 22, stance: [[-2, 0], [10, 0]], hem: 18 });
  // 上着の前あきと襟、ベルトと鞄、灯りの相談所の徽章
  for (let r = 80; r < 166; r++) { px(g, r, 128, 0); px(g, r, 129, P.A[0]); }
  rect(g, 100, 142, 56, 7, (r, c, u, v) => (v < 0.25 ? P.leather[2] : v > 0.8 ? 0 : P.leather[1]));
  ell(g, 128, 145, 5.5, 4.5, shaded(P.metal)); px(g, 145, 128, P.glow[2]);
  rect(g, 138, 150, 22, 20, (r, c, u, v) => (u < 0.08 || u > 0.92 || v < 0.1 || v > 0.9 ? 0 : v < 0.35 ? P.leather[2] : P.leather[1]));   // 腰の鞄
  ell(g, 149, 158, 3, 3, (r, c, nx, ny, d) => (d > 0.5 ? P.metal[1] : P.metal[2]));
  ell(g, 110, 108, 7, 7, (r, c, nx, ny, d) => (d > 0.8 ? 0 : d > 0.4 ? P.glow[1] : P.glow[2]));           // 徽章（灯りの印）
  for (const a of [0, 1, 2, 3]) { const an = a * 1.5708; px(g, 108 + Math.sin(an) * 9, 110 + Math.cos(an) * 9 - 2, P.glow[2]); }
  // 襟のマフラー（橙）
  ell(g, 128, 88, 21, 8, shaded(P.B)); ell(g, 140, 96, 10, 7, shaded(P.B));
  // 腕: 左（向かって右）は腕輪を光らせて胸の前へ、右は自然に下ろす
  arm(g, 100, 92, 88, 122, 92, 150, P.A, P.skin, 9.5, 7); arm(g, 158, 92, 174, 118, 160, 128, P.A, P.skin, 9.5, 7);
  ell(g, 165, 125, 8, 4.5, shaded(P.metal)); ell(g, 165, 125, 5, 2.6, (r, c, nx, ny, d) => (d > 0.5 ? P.glow[1] : P.glow[2]));
  ell(g, 165, 122, 12, 9, (r, c, nx, ny, d) => (d > 0.6 && hash(c, r) < 0.18 ? P.glow[0] : null));       // 腕輪のほのかな光
  // 顔
  face(g, 128, 50, { brow: "soft", mouth: "smile" });
  // 髪: 額にかかる前髪と、外にはねる毛先
  ell(g, 128, 30, 24, 16, (r, c, nx, ny, d, lum) => (ny > 0.45 ? null : shaded(P.hair)(r, c, nx, ny, d, lum)));
  for (const [x, y, dx, ex] of [[106, 34, -14, 10], [114, 28, -8, 6], [126, 24, 0, 2], [138, 26, 8, -2], [148, 30, 14, -6], [154, 38, 18, -10]]) lock(g, [x, y], [x + dx * 0.5, y + 8], [x + dx * 0.9 + ex * 0.2, y + 20 - Math.abs(dx) * 0.3], 8, 2);
  for (const [x, y, dx] of [[104, 20, -18], [118, 12, -8], [134, 10, 6], [148, 16, 16]]) lock(g, [x, y + 8], [x + dx * 0.6, y - 2], [x + dx * 1.1, y - 12], 7, 1.2);      // 跳ねた毛先
  rect(g, 106, 33, 44, 5, (r, c, u) => (u < 0.5 ? P.B[1] : P.B[0]));                                        // バンダナ
  lock(g, [150, 36], [166, 42], [170, 58], 3.5, 1.2, P.B);
  outlineAll(g, [P.shadow]); rimLight(g, [P.shadow], P.white);
  return g;
};
const yuriPal = [["縁", "#160e18"], ["肌暗", "#c4886a"], ["肌", "#e8b088"], ["肌明", "#f8d0aa"], ["髪暗", "#3a1e12"], ["髪", "#6a3a1e"], ["髪明", "#a8642e"], ["上着1", "#0e3a48"], ["上着2", "#1a6478"], ["上着3", "#2c92a4"], ["上着4", "#5cc4cc"], ["橙1", "#a03c10"], ["橙2", "#e0701c"], ["橙3", "#ffb040"], ["革1", "#3a2414"], ["革2", "#6a4426"], ["革3", "#a06a3a"], ["金具1", "#5a5a66"], ["金具2", "#9a9aa8"], ["金具3", "#d8d8e4"], ["灯り1", "#b06a10"], ["灯り2", "#ffb428"], ["灯り3", "#fff0a0"], ["瞳", "#2c7a5c"], ["白", "#ffffff"], ["影", "#1a2418"]];


// ======== レト: 灯里支部の先輩調査員。皮肉屋で実戦派。長い外套、腰に短剣、片手は柄に ========
const reto = () => {
  const g = makeGrid();
  lock(g, [150, 84], [176, 120], [168, 170], 6, 3, P.B);                     // 赤いマフラーの端
  body(g, { pants: [14, 15, 16], boots: [14, 15, 14], top: P.A, torsoW: 27, hw: 21, stance: [[2, 0], [-6, 0]], hem: 52, headR: [20, 24], legR: [10.5, 7] });
  torso(g, 140, 196, 23, 30, P.A);                                             // 長い外套のすそ
  for (let r = 150; r <= 196; r++) { px(g, r, 128, 0); px(g, r, 129, P.A[0]); }   // 外套の割れ目
  for (let r = 84; r <= 150; r++) { px(g, r, 128, 0); px(g, r, 129, P.A[0]); }
  ell(g, 128, 82, 20, 9, shaded(P.A));                                          // 高い襟
  ell(g, 128, 90, 19, 8, shaded(P.B)); ell(g, 142, 100, 9, 7, shaded(P.B));      // マフラー
  rect(g, 102, 138, 52, 6, (r, c, u, v) => (v < 0.3 ? P.leather[2] : v > 0.8 ? 0 : P.leather[1]));
  for (const x of [112, 128, 144]) { px(g, 112, x, P.metal[2]); px(g, 113, x, P.metal[1]); }        // 外套のボタン
  // 短剣（左腰）と握る手
  taper(g, curve([96, 150], [84, 172], [78, 196]), 3.6, 2.4, P.leather); ell(g, 97, 148, 6, 4, shaded(P.metal));
  taper(g, curve([96, 150], [110, 146], [118, 140]), 2.2, 2.2, P.metal);
  arm(g, 100, 92, 86, 122, 96, 148, P.A, P.skin, 9, 6.5); ell(g, 96, 150, 7, 6, shaded([14, 15, 16]));
  arm(g, 156, 92, 168, 122, 150, 144, P.A, P.skin, 9, 6.5); ell(g, 148, 146, 7, 6, shaded([14, 15, 16]));   // 手袋
  face(g, 128, 50, { brow: "angry", mouth: "smirk", eyeGap: 10 });
  // 髪: 後ろへ流した暗い赤茶。一房が目にかかる
  ell(g, 128, 30, 23, 15, (r, c, nx, ny, d, lum) => (ny > 0.4 ? null : shaded(P.hair)(r, c, nx, ny, d, lum)));
  for (const [x, y, dx] of [[104, 30, -20], [114, 22, -10], [128, 18, 0], [142, 22, 10], [152, 30, 20]]) lock(g, [x, y], [x + dx * 0.6, y - 6], [x + dx * 1.2, y - 8], 7, 1.5);
  lock(g, [112, 30], [116, 44], [120, 58], 5, 1.5);
  for (let c = 118; c <= 138; c++) if (hash(c, 1) < 0.5) px(g, 68 + (c % 2), c, P.hair[0]);          // うっすらとした無精ひげ
  outlineAll(g, [P.shadow]); rimLight(g, [P.shadow], P.white);
  return g;
};
const retoPal = [["縁", "#12121a"], ["肌暗", "#b87a5a"], ["肌", "#e0a882"], ["肌明", "#f4c8a0"], ["髪暗", "#2a1010"], ["髪", "#5a2418"], ["髪明", "#8a3a24"], ["外套1", "#1c222c"], ["外套2", "#323c4a"], ["外套3", "#4c5a6c"], ["外套4", "#748498"], ["赤1", "#5a0e14"], ["赤2", "#a01c24"], ["赤3", "#e04a3c"], ["革1", "#2a1a10"], ["革2", "#4a2e1c"], ["革3", "#7a4e2c"], ["金具1", "#5a5a66"], ["金具2", "#a0a0b0"], ["金具3", "#e0e0ec"], ["光1", "#3a5a8a"], ["光2", "#7aa8e0"], ["光3", "#d0e8ff"], ["瞳", "#8a4a20"], ["白", "#ffffff"], ["影", "#14181c"]];

// ======== ミナ: 麦香野の少女。水紋系の使い手。長い髪と、水の紋様の衣。杖に水の珠 ========
const mina = () => {
  const g = makeGrid();
  lock(g, [108, 40], [80, 90], [86, 170], 14, 5); lock(g, [148, 40], [176, 90], [170, 170], 14, 5);     // 長い後ろ髪
  body(g, { pants: [14, 15, 16], boots: [14, 15, 14], top: P.A, torsoW: 23, hw: 20, stance: [[0, 0], [4, 0]], hem: 0, headR: [21, 24], legR: [9, 6.5] });
  // 裾の広がる衣（水のうねり模様）
  for (let r = 146; r <= 214; r++) { const t = (r - 146) / 68, half = 22 + t * 26 + Math.sin(t * 9) * 3 * t; for (let c = Math.round(128 - half); c <= Math.round(128 + half); c++) { const u = (c - 128) / half; const lum = -u * 0.6 - t * 0.2 + 0.2; let k = P.A[toneIdx(4, lum, c, r, 0.05)]; if (Math.abs(u) > 0.95) k = 0; if (Math.sin(c * 0.35 + r * 0.25) > 0.86) k = P.B[toneIdx(3, lum + 0.3, c, r)]; if (r > 208 - Math.sin(c * 0.4) * 3) k = P.B[1]; px(g, r, c, k); } }
  torso(g, 78, 148, 23, 21, P.A);
  rect(g, 106, 136, 44, 8, (r, c, u, v) => (v < 0.3 ? P.B[2] : v > 0.8 ? 0 : P.B[1]));                          // 帯
  ell(g, 128, 112, 6, 7, (r, c, nx, ny, d) => (d > 0.7 ? 0 : d > 0.35 ? P.glow[1] : P.glow[2]));               // 胸の水滴の飾り
  ell(g, 128, 84, 15, 7, shaded(P.B));                                                                          // 襟
  // 腕と杖（水の珠）
  taper(g, curve([172, 60], [174, 130], [176, 236]), 3.4, 3.4, P.leather);
  ell(g, 172, 48, 15, 15, (r, c, nx, ny, d, lum) => (d > 0.85 ? 0 : P.glow[toneIdx(3, lum, c, r, 0.08)]));
  ell(g, 170, 44, 6, 5, () => P.white);
  for (let i = 0; i < 20; i++) { const a = i * 0.6; px(g, 48 + Math.sin(a) * 22, 172 + Math.cos(a) * 22, P.glow[1]); }
  arm(g, 104, 92, 92, 120, 110, 142, P.A, P.skin, 8, 6); arm(g, 152, 92, 168, 118, 174, 132, P.A, P.skin, 8, 6);
  face(g, 128, 50, { brow: "soft", mouth: "smile", lash: true, eyeGap: 10 });
  // 髪: 水色の長い髪、片側の三つ編み、大きなリボン
  ell(g, 128, 32, 24, 17, (r, c, nx, ny, d, lum) => (ny > 0.45 ? null : shaded(P.hair)(r, c, nx, ny, d, lum)));
  for (const [x, y, dx] of [[108, 36, -12], [118, 30, -6], [130, 28, 0], [142, 30, 6], [150, 36, 12]]) lock(g, [x, y], [x + dx * 0.5, y + 10], [x + dx * 0.8, y + 24], 8, 2);
  for (let i = 0; i < 6; i++) ell(g, 100 - i * 1.5, 84 + i * 14, 7 - i * 0.6, 8, shaded(P.hair));                     // 三つ編み
  ell(g, 100, 62, 9, 7, shaded(P.B)); lock(g, [100, 62], [90, 70], [84, 78], 4, 1.5, P.B); lock(g, [100, 62], [108, 72], [110, 82], 4, 1.5, P.B);
  outlineAll(g, [P.shadow]); rimLight(g, [P.shadow], P.white);
  return g;
};
const minaPal = [["縁", "#101828"], ["肌暗", "#d09a80"], ["肌", "#f0c4a4"], ["肌明", "#fde0c8"], ["髪暗", "#1a4a7a"], ["髪", "#3a86c4"], ["髪明", "#8ac8f0"], ["衣1", "#a0b8c8"], ["衣2", "#c8dce8"], ["衣3", "#e4f0f6"], ["衣4", "#ffffff"], ["紺1", "#0a2a4a"], ["紺2", "#1a5a8a"], ["紺3", "#3c94c0"], ["革1", "#3a2414"], ["革2", "#6a4426"], ["革3", "#a06a3a"], ["金具1", "#5a6a7a"], ["金具2", "#a0b4c4"], ["金具3", "#dceaf4"], ["水1", "#1a6aa4"], ["水2", "#4ac0e0"], ["水3", "#b4f0f8"], ["瞳", "#2a6ac0"], ["白", "#ffffff"], ["影", "#182430"]];

// ======== コハク: 硝子湖の交易商人の娘（女の子）。風唱系。ふたつ結びの髪、額にゴーグル、緑のマフラー、背に弓。コインをはじく ========
const guide = () => {
  const g = makeGrid();
  taper(g, curve([164, 30], [196, 110], [166, 196]), 3, 3, P.leather);        // 背負った弓
  for (let i = 0; i < 40; i++) { const t = i / 39; px(g, 30 + t * 166, 164 + Math.sin(t * 3.14) * 30 - 2, P.metal[1]); }
  // ふたつ結びの髪（後ろに垂れる束）
  for (const sg of [-1, 1]) lock(g, [128 + sg * 22, 36], [128 + sg * 40, 66], [128 + sg * 36, 112], 10, 4);
  lock(g, [138, 84], [176, 108], [186, 150], 7, 3, P.B); lock(g, [140, 86], [164, 120], [166, 168], 6, 2.5, P.B);     // 緑のマフラー
  body(g, { pants: [14, 15, 16], boots: [14, 15, 14], top: P.A, torsoW: 23, hw: 20, stance: [[-3, 0], [6, 0]], hem: 0, legR: [8.5, 6.2] });
  // 緑のスカート（ひだ）
  for (let r = 144; r <= 184; r++) { const t = (r - 144) / 40, half = 22 + t * 16; for (let c = Math.round(128 - half); c <= Math.round(128 + half); c++) { const u = (c - 128) / half; const lum = -u * 0.6 - t * 0.2 + 0.15; let k = P.B[toneIdx(3, lum, c, r, 0.04)]; if (Math.abs(u) > 0.95 || r === 184) k = 0; else if (Math.abs(Math.sin((c - 128) * 0.33)) < 0.12 && t > 0.15) k = P.B[0]; px(g, r, c, k); } }
  // 革の胴当てと斜め掛けの鞄
  torso(g, 96, 142, 20, 18, [14, 15, 16], 0);
  for (let i = 0; i < 56; i++) { px(g, 88 + i * 0.95, 104 + i * 0.8, P.leather[2]); px(g, 89 + i * 0.95, 104 + i * 0.8, P.leather[0]); }
  ell(g, 152, 146, 8, 7, shaded(P.leather)); px(g, 146, 152, P.metal[2]);
  ell(g, 128, 88, 18, 8, shaded(P.B)); ell(g, 140, 98, 8, 7, shaded(P.B));
  // 腕: 左は下ろして、右は胸の前でコインをはじく
  arm(g, 104, 92, 94, 120, 102, 146, P.A, P.skin, 8, 6); arm(g, 152, 92, 172, 112, 166, 92, P.A, P.skin, 8, 6);
  ell(g, 170, 78, 6, 6, (r, c, nx, ny, d, lum) => (d > 0.75 ? 0 : P.glow[toneIdx(3, lum, c, r, 0.05)]));            // 宙を舞う金貨
  px(g, 76, 168, P.white); px(g, 72, 176, P.glow[2]); px(g, 66, 172, P.glow[1]);
  face(g, 128, 50, { brow: "soft", mouth: "smirk", lash: true, eyeGap: 10 });
  // 髪: 明るい茶色。前髪と、ふたつ結びの根もと（緑のリボン）、額にゴーグル
  ell(g, 128, 32, 23, 16, (r, c, nx, ny, d, lum) => (ny > 0.42 ? null : shaded(P.hair)(r, c, nx, ny, d, lum)));
  for (const [x, y, dx] of [[108, 34, -10], [118, 30, -5], [130, 28, 0], [142, 30, 5], [150, 34, 10]]) lock(g, [x, y], [x + dx * 0.5, y + 8], [x + dx * 0.8, y + 18], 7, 2);
  for (const sg of [-1, 1]) ell(g, 128 + sg * 23, 38, 6, 5, shaded(P.B));
  rect(g, 102, 22, 52, 5, (r, c, u, v) => (v < 0.5 ? P.leather[2] : P.leather[1]));
  for (const x of [114, 142]) { ell(g, x, 21, 8, 7, (r, c, nx, ny, d, lum) => (d > 0.8 ? 0 : d > 0.45 ? P.metal[1] : P.glow[toneIdx(3, lum, c, r, 0.05)])); }
  outlineAll(g, [P.shadow]); rimLight(g, [P.shadow], P.white);
  return g;
};
const guidePal = [["縁", "#12180e"], ["肌暗", "#c08a62"], ["肌", "#e8b48a"], ["肌明", "#f8d0a8"], ["髪暗", "#6a4a20"], ["髪", "#a87a34"], ["髪明", "#dcb060"], ["服1", "#e8dcc0"], ["服2", "#f4ecd4"], ["服3", "#fffaf0"], ["服4", "#ffffff"], ["緑1", "#0e4a2a"], ["緑2", "#1e8a48"], ["緑3", "#5cc878"], ["革1", "#3a2414"], ["革2", "#6a4426"], ["革3", "#a06a3a"], ["金具1", "#6a5a2a"], ["金具2", "#c0a040"], ["金具3", "#f4e070"], ["光1", "#b08a10"], ["光2", "#ffd838"], ["光3", "#fffab0"], ["瞳", "#3a8a3a"], ["白", "#ffffff"], ["影", "#1a2418"]];

// ======== オルカ: 鉄鏈鉱山の元鉱夫。寡黙で頑固な男。ヘルメットの灯り、肩に巨大なつるはし ========
const orca = () => {
  const g = makeGrid();
  taper(g, curve([184, 234], [170, 140], [182, 30]), 5.5, 4.5, P.leather);                                      // つるはしの柄
  ell(g, 182, 28, 8, 8, shaded(P.metal));
  taper(g, curve([140, 16], [182, 6], [226, 22]), 8, 3, P.metal); taper(g, curve([224, 22], [232, 36], [234, 48]), 3.5, 1.2, P.metal);        // 鋭い刃
  body(g, { pants: [14, 15, 16], boots: [14, 15, 14], top: P.A, torsoW: 40, hw: 30, stance: [[-6, 0], [10, 0]], hem: 12, legR: [15, 10], shoes: 17, headR: [23, 25] });
  // 作業着のベストと反射帯、太いベルト
  torso(g, 88, 148, 36, 30, P.B);
  for (const y of [110, 126]) rect(g, 92, y, 72, 5, (r, c, u, v) => (v < 0.4 ? P.glow[2] : P.glow[1]));
  rect(g, 96, 144, 64, 8, (r, c, u, v) => (v < 0.25 ? P.leather[2] : v > 0.8 ? 0 : P.leather[1])); ell(g, 128, 148, 7, 5, shaded(P.metal));
  for (let r = 90; r <= 148; r++) px(g, r, 128, 0);
  // 太い腕（袖をまくった筋肉）
  arm(g, 92, 96, 70, 128, 76, 156, P.A, P.skin, 14, 10); arm(g, 164, 96, 186, 100, 184, 76, P.A, P.skin, 14, 10);
  ell(g, 74, 128, 15, 12, shaded(P.skin));  ell(g, 180, 98, 15, 12, shaded(P.skin));
  face(g, 128, 50, { brow: "angry", mouth: "flat", eyeGap: 11 });
  // 濃いひげ、傷、ヘルメットとヘッドライト
  ell(g, 128, 68, 20, 13, (r, c, nx, ny, d, lum) => (ny < -0.2 ? null : d > 0.85 ? 0 : P.hair[toneIdx(3, lum, c, r, 0.12)]));
  for (let r = 44; r < 58; r++) px(g, r, 142 + (r - 44) * 0.3, P.skin[0]);                                                 // 頬の傷
  ell(g, 128, 30, 28, 20, (r, c, nx, ny, d, lum) => (ny > 0.35 ? null : shaded(P.metal)(r, c, nx, ny, d, lum)));
  rect(g, 100, 34, 56, 6, (r, c, u, v) => (v < 0.5 ? P.metal[2] : P.metal[0]));
  ell(g, 128, 22, 11, 8, (r, c, nx, ny, d, lum) => (d > 0.8 ? 0 : P.glow[toneIdx(3, lum + 0.3, c, r, 0.05)]));               // ヘッドライト
  for (let i = 0; i < 24; i++) px(g, 22 - i * 0.2, 118 + i, P.glow[0]);                                                     // 光のすじ
  outlineAll(g, [P.shadow]); rimLight(g, [P.shadow], P.white);
  return g;
};
const orcaPal = [["縁", "#12100c"], ["肌暗", "#a06a4a"], ["肌", "#c8905e"], ["肌明", "#e4b484"], ["髭暗", "#1a1210"], ["髭", "#3a2a1e"], ["髭明", "#6a4e38"], ["作業着1", "#2a2e34"], ["作業着2", "#444c56"], ["作業着3", "#68727e"], ["作業着4", "#94a0ac"], ["橙1", "#8a3a10"], ["橙2", "#d8701c"], ["橙3", "#ff9a30"], ["革1", "#2a1a10"], ["革2", "#4a2e1c"], ["革3", "#7a4e2c"], ["金具1", "#4a4e58"], ["金具2", "#8a909c"], ["金具3", "#d0d4dc"], ["光1", "#b08a10"], ["光2", "#ffd838"], ["光3", "#fffab0"], ["瞳", "#5a3a1a"], ["白", "#ffffff"], ["影", "#181410"]];

export const PIECES = [
  { name: "C1-ユーリ", pal: yuriPal, build: yuri },
  { name: "C2-レト", pal: retoPal, build: reto },
  { name: "C3-ミナ", pal: minaPal, build: mina },
  { name: "C4-コハク", pal: guidePal, build: guide },
  { name: "C5-オルカ", pal: orcaPal, build: orca },
];
