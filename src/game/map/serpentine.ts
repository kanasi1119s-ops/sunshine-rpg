import type { CarveSpec, Rect } from "./carve-map";

/**
 * 長く続くダンジョン・森の地図（フィールドを旅するように、折れ曲がる長い道を歩く）の形を作る。
 * 横に長い通路（レーン）を何本も上下にならべ、左右のはしで、つなぐ（蛇行する一本道）。レーンのあいだには、
 * 行き止まりの小部屋（宝箱・仕掛けを置く寄り道）をいくつか彫る。形は、決まった数字（seed）から毎回同じに決まる。
 * 入り口は下の中央ぎわ、出口は上のすみ。
 */
export interface SerpentineOptions {
  /** 通路の本数。 */
  lanes: number;
  /** 壁（通れない）のタイル。 */
  wall: number;
  /** 床のタイル。 */
  floor: number;
  /** 道のタイル（あれば、通路の中央に引く）。 */
  path?: number;
  /** 同じ形の地図でも、小部屋の位置を変える数字。 */
  seed: number;
  width?: number;
}

export interface Landmarks {
  /** 小部屋の中ほどのマス（宝箱・仕掛けを置ける）。入り口に近い順。 */
  alcoves: { tileX: number; tileY: number }[];
  /** 入り口（下の出入り口のマス）と、そこから入ったときの立ち位置。 */
  south: { x: number; y: number };
  southArrival: { tileX: number; tileY: number };
  /** 出口（上の出入り口のマス）と、そこへ戻ってきたときの立ち位置。 */
  north: { x: number; y: number };
  northArrival: { tileX: number; tileY: number };
  /** 入り口ちかくの、道ばた（旅人などを置く）。 */
  nearEntry: { tileX: number; tileY: number };
  /** 出口ちかくの、道ばた（石碑などを置く）。 */
  nearExit: { tileX: number; tileY: number };
  /** 道の長さの目安（マスの数）。 */
  pathLength: number;
}

export interface SerpentineLayout {
  width: number;
  height: number;
  spec: CarveSpec;
  landmarks: Landmarks;
}

function rng(seed: number): () => number {
  let s = (seed * 2654435761) >>> 0;
  return () => {
    s = (s ^ (s << 13)) >>> 0;
    s = (s ^ (s >>> 17)) >>> 0;
    s = (s ^ (s << 5)) >>> 0;
    return (s >>> 0) / 4294967296;
  };
}

const LANE_SPACING = 7;

export function serpentineLayout(opts: SerpentineOptions): SerpentineLayout {
  const W = opts.width ?? 46;
  const L = opts.lanes;
  const H = 12 + LANE_SPACING * (L - 1);
  const rand = rng(opts.seed);
  const centers = Array.from({ length: L }, (_, i) => H - 6 - LANE_SPACING * i); // 下から上へ
  const left = 3;
  const right = W - 4;
  const rooms: Rect[] = [];
  const pathPoints: [number, number][] = [];
  const xs = Math.round(W / 2) - 8 + Math.floor(rand() * 6);
  const xe = W - 10;

  // 通路（高さ3）
  for (const y of centers) rooms.push({ x: left, y: y - 1, w: right - left + 1, h: 3 });
  // つなぎ（はばは3）。下から数えて、偶数のつなぎは右のはし、奇数は左のはし
  for (let i = 0; i < L - 1; i++) {
    const cx = i % 2 === 0 ? right - 4 : left + 1;
    rooms.push({ x: cx, y: centers[i + 1] - 1, w: 3, h: centers[i] - centers[i + 1] + 3 });
  }
  // 入り口・出口への通路
  rooms.push({ x: xs - 1, y: centers[0], w: 3, h: H - centers[0] });
  rooms.push({ x: xe - 1, y: 0, w: 3, h: centers[L - 1] + 2 });

  // 小部屋（レーンの上側のあいだに彫る。入り口に近い順に並べる）
  const alcoves: { tileX: number; tileY: number }[] = [];
  for (let i = 0; i < L - 1; i++) {
    const gapTop = centers[i + 1] + 2; // 上のレーンの下の壁の次の行
    const gapY = centers[i] - 4; // このレーンの上側に3行ぶん
    void gapTop;
    // 左と右の2つ
    const slots = [left + 4 + Math.floor(rand() * 6), Math.round(W / 2) + 4 + Math.floor(rand() * 6)];
    const ordered = i % 2 === 0 ? slots : [...slots].reverse(); // レーンを歩く向きに合わせて、先に出会う順
    for (const ax of ordered) {
      rooms.push({ x: ax, y: gapY, w: 7, h: 3 });
      alcoves.push({ tileX: ax + 3, tileY: gapY });
    }
  }

  // 道（通路の中央を、入り口から出口まで）
  pathPoints.push([xs, H - 1], [xs, centers[0]]);
  for (let i = 0; i < L; i++) {
    const goingRight = i % 2 === 0;
    pathPoints.push([goingRight ? right - 3 : left + 2, centers[i]]);
    if (i < L - 1) pathPoints.push([goingRight ? right - 3 : left + 2, centers[i + 1]]);
  }
  pathPoints.push([xe, centers[L - 1]], [xe, 0]);
  let pathLength = 0;
  for (let i = 1; i < pathPoints.length; i++) {
    pathLength += Math.abs(pathPoints[i][0] - pathPoints[i - 1][0]) + Math.abs(pathPoints[i][1] - pathPoints[i - 1][1]);
  }

  const spec: CarveSpec = {
    width: W,
    height: H,
    wall: opts.wall,
    floor: opts.floor,
    rooms,
    paths: opts.path !== undefined ? [{ tile: opts.path, points: pathPoints }] : [],
    gates: [
      { x: xs, y: H - 1, tile: opts.path ?? opts.floor },
      { x: xe, y: 0, tile: opts.path ?? opts.floor },
    ],
  };
  return {
    width: W,
    height: H,
    spec,
    landmarks: {
      alcoves,
      south: { x: xs, y: H - 1 },
      southArrival: { tileX: xs, tileY: H - 2 },
      north: { x: xe, y: 0 },
      northArrival: { tileX: xe, tileY: 1 },
      nearEntry: { tileX: xs + 5, tileY: centers[0] - 1 },
      nearExit: { tileX: xe - 4, tileY: centers[L - 1] - 1 },
      pathLength,
    },
  };
}
