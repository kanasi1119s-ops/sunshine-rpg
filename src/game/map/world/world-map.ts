import type { TileMapData } from "../types";
import { WORLD_HEIGHT, WORLD_ROWS, WORLD_TOWNS, WORLD_WIDTH } from "./world-map.generated";
import type { MapProp } from "../types";

/** 町のアイコンの絵（町ごと）。 */
const TOWN_ICON: Record<string, MapProp["kind"]> = {
  "touri-town": "icon-port",
  "mugikano-village": "icon-village",
  "garasuko-town": "icon-lake",
  "tetsukusari-town": "icon-mine",
  "toushin-town": "icon-castle",
  "sanone-town": "icon-tents",
  "kiri-town": "icon-temple",
  "shimohara-town": "icon-snowtown",
  "fushima-town": "icon-sky",
  "kyotoukyu-court": "icon-palace",
};

/**
 * 世界地図（大陸アルテシア）。上から見た大陸を歩く。町・遺跡のアイコンの上に乗ると、その場所へ入る（出入り口は `world.ts` で、
 * 各町の南の門とつなぐ）。地形は `tools/world-map/gen_world.py` で作った `world-map.generated.ts`。
 * 山・海・湖は通れない。道は、町と町をつなぐ（山脈は道だけが越える）。
 */
const GLYPH_TO_ID: Record<string, number> = { O: 1, P: 2, F: 3, M: 4, D: 5, S: 6, R: 7, H: 8, L: 9, C: 10, W: 11, T: 12 };

const TILE_COLORS: Record<number, string> = {
  1: "#1e5a96", 2: "#4a9a3a", 3: "#2f7a2a", 4: "#857c74", 5: "#d9bf82", 6: "#e8eef2", 7: "#b3853f", 8: "#5a9a40", 9: "#2f6fb0", 10: "#cfe3f2", 11: "#5a4a6a", 12: "#3a6a50",
};

const TILE_ART_MAP: Record<number, string> = {
  1: "water", 2: "grass", 3: "worldforest", 4: "mountain", 5: "tint:sand", 6: "tint:snow", 7: "path", 8: "hills", 9: "water", 10: "tint:cloud", 11: "tint:flagstone", 12: "snowforest",
};

/** 通れない地形: 海・山・湖。 */
const BLOCKED = new Set([1, 4, 9]);

export function createWorldMapData(): TileMapData {
  const ground = new Array(WORLD_WIDTH * WORLD_HEIGHT).fill(1);
  const collision = new Array(WORLD_WIDTH * WORLD_HEIGHT).fill(0);
  for (let y = 0; y < WORLD_HEIGHT; y++) {
    for (let x = 0; x < WORLD_WIDTH; x++) {
      const id = GLYPH_TO_ID[WORLD_ROWS[y][x]] ?? 1;
      ground[y * WORLD_WIDTH + x] = id;
      collision[y * WORLD_WIDTH + x] = BLOCKED.has(id) ? 1 : 0;
    }
  }
  return {
    width: WORLD_WIDTH,
    height: WORLD_HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    tileArt: TILE_ART_MAP,
    collision,
    exits: [],
    coastal: true,
    props: Object.entries(WORLD_TOWNS).map(([id, pos]) => ({ kind: TOWN_ICON[id], tileX: pos.x, tileY: pos.y })),
  };
}
