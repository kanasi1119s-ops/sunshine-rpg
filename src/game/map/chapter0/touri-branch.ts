import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const DOOR = 3;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8a7458",
  [WALL]: "#332e2a",
  [DOOR]: "#6b4a2b",
};

const WIDTH = 9;
const HEIGHT = 7;
const DOOR_X = 4;

/**
 * 灯りの相談所 灯里支部の内部（序章の依頼受注イベントの舞台）。
 * カセン支部長・レトがここにいる（NPC配置はイベントデータ側で行う）。
 */
export function createTouriBranchData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number, walkable: boolean): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = walkable ? 0 : 1;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL, false);
    set(x, HEIGHT - 1, WALL, false);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL, false);
    set(WIDTH - 1, y, WALL, false);
  }
  set(DOOR_X, HEIGHT - 1, DOOR, true);

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
        tileX: DOOR_X,
        tileY: HEIGHT - 1,
        targetMapId: "touri-town",
        targetTileX: 5,
        targetTileY: 6,
      },
    ],
  };
}

/** 入口から入ったときの立ち位置（ドアのすぐ内側）。 */
export const TOURI_BRANCH_ENTRY = { tileX: DOOR_X, tileY: HEIGHT - 2 };

/** カセン支部長・レトを置く座標（イベントデータ側で使う）。 */
export const TOURI_BRANCH_LANDMARKS = {
  kasen: { tileX: DOOR_X, tileY: 1 },
  reto: { tileX: DOOR_X - 2, tileY: 1 },
};
