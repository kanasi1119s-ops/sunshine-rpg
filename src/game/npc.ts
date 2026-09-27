import type { EventCommand } from "./event/types";
import type { Direction } from "../input/direction";
import type { PlayerState } from "./player";

export interface Npc {
  id: string;
  tileX: number;
  tileY: number;
  /** ドット絵ができるまでの仮の色。 */
  color: string;
  commands: EventCommand[];
}

const FACING_OFFSET: Record<Direction, { dx: number; dy: number }> = {
  up: { dx: 0, dy: -1 },
  down: { dx: 0, dy: 1 },
  left: { dx: -1, dy: 0 },
  right: { dx: 1, dy: 0 },
};

/** プレイヤーが向いている方向の、すぐ前のタイル座標。 */
export function getFacingTile(
  player: PlayerState,
  tileWidth: number,
  tileHeight: number,
): { tileX: number; tileY: number } {
  const centerTileX = Math.floor((player.x + player.width / 2) / tileWidth);
  const centerTileY = Math.floor((player.y + player.height / 2) / tileHeight);
  const offset = FACING_OFFSET[player.direction];
  return { tileX: centerTileX + offset.dx, tileY: centerTileY + offset.dy };
}

export function findNpcAt(npcs: Npc[], tileX: number, tileY: number): Npc | undefined {
  return npcs.find((npc) => npc.tileX === tileX && npc.tileY === tileY);
}
