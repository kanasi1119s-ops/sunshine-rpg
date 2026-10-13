// 録音のタム（Muldjord Kit。CC BY 4.0）から、ロートタム・キャノンタム・インチ違いのタムを作る。
//   元の録音は drums-muldjord.sf3 の中の Tom1〜Tom4（強さ4層）。音程を測り、鍵盤の高さに合わせて音程をずらして使う（±数半音まで）。
//   インチ違い＝音程をずらしただけ（大きい太鼓＝低い音）／キャノン＝余韻を短く・高域をやや丸く・少し低く／ロート＝打った直後に音程が上がって落ちる動き（変調エンベロープ）・響きを長めに
import fs from "fs";
import os from "os";
import path from "path";
import { execFileSync } from "child_process";
import { BasicSample, SampleTypes } from "spessasynth_core";
import { SR, loadBank, timecents, GeneratorTypes } from "./lib.mjs";

function decodeOgg(bytes) {
  const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "tom-")), "a.ogg");
  fs.writeFileSync(f, bytes);
  const buf = execFileSync("ffmpeg", ["-v", "error", "-i", f, "-ac", "1", "-ar", String(SR), "-f", "f32le", "-"], { maxBuffer: 1 << 28 });
  return new Float32Array(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
}

/** 重さを足す: 低域を持ち上げ（約+6dB・160Hz以下）、さらに1オクターブ下の低い胴鳴り（元の低域をゆっくり再生したもの）を小さく重ねる。 */
function addWeight(x) {
  const n = x.length;
  const a = Math.exp((-2 * Math.PI * 160) / SR);
  let lp = 0;
  const low = new Float32Array(n);
  for (let i = 0; i < n; i++) { lp = a * lp + (1 - a) * x[i]; low[i] = lp; }
  // 低域の持ち上げ（低域をもう1回足す＝約+6dB）
  const sub = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const pos = i * 0.5, j = Math.floor(pos), fr = pos - j; // 半分の速さ＝1オクターブ下
    sub[i] = j + 1 < n ? low[j] * (1 - fr) + low[j + 1] * fr : 0;
  }
  for (let i = 0; i < n; i++) x[i] += 1.0 * low[i] + 0.7 * sub[i];
}

/** 基本の高さ（MIDIのノート番号、小数）を測る。打った直後を避けて 0.04〜0.4 秒を見る。 */
function detectTomMidi(x) {
  const a = Math.floor(SR * 0.04), N = Math.min(Math.floor(SR * 0.36), x.length - a);
  const seg = x.subarray(a, a + N);
  const minLag = Math.floor(SR / 420), maxLag = Math.floor(SR / 55);
  let best = -1, bl = 0;
  const r = new Float32Array(maxLag + 2);
  for (let lag = minLag; lag <= maxLag + 1; lag++) {
    let s = 0, e0 = 0, e1 = 0;
    for (let i = 0; i < N - maxLag - 1; i++) { s += seg[i] * seg[i + lag]; e0 += seg[i] * seg[i]; e1 += seg[i + lag] * seg[i + lag]; }
    r[lag] = s / Math.sqrt(e0 * e1 + 1e-12);
  }
  for (let lag = minLag + 1; lag <= maxLag; lag++) if (r[lag] > best && r[lag] >= r[lag - 1] && r[lag] >= r[lag + 1]) { best = r[lag]; bl = lag; }
  const d = r[bl - 1] - 2 * r[bl] + r[bl + 1];
  const off = d ? (0.5 * (r[bl - 1] - r[bl + 1])) / d : 0;
  return { midi: 69 + 12 * Math.log2(SR / (bl + off) / 440), conf: best };
}

/** out（BasicSoundBank）に、プログラム 117（ロート）・118（キャノン）・119（インチ違い）を足す。 */
export function addRealToms(out, emptyInstrument, kitFile, report = console.log) {
  const kit = loadBank(kitFile);
  const preset = kit.presets.find((p) => p.isGMGSDrum && p.program === 0);
  const toms = new Map(); // "Tom1" → { v: { 1: [L, R] ... } }
  for (const pz of preset.zones) for (const z of pz.instrument.zones) {
    const kr = z.keyRange;
    if (kr.min !== kr.max || ![41, 43, 45, 47, 48, 50].includes(kr.min)) continue;
    const m = /^(Tom\d+) v(\d+) ([LR])$/.exec(z.sample.name);
    if (!m) continue;
    const t = toms.get(m[1]) ?? new Map();
    const layer = t.get(Number(m[2])) ?? {};
    layer[m[3]] = z.sample;
    t.set(Number(m[2]), layer);
    toms.set(m[1], t);
  }
  const bank = [];
  for (const [name, layers] of toms) {
    const vs = [...layers.keys()].sort((a, b) => a - b);
    const items = [];
    for (const v of vs) {
      const l = layers.get(v);
      const L = decodeOgg(l.L.compressedData), R = l.R ? decodeOgg(l.R.compressedData) : L;
      const n = Math.min(L.length, R.length, Math.floor(SR * 2.2));
      const mono = new Float32Array(n);
      for (let i = 0; i < n; i++) mono[i] = 0.5 * (L[i] + R[i]);
      // 終わりをなめらかに消す
      const fade = Math.floor(SR * 0.25);
      for (let i = 0; i < fade && i < n; i++) mono[n - 1 - i] *= i / fade;
      items.push({ v, data: mono });
    }
    const loud = items[items.length - 1];
    const pitch = detectTomMidi(loud.data); // 重さを足す前に測る（低域を足すと1オクターブ下に誤って測れる）
    for (const it of items) addWeight(it.data);
    // 音の大きさ: 強い層の頭0.3秒の rms を目標にそろえる（層どうしの強弱は元のまま）
    let s = 0; const m = Math.floor(SR * 0.3); for (let i = 0; i < m; i++) s += loud.data[i] ** 2;
    const g = 0.12 / Math.sqrt(s / m);
    for (const it of items) for (let i = 0; i < it.data.length; i++) it.data[i] *= g;
    bank.push({ name, items, midi: pitch.midi, conf: pitch.conf });
    report(`${name}: 基本 ${pitch.midi.toFixed(2)}（${(440 * 2 ** ((pitch.midi - 69) / 12)).toFixed(0)}Hz）確からしさ ${pitch.conf.toFixed(2)} 強さ層 ${vs.join(",")}`);
  }
  bank.sort((a, b) => a.midi - b.midi);
  const lo = Math.floor(bank[0].midi) - 8, hi = Math.ceil(bank.at(-1).midi) + 12;
  const kinds = [
    { program: 117, name: "Roto Tom", tune: 0.5, fc: null, decay: null, bend: 180, release: 1.4 },
    { program: 118, name: "Cannon Tom", tune: -1.2, fc: 5200, decay: 0.28, bend: 0, release: 0.25 },
    { program: 119, name: "Inch Tom", tune: 0, fc: null, decay: null, bend: 0, release: 0.8 },
  ];
  let zones = 0;
  const cache = new Map();
  const sample = (tom, it) => {
    const k = tom.name + it.v;
    if (!cache.has(k)) {
      const rootMidi = Math.round(tom.midi);
      const s2 = new BasicSample(`${tom.name} v${it.v}`, SR, rootMidi, Math.round((tom.midi - rootMidi) * -100), SampleTypes.monoSample, 0, 0);
      s2.setAudioData(it.data, SR);
      out.addSamples(s2);
      cache.set(k, s2);
    }
    return cache.get(k);
  };
  for (const kd of kinds) {
    const inst = emptyInstrument(kd.program, kd.name);
    for (let key = Math.max(0, lo); key <= Math.min(127, hi); key++) {
      // いちばん近い高さの太鼓を使う（音程のずらしを小さくする）
      const tom = bank.reduce((b, t) => (Math.abs(t.midi - key) < Math.abs(b.midi - key) ? t : b), bank[0]);
      const vs = tom.items.map((i) => i.v);
      tom.items.forEach((it, idx) => {
        const z = inst.createZone(sample(tom, it));
        z.keyRange = { min: key, max: key };
        z.velRange = { min: idx === 0 ? 1 : it.v, max: idx === tom.items.length - 1 ? 127 : tom.items[idx + 1].v - 1 };
        z.setGenerator(GeneratorTypes.overridingRootKey, Math.round(tom.midi));
        if (kd.tune) z.setGenerator(GeneratorTypes.fineTune, Math.round(kd.tune * 100));
        z.setGenerator(GeneratorTypes.releaseVolEnv, timecents(kd.release));
        z.setGenerator(GeneratorTypes.attackVolEnv, timecents(0.001));
        if (kd.decay) { z.setGenerator(GeneratorTypes.decayVolEnv, timecents(kd.decay)); z.setGenerator(GeneratorTypes.sustainVolEnv, 1000); }
        if (kd.fc) z.setGenerator(GeneratorTypes.initialFilterFc, Math.round(1200 * Math.log2(kd.fc / 8.176)));
        if (kd.bend) { z.setGenerator(GeneratorTypes.modEnvToPitch, kd.bend); z.setGenerator(GeneratorTypes.decayModEnv, timecents(0.07)); z.setGenerator(GeneratorTypes.sustainModEnv, 1000); }
        void vs;
        zones++;
      });
    }
  }
  report(`録音のタム: 太鼓 ${bank.length} 本・鍵盤 ${lo}〜${hi}・ゾーン ${zones}`);
  return zones;
}
