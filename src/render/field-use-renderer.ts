import type { FieldUseState } from "../game/menu/field-use";
import { drawWindow } from "./ui-frame";

export interface FieldUseMemberView {
  name: string;
  hp: number;
  maxHp: number;
  mp: number;
  maxMp: number;
}

/** フィールドの「どうぐ」「まほう」の画面。左に一覧、右に仲間のHP・MP。 */
export function renderFieldUse(ctx: CanvasRenderingContext2D, state: FieldUseState, members: FieldUseMemberView[], screenWidth: number, screenHeight: number): void {
  if (!state.open) return;
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  drawWindow(ctx, 4, 4, screenWidth - 8, screenHeight - 8);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText(state.mode === "items" ? "どうぐ（決定でつかう／Xでもどる）" : "まほう（決定でつかう／Xでもどる）", 12, 10);
  const listW = Math.floor(screenWidth * 0.52);
  const perPage = 9;
  const page = Math.floor(state.cursor / perPage);
  state.options.slice(page * perPage, (page + 1) * perPage).forEach((option, i) => {
    const index = page * perPage + i;
    const selected = index === state.cursor;
    const y = 26 + i * 18;
    ctx.fillStyle = selected ? (state.stage === "pick" ? "#f2c14e" : "#c8a850") : "#f0f0f0";
    ctx.fillText(`${selected ? "▶" : "　"}${option.label}`, 12, y);
    ctx.fillStyle = "#a8a8c8";
    ctx.fillText(`　　${option.note}`, 12, y + 9);
  });
  if (state.options.length > perPage) {
    ctx.fillStyle = "#a8a8c8";
    ctx.fillText(`${page + 1}/${Math.ceil(state.options.length / perPage)}`, listW - 30, 10);
  }
  // 仲間のHP・MP
  members.forEach((m, i) => {
    const y = 24 + i * 28;
    const selected = state.stage === "target" && i === state.targetCursor;
    ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${selected ? "▶" : "　"}${m.name}`, listW + 4, y);
    ctx.fillStyle = m.hp <= m.maxHp * 0.25 ? "#ff8888" : "#c8e8c8";
    ctx.fillText(`　HP ${m.hp}/${m.maxHp}`, listW + 4, y + 9);
    ctx.fillStyle = "#a8c8ff";
    ctx.fillText(`　MP ${m.mp}/${m.maxMp}`, listW + 4, y + 17);
  });
  if (state.message) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(state.message, 12, screenHeight - 20);
  } else if (state.stage === "target") {
    ctx.fillStyle = "#a8a8c8";
    ctx.fillText("だれに つかう？", 12, screenHeight - 20);
  }
}
