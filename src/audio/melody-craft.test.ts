// 旋律の点検（P1〜P6・P11）・動機変形（P7）・旋律の型ライブラリ（P9）・音程列の類似（P10）・ガイド追記（P8・P12）のテスト。
// 対象は tools/ の .mjs（型定義がないので import に @ts-ignore を付ける）。
import { describe, expect, it } from "vitest";
// @ts-ignore
import fs from "node:fs";
// @ts-ignore
import path from "node:path";
// @ts-ignore
import os from "node:os";
import aiSongSrc from "./ai-song.ts?raw";
import workflowMd from "../../docs/sound/ai-composition-workflow.md?raw";
// @ts-ignore
import { parseNotes } from "../../tools/audio-check/score-lib.mjs";
// @ts-ignore
import * as ml from "../../tools/audio-check/melody-lint.mjs";
// @ts-ignore
import * as mo from "../../tools/composer/motif-ops.mjs";
// @ts-ignore
import * as mp from "../../tools/composer/melody-patterns.mjs";
// @ts-ignore
import * as is from "../../tools/composer/interval-sim.mjs";

const seqOf = (s: string) => parseNotes(s).notes.filter((n: { rest: boolean }) => !n.rest);
const rep = (s: string, n: number) => Array(n).fill(s).join(" ");

describe("P1 頂点の点検", () => {
  it("区切りの中で最高音が2回なら警告", () => {
    const seq = seqOf("C5:1 E5:1 G5:1 E5:1 C5:1 G5:1 E5:1 C5:1 ".repeat(1) + rep("C5:1", 8));
    expect(ml.checkPeaks(seq, 4, 4).level).toBe("warn");
  });
  it("最高音が区切りの前25%にあると警告", () => {
    const seq = seqOf("A5:1 G5:1 E5:1 C5:1 A4:1 G4:1 E4:1 C4:1");
    const r = ml.checkPeaks(seq, 4, 2);
    expect(r.level).toBe("warn");
    expect(r.msg).toContain("前");
  });
  it("後ろ3分の1に1回だけなら OK", () => {
    const seq = seqOf("C5:1 D5:1 E5:1 G5:1 C5:1 D5:1 E5:1 D5:1");
    expect(ml.checkPeaks(seq, 4, 2).level).toBe("ok");
  });
});

describe("P2 同音の再訪・連打", () => {
  it("同じ高さが4割超なら警告", () => {
    const seq = seqOf("C5:1 C5:1 D5:1 C5:1 C5:1 E5:1 C5:1 G5:1");
    expect(ml.checkRepeatedPitch(seq, 4, 2).level).toBe("warn");
  });
  it("4回以上の連続で警告", () => {
    const seq = seqOf("C5:0.5 C5:0.5 C5:0.5 C5:0.5 D5:1 E5:1 F5:1 G5:1 A5:1 B5:1");
    expect(ml.checkRepeatedPitch(seq, 4, 3).msg).toContain("4回以上");
  });
  it("ばらけていれば OK", () => {
    const seq = seqOf("C5:1 D5:1 E5:1 G5:1 A5:1 G5:1 E5:1 D5:1");
    expect(ml.checkRepeatedPitch(seq, 4, 2).level).toBe("ok");
  });
  it("リフ役は点検の対象外", () => {
    expect(ml.isRiffRole("ギターのリフ")).toBe(true);
    expect(ml.isRiffRole("メロディ")).toBe(false);
  });
});

describe("P3 リズム型の点検", () => {
  it("4小節以上ぜんぶ同じリズム型なら警告", () => {
    const seq = seqOf(rep("C5:1 D5:1 E5:1 G5:1", 5));
    expect(ml.checkRhythmTypes(seq, 4, 5).some((r: { level: string }) => r.level === "warn")).toBe(true);
  });
  it("8小節に型が7種以上あると警告", () => {
    const bars = ["C5:4", "C5:2 D5:2", "C5:1 D5:3", "C5:3 D5:1", "C5:1 D5:1 E5:2", "C5:2 D5:1 E5:1", "C5:1 D5:2 E5:1", "C5:0.5 D5:0.5 E5:3"];
    const seq = seqOf(bars.join(" "));
    expect(ml.checkRhythmTypes(seq, 4, 8).some((r: { level: string }) => r.level === "warn")).toBe(true);
  });
  it("2〜3種を使い回していれば OK。拍頭だけの旋律は参考表示", () => {
    const a = "C5:2 D5:1 E5:1", b = "E5:1 D5:1 C5:2";
    const seq = seqOf([a, b, a, b].join(" "));
    const r = ml.checkRhythmTypes(seq, 4, 4);
    expect(r[0].level).toBe("ok");
    expect(r.some((x: { level: string }) => x.level === "info")).toBe(true);
  });
});

describe("P4 息の点検", () => {
  it("休符も2拍以上の音もなく6秒を超えると警告", () => {
    const seq = seqOf(rep("C5:1 D5:1 E5:1 G5:1", 4)); // bpm 120 で 8秒
    expect(ml.checkBreath(seq, 4, 120, 4).level).toBe("warn");
  });
  it("2拍以上の音が間にあれば OK", () => {
    const seq = seqOf("C5:1 D5:1 E5:1 G5:1 C5:3 D5:1 E5:1 G5:1 E5:1 D5:1 C5:2 R:2");
    expect(ml.checkBreath(seq, 4, 120, 4).level).toBe("ok");
  });
  it("バラードは4秒で警告する", () => {
    expect(ml.breathSeconds({ title: "夜のバラード" })).toBe(4);
    expect(ml.breathSeconds({ title: "戦闘" })).toBe(6);
    const seq = seqOf("C5:1 D5:1 E5:1 G5:1 C5:1 D5:1 E5:1 G5:1 C5:2 D5:2 E5:2 G5:2"); // bpm 120 で 4拍=2秒。8拍=4秒超
    expect(ml.checkBreath(seq, 4, 120, 3, 4).level).toBe("ok");
    const long = seqOf("C5:1 D5:1 E5:1 G5:1 C5:1 D5:1 E5:1 G5:1 C5:1 D5:1 E5:1 G5:1");
    expect(ml.checkBreath(long, 4, 120, 3, 4).level).toBe("warn");
  });
});

describe("P5 問いと答えの終わり方", () => {
  const body = (q: string, a: string) => `C5:1 D5:1 E5:1 F5:1 ${rep("D5:1 E5:1 F5:1 G5:1", 2)} ${q}:4 ${rep("D5:1 E5:1 F5:1 G5:1", 3)} ${a}:4`;
  it("前半と後半が同じ音で終わると警告", () => {
    expect(ml.checkAnswerEndings(seqOf(body("C5", "C5")), 4, 8).level).toBe("warn");
  });
  it("前半は開いた音、後半は主音なら OK", () => {
    expect(ml.checkAnswerEndings(seqOf(body("D5", "C5")), 4, 8).level).toBe("ok");
  });
  it("8小節未満は点検しない", () => {
    expect(ml.checkAnswerEndings(seqOf("C5:4 D5:4"), 4, 2).level).toBe("info");
  });
});

describe("P6 セクション間の音域差", () => {
  const plan = { sections: [{ name: "Aメロ", kind: "verse", bars: 2 }, { name: "サビ", kind: "chorus", bars: 2 }] };
  it("サビが Aメロより高ければ OK", () => {
    const seq = seqOf("C5:4 D5:4 G5:4 A5:4");
    expect(ml.checkSectionRange(seq, 4, plan)?.level).toBe("ok");
  });
  it("サビが Aメロと同じ高さなら警告", () => {
    const seq = seqOf("C5:4 D5:4 C5:4 D5:4");
    expect(ml.checkSectionRange(seq, 4, plan)?.level).toBe("warn");
  });
  it("設計図がなければ null", () => {
    expect(ml.checkSectionRange(seqOf("C5:4"), 4, null)).toBeNull();
  });
});

describe("P11 倚音・掛留の見える化", () => {
  it("強拍の和音外音が次で下へ解決すれば OK として数える", () => {
    const seq = seqOf("D5:1 C5:1 E5:2 F5:1 E5:3"); // C 和音: 1拍目 D5(外)→C5(構成音)、3拍目… 
    const r = ml.classifyStrongNonChord(seq, 4, ["C", "C"]);
    expect(r.ok.length).toBeGreaterThanOrEqual(1);
    expect(r.bad.length).toBe(0);
  });
  it("解決しない和音外音は要確認", () => {
    const seq = seqOf("D5:1 E5:3 D5:1 A5:3"); // 2小節目の D5 が上へ跳ぶ
    const r = ml.classifyStrongNonChord(seq, 4, ["C", "C"]);
    expect(r.bad.length).toBeGreaterThanOrEqual(1);
    expect(ml.checkAppoggiatura(seq, 4, ["C", "C"]).level).toBe("warn");
  });
});

describe("melodyLint（まとめ）", () => {
  it("旋律ごとに結果が出る", () => {
    const seq = seqOf(rep("C5:1 D5:1 E5:1 G5:1", 8));
    const res = ml.melodyLint({ beats: 4, bpm: 120 }, [{ role: "メロディ", seq }], { chords: Array(8).fill("C") });
    expect(res.length).toBeGreaterThan(5);
    expect(res.every((r: { msg: string }) => r.msg.startsWith("旋律「メロディ」"))).toBe(true);
  });
});

describe("P7 動機変形（motif-ops）", () => {
  const m = "E4:1 G4:0.5 A4:1.5 G4:1";
  it("移高: 音階内で2度ずらしても拍の合計が保たれる", () => {
    const out = mo.shiftDiatonic(m, 2, { tonic: "C", scale: "major" });
    expect(out).toBe("G4:1 B4:0.5 C5:1.5 B4:1");
    expect(mo.totalBeats(out)).toBe(mo.totalBeats(m));
  });
  it("半音の移高", () => {
    expect(mo.shiftSemitones(m, 2)).toBe("F#4:1 A4:0.5 B4:1.5 A4:1");
  });
  it("逆さ: 軸の音を中心に反転。音階を指定すると音階内に収まる", () => {
    expect(mo.invert(m, "E4")).toBe("E4:1 C#4:0.5 B3:1.5 C#4:1");
    const d = mo.invert(m, "E4", { tonic: "C", scale: "major" });
    expect(d).toBe("E4:1 C4:0.5 B3:1.5 C4:1");
    expect(mo.totalBeats(d)).toBe(4);
  });
  it("逆行: 音と長さが一緒に逆順になる。合計は同じ", () => {
    const r = mo.retrograde(m);
    expect(r).toBe("G4:1 A4:1.5 G4:0.5 E4:1");
    expect(mo.totalBeats(r)).toBe(mo.totalBeats(m));
  });
  it("拡大・縮小は合計が倍率になる", () => {
    expect(mo.totalBeats(mo.augment(m, 2))).toBe(8);
    expect(mo.totalBeats(mo.diminish(m, 2))).toBe(2);
  });
  it("断片化: 先頭 n 音。pad で合計を保つ", () => {
    expect(mo.fragment(m, 2)).toBe("E4:1 G4:0.5");
    const p = mo.fragment(m, 2, { pad: true });
    expect(p).toBe("E4:1 G4:0.5 R:2.5");
    expect(mo.totalBeats(p)).toBe(4);
  });
  it("間引き・装飾でも合計は変わらない", () => {
    expect(mo.totalBeats(mo.thin(m))).toBe(4);
    const o = mo.ornament(m, { tonic: "C", scale: "major", minDur: 1 });
    expect(mo.totalBeats(o)).toBe(4);
    expect(o.split(" ").length).toBeGreaterThan(m.split(" ").length);
  });
  it("休符とマーク（! など）を保つ。読めない音はエラー", () => {
    expect(mo.shiftSemitones("E4:1! R:1 G4:1,", 1)).toBe("F4:1! R:1 G#4:1,");
    expect(() => mo.parseMotif("X9:1")).toThrow();
  });
  it("CLI の入口", () => {
    expect(mo.runMotifCommand(["retro", "C4:1 D4:2"])).toBe("D4:2 C4:1");
    expect(mo.runMotifCommand(["shift", "C4:1", "--n", "1", "--tonic", "C"])).toBe("D4:1");
  });
});

describe("P8 AI_SONG_GUIDE に旋律の設計図", () => {
  it("短縮版が入っている", () => {
    const src = aiSongSrc;
    expect(src).toContain("旋律の設計図");
    expect(src).toContain("リズム型を2〜3種に絞る");
  });
});

describe("P9 旋律の型ライブラリ", () => {
  const patterns = mp.loadPatterns();
  it("見本38がすべて入っていて、拍の合計が小節数×拍子と合う", () => {
    expect(patterns.length).toBe(38);
    for (const p of patterns) {
      expect(parseNotes(p.notes).total, `型${p.id}`).toBeCloseTo(p.beats * p.bars, 6);
      expect(p.chords.length, `型${p.id}`).toBe(p.bars);
    }
  });
  it("JSON はガイドから作り直したものと一致する", () => {
    const fresh = mp.parsePatternsFromGuide(fs.readFileSync(mp.GUIDE_PATH, "utf8"));
    expect(fresh).toEqual(patterns);
  });
  it("調の表記を読む", () => {
    expect(mp.parseKeyLabel("変ホ長調")).toMatchObject({ tonic: 3, minor: false });
    expect(mp.parseKeyLabel("イ短調")).toMatchObject({ tonic: 9, minor: true });
    expect(mp.parseKeyLabel("ホ（ドリアン）")).toMatchObject({ tonic: 4, minor: null });
  });
  it("移高しても拍の合計と音の数が変わらず、コードも動く", () => {
    const p = patterns.find((x: { id: number }) => x.id === 1);
    const t = mp.transposePattern(p, mp.parseTonicArg("D"));
    expect(t.semis).toBe(-5);
    expect(t.chords[0]).toBe("D");
    expect(parseNotes(t.notes).notes.length).toBe(parseNotes(p.notes).notes.length);
    expect(parseNotes(t.notes).total).toBe(parseNotes(p.notes).total);
    expect(t.notes.startsWith("D4:1")).toBe(true);
  });
  it("場面で絞り、直前の曲の型は選ばない", () => {
    const all = mp.selectPatterns(patterns, { scene: "町" });
    expect(all.length).toBeGreaterThanOrEqual(3);
    const hist = [{ song: "a", pattern: all[0].id }];
    const next = mp.selectPatterns(patterns, { scene: "町", history: hist });
    expect(next.some((x: { id: number }) => x.id === all[0].id)).toBe(false);
    expect(mp.selectPatterns(patterns, { scene: "町", beats: 3 }).every((x: { beats: number }) => x.beats === 3)).toBe(true);
  });
  it("履歴の記録と、下書きからの変更数", () => {
    const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "pat-")), "h.json");
    try {
      mp.recordHistory("song-x", 4, f);
      expect(mp.readHistory(f)).toEqual([expect.objectContaining({ song: "song-x", pattern: 4 })]);
    } finally {
      fs.rmSync(path.dirname(f), { recursive: true, force: true });
    }
    expect(mp.changeCount("C4:1 D4:1 E4:2", "C4:1 D4:1 E4:2")).toBe(0);
    expect(mp.changeCount("C4:1 D4:1 E4:2", "C4:1 E4:1 E4:1")).toBe(2);
  });
  it("CLI の出力に下書きの注意が付く", () => {
    const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "pat-")), "h.json");
    try {
      const out = mp.runPatternCommand(["pattern", "--scene", "戦闘", "--key", "D", "--history", f]);
      expect(out).toContain("下書き");
      expect(out).toContain("型8");
    } finally {
      fs.rmSync(path.dirname(f), { recursive: true, force: true });
    }
  });
});

describe("P10 音程列の類似", () => {
  const a = seqOf("C5:1 D5:1 E5:1 G5:1 E5:1 D5:1 C5:1 D5:1 E5:2 G5:2");
  it("同じ旋律は 100% 一致。リズムも同じなら強い警告", () => {
    const r = is.intervalSimilarity(a, a);
    expect(r.rate).toBe(1);
    expect(r.rhythmRate).toBe(1);
  });
  it("移調しても音程列は一致する", () => {
    const b = a.map((n: { pitch: number }) => ({ ...n, pitch: n.pitch + 5 }));
    expect(is.intervalSimilarity(a, b).rate).toBe(1);
  });
  it("別の旋律はほとんど一致しない", () => {
    const c = seqOf("A4:1 F4:1 E5:1 B4:1 C6:1 G4:1 D5:1 F5:1 A5:2 E4:2");
    expect(is.intervalSimilarity(a, c).rate).toBeLessThan(0.2);
  });
  it("音程が同じでリズムが違えば、窓の一致だけ数える", () => {
    const d = a.map((n: { dur: number }, i: number) => ({ ...n, dur: i % 2 ? 0.5 : 1.5 }));
    const r = is.intervalSimilarity(a, d);
    expect(r.rate).toBe(1);
    expect(r.rhythmRate).toBeLessThan(1);
  });
  it("同じ音の連打だけの窓は数えない", () => {
    expect(is.windows(seqOf("C5:1 C5:1 C5:1 C5:1 C5:1 C5:1"), 6)).toEqual([]);
  });
  it("曲どうしの点検で 20% 超なら注意が出る", () => {
    const song = (notes: string) => ({ beats: 4, chords: "C C C", parts: [{ instrument: "lead", role: "メロディ", notes }] });
    const mine = song("C5:1 D5:1 E5:1 G5:1 E5:1 D5:1 C5:1 D5:1 E5:2 G5:1 R:1");
    const r = is.checkIntervalSimilarity(mine, [{ name: "前の曲", song: mine }]);
    expect(r.warnings[0]).toContain("【強い警告】");
    const other = song("A4:1 F4:1 E5:1 B4:1 C6:1 G4:1 D5:1 F5:1 A5:2 E4:1 R:1");
    expect(is.checkIntervalSimilarity(mine, [{ name: "別の曲", song: other }]).warnings).toEqual([]);
  });
});

describe("P12 直しの手順にリズム先を足した", () => {
  it("ワークフロー文書に書いてある", () => {
    const md = workflowMd;
    expect(md).toContain("音の高さより**先にリズムを変える**");
  });
});
