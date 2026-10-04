import type { Combatant } from "../game/battle/types";
import type { SpriteSpec, SpriteFrame } from "../game/sprite/overworld-sprite";
import { drawSprite } from "./sprite-renderer";

/**
 * 戦闘で見せる、味方のドット絵の「状態」。歩く絵（16×32）のドットを組みかえて作る（絵そのものの描きおこしではなく、
 * ドットの並べかえと色かえ）。普通・ダメージ・瀕死（ひざをつく）・戦闘不能（たおれる）・毒・睡眠・混乱。
 */
export type AllyState = "normal" | "hurt" | "dying" | "ko" | "sleep" | "confuse" | "poison";

/** ずっと続く状態（ダメージのけぞりは、一瞬だけなので別）。 */
export function allyStateOf(c: Combatant): AllyState {
  if (c.hp <= 0) return "ko";
  if (c.sleep) return "sleep";
  if (c.confused) return "confuse";
  if (c.poison) return "poison";
  if (c.hp <= c.maxHp * 0.25) return "dying";
  return "normal";
}

const W = 16;
const H = 32;
type Img = { w: number; h: number; d: Uint8ClampedArray };

function blank(w: number, h: number): Img {
  return { w, h, d: new Uint8ClampedArray(w * h * 4) };
}
function px(img: Img, x: number, y: number): [number, number, number, number] {
  const i = (y * img.w + x) * 4;
  return [img.d[i], img.d[i + 1], img.d[i + 2], img.d[i + 3]];
}
function put(img: Img, x: number, y: number, p: [number, number, number, number]): void {
  if (x < 0 || y < 0 || x >= img.w || y >= img.h || p[3] === 0) return;
  const i = (y * img.w + x) * 4;
  img.d[i] = p[0]; img.d[i + 1] = p[1]; img.d[i + 2] = p[2]; img.d[i + 3] = p[3];
}
/** 縁取り（いちばん暗い色）の判定に使う。 */
function isInk(p: [number, number, number, number]): boolean {
  return p[3] > 0 && p[0] + p[1] + p[2] < 110;
}

function tint(img: Img, rgb: [number, number, number], amount: number): void {
  for (let i = 0; i < img.d.length; i += 4) {
    if (img.d[i + 3] === 0) continue;
    img.d[i] = Math.round(img.d[i] * (1 - amount) + rgb[0] * amount);
    img.d[i + 1] = Math.round(img.d[i + 1] * (1 - amount) + rgb[1] * amount);
    img.d[i + 2] = Math.round(img.d[i + 2] * (1 - amount) + rgb[2] * amount);
  }
}
function desaturate(img: Img, amount: number): void {
  for (let i = 0; i < img.d.length; i += 4) {
    if (img.d[i + 3] === 0) continue;
    const g = img.d[i] * 0.3 + img.d[i + 1] * 0.59 + img.d[i + 2] * 0.11;
    img.d[i] = Math.round(img.d[i] * (1 - amount) + g * amount);
    img.d[i + 1] = Math.round(img.d[i + 1] * (1 - amount) + g * amount);
    img.d[i + 2] = Math.round(img.d[i + 2] * (1 - amount) + g * amount);
  }
}

/** 行 y0〜y1（含む）を、横に dx ドットずらして、別の絵に写す（上のほうの体を前に倒す、などに使う）。 */
function copyRows(dst: Img, src: Img, srcY0: number, srcY1: number, dstY0: number, dx: number): void {
  for (let y = srcY0; y <= srcY1; y++) {
    for (let x = 0; x < src.w; x++) put(dst, x + dx, dstY0 + (y - srcY0), px(src, x, y));
  }
}

/** 歩く絵から、状態に合わせた絵を作る。戦闘不能は、よこ向きにたおれた絵（32×16）。 */
function transform(base: Img, state: AllyState): Img {
  switch (state) {
    case "hurt": {
      // のけぞる: 上半身を後ろ（右）へ倒し、赤くそめる
      const out = blank(W, H);
      copyRows(out, base, 0, 13, 0, 2);
      copyRows(out, base, 14, 21, 14, 1);
      copyRows(out, base, 22, 31, 22, 0);
      tint(out, [255, 70, 70], 0.42);
      return out;
    }
    case "dying": {
      // 瀕死: ひざをつく。体を4ドット低くし、頭を前（左）へたらす。少し色がぬける
      const out = blank(W, H);
      copyRows(out, base, 0, 9, 6, -2);          // 頭と肩を、前（左）へたらして低く
      copyRows(out, base, 10, 17, 16, -1);
      copyRows(out, base, 26, 31, 26, 0);        // 足先
      copyRows(out, base, 20, 21, 24, 0);        // ひざ
      desaturate(out, 0.35);
      return out;
    }
    case "ko": {
      // 戦闘不能: 仰向けにたおれる（時計まわりに90度。頭が右、足が左＝敵のほう）
      const out = blank(H, W);
      for (let y = 0; y < H; y++) {
        for (let x = 0; x < W; x++) {
          const p = px(base, x, y);
          if (p[3] === 0) continue;
          // (x, y) → 時計まわり90度: 新しい x = H-1-y、新しい y = x
          put(out, H - 1 - y, x, p);
        }
      }
      desaturate(out, 0.5);
      tint(out, [90, 90, 120], 0.2);
      return out;
    }
    case "sleep": {
      // 睡眠: 頭をたれて、うとうと。ほんの少し青く
      const out = blank(W, H);
      copyRows(out, base, 0, 11, 2, -1);
      copyRows(out, base, 12, 31, 2 + 12, 0);
      // 切れた分（足の下）を上げる。体を2ドット下げたので、足の最下段をけずる
      const trimmed = blank(W, H);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (y <= 31) put(trimmed, x, y, px(out, x, y));
      tint(trimmed, [110, 140, 255], 0.18);
      return trimmed;
    }
    case "poison": {
      const out = blank(W, H);
      copyRows(out, base, 0, 31, 0, 0);
      tint(out, [150, 60, 200], 0.38);
      return out;
    }
    case "confuse": {
      const out = blank(W, H);
      copyRows(out, base, 0, 31, 0, 0);
      tint(out, [255, 230, 120], 0.12);
      return out;
    }
    default:
      return base;
  }
}

const cache = new Map<string, HTMLCanvasElement>();

/** 状態の絵（キャッシュつき）。 */
export function getAllyCanvas(spec: SpriteSpec, specKey: string, state: AllyState, frame: SpriteFrame): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  const key = `${specKey}|${state}|${state === "normal" || state === "hurt" ? frame : 0}`;
  const hit = cache.get(key);
  if (hit) return hit;
  const src = document.createElement("canvas");
  src.width = W;
  src.height = H;
  const sctx = src.getContext("2d", { willReadFrequently: true });
  if (!sctx) return null;
  drawSprite(sctx, spec, "left", frame, 0, 0);
  const data = sctx.getImageData(0, 0, W, H);
  const base: Img = { w: W, h: H, d: data.data };
  const out = transform({ ...base, d: new Uint8ClampedArray(data.data) }, state);
  const canvas = document.createElement("canvas");
  canvas.width = out.w;
  canvas.height = out.h;
  const g = canvas.getContext("2d");
  if (!g) return null;
  g.putImageData(new ImageData(new Uint8ClampedArray(out.d), out.w, out.h), 0, 0);
  cache.set(key, canvas);
  return canvas;
}

void isInk;
