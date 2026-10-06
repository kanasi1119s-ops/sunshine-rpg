import { describe, expect, it } from "vitest";
import { WORLD_MAPS, WORLD_NPCS } from "../world/world";
import { townOverlaps, townPostOverlaps, townWallOverhangs } from "./town-tidy";
import { doorOffsetX, isHouse } from "./map-props";

const towns = Object.keys(WORLD_MAPS).filter((m) => /-(town|village)$/.test(m) || /^village-/.test(m));

describe("町のととのえ", () => {
  it("町の中で、花壇いがいの飾り・調べられる物の絵が重ならない", () => {
    const all: string[] = [];
    for (const id of towns) for (const o of townOverlaps(WORLD_MAPS[id], WORLD_NPCS[id] ?? [])) all.push(`${id}: ${o}`);
    expect(all).toEqual([]);
  });
  it("町は塀で囲まれ（外まわりは通れない）、出入り口だけあいている", () => {
    for (const id of towns) {
      const d = WORLD_MAPS[id];
      expect(d.townWall, id).toBe(true);
      for (let x = 0; x < d.width; x++) {
        for (const y of [0, d.height - 1]) {
          const exit = d.exits?.some((e) => e.tileX === x && e.tileY === y);
          if (!exit) expect(d.collision![y * d.width + x], `${id} (${x},${y})`).toBe(1);
        }
      }
    }
  });
  it("建物いがいの飾りの絵は、塀にはみ出さない", () => {
    const all: string[] = [];
    for (const id of towns) for (const o of townWallOverhangs(WORLD_MAPS[id])) all.push(`${id}: ${o}`);
    expect(all).toEqual([]);
  });
  it("飾りの絵は、塀の柱（すみ・門の両わき）にかからない", () => {
    const all: string[] = [];
    for (const id of towns) for (const o of townPostOverlaps(WORLD_MAPS[id])) all.push(`${id}: ${o}`);
    expect(all).toEqual([]);
  });
  it("家の玄関は、塀にかからない", () => {
    for (const id of towns) {
      const d = WORLD_MAPS[id];
      for (const p of d.props ?? []) {
        if (!isHouse(p.kind)) continue;
        const dy = p.tileY + 1, dx = p.tileX + doorOffsetX(p.kind);
        expect(dy < d.height - 1 && dx > 0 && dx < d.width - 1, `${id} ${p.kind}(${p.tileX},${p.tileY})`).toBe(true);
      }
    }
  });
  it("街灯は、道にそって6マスごとの決まった所にある", () => {
    for (const id of towns) {
      for (const p of (WORLD_MAPS[id].props ?? []).filter((q) => q.kind === "lamp")) {
        expect(p.tileX % 6 === 3 || p.tileY % 6 === 3, `${id} lamp(${p.tileX},${p.tileY})`).toBe(true);
      }
    }
  });
});

describe("花壇の並び", () => {
  it("花壇は、家の左右（足もとの列の2マス横）にだけある", () => {
    for (const id of towns) {
      const props = WORLD_MAPS[id].props ?? [];
      for (const f of props.filter((q) => q.kind === "flowerbed")) {
        expect(props.some((q) => isHouse(q.kind) && q.tileY === f.tileY && Math.abs(q.tileX - f.tileX) === 2), `${id} flowerbed(${f.tileX},${f.tileY})`).toBe(true);
      }
    }
  });
});
