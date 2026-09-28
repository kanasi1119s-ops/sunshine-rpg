import {
  buildPortraitRows,
  colorForCell,
  PORTRAIT_GRID_HEIGHT,
  PORTRAIT_GRID_WIDTH,
  PORTRAITS,
  type PortraitSpec,
} from "../game/portrait/portraits";

/** 1ドットあたりの画面上のピクセル数。 */
export const PORTRAIT_CELL_SIZE = 3;
export const PORTRAIT_PIXEL_WIDTH = PORTRAIT_GRID_WIDTH * PORTRAIT_CELL_SIZE;
export const PORTRAIT_PIXEL_HEIGHT = PORTRAIT_GRID_HEIGHT * PORTRAIT_CELL_SIZE;

export function renderPortrait(
  ctx: CanvasRenderingContext2D,
  spec: PortraitSpec,
  x: number,
  y: number,
): void {
  const rows = buildPortraitRows(spec);
  for (let row = 0; row < rows.length; row++) {
    for (let col = 0; col < rows[row].length; col++) {
      const color = colorForCell(spec, rows[row][col]);
      if (!color) {
        continue;
      }
      ctx.fillStyle = color;
      ctx.fillRect(x + col * PORTRAIT_CELL_SIZE, y + row * PORTRAIT_CELL_SIZE, PORTRAIT_CELL_SIZE, PORTRAIT_CELL_SIZE);
    }
  }
}

/** 話者名から顔グラフィックを探して描画する。登録が無ければ何もせず false を返す。 */
export function renderPortraitByName(
  ctx: CanvasRenderingContext2D,
  speaker: string,
  x: number,
  y: number,
): boolean {
  const spec = PORTRAITS[speaker];
  if (!spec) {
    return false;
  }
  renderPortrait(ctx, spec, x, y);
  return true;
}
