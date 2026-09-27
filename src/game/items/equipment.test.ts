import { describe, expect, it } from "vitest";
import {
  applyStatBonus,
  computeEquipmentBonus,
  createEquipmentSlots,
  equip,
  unequip,
} from "./equipment";
import type { ItemData } from "./types";

const sword: ItemData = {
  id: "sword",
  name: "どうのつるぎ（仮）",
  category: "weapon",
  price: 100,
  statBonus: { attack: 5 },
};

const shield: ItemData = {
  id: "shield",
  name: "かわのたて（仮）",
  category: "armor",
  price: 50,
  statBonus: { defense: 3, maxHp: 2 },
};

const items: Record<string, ItemData> = { sword, shield };

describe("equip / unequip", () => {
  it("装備するとそのカテゴリのスロットが埋まる", () => {
    const slots = equip(createEquipmentSlots(), sword);
    expect(slots.weapon).toBe("sword");
  });

  it("同じカテゴリの装備を後から装備すると入れ替わる", () => {
    let slots = equip(createEquipmentSlots(), sword);
    const otherSword: ItemData = { ...sword, id: "sword2" };
    slots = equip(slots, otherSword);
    expect(slots.weapon).toBe("sword2");
  });

  it("unequipでスロットが空になる", () => {
    let slots = equip(createEquipmentSlots(), sword);
    slots = unequip(slots, "weapon");
    expect(slots.weapon).toBeUndefined();
  });
});

describe("computeEquipmentBonus", () => {
  it("装備しているものすべてのボーナスを合計する", () => {
    let slots = createEquipmentSlots();
    slots = equip(slots, sword);
    slots = equip(slots, shield);
    expect(computeEquipmentBonus(slots, items)).toEqual({ attack: 5, defense: 3, maxHp: 2 });
  });

  it("何も装備していなければ空", () => {
    expect(computeEquipmentBonus(createEquipmentSlots(), items)).toEqual({});
  });
});

describe("applyStatBonus", () => {
  it("基本能力値にボーナスを足した値を返す（基本値は変えない）", () => {
    const base = { level: 1, exp: 0, maxHp: 20, hp: 20, maxMp: 5, mp: 5, attack: 8, defense: 4, speed: 6 };
    const result = applyStatBonus(base, { attack: 5, defense: 3, maxHp: 2 });
    expect(result.attack).toBe(13);
    expect(result.defense).toBe(7);
    expect(result.maxHp).toBe(22);
    expect(result.hp).toBe(22);
    expect(base.maxHp).toBe(20); // 元のオブジェクトは変わらない
  });

  it("HPボーナスを足しても最大HPを超えない", () => {
    const base = { level: 1, exp: 0, maxHp: 20, hp: 10, maxMp: 5, mp: 5, attack: 8, defense: 4, speed: 6 };
    const result = applyStatBonus(base, { maxHp: 100 });
    expect(result.hp).toBe(110);
    expect(result.maxHp).toBe(120);
  });
});
