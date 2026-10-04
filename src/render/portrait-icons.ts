/**
 * 仲間6人の顔アイコン（人間がくれたドット絵、`assets-src/characters/party-dot/`。会話欄用に縮めたもの: `tools/pixel-art/backdrop/make_icons.py`）。
 * まだ読み込めていない間・絵のない人は、今までの顔グラフィックを使う。
 */
import yuri from "../assets/portraits/yuri.png";
import yuriS from "../assets/portraits/yuri-s.png";
import reto from "../assets/portraits/reto.png";
import retoS from "../assets/portraits/reto-s.png";
import mina from "../assets/portraits/mina.png";
import minaS from "../assets/portraits/mina-s.png";
import guide from "../assets/portraits/guide.png";
import guideS from "../assets/portraits/guide-s.png";
import orca from "../assets/portraits/orca.png";
import orcaS from "../assets/portraits/orca-s.png";
import ayame from "../assets/portraits/ayame.png";
import ayameS from "../assets/portraits/ayame-s.png";

export const PORTRAIT_ICON_URLS: Record<string, string> = {
  ユーリ: yuri,
  レト: reto,
  ミナ: mina,
  ガイド: guide,
  オルカ: orca,
  アヤメ: ayame,
};

/** 小さい顔アイコン（28×28。つよさ画面の一覧用）。 */
export const PORTRAIT_ICON_SMALL_URLS: Record<string, string> = {
  ユーリ: yuriS,
  レト: retoS,
  ミナ: minaS,
  ガイド: guideS,
  オルカ: orcaS,
  アヤメ: ayameS,
};

const images = new Map<string, HTMLImageElement>();

/** 顔アイコン（読み込めていれば）。まだなら読み込みを始めて null を返す。`small` なら28×28の版。 */
export function getPortraitIcon(speaker: string, small = false): HTMLImageElement | null {
  const url = (small ? PORTRAIT_ICON_SMALL_URLS : PORTRAIT_ICON_URLS)[speaker];
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

/** 顔アイコンの絵がある人か（まだ読み込めていなくても true）。読み込み中に、前の版の顔が一瞬出ないように使う。 */
export function hasPortraitIcon(speaker: string): boolean {
  return speaker in PORTRAIT_ICON_URLS;
}

/** ゲームを開いたときに、顔アイコンを先に読み込んでおく（会話の最初の一瞬に前の絵が出ないように）。 */
export function preloadPortraitIcons(): void {
  for (const name of Object.keys(PORTRAIT_ICON_URLS)) {
    getPortraitIcon(name);
    getPortraitIcon(name, true);
  }
}

preloadPortraitIcons();
