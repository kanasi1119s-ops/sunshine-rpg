// 書き出したWAVの「ざらつき(flat)・空気(8k+)・頭(5秒ごと)・余韻」を測る（tools/audio-check/analyze.py と同じ定義の JS 版）。
// ジャンル別の目標（genre-targets.mjs）と比べるための数字で、数字だけを返す。
//   flat  … 2〜8kHz のスペクトルの平坦さ（0〜1。シンバル・空気・残響・歪みなど、ノイズに近い成分が多いほど大きい）
//   air   … 8〜16kHz の量（全体に対する dB）。 presence … 4〜8kHz
//   intro … 最初の5秒の大きさ − 曲のいちばん大きい5秒（dB。analyze.py の intro_vs_max_dB。1000曲の「頭」と同じ測り方）
//   tail  … 最後の音が −20dB から −50dB まで消えるまでの秒数（残響の長さの目安）
import { spawnSync } from "child_process";

/** 実数列の in-place radix-2 FFT。re・im の長さは 2 のべき乗。 */
export function fft(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) { [re[i], re[j]] = [re[j], re[i]]; [im[i], im[j]] = [im[j], im[i]]; }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (-2 * Math.PI) / len, wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) {
        const a = i + k, b = i + k + len / 2;
        const tr = re[b] * cr - im[b] * ci, ti = re[b] * ci + im[b] * cr;
        re[b] = re[a] - tr; im[b] = im[a] - ti; re[a] += tr; im[a] += ti;
        const nr = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = nr;
      }
    }
  }
}

/**
 * 左右の波形（Float32Array）から測る。mid = (L+R)/2。
 * 戻り値: { flat, air, presence, intro, tail }（測れないときは NaN）
 */
export function spectralMetrics(L, R, sr = 44100) {
  const N = 4096, hop = 2048, n = Math.min(L.length, R.length);
  const nan = { flat: NaN, air: NaN, presence: NaN, intro: NaN, tail: NaN };
  if (n < N * 2) return nan;
  const win = new Float64Array(N);
  for (let i = 0; i < N; i++) win[i] = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / N);
  const bin = (f) => Math.ceil((f * N) / sr);
  const k2 = bin(2000), k8 = bin(8000), k4 = bin(4000), k16 = Math.min(bin(16000), N / 2);
  const frames = Math.floor((n - N) / hop) + 1;
  const re = new Float64Array(N), im = new Float64Array(N);
  const flats = [], loud = new Float64Array(frames);
  let total = 0, airE = 0, presE = 0;
  for (let f = 0; f < frames; f++) {
    const o = f * hop;
    for (let i = 0; i < N; i++) { re[i] = ((L[o + i] + R[o + i]) / 2) * win[i]; im[i] = 0; }
    fft(re, im);
    let fl = 0, logSum = 0, sum = 0, cnt = 0;
    for (let k = 0; k <= N / 2; k++) {
      const p = re[k] * re[k] + im[k] * im[k];
      fl += p;
      if (k >= k2 && k < k8) { const q = p + 1e-20; logSum += Math.log(q); sum += q; cnt++; }
      if (k >= k4 && k < k8) presE += p;
      if (k >= k8 && k < k16) airE += p;
    }
    total += fl; loud[f] = fl;
    flats.push(cnt ? Math.exp(logSum / cnt) / (sum / cnt) : NaN);
  }
  const sorted = [...flats].sort((a, b) => a - b);
  const flat = (sorted[Math.floor((sorted.length - 1) / 2)] + sorted[Math.ceil((sorted.length - 1) / 2)]) / 2; // 中央値
  const db = (e) => 10 * Math.log10(e / (total + 1e-30) + 1e-12);
  // 5秒ごとの大きさ（mid の RMS）
  const seg = sr * 5, rms = [];
  for (let i = 0; i + seg <= n; i += seg) {
    let s = 0;
    for (let j = i; j < i + seg; j++) { const m = (L[j] + R[j]) / 2; s += m * m; }
    rms.push(20 * Math.log10(Math.sqrt(s / seg) + 1e-9));
  }
  const intro = rms.length ? rms[0] - Math.max(...rms) : NaN;
  // 余韻: 大きさの包絡（フレームごとの全帯域エネルギー）が −20dB から −50dB まで落ちるまで
  const peak = Math.max(...loud);
  let last20 = -1, last50 = -1;
  for (let f = 0; f < frames; f++) {
    const e = 10 * Math.log10(loud[f] / (peak + 1e-30) + 1e-12);
    if (e > -20) last20 = f;
    if (e > -50) last50 = f;
  }
  const tail = last20 >= 0 && last50 >= last20 ? ((last50 - last20) * hop) / sr : NaN;
  return { flat, air: db(airE), presence: db(presE), intro, tail };
}

/** WAV ファイルから測る（ffmpeg が必要）。 */
export function spectralMetricsOfFile(file, sr = 44100) {
  const r = spawnSync("ffmpeg", ["-v", "error", "-i", file, "-f", "f32le", "-ac", "2", "-ar", String(sr), "-"], { maxBuffer: 1 << 30 });
  if (r.error) throw new Error("ffmpeg が使えません（インストールしてください）");
  const buf = r.stdout;
  const a = new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength - (buf.byteLength % 4)));
  const n = a.length >> 1, L = new Float32Array(n), R = new Float32Array(n);
  for (let i = 0; i < n; i++) { L[i] = a[2 * i]; R[i] = a[2 * i + 1]; }
  return spectralMetrics(L, R, sr);
}
