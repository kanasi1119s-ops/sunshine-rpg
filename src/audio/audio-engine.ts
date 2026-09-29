import {
  AMP_CURVE_SAMPLES,
  AMP_REFERENCE_VOLUME,
  getAmpSettings,
  makeDistortionCurve,
  type AmpPresetName,
} from "./amp";
import { flattenScore, getScoreDurationSec, type Score, type ScheduledNote } from "./score";

const SCHEDULE_AHEAD_SEC = 3;
const SCHEDULE_INTERVAL_MS = 1000;

/** アンプ1台ぶんの部品。`input` に音をつなぐと、アンプを通って `destination` へ出る。 */
interface AmpChain {
  input: AudioNode;
  nodes: AudioNode[];
}

/**
 * アンプシミュレーターの部品をつなぐ（`amp.ts` の設定に沿う）。
 * 入力ゲイン（ドライブ） → 歪み → 低音・中音・高音 → 低域カット → 高域カット → 出力ゲイン → destination
 */
function buildAmpChain(ctx: AudioContext, name: AmpPresetName, destination: AudioNode): AmpChain {
  const s = getAmpSettings(name);

  const input = ctx.createGain();
  input.gain.value = s.drive / AMP_REFERENCE_VOLUME;

  const shaper = ctx.createWaveShaper();
  shaper.curve = makeDistortionCurve(s.shape, s.hardness, s.asymmetry, AMP_CURVE_SAMPLES);
  // 歪みで生まれる高い倍音が折り返して濁るのを、和らげる。
  shaper.oversample = "4x";

  const bass = ctx.createBiquadFilter();
  bass.type = "lowshelf";
  bass.frequency.value = 200;
  bass.gain.value = s.bassDb;

  const mid = ctx.createBiquadFilter();
  mid.type = "peaking";
  mid.frequency.value = s.midHz;
  mid.Q.value = 0.9;
  mid.gain.value = s.midDb;

  const treble = ctx.createBiquadFilter();
  treble.type = "highshelf";
  treble.frequency.value = 3000;
  treble.gain.value = s.trebleDb;

  const cabHigh = ctx.createBiquadFilter();
  cabHigh.type = "highpass";
  cabHigh.frequency.value = s.highpassHz;

  const cabLow = ctx.createBiquadFilter();
  cabLow.type = "lowpass";
  cabLow.frequency.value = s.lowpassHz;

  // 歪みの前に大きく増幅した分を、基準の音量に戻す（出力は最大でも基準の音量×level）。
  const output = ctx.createGain();
  output.gain.value = AMP_REFERENCE_VOLUME * s.level;

  const nodes: AudioNode[] = [input, shaper, bass, mid, treble, cabHigh, cabLow, output];
  for (let i = 0; i < nodes.length - 1; i++) {
    nodes[i].connect(nodes[i + 1]);
  }
  output.connect(destination);
  return { input, nodes };
}

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
  /** 今のBGMが使っているアンプ（曲を止めるときに切り離す）。 */
  private activeBgmAmps: AmpChain[] = [];

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

  /** 音の行き先を決める。アンプの指定があれば、そのアンプを（なければ作って）通す。 */
  private destinationFor(
    ctx: AudioContext,
    amps: Map<AmpPresetName, AmpChain>,
    event: ScheduledNote,
    fallback: GainNode,
  ): AudioNode {
    if (event.amp === undefined) {
      return fallback;
    }
    let chain = amps.get(event.amp);
    if (!chain) {
      chain = buildAmpChain(ctx, event.amp, fallback);
      amps.set(event.amp, chain);
    }
    return chain.input;
  }

  private scheduleNote(
    ctx: AudioContext,
    destination: AudioNode,
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
    const amps = new Map<AmpPresetName, AmpChain>();
    for (const event of events) {
      const destination = this.destinationFor(ctx, amps, event, this.seGain!);
      this.scheduleNote(ctx, destination, event, ctx.currentTime);
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
    const amps = new Map<AmpPresetName, AmpChain>();

    const scheduleAhead = (): void => {
      while (nextStart < ctx.currentTime + SCHEDULE_AHEAD_SEC) {
        const events = flattenScore(score);
        for (const event of events) {
          const destination = this.destinationFor(ctx, amps, event, this.bgmGain!);
          const node = this.scheduleNote(ctx, destination, event, nextStart + event.startSec);
          this.activeBgmNodes.push(node);
        }
        nextStart += durationSec;
        this.activeBgmAmps = [...amps.values()];
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
    for (const amp of this.activeBgmAmps) {
      for (const node of amp.nodes) {
        node.disconnect();
      }
    }
    this.activeBgmAmps = [];
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
