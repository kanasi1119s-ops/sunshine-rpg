import { describe, expect, it } from "vitest";
import { computeVisibleChars } from "./typewriter";

describe("computeVisibleChars", () => {
  it("経過時間0では1文字も見えない", () => {
    expect(computeVisibleChars("こんにちは", 0)).toBe(0);
  });

  it("速さに応じた文字数だけ見える", () => {
    // 30文字/秒 で 100ms 経過 → 3文字。
    expect(computeVisibleChars("こんにちは", 100, 30)).toBe(3);
  });

  it("文章の長さを超えない", () => {
    expect(computeVisibleChars("こんにちは", 100000, 30)).toBe(5);
  });
});
