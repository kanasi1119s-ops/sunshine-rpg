import { describeBonus } from "../game/economy/shop";
import type { ShopMenuState } from "../game/economy/shop-menu";
import type { EquipmentSlots } from "../game/items/equipment";
import { WEAPON_LABEL, wielderName } from "../game/items/weapon-types";
import { drawWindow } from "./ui-frame";
import { drawIcon, iconForItem } from "./icon-renderer";
import { getPortraitIcon } from "./portrait-icons";
import type { EquipStatsView } from "./equip-menu-renderer";

/** お店の画面。所持金・品物（値段と効果）・買ったかどうか。 */
export function renderShop(
  ctx: CanvasRenderingContext2D,
  state: ShopMenuState,
  gold: number,
  equipment: EquipmentSlots,
  screenWidth: number,
  screenHeight: number,
): void {
  if (!state.open) {
    return;
  }
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  drawWindow(ctx, 6, 6, screenWidth - 12, screenHeight - 12);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("武具屋（決定で買う／Xで出る）", 14, 12);
  ctx.fillText(`灯貨 ${gold}`, screenWidth - 90, 12);
  state.items.forEach((item, i) => {
    const y = 25 + i * 21;
    const owned = equipment[item.category] === item.id;
    ctx.fillStyle = i === state.cursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${i === state.cursor ? "▶" : "　"}`, 14, y);
    drawIcon(ctx, iconForItem(item.id), 26, y - 2, 16);
    ctx.fillStyle = i === state.cursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${item.name}${owned ? "（装備中）" : ""}`, 46, y);
    ctx.fillStyle = gold >= item.price ? "#c8e8c8" : "#a08080";
    const user = item.category === "weapon" ? `　［${WEAPON_LABEL[item.weaponType ?? "sword"]}：${wielderName(item.weaponType ?? "sword")}］` : "";
    ctx.fillText(`${describeBonus(item)}　${item.price}灯貨${user}`, 46, y + 10);
  });
  if (state.message) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(state.message, 14, screenHeight - 24);
  }
}

export interface ShopWearView {
  itemName: string;
  bonusText: string;
  members: { name: string; currentText: string; before: EquipStatsView; after: EquipStatsView }[];
}

const WEAR_STATS: [keyof EquipStatsView, string][] = [
  ["attack", "こうげき"],
  ["defense", "ぼうぎょ"],
  ["maxHp", "HP"],
  ["speed", "すばやさ"],
];

/** 買った品を、だれにつけるか選ぶ画面（店の画面に重ねる）。仲間みんなと、いちばん下の「つけない」から選ぶ。 */
export function renderShopWear(ctx: CanvasRenderingContext2D, view: ShopWearView, cursor: number, screenWidth: number, screenHeight: number): void {
  drawWindow(ctx, 20, 12, screenWidth - 40, screenHeight - 24);
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText(`${view.itemName}（${view.bonusText}）を だれにつける？　Xで つけない`, 30, 18);
  view.members.forEach((m, i) => {
    const y = 34 + i * 26;
    const selected = i === cursor;
    const icon = getPortraitIcon(m.name, true);
    ctx.fillStyle = "#2a2140";
    ctx.fillRect(30, y - 1, 22, 22);
    if (icon) {
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";
      ctx.drawImage(icon, 30, y - 1, 22, 22);
      ctx.imageSmoothingEnabled = false;
    }
    ctx.strokeStyle = selected ? "#f2c14e" : "#6a5a3a";
    ctx.strokeRect(29.5, y - 1.5, 23, 23);
    ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${selected ? "▶" : "　"}${m.name}　いま: ${m.currentText}`, 58, y);
    const changes = WEAR_STATS.filter(([k]) => m.after[k] !== m.before[k]).map(([k, name]) => `${name}${m.before[k]}→${m.after[k]}`);
    ctx.fillStyle = changes.length > 0 ? "#88ff88" : "#a8a8c0";
    ctx.fillText(changes.length > 0 ? `　${changes.join("　")}` : "　かわらない", 58, y + 11);
  });
  const y = 34 + view.members.length * 26;
  const selected = cursor === view.members.length;
  ctx.fillStyle = selected ? "#f2c14e" : "#f0f0f0";
  ctx.fillText(`${selected ? "▶" : "　"}つけない（あとで「そうび」でつけられる）`, 30, y + 4);
}
