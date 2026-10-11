import { describe, expect, it } from "vitest";
import { AI_SONG_GUIDE, AI_SONG_SCHEMA, aiSongToScore, type AiPart, type AiSong } from "./ai-song";
import { AMP_PRESETS } from "./amp";
import { GENRE_AMP_TYPES } from "./amp-rack";
import { autoSections, type Section } from "./arrangement";
import {
  applyRecipe, AI_SONG_JPOP_GUIDE, bareKindsOf, CUT16_GRIDS, expandBare, expandCut16, expandGuitarPair, expandReverbPre, expandSectionFx, expandWiden,
  holdFirstNotes, transposeNotesText,
} from "./jpop-clean";
import { applyJpopSong, jpopFeelSong } from "./jpop-feel";
import { noteNameToMidi } from "./note";
import { buildNewSong, NEW_SONG_FEELS } from "./newsong";
import { chordBarsOf, expandEcho, expandParts, strumVoicing, type ExpandCtx } from "./part-expand";
import { PART_RECIPES } from "./sound-sets";
import { REST, type Track } from "./score";
import masterSource from "../../tools/composer/master.mjs?raw";

const fnv = (s: string): string => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, "0"); };
const CHORDS = "C G Am F";
const SECTIONS: Section[] = [{ kind: "intro", bars: 4 }, { kind: "verse", bars: 4 }, { kind: "chorus", bars: 8 }];
const ctx = (over: Partial<ExpandCtx> = {}): ExpandCtx => ({
  bpm: 120, beatsPerBar: 4, totalBeats: 64, chordBars: chordBarsOf(CHORDS, 1, 4), tonic: null, scale: null, sections: SECTIONS, ...over,
});
const guitar = (over: Partial<AiPart> = {}): AiPart => ({ instrument: "guitar", role: "ギター", volume: 0.16, pan: -0.3, amp: "auto", notes: "E4:1 G4:1 C5:1 G4:1", ...over }) as AiPart;
const song = (over: Partial<AiSong> = {}): AiSong => ({
  title: "テスト", description: "テスト", bpm: 120, beats: 4, chords: CHORDS, barsPerChord: 1, repeats: 4, autoAccompaniment: false, feel: "pop", tone: "rock",
  parts: [guitar()], ...over,
}) as AiSong;
const total = (t: Track): number => t.notes.reduce((s, n) => s + n.durationBeats, 0);
const midiOf = (t: Track): number[] => t.notes.filter((n) => n.note !== REST).map((n) => noteNameToMidi(n.note));

describe("既存の曲は変わらない（オプトイン）", () => {
  // 実装前（6ea86497）の aiSongToScore の出力のハッシュ。assets-src/ai-songs の全曲と、既存の feel（jpop 以外）の伴奏
  const BASE_SONGS: Record<string, string> = { "auto-sections-demo": "64d093b6", "autumn-dusk-bass-melody": "5a7c6ecc", "autumn-dusk-love": "ff121c8b", "band-pedal-arpeggio": "0f199a18", "bass-demo-bossa": "a63882c3", "bass-demo-funk": "4c0467f3", "bass-demo-reggae": "74351212", "bass-demo-walking": "b695b2c5", "boss-crimson-gate": "15ea5bf1", "caravan-hijaz": "a8ce3a18", "clear-sky-arpeggio": "d23af449", "clear-sky-odd7": "fa9891cb", "clear-sky-trio": "2527b46e", "dance-demo": "28f6ec33", "delicate-demo": "293a4cfc", "ember-throne": "d1dd3f8e", "fill-showcase-rock": "ba608683", "folk-ethnic-demo": "ae54daf5", "guitar-arpeggio-jazz": "9d07ed17", "guitar-arpeggio-rock": "b4ccf537", "harbor-night": "dfebe38e", "hiphop-demo": "2785a3ed", "intro-bass-first": "45cbbf0b", "intro-cold-strike": "0f56c1dc", "intro-hook-first": "10621a4b", "iron-pulse": "3134dc3d", "loud-metal-demo": "5bfd91c9", "loud-rock-demo": "ea57d9df", "melocore-shissou": "5a1eb595", "neon-circuit": "9dcfb314", "neon-dawn-road": "e6611a3e", "rhythm-groove-demo": "b64eef99", "scarlet-chapter-space-long": "86019bbc", "scene-battle-dust-scout": "a33bef40", "scene-edm-build-drop-dawn": "173c7548", "scene-ending-homeward-light": "2d1f6700", "sky-piercing-pulse-clean": "380b96a9", "sky-piercing-pulse": "582fb24d", "summer-vocaloid-demo": "5e4acc04", "synth-patch-tour-1": "c8e33a5e", "synth-patch-tour-2": "b93e9ad1", "vocaloid-style-demo": "18b08928" };
  const BASE_FEELS: Record<string, string> = { rock: "f40e3674", pop: "d3251b66", ballad: "9e650a02", dance: "9bba2faa", vocaloid: "0dbbb83d", funk: "5e480cf3", reggae: "d0856edc", bossa: "e6eded77", jazz: "42b591ee", shuffle: "ae466cb9", metal: "07b6a26b", disco: "7a2e6803", hiphop: "0e4ce23b", trap: "375797c9", dnb: "9a8ac7d4", halftime: "c7d22d65" };
  it("assets-src/ai-songs の実装前からある42曲のスコアが、実装前とまったく同じ（あとから足した曲は見ない）", () => {
    const files = import.meta.glob("../../assets-src/ai-songs/*.json", { eager: true, import: "default" }) as Record<string, unknown>;
    const now: Record<string, string> = {};
    for (const [k, v] of Object.entries(files)) {
      const id = k.split("/").pop()!.replace(/\.json$/, "");
      if (id in BASE_SONGS) now[id] = fnv(JSON.stringify(aiSongToScore(JSON.parse(JSON.stringify(v))).score));
    }
    expect(Object.keys(now).sort()).toEqual(Object.keys(BASE_SONGS).sort());
    expect(now).toEqual(BASE_SONGS);
  }, 60000);
  it("jpop 以外の feel の伴奏が、実装前とまったく同じ", () => {
    const now: Record<string, string> = {};
    for (const f of NEW_SONG_FEELS) if (f !== "jpop") now[f] = fnv(JSON.stringify(buildNewSong({ bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2, feel: f, leadInstrument: "lead" })));
    expect(now).toEqual(BASE_FEELS);
  });
});

describe("提案2: AIへの指示文に、クリーンギターの出発点の例がある", () => {
  it("AI_SONG_GUIDE の末尾に入り、浅い chorus を許し、各レシピと新しい項目に触れている", () => {
    expect(AI_SONG_GUIDE.endsWith(AI_SONG_JPOP_GUIDE)).toBe(true);
    for (const w of ["浅い chorus", "jpopClean", "cut16", "recipe", "sparkle-delay", "crystal-wide", "sparkle-wide-delay", "dimension", "sectionFx", "guitarPair", "reverbPre", "bare", "feel\":\"jpop", "jpop-band", "slap", "\"ms\":30"]) expect(AI_SONG_JPOP_GUIDE, w).toContain(w);
  });
  it("スキーマに新しい項目が入っている", () => {
    const part = (AI_SONG_SCHEMA.properties.parts.items.properties) as Record<string, unknown>;
    for (const k of ["recipe", "widen", "sectionFx", "guitarPair", "bare", "reverbPre", "cutGrid"]) expect(part[k], k).toBeDefined();
    expect((AI_SONG_SCHEMA.properties as Record<string, unknown>).bare).toBeDefined();
    expect((AI_SONG_SCHEMA.properties.feel as { enum: readonly string[] }).enum).toContain("jpop");
  });
});

describe("提案1: 新ロール jpopClean", () => {
  it("amp.ts・amp-rack・AIソングのアンプ名にそろっている", () => {
    expect(AMP_PRESETS.jpopClean.drive).toBe(1);
    expect(AMP_PRESETS.jpopClean.lowpassHz).toBeLessThanOrEqual(9000);
    expect(GENRE_AMP_TYPES).toContain("jpopClean");
    const amp = (AI_SONG_SCHEMA.properties.parts.items.properties.amp as { enum: readonly string[] }).enum;
    expect(amp).toContain("jpopClean");
  });
  it("パートに amp: jpopClean を書くと、そのまま使われる（警告なし）", () => {
    const { score, warnings } = aiSongToScore(song({ parts: [guitar({ amp: "jpopClean" })] }));
    expect(score.tracks[0].amp?.type).toBe("jpopClean");
    expect(warnings.filter((w) => w.includes("アンプ"))).toEqual([]);
  });
});

describe("提案11: 仕上げのプリセット jpop-band", () => {
  it("rock-clean をもとに、250Hz -1・2kHz +0.5・8kHz 高域 +1.5 を足している", () => {
    const line = (id: string): string => masterSource.split("\n").find((l) => l.trimStart().startsWith(`"${id}":`)) ?? "";
    const rock = line("rock-clean");
    const jpop = line("jpop-band");
    expect(jpop).not.toBe("");
    // 大きさ・広がり・圧縮などは rock-clean と同じ
    for (const part of ["lufs: -10", "widen: 1.25", "glue: \"bus2\"", "hpf: 25", "type: \"peak\", f: 100, g: 0.5", "type: \"hs\", f: 6000, g: 1"]) { expect(rock).toContain(part); expect(jpop).toContain(part); }
    for (const part of ["f: 250, g: -1", "f: 2000, g: 0.5", "type: \"hs\", f: 8000, g: 1.5"]) { expect(jpop).toContain(part); expect(rock).not.toContain(part); }
  });
});

describe("提案3: echo の ms と slap", () => {
  const p = guitar({ volume: 0.2 });
  it("ms は BPM に合わせて拍にする（BPM120で30ms＝0.06拍）。repeats の標準は1、decay は0.8まで使える", () => {
    const out = expandEcho(p, { ms: 30, decay: 0.8 }, [], 120);
    expect(out).toHaveLength(2);
    expect(out[1].shift).toBeCloseTo(0.06, 6);
    expect(out[1].volume).toBeCloseTo(0.16, 3);
    expect(expandEcho(p, { ms: 30 }, [], 60)[1].shift).toBeCloseTo(0.03, 6);
  });
  it("slap は約0.07拍・1回・decay 0.8", () => {
    const out = expandEcho(p, { time: "slap" }, [], 120);
    expect(out).toHaveLength(2);
    expect(out[1].shift).toBeCloseTo(0.07, 6);
    expect(out[1].volume).toBeCloseTo(0.16, 3);
  });
  it("拍で書く今までの echo は変わらない（decay は0.6まで、標準は2回）", () => {
    const out = expandEcho(p, { time: "dotted8", decay: 0.9 }, [], 120);
    expect(out).toHaveLength(3);
    expect(out[1].volume).toBeCloseTo(0.12, 3);
    expect(out[1].shift).toBe(0.75);
  });
  it("すでに shift があるパート（widen の右側など）に重ねると、その分が足される", () => {
    const out = expandEcho(guitar({ shift: 0.024 }), { ms: 30 }, [], 120);
    expect(out[1].shift).toBeCloseTo(0.084, 6);
  });
  it("ms の範囲外は丸める（1〜400）", () => {
    expect(expandEcho(p, { ms: 9999 }, [], 120)[1].shift).toBeCloseTo(0.8, 6);
  });
});

describe("提案4: widen dimension", () => {
  it("同じ旋律を左右に置き、右だけ ms 遅らせて浅い chorus。pan は ±0.7 まで、音量は 0.75 倍", () => {
    const out = expandWiden(guitar({ pan: 0 }), "dimension", ctx());
    expect(out).toHaveLength(2);
    expect(out[0].pan).toBeCloseTo(-0.6, 6);
    expect(out[1].pan).toBeCloseTo(0.6, 6);
    expect(out[1].shift).toBeCloseTo(0.024, 6); // 12ms @120
    expect(out[0].shift).toBeUndefined();
    expect(out[1].chorus).toBe(0.25);
    expect(out[0].volume).toBeCloseTo(0.12, 3);
    expect(out[0].notes).toBe(out[1].notes);
  });
  it("width は0.7、ms は5〜20に丸める（モノラルで痩せにくくする）", () => {
    const out = expandWiden(guitar({ pan: 0 }), { width: 1, ms: 100 }, ctx());
    expect(out[1].pan).toBeCloseTo(0.7, 6);
    expect(out[1].shift).toBeCloseTo(0.04, 6); // 20ms @120
  });
  it("曲に通すと、パートが2つ（L・R）になる", () => {
    const { score } = aiSongToScore(song({ parts: [guitar({ widen: "dimension" })] }));
    expect(score.tracks).toHaveLength(2);
    expect(score.tracks[0].pan).toBeCloseTo(-0.9, 6);
    expect(score.tracks[1].pan).toBeCloseTo(0.3, 6);
    expect(score.tracks[1].chorus).toBe(0.25);
  });
});

describe("提案5: sectionFx", () => {
  const fx = { intro: { reverb: 0.4, chorus: 0.4 }, chorus: { reverb: 0.15, chorus: 0.05 } };
  it("効果量が違うセクションの組ごとにパートを分け、ほかのセクションは休む", () => {
    const out = expandSectionFx(guitar({ reverb: 0.25, chorus: 0.2 }), fx, ctx(), []);
    expect(out).toHaveLength(3); // intro / verse（パートの値のまま）/ chorus
    const byIntro = out.find((p) => (p.sections as Record<string, number>).intro === 1)!;
    expect(byIntro.reverb).toBe(0.4);
    expect(byIntro.chorus).toBe(0.4);
    expect(byIntro.sections).toMatchObject({ intro: 1, verse: 0, chorus: 0 });
    const byVerse = out.find((p) => (p.sections as Record<string, number>).verse === 1)!;
    expect(byVerse.reverb).toBe(0.25);
    expect(byVerse.chorus).toBe(0.2);
    const byChorus = out.find((p) => (p.sections as Record<string, number>).chorus === 1)!;
    expect(byChorus.reverb).toBe(0.15);
    expect(byChorus.chorus).toBe(0.05);
  });
  it("同じ効果量のセクションは1つのパートにまとまる／1種類だけなら分けない", () => {
    const out = expandSectionFx(guitar(), { intro: { reverb: 0.4 }, verse: { reverb: 0.4 }, chorus: { reverb: 0.4 } }, ctx(), []);
    expect(out).toHaveLength(1);
    expect(out[0].reverb).toBe(0.4);
    expect(out[0].sections).toBeUndefined();
  });
  it("書いてあった sections の指定は、鳴らす側に残る", () => {
    const out = expandSectionFx(guitar({ sections: { chorus: 0.5 } }), fx, ctx(), []);
    expect(out.find((p) => (p.sections as Record<string, number>).chorus === 0.5)).toBeDefined();
  });
  it("sections がないときは警告して、パートのまま", () => {
    const w: string[] = [];
    expect(expandSectionFx(guitar(), fx, ctx({ sections: undefined }), w)).toHaveLength(1);
    expect(w.join()).toContain("sections");
  });
  it("曲に通すと、サビの部分だけ別チャンネル（別の残響量）の音になり、ほかは休む", () => {
    const { score } = aiSongToScore(song({ sections: [...SECTIONS], parts: [guitar({ reverb: 0.25, sectionFx: fx })] }));
    expect(score.tracks).toHaveLength(3);
    const chorusTrack = score.tracks.find((t) => t.reverb === 0.15)!;
    let pos = 0;
    for (const n of chorusTrack.notes) { expect(n.note === REST || pos >= 32 - 1e-6, `pos ${pos}`).toBe(true); pos += n.durationBeats; }
    expect(total(chorusTrack)).toBeCloseTo(64, 6);
  });
  it("sections も scene もない曲では、sections:auto を補って警告する", () => {
    const { score, warnings } = aiSongToScore(song({ parts: [guitar({ sectionFx: fx })] }));
    expect(warnings.join()).toContain("sections");
    expect(score.tracks.length).toBeGreaterThanOrEqual(2);
  });
});

describe("提案8: guitarPair（2本のギターの役割分担）", () => {
  it("1本目は左・クリーン＋chorus、2本目は右・浅い crunch の小音量で、サビだけ鳴る", () => {
    const out = expandGuitarPair(guitar({ volume: 0.16, pan: -0.3 }), true, ctx(), []);
    expect(out).toHaveLength(2);
    expect(out[0]).toMatchObject({ pan: -0.3, chorus: 0.3, instrument: "guitar" });
    expect(out[1]).toMatchObject({ pan: 0.3, instrument: "crunch", amp: "crunch", chorus: 0 });
    expect(out[1].volume).toBeLessThanOrEqual(0.1);
    expect(out[1].sections).toMatchObject({ intro: 0, verse: 0, chorus: 1 });
    expect(out[0].sections).toBeUndefined();
  });
  it("octave は1オクターブ上のクリーン（E5をこえる音は動かさない）、only で鳴るセクションを選べる", () => {
    const out = expandGuitarPair(guitar({ notes: "E4:1 C5:1 E5:1" }), { mode: "octave", only: ["verse", "chorus"] }, ctx(), []);
    expect(out[1].notes).toBe("E5:1 C5:1 E5:1");
    expect(out[1].instrument).toBe("guitar");
    expect(out[1].sections).toMatchObject({ intro: 0, verse: 1, chorus: 1 });
  });
  it("transposeNotesText: 休みと長さの記号はそのまま", () => {
    expect(transposeNotesText("C4:1! R:2 E4:0.5,'", 12)).toBe("C5:1! R:2 E5:0.5,'");
  });
  it("曲に通すと2パートになり、2本目のサビ以外は休み", () => {
    const { score } = aiSongToScore(song({ sections: [...SECTIONS], parts: [guitar({ guitarPair: true })] }));
    expect(score.tracks).toHaveLength(2);
    const second = score.tracks[1];
    expect(second.instrument).toBe("crunch");
    let pos = 0;
    for (const n of second.notes) { expect(n.note === REST || pos >= 32 - 1e-6).toBe(true); pos += n.durationBeats; }
  });
});

describe("提案12: reverbPre", () => {
  it("元のパートの残響を0にし、遅らせた小さな複製（暗め・音量0.3倍）に残響を載せる", () => {
        const withPre = expandReverbPre(guitar({ volume: 0.2, reverb: 0.3, reverbPre: 12 }), ctx(), []);
    expect(withPre).toHaveLength(2);
    expect(withPre[0].reverb).toBe(0);
    expect(withPre[1].reverb).toBeCloseTo(0.55, 6);
    expect(withPre[1].volume).toBeCloseTo(0.06, 3);
    expect(withPre[1].bright).toBeCloseTo(-0.3, 6);
    expect(withPre[1].shift).toBeCloseTo(0.024, 6); // 12ms @120
    expect(withPre[0].reverbPre).toBeUndefined();
  });
  it("名前（room＝10ms・ballad＝70ms）と範囲（0〜120ms）", () => {
    expect(expandReverbPre(guitar({ reverbPre: "ballad" }), ctx(), [])[1].shift).toBeCloseTo(0.14, 6);
    expect(expandReverbPre(guitar({ reverbPre: 9999 }), ctx(), [])[1].shift).toBeCloseTo(0.24, 6);
    expect(expandReverbPre(guitar({ reverbPre: 0 }), ctx(), [])).toHaveLength(1);
    const w: string[] = [];
    expect(expandReverbPre(guitar({ reverbPre: "x" as unknown as number }), ctx(), w)).toHaveLength(1);
    expect(w.join()).toContain("reverbPre");
  });
  it("曲に通すと、直接音のトラックの残響が0、複製のトラックに残響が載る", () => {
    const { score } = aiSongToScore(song({ parts: [guitar({ reverb: 0.3, reverbPre: 12 })] }));
    expect(score.tracks).toHaveLength(2);
    expect(score.tracks[0].reverb).toBe(0);
    expect(score.tracks[1].reverb).toBeGreaterThan(0.3);
  });
});

describe("提案9: bare（引き算のセクション）", () => {
  const bareSong = (over: Partial<AiSong> = {}, parts: AiPart[] = [guitar()]): AiSong => song({ autoAccompaniment: true, sections: [...SECTIONS], bare: ["verse"], parts, ...over });
  it("曲の bare は、自動の伴奏の layers に、小節の頭の音だけをのばす層を入れる（layers に書いた種類は書いた方）", () => {
    const out = applyJpopSong(bareSong({ layers: { chorus: ["kick"] } }), []);
    expect(out.layers?.verse).toMatchObject({ hold: true, groups: ["bass", "keys", "guitar", "strings"] });
    expect(out.layers?.chorus).toEqual(["kick"]);
    const out2 = applyJpopSong(bareSong({ layers: { verse: ["bass"] } }), []);
    expect(out2.layers?.verse).toEqual(["bass"]);
  });
  it("自動の伴奏のベースが、Aメロの区間では各小節の最初の音を小節いっぱいにのばす", () => {
    const { score } = aiSongToScore(bareSong());
    const bass = score.tracks.find((t) => t.instrument === "bass")!;
    let pos = 0;
    const inVerse = [];
    for (const n of bass.notes) { if (pos >= 16 - 1e-6 && pos < 32 - 1e-6) inVerse.push(n); pos += n.durationBeats; }
    expect(inVerse.length).toBeGreaterThan(0);
    for (const n of inVerse) expect(n.durationBeats).toBe(4);
  });
  it("手書きの bare: mute はそのセクションを休み、ほかは鳴る", () => {
    const { score } = aiSongToScore(bareSong({}, [guitar({ bare: "mute" })]));
    const g = score.tracks.find((t) => t.instrument === "guitar" && t.volume === 0.16)!;
    let pos = 0;
    let sounding = 0;
    for (const n of g.notes) {
      if (pos >= 16 - 1e-6 && pos < 32 - 1e-6) expect(n.note).toBe(REST);
      else if (n.note !== REST) sounding++;
      pos += n.durationBeats;
    }
    expect(sounding).toBeGreaterThan(0);
  });
  it("hold は、bare の小節の最初の音だけを小節いっぱいにのばす（それ以外の小節は変えない）", () => {
    const out = holdFirstNotes("E4:1 G4:1 C5:1 G4:1", 16, 4, [[4, 8]]);
    const toks = out!.split(" ");
    expect(toks.slice(0, 4)).toEqual(["E4:1", "G4:1", "C5:1", "G4:1"]);
    expect(toks[4]).toBe("E4:4");
    expect(toks).toHaveLength(4 + 1 + 8);
  });
  it("hold は、小節をまたぐ長い音を割り、先頭が休みの小節は休みのまま。アクセントは外す", () => {
    expect(holdFirstNotes("C4:6! D4:2", 8, 4, [[0, 8]])).toBe("C4:4 C4:4");
    expect(holdFirstNotes("R:4 E4:1", 8, 4, [[0, 4]])!.startsWith("R:4")).toBe(true);
  });
  it("パートの bare は、曲の bare の種類（なければ Aメロ）に合わせてそろえる", () => {
    const out = applyJpopSong(bareSong({ bare: ["verse", "pre"] }, [guitar({ bare: "hold" })]), []);
    expect(out.parts[0].bare).toEqual({ mode: "hold", kinds: ["verse", "pre"] });
    expect(bareKindsOf(guitar({ bare: "mute" }))).toEqual(["verse"]);
    const o = expandBare(guitar({ bare: { mode: "hold", kinds: ["verse"] } }), ctx(), []);
    expect(o).toHaveLength(1);
    expect(o[0].notes).toContain("E4:4");
  });
  it("bare を書かない曲・パートは変わらない", () => {
    const s = song();
    expect(applyJpopSong(s, [])).toBe(s);
  });
});

describe("提案6: pattern cut16（消す音付きのカッティング）", () => {
  const out = expandCut16(guitar({ pattern: "cut16", notes: "" }), ctx(), [], strumVoicing);
  it("和音の上の3声のパートに展開され、どれも曲の長さにぴったり合う", () => {
    expect(out).toHaveLength(3);
    for (const p of out) {
      const { score } = aiSongToScore(song({ parts: [p] }));
      expect(total(score.tracks[0])).toBeCloseTo(64, 6);
    }
  });
  it("型のとおり、消す音（休み）が入り、弾く音は短く、1拍目の頭だけがのびる", () => {
    const toks = out[0].notes.split(" ");
    expect(toks[0]).toMatch(/^[A-G]#?\d:0\.5!$/); // X-（2ステップ＝0.5拍、アクセント）
    expect(toks[1]).toBe("R:0.5");
    expect(toks.some((t) => t.startsWith("R:"))).toBe(true);
    expect(toks.filter((t) => t.endsWith(",'")).length).toBeGreaterThan(0); // o＝弱い消す音
    expect(toks.filter((t) => t.endsWith("'") && !t.endsWith(",'")).length).toBeGreaterThan(0); // x＝切る
    // 同じ高さの単音の連打にならない（和音の構成音が変わる）
    const pitches = new Set(out.map((p) => p.notes.split(" ")[0]));
    expect(pitches.size).toBe(3);
  });
  it("音は E3〜E5 の中（低い音は使わない）、音量は3声で分け合う", () => {
    for (const p of out) {
      const { score } = aiSongToScore(song({ parts: [p] }));
      for (const m of midiOf(score.tracks[0])) { expect(m).toBeGreaterThanOrEqual(noteNameToMidi("E3")); expect(m).toBeLessThanOrEqual(noteNameToMidi("E5")); }
      expect(p.volume).toBeLessThan(0.16);
    }
  });
  it("cutGrid は名前か16文字。まちがいは警告して pattern を使わない", () => {
    for (const name of Object.keys(CUT16_GRIDS)) expect(CUT16_GRIDS[name]).toHaveLength(16);
    const sparse = expandCut16(guitar({ pattern: "cut16", cutGrid: "sparse", notes: "" }), ctx(), [], strumVoicing);
    expect(sparse[0].notes).not.toBe(out[0].notes);
    const w: string[] = [];
    const bad = expandCut16(guitar({ pattern: "cut16", cutGrid: "zzz", notes: "" }), ctx(), w, strumVoicing);
    expect(bad).toHaveLength(1);
    expect(w.join()).toContain("cutGrid");
  });
  it("曲に通す（expandParts 経由）と3パートになる", () => {
    const { score, warnings } = aiSongToScore(song({ parts: [guitar({ pattern: "cut16", notes: "" })] }));
    expect(score.tracks).toHaveLength(3);
    expect(warnings.filter((w) => w.includes("pattern"))).toEqual([]);
  });
});

describe("名前付きのレシピ（PART_RECIPES）", () => {
  it("人間が気に入った3つが登録されている（ディレイは弱め: repeats 1・decay 0.15）", () => {
    expect(PART_RECIPES["sparkle-delay"].mix.amp?.type).toBe("sparkleClean");
    expect(PART_RECIPES["sparkle-delay"].fx?.echo).toMatchObject({ repeats: 1, decay: 0.15 });
    expect(PART_RECIPES["crystal-wide"].mix.amp?.type).toBe("crystal");
    expect(PART_RECIPES["crystal-wide"].fx?.doubleDetune).toBeDefined();
    expect(PART_RECIPES["crystal-wide"].fx?.echo).toBeUndefined();
    expect(PART_RECIPES["sparkle-wide-delay"].mix.amp?.type).toBe("sparkleClean");
    expect(PART_RECIPES["sparkle-wide-delay"].fx).toMatchObject({ doubleDetune: {}, echo: { repeats: 1, decay: 0.15 } });
  });
  it("J-POP のレシピA〜E（jpop-arpeggio・cutting・stroke・space・dimension）がある", () => {
    for (const id of ["jpop-arpeggio", "jpop-cutting", "jpop-stroke", "jpop-space", "jpop-dimension"]) {
      expect(PART_RECIPES[id], id).toBeDefined();
      expect(PART_RECIPES[id].mix.amp?.type).toBe("jpopClean");
    }
    expect(PART_RECIPES["jpop-cutting"].hint?.pattern).toBe("cut16");
  });
  it("applyRecipe は、書いていない項目だけ補う（amp が auto のときだけ amp も補う）", () => {
    const a = applyRecipe(guitar({ recipe: "sparkle-delay" }), []);
    expect(a).toMatchObject({ amp: "sparkleClean", reverb: 0.25, sustain: 1.5, echo: { repeats: 1, decay: 0.15 } });
    expect(a.recipe).toBeUndefined();
    const b = applyRecipe(guitar({ recipe: "sparkle-delay", amp: "crystal", reverb: 0.5, echo: { repeats: 2 } }), []);
    expect(b).toMatchObject({ amp: "crystal", reverb: 0.5, echo: { repeats: 2 } });
    const w: string[] = [];
    expect(applyRecipe(guitar({ recipe: "nothing" }), w).recipe).toBeUndefined();
    expect(w.join()).toContain("nothing");
  });
  it("曲に通すと、sparkle-delay＝本体＋エコー1つ、crystal-wide＝左右2本、sparkle-wide-delay＝左右2本それぞれにエコー1つ", () => {
    const run = (recipe: string) => aiSongToScore(song({ parts: [guitar({ recipe })] })).score.tracks;
    const delay = run("sparkle-delay");
    expect(delay).toHaveLength(2);
    expect(delay.every((t) => t.amp?.type === "sparkleClean")).toBe(true);
    expect(delay[1].volume).toBeCloseTo(0.16 * 0.15, 3);
    const wide = run("crystal-wide");
    expect(wide).toHaveLength(2);
    expect(wide.every((t) => t.amp?.type === "crystal")).toBe(true);
    expect(wide.map((t) => t.pan)).toEqual([-0.8, 0.2]);
    expect(wide.map((t) => t.detune)).toEqual([-8, 8]);
    const both = run("sparkle-wide-delay");
    expect(both).toHaveLength(4);
  });
  it("expandParts を直接呼んでも、書いた項目が優先される", () => {
    const out = expandParts([guitar({ recipe: "crystal-wide", doubleDetune: { cents: 3, spread: 0.2 } })], ctx(), [], new Set());
    expect(out.map((p) => p.detune)).toEqual([-3, 3]);
  });
});

describe("提案7: feel jpop の自動伴奏", () => {
  const spec = { bpm: 120, beats: 4, chords: "Am F C G", barsPerChord: 1, repeats: 2, leadInstrument: "lead" as const };
  const pop = buildNewSong({ ...spec, feel: "pop" });
  const jp = buildNewSong({ ...spec, feel: "jpop" });
  it("NEW_SONG_FEELS に入っていて、拍の合計は pop と同じ", () => {
    expect(NEW_SONG_FEELS).toContain("jpop");
    expect(jp.tracks).toHaveLength(pop.tracks.length);
    jp.tracks.forEach((t, i) => expect(total(t), t.instrument).toBeCloseTo(total(pop.tracks[i]), 6));
  });
  it("ギターは jpopClean の8分アルペジオ（E3〜E5）、ピアノは右（ギターと反対）、ほかは pop と同じ", () => {
    const g = jp.tracks.find((t) => t.instrument === "guitar")!;
    expect(g.amp?.type).toBe("jpopClean");
    expect(g.pan).toBeLessThan(0);
    expect(g.chorus).toBeGreaterThan(0);
    for (const m of midiOf(g)) { expect(m).toBeGreaterThanOrEqual(noteNameToMidi("E3")); expect(m).toBeLessThanOrEqual(noteNameToMidi("E5")); }
    expect(g.notes.filter((n) => n.durationBeats === 0.5)).toHaveLength(g.notes.length);
    expect(jp.tracks.find((t) => t.instrument === "piano")!.pan).toBeGreaterThan(0);
    for (const t of jp.tracks) if (t.instrument !== "guitar" && t.instrument !== "piano") expect(JSON.stringify(t), t.instrument).toBe(JSON.stringify(pop.tracks.find((x) => x.instrument === t.instrument && x.pan === t.pan)));
  });
  it("jpopFeelSong は pop の伴奏だけを受け取る（拍子が違っても長さがそろう）", () => {
    for (const beats of [3, 6, 7]) {
      const p = buildNewSong({ ...spec, beats, feel: "pop" });
      const j = buildNewSong({ ...spec, beats, feel: "jpop" });
      expect(total(j.tracks.find((t) => t.instrument === "guitar")!)).toBeCloseTo(total(p.tracks.find((t) => t.instrument === "guitar")!), 6);
    }
    expect(typeof jpopFeelSong).toBe("function");
  });
  it("曲に通すと、sections:auto と layers の既定（イントロ＝ギターと鍵盤、Aメロ＝ギターなし、Bメロ＝ギターが入る）、drumGenre jpop が入る", () => {
    const s = song({ feel: "jpop", autoAccompaniment: true, repeats: 8, parts: [] });
    const pre = applyJpopSong(s, []);
    expect(pre.sections).toBe("auto");
    expect(pre.drumGenre).toBe("jpop");
    expect(pre.layers?.verse).toEqual(["kick", "hat", "bass", "keys"]);
    const user = applyJpopSong({ ...s, layers: { verse: ["bass"] }, drumGenre: "rock", sections: "auto" }, []);
    expect(user.layers?.verse).toEqual(["bass"]);
    expect(user.drumGenre).toBe("rock");
  });
  it("自動伴奏のギターが、イントロで鳴り、Aメロで休み、Bメロで入る", () => {
    const s = song({ feel: "jpop", autoAccompaniment: true, repeats: 8, parts: [guitar({ role: "メロ", instrument: "lead" })] });
    const { score } = aiSongToScore(s);
    const g = score.tracks.find((t) => t.instrument === "guitar" && t.amp?.type === "jpopClean")!;
    const secs = autoSections(32);
    let at = 0;
    const range: Record<string, [number, number]> = {};
    for (const x of secs) { if (!range[x.kind]) range[x.kind] = [at * 4, (at + x.bars) * 4]; at += x.bars; }
    const soundsIn = (kind: string): boolean => {
      const [a, b] = range[kind];
      let pos = 0;
      for (const n of g.notes) { if (pos >= a - 1e-6 && pos < b - 1e-6 && n.note !== REST) return true; pos += n.durationBeats; }
      return false;
    };
    expect(soundsIn("intro")).toBe(true);
    expect(soundsIn("verse")).toBe(false);
    expect(soundsIn("pre")).toBe(true);
    expect(soundsIn("chorus")).toBe(true);
  });
});
