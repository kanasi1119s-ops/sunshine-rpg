import { sceneResidentsFor } from "./scene-residents";
import { addYuriHome } from "./yuri-home";
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
import { addChapterDungeons } from "./dungeon-extensions";
import { addHouseInteriors } from "./house-interiors";
import { addInnInteriors } from "./inn-interiors";
import { createWorldMapData } from "../map/world/world-map";
import { convertTileBuildings } from "../map/tile-buildings";
import { addKeeperShrines, connectWorldMap, SHIP_PART_NPCS, WORLD_MAP_NPCS } from "./world-map-world";
import { ISLET_MAPS, ISLET_NPCS } from "./islets-world";
import { VILLAGE_MAPS, VILLAGE_NPCS } from "./villages-world";
import { applyAutoDecor } from "../map/auto-decor";
import { applyTownDecor } from "../map/town-decor";
import { applyTownExpansion } from "../map/town-expand";
import { applyVariantWalls } from "../map/variant-walls";
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

// 第2章〜第8章の、町とボスの間にダンジョン（洞窟・塔）を足す。模様・NPCの用意が済んだあとで、つなぎかえる
addChapterDungeons(WORLD_MAPS, WORLD_NPCS);
connectWorldMap(WORLD_MAPS, WORLD_NPCS);
addKeeperShrines(WORLD_MAPS, WORLD_NPCS);
applyTownExpansion(WORLD_MAPS);
// タイルで描いていた建物も、平屋の家の絵にする（人間の指示、2026-10-05）。宿屋・飾りを置く前に置いて、重ならないようにする
convertTileBuildings(WORLD_MAPS, WORLD_NPCS);
applyVariantWalls(WORLD_MAPS, WORLD_NPCS);
applyAutoDecor(WORLD_MAPS, WORLD_NPCS);
applyTownDecor(WORLD_MAPS, WORLD_NPCS);
// 平屋の家は、1つの絵（赤い屋根）にそろえる（2階建ての屋敷はそのまま。人間の指示「家は2階建て以外は統一しましょう」、2026-10-05）
for (const m of Object.values(WORLD_MAPS)) {
  if (!m.props) continue;
  m.props = m.props.map((p) => (p.kind === "house-blue" || p.kind === "house-green" ? { ...p, kind: "house" } : p));
}
addHouseInteriors(WORLD_MAPS, WORLD_NPCS);
addInnInteriors(WORLD_MAPS, WORLD_NPCS);
// ユーリの家（灯里の、宿屋の西どなりの家）。ふつうの家の中身を入れかえる（2026-10-06）
addYuriHome(WORLD_MAPS, WORLD_NPCS);
// 物語の場面で話す人を、その町にいる人として置く（2026-10-06）。地図と人がそろったあとで
for (const [mapId, data] of Object.entries(WORLD_MAPS)) {
  const residents = sceneResidentsFor(mapId, data, WORLD_NPCS[mapId] ?? []);
  if (residents.length) (WORLD_NPCS[mapId] ??= []).push(...residents);
}
