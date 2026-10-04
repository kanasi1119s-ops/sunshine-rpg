import { describe, expect, it } from "vitest";
import { candidatesFor, ensureOwned, equipTo, ownedEquipmentIds, unequipFrom, wearerOf } from "./party-equipment";
import type { EquipmentItemData, ItemData } from "./types";

const sword: EquipmentItemData = { id: "sword", name: "剣", category: "weapon", price: 0, statBonus: { attack: 5 } };
const dagger: EquipmentItemData = { id: "dagger", name: "短剣", category: "weapon", price: 0, statBonus: { attack: 3 } };
const cloak: EquipmentItemData = { id: "cloak", name: "外套", category: "armor", price: 0, statBonus: { defense: 3 } };
const herb: ItemData = { id: "herb", name: "やくそう", category: "consumable", price: 1, healAmount: 10 };
const items: Record<string, ItemData> = { sword, dagger, cloak, herb };

describe("仲間みんなの装備", () => {
  it("持ち物の中の装備だけを数える（回復の品は入らない）", () => {
    const inv = ensureOwned([{ itemId: "herb", quantity: 2 }], ["sword", "cloak"]);
    expect(ownedEquipmentIds(inv, items).sort()).toEqual(["cloak", "sword"]);
  });

  it("すでに持っている品は、ふやさない", () => {
    const inv = ensureOwned(ensureOwned([], ["sword"]), ["sword", undefined]);
    expect(inv).toEqual([{ itemId: "sword", quantity: 1 }]);
  });

  it("仲間も、持ち物から装備できる", () => {
    const inv = ensureOwned([], ["sword", "dagger"]);
    let party = { hero: { weapon: "sword" } };
    expect(candidatesFor("reto", "weapon", party, inv, items).map((c) => c.item.id).sort()).toEqual(["dagger", "sword"]);
    party = equipTo(party, "reto", dagger) as typeof party;
    expect(party).toEqual({ hero: { weapon: "sword" }, reto: { weapon: "dagger" } });
    expect(wearerOf(party, "dagger")).toBe("reto");
  });

  it("ほかの人がつけている品を選ぶと、その人からはずれる", () => {
    const party = equipTo({ hero: { weapon: "sword" } }, "reto", sword);
    expect(party.hero.weapon).toBeUndefined();
    expect(party.reto.weapon).toBe("sword");
  });

  it("はずすと、持ち物には残る", () => {
    const inv = ensureOwned([], ["sword"]);
    const party = unequipFrom({ hero: { weapon: "sword" } }, "hero", "weapon");
    expect(party.hero.weapon).toBeUndefined();
    expect(ownedEquipmentIds(inv, items)).toEqual(["sword"]);
    expect(candidatesFor("hero", "weapon", party, inv, items).map((c) => c.item.id)).toEqual(["sword"]);
  });

  it("自分がつけている品は、候補に出ない", () => {
    const inv = ensureOwned([], ["sword"]);
    expect(candidatesFor("hero", "weapon", { hero: { weapon: "sword" } }, inv, items)).toEqual([]);
  });
});
