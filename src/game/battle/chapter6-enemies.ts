import type { Combatant } from "./types";

/**
 * 第6章のボス「試作機の歪み」（`docs/story/structure.md`「第6章（霜原）」参照）。
 * 戦跡の下の施設で、ドルンが起動した発生装置の試作機が暴走して歪んだもの。
 * 数値は roadmap 4-28 の自動シミュレーション300回（`chapter6-balance.test.ts`）で調整し、勝率約72.3%（目安70〜90%）に収めた。
 * ユーリ・レト・ミナ・ガイド・オルカの5人パーティ（Lv1想定）を前提にする。
 * 【2026-09-30 再調整】想定レベルLv15の仲間つきパーティに対する勝率が目安になるよう、体力・攻撃・防御・素早さ・経験値を作り直した（`boss-balance.test.ts`）。
 * アヤメは戦闘の後に加入するため、この戦いには参加しない。
 */
export function createShimoharaShisakukiYugami(): Combatant {
  return {
    id: "shimohara-yugami",
    name: "試作機の歪み",
    maxHp: 2506,
    hp: 2506,
    maxMp: 0,
    mp: 0,
    attack: 62,
    defense: 21,
    speed: 20,
    isEnemy: true,
    guarding: false,
    expReward: 4578,
  };
}
