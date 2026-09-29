import { describe, expect, it } from "vitest";
import {
  AMP_CURVE_SAMPLES,
  AMP_PRESET_NAMES,
  AMP_PRESETS,
  getAmpSettings,
  makeDistortionCurve,
  type AmpShape,
} from "./amp";
import { AMP_DEMO_SCORES } from "./amp-demo";
import { getScoreDurationSec } from "./score";

const SHAPES: AmpShape[] = ["soft", "hard", "asym", "steps"];

describe("makeDistortionCurve", () => {
  it.each(SHAPES)("%s: 点の数が指定どおりで、値はすべて有限で -1〜1 に収まる", (shape) => {
    const curve = makeDistortionCurve(shape, 6, 0.3, 513);
    expect(curve).toHaveLength(513);
    for (const y of curve) {
      expect(Number.isFinite(y)).toBe(true);
      expect(Math.abs(y)).toBeLessThanOrEqual(1);
    }
  });

  it.each(SHAPES)("%s: 真ん中（入力0）は出力もちょうど0", (shape) => {
    const curve = makeDistortionCurve(shape, 6, 0.3, 513);
    expect(curve[256]).toBeCloseTo(0, 6);
  });

  it.each(SHAPES)("%s: 両端（入力±1）は出力もほぼ±1", (shape) => {
    const curve = makeDistortionCurve(shape, 6, 0.3, 513);
    expect(curve[0]).toBeCloseTo(-1, 5);
    expect(curve[512]).toBeCloseTo(1, 5);
  });

  it.each(["soft", "hard", "asym"] as AmpShape[])("%s: 入力が大きいほど出力も大きい（単調に増える）", (shape) => {
    const curve = makeDistortionCurve(shape, 8, 0.4, 1025);
    for (let i = 1; i < curve.length; i++) {
      expect(curve[i]).toBeGreaterThanOrEqual(curve[i - 1] - 1e-7);
    }
  });

  it("steps: 出力が階段状（違う値が段数ぶんだけ）になる", () => {
    const curve = makeDistortionCurve("steps", 4, 0, 1025);
    const distinct = new Set(Array.from(curve, (y) => y.toFixed(5)));
    // 片側4段 → -1〜1で9種類
    expect(distinct.size).toBe(9);
  });

  it("soft: 硬さが大きいほど、小さな入力でも強く増幅される（より歪む）", () => {
    const mild = makeDistortionCurve("soft", 1, 0, 513);
    const heavy = makeDistortionCurve("soft", 10, 0, 513);
    // 入力0.25（index 320）での出力を比べる
    expect(heavy[320]).toBeGreaterThan(mild[320]);
  });

  it("asym: 非対称が0なら上下対称、0より大きいと上下で出力の大きさが変わる", () => {
    const sym = makeDistortionCurve("asym", 4, 0, 513);
    const skew = makeDistortionCurve("asym", 4, 0.6, 513);
    expect(sym[384]).toBeCloseTo(-sym[128], 6);
    expect(Math.abs(skew[384])).not.toBeCloseTo(Math.abs(skew[128]), 3);
  });

  it("asym: 非対称の値が範囲外（負・1超）でも、値は -1〜1 に収まる", () => {
    for (const a of [-5, 5]) {
      const curve = makeDistortionCurve("asym", 6, a, 257);
      for (const y of curve) {
        expect(Math.abs(y)).toBeLessThanOrEqual(1);
      }
    }
  });

  it("初期のカーブの点の数は奇数（真ん中がちょうど0になる）", () => {
    expect(AMP_CURVE_SAMPLES % 2).toBe(1);
  });
});

describe("AMP_PRESETS（ジャンル別プリセット）", () => {
  it("ジャンルの数は十分ある（あらゆるジャンルに対応する方針）", () => {
    expect(AMP_PRESET_NAMES.length).toBeGreaterThanOrEqual(12);
  });

  it("主要ジャンルがそろっている", () => {
    for (const name of ["clean", "jazz", "blues", "funk", "rock", "hardrock", "punk", "metal", "lofi"]) {
      expect(AMP_PRESET_NAMES).toContain(name);
    }
  });

  it.each(AMP_PRESET_NAMES)("%s: 設定値が正しい範囲にある", (name) => {
    const s = getAmpSettings(name);
    expect(s.label.length).toBeGreaterThan(0);
    expect(s.genre.length).toBeGreaterThan(0);
    expect(s.drive).toBeGreaterThanOrEqual(1);
    expect(s.hardness).toBeGreaterThan(0);
    expect(s.asymmetry).toBeGreaterThanOrEqual(0);
    expect(s.asymmetry).toBeLessThanOrEqual(1);
    for (const db of [s.bassDb, s.midDb, s.trebleDb]) {
      expect(Math.abs(db)).toBeLessThanOrEqual(15);
    }
    expect(s.midHz).toBeGreaterThan(200);
    expect(s.midHz).toBeLessThan(3000);
    expect(s.highpassHz).toBeGreaterThan(20);
    expect(s.lowpassHz).toBeGreaterThan(s.highpassHz * 4);
    expect(s.lowpassHz).toBeLessThanOrEqual(12000);
    expect(s.level).toBeGreaterThan(0);
    expect(s.level).toBeLessThanOrEqual(1.5);
  });

  it("ジャンルの呼び名（label）は重複しない", () => {
    const labels = AMP_PRESET_NAMES.map((n) => AMP_PRESETS[n].label);
    expect(new Set(labels).size).toBe(labels.length);
  });

  it("クリーンより、ロック → ハードロック → メタルの順にドライブが強い", () => {
    const d = (n: (typeof AMP_PRESET_NAMES)[number]) => AMP_PRESETS[n].drive;
    expect(d("clean")).toBeLessThan(d("crunch"));
    expect(d("crunch")).toBeLessThan(d("rock"));
    expect(d("rock")).toBeLessThan(d("hardrock"));
    expect(d("hardrock")).toBeLessThan(d("metal"));
  });

  it("メタルは中域を削り、ジャズは高域を丸める（ジャンルの音の性格）", () => {
    expect(AMP_PRESETS.metal.midDb).toBeLessThan(0);
    expect(AMP_PRESETS.jazz.trebleDb).toBeLessThan(0);
    expect(AMP_PRESETS.jazz.lowpassHz).toBeLessThan(AMP_PRESETS.clean.lowpassHz);
  });
});

describe("AMP_DEMO_SCORES（試聴用デモ）", () => {
  it.each(AMP_PRESET_NAMES)("%s: 全パートの合計拍数がそろっていて、アンプが指定されている", (name) => {
    const score = AMP_DEMO_SCORES[name];
    const totals = score.tracks.map((t) => t.notes.reduce((sum, n) => sum + n.durationBeats, 0));
    expect(new Set(totals).size).toBe(1);
    expect(totals[0]).toBe(16);
    expect(getScoreDurationSec(score)).toBeGreaterThan(0);
    expect(score.tracks[0].amp).toBe(name);
    expect(score.loop).toBe(true);
  });

  it("低音パートにはアンプを通さない", () => {
    expect(AMP_DEMO_SCORES.metal.tracks[2].amp).toBeUndefined();
  });
});
