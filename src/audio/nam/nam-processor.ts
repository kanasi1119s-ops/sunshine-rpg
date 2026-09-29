/**
 * Neural Amp Modeler（NAM、MITライセンス）を動かす AudioWorklet。
 * 実際のアンプを録音して学習させた「モデル（.namファイル）」を読み込み、ギターの音をそのアンプの音にする。
 * このファイルは、作曲ソフトのビルド（tools/composer/build.mjs）が、1つのスクリプトにまとめて埋め込む。
 * WASMのバイナリは、メインスレッドから processorOptions で受け取る（ワークレットの中ではファイルを読み込めないため）。
 */
import { createNamModule, NamWasmModule } from "@opendaw/nam-wasm";

declare const sampleRate: number;
declare class AudioWorkletProcessor {
  readonly port: MessagePort;
  constructor(options?: unknown);
}
declare function registerProcessor(name: string, ctor: new (options?: unknown) => AudioWorkletProcessor): void;

class NamProcessor extends AudioWorkletProcessor {
  private nam: NamWasmModule | null = null;
  private instance = -1;
  private pendingModel: string | null = null;
  private gain = 1;
  private mono = new Float32Array(128);
  private out = new Float32Array(128);

  constructor(options?: unknown) {
    super(options);
    const wasmBinary = (options as { processorOptions?: { wasmBinary?: ArrayBuffer } } | undefined)?.processorOptions?.wasmBinary;
    void this.init(wasmBinary);
    this.port.onmessage = (event: MessageEvent) => {
      const data = event.data as { type: string; modelJson?: string };
      if (data.type === "loadModel" && data.modelJson !== undefined) {
        this.load(data.modelJson);
      }
    };
  }

  private async init(wasmBinary?: ArrayBuffer): Promise<void> {
    const module = await createNamModule(wasmBinary ? { wasmBinary } : undefined);
    const nam = NamWasmModule.fromModule(module);
    nam.setSampleRate(sampleRate);
    this.instance = nam.createInstance();
    this.nam = nam;
    this.port.postMessage({ type: "ready" });
    if (this.pendingModel !== null) {
      this.load(this.pendingModel);
    }
  }

  private load(json: string): void {
    if (!this.nam) {
      this.pendingModel = json;
      return;
    }
    const ok = this.nam.loadModel(this.instance, json);
    // モデルごとの音量の差をそろえる（モデルが「音量」の情報を持っているときは、-18dBFSに合わせる）
    this.gain = ok && this.nam.hasModelLoudness(this.instance) ? Math.pow(10, (-18 - this.nam.getModelLoudness(this.instance)) / 20) : 1;
    this.port.postMessage({ type: "modelLoaded", success: ok });
  }

  process(inputs: Float32Array[][], outputs: Float32Array[][]): boolean {
    const nam = this.nam;
    const input = inputs[0];
    const output = outputs[0];
    if (!output || output.length === 0) {
      return true;
    }
    const frames = output[0].length;
    if (!nam || !nam.hasModel(this.instance) || !input || input.length === 0) {
      // モデルがない間は、そのまま通す
      for (let ch = 0; ch < output.length; ch++) {
        if (input && input[ch]) output[ch].set(input[ch]);
      }
      return true;
    }
    if (this.mono.length < frames) {
      this.mono = new Float32Array(frames);
      this.out = new Float32Array(frames);
    }
    const mono = this.mono.subarray(0, frames);
    const left = input[0];
    const right = input[1] ?? input[0];
    for (let i = 0; i < frames; i++) mono[i] = (left[i] + right[i]) * 0.5;
    const out = this.out.subarray(0, frames);
    nam.process(this.instance, mono, out);
    for (let ch = 0; ch < output.length; ch++) {
      for (let i = 0; i < frames; i++) output[ch][i] = out[i] * this.gain;
    }
    return true;
  }
}

registerProcessor("nam-processor", NamProcessor);
