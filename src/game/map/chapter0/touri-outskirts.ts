import type { TileMapData } from "../types";

const GRASS = 1;
const PATH = 2;
const TREE = 4;
const ROCK = 5;
const RIFT_GROUND = 6;

const TILE_COLORS: Record<number, string> = {
  [GRASS]: "#4a7a3f",
  [PATH]: "#b79a68",
  [TREE]: "#1f5c33",
  [ROCK]: "#5a5a5a",
  [RIFT_GROUND]: "#5b3a7a",
};

const NON_WALKABLE = new Set([TREE, ROCK]);

const WIDTH = 18;
const HEIGHT = 14;
const SOUTH_GATE = { x: 9, y: 13 };
const RIFT_CENTER = { x: 9, y: 2 };

/**
 * 町外れ・歪みの発生地点（序章の事件現場、`docs/story/structure.md`「序章（灯里）」参照）。
 * 見た目はエンジン動作確認用と同じ単色タイル。RIFT_GROUND のあたりが「歪み」の現れる場所。
 */
export function createTouriOutskirtsData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(GRASS);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周を木で囲む。南側だけ、町へ戻る道を1マス開けておく。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, TREE);
    set(x, HEIGHT - 1, x === SOUTH_GATE.x ? PATH : TREE);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, TREE);
    set(WIDTH - 1, y, TREE);
  }

  // 南の入口から、歪みの発生地点まで続く一本道。
  for (let y = 1; y < HEIGHT - 1; y++) {
    set(SOUTH_GATE.x, y, PATH);
  }

  // 歪みの発生地点。周りを岩場で囲み、地面の色を変えて異様さを出す。
  for (let dx = -1; dx <= 1; dx++) {
    set(RIFT_CENTER.x + dx, RIFT_CENTER.y - 1, ROCK);
  }
  set(RIFT_CENTER.x - 1, RIFT_CENTER.y, ROCK);
  set(RIFT_CENTER.x + 1, RIFT_CENTER.y, ROCK);
  set(RIFT_CENTER.x, RIFT_CENTER.y, RIFT_GROUND);
  set(RIFT_CENTER.x, RIFT_CENTER.y + 1, RIFT_GROUND);

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
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        targetMapId: "touri-town",
        targetTileX: 11,
        targetTileY: 1,
      },
    ],
  };
}

/** 町から入ってきたときの立ち位置。 */
export const TOURI_OUTSKIRTS_ENTRY = { tileX: SOUTH_GATE.x, tileY: HEIGHT - 2 };

/** 調査ポイント・歪み本体を置く座標（イベントデータ側で使う）。 */
export const TOURI_OUTSKIRTS_LANDMARKS = {
  scorchMark: { tileX: RIFT_CENTER.x + 2, tileY: 7 },
  yugami: { tileX: RIFT_CENTER.x, tileY: RIFT_CENTER.y + 1 },
};
