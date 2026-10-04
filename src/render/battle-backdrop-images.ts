/**
 * 戦闘画面の背景の絵（人間がくれたドット絵。400×169・64色に縮めたもの。`tools/pixel-art/backdrop/make_battle_bg.py`）。
 * 場所ごとに1〜2枚あり、戦闘のたびにどちらかを選ぶ。絵がまだ読み込めていない間や、絵のない場所は、描いた背景（`battle-backdrop.ts`）を使う。
 */
import meadow from "../assets/battle-bg/meadow.png";
import highland from "../assets/battle-bg/highland.png";
import snow1 from "../assets/battle-bg/snow1.png";
import snow2 from "../assets/battle-bg/snow2.png";
import sea1 from "../assets/battle-bg/sea1.png";
import sea2 from "../assets/battle-bg/sea2.png";
import ship1 from "../assets/battle-bg/ship1.png";
import ship2 from "../assets/battle-bg/ship2.png";
import cave from "../assets/battle-bg/cave.png";
import volcano1 from "../assets/battle-bg/volcano1.png";
import volcano2 from "../assets/battle-bg/volcano2.png";
import magmaShrine from "../assets/battle-bg/magma-shrine.png";
import forestShrine1 from "../assets/battle-bg/forest-shrine1.png";
import forestShrine2 from "../assets/battle-bg/forest-shrine2.png";
import void1 from "../assets/battle-bg/void1.png";
import void2 from "../assets/battle-bg/void2.png";
import prophecy from "../assets/battle-bg/prophecy.png";
import warp1 from "../assets/battle-bg/warp1.png";
import warp2 from "../assets/battle-bg/warp2.png";

import type { Biome } from "./battle-backdrop";

/** 場所の種類ごとの背景の絵。ここに無い種類（砂漠・沼・空・海底）は描いた背景のまま。 */
export const BACKDROP_IMAGES: Partial<Record<Biome, string[]>> = {
  grass: [meadow],
  desert: [highland],
  snow: [snow1, snow2],
  coast: [sea1, sea2],
  ship: [ship1, ship2],
  cave: [cave],
  lava: [volcano1, volcano2],
  magma: [magmaShrine],
  forest: [forestShrine1, forestShrine2],
  shrine: [void1, void2],
  prophecy: [prophecy],
  ruins: [warp1, warp2],
};

/** 名前で選べる背景の絵（オープニングのムービーなど、戦闘以外で使う）。 */
export const NAMED_BACKDROPS = { void1, void2, sea1, sea2, meadow, prophecy, highland, warp2 } as const;
export type NamedBackdrop = keyof typeof NAMED_BACKDROPS;

const images = new Map<string, HTMLImageElement>();

/** 名前で選んだ背景の絵（読み込めていれば）。まだなら読み込みを始めて null を返す。 */
export function getNamedBackdrop(name: NamedBackdrop): HTMLImageElement | null {
  return loadImage(NAMED_BACKDROPS[name]);
}

function loadImage(url: string): HTMLImageElement | null {
  if (typeof Image === "undefined") {
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

/** 背景の絵（読み込めていれば）。まだなら読み込みを始めて null を返す。 */
export function getBackdropImage(biome: Biome, variant: number): HTMLImageElement | null {
  const urls = BACKDROP_IMAGES[biome];
  if (!urls || urls.length === 0) {
    return null;
  }
  return loadImage(urls[Math.abs(Math.floor(variant)) % urls.length]);
}

/** この種類の場所に、人間がくれた背景の絵があるか（まだ読み込めていなくても true）。 */
export function hasBackdropImage(biome: Biome): boolean {
  return (BACKDROP_IMAGES[biome]?.length ?? 0) > 0;
}

/** ゲームを開いたときに、背景の絵を全部先に読み込んでおく（戦闘の最初の一瞬に、別の背景が出ないように）。 */
export function preloadBackdropImages(): void {
  for (const urls of Object.values(BACKDROP_IMAGES)) {
    for (const url of urls ?? []) loadImage(url);
  }
  for (const url of Object.values(NAMED_BACKDROPS)) loadImage(url);
}

preloadBackdropImages();
