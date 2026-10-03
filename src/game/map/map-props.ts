import type { MapProp, TileMapData } from "./types";

/** 飾りの絵（`prop:*`）は48×48の枠。足元・中央のマスにそろえる。 */
export const PROP_SIZE = 48;

/** 足元のマスから見た、通れなくするマスの範囲（左・右・上へ何マスか）。木は幹の1マス、家は横3マス×縦2マス。 */
export const PROP_FOOTPRINT: Record<MapProp["kind"], { left: number; right: number; up: number }> = {
  tree: { left: 0, right: 0, up: 0 },
  house: { left: 1, right: 1, up: 1 },
};

/** 絵の上端が、足元のマスより上へ何マスぶんはみ出すか（NPCや出入り口と重ねないための確認に使う）。 */
export function propOverhangTiles(kind: MapProp["kind"], tileHeight: number): number {
  const footprintUp = PROP_FOOTPRINT[kind].up;
  return Math.max(0, Math.ceil((PROP_SIZE - tileHeight * (footprintUp + 1)) / tileHeight));
}

/**
 * 町の飾り。家は、もとの3×2の建物ブロック（通れないマス）の真上に置く。木は、通り道から外れた草地。
 * 足元・中央のマスで書く（x, y）。NPC・出入り口と重ならないことは `map-props.test.ts` で確かめる。
 */
export const MAP_PROPS: Record<string, MapProp[]> = {
  "touri-town": [
    { kind: "house", tileX: 16, tileY: 4 },
    { kind: "tree", tileX: 1, tileY: 14 }, { kind: "tree", tileX: 9, tileY: 14 }, { kind: "tree", tileX: 14, tileY: 13 },
    { kind: "tree", tileX: 19, tileY: 12 }, { kind: "tree", tileX: 20, tileY: 5 },
  ],
  "mugikano-village": [
    { kind: "house", tileX: 6, tileY: 4 }, { kind: "house", tileX: 15, tileY: 4 },
    { kind: "tree", tileX: 2, tileY: 12 }, { kind: "tree", tileX: 19, tileY: 11 }, { kind: "tree", tileX: 5, tileY: 14 }, { kind: "tree", tileX: 17, tileY: 14 },
  ],
  "garasuko-town": [
    { kind: "house", tileX: 6, tileY: 4 }, { kind: "house", tileX: 15, tileY: 4 },
    { kind: "tree", tileX: 2, tileY: 9 }, { kind: "tree", tileX: 19, tileY: 9 }, { kind: "tree", tileX: 20, tileY: 5 },
  ],
  "tetsukusari-town": [
    { kind: "house", tileX: 5, tileY: 5 }, { kind: "house", tileX: 16, tileY: 5 },
    { kind: "tree", tileX: 2, tileY: 14 }, { kind: "tree", tileX: 10, tileY: 14 }, { kind: "tree", tileX: 19, tileY: 14 }, { kind: "tree", tileX: 20, tileY: 13 },
  ],
  "sanone-town": [
    { kind: "tree", tileX: 2, tileY: 14 }, { kind: "tree", tileX: 8, tileY: 14 }, { kind: "tree", tileX: 16, tileY: 14 }, { kind: "tree", tileX: 21, tileY: 14 },
  ],
  "kiri-town": [
    { kind: "tree", tileX: 2, tileY: 13 }, { kind: "tree", tileX: 21, tileY: 13 }, { kind: "tree", tileX: 22, tileY: 5 },
  ],
  "shimohara-town": [
    { kind: "house", tileX: 18, tileY: 5 },
    { kind: "tree", tileX: 2, tileY: 14 }, { kind: "tree", tileX: 21, tileY: 14 }, { kind: "tree", tileX: 22, tileY: 5 },
  ],
};

/** 飾りが覆うマス（足元のマスを基準に、通れなくするマス）。 */
export function propFootprintTiles(prop: MapProp): Array<{ x: number; y: number }> {
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
        if (prop.kind === "house") {
          ground[i] = grassId;
        }
      }
    }
  }
}
