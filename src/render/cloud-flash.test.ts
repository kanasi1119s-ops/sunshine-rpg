import { describe, expect, it } from "vitest";
import { cloudFlashFrame } from "./vortex-renderer";

describe("雲の中の雷", () => {
  it("ふだんはコマ0、光る→稲妻→光る→ふだん→稲妻→光る→ふだん", () => {
    expect([0, 70, 140, 200, 280, 340, 500].map((t) => cloudFlashFrame(t))).toEqual([1, 2, 1, 0, 3, 1, 0]);
    expect(cloudFlashFrame(2000)).toBe(0);
  });
  it("回ごとに稲妻 A と B を入れかえる", () => {
    expect(cloudFlashFrame(3300 + 70)).toBe(3);
    expect(cloudFlashFrame(3300 + 280)).toBe(2);
  });
});
