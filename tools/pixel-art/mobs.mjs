// 64×64 の雑魚の敵4体（こうもり・虫・結晶・しずく）。2026-10-03の「ドット絵の練習」の成果。
// 練習で意識したこと（docs/design/pixel-art-notes.md の A〜C）:
//   ・光源は左上の1つ。影は右下に寄せ、ピロー陰影（輪郭沿いにぐるり）は避ける
//   ・ランプ（暗→明）は、影を青紫寄り・光を黄寄りへ色相をずらす（実行時に zone の色相から作る。`src/game/art/mob-palette.ts`）
//   ・輪郭は1ドット。孤立した点は目のハイライトなど意図したものだけ
//   ・目は白＋瞳＋1ドットの照り。顔を読ませる
// 色番号: 0縁 1-5本体(暗→明) 6-8差し色(暗→明。腹・核・膜) 9目の白 10瞳 11影 12照り
// 既存作品のモンスターの姿・名前は参考にしていない（CLAUDE.md 1-1）。
import { makeGrid, hash, putNative } from "./lib.mjs";

const hsl = (h, s, l) => {
  h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
  const a = s * Math.min(l, 1 - l), f = (n) => { const k = (n + h / 30) % 12; return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)); };
  return "#" + [f(0), f(8), f(4)].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
};
/** プレビュー用の色（ゲームでは zone の色相で作り直す）。 */
export const previewPalette = (hue) => {
  const body = [[-24, 38, 13], [-14, 40, 24], [0, 42, 36], [8, 44, 50], [18, 46, 66]];
  const acc = [[-20, 60, 30], [10, 70, 50], [26, 80, 72]];
  return [["縁", hsl(hue - 30, 40, 6)],
    ...body.map(([dh, s, l], i) => [`本体${i + 1}`, hsl(hue + dh, s, l)]),
    ...acc.map(([dh, s, l], i) => [`差し色${i + 1}`, hsl(hue + 150 + dh, s, l)]),
    ["目の白", "#f4f8ff"], ["瞳", "#1a1030"], ["影", hsl(hue - 30, 30, 10)], ["照り", "#ffffff"]];
};
const px = (g, r, c, k) => putNative(g, Math.round(r), Math.round(c), k);
const get = (g, r, c) => g[r]?.[c] ?? -1;

/** 多角形（点は [x,y]）を塗る。fn(r,c) が色番号を返す。 */
function poly(g, pts, fn) {
  const ys = pts.map((p) => p[1]);
  for (let r = Math.floor(Math.min(...ys)); r <= Math.ceil(Math.max(...ys)); r++) for (let c = 0; c < 64; c++) {
    let inside = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      const [xi, yi] = pts[i], [xj, yj] = pts[j];
      if ((yi > r + 0.5) !== (yj > r + 0.5) && c + 0.5 < ((xj - xi) * (r + 0.5 - yi)) / (yj - yi) + xi) inside = !inside;
    }
    if (inside) { const k = fn(r, c); if (k !== null) px(g, r, c, k); }
  }
}
/** 楕円体（左上から光）。階調は ramp の番号の配列（暗→明）。 */
function ball(g, cx, cy, rx, ry, ramp, jit = 0.06) {
  for (let r = Math.floor(cy - ry); r <= Math.ceil(cy + ry); r++) for (let c = Math.floor(cx - rx); c <= Math.ceil(cx + rx); c++) {
    const nx = (c + 0.5 - cx) / rx, ny = (r + 0.5 - cy) / ry, d = nx * nx + ny * ny;
    if (d > 1) continue;
    const lum = -nx * 0.55 - ny * 0.7 + Math.sqrt(1 - d) * 0.45;
    let t = Math.floor(Math.max(0, Math.min(0.999, (lum + 0.2) / 1.1)) * ramp.length);
    if (hash(c, r) < jit) t += hash(r, c) < 0.5 ? -1 : 1;
    px(g, r, c, ramp[Math.max(0, Math.min(ramp.length - 1, t))]);
  }
}
const BODY = [1, 2, 3, 4, 5], ACC = [6, 7, 8];
/** 外周の縁取り（影・照りは対象外）。 */
function edge(g, skip = [11]) {
  const has = (r, c) => get(g, r, c) !== -1 && !skip.includes(get(g, r, c));
  const add = [];
  for (let r = 0; r < 64; r++) for (let c = 0; c < 64; c++) if ((get(g, r, c) === -1 || skip.includes(get(g, r, c))) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
  for (const [r, c] of add) px(g, r, c, 0);
}
/** 地面の影（細い楕円。縁取りの対象にしない）。 */
function shadow(g, cx, cy, rx, ry) {
  for (let r = cy - ry; r <= cy + ry; r++) for (let c = cx - rx; c <= cx + rx; c++) {
    const d = ((c - cx) / rx) ** 2 + ((r - cy) / ry) ** 2;
    if (d <= 1 && get(g, r, c) === -1 && (d < 0.55 || (r + c) % 2 === 0)) px(g, r, c, 11);
  }
}
/** 目: 白＋瞳＋照り。w×h。瞳は dx だけ寄せる（視線）。 */
function eye(g, cx, cy, w, h, dx = 0) {
  for (let r = 0; r < h; r++) for (let c = 0; c < w; c++) {
    const nx = (c + 0.5 - w / 2) / (w / 2), ny = (r + 0.5 - h / 2) / (h / 2);
    if (nx * nx + ny * ny <= 1.05) px(g, cy + r, cx + c, 9);
  }
  const pw = Math.max(2, Math.round(w / 2)), ph = Math.max(2, Math.round(h * 0.7));
  for (let r = 0; r < ph; r++) for (let c = 0; c < pw; c++) px(g, cy + Math.round((h - ph) / 2) + r, cx + Math.round((w - pw) / 2) + dx + c, 10);
  px(g, cy + Math.round((h - ph) / 2), cx + Math.round((w - pw) / 2) + dx, 12);
}

// 1. こうもり: 小さな体に大きな膜の翼。翼は骨の筋（暗）と膜（差し色）で、下の縁はスカラップ
function bat() {
  const g = makeGrid();
  const wing = (dir) => {
    const x0 = 32 + dir * 6;
    const tips = [[32 + dir * 29, 14], [32 + dir * 27, 30], [32 + dir * 19, 41]];
    const bottom = [[x0, 40], [32 + dir * 12, 47], [32 + dir * 17, 42], [32 + dir * 22, 46], [32 + dir * 25, 38]];
    const pts = [[x0, 28], tips[0], [32 + dir * 22, 22], tips[1], [32 + dir * 24, 33], ...bottom.slice(3).reverse(), [32 + dir * 17, 42], [32 + dir * 12, 47], [x0, 40]];
    poly(g, pts, (r, c) => {
      const t = (r - 14) / 33, near = Math.abs(c - 32) / 29;
      let k = near < 0.35 ? 7 : t > 0.55 ? 6 : 7;
      if (dir < 0 && near > 0.5 && t < 0.3) k = 8;
      if (dir > 0 && near < 0.5 && t > 0.6) k = 6;
      return k;
    });
    // 翼の骨（腕から指先へ細い暗線）
    const bone = (xa, ya, xb, yb) => { const n = Math.max(Math.abs(xb - xa), Math.abs(yb - ya)); for (let i = 0; i <= n; i++) px(g, ya + ((yb - ya) * i) / n, xa + ((xb - xa) * i) / n, 2); };
    bone(x0, 29, tips[0][0], tips[0][1] + 1); bone(x0, 31, tips[1][0] - dir * 1, tips[1][1] + 1); bone(x0, 34, 32 + dir * 18, 41);
    // 翼の先の爪（明るい1ドット）
    px(g, tips[0][1] - 1, tips[0][0] - dir * 0, 5);
  };
  wing(-1); wing(1);
  ball(g, 32, 35, 8, 10, BODY);
  ball(g, 32, 30, 4.5, 4, ACC);                                                  // 胸の毛並み（明るい差し色）
  ball(g, 32, 22, 8, 7, BODY);                                                   // 頭
  // 耳（先の尖った三角）
  poly(g, [[25, 19], [24, 9], [30, 16]], (r, c) => (c < 27 ? 2 : 3));
  poly(g, [[39, 19], [40, 9], [34, 16]], (r, c) => (c > 37 ? 2 : 3));
  poly(g, [[26, 17], [25, 12], [28, 16]], () => 7); poly(g, [[38, 17], [39, 12], [36, 16]], () => 7);
  eye(g, 27, 19, 4, 4, 1); eye(g, 33, 19, 4, 4, -1);
  px(g, 25, 31, 10); px(g, 25, 33, 10);                                          // 鼻
  px(g, 27, 29, 9); px(g, 27, 35, 9); px(g, 28, 29, 9); px(g, 28, 35, 9);        // 牙
  for (const dx of [-3, 3]) { px(g, 45, 32 + dx, 3); px(g, 46, 32 + dx, 2); }    // 足
  edge(g, [11]);
  return g;
}

// 2. 虫: 丸い甲羅（背の割れ目と節の模様）、頭の大あご、六本の脚と二本の触角
function beetle() {
  const g = makeGrid();
  shadow(g, 32, 53, 21, 3);
  const leg = (x, y, dx, bend) => {
    let cx = x, cy = y;
    const path = [[cx + dx * 4, cy - 1], [cx + dx * 8, cy + bend], [cx + dx * 9, cy + 7 + bend]];
    for (const [tx, ty] of path) { const n = Math.max(Math.abs(tx - cx), Math.abs(ty - cy)); for (let i = 1; i <= n; i++) { px(g, cy + ((ty - cy) * i) / n, cx + ((tx - cx) * i) / n, 1); px(g, cy + ((ty - cy) * i) / n + 1, cx + ((tx - cx) * i) / n, 0); } cx = tx; cy = ty; }
    px(g, cy + 1, cx + dx, 0);
  };
  for (const [y, b] of [[38, -4], [43, -1], [47, 1]]) { leg(24, y, -1, b); leg(40, y, 1, b); }
  ball(g, 32, 40, 17, 13, BODY, 0.04);                                           // 甲羅
  // 甲羅の割れ目（中央の暗線）と節の線
  for (let r = 28; r < 53; r++) px(g, r, 31.5 + (r > 40 ? 0 : 0), 1);
  for (let r = 29; r < 52; r++) if (get(g, r, 31) !== -1) { px(g, r, 31, 1); px(g, r, 32, 2); }
  for (const [y, w] of [[35, 12], [42, 15], [48, 12]]) for (let c = 32 - w; c <= 32 + w; c++) if ((c + y) % 3 !== 0 && get(g, y, c) !== -1 && Math.abs(c - 32) > 1) px(g, y, c, Math.max(1, get(g, y, c) - 1));
  // 甲羅のつやの照り（左上の小さな明るい斜めの線）
  for (let i = 0; i < 6; i++) px(g, 31 + i * 0.6, 22 + i * 1.2, 5);
  px(g, 30, 21, 12); px(g, 30, 22, 12);
  ball(g, 32, 24, 8, 6, BODY);                                                   // 頭
  poly(g, [[25, 28], [22, 31], [27, 30]], () => 8); poly(g, [[39, 28], [42, 31], [37, 30]], () => 8); // 大あご
  eye(g, 26, 21, 4, 4); eye(g, 34, 21, 4, 4);
  for (const dx of [-1, 1]) { let x = 32 + dx * 4, y = 19; for (let i = 0; i < 7; i++) { px(g, y, x, 1); x += dx * (i < 3 ? 1 : 0.7); y -= 1.2; } px(g, y, x, 8); px(g, y - 1, x, 8); }
  edge(g);
  return g;
}

// 3. 結晶: 面ごとに明るさの違う多角形（左上の面が明るく、右下の面が暗い）。中心の核が光り、目は核の中に
function shard() {
  const g = makeGrid();
  shadow(g, 32, 56, 18, 3);
  const top = [32, 5], L = [14, 24], R = [50, 27], lb = [19, 50], rb = [46, 51], bot = [32, 57], mid = [32, 30];
  const face = (pts, tone) => poly(g, pts, (r, c) => BODY[Math.max(0, Math.min(4, tone + (hash(c, r) < 0.05 ? 1 : 0)))]);
  face([top, L, mid], 4);          // 左上の面（いちばん明るい）
  face([top, mid, R], 3);          // 右上の面
  face([L, mid, lb], 2);           // 左下の面
  face([R, rb, mid], 1);           // 右下の面（暗い）
  face([mid, lb, bot], 2); face([mid, bot, rb], 0);
  // 小さな衛星の結晶（左右）
  poly(g, [[8, 38], [12, 30], [17, 40], [13, 49]], (r, c) => BODY[c < 12 ? 3 : 1]);
  poly(g, [[55, 39], [51, 33], [47, 42], [52, 50]], (r, c) => BODY[c < 51 ? 2 : 0]);
  // 面の境目に細い明るい稜線（左上の辺だけ）
  const line = (a, b, k) => { const n = Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])); for (let i = 0; i <= n; i++) px(g, a[1] + ((b[1] - a[1]) * i) / n, a[0] + ((b[0] - a[0]) * i) / n, k); };
  line([top[0] + 0, top[1] + 1], [L[0] + 2, L[1] - 1], 5); line([top[0] + 1, top[1] + 2], [32, 12], 5);
  // 核（中心のひし形）と目
  poly(g, [[32, 21], [40, 32], [32, 43], [24, 32]], (r, c) => { const d = Math.abs(c + 0.5 - 32) / 8 + Math.abs(r + 0.5 - 32) / 11; return d < 0.45 ? 8 : d < 0.8 ? 7 : 6; });
  eye(g, 27, 28, 4, 5, 1); eye(g, 33, 28, 4, 5, -1);
  px(g, 34, 31, 10); px(g, 34, 32, 10); px(g, 35, 32, 10);                      // 口
  edge(g);
  return g;
}

// 4. しずく（水の玉）: 球の体に、ひとつだけの大きな目。下は水たまりにつながり、ぽたぽたと落ちる。
//    ※ 涙形に笑った顔の「ゼリー」は有名作品のモンスターに似るので、あえて涙形・笑顔・口を避け、球＋単眼＋水たまりにした（CLAUDE.md 1-1）
function drop() {
  const g = makeGrid();
  // 水たまり（下の楕円。縁は明るく、中は暗い）
  for (let r = 48; r <= 58; r++) for (let c = 6; c <= 58; c++) {
    const nx = (c + 0.5 - 32) / 26, ny = (r + 0.5 - 53) / 5, d = nx * nx + ny * ny;
    if (d > 1) continue;
    px(g, r, c, d > 0.78 ? BODY[3] : d > 0.4 ? BODY[2] : BODY[1]);
  }
  for (const [x, y] of [[14, 52], [18, 55], [47, 51], [41, 56]]) px(g, y, x, BODY[4]);   // 水たまりのきらめき
  // 体の球: 左上が明るく、下は水たまりへ溶ける
  ball(g, 32, 29, 20, 21, BODY, 0.05);
  // 球の中の「光だまり」（右下の内側がやや明るい＝水越しに光が抜ける）
  for (let r = 30; r < 48; r++) for (let c = 30; c < 50; c++) {
    const nx = (c + 0.5 - 40) / 8, ny = (r + 0.5 - 40) / 8;
    if (nx * nx + ny * ny < 1 && get(g, r, c) !== -1 && get(g, r, c) <= 3 && (r + c) % 2 === 0) px(g, r, c, get(g, r, c) + 1);
  }
  // 大きな照り（左上の弧）と小さな照り
  for (let i = 0; i < 10; i++) { const a = 3.45 + i * 0.12; px(g, 29 + Math.sin(a) * 15, 31 + Math.cos(a) * 15, 12); }
  px(g, 17, 22, 12); px(g, 18, 22, 12); px(g, 19, 21, 12);
  // 体の中の泡（本体の明るい色）
  for (const [bx, by, br] of [[41, 40, 2], [24, 41, 1.5], [44, 32, 1]]) { for (let r = -br; r <= br; r++) for (let c = -br; c <= br; c++) if (r * r + c * c <= br * br + 0.5) px(g, by + r, bx + c, BODY[4]); px(g, by - br + 0.5, bx - br + 0.5, 12); }
  // 単眼
  eye(g, 25, 25, 12, 11, 1);
  // 落ちるしずく（球の下の左右に、小さな涙形が2つ）
  for (const [dx, dy] of [[12, 44], [54, 40]]) { for (let i = 0; i < 6; i++) { const w = i < 2 ? 0 : i < 4 ? 1 : 2; for (let c = -w; c <= w; c++) px(g, dy + i, dx + c, BODY[i < 3 ? 3 : 2]); } px(g, dy + 1, dx - 1, 12); }
  edge(g, [11]);
  return g;
}

export const PIECES = [
  { name: "MB1-こうもり", pal: previewPalette(262), build: bat },
  { name: "MB2-虫", pal: previewPalette(28), build: beetle },
  { name: "MB3-結晶", pal: previewPalette(190), build: shard },
  { name: "MB4-しずく", pal: previewPalette(150), build: drop },
];
