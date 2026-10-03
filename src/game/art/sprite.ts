/**
 * 大きなドット絵（地形128×128、ボス・登場人物256×256、雑魚の敵64×64）のデータ形式と読み込み。
 * 色は「色番号A〜Z（透明は_）＋続く個数（36進数の小文字。1個なら省略）」の並び（RLE）で持ち、
 * 元データは tools/pixel-art/ で作る。容量を抑えるため、画像ファイルは使わない。
 */
export interface SpriteData {
  size: number;
  palette: string[];
  rle: string;
}

/** 色番号の並び。透明は -1。 */
export function decodeSprite(data: SpriteData): Int8Array {
  const total = data.size * data.size;
  const cells = new Int8Array(total).fill(-1);
  if (data.rle.startsWith("~")) {
    // 色が27色以上の絵: 「色番号:続く数」をカンマでつないだ形式
    let pos = 0;
    for (const token of data.rle.slice(1).split(",")) {
      const [value, count] = token.split(":").map(Number);
      for (let k = 0; k < count && pos < total; k++) {
        cells[pos++] = value;
      }
    }
    return cells;
  }
  let pos = 0;
  let i = 0;
  const s = data.rle;
  while (i < s.length && pos < total) {
    const ch = s[i++];
    const value = ch === "_" ? -1 : ch.charCodeAt(0) - 65;
    let digits = "";
    while (i < s.length && /[0-9a-z]/.test(s[i])) {
      digits += s[i++];
    }
    const count = digits ? parseInt(digits, 36) : 1;
    for (let k = 0; k < count && pos < total; k++) {
      cells[pos++] = value;
    }
  }
  return cells;
}

const canvasCache = new Map<string, HTMLCanvasElement>();

/** 画面に描くためのキャンバスを作って使い回す（ブラウザ以外では null）。 */
export function getSpriteCanvas(
  key: string,
  table: Record<string, SpriteData>,
  paletteOverride?: string[],
): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  const cacheKey = paletteOverride ? `${key}|${paletteOverride.join("")}` : key;
  const cached = canvasCache.get(cacheKey);
  if (cached) {
    return cached;
  }
  const data = table[key];
  if (!data) {
    return null;
  }
  const cells = decodeSprite(data);
  const canvas = document.createElement("canvas");
  canvas.width = data.size;
  canvas.height = data.size;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return null;
  }
  const image = ctx.createImageData(data.size, data.size);
  const rgb = (paletteOverride ?? data.palette).map((hex) => {
    const v = parseInt(hex.slice(1), 16);
    return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
  });
  for (let n = 0; n < cells.length; n++) {
    const k = cells[n];
    if (k < 0 || !rgb[k]) {
      continue;
    }
    image.data[n * 4] = rgb[k][0];
    image.data[n * 4 + 1] = rgb[k][1];
    image.data[n * 4 + 2] = rgb[k][2];
    image.data[n * 4 + 3] = 255;
  }
  ctx.putImageData(image, 0, 0);
  canvasCache.set(cacheKey, canvas);
  return canvas;
}
