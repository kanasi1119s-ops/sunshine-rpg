import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec, type Score } from "./score";
import { CHAPTER5_BOSS_THEME, CHAPTER5_CAMP_THEME, CHAPTER5_TOWN_THEME } from "./chapter5-tracks";

const SCORES: Record<string, Score> = {
  town: CHAPTER5_TOWN_THEME,
  camp: CHAPTER5_CAMP_THEME,
  boss: CHAPTER5_BOSS_THEME,
};

function totalBeats(track: Score["tracks"][number]): number {
  return track.notes.reduce((sum, n) => sum + n.durationBeats, 0);
}

describe.each(Object.entries(SCORES))("第5章のBGM: %s", (_name, score) => {
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
