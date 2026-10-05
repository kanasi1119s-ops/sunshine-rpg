import type { Combatant } from "./types";

/**
 * 第7章のボス「監視卓の歪み」（`docs/story/structure.md`「第7章（浮嶼）」参照）。
 * 浮島の裏の隠れ拠点で、大陸中の歪みを見張っていた監視卓が、調べた拍子に暴走して歪んだもの。
 * 数値は roadmap 4-33 の自動シミュレーション300回（`chapter7-balance.test.ts`）で調整し、勝率約72.0%（目安70〜90%）に収めた。
 * ユーリ・レト・ミナ・コハク・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 【2026-09-30 再調整】想定レベルLv17の仲間つきパーティに対する勝率が目安になるよう、体力・攻撃・防御・素早さ・経験値を作り直した（`boss-balance.test.ts`）。
 */
export function createFushimaKanshitakuYugami(): Combatant {
  return {
    id: "fushima-yugami",
    name: "監視卓の歪み",
    maxHp: 4117,
    hp: 4117,
    maxMp: 0,
    mp: 0,
    attack: 66,
    defense: 22,
    speed: 21,
    isEnemy: true,
    guarding: false,
    expReward: 5492,
  };
}
