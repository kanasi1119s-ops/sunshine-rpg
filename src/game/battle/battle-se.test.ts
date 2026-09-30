import { describe, expect, it } from "vitest";
import { battleSeFor } from "./battle-se";
import { applyAction, createBattleState } from "./battle-engine";
import type { Combatant, Skill } from "./types";

const party = ["ユーリ", "レト"];

describe("戦闘の効果音", () => {
  it("味方の攻撃は斬撃、会心は会心の音、敵の攻撃を受けたらダメージの音", () => {
    expect(battleSeFor("ユーリ の たたかう！ スライム に 8 のダメージ", party)).toBe("attack");
    expect(battleSeFor("ユーリ の たたかう！ 会心の一撃！ スライム に 16 のダメージ", party)).toBe("critical");
    expect(battleSeFor("スライム の たたかう！ ユーリ に 5 のダメージ", party)).toBe("player-damage");
  });

  it("特技の名前で、炎・風・氷（水）の術の音になる", () => {
    expect(battleSeFor("ユーリ の 火照ノ一！ スライム に 20 のダメージ", party)).toBe("fire");
    expect(battleSeFor("ユーリ の 疾風の刃！ スライム に 20 のダメージ", party)).toBe("wind");
    expect(battleSeFor("ミナ の 水紋ノ波！ スライム に 20 のダメージ", ["ミナ"])).toBe("ice");
  });

  it("敵を倒したときだけ「倒した」音。味方が倒れたときは鳴らさない", () => {
    expect(battleSeFor("スライム を倒した！", party)).toBe("enemy-down");
    expect(battleSeFor("レト を倒した！", party)).toBeNull();
    expect(battleSeFor("ユーリ の 羽音！ スライム は一撃で倒れた", party)).toBe("enemy-down");
  });

  it("回復・防御・逃走・MP不足・HPを支払う", () => {
    expect(battleSeFor("ユーリ の 水紋の癒し！ レト のHPが 30 回復した", party)).toBe("heal");
    expect(battleSeFor("ユーリ は 灯り草 を使った。ユーリ のHPが回復した", party)).toBe("heal");
    expect(battleSeFor("ユーリ は身を守っている", party)).toBe("guard");
    expect(battleSeFor("うまく逃げ切った！", party)).toBe("flee");
    expect(battleSeFor("しかし逃げられなかった！", party)).toBe("flee-fail");
    expect(battleSeFor("ユーリ はMPが足りず 火照ノ一 を使えなかった", party)).toBe("error");
    expect(battleSeFor("ユーリ は 12 のHPを支払った", party)).toBe("debuff");
    expect(battleSeFor("なにかふしぎなできごと", party)).toBeNull();
  });

  it("実際のエンジンが出すログ（ダメージ・会心・回復）を、すべて認識できる", () => {
    const make = (id: string, isEnemy: boolean): Combatant => ({ id, name: id, maxHp: 100, hp: 60, maxMp: 20, mp: 20, attack: 20, defense: 4, speed: 10, isEnemy, guarding: false });
    const heal: Skill = { id: "h", name: "水紋の癒し", mpCost: 3, powerMultiplier: 0, effect: "heal", healRatio: 1 };
    const base = createBattleState([make("ユーリ", false), make("レト", false)], [make("スライム", true)]);
    const hit = applyAction(base, { type: "attack", actorId: "ユーリ", targetId: "スライム" }, () => 0.5);
    expect(battleSeFor(hit.log.at(-1)!, ["ユーリ", "レト"])).toBe("attack");
    const enemyHit = applyAction(base, { type: "attack", actorId: "スライム", targetId: "ユーリ" }, () => 0.5);
    expect(battleSeFor(enemyHit.log.at(-1)!, ["ユーリ", "レト"])).toBe("player-damage");
    const healed = applyAction(base, { type: "skill", actorId: "ユーリ", targetId: "レト", skill: heal }, () => 0.5);
    expect(battleSeFor(healed.log.at(-1)!, ["ユーリ", "レト"])).toBe("heal");
  });
});
