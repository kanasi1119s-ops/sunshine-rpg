export interface InventoryEntry {
  itemId: string;
  quantity: number;
}

export type Inventory = InventoryEntry[];

export function createInventory(): Inventory {
  return [];
}

export function getQuantity(inventory: Inventory, itemId: string): number {
  return inventory.find((entry) => entry.itemId === itemId)?.quantity ?? 0;
}

export function addItem(inventory: Inventory, itemId: string, quantity = 1): Inventory {
  const existing = inventory.find((entry) => entry.itemId === itemId);
  if (!existing) {
    return [...inventory, { itemId, quantity }];
  }
  return inventory.map((entry) =>
    entry.itemId === itemId ? { ...entry, quantity: entry.quantity + quantity } : entry,
  );
}

/** 所持数が足りない場合は何もせず、そのままの所持品を返す。 */
export function removeItem(inventory: Inventory, itemId: string, quantity = 1): Inventory {
  const current = getQuantity(inventory, itemId);
  if (current < quantity) {
    return inventory;
  }
  const remaining = current - quantity;
  if (remaining === 0) {
    return inventory.filter((entry) => entry.itemId !== itemId);
  }
  return inventory.map((entry) =>
    entry.itemId === itemId ? { ...entry, quantity: remaining } : entry,
  );
}
