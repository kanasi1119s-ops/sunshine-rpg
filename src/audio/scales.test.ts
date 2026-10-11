import guideText from "../../docs/sound/scales-world-guide.md?raw";
import { describe, expect, it } from "vitest";
import { CHORD_QUALITIES, SCALES, characteristicSemis, chordsInScale, findScale, harmonize, pitchClassOf, resolveScale, scalePitchClasses, snapNote, snapNotesToScale } from "./scales";
import { parseChord } from "./newsong";

const doc = guideText.split("\n");
const rowsAfter = (heading: string, count = 80): string[][] => {
  const start = doc.findIndex((l) => l.startsWith(heading));
  return doc
    .slice(start + 1, start + count)
    .filter((l) => l.startsWith("|") && !l.includes("---"))
    .map((l) => l.split("|").map((s) => s.trim()).slice(1, -1));
};
const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const pcOfName = (n: string): number => (PC[n[0]] + (n.includes("#") ? 1 : 0) - (n.includes("b") ? 1 : 0) + 12) % 12;

describe("音階の表（scales.ts）", () => {
  it("ガイド 2-1 の 42 種＋微分音 2 種が全部ある", () => {
    expect(SCALES.length).toBe(44);
    expect(SCALES.filter((s) => s.micro).length).toBe(2);
    expect(new Set(SCALES.map((s) => s.id)).size).toBe(44);
  });
  it("音の並びがガイドの表の音名と一致し、半音の間隔の合計が 12", () => {
    const rows = rowsAfter("### 2-1.", 70).filter((r) => r.length >= 7 && /^[\d-]+$/.test(r[3]));
    expect(rows.length).toBe(42);
    rows.forEach((r, i) => {
      const s = SCALES[i];
      expect(r[1].startsWith(s.name), `${i}: ${r[1]} vs ${s.name}`).toBe(true);
      expect(s.semis).toEqual(r[2].split(" ").map(pcOfName));
      const steps = r[3].split("-").map(Number);
      expect(steps.reduce((a, b) => a + b, 0)).toBe(12);
      expect(s.semis.map((v, j) => (s.semis[j + 1] ?? 12) - v)).toEqual(steps);
    });
  });
  it("名前・別名・主音つきで引ける", () => {
    expect(findScale("都節音階")?.id).toBe("miyako");
    expect(findScale("Hirajoshi")?.id).toBe("hirajoshi");
    expect(findScale("ヒジャーズ")?.id).toBe("phrygian-dominant");
    expect(resolveScale("miyako@D")).toMatchObject({ tonic: 2, scale: { id: "miyako" } });
    expect(resolveScale("ro", "Bb")?.tonic).toBe(10);
    expect(resolveScale("ぞんざい")).toBeNull();
    expect(pitchClassOf("F#4")).toBe(6);
  });
  it("scalePitchClasses: 都節を D にすると D Eb G A Bb", () => {
    expect(scalePitchClasses(findScale("miyako")!, 2)).toEqual([2, 3, 7, 9, 10]);
    expect(scalePitchClasses(findScale("rast")!, 0)).toEqual([0, 2, 4, 5, 7, 9, 11]);
  });
  it("特性音: ドリアンは長6度、フリジアンは短2度", () => {
    expect(characteristicSemis(findScale("dorian")!)).toEqual([9]);
    expect(characteristicSemis(findScale("phrygian")!)).toEqual([1]);
    expect(characteristicSemis(findScale("miyako")!)).toEqual([1, 8]);
  });
});

describe("snapToScale", () => {
  const miyakoD = findScale("miyako")!;
  it("音階内の音は変わらず、外の音は近い音へ（nearest は同じ近さなら下）", () => {
    expect(snapNote("D4", miyakoD, 2)).toBe("D4");
    expect(snapNote("E4", miyakoD, 2)).toBe("Eb4");
    expect(snapNote("F4", miyakoD, 2)).toBe("Eb4"); // Eb(−2) と G(+2) は同じ近さ → 下
    expect(snapNote("F4", miyakoD, 2, "up")).toBe("G4");
    expect(snapNote("C4", miyakoD, 2, "down")).toBe("Bb3");
  });
  it("文字列: 拍・休符・奏法の記号が残り、合計が変わらない", () => {
    const src = "E4:1! R:0.5 F4:0.5,' G4:2~ B4:1^^_ C5:1/";
    const out = snapNotesToScale(src, miyakoD, 2);
    const strip = (t: string): string[] => t.split(" ").map((x) => x.replace(/^[^:]+/, ""));
    expect(strip(out)).toEqual(strip(src));
    expect(out.split(" ")[1]).toBe("R:0.5");
    const total = (t: string): number => t.split(" ").reduce((s, x) => s + parseFloat(x.split(":")[1]), 0);
    expect(total(out)).toBe(total(src));
    for (const t of out.split(" ")) if (!t.startsWith("R")) expect(scalePitchClasses(miyakoD, 2)).toContain(pitchClassOf(t.split(":")[0])!);
  });
});

describe("音階内の和音", () => {
  it("2-3 の『完全に収まる和音』の表と一致（C 主音）", () => {
    const rows = rowsAfter("### 2-3.", 18).filter((r) => r.length === 2 && !r[0].startsWith("音階"));
    expect(rows.length).toBe(11);
    for (const r of rows) {
      const scale = findScale(r[0].replace(/（.*$/, ""))!;
      expect(scale, r[0]).toBeTruthy();
      expect(new Set(chordsInScale(scale, 0)), r[0]).toEqual(new Set(r[1].split(" ")));
    }
  });
  it("7sus4 と 5 は、指定すれば数える", () => {
    expect(chordsInScale(findScale("ro")!, 0)).not.toContain("D7sus4");
    expect(chordsInScale(findScale("ro")!, 0, [...CHORD_QUALITIES, "7sus4", "5"])).toContain("D7sus4");
  });
  it("2-2 の三和音・四和音の表と一致", () => {
    const modeOf = (n: string): string => n.replace(/（.*$/, "");
    for (const [heading, size] of [["三和音", 3], ["四和音", 4]] as const) {
      const start = doc.findIndex((l) => l.startsWith(heading));
      const rows = doc.slice(start + 1, start + 16).filter((l) => l.startsWith("|") && !l.includes("---") && !l.includes("旋法")).map((l) => l.split("|").map((s) => s.trim()).slice(1, -1));
      expect(rows.length).toBe(9);
      for (const r of rows) {
        const scale = findScale(modeOf(r[0]))!;
        expect(scale, r[0]).toBeTruthy();
        const got = harmonize(scale, 0, size).map((c) => c.name);
        expect(got, r[0]).toEqual(r.slice(1).map((x) => x.replace("※", "")));
      }
    }
  });
  it("ペンタトニックは 7 音でないので空。読めない種類は readable:false", () => {
    expect(harmonize(findScale("miyako")!, 0, 3)).toEqual([]);
    const hm = harmonize(findScale("harmonic-minor")!, 0, 4);
    expect(hm[2]).toMatchObject({ name: "Ebmaj7#5", readable: false });
    expect(hm[0]).toMatchObject({ name: "Cm(maj7)", readable: true });
  });
});

describe("第1弾の積み残し: コード記法", () => {
  it("5・m7-5・mmaj7・M7 が読める", () => {
    expect(parseChord("E5")).toMatchObject({ root: 4, intervals: [0, 7] });
    expect(parseChord("Bm7-5")?.intervals).toEqual([0, 3, 6, 10]);
    expect(parseChord("Amaj7")?.intervals).toEqual([0, 4, 7, 11]);
    expect(parseChord("Cmmaj7")?.intervals).toEqual([0, 3, 7, 11]);
    expect(parseChord("CM7")?.intervals).toEqual([0, 4, 7, 11]);
  });
});
