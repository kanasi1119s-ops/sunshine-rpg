import { describe, expect, it } from "vitest";
import { flattenScore, getScoreDurationSec, REST, type Score } from "./score";

function makeScore(): Score {
  return {
    tempoBpm: 120, // 1拍 = 0.5秒
    loop: false,
    tracks: [
      {
        waveform: "square",
        volume: 0.5,
        notes: [
          { note: "C4", durationBeats: 1 },
          { note: REST, durationBeats: 1 },
          { note: "E4", durationBeats: 2 },
        ],
      },
    ],
  };
}

describe("getScoreDurationSec", () => {
  it("拍数とテンポから長さ（秒）を計算する", () => {
    // 合計4拍 × 0.5秒 = 2秒
    expect(getScoreDurationSec(makeScore())).toBeCloseTo(2, 5);
  });

  it("パートが複数あるときは一番長いものに合わせる", () => {
    const score = makeScore();
    score.tracks.push({
      waveform: "triangle",
      volume: 0.3,
      notes: [{ note: "C3", durationBeats: 8 }],
    });
    expect(getScoreDurationSec(score)).toBeCloseTo(4, 5);
  });
});

describe("flattenScore", () => {
  it("休符を飛ばし、正しい開始時刻・長さ・周波数の一覧にする", () => {
    const events = flattenScore(makeScore());
    expect(events).toHaveLength(2);

    expect(events[0].startSec).toBeCloseTo(0, 5);
    expect(events[0].durationSec).toBeCloseTo(0.5, 5);
    expect(events[0].frequency).toBeCloseTo(261.63, 1); // C4

    // 休符(1拍=0.5秒)の後なので、開始は1.0秒。
    expect(events[1].startSec).toBeCloseTo(1.0, 5);
    expect(events[1].durationSec).toBeCloseTo(1.0, 5);
  });

  it("複数パートをまとめて返す", () => {
    const score = makeScore();
    score.tracks.push({
      waveform: "triangle",
      volume: 0.3,
      notes: [{ note: "C3", durationBeats: 1 }],
    });
    expect(flattenScore(score)).toHaveLength(3);
  });

  it("パートにアンプの指定があるときだけ、音の一覧にもアンプ名が入る", () => {
    const score = makeScore();
    score.tracks[0].amp = "rock";
    score.tracks.push({
      waveform: "triangle",
      volume: 0.3,
      notes: [{ note: "C3", durationBeats: 1 }],
    });
    const events = flattenScore(score);
    expect(events.filter((e) => e.amp === "rock")).toHaveLength(2);
    const plain = events.find((e) => e.waveform === "triangle")!;
    expect("amp" in plain).toBe(false);
  });
});
