import { describe, expect, it } from "vitest";
import { getTrack } from "./catalog";
import { trackTotalBeats, trackToNotes } from "./edit";
import { scoreToMidi } from "./midi-export";
import { midiToScore, programToInstrument } from "./midi-import";
import { createBlankScore } from "./blank-song";
import { barBeats, parseTimeSignature } from "./time-signature";

/** テスト用の小さなMIDI（480分割・1トラック）を作る。events は [デルタ, ...バイト]。 */
function smf(events: number[][]): Uint8Array {
  const vlq = (n: number): number[] => {
    const out = [n & 0x7f];
    while ((n >>= 7)) out.unshift((n & 0x7f) | 0x80);
    return out;
  };
  const body = events.flatMap(([delta, ...bytes]) => [...vlq(delta), ...bytes]).concat([0, 0xff, 0x2f, 0]);
  const u32 = (n: number): number[] => [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255];
  return new Uint8Array([0x4d, 0x54, 0x68, 0x64, ...u32(6), 0, 0, 0, 1, 1, 0xe0, 0x4d, 0x54, 0x72, 0x6b, ...u32(body.length), ...body]);
}

describe("MIDIの読み込み", () => {
  it("テンポ・拍子・和音（別トラックへ）・ドラムを読める", () => {
    const r = midiToScore(smf([
      [0, 0xff, 0x51, 3, 0x07, 0xa1, 0x20], // 120
      [0, 0xff, 0x58, 4, 3, 2, 24, 8], // 3/4
      [0, 0xc0, 0], [0, 0x90, 60, 100], [0, 0x90, 64, 100], [0, 0x99, 36, 110],
      [240, 0x89, 36, 0], [720, 0x80, 60, 0], [0, 0x80, 64, 0],
      [0, 0x90, 67, 80], [480, 0x90, 67, 0], // ランニングステータスなし・ノートオンの強さ0で離す
    ]));
    expect(r.score.tempoBpm).toBe(120);
    expect(r.score.timeSig).toEqual({ num: 3, den: 4 });
    const pianos = r.score.tracks.filter((t) => t.instrument === "piano");
    expect(pianos.length).toBe(2);
    expect(trackToNotes(pianos[0]).map((n) => [n.note, n.start, n.dur])).toEqual([["E4", 0, 2], ["G4", 2, 1]]);
    expect(trackToNotes(pianos[1]).map((n) => n.note)).toEqual(["C4"]);
    expect(r.score.tracks.find((t) => t.instrument === "kick")).toBeDefined();
    for (const t of r.score.tracks) expect(trackTotalBeats(t)).toBe(3);
  });
  it("ゲームの曲をMIDIにして、読みもどせる", () => {
    const back = midiToScore(scoreToMidi(getTrack("town-touri")));
    expect(back.notes).toBeGreaterThan(100);
    expect(back.score.tempoBpm).toBe(getTrack("town-touri").tempoBpm);
  });
  it("MIDIでないものは断る", () => {
    expect(() => midiToScore(new Uint8Array([1, 2, 3]))).toThrow(/MIDI/);
  });
  it("楽器番号から近い楽器を選ぶ", () => {
    expect(programToInstrument(0)).toBe("piano");
    expect(programToInstrument(30)).toBe("distGuitar");
    expect(programToInstrument(40)).toBe("strings");
    expect(programToInstrument(127)).toBe("pad");
  });
});

describe("1から作る曲と拍子", () => {
  it("拍子と小節の数から、空の曲を作れる", () => {
    const s = createBlankScore({ bpm: 140, sig: { num: 7, den: 8 }, bars: 8, template: "band" });
    expect(s.timeSig).toEqual({ num: 7, den: 8 });
    for (const t of s.tracks) expect(trackTotalBeats(t)).toBe(28);
  });
  it("拍子の読み書き", () => {
    expect(parseTimeSignature("5/4")).toEqual({ num: 5, den: 4 });
    expect(parseTimeSignature("13/16")).toEqual({ num: 13, den: 16 });
    expect(parseTimeSignature("4/3")).toBeNull();
    expect(barBeats({ num: 6, den: 8 })).toBe(3);
  });
  it("MIDIに拍子が書き込まれる", () => {
    const s = createBlankScore({ bpm: 100, sig: { num: 5, den: 4 }, bars: 2, template: "single" });
    s.tracks[0].notes = [{ note: "C4", durationBeats: 10 }];
    expect(midiToScore(scoreToMidi(s)).score.timeSig).toEqual({ num: 5, den: 4 });
  });
});
