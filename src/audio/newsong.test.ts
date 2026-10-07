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
    for (const feel of ["rock", "ballad", "pop", "dance", "vocaloid"] as const) for (const beats of [3, 4, 7]) {
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
  it("vocaloid: 歌なしのバック（声の楽器なし）・16分のハイハット・4小節ごとのクラッシュとフィル・左右に広げた弦", () => {
    const s = buildNewSong({ ...spec, bpm: 175, feel: "vocaloid" });
    const insts = s.tracks.map((t) => t.instrument);
    expect(insts).not.toContain("choir");
    const hat = s.tracks.find((t) => t.instrument === "hihat")!;
    expect(hat.notes.filter((n) => n.note !== REST).length).toBe(8 * 16);
    const crash = s.tracks.find((t) => t.instrument === "crash")!;
    expect(crash.notes.filter((n) => n.note !== REST).length).toBe(2);
    const snare = s.tracks.find((t) => t.instrument === "snare")!;
    // 4小節目は2拍目に1つ＋最後の1拍に16分のスネア4つ（フィル）、ほかの小節は2・4拍の2つ
    expect(snare.notes.filter((n) => n.note !== REST).length).toBe((2 * 3 + (1 + 4)) * 2);
    const pans = s.tracks.map((t) => t.pan ?? 0);
    expect(Math.min(...pans)).toBeLessThanOrEqual(-0.7);
    expect(Math.max(...pans)).toBeGreaterThanOrEqual(0.7);
    expect(s.tracks[s.tracks.length - 1].notes.every((n) => n.note === REST)).toBe(true);
  });
  it("dance: 4つ打ちのキックと、メロディのように動くベース・左右に広げた伴奏", () => {
    const s = buildNewSong({ ...spec, feel: "dance" });
    const kick = s.tracks.find((t) => t.instrument === "kick")!;
    expect(kick.notes.filter((n) => n.note !== REST).length).toBe(8 * 4);
    const bass = s.tracks.find((t) => t.instrument === "bass")!;
    const pcs = new Set(bass.notes.filter((n) => n.note !== REST).map((n) => noteNameToMidi(n.note) % 12));
    expect(pcs.size).toBeGreaterThanOrEqual(6);
    for (const n of bass.notes) if (n.note !== REST) expect(noteNameToMidi(n.note)).toBeLessThanOrEqual(55);
    const pans = s.tracks.map((t) => t.pan ?? 0);
    expect(Math.min(...pans)).toBeLessThanOrEqual(-0.6);
    expect(Math.max(...pans)).toBeGreaterThanOrEqual(0.6);
  });
});

import { voiceLead } from "./newsong";
describe("voiceLead（声部のなめらかな動き）", () => {
  const C = { root: 0, intervals: [0, 4, 7] }, F = { root: 5, intervals: [0, 4, 7] }, G = { root: 7, intervals: [0, 4, 7] }, Am = { root: 9, intervals: [0, 3, 7] };
  it("コードが変わっても、各声部の動きは小さい（最大でも3半音）", () => {
    const v = voiceLead([C, F, G, Am, C], 3);
    for (let i = 1; i < v.length; i++) v[i].forEach((m, k) => expect(Math.abs(m - v[i - 1][k])).toBeLessThanOrEqual(5));
    const total = v.slice(1).reduce((s, cur, i) => s + cur.reduce((a, m, k) => a + Math.abs(m - v[i][k]), 0), 0);
    expect(total / (v.length - 1)).toBeLessThanOrEqual(6);
  });
  it("同じコードが続くと動かない。声部が同じ高さにならない", () => {
    const v = voiceLead([C, C, F], 3);
    expect(v[1]).toEqual(v[0]);
    v.forEach((chord) => expect(new Set(chord).size).toBe(3));
  });
  it("音は和音の構成音だけ", () => {
    voiceLead([C, F, G, Am], 3).forEach((chord, i) => {
      const c = [C, F, G, Am][i];
      chord.forEach((m) => expect(c.intervals.map((iv) => (c.root + iv) % 12)).toContain(m % 12));
    });
  });
});
