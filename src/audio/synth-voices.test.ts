import { describe, expect, it } from "vitest";
import { GM_PROGRAM } from "./gm-map";
import { AI_INSTRUMENTS } from "./ai-song";
import { bitcrushCurve, DRAWBAR, shaperCurve, unisonDetunes } from "./synth-voices";

describe("追加の音源", () => {
  it("4 つの音源に GM 番号と説明がある", () => {
    for (const k of ["fmBell", "fmEpiano", "drawbarOrgan", "unisonSaw"] as const) {
      expect(GM_PROGRAM[k], k).toBeGreaterThanOrEqual(0);
      expect(AI_INSTRUMENTS[k], k).toBeTruthy();
    }
  });
  it("unisonDetunes: 本数と幅", () => {
    expect(unisonDetunes(1, 20)).toEqual([0]);
    const d = unisonDetunes(5, 18);
    expect(d.length).toBe(5);
    expect(d[0]).toBe(-18);
    expect(d[4]).toBe(18);
    expect(d[2]).toBe(0);
  });
  it("ドローバーは 1・3・2・4・6・8 倍", () => {
    expect(DRAWBAR.map((h) => h.ratio)).toEqual([1, 3, 2, 4, 6, 8]);
  });
  it("bitcrushCurve: 段数は 2^bits 以下、端は ±1", () => {
    const c = bitcrushCurve(3);
    expect(new Set(Array.from(c)).size).toBeLessThanOrEqual(2 ** 3 + 1);
    expect(c[0]).toBe(-1);
    expect(c[c.length - 1]).toBe(1);
    expect(new Set(Array.from(bitcrushCurve(8))).size).toBeGreaterThan(new Set(Array.from(c)).size);
  });
  it("shaperCurve: 範囲内・単調・drive が大きいほど中間が持ち上がる", () => {
    const a = shaperCurve(2), b = shaperCurve(12);
    for (let i = 1; i < a.length; i++) expect(a[i]).toBeGreaterThanOrEqual(a[i - 1]);
    expect(Math.max(...Array.from(b))).toBeCloseTo(1, 5);
    const q = Math.floor(a.length * 0.75);
    expect(b[q]).toBeGreaterThan(a[q]);
  });
});
