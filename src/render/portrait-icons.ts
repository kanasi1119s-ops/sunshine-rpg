/**
 * 仲間6人の顔アイコン（人間がくれたドット絵、`assets-src/characters/party-dot/`。会話欄用に縮めたもの: `tools/pixel-art/backdrop/make_icons.py`）。
 * まだ読み込めていない間・絵のない人は、今までの顔グラフィックを使う。
 */
import yuri from "../assets/portraits/yuri.png";
import reto from "../assets/portraits/reto.png";
import mina from "../assets/portraits/mina.png";
import guide from "../assets/portraits/guide.png";
import orca from "../assets/portraits/orca.png";
import ayame from "../assets/portraits/ayame.png";

export const PORTRAIT_ICON_URLS: Record<string, string> = {
  ユーリ: yuri,
  レト: reto,
  ミナ: mina,
  ガイド: guide,
  オルカ: orca,
  アヤメ: ayame,
};

const images = new Map<string, HTMLImageElement>();

/** 顔アイコン（読み込めていれば）。まだなら読み込みを始めて null を返す。 */
export function getPortraitIcon(speaker: string): HTMLImageElement | null {
  const url = PORTRAIT_ICON_URLS[speaker];
  if (!url || typeof Image === "undefined") {
    return null;
  }
  let img = images.get(url);
  if (!img) {
    img = new Image();
    img.src = url;
    images.set(url, img);
  }
  return img.complete && img.naturalWidth > 0 ? img : null;
}
