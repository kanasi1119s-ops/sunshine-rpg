import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { noteNameToMidi } from "./note";
import { applyTransforms, baseSteps, checkLedger, getMotif, ledgerMarkdown, MOTIF_IDS, MOTIFS, motifToNotes, motifUses, parseDegree, spliceNotes } from "./motif";
import { expandMotifs, guessKey, totalBarsOf } from "./song-expand";

const midis = (tokens: string[]): number[] => tokens.filter((t) => !t.startsWith("R")).map((t) => noteNameToMidi(t.split(":")[0]));
const beatsOf = (tokens: string[]): number => tokens.reduce((a, t) => a + Number(t.split(":")[1]), 0);

describe("度数の読み方", () => {
  it("1〜7・b/#・オクターブ記号・休み", () => {
    expect(parseDegree("1")).toEqual({ idx: 0, alt: 0 });
    expect(parseDegree("b3")).toEqual({ idx: 2, alt: -1 });
    expect(parseDegree("#4")).toEqual({ idx: 3, alt: 1 });
    expect(parseDegree("5,")).toEqual({ idx: 4 - 7, alt: 0 });
    expect(parseDegree("1'")).toEqual({ idx: 7, alt: 0 });
    expect(parseDegree("R")).toEqual({ idx: null, alt: 0 });
    expect(parseDegree("8")).toBeNull();
  });
});

describe("台帳 motifs.json", () => {
  it("5つの主題があり、ID・度数・リズムの数がそろう", () => {
    expect(MOTIF_IDS).toEqual(["akari", "yugami", "wa", "kazoku", "daihyo"]);
    for (const m of MOTIFS) {
      expect(m.degrees.length, m.id).toBe(m.rhythm.length);
      expect(() => baseSteps(m), m.id).not.toThrow();
      expect(m.degrees.length, m.id).toBeGreaterThanOrEqual(2);
      expect(m.degrees.length, m.id).toBeLessThanOrEqual(7); // 動機は短い
    }
  });
  it("歪みの動機は灯の動機の音を半音ずらした形（骨組みが近い）", () => {
    const a = midis(motifToNotes("akari", { key: "C", octave: 4 }).tokens);
    const y = midis(motifToNotes("yugami", { key: "C", octave: 4 }).tokens);
    const diffs = a.map((x, i) => Math.abs(x - y[i]));
    expect(diffs.filter((d) => d > 0).length).toBeGreaterThanOrEqual(1);
    expect(Math.max(...diffs)).toBeLessThanOrEqual(3);
  });
});

describe("度数 → 音名", () => {
  it("C4 の灯の動機は C4 D4 E4 A4（長音階の1 2 3 6）", () => {
    const { tokens, beats } = motifToNotes("akari", { key: "C", octave: 4 });
    expect(tokens).toEqual(["C4:0.5", "D4:0.5", "E4:1", "A4:2"]);
    expect(beats).toBe(4);
  });
  it("調を替えると平行移動（Bb でも同じ輪郭）", () => {
    const c = midis(motifToNotes("akari", { key: "C", octave: 4 }).tokens);
    const bb = midis(motifToNotes("akari", { key: "Bb", octave: 4 }).tokens);
    expect(bb.map((m, i) => m - c[i])).toEqual([10, 10, 10, 10]); // Bb4 は C4 の10半音上（輪郭は同じ）
    expect(motifToNotes("akari", { key: "F#", octave: 3 }).tokens[0]).toBe("F#3:0.5");
  });
  it("短調の曲では 3・6・7度が半音下がる", () => {
    expect(motifToNotes("akari", { key: "A", octave: 4, mode: "minor" }).tokens).toEqual(["A4:0.5", "B4:0.5", "C5:1", "F5:2"]);
  });
  it("オクターブ記号と休み", () => {
    const t = motifToNotes("kazoku", { key: "C", octave: 4 }).tokens;
    expect(t[3]).toBe("B3:1");
  });
  it("台帳にない主題・読めない key はエラー", () => {
    expect(() => motifToNotes("nothing")).toThrow(/台帳/);
    expect(() => motifToNotes("akari", { key: "H" })).toThrow(/key/);
  });
});

describe("変形", () => {
  const base = baseSteps(getMotif("akari")!);
  const total = (s: typeof base): number => s.reduce((a, x) => a + x.beats, 0);
  it("augment／diminish は合計拍が2倍／半分", () => {
    expect(total(applyTransforms(base, ["augment"]))).toBe(total(base) * 2);
    expect(total(applyTransforms(base, ["diminish"]))).toBe(total(base) / 2);
    expect(motifToNotes("akari", { transform: ["diminish"] }).beats).toBe(2);
  });
  it("invert は最初の音を軸に上下を逆にする", () => {
    const m = midis(motifToNotes("akari", { key: "C", octave: 5, transform: ["invert"] }).tokens);
    expect(m[0]).toBe(noteNameToMidi("C5"));
    expect(m.slice(1).every((x) => x < m[0])).toBe(true);
  });
  it("retrograde は逆行、head／tail は前半／後半", () => {
    expect(midis(motifToNotes("akari", { key: "C", transform: ["retrograde"] }).tokens)).toEqual(midis(motifToNotes("akari", { key: "C" }).tokens).reverse());
    expect(motifToNotes("akari", { transform: ["head"] }).tokens).toHaveLength(2);
    expect(motifToNotes("akari", { transform: ["tail"] }).tokens).toHaveLength(2);
    expect(motifToNotes("akari", { transform: ["head:3"] }).tokens).toHaveLength(3);
  });
  it("transpose は度数、octave は8度", () => {
    const base0 = midis(motifToNotes("akari", { key: "C", octave: 4 }).tokens);
    expect(midis(motifToNotes("akari", { key: "C", octave: 4, transform: ["octave:1"] }).tokens)).toEqual(base0.map((x) => x + 12));
    expect(midis(motifToNotes("akari", { key: "C", octave: 4, transform: ["transpose:2"] }).tokens)[0]).toBe(noteNameToMidi("E4"));
  });
  it("mode:minor で短調化、mode:major で戻す", () => {
    expect(motifToNotes("akari", { key: "C", octave: 4, transform: ["mode:minor"] }).tokens[2]).toBe("D#4:1");
    expect(motifToNotes("akari", { key: "C", octave: 4, transform: ["mode:minor", "mode:major"] }).tokens[2]).toBe("E4:1");
  });
  it("変形はつなげられ、使えない変形は注意", () => {
    const w: string[] = [];
    const out = applyTransforms(base, ["diminish", "head:2", "foo"], w);
    expect(out).toHaveLength(2);
    expect(total(out)).toBe(0.5);
    expect(w.join()).toContain("foo");
  });
  it("音域の外に出る音は休みにして注意", () => {
    const w: string[] = [];
    const t = motifToNotes("akari", { key: "C", octave: 9 }, w);
    expect(t.tokens.every((x) => x.startsWith("R"))).toBe(true);
    expect(w.length).toBeGreaterThan(0);
  });
});

describe("spliceNotes（手書きの音の並びに差し込む）", () => {
  it("合計の拍が変わらず、差し込んだ位置に主題が入る", () => {
    const out = spliceNotes("C3:4", 16, 8, ["E5:1", "G5:1"], 2).split(" ");
    expect(beatsOf(out)).toBe(16);
    expect(out).toEqual(["C3:4", "C3:4", "E5:1", "G5:1", "C3:4", "C3:4"].slice(0, 2).concat(["E5:1", "G5:1", "R:2", "C3:4"]).filter(Boolean) as string[]);
  });
  it("またぐ音は切り詰める／休みにする", () => {
    const out = spliceNotes("C4:8", 8, 2, ["E5:2"], 2).split(" ");
    expect(out).toEqual(["C4:2", "E5:2", "R:4"]);
    expect(beatsOf(out)).toBe(8);
  });
  it("空の notes は休みで埋める", () => {
    const out = spliceNotes("", 8, 4, ["E5:2"], 2).split(" ");
    expect(out).toEqual(["R:4", "E5:2", "R:2"]);
  });
  it("奏法の記号を保つ", () => {
    expect(spliceNotes("C4:8!", 8, 2, ["E5:2"], 2).split(" ")[0]).toBe("C4:2!");
  });
});

describe("曲への差し込み（parts[].motif）", () => {
  const song = (parts: unknown[], extra: Record<string, unknown> = {}): AiSong => ({
    title: "t", description: "d", bpm: 100, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 6, autoAccompaniment: true, feel: "pop", tone: "rock",
    parts, ...extra,
  } as AiSong);
  const lead = (motif: unknown): unknown => ({ instrument: "lead", role: "メロディ", volume: 0.25, pan: 0, amp: "auto", notes: "R:96", motif });

  it("key は最初のコードから推測する", () => {
    expect(guessKey("Am F C G")).toEqual({ key: "A", mode: "minor" });
    expect(guessKey("Bb7 Eb")).toEqual({ key: "Bb", mode: "major" });
    expect(totalBarsOf({ chords: "C Am F G", barsPerChord: 1, repeats: 6 })).toBe(24);
  });

  it("at: 小節番号で、その小節の頭に置く", () => {
    const w: string[] = [];
    const out = expandMotifs({ ...song([lead({ id: "akari", at: 9 })]) } as AiSong, w);
    const notes = String((out.parts[0] as { notes: string }).notes).split(" ");
    expect(beatsOf(notes)).toBe(96);
    expect(notes.slice(0, 2)).toEqual(["R:32", "C5:0.5"]);
    expect(out.motifs).toEqual(["akari"]);
    expect(w).toEqual([]);
  });

  it("at: セクション名（sections／scene が必要）。chorus2 で2つ目", () => {
    const sections = [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }];
    const out = expandMotifs(song([lead({ id: "akari", at: "chorus2", transform: ["diminish"] })], { sections }) as AiSong);
    const notes = String((out.parts[0] as { notes: string }).notes).split(" ");
    expect(notes.slice(0, 3)).toEqual(["R:32", "R:32", "R:16"]); // 20小節 × 4拍＝80拍
    expect(notes[3]).toBe("C5:0.25");
  });

  it("sections がないのに kind を指定すると注意", () => {
    const w: string[] = [];
    expandMotifs(song([lead({ id: "akari", at: "chorus" })]) as AiSong, w);
    expect(w.join()).toContain("sections");
  });

  it("repeat と fill、台帳にない主題は注意", () => {
    const w: string[] = [];
    const out = expandMotifs(song([lead([{ id: "akari", at: 1, repeat: 2 }, { id: "nothing", at: 5 }])]) as AiSong, w);
    const notes = String((out.parts[0] as { notes: string }).notes).split(" ");
    expect(notes.slice(0, 8).filter((t) => t.startsWith("C5")).length).toBe(2);
    expect(w.join()).toContain("nothing");
    const filled = expandMotifs(song([lead({ id: "wa", at: 1, fill: true })], { sections: [{ kind: "verse", bars: 24 }] }) as AiSong);
    expect(beatsOf(String((filled.parts[0] as { notes: string }).notes).split(" "))).toBe(96);
  });

  it("ドラムには置けない", () => {
    const w: string[] = [];
    expandMotifs(song([{ instrument: "kick", role: "k", volume: 0.2, pan: 0, notes: "x:1", motif: { id: "akari", at: 1 } }]) as AiSong, w);
    expect(w.join()).toContain("ドラム");
  });

  it("aiSongToScore まで通り、Score.meta.motifs に残る。modulate と併用できる", () => {
    const { score, warnings } = aiSongToScore(song([lead({ id: "akari", at: 1, repeat: 4 })], { modulate: { atBar: 13, semitones: 2 } }));
    expect(score.meta?.motifs).toEqual(["akari"]);
    expect(warnings.filter((x) => x.includes("主題"))).toEqual([]);
    const l = score.tracks.find((t) => t.instrument === "lead")!;
    expect(l.notes[0].note).toBe("C5");
  });
});

describe("使用一覧と台帳の食い違い", () => {
  const songs = [
    { name: "a", uses: motifUses({ parts: [{ motif: { id: "akari", transform: ["diminish"] } }], motifs: ["wa"] }) },
    { name: "b", uses: motifUses({ parts: [{ motif: [{ id: "akari", transform: ["diminish"] }] }] }) },
    { name: "c", uses: [] },
    { name: "d", uses: [] },
  ];
  it("parts[].motif（単体・配列）と motifs を集める", () => {
    expect(songs[0].uses.map((u) => u.id)).toEqual(["akari", "wa"]);
    expect(songs[1].uses).toHaveLength(1);
  });
  it("未使用の主題・断片がある曲が少ない・同じ変形の連続、を警告する", () => {
    const w = checkLedger(songs).join("\n");
    expect(w).toContain("yugami");
    expect(w).toContain("同じ変形");
  });
  it("断片のある曲が半分未満なら警告", () => {
    const few = [songs[0], { name: "x", uses: [] }, { name: "y", uses: [] }, { name: "z", uses: [] }, { name: "u", uses: [] }];
    expect(checkLedger(few).join()).toContain("1/5");
  });
  it("台帳にないIDを使うと警告", () => {
    expect(checkLedger([{ name: "x", uses: [{ id: "zzz", transform: [] }] }]).join()).toContain("zzz");
  });
  it("ledgerMarkdown に表と注意が出る", () => {
    const md = ledgerMarkdown(songs);
    expect(md).toContain("| akari（灯（あかり）の動機）");
    expect(md).toContain("a（diminish）");
    expect(md).toContain("## 注意");
  });
});
