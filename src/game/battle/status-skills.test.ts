import { describe, expect, it } from "vitest";
import { applyAction, createBattleState, resolveTurnOrder, runTurn } from "./battle-engine";
import { effectiveStat, type Combatant, type Skill } from "./types";
import { JOBS_BY_ID } from "../job/jobs";
import { battleSeFor } from "./battle-se";

function make(overrides: Partial<Combatant> & { id: string }): Combatant {
  return { name: overrides.id, maxHp: 100, hp: 100, maxMp: 20, mp: 20, attack: 20, defense: 4, speed: 10, isEnemy: false, guarding: false, ...overrides };
}
const rng = () => 0.5;

const guardUp: Skill = { id: "g", name: "地固の壁", mpCost: 3, powerMultiplier: 0, effect: "buff", stat: "defense", mult: 1.6, turns: 3 };
const cheer: Skill = { id: "c", name: "はやし立て", mpCost: 6, powerMultiplier: 0, effect: "buffAll", stat: "attack", mult: 1.25, turns: 3 };
const slow: Skill = { id: "s", name: "足止めの矢", mpCost: 3, powerMultiplier: 0, effect: "debuff", stat: "speed", mult: 0.7, turns: 3 };
const lullaby: Skill = { id: "l", name: "風唱の眠り唄", mpCost: 5, powerMultiplier: 0, effect: "sleep", chance: 0.6, turns: 2 };

describe("強化・弱体・眠り（エンジン）", () => {
  it("buff: 味方1人の能力が上がり、MPを使う。上がった能力は実際のダメージに効く", () => {
    const state = createBattleState([make({ id: "hero" }), make({ id: "ally" })], [make({ id: "e", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "ally", skill: guardUp }, rng);
    expect(effectiveStat(after.party[1], "defense")).toBe(Math.round(4 * 1.6));
    expect(effectiveStat(after.party[0], "defense")).toBe(4);
    expect(after.party[0].mp).toBe(17);
    expect(after.log.at(-1)).toContain("しゅびが上がった");
  });

  it("buffAll: 生きている味方全員の能力が上がる", () => {
    const state = createBattleState([make({ id: "a" }), make({ id: "b" }), make({ id: "c", hp: 0 })], [make({ id: "e", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "a", targetId: "a", skill: cheer }, rng);
    expect(effectiveStat(after.party[0], "attack")).toBe(25);
    expect(effectiveStat(after.party[1], "attack")).toBe(25);
    expect(effectiveStat(after.party[2], "attack")).toBe(20);
  });

  it("debuff: 確率で敵の能力が下がり、すばやさが下がると行動順が遅くなる", () => {
    const state = createBattleState([make({ id: "hero", speed: 5 })], [make({ id: "e", isEnemy: true, speed: 10 })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "e", skill: slow }, rng);
    expect(effectiveStat(after.enemies[0], "speed")).toBe(7);
    const order = resolveTurnOrder([...after.party, ...after.enemies], rng).map((c) => c.id);
    expect(order).toEqual(["e", "hero"]); // 7 > 5 なのでまだ敵が先
    const slower = applyAction(state, { type: "skill", actorId: "hero", targetId: "e", skill: { ...slow, mult: 0.3 } }, rng);
    expect(resolveTurnOrder([...slower.party, ...slower.enemies], rng)[0].id).toBe("hero");
  });

  it("sleep: 眠った相手は次のターンは行動できず、その次のターンから動く。強敵には効かない", () => {
    const state = createBattleState([make({ id: "hero", speed: 30 })], [make({ id: "e", isEnemy: true })]);
    const slept = applyAction(state, { type: "skill", actorId: "hero", targetId: "e", skill: lullaby }, () => 0.1);
    expect(slept.enemies[0].sleep).toBe(2);
    const actions = [{ type: "attack" as const, actorId: "e", targetId: "hero" }];
    const t1 = runTurn(slept, actions, rng);
    expect(t1.party[0].hp).toBe(100);
    expect(t1.log.some((l) => l.includes("眠っている"))).toBe(true);
    const t2 = runTurn(t1, actions, rng);
    expect(t2.party[0].hp).toBe(100);
    const t3 = runTurn(t2, actions, rng);
    expect(t3.party[0].hp).toBeLessThan(100);
    const boss = createBattleState([make({ id: "hero" })], [make({ id: "b", isEnemy: true, maxHp: 900, hp: 900 })]);
    const resisted = applyAction(boss, { type: "skill", actorId: "hero", targetId: "b", skill: lullaby }, () => 0.1);
    expect(resisted.enemies[0].sleep).toBeUndefined();
    expect(resisted.log.at(-1)).toContain("効かなかった");
  });

  it("強化はターンの終わりに減り、切れると元に戻る", () => {
    const state = createBattleState([make({ id: "hero", speed: 30 })], [make({ id: "e", isEnemy: true })]);
    let now = applyAction(state, { type: "skill", actorId: "hero", targetId: "hero", skill: guardUp }, rng);
    for (let i = 0; i < 3; i++) {
      expect(effectiveStat(now.party[0], "defense")).toBe(6);
      now = runTurn(now, [{ type: "defend", actorId: "hero" }], rng);
    }
    expect(effectiveStat(now.party[0], "defense")).toBe(4);
  });

  it("MPが足りなくても、効果つき特技として扱われる（何も起きない）", () => {
    const state = createBattleState([make({ id: "hero", mp: 0 })], [make({ id: "e", isEnemy: true })]);
    const after = applyAction(state, { type: "skill", actorId: "hero", targetId: "hero", skill: guardUp }, rng);
    expect(after.party[0].mods).toBeUndefined();
  });
});

describe("強化・弱体のジョブ特技と効果音", () => {
  it("ジョブの特技の説明どおりの効果が、戦闘に接続されている", () => {
    const battleSkills = Object.values(JOBS_BY_ID).flatMap((j) => j.skills).filter((s) => s.battle && ["buff", "buffAll", "debuff", "debuffAll", "sleep"].includes(s.battle.effect ?? ""));
    expect(battleSkills.map((s) => s.name)).toEqual(
      expect.arrayContaining(["受け流し", "足さばき", "足止めの矢", "水紋の膜", "風唱の追い風", "風唱の眠り唄", "地固の壁", "地固の縛り", "はやし立て", "目くらまし"]),
    );
  });
  it("強化は「能力アップ」、弱体・眠りは「能力ダウン」の音", () => {
    expect(battleSeFor("ミナ の水紋の膜！ ユーリ のしゅびが上がった", ["ユーリ", "ミナ"])).toBe("buff");
    expect(battleSeFor("ガイド の足止めの矢！ 歪み のすばやさが下がった", ["ユーリ"])).toBe("debuff");
    expect(battleSeFor("ガイド の風唱の眠り唄！ 歪み は眠ってしまった", ["ユーリ"])).toBe("debuff");
  });
});
