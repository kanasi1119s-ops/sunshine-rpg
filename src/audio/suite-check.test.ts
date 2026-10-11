import { describe, expect, it } from "vitest";
import { checkSuite, chordLink, formatSuiteReport, keyRelation, resolveSuite, suiteFieldsFromSong, tempoRatio } from "./suite-check";

describe("テンポ比", () => {
  it("1:1・2:1・3:2・3:4 を許す（2%まで）", () => {
    expect(tempoRatio(120, 120)).toEqual([1, 1]);
    expect(tempoRatio(80, 160)).toEqual([2, 1]);
    expect(tempoRatio(100, 150)).toEqual([3, 2]);
    expect(tempoRatio(120, 90)).toEqual([3, 4]);
    expect(tempoRatio(100, 101)).toEqual([1, 1]);
    expect(tempoRatio(100, 130)).toBeNull();
    expect(tempoRatio(0, 100)).toBeNull();
  });
});

describe("調の関係", () => {
  const k = (key: string, mode: "major" | "minor" = "major") => ({ key, mode });
  it("同じ・5度上下・平行調・同主調・遠い", () => {
    expect(keyRelation(k("C"), k("C"))).toBe("same");
    expect(keyRelation(k("C"), k("G"))).toBe("fifth");
    expect(keyRelation(k("C"), k("F"))).toBe("fifth");
    expect(keyRelation(k("C"), k("A", "minor"))).toBe("relative");
    expect(keyRelation(k("A", "minor"), k("C"))).toBe("relative");
    expect(keyRelation(k("C"), k("C", "minor"))).toBe("parallel");
    expect(keyRelation(k("C"), k("F#"))).toBeNull();
    expect(keyRelation(k("C"), k("H"))).toBeNull();
  });
});

describe("コードのつながり", () => {
  it("同じ根音か、最後が次の属和音", () => {
    expect(chordLink("C", "C")).toBe("same");
    expect(chordLink("G7", "C")).toBe("dominant");
    expect(chordLink("A7", "Dm")).toBe("dominant");
    expect(chordLink("F", "C")).toBeNull();
    expect(chordLink("???", "C")).toBeNull();
  });
});

const song = (bpm: number, key: string, mode: "major" | "minor", lastChord: string, firstChord: string, energy: number[], link?: "beat" | "stinger" | "segue", extra = {}) =>
  ({ id: `${key}${bpm}`, bpm, key, mode, firstChord, lastChord, energy, link, ...extra });

describe("checkSuite", () => {
  it("よくできた組曲は注意なし", () => {
    const r = checkSuite({ songs: [
      song(100, "C", "major", "E7", "C", [2, 4, 5], undefined),
      song(100, "A", "minor", "E7", "Am", [3, 5, 6], "beat"),
      song(150, "A", "minor", "A7", "Am", [2, 6, 9], "stinger", { stinger: "sting-1" }),
      song(150, "D", "minor", "A7", "Dm", [3, 7, 10], "beat"),
    ] });
    expect(r.warnings).toEqual([]);
    expect(r.lines.length).toBeGreaterThanOrEqual(4);
    expect(formatSuiteReport("t", r)).toContain("注意なし");
  });

  it("テンポ・調・コード・つなぎの問題をそれぞれ指摘する", () => {
    const r = checkSuite({ songs: [
      song(100, "C", "major", "F", "C", [3, 4, 5]),
      song(137, "F#", "major", "B", "C", [4, 5, 6]),
      song(137, "F#", "major", "B", "F#", [5, 6, 7], "stinger"),
    ] });
    const all = r.warnings.join("\n");
    expect(all).toContain("テンポの比が簡単でありません");
    expect(all).toContain("調が遠いです");
    expect(all).toContain("属和音でも同じ和音でもありません");
    expect(all).toContain("つなぎの種類");
    expect(all).toContain("stinger（効果音の名前）");
  });

  it("全体の強さ: 幅が小さい・最高点が前半・最後の山の前に谷がない", () => {
    const flat = checkSuite({ songs: [song(100, "C", "major", "G", "C", [5, 5, 5]), song(100, "C", "major", "G", "C", [5, 6, 5], "beat")] });
    expect(flat.warnings.join()).toContain("幅");
    const early = checkSuite({ songs: [song(100, "C", "major", "G", "C", [10, 4, 3]), song(100, "C", "major", "G", "C", [3, 4, 5], "beat")] });
    expect(early.warnings.join()).toContain("前半");
    const noValley = checkSuite({ songs: [song(100, "C", "major", "G", "C", [8, 8, 8]), song(100, "C", "major", "G", "C", [9, 9, 10], "beat")] });
    expect(noValley.warnings.join()).toContain("谷");
  });

  it("2曲未満は注意", () => {
    expect(checkSuite({ songs: [song(100, "C", "major", "G", "C", [1])] }).warnings.join()).toContain("2曲以上");
  });
});

describe("曲のJSONから値を読む（file）", () => {
  const json = { bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 8, energy: "sawtooth" };
  it("bpm・調・最初／最後のコード・小節数・強さを取り出す", () => {
    const f = suiteFieldsFromSong(json);
    expect(f).toMatchObject({ bpm: 120, key: "A", mode: "minor", bars: 32, firstChord: "Am", lastChord: "G" });
    expect(f.energy).toHaveLength(7);
  });
  it("file を解決して、書いた値で上書きできる。読めない file は注意", () => {
    const w: string[] = [];
    const songs = resolveSuite({ songs: [{ file: "a", link: "beat" }, { file: "missing" }, { file: "a", bpm: 90, id: "a2" }] }, (n) => (n === "a" ? json : null), w);
    expect(songs.map((s) => s.id)).toEqual(["a", "a2"]);
    expect(songs[1].bpm).toBe(90);
    expect(songs[0].link).toBe("beat");
    expect(w.join()).toContain("missing");
  });
});
