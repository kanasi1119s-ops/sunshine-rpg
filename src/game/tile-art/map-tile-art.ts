import type { TileMapData } from "../map/types";

/**
 * 地図ごとの、タイルの模様の指定（`TileMapData.tileArt` に足す）。`tint:<模様>` は、その地図のタイルの色を基本色にして、
 * 石畳（flagstone）・壁（brick）・砂（sand）・雪（snow）・板張り（plank）・雲（cloud）の模様を重ねる（`tile-art.ts`）。
 * 草・水・木は、共通のドット絵（`grass` `water` `treeCanopy`）。ここに書いていないタイルは、これまでどおり色＋質感。
 */
const T = (pattern: string): string => `tint:${pattern}`;

const DUNGEON = { 1: T("flagstone"), 2: T("brick"), 3: T("brick") };

export const MAP_TILE_ART: Record<string, Record<number, string>> = {
  "touri-branch": { 1: T("plank"), 2: T("brick") },
  "garasuko-warehouse": { 1: T("plank"), 2: T("brick"), 3: T("plank") },
  "tetsukusari-mine": { 1: T("flagstone"), 2: T("brick") },
  "sanone-town": { 1: T("sand"), 2: T("sand"), 3: T("sand"), 4: "treeCanopy", 6: "water" },
  "sanone-camp": { 1: T("sand"), 2: T("sand"), 5: T("sand") },
  "kiri-town": { 1: T("flagstone"), 2: T("flagstone"), 3: T("brick"), 4: T("cloud"), 5: T("brick") },
  "kiri-archive": { 1: T("flagstone"), 2: T("brick"), 3: T("plank"), 4: T("plank") },
  "shimohara-town": { 1: T("snow"), 2: T("flagstone"), 3: T("snow"), 4: "treeCanopy" },
  "shimohara-facility": { 1: T("flagstone"), 2: T("brick") },
  "fushima-town": { 1: T("plank"), 2: T("cloud"), 4: T("plank"), 6: T("plank") },
  "fushima-base": { 1: T("flagstone"), 2: T("brick") },
  "toushin-town": { 1: T("flagstone"), 2: T("brick"), 5: "water", 6: "grass", 7: T("plank") },
  "toushin-hall": { 1: T("flagstone"), 2: T("brick"), 4: T("plank") },
  "kyotoukyu-court": DUNGEON,
  "kyotoukyu-corridor": DUNGEON,
  "kyotoukyu-sanctum": DUNGEON,
  ...Object.fromEntries(["deep-1", "deep-2", "deep-3", "deep-4", "tower-1", "tower-2", "tower-3", "kanou-1", "kanou-2", "kanou-3", "kanou-4"].map((id) => [id, DUNGEON])),
  ...Object.fromEntries(Array.from({ length: 8 }, (_, i) => [`god-shrine-${i + 1}`, DUNGEON])),
};

/** 地図データに、模様の指定を足す（すでにある指定は残す）。 */
export function applyMapTileArt(maps: Record<string, TileMapData>): void {
  for (const [mapId, art] of Object.entries(MAP_TILE_ART)) {
    const data = maps[mapId];
    if (data) {
      data.tileArt = { ...art, ...data.tileArt };
    }
  }
}
