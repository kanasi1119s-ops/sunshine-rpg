// C2-レト（灯里支部の先輩調査員・20代なかば）: 皮肉屋で軽口を叩くが、要所では的確。
// 冷たい灰紫の髪、半分まぶたの下がった目、片方だけ上がる口もと。すそ長の調査用コートを羽織り、
// 首に巻いた赤いマフラーだけが鮮やか（要点の1色）。身内を失った過去は、少し伏せた目に出す。
import { createPalette, makeGrid, paintShape, spline, line, pip, outline, despeckle, groundShadow, put, clamp, toPieceFile } from "./lib2.mjs";

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0a0810"), RIM = pal.rgb("縁明", "#2a2338");
  const SKIN = pal.ramp("肌", 22, 0.4, 4, 0.36, 0.82, 24);
  const HAIR = pal.ramp("髪", 236, 0.16, 4, 0.12, 0.56, 30);
  const COAT = pal.ramp("コート", 186, 0.24, 4, 0.07, 0.36, 30);
  const UND = pal.ramp("中着", 40, 0.2, 2, 0.5, 0.84, 20);
  const PNT = pal.ramp("ズボン", 232, 0.22, 3, 0.12, 0.36, 24);
  const LTH = pal.ramp("革", 22, 0.42, 3, 0.12, 0.42, 24);
  const RED = pal.ramp("赤", 358, 0.78, 3, 0.26, 0.6, 12);
  const WHITE = pal.rgb("白", "#f6f2fa");
  const SHD = COAT[0];
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 243, 52, 6, SHD);

  // ---------- 脚・靴（コートのすそから少し見える） ----------
  paintShape(g, spline([[110, 170], [126, 170], [125, 208], [124, 224], [108, 224], [109, 200]], true, 5), PNT, { R: 4, ambient: 0.3 });
  paintShape(g, spline([[130, 170], [146, 170], [147, 200], [148, 224], [132, 224], [131, 208]], true, 5), PNT, { R: 4, ambient: 0.22, bias: -0.05 });
  line(g, 127, 172, 127, 224, PNT[0]);
  const bootL = spline([[104, 214], [125, 214], [126, 232], [128, 242], [99, 242], [99, 232]], true, 5);
  const bootR = spline([[131, 214], [152, 214], [157, 232], [157, 242], [128, 242], [130, 232]], true, 5);
  paintShape(g, bootL, LTH, { R: 3, ambient: 0.24, bias: 0.02 }); paintShape(g, bootR, LTH, { R: 3, ambient: 0.2 });
  for (const [x0, x1] of [[104, 125], [131, 152]]) for (let x = x0; x <= x1; x++) { put(g, 214, x, LTH[2]); put(g, 215, x, LTH[1]); }
  line(g, 101, 240, 126, 240, LTH[0]); line(g, 130, 240, 156, 240, LTH[0]);
  for (const y of [224, 228, 232]) { put(g, y, 114, UND[0]); put(g, y, 142, UND[0]); } // 靴ひも

  // ---------- 首 ----------
  paintShape(g, spline([[118, 80], [138, 80], [138, 104], [118, 104]], true, 3), SKIN, { R: 3, ambient: 0.18, bias: -0.1 });

  // ---------- コート（すそ長。前あきで、下へ向かって広がる） ----------
  const coat = spline([[96, 108], [106, 98], [150, 98], [160, 108], [158, 140], [166, 186], [170, 202], [150, 206], [128, 202], [106, 206], [86, 202], [90, 186], [98, 140]], true, 4);
  paintShape(g, coat, COAT, { R: 6, ambient: 0.26, gain: 1.15 });
  // 前あき: 中の服
  const inner = spline([[121, 100], [135, 100], [138, 150], [146, 204], [110, 204], [118, 150]], true, 4);
  paintShape(g, inner, PNT, { R: 4, ambient: 0.3, clip: (x, y) => y > 104 });
  // 中着のシャツ（胸もとだけ見える）
  paintShape(g, spline([[122, 102], [134, 102], [136, 126], [120, 126]], true, 3), UND, { R: 2, ambient: 0.4 });
  line(g, 128, 106, 128, 124, UND[0]);
  // 前あきの縁（コートの折り返し）
  line(g, 121, 100, 118, 150, COAT[3]); line(g, 118, 150, 110, 204, COAT[3]); line(g, 135, 100, 138, 150, COAT[0]); line(g, 138, 150, 146, 204, COAT[0]);
  // コートの裾のしわ・縫い目（影の色）
  for (const [x0, y0, x1, y1] of [[104, 160, 108, 200], [96, 166, 96, 196], [150, 160, 148, 202], [158, 168, 160, 198], [112, 170, 112, 186]]) line(g, x0, y0, x1, y1, COAT[0]);
  for (const [x0, y0, x1, y1] of [[100, 150, 106, 176], [154, 150, 152, 176]]) line(g, x0, y0, x1, y1, COAT[1]);
  // 裾の折り返し（明るい縁）
  for (let x = 89; x < 168; x++) { const yy = 201 + (x < 128 ? Math.round((128 - x) * 0.02) : Math.round((x - 128) * 0.02)); if (COAT.includes(g[yy][x]) || PNT.includes(g[yy][x])) { put(g, yy, x, COAT[3]); put(g, yy + 1, x, COAT[0]); } }
  // ボタン
  for (const y of [132, 148, 164]) { put(g, y, 118 - (y - 100) * 0.03, LTH[2]); put(g, y + 1, 118 - (y - 100) * 0.03, LTH[0]); }
  // 立て襟
  paintShape(g, spline([[104, 100], [120, 90], [124, 112], [110, 116]], true, 3), COAT, { R: 3, ambient: 0.35, bias: 0.1 });
  paintShape(g, spline([[152, 100], [136, 90], [132, 112], [146, 116]], true, 3), COAT, { R: 3, ambient: 0.28 });
  // 腰のベルトと肩かけカバン（斜め）
  for (let x = 102; x <= 154; x++) { put(g, 150, x, LTH[2]); put(g, 151, x, LTH[1]); put(g, 152, x, LTH[0]); }
  paintShape(g, [[102, 104], [108, 102], [160, 168], [160, 176], [152, 176], [102, 112]], LTH, { R: 2, ambient: 0.3, clip: (x, y) => pip(coat, x + 0.5, y + 0.5) && !pip(inner, x + 0.5, y + 0.5) });
  paintShape(g, spline([[142, 164], [162, 164], [164, 190], [144, 192]], true, 3), LTH, { R: 3, ambient: 0.3 });
  line(g, 143, 172, 163, 172, LTH[0]); put(g, 174, 153, UND[1]); put(g, 175, 153, UND[0]);
  put(g, 152, 127, UND[1]); put(g, 152, 128, UND[1]);

  // ---------- 赤いマフラー（首に二重に巻き、先を胸に垂らす） ----------
  paintShape(g, spline([[104, 100], [128, 110], [152, 100], [154, 112], [128, 122], [102, 112]], true, 5), RED, { R: 3, ambient: 0.3, gain: 1.2 });
  line(g, 108, 108, 126, 116, RED[0]); line(g, 148, 108, 132, 116, RED[0]);
  paintShape(g, spline([[112, 114], [124, 116], [124, 152], [120, 158], [110, 152], [110, 130]], true, 4), RED, { R: 3, ambient: 0.28, gain: 1.2 });
  for (let y = 152; y < 159; y++) for (let x = 111; x < 123; x += 2) put(g, y, x + (y % 2), RED[0]);
  line(g, 116, 120, 115, 148, RED[0]); put(g, 118, 112, RED[2]); put(g, 118, 113, RED[2]);
  put(g, 106, 112, RED[2]); put(g, 106, 113, RED[2]);

  // ---------- 腕 ----------
  // 向かって左: 袖を折り返し、革の手袋
  const armL = spline([[90, 106], [102, 100], [106, 120], [104, 136], [88, 138], [86, 122]], true, 4);
  paintShape(g, armL, COAT, { R: 4, ambient: 0.3, gain: 1.1 });
  paintShape(g, spline([[88, 134], [104, 134], [103, 156], [90, 156]], true, 3), SKIN, { R: 3, ambient: 0.28 });
  for (let x = 87; x <= 105; x++) { put(g, 134, x, UND[1]); put(g, 135, x, UND[0]); put(g, 133, x, COAT[3]); }
  paintShape(g, spline([[89, 150], [104, 150], [106, 162], [97, 168], [88, 162]], true, 4), LTH, { R: 3, ambient: 0.35, bias: 0.05 });
  line(g, 96, 158, 96, 164, LTH[0]); line(g, 100, 157, 100, 163, LTH[0]);
  // 向かって右
  const armR = spline([[166, 106], [154, 100], [150, 120], [152, 136], [168, 138], [170, 122]], true, 4);
  paintShape(g, armR, COAT, { R: 4, ambient: 0.22, gain: 1.1, bias: -0.04 });
  paintShape(g, spline([[152, 134], [168, 134], [166, 156], [154, 156]], true, 3), SKIN, { R: 3, ambient: 0.2, bias: -0.06 });
  for (let x = 151; x <= 169; x++) { put(g, 134, x, UND[1]); put(g, 135, x, UND[0]); put(g, 133, x, COAT[2]); }
  paintShape(g, spline([[153, 150], [167, 150], [168, 162], [160, 168], [152, 162]], true, 4), LTH, { R: 3, ambient: 0.25 });
  line(g, 159, 158, 159, 164, LTH[0]); line(g, 163, 157, 163, 163, LTH[0]);
  // 袖のしわ
  line(g, 92, 116, 96, 128, COAT[0]); line(g, 160, 116, 158, 128, COAT[0]);

  // ---------- 頭 ----------
  paintShape(g, spline([[96, 56], [102, 52], [104, 70], [98, 70]], true, 3), SKIN, { R: 2, ambient: 0.4 });
  paintShape(g, spline([[160, 56], [154, 52], [152, 70], [158, 70]], true, 3), SKIN, { R: 2, ambient: 0.3, bias: -0.08 });
  const face = spline([[128, 28], [146, 32], [155, 52], [152, 72], [142, 86], [128, 92], [114, 86], [104, 72], [101, 52], [110, 32]], true, 6);
  paintShape(g, face, SKIN, { R: 8, ambient: 0.4, gain: 0.55, bias: -0.08 });

  // 髪（後頭部のかたまり）
  const back = spline([[94, 58], [92, 36], [104, 18], [128, 10], [152, 18], [164, 36], [162, 58], [156, 76], [148, 70], [108, 70], [100, 78]], true, 5);
  paintShape(g, back, HAIR, { R: 6, ambient: 0.22, bias: -0.06, clip: (x, y) => !pip(face, x + 0.5, y + 0.5) });
  // 頭頂と前髪: 左（向かって右側）が長く流れ、片目に少しかかる
  const outer = spline([[95, 66], [91, 42], [100, 22], [116, 12], [132, 9], [148, 13], [160, 25], [166, 44], [164, 70], [160, 84]], false, 6);
  const fringe = [[156, 72], [154, 58], [150, 62], [146, 48], [140, 60], [134, 42], [128, 54], [122, 40], [116, 52], [110, 38], [106, 50], [103, 44], [102, 58], [99, 70]];
  paintShape(g, [...outer, ...fringe], HAIR, { R: 6, ambient: 0.3, gain: 1.0 });
  // 寝ぐせの毛束（頭頂で外へはねる）と、向かって右に長く垂れる一房
  paintShape(g, [[118, 14], [112, 4], [130, 11]], HAIR, { R: 2, ambient: 0.4, bias: 0.1 });
  paintShape(g, [[136, 11], [146, 3], [150, 18]], HAIR, { R: 2, ambient: 0.3, bias: 0.05 });
  paintShape(g, [[152, 60], [160, 62], [162, 82], [158, 92], [153, 76]], HAIR, { R: 2, ambient: 0.28 });
  line(g, 157, 66, 159, 86, HAIR[0]);
  // 頭頂の光の帯
  for (const [x0, y0, x1, y1] of [[106, 26, 120, 18], [120, 18, 138, 16]]) { line(g, x0, y0, x1, y1, HAIR[3]); line(g, x0 + 1, y0 + 1, x1 + 1, y1 + 1, HAIR[3]); }
  // 房の筋
  for (const [x, y, len] of [[110, 24, 12], [121, 21, 15], [133, 21, 13], [145, 25, 13], [101, 32, 10], [156, 34, 20]]) line(g, x, y, x + 1, y + len, HAIR[0]);
  for (const [x, y] of [[116, 30], [128, 28], [140, 30]]) line(g, x, y, x, y + 8, HAIR[1]);
  // 額の影
  for (let y = 30; y < 64; y++) for (let x = 100; x < 156; x++) {
    if (!SKIN.includes(g[y][x])) continue;
    if (HAIR.includes(g[y - 1][x]) || HAIR.includes(g[y - 2]?.[x])) g[y][x] = SKIN[0]; else if (HAIR.includes(g[y - 3]?.[x]) && (x + y) % 2 === 0) g[y][x] = SKIN[1];
  }

  // ---------- 顔立ち（半分まぶたを下ろした、斜に構えた目） ----------
  const eye = (ex, side) => {
    // 眉: 向かって右が少し上がる
    const up = side > 0 ? 2 : 0;
    line(g, ex - 6, 55 + (side < 0 ? 2 : 1) - up, ex + 5, 54 + (side < 0 ? 0 : 1) - up, HAIR[0]); line(g, ex - 5, 56 - up, ex + 4, 55 - up + (side < 0 ? 0 : 1), HAIR[1]);
    // 目: 上をまぶたが2ドット分おおう。下に虹彩、白い光
    for (let x = -3; x <= 4; x++) { put(g, 60, ex + x, OUT); if (x > -3 && x < 4) put(g, 61, ex + x, OUT); }
    for (let y = 62; y < 67; y++) for (let x = -2; x <= 3; x++) { if (y === 66 && (x === -2 || x === 3)) continue; put(g, y, ex + x, OUT); }
    for (let y = 63; y < 66; y++) for (let x = -1; x <= 2; x++) put(g, y, ex + x, COAT[y === 65 ? 3 : 2]);
    put(g, 63, ex - 1, WHITE); put(g, 64, ex - 1, WHITE);
    put(g, 67, ex - 1, SKIN[0]); put(g, 67, ex, SKIN[0]); put(g, 67, ex + 1, SKIN[0]); // 目の下の影（少し疲れた印象）
    put(g, 59, ex - 4, HAIR[0]);
  };
  eye(115, -1); eye(141, 1);
  // 鼻と、片側だけ上がる口もと
  put(g, 74, 129, SKIN[1]); put(g, 75, 129, SKIN[1]); put(g, 76, 128, SKIN[1]); put(g, 76, 130, SKIN[0]);
  line(g, 122, 82, 130, 82, LTH[0]); line(g, 130, 82, 136, 79, LTH[0]); put(g, 78, 137, LTH[0]); put(g, 83, 121, SKIN[0]);
  line(g, 126, 84, 132, 84, SKIN[0]);
  // ほおの線（ほおがこけた、少し大人びた印象）
  line(g, 106, 74, 110, 82, SKIN[1]);
  for (let x = 108; x < 148; x++) for (let y = 86; y < 94; y++) if (SKIN.includes(g[y][x]) && !SKIN.includes(g[y + 1]?.[x])) g[y][x] = SKIN[0];

  despeckle(g, 1);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C2-レト", g)]; })();
