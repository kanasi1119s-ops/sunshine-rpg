import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import type { Section } from "./arrangement";
import { barChordsOf, checkLoop, checkScoreSeam, chordRootPc, seamRelation, type LoopCheckInput } from "./loop-check";
import type { Score } from "./score";

const S = (kind: Section["kind"], bars: number): Section => ({ kind, bars });
const input = (extra: Partial<LoopCheckInput> = {}): LoopCheckInput => ({
  loop: true, bpm: 120, beatsPerBar: 4, totalBars: 32,
  barChords: barChordsOf("C Am F G", 1, 8),
  sections: [S("verse", 8), S("interlude", 8), S("verse", 8), S("bridge", 8)],
  ...extra,
});

describe("checkLoop", () => {
  it("loop を書いていない曲は何も言わない", () => {
    expect(checkLoop(input({ loop: undefined }))).toEqual([]);
    expect(checkLoop(input({ loop: false }))).toEqual([]);
  });

  it("よくできたループは警告なし", () => {
    const w = checkLoop(input({ energy: [4, 3, 4, 3], parts: [{ notes: "C5:1 D5:1 E5:2 G5:4 R:4 A5:4" }] }));
    expect(w.filter((x) => !x.includes("同じ8小節"))).toEqual([]);
  });

  it("①最後と最初の強さが3段以上ちがう", () => {
    const w = checkLoop(input({ energy: [3, 5, 7, 9] }));
    expect(w.some((x) => x.includes("段階ちがい"))).toBe(true);
    expect(checkLoop(input({ energy: [4, 5, 6, 5] })).some((x) => x.includes("段階ちがい"))).toBe(false);
  });

  it("②最後のコードが頭につながらない（loopTail があれば言わない）", () => {
    const bad = checkLoop(input({ barChords: barChordsOf("C Am F D", 1, 8) }));
    expect(bad.some((x) => x.includes("つながりにくい") && x.includes("32小節目"))).toBe(true);
    expect(checkLoop(input({ barChords: barChordsOf("C Am F G", 1, 8) })).some((x) => x.includes("つながりにくい"))).toBe(false); // V
    expect(checkLoop(input({ barChords: barChordsOf("C Am F C", 1, 8) })).some((x) => x.includes("つながりにくい"))).toBe(false);
    expect(checkLoop(input({ barChords: barChordsOf("C Am F D", 1, 8), loopTail: "dominant" })).some((x) => x.includes("つながりにくい"))).toBe(false);
  });

  it("③tag（長音）や break で終わる", () => {
    expect(checkLoop(input({ sections: [S("verse", 8), S("chorus", 8), S("tag", 8)], totalBars: 24 })).some((x) => x.includes("余韻"))).toBe(true);
    expect(checkLoop(input({ sections: [S("verse", 8), S("chorus", 8), S("break", 8)], totalBars: 24 })).some((x) => x.includes("break"))).toBe(true);
  });

  it("④8の倍数でない（4の倍数でもない場合は強い注意）", () => {
    expect(checkLoop(input({ totalBars: 30, sections: undefined })).some((x) => x.includes("4の倍数ではありません"))).toBe(true);
    expect(checkLoop(input({ totalBars: 28, sections: undefined })).some((x) => x.includes("8の倍数ではありません"))).toBe(true);
    expect(checkLoop(input({ totalBars: 32, sections: undefined })).some((x) => x.includes("の倍数"))).toBe(false);
  });

  it("⑤同じ8小節ブロックが半分以上（ループの中のループ）", () => {
    const w = checkLoop(input({ sections: undefined, parts: [{ notes: "C5:4 E5:4 G5:8" }] }));
    expect(w.some((x) => x.includes("まったく同じ8小節"))).toBe(true);
    // 旋律が32小節ぶん変化していれば言わない
    const toks: string[] = [];
    for (let i = 0; i < 32; i++) toks.push(`${["C", "D", "E", "F", "G", "A", "B"][i % 7]}${4 + (i % 3)}:4`);
    expect(checkLoop(input({ sections: undefined, barChords: barChordsOf("C Am F G Dm Em Bb A", 1, 4), parts: [{ notes: toks.join(" ") }] })).some((x) => x.includes("まったく同じ8小節"))).toBe(false);
  });

  it("⑥1周の秒数が scene の目安の外", () => {
    const w = checkLoop(input({ scene: "battle", bpm: 100 })); // 32小節×4拍÷100bpm＝76.8秒
    expect(w.some((x) => x.includes("目安"))).toBe(true);
    expect(checkLoop(input({ scene: "battle", bpm: 190, totalBars: 16, sections: undefined })).some((x) => x.includes("目安"))).toBe(false);
    expect(checkLoop(input({ scene: "fanfare" })).some((x) => x.includes("ループさせない"))).toBe(true);
  });

  it("{startBar,endBar} の範囲が不正なら注意", () => {
    expect(checkLoop(input({ loop: { startBar: 9, endBar: 4 } })).some((x) => x.includes("startBar"))).toBe(true);
    expect(checkLoop(input({ loop: { startBar: 5, endBar: 32 }, sections: undefined, totalBars: 32 })).some((x) => x.includes("startBar は1以上"))).toBe(false);
  });

  it("コードの根音と継ぎ目の関係", () => {
    expect(chordRootPc("F#m7/C#")).toBe(6);
    expect(chordRootPc("Bb")).toBe(10);
    expect(seamRelation(7, 0)).toBe("V");
    expect(seamRelation(5, 0)).toBe("IV");
    expect(seamRelation(10, 0)).toBe("bVII");
    expect(seamRelation(2, 0)).toBeNull();
  });
});

describe("checkLoop を曲の組み立てから呼ぶ", () => {
  const song = (extra: Record<string, unknown>): AiSong => ({
    title: "t", description: "d", bpm: 100, beats: 4, chords: "C Am F D", barsPerChord: 1, repeats: 8, autoAccompaniment: true, feel: "pop", tone: "rock",
    parts: [{ instrument: "lead", role: "メロディ", volume: 0.25, pan: 0, amp: "auto", notes: "C5:4" }], ...extra,
  } as AiSong);

  it("loop を書いた曲だけ警告が出る", () => {
    expect(aiSongToScore(song({})).warnings.some((w) => w.startsWith("loop:"))).toBe(false);
    const w = aiSongToScore(song({ loop: true })).warnings.filter((x) => x.startsWith("loop:"));
    expect(w.some((x) => x.includes("つながりにくい"))).toBe(true);
  });

  it("loopTail を付ければ継ぎ目の注意が消える", () => {
    const w = aiSongToScore(song({ loop: true, loopTail: "dominant" })).warnings.filter((x) => x.startsWith("loop:"));
    expect(w.some((x) => x.includes("つながりにくい"))).toBe(false);
  });
});

const note = (n: string, d: number, extra = {}) => ({ note: n, durationBeats: d, ...extra });
const scoreOf = (bars: number, build: (bar: number) => Score["tracks"][number]["notes"], opts: Partial<Score> = {}): Score => ({
  tempoBpm: 120, loop: true,
  tracks: [
    { waveform: "sawtooth", instrument: "bass", volume: 0.3, notes: Array.from({ length: bars }, (_, b) => build(b)).flat() },
  ], ...opts,
});

describe("checkScoreSeam", () => {
  it("ループでない曲は検査しない", () => {
    expect(checkScoreSeam(scoreOf(8, () => [note("C2", 4)], { loop: false }))).toEqual([]);
  });

  it("最後の低音が頭の V なら問題なし、遠い音なら注意", () => {
    const ok = scoreOf(8, (b) => [note(b === 7 ? "G2" : "C2", 4)]);
    expect(checkScoreSeam(ok).some((x) => x.includes("低音"))).toBe(false);
    const bad = scoreOf(8, (b) => [note(b === 7 ? "D2" : "C2", 4)]);
    expect(checkScoreSeam(bad).some((x) => x.includes("低音"))).toBe(true);
  });

  it("末尾の山を見つける", () => {
    const s = scoreOf(16, (b) => (b >= 14 ? [note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5)].slice(0, 8).concat([note("C2", 0)]).filter((n) => n.durationBeats > 0) : [note("C2", 4)]));
    expect(checkScoreSeam(s).some((x) => x.includes("最後の1〜2小節"))).toBe(true);
  });

  it("静かな曲の頭の一撃（opening: true なら言わない）", () => {
    const loudHead = (b: number) => (b === 0 ? [note("C2", 1), note("C2", 1), note("C2", 1), note("C2", 1), note("C2", 1), note("C2", 1), note("C2", 1), note("C2", 1)].map((n) => ({ ...n, durationBeats: 0.5 })) : [note("C2", 4)]);
    expect(checkScoreSeam(scoreOf(16, loudHead)).some((x) => x.includes("頭の小節"))).toBe(true);
    expect(checkScoreSeam(scoreOf(16, loudHead, { opening: true })).some((x) => x.includes("頭の小節"))).toBe(false);
  });

  it("末尾の長い音が頭の音と半音・増4度でぶつかる", () => {
    const mk = (last: string): Score => ({ tempoBpm: 120, loop: true, tracks: [{ waveform: "sine", instrument: "pad", volume: 0.2, notes: [note("C4", 4), note("D4", 4), note("E4", 4), note(last, 4)] }] });
    expect(checkScoreSeam(mk("B3")).some((x) => x.includes("ぶつかります"))).toBe(true); // 半音
    expect(checkScoreSeam(mk("F#4")).some((x) => x.includes("増4度"))).toBe(true);
    expect(checkScoreSeam(mk("G4")).some((x) => x.includes("ぶつかります"))).toBe(false);
    expect(checkScoreSeam(mk("C4")).some((x) => x.includes("ぶつかります"))).toBe(false);
  });
});
