import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { describeBonus } from "../economy/shop";
import { TREASURE_ITEMS_BY_ID } from "../economy/treasure";

/**
 * ダンジョンの仕掛け（宝箱・レバー・調べる石碑）を、短く書くための道具。
 * IDに「chest」「panel」「lore」などの言葉が入ると、人ではなく物として描かれる（`character-specs.ts`）。
 */
const say = (text: string, speaker?: string): EventCommand => ({ type: "message", text, speaker });

export interface ChestReward {
  gold?: number;
  /** 宝の装備のID（`economy/treasure.ts`）。 */
  equipmentId?: string;
}

/** 宝箱。一度開けたら、フラグが立って空になる。 */
export function chestNpc(id: string, tile: { tileX: number; tileY: number }, flag: string, reward: ChestReward, openText = "宝箱を開けた！"): Npc {
  const gain: EventCommand[] = [];
  if (reward.gold) {
    gain.push({ type: "giveGold", amount: reward.gold }, say(`【ごほうび】灯貨${reward.gold}を手に入れた！`));
  }
  if (reward.equipmentId) {
    const item = TREASURE_ITEMS_BY_ID[reward.equipmentId];
    gain.push(
      { type: "giveEquipment", itemId: reward.equipmentId },
      say(`【ごほうび】${item.name}を手に入れた！（${describeBonus(item)}）強ければ、その場で身につけた。`),
    );
  }
  return {
    id,
    ...tile,
    color: "#e8c860",
    commands: [
      {
        type: "if",
        flag,
        equals: true,
        then: [say("宝箱は、すでに空だ。")],
        else: [say(openText), ...gain, { type: "setFlag", flag, value: true }],
      },
    ],
  };
}

/** レバー（石の台）。2つとも動かすと、`openFlag` が立って仕掛けが開く。 */
export function leverNpc(
  id: string,
  tile: { tileX: number; tileY: number },
  ownFlag: string,
  otherFlag: string,
  openFlag: string,
  texts: { pull: string; already: string; opened: string; waiting: string },
): Npc {
  return {
    id,
    ...tile,
    color: "#8a9ab0",
    commands: [
      {
        type: "if",
        flag: ownFlag,
        equals: true,
        then: [say(texts.already)],
        else: [
          say(texts.pull),
          { type: "setFlag", flag: ownFlag, value: true },
          {
            type: "if",
            flag: otherFlag,
            equals: true,
            then: [say(texts.opened), { type: "setFlag", flag: openFlag, value: true }],
            else: [say(texts.waiting)],
          },
        ],
      },
    ],
  };
}

/** 調べると文が出る物（看板・石碑・壁画など）。 */
export function loreNpc(id: string, tile: { tileX: number; tileY: number }, lines: string[], setFlagOnRead?: string): Npc {
  const commands: EventCommand[] = lines.map((t) => say(t));
  if (setFlagOnRead) commands.push({ type: "setFlag", flag: setFlagOnRead, value: true });
  return { id, ...tile, color: "#a0a0b0", commands };
}
