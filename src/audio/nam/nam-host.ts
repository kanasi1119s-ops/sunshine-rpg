/**
 * NAM（Neural Amp Modeler）を使うための窓口。ワークレットの読み込み（1回）と、ギターごとのアンプの作成をする。
 * 作曲ソフトが `globalThis.__namAssets` に、埋め込んだ素材を入れておくと使える（ゲーム本体には入れていない）。
 */
export interface NamAssets {
  /** ワークレットのスクリプト（データURL）。 */
  processorUrl: string;
  /** NAMのWASMバイナリ。 */
  wasm: ArrayBuffer;
}
declare global {
  // eslint-disable-next-line no-var
  var __namAssets: NamAssets | undefined;
}

export class NamHost {
  private loaded: Promise<void> | null = null;

  static available(): boolean {
    return globalThis.__namAssets !== undefined;
  }

  private ensure(ctx: BaseAudioContext): Promise<void> {
    if (!this.loaded) {
      const assets = globalThis.__namAssets;
      if (!assets) {
        return Promise.reject(new Error("NAMの素材がありません"));
      }
      this.loaded = ctx.audioWorklet.addModule(assets.processorUrl);
    }
    return this.loaded;
  }

  /** ギター1本ぶんのアンプ（NAMのモデルを読み込んだ AudioWorkletNode）を作る。 */
  async createAmp(ctx: BaseAudioContext, modelJson: string): Promise<AudioWorkletNode> {
    await this.ensure(ctx);
    const assets = globalThis.__namAssets!;
    const node = new AudioWorkletNode(ctx, "nam-processor", {
      numberOfInputs: 1,
      numberOfOutputs: 1,
      outputChannelCount: [2],
      processorOptions: { wasmBinary: assets.wasm.slice(0), modelJson },
    });
    return node;
  }
}
