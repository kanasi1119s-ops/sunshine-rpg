import { describe, expect, it } from "vitest";
import { deserializeSaveData, serializeSaveData } from "./serializer";
import { SAVE_VERSION, type SaveData } from "./types";

function makeSaveData(): SaveData {
  return {
    version: SAVE_VERSION,
    savedAt: "2026-09-28T00:00:00.000Z",
    player: { mapId: "sample-field", tileX: 10, tileY: 6, direction: "down" },
    hero: {
      stats: { level: 1, exp: 0, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 12, defense: 6, speed: 9 },
      equipment: { weapon: "sword" },
    },
    companions: {
      reto: { stats: { level: 1, exp: 0, maxHp: 26, hp: 26, maxMp: 6, mp: 6, attack: 13, defense: 7, speed: 11 } },
    },
    inventory: [{ itemId: "herb", quantity: 3 }],
    flags: { met_villager: true },
  };
}

describe("serializeSaveData / deserializeSaveData", () => {
  it("シリアライズしたものを読み戻すと同じ内容になる", () => {
    const data = makeSaveData();
    const json = serializeSaveData(data);
    const restored = deserializeSaveData(json);
    expect(restored).toEqual(data);
  });

  it("壊れたJSONはエラーになる", () => {
    expect(() => deserializeSaveData("{not valid json")).toThrow();
  });

  it("対応していないバージョンはエラーになる", () => {
    const json = JSON.stringify({ ...makeSaveData(), version: 999 });
    expect(() => deserializeSaveData(json)).toThrow();
  });
});
