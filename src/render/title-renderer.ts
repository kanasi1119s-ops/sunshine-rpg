import { CREDIT_LINES, HELP_LINES } from "../game/title/title-text";
import { titleItemsFor, type TitleState } from "../game/title/title-menu";

/** タイトル画面（メニュー／あそびかた／クレジット）。 */
export function renderTitle(ctx: CanvasRenderingContext2D, state: TitleState, gameTitle: string, screenWidth: number, screenHeight: number): void {
  if (!state.open) {
    return;
  }
  // 夜空のようなグラデーションと、ちいさな灯り。
  const grad = ctx.createLinearGradient(0, 0, 0, screenHeight);
  grad.addColorStop(0, "#0c1030");
  grad.addColorStop(1, "#3a2a50");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  ctx.fillStyle = "rgba(242, 193, 78, 0.85)";
  for (const [x, y] of [[40, 30], [120, 60], [300, 40], [350, 90], [70, 110], [230, 20], [180, 100]]) {
    ctx.fillRect(x, y, 2, 2);
  }
  ctx.textBaseline = "top";

  if (state.screen === "menu") {
    ctx.fillStyle = "#f2c14e";
    ctx.font = "bold 20px monospace";
    ctx.textAlign = "center";
    ctx.fillText(gameTitle, screenWidth / 2, screenHeight * 0.2);
    ctx.font = "10px monospace";
    ctx.fillStyle = "#c8c8e0";
    ctx.fillText("サンシャインソフトウェア", screenWidth / 2, screenHeight * 0.2 + 30);
    ctx.font = "12px monospace";
    titleItemsFor(state.hasSave).forEach((item, i) => {
      const selected = i === state.cursor;
      ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
      ctx.fillText(`${selected ? "▶ " : "　"}${item.label}`, screenWidth / 2, screenHeight * 0.52 + i * 20);
    });
    ctx.font = "9px monospace";
    ctx.fillStyle = "#9a9ab8";
    ctx.fillText("やじるしで えらぶ ／ 決定で すすむ", screenWidth / 2, screenHeight - 16);
    ctx.textAlign = "left";
    return;
  }

  const lines = state.screen === "help" ? HELP_LINES : CREDIT_LINES;
  ctx.textAlign = "left";
  ctx.font = "10px monospace";
  const startY = 8;
  lines.forEach((line, i) => {
    ctx.fillStyle = i === 0 ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(line, 14, startY + i * 11);
  });
  ctx.fillStyle = "#9a9ab8";
  ctx.fillText("決定（またはX）でもどる", 14, screenHeight - 14);
}
