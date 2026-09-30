import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const PILLAR = 3;
const DOOR = 4;
const ALTAR = 5;

/** 8神の禁域の見た目（色）。 */
export interface ShrinePalette {
  floor: string;
  wall: string;
  pillar: string;
  altar: string;
}

const W = 16;
const H = 12;
const SOUTH = { x: 8, y: H - 1 };

export const SHRINE_ENTRY = { tileX: SOUTH.x, tileY: SOUTH.y - 2 };
/** 奥に立つ神（NPC）と、欠片の祭壇の座標（祭壇にはNPCが立つので、歩ける床のままにしてある）。 */
export const SHRINE_LANDMARKS = {
  god: { tileX: 8, tileY: 3 },
  altar: { tileX: 8, tileY: 1 },
  lore: { tileX: 4, tileY: 7 },
};

/**
 * 8神が守る禁域（1部屋）。南の扉から入り、奥の祭壇の手前で神が待つ。
 * @param returnTo 南の扉を出たときの行き先（その神の地方の地図）
 */
export function createShrineData(palette: ShrinePalette, returnTo: { mapId: string; tileX: number; tileY: number }): TileMapData {
  const ground: number[] = new Array(W * H).fill(FLOOR);
  const collision: number[] = new Array(W * H).fill(0);
  const set = (x: number, y: number, tile: number): void => {
    ground[y * W + x] = tile;
    collision[y * W + x] = tile === WALL || tile === PILLAR ? 1 : 0;
  };
  for (let x = 0; x < W; x++) {
    set(x, 0, WALL);
    set(x, H - 1, WALL);
  }
  for (let y = 0; y < H; y++) {
    set(0, y, WALL);
    set(W - 1, y, WALL);
  }
  for (const [x, y] of [[3, 3], [12, 3], [3, 9], [12, 9], [6, 6], [10, 6]]) {
    set(x, y, PILLAR);
  }
  set(SHRINE_LANDMARKS.altar.tileX, SHRINE_LANDMARKS.altar.tileY, ALTAR);
  set(SOUTH.x, SOUTH.y, DOOR);
  return {
    width: W,
    height: H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { [FLOOR]: palette.floor, [WALL]: palette.wall, [PILLAR]: palette.pillar, [DOOR]: "#c8b46a", [ALTAR]: palette.altar },
    collision,
    exits: [{ tileX: SOUTH.x, tileY: SOUTH.y, targetMapId: returnTo.mapId, targetTileX: returnTo.tileX, targetTileY: returnTo.tileY }],
  };
}
