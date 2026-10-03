import type { TileMapData } from "../types";
import { addCornerGroves } from "../organic";

const GRASS = 1;
const PATH = 2;
const WATER = 3;
const TREE = 4;
const MILL_WALL = 5;
const HOUSE_WALL = 6;
const BRIDGE = 7;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#5a9a4a",
  [PATH]: "#c9a86a",
  [WATER]: "#3a6ea5",
  [TREE]: "#1f5c33",
  [MILL_WALL]: "#6b5438",
  [HOUSE_WALL]: "#7a5a42",
  [BRIDGE]: "#a97c4f",
};

/** ドット絵パターン（`tile-art.ts`）を適用する地形カテゴリ。 */
const TILE_ART_MAP: Record<number, string> = {
  [GRASS]: "grass",
  [PATH]: "path",
  [WATER]: "water",
  [TREE]: "treeCanopy",
};

const NON_WALKABLE = new Set([WATER, TREE, MILL_WALL, HOUSE_WALL]);

const WIDTH = 22;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 8 };
const EAST_GATE = { x: WIDTH - 1, y: 8 };
const NORTH_GATE = { x: 11, y: 0 };
const CHANNEL_Y = 9;
const BRIDGE_X = 11;
/** 水車小屋（3x2）。 */
const MILL_ORIGIN = { x: 5, y: 3 };
/** 民家（外観のみ）。 */
const HOUSE_ORIGIN = { x: 14, y: 3 };

/**
 * 第1章の舞台、農村地帯・麦香野（`docs/story/bible.md`・`structure.md` 参照）。
 * 村を東西に貫く水路（今は水が涸れている、という設定は会話側で表現する。
 * タイルの見た目自体は水路として描いたままにしている）。
 */
export function createMugikanoVillageData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GRASS);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。西は灯里からの街道、北は水源への道を開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === NORTH_GATE.x ? PATH : TREE);
    set(x, HEIGHT - 1, TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? PATH : TREE);
    set(WIDTH - 1, y, y === EAST_GATE.y ? PATH : TREE);
  }

  // 村を東西に貫く水路。橋の下だけ渡れる。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, CHANNEL_Y, x === BRIDGE_X ? BRIDGE : WATER);
  }

  // 縦の道（水源への北の道〜橋〜村の広場）と、西の街道からの道。
  for (let y = 1; y < HEIGHT - 1; y++) {
    set(BRIDGE_X, y, y === CHANNEL_Y ? BRIDGE : PATH);
  }
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, PATH);
  }

  // 水車小屋（外観のみ）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(MILL_ORIGIN.x + dx, MILL_ORIGIN.y + dy, MILL_WALL);
    }
  }

  // 民家（外観のみ）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(HOUSE_ORIGIN.x + dx, HOUSE_ORIGIN.y + dy, HOUSE_WALL);
    }
  }

  // 四隅に木のかたまりを食い込ませて、森のふちをぎざぎざにする（道には置かない）。
  addCornerGroves(WIDTH, HEIGHT, (x, y) => set(x, y, TREE), (x, y) => ground[y * WIDTH + x] !== GRASS, true);

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
        // 灯里へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "touri-town",
        targetTileX: 20,
        targetTileY: 8,
      },
      {
        // 水源・歪みの発生地点へ。
        tileX: NORTH_GATE.x,
        tileY: NORTH_GATE.y,
        targetMapId: "mugikano-water-source",
        targetTileX: 9,
        targetTileY: 12,
      },
      {
        // 東の街道、第2章の舞台・硝子湖へ。
        tileX: EAST_GATE.x,
        tileY: EAST_GATE.y,
        targetMapId: "garasuko-town",
        targetTileX: 2,
        targetTileY: 8,
      },
    ],
  };
}

/** 灯里からの街道を渡ってきたときの立ち位置。 */
export const MUGIKANO_VILLAGE_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 水源から戻ってきたときの立ち位置。 */
export const MUGIKANO_VILLAGE_WATER_SOURCE_RETURN = { tileX: NORTH_GATE.x, tileY: NORTH_GATE.y + 1 };

/** 硝子湖から戻ってきたときの立ち位置。 */
export const MUGIKANO_VILLAGE_GARASUKO_RETURN = { tileX: EAST_GATE.x - 1, tileY: EAST_GATE.y };

/** 村人・ミナを置く座標（イベントデータ側で使う）。 */
export const MUGIKANO_VILLAGE_LANDMARKS = {
  elder: { tileX: 9, tileY: 7 },
  mina: { tileX: 14, tileY: 10 },
};
