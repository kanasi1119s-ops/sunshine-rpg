import { describe, expect, it } from "vitest";
import { migrateSaveData } from "./migrate";
import { SAVE_VERSION } from "./types";

function makeV1Data() {
  return {
    version: 1,
    savedAt: "2026-09-28T00:00:00.000Z",
    player: { mapId: "touri-town", tileX: 11, tileY: 9, direction: "down" },
    hero: {
      stats: { level: 2, exp: 150, maxHp: 35, hp: 35, maxMp: 12, mp: 12, attack: 16, defense: 7, speed: 10 },
      equipment: { weapon: "sword" },
    },
    inventory: [{ itemId: "herb", quantity: 1 }],
    flags: { chapter0_reto_joined: true },
  };
}

describe("migrateSaveData", () => {
  it("version 1（仲間データが無い）のセーブを、companionsが空のversion 2に変換する", () => {
    const migrated = migrateSaveData(makeV1Data());
    expect(migrated.version).toBe(SAVE_VERSION);
    expect(migrated.companions).toEqual({});
    // 他のフィールドはそのまま引き継がれる。
    expect(migrated.hero.stats.level).toBe(2);
    expect(migrated.flags.chapter0_reto_joined).toBe(true);
  });

  it("すでに今のバージョンのデータはそのまま返す", () => {
    const data = { ...migrateSaveData(makeV1Data()) };
    expect(migrateSaveData(data)).toEqual(data);
  });

  it("不正な形式のデータはエラーになる", () => {
    expect(() => migrateSaveData(null)).toThrow();
    expect(() => migrateSaveData({})).toThrow();
  });

  it("未対応のバージョンはエラーになる", () => {
    expect(() => migrateSaveData({ ...makeV1Data(), version: 999 })).toThrow();
  });
});
