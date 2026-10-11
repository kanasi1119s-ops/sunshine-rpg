import { describe, expect, it } from "vitest";
import { parseNotes } from "./ai-song";
import { accentTopNotes, autoArticulation, hash01 } from "./articulation";
import type { Track } from "./score";

const ev = (s: string) => parseNotes(s, false, [], "t");

describe("autoArticulation", () => {
  it("フレーズ最後の 1.5 拍以上の音にだけビブラート", () => {
    const out = autoArticulation(ev("E4:1 G4:2 R:1 A4:1 C5:2"), "leadGuitar", "", "s");
    expect(out.map((e) => e.vibrato)).toEqual([undefined, 0.7, undefined, undefined, 0.7]);
  });
  it("指定済みの音は変えない", () => {
    const out = autoArticulation(ev("E4:2~~ G4:2^"), "guitar", "", "s");
    expect(out[0].vibrato).toBe(1);
    expect(out[1].vibrato).toBeUndefined();
  });
  it("strings の旋律は 2 度以内の音をレガートでつなぎ、内声（役割が違う）には付けない", () => {
    const melody = autoArticulation(ev("C5:1 D5:1 F5:1 G5:1"), "strings", "主旋律");
    expect(melody.map((e) => e.gate)).toEqual([1.15, undefined, 1.15, undefined]);
    expect(autoArticulation(ev("C5:1 D5:1"), "strings", "内声").every((e) => e.gate === undefined)).toBe(true);
  });
  it("ハンマリング／プルオフ: 短い 2 音の 2 音目を弱く、1 音目をつなぐ。同じ seed なら同じ結果", () => {
    const src = ev("A4:0.25 C5:0.25 A4:0.25 C5:0.25 A4:0.25 C5:0.25 A4:0.25 C5:0.25 A4:0.25 C5:0.25 A4:0.25 C5:0.25 D5:1");
    const a = autoArticulation(src, "guitar", "", "seed1");
    const b = autoArticulation(src, "guitar", "", "seed1");
    expect(a).toEqual(b);
    const marked = a.filter((e) => e.velocity === 0.7).length;
    expect(marked).toBeGreaterThan(0);
    a.forEach((e, i) => { if (e.velocity === 0.7) expect(a[i - 1].gate).toBe(1.15); });
    expect(autoArticulation(src, "guitar", "", "seed2")).not.toEqual(a);
  });
  it("slap: 拍頭が強く、オクターブ上の音は短く", () => {
    const out = autoArticulation(ev("E2:1 E3:0.5 G2:0.5 A2:1"), "slap");
    expect(out[0].velocity).toBe(1.3);
    expect(out[1].gate).toBe(0.4);
    expect(out[2].velocity).toBeUndefined();
    expect(out[3].velocity).toBe(1.3);
  });
  it("hash01 は 0〜1 で決定的", () => {
    expect(hash01("a", 1)).toBe(hash01("a", 1));
    expect(hash01("a", 1)).toBeGreaterThanOrEqual(0);
    expect(hash01("a", 1)).toBeLessThan(1);
  });
});

describe("accentTopNotes", () => {
  const tr = (instrument: Track["instrument"], notes: string): Track => ({ waveform: "sine", instrument, volume: 0.2, notes: ev(notes) });
  it("同時に始まるピアノ音の最高音に ! を付ける", () => {
    const out = accentTopNotes([tr("piano", "C4:1 D4:1"), tr("piano", "G4:1 A4:1"), tr("piano", "E5:1 R:1")], [true, true, true]);
    expect(out[2].notes[0].velocity).toBe(1.3);
    expect(out[0].notes[0].velocity).toBeUndefined();
    expect(out[1].notes[0].velocity).toBeUndefined();
  });
  it("対象外の楽器・フラグなしのパートは変えない", () => {
    const tracks = [tr("guitar", "C4:1"), tr("guitar", "G4:1")];
    expect(accentTopNotes(tracks, [true, true])).toEqual(tracks);
    const pianos = [tr("piano", "C4:1"), tr("piano", "G4:1")];
    expect(accentTopNotes(pianos, [true, false])).toEqual(pianos);
  });
});
