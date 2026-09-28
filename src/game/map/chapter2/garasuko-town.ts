import type { TileMapData } from "../types";

const GROUND = 1;
const PATH = 2;
const WATER = 3;
const TREE = 4;
const STALL_WALL = 5;
const DOCK = 6;

const TILE_COLORS: Record<number, string> = {
  [GROUND]: "#8a9aa0",
  [PATH]: "#c9b98a",
  [WATER]: "#2f6f9a",
  [TREE]: "#1f5c33",
  [STALL_WALL]: "#a9723f",
  [DOCK]: "#8a6a45",
};

/** ドット絵パターン（`tile-art.ts`）を適用する地形カテゴリ。石畳の広場（GROUND）は該当パターンが無いため対象外。 */
const TILE_ART_MAP: Record<number, string> = {
  [PATH]: "path",
  [WATER]: "water",
  [TREE]: "treeCanopy",
};

const NON_WALKABLE = new Set([WATER, TREE, STALL_WALL]);

const WIDTH = 22;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 8 };
const SOUTH_GATE = { x: 11, y: HEIGHT - 1 };
const DOCK_X = 11;
const LAKE_Y = 10;
/** 市場の屋台（2棟、3x2）。 */
const STALL_A_ORIGIN = { x: 5, y: 3 };
const STALL_B_ORIGIN = { x: 14, y: 3 };

/**
 * 第2章の舞台、湖上の交易都市・硝子湖（`docs/story/bible.md`・`structure.md` 参照）。
 * 町の南側は湖そのもので、桟橋（DOCK）を伝って密輸倉庫（`garasuko-warehouse`）へ渡る。
 */
export function createGarasukoTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GROUND);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。西は麦香野からの街道を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, TREE);
    set(x, HEIGHT - 1, x === SOUTH_GATE.x ? DOCK : TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? PATH : TREE);
    set(WIDTH - 1, y, TREE);
  }

  // 町の南側は湖。桟橋だけが対岸（倉庫）まで続く。
  for (let y = LAKE_Y; y < HEIGHT - 1; y++) {
    for (let x = 1; x < WIDTH - 1; x++) {
      set(x, y, x === DOCK_X ? DOCK : WATER);
    }
  }

  // 西の街道から広場・桟橋までの道。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, PATH);
  }
  for (let y = WEST_GATE.y; y < LAKE_Y; y++) {
    set(DOCK_X, y, PATH);
  }

  // 市場の屋台（外観のみ、2棟）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(STALL_A_ORIGIN.x + dx, STALL_A_ORIGIN.y + dy, STALL_WALL);
      set(STALL_B_ORIGIN.x + dx, STALL_B_ORIGIN.y + dy, STALL_WALL);
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
        // 麦香野へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "mugikano-village",
        targetTileX: 20,
        targetTileY: 8,
      },
      {
        // 桟橋を渡って密輸倉庫へ。
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        targetMapId: "garasuko-warehouse",
        targetTileX: 5,
        targetTileY: 11,
      },
    ],
  };
}

/** 麦香野からの街道を渡ってきたときの立ち位置。 */
export const GARASUKO_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 密輸倉庫から戻ってきたときの立ち位置。 */
export const GARASUKO_TOWN_WAREHOUSE_RETURN = { tileX: SOUTH_GATE.x, tileY: SOUTH_GATE.y - 1 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const GARASUKO_TOWN_LANDMARKS = {
  merchant: { tileX: STALL_A_ORIGIN.x + 1, tileY: STALL_A_ORIGIN.y + 2 },
  guide: { tileX: STALL_B_ORIGIN.x + 1, tileY: STALL_B_ORIGIN.y + 2 },
  ferryman: { tileX: DOCK_X, tileY: LAKE_Y - 1 },
};
