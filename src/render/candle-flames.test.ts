import { describe, expect, it } from "vitest";
import { KIRI_CHURCH_FLAMES } from "../game/map/chapter5/kiri-church-flames.generated";
import { flameFrame } from "./candle-flames";

describe("ろうそくの炎の揺らめき", () => {
  it("聖堂の炎は、絵（208×224）の中にある", () => {
    expect(KIRI_CHURCH_FLAMES.length).toBeGreaterThan(10);
    for (const f of KIRI_CHURCH_FLAMES) {
      expect(f.x >= 1 && f.x < 207 && f.y >= 5 && f.y < 224, `${f.x},${f.y}`).toBe(true);
    }
  });

  it("時間がたつとコマが変わり、炎ごとにずれている", () => {
    const f = KIRI_CHURCH_FLAMES[0];
    const frames = new Set([0, 200, 400, 600, 800, 1000].map((ms) => flameFrame(f, ms)));
    expect(frames.size).toBeGreaterThan(2);
    const at0 = new Set(KIRI_CHURCH_FLAMES.map((x) => flameFrame(x, 0)));
    expect(at0.size).toBeGreaterThan(1);
  });
});
