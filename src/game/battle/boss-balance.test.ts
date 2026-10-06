import { describe, expect, it } from "vitest";
import { partyAtLevel, winRate } from "./balance-helpers";
import type { Combatant } from "./types";
import { strengthenBoss } from "./difficulty-scale";
import { createMugikanoYugami } from "./chapter1-enemies";
import { createGarasukoYugami } from "./chapter2-enemies";
import { createTetsukusariYugami } from "./chapter3-enemies";
import { createSanoneSunaarashiYugami } from "./chapter4-enemies";
import { createKiriYogenYugami } from "./chapter5-enemies";
import { createShimoharaShisakukiYugami } from "./chapter6-enemies";
import { createFushimaKanshitakuYugami } from "./chapter7-enemies";
import { createToushinBanninYugami } from "./chapter8-enemies";
import { createKyotoukyuEdreaFirst, createKyotoukyuEdreaYugami, createKyotoukyuGuardian } from "./chapter9-enemies";
import { createDeepEchoYugami, createShogenYugami } from "./chapter10-enemies";
import { createGodYugami, GODS } from "./chapter11-enemies";
import { createDungeonEnemy, DUNGEON_ENEMIES } from "./chapter12-enemies";

/**
 * 全ボスのバランス（roadmap 7-2）。各ボスは、「その章に着く頃の想定レベル」の仲間つきパーティ
 * （ユーリ＋加入済みの仲間、剣装備、レベル相応の能力値）が、手堅い戦い方で戦った勝率が目安に入るよう調整している。
 * 想定レベルは、ランダムエンカウントで1レベル上がるのに約5戦かかる前提（`docs/design/battle.md`）で、章ごとに約2レベルずつ上がる想定。
 * 序章のボスだけは、Lv1のユーリ1人で調整している（`chapter0-balance.test.ts`）。
 */
interface BossCase {
  name: string;
  level: number;
  companions: number;
  make: () => Combatant;
  /** 目安の勝率（±0.1の範囲に入っていればよい）。2026-10-05に、ボスを強くした（`difficulty-scale.ts`）ぶん、以前より0.15下げた。 */
  target: number;
}

const dungeon = (id: string) => DUNGEON_ENEMIES.find((e) => e.id === id)!;

const CASES: BossCase[] = [
  { name: "第1章「水涸れの歪み」", level: 5, companions: 1, make: createMugikanoYugami, target: 0.63 },
  { name: "第2章「積荷の歪み」", level: 7, companions: 2, make: createGarasukoYugami, target: 0.68 },
  { name: "第3章「実験の歪み」", level: 9, companions: 3, make: createTetsukusariYugami, target: 0.63 },
  { name: "第4章「砂嵐の歪み」", level: 11, companions: 4, make: createSanoneSunaarashiYugami, target: 0.61 },
  { name: "第5章「予言の歪み」", level: 13, companions: 4, make: createKiriYogenYugami, target: 0.60 },
  { name: "第6章「試作機の歪み」", level: 15, companions: 4, make: createShimoharaShisakukiYugami, target: 0.57 },
  { name: "第7章「監視卓の歪み」", level: 17, companions: 5, make: createFushimaKanshitakuYugami, target: 0.60 },
  { name: "第8章「灯芯都の番人の歪み」", level: 19, companions: 5, make: createToushinBanninYugami, target: 0.59 },
  { name: "終章「光の守り手」", level: 21, companions: 5, make: createKyotoukyuGuardian, target: 0.75 },
  { name: "終章「合議会代表エドレア」（1戦目）", level: 21, companions: 5, make: createKyotoukyuEdreaFirst, target: 0.87 },
  { name: "終章「虚灯をまとうエドレア」（2戦目。1戦目の傷を持ちこす）", level: 21, companions: 5, make: createKyotoukyuEdreaYugami, target: 0.43 },
  { name: "深部の中ボス「歪みの残響」", level: 23, companions: 5, make: createDeepEchoYugami, target: 0.74 },
  { name: "裏ボス「初源の歪み」", level: 25, companions: 5, make: createShogenYugami, target: 0.33 },
  ...GODS.map((god, i) => ({
    name: `8神 ${god.kind}「${god.name}」`,
    level: 28,
    companions: 5,
    make: () => createGodYugami(god),
    target: [0.74, 0.71, 0.7, 0.74, 0.72, 0.64, 0.71, 0.64].map((t) => Math.max(0.2, t - 0.15))[i],
  })),
  { name: "塔の強敵「雲路の結晶獣」", level: 30, companions: 5, make: () => createDungeonEnemy(dungeon("tower2-guard")), target: 0.69 },
  { name: "塔の宝の番人「環光の番人」", level: 32, companions: 5, make: () => createDungeonEnemy(dungeon("tower3-guard")), target: 0.52 },
  { name: "環奥の「裂け目の守り手」", level: 34, companions: 5, make: () => createDungeonEnemy(dungeon("kanou3-guard")), target: 0.45 },
  { name: "ラスト裏ボス「全環」", level: 36, companions: 5, make: () => createDungeonEnemy(dungeon("zenkan")), target: 0.25 },
];

describe("ボスのバランス（想定レベルの仲間つきパーティ、300回のシミュレーション）", () => {
  for (const c of CASES) {
    it(`${c.name}（Lv${c.level}）: 勝率が目安${Math.round(c.target * 100)}%の前後`, () => {
      const { rate } = winRate(partyAtLevel(c.level, c.companions), () => [strengthenBoss(c.make())]);
      expect(rate, `勝率 ${(rate * 100).toFixed(1)}%`).toBeGreaterThanOrEqual(c.target - 0.1);
      expect(rate, `勝率 ${(rate * 100).toFixed(1)}%`).toBeLessThanOrEqual(c.target + 0.1);
    });
  }

  it("章が進むほど、ボスの体力は大きくなる（本編のボス）", () => {
    const hps = [createMugikanoYugami, createGarasukoYugami, createTetsukusariYugami, createSanoneSunaarashiYugami, createKiriYogenYugami, createShimoharaShisakukiYugami, createFushimaKanshitakuYugami, createToushinBanninYugami, createKyotoukyuEdreaYugami].map((f) => f().maxHp);
    for (let i = 1; i < hps.length; i++) {
      expect(hps[i], `第${i + 1}章のボスが、前の章より体力が小さい`).toBeGreaterThan(hps[i - 1]);
    }
  });
});
