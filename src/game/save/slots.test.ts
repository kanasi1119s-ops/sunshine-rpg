import { describe, expect, it } from "vitest";
import { describeSave, latestSaveSlot, placeName, summarizeSlots } from "./slots";
import { createMemoryStore, MANUAL_SLOTS, saveToSlot } from "./storage";
import { SAVE_VERSION, type SaveData } from "./types";
import { confirmSlot, moveSlotCursor, openSlotMenu } from "../menu/slot-menu";

function data(mapId: string, savedAt: string, gold = 5): SaveData {
  return {
    version: SAVE_VERSION, savedAt, player: { mapId, tileX: 1, tileY: 1, direction: "down" },
    hero: { stats: { level: 3, exp: 0, maxHp: 30, hp: 30, maxMp: 10, mp: 10, attack: 5, defense: 5, speed: 5 }, equipment: {} },
    companions: {}, jobs: {}, inventory: [], gold, flags: {},
  };
}

describe("セーブの5か所", () => {
  it("手動のセーブ場所は5つ。ロードの一覧には自動セーブも入る", () => {
    expect(MANUAL_SLOTS).toHaveLength(5);
    const store = createMemoryStore();
    expect(summarizeSlots(store, false)).toHaveLength(5);
    expect(summarizeSlots(store, true)).toHaveLength(6);
  });
  it("場所・レベル・灯貨を説明し、いちばん新しいセーブを選ぶ", () => {
    const store = createMemoryStore();
    saveToSlot(store, "slot1", data("touri-town", "2026-10-05T10:00:00"));
    saveToSlot(store, "slot5", data("kiri-town", "2026-10-05T12:00:00"));
    saveToSlot(store, "autosave", data("sanone-town", "2026-10-05T11:00:00"));
    expect(latestSaveSlot(store)).toBe("slot5");
    expect(describeSave(data("kiri-town", "2026-10-05T12:00:00", 42))).toContain("霧断崖");
    expect(describeSave(data("kiri-town", "2026-10-05T12:00:00", 42))).toContain("Lv3");
    expect(latestSaveSlot(createMemoryStore())).toBeNull();
    expect(placeName("unknown-map")).toBe("旅の途中");
  });
  it("ロードでは、からっぽの場所は選べない。セーブではどこでも選べる", () => {
    const store = createMemoryStore();
    saveToSlot(store, "slot3", data("touri-town", "2026-10-05T10:00:00"));
    const load = openSlotMenu("load", summarizeSlots(store, true));
    expect(load.rows[load.cursor].id).toBe("slot3");
    expect(confirmSlot(moveSlotCursor(load, 1))).toBe("slot3" === load.rows[(load.cursor + 1) % 6].id ? "slot3" : null);
    const save = openSlotMenu("save", summarizeSlots(store, false));
    expect(confirmSlot(save)).toBe("slot1");
  });
});
