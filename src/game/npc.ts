import type { EventCommand } from "./event/types";
import type { Direction } from "../input/direction";
import type { PlayerState } from "./player";

export interface Npc {
  id: string;
  tileX: number;
  tileY: number;
  /** 顔グラフィック（`spriteName`）が無いときの、仮の色。 */
  color: string;
  /** `game/portrait/portraits.ts`のPORTRAITSに登録されている名前。あればマップ上もそのキャラクターのドット絵で表示する。 */
  spriteName?: string;
  commands: EventCommand[];
  /** true なら、家の近くをぶらぶら歩く（`npc-wander.ts`）。町の人だけ。 */
  wander?: boolean;
  /** 宝箱など: このフラグが立つと「開けたあと」の絵になる。 */
  openedFlag?: string;
  /** このフラグが立つと、その場所からいなくなる（倒された敵・去った人）。 */
  hideWhenFlag?: string;
  /** このフラグが立つまでは、いない（人が去ったあとに残る跡など）。 */
  showWhenFlag?: string;
  /** 物語の場面で話す人（`world/scene-residents.ts`）: どれかの場面の時期にあてはまるあいだだけ、その町にいる。 */
  sceneWindows?: Array<{ requires?: string[]; blockedBy?: string[] }>;
  /** 現れるとき、この位置（タイルの数。dx, dy）から、本来の位置まで歩いて出てくる（天幕から出てくる人など）。 */
  emerge?: { dx: number; dy: number };
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
