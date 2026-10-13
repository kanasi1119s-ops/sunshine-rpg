import { describe, expect, it } from "vitest";
import { AmpRack } from "./amp-rack";
import { buildKeysAmp, KEYS_AMP_INFO, KEYS_AMP_TYPES, softSatCurve, type KeysAmpType } from "./amp-keys";
import { aiSongToScore } from "./ai-song";
import { PART_RECIPES } from "./sound-sets";

/** つなぎ方と、パラメータの値だけを記録する、Web Audio の部品の偽物（どんな名前のパラメータも受け取る）。 */
class FakeParam {
  value = 0;
}
class FakeNode {
  outputs: { node: FakeNode; out: number; inp: number }[] = [];
  stopped = false;
  started = false;
  type = "";
  curve: Float32Array | null = null;
  oversample = "none";
  channelCount = 2;
  channelCountMode = "max";
  params: Record<string, FakeParam> = {};
  // Proxy で取り出す AudioParam（型だけ宣言する。値は作らない）
  declare frequency: FakeParam;
  declare gain: FakeParam;
  wave: { real: Float32Array; imag: Float32Array } | null = null;
  constructor(public kind: string) {
    return new Proxy(this, {
      get: (t, key: string | symbol) => {
        if (typeof key === "symbol" || key in t) return (t as unknown as Record<string, unknown>)[key as string];
        // gain・frequency・Q・delayTime・threshold などの AudioParam
        return (t.params[key] ??= new FakeParam());
      },
      set: (t, key: string | symbol, value: unknown) => {
        (t as unknown as Record<string, unknown>)[key as string] = value;
        return true;
      },
    });
  }
  connect(n: FakeNode, out = 0, inp = 0): FakeNode {
    this.outputs.push({ node: n, out, inp });
    return n;
  }
  disconnect(): void {
    this.outputs = [];
  }
  start(): void {
    this.started = true;
  }
  stop(): void {
    this.stopped = true;
  }
  setPeriodicWave(w: { real: Float32Array; imag: Float32Array }): void {
    this.wave = w;
  }
}
class FakeCtx {
  all: FakeNode[] = [];
  destination = new FakeNode("destination");
  private make(kind: string): FakeNode {
    const n = new FakeNode(kind);
    this.all.push(n);
    return n;
  }
  createGain = () => this.make("gain");
  createBiquadFilter = () => this.make("biquad");
  createWaveShaper = () => this.make("waveshaper");
  createDynamicsCompressor = () => this.make("compressor");
  createStereoPanner = () => this.make("panner");
  createDelay = (_max?: number) => this.make("delay");
  createOscillator = () => this.make("oscillator");
  createChannelSplitter = (_n?: number) => this.make("splitter");
  createChannelMerger = (_n?: number) => this.make("merger");
  createPeriodicWave = (real: Float32Array, imag: Float32Array) => ({ real, imag });
}

/** 入口から出口へ、つながりをたどれるか。 */
function reaches(from: FakeNode, to: FakeNode): boolean {
  const seen = new Set<FakeNode>();
  const stack = [from];
  while (stack.length) {
    const n = stack.pop()!;
    if (n === to) return true;
    if (seen.has(n)) continue;
    seen.add(n);
    for (const o of n.outputs) stack.push(o.node);
  }
  return false;
}

const opts = { drive: 1, toneDb: 0, level: 1 };

describe("鍵盤・シンセ用のアンプ（amp-keys）", () => {
  it("12種類あり、どれにも日本語の呼び名と使いどころがある", () => {
    expect(KEYS_AMP_TYPES).toHaveLength(12);
    expect(new Set(KEYS_AMP_TYPES).size).toBe(12);
    for (const t of KEYS_AMP_TYPES) {
      expect(KEYS_AMP_INFO[t].label.length).toBeGreaterThan(2);
      expect(KEYS_AMP_INFO[t].use.length).toBeGreaterThan(10);
    }
  });

  it.each(KEYS_AMP_TYPES)("%s: 入口から出口までつながり、フィルターを2つ以上通る", (role: KeysAmpType) => {
    const ctx = new FakeCtx();
    const seg = buildKeysAmp(ctx as unknown as BaseAudioContext, role, opts);
    expect(reaches(seg.input as unknown as FakeNode, seg.output as unknown as FakeNode)).toBe(true);
    expect(seg.nodes.filter((n) => (n as unknown as FakeNode).kind === "biquad").length).toBeGreaterThanOrEqual(2);
  });

  it("揺れのあるロールは LFO を持ち、全部始めていて、ない（EQだけの）ロールは持たない", () => {
    const moving: KeysAmpType[] = ["tapeWarm", "tremKeys", "phaserKeys", "leslie", "leslieFast", "padWide", "stringsEnsemble", "lofiKeys"];
    for (const role of KEYS_AMP_TYPES) {
      const ctx = new FakeCtx();
      const seg = buildKeysAmp(ctx as unknown as BaseAudioContext, role, opts);
      const oscs = seg.nodes.filter((n) => (n as unknown as FakeNode).kind === "oscillator") as unknown as FakeNode[];
      if (moving.includes(role)) expect(oscs.length, role).toBeGreaterThan(0);
      else expect(oscs.length, role).toBe(0);
      expect(oscs.every((o) => o.started), role).toBe(true);
      expect(seg.sources.length, role).toBe(oscs.length);
    }
  });

  it("回転スピーカー: ゆっくりは 0.8Hz・0.67Hz、速いは 6.7Hz・5.7Hz のホーンとドラムが回る", () => {
    const rates = (role: KeysAmpType): number[] => {
      const ctx = new FakeCtx();
      const seg = buildKeysAmp(ctx as unknown as BaseAudioContext, role, opts);
      return [...new Set(seg.nodes.filter((n) => (n as unknown as FakeNode).kind === "oscillator").map((n) => Math.round((n as unknown as FakeNode).frequency.value * 100) / 100))].sort((a, b) => a - b);
    };
    expect(rates("leslie")).toEqual([0.67, 0.8]);
    expect(rates("leslieFast")).toEqual([5.7, 6.7]);
  });

  it("位相をずらした LFO は、sin(ωt+φ) の周期波形（実部 sinφ・虚部 cosφ）になる", () => {
    const ctx = new FakeCtx();
    buildKeysAmp(ctx as unknown as BaseAudioContext, "padWide", opts);
    const waves = ctx.all.filter((n) => n.kind === "oscillator" && n.wave);
    expect(waves.length).toBeGreaterThan(0);
    for (const o of waves) {
      const { real, imag } = o.wave!;
      expect(real[0]).toBe(0);
      expect(real[1] ** 2 + imag[1] ** 2).toBeCloseTo(1, 5);
    }
  });

  it("tone と level と drive がつながる（高音の調整・出力の倍率・飽和の深さ）", () => {
    const ctx = new FakeCtx();
    const seg = buildKeysAmp(ctx as unknown as BaseAudioContext, "vintageKeys", { drive: 2, toneDb: -3, level: 0.8 });
    expect((seg.output as unknown as FakeNode).gain.value).toBe(0.8);
    const shelves = seg.nodes.filter((n) => (n as unknown as FakeNode).kind === "biquad" && (n as unknown as FakeNode).type === "highshelf" && (n as unknown as FakeNode).frequency.value === 3500);
    expect((shelves[0] as unknown as FakeNode).gain.value).toBe(-3);
    const shaper = seg.nodes.find((n) => (n as unknown as FakeNode).kind === "waveshaper") as unknown as FakeNode;
    const mid = (shaper.curve!.length - 1) / 2;
    // 深くすると、同じ入力(0.5)で出力が小さくなる（潰れる）
    const x = Math.round(mid * 1.5);
    const deep = shaper.curve![x];
    const shallow = softSatCurve(2.4 * 1, 0.05)[x];
    expect(deep).toBeLessThan(shallow);
  });

  it("softSatCurve: 原点の傾きが 1（小さい音は変わらない）・非対称でも 0 を 0 に返す・出力は 1/k 以内", () => {
    const c = softSatCurve(3, 0);
    const mid = (c.length - 1) / 2;
    const slope = (c[mid + 1] - c[mid - 1]) / (4 / (c.length - 1));
    expect(slope).toBeCloseTo(1, 2);
    expect(c[mid]).toBeCloseTo(0, 6);
    expect(Math.max(...Array.from(c).map(Math.abs))).toBeLessThanOrEqual(1 / 3 + 1e-6);
    const a = softSatCurve(3, 0.05);
    expect(a[mid]).toBeCloseTo(0, 6);
    expect(a[a.length - 1] + a[0]).not.toBeCloseTo(0, 3);
  });
});

describe("AmpRack との組み合わせ", () => {
  it("amp に鍵盤用の種類を書くと、そのチャンネルが組み立てられ、出口（最終出力）までつながる", () => {
    for (const type of KEYS_AMP_TYPES) {
      const ctx = new FakeCtx();
      const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
      rack.configure({ 0: 4 }, "rock", 9, { 0: { amp: { type }, pan: 0 } });
      expect(reaches(rack.input(0) as unknown as FakeNode, ctx.destination), type).toBe(true);
    }
  });

  it("つなぎ直すと、前の LFO は止まる（鳴りっぱなしにならない）", () => {
    const ctx = new FakeCtx();
    const rack = new AmpRack(ctx as unknown as BaseAudioContext, ctx.destination as unknown as AudioNode);
    rack.configure({ 0: 4 }, "rock", 9, { 0: { amp: { type: "leslie" }, pan: 0 } });
    const oscs = ctx.all.filter((n) => n.kind === "oscillator");
    expect(oscs.length).toBeGreaterThan(0);
    expect(oscs.every((o) => !o.stopped)).toBe(true);
    rack.configure({ 0: 4 }, "rock", 9, {});
    expect(oscs.every((o) => o.stopped)).toBe(true);
  });
});

describe("AIソング形式との組み合わせ", () => {
  const song = (amp: string, extra: Record<string, unknown> = {}) => ({
    title: "t", bpm: 90, beats: 4, chords: "C", barsPerChord: 1, repeats: 1, autoAccompaniment: false,
    parts: [{ instrument: "keys", role: "ep", volume: 0.1, pan: 0, amp, notes: "C4:4", ...extra }],
  });

  it("鍵盤用のアンプ名はそのまま使える（警告なし）", () => {
    for (const t of KEYS_AMP_TYPES) {
      const { score, warnings } = aiSongToScore(song(t));
      expect(warnings.filter((w) => w.includes("アンプ")), t).toEqual([]);
      expect(score.tracks[0].amp?.type, t).toBe(t);
    }
  });

  it("書かなければ、amp は付かない（これまでの曲は変わらない）", () => {
    expect(aiSongToScore(song("auto")).score.tracks[0].amp).toBeUndefined();
  });
});

describe("鍵盤・シンセのレシピ（PART_RECIPES）", () => {
  const ids = Object.keys(PART_RECIPES).filter((id) => id.startsWith("keys-") || id.startsWith("synth-") || id.startsWith("pad-") || id.startsWith("ep-") || id.startsWith("organ-") || id.startsWith("piano-") || id.startsWith("strings-")).filter((id) => PART_RECIPES[id].mix.amp); // amp を持たない昔の弦レシピ（strings-ensemble）は対象外
  it("レシピがあり、どれも amp は鍵盤用の種類で、AIソングの recipe として使える", () => {
    expect(ids.length).toBeGreaterThanOrEqual(8);
    for (const id of ids) {
      const r = PART_RECIPES[id];
      expect(KEYS_AMP_TYPES as string[], id).toContain(r.mix.amp?.type);
      expect(r.instruments.length, id).toBeGreaterThan(0);
      const instrument = r.instruments[0];
      const { warnings } = aiSongToScore({
        title: "t", bpm: 90, beats: 4, chords: "C", barsPerChord: 1, repeats: 1, autoAccompaniment: false,
        parts: [{ instrument, role: "p", volume: 0.1, pan: 0, recipe: id, notes: "C4:4" }],
      });
      expect(warnings.filter((w) => w.includes("recipe") || w.includes("アンプ")), id).toEqual([]);
    }
  });
});
