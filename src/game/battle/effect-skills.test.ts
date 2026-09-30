import { describe, expect, it } from "vitest";
import { applyAction, createBattleState } from "./battle-engine";
import { BattleController } from "./battle-controller";
import type { Combatant, Skill } from "./types";

function make(overrides: Partial<Combatant> & { id: string }): Combatant {
  return { name: overrides.id, maxHp: 100, hp: 100, maxMp: 20, mp: 20, attack: 20, defense: 4, speed: 10, isEnemy: false, guarding: false, ...overrides };
}
const rng = () => 0.5;

const combo: Skill = { id: "combo", name: "二連打", mpCost: 3, powerMultiplier: 1.0, effect: "multi", hits: 2 };
const wave: Skill = { id: "wave", name: "火照の波", mpCost: 5, powerMultiplier: 1.0, effect: "damageAll" };
const heal: Skill = { id: "heal", name: "水紋の癒し", mpCost: 3, powerMultiplier: 0, effect: "heal", healRatio: 1.5 };
const rain: Skill = { id: "rain", name: "水紋の慈雨", mpCost: 8, powerMultiplier: 0, effect: "healAll", healRatio: 1.0 };

describe("効果つきの特技（エンジン）", () => {
  it("multi: 敵1体に指定回数ぶんダメージを与え、MPを1回だけ使う。途中で倒したら止まる", () => {
    const state = createBattleState([make({ id: "hero" })], [make({ id: "e1", isEnemy: true }), make({ id: "e2", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "e1", skill: combo }, rng);
    const dmg = 100 - after.enemies[0].hp;
    expect(dmg).toBeGreaterThan(20); // 1回ぶんより多い（2回ぶん）
    expect(after.enemies[1].hp).toBe(100);
    expect(after.party[0].mp).toBe(17);
    expect(after.log.filter((l) => l.includes("二連打")).length).toBe(2);
    const weak = createBattleState([make({ id: "hero" })], [make({ id: "e1", isEnemy: true, hp: 3 })]);
    const killed = applyAction(weak, { type: "skill", actorId: "hero", targetId: "e1", skill: combo }, rng);
    expect(killed.log.filter((l) => l.includes("二連打")).length).toBe(1);
  });

  it("damageAll: 生きている敵全員にダメージを与え、倒れた敵は狙わない", () => {
    const state = createBattleState(
      [make({ id: "hero" })],
      [make({ id: "e1", isEnemy: true }), make({ id: "e2", isEnemy: true }), make({ id: "e3", isEnemy: true, hp: 0 })],
    );
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "e1", skill: wave }, rng);
    expect(after.enemies[0].hp).toBeLessThan(100);
    expect(after.enemies[1].hp).toBeLessThan(100);
    expect(after.enemies[2].hp).toBe(0);
    expect(after.party[0].mp).toBe(15);
  });

  it("heal: 味方1人を「こうげき×割合」だけ回復する（最大HPまで）。倒れている味方には使えない", () => {
    const state = createBattleState([make({ id: "hero" }), make({ id: "ally", hp: 40 })], [make({ id: "e", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "ally", skill: heal }, rng);
    expect(after.party[1].hp).toBe(70); // 20 × 1.5 = 30
    expect(after.party[0].mp).toBe(17);
    const full = applyAction(state, { type: "skill", actorId: "hero", targetId: "hero", skill: heal }, rng);
    expect(full.party[0].hp).toBe(100);
    const dead = createBattleState([make({ id: "hero" }), make({ id: "ally", hp: 0 })], [make({ id: "e", isEnemy: true })]);
    const none = applyAction(dead, { type: "skill", actorId: "hero", targetId: "ally", skill: heal }, rng);
    expect(none.party[1].hp).toBe(0);
    expect(none.party[0].mp).toBe(20);
  });

  it("healAll: 生きている味方全員を回復する。倒れている味方は回復しない", () => {
    const state = createBattleState(
      [make({ id: "hero", hp: 10 }), make({ id: "a", hp: 50 }), make({ id: "b", hp: 0 })],
      [make({ id: "e", isEnemy: true })],
    );
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "hero", skill: rain }, rng);
    expect(after.party[0].hp).toBe(30);
    expect(after.party[1].hp).toBe(70);
    expect(after.party[2].hp).toBe(0);
  });

  it("MPが足りないと、何も起きない", () => {
    const state = createBattleState([make({ id: "hero", mp: 1 })], [make({ id: "e", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "e", skill: wave }, rng);
    expect(after.enemies[0].hp).toBe(100);
    expect(after.log.at(-1)).toContain("MPが足りず");
  });
});

describe("効果つきの特技（コマンド選択）", () => {
  const skills = { hero: { id: "base", name: "とくぎ", mpCost: 1, powerMultiplier: 1.2 } };
  const item = { id: "i", name: "薬", healAmount: 10 };
  const start = (extra: Skill[]) =>
    new BattleController(
      [make({ id: "hero" }), make({ id: "ally", hp: 50 })],
      [make({ id: "e1", isEnemy: true, hp: 1000, speed: 1 }), make({ id: "e2", isEnemy: true, hp: 1000, speed: 1 })],
      rng,
      { skills, item, extraSkills: { hero: extra } },
    );
  const chooseSkill = (controller: BattleController, index: number) => {
    controller.moveCursor(1); // 「とくぎ」
    controller.confirm();
    for (let i = 0; i < index; i++) {
      controller.moveCursor(1);
    }
    controller.confirm();
  };

  it("回復の特技は、味方を対象に選ぶ", () => {
    const controller = start([heal]);
    chooseSkill(controller, 1);
    const ui = controller.getUiState();
    expect(ui.kind).toBe("target");
    if (ui.kind === "target") {
      expect(ui.candidateIds).toEqual(["hero", "ally"]);
    }
  });

  it("敵全体・味方全体の特技は、対象を選ばずに、次の人のコマンドへ進む", () => {
    for (const skill of [wave, rain]) {
      const controller = start([skill]);
      chooseSkill(controller, 1);
      expect(controller.getUiState()).toEqual({ kind: "command", actorId: "ally", cursor: 0 });
    }
  });

  it("1体を狙う特技は、これまでどおり敵を対象に選ぶ", () => {
    const controller = start([combo]);
    chooseSkill(controller, 1);
    const ui = controller.getUiState();
    expect(ui.kind === "target" && ui.candidateIds).toEqual(["e1", "e2"]);
  });
});
