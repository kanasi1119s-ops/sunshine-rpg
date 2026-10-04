import { getPortraitIcon, hasPortraitIcon } from "./portrait-icons";
import { drawSmooth } from "./smooth-draw";
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
/** 会話欄の顔の枠（正方形）。顔アイコンは同じ大きさ（64×64）の絵を、拡大も縮小もせずそのまま描く。 */
export const PORTRAIT_PIXEL_HEIGHT = 64;
export const PORTRAIT_PIXEL_WIDTH = PORTRAIT_PIXEL_HEIGHT;

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
  // 人間がくれた顔アイコン（仲間6人）があれば、それを使う。
  const icon = getPortraitIcon(speaker);
  if (!icon && hasPortraitIcon(speaker)) {
    // 読み込み中は、前の版の顔を出さず、枠だけ出す
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    return true;
  }
  if (icon) {
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    // 画面は論理の2〜4倍の細かさで描いている（`canvas.ts`）ので、大きめの絵（256×256）をなめらかに縮めて描くと、顔がくっきり見える
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(icon, x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    ctx.imageSmoothingEnabled = false;
    return true;
  }
  // 大きな立ち絵（256×256）がある人物は、頭のあたりを切り出して顔グラフィックにする。
  const full = getSpriteCanvas(`char:${speaker}`, SPRITE_DATA);
  if (full) {
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    // 104×104の立ち絵: 頭は中央上（x 32〜72、y 0〜46）。256×256の古い絵は頭の位置が違う
    const crop = full.width === 104 ? [32, 0, 40, 46] : [90, 8, 76, 90];
    drawSmooth(ctx, full, crop[0], crop[1], crop[2], crop[3], x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
    return true;
  }
  const spec = PORTRAITS[speaker];
  if (!spec) {
    return false;
  }
  ctx.fillStyle = "#2a2140";
  ctx.fillRect(x, y, PORTRAIT_PIXEL_WIDTH, PORTRAIT_PIXEL_HEIGHT);
  renderPortrait(ctx, spec, x + (PORTRAIT_PIXEL_WIDTH - PORTRAIT_GRID_WIDTH * cellSize) / 2, y + (PORTRAIT_PIXEL_HEIGHT - PORTRAIT_GRID_HEIGHT * cellSize) / 2, cellSize);
  return true;
}
