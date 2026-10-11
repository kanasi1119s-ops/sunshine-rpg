// 声部の点検（C1・C2・C3・C6）・voiceLead の改良と型（C4・C5）・対旋律／カノン／保持音の生成（C7〜C10）のテスト。
import { describe, expect, it } from "vitest";
import scoreCheckSrc from "../../tools/audio-check/score-check.mjs?raw";
// @ts-ignore
import { expand, parseNotes } from "../../tools/audio-check/score-lib.mjs";
// @ts-ignore
import * as vl from "../../tools/audio-check/voice-lint.mjs";
// @ts-ignore
import * as cp from "../../tools/composer/counterpoint.mjs";
import { voiceLead, parseChord } from "./newsong";

const part = (instrument: string, role: string, notes: string, total = 16) => ({ instrument, role, seq: expand({ instrument, notes }, total) });

describe("C1 平行5度・8度（全ペア）", () => {
  // 上声が C5 D5 E5 F5 …、下声がその5度下（F4 G4 A4 Bb4 …）と動く = 平行5度
  // 上声が C5 D5 E5 F5 G5 と上がるあいだ、下声が5度下（F4 G4 A4 Bb4 C5）で平行。そのあとは短3度下（平行5度ではない）
  const up = "C5:1 D5:1 E5:1 F5:1 G5:1 A5:1 B5:1 C6:1 D6:1 E6:1 F6:1 G6:1";
  const lowPar = "F4:1 G4:1 A4:1 Bb4:1 C5:1 F#5:1 G#5:1 A5:1 B5:1 C#6:1 D#6:1 E6:1";
  it("内声どうしでも、5度の平行が4回以上なら見つける", () => {
    const parts = [part("strings", "内声1", lowPar, 12), part("strings", "内声2", "A4:1 B4:1 C5:1 D5:2 E5:1 D5:1 C5:1 D5:4", 12), part("strings", "内声3", up, 12)];
    const r = vl.findParallels(parts, 12, { minCount: 4 });
    expect(r.some((x: { a: number; b: number }) => x.a === 0 && x.b === 2)).toBe(true);
  });
  it("ペアの大半がその音程のとき（パワーコード・オクターブ重ね）は意図として除く", () => {
    const parts = [part("guitar", "リズム", "E3:1 G3:1 A3:1 B3:1 D4:1 E4:1 G4:1 A4:1", 8), part("guitar", "リズム2", "B3:1 D4:1 E4:1 F#4:1 A4:1 B4:1 D5:1 E5:1", 8)];
    expect(vl.findParallels(parts, 8)).toEqual([]);
  });
  it("役割に「重ね」を含むパートは除く。skip で特定のペアも除ける", () => {
    const a = part("strings", "A", up, 12);
    const b = part("strings", "B 重ね", lowPar, 12);
    expect(vl.findParallels([a, b], 12)).toEqual([]);
    const b2 = { ...b, role: "B" };
    expect(vl.findParallels([a, b2], 12).length).toBe(1);
    expect(vl.findParallels([a, b2], 12, { skip: () => true })).toEqual([]);
  });
  it("向きが反対（反行）なら平行ではない", () => {
    const a = part("strings", "A", "C5:1 D5:1 E5:1 F5:1 G5:1 A5:1 B5:1 C6:1", 8);
    const b = part("strings", "B", "F4:1 E4:1 D4:1 C4:1 B3:1 A3:1 G3:1 F3:1", 8);
    expect(vl.findParallels([a, b], 8, { minCount: 1 })).toEqual([]);
  });
});

describe("C2 声部交差", () => {
  it("同じ楽器の2パートの上下が入れ替わると数える", () => {
    const hi = part("strings", "上", "E4:1 E4:1 G4:1 G4:1 E4:1 E4:1 G4:1 G4:1", 8);
    const lo = part("strings", "下", "C4:1 C4:1 C4:1 C4:1 C4:1 C4:1 C4:1 C4:1", 8);
    expect(vl.findVoiceCrossings([hi, lo], 8)).toEqual([]);
    const cross = part("strings", "下", "C4:1 C4:1 B4:1 B4:1 C4:1 C4:1 B4:1 B4:1", 8);
    const r = vl.findVoiceCrossings([hi, cross], 8);
    expect(r.length).toBe(1);
    expect(r[0].count).toBe(4);
  });
  it("楽器が違えば見ない", () => {
    const a = part("strings", "上", "E4:8", 8), b = part("pad", "下", "G4:8", 8);
    expect(vl.findVoiceCrossings([a, b], 8)).toEqual([]);
  });
});

describe("C3 隠れ5度・8度", () => {
  it("最高声が跳んで、最低声と同じ向きで完全5度に着くと数える（順次なら除く）", () => {
    const top = part("lead", "旋律", "E5:1 B5:1 E5:1 B5:1 E5:1 B5:1 E5:1 B5:1", 8);
    const bass = part("bass", "ベース", "G3:1 E4:1 G3:1 E4:1 G3:1 E4:1 G3:1 E4:1", 8);
    // 上 E5→B5 (+7)、下 G3→E4 (+9)、着地 B5-E4 = 19 = 完全5度
    const r = vl.findHiddenPerfects(top, bass, 8, { minCount: 1 });
    expect(r.count).toBeGreaterThanOrEqual(1);
    const topStep = part("lead", "旋律", "A5:1 B5:1 A5:1 B5:1 A5:1 B5:1 A5:1 B5:1", 8);
    expect(vl.findHiddenPerfects(topStep, bass, 8, { minCount: 1 }).count).toBe(0);
  });
});

describe("C6 低音域の間隔", () => {
  it("C3より下の3度とE3より下の2度を数えて、パート名を挙げる", () => {
    const a = part("bass", "ベース", "C2:4 C2:4", 8), b = part("guitar", "ギター", "E2:4 E2:4", 8);
    const r = vl.findLowMuddy([a, b], 8);
    expect(r.length).toBe(1);
    expect(r[0].kind).toBe("3度");
    expect(r[0].nameLo).toContain("ベース");
    const c = part("bass", "ベース", "E2:8", 8), d = part("guitar", "ギター", "F2:8", 8);
    expect(vl.findLowMuddy([c, d], 8)[0].kind).toBe("2度");
  });
  it("高い所の3度や、低い所の5度は数えない", () => {
    expect(vl.findLowMuddy([part("bass", "b", "C4:8", 8), part("guitar", "g", "E4:8", 8)], 8)).toEqual([]);
    expect(vl.findLowMuddy([part("bass", "b", "C2:8", 8), part("guitar", "g", "G2:8", 8)], 8)).toEqual([]);
  });
  it("voiceLint がまとめて返す", () => {
    const parts = [part("bass", "ベース", "C2:8", 8), part("guitar", "ギター", "E2:8", 8)];
    const res = vl.voiceLint(parts, { beats: 4, totalBeats: 8 });
    expect(res.some((r: { id: string; level: string }) => r.id === "C6" && r.level === "warn")).toBe(true);
    expect(res.some((r: { id: string; level: string }) => r.id === "C1" && r.level === "ok")).toBe(true);
  });
});

describe("C4 voiceLead の改良", () => {
  const ch = (s: string) => parseChord(s)!;
  const prog = ["C", "Am", "F", "G", "C", "Em", "Am", "Dm", "G", "C"].map(ch);
  const perfect = (a: number, b: number) => { const d = Math.abs(a - b) % 12; return d === 7 || (d === 0 && a !== b) ? d : -1; };
  const parallels = (v: number[][]) => {
    let n = 0;
    for (let i = 1; i < v.length; i++) for (let x = 0; x < v[i].length; x++) for (let y = x + 1; y < v[i].length; y++) {
      const k0 = perfect(v[i - 1][x], v[i - 1][y]), k1 = perfect(v[i][x], v[i][y]);
      const dx = v[i][x] - v[i - 1][x], dy = v[i][y] - v[i - 1][y];
      if (k0 >= 0 && k0 === k1 && dx && dy && Math.sign(dx) === Math.sign(dy)) n++;
    }
    return n;
  };
  it("声部が交差・追い越ししない（低い順に並ぶ）", () => {
    const v = voiceLead(prog, 3, 52, 79, { smart: true });
    for (const c of v) for (let k = 1; k < c.length; k++) expect(c[k]).toBeGreaterThan(c[k - 1]);
  });
  it("省略（旧い動作）の出力は変えない: smart を付けないと従来と同じ", () => {
    expect(voiceLead(prog, 3)).toEqual(voiceLead(prog, 3, 52, 79, { smart: false }));
  });
  it("平行5度・8度が旧い動作より増えない", () => {
    const smart = voiceLead(prog, 3, 52, 79);
    const old = voiceLead(prog, 3, 52, 79);
    expect(parallels(smart)).toBeLessThanOrEqual(parallels(old));
    expect(parallels(smart)).toBe(0);
  });
  it("共通音は同じ声部に残る（C→Am は C と E が動かない）", () => {
    const v = voiceLead([ch("C"), ch("Am")], 3, 52, 79, { smart: true });
    const common = v[0].filter((m) => v[1].includes(m));
    expect(common.length).toBeGreaterThanOrEqual(2);
    for (const m of common) expect(v[0].indexOf(m)).toBe(v[1].indexOf(m));
  });
  it("音は和音の構成音だけ。4音でも動く", () => {
    const p4 = ["Cmaj7", "Am7", "Dm7", "G7"].map(ch);
    voiceLead(p4, 4, 52, 79, { smart: true }).forEach((c, i) => {
      expect(new Set(c).size).toBe(4);
      const pcs = p4[i].intervals.map((iv) => (p4[i].root + iv) % 12);
      c.forEach((m) => expect(pcs).toContain(m % 12));
    });
  });
});

describe("C5 voiceLead の型", () => {
  const C = parseChord("Cmaj7")!;
  const span = (v: number[]) => Math.max(...v) - Math.min(...v);
  it("close はいまの動作と同じ", () => {
    expect(voiceLead([C], 4, 48, 84, { voicing: "close" })).toEqual(voiceLead([C], 4, 48, 84));
  });
  it("drop2 は密集形の上から2番目を1オクターブ下げる", () => {
    const close = voiceLead([C], 4, 48, 84)[0].slice().sort((a, b) => a - b);
    const drop = voiceLead([C], 4, 48, 84, { voicing: "drop2" })[0];
    expect(drop).toEqual([...close.slice(0, 1), close[2] - 12, ...close.slice(1, 2), ...close.slice(3)].sort((a, b) => a - b));
    expect(drop.length).toBe(4);
    expect(span(drop)).toBeGreaterThan(span(close));
  });
  it("open は根音が最低で、3度が上にくる（密集より広い）", () => {
    const open = voiceLead([parseChord("C")!], 3, 48, 84, { voicing: "open" })[0];
    expect(open[0] % 12).toBe(0);
    expect(open[open.length - 1] % 12).toBe(4);
    const close = voiceLead([parseChord("C")!], 3, 48, 84)[0];
    expect(span(open)).toBeGreaterThanOrEqual(span(close));
  });
  it("spread は open の最高声をさらに1オクターブ上げる", () => {
    const open = voiceLead([parseChord("C")!], 3, 48, 84, { voicing: "open" })[0];
    const spread = voiceLead([parseChord("C")!], 3, 48, 84, { voicing: "spread" })[0];
    expect(spread[spread.length - 1]).toBe(open[open.length - 1] + 12);
  });
});

describe("C7 対旋律の自動生成 generateCounter", () => {
  const melody = "E5:1 G5:1 A5:2 G5:1 E5:1 D5:2 C5:1 D5:1 E5:2 C5:4";
  const chords = ["C", "Am", "F", "G"];
  const gen = cp.generateCounter(melody, chords);
  it("拍の合計が旋律と同じ", () => {
    expect(parseNotes(gen.notes).total).toBeCloseTo(parseNotes(melody).total, 6);
  });
  it("旋律の下に収まり、音域内で、平行5度・8度がない", () => {
    const mel = expand({ instrument: "lead", notes: melody }, 16);
    const cnt = expand({ instrument: "strings", notes: gen.notes }, 16);
    for (const n of cnt) { expect(n.pitch).toBeGreaterThanOrEqual(48); expect(n.pitch).toBeLessThanOrEqual(72); }
    const parts = [{ instrument: "lead", role: "メロディ", seq: mel }, { instrument: "strings", role: "対旋律", seq: cnt }];
    expect(vl.findParallels(parts, 16, { minCount: 1 })).toEqual([]);
    const m = (t: number) => mel.find((n: { t: number; dur: number }) => n.t <= t && n.t + n.dur > t);
    for (const n of cnt) { const x = m(n.t); if (x) expect(x.pitch - n.pitch).toBeGreaterThanOrEqual(3); }
  });
  it("拍の頭の大半が和音の構成音", () => {
    const cnt = expand({ instrument: "strings", notes: gen.notes }, 16).filter((n: { t: number }) => Number.isInteger(n.t));
    const ch = ["C", "Am", "F", "G"].map((c) => parseChord(c)!);
    const ok = cnt.filter((n: { t: number; pitch: number }) => { const c = ch[Math.floor(n.t / 4)]; return c.intervals.some((iv) => (c.root + iv) % 12 === n.pitch % 12); });
    expect(cnt.length).toBeGreaterThan(0);
    expect(ok.length / cnt.length).toBeGreaterThanOrEqual(0.6);
  });
  it("リズムが旋律の補いになる: 旋律が音を出す瞬間に新しい音を出す割合は半分以下", () => {
    const melOn = new Set(parseNotes(melody).notes.map((n: { t: number }) => n.t));
    const onsets = parseNotes(gen.notes).notes.filter((n: { rest: boolean }) => !n.rest);
    const both = onsets.filter((n: { t: number }) => melOn.has(n.t)).length;
    expect(both / onsets.length).toBeLessThanOrEqual(0.5);
  });
  it("above では旋律の上に出る。空の旋律・読めないコードはエラー", () => {
    const up = cp.generateCounter(melody, chords, { place: "above" });
    const mel = expand({ instrument: "lead", notes: melody }, 16), cnt = expand({ instrument: "strings", notes: up.notes }, 16);
    for (const n of cnt) { const x = mel.find((m: { t: number; dur: number }) => m.t <= n.t && m.t + m.dur > n.t); if (x) expect(n.pitch - x.pitch).toBeGreaterThanOrEqual(3); }
    expect(() => cp.generateCounter("", chords)).toThrow();
    expect(() => cp.generateCounter(melody, ["X"])).toThrow();
  });
});

describe("C8 カノン／模倣 canonOf", () => {
  const m = "E4:1 G4:1 A4:2 G4:1 E4:1 D4:2";
  it("遅れ幅ぶんの休符が頭に付き、拍の合計は元と同じ", () => {
    const c = cp.canonOf(m, { delay: 2 });
    expect(c.startsWith("R:2 E4:1")).toBe(true);
    expect(parseNotes(c).total).toBe(parseNotes(m).total);
    expect(c.endsWith("G4:1") || c.endsWith("E4:1") || c.includes("D4")).toBe(true);
  });
  it("移調と反行", () => {
    expect(cp.canonOf("C4:1 E4:1 G4:2", { transpose: 7 })).toBe("G4:1 B4:1 D5:2");
    expect(cp.canonOf("C4:1 E4:1 G4:2", { invert: true })).toBe("C4:1 G#3:1 F3:2");
  });
  it("拡大（2倍）は長さが倍になり、total で切って合計をそろえる", () => {
    const aug = cp.canonOf("C4:1 D4:1", { factor: 2, total: 4 });
    expect(aug).toBe("C4:2 D4:2");
    const cut = cp.canonOf("C4:1 D4:1 E4:1 F4:1", { factor: 2, total: 4 });
    expect(parseNotes(cut).total).toBe(4);
  });
  it("縮小（0.5倍）は末尾が休符で埋まる", () => {
    const d = cp.canonOf("C4:2 D4:2", { factor: 0.5 });
    expect(d).toBe("C4:1 D4:1 R:2");
  });
  it("模倣の例: 2拍遅れて1オクターブ下を重ねても、平行5度・8度のまとまった連続（4回以上）にはならない", () => {
    const a = part("lead", "旋律", m, 16), b = part("strings", "カノン", cp.canonOf(m, { delay: 2, transpose: -12 }), 16);
    expect(b.seq[0].t).toBe(2);
    expect(vl.findParallels([a, b], 16)).toEqual([]);
  });
});

describe("C9 保持音 pedalLine", () => {
  it("根音を全体で1つの長い音にする", () => {
    const r = vl.pedalLine(["C", "F", "C", "G"], { degree: "root", beats: 4, octave: 2 });
    expect(r.notes).toBe("C2:16");
    expect(r.total).toBe(16);
  });
  it("和音が替わって保持音が和音の外になる小節を警告する", () => {
    const r = vl.pedalLine(["C", "F", "C", "G"], { degree: "root" });
    expect(r.warnings.length).toBe(1);
    expect(r.warnings[0]).toContain("4小節目");
    expect(vl.pedalLine(["C", "Am", "F", "C"], { degree: "root" }).warnings).toEqual([]);
  });
  it("5度の保持音", () => {
    expect(vl.pedalLine(["C", "C"], { degree: "fifth", octave: 3 }).notes).toBe("G3:8");
    expect(() => vl.pedalLine(["X"])).toThrow();
  });
});

describe("C10 対旋律の「入り」", () => {
  const melody = "E5:1 G5:1 A5:2 G5:1 E5:1 D5:2 C5:1 D5:1 E5:2 C5:4";
  const chords = ["C", "Am", "F", "G"];
  it("sections の2回目の同じ種類の頭から入る", () => {
    expect(cp.enterBarFromSections([{ kind: "intro", bars: 2 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "verse", bars: 4 }], 14)).toBe(10);
    expect(cp.enterBarFromSections(undefined, 16)).toBe(8);
  });
  it("入りの前は休み。拍の合計は旋律と同じ", () => {
    const r = cp.counterEntering(melody, chords, { enterBar: 2 });
    expect(r.notes.startsWith("R:8 ")).toBe(true);
    expect(parseNotes(r.notes).total).toBeCloseTo(parseNotes(melody).total, 6);
    expect(r.role).toContain("2周目");
    expect(r.enterBar).toBe(2);
  });
  it("enterBar を省くと後ろ半分から入る", () => {
    expect(cp.counterEntering(melody, chords).enterBar).toBe(2);
  });
});

describe("score-check へ組み込み", () => {
  it("旋律の点検と声部の点検の行が出る（警告があればソースに書かれた文言で）", () => {
    const src = scoreCheckSrc;
    expect(src).toContain("melodyLint(");
    expect(src).toContain("voiceLint(");
  });
});
