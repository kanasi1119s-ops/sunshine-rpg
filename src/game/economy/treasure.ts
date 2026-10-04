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
  // 序盤のダンジョン（灯里の森・麦香野の坑道）の宝箱。店の1段目より少し弱い（宝箱を探す楽しみと、店で買う楽しみを両方残す）
  { id: "treasure-7", name: "古祠の短剣", category: "weapon", price: 0, statBonus: { attack: 7 }, weaponType: "dagger" },
  { id: "treasure-8", name: "森歩きの外套", category: "armor", price: 0, statBonus: { defense: 3 } },
  { id: "treasure-9", name: "樹液のお守り", category: "accessory", price: 0, statBonus: { maxHp: 7 } },
  { id: "treasure-10", name: "坑道の灯り飾り", category: "accessory", price: 0, statBonus: { maxHp: 12 } },
  // 第2〜8章のダンジョンの奥の宝箱: その章の店の武器より少し強い、仲間それぞれの専用武器（弓・斧・槍・杖・短剣・剣・弓）
  { id: "treasure-11", name: "湖鏡の弓", category: "weapon", price: 0, statBonus: { attack: 23 }, weaponType: "bow" },
  { id: "treasure-12", name: "坑道の戦斧", category: "weapon", price: 0, statBonus: { attack: 31 }, weaponType: "axe" },
  { id: "treasure-13", name: "砂嵐の槍", category: "weapon", price: 0, statBonus: { attack: 41 }, weaponType: "spear" },
  { id: "treasure-14", name: "霧織りの杖", category: "weapon", price: 0, statBonus: { attack: 52 }, weaponType: "staff" },
  { id: "treasure-15", name: "霜夜の短剣", category: "weapon", price: 0, statBonus: { attack: 64 }, weaponType: "dagger" },
  { id: "treasure-16", name: "雲渡りの剣", category: "weapon", price: 0, statBonus: { attack: 78 } },
  { id: "treasure-17", name: "灯芯都の護り弓", category: "weapon", price: 0, statBonus: { attack: 94 }, weaponType: "bow" },
];

export const TREASURE_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(
  TREASURE_ITEMS.map((item) => [item.id, item]),
);
