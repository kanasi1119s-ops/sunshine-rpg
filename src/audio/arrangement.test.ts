import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { applySections, autoSections, fitSections } from "./arrangement";
import type { Track } from "./score";

const beatsOf = (t: Track): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const barOn = (t: Track, bar: number, bpb = 4): boolean => {
  let pos = 0;
  for (const n of t.notes) {
    if (pos + 1e-9 >= bar * bpb && pos < (bar + 1) * bpb - 1e-9 && n.note !== "R") return true;
    pos += n.durationBeats;
  }
  return false;
};
const song = (extra: object, bars = 32) => aiSongToScore({
  title: "t", description: "", bpm: 120, beats: 4, repeats: 1, chords: Array(bars).fill("Am").join(" "), barsPerChord: 1,
  autoAccompaniment: true, feel: "pop", tone: "rock", parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "A4:4" }], ...extra,
} as never);

describe("セクション編曲", () => {
  it("auto は曲の小節数ちょうどで、導入で始まりサビを含む", () => {
    for (const n of [8, 16, 24, 32, 48, 64]) {
      const s = autoSections(n);
      expect(s.reduce((a, x) => a + x.bars, 0)).toBe(n);
      expect(s.every((x) => x.bars >= 1)).toBe(true);
      if (n >= 24) expect(s.some((x) => x.kind === "chorus")).toBe(true);
    }
    expect(autoSections(32)[0].kind).toBe("intro");
  });
  it("小節数のずれは、延ばすか切って、注意を返す", () => {
    expect(fitSections([{ kind: "verse", bars: 4 }], 8).sections[0].bars).toBe(8);
    expect(fitSections([{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 8 }], 8).sections.map((x) => x.bars)).toEqual([4, 4]);
    expect(fitSections([{ kind: "verse", bars: 8 }], 8).warning).toBeUndefined();
  });
  it("導入はドラムなし、サビは全部と頭のクラッシュ、間奏はドラムなし", () => {
    const { score } = song({ sections: [{ kind: "intro", bars: 4 }, { kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }, { kind: "interlude", bars: 4 }, { kind: "chorus", bars: 8 }] });
    const by = (i: string) => score.tracks.find((t) => t.instrument === i)!;
    expect(barOn(by("kick"), 1)).toBe(false);
    expect(barOn(by("piano"), 1)).toBe(true);
    expect(barOn(by("kick"), 6)).toBe(true);
    expect(barOn(by("snare"), 6)).toBe(false);
    expect(barOn(by("snare"), 13)).toBe(true);
    expect(barOn(by("kick"), 21)).toBe(false);
    expect(barOn(by("crash"), 12)).toBe(true);
    expect(barOn(by("crash"), 13)).toBe(false);
    for (const t of score.tracks.filter((x) => x.instrument !== "lead")) expect(beatsOf(t)).toBeCloseTo(128, 6);
  });
  it("サビの前の小節は、スネアで助走する", () => {
    const { score } = song({ sections: [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }] }, 16);
    const snare = score.tracks.find((t) => t.instrument === "snare")!;
    expect(barOn(snare, 6)).toBe(false);
    expect(barOn(snare, 7)).toBe(true);
  });
  it("Bメロは だんだん強くなり、サビは元の強さ", () => {
    const tracks: Track[] = [{ waveform: "square", instrument: "piano", volume: 0.1, pan: 0, notes: Array.from({ length: 16 }, () => ({ note: "C4", durationBeats: 1, velocity: 100 })) }];
    const out = applySections(tracks, [{ kind: "pre", bars: 2 }, { kind: "chorus", bars: 2 }], 4)[0].notes;
    expect(out[0].velocity!).toBeLessThan(out[7].velocity!);
    expect(out[8].velocity).toBe(100);
  });
  it("sections なし・autoAccompaniment なしでは何も変えない", () => {
    const a = song({}).score.tracks.find((t) => t.instrument === "kick")!;
    expect(barOn(a, 0)).toBe(true);
    const b = song({ autoAccompaniment: false, sections: "auto" });
    expect(b.score.tracks.some((t) => t.instrument === "kick")).toBe(false);
  });
  it("おかしな kind は注意して Aメロにする", () => {
    const { warnings } = song({ sections: [{ kind: "zzz", bars: 32 }] });
    expect(warnings.join("\n")).toContain("zzz");
  });
});

// ───────── 2026-10-11 の拡張 ─────────
import { applyPartSections, checkArrangement, muteRanges, parseSections, resolveModulate, resolveLayers, transposeNoteName, transposeTrack, transitionInto } from "./arrangement";
import { applyScene, energyLayers, resampleEnergy, scaleSections, SCENES, SCENE_NAMES, sceneSections } from "./scene";

const velAt = (t: Track, bar: number, bpb = 4): number[] => {
  let pos = 0;
  const v: number[] = [];
  for (const n of t.notes) {
    if (pos + 1e-9 >= bar * bpb && pos < (bar + 1) * bpb - 1e-9 && n.note !== "R") v.push(n.velocity ?? 1);
    pos += n.durationBeats;
  }
  return v;
};
const beatOn = (t: Track, beat: number): boolean => {
  let pos = 0;
  for (const n of t.notes) {
    if (pos <= beat + 1e-9 && beat < pos + n.durationBeats - 1e-9) return n.note !== "R";
    pos += n.durationBeats;
  }
  return false;
};
const find = (score: { tracks: Track[] }, i: string): Track => score.tracks.find((t) => t.instrument === i)!;

describe("新しいセクション種別", () => {
  const secs = [{ kind: "verse", bars: 4 }, { kind: "build", bars: 4 }, { kind: "drop", bars: 4 }, { kind: "break", bars: 4 }, { kind: "solo", bars: 4 }, { kind: "tag", bars: 4 }];
  const { score, warnings } = song({ sections: secs }, 24);
  it("警告なしで組み立てられ、全トラックの長さがそろう", () => {
    expect(warnings.filter((w) => w.includes("使えません"))).toEqual([]);
    for (const t of score.tracks.filter((x) => x.instrument !== "lead")) expect(beatsOf(t)).toBeCloseTo(96, 6);
  });
  it("ビルドは キック・ハイハット・スネア・ベースだけで、鍵盤は休む。スネアは だんだん密になる", () => {
    for (const i of ["kick", "hihat", "snare", "bass"]) expect(barOn(find(score, i), 4)).toBe(true);
    expect(barOn(find(score, "piano"), 4)).toBe(false);
    const snare = find(score, "snare");
    const hits = (bar: number): number => { let pos = 0, c = 0; for (const n of snare.notes) { if (n.note !== "R" && pos >= bar * 4 - 1e-9 && pos < bar * 4 + 4 - 1e-9) c++; pos += n.durationBeats; } return c; };
    expect(hits(4)).toBeLessThan(hits(5));
    expect(hits(5)).toBeLessThan(hits(7));
  });
  it("ドロップの前の1拍は全員が止まり、ドロップの頭にクラッシュと全員が戻る", () => {
    const beat = 7 * 4 + 3; // ビルド最後の小節の4拍目
    for (const t of score.tracks.filter((x) => x.instrument !== "lead")) expect(beatOn(t, beat + 0.25)).toBe(false);
    expect(beatOn(find(score, "kick"), 7 * 4 + 0.1)).toBe(true); // 直前の小節の頭はまだ鳴る
    expect(barOn(find(score, "crash"), 8)).toBe(true);
    expect(beatOn(find(score, "kick"), 8 * 4)).toBe(true);
    expect(beatOn(find(score, "bass"), 8 * 4)).toBe(true);
  });
  it("ドロップ頭の kick は強い", () => {
    const v = velAt(find(score, "kick"), 8);
    const w = velAt(find(score, "kick"), 9);
    expect(v[0]).toBeGreaterThan(w[0]);
  });
  it("ブレイクは鍵盤と弦だけ、ソロはリズム隊とギターで鍵盤なし、余韻は長音だけ", () => {
    expect(barOn(find(score, "kick"), 13)).toBe(false);
    expect(barOn(find(score, "piano"), 13)).toBe(true);
    expect(barOn(find(score, "piano"), 17)).toBe(false);
    expect(barOn(find(score, "kick"), 17)).toBe(true);
    const tagPiano = find(score, "piano");
    let pos = 0;
    for (const n of tagPiano.notes) { if (pos >= 20 * 4 && pos < 22 * 4 - 1e-9 && n.note !== "R") expect(n.durationBeats).toBe(4); pos += n.durationBeats; }
    expect(barOn(tagPiano, 21)).toBe(true);
  });
  it("ソロは同じ種類のドロップ/サビより小さい", () => {
    const solo = velAt(find(score, "kick"), 16)[0];
    const drop = velAt(find(score, "kick"), 9)[0];
    expect(solo).toBeLessThan(drop);
  });
});

describe("つなぎ（from）", () => {
  const mk = (from: string, extra = {}) => song({ sections: [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8, from }], ...extra }, 16).score;
  it("break1bar は直前の1小節を全員止める（手書きパートも）", () => {
    const sc = mk("break1bar");
    for (const t of sc.tracks.filter((x) => x.instrument !== "crash")) expect(barOn(t, 7)).toBe(false);
    expect(barOn(find(sc, "kick"), 6)).toBe(true);
  });
  it("none は助走もおかずも入れない（スネアは7小節目で鳴らない）", () => {
    const sc = mk("none");
    expect(barOn(find(sc, "snare"), 7)).toBe(false);
  });
  it("riser は最後の2小節で強くなり、ハイハットが16分になる", () => {
    const sc = mk("riser");
    const hat = find(sc, "hihat");
    const first = velAt(hat, 6)[0];
    const lastV = velAt(hat, 7);
    expect(lastV.length).toBe(16);
    expect(lastV[15]).toBeGreaterThan(first);
  });
  it("kime は最後の小節が 1拍目・2拍目のウラ・3拍目 の3発になる", () => {
    const sc = mk("kime");
    const bass = find(sc, "bass");
    let pos = 0; const onsets: number[] = [];
    for (const n of bass.notes) { if (n.note !== "R" && pos >= 28 - 1e-9 && pos < 32 - 1e-9) onsets.push(pos - 28); pos += n.durationBeats; }
    expect(onsets).toEqual([0, 1.5, 2]);
    const guitar = find(sc, "crunch") ?? find(sc, "guitar");
    expect(guitar).toBeTruthy();
  });
  it("transitionInto の既定: break・drop の前は stopBeat、それ以外は fill", () => {
    const l = parseSections([{ kind: "verse", bars: 4 }, { kind: "break", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "drop", bars: 4, from: "none" }], []);
    expect([1, 2, 3].map((i) => transitionInto(l, i))).toEqual(["stopBeat", "fill", "none"]);
    expect(muteRanges(l, 4)).toEqual([[15, 16]]);
  });
  it("おかしな from は注意して無視する", () => {
    const w: string[] = [];
    const l = parseSections([{ kind: "verse", bars: 4, from: "zzz" }], w);
    expect(l[0].from).toBeUndefined();
    expect(w.join("")).toContain("zzz");
  });
});

describe("layers・occurrence・crashAt", () => {
  it("layers で verse を上書きできる（kick のみ・pad を独立）", () => {
    const sc = song({ sections: [{ kind: "verse", bars: 8 }], layers: { verse: ["kick", "bass"] } }, 8).score;
    expect(barOn(find(sc, "kick"), 0)).toBe(true);
    expect(barOn(find(sc, "hihat"), 0)).toBe(false);
    expect(barOn(find(sc, "piano"), 0)).toBe(false);
  });
  it("pad を書くと strings と別に出し入れできる", () => {
    const l = resolveLayers([{ kind: "verse", bars: 8 }], { layers: { verse: ["strings", "bass"] } });
    expect(l[0].groups).toEqual(["strings", "bass"]);
  });
  it("おかしな layers は注意して無視する", () => {
    const { warnings } = song({ sections: [{ kind: "verse", bars: 8 }], layers: { verse: ["kick", "zzz"], nope: ["kick"] } }, 8);
    expect(warnings.join("\n")).toContain("nope");
    expect(warnings.join("\n")).toContain("使えない群");
  });
  it("occurrence: 2回目の verse に guitar が足され、少し強くなる。指定なしなら同じ", () => {
    const secs = [{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }, { kind: "verse", bars: 8 }];
    const plain = song({ sections: secs }, 24).score;
    const occ = song({ sections: secs, occurrence: true }, 24).score;
    const g = (sc: { tracks: Track[] }) => sc.tracks.find((t) => t.instrument === "crunch" || t.instrument === "guitar")!;
    expect(barOn(g(plain), 17)).toBe(false);
    expect(barOn(g(occ), 17)).toBe(true);
    expect(barOn(g(occ), 1)).toBe(false);
    expect(velAt(find(occ, "kick"), 17)[0]).toBeGreaterThan(velAt(find(plain, "kick"), 17)[0]);
  });
  it("crashAt: 既定はサビの頭。solo と last と afterBridge を指定できる", () => {
    const secs = [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "bridge", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "solo", bars: 4 }];
    const d = song({ sections: secs }, 20).score;
    expect(barOn(find(d, "crash"), 4)).toBe(true);
    expect(barOn(find(d, "crash"), 16)).toBe(false);
    const c = song({ sections: secs, crashAt: ["chorus", "solo", "last", "afterBridge"] }, 20).score;
    expect(barOn(find(c, "crash"), 16)).toBe(true);
    expect(barOn(find(c, "crash"), 12)).toBe(true);
    expect(velAt(find(c, "crash"), 12)[0]).toBeGreaterThan(velAt(find(c, "crash"), 4)[0]);
    const off = song({ sections: [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4, crash: false }] }, 8).score;
    expect(off.tracks.some((t) => t.instrument === "crash")).toBe(false);
  });
});

describe("手書きパートの sections", () => {
  const secs = [{ kind: "intro", bars: 4 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }];
  const part = (extra: object) => ({ instrument: "echoGuitar", role: "対旋律", volume: 0.1, pan: 0.5, amp: "auto", notes: "C5:1", ...extra });
  const mk = (partExtra: object, extra: object = {}) => aiSongToScore({
    title: "t", description: "", bpm: 120, beats: 4, repeats: 1, chords: Array(12).fill("Am").join(" "), barsPerChord: 1,
    autoAccompaniment: true, feel: "pop", tone: "rock", sections: secs, parts: [part(partExtra)], ...extra,
  } as never);
  it("0 で休み、数字で音量、octave でオクターブ", () => {
    const { score } = mk({ sections: { intro: 0, verse: 0.5, chorus: { gain: 1, octave: 1 } } });
    const t = find(score, "echoGuitar");
    expect(barOn(t, 1)).toBe(false);
    expect(velAt(t, 5)[0]).toBeCloseTo(0.5, 6);
    expect(t.notes.find((n, i) => n.note !== "R" && t.notes.slice(0, i).reduce((a, x) => a + x.durationBeats, 0) === 32)!.note).toBe("C6");
    expect(beatsOf(t)).toBeCloseTo(48, 6);
  });
  it("sections がなくても書いた順に鳴る（指定なしは何も変えない）", () => {
    const { score } = mk({});
    expect(barOn(find(score, "echoGuitar"), 1)).toBe(true);
  });
  it("sections 未指定の曲で使うと auto にして注意する", () => {
    const { warnings, score } = mk({ sections: { verse: 0 } }, { sections: undefined });
    expect(warnings.join("\n")).toContain("sections");
    expect(barOn(find(score, "echoGuitar"), 0)).toBe(false);
  });
  it("applyPartSections: ドラムのオクターブは無視、休みは結合される", () => {
    const out = applyPartSections([{ note: "C2", durationBeats: 4 }, { note: "C2", durationBeats: 4 }], [{ kind: "intro", bars: 1 }, { kind: "verse", bars: 1 }], 4, { intro: { octave: 1, gain: 0 } }, true);
    expect(out[0].note).toBe("R");
    expect(out[1].note).toBe("C2");
  });
  it("停止つなぎでも keepBreak: true のパートは止まらない", () => {
    const sc = { sections: [{ kind: "verse", bars: 4 }, { kind: "drop", bars: 4 }] };
    const a = aiSongToScore({ title: "t", description: "", bpm: 120, beats: 4, repeats: 1, chords: Array(8).fill("Am").join(" "), barsPerChord: 1, autoAccompaniment: true, feel: "pop", tone: "rock", ...sc, parts: [part({ notes: "C5:8" }), part({ notes: "C5:8", keepBreak: true, instrument: "pad" })] } as never);
    expect(beatOn(a.score.tracks.find((t) => t.instrument === "echoGuitar")!, 15.5)).toBe(false);
    expect(beatOn(a.score.tracks.find((t) => t.instrument === "pad")!, 15.5)).toBe(true);
  });
});

describe("転調 modulate", () => {
  it("transposeNoteName: 半音・全音、範囲に収める", () => {
    expect(transposeNoteName("C4", 1)).toBe("C#4");
    expect(transposeNoteName("B4", 2)).toBe("C#5");
    expect(transposeNoteName("Bb3", 1)).toBe("B3");
    expect(transposeNoteName("C8", 2)).toBe("D7");
    expect(transposeNoteName("zzz", 3)).toBe("zzz");
  });
  const mk = (modulate: object, partExtra: object = {}, none = false) => aiSongToScore({
    title: "t", description: "", bpm: 120, beats: 4, repeats: 1, chords: "Am F C G Am F C G", barsPerChord: 1, autoAccompaniment: true, feel: "pop", tone: "rock",
    sections: [{ kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }], ...(none ? {} : { modulate }),
    parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "E5:8 E5:8 E5:16", ...partExtra }, { instrument: "kick", role: "k", volume: 0.2, pan: 0, amp: "auto", notes: "x:1" }],
  } as never);
  it("atBar 以降だけ半音上がり、ドラムは動かない。自動の伴奏も上がる", () => {
    const { score } = mk({ atBar: 5, semitones: 1 });
    const lead = find(score, "lead");
    expect(lead.notes[0].note).toBe("E5");
    expect(lead.notes[lead.notes.length - 1].note).toBe("F5");
    const plain = mk({ atBar: 5, semitones: 1 }, {}, true).score;
    const names = (t: Track, from: number, to: number): string[] => { let pos = 0; const o: string[] = []; for (const n of t.notes) { if (n.note !== "R" && pos >= from && pos < to) o.push(n.note); pos += n.durationBeats; } return o; };
    const before = names(find(score, "bass"), 0, 16);
    expect(before).toEqual(names(find(plain, "bass"), 0, 16));
    const after = names(find(score, "bass"), 16, 32);
    expect(after.length).toBeGreaterThan(4);
    expect(after).toEqual(names(find(plain, "bass"), 16, 32).map((n) => transposeNoteName(n, 1)));
    expect(find(score, "kick").notes.every((n) => n.note === "C2" || n.note === "R")).toBe(true);
  });
  it("at: lastChorus は最後のサビの頭、modulate:false のパートは動かない", () => {
    const { score } = mk({ at: "lastChorus", semitones: 2 }, { modulate: false });
    expect(find(score, "lead").notes[find(score, "lead").notes.length - 1].note).toBe("E5");
  });
  it("resolveModulate: 範囲外や0は注意して null", () => {
    const w: string[] = [];
    expect(resolveModulate({ atBar: 99, semitones: 1 }, undefined, 4, 8, w)).toBeNull();
    expect(resolveModulate({ atBar: 3, semitones: 0 }, undefined, 4, 8, w)).toBeNull();
    expect(resolveModulate({ at: "lastChorus", semitones: 1 }, undefined, 4, 8, w)).toBeNull();
    expect(w.length).toBe(3);
    expect(resolveModulate({ atBar: 3, semitones: 2 }, undefined, 4, 8, [])).toEqual({ atBeat: 8, semitones: 2 });
  });
  it("transposeTrack: ドラムは返さずそのまま", () => {
    const t: Track = { waveform: "square", instrument: "kick", volume: 1, pan: 0, notes: [{ note: "C2", durationBeats: 1 }] };
    expect(transposeTrack(t, 2, 0)).toBe(t);
  });
});

describe("編曲チェッカー", () => {
  it("変わり目が弱い（群がほぼ同じで段差がない）と小節番号つきで注意する", () => {
    const w = checkArrangement(parseSections([{ kind: "verse", bars: 8 }, { kind: "interlude", bars: 8 }, { kind: "bridge", bars: 8 }], []), 4, { layers: { interlude: { groups: ["kick", "hat", "bass", "keys"], from: 0.9, to: 0.9 } } });
    expect(w.some((x) => x.startsWith("9小節目") && x.includes("変わり目が弱い"))).toBe(true);
  });
  it("サビがAメロ以下なら注意", () => {
    const w = checkArrangement(parseSections([{ kind: "verse", bars: 8 }, { kind: "chorus", bars: 8 }], []), 4, { layers: { chorus: ["kick", "bass"] } });
    expect(w.some((x) => x.includes("9小節目") && x.includes("サビ"))).toBe(true);
  });
  it("最後のサビの前に止める場所がないと注意。ブリッジか stopBeat があれば出ない", () => {
    const bad = parseSections([{ kind: "chorus", bars: 4 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "chorus", bars: 4 }], []);
    expect(checkArrangement(bad, 4).some((x) => x.includes("最後のサビの直前"))).toBe(true);
    const ok = parseSections([{ kind: "chorus", bars: 4 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 4 }, { kind: "chorus", bars: 4, from: "stopBeat" }], []);
    expect(checkArrangement(ok, 4).some((x) => x.includes("最後のサビの直前"))).toBe(false);
    const ok2 = parseSections([{ kind: "chorus", bars: 4 }, { kind: "bridge", bars: 4 }, { kind: "chorus", bars: 4 }], []);
    expect(checkArrangement(ok2, 4).some((x) => x.includes("最後のサビの直前"))).toBe(false);
  });
  it("定番の auto 構成では注意が出ない", () => {
    for (const n of [32, 48, 64]) expect(checkArrangement(autoSections(n), 4, {}, false)).toEqual([]);
  });
});

describe("scene・energy", () => {
  it("全部の場面で、型が曲の長さにぴったり合い、1小節以上で、使える種別だけ", () => {
    for (const name of SCENE_NAMES) {
      for (const n of [16, 24, 32, 48, 64, 96]) {
        const s = sceneSections(name, n)!;
        expect(s.reduce((a, x) => a + x.bars, 0)).toBe(n);
        expect(s.every((x) => x.bars >= 1)).toBe(true);
      }
    }
  });
  it("型の小節数のまま使うとき、変えない", () => {
    expect(sceneSections("town", 32)!.map((x) => x.bars)).toEqual([8, 8, 8, 8]);
    expect(sceneSections("boss", 46)!.map((x) => x.kind).length).toBe(8);
  });
  it("scaleSections: 短い曲でも落ちない", () => {
    expect(scaleSections(SCENES.ending.sections, 4).reduce((a, x) => a + x.bars, 0)).toBe(4);
    expect(scaleSections([{ kind: "verse", bars: 8 }], 3)[0].bars).toBe(3);
  });
  it("applyScene: 書いていない項目だけ埋め、書いた項目は変えない。bpm が目安外なら注意", () => {
    const w: string[] = [];
    const r = applyScene({ scene: "battle", bpm: 100, tone: "prs" } as never, w) as { tone: string; feel: string; occurrence: boolean };
    expect(r.tone).toBe("prs");
    expect(r.feel).toBe("rock");
    expect(r.occurrence).toBe(true);
    expect(w.join("")).toContain("150〜190");
    const w2: string[] = [];
    applyScene({ scene: "zzz", bpm: 100 } as never, w2);
    expect(w2.join("")).toContain("zzz");
  });
  it("scene: 戦闘は前奏なしで1拍目に全員とクラッシュ、町はサビ/ドラムなしの間奏", () => {
    const mk = (scene: string, bars: number, bpm: number) => aiSongToScore({ title: "t", description: "", bpm, beats: 4, repeats: 1, chords: Array(bars).fill("Em").join(" "), barsPerChord: 1, autoAccompaniment: true, scene, parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "E5:1" }] } as never);
    const b = mk("battle", 16, 170);
    expect(beatOn(find(b.score, "kick"), 0)).toBe(true);
    expect(beatOn(find(b.score, "crash"), 0)).toBe(true);
    expect(b.warnings).toEqual([]);
    const t = mk("town", 32, 100);
    expect(barOn(find(t.score, "kick"), 3)).toBe(false);
    expect(barOn(find(t.score, "hihat"), 3)).toBe(true);
    expect(barOn(find(t.score, "hihat"), 9)).toBe(false);
    expect(t.score.tracks.some((x) => x.instrument === "crash")).toBe(false);
  });
  it("scene に自分の sections を書けば、そちらが優先", () => {
    const r = aiSongToScore({ title: "t", description: "", bpm: 100, beats: 4, repeats: 1, chords: Array(16).fill("Em").join(" "), barsPerChord: 1, autoAccompaniment: true, scene: "town", sections: [{ kind: "chorus", bars: 16 }], parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "E5:1" }] } as never);
    expect(barOn(find(r.score, "snare"), 3)).toBe(true);
  });
  it("energyLayers: 1〜3＝2群、4〜6＝4群、7〜8＝6群、9〜10＝全群とクラッシュ", () => {
    const l = energyLayers([2, 5, 8, 10]);
    expect(l.map((x) => x.groups.length)).toEqual([2, 4, 6, 7]);
    expect(l[0].groups).toEqual(["kick", "bass"]);
    expect(l.map((x) => !!x.crash)).toEqual([false, false, false, true]);
    expect(l[0].to).toBeGreaterThan(l[0].from);
  });
  it("resampleEnergy: 曲線名と長さの違い", () => {
    expect(resampleEnergy("stairs", 5)).toEqual([6, 7, 8, 9, 10]);
    expect(resampleEnergy([1, 10], 4)).toEqual([1, 1, 10, 10]);
    expect(resampleEnergy([3], 3)).toEqual([3, 3, 3]);
  });
  it("energy を曲に書くと、サビが全群＋クラッシュ、谷は少ない", () => {
    const { score } = song({ sections: [{ kind: "verse", bars: 4 }, { kind: "bridge", bars: 4 }, { kind: "chorus", bars: 4 }], energy: [4, 2, 10] }, 12);
    expect(barOn(find(score, "kick"), 5)).toBe(true);
    expect(barOn(find(score, "hihat"), 5)).toBe(false);
    expect(barOn(find(score, "snare"), 9)).toBe(true);
    expect(barOn(find(score, "crash"), 8)).toBe(true);
  });
  it("energy の数がちがうと注意、おかしな名前も注意", () => {
    const a = song({ sections: [{ kind: "verse", bars: 16 }, { kind: "chorus", bars: 16 }], energy: [1, 2, 3] });
    expect(a.warnings.join("")).toContain("energy の数");
    const b = song({ sections: [{ kind: "verse", bars: 32 }], energy: "zzz" });
    expect(b.warnings.join("")).toContain("zzz");
  });
  it("modulate は scene の既定（ボス: 最後のサビで全音上げ）で入る", () => {
    const mk = (scene: string) => aiSongToScore({ title: "t", description: "", bpm: 150, beats: 4, repeats: 1, chords: Array(46).fill("Em").join(" "), barsPerChord: 1, autoAccompaniment: true, scene, parts: [{ instrument: "lead", role: "m", volume: 0.2, pan: 0, amp: "auto", notes: "E5:1" }] } as never).score;
    const lead = find(mk("boss"), "lead");
    expect(lead.notes[lead.notes.length - 1].note).toBe("F#5");
    expect(find(mk("battle"), "lead").notes[0].note).toBe("E5");
  });
});
