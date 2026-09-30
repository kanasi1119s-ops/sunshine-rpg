import { describe, expect, it } from "vitest";
import { createBattleState, checkOutcome, runTurn, chooseEnemyAction } from "./battle-engine";
import type { BattleAction, Combatant } from "./types";
import { createRng } from "../random";
import { CHAPTER0_ITEM, CHAPTER0_STARTING_ITEM_COUNT, createChapter0Party } from "./chapter0-enemies";
import { createDungeonEnemy, DUNGEON_ENEMIES } from "./chapter12-enemies";
import { RETO, MINA, GUIDE, ORCA, AYAME, createCompanionCombatant } from "./companions";

const HERO_ID = "hero";
const RETO_ID = "reto";
const MINA_ID = "mina";
const GUIDE_ID = "guide";
const ORCA_ID = "orca";
const AYAME_ID = "ayame";


/**
 * 終章のボス戦は「ユーリ・レト・ミナ・ガイド・オルカ・アヤメの6人パーティ、Lv1、初期装備」を想定する
 * （アヤメは第6章で加入済み）。
 * 序章・第1章のバランステストと同じ想定条件（Lv1・初期装備）にそろえ、比較しやすくする。
 */
function createChapter9Party(): Combatant[] {
  const hero = createChapter0Party(1, {
    level: 1,
    exp: 0,
    maxHp: 30,
    hp: 30,
    maxMp: 10,
    mp: 10,
    attack: 16, // 素の12 + 剣の+4
    defense: 6,
    speed: 9,
  })[0];
  const reto = createCompanionCombatant(RETO, RETO.createInitialStats());
  const mina = createCompanionCombatant(MINA, MINA.createInitialStats());
  const guide = createCompanionCombatant(GUIDE, GUIDE.createInitialStats());
  const orca = createCompanionCombatant(ORCA, ORCA.createInitialStats());
  const ayame = createCompanionCombatant(AYAME, AYAME.createInitialStats());
  return [hero, reto, mina, guide, orca, ayame];
}

/**
 * 「HPが4割を切ったメンバーがいれば灯り草、MPがあればとくぎ、それ以外はたたかう」
 * という手堅い戦い方で決着まで進める（QA roles.md 3-6 のボス戦自動シミュレーション）。
 */
function simulateBattle(seed: number, makeBoss: () => Combatant, BOSS_ID: string): "won" | "lost" {
  const rng = createRng(seed);
  let state = createBattleState(createChapter9Party(), [makeBoss()]);
  let itemCharges = CHAPTER0_STARTING_ITEM_COUNT;

  for (let turn = 0; turn < 100 && checkOutcome(state) === "ongoing"; turn++) {
    const actions: BattleAction[] = [];
    const lowestHpAlly = [...state.party]
      .filter((c) => c.hp > 0)
      .sort((a, b) => a.hp / a.maxHp - b.hp / b.maxHp)[0];

    for (const member of state.party) {
      if (member.hp <= 0) {
        continue;
      }
      if (member.id === lowestHpAlly?.id && member.hp <= member.maxHp * 0.4 && itemCharges > 0) {
        actions.push({ type: "item", actorId: member.id, targetId: member.id, item: CHAPTER0_ITEM });
        itemCharges--;
        continue;
      }
      if (member.id === HERO_ID) {
        const skill = { id: "kashou-no-ichi", name: "火照ノ一", mpCost: 3, powerMultiplier: 1.6 };
        if (member.mp >= skill.mpCost) {
          actions.push({ type: "skill", actorId: HERO_ID, targetId: BOSS_ID, skill });
        } else {
          actions.push({ type: "attack", actorId: HERO_ID, targetId: BOSS_ID });
        }
      } else if (member.id === RETO_ID) {
        if (member.mp >= RETO.skill.mpCost) {
          actions.push({ type: "skill", actorId: RETO_ID, targetId: BOSS_ID, skill: RETO.skill });
        } else {
          actions.push({ type: "attack", actorId: RETO_ID, targetId: BOSS_ID });
        }
      } else if (member.id === MINA_ID) {
        if (member.mp >= MINA.skill.mpCost) {
          actions.push({ type: "skill", actorId: MINA_ID, targetId: BOSS_ID, skill: MINA.skill });
        } else {
          actions.push({ type: "attack", actorId: MINA_ID, targetId: BOSS_ID });
        }
      } else if (member.id === GUIDE_ID) {
        if (member.mp >= GUIDE.skill.mpCost) {
          actions.push({ type: "skill", actorId: GUIDE_ID, targetId: BOSS_ID, skill: GUIDE.skill });
        } else {
          actions.push({ type: "attack", actorId: GUIDE_ID, targetId: BOSS_ID });
        }
      } else if (member.id === ORCA_ID) {
        if (member.mp >= ORCA.skill.mpCost) {
          actions.push({ type: "skill", actorId: ORCA_ID, targetId: BOSS_ID, skill: ORCA.skill });
        } else {
          actions.push({ type: "attack", actorId: ORCA_ID, targetId: BOSS_ID });
        }
      } else if (member.id === AYAME_ID) {
        if (member.mp >= AYAME.skill.mpCost) {
          actions.push({ type: "skill", actorId: AYAME_ID, targetId: BOSS_ID, skill: AYAME.skill });
        } else {
          actions.push({ type: "attack", actorId: AYAME_ID, targetId: BOSS_ID });
        }
      }
    }

    const boss = state.enemies[0];
    if (boss && boss.hp > 0) {
      actions.push(chooseEnemyAction(boss, state.party, rng));
    }
    state = runTurn(state, actions, rng);
  }

  return checkOutcome(state) === "won" ? "won" : "lost";
}

function winRate(makeBoss: () => Combatant, bossId: string): number {
  const trials = 300;
  let wins = 0;
  for (let seed = 0; seed < trials; seed++) {
    if (simulateBattle(seed, makeBoss, bossId) === "won") {
      wins++;
    }
  }
  return wins / trials;
}

const TARGET: Record<string, [number, number]> = {
  "tower2-guard": [0.65, 0.95],
  "tower3-guard": [0.5, 0.8],
  "kanou3-guard": [0.5, 0.8],
  "zenkan": [0.25, 0.55],
};

describe("芯環塔・環奥の敵のバランス（Lv1・初期装備の6人パーティ）", () => {
  for (const enemy of DUNGEON_ENEMIES) {
    it(`${enemy.name}`, () => {
      const rate = winRate(() => createDungeonEnemy(enemy), enemy.id);
      const [lo, hi] = TARGET[enemy.id];
      expect(rate, `勝率 ${(rate * 100).toFixed(1)}%`).toBeGreaterThanOrEqual(lo);
      expect(rate, `勝率 ${(rate * 100).toFixed(1)}%`).toBeLessThanOrEqual(hi);
    });
  }
});
