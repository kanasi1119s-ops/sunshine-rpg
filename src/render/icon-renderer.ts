import { getSpriteCanvas } from "../game/art/sprite";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";

/** 16×16のアイコン（武具・消耗品・ジョブの紋・特技の印・灯貨）を描く。絵が無い名前や、ブラウザ以外（自動テスト）では何もしない。 */
/** たて・兜・頭巾の簡単なアイコン（16×16、文字の絵。. はすき間、B=ふち、M=金属、L=明るい金属、G=金、C=布、D=布の影）。 */
const GEAR_ART: Record<string, string[]> = {
  "gear-shield": [
    "................", "..BBBBBBBBBBBB..", ".BMMMMMBMMMMMLB.", ".BMLLLMBMMMMMMB.", ".BMLMMMBMMMMMMB.", ".BMMMMMGMMMMMMB.",
    ".BGGGGGGGGGGGGB.", ".BMMMMMGMMMMMMB.", ".BMMMMMBMMMMMMB.", "..BMMMMBMMMMMB..", "..BMMMMBMMMMMB..", "...BMMMBMMMMB...",
    "....BMMMMMMB....", ".....BMMMMB.....", "......BMMB......", ".......BB.......",
  ],
  "gear-helm": [
    "................", "......BBBB......", "....BBMMMMBB....", "...BMLLMMMMMB...", "..BMLMMMMMMMMB..", "..BMMMMMMMMMMB..",
    "..BMMMMMMMMMMB..", "..BGGGGGGGGGGB..", "..BMMBBBBBBMMB..", "..BMMB....BMMB..", "..BMMB....BMMB..", "..BBBB....BBBB..",
    "................", "................", "................", "................",
  ],
  "gear-hood": [
    "................", ".....BBBBBB.....", "...BBCCCCCCBB...", "..BCCCCCCCCCCB..", ".BCCCDDDDDDCCCB.", ".BCCD......DCCB.",
    ".BCCD......DCCB.", ".BCCD......DCCB.", ".BCCCD....DCCCB.", ".BCCCCD..DCCCCB.", "..BCCCCCCCCCCB..", "...BCCCCCCCCB...",
    "....BBCCCCBB....", "......BBBB......", "................", "................",
  ],
};
const GEAR_COLORS: Record<string, string> = { B: "#2a2430", M: "#9aa6c0", L: "#e8eef8", G: "#f2c14e", C: "#4a8f6a", D: "#2e5c44" };
const gearCache: Record<string, HTMLCanvasElement> = {};

function gearCanvas(name: string): HTMLCanvasElement | null {
  const art = GEAR_ART[name];
  if (!art || typeof document === "undefined") return null;
  if (!gearCache[name]) {
    const c = document.createElement("canvas");
    c.width = 16;
    c.height = 16;
    const g = c.getContext("2d");
    if (!g) return null;
    art.forEach((row, yy) => [...row].forEach((ch, xx) => {
      const color = GEAR_COLORS[ch];
      if (color) { g.fillStyle = color; g.fillRect(xx, yy, 1, 1); }
    }));
    gearCache[name] = c;
  }
  return gearCache[name];
}

export function drawIcon(ctx: CanvasRenderingContext2D, name: string | null, x: number, y: number, size = 16): void {
  if (!name) {
    return;
  }
  if (name.startsWith("gear-")) {
    const gear = gearCanvas(name);
    if (gear) {
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(gear, Math.round(x), Math.round(y), size, size);
    }
    return;
  }
  const canvas = getSpriteCanvas(`icon:${name}`, SPRITE_DATA);
  if (!canvas) {
    return;
  }
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(canvas, Math.round(x), Math.round(y), size, size);
}

const WEAPON_BY_TIER = ["weapon-sword", "weapon-sword", "weapon-sword", "weapon-sword", "weapon-scimitar", "weapon-sword", "weapon-sword", "weapon-sword", "weapon-sword-holy"];
const ARMOR_BY_TIER = ["armor-light", "armor-light", "armor-light", "armor-heavy", "armor-robe", "armor-robe", "armor-robe", "armor-heavy", "armor-heavy"];
const CHARM_BY_TIER = ["armor-bracelet", "armor-necklace", "armor-ring", "armor-ring", "armor-ring", "armor-necklace", "armor-necklace", "armor-bracelet", "armor-necklace"];

/** お店の装備（`weapon-3` `armor-5` `charm-2` ...）に合うアイコンの名前。 */
export function iconForItem(itemId: string): string | null {
  const w = /^(dagger|staff|bow|axe|spear)-\d+$/.exec(itemId);
  if (w) {
    return `weapon-${w[1]}`;
  }
  const g = /^(shield|helm|hood)-\d+$/.exec(itemId);
  if (g) {
    return g[1] === "hood" ? "gear-hood" : g[1] === "helm" ? "gear-helm" : "gear-shield";
  }
  if (itemId.startsWith("boss-")) {
    return "armor-ring";
  }
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
