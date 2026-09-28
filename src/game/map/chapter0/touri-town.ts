import type { TileMapData } from "../types";

const GRASS = 1;
const PATH = 2;
const WATER = 3;
const TREE = 4;
const BRANCH_WALL = 5;
const BRANCH_DOOR = 6;
const INN_WALL = 7;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#3f8f4f",
  [PATH]: "#c9a86a",
  [WATER]: "#3a6ea5",
  [TREE]: "#1f5c33",
  [BRANCH_WALL]: "#7a6a52",
  [BRANCH_DOOR]: "#6b4a2b",
  [INN_WALL]: "#8a5a3c",
};

/** ドット絵パターン（`tile-art.ts`）を適用する地形カテゴリ。 */
const TILE_ART_MAP: Record<number, string> = {
  [GRASS]: "grass",
  [PATH]: "path",
  [WATER]: "water",
  [TREE]: "treeCanopy",
};

const NON_WALKABLE = new Set([WATER, TREE, BRANCH_WALL, INN_WALL]);

const WIDTH = 22;
const HEIGHT = 16;

/** 相談所支部の建物の位置（3x2）。ドアは建物のすぐ南（(5,5)）。 */
const BRANCH_ORIGIN = { x: 4, y: 3 };
/** 宿屋（客室はまだ作っていない、外観のみの仮の建物）。 */
const INN_ORIGIN = { x: 15, y: 3 };

const NORTH_GATE = { x: 11, y: 0 };
const BRANCH_DOOR_POS = { x: 5, y: 5 };
const mainStreetY = 8;
/** 麦香野（第1章）へ続く街道の入り口。町の東端。 */
const EAST_GATE = { x: WIDTH - 1, y: mainStreetY };

/**
 * 序章の舞台、港町・灯里（`docs/story/bible.md`・`structure.md` 参照）。
 * 見た目はエンジン動作確認用と同じ単色タイル（本物のドット絵はフェーズ3のアート工程で追加）。
 */
export function createTouriTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GRASS);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。北側だけ、町外れへ抜ける道を1マス開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === NORTH_GATE.x ? PATH : TREE);
    set(x, HEIGHT - 1, TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, TREE);
    set(WIDTH - 1, y, y === EAST_GATE.y ? PATH : TREE);
  }

  // 町の中心を貫く道（縦の大通り＋横の大通り）。東の端は麦香野への街道の入り口。
  for (let y = 1; y < HEIGHT - 1; y++) {
    set(NORTH_GATE.x, y, PATH);
  }
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, mainStreetY, PATH);
  }

  // 灯りの相談所 灯里支部（建物）と、支部前から大通りへの脇道。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(BRANCH_ORIGIN.x + dx, BRANCH_ORIGIN.y + dy, BRANCH_WALL);
    }
  }
  set(BRANCH_DOOR_POS.x, BRANCH_DOOR_POS.y, BRANCH_DOOR);
  for (let y = BRANCH_DOOR_POS.y + 1; y <= mainStreetY; y++) {
    set(BRANCH_DOOR_POS.x, y, PATH);
  }

  // 宿屋（外観のみ。客室・宿泊機能は今後の工程で追加する仮の建物）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(INN_ORIGIN.x + dx, INN_ORIGIN.y + dy, INN_WALL);
    }
  }

  // 小さな入り江（港町らしさを出す池）。
  for (let y = 11; y <= 12; y++) {
    for (let x = 2; x <= 3; x++) {
      set(x, y, WATER);
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
        // 町外れ（歪みの発生地点）へ。
        tileX: NORTH_GATE.x,
        tileY: NORTH_GATE.y,
        targetMapId: "touri-outskirts",
        targetTileX: 9,
        targetTileY: 12,
      },
      {
        // 灯りの相談所 灯里支部の中へ。
        tileX: BRANCH_DOOR_POS.x,
        tileY: BRANCH_DOOR_POS.y,
        targetMapId: "touri-branch",
        targetTileX: 4,
        targetTileY: 5,
      },
      {
        // 麦香野（第1章）へ続く街道。
        tileX: EAST_GATE.x,
        tileY: EAST_GATE.y,
        targetMapId: "mugikano-village",
        targetTileX: 2,
        targetTileY: 8,
      },
    ],
  };
}

/** 主人公の初期位置（大通りの交差点のすぐ南）。 */
export const TOURI_TOWN_SPAWN = { tileX: NORTH_GATE.x, tileY: 9 };

/** 支部を出たとき、大通りに戻ってくる位置。 */
export const TOURI_TOWN_BRANCH_RETURN = { tileX: BRANCH_DOOR_POS.x, tileY: BRANCH_DOOR_POS.y + 1 };

/** 町の人を置く座標（イベントデータ側で使う）。 */
export const TOURI_TOWN_LANDMARKS = {
  fisherman: { tileX: 3, tileY: 10 },
  innkeeperNeighbor: { tileX: 16, tileY: 6 },
};
