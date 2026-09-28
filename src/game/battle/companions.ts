import type { GrowthProfile, LeveledStats } from "../growth/types";
import type { Combatant, Skill } from "./types";

/**
 * 仲間キャラクターのデータ。装備システムはまだ仲間には対応していない
 * （ヒーロー＝ユーリのみ。今後の課題）。とくぎは1人1つの固定。
 */
export interface CompanionDefinition {
  id: string;
  name: string;
  growth: GrowthProfile;
  skill: Skill;
  createInitialStats: () => LeveledStats;
}

/** レト（灯里支部の先輩調査員）。序章で仲間に加わる。実戦派で、共鳴術ではなく体術のとくぎを使う。 */
export const RETO: CompanionDefinition = {
  id: "reto",
  name: "レト",
  growth: { hpGrowth: 4, mpGrowth: 1, attackGrowth: 3, defenseGrowth: 2, speedGrowth: 2 },
  skill: { id: "mikiri-no-ichigeki", name: "見切りの一撃", mpCost: 2, powerMultiplier: 1.8 },
  createInitialStats: () => ({
    level: 1,
    exp: 0,
    maxHp: 26,
    hp: 26,
    maxMp: 6,
    mp: 6,
    attack: 13,
    defense: 7,
    speed: 11,
  }),
};

export const COMPANIONS: Record<string, CompanionDefinition> = {
  [RETO.id]: RETO,
};

export function createCompanionCombatant(companion: CompanionDefinition, stats: LeveledStats): Combatant {
  return {
    id: companion.id,
    name: `${companion.name} Lv${stats.level}`,
    maxHp: stats.maxHp,
    hp: stats.hp,
    maxMp: stats.maxMp,
    mp: stats.mp,
    attack: stats.attack,
    defense: stats.defense,
    speed: stats.speed,
    isEnemy: false,
    guarding: false,
  };
}
