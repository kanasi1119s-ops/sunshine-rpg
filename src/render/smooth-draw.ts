/**
 * 大きな絵を、なめらかに縮めて描く（ボス・敵の絵・顔グラフィック）。
 * ゲームのキャンバスは文字をくっきり描くために論理の2〜4倍の細かさで描いている（`canvas.ts`）。
 * そのまま「なめらかに」拡大縮小すると、細かいキャンバスの上でぼやけた絵になるので、
 * いったん論理の大きさ（dw×dh）の別のキャンバスになめらかに縮めてから、最近傍で描く（前と同じ見た目）。
 */
type Src = HTMLCanvasElement | HTMLImageElement | ImageBitmap | OffscreenCanvas;

const cache = new WeakMap<object, Map<string, HTMLCanvasElement>>();

export function drawSmooth(
  ctx: CanvasRenderingContext2D,
  img: Src,
  sx: number, sy: number, sw: number, sh: number,
  dx: number, dy: number, dw: number, dh: number,
): void {
  const w = Math.max(1, Math.round(dw));
  const h = Math.max(1, Math.round(dh));
  const key = `${sx},${sy},${sw},${sh},${w},${h}`;
  let m = cache.get(img);
  if (!m) {
    m = new Map();
    cache.set(img, m);
  }
  let small = m.get(key);
  if (!small && typeof document !== "undefined") {
    small = document.createElement("canvas");
    small.width = w;
    small.height = h;
    const c = small.getContext("2d");
    if (c) {
      c.imageSmoothingEnabled = true;
      c.imageSmoothingQuality = "high";
      c.drawImage(img as CanvasImageSource, sx, sy, sw, sh, 0, 0, w, h);
    }
    m.set(key, small);
  }
  const prev = ctx.imageSmoothingEnabled;
  ctx.imageSmoothingEnabled = false;
  if (small) {
    ctx.drawImage(small, dx, dy, w, h);
  } else {
    ctx.drawImage(img as CanvasImageSource, sx, sy, sw, sh, dx, dy, dw, dh);
  }
  ctx.imageSmoothingEnabled = prev;
}
