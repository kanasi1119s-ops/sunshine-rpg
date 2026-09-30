import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const PILLAR = 3;
const VOID = 4;
const DOOR = 5;
const GLOW = 6;
const MURAL = 7;
const BED = 8;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8e8aa0",
  [WALL]: "#2e2c3c",
  [PILLAR]: "#5c5a72",
  [VOID]: "#14121e",
  [DOOR]: "#c8b46a",
  [GLOW]: "#a8d4e8",
  [MURAL]: "#7a5a8a",
  [BED]: "#b8a8c8",
};

const NON_WALKABLE = new Set([WALL, PILLAR, VOID, MURAL, BED]);

interface Exit {
  x: number;
  y: number;
  targetMapId: string;
  targetTileX: number;
  targetTileY: number;
}

/** 外周を壁で囲んだ床に、飾りタイルと出入り口を置いて地図データにする。 */
function buildMap(
  width: number,
  height: number,
  decorate: (set: (x: number, y: number, tile: number) => void) => void,
  exits: Exit[],
): TileMapData {
  const ground: number[] = new Array(width * height).fill(FLOOR);
  const collision: number[] = new Array(width * height).fill(0);
  const set = (x: number, y: number, tile: number): void => {
    ground[y * width + x] = tile;
    collision[y * width + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };
  for (let x = 0; x < width; x++) {
    set(x, 0, WALL);
    set(x, height - 1, WALL);
  }
  for (let y = 0; y < height; y++) {
    set(0, y, WALL);
    set(width - 1, y, WALL);
  }
  decorate(set);
  for (const exit of exits) {
    set(exit.x, exit.y, DOOR);
  }
  return {
    width,
    height,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: exits.map((e) => ({ tileX: e.x, tileY: e.y, targetMapId: e.targetMapId, targetTileX: e.targetTileX, targetTileY: e.targetTileY })),
  };
}

const COURT_W = 24;
const COURT_H = 16;
const COURT_SOUTH = { x: 12, y: COURT_H - 1 };
const COURT_NORTH = { x: 12, y: 0 };

/**
 * 終章の舞台、虚灯宮の外庭。空に浮かぶ白い回廊が、光る床のまわりに続く。
 * 南の門から灯芯都へ戻れ、北の扉が環の回廊へ通じる。
 */
export function createKyotoukyuCourtData(): TileMapData {
  return buildMap(
    COURT_W,
    COURT_H,
    (set) => {
      for (let y = 2; y < COURT_H - 2; y++) {
        for (const x of [3, 4, 19, 20]) {
          set(x, y, VOID);
        }
      }
      for (const y of [4, 8, 12]) {
        set(8, y, PILLAR);
        set(15, y, PILLAR);
      }
      for (let y = 1; y < COURT_H - 1; y++) {
        set(11, y, GLOW);
        set(13, y, GLOW);
      }
      set(COURT_NORTH.x, 0, DOOR);
    },
    [
      { x: COURT_SOUTH.x, y: COURT_SOUTH.y, targetMapId: "toushin-town", targetTileX: 13, targetTileY: 15 },
      { x: COURT_NORTH.x, y: COURT_NORTH.y, targetMapId: "kyotoukyu-corridor", targetTileX: 6, targetTileY: 19 },
    ],
  );
}
export const KYOTOUKYU_COURT_ENTRY = { tileX: COURT_SOUTH.x, tileY: COURT_SOUTH.y - 2 };
export const KYOTOUKYU_COURT_LANDMARKS = {
  keeper: { tileX: 10, tileY: 12 },
};

const COR_W = 13;
const COR_H = 22;
const COR_SOUTH = { x: 6, y: COR_H - 1 };
const COR_NORTH = { x: 6, y: 0 };

/** 環の回廊。壁画に「灯の環」と歪みの由来が刻まれている。 */
export function createKyotoukyuCorridorData(): TileMapData {
  return buildMap(
    COR_W,
    COR_H,
    (set) => {
      for (let y = 2; y < COR_H - 2; y += 3) {
        set(2, y, PILLAR);
        set(10, y, PILLAR);
      }
      // 奥の壁画（左右の壁ぎわ）。
      for (let y = 8; y < 12; y++) {
        set(1, y, MURAL);
        set(11, y, MURAL);
      }
      for (let y = 1; y < COR_H - 1; y++) {
        set(6, y, GLOW);
      }
    },
    [
      { x: COR_SOUTH.x, y: COR_SOUTH.y, targetMapId: "kyotoukyu-court", targetTileX: 12, targetTileY: 2 },
      { x: COR_NORTH.x, y: COR_NORTH.y, targetMapId: "kyotoukyu-sanctum", targetTileX: 9, targetTileY: 11 },
    ],
  );
}
export const KYOTOUKYU_CORRIDOR_ENTRY = { tileX: COR_SOUTH.x, tileY: COR_SOUTH.y - 2 };
export const KYOTOUKYU_CORRIDOR_LANDMARKS = {
  muralLeft: { tileX: 2, tileY: 9 },
  muralRight: { tileX: 10, tileY: 10 },
};

const SAN_W = 19;
const SAN_H = 13;
const SAN_SOUTH = { x: 9, y: SAN_H - 1 };

/** 奥の間。祖父ソウイチが眠る寝台と、エドレアが待つ祭壇がある。 */
export function createKyotoukyuSanctumData(): TileMapData {
  return buildMap(
    SAN_W,
    SAN_H,
    (set) => {
      for (let x = 7; x < 12; x++) {
        set(x, 2, GLOW);
      }
      // 祖父の寝台（2x1）。
      set(3, 3, BED);
      set(4, 3, BED);
      for (const [x, y] of [[2, 6], [16, 6], [2, 9], [16, 9]]) {
        set(x, y, PILLAR);
      }
    },
    [{ x: SAN_SOUTH.x, y: SAN_SOUTH.y, targetMapId: "kyotoukyu-corridor", targetTileX: 6, targetTileY: 2 }],
  );
}
export const KYOTOUKYU_SANCTUM_ENTRY = { tileX: SAN_SOUTH.x, tileY: SAN_SOUTH.y - 2 };
export const KYOTOUKYU_SANCTUM_LANDMARKS = {
  grandfather: { tileX: 4, tileY: 4 },
  edrea: { tileX: 9, tileY: 4 },
};
