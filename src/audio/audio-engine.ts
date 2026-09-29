import { createBgmBus, scheduleInstrumentNote, type Source } from "./voices";
import { flattenScore, getScoreDurationSec, type Score, type ScheduledNote } from "./score";

const SCHEDULE_AHEAD_SEC = 3;
const SCHEDULE_INTERVAL_MS = 1000;

/**
 * Web Audio APIでBGM・効果音を鳴らす。
 * ブラウザの決まりで、最初の操作（クリック・キー入力・タップ）があるまで音は出せないため、
 * AudioContextの生成は最初のユーザー操作まで遅らせる（`ensureContext` を参照）。
 */
export class AudioEngine {
  private ctx: AudioContext | null = null;
  private bgmGain: GainNode | null = null;
  private seGain: GainNode | null = null;

  private bgmVolume = 0.6;
  private seVolume = 0.8;
  private muted = false;

  private bgmLoopHandle: number | null = null;
  private activeBgmNodes: Source[] = [];
  /** BGMだけに、ほんのり残響をかけるための入り口（`ensureContext`で用意する）。 */
  private bgmBus: GainNode | null = null;

  /** 最初のユーザー操作のタイミングで呼ぶ。AudioContextを用意し、一時停止も解除する。 */
  private ensureContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.bgmGain = this.ctx.createGain();
      this.bgmGain.gain.value = this.muted ? 0 : this.bgmVolume;
      this.bgmGain.connect(this.ctx.destination);
      this.bgmBus = createBgmBus(this.ctx, this.bgmGain);

      this.seGain = this.ctx.createGain();
      this.seGain.gain.value = this.muted ? 0 : this.seVolume;
      this.seGain.connect(this.ctx.destination);
    }
    if (this.ctx.state === "suspended") {
      void this.ctx.resume();
    }
    return this.ctx;
  }

  /**
   * 音を1つ予約する。`rich`（BGM用）のときは、少しだけ音程をずらした2つ目の音を重ねて厚みを出し、
   * 立ち上がりに軽いアタック、鳴っている間にゆるやかな減衰をつけて、電子音の平らさをやわらげる。
   * 効果音は従来どおり（`rich`なし）。
   */
  private scheduleNote(
    ctx: AudioContext,
    destination: AudioNode,
    event: ScheduledNote,
    when: number,
    rich = false,
  ): Source[] {
    const instrumental = scheduleInstrumentNote(ctx, destination, event, when);
    if (instrumental.length > 0) {
      return instrumental;
    }
    const gain = ctx.createGain();
    const attack = rich ? 0.012 : 0.005;
    const release = Math.min(rich ? 0.12 : 0.05, event.durationSec * 0.3);
    const peak = event.volume;
    gain.gain.setValueAtTime(0, when);
    gain.gain.linearRampToValueAtTime(peak, when + attack);
    if (rich) {
      // 鳴らし始めは少し強く、すぐ7割ほどに落ち着く（ゆるやかな減衰）
      gain.gain.linearRampToValueAtTime(peak * 0.72, when + Math.min(0.18, event.durationSec * 0.5));
    }
    const holdLevel = rich ? peak * 0.72 : peak;
    gain.gain.setValueAtTime(holdLevel, Math.max(when + attack, when + event.durationSec - release));
    gain.gain.linearRampToValueAtTime(0, when + event.durationSec);
    gain.connect(destination);

    const detunes = rich && event.waveform !== "sine" ? [-6, 6] : [0];
    const oscillators: OscillatorNode[] = [];
    for (const cents of detunes) {
      const osc = ctx.createOscillator();
      osc.type = event.waveform;
      osc.frequency.value = event.frequency;
      osc.detune.value = cents;
      if (detunes.length > 1) {
        const half = ctx.createGain();
        half.gain.value = 0.5;
        osc.connect(half);
        half.connect(gain);
      } else {
        osc.connect(gain);
      }
      osc.start(when);
      osc.stop(when + event.durationSec + 0.02);
      oscillators.push(osc);
    }
    return oscillators;
  }

  playSe(score: Score): void {
    const ctx = this.ensureContext();
    const events = flattenScore(score);
    for (const event of events) {
      this.scheduleNote(ctx, this.seGain!, event, ctx.currentTime);
    }
  }

  playBgm(score: Score): void {
    this.stopBgm();
    const ctx = this.ensureContext();
    const durationSec = getScoreDurationSec(score);
    if (durationSec <= 0) {
      return;
    }

    let nextStart = ctx.currentTime + 0.05;

    const scheduleAhead = (): void => {
      while (nextStart < ctx.currentTime + SCHEDULE_AHEAD_SEC) {
        const events = flattenScore(score);
        for (const event of events) {
          const nodes = this.scheduleNote(ctx, this.bgmBus!, event, nextStart + event.startSec, true);
          this.activeBgmNodes.push(...nodes);
        }
        nextStart += durationSec;
        if (!score.loop) {
          return;
        }
      }
    };

    scheduleAhead();
    if (score.loop) {
      this.bgmLoopHandle = window.setInterval(scheduleAhead, SCHEDULE_INTERVAL_MS);
    }
  }

  stopBgm(): void {
    if (this.bgmLoopHandle !== null) {
      window.clearInterval(this.bgmLoopHandle);
      this.bgmLoopHandle = null;
    }
    for (const node of this.activeBgmNodes) {
      try {
        node.stop();
      } catch {
        // すでに再生が終わっているノードは無視する。
      }
    }
    this.activeBgmNodes = [];
  }

  setBgmVolume(volume: number): void {
    this.bgmVolume = volume;
    if (this.bgmGain) {
      this.bgmGain.gain.value = this.muted ? 0 : volume;
    }
  }

  setSeVolume(volume: number): void {
    this.seVolume = volume;
    if (this.seGain) {
      this.seGain.gain.value = this.muted ? 0 : volume;
    }
  }

  setMuted(muted: boolean): void {
    this.muted = muted;
    if (this.bgmGain) {
      this.bgmGain.gain.value = muted ? 0 : this.bgmVolume;
    }
    if (this.seGain) {
      this.seGain.gain.value = muted ? 0 : this.seVolume;
    }
  }

  isMuted(): boolean {
    return this.muted;
  }
}
