import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { applyGuitarTone, GUITAR_TONES } from "./guitar-tones";

describe("ギターの音色プリセット（guitarTone）", () => {
  it("書かれていない項目だけ入れ、パートの値を優先する", () => {
    const w: string[] = [];
    const p: Record<string, unknown> = applyGuitarTone<Record<string, unknown>>({ instrument: "leadGuitar", guitarTone: "warm-lead-b", reverb: 0.1 }, "p", w);
    expect(p.amp).toBe("overdrive");
    expect(p.ampCabIr).toBe("dfc-ampmix");
    expect(p.reverb).toBe(0.1);
    expect(Array.isArray(p.fx)).toBe(true);
    expect(w).toEqual([]);
  });
  it("知らない名前は注意を出す", () => {
    const w: string[] = [];
    applyGuitarTone({ guitarTone: "nope" }, "p", w);
    expect(w[0]).toContain("nope");
  });
  it("曲に使うと autoScoop が止まり、アンプがプリセットのものになる", () => {
    const { song, score } = aiSongToScore({ bpm: 120, beats: 4, chords: "C G", barsPerChord: 1, repeats: 1,
      parts: [{ instrument: "leadGuitar", role: "旋律", volume: 0.2, pan: 0, notes: "C5:4 D5:4", guitarTone: "warm-lead-a" }] });
    expect(song.autoScoop).toBe(false);
    expect(JSON.stringify(score)).toContain('"lead"');
    expect(Object.keys(GUITAR_TONES)).toContain("warm-lead-a");
  });
});
