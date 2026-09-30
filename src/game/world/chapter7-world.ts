import { createFushimaBaseData } from "../map/chapter7/fushima-base";
import { createFushimaTownData } from "../map/chapter7/fushima-town";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * 第7章（浮嶼）の世界。`docs/story/structure.md`「第7章（浮嶼）」・`docs/story/mystery.md`を反映。
 * 今回（roadmap 4-31）は地図のみ。イベント・空の乗り物の入手は4-32で追加する（NPCはまだ空）。
 */
export const CHAPTER7_MAPS: Record<string, TileMapData> = {
  "fushima-town": createFushimaTownData(),
  "fushima-base": createFushimaBaseData(),
};

export const CHAPTER7_NPCS: Record<string, Npc[]> = {
  "fushima-town": [],
  "fushima-base": [],
};
