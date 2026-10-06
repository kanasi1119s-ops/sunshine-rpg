import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 町の武具屋（灯貨で装備を買う）。町の順に1段ずつ強い装備を売る（`src/game/economy/shop.ts`）。
 * 仮: 店の人のセリフは簡易。
 */
const SHOP_TOWNS: { mapId: string; tier: number; tileX: number; tileY: number; keeper: string }[] = [
  { mapId: "touri-town", tier: 1, tileX: 11, tileY: 4, keeper: "灯里の武具屋" },
  { mapId: "mugikano-village", tier: 2, tileX: 11, tileY: 4, keeper: "麦香野の行商人" },
  { mapId: "garasuko-town", tier: 3, tileX: 11, tileY: 4, keeper: "湖上市場の武具屋" },
  { mapId: "tetsukusari-town", tier: 4, tileX: 11, tileY: 4, keeper: "鉱山の鍛冶屋" },
  { mapId: "sanone-town", tier: 5, tileX: 11, tileY: 4, keeper: "砂音の武具商" },
  { mapId: "kiri-town", tier: 6, tileX: 14, tileY: 9, keeper: "霧断崖の武具屋" },
  { mapId: "shimohara-town", tier: 7, tileX: 11, tileY: 4, keeper: "霜原の武具屋" },
  { mapId: "fushima-town", tier: 8, tileX: 11, tileY: 4, keeper: "浮嶼の職人" },
  { mapId: "toushin-town", tier: 9, tileX: 11, tileY: 4, keeper: "灯芯都の名工" },
];

export const SHOP_NPCS: Record<string, Npc[]> = Object.fromEntries(
  SHOP_TOWNS.map((town) => [
    town.mapId,
    [
      {
        id: `shop-${town.tier}`,
        tileX: town.tileX,
        tileY: town.tileY,
        color: "#d0a050",
        commands: [
          say(town.keeper, "いらっしゃい。旅の装備や、傷を治す薬もそろっているよ。"),
          {
            type: "choice" as const,
            text: "買い物をしますか？",
            options: [
              { label: "武具を見る", commands: [{ type: "shop" as const, shopId: `tier-${town.tier}` }] },
              { label: "どうぐを見る", commands: [{ type: "shop" as const, shopId: `items-${town.tier}` }] },
              { label: "やめておく", commands: [say(town.keeper, "また来てくれよ。")] },
            ],
          },
        ],
      },
    ],
  ]),
);
