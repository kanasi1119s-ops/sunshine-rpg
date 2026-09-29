import type { ScheduledNote } from "./score";

/**
 * 楽器の音色をWeb Audioの部品（発振器・ノイズ・フィルター・歪み）から作る。音声ファイルは使わない。
 * ゲーム本体（audio-engine.ts）と、書き出し・BGMプレイヤーの両方から使う。
 * 通常のAudioContextでもOfflineAudioContextでも動く。
 */

type Ctx = BaseAudioContext;
export type Source = AudioScheduledSourceNode;

const noiseCache = new WeakMap<Ctx, AudioBuffer>();
const curveCache = new Map<number, Float32Array<ArrayBuffer>>();

function noiseBuffer(ctx: Ctx): AudioBuffer {
  let buf = noiseCache.get(ctx);
  if (!buf) {
    buf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
    const data = buf.getChannelData(0);
    let seed = 12345;
    for (let i = 0; i < data.length; i++) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      data[i] = seed / 2147483648 - 1;
    }
    noiseCache.set(ctx, buf);
  }
  return buf;
}

/** 歪み（ギターのディストーション）の波形。drive が大きいほど強く歪む。 */
function distortionCurve(drive: number): Float32Array<ArrayBuffer> {
  let curve = curveCache.get(drive);
  if (!curve) {
    curve = new Float32Array(2048);
    for (let i = 0; i < curve.length; i++) {
      const x = (i / (curve.length - 1)) * 2 - 1;
      curve[i] = Math.tanh(x * drive);
    }
    curveCache.set(drive, curve);
  }
  return curve;
}

/** BGM全体の出口。ほのかな残響と、音が重なっても割れないようにするコンプレッサーを通す。 */
export function createBgmBus(ctx: Ctx, destination: AudioNode): GainNode {
  const comp = ctx.createDynamicsCompressor();
  comp.threshold.value = -16;
  comp.knee.value = 12;
  comp.ratio.value = 4;
  comp.attack.value = 0.004;
  comp.release.value = 0.2;
  comp.connect(destination);

  const bus = ctx.createGain();
  const dry = ctx.createGain();
  dry.gain.value = 0.85;
  bus.connect(dry);
  dry.connect(comp);

  const seconds = 2.2;
  const length = Math.floor(ctx.sampleRate * seconds);
  const impulse = ctx.createBuffer(2, length, ctx.sampleRate);
  let seed = 987;
  for (let ch = 0; ch < 2; ch++) {
    const data = impulse.getChannelData(ch);
    for (let i = 0; i < length; i++) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      data[i] = (seed / 2147483648 - 1) * Math.pow(1 - i / length, 2.6);
    }
  }
  const convolver = ctx.createConvolver();
  convolver.buffer = impulse;
  const wet = ctx.createGain();
  wet.gain.value = 0.24;
  bus.connect(convolver);
  convolver.connect(wet);
  wet.connect(comp);
  return bus;
}

/** 立ち上がり→保つ→消える、のゲイン。持続音（弦・パッド・ギターのロングトーンなど）用。 */
function sustainGain(ctx: Ctx, dest: AudioNode, t: number, d: number, peak: number, attack: number, release: number): GainNode {
  const g = ctx.createGain();
  const end = t + Math.max(d, attack + 0.02);
  const rel = Math.min(release, Math.max(0.02, d * 0.5));
  g.gain.setValueAtTime(0.0001, t);
  g.gain.linearRampToValueAtTime(peak, t + attack);
  g.gain.setValueAtTime(peak, Math.max(t + attack, end - rel));
  g.gain.linearRampToValueAtTime(0, end + Math.max(0, release - rel));
  g.connect(dest);
  return g;
}

/** 弾いた瞬間が最大で、しだいに消えていくゲイン。ピアノ・弦をはじく音・打楽器用。 */
function pluckGain(ctx: Ctx, dest: AudioNode, t: number, peak: number, attack: number, decay: number): GainNode {
  const g = ctx.createGain();
  g.gain.setValueAtTime(0.0001, t);
  g.gain.linearRampToValueAtTime(peak, t + attack);
  g.gain.exponentialRampToValueAtTime(Math.max(0.0001, peak * 0.002), t + attack + decay);
  g.connect(dest);
  return g;
}

function osc(ctx: Ctx, type: OscillatorType, freq: number, t: number, stop: number, dest: AudioNode, level = 1, detune = 0): OscillatorNode {
  const o = ctx.createOscillator();
  o.type = type;
  o.frequency.value = freq;
  o.detune.value = detune;
  if (level === 1) {
    o.connect(dest);
  } else {
    const g = ctx.createGain();
    g.gain.value = level;
    o.connect(g);
    g.connect(dest);
  }
  o.start(t);
  o.stop(stop);
  return o;
}

function filter(ctx: Ctx, type: BiquadFilterType, freq: number, dest: AudioNode, q = 0.7): BiquadFilterNode {
  const f = ctx.createBiquadFilter();
  f.type = type;
  f.frequency.value = freq;
  f.Q.value = q;
  f.connect(dest);
  return f;
}

function noise(ctx: Ctx, t: number, stop: number, dest: AudioNode): AudioBufferSourceNode {
  const src = ctx.createBufferSource();
  src.buffer = noiseBuffer(ctx);
  src.loop = true;
  src.connect(dest);
  src.start(t, (t * 7.3) % 0.9);
  src.stop(stop);
  return src;
}

function distorted(ctx: Ctx, dest: AudioNode, drive: number, cutoff: number): BiquadFilterNode {
  const lp = filter(ctx, "lowpass", cutoff, dest, 0.6);
  const shaper = ctx.createWaveShaper();
  shaper.curve = distortionCurve(drive);
  shaper.oversample = "2x";
  shaper.connect(lp);
  // 呼び出し側は、歪ませたい音をこのフィルターの手前（shaper）に入れる。
  const pre = ctx.createBiquadFilter();
  pre.type = "highpass";
  pre.frequency.value = 70;
  pre.connect(shaper);
  return pre;
}

function voice(ctx: Ctx, dest: AudioNode, e: ScheduledNote, t: number): Source[] {
  const f = e.frequency;
  const d = e.durationSec;
  const v = e.volume;
  const out: Source[] = [];
  switch (e.instrument) {
    case "kick": {
      const g = pluckGain(ctx, dest, t, v * 1.5, 0.002, 0.28);
      const o = ctx.createOscillator();
      o.type = "sine";
      o.frequency.setValueAtTime(150, t);
      o.frequency.exponentialRampToValueAtTime(42, t + 0.13);
      o.connect(g);
      o.start(t);
      o.stop(t + 0.36);
      out.push(o);
      break;
    }
    case "snare": {
      const hp = filter(ctx, "highpass", 1400, pluckGain(ctx, dest, t, v * 0.9, 0.002, 0.17));
      out.push(noise(ctx, t, t + 0.22, hp));
      out.push(osc(ctx, "triangle", 190, t, t + 0.14, pluckGain(ctx, dest, t, v * 0.5, 0.002, 0.09)));
      break;
    }
    case "hihat": {
      const open = d > 0.3;
      const hp = filter(ctx, "highpass", 7500, pluckGain(ctx, dest, t, v * 0.5, 0.001, open ? 0.24 : 0.045));
      out.push(noise(ctx, t, t + (open ? 0.3 : 0.08), hp));
      break;
    }
    case "crash": {
      const hp = filter(ctx, "highpass", 5000, pluckGain(ctx, dest, t, v * 0.6, 0.003, 1.4));
      out.push(noise(ctx, t, t + 1.5, hp));
      break;
    }
    case "bass": {
      const g = sustainGain(ctx, dest, t, d, v, 0.006, 0.07);
      const lp = filter(ctx, "lowpass", 720, g);
      out.push(osc(ctx, "triangle", f, t, t + d + 0.1, lp));
      out.push(osc(ctx, "square", f, t, t + d + 0.1, lp, 0.35));
      break;
    }
    case "guitar":
    case "echoGuitar": {
      const taps = e.instrument === "echoGuitar" ? [0, 0.46, 0.92, 1.38] : [0];
      taps.forEach((delay, n) => {
        const decay = Math.max(0.3, Math.min(d * 1.2, 1.5));
        const g = pluckGain(ctx, dest, t + delay, v * Math.pow(0.5, n), 0.004, decay);
        const lp = ctx.createBiquadFilter();
        lp.type = "lowpass";
        lp.Q.value = 1;
        lp.frequency.setValueAtTime(3400, t + delay);
        lp.frequency.exponentialRampToValueAtTime(1000, t + delay + 0.28);
        lp.connect(g);
        const stop = t + delay + decay + 0.05;
        out.push(osc(ctx, "sawtooth", f, t + delay, stop, lp, 0.6));
        out.push(osc(ctx, "sawtooth", f, t + delay, stop, lp, 0.4, 8));
      });
      break;
    }
    case "crunch":
    case "distGuitar": {
      const metal = e.instrument === "distGuitar";
      const short = d < 0.3;
      const g = sustainGain(ctx, dest, t, d, v * 0.7, 0.005, 0.05);
      const input = distorted(ctx, g, metal ? 9 : 3.2, short ? 1500 : metal ? 3400 : 2800);
      const stop = t + d + 0.06;
      out.push(osc(ctx, "sawtooth", f, t, stop, input, 0.6));
      out.push(osc(ctx, "square", f, t, stop, input, 0.3, -6));
      out.push(osc(ctx, "sawtooth", f * 1.5, t, stop, input, 0.45)); // 5度を足したパワーコード
      if (metal) {
        out.push(osc(ctx, "square", f * 2, t, stop, input, 0.2));
      }
      break;
    }
    case "leadGuitar":
    case "lead": {
      const guitar = e.instrument === "leadGuitar";
      const g = sustainGain(ctx, dest, t, d, v, 0.012, 0.09);
      const input = guitar ? distorted(ctx, g, 5, 4200) : filter(ctx, "lowpass", 5200, g);
      const stop = t + d + 0.1;
      const a = osc(ctx, guitar ? "sawtooth" : "square", f, t, stop, input, 0.7);
      const b = osc(ctx, "sawtooth", f, t, stop, input, 0.3, 7);
      // ビブラート（音程をゆらす）。音が伸びたところから、少しずつかかる
      const lfo = ctx.createOscillator();
      lfo.frequency.value = 5.4;
      const depth = ctx.createGain();
      depth.gain.setValueAtTime(0, t);
      depth.gain.linearRampToValueAtTime(guitar ? 22 : 14, t + Math.min(0.35, d));
      lfo.connect(depth);
      depth.connect(a.detune);
      depth.connect(b.detune);
      lfo.start(t);
      lfo.stop(stop);
      out.push(a, b, lfo);
      break;
    }
    case "keys": {
      const decay = Math.max(0.5, Math.min(d * 1.4, 1.6));
      const g = pluckGain(ctx, dest, t, v, 0.004, decay);
      const stop = t + decay + 0.05;
      out.push(osc(ctx, "sine", f, t, stop, g, 0.9));
      out.push(osc(ctx, "sine", f * 2, t, stop, pluckGain(ctx, dest, t, v * 0.32, 0.003, 0.35), 1));
      out.push(osc(ctx, "triangle", f * 4, t, t + 0.2, pluckGain(ctx, dest, t, v * 0.16, 0.002, 0.12), 1));
      break;
    }
    case "piano": {
      const decay = Math.max(0.6, Math.min(d * 1.6, 2.2));
      const stop = t + decay + 0.05;
      out.push(osc(ctx, "triangle", f, t, stop, pluckGain(ctx, dest, t, v, 0.003, decay)));
      out.push(osc(ctx, "sine", f * 2, t, stop, pluckGain(ctx, dest, t, v * 0.4, 0.003, decay * 0.6)));
      out.push(osc(ctx, "sine", f * 3, t, t + 0.6, pluckGain(ctx, dest, t, v * 0.18, 0.003, 0.3)));
      break;
    }
    case "harpsichord": {
      const decay = Math.max(0.25, Math.min(d, 0.7));
      const g = pluckGain(ctx, dest, t, v, 0.002, decay);
      const lp = filter(ctx, "lowpass", 4800, g);
      const stop = t + decay + 0.05;
      out.push(osc(ctx, "sawtooth", f, t, stop, lp, 0.7));
      out.push(osc(ctx, "square", f * 2, t, stop, lp, 0.28));
      break;
    }
    case "strings": {
      const g = sustainGain(ctx, dest, t, d, v, Math.min(0.2, d * 0.4), 0.3);
      const lp = filter(ctx, "lowpass", 2300, g);
      const stop = t + d + 0.35;
      out.push(osc(ctx, "sawtooth", f, t, stop, lp, 0.4, -9));
      out.push(osc(ctx, "sawtooth", f, t, stop, lp, 0.4, 9));
      out.push(osc(ctx, "triangle", f, t, stop, lp, 0.4));
      break;
    }
    case "pad": {
      const g = sustainGain(ctx, dest, t, d, v, Math.min(0.9, d * 0.4), 1.0);
      const lp = filter(ctx, "lowpass", 1400, g);
      const stop = t + d + 1.05;
      out.push(osc(ctx, "sine", f, t, stop, lp, 0.6));
      out.push(osc(ctx, "triangle", f, t, stop, lp, 0.35, 11));
      out.push(osc(ctx, "sine", f * 2, t, stop, lp, 0.2, -7));
      break;
    }
    case "sfxDown":
    case "sfxUp": {
      // 音程が滑る効果音（下がる＝やられた・落ちる、上がる＝回復・跳ぶ）
      const g = sustainGain(ctx, dest, t, d, v, 0.004, Math.min(0.06, d * 0.4));
      const o = ctx.createOscillator();
      o.type = e.waveform;
      o.frequency.setValueAtTime(f, t);
      o.frequency.exponentialRampToValueAtTime(e.instrument === "sfxDown" ? f * 0.3 : f * 2.6, t + Math.max(0.05, d));
      o.connect(g);
      o.start(t);
      o.stop(t + d + 0.08);
      out.push(o);
      break;
    }
    case "impact": {
      // 打撃・足音・爆発。ノイズを下がっていくフィルターに通し、低い「ドン」を重ねる
      const decay = Math.max(0.08, Math.min(d * 1.2, 0.6));
      const lp = ctx.createBiquadFilter();
      lp.type = "lowpass";
      lp.frequency.setValueAtTime(Math.min(4000, f * 6), t);
      lp.frequency.exponentialRampToValueAtTime(Math.max(120, f), t + decay);
      lp.connect(pluckGain(ctx, dest, t, v, 0.002, decay));
      out.push(noise(ctx, t, t + decay + 0.05, lp));
      const thump = ctx.createOscillator();
      thump.type = "sine";
      thump.frequency.setValueAtTime(f, t);
      thump.frequency.exponentialRampToValueAtTime(Math.max(30, f * 0.35), t + decay * 0.8);
      thump.connect(pluckGain(ctx, dest, t, v * 0.8, 0.002, decay * 0.8));
      thump.start(t);
      thump.stop(t + decay + 0.05);
      out.push(thump);
      break;
    }
    case "swoosh": {
      // 風を切る音・走り抜ける音・魔法の立ち上がり。帯域が上へ動く
      const dur = Math.max(0.1, d);
      const bp = ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.Q.value = 1.2;
      bp.frequency.setValueAtTime(f, t);
      bp.frequency.exponentialRampToValueAtTime(f * 6, t + dur);
      bp.connect(sustainGain(ctx, dest, t, dur, v * 1.4, dur * 0.45, dur * 0.5));
      out.push(noise(ctx, t, t + dur + 0.1, bp));
      break;
    }
    case "chime": {
      const stop = t + 0.7;
      out.push(osc(ctx, "sine", f, t, stop, pluckGain(ctx, dest, t, v, 0.002, 0.6)));
      out.push(osc(ctx, "sine", f * 2.4, t, stop, pluckGain(ctx, dest, t, v * 0.4, 0.002, 0.3)));
      out.push(osc(ctx, "triangle", f * 4, t, t + 0.2, pluckGain(ctx, dest, t, v * 0.2, 0.002, 0.1)));
      break;
    }
    case "bell": {
      const stop = t + 2.6;
      out.push(osc(ctx, "sine", f, t, stop, pluckGain(ctx, dest, t, v, 0.003, 2.4)));
      out.push(osc(ctx, "sine", f * 2.76, t, stop, pluckGain(ctx, dest, t, v * 0.32, 0.003, 1.2)));
      out.push(osc(ctx, "sine", f * 5.4, t, stop, pluckGain(ctx, dest, t, v * 0.12, 0.003, 0.5)));
      break;
    }
  }
  return out;
}

/** 楽器の指定がある音を予約する。指定がなければ空の配列を返す（呼び出し側が従来の音を鳴らす）。 */
export function scheduleInstrumentNote(ctx: Ctx, destination: AudioNode, event: ScheduledNote, when: number): Source[] {
  return event.instrument ? voice(ctx, destination, event, when) : [];
}
