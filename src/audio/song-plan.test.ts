import { describe, expect, it } from "vitest";
import { expandBars, prepareSong, transposeChord } from "./song-plan";
import { aiSongToScore, type AiSong } from "./ai-song";

const base = (over: Partial<AiSong> = {}): AiSong => ({
  title: "t", description: "d", bpm: 100, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 1,
  autoAccompaniment: true, feel: "pop", tone: "rock",
  parts: [{ instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "C5:1 D5:1 E5:2" }],
  ...over,
} as AiSong);

describe("曲の前処理（Am*2・sectionChords・modulate・loopTail）", () => {
  it("使っていなければ同じものをそのまま返す", () => {
    const s = base();
    expect(prepareSong(s)).toBe(s);
  });
  it("Am*2 は2小節ぶん", () => {
    expect(expandBars("C Am*2 F", 1)).toEqual(["C", "Am", "Am", "F"]);
    expect(expandBars("C Am", 2)).toEqual(["C", "C", "Am", "Am"]);
    expect(() => expandBars("C*0", 1)).toThrow();
    const { score, song } = aiSongToScore(base({ chords: "C Am*2 F*3 G", repeats: 2 }));
    expect(song.chords.split(" ").length).toBe(14);
    const beats = score.tracks[0].notes.reduce((s, n) => s + n.durationBeats, 0);
    expect(beats).toBe(14 * 4);
  });
  it("sectionChords: セクションごとに進行が変わる（2回目は verse2 で別指定もできる）", () => {
    const s = prepareSong(base({
      sections: [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "verse", bars: 2 }],
      sectionChords: { verse: "Am F", chorus: "F G Em Am", verse2: "Dm" },
    }));
    expect(s.chords).toBe("Am F Am F F G Em Am Dm Dm");
    expect(s.barsPerChord).toBe(1);
  });
  it("sectionChords は sections が配列でないときは注意を出して無視する", () => {
    const w: string[] = [];
    expect(prepareSong(base({ sectionChords: { verse: "Am" } }), w).chords).toBe("C Am F G");
    expect(w.join("")).toContain("sections");
  });
  it("modulate: atBar 以降のコードと旋律が半音上がる。ドラムは動かない", () => {
    const w: string[] = [];
    const s = prepareSong(base({
      chords: "C Am F G", repeats: 2, modulate: { atBar: 5, semitones: 1 },
      parts: [
        { instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "C5:4 D5:4 E5:4 F5:4" },
        { instrument: "kick", role: "キック", volume: 0.2, pan: 0, amp: "auto", notes: "x:1 R:3" },
      ],
    }), w);
    expect(s.chords).toBe("C Am F G C# A#m F# G#");
    expect(s.parts[0].notes.split(" ")).toEqual(["C5:4", "D5:4", "E5:4", "F5:4", "C#5:4", "D#5:4", "F5:4", "F#5:4"]);
    expect(s.parts[1].notes).toBe("x:1 R:3");
    expect(w).toEqual([]);
    expect(() => aiSongToScore({ ...s })).not.toThrow();
  });
  it("modulate の範囲まちがいは注意を出して転調しない", () => {
    const w: string[] = [];
    const s = prepareSong(base({ modulate: { atBar: 99, semitones: 1 } }), w);
    expect(s.chords).toBe("C Am F G");
    expect(w.length).toBe(1);
  });
  it("loopTail: 最後の小節を V7 か vi にする", () => {
    expect(prepareSong(base({ loopTail: "dominant" })).chords).toBe("C Am F G7");
    expect(prepareSong(base({ chords: "C F Am F", loopTail: "deceptive" })).chords).toBe("C F Am Am");
    expect(prepareSong(base({ chords: "Am F C E", loopTail: "deceptive" })).chords).toBe("Am F C F");
  });
  it("コードを半音ずらす（分数コードの低音・フラット表記も）", () => {
    expect(transposeChord("G/B", 2)).toBe("A/C#");
    expect(transposeChord("Bbmaj7", -2)).toBe("Abmaj7");
    expect(transposeChord("C", -12)).toBe("C");
    expect(transposeChord("Am", -1)).toBe("G#m");
  });
});
