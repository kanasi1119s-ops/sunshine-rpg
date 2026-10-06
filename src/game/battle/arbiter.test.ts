import { describe, expect, it } from "vitest";
import { ARBITER_SKILLS, ARBITER_ATTACKS, applyAction, chooseEnemyActions, createBattleState, runTurn } from "./battle-engine";
import { arbiterChance, createArbiter } from "./arbiter";
import { partyAtLevel, winRate } from "./balance-helpers";
import { createRng } from "../random";

describe("隠しボス「機械の悪神巨人兵」", () => {
  const party = () => partyAtLevel(80, 5);

  it("出現率は 0.02%、仲間のだれかがレベル80を超えたら 0.2%（2026-10-06 人間の指示）", () => {
    expect(arbiterChance(1)).toBe(0.0002);
    expect(arbiterChance(80)).toBe(0.0002);
    expect(arbiterChance(81)).toBe(0.002);
    expect(arbiterChance(99)).toBe(0.002);
  });

  it("神の調停で、味方全員の体力が半分になる", () => {
    const s = createBattleState(party(), [createArbiter()]);
    const next = applyAction(s, { type: "skill", actorId: "arbiter", targetId: "hero", skill: ARBITER_SKILLS.judgement }, createRng(1));
    for (let i = 0; i < s.party.length; i++) expect(next.party[i].hp).toBe(Math.ceil(s.party[i].hp / 2));
  });

  it("流星の裁きは、しゅびと、ぼうぎょを無視して全員にあたる", () => {
    const s = createBattleState(party(), [createArbiter()]);
    s.party.forEach((c) => (c.guarding = true));
    const next = applyAction(s, { type: "skill", actorId: "arbiter", targetId: "hero", skill: ARBITER_SKILLS.meteor }, createRng(2));
    const base = createArbiter().attack * ARBITER_SKILLS.meteor.powerMultiplier;
    for (let i = 0; i < s.party.length; i++) expect(s.party[i].hp - next.party[i].hp).toBeGreaterThanOrEqual(Math.floor(base * 0.85));
  });

  it("神の祝福で、減ったHPの半分が回復する", () => {
    const s = createBattleState(party(), [{ ...createArbiter(), hp: 1000 }]);
    const next = applyAction(s, { type: "skill", actorId: "arbiter", targetId: "arbiter", skill: ARBITER_SKILLS.blessing }, createRng(3));
    expect(next.enemies[0].hp).toBe(1000 + Math.ceil((createArbiter().maxHp - 1000) / 2));
  });

  it("4回攻撃のターンがある（1ターンに4つの行動）", () => {
    const rng = createRng(4);
    const counts = Array.from({ length: 200 }, () => chooseEnemyActions(createArbiter(), party(), rng).length);
    expect(counts).toContain(ARBITER_ATTACKS);
    const s = runTurn(createBattleState(party(), [createArbiter()]), chooseEnemyActions({ ...createArbiter(), hp: 11000 }, party(), () => 0.99), createRng(5));
    expect(s.log.filter((l) => l.startsWith("機械の悪神巨人兵 の たたかう")).length).toBe(ARBITER_ATTACKS);
  });

  it("強さ: Lv70ではまず勝てず、Lv80で約2割、Lv90で半分以上（剣だけの装備の自動シミュレーション）", () => {
    const at = (lv: number) => winRate(partyAtLevel(lv, 5), () => [createArbiter()], 120).rate;
    const r70 = at(70), r80 = at(80), r90 = at(90);
    expect(r70).toBeLessThan(0.1);
    expect(r80).toBeGreaterThan(0.08);
    expect(r80).toBeLessThan(0.45);
    expect(r90).toBeGreaterThan(0.5);
  });
});
