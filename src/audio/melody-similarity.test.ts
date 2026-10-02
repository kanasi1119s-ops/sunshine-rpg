import { describe, expect, it } from "vitest";
// @ts-expect-error tools の .mjs（型なし）を読む
import { intervals, longestCommonRun, melodyNotes, ngrams, parsons } from "../../tools/audio-check/melody-similarity.mjs";

describe("旋律の類似チェック（tools/audio-check/melody-similarity.mjs）", () => {
  it("音程列は移調しても同じになる", () => {
    const a = melodyNotes("C4:1 E4:1 G4:1 E4:2");
    const b = melodyNotes("D4:1 F#4:1 A4:1 F#4:2");
    expect(intervals(a)).toEqual(intervals(b));
    expect(parsons(a)).toBe("UUD");
  });
  it("休みは数えない。拍の長さが違っても音程列は同じ", () => {
    expect(intervals(melodyNotes("A4:1 R:1 C5:0.5 B4:2"))).toEqual([3, -1]);
  });
  it("共通する最長の連続を見つける", () => {
    const run = longestCommonRun([1, 2, 3, 4, 5, 9], [7, 2, 3, 4, 8]);
    expect(run).toEqual({ len: 3, ia: 1, ib: 1 });
    expect(longestCommonRun([1, 2], [3, 4]).len).toBe(0);
  });
  it("n-gram は重なりなく数える", () => {
    expect(ngrams([1, 2, 3, 4], 3).size).toBe(2);
    expect(ngrams([1, 2], 3).size).toBe(0);
  });
});
