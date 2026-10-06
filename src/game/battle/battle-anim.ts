import type { WeaponType } from "../items/types";
import type { BattleState, Combatant } from "./types";

/**
 * 戦闘のメッセージ（ログ1行）から、画面に出す「動き」を決める。
 *  - 味方が攻撃するとき: 武器ごとの動き（剣=ふる／短剣=さす／斧=ふりおろす／槍=つく／弓=矢をはなつ／杖=かざす）。
 *  - 魔法・とくぎ・回復・状態異常: 対象の上に、種類ごとのエフェクト。
 *  - 味方がダメージを受けたとき: 味方がのけぞる。
 * 効果音（`battle-se.ts`）・演出（`battle-effect.ts`）と同じく、メッセージが出るたびに1回だけ始める。
 */
export type WeaponMotion = "slash" | "stab" | "cast" | "shoot" | "chop" | "thrust";
export type FxId = "fire" | "water" | "light" | "wind" | "ice" | "bolt" | "rock" | "burst" | "heal" | "buff" | "debuff" | "sleep" | "poison" | "confuse" | "meteor" | "judgement" | "blessing";
/** 全員にいっせいに落ちる魔法（1行目で全員に見せ、2行目からは、のけぞるだけ）。隠しボスの魔法（2026-10-06）。 */
export const VOLLEY_FX: ReadonlySet<FxId> = new Set<FxId>(["meteor", "judgement"]);

export interface BattleAnimSpec {
  /** 動く味方（敵の行動のときは無い）。 */
  actorId?: string;
  /** 魔法を唱える敵（唱えるあいだ、敵の足もとに魔法陣と光の柱が立つ）。 */
  casterId?: string;
  /** 魔法・矢がとんでいく元（唱えた人。球・矢の出どころ）。 */
  fromId?: string;
  /** 全体にかかる魔法（柱がいくつも立つ、など）。 */
  area?: boolean;
  motion: WeaponMotion | null;
  targetIds: string[];
  fx: FxId | null;
  /** 対象が味方で、ダメージを受けた（のけぞる）。 */
  hurt: boolean;
  /** 動き全体の長さ（ミリ秒）。 */
  durationMs: number;
  /** エフェクトが始まる位置（0〜1）。矢は飛んで当たったあと、魔法はかざしたあとに始まる。 */
  fxStart: number;
  /** 武器・杖の動きだけの長さ（ミリ秒）。エフェクトを長く見せるために全体を延ばしても、武器の動きの速さは変えない。 */
  motionMs?: number;
  /**
   * コスモリングライト（2026-10-06）の動き。equip=戦闘のはじめに環がかがやき鎧がはまる、
   * deploy=6基の砲台が舞い上がり敵のまわりへ飛ぶ、shot=砲台の1基が雷のビームを撃つ（cosmoShot＝何発目か 0〜5）。
   */
  cosmo?: "equip" | "deploy" | "shot";
  cosmoShot?: number;
}

/** 戦闘のはじめに出す、コスモリングライトの装着の文（`main.ts` が、装備している人ごとに出す）。 */
export function cosmoEquipLine(name: string): string {
  return `${name} の コスモリングライト が かがやいた！`;
}
/** コスモリングライトの動きの長さ（ミリ秒）。 */
export const COSMO_MS = { equip: 2000, deploy: 1300, shot: 520 } as const;


/** 術・魔法・とくぎのエフェクトを見せる長さ（ミリ秒）。もとの長さの1.5倍で、最低でも1.5秒、最大でも2.4秒。 */
export function stretchFx(spec: BattleAnimSpec | null): BattleAnimSpec | null {
  if (!spec || !spec.fx) return spec;
  const startMs = spec.durationMs * spec.fxStart;
  const fxMs = Math.min(2400, Math.max(1500, (spec.durationMs - startMs) * 1.5));
  const durationMs = Math.round(startMs + fxMs);
  return { ...spec, motionMs: spec.durationMs, durationMs, fxStart: durationMs > 0 ? startMs / durationMs : 0 };
}

const MOTION_OF_WEAPON: Record<WeaponType, WeaponMotion> = { sword: "slash", dagger: "stab", staff: "cast", bow: "shoot", axe: "chop", spear: "thrust" };
export const MOTION_DURATION: Record<WeaponMotion, number> = { slash: 520, stab: 420, cast: 1500, shoot: 760, chop: 620, thrust: 480 };

/** 魔法使い枠。たたかう以外の技は、杖（槍）をかざして唱える動きになる。 */
const CASTERS = new Set(["mina", "ayame"]);

/** とくぎ・魔法の名前から、エフェクトの種類を決める。 */
export function fxForSkillName(name: string): FxId {
  if (name === "流星の裁き") return "meteor";
  if (name === "神の調停") return "judgement";
  if (name === "神の祝福") return "blessing";
  if (/火|炎|灼|業|滅|照/.test(name)) return "fire";
  if (/雷|電/.test(name)) return "bolt";
  if (/氷|霜|凍/.test(name)) return "ice";
  if (/風|疾|颶|刃|矢/.test(name)) return "wind";
  if (/水|雫|波|雨|流|潮|紋|滴/.test(name)) return "water";
  if (/光|灯|閃|断/.test(name)) return "light";
  if (/土|岩|砂|地|鉄|砕/.test(name)) return "rock";
  return "burst";
}

/** 同じ人が同じ技を、2人以上の別の相手に使ったか（全体の魔法）。ログ全体から数える。 */
function isAreaMove(state: BattleState, actorName: string, skillName: string): boolean {
  const targets = new Set<string>();
  const re = new RegExp(`^${actorName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")} の ${skillName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}！ (?:会心の一撃！ )?(.+) に \\d+ のダメージ$`);
  for (const line of state.log) {
    const m = re.exec(line);
    if (m) targets.add(m[1]);
  }
  return targets.size >= 2;
}

function byName(state: BattleState, name: string): Combatant | undefined {
  return [...state.party, ...state.enemies].find((c) => c.name === name);
}

export function battleAnimFor(text: string, state: BattleState, weaponOf: (id: string) => WeaponType | undefined): BattleAnimSpec | null {
  return stretchFx(battleAnimRaw(text, state, weaponOf));
}

function battleAnimRaw(text: string, state: BattleState, weaponOf: (id: string) => WeaponType | undefined): BattleAnimSpec | null {
  const make = (p: Partial<BattleAnimSpec> & { targetIds: string[] }): BattleAnimSpec => {
    const motion = p.motion ?? null;
    return { actorId: undefined, motion, fx: null, hurt: false, durationMs: motion ? MOTION_DURATION[motion] : 900, fxStart: motion === "cast" ? 0.4 : motion === "shoot" ? 0.55 : motion ? 0.5 : 0, ...p };
  };
  const allyActor = (name: string): Combatant | undefined => {
    const c = byName(state, name);
    return c && !c.isEnemy ? c : undefined;
  };

  // コスモリングライト: 装着・砲台が舞い上がる・雷のビーム（1発ずつ）
  const equip = /^(.+?) の コスモリングライト が かがやいた！$/.exec(text);
  if (equip) {
    const actor = allyActor(equip[1]);
    return actor ? make({ actorId: actor.id, targetIds: [actor.id], cosmo: "equip", durationMs: COSMO_MS.equip }) : null;
  }
  const deploy = /^(.+?) の コスモリングライト！/.exec(text);
  if (deploy) {
    const actor = allyActor(deploy[1]);
    if (!actor) return null;
    // ねらう敵は、このあとの1発目の行から（ログには、このターンの行がもう全部ある）
    const at = state.log.lastIndexOf(text);
    const first = state.log.slice(at + 1).map((l) => new RegExp(`^${deploy[1].replace(/[.*+?^${}()|[\]\\]/g, "\\$&")} の 環光の雷撃（\\d）！ (.+) に \\d+ のダメージ$`).exec(l)).find(Boolean);
    const target = first ? byName(state, first[1]) : state.enemies.find((e) => e.hp > 0);
    return make({ actorId: actor.id, targetIds: target ? [target.id] : [], cosmo: "deploy", durationMs: COSMO_MS.deploy });
  }
  const shot = /^(.+?) の 環光の雷撃（(\d)）！ (.+) に \d+ のダメージ$/.exec(text);
  if (shot) {
    const actor = allyActor(shot[1]);
    const target = byName(state, shot[3]);
    if (!actor || !target) return null;
    return make({ actorId: actor.id, targetIds: [target.id], cosmo: "shot", cosmoShot: (Number(shot[2]) - 1) % 6, durationMs: COSMO_MS.shot });
  }

  // 味方がダメージを受けた / 敵にダメージを与えた
  const damage = /^(.+?) の (.+?)！ (?:会心の一撃！ )?(.+) に \d+ のダメージ$/.exec(text);
  if (damage) {
    const [, actorName, skillName, targetName] = damage;
    const actor = allyActor(actorName);
    const target = byName(state, targetName);
    if (!target) return null;
    if (!actor) {
      if (target.isEnemy) return null;
      const caster = byName(state, actorName);
      // 敵の魔法: 敵が光をためて、味方の上にエフェクトが出て、味方がのけぞる
      if (skillName !== "たたかう" && caster?.isEnemy) {
        const fx = fxForSkillName(skillName);
        // 流星の裁き: 全員の上に、いっせいに流星が落ちる（ためは長め）
        if (VOLLEY_FX.has(fx)) return make({ casterId: caster.id, fromId: caster.id, area: true, targetIds: state.party.filter((c) => c.hp > 0 || c.id === target.id).map((c) => c.id), fx, hurt: true, durationMs: 3400, fxStart: 0.4 });
        return make({ casterId: caster.id, fromId: caster.id, area: isAreaMove(state, actorName, skillName), targetIds: [target.id], fx, hurt: true, durationMs: 2000, fxStart: 0.45 });
      }
      // 敵の攻撃: 味方がのけぞる
      return make({ targetIds: [target.id], hurt: true, durationMs: 420 });
    }
    const weapon = weaponOf(actor.id);
    if (skillName === "たたかう") {
      return make({ actorId: actor.id, motion: MOTION_OF_WEAPON[weapon ?? "sword"], targetIds: [target.id] });
    }
    const caster = CASTERS.has(actor.id);
    return make({
      actorId: actor.id,
      fromId: actor.id,
      area: isAreaMove(state, actorName, skillName),
      motion: caster ? "cast" : MOTION_OF_WEAPON[weapon ?? "sword"],
      targetIds: [target.id],
      fx: fxForSkillName(skillName),
      ...(caster ? { durationMs: 2000, fxStart: 0.45 } : {}),
    });
  }

  // 神の調停（隠しボス）: 全員に、金の紋の輪が降りる。そのあとの「〜の体力が半分になった」は、のけぞるだけ
  const judge = /^(.+?) の 神の調停！$/.exec(text);
  if (judge) {
    const caster = byName(state, judge[1]);
    if (!caster) return null;
    return make({ casterId: caster.id, fromId: caster.id, area: true, targetIds: state.party.filter((c) => c.hp > 0).map((c) => c.id), fx: "judgement", hurt: true, durationMs: 3400, fxStart: 0.38 });
  }
  const halved = /^(.+) の体力が半分になった/.exec(text);
  if (halved) {
    const target = byName(state, halved[1]);
    return target ? make({ targetIds: [target.id], hurt: true, durationMs: 380 }) : null;
  }
  // 攻撃のミス（味方は武器を振るだけ。敵のミスは何も起きない）
  const miss = /^(.+?) の (.+?)！ ミス！ (.+) にはあたらなかった$/.exec(text);
  if (miss) {
    const actor = allyActor(miss[1]);
    const target = byName(state, miss[3]);
    if (!actor || !target) return null;
    return make({ actorId: actor.id, motion: MOTION_OF_WEAPON[weaponOf(actor.id) ?? "sword"], targetIds: [target.id] });
  }

  // 回復の魔法
  const heal = /^(.+?) の (.+?)！ (.+) のHPが \d+ 回復した$/.exec(text);
  if (heal) {
    const actor = allyActor(heal[1]);
    const target = byName(state, heal[3]);
    if (!target) return null;
    return make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: heal[2] === "神の祝福" ? "blessing" : "heal", ...(heal[2] === "神の祝福" ? { durationMs: 1700 } : {}) });
  }
  // どうぐ
  const item = /^(.+?) は (.+?) を使った。(.+?) の/.exec(text);
  if (item) {
    const target = byName(state, item[3]);
    return target ? make({ targetIds: [target.id], fx: "heal", durationMs: 900, fxStart: 0 }) : null;
  }
  // 強化・弱体
  const mod = /^(.+?) の (.+?)！ (.+) の(?:こうげき|しゅび|すばやさ)が(上がった|下がった)$/.exec(text);
  if (mod) {
    const actor = allyActor(mod[1]);
    const target = byName(state, mod[3]);
    if (!target) return null;
    return make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: mod[4] === "上がった" ? "buff" : "debuff" });
  }
  // 状態異常
  const sleepy = /^(?:(.+?) の (.+?)！ )?(.+) は眠ってしまった$/.exec(text);
  if (sleepy) {
    const target = byName(state, sleepy[3]);
    const actor = sleepy[1] ? allyActor(sleepy[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "sleep" }) : null;
  }
  const poisoned = /^(?:(.+?) の (.+?)！ )?(.+) は毒におかされた！$/.exec(text);
  if (poisoned) {
    const target = byName(state, poisoned[3]);
    const actor = poisoned[1] ? allyActor(poisoned[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "poison" }) : null;
  }
  const confused = /^(?:(.+?) の (.+?)！ )?(.+) は混乱した！$/.exec(text);
  if (confused) {
    const target = byName(state, confused[3]);
    const actor = confused[1] ? allyActor(confused[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "confuse" }) : null;
  }
  const poisonDamage = /^(.+) は毒のダメージを受けた/.exec(text);
  if (poisonDamage) {
    const target = byName(state, poisonDamage[1]);
    return target ? make({ targetIds: [target.id], fx: "poison", durationMs: 500, fxStart: 0 }) : null;
  }
  return null;
}
