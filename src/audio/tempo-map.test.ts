import { describe, expect, it } from "vitest";
import { aiSongToScore } from "./ai-song";
import { scoreToMidi } from "./midi-export";
import { flattenScore, getScoreDurationSec, type Score } from "./score";
import { expandTempoMap, loopTempoWarning, makeTempoClock, ritPoints, ritSpeed, rubatoFactor, rubatoPoints, tempoDurationSec } from "./tempo-map";
import { newFeatureSong, readMidi, ROCK_SONG } from "./rhythm-fixtures";

describe("テンポマップ（提案5）", () => {
  it("マップが無い／空のときは、今までと同じ計算（拍×60÷bpm）", () => {
    for (const map of [undefined, []]) {
      const c = makeTempoClock(97, map);
      expect(c.constant).toBe(true);
      expect(c.beatToSec(13.25)).toBe((13.25 * 60) / 97);
      expect(c.secToBeat(5)).toBe((5 * 97) / 60);
    }
  });
  it("階段のテンポ: 拍→秒が区間ごとに足し合わさり、秒→拍で元に戻る", () => {
    const c = makeTempoClock(120, [{ beat: 8, bpm: 60 }, { beat: 12, bpm: 240 }]);
    expect(c.beatToSec(8)).toBeCloseTo(4, 9); // 120bpm で 8拍＝4秒
    expect(c.beatToSec(12)).toBeCloseTo(4 + 4, 9); // 60bpm で 4拍＝4秒
    expect(c.beatToSec(16)).toBeCloseTo(8 + 1, 9); // 240bpm で 4拍＝1秒
    for (const beat of [0, 3.3, 8, 9.5, 12, 15.75, 20]) expect(c.secToBeat(c.beatToSec(beat))).toBeCloseTo(beat, 9);
    expect(c.bpmAt(7.99)).toBe(120);
    expect(c.bpmAt(8)).toBe(60);
    expect(c.bpmAt(100)).toBe(240);
  });
  it("ramp: 1/8拍ごとの階段で直線的に近づき、終わりでぴったり目標になる", () => {
    const segs = expandTempoMap(100, [{ beat: 4, bpm: 140, ramp: 4 }]);
    expect(segs[0]).toEqual({ beat: 0, bpm: 100 });
    const ramp = segs.filter((s) => s.beat >= 4 && s.beat < 8);
    expect(ramp.length).toBe(32);
    expect(ramp[0].bpm).toBeGreaterThan(100);
    expect(ramp[0].bpm).toBeLessThan(101);
    expect(ramp[31].bpm).toBeGreaterThan(139);
    for (let i = 1; i < ramp.length; i++) expect(ramp[i].bpm).toBeGreaterThan(ramp[i - 1].bpm);
    expect(segs[segs.length - 1]).toEqual({ beat: 8, bpm: 140 });
    // 直線なので、区間の平均テンポ（120）で 4拍＝2秒に近い
    const c = makeTempoClock(100, [{ beat: 4, bpm: 140, ramp: 4 }]);
    expect(c.beatToSec(8) - c.beatToSec(4)).toBeCloseTo((4 * 60) / 120, 1);
  });
  it("同じ位置の点は後のものが勝ち、同じ bpm の点は足さない", () => {
    expect(expandTempoMap(120, [{ beat: 0, bpm: 90 }])).toEqual([{ beat: 0, bpm: 90 }]);
    expect(expandTempoMap(120, [{ beat: 4, bpm: 120 }])).toEqual([{ beat: 0, bpm: 120 }]);
  });
  it("終わりの減速の曲線 v(x)=(1+(w^q−1)x)^(1/q): 始まりは1、終わりは w、単調", () => {
    expect(ritSpeed(0, 0.6)).toBeCloseTo(1, 12);
    expect(ritSpeed(1, 0.6)).toBeCloseTo(0.6, 12);
    let prev = 1;
    for (let i = 1; i <= 10; i++) { const v = ritSpeed(i / 10, 0.6); expect(v).toBeLessThan(prev); prev = v; }
    // q=2 の式は 1→w の「速さの2乗」が直線で落ちる形（最初は緩く、終わりに急）
    expect(ritSpeed(0.5, 0.6)).toBeCloseTo(Math.sqrt(1 + (0.36 - 1) * 0.5), 12);
  });
  it("ritPoints: 半拍ごとの階段、最後は to 倍。aTempo なら元に戻る", () => {
    const pts = ritPoints({ beat: 28, beats: 4, to: 0.7 }, 120);
    expect(pts.length).toBe(9);
    expect(pts[0].beat).toBe(28);
    expect(pts[0].bpm).toBeLessThan(120);
    expect(pts[8]).toEqual({ beat: 32, bpm: 84 });
    expect(ritPoints({ beat: 28, beats: 4, to: 0.7, aTempo: true }, 120)[8].bpm).toBe(120);
  });
  it("ルバート: 倍率は ±3%＋フレーズ終わりの伸び（最大 5%）の範囲、曲の頭は 1、ループで連続", () => {
    const spec = { amount: 1, totalBeats: 64, beatsPerBar: 4 };
    expect(rubatoFactor(0, spec)).toBe(1);
    let lo = 9, hi = 0;
    for (let b = 0; b < 64; b += 0.25) { const f = rubatoFactor(b, spec); lo = Math.min(lo, f); hi = Math.max(hi, f); }
    expect(hi).toBeLessThanOrEqual(1.0301);
    expect(lo).toBeGreaterThan(0.92);
    expect(lo).toBeLessThan(0.97);
    // 周期は曲をちょうど整数回まわる: 末尾の直前と先頭の波の位相が連続（sin の値が0に向かう）
    const wave = (b: number): number => Math.sin((2 * Math.PI * Math.max(1, Math.round(64 / 12)) * b) / 64);
    expect(wave(64)).toBeCloseTo(wave(0), 9);
    // フレーズの最後の拍は遅くなる
    expect(rubatoFactor(15.5, spec)).toBeLessThan(rubatoFactor(11.5, spec) + 0.05);
    expect(rubatoFactor(0, { ...spec, amount: 0 })).toBe(1);
  });
  it("rubatoPoints: 1拍ごとの点、amount 0 なら元のまま。明示のテンポの上に乗る", () => {
    expect(rubatoPoints(120, undefined, { amount: 0, totalBeats: 32, beatsPerBar: 4 })).toEqual([]);
    const pts = rubatoPoints(120, [{ beat: 16, bpm: 90 }], { amount: 0.5, totalBeats: 32, beatsPerBar: 4 });
    expect(pts.length).toBe(32);
    expect(Math.abs(pts[0].bpm - 120)).toBeLessThan(2);
    expect(pts[20].bpm).toBeLessThan(100);
    expect(pts[20].bpm).toBeGreaterThan(85);
  });
  it("ループの継ぎ目の警告: 最後のテンポが最初と違うときだけ", () => {
    expect(loopTempoWarning(120, undefined, 64)).toBeNull();
    expect(loopTempoWarning(120, [{ beat: 32, bpm: 90 }], 64)).toContain("継ぎ目");
    expect(loopTempoWarning(120, [{ beat: 32, bpm: 90 }, { beat: 60, bpm: 120 }], 64)).toBeNull();
  });
  it("曲の長さ（秒）と再生用の時刻が、マップに沿う", () => {
    const sc: Score = { tempoBpm: 120, loop: false, tempoMap: [{ beat: 4, bpm: 60 }], tracks: [{ waveform: "square", volume: 0.2, notes: [{ note: "C4", durationBeats: 4 }, { note: "D4", durationBeats: 4 }] }] };
    expect(getScoreDurationSec(sc)).toBeCloseTo(2 + 4, 9);
    const f = flattenScore(sc);
    expect(f[0].startSec).toBe(0);
    expect(f[1].startSec).toBeCloseTo(2, 9);
    expect(f[0].durationSec).toBeCloseTo(2, 9);
    expect(f[1].durationSec).toBeCloseTo(4, 9);
    expect(f[1].beatSec).toBeCloseTo(1, 9);
    expect(tempoDurationSec(120, sc.tempoMap, 8)).toBeCloseTo(6, 9);
    // マップが無い曲は今までどおり
    expect(getScoreDurationSec({ ...sc, tempoMap: undefined })).toBe(4);
  });
  it("MIDI: テンポのイベントが拍の位置（ティック）に書かれ、音の位置は拍のまま", () => {
    const sc: Score = { tempoBpm: 120, loop: true, tempoMap: [{ beat: 4, bpm: 60 }, { beat: 6, bpm: 240 }], tracks: [{ waveform: "square", instrument: "bass", volume: 0.2, notes: [{ note: "C2", durationBeats: 4 }, { note: "D2", durationBeats: 2 }, { note: "E2", durationBeats: 2 }] }] };
    const m = readMidi(scoreToMidi(sc));
    expect(m.tempos).toEqual([{ tick: 0, usec: 500000 }, { tick: 4 * 480, usec: 1000000 }, { tick: 6 * 480, usec: 250000 }]);
    // 音の位置は拍のまま（ごく小さな人のずれ・重ねた音をのぞく）
    const starts = [...new Set(m.notes.map((n) => Math.round(n.tick / 100)))];
    expect(starts).toEqual([0, 19, 29]);
  });
  it("テンポマップが無い曲のMIDIは、テンポが先頭に1つだけ", () => {
    const { score } = aiSongToScore(ROCK_SONG);
    expect(readMidi(scoreToMidi(score)).tempos).toEqual([{ tick: 0, usec: 500000 }]);
  });
});

describe("AIソングの tempo・rit・rubato（提案5・7）", () => {
  it("tempo: bar（1始まり）から、ramp は小節数", () => {
    const { score } = aiSongToScore(newFeatureSong({ tempo: [{ bar: 5, bpm: 96, ramp: 2 }] }));
    expect(score.tempoBpm).toBe(120);
    const segs = expandTempoMap(120, score.tempoMap);
    expect(segs.find((s) => s.beat >= 16)!.beat).toBe(16);
    expect(segs[segs.length - 1]).toEqual({ beat: 24, bpm: 96 });
  });
  it("rit: 最後の2小節で 0.7 倍へ。ループ曲なので継ぎ目の警告が出る。aTempo なら出ない", () => {
    const a = aiSongToScore(newFeatureSong({ rit: { bar: 7, bars: 2, to: 0.7 } }));
    expect(a.score.tempoMap![a.score.tempoMap!.length - 1]).toEqual({ beat: 32, bpm: 84 });
    expect(makeTempoClock(120, a.score.tempoMap).bpmAt(31.9)).toBeLessThan(86);
    expect(a.warnings.some((w) => w.includes("継ぎ目"))).toBe(true);
    const b = aiSongToScore(newFeatureSong({ rit: { bar: 3, bars: 2, to: 0.7, aTempo: true } }));
    expect(b.warnings.some((w) => w.includes("継ぎ目"))).toBe(false);
    // rit のぶんだけ曲が長くなる
    expect(getScoreDurationSec(a.score)).toBeGreaterThan(16);
  });
  it("rubato: ループで元に戻る（曲の頭が基準のテンポ）、曲全体の長さはほぼ同じ", () => {
    const { score } = aiSongToScore(newFeatureSong({ rubato: 0.8 }));
    expect(score.tempoMap!.length).toBeGreaterThan(20);
    expect(Math.abs(score.tempoMap![0].bpm - 120)).toBeLessThan(2);
    expect(Math.abs(getScoreDurationSec(score) - 16) / 16).toBeLessThan(0.03);
  });
  it("不正な tempo／rit は警告して無視する", () => {
    const { score, warnings } = aiSongToScore(newFeatureSong({ tempo: [{ bar: 99, bpm: 90 }], rit: { bar: 1 } }));
    expect(score.tempoMap).toBeUndefined();
    expect(warnings.filter((w) => w.includes("tempo[0]") || w.includes("rit")).length).toBe(2);
  });
});
