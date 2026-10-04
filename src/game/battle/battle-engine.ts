import { computeDamage, computeFleeChance } from "./formulas";
import type { BattleAction, BattleState, Combatant, Skill } from "./types";
import { effectiveStat, findCombatant, isAlive, STAT_LABELS } from "./types";

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
    .sort((a, b) => effectiveStat(b.c, "speed") - effectiveStat(a.c, "speed") || b.tiebreak - a.tiebreak)
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
  const { amount, critical } = computeDamage(effectiveStat(actor, "attack"), effectiveStat(target, "defense"), powerMultiplier, rng);
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

/** 能力の強化・弱体をかけ、ログに書く。同じ能力にかけ直すと、上書きする。 */
function applyMod(next: BattleState, actor: Combatant, target: Combatant, skill: Skill): void {
  const stat = skill.stat ?? "attack";
  const mult = skill.mult ?? 1.3;
  target.mods = { ...target.mods, [stat]: { mult, turns: skill.turns ?? 3 } };
  next.log.push(`${actor.name} の ${skill.name}！ ${target.name} の${STAT_LABELS[stat]}が${mult >= 1 ? "上がった" : "下がった"}`);
}

/** ターンの終わりに、強化・弱体と眠りの残りターンを1ずつ減らす（0になったら消える）。 */
function tickStatuses(state: BattleState): void {
  for (const c of [...state.party, ...state.enemies]) {
    if (c.mods) {
      const mods: NonNullable<Combatant["mods"]> = {};
      for (const [key, mod] of Object.entries(c.mods) as [keyof typeof STAT_LABELS, { mult: number; turns: number }][]) {
        if (mod.turns > 1) {
          mods[key] = { mult: mod.mult, turns: mod.turns - 1 };
        }
      }
      c.mods = Object.keys(mods).length > 0 ? mods : undefined;
    }
    if (c.sleep) {
      c.sleep = c.sleep > 1 ? c.sleep - 1 : undefined;
    }
    if (c.confused) {
      c.confused = c.confused > 1 ? c.confused - 1 : undefined;
    }
    if (c.poison && isAlive(c)) {
      const dmg = Math.max(1, Math.round(c.maxHp * 0.06));
      const lost = Math.min(dmg, Math.max(0, c.hp - 1));
      c.hp -= lost;
      state.log.push(`${c.name} は毒のダメージを受けた（${lost}）`);
      c.poison = c.poison > 1 ? c.poison - 1 : undefined;
      if (!c.poison) state.log.push(`${c.name} の毒が消えた`);
    }
  }
}

/** 状態異常をかける（かかったかどうかを返し、ログに書く）。 */
function inflict(next: BattleState, actorName: string, target: Combatant, status: "poison" | "sleep" | "confuse", turns: number, prefix: string): boolean {
  if (status === "poison") {
    target.poison = turns;
    next.log.push(`${prefix}${target.name} は毒におかされた！`);
  } else if (status === "sleep") {
    target.sleep = turns;
    next.log.push(`${prefix}${target.name} は眠ってしまった`);
  } else {
    target.confused = turns;
    next.log.push(`${prefix}${target.name} は混乱した！`);
  }
  void actorName;
  return true;
}

/**
 * ねらった敵がすでに倒れていたら、同じ側の、生きているつぎの1体に自動でねらいをかえる（ターゲットを倒したあと、
 * 同じターンの味方の行動がむだにならない）。味方をねらう行動（回復・強化・蘇生）は、そのまま。
 */
function retarget(next: BattleState, actor: Combatant, targetId: string): string {
  const foes = actor.isEnemy ? next.party : next.enemies;
  const original = foes.find((c) => c.id === targetId);
  if (!original || isAlive(original)) {
    return targetId;
  }
  return foes.find(isAlive)?.id ?? targetId;
}

/** 効果つきの特技（複数回・敵全体・回復・強化・弱体・眠り）を適用する。MPが足りない・対象がいないときは何も起きない。 */
function applyEffectSkill(next: BattleState, actor: Combatant, skill: Skill, rawTargetId: string, rng: () => number): BattleState {
  const targetId = retarget(next, actor, rawTargetId);
  const allies = actor.isEnemy ? next.enemies : next.party;
  const foes = actor.isEnemy ? next.party : next.enemies;
  if (actor.mp < skill.mpCost) {
    next.log.push(`${actor.name} はMPが足りず ${skill.name} を使えなかった`);
    return next;
  }
  if (skill.hpCost) {
    const cost = Math.min(Math.round(actor.maxHp * skill.hpCost), Math.max(0, actor.hp - 1));
    actor.hp -= cost;
    next.log.push(`${actor.name} は ${cost} のHPを支払った`);
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
    case "buff":
    case "buffAll": {
      const targets = skill.effect === "buffAll" ? allies.filter(isAlive) : allies.filter((c) => c.id === targetId && isAlive(c));
      if (targets.length === 0) {
        return next;
      }
      actor.mp -= skill.mpCost;
      for (const ally of targets) {
        applyMod(next, actor, ally, skill);
      }
      return next;
    }
    case "debuff":
    case "debuffAll": {
      const targets = skill.effect === "debuffAll" ? foes.filter(isAlive) : foes.filter((c) => c.id === targetId && isAlive(c));
      if (targets.length === 0) {
        return next;
      }
      actor.mp -= skill.mpCost;
      for (const foe of targets) {
        if (rng() < (skill.chance ?? 1)) {
          applyMod(next, actor, foe, skill);
        } else {
          next.log.push(`${actor.name} の ${skill.name}！ ${foe.name} には効かなかった`);
        }
      }
      return next;
    }
    case "poison":
    case "confuse": {
      const target = foes.find((c) => c.id === targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      actor.mp -= skill.mpCost;
      if (target.maxHp > 500 || rng() >= (skill.chance ?? 0.6)) {
        next.log.push(`${actor.name} の ${skill.name}！ ${target.name} には効かなかった`);
      } else {
        inflict(next, actor.name, target, skill.effect, skill.turns ?? 3, `${actor.name} の ${skill.name}！ `);
      }
      return next;
    }
    case "sleep": {
      const target = foes.find((c) => c.id === targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      actor.mp -= skill.mpCost;
      if (target.maxHp > 500 || rng() >= (skill.chance ?? 0.6)) {
        next.log.push(`${actor.name} の ${skill.name}！ ${target.name} には効かなかった`);
      } else {
        target.sleep = skill.turns ?? 2;
        next.log.push(`${actor.name} の ${skill.name}！ ${target.name} は眠ってしまった`);
      }
      return next;
    }
    default: {
      // 効果の種類が無い特技（HPを支払う・一撃で倒すチャンスつき）は、敵1体を狙う。
      const target = findCombatant(next, targetId);
      if (!target || !isAlive(target)) {
        return next;
      }
      actor.mp -= skill.mpCost;
      if (skill.koChance && target.maxHp <= 500 && rng() < skill.koChance) {
        target.hp = 0;
        next.log.push(`${actor.name} の ${skill.name}！ ${target.name} は一撃で倒れた`);
        next.log.push(`${target.name} を倒した！`);
        return next;
      }
      dealDamage(next, actor, target, skill.name, skill.powerMultiplier, rng);
      return next;
    }
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
      if (action.type === "skill" && (action.skill.effect || action.skill.hpCost || action.skill.koChance)) {
        return applyEffectSkill(next, nextActor, action.skill, action.targetId, rng);
      }
      const target = findCombatant(next, retarget(next, nextActor, action.targetId));
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
        effectiveStat(nextActor, "attack"),
        effectiveStat(target, "defense"),
        powerMultiplier,
        rng,
      );
      const finalAmount = target.guarding ? Math.ceil(amount / 2) : amount;
      target.hp = Math.max(0, target.hp - finalAmount);
      const inflicted = nextActor.inflicts && isAlive(target) && !target.poison && !target.sleep && !target.confused && rng() < nextActor.inflicts.chance ? nextActor.inflicts : null;
      const skillName = action.type === "skill" ? action.skill.name : "たたかう";
      const criticalNote = critical ? "会心の一撃！ " : "";
      next.log.push(
        `${nextActor.name} の ${skillName}！ ${criticalNote}${target.name} に ${finalAmount} のダメージ`,
      );
      if (!isAlive(target)) {
        next.log.push(`${target.name} を倒した！`);
      } else if (inflicted) {
        inflict(next, nextActor.name, target, inflicted.status, inflicted.turns, "");
      }
      return next;
    }

    case "item": {
      const target = findCombatant(next, action.targetId);
      if (!target) {
        return next;
      }
      const hpBefore = target.hp;
      const mpBefore = target.mp;
      target.hp = Math.min(target.maxHp, target.hp + action.item.healAmount);
      target.mp = Math.min(target.maxMp, target.mp + (action.item.mpAmount ?? 0));
      const parts: string[] = [];
      if (action.item.healAmount > 0) parts.push(`HPが ${target.hp - hpBefore} 回復した`);
      if ((action.item.mpAmount ?? 0) > 0) parts.push(`MPが ${target.mp - mpBefore} 回復した`);
      next.log.push(`${nextActor.name} は ${action.item.name} を使った。${target.name} の${parts.join("、")}`);
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
    if (livingActor.sleep) {
      current.log.push(`${livingActor.name} は眠っている`);
      continue;
    }
    if (livingActor.confused) {
      current.log.push(`${livingActor.name} は混乱している！`);
      if (rng() < 0.5) {
        // 敵味方かまわず、生きている誰かをなぐる
        const everyone = [...current.party, ...current.enemies].filter((c) => isAlive(c) && c.id !== livingActor.id);
        const victim = everyone[Math.floor(rng() * everyone.length)];
        if (victim) {
          current = applyAction(current, { type: "attack", actorId: livingActor.id, targetId: victim.id }, rng);
          continue;
        }
      }
    }
    current = applyAction(current, action, rng);
  }
  tickStatuses(current);

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
  // 攻撃魔法を持つ敵は、ときどき魔法を使う
  if (enemy.spell && rng() < enemy.spell.chance) {
    return { type: "skill", actorId: enemy.id, targetId: target.id, skill: enemy.spell.skill };
  }
  return { type: "attack", actorId: enemy.id, targetId: target.id };
}
