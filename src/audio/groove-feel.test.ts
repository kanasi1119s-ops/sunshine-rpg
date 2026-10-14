import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { GENRE_GROOVE_MS, GROOVE_FEEL_MS, beatsToMs, grooveFeelMs, grooveRoleOf, humanTableFor, msToBeats, pushBeatsOf, ROLE_HUMAN_DEFAULT, swingOf, trackHumanMult } from "./groove-feel";
import { scoreToMidi } from "./midi-export";
import { flattenScore, getScoreDurationSec, grooveOffsetBeats, type Score, type Track } from "./score";
import { fnv, newFeatureSong, readMidi, ROCK_SONG, JAZZ_SONG, WALTZ_SONG } from "./rhythm-fixtures";

const note = (n: string, d: number, extra: Partial<Track["notes"][number]> = {}): Track["notes"][number] => ({ note: n, durationBeats: d, ...extra });
const bar16 = (inst: "kick" | "snare" | "hihat" | "bass", pitch: string, vol = 0.15): Track => ({ waveform: "square", instrument: inst, volume: vol, notes: Array.from({ length: 64 }, () => note(pitch, 0.25)) });

describe("既存の出力は変わらない（提案1〜10は省略時に今までどおり）", () => {
  it("見本曲3つ×版2つ×human 2通りの MIDI・再生用の時刻・長さが、実装前のハッシュと一致", () => {
    // jazz・waltz は dynamics: "natural" なしの曲。自動伴奏のドラムの強さ（MIDI の数字 70〜112）が MIDI 127 に張りついていたのを velocityScale で直したので、ハッシュを更新した（rock は natural なので不変）
    const want: Record<string, string> = {
      "rock|modern|undefined": "d81d0d66|e236bc4d|16", "rock|modern|0.8": "6e981f36|e236bc4d|16", "rock|real|undefined": "633e13d7|e236bc4d|16", "rock|real|0.8": "7648224e|e236bc4d|16",
      "jazz|modern|undefined": "dc831d9e|77b38a28|13.714285714285714", "jazz|modern|0.8": "f41f9e76|3b2ac85e|13.714285714285714", "jazz|real|undefined": "a703fa43|77b38a28|13.714285714285714", "jazz|real|0.8": "ea16f19c|3b2ac85e|13.714285714285714",
      // ワルツの MIDI だけは、拍子記号が 4/4 → 3/4 に直った（ほかの音は同じ。再生用の時刻と長さのハッシュは実装前と同じ）
      "waltz|modern|undefined": "99aac26a|fd10805e|15", "waltz|modern|0.8": "5204c06|fd10805e|15", "waltz|real|undefined": "1c07389f|fd10805e|15", "waltz|real|0.8": "c438d889|fd10805e|15",
    };
    for (const [name, song] of [["rock", ROCK_SONG], ["jazz", JAZZ_SONG], ["waltz", WALTZ_SONG]] as const) for (const edition of ["modern", "real"] as const) for (const human of [undefined, 0.8]) {
      const { score } = aiSongToScore({ ...song, ...(human ? { human } : {}) });
      const sc = { ...score, edition };
      expect(`${fnv(scoreToMidi(sc))}|${fnv(JSON.stringify(flattenScore(sc)))}|${getScoreDurationSec(sc)}`, `${name}|${edition}|${human}`).toBe(want[`${name}|${edition}|${human}`]);
    }
  });
  it("grooveOffsetBeats: 引数を増やしても従来の呼び方は同じ値", () => {
    expect(grooveOffsetBeats(0.6, 0.02, 1.5)).toBeCloseTo(0.02 + 0.1, 12);
    expect(grooveOffsetBeats(0.6, undefined, 1.25)).toBeCloseTo(0.05, 12);
    expect(grooveOffsetBeats(undefined, 0.01, 2.5)).toBe(0.01);
    expect(grooveOffsetBeats(0, undefined, 2.5)).toBe(0);
  });
});

describe("ミリ秒の push と ノリ（提案2）", () => {
  it("同じミリ秒が、bpm 80 と 170 で違う拍数になる（push = ms × bpm ÷ 60000）", () => {
    expect(msToBeats(10, 80)).toBeCloseTo(0.01333, 4);
    expect(msToBeats(10, 170)).toBeCloseTo(0.02833, 4);
    expect(beatsToMs(msToBeats(10, 123), 123)).toBeCloseTo(10, 9);
    expect(pushBeatsOf({ pushMs: 10 }, 80)).toBeCloseTo(0.01333, 4);
    expect(pushBeatsOf({ pushMs: 10 }, 170)).toBeCloseTo(0.02833, 4);
    // push があれば足される。pushMs の範囲は ±50
    expect(pushBeatsOf({ push: 0.01, pushMs: 10 }, 120)).toBeCloseTo(0.01 + 0.02, 9);
    expect(pushBeatsOf({ pushMs: 999 }, 120)).toBeCloseTo(0.1, 9);
    expect(pushBeatsOf({}, 120)).toBeUndefined();
    expect(pushBeatsOf({ push: 0.02 }, 120)).toBe(0.02);
  });
  it("MIDI の音の位置に pushMs が効く（120bpm で +20ms ≒ 19ティック）", () => {
    const mk = (extra: Partial<Track>): number[] => {
      const sc: Score = { tempoBpm: 120, loop: true, tracks: [{ ...bar16("snare", "C2"), ...extra }] };
      return readMidi(scoreToMidi(sc)).notes.filter((n) => n.ch === 9).map((n) => n.tick);
    };
    const base = mk({});
    const pushed = mk({ pushMs: 20 });
    // 先頭の音も含め、20ms ＝ 20 ÷ (500/480) ≒ 19.2 ティック
    expect(pushed[8] - base[8]).toBeGreaterThanOrEqual(19);
    expect(pushed[8] - base[8]).toBeLessThanOrEqual(20);
    const sc80: Score = { tempoBpm: 80, loop: true, tracks: [{ ...bar16("snare", "C2"), pushMs: 20 }] };
    const sc80b: Score = { tempoBpm: 80, loop: true, tracks: [bar16("snare", "C2")] };
    const d80 = readMidi(scoreToMidi(sc80)).notes[8].tick - readMidi(scoreToMidi(sc80b)).notes[8].tick;
    expect(d80).toBeGreaterThanOrEqual(12.8 - 1);
    expect(d80).toBeLessThanOrEqual(12.8 + 1); // 80bpm なので 20ms は 0.0267 拍＝12.8 ティック
  });
  it("再生エンジン（flattenScore）にも pushMs が効く", () => {
    const base = flattenScore({ tempoBpm: 120, loop: false, tracks: [bar16("snare", "C2")] });
    const moved = flattenScore({ tempoBpm: 120, loop: false, tracks: [{ ...bar16("snare", "C2"), pushMs: 20 }] });
    expect(moved[3].startSec - base[3].startSec).toBeCloseTo(0.02, 6);
  });
  it("役割とノリの表: 3種と全ジャンル。キックは 0 が基準", () => {
    expect(grooveRoleOf("kick")).toBe("kick");
    expect(grooveRoleOf("distGuitar")).toBe("rhythm");
    expect(grooveRoleOf("slap")).toBe("bass");
    expect(grooveFeelMs("tight", undefined, "snare")).toBe(0);
    expect(grooveFeelMs("laidback", undefined, "snare")).toBe(10);
    expect(grooveFeelMs("pushed", undefined, "hihat")).toBe(-4);
    expect(grooveFeelMs("laidback", undefined, "kick")).toBe(0);
    expect(grooveFeelMs("genre", "hiphop", "snare")).toBe(14);
    expect(grooveFeelMs("genre", "trap", "snare")).toBeUndefined();
    expect(grooveFeelMs(undefined, "hiphop", "snare")).toBeUndefined();
    for (const t of Object.values(GROOVE_FEEL_MS)) for (const v of Object.values(t)) expect(Math.abs(v)).toBeLessThanOrEqual(15);
    for (const t of Object.values(GENRE_GROOVE_MS)) for (const v of Object.values(t)) expect(Math.abs(v)).toBeLessThanOrEqual(20);
  });
  it("AIソング: grooveFeel は push／pushMs を書いていないパート（自動伴奏も）だけに入り、書いたパートが優先", () => {
    const song = { ...JAZZ_SONG, grooveFeel: "laidback", parts: [{ instrument: "snare", role: "s", volume: 0.12, pan: 0, amp: "auto", push: 0.02, notes: "g:....X.......X..." }, { instrument: "hihat", role: "h", volume: 0.1, pan: 0, amp: "auto", push: 0, notes: "g:x.x.x.x.x.x.x.x." }, { instrument: "lead", role: "l", volume: 0.2, pan: 0, amp: "auto", notes: "C5:4" }] };
    const { score } = aiSongToScore(song);
    const by = (i: string): Track[] => score.tracks.filter((t) => t.instrument === i);
    const snares = by("snare");
    expect(snares.some((t) => t.push === 0.02 && t.pushMs === undefined)).toBe(true); // 書いた push が優先
    expect(by("hihat").some((t) => t.push === undefined && t.pushMs === undefined)).toBe(true); // push: 0 と書いたパートは動かさない
    expect(by("bass")[0].pushMs).toBe(8); // 自動伴奏のベースには入る
    expect(by("lead")[0].pushMs).toBe(5);
  });
  it("AIソング: pushMs は範囲に収める。grooveFeel: genre は drumGenre が要る", () => {
    const { score, warnings } = aiSongToScore({ ...ROCK_SONG, grooveFeel: "genre", parts: [{ ...ROCK_SONG.parts[1], push: undefined, pushMs: 99 }] });
    expect(score.tracks.find((t) => t.instrument === "snare")!.pushMs).toBe(50);
    expect(warnings.some((w) => w.includes("drumGenre"))).toBe(true);
  });
});

describe("パート別の human（提案1）", () => {
  const sc = (h: number, tracks: Track[], extra: Partial<Score> = {}): Score => ({ tempoBpm: 120, loop: true, human: h, tracks, ...extra });
  const spread = (tracks: Track[], ch: number, h = 0.5, extra: Partial<Score> = {}): number => {
    const notes = readMidi(scoreToMidi(sc(h, tracks, extra))).notes.filter((n) => n.ch === ch).map((n) => n.tick);
    const dev = notes.map((t) => Math.abs(t - Math.round(t / 120) * 120));
    return dev.reduce((a, b) => a + b, 0) / dev.length;
  };
  it("human の倍率の決め方: Track.human ＞ humanRoles ＞ 1", () => {
    expect(trackHumanMult({}, { instrument: "kick" })).toBe(1);
    expect(trackHumanMult({ humanRoles: { kick: 0.5 } }, { instrument: "kick" })).toBe(0.5);
    expect(trackHumanMult({ humanRoles: { kick: 0.5 } }, { instrument: "kick", human: 1.5 })).toBe(1.5);
    expect(trackHumanMult({}, { instrument: "kick", human: 9 })).toBe(2);
    expect(trackHumanMult({}, { instrument: "kick", human: -1 })).toBe(0);
  });
  it("役割の既定（キック0.5・ベース0.8・スネア0.8・ハット1.2・ギター鍵盤1.0・リード1.2）とジャンル表", () => {
    expect(ROLE_HUMAN_DEFAULT).toMatchObject({ kick: 0.5, bass: 0.8, snare: 0.8, hihat: 1.2, rhythm: 1.0, lead: 1.2 });
    expect(humanTableFor(undefined)).toEqual(ROLE_HUMAN_DEFAULT);
    expect(humanTableFor("trap").sub).toBe(0);
    expect(humanTableFor("trap").hihat).toBeLessThan(ROLE_HUMAN_DEFAULT.hihat);
    expect(humanTableFor("ballad").hihat).toBeGreaterThan(ROLE_HUMAN_DEFAULT.hihat);
    expect(humanTableFor("unknown-genre")).toEqual(ROLE_HUMAN_DEFAULT);
  });
  it("human: 0 のパートは格子にぴったり（ほかのパートは human 0.5 でずれる）", () => {
    const exact = spread([{ ...bar16("hihat", "F#2"), human: 0 }], 9);
    const normal = spread([bar16("hihat", "F#2")], 9);
    expect(exact).toBe(0);
    expect(normal).toBeGreaterThan(1);
  });
  it("倍率が大きいほどずれる: ハット 1.6 ＞ 1 ＞ キック 0.4", () => {
    const hat16 = spread([{ ...bar16("hihat", "F#2"), human: 1.6 }], 9);
    const hat1 = spread([{ ...bar16("hihat", "F#2"), human: 1 }], 9);
    const hat04 = spread([{ ...bar16("hihat", "F#2"), human: 0.4 }], 9);
    expect(hat16).toBeGreaterThan(hat1);
    expect(hat1).toBeGreaterThan(hat04);
  });
  it("humanRoles（曲の表）が効き、Track.human が優先される", () => {
    const base = spread([bar16("bass", "E2")], 0);
    const roleLow = spread([bar16("bass", "E2")], 0, 0.5, { humanRoles: { bass: 0.2 } });
    const own = spread([{ ...bar16("bass", "E2"), human: 2 }], 0, 0.5, { humanRoles: { bass: 0.2 } });
    expect(roleLow).toBeLessThan(base);
    expect(own).toBeGreaterThan(base);
  });
  it("humanTiming／humanVelocity を別々に: ずれだけ・強さだけ", () => {
    const vel = (tr: Track): number[] => readMidi(scoreToMidi(sc(0.8, [tr]))).notes.filter((n) => n.ch === 9).map((n) => n.vel);
    const tim = (tr: Track): number => spread([tr], 9, 0.8);
    const noTiming = tim({ ...bar16("hihat", "F#2", 0.1), humanTiming: 0 });
    expect(noTiming).toBeLessThan(tim({ ...bar16("hihat", "F#2", 0.1) }));
    const sd = (a: number[]): number => { const m = a.reduce((x, y) => x + y, 0) / a.length; return Math.sqrt(a.reduce((x, y) => x + (y - m) ** 2, 0) / a.length); };
    expect(sd(vel({ ...bar16("hihat", "F#2", 0.1), humanVelocity: 0 }))).toBeLessThan(sd(vel(bar16("hihat", "F#2", 0.1))));
  });
  it("slap／sub808 は既定ではずれないが、Track.human を書くと対象になる", () => {
    const ticksOf = (extra: Partial<Track>): number[] => readMidi(scoreToMidi(sc(0.5, [{ ...bar16("bass", "E2"), instrument: "sub808", ...extra }]))).notes.filter((n) => n.ch === 0).map((n) => n.tick);
    const base = ticksOf({});
    // 既定: ずれは全体の走り溜め（どのパートも同じ）だけで、音ごとのばらつきは無い → human: 0.0001 でも同じになる側と比べる
    expect(ticksOf({ human: 1 })).not.toEqual(base);
    expect(ticksOf({})).toEqual(base);
    const grid = base.map((t, i) => t - i * 120);
    expect(Math.max(...grid) - Math.min(...grid)).toBeLessThanOrEqual(21); // 走り溜め（±10ティック）の範囲
  });
  it("AIソング: parts[].human と humanProfile が Score に入る", () => {
    const { score } = aiSongToScore({ ...ROCK_SONG, humanProfile: "role", parts: [{ ...ROCK_SONG.parts[0], human: 0, humanTiming: 0.5, humanVelocity: 1.5 }, ROCK_SONG.parts[1]] });
    expect(score.humanRoles?.hihat).toBe(1.2);
    const k = score.tracks.find((t) => t.instrument === "kick")!;
    expect(k).toMatchObject({ human: 0, humanTiming: 0.5, humanVelocity: 1.5 });
    expect(aiSongToScore({ ...ROCK_SONG, drumGenre: "ballad", humanProfile: "genre" }).score.humanRoles!.hihat).toBe(1.3);
    expect(aiSongToScore({ ...ROCK_SONG, humanProfile: "nope" }).warnings.some((w) => w.includes("humanProfile"))).toBe(true);
  });
});

describe("swing の分離（提案3）", () => {
  it("swingOf: パートの swing が曲の swing を上書き（0 でまっすぐ）。swing16 は別に持てる", () => {
    expect(swingOf({ swing: 0.6 }, {})).toEqual({ swing: 0.6, swing16: undefined });
    expect(swingOf({ swing: 0.6 }, { swing: 0 })).toEqual({ swing: 0, swing16: undefined });
    expect(swingOf({ swing: 0.6, swing16: 0.2 }, {})).toEqual({ swing: 0.6, swing16: 0.2 });
    expect(swingOf({ swing: 0.6, swing16: 0.2 }, { swing: 0.3 })).toEqual({ swing: 0.3, swing16: undefined });
    expect(swingOf({ swing: 0.6 }, { swing16: 0 })).toEqual({ swing: 0.6, swing16: 0 });
  });
  it("grooveOffsetBeats: 8分の裏と16分の裏を別の量にできる", () => {
    expect(grooveOffsetBeats(0.6, undefined, 0.5, 0)).toBeCloseTo(0.1, 12);
    expect(grooveOffsetBeats(0.6, undefined, 0.25, 0)).toBe(0);
    expect(grooveOffsetBeats(0.6, undefined, 0.75, 0.3)).toBeCloseTo(0.025, 12);
    expect(grooveOffsetBeats(0, undefined, 0.75, 0.6)).toBeCloseTo(0.05, 12);
    expect(grooveOffsetBeats(0, undefined, 0.5, 0.6)).toBe(0);
  });
  it("MIDI: キックは swing 0（まっすぐ）、ハットだけ揺らす。duck 用のキック位置もキックの swing に従う", () => {
    const kick: Track = { waveform: "sine", instrument: "kick", volume: 0.2, swing: 0, notes: [note("C2", 0.5), note("C2", 0.5), note("C2", 0.5), note("C2", 0.5)] };
    const hat: Track = { waveform: "square", instrument: "hihat", volume: 0.1, notes: [note("F#2", 0.5), note("F#2", 0.5), note("F#2", 0.5), note("F#2", 0.5)] };
    const pad: Track = { waveform: "sine", instrument: "pad", volume: 0.1, duck: 0.5, notes: [note("C4", 2)] };
    const m = readMidi(scoreToMidi({ tempoBpm: 120, loop: true, swing: 0.6, tracks: [kick, hat, pad] }));
    const drums = m.notes.filter((n) => n.ch === 9);
    // キック（pitch 36）の裏拍（0.5拍＝240 ティック）はまっすぐ
    const kicks = drums.filter((n) => n.pitch === 36).map((n) => n.tick);
    const hats = drums.filter((n) => n.pitch === 42 || n.pitch === 44 || n.pitch === 46).map((n) => n.tick);
    expect(Math.abs(kicks[1] - 240)).toBeLessThan(12);
    expect(hats[1] - 240).toBeGreaterThan(40); // swing 0.6 → 0.1拍＝48ティック遅れ
  });
  it("AIソング: parts[].swing／swing16 と曲の swing16 が入る", () => {
    const { score } = aiSongToScore({ ...ROCK_SONG, swing16: 0.1, parts: [{ ...ROCK_SONG.parts[0], swing: 0 }, ROCK_SONG.parts[2]] });
    expect(score.swing16).toBe(0.1);
    expect(score.tracks.find((t) => t.instrument === "kick")!.swing).toBe(0);
    expect(score.tracks.find((t) => t.instrument === "hihat")!.swing).toBeUndefined();
  });
});

describe("lockToKick（提案8）", () => {
  const kick: Track = { waveform: "sine", instrument: "kick", volume: 0.2, notes: Array.from({ length: 16 }, () => note("C2", 1)) };
  const bass = (extra: Partial<Track> = {}): Track => ({ waveform: "sawtooth", instrument: "bass", volume: 0.25, ...extra, notes: Array.from({ length: 16 }, () => note("E1", 1)) });
  const ticks = (score: Score): { k: number[]; b: number[] } => {
    const m = readMidi(scoreToMidi(score));
    return { k: m.notes.filter((n) => n.ch === 9 && n.pitch === 36).map((n) => n.tick), b: m.notes.filter((n) => n.ch !== 9 && n.pitch === 28).map((n) => n.tick) };
  };
  it("human を上げても、重なる音のずれの差が 0 になる（ロックなしでは差が出る）", () => {
    const free = ticks({ tempoBpm: 120, loop: true, human: 0.8, tracks: [kick, bass()] });
    expect(free.k.some((t, i) => t !== free.b[i])).toBe(true);
    const locked = ticks({ tempoBpm: 120, loop: true, human: 0.8, tracks: [kick, bass({ lockToKick: true })] });
    expect(locked.k.length).toBe(16);
    expect(locked.k.map((t, i) => t - locked.b[i])).toEqual(new Array(16).fill(0));
    // 曲全体の指定でもベースに効く
    const viaScore = ticks({ tempoBpm: 120, loop: true, human: 0.8, lockToKick: true, tracks: [kick, bass()] });
    expect(viaScore.k.map((t, i) => t - viaScore.b[i])).toEqual(new Array(16).fill(0));
  });
  it("キックから遠い音（0.25拍をこえる）は、ロックされない", () => {
    const off = bass({ lockToKick: true });
    off.notes = Array.from({ length: 16 }, () => note("E1", 1));
    const kickWide: Track = { ...kick, notes: [note("C2", 2), ...Array.from({ length: 7 }, () => note("C2", 2)), note("R", 0)].slice(0, 8) };
    const t = ticks({ tempoBpm: 120, loop: true, human: 0.8, tracks: [kickWide, off] });
    // 奇数拍のベース（キックは偶数拍だけ）は、直前のキックから1拍離れているのでロックされない
    expect(t.b.length).toBeGreaterThan(t.k.length);
  });
  it("push の差は残る（ベースだけあと乗り）", () => {
    const t = ticks({ tempoBpm: 120, loop: true, human: 0.5, tracks: [kick, bass({ lockToKick: true, pushMs: 10 })] });
    for (let i = 1; i < 16; i++) expect(t.b[i] - t.k[i]).toBeGreaterThanOrEqual(9);
  });
  it("AIソング: lockToKick は曲全体にもパートにも書ける", () => {
    expect(aiSongToScore({ ...ROCK_SONG, lockToKick: true }).score.lockToKick).toBe(true);
    const { score } = aiSongToScore({ ...ROCK_SONG, parts: [{ ...ROCK_SONG.parts[3], lockToKick: true }] });
    expect(score.tracks.find((t) => t.instrument === "bass")!.lockToKick).toBe(true);
  });
});

describe("ずれの分布（提案9）", () => {
  const dev = (score: Score): number[] => {
    const m = readMidi(scoreToMidi(score));
    return m.notes.filter((n) => n.ch === 9).map((n) => n.tick - Math.round(n.tick / 120) * 120).filter((d) => Math.abs(d) < 60);
  };
  const tr: Track = { waveform: "square", instrument: "hihat", volume: 0.1, notes: Array.from({ length: 400 }, () => note("F#2", 0.25)) };
  it("humanDist 省略は今までどおり（一様）。triangle は同じ最大幅で、中心に寄る", () => {
    const uni = dev({ tempoBpm: 120, loop: true, human: 0.9, tracks: [tr] });
    const tri = dev({ tempoBpm: 120, loop: true, human: 0.9, humanDist: "triangle", tracks: [tr] });
    const sd = (a: number[]): number => { const m = a.reduce((x, y) => x + y, 0) / a.length; return Math.sqrt(a.reduce((x, y) => x + (y - m) ** 2, 0) / a.length); };
    expect(Math.max(...tri.map(Math.abs))).toBeLessThanOrEqual(Math.max(...uni.map(Math.abs)) + 1);
    expect(sd(tri)).toBeLessThan(sd(uni));
    const extreme = (a: number[]): number => a.filter((d) => Math.abs(d) > 0.8 * Math.max(...uni.map(Math.abs))).length;
    expect(extreme(tri)).toBeLessThan(extreme(uni));
  });
  it("AIソング: humanDist: \"triangle\"", () => {
    expect(aiSongToScore({ ...ROCK_SONG, humanDist: "triangle" }).score.humanDist).toBe("triangle");
    expect(aiSongToScore(ROCK_SONG).score.humanDist).toBeUndefined();
  });
});

describe("新しい項目を使っても、使わない曲は変わらない", () => {
  it("newFeatureSong を何も足さずに作ると ROCK_SONG と同じ", () => {
    expect(JSON.stringify(aiSongToScore(newFeatureSong()).score)).toBe(JSON.stringify(aiSongToScore(ROCK_SONG).score));
  });
});

describe("velocityScale: 自動伴奏のドラムの強さ（MIDI の数字）が 127 に張りつかない", () => {
  it("dynamics なしの曲でも、ドラムの MIDI ベロシティに強弱が残る", async () => {
    const { velocityScale } = await import("./score");
    expect(velocityScale(undefined)).toBe(1);
    expect(velocityScale(1.3)).toBe(1.3);
    expect(velocityScale(80)).toBeCloseTo(0.8, 12);
    const { score } = aiSongToScore({ ...JAZZ_SONG, dynamics: undefined });
    const midi = scoreToMidi(score);
    const vels: number[] = [];
    for (let i = 0; i < midi.length - 2; i++) if ((midi[i] & 0xf0) === 0x90 && (midi[i] & 0x0f) === 9 && midi[i + 2] > 0 && midi[i + 1] < 128 && midi[i + 2] < 128) vels.push(midi[i + 2]);
    expect(vels.length).toBeGreaterThan(10);
    expect(new Set(vels).size).toBeGreaterThan(3);
    expect(vels.filter((v) => v === 127).length / vels.length).toBeLessThan(0.3);
  });
});
