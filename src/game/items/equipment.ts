import type { LeveledStats } from "../growth/types";
import type { EquipmentCategory, EquipmentItemData, ItemData, StatKey } from "./types";

export type EquipmentSlots = Partial<Record<EquipmentCategory, string>>;

export function createEquipmentSlots(): EquipmentSlots {
  return {};
}

export function equip(slots: EquipmentSlots, item: EquipmentItemData): EquipmentSlots {
  return { ...slots, [item.category]: item.id };
}

export function unequip(slots: EquipmentSlots, category: EquipmentCategory): EquipmentSlots {
  const next = { ...slots };
  delete next[category];
  return next;
}

export type StatBonus = Partial<Record<StatKey, number>>;

function isEquipment(item: ItemData): item is EquipmentItemData {
  return item.category !== "consumable";
}

/** 現在装備している品の能力値ボーナスを合計する。 */
export function computeEquipmentBonus(
  slots: EquipmentSlots,
  itemsById: Record<string, ItemData>,
): StatBonus {
  const bonus: StatBonus = {};
  for (const itemId of Object.values(slots)) {
    if (!itemId) {
      continue;
    }
    const item = itemsById[itemId];
    if (!item || !isEquipment(item)) {
      continue;
    }
    for (const [key, value] of Object.entries(item.statBonus) as [StatKey, number][]) {
      bonus[key] = (bonus[key] ?? 0) + value;
    }
  }
  return bonus;
}

/**
 * レベルで決まる基本能力値に、装備ボーナスを足した「今の実力」を計算する。
 * 基本能力値そのものは変えない（装備は着せ替え自由にするため）。
 */
export function applyStatBonus(base: LeveledStats, bonus: StatBonus): LeveledStats {
  const maxHp = base.maxHp + (bonus.maxHp ?? 0);
  const maxMp = base.maxMp + (bonus.maxMp ?? 0);
  return {
    ...base,
    maxHp,
    hp: Math.min(base.hp + (bonus.maxHp ?? 0), maxHp),
    maxMp,
    mp: Math.min(base.mp + (bonus.maxMp ?? 0), maxMp),
    attack: base.attack + (bonus.attack ?? 0),
    defense: base.defense + (bonus.defense ?? 0),
    speed: base.speed + (bonus.speed ?? 0),
  };
}
