import { describe, expect, it } from "vitest";
import { scoreToMidiInfo } from "./midi-export";
import type { Score } from "./score";

const score: Score = {
  tempoBpm: 120,
  loop: true,
  tone: "rock",
  tracks: [
    { waveform: "square", instrument: "kick", volume: 0.2, pan: 0, notes: [{ note: "C2", durationBeats: 1 }] },
    { waveform: "square", instrument: "snare", volume: 0.2, pan: 0, notes: [{ note: "C2", durationBeats: 1 }] },
    { waveform: "square", instrument: "hihat", volume: 0.1, pan: 0.3, notes: [{ note: "C2", durationBeats: 1 }] },
    { waveform: "square", instrument: "tom", volume: 0.1, pan: 0, notes: [{ note: "C2", durationBeats: 1 }] },
    { waveform: "sawtooth", instrument: "bass", volume: 0.2, pan: 0, notes: [{ note: "A1", durationBeats: 1 }] },
  ],
};

const bytesOf = (m: Uint8Array): string => Array.from(m).map((b) => b.toString(16).padStart(2, "0")).join(" ");

describe("ドラムを太鼓ごとのチャンネルに分ける（内部の再生用）", () => {
  it("分けないときは、これまでどおり全部チャンネル10（9）で、役割の一覧は空", () => {
    const r = scoreToMidiInfo(score);
    expect(r.drums).toEqual({});
    expect(bytesOf(r.midi)).not.toContain("f0 0a 41 10 42 12");
  });
  it("分けると、キック15・スネア14・ハイハット13・タム/シンバル12のドラムパートになり、ベースはそれ以外のチャンネルを使う", () => {
    const r = scoreToMidiInfo(score, { splitDrums: true });
    expect(r.drums).toEqual({ 15: "kick", 14: "snare", 13: "hat", 12: "cym" });
    expect(Object.keys(r.programs).map(Number).every((c) => c !== 9 && c < 12)).toBe(true);
  });
  it("GSの『このチャンネルをドラムにする』SysEx（チェックサム付き）が入っている。チャンネル12の値は 40 1C 15 01 → チェックサム 0E", () => {
    const hex = bytesOf(scoreToMidiInfo(score, { splitDrums: true }).midi);
    expect(hex).toContain("f0 0a 41 10 42 12 40 1c 15 01 0e f7");
  });
  it("書き出す .mid（scoreToMidi）は、GM機器でも鳴るようSysExを含まない", async () => {
    const { scoreToMidi } = await import("./midi-export");
    expect(bytesOf(scoreToMidi(score))).not.toContain("41 10 42 12");
  });
});

describe("曲ごとの音量補正", () => {
  it("trimGain は dB を倍率にし、-12〜+6dB に収め、おかしな値は1にする", async () => {
    const { trimGain } = await import("./score");
    expect(trimGain(undefined)).toBe(1);
    expect(trimGain(NaN)).toBe(1);
    expect(trimGain(0)).toBe(1);
    expect(trimGain(-6)).toBeCloseTo(0.501, 2);
    expect(trimGain(-99)).toBeCloseTo(0.251, 2);
    expect(trimGain(99)).toBeCloseTo(1.995, 2);
  });
  it("AIソングの trimDb は曲に渡り、範囲に収まる", async () => {
    const { aiSongToScore } = await import("./ai-song");
    const b = { title: "t", description: "", bpm: 120, beats: 4, chords: "Am", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock", parts: [{ instrument: "kick", role: "k", volume: 0.2, pan: 0, amp: "auto", notes: "x:1" }] };
    expect(aiSongToScore({ ...b, trimDb: -5 } as never).score.trimDb).toBe(-5);
    expect(aiSongToScore({ ...b, trimDb: -50 } as never).score.trimDb).toBe(-12);
    expect(aiSongToScore(b as never).score.trimDb).toBeUndefined();
  });
});
