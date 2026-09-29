import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec } from "./score";
import { SE_LIBRARY } from "./se-library";

describe("効果音ライブラリ", () => {
  it("IDが重複せず、50種類ほどそろっている", () => {
    const ids = SE_LIBRARY.map((e) => e.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ids.length).toBeGreaterThanOrEqual(45);
  });
  it("戦闘・逃走・レベルアップなど、よくある効果音が入っている", () => {
    const ids = SE_LIBRARY.map((e) => e.id);
    for (const id of ["attack", "hit", "critical", "miss", "heal", "fire", "flee", "encounter", "level-up", "victory", "defeat", "chest", "footstep", "cursor", "confirm", "cancel"]) {
      expect(ids).toContain(id);
    }
  });
  it.each(SE_LIBRARY.map((e) => [e.id, e] as const))("%s: 読めて、2〜4秒で、ループしない", (_id, e) => {
    expect(() => flattenScore(e.score)).not.toThrow();
    const sec = getScoreDurationSec(e.score);
    expect(sec).toBeGreaterThanOrEqual(2);
    expect(sec).toBeLessThanOrEqual(4);
    expect(e.score.loop).toBe(false);
  });
});
