import { describe, expect, it } from "vitest";
import { applyAction, createBattleState } from "./battle-engine";
import { battleAnimFor } from "./battle-anim";
import { JOBS_BY_ID } from "../job/jobs";
import type { Combatant, Skill } from "./types";

/**
 * 戦闘で使うジョブの特技は、すべて動き（モーション・エフェクト）がつく（2026-10-06、人間の指示
 * 「特技はバトル画面で使うものはすべてモーションをつけてね」）。
 * 全特技を、いろいろな乱数で使ってみて、出てくる文のすべてに動きがつくことを確かめる（「〜を倒した！」は除く）。
 */
const mk = (id: string, name: string, enemy: boolean, p: Partial<Combatant> = {}): Combatant => ({
  id, name, maxHp: 400, hp: 400, maxMp: 999, mp: 999, attack: 60, defense: 20, speed: 30, isEnemy: enemy, guarding: false, ...p,
});

describe("ジョブの特技の動き", () => {
  it("どの特技も、戦闘の文に動きがつく", () => {
    const missing = new Set<string>();
    for (const job of Object.values(JOBS_BY_ID)) {
      for (const js of job.skills) {
        if (!js.battle) continue;
        const skill: Skill = { id: `job:${js.name}`, name: js.name, ...js.battle };
        const allyTarget = ["heal", "healAll", "buff", "buffAll"].includes(skill.effect ?? "");
        for (const seed of [0.01, 0.3, 0.6, 0.99]) {
          const party = [mk("hero", "ユーリ", false, { hp: 150 }), mk("reto", "レト", false, { hp: 120 })];
          const enemies = [mk("e1", "的の岩", true), mk("e2", "的の木", true, { hp: 30 })];
          const s0 = createBattleState(party, enemies);
          const s1 = applyAction(s0, { type: "skill", actorId: "hero", targetId: allyTarget ? "reto" : "e1", skill }, () => seed);
          for (const line of s1.log.slice(s0.log.length)) {
            if (/を倒した！$/.test(line)) continue;
            if (!battleAnimFor(line, s1, () => "sword")) missing.add(`${job.name}「${js.name}」: ${line}`);
          }
        }
      }
    }
    expect([...missing]).toEqual([]);
  });
});
