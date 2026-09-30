// 256×256 の「8神」と、ダンジョンの中ボス5体。bosses.mjs の描画部品（楕円体の陰影・触手・牙・光輪など）を使い回し、
// 神ごとに形（女神=翼と光輪、蟲神=羽と複眼、鬼神=角と牙、無神=空洞、純神=結晶、武神=大剣、異神=二つの顔、冥神=大鐘）を変えてある。
// 既存作品のモンスターの姿・名前は参考にしていない（CLAUDE.md 1-1）。
import { hash, makeGrid } from "./lib.mjs";
import { ell, taper, curve, fang, eye, halo, shard, miasma, outlineAll, rimLight, shadowUnder, toneIdx, px } from "./bosses.mjs";

/** 色相から、暗→明の階調を作る。 */
function hsl(h, s, l) {
  h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
  const a = s * Math.min(l, 1 - l), f = (n) => { const k = (n + h / 30) % 12; return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)); };
  return "#" + [f(0), f(8), f(4)].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
}
/** パレット: 0縁 1-5本体 6-8差し色 9-12骨・金属 13闇 14白 15-17目 18影 19-20もや 21-23光輪 */
function palette(hue, acc, sat = 45) {
  return [["縁", "#05030a"],
    ...[14, 26, 40, 54, 70].map((l, i) => [`本体${i + 1}`, hsl(hue, sat, l)]),
    ...[30, 52, 76].map((l, i) => [`差し色${i + 1}`, hsl(acc, 80, l)]),
    ...[30, 48, 66, 82].map((l, i) => [`骨${i + 1}`, hsl(hue + 20, 14, l)]),
    ["闇", "#020104"], ["白", "#fffdf0"],
    ...[35, 55, 78].map((l, i) => [`目${i + 1}`, hsl(acc, 95, l)]),
    ["影", "#0c0a14"], ["もや暗", hsl(hue, 30, 12)], ["もや", hsl(hue, 35, 22)],
    ...[16, 34, 62].map((l, i) => [`光輪${i + 1}`, hsl(acc, 60, l)])];
}
const BODY = [1, 2, 3, 4, 5], ACC = [6, 7, 8], BONE = [9, 10, 11, 12], GLOW = [15, 16, 17], HALO = [21, 22, 23];
const skin = (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BODY[toneIdx(5, lum, c, r, 0.12)]);
const glowSkin = (r, c, nx, ny, d, lum) => (d > 0.88 ? 0 : ACC[toneIdx(3, lum, c, r, 0.1)]);
const bone = (r, c, nx, ny, d, lum) => (d > 0.88 ? 0 : BONE[toneIdx(4, lum, c, r, 0.08)]);
const SKIP = [18, 19, 20, 21, 22, 23];

function finish(g, mist = 10) {
  outlineAll(g, SKIP);
  rimLight(g, SKIP, ACC[1], 14);
  miasma(g, [19, 19, 20], mist, 0.6, SKIP);
  return g;
}
const base = (ringR = 104, cy = 116) => { const g = makeGrid(); shadowUnder(g, 128, 242, 92, 10, 18); halo(g, 128, cy, ringR, HALO); return g; };
const face = (g, cx, cy, rx, ry, eyes = 2, gap = 0.55) => {
  ell(g, cx, cy, rx, ry, skin);
  for (let i = 0; i < eyes; i++) { const t = eyes === 1 ? 0 : i / (eyes - 1) - 0.5; eye(g, Math.round(cx + t * rx * gap * 2), Math.round(cy - ry * 0.1), 8, 7, GLOW, t * 0.5); }
};
/** 下半身: ゆるやかに裾が広がる法衣（布のひだ）。 */
const robe = (g, cx, top, bot, wTop, wBot) => {
  for (let r = top; r <= bot; r++) {
    const t = (r - top) / (bot - top), w = wTop + (wBot - wTop) * t ** 1.4;
    for (let c = Math.round(cx - w); c <= Math.round(cx + w); c++) {
      const nx = (c - cx) / w, fold = Math.sin(nx * 9 + t * 2) * 0.12, lum = -nx * 0.55 - 0.1 + fold + (1 - t) * 0.15;
      px(g, r, c, Math.abs(nx) > 0.96 ? 0 : BODY[toneIdx(5, lum, c, r, 0.12)]);
    }
  }
};
const wing = (g, sx, dir, n, len, ramp) => {
  for (let i = 0; i < n; i++) {
    const a = -0.9 + i * (1.6 / Math.max(1, n - 1)), ex = sx + dir * Math.cos(a) * len, ey = 140 + Math.sin(a) * len * 0.9 - 40;
    taper(g, curve([sx, 136], [sx + dir * len * 0.45, 136 + Math.sin(a) * len * 0.3 - 40], [ex, ey]), 8, 1, ramp, 0);
  }
};

// 1. 女神「恵みの残照」: 光輪と六枚の翼、祈る姿。目を閉じた穏やかな顔だが、輪の内側は歪んでいる
const god1 = () => {
  const g = base(108, 100);
  wing(g, 100, -1, 4, 96, BONE); wing(g, 156, 1, 4, 96, BONE); wing(g, 104, -1, 3, 70, ACC); wing(g, 152, 1, 3, 70, ACC);
  robe(g, 128, 120, 238, 26, 70);
  for (const x of [-2, 2]) taper(g, curve([128 + x * 18, 130], [128 + x * 10, 160], [128 + x * 2, 176]), 10, 5, BODY, 0);
  face(g, 128, 82, 28, 32, 0);
  for (const dx of [-11, 11]) for (let i = -7; i <= 7; i++) px(g, 80 + Math.round(i * i / 14), 128 + dx + i, 0);          // 閉じた目
  eye(g, 128, 62, 6, 6, GLOW);                                                                                          // 額の第三の目だけが開く
  ell(g, 128, 160, 14, 14, (r, c, nx, ny, d) => (d > 0.8 ? 8 : 14));
  for (const [x, y, w, h] of [[40, 40, 6, 14], [216, 44, 6, 14], [30, 150, 5, 12], [228, 160, 5, 12]]) shard(g, x, y, w, h, ACC, 0);
  return finish(g);
};
// 2. 蟲神「理不尽の羽音」: 複眼の大きな頭と、四枚の透ける羽、節のある脚
const god2 = () => {
  const g = base(100, 120);
  for (const dir of [-1, 1]) for (const [dy, len] of [[-10, 112], [26, 96]]) taper(g, curve([128 + dir * 24, 120 + dy], [128 + dir * len * 0.6, 40 + dy], [128 + dir * len, 70 + dy + 30]), 14, 2, ACC, 0);
  ell(g, 128, 196, 44, 44, skin);
  for (let i = 0; i < 6; i++) ell(g, 128, 168 + i * 13, 40 - i * 3, 5, (r, c, nx, ny, d) => (d > 0.6 ? 0 : BODY[0]));
  for (const dir of [-1, 1]) for (const [sy, ex, ey] of [[170, 44, 226], [190, 36, 240], [150, 52, 200]]) taper(g, curve([128 + dir * 34, sy], [128 + dir * (128 - ex) * 0.9, sy - 30], [128 + dir * (128 - ex), ey]), 6, 2, BONE, 0);
  ell(g, 128, 122, 40, 36, skin);
  for (const dx of [-26, 26]) ell(g, 128 + dx, 98, 26, 30, (r, c, nx, ny, d, lum) => { if (d > 0.88) return 0; const cell = ((Math.floor(c / 5) + Math.floor(r / 5)) % 2); return GLOW[Math.min(2, toneIdx(3, lum, c, r, 0) + cell * 0)] === undefined ? 0 : (cell ? GLOW[toneIdx(3, lum, c, r, 0)] : ACC[toneIdx(3, lum, c, r, 0)]); });
  for (const dir of [-1, 1]) taper(g, curve([128 + dir * 12, 70], [128 + dir * 30, 30], [128 + dir * 54, 14]), 4, 1, BONE, 0);
  ell(g, 128, 138, 16, 9, (r, c, nx, ny, d) => (d > 0.7 ? 0 : 13));
  for (let i = -2; i <= 2; i++) fang(g, 128 + i * 6, 132, 5, 9, 1, BONE);
  return finish(g, 12);
};
// 3. 鬼神「坩堝の顎」: 炎の角、大きな顎、胸に燃える坩堝
const god3 = () => {
  const g = base(104, 110);
  for (const dir of [-1, 1]) taper(g, curve([128 + dir * 30, 60], [128 + dir * 62, 10], [128 + dir * 40, -8]), 12, 1, BONE, 0);
  for (const dir of [-1, 1]) ell(g, 128 + dir * 84, 150, 28, 50, skin);
  for (const dir of [-1, 1]) for (const dx of [-12, 0, 12]) taper(g, curve([128 + dir * 84 + dx, 190], [128 + dir * 90 + dx, 214], [128 + dir * 94 + dx * 1.3, 238]), 5, 1, BONE, 0);
  ell(g, 128, 168, 70, 76, skin);
  ell(g, 128, 168, 32, 34, (r, c, nx, ny, d) => (d > 0.85 ? 0 : d > 0.5 ? 6 : d > 0.25 ? 7 : 8));                        // 坩堝（胸の炉）
  for (let i = 0; i < 14; i++) taper(g, curve([100 + i * 4, 180], [96 + i * 5, 150 - (i % 3) * 12], [104 + i * 4, 122 - (i % 4) * 8]), 4, 1, [6, 7, 8], 6);
  ell(g, 128, 70, 42, 40, skin);
  ell(g, 128, 98, 40, 26, (r, c, nx, ny, d, lum) => (ny < -0.1 ? null : d > 0.85 ? 0 : d > 0.45 ? 13 : 13));                // 大きな顎の口
  for (let i = 0; i < 8; i++) { fang(g, 100 + i * 8, 86, 7, 14 + (i % 2) * 6, 1, BONE); fang(g, 104 + i * 8, 110, 7, 12 + (i % 2) * 5, -1, BONE); }
  eye(g, 108, 62, 9, 7, GLOW, -0.3); eye(g, 148, 62, 9, 7, GLOW, 0.3);
  return finish(g);
};
// 4. 無神「在らざる歌」: 輪郭だけの人影。中身は空洞で、浮かぶ音符のような光の粒が環をつくる
const god4 = () => {
  const g = base(100, 120);
  ell(g, 128, 150, 56, 96, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : d > 0.62 ? BODY[toneIdx(3, lum, c, r, 0.2)] : 13));
  ell(g, 128, 66, 30, 34, (r, c, nx, ny, d, lum) => (d > 0.88 ? 0 : d > 0.55 ? BODY[toneIdx(3, lum, c, r, 0.2)] : 13));
  ell(g, 128, 76, 10, 14, (r, c, nx, ny, d) => (d > 0.6 ? 0 : 13));                                                        // 歌う口だけが開く
  for (let i = 0; i < 40; i++) { const a = i / 40 * 6.2832 * 2, rr = 50 + i * 1.6; const x = 128 + Math.cos(a) * rr, y = 130 + Math.sin(a) * rr * 0.9 - 10; ell(g, x, y, 4, 4, (r, c, nx, ny, d) => (d > 0.55 ? ACC[1] : GLOW[2])); taper(g, [[x + 3, y], [x + 3, y - 12]], 1, 1, [ACC[1]], ACC[1]); }
  for (const [x, y] of [[112, 140], [144, 156], [124, 184], [136, 120]]) eye(g, x, y, 6, 5, GLOW, 0.2);
  return finish(g, 8);
};
// 5. 純神「透き徹る誓い」: 透明な結晶の巨体。内側に光の核が浮かぶ
const god5 = () => {
  const g = base(104, 120);
  for (const [x, y, w, h] of [[60, 170, 26, 66], [196, 170, 26, 66], [92, 180, 22, 56], [164, 180, 22, 56], [40, 120, 16, 40], [216, 120, 16, 40]]) shard(g, x, y, w, h, BODY.slice(2), 0);
  shard(g, 128, 150, 52, 100, BODY.slice(1, 5), 0);
  for (let i = 0; i < 7; i++) for (let r = 70 + i * 14; r < 92 + i * 14; r++) for (let c = 112 - (r - 70) % 11; c < 144; c += 12) if (hash(c, r) < 0.2) px(g, r, c, 14);   // 内側の面の反射
  ell(g, 128, 146, 22, 22, (r, c, nx, ny, d) => (d > 0.85 ? 8 : d > 0.55 ? 15 : d > 0.25 ? 16 : 17));                      // 光の核
  shard(g, 128, 54, 22, 30, BODY.slice(2), 0);
  eye(g, 118, 52, 7, 6, GLOW, -0.2); eye(g, 138, 52, 7, 6, GLOW, 0.2);
  for (const [x, y, w, h] of [[30, 40, 6, 14], [226, 50, 6, 14], [70, 20, 5, 11], [186, 18, 5, 11]]) shard(g, x, y, w, h, ACC, 0);
  return finish(g, 6);
};
// 6. 武神「不敗の咎人」: 鎧の巨人。背に無数の折れた剣。手には巨大な大剣
const god6 = () => {
  const g = base(104, 110);
  for (let i = 0; i < 11; i++) { const a = -2.6 + i * 0.26, x = 128 + Math.cos(a) * 86, y = 120 + Math.sin(a) * 86; taper(g, [[128 + Math.cos(a) * 40, 120 + Math.sin(a) * 40], [x, y]], 4, 1, BONE, 0); }
  ell(g, 128, 170, 60, 70, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.06)]));
  for (let i = 0; i < 6; i++) for (let c = 80; c < 176; c++) if (hash(c, i) < 0.002 || (c + i) % 12 === 0) for (let r = 120 + i * 20; r < 138 + i * 20; r++) px(g, r, c, 0);   // 板金の継ぎ目
  ell(g, 128, 72, 34, 38, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.06)]));
  for (let r = 70; r < 76; r++) for (let c = 100; c < 156; c++) px(g, r, c, 13);                                          // 兜の覗き穴
  eye(g, 112, 73, 8, 3, GLOW); eye(g, 144, 73, 8, 3, GLOW);
  for (const dx of [-14, 0, 14]) taper(g, curve([128 + dx, 36], [128 + dx * 1.6, 12], [128 + dx * 2.4, 0]), 5, 1, ACC, 0);   // 兜の飾り
  ell(g, 56, 150, 26, 60, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.06)]));
  taper(g, [[206, 60], [206, 210]], 10, 8, BONE, 0);                                                                     // 大剣
  for (let r = 60; r < 210; r++) px(g, r, 205, ACC[2]);
  ell(g, 206, 214, 26, 6, (r, c, nx, ny, d, lum) => (d > 0.85 ? 0 : ACC[toneIdx(3, lum, c, r, 0)]));
  return finish(g);
};
// 7. 異神「境界を見ぬ者」: 二つの顔が背中合わせにつながる。一方は笑い、一方は泣く
const god7 = () => {
  const g = base(104, 110);
  robe(g, 128, 130, 238, 40, 82);
  for (const dir of [-1, 1]) taper(g, curve([128 + dir * 40, 150], [128 + dir * 90, 180], [128 + dir * 98, 232]), 12, 3, BODY, 0);
  for (const dir of [-1, 1]) {
    const cx = 128 + dir * 34;
    ell(g, cx, 82, 32, 40, skin);
    eye(g, cx - 10, 76, 8, dir > 0 ? 4 : 8, GLOW, 0); eye(g, cx + 10, 76, 8, dir > 0 ? 4 : 8, GLOW, 0);
    if (dir > 0) { for (let i = -14; i <= 14; i++) px(g, 104 + Math.round(-i * i / 24) + 8, cx + i, 13); }                   // 笑う口
    else { for (let i = -14; i <= 14; i++) px(g, 110 + Math.round(i * i / 24), cx + i, 13); for (const x of [cx - 10, cx + 10]) for (let r = 86; r < 112; r++) if (r % 3) px(g, r, x, GLOW[2]); }   // 泣く口と涙
  }
  ell(g, 128, 70, 8, 40, (r, c, nx, ny, d) => (d > 0.6 ? 0 : 13));                                                        // 二つの顔のあいだの裂け目
  for (let i = 0; i < 9; i++) { const a = i * 0.7; eye(g, Math.round(128 + Math.cos(a) * 60), Math.round(190 + Math.sin(a) * 36), 4, 4, GLOW, 0.3); }
  return finish(g);
};
// 8. 冥神「無音の弔鐘」: 巨大な鐘の体。舌は垂れる黒い影。鐘の口から白い手が無数に伸びる
const god8 = () => {
  const g = base(104, 104);
  taper(g, curve([128, 4], [128, 18], [128, 40]), 8, 6, BONE, 0);
  ell(g, 128, 60, 34, 26, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.06)]));
  for (let r = 70; r <= 196; r++) {
    const t = (r - 70) / 126, w = 34 + 66 * t ** 1.6;
    for (let c = Math.round(128 - w); c <= Math.round(128 + w); c++) {
      const nx = (c - 128) / w, lum = -nx * 0.7 + 0.1 - t * 0.2, band = Math.abs(r - 130) < 3 || Math.abs(r - 176) < 3;
      px(g, r, c, Math.abs(nx) > 0.96 ? 0 : band ? BONE[toneIdx(4, lum + 0.3, c, r, 0.05)] : BODY[toneIdx(5, lum, c, r, 0.1)]);
    }
  }
  ell(g, 128, 200, 100, 14, (r, c, nx, ny, d) => (d > 0.8 ? 0 : 13));                                                      // 鐘の口（闇）
  taper(g, curve([128, 196], [128, 226], [128, 244]), 12, 4, [18, 18, 13], 0);                                            // 黒い舌
  for (let i = 0; i < 16; i++) { const x = 44 + i * 11; taper(g, curve([x, 206], [x + (i % 3 - 1) * 10, 224], [x + (i % 5 - 2) * 8, 240]), 4, 1, BONE, 0); }
  for (let i = 0; i < 9; i++) for (let r = 90 + (i % 3) * 10; r < 150; r++) { const c = 92 + i * 9; if (hash(c, r) < 0.05) px(g, r, c, BODY[4]); }
  for (const dir of [-1, 1]) eye(g, 128 + dir * 22, 108, 8, 7, GLOW, dir * 0.3);
  return finish(g, 8);
};

// ---- ダンジョンの中ボス ----
// 塔の守り（2層目）: 石の像。胸の灯り石が割れている
const guard2 = () => {
  const g = base(90, 120);
  ell(g, 128, 176, 60, 62, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.14)]));
  ell(g, 128, 76, 30, 32, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.14)]));
  for (const dir of [-1, 1]) ell(g, 128 + dir * 76, 160, 20, 56, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BONE[toneIdx(4, lum, c, r, 0.14)]));
  eye(g, 116, 76, 6, 4, GLOW); eye(g, 140, 76, 6, 4, GLOW);
  shard(g, 128, 160, 14, 30, ACC, 0);
  for (const [x, y, w, h] of [[52, 96, 12, 34], [204, 96, 12, 34], [84, 30, 9, 24], [172, 30, 9, 24], [128, 6, 9, 22]]) shard(g, x, y, w, h, ACC, 0);   // 結晶の角と背のとげ
  for (let i = 0; i < 30; i++) { const c = 90 + Math.floor(hash(i, 3) * 76), r = 130 + Math.floor(hash(i, 7) * 90); for (let k = 0; k < 7; k++) px(g, r + k, c + (k % 2), 0); }
  return finish(g, 6);
};
// 塔の守り（3層目）: 歯車と針の機械。中央の大きな目
const guard3 = () => {
  const g = base(98, 120);
  for (const [cx, cy, R] of [[70, 150, 40], [186, 150, 40], [128, 200, 34]]) {
    for (let a = 0; a < 6.2832; a += 0.02) for (let t = -8; t <= 0; t += 1) { const rr = R + t; px(g, cy + Math.sin(a) * rr, cx + Math.cos(a) * rr, BONE[toneIdx(4, -Math.cos(a) * 0.6 - Math.sin(a) * 0.6, Math.round(a * 50), t, 0.1)]); }
    for (let i = 0; i < 12; i++) { const a = i / 12 * 6.2832; fang(g, Math.round(cx + Math.cos(a) * (R + 2)), Math.round(cy + Math.sin(a) * (R + 2)), 8, 9, 1, BONE); }
  }
  ell(g, 128, 120, 52, 52, skin);
  eye(g, 128, 118, 22, 22, GLOW);
  for (let i = 0; i < 12; i++) { const a = i / 12 * 6.2832; px(g, 120 + Math.sin(a) * 40, 128 + Math.cos(a) * 40, 0); }
  taper(g, [[128, 120], [150, 100]], 4, 2, ACC, 0); taper(g, [[128, 120], [110, 90]], 3, 1, ACC, 0);
  return finish(g, 6);
};
// 灯りの番人（決戦前の間）: 灯籠の体。中の炎が目になる
const guard4 = () => {
  const g = base(96, 120);
  robe(g, 128, 140, 238, 34, 60);
  ell(g, 128, 100, 52, 62, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : BODY[toneIdx(5, lum, c, r, 0.1)]));
  ell(g, 128, 100, 34, 44, (r, c, nx, ny, d) => (d > 0.8 ? 0 : d > 0.5 ? 6 : d > 0.2 ? 7 : 8));                           // 灯籠の中の炎
  eye(g, 116, 98, 7, 8, GLOW); eye(g, 140, 98, 7, 8, GLOW);
  for (const y of [42, 158]) for (let c = 84; c <= 172; c++) { px(g, y, c, 0); px(g, y + 1, c, BONE[1]); px(g, y + 2, c, BONE[2]); }
  fang(g, 128, 12, 50, 30, 1, BONE); 
  for (const dir of [-1, 1]) taper(g, curve([128 + dir * 50, 150], [128 + dir * 84, 172], [128 + dir * 76, 214]), 10, 4, BODY, 0);
  return finish(g, 8);
};
// 深部3層の歪み: 大きな目の群れ
const deep3 = () => {
  const g = base(100, 120);
  ell(g, 128, 140, 84, 80, skin);
  for (let i = 0; i < 26; i++) { const a = hash(i, 1) * 6.2832, d = Math.sqrt(hash(i, 2)) * 62; eye(g, Math.round(128 + Math.cos(a) * d), Math.round(140 + Math.sin(a) * d * 0.85), 5 + Math.floor(hash(i, 3) * 6), 5 + Math.floor(hash(i, 4) * 4), GLOW, (hash(i, 5) - 0.5) * 0.6); }
  for (let i = 0; i < 7; i++) taper(g, curve([60 + i * 22, 200], [40 + i * 28, 230], [30 + i * 32, 248]), 8, 2, BODY, 0);
  for (const [x, y, w, h] of [[40, 60, 8, 20], [216, 60, 8, 20], [128, 30, 8, 22]]) shard(g, x, y, w, h, ACC, 0);
  return finish(g, 12);
};
// 全観（クリア後の試練）: 白い大きな環と、中央の一つの目
const zenkan = () => {
  const g = base(112, 128);
  halo(g, 128, 128, 84, HALO);
  ell(g, 128, 128, 50, 50, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : d > 0.5 ? BODY[toneIdx(5, lum, c, r, 0.1)] : GLOW[toneIdx(3, lum + 0.3, c, r, 0.05)]));
  eye(g, 128, 128, 30, 30, GLOW);
  ell(g, 128, 128, 10, 22, (r, c, nx, ny, d) => (d > 0.5 ? 0 : 13));
  for (let i = 0; i < 16; i++) { const a = i / 16 * 6.2832; taper(g, [[128 + Math.cos(a) * 54, 128 + Math.sin(a) * 54], [128 + Math.cos(a) * 94, 128 + Math.sin(a) * 94]], 5, 1, i % 2 ? ACC : BONE, 0); }
  return finish(g, 6);
};

const P = (name, hue, acc, build, sat) => ({ name, pal: palette(hue, acc, sat), build });
export const PIECES = [
  P("G1-恵みの残照", 45, 50, god1, 40), P("G2-理不尽の羽音", 110, 70, god2), P("G3-坩堝の顎", 5, 35, god3, 55), P("G4-在らざる歌", 260, 290, god4, 20),
  P("G5-透き徹る誓い", 190, 175, god5, 50), P("G6-不敗の咎人", 215, 25, god6, 20), P("G7-境界を見ぬ者", 300, 330, god7), P("G8-無音の弔鐘", 240, 210, god8, 25),
  P("M1-塔の守り（2層）", 30, 40, guard2, 12), P("M2-塔の守り（3層）", 50, 20, guard3, 25), P("M3-灯りの番人", 20, 40, guard4, 35),
  P("M4-深部3層の歪み", 320, 300, deep3), P("M5-全観", 280, 50, zenkan, 25),
];
