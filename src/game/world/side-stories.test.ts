import { describe, expect, it } from "vitest";
import { SIDE_STORIES } from "./side-stories";
import { WORLD_MAPS, WORLD_NPCS } from "./world";
import { createEventRunner } from "../event/event-runner";
import { collectReferencedFlags, collectSetFlags } from "../event/inspect";
import { createTileMap, isWalkable } from "../map/tile-map";
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

function npc(id: string) {
  for (const npcs of Object.values(WORLD_NPCS)) {
    const found = npcs.find((n) => n.id === id);
    if (found) {
      return found;
    }
  }
  throw new Error(`${id} が見つからない`);
}

describe("サブストーリーのデータの整合性", () => {
  it("IDと識別子が重複しない", () => {
    expect(new Set(SIDE_STORIES.map((s) => s.id)).size).toBe(SIDE_STORIES.length);
    expect(new Set(SIDE_STORIES.map((s) => s.key)).size).toBe(SIDE_STORIES.length);
  });

  it("依頼人・調べる場所は、実在する地図の通行可能なタイルにあり、ほかのNPCと重ならない", () => {
    for (const [mapId, npcs] of Object.entries(WORLD_NPCS)) {
      const seen = new Set<string>();
      for (const n of npcs) {
        const key = `${n.tileX},${n.tileY}`;
        expect(seen.has(key), `${mapId} の (${key}) に複数のNPC（${n.id}）`).toBe(false);
        seen.add(key);
      }
    }
    const bad: string[] = [];
    for (const story of SIDE_STORIES) {
      const spots = [
        { mapId: story.giver.mapId, x: story.giver.tileX, y: story.giver.tileY, label: `${story.id} 依頼人` },
        ...story.steps.map((s, i) => ({ mapId: s.mapId, x: s.tileX, y: s.tileY, label: `${story.id} 場所${i + 1}` })),
      ];
      for (const spot of spots) {
        if (!WORLD_MAPS[spot.mapId]) {
          bad.push(`${spot.label} の地図が無い`);
          continue;
        }
        const map = createTileMap(WORLD_MAPS[spot.mapId]);
        if (!isWalkable(map, spot.x, spot.y)) {
          bad.push(`${spot.label} が通行不可タイル (${spot.mapId} ${spot.x},${spot.y})`);
        }
        const arrivals = Object.values(WORLD_MAPS).flatMap((m) => m.exits ?? []).filter((e) => e.targetMapId === spot.mapId);
        if (arrivals.some((e) => e.targetTileX === spot.x && e.targetTileY === spot.y)) {
          bad.push(`${spot.label} が到着地点の上 (${spot.mapId} ${spot.x},${spot.y})`);
        }
        const exits = WORLD_MAPS[spot.mapId].exits ?? [];
        if (exits.some((e) => e.tileX === spot.x && e.tileY === spot.y)) {
          bad.push(`${spot.label} が出入り口の上`);
        }
      }
    }
    expect(bad).toEqual([]);
  });

  it("参照するフラグは、どこかで立てられている（本編のフラグは除く）", () => {
    const all = Object.values(WORLD_NPCS).flat().filter((n) => n.id.startsWith("side-")).flatMap((n) => n.commands);
    const set = collectSetFlags(all);
    for (const f of collectReferencedFlags(all)) {
      if (f.startsWith("side_")) {
        expect(set.has(f), `フラグ ${f} がどこにも立たない`).toBe(true);
      }
    }
    for (const story of SIDE_STORIES) {
      for (const f of story.unlockFlags) {
        if (f.startsWith("side_")) {
          expect(set.has(f), `${story.id} の解放フラグ ${f}`).toBe(true);
        }
      }
    }
  });
});

describe("サブストーリーの進行", () => {
  it("すべてのサブストーリーが、解放→受注→調査→報告で完了できる。解放前は受けられない", () => {
    for (const story of SIDE_STORIES) {
      const giver = npc(`side-${story.key}-giver`);
      const flags: Flags = {};
      run(giver.commands, flags);
      expect(flags[`side_${story.key}_accepted`], `${story.id} が解放前に受注できた`).toBeUndefined();
    }
    // 解放条件（本編・ほかのサブストーリー）を満たしながら順に進める。
    const flags: Flags = {};
    for (const story of SIDE_STORIES) {
      for (const f of story.unlockFlags) {
        if (!f.startsWith("side_")) {
          flags[f] = true;
        }
      }
    }
    for (const story of SIDE_STORIES) {
      const giver = npc(`side-${story.key}-giver`);
      const first = run(giver.commands, flags, 0).join("");
      expect(flags[`side_${story.key}_accepted`], `${story.id} を受注できない`).toBe(true);
      story.steps.forEach((_, i) => {
        run(npc(`side-${story.key}-step${i + 1}`).commands, flags, 0);
        expect(flags[`side_${story.key}_step${i + 1}`], `${story.id} の場所${i + 1}`).toBe(true);
      });
      const texts = story.steps.length === 0 ? first : run(giver.commands, flags, 0).join("");
      expect(flags[`side_${story.key}_done`], `${story.id} を完了できない`).toBe(true);
      expect(texts).toContain("ごほうび（仮）");
    }
  });

  it("調べる場所を回らないうちに報告しても、完了しない", () => {
    const story = SIDE_STORIES.find((s) => s.steps.length >= 2)!;
    const flags: Flags = {};
    for (const f of story.unlockFlags) {
      flags[f] = true;
    }
    const giver = npc(`side-${story.key}-giver`);
    run(giver.commands, flags, 0);
    run(giver.commands, flags, 0);
    expect(flags[`side_${story.key}_done`]).toBeUndefined();
  });

  it("受注前は、調べる場所で何も起きない", () => {
    const story = SIDE_STORIES.find((s) => s.steps.length >= 1)!;
    const flags: Flags = {};
    run(npc(`side-${story.key}-step1`).commands, flags);
    expect(flags[`side_${story.key}_step1`]).toBeUndefined();
  });

  it("S-013は、選んだ道によってフラグが分かれる", () => {
    const flags: Flags = { chapter4_intro_seen: true };
    run(npc("side-s013-giver").commands, flags, 0);
    run(npc("side-s013-step1").commands, flags, 1);
    expect(flags.side_s013_let_go).toBe(true);
    expect(flags.side_s013_kept_rule).toBeUndefined();
  });
});
