import { allyLuck } from "./luck";
import type { BattleItem, Combatant, Skill } from "./types";
import type { LeveledStats } from "../growth/types";

/**
 * 戦闘に出ているときのユーリ（装備ボーナス込みの実力を effectiveStats で渡す。
 * 表示名のレベルは基本能力値=heroLevel を使う。`sample-battle.ts` の createSampleParty と同じ形）。
 */
export function createChapter0Party(heroLevel: number, effectiveStats: LeveledStats): Combatant[] {
  return [
    {
      id: "hero",
      name: `ユーリ Lv${heroLevel}`,
      maxHp: effectiveStats.maxHp,
      hp: effectiveStats.hp,
      maxMp: effectiveStats.maxMp,
      mp: effectiveStats.mp,
      attack: effectiveStats.attack,
      defense: effectiveStats.defense,
      speed: effectiveStats.speed,
      luck: allyLuck("hero", heroLevel),
      isEnemy: false,
      guarding: false,
    },
  ];
}

/**
 * 序章のボス「灯里の歪み」（`docs/story/mystery.md` 序章の項、
 * `docs/story/clue-ledger.md` C-001参照）。序章唯一の敵で、
 * 事件の調査の最後に町外れで対峙する。
 */
export function createYugamiBoss(): Combatant {
  return {
    id: "chapter0-yugami",
    name: "灯里の歪み",
    maxHp: 66,
    hp: 66,
    maxMp: 0,
    mp: 0,
    attack: 15,
    defense: 4,
    speed: 7,
    isEnemy: true,
    guarding: false,
    expReward: 45,
  };
}

/** ユーリの共鳴術（火照系）の初級呪文。呪文名は「系統名＋効果を表す和語」（`docs/story/bible.md` 4）。 */
export const CHAPTER0_SKILL: Skill = { id: "kashou-no-ichi", name: "火照ノ一", mpCost: 3, powerMultiplier: 1.6 };

/** 灯り石の力を吸った薬草。既存作の回復アイテム名は使わない（CLAUDE.md 1-1）。 */
export const CHAPTER0_ITEM: BattleItem = { id: "akarigusa", name: "灯り草", healAmount: 20 };

/** 序章開始時に持っている灯り草の数。 */
export const CHAPTER0_STARTING_ITEM_COUNT = 2;
