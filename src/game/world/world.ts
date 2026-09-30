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
import { SIDE_STORY_NPCS } from "./side-stories";
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
};

const CHAPTER_NPCS: Record<string, Npc[]> = {
  ...CHAPTER0_NPCS,
  ...CHAPTER1_NPCS,
  ...CHAPTER2_NPCS,
  ...CHAPTER3_NPCS,
  ...CHAPTER4_NPCS,
  ...CHAPTER5_NPCS,
  ...CHAPTER6_NPCS,
  ...CHAPTER7_NPCS,
  ...CHAPTER8_NPCS,
  ...CHAPTER9_NPCS,
};

/** 章のNPCに、サブストーリーの依頼人・調べる場所を足したもの。 */
export const WORLD_NPCS: Record<string, Npc[]> = Object.fromEntries(
  [...new Set([...Object.keys(CHAPTER_NPCS), ...Object.keys(SIDE_STORY_NPCS)])].map((mapId) => [
    mapId,
    [...(CHAPTER_NPCS[mapId] ?? []), ...(SIDE_STORY_NPCS[mapId] ?? [])],
  ]),
);
