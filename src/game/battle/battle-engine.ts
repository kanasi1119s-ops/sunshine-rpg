import { computeDamage, computeFleeChance } from "./formulas";
import type { BattleAction, BattleState, Combatant, Skill } from "./types";
import { findCombatant, isAlive } from "./types";

export function createBattleState(party: Combatant[], enemies: Combatant[]): BattleState {
  return {
    party: party.map((c) => ({ ...c, guarding: false })),
    enemies: enemies.map((c) => ({ ...c, guarding: false })),
    log: [],
    fled: false,
  };
}

export type BattleOutcome = "won" | "lost" | "fled" | "ongoing";

export function checkOutcome(state: BattleState): BattleOutcome {
  if (state.fled) {
    return "fled";
  }
  if (state.party.every((c) => !isAlive(c))) {
    return "lost";
  }
  if (state.enemies.every((c) => !isAlive(c))) {
    return "won";
  }
  return "ongoing";
}

/** すばやさが高い順に並べる。行動不能（戦闘不能）は除く。同速は乱数で決める。 */
export function resolveTurnOrder(combatants: Combatant[], rng: () => number): Combatant[] {
  return [...combatants]
    .filter(isAlive)
    .map((c) => ({ c, tiebreak: rng() }))
    .sort((a, b) => b.c.speed - a.c.speed || b.tiebreak - a.tiebreak)
    .map(({ c }) => c);
}

function averageSpeed(combatants: Combatant[]): number {
  const alive = combatants.filter(isAlive);
  if (alive.length === 0) {
    return 0;
  }
  return alive.reduce((sum, c) => sum + c.speed, 0) / alive.length;
}

/** 1体にダメージを与え、ログに書く（防御中は半分）。倒したらそのログも書く。 */
function dealDamage(next: BattleState, actor: Combatant, target: Combatant, skillName: string, powerMultiplier: number, rng: () => number): void {
  const { amount, critical } = computeDamage(actor.attack, target.defense, powerMultiplier, rng);
  const finalAmount = target.guarding ? Math.ceil(amount / 2) : amount;
  target.hp = Math.max(0, target.hp - finalAmount);
  next.log.push(`${actor.name} の ${skillName}！ ${critical ? "会心の一撃！ " : ""}${target.name} に ${finalAmount} のダメージ`);
  if (!isAlive(target)) {
    next.log.push(`${target.name} を倒した！`);
  }
}

/** 味方のHPを回復し、ログに書く。 */
function healOne(next: BattleState, actor: Combatant, target: Combatant, skill: Skill): void {
  const amount = Math.max(1, Math.round(actor.attack * (skill.healRatio ?? 1)));
  const before = target.hp;
  target.hp = Math.min(target.maxHp, target.hp + amount);
  next.log.push(`${actor.name} の ${skill.name}！ ${target.name} のHPが ${target.hp - before} 回復した`);
}

/** 効果つきの特技（複数回・敵全体・回復）を適用する。MPが足りない・対象がいないときは何も起きない。 */
function applyEffectSkill(next: BattleState, actor: Combatant, skill: Skill, targetId: string, rng: () => number): BattleState {
  const allies = actor.isEnemy ? next.enemies : next.party;
  const foes = actor.isEnemy ? next.party : next.enemies;
  if (actor.mp < skill.mpCost) {
    next.log.push(`${actor.name} はMPが足りず ${skill.name} を使えなかった`);
    return next;
  }
  switch (skill.effect) {
    case "multi": {
      const target = findCombatant(next, targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      actor.mp -= skill.mpCost;
      for (let i = 0; i < (skill.hits ?? 2) && isAlive(target); i++) {
        dealDamage(next, actor, target, skill.name, skill.powerMultiplier, rng);
      }
      return next;
    }
    case "damageAll": {
      actor.mp -= skill.mpCost;
      for (const foe of foes.filter(isAlive)) {
        dealDamage(next, actor, foe, skill.name, skill.powerMultiplier, rng);
      }
      return next;
    }
    case "heal": {
      const target = allies.find((c) => c.id === targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      actor.mp -= skill.mpCost;
      healOne(next, actor, target, skill);
      return next;
    }
    case "healAll": {
      actor.mp -= skill.mpCost;
      for (const ally of allies.filter(isAlive)) {
        healOne(next, actor, ally, skill);
      }
      return next;
    }
    default:
      return next;
  }
}

/** 1つの行動を適用し、更新後の状態を返す（元の状態は変更しない）。 */
export function applyAction(state: BattleState, action: BattleAction, rng: () => number): BattleState {
  const actor = findCombatant(state, action.actorId);
  if (!actor || !isAlive(actor)) {
    return state;
  }

  const next: BattleState = {
    party: state.party.map((c) => ({ ...c })),
    enemies: state.enemies.map((c) => ({ ...c })),
    log: [...state.log],
    fled: state.fled,
  };
  const nextActor = findCombatant(next, action.actorId)!;

  switch (action.type) {
    case "attack":
    case "skill": {
      if (action.type === "skill" && action.skill.effect) {
        return applyEffectSkill(next, nextActor, action.skill, action.targetId, rng);
      }
      const target = findCombatant(next, action.targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      const powerMultiplier = action.type === "skill" ? action.skill.powerMultiplier : 1;
      if (action.type === "skill") {
        if (nextActor.mp < action.skill.mpCost) {
          next.log.push(`${nextActor.name} はMPが足りず ${action.skill.name} を使えなかった`);
          return next;
        }
        nextActor.mp -= action.skill.mpCost;
      }
      const { amount, critical } = computeDamage(
        nextActor.attack,
        target.defense,
        powerMultiplier,
        rng,
      );
      const finalAmount = target.guarding ? Math.ceil(amount / 2) : amount;
      target.hp = Math.max(0, target.hp - finalAmount);
      const skillName = action.type === "skill" ? action.skill.name : "たたかう";
      const criticalNote = critical ? "会心の一撃！ " : "";
      next.log.push(
        `${nextActor.name} の ${skillName}！ ${criticalNote}${target.name} に ${finalAmount} のダメージ`,
      );
      if (!isAlive(target)) {
        next.log.push(`${target.name} を倒した！`);
      }
      return next;
    }

    case "item": {
      const target = findCombatant(next, action.targetId);
      if (!target) {
        return next;
      }
      target.hp = Math.min(target.maxHp, target.hp + action.item.healAmount);
      next.log.push(`${nextActor.name} は ${action.item.name} を使った。${target.name} のHPが回復した`);
      return next;
    }

    case "defend": {
      nextActor.guarding = true;
      next.log.push(`${nextActor.name} は身を守っている`);
      return next;
    }

    case "flee": {
      const chance = computeFleeChance(averageSpeed(next.party), averageSpeed(next.enemies));
      if (rng() < chance) {
        next.fled = true;
        next.log.push("うまく逃げ切った！");
      } else {
        next.log.push("しかし逃げられなかった！");
      }
      return next;
    }
  }
}

/**
 * 1ターン分（全員の行動）をまとめて処理する。
 * すばやさ順に並べ、途中で決着がついたら残りの行動は行わない。
 */
export function runTurn(
  state: BattleState,
  actions: BattleAction[],
  rng: () => number,
): BattleState {
  let current: BattleState = {
    party: state.party.map((c) => ({ ...c, guarding: false })),
    enemies: state.enemies.map((c) => ({ ...c, guarding: false })),
    log: [...state.log],
    fled: state.fled,
  };

  const actors = [...current.party, ...current.enemies];
  const order = resolveTurnOrder(actors, rng);

  for (const combatant of order) {
    if (checkOutcome(current) !== "ongoing") {
      break;
    }
    const action = actions.find((a) => a.actorId === combatant.id);
    if (!action) {
      continue;
    }
    const livingActor = findCombatant(current, combatant.id);
    if (!livingActor || !isAlive(livingActor)) {
      continue;
    }
    current = applyAction(current, action, rng);
  }

  return current;
}

/** 勝利時に入手する経験値の合計（倒した敵の経験値をすべて合算する）。 */
export function computeVictoryExp(state: BattleState): number {
  return state.enemies.reduce((sum, enemy) => sum + (enemy.expReward ?? 0), 0);
}

/** 生きている敵の中からランダムに1体を狙う、簡単な敵AI。 */
export function chooseEnemyAction(enemy: Combatant, party: Combatant[], rng: () => number): BattleAction {
  const aliveParty = party.filter(isAlive);
  const target = aliveParty[Math.floor(rng() * aliveParty.length)] ?? party[0];
  return { type: "attack", actorId: enemy.id, targetId: target.id };
}
