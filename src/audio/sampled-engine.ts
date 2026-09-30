import { Sequencer, WorkletSynthesizer } from "spessasynth_lib";
import processorUrl from "spessasynth_lib/dist/spessasynth_processor.min.js?url";
import soundfontUrl from "./soundfont/game.sf3?url";
import { AmpRack } from "./amp-rack";
import type { NamHost } from "./nam/nam-host";
import { scoreToMidiInfo } from "./midi-export";
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
  private rack: AmpRack | null = null;
  private namHost: NamHost | null = null;
  private seq: Sequencer | null = null;
  private loading: Promise<boolean> | null = null;
  private ready = false;
  private failed = false;
  private pendingOffset = 0;
  private playing = false;
  private buffer: ArrayBuffer | null = null;
  private ctx: AudioContext | null = null;

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
    // addSoundBank は渡したデータを使い切る（転送する）ので、効果音用のシンセサイザーのために、控えを取っておく
    this.buffer = buffer.slice(0);
    this.ctx = ctx;
    const synth = new WorkletSynthesizer(ctx);
    // 各チャンネルの出力を取り出し、楽器ごとのアンプ・ミキサー（AmpRack）を通してから、出口へ。
    // 出力0は、録音音源の残響・コーラスの戻りなので、そのまま出口へつなぐ。
    const rack = new AmpRack(ctx, destination);
    for (let ch = 0; ch < 16; ch++) {
      synth.connectChannel(rack.input(ch), ch);
    }
    (synth as unknown as { worklet: AudioWorkletNode }).worklet.connect(destination, 0);
    this.rack = rack;
    if (this.namHost) {
      rack.setNam(this.namHost);
    }
    await synth.soundBankManager.addSoundBank(buffer, "main");
    await synth.isReady;
    const seq = new Sequencer(synth);
    // 0=ループしない、Infinity=くり返し続ける（-1 ではくり返さず、1回で止まってしまう）
    seq.loopCount = Infinity;
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

  /** 効果音用の、もう1つのシンセサイザー（同じ録音音源を使う）。BGMとは別に鳴らすため。 */
  async createExtraSynth(destination: AudioNode): Promise<WorkletSynthesizer | null> {
    if (!this.ready || !this.buffer || !this.ctx) {
      return null;
    }
    const synth = new WorkletSynthesizer(this.ctx);
    synth.connect(destination);
    // 読み込みのたびに元のデータが消費されることがあるので、コピーを渡す
    await synth.soundBankManager.addSoundBank(this.buffer.slice(0), "main");
    await synth.isReady;
    return synth;
  }

  /** NAM（実際のアンプを学習したモデル）を使えるようにする（作曲ソフトだけ）。 */
  setNam(host: NamHost | null): void {
    this.rack?.setNam(host);
    this.namHost = host;
  }

  /** 曲を鳴らす。`offsetSec` の位置から始められる。 */
  play(score: Score, offsetSec = 0): void {
    if (!this.seq) {
      return;
    }
    const { midi, programs, amps } = scoreToMidiInfo(score);
    this.rack?.configure(programs, score.tone ?? "rock", 9, amps, score.namModels ?? {}, score.ampPlugins ?? {});
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

  /** 再生中の曲を、指定位置へ移す。 */
  seek(sec: number): void {
    if (this.seq && this.playing) {
      this.seq.currentTime = sec;
    }
  }

  positionSec(): number {
    return this.seq && this.playing ? this.seq.currentTime : 0;
  }
}

/** 効果音を録音音源で鳴らす。MIDIのイベントを、タイマーで少しずつ送る（効果音は数秒なので、これで十分）。 */
export class SampledSe {
  private synth: WorkletSynthesizer | null = null;
  private starting = false;
  private nextChannel = 0;

  isReady(): boolean {
    return this.synth !== null;
  }

  async load(bgm: SampledBgm, destination: AudioNode): Promise<void> {
    if (this.synth || this.starting) {
      return;
    }
    this.starting = true;
    try {
      this.synth = await bgm.createExtraSynth(destination);
    } catch (error) {
      console.warn("効果音の録音音源の準備に失敗しました。合成音で鳴らします:", error);
    }
  }

  /**
   * 1音を予約する。`delaySec`後に鳴らし、`lengthSec`後に離す。
   * 同じ音源を使う効果音どうしが重なっても楽器が入れ替わらないよう、音の直前に楽器を指定し、使うチャンネルを順番に変える。
   */
  note(program: number, drum: boolean, midiNote: number, velocity: number, delaySec: number, lengthSec: number): void {
    const synth = this.synth;
    if (!synth) {
      return;
    }
    const channel = drum ? 9 : this.pickChannel();
    window.setTimeout(() => {
      if (!drum) {
        synth.programChange(channel, program);
      }
      synth.noteOn(channel, midiNote, velocity);
      window.setTimeout(() => synth.noteOff(channel, midiNote), Math.max(30, lengthSec * 1000));
    }, Math.max(0, delaySec * 1000));
  }

  private pickChannel(): number {
    const channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15];
    const channel = channels[this.nextChannel % channels.length];
    this.nextChannel++;
    return channel;
  }
}
