import { describe, expect, it } from "vitest";
import { runTurn } from "./battle-engine";
import type { BattleState, Combatant } from "./types";

const mk = (id: string, isEnemy: boolean, speed: number): Combatant => ({
  id, name: id, maxHp: 100, hp: 100, maxMp: 0, mp: 0, attack: 30, defense: 5, speed, isEnemy, guarding: false,
});

describe("行動ごとのHPの記録", () => {
  it("1行動ごとに、その時点のHPが残り、後の行動のダメージは前の行に入らない", () => {
    const s: BattleState = { party: [mk("a", false, 20), mk("b", false, 10)], enemies: [mk("e", true, 1)], log: [], fled: false };
    const next = runTurn(s, [
      { type: "attack", actorId: "a", targetId: "e" },
      { type: "attack", actorId: "b", targetId: "e" },
    ], () => 0.5);
    const trail = next.hpTrail!;
    const first = trail.find((t) => t.end > 0)!;
    const last = trail[trail.length - 1];
    expect(first.hp.e).toBeLessThan(100);
    expect(last.hp.e).toBeLessThan(first.hp.e);
    const afterFirst = trail.find((t) => t.end === 1)!;
    expect(afterFirst.hp.e).toBe(first.hp.e);
  });
});
