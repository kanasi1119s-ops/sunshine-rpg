// C1-ユーリ（16歳・灯里支部の新人調査員）: 素直でまっすぐな少年。動きやすい旅装束。
// 左手首（絵では向かって右）に、亡き祖父の形見の「灯り石」の腕輪。ここだけが鮮やかな琥珀色に灯る（要点の1色）。
import { createPalette, makeGrid, paintShape, spline, line, pip, outline, despeckle, groundShadow, put, clamp, hash, toPieceFile } from "./lib2.mjs";

const mir = (pts) => pts.map(([x, y]) => [256 - x, y]).reverse();

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0c0813"), RIM = pal.rgb("縁明", "#2e2236");
  const SKIN = pal.ramp("肌", 24, 0.5, 4, 0.36, 0.78, 22);
  const HAIR = pal.ramp("髪", 20, 0.6, 4, 0.13, 0.5, 26);
  const JKT = pal.ramp("上着", 218, 0.46, 4, 0.11, 0.54, 26);
  const UND = pal.ramp("下着", 42, 0.34, 3, 0.5, 0.9, 20);
  const PNT = pal.ramp("ズボン", 34, 0.34, 3, 0.26, 0.6, 24);
  const LTH = pal.ramp("革", 18, 0.5, 3, 0.11, 0.4, 24);
  const GLOW = [pal.rgb("灯", "#ff9f1c"), pal.rgb("灯芯", "#fff1a8")];
  const WHITE = pal.rgb("白", "#fbf6ee");
  const SHD = JKT[0];
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 243, 50, 6, SHD);

  // ---------- 脚・靴 ----------
  const legL = spline([[108, 150], [126, 150], [125, 200], [124, 222], [106, 222], [107, 190]], true, 5);
  const legR = spline([[130, 150], [148, 150], [149, 190], [150, 222], [132, 222], [131, 200]], true, 5);
  paintShape(g, legL, PNT, { R: 4, ambient: 0.3 }); paintShape(g, legR, PNT, { R: 4, ambient: 0.22, bias: -0.06 });
  line(g, 127, 152, 127, 222, PNT[0]); // 脚のあいだ
  // ひざの布のしわ
  for (const [x, y, d] of [[113, 184, 1], [119, 186, 1], [137, 186, 1], [143, 184, 1]]) { line(g, x, y, x + 3 * d, y + 2, PNT[0]); }
  const bootL = spline([[103, 212], [125, 212], [126, 232], [128, 242], [98, 242], [98, 232]], true, 5);
  const bootR = spline([[131, 212], [153, 212], [158, 232], [158, 242], [128, 242], [130, 232]], true, 5);
  paintShape(g, bootL, LTH, { R: 3, ambient: 0.25, bias: 0.05 }); paintShape(g, bootR, LTH, { R: 3, ambient: 0.22 });
  for (const [x0, x1] of [[103, 125], [131, 153]]) { for (let x = x0; x <= x1; x++) { put(g, 212, x, UND[2]); put(g, 213, x, UND[1]); put(g, 214, x, UND[0]); } } // 折り返しの縁
  line(g, 100, 240, 126, 240, LTH[0]); line(g, 130, 240, 156, 240, LTH[0]); // 靴底
  put(g, 226, 108, LTH[2]); put(g, 227, 108, LTH[2]); put(g, 226, 140, LTH[2]);

  // ---------- 腕（後ろ）と胴 ----------
  // 首
  paintShape(g, spline([[119, 80], [137, 80], [137, 102], [119, 102]], true, 3), SKIN, { R: 3, ambient: 0.2, bias: -0.1 });
  // 上着の裾（腰から少し広がる）
  const torso = spline([[98, 106], [108, 98], [148, 98], [158, 106], [156, 130], [158, 156], [148, 160], [128, 158], [108, 160], [98, 156], [100, 130]], true, 4);
  paintShape(g, torso, JKT, { R: 6, ambient: 0.26, gain: 1.2 });
  // 前あき（下着の縦帯）と紐
  const under = [[121, 100], [135, 100], [136, 130], [138, 158], [118, 158], [120, 130]];
  paintShape(g, spline(under, true, 4), UND, { R: 3, ambient: 0.4 });
  for (let y = 108; y < 152; y += 8) { line(g, 122, y, 134, y + 4, UND[0]); line(g, 134, y, 122, y + 4, UND[0]); }
  // 前あきの縁（上着の折り返し）
  line(g, 121, 100, 118, 158, JKT[3]); line(g, 135, 100, 138, 158, JKT[0]);
  // 襟（立ち襟）
  paintShape(g, spline([[106, 98], [120, 92], [124, 108], [112, 110]], true, 3), JKT, { R: 2, ambient: 0.4, bias: 0.12 });
  paintShape(g, spline([[150, 98], [136, 92], [132, 108], [144, 110]], true, 3), JKT, { R: 2, ambient: 0.3 });
  // 肩から斜めがけの革ベルト
  const strap = [[100, 106], [106, 104], [157, 148], [157, 155], [151, 155], [100, 113]];
  paintShape(g, strap, LTH, { R: 2, ambient: 0.3, clip: (x, y) => pip(torso, x + 0.5, y + 0.5) });
  
  // 腰ベルトとバックル・ポーチ
  for (let x = 100; x <= 156; x++) { put(g, 148, x, LTH[2]); put(g, 149, x, LTH[1]); put(g, 150, x, LTH[0]); put(g, 151, x, LTH[0]); }
  paintShape(g, [[124, 145], [134, 145], [134, 155], [124, 155]], LTH, { R: 1, ambient: 0.5, bias: 0.2 });
  put(g, 150, 129, GLOW[1]); put(g, 150, 130, GLOW[1]); put(g, 151, 129, WHITE);
  const pouch = spline([[141, 152], [155, 152], [156, 172], [142, 174]], true, 3);
  paintShape(g, pouch, LTH, { R: 3, ambient: 0.3 }); line(g, 142, 158, 155, 158, LTH[0]); put(g, 160, 148, UND[1]); put(g, 161, 148, UND[0]);
  // 裾の縫い目と、上着のしわ（影の色）
  line(g, 100, 155, 118, 157, JKT[0]); line(g, 138, 157, 156, 155, JKT[0]);
  line(g, 108, 130, 114, 140, JKT[0]); line(g, 113, 124, 116, 132, JKT[1]); line(g, 150, 128, 144, 138, JKT[0]);

  // ---------- 腕（前） ----------
  // 向かって左の腕: 袖をまくって、前腕と手が出る
  const armL = spline([[92, 106], [104, 100], [107, 118], [106, 132], [104, 134], [90, 134], [88, 120]], true, 4);
  paintShape(g, armL, JKT, { R: 4, ambient: 0.3 });
  paintShape(g, spline([[90, 132], [105, 132], [104, 152], [92, 152]], true, 3), SKIN, { R: 3, ambient: 0.28 });
  for (let x = 89; x <= 106; x++) { put(g, 131, x, UND[2]); put(g, 132, x, UND[1]); put(g, 133, x, UND[0]); }
  paintShape(g, spline([[91, 150], [105, 150], [107, 160], [98, 166], [90, 160]], true, 4), SKIN, { R: 3, ambient: 0.3, bias: 0.05 });
  line(g, 97, 156, 97, 162, SKIN[0]); line(g, 101, 155, 101, 161, SKIN[0]);
  // 向かって右の腕（左手首に形見の腕輪）
  const armR = spline([[164, 106], [152, 100], [149, 118], [150, 132], [152, 134], [166, 134], [168, 120]], true, 4);
  paintShape(g, armR, JKT, { R: 4, ambient: 0.22, bias: -0.04 });
  paintShape(g, spline([[151, 132], [166, 132], [164, 152], [152, 152]], true, 3), SKIN, { R: 3, ambient: 0.2, bias: -0.06 });
  for (let x = 150; x <= 167; x++) { put(g, 131, x, UND[2]); put(g, 132, x, UND[1]); put(g, 133, x, UND[0]); }
  paintShape(g, spline([[152, 150], [165, 150], [166, 160], [158, 166], [150, 160]], true, 4), SKIN, { R: 3, ambient: 0.22 });
  line(g, 157, 156, 157, 162, SKIN[0]); line(g, 161, 155, 161, 161, SKIN[0]);
  // 腕輪: 革の輪と、光る灯り石
  for (let x = 152; x <= 165; x++) { put(g, 143, x, LTH[2]); put(g, 144, x, LTH[1]); put(g, 145, x, LTH[0]); }
  for (let dy = -3; dy <= 3; dy++) for (let dx = -3; dx <= 3; dx++) { const d = Math.abs(dx) + Math.abs(dy); if (d <= 3 && !(Math.abs(dx) === 3 || Math.abs(dy) === 3 && dx !== 0)) put(g, 144 + dy, 158 + dx, d <= 1 ? GLOW[1] : GLOW[0]); }
  for (const [dx, dy] of [[-4, -1], [4, 1], [-2, -4], [3, 4]]) if (SKIN.includes(g[144 + dy][158 + dx])) put(g, 144 + dy, 158 + dx, GLOW[0]);
  put(g, 143, 157, WHITE); put(g, 142, 158, GLOW[1]);

  // ---------- 頭 ----------
  // 耳
  paintShape(g, spline([[94, 56], [100, 52], [102, 70], [96, 70]], true, 3), SKIN, { R: 2, ambient: 0.4 });
  paintShape(g, spline([[162, 56], [156, 52], [154, 70], [160, 70]], true, 3), SKIN, { R: 2, ambient: 0.3, bias: -0.08 });
  put(g, 62, 97, SKIN[1]); put(g, 63, 97, SKIN[1]); put(g, 62, 159, SKIN[0]); put(g, 63, 159, SKIN[0]);
  // 顔（大きく丸い）
  const face = spline([[128, 28], [148, 32], [157, 52], [154, 70], [143, 84], [128, 90], [113, 84], [102, 70], [99, 52], [108, 32]], true, 6);
  paintShape(g, face, SKIN, { R: 8, ambient: 0.4, gain: 0.55, bias: -0.13 });

  // 髪: まず後ろ髪のかたまり（頭のうしろ・えり足）
  const back = spline([[94, 58], [92, 36], [104, 18], [128, 10], [152, 18], [164, 36], [162, 58], [158, 76], [148, 70], [108, 70], [98, 76]], true, 5);
  paintShape(g, back, HAIR, { R: 6, ambient: 0.22, bias: -0.06, clip: (x, y) => !pip(face, x + 0.5, y + 0.5) });
  // 前髪と頭頂（顔をおおう帽子のような形。生え際は房に割れ、右へ流れる）
  const outer = spline([[94, 62], [91, 40], [100, 21], [116, 12], [130, 9], [146, 13], [159, 24], [166, 42], [163, 62]], false, 6);
  const fringe = [[157, 66], [154, 50], [151, 44], [147, 52], [143, 40], [139, 50], [133, 38], [128, 50], [121, 36], [117, 46], [110, 38], [107, 50], [104, 44], [102, 56], [99, 66]];
  const cap = [...outer, ...fringe];
  paintShape(g, cap, HAIR, { R: 6, ambient: 0.3, gain: 0.95 });
  // 頭頂のあかるい帯（光の反射）
  for (const [x0, y0, x1, y1] of [[108, 24, 122, 17], [122, 17, 138, 15]]) { line(g, x0, y0, x1, y1, HAIR[3]); line(g, x0 + 1, y0 + 1, x1 + 1, y1 + 1, HAIR[3]); }
  // ぴょんとはねた毛束（あほ毛）
  paintShape(g, [[126, 12], [131, 2], [138, 10], [136, 18]], HAIR, { R: 2, ambient: 0.35, bias: 0.1 });
  // 房の筋（髪の影の色）
  for (const [x, y, len] of [[112, 24, 12], [122, 22, 14], [134, 22, 12], [146, 26, 12], [102, 32, 10]]) line(g, x, y, x + 1, y + len, HAIR[0]);
  for (const [x, y] of [[117, 30], [129, 30], [141, 32]]) { line(g, x, y, x, y + 8, HAIR[1]); }
  // 右側の髪（向かって右）はやや暗く
  for (let y = 44; y < 66; y++) for (let x = 158; x < 165; x++) { const k = g[y][x]; const i = HAIR.indexOf(k); if (i > 0) g[y][x] = HAIR[i - 1]; }
  // 前髪が額に落とす影
  for (let y = 30; y < 62; y++) for (let x = 98; x < 158; x++) {
    if (!SKIN.includes(g[y][x])) continue;
    const above = HAIR.includes(g[y - 1][x]) || HAIR.includes(g[y - 2]?.[x]);
    if (above) g[y][x] = SKIN[0]; else if (HAIR.includes(g[y - 3]?.[x]) && (x + y) % 2 === 0) g[y][x] = SKIN[1];
  }

  // ---------- 顔立ち ----------
  const eye = (ex, side) => {
    // 眉
    line(g, ex - 6, 55 + (side < 0 ? 1 : 0), ex + 5, 53 + (side < 0 ? 0 : 1), HAIR[0]); line(g, ex - 5, 56, ex + 4, 54 + (side < 0 ? 1 : 2), HAIR[1]);
    // 目: 濃い縦長の瞳。下に虹彩の色、左上に白い光
    for (let y = 0; y < 10; y++) for (let x = -2; x <= 3; x++) { if ((y === 0 || y === 9) && (x === -2 || x === 3)) continue; put(g, 57 + y, ex + x, OUT); }
    for (let y = 5; y < 9; y++) for (let x = -1; x <= 2; x++) put(g, 57 + y, ex + x, y > 6 ? JKT[3] : JKT[2]);
    put(g, 59, ex - 1, WHITE); put(g, 60, ex - 1, WHITE); put(g, 59, ex, WHITE); put(g, 63, ex + 2, JKT[3]);
    put(g, 56, ex - 3, HAIR[0]); put(g, 56, ex + 4, HAIR[0]);
  };
  eye(113, -1); eye(143, 1);
  // 鼻・口・ほほ
  put(g, 73, 129, SKIN[1]); put(g, 74, 129, SKIN[1]); put(g, 75, 128, SKIN[1]);
  line(g, 123, 80, 133, 80, HAIR[1]); put(g, 79, 121, HAIR[1]); put(g, 78, 120, SKIN[0]); put(g, 79, 135, HAIR[1]); put(g, 78, 136, SKIN[0]); line(g, 125, 81, 131, 81, SKIN[0]); put(g, 82, 128, SKIN[1]); put(g, 82, 129, SKIN[1]);
  for (const x of [105, 106, 107, 149, 150, 151]) put(g, 73, x, SKIN[2]);
  // あごの下の影を強く
  for (let x = 108; x < 150; x++) for (let y = 84; y < 92; y++) if (SKIN.includes(g[y][x]) && !SKIN.includes(g[y + 1]?.[x]) ) g[y][x] = SKIN[0];

  despeckle(g, 1);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C1-ユーリ", g)]; })();
