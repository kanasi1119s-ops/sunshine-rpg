import { describe, expect, it } from "vitest";
import { computeDisplaySize, LOGICAL_WIDTH, LOGICAL_HEIGHT } from "./canvas";

describe("computeDisplaySize", () => {
  it("横長のコンテナでは高さいっぱいに合わせる", () => {
    const { width, height } = computeDisplaySize(2000, 225);
    expect(height).toBe(LOGICAL_HEIGHT);
    expect(width).toBe(LOGICAL_WIDTH);
  });

  it("縦長のコンテナ（スマホ）では横幅いっぱいに合わせる", () => {
    const { width, height } = computeDisplaySize(375, 812);
    expect(width).toBeCloseTo(375, 5);
    expect(height).toBeCloseTo((375 / LOGICAL_WIDTH) * LOGICAL_HEIGHT, 5);
    expect(height).toBeLessThan(812);
  });

  it("アスペクト比を常に保つ", () => {
    const { width, height } = computeDisplaySize(1000, 1000);
    expect(width / height).toBeCloseTo(LOGICAL_WIDTH / LOGICAL_HEIGHT, 5);
  });
});
