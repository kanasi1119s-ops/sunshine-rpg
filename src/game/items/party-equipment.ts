import type { EquipmentSlots } from "./equipment";
import { equip, unequip } from "./equipment";
import { addItem, getQuantity, type Inventory } from "./inventory";
import type { EquipmentCategory, EquipmentItemData, ItemData } from "./types";

/**
 * 仲間みんなの装備。持ち物（`Inventory`）に入っている装備を、ユーリも仲間も、同じ持ち物から選んで身につける。
 * 1つの品を身につけられるのは1人だけ。ほかの人がつけている品を選ぶと、その人からはずれて、選んだ人がつける。
 * 主人公のキャラクターIDは "hero"。
 */
export type PartyEquipment = Record<string, EquipmentSlots>;

export const EQUIPMENT_CATEGORIES: { id: EquipmentCategory; label: string }[] = [
  { id: "weapon", label: "ぶき" },
  { id: "armor", label: "ぼうぐ" },
  { id: "accessory", label: "かざり" },
];

function isEquipment(item: ItemData | undefined): item is EquipmentItemData {
  return !!item && item.category !== "consumable";
}

/** 持ち物に入っている装備（持っている品のID）。 */
export function ownedEquipmentIds(inventory: Inventory, itemsById: Record<string, ItemData>): string[] {
  return inventory.filter((e) => e.quantity > 0 && isEquipment(itemsById[e.itemId])).map((e) => e.itemId);
}

/** 持ち物に、まだ入っていない装備を足す（買った・宝箱で見つけた・最初から持っている装備を、持ち物にそろえるときに使う）。 */
export function ensureOwned(inventory: Inventory, itemIds: Iterable<string | undefined>): Inventory {
  let next = inventory;
  for (const id of itemIds) {
    if (id && getQuantity(next, id) === 0) {
      next = addItem(next, id, 1);
    }
  }
  return next;
}

/** いま、その品を身につけている人（いなければ undefined）。 */
export function wearerOf(party: PartyEquipment, itemId: string): string | undefined {
  return Object.entries(party).find(([, slots]) => Object.values(slots).includes(itemId))?.[0];
}

export interface EquipCandidate {
  item: EquipmentItemData;
  /** いま別の人がつけているとき、その人のID。 */
  takenBy?: string;
}

/** その人のその部位に、つけられる品の一覧（持っている同じ部位の品。ほかの人がつけているものも出す）。 */
export function candidatesFor(
  owner: string,
  category: EquipmentCategory,
  party: PartyEquipment,
  inventory: Inventory,
  itemsById: Record<string, ItemData>,
): EquipCandidate[] {
  const result: EquipCandidate[] = [];
  for (const id of ownedEquipmentIds(inventory, itemsById)) {
    const item = itemsById[id];
    if (!isEquipment(item) || item.category !== category) continue;
    const wearer = wearerOf(party, id);
    if (wearer === owner) continue; // もうつけている
    result.push({ item, takenBy: wearer });
  }
  return result;
}

/** その人にその品をつける。別の人がつけていたら、その人からははずれる。 */
export function equipTo(party: PartyEquipment, owner: string, item: EquipmentItemData): PartyEquipment {
  const next: PartyEquipment = {};
  for (const [id, slots] of Object.entries(party)) {
    next[id] = Object.values(slots).includes(item.id) ? unequip(slots, item.category) : slots;
  }
  next[owner] = equip(next[owner] ?? {}, item);
  return next;
}

/** その人のその部位を、はずす。 */
export function unequipFrom(party: PartyEquipment, owner: string, category: EquipmentCategory): PartyEquipment {
  return { ...party, [owner]: unequip(party[owner] ?? {}, category) };
}
