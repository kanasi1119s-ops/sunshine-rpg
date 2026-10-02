import { describe, expect, it } from "vitest";
import { allEntries, getTrack } from "./catalog";
import "./user-songs";
import { BGM_TRIM_DB } from "./bgm-trim";

describe("曲ごとの音量補正", () => {
  it("補正は±12dB以内で、表にある曲はすべて曲一覧にある", () => {
    const ids = new Set(allEntries().map((e) => e.id));
    for (const [id, db] of Object.entries(BGM_TRIM_DB)) {
      expect(ids.has(id), id).toBe(true);
      expect(Math.abs(db), id).toBeLessThanOrEqual(12);
    }
  });
  it("曲を取り出すと trimDb が付く（補正が0の曲は付かない）。元の曲データは変えない", () => {
    const [id, db] = Object.entries(BGM_TRIM_DB).find(([, v]) => v !== 0)!;
    expect(getTrack(id).trimDb).toBe(db);
  });
});
