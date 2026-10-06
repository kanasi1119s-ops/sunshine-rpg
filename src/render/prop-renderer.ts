import { proceduralPropCanvas } from "./tent-prop";
import type { MapProp, TileMapData } from "../game/map/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import type { Camera } from "./camera";

/** 飾りの足元のy（ワールド座標）。プレイヤー・NPCとの前後（奥のものを先に描く）を決めるのに使う。 */
export function propFeetY(prop: MapProp, tileHeight: number): number {
  return prop.tileY * tileHeight + tileHeight;
}

/** 飾り（木・家）を、足元・中央のマスにそろえて描く。`filter` で、プレイヤーより奥・手前に分けて描ける。 */
export function renderProps(
  ctx: CanvasRenderingContext2D,
  data: TileMapData,
  camera: Camera,
  filter: (prop: MapProp) => boolean = () => true,
  /** 描く飾りを指定する（前後の並べ替えで1つずつ描くとき用）。省略すると地図の飾り全部。 */
  props: readonly MapProp[] | undefined = data.props,
): void {
  if (!props) {
    return;
  }
  ctx.imageSmoothingEnabled = false;
  for (const prop of props) {
    if (!filter(prop)) {
      continue;
    }
    const canvas = getSpriteCanvas(`prop:${prop.kind}`, SPRITE_DATA) ?? proceduralPropCanvas(prop);
    if (!canvas) {
      continue;
    }
    const x = prop.tileX * data.tileWidth + data.tileWidth / 2 - canvas.width / 2 - camera.x;
    const y = propFeetY(prop, data.tileHeight) - canvas.height - camera.y;
    ctx.drawImage(canvas, Math.round(x), Math.round(y));
  }
}

/**
 * 扉が開く（2026-10-06、人間の指示「町の建物ですが、扉を開いて入れるようにしてください」）。
 * 家・屋敷の絵の、両開きの扉（木の扉の4色: 明るい板・暗いすき間・板の影・金のとって）を、絵の下のほうから見つけ、
 * k（0=閉じている〜1=開ききった）にあわせて、扉の板が内がわへ開いていき、中の暗い部屋と、床にさす灯りが見える。
 */
const DOOR_COLORS = new Set(["a8703a", "4a2a14", "7a4a22", "f4cc50"]);
const doorCache = new Map<string, { x: number; y: number; w: number; h: number } | null>();

export function doorRectOf(kind: MapProp["kind"]): { x: number; y: number; w: number; h: number } | null {
  if (doorCache.has(kind)) return doorCache.get(kind)!;
  let rect: { x: number; y: number; w: number; h: number } | null = null;
  const canvas = getSpriteCanvas(`prop:${kind}`, SPRITE_DATA);
  const g = canvas?.getContext("2d", { willReadFrequently: true });
  if (canvas && g) {
    const { width: w, height: h } = canvas;
    const d = g.getImageData(0, 0, w, h).data;
    const isDoor = (x: number, y: number): boolean => {
      const i = (y * w + x) * 4;
      return d[i + 3] > 0 && DOOR_COLORS.has(((d[i] << 16) | (d[i + 1] << 8) | d[i + 2]).toString(16).padStart(6, "0"));
    };
    // 扉の板は、たてに長くつづく。絵の下半分で、扉の色がたてに6ドット以上つづく列だけを見る
    let x0 = w, x1 = -1, y0 = h, y1 = -1;
    for (let x = 0; x < w; x++) {
      let run = 0, best = 0, end = -1;
      for (let y = Math.floor(h * 0.45); y < h; y++) {
        run = isDoor(x, y) ? run + 1 : 0;
        if (run > best) {
          best = run;
          end = y;
        }
      }
      if (best >= 6) {
        x0 = Math.min(x0, x);
        x1 = Math.max(x1, x);
        y0 = Math.min(y0, end - best + 1);
        y1 = Math.max(y1, end);
      }
    }
    if (x1 >= x0) rect = { x: x0, y: y0, w: x1 - x0 + 1, h: y1 - y0 + 1 };
  }
  doorCache.set(kind, rect);
  return rect;
}

export function renderDoorOpening(ctx: CanvasRenderingContext2D, data: TileMapData, camera: Camera, prop: MapProp, k: number): void {
  const canvas = getSpriteCanvas(`prop:${prop.kind}`, SPRITE_DATA);
  const r = doorRectOf(prop.kind);
  if (!canvas || !r) return;
  const left = Math.round(prop.tileX * data.tileWidth + data.tileWidth / 2 - canvas.width / 2 - camera.x) + r.x;
  const top = Math.round(propFeetY(prop, data.tileHeight) - canvas.height - camera.y) + r.y;
  const t = Math.max(0, Math.min(1, k));
  // 中の部屋（暗がり。下のほうに、床にさす灯り）
  ctx.fillStyle = "#1c120c";
  ctx.fillRect(left, top, r.w, r.h);
  ctx.fillStyle = "#3a2416";
  ctx.fillRect(left + 1, top + r.h - 4, r.w - 2, 2);
  ctx.fillStyle = "#6a4422";
  ctx.fillRect(left + 2, top + r.h - 2, r.w - 4, 1);
  // 扉の板（左右）: 開くほど細くなる（内がわへ回って、横から見える）
  const half = Math.floor(r.w / 2);
  const leaf = Math.max(1, Math.round(half * (1 - 0.8 * t)));
  for (const [x, dir] of [[left, 1], [left + r.w - leaf, -1]] as const) {
    ctx.fillStyle = "#a8703a";
    ctx.fillRect(x, top, leaf, r.h);
    ctx.fillStyle = "#7a4a22";
    ctx.fillRect(dir > 0 ? x + leaf - 1 : x, top, 1, r.h);   // 板の、内がわのふち（影）
    ctx.fillStyle = "#4a2a14";
    ctx.fillRect(x, top, leaf, 1);
    if (leaf >= 3 && t < 0.5) {
      ctx.fillStyle = "#f4cc50";
      ctx.fillRect(dir > 0 ? x + leaf - 2 : x + 1, top + Math.floor(r.h * 0.6), 1, 1);   // とって
    }
  }
}
