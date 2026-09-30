import { shadeColor, hashCell } from "../color-utils";
import { PORTRAITS, type PortraitSpec } from "../portrait/portraits";
import type { SpriteSpec } from "./overworld-sprite";

/** 顔グラフィック（256×256の絵と同じ髪・肌・服の色）から、マップ用の絵の設計を作る。 */
export function spriteSpecFromPortrait(spec: PortraitSpec): SpriteSpec {
  return {
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
export const HERO_SPRITE: SpriteSpec = spriteSpecFromPortrait(PORTRAITS["ユーリ"]);

const SKINS = ["#f2c9a0", "#e6bd8f", "#d9a67a", "#c58f66", "#b98860", "#f4d8c0"];
const HAIRS = ["#3a2a20", "#6a4a2a", "#8a3a2a", "#c8a050", "#1e1e2a", "#5a3a4a", "#a0a0a8", "#e0e0e6"];

/**
 * NPCの絵の設計。顔グラフィックがある人（`spriteName`）は、その色。名前の無い町の人は、NPCのIDから、
 * 髪・肌・髪型を決め、服の色は `color`（仮の四角の色）を使う。同じNPCは、いつも同じ見た目になる。
 */
export function spriteSpecForNpc(npc: { id: string; color: string; spriteName?: string }): SpriteSpec {
  const portrait = npc.spriteName ? PORTRAITS[npc.spriteName] : undefined;
  if (portrait) {
    return spriteSpecFromPortrait(portrait);
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
