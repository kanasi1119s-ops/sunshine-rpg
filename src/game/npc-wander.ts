import type { Direction } from "../input/direction";
import { findExitAt, isWalkable, type TileMap } from "./map/tile-map";
import type { Npc } from "./npc";

/**
 * 町の人の「ぶらぶら歩き」。`wander: true` の町の人だけが、家（最初の位置）から2マスの範囲を、ときどき1マスずつ歩く。
 * 歩く向きに顔を向け、歩いている間は歩きのコマで動く（見た目だけでなく、話しかける位置も歩いた先のマスに変わる）。
 * 出入り口・通れないマス・ほかの人・プレイヤーのいるマスには入らない。
 */
export interface WanderState {
  homeX: number;
  homeY: number;
  fromX: number;
  fromY: number;
  /** 0〜1。1で歩き終わり。 */
  t: number;
  moving: boolean;
  dir: Direction;
  /** 次に歩き出すまでの待ち時間（ミリ秒）。 */
  waitMs: number;
  /** 歩きのコマを決める経過時間。 */
  animMs: number;
}

export const WANDER_RADIUS = 2;
export const WANDER_MOVE_MS = 460;

const states = new Map<string, WanderState>();

const DIRS: Array<{ dir: Direction; dx: number; dy: number }> = [
  { dir: "up", dx: 0, dy: -1 },
  { dir: "down", dx: 0, dy: 1 },
  { dir: "left", dx: -1, dy: 0 },
  { dir: "right", dx: 1, dy: 0 },
];

export function wanderStateOf(npcId: string): WanderState | undefined {
  return states.get(npcId);
}

function ensure(npc: Npc, rng: () => number): WanderState {
  let s = states.get(npc.id);
  if (!s) {
    s = { homeX: npc.tileX, homeY: npc.tileY, fromX: npc.tileX, fromY: npc.tileY, t: 1, moving: false, dir: "down", waitMs: 800 + rng() * 3000, animMs: 0 };
    states.set(npc.id, s);
  }
  return s;
}

/** 話しかけられたとき、相手のほうを向く。 */
export function faceNpc(npc: Npc, dir: Direction): void {
  const s = states.get(npc.id);
  if (s && !s.moving) {
    s.dir = dir;
  }
}

export function opposite(dir: Direction): Direction {
  return dir === "up" ? "down" : dir === "down" ? "up" : dir === "left" ? "right" : "left";
}

/** 毎フレーム呼ぶ。`paused` が true（会話中など）の間は、歩き出さない（歩いている途中の人は、その一歩だけ歩き終える）。 */
export function updateWander(
  npcs: Npc[],
  map: TileMap,
  playerTile: { x: number; y: number },
  dtMs: number,
  paused: boolean,
  rng: () => number,
): void {
  for (const npc of npcs) {
    if (!npc.wander) {
      continue;
    }
    const s = ensure(npc, rng);
    if (s.moving) {
      s.animMs += dtMs;
      s.t = Math.min(1, s.t + dtMs / WANDER_MOVE_MS);
      if (s.t >= 1) {
        s.moving = false;
        s.animMs = 0;
        s.waitMs = 1500 + rng() * 4500;
      }
      continue;
    }
    if (paused) {
      continue;
    }
    s.waitMs -= dtMs;
    if (s.waitMs > 0) {
      continue;
    }
    s.waitMs = 600 + rng() * 1500;
    const choice = DIRS[Math.floor(rng() * DIRS.length)];
    const tx = npc.tileX + choice.dx;
    const ty = npc.tileY + choice.dy;
    s.dir = choice.dir;
    const blocked =
      Math.abs(tx - s.homeX) > WANDER_RADIUS ||
      Math.abs(ty - s.homeY) > WANDER_RADIUS ||
      !isWalkable(map, tx, ty) ||
      !!findExitAt(map, tx, ty) ||
      (playerTile.x === tx && playerTile.y === ty) ||
      npcs.some((other) => other !== npc && other.tileX === tx && other.tileY === ty);
    if (blocked) {
      continue;
    }
    s.fromX = npc.tileX;
    s.fromY = npc.tileY;
    npc.tileX = tx;
    npc.tileY = ty;
    s.moving = true;
    s.t = 0;
    s.animMs = 0;
  }
}
