import { describe, expect, it } from "vitest";
import { advanceBootOpening, REVEAL, startBootOpening, STORY_LINES, storyDurationMs, updateBootOpening } from "./boot-opening";

describe("起動のオープニング", () => {
  it("最初は SUNSHINE SOFTWARE PRESENTS。タップ（決定）するまで進まない。決定で、あらすじ→ロゴの登場→ロゴ→タイトルの順に進む", () => {
    let s = startBootOpening();
    expect(s.phase).toBe("splash");
    expect(updateBootOpening(s, 5000, 225)).toEqual(s);
    s = advanceBootOpening(s);
    expect(s.phase).toBe("story");
    s = advanceBootOpening(s);
    expect(s.phase).toBe("reveal");
    s = advanceBootOpening(s);
    expect(s.phase).toBe("hold");
    expect(advanceBootOpening(s).open).toBe(false);
  });

  it("放っておくと、あらすじ→ロゴの登場→ロゴ、と進み、ロゴで止まったまま、ボタンが押されるまで流れつづける", () => {
    let s = advanceBootOpening(startBootOpening());
    s = updateBootOpening(s, storyDurationMs(225) + 1, 225);
    expect(s.phase).toBe("reveal");
    s = updateBootOpening(s, REVEAL.total + 1, 225);
    expect(s.phase).toBe("hold");
    // 何分たっても、タイトルへ勝手に進まない
    for (let i = 0; i < 100; i++) s = updateBootOpening(s, 10_000, 225);
    expect(s.open).toBe(true);
    expect(s.phase).toBe("hold");
  });

  it("ロゴの登場は、光が集まる→文字→サブタイトルの順", () => {
    expect(REVEAL.gatherEnd).toBeLessThan(REVEAL.lettersEnd);
    expect(REVEAL.lettersEnd).toBeLessThan(REVEAL.subtitleEnd);
    expect(REVEAL.subtitleEnd).toBeLessThanOrEqual(REVEAL.total);
  });

  it("あらすじは、世界観と主人公の旅立ちまでで、黒幕などの真相に触れない", () => {
    const text = STORY_LINES.join("");
    expect(text).toContain("灯の環");
    expect(text).not.toContain("エドレア");
    expect(text).not.toContain("黒幕");
  });
});
