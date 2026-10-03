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

const SKINS = ["#f2c9a0", "#e6bd8f", "#d9a67a", "#c58f66", "#b98860", "#f4d8c0"];
const HAIRS = ["#3a2a20", "#6a4a2a", "#8a3a2a", "#c8a050", "#1e1e2a", "#5a3a4a", "#a0a0a8", "#e0e0e6"];

/**
 * NPCの絵の設計。顔グラフィックがある人（`spriteName`）は、その色。名前の無い町の人は、NPCのIDから、
 * 髪・肌・髪型を決め、服の色は `color`（仮の四角の色）を使う。同じNPCは、いつも同じ見た目になる。
 */
export function spriteSpecForNpc(npc: { id: string; color: string; spriteName?: string }): SpriteSpec {
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
    skin: SKINS[h(1) % SKINS.length],
    hair: HAIRS[h(2) % HAIRS.length],
    top: npc.color,
    bottom: shadeColor(npc.color, -0.5),
    accent: shadeColor(npc.color, h(3) % 2 === 0 ? 0.35 : -0.3),
    hairStyle: styles[h(4) % styles.length],
    headband: h(5) % 6 === 0,
  };
}

/** 人ではなく、物・仕掛け・敵として描くNPCのIDの単語（`-` で区切ったとき）。 */
const OBJECT_WORDS = new Set([
  "scorch", "excavation", "crate", "machine", "wagon", "record", "ledger", "log", "panel", "console", "mural", "stairs",
  "pedestal", "tablet", "gate", "echo", "circle", "lore", "chest", "truth", "fork", "altar", "entrance", "yugami", "boss", "beacon", "ferry",
]);
/** 敵（ボス・強敵）として描くもの。 */
const MONSTER_WORDS = new Set(["yugami", "boss"]);

interface NpcLike {
  id: string;
  commands: import("../event/types").EventCommand[];
}

function firstSpeaker(commands: import("../event/types").EventCommand[]): { found: boolean; speaker?: string } {
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
