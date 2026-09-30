import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const BLOCK = 3;
const DOOR = 4;
const GLOW = 5;

export interface Palette {
  floor: string;
  wall: string;
  block: string;
  glow: string;
}

const W = 20;
const H = 14;
const SOUTH = { x: 10, y: H - 1 };
/** 北の封印の扉（NPCが立つ。灯り石を2つともらすと通れる）。 */
export const DEEP_GATE = { tileX: 10, tileY: 2 };

export interface DeepExit {
  targetMapId: string;
  targetTileX: number;
  targetTileY: number;
}

export function buildFloor(palette: Palette, blocks: [number, number][], southExit: DeepExit): TileMapData {
  const ground: number[] = new Array(W * H).fill(FLOOR);
  const collision: number[] = new Array(W * H).fill(0);
  const set = (x: number, y: number, tile: number): void => {
    ground[y * W + x] = tile;
    collision[y * W + x] = tile === WALL || tile === BLOCK ? 1 : 0;
  };
  for (let x = 0; x < W; x++) {
    set(x, 0, WALL);
    set(x, H - 1, WALL);
  }
  for (let y = 0; y < H; y++) {
    set(0, y, WALL);
    set(W - 1, y, WALL);
  }
  // 北の扉の手前を壁で仕切り、扉のマスだけを通れるようにする。
  for (let x = 1; x < W - 1; x++) {
    if (x !== DEEP_GATE.tileX) {
      set(x, DEEP_GATE.tileY, WALL);
    }
  }
  for (let y = 1; y < DEEP_GATE.tileY; y++) {
    set(DEEP_GATE.tileX, y, GLOW);
  }
  for (const [x, y] of blocks) {
    set(x, y, BLOCK);
  }
  set(SOUTH.x, SOUTH.y, DOOR);
  return {
    width: W,
    height: H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { [FLOOR]: palette.floor, [WALL]: palette.wall, [BLOCK]: palette.block, [DOOR]: "#c8b46a", [GLOW]: palette.glow },
    collision,
    exits: [{ tileX: SOUTH.x, tileY: SOUTH.y, ...southExit }],
  };
}

const ENTRY = { tileX: SOUTH.x, tileY: SOUTH.y - 2 };
/** 各階層の、北の扉のすぐ手前（次の階から戻ってきたときの立ち位置）。 */
export const BEFORE_GATE = { tileX: DEEP_GATE.tileX, tileY: DEEP_GATE.tileY + 2 };

export const DEEP_ENTRY = ENTRY;
export const DEEP_LANDMARKS = {
  pedestalA: { tileX: 4, tileY: 6 },
  pedestalB: { tileX: 15, tileY: 6 },
  echo: { tileX: 6, tileY: 10 },
  gate: DEEP_GATE,
  boss: { tileX: 10, tileY: 4 },
  circle: DEEP_GATE,
};

/** 第1階層「大乱期の残響」: 氷と瓦礫。 */
export function createDeep1Data(): TileMapData {
  return buildFloor(
    { floor: "#b8d0e0", wall: "#4a5a6a", block: "#7a8290", glow: "#e0f0ff" },
    [[7, 8], [8, 8], [12, 9], [13, 9], [3, 10], [16, 11]],
    { targetMapId: "kyotoukyu-sanctum", targetTileX: 15, targetTileY: 5 },
  );
}

/** 第2階層「静まりの残響」: 静まりの年の灯芯都を思わせる石の広間。 */
export function createDeep2Data(): TileMapData {
  return buildFloor(
    { floor: "#a89a80", wall: "#4a4438", block: "#6a6250", glow: "#f0e0a0" },
    [[4, 9], [15, 9], [7, 11], [12, 11], [2, 4], [17, 4]],
    { targetMapId: "deep-1", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  );
}

/** 第3階層「歪みの残響」: 過去の歪みの姿がゆらめく紫の間。 */
export function createDeep3Data(): TileMapData {
  return buildFloor(
    { floor: "#5a4468", wall: "#241a30", block: "#3a2a4a", glow: "#c8a0f0" },
    [[6, 6], [13, 6], [8, 10], [11, 10], [2, 8], [17, 8]],
    { targetMapId: "deep-2", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  );
}

/** 第4階層「初源の間」: 白と黒の円い間。奥で初源の歪みが待つ。 */
export function createDeep4Data(): TileMapData {
  return buildFloor(
    { floor: "#d8d0f0", wall: "#16121e", block: "#8a80a8", glow: "#ffffff" },
    [[5, 5], [14, 5], [5, 9], [14, 9]],
    { targetMapId: "deep-3", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  );
}
