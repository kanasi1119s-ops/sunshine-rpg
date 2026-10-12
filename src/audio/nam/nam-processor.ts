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

// ワークレットの中には URL がない（emscripten の読み込みコードが参照する）ので、最小のかわりを置く
if (typeof (globalThis as { URL?: unknown }).URL === "undefined") {
  (globalThis as { URL?: unknown }).URL = class {
    href: string;
    constructor(url: string) {
      this.href = String(url);
    }
    toString(): string {
      return this.href;
    }
  };
}

class NamProcessor extends AudioWorkletProcessor {
  private nam: NamWasmModule | null = null;
  private instance = -1;
  private pendingModel: string | null = null;
  private gain = 1;
  private mono = new Float32Array(128);
  private out = new Float32Array(128);

  constructor(options?: unknown) {
    super(options);
    const opts = (options as { processorOptions?: { wasmBinary?: ArrayBuffer; modelJson?: string } } | undefined)?.processorOptions;
    // モデルは、はじめから受け取れる（WAVの書き出し＝オフラインでは、あとからのメッセージが届かないことがあるため）
    if (opts?.modelJson !== undefined) this.pendingModel = opts.modelJson;
    this.init(opts?.wasmBinary).catch((error: unknown) => this.port.postMessage({ type: "error", message: String(error) }));
    this.port.onmessage = (event: MessageEvent) => {
      const data = event.data as { type: string; modelJson?: string };
      if (data.type === "loadModel" && data.modelJson !== undefined) {
        this.load(data.modelJson);
      }
    };
  }

  private async init(wasmBinary?: ArrayBuffer): Promise<void> {
    // WASMはその場で（同期で）組み立てる。オフラインの書き出しでは、あとの処理が動く前に音の処理が始まるので、
    // 組み立てが同期で終わったら、待たずにそのまま使う（最初の音から間に合わせる）
    const arg = wasmBinary
      ? ({
          wasmBinary,
          instantiateWasm: (imports: WebAssembly.Imports, receive: (instance: WebAssembly.Instance, module: WebAssembly.Module) => void) => {
            const compiled = new WebAssembly.Module(wasmBinary);
            const instance = new WebAssembly.Instance(compiled, imports);
            receive(instance, compiled);
            return instance.exports;
          },
        } as Parameters<typeof createNamModule>[0])
      : undefined;
    const promise = createNamModule(arg);
    const ready = arg as unknown as { _malloc?: unknown } | undefined;
    const module = ready && typeof ready._malloc === "function" ? (arg as unknown as Awaited<typeof promise>) : await promise;
    this.setup(module);
  }

  private setup(module: Awaited<ReturnType<typeof createNamModule>>): void {
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
