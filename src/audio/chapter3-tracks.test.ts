import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec, type Score } from "./score";
import { CHAPTER3_BOSS_THEME, CHAPTER3_MINE_THEME, CHAPTER3_TOWN_THEME } from "./chapter3-tracks";

const SCORES: Record<string, Score> = {
  town: CHAPTER3_TOWN_THEME,
  mine: CHAPTER3_MINE_THEME,
  boss: CHAPTER3_BOSS_THEME,
};

function totalBeats(track: Score["tracks"][number]): number {
  return track.notes.reduce((sum, n) => sum + n.durationBeats, 0);
}

describe.each(Object.entries(SCORES))("第3章のBGM: %s", (_name, score) => {
  it("テンポが正の値で、パートが1つ以上ある", () => {
    expect(score.tempoBpm).toBeGreaterThan(0);
    expect(score.tracks.length).toBeGreaterThan(0);
  });

  it("すべてのパートの合計拍数が一致する（ループが揃うように）", () => {
    const beats = score.tracks.map(totalBeats);
    const first = beats[0];
    for (const b of beats) {
      expect(b).toBeCloseTo(first, 5);
    }
  });

  it("すべての音名が正しく解釈できる（不正な音名で例外が起きない）", () => {
    expect(() => flattenScore(score)).not.toThrow();
  });

  it("曲の長さが0より大きい", () => {
    expect(getScoreDurationSec(score)).toBeGreaterThan(0);
  });

  it("ループする曲として指定されている", () => {
    expect(score.loop).toBe(true);
  });
});
