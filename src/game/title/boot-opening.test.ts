import { describe, expect, it } from "vitest";
import { advanceBootOpening, LOGO_MS, logoDrop, startBootOpening, STORY_LINES, storyDurationMs, updateBootOpening } from "./boot-opening";

describe("起動のオープニング", () => {
  it("決定でスタートするまでは進まない。決定でロゴ、あらすじ、タイトルの順に進む", () => {
    let s = startBootOpening();
    expect(updateBootOpening(s, 5000, 225)).toEqual(s);
    s = advanceBootOpening(s);
    expect(s.phase).toBe("logo");
    s = advanceBootOpening(s);
    expect(s.phase).toBe("story");
    expect(advanceBootOpening(s).open).toBe(false);
  });

  it("放っておいても、ロゴ→あらすじ→終わり（タイトルへ）と進む", () => {
    let s = advanceBootOpening(startBootOpening());
    s = updateBootOpening(s, LOGO_MS + 1, 225);
    expect(s.phase).toBe("story");
    s = updateBootOpening(s, storyDurationMs(225) + 1, 225);
    expect(s.open).toBe(false);
  });

  it("ロゴは上から落ちて、着地し、最後は決まった位置で止まる", () => {
    expect(logoDrop(0)).toBe(0);
    expect(logoDrop(450)).toBeLessThan(logoDrop(850));
    expect(logoDrop(900)).toBeCloseTo(1, 1);
    expect(logoDrop(3000)).toBe(1);
  });

  it("あらすじは、世界観と主人公の旅立ちまでで、黒幕などの真相に触れない", () => {
    const text = STORY_LINES.join("");
    expect(text).toContain("灯の環");
    expect(text).not.toContain("エドレア");
    expect(text).not.toContain("黒幕");
  });
});
