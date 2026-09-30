/**
 * マスターエフェクト（曲全体にかける、無料のWeb Audioだけで作った効果）。外部の素材やプラグインは使わない。
 * 順番: ビットクラッシュ → テープの飽和 → トレモロ → フィルター → （並列）ディレイ・コーラス。
 * 作曲ソフトの再生・WAV書き出しの両方に同じ設定がかかる（`Score.fx`）。ゲーム本体の再生にも使える。
 */
export interface MasterFxSettings {
  /** ビットクラッシュ: 何ビットに粗くするか（4〜12。小さいほどザラザラ）。 */
  bitcrush?: number;
  /** テープの飽和（あたたかい歪み）0〜1。 */
  tape?: number;
  /** トレモロ: 揺れの速さ（拍あたりの回数の逆＝周期の拍数。例 0.5＝8分音符の周期）と深さ 0〜1。 */
  tremolo?: { periodBeats: number; depth: number };
  /** フィルター: ローパスかハイパスを固定の周波数で。 */
  filter?: { type: "lowpass" | "highpass"; hz: number };
  /** ディレイ: 長さ（拍。例 0.75＝付点8分）・フィードバック 0〜0.85・音量 0〜1。 */
  delay?: { beats: number; feedback: number; mix: number };
  /** コーラス（揺れる重ね）の量 0〜1。 */
  chorus?: number;
}

type Ctx = BaseAudioContext;
const clamp = (x: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, x));

/** 数値の範囲を整えた設定にする（範囲外・型違いは捨てる）。何も残らなければ undefined。 */
export function sanitizeFx(input: unknown): MasterFxSettings | undefined {
  if (!input || typeof input !== "object") return undefined;
  const f = input as Record<string, unknown>;
  const out: MasterFxSettings = {};
  const num = (v: unknown): number | undefined => (typeof v === "number" && Number.isFinite(v) ? v : undefined);
  const bc = num(f.bitcrush); if (bc !== undefined) out.bitcrush = Math.round(clamp(bc, 4, 12));
  const tp = num(f.tape); if (tp !== undefined && tp > 0) out.tape = clamp(tp, 0, 1);
  const tr = f.tremolo as Record<string, unknown> | undefined;
  if (tr && num(tr.periodBeats) !== undefined && num(tr.depth) !== undefined) out.tremolo = { periodBeats: clamp(num(tr.periodBeats)!, 0.125, 8), depth: clamp(num(tr.depth)!, 0, 1) };
  const fl = f.filter as Record<string, unknown> | undefined;
  if (fl && (fl.type === "lowpass" || fl.type === "highpass") && num(fl.hz) !== undefined) out.filter = { type: fl.type, hz: clamp(num(fl.hz)!, 40, 18000) };
  const dl = f.delay as Record<string, unknown> | undefined;
  if (dl && num(dl.beats) !== undefined) out.delay = { beats: clamp(num(dl.beats)!, 0.0625, 4), feedback: clamp(num(dl.feedback) ?? 0.35, 0, 0.85), mix: clamp(num(dl.mix) ?? 0.25, 0, 1) };
  const ch = num(f.chorus); if (ch !== undefined && ch > 0) out.chorus = clamp(ch, 0, 1);
  return Object.keys(out).length ? out : undefined;
}

/** 量子化の階段（ビットクラッシュ）の波形。 */
function crushCurve(bits: number): Float32Array<ArrayBuffer> {
  const steps = 2 ** (bits - 1), c = new Float32Array(4096);
  for (let i = 0; i < c.length; i++) { const x = (i / (c.length - 1)) * 2 - 1; c[i] = Math.round(x * steps) / steps; }
  return c;
}
function tapeCurve(amount: number): Float32Array<ArrayBuffer> {
  const k = 1 + amount * 4, c = new Float32Array(2048);
  for (let i = 0; i < c.length; i++) { const x = (i / (c.length - 1)) * 2 - 1; c[i] = Math.tanh(x * k) / Math.tanh(k); }
  return c;
}

export class MasterFx {
  readonly input: GainNode;
  readonly output: GainNode;
  private nodes: AudioNode[] = [];
  private oscs: OscillatorNode[] = [];
  constructor(private readonly ctx: Ctx) {
    this.input = ctx.createGain();
    this.output = ctx.createGain();
    this.input.connect(this.output);
  }
  /** 設定を反映する（作り直す）。fx が無ければ素通し。 */
  configure(fx: MasterFxSettings | undefined, bpm: number): void {
    const ctx = this.ctx;
    for (const o of this.oscs) { try { o.stop(); } catch { /* すでに止まっている */ } o.disconnect(); }
    for (const n of this.nodes) n.disconnect();
    this.nodes = []; this.oscs = [];
    this.input.disconnect();
    const s = sanitizeFx(fx);
    if (!s) { this.input.connect(this.output); return; }
    const beatSec = 60 / Math.max(30, bpm);
    let tail: AudioNode = this.input;
    const add = <T extends AudioNode>(n: T): T => { this.nodes.push(n); tail.connect(n); tail = n; return n; };
    if (s.bitcrush) { const w = ctx.createWaveShaper(); w.curve = crushCurve(s.bitcrush); add(w); }
    if (s.tape) { const w = ctx.createWaveShaper(); w.curve = tapeCurve(s.tape); w.oversample = "2x"; add(w); const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 16000 - s.tape * 6000; add(lp); }
    if (s.tremolo) {
      const g = ctx.createGain(); g.gain.value = 1 - s.tremolo.depth / 2; add(g);
      const lfo = ctx.createOscillator(); lfo.type = "sine"; lfo.frequency.value = 1 / (s.tremolo.periodBeats * beatSec);
      const amt = ctx.createGain(); amt.gain.value = s.tremolo.depth / 2; lfo.connect(amt); amt.connect(g.gain); lfo.start(); this.oscs.push(lfo); this.nodes.push(amt);
    }
    if (s.filter) { const f = ctx.createBiquadFilter(); f.type = s.filter.type; f.frequency.value = s.filter.hz; f.Q.value = 0.8; add(f); }
    const merge = ctx.createGain(); this.nodes.push(merge);
    tail.connect(merge);
    if (s.delay) {
      const d = ctx.createDelay(4); d.delayTime.value = Math.min(3.9, s.delay.beats * beatSec);
      const fb = ctx.createGain(); fb.gain.value = s.delay.feedback;
      const tone = ctx.createBiquadFilter(); tone.type = "lowpass"; tone.frequency.value = 5000;
      const wet = ctx.createGain(); wet.gain.value = s.delay.mix;
      tail.connect(d); d.connect(tone); tone.connect(fb); fb.connect(d); tone.connect(wet); wet.connect(merge);
      this.nodes.push(d, fb, tone, wet);
    }
    if (s.chorus) {
      const wet = ctx.createGain(); wet.gain.value = s.chorus * 0.5; wet.connect(merge); this.nodes.push(wet);
      [0.013, 0.021].forEach((base, i) => {
        const d = ctx.createDelay(0.1); d.delayTime.value = base;
        const lfo = ctx.createOscillator(); lfo.type = "sine"; lfo.frequency.value = 0.35 + i * 0.22;
        const amt = ctx.createGain(); amt.gain.value = 0.0035 * (0.5 + s.chorus!);
        lfo.connect(amt); amt.connect(d.delayTime); lfo.start(); this.oscs.push(lfo);
        tail.connect(d); d.connect(wet); this.nodes.push(d, amt);
      });
    }
    merge.connect(this.output);
  }
}
