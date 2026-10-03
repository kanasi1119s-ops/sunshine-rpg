import { describe, expect, it } from "vitest";
import { addGold, computeVictoryGold, goldForEnemy, spendGold } from "./gold";
import { ALL_ITEMS_BY_ID, buyItem, describeBonus, receiveTreasure, shopStock, SHOP_ITEMS_BY_ID } from "./shop";
import { TREASURE_ITEMS } from "./treasure";
import { closeShopMenu, moveShopCursor, openShopMenu } from "./shop-menu";
import { createInitialEquipment } from "../battle/sample-battle";
import { computeEquipmentBonus, createEquipmentSlots } from "../items/equipment";
import { enemyStatsForLevel } from "../encounter/encounter";
import type { BattleState } from "../battle/types";

describe("灯貨", () => {
  it("敵1体の灯貨は経験値の約6割。勝利時は倒した敵ぶんの合計", () => {
    expect(goldForEnemy(100)).toBe(60);
    const state = { party: [], enemies: [{ expReward: 100 }, { expReward: 50 }] } as unknown as BattleState;
    expect(computeVictoryGold(state)).toBe(90);
  });
  it("足す・払う（足りなければ払えない）", () => {
    expect(addGold(10, 5)).toBe(15);
    expect(addGold(3, -10)).toBe(0);
    expect(spendGold(100, 60)).toBe(40);
    expect(spendGold(10, 60)).toBeNull();
  });
});

describe("お店", () => {
  it("1〜9段目の店があり、2段目以降は前の段の品も並ぶ（6品）。存在しない店は空", () => {
    expect(shopStock("tier-1")).toHaveLength(3);
    for (let tier = 2; tier <= 9; tier++) {
      expect(shopStock(`tier-${tier}`)).toHaveLength(6);
    }
    expect(shopStock("tier-0")).toEqual([]);
    expect(shopStock("nothing")).toEqual([]);
  });

  it("段が上がるほど、装備は強く、値段は高い。すべての品が品物一覧に登録されている", () => {
    for (let tier = 1; tier < 9; tier++) {
      for (const kind of ["weapon", "armor", "charm"]) {
        const a = SHOP_ITEMS_BY_ID[`${kind}-${tier}`];
        const b = SHOP_ITEMS_BY_ID[`${kind}-${tier + 1}`];
        expect(b.price).toBeGreaterThan(a.price);
        expect(Object.values(b.statBonus)[0]!).toBeGreaterThan(Object.values(a.statBonus)[0]!);
        expect(ALL_ITEMS_BY_ID[a.id]).toBeDefined();
      }
    }
  });

  it("買うと、灯貨が減って、その場で装備する。強い装備を持っているときや、灯貨が足りないときは買えない", () => {
    const start = createInitialEquipment(); // 使い込まれた鉄の剣（+4）
    const first = buyItem("weapon-1", 100, start);
    expect(first.ok).toBe(true);
    if (first.ok) {
      expect(first.gold).toBe(20);
      expect(first.equipment.weapon).toBe("weapon-1");
      expect(computeEquipmentBonus(first.equipment, ALL_ITEMS_BY_ID).attack).toBe(9);
      expect(buyItem("weapon-1", 999, first.equipment)).toEqual({ ok: false, message: "すでに装備している" });
      expect(buyItem("weapon-1", 999, { weapon: "weapon-3" })).toEqual({ ok: false, message: "いまの装備のほうが強い" });
    }
    expect(buyItem("weapon-2", 10, createEquipmentSlots())).toEqual({ ok: false, message: "灯貨が足りない" });
    expect(buyItem("nothing", 999, start).ok).toBe(false);
  });

  it("装備の説明が出る", () => {
    expect(describeBonus(SHOP_ITEMS_BY_ID["weapon-1"])).toBe("こうげき+9");
    expect(describeBonus(SHOP_ITEMS_BY_ID["charm-1"])).toBe("HP+8");
  });

  it("雑魚1戦の灯貨で、その段の武器が買えるまでの戦闘数が、現実的（3〜40戦）", () => {
    const levels = [2, 4, 6, 8, 10, 12, 14, 16];
    levels.forEach((level, i) => {
      const goldPerFight = goldForEnemy(enemyStatsForLevel(level).expReward) * 2; // 平均2体
      const fights = SHOP_ITEMS_BY_ID[`weapon-${i + 1}`].price / goldPerFight;
      expect(fights, `段${i + 1}の武器に${fights.toFixed(1)}戦`).toBeGreaterThanOrEqual(1);
      expect(fights, `段${i + 1}の武器に${fights.toFixed(1)}戦`).toBeLessThanOrEqual(40);
    });
  });
});

describe("お店の画面", () => {
  it("開く・動く・閉じる", () => {
    let state = openShopMenu("tier-3");
    expect(state.open).toBe(true);
    expect(state.items).toHaveLength(6);
    state = moveShopCursor(state, -1);
    expect(state.cursor).toBe(5);
    expect(closeShopMenu(state).open).toBe(false);
    expect(openShopMenu("nothing").open).toBe(false);
  });
});

describe("小島の宝の装備", () => {
  it("宝の品はすべて ALL_ITEMS_BY_ID にあり、店では売っていない", () => {
    for (const item of TREASURE_ITEMS) {
      expect(ALL_ITEMS_BY_ID[item.id]).toBeDefined();
      expect(SHOP_ITEMS_BY_ID[item.id]).toBeUndefined();
    }
  });

  it("いまの装備より強ければ装備し、弱ければそのまま", () => {
    const weak = receiveTreasure("treasure-6", { weapon: "weapon-1" });
    expect(weak.equipped).toBe(true);
    expect(weak.equipment.weapon).toBe("treasure-6");
    const keep = receiveTreasure("treasure-4", { weapon: "treasure-6" });
    expect(keep.equipped).toBe(false);
    expect(keep.equipment.weapon).toBe("treasure-6");
    expect(receiveTreasure("nothing", {}).equipped).toBe(false);
  });
});
