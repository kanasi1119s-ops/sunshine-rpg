/**
 * ドット絵の文字。ふつうの書体を小さく（12ドット）描いて、白黒（あり・なし）に区切り、黒いふちどりをつけて、
 * 論理の画面に1ドット＝1マスで写す。なめらかな縁（アンチエイリアス）が出ないので、ドット絵のゲームらしい文字になる。
 * 同じ文字列は一度作ったものを使いまわす。
 */
const FONT = "'Hiragino Sans', 'Yu Gothic', 'Noto Sans CJK JP', 'Noto Sans JP', sans-serif";
const cache = new Map<string, HTMLCanvasElement>();

export interface PixelTextOptions {
  /** 文字の大きさ（ドット）。既定 12。 */
  size?: number;
  color?: string;
  outline?: string;
  /** 太字にする（線をすこし太くする）。 */
  bold?: boolean;
}

function build(text: string, size: number, color: string, outline: string, bold: boolean): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  const m = document.createElement("canvas").getContext("2d");
  if (!m) return null;
  m.font = `${bold ? "bold " : ""}${size}px ${FONT}`;
  const textW = Math.ceil(m.measureText(text).width);
  const pad = 2;
  const w = textW + pad * 2;
  const h = size + pad * 2 + 2;
  const src = document.createElement("canvas");
  src.width = w;
  src.height = h;
  const g = src.getContext("2d", { willReadFrequently: true });
  if (!g) return null;
  g.font = m.font;
  g.textBaseline = "alphabetic";
  g.fillStyle = "#fff";
  g.fillText(text, pad, pad + size - 1);
  const data = g.getImageData(0, 0, w, h).data;
  const on = new Uint8Array(w * h);
  for (let i = 0; i < on.length; i++) on[i] = data[i * 4 + 3] >= (bold ? 80 : 120) ? 1 : 0;
  const out = document.createElement("canvas");
  out.width = w;
  out.height = h;
  const o = out.getContext("2d")!;
  const at = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && on[y * w + x] === 1;
  o.fillStyle = outline;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (at(x, y)) continue;
      if (at(x - 1, y) || at(x + 1, y) || at(x, y - 1) || at(x, y + 1) || at(x + 1, y + 1)) o.fillRect(x, y, 1, 1);
    }
  }
  o.fillStyle = color;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (at(x, y)) o.fillRect(x, y, 1, 1);
  return out;
}

/** ドット絵の文字を、中央・左・右のどれかにそろえて描く（y は文字の上のはし）。alpha は 0〜1。 */
export function drawPixelText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  align: "left" | "center" | "right" = "center",
  alpha = 1,
  opts: PixelTextOptions = {},
): void {
  if (!text) return;
  const size = opts.size ?? 12;
  const color = opts.color ?? "#faf0d2";
  const outline = opts.outline ?? "#1a1228";
  const bold = opts.bold ?? false;
  const key = `${size}|${color}|${outline}|${bold}|${text}`;
  let c = cache.get(key);
  if (!c) {
    const made = build(text, size, color, outline, bold);
    if (!made) return;
    c = made;
    cache.set(key, c);
  }
  const left = Math.round(align === "center" ? x - c.width / 2 : align === "right" ? x - c.width : x);
  const prevSmooth = ctx.imageSmoothingEnabled;
  const prevAlpha = ctx.globalAlpha;
  ctx.imageSmoothingEnabled = false;
  ctx.globalAlpha = prevAlpha * alpha;
  ctx.drawImage(c, left, Math.round(y));
  ctx.globalAlpha = prevAlpha;
  ctx.imageSmoothingEnabled = prevSmooth;
}
