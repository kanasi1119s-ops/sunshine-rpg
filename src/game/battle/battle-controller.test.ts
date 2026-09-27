import { describe, expect, it } from "vitest";
import { BattleController, COMMANDS } from "./battle-controller";
import type { Combatant } from "./types";

function makeCombatant(overrides: Partial<Combatant> & { id: string }): Combatant {
  return {
    name: overrides.id,
    maxHp: 30,
    hp: 30,
    maxMp: 10,
    mp: 10,
    attack: 20,
    defense: 0,
    speed: 10,
    isEnemy: false,
    guarding: false,
    ...overrides,
  };
}

const skill = { id: "fire", name: "ファイア", mpCost: 3, powerMultiplier: 1.5 };
const item = { id: "herb", name: "やくそう", healAmount: 20 };

describe("BattleController", () => {
  it("最初はパーティ1人目のコマンド選択から始まる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skill, item },
    );
    expect(controller.getUiState()).toEqual({ kind: "command", actorId: "hero", cursor: 0 });
  });

  it("attackを選ぶと対象選択に移り、確定するとメッセージが出る", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skill, item },
    );

    expect(COMMANDS[0].kind).toBe("attack");
    controller.confirm(); // attackを選択
    expect(controller.getUiState()).toMatchObject({ kind: "target", commandKind: "attack" });

    controller.confirm(); // 対象（slime）を確定
    expect(controller.getUiState().kind).toBe("message");
  });

  it("defendとfleeは対象選択なしで即座に次の人へ進む", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "a" }), makeCombatant({ id: "b" })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1000, speed: 1 })],
      () => 0.5,
      { skill, item },
    );

    const defendIndex = COMMANDS.findIndex((c) => c.kind === "defend");
    controller.moveCursor(defendIndex); // aのコマンドをdefendに合わせる
    controller.confirm();

    expect(controller.getUiState()).toEqual({ kind: "command", actorId: "b", cursor: 0 });
  });

  it("敵を倒すと最終的にfinished(won)になる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero", attack: 999, speed: 100 })],
      [makeCombatant({ id: "slime", isEnemy: true, hp: 1, defense: 0, speed: 1 })],
      () => 0.5,
      { skill, item },
    );

    controller.confirm(); // attack
    controller.confirm(); // target slime

    // メッセージを最後まで送る。
    let guard = 0;
    while (controller.getUiState().kind === "message" && guard < 20) {
      controller.confirm();
      guard++;
    }

    expect(controller.getUiState().kind).toBe("finished");
    expect(controller.getUiState()).toMatchObject({ outcome: "won" });
  });

  it("味方が全滅するとfinished(lost)になる", () => {
    const controller = new BattleController(
      [makeCombatant({ id: "hero", hp: 1, defense: 0, speed: 1 })],
      [makeCombatant({ id: "slime", isEnemy: true, attack: 999, speed: 100 })],
      () => 0.5,
      { skill, item },
    );

    const defendIndex = COMMANDS.findIndex((c) => c.kind === "defend");
    controller.moveCursor(defendIndex);
    controller.confirm(); // defend（enemyのAI攻撃で倒れるはず）

    let guard = 0;
    while (controller.getUiState().kind === "message" && guard < 20) {
      controller.confirm();
      guard++;
    }

    expect(controller.getUiState()).toMatchObject({ kind: "finished", outcome: "lost" });
  });
});
