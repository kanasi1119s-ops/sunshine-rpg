import type { TileMapData } from "../types";
import { carveMap, type Rect } from "../carve-map";

const GRASS = 1;
const PATH = 2;
const TREE = 4;
const ROCK = 5;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#4a7a3f",
  [PATH]: "#b79a68",
  [TREE]: "#1f5c33",
  [ROCK]: "#5a5a5a",
};
const TILE_ART_MAP: Record<number, string> = { [GRASS]: "grass", [PATH]: "path", [TREE]: "treeCanopy" };

const W = 22;
const H = 18;

/** 町の北の門を出てすぐの、森の道（序章のダンジョンの1つ目。入り口の広場・曲がり道・東の寄り道・南西のかくれ場所）。 */
export function createTouriForest1Data(): TileMapData {
  const rooms: Rect[] = [
    { x: 8, y: 14, w: 8, h: 3 }, // 町から入ってきた広場
    { x: 9, y: 10, w: 3, h: 5 }, // 北へのぬけ道
    { x: 5, y: 6, w: 12, h: 4 }, // 中ほどの広場
    { x: 3, y: 3, w: 5, h: 4 }, // 西の曲がり
    { x: 5, y: 1, w: 3, h: 3 }, // 北の出口の前
    { x: 14, y: 3, w: 6, h: 4 }, // 東の寄り道
    { x: 2, y: 12, w: 4, h: 3 }, // 南西のかくれ場所
    { x: 5, y: 13, w: 4, h: 1 }, // かくれ場所への小道
  ];
  return carveMap(
    {
      width: W,
      height: H,
      wall: TREE,
      floor: GRASS,
      rooms,
      paths: [{ tile: PATH, points: [[11, 17], [11, 12], [10, 8], [8, 7], [6, 4], [6, 1]] }],
      tiles: [
        { x: 9, y: 8, tile: ROCK, blocked: true },
        { x: 14, y: 8, tile: ROCK, blocked: true },
        { x: 17, y: 5, tile: ROCK, blocked: true },
      ],
      gates: [{ x: FOREST1_SOUTH.x, y: FOREST1_SOUTH.y, tile: PATH }, { x: FOREST1_NORTH.x, y: FOREST1_NORTH.y, tile: PATH }],
    },
    {
      tileColors: TILE_COLORS,
      tileArt: TILE_ART_MAP,
      exits: [
        { tileX: FOREST1_SOUTH.x, tileY: FOREST1_SOUTH.y, targetMapId: "touri-town", targetTileX: 11, targetTileY: 1 },
        { tileX: FOREST1_NORTH.x, tileY: FOREST1_NORTH.y, targetMapId: "touri-forest-2", targetTileX: 11, targetTileY: 16 },
      ],
    },
  );
}

export const FOREST1_SOUTH = { x: 11, y: 17 };
export const FOREST1_NORTH = { x: 6, y: 0 };
/** 町から入ってきたときの立ち位置。 */
export const TOURI_FOREST1_ENTRY = { tileX: 11, tileY: 16 };
/** 宝箱・看板・旅人を置く座標。 */
export const TOURI_FOREST1_LANDMARKS = {
  chestEast: { tileX: 18, tileY: 4 },
  chestHidden: { tileX: 3, tileY: 13 },
  signpost: { tileX: 10, tileY: 12 },
  traveler: { tileX: 13, tileY: 8 },
};

/** 古い祠のある森（序章のダンジョンの2つ目）。左右の石の台（レバー）を動かすと、北の祠の門が開く。 */
export function createTouriForest2Data(): TileMapData {
  const rooms: Rect[] = [
    { x: 8, y: 13, w: 7, h: 4 }, // 入ってきた広場
    { x: 10, y: 10, w: 3, h: 4 }, // 祠の広場へのぬけ道
    { x: 6, y: 5, w: 10, h: 6 }, // 祠の広場
    { x: 1, y: 6, w: 5, h: 3 }, // 西の石の台
    { x: 16, y: 6, w: 5, h: 3 }, // 東の石の台
    { x: 9, y: 1, w: 4, h: 5 }, // 北の門へ
    { x: 15, y: 13, w: 5, h: 3 }, // 南東のかくれ場所
    { x: 14, y: 12, w: 2, h: 2 }, // かくれ場所へのぬけ道
  ];
  return carveMap(
    {
      width: W,
      height: H,
      wall: TREE,
      floor: GRASS,
      rooms,
      paths: [{ tile: PATH, points: [[11, 17], [11, 12], [10, 9], [10, 1]] }],
      tiles: [
        // 祠の広場の古い石（飾り）
        { x: 7, y: 6, tile: ROCK, blocked: true },
        { x: 14, y: 6, tile: ROCK, blocked: true },
        { x: 7, y: 9, tile: ROCK, blocked: true },
        { x: 14, y: 9, tile: ROCK, blocked: true },
      ],
      gates: [{ x: FOREST2_SOUTH.x, y: FOREST2_SOUTH.y, tile: PATH }, { x: FOREST2_NORTH.x, y: FOREST2_NORTH.y, tile: PATH }],
    },
    {
      tileColors: TILE_COLORS,
      tileArt: TILE_ART_MAP,
      exits: [
        { tileX: FOREST2_SOUTH.x, tileY: FOREST2_SOUTH.y, targetMapId: "touri-forest-1", targetTileX: 6, targetTileY: 1 },
        {
          tileX: FOREST2_NORTH.x,
          tileY: FOREST2_NORTH.y,
          targetMapId: "touri-outskirts",
          targetTileX: 9,
          targetTileY: 12,
          requireFlag: "chapter0_shrine_open",
          blockedMessage: "祠の門は固く閉ざされている。左右にある石の台（レバー）を調べてみよう。",
        },
      ],
    },
  );
}

export const FOREST2_SOUTH = { x: 11, y: 17 };
export const FOREST2_NORTH = { x: 10, y: 0 };
/** 外れの境目（歪みの発生地点）から戻ってきたときの立ち位置。 */
export const TOURI_FOREST2_NORTH_ENTRY = { tileX: 10, tileY: 1 };
export const TOURI_FOREST2_LANDMARKS = {
  leverWest: { tileX: 2, tileY: 7 },
  leverEast: { tileX: 19, tileY: 7 },
  chest: { tileX: 18, tileY: 14 },
  inscription: { tileX: 12, tileY: 3 },
};
