import type { TileMapData } from "../types";

const GROUND = 1;
const PATH = 2;
const ROCK = 3;
const TREE = 4;
const HOUSE_WALL = 5;
const MINE_GATE = 6;

const TILE_COLORS: Record<number, string> = {
  [GROUND]: "#7d7468",
  [PATH]: "#b8a77c",
  [ROCK]: "#4a4640",
  [TREE]: "#2a4a30",
  [HOUSE_WALL]: "#8a5a3a",
  [MINE_GATE]: "#2c2622",
};

/** ドット絵パターン（`tile-art.ts`）を適用する地形カテゴリ。岩場（ROCK）などは対象外。 */
const TILE_ART_MAP: Record<number, string> = {
  [PATH]: "path",
  [TREE]: "treeCanopy",
};

const NON_WALKABLE = new Set([ROCK, TREE, HOUSE_WALL]);

const WIDTH = 22;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 10 };
/** 町の北の崖に開いた坑道の入口（鉱山の内部へ続く）。 */
const MINE_GATE_POS = { x: 11, y: 0 };
/** 組合の詰め所（3x2）と、鉱山会社の事務所（3x2）。 */
const UNION_HALL_ORIGIN = { x: 4, y: 4 };
const OFFICE_ORIGIN = { x: 15, y: 4 };

/**
 * 第3章の舞台、灯り石の鉱山町・鉄鏈鉱山（`docs/story/structure.md`「第3章（鉄鏈鉱山）」参照）。
 * 北の崖に坑道の入口があり、町には労働組合の詰め所と、鉱山会社の事務所が向かい合って建つ。
 */
export function createTetsukusariTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GROUND);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周: 北と東は岩の崖、南と西は木。西は硝子湖からの街道、北は坑道の入口を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === MINE_GATE_POS.x ? MINE_GATE : ROCK);
    set(x, HEIGHT - 1, TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? PATH : TREE);
    set(WIDTH - 1, y, ROCK);
  }

  // 西の街道から広場まで、広場から坑道の入口までの道。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, PATH);
  }
  for (let y = 1; y <= WEST_GATE.y; y++) {
    set(MINE_GATE_POS.x, y, PATH);
  }

  // 坑道の入口まわりの岩場（入口の左右を崖で囲う）。
  for (const [x, y] of [[9, 1], [10, 1], [12, 1], [13, 1], [9, 2], [13, 2]] as [number, number][]) {
    set(x, y, ROCK);
  }

  // 組合の詰め所と鉱山会社の事務所（外観のみ）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(UNION_HALL_ORIGIN.x + dx, UNION_HALL_ORIGIN.y + dy, HOUSE_WALL);
      set(OFFICE_ORIGIN.x + dx, OFFICE_ORIGIN.y + dy, HOUSE_WALL);
    }
  }

  return {
    width: WIDTH,
    height: HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    tileArt: TILE_ART_MAP,
    collision,
    exits: [
      {
        // 硝子湖へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "garasuko-town",
        targetTileX: 19,
        targetTileY: 8,
      },
      {
        // 坑道の入口から、鉱山の内部へ。
        tileX: MINE_GATE_POS.x,
        tileY: MINE_GATE_POS.y,
        targetMapId: "tetsukusari-mine",
        targetTileX: 8,
        targetTileY: 13,
      },
    ],
  };
}

/** 硝子湖からの街道を渡ってきたときの立ち位置。 */
export const TETSUKUSARI_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 鉱山の内部から戻ってきたときの立ち位置。 */
export const TETSUKUSARI_TOWN_MINE_RETURN = { tileX: MINE_GATE_POS.x, tileY: MINE_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const TETSUKUSARI_TOWN_LANDMARKS = {
  orca: { tileX: UNION_HALL_ORIGIN.x + 1, tileY: UNION_HALL_ORIGIN.y + 2 },
  officeClerk: { tileX: OFFICE_ORIGIN.x + 1, tileY: OFFICE_ORIGIN.y + 2 },
  miner: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
