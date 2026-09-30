import type { TileMapData } from "../types";

const PAVING = 1;
const WALL = 2;
const HOUSE = 3;
const HALL_DOOR = 4;
const FOUNTAIN = 5;
const GARDEN = 6;
const DOCK = 7;

const TILE_COLORS: Record<number, string> = {
  [PAVING]: "#b4b0a4",
  [WALL]: "#6a6a76",
  [HOUSE]: "#8a7a6a",
  [HALL_DOOR]: "#4a5a86",
  [FOUNTAIN]: "#7ab0cc",
  [GARDEN]: "#6a9a5a",
  [DOCK]: "#9a8a6a",
};

const NON_WALKABLE = new Set([WALL, HOUSE, FOUNTAIN, GARDEN]);

const WIDTH = 26;
const HEIGHT = 18;

/** 南の空の船着き場（浮嶼の空の乗り物が着く）。 */
const DOCK_POS = { x: 13, y: HEIGHT - 1 };
/** 北の合議会堂の入口。 */
const HALL_GATE_POS = { x: 13, y: 0 };
/** 宿屋（3x2）。 */
const INN_ORIGIN = { x: 4, y: 6 };
/** 中央の噴水（2x2）。 */
const FOUNTAIN_ORIGIN = { x: 12, y: 8 };

/**
 * 第8章の舞台、大陸中央の都・灯芯都（`docs/story/structure.md`「第8章（灯芯都）」参照）。
 * 石畳の広場の北に合議会堂の入口があり、南に空の乗り物の船着き場がある。
 */
export function createToushinTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(PAVING);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === HALL_GATE_POS.x ? HALL_DOOR : WALL);
    set(x, HEIGHT - 1, x === DOCK_POS.x ? DOCK : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 宿屋（外観のみ）と、向かい側の商家。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(INN_ORIGIN.x + dx, INN_ORIGIN.y + dy, HOUSE);
      set(WIDTH - 8 + dx, INN_ORIGIN.y + dy, HOUSE);
    }
  }
  // 中央の噴水。
  for (let dx = 0; dx < 2; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(FOUNTAIN_ORIGIN.x + dx, FOUNTAIN_ORIGIN.y + dy, FOUNTAIN);
    }
  }
  // 広場の植え込み。
  for (const [x, y] of [[8, 12], [9, 12], [16, 12], [17, 12], [8, 3], [17, 3]]) {
    set(x, y, GARDEN);
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
        // 南の船着き場から、浮嶼の町へ。
        tileX: DOCK_POS.x,
        tileY: DOCK_POS.y,
        targetMapId: "fushima-town",
        targetTileX: 9,
        targetTileY: 9,
      },
      {
        // 北の入口から、合議会堂へ。
        tileX: HALL_GATE_POS.x,
        tileY: HALL_GATE_POS.y,
        targetMapId: "toushin-hall",
        targetTileX: 10,
        targetTileY: 13,
      },
    ],
  };
}

/** 空の乗り物で着いたときの立ち位置。 */
export const TOUSHIN_TOWN_ENTRY = { tileX: DOCK_POS.x, tileY: DOCK_POS.y - 2 };

/** 合議会堂から戻ってきたときの立ち位置。 */
export const TOUSHIN_TOWN_HALL_RETURN = { tileX: HALL_GATE_POS.x, tileY: HALL_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const TOUSHIN_TOWN_LANDMARKS = {
  clerk: { tileX: HALL_GATE_POS.x - 2, tileY: 3 },
  guard: { tileX: HALL_GATE_POS.x + 2, tileY: 3 },
  innkeeper: { tileX: INN_ORIGIN.x + 1, tileY: INN_ORIGIN.y + 2 },
};
