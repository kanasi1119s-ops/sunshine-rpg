import { describe, expect, it } from "vitest";
import { AmpRack, GENRE_AMP_TYPES, stepCurve } from "./amp-rack";
import { cabApproxSpec, CAB_KINDS, MIC_POSITIONS } from "./amp-cab";
import { CURVE_KINDS, shapeCurve } from "./amp-curves";
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

function rackWith(type: AmpSetting["type"], extra: Partial<AmpSetting> = {}) {
  const ctx = new FakeCtx();
  const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
  rack.configure({ 0: 30 }, "rock", 9, { 0: { amp: { type, ...extra }, pan: 0 } });
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
  it("19種類ある（リード・モダン高ゲイン・きらびやかなクリーン・J-POPクリーンを含む）", () => {
    expect(GENRE_AMP_TYPES).toHaveLength(19);
    expect(new Set(GENRE_AMP_TYPES).size).toBe(19);
    for (const t of ["lead", "modernHigh", "sparkleClean", "jpopClean"]) expect(GENRE_AMP_TYPES).toContain(t);
  });

  it.each(GENRE_AMP_TYPES)("%s: 入口から出口（最終出力）までつながり、素通しではない", (type: GenreAmpType) => {
    const { path, ctx } = rackWith(type);
    expect(path[path.length - 1]).toBe(ctx.destination);
    // フィルターを2つ以上通る（音づくりがされている）
    expect(path.filter((n) => n.kind === "biquad").length).toBeGreaterThanOrEqual(2);
  });

  it("歪ませるジャンルは歪みの部品（ウェーブシェイパー）を通り、4倍オーバーサンプリングで濁りを抑える", () => {
    for (const type of ["blues", "crunch", "hardrock", "punk", "fuzz", "shoegaze", "radio", "loudmetal", "loudrock", "lead", "modernHigh"] as const) {
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

const lowpasses = (path: FakeNode[]) => path.filter((n) => n.kind === "biquad" && n.type === "lowpass").map((n) => n.frequency.value);

describe("キャビネット近似（cabApprox）", () => {
  it("どの箱・マイク位置でも、ローパスは周波数をずらした2枚以上で、7.1kHzまでに収まる", () => {
    for (const kind of CAB_KINDS) {
      for (const mic of MIC_POSITIONS) {
        const lp = cabApproxSpec(kind, mic).filter((f) => f.type === "lowpass");
        expect(lp.length, `${kind}/${mic}`).toBeGreaterThanOrEqual(2);
        expect(new Set(lp.map((f) => f.freq)).size, `${kind}/${mic}`).toBe(lp.length);
        expect(Math.min(...lp.map((f) => f.freq)), `${kind}/${mic}`).toBeLessThan(6000);
        expect(Math.max(...lp.map((f) => f.freq)), `${kind}/${mic}`).toBeLessThanOrEqual(7100);
      }
    }
  });

  it("マイク位置: 端寄り・斜め・遠いは正面より暗い（ローパスが低い）", () => {
    const top = (mic: (typeof MIC_POSITIONS)[number]) => Math.min(...cabApproxSpec("closed", mic).filter((f) => f.type === "lowpass").map((f) => f.freq));
    expect(top("edge")).toBeLessThan(top("center"));
    expect(top("off")).toBeLessThan(top("edge"));
    expect(top("far")).toBeLessThan(top("center"));
  });

  it("cab を指定すると出口にローパスの束が足され、指定しないロールは変わらない", () => {
    const base = rackWith("overdrive").path;
    expect(lowpasses(base)).toEqual([5600]);
    const withCab = rackWith("overdrive", { cab: "closed" }).path;
    expect(lowpasses(withCab).length).toBeGreaterThanOrEqual(5);
    expect(rackWith("overdrive", { mic: "far" }).path.filter((n) => n.kind === "biquad").length).toBeGreaterThan(base.filter((n) => n.kind === "biquad").length);
  });

  it("新しいロールは既定のキャビネット近似を通る", () => {
    for (const t of ["lead", "modernHigh", "sparkleClean"] as const) expect(lowpasses(rackWith(t).path).length, t).toBeGreaterThanOrEqual(3);
  });
});

describe("前段ローパス・DC除去・オーバーサンプリング・曲線", () => {
  it("リードとモダン高ゲインは、最初の歪みの前にローパスが入る", () => {
    for (const t of ["lead", "modernHigh"] as const) {
      const path = rackWith(t).path;
      const first = path.findIndex((n) => n.kind === "waveshaper");
      expect(path.slice(0, first).some((n) => n.kind === "biquad" && n.type === "lowpass" && n.frequency.value >= 6000), t).toBe(true);
    }
    // 既存ロールには足さない。指定したときだけ入る
    const od = rackWith("overdrive").path;
    expect(od.slice(0, od.findIndex((n) => n.kind === "waveshaper")).some((n) => n.type === "lowpass")).toBe(false);
    const pre = rackWith("overdrive", { preLowpass: 7000 }).path;
    expect(pre.slice(0, pre.findIndex((n) => n.kind === "waveshaper")).some((n) => n.type === "lowpass" && n.frequency.value === 7000)).toBe(true);
  });

  it("非対称の歪み（blues・fuzz・shoegaze・loudrock）の直後に25Hzのハイパス（DC除去）が入る", () => {
    for (const t of ["blues", "fuzz", "shoegaze", "loudrock", "prs", "hardrock"] as const) {
      const path = rackWith(t).path;
      const i = path.findIndex((n) => n.kind === "waveshaper");
      expect(path[i + 1].type, t).toBe("highpass");
      expect(path[i + 1].frequency.value, t).toBe(25);
    }
    const punk = rackWith("punk").path;
    expect(punk[punk.findIndex((n) => n.kind === "waveshaper") + 1].frequency.value).not.toBe(25);
  });

  it("浅い歪み（jazz・funk・lofi）は2x、深い歪みは4x。深い歪みの曲線は点が倍", () => {
    for (const t of ["jazz", "funk", "lofi"] as const) expect(rackWith(t).path.find((n) => n.kind === "waveshaper")!.oversample, t).toBe("2x");
    expect(rackWith("fuzz").path.find((n) => n.kind === "waveshaper")!.curve!.length).toBe(8192);
    expect(rackWith("overdrive").path.find((n) => n.kind === "waveshaper")!.curve!.length).toBe(4096);
  });

  it.each(CURVE_KINDS)("曲線 %s: 0を入れたら0、端は-1〜1に収まり、単調に増える", (kind) => {
    for (const bias of [0, 0.1]) {
      const c = shapeCurve(kind, 4, bias);
      const mid = c.length / 2;
      expect(Math.abs((c[mid - 1] + c[mid]) / 2)).toBeLessThan(0.01);
      // 非対称（bias）のときは、片側が offset の分だけ 1 を超える（これまでの curve() と同じ）
      expect(Math.max(...Array.from(c).map(Math.abs))).toBeLessThanOrEqual(bias ? 1.5 : 1.0001);
      for (let i = 1; i < c.length; i++) expect(c[i]).toBeGreaterThanOrEqual(c[i - 1] - 1e-9);
    }
  });

  it("曲線の指定（softsqrt）は歪みの表を差しかえ、既定（tanh）とは別の形", () => {
    const a = rackWith("crunch").path.find((n) => n.kind === "waveshaper")!.curve!;
    const b = rackWith("crunch", { curve: "softsqrt" }).path.find((n) => n.kind === "waveshaper")!.curve!;
    expect(Array.from(a).some((v, i) => Math.abs(v - b[i]) > 0.01)).toBe(true);
  });
});

describe("tight・ノイズゲート", () => {
  it("tight を上げると、歪みの前のハイパスが高くなる（100〜300Hz）", () => {
    const hp = (t: number) => rackWith("hardrock", { tight: t }).path[0];
    expect(hp(0).kind).toBe("biquad"); // 0 は足さない: 元のハイパス110Hz
    expect(hp(0).frequency.value).toBe(110);
    expect(hp(0.5).frequency.value).toBe(200);
    expect(hp(1).frequency.value).toBe(300);
  });

  it("ワークレットのない環境でも、ゲートを指定して落ちず、入口から出口までつながる", () => {
    const { path, ctx } = rackWith("modernHigh", { gate: 40 });
    expect(path[path.length - 1]).toBe(ctx.destination);
  });
});

/** 入力ギター風の信号（基音110Hz＋倍音。ピーク0.5＝-6dBFS、平均は約-18dBFS）。 */
function pseudoGuitar(n = 4800, sr = 48000): Float32Array {
  const x = new Float32Array(n);
  for (let i = 0; i < n; i++) for (let h = 1; h <= 8; h++) x[i] += Math.sin((2 * Math.PI * 110 * h * i) / sr + h) / h ** 1.1;
  const peak = Math.max(...Array.from(x).map(Math.abs));
  return x.map((v) => (v / peak) * 0.5) as Float32Array;
}
/** つなぎ方の記録から、ゲイン（増幅）と歪みの表だけをたどって、静的に出力の大きさを見積もる（フィルターと圧縮は見ない。圧縮のあるロールは実際はもっと小さい）。 */
function staticOutput(path: FakeNode[], input: Float32Array): Float32Array {
  let x: Float32Array = input;
  for (const n of path) {
    if (n.kind === "gain") x = x.map((v) => v * n.gain.value) as Float32Array;
    else if (n.kind === "waveshaper" && n.curve) {
      const c = n.curve;
      x = x.map((v) => {
        const p = ((Math.max(-1, Math.min(1, v)) + 1) / 2) * (c.length - 1);
        const i = Math.min(c.length - 2, Math.floor(p));
        return c[i] + (c[i + 1] - c[i]) * (p - i);
      }) as Float32Array;
    }
  }
  return x;
}
const peakOf = (x: Float32Array) => Math.max(...Array.from(x).map(Math.abs));
const rmsDb = (x: Float32Array) => 20 * Math.log10(Math.sqrt(x.reduce((a, v) => a + v * v, 0) / x.length));

/** ゲイン階段の表: 入力 -6dBFS のギター風信号を通したときの、出口の山(dB)の静的な見積もり。ロールを調整したら、意図して更新する。 */
const GAIN_STAIRS: Record<string, number> = {
  clean: -5.2, overdrive: -3.8, distortion: -4.5, metal: -8.2, prs: -3.8, jazz: -7.8, blues: -2.9, funk: -4.2, crunch: -3.9, hardrock: -6.0, punk: -8.0, fuzz: -6.4,
  shoegaze: 3.3, lofi: -7.2, retro8bit: -7.4, radio: -5.2, loudmetal: -10.0, loudrock: -5.1, delicate: -6.0, crystal: -6.0, lead: -4.7, modernHigh: -9.8, sparkleClean: -6.0, jpopClean: -6.0,
};

describe("ゲイン階段（音割れの回帰を防ぐ）", () => {
  const roles = Object.keys(GAIN_STAIRS);
  const input = pseudoGuitar();
  const peakDb = (r: string) => 20 * Math.log10(peakOf(staticOutput(rackWith(r as AmpSetting["type"]).path, input)));

  it("表のすべてのロールが GENRE_AMP_TYPES と基本のロールに対応している", () => {
    expect(roles.sort()).toEqual([...["clean", "overdrive", "distortion", "metal", "prs"], ...GENRE_AMP_TYPES].sort());
  });

  it("各ロールの出口の山が、表の値から 1dB 以上動いていない（ゲインを上げすぎる回帰を防ぐ）", () => {
    if ((globalThis as { process?: { env: Record<string, string | undefined> } }).process?.env.AMP_STAIRS) console.log(roles.map((r) => `${r}: 山 ${peakDb(r).toFixed(1)}dB 平均 ${rmsDb(staticOutput(rackWith(r as AmpSetting["type"]).path, input)).toFixed(1)}dB`).join("\n"));
    for (const r of roles) expect(Math.abs(peakDb(r) - GAIN_STAIRS[r]), r).toBeLessThanOrEqual(1);
  });

  it("圧縮のないロールは、山が -2.5dBFS（0.75）以下で、割れの元になる大きさにならない（シューゲイザーは強い圧縮が前提）", () => {
    for (const r of roles) if (r !== "shoegaze") expect(peakDb(r), r).toBeLessThanOrEqual(20 * Math.log10(0.75));
  });

  it("歪ませるロール同士で、出口の平均の大きさが 6dB 以上ばらつかない（ロールを替えても極端に音量が変わらない）", () => {
    const dists = ["overdrive", "distortion", "metal", "prs", "blues", "crunch", "hardrock", "fuzz", "loudmetal", "loudrock", "lead", "modernHigh"];
    const levels = dists.map((r) => rmsDb(staticOutput(rackWith(r as AmpSetting["type"]).path, input)));
    expect(Math.max(...levels) - Math.min(...levels)).toBeLessThan(6);
  });
});
