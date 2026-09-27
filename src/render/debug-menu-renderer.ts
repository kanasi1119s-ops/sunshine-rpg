import type { DebugMenuState } from "../game/debug/debug-menu";

const LINE_HEIGHT = 12;
const PADDING = 6;

export interface DebugMenuRow {
  label: () => string;
}

export function renderDebugMenu(
  ctx: CanvasRenderingContext2D,
  state: DebugMenuState,
  rows: DebugMenuRow[],
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }

  const boxWidth = Math.min(screenWidth - 16, 260);
  const boxHeight = rows.length * LINE_HEIGHT + PADDING * 2 + LINE_HEIGHT;
  const boxX = (screenWidth - boxWidth) / 2;
  const boxY = (screenHeight - boxHeight) / 2;

  ctx.fillStyle = "rgba(10, 20, 10, 0.95)";
  ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
  ctx.strokeStyle = "#88ff88";
  ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);

  ctx.font = "10px monospace";
  ctx.textBaseline = "top";
  ctx.fillStyle = "#88ff88";
  ctx.fillText("デバッグメニュー（`で閉じる）", boxX + PADDING, boxY + PADDING);

  rows.forEach((row, index) => {
    const y = boxY + PADDING + LINE_HEIGHT * (index + 1);
    const cursor = index === state.cursor ? "▶" : " ";
    ctx.fillStyle = index === state.cursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${cursor} ${row.label()}`, boxX + PADDING, y);
  });
}
