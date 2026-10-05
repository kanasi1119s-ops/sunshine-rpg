import type { Combatant } from "./types";

/**
 * クリア後ダンジョン「虚灯宮・深部」の敵（`docs/story/secret-boss.md`、roadmap 6-2）。
 * 数値は自動シミュレーション300回（`chapter10-balance.test.ts`）で調整する。
 * ユーリ・レト・ミナ・コハク・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 実際のクリア後は、仲間はもっと育っているはずなので、Lv1想定での勝率は「いちばん厳しい場合」の目安になる。
 */

/** 第3階層の「歪みの残響」。これまでの歪みが一つに溶け合った中ボス（目安の勝率75〜90%）。 */
export function createDeepEchoYugami(): Combatant {
  return {
    id: "deep3-yugami",
    name: "歪みの残響",
    maxHp: 4930,
    hp: 4930,
    maxMp: 0,
    mp: 0,
    attack: 84,
    defense: 28,
    speed: 25,
    isEnemy: true,
    guarding: false,
    expReward: 8546,
  };
}

/** 裏ボス「初源の歪み」（目安の勝率50%前後）。 */
export function createShogenYugami(): Combatant {
  return {
    id: "deep-yugami",
    name: "初源の歪み",
    maxHp: 6306,
    hp: 6306,
    maxMp: 0,
    mp: 0,
    attack: 91,
    defense: 29,
    speed: 26,
    isEnemy: true,
    guarding: false,
    expReward: 9657,
  };
}
