import type { Combatant } from "./types";

/**
 * 第5章のボス「予言の歪み」（`docs/story/structure.md`「第5章（霧断崖）」参照）。
 * 書き換えられた碑文の文字が、霧とともに歪んだもの。
 * 数値は roadmap 4-23 の自動シミュレーション300回（`chapter5-balance.test.ts`）で調整し、勝率約74.7%（目安70〜90%）に収めた。
 * ユーリ・レト・ミナ・ガイド・オルカの5人パーティ（Lv1想定。加入なしの章）を前提に、第4章より強くしてある。
 */
export function createKiriYogenYugami(): Combatant {
  return {
    id: "kiri-yugami",
    name: "予言の歪み",
    maxHp: 270,
    hp: 270,
    maxMp: 0,
    mp: 0,
    attack: 27,
    defense: 11,
    speed: 12,
    isEnemy: true,
    guarding: false,
    expReward: 160,
  };
}
