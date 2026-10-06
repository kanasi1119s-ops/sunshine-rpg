import type { MapProp, TileMapData } from "../game/map/types";

/**
 * 町の木の根もとの、レンガの囲い（2026-10-06、人間の指示「地面がすべて芝じゃない町は木の周りの芝の地面に
 * 町の色に合わせたレンガの囲いを作りましょう。作り方は木の技法で」）。絵は assets-src/pixel-practice/r17-polish/planter2d.py。
 * 草でない地面（石だたみ・板など）に立つ広葉樹・針葉樹だけ。奥の半分と中の芝（prop:planter-<色>）は地面の上に木より先に、
 * 前の半分（prop:planter-<色>-front）は木のあとに描いて、幹の根もとをかくす。
 * 色: 白い家の町は pale（白っぽい石）、板・砂の地面は sand（砂色）、ほかは red（赤茶）。
 */
const PLANTER_TREES = new Set(["tree", "tree-pine"]);
const GRASSY = new Set(["grass", "treeCanopy", "worldforest", "hills"]);

export function planterColor(data: TileMapData, prop: MapProp): string | null {
  if (!PLANTER_TREES.has(prop.kind) || !data.tileArt || data.tileTexture || data.theme) return null;
  const id = data.layers[0]?.data[prop.tileY * data.width + prop.tileX];
  const art = id === undefined ? undefined : data.tileArt[id];
  if (!art || GRASSY.has(art)) return null;
  if (data.props?.some((p) => p.kind === "house-white")) return "pale";
  if (/plank|sand/.test(art)) return "sand";
  return "red";
}

/** 囲いの絵の左上（ワールド座標）。絵は 44×26 で、(22, 18) が木の根もと。 */
export function planterOrigin(data: TileMapData, prop: MapProp): { x: number; y: number } {
  return { x: prop.tileX * data.tileWidth + data.tileWidth / 2 - 22, y: (prop.tileY + 1) * data.tileHeight - 18 };
}
