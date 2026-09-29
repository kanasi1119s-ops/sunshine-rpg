import { createSanoneCampData } from "../map/chapter4/sanone-camp";
import { createSanoneTownData } from "../map/chapter4/sanone-town";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * 第4章（砂音）の世界。`docs/story/structure.md`「第4章（砂音）」・`docs/story/mystery.md`を反映。
 * 地図のみ（roadmap 4-16）。NPC・イベント・伏線（C-005回収・C-008）は4-17で追加する。
 */
export const CHAPTER4_MAPS: Record<string, TileMapData> = {
  "sanone-town": createSanoneTownData(),
  "sanone-camp": createSanoneCampData(),
};

export const CHAPTER4_NPCS: Record<string, Npc[]> = {};
