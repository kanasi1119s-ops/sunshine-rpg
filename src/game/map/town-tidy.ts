import type { Npc } from "../npc";
import { npcLook } from "../sprite/character-specs";
import { objectKindOf } from "../../render/object-markers";
import { doorOffsetX, isHouse, propFootprintTiles } from "./map-props";
import type { MapProp, MapPropKind, TileMapData } from "./types";

/**
 * 町のととのえ（2026-10-06、人間の指示「花壇のオブジェクトは重なってもいいですが、ほかのオブジェクト（ドットのキャラ以外）は、
 * 町の中で重ならないようにしてください」「町ですが、囲いとかいろいろ適当な部分があります。規則性も入れて直してください」）。
 * 町の飾りを置きおえたあと（家の中を作る前）に、町ごとに次の順で直す。
 *  1) 玄関が町の外まわり（塀）にかかる家は、取りのぞく（入れない家をなくす）。
 *  2) 街灯は、道にそって、決まった間かく（6マスごと）・決まった側（横の道は北がわ、たての道は東がわ）に立てなおす。
 *  3) 花壇は、家の玄関の左右（足もとの列の、2マス横）に、そろえて置く。家のそばにない花壇は、はずす。
 *  3.2) 樽は家のすぐとなり、井戸は家の近く（2マスいない）へ移す。屋台は、まっすぐな横の道の上へ移し、
 *     その手前（南）の1列を道にして、人が屋台をよけて通れるようにする（2026-10-06 人間の指示
 *     「井戸は家の近くに商店は道の上に置いて」「樽は小さくしてすべて家の近くに置こうか」）。置けなければ、はずす。
 *  4) 絵が重なる飾りは、だいじなほう（建物 → 井戸・祠など → 木 → 街灯 → ベンチ・荷車など → 樽・箱・岩）を残し、ほかは取りのぞく。
 *     花壇は重なってもよい。調べられる物（看板・宝箱など。人のドット絵はのぞく）は、かならず残す。
 * 絵の範囲は `PROP_BOX`（足もとのマスのまんなか・下のはしから、絵の左・右・上・下のドット。ゲームの絵からはかった値）。
 */
export const PROP_BOX: Partial<Record<MapPropKind, [number, number, number, number]>> = {
  "banner-purple": [-11, 11, -42, -5],
  "banner-red": [-11, 11, -42, -5],
  "barrel": [-9, 9, -24, -1],
  "barrel-broken": [-18, 16, -21, 0],
  "bench": [-18, 9, -17, -1],
  "bones": [-16, 16, -17, 0],
  "box-broken": [-16, 16, -24, 0],
  "brazier": [-7, 6, -29, -1],
  "bush": [-15, 13, -17, -1],
  "bush-snow": [-13, 12, -16, -1],
  "cactus": [-13, 12, -40, -1],
  "candelabra": [-10, 10, -36, 0],
  "cart": [-23, 12, -25, -1],
  "chains": [-10, 10, -44, -8],
  "chest-closed": [-12, 13, -22, 0],
  "chest-open": [-12, 13, -30, 0],
  "church": [-46, 83, -157, -1],
  "cobweb": [-13, 13, -26, -1],
  "coffin": [-21, 21, -24, 0],
  "crates": [-13, 16, -27, -1],
  "crystal-blue": [-17, 17, -36, 0],
  "crystal-red": [-17, 17, -36, 0],
  "fence": [-8, 8, -17, 0],
  "fence-end": [-8, 8, -18, 0],
  "flowerbed": [-15, 14, -15, -1],
  "fountain": [-23, 23, -47, 0],
  "grave-cross": [-8, 7, -20, -1],
  "grave-round": [-8, 8, -19, 0],
  "haystack": [-16, 16, -28, 0],
  "house": [-24, 24, -51, -1],   // 2026-10-06 に絵を横へ広げた（56 ドット）が、重なりは本体で見る（左右のはしの2〜4ドットは軒のでっぱり）
  "house-blue": [-24, 24, -51, -1],
  "house-green": [-24, 24, -51, -1],
  "house-white": [-24, 24, -51, -1],
  "jail-bars": [-17, 17, -50, 0],
  "lamp": [-5, 4, -43, -1],
  "laundry": [-22, 23, -30, 0],
  "manor": [-40, 40, -70, -1],
  "manor-blue": [-40, 40, -70, -1],
  "manor-green": [-40, 40, -70, -1],
  "mushrooms": [-16, 16, -25, 0],
  "noticeboard": [-14, 13, -32, -1],
  "palm": [-15, 14, -41, -1],
  "pillar": [-10, 10, -48, 0],
  "pillar-broken": [-13, 13, -29, 0],
  "rock": [-15, 13, -17, -1],
  "rock-snow": [-13, 11, -18, -1],
  "shrine": [-9, 8, -30, -1],
  "signpost": [-16, 15, -34, -1],
  "stall": [-15, 14, -35, -1],
  "statue-soldier": [-9, 7, -41, -1],
  "statue-traveler": [-8, 7, -37, -1],
  "statue-winged": [-11, 10, -39, -1],
  "tree": [-26, 26, -69, -1],
  "tree-dead": [-19, 19, -36, -1],
  "tree-snow": [-16, 15, -40, -1],
  "tree-pine": [-15, 15, -42, -1],
  "well": [-14, 13, -35, -1]
};

const PRIORITY = (kind: MapPropKind): number => {
  if (isHouse(kind) || kind === "church") return 100;
  if (["shrine", "fountain", "well", "stall", "noticeboard", "statue-traveler", "statue-soldier", "statue-winged", "tent", "brazier"].includes(kind)) return 80;
  if (["tree", "tree-snow", "tree-dead", "tree-pine", "palm", "cactus"].includes(kind)) return 60;
  if (kind === "lamp") return 50;
  if (["cart", "haystack", "laundry", "bench", "signpost", "fence", "fence-end"].includes(kind)) return 40;
  return 20;
};

interface Box { x0: number; y0: number; x1: number; y1: number }

/** 絵のある「物」（看板・宝箱・家具など）。人のドット絵と、絵のない調べる場所（小さなきらめき）は、のぞく。 */
function isSolidObject(n: Npc): boolean {
  return npcLook(n) === "object" && objectKindOf(n.id) !== "generic";
}

function boxOf(p: MapProp, ts: number): Box | null {
  const b = PROP_BOX[p.kind];
  if (!b) return null;
  const cx = p.tileX * ts + ts / 2, by = p.tileY * ts + ts;
  return { x0: cx + b[0], x1: cx + b[1], y0: by + b[2], y1: by + b[3] };
}

/** 2つの絵が、ふちのすこしのかさなり（2ドット）をこえて重なるか。 */
function overlaps(a: Box, b: Box): boolean {
  return Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0) > 2 && Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0) > 2;
}

function isTown(mapId: string): boolean {
  return (/-(town|village)$/.test(mapId) || /^village-/.test(mapId)) && mapId !== "world-map";
}

const AROUND: Array<[number, number]> = [[1, 0], [-1, 0], [0, 1], [0, -1]];

export function tidyTowns(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    if (!isTown(mapId) || !data.collision || !data.props) continue;
    tidyTown(data, npcsByMap[mapId] ?? []);
  }
}

export function tidyTown(data: TileMapData, npcs: readonly Npc[]): void {
  const w = data.width, h = data.height, ts = data.tileWidth;
  const col = data.collision!;
  const ground = data.layers[0].data;
  const art = (x: number, y: number): string | undefined => data.tileArt?.[ground[y * w + x]];
  const ring = (x: number, y: number): boolean => x <= 0 || y <= 0 || x >= w - 1 || y >= h - 1;
  const exits = data.exits ?? [];
  let props = [...(data.props ?? [])];

  const footSet = (list: MapProp[]): Set<number> => {
    const s = new Set<number>();
    for (const p of list) for (const t of propFootprintTiles(p)) s.add(t.y * w + t.x);
    return s;
  };
  const free = (p: MapProp): void => {
    const still = footSet(props);
    for (const t of propFootprintTiles(p)) {
      const i = t.y * w + t.x;
      if (!still.has(i) && !ring(t.x, t.y) && art(t.x, t.y) !== "water") col[i] = 0;
    }
  };
  const remove = (p: MapProp): void => {
    props = props.filter((q) => q !== p);
    free(p);
  };

  // 1) 玄関が外まわりにかかる家
  for (const p of [...props]) {
    if (!isHouse(p.kind)) continue;
    const dx = p.tileX + doorOffsetX(p.kind), dy = p.tileY + 1;
    if (ring(dx, dy) && !exits.some((e) => e.tileX === dx && e.tileY === dy)) remove(p);
  }

  // 置けるかのしらべ（人・出入り口・家の玄関の前をふさがず、出入り口と人へ歩いて行けるまま）
  const doorFront = new Set<number>();
  for (const p of props) if (isHouse(p.kind)) for (let k = 1; k <= 2; k++) for (const ox of [-1, 0, 1]) doorFront.add((p.tileY + k) * w + p.tileX + doorOffsetX(p.kind) + ox);
  const nearPersonOrExit = (x: number, y: number): boolean =>
    npcs.some((n) => Math.abs(n.tileX - x) <= 1 && Math.abs(n.tileY - y) <= 1) || exits.some((e) => Math.abs(e.tileX - x) <= 1 && Math.abs(e.tileY - y) <= 1);
  const reachable = (): boolean => {
    const start = exits[0];
    if (!start) return true;
    const seen = new Set<number>([start.tileY * w + start.tileX]);
    const q = [start.tileY * w + start.tileX];
    for (let i = 0; i < q.length; i++) {
      const x = q[i] % w, y = Math.floor(q[i] / w);
      for (const [ddx, ddy] of AROUND) {
        const nx = x + ddx, ny = y + ddy, ni = ny * w + nx;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen.has(ni) || col[ni] === 1) continue;
        seen.add(ni);
        q.push(ni);
      }
    }
    return exits.every((e) => seen.has(e.tileY * w + e.tileX)) && npcs.every((n) => AROUND.some(([ddx, ddy]) => seen.has((n.tileY + ddy) * w + n.tileX + ddx)));
  };
  const objectBoxes = (): Box[] =>
    npcs.filter(isSolidObject).map((n) => ({ x0: n.tileX * ts, x1: n.tileX * ts + ts, y0: n.tileY * ts, y1: n.tileY * ts + ts }));
  const tryPlace = (kind: MapPropKind, x: number, y: number, onRoad = false): boolean => {
    if (ring(x, y)) return false;
    const p: MapProp = { kind, tileX: x, tileY: y };
    const tiles = propFootprintTiles(p);
    const occupied = footSet(props);
    for (const t of tiles) {
      const i = t.y * w + t.x;
      if (ring(t.x, t.y) || col[i] === 1 || occupied.has(i) || doorFront.has(i) || (art(t.x, t.y) === "path") !== onRoad || art(t.x, t.y) === "water" || nearPersonOrExit(t.x, t.y)) return false;
    }
    const b = boxOf(p, ts);
    // 絵が町の塀（左・右・下のはしの1マス）にはみ出す所には置かない（2026-10-06 人間の指示「塀にはみ出てる」）
    if (b && (b.x0 < ts - 1 || b.x1 > (w - 1) * ts + 1 || b.y1 > (h - 1) * ts + 1)) return false;
    if (b && kind !== "flowerbed") {
      for (const q of props) {
        if (q.kind === "flowerbed") continue;
        const qb = boxOf(q, ts);
        if (qb && overlaps(b, qb)) return false;
      }
      if (objectBoxes().some((o) => overlaps(b, o))) return false;
    }
    for (const t of tiles) col[t.y * w + t.x] = 1;
    if (!reachable()) {
      for (const t of tiles) col[t.y * w + t.x] = 0;
      return false;
    }
    props.push(p);
    return true;
  };

  // 2) 街灯: いまの街灯をはずし、道にそって決まった間かくで立てなおす
  for (const p of props.filter((q) => q.kind === "lamp")) remove(p);
  const road = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && art(x, y) === "path";
  const lamps: Array<[number, number]> = [];
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      if (!road(x, y)) continue;
      const horiz = road(x - 1, y) && road(x + 1, y);
      const vert = road(x, y - 1) && road(x, y + 1);
      if (horiz && !vert && x % 6 === 3 && !road(x, y - 1)) lamps.push([x, y - 1]);
      if (vert && !horiz && y % 6 === 3 && !road(x + 1, y)) lamps.push([x + 1, y]);
    }
  }
  for (const [x, y] of lamps) {
    if (props.some((q) => q.kind === "lamp" && Math.abs(q.tileX - x) + Math.abs(q.tileY - y) < 4)) continue;
    tryPlace("lamp", x, y);
  }

  // 3) 花壇: 家の玄関の左右に、そろえて。家のそばにない花壇（家を取りのぞいたあとに残ったものなど）は、はずす
  const besideHouse = (f: MapProp): boolean => props.some((q) => isHouse(q.kind) && q.tileY === f.tileY && Math.abs(q.tileX - f.tileX) === 2);
  for (const f of props.filter((q) => q.kind === "flowerbed" && !besideHouse(q))) remove(f);
  for (const p of props.filter((q) => isHouse(q.kind) && !q.kind.startsWith("manor"))) {
    for (const dx of [-2, 2]) {
      if (!props.some((q) => q.kind === "flowerbed" && q.tileX === p.tileX + dx && q.tileY === p.tileY)) tryPlace("flowerbed", p.tileX + dx, p.tileY);
    }
  }

  // 3.2) 樽・井戸は家の近くへ、屋台は道の上へ
  const houseTiles = (): Array<[number, number]> => props.filter((q) => isHouse(q.kind)).flatMap((q) => propFootprintTiles(q).map((t): [number, number] => [t.x, t.y]));
  const houseDist = (x: number, y: number, hs: Array<[number, number]>): number =>
    hs.reduce((m, [hx, hy]) => Math.min(m, Math.max(Math.abs(hx - x), Math.abs(hy - y))), 99);
  for (const [kind, maxD] of [["well", 2], ["barrel", 1]] as const) {
    for (const p of props.filter((q) => q.kind === kind)) {
      const hs = houseTiles();
      if (houseDist(p.tileX, p.tileY, hs) <= maxD) continue;
      remove(p);
      const cands: Array<[number, number, number]> = [];
      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          const d = houseDist(x, y, hs);
          // 玄関の前の列（玄関から左右3マス）は、宿屋の看板などのためにあけておく
          const front = props.some((q) => isHouse(q.kind) && y === q.tileY + 1 && Math.abs(x - q.tileX - doorOffsetX(q.kind)) <= 3);
          if (d >= 1 && d <= maxD && !front) cands.push([x, y, d * 100 + Math.abs(x - p.tileX) + Math.abs(y - p.tileY)]);
        }
      }
      cands.sort((a, b) => a[2] - b[2]);
      for (const [x, y] of cands) if (tryPlace(kind, x, y)) break;
    }
  }
  const pathTile = ground.find((_g, i) => art(i % w, Math.floor(i / w)) === "path");
  for (const p of props.filter((q) => q.kind === "stall")) {
    if (road(p.tileX, p.tileY)) continue;
    remove(p);
    if (pathTile === undefined) continue;
    const cands: Array<[number, number, number]> = [];
    for (let y = 2; y < h - 2; y++) {
      for (let x = 3; x < w - 3; x++) {
        // まっすぐな横の道（左右2マスずつ道がつづき、上には道がない所）
        let ok = true;
        for (let dx = -2; dx <= 2; dx++) if (!road(x + dx, y) || road(x + dx, y - 1)) ok = false;
        if (ok) cands.push([x, y, Math.abs(x - p.tileX) + Math.abs(y - p.tileY)]);
      }
    }
    cands.sort((a, b) => a[2] - b[2]);
    for (const [x, y] of cands) {
      // 屋台の手前（南）の1列を、よけて通る道にする（空いている所だけ）
      const bypass: number[] = [];
      let ok = true;
      for (let dx = -2; dx <= 2; dx++) {
        const i = (y + 1) * w + x + dx;
        if (road(x + dx, y + 1)) continue;
        if (ring(x + dx, y + 1) || col[i] === 1 || footSet(props).has(i) || art(x + dx, y + 1) === "water") ok = false;
        bypass.push(i);
      }
      if (!ok) continue;
      const old = bypass.map((i) => ground[i]);
      for (const i of bypass) ground[i] = pathTile;
      if (tryPlace("stall", x, y, true)) break;
      bypass.forEach((i, k) => (ground[i] = old[k]));
    }
  }

  // 3.5) 絵が塀にはみ出す飾り（建物はのぞく）は、取りのぞく（2026-10-06）
  for (const p of [...props]) {
    if (isHouse(p.kind) || p.kind === "church") continue;
    const b = boxOf(p, ts);
    if (b && (b.x0 < ts - 1 || b.x1 > (w - 1) * ts + 1 || b.y1 > (h - 1) * ts + 1)) remove(p);
  }

  // 4) 重なり: だいじなほうを残す（花壇はのぞく）。調べられる物と重なる飾りも取りのぞく
  const objs = objectBoxes();
  let changed = true;
  while (changed) {
    changed = false;
    const order = [...props].sort((a, b) => PRIORITY(b.kind) - PRIORITY(a.kind));
    outer: for (let i = 0; i < order.length; i++) {
      const a = order[i];
      if (a.kind === "flowerbed") continue;
      const ab = boxOf(a, ts);
      if (!ab) continue;
      if (PRIORITY(a.kind) < 100 && objs.some((o) => overlaps(ab, o))) {
        remove(a);
        changed = true;
        break;
      }
      for (let j = 0; j < i; j++) {
        const b = order[j];
        if (b.kind === "flowerbed") continue;
        const bb = boxOf(b, ts);
        if (bb && overlaps(ab, bb)) {
          remove(a);
          changed = true;
          break outer;
        }
      }
    }
  }
  // 重なりで家を取りのぞいたあとに残った花壇も、はずす
  for (const f of props.filter((q) => q.kind === "flowerbed" && !besideHouse(q))) remove(f);
  data.props = props;
}

/** 町の中で、花壇いがいの飾り・調べられる物の絵が重なっている組（テスト用）。 */
export function townOverlaps(data: TileMapData, npcs: readonly Npc[]): string[] {
  const ts = data.tileWidth;
  const out: string[] = [];
  const boxes: Array<{ name: string; box: Box }> = [];
  for (const p of data.props ?? []) {
    if (p.kind === "flowerbed") continue;
    const b = boxOf(p, ts);
    if (b) boxes.push({ name: `${p.kind}(${p.tileX},${p.tileY})`, box: b });
  }
  for (const n of npcs) if (isSolidObject(n)) boxes.push({ name: n.id, box: { x0: n.tileX * ts, x1: n.tileX * ts + ts, y0: n.tileY * ts, y1: n.tileY * ts + ts } });
  for (let i = 0; i < boxes.length; i++) for (let j = 0; j < i; j++) if (overlaps(boxes[i].box, boxes[j].box)) out.push(`${boxes[i].name} × ${boxes[j].name}`);
  return out;
}

/** 町の塀（左・右・下のはし）に絵がはみ出している飾り（建物はのぞく。テスト用）。 */
export function townWallOverhangs(data: TileMapData): string[] {
  const ts = data.tileWidth, w = data.width, h = data.height;
  const out: string[] = [];
  for (const p of data.props ?? []) {
    if (isHouse(p.kind) || p.kind === "church") continue;
    const b = boxOf(p, ts);
    if (b && (b.x0 < ts - 1 || b.x1 > (w - 1) * ts + 1 || b.y1 > (h - 1) * ts + 1)) out.push(`${p.kind}(${p.tileX},${p.tileY})`);
  }
  return out;
}
