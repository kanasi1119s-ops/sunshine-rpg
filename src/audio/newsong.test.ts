import { describe, expect, it } from "vitest";
import { buildNewSong, parseChord } from "./newsong";
import { trackTotalBeats } from "./edit";
import { noteNameToMidi } from "./note";
import { REST } from "./score";

const spec = { bpm: 100, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2, feel: "rock" as const, leadInstrument: "leadGuitar" as const };

describe("新しい曲（コード進行から伴奏）", () => {
  it("コード名を読める", () => {
    expect(parseChord("Am")).toEqual({ root: 9, intervals: [0, 3, 7] });
    expect(parseChord("Bbmaj7")).toEqual({ root: 10, intervals: [0, 4, 7, 11] });
    expect(parseChord("F#m7")?.root).toBe(6);
    expect(parseChord("H")).toBeNull();
    expect(parseChord("Cxyz")).toBeNull();
  });
  it("すべてのトラックの長さがそろい（8小節×4拍=32拍）、音名が読める", () => {
    for (const feel of ["rock", "ballad", "pop"] as const) for (const beats of [3, 4, 7]) {
      const s = buildNewSong({ ...spec, feel, beats });
      const total = 8 * beats;
      for (const t of s.tracks) {
        expect(trackTotalBeats(t)).toBeCloseTo(total, 6);
        for (const n of t.notes) if (n.note !== REST) expect(Number.isFinite(noteNameToMidi(n.note))).toBe(true);
      }
    }
  });
  it("ベースは、コードの根音を鳴らす", () => {
    const bass = buildNewSong(spec).tracks.find((t) => t.instrument === "bass")!;
    expect(noteNameToMidi(bass.notes[0].note) % 12).toBe(9);
  });
  it("読めないコードは断る", () => {
    expect(() => buildNewSong({ ...spec, chords: "Am Q" })).toThrow(/読めない/);
    expect(() => buildNewSong({ ...spec, chords: "" })).toThrow();
  });
});
