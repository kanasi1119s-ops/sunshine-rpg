import { describe, expect, it } from "vitest";
import { parseNotes } from "./ai-song";
import { applyBreath, checkBreath, checkInstrumentRange, checkPolyphony, checkWorldInstrumentScale, INSTRUMENT_RANGES, longestRun } from "./instrument-range";
import { AI_INSTRUMENTS } from "./ai-song";
import { REST } from "./score";

const tr = (instrument: string, notes: string, drum = false) => ({ instrument: instrument as never, role: instrument, notes: parseNotes(notes, drum, [], "t") });

describe("音域の点検", () => {
  it("楽器ごとの表がある（ドラム・効果音を除く AI 楽器はほぼ全部）", () => {
    const need = Object.keys(AI_INSTRUMENTS).filter((k) => !["kick", "snare", "hihat", "crash", "tom"].includes(k));
    expect(need.filter((k) => !INSTRUMENT_RANGES[k])).toEqual([]);
  });
  it("尺八の C4 は出ない（最低 D4）。小節番号つき", () => {
    const w = checkInstrumentRange([tr("shakuhachi", "D4:4 C4:4 F4:4")], 4);
    expect(w).toHaveLength(1);
    expect(w[0]).toContain("C4");
    expect(w[0]).toContain("2小節目");
  });
  it("自然な音域の外（歪みギターの高い音）は注意", () => {
    const w = checkInstrumentRange([tr("distGuitar", "E4:4 A4:4")], 4);
    expect(w[0]).toMatch(/^注意/);
    expect(w[0]).toContain("A4");
  });
  it("音域内なら何も出ない", () => {
    expect(checkInstrumentRange([tr("guitar", "E2:2 A3:2 E5:4"), tr("piano", "C3:4")], 4)).toEqual([]);
  });
});

describe("同時発音の点検", () => {
  it("ギター 7 音の同時発音は警告、同じ音の二重録りは数えない", () => {
    const six = ["E2", "B2", "E3", "G#3", "B3", "E4"].map((n) => tr("guitar", `${n}:4`));
    expect(checkPolyphony(six, 4)).toEqual([]);
    expect(checkPolyphony([...six, tr("guitar", "G4:4")], 4)[0]).toContain("7 音");
    expect(checkPolyphony([...six, tr("distGuitar", "E4:4")], 4)).toEqual([]);
  });
  it("半音ちがいが同時に鳴るギターは注意", () => {
    expect(checkPolyphony([tr("guitar", "E3:4"), tr("crunch", "F3:4")], 4)[0]).toMatch(/半音/);
  });
  it("ドラム: 手は 2 本。スネア＋ハイハット＋クラッシュは警告、キックを足すのは良い", () => {
    const d = (i: string, n: string) => tr(i, n, true);
    expect(checkPolyphony([d("kick", "x:1"), d("snare", "x:1"), d("hihat", "x:1")], 4)).toEqual([]);
    const w = checkPolyphony([d("snare", "x:1"), d("hihat", "x:1"), d("crash", "x:1")], 4);
    expect(w.join()).toContain("3 つ以上");
    expect(checkPolyphony([d("kick", "x:1"), d("snare", "x:1"), d("hihat", "x:1"), d("tom", "x:1"), d("crash", "x:1")], 4).join()).toContain("5 つ");
  });
});

describe("息継ぎ", () => {
  const bpm = 120; // 1 拍 0.5 秒
  it("11 秒休まない lead は警告、休符があれば出ない", () => {
    expect(checkBreath([tr("lead", "C5:22")], bpm, 4)[0]).toContain("11.0 秒");
    expect(checkBreath([tr("lead", "C5:10 R:1 C5:11")], bpm, 4)).toEqual([]);
    expect(checkBreath([tr("guitar", "C4:40")], bpm, 4)).toEqual([]);
  });
  it("longestRun は休符で切れる", () => {
    const ev = parseNotes("C5:4 R:1 C5:8", false, [], "t");
    expect(longestRun(ev, 120)).toEqual({ sec: 4, startBeat: 5 });
  });
  it("applyBreath: 長さは変わらず、続けて鳴る時間が短くなる", () => {
    const ev = parseNotes("C5:2 D5:2 E5:2 F5:2 G5:2 A5:2 B5:2 C6:2", false, [], "t"); // 16 拍＝8 秒
    const out = applyBreath(ev, bpm, 4);
    const total = (l: typeof ev) => l.reduce((s, e) => s + e.durationBeats, 0);
    expect(total(out)).toBe(total(ev));
    expect(out.filter((e) => e.note === REST).length).toBeGreaterThan(0);
    expect(longestRun(out, bpm).sec).toBeLessThan(longestRun(ev, bpm).sec);
  });
});

describe("和楽器の音階", () => {
  it("尺八の基準（D F G A C）から外れ過ぎると注意、メリ付きは許す", () => {
    expect(checkWorldInstrumentScale([tr("shakuhachi", "D4:1 F4:1 G4:1 A4:1 C5:1 D5:1")])).toEqual([]);
    expect(checkWorldInstrumentScale([tr("shakuhachi", "D4:1 E4:1 G4:1 B4:1")])[0]).toContain("50%");
    expect(checkWorldInstrumentScale([tr("shakuhachi", "D4:1 E4:1/ G4:1 B4:1^")])).toEqual([]);
  });
});
