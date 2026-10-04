import { CONTROLS_ROW_COUNT, DIFFICULTY_ROW, SPEED_ROW, type ControlsMenuState } from "../game/menu/controls-menu";
import { CONTROL_ACTIONS, describeBinding, type KeyBindings } from "../input/key-bindings";
import { MOVE_SPEEDS } from "../game/move-speed";
import { DIFFICULTIES, difficultyLabel, type Difficulty } from "../game/difficulty";
import { drawWindow } from "./ui-frame";

/** そうさ設定の画面。動作ごとのキー、もとにもどす、とじる。下に、コントローラーの配置。 */
export function renderControlsMenu(ctx: CanvasRenderingContext2D, state: ControlsMenuState, bindings: KeyBindings, moveSpeed: number, difficulty: Difficulty, screenWidth: number, screenHeight: number): void {
  if (!state.open) return;
  drawWindow(ctx, 6, 6, screenWidth - 12, screenHeight - 12);
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("そうさ設定（決定でキーをかえる／左右で速さ・モード／Xでとじる）", 14, 12);
  for (let i = 0; i < CONTROLS_ROW_COUNT; i++) {
    const y = 26 + i * 13;
    const selected = i === state.cursor;
    ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
    const cursor = selected ? "▶" : "　";
    if (i < CONTROL_ACTIONS.length) {
      const action = CONTROL_ACTIONS[i];
      const value = selected && state.capturing ? "新しいキーを おして（Escでやめる）" : describeBinding(bindings, action.id);
      ctx.fillText(`${cursor}${action.label}`, 14, y);
      ctx.fillStyle = selected && state.capturing ? "#88ff88" : selected ? "#f2c14e" : "#c8c8e0";
      ctx.fillText(value, 150, y);
    } else if (i === SPEED_ROW) {
      ctx.fillText(`${cursor}あるく速さ`, 14, y);
      ctx.fillStyle = selected ? "#f2c14e" : "#c8c8e0";
      ctx.fillText(`◀ ${MOVE_SPEEDS[moveSpeed].label} ▶`, 150, y);
    } else if (i === DIFFICULTY_ROW) {
      ctx.fillText(`${cursor}モード`, 14, y);
      ctx.fillStyle = selected ? "#f2c14e" : "#c8c8e0";
      ctx.fillText(`◀ ${difficultyLabel(difficulty)} ▶　${DIFFICULTIES.find((d) => d.id === difficulty)?.hint ?? ""}`, 150, y);
    } else if (i === SPEED_ROW + 2) {
      ctx.fillText(`${cursor}もとにもどす`, 14, y);
    } else {
      ctx.fillText(`${cursor}とじる`, 14, y);
    }
  }
  if (state.message) {
    ctx.fillStyle = "#88ff88";
    ctx.textAlign = "right";
    ctx.fillText(state.message, screenWidth - 14, 12);
    ctx.textAlign = "left";
  }
  ctx.fillStyle = "#a8a8c0";
  ctx.fillText("コントローラー: 十字キー・左スティック=うごく　A=決定　B=もどる", 14, screenHeight - 24);
  ctx.fillText("　　　　　　　 X=ジョブ　Y=世界地図　スタート=メニュー", 14, screenHeight - 12);
}
