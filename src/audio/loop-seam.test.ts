import { describe, expect, it } from "vitest";
import { allEntries, getTrack } from "./catalog";
import { checkScoreSeam } from "./loop-check";
import "./user-songs";

describe("ゲームの全曲のループ継ぎ目の検査（情報）", () => {
  it("全曲に対して検査が最後まで動く", () => {
    const rows: string[] = [];
    let looping = 0, flagged = 0;
    for (const e of allEntries()) {
      const score = getTrack(e.id);
      if (!score.loop) continue;
      looping++;
      const w = checkScoreSeam(score);
      if (w.length) { flagged++; rows.push(`${e.id}: ${w.length}件 — ${w[0]}`); }
    }
    console.log(`ループ曲 ${looping} 曲のうち、継ぎ目に注意がある曲 ${flagged} 曲\n${rows.join("\n")}`);
    expect(looping).toBeGreaterThan(10);
  }, 120000);
});
