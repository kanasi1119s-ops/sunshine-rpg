import { createBattleState, checkOutcome, runTurn, chooseEnemyActions } from "./battle-engine";
import type { BattleAction, Combatant } from "./types";
import { createRng } from "../random";
import { CHAPTER0_ITEM, CHAPTER0_SKILL, CHAPTER0_STARTING_ITEM_COUNT, createChapter0Party } from "./chapter0-enemies";
import { COMPANIONS, createCompanionCombatant } from "./companions";
import { createInitialHeroStats, SAMPLE_GROWTH, SAMPLE_WEAPON } from "./sample-battle";
import { statsAtLevel } from "../growth/level-up";

/**
 * バランス調整の自動シミュレーション用の共通部品（QA roles.md 3-6）。
 * 「その章に着く頃の想定レベル」のパーティ（ユーリ＋加入済みの仲間、剣装備、レベル相応の能力値）が、
 * 手堅い戦い方（HPが4割を切ったら灯り草、MPがあればとくぎ、それ以外はたたかう）で戦った結果を数える。
 */

/** 仲間の加入順（本編の順）。 */
export const JOIN_ORDER = ["reto", "mina", "guide", "orca", "ayame"] as const;

/** 想定レベルのユーリ（剣の+4込み）と、加入済みの仲間 `companionCount` 人のパーティ。 */
export function partyAtLevel(level: number, companionCount: number): Combatant[] {
  const heroStats = statsAtLevel(createInitialHeroStats(), SAMPLE_GROWTH, level);
  const party = createChapter0Party(level, { ...heroStats, attack: heroStats.attack + (SAMPLE_WEAPON.statBonus.attack ?? 0) });
  for (const id of JOIN_ORDER.slice(0, companionCount)) {
    const def = COMPANIONS[id];
    party.push(createCompanionCombatant(def, statsAtLevel(def.createInitialStats(), def.growth, level)));
  }
  return party;
}

function skillOf(id: string) {
  return id === "hero" ? CHAPTER0_SKILL : COMPANIONS[id].skill;
}

export interface FightResult {
  won: boolean;
  /** 戦闘後の、味方のHPの合計÷最大HPの合計。 */
  hpRatio: number;
}

/** 1回の戦闘を最後まで進める。敵は先頭の生きている1体を全員で狙う。 */
export function simulateFight(party: Combatant[], enemies: Combatant[], seed: number): FightResult {
  const rng = createRng(seed);
  let state = createBattleState(party.map((c) => ({ ...c })), enemies.map((c) => ({ ...c })));
  let itemCharges = CHAPTER0_STARTING_ITEM_COUNT;
  for (let turn = 0; turn < 100 && checkOutcome(state) === "ongoing"; turn++) {
    const actions: BattleAction[] = [];
    const target = state.enemies.find((e) => e.hp > 0);
    const lowest = [...state.party].filter((c) => c.hp > 0).sort((a, b) => a.hp / a.maxHp - b.hp / b.maxHp)[0];
    for (const member of state.party) {
      if (member.hp <= 0 || !target) {
        continue;
      }
      if (member.id === lowest?.id && member.hp <= member.maxHp * 0.4 && itemCharges > 0) {
        actions.push({ type: "item", actorId: member.id, targetId: member.id, item: CHAPTER0_ITEM });
        itemCharges--;
        continue;
      }
      const skill = skillOf(member.id);
      if (member.mp >= skill.mpCost) {
        actions.push({ type: "skill", actorId: member.id, targetId: target.id, skill });
      } else {
        actions.push({ type: "attack", actorId: member.id, targetId: target.id });
      }
    }
    for (const enemy of state.enemies) {
      if (enemy.hp > 0) {
        actions.push(...chooseEnemyActions(enemy, state.party, rng));
      }
    }
    state = runTurn(state, actions, rng);
  }
  const maxSum = party.reduce((sum, c) => sum + c.maxHp, 0);
  const hpSum = state.party.reduce((sum, c) => sum + Math.max(0, c.hp), 0);
  return { won: checkOutcome(state) === "won", hpRatio: hpSum / maxSum };
}

export function winRate(party: Combatant[], makeEnemies: () => Combatant[], trials = 300): { rate: number; hpRatio: number } {
  let wins = 0;
  let hp = 0;
  for (let seed = 0; seed < trials; seed++) {
    const result = simulateFight(party, makeEnemies(), seed);
    if (result.won) {
      wins++;
      hp += result.hpRatio;
    }
  }
  return { rate: wins / trials, hpRatio: wins > 0 ? hp / wins : 0 };
}
