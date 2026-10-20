/**
 * エフェクター（トラックごとの「足し算の音づくり」）。アンプのあとに、書いた順につながる。
 * Web Audio の部品だけで作る（作曲ソフトでも、ゲームでも、書き出し＝オフラインでも同じ音になる）。
 * どれも `mix`（0〜1）で、元の音との混ぜ具合を決める。省略すると、その効果の標準の量。
 */

import { EXTRA_FX_INFO, EXTRA_FX_TYPES, buildExtraFx } from "./fx-extra";

export const FX_TYPES = [
  "delay", "pingpong", "reverb", "plate", "spring", "room",
  "chorus", "flanger", "phaser", "tremolo", "vibrato", "wah", "autowah",
  "compressor", "eq", "boost", "tubescreamer", "fuzz", "bitcrusher", "ringmod", "filter", "widen",
  // 2026-10-14 追加（fx-extra.ts）
  ...EXTRA_FX_TYPES,
] as const;
export type FxType = (typeof FX_TYPES)[number];

export interface FxSpec {
  type: FxType;
  /** 元の音との混ぜ具合 0〜1（効果の種類ごとの標準がある）。 */
  mix?: number;
  /** delay／pingpong: 間隔（ミリ秒。`beats` を書けばテンポから計算）。 */
  ms?: number;
  /** delay／pingpong: くり返し（0〜0.9）。 */
  feedback?: number;
  /** chorus／flanger／phaser／tremolo／vibrato／autowah: ゆれの速さ（Hz）。 */
  rate?: number;
  /** ゆれの深さ 0〜1（tremolo は音量のゆれ、ほかは音程・位相のゆれ）。 */
  depth?: number;
  /** wah／filter: 中心の周波数（Hz）。 */
  freq?: number;
  /** wah／filter: 鋭さ。 */
  q?: number;
  /** boost／tubescreamer／fuzz: 入力の増幅（dB）。 */
  gain?: number;
  /** tubescreamer／fuzz／boost: 出力の大きさ（dB）。 */
  level?: number;
  /** eq: 低音・中音・高音（dB）と、中音の周波数。 */
  low?: number;
  mid?: number;
  midHz?: number;
  high?: number;
  /** compressor: しきい値（dB）と圧縮の比。 */
  threshold?: number;
  ratio?: number;
  /** bitcrusher: ビット数（2〜12）。 */
  bits?: number;
  /** cabir: 録音のキャビネットIRの名前（作曲ソフトに登録されたもの。例 "dfc-ampmix"）。省略は近似の箱。 */
  ir?: string;
  /** filter: "lowpass" | "highpass" | "bandpass"。 */
  kind?: "lowpass" | "highpass" | "bandpass";
  /** transgate: 切る形（x＝鳴る・.＝切る。1文字＝beats 拍）。 */
  pattern?: string;
  /** compressor／pcomp: 反応の速さ・戻りの速さ（秒）。省略は compressor が 0.012／0.2、pcomp が 0.005／0.12。 */
  attack?: number;
  release?: number;
  /** true なら、アンプの「前」につなぐ（ペダルボードの本来の位置。歪み・ブースター・コンプ・ワウ・ファズ向き）。省略はアンプのあと。 */
  pre?: boolean;
  /** reverb系: 響きの長さの倍率（0.3〜3）。 */
  size?: number;
  /** delay系・reverb系: 響きの高音の丸め（Hz。小さいほど暗い）。 */
  tone?: number;
}

/** 日本語の呼び名と、向く場面。 */
export const FX_INFO: Record<FxType, { label: string; use: string; mix: number }> = {
  delay: { label: "ディレイ", use: "やまびこ。メロディに奥行き", mix: 0.25 },
  pingpong: { label: "ピンポンディレイ", use: "左右に跳ねるやまびこ", mix: 0.25 },
  reverb: { label: "ホール", use: "広い空間の残響", mix: 0.2 },
  plate: { label: "プレート", use: "明るく密な残響（ボーカル・スネア向け）", mix: 0.2 },
  spring: { label: "スプリング", use: "ビヨンと鳴るギターアンプの残響", mix: 0.2 },
  room: { label: "ルーム", use: "小さな部屋の自然な響き（ドラム向け）", mix: 0.15 },
  chorus: { label: "コーラス", use: "音を厚く広げる（クリーンのギターには不向き）", mix: 0.4 },
  flanger: { label: "フランジャー", use: "ジェット機のような うねり", mix: 0.5 },
  phaser: { label: "フェイザー", use: "ゆるやかに回る うねり", mix: 0.5 },
  tremolo: { label: "トレモロ", use: "音量が震える", mix: 1 },
  vibrato: { label: "ビブラート", use: "音程が震える", mix: 1 },
  wah: { label: "ワウ", use: "「ワウワウ」と口を開け閉めする音（固定位置）", mix: 1 },
  autowah: { label: "オートワウ", use: "自動で動くワウ（ファンク）", mix: 1 },
  compressor: { label: "コンプレッサー", use: "音量をそろえて粘らせる", mix: 1 },
  eq: { label: "イコライザー", use: "低音・中音・高音の調整", mix: 1 },
  boost: { label: "ブースター", use: "きれいに音量を上げる", mix: 1 },
  tubescreamer: { label: "オーバードライブ（ペダル）", use: "中域が前に出る定番の浅い歪み", mix: 1 },
  fuzz: { label: "ファズ", use: "もこもこ荒い歪み", mix: 1 },
  bitcrusher: { label: "ビットクラッシャー", use: "ざらざらした粗い音", mix: 0.5 },
  ringmod: { label: "リングモジュレーター", use: "金属的な変な音（効果音向け）", mix: 0.4 },
  filter: { label: "フィルター", use: "高音や低音を削る", mix: 1 },
  widen: { label: "ステレオ広げ", use: "左右に少しずらして広げる", mix: 0.5 },
  ...EXTRA_FX_INFO,
};

export interface BuiltFx {
  input: AudioNode;
  output: AudioNode;
  /** 切りはなすとき止める・外す部品（発振器を含む）。 */
  nodes: AudioNode[];
}

const clamp = (x: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, x));
const num = (x: unknown, def: number): number => (typeof x === "number" && Number.isFinite(x) ? x : def);
const dbToGain = (db: number): number => Math.pow(10, db / 20);

/** 残響のインパルス応答（ノイズが指数で減る。種類ごとに長さ・立ち上がり・高音の減り方を変える）。 */
export function makeReverbImpulse(ctx: BaseAudioContext, kind: "reverb" | "plate" | "spring" | "room", size = 1, toneHz = 0): AudioBuffer {
  const sr = ctx.sampleRate;
  const base = { reverb: 2.2, plate: 1.5, spring: 0.9, room: 0.5 }[kind] * clamp(size, 0.3, 3);
  const len = Math.floor(sr * base);
  const buf = ctx.createBuffer(2, len, sr);
  const damp = toneHz > 0 ? clamp(toneHz / (sr / 2), 0.02, 0.98) : { reverb: 0.35, plate: 0.8, spring: 0.25, room: 0.4 }[kind];
  for (let ch = 0; ch < 2; ch++) {
    const d = buf.getChannelData(ch);
    let seed = 12345 + ch * 777 + kind.length * 31;
    const rnd = (): number => {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      return seed / 4294967296 - 0.5;
    };
    let lp = 0;
    for (let i = 0; i < len; i++) {
      const t = i / len;
      let env = Math.pow(1 - t, kind === "plate" ? 2.2 : 3);
      // 初期反射の山（部屋・ホール）／スプリングの「ビヨン」（短い周期のうねり）
      if (kind === "spring") env *= 0.6 + 0.4 * Math.sin((i / sr) * 2 * Math.PI * 38) * Math.sin((i / sr) * 2 * Math.PI * 7);
      if (kind === "room" && i < sr * 0.03) env *= 1.6;
      lp += (rnd() * 2 - lp) * damp;
      d[i] = lp * env * (i < 64 ? i / 64 : 1);
    }
  }
  return buf;
}

/** ゆれ（LFO）: 発振器 → 深さの増幅 → 目的の項目。 */
function lfo(ctx: BaseAudioContext, rate: number, depth: number, target: AudioParam, nodes: AudioNode[], type: OscillatorType = "sine"): void {
  const osc = ctx.createOscillator();
  osc.type = type;
  osc.frequency.value = rate;
  const g = ctx.createGain();
  g.gain.value = depth;
  osc.connect(g);
  g.connect(target);
  osc.start();
  nodes.push(osc, g);
}

function curveSoft(drive: number, size = 2048): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size) as Float32Array<ArrayBuffer>;
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.tanh(x * drive) / Math.tanh(drive);
  }
  return c;
}
function curveFuzz(size = 2048): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size) as Float32Array<ArrayBuffer>;
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    // 上下で違うクリップ（正側は硬く、負側はやわらかく）
    c[i] = x >= 0 ? Math.min(1, x * 6) * 0.9 : -Math.tanh(-x * 4) * 0.8;
  }
  return c;
}
function curveBits(bits: number, size = 4096): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size) as Float32Array<ArrayBuffer>;
  const steps = Math.pow(2, clamp(Math.round(bits), 2, 12));
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.round(x * (steps / 2)) / (steps / 2);
  }
  return c;
}

/** 元の音（dry）と効果（wet）を混ぜる枠。 */
function wetDry(ctx: BaseAudioContext, mix: number, nodes: AudioNode[]): { input: GainNode; dry: GainNode; wet: GainNode; output: GainNode } {
  const input = ctx.createGain();
  const output = ctx.createGain();
  const dry = ctx.createGain();
  const wet = ctx.createGain();
  dry.gain.value = 1 - mix * 0.5; // 完全に消さない（音量が痩せないように、半分だけ引く）
  wet.gain.value = mix;
  input.connect(dry);
  dry.connect(output);
  wet.connect(output);
  nodes.push(input, output, dry, wet);
  return { input, dry, wet, output };
}

/** 効果を1つ作る。 */
export function buildFx(ctx: BaseAudioContext, spec: FxSpec): BuiltFx {
  const nodes: AudioNode[] = [];
  const mix = clamp(num(spec.mix, FX_INFO[spec.type]?.mix ?? 0.3), 0, 1);
  const filt = (type: BiquadFilterType, f: number, g = 0, q = 0.7): BiquadFilterNode => {
    const b = ctx.createBiquadFilter();
    b.type = type;
    b.frequency.value = f;
    b.gain.value = g;
    b.Q.value = q;
    nodes.push(b);
    return b;
  };
  const gain = (v: number): GainNode => {
    const g = ctx.createGain();
    g.gain.value = v;
    nodes.push(g);
    return g;
  };
  const inline = (chain: AudioNode[]): BuiltFx => {
    // 直列の効果（歪み・EQ など）: mix で元の音と混ぜる
    const m = wetDry(ctx, mix >= 1 ? 1 : mix, nodes);
    m.dry.gain.value = 1 - mix;
    let prev: AudioNode = m.input;
    for (const n of chain) {
      prev.connect(n);
      prev = n;
    }
    prev.connect(m.wet);
    return { input: m.input, output: m.output, nodes };
  };

  switch (spec.type) {
    case "delay": {
      const m = wetDry(ctx, mix, nodes);
      const d = ctx.createDelay(2);
      d.delayTime.value = clamp(num(spec.ms, 375), 20, 1900) / 1000;
      const fb = gain(clamp(num(spec.feedback, 0.35), 0, 0.9));
      const tone = filt("lowpass", num(spec.tone, 3500));
      nodes.push(d);
      m.input.connect(d);
      d.connect(tone);
      tone.connect(fb);
      fb.connect(d);
      tone.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    case "pingpong": {
      const m = wetDry(ctx, mix, nodes);
      const t = clamp(num(spec.ms, 375), 20, 1900) / 1000;
      const dl = ctx.createDelay(2);
      const dr = ctx.createDelay(2);
      dl.delayTime.value = t;
      dr.delayTime.value = t;
      const fb = gain(clamp(num(spec.feedback, 0.4), 0, 0.9));
      const tone = filt("lowpass", num(spec.tone, 3500));
      const pl = ctx.createStereoPanner();
      const pr = ctx.createStereoPanner();
      pl.pan.value = -0.8;
      pr.pan.value = 0.8;
      nodes.push(dl, dr, pl, pr);
      m.input.connect(dl);
      dl.connect(pl);
      pl.connect(m.wet);
      dl.connect(tone);
      tone.connect(dr);
      dr.connect(pr);
      pr.connect(m.wet);
      dr.connect(fb);
      fb.connect(dl);
      return { input: m.input, output: m.output, nodes };
    }
    case "reverb":
    case "plate":
    case "spring":
    case "room": {
      const m = wetDry(ctx, mix, nodes);
      const conv = ctx.createConvolver();
      conv.buffer = makeReverbImpulse(ctx, spec.type, num(spec.size, 1), num(spec.tone, 0));
      nodes.push(conv);
      m.input.connect(conv);
      conv.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    case "chorus": {
      const m = wetDry(ctx, mix, nodes);
      const d = ctx.createDelay(0.1);
      d.delayTime.value = 0.022;
      nodes.push(d);
      lfo(ctx, clamp(num(spec.rate, 0.8), 0.05, 8), 0.0035 * clamp(num(spec.depth, 0.6), 0, 1) * 1.5, d.delayTime, nodes);
      m.input.connect(d);
      d.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    case "flanger": {
      const m = wetDry(ctx, mix, nodes);
      const d = ctx.createDelay(0.05);
      d.delayTime.value = 0.004;
      const fb = gain(0.55);
      nodes.push(d);
      lfo(ctx, clamp(num(spec.rate, 0.3), 0.05, 5), 0.003 * clamp(num(spec.depth, 0.7), 0, 1), d.delayTime, nodes);
      m.input.connect(d);
      d.connect(fb);
      fb.connect(d);
      d.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    case "phaser": {
      const m = wetDry(ctx, mix, nodes);
      let prev: AudioNode = m.input;
      const depth = clamp(num(spec.depth, 0.7), 0, 1);
      for (let i = 0; i < 4; i++) {
        const a = filt("allpass", 600 + i * 350, 0, 0.7);
        lfo(ctx, clamp(num(spec.rate, 0.4), 0.05, 6), 500 * depth * (1 + i * 0.4), a.frequency, nodes);
        prev.connect(a);
        prev = a;
      }
      prev.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    case "tremolo": {
      const depth = clamp(num(spec.depth, 0.5), 0, 1);
      const g = gain(1 - depth / 2);
      lfo(ctx, clamp(num(spec.rate, 5), 0.1, 20), depth / 2, g.gain, nodes);
      return { input: g, output: g, nodes };
    }
    case "vibrato": {
      const d = ctx.createDelay(0.05);
      d.delayTime.value = 0.006;
      nodes.push(d);
      lfo(ctx, clamp(num(spec.rate, 5.5), 0.5, 10), 0.0025 * clamp(num(spec.depth, 0.4), 0, 1), d.delayTime, nodes);
      return { input: d, output: d, nodes };
    }
    case "wah": {
      const f = filt("bandpass", clamp(num(spec.freq, 900), 250, 2800), 0, clamp(num(spec.q, 5), 0.5, 12));
      const m = wetDry(ctx, mix, nodes);
      m.input.connect(f);
      f.connect(m.wet);
      m.wet.gain.value = mix * 2.2;
      return { input: m.input, output: m.output, nodes };
    }
    case "autowah": {
      const f = filt("bandpass", 900, 0, clamp(num(spec.q, 4), 0.5, 12));
      lfo(ctx, clamp(num(spec.rate, 1.6), 0.1, 10), 650 * clamp(num(spec.depth, 0.8), 0, 1), f.frequency, nodes);
      const m = wetDry(ctx, mix, nodes);
      m.input.connect(f);
      f.connect(m.wet);
      m.wet.gain.value = mix * 2.2;
      return { input: m.input, output: m.output, nodes };
    }
    case "compressor": {
      const c = ctx.createDynamicsCompressor();
      c.threshold.value = clamp(num(spec.threshold, -24), -60, 0);
      c.ratio.value = clamp(num(spec.ratio, 4), 1, 20);
      c.attack.value = clamp(num(spec.attack, 0.012), 0.0005, 0.2);
      c.release.value = clamp(num(spec.release, 0.2), 0.02, 1);
      c.knee.value = 12;
      nodes.push(c);
      const makeup = gain(dbToGain(clamp(-num(spec.threshold, -24) * 0.25, 0, 12)));
      c.connect(makeup);
      return { input: c, output: makeup, nodes };
    }
    case "eq": {
      const lo = filt("lowshelf", 150, clamp(num(spec.low, 0), -15, 15));
      const mi = filt("peaking", clamp(num(spec.midHz, 1000), 200, 6000), clamp(num(spec.mid, 0), -15, 15), 0.9);
      const hi = filt("highshelf", 4500, clamp(num(spec.high, 0), -15, 15));
      lo.connect(mi);
      mi.connect(hi);
      return { input: lo, output: hi, nodes };
    }
    case "boost": {
      const g = gain(dbToGain(clamp(num(spec.gain, 6), -12, 24) + clamp(num(spec.level, 0), -12, 12)));
      return { input: g, output: g, nodes };
    }
    case "tubescreamer": {
      // 低音を削って（720Hz付近より下）→ 増幅 → やわらかく歪ませ → 高音を丸める → 音量
      const sh = ctx.createWaveShaper();
      sh.curve = curveSoft(2.2 + clamp(num(spec.gain, 12), 0, 30) / 8);
      sh.oversample = "4x";
      nodes.push(sh);
      return inline([filt("highpass", 700, 0, 0.7), filt("peaking", 900, 3, 0.8), gain(dbToGain(clamp(num(spec.gain, 12), 0, 30))), sh, filt("lowpass", num(spec.tone, 4200)), gain(dbToGain(clamp(num(spec.level, -10), -24, 6)))]);
    }
    case "fuzz": {
      const sh = ctx.createWaveShaper();
      sh.curve = curveFuzz();
      sh.oversample = "4x";
      nodes.push(sh);
      return inline([filt("highpass", 90), gain(dbToGain(clamp(num(spec.gain, 18), 0, 36))), sh, filt("lowpass", num(spec.tone, 4800)), gain(dbToGain(clamp(num(spec.level, -12), -30, 6)))]);
    }
    case "bitcrusher": {
      const sh = ctx.createWaveShaper();
      sh.curve = curveBits(num(spec.bits, 6));
      nodes.push(sh);
      return inline([sh]);
    }
    case "ringmod": {
      const g = gain(0);
      const osc = ctx.createOscillator();
      osc.frequency.value = clamp(num(spec.freq, 300), 20, 3000);
      osc.connect(g.gain);
      osc.start();
      nodes.push(osc);
      return inline([g]);
    }
    case "filter": {
      const kind = spec.kind === "highpass" || spec.kind === "bandpass" ? spec.kind : "lowpass";
      const f = filt(kind, clamp(num(spec.freq, 3000), 40, 16000), 0, clamp(num(spec.q, 0.9), 0.3, 12));
      return { input: f, output: f, nodes };
    }
    case "widen": {
      // 片方をほんの少し遅らせて、左右の広がりを作る（モノラルで聴いても音が痩せにくい程度に短く）
      const m = wetDry(ctx, mix, nodes);
      const d = ctx.createDelay(0.05);
      d.delayTime.value = 0.017;
      const p = ctx.createStereoPanner();
      p.pan.value = 0.7;
      nodes.push(d, p);
      m.input.connect(d);
      d.connect(p);
      p.connect(m.wet);
      return { input: m.input, output: m.output, nodes };
    }
    default: {
      const extra = buildExtraFx(ctx, spec, FX_INFO[spec.type]?.mix ?? 0.3);
      if (extra) return extra;
      const g = gain(1);
      return { input: g, output: g, nodes };
    }
  }
}

/** 効果の並びを直列につなぐ。 */
export function buildFxChain(ctx: BaseAudioContext, specs: FxSpec[]): BuiltFx | null {
  const list = specs.filter((s) => s && (FX_TYPES as readonly string[]).includes(s.type));
  if (list.length === 0) return null;
  const built = list.map((s) => buildFx(ctx, s));
  for (let i = 0; i + 1 < built.length; i++) built[i].output.connect(built[i + 1].input);
  return { input: built[0].input, output: built[built.length - 1].output, nodes: built.flatMap((b) => b.nodes) };
}
