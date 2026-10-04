import { describe, expect, it } from "vitest";
import type { Combatant } from "./battle/types";
import { applyVital, fullRestore, growVital, healVital, vitalsAfterBattle, type Vitals } from "./vitals";

const c = (id: string, hp: number, mp: number, isEnemy = false): Combatant => ({ id, name: id, maxHp: 30, hp, maxMp: 10, mp, attack: 5, defense: 5, speed: 5, isEnemy, guarding: false });

describe("vitals", () => {
  it("戦闘後の味方のHP・MPを持ち越し、敵は入れない", () => {
    const v = vitalsAfterBattle([c("hero", 12, 4), c("mina", 0, 2), c("slime", 5, 0, true)], false);
    expect(v).toEqual({ hero: { hp: 12, mp: 4 }, mina: { hp: 1, mp: 2 } });
  });
  it("負けたときは全員HP1", () => {
    expect(vitalsAfterBattle([c("hero", 0, 3)], true).hero).toEqual({ hp: 1, mp: 3 });
  });
  it("戦闘に出すとき、最大値をこえず、入っていない人は全快のまま", () => {
    expect(applyVital(c("hero", 30, 10), { hp: 99, mp: 99 })).toMatchObject({ hp: 30, mp: 10 });
    expect(applyVital(c("hero", 30, 10), { hp: 7, mp: 3 })).toMatchObject({ hp: 7, mp: 3 });
    expect(applyVital(c("hero", 30, 10), undefined)).toMatchObject({ hp: 30, mp: 10 });
  });
  it("回復・全快・レベルアップ", () => {
    let v: Vitals = { hero: { hp: 5, mp: 2 } };
    v = healVital(v, "hero", { maxHp: 30, maxMp: 10 }, 40, 3);
    expect(v.hero).toEqual({ hp: 30, mp: 5 });
    expect(growVital(v, "hero", 4, 1).hero).toEqual({ hp: 34, mp: 6 });
    expect(fullRestore(v)).toEqual({});
    expect(fullRestore({ ...v, mina: { hp: 1, mp: 1 } }, ["mina"])).toEqual({ hero: v.hero });
  });
});
