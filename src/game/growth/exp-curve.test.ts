import { describe, expect, it } from "vitest";
import { expRequiredForLevel, expToNextLevel, levelForExp } from "./exp-curve";

describe("expRequiredForLevel", () => {
  it("レベル1は0経験値で到達できる", () => {
    expect(expRequiredForLevel(1)).toBe(20);
  });

  it("レベルが上がるほど必要量が増える", () => {
    expect(expRequiredForLevel(5)).toBeLessThan(expRequiredForLevel(10));
  });
});

describe("levelForExp", () => {
  it("経験値0でもレベル1", () => {
    expect(levelForExp(0)).toBe(1);
  });

  it("必要経験値ちょうどでそのレベルになる", () => {
    const need = expRequiredForLevel(5);
    expect(levelForExp(need)).toBe(5);
    expect(levelForExp(need - 1)).toBe(4);
  });
});

describe("expToNextLevel", () => {
  it("経験値0のとき、レベル2に必要な分を返す", () => {
    expect(expToNextLevel(0)).toBe(expRequiredForLevel(2));
  });
});
