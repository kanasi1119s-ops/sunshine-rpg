import type { TileMapData } from "../types";
import { TOURI_FOREST2_NORTH_ENTRY } from "./touri-forest";

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

  // 南の入口から、歪みの発生地点まで続く道。まっすぐにせず、途中で東へ1マス寄ってまた戻る。
  for (let y = 4; y < HEIGHT - 1; y++) {
    set(y === 5 || y === 6 ? SOUTH_GATE.x + 1 : SOUTH_GATE.x, y, PATH);
  }
  for (const y of [4, 7]) {
    set(SOUTH_GATE.x, y, PATH);
    set(SOUTH_GATE.x + 1, y, PATH);
  }

  // 森のふちを、四角ではなく角のほうへ木が食い込む形にする（四隅のかたまり）。
  const CORNER_TREES: Array<[number, number]> = [
    [1, 1], [2, 1], [3, 1], [1, 2], [2, 2], [1, 3],
    [14, 1], [15, 1], [16, 1], [15, 2], [16, 2], [16, 3],
    [1, 12], [2, 12], [1, 11],
    [16, 12], [15, 12], [16, 11],
  ];
  for (const [x, y] of CORNER_TREES) {
    set(x, y, TREE);
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
    tileArt: TILE_ART_MAP,
    collision,
    exits: [
      {
        tileX: SOUTH_GATE.x,
        tileY: SOUTH_GATE.y,
        // 古い祠の森へ戻る（北の門のすぐ手前）。
        targetMapId: "touri-forest-2",
        targetTileX: TOURI_FOREST2_NORTH_ENTRY.tileX,
        targetTileY: TOURI_FOREST2_NORTH_ENTRY.tileY,
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
