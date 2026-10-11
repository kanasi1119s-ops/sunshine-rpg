import { describe, expect, it } from "vitest";
import { aiSongToScore, parseNotes } from "./ai-song";
import { scoreToMidi } from "./midi-export";
import { REST, type Score } from "./score";
import { strumVoicing } from "./part-expand";
import { noteNameToMidi } from "./note";

const base = {
  title: "楽器テスト", description: "テスト", bpm: 120, beats: 4, chords: "C G Am F", barsPerChord: 1, repeats: 1,
  autoAccompaniment: false, feel: "rock", tone: "rock",
} as const;
const mk = (parts: unknown[], extra: Record<string, unknown> = {}) => aiSongToScore({ ...base, ...extra, parts });
const total = (t: { notes: { durationBeats: number }[] }): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const starts = (t: Score["tracks"][number]): { note: string; at: number; dur: number; velocity?: number; gate?: number }[] => {
  let at = 0;
  return t.notes.flatMap((n) => { const r = n.note === REST ? [] : [{ note: n.note, at, dur: n.durationBeats, velocity: n.velocity, gate: n.gate }]; at += n.durationBeats; return r; });
};

/** MIDI のコントローラ（0xB0）とノートオンを集める。 */
function midiEvents(bytes: Uint8Array): { tick: number; ch: number; kind: number; d1: number; d2: number }[] {
  const out: { tick: number; ch: number; kind: number; d1: number; d2: number }[] = [];
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
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
      const kind = status & 0xf0;
      if (kind === 0xc0) { p++; continue; }
      out.push({ tick, ch: status & 0x0f, kind, d1: bytes[p], d2: bytes[p + 1] });
      p += 2;
    }
    pos = end;
  }
  return out;
}

describe("ストローク（strum）", () => {
  const strum = { instrument: "guitar", role: "ストローク", volume: 0.14, pan: -0.3, amp: "clean", notes: "", strum: { pattern: "D.DU.UDU" } };
  it("コードフォームの弦ごとのパートに展開され、全部が曲の長さと同じ", () => {
    const { score, warnings } = mk([strum]);
    expect(warnings).toEqual([]);
    expect(score.tracks.length).toBe(5); // C の開放弦フォームは5本
    for (const t of score.tracks) expect(total(t)).toBeCloseTo(16, 5);
  });
  it("1 小節目はダウンで C3 E3 G3 C4 E4 が低い弦から順にずれて鳴る（アップは高い弦だけ）", () => {
    const { score } = mk([strum]);
    const first = score.tracks.map((t) => starts(t)[0]);
    expect(first.map((x) => x.note)).toEqual(["C3", "E3", "G3", "C4", "E4"]);
    expect(first[0].at).toBe(0);
    for (let i = 1; i < first.length; i++) expect(first[i].at).toBeGreaterThan(first[i - 1].at);
    expect(first[4].at).toBeLessThan(0.1);
    expect(first[0].velocity).toBe(1.3); // 拍頭のダウンは強く
    // 最初の U（4 つ目のステップ=1.5 拍）: 低いパートは休み
    expect(starts(score.tracks[0]).some((x) => Math.abs(x.at - 1.5) < 0.05)).toBe(false);
    expect(starts(score.tracks[4]).some((x) => Math.abs(x.at - 1.5) < 0.1 && x.velocity === 0.7)).toBe(true);
  });
  it("コードが変わると音も変わる（C → G → Am → F）", () => {
    const { score } = mk([strum]);
    const g = score.tracks.map((t) => starts(t).find((x) => x.at >= 4 && x.at < 4.2)?.note);
    expect(g.filter(Boolean).map((n) => n!.replace(/\d/, ""))).toEqual(["G", "D", "G", "B", "G"]);
  });
  it("strings で本数、chords で独自の進行、読めないコードは警告", () => {
    expect(mk([{ ...strum, strum: { strings: 3 } }]).score.tracks.length).toBe(3);
    const custom = mk([{ ...strum, strum: { chords: "Em D", bars: 2 } }]).score;
    expect(starts(custom.tracks[0])[0].note).toBe("E2");
    const bad = mk([{ ...strum, strum: { chords: "Xyz" } }]);
    expect(bad.warnings.join()).toContain("Xyz");
    expect(bad.score.tracks.length).toBe(1);
  });
  it("バレーの形（フォームの無いコード）も作れる / 開放弦のフォームはガイドの表どおり", () => {
    expect(strumVoicing("C", 6)).toEqual(["C3", "E3", "G3", "C4", "E4"].map(noteNameToMidi));
    expect(strumVoicing("G", 6)).toEqual(["G2", "B2", "D3", "G3", "B3", "G4"].map(noteNameToMidi));
    expect(strumVoicing("G", 5)).toEqual(["G2", "D3", "G3", "B3", "G4"].map(noteNameToMidi)); // 5度（D）を残す
    const v = strumVoicing("Bm7", 5)!;
    expect(v[0] % 12).toBe(11);
    expect(v.every((m, i) => i === 0 || m > v[i - 1])).toBe(true);
  });
  it("型の文字が不正なら警告して notes のまま", () => {
    const r = mk([{ ...strum, strum: { pattern: "DQ" } }]);
    expect(r.warnings.join()).toContain("pattern");
  });
});

describe("エコー・自動ダブル・detune", () => {
  const lead = { instrument: "lead", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "C5:1 E5:1 G5:2" };
  it("echo: 付点8分ずつ遅れて小さくなるコピー（左右交互・暗く）", () => {
    const { score } = mk([{ ...lead, echo: { repeats: 2 } }]);
    expect(score.tracks.length).toBe(3);
    const [a, e1, e2] = score.tracks;
    expect(starts(e1)[0].at).toBeCloseTo(0.75, 5);
    expect(starts(e2)[0].at).toBeCloseTo(1.5, 5);
    expect(e1.volume).toBeCloseTo(a.volume * 0.3, 2);
    expect(e1.pan).toBeGreaterThan(0);
    expect(e2.pan).toBeLessThan(0);
    expect(e2.bright).toBeCloseTo(-0.4, 5);
    for (const t of score.tracks) expect(total(t)).toBeCloseTo(16, 5);
  });
  it("doubleDetune: 左右 ±0.5、±8 セント。MIDI では別チャンネルで RPN 1 が出る", () => {
    const { score } = mk([{ ...lead, doubleDetune: true }]);
    expect(score.tracks.map((t) => [t.pan, t.detune])).toEqual([[-0.5, -8], [0.5, 8]]);
    const ev = midiEvents(scoreToMidi(score));
    const fine = ev.filter((e) => e.kind === 0xb0 && e.d1 === 100 && e.d2 === 1);
    expect(new Set(fine.map((e) => e.ch)).size).toBe(2);
    const data = ev.filter((e) => e.kind === 0xb0 && e.d1 === 6 && fine.some((f) => f.ch === e.ch && f.tick === e.tick)).map((e) => e.d2);
    expect(Math.min(...data)).toBeLessThan(64);
    expect(Math.max(...data)).toBeGreaterThanOrEqual(64);
  });
  it("attack・release は CC73・CC72 になる", () => {
    const { score } = mk([{ instrument: "pad", role: "パッド", volume: 0.1, pan: 0, amp: "auto", notes: "C3:16", attack: 0.8, release: 0.9 }]);
    const ev = midiEvents(scoreToMidi(score));
    expect(ev.some((e) => e.kind === 0xb0 && e.d1 === 73 && e.d2 === Math.round(0.8 * 127))).toBe(true);
    expect(ev.some((e) => e.kind === 0xb0 && e.d1 === 72 && e.d2 === Math.round(0.9 * 127))).toBe(true);
  });
});

describe("ドローン・リズムの型・音階", () => {
  it("drone: 主音の長い音が曲の長さぴったりになる / root5 は 5 度のパートも", () => {
    const r = mk([{ instrument: "sitar", role: "ドローン", volume: 0.06, pan: 0, amp: "auto", notes: "", drone: "root5" }], { tonic: "D" });
    expect(r.score.tracks.length).toBe(2);
    for (const t of r.score.tracks) expect(total(t)).toBeCloseTo(16, 5);
    expect(r.score.tracks[0].notes[0].note).toBe("D3");
    expect(r.score.tracks[1].notes[0].note).toBe("A3");
  });
  it("drone の主音は、書かなければ最初のコードの根音", () => {
    const r = mk([{ instrument: "pad", role: "ドローン", volume: 0.06, pan: 0, amp: "auto", notes: "", drone: "root" }], { chords: "Am F C G" });
    expect(r.score.tracks[0].notes[0].note).toBe("A2");
  });
  it("pattern: son32 が notes に展開され、taiko2 は 2 つの太鼓になる", () => {
    const r = mk([{ instrument: "tom", role: "クラーベ", volume: 0.1, pan: 0, amp: "auto", notes: "", pattern: "son32" }]);
    const t = r.score.tracks[0];
    expect(total(t)).toBeCloseTo(16, 5);
    expect(starts(t).slice(0, 5).map((x) => x.at)).toEqual([0, 1.5, 3, 5, 6]);
    expect(mk([{ instrument: "tom", role: "太鼓", volume: 0.1, pan: 0, amp: "auto", notes: "", pattern: "taiko2" }]).score.tracks.length).toBe(2);
    expect(mk([{ instrument: "tom", role: "x", volume: 0.1, pan: 0, amp: "auto", notes: "", pattern: "nothing" }]).warnings.join()).toContain("nothing");
    const bell = mk([{ instrument: "bell", role: "鈴", volume: 0.1, pan: 0, amp: "auto", notes: "", pattern: "tresillo", patternNote: "E6" }]).score.tracks[0];
    expect(starts(bell)[0].note).toBe("E6");
  });
  it("scale: 音階外の音に注意が出て、snap で消える。書かなければ出ない", () => {
    const part = { instrument: "koto", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "D4:2 E4:2 G4:2 A4:2 D4:8" };
    expect(mk([part]).warnings).toEqual([]);
    const w = mk([part], { scale: "miyako", tonic: "D" }).warnings;
    expect(w.join()).toContain("都節");
    const snapped = mk([{ ...part, snap: true }], { scale: "miyako", tonic: "D" });
    expect(snapped.warnings.filter((x) => x.includes("外の音"))).toEqual([]);
    expect(parseNotes("E4:2", false, [], "")[0].note).toBe("E4");
    expect(starts(snapped.score.tracks[0])[1].note).toBe("Eb4");
  });
  it("scale の名前が読めなければ警告、scene と合わない音階は注意", () => {
    const part = { instrument: "koto", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "D4:2 G4:2" };
    expect(mk([part], { scale: "nothing" }).warnings.join()).toContain("nothing");
    expect(mk([part], { scale: "miyako", tonic: "D", scene: "battle" }).warnings.join()).toContain("おすすめの音階");
  });
  it("^. は 0.5 半音のベンド", () => {
    expect(parseNotes("E4:2^.", false, [], "")[0].bend).toBe(0.5);
    expect(parseNotes("E4:2^^.", false, [], "")[0].bend).toBe(1.5);
    expect(parseNotes("E4:2^^", false, [], "")[0].bend).toBe(2);
    expect(parseNotes("E4:2/. D4:1\\.", false, [], "").map((n) => [n.scoop, n.fall])).toEqual([[0.5, undefined], [undefined, 0.5]]);
  });
});

describe("奏法・息継ぎ・ペダル・点検", () => {
  it("autoArticulation: 曲全体でも、パートごとの false で止められる", () => {
    const part = { instrument: "leadGuitar", role: "メロディ", volume: 0.2, pan: 0, amp: "auto", notes: "A4:2 R:1 E5:3 R:10" };
    const on = mk([part], { autoArticulation: true }).score.tracks[0];
    expect(on.notes.filter((n) => n.vibrato).length).toBe(2);
    expect(mk([{ ...part, autoArticulation: false }], { autoArticulation: true }).score.tracks[0].notes.some((n) => n.vibrato)).toBe(false);
    expect(mk([part]).score.tracks[0].notes.some((n) => n.vibrato)).toBe(false);
  });
  it("breath: 息継ぎの隙間ができ、点検の警告が消える", () => {
    const part = { instrument: "shakuhachi", role: "尺八", volume: 0.2, pan: 0, amp: "auto", notes: "D4:2 F4:2 G4:2 A4:2 C5:2 A4:2 G4:2 F4:2 D5:2 C5:2 A4:2 G4:2 F4:2 D4:2 F4:2 G4:2" };
    expect(mk([part], { instrumentCheck: true, repeats: 2 }).warnings.join()).toContain("休まず");
    const r = mk([{ ...part, breath: true }], { instrumentCheck: true, repeats: 2 });
    expect(r.warnings.join()).not.toContain("休まず");
    expect(total(r.score.tracks[0])).toBeCloseTo(32, 5);
  });
  it("instrumentCheck: 音域・同時発音の警告が小節番号つきで出る。省略時は出さない", () => {
    const parts = [{ instrument: "shakuhachi", role: "尺八", volume: 0.2, pan: 0, amp: "auto", notes: "D4:4 C4:4 R:8" }];
    expect(mk(parts).warnings).toEqual([]);
    const w = mk(parts, { instrumentCheck: true }).warnings;
    expect(w[0]).toContain("C4");
    expect(w[0]).toContain("2小節目");
  });
  it("pedal: chord はコードの変わり目だけ踏み替え、none は踏まない。省略は 4 拍ごとの従来どおり", () => {
    const part = { instrument: "piano", role: "ピアノ", volume: 0.2, pan: 0, amp: "auto", notes: "C4:16" };
    const pedals = (extra: object): number[] => midiEvents(scoreToMidi(mk([{ ...part, ...extra }], { chords: "C C G G" }).score)).filter((e) => e.kind === 0xb0 && e.d1 === 64 && e.d2 === 127).map((e) => e.tick);
    expect(pedals({})).toEqual([0, 1920, 3840, 5760].map((t) => t)); // 480 × 4拍 = 1920
    expect(pedals({ pedal: "chord" })).toEqual([0, 4 * 2 * 480]);
    expect(pedals({ pedal: "bar" })).toEqual([0, 1920, 3840, 5760]);
    expect(pedals({ pedal: "none" })).toEqual([]);
  });
  it("ピアノ 2 パートの同時に始まる音は、高い方が強くなる（autoArticulation）", () => {
    const r = mk([
      { instrument: "piano", role: "右手", volume: 0.2, pan: 0, amp: "auto", notes: "E5:4" },
      { instrument: "piano", role: "左手", volume: 0.2, pan: 0, amp: "auto", notes: "C3:4" },
    ], { autoArticulation: true });
    expect(r.score.tracks[0].notes[0].velocity).toBe(1.3);
    expect(r.score.tracks[1].notes[0].velocity).toBeUndefined();
  });
  it("コード記法 5 / m7-5 / mmaj7 を chords に書ける", () => {
    expect(() => mk([{ instrument: "kick", role: "k", volume: 0.2, pan: 0, amp: "auto", notes: "x:1" }], { chords: "E5 Bm7-5 Cmmaj7 A5", autoAccompaniment: true })).not.toThrow();
  });
});
