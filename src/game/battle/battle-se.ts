/**
 * 戦闘のメッセージ（ログ1行）から、鳴らす効果音のID（`src/audio/se-library.ts`）を決める。
 * メッセージが出るたびに1回だけ鳴らす。戦闘ログの形は `battle-engine.ts` のとおり:
 * 「Aの技名！ Bに N のダメージ」「Bを倒した！」「Bのふたつめ…回復した」「Aは身を守っている」など。
 */
export function battleSeFor(text: string, partyNames: string[]): string | null {
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
  if (/の(こうげき|しゅび|すばやさ)が上がった$/.test(text)) {
    return "buff";
  }
  if (/の(こうげき|しゅび|すばやさ)が下がった$/.test(text) || text.includes("は眠ってしまった")) {
    return "debuff";
  }
  if (text.includes("HPを支払った")) {
    return "debuff";
  }
  const killed = /^(.+) を倒した！$/.exec(text);
  if (killed) {
    return partyNames.includes(killed[1]) ? null : "enemy-down";
  }
  if (text.includes("は一撃で倒れた")) {
    return "enemy-down";
  }
  const damage = /^(.+?) の(.+?)！ (?:会心の一撃！ )?(.+) に \d+ のダメージ$/.exec(text);
  if (damage) {
    const [, , skill, target] = damage;
    if (partyNames.includes(target)) {
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
    if (/氷|水|雨/.test(skill)) {
      return "ice";
    }
    return "attack";
  }
  return null;
}
