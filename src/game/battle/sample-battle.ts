import type { BattleItem, Combatant, Skill } from "./types";
import type { GrowthProfile, LeveledStats } from "../growth/types";

/** 戦闘システムの動作確認用データ。本物のパーティ・敵はフェーズ2以降で作る。 */
export const SAMPLE_SKILL: Skill = { id: "test-skill", name: "とくぎ（仮）", mpCost: 3, powerMultiplier: 1.6 };
export const SAMPLE_ITEM: BattleItem = { id: "test-item", name: "やくそう（仮）", healAmount: 20 };

export const SAMPLE_GROWTH: GrowthProfile = {
  hpGrowth: 5,
  mpGrowth: 2,
  attackGrowth: 2,
  defenseGrowth: 1,
  speedGrowth: 1,
};

export function createInitialHeroStats(): LeveledStats {
  return { level: 1, exp: 0, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 12, defense: 6, speed: 9 };
}

export function createSampleParty(heroStats: LeveledStats): Combatant[] {
  return [
    {
      id: "hero",
      name: `ゆうしゃ（仮） Lv${heroStats.level}`,
      maxHp: heroStats.maxHp,
      hp: heroStats.hp,
      maxMp: heroStats.maxMp,
      mp: heroStats.mp,
      attack: heroStats.attack,
      defense: heroStats.defense,
      speed: heroStats.speed,
      isEnemy: false,
      guarding: false,
    },
  ];
}

export function createSampleEnemies(): Combatant[] {
  return [
    {
      id: "slime-1",
      name: "スライム（仮）",
      maxHp: 18,
      hp: 18,
      maxMp: 0,
      mp: 0,
      attack: 6,
      defense: 2,
      speed: 5,
      isEnemy: true,
      guarding: false,
      expReward: 12,
    },
  ];
}
