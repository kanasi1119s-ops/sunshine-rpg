import { CHAPTER0_MAPS, CHAPTER0_NPCS } from "./chapter0-world";
import { CHAPTER1_MAPS, CHAPTER1_NPCS } from "./chapter1-world";
import { CHAPTER2_MAPS, CHAPTER2_NPCS } from "./chapter2-world";
import { CHAPTER3_MAPS, CHAPTER3_NPCS } from "./chapter3-world";
import { CHAPTER4_MAPS, CHAPTER4_NPCS } from "./chapter4-world";
import { CHAPTER5_MAPS, CHAPTER5_NPCS } from "./chapter5-world";
import { CHAPTER6_MAPS, CHAPTER6_NPCS } from "./chapter6-world";
import { CHAPTER7_MAPS, CHAPTER7_NPCS } from "./chapter7-world";
import { CHAPTER8_MAPS, CHAPTER8_NPCS } from "./chapter8-world";
import { CHAPTER9_MAPS, CHAPTER9_NPCS } from "./chapter9-world";
import { CHAPTER10_MAPS, CHAPTER10_NPCS } from "./chapter10-world";
import { CHAPTER11_MAPS, CHAPTER11_NPCS } from "./chapter11-world";
import { CHAPTER12_MAPS, CHAPTER12_NPCS } from "./chapter12-world";
import { SIDE_STORY_NPCS } from "./side-stories";
import { SHOP_NPCS } from "./shops-world";
import { AMBIENT_NPCS } from "./ambient-world";
import { applyMapTileArt } from "../tile-art/map-tile-art";
import { applyMapProps } from "../map/map-props";
import { createWorldMapData } from "../map/world/world-map";
import { connectWorldMap, SHIP_PART_NPCS, WORLD_MAP_NPCS } from "./world-map-world";
import { ISLET_MAPS, ISLET_NPCS } from "./islets-world";
import { VILLAGE_MAPS, VILLAGE_NPCS } from "./villages-world";
import { applyAutoDecor } from "../map/auto-decor";
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
  ...CHAPTER4_MAPS,
  ...CHAPTER5_MAPS,
  ...CHAPTER6_MAPS,
  ...CHAPTER7_MAPS,
  ...CHAPTER8_MAPS,
  ...CHAPTER9_MAPS,
  ...CHAPTER10_MAPS,
  ...CHAPTER11_MAPS,
  ...CHAPTER12_MAPS,
  "world-map": createWorldMapData(),
  ...ISLET_MAPS,
  ...VILLAGE_MAPS,
};

applyMapTileArt(WORLD_MAPS);
applyMapProps(WORLD_MAPS);

const NPC_SOURCES: Record<string, Npc[]>[] = [
  CHAPTER0_NPCS,
  CHAPTER1_NPCS,
  CHAPTER2_NPCS,
  CHAPTER3_NPCS,
  CHAPTER4_NPCS,
  CHAPTER5_NPCS,
  CHAPTER6_NPCS,
  CHAPTER7_NPCS,
  CHAPTER8_NPCS,
  CHAPTER9_NPCS,
  CHAPTER10_NPCS,
  CHAPTER11_NPCS,
  CHAPTER12_NPCS,
  WORLD_MAP_NPCS,
  SHIP_PART_NPCS,
  ISLET_NPCS,
  VILLAGE_NPCS,
  SIDE_STORY_NPCS,
  SHOP_NPCS,
  AMBIENT_NPCS,
];

/** 章のNPC・サブストーリーの依頼人・8神の禁域の入口などを、地図ごとに1つにまとめたもの。 */
export const WORLD_NPCS: Record<string, Npc[]> = (() => {
  const merged: Record<string, Npc[]> = {};
  for (const source of NPC_SOURCES) {
    for (const [mapId, npcs] of Object.entries(source)) {
      (merged[mapId] ??= []).push(...npcs);
    }
  }
  return merged;
})();

connectWorldMap(WORLD_MAPS, WORLD_NPCS);
applyAutoDecor(WORLD_MAPS, WORLD_NPCS);
