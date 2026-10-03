import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import {
  buildShadedCells,
  PORTRAIT_GRID_HEIGHT,
  PORTRAIT_GRID_WIDTH,
  PORTRAITS,
  type PortraitSpec,
} from "../game/portrait/portraits";

/** 会話欄で使う、1ドットあたりの画面上のピクセル数。 */
export const PORTRAIT_CELL_SIZE = 3;
export const PORTRAIT_PIXEL_WIDTH = PORTRAIT_GRID_WIDTH * PORTRAIT_CELL_SIZE;
export const PORTRAIT_PIXEL_HEIGHT = PORTRAIT_GRID_HEIGHT * PORTRAIT_CELL_SIZE;

/**
 * マップ上のプレイヤー・NPC用に、1ドット＝1画面ピクセルで描く等倍サイズ。
 * グリッドの幅・高さ（12×14）が、そのままプレイヤーの当たり判定サイズ
 * （`createPlayer`の width=12, height=14）に一致するよう設計してある。
 */
export const OVERWORLD_CELL_SIZE = 1;

export function renderPortrait(
  ctx: CanvasRenderingContext2D,
  spec: PortraitSpec,
  x: number,
  y: number,
  cellSize: number = PORTRAIT_CELL_SIZE,
): void {
  for (const cell of buildShadedCells(spec)) {
    ctx.fillStyle = cell.color;
    ctx.fillRect(x + cell.col * cellSize, y + cell.row * cellSize, cellSize, cellSize);
  }
}

/** 話者名から顔グラフィックを探して描画する。登録が無ければ何もせず false を返す。 */
export function renderPortraitByName(
  ctx: CanvasRenderingContext2D,
  speaker: string,
  x: number,
  y: number,
  cellSize: number = PORTRAIT_CELL_SIZE,
): boolean {
  // 大きな立ち絵（256×256）がある人物は、頭のあたりを切り出して顔グラフィックにする。
  const full = getSpriteCanvas(`char:${speaker}`, SPRITE_DATA);
  if (full) {
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    // 104×104の立ち絵: 頭は中央上（x 32〜72、y 0〜46）。256×256の古い絵は頭の位置が違う
    const crop = full.width === 104 ? [32, 0, 40, 46] : [90, 8, 76, 90];
    ctx.drawImage(full, crop[0], crop[1], crop[2], crop[3], x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    return true;
  }
  const spec = PORTRAITS[speaker];
  if (!spec) {
    return false;
  }
  renderPortrait(ctx, spec, x, y, cellSize);
  return true;
}
