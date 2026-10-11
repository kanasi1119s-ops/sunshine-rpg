import { describe, expect, it } from "vitest";
import { SFX_RECIPES, SFX_BY_ID } from "./sfx-recipes";
import { DUCK_DB, adjustSe, RoundRobin, SeThrottle, SE_MAX_SEC, checkSe, duckBgmForSe, duckLevelOf, inspectSe, makeVariants, recipeDuration, renderSfx, snapFrequency, tuneSe, varySe } from "./sfx-synth";
import { makeRng, toWav16 } from "./synth-dsp";

describe("SE レシピ", () => {
  it("58 個あり、id が重複しない", () => {
    expect(SFX_RECIPES.length).toBe(58);
    expect(new Set(SFX_RECIPES.map((r) => r.id)).size).toBe(58);
    expect(SFX_BY_ID["level-up"]).toBeTruthy();
  });

  for (const r of SFX_RECIPES) {
    it(`${r.id}: 描けて検査を通る`, () => {
      const { analysis, warnings, samples } = inspectSe(r, 22050);
      expect(samples.length).toBeGreaterThan(100);
      for (let i = 0; i < samples.length; i++) if (!Number.isFinite(samples[i])) throw new Error("NaN at " + i);
      expect(analysis.peakDb).toBeLessThanOrEqual(-3);
      expect(analysis.lengthSec).toBeLessThanOrEqual(SE_MAX_SEC[r.kind] + 1e-6);
      expect(warnings).toEqual([]);
    });
  }
});

describe("SE の仕組み", () => {
  const cursor = SFX_BY_ID["cursor"];
  it("同じ種なら同じ音（決定的）", () => {
    const a = renderSfx(cursor, 22050);
    const b = renderSfx(cursor, 22050);
    expect(Array.from(a.slice(0, 500))).toEqual(Array.from(b.slice(0, 500)));
    expect(recipeDuration(cursor)).toBeGreaterThan(0);
  });
  it("checkSe: 山が高い・長すぎるを検出", () => {
    const w = checkSe({ peak: 1, peakDb: 0, rmsDb: -10, lengthSec: 2, attackMs: 1, dc: 0, centroidHz: 1000, band1to4k: 0.5 }, { id: "x", kind: "ui" });
    expect(w.length).toBe(2);
  });
  it("varySe: 範囲内で決定的", () => {
    const r = SFX_RECIPES.find((x) => x.vary?.pitch)!;
    const a = varySe(r, makeRng(3));
    const b = varySe(r, makeRng(3));
    expect(JSON.stringify(a)).toBe(JSON.stringify(b));
    const l0 = r.layers[0], a0 = a.layers[0];
    if (l0.kind === "tone" && a0.kind === "tone") {
      const ratio = a0.f0 / l0.f0;
      expect(ratio).toBeGreaterThanOrEqual(1 - (r.vary!.pitch ?? 0) - 1e-9);
      expect(ratio).toBeLessThanOrEqual(1 + (r.vary!.pitch ?? 0) + 1e-9);
    }
    expect(makeVariants(r, 4, 1).length).toBe(4);
    expect(JSON.stringify(makeVariants(r, 4, 1))).toBe(JSON.stringify(makeVariants(r, 4, 1)));
  });
  it("tuneSe: ±2 半音以内で音階の音へ寄る", () => {
    const tuned = SFX_RECIPES.filter((r) => r.layers.some((l) => l.tune));
    expect(tuned.length).toBeGreaterThan(3);
    for (const r of tuned) {
      const t = tuneSe(r, 2, "aeolian");
      r.layers.forEach((l, i) => {
        const m = t.layers[i];
        if (l.kind === "tone" && m.kind === "tone" && l.tune) {
          expect(Math.abs(12 * Math.log2(m.f0 / l.f0))).toBeLessThanOrEqual(2.001);
        }
      });
    }
    // D(=2) 短調：A4=440 は音階内なのでそのまま
    expect(snapFrequency(440, [2, 4, 5, 7, 9, 10, 0])).toBeCloseTo(440, 5);
    // C#4 は D 短調の外 → 半音寄る
    const cs = 440 * 2 ** (-8 / 12);
    expect(snapFrequency(cs, [2, 4, 5, 7, 9, 10, 0])).not.toBeCloseTo(cs, 3);
  });
  it("SeThrottle / RoundRobin", () => {
    const t = new SeThrottle();
    expect(t.allow("a", 0, 100)).toBe(true);
    expect(t.allow("a", 50, 100)).toBe(false);
    expect(t.allow("a", 120, 100)).toBe(true);
    expect(t.allow("b", 120, 100)).toBe(true);
    const rr = new RoundRobin();
    expect([0, 1, 2, 3, 4].map(() => rr.next("s", 3))).toEqual([0, 1, 2, 0, 1]);
  });
  it("duckBgmForSe: 量とタイミング", () => {
    const calls: [number, number, number][] = [];
    const p = { setTargetAtTime: (a: number, b: number, c: number) => void calls.push([a, b, c]) };
    expect(duckBgmForSe(p, "none", 1, 1)).toBe(1);
    expect(calls.length).toBe(0);
    const g = duckBgmForSe(p, "fanfare", 1, 2);
    expect(20 * Math.log10(g)).toBeCloseTo(DUCK_DB.fanfare, 5);
    expect(calls.length).toBe(2);
    expect(calls[1][0]).toBe(1);
    expect(calls[1][1]).toBeCloseTo(3, 5);
    expect(duckLevelOf({ kind: "fanfare" })).toBe("fanfare");
    expect(duckLevelOf({ kind: "ui" })).toBe("none");
  });
  it("adjustSe: 高さ・長さ・山を変えられる", () => {
    const r = SFX_BY_ID["confirm"];
    const up = adjustSe(r, { pitch: 2 });
    const l0 = r.layers[0], l1 = up.layers[0];
    if (l0.kind === "tone" && l1.kind === "tone") expect(l1.f0).toBeCloseTo(l0.f0 * 2, 6);
    const slow = adjustSe(r, { time: 2 });
    expect(slow.lengthSec).toBeCloseTo(r.lengthSec * 2, 6);
    expect(adjustSe(r, { peakDb: 0 }).peakDb).toBe(-3);
    expect(adjustSe(r, {}).layers.length).toBe(r.layers.length);
  });
  it("toWav16: RIFF ヘッダー", () => {
    const w = toWav16(new Float32Array(100), 22050);
    expect(String.fromCharCode(...w.slice(0, 4))).toBe("RIFF");
    expect(w.length).toBe(44 + 200);
  });
});
