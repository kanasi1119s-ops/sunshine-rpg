import { describe, expect, it } from "vitest";
import { bandPass, formatPhoneReport, phoneCheck, readWavPcm16 } from "./phone-check";

const fs = 44100;
const sine = (f: number, sec = 1, amp = 0.5, phase = 0): Float32Array => Float32Array.from({ length: Math.round(fs * sec) }, (_, i) => amp * Math.sin(2 * Math.PI * f * (i / fs) + phase));
const rms = (x: Float32Array): number => Math.sqrt(x.reduce((s, v) => s + v * v, 0) / x.length);
const mix = (...xs: Float32Array[]): Float32Array => Float32Array.from({ length: xs[0].length }, (_, i) => xs.reduce((s, x) => s + x[i], 0));

describe("bandPass", () => {
  it("通す帯域の音は残り、遠い音は大きく減る", () => {
    const keep = rms(bandPass(sine(1000), 800, Infinity, fs));
    const cut = rms(bandPass(sine(100), 800, Infinity, fs));
    expect(keep).toBeGreaterThan(0.2);
    expect(cut).toBeLessThan(0.005);
    expect(rms(bandPass(sine(60), 40, 150, fs))).toBeGreaterThan(0.2);
    expect(rms(bandPass(sine(3000), 40, 150, fs))).toBeLessThan(0.002);
  });
});

describe("phoneCheck", () => {
  it("低い音だけの曲は『800Hz以上が小さい』『倍音が少ない』", () => {
    const bass = sine(80);
    const r = phoneCheck([bass, bass], fs);
    expect(r.highShareDb).toBeLessThan(-30);
    expect(r.warnings.some((w) => w.includes("800Hz"))).toBe(true);
    expect(r.warnings.some((w) => w.includes("ベースの倍音"))).toBe(true);
  });

  it("ベースに倍音があれば倍音の警告は出ない", () => {
    const bass = mix(sine(80, 1, 0.3), sine(400, 1, 0.2), sine(2000, 1, 0.1));
    const r = phoneCheck([bass, bass], fs);
    expect(r.bassHarmonicsDb).toBeGreaterThan(-6);
    expect(r.warnings.some((w) => w.includes("ベースの倍音"))).toBe(false);
    expect(r.warnings.some((w) => w.includes("800Hz"))).toBe(false);
  });

  it("逆相の旋律はモノにたたむと消える", () => {
    const m = sine(1000);
    const inv = Float32Array.from(m, (v) => -v);
    const r = phoneCheck([m, inv], fs);
    expect(r.monoLossDb).toBeGreaterThan(20);
    expect(r.monoMelodyLossDb).toBeGreaterThan(20);
    expect(r.warnings.some((w) => w.includes("モノラル"))).toBe(true);
  });

  it("中央の旋律はモノにしても損失がない", () => {
    const m = mix(sine(1000), sine(120, 1, 0.2), sine(500, 1, 0.1));
    const r = phoneCheck([m, m], fs);
    expect(r.monoLossDb).toBeLessThan(0.1);
    expect(r.monoMelodyLossDb).toBeLessThan(0.1);
    expect(r.warnings).toEqual([]);
  });

  it("モノのWAV（1ch）も測れる／無音は測れないと言う", () => {
    expect(phoneCheck([mix(sine(1000), sine(100, 1, 0.1))], fs).warnings).toEqual([]);
    expect(phoneCheck([new Float32Array(1000)], fs).warnings.join()).toContain("無音");
  });

  it("表示に○と要確認が出る", () => {
    const bass = sine(80);
    const text = formatPhoneReport(phoneCheck([bass, bass], fs), "x.wav");
    expect(text).toContain("x.wav");
    expect(text).toContain("要確認");
    expect(text).toContain("○");
  });
});

describe("readWavPcm16", () => {
  const wav = (ch: number, frames: number): Uint8Array => {
    const out = new Uint8Array(44 + frames * ch * 2);
    const dv = new DataView(out.buffer);
    const w = (o: number, s: string): void => { for (let i = 0; i < s.length; i++) out[o + i] = s.charCodeAt(i); };
    w(0, "RIFF"); dv.setUint32(4, 36 + frames * ch * 2, true); w(8, "WAVE"); w(12, "fmt "); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, ch, true);
    dv.setUint32(24, 48000, true); dv.setUint32(28, 48000 * ch * 2, true); dv.setUint16(32, ch * 2, true); dv.setUint16(34, 16, true); w(36, "data"); dv.setUint32(40, frames * ch * 2, true);
    for (let i = 0; i < frames; i++) for (let c = 0; c < ch; c++) dv.setInt16(44 + (i * ch + c) * 2, c === 0 ? 16384 : -16384, true);
    return out;
  };
  it("ステレオ16bitを読める", () => {
    const r = readWavPcm16(wav(2, 100));
    expect(r.sampleRate).toBe(48000);
    expect(r.channels).toHaveLength(2);
    expect(r.channels[0][0]).toBeCloseTo(0.5);
    expect(r.channels[1][0]).toBeCloseTo(-0.5);
  });
  it("WAVでなければエラー", () => {
    expect(() => readWavPcm16(new Uint8Array(50))).toThrow(/WAV/);
  });
});
