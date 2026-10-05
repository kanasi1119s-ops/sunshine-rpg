import { hashCell } from "../color-utils";
import type { Npc } from "../npc";
import { PROP_HEIGHT, propFootprintTiles } from "./map-props";
import type { MapProp, MapPropKind, TileMapData } from "./types";

/**
 * ダンジョン・塔・遺跡・洞窟・施設の「飾り」（石柱・垂れ幕・燭台・像・水晶・きのこ・骨・くも巣など）を、決まった規則で自動で置く。
 * 壁ぎわ（壁の正面のすぐ下の床）と、床のところどころに、地図ごとに決まった（毎回同じ）位置へ。
 * 置いても、出入り口・人のいるマス・そこへ歩いていく道がふさがれないようにする（ふさぐ位置は、あきらめる）。
 */
interface DecorSet {
  /** 壁ぎわに置く（背の高い）飾り。 */
  wall: MapPropKind[];
  /** 床のまんなかあたりに置く飾り。 */
  floor: MapPropKind[];
  /** 壁ぎわの個数・床の個数（地図の広さに応じて、この比率で増やす）。 */
  wallPer100: number;
  floorPer100: number;
}

const DECOR: Record<string, DecorSet> = {
  tower: { wall: ["banner-purple", "pillar", "candelabra", "statue-winged", "banner-purple", "cobweb"], floor: ["pillar-broken", "bones"], wallPer100: 4.2, floorPer100: 1.2 },
  ruins: { wall: ["banner-red", "pillar", "statue-soldier", "candelabra", "banner-purple", "cobweb"], floor: ["pillar-broken", "bones", "coffin", "box-broken"], wallPer100: 4.2, floorPer100: 1.8 },
  mine: { wall: ["crystal-blue", "crystal-red"], floor: ["barrel-broken", "box-broken", "bones"], wallPer100: 3.6, floorPer100: 2.0 },
  seabed: { wall: ["crystal-blue", "pillar", "statue-winged", "pillar", "crystal-blue", "candelabra"], floor: ["pillar-broken", "bones", "box-broken"], wallPer100: 3.6, floorPer100: 1.6 },
  volcano: { wall: ["brazier", "crystal-red", "banner-red", "brazier", "pillar"], floor: ["bones", "pillar-broken"], wallPer100: 3.6, floorPer100: 1.6 },
  facility: { wall: ["banner-red", "pillar", "candelabra"], floor: ["box-broken", "barrel-broken", "bones"], wallPer100: 3.0, floorPer100: 1.4 },
};

const AROUND: Array<[number, number]> = [[1, 0], [-1, 0], [0, 1], [0, -1]];

export function applyAutoDecor(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    const set = data.theme ? DECOR[data.theme] : undefined;
    if (!set || !data.collision) {
      continue;
    }
    const w = data.width;
    const h = data.height;
    const collision = data.collision;
    const npcs = npcsByMap[mapId] ?? [];
    const exits = data.exits ?? [];
    const art = (x: number, y: number): string | undefined => data.tileArt?.[data.layers[0].data[y * w + x]];
    const isFloor = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && collision[y * w + x] === 0 && art(x, y) === "tint:flagstone";
    const isWall = (x: number, y: number): boolean => x < 0 || y < 0 || x >= w || y >= h || (collision[y * w + x] === 1 && art(x, y) === "tint:brick");
    const nearNpcOrExit = (x: number, y: number, r: number): boolean =>
      npcs.some((n) => Math.abs(n.tileX - x) <= r && Math.abs(n.tileY - y) <= r) || exits.some((e) => Math.abs(e.tileX - x) <= r && Math.abs(e.tileY - y) <= r);

    const props: MapProp[] = [...(data.props ?? [])];
    const occupied = new Set<number>();
    const place = (kind: MapPropKind, x: number, y: number): boolean => {
      const tiles = propFootprintTiles({ kind, tileX: x, tileY: y });
      // 背の高い飾りは、地図の上すぎる位置に置かない（絵が画面の外へ切れる）
      if (PROP_HEIGHT[kind] > 30 && y < 3) {
        return false;
      }
      for (const t of tiles) {
        if (!isFloor(t.x, t.y) || occupied.has(t.y * w + t.x) || nearNpcOrExit(t.x, t.y, 2)) {
          return false;
        }
      }
      if (tiles.length === 0 && (occupied.has(y * w + x) || nearNpcOrExit(x, y, 1))) {
        return false;
      }
      if (tiles.length > 0) {
        for (const t of tiles) collision[t.y * w + t.x] = 1;
        if (!stillReachable()) {
          for (const t of tiles) collision[t.y * w + t.x] = 0;
          return false;
        }
        for (const t of tiles) occupied.add(t.y * w + t.x);
      } else {
        occupied.add(y * w + x);
      }
      props.push({ kind, tileX: x, tileY: y });
      return true;
    };
    const stillReachable = (): boolean => {
      const start = exits[0];
      if (!start) return true;
      const seen = new Set<number>([start.tileY * w + start.tileX]);
      const stack: Array<[number, number]> = [[start.tileX, start.tileY]];
      while (stack.length) {
        const [x, y] = stack.pop()!;
        for (const [dx, dy] of AROUND) {
          const nx = x + dx;
          const ny = y + dy;
          if (nx < 0 || ny < 0 || nx >= w || ny >= h || collision[ny * w + nx] === 1 || seen.has(ny * w + nx)) continue;
          seen.add(ny * w + nx);
          stack.push([nx, ny]);
        }
      }
      const ok = (x: number, y: number): boolean => seen.has(y * w + x);
      return exits.every((e) => ok(e.tileX, e.tileY)) && npcs.every((n) => AROUND.some(([dx, dy]) => ok(n.tileX + dx, n.tileY + dy)));
    };

    let floorTiles = 0;
    const wallSpots: Array<[number, number]> = [];
    const floorSpots: Array<[number, number]> = [];
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        if (!isFloor(x, y)) continue;
        floorTiles++;
        if (isWall(x, y - 1) && (isWall(x - 1, y - 1) || isWall(x + 1, y - 1))) wallSpots.push([x, y]);
        else if (!isWall(x - 1, y) && !isWall(x + 1, y) && !isWall(x, y + 1)) floorSpots.push([x, y]);
      }
    }
    const order = (spots: Array<[number, number]>, salt: number): Array<[number, number]> =>
      [...spots].sort((a, b) => hashCell(a[0] * 31 + salt, a[1] * 17) - hashCell(b[0] * 31 + salt, b[1] * 17));
    // 置きすぎると歩くのにじゃまなので、密度は低め・1つの地図に置く数にも上限（2026-10-04）
    const wantWall = Math.min(8, Math.max(2, Math.round((floorTiles * set.wallPer100 * 0.35) / 100)));
    const wantFloor = Math.min(3, Math.max(1, Math.round((floorTiles * set.floorPer100 * 0.3) / 100)));
    let placed = 0;
    let i = 0;
    for (const [x, y] of order(wallSpots, 11)) {
      if (placed >= wantWall) break;
      // 壁ぎわの飾りは、近くに同じ飾りを置かない（間をあける）
      if (props.some((p) => Math.abs(p.tileX - x) <= 6 && Math.abs(p.tileY - y) <= 3)) continue;
      const kind = set.wall[hashCell(x * 5 + i, y * 3 + 7) % set.wall.length];
      i++;
      if (place(kind, x, y)) placed++;
    }
    placed = 0;
    for (const [x, y] of order(floorSpots, 23)) {
      if (placed >= wantFloor) break;
      if (props.some((p) => Math.abs(p.tileX - x) <= 6 && Math.abs(p.tileY - y) <= 6)) continue;
      const kind = set.floor[hashCell(x * 7 + i, y * 11 + 3) % set.floor.length];
      i++;
      if (place(kind, x, y)) placed++;
    }
    data.props = props;
  }
}
