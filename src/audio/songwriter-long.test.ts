import { describe, expect, it } from "vitest";
import { getScoreDurationSec } from "./score";
import { composeSong, planKinds, type Flavor, type SongSpec, type Style } from "./songwriter";

const STYLES: Style[] = [
  "rock", "metal", "classic", "space", "cafe", "discord", "mystery", "epic", "folk", "baroque", "nature", "phonk",
  "samba", "jazz", "rnb", "electro", "hardcore", "deathmetal", "progmetal", "jpop", "dancerock", "cleandance",
];
const base = (over: Partial<SongSpec>): SongSpec => ({ id: "t", title: "t", scene: "", style: "rock", tonic: "E", minor: true, bpm: 130, seed: 1, ...over, beats: (over.style ?? "rock") === "progmetal" ? 7 : (over.beats ?? 4) });
const beatsOf = (notes: { durationBeats: number }[]): number => notes.reduce((s, n) => s + n.durationBeats, 0);

describe("長尺モード（4〜5分）", () => {
  it("どのテンポでも、構成が決まりごとを満たす（イントロで始まりアウトロで終わる・サビは2回以上・同じ区間が3回続かない・長いときは間奏がある）", () => {
    for (const bpm of [70, 90, 110, 130, 150, 170, 200]) {
      for (const beats of [3, 4]) {
        const kinds = planKinds(bpm, beats, 270);
        expect(kinds[0]).toBe("intro");
        expect(kinds[kinds.length - 1]).toBe("outro");
        expect(kinds.filter((k) => k === "chorus").length).toBeGreaterThanOrEqual(2);
        for (let i = 2; i < kinds.length; i++) expect(!(kinds[i] === kinds[i - 1] && kinds[i] === kinds[i - 2])).toBe(true);
        // B・B、間奏・間奏、アウトロ・アウトロのように同じ区間が並ばない（A・A とサビ・サビだけは許す）
        for (let i = 1; i < kinds.length; i++) if (kinds[i] === kinds[i - 1]) expect(["verse", "chorus"], `${bpm}BPM ${beats}拍 ${kinds.join(",")}`).toContain(kinds[i]);
        if (kinds.length >= 9) expect(kinds).toContain("solo");
      }
    }
  });

  it("全ての曲調で、目標270秒に対して4:00〜5:00に収まり、全パートの拍数がそろう（ループできる）", () => {
    for (const style of STYLES) {
      for (const bpm of [80, 120, 160, 190]) {
        const score = composeSong(base({ style, bpm, targetSec: 270, seed: bpm }));
        const sec = getScoreDurationSec(score);
        expect(sec, `${style} ${bpm}BPM`).toBeGreaterThanOrEqual(240);
        expect(sec, `${style} ${bpm}BPM`).toBeLessThanOrEqual(300);
        const lens = new Set(score.tracks.map((t) => Math.round(beatsOf(t.notes) * 1000)));
        expect(lens.size, `${style} ${bpm}BPM のパートの長さがそろっていない`).toBe(1);
      }
    }
  });

  it("2回目のAメロは1回目と別の旋律になる（単調にならない）", () => {
    const score = composeSong(base({ style: "jpop", tonic: "C", minor: false, bpm: 120, targetSec: 270, seed: 5 }));
    const lead = score.tracks.find((t) => t.instrument === "lead" || t.instrument === "leadGuitar");
    expect(lead).toBeTruthy();
    const kinds = planKinds(120, 4, 270);
    // 区間ごとの旋律を切り出して、verseの1回目と2回目を比べる
    const bars = (kind: string, nth: number): string => {
      let bar = 0;
      let count = 0;
      for (const k of kinds) {
        const len = k === "intro" ? 4 : 8;
        if (k === kind && count++ === nth) {
          let pos = 0;
          const out: string[] = [];
          for (const n of lead!.notes) {
            if (pos >= bar * 4 && pos < (bar + len) * 4) out.push(`${n.note}:${n.durationBeats}`);
            pos += n.durationBeats;
          }
          return out.join(" ");
        }
        bar += len;
      }
      return "";
    };
    const v1 = bars("verse", 0);
    const v2 = bars("verse", 1);
    expect(v1.length).toBeGreaterThan(0);
    // 長尺では、verseの1回目と2回目は別の旋律（短尺の従来動作は変えない）
    expect(planKinds(120, 4, 270).filter((k) => k === "verse").length).toBeGreaterThanOrEqual(2);
    expect(v1).not.toBe(v2);
    expect(bars("verse", 2)).not.toBe(v1);
    expect(bars("verse", 2)).not.toBe(v2);
  });

  it("同じ設計図からは、毎回同じ曲ができる", () => {
    const a = composeSong(base({ style: "progmetal", bpm: 150, targetSec: 270, seed: 42, flavor: "loud" }));
    const b = composeSong(base({ style: "progmetal", bpm: 150, targetSec: 270, seed: 42, flavor: "loud" }));
    expect(JSON.stringify(a)).toBe(JSON.stringify(b));
  });

  it("90秒以下の従来の曲（60〜90秒）は変わらない", () => {
    for (const style of STYLES) {
      const sec = getScoreDurationSec(composeSong(base({ style, bpm: 130, seed: 3 })));
      expect(sec, style).toBeGreaterThanOrEqual(55);
      expect(sec, style).toBeLessThanOrEqual(95);
    }
  });
});

describe("味つけ（flavor）", () => {
  const instruments = (flavor: Flavor, style: Style = "rock"): Set<string | undefined> => new Set(composeSong(base({ style, flavor, targetSec: 270 })).tracks.map((t) => t.instrument));

  it("オーケストラは、弦・ブラス・合唱・ティンパニを足す", () => {
    const set = instruments("orchestra");
    for (const i of ["strings", "brass", "choir", "tom"]) expect(set.has(i)).toBe(true);
  });

  it("和楽器は、琴・三味線・尺八を足す", () => {
    const set = instruments("wagakki", "metal");
    for (const i of ["koto", "shamisen", "shakuhachi"]) expect(set.has(i)).toBe(true);
  });

  it("ラウドは、リズムギターを左右いっぱいに倍にして、専用アンプを通す（メタル系は loudmetal、ロック系は loudrock）", () => {
    for (const [style, amp] of [["metal", "loudmetal"], ["rock", "loudrock"]] as const) {
      const score = composeSong(base({ style, flavor: "loud", targetSec: 270 }));
      const rhythm = score.tracks.filter((t) => t.instrument === "distGuitar" || t.instrument === "crunch");
      expect(rhythm.length).toBeGreaterThanOrEqual(2);
      expect(rhythm.every((t) => t.amp?.type === amp)).toBe(true);
      expect(rhythm.some((t) => t.pan === -0.9)).toBe(true);
      expect(rhythm.some((t) => t.pan === 0.9)).toBe(true);
      expect(rhythm.every((t) => t.volume <= 0.1)).toBe(true);
    }
  });

  it("味つけをつけても、全パートの拍数がそろう", () => {
    for (const flavor of ["loud", "orchestra", "wagakki"] as const) {
      for (const style of ["rock", "metal", "dancerock", "progmetal"] as const) {
        const score = composeSong(base({ style, flavor, targetSec: 270 }));
        const lens = new Set(score.tracks.map((t) => Math.round(beatsOf(t.notes) * 1000)));
        expect(lens.size, `${style}+${flavor}`).toBe(1);
      }
    }
  });
});
