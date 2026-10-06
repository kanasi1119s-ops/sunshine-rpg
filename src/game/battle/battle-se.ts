/**
 * 戦闘のメッセージ（ログ1行）から、鳴らす効果音のID（`src/audio/se-library.ts`）を決める。
 * メッセージが出るたびに1回だけ鳴らす。戦闘ログの形は `battle-engine.ts` のとおり:
 * 「Aの技名！ Bに N のダメージ」「Bを倒した！」「Bのふたつめ…回復した」「Aは身を守っている」など。
 */
export function battleSeFor(text: string, partyNames: string[]): string | null {
  // 隠しボス「機械の悪神巨人兵」の魔法は、専用の音（2026-10-06）
  // コスモリングライト（2026-10-06）
  if (text.includes("の コスモリングライト が かがやいた")) return "cosmo-equip";
  if (text.includes("の コスモリングライト！")) return "cosmo-deploy";
  if (text.includes("の 環光の雷撃（")) return "cosmo-beam";
  if (text.includes("の 流星の裁き！")) return "meteor";
  if (text.includes("の 神の調停！")) return "judgement";
  if (text.includes("の 神の祝福！")) return "blessing";
  if (text.includes("の体力が半分になった")) return "player-damage";
  if (text.includes("MPが足りず")) {
    return "error";
  }
  if (text.includes("うまく逃げ切った")) {
    return "flee";
  }
  if (text.includes("逃げられなかった")) {
    return "flee-fail";
  }
  if (text.includes("身を守っている")) {
    return "guard";
  }
  if (text.includes("のHPが") && text.includes("回復した")) {
    return "heal";
  }
  if (text.includes("は毒におかされた") || text.includes("は毒のダメージ")) {
    return "poison";
  }
  if (text.includes("は混乱した！")) {
    return "confuse";
  }
  if (text.includes("は眠ってしまった")) {
    return "sleep";
  }
  if (/の(こうげき|しゅび|すばやさ)が上がった$/.test(text)) {
    return "buff";
  }
  if (/の(こうげき|しゅび|すばやさ)が下がった$/.test(text)) {
    return "debuff";
  }
  if (text.includes("HPを支払った")) {
    return "debuff";
  }
  const killed = /^(.+) を倒した！$/.exec(text);
  if (killed) {
    return partyNames.includes(killed[1]) ? "ally-down" : "enemy-down";
  }
  if (text.includes("は一撃で倒れた")) {
    return "enemy-down";
  }
  const damage = /^(.+?) の(.+?)！ (?:会心の一撃！ )?(.+) に \d+ のダメージ$/.exec(text);
  if (damage) {
    const [, , skill, target] = damage;
    if (partyNames.includes(target)) {
      // 敵の魔法（技名つき）は、その術の音。ふつうの攻撃は、味方がダメージを受ける音
      if (skill.trim() !== "たたかう" && !partyNames.some((n) => n === actorNameOf(text))) {
        return elementSe(skill) ?? "player-damage";
      }
      return "player-damage";
    }
    if (text.includes("会心の一撃")) {
      return "critical";
    }
    if (/火|炎|灼|業|滅/.test(skill)) {
      return "fire";
    }
    if (/風|疾|颶|刃/.test(skill)) {
      return "wind";
    }
    if (/雷|電/.test(skill)) {
      return "thunder";
    }
    if (/氷|霜|凍/.test(skill)) {
      return "ice";
    }
    if (/水|雫|波|雨|流|潮|紋/.test(skill)) {
      return "water";
    }
    if (/光|灯|閃|断/.test(skill)) {
      return "light";
    }
    if (/土|岩|砂|地|鉄/.test(skill)) {
      return "rock";
    }
    return "attack";
  }
  return null;
}

/** 武器の動き（振る・さす・矢をはなつ…）の効果音。動きの始まりに鳴らす。 */
export function swingSeFor(motion: "slash" | "stab" | "cast" | "shoot" | "chop" | "thrust"): string {
  return { slash: "swing-sword", stab: "swing-dagger", cast: "magic-charge", shoot: "bow-shoot", chop: "swing-axe", thrust: "spear-thrust" }[motion];
}

function actorNameOf(text: string): string {
  return /^(.+?) の/.exec(text)?.[1] ?? "";
}

function elementSe(skill: string): string | null {
  if (/火|炎|灼|業|滅|照/.test(skill)) return "fire";
  if (/風|疾|颶|刃/.test(skill)) return "wind";
  if (/雷|電/.test(skill)) return "thunder";
  if (/氷|霜|凍/.test(skill)) return "ice";
  if (/水|雫|波|雨|流|潮|紋|滴/.test(skill)) return "water";
  if (/光|灯|閃|断/.test(skill)) return "light";
  if (/土|岩|砂|地|鉄|砕/.test(skill)) return "rock";
  return null;
}
