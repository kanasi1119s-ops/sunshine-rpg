import { describe, expect, it } from "vitest";
import { aiSongToScore, parseNotes, AI_SONG_GUIDE, AI_SONG_SCHEMA } from "./ai-song";
import { AI_SONG_EXTRAS_GUIDE } from "./ai-song-extras";
import { bendCurve, glideCurve, scoreToMidi, vibratoCurve } from "./midi-export";
import { REST, type Score, type Track } from "./score";
import { noteNameToMidi } from "./note";
import { applyGhostNotes, applyLegato, capoVoicing, deadNoteName, diatonicShift, expandNoteSugar, figureTokens, STRUM_PRESETS, transposeChordName } from "./guitar-tech";
// @ts-expect-error 型定義のない .mjs（検査ツール）
import { guitarLint, readNotes } from "../../tools/audio-check/guitar-lint.mjs";

const base = {
  title: "ギター奏法テスト", description: "テスト", bpm: 120, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1,
  autoAccompaniment: false, feel: "rock", tone: "rock",
} as const;
const mk = (parts: unknown[], extra: Record<string, unknown> = {}) => aiSongToScore({ ...base, ...extra, parts });
const total = (t: { notes: { durationBeats: number }[] }): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const gt = (over: Record<string, unknown> = {}) => ({ instrument: "guitar", role: "ギター", volume: 0.14, pan: -0.3, amp: "clean", notes: "", ...over });
const starts = (t: Track): { note: string; at: number; dur: number; velocity?: number; gate?: number }[] => {
  let at = 0;
  return t.notes.flatMap((n) => { const r = n.note === REST ? [] : [{ note: n.note, at, dur: n.durationBeats, velocity: n.velocity, gate: n.gate }]; at += n.durationBeats; return r; });
};

/** MIDI から、指定の種類のイベントを（時刻・チャンネル・値1・値2）で取り出す。 */
function events(bytes: Uint8Array, kind: number): { tick: number; ch: number; a: number; b: number }[] {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const out: { tick: number; ch: number; a: number; b: number }[] = [];
  let pos = 14;
  for (let t = 0; t < dv.getUint16(10); t++) {
    const len = dv.getUint32(pos + 4);
    let p = pos + 8;
    const end = p + len;
    let tick = 0;
    while (p < end) {
      let delta = 0, b: number;
      do { b = bytes[p++]; delta = (delta << 7) | (b & 0x7f); } while (b & 0x80);
      tick += delta;
      if (bytes[p] === 0xff) { p += 3 + bytes[p + 2]; continue; }
      const status = bytes[p++];
      const k = status & 0xf0;
      if (k === 0xc0) { p++; continue; }
      if (k === kind) out.push({ tick, ch: status & 15, a: bytes[p], b: bytes[p + 1] });
      p += 2;
    }
    pos = end;
  }
  return out;
}
const bendSemi = (e: { a: number; b: number }): number => (((e.b << 7) | e.a) - 0x2000) / 0x2000 * 12;
const lead = (notes: Track["notes"], extra: Partial<Track> = {}): Score => ({ tempoBpm: 120, loop: false, tracks: [{ waveform: "square", instrument: "leadGuitar", volume: 0.2, pan: 0, notes, ...extra }] });

describe("(1) autoScoop をパート単位に／strum の展開音には掛けない（deep-guide #5）", () => {
  const two = (a: boolean | undefined, b: boolean | undefined): Score => ({
    tempoBpm: 120, loop: false,
    tracks: [
      { waveform: "square", instrument: "guitar", volume: 0.2, pan: -0.5, ...(a !== undefined ? { autoScoop: a } : {}), notes: [{ note: "C4", durationBeats: 1 }, { note: "E4", durationBeats: 2 }] },
      { waveform: "square", instrument: "guitar", volume: 0.2, pan: 0.5, ...(b !== undefined ? { autoScoop: b } : {}), notes: [{ note: "C4", durationBeats: 1 }, { note: "E4", durationBeats: 2 }] },
    ],
  });
  const channelsWithBend = (sc: Score): number[] => [...new Set(events(scoreToMidi(sc), 0xe0).filter((e) => e.a !== 0 || e.b !== 64).map((e) => e.ch))];
  it("Track.autoScoop:false のパートだけしゃくりが無い", () => {
    expect(channelsWithBend(two(false, undefined)).length).toBe(1);
    expect(channelsWithBend(two(undefined, undefined)).length).toBe(2);
    expect(channelsWithBend(two(false, false)).length).toBe(0);
  });
  it("曲が autoScoop:false でも、true のパートだけは付く", () => {
    expect(channelsWithBend({ ...two(true, undefined), autoScoop: false } as Score).length).toBe(1);
  });
  it("パートの autoScoop が Track に渡る", () => {
    const { score } = mk([gt({ notes: "C4:2", autoScoop: false }), gt({ notes: "C4:2", pan: 0.3 })]);
    expect(score.tracks[0].autoScoop).toBe(false);
    expect(score.tracks[1].autoScoop).toBeUndefined();
  });
  it("strum で展開した和音のパートは autoScoop:false（strum.scoop:true で戻す）。MIDI にしゃくりが出ない", () => {
    const { score } = mk([gt({ strum: { pattern: "D...D..." } })]);
    expect(score.tracks.length).toBe(5);
    expect(score.tracks.every((t) => t.autoScoop === false)).toBe(true);
    expect(events(scoreToMidi(score), 0xe0).every((e) => e.a === 0 && e.b === 64)).toBe(true);
    const back = mk([gt({ strum: { pattern: "D...D...", scoop: true } })]).score;
    expect(back.tracks.every((t) => t.autoScoop === undefined)).toBe(true);
    expect(events(scoreToMidi(back), 0xe0).some((e) => e.a !== 0 || e.b !== 64)).toBe(true);
  });
  it("書かない曲は今までと同じ（autoScoop のキーが Track に増えない）", () => {
    const { score } = mk([gt({ notes: "C4:2 E4:2" })]);
    expect("autoScoop" in score.tracks[0]).toBe(false);
  });
});

describe("(2) パワーコード記法（power）", () => {
  it("power:true は根音＋5度の2パート、oct で3パート。音程と長さが合う", () => {
    const { score } = mk([gt({ power: true, notes: "A2:1 C3:0.5 R:0.5" })]);
    expect(score.tracks.length).toBe(2);
    expect(starts(score.tracks[0]).slice(0, 2).map((x) => x.note)).toEqual(["A2", "C3"]);
    expect(starts(score.tracks[1]).slice(0, 2).map((x) => x.note)).toEqual(["E3", "G3"]);
    const oct = mk([gt({ power: "oct", notes: "A2:1" })]).score;
    expect(oct.tracks.length).toBe(3);
    expect(starts(oct.tracks[2])[0].note).toBe("A3");
    expect(mk([gt({ power: true, oct: true, notes: "A2:1" })]).score.tracks.length).toBe(3);
    for (const t of score.tracks) expect(total(t)).toBeCloseTo(16, 5);
  });
  it("休符はそのまま、音量は1パートあたり小さくなる", () => {
    const { score } = mk([gt({ power: true, volume: 0.2, notes: "A2:1 R:1" })]);
    expect(score.tracks[0].volume).toBeCloseTo(0.2 / Math.SQRT2, 2);
    expect(score.tracks[1].notes[1].note).toBe(REST);
  });
  it("ベンドは根音のパートにだけ付く。autoScoop は付かない", () => {
    const { score } = mk([gt({ power: true, notes: "A2:2^^" })]);
    expect(score.tracks[0].notes[0].bend).toBe(2);
    expect(score.tracks[1].notes[0].bend).toBeUndefined();
    expect(score.tracks.every((t) => t.autoScoop === false)).toBe(true);
  });
  it("distGuitar／crunch は書き出しで5度が重なるので展開せず、警告する", () => {
    const r = mk([{ ...gt({ power: true, notes: "A2:1" }), instrument: "distGuitar" }]);
    expect(r.score.tracks.length).toBe(1);
    expect(r.warnings.join()).toContain("power");
  });
});

describe("(3) ギャロップ／トレモロの糖衣・パームミュート", () => {
  it("E2:2@gallop は 1 拍ごとに 0.5! 0.25 0.25 を 2 回", () => {
    expect(expandNoteSugar("E2:2@gallop")).toBe("E2:0.5! E2:0.25 E2:0.25 E2:0.5! E2:0.25 E2:0.25");
    expect(expandNoteSugar("E2:1@rgallop")).toBe("E2:0.25 E2:0.25 E2:0.5!");
    expect(expandNoteSugar("E4:1@trem")).toBe(Array(8).fill("E4:0.125").join(" "));
    expect(expandNoteSugar("E4:1@trem16")).toBe(Array(4).fill("E4:0.25").join(" "));
    expect(expandNoteSugar("R:2@gallop C4:1")).toBe("R:2 C4:1");
    expect(expandNoteSugar("C4:1 D4:1")).toBe("C4:1 D4:1");
  });
  it("端数は最後に1音で埋め、マークは先頭に残る", () => {
    expect(figureTokens("E2", 1.5, "'", "gallop").join(" ")).toBe("E2:0.5'! E2:0.25' E2:0.25' E2:0.5'");
    const sum = figureTokens("E2", 2.75, "", "gallop").map((t) => Number(/:(\d+(?:\.\d+)?)/.exec(t)![1])).reduce((a, b) => a + b, 0);
    expect(sum).toBeCloseTo(2.75, 6);
  });
  it("parseNotes が糖衣を読み、拍の合計が変わらない", () => {
    const err: string[] = [];
    const ev = parseNotes("E2:2@gallop E2:1@trem", false, err, "t");
    expect(err).toEqual([]);
    expect(ev.reduce((s, e) => s + e.durationBeats, 0)).toBeCloseTo(3, 6);
    expect(ev[0].velocity).toBe(1.3);
    expect(ev.length).toBe(6 + 8);
  });
  it("パートの rhythm:\"gallop\" は 1 拍以上の音だけを展開する", () => {
    const { score } = mk([gt({ instrument: "distGuitar", rhythm: "gallop", notes: "E2:2 B2:0.5 E2:1.5" })]);
    const t = score.tracks[0];
    expect(t.notes.slice(0, 3).map((n) => n.durationBeats)).toEqual([0.5, 0.25, 0.25]);
    expect(t.notes.some((n) => n.durationBeats === 0.5 && n.note === "B2")).toBe(true);
    expect(mk([gt({ rhythm: "zzz", notes: "E2:2" })]).warnings.join()).toContain("rhythm");
  });
  it("palmMute: sustain 0.9・bright -0.2（短く切るスタッカートにはしない）", () => {
    const { score } = mk([gt({ palmMute: true, notes: "E2:0.5 E2:0.5" })]);
    expect(score.tracks[0].bright).toBeCloseTo(-0.2, 5);
    expect(score.tracks[0].notes[0].gate).toBe(0.9);
    expect(mk([gt({ palmMute: 0.85, notes: "E2:0.5" })]).score.tracks[0].notes[0].gate).toBe(0.85);
    expect(mk([gt({ palmMute: 1.2, notes: "E2:0.5" })]).score.tracks[0].notes[0].gate).toBeUndefined(); // 上限 1.0（sustain 1 は gate を付けない）
    expect(mk([gt({ palmMute: true, sustain: 1.3, notes: "E2:0.5" })]).score.tracks[0].notes[0].gate).toBe(1.3);
  });
  it("tremolo: 長い音を同音の連なりに。余韻が重なる sustain 1.6", () => {
    const { score } = mk([gt({ tremolo: true, notes: "E4:2 G4:0.5" })]);
    const t = score.tracks[0];
    expect(t.notes.slice(0, 8).every((n) => n.note === "E4" && n.durationBeats === 0.25)).toBe(true);
    expect(t.notes[8].note).toBe("G4");
    expect(t.notes[0].gate).toBe(1.6);
    expect(mk([gt({ tremolo: { rate: 0.125 }, notes: "E4:1" })]).score.tracks[0].notes.length).toBe(16 * 8); // 1 拍＝8音。曲の長さ 16 拍までくり返す
  });
});

describe("(4) strum.pattern の型の名前・アクセント・ゴースト・パームミュート", () => {
  it("名前は pattern・step・strings の既定を持ち、書いた値が優先", () => {
    const skank = mk([gt({ strum: { pattern: "skank" } })]).score;
    expect(skank.tracks.length).toBe(3);
    expect(skank.tracks[2].notes[0].note).toBe(REST);
    expect(skank.tracks[2].notes[0].durationBeats).toBe(0.5);
    expect(skank.tracks[2].notes[1].gate).toBe(0.4); // 型の sustain 0.4（アップは高い弦だけ鳴る）
    expect(mk([gt({ strum: { pattern: "skank", strings: 4 } })]).score.tracks.length).toBe(4);
    expect(mk([gt({ strum: { pattern: "folk6" } })]).score.tracks.length).toBe(6); // G の開放フォームが6本
    expect(mk([gt({ strum: { pattern: "pop" } })]).score.tracks.length).toBe(5);
    expect(mk([gt({ sustain: 2, strum: { pattern: "skank" } })]).score.tracks[2].notes[1].gate).toBe(2);
  });
  it("全部の名前が読めて、曲の長さにそろう", () => {
    for (const name of Object.keys(STRUM_PRESETS)) {
      const r = mk([gt({ strum: { pattern: name } })], name === "waltz" ? { beats: 3, chords: "C G" } : {});
      expect(r.warnings.filter((w) => w.includes("pattern"))).toEqual([]);
      expect(r.score.tracks.length).toBeGreaterThanOrEqual(3);
      const want = name === "waltz" ? 6 : 16;
      for (const t of r.score.tracks) expect(total(t), name).toBeCloseTo(want, 5);
    }
  });
  it("rasgueado は 0.25 拍の連打、bossa は 0.25 拍刻み、funk-cut に g と x が混ざる", () => {
    const ras = mk([gt({ strum: { pattern: "rasgueado" } })]).score.tracks[0];
    expect(ras.notes.slice(0, 4).every((n) => n.durationBeats > 0 && n.durationBeats <= 3.25)).toBe(true);
    const funk = mk([gt({ strum: { pattern: "funk-cut" } })]).score.tracks[0];
    const vels = new Set(funk.notes.filter((n) => n.note !== REST).map((n) => n.velocity));
    expect(vels.has(0.45)).toBe(true); // g
    expect(vels.has(0.7)).toBe(true); // x
  });
  it("知らない名前は警告して notes のまま、DQ のような短い誤りは従来の警告", () => {
    expect(mk([gt({ strum: { pattern: "nanika" } })]).warnings.join()).toContain("nanika");
    expect(mk([gt({ strum: { pattern: "DQ" } })]).warnings.join()).toContain("pattern");
  });
  it("ring（既定）: 低い弦はアップの間も鳴り続け、次に弾くまでのびる。ring:false なら従来どおり1ステップ分", () => {
    const on = starts(mk([gt({ strum: { pattern: "D.DU.UDU" } })], { chords: "C" }).score.tracks[0]);
    // D.（1拍）の低い弦は、次のD（1拍後）の直前まで鳴る
    expect(on[0].dur).toBeGreaterThan(0.9);
    const off = starts(mk([gt({ strum: { pattern: "D.DU.UDU", ring: false } })], { chords: "C" }).score.tracks[0]);
    expect(off[0].dur).toBeLessThanOrEqual(1.01);
  });
  it("> は次の1打のアクセント、m は 7 割に切るパームミュート、g は弱いゴースト", () => {
    // 1 小節ごとに型が頭から始まる。step 0.5: D.(1拍) m D g D = 3拍、残り1拍はくり返しの頭の D
    const { score } = mk([gt({ strum: { pattern: ">D.mDgD" } })], { chords: "C" });
    const t = score.tracks[0];
    const s = starts(t);
    expect(s[0].velocity).toBe(1.3); // アクセント
    expect(s[0].dur).toBeCloseTo(1, 1);
    expect(s[1].velocity).toBe(0.7); // m
    expect(s[1].at).toBeCloseTo(1, 1);
    expect(s[1].dur).toBeCloseTo(0.25, 1); // パームは 0.25 拍に切る（長く伸ばした直後ではなく、短い刻みの中だけ）
    expect(s[2].velocity).toBeUndefined(); // 拍の頭でないダウン
    expect(s[3].velocity).toBe(0.45); // g
    expect(s[3].gate).toBe(0.4);
    expect(t.notes.some((n) => n.note === REST)).toBe(true);
    // 次の1打だけがアクセント
    expect(s[4].velocity).toBeUndefined();
  });
});

describe("(5) デッドノート x", () => {
  it("x:0.25 は直前の音を G3 以下に下げた、弱くて短い dead 音", () => {
    const err: string[] = [];
    const ev = parseNotes("A4:1 x:0.25 x:0.25! x:0.25,", false, err, "t");
    expect(err).toEqual([]);
    expect(ev[1]).toMatchObject({ note: "A2", dead: true, velocity: 0.45, gate: 0.3, durationBeats: 0.25 });
    expect(ev[2].velocity).toBe(0.8);
    expect(ev[3].velocity).toBe(0.3);
    expect(deadNoteName(null)).toBe("E3");
    expect(deadNoteName("C6")).toBe("C3");
    expect(noteNameToMidi(deadNoteName("E2"))).toBeLessThanOrEqual(55);
  });
  it("ドラムの x は今までどおり", () => {
    const ev = parseNotes("x:1 R:1", true, [], "t");
    expect(ev[0].dead).toBeUndefined();
    expect(ev[0].note).toBe("C2");
  });
  it("ghost: 休符の16分の裏にだけ、決まった位置で入る。同じ seed なら同じ", () => {
    const rests = [{ note: "E3", durationBeats: 0.5 }, { note: REST, durationBeats: 3.5 }];
    const a = applyGhostNotes(rests, 1, "s");
    const b = applyGhostNotes(rests, 1, "s");
    expect(a).toEqual(b);
    const d = a.filter((e) => e.dead);
    expect(d.length).toBeGreaterThan(2);
    let at = 0;
    for (const e of a) { if (e.dead) expect([0.25, 0.75, 0.5]).toContain(Math.round((at % 1) * 1000) / 1000); at += e.durationBeats; }
    expect(at).toBeCloseTo(4, 6);
    expect(applyGhostNotes(rests, 0, "s")).toEqual(rests);
  });
  it("パートの ghost が曲に入る（長さは変わらない）", () => {
    const { score } = mk([gt({ ghost: 0.6, notes: "E3:0.5 R:3.5" })]);
    const t = score.tracks[0];
    expect(t.notes.some((n) => n.dead)).toBe(true);
    expect(total(t)).toBeCloseTo(16, 5);
  });
});

describe("(6) ビブラートの深さの段階・ベンドの形・スライド", () => {
  it("~. ＝0.4、~ ＝0.7、~~ ＝1、~~~ ＝1.5", () => {
    const ev = parseNotes("A4:1~. A4:1~ A4:1~~ A4:1~~~ A4:1", false, [], "t");
    expect(ev.map((e) => e.vibrato)).toEqual([0.4, 0.7, 1, 1.5, undefined]);
  });
  it("ベンドの形: ^^@0.25 / /@0.1 / \\@0.5 が読める。範囲外は無視、半音の . も使える", () => {
    const [a, b, c, d] = parseNotes("A4:2^^@0.25 A4:2/@0.1 A4:2^^\\@0.5 A4:2^.@9", false, [], "t");
    expect(a).toMatchObject({ bend: 2, bendT: 0.25 });
    expect(b).toMatchObject({ scoop: 1, scoopT: 0.1 });
    expect(c).toMatchObject({ bend: 2, fall: 1, fallAt: 0.5 });
    expect(d.bend).toBe(0.5);
    expect(d.bendT).toBeUndefined();
  });
  it("bendCurve: bendT で上がる速さ、fallAt で戻り始め、slide で行き先へ。指定なしは今までと同じ", () => {
    const dur = 960;
    const std = bendCurve({ bend: 2 }, dur)!;
    expect(std(240)).toBeCloseTo(2, 5); // 既定: min(35%,0.5拍)=240 ticks で到達
    const fast = bendCurve({ bend: 2, bendT: 0.125 }, dur)!;
    expect(fast(60)).toBeCloseTo(2, 5);
    expect(std(60)).toBeLessThan(1.5);
    const early = bendCurve({ bend: 2, fall: 2, fallAt: 0.4 }, dur)!;
    const late = bendCurve({ bend: 2, fall: 2 }, dur)!;
    expect(early(600)).toBeLessThan(late(600));
    expect(late(100)).toBeGreaterThan(0);
    const sl = bendCurve({ slide: 5 }, dur)!;
    expect(sl(0)).toBeCloseTo(0, 5);
    expect(sl(dur * 0.9)).toBeCloseTo(5, 5);
    expect(bendCurve({}, dur)).toBeNull();
  });
  it("スライド A4:1>D5 は +5 半音。行き先が遠い・同じ音ならエラー", () => {
    const err: string[] = [];
    const ev = parseNotes("A4:1>D5 A4:1_>D5", false, err, "t");
    expect(ev[0].slide).toBe(5);
    expect(ev[1].slide).toBe(5);
    expect(ev[1].gate).toBe(1.15);
    expect(err).toEqual([]);
    const bad: string[] = [];
    parseNotes("A4:1>A4 A4:1>A6", false, bad, "t");
    expect(bad.length).toBe(2);
  });
  it("MIDI: スライドは最後にかけて +5 半音へ、bendT は速く上がる", () => {
    const m = scoreToMidi(lead([{ note: "A4", durationBeats: 1, slide: 5 }]));
    const bends = events(m, 0xe0).map(bendSemi);
    expect(Math.max(...bends)).toBeGreaterThan(4.5);
    const fast = events(scoreToMidi(lead([{ note: "A4", durationBeats: 2, bend: 2, bendT: 0.125 }])), 0xe0);
    const slow = events(scoreToMidi(lead([{ note: "A4", durationBeats: 2, bend: 2 }])), 0xe0);
    const reach = (es: typeof fast): number => es.find((e) => bendSemi(e) > 1.9)!.tick;
    expect(reach(fast)).toBeLessThan(reach(slow));
  });
  it("自前のビブラート: ~~~ はピッチベンドが正弦波に揺れ、CC1 は出さない。~ は今までどおり CC1", () => {
    const wide = scoreToMidi(lead([{ note: "A4", durationBeats: 2, vibrato: 1.5 }]));
    const bends = events(wide, 0xe0).map(bendSemi);
    expect(Math.max(...bends)).toBeGreaterThan(0.2);
    expect(Math.min(...bends)).toBeLessThan(-0.2);
    expect(Math.max(...bends.map(Math.abs))).toBeLessThan(0.45);
    expect(events(wide, 0xb0).filter((e) => e.a === 1 && e.b > 40).length).toBe(0);
    const norm = scoreToMidi(lead([{ note: "A4", durationBeats: 2, vibrato: 0.7 }]));
    expect(events(norm, 0xe0).every((e) => e.a === 0 && e.b === 64 || e.tick < 6)).toBe(true);
    expect(events(norm, 0xb0).some((e) => e.a === 1 && e.b > 40)).toBe(true);
  });
  it("パートの vibrato:{rate,depth,delay} は ~ の音を自前の揺れにする。depth が大きいほど振れる", () => {
    const mkv = (depth: number): number => Math.max(...events(scoreToMidi(lead([{ note: "A4", durationBeats: 3, vibrato: 0.7 }], { vibratoSpec: { rate: 6, depth, delay: 0.2 } })), 0xe0).map((e) => Math.abs(bendSemi(e))));
    expect(mkv(50)).toBeGreaterThan(mkv(15) + 0.1);
    const { score } = mk([gt({ instrument: "leadGuitar", vibrato: { rate: 5, depth: 40, delay: 0.3 }, notes: "A4:2~" })]);
    expect(score.tracks[0].vibratoSpec).toEqual({ rate: 5, depth: 40, delay: 0.3 });
  });
  it("ベンドビブラート: ベンドした音の揺れは、上がりきってから始まり、頂点を中心に揺れる", () => {
    const bv = vibratoCurve({ delay: 0 }, 1920, (rel) => rel / 960, 240);
    expect(bv(100)).toBe(0);
    expect(Math.abs(bv(700))).toBeGreaterThan(0.05);
    const m = scoreToMidi(lead([{ note: "A4", durationBeats: 4, bend: 2, vibrato: 1.5 }]));
    const late = events(m, 0xe0).filter((e) => e.tick > 400 && e.tick < 1700).map(bendSemi);
    expect(Math.min(...late)).toBeGreaterThan(1.4);
    expect(Math.max(...late)).toBeGreaterThan(2.1);
  });
});

describe("グライド（アームの揺れ。rock-guide #8）", () => {
  it("glide は 1 拍以上の音にだけ、ゆっくり不規則なピッチの揺れを作る。ベンドを書いた音・短い音には付かない", () => {
    const tr = (n: Track["notes"][number], glide?: Track["glide"]): Score => lead([n], glide ? { glide } : {});
    const bends = (sc: Score): number[] => events(scoreToMidi(sc), 0xe0).map(bendSemi);
    const g = bends(tr({ note: "A4", durationBeats: 6 }, { depth: 100, rate: 0.5 }));
    expect(Math.max(...g)).toBeGreaterThan(0.3);
    expect(Math.min(...g)).toBeLessThan(-0.3);
    expect(Math.max(...g.map(Math.abs))).toBeLessThan(1.1);
    expect(bends(tr({ note: "A4", durationBeats: 0.5 }, {})).every((b) => Math.abs(b) < 0.01)).toBe(true);
    expect(bends(tr({ note: "A4", durationBeats: 6, bend: 2 }, {})).every((b) => b >= -0.01)).toBe(true);
    expect(bends(tr({ note: "A4", durationBeats: 6 })).every((b) => Math.abs(b) < 0.01)).toBe(true);
    const c = glideCurve({}, 2880, (rel) => rel / 960, 1);
    expect(c(0)).toBeCloseTo(0, 5);
  });
  it("パートの glide が Track に渡る（true は既定値）", () => {
    expect(mk([gt({ glide: { depth: 80, rate: 0.3 }, notes: "A4:4" })]).score.tracks[0].glide).toEqual({ depth: 80, rate: 0.3 });
    expect(mk([gt({ glide: true, notes: "A4:4" })]).score.tracks[0].glide).toEqual({});
  });
});

describe("(7) スウェル記号と attack の自動", () => {
  it("< > はスウェル、MIDI の CC11 が立ち上がる／減る。human の山とは重ならない", () => {
    const ev = parseNotes("E4:4< E4:4>", false, [], "t");
    expect(ev.map((e) => e.swell)).toEqual([1, -1]);
    const up = events(scoreToMidi(lead([{ note: "E4", durationBeats: 4, swell: 1 }])), 0xb0).filter((e) => e.a === 11).map((e) => e.b);
    expect(up[0]).toBeLessThan(40);
    expect(Math.max(...up)).toBe(127);
    const down = events(scoreToMidi(lead([{ note: "E4", durationBeats: 4, swell: -1 }])), 0xb0).filter((e) => e.a === 11).map((e) => e.b);
    expect(down[0]).toBe(127);
    expect(Math.min(...down)).toBeLessThan(60);
    expect(down[down.length - 1]).toBe(127);
    expect(events(scoreToMidi(lead([{ note: "E4", durationBeats: 4 }])), 0xb0).filter((e) => e.a === 11).length).toBe(0);
  });
  it("swell:true は 1 拍以上の音に < を付け、attack を 0.7 にする（書いた attack・< > は尊重）", () => {
    const { score } = mk([gt({ instrument: "leadGuitar", swell: true, notes: "E4:2 G4:0.5 B4:2> D5:1" })]);
    const t = score.tracks[0];
    expect(t.attack).toBe(0.7);
    expect(t.notes.slice(0, 4).map((n) => n.swell)).toEqual([1, undefined, -1, 1]);
    expect(mk([gt({ swell: true, attack: 0.4, notes: "E4:2" })]).score.tracks[0].attack).toBe(0.4);
    expect(mk([gt({ swell: 3, notes: "E4:2 E4:3" })]).score.tracks[0].notes.slice(0, 2).map((n) => n.swell)).toEqual([undefined, 1]);
  });
});

describe("(9) capo・fingerpick・ハーモナイザ", () => {
  it("コード名のずらし: 鳴る和音 → カポの分だけ下げた形", () => {
    expect(transposeChordName("D", -2)).toBe("C");
    expect(transposeChordName("Am7", -2)).toBe("Gm7");
    expect(transposeChordName("A/C#", -2)).toBe("G/B");
    expect(transposeChordName("Xyz", -2)).toBeNull();
  });
  it("capoVoicing: D をカポ2で＝C の開放フォームを +2。カポ0は strum と同じ", () => {
    expect(capoVoicing("D", 5, 2)).toEqual([N("C3") + 2, N("E3") + 2, N("G3") + 2, N("C4") + 2, N("E4") + 2]);
    expect(capoVoicing("C", 5, 0)).toEqual([N("C3"), N("E3"), N("G3"), N("C4"), N("E4")]);
    expect(capoVoicing("Q", 5, 2)).toBeNull();
  });
  function N(s: string): number { return noteNameToMidi(s); }
  it("strum の capo（strum.capo／パートの capo）: 鳴る音は同じ和音の構成音のまま、押さえる形が変わる", () => {
    const sc = mk([gt({ strum: { pattern: "D...", chords: "D", capo: 2 } })], { chords: "D" }).score;
    const first = sc.tracks.map((t) => starts(t)[0].note);
    expect(first).toEqual(["D3", "F#3", "A3", "D4", "F#4"]);
    const viaPart = mk([gt({ capo: 2, strum: { pattern: "D...", chords: "D" } })], { chords: "D" }).score;
    expect(viaPart.tracks.map((t) => starts(t)[0].note)).toEqual(first);
    // カポなしの D は D3 A3 D4 F#4 の4本
    expect(mk([gt({ strum: { pattern: "D...", chords: "D" } })], { chords: "D" }).score.tracks.length).toBe(4);
  });
  it("fingerpick travis: 親指と指の2パート、拍ごとに低音が交互。長さは曲と同じ", () => {
    const { score, warnings } = mk([gt({ fingerpick: { pattern: "travis" } })]);
    expect(warnings).toEqual([]);
    expect(score.tracks.length).toBe(2);
    for (const t of score.tracks) expect(total(t)).toBeCloseTo(16, 5);
    const thumb = starts(score.tracks[0]);
    expect(thumb.slice(0, 2).map((x) => x.note)).toEqual(["C3", "E3"]); // p=最低音、q=2番目
    expect(thumb[0].at).toBe(0);
    expect(thumb[1].at).toBe(1);
    const fingers = starts(score.tracks[1]);
    expect(fingers[0].at).toBe(0.5);
    expect(score.tracks.every((t) => t.autoScoop === false)).toBe(true);
  });
  it("fingerpick: カスタム型・chords・capo・誤りの警告", () => {
    const custom = mk([gt({ fingerpick: { pattern: "p-i-m-a-", step: 0.5, chords: "Am F", bars: 2, capo: 0 } })]).score;
    expect(custom.tracks.length).toBe(2);
    expect(mk([gt({ fingerpick: { pattern: "zzz" } })]).warnings.join()).toContain("fingerpick");
    expect(mk([gt({ fingerpick: { pattern: "bossaThumb" } })]).score.tracks.length).toBe(1); // 親指だけ
    const capo2 = mk([gt({ fingerpick: { pattern: "pima", chords: "D", capo: 2 } })], { chords: "D" }).score;
    expect(starts(capo2.tracks[0])[0].note).toBe("D3");
  });
  it("diatonicShift: 音階の音だけで3度下／上", () => {
    const aeol = [4, 6, 7, 9, 11, 0, 2]; // E ナチュラルマイナー
    expect(diatonicShift(noteNameToMidi("G4"), -2, aeol)).toBe(noteNameToMidi("E4")); // G の3度下は E
    expect(diatonicShift(noteNameToMidi("A4"), -2, aeol)).toBe(noteNameToMidi("F#4"));
    expect(diatonicShift(noteNameToMidi("B4"), 2, aeol)).toBe(noteNameToMidi("D5"));
    expect(diatonicShift(noteNameToMidi("A#4"), -2, aeol)).toBe(noteNameToMidi("F#4")); // 音階外は近い音（下）へそろえてから
  });
  it("harmonize: 3度下のパートが自動で増え、元のパートと同じ長さ。マイナーで半音のずれが出ない", () => {
    const { score, warnings } = mk([{ ...gt({ instrument: "lead", role: "メロディ", pan: 0.2, harmonize: { interval: -3, scale: "minor@E" }, notes: "G4:1 A4:1 B4:2 E5:4" }) }]);
    expect(warnings).toEqual([]);
    expect(score.tracks.length).toBe(2);
    expect(starts(score.tracks[1]).slice(0, 4).map((x) => x.note)).toEqual(["E4", "F#4", "G4", "C5"]);
    expect(score.tracks[1].volume).toBeLessThan(score.tracks[0].volume);
    expect(total(score.tracks[1])).toBeCloseTo(16, 5);
  });
  it("harmonize: 曲の scale を使う／度数が範囲外・音階なしは警告", () => {
    const withSong = mk([gt({ instrument: "lead", harmonize: { interval: 3 }, notes: "E4:1" })], { scale: "minor", tonic: "E" });
    expect(starts(withSong.score.tracks[1])[0].note).toBe("G4");
    expect(mk([gt({ instrument: "lead", harmonize: { interval: 1 }, notes: "E4:1" })], { scale: "minor", tonic: "E" }).warnings.join()).toContain("interval");
    expect(mk([gt({ instrument: "lead", harmonize: true, notes: "E4:1" })]).warnings.join()).toContain("scale");
  });
});

describe("そのほかの提案: unison bend・mask・legato・gtrStyle", () => {
  it("ユニゾンベンド D5:3u(E5): D5 を全音ベンドし、E5 を弾く別パートを作る（ベンド量は自動で合わせる）", () => {
    const { score } = mk([gt({ instrument: "leadGuitar", notes: "D5:3!u(E5) R:1" })]);
    expect(score.tracks.length).toBe(2);
    expect(score.tracks[0].notes[0]).toMatchObject({ note: "D5", bend: 2, velocity: 1.3 });
    expect(score.tracks[1].notes[0]).toMatchObject({ note: "E5", durationBeats: 3 });
    expect(score.tracks[1].notes[0].bend).toBeUndefined();
    const mismatch = mk([gt({ instrument: "leadGuitar", notes: "D5:3^u(E5)" })]);
    expect(mismatch.warnings.join()).toContain("食い違");
    expect(mismatch.score.tracks[0].notes[0].bend).toBe(2);
    expect(mk([gt({ instrument: "leadGuitar", notes: "D5:3u(A5)" })]).warnings.join()).toContain("ユニゾン");
  });
  it("mask: 相手が鳴っている間は消え、休符だけ残る。鳴り始めの前で切る。gain>0 なら弱く残す", () => {
    const vocal = { instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "C5:2 R:2 C5:1 R:3" };
    const oblig = gt({ instrument: "leadGuitar", role: "合いの手", mask: "メロディ", notes: "E4:1 E4:1 E4:1 E4:1" });
    const { score } = mk([vocal, oblig], { chords: "C", repeats: 2 });
    const g = score.tracks[1];
    const s = starts(g);
    expect(s.map((x) => x.at)).toEqual([2, 3, 5, 6, 7]); // 0〜2 と 4〜5 は相手が鳴るので消える
    expect(total(g)).toBeCloseTo(8, 5);
    const soft = mk([vocal, { ...oblig, mask: { role: "メロディ", gain: 0.5 } }], { chords: "C", repeats: 2 }).score.tracks[1];
    expect(soft.notes.some((n) => n.velocity === 0.45)).toBe(true);
    expect(mk([oblig], { chords: "C" }).warnings.join()).toContain("mask");
  });
  it("legato: 0.25 拍以下の3音以上を _ でつなぎ、山なりに。強さを書いた音・2音以下は変えない", () => {
    const ev = [0, 1, 2, 3, 4].map((i) => ({ note: "C4", durationBeats: 0.25, ...(i === 2 ? { velocity: 0.9 } : {}) }));
    const out = applyLegato([...ev, { note: "D4", durationBeats: 1 }]);
    expect(out.slice(0, 4).every((e) => e.gate === 1.15)).toBe(true);
    expect(out[4].gate).toBeUndefined();
    expect(out[2].velocity).toBe(0.9);
    expect(out[0].velocity).toBe(1.2);
    expect(applyLegato([ev[0], ev[1]]).every((e) => e.gate === undefined)).toBe(true);
    const { score } = mk([gt({ legato: true, notes: "C4:0.25 D4:0.25 E4:0.25 F4:0.25 G4:1" })]);
    expect(score.tracks[0].notes[0].gate).toBe(1.15);
  });
  it("gtrStyle: 既定を入れる（書いた値が優先）。知らない名前は警告", () => {
    const { score } = mk([gt({ instrument: "distGuitar", amp: "auto", gtrStyle: "melocore", notes: "E2:1" })]);
    expect(score.tracks.length).toBe(2); // doubleDetune の L／R
    expect(score.tracks[0].amp?.type).toBe("loudrock");
    expect(mk([gt({ instrument: "distGuitar", gtrStyle: "melocore", amp: "crunch", notes: "E2:1" })]).score.tracks[0].amp?.type).toBe("crunch");
    const thrash = mk([gt({ instrument: "distGuitar", amp: "auto", gtrStyle: "thrash", notes: "E2:1" })]).score;
    expect(thrash.tracks[0].notes[0].gate).toBe(0.9);
    expect(mk([gt({ gtrStyle: "nanika", notes: "E2:1" })]).warnings.join()).toContain("gtrStyle");
  });
  it("禁止の音（banned-sounds.md）の作り方を、型に入れていない", () => {
    for (const [name, st] of Object.entries(GTR_STYLES_FOR_TEST())) {
      expect(["hardrock", "punk"], name).not.toContain(st.amp);
    }
  });
});
function GTR_STYLES_FOR_TEST(): Record<string, { amp?: string }> {
  const out: Record<string, { amp?: string }> = {};
  for (const name of ["melocore", "thrash", "shoegaze", "funkCut", "ballad", "bossa"]) {
    out[name] = { amp: mk([gt({ instrument: "distGuitar", amp: "auto", gtrStyle: name, notes: "E2:1" })]).score.tracks[0].amp?.type };
  }
  return out;
}

describe("既存の動き・スキーマ・ガイド", () => {
  it("糖衣・x・新しい記号のない notes は、今までと同じ結果（記号の追加で変わらない）", () => {
    const ev = parseNotes("E5:1! D5:0.5, R:0.5 C5:2_ A4:2^^~ G4:1/ F4:1\\ E4:1^.", false, [], "t");
    expect(ev.map((e) => [e.velocity, e.gate, e.bend, e.scoop, e.fall, e.vibrato])).toEqual([
      [1.3, undefined, undefined, undefined, undefined, undefined],
      [0.7, undefined, undefined, undefined, undefined, undefined],
      [undefined, undefined, undefined, undefined, undefined, undefined],
      [undefined, 1.15, undefined, undefined, undefined, undefined],
      [undefined, undefined, 2, undefined, undefined, 0.7],
      [undefined, undefined, undefined, 1, undefined, undefined],
      [undefined, undefined, undefined, undefined, 1, undefined],
      [undefined, undefined, 0.5, undefined, undefined, undefined],
    ]);
    for (const e of ev) { expect(e.dead).toBeUndefined(); expect(e.swell).toBeUndefined(); expect(e.slide).toBeUndefined(); expect(e.bendT).toBeUndefined(); }
  });
  it("スキーマに新しい項目があり、ガイドに説明がある", () => {
    const props = (AI_SONG_SCHEMA.properties.parts.items.properties as Record<string, unknown>);
    for (const k of ["power", "oct", "palmMute", "tremolo", "rhythm", "swell", "legato", "ghost", "harmonize", "fingerpick", "capo", "mask", "gtrStyle", "vibrato", "glide", "autoScoop"]) expect(props[k], k).toBeDefined();
    const guide = AI_SONG_GUIDE + AI_SONG_EXTRAS_GUIDE;
    for (const w of ["power", "@gallop", "palmMute", "x:0.25", "skank", "fingerpick", "capo", "harmonize", "mask", "~~~", "^^@0.25", "A4:1>D5", "u(E5)", "swell", "legato", "gtrStyle", "glide", "autoScoop"]) expect(guide, w).toContain(w);
  });
});

describe("検査（guitar-lint。解析だけ）", () => {
  const solo = (notes: string, extra: Record<string, unknown> = {}) => ({
    title: "t", bpm: 100, beats: 4, chords: "Am F C G", barsPerChord: 2, repeats: 1, ...extra,
    parts: [{ instrument: "leadGuitar", role: "ギターソロ", volume: 0.1, pan: 0, amp: "lead", notes }],
  });
  const msgs = (song: unknown): string => guitarLint(song).map((r: { msg: string }) => r.msg).join("\n");
  const warns = (song: unknown): string[] => guitarLint(song).filter((r: { level: string }) => r.level === "warn").map((r: { msg: string }) => r.msg);
  // 16 小節: 詰め込み（休符なし）・最高音が前半に3回・全音に ~
  const packed = Array.from({ length: 32 }, (_, i) => `${["A5", "C5", "E5", "D5"][i % 4]}:1~`).join(" ");
  it("ソロ: 休符なし・頂点が前半・~ の過多を警告する", () => {
    const w = warns(solo(packed)).join("\n");
    expect(w).toContain("休符");
    expect(w).toContain("最高音");
    expect(w).toContain("~");
  });
  it("ソロ: 休符があり、頂点が後ろに1回で、~ が少ない設計は通る", () => {
    const good = "A4:2 R:1 C5:1 D5:1 R:1 E5:2~ R:1 C5:1 D5:2 R:2 E5:1 G5:1 R:2 C5:2 E5:2 R:2 G5:2 A5:3~~ R:1 E5:4\\";
    const w = warns(solo(good));
    expect(w.filter((x) => x.includes("休符") || x.includes("最高音"))).toEqual([]);
  });
  it("表現の過多: 短い音の ~・^、全音に ~、同じ深さの ~ の連続、autoArticulation との重複", () => {
    const song = solo("A4:0.25~ B4:0.125^^ C5:1~ D5:1~ E5:1~ F5:1~ G5:1~ A5:1~ C5:1~", { autoArticulation: true });
    const w = warns(song).join("\n");
    expect(w).toContain("0.4拍未満");
    expect(w).toContain("0.25拍未満の音に ^");
    expect(w).toContain("同じ深さの ~");
    expect(w).toContain("autoArticulation");
    expect(w).toContain("ほぼ全部");
  });
  it("表現の過多: ストロークの自動しゃくり（strum.scoop:true）と、1拍以上の長音への自動しゃくり", () => {
    const strum = { title: "t", bpm: 100, beats: 4, chords: "C G", barsPerChord: 1, repeats: 1, parts: [{ instrument: "guitar", role: "s", volume: 0.1, pan: 0, amp: "clean", notes: "", strum: { scoop: true } }] };
    expect(warns(strum).join()).toContain("strum.scoop");
    const longs = { ...strum, parts: [{ instrument: "guitar", role: "g", volume: 0.1, pan: 0, amp: "clean", notes: Array(8).fill("E4:2").join(" ") }] };
    expect(warns({ ...longs, chords: "C G Am F" }).join()).toContain("自動しゃくり");
    expect(warns({ ...longs, chords: "C G Am F", autoScoop: false }).join()).not.toContain("自動しゃくり");
  });
  it("表現の過多: スタッカートの同音連打（禁止の音）は警告、ギャロップの糖衣は警告しない", () => {
    const stacc = solo("A4:0.25' A4:0.25' A4:0.25' A4:0.25' A4:0.25' R:3");
    expect(warns(stacc).join()).toContain("同音の連打");
    const gal = { ...solo("E2:2@gallop R:2"), parts: [{ instrument: "distGuitar", role: "刻み", volume: 0.07, pan: 0, amp: "loudmetal", notes: "E2:2@gallop R:2" }] };
    expect(warns(gal).join()).not.toContain("同音の連打");
  });
  it("音域: 歪みの刻みが A3 超、リードの C6 超の長音、リズムギターが C4〜B4 でメロディとぶつかる", () => {
    const song = {
      title: "t", bpm: 100, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1,
      parts: [
        { instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "C5:4" },
        { instrument: "distGuitar", role: "刻み", volume: 0.07, pan: 0, amp: "loudrock", notes: "C4:1 E4:1 G4:1 C4:1" },
        { instrument: "leadGuitar", role: "リード", volume: 0.1, pan: 0, amp: "lead", notes: "D6:2 R:2" },
        { instrument: "guitar", role: "伴奏", volume: 0.1, pan: 0, amp: "clean", notes: "E4:1 G4:1 B4:1 E4:1" },
      ],
    };
    const w = warns(song).join("\n");
    expect(w).toContain("A3 より高い");
    expect(w).toContain("C6 より高い");
    expect(w).toContain("C4〜B4");
    const ok = { ...song, parts: [{ instrument: "distGuitar", role: "刻み", volume: 0.07, pan: 0, amp: "loudrock", notes: "E2:1 A2:1 E3:1 A2:1" }] };
    expect(warns(ok)).toEqual([]);
  });
  it("readNotes: 糖衣・デッドノート・休符を読む", () => {
    const { notes, total: tot } = readNotes("E2:1@gallop x:0.25 R:0.75");
    expect(notes.length).toBe(5);
    expect(tot).toBeCloseTo(2, 6);
    expect(notes[3].dead).toBe(true);
    expect(msgs({ title: "t", chords: "C", parts: [] })).toBe("");
  });
});
