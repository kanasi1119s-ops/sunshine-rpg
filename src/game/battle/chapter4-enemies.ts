import type { Combatant } from "./types";

/**
 * 第4章のボス「砂嵐の歪み」（`docs/story/structure.md`「第4章（砂音）」参照）。
 * 隊商の野営地で、ドルンが荷に混ぜた灯り石が砂を巻き込んで歪んだもの。
 * 数値は roadmap 4-18 の自動シミュレーション（`chapter4-balance.test.ts`）で調整した。
 * ユーリ・レト・ミナ・ガイド・オルカの5人パーティ（Lv1想定）を前提に、第3章より強くしてある。
 */
export function createSanoneSunaarashiYugami(): Combatant {
  return {
    id: "sanone-yugami",
    name: "砂嵐の歪み",
    maxHp: 260,
    hp: 260,
    maxMp: 0,
    mp: 0,
    attack: 27,
    defense: 11,
    speed: 12,
    isEnemy: true,
    guarding: false,
    expReward: 150,
  };
}
