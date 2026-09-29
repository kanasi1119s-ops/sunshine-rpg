import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const MACHINE = 3;
const PIPE = 4;
const DOOR = 5;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#7d8590",
  [WALL]: "#3e424c",
  [MACHINE]: "#5c6b78",
  [PIPE]: "#8a7a5a",
  [DOOR]: "#5a5a66",
};

const NON_WALKABLE = new Set([WALL, MACHINE, PIPE]);

const WIDTH = 20;
const HEIGHT = 14;

const SOUTH_DOOR = { x: 9, y: HEIGHT - 1 };
/** 奥の大きな装置（3x2）。「静まりの年」に使われた発生装置の試作機。 */
const MACHINE_ORIGIN = { x: 8, y: 3 };

/**
 * 第6章の事件現場、戦跡の雪の下に隠された施設。
 * 「静まりの年」に使われた発生装置の試作施設で、いまも一部が動いている。
 */
export function createShimoharaFacilityData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL);
    set(x, HEIGHT - 1, x === SOUTH_DOOR.x ? DOOR : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 左右の壁ぎわの配管。
  for (let y = 2; y < 10; y++) {
    set(2, y, PIPE);
    set(WIDTH - 3, y, PIPE);
  }
  // 奥の大きな装置。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(MACHINE_ORIGIN.x + dx, MACHINE_ORIGIN.y + dy, MACHINE);
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
        // 南の扉から、霜原の町へ。
        tileX: SOUTH_DOOR.x,
        tileY: SOUTH_DOOR.y,
        targetMapId: "shimohara-town",
        targetTileX: 12,
        targetTileY: 2,
      },
    ],
  };
}

/** 町から入ってきたときの立ち位置。 */
export const SHIMOHARA_FACILITY_ENTRY = { tileX: SOUTH_DOOR.x, tileY: SOUTH_DOOR.y - 2 };

/** 施設内のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const SHIMOHARA_FACILITY_LANDMARKS = {
  machine: { tileX: MACHINE_ORIGIN.x + 1, tileY: MACHINE_ORIGIN.y + 2 },
  log: { tileX: 4, tileY: 5 },
  panel: { tileX: 15, tileY: 5 },
  guard: { tileX: 7, tileY: 7 },
};
