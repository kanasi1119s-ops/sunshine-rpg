import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { applySections, autoSections, fitSections } from "./arrangement";
import type { Track } from "./score";

const beatsOf = (t: Track): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const barOn = (t: Track, bar: number, bpb = 4): boolean => {
  let pos = 0;
  for (const n of t.notes) {
    if (pos + 1e-9 >= bar * bpb && pos < (bar + 1) * bpb - 1e-9 && n.note !== "R") return true;
    pos += n.durationBeats;
  }
  return false;
};
const song = (extra: object, bars = 32) => aiSongToScore({
  title: "t", description: "", bpm: 120, beats: 4, repeats: 1, chords: Array(bars).fill("Am").join(" "), barsPerChord: 1,
  autoAccompaniment: true, feel: "pop", tone: "rock", parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "A4:4" }], ...extra,
} as never);

describe("セクション編曲", () => {
  it("auto は曲の小節数ちょうどで、導入で始まりサビを含む", () => {
    for (const n of [8, 16, 24, 32, 48, 64]) {
      const s = autoSections(n);
      expect(s.reduce((a, x) => a + x.bars, 0)).toBe(n);
      expect(s.every((x) => x.bars >= 1)).toBe(true);
      if (n >= 24) expect(s.some((x) => x.kind === "chorus")).toBe(true);
    }
    expect(autoSections(32)[0].kind).toBe("intro");
  });
  it("小節数のずれは、延ばすか切って、注意を返す", () => {
    expect(fitSections([{ kind: "verse", bars: 4 }], 8).sections[0].bars).toBe(8);
    expect(fitSections([{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 8 }], 8).sections.map((x) => x.bars)).toEqual([4, 4]);
    expect(fitSections([{ kind: "verse", bars: 8 }], 8).warning).toBeUndefined();
  });
  it("導入はドラムなし、サビは全部と頭のクラッシュ、間奏はドラムなし", () => {
    const { score } = song({ sections: [{ kind: "intro", bars: 4 }, { kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }, { kind: "interlude", bars: 4 }, { kind: "chorus", bars: 8 }] });
    const by = (i: string) => score.tracks.find((t) => t.instrument === i)!;
    expect(barOn(by("kick"), 1)).toBe(false);
    expect(barOn(by("piano"), 1)).toBe(true);
    expect(barOn(by("kick"), 6)).toBe(true);
    expect(barOn(by("snare"), 6)).toBe(false);
    expect(barOn(by("snare"), 13)).toBe(true);
    expect(barOn(by("kick"), 21)).toBe(false);
    expect(barOn(by("crash"), 12)).toBe(true);
    expect(barOn(by("crash"), 13)).toBe(false);
    for (const t of score.tracks.filter((x) => x.instrument !== "lead")) expect(beatsOf(t)).toBeCloseTo(128, 6);
  });
  it("サビの前の小節は、スネアで助走する", () => {
    const { score } = song({ sections: [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }] }, 16);
    const snare = score.tracks.find((t) => t.instrument === "snare")!;
    expect(barOn(snare, 6)).toBe(false);
    expect(barOn(snare, 7)).toBe(true);
  });
  it("Bメロは だんだん強くなり、サビは元の強さ", () => {
    const tracks: Track[] = [{ waveform: "square", instrument: "piano", volume: 0.1, pan: 0, notes: Array.from({ length: 16 }, () => ({ note: "C4", durationBeats: 1, velocity: 100 })) }];
    const out = applySections(tracks, [{ kind: "pre", bars: 2 }, { kind: "chorus", bars: 2 }], 4)[0].notes;
    expect(out[0].velocity!).toBeLessThan(out[7].velocity!);
    expect(out[8].velocity).toBe(100);
  });
  it("sections なし・autoAccompaniment なしでは何も変えない", () => {
    const a = song({}).score.tracks.find((t) => t.instrument === "kick")!;
    expect(barOn(a, 0)).toBe(true);
    const b = song({ autoAccompaniment: false, sections: "auto" });
    expect(b.score.tracks.some((t) => t.instrument === "kick")).toBe(false);
  });
  it("おかしな kind は注意して Aメロにする", () => {
    const { warnings } = song({ sections: [{ kind: "zzz", bars: 32 }] });
    expect(warnings.join("\n")).toContain("zzz");
  });
});
