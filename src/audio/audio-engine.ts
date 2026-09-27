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
  private activeBgmNodes: OscillatorNode[] = [];

  /** 最初のユーザー操作のタイミングで呼ぶ。AudioContextを用意し、一時停止も解除する。 */
  private ensureContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.bgmGain = this.ctx.createGain();
      this.bgmGain.gain.value = this.muted ? 0 : this.bgmVolume;
      this.bgmGain.connect(this.ctx.destination);

      this.seGain = this.ctx.createGain();
      this.seGain.gain.value = this.muted ? 0 : this.seVolume;
      this.seGain.connect(this.ctx.destination);
    }
    if (this.ctx.state === "suspended") {
      void this.ctx.resume();
    }
    return this.ctx;
  }

  private scheduleNote(
    ctx: AudioContext,
    destination: GainNode,
    event: ScheduledNote,
    when: number,
  ): OscillatorNode {
    const osc = ctx.createOscillator();
    osc.type = event.waveform;
    osc.frequency.value = event.frequency;

    const gain = ctx.createGain();
    const attack = 0.005;
    const release = Math.min(0.05, event.durationSec * 0.3);
    gain.gain.setValueAtTime(0, when);
    gain.gain.linearRampToValueAtTime(event.volume, when + attack);
    gain.gain.setValueAtTime(event.volume, Math.max(when + attack, when + event.durationSec - release));
    gain.gain.linearRampToValueAtTime(0, when + event.durationSec);

    osc.connect(gain);
    gain.connect(destination);
    osc.start(when);
    osc.stop(when + event.durationSec + 0.02);
    return osc;
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
          const node = this.scheduleNote(ctx, this.bgmGain!, event, nextStart + event.startSec);
          this.activeBgmNodes.push(node);
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
