import type { TileMapData } from "../types";

const SAND = 1;
const ROAD = 2;
const DUNE = 3;
const PALM = 4;
const TENT = 5;
const OASIS = 6;
const CAMP_GATE = 7;

const TILE_COLORS: Record<number, string> = {
  [SAND]: "#d9bf82",
  [ROAD]: "#b89a5e",
  [DUNE]: "#c2a05c",
  [PALM]: "#3f6b3a",
  [TENT]: "#a8483a",
  [OASIS]: "#3f8ab0",
  [CAMP_GATE]: "#8a6a3a",
};

const NON_WALKABLE = new Set([DUNE, PALM, TENT, OASIS]);

const WIDTH = 24;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 10 };
/** 東の砂丘の切れ目。断崖の宗教都市・霧断崖へ続く街道。 */
const EAST_GATE = { x: WIDTH - 1, y: 10 };
/** 町の南に開いた、隊商の野営地へ続く道。 */
const CAMP_GATE_POS = { x: 12, y: HEIGHT - 1 };
/** 隊商組合の大天幕（4x2）と、市場の天幕（3x2）。 */
const GUILD_TENT_ORIGIN = { x: 5, y: 4 };
const MARKET_TENT_ORIGIN = { x: 17, y: 4 };
/** 町の中央のオアシス（池）。 */
const OASIS_AREA = { x: 10, y: 5, w: 4, h: 2 };

/**
 * 第4章の舞台、砂漠の隊商都市・砂音（`docs/story/structure.md`「第4章（砂音）」参照）。
 * 町の中央にオアシスがあり、隊商組合と市場の天幕が並ぶ。南の門の先が、隊商の野営地。
 */
export function createSanoneTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(SAND);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周: 砂丘で囲み、西（鉄鏈鉱山からの街道）と南（野営地）だけ開ける。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, DUNE);
    set(x, HEIGHT - 1, x === CAMP_GATE_POS.x ? CAMP_GATE : DUNE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? ROAD : DUNE);
    set(WIDTH - 1, y, y === EAST_GATE.y ? ROAD : DUNE);
  }

  // 西の門から東へのびる大通りと、南の門へ向かう道。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, ROAD);
  }
  for (let y = WEST_GATE.y; y < HEIGHT - 1; y++) {
    set(CAMP_GATE_POS.x, y, ROAD);
  }

  // 中央のオアシスと、まわりのヤシの木。
  for (let dx = 0; dx < OASIS_AREA.w; dx++) {
    for (let dy = 0; dy < OASIS_AREA.h; dy++) {
      set(OASIS_AREA.x + dx, OASIS_AREA.y + dy, OASIS);
    }
  }
  for (const [x, y] of [[9, 4], [14, 4], [9, 7], [14, 7]] as [number, number][]) {
    set(x, y, PALM);
  }

  // 隊商組合の大天幕と、市場の天幕（外観のみ）。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(GUILD_TENT_ORIGIN.x + dx, GUILD_TENT_ORIGIN.y + dy, TENT);
    }
  }
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(MARKET_TENT_ORIGIN.x + dx, MARKET_TENT_ORIGIN.y + dy, TENT);
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
        // 鉄鏈鉱山へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "tetsukusari-town",
        targetTileX: 19,
        targetTileY: 10,
      },
      {
        // 東の街道を進んで霧断崖へ。
        tileX: EAST_GATE.x,
        tileY: EAST_GATE.y,
        targetMapId: "kiri-town",
        targetTileX: 2,
        targetTileY: 16,
      },
      {
        // 南の門から、隊商の野営地へ。
        tileX: CAMP_GATE_POS.x,
        tileY: CAMP_GATE_POS.y,
        targetMapId: "sanone-camp",
        targetTileX: 9,
        targetTileY: 2,
      },
    ],
  };
}

/** 鉄鏈鉱山からの街道を渡ってきたときの立ち位置。 */
export const SANONE_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 霧断崖から街道を戻ってきたときの立ち位置。 */
export const SANONE_TOWN_EAST_RETURN = { tileX: EAST_GATE.x - 2, tileY: EAST_GATE.y };

/** 野営地から戻ってきたときの立ち位置。 */
export const SANONE_TOWN_CAMP_RETURN = { tileX: CAMP_GATE_POS.x, tileY: CAMP_GATE_POS.y - 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const SANONE_TOWN_LANDMARKS = {
  guildMaster: { tileX: GUILD_TENT_ORIGIN.x + 1, tileY: GUILD_TENT_ORIGIN.y + 2 },
  merchant: { tileX: MARKET_TENT_ORIGIN.x + 1, tileY: MARKET_TENT_ORIGIN.y + 2 },
  informant: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
