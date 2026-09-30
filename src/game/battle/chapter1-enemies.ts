import type { Combatant } from "./types";

/**
 * 第1章のボス「水涸れの歪み」（`docs/story/mystery.md`、
 * `docs/story/clue-ledger.md` C-002参照）。麦香野の水源、古い灯り石の
 * 採掘跡で対峙する。序章のボスよりやや強い（パーティが2人に増えているため）。
 */
export function createMugikanoYugami(): Combatant {
  return {
    id: "mugikano-yugami",
    name: "水涸れの歪み",
    maxHp: 179,
    hp: 179,
    maxMp: 0,
    mp: 0,
    attack: 32,
    defense: 12,
    speed: 14,
    isEnemy: true,
    guarding: false,
    expReward: 968,
  };
}
