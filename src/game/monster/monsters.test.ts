import { describe, expect, it } from "vitest";
import { buildMonsterCells, MONSTER_GRID_SIZE, MONSTERS, type MonsterSpec } from "./monsters";

const SAMPLE_SPEC: MonsterSpec = {
  body: "#6a3fa8",
  core: "#b98fe0",
  eye: "#f2c14e",
  spikeCount: 7,
  spikeAmplitude: 0.35,
  baseRadiusRatio: 0.8,
};

describe("buildMonsterCells", () => {
  it("グリッドの範囲内のマスだけを返す", () => {
    for (const cell of buildMonsterCells(SAMPLE_SPEC)) {
      expect(cell.row).toBeGreaterThanOrEqual(0);
      expect(cell.row).toBeLessThan(MONSTER_GRID_SIZE);
      expect(cell.col).toBeGreaterThanOrEqual(0);
      expect(cell.col).toBeLessThan(MONSTER_GRID_SIZE);
    }
  });

  it("すべて有効な#rrggbb形式の色になる", () => {
    for (const cell of buildMonsterCells(SAMPLE_SPEC)) {
      expect(cell.color).toMatch(/^#[0-9a-f]{6}$/i);
    }
  });

  it("同じ仕様なら毎回同じ結果になる（時刻・乱数に依存しない）", () => {
    expect(buildMonsterCells(SAMPLE_SPEC)).toEqual(buildMonsterCells(SAMPLE_SPEC));
  });

  it("目の色のマスを少なくとも1つ含む", () => {
    const cells = buildMonsterCells(SAMPLE_SPEC);
    expect(cells.some((c) => c.color.toLowerCase() === SAMPLE_SPEC.eye.toLowerCase())).toBe(true);
  });

  it("ある程度の広さの塊になる（点だけ・全面だけにならない）", () => {
    const cells = buildMonsterCells(SAMPLE_SPEC);
    const totalCells = MONSTER_GRID_SIZE * MONSTER_GRID_SIZE;
    expect(cells.length).toBeGreaterThan(totalCells * 0.1);
    expect(cells.length).toBeLessThan(totalCells * 0.9);
  });
});

describe("MONSTERS", () => {
  it("序章・第1章のボスが登録されている", () => {
    expect(MONSTERS["chapter0-yugami"]).toBeDefined();
    expect(MONSTERS["mugikano-yugami"]).toBeDefined();
  });

  it("登録されている敵は、みな異なる見た目になる（設定値が同一ではない）", () => {
    const specs = Object.values(MONSTERS);
    const unique = new Set(specs.map((s) => JSON.stringify(s)));
    expect(unique.size).toBe(specs.length);
  });
});
