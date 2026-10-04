import type { BattleItem } from "../battle/types";

export type StatKey = "maxHp" | "maxMp" | "attack" | "defense" | "speed";
export type EquipmentCategory = "weapon" | "armor" | "accessory";
/** 武器の種類。キャラクターごとに、持てる種類が決まっている（`weapon-types.ts`）。 */
export type WeaponType = "sword" | "dagger" | "staff" | "bow" | "axe" | "spear";

export interface ConsumableItemData {
  id: string;
  name: string;
  category: "consumable";
  price: number;
  healAmount: number;
  /** MPを回復する量（省略は0）。 */
  mpAmount?: number;
  /** 説明（もちもの・店に出す）。 */
  description?: string;
}

export interface EquipmentItemData {
  id: string;
  name: string;
  category: EquipmentCategory;
  price: number;
  statBonus: Partial<Record<StatKey, number>>;
  /** 武器のときの種類（省略は剣）。 */
  weaponType?: WeaponType;
}

export type ItemData = ConsumableItemData | EquipmentItemData;

export function toBattleItem(item: ConsumableItemData): BattleItem {
  return { id: item.id, name: item.name, healAmount: item.healAmount, mpAmount: item.mpAmount };
}
