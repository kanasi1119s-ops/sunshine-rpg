// 作曲ソフトの録音: オーディオインターフェース（マイク・ギターのライン入力など）から、実際の楽器を録る。
// 録った音は FLAC（音質そのまま）で曲の中に入れ、再生・書き出しのときはアンプを通して鳴らす。
import { AmpRack } from "../../src/audio/amp-rack";
import { configureAudioRack, scheduleAudioTracks } from "../../src/audio/audio-clips";
import type { NamHost } from "../../src/audio/nam/nam-host";
import type { AmpSetting, Score } from "../../src/audio/score";

/** 録音用のワークレット（入ってきた音を、そのままメインへ送る）。 */
const RECORDER_CODE = `
class SunshineRecorder extends AudioWorkletProcessor {
  constructor() { super(); this.on = true; this.port.onmessage = (e) => { if (e.data === "stop") this.on = false; }; this.buf = []; this.n = 0; }
  process(inputs) {
    const input = inputs[0];
    if (!this.on) return false;
    if (input && input.length) {
      this.buf.push(input.map((c) => c.slice(0)));
      this.n++;
      if (this.n >= 16) { this.port.postMessage(this.buf); this.buf = []; this.n = 0; }
    }
    return true;
  }
}
registerProcessor("sunshine-recorder", SunshineRecorder);
`;
const RECORDER_URL = `data:text/javascript;base64,${btoa(RECORDER_CODE)}`;

export type InputMode = "in1" | "in2" | "stereo";

export interface InputDevice {
  id: string;
  label: string;
}

/** 使える入力（オーディオインターフェース・マイク）の一覧。はじめて使うときは、許可を求める。 */
export async function listInputs(): Promise<InputDevice[]> {
  if (!navigator.mediaDevices?.getUserMedia) throw new Error("このブラウザでは録音できません（Chrome・Edge・デスクトップ版で使えます）");
  // 名前を見るには、いちど許可をもらう必要がある
  const probe = await navigator.mediaDevices.getUserMedia({ audio: true });
  probe.getTracks().forEach((t) => t.stop());
  const devices = await navigator.mediaDevices.enumerateDevices();
  return devices.filter((d) => d.kind === "audioinput").map((d, i) => ({ id: d.deviceId, label: d.label || `入力 ${i + 1}` }));
}

const loaded = new WeakSet<BaseAudioContext>();

export interface LiveInput {
  /** 入力の音（モノラル化・チャンネル選びのあと）。 */
  node: AudioNode;
  /** モニター（録りながら、アンプを通した音を聞く）を切り替える。 */
  setMonitor(on: boolean, amp: AmpSetting | undefined, score: Score): void;
  close(): void;
  channels: number;
}

/** 入力を開く（楽器の音を、そのまま取り込む。エコー消し・雑音消し・音量の自動調整は切る）。 */
export async function openInput(ctx: AudioContext, deviceId: string, mode: InputMode, destination: AudioNode, nam: NamHost | null): Promise<LiveInput> {
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: { deviceId: deviceId ? { exact: deviceId } : undefined, echoCancellation: false, noiseSuppression: false, autoGainControl: false, channelCount: { ideal: 2 } },
  });
  const src = ctx.createMediaStreamSource(stream);
  const split = ctx.createChannelSplitter(2);
  src.connect(split);
  let node: AudioNode;
  if (mode === "stereo") {
    node = src;
  } else {
    // 入力1（左）か入力2（右）だけを、真ん中のモノラルにする
    const mono = ctx.createGain();
    mono.channelCount = 1;
    mono.channelCountMode = "explicit";
    split.connect(mono, mode === "in1" ? 0 : 1);
    node = mono;
  }
  let monitorRack: AmpRack | null = null;
  let monitorGain: GainNode | null = null;
  return {
    node,
    channels: mode === "stereo" ? 2 : 1,
    setMonitor(on, amp, score) {
      monitorGain?.disconnect();
      monitorGain = null;
      if (!on) return;
      monitorRack ??= new AmpRack(ctx, destination);
      monitorRack.setNam(nam);
      configureAudioRack(monitorRack, { ...score, audioTracks: [{ name: "monitor", volume: 1, pan: 0, amp, clips: [] }] });
      monitorGain = ctx.createGain();
      node.connect(monitorGain);
      monitorGain.connect(monitorRack.input(0));
    },
    close() {
      monitorGain?.disconnect();
      src.disconnect();
      stream.getTracks().forEach((t) => t.stop());
    },
  };
}

export interface Recording {
  stop(): Promise<{ channels: Float32Array[]; sampleRate: number }>;
}

/** 録音を始める。stop で、録った音（チャンネルごとの並び）を返す。 */
export async function startRecording(ctx: AudioContext, input: LiveInput): Promise<Recording> {
  if (!loaded.has(ctx)) {
    await ctx.audioWorklet.addModule(RECORDER_URL);
    loaded.add(ctx);
  }
  const rec = new AudioWorkletNode(ctx, "sunshine-recorder", { numberOfInputs: 1, numberOfOutputs: 0, channelCount: input.channels, channelCountMode: "explicit" });
  const parts: Float32Array[][] = [];
  rec.port.onmessage = (e: MessageEvent<Float32Array[][]>) => parts.push(...e.data);
  input.node.connect(rec);
  return {
    async stop() {
      rec.port.postMessage("stop");
      await new Promise((r) => window.setTimeout(r, 120));
      input.node.disconnect(rec);
      rec.port.onmessage = null;
      const n = input.channels;
      const len = parts.reduce((s, p) => s + p[0].length, 0);
      const channels = Array.from({ length: n }, () => new Float32Array(len));
      let at = 0;
      for (const p of parts) {
        for (let c = 0; c < n; c++) channels[c].set(p[c] ?? p[0], at);
        at += p[0].length;
      }
      return { channels, sampleRate: ctx.sampleRate };
    },
  };
}

/**
 * 再生中に、録音トラックの音をいっしょに鳴らす。
 * 録音音源の再生（シーケンサー）の位置に合わせて予約し、曲がくり返したら、予約し直す。
 */
export class ClipPlayer {
  private stopFns: (() => void)[] = [];
  private rack: AmpRack | null = null;
  private lastPos = 0;
  private lastAt = 0;
  private active = false;
  private score: Score | null = null;

  constructor(private ctx: () => AudioContext, private destination: () => AudioNode, private position: () => number, private nam: () => NamHost | null) {}

  start(score: Score): void {
    this.stop();
    if (!score.audioTracks?.some((t) => t.clips.length)) return;
    this.score = score;
    this.active = true;
    this.lastPos = -1;
  }

  /** 画面の更新のたびに呼ぶ。曲の頭がどこにあるかを見て、予約する。 */
  tick(playing: boolean): void {
    if (!this.active || !this.score) return;
    if (!playing) {
      this.stop();
      return;
    }
    const pos = this.position();
    const now = this.ctx().currentTime;
    if (pos <= 0.02 && this.lastPos < 0) return; // まだ鳴りはじめていない
    const expected = this.lastPos + (now - this.lastAt);
    if (this.lastPos < 0 || Math.abs(pos - expected) > 0.35) {
      // 鳴りはじめた・曲の頭にもどった・位置を動かした: 今の位置から予約し直す
      this.clear();
      const ctx = this.ctx();
      if (!this.rack) {
        this.rack = new AmpRack(ctx, this.destination());
      }
      this.rack.setNam(this.nam());
      configureAudioRack(this.rack, this.score);
      const songStartAt = ctx.currentTime - pos;
      void scheduleAudioTracks(ctx, this.score, this.rack, songStartAt, pos).then((fn) => {
        if (this.active) this.stopFns.push(fn);
        else fn();
      });
    }
    this.lastPos = pos;
    this.lastAt = now;
  }

  private clear(): void {
    for (const f of this.stopFns) f();
    this.stopFns = [];
  }

  stop(): void {
    this.active = false;
    this.clear();
  }
}
