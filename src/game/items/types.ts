import type { BattleItem } from "../battle/types";

export type StatKey = "maxHp" | "maxMp" | "attack" | "defense" | "speed";
export type EquipmentCategory = "weapon" | "armor" | "accessory";

export interface ConsumableItemData {
  id: string;
  name: string;
  category: "consumable";
  price: number;
  healAmount: number;
}

export interface EquipmentItemData {
  id: string;
  name: string;
  category: EquipmentCategory;
  price: number;
  statBonus: Partial<Record<StatKey, number>>;
}

export type ItemData = ConsumableItemData | EquipmentItemData;

export function toBattleItem(item: ConsumableItemData): BattleItem {
  return { id: item.id, name: item.name, healAmount: item.healAmount };
}
