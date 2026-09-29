// 128×128 の地形（フィールド用）。継ぎ目なく並べられるよう、乱数は端でつながる（回り込む）作りにしてある。
// 参考にしたのは「質の要素」（多段階の明暗・密な模様・縁取り・小物）で、特定作品の絵そのものは写していない。
import { N, hash, makeGrid, putNative } from "./lib.mjs";

const W = 128;
const wrap = (v) => ((Math.round(v) % W) + W) % W;
const px = (g, r, c, k) => putNative(g, wrap(r), wrap(c), k);
/** 回り込む値ノイズ（周期 period マスでつながる）。 */
function vn(x, y, s, seed = 0, sy = s) {
  const per = W / s, perY = W / sy;
  const fx = x / s, fy = y / sy, ix = Math.floor(fx), iy = Math.floor(fy);
  const ax = fx - ix, ay = fy - iy;
  const f = (t) => t * t * (3 - 2 * t);
  const v = (i, j) => hash(((i % per) + per) % per + seed * 131, ((j % perY) + perY) % perY + seed * 71);
  const a = v(ix, iy), b = v(ix + 1, iy), c = v(ix, iy + 1), d = v(ix + 1, iy + 1);
  return (a * (1 - f(ax)) + b * f(ax)) * (1 - f(ay)) + (c * (1 - f(ax)) + d * f(ax)) * f(ay);
}
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// ---------- 草地 ----------
const grass = () => {
  const g = makeGrid();
  // pal: 0暗い影 1-5緑(暗→明) 6花桃 7花黄 8花白 9花紫 10土 11葉先の黄
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    const zone = vn(c, r, 32, 1) * 0.6 + vn(c, r, 12, 2) * 0.3 + vn(c, r, 5, 3) * 0.1;
    let t = clamp(Math.floor(zone * 5.2) + 0, 0, 4);          // 0..4 → 緑1〜5
    if (hash(c, r) < 0.12) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 4);
    g[r][c] = 1 + t;
  }
  // 草の房（ハの字。根もとは暗く、先は明るく）
  for (let n = 0; n < 420; n++) {
    const c = Math.floor(hash(n, 1) * W), r = Math.floor(hash(n, 2) * W), h = 3 + Math.floor(hash(n, 3) * 4);
    const lean = hash(n, 4) < 0.5 ? -1 : 1;
    for (let i = 0; i < h; i++) {
      const k = i === 0 ? 1 : i < h - 1 ? 3 : 5;
      px(g, r - i, c + Math.round(lean * i * 0.4), k + (hash(n, i + 5) < 0.3 ? 0 : 0));
      if (i > 0 && i < h) px(g, r - i, c - lean * Math.min(1, i), i === h - 1 ? 5 : 4);
    }
  }
  // 明るい葉先の点（日なた）
  for (let n = 0; n < 260; n++) { const c = Math.floor(hash(n, 21) * W), r = Math.floor(hash(n, 22) * W); if (vn(c, r, 32, 1) > 0.5) px(g, r, c, 11); }
  // 花（4〜5マスの小さな花。まとまって咲く）
  for (let m = 0; m < 9; m++) {
    const cx = hash(m, 31) * W, cy = hash(m, 32) * W, col = 6 + (m % 4);
    for (let i = 0; i < 6; i++) {
      const c = cx + (hash(m, 40 + i) - 0.5) * 16, r = cy + (hash(m, 50 + i) - 0.5) * 12;
      px(g, r, c, col); px(g, r, c + 1, col); px(g, r - 1, c, col); px(g, r + 1, c, col); px(g, r, c - 1, col); px(g, r, c, 7);
      px(g, r + 2, c, 2); px(g, r + 3, c, 1);
    }
  }
  return g;
};
const grassPal = [["影", "#0f2e12"], ["草1", "#1b4d1a"], ["草2", "#2a7222"], ["草3", "#3f9a2a"], ["草4", "#6ec238"], ["草5", "#a6e050"], ["花桃", "#ff86a4"], ["花黄", "#ffe25a"], ["花白", "#ffffff"], ["花紫", "#b48cff"], ["土", "#7a4a24"], ["葉先", "#d8f47a"]];

// ---------- 土の道 ----------
const dirt = () => {
  const g = makeGrid();
  // pal: 0暗い割れ目 1-5土(暗→明) 6石暗 7石 8石明
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    const z = vn(c, r, 24, 4) * 0.55 + vn(c, r, 9, 5) * 0.3 + vn(c, r, 4, 6) * 0.15;
    let t = clamp(Math.floor(z * 5.2), 0, 4);
    if (hash(c, r) < 0.16) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 4);
    g[r][c] = 1 + t;
  }
  // 踏み固めた跡の筋
  for (let n = 0; n < 5; n++) { let r = Math.floor(hash(n, 60) * W), c = Math.floor(hash(n, 61) * W); for (let i = 0; i < 70; i++) { c += 1; r += Math.round((hash(n, 100 + i) - 0.5) * 1.4); px(g, r, c, 1); if (hash(n, 200 + i) < 0.6) px(g, r + 1, c, 2); } }
  // 割れ目
  for (let n = 0; n < 7; n++) { let r = hash(n, 70) * W, c = hash(n, 71) * W; const dir = hash(n, 72) * 6.28; for (let i = 0; i < 22; i++) { r += Math.sin(dir + hash(n, 300 + i) - 0.5) * 1.2; c += Math.cos(dir + hash(n, 300 + i) - 0.5) * 1.2; px(g, r, c, 0); } }
  // 小石（上が明るく、下が暗い）
  for (let n = 0; n < 34; n++) {
    const cx = hash(n, 80) * W, cy = hash(n, 81) * W, rx = 2.5 + hash(n, 82) * 4, ry = rx * (0.6 + hash(n, 83) * 0.25);
    for (let r = -ry - 1; r <= ry + 1; r++) for (let c = -rx - 1; c <= rx + 1; c++) {
      const d = (c / rx) ** 2 + (r / ry) ** 2; if (d > 1) continue;
      px(g, cy + r, cx + c, d > 0.8 ? 6 : r < -ry * 0.2 ? 8 : r < ry * 0.4 ? 7 : 6);
    }
    px(g, cy + ry + 1, cx + 1, 0); px(g, cy + ry + 1, cx + 2, 0);
  }
  return g;
};
const dirtPal = [["割れ目", "#2e1a0e"], ["土1", "#4a3626"], ["土2", "#6a4c32"], ["土3", "#8c6a44"], ["土4", "#ae8a58"], ["土5", "#cfad78"], ["石暗", "#5e5a56"], ["石", "#8f8a82"], ["石明", "#c2bdb2"]];

// ---------- 水面（川） ----------
const water = () => {
  const g = makeGrid();
  // pal: 0深い 1-5水(暗→明) 6泡白 7石影 8石
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    const flow = vn(c, r, 8, 7, 24) * 0.55 + vn(c, r, 16, 8, 40) * 0.3 + vn(c, r, 4, 9, 8) * 0.15;   // 縦に長い流れの筋
    let t = clamp(Math.floor(Math.pow(flow, 1.5) * 5.8), 0, 4);
    // うろこ状の波紋
    const sc = ((c >> 1) + (((r >> 2) & 1) * 1) + (r >> 3)) % 4;
    if (sc === 0 && t < 3) t += 1; else if (sc === 2 && t > 0 && hash(c, r) < 0.6) t -= 1;
    if (hash(c + 7, r + 3) < 0.10) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 4);
    g[r][c] = 1 + t;
  }
  // 川底の石（暗く沈んで見える）
  for (let n = 0; n < 14; n++) { const cx = hash(n, 90) * W, cy = hash(n, 91) * W, rx = 3 + hash(n, 92) * 5, ry = 2 + hash(n, 93) * 3; for (let r = -ry; r <= ry; r++) for (let c = -rx; c <= rx; c++) { if ((c / rx) ** 2 + (r / ry) ** 2 <= 1) px(g, cy + r, cx + c, 1); } }
  // 波の白いきらめき（十字と短い横線）
  for (let n = 0; n < 60; n++) { const c = hash(n, 95) * W, r = hash(n, 96) * W; px(g, r, c, 6); if (n % 3 === 0) { px(g, r, c + 1, 5); px(g, r, c - 1, 5); px(g, r - 1, c, 5); } else px(g, r, c + 1, 5); }
  return g;
};
const waterPal = [["深い", "#04182c"], ["水1", "#0a3352"], ["水2", "#115a7a"], ["水3", "#1f8496"], ["水4", "#3fb0b4"], ["水5", "#9fe4dc"], ["泡", "#ffffff"], ["石影", "#1a2830"], ["石", "#4a6068"]];

// ---------- 崖の壁 ----------
const cliff = () => {
  const g = makeGrid();
  // pal: 0割れ目 1-5岩(暗→明) 6苔暗 7苔 8苔明 9上端の草
  const R = [1, 2, 3, 4, 5];
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    const strata = Math.sin(r / 5.5 + vn(c, r, 18, 10, 30) * 4) * 0.5 + 0.5;     // 波打つ地層
    const z = strata * 0.5 + vn(c, r, 10, 11, 6) * 0.35 + vn(c, r, 4, 12) * 0.15;
    let t = clamp(Math.floor(z * 5.2), 0, 4);
    if (hash(c, r) < 0.12) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 4);
    g[r][c] = R[t];
  }
  // 岩のかたまり（上左が明るく、下右が暗い。縁に暗い線）
  for (let n = 0; n < 60; n++) {
    const cx = hash(n, 110) * W, cy = 10 + hash(n, 111) * (W - 20), rx = 6 + hash(n, 112) * 9, ry = 4 + hash(n, 113) * 6;
    for (let r = -ry; r <= ry; r++) for (let c = -rx; c <= rx; c++) {
      const d = (c / rx) ** 2 + (r / ry) ** 2; if (d > 1) continue;
      const light = -(c / rx) * 0.5 - (r / ry) * 0.8;
      let t = light > 0.45 ? 4 : light > 0.05 ? 3 : light > -0.35 ? 2 : 1;
      if (d > 0.82) t = light < 0 ? 0 : Math.max(1, t - 1);
      px(g, cy + r, cx + c, t === 0 ? 0 : R[t]);
    }
  }
  // 縦の割れ目
  for (let n = 0; n < 16; n++) { let c = hash(n, 120) * W, r = hash(n, 121) * (W - 30); for (let i = 0; i < 26; i++) { r += 1; c += (hash(n, 400 + i) - 0.5) * 1.6; px(g, r, c, 0); if (hash(n, 500 + i) < 0.4) px(g, r, c + 1, 1); } }
  // 上端の明るい縁と草のひさし、下端の暗い影、苔
  for (let c = 0; c < W; c++) {
    for (let r = 0; r < 4; r++) g[r][c] = r === 0 ? 4 : r === 1 ? 5 : r === 2 ? 4 : 3;
    const gh = 3 + Math.floor(hash(c, 130) * 4); for (let r = 0; r < gh - 3; r++) g[r][c] = 9;
    for (let r = W - 6; r < W; r++) g[r][c] = r > W - 3 ? 0 : hash(c, r) < 0.5 ? 1 : 2;
  }
  for (let n = 0; n < 90; n++) { const c = hash(n, 140) * W, r = 4 + hash(n, 141) * 40; const k = 6 + Math.floor(hash(n, 142) * 3); px(g, r, c, k); px(g, r, c + 1, k); px(g, r + 1, c, 6); }
  return g;
};
const cliffPal = [["割れ目", "#2e150e"], ["岩1", "#5a2c1a"], ["岩2", "#8a4526"], ["岩3", "#b26433"], ["岩4", "#d98e4c"], ["岩5", "#f0b96a"], ["苔暗", "#245a1c"], ["苔", "#3f8f2a"], ["苔明", "#7fcb35"], ["草", "#4fa32c"]];

// ---------- 深い森の樹冠 ----------
const forest = () => {
  const g = makeGrid();
  // pal: 0影 1-5葉(暗→明) 6光
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) { g[r][c] = vn(c, r, 8, 19) < 0.55 ? 0 : 1; }
  const blobs = [];
  for (let n = 0; n < 70; n++) blobs.push([hash(n, 150) * W, hash(n, 151) * W, 7 + hash(n, 152) * 8]);
  blobs.sort((a, b) => a[1] - b[1]);
  for (const [cx, cy, R] of blobs) for (let r = -R; r <= R; r++) for (let c = -R; c <= R; c++) {
    const d = (c * c + r * r) / (R * R); if (d > 1) continue;
    const light = (-c * 0.6 - r * 0.8) / R;
    let t = light > 0.5 ? 5 : light > 0.15 ? 4 : light > -0.25 ? 3 : light > -0.6 ? 2 : 1;
    if (d > 0.8 && light < 0.1) t = Math.max(1, t - 1);
    if (d > 0.92) t = 0;
    if (hash(cx + c, cy + r) < 0.16) t = clamp(t + (hash(cy + r, cx + c) < 0.5 ? -1 : 1), 0, 5);
    if (d < 0.35 && light > 0.3 && hash(c, r + cx) < 0.2) t = 6;
    px(g, cy + r, cx + c, t === 0 ? 0 : t);
  }
  return g;
};
const forestPal = [["影", "#08170e"], ["葉1", "#0f3a1a"], ["葉2", "#1b5a22"], ["葉3", "#2c7f2a"], ["葉4", "#4fa833"], ["葉5", "#86cc44"], ["光", "#cdee6c"]];

// ---------- 岸辺（草→岸の石→水） ----------
const bank = () => {
  const g = makeGrid();
  // pal: 0縁 1-5草 6-10岸石(暗→明) 11-14水 15泡
  const edge = (c) => 44 + Math.sin(c / 9) * 5 + vn(c, 0, 16, 13) * 8;      // 草と岸の境
  const shore = (c) => 74 + Math.sin(c / 11 + 2) * 4 + vn(c, 0, 12, 14) * 6; // 岸と水の境
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    const e = edge(c), s = shore(c);
    if (r < e) { const z = vn(c, r, 20, 15) * 0.6 + vn(c, r, 6, 16) * 0.4; let t = clamp(Math.floor(z * 4.6), 0, 3); if (hash(c, r) < 0.13) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 3); g[r][c] = 1 + t; if (hash(c + 5, r) < 0.02) g[r][c] = 5; }
    else if (r < s) { g[r][c] = 6; }
    else { const z = vn(c, r, 7, 17, 22) * 0.6 + vn(c, r, 4, 18) * 0.4; let t = clamp(Math.floor(z * 3.6), 0, 3); if (hash(c, r) < 0.1) t = clamp(t + (hash(r, c) < 0.5 ? -1 : 1), 0, 3); g[r][c] = 11 + t; }
  }
  // 岸の石（丸い石を並べる。明るい上面・暗い下面・縁取り）
  for (let n = 0; n < 130; n++) {
    const cx = hash(n, 160) * W, t0 = hash(n, 161), rx = 5 + hash(n, 162) * 5, ry = 3.5 + hash(n, 163) * 3;
    const cy = edge(cx) + 4 + t0 * (shore(cx) - edge(cx) - 6);
    for (let r = -ry; r <= ry; r++) for (let c = -rx; c <= rx; c++) {
      const d = (c / rx) ** 2 + (r / ry) ** 2; if (d > 1) continue;
      const light = -(c / rx) * 0.5 - (r / ry) * 0.8;
      let k = light > 0.4 ? 10 : light > 0.0 ? 9 : light > -0.4 ? 8 : 7;
      if (d > 0.78) k = light > 0 ? 8 : 6;
      if (d > 0.93) k = 0;
      px(g, cy + r, cx + c, k);
    }
  }
  // 草が岸にかぶさる
  for (let c = 0; c < W; c++) { const e = Math.floor(edge(c)); for (let i = 0; i < 3; i++) if (hash(c, i + 300) < 0.6) px(g, e + i, c, 2 + (i % 2)); }
  // 水際の泡
  for (let c = 0; c < W; c++) { const s = Math.floor(shore(c)); for (let i = 0; i < 3; i++) if (hash(c, i + 400) < 0.7 - i * 0.2) px(g, s + i, c, 15); }
  return g;
};
const bankPal = [["縁", "#1a1010"], ["草1", "#1b4d1a"], ["草2", "#2a7222"], ["草3", "#3f9a2a"], ["草4", "#6ec238"], ["草5", "#a6e050"], ["岸石1", "#4a2a1a"], ["岸石2", "#7a4a2c"], ["岸石3", "#a86a3c"], ["岸石4", "#d08c50"], ["岸石5", "#f0b878"], ["水1", "#0c3f63"], ["水2", "#14688c"], ["水3", "#2792a8"], ["水4", "#54c0c4"], ["泡", "#ffffff"]];

export const PIECES = [
  { name: "T1-草地", pal: grassPal, build: grass },
  { name: "T2-土の道", pal: dirtPal, build: dirt },
  { name: "T3-水面", pal: waterPal, build: water },
  { name: "T4-崖の壁", pal: cliffPal, build: cliff },
  { name: "T5-深い森", pal: forestPal, build: forest },
  { name: "T6-岸辺", pal: bankPal, build: bank },
];
