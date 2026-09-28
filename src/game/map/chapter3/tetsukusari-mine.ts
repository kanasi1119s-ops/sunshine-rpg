import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const ORE = 3;
const RAIL = 4;
const DOOR = 5;
const MACHINE = 6;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#5b544a",
  [WALL]: "#2b2722",
  [ORE]: "#6fa8c8",
  [RAIL]: "#7a6a52",
  [DOOR]: "#b79a68",
  [MACHINE]: "#5a4a70",
};

const NON_WALKABLE = new Set([WALL, ORE, MACHINE]);

const WIDTH = 18;
const HEIGHT = 16;

const SOUTH_GATE = { x: 8, y: HEIGHT - 1 };
/** 奥の実験装置（3x2、「歪みを人為的に作る実験」の証拠）。 */
const MACHINE_ORIGIN = { x: 7, y: 2 };

/**
 * 第3章の事件現場、鉄鏈鉱山の内部（`docs/story/mystery.md` 第3章参照）。
 * 労働争議の目くらましの奥で、歪みを人為的に作る実験装置が隠されている。
 */
export function createTetsukusariMineData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を壁で囲む。南だけ、坑道の入口へ戻る戸を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL);
    set(x, HEIGHT - 1, x === SOUTH_GATE.x ? DOOR : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 入口から奥へ続くトロッコの線路（通行可能）。
  for (let y = 4; y < HEIGHT - 1; y++) {
    set(SOUTH_GATE.x, y, RAIL);
  }

  // 光る灯り石の鉱脈（通路以外の壁際に点在）。
  const orePositions: [number, number][] = [
    [2, 3], [2, 4], [3, 3],
    [14, 3], [15, 3], [15, 4],
    [2, 10], [3, 10],
    [14, 10], [14, 11],
  ];
  for (const [x, y] of orePositions) {
    set(x, y, ORE);
  }

  // 奥の実験装置（3x2、事件の証拠）。
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
        // 坑道の入口を戻って鉄鏈鉱山の町へ。
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        targetMapId: "tetsukusari-town",
        targetTileX: 11,
        targetTileY: 2,
      },
    ],
  };
}

/** 町の坑道の入口から入ってきたときの立ち位置。 */
export const TETSUKUSARI_MINE_ENTRY = { tileX: SOUTH_GATE.x, tileY: HEIGHT - 3 };

/** 鉱山内のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const TETSUKUSARI_MINE_LANDMARKS = {
  machine: { tileX: MACHINE_ORIGIN.x + 1, tileY: MACHINE_ORIGIN.y + 2 },
  dorun: { tileX: 8, tileY: 6 },
};
