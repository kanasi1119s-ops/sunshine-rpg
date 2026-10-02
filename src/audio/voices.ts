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

/** 入力が knee 以下はそのまま、それより上は ceiling に向けてなめらかに近づく（超えない）カーブ。 */
export function ceilingCurve(knee: number, ceiling: number, samples = 2049): Float32Array<ArrayBuffer> {
  const curve = new Float32Array(new ArrayBuffer(samples * 4));
  const range = ceiling - knee;
  for (let i = 0; i < samples; i++) {
    const x = (i * 2) / (samples - 1) - 1;
    const a = Math.abs(x);
    const y = a <= knee ? a : knee + range * Math.tanh((a - knee) / range);
    curve[i] = Math.sign(x) * y;
  }
  return curve;
}

/** 楽器ごとの残響の送り先（S-4）。`dryIn` は残響を通さず直接出口へ、`wetIn` は残響にだけ足す。 */
const busSends = new WeakMap<AudioNode, { dryIn: AudioNode; wetIn: AudioNode }>();

/** 残響を少なくする楽器（低音とリズム）と、多くする楽器（弦・パッド・ピアノなど）。 */
const DRY_INSTRUMENTS = new Set(["kick", "snare", "hihat", "tom", "bass", "slap", "sub808"]);
const WET_INSTRUMENTS = new Set(["strings", "pad", "choir", "piano", "harp", "chime", "bell"]);
/** 多めの楽器が残響へ余分に送る量 */
const EXTRA_WET_SEND = 0.5;

/** BGM全体の出口。ほのかな残響と、音が重なっても割れないようにするコンプレッサーを通す。 */
export function createBgmBus(ctx: Ctx, destination: AudioNode, wetLevel = 0.24, reverbSec = 2.2, widen = 1.6): GainNode {
  // 最終段: 音が重なっても割れないようにする歯止め（リミッター）と、全体の音量の底上げ
  const limiter = ctx.createDynamicsCompressor();
  limiter.threshold.value = -0.5;
  limiter.knee.value = 0;
  limiter.ratio.value = 12;
  limiter.attack.value = 0.002;
  limiter.release.value = 0.1;
  // 最後の安全装置: リミッターが追いつかなかった瞬間のピークだけをなめらかに丸め、出力が ±0.98 を超えない（音割れしない）ようにする。
  // 0.7 より小さい音はほぼそのまま通す
  const guard = ctx.createWaveShaper();
  guard.curve = ceilingCurve(0.7, 0.98);
  guard.oversample = "4x";
  limiter.connect(guard);
  guard.connect(destination);
  const makeup = ctx.createGain();
  makeup.gain.value = 1.0;
  makeup.connect(limiter);
  // 音の仕上げ: 低音とキラキラした高音を少し持ち上げる（現代的なゲーム音楽らしい厚みと抜けの良さ）
  const low = ctx.createBiquadFilter();
  low.type = "lowshelf";
  low.frequency.value = 95;
  low.gain.value = 3;
  // 3kHz付近を少し持ち上げて、旋律とアタックの輪郭をはっきりさせる
  const presence = ctx.createBiquadFilter();
  presence.type = "peaking";
  presence.frequency.value = 3200;
  presence.Q.value = 0.9;
  presence.gain.value = 0.7;
  const high = ctx.createBiquadFilter();
  high.type = "highshelf";
  high.frequency.value = 8000;
  high.gain.value = 1.2;
  low.connect(presence);
  presence.connect(high);
  // アナログ機材のような、ごくわずかな飽和（デジタルの硬さをやわらげる）
  const warmth = ctx.createWaveShaper();
  warmth.curve = distortionCurve(1.15);
  warmth.oversample = "2x";
  const comp = ctx.createDynamicsCompressor();
  high.connect(warmth);
  warmth.connect(comp);
  // 打楽器のアタックは通し、全体の厚みは詰める（現代的なゲーム音楽の「太くてパンチのある」音）
  comp.threshold.value = -10;
  comp.knee.value = 10;
  comp.ratio.value = 1.4;
  comp.attack.value = 0.03;
  comp.release.value = 0.16;
  // 左右の広がり（S-2）: 250Hz より上の「左右の差」（S=(L-R)/2）の成分だけを持ち上げる。低音（キック・ベース）は真ん中のまま、
  // 和音・弦・パッド・残響が左右に広がる。左右を足したモノラル再生では差の成分は消えるので、音は変わらない
  if (widen > 1 && typeof ctx.createChannelSplitter === "function") {
    const split = ctx.createChannelSplitter(2);
    const merge = ctx.createChannelMerger(2);
    const side = ctx.createGain(); // S = (L-R)/2
    side.gain.value = 0.5 * (widen - 1);
    const sideInv = ctx.createGain();
    sideInv.gain.value = -1;
    const sideHp = ctx.createBiquadFilter();
    sideHp.type = "highpass";
    sideHp.frequency.value = 250;
    comp.connect(split);
    split.connect(side, 0);
    split.connect(sideInv, 1);
    sideInv.connect(side);
    side.connect(sideHp);
    // 左 = 元の左 + 足した差、右 = 元の右 - 足した差
    const addL = ctx.createGain();
    const addR = ctx.createGain();
    addR.gain.value = -1;
    sideHp.connect(addL);
    sideHp.connect(addR);
    const outL = ctx.createGain();
    const outR = ctx.createGain();
    split.connect(outL, 0);
    split.connect(outR, 1);
    addL.connect(outL);
    addR.connect(outR);
    outL.connect(merge, 0, 0);
    outR.connect(merge, 0, 1);
    merge.connect(makeup);
  } else {
    comp.connect(makeup);
  }

  const bus = ctx.createGain();
  const dry = ctx.createGain();
  dry.gain.value = 0.85;
  bus.connect(dry);
  dry.connect(low);

  const seconds = reverbSec;
  const length = Math.floor(ctx.sampleRate * seconds);
  const impulse = ctx.createBuffer(2, length, ctx.sampleRate);
  let seed = 987;
  const preDelay = Math.floor(ctx.sampleRate * 0.03);
  for (let ch = 0; ch < 2; ch++) {
    const data = impulse.getChannelData(ch);
    let lp = 0;
    for (let i = preDelay; i < length; i++) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      // 尾の高音を少しずつ落として、自然な余韻にする
      const k = 0.55 - 0.4 * (i / length);
      lp += ((seed / 2147483648 - 1) - lp) * k;
      data[i] = lp * Math.pow(1 - (i - preDelay) / (length - preDelay), 2.6) * 2.2;
    }
  }
  const convolver = ctx.createConvolver();
  convolver.buffer = impulse;
  const wet = ctx.createGain();
  wet.gain.value = wetLevel;
  bus.connect(convolver);
  convolver.connect(wet);
  wet.connect(low);
  // 楽器ごとの送り量（S-4）: 低音・ドラムは残響を通さず、弦・パッド・ピアノは残響へ余分に送る
  const dryIn = ctx.createGain();
  dryIn.connect(dry);
  const wetIn = ctx.createGain();
  wetIn.connect(convolver);
  busSends.set(bus, { dryIn, wetIn });
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
      // 頭のカチッとした打撃感
      const click = filter(ctx, "highpass", 2800, pluckGain(ctx, dest, t, v * 0.5, 0.001, 0.012));
      out.push(noise(ctx, t, t + 0.03, click));
      break;
    }
    case "snare": {
      const hp = filter(ctx, "highpass", 1400, pluckGain(ctx, dest, t, v * 0.9, 0.002, 0.17));
      out.push(noise(ctx, t, t + 0.22, hp));
      out.push(osc(ctx, "triangle", 190, t, t + 0.14, pluckGain(ctx, dest, t, v * 0.5, 0.002, 0.09)));
      out.push(osc(ctx, "triangle", 330, t, t + 0.08, pluckGain(ctx, dest, t, v * 0.25, 0.002, 0.05)));
      break;
    }
    case "hihat": {
      const open = d > 0.3;
      const hp = filter(ctx, "highpass", 7500, pluckGain(ctx, dest, t, v * 0.5, 0.001, open ? 0.24 : 0.045));
      out.push(noise(ctx, t, t + (open ? 0.3 : 0.08), hp));
      break;
    }
    case "tom": {
      // タム: 音程が下がる太鼓（音の高さがそのまま太鼓の高さ）
      const g = pluckGain(ctx, dest, t, v * 1.1, 0.002, 0.3);
      const o = ctx.createOscillator();
      o.type = "sine";
      o.frequency.setValueAtTime(f * 1.6, t);
      o.frequency.exponentialRampToValueAtTime(f, t + 0.08);
      o.connect(g);
      o.start(t);
      o.stop(t + 0.36);
      out.push(o);
      break;
    }
    case "crash": {
      const hp = filter(ctx, "highpass", 5000, pluckGain(ctx, dest, t, v * 0.6, 0.003, 1.4));
      out.push(noise(ctx, t, t + 1.5, hp));
      break;
    }
    case "slap":
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
    case "brass":
    case "lead": {
      const guitar = e.instrument === "leadGuitar";
      const g = sustainGain(ctx, dest, t, d, v, 0.012, 0.09);
      const input = guitar ? distorted(ctx, g, 5, 4200) : filter(ctx, "lowpass", 5200, g);
      const stop = t + d + 0.1;
      const a = osc(ctx, guitar ? "sawtooth" : "square", f, t, stop, input, 0.6);
      const b = osc(ctx, "sawtooth", f, t, stop, input, 0.3, 9);
      // もう1本、逆側にずらして重ねる（現代的な厚みのある主旋律）
      const c = osc(ctx, "sawtooth", f, t, stop, input, 0.3, -9);
      // ビブラート（音程をゆらす）。音が伸びたところから、少しずつかかる
      const lfo = ctx.createOscillator();
      lfo.frequency.value = 5.4;
      const depth = ctx.createGain();
      depth.gain.setValueAtTime(0, t);
      depth.gain.linearRampToValueAtTime(guitar ? 22 : 14, t + Math.min(0.35, d));
      lfo.connect(depth);
      depth.connect(a.detune);
      depth.connect(b.detune);
      depth.connect(c.detune);
      lfo.start(t);
      lfo.stop(stop);
      out.push(a, b, c, lfo);
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
    case "choir":
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
    case "wind": {
      // 風: ノイズの帯域がゆっくり上下し、吹き始めと吹き終わりがなめらか
      const dur = Math.max(0.5, d);
      const bp = ctx.createBiquadFilter();
      bp.type = "bandpass";
      bp.Q.value = 0.9;
      bp.frequency.setValueAtTime(f, t);
      bp.frequency.linearRampToValueAtTime(f * 1.7, t + dur * 0.5);
      bp.frequency.linearRampToValueAtTime(f * 1.1, t + dur);
      bp.connect(sustainGain(ctx, dest, t, dur, v * 1.6, dur * 0.4, dur * 0.4));
      out.push(noise(ctx, t, t + dur * 1.4 + 0.1, bp));
      break;
    }
    case "rain": {
      const dur = Math.max(0.5, d);
      const hp = filter(ctx, "highpass", 2500, sustainGain(ctx, dest, t, dur, v * 0.9, 0.4, 0.5));
      const lp = filter(ctx, "lowpass", 9000, hp);
      out.push(noise(ctx, t, t + dur + 0.6, lp));
      break;
    }
    case "stream": {
      // せせらぎ: 2つの帯域を、速さの違うゆらぎ（LFO）で揺らす
      const dur = Math.max(0.5, d);
      const g = sustainGain(ctx, dest, t, dur, v, 0.5, 0.5);
      [[1100, 6.3, 380], [2300, 9.1, 700]].forEach(([center, rate, depth]) => {
        const bp = ctx.createBiquadFilter();
        bp.type = "bandpass";
        bp.Q.value = 2.2;
        bp.frequency.value = center;
        bp.connect(g);
        const lfo = ctx.createOscillator();
        lfo.frequency.value = rate;
        const amount = ctx.createGain();
        amount.gain.value = depth;
        lfo.connect(amount);
        amount.connect(bp.frequency);
        lfo.start(t);
        lfo.stop(t + dur + 0.6);
        out.push(noise(ctx, t, t + dur + 0.6, bp), lfo);
      });
      break;
    }
    case "bird": {
      // 小鳥: 短い上昇音を3つ、ゆるいリズムで
      [0, 0.13, 0.26].forEach((delay, n) => {
        const start = t + delay;
        const o = ctx.createOscillator();
        o.type = "sine";
        o.frequency.setValueAtTime(f * (n === 1 ? 1.25 : 1), start);
        o.frequency.exponentialRampToValueAtTime(f * (n === 2 ? 1.9 : 1.5), start + 0.09);
        o.connect(pluckGain(ctx, dest, start, v * 0.7, 0.005, 0.1));
        o.start(start);
        o.stop(start + 0.14);
        out.push(o);
      });
      break;
    }
    case "crickets": {
      // 虫の声: 高い音を、細かく断続させる
      const dur = Math.max(0.5, d);
      const g = ctx.createGain();
      g.gain.value = 0;
      const gate = ctx.createOscillator();
      gate.type = "square";
      gate.frequency.value = 14;
      const gateDepth = ctx.createGain();
      gateDepth.gain.value = v * 0.5;
      const offset = ctx.createConstantSource();
      offset.offset.value = v * 0.5;
      gate.connect(gateDepth);
      gateDepth.connect(g.gain);
      offset.connect(g.gain);
      const env = sustainGain(ctx, dest, t, dur, 1, 0.6, 0.6);
      g.connect(env);
      gate.start(t);
      offset.start(t);
      gate.stop(t + dur + 0.7);
      offset.stop(t + dur + 0.7);
      out.push(osc(ctx, "sine", f, t, t + dur + 0.7, g, 1), gate, offset);
      break;
    }
    case "pierce": {
      // 鋭く刺さる高音: 明るいノコギリ波が一気に下がり、金属的な共鳴が短く残る（ダメージ音の後ろにつく）
      const decay = Math.max(0.16, Math.min(d * 1.2, 0.5));
      const g = pluckGain(ctx, dest, t, v, 0.001, decay);
      const hp = filter(ctx, "highpass", 1400, g);
      const bp = filter(ctx, "bandpass", f * 1.25, hp, 4.5);
      const o = ctx.createOscillator();
      o.type = "sawtooth";
      o.frequency.setValueAtTime(f * 1.3, t);
      o.frequency.exponentialRampToValueAtTime(f, t + 0.05);
      o.connect(bp);
      o.start(t);
      o.stop(t + decay + 0.05);
      out.push(o);
      out.push(osc(ctx, "square", f * 2.01, t, t + 0.12, pluckGain(ctx, dest, t, v * 0.35, 0.001, 0.1)));
      break;
    }
    case "sub808": {
      // 808の低音: 頭で少し音程が下がり、長く伸びる。倍音を足すために軽く歪ませる
      const len = Math.max(0.2, d * 1.6);
      const g = sustainGain(ctx, dest, t, len, v, 0.004, Math.min(0.15, len * 0.4));
      const sh = ctx.createWaveShaper();
      sh.curve = distortionCurve(2.2);
      sh.connect(g);
      const o = ctx.createOscillator();
      o.type = "sine";
      o.frequency.setValueAtTime(f * 1.6, t);
      o.frequency.exponentialRampToValueAtTime(f, t + 0.06);
      o.connect(sh);
      o.start(t);
      o.stop(t + len + 0.2);
      out.push(o);
      break;
    }
    case "cowbell": {
      // カウベル: 少しずれた2つの四角波を、帯域を絞って短くはじく
      const g = pluckGain(ctx, dest, t, v, 0.002, Math.max(0.12, Math.min(d * 0.9, 0.35)));
      const bp = filter(ctx, "bandpass", f * 2.2, g, 1.6);
      const stop = t + 0.45;
      out.push(osc(ctx, "square", f, t, stop, bp, 0.6));
      out.push(osc(ctx, "square", f * 1.504, t, stop, bp, 0.6));
      break;
    }
    // ── 民族楽器（2026-10-02）。録音音源がない環境のための簡易な合成。刺さらないよう、どれも高域を丸める ──
    case "sitar":
    case "koto":
    case "shamisen":
    case "banjo":
    case "harp":
    case "kalimba": {
      const k = e.instrument as string;
      const ringy = k === "harp" || k === "kalimba" || k === "koto";
      const decay = Math.max(0.3, Math.min(d * (ringy ? 1.8 : 1.1), ringy ? 1.8 : 1.0));
      const g = pluckGain(ctx, dest, t, v, k === "shamisen" || k === "banjo" ? 0.001 : 0.003, decay);
      const bright = k === "sitar" ? 3600 : k === "shamisen" ? 3200 : k === "banjo" ? 3000 : k === "koto" ? 2600 : 2200;
      const lp = filter(ctx, "lowpass", bright, g);
      const stop = t + decay + 0.05;
      if (k === "kalimba") {
        out.push(osc(ctx, "sine", f, t, stop, lp, 0.8));
        out.push(osc(ctx, "sine", f * 5.4, t, t + 0.15, lp, 0.18));
      } else {
        out.push(osc(ctx, k === "harp" ? "triangle" : "sawtooth", f, t, stop, lp, 0.6));
        out.push(osc(ctx, "square", f * 2, t, stop, lp, k === "sitar" ? 0.35 : 0.18));
        // シタールの「ビヨーン」: 少しずれた共鳴弦
        if (k === "sitar") out.push(osc(ctx, "sawtooth", f * 1.5, t, stop, lp, 0.18, 7));
      }
      break;
    }
    case "panflute":
    case "shakuhachi":
    case "ocarina": {
      const k = e.instrument as string;
      const g = sustainGain(ctx, dest, t, d, v, k === "shakuhachi" ? 0.09 : 0.05, 0.12);
      const lp = filter(ctx, "lowpass", k === "ocarina" ? 2400 : 3400, g);
      const stop = t + d + 0.15;
      out.push(osc(ctx, "sine", f, t, stop, lp, 0.9));
      out.push(osc(ctx, "triangle", f * 2, t, stop, lp, k === "ocarina" ? 0.06 : 0.16));
      // 息の揺れ（ゆっくりしたビブラート）
      const lfo = ctx.createOscillator();
      lfo.frequency.value = k === "shakuhachi" ? 4.6 : 5.2;
      const depth = ctx.createGain();
      depth.gain.value = k === "shakuhachi" ? 12 : 7;
      lfo.connect(depth);
      for (const o of out.slice(-2)) if ("detune" in o) depth.connect((o as OscillatorNode).detune);
      lfo.start(t);
      lfo.stop(stop);
      out.push(lfo);
      break;
    }
    case "fiddle":
    case "bagpipe": {
      const pipe = e.instrument === "bagpipe";
      const g = sustainGain(ctx, dest, t, d, v, pipe ? 0.03 : 0.06, 0.1);
      const lp = filter(ctx, "lowpass", pipe ? 2200 : 2800, g);
      const stop = t + d + 0.12;
      out.push(osc(ctx, "sawtooth", f, t, stop, lp, 0.5, pipe ? 0 : -6));
      out.push(osc(ctx, "sawtooth", f, t, stop, lp, 0.4, pipe ? 3 : 6));
      if (pipe) out.push(osc(ctx, "square", f * 0.5, t, stop, lp, 0.18));
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

const ECHO_INSTRUMENTS = new Set(["lead", "leadGuitar", "cowbell", "bell", "keys"]);

/**
 * 楽器の指定がある音を予約する。指定がなければ空の配列を返す（呼び出し側が従来の音を鳴らす）。
 * 左右の位置（pan）と、主旋律向けの楽器のテンポに合わせたエコー（付点8分と付点4分）をここでかける。
 */
export function scheduleInstrumentNote(ctx: Ctx, destination: AudioNode, event: ScheduledNote, when: number): Source[] {
  if (!event.instrument) {
    return [];
  }
  const build = (target: AudioNode, ev: ScheduledNote, at: number, pan: number): Source[] => {
    let node = target;
    if (pan !== 0 && "createStereoPanner" in ctx) {
      const panner = ctx.createStereoPanner();
      panner.pan.value = Math.max(-1, Math.min(1, pan));
      panner.connect(target);
      node = panner;
    }
    return voice(ctx, node, ev, at);
  };
  const pan = event.pan ?? 0;
  // 残響の送り量を楽器ごとに変える。出口（createBgmBus）以外へつなぐときは従来どおり
  const sends = busSends.get(destination);
  let target = destination;
  if (sends && event.beatSec > 0) {
    if (DRY_INSTRUMENTS.has(event.instrument)) {
      target = sends.dryIn;
    } else if (WET_INSTRUMENTS.has(event.instrument)) {
      const tee = ctx.createGain();
      const extra = ctx.createGain();
      extra.gain.value = EXTRA_WET_SEND;
      tee.connect(destination);
      tee.connect(extra);
      extra.connect(sends.wetIn);
      target = tee;
    }
  }
  const out = build(target, event, when, pan);
  // 曲（ループするBGM）の主旋律だけにエコーをかける。効果音（1回きり）にはかけない
  if (event.beatSec > 0 && ECHO_INSTRUMENTS.has(event.instrument) && event.durationSec >= event.beatSec * 0.4) {
    const echoes: [number, number, number][] = [[0.75, 0.3, 0.45], [1.5, 0.13, -0.45]];
    for (const [beats, gain, side] of echoes) {
      out.push(...build(destination, { ...event, volume: event.volume * gain, durationSec: Math.min(event.durationSec, event.beatSec) }, when + beats * event.beatSec, pan * 0.5 + side));
    }
  }
  return out;
}

/** PS2世代のゲーム機にあった「ホール」の残響のような、密で長い響き（約2.8秒、少し暗い）。 */
export function createHallImpulse(ctx: Ctx): AudioBuffer {
  const seconds = 2.8;
  const length = Math.floor(ctx.sampleRate * seconds);
  const impulse = ctx.createBuffer(2, length, ctx.sampleRate);
  const preDelay = Math.floor(ctx.sampleRate * 0.03);
  let seed = 4242;
  for (let ch = 0; ch < 2; ch++) {
    const data = impulse.getChannelData(ch);
    let lp = 0;
    for (let i = preDelay; i < length; i++) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      const k = 0.5 - 0.42 * (i / length);
      lp += ((seed / 2147483648 - 1) - lp) * k;
      data[i] = lp * Math.pow(1 - (i - preDelay) / (length - preDelay), 1.9) * 2.4;
    }
  }
  return impulse;
}
