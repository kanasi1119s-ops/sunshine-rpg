import type { Direction } from "../input/direction";
import { isWalkable, type TileMap } from "./map/tile-map";

export interface PlayerState {
  /** ワールド座標（ピクセル）。プレイヤーの左上を表す。 */
  x: number;
  y: number;
  width: number;
  height: number;
  direction: Direction;
  moving: boolean;
}

export function createPlayer(x: number, y: number): PlayerState {
  return { x, y, width: 12, height: 14, direction: "down", moving: false };
}

const DIRECTION_VECTOR: Record<Direction, { dx: number; dy: number }> = {
  up: { dx: 0, dy: -1 },
  down: { dx: 0, dy: 1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

const SPEED_PX_PER_SEC = 64;

/** プレイヤーの足元4隅すべてが通れるタイルなら移動を許可する。 */
function canMoveTo(map: TileMap, nextX: number, nextY: number, width: number, height: number): boolean {
  const tileWidth = map.data.tileWidth;
  const tileHeight = map.data.tileHeight;
  const corners: [number, number][] = [
    [nextX, nextY],
    [nextX + width - 1, nextY],
    [nextX, nextY + height - 1],
    [nextX + width - 1, nextY + height - 1],
  ];
  return corners.every(([cx, cy]) =>
    isWalkable(map, Math.floor(cx / tileWidth), Math.floor(cy / tileHeight)),
  );
}

export function updatePlayer(
  state: PlayerState,
  direction: Direction | null,
  dtMs: number,
  map: TileMap,
): PlayerState {
  if (!direction) {
    return { ...state, moving: false };
  }

  const { dx, dy } = DIRECTION_VECTOR[direction];
  const distance = (SPEED_PX_PER_SEC * dtMs) / 1000;
  const nextX = state.x + dx * distance;
  const nextY = state.y + dy * distance;

  if (!canMoveTo(map, nextX, nextY, state.width, state.height)) {
    return { ...state, direction, moving: false };
  }

  return { ...state, x: nextX, y: nextY, direction, moving: true };
}
