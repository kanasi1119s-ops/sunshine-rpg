import { SampledBgm } from "./sampled-engine";
import { createBgmBus, scheduleInstrumentNote, type Source } from "./voices";
import { flattenScore, getScoreDurationSec, type Score, type ScheduledNote } from "./score";

/** `?synth` をつけて開くと、録音音源を使わず合成音だけで鳴らす（音の比較・不具合の切り分け用）。 */
const SYNTH_ONLY_FROM_URL = typeof location !== "undefined" && new URLSearchParams(location.search).has("synth");
const SCHEDULE_AHEAD_SEC = 2.5;
const SCHEDULE_INTERVAL_MS = 250;

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
  private activeBgmNodes = new Set<Source>();
  /** BGMだけに、ほんのり残響をかけるための入り口（`ensureContext`で用意する）。 */
  private bgmBus: GainNode | null = null;
  /** 録音音源（サウンドフォント）のBGM再生。準備ができるまでは合成音で鳴らす。 */
  private sampled = new SampledBgm();
  private sampledBus: GainNode | null = null;
  private currentBgm: Score | null = null;
  private synthOnly = SYNTH_ONLY_FROM_URL;
  private bgmLoopStart = 0;
  private bgmDurationSec = 0;

  /** 最初のユーザー操作のタイミングで呼ぶ。AudioContextを用意し、一時停止も解除する。 */
  private ensureContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.bgmGain = this.ctx.createGain();
      this.bgmGain.gain.value = this.muted ? 0 : this.bgmVolume;
      this.bgmGain.connect(this.ctx.destination);
      this.bgmBus = createBgmBus(this.ctx, this.bgmGain);
      // 録音音源は、ほんの少しだけ残響を足して、同じ出口（音量・仕上げ）を通す
      this.sampledBus = createBgmBus(this.ctx, this.bgmGain, 0.1);
      if (!this.synthOnly) {
        void this.sampled.load(this.ctx, this.sampledBus).then((ok) => {
          if (ok && this.currentBgm && this.bgmLoopHandle !== null) {
            // 準備ができたら、いま合成音で鳴っている曲を、同じ位置から録音音源に切り替える
            this.playBgm(this.currentBgm, this.getBgmPositionSec());
          }
        });
      }

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

  /** `offsetSec`: 曲の途中（この秒数の位置）から鳴らす。BGMプレイヤーの「聴きたい部分から再生」用。 */
  playBgm(score: Score, offsetSec = 0): void {
    this.stopBgm();
    const ctx = this.ensureContext();
    const durationSec = getScoreDurationSec(score);
    if (durationSec <= 0) {
      return;
    }
    this.currentBgm = score;
    if (this.sampled.isReady() && !this.synthOnly) {
      this.sampled.play(score, offsetSec);
      this.bgmLoopHandle = -1; // 「鳴っている」印（録音音源はシーケンサーが自分でループする）
      return;
    }

    // 曲全体を一度に予約すると、長い曲では数千個の音を一気に作ってしまい、音が途切れたり出なくなる。
    // そこで、先の数秒ぶんだけを少しずつ予約する（次の周回も同じ要領でつなぐ）。
    const events = flattenScore(score).sort((x, y) => x.startSec - y.startSec);
    const offset = Math.max(0, Math.min(offsetSec, durationSec - 0.01));
    let loopStart = ctx.currentTime + 0.08 - offset;
    let index = 0;
    while (index < events.length && events[index].startSec < offset) {
      index++;
    }
    this.bgmLoopStart = loopStart;
    this.bgmDurationSec = durationSec;

    const scheduleAhead = (): void => {
      const horizon = ctx.currentTime + SCHEDULE_AHEAD_SEC;
      for (;;) {
        if (index >= events.length) {
          if (!score.loop) {
            return;
          }
          index = 0;
          loopStart += durationSec;
          this.bgmLoopStart = loopStart;
        }
        const event = events[index];
        const when = loopStart + event.startSec;
        if (when > horizon) {
          return;
        }
        const nodes = this.scheduleNote(ctx, this.bgmBus!, event, Math.max(when, ctx.currentTime), true);
        for (const node of nodes) {
          this.activeBgmNodes.add(node);
          node.onended = () => this.activeBgmNodes.delete(node);
        }
        index++;
      }
    };

    scheduleAhead();
    this.bgmLoopHandle = window.setInterval(scheduleAhead, SCHEDULE_INTERVAL_MS);
  }

  /** true にすると、録音音源を使わず合成音だけで鳴らす（音の聴き比べ用）。鳴っている曲は同じ位置から切り替える。 */
  setSynthOnly(value: boolean): void {
    if (this.synthOnly === value) {
      return;
    }
    this.synthOnly = value;
    if (this.currentBgm && this.bgmLoopHandle !== null) {
      this.playBgm(this.currentBgm, this.getBgmPositionSec());
    }
  }

  /** 録音音源の準備ができているか（BGMプレイヤーの表示用）。 */
  isSampledReady(): boolean {
    return this.sampled.isReady();
  }

  /** いま鳴っているBGMの、曲の中での位置（秒）。鳴っていなければ0。 */
  getBgmPositionSec(): number {
    if (this.sampled.isPlaying()) {
      return this.sampled.positionSec();
    }
    if (!this.ctx || this.bgmLoopHandle === null || this.bgmDurationSec <= 0) {
      return 0;
    }
    const pos = this.ctx.currentTime - this.bgmLoopStart;
    return Math.max(0, pos % this.bgmDurationSec);
  }

  stopBgm(): void {
    this.sampled.stop();
    if (this.bgmLoopHandle !== null) {
      if (this.bgmLoopHandle >= 0) {
        window.clearInterval(this.bgmLoopHandle);
      }
      this.bgmLoopHandle = null;
    }
    for (const node of this.activeBgmNodes) {
      try {
        node.stop();
      } catch {
        // すでに再生が終わっているノードは無視する。
      }
    }
    this.activeBgmNodes.clear();
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
