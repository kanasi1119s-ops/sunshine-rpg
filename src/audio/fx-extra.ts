/**
 * 追加のエフェクター（2026-10-14 ペダルボード調査の実装。調査: docs/sound/band-ensemble/pedalboard-signal-chain.md の §13・§14）。
 * Web Audio の部品だけで作る（作曲ソフトでも、ゲームでも、書き出し＝オフラインでも同じ音になる）。外部の音声ファイルは使わない。
 *
 * 種類: tape（テープディレイ）／rotary（ロータリースピーカー）／doubler（ステレオ・ダブラー）／pcomp（パラレル・コンプ）／
 *       harmtrem（ハーモニック・トレモロ）／octup（オクターブ・アップ）／cabir（キャビネットIR近似）／springx（ドリップ付きスプリング）／
 *       envwah（エンベロープ・フィルター。弾く強さで開く本物のオートワウ。既存の autowah は一定の速さで動く LFO 式）
 *
 * fx-chain.ts の buildFx から呼ばれる（fx-chain.ts を実行時に読み込まない＝循環を作らない）。
 * 耳での確認は利用者が行う（作者は音を聴けない）。音の性格の数字は「仮」。波形やスペクトルの測定は pedalboard-signal-chain.md §14 にある。
 */

import { cabApproxSpec, type CabKind, type MicPos } from "./amp-cab";
import type { BuiltFx, FxSpec } from "./fx-chain";

export const EXTRA_FX_TYPES = ["tape", "rotary", "doubler", "pcomp", "harmtrem", "octup", "cabir", "springx", "envwah"] as const;
export type ExtraFxType = (typeof EXTRA_FX_TYPES)[number];

/** 日本語の呼び名と、向く場面と、標準の混ぜ具合（fx-chain.ts の FX_INFO に足される）。 */
export const EXTRA_FX_INFO: Record<ExtraFxType, { label: string; use: string; mix: number }> = {
  tape: { label: "テープディレイ", use: "くり返しが少しずつ暗くなり、ゆれる。やさしい残響のやまびこ", mix: 0.28 },
  rotary: { label: "ロータリー", use: "回るスピーカーのうねり（クリーン・オルガン風のギター）", mix: 0.85 },
  doubler: { label: "ステレオ・ダブラー", use: "1本のギターを左右に二重にして広げる（モノラルでも痩せにくい）", mix: 0.8 },
  pcomp: { label: "パラレルコンプ", use: "強く潰した音を足して、粒をそろえて太くする（クリーン・ファンク）。足した分だけ音量が上がる", mix: 0.35 },
  harmtrem: { label: "ハーモニックトレモロ", use: "低音と高音が交互に震える、やわらかいトレモロ（サーフ・古いクリーン）", mix: 1 },
  octup: { label: "オクターブアップ", use: "1オクターブ上の音を足す（単音のリード向き。和音では濁る）", mix: 0.4 },
  cabir: { label: "キャビネットIR", use: "スピーカーの箱とマイクの癖を足す（アンプ前の歪みペダルだけの音を仕上げる）", mix: 1 },
  springx: { label: "スプリング（ドリップ）", use: "ビヨンと鳴る本物らしい金属ばねの残響", mix: 0.22 },
  envwah: { label: "エンベロープ・フィルター", use: "強く弾くほどフィルターが開く「ニャウ」（ファンクのカッティング・ベース）。コンプより前に置く", mix: 1 },
};

const clamp = (x: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, x));
const num = (x: unknown, def: number): number => (typeof x === "number" && Number.isFinite(x) ? x : def);
const dbToGain = (db: number): number => Math.pow(10, db / 20);

// ───────────────────────── 純粋な関数（Web Audio に依存しない。テストできる） ─────────────────────────

/** スプリングの「ビヨン」: 1つのばねのインパルス応答（モノラル）。往復 roundTrip 秒ごとに、高→低へ滑る音（チャープ）が戻ってくる。 */
export function springImpulse(sampleRate: number, opts: { roundTrip?: number; seconds?: number; seed?: number; decay?: number } = {}): Float32Array {
  const T = opts.roundTrip ?? 0.034;
  const seconds = opts.seconds ?? 1.6;
  const decay = opts.decay ?? 0.7;
  const len = Math.floor(sampleRate * seconds);
  const out = new Float32Array(len);
  let seed = (opts.seed ?? 4242) >>> 0;
  const rnd = (): number => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296 - 0.5;
  };
  const echoes = Math.min(40, Math.floor(seconds / T));
  for (let k = 0; k < echoes; k++) {
    const start = Math.floor((T * (k + 1)) * sampleRate);
    const amp = Math.pow(decay, k);
    if (amp < 0.01) break;
    // 戻りが重なるほど、チャープは長く・なだらかに広がる（高音から先に着く）
    const dur = (0.012 + 0.006 * Math.sqrt(k + 1)) * sampleRate;
    const f0 = 4200 / (1 + 0.15 * k);
    const f1 = 320;
    let phase = 0;
    for (let i = 0; i < dur && start + i < len; i++) {
      const u = i / dur;
      const f = f0 * Math.pow(f1 / f0, u);
      phase += (2 * Math.PI * f) / sampleRate;
      const env = Math.sin(Math.PI * Math.min(1, u)) * (1 - u * 0.2);
      out[start + i] += Math.sin(phase) * env * amp * 0.5;
    }
  }
  // 細かいにじみ（ばねのからみ）: 高音を落とした薄いノイズの尾
  let lp = 0;
  for (let i = 0; i < len; i++) {
    const t = i / sampleRate;
    lp += (rnd() * 2 - lp) * 0.12;
    out[i] += lp * Math.exp(-t / 0.35) * 0.16 * (i < 64 ? i / 64 : 1);
  }
  return out;
}

/** バイクアッドの係数（RBJ のクックブックの式）。highpass・lowpass・peaking だけ。 */
export function biquadCoefficients(type: "highpass" | "lowpass" | "peaking", freq: number, gainDb: number, q: number, sampleRate: number): { b0: number; b1: number; b2: number; a1: number; a2: number } {
  const w0 = (2 * Math.PI * clamp(freq, 10, sampleRate * 0.45)) / sampleRate;
  const cos = Math.cos(w0);
  const sin = Math.sin(w0);
  const alpha = sin / (2 * Math.max(0.05, q));
  let b0: number, b1: number, b2: number, a0: number, a1: number, a2: number;
  if (type === "highpass") {
    b0 = (1 + cos) / 2; b1 = -(1 + cos); b2 = (1 + cos) / 2; a0 = 1 + alpha; a1 = -2 * cos; a2 = 1 - alpha;
  } else if (type === "lowpass") {
    b0 = (1 - cos) / 2; b1 = 1 - cos; b2 = (1 - cos) / 2; a0 = 1 + alpha; a1 = -2 * cos; a2 = 1 - alpha;
  } else {
    const A = Math.pow(10, gainDb / 40);
    b0 = 1 + alpha * A; b1 = -2 * cos; b2 = 1 - alpha * A; a0 = 1 + alpha / A; a1 = -2 * cos; a2 = 1 - alpha / A;
  }
  return { b0: b0 / a0, b1: b1 / a0, b2: b2 / a0, a1: a1 / a0, a2: a2 / a0 };
}

/** ある周波数での大きさ（インパルス応答を離散フーリエ変換して1点だけ見る）。 */
export function magnitudeAt(ir: Float32Array, freq: number, sampleRate: number): number {
  let re = 0;
  let im = 0;
  const w = (2 * Math.PI * freq) / sampleRate;
  for (let n = 0; n < ir.length; n++) {
    re += ir[n] * Math.cos(w * n);
    im -= ir[n] * Math.sin(w * n);
  }
  return Math.hypot(re, im);
}

/**
 * キャビネットのインパルス応答（モノラル）。amp-cab.ts のフィルターの並び（cabApproxSpec）を直列に通した応答に、マイク位置による癖を足す:
 *  off＝斜めのマイク（わずかな遅れの反射 → 2kHz 前後に浅い谷）／far＝遠いマイク（部屋の初期反射を3つ）。center・edge は足さない。
 * 最後に 1kHz の大きさが 1 になるようにそろえる（音量が変わらないように）。【推測】反射の数字は仮。
 */
export function cabImpulse(sampleRate: number, kind: CabKind = "closed", mic: MicPos = "center", length = 2048): Float32Array {
  let ir = new Float32Array(length);
  ir[0] = 1;
  for (const f of cabApproxSpec(kind, mic)) {
    const c = biquadCoefficients(f.type, f.freq, f.gain, f.q, sampleRate);
    const out = new Float32Array(length);
    let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    for (let n = 0; n < length; n++) {
      const x = ir[n];
      const y = c.b0 * x + c.b1 * x1 + c.b2 * x2 - c.a1 * y1 - c.a2 * y2;
      x2 = x1; x1 = x; y2 = y1; y1 = y;
      out[n] = y;
    }
    ir = out;
  }
  const taps: [number, number][] = mic === "off" ? [[0.00025, 0.35]] : mic === "far" ? [[0.0021, 0.18], [0.0037, 0.12], [0.0062, 0.08]] : [];
  if (taps.length) {
    const mixed = new Float32Array(length);
    mixed.set(ir);
    for (const [sec, g] of taps) {
      const d = Math.round(sec * sampleRate);
      for (let n = 0; n + d < length; n++) mixed[n + d] += ir[n] * g;
    }
    ir = mixed;
  }
  const m = magnitudeAt(ir, 1000, sampleRate);
  if (m > 1e-6) for (let n = 0; n < length; n++) ir[n] /= m;
  return ir;
}

// ───────────── 録音のキャビネットIR（2026-10-15） ─────────────
// 本物のスピーカーの箱をマイクで録った応答（docs/assets-credits.md で規約を確かめたもの）。データは作曲ソフトの側
// （tools/composer/cab-irs.ts）から registerCabIr で登録する。ゲーム本体には入れない（登録されていなければ近似の箱に戻る）。
const RECORDED_IRS = new Map<string, { data: Float32Array; rate: number }>();
/** 録音のキャビネットIRを名前で登録する（data はモノラル）。 */
export function registerCabIr(name: string, data: Float32Array, rate: number): void {
  RECORDED_IRS.set(name, { data, rate });
}
/** 登録ずみの録音IRの名前の一覧。 */
export function recordedCabIrNames(): string[] {
  return [...RECORDED_IRS.keys()];
}
/** 録音IRを、出力のサンプルレートに直し（線形補間）、1kHz の大きさが 1 になるようにそろえて返す。なければ null。 */
export function recordedCabImpulse(name: string, sampleRate: number): Float32Array | null {
  // "a+b"（＋c…）: 2本のマイクを混ぜるように、それぞれをそろえてから平均する（2026-10-20 ラウドロック）
  if (name.includes("+")) {
    const list = name.split("+").map((n) => recordedCabImpulse(n.trim(), sampleRate)).filter((x): x is Float32Array => x !== null);
    if (!list.length) return null;
    const len = Math.max(...list.map((x) => x.length));
    const mix = new Float32Array(len);
    for (const x of list) for (let n = 0; n < x.length; n++) mix[n] += x[n] / list.length;
    const mm = magnitudeAt(mix, 1000, sampleRate);
    if (mm > 1e-6) for (let n = 0; n < len; n++) mix[n] /= mm;
    return mix;
  }
  const r = RECORDED_IRS.get(name);
  if (!r) return null;
  const ratio = r.rate / sampleRate;
  const len = Math.max(1, Math.floor(r.data.length / ratio));
  const out = new Float32Array(len);
  for (let n = 0; n < len; n++) {
    const x = n * ratio, i = Math.floor(x), f = x - i;
    out[n] = (r.data[i] ?? 0) * (1 - f) + (r.data[i + 1] ?? 0) * f;
  }
  const m = magnitudeAt(out, 1000, sampleRate);
  if (m > 1e-6) for (let n = 0; n < len; n++) out[n] /= m;
  return out;
}

/** 全波整流（|x|）の曲線。オクターブアップ（Octavia 系）の中身。 */
export function rectifierCurve(size = 2048, preGain = 3): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size) as Float32Array<ArrayBuffer>;
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.abs(Math.tanh(x * preGain));
  }
  return c;
}

/** 磁気テープのやわらかい飽和（入れた音が大きいほど、少しだけ丸まる）。 */
export function tapeSaturationCurve(size = 2048, drive = 1.4): Float32Array<ArrayBuffer> {
  const c = new Float32Array(size) as Float32Array<ArrayBuffer>;
  // 小さい音の傾きを 1 にそろえる（くり返しの道に入れるので、傾きが 1 を超えると、くり返しが減らずに増えてしまう。2026-10-14 実測で確認）
  for (let i = 0; i < size; i++) {
    const x = (i / (size - 1)) * 2 - 1;
    c[i] = Math.tanh(x * drive) / drive;
  }
  return c;
}

// ───────────────────────── Web Audio の部品 ─────────────────────────

/** 追加のエフェクターを1つ作る。知らない種類は null。 */
export function buildExtraFx(ctx: BaseAudioContext, spec: FxSpec, mixDefault: number): BuiltFx | null {
  const type = spec.type as string;
  if (!(EXTRA_FX_TYPES as readonly string[]).includes(type)) return null;
  const nodes: AudioNode[] = [];
  const mix = clamp(num(spec.mix, mixDefault), 0, 1);

  const gain = (v: number): GainNode => {
    const g = ctx.createGain();
    g.gain.value = v;
    nodes.push(g);
    return g;
  };
  const filt = (t: BiquadFilterType, f: number, g = 0, q = 0.7): BiquadFilterNode => {
    const b = ctx.createBiquadFilter();
    b.type = t;
    b.frequency.value = f;
    b.gain.value = g;
    b.Q.value = q;
    nodes.push(b);
    return b;
  };
  /** ゆれ（LFO）: 発振器 → 深さの増幅 → 目的の項目。 */
  const lfo = (rate: number, depth: number, target: AudioParam, wave: OscillatorType = "sine"): OscillatorNode => {
    const osc = ctx.createOscillator();
    osc.type = wave;
    osc.frequency.value = rate;
    const g = ctx.createGain();
    g.gain.value = depth;
    osc.connect(g);
    g.connect(target);
    osc.start();
    nodes.push(osc, g);
    return osc;
  };
  /** 元の音（dry）と効果（wet）を混ぜる枠。dry は mix が大きいほど少し引く（痩せすぎない程度）。 */
  const frame = (dryDrop = 0.5): { input: GainNode; output: GainNode; wet: GainNode; dry: GainNode } => {
    const input = gain(1);
    const output = gain(1);
    const dry = gain(1 - mix * dryDrop);
    const wet = gain(mix);
    input.connect(dry);
    dry.connect(output);
    wet.connect(output);
    return { input, output, wet, dry };
  };

  switch (type as ExtraFxType) {
    case "tape": {
      // 入力 → 低音を少し削る → 遅れ（ゆらぐ）→ 高音を丸める → テープの飽和 →（くり返し）。くり返すたびに暗く・平らになる
      const f = frame(0.3);
      const d = ctx.createDelay(2);
      d.delayTime.value = clamp(num(spec.ms, 350), 40, 1900) / 1000;
      nodes.push(d);
      const hp = filt("highpass", 140, 0, 0.7);
      const lp = filt("lowpass", clamp(num(spec.tone, 2800), 800, 9000), 0, 0.7);
      const sat = ctx.createWaveShaper();
      sat.curve = tapeSaturationCurve();
      sat.oversample = "2x";
      nodes.push(sat);
      const fb = gain(clamp(num(spec.feedback, 0.45), 0, 0.88));
      const depth = clamp(num(spec.depth, 0.35), 0, 1);
      // 遅い「ワウ」（回転むら）と速い「フラッター」（細かいゆれ）。時間のゆれは秒単位
      lfo(clamp(num(spec.rate, 0.55), 0.1, 3), 0.0006 * depth, d.delayTime);
      lfo(6.8, 0.00007 * depth, d.delayTime);
      f.input.connect(hp);
      hp.connect(d);
      d.connect(lp);
      lp.connect(sat);
      sat.connect(fb);
      fb.connect(d);
      sat.connect(f.wet);
      return { input: f.input, output: f.output, nodes };
    }
    case "rotary": {
      // 800Hz で高音（ホーン）と低音（ドラム）に分け、それぞれ「ドップラー（遅れのゆれ）」「音量のゆれ」「左右のゆれ」を、少し違う速さで回す
      const f = frame(0.3);
      const depth = clamp(num(spec.depth, 0.7), 0, 1);
      const horn = clamp(num(spec.rate, 0.8), 0.2, 8); // 0.8Hz≒ゆっくり（chorale）／6.7Hz≒速い（tremolo）
      const drum = horn * 0.85;
      const hi = filt("highpass", 800, 0, 0.7);
      const lo = filt("lowpass", 800, 0, 0.7);
      f.input.connect(hi);
      f.input.connect(lo);
      const rotor = (src: AudioNode, hz: number, doppler: number, am: number, panAmt: number): void => {
        const d = ctx.createDelay(0.02);
        d.delayTime.value = doppler * 1.2;
        nodes.push(d);
        lfo(hz, doppler * depth, d.delayTime);
        const g = gain(1 - am * depth);
        lfo(hz, am * depth * 0.5, g.gain);
        const p = ctx.createStereoPanner();
        p.pan.value = 0;
        nodes.push(p);
        lfo(hz, panAmt * depth, p.pan);
        src.connect(d);
        d.connect(g);
        g.connect(p);
        p.connect(f.wet);
      };
      rotor(hi, horn, 0.0004, 0.55, 0.85);
      rotor(lo, drum, 0.00025, 0.3, 0.5);
      return { input: f.input, output: f.output, nodes };
    }
    case "doubler": {
      // 左右に別々の遅れ（14ms／21ms 前後）を、別々の速さでゆらして足す。元の音は真ん中に残る（モノラルで聴いても消えにくい）
      const f = frame(0.35);
      const depth = clamp(num(spec.depth, 0.5), 0, 1);
      const base = clamp(num(spec.ms, 14), 6, 40) / 1000;
      const side = (delay: number, hz: number, pan: number): void => {
        const d = ctx.createDelay(0.1);
        d.delayTime.value = delay;
        nodes.push(d);
        lfo(hz, 0.0012 * depth, d.delayTime);
        const p = ctx.createStereoPanner();
        p.pan.value = pan;
        nodes.push(p);
        f.input.connect(d);
        d.connect(p);
        p.connect(f.wet);
      };
      const r = clamp(num(spec.rate, 0.4), 0.05, 4);
      side(base, r * 0.93, -0.9);
      side(base * 1.5, r * 1.27, 0.9);
      return { input: f.input, output: f.output, nodes };
    }
    case "pcomp": {
      // 強く潰した音を、元の音の下に足す（元の音は引かない）。アタックは5ms・リリースは120ms の柔らかい膝
      const input = gain(1);
      const output = gain(1);
      const c = ctx.createDynamicsCompressor();
      const thr = clamp(num(spec.threshold, -32), -60, 0);
      c.threshold.value = thr;
      c.ratio.value = clamp(num(spec.ratio, 10), 1, 20);
      c.attack.value = clamp(num(spec.attack, 0.005), 0.0005, 0.2);
      c.release.value = clamp(num(spec.release, 0.12), 0.02, 1);
      c.knee.value = 20;
      nodes.push(c);
      // Web Audio の DynamicsCompressorNode は自動でメイクアップ（音量の持ち上げ）をするので、ここでは足さない（2026-10-14 実測: 足すと +9dB うるさくなった）
      const makeup = gain(mix * dbToGain(clamp(num(spec.level, 0), -24, 6)));
      // DynamicsCompressorNode は約6ミリ秒の「先読み」の遅れを持つ。元の音も同じだけ遅らせないと、足したときに音が打ち消し合う（2026-10-14 実測）
      const dryDelay = ctx.createDelay(0.05);
      dryDelay.delayTime.value = 0.006;
      nodes.push(dryDelay);
      input.connect(dryDelay);
      dryDelay.connect(output);
      input.connect(c);
      c.connect(makeup);
      makeup.connect(output);
      return { input, output, nodes };
    }
    case "harmtrem": {
      // 700Hz で低音と高音に分け、音量のゆれを正反対にする（片方が大きいとき、もう片方は小さい）
      const input = gain(1);
      const output = gain(1);
      const depth = clamp(num(spec.depth, 0.6), 0, 1);
      const rate = clamp(num(spec.rate, 4.5), 0.5, 12);
      const lo = filt("lowpass", 700, 0, 0.7);
      const hi = filt("highpass", 700, 0, 0.7);
      const gl = gain(1 - depth / 2);
      const gh = gain(1 - depth / 2);
      const osc = ctx.createOscillator();
      osc.frequency.value = rate;
      const posAmt = gain(depth / 2);
      const negAmt = gain(-depth / 2);
      osc.connect(posAmt);
      osc.connect(negAmt);
      posAmt.connect(gl.gain);
      negAmt.connect(gh.gain);
      osc.start();
      nodes.push(osc);
      input.connect(lo);
      input.connect(hi);
      lo.connect(gl);
      hi.connect(gh);
      gl.connect(output);
      gh.connect(output);
      return { input, output, nodes };
    }
    case "octup": {
      // 増幅 → 全波整流（|x|。単音だと1オクターブ上の音になる）→ 直流と低音を除く → 高音を丸める → 混ぜる
      const f = frame(0.2);
      const sh = ctx.createWaveShaper();
      sh.curve = rectifierCurve();
      sh.oversample = "4x";
      nodes.push(sh);
      const pre = gain(dbToGain(clamp(num(spec.gain, 6), -6, 24)));
      const dc = filt("highpass", 250, 0, 0.7);
      const lp = filt("lowpass", clamp(num(spec.tone, 5200), 1500, 9000), 0, 0.7);
      const out = gain(dbToGain(clamp(num(spec.level, -2), -24, 12)));
      f.input.connect(pre);
      pre.connect(sh);
      sh.connect(dc);
      dc.connect(lp);
      lp.connect(out);
      out.connect(f.wet);
      return { input: f.input, output: f.output, nodes };
    }
    case "cabir": {
      // 箱とマイクの応答（インパルス）で畳み込む。tone（Hz）が小さいほど暗い箱。mix＝元の音との混ぜ具合（標準は 1＝全部通す）
      const f = frame(1);
      const kind: CabKind = spec.tone !== undefined && spec.tone < 3600 ? "dark" : spec.tone !== undefined && spec.tone > 5200 ? "bright" : "closed";
      const mic: MicPos = spec.size !== undefined && spec.size > 1.5 ? "far" : spec.size !== undefined && spec.size < 0.7 ? "off" : "center";
      // ir に録音IRの名前を書けば、近似の箱のかわりに本物の録音で畳み込む（登録がなければ近似に戻る）
      const data = (spec.ir ? recordedCabImpulse(spec.ir, ctx.sampleRate) : null) ?? cabImpulse(ctx.sampleRate, kind, mic);
      const buf = ctx.createBuffer(1, data.length, ctx.sampleRate);
      buf.getChannelData(0).set(data);
      const conv = ctx.createConvolver();
      conv.normalize = false;
      conv.buffer = buf;
      nodes.push(conv);
      f.input.connect(conv);
      conv.connect(f.wet);
      return { input: f.input, output: f.output, nodes };
    }
    case "envwah": {
      // 音の大きさを追いかけ（整流 → 15Hz のローパス）、その大きさでバンドパスの中心周波数を動かす。強く弾くと上がり、音が減ると戻る
      const f = frame(0);
      const base = clamp(num(spec.freq, 350), 120, 1500);
      const bp = filt("bandpass", base, 0, clamp(num(spec.q, 4.5), 0.7, 12));
      const rect = ctx.createWaveShaper();
      rect.curve = rectifierCurve(2048, 1);
      nodes.push(rect);
      const smooth = filt("lowpass", clamp(num(spec.rate, 14), 3, 40), 0, 0.5);
      const range = gain(clamp(num(spec.depth, 0.7), 0, 1) * 14000);
      f.input.connect(rect);
      rect.connect(smooth);
      smooth.connect(range);
      range.connect(bp.frequency);
      f.input.connect(bp);
      const out = gain(2.2 * mix);
      bp.connect(out);
      out.connect(f.output);
      f.dry.gain.value = 1 - mix;
      return { input: f.input, output: f.output, nodes };
    }
    case "springx": {
      // 2本のばね（往復 34ms と 41ms）を左右の耳に。チャープのつぶがビヨンと戻る。高音の丸めは tone
      const f = frame(0.3);
      const sec = clamp(num(spec.size, 1), 0.4, 2.5) * 1.6;
      const buf = ctx.createBuffer(2, Math.floor(ctx.sampleRate * sec), ctx.sampleRate);
      buf.getChannelData(0).set(springImpulse(ctx.sampleRate, { roundTrip: 0.034, seconds: sec, seed: 11 }));
      buf.getChannelData(1).set(springImpulse(ctx.sampleRate, { roundTrip: 0.041, seconds: sec, seed: 29 }));
      const conv = ctx.createConvolver();
      conv.normalize = true;
      conv.buffer = buf;
      nodes.push(conv);
      const tone = filt("lowpass", clamp(num(spec.tone, 4800), 1500, 12000), 0, 0.7);
      f.input.connect(conv);
      conv.connect(tone);
      tone.connect(f.wet);
      return { input: f.input, output: f.output, nodes };
    }
  }
  return null;
}
