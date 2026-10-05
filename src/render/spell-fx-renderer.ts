import { SPELL_FX, type SpellFxSheet } from "../game/art/spell-fx.generated";

/**
 * 術のエフェクトを、ドット絵エディタで描いたコマ（シート）で再生する（2026-10-05）。
 * シートは、横にコマが並んだPNG（1コマ＝ w×h）。コマの足もとの点（ax, ay）を、当たる人・となえる人の足もとに合わせて描く。
 * 種類: hit（1人に当たる）・area（全体の術で1人ずつ）・charge（ため）・bolt（飛んでいく弾。左向きに描いてある）。
 */
const URLS = import.meta.glob("../assets/spell-fx/*.png", { eager: true, query: "?url", import: "default" }) as Record<string, string>;

const images = new Map<string, HTMLImageElement>();

function sheetImage(key: string): HTMLImageElement | null {
  if (typeof Image === "undefined") return null;
  const cached = images.get(key);
  if (cached) return cached.complete && cached.naturalWidth > 0 ? cached : null;
  const url = URLS[`../assets/spell-fx/${key.replace("/", "-")}.png`];
  if (!url) return null;
  const img = new Image();
  img.src = url;
  images.set(key, img);
  return null;
}

/** そのコマがあるか（無ければ、これまでのコードで描くエフェクトを使う）。 */
export function hasSpellFx(fx: string, kind: "hit" | "area" | "charge" | "bolt"): boolean {
  return !!SPELL_FX[`${fx}/${kind}`];
}

/** すべてのシートを先に読みこんでおく（戦闘が始まったときに呼ぶと、最初の術でも絵が出る）。 */
export function preloadSpellFx(): void {
  for (const key of Object.keys(SPELL_FX)) sheetImage(key);
}

/** 進み（0〜1）から、何コマ目かを、コマごとの長さの比で決める。 */
function frameAt(sheet: SpellFxSheet, progress: number): number {
  const total = sheet.frames.reduce((s, f) => s + f[0], 0);
  let t = Math.max(0, Math.min(0.9999, progress)) * total;
  for (let k = 0; k < sheet.frames.length; k++) {
    t -= sheet.frames[k][0];
    if (t < 0) return k;
  }
  return sheet.frames.length - 1;
}

export interface SpellFrameInfo {
  flash: number;
  shake: number;
  flashColor: string;
}

/**
 * コマを1枚描く。at は足もと（弾は弾のまん中）。scale は整数（大きな敵には2倍）。flip で左右反転（弾が右へ飛ぶとき）。
 * loopMs を渡すと、進みではなく時刻でくり返す（弾）。描けたら、そのコマの光・揺れを返す。
 */
export function drawSpellFrame(
  ctx: CanvasRenderingContext2D,
  fx: string,
  kind: "hit" | "area" | "charge" | "bolt",
  progress: number,
  at: { x: number; y: number },
  opts: { scale?: number; flip?: boolean; loopMs?: number } = {},
): SpellFrameInfo | null {
  const key = `${fx}/${kind}`;
  const sheet = SPELL_FX[key];
  if (!sheet) return null;
  const img = sheetImage(key);
  if (!img) return null;
  let k: number;
  if (opts.loopMs !== undefined) {
    const total = sheet.frames.reduce((s, f) => s + f[0], 0);
    k = frameAt(sheet, (opts.loopMs % total) / total);
  } else {
    k = frameAt(sheet, progress);
  }
  const s = opts.scale ?? 1;
  const dx = Math.round(at.x - (opts.flip ? sheet.w - sheet.ax : sheet.ax) * s);
  const dy = Math.round(at.y - sheet.ay * s);
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  if (opts.flip) {
    ctx.translate(dx + sheet.w * s, dy);
    ctx.scale(-1, 1);
    ctx.drawImage(img, k * sheet.w, 0, sheet.w, sheet.h, 0, 0, sheet.w * s, sheet.h * s);
  } else {
    ctx.drawImage(img, k * sheet.w, 0, sheet.w, sheet.h, dx, dy, sheet.w * s, sheet.h * s);
  }
  ctx.restore();
  const f = sheet.frames[k];
  return { flash: f[1], shake: f[2], flashColor: sheet.flashColor };
}
if (typeof window !== "undefined") preloadSpellFx();
