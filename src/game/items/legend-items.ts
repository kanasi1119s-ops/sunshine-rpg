import type { EquipmentItemData } from "./types";

/**
 * レジェンドの装備（2026-10-06）。
 * コスモリングライト（はじめの名前は「コスモ」。2026-10-06 人間の指示で改名。IDは legend-cosmo のまま）: 隠しボス「機械の悪神巨人兵」を倒すと手に入る、だれでも装備できる鎧の形の武器（ぶきの欄につける）。
 * 力・見た目・名前のくわしいところは、人間と「この後じっくり決める」ことになっている（数値・説明は仮）。
 */
export const COSMO_ID = "legend-cosmo";

export const LEGEND_ITEMS: EquipmentItemData[] = [
  {
    id: COSMO_ID,
    name: "コスモリングライト",
    category: "weapon",
    price: 0,
    anyWielder: true,
    statBonus: { attack: 60, defense: 40, maxHp: 120 },
    description: "（仮）世界の調停者が遺した、光の環の鎧。まわりに6基の追尾砲台が浮かぶ。だれでも装備できる。くわしい力は、これから決める。",
  },
];

export const LEGEND_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(LEGEND_ITEMS.map((i) => [i.id, i]));
