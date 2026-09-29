import { describe, expect, it } from "vitest";
import { encodeWav } from "./wav";
import { encodeFlac } from "./flac";
import { muxOggOpus, oggCrc } from "./ogg-opus";
import { scoreToCsv, scoreToMusicXml } from "./musicxml";
import type { Score } from "./score";

const score: Score = { tempoBpm: 100, timeSig: { num: 3, den: 4 }, loop: true, tracks: [
  { waveform: "sine", instrument: "piano", volume: 0.2, notes: [{ note: "C4", durationBeats: 2 }, { note: "F#4", durationBeats: 2.5 }, { note: "R", durationBeats: 1.5 }] },
  { waveform: "square", instrument: "kick", volume: 0.3, notes: [{ note: "C2", durationBeats: 1 }, { note: "R", durationBeats: 5 }] },
] };

describe("いろいろな形式での書き出し", () => {
  it("WAV 24ビット・32ビット（小数）", () => {
    const ch = [new Float32Array([0.5, -1]), new Float32Array([0, 1])];
    const w24 = encodeWav(ch, 48000, 0, undefined, 24);
    expect(w24.length).toBe(44 + 2 * 6);
    expect(new DataView(w24.buffer).getUint16(34, true)).toBe(24);
    const w32 = encodeWav(ch, 48000, 0, undefined, 32);
    const v = new DataView(w32.buffer);
    expect(v.getUint16(20, true)).toBe(3);
    expect(v.getFloat32(44, true)).toBe(0.5);
  });
  it("FLAC の見出しと、無音の圧縮", () => {
    const f = encodeFlac([new Float32Array(10000), new Float32Array(10000)], 44100);
    expect(String.fromCharCode(...f.slice(0, 4))).toBe("fLaC");
    expect(f.length).toBeLessThan(400);
  });
  it("Ogg の入れ物（CRC とページ）", () => {
    expect(oggCrc(new TextEncoder().encode("123456789"))).toBe(0x89a1897f);
    const ogg = muxOggOpus([{ data: new Uint8Array(300), samples: 960 }, { data: new Uint8Array(10), samples: 960 }], { channels: 2, preSkip: 312, inputSampleRate: 48000, totalSamples: 1500, title: "テスト" });
    expect(String.fromCharCode(...ogg.slice(0, 4))).toBe("OggS");
    expect(new TextDecoder().decode(ogg.slice(28, 36))).toBe("OpusHead");
  });
  it("MusicXML: 拍子・小節線をまたぐタイ・付点", () => {
    const xml = scoreToMusicXml(score, "テスト");
    expect(xml).toContain("<beats>3</beats><beat-type>4</beat-type>");
    expect((xml.match(/<measure /g) ?? []).length).toBe(4);
    expect(xml).toContain('<tie type="start"/>');
    expect(xml).toContain("<alter>1</alter>");
    expect(xml).toContain("<clef><sign>percussion</sign></clef>");
  });
  it("CSV", () => {
    expect(scoreToCsv(score).split("\n")[2]).toBe("1,piano,2,2.5,F#4,66,1");
  });
});
