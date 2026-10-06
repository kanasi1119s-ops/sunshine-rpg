import type { BattleItem } from "../battle/types";

export type StatKey = "maxHp" | "maxMp" | "attack" | "defense" | "speed";
/** 部位: ぶき・たて・あたま（兜・頭巾）・ぼうぐ・かざり。 */
export type EquipmentCategory = "weapon" | "shield" | "head" | "armor" | "accessory";

/**
 * 装備の特殊効果（ボスが落とすかざりなど）。
 * luck=運、crit=会心の出やすさ（%）、evade=敵の通常攻撃がはずれやすくなる（%）、guard=状態異常を受けない、
 * regenHp=毎ターンの終わりに最大HPの何%回復、regenMp=毎ターンの終わりにMPが回復、multi=連続攻撃に必要なすばやさの差がその分へる。
 */
export type ItemTrait =
  | { kind: "luck"; value: number }
  | { kind: "crit"; value: number }
  | { kind: "evade"; value: number }
  | { kind: "guard"; status: "poison" | "sleep" | "confuse" }
  | { kind: "regenHp"; percent: number }
  | { kind: "regenMp"; value: number }
  | { kind: "multi"; value: number };
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
  /** だれでも持てる武器（武器の種類の決まりを受けない。レジェンドの装備「コスモリングライト」）。 */
  anyWielder?: boolean;
  /** 特殊効果（省略はなし）。 */
  traits?: ItemTrait[];
  /** つけられる人のキャラクターID（省略はだれでも）。たて・兜など。 */
  wearers?: string[];
  /** 説明（装備の画面に出す）。 */
  description?: string;
}

export type ItemData = ConsumableItemData | EquipmentItemData;

export function toBattleItem(item: ConsumableItemData): BattleItem {
  return { id: item.id, name: item.name, healAmount: item.healAmount, mpAmount: item.mpAmount };
}
