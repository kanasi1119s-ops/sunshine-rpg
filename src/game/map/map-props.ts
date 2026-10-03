import type { MapProp, TileMapData } from "./types";

/** 飾りの絵（`prop:*`）は48×48の枠。足元・中央のマスにそろえる。 */
export const PROP_SIZE = 48;

/** 足元のマスから見た、通れなくするマスの範囲（左・右・上へ何マスか）。木は幹の1マス、家は横3マス×縦2マス、屋敷は横5マス×縦2マス。 */
export const PROP_FOOTPRINT: Record<MapProp["kind"], { left: number; right: number; up: number }> = {
  tree: { left: 0, right: 0, up: 0 },
  house: { left: 1, right: 1, up: 1 },
  "house-blue": { left: 1, right: 1, up: 1 },
  "house-green": { left: 1, right: 1, up: 1 },
  manor: { left: 2, right: 2, up: 1 },
  "manor-blue": { left: 2, right: 2, up: 1 },
  "manor-green": { left: 2, right: 2, up: 1 },
  rock: { left: 0, right: 0, up: 0 },
  bush: { left: 0, right: 0, up: 0 },
  "tree-snow": { left: 0, right: 0, up: 0 },
  "tree-dead": { left: 0, right: 0, up: 0 },
  "rock-snow": { left: 0, right: 0, up: 0 },
  "bush-snow": { left: 0, right: 0, up: 0 },
  palm: { left: 0, right: 0, up: 0 },
  cactus: { left: 0, right: 0, up: 0 },
  barrel: { left: 0, right: 0, up: 0 },
  lamp: { left: 0, right: 0, up: 0 },
  well: { left: 0, right: 0, up: 0 },
  signpost: { left: 0, right: 0, up: 0 },
  crates: { left: 0, right: 0, up: 0 },
  flowerbed: { left: 0, right: 0, up: 0 },
  "icon-port": { left: 0, right: 0, up: 0 },
  "icon-village": { left: 0, right: 0, up: 0 },
  "icon-lake": { left: 0, right: 0, up: 0 },
  "icon-mine": { left: 0, right: 0, up: 0 },
  "icon-castle": { left: 0, right: 0, up: 0 },
  "icon-tents": { left: 0, right: 0, up: 0 },
  "icon-temple": { left: 0, right: 0, up: 0 },
  "icon-snowtown": { left: 0, right: 0, up: 0 },
  "icon-sky": { left: 0, right: 0, up: 0 },
  "icon-palace": { left: 0, right: 0, up: 0 },
  "icon-ruin": { left: 0, right: 0, up: 0 },
  "icon-shrine": { left: 0, right: 0, up: 0 },
  "icon-cave": { left: 0, right: 0, up: 0 },
  "icon-stones": { left: 0, right: 0, up: 0 },
  "icon-bigtree": { left: 0, right: 0, up: 0 },
  "icon-vortex": { left: 0, right: 0, up: 0 },
  "fountain": { left: 1, right: 1, up: 1 },
  "stall": { left: 1, right: 1, up: 0 },
  "haystack": { left: 0, right: 0, up: 0 },
  "cart": { left: 1, right: 1, up: 0 },
  "laundry": { left: 1, right: 1, up: 0 },
  "fence": { left: 0, right: 0, up: 0 },
  "fence-end": { left: 0, right: 0, up: 0 },
  "bench": { left: 1, right: 0, up: 0 },
  "statue-traveler": { left: 0, right: 0, up: 0 },
  "grave-cross": { left: 0, right: 0, up: 0 },
  "grave-round": { left: 0, right: 0, up: 0 },
  "noticeboard": { left: 0, right: 1, up: 0 },
  "brazier": { left: 0, right: 0, up: 0 },
  "shrine": { left: 0, right: 0, up: 0 },
  "pillar": { left: 0, right: 0, up: 0 },
  "pillar-broken": { left: 0, right: 0, up: 0 },
  "statue-soldier": { left: 0, right: 0, up: 0 },
  "statue-winged": { left: 0, right: 1, up: 0 },
  "candelabra": { left: 0, right: 0, up: 0 },
  "coffin": { left: 1, right: 1, up: 0 },
  "box-broken": { left: 1, right: 0, up: 0 },
  "crystal-blue": { left: 1, right: 1, up: 0 },
  "crystal-red": { left: 1, right: 1, up: 0 },
  "chest-closed": { left: 0, right: 0, up: 0 },
  "chest-open": { left: 0, right: 0, up: 0 },
  "jail-bars": { left: 1, right: 0, up: 0 },
  "banner-purple": { left: 0, right: 0, up: 0 },
  "banner-red": { left: 0, right: 0, up: 0 },
  "bones": { left: 0, right: 0, up: 0 },
  "cobweb": { left: 0, right: 0, up: 0 },
  "barrel-broken": { left: 0, right: 0, up: 0 },
  "mushrooms": { left: 0, right: 0, up: 0 },
  "chains": { left: 0, right: 0, up: 0 },
};

/** 絵の高さ（ピクセル）。岩・茂みは低く、家・木は枠いっぱい。 */
export const PROP_HEIGHT: Record<MapProp["kind"], number> = { tree: 48, house: 56, "house-blue": 56, "house-green": 56, manor: 80, "manor-blue": 80, "manor-green": 80, rock: 20, bush: 18, "tree-snow": 48, "tree-dead": 48, "rock-snow": 20, "bush-snow": 18, palm: 48, cactus: 48, barrel: 26, lamp: 48, well: 44, signpost: 40, crates: 36, flowerbed: 12, "icon-port": 48, "icon-village": 48, "icon-lake": 48, "icon-mine": 48, "icon-castle": 48, "icon-tents": 48, "icon-temple": 48, "icon-snowtown": 48, "icon-sky": 48, "icon-palace": 48, "icon-ruin": 48, "icon-shrine": 48, "icon-cave": 48, "icon-stones": 48, "icon-bigtree": 48, "icon-vortex": 48, "fountain": 47, "stall": 45, "haystack": 28, "cart": 32, "laundry": 30, "fence": 17, "fence-end": 18, "bench": 20, "statue-traveler": 41, "grave-cross": 22, "grave-round": 19, "noticeboard": 37, "brazier": 32, "shrine": 33, "pillar": 48, "pillar-broken": 29, "statue-soldier": 46, "statue-winged": 46, "banner-purple": 42, "banner-red": 42, "bones": 17, "cobweb": 26, "candelabra": 36, "coffin": 24, "barrel-broken": 21, "box-broken": 24, "crystal-blue": 36, "crystal-red": 36, "mushrooms": 25, "chest-closed": 22, "chest-open": 30, "chains": 44, "jail-bars": 50 };

/** 通り抜けられる飾り（壁の飾り・床の飾り）。足元のマスを通れなくしない。 */
export const PASSABLE_PROPS = new Set<string>(["banner-purple", "banner-red", "bones", "cobweb", "barrel-broken", "mushrooms", "chains"]);

export const isHouse = (kind: MapProp["kind"]): boolean => kind.startsWith("house") || kind.startsWith("manor");

/** 絵の上端が、足元のマスより上へ何マスぶんはみ出すか（NPCや出入り口と重ねないための確認に使う）。 */
export function propOverhangTiles(kind: MapProp["kind"], tileHeight: number): number {
  const footprintUp = PROP_FOOTPRINT[kind].up;
  return Math.max(0, Math.ceil((PROP_HEIGHT[kind] - tileHeight * (footprintUp + 1)) / tileHeight));
}

/**
 * 町の飾り。家は、もとの3×2の建物ブロック（通れないマス）の真上に置く。木は、通り道から外れた草地。
 * 足元・中央のマスで書く（x, y）。NPC・出入り口と重ならないことは `map-props.test.ts` で確かめる。
 */
export const MAP_PROPS: Record<string, MapProp[]> = {
  "touri-town": [
    { kind: "shrine", tileX: 3, tileY: 6 }, { kind: "bench", tileX: 9, tileY: 12 },
    { kind: "well", tileX: 14, tileY: 11 }, { kind: "lamp", tileX: 9, tileY: 10 }, { kind: "signpost", tileX: 13, tileY: 7 }, { kind: "barrel", tileX: 6, tileY: 9 }, { kind: "crates", tileX: 18, tileY: 10 }, { kind: "flowerbed", tileX: 8, tileY: 12 },
    { kind: "manor", tileX: 17, tileY: 4 },
    { kind: "tree", tileX: 1, tileY: 14 }, { kind: "tree", tileX: 9, tileY: 14 }, { kind: "tree", tileX: 14, tileY: 13 },
    { kind: "tree", tileX: 19, tileY: 12 }, { kind: "tree", tileX: 20, tileY: 5 },
    { kind: "bush", tileX: 7, tileY: 13 }, { kind: "rock", tileX: 12, tileY: 14 },
  ],
  "mugikano-village": [
    { kind: "haystack", tileX: 19, tileY: 7 }, { kind: "cart", tileX: 4, tileY: 12 }, { kind: "shrine", tileX: 18, tileY: 13 },
    { kind: "barrel", tileX: 4, tileY: 10 }, { kind: "crates", tileX: 18, tileY: 10 }, { kind: "lamp", tileX: 12, tileY: 6 }, { kind: "flowerbed", tileX: 9, tileY: 13 },
    { kind: "house-green", tileX: 6, tileY: 4 }, { kind: "manor-green", tileX: 16, tileY: 4 },
    { kind: "tree", tileX: 2, tileY: 12 }, { kind: "tree", tileX: 19, tileY: 11 }, { kind: "tree", tileX: 5, tileY: 14 }, { kind: "tree", tileX: 17, tileY: 14 },
    { kind: "bush", tileX: 3, tileY: 10 }, { kind: "rock", tileX: 20, tileY: 13 },
  ],
  "garasuko-town": [
    { kind: "noticeboard", tileX: 19, tileY: 7 }, { kind: "stall", tileX: 3, tileY: 10 },
    { kind: "barrel", tileX: 6, tileY: 8 }, { kind: "crates", tileX: 16, tileY: 8 }, { kind: "lamp", tileX: 9, tileY: 7 },
    { kind: "manor-blue", tileX: 5, tileY: 4 }, { kind: "house", tileX: 15, tileY: 4 },
    { kind: "tree", tileX: 2, tileY: 9 }, { kind: "tree", tileX: 19, tileY: 9 }, { kind: "tree", tileX: 20, tileY: 5 },
    { kind: "bush", tileX: 3, tileY: 8 }, { kind: "rock", tileX: 18, tileY: 9 },
  ],
  "tetsukusari-town": [
    { kind: "brazier", tileX: 9, tileY: 7 }, { kind: "shrine", tileX: 4, tileY: 10 },
    { kind: "barrel", tileX: 7, tileY: 10 }, { kind: "crates", tileX: 14, tileY: 10 }, { kind: "lamp", tileX: 10, tileY: 7 },
    { kind: "house-blue", tileX: 5, tileY: 5 }, { kind: "house-green", tileX: 16, tileY: 5 },
    { kind: "tree", tileX: 2, tileY: 14 }, { kind: "tree", tileX: 10, tileY: 14 }, { kind: "tree", tileX: 19, tileY: 14 }, { kind: "tree", tileX: 20, tileY: 13 },
  ],
  "sanone-town": [
    { kind: "stall", tileX: 10, tileY: 10 }, { kind: "cart", tileX: 15, tileY: 10 },
    { kind: "rock", tileX: 4, tileY: 12 }, { kind: "rock", tileX: 19, tileY: 12 },
    { kind: "palm", tileX: 2, tileY: 14 }, { kind: "palm", tileX: 8, tileY: 14 }, { kind: "palm", tileX: 16, tileY: 14 }, { kind: "cactus", tileX: 21, tileY: 14 },
    { kind: "cactus", tileX: 6, tileY: 13 },
  ],
  "kiri-town": [
    { kind: "statue-traveler", tileX: 14, tileY: 6 }, { kind: "bench", tileX: 6, tileY: 10 }, { kind: "shrine", tileX: 18, tileY: 10 },
    { kind: "lamp", tileX: 8, tileY: 6 }, { kind: "barrel", tileX: 15, tileY: 10 }, { kind: "flowerbed", tileX: 7, tileY: 10 },
    { kind: "bush", tileX: 4, tileY: 11 }, { kind: "bush", tileX: 19, tileY: 11 },
    { kind: "tree", tileX: 2, tileY: 13 }, { kind: "tree", tileX: 21, tileY: 13 }, { kind: "tree", tileX: 22, tileY: 5 },
  ],
  "touri-outskirts": [
    { kind: "tree", tileX: 2, tileY: 5 }, { kind: "tree", tileX: 15, tileY: 5 }, { kind: "tree", tileX: 3, tileY: 10 }, { kind: "tree", tileX: 14, tileY: 11 },
    { kind: "bush", tileX: 6, tileY: 8 }, { kind: "rock", tileX: 12, tileY: 9 },
  ],
  "mugikano-water-source": [
    { kind: "tree", tileX: 2, tileY: 6 }, { kind: "tree", tileX: 15, tileY: 4 }, { kind: "tree", tileX: 3, tileY: 11 }, { kind: "tree", tileX: 15, tileY: 10 },
    { kind: "rock", tileX: 5, tileY: 9 }, { kind: "bush", tileX: 13, tileY: 8 },
  ],
  "shimohara-town": [
    { kind: "brazier", tileX: 12, tileY: 9 }, { kind: "grave-cross", tileX: 4, tileY: 13 }, { kind: "grave-round", tileX: 6, tileY: 13 },
    { kind: "house-blue", tileX: 18, tileY: 5 }, { kind: "rock-snow", tileX: 4, tileY: 12 }, { kind: "rock-snow", tileX: 12, tileY: 14 },
    { kind: "tree-snow", tileX: 2, tileY: 14 }, { kind: "tree-dead", tileX: 21, tileY: 14 }, { kind: "tree-snow", tileX: 22, tileY: 5 },
    { kind: "tree-dead", tileX: 7, tileY: 13 }, { kind: "bush-snow", tileX: 15, tileY: 12 }, { kind: "tree-snow", tileX: 9, tileY: 14 },
  ],
};

/** 飾りが覆うマス（足元のマスを基準に、通れなくするマス）。 */
export function propFootprintTiles(prop: MapProp): Array<{ x: number; y: number }> {
  // 世界地図の町のアイコンは、乗っても通れる（その上が出入り口）。
  if (prop.kind.startsWith("icon-") || PASSABLE_PROPS.has(prop.kind)) {
    return [];
  }
  const f = PROP_FOOTPRINT[prop.kind];
  const tiles: Array<{ x: number; y: number }> = [];
  for (let y = prop.tileY - f.up; y <= prop.tileY; y++) {
    for (let x = prop.tileX - f.left; x <= prop.tileX + f.right; x++) {
      tiles.push({ x, y });
    }
  }
  return tiles;
}

/** 地図データに飾りを足す。足元のマスを通れなくし、家の下は、もとの建物の絵（屋根・壁のタイル）を地面の草に置き換える。 */
export function applyMapProps(maps: Record<string, TileMapData>): void {
  for (const [mapId, props] of Object.entries(MAP_PROPS)) {
    const data = maps[mapId];
    if (!data) {
      continue;
    }
    data.props = props.map((p) => ({ ...p }));
    const collision = data.collision ?? new Array<number>(data.width * data.height).fill(0);
    data.collision = collision;
    const ground = data.layers[0].data;
    const counts = new Map<number, number>();
    for (let i = 0; i < ground.length; i++) {
      if (!collision[i]) {
        counts.set(ground[i], (counts.get(ground[i]) ?? 0) + 1);
      }
    }
    const grassId = [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? ground[0];
    for (const prop of props) {
      for (const { x, y } of propFootprintTiles(prop)) {
        const i = y * data.width + x;
        if (i < 0 || i >= collision.length || x < 0 || x >= data.width) {
          continue;
        }
        collision[i] = 1;
        if (isHouse(prop.kind)) {
          ground[i] = grassId;
        }
      }
    }
  }
}
