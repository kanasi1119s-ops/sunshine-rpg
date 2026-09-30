import { describe, expect, it } from "vitest";
import { CHAPTER11_MAPS, CHAPTER11_NPCS } from "./chapter11-world";
import { WORLD_MAPS, WORLD_NPCS } from "./world";
import { GODS } from "../battle/chapter11-enemies";
import { collectBattleIds, collectReferencedFlags, collectSetFlags, collectWarpTargets } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
import { createEventRunner } from "../event/event-runner";
import type { EventCommand, Flags } from "../event/types";

function run(commands: EventCommand[], flags: Flags, choose = 0): string[] {
  const runner = createEventRunner(commands, flags);
  const texts: string[] = [];
  let result = runner.next();
  let guard = 0;
  while (!result.done && guard++ < 500) {
    if (result.step?.kind === "message") {
      texts.push(result.step.text);
      result = runner.next({ kind: "advance" });
    } else {
      result = runner.next({ kind: "choose", index: choose });
    }
  }
  return texts;
}

const all = () => Object.values(CHAPTER11_NPCS).flat();
const npc = (id: string) => {
  const found = all().find((n) => n.id === id);
  if (!found) {
    throw new Error(`${id} が見つからない`);
  }
  return found;
};

describe("8神の禁域のデータの整合性", () => {
  it("8つの禁域と、神・祭壇・入口が揃っている", () => {
    expect(Object.keys(CHAPTER11_MAPS)).toHaveLength(8);
    for (const god of GODS) {
      for (const suffix of ["entrance", "boss", "altar", "lore"]) {
        expect(() => npc(`${god.id}-${suffix}`)).not.toThrow();
      }
    }
  });

  it("NPCは実在する地図の通行可能なタイルにあり、同じ地図のほかのNPC・出入り口・到着地点と重ならない", () => {
    const bad: string[] = [];
    for (const [mapId, npcs] of Object.entries(WORLD_NPCS)) {
      const seen = new Set<string>();
      for (const n of npcs) {
        const key = `${n.tileX},${n.tileY}`;
        if (seen.has(key)) {
          bad.push(`${mapId} の ${key} にNPCが重なる（${n.id}）`);
        }
        seen.add(key);
      }
    }
    for (const [mapId, npcs] of Object.entries(CHAPTER11_NPCS)) {
      const data = WORLD_MAPS[mapId];
      const map = createTileMap(data);
      const arrivals = Object.values(WORLD_MAPS).flatMap((m) => m.exits ?? []).filter((e) => e.targetMapId === mapId);
      for (const n of npcs) {
        if (!isWalkable(map, n.tileX, n.tileY)) {
          bad.push(`${mapId} の ${n.id} が通行不可`);
        }
        if ((data.exits ?? []).some((e) => e.tileX === n.tileX && e.tileY === n.tileY)) {
          bad.push(`${mapId} の ${n.id} が出入り口の上`);
        }
        if (arrivals.some((e) => e.targetTileX === n.tileX && e.targetTileY === n.tileY)) {
          bad.push(`${mapId} の ${n.id} が到着地点の上`);
        }
      }
    }
    expect(bad).toEqual([]);
  });

  it("禁域の出入り口は、その神の地方の地図の、歩ける場所へ戻る", () => {
    for (const [mapId, data] of Object.entries(CHAPTER11_MAPS)) {
      for (const exit of data.exits ?? []) {
        const target = WORLD_MAPS[exit.targetMapId];
        expect(target, `${mapId} の戻り先が無い`).toBeDefined();
        expect(isWalkable(createTileMap(target), exit.targetTileX, exit.targetTileY), `${mapId} の戻り先が歩けない`).toBe(true);
      }
    }
  });

  it("参照するフラグは、どこかでsetFlagされているか、戦闘の勝利で立つ。warpは実在、戦闘IDは8神のもの", () => {
    const commands = all().flatMap((n) => n.commands);
    const set = collectSetFlags(commands);
    const victory = new Set(GODS.map((g) => `god${g.no}_defeated`));
    for (const flag of collectReferencedFlags(commands)) {
      if (flag === "deep_yugami_defeated" || victory.has(flag)) {
        continue;
      }
      expect(set.has(flag), `フラグ ${flag} がどこにも立たない`).toBe(true);
    }
    for (const mapId of collectWarpTargets(commands)) {
      expect(WORLD_MAPS[mapId]).toBeDefined();
    }
    expect(collectBattleIds(commands)).toEqual(new Set(GODS.map((g) => g.id)));
  });
});

describe("8神の禁域の進行", () => {
  it("裏ボスを倒す前は、入口に入れない", () => {
    const flags: Flags = {};
    const texts = run(npc("god-1-entrance").commands, flags).join("");
    expect(texts).toContain("特別なものは見当たらない");
    const cleared: Flags = { deep_yugami_defeated: true };
    const targets = collectWarpTargets(npc("god-1-entrance").commands);
    expect(targets).toEqual(new Set(["god-shrine-1"]));
    expect(run(npc("god-1-entrance").commands, cleared).join("")).toContain("石扉");
  });

  it("裏ボスを倒したあとは入口から禁域へ入れ、神を倒し、祭壇で環の欠片を得る（神を倒す前は得られない）", () => {
    for (const god of GODS) {
      const flags: Flags = { deep_yugami_defeated: true };
      run(npc(`${god.id}-altar`).commands, flags);
      expect(flags[`god${god.no}_fragment`], `${god.id} 倒す前に欠片が手に入った`).toBeUndefined();
      run(npc(`${god.id}-boss`).commands, flags);
      expect(flags[`god${god.no}_told`]).toBe(true);
      flags[`god${god.no}_defeated`] = true;
      const texts = run(npc(`${god.id}-altar`).commands, flags).join("");
      expect(flags[`god${god.no}_fragment`]).toBe(true);
      expect(texts).toContain("環の欠片");
      expect(texts).toContain("ごほうび");
    }
  });
});
