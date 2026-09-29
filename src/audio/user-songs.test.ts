import { describe, expect, it } from "vitest";
import { allEntries, getTrack } from "./catalog";
import type { Score } from "./score";
import { songFileToEntry } from "./user-songs";

const score: Score = { tempoBpm: 120, loop: true, tracks: [{ waveform: "sine", volume: 0.2, amp: { type: "nam", model: "x" }, notes: [{ note: "C4", durationBeats: 4 }] }], namModels: { x: "{}" } };
const file = { format: "sunshine-game-song", version: 1, id: "my-song", title: "ぼくの曲", scene: "テスト", score };

describe("作曲ソフトで作ったゲーム用の曲", () => {
  it("ファイルを一覧の1件にできる。NAMの指定はゲーム用に外す", () => {
    const e = songFileToEntry(file, new Set());
    expect(e.id).toBe("my-song");
    expect(e.handmade?.namModels).toBeUndefined();
    expect(e.handmade?.tracks[0].amp?.type).toBe("auto");
    expect(score.namModels).toBeDefined();
  });
  it("形式・IDがおかしいものは断る", () => {
    expect(() => songFileToEntry({ ...file, format: "x" }, new Set())).toThrow();
    expect(() => songFileToEntry({ ...file, id: "Bad ID" }, new Set())).toThrow();
    expect(() => songFileToEntry(file, new Set(["my-song"]))).toThrow();
  });
  it("登録した曲は getTrack で取り出せる", async () => {
    const { EXTRA_ENTRIES } = await import("./catalog");
    EXTRA_ENTRIES.push(songFileToEntry(file, new Set()));
    expect(getTrack("my-song").tempoBpm).toBe(120);
    expect(allEntries().some((e) => e.id === "my-song")).toBe(true);
    EXTRA_ENTRIES.length = 0;
  });
});
