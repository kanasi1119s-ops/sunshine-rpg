/**
 * 曲の音量をそろえる仕上げ（書き出し用）。ITU-R BS.1770 の考え方（K特性フィルター＋ゲート付きの統合ラウドネス）で
 * 曲の「聞こえる大きさ」（LUFS）を測り、目標にそろえる。山（ピーク）だけをそろえるより、曲どうしの大きさが揃う。
 */
type Biquad = { b0: number; b1: number; b2: number; a1: number; a2: number };

/** BS.1770 の K特性（高域の持ち上げ＋低域のカット）を、サンプルレートに合わせて計算する。 */
function kWeighting(fs: number): Biquad[] {
  const f0 = 1681.974450955533, G = 3.999843853973347, Q = 0.7071752369554196;
  const K = Math.tan((Math.PI * f0) / fs);
  const Vh = Math.pow(10, G / 20), Vb = Math.pow(Vh, 0.4996667741545416);
  const a0 = 1 + K / Q + K * K;
  const shelf: Biquad = {
    b0: (Vh + (Vb * K) / Q + K * K) / a0, b1: (2 * (K * K - Vh)) / a0, b2: (Vh - (Vb * K) / Q + K * K) / a0,
    a1: (2 * (K * K - 1)) / a0, a2: (1 - K / Q + K * K) / a0,
  };
  const f1 = 38.13547087602444, Q2 = 0.5003270373238773;
  const K2 = Math.tan((Math.PI * f1) / fs);
  const d = 1 + K2 / Q2 + K2 * K2;
  const hp: Biquad = { b0: 1, b1: -2, b2: 1, a1: (2 * (K2 * K2 - 1)) / d, a2: (1 - K2 / Q2 + K2 * K2) / d };
  return [shelf, hp];
}

function filtered(x: Float32Array, stages: Biquad[]): Float32Array {
  let cur = x;
  for (const s of stages) {
    const y = new Float32Array(cur.length);
    let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    for (let i = 0; i < cur.length; i++) {
      const v = s.b0 * cur[i] + s.b1 * x1 + s.b2 * x2 - s.a1 * y1 - s.a2 * y2;
      x2 = x1; x1 = cur[i]; y2 = y1; y1 = v; y[i] = v;
    }
    cur = y;
  }
  return cur;
}

/** 統合ラウドネス（LUFS）。無音なら -Infinity。 */
export function measureLufs(channels: Float32Array[], sampleRate: number): number {
  const stages = kWeighting(sampleRate);
  const fl = channels.map((c) => filtered(c, stages));
  const block = Math.round(0.4 * sampleRate), hop = Math.round(0.1 * sampleRate);
  const powers: number[] = [];
  for (let s = 0; s + block <= fl[0].length; s += hop) {
    let sum = 0;
    for (const c of fl) { let e = 0; for (let i = s; i < s + block; i++) e += c[i] * c[i]; sum += e / block; }
    powers.push(sum);
  }
  if (!powers.length) return -Infinity;
  const lufs = (p: number) => -0.691 + 10 * Math.log10(p);
  const abs = powers.filter((p) => lufs(p) > -70);
  if (!abs.length) return -Infinity;
  const mean = (a: number[]) => a.reduce((x, y) => x + y, 0) / a.length;
  const rel = lufs(mean(abs)) - 10;
  const gated = abs.filter((p) => lufs(p) > rel);
  return gated.length ? lufs(mean(gated)) : -Infinity;
}

/** ceiling を超える山だけをなめらかに丸める（knee より下はそのまま）。 */
function softCeiling(x: number, knee: number, ceiling: number): number {
  const a = Math.abs(x);
  if (a <= knee) return x;
  const over = (a - knee) / (ceiling - knee);
  return Math.sign(x) * (knee + (ceiling - knee) * Math.tanh(over));
}

/**
 * 聞こえる大きさを targetLufs にそろえ、山は ceiling（0〜1）を超えないよう丸める。
 * 持ち上げは最大 +12dB まで（ほぼ無音の曲を無理に大きくしない）。戻り値は測った元の LUFS と かけた倍率（dB）。
 */
export function normalizeLoudness(channels: Float32Array[], sampleRate: number, targetLufs = -16, ceiling = 0.97): { measured: number; gainDb: number } {
  const measured = measureLufs(channels, sampleRate);
  if (!isFinite(measured)) return { measured, gainDb: 0 };
  const gainDb = Math.max(-24, Math.min(12, targetLufs - measured));
  const g = Math.pow(10, gainDb / 20);
  const knee = ceiling * 0.8;
  for (const c of channels) for (let i = 0; i < c.length; i++) c[i] = softCeiling(c[i] * g, knee, ceiling);
  return { measured, gainDb };
}
