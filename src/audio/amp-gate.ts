/**
 * ノイズゲート（AudioWorklet）。高ゲインで目立つ雑音や、音の「ザー」という尾を、音の切れ目で小さくして締める。
 * 検出: 1.5kHz 以上を強調 → 整流 → 包絡（速く立ち上がり、ゆっくり戻る）。しきい値を超えたら開き、
 * しきい値より hysteresisDb 下がったら hold 秒待ってから、release 秒かけて depthDb だけ小さくする（-∞ 近くまで切るなら depthDb を大きく）。
 * 考え方は `docs/sound/amp-sim-guide.md` §5・提案4。`OfflineAudioContext`（書き出し）でも動く。
 */
export const GATE_PROCESSOR_NAME = "sunshine-gate";

export interface GateOptions {
  /** しきい値（dBFS。既定 -52）。 */
  thresholdDb?: number;
  /** 切り下げる深さ（dB。既定 24。メタルは 60 など）。 */
  depthDb: number;
  /** しきい値より何dB下がったら閉じはじめるか（既定 4）。 */
  hysteresisDb?: number;
  /** 待つ時間（秒。既定 0.02）。 */
  hold?: number;
  /** 閉じる時間（秒。既定 0.12）。 */
  release?: number;
  /** 開く時間（秒。既定 0.001）。 */
  attack?: number;
}

export const GATE_PROCESSOR_CODE = `
class SunshineGate extends AudioWorkletProcessor {
  constructor(options) {
    super();
    const o = options.processorOptions || {};
    const sr = sampleRate;
    const thr = Math.pow(10, (o.thresholdDb === undefined ? -52 : o.thresholdDb) / 20);
    this.thrOpen = thr;
    this.thrClose = thr * Math.pow(10, -(o.hysteresisDb === undefined ? 4 : o.hysteresisDb) / 20);
    this.floor = Math.pow(10, -(o.depthDb === undefined ? 24 : o.depthDb) / 20);
    this.holdSamples = Math.round((o.hold === undefined ? 0.02 : o.hold) * sr);
    this.ca = 1 - Math.exp(-1 / Math.max(1, (o.attack === undefined ? 0.001 : o.attack) * sr));
    this.cr = 1 - Math.exp(-1 / Math.max(1, (o.release === undefined ? 0.12 : o.release) * sr));
    this.hpA = 1 - Math.exp(-2 * Math.PI * 1500 / sr);
    this.envA = 1 - Math.exp(-1 / (0.0003 * sr));
    this.envR = 1 - Math.exp(-1 / (0.008 * sr));
    this.lp = 0; this.env = 0; this.gain = this.floor; this.open = false; this.hold = 0;
  }
  process(inputs, outputs) {
    const input = inputs[0], output = outputs[0];
    if (!input || input.length === 0) return true;
    const n = input[0].length;
    for (let i = 0; i < n; i++) {
      // 2026-10-20: 左右の大きいほうで開け閉めを決める（左だけを見ていたので、右に振ったギターではゲートが閉じたまま＝ほぼ無音になっていた）
      const l = input[0][i], r = input[1] ? input[1][i] : l;
      const x = Math.abs(l) >= Math.abs(r) ? l : r;
      this.lp += this.hpA * (x - this.lp);
      const a = Math.abs(x - this.lp);
      this.env += (a > this.env ? this.envA : this.envR) * (a - this.env);
      if (this.env > this.thrOpen) { this.open = true; this.hold = this.holdSamples; }
      else if (this.open && this.env < this.thrClose) { if (this.hold > 0) this.hold--; else this.open = false; }
      const target = this.open ? 1 : this.floor;
      this.gain += (target - this.gain) * (target > this.gain ? this.ca : this.cr);
      for (let c = 0; c < output.length; c++) output[c][i] = (input[c] || input[0])[i] * this.gain;
    }
    return true;
  }
}
registerProcessor("${GATE_PROCESSOR_NAME}", SunshineGate);
`;

const loaded = new WeakMap<BaseAudioContext, Promise<void>>();
/** ゲートのワークレットを読み込む（同じ ctx では1回だけ）。ワークレットを持たない環境（テストなど）では null。 */
export function loadGate(ctx: BaseAudioContext): Promise<void> | null {
  const worklet = (ctx as unknown as { audioWorklet?: { addModule(url: string): Promise<void> } }).audioWorklet;
  if (!worklet || typeof AudioWorkletNode === "undefined") return null;
  let p = loaded.get(ctx);
  if (!p) {
    p = worklet.addModule(`data:text/javascript;base64,${btoa(GATE_PROCESSOR_CODE)}`);
    loaded.set(ctx, p);
  }
  return p;
}

export function createGate(ctx: BaseAudioContext, opts: GateOptions): AudioWorkletNode {
  return new AudioWorkletNode(ctx, GATE_PROCESSOR_NAME, { numberOfInputs: 1, numberOfOutputs: 1, outputChannelCount: [2], processorOptions: opts });
}
