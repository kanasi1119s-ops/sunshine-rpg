import { describe, expect, it } from "vitest";
import { findTypeRepeats, inferIntroType, readTrackTypes, typeWarnings } from "./type-check";

const part = (instrument: string, notes: string) => ({ instrument, notes });

describe("導入の型の推測", () => {
  it("1拍目から全員＝I1", () => {
    expect(inferIntroType({ beats: 4, parts: [part("kick", "x:1"), part("bass", "C2:1"), part("distGuitar", "E3:1"), part("lead", "E5:1")] })).toBe("I1");
  });
  it("最初の1小節が休みで2小節目から全員＝I4", () => {
    expect(inferIntroType({ beats: 4, parts: [part("kick", "R:4 x:1 x:1 x:1 x:1"), part("bass", "R:4 C2:4"), part("lead", "R:4 E5:4")] })).toBe("I4");
  });
  it("ドラムだけ＝I6、長音1つ＝I5、短い音1つ＝I2", () => {
    expect(inferIntroType({ beats: 4, parts: [part("hihat", "x:0.5"), part("lead", "R:8 E5:4"), part("bass", "R:8 C2:4")] })).toBe("I6");
    expect(inferIntroType({ beats: 4, parts: [part("pad", "C3:8"), part("lead", "R:8 E5:4"), part("bass", "R:8 C2:4")] })).toBe("I5");
    expect(inferIntroType({ beats: 4, parts: [part("lead", "E5:0.5 G5:0.5"), part("bass", "R:8 C2:4"), part("kick", "R:8 x:1")] })).toBe("I2");
  });
  it("先頭が chorus 4小節以下＝I3、判断できなければ undefined", () => {
    expect(inferIntroType({ beats: 4, sections: [{ kind: "chorus", bars: 4 }, { kind: "verse", bars: 8 }], parts: [part("lead", "E5:4")] })).toBe("I3");
    expect(inferIntroType({ beats: 4, parts: [] })).toBeUndefined();
  });
});

describe("重複チェック", () => {
  it("書いた型が直前の曲と同じなら警告", () => {
    const w = typeWarnings({ name: "now", introType: "I5", outroType: "E1" }, [{ name: "prev", introType: "I5", outroType: "E3" }, { name: "prev2", introType: "I1", outroType: "E1" }]);
    expect(w).toHaveLength(2);
    expect(w[0]).toContain("prev");
    expect(w[0]).toContain("I5");
    expect(w[1]).toContain("prev2");
  });
  it("型の記録がない曲は無警告", () => {
    expect(typeWarnings({ name: "now" }, [{ name: "prev" }, { name: "prev2" }])).toEqual([]);
    expect(typeWarnings({ name: "now", introType: "I2" }, [{ name: "prev" }])).toEqual([]);
  });
  it("書いていない側は推測で比べる（推測と明記）", () => {
    const song = { beats: 4, parts: [part("pad", "C3:8"), part("lead", "R:8 E5:4"), part("bass", "R:8 C2:4")] };
    const r = findTypeRepeats({ name: "now", introType: "I5" }, [{ name: "prev", song }]);
    expect(r).toEqual([{ kind: "intro", type: "I5", with: "prev", inferred: true }]);
    expect(typeWarnings({ name: "now", introType: "I5" }, [{ name: "prev", song }])[0]).toContain("推測");
  });
  it("違う型なら警告なし", () => {
    expect(typeWarnings({ name: "now", introType: "I1", outroType: "E2" }, [{ name: "prev", introType: "I5", outroType: "E1" }])).toEqual([]);
  });
});

describe("tracks.md の表", () => {
  const md = "# 曲\n\n## 導入・終わりの型\n\n| ID | 導入の型 | 終わりの型 |\n|---|---|---|\n| title | I3 | E5 |\n| battle | i1 | E1 |\n| town | | |\n| bad | I11 | E0 |\n\n次の文。\n| ID | 曲名 |\n";
  it("型が書かれた行だけ読む", () => {
    expect(readTrackTypes(md)).toEqual([{ name: "title", introType: "I3", outroType: "E5" }, { name: "battle", introType: "I1", outroType: "E1" }]);
  });
  it("表がなければ空", () => {
    expect(readTrackTypes("| ID | 曲名 |\n|---|---|\n| a | b |")).toEqual([]);
  });
});
