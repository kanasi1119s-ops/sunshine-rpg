import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { sanitizeFx } from "./master-fx";
import { composeSong } from "./songwriter";

describe("マスターエフェクト", () => {
  it("範囲外の値を整え、使えない値は捨てる", () => {
    expect(sanitizeFx({ bitcrush: 1, tape: 5, chorus: -1, delay: { beats: 100, feedback: 2, mix: 9 }, tremolo: { periodBeats: 0.5, depth: 3 }, filter: { type: "bandpass", hz: 1000 } })).toEqual({
      bitcrush: 4, tape: 1, delay: { beats: 4, feedback: 0.85, mix: 1 }, tremolo: { periodBeats: 0.5, depth: 1 },
    });
    expect(sanitizeFx({})).toBeUndefined();
    expect(sanitizeFx("x")).toBeUndefined();
  });
  it("AIソングの fx が曲に入る", () => {
    const { score } = aiSongToScore({ title: "t", description: "", bpm: 100, beats: 4, chords: "C", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "pop", tone: "rock", fx: { tape: 0.5, chorus: 0.4 }, parts: [{ instrument: "piano", role: "p", volume: 0.2, pan: 0, amp: "auto", notes: "C4:4" }] });
    expect(score.fx).toEqual({ tape: 0.5, chorus: 0.4 });
  });
  it("ジャンルの型にもエフェクトが付く（ローファイ）", () => {
    expect(composeSong({ id: "t", title: "t", scene: "", style: "lofi", tonic: "C", minor: false, bpm: 0, seed: 1 }).fx?.tape).toBeGreaterThan(0);
  });
});
