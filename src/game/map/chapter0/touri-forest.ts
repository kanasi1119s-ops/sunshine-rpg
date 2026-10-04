import type { TileMapData } from "../types";
import { carveMap } from "../carve-map";
import { mazeLayout, type Landmarks } from "../serpentine";

const GRASS = 1;
const PATH = 2;
const TREE = 4;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#4a7a3f",
  [PATH]: "#b79a68",
  [TREE]: "#1f5c33",
  5: "#5a5a5a",
};
const TILE_ART_MAP: Record<number, string> = { [GRASS]: "grass", [PATH]: "path", [TREE]: "treeCanopy" };

/** 序章のダンジョン（森）。長く折れ曲がる道を、フィールドを旅するように歩く（5本の通路）。 */
const LAYOUT_1 = mazeLayout({ wall: TREE, floor: GRASS, seed: 11 });
const LAYOUT_2 = mazeLayout({ wall: TREE, floor: GRASS, seed: 12 });

const at = (l: Landmarks, i: number): { tileX: number; tileY: number } => l.alcoves[Math.min(i, l.alcoves.length - 1)];

/** 町の北の門を出てすぐの、森の道。 */
export function createTouriForest1Data(): TileMapData {
  const l = LAYOUT_1.landmarks;
  return carveMap(LAYOUT_1.spec, {
    tileColors: TILE_COLORS,
    tileArt: TILE_ART_MAP,
    exits: [
      { tileX: l.south.x, tileY: l.south.y, targetMapId: "touri-town", targetTileX: 11, targetTileY: 1 },
      { tileX: l.north.x, tileY: l.north.y, targetMapId: "touri-forest-2", targetTileX: LAYOUT_2.landmarks.southArrival.tileX, targetTileY: LAYOUT_2.landmarks.southArrival.tileY },
    ],
  });
}

/** 町から入ってきたときの立ち位置（町の北の門の出口が目指す場所）。 */
export const TOURI_FOREST1_ENTRY = LAYOUT_1.landmarks.southArrival;
/** 宝箱・看板・旅人を置く座標。 */
export const TOURI_FOREST1_LANDMARKS = {
  chestEast: at(LAYOUT_1.landmarks, 2),
  chestHidden: at(LAYOUT_1.landmarks, 6),
  signpost: LAYOUT_1.landmarks.nearExit,
  traveler: LAYOUT_1.landmarks.nearEntry,
};

/** 古い祠のある森（序章のダンジョンの2つ目）。左右の石の台（レバー）を動かすと、北の祠の門が開く。 */
export function createTouriForest2Data(): TileMapData {
  const l = LAYOUT_2.landmarks;
  return carveMap(LAYOUT_2.spec, {
    tileColors: TILE_COLORS,
    tileArt: TILE_ART_MAP,
    exits: [
      { tileX: l.south.x, tileY: l.south.y, targetMapId: "touri-forest-1", targetTileX: LAYOUT_1.landmarks.northArrival.tileX, targetTileY: LAYOUT_1.landmarks.northArrival.tileY },
      {
        tileX: l.north.x,
        tileY: l.north.y,
        targetMapId: "touri-outskirts",
        targetTileX: 9,
        targetTileY: 12,
        requireFlag: "chapter0_shrine_open",
        blockedMessage: "祠の門は固く閉ざされている。森のあちこちにある、石の台（レバー）を2つとも探して調べてみよう。",
      },
    ],
  });
}

/** 歪みの発生地点から戻ってきたときの立ち位置。 */
export const TOURI_FOREST2_NORTH_ENTRY = LAYOUT_2.landmarks.northArrival;
export const TOURI_FOREST2_LANDMARKS = {
  leverWest: at(LAYOUT_2.landmarks, 1),
  leverEast: at(LAYOUT_2.landmarks, 6),
  chest: at(LAYOUT_2.landmarks, 4),
  inscription: LAYOUT_2.landmarks.nearExit,
};
