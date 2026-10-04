import { describe, expect, it } from "vitest";
import { addItem } from "./inventory";
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
    party = equipTo(party, "reto", dagger, inv) as typeof party;
    expect(party).toEqual({ hero: { weapon: "sword" }, reto: { weapon: "dagger" } });
    expect(wearerOf(party, "dagger")).toBe("reto");
  });

  it("ほかの人がつけている品を選ぶと、その人からはずれる", () => {
    const party = equipTo({ hero: { weapon: "sword" } }, "reto", sword, ensureOwned([], ["sword"]));
    expect(party.hero.weapon).toBeUndefined();
    expect(party.reto.weapon).toBe("sword");
  });

  it("同じ品を2個持っていれば、2人がつけられる（あまりがあるときは、取りかえない）", () => {
    const inv = addItem(ensureOwned([], ["sword"]), "sword", 1); // 2個
    let party: Record<string, Record<string, string>> = { hero: { weapon: "sword" } };
    expect(candidatesFor("reto", "weapon", party, inv, items).find((c) => c.item.id === "sword")?.takenBy).toBeUndefined();
    party = equipTo(party, "reto", sword, inv);
    expect(party.hero.weapon).toBe("sword");
    expect(party.reto.weapon).toBe("sword");
    // 3人目は、あまりがないので、取りかえになる
    const third = equipTo(party, "mina", sword, inv);
    expect(Object.values(third).filter((s) => s.weapon === "sword")).toHaveLength(2);
    expect(third.mina.weapon).toBe("sword");
    expect(candidatesFor("mina", "weapon", { ...party }, inv, items).find((c) => c.item.id === "sword")?.takenBy).toBe("hero");
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
