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

/**
 * 決められた道を歩かせる（物語の場面で、話し手が主人公のそばまで歩いてくる・元の所へ帰るとき。2026-10-06、
 * 人間の指示「会話イベントもドットキャラは近づくときは歩いてきて、必ず町にいるように」）。
 * 道は、いまのマスのとなりから、着くマスまで（1マスずつ、上下左右につながる）。ぶらぶら歩きの人でなくても歩ける。
 */
const scripted = new Map<string, Array<{ x: number; y: number }>>();
/** 場面で歩く一歩の時間（ふだんのぶらぶら歩きより少し速い）。 */
export const SCRIPTED_MOVE_MS = 260;

export function walkNpcAlong(npc: Npc, path: Array<{ x: number; y: number }>): void {
  ensure(npc, () => 0.5);
  if (path.length > 0) scripted.set(npc.id, path.map((p) => ({ ...p })));
}

/** 決められた道を歩いている人がいるか。 */
export function isScriptedWalking(npcId?: string): boolean {
  return npcId ? scripted.has(npcId) : scripted.size > 0;
}

/** 決められた道を、すぐに歩き終えたことにする（地図が変わったときなど）。 */
export function finishScriptedWalks(npcs: Npc[]): void {
  for (const npc of npcs) {
    const path = scripted.get(npc.id);
    if (!path || path.length === 0) continue;
    const last = path[path.length - 1];
    npc.tileX = last.x;
    npc.tileY = last.y;
    const s = states.get(npc.id);
    if (s) s.moving = false;
  }
  scripted.clear();
}

function stepScripted(npc: Npc, s: WanderState, dtMs: number): void {
  const path = scripted.get(npc.id)!;
  if (s.moving) {
    s.animMs += dtMs;
    s.t = Math.min(1, s.t + dtMs / SCRIPTED_MOVE_MS);
    if (s.t < 1) return;
    s.moving = false;
  }
  const next = path.shift();
  if (!next) {
    scripted.delete(npc.id);
    s.animMs = 0;
    s.waitMs = 1500;
    return;
  }
  s.dir = next.x > npc.tileX ? "right" : next.x < npc.tileX ? "left" : next.y > npc.tileY ? "down" : "up";
  s.fromX = npc.tileX;
  s.fromY = npc.tileY;
  npc.tileX = next.x;
  npc.tileY = next.y;
  s.moving = true;
  s.t = 0;
}

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
    if (scripted.has(npc.id)) {
      stepScripted(npc, ensure(npc, rng), dtMs);
      continue;
    }
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
