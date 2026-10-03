import type { TileMapData } from "../map/types";

/**
 * 地図ごとの、タイルの模様の指定（`TileMapData.tileArt` に足す）。`tint:<模様>` は、その地図のタイルの色を基本色にして、
 * 石畳（flagstone）・壁（brick）・砂（sand）・雪（snow）・板張り（plank）・雲（cloud）の模様を重ねる（`tile-art.ts`）。
 * 草・水・木は、共通のドット絵（`grass` `water` `treeCanopy`）。ここに書いていないタイルは、これまでどおり色＋質感。
 */
const T = (pattern: string): string => `tint:${pattern}`;

const DUNGEON = { 1: T("flagstone"), 2: T("brick"), 3: T("brick"), 4: T("gate"), 5: T("crystal") };
/** 虚灯宮の内部: 3=柱、4=虚（何もない暗がり）、6=光る石。 */
const KYOTOUKYU = { ...DUNGEON, 3: T("pillar"), 4: T("void"), 5: T("gate"), 6: T("crystal"), 7: T("mural"), 8: T("bed") };

export const MAP_TILE_ART: Record<string, Record<number, string>> = {
  // 町の建物（壁・屋根・扉・橋・木箱）。屋根は瓦、扉・橋・板壁は板張り、石造りは煉瓦。
  "touri-town": { 5: T("brick"), 6: T("plank"), 7: T("roof") },
  "touri-outskirts": { 5: T("flagstone"), 6: T("rift") },
  "mugikano-village": { 5: T("plank"), 6: T("roof"), 7: T("plank") },
  "mugikano-water-source": { 5: T("flagstone"), 6: T("sand") },
  "garasuko-town": { 1: T("flagstone"), 5: T("roof"), 6: T("plank") },
  "tetsukusari-town": { 1: T("flagstone"), 3: T("flagstone"), 5: T("brick"), 6: T("brick") },
  "touri-branch": { 1: T("plank"), 2: T("brick"), 3: T("plank") },
  "garasuko-warehouse": { 1: T("plank"), 2: T("brick"), 3: T("crate"), 4: T("plank") },
  "tetsukusari-mine": { 1: T("flagstone"), 2: T("brick"), 3: T("crystal"), 4: T("plank"), 5: T("plank"), 6: T("machine") },
  "sanone-town": { 1: T("sand"), 2: T("sand"), 3: T("sand"), 4: "treeCanopy", 5: T("roof"), 6: "water", 7: T("plank") },
  "sanone-camp": { 1: T("sand"), 2: T("sand"), 3: T("crate"), 4: T("plank"), 5: T("sand"), 6: T("plank") },
  "kiri-town": { 1: T("flagstone"), 2: T("flagstone"), 3: T("brick"), 4: T("cloud"), 5: T("brick"), 6: T("brick"), 7: T("plank") },
  "kiri-archive": { 1: T("flagstone"), 2: T("brick"), 3: T("plank"), 4: T("plank"), 5: T("plank") },
  "shimohara-town": { 1: T("snow"), 2: T("flagstone"), 3: T("snow"), 4: "treeCanopy", 5: T("roof"), 6: T("brick"), 7: T("plank") },
  "shimohara-facility": { 1: T("flagstone"), 2: T("brick"), 3: T("machine"), 4: T("pipe"), 5: T("plank") },
  "fushima-town": { 1: T("plank"), 2: T("cloud"), 3: T("plank"), 4: T("plank"), 5: T("plank"), 6: T("crate") },
  "fushima-base": { 1: T("flagstone"), 2: T("brick"), 3: T("machine"), 4: T("pipe"), 5: T("plank") },
  "toushin-town": { 1: T("flagstone"), 2: T("brick"), 3: T("roof"), 4: T("plank"), 5: "water", 6: "grass", 7: T("plank") },
  "toushin-hall": { 1: T("flagstone"), 2: T("brick"), 3: T("flagstone"), 4: T("plank"), 5: T("plank"), 6: T("carpet") },
  "kyotoukyu-court": KYOTOUKYU,
  "kyotoukyu-corridor": KYOTOUKYU,
  "kyotoukyu-sanctum": KYOTOUKYU,
  ...Object.fromEntries(["deep-1", "deep-2", "deep-3", "deep-4", "tower-1", "tower-2", "tower-3", "kanou-1", "kanou-2", "kanou-3", "kanou-4"].map((id) => [id, DUNGEON])),
  ...Object.fromEntries(Array.from({ length: 8 }, (_, i) => [`god-shrine-${i + 1}`, DUNGEON])),
};

/** 雪の地方の地図（木のタイルに雪をのせる）。 */
const SNOWY_MAPS = new Set(["shimohara-town"]);

/** 床と壁の描き方（`render/dungeon-tiles.ts`）を使う地図。 */
const MAP_THEME: Record<string, string> = {
  "tetsukusari-mine": "mine",
  "shimohara-facility": "facility",
  "fushima-base": "facility",
  "kiri-archive": "interior",
  "touri-branch": "interior",
  "garasuko-warehouse": "interior",
  "toushin-hall": "interior",
  ...Object.fromEntries(["tower-1", "tower-2", "tower-3"].map((id) => [id, "tower"])),
  ...Object.fromEntries(["deep-1", "deep-2", "deep-3", "deep-4", "kanou-1", "kanou-2", "kanou-3", "kanou-4"].map((id) => [id, "ruins"])),
  ...Object.fromEntries(Array.from({ length: 8 }, (_, i) => [`god-shrine-${i + 1}`, "ruins"])),
};

/** 町の建物を屋根と壁で描く地図（壁のタイルID、屋根の色、壁の色）。 */
const MAP_BUILDING: Record<string, { walls: number[]; roof: string; plaster: string }> = {
  "touri-town": { walls: [5, 7], roof: "#b4533c", plaster: "#e6d8bc" },
  "mugikano-village": { walls: [5, 6], roof: "#8a6a3a", plaster: "#e8dcb8" },
  "garasuko-town": { walls: [5], roof: "#3a6a8a", plaster: "#d8d4c4" },
  "tetsukusari-town": { walls: [5], roof: "#6a4a3a", plaster: "#c8bca4" },
  "kiri-town": { walls: [5], roof: "#5a6a8a", plaster: "#ece6d8" },
  "shimohara-town": { walls: [5], roof: "#5a7a9a", plaster: "#e4dccc" },
  "fushima-town": { walls: [4], roof: "#7a5a3a", plaster: "#d8ccb0" },
  "toushin-town": { walls: [3], roof: "#4a5a86", plaster: "#e0d8c8" },
};

/** 地図データに、模様の指定を足す（すでにある指定は残す）。 */
export function applyMapTileArt(maps: Record<string, TileMapData>): void {
  for (const [mapId, art] of Object.entries(MAP_TILE_ART)) {
    const data = maps[mapId];
    if (data) {
      data.tileArt = { ...art, ...data.tileArt };
      if (SNOWY_MAPS.has(mapId)) {
        data.snowy = true;
      }
      if (MAP_BUILDING[mapId]) {
        data.building = MAP_BUILDING[mapId];
      }
      if (MAP_THEME[mapId]) {
        data.theme = MAP_THEME[mapId];
      }
    }
  }
}
