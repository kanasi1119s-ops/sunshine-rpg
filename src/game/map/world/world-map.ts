import type { TileMapData } from "../types";
import { WORLD_HEIGHT, WORLD_ISLETS, WORLD_LANDMARKS, WORLD_VILLAGES, WORLD_ROWS, WORLD_TOWER, WORLD_TOWNS, WORLD_WIDTH } from "./world-map.generated";
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
const GLYPH_TO_ID: Record<string, number> = { O: 1, P: 2, F: 3, M: 4, D: 5, S: 6, R: 7, H: 8, L: 9, C: 10, W: 11, T: 12, V: 13, Q: 14, N: 15, X: 16, Z: 17, A: 18 };

const TILE_COLORS: Record<number, string> = {
  1: "#1e5a96", 2: "#4a9a3a", 3: "#2f7a2a", 4: "#857c74", 5: "#d9bf82", 6: "#e8eef2", 7: "#b3853f", 8: "#5a9a40", 9: "#2f6fb0", 10: "#cfe3f2", 11: "#5a4a6a", 12: "#3a6a50", 13: "#143a78", 14: "#143a78", 15: "#6a6068", 16: "#3a2c3a", 17: "#d8501c", 18: "#4a4244",
};

const TILE_ART_MAP: Record<number, string> = {
  1: "water", 2: "grass", 3: "worldforest", 4: "mountain", 5: "tint:sand", 6: "tint:snow", 7: "path", 8: "hills", 9: "water", 10: "tint:cloud", 11: "tint:flagstone", 12: "snowforest", 13: "water", 14: "water", 15: "peaks", 16: "chasm", 17: "lava", 18: "tint:sand",
};

/** 全体フィールドの地形テクスチャ（`tools/pixel-art/ai-gen/world_tiles.py` で作り、エディタで描いて確かめたもの。2026-10-04）。 */
const TILE_TEXTURE: Record<number, string> = {
  1: "terrain:w-sea", 2: "terrain:w-grass", 3: "terrain:w-forest", 4: "terrain:w-mountain", 5: "terrain:w-sand", 6: "terrain:w-snow", 7: "terrain:w-road", 8: "terrain:w-hills", 9: "terrain:w-lake", 10: "terrain:w-cloud", 11: "terrain:w-waste", 12: "terrain:w-snowforest", 13: "terrain:w-sea", 14: "terrain:w-sea", 15: "terrain:w-peaks", 16: "terrain:w-chasm", 17: "terrain:w-lava", 18: "terrain:w-ash",
};

/** 通れない地形: 海・山・湖。 */
const BLOCKED = new Set([1, 4, 9, 13, 14, 15, 16, 17]);

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
    tileTexture: TILE_TEXTURE,
    collision,
    exits: [],
    coastal: true,
    props: [
      ...Object.entries(WORLD_TOWNS).map(([id, pos]) => ({ kind: TOWN_ICON[id], tileX: pos.x, tileY: pos.y })),
      ...WORLD_VILLAGES.map((v) => ({ kind: `icon-${v.icon}` as MapProp["kind"], tileX: v.x, tileY: v.y })),
      ...WORLD_ISLETS.map((islet, i) => ({ kind: (["icon-islet-ruin", "icon-islet-cave", "icon-islet-shrine", "icon-islet-fort", "icon-dive", "icon-volcano"] as const)[i], tileX: islet.x, tileY: islet.y })),
      ...WORLD_LANDMARKS.map((m) => ({ kind: `icon-${m.kind}` as MapProp["kind"], tileX: m.x, tileY: m.y })),
      { kind: "icon-spire" as const, tileX: WORLD_TOWER.x, tileY: WORLD_TOWER.y },
    ],
  };
}
