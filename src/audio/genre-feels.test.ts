import { describe, expect, it } from "vitest";
import { approachNote, bassFromKick, buildNewSong, GENRE_FEELS, NEW_SONG_FEELS, } from "./newsong";
import { aiSongToScore } from "./ai-song";
import { applySections } from "./arrangement";
import { trackTotalBeats } from "./edit";
import { noteNameToMidi } from "./note";
import { REST, type Score } from "./score";
import { DRUM_GENRES, blastPattern, breakdownHalftime, drumMixFor, gallop, gridLengthOk, hihatPattern, jazzSwingForBpm, limitDensity, placeGhosts, swingFromPercent, trapRoll, trapRollBeats, twoBass } from "./drum-genres";
import { checkScore, kickBassAlignment } from "./song-check";
import { SOUND_SETS } from "./sound-sets";


const fnv = (s: string): string => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, "0"); };
const base = { bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2, leadInstrument: "lead" as const };
const PROGRESSIONS = ["Am F C G", "Dm7 G7 Cmaj7 A7", "E7 A7 E7 B7", "C G/B Am Em/G F", "Bbm Gb Db Ab", "B E F# G#m"];

describe("既存の feel の出力は変わらない（rock/pop/ballad/dance/vocaloid）", () => {
  // vocaloid だけは、ベースのオクターブ上の音が音域（E1〜G3）をこえていたのを収めたので、最後の4つ（vocaloid）の値が実装前（75ebc90b 39ff79f5 7bb65f3d a3011faf）から変わっている。他は実装前と同じ。
  it("2026-10-11 の実装前と同じ（ハッシュ照合。vocaloid のベース音域だけ修正）", () => {
    const out: string[] = [];
    for (const feel of ["rock", "pop", "ballad", "dance", "vocaloid"] as const) for (const beats of [3, 4]) for (const chords of ["Am F C G", "Dm7 G7 Cmaj7 A7"]) {
      const sc = buildNewSong({ bpm: 120, beats, chords, barsPerChord: 1, repeats: 2, feel, leadInstrument: "lead" });
      out.push(fnv(JSON.stringify(sc)));
    }
    expect(out.join(" ")).toBe("ea322d64 5da7cd32 f40e3674 c81b778a 56c9f410 b0f07c76 d3251b66 8e20ed94 ed6b714c e40e7d10 9e650a02 edecaa3e 87aa6e6e c70a5d32 9bba2faa 4be6966e 8323a0fb 6c03f95d 0dbbb83d 674a9d67");
  });
  it("approach: true のとき、rock/pop/ballad のベースも4小節目の最後が次の根音の半音まわりになる", () => {
    for (const feel of ["rock", "pop", "ballad"] as const) {
      const plain = buildNewSong({ ...base, feel }).tracks.find((t) => t.instrument === "bass")!;
      const ap = buildNewSong({ ...base, feel, approach: true }).tracks.find((t) => t.instrument === "bass")!;
      expect(trackTotalBeats(ap)).toBeCloseTo(trackTotalBeats(plain), 6);
      expect(JSON.stringify(ap.notes)).not.toBe(JSON.stringify(plain.notes));
      // 4小節目（G）の最後の音は、次の小節（Am の A2=45）の半音下 G#2=44
      let pos = 0, lastMidi = 0;
      for (const n of ap.notes) { if (pos < 16 && n.note !== REST) lastMidi = noteNameToMidi(n.note); pos += n.durationBeats; }
      expect(lastMidi).toBe(44);
    }
  });
});

describe("ジャンル別の自動伴奏", () => {
  it("すべての feel × 進行 × 拍子で、拍の合計がそろい、ベースは音域内（E1〜G3、808は C1〜C3）", () => {
    for (const feel of NEW_SONG_FEELS) for (const chords of PROGRESSIONS) for (const beats of [3, 4, 6, 7]) {
      const s = buildNewSong({ ...base, chords, beats, feel });
      const n = chords.split(" ").length * 2;
      for (const t of s.tracks) {
        expect(trackTotalBeats(t), `${feel} ${t.instrument} ${chords} ${beats}`).toBeCloseTo(n * beats, 6);
        for (const e of t.notes) if (e.note !== REST) expect(Number.isFinite(noteNameToMidi(e.note))).toBe(true);
      }
      for (const t of s.tracks.filter((x) => x.instrument === "bass" || x.instrument === "sub808")) {
        const [lo, hi] = t.instrument === "sub808" ? [24, 48] : [28, 55];
        for (const e of t.notes) if (e.note !== REST) {
          const m = noteNameToMidi(e.note);
          expect(m, `${feel} ${chords} ${e.note}`).toBeGreaterThanOrEqual(lo);
          expect(m, `${feel} ${chords} ${e.note}`).toBeLessThanOrEqual(hi);
        }
      }
    }
  }, 60000);
  it("自動伴奏の強さは MIDI 数字（ゴースト以外は70以上、112以下は主要な音）", () => {
    for (const feel of GENRE_FEELS) {
      const s = buildNewSong({ ...base, feel });
      for (const t of s.tracks) for (const e of t.notes) if (e.note !== REST && e.velocity !== undefined) expect(e.velocity).toBeLessThanOrEqual(127);
    }
  });
  it("最後のトラックは空のメロディ（lead）", () => {
    for (const feel of GENRE_FEELS) {
      const s = buildNewSong({ ...base, feel });
      expect(s.tracks[s.tracks.length - 1].notes.every((n) => n.note === REST)).toBe(true);
    }
  });
  it("jazz: 1拍1音のウォーキング（根音→3度→5度→次の根音の半音）", () => {
    const s = buildNewSong({ ...base, feel: "jazz", chords: "Dm7 G7 Cmaj7 Cmaj7", repeats: 1 });
    const bass = s.tracks.find((t) => t.instrument === "bass")!;
    const notes = bass.notes.filter((n) => n.note !== REST);
    expect(notes.length).toBe(16);
    expect(notes.every((n) => n.durationBeats === 1)).toBe(true);
    const m = notes.map((n) => noteNameToMidi(n.note));
    expect(m[0] % 12).toBe(2); // D
    expect(m[1] % 12).toBe(5); // F（3度）
    expect(m[2] % 12).toBe(9); // A（5度）
    expect(m[3] % 12).toBe(6); // Gの半音上=F#（次の根音 G より半音下）
    expect(s.swing).toBeGreaterThan(0);
  });
  it("reggae: ワンドロップ（1拍目のキックなし・3拍目にキックとスネア）、ベースは1拍目を休む", () => {
    const s = buildNewSong({ ...base, feel: "reggae" });
    const kick = s.tracks.find((t) => t.instrument === "kick")!;
    let pos = 0; const kickAt: number[] = [];
    for (const n of kick.notes) { if (n.note !== REST) kickAt.push(pos); pos += n.durationBeats; }
    expect(kickAt.slice(0, 2)).toEqual([2, 6]);
    const bass = s.tracks.find((t) => t.instrument === "bass")!;
    expect(bass.notes[0].note).toBe(REST);
  });
  it("bossa: ベースは付点4分＋8分（根音と5度）で、キックと同じ位置", () => {
    const s = buildNewSong({ ...base, feel: "bossa" });
    const bass = s.tracks.find((t) => t.instrument === "bass")!;
    expect(bass.notes.slice(0, 4).map((n) => n.durationBeats)).toEqual([1.5, 0.5, 1.5, 0.5]);
    const align = kickBassAlignment(s)!;
    expect(align.kickWithBass).toBe(1);
  });
  it("funk: ベースは1拍目の頭に必ず根音。ghostDensity で弱いゴーストが増える。決まった種から作るので同じ結果", () => {
    const a = buildNewSong({ ...base, feel: "funk", ghostDensity: 0 }).tracks.find((t) => t.instrument === "bass")!;
    const b = buildNewSong({ ...base, feel: "funk", ghostDensity: 1 }).tracks.find((t) => t.instrument === "bass")!;
    const ghosts = (t: typeof a): number => t.notes.filter((n) => n.note !== REST && (n.velocity ?? 99) < 60).length;
    expect(ghosts(a)).toBe(0);
    expect(ghosts(b)).toBeGreaterThan(8);
    expect(noteNameToMidi(b.notes[0].note) % 12).toBe(9);
    expect(b.notes[0].velocity).toBeGreaterThan(100);
    expect(JSON.stringify(buildNewSong({ ...base, feel: "funk", ghostDensity: 1 }))).toBe(JSON.stringify(buildNewSong({ ...base, feel: "funk", ghostDensity: 1 })));
  });
  it("metal: キックの位置にベースの根音（整合率が高い）。速いテンポ（200）では16分を8分に落とす", () => {
    const s = buildNewSong({ ...base, feel: "metal", bpm: 160 });
    expect(kickBassAlignment(s)!.kickWithBass).toBeGreaterThanOrEqual(0.9);
    const kicks = (sc: Score): number => sc.tracks.find((t) => t.instrument === "kick")!.notes.filter((n) => n.note !== REST).length;
    expect(kicks(buildNewSong({ ...base, feel: "metal", bpm: 210 }))).toBeLessThan(kicks(s));
  });
  it("trap/halftime: 808（sub808）がキックの位置から鳴る。スネアは3拍目だけ", () => {
    for (const feel of ["trap", "halftime"] as const) {
      const s = buildNewSong({ ...base, feel });
      expect(s.tracks.some((t) => t.instrument === "sub808")).toBe(true);
      expect(kickBassAlignment(s)!.kickWithBass).toBe(1);
      const snare = s.tracks.find((t) => t.instrument === "snare")!;
      let pos = 0; const at = new Set<number>();
      for (const n of snare.notes) { if (n.note !== REST && (n.velocity ?? 0) > 80) at.add(pos % 4); pos += n.durationBeats; }
      expect([...at]).toEqual([2]);
    }
  });
  it("shuffle/jazz は swing が入る。funk は 0.2", () => {
    expect(buildNewSong({ ...base, feel: "shuffle" }).swing).toBe(0.6);
    expect(buildNewSong({ ...base, feel: "jazz" }).swing).toBe(0.6);
    expect(buildNewSong({ ...base, feel: "funk" }).swing).toBe(0.2);
    expect(buildNewSong({ ...base, feel: "rock" }).swing).toBeUndefined();
  });
  it("小節末のアプローチ: 新しいジャンルは4・8小節目の最後が次の根音の半音まわり", () => {
    expect(approachNote(45, 48)).toBe(47);
    expect(approachNote(48, 45)).toBe(46);
    for (const feel of ["funk", "shuffle", "disco", "dnb", "reggae"] as const) {
      const s = buildNewSong({ ...base, feel });
      const bass = s.tracks.find((t) => t.instrument === "bass")!;
      let pos = 0, last = 0;
      for (const n of bass.notes) { if (pos < 16 && n.note !== REST) last = noteNameToMidi(n.note); pos += n.durationBeats; }
      expect(last, feel).toBe(44); // 次は Am の A2=45 の半音下
    }
  });
  it("bassFromKick: キックのマスは根音、ほかは filler", () => {
    expect(bassFromKick("X...X...", "..5...5.")).toBe("r.5.r.5.");
    expect(bassFromKick("X.o.....", "..5...5.")).toBe("r.5...5.");
  });
});

describe("aiSongToScore でジャンル別 feel", () => {
  const song = (extra: object) => ({ title: "t", description: "d", bpm: 110, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 4, autoAccompaniment: true, feel: "funk", tone: "rock", parts: [], ...extra });
  it("全 feel が通り、未知の feel は pop になる", () => {
    for (const feel of NEW_SONG_FEELS) expect(() => aiSongToScore(song({ feel }))).not.toThrow();
    expect(aiSongToScore(song({ feel: "nope" })).score.tracks.length).toBe(aiSongToScore(song({ feel: "pop" })).score.tracks.length);
  });
  it("swing を書かなければジャンルの標準（jazz 0.6）、書けばそれが優先", () => {
    expect(aiSongToScore(song({ feel: "jazz" })).score.swing).toBe(0.6);
    expect(aiSongToScore(song({ feel: "jazz", swing: 0.3 })).score.swing).toBe(0.3);
  });
  it("drumGenre は drumMix・swing・human を補い、書いた drumMix が優先", () => {
    const r = aiSongToScore(song({ feel: "rock", drumGenre: "metal", drumMix: { kick: { level: 0.5 } } })).score;
    expect(r.drumMix?.kick?.level).toBe(0.5);
    expect(r.drumMix?.snare?.reverb).toBe(0.1);
    expect(r.human).toBe(0.15);
    expect(aiSongToScore(song({ drumGenre: "zzz" })).warnings.join()).toMatch(/drumGenre/);
  });
  it("ghostDensity は human から導かれる（funk のスネアのゴースト）", () => {
    const ghosts = (extra: object): number => aiSongToScore(song(extra)).score.tracks.find((t) => t.instrument === "snare")!.notes.filter((n) => n.note !== REST && (n.velocity ?? 99) < 60).length;
    expect(ghosts({ ghostDensity: 1 })).toBeGreaterThan(ghosts({ ghostDensity: 0 }));
  });
  it("sections + bassDensity: Aメロは拍の頭だけ、終わりは根音1音。指定しなければ変わらない", () => {
    const plain = aiSongToScore(song({ feel: "rock", repeats: 8, sections: [{ kind: "verse", bars: 16 }, { kind: "outro", bars: 16 }] })).score;
    const dens = aiSongToScore(song({ feel: "rock", repeats: 8, bassDensity: true, sections: [{ kind: "verse", bars: 16 }, { kind: "outro", bars: 16 }] })).score;
    const count = (sc: Score): number => sc.tracks.find((t) => t.instrument === "bass")!.notes.filter((n) => n.note !== REST).length;
    expect(count(dens)).toBeLessThan(count(plain));
    const outroNotes = (sc: Score): number => { let pos = 0, c = 0; for (const n of sc.tracks.find((t) => t.instrument === "bass")!.notes) { if (pos >= 64 && n.note !== REST) c++; pos += n.durationBeats; } return c; };
    expect(outroNotes(dens)).toBe(16);
  });
  it("sections の bassDensity: サビの8分の裏はオクターブ上（音域内）", () => {
    const sc = buildNewSong({ ...base, feel: "rock", repeats: 2 });
    const out = applySections(sc.tracks.slice(0, -1), [{ kind: "chorus", bars: 8 }], 4, true, { bassDensity: true }).find((t) => t.instrument === "bass")!;
    for (const n of out.notes) if (n.note !== REST) expect(noteNameToMidi(n.note)).toBeLessThanOrEqual(55);
    expect(out.notes.some((n, i) => i > 0 && n.note !== REST && noteNameToMidi(n.note) > noteNameToMidi(out.notes[0].note))).toBe(true);
  });
});

describe("音域・整合率の検査（song-check）", () => {
  it("ベースが E1〜G3 の外なら注意する", () => {
    const sc: Score = { tempoBpm: 100, loop: true, tracks: [{ waveform: "sawtooth", instrument: "bass", volume: 0.3, notes: [{ note: "C1", durationBeats: 2 }, { note: "C4", durationBeats: 2 }] }] };
    expect(checkScore(sc).join()).toMatch(/音域/);
    expect(checkScore({ ...sc, tracks: [{ ...sc.tracks[0], notes: [{ note: "E1", durationBeats: 2 }, { note: "G3", durationBeats: 2 }] }] }).join()).not.toMatch(/音域/);
  });
  it("自動伴奏のベースは、どの feel でも音域の注意が出ない", () => {
    for (const feel of NEW_SONG_FEELS) expect(checkScore(buildNewSong({ ...base, feel })).join(), feel).not.toMatch(/音域.*外/);
  });
  it("kickBassAlignment: rock は高く、reggae はキックの数が少ない", () => {
    expect(kickBassAlignment(buildNewSong({ ...base, feel: "rock" }))!.kickWithBass).toBeGreaterThanOrEqual(0.9);
  });
});

describe("drum-genres（ジャンル別の表と道具）", () => {
  it("すべての格子は16文字で、drumMix に展開できる", () => {
    for (const g of Object.values(DRUM_GENRES)) {
      for (const k of ["kick", "snare", "hat"] as const) expect(gridLengthOk(g.grids[k]), `${g.id}.${k}`).toBe(true);
      expect(drumMixFor(g.id)).toBeDefined();
      expect(g.bpm[0]).toBeLessThan(g.bpm[1]);
    }
    expect(drumMixFor("nope")).toBeUndefined();
  });
  it("ジャンル別 feel の格子も16文字（CFG を通した出力のスネア・キック・ハイハットが拍に乗る）", () => {
    for (const feel of GENRE_FEELS) {
      const s = buildNewSong({ ...base, feel });
      for (const inst of ["kick", "snare", "hihat"]) expect(s.tracks.find((t) => t.instrument === inst)!.notes.length).toBe(8 * 16);
    }
  });
  it("swing の換算", () => {
    expect(swingFromPercent(50)).toBe(0);
    expect(swingFromPercent(66.7)).toBeCloseTo(1, 1);
    expect(swingFromPercent(58)).toBeCloseTo(0.48, 1);
    expect(jazzSwingForBpm(90)).toBeGreaterThanOrEqual(0.8);
    expect(jazzSwingForBpm(160)).toBeGreaterThanOrEqual(0.5);
    expect(jazzSwingForBpm(160)).toBeLessThanOrEqual(0.7);
    expect(jazzSwingForBpm(220)).toBeLessThanOrEqual(0.5);
    expect(jazzSwingForBpm(120)).toBeGreaterThan(jazzSwingForBpm(200));
  });
  it("ブラスト・ギャロップ・ブレイクダウンは16文字。速いテンポは8分に落ちる", () => {
    for (const t of ["alternating", "hammer", "bomb"] as const) for (const k of ["kick", "snare", "hat"] as const) expect(blastPattern(t)[k].length).toBe(16);
    expect(blastPattern("bomb", 180).kick).toBe("xxxxxxxxxxxxxxxx");
    expect(blastPattern("bomb", 230).kick).toBe("x.x.x.x.x.x.x.x.");
    expect(gallop().kick.length).toBe(16);
    expect(breakdownHalftime().snare).toBe("........X.......");
    expect(twoBass(150).kick).toBe("XxXxXxXxXxXxXxXx");
    expect(limitDensity("XxXxXxXx", 220)).toBe("X.X.X.X.");
  });
  it("トラップのロールは合計4拍", () => {
    expect(trapRollBeats(trapRoll("triplet"))).toBeCloseTo(4, 3);
    expect(trapRollBeats(trapRoll("thirtysecond"))).toBeCloseTo(4, 3);
  });
  it("ゴースト: キックと同じマスにも、バックビートにも置かない。3つ続けない。決まった結果", () => {
    for (let bar = 0; bar < 16; bar++) {
      const g = placeGhosts("....X.......X...", "X.x.......x.....", 1, bar, 100);
      expect(g.length).toBe(16);
      expect(g[0]).toBe("."); expect(g[2]).toBe("."); expect(g[4]).toBe("X"); expect(g[12]).toBe("X");
      expect(g).not.toMatch(/ooo/);
      expect(g).toBe(placeGhosts("....X.......X...", "X.x.......x.....", 1, bar, 100));
      // 速いテンポではバックビートの直前を避ける
      const fast = placeGhosts("....X.......X...", "X.x.......x.....", 1, bar, 170);
      expect(fast[3]).toBe("."); expect(fast[11]).toBe(".");
    }
    expect(placeGhosts("....X.......X...", "X...............", 0, 1)).toBe("....X.......X...");
  });
  it("hihatPattern: 16文字、4小節目に O が1つ、小節ごとに型が変わる", () => {
    for (const id of Object.keys(DRUM_GENRES)) for (let b = 0; b < 8; b++) {
      const p = hihatPattern(id, b);
      expect(p.length).toBe(16);
      const baseO = (DRUM_GENRES[id].grids.hat.match(/O/g) ?? []).length;
      expect((p.match(/O/g) ?? []).length).toBeLessThanOrEqual(baseO || 1);
    }
    expect(hihatPattern("rock", 3)).toContain("O");
    expect(hihatPattern("jpop", 0)).not.toBe(hihatPattern("jpop", 1));
    expect(hihatPattern("rock", 0, "chorus").length).toBe(16);
  });
});

describe("ジャンル別サウンドセット", () => {
  it("14個が登録され、drumMix・パターンを持つ", () => {
    for (const id of ["rock-band", "metal", "jpop-anime", "ballad", "jazz-swing", "funk-tight", "hiphop-boombap", "trap", "house", "dnb", "reggae", "bossa", "game-battle", "game-boss"]) {
      const s = SOUND_SETS[id];
      expect(s, id).toBeDefined();
      expect(s.drumMix).toBeDefined();
      expect(Object.values(s.drumPatterns ?? {}).every((g) => g.length === 16)).toBe(true);
    }
  });
});

describe("ベース単独の見本（assets-src/ai-songs/bass-demo-*.json）", () => {
  for (const name of ["funk", "reggae", "bossa", "walking"]) {
    it(`${name}: 読めて、ベースの音が曲の長さにそろう`, () => {
      const files = import.meta.glob("../../assets-src/ai-songs/bass-demo-*.json", { eager: true, import: "default" }) as Record<string, unknown>;
      const json = files[`../../assets-src/ai-songs/bass-demo-${name}.json`];
      const r = aiSongToScore(json);
      const bass = r.score.tracks.find((t) => t.instrument === "bass")!;
      expect(trackTotalBeats(bass)).toBeCloseTo(8 * 4, 6);
      for (const n of bass.notes) if (n.note !== REST) { const m = noteNameToMidi(n.note); expect(m).toBeGreaterThanOrEqual(28); expect(m).toBeLessThanOrEqual(55); }
      expect(r.warnings.filter((w) => /長い/.test(w))).toEqual([]);
    });
  }
});

describe("書き方の確認（ブラスト・ギャロップ・トラップのロール）", () => {
  const mk = (instrument: string, notes: string) => aiSongToScore({ title: "t", description: "d", bpm: 150, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 1, autoAccompaniment: false, feel: "rock", tone: "rock", parts: [{ instrument, role: "r", volume: 0.1, pan: 0, notes }] });
  it("トラップのロール（三連・32分）が読めて、1小節=4拍に収まる。中の音は弱く、最後は強い", () => {
    for (const kind of ["triplet", "thirtysecond"] as const) {
      const r = mk("hihat", `${trapRoll(kind)} ${trapRoll(kind)} ${trapRoll(kind)} ${trapRoll(kind)}`);
      const t = r.score.tracks.find((x) => x.instrument === "hihat")!;
      expect(trackTotalBeats(t)).toBeCloseTo(16, 2);
      expect(r.warnings.filter((w) => /長い|読め/.test(w))).toEqual([]);
      const tail = t.notes.slice(t.notes.length - 1)[0];
      const weak = t.notes.find((n) => n.durationBeats < 0.34 && n.durationBeats > 0.1)!;
      expect((tail.velocity ?? 1)).toBeGreaterThan(weak.velocity ?? 1);
    }
  });
  it("ブラスト・ギャロップ・ツーバス・ブレイクダウンの格子が、そのままドラムのパートとして読める", () => {
    for (const g of [blastPattern("alternating"), blastPattern("hammer"), blastPattern("bomb"), gallop(), twoBass(150), breakdownHalftime()]) {
      for (const [inst, grid] of [["kick", g.kick], ["snare", g.snare], ["hihat", g.hat]] as const) {
        const r = mk(inst, `g:${grid}`);
        expect(trackTotalBeats(r.score.tracks.find((x) => x.instrument === inst)!)).toBeCloseTo(16, 6); // 1小節の型は曲の長さまでくり返される
      }
    }
  });
});
