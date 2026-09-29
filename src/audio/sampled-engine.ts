import { Sequencer, WorkletSynthesizer } from "spessasynth_lib";
import processorUrl from "spessasynth_lib/dist/spessasynth_processor.min.js?url";
import soundfontUrl from "./soundfont/game.sf3?url";
import { scoreToMidi } from "./midi-export";
import type { Score } from "./score";

/**
 * 録音音源（サウンドフォント）でBGMを鳴らす。曲（Score）を標準MIDIに変換し、シーケンサーに渡す。
 * サウンドフォントは FluidR3 Mono GM（MITライセンス）から、ゲームで使う楽器だけを切り出したもの（`tools/soundfont/`、`docs/assets-credits.md`）。
 * 読み込みには少し時間がかかるので、準備ができるまでは、呼び出し側（AudioEngine）が合成音で鳴らす。
 */

/** BGMプレイヤー（1ファイルのHTML）では、外部ファイルを読み込めないので、あらかじめ埋め込んだ素材をここへ入れる。 */
export interface SampledAssets {
  soundfont: ArrayBuffer;
  processorUrl: string;
}
declare global {
  // eslint-disable-next-line no-var
  var __sampledAssets: SampledAssets | undefined;
}

export class SampledBgm {
  private synth: WorkletSynthesizer | null = null;
  private seq: Sequencer | null = null;
  private loading: Promise<boolean> | null = null;
  private ready = false;
  private failed = false;
  private pendingOffset = 0;
  private playing = false;

  isReady(): boolean {
    return this.ready;
  }
  hasFailed(): boolean {
    return this.failed;
  }
  isPlaying(): boolean {
    return this.playing;
  }

  /** 準備を始める（何度呼んでもよい）。出力は `destination` につなぐ。 */
  load(ctx: AudioContext, destination: AudioNode): Promise<boolean> {
    if (!this.loading) {
      this.loading = this.doLoad(ctx, destination).catch((error) => {
        console.warn("録音音源の準備に失敗しました。合成音で鳴らします:", error);
        this.failed = true;
        return false;
      });
    }
    return this.loading;
  }

  private async doLoad(ctx: AudioContext, destination: AudioNode): Promise<boolean> {
    const embedded = globalThis.__sampledAssets;
    const workletUrl = embedded ? embedded.processorUrl : processorUrl;
    await ctx.audioWorklet.addModule(workletUrl);
    const buffer = embedded ? embedded.soundfont : await (await fetch(soundfontUrl)).arrayBuffer();
    const synth = new WorkletSynthesizer(ctx);
    synth.connect(destination);
    await synth.soundBankManager.addSoundBank(buffer, "main");
    await synth.isReady;
    const seq = new Sequencer(synth);
    seq.loopCount = -1;
    seq.eventHandler.addEvent("songChange", "sampled-bgm", () => {
      if (this.pendingOffset > 0) {
        seq.currentTime = this.pendingOffset;
        this.pendingOffset = 0;
      }
      seq.play();
    });
    this.synth = synth;
    this.seq = seq;
    this.ready = true;
    return true;
  }

  /** 曲を鳴らす。`offsetSec` の位置から始められる。 */
  play(score: Score, offsetSec = 0): void {
    if (!this.seq) {
      return;
    }
    const midi = scoreToMidi(score);
    this.pendingOffset = offsetSec;
    this.playing = true;
    const binary = midi.buffer.slice(midi.byteOffset, midi.byteOffset + midi.byteLength) as ArrayBuffer;
    this.seq.loadNewSongList([{ binary, fileName: "bgm.mid" }]);
  }

  stop(): void {
    this.playing = false;
    this.pendingOffset = 0;
    if (this.seq) {
      this.seq.pause();
      this.synth?.stopAll(true);
    }
  }

  positionSec(): number {
    return this.seq && this.playing ? this.seq.currentTime : 0;
  }
}
