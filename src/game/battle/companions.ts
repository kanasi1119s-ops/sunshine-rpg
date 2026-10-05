import { allyLuck } from "./luck";
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
  /** もともと使える、とくぎ以外の魔法（魔法使い枠）。minLevel 以上で使える。ジョブで覚える特技とは別。 */
  extraSkills?: { minLevel: number; skill: Skill }[];
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
  // 魔法使い枠（初級）。上の呪文は、ジョブ（水紋術士など）で覚える
  extraSkills: [
    { minLevel: 1, skill: { id: "shizuku-no-megumi", name: "雫ノ恵み", mpCost: 4, powerMultiplier: 1, effect: "heal", healRatio: 2.6 } },
    { minLevel: 4, skill: { id: "konami-no-retsu", name: "小波ノ列", mpCost: 6, powerMultiplier: 0.9, effect: "damageAll" } },
  ],
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

/** コハク（硝子湖の交易商人の娘、風唱系）。第2章で仲間に加わる。すばしっこく、風のとくぎで援護する。 */
export const GUIDE: CompanionDefinition = {
  id: "guide",
  name: "コハク",
  growth: { hpGrowth: 3, mpGrowth: 2, attackGrowth: 3, defenseGrowth: 1, speedGrowth: 3 },
  skill: { id: "shippu-no-ya", name: "疾風ノ矢", mpCost: 3, powerMultiplier: 1.6 },
  createInitialStats: () => ({
    level: 1,
    exp: 0,
    maxHp: 23,
    hp: 23,
    maxMp: 8,
    mp: 8,
    attack: 12,
    defense: 5,
    speed: 13,
  }),
};

/** オルカ（鉄鏈鉱山出身、地固系の元鉱山労働者）。第3章で仲間に加わる。打たれ強く、重い一撃で押す。 */
export const ORCA: CompanionDefinition = {
  id: "orca",
  name: "オルカ",
  growth: { hpGrowth: 5, mpGrowth: 1, attackGrowth: 3, defenseGrowth: 3, speedGrowth: 1 },
  skill: { id: "iwakudaki-no-ikki", name: "岩砕きの一撃", mpCost: 3, powerMultiplier: 1.7 },
  createInitialStats: () => ({
    level: 1,
    exp: 0,
    maxHp: 32,
    hp: 32,
    maxMp: 6,
    mp: 6,
    attack: 14,
    defense: 9,
    speed: 7,
  }),
};

/** アヤメ（霜原の案内人、光断系）。第6章で仲間に加わる。すばやく、鋭い一閃で急所を突く。 */
export const AYAME: CompanionDefinition = {
  id: "ayame",
  name: "アヤメ",
  growth: { hpGrowth: 3, mpGrowth: 2, attackGrowth: 3, defenseGrowth: 2, speedGrowth: 3 },
  skill: { id: "koudan-no-issen", name: "光断ノ一閃", mpCost: 3, powerMultiplier: 1.7 },
  // 魔法使い枠（初級）。上の呪文は、ジョブで覚える
  extraSkills: [
    { minLevel: 1, skill: { id: "toukou-no-megumi", name: "灯光ノ恵み", mpCost: 4, powerMultiplier: 1, effect: "heal", healRatio: 2.6 } },
    { minLevel: 1, skill: { id: "koudan-no-ren", name: "光断ノ連", mpCost: 5, powerMultiplier: 1.0, effect: "multi", hits: 2 } },
  ],
  createInitialStats: () => ({
    level: 1,
    exp: 0,
    maxHp: 25,
    hp: 25,
    maxMp: 9,
    mp: 9,
    attack: 13,
    defense: 6,
    speed: 12,
  }),
};

export const COMPANIONS: Record<string, CompanionDefinition> = {
  [RETO.id]: RETO,
  [MINA.id]: MINA,
  [GUIDE.id]: GUIDE,
  [ORCA.id]: ORCA,
  [AYAME.id]: AYAME,
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
    luck: allyLuck(companion.id, stats.level),
    isEnemy: false,
    guarding: false,
  };
}
