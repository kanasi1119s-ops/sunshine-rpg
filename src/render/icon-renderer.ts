import { getSpriteCanvas } from "../game/art/sprite";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";

/** 16×16のアイコン（武具・消耗品・ジョブの紋・特技の印・灯貨）を描く。絵が無い名前や、ブラウザ以外（自動テスト）では何もしない。 */
export function drawIcon(ctx: CanvasRenderingContext2D, name: string | null, x: number, y: number, size = 16): void {
  if (!name) {
    return;
  }
  const canvas = getSpriteCanvas(`icon:${name}`, SPRITE_DATA);
  if (!canvas) {
    return;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, Math.round(x), Math.round(y), size, size);
}

const WEAPON_BY_TIER = ["weapon-sword", "weapon-sword", "weapon-sword", "weapon-sword", "weapon-scimitar", "weapon-sword", "weapon-sword", "weapon-spear", "weapon-sword-holy"];
const ARMOR_BY_TIER = ["armor-light", "armor-light", "armor-light", "armor-heavy", "armor-robe", "armor-robe", "armor-robe", "armor-heavy", "armor-heavy"];
const CHARM_BY_TIER = ["armor-bracelet", "armor-necklace", "armor-ring", "armor-ring", "armor-ring", "armor-necklace", "armor-necklace", "armor-bracelet", "armor-necklace"];

/** お店の装備（`weapon-3` `armor-5` `charm-2` ...）に合うアイコンの名前。 */
export function iconForItem(itemId: string): string | null {
  const m = /^(weapon|armor|charm)-(\d+)$/.exec(itemId);
  if (!m) {
    return null;
  }
  const tier = Math.max(0, Math.min(8, Number(m[2]) - 1));
  return (m[1] === "weapon" ? WEAPON_BY_TIER : m[1] === "armor" ? ARMOR_BY_TIER : CHARM_BY_TIER)[tier];
}

/** ジョブID（`sword-guard` など）に合うアイコンの名前。 */
export function iconForJob(jobId: string): string | null {
  return `job-${jobId}`;
}
