import { CHAPTER0_MAPS, CHAPTER0_NPCS } from "./chapter0-world";
import { CHAPTER1_MAPS, CHAPTER1_NPCS } from "./chapter1-world";
import { CHAPTER2_MAPS, CHAPTER2_NPCS } from "./chapter2-world";
import { CHAPTER3_MAPS, CHAPTER3_NPCS } from "./chapter3-world";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * すべての章の地図・NPCをまとめた世界全体のレジストリ。
 * 章をまたぐ出入り口（例: 灯里の町 → 麦香野の村）を成立させるため、
 * main.ts はこちらを使う（章ごとの開始地点・オープニングは各章のworldファイルを使う）。
 */
export const WORLD_MAPS: Record<string, TileMapData> = {
  ...CHAPTER0_MAPS,
  ...CHAPTER1_MAPS,
  ...CHAPTER2_MAPS,
  ...CHAPTER3_MAPS,
};

export const WORLD_NPCS: Record<string, Npc[]> = {
  ...CHAPTER0_NPCS,
  ...CHAPTER1_NPCS,
  ...CHAPTER2_NPCS,
  ...CHAPTER3_NPCS,
};
