import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const CRATE = 3;
const DOOR = 4;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#6a5a48",
  [WALL]: "#3a3028",
  [CRATE]: "#8a6a3f",
  [DOOR]: "#b79a68",
};

const NON_WALKABLE = new Set([WALL, CRATE]);

const WIDTH = 16;
const HEIGHT = 14;

const SOUTH_GATE = { x: 5, y: HEIGHT - 1 };
/** 密輸された灯り石の木箱の山（伏線・事件の証拠、奥の壁際）。 */
const CRATE_PILE_ORIGIN = { x: 9, y: 2 };

/**
 * 第2章の事件現場、桟橋の先にある密輸倉庫（`docs/story/structure.md`「第2章（硝子湖）」、
 * `docs/story/mystery.md` 参照）。密輸品に不自然な量の灯り石が紛れ込んでいる現場。
 */
export function createGarasukoWarehouseData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を壁で囲む。南だけ、桟橋へ戻る戸を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL);
    set(x, HEIGHT - 1, x === SOUTH_GATE.x ? DOOR : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 積み上げられた木箱（通路以外に点在）。
  const cratePositions: [number, number][] = [
    [2, 3], [2, 4], [3, 3],
    [12, 3], [13, 3], [13, 4],
    [2, 9], [3, 9],
    [12, 9], [12, 10],
  ];
  for (const [x, y] of cratePositions) {
    set(x, y, CRATE);
  }

  // 奥の灯り石の木箱の山（3x2、事件の証拠）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(CRATE_PILE_ORIGIN.x + dx, CRATE_PILE_ORIGIN.y + dy, CRATE);
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
        // 桟橋を戻って硝子湖の町へ。
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        targetMapId: "garasuko-town",
        targetTileX: 11,
        targetTileY: 14,
      },
    ],
  };
}

/** 町の桟橋から渡ってきたときの立ち位置。 */
export const GARASUKO_WAREHOUSE_ENTRY = { tileX: SOUTH_GATE.x, tileY: HEIGHT - 3 };

/** 倉庫内のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const GARASUKO_WAREHOUSE_LANDMARKS = {
  cratePile: { tileX: CRATE_PILE_ORIGIN.x + 1, tileY: CRATE_PILE_ORIGIN.y + 2 },
  dorun: { tileX: 8, tileY: 6 },
};
