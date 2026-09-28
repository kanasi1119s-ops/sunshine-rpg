import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec, type Score } from "./score";
import {
  CHAPTER0_ATTACK_SE,
  CHAPTER0_CONFIRM_SE,
  CHAPTER0_CURSOR_SE,
  CHAPTER0_DEFEAT_SE,
  CHAPTER0_DOOR_SE,
  CHAPTER0_VICTORY_SE,
} from "./chapter0-se";

const SCORES: Record<string, Score> = {
  confirm: CHAPTER0_CONFIRM_SE,
  cursor: CHAPTER0_CURSOR_SE,
  door: CHAPTER0_DOOR_SE,
  victory: CHAPTER0_VICTORY_SE,
  defeat: CHAPTER0_DEFEAT_SE,
  attack: CHAPTER0_ATTACK_SE,
};

describe.each(Object.entries(SCORES))("序章の効果音: %s", (_name, score) => {
  it("ループしない効果音として指定されている", () => {
    expect(score.loop).toBe(false);
  });

  it("すべての音名が正しく解釈できる", () => {
    expect(() => flattenScore(score)).not.toThrow();
  });

  it("長さが0より大きく、5秒以内におさまる（効果音として妥当な長さ）", () => {
    const seconds = getScoreDurationSec(score);
    expect(seconds).toBeGreaterThan(0);
    expect(seconds).toBeLessThan(5);
  });
});
