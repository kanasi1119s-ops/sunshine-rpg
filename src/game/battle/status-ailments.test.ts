import { describe, expect, it } from "vitest";
import { runTurn, createBattleState } from "./battle-engine";
import type { Combatant } from "./types";

const c = (o: Partial<Combatant> & { id: string }): Combatant => ({ name: o.id, maxHp: 50, hp: 50, maxMp: 10, mp: 10, attack: 10, defense: 0, speed: 10, isEnemy: false, guarding: false, ...o });

describe("状態異常（毒・混乱・敵の状態異常攻撃）", () => {
  it("毒は、ターンの終わりにダメージを与え、HPは1より下がらず、残りターンが減って消える", () => {
    const st = createBattleState([c({ id: "hero", poison: 2, hp: 4 })], [c({ id: "slime", isEnemy: true, hp: 999, speed: 1, attack: 0 })]);
    const t1 = runTurn(st, [{ type: "defend", actorId: "hero" }], () => 0.5);
    expect(t1.party[0].hp).toBeGreaterThanOrEqual(1);
    expect(t1.log.join("\n")).toContain("毒のダメージ");
    expect(t1.party[0].poison).toBe(1);
    const t2 = runTurn(t1, [{ type: "defend", actorId: "hero" }], () => 0.5);
    expect(t2.party[0].poison).toBeUndefined();
    expect(t2.log.join("\n")).toContain("毒が消えた");
  });
  it("混乱中は、乱数しだいで味方をなぐる（ログに出る）", () => {
    const st = createBattleState([c({ id: "hero", confused: 2, speed: 20 }), c({ id: "mina" })], [c({ id: "slime", isEnemy: true, hp: 999, speed: 1, attack: 0 })]);
    const t = runTurn(st, [{ type: "attack", actorId: "hero", targetId: "slime" }], () => 0.1);
    expect(t.log.join("\n")).toContain("混乱している");
  });
  it("敵の通常攻撃が当たると、ときどき状態異常がかかる", () => {
    for (const [status, text] of [["poison", "毒におかされた"], ["sleep", "眠ってしまった"], ["confuse", "混乱した"]] as const) {
      const st = createBattleState([c({ id: "hero" })], [c({ id: "spider", isEnemy: true, speed: 30, inflicts: { status, chance: 1, turns: 3 } })]);
      const t = runTurn(st, [{ type: "defend", actorId: "hero" }, { type: "attack", actorId: "spider", targetId: "hero" }], () => 0.5);
      expect(t.log.join("\n")).toContain(text);
    }
  });
});
