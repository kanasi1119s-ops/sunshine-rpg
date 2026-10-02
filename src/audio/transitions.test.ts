import { describe, expect, it } from "vitest";
import { REST, type NoteEvent, type Score } from "./score";
import { composeSong, planKinds, type SongSpec, type Style } from "./songwriter";
import { applyTransitions, overlay } from "./transitions";

const beatsOf = (n: NoteEvent[]): number => n.reduce((s, e) => s + e.durationBeats, 0);
const at = (notes: NoteEvent[], beat: number): NoteEvent | undefined => {
  let pos = 0;
  for (const e of notes) {
    if (beat >= pos - 1e-9 && beat < pos + e.durationBeats - 1e-9) return e;
    pos += e.durationBeats;
  }
  return undefined;
};

describe("overlay（時間の一部を差し替える）", () => {
  const n = (note: string, d: number): NoteEvent => ({ note, durationBeats: d });
  it("長さを変えずに、まん中を差し替える。またぐ音は前後に切る", () => {
    const out = overlay([n("C4", 4), n("D4", 4)], 3, 2, [n(REST, 2)]);
    expect(beatsOf(out)).toBe(8);
    expect(out.map((e) => `${e.note}:${e.durationBeats}`)).toEqual(["C4:3", "R:2", "D4:3"]);
  });
  it("先頭・末尾・ちょうど音の境目でも長さが保たれる", () => {
    for (const [s, l] of [[0, 1], [7, 1], [4, 2], [0.5, 0.25], [3.75, 0.5]] as const) {
      const out = overlay([n("C4", 4), n("D4", 2), n("E4", 2)], s, l, [n(REST, l)]);
      expect(beatsOf(out), `${s}+${l}`).toBeCloseTo(8, 9);
    }
  });
});

const spec = (style: Style, over: Partial<SongSpec> = {}): SongSpec => ({ id: "t", title: "t", scene: "", style, tonic: "E", minor: true, bpm: 132, seed: 3, beats: 4, targetSec: 270, ...over });

describe("つなぎ目の演出", () => {
  it("サビ・間奏の頭にクラッシュが鳴る。全パートの長さはそろったまま", () => {
    for (const style of ["rock", "metal", "jpop", "dancerock", "hardcore"] as const) {
      const score = composeSong(spec(style));
      const kinds = planKinds(132, 4, 270);
      const crash = score.tracks.find((t) => t.instrument === "crash")!;
      let pos = 0;
      kinds.forEach((k) => {
        if (k === "chorus" || k === "solo") {
          const e = at(crash.notes, pos);
          expect(e?.note, `${style} ${k} @${pos}`).toBe("C4");
        }
        pos += (k === "intro" ? 4 : 8) * 4;
      });
      expect(new Set(score.tracks.map((t) => Math.round(beatsOf(t.notes) * 1000))).size, style).toBe(1);
    }
  });

  it("Bメロからサビに入る直前の1拍は、ドラム以外が止まる（ドラムは止まらない）", () => {
    const score = composeSong(spec("rock"));
    const kinds = planKinds(132, 4, 270);
    let pos = 0;
    let found = 0;
    kinds.forEach((k, i) => {
      if (k === "chorus" && kinds[i - 1] === "bridge") {
        found++;
        const bass = score.tracks.find((t) => t.instrument === "bass")!;
        expect(at(bass.notes, pos - 0.5)?.note).toBe(REST);
        const kick = score.tracks.find((t) => t.instrument === "kick")!;
        expect(at(kick.notes, pos - 4)).toBeTruthy();
      }
      pos += (k === "intro" ? 4 : 8) * 4;
    });
    expect(found).toBeGreaterThan(0);
  });

  it("ドラムのない曲調（クラシック・自然音など）は何も足さない。短い曲（ゲームのBGM）も変わらない", () => {
    const classic = composeSong(spec("classic", { tonic: "D", minor: false }));
    expect(classic.tracks.some((t) => t.instrument === "crash")).toBe(false);
    const short = composeSong(spec("rock", { targetSec: 75 }));
    // 短い曲では、つなぎ目の演出（ストップタイム）はかからない: Bメロ→サビの直前の拍でも、ベースは鳴ったまま
    const kinds = planKinds(132, 4, 75);
    let pos = 0;
    kinds.forEach((k, i) => {
      if (k === "chorus" && kinds[i - 1] === "bridge") {
        const bass = short.tracks.find((t) => t.instrument === "bass")!;
        expect(at(bass.notes, pos - 0.5)?.note).not.toBe(REST);
      }
      pos += (k === "intro" ? 4 : 8) * 4;
    });
    expect(JSON.stringify(composeSong(spec("rock", { targetSec: 75 })))).toBe(JSON.stringify(short));
  });

  it("applyTransitions は、ドラムがなければ何もしない", () => {
    const score: Score = { tempoBpm: 120, loop: true, tracks: [{ waveform: "sine", instrument: "piano", volume: 0.2, notes: [{ note: "C4", durationBeats: 40 }] }] };
    expect(applyTransitions(score, ["intro", "verse", "bridge", "chorus", "outro"], 4)).toEqual({ crashes: [], stops: [] });
    expect(score.tracks.length).toBe(1);
  });
});
