import type { TileMapData } from "./types";

const GRASS = 1;
const PATH = 2;
const WATER = 3;
const TREE = 4;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#3f8f4f",
  [PATH]: "#c9a86a",
  [WATER]: "#3a6ea5",
  [TREE]: "#1f5c33",
};

const NON_WALKABLE = new Set([WATER, TREE]);

/**
 * エンジンの動作確認用の仮マップ（単色タイル）。
 * 木で囲まれた原っぱの中央を道が横切り、隅に小さな池がある。
 * 本物のドット絵ができるまでのプレースホルダー。
 */
export function createSampleMapData(): TileMapData {
  const width = 20;
  const height = 12;
  const ground: number[] = new Array(width * height).fill(GRASS);
  const collision: number[] = new Array(width * height).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * width + x] = tile;
    collision[y * width + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。
  for (let x = 0; x < width; x++) {
    set(x, 0, TREE);
    set(x, height - 1, TREE);
  }
  for (let y = 0; y < height; y++) {
    set(0, y, TREE);
    set(width - 1, y, TREE);
  }

  // 縦の道と横の道を1本ずつ通す。
  const pathY = Math.floor(height / 2);
  for (let x = 1; x < width - 1; x++) {
    set(x, pathY, PATH);
  }
  const pathX = Math.floor(width / 2);
  for (let y = 1; y < height - 1; y++) {
    set(pathX, y, PATH);
  }

  // 隅に小さな池。
  for (let y = 2; y <= 3; y++) {
    for (let x = 2; x <= 4; x++) {
      set(x, y, WATER);
    }
  }

  return {
    width,
    height,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
  };
}

/** プレイヤーの初期位置（タイル座標）。道の交差点にする。 */
export const SAMPLE_MAP_SPAWN = {
  tileX: Math.floor(20 / 2),
  tileY: Math.floor(12 / 2),
};
