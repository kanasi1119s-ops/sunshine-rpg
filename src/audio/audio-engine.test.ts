import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AudioEngine } from "./audio-engine";
import { REST, type Score } from "./score";

/** Web Audio の部品の代わりになる、つなぎ方だけを記録する偽物。 */
class FakeParam {
  value = 0;
  setValueAtTime(): void {}
  linearRampToValueAtTime(): void {}
}

class FakeNode {
  static all: FakeNode[] = [];
  kind: string;
  outputs: FakeNode[] = [];
  disconnected = false;
  gain = new FakeParam();
  frequency = new FakeParam();
  Q = new FakeParam();
  type = "";
  curve: Float32Array | null = null;
  oversample = "none";
  constructor(kind: string) {
    this.kind = kind;
    FakeNode.all.push(this);
  }
  connect(target: FakeNode): FakeNode {
    this.outputs.push(target);
    return target;
  }
  disconnect(): void {
    this.disconnected = true;
  }
  start(): void {}
  stop(): void {}
}

class FakeAudioContext {
  currentTime = 0;
  state = "running";
  destination = new FakeNode("destination");
  resume(): Promise<void> {
    return Promise.resolve();
  }
  createGain(): FakeNode {
    return new FakeNode("gain");
  }
  createOscillator(): FakeNode {
    return new FakeNode("oscillator");
  }
  createWaveShaper(): FakeNode {
    return new FakeNode("waveshaper");
  }
  createBiquadFilter(): FakeNode {
    return new FakeNode("biquad");
  }
}

function makeScore(withAmp: boolean): Score {
  return {
    tempoBpm: 120,
    loop: false,
    tracks: [
      {
        waveform: "sawtooth",
        volume: 0.2,
        notes: [
          { note: "A2", durationBeats: 1 },
          { note: REST, durationBeats: 1 },
        ],
        ...(withAmp ? { amp: "metal" as const } : {}),
      },
      {
        waveform: "triangle",
        volume: 0.2,
        notes: [{ note: "A1", durationBeats: 2 }],
      },
    ],
  };
}

describe("AudioEngine のアンプ接続", () => {
  beforeEach(() => {
    FakeNode.all = [];
    vi.stubGlobal("AudioContext", FakeAudioContext);
    vi.stubGlobal("window", { setInterval: () => 1, clearInterval: () => {} });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  const oscillators = () => FakeNode.all.filter((n) => n.kind === "oscillator");
  /** 音（オシレーター）の先の、音量ゲインの行き先。 */
  const targetOf = (osc: FakeNode) => osc.outputs[0].outputs[0];

  it("アンプの指定があるパートは、歪み・イコライザー・キャビネットを通ってBGMの音量へ出る", () => {
    const engine = new AudioEngine();
    engine.playBgm(makeScore(true));

    const shapers = FakeNode.all.filter((n) => n.kind === "waveshaper");
    expect(shapers).toHaveLength(1);
    expect(shapers[0].oversample).toBe("4x");
    expect(shapers[0].curve).not.toBeNull();

    // オシレーター2つのうち、ノコギリ波（アンプあり）の行き先はアンプの入力ゲイン。
    const [amped, plain] = oscillators();
    const ampInput = targetOf(amped);
    expect(ampInput.outputs[0]).toBe(shapers[0]);

    // 三角波（アンプなし）の行き先は、BGM音量のゲイン（アンプの入力ではない）。
    expect(targetOf(plain)).not.toBe(ampInput);
    expect(targetOf(plain).kind).toBe("gain");

    // アンプの出口は、BGM音量のゲインにつながる。
    let node: FakeNode = shapers[0];
    const kinds: string[] = [];
    while (node.outputs.length > 0) {
      node = node.outputs[0];
      kinds.push(node.kind);
    }
    // 低音・中音・高音・低域カット・高域カット → アンプの出力ゲイン → BGM音量のゲイン → 最終出力
    expect(kinds).toEqual(["biquad", "biquad", "biquad", "biquad", "biquad", "gain", "gain", "destination"]);
  });

  it("アンプの指定がないパートだけの曲では、アンプ（歪み）を作らない（既存の曲は今までどおり）", () => {
    const engine = new AudioEngine();
    engine.playBgm(makeScore(false));
    expect(FakeNode.all.filter((n) => n.kind === "waveshaper")).toHaveLength(0);
  });

  it("同じプリセットのパートが複数あっても、アンプは1台だけ作って共有する", () => {
    const engine = new AudioEngine();
    const score = makeScore(true);
    score.tracks.push({ ...score.tracks[0], notes: [{ note: "E3", durationBeats: 2 }] });
    engine.playBgm(score);
    expect(FakeNode.all.filter((n) => n.kind === "waveshaper")).toHaveLength(1);
  });

  it("BGMを止めると、アンプの部品も切り離す", () => {
    const engine = new AudioEngine();
    engine.playBgm(makeScore(true));
    const shaper = FakeNode.all.find((n) => n.kind === "waveshaper")!;
    expect(shaper.disconnected).toBe(false);
    engine.stopBgm();
    expect(shaper.disconnected).toBe(true);
  });

  it("効果音（playSe）でもアンプを通せる", () => {
    const engine = new AudioEngine();
    engine.playSe(makeScore(true));
    expect(FakeNode.all.filter((n) => n.kind === "waveshaper")).toHaveLength(1);
  });
});
