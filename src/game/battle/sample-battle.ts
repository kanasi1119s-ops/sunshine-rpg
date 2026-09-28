import type { BattleItem, Combatant, Skill } from "./types";
import type { GrowthProfile, LeveledStats } from "../growth/types";
import type { EquipmentItemData, ItemData } from "../items/types";
import { createEquipmentSlots, equip, type EquipmentSlots } from "../items/equipment";

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

export const SAMPLE_WEAPON: EquipmentItemData = {
  id: "sword",
  name: "使い込まれた鉄の剣",
  category: "weapon",
  price: 100,
  statBonus: { attack: 4 },
};

export const SAMPLE_ITEMS_BY_ID: Record<string, ItemData> = {
  [SAMPLE_WEAPON.id]: SAMPLE_WEAPON,
};

/** 動作確認用に、最初から剣を装備した状態にしておく。 */
export function createInitialEquipment(): EquipmentSlots {
  return equip(createEquipmentSlots(), SAMPLE_WEAPON);
}

/**
 * effectiveStats には、装備ボーナスをすでに足した「今の実力」を渡す
 * （表示名のレベルは基本能力値=heroStats.level を使う）。
 */
export function createSampleParty(heroLevel: number, effectiveStats: LeveledStats): Combatant[] {
  return [
    {
      id: "hero",
      name: `ゆうしゃ（仮） Lv${heroLevel}`,
      maxHp: effectiveStats.maxHp,
      hp: effectiveStats.hp,
      maxMp: effectiveStats.maxMp,
      mp: effectiveStats.mp,
      attack: effectiveStats.attack,
      defense: effectiveStats.defense,
      speed: effectiveStats.speed,
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
