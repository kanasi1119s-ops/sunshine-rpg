import { describe, expect, it } from "vitest";
import { allySlot, applyFormation, BACK_DEFENSE, FRONT_ATTACK, sortByOrder, swapOrder } from "./formation";
import type { Combatant } from "./types";

const mk = (id: string): Combatant => ({ id, name: id, maxHp: 100, hp: 100, maxMp: 0, mp: 0, attack: 100, defense: 100, speed: 10, isEnemy: false, guarding: false });

describe("戦闘の並び（横2列）", () => {
  it("1〜3人目は前列でこうげきが上がり、4人目からは後列でしゅびが上がる", () => {
    const p = applyFormation(["a", "b", "c", "d", "e"].map(mk));
    expect(p.slice(0, 3).map((c) => [c.attack, c.defense])).toEqual([[100 * FRONT_ATTACK, 100], [100 * FRONT_ATTACK, 100], [100 * FRONT_ATTACK, 100]].map(([a, d]) => [Math.round(a), d]));
    expect(p.slice(3).map((c) => [c.attack, c.defense])).toEqual([[100, Math.round(100 * BACK_DEFENSE)], [100, Math.round(100 * BACK_DEFENSE)]]);
  });
  it("並び順のとおりに並べ、2人を入れかえられる", () => {
    const members = ["hero", "reto", "mina", "orca"].map(mk);
    expect(sortByOrder(members, ["mina", "hero"]).map((m) => m.id)).toEqual(["mina", "hero", "reto", "orca"]);
    expect(swapOrder(["hero", "reto", "mina"], 0, 2)).toEqual(["mina", "reto", "hero"]);
  });
  it("前列は同じ高さに横一列、後列はその奥に横一列", () => {
    const s = [0, 1, 2, 3, 4, 5].map((i) => allySlot(i, 400, 165));
    expect(new Set(s.slice(0, 3).map((p) => p.feetY)).size).toBe(1);
    expect(new Set(s.slice(3).map((p) => p.feetY)).size).toBe(1);
    expect(s[3].feetY).toBeLessThan(s[0].feetY);
    expect(s[0].leftX).toBeLessThan(s[1].leftX);
    expect(Math.max(...s.map((p) => p.leftX)) + 16).toBeLessThanOrEqual(400);
  });
});
