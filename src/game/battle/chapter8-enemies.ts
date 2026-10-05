import type { Combatant } from "./types";

/**
 * 第8章のボス「灯芯都の番人の歪み」（`docs/story/structure.md`「第8章（灯芯都）」参照）。
 * 追い詰められたエドレアが、合議会堂の床に仕込んでいた発生装置を起動して呼び出した番人が、歪んだもの。
 * 数値は roadmap 4-38 の自動シミュレーション300回（`chapter8-balance.test.ts`）で調整する（目安70〜90%）。
 * ユーリ・レト・ミナ・コハク・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 * 【2026-09-30 再調整】想定レベルLv19の仲間つきパーティに対する勝率が目安になるよう、体力・攻撃・防御・素早さ・経験値を作り直した（`boss-balance.test.ts`）。
 */
export function createToushinBanninYugami(): Combatant {
  return {
    id: "toushin-yugami",
    name: "灯芯都の番人の歪み",
    maxHp: 4560,
    hp: 4560,
    maxMp: 0,
    mp: 0,
    attack: 72,
    defense: 24,
    speed: 22,
    isEnemy: true,
    guarding: false,
    expReward: 6459,
  };
}
