/**
 * FLAC（音質が落ちない圧縮）の書き出し。16ビット・ステレオ。
 * 各ブロックで、固定の予測（0〜4次）のうちいちばん小さくなるものを選び、残りをライス符号で詰める。
 */
class BitWriter {
  private buf = new Uint8Array(1 << 16);
  private len = 0;
  private acc = 0;
  private nbits = 0;
  private ensure(n: number): void {
    if (this.len + n <= this.buf.length) return;
    let size = this.buf.length * 2;
    while (size < this.len + n) size *= 2;
    const next = new Uint8Array(size);
    next.set(this.buf.subarray(0, this.len));
    this.buf = next;
  }
  write(value: number, bits: number): void {
    // 32ビットを超えないよう、分けて書く
    while (bits > 24) {
      bits -= 24;
      this.write(Math.floor(value / 2 ** bits) & 0xffffff, 24);
      value = value % 2 ** bits;
    }
    this.acc = (this.acc * 2 ** bits + (value & (2 ** bits - 1))) >>> 0;
    this.nbits += bits;
    this.ensure(4);
    while (this.nbits >= 8) {
      this.nbits -= 8;
      this.buf[this.len++] = (this.acc >>> this.nbits) & 255;
      this.acc &= (1 << this.nbits) - 1;
    }
  }
  unary(q: number): void {
    while (q >= 24) {
      this.write(0, 24);
      q -= 24;
    }
    this.write(1, q + 1);
  }
  align(): void {
    if (this.nbits > 0) this.write(0, 8 - this.nbits);
  }
  get length(): number {
    return this.len;
  }
  bytes(from = 0, to = this.len): Uint8Array {
    return this.buf.subarray(from, to);
  }
}

const CRC8 = new Uint8Array(256);
const CRC16 = new Uint16Array(256);
for (let i = 0; i < 256; i++) {
  let c = i;
  for (let k = 0; k < 8; k++) c = c & 0x80 ? ((c << 1) ^ 0x07) & 255 : (c << 1) & 255;
  CRC8[i] = c;
  let d = i << 8;
  for (let k = 0; k < 8; k++) d = d & 0x8000 ? ((d << 1) ^ 0x8005) & 0xffff : (d << 1) & 0xffff;
  CRC16[i] = d;
}
const crc8 = (b: Uint8Array): number => b.reduce((c, x) => CRC8[c ^ x], 0);
const crc16 = (b: Uint8Array): number => b.reduce((c, x) => ((c << 8) & 0xffff) ^ CRC16[(c >> 8) ^ x], 0);

const BLOCK = 4096;

function residuals(x: Int32Array, order: number): Int32Array {
  const n = x.length;
  const r = new Int32Array(n - order);
  for (let i = order; i < n; i++) {
    let p = 0;
    if (order === 1) p = x[i - 1];
    else if (order === 2) p = 2 * x[i - 1] - x[i - 2];
    else if (order === 3) p = 3 * x[i - 1] - 3 * x[i - 2] + x[i - 3];
    else if (order === 4) p = 4 * x[i - 1] - 6 * x[i - 2] + 4 * x[i - 3] - x[i - 4];
    r[i - order] = x[i] - p;
  }
  return r;
}

function riceCost(r: Int32Array, k: number): number {
  let bits = 0;
  for (let i = 0; i < r.length; i++) {
    const u = r[i] >= 0 ? r[i] * 2 : -r[i] * 2 - 1;
    bits += Math.floor(u / 2 ** k) + 1 + k;
  }
  return bits;
}

function writeSubframe(w: BitWriter, x: Int32Array, bps: number): void {
  // 無音・一定の値なら、定数として書く
  if (x.every((v) => v === x[0])) {
    w.write(0, 1);
    w.write(0, 6);
    w.write(0, 1);
    w.write(x[0] & (2 ** bps - 1), bps);
    return;
  }
  let best: { order: number; k: number; cost: number; r: Int32Array } = { order: 0, k: 0, cost: Infinity, r: new Int32Array(0) };
  for (let order = 0; order <= Math.min(4, x.length - 1); order++) {
    const r = residuals(x, order);
    let mean = 0;
    for (let i = 0; i < r.length; i++) mean += Math.abs(r[i]);
    mean = r.length ? mean / r.length : 0;
    const guess = Math.max(0, Math.min(14, Math.floor(Math.log2(Math.max(1, mean)))));
    for (const k of [guess - 1, guess, guess + 1].filter((v) => v >= 0 && v <= 14)) {
      const cost = riceCost(r, k) + order * bps;
      if (cost < best.cost) best = { order, k, cost, r };
    }
  }
  if (best.cost >= x.length * bps) {
    // 詰めても小さくならなければ、そのまま書く
    w.write(0, 1);
    w.write(1, 6);
    w.write(0, 1);
    for (let i = 0; i < x.length; i++) w.write(x[i] & (2 ** bps - 1), bps);
    return;
  }
  w.write(0, 1);
  w.write(8 | best.order, 6);
  w.write(0, 1);
  for (let i = 0; i < best.order; i++) w.write(x[i] & (2 ** bps - 1), bps);
  w.write(0, 2); // ライス符号（4ビットの引数）
  w.write(0, 4); // 区切りなし
  w.write(best.k, 4);
  for (let i = 0; i < best.r.length; i++) {
    const u = best.r[i] >= 0 ? best.r[i] * 2 : -best.r[i] * 2 - 1;
    w.unary(Math.floor(u / 2 ** best.k));
    if (best.k) w.write(u % 2 ** best.k, best.k);
  }
}

function utf8Number(n: number): number[] {
  if (n < 0x80) return [n];
  if (n < 0x800) return [0xc0 | (n >> 6), 0x80 | (n & 63)];
  if (n < 0x10000) return [0xe0 | (n >> 12), 0x80 | ((n >> 6) & 63), 0x80 | (n & 63)];
  if (n < 0x200000) return [0xf0 | (n >> 18), 0x80 | ((n >> 12) & 63), 0x80 | ((n >> 6) & 63), 0x80 | (n & 63)];
  return [0xf8 | (n >> 24), 0x80 | ((n >> 18) & 63), 0x80 | ((n >> 12) & 63), 0x80 | ((n >> 6) & 63), 0x80 | (n & 63)];
}

export function encodeFlac(channels: Float32Array[], sampleRate: number): Uint8Array {
  const left = channels[0];
  const right = channels[1] ?? channels[0];
  const frames = left.length;
  const toInt = (x: number): number => Math.round(Math.max(-1, Math.min(1, x)) * 32767);
  const w = new BitWriter();
  w.write(0x664c6143, 32); // "fLaC"
  // STREAMINFO（最後のメタデータ）
  w.write(1, 1);
  w.write(0, 7);
  w.write(34, 24);
  w.write(BLOCK, 16);
  w.write(BLOCK, 16);
  w.write(0, 24);
  w.write(0, 24);
  w.write(sampleRate, 20);
  w.write(1, 3); // 2チャンネル
  w.write(15, 5); // 16ビット
  w.write(Math.floor(frames / 2 ** 32), 4);
  w.write(frames >>> 0, 32);
  for (let i = 0; i < 4; i++) w.write(0, 32); // MD5（不明）
  const L = new Int32Array(BLOCK);
  const R = new Int32Array(BLOCK);
  for (let f = 0, index = 0; f < frames; f += BLOCK, index++) {
    const n = Math.min(BLOCK, frames - f);
    for (let i = 0; i < n; i++) {
      L[i] = toInt(left[f + i]);
      R[i] = toInt(right[f + i]);
    }
    const start = w.length;
    w.write(0x3ffe, 14);
    w.write(0, 1);
    w.write(0, 1); // 固定のブロックの大きさ
    w.write(n === BLOCK ? 12 : 7, 4); // 4096 か、最後に16ビットで書く
    w.write(0, 4); // サンプリング周波数は STREAMINFO のとおり
    w.write(1, 4); // 左右が別々
    w.write(4, 3); // 16ビット
    w.write(0, 1);
    for (const b of utf8Number(index)) w.write(b, 8);
    if (n !== BLOCK) w.write(n - 1, 16);
    w.write(crc8(w.bytes(start)), 8);
    writeSubframe(w, L.subarray(0, n), 16);
    writeSubframe(w, R.subarray(0, n), 16);
    w.align();
    w.write(crc16(w.bytes(start)), 16);
  }
  return w.bytes().slice();
}
