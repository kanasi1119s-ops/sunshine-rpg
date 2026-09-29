import type { TileMapData } from "../types";

const SAND = 1;
const DUNE = 2;
const CRATE = 3;
const WAGON = 4;
const TRACK = 5;
const GATE = 6;

const TILE_COLORS: Record<number, string> = {
  [SAND]: "#d2b676",
  [DUNE]: "#b8955a",
  [CRATE]: "#7a5a34",
  [WAGON]: "#6a4a3a",
  [TRACK]: "#c4a468",
  [GATE]: "#8a6a3a",
};

const NON_WALKABLE = new Set([DUNE, CRATE, WAGON]);

const WIDTH = 20;
const HEIGHT = 16;

const NORTH_GATE = { x: 9, y: 0 };
/** 奥に停まる隊商の荷馬車列（4x2、密輸の積荷が紛れ込んでいる）。 */
const WAGON_ORIGIN = { x: 8, y: 11 };

/**
 * 第4章の事件現場、砂音の南の隊商野営地（`docs/story/mystery.md` 第4章参照）。
 * 隊商路を巡る対立の陰で、荷馬車に紛れた密輸の積荷が見つかる。
 */
export function createSanoneCampData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(SAND);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を砂丘で囲む。北だけ、砂音の町へ戻る門を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === NORTH_GATE.x ? GATE : DUNE);
    set(x, HEIGHT - 1, DUNE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, DUNE);
    set(WIDTH - 1, y, DUNE);
  }

  // 門から荷馬車列へのびる轍（通行可能）。
  for (let y = 1; y < WAGON_ORIGIN.y; y++) {
    set(NORTH_GATE.x, y, TRACK);
  }

  // 野営地のまわりに積まれた木箱。
  for (const [x, y] of [
    [3, 3], [4, 3], [3, 4],
    [15, 3], [16, 3], [16, 4],
    [3, 8], [4, 8],
    [15, 8], [15, 9],
  ] as [number, number][]) {
    set(x, y, CRATE);
  }

  // 奥の荷馬車列。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(WAGON_ORIGIN.x + dx, WAGON_ORIGIN.y + dy, WAGON);
    }
  }

  return {
    width: WIDTH,
    height: HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: [
      {
        // 北の門を戻って砂音の町へ。
        tileX: NORTH_GATE.x,
        tileY: NORTH_GATE.y,
        targetMapId: "sanone-town",
        targetTileX: 12,
        targetTileY: 13,
      },
    ],
  };
}

/** 町の南の門から入ってきたときの立ち位置。 */
export const SANONE_CAMP_ENTRY = { tileX: NORTH_GATE.x, tileY: NORTH_GATE.y + 2 };

/** 野営地のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const SANONE_CAMP_LANDMARKS = {
  wagon: { tileX: WAGON_ORIGIN.x + 1, tileY: WAGON_ORIGIN.y - 1 },
  dorun: { tileX: 9, tileY: 6 },
};
