import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { lintAiSong } from "./ai-song-lint";

const base = {
  title: "テスト", description: "テスト", bpm: 120, beats: 4, chords: "Am F C G Am", barsPerChord: 1, repeats: 2,
  autoAccompaniment: false, feel: "rock", tone: "rock",
  parts: [{ instrument: "piano", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "R:4 A4:1 C5:1 E5:2" }],
} as unknown as AiSong;

describe("AIソング形式の点検（lint）", () => {
  it("問題のない曲は警告なし", () => {
    expect(lintAiSong(base)).toEqual([]);
  });
  it("歪みギターの音量が大きいとつぶれ注意", () => {
    const song = { ...base, parts: [...base.parts, { instrument: "distGuitar", role: "刻み", volume: 0.075, pan: -0.9, amp: "distortion", notes: "R:4 E3:1" }] } as AiSong;
    expect(lintAiSong(song).some((w) => w.includes("つぶれ注意"))).toBe(true);
    const quiet = { ...song, parts: [base.parts[0], { ...song.parts[1], volume: 0.04 }] } as AiSong;
    expect(lintAiSong(quiet).some((w) => w.includes("つぶれ注意"))).toBe(false);
  });
  it("音域外・ループのコード違い・leadの音色を知らせる", () => {
    const song = { ...base, chords: "Am F C G", parts: [{ instrument: "bass", role: "ベース", volume: 0.2, pan: 0, amp: "auto", notes: "R:1 C6:1" }, { instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "R:1 C5:1" }] } as AiSong;
    const w = lintAiSong(song);
    expect(w.some((x) => x.includes("音域外"))).toBe(true);
    expect(w.some((x) => x.includes("ループ"))).toBe(true);
    expect(w.some((x) => x.includes("lead は"))).toBe(true);
    expect(w.some((x) => x.includes("bass は"))).toBe(true);
    // style / synth を選べば音色の注意は出ない
    const folk = lintAiSong({ ...song, style: "folk" } as AiSong);
    expect(folk.some((x) => x.includes("音色の注意"))).toBe(false);
  });
  it("style は score.style に入る（rock・不明な値は入らない）。synth は electro になる", () => {
    expect(aiSongToScore({ ...base, style: "folk" } as AiSong).score.style).toBe("folk");
    expect(aiSongToScore({ ...base, style: "rock" } as AiSong).score.style).toBeUndefined();
    expect(aiSongToScore({ ...base, style: "nonsense" } as unknown as AiSong).score.style).toBeUndefined();
    expect(aiSongToScore({ ...base, synth: true, style: "folk" } as AiSong).score.style).toBe("electro");
  });
});
