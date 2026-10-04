import { describe, expect, it } from "vitest";
import {
  applyAction,
  checkOutcome,
  chooseEnemyAction,
  computeVictoryExp,
  createBattleState,
  resolveTurnOrder,
  runTurn,
} from "./battle-engine";
import type { Combatant, Skill } from "./types";

function makeCombatant(overrides: Partial<Combatant> & { id: string }): Combatant {
  return {
    name: overrides.id,
    maxHp: 30,
    hp: 30,
    maxMp: 10,
    mp: 10,
    attack: 10,
    defense: 5,
    speed: 10,
    isEnemy: false,
    guarding: false,
    ...overrides,
  };
}

const fixedRng = () => 0.5;

describe("createBattleState", () => {
  it("guardingをfalseにしてコピーする", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero", guarding: true })],
      [makeCombatant({ id: "slime", isEnemy: true })],
    );
    expect(state.party[0].guarding).toBe(false);
  });
});

describe("checkOutcome", () => {
  it("敵が全滅したらwon", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", hp: 0 })],
    );
    expect(checkOutcome(state)).toBe("won");
  });

  it("味方が全滅したらlost", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero", hp: 0 })],
      [makeCombatant({ id: "slime" })],
    );
    expect(checkOutcome(state)).toBe("lost");
  });

  it("両方生きていればongoing", () => {
    const state = createBattleState([makeCombatant({ id: "hero" })], [makeCombatant({ id: "slime" })]);
    expect(checkOutcome(state)).toBe("ongoing");
  });
});

describe("resolveTurnOrder", () => {
  it("すばやさが高い順に並べる", () => {
    const fast = makeCombatant({ id: "fast", speed: 20 });
    const slow = makeCombatant({ id: "slow", speed: 5 });
    const order = resolveTurnOrder([slow, fast], fixedRng);
    expect(order.map((c) => c.id)).toEqual(["fast", "slow"]);
  });

  it("戦闘不能を除く", () => {
    const alive = makeCombatant({ id: "alive", speed: 10 });
    const dead = makeCombatant({ id: "dead", speed: 20, hp: 0 });
    const order = resolveTurnOrder([alive, dead], fixedRng);
    expect(order.map((c) => c.id)).toEqual(["alive"]);
  });
});

describe("applyAction", () => {
  it("attack: 対象のHPを減らしログを残す", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero", attack: 20 })],
      [makeCombatant({ id: "slime", defense: 0, hp: 30 })],
    );
    const next = applyAction(state, { type: "attack", actorId: "hero", targetId: "slime" }, fixedRng);
    const slime = next.enemies.find((c) => c.id === "slime")!;
    expect(slime.hp).toBeLessThan(30);
    expect(next.log.length).toBe(1);
  });

  it("skill: MP不足なら不発になる", () => {
    const skill: Skill = { id: "fireball", name: "ファイア", mpCost: 99, powerMultiplier: 2 };
    const state = createBattleState(
      [makeCombatant({ id: "hero", mp: 5 })],
      [makeCombatant({ id: "slime" })],
    );
    const next = applyAction(
      state,
      { type: "skill", actorId: "hero", targetId: "slime", skill },
      fixedRng,
    );
    expect(next.enemies[0].hp).toBe(30);
    expect(next.party[0].mp).toBe(5);
  });

  it("item: 対象のHPを回復する（最大値を超えない）", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero", hp: 10, maxHp: 30 })],
      [makeCombatant({ id: "slime" })],
    );
    const next = applyAction(
      state,
      { type: "item", actorId: "hero", targetId: "hero", item: { id: "potion", name: "やくそう", healAmount: 50 } },
      fixedRng,
    );
    expect(next.party[0].hp).toBe(30);
  });

  it("defend: guardingがtrueになり、ダメージが半分になる", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero", defense: 0, hp: 30, maxHp: 30 })],
      [makeCombatant({ id: "slime", attack: 20 })],
    );
    const guarded = applyAction(state, { type: "defend", actorId: "hero" }, fixedRng);
    const withoutGuard = applyAction(state, { type: "attack", actorId: "slime", targetId: "hero" }, fixedRng);
    const withGuard = applyAction(guarded, { type: "attack", actorId: "slime", targetId: "hero" }, fixedRng);

    const damageWithout = 30 - withoutGuard.party[0].hp;
    const damageWith = 30 - withGuard.party[0].hp;
    expect(damageWith).toBeLessThan(damageWithout);
  });

  it("flee: 成功率を下回る乱数なら逃げ切る", () => {
    const state = createBattleState([makeCombatant({ id: "hero" })], [makeCombatant({ id: "slime" })]);
    const next = applyAction(state, { type: "flee", actorId: "hero" }, () => 0);
    expect(next.fled).toBe(true);
  });

  it("flee: 成功率を上回る乱数なら失敗する", () => {
    const state = createBattleState([makeCombatant({ id: "hero" })], [makeCombatant({ id: "slime" })]);
    const next = applyAction(state, { type: "flee", actorId: "hero" }, () => 0.999);
    expect(next.fled).toBe(false);
  });
});

describe("runTurn", () => {
  it("すばやさ順に処理し、決着がついたら残りの行動を打ち切る", () => {
    const hero = makeCombatant({ id: "hero", speed: 20, attack: 100 });
    const slime = makeCombatant({ id: "slime", speed: 5, hp: 1, defense: 0 });
    const state = createBattleState([hero], [slime]);

    const next = runTurn(
      state,
      [
        { type: "attack", actorId: "hero", targetId: "slime" },
        { type: "attack", actorId: "slime", targetId: "hero" },
      ],
      fixedRng,
    );

    expect(next.enemies[0].hp).toBe(0);
    expect(next.party[0].hp).toBe(hero.maxHp); // slimeは倒れているので反撃できない
  });
});

describe("computeVictoryExp", () => {
  it("敵の経験値をすべて合算する", () => {
    const state = createBattleState(
      [makeCombatant({ id: "hero" })],
      [
        makeCombatant({ id: "a", expReward: 10 }),
        makeCombatant({ id: "b", expReward: 15 }),
      ],
    );
    expect(computeVictoryExp(state)).toBe(25);
  });

  it("expRewardが無い敵は0として扱う", () => {
    const state = createBattleState([makeCombatant({ id: "hero" })], [makeCombatant({ id: "a" })]);
    expect(computeVictoryExp(state)).toBe(0);
  });
});

describe("chooseEnemyAction", () => {
  it("生きている味方だけを狙う", () => {
    const enemy = makeCombatant({ id: "slime", isEnemy: true });
    const dead = makeCombatant({ id: "dead", hp: 0 });
    const alive = makeCombatant({ id: "alive" });
    const action = chooseEnemyAction(enemy, [dead, alive], () => 0.9);
    expect(action.type).toBe("attack");
    if (action.type === "attack") {
      expect(action.targetId).toBe("alive");
    }
  });
});

describe("ねらった敵が倒れていたとき", () => {
  it("同じターンの、あとの味方の行動は、生きているつぎの敵に自動でねらいをかえる", () => {
    const hero = { id: "hero", name: "ユーリ", isEnemy: false, hp: 50, maxHp: 50, mp: 0, maxMp: 0, attack: 30, defense: 1, speed: 20 } as never;
    const friend = { id: "reto", name: "レト", isEnemy: false, hp: 50, maxHp: 50, mp: 0, maxMp: 0, attack: 30, defense: 1, speed: 10 } as never;
    const a = { id: "e1", name: "敵A", isEnemy: true, hp: 1, maxHp: 1, mp: 0, maxMp: 0, attack: 1, defense: 0, speed: 1 } as never;
    const b = { id: "e2", name: "敵B", isEnemy: true, hp: 100, maxHp: 100, mp: 0, maxMp: 0, attack: 1, defense: 0, speed: 1 } as never;
    const state = { party: [hero, friend], enemies: [a, b], log: [], fled: false } as never;
    const after = applyAction(applyAction(state, { type: "attack", actorId: "hero", targetId: "e1" }, () => 0.5), { type: "attack", actorId: "reto", targetId: "e1" }, () => 0.5);
    expect(after.enemies[0].hp).toBe(0);
    expect(after.enemies[1].hp).toBeLessThan(100);
  });
});
