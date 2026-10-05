import type { MapProp } from "../game/map/types";

/** 天幕（テント）の絵。しま模様の布、まんなかの入り口（暗い内がわ・めくれた布）、柱の先の旗、綱と杭。ドット絵（1ドット＝1px、半透明なし）。 */
const W = 56, H = 46;
let cache: HTMLCanvasElement | null = null;

const OUT = "#2a1a14";

export function getTentCanvas(): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  if (cache) return cache;
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d");
  if (!g) return null;
  const px = (x: number, y: number, col: string, w = 1, h = 1): void => {
    g.fillStyle = col;
    g.fillRect(x, y, w, h);
  };
  const cx = W / 2;
  const top = 8, bottom = H - 4;
  // 地面の影
  for (let x = 4; x < W - 4; x++) px(x, H - 2, "#5c4a30");
  // 屋根（三角形）。しま模様（砂色と赤茶）。左から光が当たる
  for (let y = top; y <= bottom; y++) {
    const t = (y - top) / (bottom - top);
    const half = Math.round(4 + t * 22);
    for (let x = cx - half; x <= cx + half; x++) {
      const stripe = Math.floor((x + 100) / 4) % 2 === 0;
      let col = stripe ? "#d8b878" : "#a8482c";
      if (x - (cx - half) < 2) col = stripe ? "#f0d898" : "#c8603c";
      if (cx + half - x < 3) col = stripe ? "#a88850" : "#7a3220";
      px(x, y, col);
    }
    px(cx - half - 1, y, OUT);
    px(cx + half + 1, y, OUT);
  }
  for (let x = cx - 27; x <= cx + 27; x++) px(x, bottom + 1, OUT);
  // 入り口（暗い内がわ）と、左右にめくれた布
  const doorTop = 22;
  for (let y = doorTop; y <= bottom; y++) {
    const t = (y - doorTop) / (bottom - doorTop);
    const half = Math.round(2 + t * 4);
    for (let x = cx - half; x <= cx + half; x++) px(x, y, y < doorTop + 3 ? "#3a2418" : "#1a100c");
    px(cx - half - 2, y, "#c8603c");
    px(cx - half - 1, y, OUT);
    px(cx + half + 1, y, OUT);
    px(cx + half + 2, y, "#7a3220");
  }
  // 柱と旗
  for (let y = 1; y < top + 2; y++) px(cx, y, "#6a4a2a");
  px(cx + 1, 1, "#e8483c", 5, 1);
  px(cx + 1, 2, "#e8483c", 4, 1);
  px(cx + 1, 3, "#b02a20", 3, 1);
  // 綱と杭
  for (let i = 0; i < 6; i++) {
    px(cx - 22 - i, bottom - 10 + i * 2, "#8a7050");
    px(cx + 22 + i, bottom - 10 + i * 2, "#8a7050");
  }
  px(cx - 30, bottom + 1, "#6a4a2a", 2, 3);
  px(cx + 29, bottom + 1, "#6a4a2a", 2, 3);
  cache = c;
  return c;
}

/** 飾りの種類が天幕なら、その絵を返す（ふつうの飾りは、`sprite-data` の絵を使う）。 */
export function proceduralPropCanvas(prop: MapProp): HTMLCanvasElement | null {
  return prop.kind === "tent" ? getTentCanvas() : null;
}
