/**
 * 自動ミックスの「測る」部分（2026-10-14）。耳では確かめられないので、パートごと・全体を数字にする。
 * 波形（左右の Float32Array）だけを入力にする純関数なので、ブラウザ（作曲ソフトの書き出し）でも Node でもテストでも同じに動く。
 *   - ラウドネス: 統合 LUFS（ゲート付き・BS.1770）、ショートターム（3 秒）の最大と中央値、サンプルピーク、RMS、クレストファクター
 *   - 帯域: Sub 20-60 / Bass 60-120 / Low-mid 120-250 / Mud 250-500 / Mid 500-2k / Presence 2-5k / Air 5k+（+ 濁り判定用の 200-500Hz）
 *   - スペクトル重心、ステレオの相関・幅（Side/Mid）・左右バランス・低域（150Hz 以下）の相関
 *   - 時間窓ごとの帯域の強さ（パート間のマスキング診断に使う）
 * 使い方と目標値は docs/sound/band-ensemble/auto-mix.md。
 */
import { filtered, kWeighting } from "./loudness";

export type BandId = "sub" | "bass" | "lowmid" | "mud" | "mid" | "presence" | "air";
export interface BandDef { id: BandId; label: string; lo: number; hi: number }

/** 7 帯域（依頼の定義）。air は 5kHz 以上〜20kHz。 */
export const BANDS: BandDef[] = [
  { id: "sub", label: "Sub 20-60", lo: 20, hi: 60 },
  { id: "bass", label: "Bass 60-120", lo: 60, hi: 120 },
  { id: "lowmid", label: "Low-mid 120-250", lo: 120, hi: 250 },
  { id: "mud", label: "Mud 250-500", lo: 250, hi: 500 },
  { id: "mid", label: "Mid 500-2k", lo: 500, hi: 2000 },
  { id: "presence", label: "Presence 2-5k", lo: 2000, hi: 5000 },
  { id: "air", label: "Air 5k+", lo: 5000, hi: 20000 },
];
/** 濁り（団子）の判定に使う帯域（mixing-guide: 200〜500Hz、特に 200〜350Hz）。時間窓の配列では BANDS の次（添字 7）に入れる。 */
export const MUD_RANGE: [number, number] = [200, 500];
export const BAND_IDS: BandId[] = BANDS.map((b) => b.id);
/** 窓ごとの配列の列数 = 7 帯域 + 200-500Hz */
export const WIN_COLS = BANDS.length + 1;
export const MUD_COL = BANDS.length;

export const FFT_SIZE = 4096;
const FLOOR_DB = -120;

const db10 = (p: number): number => (p > 1e-12 ? 10 * Math.log10(p) : FLOOR_DB);
const round1 = (v: number): number => (Number.isFinite(v) ? Math.round(v * 10) / 10 : v);

/** 実数 2 列を 1 回の複素 FFT で変換する（re=左, im=右 を入れる）。長さは 2 のべき乗。 */
export function fftInPlace(re: Float64Array, im: Float64Array): void {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) { const tr = re[i]; re[i] = re[j]; re[j] = tr; const ti = im[i]; im[i] = im[j]; im[j] = ti; }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (-2 * Math.PI) / len, wr = Math.cos(ang), wi = Math.sin(ang);
    const half = len >> 1;
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      for (let k = 0; k < half; k++) {
        const a = i + k, b = a + half;
        const tr = re[b] * cr - im[b] * ci, ti = re[b] * ci + im[b] * cr;
        re[b] = re[a] - tr; im[b] = im[a] - ti; re[a] += tr; im[a] += ti;
        const nr = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = nr;
      }
    }
  }
}

export interface StereoStats {
  /** 左右の相関（-1〜1。1 = モノ） */
  corr: number;
  /** Side の力 − Mid の力（dB。大きいほど広い。-∞ に近いほどモノ） */
  widthDb: number;
  /** 右 − 左 の力（dB。0 = 釣り合い。プラスは右寄り） */
  balanceDb: number;
  /** 150Hz 以下の左右の相関（1 に近くないと、モノで低音が痩せる） */
  lowCorr: number;
}

export interface AnalyzeOptions {
  /** マスキング診断用の時間窓（秒）。0 または省略で窓の配列を作らない。 */
  windowSec?: number;
  /** true なら 1 本の平均スペクトルも返す（全体の傾きの計算用） */
  meanSpectrum?: boolean;
}

export interface Analysis {
  seconds: number;
  sampleRate: number;
  lufsIntegrated: number;
  lufsShortMax: number;
  /** ショートターム（3 秒）の中央値（鳴っている間だけ） */
  lufsShortMedian: number;
  samplePeakDb: number;
  /** 左右の力の平均の RMS（dBFS、無音も含めた全体）。Mid ではなく左右の力で測るので、パンを振っても値が変わらない（analyze-stems.py の share_dB は Mid なので、広いギターは約 2〜3dB 小さく出ている） */
  rmsDb: number;
  /** 鳴っている間（ブロックの LUFS が -70 より上）だけの RMS（dBFS） */
  activeRmsDb: number;
  /** サンプルピーク − 鳴っている間の RMS（dB。小さいほどつぶれている） */
  crestDb: number;
  /** 鳴っている時間の割合（0〜1。100ms ごとに、いちばん大きい所の -35dB より上かどうか） */
  activity: number;
  /** 帯域の力（その音の全体を 0dB とした dB） */
  bandShareDb: Record<BandId, number>;
  /** 帯域の力（dBFS 相当の絶対値。パート同士を比べるのに使う） */
  bandAbsDb: Record<BandId, number>;
  /** 200-500Hz の力（全体に対する dB） */
  mudShareDb: number;
  centroidHz: number;
  stereo: StereoStats;
  /** 時間窓ごとの帯域の力（dB、[窓][WIN_COLS]）。windowSec を渡したときだけ */
  windows?: number[][];
  /** 時間窓ごとの全帯域の力（dB） */
  windowTotal?: number[];
  windowSec?: number;
  /** 平均スペクトル（1 ビンあたりの平均 2 乗。meanSpectrum: true のときだけ） */
  meanSpec?: number[];
}

function emptyBands(v: number): Record<BandId, number> {
  return { sub: v, bass: v, lowmid: v, mud: v, mid: v, presence: v, air: v };
}

/**
 * 波形を測る。左右が同じ長さ・サンプルレートであること。
 * ラウドネスは BS.1770 の K 特性、帯域は Hann 窓 4096 点の FFT（半分ずつ重ねる）で測る。
 */
export function analyzeChannels(left: Float32Array, right: Float32Array, sampleRate: number, opts: AnalyzeOptions = {}): Analysis {
  const n = Math.min(left.length, right.length);
  const seconds = n / sampleRate;
  const sr = sampleRate;

  // ── ラウドネス（K 特性）と RMS（100ms ごとに合計） ──
  const stages = kWeighting(sr);
  const kl = filtered(left.length === n ? left : left.subarray(0, n), stages);
  const kr = filtered(right.length === n ? right : right.subarray(0, n), stages);
  const hop = Math.round(0.1 * sr);
  const hops = Math.floor(n / hop);
  const kHop = new Float64Array(hops); // K 特性後の 2 乗の和（左+右）
  const rawHop = new Float64Array(hops); // 左右の 2 乗の平均の和
  let peak = 0, sumLL = 0, sumRR = 0, sumLR = 0;
  for (let h = 0; h < hops; h++) {
    let k = 0, r = 0;
    for (let i = h * hop, e = i + hop; i < e; i++) {
      const l = left[i], rr = right[i];
      k += kl[i] * kl[i] + kr[i] * kr[i];
      r += (l * l + rr * rr) * 0.5; // 左右の力の平均（パンの位置に左右されない）
      const al = Math.abs(l), ar = Math.abs(rr);
      if (al > peak) peak = al;
      if (ar > peak) peak = ar;
      sumLL += l * l; sumRR += rr * rr; sumLR += l * rr;
    }
    kHop[h] = k; rawHop[h] = r;
  }
  const lufsOf = (p: number): number => (p > 0 ? -0.691 + 10 * Math.log10(p) : -Infinity);
  const blockPow: number[] = []; // 400ms ブロック（100ms ずつずらす）
  for (let h = 0; h + 4 <= hops; h++) blockPow.push((kHop[h] + kHop[h + 1] + kHop[h + 2] + kHop[h + 3]) / (4 * hop));
  const absGated = blockPow.filter((p) => lufsOf(p) > -70);
  let lufsIntegrated = -Infinity;
  if (absGated.length) {
    const mean = (a: number[]): number => a.reduce((x, y) => x + y, 0) / a.length;
    const rel = lufsOf(mean(absGated)) - 10;
    const gated = absGated.filter((p) => lufsOf(p) > rel);
    lufsIntegrated = gated.length ? lufsOf(mean(gated)) : -Infinity;
  }
  // ショートターム: 3 秒（30 ホップ）の平均、1 秒ごと
  const shorts: number[] = [];
  for (let h = 0; h + 30 <= hops; h += 10) {
    let s = 0;
    for (let j = 0; j < 30; j++) s += kHop[h + j];
    shorts.push(lufsOf(s / (30 * hop)));
  }
  const activeShorts = shorts.filter((v) => v > -70).sort((a, b) => a - b);
  const lufsShortMax = activeShorts.length ? activeShorts[activeShorts.length - 1] : -Infinity;
  const lufsShortMedian = activeShorts.length ? activeShorts[Math.floor((activeShorts.length - 1) / 2)] : -Infinity;
  // RMS
  let rawAll = 0, rawActive = 0, activeHops = 0;
  const hopLufs = Array.from({ length: hops }, (_, h) => lufsOf(kHop[h] / hop));
  const hopMax = hopLufs.reduce((a, b) => Math.max(a, b), -Infinity);
  let loudHops = 0;
  for (let h = 0; h < hops; h++) {
    rawAll += rawHop[h];
    if (hopLufs[h] > -70) { rawActive += rawHop[h]; activeHops++; }
    if (hopLufs[h] > hopMax - 35) loudHops++;
  }
  const rmsDb = db10(hops ? rawAll / (hops * hop) : 0) ;
  const activeRmsDb = db10(activeHops ? rawActive / (activeHops * hop) : 0);
  const samplePeakDb = peak > 0 ? 20 * Math.log10(peak) : FLOOR_DB;

  // ── 帯域・重心・ステレオ（FFT） ──
  const N = FFT_SIZE, half = N / 2, fhop = N / 2;
  const hann = new Float64Array(N);
  let hann2 = 0;
  for (let i = 0; i < N; i++) { hann[i] = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / N); hann2 += hann[i] * hann[i]; }
  const norm = 1 / (N * hann2); // 全ビンの p の合計 = 平均 2 乗
  const binHz = sr / N;
  const colRange = (lo: number, hi: number): [number, number] => [Math.max(1, Math.ceil(lo / binHz)), Math.min(half - 1, Math.ceil(hi / binHz) - 1)];
  const cols: [number, number][] = [...BANDS.map((b) => colRange(b.lo, b.hi)), colRange(MUD_RANGE[0], MUD_RANGE[1])];
  const lowTop = Math.min(half - 1, Math.ceil(150 / binHz) - 1);
  const frames = n >= N ? Math.floor((n - N) / fhop) + 1 : 0;
  const re = new Float64Array(N), im = new Float64Array(N);
  const bandSum = new Float64Array(WIN_COLS); // 全フレームの平均 2 乗（左右平均）の合計
  let totalSum = 0, wSum = 0, wfSum = 0;
  let mSum = 0, sSum = 0, lSum = 0, rSum = 0; // 全体の Mid / Side / 左 / 右
  let lowLL = 0, lowRR = 0, lowLR = 0;
  const wantSpec = !!opts.meanSpectrum;
  const meanSpec = wantSpec ? new Float64Array(half + 1) : null;
  const winLen = opts.windowSec && opts.windowSec > 0 ? opts.windowSec : 0;
  const nWin = winLen ? Math.max(1, Math.ceil(seconds / winLen)) : 0;
  const winAcc = nWin ? Array.from({ length: nWin }, () => new Float64Array(WIN_COLS + 2)) : []; // [..cols, total, frames]
  for (let f = 0; f < frames; f++) {
    const o = f * fhop;
    for (let i = 0; i < N; i++) { re[i] = left[o + i] * hann[i]; im[i] = right[o + i] * hann[i]; }
    fftInPlace(re, im);
    const wi = nWin ? Math.min(nWin - 1, Math.floor(((o + N / 2) / sr) / winLen)) : 0;
    const acc = nWin ? winAcc[wi] : null;
    // 帯域ごと
    const pl = new Float64Array(half + 1), pr = new Float64Array(half + 1);
    for (let k = 1; k < half; k++) {
      const k2 = N - k;
      const zr = re[k], zi = im[k], cr = re[k2], ci = -im[k2]; // Z[k] と Z*[N-k]
      const xlr = (zr + cr) * 0.5, xli = (zi + ci) * 0.5; // 左のスペクトル
      const xrr = (zi - ci) * 0.5, xri = -(zr - cr) * 0.5; // 右のスペクトル（(Z[k]-Z*[N-k])/(2i)）
      pl[k] = 2 * norm * (xlr * xlr + xli * xli);
      pr[k] = 2 * norm * (xrr * xrr + xri * xri);
      const cross = 2 * norm * (xlr * xrr + xli * xri);
      const pm = (pl[k] + pr[k] + 2 * cross) / 4, ps = (pl[k] + pr[k] - 2 * cross) / 4;
      mSum += pm; sSum += ps; lSum += pl[k]; rSum += pr[k];
      if (k <= lowTop) { lowLL += pl[k]; lowRR += pr[k]; lowLR += cross; }
    }
    // DC・ナイキストは測らない（ごく小さい）
    let ftot = 0;
    for (let k = 1; k < half; k++) {
      const p = (pl[k] + pr[k]) * 0.5;
      ftot += p;
      wSum += p; wfSum += p * k * binHz;
      if (meanSpec) meanSpec[k] += p;
    }
    totalSum += ftot;
    for (let c = 0; c < WIN_COLS; c++) {
      let s = 0;
      for (let k = cols[c][0]; k <= cols[c][1]; k++) s += (pl[k] + pr[k]) * 0.5;
      bandSum[c] += s;
      if (acc) acc[c] += s;
    }
    if (acc) { acc[WIN_COLS] += ftot; acc[WIN_COLS + 1] += 1; }
  }
  const bandAbsDb = emptyBands(FLOOR_DB), bandShareDb = emptyBands(FLOOR_DB);
  const nf = Math.max(1, frames);
  BANDS.forEach((b, i) => {
    bandAbsDb[b.id] = round1(db10(bandSum[i] / nf));
    bandShareDb[b.id] = round1(totalSum > 0 ? db10(bandSum[i] / totalSum) : FLOOR_DB);
  });
  const mudShareDb = round1(totalSum > 0 ? db10(bandSum[MUD_COL] / totalSum) : FLOOR_DB);
  const corr = sumLL > 0 && sumRR > 0 ? sumLR / Math.sqrt(sumLL * sumRR) : 0;
  const lowCorr = lowLL > 0 && lowRR > 0 ? lowLR / Math.sqrt(lowLL * lowRR) : 1;
  const stereo: StereoStats = {
    corr: Math.round(corr * 1000) / 1000,
    widthDb: round1(mSum > 0 && sSum > 0 ? db10(sSum / mSum) : FLOOR_DB),
    balanceDb: round1(lSum > 0 && rSum > 0 ? db10(rSum / lSum) : 0),
    lowCorr: Math.round(lowCorr * 1000) / 1000,
  };
  const out: Analysis = {
    seconds: round1(seconds), sampleRate: sr,
    lufsIntegrated: round1(lufsIntegrated), lufsShortMax: round1(lufsShortMax), lufsShortMedian: round1(lufsShortMedian),
    samplePeakDb: round1(samplePeakDb), rmsDb: round1(rmsDb), activeRmsDb: round1(activeRmsDb),
    crestDb: round1(samplePeakDb - activeRmsDb), activity: hops ? Math.round((loudHops / hops) * 1000) / 1000 : 0,
    bandShareDb, bandAbsDb, mudShareDb, centroidHz: Math.round(wSum > 0 ? wfSum / wSum : 0), stereo,
  };
  if (nWin) {
    out.windowSec = winLen;
    out.windows = winAcc.map((a) => Array.from({ length: WIN_COLS }, (_, c) => round1(db10(a[WIN_COLS + 1] ? a[c] / a[WIN_COLS + 1] : 0))));
    out.windowTotal = winAcc.map((a) => round1(db10(a[WIN_COLS + 1] ? a[WIN_COLS] / a[WIN_COLS + 1] : 0)));
  }
  if (meanSpec) out.meanSpec = Array.from(meanSpec, (v) => v / nf);
  return out;
}

/** 平均スペクトルから、100Hz〜10kHz の傾き（dB/oct）。analyze.py の tilt_dB_oct と同じ（1 ビンあたりの力を対数周波数で回帰）。1/3 オクターブ幅の帯域での傾きは、これ + 3。 */
export function spectralTilt(meanSpec: number[], sampleRate: number): { psd: number; third: number } {
  const binHz = sampleRate / FFT_SIZE;
  const xs: number[] = [], ys: number[] = [];
  for (let k = 1; k < meanSpec.length; k++) {
    const f = k * binHz;
    if (f > 100 && f < 10000) { xs.push(Math.log2(f)); ys.push(10 * Math.log10(meanSpec[k] + 1e-20)); }
  }
  if (xs.length < 3) return { psd: 0, third: 3 };
  const mx = xs.reduce((a, b) => a + b, 0) / xs.length, my = ys.reduce((a, b) => a + b, 0) / ys.length;
  let sxy = 0, sxx = 0;
  for (let i = 0; i < xs.length; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) ** 2; }
  const psd = sxx > 0 ? sxy / sxx : 0;
  return { psd: Math.round(psd * 100) / 100, third: Math.round((psd + 3) * 100) / 100 };
}

/** analyze.py --bands と同じ 4 帯域（全体に対する dB）: bass 60-250 / lowmid 250-1k / mid 1-4k / presence 4-8k。平均スペクトルから。 */
export function familyBands(meanSpec: number[], sampleRate: number): { bass: number; lowmid: number; mid: number; presence: number } {
  const binHz = sampleRate / FFT_SIZE;
  const sum = (lo: number, hi: number): number => {
    let s = 0;
    for (let k = 1; k < meanSpec.length; k++) { const f = k * binHz; if (f >= lo && f < hi) s += meanSpec[k]; }
    return s;
  };
  const total = sum(20, 20000) + 1e-30;
  const d = (lo: number, hi: number): number => round1(db10(sum(lo, hi) / total));
  return { bass: d(60, 250), lowmid: d(250, 1000), mid: d(1000, 4000), presence: d(4000, 8000) };
}

// ───────────────────────── マスキング診断（パート間） ─────────────────────────

export interface MaskStem {
  id: string;
  role: string;
  /** 時間窓ごとの帯域の力（dB、[窓][WIN_COLS]） */
  windows: number[][];
  windowTotal: number[];
}

export interface MaskOptions {
  /** 「主な担い手」とみなす幅: その帯域でいちばん強いパートからこの dB 以内（既定 6） */
  majorDb?: number;
  /** 3 つ以上が主な担い手 = 混んでいる */
  crowdedCount?: number;
  /** 窓が「鳴っている」とみなすしきい値: 曲の最大の窓より何 dB 下まで（既定 40） */
  activeRangeDb?: number;
  /** 濁りの 200-500Hz の割合の目標（全体に対する dB）。超えた分を「濁りの超過」とする */
  mudShareTargetDb?: number;
  /** リードの聞こえやすさを見る帯域 */
  leadId?: string | null;
  /** 聞こえやすさ（クラリティ）を見る役割と帯域 */
  clarity?: { role: string; bands: BandId[] }[];
}

export interface CrowdStat { meanMajor: number; crowdedPct: number; activeWindows: number }
export interface PairOverlap { a: string; b: string; band: BandId; pct: number }
export interface ClarityStat { id: string; role: string; bands: BandId[]; medianDb: number; p10Db: number; windows: number }
export interface MaskingReport {
  windows: number;
  /** 帯域ごとの「主な担い手の数」 */
  crowd: Record<BandId, CrowdStat>;
  mud: { shareMedianDb: number; shareP90Db: number; excessDb: number; top: { id: string; pct: number }[] };
  /** キック・ベースの低域の重なり（キックかベースが無ければ null） */
  kickBass: { bothActivePct: number; closePct: number; bandLabel: string } | null;
  clarity: ClarityStat[];
  pairs: PairOverlap[];
  /** ぐじゃぐじゃ指数 0〜100（小さいほどすっきり）と、その内訳 */
  mess: { value: number; mud: number; midCrowd: number; lowCollision: number | null; leadBuried: number | null };
}

const sumPowDb = (vals: number[]): number => db10(vals.reduce((a, v) => a + Math.pow(10, v / 10), 0));
const pct = (num: number, den: number): number => (den > 0 ? Math.round((num / den) * 1000) / 10 : 0);
const quantile = (sorted: number[], q: number): number => (sorted.length ? sorted[Math.min(sorted.length - 1, Math.max(0, Math.floor(q * (sorted.length - 1))))] : NaN);

/**
 * パート同士の重なりを、時間窓ごとの帯域の力から数字にする。
 *  - 主な担い手の数: ある窓のある帯域で、いちばん強いパートから majorDb 以内のパートの数（3 つ以上 = 混んでいる）
 *  - 濁り: 200-500Hz の力が全体に占める割合（目標を超えた分）と、その帯域に寄与しているパート
 *  - キックとベースの重なり: 低域（Sub+Bass）で両方が鳴り、差が 4dB 以内の窓の割合
 *  - 聞こえやすさ: 指定した役割のパートの、指定帯域の力 − 他のパート全部の力（dB。プラスなら抜けている）
 *  - ぐじゃぐじゃ指数: 濁り・Mid の混み・低域のぶつかり・リードの埋もれ、の 0〜100 の平均
 */
export function diagnoseMasking(stems: MaskStem[], o: MaskOptions = {}): MaskingReport {
  const majorDb = o.majorDb ?? 6, crowdedCount = o.crowdedCount ?? 3, activeRange = o.activeRangeDb ?? 40;
  const mudTarget = o.mudShareTargetDb ?? -9;
  const W = Math.min(...stems.map((s) => s.windows.length));
  const empty = (): MaskingReport => ({
    windows: 0, crowd: Object.fromEntries(BAND_IDS.map((b) => [b, { meanMajor: 0, crowdedPct: 0, activeWindows: 0 }])) as Record<BandId, CrowdStat>,
    mud: { shareMedianDb: NaN, shareP90Db: NaN, excessDb: 0, top: [] }, kickBass: null, clarity: [], pairs: [],
    mess: { value: 0, mud: 0, midCrowd: 0, lowCollision: null, leadBuried: null },
  });
  if (!stems.length || !Number.isFinite(W) || W <= 0) return empty();
  const tot = (w: number): number => sumPowDb(stems.map((s) => s.windowTotal[w]));
  const totals = Array.from({ length: W }, (_, w) => tot(w));
  const maxTot = Math.max(...totals);
  const activeWin = totals.map((t) => t > maxTot - activeRange);
  const nActive = activeWin.filter(Boolean).length;
  const melodic = stems.filter((s) => !isDrumRole(s.role) && s.role !== "bass");

  // 主な担い手の数
  const crowd = {} as Record<BandId, CrowdStat>;
  BAND_IDS.forEach((band, bi) => {
    let sumMajor = 0, crowded = 0, cnt = 0;
    const bandMax = Math.max(...stems.flatMap((s) => s.windows.slice(0, W).map((r) => r[bi])));
    for (let w = 0; w < W; w++) {
      if (!activeWin[w]) continue;
      const vals = stems.map((s) => s.windows[w][bi]);
      const top = Math.max(...vals);
      if (top < bandMax - activeRange) continue; // この帯域は、その窓ではほぼ鳴っていない
      const major = vals.filter((v) => v >= top - majorDb).length;
      sumMajor += major; cnt++;
      if (major >= crowdedCount) crowded++;
    }
    crowd[band] = { meanMajor: cnt ? Math.round((sumMajor / cnt) * 100) / 100 : 0, crowdedPct: pct(crowded, cnt), activeWindows: cnt };
  });

  // 濁り: 全体に占める 200-500Hz の割合
  const shares: number[] = [];
  const mudPow = new Map<string, number>();
  for (let w = 0; w < W; w++) {
    if (!activeWin[w]) continue;
    const m = sumPowDb(stems.map((s) => s.windows[w][MUD_COL]));
    shares.push(m - totals[w]);
    for (const s of stems) mudPow.set(s.id, (mudPow.get(s.id) ?? 0) + Math.pow(10, s.windows[w][MUD_COL] / 10));
  }
  shares.sort((a, b) => a - b);
  const mudSum = [...mudPow.values()].reduce((a, b) => a + b, 0);
  const mudTop = [...mudPow.entries()].map(([id, p]) => ({ id, pct: pct(p, mudSum) })).sort((a, b) => b.pct - a.pct).slice(0, 4);
  const shareMedian = quantile(shares, 0.5);
  const mud = { shareMedianDb: Math.round(shareMedian * 10) / 10, shareP90Db: Math.round(quantile(shares, 0.9) * 10) / 10, excessDb: Math.round(Math.max(0, shareMedian - mudTarget) * 10) / 10, top: mudTop };

  // キックとベース
  const kick = stems.find((s) => s.role === "kick");
  const bassStem = stems.find((s) => s.role === "bass");
  let kickBass: MaskingReport["kickBass"] = null;
  if (kick && bassStem) {
    let both = 0, close = 0, kmax = -Infinity, bmax = -Infinity;
    const lowOf = (s: MaskStem, w: number): number => sumPowDb([s.windows[w][0], s.windows[w][1]]);
    for (let w = 0; w < W; w++) { kmax = Math.max(kmax, lowOf(kick, w)); bmax = Math.max(bmax, lowOf(bassStem, w)); }
    for (let w = 0; w < W; w++) {
      const kd = lowOf(kick, w), bd = lowOf(bassStem, w);
      if (kd > kmax - 25 && bd > bmax - 25) { both++; if (Math.abs(kd - bd) <= 4) close++; }
    }
    kickBass = { bothActivePct: pct(both, W), closePct: pct(close, both), bandLabel: "Sub+Bass 20-120Hz" };
  }

  // 聞こえやすさ（指定した役割 × 帯域）
  const clarity: ClarityStat[] = [];
  for (const rule of o.clarity ?? []) {
    for (const s of stems.filter((x) => x.role === rule.role)) {
      const diffs: number[] = [];
      for (let w = 0; w < W; w++) {
        if (!activeWin[w]) continue;
        const idx = rule.bands.map((b) => BAND_IDS.indexOf(b));
        const mine = sumPowDb(idx.map((i) => s.windows[w][i]));
        const others = sumPowDb(stems.filter((x) => x !== s).flatMap((x) => idx.map((i) => x.windows[w][i])));
        // その窓で自分がほぼ鳴っていないときは数えない
        if (mine < s.windowTotal[w] - 25 || s.windowTotal[w] < Math.max(...s.windowTotal.slice(0, W)) - 30) continue;
        diffs.push(mine - others);
      }
      diffs.sort((a, b) => a - b);
      clarity.push({ id: s.id, role: s.role, bands: rule.bands, medianDb: Math.round(quantile(diffs, 0.5) * 10) / 10, p10Db: Math.round(quantile(diffs, 0.1) * 10) / 10, windows: diffs.length });
    }
  }

  // 2 パートが同じ帯域で同時に強い割合
  const pairs: PairOverlap[] = [];
  const bandIdxs = (["lowmid", "mud", "mid", "presence"] as BandId[]).map((b) => [b, BAND_IDS.indexOf(b)] as const);
  for (let i = 0; i < stems.length; i++) {
    for (let j = i + 1; j < stems.length; j++) {
      for (const [band, bi] of bandIdxs) {
        let cnt = 0, both = 0;
        for (let w = 0; w < W; w++) {
          if (!activeWin[w]) continue;
          const vals = stems.map((s) => s.windows[w][bi]);
          const top = Math.max(...vals);
          const a = stems[i].windows[w][bi], b = stems[j].windows[w][bi];
          if (a >= top - majorDb || b >= top - majorDb) { cnt++; if (a >= top - majorDb && b >= top - majorDb) both++; }
        }
        if (cnt >= 8) pairs.push({ a: stems[i].id, b: stems[j].id, band, pct: pct(both, cnt) });
      }
    }
  }
  pairs.sort((x, y) => y.pct - x.pct);

  // ぐじゃぐじゃ指数
  const clamp01 = (v: number): number => Math.max(0, Math.min(1, v));
  const mudScore = clamp01(mud.excessDb / 6) * 100;
  // Mid（500-2k）の混み: 旋律・和音のパートだけで数える（ドラム・ベースは別）
  let midCrowd = 0;
  if (melodic.length >= 2) {
    const mi = BAND_IDS.indexOf("mid");
    let c = 0, k = 0;
    const bandMax = Math.max(...melodic.flatMap((s) => s.windows.slice(0, W).map((r) => r[mi])));
    for (let w = 0; w < W; w++) {
      if (!activeWin[w]) continue;
      const vals = melodic.map((s) => s.windows[w][mi]);
      const top = Math.max(...vals);
      if (top < bandMax - activeRange) continue;
      k++;
      if (vals.filter((v) => v >= top - majorDb).length >= crowdedCount) c++;
    }
    midCrowd = pct(c, k);
  }
  const lowCollision = kickBass ? kickBass.closePct : null;
  let leadBuried: number | null = null;
  const leadClar = clarity.find((c) => c.id === o.leadId);
  if (leadClar) leadBuried = Math.round(clamp01((-leadClar.medianDb + 3) / 9) * 100);
  const parts = [mudScore, midCrowd, lowCollision, leadBuried].filter((v): v is number => v !== null);
  const value = parts.length ? Math.round(parts.reduce((a, b) => a + b, 0) / parts.length) : 0;
  void nActive;
  return { windows: W, crowd, mud, kickBass, clarity, pairs: pairs.slice(0, 12), mess: { value, mud: Math.round(mudScore), midCrowd, lowCollision, leadBuried } };
}

/** ドラムの役割か */
export function isDrumRole(role: string): boolean {
  return role === "kick" || role === "snare" || role === "hihat" || role === "cymbal" || role === "tom" || role === "perc" || role === "drums";
}
