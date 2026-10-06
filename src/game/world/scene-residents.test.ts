import { describe, expect, it } from "vitest";
import { firstSpeaker } from "../sprite/character-specs";
import { createTileMap, isWalkable } from "../map/tile-map";
import { WORLD_MAPS, WORLD_NPCS } from "./world";
import { isVoiceOnly, sceneSpeakers, STORY_SCENES } from "./story-scenes";
import { PARTY_NAMES, residentVisible } from "./scene-residents";

describe("物語の場面で話す人は、その町にいる", () => {
  it("場面の話し手（仲間・声だけの人をのぞく）は、みな、その場面の地図にいる", () => {
    const missing: string[] = [];
    for (const s of STORY_SCENES) {
      if (s.mapId === "world-map") continue;   // 世界地図の場面は、少しはなれた所から歩いてくる
      const people = new Set((WORLD_NPCS[s.mapId] ?? []).map((n) => firstSpeaker(n.commands).speaker));
      for (const name of sceneSpeakers(s.commands)) {
        if (PARTY_NAMES.has(name) || isVoiceOnly(name)) continue;
        if (!people.has(name)) missing.push(`${s.id}: ${name}`);
      }
    }
    expect(missing).toEqual([]);
  });

  it("町に置いた人は、通れるマスにいて、場面の時期だけいる", () => {
    for (const [mapId, npcs] of Object.entries(WORLD_NPCS)) {
      const map = createTileMap(WORLD_MAPS[mapId]);
      for (const n of npcs.filter((m) => m.sceneWindows)) {
        expect(isWalkable(map, n.tileX, n.tileY), `${mapId} ${n.id}`).toBe(true);
      }
    }
    const win = [{ requires: ["a"], blockedBy: ["b"] }];
    expect(residentVisible(win, {})).toBe(false);
    expect(residentVisible(win, { a: true })).toBe(true);
    expect(residentVisible(win, { a: true, b: true })).toBe(false);
  });
});
