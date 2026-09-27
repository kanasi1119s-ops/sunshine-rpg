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
