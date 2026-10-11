import { describe, expect, it } from "vitest";
import { aiSongToScore, AI_SONG_SCHEMA } from "./ai-song";
import { accentOnGroupHeads, applyGroupingToDrums, beatsOk, defaultGrouping, groupingBar, groupStarts, parseGrouping } from "./meter";
import { scoreToMidi } from "./midi-export";
import { REST, type Track } from "./score";
import { readMidi, ROCK_SONG } from "./rhythm-fixtures";

const total = (t: Track): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const song = (beats: number, extra: Record<string, unknown> = {}): Record<string, unknown> => ({
  ...ROCK_SONG, beats, chords: "Am F C G", repeats: 2, autoAccompaniment: true, feel: "rock", human: undefined, swing: undefined, ...extra,
  parts: [{ instrument: "lead", role: "l", volume: 0.2, pan: 0, amp: "auto", notes: `C5:${beats}` }],
});

describe("拍子の拡張（提案6）", () => {
  it("beats は 2〜12 の整数（5・9・11・12拍子もつくれる）。範囲外はエラー", () => {
    for (const b of [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) {
      expect(beatsOk(b)).toBe(true);
      const { score } = aiSongToScore(song(b));
      expect(score.timeSig).toEqual(b === 4 ? undefined : { num: b, den: 4 });
      for (const t of score.tracks) expect(total(t)).toBeCloseTo(b * 8, 6); // 4コード×2回＝8小節
    }
    for (const b of [1, 13, 4.5, "x"]) expect(() => aiSongToScore(song(b as number))).toThrow(/beats/);
    expect(AI_SONG_SCHEMA.properties.beats.enum).toEqual([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
  });
  it("MIDI の拍子記号に 5/4・9/4・12/4 が書かれる", () => {
    for (const b of [5, 9, 12]) {
      const bytes = scoreToMidi(aiSongToScore(song(b)).score);
      let found = false;
      for (let i = 0; i < bytes.length - 6; i++) if (bytes[i] === 0xff && bytes[i + 1] === 0x58 && bytes[i + 2] === 4) { expect(bytes[i + 3]).toBe(b); found = true; break; }
      expect(found).toBe(true);
    }
  });
  it("既定のまとまり: 5＝3+2、7＝2+2+3、9＝3+3+3、11＝3+3+3+2。合計は beats", () => {
    expect(defaultGrouping(5)).toEqual([3, 2]);
    expect(defaultGrouping(7)).toEqual([2, 2, 3]);
    expect(defaultGrouping(9)).toEqual([3, 3, 3]);
    expect(defaultGrouping(11)).toEqual([3, 3, 3, 2]);
    for (let b = 2; b <= 12; b++) expect(defaultGrouping(b).reduce((s, x) => s + x, 0)).toBe(b);
    expect(groupStarts([2, 2, 3])).toEqual([0, 2, 4]);
  });
  it("parseGrouping: auto・配列・合計がちがう・読めない", () => {
    const w: string[] = [];
    expect(parseGrouping("auto", 7, w)).toEqual([2, 2, 3]);
    expect(parseGrouping([3, 2], 5, w)).toEqual([3, 2]);
    expect(parseGrouping(undefined, 5, w)).toBeNull();
    expect(w).toEqual([]);
    expect(parseGrouping([2, 2], 5, w)).toBeNull();
    expect(parseGrouping("x", 5, w)).toBeNull();
    expect(w.length).toBe(2);
  });
  it("まとまりに沿った1小節: キックは1つめ・3つめの頭、スネアは2つめの頭、ハットはまとまりの頭が強い", () => {
    const bar = groupingBar([2, 2, 3], 7);
    const on = (ns: { note: string }[]): number[] => ns.flatMap((n, i) => (n.note === REST ? [] : [i / 2]));
    expect(on(bar.kick)).toEqual([0, 4]);
    expect(on(bar.snare)).toEqual([2]);
    expect(on(bar.hihat).length).toBe(14);
    const heads = [0, 2, 4].map((b) => bar.hihat[b * 2].velocity);
    expect(heads).toEqual([1.3, 1.3, 1.3]);
    expect(bar.hihat[1].velocity).toBe(0.7);
    expect(bar.kick.reduce((s, n) => s + n.durationBeats, 0)).toBe(7);
  });
  it("applyGroupingToDrums: 長さはそのまま、kick・snare・hihat 以外は変えない", () => {
    const tracks: Track[] = [
      { waveform: "square", instrument: "kick", volume: 0.2, notes: [{ note: "C2", durationBeats: 14 }] },
      { waveform: "square", instrument: "bass", volume: 0.2, notes: [{ note: "C2", durationBeats: 14 }] },
    ];
    const out = applyGroupingToDrums(tracks, [2, 2, 3], 7);
    expect(total(out[0])).toBe(14);
    expect(out[0].notes.length).toBe(28);
    expect(out[1]).toBe(tracks[1]);
  });
  it("AIソング: grouping を書くと、自動伴奏のドラムが 2+2+3 の頭に鳴る（MIDIで確認）", () => {
    const withG = aiSongToScore(song(7, { grouping: [2, 2, 3], human: undefined }));
    const m = readMidi(scoreToMidi(withG.score));
    const kickBeats = m.notes.filter((n) => n.ch === 9 && n.pitch === 36).map((n) => Math.round(n.tick / 480)).slice(0, 4);
    expect(kickBeats).toEqual([0, 4, 7, 11]);
    const hat = withG.score.tracks.find((t) => t.instrument === "hihat")!;
    expect(accentOnGroupHeads(hat.notes, [2, 2, 3], 7)).toBe(1);
    // 書かなければ今までの自動伴奏
    const without = aiSongToScore(song(7));
    expect(JSON.stringify(without.score.tracks)).not.toBe(JSON.stringify(withG.score.tracks));
  });
  it("grouping の合計が beats と違うときは警告して使わない", () => {
    const { warnings } = aiSongToScore(song(5, { grouping: [2, 2] }));
    expect(warnings.some((w) => w.includes("合計"))).toBe(true);
  });
  it("5/4 の自動伴奏（grouping auto）は 3+2: スネアは3拍目の頭", () => {
    const { score } = aiSongToScore(song(5, { grouping: "auto" }));
    const m = readMidi(scoreToMidi(score));
    const snare = m.notes.filter((n) => n.ch === 9 && (n.pitch === 38 || n.pitch === 40 || n.pitch === 39 || n.pitch === 37)).map((n) => Math.round(n.tick / 480));
    expect([...new Set(snare)].slice(0, 2)).toEqual([3, 8]);
  });
});
