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
  /** 歩行アニメーション用に、動いている間だけ進む経過時間（ms）。止まると0に戻る。 */
  animationMs: number;
}

export function createPlayer(x: number, y: number): PlayerState {
  return { x, y, width: 12, height: 14, direction: "down", moving: false, animationMs: 0 };
}

const DIRECTION_VECTOR: Record<Direction, { dx: number; dy: number }> = {
  up: { dx: 0, dy: -1 },
  down: { dx: 0, dy: 1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

const SPEED_PX_PER_SEC = 64;

/** プレイヤーの足元4隅すべてが通れるタイルなら移動を許可する。 */
function canMoveTo(
  map: TileMap,
  nextX: number,
  nextY: number,
  width: number,
  height: number,
  blockedTiles: readonly TilePos[],
  from?: { x: number; y: number },
): boolean {
  const tileWidth = map.data.tileWidth;
  const tileHeight = map.data.tileHeight;
  const corners: [number, number][] = [
    [nextX, nextY],
    [nextX + width - 1, nextY],
    [nextX, nextY + height - 1],
    [nextX + width - 1, nextY + height - 1],
  ];
  if (!corners.every(([cx, cy]) => isWalkable(map, Math.floor(cx / tileWidth), Math.floor(cy / tileHeight)))) {
    return false;
  }
  // 人（NPC）のいるマスには入れない。すでに重なっているときは、離れる向きの移動だけ許す。
  return blockedTiles.every((t) => {
    const hits = (x: number, y: number): boolean =>
      x < (t.tileX + 1) * tileWidth && x + width > t.tileX * tileWidth && y < (t.tileY + 1) * tileHeight && y + height > t.tileY * tileHeight;
    if (!hits(nextX, nextY)) return true;
    return from !== undefined && hits(from.x, from.y);
  });
}

export interface TilePos {
  tileX: number;
  tileY: number;
}

/** 角や出口にひっかかったとき、この距離（px）以内のずれなら、自動で横へすべって通れるようにする。 */
const SLIDE_ASSIST_PX = 10;

export function updatePlayer(
  state: PlayerState,
  direction: Direction | null,
  dtMs: number,
  map: TileMap,
  /** 通れないマス（NPCのいる場所）。 */
  blockedTiles: readonly TilePos[] = [],
): PlayerState {
  if (!direction) {
    return { ...state, moving: false, animationMs: 0 };
  }

  const { dx, dy } = DIRECTION_VECTOR[direction];
  const distance = (SPEED_PX_PER_SEC * dtMs) / 1000;
  const nextX = state.x + dx * distance;
  const nextY = state.y + dy * distance;

  const from = { x: state.x, y: state.y };
  const wrapPos = (p: PlayerState): PlayerState => {
    if (!map.data.wrap) return p;
    const w = map.widthPx, h = map.heightPx;
    return { ...p, x: ((p.x % w) + w) % w, y: ((p.y % h) + h) % h };
  };
  if (!canMoveTo(map, nextX, nextY, state.width, state.height, blockedTiles, from)) {
    // 出口・扉・角の手前で少しずれていても、通れる位置まで横へすべらせる（すべり補助）。
    const slide = findSlide(map, state, dx, dy, nextX, nextY, blockedTiles, from);
    if (slide !== 0) {
      const step = Math.min(Math.abs(slide), distance) * Math.sign(slide);
      const slidX = dx === 0 ? state.x + step : state.x;
      const slidY = dy === 0 ? state.y + step : state.y;
      if (canMoveTo(map, slidX, slidY, state.width, state.height, blockedTiles, from)) {
        return wrapPos({ ...state, x: slidX, y: slidY, direction, moving: true, animationMs: state.animationMs + dtMs });
      }
    }
    return { ...state, direction, moving: false, animationMs: 0 };
  }

  return wrapPos({ ...state, x: nextX, y: nextY, direction, moving: true, animationMs: state.animationMs + dtMs });
}

/** 進みたい向きが塞がれているとき、横へ何px動けば通れるか（0なら通れる位置が近くにない）。 */
function findSlide(
  map: TileMap,
  state: PlayerState,
  dx: number,
  dy: number,
  nextX: number,
  nextY: number,
  blockedTiles: readonly TilePos[],
  from: { x: number; y: number },
): number {
  for (let offset = 1; offset <= SLIDE_ASSIST_PX; offset++) {
    for (const sign of [1, -1]) {
      const x = dx === 0 ? nextX + sign * offset : nextX;
      const y = dy === 0 ? nextY + sign * offset : nextY;
      if (canMoveTo(map, x, y, state.width, state.height, blockedTiles, from)) {
        return sign * offset;
      }
    }
  }
  return 0;
}
