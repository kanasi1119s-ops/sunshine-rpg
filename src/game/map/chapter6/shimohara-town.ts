import type { TileMapData } from "../types";

const SNOW = 1;
const ROAD = 2;
const ICE = 3;
const PINE = 4;
const HOUSE = 5;
const FACILITY_GATE = 6;
const FENCE = 7;

const TILE_COLORS: Record<number, string> = {
  [SNOW]: "#e8eef2",
  [ROAD]: "#b9b5a8",
  [ICE]: "#a9c8dc",
  [PINE]: "#3f5f52",
  [HOUSE]: "#8a6a50",
  [FACILITY_GATE]: "#5a5a66",
  [FENCE]: "#7a746a",
};

const NON_WALKABLE = new Set([ICE, PINE, HOUSE, FENCE]);

const WIDTH = 24;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 10 };
const EAST_GATE = { x: WIDTH - 1, y: 10 };
/** 町の北、雪原の戦跡に口を開けた施設への入口。 */
const FACILITY_GATE_POS = { x: 12, y: 0 };
/** 番所（4x2）と、宿屋（3x2）。 */
const WATCH_ORIGIN = { x: 5, y: 4 };
const INN_ORIGIN = { x: 17, y: 4 };

/**
 * 第6章の舞台、北の雪原の町・霜原（`docs/story/structure.md`「第6章（霜原）」参照）。
 * 大乱期の戦跡に寄り添う小さな町。北の雪の下に、戦跡に隠された施設への入口がある。
 */
export function createShimoharaTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(SNOW);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周: 針葉樹で囲み、西（霧断崖からの街道）と北（施設）だけ開ける。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === FACILITY_GATE_POS.x ? FACILITY_GATE : PINE);
    set(x, HEIGHT - 1, PINE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? ROAD : PINE);
    set(WIDTH - 1, y, y === EAST_GATE.y ? ROAD : PINE);
  }

  // 西の街道から広場へ、広場から施設へ。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, ROAD);
  }
  for (let y = 1; y < WEST_GATE.y; y++) {
    set(FACILITY_GATE_POS.x, y, ROAD);
  }

  // 番所と宿屋（外観のみ）。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(WATCH_ORIGIN.x + dx, WATCH_ORIGIN.y + dy, HOUSE);
    }
  }
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(INN_ORIGIN.x + dx, INN_ORIGIN.y + dy, HOUSE);
    }
  }
  // 凍った池。
  for (let x = 16; x < 21; x++) {
    for (let y = 12; y < 14; y++) {
      set(x, y, ICE);
    }
  }
  // 施設の手前の古い柵（戦跡の名残）。
  for (const x of [10, 11, 13, 14]) {
    set(x, 2, FENCE);
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
        // 霧断崖へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "kiri-town",
        targetTileX: 21,
        targetTileY: 16,
      },
      {
        // 東の街道を渡って、第7章の浮嶼へ。
        tileX: EAST_GATE.x,
        tileY: EAST_GATE.y,
        targetMapId: "fushima-town",
        targetTileX: 2,
        targetTileY: 10,
      },
      {
        // 北の雪原の入口から、戦跡の施設へ。
        tileX: FACILITY_GATE_POS.x,
        tileY: FACILITY_GATE_POS.y,
        targetMapId: "shimohara-facility",
        targetTileX: 9,
        targetTileY: 12,
      },
    ],
  };
}

/** 霧断崖から街道を渡ってきたときの立ち位置。 */
export const SHIMOHARA_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 浮嶼から街道を戻ってきたときの立ち位置。 */
export const SHIMOHARA_TOWN_EAST_RETURN = { tileX: EAST_GATE.x - 2, tileY: EAST_GATE.y };

/** 施設から戻ってきたときの立ち位置。 */
export const SHIMOHARA_TOWN_FACILITY_RETURN = { tileX: FACILITY_GATE_POS.x, tileY: FACILITY_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const SHIMOHARA_TOWN_LANDMARKS = {
  watchman: { tileX: WATCH_ORIGIN.x + 1, tileY: WATCH_ORIGIN.y + 2 },
  innkeeper: { tileX: INN_ORIGIN.x + 1, tileY: INN_ORIGIN.y + 2 },
  hunter: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
