import { describe, expect, it } from "vitest";
import { AmpRack, GENRE_AMP_TYPES, stepCurve } from "./amp-rack";
import type { AmpSetting, GenreAmpType } from "./score";

/** つなぎ方だけを記録する、Web Audio の部品の偽物。 */
class FakeParam {
  value = 0;
}
class FakeNode {
  outputs: FakeNode[] = [];
  gain = new FakeParam();
  frequency = new FakeParam();
  Q = new FakeParam();
  threshold = new FakeParam();
  knee = new FakeParam();
  ratio = new FakeParam();
  attack = new FakeParam();
  release = new FakeParam();
  pan = new FakeParam();
  type = "";
  curve: Float32Array | null = null;
  oversample = "none";
  constructor(public kind: string) {}
  connect(n: FakeNode): FakeNode {
    this.outputs.push(n);
    return n;
  }
  disconnect(): void {
    this.outputs = [];
  }
}
class FakeCtx {
  destination = new FakeNode("destination");
  createGain = () => new FakeNode("gain");
  createBiquadFilter = () => new FakeNode("biquad");
  createWaveShaper = () => new FakeNode("waveshaper");
  createDynamicsCompressor = () => new FakeNode("compressor");
  createStereoPanner = () => new FakeNode("panner");
}

/** 入口から出口までたどって、通った部品を返す。 */
function walk(from: FakeNode): FakeNode[] {
  const path: FakeNode[] = [];
  let n = from;
  while (n.outputs.length > 0) {
    n = n.outputs[0];
    path.push(n);
  }
  return path;
}

function rackWith(type: AmpSetting["type"]) {
  const ctx = new FakeCtx();
  const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
  rack.configure({ 0: 30 }, "rock", 9, { 0: { amp: { type }, pan: 0 } });
  return { ctx, path: walk(rack.input(0) as unknown as FakeNode) };
}

describe("stepCurve（階段状の波形）", () => {
  it("値は -1〜1 で、段の数だけ違う値になり、真ん中は0", () => {
    const c = stepCurve(4);
    expect(c.length % 2).toBe(1);
    expect(c[(c.length - 1) / 2]).toBe(0);
    expect(c[0]).toBe(-1);
    expect(c[c.length - 1]).toBe(1);
    expect(new Set(Array.from(c)).size).toBe(9);
  });
});

describe("ジャンル別のアンプ", () => {
  it("14種類ある", () => {
    expect(GENRE_AMP_TYPES).toHaveLength(14);
    expect(new Set(GENRE_AMP_TYPES).size).toBe(14);
  });

  it.each(GENRE_AMP_TYPES)("%s: 入口から出口（最終出力）までつながり、素通しではない", (type: GenreAmpType) => {
    const { path, ctx } = rackWith(type);
    expect(path[path.length - 1]).toBe(ctx.destination);
    // フィルターを2つ以上通る（音づくりがされている）
    expect(path.filter((n) => n.kind === "biquad").length).toBeGreaterThanOrEqual(2);
  });

  it("歪ませるジャンルは歪みの部品（ウェーブシェイパー）を通り、4倍オーバーサンプリングで濁りを抑える", () => {
    for (const type of ["blues", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "radio", "loudmetal", "loudrock"] as const) {
      const shapers = rackWith(type).path.filter((n) => n.kind === "waveshaper");
      expect(shapers.length, type).toBeGreaterThanOrEqual(1);
      expect(shapers[0].oversample, type).toBe("4x");
    }
  });

  it("ローファイとレトロ8bitは、階段状の波形を通る", () => {
    for (const type of ["lofi", "retro8bit"] as const) {
      const curves = rackWith(type).path.filter((n) => n.kind === "waveshaper").map((n) => n.curve!);
      expect(curves.some((c) => new Set(Array.from(c)).size < 60), type).toBe(true);
    }
  });

  it("ラジオは400Hzより低い音と3kHzより高い音を削る", () => {
    const f = rackWith("radio").path.filter((n) => n.kind === "biquad");
    expect(f.some((n) => n.type === "highpass" && n.frequency.value === 400)).toBe(true);
    expect(f.some((n) => n.type === "lowpass" && n.frequency.value === 3000)).toBe(true);
  });

  it("これまでの種類（オーバードライブ）のつなぎ方は変わらない", () => {
    const od = rackWith("overdrive").path;
    expect(od.filter((n) => n.kind === "waveshaper")).toHaveLength(1);
    expect(od[od.length - 1].kind).toBe("destination");
  });
});
