import type { Combatant } from "./types";

/**
 * 第8章のボス「灯芯都の番人の歪み」（`docs/story/structure.md`「第8章（灯芯都）」参照）。
 * 追い詰められたエドレアが、合議会堂の床に仕込んでいた発生装置を起動して呼び出した番人が、歪んだもの。
 * 数値は roadmap 4-38 の自動シミュレーション300回（`chapter8-balance.test.ts`）で調整する（目安70〜90%）。
 * ユーリ・レト・ミナ・ガイド・オルカ・アヤメの6人パーティ（Lv1想定）を前提にする。
 */
export function createToushinBanninYugami(): Combatant {
  return {
    id: "toushin-yugami",
    name: "灯芯都の番人の歪み",
    maxHp: 310,
    hp: 310,
    maxMp: 0,
    mp: 0,
    attack: 28,
    defense: 12,
    speed: 13,
    isEnemy: true,
    guarding: false,
    expReward: 240,
  };
}
