import type { SlotMenuState } from "../game/menu/slot-menu";
import { drawWindow } from "./ui-frame";

/** セーブ・ロードの場所えらびの画面。 */
export function renderSlotMenu(ctx: CanvasRenderingContext2D, state: SlotMenuState, screenWidth: number, screenHeight: number): void {
  if (!state.open) return;
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  drawWindow(ctx, 6, 6, screenWidth - 12, screenHeight - 12);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText(state.mode === "save" ? "どこにセーブする？（決定／Xでもどる）" : "どのセーブから はじめる？（決定／Xでもどる）", 14, 12);
  state.rows.forEach((row, i) => {
    const y = 30 + i * 24;
    const selected = i === state.cursor;
    const disabled = state.mode === "load" && row.empty;
    ctx.fillStyle = selected ? "#f2c14e" : disabled ? "#80809a" : "#f0f0f0";
    ctx.fillText(`${selected ? "▶" : "　"}${row.label}`, 14, y);
    ctx.fillStyle = row.empty ? "#80809a" : "#c8c8e0";
    ctx.fillText(row.empty ? "　　（からっぽ）" : `　　${row.text ?? ""}`, 14, y + 11);
  });
  const fy = 30 + state.rows.length * 24;
  const fileSelected = state.cursor === state.rows.length;
  ctx.fillStyle = fileSelected ? "#f2c14e" : "#9ad0ff";
  ctx.fillText(`${fileSelected ? "▶" : "　"}${state.mode === "save" ? "バックアップを書き出す（ファイル・テキスト）" : "バックアップから読み込む（ファイル・テキスト）"}`, 14, fy);
  if (state.message) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(state.message, 14, screenHeight - 22);
  }
}
