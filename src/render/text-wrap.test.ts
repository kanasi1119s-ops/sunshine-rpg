import { describe, expect, it } from "vitest";
import { wrapText } from "./text-wrap";

const measureByLength = (segment: string): number => segment.length;

describe("wrapText", () => {
  it("幅に収まる文章は1行のまま", () => {
    expect(wrapText("こんにちは", 10, measureByLength)).toEqual(["こんにちは"]);
  });

  it("幅を超えたら改行する", () => {
    expect(wrapText("あいうえおかきくけこ", 5, measureByLength)).toEqual([
      "あいうえお",
      "かきくけこ",
    ]);
  });

  it("改行文字で明示的に改行する", () => {
    expect(wrapText("あい\nうえ", 10, measureByLength)).toEqual(["あい", "うえ"]);
  });
});
