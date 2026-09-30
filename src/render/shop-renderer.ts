import { describeBonus } from "../game/economy/shop";
import type { ShopMenuState } from "../game/economy/shop-menu";
import type { EquipmentSlots } from "../game/items/equipment";

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
  ctx.fillStyle = "rgba(16, 20, 40, 0.96)";
  ctx.fillRect(6, 6, screenWidth - 12, screenHeight - 12);
  ctx.strokeStyle = "#f2c14e";
  ctx.strokeRect(6, 6, screenWidth - 12, screenHeight - 12);
  ctx.font = "10px monospace";
  ctx.fillStyle = "#f2c14e";
  ctx.fillText("武具屋（決定で買う／Xで出る）", 14, 12);
  ctx.fillText(`灯貨 ${gold}`, screenWidth - 90, 12);
  state.items.forEach((item, i) => {
    const y = 30 + i * 22;
    const owned = equipment[item.category] === item.id;
    ctx.fillStyle = i === state.cursor ? "#f2c14e" : "#f0f0f0";
    ctx.fillText(`${i === state.cursor ? "▶" : "　"} ${item.name}${owned ? "（装備中）" : ""}`, 14, y);
    ctx.fillStyle = gold >= item.price ? "#c8e8c8" : "#a08080";
    ctx.fillText(`　　${describeBonus(item)}　${item.price}灯貨`, 14, y + 10);
  });
  if (state.message) {
    ctx.fillStyle = "#88ff88";
    ctx.fillText(state.message, 14, screenHeight - 24);
  }
}
