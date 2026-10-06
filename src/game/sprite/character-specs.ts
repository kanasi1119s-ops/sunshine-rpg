import { shadeColor, hashCell } from "../color-utils";
import { PORTRAITS, type PortraitSpec } from "../portrait/portraits";
import type { SpriteSpec } from "./overworld-sprite";
import { WALKERS } from "./walker-data.generated";

/** 顔グラフィック（256×256の絵と同じ髪・肌・服の色）から、マップ用の絵の設計を作る。 */
export function spriteSpecFromPortrait(spec: PortraitSpec, name?: string): SpriteSpec {
  return {
    handKey: name && WALKERS[name] ? name : undefined,
    skin: spec.skin,
    hair: spec.hair,
    top: spec.accent,
    bottom: shadeColor(spec.accent, -0.55),
    accent: shadeColor(spec.accent, 0.25),
    hairStyle: spec.hairStyle === "slick" ? "short" : spec.hairStyle,
    headband: spec.accessory === "headband",
  };
}

/** 主人公ユーリ。 */
export const HERO_SPRITE: SpriteSpec = spriteSpecFromPortrait(PORTRAITS["ユーリ"], "ユーリ");

/** 町の人の2頭身の素体（レト・ミナ・コハクと同じ作りの絵。man2 はレトの髪にユーリの服）。 */
const MOB_BODIES = ["reto", "man2", "mina", "guide", "woman3", "woman4"];
/** 男の素体・女の素体（`MOB_BODIES` の名前）。 */
const MALE_BODIES = ["reto", "man2"];
const FEMALE_BODIES = ["mina", "guide", "woman3", "woman4"];
/** 呼び名（会話の話し手の名前）から、男・女がはっきりしている役割。漁師などは男にする（2026-10-04、人間の指示）。 */
const MALE_ROLE = /(漁師|船乗り|船頭|渡し守|おじ|じい|爺|少年|男|兄|親父|鉱夫|坑夫|職人|兵士|番人|衛兵|組合長)/;
/** 兜と鎧の戦士にする役割（兵士・衛兵など）。 */
const WARRIOR_ROLE = /(兵士|衛兵|番人|戦士|騎士|門番|傭兵|守備)/;
const FEMALE_ROLE = /(おば|ばあ|婆|主婦|むすめ|娘|女|姉|母|おかみ|女将)/;

function speakerOf(npc: { commands?: import("../event/types").EventCommand[] }): string {
  return npc.commands ? firstSpeaker(npc.commands).speaker ?? "" : "";
}

function isWarrior(npc: { id: string; commands?: import("../event/types").EventCommand[] }): boolean {
  return WARRIOR_ROLE.test(speakerOf(npc)) || /(^|-)(guard|soldier|warrior|knight)($|-)/.test(npc.id);
}

function pickMobBody(npc: { id: string; commands?: import("../event/types").EventCommand[] }, n: number): string {
  const who = speakerOf(npc);
  const pool = MALE_ROLE.test(who) || isWarrior(npc) ? MALE_BODIES : FEMALE_ROLE.test(who) ? FEMALE_BODIES : MOB_BODIES;
  return pool[n % pool.length];
}

const MOB_ACCENTS = ["#d8b048", "#c0504a", "#4a78b0", "#58985a", "#8a58a8", "#e8e0d0", "#d8803a"];
const MOB_BOTTOMS = ["#5a4a3a", "#4a4a5a", "#3a4a5a", "#6a5a4a", "#4a3a3a", "#5a5a48"];
const SKINS = ["#f2c9a0", "#e6bd8f", "#d9a67a", "#c58f66", "#b98860", "#f4d8c0"];
const HAIRS = ["#3a2a20", "#6a4a2a", "#8a3a2a", "#c8a050", "#1e1e2a", "#5a3a4a", "#a0a0a8", "#e0e0e6"];

/**
 * NPCの絵の設計。顔グラフィックがある人（`spriteName`）は、その色。名前の無い町の人は、NPCのIDから、
 * 髪・肌・髪型を決め、服の色は `color`（仮の四角の色）を使う。同じNPCは、いつも同じ見た目になる。
 */
export function spriteSpecForNpc(npc: { id: string; color: string; spriteName?: string; commands?: import("../event/types").EventCommand[] }): SpriteSpec {
  const portrait = npc.spriteName ? PORTRAITS[npc.spriteName] : undefined;
  if (portrait) {
    return spriteSpecFromPortrait(portrait, npc.spriteName);
  }
  let seed = 0;
  for (let i = 0; i < npc.id.length; i++) {
    seed = (seed * 31 + npc.id.charCodeAt(i)) >>> 0;
  }
  const h = (n: number): number => hashCell(seed, n);
  const styles = ["short", "short", "long", "twin"] as const;
  return {
    mobTemplate: pickMobBody(npc, h(6)),
    merchant: (!isWarrior(npc) && /(^shop-|merchant|vendor|stall|shopkeeper)/.test(npc.id)) || undefined,
    warrior: isWarrior(npc) || undefined,
    skin: SKINS[h(1) % SKINS.length],
    hair: HAIRS[h(2) % HAIRS.length],
    top: npc.color,
    bottom: MOB_BOTTOMS[h(7) % MOB_BOTTOMS.length] ?? shadeColor(npc.color, -0.5),
    accent: MOB_ACCENTS[h(3) % MOB_ACCENTS.length],
    hairStyle: styles[h(4) % styles.length],
    headband: h(5) % 6 === 0,
  };
}

/** 人ではなく、物・仕掛け・敵として描くNPCのIDの単語（`-` で区切ったとき）。 */
const OBJECT_WORDS = new Set([
  "scorch", "excavation", "crate", "machine", "wagon", "record", "ledger", "log", "panel", "console", "mural", "stairs",
  "pedestal", "tablet", "gate", "echo", "circle", "lore", "chest", "truth", "fork", "altar", "entrance", "yugami", "boss", "beacon", "ferry", "tansu", "bed", "shelf", "table", "counter", "signpost", "sign", "signboard", "oldsign",
  "desk", "papers", "cabinet", "reception", "hearth", "ladder", "airship", "kitchen", "cupboard",
  // 2026-10-06: 終章の光の階段・眠りの回廊、芯環塔の窓
  "bridge", "door", "window", "view", "stele",
]);
/** 敵（ボス・強敵）として描くもの。 */
const MONSTER_WORDS = new Set(["yugami", "boss", "guardian", "trial"]);

interface NpcLike {
  id: string;
  commands: import("../event/types").EventCommand[];
}

export function firstSpeaker(commands: import("../event/types").EventCommand[]): { found: boolean; speaker?: string } {
  for (const c of commands) {
    if (c.type === "message") {
      return { found: true, speaker: c.speaker };
    }
    const nested = c.type === "choice" ? c.options.flatMap((o) => o.commands) : c.type === "if" ? [...c.then, ...(c.else ?? [])] : [];
    const r = firstSpeaker(nested);
    if (r.found) {
      return r;
    }
  }
  return { found: false };
}

export type NpcLook = "person" | "object" | "monster";

/**
 * NPCの見た目の種類。IDに「台・扉・宝箱・壁画」などの単語が入るものは物、「歪み・ボス・強敵」は敵、
 * サブストーリーの調べる場所は、最初の会話に話す人がいなければ物、それ以外は人（16×32の人のドット絵）。
 */
export function npcLook(npc: NpcLike): NpcLook {
  const words = npc.id.split("-");
  if (/^(tower|kanou)\d-guard$/.test(npc.id) || words.some((w) => MONSTER_WORDS.has(w))) {
    return "monster";
  }
  if (words.some((w) => OBJECT_WORDS.has(w))) {
    return "object";
  }
  if (npc.id.startsWith("side-") && words.some((w) => /^step\d+$/.test(w))) {
    return firstSpeaker(npc.commands).speaker ? "person" : "object";
  }
  return "person";
}
