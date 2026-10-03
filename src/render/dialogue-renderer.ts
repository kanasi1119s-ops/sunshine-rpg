import type { DialogueRenderState } from "../game/dialogue/dialogue-controller";
import { wrapText } from "./text-wrap";
import { PORTRAIT_PIXEL_WIDTH, renderPortraitByName } from "./portrait-renderer";
import { drawWindow } from "./ui-frame";

const LINE_HEIGHT = 12;
const PADDING = 6;
const PORTRAIT_GAP = 4;

export function renderDialogue(
  ctx: CanvasRenderingContext2D,
  state: DialogueRenderState,
  screenWidth: number,
  screenHeight: number,
): void {
  const boxX = 8;
  const boxHeight = 56;
  const boxY = screenHeight - boxHeight - 8;
  const boxWidth = screenWidth - 16;

  drawWindow(ctx, boxX, boxY, boxWidth, boxHeight);

  ctx.font = "10px monospace";
  ctx.textBaseline = "top";
  ctx.fillStyle = "#f0f0f0";

  if (state.kind === "message") {
    const hasPortrait = state.speaker !== undefined && renderPortraitByName(ctx, state.speaker, boxX + PADDING, boxY + PADDING);
    if (hasPortrait) {
      ctx.strokeStyle = "#c89a48";
      ctx.strokeRect(boxX + PADDING - 0.5, boxY + PADDING - 0.5, PORTRAIT_PIXEL_WIDTH + 1, 14 * 3 + 1);
    }
    const textIndent = hasPortrait ? PORTRAIT_PIXEL_WIDTH + PORTRAIT_GAP : 0;
    const textX = boxX + PADDING + textIndent;

    let textY = boxY + PADDING;
    if (state.speaker) {
      ctx.fillStyle = "#f2c14e";
      ctx.fillText(state.speaker, textX, textY);
      textY += LINE_HEIGHT;
      ctx.fillStyle = "#f0f0f0";
    }
    const lines = wrapText(state.visibleText, boxWidth - PADDING * 2 - textIndent, (segment) =>
      ctx.measureText(segment).width,
    );
    lines.forEach((line, index) => {
      ctx.fillText(line, textX, textY + index * LINE_HEIGHT);
    });
    if (state.fullyShown) {
      ctx.fillText("▼", boxX + boxWidth - PADDING - 8, boxY + boxHeight - LINE_HEIGHT - 2);
    }
    return;
  }

  ctx.fillText(state.text, boxX + PADDING, boxY + PADDING);
  state.labels.forEach((label, index) => {
    const y = boxY + PADDING + LINE_HEIGHT * (index + 1) + 4;
    const cursor = index === state.selectedIndex ? "▶" : " ";
    ctx.fillText(`${cursor} ${label}`, boxX + PADDING + 4, y);
  });
}
