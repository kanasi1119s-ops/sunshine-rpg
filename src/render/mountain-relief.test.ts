import { describe, expect, it } from "vitest";
import { computeReliefField, reliefNoise, reliefTierOf, TIERS, reliefOverWater } from "./mountain-relief";
import { RELIEF_SPRITES } from "../game/art/relief-sprites.generated";

describe("山の高低差（見た目だけ）", () => {
  it("ふちは山すそ、内がわほど高くなる", () => {
    const W = 21, H = 21;
    const isMount = (x: number, y: number) => x >= 2 && y >= 2 && x <= 18 && y <= 18;
    const f = computeReliefField(W, H, isMount, () => false, () => 0);
    expect(f.dist[2 * W + 2]).toBe(1);
    expect(TIERS[f.tier[2 * W + 10]]).toBe("foot");
    expect(f.dist[10 * W + 10]).toBeGreaterThan(5);
    expect(f.elev[10 * W + 10]).toBeGreaterThan(f.elev[3 * W + 10]);
    // 山でないマスには何も置かない
    expect(f.dist[0]).toBe(0);
  });

  it("雪の峰は、ふちでは出ず、高い所だけ", () => {
    expect(reliefTierOf(1, 9, true)).toBe(0);
    expect(reliefTierOf(6, 4.2, true)).toBe(3);
    expect(reliefTierOf(6, 4.2, false)).toBe(2);
    expect(reliefTierOf(3, 3.0, true)).toBe(1);
  });

  it("ゆらぎは決まった値で、-1〜1 におさまる", () => {
    for (let i = 0; i < 200; i++) {
      const v = reliefNoise(i * 7, i * 3);
      expect(v).toBe(reliefNoise(i * 7, i * 3));
      expect(Math.abs(v)).toBeLessThanOrEqual(1);
    }
  });

  it("すべての山の形に影の絵がそろっている", () => {
    for (const fam of ["gray", "snow", "volc"]) {
      expect(RELIEF_SPRITES[`relief:valley-${fam}`]).toBeTruthy();
      for (const tier of TIERS) for (const lr of "lr") for (const v of "abc") {
        expect(RELIEF_SPRITES[`relief:${fam}-${tier}-${lr}${v}`]).toBeTruthy();
        expect(RELIEF_SPRITES[`relief:${fam}-${tier}-${lr}${v}-sh`]).toBeTruthy();
      }
    }
  });
});

describe("山は川・湖・海にはみ出ない", () => {
  it("すぐ上が水なら、峰の絵はかかるが、ふもとの小山はかからない（横にはみ出る数ドットは、描いたあとに消す）", () => {
    const waterUp = (x: number, y: number): boolean => x === 10 && y === 9;
    expect(reliefOverWater("peak", 10, 10, 0, 0, waterUp)).toBe(true);
    expect(reliefOverWater("foot", 10, 10, 0, 1, waterUp)).toBe(false);
    expect(reliefOverWater("peak", 10, 10, 0, 0, (x, y) => x === 11 && y === 10)).toBe(true);
  });
  it("2マス上の水には、峰の絵がかかる（高い山は、川のすぐ下には立たない）", () => {
    const waterAbove = (x: number, y: number): boolean => x === 10 && y === 8;
    expect(reliefOverWater("peak", 10, 10, 0, 0, waterAbove)).toBe(true);
    expect(reliefOverWater("slope", 10, 10, 0, 0, waterAbove)).toBe(false);
  });
});
