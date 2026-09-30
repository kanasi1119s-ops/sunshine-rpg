import type { Combatant } from "./types";

/**
 * 第7章のボス「監視卓の歪み」（`docs/story/structure.md`「第7章（浮嶼）」参照）。
 * 浮島の裏の隠れ拠点で、大陸中の歪みを見張っていた監視卓が、調べた拍子に暴走して歪んだもの。
 * 数値は roadmap 4-33 の自動シミュレーション300回（`chapter7-balance.test.ts`）で調整し、勝率約72.0%（目安70〜90%）に収めた。
 * ユーリ・レト・ミナ・ガイド・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 */
export function createFushimaKanshitakuYugami(): Combatant {
  return {
    id: "fushima-yugami",
    name: "監視卓の歪み",
    maxHp: 310,
    hp: 310,
    maxMp: 0,
    mp: 0,
    attack: 28,
    defense: 12,
    speed: 13,
    isEnemy: true,
    guarding: false,
    expReward: 220,
  };
}
