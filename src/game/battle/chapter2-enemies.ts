import type { Combatant } from "./types";

/**
 * 第2章のボス「積荷の歪み」（`docs/story/mystery.md`、
 * `docs/story/clue-ledger.md` C-003・C-004参照）。硝子湖の密輸倉庫、
 * 積み上げられた大量の灯り石が反応して生まれる。数値はroadmap 4-8の
 * バランス調整（自動シミュレーション300回、勝率約84.7%）で確定した。
 * ユーリ・レト・ミナの3人パーティを想定し、第1章のボスよりやや強くしてある。
 */
export function createGarasukoYugami(): Combatant {
  return {
    id: "garasuko-yugami",
    name: "積荷の歪み",
    maxHp: 155,
    hp: 155,
    maxMp: 0,
    mp: 0,
    attack: 24,
    defense: 9,
    speed: 10,
    isEnemy: true,
    guarding: false,
    expReward: 95,
  };
}
