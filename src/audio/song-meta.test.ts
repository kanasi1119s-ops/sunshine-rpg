import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { buildLoopMeta, buildManifest, buildSongMeta, INTRO_TYPES, OUTRO_TYPES, parseBossPhases, parseIntroType, parseOutroType } from "./song-meta";

describe("ループ点（loop: {startBar,endBar}）", () => {
  it("true は曲全体、秒数は小節から計算", () => {
    expect(buildLoopMeta(true, 32, 4, 120, [])).toEqual({ startBar: 1, endBar: 32, startSec: 0, endSec: 64 });
    expect(buildLoopMeta("seamless", 16, 4, 60, [])?.endSec).toBe(64);
  });
  it("導入を1回だけ鳴らして 5〜36小節をくり返す", () => {
    expect(buildLoopMeta({ startBar: 5, endBar: 36 }, 36, 4, 120, [])).toEqual({ startBar: 5, endBar: 36, startSec: 8, endSec: 72 });
  });
  it("範囲がおかしければ注意を出して曲全体にする", () => {
    const w: string[] = [];
    expect(buildLoopMeta({ startBar: 9, endBar: 4 }, 16, 4, 120, w)).toMatchObject({ startBar: 1, endBar: 16 });
    expect(w.join()).toContain("startBar");
  });
  it("loop を書かなければ undefined", () => {
    expect(buildLoopMeta(undefined, 16, 4, 120, [])).toBeUndefined();
    expect(buildLoopMeta(false, 16, 4, 120, [])).toBeUndefined();
  });
});

describe("導入・終わりの型", () => {
  it("I1〜I10・E1〜E10（小文字も可）", () => {
    expect(Object.keys(INTRO_TYPES)).toHaveLength(10);
    expect(Object.keys(OUTRO_TYPES)).toHaveLength(10);
    expect(parseIntroType("i5", [])).toBe("I5");
    expect(parseOutroType("E10", [])).toBe("E10");
  });
  it("未記入は何も言わない／使えない型は注意", () => {
    const w: string[] = [];
    expect(parseIntroType(undefined, w)).toBeUndefined();
    expect(parseOutroType("", w)).toBeUndefined();
    expect(w).toEqual([]);
    expect(parseIntroType("I11", w)).toBeUndefined();
    expect(w.join()).toContain("I11");
  });
});

describe("ボスの段階表", () => {
  const secs = [{ kind: "intro" as const, bars: 2 }, { kind: "chorus" as const, bars: 14 }, { kind: "chorus" as const, bars: 16 }, { kind: "chorus" as const, bars: 16 }];
  it("正しい表はそのまま通る（HPは1→0.6→0.3）", () => {
    const w: string[] = [];
    const p = parseBossPhases([{ startBar: 1, endBar: 16, hpBelow: 1 }, { startBar: 17, endBar: 32, hpBelow: 0.6 }, { startBar: 33, endBar: 48, hpBelow: 0.3 }], 48, secs, w);
    expect(p).toHaveLength(3);
    expect(p![1]).toEqual({ id: "p2", startBar: 17, endBar: 32, hpBelow: 0.6 });
    expect(w).toEqual([]);
  });
  it("endBar と hpBelow を省略すると自動で埋める", () => {
    const p = parseBossPhases([{ startBar: 1 }, { startBar: 17 }, { startBar: 33 }], 48, undefined, []);
    expect(p!.map((x) => x.endBar)).toEqual([16, 32, 48]);
    expect(p!.map((x) => x.hpBelow)).toEqual([1, 0.67, 0.33]);
  });
  it("範囲外・短すぎ・HPが減らない・セクションの変わり目でない、に注意", () => {
    const w: string[] = [];
    parseBossPhases([{ startBar: 1, endBar: 16, hpBelow: 0.5 }, { startBar: 18, endBar: 20, hpBelow: 0.8 }, { startBar: 30, endBar: 99, hpBelow: 0.2 }], 48, secs, w);
    const all = w.join("\n");
    expect(all).toContain("最初の段階の hpBelow は 1");
    expect(all).toContain("短すぎ");
    expect(all).toContain("範囲");
    expect(all).toContain("以上です");
    expect(all).toContain("変わり目ではありません");
  });
  it("書かなければ undefined、空配列は注意", () => {
    expect(parseBossPhases(undefined, 48, undefined, [])).toBeUndefined();
    const w: string[] = [];
    expect(parseBossPhases([], 48, undefined, w)).toBeUndefined();
    expect(w).toHaveLength(1);
  });
});

describe("buildSongMeta と管理ファイル", () => {
  it("何も書かれていなければ meta なし", () => {
    expect(buildSongMeta({}, { totalBars: 16, beatsPerBar: 4, bpm: 120 }, [])).toBeUndefined();
  });
  it("まとめて入る", () => {
    const m = buildSongMeta({ form: "AABA", loop: true, introType: "I5", outroType: "E1", motifs: ["akari", "akari", "wa"], laps: 2 }, { totalBars: 32, beatsPerBar: 4, bpm: 100 }, []);
    expect(m).toMatchObject({ form: "AABA", introType: "I5", outroType: "E1", motifs: ["akari", "wa"], laps: 2, bars: 32, beatsPerBar: 4 });
    expect(m?.loop?.endSec).toBe(76.8);
  });
  it("管理ファイルに曲名・テンポ・メタが入る", () => {
    const man = buildManifest("x", "題", { tempoBpm: 100, loop: true, tracks: [], meta: { introType: "I2" } }, 30);
    expect(man).toMatchObject({ format: "sunshine-song-manifest", name: "x", title: "題", bpm: 100, seconds: 30, introType: "I2" });
  });
});

describe("aiSongToScore で meta ができる", () => {
  const song = (extra: Record<string, unknown>): AiSong => ({
    title: "t", description: "d", bpm: 160, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 12, autoAccompaniment: true, feel: "rock", tone: "metal",
    parts: [{ instrument: "lead", role: "メロディ", volume: 0.25, pan: 0, amp: "auto", notes: "A4:4" }], ...extra,
  } as AiSong);
  it("loop・型・ボス段階が Score.meta に残る", () => {
    const { score, warnings } = aiSongToScore(song({
      loop: { startBar: 5, endBar: 48 }, introType: "I4", outroType: "E7",
      sections: [{ kind: "intro", bars: 4 }, { kind: "chorus", bars: 12 }, { kind: "chorus", bars: 16 }, { kind: "chorus", bars: 16 }],
      bossPhases: [{ startBar: 5, endBar: 16, hpBelow: 1 }, { startBar: 17, endBar: 32, hpBelow: 0.6 }, { startBar: 33, endBar: 48, hpBelow: 0.3 }],
    }));
    expect(score.meta?.loop).toMatchObject({ startBar: 5, endBar: 48, startSec: 6 });
    expect(score.meta?.introType).toBe("I4");
    expect(score.meta?.outroType).toBe("E7");
    expect(score.meta?.bossPhases).toHaveLength(3);
    expect(warnings.filter((w) => w.includes("bossPhases"))).toEqual([]);
  });
  it("使わなければ meta なし", () => {
    expect(aiSongToScore(song({})).score.meta).toBeUndefined();
  });
  it("存在しない主題IDは注意", () => {
    expect(aiSongToScore(song({ motifs: ["nothing"] })).warnings.join()).toContain("nothing");
  });
});
