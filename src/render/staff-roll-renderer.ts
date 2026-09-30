import { STAFF_LINE_HEIGHT, STAFF_ROLL_LINES, type StaffRollState } from "../game/title/staff-roll";

/** スタッフロール（夜空の上を、文字が下から上へ流れる）。 */
export function renderStaffRoll(ctx: CanvasRenderingContext2D, state: StaffRollState, screenWidth: number, screenHeight: number): void {
  if (!state.open) {
    return;
  }
  const grad = ctx.createLinearGradient(0, 0, 0, screenHeight);
  grad.addColorStop(0, "#08081c");
  grad.addColorStop(1, "#2a2040");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, screenWidth, screenHeight);
  ctx.textBaseline = "top";
  ctx.textAlign = "center";
  ctx.font = "11px monospace";
  STAFF_ROLL_LINES.forEach((line, i) => {
    const y = screenHeight - state.offset + i * STAFF_LINE_HEIGHT;
    if (y < -STAFF_LINE_HEIGHT || y > screenHeight) {
      return;
    }
    ctx.fillStyle = i === 0 || line.startsWith("【") || line === "登場した人たち" || line === "制作" ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(line, screenWidth / 2, y);
  });
  ctx.textAlign = "left";
  ctx.font = "9px monospace";
  ctx.fillStyle = "rgba(200, 200, 224, 0.7)";
  ctx.fillText("決定でとばす", 6, screenHeight - 12);
}
