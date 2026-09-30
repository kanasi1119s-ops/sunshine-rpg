import type { Combatant } from "./types";

/**
 * クリア後ダンジョン「虚灯宮・深部」の敵（`docs/story/secret-boss.md`、roadmap 6-2）。
 * 数値は自動シミュレーション300回（`chapter10-balance.test.ts`）で調整する。
 * ユーリ・レト・ミナ・ガイド・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 実際のクリア後は、仲間はもっと育っているはずなので、Lv1想定での勝率は「いちばん厳しい場合」の目安になる。
 */

/** 第3階層の「歪みの残響」。これまでの歪みが一つに溶け合った中ボス（目安の勝率75〜90%）。 */
export function createDeepEchoYugami(): Combatant {
  return {
    id: "deep3-yugami",
    name: "歪みの残響",
    maxHp: 302,
    hp: 302,
    maxMp: 0,
    mp: 0,
    attack: 27,
    defense: 12,
    speed: 13,
    isEnemy: true,
    guarding: false,
    expReward: 300,
  };
}

/** 裏ボス「初源の歪み」（目安の勝率50%前後）。 */
export function createShogenYugami(): Combatant {
  return {
    id: "deep-yugami",
    name: "初源の歪み",
    maxHp: 320,
    hp: 320,
    maxMp: 0,
    mp: 0,
    attack: 29,
    defense: 12,
    speed: 14,
    isEnemy: true,
    guarding: false,
    expReward: 800,
  };
}
