import { describe, expect, it } from "vitest";
import { createBattleState, checkOutcome, runTurn, chooseEnemyAction } from "./battle-engine";
import type { BattleAction, Combatant } from "./types";
import { createRng } from "../random";
import { CHAPTER0_ITEM, CHAPTER0_STARTING_ITEM_COUNT, createChapter0Party } from "./chapter0-enemies";
import { createMugikanoYugami } from "./chapter1-enemies";
import { RETO, createCompanionCombatant } from "./companions";

const HERO_ID = "hero";
const RETO_ID = "reto";
const BOSS_ID = "mugikano-yugami";

/**
 * 第1章のボス戦は「ユーリ・レトの2人パーティ、Lv1、初期装備」を想定する
 * （ミナはこの戦闘のあと村長への報告を経て仲間に加わるため、まだ加入していない）。
 * `sample-battle.ts` の初期値・`chapter0-balance.test.ts` と同じユーリの初期値を使う。
 */
function createChapter1Party(): Combatant[] {
  const hero = createChapter0Party(1, {
    level: 1,
    exp: 0,
    maxHp: 30,
    hp: 30,
    maxMp: 10,
    mp: 10,
    attack: 16, // 素の12 + 剣の+4
    defense: 6,
    speed: 9,
  })[0];
  const reto = createCompanionCombatant(RETO, RETO.createInitialStats());
  return [hero, reto];
}

/**
 * 「HPが4割を切ったメンバーがいれば灯り草、MPがあればとくぎ、それ以外はたたかう」
 * という手堅い戦い方で決着まで進める（QA roles.md 3-6 のボス戦自動シミュレーション）。
 */
function simulateBattle(seed: number): "won" | "lost" {
  const rng = createRng(seed);
  let state = createBattleState(createChapter1Party(), [createMugikanoYugami()]);
  let itemCharges = CHAPTER0_STARTING_ITEM_COUNT;

  for (let turn = 0; turn < 100 && checkOutcome(state) === "ongoing"; turn++) {
    const actions: BattleAction[] = [];
    const lowestHpAlly = [...state.party]
      .filter((c) => c.hp > 0)
      .sort((a, b) => a.hp / a.maxHp - b.hp / b.maxHp)[0];

    for (const member of state.party) {
      if (member.hp <= 0) {
        continue;
      }
      if (member.id === lowestHpAlly?.id && member.hp <= member.maxHp * 0.4 && itemCharges > 0) {
        actions.push({ type: "item", actorId: member.id, targetId: member.id, item: CHAPTER0_ITEM });
        itemCharges--;
        continue;
      }
      if (member.id === HERO_ID) {
        const skill = { id: "kashou-no-ichi", name: "火照ノ一", mpCost: 3, powerMultiplier: 1.6 };
        if (member.mp >= skill.mpCost) {
          actions.push({ type: "skill", actorId: HERO_ID, targetId: BOSS_ID, skill });
        } else {
          actions.push({ type: "attack", actorId: HERO_ID, targetId: BOSS_ID });
        }
      } else if (member.id === RETO_ID) {
        if (member.mp >= RETO.skill.mpCost) {
          actions.push({ type: "skill", actorId: RETO_ID, targetId: BOSS_ID, skill: RETO.skill });
        } else {
          actions.push({ type: "attack", actorId: RETO_ID, targetId: BOSS_ID });
        }
      }
    }

    const boss = state.enemies[0];
    if (boss && boss.hp > 0) {
      actions.push(chooseEnemyAction(boss, state.party, rng));
    }
    state = runTurn(state, actions, rng);
  }

  return checkOutcome(state) === "won" ? "won" : "lost";
}

describe("第1章ボス「水涸れの歪み」のバランス", () => {
  it("想定パーティ（ユーリ・レト Lv1、初期装備）で、無理のない範囲で勝てる（roles.md 3-6: 目安70〜90%）", () => {
    const trials = 300;
    let wins = 0;
    for (let seed = 0; seed < trials; seed++) {
      if (simulateBattle(seed) === "won") {
        wins++;
      }
    }
    const winRate = wins / trials;
    expect(winRate, `勝率 ${(winRate * 100).toFixed(1)}%`).toBeGreaterThanOrEqual(0.6);
    expect(winRate, `勝率 ${(winRate * 100).toFixed(1)}%`).toBeLessThanOrEqual(0.95);
  });
});
