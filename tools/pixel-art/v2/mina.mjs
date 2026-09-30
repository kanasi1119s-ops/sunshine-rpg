// C3-ミナ（麦香野の村の出身・水紋系の使い手）: 丁寧でおっとりした、誰にでも優しい少女。
// 麦穂色の髪を片側で長く編み、水色のリボンで結ぶ。木綿のふくらんだ袖と、若草色のベスト、ひざ丈のスカート。
// 水色のリボンと胸の雫の飾りだけが鮮やか（要点の1色）。笑顔の奥の恐れは、伏せがちな目もとにほのかに残す。
import { createPalette, makeGrid, paintShape, spline, line, pip, outline, despeckle, groundShadow, put, clamp, toPieceFile } from "./lib2.mjs";

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0c0912"), RIM = pal.rgb("縁明", "#2d2438");
  const SKIN = pal.ramp("肌", 20, 0.52, 4, 0.38, 0.84, 22);
  const HAIR = pal.ramp("髪", 38, 0.62, 4, 0.2, 0.64, 26);
  const BLS = pal.ramp("ブラウス", 44, 0.3, 3, 0.52, 0.9, 20);
  const VST = pal.ramp("ベスト", 128, 0.3, 3, 0.16, 0.48, 26);
  const SKT = pal.ramp("スカート", 12, 0.42, 3, 0.24, 0.58, 26);
  const LTH = pal.ramp("革", 22, 0.46, 3, 0.11, 0.4, 24);
  const AQ = pal.ramp("水", 190, 0.8, 3, 0.36, 0.72, 16);
  const WHITE = pal.rgb("白", "#fbf8f2");
  const SHD = VST[0];
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 243, 54, 6, SHD);

  // ---------- 脚・靴 ----------
  paintShape(g, spline([[110, 190], [126, 190], [125, 214], [124, 226], [110, 226], [111, 210]], true, 5), BLS, { R: 3, ambient: 0.3 });
  paintShape(g, spline([[130, 190], [146, 190], [147, 210], [146, 226], [132, 226], [131, 214]], true, 5), BLS, { R: 3, ambient: 0.22, bias: -0.06 });
  line(g, 127, 192, 127, 226, BLS[0]);
  const bootL = spline([[106, 214], [125, 214], [126, 232], [128, 242], [101, 242], [101, 232]], true, 5);
  const bootR = spline([[131, 214], [150, 214], [155, 232], [155, 242], [128, 242], [130, 232]], true, 5);
  paintShape(g, bootL, LTH, { R: 3, ambient: 0.26, bias: 0.04 }); paintShape(g, bootR, LTH, { R: 3, ambient: 0.22 });
  for (const [x0, x1] of [[106, 125], [131, 150]]) for (let x = x0; x <= x1; x++) { put(g, 214, x, LTH[2]); put(g, 215, x, LTH[1]); }
  line(g, 103, 240, 126, 240, LTH[0]); line(g, 130, 240, 154, 240, LTH[0]);
  for (const [x, y] of [[112, 222], [112, 226], [144, 222], [144, 226]]) put(g, y, x, BLS[1]);

  // ---------- 長い後ろ髪（肩の後ろへ） ----------
  paintShape(g, spline([[94, 60], [92, 84], [96, 104], [106, 108], [118, 100], [124, 80]], true, 4), HAIR, { R: 4, ambient: 0.2, bias: -0.1 });
  paintShape(g, spline([[162, 60], [164, 84], [160, 104], [150, 108], [138, 100], [132, 80]], true, 4), HAIR, { R: 4, ambient: 0.18, bias: -0.12 });

  // ---------- 首 ----------
  paintShape(g, spline([[119, 80], [137, 80], [137, 102], [119, 102]], true, 3), SKIN, { R: 3, ambient: 0.18, bias: -0.1 });

  // ---------- 胴とスカート ----------
  const torso = spline([[100, 108], [108, 98], [148, 98], [156, 108], [154, 130], [152, 150], [150, 160]], false, 4);
  const skirt = spline([[150, 156], [162, 198], [128, 204], [94, 198], [106, 156]], false, 5);
  const body = [...torso, ...skirt];
  // ブラウス（下に見える身ごろ）
  paintShape(g, body, BLS, { R: 6, ambient: 0.3, gain: 1.05 });
  // スカート（広がるひざ丈）
  const skirtPoly = spline([[106, 154], [150, 154], [163, 198], [150, 204], [128, 200], [106, 204], [93, 198]], true, 5);
  paintShape(g, skirtPoly, SKT, { R: 6, ambient: 0.26, gain: 1.1 });
  // スカートのひだ（影の色）
  for (const [x0, y0, x1, y1] of [[112, 160, 106, 200], [120, 162, 118, 202], [136, 162, 138, 202], [144, 160, 150, 200], [128, 164, 128, 203]]) line(g, x0, y0, x1, y1, SKT[0]);
  for (const [x0, y0, x1, y1] of [[116, 160, 112, 198], [140, 160, 144, 198]]) line(g, x0, y0, x1, y1, SKT[2]);
  // すその縁取り（明るい線）
  for (let x = 94; x < 163; x++) { const yy = 200 + Math.round(Math.abs(x - 128) / 34 * 3) * -0 + (x < 100 || x > 156 ? -2 : 0); if (SKT.includes(g[yy][x])) { put(g, yy, x, BLS[1]); put(g, yy - 1, x, SKT[2]); } }
  // ベスト（若草色・胸あて。前は紐で編み上げ）
  const vest = spline([[106, 106], [118, 100], [122, 118], [118, 150], [108, 152], [104, 128]], true, 4);
  const vest2 = spline([[150, 106], [138, 100], [134, 118], [138, 150], [148, 152], [152, 128]], true, 4);
  paintShape(g, vest, VST, { R: 4, ambient: 0.3, gain: 1.1 }); paintShape(g, vest2, VST, { R: 4, ambient: 0.22, gain: 1.1, bias: -0.04 });
  for (let y = 108; y < 150; y += 7) { line(g, 122, y, 134, y + 3, LTH[2]); line(g, 134, y, 122, y + 3, LTH[2]); put(g, y + 1, 122, LTH[0]); put(g, y + 1, 134, LTH[0]); }
  line(g, 118, 118, 118, 150, VST[0]); line(g, 138, 118, 138, 150, VST[0]);
  // 襟（丸い白い襟）
  paintShape(g, spline([[110, 100], [124, 96], [128, 112], [116, 112]], true, 3), BLS, { R: 2, ambient: 0.5, bias: 0.15 });
  paintShape(g, spline([[146, 100], [132, 96], [128, 112], [140, 112]], true, 3), BLS, { R: 2, ambient: 0.4, bias: 0.05 });
  // 腰の飾り帯（水色のリボン結び）
  for (let x = 106; x <= 150; x++) { put(g, 152, x, LTH[2]); put(g, 153, x, LTH[1]); put(g, 154, x, LTH[0]); }
  paintShape(g, spline([[118, 148], [128, 154], [118, 164], [110, 158]], true, 3), AQ, { R: 2, ambient: 0.4 });
  paintShape(g, spline([[138, 148], [128, 154], [138, 164], [146, 158]], true, 3), AQ, { R: 2, ambient: 0.3 });
  put(g, 154, 127, AQ[0]); put(g, 154, 128, AQ[0]); put(g, 155, 127, AQ[0]); put(g, 155, 128, AQ[0]);
  line(g, 124, 156, 120, 172, AQ[1]); line(g, 132, 156, 136, 172, AQ[0]); line(g, 125, 156, 121, 172, AQ[0]);
  // 胸の雫の飾り（首から下げる）
  line(g, 122, 106, 128, 114, LTH[1]); line(g, 134, 106, 128, 114, LTH[1]);
  for (const [dx, dy, k] of [[0, 0, AQ[2]], [-1, 1, AQ[1]], [0, 1, AQ[2]], [1, 1, AQ[1]], [-1, 2, AQ[1]], [0, 2, AQ[1]], [1, 2, AQ[0]], [0, 3, AQ[0]]]) put(g, 114 + dy, 128 + dx, k);
  put(g, 115, 127, WHITE);

  // ---------- 編み込みの三つ編み（向かって左の肩から前へ） ----------
  // 三つ編み: 左右にゆれる丸い束を重ねて編み目にする
  const bp = [[109, 92, 7], [110, 100, 7], [112, 108, 7], [111, 116, 6.5], [109, 124, 6.5], [110, 132, 6], [111, 140, 6], [110, 148, 5.5]];
  bp.forEach(([x, y, r], i) => {
    const o = i % 2 ? 2 : -2, pts = spline([[x + o - r, y], [x + o, y - 5], [x + o + r, y], [x + o + 1, y + 6]], true, 3);
    paintShape(g, pts, HAIR, { R: 2, ambient: 0.26, gain: 1.2, bias: i % 2 ? -0.06 : 0.04 });
    line(g, x + o - r + 1, y + 3, x + o + r - 1, y + 5, HAIR[0]);
  });
  paintShape(g, spline([[104, 152], [117, 150], [118, 158], [105, 164]], true, 3), AQ, { R: 2, ambient: 0.4 });
  put(g, 152, 107, WHITE); put(g, 153, 107, AQ[2]);

  // ---------- 腕（ふくらんだ袖） ----------
  const armL = spline([[88, 108], [100, 100], [106, 116], [104, 134], [86, 136], [82, 120]], true, 4);
  paintShape(g, armL, BLS, { R: 5, ambient: 0.3, gain: 1.1 });
  line(g, 90, 112, 94, 128, BLS[0]); line(g, 98, 108, 100, 124, BLS[1]);
  for (let x = 84; x <= 105; x++) { put(g, 135, x, SKT[1]); put(g, 136, x, SKT[0]); } // 袖口の細いひも
  paintShape(g, spline([[88, 136], [102, 136], [102, 154], [90, 154]], true, 3), SKIN, { R: 3, ambient: 0.3 });
  paintShape(g, spline([[89, 152], [103, 152], [105, 162], [96, 168], [88, 162]], true, 4), SKIN, { R: 3, ambient: 0.3, bias: 0.05 });
  line(g, 96, 158, 96, 164, SKIN[0]); line(g, 100, 157, 100, 163, SKIN[0]);
  const armR = spline([[168, 108], [156, 100], [150, 116], [152, 134], [170, 136], [174, 120]], true, 4);
  paintShape(g, armR, BLS, { R: 5, ambient: 0.2, gain: 1.1, bias: -0.06 });
  line(g, 164, 112, 162, 128, BLS[0]);
  for (let x = 151; x <= 172; x++) { put(g, 135, x, SKT[1]); put(g, 136, x, SKT[0]); }
  paintShape(g, spline([[154, 136], [168, 136], [166, 154], [154, 154]], true, 3), SKIN, { R: 3, ambient: 0.2, bias: -0.06 });
  paintShape(g, spline([[153, 152], [167, 152], [168, 162], [160, 168], [152, 162]], true, 4), SKIN, { R: 3, ambient: 0.22 });
  line(g, 159, 158, 159, 164, SKIN[0]); line(g, 163, 157, 163, 163, SKIN[0]);

  // ---------- 頭 ----------
  paintShape(g, spline([[95, 58], [101, 54], [102, 70], [97, 70]], true, 3), SKIN, { R: 2, ambient: 0.4 });
  paintShape(g, spline([[161, 58], [155, 54], [154, 70], [159, 70]], true, 3), SKIN, { R: 2, ambient: 0.3, bias: -0.08 });
  const face = spline([[128, 28], [148, 32], [158, 52], [155, 70], [144, 84], [128, 90], [112, 84], [101, 70], [98, 52], [108, 32]], true, 6);
  paintShape(g, face, SKIN, { R: 8, ambient: 0.42, gain: 0.55, bias: -0.1 });

  // 髪: ふんわりした頭頂、中わけの前髪、頬にかかる横の髪
  const back = spline([[93, 62], [91, 38], [103, 18], [128, 9], [153, 18], [165, 38], [163, 62], [160, 84], [150, 72], [106, 72], [96, 84]], true, 5);
  paintShape(g, back, HAIR, { R: 6, ambient: 0.22, bias: -0.06, clip: (x, y) => !pip(face, x + 0.5, y + 0.5) });
  const outer = spline([[96, 84], [92, 60], [90, 40], [100, 21], [116, 12], [130, 9], [146, 12], [158, 22], [166, 40], [164, 60], [160, 84]], false, 6);
  // 生え際: 中わけ。額の両側へなだらかに流れ、頬の横の髪へつながる
  const fringe = [[156, 82], [153, 64], [150, 54], [142, 50], [134, 46], [128, 40], [122, 46], [114, 50], [106, 54], [103, 64], [100, 82]];
  paintShape(g, [...outer, ...fringe], HAIR, { R: 6, ambient: 0.3, gain: 1.0 });
  // 頭頂の光の帯（ふんわりした曲線）
  for (const [x0, y0, x1, y1] of [[106, 30, 114, 22], [114, 22, 128, 18], [128, 18, 144, 20]]) { line(g, x0, y0, x1, y1, HAIR[3]); }
  // 房の筋（中わけから外へ流れる）
  for (const [x0, y0, x1, y1] of [[126, 18, 112, 42], [124, 20, 104, 50], [130, 18, 146, 42], [132, 20, 152, 50], [98, 40, 100, 78], [158, 40, 156, 78], [116, 24, 106, 40], [142, 24, 150, 40]]) line(g, x0, y0, x1, y1, HAIR[0]);
  for (const [x0, y0, x1, y1] of [[120, 30, 112, 44], [136, 30, 146, 44]]) line(g, x0, y0, x1, y1, HAIR[1]);
  // 頬の横の髪は右側（向かって右）をやや暗く
  for (let y = 46; y < 84; y++) for (let x = 154; x < 166; x++) { const i = HAIR.indexOf(g[y][x]); if (i > 0 && x > 156) g[y][x] = HAIR[i - 1]; }
  // 前髪の影
  for (let y = 30; y < 64; y++) for (let x = 100; x < 158; x++) {
    if (!SKIN.includes(g[y][x])) continue;
    if (HAIR.includes(g[y - 1][x]) || HAIR.includes(g[y - 2]?.[x])) g[y][x] = SKIN[0]; else if (HAIR.includes(g[y - 3]?.[x]) && (x + y) % 2 === 0) g[y][x] = SKIN[1];
  }
  // 髪飾りの小さな水色のリボン（耳のうえ）
  paintShape(g, spline([[102, 40], [112, 34], [114, 44], [106, 48]], true, 3), AQ, { R: 2, ambient: 0.45 });
  put(g, 42, 108, AQ[0]); put(g, 41, 108, AQ[0]);

  // ---------- 顔立ち（やわらかくたれた目） ----------
  const eye = (ex, side) => {
    line(g, ex - 6, 57 + (side < 0 ? 1 : 0), ex + 5, 55 + (side < 0 ? 0 : 1), HAIR[1]); // やさしい弧の眉
    // 目: 少し大きく丸い。外側が少し下がる
    for (let y = 0; y < 10; y++) for (let x = -3; x <= 4; x++) { if ((y === 0 || y === 9) && (x <= -2 || x >= 3)) continue; if (y === 1 && (x === -3 || x === 4)) continue; put(g, 59 + y, ex + x, OUT); }
    for (let y = 3; y < 9; y++) for (let x = -2; x <= 3; x++) { if (y === 8 && (x === -2 || x === 3)) continue; put(g, 59 + y, ex + x, y < 5 ? AQ[0] : y < 7 ? AQ[1] : AQ[2]); }
    for (let x = -1; x <= 2; x++) put(g, 61, ex + x, OUT); put(g, 62, ex, OUT); put(g, 62, ex + 1, OUT); // 瞳孔
    put(g, 60, ex - 2, OUT); put(g, 60, ex - 1, OUT);
    put(g, 63, ex - 2, WHITE); put(g, 64, ex - 2, WHITE); put(g, 63, ex - 1, WHITE); put(g, 66, ex + 2, WHITE);
    put(g, 58, ex - 3, HAIR[0]); put(g, 58, ex + 4, HAIR[0]); // まつげ
  };
  eye(113, -1); eye(143, 1);
  // ほんのり赤いほお
  for (const [x, y] of [[104, 74], [105, 74], [106, 74], [105, 75], [106, 75], [107, 75], [150, 74], [151, 74], [152, 74], [149, 75], [150, 75], [151, 75]]) put(g, y, x, SKT[2]);
  // 鼻・小さな笑顔
  put(g, 74, 129, SKIN[1]); put(g, 75, 128, SKIN[1]); put(g, 75, 129, SKIN[0]);
  line(g, 122, 81, 124, 83, SKT[0]); line(g, 124, 83, 132, 83, SKT[0]); line(g, 132, 83, 134, 81, SKT[0]); line(g, 126, 84, 130, 84, SKT[1]);
  for (let x = 108; x < 150; x++) for (let y = 84; y < 92; y++) if (SKIN.includes(g[y][x]) && !SKIN.includes(g[y + 1]?.[x])) g[y][x] = SKIN[0];

  despeckle(g, 1);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C3-ミナ", g)]; })();
