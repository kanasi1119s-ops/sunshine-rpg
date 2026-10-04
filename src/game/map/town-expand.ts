import type { TileMapData } from "./types";

/**
 * 町・村を広げる（2026-10-04、人間の依頼「町が狭い」）。
 * もとの座標（NPC・出入り口・到着地点・飾り）はそのままにするため、東側に `EXTRA` 列を足す。
 * 東のはしの出入り口は、新しい東のはしへ移し、そこまで道をのばす。足した区域には、南北の大通りを1本通す
 * （家・街灯などは `town-decor.ts` が、この道ぞいに置く）。
 */
export const TOWN_EXTRA_COLUMNS = 14;
/** 広げる前の幅（東の新しい区域は、この列から先）。 */
export const TOWN_OLD_WIDTH = new Map<string, number>();

function isTown(mapId: string): boolean {
  return (/-(town|village)$/.test(mapId) || /^village-/.test(mapId)) && mapId !== "world-map";
}

export function applyTownExpansion(maps: Record<string, TileMapData>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    if (!isTown(mapId) || !data.collision) continue;
    const W = data.width;
    TOWN_OLD_WIDTH.set(mapId, W);
    const H = data.height;
    const W2 = W + TOWN_EXTRA_COLUMNS;
    const ground = data.layers[0].data;
    const exits = data.exits ?? [];

    // いちばん多い歩ける地面（広場・草地）と、外周の地面
    const walkCount = new Map<number, number>();
    const borderCount = new Map<number, number>();
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const i = y * W + x;
        const border = x === 0 || y === 0 || x === W - 1 || y === H - 1;
        if (border) {
          if (data.collision[i] === 1) borderCount.set(ground[i], (borderCount.get(ground[i]) ?? 0) + 1);
        } else if (data.collision[i] === 0) {
          walkCount.set(ground[i], (walkCount.get(ground[i]) ?? 0) + 1);
        }
      }
    }
    const top = (m: Map<number, number>): number | undefined => [...m.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
    const baseId = top(walkCount) ?? ground[0];
    const borderId = top(borderCount) ?? ground[0];

    // 東のはしの出入り口（道のタイルを、新しいはしまでのばす）
    const eastExits = exits.filter((e) => e.tileX === W - 1);
    const roadRows = new Map<number, number>(); // y → 道の地面ID
    for (const e of eastExits) roadRows.set(e.tileY, ground[e.tileY * W + (W - 1)]);

    const grow = (src: number[], fill: (x: number, y: number) => number): number[] => {
      const out = new Array<number>(W2 * H).fill(0);
      for (let y = 0; y < H; y++) {
        for (let x = 0; x < W2; x++) out[y * W2 + x] = x < W ? src[y * W + x] : fill(x, y);
      }
      return out;
    };
    const isRim = (x: number, y: number): boolean => x === W2 - 1 || y === 0 || y === H - 1;
    const streetX = W + Math.floor(TOWN_EXTRA_COLUMNS / 2);
    const roadId = [...roadRows.values()][0] ?? baseId;

    data.layers = data.layers.map((layer, li) => ({
      ...layer,
      data: grow(layer.data, (x, y) => {
        if (li !== 0) return 0;
        if (isRim(x, y)) return roadRows.has(y) && x === W2 - 1 ? roadRows.get(y)! : borderId;
        if (roadRows.has(y)) return roadRows.get(y)!;
        if (x === streetX && y > 0 && y < H - 1) return roadId; // 南北の大通り
        return baseId;
      }),
    }));
    const oldCollision = data.collision;
    data.collision = grow(oldCollision, (x, y) => (isRim(x, y) && !(roadRows.has(y) && x === W2 - 1) ? 1 : 0));

    // 古い東のはし（木・かき）は、あけて歩けるようにする。出入り口の行は道にする
    for (let y = 1; y < H - 1; y++) {
      const i = y * W2 + (W - 1);
      data.layers[0].data[i] = roadRows.has(y) ? roadRows.get(y)! : baseId;
      data.collision[i] = 0;
    }
    data.width = W2;
    data.exits = exits.map((e) => (e.tileX === W - 1 ? { ...e, tileX: W2 - 1 } : e));
  }
}
