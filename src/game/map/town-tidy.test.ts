import { describe, expect, it } from "vitest";
import { WORLD_MAPS, WORLD_NPCS } from "../world/world";
import { townCrowdedHouses, townOverlaps, townPropsOnPath, townObjectsNearGate, townTreesTooClose, townPathOverlaps, townPostOverlaps, townWallOverhangs } from "./town-tidy";
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
  it("街灯は、決まった所にある（道ぞいの4マスごと・家の玄関の前の左右・足りない町の決まった間かく）", () => {
    for (const id of towns) {
      const props = WORLD_MAPS[id].props ?? [];
      for (const p of props.filter((q) => q.kind === "lamp")) {
        const road = p.tileX % 4 === 2 || p.tileY % 4 === 2;
        const door = props.some((q) => isHouse(q.kind) && p.tileY === q.tileY + 1 && [2, 3].includes(Math.abs(p.tileX - q.tileX - (q.kind.startsWith("manor") ? -1 : 0))));
        const grid = (p.tileX + 2 * p.tileY) % 5 === 0;
        expect(road || door || grid, `${id} lamp(${p.tileX},${p.tileY})`).toBe(true);
      }
    }
  });
  it("どの町にも、木が3本以上・街灯が4本以上ある", () => {
    for (const id of towns) {
      const props = WORLD_MAPS[id].props ?? [];
      expect(props.filter((q) => ["tree", "tree-pine", "tree-snow", "tree-dead", "palm"].includes(q.kind)).length, `${id} 木`).toBeGreaterThanOrEqual(id === "garasuko-town" ? 2 : 3);   // 硝子湖は、湖・家・人で場所がなく、木を4マスはなすと2本まで（2026-10-06）
      expect(props.filter((q) => q.kind === "lamp").length, `${id} 街灯`).toBeGreaterThanOrEqual(4);
    }
  });
});

describe("花壇の並び", () => {
  it("花壇は、家の左右（足もとの列の2マス横。歩道をよけたときは3マス横）にだけある", () => {
    for (const id of towns) {
      const props = WORLD_MAPS[id].props ?? [];
      for (const f of props.filter((q) => q.kind === "flowerbed")) {
        expect(props.some((q) => isHouse(q.kind) && q.tileY === f.tileY && [2, 3].includes(Math.abs(q.tileX - f.tileX))), `${id} flowerbed(${f.tileX},${f.tileY})`).toBe(true);
      }
    }
  });
});

describe("歩道との重なり", () => {
  it("家・花壇の絵は、歩道（道）にかからない（2026-10-06「一部花壇、家が歩道に重なってるから少し離して」）", () => {
    for (const id of towns) expect(townPathOverlaps(WORLD_MAPS[id]), id).toEqual([]);
  });
});

describe("建物の間・井戸・噴水", () => {
  it("家の軒は、ほかの建物とくっつかない（2026-10-06「そこも直して」）", () => {
    for (const id of towns) expect(townCrowdedHouses(WORLD_MAPS[id]), id).toEqual([]);
  });
  it("どの町にも井戸がある（2026-10-06「井戸も置こう」）", () => {
    for (const id of towns) expect((WORLD_MAPS[id].props ?? []).some((p) => p.kind === "well"), id).toBe(true);
  });
  it("どの町にも噴水がある（2026-10-06「各町噴水も置こうか」）", () => {
    for (const id of towns) expect((WORLD_MAPS[id].props ?? []).some((p) => p.kind === "fountain"), id).toBe(true);
  });
});

describe("歩道", () => {
  it("歩道（道）の上には、飾りがのらない（歩ける。2026-10-06「歩道には歩けるようにオブジェクトがのらないように」）", () => {
    for (const id of towns) expect(townPropsOnPath(WORLD_MAPS[id]), id).toEqual([]);
  });
});

describe("門のまわり", () => {
  it("町の出入り口（門）の近く（4マス以内）に、建物・花壇のほかの飾りを置かない（2026-10-06「入り口近くにオブジェクトを置くのをやめよう」）", () => {
    for (const id of towns) expect(townObjectsNearGate(WORLD_MAPS[id]), id).toEqual([]);
  });
});

describe("木の間かく", () => {
  it("町の木と木は、4マス以上はなれている（2026-10-06「町で木と木は近すぎないようにしてほしい」）", () => {
    for (const id of towns) expect(townTreesTooClose(WORLD_MAPS[id]), id).toEqual([]);
  });
});
