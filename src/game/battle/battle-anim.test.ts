import { describe, expect, it } from "vitest";
import { battleAnimFor, fxForSkillName } from "./battle-anim";
import type { BattleState, Combatant } from "./types";

const c = (id: string, name: string, isEnemy = false): Combatant => ({ id, name, maxHp: 30, hp: 30, maxMp: 5, mp: 5, attack: 5, defense: 0, speed: 5, isEnemy, guarding: false });
const state: BattleState = { party: [c("hero", "ユーリ Lv1"), c("guide", "ガイド Lv1"), c("mina", "ミナ Lv1"), c("orca", "オルカ Lv1")], enemies: [c("slime", "ゆらぎ玉", true)], log: [], fled: false };
const weapons: Record<string, "sword" | "bow" | "staff" | "axe"> = { hero: "sword", guide: "bow", mina: "staff", orca: "axe" };
const w = (id: string) => weapons[id];

describe("戦闘の動き", () => {
  it("味方のたたかうは、武器ごとの動き（ガイドは矢をはなつ）", () => {
    expect(battleAnimFor("ユーリ Lv1 の たたかう！ ゆらぎ玉 に 5 のダメージ", state, w)).toMatchObject({ actorId: "hero", motion: "slash", targetIds: ["slime"] });
    expect(battleAnimFor("ガイド Lv1 の たたかう！ ゆらぎ玉 に 5 のダメージ", state, w)?.motion).toBe("shoot");
    expect(battleAnimFor("オルカ Lv1 の たたかう！ ゆらぎ玉 に 5 のダメージ", state, w)?.motion).toBe("chop");
  });
  it("魔法使い（ミナ）の技は、かざして唱え、水のエフェクト", () => {
    expect(battleAnimFor("ミナ Lv1 の 水紋ノ波！ ゆらぎ玉 に 9 のダメージ", state, w)).toMatchObject({ motion: "cast", fx: "water" });
  });
  it("回復は、唱えて、対象に回復のエフェクト", () => {
    expect(battleAnimFor("ミナ Lv1 の 雫ノ恵み！ ユーリ Lv1 のHPが 20 回復した", state, w)).toMatchObject({ motion: "cast", fx: "heal", targetIds: ["hero"] });
  });
  it("敵の攻撃で味方がのけぞる。敵への攻撃では、敵の動きは無い", () => {
    expect(battleAnimFor("ゆらぎ玉 の たたかう！ ユーリ Lv1 に 3 のダメージ", state, w)).toMatchObject({ hurt: true, targetIds: ["hero"], motion: null });
  });
  it("状態異常のエフェクト", () => {
    expect(battleAnimFor("ユーリ Lv1 は毒におかされた！", state, w)?.fx).toBe("poison");
    expect(battleAnimFor("ガイド Lv1 は眠ってしまった", state, w)?.fx).toBe("sleep");
    expect(battleAnimFor("ミナ Lv1 は混乱した！", state, w)?.fx).toBe("confuse");
    expect(battleAnimFor("ユーリ Lv1 は毒のダメージを受けた（2）", state, w)?.fx).toBe("poison");
  });
  it("技の名前からエフェクトの種類", () => {
    expect(fxForSkillName("火照ノ一")).toBe("fire");
    expect(fxForSkillName("光断ノ一閃")).toBe("light");
    expect(fxForSkillName("疾風ノ矢")).toBe("wind");
    expect(fxForSkillName("よくわからない")).toBe("burst");
  });
});

describe("敵の魔法", () => {
  it("敵が技名つきでダメージを与えたら、敵が光をため、味方の上にエフェクト、味方はのけぞる", () => {
    const anim = battleAnimFor("ゆらぎ玉 の 滴ノ礫！ ユーリ Lv1 に 6 のダメージ", state, w);
    expect(anim).toMatchObject({ casterId: "slime", fx: "water", hurt: true, targetIds: ["hero"], motion: null });
  });
});
