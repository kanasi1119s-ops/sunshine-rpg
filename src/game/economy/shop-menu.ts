import type { EquipmentItemData } from "../items/types";
import { shopStock } from "./shop";

/** お店の画面の状態（上下で選び、決定で買う、Xで閉じる）。買う処理そのものは main.ts が `buyItem` で行う。 */
export interface ShopMenuState {
  open: boolean;
  shopId: string;
  items: EquipmentItemData[];
  cursor: number;
  message: string | null;
}

export function createShopMenuState(): ShopMenuState {
  return { open: false, shopId: "", items: [], cursor: 0, message: null };
}

export function openShopMenu(shopId: string): ShopMenuState {
  const items = shopStock(shopId);
  return { open: items.length > 0, shopId, items, cursor: 0, message: null };
}

export function moveShopCursor(state: ShopMenuState, delta: number): ShopMenuState {
  if (!state.open || state.items.length === 0) {
    return state;
  }
  return { ...state, cursor: (state.cursor + delta + state.items.length) % state.items.length, message: null };
}

export function closeShopMenu(state: ShopMenuState): ShopMenuState {
  return { ...state, open: false, message: null };
}

export function withShopMessage(state: ShopMenuState, message: string): ShopMenuState {
  return { ...state, message };
}
