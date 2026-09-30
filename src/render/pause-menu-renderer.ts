import { PAUSE_ITEMS, type PauseMenuState } from "../game/menu/pause-menu";

export interface StatusRow {
  name: string;
  level: number;
  hp: number;
  maxHp: number;
  mp: number;
  maxMp: number;
  attack: number;
  defense: number;
  speed: number;
  expToNext: number;
}

/** ゲーム中のメニューと、つよさ画面。 */
export function renderPauseMenu(
  ctx: CanvasRenderingContext2D,
  state: PauseMenuState,
  rows: StatusRow[],
  message: string | null,
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  if (state.screen === "main") {
    const boxW = 150;
    const boxH = PAUSE_ITEMS.length * 16 + 16;
    const x = screenWidth - boxW - 8;
    const y = 18;
    ctx.fillStyle = "rgba(16, 16, 40, 0.95)";
    ctx.fillRect(x, y, boxW, boxH);
    ctx.strokeStyle = "#f2c14e";
    ctx.strokeRect(x, y, boxW, boxH);
    ctx.font = "11px monospace";
    PAUSE_ITEMS.forEach((item, i) => {
      ctx.fillStyle = i === state.cursor ? "#f2c14e" : "#f0f0f0";
      ctx.fillText(`${i === state.cursor ? "▶" : "　"} ${item.label}`, x + 8, y + 8 + i * 16);
    });
    if (message) {
      ctx.fillStyle = "#88ff88";
      ctx.font = "10px monospace";
      ctx.fillText(message, x, y + boxH + 4);
    }
    return;
  }
  ctx.fillStyle = "rgba(16, 16, 40, 0.96)";
  ctx.fillRect(4, 4, screenWidth - 8, screenHeight - 8);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(4, 4, screenWidth - 8, screenHeight - 8);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("つよさ（決定またはXでもどる）", 12, 10);
  rows.forEach((row, i) => {
    const y = 26 + i * 30;
    ctx.fillStyle = "#f0f0f0";
    ctx.fillText(`${row.name}　Lv${row.level}　HP ${row.hp}/${row.maxHp}　MP ${row.mp}/${row.maxMp}`, 12, y);
    ctx.fillStyle = "#c8c8e0";
    ctx.fillText(`　こうげき${row.attack}　ぼうぎょ${row.defense}　すばやさ${row.speed}　つぎのLvまで${row.expToNext}`, 12, y + 11);
  });
}
