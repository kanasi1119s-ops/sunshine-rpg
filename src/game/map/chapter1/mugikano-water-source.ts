import type { TileMapData } from "../types";
import { MUGIKANO_TUNNEL_NORTH_ENTRY } from "./mugikano-dungeon";
import { addCornerGroves } from "../organic";

const GRASS = 1;
const PATH = 2;
const TREE = 4;
const ROCK = 5;
const DUG_EARTH = 6;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#4a7a3f",
  [PATH]: "#b79a68",
  [TREE]: "#1f5c33",
  [ROCK]: "#5a5a5a",
  [DUG_EARTH]: "#8a7a5a",
};

/** ドット絵パターン（`tile-art.ts`）を適用する地形カテゴリ。 */
const TILE_ART_MAP: Record<number, string> = {
  [GRASS]: "grass",
  [PATH]: "path",
  [TREE]: "treeCanopy",
};

const NON_WALKABLE = new Set([TREE, ROCK]);

const WIDTH = 18;
const HEIGHT = 14;
const SOUTH_GATE = { x: 9, y: 13 };
/** 水が涸れた水源、その奥にある古い灯り石の採掘跡。 */
const SOURCE_CENTER = { x: 9, y: 2 };

/**
 * 第1章の事件現場、水源・歪みの発生地点（`docs/story/structure.md`「第1章（麦香野）」、
 * `docs/story/mystery.md` 参照）。村の水路工事で偶然掘り当てられた、古い灯り石の
 * 採掘跡（伏線C-002）がある。
 */
export function createMugikanoWaterSourceData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GRASS);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。南だけ、村へ戻る道を1マス開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, TREE);
    set(x, HEIGHT - 1, x === SOUTH_GATE.x ? PATH : TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, TREE);
    set(WIDTH - 1, y, TREE);
  }

  // 南の入口から、水源の採掘跡まで続く一本道。
  for (let y = 1; y < HEIGHT - 1; y++) {
    set(SOUTH_GATE.x, y, PATH);
  }

  // 水源・採掘跡。周りを岩場で囲み、掘り返された地面の色を変える。
  for (let dx = -1; dx <= 1; dx++) {
    set(SOURCE_CENTER.x + dx, SOURCE_CENTER.y - 1, ROCK);
  }
  set(SOURCE_CENTER.x - 1, SOURCE_CENTER.y, ROCK);
  set(SOURCE_CENTER.x + 1, SOURCE_CENTER.y, ROCK);
  set(SOURCE_CENTER.x, SOURCE_CENTER.y, DUG_EARTH);
  set(SOURCE_CENTER.x, SOURCE_CENTER.y + 1, DUG_EARTH);

  // 四隅に木のかたまりを食い込ませて、森のふちをぎざぎざにする（道には置かない）。
  addCornerGroves(WIDTH, HEIGHT, (x, y) => set(x, y, TREE), (x, y) => ground[y * WIDTH + x] !== GRASS, false);

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
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        // 古い坑道へ戻る（奥の岩戸のすぐ手前）。
        targetMapId: "mugikano-tunnel",
        targetTileX: MUGIKANO_TUNNEL_NORTH_ENTRY.tileX,
        targetTileY: MUGIKANO_TUNNEL_NORTH_ENTRY.tileY,
      },
    ],
  };
}

/** 村から入ってきたときの立ち位置。 */
export const MUGIKANO_WATER_SOURCE_ENTRY = { tileX: SOUTH_GATE.x, tileY: HEIGHT - 2 };

/** 採掘跡・歪み本体を置く座標（イベントデータ側で使う）。 */
export const MUGIKANO_WATER_SOURCE_LANDMARKS = {
  excavationMark: { tileX: SOURCE_CENTER.x + 2, tileY: 7 },
  yugami: { tileX: SOURCE_CENTER.x, tileY: SOURCE_CENTER.y + 1 },
};
