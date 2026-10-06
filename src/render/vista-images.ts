/**
 * 景色の絵（400×225。ゲームの画面いっぱい）。イベントの `vista` コマンドで、会話のうしろに出す。
 * 元の絵は `assets-src/pixel-practice/r32-tower-vista/vista.py`（ドット絵エディタで食い違い 0 マスを確認）。
 */
import clouds from "../assets/vista/vista-clouds.png";
import summit from "../assets/vista/vista-summit.png";
import type { VistaImage } from "../game/event/types";

const URLS: Record<VistaImage, string> = { clouds, summit };
const images = new Map<VistaImage, HTMLImageElement>();

/** 景色の絵（読み込めていれば）。まだなら読み込みを始めて null を返す。 */
export function getVistaImage(name: VistaImage): HTMLImageElement | null {
  if (typeof Image === "undefined") return null;
  let img = images.get(name);
  if (!img) {
    img = new Image();
    img.src = URLS[name];
    images.set(name, img);
  }
  return img.complete && img.naturalWidth > 0 ? img : null;
}
