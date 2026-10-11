import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { fitTokens, expandLaps, SCENE_LAPS } from "./laps";
import { parseSections, resolveLayers } from "./arrangement";

const beatsOf = (tokens: string[]): number => tokens.reduce((a, t) => a + Number(t.split(":")[1]), 0);
const song = (extra: Record<string, unknown> = {}, parts?: unknown[]): AiSong => ({
  title: "t", description: "d", bpm: 100, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 4, autoAccompaniment: true, feel: "pop", tone: "rock",
  parts: parts ?? [{ instrument: "lead", role: "lead", volume: 0.25, pan: 0, amp: "auto", notes: "C5:4 D5:4 E5:4 G5:4" }], ...extra,
} as AiSong);
const total = (s: AiSong): number => Number(s.beats) * (s as unknown as { repeats: number }).repeats * 4;

describe("fitTokens", () => {
  it("短ければくり返し、長ければ切って、ちょうどの拍数にする", () => {
    expect(beatsOf(fitTokens("C4:1 D4:1", 8))).toBe(8);
    expect(fitTokens("C4:4 D4:4", 6)).toEqual(["C4:4", "D4:2"]);
    expect(fitTokens("", 4)).toEqual(["R:4"]);
    expect(beatsOf(fitTokens("R:2", 100))).toBe(100);
  });
});

describe("laps / lap2", () => {
  it("laps なしは何も変えない", () => {
    const s = song();
    expect(expandLaps(s as never)).toBe(s);
  });

  it("laps: 2 は repeats が2倍になり、パートは1周ずつ並ぶ", () => {
    const w: string[] = [];
    const out = expandLaps(song({ laps: 2 }) as never, w) as unknown as AiSong;
    expect(out.repeats).toBe(8);
    expect(beatsOf(out.parts[0].notes.split(" "))).toBe(128);
    expect(w).toEqual([]);
  });

  it("lap2.parts.octave で2周目の旋律が1オクターブ上がる", () => {
    const out = expandLaps(song({ laps: 2, lap2: { parts: { lead: { octave: 1 } } } }) as never) as unknown as AiSong;
    const t = out.parts[0].notes.split(" ");
    expect(t.slice(0, 4)).toEqual(["C5:4", "D5:4", "E5:4", "G5:4"]);
    expect(t.slice(16, 20)).toEqual(["C6:4", "D6:4", "E6:4", "G6:4"]);
  });

  it("lap2.parts.notes で2周目のおかず（旋律）を替える", () => {
    const out = expandLaps(song({ laps: 2, lap2: { parts: { lead: { notes: "A5:16" } } } }) as never) as unknown as AiSong;
    const t = out.parts[0].notes.split(" ");
    expect(t).toContain("A5:16");
    expect(beatsOf(t)).toBe(128);
  });

  it("lap2.addParts は2周目から鳴る（1周目は休み）", () => {
    const out = expandLaps(song({ laps: 2, lap2: { addParts: [{ instrument: "bell", role: "鐘", volume: 0.12, pan: 0.4, notes: "C6:2 R:2" }] } }) as never) as unknown as AiSong;
    expect(out.parts).toHaveLength(2);
    const bell = out.parts[1].notes.split(" ");
    expect(beatsOf(bell)).toBe(128);
    expect(bell.slice(0, 2)).toEqual(["R:32", "R:32"]);
    expect(bell).toContain("C6:2");
  });

  it("sections／energy が周ごとにコピーされ、add・gain・energyDelta が2周目だけに入る", () => {
    const sections = [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }];
    const out = expandLaps(song({ laps: 2, sections, energy: [4, 8], lap2: { add: ["guitar"], gain: 0.05, energyDelta: 1 } }) as never) as unknown as { sections: { kind: string; add?: string[]; gain?: number }[]; energy: number[] };
    expect(out.sections).toHaveLength(4);
    expect(out.sections[0].add).toBeUndefined();
    expect(out.sections[2]).toMatchObject({ kind: "verse", add: ["guitar"], gain: 0.05 });
    expect(out.energy).toEqual([4, 8, 5, 9]);
  });

  it("scene だけの曲でも sections を作って周ごとに並べる（occurrence も入る）", () => {
    const out = expandLaps(song({ laps: 2, scene: "town", repeats: 8, lap2: { add: ["strings"] } }) as never) as unknown as { sections: unknown[]; occurrence?: boolean };
    expect(out.sections).toHaveLength(8);
    expect(out.occurrence).toBe(true);
  });

  it('laps: "auto" は scene の標準（town は2周、sad は変えない）', () => {
    expect(SCENE_LAPS.town).toBe(2);
    expect((expandLaps(song({ laps: "auto", scene: "town" }) as never) as unknown as AiSong).repeats).toBe(8);
    const sad = song({ laps: "auto", scene: "sad" });
    expect(expandLaps(sad as never)).toBe(sad);
  });

  it("3周目は lap3 がなければ lap2 の差を使う", () => {
    const out = expandLaps(song({ laps: 3, lap2: { parts: { lead: { octave: 1 } } } }) as never) as unknown as AiSong;
    const t = out.parts[0].notes.split(" ");
    expect(t[32]).toBe("C6:4");
    const out2 = expandLaps(song({ laps: 3, lap2: { parts: { lead: { octave: 1 } } }, lap3: { parts: { lead: { octave: -1 } } } }) as never) as unknown as AiSong;
    expect(out2.parts[0].notes.split(" ")[32]).toBe("C4:4");
  });

  it("使えない laps は無視して注意", () => {
    const w: string[] = [];
    const s = song({ laps: 9 });
    expect(expandLaps(s as never, w)).toBe(s);
    expect(w.join()).toContain("laps");
  });

  it("ドラムの短い型はそのまま（くり返しで埋まる）", () => {
    const s = song({ laps: 2 }, [{ instrument: "kick", role: "k", volume: 0.3, pan: 0, notes: "x:1 R:1" }]);
    const out = expandLaps(s as never) as unknown as AiSong;
    expect(out.parts[0].notes).toBe("x:1 R:1");
  });

  it("1周より長い手書きはそのまま", () => {
    const long = Array.from({ length: 12 }, () => "C5:8").join(" ");
    const out = expandLaps(song({ laps: 2 }, [{ instrument: "lead", role: "lead", volume: 0.2, pan: 0, notes: long }]) as never) as unknown as AiSong;
    expect(out.parts[0].notes).toBe(long);
  });
});

describe("sections の add・gain（resolveLayers）", () => {
  it("add の群が足され、gain で強さが変わる", () => {
    const secs = parseSections([{ kind: "verse", bars: 8 }, { kind: "verse", bars: 8, add: ["pad", "foo"], gain: 0.1 }], []);
    const l = resolveLayers(secs);
    expect(l[1].groups).toContain("pad");
    expect(l[1].groups).not.toContain("foo" as never);
    expect(l[1].from).toBeCloseTo(l[0].from + 0.1);
  });
});

describe("aiSongToScore との結合", () => {
  it("laps: 2 で曲の長さが2倍になり、2周目の旋律が上がる", () => {
    const once = aiSongToScore(song());
    const twice = aiSongToScore(song({ laps: 2, lap2: { parts: { lead: { octave: 1 } } } }));
    const len = (s: ReturnType<typeof aiSongToScore>): number => s.score.tracks[0].notes.reduce((a, n) => a + n.durationBeats, 0);
    expect(len(twice)).toBe(len(once) * 2);
    const lead = twice.score.tracks.find((t) => t.instrument === "lead")!;
    expect(lead.notes[0].note).toBe("C5");
    expect(lead.notes.find((n) => n.note === "C6")).toBeTruthy();
    expect(twice.score.meta?.laps).toBe(2);
    expect(twice.warnings.filter((w) => w.includes("laps"))).toEqual([]);
  });
  it("laps:2 の長さの見積もり", () => {
    expect(total(song())).toBe(64);
  });
});
