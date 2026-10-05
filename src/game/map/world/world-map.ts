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

/** 村の印を、立っている地面に合わせて替える（2026-10-05。雪原の霧間の集落・草原の砂守のいずみと荒野の市）。 */
const VILLAGE_ICON: Record<string, MapProp["kind"]> = {
  "village-kirima": "icon-village-mist",
  "village-samori": "icon-tents-grass",
  "village-arano": "icon-tents-grass",
};

/**
 * 世界地図（大陸アルテシア）。上から見た大陸を歩く。町・遺跡のアイコンの上に乗ると、その場所へ入る（出入り口は `world.ts` で、
 * 各町の南の門とつなぐ）。地形は `tools/world-map/gen_world.py` で作った `world-map.generated.ts`。
 * 山・海・湖は通れない。道は、町と町をつなぐ（山脈は道だけが越える）。
 */
const GLYPH_TO_ID: Record<string, number> = { O: 1, P: 2, F: 3, M: 4, D: 5, S: 6, R: 7, H: 8, L: 9, C: 10, W: 11, T: 12, V: 13, Q: 14, N: 15, X: 16, Z: 17, A: 18 };

const TILE_COLORS: Record<number, string> = {
  1: "#1e5a96", 2: "#4a9a3a", 3: "#2f7a2a", 4: "#857c74", 5: "#d9bf82", 6: "#e8eef2", 7: "#b3853f", 8: "#5a9a40", 9: "#2f6fb0", 10: "#cfe3f2", 11: "#5a4a6a", 12: "#3a6a50", 13: "#143a78", 14: "#143a78", 15: "#6a6068", 16: "#3a2c3a", 17: "#d8501c", 18: "#4a4244", 19: "#9ac8ec",
};

const TILE_ART_MAP: Record<number, string> = {
  1: "water", 2: "grass", 3: "worldforest", 4: "mountain", 5: "tint:sand", 6: "tint:snow", 7: "path", 8: "hills", 9: "water", 10: "tint:cloud", 11: "tint:flagstone", 12: "snowforest", 13: "water", 14: "water", 15: "peaks", 16: "chasm", 17: "lava", 18: "tint:sand", 19: "water",
};

/** 全体フィールドの地形テクスチャ（`tools/pixel-art/ai-gen/world_tiles.py` で作り、エディタで描いて確かめたもの。2026-10-04）。 */
const TILE_TEXTURE: Record<number, string> = {
  1: "terrain:w-sea", 2: "terrain:w-grass", 3: "terrain:w-forest", 4: "terrain:w-mountain", 5: "terrain:w-sand", 6: "terrain:w-snow", 7: "terrain:w-road", 8: "terrain:w-hills", 9: "terrain:w-lake", 10: "terrain:w-cloud", 11: "terrain:w-waste", 12: "terrain:w-snowforest", 13: "terrain:w-sea", 14: "terrain:w-sea", 15: "terrain:w-pyramids", 16: "terrain:w-chasm", 17: "terrain:w-lava", 18: "terrain:w-ash", 19: "terrain:w-lake",
};

/** 通れない地形: 海・山・湖・渦・谷・溶岩・大滝。 */
const BLOCKED = new Set([1, 4, 9, 13, 14, 15, 16, 17, 19]);

/** 大滝（芯環塔のまわりの陥没のふち。海が穴へ流れ落ちる）。 */
export const FALLS = 19;
const CHASM = 16;
const WASTE = 11;
/** 陥没（深い穴）の半径と、大滝のふちの外がわの半径（マス）。 */
export const BASIN_PIT_R = 6.6;
export const BASIN_RIM_R = 8.4;
/** 塔のまわりで、大滝のふちの外を海にする広さ（マス。渦の輪・切れ目には手をつけない）。 */
const BASIN_SEA_R = 16;

/** 塔のまわりで、陥没の上を塔の足もとへ渡る岩の細い道（南の切れ目から、まっすぐ北へ）のマスか。 */
export function isBasinCauseway(_x: number, _y: number): boolean {
  return false;   // 塔に近寄れなくしたので、道はない（2026-10-05）
}

/**
 * 芯環塔のまわり（2026-10-05、人間の指示「中央の塔は、自然にできたような感じで、もっと高く。上の方は雲で見えなく。まわりは常時嵐で近寄れない。
 * まわりは陥没していて、ナイアガラの滝のような大きな滝になっていて近づけない」）。
 * 渦の輪の内がわのうち、塔のまわりを大きな穴（谷）にし、そのふちは海が流れ落ちる大滝にする。
 * 塔へは、南の切れ目（航路が開くと海になる）から、岩の細い道が一本だけ通る（物語で塔へ入るための道。航路が開くまでは渦の輪の嵐で近づけない）。
 */
function sinkTowerBasin(ground: number[], collision: number[]): void {
  const r = BASIN_SEA_R;
  for (let y = WORLD_TOWER.y - r; y <= WORLD_TOWER.y + r; y++) {
    for (let x = WORLD_TOWER.x - r; x <= WORLD_TOWER.x + r; x++) {
      const i = y * WORLD_WIDTH + x;
      const id = ground[i];
      if (id === 13 || id === 14) continue;                       // 渦の輪・切れ目はそのまま
      const d = Math.hypot(x - WORLD_TOWER.x, y - WORLD_TOWER.y);
      if (d > BASIN_SEA_R) continue;
      let next = id;
      if (isBasinCauseway(x, y)) next = WASTE;
      else if (d <= BASIN_PIT_R) next = CHASM;
      else if (d <= BASIN_RIM_R) next = FALLS;
      else next = 1;          // 大滝のふちの外は、渦の輪まで海（まわりの岩はなくす。2026-10-05、人間の指示「塔は周りの岩なくして」）
      ground[i] = next;
      collision[i] = BLOCKED.has(next) ? 1 : 0;
    }
  }
}

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
  sinkTowerBasin(ground, collision);
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
    wrap: true,
    props: [
      ...Object.entries(WORLD_TOWNS).map(([id, pos]) => ({ kind: TOWN_ICON[id], tileX: pos.x, tileY: pos.y })),
      ...WORLD_VILLAGES.map((v) => ({ kind: VILLAGE_ICON[v.id] ?? (`icon-${v.icon}` as MapProp["kind"]), tileX: v.x, tileY: v.y })),
      ...WORLD_ISLETS.map((islet, i) => ({ kind: (["icon-islet-ruin", "icon-islet-cave", "icon-islet-shrine", "icon-islet-fort", "icon-dive", "icon-volcano"] as const)[i], tileX: islet.x, tileY: islet.y })),
      ...WORLD_LANDMARKS.map((m) => ({ kind: `icon-${m.kind}` as MapProp["kind"], tileX: m.x, tileY: m.y })),
      // 芯環塔の絵は、大滝・嵐といっしょの1枚の動く絵（vortex-renderer の renderBasin）で描くので、ここには置かない
    ],
  };
}
