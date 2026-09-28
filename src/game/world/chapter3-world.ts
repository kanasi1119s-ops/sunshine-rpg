import { createTetsukusariMineData } from "../map/chapter3/tetsukusari-mine";
import { createTetsukusariTownData } from "../map/chapter3/tetsukusari-town";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * 第3章（鉄鏈鉱山）の世界。`docs/story/structure.md`「第3章（鉄鏈鉱山）」・
 * `docs/story/mystery.md` を参照。
 * 今回（roadmap 4-11）は地図データのみ。NPC・イベント・依頼は 4-12 で追加する。
 */
export const CHAPTER3_MAPS: Record<string, TileMapData> = {
  "tetsukusari-town": createTetsukusariTownData(),
  "tetsukusari-mine": createTetsukusariMineData(),
};

export const CHAPTER3_NPCS: Record<string, Npc[]> = {};
