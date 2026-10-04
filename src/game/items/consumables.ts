import type { ConsumableItemData } from "./types";

/**
 * 回復アイテム（消費アイテム）。戦闘中の「どうぐ」・もちもの画面から使う。店（道具屋）で買える。
 * 名前は、このゲームの「灯り」「雫」にちなんだ完全オリジナル（既存作の回復アイテム名は使わない。CLAUDE.md 1-1）。数値は仮。
 */
export const CONSUMABLE_ITEMS: ConsumableItemData[] = [
  { id: "akarigusa", name: "灯り草", category: "consumable", price: 8, healAmount: 20, description: "HPを20回復" },
  { id: "akari-gusuri", name: "灯り薬", category: "consumable", price: 30, healAmount: 60, description: "HPを60回復" },
  { id: "kagayaki-gusuri", name: "輝き薬", category: "consumable", price: 90, healAmount: 150, description: "HPを150回復" },
  { id: "zenkai-no-akari", name: "全快の灯", category: "consumable", price: 260, healAmount: 9999, description: "HPを全回復" },
  { id: "tsuyu-no-shizuku", name: "露の雫", category: "consumable", price: 25, healAmount: 0, mpAmount: 15, description: "MPを15回復" },
  { id: "hoshi-no-shizuku", name: "星の雫", category: "consumable", price: 80, healAmount: 0, mpAmount: 40, description: "MPを40回復" },
];

export const CONSUMABLES_BY_ID: Record<string, ConsumableItemData> = Object.fromEntries(CONSUMABLE_ITEMS.map((i) => [i.id, i]));

/** 1種類を持てる数の上限。 */
export const MAX_CONSUMABLE_STACK = 99;

/** 新しい旅のはじめに持っている回復アイテム。 */
export const STARTER_CONSUMABLES: Array<{ itemId: string; quantity: number }> = [{ itemId: "akarigusa", quantity: 3 }];

/** 道具屋（店ID `items-1`〜`items-9`）に並べる品。町が進むほど、強い薬が増える。 */
const STOCK_FROM_TIER: Record<string, number> = {
  "akarigusa": 1, "tsuyu-no-shizuku": 1, "akari-gusuri": 3, "hoshi-no-shizuku": 4, "kagayaki-gusuri": 5, "zenkai-no-akari": 7,
};
export function consumableStock(tier: number): ConsumableItemData[] {
  return CONSUMABLE_ITEMS.filter((i) => tier >= (STOCK_FROM_TIER[i.id] ?? 99));
}
