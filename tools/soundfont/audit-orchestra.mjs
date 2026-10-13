// 使い方: node tools/soundfont/audit-orchestra.mjs [program ...]（dist-composer を先にビルドしておく）
// オーケストラ音源の全楽器について、半音ずつ鳴らして点検する: ①測った音の高さが合っているか ②隣の音との音量差 ③長い音のループのつなぎ目（音の途切れ・プチッという音）
import fs from "fs";
import { execSync } from "child_process";
const R = execSync("npm root -g", { encoding: "utf8" }).trim();
const { chromium } = await import(R + "/playwright/index.mjs");
const SR = 44100;
const SETS = { // [プログラム, 名前, 低い音, 高い音]
  40: ["violin", 55, 100], 41: ["viola", 48, 88], 42: ["cello", 36, 78], 43: ["contrabass", 30, 62], 45: ["pizzicato", 57, 88],
  46: ["harp", 28, 95], 47: ["timpani", 30, 48], 48: ["strings", 36, 90], 56: ["trumpet", 53, 86], 57: ["trombone", 34, 68], 58: ["tuba", 29, 64],
  60: ["horn", 33, 79], 61: ["brass", 34, 86], 68: ["oboe", 58, 91], 70: ["bassoon", 34, 77], 71: ["clarinet", 50, 92], 72: ["piccolo", 79, 98],
  73: ["flute", 60, 98], 19: ["organ", 24, 98], 12: ["marimba", 41, 98], 9: ["glock", 79, 98], 0: ["piano", 21, 108],
};
const want = process.argv.slice(2).map(Number);
const progs = Object.keys(SETS).map(Number).filter((p) => !want.length || want.includes(p));
const overlay = (p) => (p === 0 ? ["std", "salamander"] : ["vsco", "std"]);
const b = await chromium.launch({ args: ["--autoplay-policy=no-user-gesture-required", "--disable-gpu"] });
const page = await b.newPage();
await page.goto("file://" + process.cwd() + "/dist-composer/index.html", { timeout: 240000 });
await page.waitForFunction(() => "__composer" in window, undefined, { timeout: 240000 });
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nn = (m) => NAMES[m % 12] + (Math.floor(m / 12) - 1);
function detect(x) { // 自己相関で音の高さ（MIDI）を測る
  const N = Math.min(x.length, 12000), minLag = Math.floor(SR / 3500), maxLag = Math.min(Math.floor(SR / 25), N >> 1);
  let e0 = 0; for (let i = 0; i < N - maxLag; i++) e0 += x[i] * x[i];
  if (e0 < 1e-8) return null;
  const r = new Float32Array(maxLag + 2);
  for (let lag = minLag; lag <= maxLag + 1; lag++) { let s = 0, e1 = 0; for (let i = 0; i < N - maxLag - 1; i++) { s += x[i] * x[i + lag]; e1 += x[i + lag] ** 2; } r[lag] = s / Math.sqrt(e0 * e1 + 1e-12); }
  let best = 0; for (let l = minLag + 1; l <= maxLag; l++) if (r[l] > best && r[l] >= r[l - 1] && r[l] >= r[l + 1]) best = r[l];
  if (best < 0.45) return null;
  for (let l = minLag + 1; l <= maxLag; l++) if (r[l] >= best * 0.9 && r[l] >= r[l - 1] && r[l] >= r[l + 1]) { const a = r[l - 1], bb = r[l], c = r[l + 1], d = a - 2 * bb + c; return 69 + 12 * Math.log2(SR / (l + (d ? (0.5 * (a - c)) / d : 0)) / 440); }
  return null;
}
const decode = (b64) => { const buf = Buffer.from(b64, "base64"); const n = (buf.length - 44) >> 2; const L = new Float32Array(n); for (let i = 0; i < n; i++) L[i] = (buf.readInt16LE(44 + i * 4) + buf.readInt16LE(46 + i * 4)) / 65536; return L; };
const report = [];
for (const p of progs) {
  const [name, lo, hi] = SETS[p];
  const [orch, piano] = overlay(p);
  await page.evaluate(([o, pi]) => window.__composer.setOverlays("std", "std", "std", o, pi), [orch, piano]);
  const notes = []; for (let m = lo; m <= hi; m++) notes.push({ note: nn(m), durationBeats: 1.5, velocity: 0.7 }), notes.push({ note: null, durationBeats: 0.5 });
  const score = { tempoBpm: 120, loop: false, drumKit: 0, tone: "rock", dynamicRange: "wide", tracks: [{ waveform: "sine", program: p, instrument: "strings", volume: 0.2, pan: 0, reverb: 0, notes: notes.map((n) => n.note ? n : { note: "R", durationBeats: n.durationBeats, velocity: 0 }) }] };
  const x = decode(await page.evaluate(([s]) => window.__composer.renderWav(s, "real"), [score]));
  if (process.env.AUDIT_WAV) fs.writeFileSync(`${process.env.AUDIT_WAV}-${p}.f32`, Buffer.from(x.buffer));
  const per = []; // 1音 = 1秒
  for (let i = 0; i < hi - lo + 1; i++) {
    const seg = x.subarray(Math.floor(i * SR + SR * 0.25), Math.floor(i * SR + SR * 0.75 + 0));
    let t = 0; for (const v of seg) t += v * v;
    const rms = Math.sqrt(t / seg.length), m = detect(seg);
    per.push({ midi: lo + i, rms, cents: m === null ? null : Math.round((m - (lo + i)) * 100) });
  }
  const issues = [];
  per.forEach((q, i) => {
    if (q.rms < 0.002) issues.push(`${nn(q.midi)}: ほぼ無音`);
    else if (q.cents !== null && Math.abs(q.cents) > 45 && Math.abs(q.cents) < 1100) issues.push(`${nn(q.midi)}: 音の高さが ${q.cents} セントずれ`);
    const nb = per.slice(Math.max(0, i - 2), i + 3).filter((_, j) => j !== Math.min(i, 2)).map((z) => z.rms).sort((a, c) => a - c);
    const med = nb[Math.floor(nb.length / 2)];
    if (med > 0.002 && q.rms > 0 && Math.abs(20 * Math.log10(q.rms / med)) > 7) issues.push(`${nn(q.midi)}: 隣と音量が ${(20 * Math.log10(q.rms / med)).toFixed(1)}dB ちがう`);
  });
  // 長い音（中ほどのA音）で、ループの途切れを見る
  const mid = Math.round((lo + hi) / 2);
  const long = { tempoBpm: 60, loop: false, drumKit: 0, tone: "rock", dynamicRange: "wide", tracks: [{ waveform: "sine", program: p, instrument: "strings", volume: 0.2, pan: 0, reverb: 0, notes: [{ note: nn(mid), durationBeats: 12, velocity: 0.7 }] }] };
  const y = decode(await page.evaluate(([s]) => window.__composer.renderWav(s, "real"), [long]));
  const win = (a, bb) => { let t = 0; const s = y.subarray(Math.floor(a * SR), Math.floor(bb * SR)); for (const v of s) t += v * v; return Math.sqrt(t / s.length); };
  const e = [1, 3, 5, 7, 9, 11].map((s) => win(s, s + 0.5));
  let maxj = 0, at = 0; const s0 = Math.floor(1.5 * SR), s1 = Math.floor(11 * SR); for (let i = s0; i < s1; i++) { const d = Math.abs(y[i + 1] - y[i]); if (d > maxj) { maxj = d; at = i / SR; } }
  const rmsAll = win(1.5, 11);
  report.push({ p, name, per: per.map((q) => [q.midi, +q.rms.toFixed(5)]), notes: per.length, issues, sustain: e.map((v) => +(20 * Math.log10(v + 1e-9)).toFixed(1)), maxJump: +maxj.toFixed(3), rms: +rmsAll.toFixed(3) });
  console.log(`${p} ${name}: 点検 ${per.length}音 問題 ${issues.length}件 / 長い音の音量(dB) ${e.map((v) => (20 * Math.log10(v + 1e-9)).toFixed(0)).join(",")} / 最大の段差 ${maxj.toFixed(3)} (${at.toFixed(1)}s)`);
  for (const s of issues.slice(0, 8)) console.log("   ", s);
}
fs.writeFileSync(process.env.AUDIT_OUT ?? "/tmp/orchestra-audit.json", JSON.stringify(report, null, 1));
await b.close();
