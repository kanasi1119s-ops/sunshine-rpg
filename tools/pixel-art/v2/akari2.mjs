// 灯里の歪み（序章のボス・v2 重厚版）: 歪んだ灯り石に呑まれた、巨大な古い角灯。
// 割れたガラスの内側で炎がのたうち、一つ目が外をにらむ。錆びた鉄枠、傷、鎖、紫の歪みが這い上がる。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, eye, hash, put, clamp, smoothstep, W, toPieceFile } from "./lib2.mjs";

const vnoise = (x, y, s) => { const gx = x / s, gy = y / s, x0 = Math.floor(gx), y0 = Math.floor(gy), fx = gx - x0, fy = gy - y0, sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy); const a = hash(x0, y0), b = hash(x0 + 1, y0), c = hash(x0, y0 + 1), d = hash(x0 + 1, y0 + 1); return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy; };
const pip = (poly, x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#070510"), RIM = pal.rgb("縁明", "#2c2440"), SHD = pal.rgb("影", "#100b1a");
  const IRON = pal.ramp("鉄", 240, 0.24, 5, 0.07, 0.5, 34);
  const RUST = pal.ramp("錆", 20, 0.62, 3, 0.16, 0.44, 24);
  const GLASS = pal.ramp("ガラス", 195, 0.34, 3, 0.2, 0.6, 20);
  const VIO = pal.ramp("歪み", 276, 0.5, 3, 0.12, 0.5, 30);
  const FIRE = [...pal.ramp("炎", 14, 1.0, 3, 0.2, 0.56, 30), pal.rgb("炎黄", "#ffb52e"), pal.rgb("炎芯", "#ffe98a")];
  const EYE = pal.ramp("目", 350, 0.8, 3, 0.36, 0.7, 10);
  const WHITE = pal.rgb("白", "#f4f0ff");
  const g = makeGrid();
  const cx = 128;
  const hw = (y) => 62 - (y - 84) * 0.09;      // 胴の半幅（下すぼまり）
  const BODY_T = 86, BODY_B = 190;
  const inBody = (x, y) => y >= BODY_T && y <= BODY_B && Math.abs(x - cx) <= hw(y);

  // 地面の影
  groundShadow(g, cx, 240, 96, 9, SHD);

  // ---------- 鎖（輪を1つずつ描く。光は左上） ----------
  const link = (x, y, ang, a, b) => {
    for (let off = 0; off < 2; off++) for (let t = 0; t < 6.283; t += 0.04) {
      const ex = Math.cos(t) * (a - off), ey = Math.sin(t) * (b - off);
      const px = x + ex * Math.cos(ang) - ey * Math.sin(ang), py = y + ex * Math.sin(ang) + ey * Math.cos(ang);
      const nx = Math.cos(t) * Math.cos(ang) / (a) - Math.sin(t) * Math.sin(ang) / b * 0, ny = Math.sin(t);
      const lum = clamp(0.5 + (-(px - x) * 0.6 - (py - y) * 0.8) / Math.max(a, b) * (off ? -0.55 : 0.75), 0, 1);
      put(g, py, px, IRON[clamp(Math.round(lum * 3) + (off ? 0 : 1), 0, 4)]);
    }
  };
  const flatLink = (x, y, ang, a) => { for (let s = -a; s <= a; s++) for (let w = -1; w <= 1; w++) { const px = x + s * Math.cos(ang) - w * Math.sin(ang), py = y + s * Math.sin(ang) + w * Math.cos(ang); put(g, py, px, IRON[w < 0 ? 3 : w === 0 ? 2 : 1]); } };
  const chain = (pts, step) => {
    let acc = 0, i = 0, prev = pts[0];
    for (let k = 1; k < pts.length; k++) {
      const [x, y] = pts[k], d = Math.hypot(x - prev[0], y - prev[1]); acc += d;
      if (acc >= step) { const ang = Math.atan2(y - prev[1], x - prev[0]); if (i % 2 === 0) link(x, y, ang, 7.5, 4.6); else flatLink(x, y, ang, 6); i++; acc = 0; }
      prev = [x, y];
    }
  };
  // 吊り鎖（上へ伸びる）
  chain(Array.from({ length: 60 }, (_, i) => [cx, 46 - i]), 9);
  // 地面に落ちた鎖（左は垂れ下がり、右は地面をはう）
  chain(bezier([74, 196], [30, 210], [34, 244], 40), 9);
  chain(bezier([32, 246], [20, 248], [8, 244], 10), 9);
  chain(bezier([180, 200], [232, 214], [228, 246], 40), 9);

  // ---------- 内側: 暗い空洞と、紫に染まる奥 ----------
  const flameHf = heightField([
    { cx: cx + 2, cy: 154, rx: 34, ry: 30, h: 1 },
    { cx: cx - 2, cy: 128, rx: 26, ry: 40, h: 1 },
    { cx: cx + 10, cy: 104, rx: 14, ry: 26, h: 1 },
    { cx: cx + 2, cy: 92, rx: 7, ry: 12, h: 1 },
    { cx: cx - 30, cy: 150, rx: 10, ry: 22, h: 0.9 },
    { cx: cx + 36, cy: 146, rx: 10, ry: 24, h: 0.9 },
  ], 6);
  let hmax = 0; for (let y = 80; y < 200; y++) for (let x = 80; x < 180; x++) hmax = Math.max(hmax, flameHf(x, y));
  for (let y = BODY_T; y <= BODY_B; y++) for (let x = cx - 66; x <= cx + 66; x++) {
    if (!inBody(x, y)) continue;
    const h = flameHf(x, y) / hmax;
    // 炎のゆらぎ（縦に流れる揺れで縁が波打つ）
    const w = Math.sin(y * 0.23 + x * 0.09) * 0.05 + (vnoise(x * 1.5, y * 0.5, 6) - 0.5) * 0.14;
    let v = h + w * (h > 0.02 ? 1 : 0);
    let k;
    const dist = Math.hypot((x - cx) / 62, (y - 138) / 56);
    if (v > 0.1) {
      v += (-(x - cx) * 0.0008 - (y - 140) * 0.0006);
      v -= 0.06; k = v < 0.2 ? VIO[2] : v < 0.4 ? FIRE[0] : v < 0.58 ? FIRE[1] : v < 0.76 ? FIRE[2] : v < 0.9 ? FIRE[3] : FIRE[4];
    } else {
      // 炎のまわりの照り返し（市松のディザで奥が明るくなる）
      const glow = 1 - dist;
      k = glow > 0.42 ? ((x + y) % 2 === 0 ? VIO[1] : VIO[0]) : glow > 0.22 ? ((x + y) % 2 === 0 ? VIO[0] : SHD) : SHD;
      if (glow > 0.62) k = VIO[1];
    }
    put(g, y, x, k);
  }

  // ---------- 一つ目 ----------
  eye(g, cx, 142, 21, 17, EYE, OUT, 0);
  // 瞳の縦の裂け目と、白い反射
  for (let y = 132; y <= 152; y++) { const w = Math.round((1 - Math.abs(y - 142) / 11) * 3); for (let x = -w; x <= w; x++) if (Math.abs(y - 142) <= 10) put(g, y, cx + x + 1, OUT); }
  for (const [dx, dy] of [[-9, -8], [-8, -8], [-9, -7], [-6, -9]]) put(g, 142 + dy, cx + dx, WHITE);
  // まぶたの影（上から半分かぶさる、怒った目）
  for (let x = -22; x <= 22; x++) { const yy = 142 - 16 + Math.round(Math.abs(x) * 0.0 + (x < 0 ? -x * 0.3 : x * 0.05)) ; put(g, yy, cx + x, OUT); put(g, yy - 1, cx + x, VIO[0]); }

  // ---------- ガラスの割れ穴（ぎざぎざ） ----------
  const holes = [
    [[132, 92], [142, 96], [152, 91], [158, 103], [151, 110], [161, 121], [146, 127], [141, 116], [129, 111], [135, 103]],
    [[80, 142], [92, 147], [99, 141], [102, 158], [93, 172], [84, 166], [78, 154]],
    [[160, 152], [170, 158], [178, 147], [184, 164], [172, 178], [163, 168]],
  ];
  const inHole = (x, y) => holes.some((p) => pip(p, x + 0.5, y + 0.5));

  // ---------- ガラスの反射（左上から。ひび割れと一緒に） ----------
  const panelEdges = [-1, -0.5, 0.5, 1]; // 半幅に対する柱の位置
  const panelOf = (x, y) => { const u = (x - cx) / hw(y); return u < -0.5 ? 0 : u < 0.5 ? 1 : 2; };
  for (let y = BODY_T; y <= BODY_B; y++) for (let x = cx - 66; x <= cx + 66; x++) {
    if (!inBody(x, y) || inHole(x, y)) continue;
    const p = panelOf(x, y), u = (x - cx) / hw(y);
    const left = p === 0 ? -1 : p === 1 ? -0.5 : 0.5, right = p === 0 ? -0.5 : p === 1 ? 0.5 : 1;
    const t = (u - left) / (right - left); // パネル内の位置 0..1
    const c = g[y][x];
    // 斜めの反射帯（太い帯と細い帯）
    const s = t * 60 + (y - BODY_T) * 0.55;
    const inWide = s > 10 && s < 17 && (y - BODY_T) < 78, inThin = s > 20 && s < 22.5 && (y - BODY_T) < 60;
    if (inWide) put(g, y, x, VIO.includes(c) || c === SHD ? GLASS[1] : FIRE.includes(c) ? FIRE[clamp(FIRE.indexOf(c) + 1, 0, 4)] : c);
    else if (inThin) put(g, y, x, VIO.includes(c) || c === SHD ? GLASS[2] : c);
    // パネル右下の縁: 炎のオレンジが内側から映る
    if (t > 0.9 && (y - BODY_T) > 20 && (x + y) % 2 === 0 && (VIO.includes(c) || c === SHD)) put(g, y, x, FIRE[0]);
    // ガラスの曇り（細かい格子）
    if (x % 2 === 0 && y % 2 === 0 && (VIO.includes(g[y][x]) || g[y][x] === SHD)) put(g, y, x, GLASS[0]);
    // 上端はガラスが厚く暗い
    if (y - BODY_T < 3 && VIO.includes(c)) put(g, y, x, GLASS[0]);
  }
  // 反射帯の端に白い光の点
  for (let p = 0; p < 3; p++) { const left = [-1, -0.5, 0.5][p], right = [-0.5, 0.5, 1][p]; for (let y = BODY_T + 3; y < BODY_T + 8; y++) { const u = left + (right - left) * ((10.5 - (y - BODY_T) * 0.55) / 60); const x = Math.round(cx + u * hw(y)); if (inBody(x, y) && !inHole(x, y)) put(g, y, x + 1, WHITE); } }

  // ひび割れ（穴から放射。明るい線と、影の線）
  const crack = (x0, y0, x1, y1, seed) => {
    let x = x0, y = y0; const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0));
    for (let i = 0; i < n * 1.2; i++) {
      const t = i / (n * 1.2); x += (x1 - x0) / (n * 1.2) + (hash(i, seed) - 0.5) * 1.6; y += (y1 - y0) / (n * 1.2) + (hash(i, seed + 7) - 0.5) * 1.6;
      const px = Math.round(x), py = Math.round(y); if (!inBody(px, py) || inHole(px, py)) continue;
      put(g, py, px, t < 0.7 ? GLASS[2] : GLASS[1]); put(g, py + 1, px + 1, VIO[2]);
      if (hash(i, seed + 3) < 0.09) { put(g, py, px - 1, GLASS[2]); }
    }
  };
  crack(132, 100, 100, 88, 1); crack(130, 110, 104, 122, 2); crack(146, 128, 150, 172, 3); crack(158, 106, 178, 92, 4); crack(151, 110, 168, 132, 8);
  crack(92, 172, 100, 186, 5); crack(80, 146, 70, 120, 6); crack(178, 162, 172, 186, 7); crack(99, 145, 118, 150, 9);

  // 穴の縁（欠けたガラスの断面が光る。左上の縁は白、ほかは水色）
  for (let y = BODY_T; y <= BODY_B; y++) for (let x = cx - 66; x <= cx + 66; x++) {
    if (!inBody(x, y) || !inHole(x, y)) continue;
    const nb = [[-1, 0], [0, -1], [1, 0], [0, 1]].map(([a, b]) => inBody(x + a, y + b) && !inHole(x + a, y + b));
    if (nb.some(Boolean)) put(g, y, x, (nb[0] || nb[1]) && (x + y) % 3 !== 0 ? WHITE : GLASS[2]);
  }
  // 穴からあふれる炎の舌（右へ）
  // 炎の舌: 経路に沿って円をならべ、中心ほど明るく縁ほど暗い赤にする（うねりつき）
  const flick = (pts, r0, r1, amp) => {
    const best = new Map();
    pts.forEach(([px, py], i) => {
      const t = i / (pts.length - 1), r = r0 + (r1 - r0) * t, ox = Math.sin(t * 7) * amp * (1 - t * 0.3);
      for (let y = -r - 1; y <= r + 1; y++) for (let x = -r - 1; x <= r + 1; x++) { const d = Math.hypot(x, y) / r; if (d > 1) continue; const key = Math.round(py + y) * 1000 + Math.round(px + x + ox); if (!(best.has(key) && best.get(key) <= d)) best.set(key, d + t * 0.25); }
    });
    for (const [key, d] of best) { const yy = Math.floor(key / 1000), xx = key % 1000; put(g, yy, xx, d < 0.22 ? FIRE[4] : d < 0.45 ? FIRE[3] : d < 0.72 ? FIRE[2] : d < 0.92 ? FIRE[1] : FIRE[0]); }
  };
  flick(bezier([146, 110], [182, 108], [178, 62], 40), 11, 1.5, 4);
  flick(bezier([172, 162], [200, 170], [204, 138], 30), 8, 1.5, 3);
  flick(bezier([138, 96], [126, 84], [140, 70], 20), 6, 1.2, 2);
  // 左の穴の紫の煙
  limb(g, bezier([88, 152], [66, 140], [58, 112], 18), 7, 2, VIO, { ambient: 0.5 });

  // ---------- 鉄枠 ----------
  const kink = (y) => (y > 118 && y < 150 ? Math.round(Math.sin((y - 118) / 32 * Math.PI) * 4) : 0); // 右の柱は衝撃で曲がっている
  const post = (u, bend) => {
    for (let y = BODY_T - 2; y <= BODY_B + 2; y++) {
      const x0 = Math.round(cx + u * hw(y)) + (bend ? kink(y) : 0), thick = Math.abs(u) === 1 ? 3 : 2;
      for (let t = -thick; t <= thick; t++) {
        const f = (t + thick) / (2 * thick); // 0 左 → 1 右
        put(g, y, x0 + t, IRON[f < 0.18 ? 4 : f < 0.4 ? 3 : f < 0.7 ? 2 : f < 0.9 ? 1 : 0]);
      }
      // 傷: 柱に斜めの引っかき
      if ((y + Math.round(u * 20)) % 23 === 0) { put(g, y, x0 - 1, IRON[4]); put(g, y + 1, x0, IRON[4]); put(g, y + 2, x0 + 1, IRON[3]); }
    }
  };
  for (const u of [-1, -0.5, 0.5, 1]) post(u, u === 0.5);
  // 柱の留め金（金具と鋲）
  for (const y of [108, 170]) for (const u of [-1, -0.5, 0.5, 1]) {
    const x0 = Math.round(cx + u * hw(y)) + (u === 0.5 ? kink(y) : 0);
    for (let r = -3; r <= 3; r++) for (let c = -6; c <= 6; c++) put(g, y + r, x0 + c, IRON[r === -3 ? 4 : r < 0 ? 3 : r < 2 ? 2 : r === 2 ? 1 : 0]);
    for (const dx of [-4, 4]) { put(g, y, x0 + dx, IRON[4]); put(g, y + 1, x0 + dx, IRON[0]); }
  }

  // 屋根（円すいと、ふち）
  paintField(g, heightField([{ cx, cy: 86, rx: 72, ry: 10, h: 1 }, { cx, cy: 72, rx: 48, ry: 22, h: 1 }, { cx, cy: 56, rx: 26, ry: 13, h: 1 }, { cx, cy: 46, rx: 12, ry: 9, h: 1 }], 5), IRON, { ambient: 0.18, gain: 1.0, box: [40, 30, 216, 100], tex: (x, y) => (Math.abs(((x - cx) * 0.22 + (y - 40) * 0.5) % 6) < 0.5 ? -0.09 : 0) });
  // 屋根のへこみと欠け（右の縁が欠けている）
  for (let y = 80; y <= 90; y++) for (let x = 176; x <= 196; x++) if (hash(x, y) < 0.5 && (x - 176) + (y - 80) * 1.3 > 14 && g[y][x] >= 0) g[y][x] = -1;
  // 吊り輪
  for (let a = 0; a < 6.283; a += 0.02) for (const rr of [9, 10, 11]) { const x = cx + Math.cos(a) * rr, y = 33 + Math.sin(a) * rr, lum = clamp(0.5 + (-Math.cos(a) * 0.6 - Math.sin(a) * 0.8) * 0.5, 0, 1); put(g, y, x, IRON[clamp(Math.round(lum * 4) - (rr === 11 ? 1 : 0), 0, 4)]); }
  // 底の受け皿と足
  paintField(g, heightField([{ cx, cy: 199, rx: 68, ry: 10, h: 1 }, { cx, cy: 210, rx: 50, ry: 9, h: 1 }], 5), IRON, { ambient: 0.16, gain: 1.0, box: [40, 180, 216, 230] });
  for (const fx of [-50, 0, 50]) for (let r = 0; r < 9; r++) for (let c = -7; c <= 7; c++) { if (Math.abs(c) > 7 - r * 0.35) continue; put(g, 216 + r, cx + fx + c, IRON[c < -3 ? 3 : c < 3 ? 2 : c < 6 ? 1 : 0]); }

  // ---------- 錆・傷（鉄の色だけを置き換える） ----------
  const isIron = (k) => IRON.includes(k);
  for (let y = 26; y < 232; y++) for (let x = 24; x < 232; x++) {
    const k = g[y][x]; if (!isIron(k)) continue;
    const i = IRON.indexOf(k);
    // 錆は「下・縁・重なりの隙間」にたまる
    const n = vnoise(x + 11, y + 3, 6) * 0.65 + vnoise(x, y, 2.5) * 0.35;
    const wet = smoothstep(90, 210, y) * 0.14 + (i <= 1 ? 0.1 : 0);
    if (n + wet > 0.84) g[y][x] = RUST[i <= 1 ? 0 : i <= 3 ? 1 : 2];
  }
  // 鉄の傷（細い明るい引っかき線と、暗い凹み）
  for (let s = 0; s < 46; s++) {
    let x = 44 + Math.floor(hash(s, 1) * 170), y = 40 + Math.floor(hash(s, 2) * 190); if (!isIron(g[y][x]) && !RUST.includes(g[y][x])) continue;
    const len = 3 + Math.floor(hash(s, 3) * 5), dir = hash(s, 4) < 0.6 ? 1 : -1;
    for (let i = 0; i < len; i++) { if (isIron(g[y][x]) || RUST.includes(g[y][x])) put(g, y, x, IRON[4]); if (isIron(g[y + 1]?.[x + 1]) || RUST.includes(g[y + 1]?.[x + 1])) put(g, y + 1, x + 1, IRON[0]); x += dir; y += 1; }
  }

  // ---------- 紫の歪み: 地面から這い上がり、枠に絡む ----------
  const tendril = (pts, r0, r1) => limb(g, pts, r0, r1, VIO, { ambient: 0.22 });
  tendril(bezier([50, 236], [44, 206], [78, 196], 20), 7, 3);
  tendril(bezier([64, 202], [50, 170], [74, 150], 20), 5, 2);
  tendril(bezier([204, 236], [214, 208], [182, 194], 20), 7, 3);
  tendril(bezier([190, 200], [206, 170], [184, 148], 20), 5, 2);
  tendril(bezier([104, 240], [98, 224], [112, 214], 12), 5, 2);
  // 底の割れ目から漏れる紫の光
  for (let x = cx - 40; x <= cx + 40; x += 1) if (hash(x, 5) < 0.34) { put(g, 206 + Math.round(Math.sin(x * 0.3) * 1), x, VIO[2]); }

  // ---------- 浮かぶガラスの破片（面ごとに明暗、縁が光る） ----------
  const shard = (pts, seed) => {
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    for (let y = Math.min(...ys); y <= Math.max(...ys); y++) for (let x = Math.min(...xs); x <= Math.max(...xs); x++) {
      if (!pip(pts, x + 0.5, y + 0.5)) continue;
      const u = (x - Math.min(...xs)) / (Math.max(...xs) - Math.min(...xs) + 1), v = (y - Math.min(...ys)) / (Math.max(...ys) - Math.min(...ys) + 1);
      put(g, y, x, u + v < 0.5 ? GLASS[2] : u + v < 1.15 ? GLASS[1] : GLASS[0]);
    }
    for (let y = Math.min(...ys); y <= Math.max(...ys); y++) for (let x = Math.min(...xs); x <= Math.max(...xs); x++) if (pip(pts, x + 0.5, y + 0.5) && (!pip(pts, x - 0.5, y + 0.5) || !pip(pts, x + 0.5, y - 0.5)) ) put(g, y, x, WHITE);
  };
  shard([[28, 92], [40, 78], [46, 112], [34, 122]], 1);
  shard([[214, 84], [224, 74], [232, 98], [220, 110]], 2);
  shard([[22, 170], [34, 160], [36, 182]], 3);
  shard([[222, 150], [238, 140], [236, 170], [226, 178]], 4);
  shard([[70, 28], [80, 18], [84, 34]], 5);

  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M0-灯里の歪み", g)]; })();
