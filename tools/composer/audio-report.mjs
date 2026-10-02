// 書き出したWAVを、数値で確かめる（音量・ピーク・低域〜高域のバランス）。FFmpeg を使う。耳の代わりにはならないが、
// 「音が割れている」「小さすぎる」「こもっている」「低域だけ過剰」のような、はっきりした不具合は見つけられる。
import { spawnSync } from "child_process";

const BANDS = [[20, 60], [60, 120], [120, 250], [250, 500], [500, 1000], [1000, 2000], [2000, 4000], [4000, 8000], [8000, 16000]];
const SR = 22050;

function fft(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      [re[i], re[j]] = [re[j], re[i]];
      [im[i], im[j]] = [im[j], im[i]];
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = (-2 * Math.PI) / len;
    const wr = Math.cos(ang);
    const wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1;
      let ci = 0;
      for (let k = 0; k < len / 2; k++) {
        const a = i + k;
        const b = a + len / 2;
        const tr = re[b] * cr - im[b] * ci;
        const ti = re[b] * ci + im[b] * cr;
        re[b] = re[a] - tr;
        im[b] = im[a] - ti;
        re[a] += tr;
        im[a] += ti;
        const ncr = cr * wr - ci * wi;
        ci = cr * wi + ci * wr;
        cr = ncr;
      }
    }
  }
}

/** @returns {{ok:boolean, lufs?:number, lra?:number, truePeak?:number, seconds?:number, bands?:Record<string,number>, warnings:string[]}} */
export function analyzeWav(file) {
  const warnings = [];
  const e = spawnSync("ffmpeg", ["-nostats", "-i", file, "-af", "ebur128=peak=true", "-f", "null", "-"], { encoding: "utf8", maxBuffer: 1 << 26 });
  if (e.status !== 0) return { ok: false, warnings: ["音の解析に失敗しました（FFmpeg）"] };
  const sum = e.stderr.slice(e.stderr.lastIndexOf("Summary:"));
  const num = (re) => {
    const m = re.exec(sum);
    return m ? Number(m[1]) : undefined;
  };
  const lufs = num(/I:\s+(-?\d+(?:\.\d+)?) LUFS/);
  const lra = num(/LRA:\s+(-?\d+(?:\.\d+)?) LU/);
  const truePeak = num(/Peak:\s+(-?\d+(?:\.\d+)?) dBFS/);
  const dur = /Duration: (\d+):(\d+):(\d+\.\d+)/.exec(e.stderr);
  const seconds = dur ? Number(dur[1]) * 3600 + Number(dur[2]) * 60 + Number(dur[3]) : undefined;

  // 中ほどの30秒を取り出して、帯域ごとのエネルギーを見る（モノラル・22.05kHz）
  const start = seconds && seconds > 40 ? Math.floor(seconds / 2 - 15) : 0;
  const pcm = spawnSync("ffmpeg", ["-v", "error", "-ss", String(start), "-t", "30", "-i", file, "-ac", "1", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 28 });
  const bands = {};
  if (pcm.status === 0 && pcm.stdout.length > 4096 * 4) {
    const x = new Float32Array(pcm.stdout.buffer, pcm.stdout.byteOffset, Math.floor(pcm.stdout.length / 4));
    const N = 4096;
    const power = new Float64Array(N / 2);
    for (let off = 0; off + N <= x.length; off += N) {
      const re = new Float64Array(N);
      const im = new Float64Array(N);
      for (let i = 0; i < N; i++) re[i] = x[off + i] * (0.5 - 0.5 * Math.cos((2 * Math.PI * i) / (N - 1)));
      fft(re, im);
      for (let k = 0; k < N / 2; k++) power[k] += re[k] * re[k] + im[k] * im[k];
    }
    const hz = SR / N;
    let total = 0;
    for (let k = 1; k < N / 2; k++) total += power[k];
    for (const [a, b] of BANDS) {
      let s = 0;
      for (let k = Math.ceil(a / hz); k < Math.min(N / 2, Math.floor(b / hz)); k++) s += power[k];
      bands[`${a}-${b}`] = Math.round(10 * Math.log10(s / total + 1e-12) * 10) / 10;
    }
  }
  if (lufs !== undefined && lufs < -24) warnings.push(`音が小さい（${lufs} LUFS）`);
  if (truePeak !== undefined && truePeak > -0.3) warnings.push(`ピークが大きすぎる（${truePeak} dBTP）。音が割れる可能性`);
  if (bands["8000-16000"] !== undefined && bands["8000-16000"] < -32) warnings.push("高域が少なく、こもって聞こえる可能性");
  if (bands["20-60"] !== undefined && bands["20-60"] > -8) warnings.push("超低域（20〜60Hz）が多すぎる可能性");
  if (bands["2000-4000"] !== undefined && bands["2000-4000"] > -2) warnings.push("2〜4kHzが強すぎて、耳に痛い可能性");
  return { ok: true, lufs, lra, truePeak, seconds, bands, warnings };
}
