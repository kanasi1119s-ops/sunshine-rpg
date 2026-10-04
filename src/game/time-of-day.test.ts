import { describe, expect, it } from "vitest";
import { DAY_MS, dayFraction, isNight, isOutdoorMap, nextMorning, nightness, periodLabel, staysOutAtNight } from "./time-of-day";

describe("昼と夜", () => {
  it("朝から始まり、昼→夕方→夜→夜明けと移る", () => {
    expect(nightness(0)).toBe(0);
    expect(nightness(0.3)).toBe(0);
    expect(nightness(0.58)).toBeGreaterThan(0.3);
    expect(nightness(0.58)).toBeLessThan(0.9);
    expect(nightness(0.75)).toBe(1);
    expect(nightness(0.94)).toBeLessThan(0.6);
    expect(nightness(0.999)).toBeLessThan(0.05);
    expect(periodLabel(0)).toBe("昼");
    expect(periodLabel(DAY_MS * 0.75)).toBe("夜");
  });
  it("夜かどうか。宿にとまると、つぎの朝", () => {
    expect(isNight(DAY_MS * 0.75)).toBe(true);
    expect(isNight(DAY_MS * 0.2)).toBe(false);
    const morning = nextMorning(DAY_MS * 0.75);
    expect(morning).toBe(DAY_MS);
    expect(isNight(morning)).toBe(false);
    expect(dayFraction(morning)).toBe(0);
    expect(nextMorning(DAY_MS * 2.1)).toBe(DAY_MS * 3);
  });
  it("夜に外にいる町の人は、およそ3人に1人。同じ人はいつも同じ", () => {
    const ids = Array.from({ length: 300 }, (_, i) => `town-townsfolk-${i}`);
    const out = ids.filter(staysOutAtNight).length;
    expect(out).toBeGreaterThan(70);
    expect(out).toBeLessThan(130);
    expect(staysOutAtNight("a-1")).toBe(staysOutAtNight("a-1"));
  });
  it("外の地図だけ、夜の色がつく", () => {
    expect(isOutdoorMap("world-map")).toBe(true);
    expect(isOutdoorMap("touri-town")).toBe(true);
    expect(isOutdoorMap("village-namioto")).toBe(true);
    expect(isOutdoorMap("touri-house-1")).toBe(false);
  });
});
