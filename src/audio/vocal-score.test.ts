import { describe, expect, it } from "vitest";
import { composeSong, type SongSpec, type VocalSection } from "./songwriter";
import { FRAMERATE, VALID_MORAS, buildVocalPlan, parseLyrics, parseMelody, splitMoras, vowelOf } from "./vocal-score";

const spec = (over: Partial<SongSpec> = {}): SongSpec => ({ id: "t", title: "t", scene: "", style: "jpop", tonic: "C", minor: false, bpm: 120, seed: 9, beats: 4, targetSec: 270, vocal: true, ...over });
const kana = (text: string): string[] => splitMoras(text).moras.map((m) => m.kana);

describe("歌詞を1音ずつに分ける", () => {
  it("拗音・のばす音・「っ」・「ん」を正しく分ける", () => {
    expect(kana("きょうは")).toEqual(["キョ", "ウ", "ハ"]);
    expect(kana("とーきょー")).toEqual(["ト", "オ", "キョ", "オ"]);
    expect(kana("ふぁいと")).toEqual(["ファ", "イ", "ト"]);
    expect(splitMoras("がっこう").moras).toEqual([{ kana: "ガ" }, { kana: "ッ", tail: true }, { kana: "コ" }, { kana: "ウ" }]);
    expect(kana("しんじゅ")).toEqual(["シ", "ン", "ジュ"]);
    expect(kana("ヴァイオリン")).toEqual(["ヴァ", "イ", "オ", "リ", "ン"]);
  });

  it("読めない文字（漢字・英字）は報告し、記号と空白は無視する", () => {
    const r = splitMoras("君のこえ、abc！ ね");
    expect(r.invalid).toEqual(["君", "a", "b", "c"]);
    expect(r.moras.map((m) => m.kana)).toEqual(["ノ", "コ", "エ", "ネ"]);
  });

  it("出てくる音は、すべて VOICEVOX が歌える音（一覧にある）", () => {
    const all = "あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをんきゃきゅきょしゃしゅしょちゃちゅちょにゃひゃみゃりゃぎゃじゃびゃぴゃふぁふぃふぇふぉてぃでぃうぃ";
    const r = splitMoras(all);
    expect(r.invalid).toEqual([]);
    for (const m of r.moras) expect(VALID_MORAS.has(m.kana), m.kana).toBe(true);
  });

  it("母音を取り出す", () => {
    expect(vowelOf("キョ")).toBe("オ");
    expect(vowelOf("カ")).toBe("ア");
    expect(vowelOf("ン")).toBeNull();
  });
});

describe("歌詞のまとまり", () => {
  it("見出し（[verse] [chorus 2] [サビ]）を読む", () => {
    const st = parseLyrics("[verse]\nあいう\nえお\n\n[chorus 2]\nかきく\n[サビ]\nさしす");
    expect(st.map((s) => [s.kind, s.nth, s.lines.length])).toEqual([["verse", undefined, 2], ["chorus", 2, 1], ["chorus", undefined, 1]]);
  });

  it("見出しがないときは、Aメロ→Bメロ→サビの順にあてる", () => {
    const st = parseLyrics("あ\n\nい\n\nう\n\nえ");
    expect(st.map((s) => s.kind)).toEqual(["verse", "bridge", "chorus", "verse"]);
  });
});

describe("メロディを歌にする", () => {
  it("メロディの文字列を、拍の位置つきの音にする", () => {
    expect(parseMelody("C4:1 R:0.5 E4:1.5")).toEqual([
      { startBeat: 0, durBeats: 1, midi: 60 },
      { startBeat: 1, durBeats: 0.5, midi: null },
      { startBeat: 1.5, durBeats: 1.5, midi: 64 },
    ]);
  });

  it("歌のメロディを足しても、楽器の曲は変わらない。同じ設計図なら同じメロディ", () => {
    const a = JSON.stringify(composeSong(spec({ vocal: false })));
    const out1: { vocal?: VocalSection[] } = {};
    const out2: { vocal?: VocalSection[] } = {};
    expect(JSON.stringify(composeSong(spec(), out1))).toBe(a);
    composeSong(spec(), out2);
    expect(out1.vocal?.length).toBeGreaterThan(5);
    expect(JSON.stringify(out1.vocal)).toBe(JSON.stringify(out2.vocal));
  });

  it("歌のメロディは、Aメロ・Bメロ・サビだけ。女声の歌いやすい高さ（D4〜G5あたり）に収まる", () => {
    for (const style of ["jpop", "rock", "metal", "dancerock", "phonk"] as const) {
      const out: { vocal?: VocalSection[] } = {};
      composeSong(spec({ style }), out);
      expect(out.vocal!.every((v) => ["verse", "bridge", "chorus"].includes(v.kind))).toBe(true);
      for (const v of out.vocal!) for (const n of parseMelody(v.melody)) if (n.midi !== null) {
        expect(n.midi, style).toBeGreaterThanOrEqual(60);
        expect(n.midi, style).toBeLessThanOrEqual(79);
      }
    }
  });

  const LYRICS = [
    "[verse]", "あさひがのぼる まちのそら", "ひとりであるく かいだんを", "まだねむそうな ひとびとの", "こえがとおくで ゆれている",
    "[bridge]", "いまならまにあう きっと", "てをのばしたら とどくはず", "ためらうよりも はやく", "かぜがせなかを おしてくれる",
    "[chorus]", "かがやけ ぼくらの あしたへ", "どこまでも ゆけるさ", "ひかりのほうへ はしれ", "ずっとずっと うたいつづけよう",
  ].join("\n");

  it("歌詞をのせた楽譜は、規則どおり（先頭と末尾は音・音は一覧にある・位置が増えていく・フレームは整数）", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const plan = buildVocalPlan(out.vocal!, LYRICS, 120);
    expect(plan.chunks.length).toBeGreaterThanOrEqual(5);
    let prevEnd = 0;
    for (const c of plan.chunks) {
      expect(c.notes[0].key).not.toBeNull();
      expect(c.notes[c.notes.length - 1].key).not.toBeNull();
      expect(c.startFrame).toBeGreaterThanOrEqual(prevEnd);
      prevEnd = c.startFrame + c.notes.reduce((s, n) => s + n.frame_length, 0);
      for (const n of c.notes) {
        expect(Number.isInteger(n.frame_length) && n.frame_length >= 1).toBe(true);
        if (n.key === null) expect(n.lyric).toBe("");
        else {
          expect(VALID_MORAS.has(n.lyric), n.lyric).toBe(true);
          expect(n.key).toBeGreaterThanOrEqual(55);
          expect(n.key).toBeLessThanOrEqual(84);
        }
      }
    }
    // サビの2回目以降は、同じ歌詞・同じ旋律のくり返し
    const chorus = plan.chunks.filter((c) => c.kind === "chorus");
    expect(chorus.length).toBeGreaterThanOrEqual(2);
    expect(JSON.stringify(chorus[0].notes)).toBe(JSON.stringify(chorus[1].notes));
  });

  it("区間の長さ（フレーム）が、拍からの計算とぴったり合う（ずれがたまらない）", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const plan = buildVocalPlan(out.vocal!, LYRICS, 120);
    const first = plan.chunks[0];
    const sec = out.vocal![0];
    const notes = parseMelody(sec.melody);
    const lastSung = [...notes].reverse().find((n) => n.midi !== null)!;
    const firstSung = notes.find((n) => n.midi !== null)!;
    const expectLen = Math.round(((sec.startBeat + lastSung.startBeat + lastSung.durBeats) * 60 * FRAMERATE) / 120) - Math.round(((sec.startBeat + firstSung.startBeat) * 60 * FRAMERATE) / 120);
    expect(first.notes.reduce((s, n) => s + n.frame_length, 0)).toBe(expectLen);
  });

  it("歌詞が長すぎるときは、音を割って収める。それでも足りなければ警告する", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const longText = "[verse]\n" + "あいうえおかきくけこ".repeat(20);
    const plan = buildVocalPlan(out.vocal!, longText, 120);
    expect(plan.warnings.some((w) => w.includes("足りず"))).toBe(true);
  });

  it("Aメロ・Bメロの歌詞が足りない回は楽器だけで進む（くり返さない）。サビは全部歌う", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const plan = buildVocalPlan(out.vocal!, LYRICS, 120);
    const count = (k: string): number => out.vocal!.filter((v) => v.kind === k).length;
    expect(plan.chunks.filter((c) => c.kind === "verse").length).toBe(1);
    expect(plan.chunks.filter((c) => c.kind === "bridge").length).toBe(1);
    expect(plan.chunks.filter((c) => c.kind === "chorus").length).toBe(count("chorus"));
    expect(count("verse")).toBeGreaterThan(1);
  });

  it("歌詞の行の終わりに息つぎ（休符）が入り、行の途中には入らない", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const c = buildVocalPlan(out.vocal!, LYRICS, 120).chunks.find((x) => x.kind === "chorus")!;
    const rests = c.notes.filter((n) => n.key === null).length;
    expect(rests).toBe(3); // 4行 → 行のあいだに3回
  });

  it("歌詞が短いときは、母音をのばして音を埋める（歌詞が余らない）", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const plan = buildVocalPlan(out.vocal!, "[verse]\nあ\nい\nう\nえ", 120);
    const c = plan.chunks.find((x) => x.kind === "verse")!;
    const lyrics = c.notes.filter((n) => n.key !== null).map((n) => n.lyric);
    expect(lyrics.length).toBeGreaterThan(4);
    expect(new Set(lyrics)).toEqual(new Set(["ア", "イ", "ウ", "エ"]));
  });

  it("「っ」は直前の音の末尾に短く入る。漢字は警告して歌わない。歌詞のない区間は楽器だけ", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const plan = buildVocalPlan(out.vocal!, "[chorus]\nがっこうへ\nまっすぐ\n君へ\nはしる", 120);
    expect(plan.chunks.every((c) => c.kind === "chorus")).toBe(true);
    expect(plan.chunks.some((c) => c.notes.some((n) => n.lyric === "ッ"))).toBe(true);
    expect(plan.warnings.some((w) => w.includes("君"))).toBe(true);
  });

  it("移調できる（男声などに合わせる）", () => {
    const out: { vocal?: VocalSection[] } = {};
    composeSong(spec(), out);
    const a = buildVocalPlan(out.vocal!, LYRICS, 120, 0).chunks[0].notes.find((n) => n.key !== null)!.key!;
    const b = buildVocalPlan(out.vocal!, LYRICS, 120, -12).chunks[0].notes.find((n) => n.key !== null)!.key!;
    expect(b).toBe(a - 12);
  });

  it("3拍子・7拍子・各テンポでも成り立つ", () => {
    for (const [beats, bpm] of [[3, 100], [4, 90], [4, 170], [7, 150]] as const) {
      const out: { vocal?: VocalSection[] } = {};
      composeSong(spec({ beats, bpm, style: beats === 7 ? "progmetal" : beats === 3 ? "classic" : "jpop" }), out);
      const plan = buildVocalPlan(out.vocal!, LYRICS, bpm);
      expect(plan.chunks.length, `${beats}拍 ${bpm}`).toBeGreaterThan(4);
    }
  });
});
