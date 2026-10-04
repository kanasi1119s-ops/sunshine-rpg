import { hashCell } from "../color-utils";
import type { Npc } from "../npc";
import { TOWN_OLD_WIDTH } from "./town-expand";
import { isHouse, propFootprintTiles, propOverhangTiles } from "./map-props";
import type { MapProp, MapPropKind, TileMapData } from "./types";
import type { EventCommand } from "../event/types";

/**
 * 町・村を「王道のRPGの町」らしくする（2026-10-04、人間の依頼）。
 * もとの地図は、広い空き地に家が数軒だけで、がらんとしていた。町の大通り（道）の両わきに、家（屋根の色ちがい）を
 * 並べ、広場に井戸・噴水・ベンチ・花壇を置き、通りに街灯を立て、すみに木を植える。
 * 置くときは、出入り口・人のいるマス・そこへ歩く道がふさがれないようにする（ふさぐ位置はあきらめる）。毎回同じ位置になる。
 */
const HOUSE_KINDS: MapPropKind[] = ["house", "house-blue", "house-green", "house", "house-blue", "house-green"];
const AROUND: Array<[number, number]> = [[1, 0], [-1, 0], [0, 1], [0, -1]];

/** 町・村の地図か（ダンジョンや屋内は除く）。 */
function isTown(mapId: string): boolean {
  return (/-(town|village)$/.test(mapId) || /^village-/.test(mapId)) && mapId !== "world-map";
}

export function applyTownDecor(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    if (!isTown(mapId) || !data.collision) continue;
    const w = data.width;
    const h = data.height;
    const collision = data.collision;
    const ground = data.layers[0].data;
    const npcs = npcsByMap[mapId] ?? [];
    const exits = data.exits ?? [];
    const art = (x: number, y: number): string | undefined => data.tileArt?.[ground[y * w + x]];
    const inMap = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h;
    const isRoad = (x: number, y: number): boolean => inMap(x, y) && art(x, y) === "path";
    const isOpen = (x: number, y: number): boolean => inMap(x, y) && collision[y * w + x] === 0 && art(x, y) !== "water";
    const props: MapProp[] = [...(data.props ?? [])];
    const occupied = new Set<number>();
    for (const p of props) for (const t of propFootprintTiles(p)) occupied.add(t.y * w + t.x);
    const nearNpcOrExit = (x: number, y: number, rx: number, ryUp: number, ryDown: number): boolean =>
      npcs.some((n) => n.tileX >= x - rx && n.tileX <= x + rx && n.tileY >= y - ryUp && n.tileY <= y + ryDown) ||
      exits.some((e) => e.tileX >= x - rx && e.tileX <= x + rx && e.tileY >= y - ryUp && e.tileY <= y + ryDown);

    // ふつうの地面（いちばん多い歩ける地面）。家の下は、これにする
    const counts = new Map<number, number>();
    for (let i = 0; i < ground.length; i++) if (!collision[i]) counts.set(ground[i], (counts.get(ground[i]) ?? 0) + 1);
    const baseId = [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] ?? ground[0];

    const reachable = (): boolean => {
      const start = exits[0];
      if (!start) return true;
      const seen = new Set<number>([start.tileY * w + start.tileX]);
      const stack: Array<[number, number]> = [[start.tileX, start.tileY]];
      while (stack.length) {
        const [x, y] = stack.pop()!;
        for (const [dx, dy] of AROUND) {
          const nx = x + dx;
          const ny = y + dy;
          if (!inMap(nx, ny) || collision[ny * w + nx] === 1 || seen.has(ny * w + nx)) continue;
          seen.add(ny * w + nx);
          stack.push([nx, ny]);
        }
      }
      const ok = (x: number, y: number): boolean => seen.has(y * w + x);
      return exits.every((e) => ok(e.tileX, e.tileY)) && npcs.every((n) => AROUND.some(([dx, dy]) => ok(n.tileX + dx, n.tileY + dy)));
    };

    const place = (kind: MapPropKind, x: number, y: number): boolean => {
      const tiles = propFootprintTiles({ kind, tileX: x, tileY: y });
      const house = isHouse(kind);
      if (house && y < 3) return false; // 絵が画面の外へ切れる
      if (tiles.length === 0) return false;
      for (const t of tiles) {
        if (!isOpen(t.x, t.y) || isRoad(t.x, t.y) || occupied.has(t.y * w + t.x)) return false;
        // 道のまんなかや、扉の前をふさがない（家は、足元の1マス下が道か広場）
      }
      // 家は絵が上へはみ出す。人・出入り口とは、まわり2マス＋上2マスあける
      if (house ? nearNpcOrExit(x, y, 2, 2, 1) : nearNpcOrExit(x, y, 1, 1, 1)) return false;
      for (const t of tiles) collision[t.y * w + t.x] = 1;
      if (!reachable()) {
        for (const t of tiles) collision[t.y * w + t.x] = 0;
        return false;
      }
      for (const t of tiles) {
        occupied.add(t.y * w + t.x);
        if (house) ground[t.y * w + t.x] = baseId;
      }
      props.push({ kind, tileX: x, tileY: y });
      return true;
    };

    let open = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (isOpen(x, y)) open++;
    const existingHouses = props.filter((p) => isHouse(p.kind)).length;
    const wantHouses = Math.max(0, Math.min(9, Math.round(open / 30)) - existingHouses);

    // 1) 家: 道に面した場所（足元の下・左右が道か、道のすぐわき）から、まばらに選んで並べる。間は横4マス・縦3マスあける
    const spots: Array<[number, number]> = [];
    for (let y = 3; y < h - 1; y++) {
      for (let x = 1; x < w - 1; x++) {
        if (!isOpen(x, y) || isRoad(x, y)) continue;
        // 足元のすぐ下が道（＝玄関が道に面している）
        const nearRoad = [1, 2, 3].some((d) => isRoad(x, y + d)) || [-3, -2, 2, 3].some((d) => isRoad(x + d, y));
        if (nearRoad) spots.push([x, y]);
      }
    }
    let idSalt = 0;
    for (let i = 0; i < mapId.length; i++) idSalt = (idSalt * 31 + mapId.charCodeAt(i)) % 9973;
    const order = (list: Array<[number, number]>, salt: number): Array<[number, number]> =>
      [...list].sort((a, b) => hashCell(a[0] * 31 + salt + idSalt, a[1] * 17) - hashCell(b[0] * 31 + salt + idSalt, b[1] * 17));
    let housesPlaced = 0;
    let n = 0;
    for (const [x, y] of order(spots, 41)) {
      if (housesPlaced >= wantHouses) break;
      if (props.some((p) => isHouse(p.kind) && Math.abs(p.tileX - x) <= 3 && Math.abs(p.tileY - y) <= 2)) continue;
      if (place(HOUSE_KINDS[hashCell(x + n, y) % HOUSE_KINDS.length], x, y)) housesPlaced++;
      n++;
    }

    // 2) 広場の井戸（なければ）: 道が交わるあたり（道のマスの、すぐとなり）
    const hasKind = (...kinds: string[]): boolean => props.some((p) => kinds.includes(p.kind));
    const roadAdjacent: Array<[number, number]> = [];
    for (let y = 2; y < h - 2; y++) {
      for (let x = 2; x < w - 2; x++) {
        if (!isOpen(x, y) || isRoad(x, y)) continue;
        const roads = AROUND.filter(([dx, dy]) => isRoad(x + dx, y + dy)).length;
        if (roads >= 1) roadAdjacent.push([x, y]);
      }
    }
    const centerX = w / 2;
    const centerY = h / 2;
    const byCenter = [...roadAdjacent].sort((a, b) => Math.hypot(a[0] - centerX, a[1] - centerY) - Math.hypot(b[0] - centerX, b[1] - centerY));
    if (!hasKind("well", "fountain")) {
      for (const [x, y] of byCenter) if (place("well", x, y)) break;
    }
    // 3) 街灯: 道のわきに、間をあけて（5マス）
    let lamps = 0;
    for (const [x, y] of order(roadAdjacent, 7)) {
      if (lamps >= 3) break;
      if (props.some((p) => p.kind === "lamp" && Math.hypot(p.tileX - x, p.tileY - y) < 6)) continue;
      if (place("lamp", x, y)) lamps++;
    }
    // 4) 花壇（家の足元のすぐ横）とベンチ
    const houses = props.filter((p) => isHouse(p.kind));
    let beds = 0;
    for (const hp of houses) {
      if (beds >= 5) break;
      for (const dx of [-2, 2]) {
        if (place("flowerbed", hp.tileX + dx, hp.tileY)) {
          beds++;
          break;
        }
      }
    }
    let benches = 0;
    for (const [x, y] of byCenter) {
      if (benches >= 1) break;
      if (props.some((p) => p.kind === "bench")) break;
      if (place("bench", x, y)) benches++;
    }
    data.props = props;

    // 5) 広げた東の区域に、町の人を3人（ぶらぶら歩く）。道や広場のあいたマスに置く
    const oldW = TOWN_OLD_WIDTH.get(mapId);
    if (oldW !== undefined) {
      const lines = [
        "ここは、旅の人がよく通る町だよ。ゆっくりしていってね。",
        "市場の品は、朝がいちばん新鮮なの。夕方には売り切れちゃうのよ。",
        "大通りの東にも、家がふえてね。ずいぶん、にぎやかになったもんだ。",
        "宿屋のスープは、この町いちばんの自慢さ。",
        "このごろ、灯り石の光が、ほんの少しちらつくんだ。気のせいかな。",
        "子どもたちは、広場で毎日かけっこしてるよ。元気なのは、いいことさ。",
      ];
      const colors = ["#c08060", "#6a8ab0", "#a0a070", "#b07090", "#7a9a6a"];
      const taken = new Set(npcs.map((n) => `${n.tileX},${n.tileY}`));
      const cand: Array<[number, number]> = [];
      for (let y = 2; y < h - 2; y++) {
        for (let x = oldW + 1; x < w - 2; x++) {
          if (isOpen(x, y) && !occupied.has(y * w + x) && AROUND.every(([dx, dy]) => !occupied.has((y + dy) * w + x + dx))) cand.push([x, y]);
        }
      }
      const list = npcsByMap[mapId] ?? (npcsByMap[mapId] = []);
      let made = 0;
      for (const [x, y] of order(cand, 91)) {
        if (made >= 3) break;
        if (taken.has(`${x},${y}`) || [...taken].some((t) => { const [tx, ty] = t.split(",").map(Number); return Math.abs(tx - x) + Math.abs(ty - y) < 4; })) continue;
        const idx = (hashCell(x + idSalt, y) + made) % lines.length;
        list.push({
          id: `${mapId}-townsfolk-${made + 1}`,
          tileX: x,
          tileY: y,
          color: colors[(hashCell(y, x + idSalt) + made) % colors.length],
          wander: true,
          commands: [{ type: "message", text: lines[idx], speaker: "町の人" }],
        });
        taken.add(`${x},${y}`);
        made++;
      }
    }

    // 6) 宿屋の主人。すでにいる人（宿屋の主人）にはとまる選択を足し、いない町は、町の広場の近くに1人置く
    addInnkeeper(mapId, data, npcsByMap, { occupied, isOpen, inMap, nearNpcOrExit });
  }
}

/** 宿代（灯貨）。町ごと。物語が進む町ほど高い。 */
const INN_PRICES: Record<string, number> = {
  "touri-town": 8, "mugikano-village": 12, "garasuko-town": 16, "tetsukusari-town": 20, "sanone-town": 24,
  "kiri-town": 28, "shimohara-town": 32, "fushima-town": 36, "toushin-town": 40,
};

function addInnkeeper(
  mapId: string,
  data: TileMapData,
  npcsByMap: Record<string, Npc[]>,
  g: { occupied: Set<number>; isOpen: (x: number, y: number) => boolean; inMap: (x: number, y: number) => boolean; nearNpcOrExit: (x: number, y: number, rx: number, ryUp: number, ryDown: number) => boolean },
): void {
  const price = INN_PRICES[mapId] ?? 20;
  const list = npcsByMap[mapId] ?? (npcsByMap[mapId] = []);
  const inn: EventCommand = { type: "inn", price };
  const existing = list.find((n) => /-innkeeper$/.test(n.id));
  if (existing) {
    if (!existing.commands.some((c) => c.type === "inn")) existing.commands = [...existing.commands, inn];
    return;
  }
  const w = data.width, h = data.height;
  const cx = w / 2, cy = h / 2;
  // 絵がはみ出す上のマス（奥に隠れてしまう）にも置かない
  const hidden = new Set<number>();
  for (const prop of data.props ?? []) {
    const tiles = propFootprintTiles(prop);
    if (!tiles.length) continue;
    const top = Math.min(...tiles.map((t) => t.y)) - propOverhangTiles(prop.kind, data.tileHeight);
    const pad = prop.kind === "tree" ? 1 : 0;
    const x0 = Math.min(...tiles.map((t) => t.x)) - pad, x1 = Math.max(...tiles.map((t) => t.x)) + pad;
    for (let yy = top; yy <= prop.tileY; yy++) for (let xx = x0; xx <= x1; xx++) hidden.add(yy * w + xx);
  }
  const cand: Array<[number, number]> = [];
  for (let y = 2; y < h - 2; y++) {
    for (let x = 2; x < w - 2; x++) {
      if (!g.isOpen(x, y) || g.occupied.has(y * w + x)) continue;
      if (!AROUND.every(([dx, dy]) => g.inMap(x + dx, y + dy) && g.isOpen(x + dx, y + dy) && !g.occupied.has((y + dy) * w + x + dx))) continue;
      if (g.nearNpcOrExit(x, y, 2, 2, 2) || [[0, 0], ...AROUND].some(([dx, dy]) => hidden.has((y + dy) * w + x + dx))) continue;
      cand.push([x, y]);
    }
  }
  cand.sort((a, b) => Math.hypot(a[0] - cx, a[1] - cy) - Math.hypot(b[0] - cx, b[1] - cy));
  const spot = cand[0];
  if (!spot) return;
  list.push({
    id: `${mapId}-innkeeper`,
    tileX: spot[0],
    tileY: spot[1],
    color: "#b08a5a",
    commands: [{ type: "message", text: "旅の人かい？ うちの宿で、ゆっくり休んでいきなよ。", speaker: "宿屋の主人" }, inn],
  });
}
