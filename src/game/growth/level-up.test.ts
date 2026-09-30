import { describe, expect, it } from "vitest";
import { gainExp } from "./level-up";
import { expRequiredForLevel } from "./exp-curve";
import type { GrowthProfile, LeveledStats } from "./types";

const growth: GrowthProfile = {
  hpGrowth: 5,
  mpGrowth: 2,
  attackGrowth: 3,
  defenseGrowth: 1,
  speedGrowth: 1,
};

function makeStats(): LeveledStats {
  return { level: 1, exp: 0, maxHp: 20, hp: 20, maxMp: 5, mp: 5, attack: 8, defense: 4, speed: 6 };
}

describe("gainExp", () => {
  it("レベルアップに満たない経験値では、経験値だけ増えて能力値は変わらない", () => {
    const result = gainExp(makeStats(), 1, growth);
    expect(result.levelsGained).toBe(0);
    expect(result.stats.exp).toBe(1);
    expect(result.stats.maxHp).toBe(20);
  });

  it("必要経験値ちょうどでレベルが1つ上がり、能力値が成長する", () => {
    const need = expRequiredForLevel(2);
    const result = gainExp(makeStats(), need, growth);
    expect(result.levelsGained).toBe(1);
    expect(result.stats.level).toBe(2);
    expect(result.stats.maxHp).toBe(25);
    expect(result.stats.hp).toBe(25);
    expect(result.stats.attack).toBe(11);
  });

  it("大量の経験値で複数レベル分まとめて成長する", () => {
    const need = expRequiredForLevel(4);
    const result = gainExp(makeStats(), need, growth);
    expect(result.levelsGained).toBe(3);
    expect(result.stats.level).toBe(4);
    expect(result.stats.maxHp).toBe(20 + 5 * 3);
    expect(result.stats.attack).toBe(8 + 3 * 3);
  });
});

import { statsAtLevel } from "./level-up";
describe("statsAtLevel（指定のレベルまで成長させる）", () => {
  const growth = { hpGrowth: 5, mpGrowth: 2, attackGrowth: 2, defenseGrowth: 1, speedGrowth: 1 };
  const initial = { level: 1, exp: 0, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 12, defense: 6, speed: 9 };
  it("レベルNでは、初期値に(N-1)回ぶんの伸びを足した値になる", () => {
    const result = statsAtLevel(initial, growth, 10);
    expect(result.level).toBe(10);
    expect(result.maxHp).toBe(30 + 5 * 9);
    expect(result.attack).toBe(12 + 2 * 9);
    expect(result.defense).toBe(6 + 9);
  });
  it("いまのレベル以下を指定しても、そのまま", () => {
    expect(statsAtLevel(initial, growth, 1)).toEqual(initial);
  });
});
