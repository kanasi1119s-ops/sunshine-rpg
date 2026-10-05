import { describe, expect, it } from "vitest";
import { runTurn } from "./battle-engine";
import type { BattleState, Combatant } from "./types";

const mk = (id: string, isEnemy: boolean, speed: number): Combatant => ({
  id, name: id, maxHp: 100, hp: 100, maxMp: 0, mp: 0, attack: 30, defense: 5, speed, isEnemy, guarding: false,
});

describe("行動ごとのHPの記録", () => {
  it("1行動ごとに、その時点のHPが残り、後の行動のダメージは前の行に入らない", () => {
    const s: BattleState = { party: [mk("a", false, 5), mk("b", false, 4)], enemies: [mk("e", true, 3)], log: [], fled: false };
    const next = runTurn(s, [
      { type: "attack", actorId: "a", targetId: "e" },
      { type: "attack", actorId: "b", targetId: "e" },
    ], () => 0.5);
    const trail = next.hpTrail!;
    const first = trail.find((t) => t.end > 0)!;
    const last = trail[trail.length - 1];
    expect(first.hp.e).toBeLessThan(100);
    expect(last.hp.e).toBeLessThan(first.hp.e);
    expect(last.hp.e).toBeLessThanOrEqual(first.hp.e);
  });
});

describe("連続攻撃・ミス・運", () => {
  it("すばやさの差が大きいほど、1回の攻撃での回数がふえる（2→3→4回）", async () => {
    const { attackCount } = await import("./formulas");
    expect([0, 11, 12, 23, 24, 39, 40, 99].map(attackCount)).toEqual([1, 1, 2, 2, 3, 3, 4, 4]);
  });
  it("運が高いほど会心が出やすく、相手の運が高いほどミスしやすい", async () => {
    const { criticalChance, missChance } = await import("./formulas");
    expect(criticalChance(15)).toBeGreaterThan(criticalChance(5));
    expect(missChance(5, 15)).toBeGreaterThan(missChance(15, 5));
  });
  it("すばやさが相手よりずっと高いと、1回の行動で複数回こうげきする", () => {
    const s: BattleState = { party: [mk("a", false, 60)], enemies: [mk("e", true, 5)], log: [], fled: false };
    s.enemies[0].maxHp = s.enemies[0].hp = 9999;
    const next = runTurn(s, [{ type: "attack", actorId: "a", targetId: "e" }], () => 0.5);
    expect(next.log.some((l) => l.includes("4回 こうげき"))).toBe(true);
    expect(next.log.filter((l) => l.includes("のダメージ"))).toHaveLength(4);
  });
  it("ミスのとき、ダメージは入らない", () => {
    const s: BattleState = { party: [mk("a", false, 5)], enemies: [mk("e", true, 5)], log: [], fled: false };
    const next = runTurn(s, [{ type: "attack", actorId: "a", targetId: "e" }], () => 0.001);
    expect(next.log.some((l) => l.includes("ミス！"))).toBe(true);
    expect(next.enemies[0].hp).toBe(100);
  });
});
