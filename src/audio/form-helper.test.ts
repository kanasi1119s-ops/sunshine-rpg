import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { bluesChords, expandForm, FORM_PRESETS, type FormFields } from "./form-helper";

const base: FormFields = { chords: "C Am F G", barsPerChord: 1, repeats: 1 };
const sum = (s: unknown): number => (s as { bars: number }[]).reduce((a, x) => a + x.bars, 0);
const kinds = (s: unknown): string => (s as { kind: string }[]).map((x) => x.kind).join(",");

describe("form（形式の略記）", () => {
  it("form がなければ何も変えない", () => {
    const song = { ...base };
    expect(expandForm(song)).toBe(song);
  });

  it("AABA は 8小節×4 で A=verse・B=bridge、同じ文字は同じ kind", () => {
    const w: string[] = [];
    const out = expandForm({ ...base, form: "AABA" }, w);
    expect(kinds(out.sections)).toBe("verse,verse,bridge,verse");
    expect(sum(out.sections)).toBe(32);
    expect(out.repeats).toBe(8); // 4小節の進行を 32小節ぶん
    expect(out.occurrence).toBe(true);
    expect(w).toEqual([]);
  });

  it("名前つきの型がそれぞれ決まった並びになる", () => {
    expect(kinds(expandForm({ ...base, form: "ABAC" }).sections)).toBe("verse,interlude,verse,bridge");
    expect(kinds(expandForm({ ...base, form: "rondo" }).sections)).toBe("verse,interlude,verse,bridge,verse");
    expect(sum(expandForm({ ...base, form: "rondo" }).sections)).toBe(40);
    expect(kinds(expandForm({ ...base, form: "AB" }).sections)).toBe("verse,chorus");
    expect(sum(expandForm({ ...base, form: "AB" }).sections)).toBe(16);
    expect(Object.keys(FORM_PRESETS).length).toBeGreaterThanOrEqual(10);
  });

  it("verseChorus は導入・Bメロ・間奏・終わりが4小節", () => {
    const out = expandForm({ ...base, form: "verseChorus" });
    const secs = out.sections as { kind: string; bars: number }[];
    expect(secs[0]).toEqual({ kind: "intro", bars: 4 });
    expect(secs.find((s) => s.kind === "pre")?.bars).toBe(4);
    expect(secs.find((s) => s.kind === "chorus")?.bars).toBe(8);
    expect(secs[secs.length - 1]).toEqual({ kind: "outro", bars: 4 });
  });

  it("任意の文字の並びと unit・bars・kinds の上書き", () => {
    const out = expandForm({ ...base, form: { pattern: "ABBA", unit: 4, bars: { A: 8 }, kinds: { B: "interlude" } } });
    expect(out.sections).toEqual([{ kind: "verse", bars: 8 }, { kind: "interlude", bars: 4 }, { kind: "interlude", bars: 4 }, { kind: "verse", bars: 8 }]);
  });

  it("kind が決まらない文字は注意を出して飛ばす", () => {
    const w: string[] = [];
    const out = expandForm({ ...base, form: "AZA" }, w);
    expect(kinds(out.sections)).toBe("verse,verse");
    expect(w.join()).toContain("Z");
  });

  it("割り切れない小節数は注意を出す", () => {
    const w: string[] = [];
    const out = expandForm({ ...base, chords: "C Am F", form: "AABA" }, w);
    expect(out.repeats).toBe(11);
    expect(w.join()).toContain("整数倍");
  });

  it("form.chords は sectionChords（kind がキー）になる", () => {
    const out = expandForm({ ...base, form: { pattern: "AABA", chords: { A: "C Am F G", B: "F G Em Am" } } });
    expect(out.sectionChords).toEqual({ verse: "C Am F G", bridge: "F G Em Am" });
  });

  it("sections を自分で書いた曲では form の sections を使わない", () => {
    const w: string[] = [];
    const sections = [{ kind: "verse", bars: 4 }];
    const out = expandForm({ ...base, sections, form: "AABA" }, w);
    expect(out.sections).toBe(sections);
    expect(w.join()).toContain("sections が曲に書かれている");
  });

  it("使えない form は無視して注意", () => {
    const w: string[] = [];
    const song = { ...base, form: "aaba!" };
    expect(expandForm(song, w).sections).toBeUndefined();
    expect(w.join()).toContain("使えません");
  });

  it("曲線の名前を form に書くと sections と energy が入る", () => {
    const out = expandForm({ ...base, form: "sawtooth" });
    expect(kinds(out.sections)).toBe("intro,build,drop,break,build,drop,outro");
    expect(out.energy).toBe("sawtooth");
    expect(sum(out.sections)).toBe(72);
  });
});

describe("blues12", () => {
  it("12小節の進行（I7×4／IV7×2・I7×2／V7・IV7・I7・V7）", () => {
    expect(bluesChords("C")).toEqual(["C7", "C7", "C7", "C7", "F7", "F7", "C7", "C7", "G7", "F7", "C7", "G7"]);
  });
  it("クイックチェンジは2小節目が IV7、短調は m7", () => {
    expect(bluesChords("A", { quickChange: true })[1]).toBe("D7");
    expect(bluesChords("Bb", { minor: true }).slice(0, 5)).toEqual(["Bbm7", "Bbm7", "Bbm7", "Bbm7", "Ebm7"]);
  });
  it("form: blues12 は chords を 12 個にして repeats を周回数にする", () => {
    const out = expandForm({ ...base, form: { pattern: "blues12", key: "E", laps: 4 } });
    expect(out.chords.split(" ")).toHaveLength(12);
    expect(out.repeats).toBe(4);
    expect(sum(out.sections)).toBe(48);
    expect(kinds(out.sections)).toBe("verse,verse,verse,chorus");
  });
  it("laps を書かなければ repeats（2以上）か 3 周", () => {
    expect(expandForm({ ...base, form: "blues12" }).repeats).toBe(3);
    expect(expandForm({ ...base, repeats: 5, form: "blues12" }).repeats).toBe(5);
  });
});

describe("aiSongToScore との結合", () => {
  const song = (extra: Record<string, unknown>): AiSong => ({
    title: "t", description: "d", bpm: 100, beats: 4, chords: "C Am F G", barsPerChord: 1, repeats: 1, autoAccompaniment: true,
    feel: "pop", tone: "rock", parts: [{ instrument: "lead", role: "メロディ", volume: 0.25, pan: 0, amp: "auto", notes: "C5:4" }], ...extra,
  } as AiSong);

  it("form: AABA で 32小節の曲になる（occurrence で2回目のAに楽器が足される）", () => {
    const { score, warnings } = aiSongToScore(song({ form: "AABA" }));
    const beats = score.tracks[0].notes.reduce((a, n) => a + n.durationBeats, 0);
    expect(beats).toBe(32 * 4);
    expect(warnings.filter((w) => w.includes("form"))).toEqual([]);
    expect(score.meta?.form).toBe("AABA");
  });

  it("blues12 は 12小節×周回", () => {
    const { score } = aiSongToScore(song({ form: { pattern: "blues12", laps: 2 } }));
    expect(score.tracks[0].notes.reduce((a, n) => a + n.durationBeats, 0)).toBe(24 * 4);
  });

  it("form がなければ今までと同じ（meta なし）", () => {
    expect(aiSongToScore(song({})).score.meta).toBeUndefined();
  });
});
