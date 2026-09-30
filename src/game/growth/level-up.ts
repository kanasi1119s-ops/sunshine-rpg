import { expRequiredForLevel, levelForExp } from "./exp-curve";
import type { GrowthProfile, LeveledStats } from "./types";

export interface GainExpResult {
  stats: LeveledStats;
  levelsGained: number;
}

function applyOneLevelUp(stats: LeveledStats, growth: GrowthProfile): LeveledStats {
  return {
    ...stats,
    level: stats.level + 1,
    maxHp: stats.maxHp + growth.hpGrowth,
    hp: stats.hp + growth.hpGrowth,
    maxMp: stats.maxMp + growth.mpGrowth,
    mp: stats.mp + growth.mpGrowth,
    attack: stats.attack + growth.attackGrowth,
    defense: stats.defense + growth.defenseGrowth,
    speed: stats.speed + growth.speedGrowth,
  };
}

/** 経験値を加算し、必要ならレベルアップ分の能力値の伸びをまとめて適用する。 */
export function gainExp(stats: LeveledStats, amount: number, growth: GrowthProfile): GainExpResult {
  const newExp = stats.exp + amount;
  const newLevel = levelForExp(newExp);
  const levelsGained = newLevel - stats.level;

  let result: LeveledStats = { ...stats, exp: newExp };
  for (let i = 0; i < levelsGained; i++) {
    result = applyOneLevelUp(result, growth);
  }
  return { stats: result, levelsGained };
}

/** 初期能力値から、指定のレベルまで成長させた能力値（仲間が途中加入したときの追いつき・バランス調整のシミュレーションに使う）。 */
export function statsAtLevel(initial: LeveledStats, growth: GrowthProfile, level: number): LeveledStats {
  if (level <= initial.level) {
    return initial;
  }
  return gainExp(initial, expRequiredForLevel(level) - initial.exp, growth).stats;
}
