// 使い方: node tools/soundfont/build-analog-synths.mjs [作業フォルダ] [--only 名前の正規表現]
// アナログシンセ風の音（ソー・スーパーソー・アルペジオ向けの短い音・ジュピター系のポリシンセ・シンセブラス・ストリングスマシン・ムーグ系ベース・アシッドベース）を、
// このプログラム自身で作る（外部の録音は使わない。polyBLEP のソー波・パルス波 → ムーグ型ラダーフィルター → アンサンブルコーラスの順。作者の著作物として CC0 扱いにできる）。
//   1) 音ごとの WAV（16bit・44.1kHz・モノラル）と SFZ を作業フォルダに書く。
//   2) tools/soundfont/sfz-to-sf3.mjs で SF3 にして assets-src/soundfont/extra/ に置く。
// 続けて伸ばす音は、ループの長さをちょうど整数フレーム（88200 または 44100）にして、全オシレーターの周期の数を整数にそろえている（つなぎ目でプチッと鳴らない）。
//   そのため基音の周波数が最大で 0.25Hz（ベースは 1Hz）ずれるので、そのぶんは SFZ の tune（セント）で打ち消している。
// 耳での確認は別（作曲ソフトで鳴らして聞く）。ここでは、音程と無音でないことの機械検査（combcheck 相当）だけを行う。
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";

const SR = 44100;
const args = process.argv.slice(2);
const workDir = path.resolve(args[0] && !args[0].startsWith("--") ? args[0] : "/tmp/analog-synths");
const only = args.includes("--only") ? new RegExp(args[args.indexOf("--only") + 1]) : null;
fs.mkdirSync(workDir, { recursive: true });

// ---------- 部品 ----------
const TAU = Math.PI * 2;
function polyblep(t, dt) {
  if (t < dt) { t /= dt; return t + t - t * t - 1; }
  if (t > 1 - dt) { t = (t - 1) / dt; return t * t + t + t + 1; }
  return 0;
}
/** ソー波・パルス波。cycles = ループ全長(frames)の間に何周期入るか（整数）。 */
function osc(kind, cycles, L, n, phase0, pw = 0.5, mult = 1) {
  const out = new Float64Array(n);
  const inc = (cycles * mult) / L; // 1サンプルあたりの位相の進み
  let p = phase0 % 1;
  for (let i = 0; i < n; i++) {
    if (kind === "saw") out[i] = 2 * p - 1 - polyblep(p, inc);
    else if (kind === "sq") out[i] = (p < pw ? 1 : -1) + polyblep(p, inc) - polyblep((p - pw + 1) % 1, inc);
    else if (kind === "tri") out[i] = 4 * Math.abs(p - 0.5) - 1;
    else if (kind === "sin") out[i] = Math.sin(TAU * p);
    p += inc; if (p >= 1) p -= 1;
  }
  return out;
}
/** ムーグ型の 4 段ラダーフィルター（tanh で飽和、4 倍オーバーサンプリング）。fc は秒→Hz の関数。
 *  カットオフが高いとき（約 5kHz 以上）は、離散化で共振が不安定になる（半分の周波数の発振が出る）ので、共振を段階的に 0 にする。 */
function ladder(x, fcAt, res, drive = 1) {
  const y = new Float64Array(x.length);
  const OS = 4;
  let s0 = 0, s1 = 0, s2 = 0, s3 = 0, t0 = 0, t1 = 0, t2 = 0, t3 = 0;
  for (let i = 0; i < x.length; i++) {
    const fc = Math.min(fcAt(i / SR), SR * 0.2);
    const g = 1 - Math.exp(-TAU * fc / (OS * SR));
    const r = res * Math.max(0, Math.min(1, 1 - (fc - 4500) / 3500));
    for (let k = 0; k < OS; k++) {
      const tu = Math.tanh(drive * x[i] - r * s3);
      s0 += g * (tu - t0); t0 = Math.tanh(s0);
      s1 += g * (t0 - t1); t1 = Math.tanh(s1);
      s2 += g * (t1 - t2); t2 = Math.tanh(s2);
      s3 += g * (t2 - t3); t3 = Math.tanh(s3);
    }
    y[i] = s3 * (1 + r * 0.45);
  }
  return y;
}
function onepole(x, fc) {
  const a = 1 - Math.exp(-TAU * fc / SR); const y = new Float64Array(x.length); let s = 0;
  for (let i = 0; i < x.length; i++) { s += a * (x[i] - s); y[i] = s; }
  return y;
}
function highpass(x, fc) { const lp = onepole(x, fc); const y = new Float64Array(x.length); for (let i = 0; i < x.length; i++) y[i] = x[i] - lp[i]; return y; }
/** アンサンブル（ストリングスマシン／ジュピターのコーラス）。LFO は L の間にちょうど整数回まわる（ループがつながる）。 */
function ensemble(x, L, taps) {
  const y = new Float64Array(x.length);
  for (const { base, depth, cycles, phase, gain } of taps) {
    for (let i = 0; i < x.length; i++) {
      const d = (base + depth * Math.sin(TAU * (cycles * i / L) + phase)) * SR;
      const pos = i - d; const i0 = Math.floor(pos); const fr = pos - i0;
      const a = i0 >= 0 ? x[i0] : 0, b = i0 + 1 >= 0 ? x[i0 + 1] : 0;
      y[i] += gain * (a + (b - a) * fr);
    }
  }
  return y;
}
const cents = (c) => 2 ** (c / 1200);
function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
const expEnv = (t, t0, t1, a, b) => (t <= t0 ? a : t >= t1 ? b : a * (b / a) ** ((t - t0) / (t1 - t0))); // a→b の指数的な動き
const smooth = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
function writeWav(file, x) {
  const buf = Buffer.alloc(44 + x.length * 2);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + x.length * 2, 4); buf.write("WAVEfmt ", 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(x.length * 2, 40);
  for (let i = 0; i < x.length; i++) buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, x[i])) * 32767), 44 + i * 2);
  fs.writeFileSync(file, buf);
}

// ---------- 音色の定義 ----------
// render({ f0, cyc(f)→整数, L, pre, n, seed }) → Float64Array（長さ n = pre + L + 余白）
const midiHz = (m) => 440 * 2 ** ((m - 69) / 12);
const INSTR = {
  // ソー・リード（GM 81）: 2本のソー（±6セント）＋サブのパルス。立ち上がりに少しだけフィルターが開く
  "synth-lead-saw": {
    program: 81, loop: 88200, pre: 17640, step: 4, keys: [28, 100], level: 0.92, release: 0.25,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-6, 6]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.5; }
      const sub = osc("sq", c0, L, n, rnd(), 0.5, 0.5); for (let i = 0; i < n; i++) x[i] += sub[i] * 0.12;
      const y = ladder(x, (t) => Math.min(14000, f0 * 7 + 2200) * expEnv(t, 0, 0.12, 1.5, 1), 0.5, 1.1);
      const env = (t) => smooth(t / 0.004);
      return y.map((v, i) => v * env(i / SR));
    },
  },
  // スーパーソー（GM 81）: ジュピター風の 7 本のソー（±3〜22 セント）。広がりと厚み
  "synth-lead-supersaw": {
    program: 81, loop: 88200, pre: 22050, step: 4, keys: [28, 100], level: 0.95, release: 0.3,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      const det = [-22, -13, -5, 0, 6, 14, 23], gn = [0.55, 0.7, 0.85, 1, 0.85, 0.7, 0.55];
      det.forEach((d, k) => { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * gn[k] * 0.28; });
      const hp = highpass(x, 90);
      const y = ladder(hp, (t) => Math.min(13000, f0 * 5 + 3200) * expEnv(t, 0, 0.1, 1.3, 1), 0.15, 1.0);
      const env = (t) => smooth(t / 0.01);
      return y.map((v, i) => v * env(i / SR));
    },
  },
  // アルペジオ向けの短い音（GM 81 の差し替え。ループなし）: ソー 2 本＋パルス。フィルターと音量がすばやく閉じる
  "synth-lead-arp": {
    program: 81, loop: 0, total: 0.9, step: 4, keys: [28, 100], level: 0.95, release: 0.12, fade: 0.25,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-9, 9]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.45; }
      const pu = osc("sq", c0, L, n, rnd(), 0.3); for (let i = 0; i < n; i++) x[i] += pu[i] * 0.25;
      const y = ladder(x, (t) => Math.min(12000, f0 * 14) * expEnv(t, 0, 0.16, 1, 0.12) + 250, 0.9, 1.2);
      return y.map((v, i) => { const t = i / SR; return v * smooth(t / 0.002) * expEnv(t, 0.02, 0.8, 1, 0.01); });
    },
  },
  // ジュピター系のポリシンセ（GM 90）: ソー 2 本＋パルス（PWM 風にゆらす）、アンサンブルコーラス、ゆるい立ち上がり
  "synth-poly-analog": {
    program: 90, loop: 88200, pre: 35280, step: 4, keys: [28, 100], level: 0.95, release: 0.55,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-8, 8]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.4; }
      const pu = osc("sq", c0, L, n, rnd(), 0.5); for (let i = 0; i < n; i++) x[i] += pu[i] * 0.2;
      const y = ladder(x, (t) => Math.min(9000, f0 * 3.2 + 900) * (0.55 + 0.45 * smooth(t / 0.25)), 0.3, 1.0);
      const e = ensemble(y, L, [
        { base: 0.011, depth: 0.0030, cycles: 1, phase: 0, gain: 0.5 },
        { base: 0.016, depth: 0.0035, cycles: 2, phase: 2.1, gain: 0.5 },
      ]);
      return e.map((v, i) => v * smooth(i / SR / 0.14));
    },
  },
  // シンセブラス（GM 62）: ソー 2 本（±4 セント）。フィルターが頭でふくらんで落ち着く（ジュピター・ミニムーグのブラス）
  "synth-brass-analog": {
    program: 62, loop: 88200, pre: 26460, step: 4, keys: [28, 96], level: 0.85, release: 0.2,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-4, 4]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.5; }
      const base = Math.min(8000, f0 * 3 + 700);
      const fc = (t) => base * (t < 0.14 ? 0.35 + 1.55 * smooth(t / 0.14) : 1.9 - 0.9 * smooth((t - 0.14) / 0.2));
      const y = ladder(x, fc, 0.6, 1.2);
      return y.map((v, i) => v * smooth(i / SR / 0.03));
    },
  },
  // ストリングスマシン（GM 50）: 3 本のソー＋上のオクターブ、3 つのコーラス（ソリーナ風）、やわらかい立ち上がり
  "synth-strings-machine": {
    program: 50, loop: 88200, pre: 44100, step: 4, keys: [28, 100], level: 0.95, release: 0.5,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-9, 0, 9]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.3; }
      const up = osc("saw", cyc(f0 * 2), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += up[i] * 0.16;
      let y = onepole(onepole(x, Math.min(5200, f0 * 6 + 1800)), Math.min(7000, f0 * 9 + 2500));
      y = ensemble(y, L, [
        { base: 0.0095, depth: 0.0022, cycles: 1, phase: 0.0, gain: 0.34 },
        { base: 0.0120, depth: 0.0020, cycles: 1, phase: 2.1, gain: 0.34 },
        { base: 0.0150, depth: 0.0018, cycles: 1, phase: 4.2, gain: 0.34 },
        { base: 0.0045, depth: 0.0006, cycles: 12, phase: 1.0, gain: 0.22 },
      ]);
      return y.map((v, i) => v * smooth(i / SR / 0.22));
    },
  },
  // ムーグ系ベース（GM 38）: ソー＋パルス＋1 オクターブ下のサブ。24dB ラダーの頭がパクッと開いて落ち着く
  "synth-bass-moog": {
    program: 38, loop: 44100, pre: 39690, step: 4, keys: [24, 72], level: 0.8, release: 0.12, even: true,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      const s = osc("saw", c0, L, n, rnd()); const p = osc("sq", c0, L, n, rnd(), 0.5); const sub = osc("sq", c0, L, n, rnd(), 0.5, 0.5);
      for (let i = 0; i < n; i++) x[i] = s[i] * 0.45 + p[i] * 0.3 + sub[i] * 0.4;
      const y = ladder(x, (t) => 380 + f0 * 2.2 + 3200 * Math.exp(-t / 0.09), 1.5, 1.3);
      return y.map((v, i) => v * smooth(i / SR / 0.003));
    },
  },
  // アシッドベース（GM 39）: ソー 1 本、レゾナンスを強くしたラダー、フィルターが速く閉じる（303 風）
  "synth-bass-acid": {
    program: 39, loop: 44100, pre: 39690, step: 4, keys: [24, 72], level: 0.8, release: 0.1, even: true,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = osc("saw", c0, L, n, rnd());
      const y = ladder(x, (t) => 300 + f0 * 1.3 + 3600 * Math.exp(-t / 0.075), 3.0, 1.2);
      return y.map((v, i) => v * smooth(i / SR / 0.002));
    },
  },
  // ── 2026-10-20 人間「電子音楽、テクノポップ、ダンスミュージック、ボカロ向けの音源も追加して」──
  // EDM・ボカロのプラック（GM 85）: ソー 3 本（±12 セント）＋1 オクターブ上の薄いソー。フィルターが「ポン」と閉じて、0.9 秒で消える（ループなし）
  "synth-pluck-edm": {
    program: 85, loop: 0, total: 1.1, step: 4, keys: [36, 100], level: 0.95, release: 0.15, fade: 0.3,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-12, 0, 12]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.33; }
      const up = osc("saw", cyc(f0 * 2), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += up[i] * 0.12;
      const y = ladder(highpass(x, 120), (t) => 200 + Math.min(11000, f0 * 10) * Math.exp(-t / 0.11), 0.6, 1.1);
      return y.map((v, i) => { const t = i / SR; return v * smooth(t / 0.0015) * expEnv(t, 0.01, 1.0, 1, 0.004); });
    },
  },
  // チップチューン（ファミコン風）のパルス波 25%（GM 124）: フィルターなしの角ばった音。ごく浅いビブラートは入れない（曲の ~ で付ける）
  "synth-chip-pulse25": {
    program: 124, loop: 88200, pre: 4410, step: 4, keys: [36, 100], level: 0.6, release: 0.05,
    render: ({ f0, cyc, L, n, rnd }) => {
      const p = osc("sq", cyc(f0), L, n, rnd(), 0.25);
      return p.map((v, i) => v * smooth(i / SR / 0.002));
    },
  },
  // チップチューンのパルス波 12.5%（GM 125）: 細く鼻にかかった音（伴奏・アルペジオ向き）
  "synth-chip-pulse12": {
    program: 125, loop: 88200, pre: 4410, step: 4, keys: [36, 100], level: 0.6, release: 0.05,
    render: ({ f0, cyc, L, n, rnd }) => {
      const p = osc("sq", cyc(f0), L, n, rnd(), 0.125);
      return p.map((v, i) => v * smooth(i / SR / 0.002));
    },
  },
  // リースベース（GM 34）: ソー 2 本を ±16 セントずらしてうねらせ（ドラムンベース・ダブステップ・ボカロの太いベース）、サブのサイン、ラダーで 900Hz 前後に
  "synth-bass-reese": {
    program: 34, loop: 88200, pre: 22050, step: 4, keys: [24, 72], level: 0.8, release: 0.15, even: true,
    render: ({ f0, cyc, L, n, rnd }) => {
      const c0 = cyc(f0); const x = new Float64Array(n);
      for (const d of [-16, 16]) { const o = osc("saw", Math.round(c0 * cents(d)), L, n, rnd()); for (let i = 0; i < n; i++) x[i] += o[i] * 0.45; }
      const sub = osc("sin", c0, L, n, 0); for (let i = 0; i < n; i++) x[i] += sub[i] * 0.5;
      const y = ladder(x, () => Math.min(1400, 500 + f0 * 4), 0.4, 1.4);
      return y.map((v, i) => v * smooth(i / SR / 0.004));
    },
  },
};

// ---------- 書き出し ----------
const results = [];
for (const [name, def] of Object.entries(INSTR)) {
  if (only && !only.test(name)) continue;
  const dir = path.join(workDir, name); fs.mkdirSync(dir, { recursive: true });
  const L = def.loop || Math.round((def.total ?? 0.9) * SR);
  const n = def.loop ? def.pre + L + 2205 : L;
  const lines = [];
  const keys = []; for (let k = def.keys[0]; k <= def.keys[1]; k += def.step) keys.push(k);
  for (const k of keys) {
    const f0 = midiHz(k);
    // 全オシレーターの周期の数を整数にする。基音は f0 に最も近い整数（ベースはサブのオクターブ下のため偶数）
    const cyc = (f) => { const c = f * L / SR; return def.even ? 2 * Math.max(1, Math.round(c / 2)) : Math.max(1, Math.round(c)); };
    const rnd = rng(k * 7919 + name.length);
    const x = highpass(def.render({ f0, cyc, L, pre: def.pre, n, rnd }), 22);
    let pk = 0; for (let i = 0; i < n; i++) pk = Math.max(pk, Math.abs(x[i]));
    if (!(pk > 1e-6)) throw new Error(`無音: ${name} ${k}`);
    const g = def.level / pk;
    const y = new Float64Array(n); for (let i = 0; i < n; i++) y[i] = x[i] * g;
    writeWav(path.join(dir, `${name}_${k}.wav`), y);
    const f0eff = cyc(f0) * SR / L; // ループ長 L のなかに cyc(f0) 周期 = 実際の基音
    const tune = Math.round(-1200 * Math.log2(f0eff / f0));
    const lo = k === keys[0] ? 0 : k - def.step / 2 + 1, hi = k === keys[keys.length - 1] ? 127 : k + def.step / 2;
    lines.push(`<region> sample=${name}_${k}.wav pitch_keycenter=${k} lokey=${lo} hikey=${hi} tune=${tune}` + (def.loop ? ` loop_mode=loop_continuous loop_start=${def.pre} loop_end=${def.pre + L}` : ""));
  }
  fs.writeFileSync(path.join(dir, `${name}.sfz`), lines.join("\n") + "\n");
  const a = ["tools/soundfont/sfz-to-sf3.mjs", path.join(dir, `${name}.sfz`), name, "--program", String(def.program), "--seconds", String(def.loop ? (n / SR + 0.1).toFixed(2) : (L / SR).toFixed(2)), "--rr", "1", "--q", "4", "--release", String(def.release ?? 0.3), "--fade", String(def.fade ?? 0.3)];
  if (def.loop) a.push("--loop");
  const o = execFileSync("node", a, { encoding: "utf8" });
  console.log(o.trim().split("\n").pop());
  results.push(name);
}
console.log("作った音色:", results.join(", "));
