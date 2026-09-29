import { createShimoharaFacilityData } from "../map/chapter6/shimohara-facility";
import { createShimoharaTownData } from "../map/chapter6/shimohara-town";
import type { TileMapData } from "../map/types";
import type { Npc } from "../npc";

/**
 * 第6章（霜原）の世界。`docs/story/structure.md`「第6章（霜原）」・`docs/story/mystery.md`を反映。
 * 今回（roadmap 4-26）は地図のみ。イベント・アヤメ加入は4-27で追加する（NPCはまだ空）。
 */
export const CHAPTER6_MAPS: Record<string, TileMapData> = {
  "shimohara-town": createShimoharaTownData(),
  "shimohara-facility": createShimoharaFacilityData(),
};

export const CHAPTER6_NPCS: Record<string, Npc[]> = {
  "shimohara-town": [],
  "shimohara-facility": [],
};
