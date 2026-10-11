import { describe, expect, it } from "vitest";
import { applySections, parseLayers, peelGroups, resolveLayers, type Section } from "./arrangement";
import { aiSongToScore, type AiSong } from "./ai-song";
import type { Track } from "./score";

describe("peel（層をはがして消える）", () => {
  it("1小節ごとに、リズム楽器 → 彩り → 和音 → 低音の順に1群ずつ減り、最後は1群", () => {
    const g = ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"] as const;
    const counts = Array.from({ length: 10 }, (_, b) => peelGroups([...g], true, b).length);
    expect(counts).toEqual([7, 6, 5, 4, 3, 2, 1, 1, 1, 1]);
    expect(peelGroups([...g], true, 6)).toEqual(["bass"]);
    expect(peelGroups([...g], true, 1)).not.toContain("hat");
    expect(peelGroups([...g], true, 3)).not.toContain("kick");
  });
  it("数字は N 小節ごと", () => {
    const g = ["kick", "bass", "keys"] as const;
    expect(Array.from({ length: 6 }, (_, b) => peelGroups([...g], 2, b).length)).toEqual([3, 3, 2, 2, 1, 1]);
  });
  it("peel なしは変わらない", () => {
    expect(peelGroups(["kick", "bass"], undefined, 5)).toEqual(["kick", "bass"]);
    expect(peelGroups(["kick", "bass"], false, 5)).toEqual(["kick", "bass"]);
  });
  it("layers の peel を読む", () => {
    const w: string[] = [];
    const l = parseLayers({ outro: { peel: true }, tag: { peel: 2 }, verse: { peel: "x" } }, w);
    expect(l?.outro).toMatchObject({ peel: true });
    expect(l?.tag).toMatchObject({ peel: 2 });
    expect((l?.verse as { peel?: unknown }).peel).toBeUndefined();
  });
  it("energy で群を決めた曲にも layers の peel が乗る", () => {
    const secs: Section[] = [{ kind: "chorus", bars: 4 }, { kind: "outro", bars: 6 }];
    const l = resolveLayers(secs, { perSection: [{ groups: ["kick", "bass"], from: 1, to: 1 }, { groups: ["kick", "bass", "keys"], from: 0.8, to: 0.5 }], layers: { outro: { peel: true } } });
    expect(l[1].peel).toBe(true);
    expect(l[0].peel).toBeUndefined();
  });

  const mk = (instrument: Track["instrument"]): Track => ({ waveform: "sawtooth", instrument, volume: 0.2, notes: Array.from({ length: 12 }, () => ({ note: "C3", durationBeats: 1 })) });
  it("applySections: outro の中で小節ごとに鳴る楽器が減る", () => {
    const tracks = [mk("hihat"), mk("bass"), mk("piano"), mk("strings")];
    const secs: Section[] = [{ kind: "outro", bars: 3 }];
    const out = applySections(tracks, secs, 4, false, { layers: { outro: { groups: ["hat", "bass", "keys", "strings"], from: 1, to: 1, peel: true } } });
    const playing = (inst: string, bar: number): boolean => {
      const t = out.find((x) => x.instrument === inst)!;
      let pos = 0;
      for (const n of t.notes) { if (pos >= bar * 4 && pos < bar * 4 + 4 && n.note !== "R") return true; pos += n.durationBeats; }
      return false;
    };
    expect(["hihat", "bass", "piano", "strings"].map((i) => playing(i, 0))).toEqual([true, true, true, true]);
    expect(["hihat", "bass", "piano", "strings"].map((i) => playing(i, 1))).toEqual([false, true, true, true]);
    expect(["hihat", "bass", "piano", "strings"].map((i) => playing(i, 2))).toEqual([false, true, true, false]); // hat・strings の順にはがれて、keys と bass が残る
  });

  it("曲のJSONの layers.outro.peel が通る", () => {
    const song: AiSong = {
      title: "t", description: "d", bpm: 80, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 3, autoAccompaniment: true, feel: "ballad", tone: "rock",
      sections: [{ kind: "verse", bars: 8 }, { kind: "outro", bars: 4 }], layers: { outro: { groups: ["hat", "bass", "keys", "strings"], peel: true } },
      parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "C5:4" }],
    } as AiSong;
    const { warnings } = aiSongToScore(song);
    expect(warnings.filter((w) => w.includes("layers"))).toEqual([]);
  });
});
