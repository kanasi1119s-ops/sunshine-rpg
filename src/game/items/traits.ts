import type { Combatant } from "../battle/types";
import { luckOf } from "../battle/luck";
import type { EquipmentSlots } from "./equipment";
import type { ItemData } from "./types";

/** 身につけている装備の特殊効果を、戦闘の本人に足す。 */
export function applyTraits(combatant: Combatant, slots: EquipmentSlots, itemsById: Record<string, ItemData>): Combatant {
  const next: Combatant = { ...combatant };
  for (const id of Object.values(slots)) {
    const item = id ? itemsById[id] : undefined;
    if (!item || item.category === "consumable") continue;
    for (const trait of item.traits ?? []) {
      switch (trait.kind) {
        case "luck": next.luck = luckOf(next) + trait.value; break;
        case "crit": next.critBonus = (next.critBonus ?? 0) + trait.value / 100; break;
        case "evade": next.evade = (next.evade ?? 0) + trait.value / 100; break;
        case "guard": next.guards = [...new Set([...(next.guards ?? []), trait.status])]; break;
        case "regenHp": next.regenHp = (next.regenHp ?? 0) + trait.percent / 100; break;
        case "regenMp": next.regenMp = (next.regenMp ?? 0) + trait.value; break;
        case "multi": next.multiBonus = (next.multiBonus ?? 0) + trait.value; break;
      }
    }
  }
  return next;
}
