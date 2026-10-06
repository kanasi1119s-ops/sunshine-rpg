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
 *  5) 最後に、木が3本・街灯が4本に足りない町は、空いた所に足す（木は、その町の気候の木。重なりを取りのぞいたあとに）。
 *  3.2) 樽は家のすぐとなり、井戸は家の近く（家とのあいだに1マスあけた、2〜3マスの所）へ移す。屋台は、まっすぐな横の道の上へ移し、
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

/** 町の塀の柱（四すみと、門の両わき）の絵の範囲（town-wall.ts と同じ決め方。柱は 16×28 で、足もとのマスの下にそろう）。 */
export function townPostBoxes(data: TileMapData): Box[] {
  const w = data.width, h = data.height, ts = data.tileWidth;
  const exits = data.exits ?? [];
  const isExit = (x: number, y: number): boolean => exits.some((e) => e.tileX === x && e.tileY === y);
  const ring = (x: number, y: number): boolean => x === 0 || y === 0 || x === w - 1 || y === h - 1;
  const out: Box[] = [];   // 町の塀は tidyTowns のあとで立てるが、町にはかならず立つので、ここでは町かどうかを見ない
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (!ring(x, y) || isExit(x, y)) continue;
      const corner = (x === 0 || x === w - 1) && (y === 0 || y === h - 1);
      const gateSide = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => ring(x + dx, y + dy) && isExit(x + dx, y + dy));
      if (corner || gateSide) out.push({ x0: x * ts, x1: x * ts + ts, y0: (y + 1) * ts - 28, y1: (y + 1) * ts });
    }
  }
  return out;
}

function isTown(mapId: string): boolean {
  return (/-(town|village)$/.test(mapId) || /^village-/.test(mapId)) && mapId !== "world-map";
}

const AROUND: Array<[number, number]> = [[1, 0], [-1, 0], [0, 1], [0, -1]];

function hn32(a: number, b: number): number {
  let n = 2166136261 ^ (a * 374761393) ^ (b * 668265263);
  n = Math.imul(n ^ (n >>> 13), 1274126177);
  return (n ^ (n >>> 16)) >>> 0;
}

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
  const npcAt = new Set(npcs.map((n) => n.tileY * w + n.tileX));   // 人の立つマスは、人が通れない（物とおなじ）
  /** 町の最初の出入り口から歩いて行けるマス。blockNpc: 人の立つマスも通れないとする。skip: 通れるとみなすマス（置く前のようす）。 */
  const walkFrom = (blockNpc: boolean, skip?: Set<number>): Set<number> => {
    const start = exits[0];
    const seen = new Set<number>();
    if (!start) return seen;
    seen.add(start.tileY * w + start.tileX);
    const q = [start.tileY * w + start.tileX];
    for (let i = 0; i < q.length; i++) {
      const x = q[i] % w, y = Math.floor(q[i] / w);
      for (const [ddx, ddy] of AROUND) {
        const nx = x + ddx, ny = y + ddy, ni = ny * w + nx;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen.has(ni) || (col[ni] === 1 && !skip?.has(ni)) || (blockNpc && npcAt.has(ni))) continue;
        seen.add(ni);
        q.push(ni);
      }
    }
    return seen;
  };
  const reachable = (placed: Array<{ x: number; y: number }> = []): boolean => {
    if (!exits[0]) return true;
    const seen = walkFrom(false);
    if (!(exits.every((e) => seen.has(e.tileY * w + e.tileX)) && npcs.every((n) => AROUND.some(([ddx, ddy]) => seen.has((n.tileY + ddy) * w + n.tileX + ddx))))) return false;
    // 家の玄関の前（家の中への出入り口は、このあとで足す）へ、人をよけても歩いて行けること。置く前から人でふさがっていた玄関は問わない
    const doors = props.filter((p) => isHouse(p.kind)).map((p) => (p.tileY + 1) * w + p.tileX + doorOffsetX(p.kind));
    const seenN = walkFrom(true);
    const lost = doors.filter((d) => !seenN.has(d));
    if (!lost.length) return true;
    const before = walkFrom(true, new Set(placed.map((t) => t.y * w + t.x)));
    return lost.every((d) => !before.has(d));
  };
  const posts = townPostBoxes(data);
  /** 飾りの絵が、道（path）のマスにかかるドットの数。 */
  const onPathPx = (p: MapProp): number => {
    const b = boxOf(p, ts);
    if (!b) return 0;
    let n = 0;
    // ふちの1ドット・屋根のてっぺんの3ドット（えんとつの先など）は、かかっても目立たないので数えない
    for (let y = b.y0 + 3; y < b.y1; y++) for (let x = b.x0 + 1; x < b.x1; x++) {
      const tx = Math.floor(x / ts), ty = Math.floor(y / ts);
      if (tx >= 0 && ty >= 0 && tx < w && ty < h && art(tx, ty) === "path") n++;
    }
    return n;
  };
  const objectBoxes = (): Box[] =>
    npcs.filter(isSolidObject).map((n) => ({ x0: n.tileX * ts, x1: n.tileX * ts + ts, y0: n.tileY * ts, y1: n.tileY * ts + ts }));
  // 家をずらすときは、人のすぐとなりでもよい（人の立つマスにはかからず、人へ歩いて行けるまま。出入り口のそばはさける）
  const onPersonOrNearExit = (x: number, y: number): boolean =>
    npcs.some((n) => n.tileX === x && n.tileY === y) || exits.some((e) => Math.abs(e.tileX - x) <= 1 && Math.abs(e.tileY - y) <= 1);
  const tryPlace = (kind: MapPropKind, x: number, y: number, onRoad = false, nearPeopleOk = false): boolean => {
    if (ring(x, y)) return false;
    const p: MapProp = { kind, tileX: x, tileY: y };
    const tiles = propFootprintTiles(p);
    const occupied = footSet(props);
    for (const t of tiles) {
      const i = t.y * w + t.x;
      if (ring(t.x, t.y) || col[i] === 1 || occupied.has(i) || doorFront.has(i) || (art(t.x, t.y) === "path") !== onRoad || art(t.x, t.y) === "water" || (nearPeopleOk ? onPersonOrNearExit(t.x, t.y) : nearPersonOrExit(t.x, t.y))) return false;
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
      if (posts.some((o) => overlaps(b, o))) return false;               // 門柱・すみの柱にかからない
    }
    for (const t of tiles) col[t.y * w + t.x] = 1;
    if (!reachable(tiles)) {
      for (const t of tiles) col[t.y * w + t.x] = 0;
      return false;
    }
    props.push(p);
    return true;
  };

  // 街灯は 2) で立てなおすので、家をずらす前にはずしておく（家の置き場所をせばめないように）
  for (const p of props.filter((q) => q.kind === "lamp")) remove(p);
  // 1.5) 絵（屋根・壁）が歩道（道）にかかる家は、近くの、道にかからない所へ少しずらす（2026-10-06 人間の指示
  //      「一部花壇、家が歩道に重なってるから少し離して」）。玄関の前は、通れて、町の出入り口から歩いて行けるまま
  const reachSet = (): Set<number> => {
    const seen = new Set<number>();
    for (const e of exits) {
      const q = [e.tileY * w + e.tileX];
      seen.add(q[0]);
      for (let i = 0; i < q.length; i++) {
        const x = q[i] % w, y = Math.floor(q[i] / w);
        for (const [ddx, ddy] of AROUND) {
          const nx = x + ddx, ny = y + ddy, ni = ny * w + nx;
          if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen.has(ni) || col[ni] === 1 || npcAt.has(ni)) continue;   // 人の立つマスも通れない
          seen.add(ni);
          q.push(ni);
        }
      }
    }
    return seen;
  };
  const rebuildDoorFront = (): void => {
    doorFront.clear();
    for (const p of props) if (isHouse(p.kind)) for (let k = 1; k <= 2; k++) for (const ox of [-1, 0, 1]) doorFront.add((p.tileY + k) * w + p.tileX + doorOffsetX(p.kind) + ox);
  };
  //      軒がほかの建物とくっつく（重なる）家も、同じようにずらす（2026-10-06 人間の指示「そこも直して」）。屋敷・教会は動かさない
  const roomy = (b: Box): Box => ({ x0: b.x0 - 12, x1: b.x1 + 12, y0: b.y0 - 8, y1: b.y1 + 8 });
  const crowded = (p: MapProp): boolean => {
    const b = boxOf(p, ts);
    return !!b && props.some((q) => q !== p && (isHouse(q.kind) || q.kind === "church") && !!boxOf(q, ts) && overlaps(roomy(b), boxOf(q, ts)!));
  };
  for (const p of props.filter((q) => isHouse(q.kind) && !q.kind.startsWith("manor"))) {
    if (!props.includes(p) || !(onPathPx(p) > 20 || crowded(p))) continue;
    remove(p);
    rebuildDoorFront();
    let moved = false;
    // まず1〜2マスのずらし、だめなら、もう少しはなれた空き地（よこ12・たて10マスまで。近い順）
    const shifts: Array<[number, number]> = [[0, 1], [-1, 0], [1, 0], [-1, 1], [1, 1], [0, 2], [-2, 0], [2, 0], [0, -1]];
    const far: Array<[number, number]> = [];
    for (let dy = -10; dy <= 10; dy++) for (let dx = -12; dx <= 12; dx++) if (!shifts.some(([a, c]) => a === dx && c === dy) && (dx || dy)) far.push([dx, dy]);
    far.sort((a, c) => Math.hypot(a[0], a[1]) - Math.hypot(c[0], c[1]));
    // 1マスほどの間をあけられないときは、少しの間（軒がふれない）で、もう一度
    for (const [mx, my] of [[12, 8], [4, 3]]) {
    if (moved) break;
    for (const [dx, dy] of [...shifts, ...far]) {
      const n: MapProp = { kind: p.kind, tileX: p.tileX + dx, tileY: p.tileY + dy };
      if (onPathPx(n) > 20) continue;
      const doorX = n.tileX + doorOffsetX(n.kind), doorY = n.tileY + 1;
      if (ring(doorX, doorY) || col[doorY * w + doorX] === 1 || art(doorX, doorY) === "water") continue;
      // ほかの建物とは、1マスほど間をあける（軒が重ならないように）
      const nb = boxOf(n, ts);
      if (nb && props.some((q) => (isHouse(q.kind) || q.kind === "church") && boxOf(q, ts) && overlaps({ x0: nb.x0 - mx, x1: nb.x1 + mx, y0: nb.y0 - my, y1: nb.y1 + my }, boxOf(q, ts)!))) continue;
      if (!tryPlace(n.kind, n.tileX, n.tileY, false, true)) continue;
      if (!reachSet().has(doorY * w + doorX)) {
        remove(props[props.length - 1]);
        continue;
      }
      moved = true;
      break;
    }
    }
    if (!moved) {
      props.push(p);                                                       // ずらせなければ、もとの所のまま
      for (const t of propFootprintTiles(p)) col[t.y * w + t.x] = 1;
      // 家のうしろを通る道が屋根の下にかかるときは、道のほうを1マス上へ曲げて、家からはなす（見た目だけ。通れる所は変えない）
      const b = boxOf(p, ts);
      const top = Math.min(...propFootprintTiles(p).map((t) => t.y));
      if (b) {
        const tx0 = Math.floor((b.x0 + 1) / ts), tx1 = Math.floor((b.x1 - 1) / ts);
        const used = footSet(props);
        const okUp = (x: number, y: number): boolean => y - 1 > 0 && !ring(x, y - 1) && col[(y - 1) * w + x] === 0 && !used.has((y - 1) * w + x) && art(x, y - 1) !== "water";
        for (let ty = Math.floor((b.y0 + 3) / ts); ty < top; ty++) {
          const xs: number[] = [];
          for (let x = tx0; x <= tx1; x++) if (art(x, ty) === "path") xs.push(x);
          if (!xs.length || !xs.every((x) => okUp(x, ty) && art(x, ty - 1) !== "path")) continue;
          for (const x of xs) {
            const i = ty * w + x, j = (ty - 1) * w + x;
            [ground[i], ground[j]] = [ground[j], ground[i]];
          }
          for (const x of [tx0 - 1, tx1 + 1]) {                           // 曲がりかどを、ななめにつなぐ
            if (x > 0 && x < w - 1 && art(x, ty) === "path" && okUp(x, ty)) ground[(ty - 1) * w + x] = ground[ty * w + x];
          }
        }
      }
    }
    rebuildDoorFront();
  }

  // 2) 街灯: いまの街灯をはずし、道にそって決まった間かくで立てなおす
  for (const p of props.filter((q) => q.kind === "lamp")) remove(p);
  const road = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && art(x, y) === "path";
  const lamps: Array<[number, number]> = [];
  for (let y = 1; y < h - 1; y++) {
    for (let x = 1; x < w - 1; x++) {
      if (!road(x, y)) continue;
      const horiz = road(x - 1, y) && road(x + 1, y);
      const vert = road(x, y - 1) && road(x, y + 1);
      // 2026-10-06 人間の指示「いろんな町に街灯を増やそう」: 6マスごと → 4マスごと
      if (horiz && !vert && x % 4 === 2 && !road(x, y - 1)) lamps.push([x, y - 1]);
      if (vert && !horiz && y % 4 === 2 && !road(x + 1, y)) lamps.push([x + 1, y]);
    }
  }
  const lampNear = (x: number, y: number, d: number): boolean => props.some((q) => q.kind === "lamp" && Math.abs(q.tileX - x) + Math.abs(q.tileY - y) < d);
  for (const [x, y] of lamps) {
    if (lampNear(x, y, 3)) continue;
    tryPlace("lamp", x, y);
  }
  // 家の玄関の前の、左か右に1本（石だたみの町など、土の道のない町にも街灯が立つように）
  for (const p of props.filter((q) => isHouse(q.kind))) {
    const dx0 = p.tileX + doorOffsetX(p.kind);
    const sides = hn32(p.tileX, p.tileY) % 2 === 0 ? [-2, 2, -3, 3] : [2, -2, 3, -3];
    for (const sx of sides) {
      const x = dx0 + sx, y = p.tileY + 1;
      if (lampNear(x, y, 3)) break;
      if (tryPlace("lamp", x, y)) break;
    }
  }

  // 3) 花壇: 家の玄関の左右に、そろえて。家のそばにない花壇（家を取りのぞいたあとに残ったものなど）は、はずす
  //    花壇の絵が歩道（道）にかかる所には置かず、1マス外（家から3マス）へずらす。それでもかかるなら置かない
  //    （2026-10-06 人間の指示「一部花壇、家が歩道に重なってるから少し離して」）
  const besideHouse = (f: MapProp): boolean => props.some((q) => isHouse(q.kind) && q.tileY === f.tileY && [2, 3].includes(Math.abs(q.tileX - f.tileX)));
  for (const f of props.filter((q) => q.kind === "flowerbed" && (!besideHouse(q) || onPathPx(q) > 0))) remove(f);
  for (const p of props.filter((q) => isHouse(q.kind) && !q.kind.startsWith("manor"))) {
    for (const side of [-1, 1]) {
      if (props.some((q) => q.kind === "flowerbed" && q.tileY === p.tileY && (q.tileX === p.tileX + side * 2 || q.tileX === p.tileX + side * 3))) continue;
      for (const dx of [side * 2, side * 3]) {
        if (onPathPx({ kind: "flowerbed", tileX: p.tileX + dx, tileY: p.tileY }) > 0) continue;
        if (tryPlace("flowerbed", p.tileX + dx, p.tileY)) break;
      }
    }
  }

  // 3.2) 樽・井戸は家の近くへ、屋台は道の上へ
  const houseTiles = (): Array<[number, number]> => props.filter((q) => isHouse(q.kind)).flatMap((q) => propFootprintTiles(q).map((t): [number, number] => [t.x, t.y]));
  const houseDist = (x: number, y: number, hs: Array<[number, number]>): number =>
    hs.reduce((m, [hx, hy]) => Math.min(m, Math.max(Math.abs(hx - x), Math.abs(hy - y))), 99);
  // 井戸は家から少しはなす（あいだに1マスあける。2026-10-06 人間の指示「家の近くの井戸は少し離しましょう」）。樽は家のすぐとなり
  // 井戸の絵と、家・花壇の絵とのあいだ（ドット）。家の絵は足もとのマスより横に広く、花壇も玄関の横にあるので、絵どうしではかる
  const gapPx = (a: Box, b: Box): number => Math.max(Math.max(a.x0, b.x0) - Math.min(a.x1, b.x1), Math.max(a.y0, b.y0) - Math.min(a.y1, b.y1));
  const wellGapOk = (x: number, y: number): boolean => {
    const wb = boxOf({ kind: "well", tileX: x, tileY: y }, ts);
    if (!wb) return true;
    if (wb.y0 < ts + 4) return false;                                     // 上の塀に、屋根がかからない所
    if (props.some((q) => q.kind !== "flowerbed" && !isHouse(q.kind) && q !== undefined && boxOf(q, ts) && gapPx(wb, boxOf(q, ts)!) < 4 && !(q.tileX === x && q.tileY === y))) return false;   // ほかの飾りとも、少しあける
    const near = props.filter((q) => isHouse(q.kind) || q.kind === "flowerbed").map((q) => boxOf(q, ts)).filter((b): b is Box => !!b);
    return near.every((b) => gapPx(wb, b) >= 10) && near.some((b) => gapPx(wb, b) <= 40);
  };
  // 井戸のない町には、井戸を1つ置く（2026-10-06 人間の指示「井戸も置こう」）。町のまんなかに近い家のそばへ
  const wellTarget: MapProp[] = props.some((q) => q.kind === "well") ? [] : [{ kind: "well", tileX: Math.floor(w / 2), tileY: Math.floor(h / 2) }];
  for (const [kind, minD, maxD] of [["well", 2, 3], ["barrel", 1, 1]] as const) {
    for (const p of [...props.filter((q) => q.kind === kind), ...(kind === "well" ? wellTarget : [])]) {
      const hs = houseTiles();
      const isNew = !props.includes(p);
      const d0 = houseDist(p.tileX, p.tileY, hs);
      if (!isNew && d0 >= minD && d0 <= maxD && (kind !== "well" || wellGapOk(p.tileX, p.tileY))) continue;
      if (!isNew) remove(p);
      const cands: Array<[number, number, number]> = [];
      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          const d = houseDist(x, y, hs);
          // 玄関の前の列（玄関から左右3マス）は、宿屋の看板などのためにあけておく
          const front = props.some((q) => isHouse(q.kind) && y === q.tileY + 1 && Math.abs(x - q.tileX - doorOffsetX(q.kind)) <= 3);
          if (d >= minD && d <= maxD && !front && (kind !== "well" || wellGapOk(x, y))) cands.push([x, y, d * 100 + Math.abs(x - p.tileX) + Math.abs(y - p.tileY)]);
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

  // 3.6) 門柱・すみの柱に絵がかかる飾り（建物はのぞく）は、近くへずらす。置ける所がなければ、はずす
  //      （2026-10-06 人間の指示「灯の町の入って左側の木も柱に食い込んでるから直して」）
  for (const p of [...props]) {
    if (isHouse(p.kind) || p.kind === "church" || p.kind === "flowerbed") continue;
    const b = boxOf(p, ts);
    if (!b || !posts.some((o) => overlaps(b, o))) continue;
    remove(p);
    const cands: Array<[number, number]> = [];
    for (let dy = -3; dy <= 1; dy++) for (let dx = -3; dx <= 3; dx++) if (dx || dy) cands.push([p.tileX + dx, p.tileY + dy]);
    cands.sort((a, c) => Math.hypot(a[0] - p.tileX, (a[1] - p.tileY) * 1.2) - Math.hypot(c[0] - p.tileX, (c[1] - p.tileY) * 1.2));
    for (const [x, y] of cands) if (tryPlace(p.kind, x, y)) break;
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
  // 5) 木は3本以上・街灯は4本以上（2026-10-06 人間の指示「いろんな町に街灯を増やそう」「あと木も3本は置くようにしよう」）。
  //      木の種類は、その町にもとからある木（気候に合わせた木）にそろえる。足りない分は、塀ぎわの空いた所に、間をあけて置く
  const TREEISH = ["tree", "tree-pine", "tree-snow", "tree-dead", "palm"];
  const treeCount = (): number => props.filter((q) => TREEISH.includes(q.kind)).length;
  if (treeCount() < 3) {
    const have: Record<string, number> = {};
    for (const q of props) if (TREEISH.includes(q.kind) && q.kind !== "tree-dead") have[q.kind] = (have[q.kind] ?? 0) + 1;
    const kindT = (Object.entries(have).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "tree") as MapPropKind;
    const cands: Array<[number, number, number]> = [];
    for (let y = 3; y < h - 2; y++) {
      for (let x = 2; x < w - 2; x++) {
        if (road(x, y)) continue;
        const edge = Math.min(x - 1, w - 2 - x, h - 2 - y);         // 塀からの近さ（上の塀ぎわは、絵が塀にかかるのでさける）
        cands.push([x, y, edge * 10 + (hn32(x, y) % 7)]);
      }
    }
    cands.sort((a, c) => a[2] - c[2]);
    // 置けなければ、木と木の間を少しつめて、もう一度。それでも足りない町（家と水でせまい町）は、絵の細い針葉樹で
    for (const [gap, k] of [[5, kindT], [3, kindT], [3, kindT === "tree" ? "tree-pine" : kindT]] as Array<[number, MapPropKind]>) {
      for (const [x, y] of cands) {
        if (treeCount() >= 3) break;
        if (props.some((q) => TREEISH.includes(q.kind) && Math.max(Math.abs(q.tileX - x), Math.abs(q.tileY - y)) < gap)) continue;
        tryPlace(k, x, y);
      }
    }
  }
  if (props.filter((q) => q.kind === "lamp").length < 4) {
    const cx = w / 2, cy = h / 2;
    const cands: Array<[number, number]> = [];
    for (let y = 2; y < h - 2; y++) for (let x = 2; x < w - 2; x++) if ((x + 2 * y) % 5 === 0) cands.push([x, y]);
    cands.sort((a, c) => Math.hypot(a[0] - cx, a[1] - cy) - Math.hypot(c[0] - cx, c[1] - cy));
    for (const [x, y] of cands) {
      if (props.filter((q) => q.kind === "lamp").length >= 4) break;
      if (lampNear(x, y, 5)) continue;
      tryPlace("lamp", x, y);
    }
  }

  // 噴水のない町には、町のまんなかに近い空き地に、噴水を1つ置く（2026-10-06 人間の指示「各町噴水も置こうか」）。
  // 道の上・家の軒のすぐそばはさける
  if (!props.some((q) => q.kind === "fountain")) {
    const cx = w / 2, cy = h / 2;
    const cands: Array<[number, number]> = [];
    for (let y = 3; y < h - 2; y++) for (let x = 2; x < w - 2; x++) cands.push([x, y]);
    cands.sort((a, c) => Math.hypot(a[0] - cx, (a[1] - cy) * 1.3) - Math.hypot(c[0] - cx, (c[1] - cy) * 1.3));
    // 置けないせまい町は、家とのあいだを少しつめ、人のすぐそばでも置けるようにして、もう一度
    let placed = false;
    for (const [gap, nearOk] of [[8, false], [3, true]] as const) {
      for (const [x, y] of cands) {
        if (placed) break;
        const fb = boxOf({ kind: "fountain", tileX: x, tileY: y }, ts);
        if (!fb || fb.y0 < ts + 4) continue;
        if (props.some((q) => (isHouse(q.kind) || q.kind === "church" || q.kind === "flowerbed") && boxOf(q, ts) && Math.max(Math.max(fb.x0, boxOf(q, ts)!.x0) - Math.min(fb.x1, boxOf(q, ts)!.x1), Math.max(fb.y0, boxOf(q, ts)!.y0) - Math.min(fb.y1, boxOf(q, ts)!.y1)) < gap)) continue;
        placed = tryPlace("fountain", x, y, false, nearOk);
      }
    }
    // それでも置けないときは、じゃまになる小さな飾り（ベンチ・岩・樽など）をどけて置く
    for (const [x, y] of cands) {
      if (placed) break;
      const fb = boxOf({ kind: "fountain", tileX: x, tileY: y }, ts);
      if (!fb || fb.y0 < ts + 4) continue;
      if (props.some((q) => (isHouse(q.kind) || q.kind === "church" || q.kind === "flowerbed") && boxOf(q, ts) && overlaps({ x0: fb.x0 - 3, x1: fb.x1 + 3, y0: fb.y0 - 3, y1: fb.y1 + 3 }, boxOf(q, ts)!))) continue;
      const fp = new Set(propFootprintTiles({ kind: "fountain", tileX: x, tileY: y }).map((t) => t.y * w + t.x));
      const small = props.filter((q) => PRIORITY(q.kind) <= 40 && q.kind !== "flowerbed" && ((boxOf(q, ts) && overlaps(fb, boxOf(q, ts)!)) || propFootprintTiles(q).some((t) => fp.has(t.y * w + t.x))));
      if (!small.length) continue;
      for (const q of small) remove(q);
      placed = tryPlace("fountain", x, y, false, true);
      if (!placed) for (const q of small) { props.push(q); for (const t of propFootprintTiles(q)) col[t.y * w + t.x] = 1; }
    }
  }

  // 重なりで家を取りのぞいたあとに残った花壇も、はずす
  for (const f of props.filter((q) => q.kind === "flowerbed" && !besideHouse(q))) remove(f);
  // 描く順（地図ぜんたいの絵など、並べ替えずに描く所のため）: 奥の列から。同じ列では、家 → 花壇 → 街灯などの順
  // （2026-10-06 人間の指示「灯と花壇が重なっていて灯のが前にこなきゃいけない」「花壇は家より前だよ」）
  const rank = (q: MapProp): number => (isHouse(q.kind) || q.kind === "church" ? 0 : q.kind === "flowerbed" ? 1 : 2);
  data.props = props.map((q, i) => ({ q, i })).sort((a, b) => a.q.tileY - b.q.tileY || rank(a.q) - rank(b.q) || a.i - b.i).map((e) => e.q);
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

/** 町の塀の柱に、絵がかかっている飾り（建物・花壇はのぞく。テスト用）。 */
export function townPostOverlaps(data: TileMapData): string[] {
  const ts = data.tileWidth;
  const posts = townPostBoxes(data);
  const out: string[] = [];
  for (const p of data.props ?? []) {
    if (isHouse(p.kind) || p.kind === "church" || p.kind === "flowerbed") continue;
    const b = boxOf(p, ts);
    if (b && posts.some((o) => overlaps(b, o))) out.push(`${p.kind}(${p.tileX},${p.tileY})`);
  }
  return out;
}

/** 町の、絵が歩道（道）にかかっている家・花壇（テスト用）。ふちの1ドットと屋根のてっぺんの3ドットは数えない。 */
export function townPathOverlaps(data: TileMapData): string[] {
  const ts = data.tileWidth, w = data.width, h = data.height;
  const ground = data.layers[0].data;
  const out: string[] = [];
  for (const p of data.props ?? []) {
    if (!isHouse(p.kind) && p.kind !== "flowerbed") continue;
    const b = boxOf(p, ts);
    if (!b) continue;
    let n = 0;
    for (let y = b.y0 + 3; y < b.y1; y++) for (let x = b.x0 + 1; x < b.x1; x++) {
      const tx = Math.floor(x / ts), ty = Math.floor(y / ts);
      if (tx >= 0 && ty >= 0 && tx < w && ty < h && data.tileArt?.[ground[ty * w + tx]] === "path") n++;
    }
    if (n > (p.kind === "flowerbed" ? 0 : 20)) out.push(`${p.kind}(${p.tileX},${p.tileY}) ${n}`);
  }
  return out;
}

/** 町の、軒がほかの建物とくっつく（1マスほどの間がない）家（テスト用）。 */
export function townCrowdedHouses(data: TileMapData): string[] {
  const ts = data.tileWidth;
  const bs = (data.props ?? []).filter((p) => isHouse(p.kind) || p.kind === "church").map((p) => ({ p, b: boxOf(p, ts) })).filter((e): e is { p: MapProp; b: Box } => !!e.b);
  const out: string[] = [];
  for (let i = 0; i < bs.length; i++) for (let j = 0; j < i; j++) {
    const a = bs[i].b;
    if (overlaps({ x0: a.x0 - 12, x1: a.x1 + 12, y0: a.y0 - 8, y1: a.y1 + 8 }, bs[j].b)) out.push(`${bs[i].p.kind}(${bs[i].p.tileX},${bs[i].p.tileY}) × ${bs[j].p.kind}(${bs[j].p.tileX},${bs[j].p.tileY})`);
  }
  return out;
}
