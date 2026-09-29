import { describe, expect, it } from "vitest";
import { AI_SONG_GUIDE, AI_SONG_SCHEMA, aiSongToScore, fitToLength } from "./ai-song";
import { trackTotalBeats } from "./edit";
import { REST } from "./score";

const song = {
  title: "テストの曲", description: "テスト", bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2,
  autoAccompaniment: true, feel: "rock", tone: "rock",
  parts: [
    { instrument: "leadGuitar", role: "メロディ", volume: 0.25, pan: 0, amp: "prs", notes: "A4:1 C5:1 E5:2 R:4 D5:0.5 C5:0.5 B4:1 A4:2" },
    { instrument: "kick", role: "キック", volume: 0.3, pan: 0, amp: "auto", notes: "x:1 R:1 x:1 R:1" },
  ],
};

describe("AIソング形式", () => {
  it("曲に組み立てられる。伴奏つき・長さがそろう・短いパートはくり返す", () => {
    const { score, warnings } = aiSongToScore(song);
    expect(warnings).toEqual([]);
    expect(score.tempoBpm).toBe(120);
    const total = 8 * 4;
    for (const t of score.tracks) expect(trackTotalBeats(t)).toBeCloseTo(total, 6);
    const lead = score.tracks[score.tracks.length - 2];
    expect(lead.amp).toEqual({ type: "prs" });
    const kick = score.tracks[score.tracks.length - 1];
    expect(kick.notes.filter((n) => n.note !== REST).length).toBe(16);
  });
  it("伴奏なしにもできる", () => {
    expect(aiSongToScore({ ...song, autoAccompaniment: false }).score.tracks.length).toBe(2);
  });
  it("まちがいは、場所つきでまとめて知らせる", () => {
    const bad = { ...song, parts: [{ ...song.parts[0], notes: "H4:1 C5:abc" }, { ...song.parts[1], notes: "C4:1" }, { ...song.parts[0], instrument: "banjo" }] };
    const msg = (() => {
      try {
        aiSongToScore(bad);
        return "";
      } catch (e) {
        return (e as Error).message;
      }
    })();
    expect(msg).toMatch(/音名が読めません「H4:1」/);
    expect(msg).toMatch(/拍が読めません「C5:abc」/);
    expect(msg).toMatch(/ドラムは x か R/);
    expect(msg).toMatch(/楽器が一覧にありません/);
    expect(() => aiSongToScore({ ...song, chords: "Am Q" })).toThrow(/chords/);
  });
  it("長すぎるパートは切って知らせる", () => {
    const { warnings } = aiSongToScore({ ...song, parts: [{ ...song.parts[0], notes: "A4:40" }] });
    expect(warnings[0]).toMatch(/切りました/);
  });
  it("長さをそろえる道具", () => {
    expect(fitToLength([{ note: "C4", durationBeats: 3 }], 4).map((e) => e.durationBeats)).toEqual([3, 1]);
    expect(fitToLength([], 4)).toEqual([{ note: REST, durationBeats: 4 }]);
  });
  it("説明とスキーマに楽器の一覧が入っている", () => {
    expect(AI_SONG_GUIDE).toMatch(/leadGuitar/);
    expect(AI_SONG_SCHEMA.properties.parts.items.properties.instrument.enum).toContain("kick");
  });
  it("ジャンル別のアンプ（jazz など）を使える。知らない名前は注意を出して、おまかせにする", () => {
    const withAmps = { ...song, autoAccompaniment: false, parts: [{ ...song.parts[0], amp: "jazz" }, { ...song.parts[0], amp: "tubescreamer" }] };
    const { score, warnings } = aiSongToScore(withAmps);
    expect(score.tracks[0].amp).toEqual({ type: "jazz" });
    expect(score.tracks[1].amp).toBeUndefined();
    expect(warnings.some((w) => w.includes("tubescreamer"))).toBe(true);
    expect(AI_SONG_SCHEMA.properties.parts.items.properties.amp.enum).toContain("shoegaze");
  });
});
