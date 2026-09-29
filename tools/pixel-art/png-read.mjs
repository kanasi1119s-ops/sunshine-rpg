// PNG画像を読み込む最小限の関数（外部ライブラリを使わず、Node標準の zlib だけで読む）。
// 対応: 8ビットのパレット・グレー・RGB・RGBA（インターレースなし）。外部素材の取り込み（import-pipoya.mjs）で使う。
import fs from "fs";
import zlib from "zlib";

/** @returns {{ width: number, height: number, pixels: Uint8Array }} pixels は RGBA の並び */
export function readPng(path) {
  const buf = fs.readFileSync(path);
  if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error(`PNGではありません: ${path}`);
  let pos = 8, width = 0, height = 0, bitDepth = 0, colorType = 0, interlace = 0;
  let palette = null, trns = null;
  const idat = [];
  while (pos < buf.length) {
    const len = buf.readUInt32BE(pos);
    const type = buf.toString("ascii", pos + 4, pos + 8);
    const data = buf.subarray(pos + 8, pos + 8 + len);
    if (type === "IHDR") {
      width = data.readUInt32BE(0); height = data.readUInt32BE(4);
      bitDepth = data[8]; colorType = data[9]; interlace = data[12];
    } else if (type === "PLTE") palette = data;
    else if (type === "tRNS") trns = data;
    else if (type === "IDAT") idat.push(data);
    else if (type === "IEND") break;
    pos += 12 + len;
  }
  if (bitDepth !== 8 || interlace !== 0) throw new Error(`未対応のPNG形式（bitDepth=${bitDepth}, interlace=${interlace}）: ${path}`);
  const channels = { 0: 1, 2: 3, 3: 1, 4: 2, 6: 4 }[colorType];
  if (!channels) throw new Error(`未対応の色形式 ${colorType}: ${path}`);
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = width * channels;
  const rows = new Uint8Array(stride * height);
  for (let y = 0; y < height; y++) {
    const filter = raw[y * (stride + 1)];
    const src = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    const out = rows.subarray(y * stride, (y + 1) * stride);
    const prev = y > 0 ? rows.subarray((y - 1) * stride, y * stride) : null;
    for (let i = 0; i < stride; i++) {
      const a = i >= channels ? out[i - channels] : 0;
      const b = prev ? prev[i] : 0;
      const c = prev && i >= channels ? prev[i - channels] : 0;
      let v = src[i];
      if (filter === 1) v += a;
      else if (filter === 2) v += b;
      else if (filter === 3) v += (a + b) >> 1;
      else if (filter === 4) {
        const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
        v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      }
      out[i] = v & 255;
    }
  }
  const pixels = new Uint8Array(width * height * 4);
  for (let n = 0; n < width * height; n++) {
    const s = n * channels, d = n * 4;
    if (colorType === 3) {
      const k = rows[s];
      pixels[d] = palette[k * 3]; pixels[d + 1] = palette[k * 3 + 1]; pixels[d + 2] = palette[k * 3 + 2];
      pixels[d + 3] = trns && k < trns.length ? trns[k] : 255;
    } else if (colorType === 0 || colorType === 4) {
      pixels[d] = pixels[d + 1] = pixels[d + 2] = rows[s];
      pixels[d + 3] = colorType === 4 ? rows[s + 1] : 255;
    } else {
      pixels[d] = rows[s]; pixels[d + 1] = rows[s + 1]; pixels[d + 2] = rows[s + 2];
      pixels[d + 3] = colorType === 6 ? rows[s + 3] : 255;
    }
  }
  return { width, height, pixels };
}
