import { describe, expect, it } from "vitest";
import { aiSongToScore, type AiSong } from "./ai-song";
import { allEntries, getTrackEdition } from "./catalog";
import { ampDistorts, scoreToMidiInfo } from "./midi-export";
import { realEdition } from "./real-edition";
import { ps2Edition } from "./ps2-edition";
import type { Score } from "./score";
import "./user-songs";

/**
 * 歪みは必ず1回だけ（二重がけ禁止。人間の指示 2026-10-02）。
 * 録音音源のギターのうち、GM 29（オーバードライブ）・30（ディストーション）はすでに歪んでいる。その上にアンプで歪ませると二重になる。
 * どの曲・どの版でも、「すでに歪んだ音色」のチャンネルに「歪ませるアンプ」が付かないことを確かめる。
 */
function assertSingleDistortion(score: Score, label: string): number {
  const info = scoreToMidiInfo(score);
  let guitars = 0;
  for (const [ch, program] of Object.entries(info.programs)) {
    const amp = info.amps[Number(ch)]?.amp;
    if (program === 29 || program === 30) {
      // 録音の歪みを使うなら、歪ませないアンプを明示していること
      expect(ampDistorts(amp, program), `${label} ch${ch}: 録音の歪み（GM${program}）にアンプの歪みが重なる`).toBe(false);
    } else if (amp && ampDistorts(amp, program)) {
      guitars++;
    }
  }
  return guitars;
}

describe("歪みの二重がけ禁止", () => {
  it("ゲームの全曲×3つの版で、録音の歪みとアンプの歪みが重ならない", () => {
    let checked = 0;
    for (const e of allEntries()) {
      for (const ed of ["modern", "ps2", "real"] as const) {
        assertSingleDistortion(getTrackEdition(e.id, ed), `${e.id}（${ed}）`);
        checked++;
      }
    }
    expect(checked).toBeGreaterThan(100);
  });

  it("assets-src/ai-songs の全曲（実楽器版・PS2版を含む）でも重ならない", () => {
    const files = import.meta.glob("../../assets-src/ai-songs/*.json", { eager: true, import: "default" }) as Record<string, AiSong>;
    for (const [f, song] of Object.entries(files)) {
      const { score } = aiSongToScore(song);
      for (const [name, s] of [["そのまま", score], ["実楽器版", realEdition(score)], ["PS2版", ps2Edition(score)]] as const) {
        assertSingleDistortion(s, `${f}（${name}）`);
      }
    }
  });

  it("amp が省略（auto）の歪みギターは、クリーンの音色（27）に、歪みの種類を明示したアンプを付ける", () => {
    const score: Score = {
      tempoBpm: 120, loop: false, tone: "metal",
      tracks: [
        { waveform: "sawtooth", instrument: "distGuitar", volume: 0.1, pan: -0.9, notes: [{ note: "E3", durationBeats: 1 }] },
        { waveform: "sawtooth", instrument: "crunch", volume: 0.1, pan: 0.9, notes: [{ note: "E3", durationBeats: 1 }] },
      ],
    };
    const info = scoreToMidiInfo(score);
    expect(Object.values(info.programs)).toEqual([27, 27]); // どちらも歪んでいない音色
    expect(Object.values(info.amps).map((a) => a.amp.type).sort()).toEqual(["metal", "overdrive"]); // 歪みはアンプだけ
  });

  it("歪ませないアンプ（clean など）を明示したときだけ、録音の歪みをそのまま使う", () => {
    const score: Score = {
      tempoBpm: 120, loop: false,
      tracks: [{ waveform: "sawtooth", instrument: "distGuitar", volume: 0.1, pan: 0, amp: { type: "clean" }, notes: [{ note: "E3", durationBeats: 1 }] }],
    };
    expect(Object.values(scoreToMidiInfo(score).programs)).toEqual([30]);
  });

  it("ampDistorts: auto は 29・30 のとき歪ませる扱い。明示した種類は種類で決まる", () => {
    expect(ampDistorts(undefined, 30)).toBe(true);
    expect(ampDistorts({ type: "auto" }, 29)).toBe(true);
    expect(ampDistorts({ type: "auto" }, 27)).toBe(false);
    expect(ampDistorts({ type: "jazz" }, 30)).toBe(false);
    expect(ampDistorts({ type: "loudrock" }, 27)).toBe(true);
    expect(ampDistorts({ type: "genre", preset: "clean" }, 27)).toBe(false);
  });
});
