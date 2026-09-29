import { describe, expect, it } from "vitest";
import { encodeWav } from "./wav";

describe("WAV書き出し", () => {
  it("ヘッダーと長さが正しい（ステレオ・16ビット）", () => {
    const wav = encodeWav([new Float32Array([0, 0.5, -0.5, 2]), new Float32Array([0, 0, 0, -2])], 44100);
    const v = new DataView(wav.buffer);
    expect(String.fromCharCode(...wav.slice(0, 4))).toBe("RIFF");
    expect(String.fromCharCode(...wav.slice(8, 12))).toBe("WAVE");
    expect(v.getUint32(24, true)).toBe(44100);
    expect(v.getUint32(40, true)).toBe(16);
    expect(wav.length).toBe(44 + 16);
    expect(v.getInt16(44 + 4, true)).toBe(16384);
    expect(v.getInt16(44 + 12, true)).toBe(32767);
    expect(v.getInt16(46 + 12, true)).toBe(-32767);
  });
});
