import { describe, expect, it } from "vitest";
import { AmpRack } from "./amp-rack";
import { aiSongToScore } from "./ai-song";
import { buildFx, buildFxChain, FX_INFO, FX_TYPES, type FxSpec } from "./fx-chain";
import { biquadCoefficients, buildExtraFx, cabImpulse, registerCabIr, EXTRA_FX_INFO, EXTRA_FX_TYPES, magnitudeAt, rectifierCurve, springImpulse, tapeSaturationCurve } from "./fx-extra";
import { scoreToMidiInfo } from "./midi-export";

/** つなぎ方だけを記録する、Web Audio の部品の偽物（どんな createXxx にも、接続できる部品を返す）。 */
class FakeParam {
  value = 0;
}
class FakeNode {
  outputs: FakeNode[] = [];
  buffer: { data: Float32Array[] } | null = null;
  [k: string]: unknown;
  constructor(public kind: string) {
    for (const p of ["gain", "frequency", "Q", "delayTime", "threshold", "knee", "ratio", "attack", "release", "pan"]) this[p] = new FakeParam();
  }
  connect(n: FakeNode): FakeNode {
    this.outputs.push(n);
    return n;
  }
  disconnect(): void {
    this.outputs = [];
  }
  start(): void {}
  stop(): void {}
}
function fakeCtx() {
  const created: FakeNode[] = [];
  const make = (kind: string) => () => {
    const n = new FakeNode(kind);
    created.push(n);
    return n;
  };
  const ctx = {
    sampleRate: 48000,
    destination: new FakeNode("destination"),
    createGain: make("gain"),
    createBiquadFilter: make("biquad"),
    createWaveShaper: make("waveshaper"),
    createDynamicsCompressor: make("compressor"),
    createStereoPanner: make("panner"),
    createDelay: make("delay"),
    createOscillator: make("oscillator"),
    createConvolver: make("convolver"),
    createBuffer: (ch: number, len: number) => ({ numberOfChannels: ch, length: len, getChannelData: (i: number) => (buffers[`${ch}:${len}`] ??= Array.from({ length: ch }, () => new Float32Array(len)))[i] }),
  };
  const buffers: Record<string, Float32Array[]> = {};
  return { ctx, created };
}

describe("追加のエフェクター（fx-extra）", () => {
  it("9種類すべてが FX_TYPES・FX_INFO にあり、日本語の名前がある", () => {
    expect(EXTRA_FX_TYPES.length).toBe(9);
    for (const t of EXTRA_FX_TYPES) {
      expect(FX_TYPES).toContain(t);
      expect(FX_INFO[t].label.length).toBeGreaterThan(0);
      expect(EXTRA_FX_INFO[t].use.length).toBeGreaterThan(0);
      expect(FX_INFO[t].mix).toBeGreaterThanOrEqual(0);
      expect(FX_INFO[t].mix).toBeLessThanOrEqual(1);
    }
  });

  it("どの種類も、入口と出口のある部品を組み立てられる（知らない種類は null）", () => {
    for (const t of EXTRA_FX_TYPES) {
      const { ctx } = fakeCtx();
      const built = buildFx(ctx as unknown as BaseAudioContext, { type: t });
      expect(built.input).toBeTruthy();
      expect(built.output).toBeTruthy();
      expect(built.nodes.length).toBeGreaterThan(0);
    }
    const { ctx } = fakeCtx();
    expect(buildExtraFx(ctx as unknown as BaseAudioContext, { type: "delay" }, 0.2)).toBeNull();
  });

  it("テープディレイは、くり返しの道に高音を丸める部品と飽和の部品を持ち、遅れの時間がゆれる", () => {
    const { ctx, created } = fakeCtx();
    buildFx(ctx as unknown as BaseAudioContext, { type: "tape", ms: 400, feedback: 0.5, tone: 2400 });
    const lows = created.filter((n) => n.kind === "biquad");
    expect(lows.some((n) => (n.frequency as FakeParam).value === 2400)).toBe(true);
    expect(created.filter((n) => n.kind === "waveshaper").length).toBe(1);
    expect(created.filter((n) => n.kind === "oscillator").length).toBe(2); // ワウ＋フラッター
    expect((created.find((n) => n.kind === "delay")!.delayTime as FakeParam).value).toBeCloseTo(0.4, 6);
  });

  it("ロータリーは、高音と低音の2つの回転（ホーン・ドラム）を持ち、ドラムはホーンより少し遅い", () => {
    const { ctx, created } = fakeCtx();
    buildFx(ctx as unknown as BaseAudioContext, { type: "rotary", rate: 6.7 });
    const oscs = created.filter((n) => n.kind === "oscillator").map((n) => (n.frequency as FakeParam).value);
    expect(oscs.length).toBe(6); // 2つの回転 × （遅れ・音量・左右）
    expect(Math.max(...oscs)).toBeCloseTo(6.7, 5);
    expect(Math.min(...oscs)).toBeCloseTo(6.7 * 0.85, 5);
  });

  it("ステレオ・ダブラーは左右に別々の遅れと別々のゆれを持つ", () => {
    const { ctx, created } = fakeCtx();
    buildFx(ctx as unknown as BaseAudioContext, { type: "doubler", ms: 14 });
    const delays = created.filter((n) => n.kind === "delay").map((n) => (n.delayTime as FakeParam).value);
    expect(delays[0]).toBeCloseTo(0.014, 6);
    expect(delays[1]).toBeCloseTo(0.021, 6);
    const pans = created.filter((n) => n.kind === "panner").map((n) => (n.pan as FakeParam).value);
    expect(pans.sort()).toEqual([-0.9, 0.9]);
  });

  it("パラレルコンプは、元の音をそのまま通しつつ（引かない）、潰した音を足す", () => {
    const { ctx, created } = fakeCtx();
    const built = buildFx(ctx as unknown as BaseAudioContext, { type: "pcomp", threshold: -30, ratio: 12, attack: 0.004, release: 0.2 });
    const comp = created.find((n) => n.kind === "compressor")!;
    expect((comp.threshold as FakeParam).value).toBe(-30);
    expect((comp.attack as FakeParam).value).toBeCloseTo(0.004, 6);
    expect((comp.release as FakeParam).value).toBeCloseTo(0.2, 6);
    // 元の音の道が残っている（コンプの先読み 6ms と同じだけ遅らせて、足したときに打ち消し合わないようにする）
    const dryDelay = created.find((n) => n.kind === "delay")!;
    expect((dryDelay.delayTime as FakeParam).value).toBeCloseTo(0.006, 6);
    expect((built.input as unknown as FakeNode).outputs).toContain(dryDelay);
    expect(dryDelay.outputs).toContain(built.output as unknown as FakeNode);
  });

  it("compressor に attack／release を書ける（省略は従来どおり 12ms／200ms）", () => {
    const a = fakeCtx();
    buildFx(a.ctx as unknown as BaseAudioContext, { type: "compressor" });
    const ca = a.created.find((n) => n.kind === "compressor")!;
    expect((ca.attack as FakeParam).value).toBeCloseTo(0.012, 6);
    expect((ca.release as FakeParam).value).toBeCloseTo(0.2, 6);
    const b = fakeCtx();
    buildFx(b.ctx as unknown as BaseAudioContext, { type: "compressor", attack: 0.005, release: 0.05 });
    const cb = b.created.find((n) => n.kind === "compressor")!;
    expect((cb.attack as FakeParam).value).toBeCloseTo(0.005, 6);
    expect((cb.release as FakeParam).value).toBeCloseTo(0.05, 6);
  });

  it("直列に9個つないでも壊れない", () => {
    const { ctx } = fakeCtx();
    const specs: FxSpec[] = EXTRA_FX_TYPES.map((type) => ({ type }));
    const chain = buildFxChain(ctx as unknown as BaseAudioContext, specs);
    expect(chain).not.toBeNull();
    expect(chain!.nodes.length).toBeGreaterThan(20);
  });
});

describe("純粋な関数（Web Audio なし）", () => {
  it("スプリングのインパルス: 往復ごとに戻りが来て、だんだん小さくなり、同じ種なら同じ", () => {
    const sr = 48000;
    const ir = springImpulse(sr, { roundTrip: 0.034, seconds: 1.2, seed: 7 });
    expect(ir.length).toBe(Math.floor(sr * 1.2));
    const rms = (from: number, to: number): number => {
      let s = 0;
      for (let i = Math.floor(from * sr); i < Math.floor(to * sr); i++) s += ir[i] * ir[i];
      return Math.sqrt(s / ((to - from) * sr));
    };
    // 最初の戻り（34ms〜60ms）は、その前の空白（0〜30ms）よりずっと強い
    expect(rms(0.034, 0.06)).toBeGreaterThan(rms(0, 0.03) * 5);
    // 後ろの方ほど小さい
    expect(rms(0.034, 0.2)).toBeGreaterThan(rms(0.8, 1.0));
    const again = springImpulse(sr, { roundTrip: 0.034, seconds: 1.2, seed: 7 });
    expect(Array.from(again.slice(2000, 2010))).toEqual(Array.from(ir.slice(2000, 2010)));
    expect(ir.every(Number.isFinite)).toBe(true);
  });

  it("バイクアッド係数: ローパスは低い音を通し、高い音を落とす", () => {
    const sr = 48000;
    const c = biquadCoefficients("lowpass", 2000, 0, 0.7, sr);
    // 直流の大きさ = (b0+b1+b2)/(1+a1+a2) が 1
    expect((c.b0 + c.b1 + c.b2) / (1 + c.a1 + c.a2)).toBeCloseTo(1, 6);
    const ir = new Float32Array(1024);
    let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    for (let n = 0; n < ir.length; n++) {
      const x = n === 0 ? 1 : 0;
      const y = c.b0 * x + c.b1 * x1 + c.b2 * x2 - c.a1 * y1 - c.a2 * y2;
      x2 = x1; x1 = x; y2 = y1; y1 = y;
      ir[n] = y;
    }
    expect(magnitudeAt(ir, 200, sr)).toBeGreaterThan(0.95);
    expect(magnitudeAt(ir, 8000, sr)).toBeLessThan(0.1);
  });

  it("キャビネットIR: 1kHz で大きさ1にそろい、高い音ほど落ち、有限の値だけ", () => {
    const sr = 48000;
    for (const kind of ["closed", "open", "dark", "bright"] as const) {
      for (const mic of ["center", "edge", "off", "far"] as const) {
        const ir = cabImpulse(sr, kind, mic);
        expect(ir.every(Number.isFinite)).toBe(true);
        expect(magnitudeAt(ir, 1000, sr)).toBeCloseTo(1, 3);
        expect(magnitudeAt(ir, 9000, sr)).toBeLessThan(magnitudeAt(ir, 1000, sr) * 0.35);
      }
    }
    // 暗い箱は、明るい箱より 5kHz が小さい
    expect(magnitudeAt(cabImpulse(sr, "dark"), 5000, sr)).toBeLessThan(magnitudeAt(cabImpulse(sr, "bright"), 5000, sr));
  });

  it("整流の曲線は、負の入力も正にする（オクターブ上の元）", () => {
    const c = rectifierCurve(2049, 3);
    expect(c[0]).toBeCloseTo(c[c.length - 1], 6);
    expect(c[(c.length - 1) / 2]).toBeCloseTo(0, 6);
    expect(Math.min(...Array.from(c))).toBeGreaterThanOrEqual(0);
  });

  it("テープの飽和は、小さい音の傾きがほぼ 1（くり返しが増えない）で、大きい音だけ丸まる", () => {
    const c = tapeSaturationCurve(2049, 1.4);
    const mid = (c.length - 1) / 2;
    const slope = (c[mid + 5] - c[mid]) / (5 / mid);
    expect(slope).toBeGreaterThan(0.97);
    expect(slope).toBeLessThan(1.03);
    expect(c[c.length - 1]).toBeLessThan(0.7); // 全開の音は丸まる
    expect(c[0]).toBeCloseTo(-c[c.length - 1], 6);
  });
});

describe("pre: true（アンプの前につなぐ）", () => {
  const base = { title: "ペダル", description: "テスト", bpm: 120, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock" } as const;

  it("AIソングの fx に pre: true と attack／release を書くと、そのまま通る", () => {
    const { score } = aiSongToScore({ ...base, parts: [{ instrument: "leadGuitar", role: "メロディ", volume: 0.3, notes: "C4:4 D4:4", fx: [{ type: "tubescreamer", pre: true, gain: 8 }, { type: "compressor", attack: 0.005, release: 0.05 }, { type: "octup" }] }] });
    const fx = score.tracks[0].fx!;
    expect(fx[0]).toMatchObject({ type: "tubescreamer", pre: true });
    expect(fx[1]).toMatchObject({ type: "compressor", attack: 0.005, release: 0.05 });
    expect(fx[2].type).toBe("octup");
    expect(Object.values(scoreToMidiInfo(score).fx)[0][0].pre).toBe(true);
  });

  it("pre の fx は入口とアンプのあいだ、pre でない fx はアンプと出口のあいだに入る", () => {
    const { ctx } = fakeCtx();
    const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
    const fx: Record<number, FxSpec[]> = { 0: [{ type: "boost", pre: true, gain: 6 }, { type: "plate" }] };
    rack.configure({ 0: 30 }, "rock", 9, { 0: { amp: { type: "overdrive" }, pan: 0 } }, {}, {}, fx);
    // 入口からたどる（最初の出力だけ）。ブースター（pre）の1個目の部品が先頭に来て、最後は出口に着く
    let n = rack.input(0) as unknown as FakeNode;
    const kinds: string[] = [];
    const seen = new Set<FakeNode>();
    while (n.outputs.length > 0 && !seen.has(n)) {
      seen.add(n);
      n = n.outputs[0];
      kinds.push(n.kind);
    }
    expect(kinds[kinds.length - 1]).toBe("destination");
    expect(kinds[0]).toBe("gain"); // pre のブースターの入口
    expect(kinds).toContain("waveshaper"); // アンプの歪み
    expect(kinds.indexOf("waveshaper")).toBeGreaterThan(1);
  });

  it("pre だけの fx でも、アンプのあとの道は出口へ直接つながる", () => {
    const { ctx } = fakeCtx();
    const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
    rack.configure({ 0: 29 }, "rock", 9, {}, {}, {}, { 0: [{ type: "fuzz", pre: true }] });
    let n = rack.input(0) as unknown as FakeNode;
    let hops = 0;
    while (n.outputs.length > 0 && hops < 100) {
      n = n.outputs[0];
      hops++;
    }
    expect(n.kind).toBe("destination");
  });
});

describe("歪み系アンプの標準の録音キャビネットIR（2026-10-15）", () => {
  const kindsFrom = (rack: AmpRack, ch: number): string[] => {
    const all: string[] = [];
    const walk = (n: FakeNode, depth: number): void => {
      if (depth > 200) return;
      for (const o of n.outputs) { all.push(o.kind); walk(o, depth + 1); }
    };
    walk(rack.input(ch) as unknown as FakeNode, 0);
    return all;
  };
  it("IR が登録されていれば hardrock の後ろに畳み込みが入り、ampCabIr: none なら入らない", () => {
    registerCabIr("dfc-bestplugins", new Float32Array([1, 0.5, 0.25, 0]), 44100);
    const { ctx } = fakeCtx();
    const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
    rack.configure({ 0: 30, 1: 30 }, "rock", 9, { 0: { amp: { type: "hardrock" }, pan: 0 }, 1: { amp: { type: "hardrock", cabIr: "none" }, pan: 0 } });
    expect(kindsFrom(rack, 0)).toContain("convolver");
    expect(kindsFrom(rack, 1)).not.toContain("convolver");
  });
});
