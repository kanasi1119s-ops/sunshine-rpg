import type { TileMapData } from "../types";

/**
 * 霧断崖の「環の聖堂」の中（2026-10-05、人間の指示「司祭がいるなら教会もほしい。教会内ならエディタ使って細かく作って」）。
 * 見た目は1枚絵 `prop:church-interior`（assets-src/pixel-practice/r17-polish/church.py で描き、ドット絵エディタで確かめたもの）。
 * 13×11マス。奥に祭壇と、金の灯の環（8つの灯＝8柱の神）、ステンドグラス。左右に長いすが4列ずつ。まんなかの赤いじゅうたんが通路。
 * 通れるかどうかは、絵に合わせて下の collision で決める（壁・祭壇・燭台・長いすは通れない）。
 */
const W = 13;
const H = 11;
const FLOOR = 1;
const WALL = 2;

/** 聖堂の入口（下のまんなかの扉）。 */
export const KIRI_CHURCH_DOOR = { x: 6, y: 10 };
/** 町から入ったときの立ち位置。 */
export const KIRI_CHURCH_ENTRY = { tileX: 6, tileY: 9 };
/** 中の人の立ち位置。司祭は祭壇の前、修道士は左の燭台のそば、祈る人は右。 */
export const KIRI_CHURCH_SPOTS = {
  priest: { tileX: 6, tileY: 4 },
  friar: { tileX: 2, tileY: 4 },
  worshipper: { tileX: 10, tileY: 4 },
};

export function createKiriChurchData(townDoor: { x: number; y: number }): TileMapData {
  const ground = new Array<number>(W * H).fill(FLOOR);
  const collision = new Array<number>(W * H).fill(0);
  const block = (x: number, y: number): void => {
    ground[y * W + x] = WALL;
    collision[y * W + x] = 1;
  };
  for (let x = 0; x < W; x++) {
    for (let y = 0; y <= 2; y++) block(x, y);          // 奥の壁・ステンドグラス・祭壇
    if (x !== KIRI_CHURCH_DOOR.x) block(x, H - 1);      // 手前の壁（扉のところだけ開く）
  }
  for (let y = 0; y < H; y++) {
    block(0, y);
    block(W - 1, y);                                     // 左右の壁と柱
  }
  for (let x = 3; x <= 9; x++) block(x, 3);             // 祭壇の段と、左右の燭台
  for (let y = 5; y <= 9; y++) {
    for (const x of [1, 2, 3, 4, 8, 9, 10, 11]) block(x, y);   // 長いす（左右に4列）
  }
  return {
    width: W,
    height: H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { [FLOOR]: "#6e6876", [WALL]: "#463c4c" },
    collision,
    backdropSprite: "prop:church-interior",
    exits: [
      { tileX: KIRI_CHURCH_DOOR.x, tileY: KIRI_CHURCH_DOOR.y, targetMapId: "kiri-town", targetTileX: townDoor.x, targetTileY: townDoor.y + 1 },
    ],
  };
}
