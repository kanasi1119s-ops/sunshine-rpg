// タッピングのソロを、弦モデルで1音ずつ直接作る（ハンマリング・プリングの柔らかい立ち上がり、叩いた音の「コツ」、音をつなぐときの前の音の止まり）。
// 使い方: node --experimental-strip-types tools/soundfont/tap-synth.mjs <音符.json> <出力.wav>
//  音符.json: [[midi, 開始拍, 長さ拍, ビブラート?, ベンド?], ...]  （BPM172）
import fs from "fs";
import { pluck } from "./build-guitar-pluck.mjs";
const SR = 44100, BPM = 172, beat = 60 / BPM;
const ev = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const total = Math.ceil((ev[ev.length - 1][1] + ev[ev.length - 1][2]) * beat * SR + 5 * SR);
const dry = new Float32Array(total);
const vTap = { lp1: 6800, lp2: 9500, comb: 0.65, body: false };
// 8音ごとの強弱: 叩いた高い音が一番はっきり、ハンマー・プルは柔らかく
const VEL = [0.8, 0.62, 0.62, 1.0, 0.62, 0.62, 0.75, 0.62];
function resample(x, ratioAt) { // ratioAt(t秒) = 音の高さの倍率
  const y = new Float32Array(x.length); let pos = 0;
  for (let i = 0; i < y.length; i++) { const t = i / SR; const k = Math.floor(pos); if (k + 1 >= x.length) break; const f = pos - k; y[i] = x[k] * (1 - f) + x[k + 1] * f; pos += ratioAt(t); }
  return y;
}
ev.forEach(([midi, b, d, vib, bend, gain = 1], idx) => {
  const top = idx % 8 === 3;
  let x = pluck(midi, top ? 0.5 : 0.22, 4, vTap);
  if (bend || vib) x = resample(x, (t) => 2 ** (((bend ? Math.min(2, t / 0.25 * 2) : 0) + (vib ? 0.3 * Math.sin(2 * Math.PI * 5.5 * Math.max(0, t - (bend ? 0.35 : 0.2))) * Math.min(1, Math.max(0, (t - 0.2) / 0.3)) : 0)) / 12));
  const start = Math.floor(b * beat * SR), len = Math.floor((d * beat + (bend || vib ? 0.6 : 0.03)) * SR), fo = Math.floor((bend || vib ? 0.35 : 0.03) * SR);
  const g = VEL[idx % 8] * gain;
  for (let i = 0; i < len && start + i < total; i++) {
    let a = 1; if (i < 0.003 * SR) a = i / (0.003 * SR); if (i > len - fo) a = Math.min(a, (len - i) / fo);
    dry[start + i] += x[i] * a * g;
  }
  if (top) { const n = Math.floor(0.012 * SR); for (let i = 0; i < n; i++) dry[start + i] += 0.12 * gain * Math.sin(2 * Math.PI * 130 * i / SR) * Math.exp(-i / (0.004 * SR)); }
});
// 軽い残響（T60 約2秒）
function reverb(x, off) {
  const T60 = 2, combs = [1557, 1617, 1491, 1422].map((n) => n + off); let out = new Float32Array(total);
  for (const n of combs) { const g = 10 ** (-3 * n / (T60 * SR)); const buf = new Float32Array(n); let idx = 0, lp = 0; for (let i = 0; i < total; i++) { const y = buf[idx]; lp = 0.6 * y + 0.4 * lp; buf[idx] = x[i] + lp * g; idx = (idx + 1) % n; out[i] += y * 0.25; } }
  return out;
}
const wl = reverb(dry, 0), wr = reverb(dry, 29);
const L = new Float32Array(total), R = new Float32Array(total);
for (let i = 0; i < total; i++) { L[i] = dry[i] + wl[i] * 0.35; R[i] = dry[i] + wr[i] * 0.35; }
const buf = Buffer.alloc(44 + total * 4); buf.write("RIFF", 0); buf.writeUInt32LE(36 + total * 4, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(total * 4, 40);
let pk = 0; for (let i = 0; i < total; i++) pk = Math.max(pk, Math.abs(L[i]), Math.abs(R[i]));
for (let i = 0; i < total; i++) { buf.writeInt16LE(Math.round(L[i] / pk * 24000), 44 + i * 4); buf.writeInt16LE(Math.round(R[i] / pk * 24000), 46 + i * 4); }
fs.writeFileSync(process.argv[3], buf); console.log("ok", ev.length, "音", (total / SR).toFixed(1) + "秒");
