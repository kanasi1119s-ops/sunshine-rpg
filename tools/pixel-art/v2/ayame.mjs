// C6-アヤメ（第6章加入・光断系）: 霜原の案内人。静かで丁寧、感情を見せない観察者。
// 藍がかった黒髪のぱっつん前髪と長い髪、毛皮えりの短い外套、藍の合わせ着、朱色の帯びと組みひも、腰に細身の刀。
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
  const OUT = pal.rgb("縁", "#0b0913"), RIM = pal.rgb("縁明", "#31304a");
  const SKIN = pal.ramp("肌", 18, 0.42, 4, 0.44, 0.88, 22);
  const HAIR = pal.ramp("髪", 246, 0.34, 4, 0.07, 0.42, 26);
  const IND = pal.ramp("藍", 230, 0.4, 4, 0.16, 0.5, 24);
  const CLK = pal.ramp("外套", 208, 0.16, 4, 0.34, 0.92, 22);
  const RED = pal.ramp("朱", 352, 0.8, 3, 0.28, 0.56, 14);
  const GOLD = pal.rgb("金", "#efc766");
  const WHITE = pal.rgb("白", "#f8f6fb");
  const C = { dark: OUT, iris: IND[2], irisDk: IND[1], white: WHITE, hi: WHITE };
  const g = makeGrid();
  const cx = 128;

  groundShadow(g, cx, 247, 54, 6, HAIR[0]);

  // ---------- 背中の長い髪（肩の外へ流れる） ----------
  vol(g, [{ cx, cy: 62, rx: 38, ry: 42 }, { cx, cy: 128, rx: 42, ry: 50, h: 0.9 }, { cx: cx - 14, cy: 150, rx: 22, ry: 34, h: 0.8 }, { cx: cx + 14, cy: 150, rx: 22, ry: 34, h: 0.8 }], HAIR, { box: [76, 10, 182, 190], ambient: 0.16, gain: 1.3, tex: (x, y) => (Math.sin(x * 0.7 + y * 0.05) > 0.92 ? 0.09 : 0) });

  // ---------- 長いスカート（ひだが広がる） ----------
  const skirt = [{ cx, cy: 176, rx: 27, ry: 30 }, { cx, cy: 210, rx: 38, ry: 26 }, { cx, cy: 228, rx: 42, ry: 14 }];
  vol(g, skirt, IND, { box: [76, 140, 180, 246], mask: (x, y) => y < 238 + Math.sin(x * 0.35) * 1.5, ambient: 0.13, gain: 1.1 });
  for (let k = -6; k <= 6; k++) {
    line(g, cx + k * 3, 162, cx + k * 6.6, 236, k % 2 ? IND[0] : IND[1]);
    if (k < 3) line(g, cx + k * 3 - 1, 166, cx + k * 6.6 - 1, 234, IND[3]);
  }
  // すそのふち（明るい線）
  for (let x = 90; x <= 166; x++) { const yy = 236 + Math.round(Math.sin(x * 0.35) * 1.5); if (g[yy]?.[x] >= 0 && IND.includes(g[yy][x])) { put(g, yy, x, IND[3]); put(g, yy - 1, x, IND[2]); } }
  // ブーツ
  for (const s of [-1, 1]) { ell(g, cx + s * 16, 241, 12, 6, HAIR, { ambient: 0.3, gain: 1.2 }); }

  // ---------- 首・胴 ----------
  tube(g, [[128, 84, 7], [128, 102, 8.5]], SKIN, { ambient: 0.2, gain: 1.0 });
  const torso = [{ cx, cy: 128, rx: 21, ry: 32 }, { cx, cy: 108, rx: 28, ry: 13 }, { cx, cy: 150, rx: 19, ry: 14 }];
  vol(g, torso, IND, { box: [94, 92, 164, 172], ambient: 0.15, gain: 1.2 });
  // 合わせ襟（Vのえり。うすい縁どり）
  fillPoly(g, [[116, 98], [124, 98], [140, 148], [132, 148]], (x, y) => (x - (116 + (y - 98) * 0.48) < 2.6 ? CLK[2] : IND[3]));
  fillPoly(g, [[140, 98], [132, 98], [116, 148], [124, 148]], (x, y) => ((140 - (y - 98) * 0.48) - x < 2.6 ? CLK[1] : IND[2]));
  line(g, 124, 100, 133, 146, IND[0]);
  // 見えている肌（Vの胸もと）
  fillPoly(g, [[122, 96], [134, 96], [128, 112]], (x, y) => SKIN[y > 106 ? 1 : 2]);
  // 帯（朱）と結び
  for (let y = 146; y < 162; y++) for (let x = 96; x <= 160; x++) { const half = 21 + (y - 146) * 0.25; if (Math.abs(x - cx) > half) continue; put(g, y, x, y < 148 ? RED[2] : y < 154 ? RED[1] : RED[0]); }
  for (let x = 108; x <= 148; x += 1) put(g, 146, x, RED[2]);
  // 帯じめの組みひも（金の留め）
  ell(g, cx, 154, 4, 5, [RED[0], GOLD, WHITE], { ambient: 0.4 });
  // ひもの垂れ
  line(g, 150, 158, 152, 188, RED[1]); line(g, 151, 158, 153, 188, RED[0]); line(g, 148, 158, 148, 184, RED[1]);
  ell(g, 152, 192, 3.4, 4.6, RED, { ambient: 0.3 });
  // 腰の細身の刀（左腰から右下がりに。さや・つば・朱の巻き）
  tube(g, [[112, 156, 3.6], [100, 186, 3.2], [92, 214, 2.6]], HAIR, { ambient: 0.2, gain: 1.2 });
  for (let t = 0; t < 4; t++) { const yy = 164 + t * 6, xx = 112 - (yy - 156) * 0.4; put(g, yy, Math.round(xx) - 1, RED[2]); put(g, yy, Math.round(xx), RED[1]); put(g, yy, Math.round(xx) + 1, RED[0]); }
  ell(g, 111, 157, 5, 3, [CLK[0], CLK[2], CLK[3]], { ambient: 0.5 }); // つば
  line(g, 91, 214, 89, 220, CLK[3]);
  tube(g, [[113, 152, 2.2], [115, 144, 2.2]], IND, { ambient: 0.2 });
  // ---------- 腕・広い袖（手は前で組む） ----------
  tube(g, [[100, 108, 10], [93, 132, 11.5], [100, 152, 12], [114, 162, 10]], IND, { ambient: 0.16, gain: 1.3 });
  tube(g, [[156, 108, 10], [163, 132, 11.5], [156, 152, 12], [142, 162, 10]], IND, { ambient: 0.14, gain: 1.3 });
  // 袖口の白い縁とかざり
  for (const s of [-1, 1]) for (let t = -8; t <= 8; t++) { const px = cx + s * 20 + t * 0.9 * (s > 0 ? -1 : 1) * 0, py = 160 + t * 0.0; }
  fillPoly(g, [[108, 154], [122, 166], [118, 172], [104, 162]], (x, y) => (x + y < 274 ? CLK[2] : CLK[1]));
  fillPoly(g, [[148, 154], [134, 166], [138, 172], [152, 162]], (x, y) => (y - x > -114 ? CLK[1] : CLK[0]));
  // 組んだ手
  ell(g, cx, 168, 11, 6.4, SKIN, { ambient: 0.3, gain: 1.4 });
  for (const dx of [-5, -1, 3]) { put(g, 166, cx + dx, SKIN[0]); put(g, 167, cx + dx, SKIN[0]); }
  line(g, 122, 171, 134, 171, SKIN[0]);

  // ---------- 外套（短い肩掛け）と毛皮えり ----------
  const cape = [{ cx, cy: 108, rx: 42, ry: 15 }, { cx, cy: 118, rx: 34, ry: 12 }];
  vol(g, cape, CLK, { box: [80, 88, 176, 140], mask: (x, y) => y < 128 + Math.round(Math.sin(x * 0.5) * 2) - Math.abs(x - cx) * 0.06 && !(Math.abs(x - cx) < 10 && y > 100), ambient: 0.16, gain: 1.3 });
  // 外套のすそ（ふち取りの暗線と、毛のふさふさ）
  for (let x = 88; x <= 168; x++) { for (let y = 112; y <= 136; y++) { if (CLK.includes(g[y][x]) && !CLK.includes(g[y + 1]?.[x]) && g[y + 1]?.[x] !== undefined) { put(g, y, x, CLK[3]); put(g, y - 1, x, CLK[2]); break; } } }
  // 毛皮のえり（ふくらむ輪）
  tube(g, [[104, 98, 7.5], [114, 106, 9], [128, 110, 9.6], [142, 106, 9], [152, 98, 7.5]], CLK, { ambient: 0.35, gain: 1.4, tex: (x, y) => (hash(x >> 1, y >> 1) < 0.18 ? -0.12 : hash(x, y) < 0.1 ? 0.1 : 0) });
  // 前の朱の組みひも（えりを留める）
  line(g, 120, 108, 125, 112, RED[1]); line(g, 136, 108, 131, 112, RED[1]);
  line(g, 125, 112, 131, 112, RED[2]); line(g, 128, 113, 128, 126, RED[1]); line(g, 129, 113, 129, 126, RED[0]);
  ell(g, 128, 129, 2.6, 3.4, RED, { ambient: 0.4 });

  // ---------- 頭 ----------
  ell(g, 101, 68, 4, 5.4, SKIN, { ambient: 0.35 }); ell(g, 155, 68, 4, 5.4, SKIN, { ambient: 0.2 });
  vol(g, [{ cx, cy: 54, rx: 28, ry: 33 }, { cx, cy: 72, rx: 21, ry: 19, h: 1 }], SKIN, { box: [90, 14, 168, 96], ambient: 0.4, gain: 1.15, k: 6 });
  // 目（すずしいつり目・長いまつげ）
  eyeF(g, cx - 12, 65, 5, 4, C, -1); eyeF(g, cx + 12, 65, 5, 4, C, 1);
  for (const s of [-1, 1]) { line(g, cx + s * 12 + s * 6, 62, cx + s * 12 + s * 8, 60, OUT); put(g, 66, cx + s * 12 + s * 7, OUT); }
  // まゆ（細くまっすぐ）
  for (let x = -8; x <= 7; x++) put(g, 56 + Math.round((x + 8) * -0.05), cx - 12 + x, x < -3 ? HAIR[2] : HAIR[1]);
  for (let x = -7; x <= 8; x++) put(g, 56 + Math.round((8 - x) * -0.05), cx + 12 + x, x > 3 ? HAIR[2] : HAIR[1]);
  // 鼻と口（小さく）
  put(g, 74, cx - 1, SKIN[1]); put(g, 75, cx - 1, SKIN[1]); put(g, 76, cx, SKIN[0]); put(g, 76, cx - 1, SKIN[0]);
  for (let x = -4; x <= 4; x++) put(g, 82, cx + x, Math.abs(x) < 3 ? RED[1] : RED[0]);
  for (let x = -2; x <= 2; x++) put(g, 83, cx + x, SKIN[1]);
  put(g, 81, cx - 1, RED[2]); put(g, 81, cx, RED[2]);
  // ほほ
  for (const [dx, dy] of [[-17, 74], [-16, 74], [17, 74], [16, 74]]) put(g, dy, cx + dx, SKIN[1]);

  // ---------- 前髪と左右の長い房（ぱっつん） ----------
  const tri = (v) => Math.abs((v % 1 + 1) % 1 - 0.5) * 2;
  const fringe = (x) => 49 + Math.round(tri((x - 96) / 8.5) * 1.6) + (Math.abs(x - cx) < 6 ? 1 : 0) - Math.round(Math.max(0, Math.abs(x - cx) - 24) * 0.5);
  const hairMask = (x, y) => { const dx = Math.abs(x - cx); if (dx > 35) return false; if (y < fringe(x)) return true; if (dx > 24 && y < 96) return true; return false; };
  vol(g, [{ cx, cy: 48, rx: 36, ry: 36 }, { cx, cy: 74, rx: 38, ry: 28, h: 0.9 }], HAIR, { box: [84, 4, 172, 110], mask: hairMask, ambient: 0.14, gain: 1.4, tex: (x, y) => { const band = 24 + ((x - cx - 3) / 34) ** 2 * 20; const d = Math.abs(y - band); return (d < 1.6 && x < cx + 26 ? 0.34 : 0) + (Math.sin(x * 0.75 + 0.8) > 0.93 ? 0.06 : 0) - (d >= 1.6 && d < 3 && x < cx + 26 ? 0.0 : 0); } });
  // 左右に垂れる長い房（前へ）
  const lock = (pts) => tube(g, pts, HAIR, { ambient: 0.14, gain: 1.4, tex: (x, y) => (Math.sin(x * 0.8) > 0.9 ? 0.08 : 0) });
  lock([[98, 66, 8], [95, 96, 8], [96, 124, 6], [100, 146, 2.4]]);
  lock([[158, 66, 8], [161, 96, 8], [160, 124, 6], [157, 146, 2.4]]);
  // 房の内側のすきま（顔と髪のさかいの影）
  for (let y = 52; y < 88; y++) for (const s of [-1, 1]) { const x = cx + s * (27 - Math.max(0, (y - 70)) * 0.9); if (SKIN.includes(g[y][Math.round(x)])) put(g, y, Math.round(x), SKIN[0]); }
  // 前髪の下の影
  for (let x = 98; x <= 158; x++) { const y = fringe(x); if (SKIN.includes(g[y + 1]?.[x])) put(g, y + 1, x, SKIN[1]); if (SKIN.includes(g[y + 2]?.[x]) && x % 2 === 0) put(g, y + 2, x, SKIN[2]); }
  // 髪かざり（銀の花と金のしずく）と、左の房の朱のひも
  for (const [dx, dy] of [[0, -5], [5, -1], [-5, -1], [-3, 4], [3, 4]]) ell(g, 152 + dx, 30 + dy, 3.6, 3.6, [CLK[1], CLK[2], CLK[3]], { ambient: 0.4 });
  ell(g, 152, 30, 2.4, 2.4, [RED[0], RED[1], RED[2]], { ambient: 0.5 });
  line(g, 152, 38, 152, 44, GOLD); put(g, 45, 152, GOLD); put(g, 46, 152, WHITE);
  for (let y = 100; y < 104; y++) for (let x = 90; x <= 103; x++) if (HAIR.includes(g[y][x])) put(g, y, x, y === 100 ? RED[2] : y === 101 ? RED[1] : RED[0]);

  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "C6-アヤメ", g)]; })();
