import type { Combatant } from "./types";

/**
 * 第6章のボス「試作機の歪み」（`docs/story/structure.md`「第6章（霜原）」参照）。
 * 戦跡の下の施設で、ドルンが起動した発生装置の試作機が暴走して歪んだもの。
 * 数値は roadmap 4-28 の自動シミュレーション300回（`chapter6-balance.test.ts`）で調整し、勝率約72.3%（目安70〜90%）に収めた。
 * ユーリ・レト・ミナ・ガイド・オルカの5人パーティ（Lv1想定）を前提にする。
 * アヤメは戦闘の後に加入するため、この戦いには参加しない。
 */
export function createShimoharaShisakukiYugami(): Combatant {
  return {
    id: "shimohara-yugami",
    name: "試作機の歪み",
    maxHp: 275,
    hp: 275,
    maxMp: 0,
    mp: 0,
    attack: 27,
    defense: 11,
    speed: 12,
    isEnemy: true,
    guarding: false,
    expReward: 190,
  };
}
