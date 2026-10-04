/**
 * タイトルロゴ（ドット絵）。「光」と「リング」がモチーフ。金色の文字 RINGLIGHT に、光の輪（リング）がななめにかかり、
 * その下に小さな CHRONICLE。文字の形は、ふつうの書体をごく小さく描いて白黒にしたもの（＝ドットの文字）を、ドット単位で
 * 色ぬり（上が白っぽく下が濃い金、ふちが明るい・暗い、黒いふちどり、影、ディザ）して作る。
 * 論理の画面に、整数倍（1倍・2倍）で、補間なしに描く。
 */
export const LOGO_NATIVE_W = 190;
export const LOGO_NATIVE_H = 56;

type RGBA = [number, number, number, number];

const GOLDS: string[] = ["#fffbd8", "#ffe880", "#ffc83a", "#eea01c", "#c06c10", "#82400a"];
const OUTLINE = "#2a1204";

function hex(c: string): RGBA {
  return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16), 255];
}

/** 文字を小さく描いて、白黒（あり・なし）の点の並びにする。 */
function textMask(text: string, fontPx: number, bold: boolean, letterSpacing: number, maxWidth: number): { w: number; h: number; on: Uint8Array } | null {
  if (typeof document === "undefined") return null;
  const c = document.createElement("canvas");
  c.width = maxWidth + 60;
  c.height = Math.ceil(fontPx * 1.5);
  const g = c.getContext("2d", { willReadFrequently: true });
  if (!g) return null;
  const serif = "Georgia, 'Times New Roman', 'Hiragino Mincho ProN', serif";
  let size = fontPx;
  const set = (): void => {
    g.font = `${bold ? "bold " : ""}${size}px ${serif}`;
    (g as unknown as { letterSpacing: string }).letterSpacing = `${letterSpacing}px`;
  };
  set();
  while (g.measureText(text).width > maxWidth && size > 6) {
    size -= 1;
    set();
  }
  g.fillStyle = "#fff";
  g.textBaseline = "alphabetic";
  const metrics = g.measureText(text);
  const x = Math.floor((c.width - metrics.width) / 2);
  const baseline = Math.round(fontPx * 1.05);
  g.fillText(text, x, baseline);
  const data = g.getImageData(0, 0, c.width, c.height).data;
  const on = new Uint8Array(c.width * c.height);
  for (let i = 0; i < on.length; i++) on[i] = data[i * 4 + 3] >= 120 ? 1 : 0;
  return { w: c.width, h: c.height, on };
}

function bounds(m: { w: number; h: number; on: Uint8Array }): { top: number; bottom: number; left: number; right: number } {
  let top = m.h, bottom = 0, left = m.w, right = 0;
  for (let y = 0; y < m.h; y++) {
    for (let x = 0; x < m.w; x++) {
      if (m.on[y * m.w + x]) {
        top = Math.min(top, y);
        bottom = Math.max(bottom, y);
        left = Math.min(left, x);
        right = Math.max(right, x);
      }
    }
  }
  return { top, bottom, left, right };
}

interface Layer {
  w: number;
  h: number;
  px: Uint8ClampedArray<ArrayBuffer>;
}

function newLayer(w: number, h: number): Layer {
  return { w, h, px: new Uint8ClampedArray(new ArrayBuffer(w * h * 4)) };
}

function put(l: Layer, x: number, y: number, c: RGBA): void {
  if (x < 0 || y < 0 || x >= l.w || y >= l.h) return;
  const i = (y * l.w + x) * 4;
  l.px[i] = c[0];
  l.px[i + 1] = c[1];
  l.px[i + 2] = c[2];
  l.px[i + 3] = c[3];
}

/** 文字のマスクを、金色のドット（ふちどり・影・ディザつき）にして、レイヤーに置く。 */
function paintGoldText(layer: Layer, mask: { w: number; h: number; on: Uint8Array }, ox: number, oy: number, palette: string[], outline: string): void {
  const b = bounds(mask);
  const at = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < mask.w && y < mask.h && mask.on[y * mask.w + x] === 1;
  const cols = palette.map(hex);
  const height = Math.max(1, b.bottom - b.top);
  // 影（右下へ2ドット）
  for (let y = 0; y < mask.h; y++) {
    for (let x = 0; x < mask.w; x++) {
      if (at(x - 1, y - 2) || at(x - 2, y - 2)) {
        if (!at(x, y)) put(layer, ox + x, oy + y, [0, 0, 0, 120]);
      }
    }
  }
  // ふちどり（まわり1ドット。斜めも）
  for (let y = -1; y <= mask.h; y++) {
    for (let x = -1; x <= mask.w; x++) {
      if (at(x, y)) continue;
      let near = false;
      for (let dy = -1; dy <= 1 && !near; dy++) for (let dx = -1; dx <= 1; dx++) if (at(x + dx, y + dy)) { near = true; break; }
      if (near) put(layer, ox + x, oy + y, hex(outline));
    }
  }
  // 文字の中: 上から下へ色の帯。帯の境目は市松でなじませる。ふちは明るく／暗く。
  for (let y = 0; y < mask.h; y++) {
    for (let x = 0; x < mask.w; x++) {
      if (!at(x, y)) continue;
      const t = ((y - b.top) / height) * (cols.length - 1);
      let band = Math.floor(t);
      const frac = t - band;
      if (frac > 0.6 && (x + y) % 2 === 0) band += 1;
      band = Math.min(cols.length - 1, band);
      let c = cols[band];
      if (!at(x, y - 1)) c = cols[0]; // 上のふち: いちばん明るい
      else if (!at(x - 1, y)) c = cols[Math.max(0, band - 1)]; // 左のふち: 明るく
      else if (!at(x, y + 1) || !at(x + 1, y)) c = cols[Math.min(cols.length - 1, band + 1)]; // 下・右のふち: 暗く
      put(layer, ox + x, oy + y, c);
    }
  }
}

/** 光のリング（ななめの楕円）。中心が白く、外へ金・だいだい、まわりにディザの光。front=true は手前（下半分）、false は奥（上半分）。 */
function paintRing(layer: Layer, cx: number, cy: number, rx: number, ry: number, tilt: number, front: boolean): void {
  const cos = Math.cos(-tilt);
  const sin = Math.sin(-tilt);
  const core = hex("#ffffff");
  const gold = hex("#ffe070");
  const amber = hex("#f0a020");
  const glow = hex("#ffd060");
  for (let y = 0; y < layer.h; y++) {
    for (let x = 0; x < layer.w; x++) {
      const dx = x - cx;
      const dy = y - cy;
      const lx = dx * cos - dy * sin;
      const ly = dx * sin + dy * cos;
      const isFront = ly >= 0;
      if (isFront !== front) continue;
      const d = Math.abs(Math.hypot(lx / rx, ly / ry) - 1) * Math.min(rx, ry); // リングの中心線からの、ドットで数えた近さ
      const thick = 0.7 + 0.45 * Math.abs(ly / ry); // 手前・奥のはしほど太く
      if (d < thick * 0.7) put(layer, x, y, core);
      else if (d < thick * 1.5) put(layer, x, y, gold);
      else if (d < thick * 2.4) put(layer, x, y, amber);
      else if (d < thick * 3.6 && (x + y) % 2 === 0) put(layer, x, y, [glow[0], glow[1], glow[2], 200]);
      else if (d < thick * 5.2 && x % 2 === 0 && y % 2 === 0) put(layer, x, y, [glow[0], glow[1], glow[2], 120]);
    }
  }
}

function toCanvas(l: Layer): HTMLCanvasElement {
  const c = document.createElement("canvas");
  c.width = l.w;
  c.height = l.h;
  const g = c.getContext("2d")!;
  g.putImageData(new ImageData(l.px, l.w, l.h), 0, 0);
  return c;
}

let cached: HTMLCanvasElement | null = null;
let scratch: HTMLCanvasElement | null = null;

/** 土台のロゴ（RINGLIGHT ＋ リング ＋ CHRONICLE）。ブラウザ以外では null。 */
export function getPixelLogo(title: string): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  if (cached) return cached;
  const words = title.replace(/（.*?）/g, "").trim().split(/\s+/);
  const main = (words[0] ?? title).toUpperCase();
  const sub = words.slice(1).join(" ").toUpperCase();
  const W = LOGO_NATIVE_W;
  const H = LOGO_NATIVE_H;
  const mainMask = textMask(main, 34, true, 1, 134);
  if (!mainMask) return null;
  const mb = bounds(mainMask);
  const mainW = mb.right - mb.left + 1;
  const mainH = mb.bottom - mb.top + 1;
  const ox = Math.round((W - mainMask.w) / 2);
  const TOP = 13;
  const oy = TOP - mb.top;
  const textCy = TOP + mainH / 2 + 2;

  const back = newLayer(W, H);
  const textLayer = newLayer(W, H);
  const front = newLayer(W, H);
  const ringRx = Math.min(W / 2 - 20, mainW / 2 + 10);
  paintRing(back, W / 2, textCy, ringRx, 9, -0.13, false);
  paintRing(front, W / 2, textCy, ringRx, 9, -0.13, true);
  paintGoldText(textLayer, mainMask, ox, oy, GOLDS, OUTLINE);
  // CHRONICLE（小さく。白から水色）
  if (sub) {
    const subMask = textMask(sub, 12, true, 4, 110);
    if (subMask) {
      const sb = bounds(subMask);
      const sx = Math.round((W - subMask.w) / 2);
      const sy = Math.round(TOP + mainH + 14) - sb.top;
      paintGoldText(textLayer, subMask, sx, sy, ["#ffffff", "#e8f6ff", "#bfe4ff", "#8ac4f0", "#5a98d0", "#3a6a9c"], "#0c1a30");
      // 左右の飾り（ひし形の光と線）
      const lineY = sy + Math.round((sb.top + sb.bottom) / 2);
      const x0 = sx + sb.left - 6;
      const x1 = sx + sb.right + 6;
      for (let i = 0; i < 26; i++) {
        const a: RGBA = [255, 224, 112, Math.max(0, 255 - i * 9)];
        put(textLayer, x0 - i, lineY, a);
        put(textLayer, x1 + i, lineY, a);
      }
      for (const [dx, dy] of [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]) {
        put(textLayer, x0 + dx, lineY + dy, hex("#ffffff"));
        put(textLayer, x1 + dx, lineY + dy, hex("#ffffff"));
      }
    }
  }
  // 合成: 奥のリング → 文字 → 手前のリング
  const out = document.createElement("canvas");
  out.width = W;
  out.height = H;
  const g = out.getContext("2d")!;
  g.imageSmoothingEnabled = false;
  g.drawImage(toCanvas(back), 0, 0);
  g.drawImage(toCanvas(textLayer), 0, 0);
  g.drawImage(toCanvas(front), 0, 0);
  cached = out;
  return out;
}

/** ロゴのリングの上の、きらめきの位置（ロゴの左上を原点にした、ドットの座標）。 */
const SPARKLES: [number, number][] = [[24, 26], [160, 22], [96, 38], [60, 36], [132, 18]];

/**
 * ロゴを描く。scale は整数（1か2）。shine は 0〜1 なら、光の帯が文字の上を走る（範囲外は走らない）。
 * ms は、きらめきの点滅用の時間。
 */
export function drawPixelLogo(ctx: CanvasRenderingContext2D, title: string, cx: number, cy: number, scale: number, shine: number, ms: number): void {
  const logo = getPixelLogo(title);
  if (!logo) return;
  let src: HTMLCanvasElement = logo;
  if (shine >= 0 && shine <= 1) {
    if (!scratch) {
      scratch = document.createElement("canvas");
      scratch.width = logo.width;
      scratch.height = logo.height;
    }
    const g = scratch.getContext("2d")!;
    g.clearRect(0, 0, scratch.width, scratch.height);
    g.drawImage(logo, 0, 0);
    g.save();
    g.globalCompositeOperation = "source-atop";
    const x = -20 + shine * (logo.width + 40);
    g.fillStyle = "rgba(255,255,255,0.85)";
    // ななめの帯（ドットの階段）
    for (let y = 0; y < logo.height; y++) {
      g.fillRect(Math.round(x - y * 0.5), y, 7, 1);
    }
    g.restore();
    src = scratch;
  }
  const dw = logo.width * scale;
  const dh = logo.height * scale;
  const left = Math.round(cx - dw / 2);
  const top = Math.round(cy - dh / 2);
  const prev = ctx.imageSmoothingEnabled;
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(src, left, top, dw, dh);
  // きらめき（十字の光。ゆっくり点滅）
  SPARKLES.forEach(([sx, sy], i) => {
    const phase = (ms / 700 + i * 0.37) % 1;
    const size = phase < 0.5 ? Math.round(phase * 2 * 3) : Math.round((1 - phase) * 2 * 3);
    if (size <= 0) return;
    const px = left + sx * scale;
    const py = top + sy * scale;
    ctx.fillStyle = "#ffffff";
    for (let k = -size; k <= size; k++) {
      ctx.fillRect(px + k * scale, py, scale, scale);
      ctx.fillRect(px, py + k * scale, scale, scale);
    }
  });
  ctx.imageSmoothingEnabled = prev;
}
