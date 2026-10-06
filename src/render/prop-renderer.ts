import { proceduralPropCanvas } from "./tent-prop";
import type { MapProp, TileMapData } from "../game/map/types";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import type { Camera } from "./camera";
import { planterColor, planterOrigin } from "./tree-planter";

/** 飾りの足元のy（ワールド座標）。プレイヤー・NPCとの前後（奥のものを先に描く）を決めるのに使う。 */
export function propFeetY(prop: MapProp, tileHeight: number): number {
  return prop.tileY * tileHeight + tileHeight;
}

/** 動く飾り（噴水など）のコマの数。`prop:<種類>` のほかに `prop:<種類>-1`, `-2`… があれば、順番に見せる（2026-10-06「噴水は水が流れるようにして」）。 */
const frameCounts = new Map<string, number>();
function propFrameCount(kind: string): number {
  let n = frameCounts.get(kind);
  if (n === undefined) {
    n = 1;
    while (SPRITE_DATA[`prop:${kind}-${n}`]) n++;
    frameCounts.set(kind, n);
  }
  return n;
}
const PROP_FRAME_MS = 140;
/** いま見せるコマの絵の名前。 */
export function propSpriteKey(kind: string, nowMs: number): string {
  const n = propFrameCount(kind);
  if (n <= 1) return `prop:${kind}`;
  const f = Math.floor(nowMs / PROP_FRAME_MS) % n;
  return f === 0 ? `prop:${kind}` : `prop:${kind}-${f}`;
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
  const nowMs = typeof performance !== "undefined" ? performance.now() : 0;
  for (const prop of props) {
    if (!filter(prop)) {
      continue;
    }
    const canvas = getSpriteCanvas(propSpriteKey(prop.kind, nowMs), SPRITE_DATA) ?? proceduralPropCanvas(prop);
    if (!canvas) {
      continue;
    }
    const x = prop.tileX * data.tileWidth + data.tileWidth / 2 - canvas.width / 2 - camera.x;
    const y = propFeetY(prop, data.tileHeight) - canvas.height - camera.y;
    ctx.drawImage(canvas, Math.round(x), Math.round(y));
    if (FRONT_GRASS_KINDS.has(prop.kind)) drawFrontGrass(ctx, data, prop, canvas, Math.round(x), Math.round(y), camera);
    const planter = planterColor(data, prop);                       // 木の根もとのレンガの囲い（前の半分）
    if (planter) {
      const front = getSpriteCanvas(`prop:planter-${planter}-front`, SPRITE_DATA);
      const o = planterOrigin(data, prop);
      if (front) ctx.drawImage(front, Math.round(o.x + 22 - front.width / 2 - camera.x), Math.round(o.y + 26 - front.height - camera.y));   // 絵は正方形にそろえて下づめ
    }
  }
}

/**
 * 草むらの中に立つ木の根元を、手前の草の葉で少しかくす（2026-10-06 人間の指示「木の根元も手前のしげみで少し隠れるようにしよう」）。
 * 木を描いたあと、根元のあたり（足もとから上へ10ドット）の、木の絵がある所にだけ、草むらと同じ並びの「葉だけの絵」
 * （terrain:forest-front。地面は透明）を重ねる。木が草むらのタイルに立っているときだけ。
 */
const FRONT_GRASS_KINDS = new Set<string>(["tree", "tree-pine", "tree-dead"]);
const alphaMasks = new Map<HTMLCanvasElement, Uint8ClampedArray | null>();
function solidMask(canvas: HTMLCanvasElement): Uint8ClampedArray | null {
  let m = alphaMasks.get(canvas);
  if (m === undefined) {
    m = null;
    try {
      const c = canvas.getContext("2d");
      if (c) m = c.getImageData(0, 0, canvas.width, canvas.height).data;
    } catch {
      m = null;
    }
    alphaMasks.set(canvas, m);
  }
  return m;
}
function drawFrontGrass(ctx: CanvasRenderingContext2D, data: TileMapData, prop: MapProp, canvas: HTMLCanvasElement, sx: number, sy: number, camera: Camera): void {
  const ground = data.layers[0]?.data;
  if (!ground || !data.tileArt) return;
  if (data.tileArt[ground[prop.tileY * data.width + prop.tileX]] !== "treeCanopy") return;
  const grass = getSpriteCanvas("terrain:forest-front", SPRITE_DATA);
  const mask = solidMask(canvas);
  if (!grass || !mask) return;
  const W = canvas.width, H = canvas.height;
  for (let py = Math.max(0, H - 11); py < H; py++) {
    for (let px = 0; px < W; px++) {
      if (mask[(py * W + px) * 4 + 3] < 250) continue;          // 木の絵がある所（すける影はのぞく）だけ
      const wx = sx + px + camera.x, wy = sy + py + camera.y;      // ワールド座標（草むらの絵の位置にそろえる）
      ctx.drawImage(grass, ((wx % 128) + 128) % 128, ((wy % 128) + 128) % 128, 1, 1, sx + px, sy + py, 1, 1);
    }
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
