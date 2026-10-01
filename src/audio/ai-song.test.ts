import { describe, expect, it } from "vitest";
import { AI_SONG_GUIDE, AI_SONG_SCHEMA, aiSongToScore, applySustain, fitToLength, parseNotes } from "./ai-song";
import { trackTotalBeats } from "./edit";
import { grooveOffsetBeats, REST } from "./score";

const song = {
  title: "テストの曲", description: "テスト", bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2,
  autoAccompaniment: true, feel: "rock", tone: "rock",
  parts: [
    { instrument: "leadGuitar", role: "メロディ", volume: 0.25, pan: 0, amp: "prs", notes: "A4:1 C5:1 E5:2 R:4 D5:0.5 C5:0.5 B4:1 A4:2" },
    { instrument: "kick", role: "キック", volume: 0.3, pan: 0, amp: "auto", notes: "x:1 R:1 x:1 R:1" },
  ],
};

describe("AIソング形式", () => {
  it("曲に組み立てられる。伴奏つき・長さがそろう・短いパートはくり返す", () => {
    const { score, warnings } = aiSongToScore(song);
    expect(warnings).toEqual([]);
    expect(score.tempoBpm).toBe(120);
    const total = 8 * 4;
    for (const t of score.tracks) expect(trackTotalBeats(t)).toBeCloseTo(total, 6);
    const lead = score.tracks[score.tracks.length - 2];
    expect(lead.amp).toEqual({ type: "prs" });
    const kick = score.tracks[score.tracks.length - 1];
    expect(kick.notes.filter((n) => n.note !== REST).length).toBe(16);
  });
  it("伴奏なしにもできる", () => {
    expect(aiSongToScore({ ...song, autoAccompaniment: false }).score.tracks.length).toBe(2);
  });
  it("まちがいは、場所つきでまとめて知らせる", () => {
    const bad = { ...song, parts: [{ ...song.parts[0], notes: "H4:1 C5:abc" }, { ...song.parts[1], notes: "C4:1" }, { ...song.parts[0], instrument: "theremin" }] };
    const msg = (() => {
      try {
        aiSongToScore(bad);
        return "";
      } catch (e) {
        return (e as Error).message;
      }
    })();
    expect(msg).toMatch(/音名が読めません「H4:1」/);
    expect(msg).toMatch(/拍が読めません「C5:abc」/);
    expect(msg).toMatch(/ドラムは x か R/);
    expect(msg).toMatch(/楽器が一覧にありません/);
    expect(() => aiSongToScore({ ...song, chords: "Am Q" })).toThrow(/chords/);
  });
  it("長すぎるパートは切って知らせる", () => {
    const { warnings } = aiSongToScore({ ...song, parts: [{ ...song.parts[0], notes: "A4:40" }] });
    expect(warnings[0]).toMatch(/切りました/);
  });
  it("長さをそろえる道具", () => {
    expect(fitToLength([{ note: "C4", durationBeats: 3 }], 4).map((e) => e.durationBeats)).toEqual([3, 1]);
    expect(fitToLength([], 4)).toEqual([{ note: REST, durationBeats: 4 }]);
  });
  it("説明とスキーマに楽器の一覧が入っている", () => {
    expect(AI_SONG_GUIDE).toMatch(/leadGuitar/);
    expect(AI_SONG_SCHEMA.properties.parts.items.properties.instrument.enum).toContain("kick");
  });
  it("ジャンル別のアンプ（jazz など）を使える。知らない名前は注意を出して、おまかせにする", () => {
    const withAmps = { ...song, autoAccompaniment: false, parts: [{ ...song.parts[0], amp: "jazz" }, { ...song.parts[0], amp: "tubescreamer" }] };
    const { score, warnings } = aiSongToScore(withAmps);
    expect(score.tracks[0].amp).toEqual({ type: "jazz" });
    expect(score.tracks[1].amp).toBeUndefined();
    expect(warnings.some((w) => w.includes("tubescreamer"))).toBe(true);
    expect(AI_SONG_SCHEMA.properties.parts.items.properties.amp.enum).toContain("shoegaze");
  });
});

describe("民族楽器・ラウド系・繊細系アンプ（2026-10-02）", () => {
  const base = { title: "t", description: "", bpm: 100, beats: 4, chords: "Am", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "metal", parts: [] as unknown[] };
  it("民族楽器とラウド系・繊細系のアンプを受け付け、警告も出ない", () => {
    const parts = ["sitar", "koto", "shamisen", "banjo", "harp", "kalimba", "panflute", "shakuhachi", "ocarina", "fiddle", "bagpipe"].map((instrument, i) => ({ instrument, role: "r", volume: 0.1, pan: 0, amp: ["auto", "loudmetal", "loudrock", "delicate"][i % 4], notes: "A3:1 C4:1 E4:2" }));
    const r = aiSongToScore({ ...base, parts } as never);
    expect(r.warnings).toEqual([]);
    expect(r.score.tracks.length).toBe(parts.length);
  });
});

describe("ドラムのグリッド記法・音の伸び・グルーブ", () => {
  it("g: は1文字＝16分音符で、X は強く・o は弱く・. は休み", () => {
    const errors: string[] = [];
    const ev = parseNotes("g:Xxo.", true, errors, "t");
    expect(errors).toEqual([]);
    expect(ev.map((e) => e.durationBeats)).toEqual([0.25, 0.25, 0.25, 0.25]);
    expect(ev[0].velocity).toBe(1.3);
    expect(ev[1].velocity).toBeUndefined();
    expect(ev[2].velocity).toBe(0.5);
    expect(ev[3].note).toBe(REST);
    parseNotes("g:xz", true, errors, "t");
    expect(errors.length).toBe(1);
  });
  it("アクセントの強さは1.3倍までで、音量が極端に大きくならない", () => {
    expect(parseNotes("X:1", true, [], "t")[0].velocity).toBe(1.3);
  });
  it("sustain は休符以外に gate を付け、範囲は 0.2〜3", () => {
    const ev = applySustain([{ note: "C4", durationBeats: 1 }, { note: REST, durationBeats: 1 }], 9);
    expect(ev[0].gate).toBe(3);
    expect(ev[1].gate).toBeUndefined();
    expect(applySustain([{ note: "C4", durationBeats: 1 }], 1)[0].gate).toBeUndefined();
  });
  it("グルーブ: 裏拍は swing で遅れ、push はそのままずれる", () => {
    expect(grooveOffsetBeats(0, 0, 0.5)).toBe(0);
    expect(grooveOffsetBeats(0.6, 0, 0.5)).toBeCloseTo(0.1);
    expect(grooveOffsetBeats(0.6, 0, 1)).toBe(0);
    expect(grooveOffsetBeats(0.6, 0.02, 1.25)).toBeCloseTo(0.07);
  });
});

describe("出口の安全装置", () => {
  it("ceilingCurve は、小さい音はそのまま通し、どんなに大きくても ceiling を超えない", async () => {
    const { ceilingCurve } = await import("./voices");
    const c = ceilingCurve(0.7, 0.98);
    const at = (x: number): number => c[Math.round(((x + 1) / 2) * (c.length - 1))];
    expect(at(0.5)).toBeCloseTo(0.5, 2);
    expect(at(-0.5)).toBeCloseTo(-0.5, 2);
    expect(at(1)).toBeLessThanOrEqual(0.98);
    expect(Math.max(...Array.from(c).map(Math.abs))).toBeLessThanOrEqual(0.98);
    for (let i = 1; i < c.length; i++) expect(c[i]).toBeGreaterThanOrEqual(c[i - 1]);
  });
});

describe("サイドチェイン風（pump）", () => {
  it("pump: true で曲の pump が立ち、指定しなければ立たない", () => {
    const b = { title: "t", description: "", bpm: 120, beats: 4, chords: "Am", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "dance", tone: "rock", parts: [{ instrument: "kick", role: "k", volume: 0.2, pan: 0, amp: "auto", notes: "x:1" }] };
    expect(aiSongToScore({ ...b, pump: true } as never).score.pump).toBe(true);
    expect(aiSongToScore(b as never).score.pump).toBeUndefined();
  });
});
