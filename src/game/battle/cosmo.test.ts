import { describe, expect, it } from "vitest";
import { applyAction, COSMO_BEAM, COSMO_SHOTS, createBattleState, runTurn } from "./battle-engine";
import type { Combatant } from "./types";
import { applyTraits } from "../items/traits";
import { ALL_ITEMS_BY_ID } from "../economy/shop";
import { COSMO_ID } from "../items/legend-items";
import { createRng } from "../random";

const mk = (id: string, p: Partial<Combatant> = {}): Combatant => ({ id, name: id, maxHp: 500, hp: 500, maxMp: 0, mp: 0, attack: 100, defense: 50, speed: 50, isEnemy: false, guarding: false, ...p });

describe("コスモリングライト（6基の砲台の雷のビーム6連射）", () => {
  it("装備すると、たたかうが6連射になる", () => {
    const hero = applyTraits(mk("hero"), { weapon: COSMO_ID }, ALL_ITEMS_BY_ID);
    expect(hero.cosmo).toBe(true);
  });
  it("1発ごとに、攻撃力そのまま（しゅび・ぼうぎょ無視）のダメージを6回", () => {
    const s = createBattleState([mk("hero", { cosmo: true, attack: 120 })], [mk("e", { isEnemy: true, maxHp: 5000, hp: 5000, defense: 999 })]);
    s.enemies[0].guarding = true;
    const n = applyAction(s, { type: "attack", actorId: "hero", targetId: "e" }, createRng(1));
    const shots = n.log.filter((l) => l.includes(COSMO_BEAM));
    expect(shots).toHaveLength(COSMO_SHOTS);
    expect(shots.every((l) => l.endsWith("に 120 のダメージ"))).toBe(true);
    expect(n.enemies[0].hp).toBe(5000 - 120 * 6);
  });
  it("ねらった敵が倒れたら、ほかの敵を追う", () => {
    const s = createBattleState([mk("hero", { cosmo: true, attack: 100 })], [mk("a", { isEnemy: true, hp: 150, maxHp: 150 }), mk("b", { isEnemy: true, hp: 1000, maxHp: 1000 })]);
    const n = applyAction(s, { type: "attack", actorId: "hero", targetId: "a" }, createRng(2));
    expect(n.enemies[0].hp).toBe(0);
    expect(n.enemies[1].hp).toBe(1000 - 100 * 4);
  });
  it("すばやさの連続攻撃にはならない（6連射を1回）", () => {
    const s = createBattleState([mk("hero", { cosmo: true, attack: 10, speed: 999 })], [mk("e", { isEnemy: true, hp: 5000, maxHp: 5000, speed: 1, attack: 1 })]);
    const n = runTurn(s, [{ type: "attack", actorId: "hero", targetId: "e" }], createRng(3));
    expect(n.log.filter((l) => l.includes(COSMO_BEAM))).toHaveLength(COSMO_SHOTS);
    expect(n.log.some((l) => l.includes("すばやい動き"))).toBe(false);
  });
});
