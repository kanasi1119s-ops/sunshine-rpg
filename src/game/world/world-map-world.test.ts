import { describe, expect, it } from "vitest";
import { worldEntryProblems } from "./world-map-world";
import { isletRequirementHint } from "./islets-world";
import { WORLD_MAPS } from "./world";

describe("世界地図の入場条件（章は順番に進む）", () => {
  it("最初の町は、いつでも入れる。次の町は、前の章を終えるまで入れない", () => {
    expect(worldEntryProblems("touri-town", {})).toEqual([]);
    expect(worldEntryProblems("mugikano-village", {}).length).toBeGreaterThan(0);
    expect(worldEntryProblems("mugikano-village", { chapter0_reported_to_kasen: true })).toEqual([]);
  });

  it("章の順に、前の章の報告が条件になっている（9つの町が一列につながる）", () => {
    const order = ["mugikano-village", "garasuko-town", "tetsukusari-town", "sanone-town", "kiri-town", "shimohara-town", "fushima-town", "toushin-town", "kyotoukyu-court"];
    for (const town of order) {
      expect(worldEntryProblems(town, {}).length, town).toBeGreaterThan(0);
    }
  });

  it("隠しダンジョンの小島は、乗り物と章の進み具合の条件がそろうまで入れない。飛空艇でないと行けない島もある", () => {
    expect(isletRequirementHint("islet-1-1", {}).length).toBe(2);
    expect(isletRequirementHint("islet-1-1", { has_ship: true, chapter5_reported: true })).toEqual([]);
    expect(isletRequirementHint("islet-4-1", { has_ship: true, chapter8_reported: true }).length).toBe(1);
    expect(isletRequirementHint("islet-4-1", { has_airship: true, chapter8_reported: true })).toEqual([]);
  });

  it("芯環塔は、渦の航路が開くまで入れない", () => {
    expect(worldEntryProblems("tower-1", {}).length).toBe(1);
    expect(worldEntryProblems("tower-1", { vortex_route_open: true })).toEqual([]);
  });

  it("世界地図の出入り口は、町10か所（虚灯宮を含む）・村8つ・小島4つ・芯環塔1つ", () => {
    const targets = (WORLD_MAPS["world-map"].exits ?? []).map((e) => e.targetMapId);
    expect(targets.length).toBe(23);
    expect(targets).toContain("tower-1");
    expect(targets.filter((t) => t.startsWith("islet-")).length).toBe(4);
  });
});
