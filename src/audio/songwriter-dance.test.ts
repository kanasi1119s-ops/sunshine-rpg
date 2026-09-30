import { describe, expect, it } from "vitest";
import { composeSong, keyOf, walkBass } from "./songwriter";
import { trackTotalBeats } from "./edit";
import { noteNameToMidi } from "./note";
import { REST } from "./score";

describe("作曲エンジン: ダンス×ロック・きれいなダンス", () => {
  for (const style of ["dancerock", "cleandance"] as const) {
    it(`${style}: 全トラックの長さがそろい、ベースは音域内でメロディのように動き、左右に広がる`, () => {
      for (const seed of [1, 7, 42]) {
        const s = composeSong({ id: "t", title: "t", scene: "", style, tonic: "D", minor: seed % 2 === 1, bpm: 150, seed, targetSec: 90 });
        const total = trackTotalBeats(s.tracks[0]);
        for (const t of s.tracks) expect(trackTotalBeats(t)).toBeCloseTo(total, 6);
        const bass = s.tracks.find((t) => t.instrument === "bass")!;
        const notes = bass.notes.filter((n) => n.note !== REST).map((n) => noteNameToMidi(n.note));
        for (const m of notes) {
          expect(m).toBeGreaterThanOrEqual(28);
          expect(m).toBeLessThanOrEqual(55);
        }
        expect(new Set(notes.map((m) => m % 12)).size).toBeGreaterThanOrEqual(6);
        const pans = s.tracks.map((t) => t.pan ?? 0);
        expect(Math.min(...pans)).toBeLessThanOrEqual(-0.6);
        expect(Math.max(...pans)).toBeGreaterThanOrEqual(0.7);
        expect(s.style).toBe(style);
      }
    });
  }
  it("cleandance は歪んだギターとシンセのリードを使わない", () => {
    const s = composeSong({ id: "t", title: "t", scene: "", style: "cleandance", tonic: "C", minor: false, bpm: 140, seed: 3 });
    expect(s.tracks.some((t) => t.instrument === "distGuitar" || t.instrument === "lead")).toBe(false);
  });
  it("walkBass: 小節の最後の音を、次の小節の最初の音へ向かう音にし、和音と半音でぶつかる音は避ける", () => {
    const key = keyOf({ tonic: "D", minor: true });
    // A（ラ・ド#・ミ）の小節の最後から、Dm の小節へ。C（ド）はド#と半音でぶつかるので選ばない
    const out = walkBass(
      [{ note: "A2", durationBeats: 2 }, { note: "E3", durationBeats: 1 }, { note: "A2", durationBeats: 1 }, { note: "D3", durationBeats: 4 }],
      ["A", "Dm"], 4, key,
    );
    expect(out[2].note).not.toBe("A2");
    expect(out[2].note).not.toBe("C3");
    expect(Math.abs(noteNameToMidi(out[2].note) - noteNameToMidi("D3"))).toBeLessThanOrEqual(3);
  });
});
