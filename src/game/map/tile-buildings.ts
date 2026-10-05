import type { Npc } from "../npc";
import type { TileMapData } from "./types";

/**
 * タイル（壁のかたまり）で描いていた町の建物を、平屋の家の絵（`house`）に置きかえる
 * （人間の指示「タイルで描いた家も平屋の家にして。色は変えていいから」、2026-10-05）。
 * 壁のかたまり（地図のふちに接していないもの）ごとに: 壁を地面にもどし、下の段のまんなかを足もとにして家の絵を置く（横3マス×縦2マスが通れない）。
 * かたまりの中にあった出入り口（相談所など）は、家の玄関（足もとのすぐ下）に移し、ほかの地図からそこへ来る出入り口も、玄関の前に着くようにする。
 * 出入り口の無い建物は、ほかの家と同じく、あとで家の中（house-interiors.ts）がつく。
 */
export function convertTileBuildings(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, m] of Object.entries(maps)) {
    if (!m.building || m.building.tent || !m.collision) continue;
    const W = m.width, H = m.height, g = m.layers[0].data, col = m.collision;
    const walls = m.building.walls;
    const isWall = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < W && y < H && walls.includes(g[y * W + x]);
    // いちばん多い、歩ける地面
    const counts = new Map<number, number>();
    for (let i = 0; i < g.length; i++) if (!col[i] && !walls.includes(g[i])) counts.set(g[i], (counts.get(g[i]) ?? 0) + 1);
    const groundId = [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
    if (groundId === undefined) continue;
    const seen = new Set<number>();
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        if (!isWall(x, y) || seen.has(y * W + x)) continue;
        const cells: [number, number][] = [];
        const stack: [number, number][] = [[x, y]];
        seen.add(y * W + x);
        while (stack.length) {
          const [cx, cy] = stack.pop()!;
          cells.push([cx, cy]);
          for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
            const nx = cx + dx, ny = cy + dy;
            if (isWall(nx, ny) && !seen.has(ny * W + nx)) {
              seen.add(ny * W + nx);
              stack.push([nx, ny]);
            }
          }
        }
        const x0 = Math.min(...cells.map((c) => c[0])), x1 = Math.max(...cells.map((c) => c[0]));
        const y0 = Math.min(...cells.map((c) => c[1])), y1 = Math.max(...cells.map((c) => c[1]));
        if (x0 === 0 || y0 === 0 || x1 === W - 1 || y1 === H - 1) continue;   // 町の外周の壁
        if (x1 - x0 > 5 || y1 - y0 > 3) continue;                             // 大きすぎるもの（家ではない）
        const foot = { x: x0 + 1, y: y1 };
        const door = { x: foot.x, y: foot.y + 1 };
        // 壁を地面にもどし、家の足もと（横3マス×縦2マス）だけ通れなくする
        for (const [cx, cy] of cells) {
          g[cy * W + cx] = groundId;
          col[cy * W + cx] = 0;
        }
        for (let yy = foot.y - 1; yy <= foot.y; yy++) for (let xx = foot.x - 1; xx <= foot.x + 1; xx++) col[yy * W + xx] = 1;
        m.props = [...(m.props ?? []), { kind: "house", tileX: foot.x, tileY: foot.y }];
        // かたまりの中の出入り口は、玄関へ（上へ押して入る）
        const inside = (ex: number, ey: number): boolean => ex >= x0 && ex <= x1 && ey >= y0 && ey <= y1;
        const moved = (m.exits ?? []).filter((e) => inside(e.tileX, e.tileY));
        m.exits = (m.exits ?? []).map((e) => (inside(e.tileX, e.tileY) ? { ...e, tileX: door.x, tileY: door.y, enter: "up" as const } : e));
        // ほかの地図から、この建物（の出入り口）へもどってくる出入り口は、玄関の前に着く
        if (moved.length) {
          for (const other of Object.values(maps)) {
            other.exits = other.exits?.map((e) =>
              e.targetMapId === mapId && (inside(e.targetTileX, e.targetTileY) || (e.targetTileX === door.x && e.targetTileY === door.y))
                ? { ...e, targetTileX: door.x, targetTileY: door.y + 1 }
                : e,
            );
          }
        }
        // 玄関・足もとに立っていた人は、玄関の前のあいている所へずらす
        for (const npc of npcsByMap[mapId] ?? []) {
          const onFoot = npc.tileX >= foot.x - 1 && npc.tileX <= foot.x + 1 && npc.tileY >= foot.y - 1 && npc.tileY <= foot.y;
          if (onFoot || (npc.tileX === door.x && npc.tileY === door.y)) {
            npc.tileX = door.x + 2;
            npc.tileY = door.y;
          }
        }
      }
    }
  }
}
