/**
 * 純粋な信号処理の部品（Web Audio を使わない）。効果音のレシピを Float32Array に描く（sfx-synth.ts）、聞き比べ用の WAV 書き出し、
 * 検査（山・長さ・立ち上がり・帯域・重心）に使う。ブラウザでも Node（vitest・song.mjs）でも同じ結果になる。
 * docs/sound/synth-sfx-guide.md §3・§6・§7 の数字をそのまま使っている。
 */

/** 種つきの疑似乱数（mulberry32）。同じ種なら同じ列。 */
export function makeRng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export const dbToGain = (db: number): number => 10 ** (db / 20);
export const gainToDb = (g: number): number => 20 * Math.log10(Math.max(g, 1e-9));

export type Wave = "sine" | "triangle" | "square" | "sawtooth" | "pulse25" | "pulse12";

/** PolyBLEP（角のある波形のエイリアシングを減らす補正）。t は位相 0〜1、dt は 1 サンプルの位相の進み。 */
function polyBlep(t: number, dt: number): number {
  if (t < dt) { const x = t / dt; return x + x - x * x - 1; }
  if (t > 1 - dt) { const x = (t - 1) / dt; return x * x + x + x + 1; }
  return 0;
}

/** 位相 phase（0〜1）の波形の値。dt は 1 サンプルあたりの位相の進み（PolyBLEP 用）。 */
export function waveAt(wave: Wave, phase: number, dt: number): number {
  switch (wave) {
    case "sine": return Math.sin(2 * Math.PI * phase);
    case "triangle": return 4 * Math.abs(phase - Math.floor(phase + 0.5)) - 1;
    case "sawtooth": return 2 * phase - 1 - polyBlep(phase, dt);
    case "square": case "pulse25": case "pulse12": {
      const duty = wave === "square" ? 0.5 : wave === "pulse25" ? 0.25 : 0.125;
      let v = phase < duty ? 1 : -1;
      v += polyBlep(phase, dt);
      v -= polyBlep((phase - duty + 1) % 1, dt);
      return v - (2 * duty - 1); // 直流を除く
    }
  }
}

export type NoiseColor = "white" | "pink" | "brown";

/** ノイズ 1 本分の生成器（状態を持つ）。pink は Paul Kellet の近似、brown は漏れのある積分。 */
export function noiseGen(color: NoiseColor, rng: () => number): () => number {
  if (color === "white") return () => rng() * 2 - 1;
  if (color === "brown") {
    let last = 0;
    return () => {
      last = (last + 0.02 * (rng() * 2 - 1)) / 1.02;
      return last * 3.5;
    };
  }
  let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
  return () => {
    const w = rng() * 2 - 1;
    b0 = 0.99886 * b0 + w * 0.0555179; b1 = 0.99332 * b1 + w * 0.0750759; b2 = 0.969 * b2 + w * 0.153852;
    b3 = 0.8665 * b3 + w * 0.3104856; b4 = 0.55 * b4 + w * 0.5329522; b5 = -0.7616 * b5 - w * 0.016898;
    const out = b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362;
    b6 = w * 0.115926;
    return out * 0.11;
  };
}

export type FilterType = "lp" | "hp" | "bp";
export interface FilterSpec {
  type: FilterType;
  /** 周波数（Hz）。f1 があれば、f0 から f1 へ sweep 秒で指数的に動く。 */
  f0: number;
  f1?: number;
  sweep?: number;
  q?: number;
  /** 折れ線の動き [[秒, Hz], ...]（指数的に結ぶ）。あれば f0・f1 のかわりに使う。 */
  path?: [number, number][];
  /** 周波数をゆらす LFO（hz＝速さ、depth＝周波数の倍率の幅。0.3 なら ±30%）。 */
  lfo?: { hz: number; depth: number };
}

/** [[t, v], ...] を指数で結んだ時刻 t の値（範囲外は端の値）。 */
export function pathAt(path: [number, number][], t: number): number {
  if (t <= path[0][0]) return path[0][1];
  for (let i = 1; i < path.length; i++) {
    if (t <= path[i][0]) {
      const [t0, v0] = path[i - 1], [t1, v1] = path[i];
      return v0 * (v1 / v0) ** ((t - t0) / Math.max(1e-9, t1 - t0));
    }
  }
  return path[path.length - 1][1];
}

/** 2 次の biquad（RBJ クックブック）。周波数が時間で変わるので、係数は 32 サンプルごとに作り直す。 */
export class Biquad {
  private x1 = 0; private x2 = 0; private y1 = 0; private y2 = 0;
  private b0 = 1; private b1 = 0; private b2 = 0; private a1 = 0; private a2 = 0;
  constructor(private type: FilterType, private sr: number) {}
  set(freq: number, q: number): void {
    const f = Math.max(20, Math.min(freq, this.sr * 0.45));
    const w0 = (2 * Math.PI * f) / this.sr;
    const cos = Math.cos(w0);
    const alpha = Math.sin(w0) / (2 * Math.max(0.05, q));
    let b0: number, b1: number, b2: number;
    if (this.type === "lp") { b0 = (1 - cos) / 2; b1 = 1 - cos; b2 = b0; }
    else if (this.type === "hp") { b0 = (1 + cos) / 2; b1 = -(1 + cos); b2 = b0; }
    else { b0 = alpha; b1 = 0; b2 = -alpha; }
    const a0 = 1 + alpha;
    this.b0 = b0 / a0; this.b1 = b1 / a0; this.b2 = b2 / a0; this.a1 = (-2 * cos) / a0; this.a2 = (1 - alpha) / a0;
  }
  process(x: number): number {
    const y = this.b0 * x + this.b1 * this.x1 + this.b2 * this.x2 - this.a1 * this.y1 - this.a2 * this.y2;
    this.x2 = this.x1; this.x1 = x; this.y2 = this.y1; this.y1 = y;
    return y;
  }
}

/** FilterSpec の時間変化つきフィルターを、バッファ buf（sr）に開始 startSample から掛ける。 */
export function applyFilter(buf: Float32Array, spec: FilterSpec, sr: number, startSample = 0): void {
  const bq = new Biquad(spec.type, sr);
  const q = spec.q ?? 0.7;
  const sweepN = Math.max(1, Math.round((spec.sweep ?? 0.2) * sr));
  const ratio = spec.f1 ? spec.f1 / spec.f0 : 1;
  for (let i = 0; i < buf.length; i++) {
    if (i % 32 === 0) {
      const sec = (i - startSample) / sr;
      let f = spec.path ? pathAt(spec.path, sec) : spec.f0 * ratio ** Math.min(1, Math.max(0, (i - startSample) / sweepN));
      if (spec.lfo) f *= 1 + spec.lfo.depth * Math.sin(2 * Math.PI * spec.lfo.hz * sec);
      bq.set(f, q);
    }
    buf[i] = bq.process(buf[i]);
  }
}

/** A/D/S/R（秒、s は 0〜1）の音量の形。attack は直線、decay と release は指数。hold は s の高さで保つ秒。 */
export interface EnvSpec { a: number; d: number; s: number; r: number; hold?: number }
export const envLength = (e: EnvSpec): number => e.a + e.d + (e.hold ?? 0) + e.r;
export function envAt(e: EnvSpec, t: number): number {
  const a = Math.max(e.a, 0.002);
  const hold = e.hold ?? 0;
  const sus = Math.max(e.s, 0.0001);
  if (t < 0) return 0;
  if (t < a) return t / a;
  if (t < a + e.d) return e.d > 0 ? sus ** ((t - a) / e.d) : sus;
  if (t < a + e.d + hold) return e.s;
  const rt = t - a - e.d - hold;
  if (rt >= e.r) return 0;
  // 余韻は指数に近づけつつ、最後は 0 へ（クリック防止）
  const g = e.s * 0.0001 ** (rt / Math.max(e.r, 1e-4));
  return g * (1 - rt / e.r) ** 0.5;
}

/** 実数列のフーリエ変換の大きさ（2 のべきの長さに 0 を足す）。 */
export function magnitudeSpectrum(x: Float32Array, size = 8192): Float32Array {
  const n = size;
  const re = new Float64Array(n), im = new Float64Array(n);
  const len = Math.min(x.length, n);
  for (let i = 0; i < len; i++) re[i] = x[i] * (0.5 - 0.5 * Math.cos((2 * Math.PI * i) / Math.max(1, len - 1)));
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) { const t = re[i]; re[i] = re[j]; re[j] = t; }
  }
  for (let size2 = 2; size2 <= n; size2 <<= 1) {
    const ang = (-2 * Math.PI) / size2;
    const wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += size2) {
      let cr = 1, ci = 0;
      for (let k = 0; k < size2 / 2; k++) {
        const a = i + k, b = i + k + size2 / 2;
        const tr = re[b] * cr - im[b] * ci, ti = re[b] * ci + im[b] * cr;
        re[b] = re[a] - tr; im[b] = im[a] - ti; re[a] += tr; im[a] += ti;
        const ncr = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = ncr;
      }
    }
  }
  const out = new Float32Array(n / 2);
  for (let i = 0; i < n / 2; i++) out[i] = Math.hypot(re[i], im[i]);
  return out;
}

export interface SeAnalysis {
  peak: number;
  peakDb: number;
  rmsDb: number;
  /** 音が実質消えるまでの長さ（秒）。山から −50dB 以下になった最後の時刻。 */
  lengthSec: number;
  /** 山の 20% に最初に届く時刻（ミリ秒）。 */
  attackMs: number;
  /** 直流成分（平均）÷ 山。 */
  dc: number;
  /** スペクトル重心（Hz）。 */
  centroidHz: number;
  /** 1〜4kHz のエネルギーの割合（0〜1）。 */
  band1to4k: number;
}

/** 音の分析（山・長さ・立ち上がり・直流・重心・帯域）。 */
export function analyzeSamples(x: Float32Array, sr: number): SeAnalysis {
  let peak = 0, sum = 0, sq = 0;
  for (let i = 0; i < x.length; i++) { const a = Math.abs(x[i]); if (a > peak) peak = a; sum += x[i]; sq += x[i] * x[i]; }
  const floor = peak * 10 ** (-50 / 20);
  let last = 0, first = -1;
  for (let i = 0; i < x.length; i++) {
    const a = Math.abs(x[i]);
    if (a > floor) last = i;
    if (first < 0 && a >= peak * 0.2) first = i;
  }
  const spec = magnitudeSpectrum(x.subarray(0, Math.min(x.length, 16384)), 16384);
  let num = 0, den = 0, band = 0;
  for (let i = 1; i < spec.length; i++) {
    const f = (i * sr) / (spec.length * 2);
    const e = spec[i] * spec[i];
    num += f * e; den += e;
    if (f >= 1000 && f <= 4000) band += e;
  }
  return {
    peak, peakDb: gainToDb(peak), rmsDb: gainToDb(Math.sqrt(sq / Math.max(1, x.length))),
    lengthSec: (last + 1) / sr, attackMs: first < 0 ? 0 : (first / sr) * 1000,
    dc: peak > 0 ? Math.abs(sum / x.length) / peak : 0, centroidHz: den > 0 ? num / den : 0, band1to4k: den > 0 ? band / den : 0,
  };
}

/** 16 ビット・モノラルの WAV にする。 */
export function toWav16(x: Float32Array, sr: number): Uint8Array {
  const n = x.length;
  const out = new Uint8Array(44 + n * 2);
  const dv = new DataView(out.buffer);
  const wr = (o: number, s: string): void => { for (let i = 0; i < s.length; i++) out[o + i] = s.charCodeAt(i); };
  wr(0, "RIFF"); dv.setUint32(4, 36 + n * 2, true); wr(8, "WAVE"); wr(12, "fmt ");
  dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 1, true); dv.setUint32(24, sr, true);
  dv.setUint32(28, sr * 2, true); dv.setUint16(32, 2, true); dv.setUint16(34, 16, true); wr(36, "data"); dv.setUint32(40, n * 2, true);
  for (let i = 0; i < n; i++) dv.setInt16(44 + i * 2, Math.max(-32768, Math.min(32767, Math.round(x[i] * 32767))), true);
  return out;
}
