import { createGarasukoTownData } from "../map/chapter2/garasuko-town";
import { createGarasukoWarehouseData } from "../map/chapter2/garasuko-warehouse";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * 第2章（硝子湖）の世界。`docs/story/structure.md`「第2章（硝子湖）」・
 * `docs/story/mystery.md`（真相）を反映。
 * roadmap 4-6時点では地図のみ。イベント・NPC配置は4-7で追加する。
 */
export const CHAPTER2_MAPS: Record<string, TileMapData> = {
  "garasuko-town": createGarasukoTownData(),
  "garasuko-warehouse": createGarasukoWarehouseData(),
};

export const CHAPTER2_NPCS: Record<string, Npc[]> = {};
