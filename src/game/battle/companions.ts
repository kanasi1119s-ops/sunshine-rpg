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

/** ミナ（麦香野出身、水紋系の使い手）。第1章で仲間に加わる。 */
export const MINA: CompanionDefinition = {
  id: "mina",
  name: "ミナ",
  growth: { hpGrowth: 3, mpGrowth: 3, attackGrowth: 2, defenseGrowth: 2, speedGrowth: 2 },
  skill: { id: "suimon-no-nami", name: "水紋ノ波", mpCost: 3, powerMultiplier: 1.5 },
  createInitialStats: () => ({
    level: 1,
    exp: 0,
    maxHp: 24,
    hp: 24,
    maxMp: 10,
    mp: 10,
    attack: 11,
    defense: 6,
    speed: 10,
  }),
};

export const COMPANIONS: Record<string, CompanionDefinition> = {
  [RETO.id]: RETO,
  [MINA.id]: MINA,
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
