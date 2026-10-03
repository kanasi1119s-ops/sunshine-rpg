import type { EquipmentItemData } from "../items/types";

/**
 * 隠しダンジョンの小島の宝箱に入っている、ここでしか手に入らない装備。お店では売っていない。
 * 小島に行ける頃の店の装備より、少しだけ強い。数値は仮（自動シミュレーションはまだ）。
 * 受け取り方は `shop.ts` の `receiveTreasure`（同じ部位の今の装備より強いときだけ、その場で装備する）。
 */
export const TREASURE_ITEMS: EquipmentItemData[] = [
  { id: "treasure-1", name: "月影の護り", category: "accessory", price: 0, statBonus: { maxHp: 70 } },
  { id: "treasure-2", name: "火宿りの鎧", category: "armor", price: 0, statBonus: { defense: 40 } },
  { id: "treasure-3", name: "灯室の外套", category: "armor", price: 0, statBonus: { defense: 50 } },
  { id: "treasure-4", name: "風駆けの刃", category: "weapon", price: 0, statBonus: { attack: 90 } },
  { id: "treasure-5", name: "潮読みの腕輪", category: "accessory", price: 0, statBonus: { maxHp: 120 } },
  { id: "treasure-6", name: "紅炎の剣", category: "weapon", price: 0, statBonus: { attack: 98 } },
];

export const TREASURE_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(
  TREASURE_ITEMS.map((item) => [item.id, item]),
);
