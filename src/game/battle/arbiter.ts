import type { Combatant } from "./types";

/**
 * 隠しボス「機械の悪神巨人兵」（世界の調停者。2026-10-06、人間の指示）。
 * 全体フィールド（世界地図）で、出会いのうち 0.01% で現れる。推定レベル80（パーティの想定レベル80で、勝てるか勝てないかの強さ）。
 * 1ターンに、4回攻撃・流星の裁き（全体・防御無視）・神の調停（全員の体力を半分に）・神の祝福（減ったHPの半分を回復）のどれか1つ。
 * 数値は自動シミュレーション（`arbiter.test.ts`、Lv80の6人・剣だけの装備）で、勝率が Lv70 でほぼ0、Lv80 で約2割、Lv90 で約7割になるように決めた（実際は防具・回復があるので、もう少し勝ちやすい）。
 * 倒すと、レジェンドの装備「コスモ」（だれでも装備できる、鎧の形の武器。中身は仮）を手に入れる。
 */
export const ARBITER_ID = "arbiter";
export const ARBITER_NAME = "機械の悪神巨人兵";
/** 世界地図の出会い1回あたりの、現れる確率（0.01%）。 */
export const ARBITER_CHANCE = 0.0001;

export const ARBITER_STATS = { maxHp: 10000, maxMp: 360, attack: 175, defense: 85, speed: 120, expReward: 60000 };

export function createArbiter(): Combatant {
  return {
    id: ARBITER_ID,
    name: ARBITER_NAME,
    maxHp: ARBITER_STATS.maxHp,
    hp: ARBITER_STATS.maxHp,
    maxMp: ARBITER_STATS.maxMp,
    mp: ARBITER_STATS.maxMp,
    attack: ARBITER_STATS.attack,
    defense: ARBITER_STATS.defense,
    speed: ARBITER_STATS.speed,
    luck: 20,
    isEnemy: true,
    guarding: false,
    expReward: ARBITER_STATS.expReward,
    guards: ["poison", "sleep", "confuse"],
    ai: "arbiter",
  };
}
