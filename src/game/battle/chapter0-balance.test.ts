import { describe, expect, it } from "vitest";
import { createBattleState, checkOutcome, runTurn, chooseEnemyAction } from "./battle-engine";
import type { BattleAction } from "./types";
import { createRng } from "../random";
import {
  CHAPTER0_ITEM,
  CHAPTER0_SKILL,
  CHAPTER0_STARTING_ITEM_COUNT,
  createChapter0Party,
  createYugamiBoss,
} from "./chapter0-enemies";

const HERO_ID = "hero";
const BOSS_ID = "chapter0-yugami";

/** 序章クリア時点を想定した、レベル1・剣装備込みのユーリ。`sample-battle.ts` の初期値と同じ。 */
function createChapter0Hero() {
  return createChapter0Party(1, {
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
}

/**
 * 「HPが4割を切ったら灯り草、MPがあれば火照ノ一、それ以外はたたかう」という
 * 手堅い戦い方で決着まで進める（QA roles.md 3-6 のボス戦自動シミュレーション）。
 */
function simulateBattle(seed: number): "won" | "lost" {
  const rng = createRng(seed);
  let state = createBattleState([createChapter0Hero()], [createYugamiBoss()]);
  let itemCharges = CHAPTER0_STARTING_ITEM_COUNT;

  for (let turn = 0; turn < 100 && checkOutcome(state) === "ongoing"; turn++) {
    const hero = state.party[0];
    const boss = state.enemies[0];

    let heroAction: BattleAction;
    if (hero.hp <= hero.maxHp * 0.4 && itemCharges > 0) {
      heroAction = { type: "item", actorId: HERO_ID, targetId: HERO_ID, item: CHAPTER0_ITEM };
      itemCharges--;
    } else if (hero.mp >= CHAPTER0_SKILL.mpCost) {
      heroAction = { type: "skill", actorId: HERO_ID, targetId: BOSS_ID, skill: CHAPTER0_SKILL };
    } else {
      heroAction = { type: "attack", actorId: HERO_ID, targetId: BOSS_ID };
    }

    const bossAction = chooseEnemyAction(boss, state.party, rng);
    state = runTurn(state, [heroAction, bossAction], rng);
  }

  return checkOutcome(state) === "won" ? "won" : "lost";
}

describe("序章ボス「灯里の歪み」のバランス", () => {
  it("想定レベル（Lv1・初期装備）で、無理のない範囲で勝てる（roles.md 3-6: 目安70〜90%）", () => {
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
