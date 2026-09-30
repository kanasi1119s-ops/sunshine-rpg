import type { Combatant } from "./types";

/**
 * 第3章のボス「実験の歪み」（`docs/story/mystery.md`、
 * `docs/story/clue-ledger.md` C-006・C-007参照）。鉄鏈鉱山の奥で、
 * 人為的に歪みを作る実験装置が暴走して生まれる。数値はroadmap 4-13の
 * バランス調整（自動シミュレーション300回、勝率約83.7%）で確定した。
 * ユーリ・レト・ミナ・ガイドの4人パーティを想定し、第2章のボスよりやや強くしてある。
 */
export function createTetsukusariYugami(): Combatant {
  return {
    id: "tetsukusari-yugami",
    name: "実験の歪み",
    maxHp: 1112,
    hp: 1112,
    maxMp: 0,
    mp: 0,
    attack: 40,
    defense: 16,
    speed: 16,
    isEnemy: true,
    guarding: false,
    expReward: 2196,
  };
}
