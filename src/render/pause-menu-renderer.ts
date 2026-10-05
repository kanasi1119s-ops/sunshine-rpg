import { PAUSE_ITEMS, type PauseMenuState } from "../game/menu/pause-menu";
import { drawWindow } from "./ui-frame";
import { getPortraitIcon } from "./portrait-icons";

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
  luck: number;
  expToNext: number;
}

export interface ItemsView {
  /** だいじなもの（名前と説明）。 */
  keyItems: { name: string; note: string }[];
  /** 持っている装備（名前・数・効果・つけている人）。 */
  equipment: { name: string; count: number; bonus: string; wearers: string }[];
}

/** 「もちもの」の画面。だいじなものと、持っている装備の一覧（上下でスクロール）。 */
export function renderItemsScreen(ctx: CanvasRenderingContext2D, view: ItemsView, scroll: number, gold: number, screenWidth: number, screenHeight: number): void {
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  drawWindow(ctx, 4, 4, screenWidth - 8, screenHeight - 8);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("もちもの（上下でスクロール／決定またはXでもどる）", 12, 10);
  ctx.fillText(`灯貨 ${gold}`, screenWidth - 90, 10);
  type Row = { text: string; color: string; sub?: string };
  const rows: Row[] = [{ text: "【だいじなもの】", color: "#88c8ff" }];
  for (const k of view.keyItems) rows.push({ text: `　${k.name}`, color: "#f0f0f0", sub: `　　${k.note}` });
  rows.push({ text: "", color: "#fff" });
  rows.push({ text: "【そうび】", color: "#88c8ff" });
  if (view.equipment.length === 0) rows.push({ text: "　（まだ持っていない）", color: "#a0a0b8" });
  for (const e of view.equipment) rows.push({ text: `　${e.name}${e.count > 1 ? ` ×${e.count}` : ""}　${e.bonus}`, color: "#f0f0f0", sub: e.wearers ? `　　つけている人: ${e.wearers}` : "　　（だれもつけていない）" });
  const rowH = 11;
  const lines: { text: string; color: string }[] = [];
  for (const r of rows) {
    lines.push({ text: r.text, color: r.color });
    if (r.sub) lines.push({ text: r.sub, color: "#a8a8c8" });
  }
  const visible = Math.floor((screenHeight - 40) / rowH);
  const maxScroll = Math.max(0, lines.length - visible);
  const start = Math.max(0, Math.min(maxScroll, scroll));
  lines.slice(start, start + visible).forEach((l, i) => {
    ctx.fillStyle = l.color;
    ctx.fillText(l.text, 12, 26 + i * rowH);
  });
  if (start > 0) {
    ctx.fillStyle = "#f2c14e";
    ctx.fillText("▲", screenWidth - 18, 24);
  }
  if (start < maxScroll) {
    ctx.fillStyle = "#f2c14e";
    ctx.fillText("▼", screenWidth - 18, screenHeight - 20);
  }
}

/** ゲーム中のメニューと、つよさ画面。 */
export function renderPauseMenu(
  ctx: CanvasRenderingContext2D,
  state: PauseMenuState,
  rows: StatusRow[],
  message: string | null,
  gold: number,
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }
  if (state.screen === "items") {
    return; // 「もちもの」は renderItemsScreen で描く
  }
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  if (state.screen === "main") {
    const boxW = 150;
    const boxH = PAUSE_ITEMS.length * 16 + 16;
    const x = screenWidth - boxW - 8;
    const y = 18;
    drawWindow(ctx, x, y, boxW, boxH);
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
  drawWindow(ctx, 4, 4, screenWidth - 8, screenHeight - 8);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("つよさ（決定またはXでもどる）", 12, 10);
  ctx.fillText(`灯貨 ${gold}`, screenWidth - 90, 10);
  rows.forEach((row, i) => {
    const y = 26 + i * 30;
    // 顔アイコン（28×28、拡大も縮小もせずそのまま）。絵のない人は、枠だけ
    const icon = getPortraitIcon(row.name, true);
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(12, y - 2, 28, 28);
    if (icon) {
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";
      ctx.drawImage(icon, 12, y - 2, 28, 28);
      ctx.imageSmoothingEnabled = false;
    }
    ctx.strokeStyle = "#c89a48";
    ctx.strokeRect(11.5, y - 2.5, 29, 29);
    ctx.fillStyle = "#f0f0f0";
    ctx.fillText(`${row.name}　Lv${row.level}　HP ${row.hp}/${row.maxHp}　MP ${row.mp}/${row.maxMp}`, 48, y);
    ctx.fillStyle = "#c8c8e0";
    ctx.fillText(`こうげき${row.attack}　ぼうぎょ${row.defense}　すばやさ${row.speed}　うん${row.luck}　つぎのLvまで${row.expToNext}`, 48, y + 12);
  });
}
