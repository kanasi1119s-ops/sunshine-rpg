import { describe, expect, it } from "vitest";
import { createMemoryStore, deleteSlot, hasSlot, loadFromSlot, saveToSlot } from "./storage";
import { SAVE_VERSION, type SaveData } from "./types";

function makeSaveData(): SaveData {
  return {
    version: SAVE_VERSION,
    savedAt: "2026-09-28T00:00:00.000Z",
    player: { mapId: "sample-field", tileX: 10, tileY: 6, direction: "down" },
    hero: {
      stats: { level: 1, exp: 0, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 12, defense: 6, speed: 9 },
      equipment: {},
    },
    companions: {},
    inventory: [],
    flags: {},
  };
}

describe("save slots", () => {
  it("空のスロットはnullを返す", () => {
    const store = createMemoryStore();
    expect(loadFromSlot(store, "slot1")).toBeNull();
    expect(hasSlot(store, "slot1")).toBe(false);
  });

  it("保存したデータをそのまま読み込める", () => {
    const store = createMemoryStore();
    const data = makeSaveData();
    saveToSlot(store, "slot1", data);
    expect(hasSlot(store, "slot1")).toBe(true);
    expect(loadFromSlot(store, "slot1")).toEqual(data);
  });

  it("スロットごとに独立している", () => {
    const store = createMemoryStore();
    saveToSlot(store, "slot1", makeSaveData());
    expect(hasSlot(store, "slot2")).toBe(false);
  });

  it("deleteSlotでスロットが空になる", () => {
    const store = createMemoryStore();
    saveToSlot(store, "autosave", makeSaveData());
    deleteSlot(store, "autosave");
    expect(hasSlot(store, "autosave")).toBe(false);
  });

  it("壊れたデータが入っているスロットはnullを返す（例外を投げない）", () => {
    const store = createMemoryStore();
    store.setItem("sunshine-rpg:save:slot1", "not valid json");
    expect(loadFromSlot(store, "slot1")).toBeNull();
  });
});
