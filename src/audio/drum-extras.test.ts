import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { BOSS_PHASES, applyHihatSections, applyTrapRolls, barKindsOf, bossPhasePlan, hatSectionOf, replaceBeatRange } from "./drum-extras";
import { hihatPattern } from "./drum-genres";
import { makeTempoClock } from "./tempo-map";
import { REST, type NoteEvent, type Track } from "./score";
import { ROCK_SONG } from "./rhythm-fixtures";
import { getScoreDurationSec } from "./score";

const sum = (ns: readonly NoteEvent[]): number => ns.reduce((s, n) => s + n.durationBeats, 0);
const hatTrack = (bars: number, beats = 4): Track => ({ waveform: "square", instrument: "hihat", volume: 0.1, notes: Array.from({ length: bars * beats * 2 }, () => ({ note: "F#2", durationBeats: 0.5, velocity: 78 })) });

describe("セクション別ハイハット", () => {
  it("セクションの種類 → hihatPattern の section", () => {
    expect(hatSectionOf("verse")).toBe("verse");
    expect(hatSectionOf("intro")).toBe("verse");
    expect(hatSectionOf("chorus")).toBe("chorus");
    expect(hatSectionOf("drop")).toBe("chorus");
    expect(hatSectionOf("bridge")).toBeUndefined();
    expect(barKindsOf([{ kind: "verse", bars: 2 }, { kind: "chorus", bars: 1 }])).toEqual(["verse", "verse", "chorus"]);
  });
  it("verse は半分に間引き、chorus は 16分に細かく。長さは変わらず、4小節目にオープン", () => {
    const out = applyHihatSections([hatTrack(8)], [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }], 4, "rock")[0];
    expect(sum(out.notes)).toBe(32);
    const barNotes = (bar: number): NoteEvent[] => out.notes.slice(bar * 16, bar * 16 + 16);
    const hits = (ns: NoteEvent[]): number => ns.filter((n) => n.note !== REST).length;
    expect(hits(barNotes(0))).toBe(4); // verse: 4分
    expect(hits(barNotes(5))).toBeGreaterThan(hits(barNotes(0)) * 2); // chorus: 細かい
    expect(barNotes(7).some((n) => n.open)).toBe(true); // 4小節ごとの最後（chorus の型）にオープン
    // hihatPattern と同じ型
    const grid = hihatPattern("rock", 0, "verse");
    expect(barNotes(0).map((n) => (n.note === REST ? "." : "x")).join("")).toBe([...grid].map((c) => (c === "." ? "." : "x")).join(""));
  });
  it("ハイハット以外のパートは変えない。3拍子なら 12マスの小節", () => {
    const k: Track = { waveform: "sine", instrument: "kick", volume: 0.2, notes: [{ note: "C2", durationBeats: 12 }] };
    const out = applyHihatSections([k, hatTrack(4, 3)], [{ kind: "verse", bars: 4 }], 3, "pop");
    expect(out[0]).toBe(k);
    expect(sum(out[1].notes)).toBe(12);
  });
  it("AIソング: hihatBySection: true（drumGenre と sections が要る）", () => {
    const song = { ...ROCK_SONG, autoAccompaniment: true, feel: "rock", human: undefined, swing: undefined, drumGenre: "rock", sections: [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }], parts: [ROCK_SONG.parts[5]] };
    const a = aiSongToScore({ ...song, hihatBySection: true });
    const b = aiSongToScore(song);
    expect(JSON.stringify(a.score.tracks.find((t) => t.instrument === "hihat"))).not.toBe(JSON.stringify(b.score.tracks.find((t) => t.instrument === "hihat")));
    expect(aiSongToScore({ ...song, sections: undefined, hihatBySection: true }).warnings.some((w) => w.includes("hihatBySection"))).toBe(true);
  });
});

describe("トラップのロール自動化", () => {
  it("replaceBeatRange: 範囲だけを置き換え、全体の長さは同じ", () => {
    const base = hatTrack(1).notes;
    const out = replaceBeatRange(base, 3, 4, [{ note: "F#2", durationBeats: 0.5 }, { note: "F#2", durationBeats: 0.5 }]);
    expect(sum(out)).toBe(4);
    expect(out.length).toBe(base.length);
    const cut = replaceBeatRange([{ note: "C2", durationBeats: 2 }], 0.5, 1, [{ note: "D2", durationBeats: 0.5 }]);
    expect(cut.map((n) => [n.note, n.durationBeats])).toEqual([["C2", 0.5], ["D2", 0.5], ["C2", 1]]);
  });
  it("4小節ごとの最後の拍に三連・半拍に32分。中の音は弱く最後は強く。長さは同じ", () => {
    const out = applyTrapRolls([hatTrack(8)], 4)[0];
    expect(sum(out.notes)).toBeCloseTo(32, 6);
    // 4小節目の末尾（拍 15〜16）が三連
    const at = (from: number): NoteEvent[] => { const r: NoteEvent[] = []; let t = 0; for (const n of out.notes) { if (t >= from - 1e-6 && t < from + 1 - 1e-6) r.push(n); t += n.durationBeats; } return r; };
    const first = at(15);
    expect(first.map((n) => n.durationBeats)).toEqual([0.3333, 0.3333, 0.3334]);
    expect(first[2].velocity!).toBeGreaterThan(first[0].velocity!);
    expect(first[2].velocity).toBeCloseTo(78 * 1.3, 1);
    // 8小節目の末尾の半拍は32分（auto は三連と交互）
    expect(out.notes.filter((n) => n.durationBeats === 0.125).length).toBe(4);
  });
  it("every と kind を指定できる。ハイハット以外は変えない", () => {
    const k: Track = { waveform: "sine", instrument: "kick", volume: 0.2, notes: [{ note: "C2", durationBeats: 16 }] };
    const out = applyTrapRolls([k, hatTrack(4)], 4, { every: 2, kind: "triplet" });
    expect(out[0]).toBe(k);
    expect(out[1].notes.filter((n) => n.durationBeats === 0.3334).length).toBe(2);
  });
  it("AIソング: trapRolls: true で自動伴奏と手書きのハイハットの両方に入る。書かなければ入らない", () => {
    const song = { ...ROCK_SONG, human: undefined, swing: undefined, autoAccompaniment: true, feel: "trap", parts: [{ instrument: "hihat", role: "h", volume: 0.1, pan: 0, amp: "auto", notes: "g:x.x.x.x.x.x.x.x." }] };
    const withRolls = aiSongToScore({ ...song, trapRolls: true }).score;
    const without = aiSongToScore(song).score;
    for (const sc of [withRolls, without]) for (const t of sc.tracks) expect(sum(t.notes)).toBeCloseTo(32, 5);
    const rolled = withRolls.tracks.filter((t) => t.instrument === "hihat");
    expect(rolled.length).toBe(2);
    expect(rolled.every((t) => t.notes.some((n) => n.durationBeats === 0.3334))).toBe(true);
    expect(without.tracks.filter((t) => t.instrument === "hihat").some((t) => t.notes.some((n) => n.durationBeats === 0.3334))).toBe(false);
  });
});

describe("ボス曲のフェーズ表", () => {
  it("標準は3段（+0%・+5%・+10%）。フェーズの頭はセクションの頭にそろい、最後の2小節で基準へ戻る", () => {
    expect(BOSS_PHASES.map((p) => p.bpmScale)).toEqual([1, 1.05, 1.1]);
    const sections = [{ kind: "intro" as const, bars: 2 }, { kind: "chorus" as const, bars: 8 }, { kind: "interlude" as const, bars: 4 }, { kind: "chorus" as const, bars: 8 }, { kind: "bridge" as const, bars: 4 }, { kind: "pre" as const, bars: 4 }, { kind: "chorus" as const, bars: 8 }, { kind: "chorus" as const, bars: 8 }];
    const plan = bossPhasePlan(150, 46, 4, sections);
    expect(plan.phases.map((p) => p.label)).toEqual(["第1形態", "第2形態", "最終形態"]);
    const starts = [0, 2, 10, 14, 22, 26, 30, 38];
    for (const p of plan.phases) expect(starts).toContain(p.bar);
    expect(plan.phases.map((p) => p.bpm)).toEqual([150, 157.5, 165]);
    const clock = makeTempoClock(150, plan.tempo);
    expect(clock.bpmAt(plan.phases[1].bar * 4)).toBeCloseTo(157.5, 5);
    expect(clock.bpmAt(plan.phases[2].bar * 4 + 1)).toBeCloseTo(165, 5);
    // 最後の2小節で 150 に戻る（ループの継ぎ目）
    expect(clock.bpmAt(46 * 4 - 0.01)).toBeLessThan(151);
    expect(plan.tempo[plan.tempo.length - 1].ramp).toBe(8);
    expect(bossPhasePlan(150, 46, 4, sections, { loopBack: false }).tempo.some((t) => t.ramp)).toBe(false);
  });
  it("フェーズを小節で指定できる（bar は1始まり）。ほぼ同じ位置のものは重ならない", () => {
    const plan = bossPhasePlan(100, 32, 4, undefined, { phases: [{ bar: 1, bpmScale: 1 }, { bar: 9, bpmScale: 1.2 }, { bar: 10, bpmScale: 1.3 }], loopBack: false });
    expect(plan.phases.map((p) => p.bar)).toEqual([0, 8]);
    expect(plan.tempo).toEqual([{ beat: 32, bpm: 120 }]);
  });
  it("AIソング: bossPhases: true でテンポマップができ、継ぎ目の警告は出ない。曲が少し短くなる", () => {
    const song = { ...ROCK_SONG, human: undefined, swing: undefined, chords: "Am F C G", repeats: 8, autoAccompaniment: true, sections: "auto", parts: [ROCK_SONG.parts[5]], notes: undefined };
    const a = aiSongToScore({ ...song, bossPhases: true });
    expect(a.score.tempoMap!.length).toBeGreaterThan(2);
    expect(a.warnings.some((w) => w.includes("継ぎ目"))).toBe(false);
    const b = aiSongToScore({ ...song, bossPhases: { phases: [{ at: 0, bpmScale: 1 }, { at: 0.5, bpmScale: 1.2 }] } });
    expect(getScoreDurationSec(b.score)).toBeLessThan(getScoreDurationSec(aiSongToScore(song).score));
  });
});
