import { describe, expect, it } from "vitest";
import { midiToFrequency, noteNameToFrequency, noteNameToMidi } from "./note";

describe("noteNameToMidi", () => {
  it("C4はMIDIノート番号60", () => {
    expect(noteNameToMidi("C4")).toBe(60);
  });

  it("シャープ・フラットを扱える", () => {
    expect(noteNameToMidi("C#4")).toBe(61);
    expect(noteNameToMidi("Db4")).toBe(61);
  });

  it("不正な音名は例外を投げる", () => {
    expect(() => noteNameToMidi("H4")).toThrow();
    expect(() => noteNameToMidi("")).toThrow();
  });
});

describe("midiToFrequency", () => {
  it("A4（MIDI69）は440Hz", () => {
    expect(midiToFrequency(69)).toBeCloseTo(440, 5);
  });

  it("1オクターブ上は周波数が2倍", () => {
    expect(midiToFrequency(81)).toBeCloseTo(880, 5);
  });
});

describe("noteNameToFrequency", () => {
  it("A4は440Hz", () => {
    expect(noteNameToFrequency("A4")).toBeCloseTo(440, 5);
  });
});
