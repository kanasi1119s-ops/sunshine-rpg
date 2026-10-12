// 出だしの1回の和音を、弦モデルで直接作る（作曲ソフトの音量の落ち方を通さない）。長い残響とエコーつき。
import fs from "fs";
import { pluck } from "/home/claude/wt-k1/tools/soundfont/build-guitar-pluck.mjs";
const SR = 44100, SEC = 14;
const v = { lp1: 5550, lp2: 8225, comb: 0.815, body: true, air: 0.3, t60mul: 4, bmul: 0.45 };
const notes = [[49, -0.45, 0], [56, 0.45, 0.018], [52, 0, 0.036]]; // [midi, pan, 遅れ(秒)]  C#3 G#3 E3 （F#m を5半音下げた形）
const N = SEC * SR;
const dry = [new Float32Array(N), new Float32Array(N)];
for (const [m, pan, dly] of notes) {
  const x = pluck(m, 0.6, 9, v), o = Math.floor(dly * SR);
  const gl = Math.cos((pan + 1) * Math.PI / 4), gr = Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < x.length && i + o < N; i++) { dry[0][i + o] += x[i] * gl; dry[1][i + o] += x[i] * gr; }
}
// ボリューム奏法ふうに: 頭の弾いた音は消して 1.4 秒かけてふくらませ、弦の自然な減りは持ち上げて打ち消す（平らに伸ばす）
for (let c = 0; c < 2; c++) for (let i = 0; i < N; i++) {
  const t = i / SR; const sw = Math.min(1, t / 1.4); const fadeIn = sw * sw * (3 - 2 * sw);
  const comp = 10 ** (Math.min(t, 4.6) * 4.5 / 20);
  dry[c][i] *= fadeIn * comp;
}
// 5.6秒(4小節)のスネアの連打の終わりまで保ち、そのあとなめらかに消す
const f0 = Math.floor(4.6 * SR), f1 = Math.floor(7.5 * SR);
for (let c = 0; c < 2; c++) for (let i = f0; i < N; i++) dry[c][i] *= i > f1 ? 0 : 0.5 + 0.5 * Math.cos(Math.PI * (i - f0) / (f1 - f0));
// エコー（付点8分=0.75拍、BPM172）2回、減り方0.6。左右に交互
const d = Math.round(0.75 * 60 / 172 * SR);
const ech = [Float32Array.from(dry[0]), Float32Array.from(dry[1])];
for (const [k, g] of [[1, 0.6], [2, 0.36]]) for (let c = 0; c < 2; c++) for (let i = k * d; i < N; i++) ech[1 - c][i] += dry[c][i - k * d] * g * (k % 2 ? 1 : 1);
// 残響（シュローダー型。T60 約7秒、高域はゆっくり減る）
function reverb(x, off) {
  const T60 = 7;
  const combs = [1557, 1617, 1491, 1422, 1277, 1356, 1188, 1116].map((n) => n + off);
  let out = new Float32Array(N);
  for (const n of combs) {
    const g = 10 ** (-3 * n / (T60 * SR)); const buf = new Float32Array(n); let idx = 0, lp = 0;
    for (let i = 0; i < N; i++) { const y = buf[idx]; lp = 0.7 * y + 0.3 * lp; buf[idx] = x[i] + lp * g; idx = (idx + 1) % n; out[i] += y * 0.18; }
  }
  for (const n of [556, 441, 341, 225].map((q) => q + off)) {
    const buf = new Float32Array(n); let idx = 0; const o2 = new Float32Array(N);
    for (let i = 0; i < N; i++) { const b = buf[idx]; const y = -0.5 * out[i] + b; buf[idx] = out[i] + 0.5 * b; o2[i] = y; idx = (idx + 1) % n; }
    out = o2;
  }
  return out;
}
const wet = [reverb(ech[0], 0), reverb(ech[1], 23)];
const L = new Float32Array(N), R = new Float32Array(N);
for (let i = 0; i < N; i++) { L[i] = ech[0][i] * 0.7 + wet[0][i] * 1.6; R[i] = ech[1][i] * 0.7 + wet[1][i] * 1.6; }
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
let pk = 0; for (let i = 0; i < N; i++) pk = Math.max(pk, Math.abs(L[i]), Math.abs(R[i]));
for (let i = 0; i < N; i++) { buf.writeInt16LE(Math.round(L[i] / pk * 30000), 44 + i * 4); buf.writeInt16LE(Math.round(R[i] / pk * 30000), 46 + i * 4); }
fs.writeFileSync(process.argv[2], buf); console.log("ok", pk.toFixed(3));
