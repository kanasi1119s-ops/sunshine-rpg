import { describe, expect, it } from "vitest";
import { applySections } from "./arrangement";
import { FILLS, overwriteRange, pickFill, placeFill } from "./drum-fills";
import { REST, type NoteEvent, type Track } from "./score";

const beats = (ns: NoteEvent[]): number => ns.reduce((a, n) => a + n.durationBeats, 0);
const grid = (inst: "kick" | "snare" | "hihat", bars: number): Track => ({ waveform: "square", instrument: inst, volume: 0.1, pan: 0, notes: Array.from({ length: bars * 16 }, (_, i) => (inst === "hihat" || i % 4 === 0 ? { note: "C2", durationBeats: 0.25 } : { note: REST, durationBeats: 0.25 })) });

describe("ドラムのおかず", () => {
  it("型は、どれも8マス。タムの数字は1〜6", () => {
    for (const f of FILLS) {
      for (const lane of [f.S, f.K, f.T, ...(f.H !== undefined ? [f.H] : [])]) expect(lane.length, f.id).toBe(8);
      expect(f.T).toMatch(/^[1-6.]{8}$/);
    }
  });
  it("overwriteRange: 長さは変わらず、指定の範囲だけが入れ替わる（またがる音符は切る）", () => {
    const base: NoteEvent[] = [{ note: "C2", durationBeats: 1 }, { note: "C2", durationBeats: 3 }];
    const out = overwriteRange(base, 2, 4, [{ note: "D2", durationBeats: 2 }]);
    expect(beats(out)).toBe(4);
    expect(out.map((n) => n.note)).toEqual(["C2", "C2", "D2"]);
    expect(out[1].durationBeats).toBe(1);
  });
  it("placeFill: 全トラックの長さが保たれ、タムのトラックが作られる", () => {
    const tracks = [grid("kick", 2), grid("snare", 2), grid("hihat", 2)];
    const out = placeFill(tracks, pickFill("big", 0), 6, 8);
    for (const t of out) expect(beats(t.notes)).toBeCloseTo(8);
    const tom = out.find((t) => t.instrument === "tom");
    expect(tom).toBeTruthy();
    expect(tom!.notes.some((n) => n.note === "C4")).toBe(true);
  });
  it("applySections: サビの前の小節に big のおかず（タム）、fills=false なら入れない", () => {
    const secs = [{ kind: "verse" as const, bars: 4 }, { kind: "pre" as const, bars: 4 }, { kind: "chorus" as const, bars: 4 }];
    const mk = (): Track[] => [grid("kick", 12), grid("snare", 12), grid("hihat", 12)];
    const withFills = applySections(mk(), secs, 4, true);
    const tom = withFills.find((t) => t.instrument === "tom");
    expect(tom).toBeTruthy();
    expect(beats(tom!.notes)).toBeCloseTo(48);
    // サビ前（pre の最後の小節 = 8小節目の後ろ2拍 = 拍 30〜32）に音がある
    let pos = 0;
    const hit = tom!.notes.some((n) => { const s = pos; pos += n.durationBeats; return n.note !== REST && s >= 30 && s < 32; });
    expect(hit).toBe(true);
    expect(applySections(mk(), secs, 4, false).some((t) => t.instrument === "tom")).toBe(false);
  });
});
