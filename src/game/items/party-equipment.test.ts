import { describe, expect, it } from "vitest";
import { addItem } from "./inventory";
import { candidatesFor, ensureOwned, equipTo, ownedEquipmentIds, sanitizeParty, unequipFrom, wearerOf } from "./party-equipment";
import type { EquipmentItemData, ItemData } from "./types";

const sword: EquipmentItemData = { id: "sword", name: "剣", category: "weapon", price: 0, statBonus: { attack: 5 } };
const dagger: EquipmentItemData = { id: "dagger", name: "短剣", category: "weapon", price: 0, statBonus: { attack: 3 }, weaponType: "dagger" };
const staff: EquipmentItemData = { id: "staff", name: "杖", category: "weapon", price: 0, statBonus: { attack: 2 }, weaponType: "staff" };
const cloak: EquipmentItemData = { id: "cloak", name: "外套", category: "armor", price: 0, statBonus: { defense: 3 } };
const herb: ItemData = { id: "herb", name: "やくそう", category: "consumable", price: 1, healAmount: 10 };
const items: Record<string, ItemData> = { sword, dagger, staff, cloak, herb };

describe("仲間みんなの装備", () => {
  it("持ち物の中の装備だけを数える（回復の品は入らない）", () => {
    const inv = ensureOwned([{ itemId: "herb", quantity: 2 }], ["sword", "cloak"]);
    expect(ownedEquipmentIds(inv, items).sort()).toEqual(["cloak", "sword"]);
  });

  it("すでに持っている品は、ふやさない", () => {
    const inv = ensureOwned(ensureOwned([], ["sword"]), ["sword", undefined]);
    expect(inv).toEqual([{ itemId: "sword", quantity: 1 }]);
  });

  it("仲間も、持ち物から装備できる（持てる種類の武器だけ）", () => {
    const inv = ensureOwned([], ["sword", "dagger", "staff"]);
    let party = { hero: { weapon: "sword" } };
    // レトは短剣、ミナは杖。剣は、ユーリ専用
    expect(candidatesFor("reto", "weapon", party, inv, items).map((c) => c.item.id)).toEqual(["dagger"]);
    expect(candidatesFor("mina", "weapon", party, inv, items).map((c) => c.item.id)).toEqual(["staff"]);
    party = equipTo(party, "reto", dagger, inv) as typeof party;
    expect(party).toEqual({ hero: { weapon: "sword" }, reto: { weapon: "dagger" } });
    expect(wearerOf(party, "dagger")).toBe("reto");
  });

  it("持てない種類の武器は、つけられない（杖のミナに剣）", () => {
    const inv = ensureOwned([], ["sword"]);
    const party = { hero: { weapon: "sword" } };
    expect(equipTo(party, "mina", sword, inv)).toEqual(party);
    expect(sanitizeParty({ hero: { weapon: "sword" }, mina: { weapon: "sword", armor: "cloak" } }, items)).toEqual({ hero: { weapon: "sword" }, mina: { armor: "cloak" } });
  });

  it("ほかの人がつけている品を選ぶと、その人からはずれる", () => {
    const party = equipTo({ hero: { armor: "cloak" } }, "reto", cloak, ensureOwned([], ["cloak"]));
    expect(party.hero.armor).toBeUndefined();
    expect(party.reto.armor).toBe("cloak");
  });

  it("同じ品を2個持っていれば、2人がつけられる（あまりがあるときは、取りかえない）", () => {
    const inv = addItem(ensureOwned([], ["cloak"]), "cloak", 1); // 2個
    let party: Record<string, Record<string, string>> = { hero: { armor: "cloak" } };
    expect(candidatesFor("reto", "armor", party, inv, items).find((c) => c.item.id === "cloak")?.takenBy).toBeUndefined();
    party = equipTo(party, "reto", cloak, inv);
    expect(party.hero.armor).toBe("cloak");
    expect(party.reto.armor).toBe("cloak");
    // 3人目は、あまりがないので、取りかえになる
    const third = equipTo(party, "mina", cloak, inv);
    expect(Object.values(third).filter((s) => s.armor === "cloak")).toHaveLength(2);
    expect(third.mina.armor).toBe("cloak");
    expect(candidatesFor("mina", "armor", { ...party }, inv, items).find((c) => c.item.id === "cloak")?.takenBy).toBe("hero");
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
